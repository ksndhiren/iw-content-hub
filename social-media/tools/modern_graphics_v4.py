"""
Internwise — Modern Graphics Generator v4
Creative 2026 design with 3D illustration hero, new color palette,
glassmorphism, and dynamic asymmetric layout.
Uses HTML/CSS + Playwright for pixel-perfect rendering.
"""

import os
import base64
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
ILLUSTRATIONS_DIR = os.path.join(BASE_DIR, "assets", "illustrations")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

PLATFORM_SIZES = {
    "instagram":       (1080, 1080),
    "instagram_story": (1080, 1920),
    "linkedin":        (1200, 627),
    "x":               (1200, 675),
    "tiktok":          (1080, 1920),
}

# New brand colors
DEEP_BLUE = "#264D7E"
TEAL = "#5B9291"
MEDIUM_BLUE = "#3E77B1"
LIGHT_BLUE = "#5FA7E5"
AMBER = "#FFB120"
CHARCOAL = "#333333"
SILVER = "#E4E8F1"


def _load_file_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _build_font_faces():
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
            b64 = _load_file_base64(os.path.join(FONTS_DIR, filename))
            if b64:
                css += f"""
@font-face {{
    font-family: '{family}';
    src: url(data:font/truetype;base64,{b64}) format('truetype');
    font-weight: {weight};
    font-style: normal;
}}"""
    return css


def generate_creative_tip_card(platform, tag_text, title, subtitle, steps,
                                cta_text, campaign_id,
                                illustration_file="interview_3d.png"):
    width, height = PLATFORM_SIZES[platform]
    font_faces = _build_font_faces()

    # Load illustration as base64
    illust_path = os.path.join(ILLUSTRATIONS_DIR, illustration_file)
    illust_b64 = _load_file_base64(illust_path)
    illust_img = ""
    if illust_b64:
        illust_img = f'<img src="data:image/png;base64,{illust_b64}" class="hero-illustration" alt="Interview">'

    # Load white logo PNG
    logo_path = os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")
    logo_b64 = _load_file_base64(logo_path)
    logo_img = ""
    if logo_b64:
        logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo" alt="Internwise">'

    # Build steps HTML
    steps_html = ""
    icons = ["📍", "🔙", "🚀"]  # Present, Past, Future
    for i, step in enumerate(steps):
        steps_html += f"""
        <div class="step-pill">
            <div class="step-icon">{icons[i] if i < len(icons) else str(i+1)}</div>
            <div class="step-text">
                <span class="step-label">{step['title']}</span>
                <span class="step-desc">{step['description']}</span>
            </div>
        </div>"""

    # Compute responsive sizes
    is_square = platform == "instagram"
    illust_h = int(height * 0.38) if is_square else int(height * 0.35)
    title_size = int(width * 0.048) if is_square else int(width * 0.04)
    tag_size = int(width * 0.013)
    sub_size = int(width * 0.019)
    step_label_size = int(width * 0.018)
    step_desc_size = int(width * 0.016)
    cta_size = int(width * 0.017)
    pad_x = int(width * 0.06)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{font_faces}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

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
    background: linear-gradient(170deg, #0f1c2e 0%, {DEEP_BLUE} 30%, #1a3a5c 55%, #1d4063 75%, #0f1c2e 100%);
    overflow: hidden;
}}

/* ── Gradient orbs for depth ── */
.orb {{
    position: absolute;
    border-radius: 50%;
    z-index: 0;
}}
.orb-1 {{
    width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(91,146,145,0.5) 0%, transparent 65%);
    top: -200px; right: -200px;
    filter: blur(100px);
}}
.orb-2 {{
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(62,119,177,0.4) 0%, transparent 65%);
    bottom: -200px; left: -200px;
    filter: blur(100px);
}}
.orb-3 {{
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(95,167,229,0.25) 0%, transparent 55%);
    top: 40%; left: 50%;
    transform: translateX(-50%);
    filter: blur(80px);
}}
/* warm accent orb behind illustration */
.orb-4 {{
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(255,177,32,0.12) 0%, transparent 55%);
    top: 5%; left: 30%;
    filter: blur(90px);
}}

/* ── Subtle noise texture ── */
.noise {{
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    background-size: 256px 256px;
    z-index: 1;
    opacity: 0.6;
}}

/* ── Top accent bar ── */
.top-bar {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, {TEAL} 0%, {MEDIUM_BLUE} 40%, {LIGHT_BLUE} 70%, {TEAL} 100%);
    z-index: 30;
}}

/* ── Hero illustration zone ── */
.hero-zone {{
    position: relative;
    z-index: 10;
    width: 100%;
    height: {illust_h}px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding-top: {int(height * 0.03)}px;
}}

.hero-illustration {{
    height: {int(illust_h * 0.92)}px;
    object-fit: contain;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.4));
    position: relative;
    z-index: 5;
}}

/* Glow behind illustration */
.hero-glow {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(91,146,145,0.2) 0%, transparent 70%);
    z-index: 2;
}}

