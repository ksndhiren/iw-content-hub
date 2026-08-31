"""Ayrshare publisher - posts APPROVED dashboard content to social networks.

The human gate is the dashboard: only posts whose status is "approved" in
data/weeks.json are eligible. Each post is sent to the networks that suit its
lane (intersected with the accounts actually connected in Ayrshare), using that
network's own caption + hashtags and the slide image(s) served from R2.

Safe by default: runs a DRY-RUN (prints the plan, calls nothing) unless --live
is given. Every live post is recorded in content/ayrshare_posted.json so a
re-run never double-posts.

    python3 tools/ayrshare_publish.py --week week14              # dry-run plan
    python3 tools/ayrshare_publish.py --week week14 --schedule   # dry-run + times
    python3 tools/ayrshare_publish.py --week week14 --live       # actually post
    python3 tools/ayrshare_publish.py --week week14 --live --schedule

Notes:
- Networks connected today: instagram, linkedin, threads (+ youtube/gmb unused).
  Facebook, X/Twitter and TikTok are NOT connected, so lanes that would target
  them simply skip those networks until they're linked in Ayrshare.
- Threads has a 500-char limit; long captions are trimmed for Threads only
  (and flagged). All other networks receive the full caption.
"""
from __future__ import annotations
import os, sys, json, argparse, datetime
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
HUB  = os.path.dirname(SM)
WEEKS = os.path.join(HUB, "data", "weeks.json")
POSTED = os.path.join(SM, "content", "ayrshare_posted.json")
R2_BASE = "https://pub-5f843c240ef6453bba67e131500424af.r2.dev"
API = "https://api.ayrshare.com/api/post"
USER_API = "https://api.ayrshare.com/api/user"


def _load_env():
    for p in (os.path.join(SM, ".env"), os.path.join(HUB, ".env")):
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
_load_env()
KEY = os.getenv("AYRSHARE_API_KEY", "")

# Ayrshare network -> which caption/hashtag key in weeks.json it should use.
NET_CAPTION = {"instagram": "ig-fb", "facebook": "ig-fb", "threads": "ig-fb",
               "linkedin": "linkedin", "twitter": "x"}
# Rough per-network caption character ceilings (trim only where needed).
NET_LIMIT = {"twitter": 280, "threads": 500, "instagram": 2200,
             "facebook": 63000, "linkedin": 3000}
# Lane -> the networks we WANT it on (before intersecting with connected ones).
LANE_NETWORKS = {
    "news":      ["instagram", "facebook", "linkedin", "twitter", "threads"],
    "quote":     ["instagram", "facebook", "threads", "twitter"],
    "fun":       ["instagram", "threads", "twitter"],
    "employer":  ["linkedin", "facebook"],
    "education": ["instagram", "linkedin", "facebook", "threads"],
}
# Recommended local posting time per lane (UK), used with --schedule.
LANE_TIME = {"quote": "08:00", "news": "09:30", "employer": "11:00",
             "education": "12:30", "fun": "17:30"}
DAY_INDEX = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4}


def active_networks():
    req = urllib.request.Request(USER_API, headers={"Authorization": f"Bearer {KEY}"})
    d = json.load(urllib.request.urlopen(req, timeout=20))
    return set(d.get("activeSocialAccounts", []))


def _trim(text, limit):
    if len(text) <= limit:
        return text, False
    cut = text[:limit - 1].rsplit(" ", 1)[0].rstrip(",.;:-")
    return cut + "…", True


def caption_for(post, net):
    caps = post.get("captions") or {}
    tags = post.get("hashtagsByPlatform") or {}
    ckey = NET_CAPTION[net]
    text = caps.get(ckey) or post.get("caption", "")
    hs = tags.get(ckey) or post.get("hashtags", [])
    if hs:
        text = text.rstrip() + "\n\n" + " ".join(hs)
    return _trim(text, NET_LIMIT.get(net, 5000))


def media_for(post, week_id):
    return [f"{R2_BASE}/{week_id}/{post['id']}/{s}" for s in post.get("slides", [])]


