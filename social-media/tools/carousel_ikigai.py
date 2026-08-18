"""
Internwise — Ikigai Carousel
Post 5: 3-slide Instagram carousel (1080x1080)
Japanese concept: finding your reason for being. Integrated with avataaars.
"""

import os
import base64
import requests
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

DEEP_BLUE = "#264D7E"
TEAL = "#5B9291"
AMBER = "#FFB120"
CREAM = "#faf8f3"


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


def _fetch_dicebear_avatar(seed, style="avataaars", scale=100):
    url = f"https://api.dicebear.com/7.x/{style}/png?seed={seed}&scale={scale}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return base64.b64encode(resp.content).decode()
    except Exception:
        pass
    return None


def _render(html, output_path, width=1080, height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()
    print(f"  ✓ {output_path}")


def generate_slide1(campaign_dir):
    """Slide 1: Hook with 3 avatars"""

    w, h = 1080, 1080
    font_faces = _build_font_faces()
    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""

    avatars = [_fetch_dicebear_avatar(f"ikigai_{i}", "avataaars", 100) for i in range(3)]
    avatar_grid = "".join(f'<img src="data:image/png;base64,{av}" class="avatar">' for av in avatars if av)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, {CREAM} 0%, #f0ebe0 100%);
}}

.logo-wrap {{ position:absolute; top:30px; left:30px; z-index:25; }}
.logo {{ height:70px; opacity:0.9; }}

.top-bar {{ position:absolute; top:0; left:0; right:0; height:5px;
    background: linear-gradient(90deg, {TEAL}, {DEEP_BLUE}, {AMBER}); z-index:30; }}

.content {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    width:90%; z-index:10;
}}

.headline {{
    font-family:Inter; font-weight:700;
    font-size:44px; line-height:1.3;
    color:{DEEP_BLUE}; text-align:center;
    margin-bottom:50px;
}}

.headline .highlight {{ color:{AMBER}; }}

.avatar-grid {{
    display:grid;
    grid-template-columns:repeat(3, 1fr);
    gap:25px;
    margin-bottom:30px;
}}

.avatar {{
    width:260px; height:260px;
    border-radius:16px;
    background:#ffffff;
    object-fit:contain;
    padding:10px;
}}

.subtext {{
    font-family:DM Sans; font-size:16px;
    color:{DEEP_BLUE}; opacity:0.8;
    text-align:center; line-height:1.5;
}}
</style>
</head><body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="logo-wrap">{logo_img}</div>
    <div class="content">
        <div class="headline">Find Your <span class="highlight">Ikigai</span></div>
        <div class="avatar-grid">{avatar_grid}</div>
        <div class="subtext">Your reason for being. The intersection of passion, skill, need, and purpose.</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_1.png"))


def generate_slide2(campaign_dir):
    """Slide 2: What you love - with avatar"""

    w, h = 1080, 1080
    font_faces = _build_font_faces()

    avatar = _fetch_dicebear_avatar("ikigai_love", "avataaars", 120)
    avatar_html = f'<img src="data:image/png;base64,{avatar}" class="avatar-main">' if avatar else ""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, {CREAM} 0%, #f0ebe0 100%);
}}

.grid {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:grid;
    grid-template-columns:330px 1fr;
    gap:40px;
    width:90%; z-index:10;
}}

.avatar-main {{
    width:330px; height:400px;
    border-radius:20px;
    background:#ffffff;
    object-fit:contain;
    padding:10px;
}}

.content {{
    display:flex;
    flex-direction:column;
    justify-content:center;
}}

.number {{
    font-family:DM Sans; font-size:13px;
    color:{AMBER};
    text-transform:uppercase; letter-spacing:1px;
    margin-bottom:10px;
}}

.title {{
    font-family:Inter; font-weight:700;
    font-size:40px; color:{DEEP_BLUE};
    line-height:1.3; margin-bottom:20px;
}}

.description {{
    font-family:DM Sans; font-size:16px;
    color:{DEEP_BLUE}; opacity:0.8;
    line-height:1.6;
}}
</style>
</head><body>
<div class="canvas">
    <div class="grid">
        <div>{avatar_html}</div>
        <div class="content">
            <div class="number">Circle 1</div>
            <div class="title">What You <span style="color:{AMBER}">Love</span></div>
            <div class="description">The activities that energize you. What would you do if time/money weren't factors?</div>
        </div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_2.png"))


def generate_slide3(campaign_dir):
    """Slide 3: The other circles + integration - with avatars"""

    w, h = 1080, 1080
    font_faces = _build_font_faces()

    avatars = [
        _fetch_dicebear_avatar("ikigai_good", "avataaars", 100),
        _fetch_dicebear_avatar("ikigai_paid", "avataaars", 100),
        _fetch_dicebear_avatar("ikigai_needed", "avataaars", 100),
    ]

    avatar_html = "".join(f'<img src="data:image/png;base64,{av}" class="avatar-circle">' for av in avatars if av)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, {CREAM} 0%, #f0ebe0 100%);
}}

.content {{
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    width:90%; z-index:10;
}}

.headline {{
    font-family:Inter; font-weight:700;
    font-size:42px; line-height:1.3;
    color:{DEEP_BLUE}; text-align:center;
    margin-bottom:50px;
}}

.headline .highlight {{ color:{AMBER}; }}

.avatar-grid {{
    display:grid;
    grid-template-columns:repeat(3, 1fr);
    gap:25px;
    margin-bottom:40px;
}}

.avatar-circle {{
    width:260px; height:260px;
    border-radius:16px;
    background:#ffffff;
    object-fit:contain;
    padding:10px;
}}

.circles {{
    font-family:DM Sans; font-size:14px;
    color:{DEEP_BLUE}; opacity:0.75;
    text-align:center; line-height:1.8;
}}

.circle-item {{
    margin:8px 0;
    font-weight:500;
}}

.circle-item .label {{
    color:{AMBER};
    font-weight:700;
}}
</style>
</head><body>
<div class="canvas">
    <div class="content">
        <div class="headline">The Complete <span class="highlight">Ikigai</span></div>
        <div class="avatar-grid">{avatar_html}</div>
        <div class="circles">
            <div class="circle-item"><span class="label">Good at:</span> Skills you've mastered</div>
            <div class="circle-item"><span class="label">Paid for:</span> What employers need</div>
            <div class="circle-item"><span class="label">Needed:</span> What the world needs</div>
            <div style="margin-top:20px; border-top:1px solid rgba(38,77,126,0.2); padding-top:20px;">
                The intersection is where fulfillment lives.
            </div>
        </div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_3.png"))


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating Ikigai Carousel (Post 5)...")
    generate_slide1(campaign_dir)
    generate_slide2(campaign_dir)
    generate_slide3(campaign_dir)
    print("✓ Ikigai carousel complete!")
