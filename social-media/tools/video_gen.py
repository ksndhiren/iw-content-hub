"""Video generation and assembly wrapper."""

from __future__ import annotations

import os
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

VIDEO_SPECS = {
    "tiktok": {"aspect_ratio": "9:16", "max_length": 180, "format": "mp4"},
    "instagram_reel": {"aspect_ratio": "9:16", "max_length": 90, "format": "mp4"},
    "linkedin_video": {"aspect_ratio": "16:9", "max_length": 600, "format": "mp4"},
}


def generate_video(prompt: str, duration: int = 5, output_path: str | None = None) -> dict:
    """Generate a short video clip from a text prompt.

    Args:
        prompt: Video generation prompt.
        duration: Desired duration in seconds.
        output_path: Path to save the video file.

    Returns:
        Dict with video_url, duration, and local_path.
    """
    if not RUNWAY_API_KEY:
        return _mock_video(prompt, duration, output_path)

    # RunwayML Gen-3 API call (placeholder — adapt to actual SDK)
    import requests
    url = "https://api.runwayml.com/v1/generate"
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": prompt,
        "duration": duration,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    video_url = resp.json().get("video_url", "")

    local_path = None
    if output_path and video_url:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        dl = requests.get(video_url, timeout=60)
        Path(output_path).write_bytes(dl.content)
        local_path = output_path

    return {"video_url": video_url, "duration": duration, "local_path": local_path}


def assemble_video(
    voiceover_path: str,
    video_path: str,
    captions_srt: str | None = None,
    output_path: str = "output.mp4",
) -> dict:
    """Assemble a final video from voiceover audio and video clip.

    Uses ffmpeg to combine audio + video and optionally burn in subtitles.

    Args:
        voiceover_path: Path to the voiceover audio file.
        video_path: Path to the video clip.
        captions_srt: Optional SRT subtitle content to burn in.
        output_path: Path for the final assembled video.

    Returns:
        Dict with output_path and success status.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Write SRT file if captions provided
    srt_path = None
    if captions_srt:
        srt_path = output_path.replace(".mp4", ".srt")
        Path(srt_path).write_text(captions_srt)

    # Build ffmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", voiceover_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
    ]

    if srt_path:
        cmd.extend(["-vf", f"subtitles={srt_path}"])

    cmd.append(output_path)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        success = result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        success = False

    return {"output_path": output_path, "success": success, "srt_path": srt_path}


def _mock_video(prompt: str, duration: int, output_path: str | None) -> dict:
    """Return mock result for dry-run / testing."""
    return {
        "video_url": "https://example.com/mock-video.mp4",
        "duration": duration,
        "local_path": output_path,
        "mock": True,
        "prompt_used": prompt,
    }
