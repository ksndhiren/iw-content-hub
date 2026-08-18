"""
Internwise — Carousel Slide Generator
Generates individual carousel slides for Instagram (1080x1080).
Each slide is a standalone design with consistent branding.
"""

import os
import base64
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
ILLUSTRATIONS_DIR = os.path.join(BASE_DIR, "assets", "illustrations")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

# Brand colors
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
            ("Inter-Bold.ttf", 700), ("Inter-SemiBold.ttf", 600),
            ("Inter-Medium.ttf", 500), ("Inter-Regular.ttf", 400),
        ],
        "DM Sans": [
            ("DMSans-Bold.ttf", 700), ("DMSans-Medium.ttf", 500),
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
    font-weight: {weight}; font-style: normal;
}}"""
    return css


def _render(html, output_path, width=1080, height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()
    print(f"  ✓ {output_path}")


def generate_comeback_slide1(campaign_dir, illustration_file="interview_3d.png"):
    """Slide 1: Bold comeback hook with 3D illustration."""

    w, h = 1080, 1080
    font_faces = _build_font_faces()

    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""

    illust_b64 = _load_file_base64(os.path.join(ILLUSTRATIONS_DIR, illustration_file))
    illust_img = f'<img src="data:image/png;base64,{illust_b64}" class="hero-img">' if illust_b64 else ""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(170deg, #0f1c2e 0%, {DEEP_BLUE} 35%, #1a3a5c 60%, #0f1c2e 100%);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}}

/* Orbs */
.orb {{ position:absolute; border-radius:50%; z-index:0; }}
.orb-1 {{ width:600px; height:600px; background:radial-gradient(circle,rgba(91,146,145,0.4) 0%,transparent 60%); top:-150px; right:-150px; filter:blur(90px); }}
.orb-2 {{ width:500px; height:500px; background:radial-gradient(circle,rgba(95,167,229,0.3) 0%,transparent 55%); bottom:-150px; left:-100px; filter:blur(90px); }}
.orb-3 {{ width:300px; height:300px; background:radial-gradient(circle,rgba(255,177,32,0.12) 0%,transparent 50%); top:35%; left:40%; filter:blur(70px); }}

.top-bar {{ position:absolute; top:0; left:0; right:0; height:5px; background:linear-gradient(90deg,{TEAL},{MEDIUM_BLUE},{LIGHT_BLUE},{AMBER}); z-index:30; }}

/* Logo */
.logo-wrap {{ position:absolute; top:28px; left:35px; z-index:25; }}
.logo {{ height:54px; opacity:0.9; }}

/* Swipe hint */
.swipe {{ position:absolute; bottom:30px; right:35px; z-index:25;
    font-family:'DM Sans',sans-serif; font-weight:500; font-size:15px;
    color:rgba(255,255,255,0.4); letter-spacing:0.5px;
    display:flex; align-items:center; gap:6px;
}}
.swipe-arrow {{ font-size:18px; }}

/* Hero illustration */
.hero-zone {{
    position:relative; z-index:10;
    margin-bottom: 30px;
}}
.hero-img {{
    height: 380px;
    object-fit: contain;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.45));
}}
.hero-glow {{
    position:absolute; bottom:-20px; left:50%; transform:translateX(-50%);
    width:420px; height:200px; border-radius:50%;
    background:radial-gradient(ellipse,rgba(62,119,177,0.2) 0%,transparent 70%);
    z-index:1;
}}

/* Text content */
.text-block {{
    position:relative; z-index:15;
    text-align:center;
    padding: 0 60px;
}}

.headline {{
    font-family:'Inter',sans-serif; font-weight:700;
    font-size: 52px; color: #FFFFFF;
    line-height: 1.15; margin-bottom: 14px;
}}

.headline-accent {{
    color: {AMBER};
}}

.subline {{
    font-family:'DM Sans',sans-serif; font-weight:400;
    font-size: 24px; color: rgba(255,255,255,0.55);
    line-height: 1.4;
}}

/* Slide indicator dots */
.dots {{
    position:absolute; bottom:32px; left:50%; transform:translateX(-50%);
    display:flex; gap:8px; z-index:25;
}}
.dot {{
    width:8px; height:8px; border-radius:50%;
    background:rgba(255,255,255,0.25);
}}
.dot.active {{ background:{AMBER}; width:24px; border-radius:4px; }}

/* Decorative */
.ring {{ position:absolute; border:2px solid rgba(95,167,229,0.12); border-radius:50%; z-index:3; }}
.r1 {{ width:50px; height:50px; top:10%; left:8%; }}
.r2 {{ width:35px; height:35px; top:18%; right:10%; }}
.cdot {{ position:absolute; border-radius:50%; z-index:3; }}
.cd1 {{ width:8px; height:8px; background:{TEAL}; opacity:0.3; top:25px; right:120px; }}
.cd2 {{ width:5px; height:5px; background:{AMBER}; opacity:0.25; top:15%; left:15%; }}

.attribution {{
    position:absolute; bottom:6px; left:10px;
    font-family:'DM Sans'; font-size:7px; color:rgba(255,255,255,0.1); z-index:20;
}}
</style></head>
<body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="ring r1"></div>
    <div class="ring r2"></div>
    <div class="cdot cd1"></div>
    <div class="cdot cd2"></div>

    <div class="logo-wrap">{logo_img}</div>

    <div class="hero-zone">
        <div class="hero-glow"></div>
        {illust_img}
    </div>

    <div class="text-block">
        <div class="headline">We took a break.<br>But we <span class="headline-accent">never stopped</span><br>believing in you.</div>
        <div class="subline">Swipe for 4 reminders if your job search feels stuck.</div>
    </div>

    <div class="dots">
        <div class="dot active"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>

    <div class="swipe">Swipe <span class="swipe-arrow">→</span></div>
    <div class="attribution">3D art by Zikku Creative via Vecteezy</div>
</div>
</body></html>"""

    out = os.path.join(campaign_dir, "slide_1.png")
    _render(html, out)
    return out


if __name__ == "__main__":
    campaign_dir = os.path.join(OUTPUT_DIR, "wk1-day1-comeback-carousel")
    os.makedirs(campaign_dir, exist_ok=True)

    print("\n🎨 Post 1 — Comeback Carousel")
    print("=" * 50)
    generate_comeback_slide1(campaign_dir)
