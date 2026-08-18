"""
Internwise — Modern Graphics Generator (2026 aesthetics)
Uses HTML/CSS + Playwright headless browser for rendering.
Supports: glassmorphism, mesh gradients, modern typography, proper layering.
"""

import os
import base64
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

PLATFORM_SIZES = {
    "instagram":       (1080, 1080),
    "instagram_story": (1080, 1920),
    "linkedin":        (1200, 627),
    "x":               (1200, 675),
    "tiktok":          (1080, 1920),
}


def _load_font_base64(font_name):
    """Load a font file as base64 for CSS embedding."""
    path = os.path.join(FONTS_DIR, font_name)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _load_logo_base64():
    """Load the white horizontal logo SVG as base64."""
    logo_path = os.path.join(BRANDING_DIR, "SVG", "IW.Com-Horizontal-White Logo.svg")
    if not os.path.exists(logo_path):
        return None
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _build_font_faces():
    """Build @font-face CSS rules with embedded fonts."""
    fonts = {
        "Inter": [
            ("Inter-Bold.ttf", 700),
            ("Inter-SemiBold.ttf", 600),
            ("Inter-Medium.ttf", 500),
            ("Inter-Regular.ttf", 400),
        ],
        "DM Sans": [
            ("DMSans-Bold.ttf", 700),
            ("DMSans-Medium.ttf", 500),
            ("DMSans-Regular.ttf", 400),
        ],
    }
    css = ""
    for family, variants in fonts.items():
        for filename, weight in variants:
            b64 = _load_font_base64(filename)
            if b64:
                css += f"""
@font-face {{
    font-family: '{family}';
    src: url(data:font/truetype;base64,{b64}) format('truetype');
    font-weight: {weight};
    font-style: normal;
}}"""
    return css


