"""One-off: rebuild Week 15 EDUCATION to kill the repeat-from-week14 problem.

- Mon/Tue/Wed carousels: 3 FRESH deduped topics + the new rotated worlds, fresh LLM copy.
- Thu/Fri singles: SAME approved copy (transcribed from the live slides) re-rendered
  in their new rotated single worlds (so they no longer match week14's Thu/Fri look).
Renders into images/week15/<pid>/ and patches data/weeks.json. Does NOT upload
(inspect first, then r2 upload). Task 3 (Mon slide5 tablet) + Task 4 (Wed cover
recut) are applied as separate steps after this base render.
"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_week as bw
import lane_education as edu
import writer
import lanes_common as L

WID = "week15"
HUB = bw.HUB
WEEKS = bw.WEEKS
IMG = os.path.join(HUB, "images", WID)

# 3 fresh carousel topics (editorial pick: distinct clusters, no week14/kept overlap)
CAROUSEL_TITLES = ["Your LinkedIn Profile Is Too Empty To Trust",
                   "Your Cover Letter Is Too Polite",
                   "Why Your Job Search Feels Random"]

# Thu/Fri approved single copy, transcribed from the current live slides.
THU_COPY = {"eyebrow": "CV INSIGHTS", "headline": "Why Your CV Gets Skipped",
            "points": ["Focus on role fit first", "Describe actions, not tasks",
                       "Show results, not duties", "Highlight top skills early",
                       "Avoid hiding proof on page two"],
            "cta": "Boost your CV at internwise.co.uk"}
FRI_COPY = {"eyebrow": "ASSESSMENT TIPS", "headline": "Quiet Wins at Assessment Centres",
            "points": ["Show useful behaviour under stress.",
                       "Include quiet voices in discussions.",
                       "Summarise to show leadership skills.",
                       "Facilitate decisions, don't dominate."],
            "cta": "internwise.co.uk"}


def _nodash(s):
    if isinstance(s, str):
        return s.replace("—", " - ").replace("–", "-")
    if isinstance(s, list):
        return [_nodash(x) for x in s]
    if isinstance(s, dict):
        return {k: _nodash(v) for k, v in s.items()}
    return s


def strip_week_from_ledger():
    import nuno_ledger as nl
    log = nl._load()
    log["uses"] = [u for u in log.get("uses", []) if u.get("week") != WID]
    nl._save(log)
    print("stripped", WID, "from nuno_ledger")


def topic_by_title(title):
    topics = json.load(open(bw.AUTO)).get("topics", [])
    t = next(x for x in topics if x["title"] == title)
    return {"title": t.get("title", ""), "hook": (t.get("hook_candidates") or [""])[0],
            "promise": t.get("promise", ""), "core_takeaway": t.get("core_takeaway", ""),
            "proof_points": t.get("proof_points", [])}


def main():
    strip_week_from_ledger()
    patch = {}   # pid -> dict of weeks.json fields to update

    # --- carousels: Mon(0) Tue(1) Wed(2) ---
    for di, title in zip(range(3), CAROUSEL_TITLES):
        dkey = bw.DKEYS[di]
        world, fmt = bw.education_world(di, WID)
        assert fmt == "carousel", (di, fmt)
        tp = topic_by_title(title)
        print(f"\n=== {dkey} carousel: {title}  (world={world}) ===")
        ec = _nodash(writer.write_education(tp, fmt="carousel", slides=3))
        pid = f"{WID}-{dkey}-education"
        paths = edu.render_education(ec, world, os.path.join(IMG, pid), week_id=WID)
        slides = [os.path.basename(p) for p in sorted(paths)]
        patch[pid] = {"title": ec.get("headline", title), "format": "Carousel",
                      "slides": slides, "caption": ec["captions"].get("ig-fb", ""),
                      "hashtags": ec["hashtags"].get("ig-fb", []),
                      "captions": ec["captions"], "hashtagsByPlatform": ec["hashtags"]}

    # --- singles: Thu(3) Fri(4) - keep copy, new world only ---
    for di, copy in ((3, THU_COPY), (4, FRI_COPY)):
        dkey = bw.DKEYS[di]
        world, fmt = bw.education_world(di, WID)
        assert fmt == "single", (di, fmt)
        pid = f"{WID}-{dkey}-education"
        print(f"\n=== {dkey} single (world={world}) : {copy['headline']} ===")
        edu.render_education(copy, world, os.path.join(IMG, pid), week_id=WID)
        # image only; weeks.json copy/caption unchanged

    # --- patch weeks.json ---
    data = json.load(open(WEEKS))
    wk = next(w for w in data["weeks"] if w.get("label") == "Week 15" or w.get("id") == WID)
    for p in wk["posts"]:
        if p["id"] in patch:
            p.update(patch[p["id"]])
    json.dump(data, open(WEEKS, "w"), indent=2, ensure_ascii=False)
    print("\npatched weeks.json for:", ", ".join(patch))


if __name__ == "__main__":
    main()
