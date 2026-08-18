"""
Internwise — Confidence Tip Card (Gen Z Edition v2)
Post 7: Static Instagram tip card (1080x1080)

Design concept: Split canvas with high contrast
- TOP: Deep navy hero with massive "OWN IT." + 3D bolt
- BOTTOM: Cream section with chunky, large-text tip cards
- Maximum contrast between zones for readability
"""

import os
import base64
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

DEEP_BLUE = "#264D7E"
DARK_NAVY = "#162d4a"
AMBER = "#FFB120"
CORAL = "#FF6B6B"
SOFT_ORANGE = "#FF9961"
PURPLE = "#7B5CE6"
MINT = "#7FDBB6"
CREAM = "#FFF4E0"
OFF_WHITE = "#FAF5EC"


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


def generate(campaign_dir):
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
    background: {OFF_WHITE};
}}

/* Dark navy hero zone — top 50% */
.hero-zone {{
    position:absolute;
    top:0; left:0; right:0;
    height:540px;
    background: linear-gradient(135deg, {DEEP_BLUE} 0%, {DARK_NAVY} 70%, {PURPLE} 100%);
    z-index:1;
}}

/* Soft glow inside hero */
.glow {{
    position:absolute;
    top:-50px; right:-50px;
    width:500px; height:500px;
    background: radial-gradient(circle, rgba(255,177,32,0.25) 0%, transparent 60%);
    filter:blur(40px);
    z-index:2;
}}

/* Grain */
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 3px 3px;
    z-index:3;
}}

/* Logo top-left */
.logo {{
    position:absolute; top:44px; left:44px;
    height:72px; z-index:25; opacity:0.98;
}}

/* Sticker badge top-right */
.badge {{
    position:absolute; top:50px; right:50px;
    background: {AMBER}; color:{DEEP_BLUE};
    padding:12px 26px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:15px;
    letter-spacing:2px; text-transform:uppercase;
    transform: rotate(4deg);
    box-shadow: 0 8px 20px rgba(255,177,32,0.4);
    z-index:20;
}}

/* HERO CONTENT */
.hero-content {{
    position:absolute;
    top:130px; left:44px; right:44px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    z-index:15;
}}

.hero-text {{
    flex:1;
}}

.kicker {{
    font-family:DM Sans; font-weight:700;
    font-size:22px;
    color:{AMBER};
    text-transform:uppercase;
    letter-spacing:3px;
    margin-bottom:12px;
}}

.headline {{
    font-family:Inter; font-weight:700;
    font-size:160px; line-height:0.85;
    color:white;
    letter-spacing:-7px;
}}
.headline .it {{
    color:{AMBER};
    font-style:italic;
    text-shadow: 5px 5px 0 {CORAL};
}}
.headline .period {{
    color:{CORAL};
    font-size:170px;
}}

/* 3D Lightning bolt */
.bolt {{
    width:220px; height:220px;
    filter: drop-shadow(0 20px 40px rgba(255,177,32,0.4));
    transform: rotate(-5deg);
    flex-shrink:0;
}}

/* Sparkles */
.sparkle {{
    position:absolute;
    z-index:14;
}}
.sparkle-1 {{ top:100px; right:290px; }}
.sparkle-2 {{ top:380px; right:60px; }}
.sparkle-3 {{ top:300px; right:380px; }}

/* Curved divider between zones */
.divider {{
    position:absolute;
    top:510px; left:0; right:0;
    height:60px;
    background:{OFF_WHITE};
    border-radius:50% 50% 0 0 / 100% 100% 0 0;
    z-index:5;
}}

/* TIPS */
.tips {{
    position:absolute;
    top:555px; left:40px; right:40px;
    display:flex;
    flex-direction:column;
    gap:10px;
    z-index:15;
}}

.tip {{
    background: white;
    border: 3px solid {DEEP_BLUE};
    border-radius:18px;
    padding:12px 18px;
    display:flex;
    align-items:center;
    gap:16px;
    box-shadow: 6px 6px 0 {DEEP_BLUE};
}}

