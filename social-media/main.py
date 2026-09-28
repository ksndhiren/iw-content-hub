"""Higgsfield Seedance 2.5 text-to-video example.

Generates a short video with bytedance/seedance-2.5/text-to-video and prints
the resulting video URL.

Usage:
    python main.py

Requires HF_KEY (format "key-id:key-secret") in .env.local.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

# Load credentials before importing the SDK so it picks up HF_KEY from the env.
load_dotenv(Path(__file__).with_name(".env.local"))

import higgsfield_client  # noqa: E402
from higgsfield_client import (  # noqa: E402
    Cancelled,
    Completed,
    CredentialsMissedError,
    Failed,
    HiggsfieldClientError,
    NSFW,
    Status,
)

MODEL = "bytedance/seedance-2.5/text-to-video"

ARGUMENTS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}

# subscribe() returns the final payload whatever the outcome, so we record the
# terminal status ourselves and refuse to report success unless it is Completed.
TERMINAL_MESSAGES = {
    Failed: "generation failed",
    Cancelled: "generation was canceled",
    NSFW: "generation was blocked by content moderation",
}


def extract_video_url(result):
    """Pull the video URL out of the completed-request payload."""
    video = result.get("video") if isinstance(result, dict) else None

    if isinstance(video, dict):
        return video.get("url")
    if isinstance(video, str):
        return video
    return None


def main() -> int:
    last_status = {"value": None}

    def on_enqueue(request_id: str) -> None:
        print(f"Request enqueued: {request_id}")

    def on_queue_update(status: Status) -> None:
        last_status["value"] = status
        print(f"Status: {type(status).__name__}")

    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGUMENTS,
            on_enqueue=on_enqueue,
            on_queue_update=on_queue_update,
        )
    except CredentialsMissedError as exc:
        print(f"Credentials error: {exc}", file=sys.stderr)
        print("Set HF_KEY in .env.local as key-id:key-secret.", file=sys.stderr)
        return 2
    except HiggsfieldClientError as exc:
        print(f"Higgsfield API error: {exc}", file=sys.stderr)
        return 1

    status = last_status["value"]

    for status_type, message in TERMINAL_MESSAGES.items():
        if isinstance(status, status_type):
            print(f"Request did not succeed - {message}.", file=sys.stderr)
            print(f"Response: {result}", file=sys.stderr)
            return 1

    if not isinstance(status, Completed):
        print(f"Request ended in an unexpected state: {status!r}", file=sys.stderr)
        return 1

    video_url = extract_video_url(result)

    if not video_url:
        print("Request completed but no video URL was returned.", file=sys.stderr)
        print(f"Response: {result}", file=sys.stderr)
        return 1

    print(f"Video URL: {video_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
