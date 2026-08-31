"""Google Search Console -> topic-demand signal for the content engine.

Pulls what people search on Google to reach internwise.co.uk (top + rising
queries, top pages) and writes data/search_console.json, which the dashboard's
Insights tab and the topic engine read. Uses a Google service account (headless,
cloud-friendly - no interactive OAuth), so it runs unattended in CI.

Setup (one-off, done in the user's Google Cloud + Search Console):
  1. Google Cloud console -> create a project (or reuse) -> enable
     "Google Search Console API".
  2. Create a Service Account -> add a JSON key -> download it.
  3. In Search Console (search.google.com/search-console) open the
     internwise.co.uk property -> Settings -> Users and permissions ->
     add the service account's email (…iam.gserviceaccount.com) as a
     Full or Restricted user.
  4. Save the JSON key to social-media/secrets/gsc-service-account.json
     (gitignored) and set GSC_SITE_URL in .env.

    python3 tools/gsc_fetch.py --list-sites     # confirm the property string
    python3 tools/gsc_fetch.py                  # write data/search_console.json
"""
from __future__ import annotations
import os, sys, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
HUB  = os.path.dirname(SM)
OUT  = os.path.join(HUB, "data", "search_console.json")
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
API = "https://searchconsole.googleapis.com/webmasters/v3"


def _load_env():
    for p in (os.path.join(SM, ".env"), os.path.join(HUB, ".env")):
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
_load_env()

SA_JSON  = os.getenv("GSC_SA_JSON", os.path.join(SM, "secrets", "gsc-service-account.json"))
SITE_URL = os.getenv("GSC_SITE_URL", "sc-domain:internwise.co.uk")


def _session():
    """Authorised requests session from the service-account key."""
    import requests
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    if not os.path.exists(SA_JSON):
        sys.exit(f"Service-account key not found at {SA_JSON} "
                 f"(set GSC_SA_JSON or drop the file there).")
    creds = service_account.Credentials.from_service_account_file(SA_JSON, scopes=[SCOPE])
    return AuthorizedSession(creds)


def list_sites():
    s = _session()
    r = s.get(f"{API}/sites"); r.raise_for_status()
    for site in r.json().get("siteEntry", []):
        print(f"  {site.get('permissionLevel'):20} {site.get('siteUrl')}")


def _query(s, start, end, dimensions, row_limit=100):
    body = {"startDate": start, "endDate": end, "dimensions": dimensions,
            "rowLimit": row_limit, "dataState": "final"}
    r = s.post(f"{API}/sites/{SITE_URL.replace('/', '%2F') if not SITE_URL.startswith('sc-domain') else SITE_URL}/searchAnalytics/query",
               json=body)
    if r.status_code != 200:
        sys.exit(f"GSC query failed ({r.status_code}): {r.text[:300]}")
    return r.json().get("rows", [])


def _row(r):
    return {"key": r["keys"][0], "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0), 4), "position": round(r.get("position", 0), 1)}


def fetch():
    s = _session()
    today = datetime.date.today()
    end = today - datetime.timedelta(days=3)          # GSC lags ~2-3 days
    start = end - datetime.timedelta(days=27)          # last 28 days
    prev_end = start - datetime.timedelta(days=1)
    prev_start = prev_end - datetime.timedelta(days=27)  # prior 28 days

    cur = {r["keys"][0]: _row(r) for r in _query(s, start.isoformat(), end.isoformat(), ["query"])}
    prev = {r["keys"][0]: _row(r) for r in _query(s, prev_start.isoformat(), prev_end.isoformat(), ["query"])}
    pages = [_row(r) for r in _query(s, start.isoformat(), end.isoformat(), ["page"], row_limit=50)]

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
    print("Top 10 by clicks:")
    for r in top[:10]:
        print(f"  {r['clicks']:4} clicks | {r['impressions']:6} impr | pos {r['position']:4} | {r['key']}")


if __name__ == "__main__":
    if "--list-sites" in sys.argv:
        list_sites()
    else:
        fetch()
