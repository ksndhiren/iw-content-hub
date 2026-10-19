"""rerender_week.py - re-render an ALREADY BUILT week's graphics in place.

Use this when a design or typography fix needs to reach a week that has already
shipped to the dashboard. The copy is read back out of data/weeks.json, so
nothing about the words, the topics or the lane assignments changes - only the
pixels. build_week.py is for creating a week; this is for correcting one.

    python3 tools/rerender_week.py week21
    python3 tools/rerender_week.py week21 --only week21-mon-engagement,week21-thu-engagement
    python3 tools/rerender_week.py week21 --world week21-mon-engagement=ballot
    python3 tools/rerender_week.py week21 --upload          # push to R2 as well
    python3 tools/rerender_week.py week21 --dry             # plan only

Two things bite every time this is done by hand, so they are handled here:

1. builtAt. app.js cache-busts every image URL with ?v=<week.builtAt>, and R2
   serves the files with a one-year immutable cache. Re-rendering a slide under
   the same filename WITHOUT bumping builtAt leaves every viewer looking at the
   copy their browser already cached - the fix is live on R2 and invisible on the
   dashboard. This script always re-stamps builtAt.

2. nuno_ledger. nuno_ledger.pick() APPENDS a row on every call, so simply
   re-running the education lane makes the poses the original build chose look
   "recently used" and the next-best pose gets picked instead. That is how an
   overwhelm pose once landed on an instructional CV hook. Posts carry a `poses`
   record so a re-render replays exactly what shipped. A post built before that
   existed has none, so a FULL re-render clears the week's own ledger rows and
   re-picks in build order, which reproduces the original choice and stores it;
   a partial re-render of such a post cannot reproduce it and is refused.

The news lane is never touched: it is built day-prior and auto-scheduled, so a
re-render could only desynchronise it from what has already gone to Ayrshare.
"""
from __future__ import annotations
import os, sys, json, argparse, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import lane_education as E, lane_quote as QL, lane_conversation as CL
import design_ledger

HUB = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEEKS = os.path.join(HUB, "data", "weeks.json")
NUNO = os.path.join(HUB, "social-media", "content", "nuno_ledger.json")
SKIP_LANES = {"news"}


def _write_json(path, data):
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def clear_nuno_rows(wid):
    """Drop this week's own pose rows so pick() reproduces the original build."""
    led = json.load(open(NUNO))
    before = len(led["uses"])
    led["uses"] = [u for u in led["uses"] if u.get("week") != wid]
    dropped = before - len(led["uses"])
    if dropped:
        _write_json(NUNO, led)
    return dropped


