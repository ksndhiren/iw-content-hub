"""
prune_approved.py

Lightweight companion to sync_featured_jobs.py. Reads the shared post statuses
from the live dashboard KV endpoint and removes any FEATURED post that has been
marked "approved" (== published) from data/featured.json, deletes its images, and
records its sourceId in data/featured_published.json so the daily scrape never
re-adds it.

No browser / Playwright needed - it only reads the statuses API and edits JSON,
so it is cheap enough to run on a frequent schedule (e.g. hourly).

Run:  python3 automation/prune_approved.py
      STATUSES_URL=... FEATURED_HUB_DIR=... python3 automation/prune_approved.py
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import sync_featured_jobs as sfj


def main():
    print(f"Hub: {sfj.HUB_DIR}")
    statuses  = sfj.fetch_statuses()
    published = sfj.seed_published_from_statuses(statuses, sfj.load_published())
    data      = sfj.load_featured()

    before = len(data.get("posts", []))
    pruned = sfj.prune_approved(data, statuses, published)

    if pruned == 0:
        print("No approved featured posts to prune. Nothing to do.")
        return 0

    sfj.save_published(published)
    with open(sfj.FEATURED_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Pruned {pruned} approved post(s). posts {before} -> {len(data['posts'])}.")
    print(f"Wrote {sfj.FEATURED_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
