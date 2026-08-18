"""Content writer agent — generates platform-specific social media copy."""

from __future__ import annotations

import json
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

from tools.brand_memory import get_brand_memory, get_past_posts
from tools.search import search

MODEL = "claude-sonnet-4-5-20250514"

SYSTEM_PROMPT = """You are a social media copywriter for Internwise — the UK and Europe's internship recruitment specialist. Since 2010, Internwise connects global employers with ambitious students and recent graduates.

Your voice is warm, encouraging, and human — like a trusted career mentor. You are never salesy, corporate, or condescending toward young job seekers.

You always:
- Load brand guidelines before writing anything
- Match tone to platform: polished but warm on LinkedIn, visual-first punchy on Instagram, sharp and concise on X, high-energy relatable on TikTok
- Keep copy within platform character limits (LinkedIn: 3000, X: 280, Instagram: 2200, TikTok: 2200)
- Include relevant hashtags per platform rules (LinkedIn: 3-5, Instagram: 5-10, X: 1-2, TikTok: 3-6)
- Always include at least one core brand hashtag (#Internwise, #FindYourInternship, #InternshipLife)
- End with a clear CTA matched to the campaign goal
- Tag output with the content pillar it belongs to (career inspiration, market insights, practical advice, employer spotlight, platform & community)
- Reference current data from the search tool when available — never make up statistics
- Avoid clichés (rockstar, ninja, guru, hustle), excessive exclamation marks, competitor mentions, and overpromising

Return output as structured JSON only."""

CHAR_LIMITS = {
    "linkedin": 3000,
    "x": 280,
    "instagram": 2200,
    "tiktok": 2200,
}

# Tool definitions for the Claude API
TOOLS = [
    {
        "name": "search",
        "description": "Search the web for trending topics, job market data, or statistics. Use this to find real data to cite in posts.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_brand_memory",
        "description": "Load the brand voice, tone guidelines, colors, and content pillars.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_past_posts",
        "description": "Get recent published posts for a platform to avoid repeating content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "The social platform (linkedin, instagram, x, tiktok).",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of recent posts to retrieve (default 10).",
                },
            },
            "required": ["platform"],
        },
    },
]


def _handle_tool_call(tool_name: str, tool_input: dict) -> str:
    """Execute a tool call and return the result as a string."""
    if tool_name == "search":
        result = search(tool_input["query"])
    elif tool_name == "get_brand_memory":
        result = get_brand_memory()
    elif tool_name == "get_past_posts":
        result = get_past_posts(tool_input["platform"], tool_input.get("limit", 10))
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    return json.dumps(result, default=str)


def generate_copy(
    platform: str,
    topic: str,
    audience: str,
    goal: str,
    tone_override: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Generate social media copy for a given platform and topic.

    Args:
        platform: Target platform (linkedin, instagram, x, tiktok).
        topic: Campaign topic / brief.
        audience: Target audience description.
        goal: Campaign goal (awareness, engagement, conversion).
        tone_override: Optional tone override.
        dry_run: If True, return mock output without API calls.

    Returns:
        Dict with platform, copy, hashtags, cta, char_count, tone.
    """
    if dry_run:
        return _mock_copy(platform, topic, goal)

    client = anthropic.Anthropic()

    user_message = f"""Create a social media post for {platform}.

Topic: {topic}
Target audience: {audience}
Campaign goal: {goal}
Character limit: {CHAR_LIMITS.get(platform, 2200)}
{"Tone: " + tone_override if tone_override else "Use default brand tone for this platform."}

First, load brand guidelines and check past posts to avoid repetition.
Then search for any relevant current data or trends to reference.
Finally, write the post and return it as JSON with these fields:
- platform
- copy
- hashtags (array)
- cta
- char_count
- tone"""

    messages = [{"role": "user", "content": user_message}]

    # Agentic loop — let the model call tools until it produces a final response
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        # Collect all tool uses and text blocks
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        text_blocks = [b for b in response.content if b.type == "text"]

        if response.stop_reason == "end_turn" or not tool_uses:
            # Final response — extract JSON from text
            full_text = "\n".join(b.text for b in text_blocks)
            return _parse_json_output(full_text, platform)

        # Process tool calls
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tool_use in tool_uses:
            result = _handle_tool_call(tool_use.name, tool_use.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result,
            })
        messages.append({"role": "user", "content": tool_results})


def _parse_json_output(text: str, platform: str) -> dict:
    """Extract JSON from the model's text response."""
    # Try to find JSON in the response
    try:
        # Look for JSON block
        if "```json" in text:
            json_str = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            json_str = text.split("```")[1].split("```")[0].strip()
        elif "{" in text:
            start = text.index("{")
            end = text.rindex("}") + 1
            json_str = text[start:end]
        else:
            json_str = text

        result = json.loads(json_str)
        # Enforce character limit
        char_limit = CHAR_LIMITS.get(platform, 2200)
        if len(result.get("copy", "")) > char_limit:
            result["copy"] = result["copy"][:char_limit]
            result["char_count"] = char_limit
            result["truncated"] = True
        return result
    except (json.JSONDecodeError, ValueError):
        return {
            "platform": platform,
            "copy": text,
            "hashtags": [],
            "cta": "",
            "char_count": len(text),
            "tone": "unknown",
            "parse_error": True,
        }


def _mock_copy(platform: str, topic: str, goal: str) -> dict:
    """Return mock output for dry-run testing."""
    return {
        "platform": platform,
        "copy": f"[MOCK] {topic} — Check out the latest opportunities on our job board!",
        "hashtags": ["#Jobs", "#Hiring", "#CareerGrowth"],
        "cta": "Visit our job board to explore roles →" if goal == "conversion" else "What do you think? Drop a comment below!",
        "char_count": 80,
        "tone": "professional" if platform == "linkedin" else "casual",
        "mock": True,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Content Writer Agent")
    parser.add_argument("--platform", required=True, choices=["linkedin", "instagram", "x", "tiktok"])
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", default="job seekers and professionals, 25-45")
    parser.add_argument("--goal", default="awareness", choices=["awareness", "engagement", "conversion"])
    parser.add_argument("--tone", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = generate_copy(
        platform=args.platform,
        topic=args.topic,
        audience=args.audience,
        goal=args.goal,
        tone_override=args.tone,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2))
