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
    python3 tools/ayrshare_publish.py --featured                 # dry-run approved featured jobs
    python3 tools/ayrshare_publish.py --featured --live          # post approved featured jobs

Notes:
- Networks connected in Ayrshare: instagram, facebook, linkedin, threads,
  gmb (Google Business Profile), pinterest, youtube. The lane routing below only
  targets ig/fb/li/threads today; gmb/pinterest/youtube are connected but no lane
  sends to them yet. X/Twitter and TikTok are NOT connected, so lanes that would
  target them simply skip those networks until they're linked in Ayrshare.
  Connected accounts are resolved dynamically via active_networks().
- Threads has a 500-char limit; long captions are trimmed for Threads only
  (and flagged). All other networks receive the full caption.
"""
from __future__ import annotations
import os, sys, json, argparse, datetime
import urllib.request, urllib.error
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
HUB  = os.path.dirname(SM)
WEEKS = os.path.join(HUB, "data", "weeks.json")
FEATURED = os.path.join(HUB, "data", "featured.json")
POSTED = os.path.join(SM, "content", "ayrshare_posted.json")
R2_BASE = "https://pub-5f843c240ef6453bba67e131500424af.r2.dev"
API = "https://api.ayrshare.com/api/post"
USER_API = "https://api.ayrshare.com/api/user"
# Live dashboard KV endpoint: { "<postId>": "approved" | "in-review" | ... }.
# For featured jobs the dashboard approval (not the file status) is the gate.
STATUSES_URL = "https://iw-content-hub.pages.dev/api/statuses"


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
# gmb (Google Business Profile) is customer-facing local content; it reuses the
# ig-fb caption.
NET_CAPTION = {"instagram": "ig-fb", "facebook": "ig-fb", "threads": "ig-fb",
               "linkedin": "linkedin", "twitter": "x", "gmb": "ig-fb",
               "pinterest": "ig-fb"}
# Rough per-network caption character ceilings (trim only where needed).
NET_LIMIT = {"twitter": 280, "threads": 500, "instagram": 2200,
             "facebook": 63000, "linkedin": 3000, "gmb": 1500,
             "pinterest": 500}
# GMB only accepts a SINGLE image per post (no carousels); these lanes send just
# their cover slide to GMB (see build_jobs).
SINGLE_IMAGE_NETS = {"gmb", "pinterest"}
# Lane -> the networks we WANT it on (before intersecting with connected ones).
# gmb added to the substantive, business-relevant lanes only (news/employer/
# education); quote/fun/engagement/featured stay off GMB.
LANE_NETWORKS = {
    "news":      ["instagram", "facebook", "linkedin", "twitter", "threads", "gmb", "pinterest"],
    "quote":     ["instagram", "facebook", "threads", "twitter", "pinterest"],
    "fun":       ["instagram", "facebook", "threads", "twitter", "pinterest"],
    "engagement":["instagram", "facebook", "threads", "twitter", "linkedin", "pinterest"],
    "employer":  ["linkedin", "facebook", "gmb"],
    "education": ["instagram", "linkedin", "facebook", "threads", "gmb", "pinterest"],
    # Featured job ads: candidate-facing + employer-credible.
    "featured":  ["instagram", "facebook", "linkedin", "threads", "pinterest"],
}
# Instagram location tagging (IG feed only). Ayrshare tags a location by a
# Facebook Page ID (or "@pagename") for a place with a physical location - a whole
# country ("United Kingdom") has no such Page, so we tag the "London, United
# Kingdom" place as the UK-wide proxy (Facebook place id 106078429431815). Applied
# to the lanes in LOCATION_LANES, and ONLY to single-image posts: Instagram rejects
# a location on carousels, so multi-slide education posts are left untagged
# automatically. Override the Page id with IG_LOCATION_ID in .env if it changes.
# NB: Ayrshare has no dry-run for the location value - it only validates the id at
# post time, and errors if the Page has no physical location listed. The first
# tagged live post is the real confirmation this id resolves.
IG_LOCATION_ID = os.getenv("IG_LOCATION_ID", "106078429431815").strip()
LOCATION_LANES = {"news", "education"}

# Recommended local posting time per lane (UK), used with --schedule.
# Times set from the founder's reach observation (Sept 2026): the quote takes the
# 8pm reach slot, news opens the day, education runs early afternoon, employer
# closes the evening.
LANE_TIME = {"news": "08:00", "education": "13:30", "engagement": "16:30",
             "quote": "20:00", "employer": "20:30", "featured": "17:30"}
DAY_INDEX = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}


def fetch_statuses():
    """Read shared post statuses from the live dashboard KV endpoint. On any
    failure, return {} (nothing treated as approved) so we never over-post."""
    try:
        # Cloudflare blocks the default python-urllib agent (403); send a real UA.
        req = urllib.request.Request(STATUSES_URL, headers={
            "cache-control": "no-store",
            "User-Agent": "Mozilla/5.0 (compatible; internwise-content-bot/1.0)",
        })
        return json.load(urllib.request.urlopen(req, timeout=20)) or {}
    except Exception as e:
        print(f"  (statuses fetch failed: {e}); treating none as approved")
        return {}


def load_featured_week():
    """featured.json is shaped like a week (id + posts). Featured posts carry no
    lane and their file status stays 'in-review'; the real gate is the dashboard
    KV approval, so we stamp lane='featured' and overlay each post's live status."""
    fw = json.load(open(FEATURED))
    statuses = fetch_statuses()
    for p in fw.get("posts", []):
        p["lane"] = "featured"
        p["status"] = statuses.get(p["id"], p.get("status"))
    return fw


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
    # Threads uses a purpose-written short caption when present (500-char limit);
    # otherwise it falls back to the ig-fb caption (trimmed only if needed).
    if net == "threads" and caps.get("threads"):
        # Dedicated Threads caption is written complete + length-budgeted; use as-is.
        return _trim(caps["threads"], NET_LIMIT.get(net, 5000))
    ckey = NET_CAPTION[net]
    text = caps.get(ckey) or post.get("caption", "")
    hs = tags.get(ckey) or post.get("hashtags", [])
    # Brand rule: hashtags always lowercase (#techjobs, never #TechJobs).
    hs = ["#" + t[1:].lower() if isinstance(t, str) and t.startswith("#") else t for t in hs]
    if hs:
        text = text.rstrip() + "\n\n" + " ".join(hs)
    return _trim(text, NET_LIMIT.get(net, 5000))


