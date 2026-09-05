"""ingest_analytics.py - fold the weekly MANUAL exports into the past-data layer.

Ayrshare alone is too thin to judge performance (near-zero engagement volumes).
Every Friday night the operator hands over richer exports; this parses them into
two committed files that both the dashboard and the Saturday build read:

  social-media/content/analytics_history.json   ROLLING, comprehensive past data
      one dated snapshot per week (LinkedIn per-post + demographics, GSC search
      demand for the IG profile + YouTube channel). Grows over time.
  social-media/content/planning_signals.json    DECISION inputs for build_week
      search-demand topics (what people actually Google), best day, follower mix.

Inputs (auto-discovered; override with flags):
  <dir>/LinkedIn/internwise_content_*.xls        (per-post: 'All posts' sheet)
  <dir>/LinkedIn/internwise_followers_*.xls       (demographics)
  <dir>/LinkedIn/internwise_visitors_*.xls        (page visitors)
  <dir>/instagram.com_*-Performance-on-Search-*.zip   (Google Search Console)
  <dir>/youtube.com_*-Performance-on-Search-*.zip     (Google Search Console)

    python3 tools/ingest_analytics.py                    # discover in ~/Downloads
    python3 tools/ingest_analytics.py --dir /path/to/exports
    python3 tools/ingest_analytics.py --date 2026-09-05  # stamp the snapshot
"""
from __future__ import annotations
import os, sys, json, glob, zipfile, csv, io, argparse, datetime, warnings
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
SM   = os.path.dirname(HERE)
HUB  = os.path.dirname(SM)
HISTORY  = os.path.join(SM, "content", "analytics_history.json")
SIGNALS  = os.path.join(SM, "content", "planning_signals.json")

DOW = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# Brand / navigational search queries - excluded from search-DEMAND topics (those
# feed education topic planning; brand lookups don't tell us what content to make).
BRAND_Q = ("internwise", "interwise", "intern wise", "gradwiz", "internwis")


def _latest(pattern):
    hits = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return hits[0] if hits else None


def discover(base):
    lk = os.path.join(base, "LinkedIn")
    return {
        "content":   _latest(os.path.join(lk, "*content*.xls")),
        "followers": _latest(os.path.join(lk, "*followers*.xls")),
        "visitors":  _latest(os.path.join(lk, "*visitors*.xls")),
        "gsc_ig":    _latest(os.path.join(base, "instagram.com_*Performance-on-Search*.zip")),
        "gsc_yt":    _latest(os.path.join(base, "youtube.com_*Performance-on-Search*.zip")),
    }


# ---------------- LinkedIn ----------------

def parse_linkedin_content(path):
    import pandas as pd
    df = pd.read_excel(path, sheet_name="All posts", header=1)
    df["Created date"] = pd.to_datetime(df["Created date"], errors="coerce")
    df = df.dropna(subset=["Created date"]).sort_values("Created date")
    num = lambda c: pd.to_numeric(df.get(c), errors="coerce").fillna(0)
    impr = num("Impressions")
    df["dow"] = df["Created date"].dt.day_name()
    df["isoweek"] = df["Created date"].dt.isocalendar().week.astype(int)

    by_week = [{"week": int(w), "posts": int(len(g)),
                "impressions": int(g["Impressions"].sum()),
                "meanImpressions": round(float(g["Impressions"].mean()), 1)}
               for w, g in df.groupby("isoweek")]
    by_dow = {}
    for d, g in df.groupby("dow"):
        by_dow[d] = {"posts": int(len(g)),
                     "meanImpressions": round(float(g["Impressions"].mean()), 1),
                     "meanLikes": round(float(pd.to_numeric(g["Likes"], errors="coerce").fillna(0).mean()), 2)}
    top = (df.sort_values("Impressions", ascending=False).head(6))
    top_posts = [{"date": str(r["Created date"])[:10], "impressions": int(r["Impressions"]),
                  "clicks": int(pd.to_numeric([r.get("Clicks", 0)])[0] or 0),
                  "likes": int(pd.to_numeric([r.get("Likes", 0)])[0] or 0),
                  "title": str(r.get("Post title", ""))[:90]}
                 for _, r in top.iterrows()]
    return {
        "dateRange": [str(df["Created date"].min())[:10], str(df["Created date"].max())[:10]],
        "totals": {"posts": int(len(df)), "impressions": int(impr.sum()),
                   "clicks": int(num("Clicks").sum()), "likes": int(num("Likes").sum()),
                   "comments": int(num("Comments").sum()), "reposts": int(num("Reposts").sum()),
                   "follows": int(num("Follows").sum())},
        "meanImpressions": round(float(impr.mean()), 1) if len(df) else 0,
        "byWeek": sorted(by_week, key=lambda x: x["week"]),
        "byDow": {d: by_dow[d] for d in DOW if d in by_dow},
        "topPosts": top_posts,
    }


