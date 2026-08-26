"""Week orchestrator - the full Daily-5 build (all 5 lanes, LLM-written).

For each day it sources content, has the LLM (writer.py) write all on-screen copy
+ captions, renders each lane from its design library, and patches the day-based
`data/weeks.json` as `in-review`. Runs locally or in the cloud (daily5-build.yml).

    python3 tools/build_week.py                 # full 5-day week
    python3 tools/build_week.py --days 1         # just Monday (cheap validation)
    python3 tools/build_week.py --dry            # plan only, no render/write
"""
import os, sys, json, datetime
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
import lane_quote, lane_fun, lane_employer, lane_education

HUB   = os.path.dirname(L.BASE)
WEEKS = os.path.join(HUB, "data", "weeks.json")
AUTO  = os.path.join(L.BASE, "video", "topics", "auto.json")
DKEYS = ["mon", "tue", "wed", "thu", "fri"]


def target_week():
    """Which week to build. Env WEEK_ID/WEEK_WC/WEEK_LABEL override; otherwise the
    UPCOMING week (next Monday), numbered relative to week14 = w/c 2026-08-31."""
    wid = os.getenv("WEEK_ID")
    if wid:
        wc = os.getenv("WEEK_WC", "")
        mon = datetime.date.fromisoformat(wc) if wc else datetime.date.today()
        return wid, os.getenv("WEEK_LABEL", "Week " + wid.replace("week", "")), mon.isoformat(), mon
    ref, refn = datetime.date(2026, 8, 31), 14
    today = datetime.date.today()
    ahead = (0 - today.weekday()) % 7 or 7          # next Monday
    mon = today + datetime.timedelta(days=ahead)
    n = refn + (mon - ref).days // 7
    return f"week{n}", f"Week {n}", mon.isoformat(), mon

QUOTE = [("editorial", "q001"), ("spotlight", "q002"), ("colorblock", "q003"),
         ("split", "q004"), ("paper", "q005")]
FUN = [("bingo", "bingo"), ("tierlist", "tier_list"), ("greenflags", "green_flags"),
       ("pov", "pov"), ("starterpack", "checklist")]
EMPLOYER = [("benefits", "e001"), ("bigstat", "e004"), ("process", "e003"),
            ("trust", "e005"), ("statement", "e002")]
# education: 3 carousels + 2 singles, rotating worlds
EDU_WORLDS = [("navy", "carousel"), ("plum", "carousel"), ("teal", "carousel"),
              ("tipcard", "single"), ("statement", "single")]

FUN_ONSCREEN = {"bingo": "Graduate job-hunt bingo - the shared truths of the search",
                "tierlist": "Interview questions ranked by dread (S to B tier)",
                "greenflags": "Green flags in a good internship: real tasks, a mentor, honest feedback, fair pay",
                "pov": "POV: you just got the 'we'd love to offer you the role' email",
                "starterpack": "The 'I'm basically a pro now' starter pack"}

PAID_BLOCK = ("paid", "unpaid", "internship-rights")   # never make paid-vs-unpaid content


def pick_education(n):
    topics = json.load(open(AUTO)).get("topics", [])
    out = []
    for t in topics:
        hay = (t.get("title", "") + " " + t.get("source_cluster", "")).lower()
        if any(b in hay for b in PAID_BLOCK):
            continue                                   # brand: all internships should be paid
        out.append(t)
        if len(out) >= n:
            break
    return out


def _post(pid, day, lane, title, fmt, slides, captions, hashtags):
    return {"id": pid, "day": day, "lane": lane, "title": title,
            "platform": "Multi-Platform", "format": fmt, "slides": slides,
            "status": "in-review", "caption": captions.get("ig-fb", ""),
            "hashtags": hashtags.get("ig-fb", []), "captions": captions,
            "hashtagsByPlatform": hashtags}


