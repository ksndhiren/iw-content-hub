"""
Pexels image utilities
- Fetch images via Pexels API
- Remove backgrounds via rembg
- Local caching
"""

import os
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "assets", "pexels_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"


def _cache_path(key, ext="jpg"):
    h = hashlib.md5(key.encode()).hexdigest()[:12]
    return os.path.join(CACHE_DIR, f"{h}.{ext}")


def search_pexels(query, per_page=10, orientation="portrait"):
    """Search Pexels for a query. Returns list of photo dicts."""
    if not PEXELS_API_KEY:
        raise RuntimeError("PEXELS_API_KEY not set in .env")

    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": orientation}
    r = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json().get("photos", [])


def download_image(url, cache_key):
    """Download an image with caching."""
    path = _cache_path(cache_key, "jpg")
    if os.path.exists(path):
        return path
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)
    return path


def remove_background(image_path):
    """Remove background using ISNet-General-Use (DIS model — sharp edges, fine hair detail,
    already cached at ~/.u2net/isnet-general-use.onnx, 168MB).
    Returns path to transparent PNG."""
    out_path = image_path.replace(".jpg", "_nobg.png")
    if os.path.exists(out_path):
        return out_path

    from rembg import remove, new_session
    session = new_session("isnet-general-use")
    with open(image_path, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data, session=session)
    with open(out_path, "wb") as f:
        f.write(output_data)
    return out_path


def get_cutout(query, index=0, orientation="portrait"):
    """
    Convenience: search query, pick result[index], download, remove bg.
    Returns path to transparent PNG cutout.
    """
    photos = search_pexels(query, per_page=max(5, index + 2), orientation=orientation)
    if not photos:
        raise RuntimeError(f"No Pexels results for: {query}")
    photo = photos[index]
    url = photo["src"]["large"]
    cache_key = f"{query}_{photo['id']}"
    jpg_path = download_image(url, cache_key)
    png_path = remove_background(jpg_path)
    return png_path


def get_photo(query, index=0, orientation="portrait", size="large"):
    """Download a Pexels photo (with background). Returns local path."""
    photos = search_pexels(query, per_page=max(5, index + 2), orientation=orientation)
    if not photos:
        raise RuntimeError(f"No Pexels results for: {query}")
    photo = photos[index]
    url = photo["src"][size]
    cache_key = f"{query}_{photo['id']}_{size}"
    return download_image(url, cache_key)


if __name__ == "__main__":
    # Quick test
    path = get_cutout("young professional smiling", index=0)
    print(f"Cutout saved: {path}")
