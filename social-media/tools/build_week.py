"""Week orchestrator - the weekly evergreen build (quote, employer, education).

For each day it sources content, has the LLM (writer.py) write all on-screen copy
+ captions, renders each lane from its design library, and patches the day-based
`data/weeks.json` as `in-review`. Runs locally or in the cloud (daily5-build.yml).

NEWS is deliberately NOT built here - it is generated exactly one day before it
posts by build_news_day.py (news-daily.yml) so headlines are never stale. This
batch preserves any news posts already present for the week when it rewrites the
entry. Daily-5 means five core reviewable posts per posting day; featured jobs
are separate and do not count toward the core five. The fifth core post is Poll/Conversation
(stored as lane "engagement" for dashboard/publishing compatibility).

    python3 tools/build_week.py                 # full 5-day week
    python3 tools/build_week.py --days 1         # just Monday (cheap validation)
    python3 tools/build_week.py --dry            # plan only, no render/write
"""
import os, sys, json, re, datetime, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L


def _load_env():
    """Load social-media/.env (and repo .env) so OPENAI_API_KEY etc. are present
    when run locally. Cloud secrets are already in os.environ and win (setdefault)."""
    for path in (os.path.join(L.BASE, ".env"), os.path.join(os.path.dirname(L.BASE), ".env")):
        if os.path.exists(path):
            for line in open(path):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
_load_env()

import writer, news_fetch, news_card
import lane_quote, lane_employer, lane_education, lane_conversation
import nuno_ledger
import design_ledger   # enforces the hard rule: a new design per post every week

HUB   = os.path.dirname(L.BASE)
WEEKS = os.path.join(HUB, "data", "weeks.json")
AUTO  = os.path.join(L.BASE, "video", "topics", "auto.json")
EDU_USED = os.path.join(L.BASE, "content", "education_used.json")   # cross-week topic dedup
EDU_DEDUP_WEEKS = 2                                                  # don't reuse a topic within N weeks
QUOTE_DEDUP_WEEKS = 4                                                # do not repeat quote text/author in recent weeks
CONVERSATION_DEDUP_WEEKS = 8                                         # do not repeat fifth-post ideas in recent weeks
TOPIC_REPEAT_OVERRIDE_ENV = "IW_ALLOW_TOPIC_REPEAT"                      # explicit emergency override only
DKEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
NEWS_IMAGE_USED = os.path.join(L.BASE, "content", "news_image_used.json")
AYRSHARE_POSTED = os.path.join(L.BASE, "content", "ayrshare_posted.json")


class TopicFreshnessError(RuntimeError):
    """Raised when content planning would need to repeat a recent topic."""


def topic_repeat_allowed():
    return os.getenv(TOPIC_REPEAT_OVERRIDE_ENV, "").strip().lower() in {"1", "true", "yes", "y"}


def _load_posted_ids():
    """Return post ids with at least one successful Ayrshare send/schedule.

    The Ayrshare ledger is the source of truth for content that has already gone
    live or is queued to go live. Keys are shaped like
    `week19-wed-quote:instagram` or `week19-wed-quote:instagram:story`.
    """
    try:
        data = json.load(open(AYRSHARE_POSTED))
    except Exception:
        return set()
    return {str(k).split(":", 1)[0] for k in data.keys()}


def _posted_posts(lanes=None):
    """Return week posts that appear in the Ayrshare posted ledger."""
    posted_ids = _load_posted_ids()
    if not posted_ids:
        return []
    lanes = set(lanes or [])
    try:
        data = json.load(open(WEEKS))
    except Exception:
        return []
    out = []
    for week in data.get("weeks", []):
        for post in week.get("posts", []):
            if post.get("id") not in posted_ids:
                continue
            if lanes and post.get("lane") not in lanes:
                continue
            out.append(post)
    return out


def _posted_title_words(lanes):
    return [_edu_words(p.get("title", "")) for p in _posted_posts(lanes)
            if p.get("title")]


def posted_titles(lanes):
    """Titles of content already sent/scheduled through Ayrshare for hard dedup."""
    return [p.get("title", "") for p in _posted_posts(lanes) if p.get("title")]