def media_for(post, week_id):
    return [f"{R2_BASE}/{week_id}/{post['id']}/{s}" for s in post.get("slides", [])]


def schedule_iso(week, post, at=None):
    """Future UTC ISO for this post's lane time (UK local) on its day.

    LANE_TIME is UK wall-clock; we localise to Europe/London (handles BST/GMT
    automatically) then convert to UTC for Ayrshare. Past times return None so
    the caller posts immediately instead of getting rejected. `at` (\"HH:MM\")
    overrides the lane time for a one-off custom slot."""
    wc = week.get("weekCommencing")
    if not wc:
        return None
    mon = datetime.date.fromisoformat(wc)
    dkey = post["id"].split("-")[-2] if post["id"].count("-") >= 2 else None
    di = DAY_INDEX.get(dkey, 0)
    hh, mm = (at or LANE_TIME.get(post.get("lane"), "09:00")).split(":")
    when_uk = datetime.datetime.combine(
        mon + datetime.timedelta(days=di), datetime.time(int(hh), int(mm)),
        tzinfo=ZoneInfo("Europe/London"))
    if when_uk <= datetime.datetime.now(datetime.timezone.utc):
        return None  # in the past - Ayrshare rejects; caller posts immediately
    return when_uk.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _dkey(post):
    return post["id"].split("-")[-2] if post["id"].count("-") >= 2 else None


