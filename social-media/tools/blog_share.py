"""Blog re-share - schedules the latest internwise.com/blog posts to socials.

Part of the Saturday content ritual: every week we surface the 5 most recent
blog posts and schedule them out to LinkedIn, Facebook, Threads (and Google
Business Profile once it's connected in Ayrshare) across the upcoming week.

Recency comes from the site's sitemap.xml (<lastmod>), which is the only
reliable "newest first" signal - the /blog listing is a React SPA. Each post's
title + summary come from its page's <title> / og:description. These are LINK
posts (no image); the network unfurls the URL card.

Safe by default: DRY-RUN (prints the plan, calls nothing) unless --live is
given. Every live post is recorded in content/blog_shared.json (keyed by URL)
so a re-run never double-posts the same article.

    python3 tools/blog_share.py                     # dry-run plan (upcoming week)
    python3 tools/blog_share.py --schedule          # dry-run + spread across week
    python3 tools/blog_share.py --live --schedule   # actually schedule them
    python3 tools/blog_share.py --limit 5 --live    # post now (no schedule)

Networks: linkedin, facebook, threads by default (intersected with the accounts
actually connected in Ayrshare). Add gmb once Google Business Profile is linked.
"""
from __future__ import annotations
import os, sys, re, json, html, argparse, datetime
import urllib.request, urllib.error
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
HUB  = os.path.dirname(SM)
WEEKS = os.path.join(HUB, "data", "weeks.json")
SHARED = os.path.join(SM, "content", "blog_shared.json")
SITEMAP = "https://www.internwise.com/sitemap.xml"
API = "https://api.ayrshare.com/api/post"
USER_API = "https://api.ayrshare.com/api/user"
UA = "Mozilla/5.0 (compatible; internwise-content-bot/1.0)"

# Networks we WANT blog re-shares on (intersected with connected accounts).
# "gmb" (Google Business Profile) is included but only fires once it's linked
# in Ayrshare - until then active_networks() won't contain it and it's skipped.
BLOG_NETWORKS = ["linkedin", "facebook", "threads", "gmb"]
NET_LIMIT = {"threads": 500, "facebook": 63000, "linkedin": 3000, "gmb": 1500}
# One blog per weekday at 10:30 UK - a late-morning slot clear of the lane posts
# (news 08:00, education 13:30, quote 20:00, employer 20:30).
BLOG_DAY_TIME = [("mon", "10:30"), ("tue", "10:30"), ("wed", "10:30"),
                 ("thu", "10:30"), ("fri", "10:30")]


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


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def recent_posts(limit=5):
    """Return the `limit` most recent blog ARTICLE URLs (with lastmod), newest
    first, from the sitemap. Articles have >=2 path segments after /blog/;
    single-segment /blog/<category> pages are section indexes, not posts."""
    xml = _get(SITEMAP)
    pairs = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", xml)
    arts = []
    for u, d in pairs:
        if "/blog/" not in u:
            continue
        tail = u.split("/blog/", 1)[1].strip("/")
        if tail and tail.count("/") >= 1:      # category/article
            arts.append((u, d))
    arts.sort(key=lambda x: x[1], reverse=True)
    return arts[:limit]


def _meta(patterns, page):
    for pat in patterns:
        m = re.search(pat, page, re.I | re.S)
        if m:
            return html.unescape(m.group(1)).strip()
    return ""


def article_meta(url):
    """Pull a title + summary for the post from its page metadata."""
    try:
        page = _get(url)
    except Exception as e:
        return {"title": "", "summary": "", "error": str(e)}
    title = _meta([r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']',
                   r'<title[^>]*>(.*?)</title>'], page)
    summary = _meta([r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
                     r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']'], page)
    # Strip a trailing " | Internwise"-style site suffix from the title.
    title = re.sub(r"\s*[|\-–]\s*Internwise.*$", "", title, flags=re.I).strip()
    return {"title": title, "summary": summary}