def target_week():
    """Which week to build. Env WEEK_ID/WEEK_WC/WEEK_LABEL override; otherwise the
    UPCOMING week (next Monday), numbered relative to week14 = w/c 2026-08-31."""
    ref, refn = datetime.date(2026, 8, 31), 14        # week14 = w/c 2026-08-31
    wid = os.getenv("WEEK_ID")
    if wid:
        wc = os.getenv("WEEK_WC", "")
        if wc:
            mon = datetime.date.fromisoformat(wc)
        else:                                          # derive Monday from the week number
            try:
                mon = ref + datetime.timedelta(weeks=int(wid.replace("week", "")) - refn)
            except ValueError:
                mon = datetime.date.today()
        return wid, os.getenv("WEEK_LABEL", "Week " + wid.replace("week", "")), mon.isoformat(), mon
    today = datetime.date.today()
    ahead = (0 - today.weekday()) % 7 or 7          # next Monday
    mon = today + datetime.timedelta(days=ahead)
    n = refn + (mon - ref).days // 7
    return f"week{n}", f"Week {n}", mon.isoformat(), mon

# Visual worlds cycle every day; the QUOTE TEXT rotates weekly through the whole
# bank (see build()) so no two consecutive weeks repeat the same 5 quotes.
QUOTE_WORLDS = ["editorial", "spotlight", "colorblock", "split", "paper",
                "arc", "blueprint", "band", "minimal", "bubble",
                "marquee", "stamp"]
# Employer is a core Daily-5 lane and must run every weekday. Featured jobs are
# a separate sixth queue, never a substitute for missing core-grid posts.
EMPLOYER_DAYS = {0, 1, 2, 3, 4}
EMPLOYER_PAIRS = [("benefits", "e001"), ("bigstat", "e004"), ("process", "e003"),
                  ("trust", "e005"), ("statement", "e002")]
# All employer worlds (incl. the week16 additions) + a compatible angle for CTA copy.
# World SELECTION now goes through the design ledger (no-repeat), not this list's rotation.
EMPLOYER_WORLDS = ["benefits", "bigstat", "process", "trust", "statement", "kpi", "cards", "pipeline", "proofboard",
                   "command", "talentmap"]
EMPLOYER_ANGLE = {"benefits": "e001", "bigstat": "e004", "process": "e003",
                  "trust": "e005", "statement": "e002", "kpi": "e004", "cards": "e001",
                  "pipeline": "e003", "proofboard": "e004", "command": "e006", "talentmap": "e004"}
# education: 3 carousels + 2 singles. The FORMAT is fixed per weekday (Mon-Wed
# carousels, Thu/Fri singles) so the weekly mix never drifts; the visual WORLD
# rotates by week (see week_offset / build) so the same weekday never looks the
# same two weeks running.
EDU_FORMAT_BY_DAY = ["carousel", "carousel", "carousel", "single", "single"]
EDU_CAROUSEL_WORLDS = ["navy", "plum", "teal", "cream", "midnight", "slate",
                       "marker", "flash", "tabs"]
EDU_SINGLE_WORLDS = ["tipcard", "statement", "bigidea", "splitcard", "memo", "scorecard"]
CONVERSATION_WORLDS = ["decision", "proofboard", "debate", "scorecard", "signal",
                       "vote_cards", "shortlist_poll", "cv_poll", "route_map", "comment_wall"]


def week_offset(wid):
    """Per-week rotation step (0 for week14, +1 each week after) used to advance
    the quote/education visual worlds so consecutive weeks never share a look."""
    try:
        return int(wid.replace("week", "")) - 14
    except ValueError:
        return 0


def quote_world(di, wid):
    return QUOTE_WORLDS[(di + week_offset(wid)) % len(QUOTE_WORLDS)]


def education_world(di, wid):
    """(world, fmt) for a given weekday, rotating the world within its format
    group so Mon/Wed stay carousels but land on a fresh colour world each week."""
    off = week_offset(wid)
    fmt = EDU_FORMAT_BY_DAY[di]
    if fmt == "carousel":
        return EDU_CAROUSEL_WORLDS[(di + off) % len(EDU_CAROUSEL_WORLDS)], fmt
    return EDU_SINGLE_WORLDS[((di - EDU_FORMAT_BY_DAY.index("single")) + off) % len(EDU_SINGLE_WORLDS)], fmt

PAID_BLOCK = ("paid", "unpaid", "internship-rights")   # never make paid-vs-unpaid content


