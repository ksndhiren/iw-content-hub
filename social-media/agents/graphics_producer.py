"""Graphics producer agent — generates images and visual assets for social media."""

from __future__ import annotations

import json
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

from tools.brand_memory import get_brand_memory
from tools.image_gen import generate_image

MODEL = "claude-sonnet-4-5-20250514"

SYSTEM_PROMPT = """You are a graphic design agent for Internwise — the UK and Europe's internship recruitment specialist.
Given a content brief, you generate images and visual assets for social media.
You always:
- Load brand guidelines from memory before generating — use the exact Internwise colour palette (navy #1A1A2E, coral-red #E94560, light grey #F5F5F5, white)
- Use Inter for headings and DM Sans for body text — never more than two fonts per asset
- Write detailed image generation prompts that match brand aesthetics: clean, professional, modern, diverse global talent in genuine work settings
- Avoid generic stock photo energy — prefer candid working moments, collaborative scenes, London/city backdrops
- Select the correct template type for the content goal
- Enforce correct dimensions per platform
- Ensure the IW logo is top-left or centred with 40px clear space on approved backgrounds only (white, navy, coral)
- Never use competitor logos or copyrighted visual styles
- Return structured metadata alongside each generated asset

Return output as structured JSON with asset paths and metadata."""

PLATFORM_DIMENSIONS = {
    "linkedin": {"format": "banner", "size": "1200x627"},
    "instagram": {"format": "square", "size": "1080x1080"},
    "instagram_story": {"format": "story", "size": "1080x1920"},
    "x": {"format": "card", "size": "1200x675"},
    "tiktok": {"format": "vertical", "size": "1080x1920"},
}

TEMPLATE_TYPES = ["stat_card", "job_spotlight", "employer_spotlight", "tip_card", "carousel"]

TOOLS = [
    {
        "name": "generate_image",
        "description": "Generate an image from a text prompt using DALL-E 3 or Stable Diffusion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed image generation prompt.",
                },
                "size": {
                    "type": "string",
                    "description": "Image dimensions (e.g. '1024x1024').",
                },
            },
            "required": ["prompt", "size"],
        },
    },
    {
        "name": "get_brand_memory",
        "description": "Load the brand color palette, font rules, logo guidelines, and visual style.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def _handle_tool_call(tool_name: str, tool_input: dict, output_dir: str) -> str:
    """Execute a tool call and return the result as a string."""
    if tool_name == "generate_image":
        output_path = os.path.join(output_dir, "generated_image.png")
        result = generate_image(
            prompt=tool_input["prompt"],
            size=tool_input.get("size", "1024x1024"),
            output_path=output_path,
        )
    elif tool_name == "get_brand_memory":
        result = get_brand_memory()
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    return json.dumps(result, default=str)


def generate_graphics(
    platform: str,
    topic: str,
    goal: str,
    template_type: str = "stat_card",
    copy_text: str = "",
    output_dir: str = ".",
    dry_run: bool = False,
) -> dict:
    """Generate a graphic asset for a social media post.

    Args:
        platform: Target platform.
        topic: Campaign topic.
        goal: Campaign goal.
        template_type: Type of template (stat_card, job_spotlight, etc.).
        copy_text: Post copy to reference for visual alignment.
        output_dir: Directory to save generated assets.
        dry_run: If True, return mock output.

    Returns:
        Dict with platform, template, image_url, dimensions, alt_text, brand_compliant.
    """
    if dry_run:
        return _mock_graphics(platform, template_type)

    dims = PLATFORM_DIMENSIONS.get(platform, PLATFORM_DIMENSIONS["instagram"])
    client = anthropic.Anthropic()

    user_message = f"""Create a social media graphic for {platform}.

Topic: {topic}
Template type: {template_type}
Platform dimensions: {dims['size']} ({dims['format']})
Campaign goal: {goal}
Post copy for reference: {copy_text}

Steps:
1. Load brand guidelines to get colors, fonts, and style rules
2. Write a detailed image generation prompt that matches our brand aesthetic
3. Generate the image
4. Return structured JSON with: platform, template, image_url, dimensions, alt_text, brand_compliant"""

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
            return _parse_json_output(full_text, platform, template_type, dims["size"])

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


def _parse_json_output(text: str, platform: str, template: str, dimensions: str) -> dict:
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
            "template": template,
            "image_url": None,
            "dimensions": dimensions,
            "alt_text": text[:200] if text else "",
            "brand_compliant": False,
            "parse_error": True,
        }


def _mock_graphics(platform: str, template_type: str) -> dict:
    """Return mock output for dry-run testing."""
    dims = PLATFORM_DIMENSIONS.get(platform, PLATFORM_DIMENSIONS["instagram"])
    return {
        "platform": platform,
        "template": template_type,
        "image_url": "https://example.com/mock-graphic.png",
        "dimensions": dims["size"],
        "alt_text": f"[MOCK] {template_type} graphic for {platform}",
        "brand_compliant": True,
        "mock": True,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Graphics Producer Agent")
    parser.add_argument("--platform", required=True, choices=["linkedin", "instagram", "instagram_story", "x", "tiktok"])
    parser.add_argument("--topic", required=True)
    parser.add_argument("--goal", default="awareness")
    parser.add_argument("--template", default="stat_card", choices=TEMPLATE_TYPES)
    parser.add_argument("--copy", default="")
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = generate_graphics(
        platform=args.platform,
        topic=args.topic,
        goal=args.goal,
        template_type=args.template,
        copy_text=args.copy,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2))
