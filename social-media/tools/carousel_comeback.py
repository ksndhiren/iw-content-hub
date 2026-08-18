"""
Internwise — Comeback Carousel Generator
Post 1: "Back & Better" — 5-slide Instagram carousel (1080x1080)
Each slide has a unique layout while maintaining visual cohesion.

Design concept for Slide 1: "Warm Glow"
- Typography-forward hero design
- Dark-to-warm gradient (deep blue → amber glow) evoking sunrise/new beginnings
- Large emotional text with amber highlight on key phrase
- Radial warm glow behind text as visual anchor
- Geometric accent shapes for modern feel
"""

import os
import base64
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


def generate_slide1(campaign_dir):
    """Slide 1: Hook — 'We took a break. We never stopped believing in you.'
    Design: Warm Glow — typography hero with sunrise gradient."""

    w, h = 1080, 1080
    font_faces = _build_font_faces()

    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(155deg, #0a1628 0%, #0f2035 20%, #162d4a 40%, #1e3d5e 60%, #264D7E 80%, #2d5a3d 100%);
}}

/* ── Warm sunrise glow — large radial behind text ── */
.glow-warm {{
    position:absolute;
    width:900px; height:900px;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    border-radius:50%;
    background: radial-gradient(circle,
        rgba(255,177,32,0.18) 0%,
        rgba(255,153,97,0.1) 25%,
        rgba(62,119,177,0.08) 45%,
        transparent 65%
    );
    z-index:1;
    filter: blur(40px);
}}

/* Secondary cool glow top-right */
.glow-cool {{
    position:absolute;
    width:500px; height:500px;
    top:-120px; right:-80px;
    border-radius:50%;
    background: radial-gradient(circle,
        rgba(95,167,229,0.2) 0%,
        rgba(91,146,145,0.1) 40%,
        transparent 65%
    );
    z-index:1;
    filter: blur(60px);
}}

/* Subtle bottom-left teal glow */
.glow-teal {{
    position:absolute;
    width:400px; height:400px;
    bottom:-80px; left:-60px;
    border-radius:50%;
    background: radial-gradient(circle,
        rgba(91,146,145,0.15) 0%,
        transparent 60%
    );
    z-index:1;
    filter: blur(50px);
}}

/* ── Top accent bar ── */
.top-bar {{
    position:absolute; top:0; left:0; right:0;
    height:5px;
    background: linear-gradient(90deg, {TEAL}, {MEDIUM_BLUE}, {LIGHT_BLUE}, {AMBER});
    z-index:30;
}}

/* ── Logo — top left, large ── */
.logo-wrap {{
    position:absolute; top:32px; left:38px; z-index:25;
}}
.logo {{
    height:80px; opacity:0.92;
}}

/* ── Geometric accents ── */
.geo-ring {{
    position:absolute;
    border: 2px solid rgba(255,177,32,0.12);
    border-radius:50%;
    z-index:2;
}}
.gr-1 {{ width:180px; height:180px; top:60px; right:60px; }}
.gr-2 {{ width:100px; height:100px; bottom:120px; left:50px; border-color:rgba(95,167,229,0.1); }}
.gr-3 {{ width:60px; height:60px; top:200px; left:80px; border-color:rgba(91,146,145,0.12); }}

/* Small diamond shapes */
.diamond {{
    position:absolute;
    width:12px; height:12px;
    transform: rotate(45deg);
    z-index:3;
}}
.d-1 {{ top:140px; right:180px; background:{AMBER}; opacity:0.2; }}
.d-2 {{ bottom:200px; left:140px; background:{LIGHT_BLUE}; opacity:0.15; width:8px; height:8px; }}
.d-3 {{ top:320px; right:70px; background:{TEAL}; opacity:0.18; width:6px; height:6px; }}