_NEWS_STOP = {"with", "from", "your", "this", "that", "will", "says", "said",
              "survey", "suggests", "amid", "after", "over", "into", "more", "most",
              "than", "have", "been", "could", "would", "should", "their", "them",
              "they", "what", "when", "which", "where", "about", "just", "year",
              "years", "week", "month", "new", "uk", "gov"}


def _news_words(title):
    return {w for w in re.findall(r"[a-z]+", (title or "").lower())
            if len(w) >= 4 and w not in _NEWS_STOP}


def pick_distinct_news(pool, n, thresh=0.4):
    """Greedily pick `n` news items whose headlines don't repeat a topic already
    chosen this week. Two items count as the same story when their significant
    headline words overlap >= `thresh` (overlap coefficient) - e.g. the two
    'graduate vacancies at a multi-year low' stories that used to land twice in
    one week. Backfills from the pool if fewer than `n` distinct items exist."""
    picked, picked_sets = [], []
    for it in pool:
        ws = _news_words(it.get("title", ""))
        if any(ws and ps and len(ws & ps) / min(len(ws), len(ps)) >= thresh
               for ps in picked_sets):
            continue
        picked.append(it); picked_sets.append(ws)
        if len(picked) >= n:
            return picked
    for it in pool:                                   # backfill if too few distinct
        if it not in picked:
            picked.append(it)
            if len(picked) >= n:
                break
    return picked


SIGNALS = os.path.join(L.BASE, "content", "planning_signals.json")


def _demand_terms():
    """Significant words from the operator's weekly GSC search-demand topics
    (planning_signals.json, written by ingest_analytics.py). Empty if not present
    yet - education planning then falls back to plain topic order."""
    try:
        sig = json.load(open(SIGNALS))
    except Exception:
        return []
    terms = []
    for t in sig.get("searchDemandTopics", []):
        ws = {w for w in re.findall(r"[a-z]+", t.get("query", "").lower()) if len(w) >= 4}
        if ws:
            terms.append((ws, t.get("impressions", 0)))
    return terms


_EDU_STOP = {"your", "the", "that", "this", "with", "without", "into", "from",
             "what", "when", "why", "how", "are", "not", "too", "keep", "feels",
             "is", "a", "an", "and", "for", "of", "to"}


def _edu_words(title):
    return {w for w in re.findall(r"[a-z]+", (title or "").lower())
            if len(w) >= 4 and w not in _EDU_STOP}


def load_edu_used(weeks=EDU_DEDUP_WEEKS):
    """Word-sets of education topics used in the last `weeks` build weeks, so we
    never repeat a topic (or a near-duplicate) two weeks running - the way the
    11-topic bank used to resurface the same 5 every week."""
    try:
        rows = json.load(open(EDU_USED)).get("used", [])
    except Exception:
        return []
    recent = sorted({r.get("week", "") for r in rows}, reverse=True)[:weeks]
    return [_edu_words(r.get("title", "")) for r in rows if r.get("week") in recent]


def record_edu_used(wid, titles):
    try:
        data = json.load(open(EDU_USED))
    except Exception:
        data = {"used": []}
    data["used"] = [r for r in data.get("used", []) if r.get("week") != wid]
    data["used"] += [{"week": wid, "title": t} for t in titles]
    os.makedirs(os.path.dirname(EDU_USED), exist_ok=True)
    json.dump(data, open(EDU_USED, "w"), indent=2, ensure_ascii=False)


def pick_education(n, used_sets=None, thresh=0.5):
    """Pick `n` education topics, demand-ranked, skipping any that repeat a topic
    used in the recent weeks (`used_sets`; defaults to the last EDU_DEDUP_WEEKS)
    OR any education topic already sent/scheduled through Ayrshare. Raises instead
    of silently repeating unless IW_ALLOW_TOPIC_REPEAT=1 is set."""
    topics = json.load(open(AUTO)).get("topics", [])
    demand = _demand_terms()
    used_sets = list(load_edu_used() if used_sets is None else used_sets)
    used_sets += _posted_title_words({"education"})

    def demand_score(t):
        """Higher when a topic matches what people actually search (GSC)."""
        hay = {w for w in re.findall(r"[a-z]+", (t.get("title", "") + " " +
               t.get("source_cluster", "")).lower()) if len(w) >= 4}
        return sum(impr for ws, impr in demand if hay & ws)

    eligible = [t for t in topics
                if not any(b in (t.get("title", "") + " " + t.get("source_cluster", "")).lower()
                           for b in PAID_BLOCK)]                # all internships should be paid
    if demand:
        # Stable sort: demand-matching topics first (by search volume), order kept otherwise.
        eligible = sorted(eligible, key=demand_score, reverse=True)

    def is_recent(t):
        ws = _edu_words(t.get("title", ""))
        return any(ws and us and len(ws & us) / min(len(ws), len(us)) >= thresh
                   for us in used_sets)

    fresh = [t for t in eligible if not is_recent(t)]
    picked = fresh[:n]
    if len(picked) < n:
        if not topic_repeat_allowed():
            raise TopicFreshnessError(
                f"Education topic bank has only {len(fresh)} fresh topic(s) for {n} slot(s) "
                "after excluding recent and already posted content. Add new education topics "
                f"or set {TOPIC_REPEAT_OVERRIDE_ENV}=1 for an explicit emergency repeat."
            )
        picked += [t for t in eligible if t not in picked][: n - len(picked)]
    return picked


