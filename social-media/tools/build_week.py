"""Week orchestrator - the weekly evergreen build (quote, employer, education).

For each day it sources content, has the LLM (writer.py) write all on-screen copy
+ captions, renders each lane from its design library, and patches the day-based
`data/weeks.json` as `in-review`. Runs locally or in the cloud (daily5-build.yml).

NEWS is deliberately NOT built here - it is generated the day before it posts by
build_news_day.py (news-daily.yml) so headlines are never stale. This batch
preserves any news posts already present for the week when it rewrites the entry.
The FUN lane was retired (Week 15) after it underperformed on every platform.

    python3 tools/build_week.py                 # full 5-day week
    python3 tools/build_week.py --days 1         # just Monday (cheap validation)
    python3 tools/build_week.py --dry            # plan only, no render/write
"""
import os, sys, json, re, datetime
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
import lane_quote, lane_employer, lane_education
import nuno_ledger

HUB   = os.path.dirname(L.BASE)
WEEKS = os.path.join(HUB, "data", "weeks.json")
AUTO  = os.path.join(L.BASE, "video", "topics", "auto.json")
DKEYS = ["mon", "tue", "wed", "thu", "fri"]


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
QUOTE_WORLDS = ["editorial", "spotlight", "colorblock", "split", "paper"]
EMPLOYER = [("benefits", "e001"), ("bigstat", "e004"), ("process", "e003"),
            ("trust", "e005"), ("statement", "e002")]
# education: 3 carousels + 2 singles, rotating worlds
EDU_WORLDS = [("navy", "carousel"), ("plum", "carousel"), ("teal", "carousel"),
              ("tipcard", "single"), ("statement", "single")]

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


def pick_education(n):
    topics = json.load(open(AUTO)).get("topics", [])
    demand = _demand_terms()

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
    return eligible[:n]


def _post(pid, day, lane, title, fmt, slides, captions, hashtags):
    return {"id": pid, "day": day, "lane": lane, "title": title,
            "platform": "Multi-Platform", "format": fmt, "slides": slides,
            "status": "in-review", "caption": captions.get("ig-fb", ""),
            "hashtags": hashtags.get("ig-fb", []), "captions": captions,
            "hashtagsByPlatform": hashtags}


def build_news_post(wid, dkey, dlabel, pdate, img, item, issue_no=1, dry=False):
    """Build ONE news post: LLM rewrite + rendered news card -> post dict.

    Shared by the day-prior news job (build_news_day.py) so news is generated
    close to posting and never goes stale. The weekly batch (build) no longer
    builds news itself."""
    nc = writer.write_news(item)
    pid = f"{wid}-{dkey}-news"
    if not dry:
        news_card.render_news({"kicker": nc.get("kicker", "JOB MARKET"), "date": pdate},
                              os.path.join(img, pid), issue_no=issue_no,
                              headline=nc["headline"], brief=nc["brief"],
                              sidebar=nc["sidebar"], pull=nc["pull"])
    return _post(pid, dlabel, "news", nc["headline"], "Single", ["slide_1.png"],
                 nc["captions"], nc["hashtags"])


def build(days=5, dry=False):
    quotes = {q["id"]: q for q in L.load("quotes_bank.json")["quotes"]}
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    wid, wlabel, wc, mon = target_week()
    # Rotate the quote bank by week so consecutive weeks never share quotes.
    qids = sorted(quotes.keys())
    try:
        wn = int(wid.replace("week", ""))
    except ValueError:
        wn = 14
    qstart = ((wn - 14) * 5) % len(qids)
    week_quotes = [qids[(qstart + i) % len(qids)] for i in range(5)]
    img = os.path.join(HUB, "images", wid)
    daylist = [(DKEYS[i], (mon + datetime.timedelta(days=i)).strftime("%a %d %b").replace(" 0", " ")) for i in range(5)]
    edu_topics = pick_education(days)
    posts = []
    print(f"Building {wid} (w/c {wc}) - {days} day(s)")

    for di in range(days):
        dkey, dlabel = daylist[di]
        print(f"\n=== {dlabel} ===")

        # NEWS is built day-prior by build_news_day.py so it is never stale.

        # QUOTE
        world = QUOTE_WORLDS[di]; qid = week_quotes[di]; q = quotes[qid]
        cap = writer.write_captions("quote", f"Quote by {q['author']}", q["text"], q.get("cta"))
        pid = f"{wid}-{dkey}-quote"
        if not dry:
            lane_quote.render_quote(q, world, os.path.join(img, pid))
        posts.append(_post(pid, dlabel, "quote", f"Quote: {q['author']}", "Single", ["slide_1.png"],
                           cap["captions"], cap["hashtags"]))

        # FUN lane retired (Week 15) - underperformed on every platform.

        # EMPLOYER
        world, aid = EMPLOYER[di]; a = angles[aid]
        onscreen = a["headline"] + ". " + a.get("body", "") + " " + " ".join(a.get("benefits", []))
        cap = writer.write_captions("employer", a["headline"], onscreen)
        pid = f"{wid}-{dkey}-employer"
        if not dry:
            lane_employer.render_employer(a, world, os.path.join(img, pid), week_id=wid)
        posts.append(_post(pid, dlabel, "employer", a["headline"], "Single", ["slide_1.png"],
                           cap["captions"], cap["hashtags"]))

        # EDUCATION - LLM carousel/single
        world, fmt = EDU_WORLDS[di]
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
        try:
            import r2                                     # normalises R2_* env on import
            if os.getenv("R2_ACCESS_KEY_ID"):
                r2.ensure_bucket()
                print(f"uploading {wid} slides to R2 ...")
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