/* Horizontal accent lines */
.h-line {{
    position:absolute;
    height:2px;
    border-radius:1px;
    z-index:3;
}}
.hl-1 {{
    width:80px; top:400px; left:55px;
    background: linear-gradient(90deg, {AMBER}, transparent);
    opacity:0.3;
}}
.hl-2 {{
    width:60px; top:680px; right:55px;
    background: linear-gradient(270deg, {LIGHT_BLUE}, transparent);
    opacity:0.25;
}}

/* ── Main text block — centered ── */
.text-zone {{
    position:absolute;
    top:0; left:0; right:0; bottom:0;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    z-index:10;
    padding: 0 70px;
    text-align:center;
}}

.line-break {{
    display:block;
}}

.headline {{
    font-family: Inter;
    font-size: 52px;
    font-weight: 700;
    color: white;
    line-height: 1.25;
    margin: 0;
}}

.headline .highlight {{
    color: {AMBER};
}}

.subtext {{
    font-family: DM Sans;
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    margin-top: 24px;
    line-height: 1.5;
}}
</style>
</head><body>
<div class="canvas">
    <div class="glow-warm"></div>
    <div class="glow-cool"></div>
    <div class="glow-teal"></div>
    <div class="top-bar"></div>

    <div class="geo-ring gr-1"></div>
    <div class="geo-ring gr-2"></div>
    <div class="geo-ring gr-3"></div>
    <div class="diamond d-1"></div>
    <div class="diamond d-2"></div>
    <div class="diamond d-3"></div>
    <div class="h-line hl-1"></div>
    <div class="h-line hl-2"></div>

    <div class="logo-wrap">{logo_img}</div>

    <div class="text-zone">
        <h1 class="headline">We took a break.<br><span class="line-break"><span class="highlight">We never stopped believing</span> in you.</span></h1>
        <p class="subtext">Your comeback story starts here.</p>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_1.png"))


def generate_slide2(campaign_dir):
    """Slide 2: Resilience - Rejection is redirection"""
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, #0f2035 0%, {DEEP_BLUE} 50%, #1a4a6e 100%);
}}

.top-bar {{
    position:absolute; top:0; left:0; right:0; height:5px;
    background: linear-gradient(90deg, {TEAL}, {MEDIUM_BLUE}, {LIGHT_BLUE}, {AMBER});
    z-index:30;
}}

.accent-shape {{
    position:absolute;
    background: rgba(255,177,32,0.08);
    border-radius: 50%;
    z-index:1;
}}
.shape-1 {{ width:400px; height:400px; top:-100px; right:-80px; }}
.shape-2 {{ width:250px; height:250px; bottom:-50px; left:40px; }}

.content {{
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    width:90%;
    z-index:10;
}}

.message {{
    font-family: Inter;
    font-size: 48px;
    font-weight: 700;
    color: white;
    text-align: center;
    line-height: 1.3;
    margin: 0;
}}

.message .highlight {{
    color: {AMBER};
}}

.detail {{
    font-family: DM Sans;
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    margin-top: 20px;
    text-align: center;
}}
</style>
</head><body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="accent-shape shape-1"></div>
    <div class="accent-shape shape-2"></div>

    <div class="content">
        <div class="message"><span class="highlight">Rejection</span> is redirection.</div>
        <div class="detail">Every "no" is pushing you toward your true "yes".</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_2.png"))


def generate_slide3(campaign_dir):
    """Slide 3: Progress is invisible"""
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, #162d4a 0%, {DEEP_BLUE} 100%);
}}

.top-bar {{
    position:absolute; top:0; left:0; right:0; height:5px;
    background: linear-gradient(90deg, {TEAL}, {MEDIUM_BLUE}, {LIGHT_BLUE}, {AMBER});
    z-index:30;
}}

.content {{
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    width:85%;
    z-index:10;
}}

.message {{
    font-family: Inter;
    font-size: 48px;
    font-weight: 700;
    color: white;
    text-align: center;
    line-height: 1.3;
    margin: 0;
}}