def _post(pid, day, lane, title, fmt, slides, captions, hashtags):
    return {"id": pid, "day": day, "lane": lane, "title": title,
            "platform": "Multi-Platform", "format": fmt, "slides": slides,
            "status": "in-review", "caption": captions.get("ig-fb", ""),
            "hashtags": hashtags.get("ig-fb", []), "captions": captions,
            "hashtagsByPlatform": hashtags}


def _recent_quote_blocks(wid, weeks=QUOTE_DEDUP_WEEKS):
    """Return quote IDs/authors used in recent weeks. Legacy posts may not have
    quoteId, so use their `Quote: Author` title as a conservative fallback."""
    try:
        data = json.load(open(WEEKS))
    except Exception:
        return set(), set()
    current = week_offset(wid) + 14
    min_week = current - weeks
    blocked_ids, blocked_authors = set(), set()
    for week in data.get("weeks", []):
        wn = week_offset(week.get("id", "")) + 14
        if wn >= current or wn < min_week:
            continue
        for post in week.get("posts", []):
            if post.get("lane") != "quote":
                continue
            if post.get("quoteId"):
                blocked_ids.add(post["quoteId"])
            m = re.match(r"Quote:\s*(.+)", post.get("title", ""))
            if m:
                blocked_authors.add(m.group(1).strip().lower())
    return blocked_ids, blocked_authors


def pick_quote_ids(quotes, days, wid):
    """Pick quote IDs from the normal weekly rotation while blocking recent
    quote IDs/authors and anything already sent/scheduled through Ayrshare.
    Raises instead of silently repeating unless explicitly overridden."""
    def has_portrait(q):
        author = q.get("author", "")
        slug = re.sub(r"[^a-z0-9]+", "-", author.lower()).strip("-")
        auth_dir = os.path.join(L.BASE, "assets", "quote_authors")
        return any(os.path.exists(os.path.join(auth_dir, f"{slug}.{ext}"))
                   for ext in ("jpg", "jpeg", "png", "webp"))

    qids = sorted(quotes.keys())
    try:
        wn = int(wid.replace("week", ""))
    except ValueError:
        wn = 14
    qstart = ((wn - 14) * 5) % len(qids)
    rotated = [qids[(qstart + i) % len(qids)] for i in range(len(qids))]
    blocked_ids, blocked_authors = _recent_quote_blocks(wid)
    for post in _posted_posts({"quote"}):
        if post.get("quoteId"):
            blocked_ids.add(post["quoteId"])
        m = re.match(r"Quote:\s*(.+)", post.get("title", ""))
        if m:
            blocked_authors.add(m.group(1).strip().lower())
    fresh = [qid for qid in rotated
             if qid not in blocked_ids
             and quotes[qid].get("author", "").strip().lower() not in blocked_authors
             and has_portrait(quotes[qid])]
    if len(fresh) < days and not topic_repeat_allowed():
        raise TopicFreshnessError(
            f"Quote bank has only {len(fresh)} fresh portrait-backed quote(s) for {days} slot(s) "
            f"after the {QUOTE_DEDUP_WEEKS}-week lookback and already-posted filter. "
            f"Add real author portraits/quotes or set {TOPIC_REPEAT_OVERRIDE_ENV}=1 "
            "for an explicit emergency repeat."
        )
    fallback = [qid for qid in rotated if qid not in fresh and has_portrait(quotes[qid])]
    return (fresh + fallback)[:days]