def needs_pose_replay(targets):
    """Education carousels with no stored `poses`. Their cutouts depend on ledger
    order, so they can only be reproduced by re-picking the whole week in build
    order - re-rendering a few of them in isolation would reshuffle the rest."""
    return [p for p in targets
            if p.get("lane") == "education" and p.get("world") in E.CAROUSEL and not p.get("poses")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("week", help="week id, e.g. week21")
    ap.add_argument("--only", default="", help="comma-separated post ids to re-render (default: every non-news post)")
    ap.add_argument("--world", action="append", default=[], metavar="PID=WORLD",
                    help="move a post onto a different design world, e.g. week21-mon-engagement=ballot")
    ap.add_argument("--upload", action="store_true", help="upload the re-rendered posts to R2 afterwards")
    ap.add_argument("--dry", action="store_true", help="print the plan and change nothing")
    args = ap.parse_args()

    wid = args.week
    data = json.load(open(WEEKS))
    week = next((w for w in data["weeks"] if w.get("id") == wid), None)
    if week is None:
        raise SystemExit(f"{wid} is not in {WEEKS}.")

    only = {s.strip() for s in args.only.split(",") if s.strip()}
    overrides = {}
    for spec in args.world:
        pid, _, world = spec.partition("=")
        if not world:
            raise SystemExit(f"--world expects PID=WORLD, got {spec!r}.")
        overrides[pid.strip()] = world.strip()

    targets = [p for p in week["posts"]
               if p.get("lane") not in SKIP_LANES and (not only or p["id"] in only)]
    unknown = only - {p["id"] for p in targets}
    if unknown:
        raise SystemExit(f"not in {wid} (or is a news post): {', '.join(sorted(unknown))}")
    if not targets:
        raise SystemExit(f"nothing to re-render in {wid}.")

    print(f"{wid}: {len(targets)} post(s)")
    for p in targets:
        world = overrides.get(p["id"], p.get("world"))
        flag = "  (world change)" if p["id"] in overrides and overrides[p["id"]] != p.get("world") else ""
        print(f"  {p['id']:28} {p.get('lane',''):11} {world}{flag}")
    full = not only
    stale = needs_pose_replay(targets)
    if stale and not full:
        raise SystemExit(
            "These posts have no stored `poses`, so their founder cutouts cannot be "
            "reproduced in isolation:\n  " + "\n  ".join(p["id"] for p in stale) +
            f"\nRe-run without --only to re-pick {wid} in build order (this stores the "
            "poses, after which targeting them individually works).")
    if args.dry:
        print("\nDRY: nothing rendered, weeks.json untouched, builtAt not stamped.")
        return

    # Only safe on a full pass: clearing drops rows for posts we are not about to
    # re-render, which would lose their cutouts from the no-repeat history.
    if full and stale:
        print(f"\ncleared {clear_nuno_rows(wid)} {wid} nuno_ledger rows to re-pick in build order")

    img = os.path.join(HUB, "images", wid)
    ideas = {i["id"]: i for i in L.load("conversation_ideas.json")["ideas"]}
    quotes = {q["id"]: q for q in L.load("quotes_bank.json")["quotes"]}

    done = []
    for p in targets:
        pid, lane = p["id"], p["lane"]
        p["world"] = overrides.get(pid, p.get("world"))
        out = os.path.join(img, pid)
        if lane == "education":
            # Replay the stored cutouts when we have them; otherwise pick now and
            # record them on the post so every later re-render is deterministic.
            poses = p.get("poses") or E.choose_poses(p["onSlide"], p["world"], wid)
            if poses:
                p["poses"] = poses
            E.render_education(p["onSlide"], p["world"], out, week_id=wid, poses=poses)
        elif lane == "engagement":
            CL.render_conversation(ideas[p["ideaId"]], p["world"], out)
        elif lane == "quote":
            QL.render_quote(quotes[p["quoteId"]], p["world"], out)
        else:
            print(f"  ! no renderer for lane {lane!r}; skipped {pid}")
            continue
        done.append(p)

    # Re-stamp so app.js's ?v=<builtAt> cache-buster actually points at a new URL.
    old = week.get("builtAt")
    week["builtAt"] = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    _write_json(WEEKS, data)
    print(f"\nbuiltAt {old} -> {week['builtAt']} (cache-buster stamped)")

    # Keep the design ledger honest about which worlds this week actually used,
    # so next week's no-repeat window blocks what is really on the page.
    for lane, key in (("engagement", "conversation"), ("quote", "quote")):
        used = sorted({p["world"] for p in week["posts"] if p.get("lane") == lane and p.get("world")})
        if used:
            design_ledger.record(key, wid, used)

    if args.upload:
        import r2
        if not os.getenv("R2_ACCESS_KEY_ID"):
            print("\n! --upload given but R2_ACCESS_KEY_ID is not set; skipped.")
        else:
            r2.ensure_bucket()
            for p in done:
                r2.upload_tree(os.path.join(img, p["id"]), prefix=f"{wid}/{p['id']}/")
            print(f"uploaded {len(done)} post(s) to R2.")

    print(f"\nre-rendered {len(done)} post(s) in {wid}.")
    print("Commit data/weeks.json - without the new builtAt the dashboard keeps "
          "serving the cached images.")


if __name__ == "__main__":
    main()