def caption_for(meta, url, net):
    title = meta.get("title") or "New on the Internwise blog"
    summary = meta.get("summary") or ""
    if net == "threads":
        body = title if not summary else f"{title}\n\n{summary}"
        text = f"{body}\n\n{url}"
    elif net == "linkedin":
        text = (f"{title}\n\n{summary}\n\nRead the full post: {url}"
                "\n\n#internships #careers #startups")
    else:  # facebook, gmb
        text = f"{title}\n\n{summary}\n\nRead more: {url}"
    limit = NET_LIMIT.get(net, 2000)
    if len(text) > limit:
        text = text[:limit - 1].rsplit(" ", 1)[0] + "…"
    return text


def active_networks():
    req = urllib.request.Request(USER_API, headers={"Authorization": f"Bearer {KEY}"})
    d = json.load(urllib.request.urlopen(req, timeout=20))
    return set(d.get("activeSocialAccounts", []))


def upcoming_monday():
    today = datetime.date.today()
    return today + datetime.timedelta(days=(7 - today.weekday()) % 7 or 7)


def schedule_iso(idx, use_schedule):
    if not use_schedule:
        return None
    mon = upcoming_monday()
    day_idx = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4}
    dkey, hhmm = BLOG_DAY_TIME[idx % len(BLOG_DAY_TIME)]
    hh, mm = hhmm.split(":")
    when_uk = datetime.datetime.combine(
        mon + datetime.timedelta(days=day_idx[dkey]),
        datetime.time(int(hh), int(mm)), tzinfo=ZoneInfo("Europe/London"))
    if when_uk <= datetime.datetime.now(datetime.timezone.utc):
        return None
    return when_uk.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def post_job(text, net, sched):
    body = {"post": text, "platforms": [net]}
    if sched:
        body["scheduleDate"] = sched
    data = json.dumps(body).encode()
    req = urllib.request.Request(API, data=data, method="POST",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return {"status": "error", "code": e.code, "body": e.read().decode()[:400]}


def load_shared():
    if os.path.exists(SHARED):
        try: return json.load(open(SHARED))
        except Exception: return {}
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=5, help="how many recent posts to share")
    ap.add_argument("--live", action="store_true", help="actually post (default: dry-run)")
    ap.add_argument("--schedule", action="store_true", help="spread across the upcoming week instead of now")
    ap.add_argument("--network", default=None, help="comma list to limit networks (e.g. linkedin,facebook)")
    args = ap.parse_args()
    if not KEY:
        sys.exit("No AYRSHARE_API_KEY in env (.env).")
    only_nets = set(n.strip() for n in args.network.split(",")) if args.network else None

    connected = active_networks()
    nets = [n for n in BLOG_NETWORKS if n in connected and (not only_nets or n in only_nets)]
    shared = load_shared()
    posts = recent_posts(args.limit)

    print(f"Blog re-share | connected: {sorted(connected)} | targeting: {nets} "
          f"| {'LIVE' if args.live else 'DRY-RUN'}")
    print(f"{len(posts)} recent posts from sitemap:\n")

    todo = []
    for idx, (url, lastmod) in enumerate(posts):
        meta = article_meta(url)
        sched = schedule_iso(idx, args.schedule)
        done_nets = set(shared.get(url, {}).get("networks", []))
        flag = "sched " + sched if sched else "now"
        print(f"  {lastmod}  {meta.get('title','(no title)')[:60]}")
        print(f"           {url}")
        for net in nets:
            if net in done_nets:
                print(f"           -> {net:9} ALREADY SHARED")
                continue
            text = caption_for(meta, url, net)
            print(f"           -> {net:9} [{len(text)}c] {flag}")
            todo.append((url, net, text, sched))

    if not args.live:
        print(f"\nDRY-RUN: nothing sent. {len(todo)} would post. Add --live to send.")
        return
    print(f"\nLIVE: sending {len(todo)} ...")
    for url, net, text, sched in todo:
        res = post_job(text, net, sched)
        ok = res.get("status") == "success" or res.get("id")
        print(f"  {net:9} {url.split('/')[-1]}: "
              f"{'OK ' + str(res.get('id','')) if ok else 'FAIL ' + json.dumps(res)[:200]}")
        if ok:
            rec = shared.setdefault(url, {"networks": [], "at": datetime.datetime.utcnow().isoformat()})
            rec["networks"] = sorted(set(rec["networks"]) | {net})
            json.dump(shared, open(SHARED, "w"), indent=2)
    print("Done.")


if __name__ == "__main__":
    main()
