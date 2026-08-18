"""
Internwise — Networking 101 Carousel (Gen Z Edition)
Post 6: 5-slide Instagram carousel (1080x1080)

Design concept: "Scroll-Stopping Gen Z"
- MASSIVE typography that dominates
- 3D-styled illustrations with depth & gradients
- Sticker-style layered elements
- Asymmetric, dynamic compositions
- Hand-drawn accents (arrows, scribbles, circles)
- Bold color blocks & vibrant gradients
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
CORAL = "#FF6B6B"
PURPLE = "#7B5CE6"
MINT = "#7FDBB6"
CREAM = "#FFF4E0"


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


# ============================================================
# SLIDE 1 — HOOK: "Network Like A Pro"
# Bold, scroll-stopping with massive type + 3D floating orbs
# ============================================================
def generate_slide1(campaign_dir):
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
    background: linear-gradient(135deg, {DEEP_BLUE} 0%, #1a3d5e 60%, {PURPLE} 100%);
}}

/* Grain overlay */
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px);
    background-size: 3px 3px;
    z-index:2;
}}

/* Floating 3D orbs */
.orb {{
    position:absolute; border-radius:50%;
    filter: blur(1px);
}}
.orb-1 {{
    width:260px; height:260px;
    top:-80px; right:-80px;
    background: radial-gradient(circle at 30% 30%, {AMBER}, #ff8c00);
    box-shadow: 0 20px 60px rgba(255,140,0,0.4);
}}
.orb-2 {{
    width:160px; height:160px;
    bottom:120px; left:-30px;
    background: radial-gradient(circle at 30% 30%, {CORAL}, #c94545);
    box-shadow: 0 20px 60px rgba(255,107,107,0.4);
}}
.orb-3 {{
    width:100px; height:100px;
    top:250px; left:80px;
    background: radial-gradient(circle at 30% 30%, {MINT}, #4db793);
    box-shadow: 0 10px 30px rgba(127,219,182,0.4);
}}

/* Top badge */
.badge {{
    position:absolute; top:50px; right:60px;
    background: {AMBER}; color:{DEEP_BLUE};
    padding:12px 26px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:16px;
    letter-spacing:1px; text-transform:uppercase;
    transform: rotate(3deg);
    box-shadow: 0 8px 20px rgba(255,177,32,0.4);
    z-index:15;
}}

.logo {{ position:absolute; top:44px; left:44px; height:72px; opacity:0.95; z-index:25; }}

/* Massive headline */
.headline-wrap {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    text-align:center; z-index:20;
    width:100%;
}}

.headline {{
    font-family:Inter; font-weight:700;
    font-size:160px; line-height:0.9;
    color:white; letter-spacing:-6px;
    text-shadow: 0 6px 30px rgba(0,0,0,0.3);
}}
.headline .line1 {{ display:block; }}
.headline .line2 {{
    display:block;
    color:{AMBER};
    font-style:italic;
    transform:translateX(20px);
}}

/* Scribble underline */
.scribble {{
    position:absolute;
    bottom:-20px; left:50%;
    transform:translateX(-50%);
    width:400px; height:30px;
}}

/* Tagline sticker */
.tagline {{
    position:absolute;
    bottom:140px; left:50%;
    transform:translateX(-50%) rotate(-1deg);
    background:white;
    padding:18px 40px;
    border-radius:60px;
    font-family:DM Sans; font-weight:700; font-size:24px;
    color:{DEEP_BLUE};
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    z-index:20;
    white-space:nowrap;
}}
.tagline em {{
    font-style:italic; color:{CORAL};
    font-weight:700;
}}

/* Corner arrow */
.corner-arrow {{
    position:absolute;
    bottom:60px; right:60px;
    z-index:20;
}}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>

    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    {logo_img}
    <div class="badge">The Real Talk</div>

    <div class="headline-wrap">
        <div class="headline">
            <span class="line1">NETWORK</span>
            <span class="line2">like a pro</span>
        </div>
    </div>

    <div class="tagline">no <em>cringe</em> required</div>

    <svg class="corner-arrow" width="80" height="80" viewBox="0 0 80 80">
        <path d="M 20 20 Q 40 50 60 60" stroke="{AMBER}" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M 50 55 L 60 60 L 55 50" stroke="{AMBER}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_1.png"))


# ============================================================
# SLIDE 2 — "YOUR PEOPLE" (Start With Who You Know)
# Split composition, huge text, 3D avatar cluster
# ============================================================
def generate_slide2(campaign_dir):
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
    background: {CREAM};
}}

/* Diagonal color block */
.block {{
    position:absolute;
    top:-100px; right:-200px;
    width:900px; height:900px;
    background: linear-gradient(135deg, {CORAL} 0%, #ff8c00 100%);
    transform: rotate(18deg);
    border-radius:80px;
    box-shadow: 0 20px 80px rgba(255,107,107,0.3);
    z-index:1;
}}

/* Number sticker */
.number {{
    position:absolute;
    top:70px; left:70px;
    width:110px; height:110px;
    background: {DEEP_BLUE};
    color:white;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:Inter; font-weight:700; font-size:56px;
    transform:rotate(-8deg);
    box-shadow: 0 10px 30px rgba(38,77,126,0.3);
    z-index:20;
}}

/* Main heading */
.main-text {{
    position:absolute;
    top:240px; left:60px;
    z-index:15;
    width:600px;
}}
.kicker {{
    font-family:DM Sans; font-weight:700;
    font-size:26px; color:{DEEP_BLUE};
    text-transform:uppercase;
    letter-spacing:3px;
    margin-bottom:15px;
}}
.headline {{
    font-family:Inter; font-weight:700;
    font-size:130px; line-height:0.9;
    color:{DEEP_BLUE};
    letter-spacing:-5px;
}}
.headline .highlight {{
    display:inline-block;
    background:{AMBER};
    color:{DEEP_BLUE};
    padding:0 14px;
    transform:rotate(-2deg);
    box-shadow: 0 8px 20px rgba(255,177,32,0.4);
}}

/* Bottom explainer */
.explainer {{
    position:absolute;
    bottom:70px; left:60px;
    right:60px;
    font-family:DM Sans; font-weight:500;
    font-size:30px; line-height:1.3;
    color:{DEEP_BLUE};
    z-index:15;
    max-width:620px;
}}
.explainer strong {{
    color:{CORAL};
    font-weight:700;
}}

/* 3D people cluster (right side) */
.people-cluster {{
    position:absolute;
    top:220px; right:60px;
    z-index:12;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.25));
}}

/* Sparkle */
.sparkle {{
    position:absolute;
    z-index:14;
    animation: none;
}}
.sparkle-1 {{ top:180px; right:100px; }}
.sparkle-2 {{ bottom:280px; right:380px; }}
</style>
</head><body>
<div class="canvas">
    <div class="block"></div>

    <div class="number">1</div>

    <div class="main-text">
        <div class="kicker">Rule #1</div>
        <div class="headline">
            YOUR<br>
            <span class="highlight">PEOPLE</span>
        </div>
    </div>

    <svg class="people-cluster" width="380" height="380" viewBox="0 0 120 120">
        <defs>
            <radialGradient id="p1" cx="30%" cy="30%">
                <stop offset="0%" stop-color="{LIGHT_BLUE}"/>
                <stop offset="100%" stop-color="{DEEP_BLUE}"/>
            </radialGradient>
            <radialGradient id="p2" cx="30%" cy="30%">
                <stop offset="0%" stop-color="{AMBER}"/>
                <stop offset="100%" stop-color="#cc8b00"/>
            </radialGradient>
            <radialGradient id="p3" cx="30%" cy="30%">
                <stop offset="0%" stop-color="{MINT}"/>
                <stop offset="100%" stop-color="#4db793"/>
            </radialGradient>
            <radialGradient id="p4" cx="30%" cy="30%">
                <stop offset="0%" stop-color="{PURPLE}"/>
                <stop offset="100%" stop-color="#5d3fc4"/>
            </radialGradient>
        </defs>
        <!-- Avatar 1 (back) -->
        <circle cx="40" cy="40" r="22" fill="url(#p1)"/>
        <path d="M 18 75 Q 18 62 40 62 Q 62 62 62 75 L 62 90 L 18 90 Z" fill="url(#p1)"/>
        <!-- Avatar 2 (front-right) -->
        <circle cx="80" cy="50" r="24" fill="url(#p2)"/>
        <path d="M 56 90 Q 56 75 80 75 Q 104 75 104 90 L 104 105 L 56 105 Z" fill="url(#p2)"/>
        <!-- Avatar 3 (small left) -->
        <circle cx="22" cy="78" r="15" fill="url(#p3)"/>
        <!-- Avatar 4 (small top) -->
        <circle cx="62" cy="15" r="12" fill="url(#p4)"/>
    </svg>

    <svg class="sparkle sparkle-1" width="40" height="40" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{AMBER}"/>
    </svg>
    <svg class="sparkle sparkle-2" width="30" height="30" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="white"/>
    </svg>

    <div class="explainer">
        Friends, family, old classmates — they're your <strong>unfair advantage</strong>. Tell them you're looking.
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_2.png"))


# ============================================================
# SLIDE 3 — "GIVE FIRST." (Give Before You Ask)
# Dark background, massive text, 3D gift box
# ============================================================
def generate_slide3(campaign_dir):
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
    background: linear-gradient(160deg, #0f1e33 0%, {DEEP_BLUE} 100%);
}}

/* Soft glow */
.glow {{
    position:absolute;
    top:40%; left:50%;
    transform:translate(-50%,-50%);
    width:700px; height:700px;
    background: radial-gradient(circle, rgba(255,177,32,0.25) 0%, transparent 60%);
    filter:blur(40px);
    z-index:1;
}}

/* Number sticker */
.number {{
    position:absolute;
    top:70px; left:70px;
    width:110px; height:110px;
    background: {AMBER};
    color:{DEEP_BLUE};
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:Inter; font-weight:700; font-size:56px;
    transform:rotate(8deg);
    box-shadow: 0 10px 30px rgba(255,177,32,0.4);
    z-index:20;
}}

.kicker {{
    position:absolute;
    top:95px; left:220px;
    font-family:DM Sans; font-weight:700;
    font-size:26px; color:rgba(255,255,255,0.6);
    text-transform:uppercase;
    letter-spacing:3px;
    z-index:15;
}}

/* Main text */
.headline {{
    position:absolute;
    top:260px; left:60px;
    font-family:Inter; font-weight:700;
    font-size:180px; line-height:0.88;
    color:white; letter-spacing:-8px;
    z-index:15;
}}
.headline .give {{
    color:{AMBER};
    font-style:italic;
}}
.headline .period {{
    color:{CORAL};
    font-size:200px;
}}

/* 3D gift box */
.gift {{
    position:absolute;
    top:200px; right:60px;
    z-index:12;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.4));
    transform:rotate(-5deg);
}}

/* Sparkles */
.sparkle {{
    position:absolute;
    z-index:14;
}}
.sparkle-1 {{ top:140px; right:380px; }}
.sparkle-2 {{ top:440px; right:40px; }}
.sparkle-3 {{ top:280px; right:440px; }}

/* Explainer card */
.card {{
    position:absolute;
    bottom:60px; left:60px; right:60px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(255,255,255,0.15);
    border-radius: 24px;
    padding:28px 32px;
    font-family:DM Sans; font-weight:500;
    font-size:28px; line-height:1.4;
    color:white;
    z-index:15;
}}
.card strong {{
    color:{AMBER};
    font-weight:700;
}}
.arrow-emoji {{
    display:inline-block;
    font-size:32px;
    margin-right:8px;
}}
</style>
</head><body>
<div class="canvas">
    <div class="glow"></div>

    <div class="number">2</div>
    <div class="kicker">Rule #2</div>

    <div class="headline">
        <span class="give">GIVE</span><br>
        FIRST<span class="period">.</span>
    </div>

    <svg class="gift" width="340" height="340" viewBox="0 0 120 120">
        <defs>
            <linearGradient id="box-top" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{CORAL}"/>
                <stop offset="100%" stop-color="#d94545"/>
            </linearGradient>
            <linearGradient id="box-bot" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{AMBER}"/>
                <stop offset="100%" stop-color="#cc8b00"/>
            </linearGradient>
            <linearGradient id="ribbon" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="{MINT}"/>
                <stop offset="100%" stop-color="#4db793"/>
            </linearGradient>
        </defs>
        <!-- Box body -->
        <rect x="18" y="55" width="84" height="55" rx="4" fill="url(#box-bot)"/>
        <!-- Box lid -->
        <rect x="14" y="42" width="92" height="18" rx="3" fill="url(#box-top)"/>
        <!-- Vertical ribbon -->
        <rect x="55" y="42" width="10" height="68" fill="url(#ribbon)"/>
        <!-- Horizontal ribbon -->
        <rect x="14" y="47" width="92" height="8" fill="url(#ribbon)"/>
        <!-- Bow -->
        <path d="M 45 38 Q 35 25 40 20 Q 55 22 60 38" fill="url(#ribbon)"/>
        <path d="M 75 38 Q 85 25 80 20 Q 65 22 60 38" fill="url(#ribbon)"/>
        <circle cx="60" cy="38" r="5" fill="url(#ribbon)"/>
        <!-- Shine -->
        <rect x="20" y="58" width="10" height="40" fill="rgba(255,255,255,0.3)" rx="2"/>
    </svg>

    <svg class="sparkle sparkle-1" width="36" height="36" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{AMBER}"/>
    </svg>
    <svg class="sparkle sparkle-2" width="26" height="26" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{MINT}"/>
    </svg>
    <svg class="sparkle sparkle-3" width="20" height="20" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="white"/>
    </svg>

    <div class="card">
        <span class="arrow-emoji">💡</span>Share articles. Make intros. Help people <strong>before</strong> you need anything.
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_3.png"))


# ============================================================
# SLIDE 4 — "LINKEDIN CHEAT CODES" (LinkedIn Moves)
# Grid/card layout with bold headers + emoji checklist
# ============================================================
def generate_slide4(campaign_dir):
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
    background: linear-gradient(180deg, #e8f0f7 0%, {CREAM} 100%);
}}

/* Blob shapes */
.blob-1 {{
    position:absolute;
    top:-100px; left:-100px;
    width:400px; height:400px;
    background: {PURPLE};
    border-radius:50% 40% 60% 50%;
    opacity:0.12;
    filter: blur(20px);
}}
.blob-2 {{
    position:absolute;
    bottom:-80px; right:-80px;
    width:350px; height:350px;
    background: {AMBER};
    border-radius:60% 40% 50% 50%;
    opacity:0.2;
    filter: blur(20px);
}}

/* Number sticker */
.number {{
    position:absolute;
    top:70px; left:70px;
    width:110px; height:110px;
    background: {DEEP_BLUE};
    color:white;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:Inter; font-weight:700; font-size:56px;
    transform:rotate(-5deg);
    box-shadow: 0 10px 30px rgba(38,77,126,0.3);
    z-index:20;
}}

/* Headline */
.headline-wrap {{
    position:absolute;
    top:210px; left:60px; right:60px;
    z-index:15;
    display:flex;
    align-items:flex-start;
    gap:24px;
}}
.headline-text {{
    flex:1;
}}
.kicker {{
    font-family:DM Sans; font-weight:700;
    font-size:26px; color:{DEEP_BLUE};
    text-transform:uppercase;
    letter-spacing:3px;
    margin-bottom:10px;
}}
.headline {{
    font-family:Inter; font-weight:700;
    font-size:92px; line-height:0.9;
    color:{DEEP_BLUE};
    letter-spacing:-4px;
}}
.headline .cheat {{
    color:white;
    background:{DEEP_BLUE};
    padding:0 16px;
    display:inline-block;
    transform:rotate(-1deg);
    font-style:italic;
}}

/* LinkedIn logo */
.linkedin-badge {{
    width:130px; height:130px;
    background:#0A66C2;
    border-radius:28px;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow: 8px 8px 0 {DEEP_BLUE};
    transform:rotate(4deg);
    flex-shrink:0;
    margin-top:20px;
}}
.linkedin-badge svg {{ width:70px; height:70px; }}

/* Cards */
.cards {{
    position:absolute;
    top:530px; left:60px; right:60px;
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap:18px;
    z-index:15;
}}
.card {{
    background:white;
    border: 3px solid {DEEP_BLUE};
    border-radius:20px;
    padding:20px 22px;
    display:flex;
    align-items:center;
    gap:14px;
    box-shadow: 6px 6px 0 {DEEP_BLUE};
}}
.card-icon {{
    font-size:42px;
    flex-shrink:0;
}}
.card-text {{
    font-family:DM Sans; font-weight:700;
    font-size:20px;
    color:{DEEP_BLUE};
    line-height:1.2;
}}
.card-text span {{
    color:{CORAL};
    font-weight:700;
}}
</style>
</head><body>
<div class="canvas">
    <div class="blob-1"></div>
    <div class="blob-2"></div>

    <div class="number">3</div>

    <div class="headline-wrap">
        <div class="headline-text">
            <div class="kicker">Rule #3</div>
            <div class="headline">
                LINKEDIN<br>
                <span class="cheat">cheat codes</span>
            </div>
        </div>
        <div class="linkedin-badge">
            <svg viewBox="0 0 24 24" fill="white">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.063 2.063 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
        </div>
    </div>

    <div class="cards">
        <div class="card">
            <div class="card-icon">💬</div>
            <div class="card-text"><span>Personalize</span> every DM</div>
        </div>
        <div class="card">
            <div class="card-icon">🔥</div>
            <div class="card-text"><span>Comment</span> on hiring posts</div>
        </div>
        <div class="card">
            <div class="card-icon">📢</div>
            <div class="card-text"><span>Engage</span> with companies</div>
        </div>
        <div class="card">
            <div class="card-icon">🤝</div>
            <div class="card-text"><span>Join</span> industry groups</div>
        </div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_4.png"))


# ============================================================
# SLIDE 5 — "JUST SEND IT." (Send The Message)
# High energy CTA, paper plane blasting across, motion feel
# ============================================================
def generate_slide5(campaign_dir):
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
    background: linear-gradient(135deg, {CORAL} 0%, {AMBER} 100%);
}}

/* Diagonal motion lines */
.motion-line {{
    position:absolute;
    height:8px;
    background:rgba(255,255,255,0.3);
    border-radius:4px;
    transform:rotate(-20deg);
}}
.ml-1 {{ top:180px; left:-50px; width:300px; }}
.ml-2 {{ top:250px; left:-50px; width:200px; opacity:0.5; }}
.ml-3 {{ top:320px; left:-50px; width:150px; opacity:0.3; }}

/* Grain */
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(0,0,0,0.05) 1px, transparent 1px);
    background-size: 3px 3px;
    z-index:2;
}}

.logo {{
    position:absolute; top:44px; left:44px;
    height:72px; z-index:25;
    filter: brightness(0) saturate(100%) invert(18%) sepia(34%) saturate(1289%) hue-rotate(183deg) brightness(94%) contrast(91%);
}}

/* Paper plane massive */
.plane {{
    position:absolute;
    top:170px; right:-30px;
    z-index:10;
    filter: drop-shadow(0 25px 40px rgba(0,0,0,0.25));
    transform:rotate(-15deg);
}}

/* Main headline */
.headline-wrap {{
    position:absolute;
    top:480px; left:60px;
    z-index:15;
}}
.headline {{
    font-family:Inter; font-weight:700;
    font-size:200px; line-height:0.85;
    color:{DEEP_BLUE};
    letter-spacing:-10px;
}}
.headline .just {{
    display:block;
    font-style:italic;
    font-size:110px;
    color:white;
    letter-spacing:-4px;
    margin-bottom:10px;
}}
.headline .send {{
    display:block;
    text-shadow: 6px 6px 0 {CORAL};
}}
.headline .period {{
    color:white;
    text-shadow: 6px 6px 0 {CORAL};
}}

/* CTA card */
.cta {{
    position:absolute;
    bottom:60px; left:60px; right:60px;
    background:{DEEP_BLUE};
    color:white;
    padding:28px 36px;
    border-radius:24px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    z-index:15;
}}
.cta-text {{
    font-family:DM Sans; font-weight:700;
    font-size:22px;
    line-height:1.3;
}}
.cta-url {{
    font-family:Inter; font-weight:700;
    font-size:30px;
    color:{AMBER};
    margin-top:8px;
    display:block;
    letter-spacing:-0.5px;
}}
.cta-arrow {{
    width:70px; height:70px;
    background:{AMBER};
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-shrink:0;
}}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>

    <div class="motion-line ml-1"></div>
    <div class="motion-line ml-2"></div>
    <div class="motion-line ml-3"></div>

    {logo_img}

    <svg class="plane" width="620" height="500" viewBox="0 0 120 100">
        <defs>
            <linearGradient id="plane-main" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="white"/>
                <stop offset="100%" stop-color="#e8e8e8"/>
            </linearGradient>
            <linearGradient id="plane-shadow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#d0d0d0"/>
                <stop offset="100%" stop-color="#a8a8a8"/>
            </linearGradient>
        </defs>
        <!-- Plane body (top wing) -->
        <path d="M 10 50 L 110 15 L 65 55 Z" fill="url(#plane-main)"/>
        <!-- Plane body (bottom wing) -->
        <path d="M 10 50 L 65 55 L 50 85 Z" fill="url(#plane-shadow)"/>
        <!-- Center fold -->
        <path d="M 10 50 L 65 55 L 110 15" stroke="rgba(0,0,0,0.15)" stroke-width="1" fill="none"/>
    </svg>

    <div class="headline-wrap">
        <div class="headline">
            <span class="just">just</span>
            <span class="send">SEND<span class="period">.</span></span>
        </div>
    </div>

    <div class="cta">
        <div class="cta-text">
            Stop waiting. Start your journey.
            <span class="cta-url">www.internwise.co.uk</span>
        </div>
        <div class="cta-arrow">
            <svg width="36" height="36" viewBox="0 0 36 36">
                <path d="M 8 18 L 26 18 M 20 10 L 28 18 L 20 26" stroke="{DEEP_BLUE}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_5.png"))


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating Networking Carousel (Gen Z Edition)...")
    generate_slide1(campaign_dir)
    generate_slide2(campaign_dir)
    generate_slide3(campaign_dir)
    generate_slide4(campaign_dir)
    generate_slide5(campaign_dir)
    print("✓ Networking carousel complete!")
