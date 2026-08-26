"""One-time (and re-runnable) backfill: upload the whole images/ tree to R2.
Key = path relative to images/ (e.g. week14/week14-mon-news/slide_1.png), which
is what the dashboard resolves against IMAGE_BASE_URL.

    python3 tools/r2_sync.py
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2

IMAGES = os.path.join(os.path.dirname(r2.SM), "images")

if __name__ == "__main__":
    r2.ensure_bucket()
    print("syncing", IMAGES, "->", r2.BUCKET)
    t = time.time()
    n = r2.upload_tree(IMAGES)
    print(f"backfilled {n} objects in {time.time()-t:.0f}s")