def _recent_conversation_blocks(wid, weeks=CONVERSATION_DEDUP_WEEKS):
    """Return current conversation + legacy fun/engagement idea IDs/titles used in recent weeks."""
    try:
        data = json.load(open(WEEKS))
    except Exception:
        return set(), set()
    current = week_offset(wid) + 14
    min_week = current - weeks
    blocked_ids, blocked_titles = set(), set()
    for week in data.get("weeks", []):
        wn = week_offset(week.get("id", "")) + 14
        if wn >= current or wn < min_week:
            continue
        for post in week.get("posts", []):
            if post.get("lane") not in {"engagement", "fun"}:
                continue
            if post.get("ideaId"):
                blocked_ids.add(post["ideaId"])
            if post.get("title"):
                blocked_titles.add(post["title"].strip().lower())
    return blocked_ids, blocked_titles


def pick_conversation_ideas(conversation_ideas, days, wid):
    blocked_ids, blocked_titles = _recent_conversation_blocks(wid)
    for post in _posted_posts({"engagement", "fun"}):
        if post.get("ideaId"):
            blocked_ids.add(post["ideaId"])
        if post.get("title"):
            blocked_titles.add(post["title"].strip().lower())
    fresh = [idea for idea in conversation_ideas
             if idea.get("id") not in blocked_ids
             and idea.get("hook", "").strip().lower() not in blocked_titles]
    if len(fresh) < days and not topic_repeat_allowed():
        raise TopicFreshnessError(
            f"Conversation bank has only {len(fresh)} fresh idea(s) for {days} slot(s) after the "
            f"{CONVERSATION_DEDUP_WEEKS}-week lookback and already-posted filter. "
            f"Add conversation ideas or set {TOPIC_REPEAT_OVERRIDE_ENV}=1 for an explicit emergency repeat."
        )
    fallback = [idea for idea in conversation_ideas if idea not in fresh]
    return (fresh + fallback)[:days]


def _news_source_text(item, headline):
    return " ".join([
        headline or "",
        item.get("title", ""),
        item.get("summary", ""),
    ]).lower()


def _news_image_queries(item, headline):
    """Return article-specific image queries, ordered from precise to broad.

    Hard rule: news cards must use a relevant article image. The first query
    should describe the actual story; broad workplace fallbacks are last only.
    """
    source = _news_source_text(item, headline)
    clean_head = re.sub(r"[^a-zA-Z0-9 ]+", " ", headline or item.get("title", "")).strip()
    queries = []
    if any(w in source for w in ["award", "awards", "recognised", "recognized", "recruitment strategies", "talent recruitment"]):
        queries += [
            "UK recruitment awards hiring talent networking event",
            "business awards recruitment hiring team office event",
            "recruiters young professionals networking awards event",
        ]
    if "disabled" in source or "disability" in source or "long-term health" in source:
        queries += [
            "disabled young professional workplace support inclusive office",
            "inclusive workplace young disabled professional laptop",
            "young professional wheelchair office support employment",
        ]
    if "ai" in source or "automation" in source:
        queries += [
            "student professional technology workplace artificial intelligence",
            "young professionals laptop technology office artificial intelligence",
        ]
    if "skill" in source or "training" in source:
        queries += [
            "young professional skills training workplace",
            "early career training workshop office",
        ]
    if "north" in source or "investment" in source:
        queries += [
            "young professional workplace city office",
            "UK city office young professionals workplace",
        ]
    if clean_head:
        queries.append(f"{clean_head} UK workplace early career")
    queries += [
        "young professionals recruitment interview office",
        "early career candidates recruiter office meeting",
    ]
    # Preserve order while removing duplicates.
    return list(dict.fromkeys(q for q in queries if q.strip()))


def _news_image_caption(item, headline):
    source = _news_source_text(item, headline)
    if any(w in source for w in ["award", "awards", "recruitment strategies", "talent recruitment"]):
        return "Recruitment ideas, recognised on the awards floor."
    if "disabled" in source or "disability" in source or "long-term health" in source:
        return "Workplace support, turned into experience."
    if "ai" in source or "automation" in source:
        return "Technology is reshaping early-career hiring."
    if "skill" in source or "training" in source:
        return "Skills training is becoming career currency."
    return "The job market story behind the headline."


def _news_image_query(item, headline):
    # Backward-compatible helper for any older callers.
    return _news_image_queries(item, headline)[0]


