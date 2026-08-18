"""Re-render only wk6 D5 slide 7 using the existing cached photo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wk6_d5_firstdays as d5

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(BASE_DIR, "assets", "pexels_cache")
OUT = "campaigns/outputs/week6/d5-firstdays"

d5._load_logos()
photo = os.path.join(CACHE, "db366eeb1555_nobg.png")
d5._slide7(os.path.join(OUT, "slide_7.png"), photo)
print("D5 slide 7 re-rendered")