def build_jobs(week, connected, want_status, use_schedule, only=None, days=None, stories=True, at=None, networks=None):
    jobs = []
    for post in week.get("posts", []):
        if only:
            if post["id"] != only:
                continue           # --only names one post; post it regardless of status
        elif post.get("status") != want_status:
            continue
        if days and _dkey(post) not in days:
            continue
        lane = post.get("lane")
        nets = [n for n in LANE_NETWORKS.get(lane, []) if n in connected]
        if networks:               # --network limits the send to specific platform(s)
            nets = [n for n in nets if n in networks]
        media = media_for(post, week["id"])
        sched = schedule_iso(week, post, at=at) if use_schedule else None
        for net in nets:
            text, trimmed = caption_for(post, net)
            # GMB accepts only one image; send the cover slide alone.
            net_media = media[:1] if net in SINGLE_IMAGE_NETS else media
            extra = {}
            # Instagram location tag: feed only, chosen lanes, single image only
            # (IG rejects a location on carousels, so >1 slide is left untagged).
            geo = (net == "instagram" and lane in LOCATION_LANES
                   and IG_LOCATION_ID and len(net_media) == 1)
            if geo:
                extra["instagramOptions"] = {"locationId": IG_LOCATION_ID}
            jobs.append({"pid": post["id"], "lane": lane, "network": net, "kind": "feed",
                         "text": text, "trimmed": trimmed, "mediaUrls": net_media,
                         "extra": extra, "geo": bool(geo), "scheduleDate": sched})
        # Story companions are automatic for reach: every Instagram feed post
        # gets a matching Story when story.png exists. Facebook Stories mirror
        # this once a Facebook Page is connected in Ayrshare.
        if stories and media:
            local_story = os.path.join(HUB, "images", week["id"], post["id"], "story.png")
            if not os.path.exists(local_story):
                continue
            story_url = f"{R2_BASE}/{week['id']}/{post['id']}/story.png"
            if "instagram" in nets:
                jobs.append({"pid": post["id"], "lane": lane, "network": "instagram", "kind": "story",
                             "text": post.get("title", " ")[:60], "trimmed": False,
                             "mediaUrls": [story_url], "extra": {"instagramOptions": {"stories": True}},
                             "scheduleDate": sched})
            # Facebook Story companion, mirroring Instagram (requires a connected
            # Facebook Page; Ayrshare posts a single-image Story via faceBookOptions).
            if "facebook" in nets:
                jobs.append({"pid": post["id"], "lane": lane, "network": "facebook", "kind": "story",
                             "text": post.get("title", " ")[:60], "trimmed": False,
                             "mediaUrls": [story_url], "extra": {"faceBookOptions": {"stories": True}},
                             "scheduleDate": sched})
    return jobs


def post_job(job):
    body = {"post": job["text"], "platforms": [job["network"]],
            "mediaUrls": job["mediaUrls"]}
    body.update(job.get("extra") or {})
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
    ap.add_argument("--week", help="week id in weeks.json (e.g. week14)")
    ap.add_argument("--featured", action="store_true",
                    help="publish approved FEATURED jobs (data/featured.json, KV-gated) instead of a week")
    ap.add_argument("--live", action="store_true", help="actually post (default: dry-run)")
    ap.add_argument("--schedule", action="store_true", help="schedule at lane times instead of now")
    ap.add_argument("--status", default="approved", help="which post status is eligible")
    ap.add_argument("--only", default=None, help="post just this one post id (ignores status gate)")
    ap.add_argument("--days", default=None, help="comma list of day keys to include, e.g. tue,wed,thu,fri")
    ap.add_argument("--stories", action="store_true",
                    help="legacy/no-op: Instagram Stories are posted automatically with Instagram feed posts")
    ap.add_argument("--at", default=None, help="one-off UK HH:MM time override for scheduling")
    ap.add_argument("--network", default=None, help="comma list of networks to send to (e.g. facebook); default: all connected for the lane")
    args = ap.parse_args()
    days = set(d.strip() for d in args.days.split(",")) if args.days else None
    networks = set(n.strip() for n in args.network.split(",")) if args.network else None

    if not KEY:
        sys.exit("No AYRSHARE_API_KEY in env (.env).")
    if bool(args.week) == bool(args.featured):
        sys.exit("Pass exactly one of --week <id> or --featured.")
    if args.featured:
        week = load_featured_week()
        label = "featured"
    else:
        data = json.load(open(WEEKS))
        week = next((w for w in data["weeks"] if w["id"] == args.week), None)
        if not week:
            sys.exit(f"Week {args.week} not found.")
        label = args.week

    connected = active_networks()
    posted = load_posted()
    jobs = build_jobs(week, connected, args.status, args.schedule, only=args.only,
                      days=days, stories=True, at=args.at, networks=networks)

    print(f"Target {label} | connected: {sorted(connected)} | status='{args.status}' "
          f"| {'LIVE' if args.live else 'DRY-RUN'}")
    print(f"{len(jobs)} post-jobs planned:\n")
    key_seen = set()
    todo = []
    for j in jobs:
        kind = j.get("kind", "feed")
        pkey = f"{j['pid']}:{j['network']}" + (":story" if kind == "story" else "")
        already = pkey in posted
        flag = "ALREADY POSTED" if already else ("sched " + j["scheduleDate"] if j["scheduleDate"] else "now")
        print(f"  {j['pid']:22} -> {j['network']:10} {kind:5} [{len(j['text'])}c"
              f"{' TRIMMED' if j['trimmed'] else ''}] {len(j['mediaUrls'])} img"
              f"{' +geo' if j.get('geo') else ''} | {flag}")
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
