"""
build_analytics.py — turn Ayrshare analytics into the dashboard's data/analytics.json.

Two jobs, matching what the Analytics tab shows:
  PRESENT (review performance): per-platform account metrics (followers, reach,
    views, engagement) from Ayrshare /analytics/social.
  DECISION-MAKING (what to do next): from Ayrshare /history (recent posts, each
    carrying our R2 mediaUrl so we can recover the lane/topic + the time posted)
    joined with per-post /analytics/post engagement, we aggregate:
      - byLane  : which topics/pillars earn the most engagement
      - byDay   : which day of week performs best
      - byHour  : which time of day performs best
      - topPosts: the individual posts that worked
      - insights: plain-English takeaways derived from the above

Reads AYRSHARE_API_KEY from env (or social-media/.env). Writes two files:
  - data/analytics.json                       (PUBLIC: per-platform performance;
    the Meta-style dashboard reads this - same pattern as weeks.json / featured.json)
  - social-media/content/analytics_insights.json  (BACKEND: best time/topics,
    insights, top posts - feeds content planning, never served to the public site)

    python3 social-media/tools/build_analytics.py            # write data/analytics.json
    python3 social-media/tools/build_analytics.py --records 80
"""
from __future__ import annotations
import os, sys, json, re, argparse, datetime
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
HUB  = os.path.dirname(SM)
# Public: the Meta-style performance dashboard reads this (served to the browser).
OUT  = os.path.join(HUB, "data", "analytics.json")
# Backend: decision-making aggregates (best time/topics, insights, top posts).
# Kept out of the public site - it feeds our content planning, not the dashboard.
INSIGHTS_OUT = os.path.join(SM, "content", "analytics_insights.json")
BASE = "https://api.ayrshare.com/api"
DOW  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# Lane label + display order for the topic breakdown.
LANE_LABELS = {"education": "Education", "news": "News", "quote": "Quote",
               "fun": "Fun", "employer": "Employer", "featured": "Featured jobs",
               "shorts": "Shorts"}


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


def _api(path, body=None, method="GET"):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{BASE}/{path}", data=data, method=method,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        return {"_http": e.code, "_body": e.read().decode()[:300]}
    except Exception as e:
        return {"_error": str(e)}


# Platforms we actually publish to and want reviewed.
PLATFORMS = ["instagram", "facebook", "linkedin", "threads"]


def social_summary():
    """Per-platform account metrics for the Present/performance view."""
    res = _api("analytics/social", {"platforms": PLATFORMS}, "POST")
    out = {}
    for net in PLATFORMS:
        a = ((res.get(net) or {}).get("analytics")) or {}
        if not a:
            continue
        # Followers can be a flat count or a nested object (LinkedIn:
        # {totalFollowerCount, organicFollowerCount, ...}).
        foll = a.get("followersCount") or a.get("followers") or a.get("followerCount")
        if isinstance(foll, dict):
            foll = (foll.get("totalFollowerCount") or foll.get("organicFollowerCount")
                    or next((v for v in foll.values() if isinstance(v, (int, float))), None))
        out[net] = {
            "followers":   foll,
            "reach":       a.get("reachCount") or a.get("reach"),
            "views":       a.get("viewsCount") or a.get("impressionsCount") or a.get("impressions"),
            "likes":       a.get("likeCount") or a.get("likesCount"),
            "comments":    a.get("commentsCount"),
            "shares":      a.get("shareCount") or a.get("sharesCount"),
            "posts":       a.get("mediaCount") or a.get("postsCount"),
            "name":        a.get("name") or a.get("username"),
        }
    return out


def _lane_from_media(urls):
    """Recover our lane/topic from the R2 path in a post's mediaUrls.
    .../week14/week14-fri-fun/slide_1.png -> 'fun'; .../featured/job-1/... -> 'featured'."""
    for u in urls or []:
        m = re.search(r"/(week\d+)/\1-(?:mon|tue|wed|thu|fri|sat|sun)-([a-z]+)/", u)
        if m:
            return m.group(2)
        if "/featured/" in u:
            return "featured"
        if "/shorts" in u or "/video" in u:
            return "shorts"
    return None


def _engagement(pa):
    """Normalise an engagement number from one platform's post-analytics block,
    across the differing field names Ayrshare returns per network."""
    if not isinstance(pa, dict):
        return 0
    if isinstance(pa.get("engagementCount"), (int, float)):
        return pa["engagementCount"]
    total = 0
    for k in ("likeCount", "likesCount", "commentsCount", "shareCount",
              "sharesCount", "reactionsCount", "savedCount", "repostCount",
              "quoteCount", "replyCount"):
        v = pa.get(k)
        if isinstance(v, (int, float)):
            total += v
    return total


