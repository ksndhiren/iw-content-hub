"""Image generation API wrapper (DALL-E 3 default, Stable Diffusion fallback)."""

from __future__ import annotations

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

PLATFORM_DIMENSIONS = {
    "linkedin_banner": "1200x627",
    "instagram_square": "1080x1080",
    "instagram_story": "1080x1920",
    "x_card": "1200x675",
    "tiktok_vertical": "1080x1920",
}


def generate_image(prompt: str, size: str = "1024x1024", output_path: str | None = None) -> dict:
    """Generate an image from a text prompt.

    Args:
        prompt: Descriptive image generation prompt.
        size: Image dimensions (e.g. "1024x1024", "1792x1024", "1024x1792").
        output_path: Optional path to save the image file.

    Returns:
        Dict with image_url, size, and local_path (if saved).
    """
    if OPENAI_API_KEY:
        return _generate_dalle(prompt, size, output_path)
    elif STABILITY_API_KEY:
        return _generate_stability(prompt, size, output_path)
    else:
        return _mock_generate(prompt, size, output_path)


def _generate_dalle(prompt: str, size: str, output_path: str | None) -> dict:
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    # DALL-E 3 supported sizes
    dalle_size = _map_to_dalle_size(size)
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": dalle_size,
        "quality": "hd",
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    if resp.status_code != 200:
        print(f"DALL-E error: {resp.status_code} — {resp.text}")
        resp.raise_for_status()
    image_url = resp.json()["data"][0]["url"]

    local_path = None
    if output_path:
        local_path = _download_image(image_url, output_path)

    return {"image_url": image_url, "size": dalle_size, "local_path": local_path}


def _generate_stability(prompt: str, size: str, output_path: str | None) -> dict:
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    w, h = (int(d) for d in size.split("x"))
    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "width": min(w, 1024),
        "height": min(h, 1024),
        "samples": 1,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    import base64
    img_data = base64.b64decode(resp.json()["artifacts"][0]["base64"])

    local_path = None
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(img_data)
        local_path = output_path

    return {"image_url": None, "size": size, "local_path": local_path}


def _mock_generate(prompt: str, size: str, output_path: str | None) -> dict:
    """Return mock result for dry-run / testing."""
    return {
        "image_url": "https://example.com/mock-image.png",
        "size": size,
        "local_path": output_path,
        "mock": True,
        "prompt_used": prompt,
    }


def _map_to_dalle_size(size: str) -> str:
    """Map arbitrary size to nearest DALL-E 3 supported size."""
    w, h = (int(d) for d in size.split("x"))
    ratio = w / h
    if ratio > 1.3:
        return "1792x1024"
    elif ratio < 0.77:
        return "1024x1792"
    else:
        return "1024x1024"


def _download_image(url: str, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    Path(output_path).write_bytes(resp.content)
    return output_path