.tip-num {{
    width:52px; height:52px;
    border-radius:50%;
    background: linear-gradient(135deg, {AMBER}, #ff8c00);
    color:{DEEP_BLUE};
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:Inter; font-weight:700; font-size:24px;
    flex-shrink:0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}}

.tip-emoji {{
    font-size:34px;
    flex-shrink:0;
}}

.tip-text {{
    font-family:DM Sans; font-weight:600;
    font-size:25px;
    color:{DEEP_BLUE};
    line-height:1.25;
    flex:1;
}}
.tip-text strong {{
    color:{CORAL};
    font-weight:700;
}}

/* Bottom CTA */
.cta {{
    position:absolute;
    bottom:24px; left:44px; right:44px;
    background:{DEEP_BLUE};
    border-radius:18px;
    padding:16px 22px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    z-index:20;
    box-shadow: 5px 5px 0 {DARK_NAVY};
    border:3px solid {DARK_NAVY};
}}
.cta-action {{
    font-family:Inter; font-weight:700;
    font-size:20px; color:white;
    line-height:1.2;
}}
.cta-url {{
    font-family:Inter; font-weight:700;
    font-size:17px;
    color:{AMBER};
    margin-top:3px;
    letter-spacing:-0.3px;
}}
.cta-arrow {{
    width:52px; height:52px;
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
    <div class="hero-zone">
        <div class="glow"></div>
        <div class="grain"></div>
    </div>

    {logo_img}
    <div class="badge">You got this</div>

    <div class="hero-content">
        <div class="hero-text">
            <div class="kicker">Confidence = unlocked</div>
            <div class="headline">
                OWN<br>
                <span class="it">IT</span><span class="period">.</span>
            </div>
        </div>
        <svg class="bolt" viewBox="0 0 120 120">
            <defs>
                <linearGradient id="bolt-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FFE082"/>
                    <stop offset="50%" stop-color="{AMBER}"/>
                    <stop offset="100%" stop-color="#E89000"/>
                </linearGradient>
                <linearGradient id="bolt-shadow" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#c97d00"/>
                    <stop offset="100%" stop-color="#8a5500"/>
                </linearGradient>
            </defs>
            <!-- Bolt shadow (back layer for 3D depth) -->
            <path d="M 58 12 L 22 62 L 48 62 L 38 108 L 82 52 L 56 52 L 70 12 Z"
                  fill="url(#bolt-shadow)" transform="translate(5,5)"/>
            <!-- Main bolt -->
            <path d="M 58 12 L 22 62 L 48 62 L 38 108 L 82 52 L 56 52 L 70 12 Z"
                  fill="url(#bolt-grad)"
                  stroke="white" stroke-width="3" stroke-linejoin="round"/>
            <!-- Highlight shine -->
            <path d="M 58 18 L 32 58 L 45 58 L 40 90" stroke="rgba(255,255,255,0.55)" stroke-width="4" fill="none" stroke-linecap="round"/>
        </svg>
    </div>

    <svg class="sparkle sparkle-1" width="32" height="32" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="white"/>
    </svg>
    <svg class="sparkle sparkle-2" width="26" height="26" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{AMBER}"/>
    </svg>
    <svg class="sparkle sparkle-3" width="20" height="20" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{MINT}"/>
    </svg>

    <div class="divider"></div>

    <div class="tips">
        <div class="tip">
            <div class="tip-num">1</div>
            <div class="tip-emoji">🎤</div>
            <div class="tip-text"><strong>Pitch yourself</strong> in 30 seconds flat</div>
        </div>
        <div class="tip">
            <div class="tip-num">2</div>
            <div class="tip-emoji">⭐</div>
            <div class="tip-text">Use the <strong>STAR method</strong> for stories</div>
        </div>
        <div class="tip">
            <div class="tip-num">3</div>
            <div class="tip-emoji">👔</div>
            <div class="tip-text"><strong>Dress</strong> for the role you want</div>
        </div>
        <div class="tip">
            <div class="tip-num">4</div>
            <div class="tip-emoji">💪</div>
            <div class="tip-text"><strong>Flex</strong> without apologies</div>
        </div>
    </div>

    <div class="cta">
        <div>
            <div class="cta-action">Find roles that match your confidence</div>
            <div class="cta-url">internwise.co.uk →</div>
        </div>
        <div class="cta-arrow">
            <svg width="22" height="22" viewBox="0 0 22 22">
                <path d="M 4 11 L 16 11 M 12 6 L 17 11 L 12 16" stroke="{DEEP_BLUE}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
</div>
</body></html>
"""

    os.makedirs(campaign_dir, exist_ok=True)
    _render(html, os.path.join(campaign_dir, "tipcard_confidence.png"))
    print("✓ Confidence tip card complete!")
