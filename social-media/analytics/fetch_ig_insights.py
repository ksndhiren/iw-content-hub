"""
fetch_ig_insights.py

Pulls per-post Instagram insights for the Internwise IG Business account via the
Meta Graph API and writes them to a CSV for analysis.

SECURITY: the access token is read from a LOCAL FILE (default analytics/ig_token.txt)
and is NEVER printed. Keep that file private - do not paste the token into chat or
commit it anywhere.

Setup (one time):
  1. Get a token with permissions: instagram_basic, instagram_manage_insights,
     pages_read_engagement, pages_show_list  (see analytics/README.md).
  2. Save it to analytics/ig_token.txt  (just the token string, nothing else).
  3. Run:  python3 analytics/fetch_ig_insights.py

Output: analytics/ig_insights.csv  (one row per post, newest first).
"""
import os, sys, csv, json, time, urllib.parse, urllib.request

API = "https://graph.facebook.com/v21.0"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.environ.get("IG_TOKEN_FILE", os.path.join(HERE, "ig_token.txt"))
OUT_CSV    = os.path.join(HERE, "ig_insights.csv")

# Per-post metrics to try. Availability varies by API version + media type, so we
# request them and keep whatever the API returns (unsupported ones are skipped).
POST_METRICS = ["reach", "impressions", "views", "saved", "shares",
                "total_interactions", "likes", "comments", "profile_visits"]


def _token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(f"ERROR: token file not found: {TOKEN_FILE}\n"
                 f"Create it with your Graph API token (see analytics/README.md).")
    with open(TOKEN_FILE) as f:
        t = f.read().strip()
    if not t:
        sys.exit(f"ERROR: token file is empty: {TOKEN_FILE}")
    return t


def _get(path, params):
    url = f"{API}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "internwise-analytics/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def _get_full_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "internwise-analytics/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def find_ig_account(token):
    """Find the IG Business account id via the linked Facebook Page. Returns
    (ig_id, ig_username, page_access_token)."""
    pages = _get("me/accounts", {"fields": "name,id,access_token", "access_token": token})
    data = pages.get("data", [])
    if not data:
        sys.exit("ERROR: no Facebook Pages found for this token. Make sure the token "
                 "has pages_show_list and the IG Business account is linked to a Page.")
    for pg in data:
        pg_token = pg.get("access_token", token)
        info = _get(pg["id"], {"fields": "instagram_business_account{id,username}",
                               "access_token": pg_token})
        iba = info.get("instagram_business_account")
        if iba:
            print(f"  Page: {pg.get('name')} -> IG @{iba.get('username')} ({iba['id']})")
            return iba["id"], iba.get("username", ""), pg_token
    sys.exit("ERROR: none of your Pages have a linked Instagram Business account. "
             "Link the IG (the 'Facebook + Instagram' asset) to the Page and retry.")


def fetch_media(ig_id, token):
    """All media (paginated), newest first."""
    media = []
    resp = _get(f"{ig_id}/media", {
        "fields": "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count",
        "limit": 100, "access_token": token,
    })
    while True:
        media.extend(resp.get("data", []))
        nxt = resp.get("paging", {}).get("next")
        if not nxt:
            break
        resp = _get_full_url(nxt)
        time.sleep(0.3)
    return media


def fetch_insights(media_id, token):
    """Return {metric: value} for a post, trying the broad metric set and dropping
    any the API rejects for this media type/version."""
    out = {}
    for metric in POST_METRICS:
        try:
            r = _get(f"{media_id}/insights", {"metric": metric, "access_token": token})
            vals = r.get("data", [])
            if vals:
                v = vals[0].get("values", [{}])[0].get("value")
                out[metric] = v
        except Exception:
            continue  # metric not supported for this post - skip
    return out


def main():
    token = _token()
    print("Finding Instagram Business account...")
    ig_id, username, pg_token = find_ig_account(token)

    print("Fetching media list...")
    media = fetch_media(ig_id, pg_token)
    print(f"  {len(media)} posts found. Pulling insights (this can take a minute)...")

    rows = []
    for i, m in enumerate(media, 1):
        ins = fetch_insights(m["id"], pg_token)
        cap = (m.get("caption") or "").replace("\n", " ").strip()
        rows.append({
            "date": (m.get("timestamp") or "")[:10],
            "type": m.get("media_product_type") or m.get("media_type") or "",
            "hook": cap[:80],
            "reach": ins.get("reach", ""),
            "impressions": ins.get("impressions", ins.get("views", "")),
            "likes": ins.get("likes", m.get("like_count", "")),
            "comments": ins.get("comments", m.get("comments_count", "")),
            "saves": ins.get("saved", ""),
            "shares": ins.get("shares", ""),
            "total_interactions": ins.get("total_interactions", ""),
            "profile_visits": ins.get("profile_visits", ""),
            "permalink": m.get("permalink", ""),
        })
        if i % 10 == 0:
            print(f"    ...{i}/{len(media)}")
        time.sleep(0.2)

    cols = ["date", "type", "hook", "reach", "impressions", "likes", "comments",
            "saves", "shares", "total_interactions", "profile_visits", "permalink"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    print(f"\nDone. Wrote {len(rows)} posts -> {OUT_CSV}")
    print("NOTE: IG's API does not expose per-post outbound link clicks for organic "
          "feed posts - use UTM links + GA4 to measure clicks-to-site. This CSV covers "
          "reach, impressions/views, saves, shares and engagement, which is what we "
          "need for the reach/engagement side.")


if __name__ == "__main__":
    main()
