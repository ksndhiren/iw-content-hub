"""
Internwise — CV Mistakes Tip Card
Post 2: Single image tip card (1080x1080)
5 common CV mistakes with avatar visual support.
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
MEDIUM_BLUE = "#3E77B1"
LIGHT_BLUE = "#5FA7E5"
AMBER = "#FFB120"
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


def generate(campaign_dir):
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""

    # Fetch 2 avatars for visual support
    avatars = [
        _fetch_dicebear_avatar("cv_mistake_1", "avataaars", 90),
        _fetch_dicebear_avatar("cv_mistake_2", "avataaars", 90),
    ]

    avatar_html = ""
    for i, av in enumerate(avatars):
        if av:
            side = 'left' if i == 0 else 'right'
            avatar_html += f'<img src="data:image/png;base64,{av}" class="avatar-{side}">'

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: #F0F2F7;
}}

.avatar-left {{
    position:absolute;
    left:20px; bottom:30px;
    width:200px; height:240px;
    background:#ffffff;
    border-radius:12px;
    padding:8px;
    object-fit:contain;
}}

.avatar-right {{
    position:absolute;
    right:20px; top:30px;
    width:200px; height:240px;
    background:#ffffff;
    border-radius:12px;
    padding:8px;
    object-fit:contain;
}}

.header-band {{
    position:absolute;
    top:0; left:0; right:0;
    height:360px;
    background: linear-gradient(135deg, #0f2035 0%, {DEEP_BLUE} 50%, #1a4a6e 100%);
    z-index:1;
}}

.header-curve {{
    position:absolute;
    top:330px; left:0; right:0;
    height:60px;
    background:#F0F2F7;
    border-radius:50% 50% 0 0 / 100% 100% 0 0;
    z-index:2;
}}

.logo {{ position:absolute; top:35px; left:35px; height:70px; opacity:0.9; z-index:25; }}

.headline {{
    position:absolute; top:140px; left:40px; right:40px;
    font-family:Inter; font-weight:700;
    font-size:44px; line-height:1.2;
    color:white;
}}

.headline .highlight {{ color:{AMBER}; }}

.tips-container {{
    position:absolute;
    top:420px; left:35px; right:35px; bottom:35px;
    display:flex;
    flex-direction:column;
    gap:16px;
    z-index:10;
}}

.tip {{
    display:grid;
    grid-template-columns:45px 1fr;
    gap:15px;
    align-items:start;
}}

.tip-number {{
    width:45px; height:45px;
    background:{AMBER};
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:Inter; font-weight:700;
    font-size:20px;
    color:white;
    flex-shrink:0;
}}

.tip-text {{
    font-family:DM Sans; font-size:15px;
    color:{DEEP_BLUE};
    line-height:1.5;
    padding-top:4px;
}}

.cta {{
    text-align:center;
    font-family:DM Sans; font-weight:600;
    font-size:14px;
    color:{AMBER};
    margin-top:10px;
}}
</style>
</head><body>
<div class="canvas">
    {avatar_html}
    <div class="logo">{logo_img}</div>
    <div class="header-band"></div>
    <div class="header-curve"></div>

    <div class="headline">Avoid These <span class="highlight">5 CV Mistakes</span></div>

    <div class="tips-container">
        <div class="tip">
            <div class="tip-number">1</div>
            <div class="tip-text"><strong>Generic objective</strong> — Tailor it to each role</div>
        </div>
        <div class="tip">
            <div class="tip-number">2</div>
            <div class="tip-text"><strong>No metrics</strong> — Use numbers. "Increased sales 40%"</div>
        </div>
        <div class="tip">
            <div class="tip-number">3</div>
            <div class="tip-text"><strong>Spelling errors</strong> — Proofread 3x. No excuses</div>
        </div>
        <div class="tip">
            <div class="tip-number">4</div>
            <div class="tip-text"><strong>Poor formatting</strong> — Clean, readable, ATS-friendly</div>
        </div>
        <div class="tip">
            <div class="tip-number">5</div>
            <div class="tip-text"><strong>Too long</strong> — Max 1-2 pages. Quality over length</div>
        </div>
        <div class="cta">✓ www.internwise.co.uk</div>
    </div>
</div>
</body></html>
"""

    os.makedirs(campaign_dir, exist_ok=True)
    _render(html, os.path.join(campaign_dir, "tipcard_cv_mistakes.png"))
    print("✓ CV Mistakes tip card complete!")


def generate_standalone(output_path):
    """Alternative: call directly for testing"""
    campaign_dir = os.path.dirname(output_path)
    generate(campaign_dir)
