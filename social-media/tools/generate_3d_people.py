"""
Generate 3D character illustrations using DALL-E 3 for the Networking carousel.
Downloads PNGs to assets/3d-people/ for use in slide designs.
"""

import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "3d-people")
os.makedirs(OUTPUT_DIR, exist_ok=True)

STYLE_PREFIX = (
    "3D rendered cartoon illustration, Pixar/Clay style, "
    "smooth rounded shapes, soft lighting, pastel colors, "
    "transparent background (plain white background), "
    "full body character, high quality, clean render, "
    "no text, no watermark. "
)

ILLUSTRATIONS = [
    {
        "name": "two_people_chatting",
        "prompt": (
            STYLE_PREFIX +
            "Two young diverse professionals having a friendly conversation. "
            "One is a woman with long dark hair wearing a coral/orange top, "
            "the other is a man with short dark hair wearing a navy blue blazer. "
            "They are facing each other, smiling, with speech bubble icons floating between them. "
            "Warm and approachable corporate style."
        ),
    },
    {
        "name": "three_people_group",
        "prompt": (
            STYLE_PREFIX +
            "Three diverse young people standing together in a friendly group. "
            "One is a Black woman with curly hair in a teal top, "
            "one is a white man with brown hair in a light blue shirt, "
            "one is a woman wearing a yellow/amber hijab. "
            "They are smiling and look approachable. Professional but casual."
        ),
    },
    {
        "name": "person_sharing_likes",
        "prompt": (
            STYLE_PREFIX +
            "Two young professionals, one is giving a thumbs up and sharing/liking content. "
            "A man in a navy suit is sharing a heart icon toward a woman in a teal top. "
            "Social media reaction icons (heart, thumbs up, comment bubble) floating between them. "
            "Warm, supportive interaction."
        ),
    },
    {
        "name": "person_sending_message",
        "prompt": (
            STYLE_PREFIX +
            "A young woman wearing an amber/yellow hijab, sitting and holding a smartphone, "
            "typing a message. A large chat bubble floats next to her showing a friendly message. "
            "She looks confident and proactive. Professional setting."
        ),
    },
    {
        "name": "diverse_group_connected",
        "prompt": (
            STYLE_PREFIX +
            "Five diverse young professionals standing together in a semicircle, connected by glowing lines. "
            "Different ethnicities, hair styles, and clothing colors (coral, navy, teal, blue, amber). "
            "They look happy, connected, and collaborative. Networking/community concept."
        ),
    },
]


def generate_illustration(name, prompt):
    """Generate a single illustration using DALL-E 3."""
    print(f"  Generating: {name}...")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1,
    )

    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt
    print(f"  Revised prompt: {revised_prompt[:100]}...")

    # Download the image
    img_response = requests.get(image_url)
    output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    with open(output_path, "wb") as f:
        f.write(img_response.content)

    print(f"  ✓ Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    print("\n🎨 Generating 3D Character Illustrations (DALL-E 3)")
    print("=" * 55)

    for illust in ILLUSTRATIONS:
        try:
            generate_illustration(illust["name"], illust["prompt"])
        except Exception as e:
            print(f"  ✗ Error generating {illust['name']}: {e}")

    print("\n✅ All illustrations generated!")
    print(f"   Output: {OUTPUT_DIR}")
