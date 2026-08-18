"""Brand memory layer — shared context for all agents."""

import json
import os
from pathlib import Path

MEMORY_DIR = Path(__file__).resolve().parent.parent / "memory"


def get_brand_memory() -> dict:
    """Load brand guidelines, past posts, and analytics into a single dict."""
    guidelines_path = MEMORY_DIR / "brand_guidelines.md"
    past_posts_path = MEMORY_DIR / "past_posts.json"
    analytics_path = MEMORY_DIR / "analytics.json"

    brand_guidelines = ""
    if guidelines_path.exists():
        brand_guidelines = guidelines_path.read_text()

    past_posts = {}
    if past_posts_path.exists():
        past_posts = json.loads(past_posts_path.read_text())

    analytics = {}
    if analytics_path.exists():
        analytics = json.loads(analytics_path.read_text())

    return {
        "brand_guidelines": brand_guidelines,
        "past_posts": past_posts,
        "analytics": analytics,
    }


def get_past_posts(platform: str, limit: int = 10) -> list:
    """Return the most recent posts for a given platform."""
    past_posts_path = MEMORY_DIR / "past_posts.json"
    if not past_posts_path.exists():
        return []
    data = json.loads(past_posts_path.read_text())
    posts = data.get(platform, [])
    return posts[-limit:]


def save_post(platform: str, post_data: dict) -> None:
    """Append a published post to past_posts.json."""
    past_posts_path = MEMORY_DIR / "past_posts.json"
    data = {}
    if past_posts_path.exists():
        data = json.loads(past_posts_path.read_text())

    if platform not in data:
        data[platform] = []
    data[platform].append(post_data)

    # Keep only last 30 per platform
    data[platform] = data[platform][-30:]
    past_posts_path.write_text(json.dumps(data, indent=2))


def update_analytics(platform: str, post_id: str, metrics: dict) -> None:
    """Update analytics.json with engagement data for a post."""
    analytics_path = MEMORY_DIR / "analytics.json"
    data = {}
    if analytics_path.exists():
        data = json.loads(analytics_path.read_text())

    if "post_metrics" not in data:
        data["post_metrics"] = []
    data["post_metrics"].append({
        "platform": platform,
        "post_id": post_id,
        **metrics,
    })

    analytics_path.write_text(json.dumps(data, indent=2))
