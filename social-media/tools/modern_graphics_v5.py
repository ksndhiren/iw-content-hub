"""
Internwise — Creative Graphics v5
Bold editorial layout, large typography, full canvas utilization,
3D illustration hero with proper contrast and creative design.
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
    "instagram": (1080, 1080),
    "instagram_story": (1080, 1920),
    "linkedin": (1200, 627),
    "x": (1200, 675),
    "tiktok": (1080, 1920),
}


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


def generate(platform, tag_text, title_line1, title_line2, subtitle,
             steps, cta_text, campaign_id,
             illustration_file="interview_3d.png"):

    width, height = PLATFORM_SIZES[platform]
    font_faces = _build_font_faces()

    # Load assets
    illust_b64 = _load_file_base64(os.path.join(ILLUSTRATIONS_DIR, illustration_file))
    illust_img = f'<img src="data:image/png;base64,{illust_b64}" class="hero-img">' if illust_b64 else ""

    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""

    # Steps HTML - numbered circles with bright colors
    step_colors = ["#5FA7E5", "#5B9291", "#FFB120"]
    steps_html = ""
    for i, step in enumerate(steps):
        color = step_colors[i % len(step_colors)]
        steps_html += f"""
        <div class="step-card">
            <div class="step-num" style="background: {color};">{i + 1}</div>
            <div class="step-body">
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

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
}}

.canvas {{
    width: {width}px;
    height: {height}px;
    position: relative;
    overflow: hidden;
}}

/* ══════════════════════════════════════════
   BACKGROUND: Diagonal split design
   ══════════════════════════════════════════ */

/* Top zone - lighter blue for illustration */
.bg-top {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 52%;
    background: linear-gradient(160deg, #1a3f6b 0%, #264D7E 40%, #2d5a8a 100%);
    z-index: 0;
}}

/* Bottom zone - darker for text readability */
.bg-bottom {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 52%;
    background: linear-gradient(180deg, #0f1f35 0%, #0c1a2e 50%, #0a1525 100%);
    z-index: 0;
}}

/* Diagonal divider - a curved wave separating the zones */
.wave-divider {{
    position: absolute;
    top: 42%;
    left: 0; right: 0;
    height: 16%;
    z-index: 2;
    overflow: hidden;
}}
.wave-divider svg {{
    width: 100%;
    height: 100%;
}}

/* ── Gradient orbs ── */
.orb {{
    position: absolute;
    border-radius: 50%;
    z-index: 1;
}}
.orb-1 {{
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(95,167,229,0.3) 0%, transparent 60%);
    top: -100px; right: -100px;
    filter: blur(80px);
}}
.orb-2 {{
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(91,146,145,0.25) 0%, transparent 55%);
    top: 30%; left: -100px;
    filter: blur(80px);
}}
.orb-3 {{
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(255,177,32,0.1) 0%, transparent 50%);
    bottom: 10%; right: -50px;
    filter: blur(70px);
}}

/* ── Top accent bar ── */
.top-accent {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, #5B9291, #3E77B1, #5FA7E5, #FFB120);
    z-index: 30;
}}

/* ══════════════════════════════════════════
   HERO ILLUSTRATION - Large, asymmetric
   ══════════════════════════════════════════ */
.hero-zone {{
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    display: flex;
    justify-content: center;
}}

.hero-img {{
    height: {int(height * 0.40)}px;
    object-fit: contain;
    filter: drop-shadow(0 25px 50px rgba(0,0,0,0.5));
}}

/* Circular glow behind illustration */
.hero-backdrop {{
    position: absolute;
    top: {int(height * 0.05)}px;
    left: 50%;
    transform: translateX(-50%);
    width: {int(width * 0.55)}px;
    height: {int(width * 0.55)}px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(62,119,177,0.2) 0%, rgba(38,77,126,0.1) 50%, transparent 70%);
    z-index: 3;
}}

/* ══════════════════════════════════════════
   CONTENT - Bold, large, readable
   ══════════════════════════════════════════ */