def generate_tip_card_html(platform, tag_text, title, subtitle, steps, cta_text):
    """Generate modern tip card HTML with glassmorphism and mesh gradients."""
    width, height = PLATFORM_SIZES[platform]
    logo_b64 = _load_logo_base64()
    font_faces = _build_font_faces()

    logo_img = ""
    if logo_b64:
        logo_img = f'<img src="data:image/svg+xml;base64,{logo_b64}" class="logo" alt="Internwise">'

    steps_html = ""
    for i, step in enumerate(steps):
        is_last = i == len(steps) - 1
        connector = "" if is_last else '<div class="connector"></div>'
        steps_html += f"""
        <div class="step">
            <div class="step-left">
                <div class="step-number">{i + 1}</div>
                {connector}
            </div>
            <div class="step-content">
                <div class="step-title">{step['title']}</div>
                <div class="step-desc">{step['description']}</div>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{font_faces}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    font-family: 'DM Sans', 'Inter', sans-serif;
}}

.canvas {{
    width: {width}px;
    height: {height}px;
    position: relative;
    background: linear-gradient(160deg, #0a0a18 0%, #131328 20%, #1A1A2E 40%, #1a1535 60%, #16213E 80%, #0d0d1a 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* ── Mesh gradient orbs ── */
.orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(90px);
    z-index: 0;
}}
.orb-1 {{
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(233, 69, 96, 0.7) 0%, rgba(233, 69, 96, 0.15) 45%, transparent 70%);
    top: -250px;
    right: -200px;
    opacity: 0.8;
    filter: blur(100px);
}}
.orb-2 {{
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(79, 70, 229, 0.55) 0%, rgba(99, 102, 241, 0.12) 45%, transparent 70%);
    bottom: -200px;
    left: -180px;
    opacity: 0.75;
    filter: blur(100px);
}}
.orb-3 {{
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(236, 72, 153, 0.35) 0%, transparent 55%);
    top: 55%;
    right: -80px;
    opacity: 0.6;
    filter: blur(80px);
}}
.orb-4 {{
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(14, 165, 233, 0.25) 0%, transparent 55%);
    top: 25%;
    left: -80px;
    opacity: 0.5;
    filter: blur(80px);
}}

/* ── Subtle grid pattern overlay ── */
.grid-overlay {{
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 60px 60px;
    z-index: 1;
}}

/* ── Content wrapper ── */
.content {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    padding: 0 {int(width * 0.07)}px;
    gap: 0;
}}

/* ── Tag badge ── */
.tag {{
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: {int(width * 0.015)}px;
    letter-spacing: 3px;
    color: #E94560;
    background: rgba(233, 69, 96, 0.12);
    border: 1px solid rgba(233, 69, 96, 0.3);
    padding: 10px 28px;
    border-radius: 50px;
    text-transform: uppercase;
    margin-bottom: {int(height * 0.03)}px;
}}

/* ── Main title ── */
.title {{
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: {int(width * 0.058)}px;
    color: #FFFFFF;
    text-align: center;
    line-height: 1.15;
    margin-bottom: {int(height * 0.012)}px;
    max-width: 90%;
    text-shadow: 0 0 40px rgba(233, 69, 96, 0.15);
}}

/* ── Subtitle ── */
.subtitle {{
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: {int(width * 0.022)}px;
    color: rgba(255, 255, 255, 0.5);
    text-align: center;
    margin-bottom: {int(height * 0.04)}px;
    letter-spacing: 0.5px;
}}

/* ── Glass card container ── */
.glass-card {{
    width: 88%;
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    padding: {int(height * 0.04)}px {int(width * 0.05)}px;
    display: flex;
    flex-direction: column;
    gap: {int(height * 0.028)}px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.05);
}}

/* ── Step rows ── */
.step {{
    display: flex;
    align-items: flex-start;
    gap: {int(width * 0.025)}px;
}}

.step + .step {{
    padding-top: {int(height * 0.005)}px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}}

.step-left {{
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
    width: 48px;
}}

.step-number {{
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #E94560 0%, #c23152 100%);
    color: white;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 20px rgba(233, 69, 96, 0.35);
    flex-shrink: 0;
}}

.connector {{
    width: 2px;
    height: {int(height * 0.035)}px;
    background: linear-gradient(180deg, rgba(233, 69, 96, 0.4) 0%, rgba(233, 69, 96, 0.05) 100%);
    margin-top: 8px;
}}

.step-content {{
    padding-top: 2px;
    flex: 1;
}}

.step-title {{
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: {int(width * 0.026)}px;
    color: #FFFFFF;
    margin-bottom: 8px;
    letter-spacing: 0.3px;
}}

.step-desc {{
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
    font-size: {int(width * 0.019)}px;
    color: rgba(255, 255, 255, 0.65);
    line-height: 1.55;
}}

/* ── CTA ── */
.cta {{
    margin-top: {int(height * 0.035)}px;
    background: linear-gradient(135deg, #E94560 0%, #d63851 50%, #c23152 100%);
    color: white;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: {int(width * 0.019)}px;
    padding: 16px 40px;
    border-radius: 50px;
    text-align: center;
    letter-spacing: 0.5px;
    box-shadow: 0 8px 32px rgba(233, 69, 96, 0.3);
}}

/* ── Footer with logo ── */
.footer {{
    position: absolute;
    bottom: {int(height * 0.035)}px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
}}

.logo {{
    height: {int(height * 0.038)}px;
    opacity: 0.8;
    filter: brightness(1);
}}

/* ── Decorative corner accent ── */
.corner-accent {{
    position: absolute;
    top: -2px;
    right: -2px;
    width: 200px;
    height: 200px;
    border-radius: 0 0 0 200px;
    background: linear-gradient(225deg, rgba(233, 69, 96, 0.15) 0%, transparent 60%);
    z-index: 2;
}}

.corner-accent-bl {{
    position: absolute;
    bottom: -2px;
    left: -2px;
    width: 150px;
    height: 150px;
    border-radius: 0 150px 0 0;
    background: linear-gradient(45deg, rgba(99, 102, 241, 0.1) 0%, transparent 60%);
    z-index: 2;
}}

/* ── Thin top accent line ── */
.top-line {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, #E94560 50%, transparent 100%);
    z-index: 20;
}}
</style>
</head>
<body>
<div class="canvas">
    <!-- Decorative layers -->
    <div class="top-line"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
    <div class="grid-overlay"></div>
    <div class="corner-accent"></div>
    <div class="corner-accent-bl"></div>

    <!-- Main content -->
    <div class="content">
        <div class="tag">{tag_text}</div>
        <div class="title">{title}</div>
        <div class="subtitle">{subtitle}</div>

        <div class="glass-card">
            {steps_html}
        </div>

        <div class="cta">{cta_text}</div>
    </div>

    <!-- Footer logo -->
    <div class="footer">
        {logo_img}
    </div>
</div>
</body>
</html>"""
    return html


def render_html_to_png(html, output_path, width, height):
    """Render HTML string to PNG using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()
    print(f"  ✓ Rendered: {output_path} ({width}×{height} @2x)")


def generate_modern_tip_card(platform, tag_text, title, subtitle, steps,
                              cta_text, campaign_id):
    """Generate a modern tip card graphic for the given platform."""
    width, height = PLATFORM_SIZES[platform]

    html = generate_tip_card_html(
        platform=platform,
        tag_text=tag_text,
        title=title,
        subtitle=subtitle,
        steps=steps,
        cta_text=cta_text,
    )

    output_dir = os.path.join(OUTPUT_DIR, campaign_id)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"graphic_{platform}_v3.png")

    render_html_to_png(html, output_path, width, height)
    return output_path


if __name__ == "__main__":
    CAMPAIGN_ID = "candidate-tmay-magic-formula"

    steps = [
        {
            "title": "Present",
            "description": "Start with who you are right now — your degree, your current focus, and what drives you."
        },
        {
            "title": "Past",
            "description": "Share the experience that led you here — a project, internship, or skill you built along the way."
        },
        {
            "title": "Future",
            "description": "Connect it to this role. Why this company? Why now? Show them you've done your homework."
        }
    ]

    print("\n🎨 Modern Graphics Generator — Internwise")
    print("=" * 50)

    path = generate_modern_tip_card(
        platform="instagram",
        tag_text="Interview Tip",
        title='"Tell me about yourself"',
        subtitle="The magic formula to nail your answer every time",
        steps=steps,
        cta_text="Find your next internship → internwise.com",
        campaign_id=CAMPAIGN_ID,
    )

    print(f"\n✅ Done: {path}")