def _load_news_image_used():
    try:
        return json.load(open(NEWS_IMAGE_USED))
    except Exception:
        return {"images": []}


def _file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _remember_news_image(path, headline, query, photo_id=None):
    log = _load_news_image_used()
    sha = _file_sha256(path)
    if not any(row.get("sha256") == sha for row in log.get("images", [])):
        log.setdefault("images", []).append({
            "sha256": sha,
            "headline": headline,
            "query": query,
            "photo_id": photo_id,
            "path": os.path.relpath(path, L.BASE),
            "at": datetime.datetime.utcnow().isoformat() + "Z",
        })
        os.makedirs(os.path.dirname(NEWS_IMAGE_USED), exist_ok=True)
        json.dump(log, open(NEWS_IMAGE_USED, "w"), indent=2, ensure_ascii=False)
    return sha


def _news_image_seen(path):
    sha = _file_sha256(path)
    seen = {row.get("sha256") for row in _load_news_image_used().get("images", [])}
    return sha in seen


def _fetch_required_news_image(item, headline):
    try:
        from pexels_utils import search_pexels, download_image
        errors = []
        for query in _news_image_queries(item, headline):
            try:
                photos = search_pexels(query, per_page=8, orientation="landscape")
            except Exception as exc:
                errors.append(f"{query}: {exc}")
                continue
            for photo in photos:
                url = photo["src"].get("large") or photo["src"].get("original")
                if not url:
                    continue
                path = download_image(url, f"news_{query}_{photo['id']}_large")
                if _news_image_seen(path):
                    continue
                _remember_news_image(path, headline, query, photo.get("id"))
                return path
        raise RuntimeError("all fetched candidates were missing or already used; " + " | ".join(errors[:3]))
    except Exception as exc:
        raise RuntimeError(
            "News cards require a relevant, non-repeated image. Use Codex ImageGen "
            "to create a project asset, or pass image_path explicitly; "
            f"image fetch failed for {headline!r}: {exc}"
        )


def build_news_post(wid, dkey, dlabel, pdate, img, item, issue_no=1, dry=False, image_path=None):
    """Build ONE news post: LLM rewrite + rendered news card -> post dict.

    Shared by the day-prior news job (build_news_day.py) so news is generated
    close to posting and never goes stale. The weekly batch (build) no longer
    builds news itself."""
    nc = writer.write_news(item)
    pid = f"{wid}-{dkey}-news"
    if not dry:
        image_path = image_path or _fetch_required_news_image(item, nc["headline"])
        news_card.render_news({"kicker": "JOB MARKET", "date": pdate},
                              os.path.join(img, pid), issue_no=issue_no,
                              headline=nc["headline"], brief=nc["brief"],
                              sidebar=nc["sidebar"], pull=nc["pull"],
                              image_path=image_path,
                              image_caption=_news_image_caption(item, nc["headline"]))
    return _post(pid, dlabel, "news", nc["headline"], "Single", ["slide_1.png"],
                 nc["captions"], nc["hashtags"])


