"""Blog re-share - schedules internwise.com/blog posts to socials.

Daily mode (--daily, how the scheduled workflow runs): once a day, share the
--limit newest unshared articles to LinkedIn, Facebook and Google Business
Profile, starting at 10:30 UK and staggered 30 minutes apart (the workflow
currently sends two, at 10:30 and 11:00). If that
slot has already passed when the run fires (GitHub delays scheduled workflows
by hours), the post rolls to tomorrow's 10:30 rather than going out now. The
article chosen is the newest one, published BEFORE today, not yet on every
target network. Skipping today's posts means the run never has to wait on an
article that may not be up yet when the cron fires (--include-today overrides).
The backlog drains steadily and a day with no new post still has something to
go out; ~86 articles are in the catalogue, so supply is not a constraint.

Weekly mode (no --daily, the original behaviour): surface the N most recent
posts and spread them across the upcoming week.

Recency comes from the site's sitemap.xml (<lastmod>), which is the only
reliable "newest first" signal - the /blog listing is a React SPA. Each post's
title + summary come from its page's <title> / og:description. These are LINK
posts (no image); the network unfurls the URL card.

Safe by default: DRY-RUN (prints the plan, calls nothing) unless --live is
given. Every live post is recorded in content/blog_shared.json (keyed by URL)
so a re-run never double-posts the same article.

    python3 tools/blog_share.py --daily --schedule  # dry-run the day's single post
    python3 tools/blog_share.py --daily --schedule --live   # what the cron runs
    python3 tools/blog_share.py                     # dry-run plan (upcoming week)
    python3 tools/blog_share.py --schedule          # dry-run + spread across week
    python3 tools/blog_share.py --live --schedule   # actually schedule them
    python3 tools/blog_share.py --limit 5 --live    # post now (no schedule)

Networks: intersected with the accounts actually connected in Ayrshare; any
requested network that is not connected is reported loudly and skipped.
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
BLOG_TIME_UK = "10:30"
BLOG_DAY_TIME = [("mon", BLOG_TIME_UK), ("tue", BLOG_TIME_UK), ("wed", BLOG_TIME_UK),
                 ("thu", BLOG_TIME_UK), ("fri", BLOG_TIME_UK)]


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
        # XML escapes '&' in <loc>, so a category like "startup-hiring-&-internships"
        # arrives as "...-&amp;-...". Posting that raw gives a 404 link.
        u = html.unescape(u)
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


def today_slot_iso(hhmm=BLOG_TIME_UK, idx=0, stagger_min=30, roll_forward=True):
    """The next blog slot in UTC: today's if it is still ahead, otherwise
    tomorrow's.

    GitHub runs scheduled workflows on a best-effort queue and routinely fires
    this job hours late, so "today at 10:30 UK" is frequently already behind us
    by the time we get here. This used to return None, and the caller then
    posted IMMEDIATELY - so every daily share went out at whatever random hour
    the runner happened to start, and the 10:30 slot was silently never used.
    Rolling to tomorrow keeps the posting time honest; the article is a
    re-share from a backlog, so a few hours later costs nothing.

    `idx` staggers extra articles by `stagger_min` minutes, so a run sending
    several does not stack them all on the same minute. Pass roll_forward=False to get the old behaviour (None
    when the slot has passed, meaning post now).
    """
    hh, mm = hhmm.split(":")
    stagger = datetime.timedelta(minutes=idx * stagger_min)
    now = datetime.datetime.now(datetime.timezone.utc)
    for day_offset in (0, 1):
        when_uk = datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=day_offset),
            datetime.time(int(hh), int(mm)), tzinfo=ZoneInfo("Europe/London")) + stagger
        if when_uk > now:
            if day_offset:
                print(f"  (today's {hhmm} UK slot has passed; rolling to tomorrow "
                      "rather than posting now)")
            return when_uk.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if not roll_forward:
            return None
    return None


def pick_daily(nets, shared, count=1, pool=200, day_prior=True):
    """The `count` newest articles still missing at least one target network.

    Daily mode selects from the whole catalogue rather than just the newest few,
    so a day whose latest post is already out still has something to share and
    the backlog drains steadily. Returns [(url, lastmod), ...], newest first.

    day_prior: ignore anything published TODAY, so the run never depends on a
    post that may not be up yet when the cron fires (same day-prior principle as
    the news lane). The newest eligible article is therefore yesterday's, or
    older if nothing was published yesterday - blog cadence is irregular, so
    requiring an article dated exactly yesterday would leave most days silent.
    """
    cutoff = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    out = []
    for url, lastmod in recent_posts(pool):
        if day_prior and lastmod[:10] > cutoff:
            continue                       # published today - leave it for tomorrow
        done = set(shared.get(url, {}).get("networks", []))
        if set(nets) - done:
            out.append((url, lastmod))
            if len(out) >= count:
                break
    return out


def upcoming_monday():
    today = datetime.date.today()
    return today + datetime.timedelta(days=(7 - today.weekday()) % 7 or 7)


def schedule_iso(idx, use_schedule, week_monday=None):
    if not use_schedule:
        return None
    mon = week_monday or upcoming_monday()
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
    ap.add_argument("--week-monday", default=None, help="ISO date of the Monday to schedule against (default: upcoming Monday). Past slots post immediately.")
    ap.add_argument("--daily", action="store_true",
                    help="daily mode: share the newest article not yet on every target "
                         "network, at today's 10:30 UK slot (default --limit 1)")
    ap.add_argument("--include-today", action="store_true",
                    help="daily mode: also consider articles published today "
                         "(default: day-prior only, never waits on a same-day post)")
    args = ap.parse_args()
    if args.daily and "--limit" not in sys.argv:
        args.limit = 1          # one blog per day unless explicitly overridden
    if not KEY:
        sys.exit("No AYRSHARE_API_KEY in env (.env).")
    only_nets = set(n.strip() for n in args.network.split(",")) if args.network else None
    week_monday = datetime.date.fromisoformat(args.week_monday) if args.week_monday else None

    connected = active_networks()
    wanted = [n for n in BLOG_NETWORKS if not only_nets or n in only_nets]
    nets = [n for n in wanted if n in connected]
    shared = load_shared()

    print(f"Blog re-share | connected: {sorted(connected)} | targeting: {nets} "
          f"| {'LIVE' if args.live else 'DRY-RUN'}")
    missing = [n for n in wanted if n not in connected]
    if missing:
        # Loud, not silent: a network the operator asked for but Ayrshare does
        # not report as connected will simply never receive posts.
        print(f"  !! requested but NOT connected in Ayrshare, so skipped: {missing}")
        print("     Reconnect the account in Ayrshare for these to go out.")
    if not nets:
        sys.exit("No target network is connected in Ayrshare - nothing to do.")

    if args.daily:
        posts = pick_daily(nets, shared, count=args.limit,
                           day_prior=not args.include_today)
        window = "up to today" if args.include_today else "published before today"
        print(f"Daily mode ({window}): {len(posts)} article(s) not yet on {nets}:\n")
    else:
        posts = recent_posts(args.limit)
        print(f"{len(posts)} recent posts from sitemap:\n")

    todo = []
    for idx, (url, lastmod) in enumerate(posts):
        meta = article_meta(url)
        if args.daily:
            sched = today_slot_iso(idx=idx) if args.schedule else None
        else:
            sched = schedule_iso(idx, args.schedule, week_monday=week_monday)
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
            rec = shared.setdefault(url, {"networks": [], "at": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat()})
            rec["networks"] = sorted(set(rec["networks"]) | {net})
            json.dump(shared, open(SHARED, "w"), indent=2)
    print("Done.")


if __name__ == "__main__":
    main()