def schedule_iso(week, post):
    """Future UTC ISO for this post's lane time on its day (skips past times)."""
    wc = week.get("weekCommencing")
    if not wc:
        return None
    mon = datetime.date.fromisoformat(wc)
    dkey = post["id"].split("-")[-2] if post["id"].count("-") >= 2 else None
    di = DAY_INDEX.get(dkey, 0)
    hh, mm = (LANE_TIME.get(post.get("lane"), "09:00")).split(":")
    when = datetime.datetime.combine(mon + datetime.timedelta(days=di),
                                     datetime.time(int(hh), int(mm)))
    if when <= datetime.datetime.now():
        return None  # in the past - Ayrshare rejects; caller posts immediately
    return when.strftime("%Y-%m-%dT%H:%M:%SZ")


def build_jobs(week, connected, want_status, use_schedule):
    jobs = []
    for post in week.get("posts", []):
        if post.get("status") != want_status:
            continue
        lane = post.get("lane")
        nets = [n for n in LANE_NETWORKS.get(lane, []) if n in connected]
        media = media_for(post, week["id"])
        for net in nets:
            text, trimmed = caption_for(post, net)
            jobs.append({"pid": post["id"], "lane": lane, "network": net,
                         "text": text, "trimmed": trimmed, "mediaUrls": media,
                         "scheduleDate": schedule_iso(week, post) if use_schedule else None})
    return jobs


def post_job(job):
    body = {"post": job["text"], "platforms": [job["network"]],
            "mediaUrls": job["mediaUrls"]}
    if job.get("scheduleDate"):
        body["scheduleDate"] = job["scheduleDate"]
    data = json.dumps(body).encode()
    req = urllib.request.Request(API, data=data, method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return {"status": "error", "code": e.code, "body": e.read().decode()[:400]}


def load_posted():
    if os.path.exists(POSTED):
        try: return json.load(open(POSTED))
        except Exception: return {}
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True)
    ap.add_argument("--live", action="store_true", help="actually post (default: dry-run)")
    ap.add_argument("--schedule", action="store_true", help="schedule at lane times instead of now")
    ap.add_argument("--status", default="approved", help="which post status is eligible")
    args = ap.parse_args()

    if not KEY:
        sys.exit("No AYRSHARE_API_KEY in env (.env).")
    data = json.load(open(WEEKS))
    week = next((w for w in data["weeks"] if w["id"] == args.week), None)
    if not week:
        sys.exit(f"Week {args.week} not found.")

    connected = active_networks()
    posted = load_posted()
    jobs = build_jobs(week, connected, args.status, args.schedule)

    print(f"Week {args.week} | connected: {sorted(connected)} | status='{args.status}' "
          f"| {'LIVE' if args.live else 'DRY-RUN'}")
    print(f"{len(jobs)} post-jobs planned:\n")
    key_seen = set()
    todo = []
    for j in jobs:
        pkey = f"{j['pid']}:{j['network']}"
        already = pkey in posted
        flag = "ALREADY POSTED" if already else ("sched " + j["scheduleDate"] if j["scheduleDate"] else "now")
        print(f"  {j['pid']:22} -> {j['network']:10} [{len(j['text'])}c"
              f"{' TRIMMED' if j['trimmed'] else ''}] {len(j['mediaUrls'])} img | {flag}")
        if not already:
            todo.append((pkey, j))

    if not args.live:
        print(f"\nDRY-RUN: nothing sent. {len(todo)} would post. Add --live to send.")
        return
    print(f"\nLIVE: sending {len(todo)} ...")
    for pkey, j in todo:
        res = post_job(j)
        ok = res.get("status") == "success" or res.get("id")
        print(f"  {pkey}: {'OK ' + str(res.get('id','')) if ok else 'FAIL ' + json.dumps(res)[:200]}")
        if ok:
            posted[pkey] = {"id": res.get("id"), "at": datetime.datetime.utcnow().isoformat(),
                            "network": j["network"], "scheduleDate": j["scheduleDate"]}
            json.dump(posted, open(POSTED, "w"), indent=2)
    print("Done.")


if __name__ == "__main__":
    main()