.message .highlight {{
    color: {AMBER};
}}

.detail {{
    font-family: DM Sans;
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    margin-top: 20px;
    text-align: center;
}}

.progress-bar {{
    width: 60%;
    height: 4px;
    background: rgba(255,255,255,0.2);
    border-radius: 2px;
    margin-top: 40px;
    overflow: hidden;
}}

.progress-fill {{
    height: 100%;
    background: linear-gradient(90deg, {AMBER}, {LIGHT_BLUE});
    width: 35%;
    animation: none;
}}
</style>
</head><body>
<div class="canvas">
    <div class="top-bar"></div>

    <div class="content">
        <div class="message"><span class="highlight">Progress</span> is invisible.</div>
        <div class="detail">You're growing even when it doesn't feel like it.</div>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_3.png"))


def generate_slide4(campaign_dir):
    """Slide 4: Comparison is a trap"""
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, {DEEP_BLUE} 0%, #162d4a 100%);
}}

.top-bar {{
    position:absolute; top:0; left:0; right:0; height:5px;
    background: linear-gradient(90deg, {TEAL}, {MEDIUM_BLUE}, {LIGHT_BLUE}, {AMBER});
    z-index:30;
}}

.content {{
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    width:85%;
    z-index:10;
}}

.message {{
    font-family: Inter;
    font-size: 48px;
    font-weight: 700;
    color: white;
    text-align: center;
    line-height: 1.3;
    margin: 0;
}}

.message .highlight {{
    color: {AMBER};
}}

.detail {{
    font-family: DM Sans;
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    margin-top: 20px;
    text-align: center;
}}
</style>
</head><body>
<div class="canvas">
    <div class="top-bar"></div>

    <div class="content">
        <div class="message">Stop <span class="highlight">comparing</span>.</div>
        <div class="detail">Your journey is uniquely yours. Comparison steals joy.</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_4.png"))


def generate_slide5(campaign_dir):
    """Slide 5: CTA - You've got this"""
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, #1e3d5e 0%, {DEEP_BLUE} 100%);
}}

.top-bar {{
    position:absolute; top:0; left:0; right:0; height:5px;
    background: linear-gradient(90deg, {TEAL}, {MEDIUM_BLUE}, {LIGHT_BLUE}, {AMBER});
    z-index:30;
}}

.glow {{
    position:absolute;
    width:600px; height:600px;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    border-radius:50%;
    background: radial-gradient(circle,
        rgba(255,177,32,0.1) 0%,
        transparent 70%
    );
    z-index:1;
    filter: blur(50px);
}}

.content {{
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    width:90%;
    z-index:10;
    text-align:center;
}}

.headline {{
    font-family: Inter;
    font-size: 52px;
    font-weight: 700;
    color: white;
    line-height: 1.3;
    margin: 0 0 30px 0;
}}

.headline .highlight {{
    color: {AMBER};
}}

.cta-button {{
    display:inline-block;
    background: {AMBER};
    color: {DEEP_BLUE};
    padding: 16px 40px;
    border-radius: 50px;
    font-family: Inter;
    font-weight: 700;
    font-size: 16px;
    text-decoration: none;
    margin-top: 20px;
}}

.url {{
    font-family: DM Sans;
    font-size: 14px;
    color: rgba(255,255,255,0.7);
    margin-top: 15px;
}}
</style>
</head><body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="glow"></div>

    <div class="content">
        <div class="headline">You've <span class="highlight">got</span> this.</div>
        <div class="url">www.internwise.co.uk</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_5.png"))


def generate(campaign_dir):
    """Generate all 5 slides."""
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating Comeback Carousel (Post 1)...")
    generate_slide1(campaign_dir)
    generate_slide2(campaign_dir)
    generate_slide3(campaign_dir)
    generate_slide4(campaign_dir)
    generate_slide5(campaign_dir)
    print("✓ Comeback carousel complete!")
