"""Week orchestrator - the weekly evergreen build (quote, conversation, education).

For each day it sources content, has the LLM (writer.py) write all on-screen copy
+ captions, renders each active lane from its design library, and patches the day-based
`data/weeks.json` as `in-review`. Runs locally or in the cloud (daily5-build.yml).

NEWS is deliberately NOT built here - it is generated exactly one day before it
posts by build_news_day.py (news-daily.yml) so headlines are never stale. This
batch preserves any news posts already present for the week when it rewrites the
entry. The active weekly evergreen set is Quote, Poll/Conversation, and Education.
News is day-prior. Featured jobs are separate and employer acquisition graphics are not
part of the weekly batch unless the user explicitly asks to bring them back.

    python3 tools/build_week.py                 # full 5-day week
    python3 tools/build_week.py --days 1         # just Monday (cheap validation)
    python3 tools/build_week.py --dry            # plan only, no render/write
    WEEK_ID=week23 python3 tools/build_week.py --start 1   # late build: Tue-Fri of week23
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
# Polls are paused (Nov 2026): too little channel activity for them to earn replies.
# Flip back to True to bring the poll/conversation lane back into the weekly build.
POLLS_ENABLED = False
TOPIC_REPEAT_OVERRIDE_ENV = "IW_ALLOW_TOPIC_REPEAT"                      # explicit emergency override only
DKEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
NEWS_IMAGE_USED = os.path.join(L.BASE, "content", "news_image_used.json")
AYRSHARE_POSTED = os.path.join(L.BASE, "content", "ayrshare_posted.json")
NEWS_ASSET_BANK = os.path.join(L.BASE, "assets", "news", "news_asset_bank.json")


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
# 18 worlds for 5 slots a week. At 15 the bank was exactly three weeks deep, so
# with a 2-week block the "least recently used" pick had no choice left and the
# lane ran a locked 3-week cycle (week21 shipped week18's five designs). The spare
# three give the rotation slack.
QUOTE_WORLDS = ["editorial", "spotlight", "colorblock", "split", "paper",
                "arc", "blueprint", "band", "minimal", "bubble",
                "marquee", "stamp", "notebook", "gallery", "manifesto",
                "prism", "monument", "horizon"]
# Employer acquisition graphics were dropped from the weekly batch. Keep the renderer
# library for manual one-offs, but do not generate employer posts unless this set is
# explicitly re-enabled.
EMPLOYER_DAYS = set()
EMPLOYER_PAIRS = [("benefits", "e001"), ("bigstat", "e004"), ("process", "e003"),
                  ("trust", "e005"), ("statement", "e002")]
# All employer worlds (incl. the week16 additions) + a compatible angle for CTA copy.
# World SELECTION now goes through the design ledger (no-repeat), not this list's rotation.
EMPLOYER_WORLDS = ["benefits", "bigstat", "process", "trust", "statement", "kpi", "cards", "pipeline", "proofboard",
                   "command", "talentmap", "goodcompany", "fastmatch"]
EMPLOYER_ANGLE = {"benefits": "e001", "bigstat": "e004", "process": "e003",
                  "trust": "e005", "statement": "e002", "kpi": "e004", "cards": "e001",
                  "pipeline": "e003", "proofboard": "e004", "command": "e006", "talentmap": "e004",
                  "goodcompany": "e005", "fastmatch": "e004"}
# education: 3 carousels + 2 singles. The FORMAT is fixed per weekday (Mon-Wed
# carousels, Thu/Fri singles) so the weekly mix never drifts; the visual WORLD
# rotates by week (see week_offset / build) so the same weekday never looks the
# same two weeks running.
EDU_FORMAT_BY_DAY = ["carousel", "carousel", "carousel", "single", "single"]
EDU_CAROUSEL_WORLDS = ["navy", "plum", "teal", "cream", "midnight", "slate",
                       "marker", "flash", "tabs", "ledger", "grid", "strip"]
# message_lab / focus_studio / answerbank were authored into lane_education.SINGLE
# but never listed here, so the ledger could only ever see 6 of the 9 singles.
EDU_SINGLE_WORLDS = ["tipcard", "statement", "bigidea", "splitcard", "memo", "scorecard",
                     "message_lab", "focus_studio", "answerbank", "badge"]
CONVERSATION_WORLDS = ["decision", "proofboard", "debate", "scorecard", "signal",
                       "vote_cards", "shortlist_poll", "cv_poll", "route_map", "comment_wall",
                       "ballot", "dial", "receipt", "stickies", "bars", "marquee"]


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


EDU_COLLIDE_THRESH = 0.34     # Jaccard; ~the old 0.5 overlap for equal-length titles
COLLIDE_MIN_WORDS = 2         # a one-word set is too thin to call a repeat on


def sets_collide(a, b, thresh, metric="jaccard", min_words=COLLIDE_MIN_WORDS):
    """True when two significant-word sets describe the same topic.

    metric="jaccard" divides the intersection by the UNION. The original
    overlap coefficient divided by min(len(a), len(b)), which turned any short
    set into a mass blocker: a two-word used-set blocked every title sharing
    ONE word with it (1/2 = 0.5), which is how the single word "experience"
    retired a whole topic. Union scaling judges the pair rather than its
    shorter member.

    metric="overlap" keeps the original coefficient for news, where both sets
    are full headlines of comparable length and 0.4 is tuned for them; there
    only the min_words floor is new.
    """
    if not a or not b or len(a) < min_words or len(b) < min_words:
        return False
    denom = len(a | b) if metric == "jaccard" else min(len(a), len(b))
    return len(a & b) / denom >= thresh


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
        if any(sets_collide(ws, ps, thresh, metric="overlap") for ps in picked_sets):
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


def pick_education(n, used_sets=None, thresh=EDU_COLLIDE_THRESH):
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
        return any(sets_collide(ws, us, thresh) for us in used_sets)

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

    Hard rule: news cards must use a relevant article image. Queries must be
    tied to the selected story or story category. Do not use generic workplace
    fallbacks just to make image selection succeed.
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
    # Preserve order while removing duplicates.
    return list(dict.fromkeys(q for q in queries if q.strip()))


def _news_image_caption(item, headline):
    bank_caption = item.get("_image_caption")
    if bank_caption:
        return bank_caption
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
            "at": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z",
        })
        os.makedirs(os.path.dirname(NEWS_IMAGE_USED), exist_ok=True)
        json.dump(log, open(NEWS_IMAGE_USED, "w"), indent=2, ensure_ascii=False)
    return sha


def _news_image_seen(path):
    sha = _file_sha256(path)
    seen = {row.get("sha256") for row in _load_news_image_used().get("images", [])}
    return sha in seen


def _load_news_asset_bank():
    try:
        data = json.load(open(NEWS_ASSET_BANK))
    except Exception:
        return []
    return [a for a in data.get("assets", []) if a.get("path")]


def _pick_bank_news_image(item, headline):
    """Pick an approved repo asset that matches the story.

    Manual/operator builds can pass an explicit `--image`; the unattended cloud
    workflow uses Pexels by default because GitHub Actions cannot call Codex's
    built-in ImageGen.
    """
    source = _news_source_text(item, headline)
    candidates = []
    for asset in _load_news_asset_bank():
        path = asset["path"]
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(L.BASE), path)
        if not os.path.exists(path) or _news_image_seen(path):
            continue
        keywords = [str(k).lower() for k in asset.get("keywords", [])]
        score = sum(1 for kw in keywords if kw and kw in source)
        if score:
            candidates.append((score, path, asset))
    if not candidates:
        return None
    _, path, asset = sorted(candidates, key=lambda row: row[0], reverse=True)[0]
    item["_image_caption"] = asset.get("caption") or _news_image_caption(item, headline)
    _remember_news_image(path, headline, "approved-news-asset-bank")
    return path


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
            "News cards require a relevant, non-repeated image. Configure PEXELS_API_KEY "
            "for the default cloud image source, or pass image_path explicitly for a "
            "manual editorial asset. Generic workplace fallback images are not allowed; "
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


def preflight(days=5):
    """Dry capacity check: run every picker that can refuse to build, render
    nothing, write nothing. Returns True when the week would build.

    This exists because the Saturday build was the FIRST place a topic or
    design shortfall showed up - by then the week is already late. Run it
    mid-week and a shortfall surfaces while there is still time to restock.
    Every picker below is read-only (design_ledger.pick and the topic pickers
    all defer their ledger writes to a matching record() call), so this is safe
    to run on a schedule.
    """
    wid, _, wc, _ = target_week()
    print(f"PRE-FLIGHT {wid} (w/c {wc}) - {days} day(s), nothing is rendered or written\n")

    quotes = {q["id"]: q for q in L.load("quotes_bank.json")["quotes"]}
    conversation_ideas = L.load("conversation_ideas.json")["ideas"]
    fmts = EDU_FORMAT_BY_DAY[:days]

    checks = [
        ("education topics", lambda: [t.get("title", "") for t in pick_education(days)]),
        ("quote picks", lambda: pick_quote_ids(quotes, days, wid)),
        *([("conversation picks", lambda: [c.get("id") for c in pick_conversation_ideas(conversation_ideas, days, wid)])]
          if POLLS_ENABLED else []),
        ("quote designs", lambda: design_ledger.pick("quote", QUOTE_WORLDS, days, wid)),
        *([("conversation designs", lambda: design_ledger.pick("conversation", CONVERSATION_WORLDS, days, wid))]
          if POLLS_ENABLED else []),
        ("edu carousel designs", lambda: design_ledger.pick("edu_carousel", EDU_CAROUSEL_WORLDS, fmts.count("carousel"), wid)),
        ("edu single designs", lambda: design_ledger.pick("edu_single", EDU_SINGLE_WORLDS, fmts.count("single"), wid)),
    ]
    emp_days = sorted(d for d in EMPLOYER_DAYS if d < days)
    if emp_days:
        checks.append(("employer designs",
                       lambda: design_ledger.pick("employer", EMPLOYER_WORLDS, len(emp_days), wid)))

    failures = []
    for label, fn in checks:
        try:
            got = fn()
            print(f"  OK    {label}: {got}")
        except Exception as exc:
            failures.append((label, exc))
            print(f"  FAIL  {label}: {type(exc).__name__}: {exc}")

    print()
    if failures:
        print(f"PRE-FLIGHT FAILED for {wid} - {len(failures)} of {len(checks)} check(s):")
        for label, exc in failures:
            print(f"  - {label}: {exc}")
        print("\nThe Saturday build will fail on these unless the banks are restocked.")
        return False
    print(f"PRE-FLIGHT PASSED - {wid} has everything it needs to build.")
    return True


def build(days=5, dry=False, start=0):
    # start > 0 skips weekdays that have already passed (a late build mid-week):
    # posts keep their real day ids, and every pick is sized to the remaining days.
    slots = list(range(start, days))
    n = len(slots)
    quotes = {q["id"]: q for q in L.load("quotes_bank.json")["quotes"]}
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    conversation_ideas = L.load("conversation_ideas.json")["ideas"]
    wid, wlabel, wc, mon = target_week()
    # Rotate the quote bank by week, but block recent quote IDs/authors so the
    # same quote cannot reappear just because the visual world changed.
    week_quotes = pick_quote_ids(quotes, n, wid)
    week_conversation = pick_conversation_ideas(conversation_ideas, n, wid) if POLLS_ENABLED else []

    # DESIGN SELECTION goes through the no-repeat ledger (the hard rule: a new
    # design direction per post every week). Each lane picks worlds NOT used in
    # the recent lookback window; if the bank is too shallow, design_ledger raises
    # instead of silently reusing a stale look. Replaces the old week_offset rotation.
    def pick_worlds(lane, bank, k, full):
        # The repeat window is sized from a FULL week (`full` posts), not `k`: pick()
        # derives it from the bank / posts ratio, so a late Tue-Fri build would
        # otherwise widen the window and block worlds a normal week may use.
        window = max(design_ledger.DEFAULT_AVOID_WEEKS, design_ledger.cycle_weeks(bank, full) - 1)
        return design_ledger.pick(lane, bank, k, wid, avoid_weeks=window)

    q_worlds = pick_worlds("quote", QUOTE_WORLDS, n, days)
    emp_days = sorted(d for d in EMPLOYER_DAYS if start <= d < days)
    emp_worlds = design_ledger.pick("employer", EMPLOYER_WORLDS, len(emp_days), wid)
    week_emp = {d: (emp_worlds[i], EMPLOYER_ANGLE[emp_worlds[i]]) for i, d in enumerate(emp_days)}
    # avoid_weeks=1 blocked only the single previous week, and the bank held exactly
    # 10 worlds for 5 slots, so the lane alternated between two fixed sets: week19
    # and week21 shipped the identical five designs. 16 worlds + a 2-week block
    # means a conversation design cannot come back inside three weeks.
    conversation_worlds = pick_worlds("conversation", CONVERSATION_WORLDS, n, days) if POLLS_ENABLED else []
    fmts = [EDU_FORMAT_BY_DAY[i] for i in slots]
    full_fmts = EDU_FORMAT_BY_DAY[:days]
    edu_car = pick_worlds("edu_carousel", EDU_CAROUSEL_WORLDS, fmts.count("carousel"), full_fmts.count("carousel"))
    edu_sing = pick_worlds("edu_single", EDU_SINGLE_WORLDS, fmts.count("single"), full_fmts.count("single"))
    car_i = sing_i = 0
    img = os.path.join(HUB, "images", wid)
    daylist = [(DKEYS[i], (mon + datetime.timedelta(days=i)).strftime("%a %d %b").replace(" 0", " ")) for i in range(5)]
    edu_topics = pick_education(n)
    if not dry:
        record_edu_used(wid, [t.get("title", "") for t in edu_topics])
    posts = []
    print(f"Building {wid} (w/c {wc}) - {n} day(s)" + (f", from {daylist[start][1]}" if start else ""))

    for si, di in enumerate(slots):
        dkey, dlabel = daylist[di]
        print(f"\n=== {dlabel} ===")

        # NEWS is built day-prior by build_news_day.py so it is never stale.

        # QUOTE
        world = q_worlds[si]; qid = week_quotes[si]; q = quotes[qid]
        cap = writer.write_captions("quote", f"Quote by {q['author']}", q["text"], q.get("cta"))
        pid = f"{wid}-{dkey}-quote"
        if not dry:
            lane_quote.render_quote(q, world, os.path.join(img, pid))
        posts.append(_post(pid, dlabel, "quote", f"Quote: {q['author']}", "Single", ["slide_1.png"],
                           cap["captions"], cap["hashtags"]))
        posts[-1]["quoteId"] = qid
        posts[-1]["world"] = world

        # POLL / CONVERSATION lane. Keep it useful and brand-safe; featured jobs
        # remain a separate queue.
        if POLLS_ENABLED:
            idea = week_conversation[si]
            world = conversation_worlds[si]
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

        # EMPLOYER - disabled by default. Featured jobs remain separate.
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
        topic = edu_topics[si] if si < len(edu_topics) else {"title": "Career tips", "hook": "", "promise": "", "core_takeaway": "", "proof_points": []}
        tp = {"title": topic.get("title", ""), "hook": (topic.get("hook_candidates") or [""])[0],
              "promise": topic.get("promise", ""), "core_takeaway": topic.get("core_takeaway", ""),
              "proof_points": topic.get("proof_points", [])}
        ec = writer.write_education(tp, fmt=fmt, slides=3)   # cover + 3 teaching + CTA = 5-slide carousel
        poses = {}
        pid = f"{wid}-{dkey}-education"
        if not dry:
            # Keep the chosen cutouts on the post so rerender_week.py can replay them;
            # without them a single post cannot be re-rendered later.
            poses = lane_education.choose_poses(ec, world, wid)
            paths = lane_education.render_education(ec, world, os.path.join(img, pid), week_id=wid, poses=poses)
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
        if not dry and poses:
            posts[-1]["poses"] = poses

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
        design_ledger.record("quote", wid, q_worlds[:n])
        if emp_worlds:
            design_ledger.record("employer", wid, emp_worlds)
        if edu_car:
            design_ledger.record("edu_carousel", wid, edu_car)
        if edu_sing:
            design_ledger.record("edu_single", wid, edu_sing)
        if conversation_worlds:
            design_ledger.record("conversation", wid, conversation_worlds[:n])

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
    days, start = 5, 0
    for i, a in enumerate(sys.argv):
        if a == "--days" and i + 1 < len(sys.argv):
            days = int(sys.argv[i + 1])
        if a == "--start" and i + 1 < len(sys.argv):
            start = int(sys.argv[i + 1])           # 1 = start Tuesday, for a late build
    if "--preflight" in sys.argv:
        sys.exit(0 if preflight(days=days) else 1)
    build(days=days, dry="--dry" in sys.argv, start=start)
