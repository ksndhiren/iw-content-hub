#!/usr/bin/env python3
"""QA gate for weekly social graphics.

This catches structural mistakes automatically and creates a contact sheet for
human overlap review. Some visual collisions are subjective after rasterization,
so the script deliberately requires --ack-overlap-review before it exits cleanly.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
SOCIAL = HERE.parent
HUB = SOCIAL.parent
WEEKS = HUB / "data" / "weeks.json"
IMG_ROOT = HUB / "images"
AUTHORS = SOCIAL / "assets" / "quote_authors"
AYRSHARE_POSTED = SOCIAL / "content" / "ayrshare_posted.json"

CORE_LANES = ("education", "quote", "engagement")
CORE_LANE_LABELS = {
    "education": "Education",
    "quote": "Quote",
    "engagement": "Poll/Conversation",
}
EXTS = ("jpg", "jpeg", "png", "webp")
FUN_DEDUP_WEEKS = 8


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def load_week(week_id: str) -> dict:
    data = json.loads(WEEKS.read_text())
    try:
        return next(w for w in data["weeks"] if w["id"] == week_id)
    except StopIteration:
        raise SystemExit(f"Unknown week id: {week_id}")


def quote_bank() -> dict:
    path = SOCIAL / "content" / "quotes_bank.json"
    data = json.loads(path.read_text())
    return {q["id"]: q for q in data["quotes"]}


def posted_ids() -> set[str]:
    try:
        data = json.loads(AYRSHARE_POSTED.read_text())
    except Exception:
        return set()
    return {str(k).split(":", 1)[0] for k in data.keys()}


def posted_index(all_weeks: list[dict]) -> dict[str, str]:
    ids = posted_ids()
    out = {}
    for wk in all_weeks:
        for post in wk.get("posts", []):
            if post.get("id") in ids and post.get("title"):
                out[slug(post.get("title", ""))] = post.get("id", "")
    return out


def portrait_path(author: str) -> Path | None:
    s = slug(author)
    if not s:
        return None
    for ext in EXTS:
        path = AUTHORS / f"{s}.{ext}"
        if path.exists():
            return path
    return None


def image_has_pixels(path: Path) -> bool:
    try:
        im = Image.open(path).convert("RGB")
    except Exception:
        return False
    if im.width < 1000 or im.height < 1000:
        return False
    small = im.resize((32, 32), Image.Resampling.LANCZOS)
    extrema = small.getextrema()
    return any(hi - lo > 8 for lo, hi in extrema)


def contact_sheet(week: dict, out_path: Path) -> Path:
    posts = week["posts"]
    thumbs = []
    for post in posts:
        first_slide = (post.get("slides") or ["slide_1.png"])[0]
        path = IMG_ROOT / week["id"] / post["id"] / first_slide
        if not path.exists():
            continue
        im = Image.open(path).convert("RGB")
        im = ImageOps.contain(im, (260, 260), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (300, 340), "white")
        x = (300 - im.width) // 2
        canvas.paste(im, (x, 12))
        d = ImageDraw.Draw(canvas)
        label = f"{post.get('day','')} | {post.get('lane','')} | {post.get('title','')}"
        d.text((12, 282), label[:38], fill=(24, 24, 32))
        d.text((12, 306), post["id"][:38], fill=(92, 92, 104))
        thumbs.append(canvas)

    cols = 5
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 300, max(1, rows) * 340), (244, 241, 234))
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * 300, (i // cols) * 340))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=92)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("week_id", nargs="?", default="week18")
    parser.add_argument("--ack-overlap-review", action="store_true",
                        help="Set only after reviewing the generated contact sheet for text/image/shape overlaps.")
    args = parser.parse_args()

    week = load_week(args.week_id)
    all_weeks = json.loads(WEEKS.read_text())["weeks"]
    quotes = quote_bank()
    already_posted = posted_index(all_weeks)
    current_posted = posted_ids()
    errors: list[str] = []

    by_day: dict[str, list[dict]] = defaultdict(list)
    for post in week["posts"]:
        by_day[post.get("day", "")].append(post)

    for day, posts in sorted(by_day.items()):
        core = [p for p in posts if p.get("lane") in CORE_LANES]
        lanes = [p.get("lane") for p in core]
        counts = Counter(lanes)
        missing = [lane for lane in CORE_LANES if counts[lane] == 0]
        dupes = [lane for lane, count in counts.items() if count > 1]
        if len(core) != len(CORE_LANES) or missing or dupes:
            expected = ", ".join(CORE_LANE_LABELS[lane] for lane in CORE_LANES)
            missing_labels = [CORE_LANE_LABELS.get(lane, lane) for lane in missing]
            errors.append(f"{day}: expected one each of {expected}; missing={missing_labels} duplicates={dupes}")

    seen_ids = Counter(p["id"] for p in week["posts"])
    for pid, count in seen_ids.items():
        if count > 1:
            errors.append(f"duplicate post id: {pid}")

    current_num = int(week["id"].replace("week", ""))
    recent_fun_ids = {}
    recent_fun_titles = {}
    for prev in all_weeks:
        try:
            prev_num = int(prev.get("id", "").replace("week", ""))
        except ValueError:
            continue
        if prev_num >= current_num or prev_num < current_num - FUN_DEDUP_WEEKS:
            continue
        for post in prev.get("posts", []):
            if post.get("lane") not in {"engagement", "fun"}:
                continue
            if post.get("ideaId"):
                recent_fun_ids[post["ideaId"]] = prev["id"]
            if post.get("title"):
                recent_fun_titles[post["title"].strip().lower()] = prev["id"]

    for post in week["posts"]:
        title_key = slug(post.get("title", ""))
        previous_post_id = already_posted.get(title_key)
        if title_key and previous_post_id and previous_post_id != post.get("id") and post.get("id") not in current_posted:
            errors.append(f"{post['id']}: title repeats already posted content from {previous_post_id}")

        slides = post.get("slides") or ["slide_1.png"]
        for slide in slides:
            path = IMG_ROOT / week["id"] / post["id"] / slide
            if not path.exists():
                errors.append(f"missing slide file: {path}")
            elif not image_has_pixels(path):
                errors.append(f"blank or undersized slide: {path}")

        if post.get("lane") == "quote":
            quote = quotes.get(post.get("quoteId", ""))
            author = (quote or {}).get("author") or post.get("title", "").replace("Quote:", "").strip()
            if not quote:
                errors.append(f"{post['id']}: unknown quote id {post.get('quoteId')}")
            elif not portrait_path(author):
                errors.append(f"{post['id']}: missing real quote portrait for {author!r}")

        if post.get("lane") == "engagement":
            idea_id = post.get("ideaId")
            title = post.get("title", "").strip().lower()
            if idea_id in recent_fun_ids:
                errors.append(f"{post['id']}: poll/conversation idea {idea_id} already used in {recent_fun_ids[idea_id]}")
            if title in recent_fun_titles:
                errors.append(f"{post['id']}: poll/conversation title already used in {recent_fun_titles[title]}")

    sheet = contact_sheet(week, Path("/private/tmp") / f"{week['id']}_overlap_qa.jpg")
    print(f"Overlap contact sheet: {sheet}")

    if not args.ack_overlap_review:
        errors.append("overlap review not acknowledged; inspect the contact sheet, fix collisions, then rerun with --ack-overlap-review")

    if errors:
        print("QA failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    print(f"QA passed for {week['id']}: active evergreen lanes per weekday incl. Poll/Conversation, quote portraits present, slide files valid, overlap review acknowledged. News is checked by the day-prior news job.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
