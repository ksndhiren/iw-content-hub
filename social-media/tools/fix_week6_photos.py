"""
Targeted fix for week 6 specific slides only.
- D3 slide 1: new photo with dark clothing (better rembg cutout)
- D4 slide 7: new photo with dark clothing (better contrast on coral arch)
- D5 slides 1 & 7: fresh photos (user flagged as repeating from prev weeks)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dedup import get_used_hashes, register_used_hashes, get_cutout_unique

# Import slide functions + logo loaders from each generator
import wk6_d3_personalstatement as d3
import wk6_d4_referral as d4
import wk6_d5_firstdays as d5

D3_OUT = "campaigns/outputs/week6/d3-personalstatement"
D4_OUT = "campaigns/outputs/week6/d4-referral"
D5_OUT = "campaigns/outputs/week6/d5-firstdays"


def fix_d3_slide1():
    print("Fixing D3 slide 1 (new photo with dark clothing)...")
    d3._load_logos()
    used = get_used_hashes()
    # Dark jacket query — rembg handles dark-on-white much better than white-on-white
    photo = get_cutout_unique(
        "young woman dark jacket writing notes portrait studio white background",
        orientation="portrait", extra_exclude=used
    )
    h = os.path.basename(photo).replace("_nobg.png", "")
    d3._slide1(os.path.join(D3_OUT, "slide_1.png"), photo)
    register_used_hashes([h], "week6/d3-personalstatement/fix", "week6")
    print(f"  D3 slide 1 done — hash {h}")


def fix_d4_slide7():
    print("Fixing D4 slide 7 (new photo with dark clothing)...")
    d4._load_logos()
    used = get_used_hashes()
    # Dark suit — better contrast against coral arch
    photo = get_cutout_unique(
        "young man dark suit business confident portrait studio white background",
        orientation="portrait", extra_exclude=used
    )
    h = os.path.basename(photo).replace("_nobg.png", "")
    d4._slide7(os.path.join(D4_OUT, "slide_7.png"), photo)
    register_used_hashes([h], "week6/d4-referral/fix", "week6")
    print(f"  D4 slide 7 done — hash {h}")


def fix_d5_slides():
    print("Fixing D5 slides 1 & 7 (fresh photos)...")
    d5._load_logos()
    used = get_used_hashes()

    # Slide 1: different demographic/pose from prev pick (was woman with tablet)
    photo1 = get_cutout_unique(
        "young man business casual confident smiling office portrait studio",
        orientation="portrait", extra_exclude=used
    )
    h1 = os.path.basename(photo1).replace("_nobg.png", "")

    used2 = used | {h1}
    # Slide 7: avoid graduation gown — go for office-ready professional
    photo7 = get_cutout_unique(
        "young woman dark blazer professional career portrait studio white background",
        orientation="portrait", extra_exclude=used2
    )
    h7 = os.path.basename(photo7).replace("_nobg.png", "")

    d5._slide1(os.path.join(D5_OUT, "slide_1.png"), photo1)
    d5._slide7(os.path.join(D5_OUT, "slide_7.png"), photo7)
    register_used_hashes([h1, h7], "week6/d5-firstdays/fix", "week6")
    print(f"  D5 slide 1 done — hash {h1}")
    print(f"  D5 slide 7 done — hash {h7}")


if __name__ == "__main__":
    fix_d3_slide1()
    fix_d4_slide7()
    fix_d5_slides()
    print("\nAll photo fixes done.")