def parse_linkedin_followers(path):
    import pandas as pd
    xl = pd.ExcelFile(path)
    out = {}
    def top(sheet, key, n=5):
        if sheet not in xl.sheet_names:
            return
        df = xl.parse(sheet)
        if df.shape[1] >= 2:
            df = df.dropna()
            out[key] = [{"label": str(r.iloc[0]), "value": int(r.iloc[1])}
                        for _, r in df.head(n).iterrows()]
    if "New followers" in xl.sheet_names:
        nf = xl.parse("New followers")
        col = "Total followers" if "Total followers" in nf.columns else nf.columns[-1]
        out["newFollowersInWindow"] = int(pd.to_numeric(nf[col], errors="coerce").fillna(0).sum())
    top("Location", "byLocation"); top("Seniority", "bySeniority", 8)
    top("Job function", "byFunction"); top("Industry", "byIndustry"); top("Company size", "byCompanySize", 8)
    return out


# ---------------- GSC (Search Console) ----------------

def parse_gsc(zip_path):
    def read(name):
        with zipfile.ZipFile(zip_path) as z:
            for n in z.namelist():
                if n.endswith(name):
                    return list(csv.DictReader(io.TextIOWrapper(z.open(n), "utf-8")))
        return []
    def _i(v):
        try: return int(float(str(v).replace(",", "")))
        except Exception: return 0
    chart = read("Chart.csv")
    queries = read("Queries.csv")
    clicks = sum(_i(r.get("Clicks")) for r in chart)
    impr = sum(_i(r.get("Impressions")) for r in chart)
    q = [{"q": r.get("Top queries", ""), "impressions": _i(r.get("Impressions")),
          "clicks": _i(r.get("Clicks")), "position": r.get("Position", "")}
         for r in queries]
    q.sort(key=lambda x: x["impressions"], reverse=True)
    return {"clicks": clicks, "impressions": impr, "topQueries": q[:20]}


def _is_brand(query):
    ql = (query or "").lower()
    return any(b in ql for b in BRAND_Q)


# ---------------- assemble + write ----------------

def build_snapshot(files, captured):
    snap = {"capturedAt": captured, "windowDays": 28}
    if files.get("content"):
        try: snap.setdefault("linkedin", {}).update(parse_linkedin_content(files["content"]))
        except Exception as e: print("  ! LinkedIn content parse failed:", e)
    if files.get("followers"):
        try: snap.setdefault("linkedin", {})["followers"] = parse_linkedin_followers(files["followers"])
        except Exception as e: print("  ! LinkedIn followers parse failed:", e)
    for key, dst in (("gsc_ig", "instagram"), ("gsc_yt", "youtube")):
        if files.get(key):
            try: snap.setdefault("gsc", {})[dst] = parse_gsc(files[key])
            except Exception as e: print(f"  ! GSC {dst} parse failed:", e)
    return snap


def make_signals(snap):
    """Distil the snapshot into decision inputs for the Saturday build."""
    demand = []
    for src, block in (snap.get("gsc") or {}).items():
        for q in block.get("topQueries", []):
            if q["impressions"] >= 20 and not _is_brand(q["q"]):
                demand.append({"query": q["q"], "impressions": q["impressions"], "source": src})
    demand.sort(key=lambda x: x["impressions"], reverse=True)

    best_day = None
    dows = ((snap.get("linkedin") or {}).get("byDow")) or {}
    if dows:
        best_day = max(dows.items(), key=lambda kv: kv[1].get("meanImpressions", 0))[0]

    return {
        "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "capturedAt": snap["capturedAt"],
        "searchDemandTopics": demand[:25],
        "bestDayLinkedIn": best_day,
        "followerMix": (snap.get("linkedin") or {}).get("followers", {}),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default=os.path.expanduser("~/Downloads"), help="folder holding the exports")
    p.add_argument("--date", default=datetime.date.today().isoformat(), help="snapshot date (YYYY-MM-DD)")
    args = p.parse_args()

    files = discover(args.dir)
    print("Discovered:")
    for k, v in files.items():
        print(f"  {k:10} {'-> ' + os.path.basename(v) if v else '(missing)'}")
    if not any(files.values()):
        sys.exit(f"No exports found under {args.dir}. Nothing to ingest.")

    snap = build_snapshot(files, args.date)

    hist = {"snapshots": []}
    if os.path.exists(HISTORY):
        hist = json.load(open(HISTORY))
    hist["snapshots"] = [s for s in hist.get("snapshots", []) if s.get("capturedAt") != args.date] + [snap]
    hist["snapshots"].sort(key=lambda s: s["capturedAt"])
    hist["generatedAt"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    json.dump(hist, open(HISTORY, "w"), indent=2, ensure_ascii=False); open(HISTORY, "a").write("\n")
    print(f"\nWrote {HISTORY} ({len(hist['snapshots'])} weekly snapshot(s)).")

    signals = make_signals(snap)
    json.dump(signals, open(SIGNALS, "w"), indent=2, ensure_ascii=False); open(SIGNALS, "a").write("\n")
    print(f"Wrote {SIGNALS} ({len(signals['searchDemandTopics'])} demand topics; "
          f"best LinkedIn day: {signals['bestDayLinkedIn']}).")
    if signals["searchDemandTopics"]:
        print("Top search-demand topics:")
        for t in signals["searchDemandTopics"][:6]:
            print(f"  - {t['query']}  ({t['impressions']} impr, {t['source']})")


if __name__ == "__main__":
    main()
