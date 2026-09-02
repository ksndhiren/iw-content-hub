"""
publish_featured.py — automate FEATURED job-ad posting, then clear the posted ones.

Flow (the dashboard approval is the human gate):
  1. A featured job appears on the dashboard as "in-review" (from the daily scrape).
  2. A human clicks Approve -> the KV status flips to "approved".
  3. This script (on a schedule) publishes every APPROVED featured job to the
     connected social networks via Ayrshare, immediately (job ads are time-
     sensitive), recording each send in content/ayrshare_posted.json so a re-run
     never double-posts.
  4. Every featured job that has actually been posted is then REMOVED from
     data/featured.json (images deleted from R2, sourceId recorded in
     featured_published.json so the daily scrape can't re-add it). New featured
     jobs keep flowing in from the scrape to take their place.

Safe by default: DRY-RUN unless --live is given. A job is only pruned once it is
confirmed posted (present in ayrshare_posted.json) — a failed send is left in
place for the next run, never silently dropped.

    python3 automation/publish_featured.py            # dry-run: show the plan
    python3 automation/publish_featured.py --live      # post approved + prune posted
"""
import os, sys, json, argparse, datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
_HUB  = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HUB, "social-media", "tools"))

import ayrshare_publish as ap        # the publisher (weeks + featured)
import sync_featured_jobs as sfj      # featured.json / published-set / R2 helpers


def _posted_pids(posted):
    """Set of post ids that have at least one recorded successful send."""
    return {k.split(":", 1)[0] for k in posted.keys()}


def publish(live):
    if not ap.KEY:
        sys.exit("No AYRSHARE_API_KEY in env (.env).")

    week = ap.load_featured_week()          # posts stamped lane='featured' + KV status
    connected = ap.active_networks()
    posted = ap.load_posted()

    approved = [p for p in week.get("posts", []) if p.get("status") == "approved"]
    # Featured job ads post immediately on approval (no schedule), so prune-after-
    # post stays correct.
    jobs = ap.build_jobs(week, connected, "approved", use_schedule=False)

    print(f"Featured | connected: {sorted(connected)} | approved: {len(approved)} "
          f"| {len(jobs)} post-jobs | {'LIVE' if live else 'DRY-RUN'}\n")

    todo = []
    for j in jobs:
        pkey = f"{j['pid']}:{j['network']}"
        already = pkey in posted
        print(f"  {j['pid']:20} -> {j['network']:10} [{len(j['text'])}c"
              f"{' TRIMMED' if j['trimmed'] else ''}] {len(j['mediaUrls'])} img | "
              f"{'ALREADY POSTED' if already else 'now'}")
        if not already:
            todo.append((pkey, j))

    if not live:
        print(f"\nDRY-RUN: nothing sent, nothing pruned. {len(todo)} would post. Add --live.")
        return

    print(f"\nLIVE: sending {len(todo)} ...")
    for pkey, j in todo:
        res = ap.post_job(j)
        ok = res.get("status") == "success" or res.get("id")
        print(f"  {pkey}: {'OK ' + str(res.get('id','')) if ok else 'FAIL ' + json.dumps(res)[:200]}")
        if ok:
            posted[pkey] = {"id": res.get("id"), "at": datetime.datetime.utcnow().isoformat(),
                            "network": j["network"], "scheduleDate": j.get("scheduleDate")}
            json.dump(posted, open(ap.POSTED, "w"), indent=2)

    prune_posted(posted)


def prune_posted(posted):
    """Remove featured jobs that are approved AND now posted, via the shared
    (posted-gated) prune in sync_featured_jobs so every prune path behaves the
    same. Deletes their R2 images and records the sourceId so the daily scrape
    can't re-add them."""
    statuses = sfj.fetch_statuses()
    data = sfj.load_featured()
    pub  = sfj.load_published()
    removed = sfj.prune_approved(data, statuses, pub, posted_ids=_posted_pids(posted))
    if removed:
        sfj.save_published(pub)
        with open(sfj.FEATURED_JSON, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False); f.write("\n")
        print(f"\nPruned {removed} posted featured job(s). posts remaining: {len(data['posts'])}.")
    else:
        print("\nNo posted featured jobs to prune.")


def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("--live", action="store_true", help="actually post + prune (default: dry-run)")
    args = ap_.parse_args()
    publish(args.live)


if __name__ == "__main__":
    main()
