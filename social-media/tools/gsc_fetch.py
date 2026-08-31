"""Google Search Console -> topic-demand signal for the content engine.

Pulls what people search on Google to reach internwise.co.uk (top + rising
queries, top pages) and writes data/search_console.json, which the dashboard's
Insights tab and the topic engine read.

Auth reuses the OAuth refresh-token already set up for the site-monitor project
(GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / GOOGLE_REFRESH_TOKEN) - a long-lived
token for the user's Google account, so it can read every Search Console
property that account owns, no service-account key needed. Headless/cloud-safe.

    python3 tools/gsc_fetch.py --list-sites     # show properties -> confirm string
    python3 tools/gsc_fetch.py                  # write data/search_console.json
"""
from __future__ import annotations
import os, sys, json, datetime, urllib.request, urllib.error, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
HUB  = os.path.dirname(SM)
OUT  = os.path.join(HUB, "data", "search_console.json")
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://searchconsole.googleapis.com/webmasters/v3"


def _load_env():
    for p in (os.path.join(SM, ".env"), os.path.join(HUB, ".env")):
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"'))
_load_env()

SITE_URL = os.getenv("GSC_SITE_URL", "sc-domain:internwise.co.uk")


def _access_token():
    for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"):
        if not os.getenv(k):
            sys.exit(f"Missing {k} in env (.env).")
    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=30))["access_token"]
    except urllib.error.HTTPError as e:
        sys.exit(f"Token refresh failed ({e.code}): {e.read().decode()[:300]}")


def _api(token, path, body=None):
    url = f"{API}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit(f"GSC {path} failed ({e.code}): {e.read().decode()[:300]}")


def list_sites():
    token = _access_token()
    for s in _api(token, "sites").get("siteEntry", []):
        print(f"  {s.get('permissionLevel',''):22} {s.get('siteUrl')}")


def _query(token, start, end, dimensions, row_limit=100):
    body = {"startDate": start, "endDate": end, "dimensions": dimensions,
            "rowLimit": row_limit, "dataState": "final"}
    path = f"sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
    return _api(token, path, body).get("rows", [])


def _row(r):
    return {"key": r["keys"][0], "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0), 4), "position": round(r.get("position", 0), 1)}


def fetch():
    token = _access_token()
    today = datetime.date.today()
    end = today - datetime.timedelta(days=3)             # GSC lags ~2-3 days
    start = end - datetime.timedelta(days=27)             # last 28 days
    prev_end = start - datetime.timedelta(days=1)
    prev_start = prev_end - datetime.timedelta(days=27)   # prior 28 days

    cur = {r["keys"][0]: _row(r) for r in _query(token, start.isoformat(), end.isoformat(), ["query"])}
    prev = {r["keys"][0]: _row(r) for r in _query(token, prev_start.isoformat(), prev_end.isoformat(), ["query"])}
    pages = [_row(r) for r in _query(token, start.isoformat(), end.isoformat(), ["page"], row_limit=50)]

    top = sorted(cur.values(), key=lambda x: (x["clicks"], x["impressions"]), reverse=True)[:50]
    rising = []
    for q, row in cur.items():
        base = prev.get(q, {}).get("impressions", 0)
        delta = row["impressions"] - base
        if delta > 0:
            rising.append({**row, "prevImpressions": base, "deltaImpressions": delta,
                           "isNew": q not in prev})
    rising.sort(key=lambda x: x["deltaImpressions"], reverse=True)

    data = {
        "source": "google-search-console",
        "site": SITE_URL,
        "updatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "range": {"start": start.isoformat(), "end": end.isoformat()},
        "topQueries": top,
        "risingQueries": rising[:30],
        "topPages": sorted(pages, key=lambda x: x["clicks"], reverse=True)[:25],
    }
    json.dump(data, open(OUT, "w"), indent=2, ensure_ascii=False)
    print(f"Wrote {OUT}: {len(top)} top queries, {len(rising)} rising, {len(pages)} pages "
          f"({start} to {end}).")
    for r in top[:10]:
        print(f"  {r['clicks']:4} clicks | {r['impressions']:6} impr | pos {r['position']:4} | {r['key']}")


if __name__ == "__main__":
    (list_sites if "--list-sites" in sys.argv else fetch)()
