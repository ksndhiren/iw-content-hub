"""Audio/video producer agent — creates short-form video content."""

from __future__ import annotations

import json
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

from tools.brand_memory import get_brand_memory
from tools.tts import generate_voiceover
from tools.video_gen import generate_video, assemble_video

MODEL = "claude-sonnet-4-5-20250514"

SYSTEM_PROMPT = """You are a short-form video producer for Internwise — the UK and Europe's internship recruitment specialist.
You create engaging 15-60 second videos for TikTok, Instagram Reels, and LinkedIn Video.
You always:
- Open with a strong hook in the first 2-3 seconds (especially TikTok — highest energy)
- Keep scripts punchy: one idea per sentence, short sentences
- Match energy to platform: high-energy relatable on TikTok, aspirational on Instagram Reels, polished and warm on LinkedIn
- Write in the Internwise voice — encouraging, human, like a career mentor talking to a friend
- Never be condescending toward young job seekers or use clichés (rockstar, ninja, guru)
- Include on-screen text/captions for silent viewing using brand colours (navy #1A1A2E, coral #E94560)
- Use Inter font for on-screen text
- End with a verbal and on-screen CTA directing to internwise.com
- Keep total video under 60 seconds (TikTok/Reels) or under 3 minutes (LinkedIn)
- Educational content works best: "5 things no one tells you about internships" style

Return the script, voiceover cues, and assembly instructions as structured JSON."""

VIDEO_SPECS = {
    "tiktok": {"aspect_ratio": "9:16", "max_length": 180, "format": "mp4"},
    "instagram_reel": {"aspect_ratio": "9:16", "max_length": 90, "format": "mp4"},
    "linkedin_video": {"aspect_ratio": "16:9", "max_length": 600, "format": "mp4"},
}

TOOLS = [
    {
        "name": "generate_voiceover",
        "description": "Generate voiceover audio from a script using ElevenLabs TTS.",
        "input_schema": {
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "The voiceover script text.",
                },
                "voice_id": {
                    "type": "string",
                    "description": "ElevenLabs voice ID (optional, uses brand default).",
                },
            },
            "required": ["script"],
        },
    },
    {
        "name": "generate_video",
        "description": "Generate a short video clip from a text prompt.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Video generation prompt.",
                },
                "duration": {
                    "type": "integer",
                    "description": "Desired duration in seconds.",
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "get_brand_memory",
        "description": "Load approved voice IDs, music tracks, and brand guidelines.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def _handle_tool_call(tool_name: str, tool_input: dict, output_dir: str) -> str:
    """Execute a tool call and return the result as a string."""
    if tool_name == "generate_voiceover":
        output_path = os.path.join(output_dir, "voiceover.mp3")
        result = generate_voiceover(
            script=tool_input["script"],
            voice_id=tool_input.get("voice_id"),
            output_path=output_path,
        )
    elif tool_name == "generate_video":
        output_path = os.path.join(output_dir, "clip.mp4")
        result = generate_video(
            prompt=tool_input["prompt"],
            duration=tool_input.get("duration", 15),
            output_path=output_path,
        )
    elif tool_name == "get_brand_memory":
        result = get_brand_memory()
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    return json.dumps(result, default=str)


def produce_video(
    platform: str,
    topic: str,
    goal: str,
    copy_text: str = "",
    output_dir: str = ".",
    dry_run: bool = False,
) -> dict:
    """Produce a short-form video for a social media platform.

    Args:
        platform: Target platform (tiktok, instagram_reel, linkedin_video).
        topic: Campaign topic.
        goal: Campaign goal.
        copy_text: Post copy for script alignment.
        output_dir: Directory to save generated assets.
        dry_run: If True, return mock output.

    Returns:
        Dict with platform, script, voiceover_url, video_url, duration, captions_srt, thumbnail_url.
    """
    if dry_run:
        return _mock_video(platform, topic)

    # Map platform names
    spec_key = platform
    if platform == "tiktok":
        spec_key = "tiktok"
    elif platform == "instagram":
        spec_key = "instagram_reel"
    elif platform == "linkedin":
        spec_key = "linkedin_video"

    spec = VIDEO_SPECS.get(spec_key, VIDEO_SPECS["tiktok"])
    client = anthropic.Anthropic()

    user_message = f"""Create a short-form video for {platform}.

Topic: {topic}
Campaign goal: {goal}
Max video length: {spec['max_length']} seconds
Aspect ratio: {spec['aspect_ratio']}
Post copy for reference: {copy_text}

Steps:
1. Load brand guidelines for approved voice and style
2. Write a punchy video script (hook → body → CTA)
3. Generate voiceover audio from the script
4. Generate a video clip to accompany the voiceover
5. Return structured JSON with: platform, script, voiceover_url, video_url, duration_seconds, captions_srt, thumbnail_url"""

    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        text_blocks = [b for b in response.content if b.type == "text"]

        if response.stop_reason == "end_turn" or not tool_uses:
            full_text = "\n".join(b.text for b in text_blocks)
            return _parse_json_output(full_text, platform)

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tool_use in tool_uses:
            result = _handle_tool_call(tool_use.name, tool_use.input, output_dir)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result,
            })
        messages.append({"role": "user", "content": tool_results})


def _parse_json_output(text: str, platform: str) -> dict:
    """Extract JSON from the model's text response."""
    try:
        if "```json" in text:
            json_str = text.split("```json")[1].split("```")[0].strip()
        elif "{" in text:
            start = text.index("{")
            end = text.rindex("}") + 1
            json_str = text[start:end]
        else:
            json_str = text
        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        return {
            "platform": platform,
            "script": text,
            "voiceover_url": None,
            "video_url": None,
            "duration_seconds": 0,
            "captions_srt": None,
            "thumbnail_url": None,
            "parse_error": True,
        }


def _mock_video(platform: str, topic: str) -> dict:
    """Return mock output for dry-run testing."""
    return {
        "platform": platform,
        "script": f"[MOCK] Hook: Did you know? {topic}. Body: Here's what's happening. CTA: Check our job board!",
        "voiceover_url": "https://example.com/mock-voiceover.mp3",
        "video_url": "https://example.com/mock-video.mp4",
        "duration_seconds": 30,
        "captions_srt": "1\n00:00:00,000 --> 00:00:03,000\n[MOCK] Did you know?\n",
        "thumbnail_url": "https://example.com/mock-thumbnail.jpg",
        "mock": True,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AV Producer Agent")
    parser.add_argument("--platform", required=True, choices=["tiktok", "instagram", "linkedin"])
    parser.add_argument("--topic", required=True)
    parser.add_argument("--goal", default="awareness")
    parser.add_argument("--copy", default="")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = produce_video(
        platform=args.platform,
        topic=args.topic,
        goal=args.goal,
        copy_text=args.copy,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2))
