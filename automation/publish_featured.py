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

    python3 automation/publish_featured.py                 # dry-run: show the plan
    python3 automation/publish_featured.py --live           # post ALL approved + prune posted
    python3 automation/publish_featured.py --live --per-day 1  # post at most one job/day
"""
import os, sys, json, argparse, datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
_HUB  = os.path.dirname(_HERE)
# Order matters: social-media/tools carries an older sync_featured_jobs.py that
# lacks fetch_statuses/prune_approved, so automation/ has to resolve FIRST.
sys.path.insert(0, os.path.join(_HUB, "social-media", "tools"))
sys.path.insert(0, _HERE)

import ayrshare_publish as ap        # the publisher (weeks + featured)
import sync_featured_jobs as sfj      # featured.json / published-set / R2 helpers


def _posted_pids(posted):
    """Set of post ids that have at least one recorded successful send."""
    return {k.split(":", 1)[0] for k in posted.keys()}


def _is_featured_pid(pid):
    """Featured job post ids are always `job-<sourceId>`; weekly lane posts are
    `week<N>-<day>-<lane>`. The Ayrshare ledger is shared by both."""
    return pid.startswith("job-")


def _pids_posted_today(posted):
    """Distinct FEATURED job ids with at least one send recorded today (UTC).
    Lets us cap posting to N jobs/day even across multiple runs.

    Only featured ids count: ayrshare_posted.json is shared with the weekly
    lanes, and counting those too made any day with a lane post look like the
    featured quota was already spent."""
    today = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).date().isoformat()
    return {k.split(":", 1)[0] for k, v in posted.items()
            if str((v or {}).get("at", ""))[:10] == today
            and _is_featured_pid(k.split(":", 1)[0])}


def _cap_per_day(todo, posted, per_day):
    """Trim the send list so at most `per_day` distinct jobs post today - finishing
    any job already started today first, then admitting new ones up to the budget.
    per_day <= 0 means no cap (post everything approved)."""
    if per_day <= 0:
        return todo
    started = _pids_posted_today(posted)
    budget = max(0, per_day - len(started))
    admitted, out = set(), []
    for pkey, j in todo:
        pid = j["pid"]
        if pid in started or pid in admitted:
            out.append((pkey, j))            # finish this job's remaining networks
        elif budget > 0:
            admitted.add(pid); budget -= 1
            out.append((pkey, j))
        # else: over the daily cap - leave for a future day
    return out


def publish(live, per_day=0):
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

    if per_day > 0:
        before = len({j["pid"] for _, j in todo})
        todo = _cap_per_day(todo, posted, per_day)
        after = len({j["pid"] for _, j in todo})
        print(f"\nDaily cap: {per_day}/day | posting {after} job(s) now "
              f"({before} approved & waiting){' - already met today' if after == 0 else ''}.")

    if not live:
        print(f"\nDRY-RUN: nothing sent, nothing pruned. {len(todo)} would post. Add --live.")
        return

    print(f"\nLIVE: sending {len(todo)} ...")
    for pkey, j in todo:
        res = ap.post_job(j)
        ok = res.get("status") == "success" or res.get("id")
        print(f"  {pkey}: {'OK ' + str(res.get('id','')) if ok else 'FAIL ' + json.dumps(res)[:200]}")
        if ok:
            posted[pkey] = {"id": res.get("id"), "at": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat(),
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
    ap_.add_argument("--per-day", type=int, default=0,
                     help="max distinct featured jobs to post per day (0 = no cap)")
    args = ap_.parse_args()
    publish(args.live, per_day=args.per_day)


if __name__ == "__main__":
    main()
