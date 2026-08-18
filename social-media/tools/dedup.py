"""
Dedup utilities — prevents reuse of photos, design patterns, and content topics.

Usage in generators:
    from dedup import get_used_hashes, register_used_hashes, get_used_designs

Photo hashes are the 12-char prefix of cache filenames (e.g. "2ca33be9d2f7" from "2ca33be9d2f7_nobg.png").
"""
import os
import json
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR  = os.path.join(BASE_DIR, "memory")
CACHE_DIR   = os.path.join(BASE_DIR, "assets", "pexels_cache")
WEEKS_JSON  = os.path.join(BASE_DIR, "iw-content-hub", "data", "weeks.json") \
              if os.path.exists(os.path.join(BASE_DIR, "iw-content-hub")) \
              else os.path.join(BASE_DIR, "..", "iw-content-hub", "data", "weeks.json")

USED_IMAGES_PATH  = os.path.join(MEMORY_DIR, "used_images.json")
DESIGN_REG_PATH   = os.path.join(MEMORY_DIR, "design_registry.json")

PEXELS_API_KEY    = os.getenv("PEXELS_API_KEY")
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"


# ─── Image dedup ──────────────────────────────────────────────────────────────

def _load_used_images():
    if not os.path.exists(USED_IMAGES_PATH):
        return {}
    with open(USED_IMAGES_PATH) as f:
        return json.load(f).get("used_hashes", {})


def _save_used_images(used):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(USED_IMAGES_PATH, "w") as f:
        json.dump({"used_hashes": used}, f, indent=2)


def get_used_hashes() -> set:
    """Return set of 12-char cache hashes that are already used in published posts."""
    return set(_load_used_images().keys())


def register_used_hashes(hashes: list, post_id: str, week_id: str):
    """Mark image hashes as used. Call after a generator succeeds."""
    used = _load_used_images()
    for h in hashes:
        used[h] = {"post": post_id, "week": week_id}
    _save_used_images(used)


def _cache_hash(query: str, photo_id) -> str:
    key = f"{query}_{photo_id}"
    return hashlib.md5(key.encode()).hexdigest()[:12]


def _cache_path(h: str, ext: str) -> str:
    return os.path.join(CACHE_DIR, f"{h}.{ext}")


def get_cutout_unique(query: str, orientation: str = "portrait",
                      extra_exclude: set = None) -> str:
    """
    Fetch a Pexels photo + rembg cutout that hasn't been used before.
    Skips any photo whose cache hash is in used_images.json OR extra_exclude.
    Returns path to _nobg.png.
    """
    if not PEXELS_API_KEY:
        raise RuntimeError("PEXELS_API_KEY not set in .env")

    blocked = get_used_hashes()
    if extra_exclude:
        blocked |= set(extra_exclude)

    headers = {"Authorization": PEXELS_API_KEY}
    params  = {"query": query, "per_page": 30, "orientation": orientation}
    r = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    photos = r.json().get("photos", [])

    for photo in photos:
        h = _cache_hash(query, photo["id"])
        if h in blocked:
            continue

        jpg_path = _cache_path(h, "jpg")
        if not os.path.exists(jpg_path):
            img_r = requests.get(photo["src"]["large"], timeout=30)
            img_r.raise_for_status()
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(jpg_path, "wb") as f:
                f.write(img_r.content)

        nobg_path = _cache_path(h, "jpg").replace(".jpg", "_nobg.png")
        if not os.path.exists(nobg_path):
            from rembg import remove, new_session
            session = new_session("isnet-general-use")
            with open(jpg_path, "rb") as f:
                data = f.read()
            out = remove(data, session=session)
            with open(nobg_path, "wb") as f:
                f.write(out)

        print(f"  photo selected: {h} (Pexels ID {photo['id']})")
        return nobg_path

    raise RuntimeError(f"No unused Pexels photos found for query: '{query}' (tried {len(photos)})")


# ─── Design pattern dedup ─────────────────────────────────────────────────────

def _load_design_registry():
    if not os.path.exists(DESIGN_REG_PATH):
        return {}
    with open(DESIGN_REG_PATH) as f:
        return json.load(f)


def _save_design_registry(reg):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(DESIGN_REG_PATH, "w") as f:
        json.dump(reg, f, indent=2)


def get_used_designs() -> dict:
    """Return dict of {hook_layout_name: post_id} for already used hook designs."""
    return _load_design_registry().get("hook_layouts", {})


def register_design(layout_name: str, post_id: str, week_id: str):
    """Record a hook slide design pattern as used."""
    reg = _load_design_registry()
    if "hook_layouts" not in reg:
        reg["hook_layouts"] = {}
    reg["hook_layouts"][layout_name] = {"post": post_id, "week": week_id}
    _save_design_registry(reg)


# ─── Content topic dedup ──────────────────────────────────────────────────────

def get_past_topics() -> list:
    """Return list of past post titles from weeks.json."""
    # Try a few candidate paths for weeks.json
    candidates = [
        os.path.join(BASE_DIR, "iw-content-hub", "data", "weeks.json"),
        os.path.join(BASE_DIR, "..", "iw-content-hub", "data", "weeks.json"),
        os.path.join(os.path.expanduser("~"), "Claude", "iw-content-hub", "data", "weeks.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            return [post["title"] for week in data.get("weeks", [])
                    for post in week.get("posts", [])]
    return []