def build(days=5, dry=False):
    quotes = {q["id"]: q for q in L.load("quotes_bank.json")["quotes"]}
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    conversation_ideas = L.load("conversation_ideas.json")["ideas"]
    wid, wlabel, wc, mon = target_week()
    # Rotate the quote bank by week, but block recent quote IDs/authors so the
    # same quote cannot reappear just because the visual world changed.
    week_quotes = pick_quote_ids(quotes, days, wid)
    week_conversation = pick_conversation_ideas(conversation_ideas, days, wid)

    # DESIGN SELECTION goes through the no-repeat ledger (the hard rule: a new
    # design direction per post every week). Each lane picks worlds NOT used in
    # the recent lookback window; if the bank is too shallow, design_ledger raises
    # instead of silently reusing a stale look. Replaces the old week_offset rotation.
    q_worlds = design_ledger.pick("quote", QUOTE_WORLDS, days, wid)
    emp_days = sorted(d for d in EMPLOYER_DAYS if d < days)
    emp_worlds = design_ledger.pick("employer", EMPLOYER_WORLDS, len(emp_days), wid)
    week_emp = {d: (emp_worlds[i], EMPLOYER_ANGLE[emp_worlds[i]]) for i, d in enumerate(emp_days)}
    conversation_worlds = design_ledger.pick("conversation", CONVERSATION_WORLDS, days, wid, avoid_weeks=1)
    fmts = EDU_FORMAT_BY_DAY[:days]
    edu_car = design_ledger.pick("edu_carousel", EDU_CAROUSEL_WORLDS, fmts.count("carousel"), wid)
    edu_sing = design_ledger.pick("edu_single", EDU_SINGLE_WORLDS, fmts.count("single"), wid)
    car_i = sing_i = 0
    img = os.path.join(HUB, "images", wid)
    daylist = [(DKEYS[i], (mon + datetime.timedelta(days=i)).strftime("%a %d %b").replace(" 0", " ")) for i in range(5)]
    edu_topics = pick_education(days)
    if not dry:
        record_edu_used(wid, [t.get("title", "") for t in edu_topics])
    posts = []
    print(f"Building {wid} (w/c {wc}) - {days} day(s)")

    for di in range(days):
        dkey, dlabel = daylist[di]
        print(f"\n=== {dlabel} ===")

        # NEWS is built day-prior by build_news_day.py so it is never stale.

        # QUOTE
        world = q_worlds[di]; qid = week_quotes[di]; q = quotes[qid]
        cap = writer.write_captions("quote", f"Quote by {q['author']}", q["text"], q.get("cta"))
        pid = f"{wid}-{dkey}-quote"
        if not dry:
            lane_quote.render_quote(q, world, os.path.join(img, pid))
        posts.append(_post(pid, dlabel, "quote", f"Quote: {q['author']}", "Single", ["slide_1.png"],
                           cap["captions"], cap["hashtags"]))
        posts[-1]["quoteId"] = qid
        posts[-1]["world"] = world

        # POLL / CONVERSATION lane - the fifth core Daily-5 surface.
        # Keep it useful and brand-safe; featured jobs remain a separate sixth queue.
        idea = week_conversation[di]
        world = conversation_worlds[di]
        visual_hook = idea.get("hook", "Career conversation")
        onscreen = ". ".join([visual_hook, idea.get("subhead", ""), idea.get("takeaway", ""), idea.get("cta", "")])
        cap = writer.write_captions("engagement", visual_hook, onscreen)
        pid = f"{wid}-{dkey}-engagement"
        if not dry:
            lane_conversation.render_conversation(idea, world, os.path.join(img, pid))
        posts.append(_post(pid, dlabel, "engagement", visual_hook, "Single", ["slide_1.png"],
                           cap["captions"], cap["hashtags"]))
        posts[-1]["world"] = world
        posts[-1]["ideaId"] = idea.get("id")

        # EMPLOYER - core Daily-5 lane. Featured jobs remain separate.
        if di in EMPLOYER_DAYS:
            world, aid = week_emp[di]; a = angles[aid]
            onscreen = a["headline"] + ". " + a.get("body", "") + " " + " ".join(a.get("benefits", []))
            cap = writer.write_captions("employer", a["headline"], onscreen)
            pid = f"{wid}-{dkey}-employer"
            if not dry:
                lane_employer.render_employer(a, world, os.path.join(img, pid), week_id=wid)
            posts.append(_post(pid, dlabel, "employer", a["headline"], "Single", ["slide_1.png"],
                               cap["captions"], cap["hashtags"]))
            posts[-1]["world"] = world

        # EDUCATION - LLM carousel/single. World comes from the ledger; format is
        # fixed per weekday (Mon-Wed carousel, Thu/Fri single).
        fmt = EDU_FORMAT_BY_DAY[di]
        if fmt == "carousel":
            world = edu_car[car_i]; car_i += 1
        else:
            world = edu_sing[sing_i]; sing_i += 1
        topic = edu_topics[di] if di < len(edu_topics) else {"title": "Career tips", "hook": "", "promise": "", "core_takeaway": "", "proof_points": []}
        tp = {"title": topic.get("title", ""), "hook": (topic.get("hook_candidates") or [""])[0],
              "promise": topic.get("promise", ""), "core_takeaway": topic.get("core_takeaway", ""),
              "proof_points": topic.get("proof_points", [])}
        ec = writer.write_education(tp, fmt=fmt, slides=3)   # cover + 3 teaching + CTA = 5-slide carousel
        pid = f"{wid}-{dkey}-education"
        if not dry:
            paths = lane_education.render_education(ec, world, os.path.join(img, pid), week_id=wid)
            slides = [os.path.basename(p) for p in sorted(paths)]
        else:
            slides = ["slide_1.png"] * (7 if fmt == "carousel" else 1)
        posts.append(_post(pid, dlabel, "education", ec.get("headline", tp["title"]),
                           "Carousel" if fmt == "carousel" else "Single", slides,
                           ec["captions"], ec["hashtags"]))
        # PERSIST the on-slide copy so a later re-render (e.g. a design change) never
        # has to regenerate it - the not-stored problem that used to force drift.
        posts[-1]["onSlide"] = {k: ec.get(k) for k in ("eyebrow", "headline", "tone", "slides", "points", "cta")}
        posts[-1]["world"] = world

    if not dry and nuno_ledger.REPEATS:
        need = {}
        for r in nuno_ledger.REPEATS:
            need[r["family"]] = need.get(r["family"], 0) + 1
        report = {"week": wid, "generatedAt": datetime.datetime.now(datetime.timezone.utc)
                  .strftime("%Y-%m-%dT%H:%M:%SZ"), "needByFamily": need,
                  "repeats": nuno_ledger.REPEATS}
        os.makedirs(os.path.join(L.BASE, "content"), exist_ok=True)
        json.dump(report, open(os.path.join(L.BASE, "content", "nuno_needed.json"), "w"),
                  indent=2, ensure_ascii=False)
        print("\n⚠ Nuno library short - poses REPEATED (need fresh cutouts): "
              + ", ".join(f"{n}×{fam}" for fam, n in need.items()))

    if not dry:
        # Commit the design choices so next week's build avoids them (the hard rule).
        design_ledger.record("quote", wid, q_worlds[:days])
        if emp_worlds:
            design_ledger.record("employer", wid, emp_worlds)
        if edu_car:
            design_ledger.record("edu_carousel", wid, edu_car)
        if edu_sing:
            design_ledger.record("edu_single", wid, edu_sing)
        if conversation_worlds:
            design_ledger.record("conversation", wid, conversation_worlds[:days])

    if not dry:
        # Render each story-lane post's 1080x1920 Story companion from its cover
        # slide, so ayrshare_publish --stories has media in R2. Done BEFORE the
        # upload so upload_tree ships story.png alongside the slides (otherwise
        # Facebook/Instagram Stories fail at post time with error 164).
        try:
            import story_card
            made = []
            for p in posts:
                if p.get("lane") not in story_card.STORY_LANES:
                    continue
                cover = (p.get("slides") or ["slide_1.png"])[0]
                src = os.path.join(img, p["id"], cover)
                if os.path.exists(src):
                    story_card.make_story(src, os.path.join(img, p["id"], "story.png"))
                    made.append(p["id"])
            print(f"rendered {len(made)} Story companions (story.png)")
        except Exception as e:
            print("story render skipped:", e)

        try:
            import r2                                     # normalises R2_* env on import
            if os.getenv("R2_ACCESS_KEY_ID"):
                r2.ensure_bucket()
                print(f"uploading {wid} slides + stories to R2 ...")
                r2.upload_tree(img, prefix=wid + "/")
        except Exception as e:
            print("R2 upload skipped:", e)

    if dry:
        print(f"\nDRY: planned {len(posts)} posts.")
        return posts

    data = json.load(open(WEEKS))
    # Preserve any news posts already added for this week by the day-prior news
    # job, so a batch re-run never wipes news that has been built/approved.
    prev = next((w for w in data["weeks"] if w.get("id") == wid), None)
    carry = [p for p in (prev or {}).get("posts", []) if p.get("lane") == "news"]
    data["weeks"] = [w for w in data["weeks"] if w.get("id") != wid]
    built_at = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    data["weeks"].append({"id": wid, "label": wlabel, "weekCommencing": wc,
                          "builtAt": built_at, "posts": posts + carry})
    json.dump(data, open(WEEKS, "w"), indent=2, ensure_ascii=False)
    print(f"\nWrote {len(posts)} posts to weeks.json ({wid})"
          + (f" (+{len(carry)} existing news preserved)" if carry else "") + ".")
    return posts


if __name__ == "__main__":
    days = 5
    for i, a in enumerate(sys.argv):
        if a == "--days" and i + 1 < len(sys.argv):
            days = int(sys.argv[i + 1])
    build(days=days, dry="--dry" in sys.argv)