.content {{
    position: absolute;
    top: {int(height * 0.42)}px;
    left: 0; right: 0;
    z-index: 15;
    padding: 0 {int(width * 0.06)}px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* Tag */
.tag {{
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: {int(width * 0.018)}px;
    letter-spacing: 3px;
    color: #FFB120;
    text-transform: uppercase;
    margin-bottom: {int(height * 0.012)}px;
}}

/* Title - BIG and bold */
.title-block {{
    text-align: center;
    margin-bottom: {int(height * 0.008)}px;
}}

.title-line {{
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: {int(width * 0.072)}px;
    color: #FFFFFF;
    line-height: 1.1;
    display: block;
}}

.title-highlight {{
    color: #FFB120;
}}

/* Subtitle */
.subtitle {{
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
    font-size: {int(width * 0.024)}px;
    color: rgba(255,255,255,0.55);
    text-align: center;
    margin-bottom: {int(height * 0.025)}px;
}}

/* ── Step cards - three columns side by side ── */
.steps-grid {{
    display: flex;
    gap: {int(width * 0.02)}px;
    width: 100%;
    margin-bottom: {int(height * 0.025)}px;
}}

.step-card {{
    flex: 1;
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: {int(height * 0.018)}px {int(width * 0.02)}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: {int(height * 0.008)}px;
}}

.step-num {{
    width: {int(width * 0.05)}px;
    height: {int(width * 0.05)}px;
    border-radius: 50%;
    color: #0c1a2e;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: {int(width * 0.024)}px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}}

.step-title {{
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: {int(width * 0.022)}px;
    color: #FFFFFF;
}}

.step-desc {{
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
    font-size: {int(width * 0.019)}px;
    color: rgba(255,255,255,0.6);
    line-height: 1.4;
}}

/* ── CTA ── */
.cta {{
    background: linear-gradient(135deg, #5B9291 0%, #3E77B1 100%);
    color: white;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: {int(width * 0.022)}px;
    padding: {int(height * 0.016)}px {int(width * 0.08)}px;
    border-radius: 50px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(91,146,145,0.35);
}}

/* ── Logo - top left ── */
.logo-wrapper {{
    position: absolute;
    top: {int(height * 0.025)}px;
    left: {int(width * 0.04)}px;
    z-index: 25;
}}

.logo {{
    height: {int(height * 0.05)}px;
    opacity: 0.9;
}}

/* ── Decorative accents ── */
.accent-line-left {{
    position: absolute;
    top: {int(height * 0.44)}px;
    left: {int(width * 0.04)}px;
    width: 3px;
    height: {int(height * 0.08)}px;
    background: linear-gradient(180deg, #5FA7E5, transparent);
    border-radius: 2px;
    z-index: 12;
}}

.accent-line-right {{
    position: absolute;
    top: {int(height * 0.46)}px;
    right: {int(width * 0.04)}px;
    width: 3px;
    height: {int(height * 0.06)}px;
    background: linear-gradient(180deg, #FFB120, transparent);
    border-radius: 2px;
    z-index: 12;
}}

.corner-dot {{
    position: absolute;
    width: 8px; height: 8px;
    border-radius: 50%;
    z-index: 12;
}}
.cd-1 {{ top: 30px; left: 30px; background: #5B9291; opacity: 0.4; }}
.cd-2 {{ top: 30px; right: 30px; background: #5FA7E5; opacity: 0.3; }}
.cd-3 {{ top: 45px; left: 50px; background: #FFB120; opacity: 0.25; width: 5px; height: 5px; }}

/* Ring decoration near illustration */
.ring-decor {{
    position: absolute;
    width: 60px; height: 60px;
    border: 2px solid rgba(95,167,229,0.15);
    border-radius: 50%;
    z-index: 4;
}}
.rd-1 {{ top: 8%; left: 10%; }}
.rd-2 {{ top: 15%; right: 8%; width: 40px; height: 40px; border-color: rgba(91,146,145,0.15); }}

/* Attribution */
.attribution {{
    position: absolute;
    bottom: 6px; right: 10px;
    font-family: 'DM Sans', sans-serif;
    font-size: 8px;
    color: rgba(255,255,255,0.12);
    z-index: 20;
}}

</style>
</head>
<body>
<div class="canvas">
    <!-- Background zones -->
    <div class="bg-top"></div>
    <div class="bg-bottom"></div>
    <div class="top-accent"></div>

    <!-- Wave divider SVG -->
    <div class="wave-divider">
        <svg viewBox="0 0 1080 180" preserveAspectRatio="none">
            <path d="M0,90 C200,160 400,20 540,90 C680,160 880,20 1080,90 L1080,180 L0,180 Z"
                  fill="#0f1f35"/>
        </svg>
    </div>

    <!-- Gradient orbs -->
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    <!-- Decorative elements -->
    <div class="corner-dot cd-1"></div>
    <div class="corner-dot cd-2"></div>
    <div class="corner-dot cd-3"></div>
    <div class="ring-decor rd-1"></div>
    <div class="ring-decor rd-2"></div>
    <div class="accent-line-left"></div>
    <div class="accent-line-right"></div>

    <!-- Hero illustration with backdrop glow -->
    <div class="hero-backdrop"></div>
    <div class="hero-zone">
        {illust_img}
    </div>

    <!-- Main content -->
    <div class="content">
        <div class="tag">{tag_text}</div>

        <div class="title-block">
            <span class="title-line">{title_line1}</span>
            <span class="title-line"><span class="title-highlight">{title_line2}</span></span>
        </div>

        <div class="subtitle">{subtitle}</div>

        <div class="steps-grid">
            {steps_html}
        </div>

        <div class="cta">{cta_text}</div>
    </div>

    <!-- Logo - top left -->
    <div class="logo-wrapper">
        {logo_img}
    </div>

    <div class="attribution">3D art by Zikku Creative via Vecteezy</div>
</div>
</body>
</html>"""

    output_dir = os.path.join(OUTPUT_DIR, campaign_id)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"graphic_{platform}_v5.png")

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
        {"title": "Present", "description": "Who you are now, your degree, focus, and drive."},
        {"title": "Past", "description": "The experience that built you: projects, internships, skills."},
        {"title": "Future", "description": "Why this role, this company, right now."},
    ]

    print("\n🎨 Internwise — Creative Graphics v5")
    print("=" * 50)

    generate(
        platform="instagram",
        tag_text="Interview Tip",
        title_line1='"Tell Me About',
        title_line2='Yourself"',
        subtitle="The magic formula to nail your answer every time",
        steps=steps,
        cta_text="Find your next internship → www.internwise.com",
        campaign_id=CAMPAIGN_ID,
    )