/* ── Content zone ── */
.content-zone {{
    position: relative;
    z-index: 10;
    padding: {int(height * 0.02)}px {pad_x}px {int(height * 0.01)}px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* ── Tag badge ── */
.tag {{
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: {tag_size}px;
    letter-spacing: 2.5px;
    color: {LIGHT_BLUE};
    background: rgba(95,167,229,0.1);
    border: 1px solid rgba(95,167,229,0.25);
    padding: 8px 24px;
    border-radius: 50px;
    text-transform: uppercase;
    margin-bottom: {int(height * 0.015)}px;
}}

/* ── Title ── */
.title {{
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: {title_size}px;
    color: #FFFFFF;
    text-align: center;
    line-height: 1.15;
    margin-bottom: {int(height * 0.008)}px;
}}

.title em {{
    font-style: normal;
    background: linear-gradient(135deg, {LIGHT_BLUE}, {TEAL});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

/* ── Subtitle ── */
.subtitle {{
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
    font-size: {sub_size}px;
    color: rgba(255,255,255,0.5);
    text-align: center;
    margin-bottom: {int(height * 0.02)}px;
}}

/* ── Steps — horizontal pill cards ── */
.steps-row {{
    display: flex;
    flex-direction: column;
    gap: {int(height * 0.012)}px;
    width: 100%;
    margin-bottom: {int(height * 0.02)}px;
}}

.step-pill {{
    display: flex;
    align-items: center;
    gap: {int(width * 0.02)}px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: {int(height * 0.014)}px {int(width * 0.03)}px;
    transition: all 0.3s;
}}

.step-pill:nth-child(1) {{
    border-left: 3px solid {TEAL};
}}
.step-pill:nth-child(2) {{
    border-left: 3px solid {MEDIUM_BLUE};
}}
.step-pill:nth-child(3) {{
    border-left: 3px solid {LIGHT_BLUE};
}}

.step-icon {{
    font-size: {int(width * 0.028)}px;
    flex-shrink: 0;
    width: {int(width * 0.045)}px;
    height: {int(width * 0.045)}px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.step-text {{
    display: flex;
    flex-direction: column;
    gap: 2px;
}}

.step-label {{
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: {step_label_size}px;
    color: #FFFFFF;
    letter-spacing: 0.3px;
}}

.step-desc {{
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
    font-size: {step_desc_size}px;
    color: rgba(255,255,255,0.55);
    line-height: 1.4;
}}

/* ── CTA button ── */
.cta {{
    background: linear-gradient(135deg, {TEAL} 0%, {MEDIUM_BLUE} 100%);
    color: white;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: {cta_size}px;
    padding: 14px 36px;
    border-radius: 50px;
    text-align: center;
    letter-spacing: 0.3px;
    box-shadow: 0 8px 28px rgba(91,146,145,0.3);
}}

/* ── Footer ── */
.footer {{
    position: absolute;
    bottom: {int(height * 0.025)}px;
    left: 0; right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
}}

.logo {{
    height: {int(height * 0.03)}px;
    opacity: 0.7;
}}

/* ── Decorative floating shapes ── */
.float-shape {{
    position: absolute;
    border-radius: 50%;
    z-index: 3;
}}
.fs-1 {{
    width: 12px; height: 12px;
    background: {TEAL};
    opacity: 0.3;
    top: 15%; left: 8%;
}}
.fs-2 {{
    width: 8px; height: 8px;
    background: {LIGHT_BLUE};
    opacity: 0.25;
    top: 25%; right: 10%;
}}
.fs-3 {{
    width: 16px; height: 16px;
    border: 2px solid rgba(91,146,145,0.2);
    background: none;
    top: 10%; right: 20%;
}}
.fs-4 {{
    width: 6px; height: 6px;
    background: {AMBER};
    opacity: 0.3;
    top: 35%; left: 12%;
}}
.fs-5 {{
    width: 10px; height: 10px;
    border: 2px solid rgba(95,167,229,0.15);
    background: none;
    bottom: 30%; right: 8%;
}}

/* ── Attribution (required by Vecteezy free license) ── */
.attribution {{
    position: absolute;
    bottom: 6px;
    right: 10px;
    font-family: 'DM Sans', sans-serif;
    font-size: 8px;
    color: rgba(255,255,255,0.15);
    z-index: 20;
}}

</style>
</head>
<body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="noise"></div>

    <!-- Gradient orbs -->
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>

    <!-- Floating shapes -->
    <div class="float-shape fs-1"></div>
    <div class="float-shape fs-2"></div>
    <div class="float-shape fs-3"></div>
    <div class="float-shape fs-4"></div>
    <div class="float-shape fs-5"></div>

    <!-- Hero illustration -->
    <div class="hero-zone">
        <div class="hero-glow"></div>
        {illust_img}
    </div>

    <!-- Content -->
    <div class="content-zone">
        <div class="tag">{tag_text}</div>
        <div class="title">{title}</div>
        <div class="subtitle">{subtitle}</div>

        <div class="steps-row">
            {steps_html}
        </div>

        <div class="cta">{cta_text}</div>
    </div>

    <!-- Logo -->
    <div class="footer">
        {logo_img}
    </div>

    <div class="attribution">3D illustration by Zikku Creative via Vecteezy</div>
</div>
</body>
</html>"""

    # Render
    output_dir = os.path.join(OUTPUT_DIR, campaign_id)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"graphic_{platform}_v4.png")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()

    print(f"  ✓ {platform}: {output_path} ({width}×{height} @2x)")
    return output_path


if __name__ == "__main__":
    CAMPAIGN_ID = "candidate-tmay-magic-formula"

    steps = [
        {
            "title": "Present",
            "description": "Who you are right now — your degree, focus, and what drives you."
        },
        {
            "title": "Past",
            "description": "The experience that led you here — a project, internship, or skill you built."
        },
        {
            "title": "Future",
            "description": "Why this role, this company, right now. Show you've done your homework."
        }
    ]

    print("\n🎨 Internwise — Creative Graphics v4")
    print("=" * 50)

    path = generate_creative_tip_card(
        platform="instagram",
        tag_text="Interview Tip",
        title='"Tell me about <em>yourself</em>"',
        subtitle="The magic formula to nail your answer every time",
        steps=steps,
        cta_text="Find your next internship → internwise.com",
        campaign_id=CAMPAIGN_ID,
    )

    print(f"\n✅ Done: {path}")
