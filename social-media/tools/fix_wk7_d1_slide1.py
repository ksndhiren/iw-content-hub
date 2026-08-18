"""Fix D1 slide 1 with a video-call specific photo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import get_used_hashes, register_used_hashes, get_cutout_unique
import wk7_d1_videointerview as d1

OUT = "campaigns/outputs/week7/d1-videointerview"

print("Fixing D1 slide 1 (video interview photo)...")
d1._load_logos()
used = get_used_hashes()

# Try video-call specific queries. Fall back progressively if none work.
queries = [
    "person video call laptop webcam smiling professional",
    "young professional video conference laptop portrait",
    "student laptop video meeting home office professional",
    "young woman laptop screen video interview smiling",
]
photo = None
for q in queries:
    try:
        photo = get_cutout_unique(q, orientation="portrait", extra_exclude=used)
        if photo:
            print(f"  matched query: {q}")
            break
    except Exception as e:
        print(f"  no match for: {q} ({e})")
if not photo:
    print("  ERROR: no photo found")
    sys.exit(1)

h = os.path.basename(photo).replace("_nobg.png", "")
d1._slide1(os.path.join(OUT, "slide_1.png"), photo)
register_used_hashes([h], "week7/d1-videointerview/slide1-fix", "week7")
print(f"  done — hash {h}")
