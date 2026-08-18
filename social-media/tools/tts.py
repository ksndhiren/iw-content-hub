"""Text-to-speech wrapper using ElevenLabs API."""

from __future__ import annotations

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Default voice IDs (can be overridden via brand memory)
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs "Rachel" voice


def generate_voiceover(
    script: str,
    voice_id: str | None = None,
    output_path: str | None = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> dict:
    """Generate voiceover audio from a script.

    Args:
        script: The text to convert to speech.
        voice_id: ElevenLabs voice ID (defaults to brand voice).
        output_path: Path to save the audio file.
        stability: Voice stability setting (0-1).
        similarity_boost: Voice similarity setting (0-1).

    Returns:
        Dict with audio_url and local_path.
    """
    voice_id = voice_id or DEFAULT_VOICE_ID

    if not ELEVENLABS_API_KEY:
        return _mock_voiceover(script, output_path)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": script,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()

    local_path = None
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(resp.content)
        local_path = output_path

    return {"audio_url": None, "local_path": local_path}


def _mock_voiceover(script: str, output_path: str | None) -> dict:
    """Return mock result for dry-run / testing."""
    return {
        "audio_url": "https://example.com/mock-voiceover.mp3",
        "local_path": output_path,
        "mock": True,
        "script_length": len(script),
    }
