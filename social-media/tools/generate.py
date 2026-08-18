"""
Internwise — Brief-driven carousel generator
Uses Claude API to generate slide HTML from a JSON brief, then renders with Playwright.

Usage:
  python3 tools/generate.py briefs/week3-d2-cv.json
  python3 tools/generate.py briefs/week3-d2-cv.json --dry-run
  python3 tools/generate.py briefs/week3-d2-cv.json --slides 1,3,5   # regenerate specific slides only
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Paths — defined before load_dotenv so we can pass the .env location
BASE_DIR     = Path(__file__).parent.parent
BRANDING_DIR = BASE_DIR / "branding"
FONTS_DIR    = BASE_DIR / "assets" / "fonts"
OUTPUT_DIR   = BASE_DIR / "campaigns" / "outputs"

# Load .env from project root — override=True ensures .env wins over
# any empty env vars set by the parent process (e.g. Claude Code shell)
load_dotenv(BASE_DIR / ".env", override=True)

# Ensure tools/ is on the path (needed for brand_context import inside generate_slide_html)
sys.path.insert(0, str(Path(__file__).parent))


# ── Asset helpers ────────────────────────────────────────────────────────────

def _b64(path):
    p = Path(path)
    return base64.b64encode(p.read_bytes()).decode() if p.exists() else None


def _build_fonts_css() -> str:
    """Build base64 @font-face declarations for Inter and DM Sans."""
    fonts = {
        "Inter":   [("Inter-Bold.ttf", 700), ("Inter-SemiBold.ttf", 600),
                    ("Inter-Medium.ttf", 500), ("Inter-Regular.ttf", 400)],
        "DM Sans": [("DMSans-Bold.ttf", 700), ("DMSans-Medium.ttf", 500),
                    ("DMSans-Regular.ttf", 400)],
    }
    css = ""
    for family, variants in fonts.items():
        for fn, weight in variants:
            b64 = _b64(FONTS_DIR / fn)
            if b64:
                css += (
                    f"@font-face{{font-family:'{family}';"
                    f"src:url(data:font/truetype;base64,{b64}) format('truetype');"
                    f"font-weight:{weight};}}"
                )
    return css


def _logo_src() -> str:
    b64 = _b64(BRANDING_DIR / "PNG" / "IW.com_Horizontal_white logo.png")
    return f"data:image/png;base64,{b64}" if b64 else ""


# ── Rendering ────────────────────────────────────────────────────────────────

def render_html(html: str, output_path: str):
    """Render an HTML string to a 1080x1080 PNG via Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1080, "height": 1080},
            device_scale_factor=2,
        )
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()
    print(f"    ✓ saved → {Path(output_path).name}")


# ── Claude API call ───────────────────────────────────────────────────────────

def generate_slide_html(
    slide: dict,
    fonts_css: str,
    logo_src: str,
) -> str:
    """
    Call Claude API with the brand system prompt + slide spec.
    Returns a complete, renderable HTML string.
    """
    from anthropic import Anthropic
    from brand_context import BRAND_SYSTEM_PROMPT, slide_prompt

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Inject fonts into system prompt (keeps user prompt small)
    system = BRAND_SYSTEM_PROMPT.replace("{{FONTS_CSS}}", fonts_css)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=system,
        messages=[{"role": "user", "content": slide_prompt(slide)}],
    )

    html = response.content[0].text.strip()

    # Strip code fences if Claude wrapped output despite instructions
    if html.startswith("```"):
        html = html.split("\n", 1)[1]
        if "```" in html:
            html = html.rsplit("```", 1)[0]
        html = html.strip()

    # Inject logo data URI — Claude leaves the {{LOGO_SRC}} placeholder
    html = html.replace("{{LOGO_SRC}}", logo_src)

    return html


# ── Main ─────────────────────────────────────────────────────────────────────

def generate(brief_path: str, dry_run: bool = False, only_slides=None):
    brief       = json.loads(Path(brief_path).read_text())
    campaign_id = brief["campaign_id"]
    out_dir     = OUTPUT_DIR / brief["output_dir"]
    slides      = brief["slides"]

    print(f"\n🎨  {campaign_id}  ({len(slides)} slides)")
    print(f"    Output: {out_dir}\n")

    if dry_run:
        for i, s in enumerate(slides, 1):
            skip = " [SKIP]" if (only_slides and i not in only_slides) else ""
            print(f"  slide {i:02d}  type={s['type']:12s}  badge={s.get('badge','—')}{skip}")
        print("\n[dry-run] No API calls made.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    fonts_css = _build_fonts_css()
    logo_src  = _logo_src()

    generated = []
    for i, slide in enumerate(slides, 1):
        if only_slides and i not in only_slides:
            continue

        output_path = str(out_dir / f"slide_{i}.png")
        print(f"  [{i}/{len(slides)}] {slide['type']}...", end=" ", flush=True)

        html = generate_slide_html(slide, fonts_css, logo_src)
        render_html(html, output_path)
        generated.append(i)

    print(f"\n✓  Done — {len(generated)} slide(s) → {out_dir}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Generate an Internwise carousel from a JSON brief."
    )
    ap.add_argument("brief", help="Path to brief JSON (e.g. briefs/week3-d2-cv.json)")
    ap.add_argument(
        "--dry-run", action="store_true",
        help="Print the slide plan without calling the API",
    )
    ap.add_argument(
        "--slides", type=str, default=None,
        help="Comma-separated slide numbers to (re)generate, e.g. --slides 1,3",
    )
    args = ap.parse_args()

    only = [int(n.strip()) for n in args.slides.split(",")] if args.slides else None
    generate(args.brief, dry_run=args.dry_run, only_slides=only)