def decision_making(records):
    """Join history (lane + time) with per-post engagement into aggregates."""
    hist = _api(f"history?lastRecords={records}")
    items = hist.get("history") if isinstance(hist, dict) else (hist if isinstance(hist, list) else [])
    by_lane, by_day, by_hour, top = {}, {}, {}, []

    for it in items or []:
        if it.get("status") not in (None, "success"):
            continue
        aid = it.get("id")
        lane = _lane_from_media(it.get("mediaUrls"))
        created = it.get("created")
        nets = it.get("platforms") or []
        net = nets[0] if nets else None
        if not aid or not created:
            continue
        try:
            dt = datetime.datetime.fromisoformat(created.replace("Z", "+00:00"))
        except Exception:
            continue

        pa = _api("analytics/post", {"id": aid}, "POST")
        eng = _engagement((pa.get(net) or {}).get("analytics")) if net else 0

        # aggregates
        if lane:
            L = by_lane.setdefault(lane, {"posts": 0, "engagement": 0})
            L["posts"] += 1; L["engagement"] += eng
        d = DOW[dt.weekday()]
        D = by_day.setdefault(d, {"posts": 0, "engagement": 0})
        D["posts"] += 1; D["engagement"] += eng
        hh = dt.hour
        H = by_hour.setdefault(hh, {"posts": 0, "engagement": 0})
        H["posts"] += 1; H["engagement"] += eng

        top.append({"lane": lane, "network": net, "engagement": eng,
                    "created": created,
                    "caption": (it.get("post") or "")[:120]})

    def avg(d):
        return {k: {"posts": v["posts"], "engagement": v["engagement"],
                    "avg": round(v["engagement"] / v["posts"], 1) if v["posts"] else 0}
                for k, v in d.items()}

    by_lane, by_day, by_hour = avg(by_lane), avg(by_day), avg(by_hour)
    top.sort(key=lambda p: p["engagement"], reverse=True)
    return by_lane, by_day, by_hour, top[:8]


def make_insights(by_lane, by_day, by_hour):
    """Plain-English takeaways the team can act on."""
    out = []
    def best(d, label):
        cand = {k: v for k, v in d.items() if v["posts"] >= 1}
        if not cand:
            return None
        return max(cand.items(), key=lambda kv: kv[1]["avg"])
    bl = best(by_lane, "lane")
    if bl:
        out.append(f"Your strongest topic is {LANE_LABELS.get(bl[0], bl[0].title())} "
                   f"({bl[1]['avg']} avg engagement/post). Make more of it.")
    bd = best(by_day, "day")
    if bd:
        out.append(f"{bd[0]} is your best posting day ({bd[1]['avg']} avg engagement/post).")
    bh = best(by_hour, "hour")
    if bh:
        out.append(f"Posts around {int(bh[0]):02d}:00 UTC perform best "
                   f"({bh[1]['avg']} avg engagement/post).")
    weak = {k: v for k, v in by_lane.items() if v["posts"] >= 2}
    if weak:
        w = min(weak.items(), key=lambda kv: kv[1]["avg"])
        out.append(f"{LANE_LABELS.get(w[0], w[0].title())} is underperforming "
                   f"({w[1]['avg']} avg) - rework the angle or post it at a stronger time.")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", type=int, default=60, help="how many recent posts to analyse")
    args = ap.parse_args()
    if not KEY:
        sys.exit("No AYRSHARE_API_KEY in env (.env).")

    print(f"Fetching Ayrshare analytics (last {args.records} posts) ...")
    social = social_summary()
    by_lane, by_day, by_hour, top = decision_making(args.records)
    insights = make_insights(by_lane, by_day, by_hour)

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # PUBLIC — Meta-style performance dashboard (per-platform account metrics only).
    public = {
        "generatedAt": now,
        "windowRecords": args.records,
        "platforms": social,
    }
    with open(OUT, "w") as f:
        json.dump(public, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT} (platforms: {list(social)})")

    # BACKEND — decision-making aggregates, not served to the public site.
    backend = {
        "generatedAt": now,
        "windowRecords": args.records,
        "byLane": by_lane,
        "byDay": by_day,
        "byHour": by_hour,
        "topPosts": top,
        "insights": insights,
        "laneLabels": LANE_LABELS,
    }
    os.makedirs(os.path.dirname(INSIGHTS_OUT), exist_ok=True)
    with open(INSIGHTS_OUT, "w") as f:
        json.dump(backend, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {INSIGHTS_OUT} (lanes: {list(by_lane)} | topPosts: {len(top)})")
    for i in insights:
        print("  -", i)


if __name__ == "__main__":
    main()
