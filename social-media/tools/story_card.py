"""Build Instagram-Story images (1080x1920) from post cover slides.

Instagram Stories cap image width at 1920px, so the 2160px feed slides are
rejected. This composes each post's cover slide onto a 1080x1920 brand-navy
canvas (rounded corners + soft shadow) -> images/<week>/<pid>/story.png, which
ayrshare_publish.py uses for the Story companion of each post.

    python3 tools/story_card.py week14                 # all story-eligible posts
    python3 tools/story_card.py week14 mon,tue          # only these day keys
"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
HUB  = os.path.dirname(os.path.dirname(HERE))
WEEKS = os.path.join(HUB, "data", "weeks.json")
W, H, CARD, RADIUS = 1080, 1920, 1000, 30
NAVY_TOP, NAVY_BOT = (26, 26, 46), (12, 12, 28)
# Lanes that get an Instagram Story (i.e. lanes posted to Instagram).
STORY_LANES = {"news", "quote", "fun", "education"}


def _bg():
    bg = Image.new("RGB", (W, H)); px = bg.load()
    for y in range(H):
        t = y / (H - 1)
        row = tuple(int(NAVY_TOP[i] + (NAVY_BOT[i] - NAVY_TOP[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = row
    return bg


def _mask():
    m = Image.new("L", (CARD, CARD), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, CARD, CARD], radius=RADIUS, fill=255)
    return m


def make_story(src, dst):
    card = Image.open(src).convert("RGB").resize((CARD, CARD), Image.LANCZOS)
    bg = _bg()
    cx, cy = (W - CARD) // 2, (H - CARD) // 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [cx, cy + 16, cx + CARD, cy + CARD + 16], radius=RADIUS, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    bg.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), shadow.split()[3])
    bg.paste(card, (cx, cy), _mask())
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    bg.save(dst, "PNG")


def main():
    wid = sys.argv[1] if len(sys.argv) > 1 else "week14"
    days = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None
    week = next(w for w in json.load(open(WEEKS))["weeks"] if w["id"] == wid)
    img = os.path.join(HUB, "images", wid)
    made = []
    for p in week["posts"]:
        if p.get("lane") not in STORY_LANES:
            continue
        if days and p["id"].split("-")[-2] not in days:
            continue
        src = os.path.join(img, p["id"], (p.get("slides") or ["slide_1.png"])[0])
        if os.path.exists(src):
            make_story(src, os.path.join(img, p["id"], "story.png"))
            made.append(p["id"])
    print(f"made story.png for {len(made)} posts in {wid}")


if __name__ == "__main__":
    main()