def build(days=5, dry=False):
    quotes = {q["id"]: q for q in L.load("quotes_bank.json")["quotes"]}
    ideas  = {i["format"]: i for i in L.load("fun_ideas.json")["ideas"]}
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    wid, wlabel, wc, mon = target_week()
    img = os.path.join(HUB, "images", wid)
    daylist = [(DKEYS[i], (mon + datetime.timedelta(days=i)).strftime("%a %d %b").replace(" 0", " ")) for i in range(5)]
    news_pool = news_fetch.fetch(limit=15)
    edu_topics = pick_education(days)
    posts = []
    print(f"Building {wid} (w/c {wc}) - {days} day(s)")

    for di in range(days):
        dkey, dlabel = daylist[di]
        print(f"\n=== {dlabel} ===")

        # NEWS - LLM reworded
        item = news_pool[di] if di < len(news_pool) else news_fetch.sample_item()
        nc = writer.write_news(item)
        pdate = datetime.datetime.combine(mon, datetime.time()) + datetime.timedelta(days=di)
        pid = f"{wid}-{dkey}-news"
        if not dry:
            news_card.render_news({"kicker": nc.get("kicker", "JOB MARKET"), "date": pdate},
                                  os.path.join(img, pid), issue_no=di + 1,
                                  headline=nc["headline"], brief=nc["brief"],
                                  sidebar=nc["sidebar"], pull=nc["pull"])
        posts.append(_post(pid, dlabel, "news", nc["headline"], "Single", ["slide_1.png"],
                           nc["captions"], nc["hashtags"]))

        # QUOTE
        world, qid = QUOTE[di]; q = quotes[qid]
        cap = writer.write_captions("quote", f"Quote by {q['author']}", q["text"], q.get("cta"))
        pid = f"{wid}-{dkey}-quote"
        if not dry:
            lane_quote.render_quote(q, world, os.path.join(img, pid))
        posts.append(_post(pid, dlabel, "quote", f"Quote: {q['author']}", "Single", ["slide_1.png"],
                           cap["captions"], cap["hashtags"]))

        # FUN
        world, fkey = FUN[di]; idea = ideas.get(fkey, {})
        cap = writer.write_captions("fun", FUN_ONSCREEN[world], FUN_ONSCREEN[world])
        pid = f"{wid}-{dkey}-fun"
        if not dry:
            lane_fun.render_fun(idea, world, os.path.join(img, pid))
        posts.append(_post(pid, dlabel, "fun", FUN_ONSCREEN[world].split(" - ")[0].split(":")[0],
                           "Single", ["slide_1.png"], cap["captions"], cap["hashtags"]))

        # EMPLOYER
        world, aid = EMPLOYER[di]; a = angles[aid]
        onscreen = a["headline"] + ". " + a.get("body", "") + " " + " ".join(a.get("benefits", []))
        cap = writer.write_captions("employer", a["headline"], onscreen)
        pid = f"{wid}-{dkey}-employer"
        if not dry:
            lane_employer.render_employer(a, world, os.path.join(img, pid))
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
            paths = lane_education.render_education(ec, world, os.path.join(img, pid))
            slides = [os.path.basename(p) for p in sorted(paths)]
        else:
            slides = ["slide_1.png"] * (7 if fmt == "carousel" else 1)
        posts.append(_post(pid, dlabel, "education", ec.get("headline", tp["title"]),
                           "Carousel" if fmt == "carousel" else "Single", slides,
                           ec["captions"], ec["hashtags"]))

    if not dry:
        news_fetch.mark_used(news_pool[:days])
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
    data["weeks"] = [w for w in data["weeks"] if w.get("id") != wid]
    data["weeks"].append({"id": wid, "label": wlabel, "weekCommencing": wc, "posts": posts})
    json.dump(data, open(WEEKS, "w"), indent=2, ensure_ascii=False)
    print(f"\nWrote {len(posts)} posts to weeks.json ({wid}).")
    return posts


if __name__ == "__main__":
    days = 5
    for i, a in enumerate(sys.argv):
        if a == "--days" and i + 1 < len(sys.argv):
            days = int(sys.argv[i + 1])
    build(days=days, dry="--dry" in sys.argv)
