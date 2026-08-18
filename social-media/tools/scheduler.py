"""Social platform publisher / scheduler."""

from __future__ import annotations

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")


def schedule_post(
    platform: str,
    content: dict,
    publish_at: str | None = None,
) -> dict:
    """Schedule or immediately publish a post to a social platform.

    Args:
        platform: Target platform (linkedin, instagram, x, tiktok).
        content: Content package with copy, media URLs, etc.
        publish_at: ISO 8601 datetime for scheduled publishing, or None for immediate.

    Returns:
        Dict with post_id, platform, status, and scheduled_time.
    """
    if not content.get("human_approved"):
        return {
            "error": "Content must be human-approved before publishing.",
            "status": "blocked",
        }

    if BUFFER_ACCESS_TOKEN:
        return _publish_via_buffer(platform, content, publish_at)
    else:
        return _publish_direct(platform, content, publish_at)


def _publish_via_buffer(platform: str, content: dict, publish_at: str | None) -> dict:
    """Publish via Buffer API."""
    url = "https://api.bufferapp.com/1/updates/create.json"
    payload = {
        "access_token": BUFFER_ACCESS_TOKEN,
        "text": content.get("copy", ""),
        "profile_ids[]": [_get_buffer_profile_id(platform)],
        "now": publish_at is None,
    }
    if publish_at:
        payload["scheduled_at"] = publish_at

    if content.get("image_url"):
        payload["media[photo]"] = content["image_url"]

    resp = requests.post(url, data=payload, timeout=15)
    resp.raise_for_status()
    result = resp.json()

    return {
        "post_id": result.get("updates", [{}])[0].get("id", "unknown"),
        "platform": platform,
        "status": "scheduled" if publish_at else "published",
        "scheduled_time": publish_at,
    }


def _publish_direct(platform: str, content: dict, publish_at: str | None) -> dict:
    """Direct platform publish (mock for now — implement per-platform SDKs)."""
    return {
        "post_id": f"mock-{platform}-{datetime.utcnow().isoformat()}",
        "platform": platform,
        "status": "mock_published",
        "scheduled_time": publish_at,
        "content_preview": content.get("copy", "")[:100],
    }


def _get_buffer_profile_id(platform: str) -> str:
    """Return the Buffer profile ID for a given platform.

    In production, query Buffer's /profiles endpoint.
    """
    profile_map = {
        "linkedin": os.getenv("BUFFER_LINKEDIN_PROFILE_ID", ""),
        "instagram": os.getenv("BUFFER_INSTAGRAM_PROFILE_ID", ""),
        "x": os.getenv("BUFFER_X_PROFILE_ID", ""),
        "tiktok": os.getenv("BUFFER_TIKTOK_PROFILE_ID", ""),
    }
    return profile_map.get(platform, "")
