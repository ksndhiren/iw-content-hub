"""
Internwise — AI Jobs Carousel (Gen Z Edition v3)
Post 8: 4-slide Instagram carousel (1080x1080)

Design concept: Thematic illustrations per role
- Slide 1: Real Pexels photo — excited professional at laptop (hook)
- Slide 2: Neural network / brain SVG  — AI/ML Engineer
- Slide 3: Data dashboard HTML/CSS     — Data Analyst
- Slide 4: Floating prompt bubbles     — Prompt Engineer
"""

import os
import base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_cutout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

DEEP_BLUE = "#264D7E"
DARK_NAVY = "#162d4a"
AMBER = "#FFB120"
CORAL = "#FF6B6B"
PURPLE = "#7B5CE6"
MINT = "#7FDBB6"
CREAM = "#FFF4E0"
OFF_WHITE = "#FAF5EC"
LIGHT_BLUE = "#5FA7E5"


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


def _fetch_hook_photo():
    """Only slide 1 uses a real photo."""
    print("  ↓ Fetching hook photo...")
    path = get_cutout("tech startup professional portrait confident", index=1, orientation="portrait")
    print(f"    ✓ hook: {path}")
    return path


# ── Thematic illustrations ────────────────────────────────────────────────────

def _make_neural_net():
    """Glowing neural network SVG — AI/ML Engineer. Brain is the hero."""
    # Hub at (290, 400) in 560×680 viewBox, inner ring r=180
    return f"""
<svg style="position:absolute;bottom:0;left:0;width:100%;height:100%;"
     viewBox="0 0 560 680" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="hubGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{AMBER}" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
    </radialGradient>
    <filter id="nGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Wide ambient glow behind brain -->
  <circle cx="290" cy="400" r="200" fill="url(#hubGlow)"/>

  <!-- Hub → inner ring lines (r=180, 6 nodes) -->
  <!-- top:        (290, 220) -->
  <!-- top-right:  (290+156, 310) = (446, 310) -->
  <!-- bot-right:  (446, 490) -->
  <!-- bottom:     (290, 580) -->
  <!-- bot-left:   (134, 490) -->
  <!-- top-left:   (134, 310) -->
  <line x1="290" y1="400" x2="290" y2="220" stroke="rgba(255,177,32,0.6)"  stroke-width="2.5"/>
  <line x1="290" y1="400" x2="446" y2="310" stroke="rgba(255,177,32,0.55)" stroke-width="2"/>
  <line x1="290" y1="400" x2="446" y2="490" stroke="rgba(255,177,32,0.55)" stroke-width="2"/>
  <line x1="290" y1="400" x2="290" y2="580" stroke="rgba(255,177,32,0.45)" stroke-width="2"/>
  <line x1="290" y1="400" x2="134" y2="490" stroke="rgba(255,177,32,0.55)" stroke-width="2"/>
  <line x1="290" y1="400" x2="134" y2="310" stroke="rgba(255,177,32,0.6)"  stroke-width="2.5"/>

  <!-- Ring mesh -->
  <line x1="290" y1="220" x2="446" y2="310" stroke="rgba(255,177,32,0.28)" stroke-width="1.5"/>
  <line x1="446" y1="310" x2="446" y2="490" stroke="rgba(255,177,32,0.28)" stroke-width="1.5"/>
  <line x1="446" y1="490" x2="290" y2="580" stroke="rgba(255,177,32,0.28)" stroke-width="1.5"/>
  <line x1="290" y1="580" x2="134" y2="490" stroke="rgba(255,177,32,0.28)" stroke-width="1.5"/>
  <line x1="134" y1="490" x2="134" y2="310" stroke="rgba(255,177,32,0.28)" stroke-width="1.5"/>
  <line x1="134" y1="310" x2="290" y2="220" stroke="rgba(255,177,32,0.28)" stroke-width="1.5"/>

  <!-- Skip connections -->
  <line x1="290" y1="220" x2="446" y2="490" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="446" y1="310" x2="290" y2="580" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="446" y1="310" x2="134" y2="490" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="290" y1="220" x2="134" y2="490" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  <line x1="134" y1="310" x2="446" y2="490" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>

  <!-- Tentacles into dark area -->
  <line x1="290" y1="220" x2="255" y2="90"  stroke="rgba(255,255,255,0.22)" stroke-width="1.5"/>
  <line x1="290" y1="220" x2="370" y2="80"  stroke="rgba(255,255,255,0.16)" stroke-width="1"/>
  <line x1="446" y1="310" x2="530" y2="200" stroke="rgba(255,255,255,0.16)" stroke-width="1"/>
  <line x1="134" y1="310" x2="56"  y2="200" stroke="rgba(255,255,255,0.16)" stroke-width="1"/>
  <line x1="134" y1="310" x2="42"  y2="370" stroke="rgba(255,255,255,0.14)" stroke-width="1"/>

  <!-- Outer micro-nodes -->
  <circle cx="255" cy="90"  r="9"  fill="rgba(255,177,32,0.8)"/>
  <circle cx="370" cy="80"  r="7"  fill="rgba(255,255,255,0.55)"/>
  <circle cx="530" cy="200" r="8"  fill="rgba(255,177,32,0.7)"/>
  <circle cx="56"  cy="200" r="8"  fill="rgba(255,255,255,0.55)"/>
  <circle cx="42"  cy="370" r="7"  fill="rgba(255,177,32,0.65)"/>

  <!-- Inner ring nodes — white for contrast against amber arch -->
  <circle cx="290" cy="220" r="22" fill="white" filter="url(#nGlow)" opacity="0.95"/>
  <circle cx="446" cy="310" r="19" fill="white" filter="url(#nGlow)" opacity="0.9"/>
  <circle cx="446" cy="490" r="19" fill="white" filter="url(#nGlow)" opacity="0.9"/>
  <circle cx="290" cy="580" r="17" fill="white" filter="url(#nGlow)" opacity="0.8"/>
  <circle cx="134" cy="490" r="19" fill="white" filter="url(#nGlow)" opacity="0.9"/>
  <circle cx="134" cy="310" r="22" fill="white" filter="url(#nGlow)" opacity="0.95"/>

  <!-- DOMINANT BRAIN — the hero of this slide -->
  <!-- Outer glow ring -->
  <circle cx="290" cy="400" r="148" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="3"/>
  <circle cx="290" cy="400" r="140" fill="white" opacity="0.96"/>
  <circle cx="290" cy="400" r="130" fill="{DEEP_BLUE}"/>
  <!-- Brain emoji, very large -->
  <text x="290" y="440" text-anchor="middle" dominant-baseline="auto" font-size="130">🧠</text>
</svg>"""


def _make_dashboard():
    """Mini data dashboard — Data Analyst."""
    return f"""
<div style="position:absolute;bottom:28px;right:8px;width:440px;height:516px;
            display:flex;flex-direction:column;gap:12px;padding:14px;">

  <!-- Main chart card -->
  <div style="background:white;border:3px solid {DEEP_BLUE};border-radius:20px;
              padding:18px 18px 14px;box-shadow:6px 6px 0 {DEEP_BLUE};flex:1;">

    <div style="font:700 13px/1 Inter,sans-serif;color:{DEEP_BLUE};
                text-transform:uppercase;letter-spacing:2px;margin-bottom:14px;">
      Performance Overview
    </div>

    <!-- Bar chart -->
    <div style="display:flex;align-items:flex-end;gap:8px;height:128px;margin-bottom:12px;padding:0 2px;">
      <div style="flex:1;height:57%;background:linear-gradient(180deg,{CORAL},{DEEP_BLUE});border-radius:5px 5px 0 0;"></div>
      <div style="flex:1;height:83%;background:linear-gradient(180deg,{AMBER},#d97d00);border-radius:5px 5px 0 0;"></div>
      <div style="flex:1;height:42%;background:linear-gradient(180deg,{PURPLE},{DEEP_BLUE});border-radius:5px 5px 0 0;"></div>
      <div style="flex:1;height:100%;background:linear-gradient(180deg,{CORAL},{DEEP_BLUE});border-radius:5px 5px 0 0;"></div>
      <div style="flex:1;height:67%;background:linear-gradient(180deg,{MINT},#2ea87a);border-radius:5px 5px 0 0;"></div>
      <div style="flex:1;height:89%;background:linear-gradient(180deg,{AMBER},#d97d00);border-radius:5px 5px 0 0;"></div>
    </div>

    <!-- Trend line -->
    <svg width="100%" height="42" viewBox="0 0 380 42">
      <defs>
        <linearGradient id="tFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{AMBER}" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <polyline points="0,38 60,30 120,20 180,25 240,13 300,8 380,4"
                stroke="{AMBER}" stroke-width="3" fill="none"
                stroke-linecap="round" stroke-linejoin="round"/>
      <polyline points="0,38 60,30 120,20 180,25 240,13 300,8 380,4 380,42 0,42"
                fill="url(#tFill)"/>
      <circle cx="380" cy="4" r="5" fill="{AMBER}"/>
    </svg>
  </div>

  <!-- Metric pills -->
  <div style="display:flex;gap:10px;">
    <div style="flex:1;background:{DEEP_BLUE};border-radius:14px;padding:12px 6px;text-align:center;">
      <div style="font:800 26px/1 Inter,sans-serif;color:{AMBER};">+24%</div>
      <div style="font:600 11px/1.3 DM Sans,sans-serif;color:rgba(255,255,255,0.65);margin-top:3px;">growth</div>
    </div>
    <div style="flex:1;background:{CORAL};border-radius:14px;padding:12px 6px;text-align:center;">
      <div style="font:800 26px/1 Inter,sans-serif;color:white;">1.2M</div>
      <div style="font:600 11px/1.3 DM Sans,sans-serif;color:rgba(255,255,255,0.75);margin-top:3px;">rows</div>
    </div>
    <div style="flex:1;background:{MINT};border-radius:14px;padding:12px 6px;text-align:center;
                border:2px solid {DEEP_BLUE};">
      <div style="font:800 26px/1 Inter,sans-serif;color:{DEEP_BLUE};">98%</div>
      <div style="font:600 11px/1.3 DM Sans,sans-serif;color:{DEEP_BLUE};opacity:.6;margin-top:3px;">accuracy</div>
    </div>
  </div>
</div>"""


def _make_prompts():
    """Floating AI prompt bubbles — Prompt Engineer."""
    return f"""
<div style="position:absolute;bottom:0;left:0;width:100%;height:100%;">

  <!-- Bubble 1 — white -->
  <div style="position:absolute;top:55px;right:18px;
              background:white;border:2.5px solid {DEEP_BLUE};border-radius:20px;
              padding:14px 18px;max-width:330px;
              box-shadow:5px 5px 0 {DEEP_BLUE};transform:rotate(-3deg);z-index:4;">
    <div style="font:700 15px/1.45 Inter,sans-serif;color:{DEEP_BLUE};">
      "Summarise this report in 3 bullets →"
    </div>
  </div>

  <!-- Bubble 2 — amber -->
  <div style="position:absolute;top:205px;right:10px;
              background:{AMBER};border:2.5px solid {DEEP_BLUE};border-radius:20px;
              padding:14px 18px;max-width:320px;
              box-shadow:5px 5px 0 {DEEP_BLUE};transform:rotate(2deg);z-index:3;">
    <div style="font:700 15px/1.45 Inter,sans-serif;color:{DEEP_BLUE};">
      "Act as a senior developer and review my code"
    </div>
  </div>

  <!-- Bubble 3 — navy -->
  <div style="position:absolute;top:368px;right:28px;
              background:{DEEP_BLUE};border:2.5px solid {DARK_NAVY};border-radius:20px;
              padding:14px 18px;max-width:300px;
              box-shadow:5px 5px 0 {DARK_NAVY};transform:rotate(-2deg);z-index:2;">
    <div style="font:700 15px/1.45 Inter,sans-serif;color:white;">
      "Write this in a Gen Z tone →"
    </div>
  </div>

  <!-- Bubble 4 — coral -->
  <div style="position:absolute;top:520px;right:40px;
              background:{CORAL};border:2.5px solid {DEEP_BLUE};border-radius:20px;
              padding:14px 18px;max-width:275px;
              box-shadow:5px 5px 0 {DEEP_BLUE};transform:rotate(3deg);z-index:1;">
    <div style="font:700 15px/1.45 Inter,sans-serif;color:white;">
      "Explain this like I'm 5..."
    </div>
  </div>

  <!-- Floating accents -->
  <div style="position:absolute;top:158px;right:362px;font-size:30px;transform:rotate(-10deg);">✨</div>
  <div style="position:absolute;top:448px;right:348px;font-size:22px;transform:rotate(5deg);">⚡</div>
</div>"""


# ── Slide 1 — HOOK ────────────────────────────────────────────────────────────

def generate_slide1(campaign_dir, photo_path):
    w, h = 1080, 1080
    font_faces = _build_font_faces()
    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""
    photo_b64 = _load_file_base64(photo_path)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, {DARK_NAVY} 0%, {DEEP_BLUE} 50%, {PURPLE} 100%);
}}
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px);
    background-size: 3px 3px; z-index:2;
}}
.glow {{
    position:absolute; bottom:-200px; right:-200px;
    width:700px; height:700px;
    background: radial-gradient(circle, rgba(255,177,32,0.25) 0%, transparent 60%);
    filter:blur(50px); z-index:1;
}}
.logo {{ position:absolute; top:44px; left:44px; height:72px; opacity:0.95; z-index:25; }}
.badge {{
    position:absolute; top:50px; right:50px;
    background:{AMBER}; color:{DEEP_BLUE};
    padding:12px 26px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:15px;
    letter-spacing:2px; text-transform:uppercase;
    transform:rotate(4deg);
    box-shadow: 0 8px 20px rgba(255,177,32,0.4); z-index:30;
}}
.headline-wrap {{
    position:absolute; top:180px; left:44px; right:44px; z-index:20;
}}
.kicker {{
    font-family:DM Sans; font-weight:700; font-size:22px; color:{AMBER};
    text-transform:uppercase; letter-spacing:3px; margin-bottom:10px;
}}
.headline {{
    font-family:Inter; font-weight:700;
    font-size:180px; line-height:0.85;
    color:white; letter-spacing:-8px;
}}
.headline .ai {{
    color:{AMBER}; font-style:italic;
    text-shadow: 6px 6px 0 {CORAL};
}}
.photo-wrap {{
    position:absolute; bottom:0; right:-30px;
    width:620px; height:720px; z-index:10;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.4));
}}
.photo-wrap img {{ width:100%; height:100%; object-fit:contain; object-position:bottom; }}
.photo-bg {{
    position:absolute; bottom:80px; right:40px;
    width:480px; height:580px;
    background: linear-gradient(135deg, {CORAL}, {AMBER});
    border-radius:250px 250px 40px 40px;
    z-index:5; opacity:0.95;
}}
.tag {{
    position:absolute;
    background:white; padding:12px 22px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:18px; color:{DEEP_BLUE};
    box-shadow: 0 8px 20px rgba(0,0,0,0.2); z-index:20;
}}
.tag-1 {{ top:515px; left:50px;  transform:rotate(-4deg); }}
.tag-2 {{ top:610px; left:180px; transform:rotate(3deg); background:{AMBER}; }}
.tag-3 {{ top:705px; left:60px;  transform:rotate(-2deg); background:{MINT}; }}
.tagline {{
    position:absolute; bottom:40px; left:44px;
    font-family:DM Sans; font-weight:700; font-size:24px;
    color:rgba(255,255,255,0.9); z-index:20;
}}
.tagline strong {{ color:{AMBER}; }}
.sparkle {{ position:absolute; z-index:14; }}
.sparkle-1 {{ top:140px; right:380px; }}
.sparkle-2 {{ top:350px; left:580px; }}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>
    <div class="glow"></div>
    {logo_img}
    <div class="badge">2026 Edition</div>
    <div class="headline-wrap">
        <div class="kicker">The future is hiring</div>
        <div class="headline">
            <span class="ai">AI</span>
            <span style="display:block;">JOBS</span>
        </div>
    </div>
    <div class="photo-bg"></div>
    <div class="photo-wrap">
        <img src="data:image/png;base64,{photo_b64}">
    </div>
    <div class="tag tag-1">🚀 Growing fast</div>
    <div class="tag tag-2">💰 High paying</div>
    <div class="tag tag-3">🌍 Remote-friendly</div>
    <div class="tagline">2026 is <strong>your year</strong> to break in →</div>
    <svg class="sparkle sparkle-1" width="32" height="32" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="white"/>
    </svg>
    <svg class="sparkle sparkle-2" width="22" height="22" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{AMBER}"/>
    </svg>
</div>
</body></html>"""
    _render(html, os.path.join(campaign_dir, "slide_1.png"))


# ── Role slide template (slides 2-4) ─────────────────────────────────────────

def _role_slide(campaign_dir, slide_num, graphic_html, config):
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    bg_styles = {
        "coral": {
            "canvas_bg": f"linear-gradient(135deg, {OFF_WHITE} 0%, #f5e8d9 100%)",
            "shape_bg":  f"linear-gradient(135deg, {CORAL}, #ff8c00)",
            "text_main": DEEP_BLUE,
            "text_accent": CORAL,
            "card_bg": "white",
            "card_text": DEEP_BLUE,
        },
        "purple": {
            "canvas_bg": f"linear-gradient(135deg, {DARK_NAVY} 0%, {DEEP_BLUE} 60%, {PURPLE} 100%)",
            "shape_bg":  f"linear-gradient(135deg, {AMBER}, #ff8c00)",
            "text_main": "white",
            "text_accent": AMBER,
            "card_bg": "rgba(255,255,255,0.95)",
            "card_text": DEEP_BLUE,
        },
        "mint": {
            "canvas_bg": f"linear-gradient(135deg, #e9f7f1 0%, {OFF_WHITE} 100%)",
            "shape_bg":  f"linear-gradient(135deg, {MINT}, #3fb88b)",
            "text_main": DEEP_BLUE,
            "text_accent": "#2d8a68",
            "card_bg": "white",
            "card_text": DEEP_BLUE,
        },
    }
    s = bg_styles[config["bg_style"]]

    skills_html = "".join(
        f'<div class="skill-pill">{sk}</div>' for sk in config["skills"]
    )

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: {s["canvas_bg"]};
}}
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(0,0,0,0.03) 1px, transparent 1px);
    background-size: 3px 3px; z-index:2;
}}
.number {{
    position:absolute; top:50px; left:50px;
    width:100px; height:100px;
    background:{DEEP_BLUE}; color:white; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-family:Inter; font-weight:700; font-size:48px;
    transform:rotate(-5deg);
    box-shadow: 0 10px 30px rgba(38,77,126,0.3); z-index:25;
}}
.kicker {{
    position:absolute; top:75px; left:180px;
    font-family:DM Sans; font-weight:700; font-size:22px;
    color:{s["text_main"]}; text-transform:uppercase;
    letter-spacing:3px; opacity:0.7; z-index:20;
}}
.emoji-badge {{
    position:absolute; top:50px; right:50px;
    width:100px; height:100px;
    background:{AMBER}; border-radius:28px;
    display:flex; align-items:center; justify-content:center;
    font-size:52px; transform:rotate(6deg);
    box-shadow: 8px 8px 0 {DEEP_BLUE}; z-index:25;
}}
.headline {{
    position:absolute; top:180px; left:50px;
    font-family:Inter; font-weight:700;
    font-size:100px; line-height:0.9;
    color:{s["text_main"]}; letter-spacing:-4px;
    z-index:20; max-width:640px;
}}
.headline .line2 {{
    display:inline-block;
    background:{s["text_accent"]}; color:white;
    padding:0 14px; transform:rotate(-1deg); font-style:italic;
}}
.photo-bg {{
    position:absolute; bottom:20px; right:30px;
    width:460px; height:540px;
    background: {s["shape_bg"]};
    border-radius:230px 230px 40px 40px;
    z-index:5;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}}
.graphic-wrap {{
    position:absolute; bottom:0; right:-20px;
    width:560px; height:680px;
    z-index:10; overflow:visible;
}}
.skills {{
    position:absolute; top:460px; left:50px;
    display:flex; flex-wrap:wrap; gap:10px;
    max-width:540px; z-index:15;
}}
.skill-pill {{
    background:{s["card_bg"]}; color:{s["card_text"]};
    padding:10px 20px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:17px;
    border: 2px solid {DEEP_BLUE};
    box-shadow: 3px 3px 0 {DEEP_BLUE};
}}
.fact-card {{
    position:absolute; bottom:50px; left:50px;
    background:{DEEP_BLUE}; color:white;
    padding:20px 26px; border-radius:18px;
    max-width:500px; z-index:20;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}}
.fact-label {{
    font-family:DM Sans; font-weight:700; font-size:14px; color:{AMBER};
    text-transform:uppercase; letter-spacing:2px; margin-bottom:4px;
}}
.fact-text {{
    font-family:Inter; font-weight:700; font-size:22px; line-height:1.2;
}}
.sparkle {{ position:absolute; z-index:14; }}
.sparkle-1 {{ top:200px; right:520px; }}
.sparkle-2 {{ top:400px; right:480px; }}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>
    <div class="number">{config["number"]}</div>
    <div class="kicker">{config["kicker"]}</div>
    <div class="emoji-badge">{config["emoji"]}</div>
    <div class="headline">
        {config["role_line1"]}<br>
        <span class="line2">{config["role_line2"]}</span>
    </div>
    <div class="photo-bg"></div>
    <div class="graphic-wrap">{graphic_html}</div>
    <div class="skills">{skills_html}</div>
    <div class="fact-card">
        <div class="fact-label">{config["fact_label"]}</div>
        <div class="fact-text">{config["fact_text"]}</div>
    </div>
    <svg class="sparkle sparkle-1" width="24" height="24" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{s["text_accent"]}"/>
    </svg>
    <svg class="sparkle sparkle-2" width="18" height="18" viewBox="0 0 40 40">
        <path d="M 20 4 L 23 17 L 36 20 L 23 23 L 20 36 L 17 23 L 4 20 L 17 17 Z" fill="{AMBER}"/>
    </svg>
</div>
</body></html>"""
    _render(html, os.path.join(campaign_dir, f"slide_{slide_num}.png"))


# ── Per-slide generators ──────────────────────────────────────────────────────

def generate_slide2(campaign_dir):
    _role_slide(campaign_dir, 2, _make_neural_net(), {
        "number": "1", "kicker": "Role #1", "emoji": "🤖",
        "role_line1": "AI/ML", "role_line2": "Engineer",
        "skills": ["Python", "TensorFlow", "Cloud", "Math-y brain"],
        "fact_label": "Avg salary (UK entry)",
        "fact_text": "£45k–£60k + fast promotions",
        "bg_style": "purple",
    })


def generate_slide3(campaign_dir):
    _role_slide(campaign_dir, 3, _make_dashboard(), {
        "number": "2", "kicker": "Role #2", "emoji": "📊",
        "role_line1": "Data", "role_line2": "Analyst",
        "skills": ["SQL", "Python", "Tableau", "Storytelling"],
        "fact_label": "Demand",
        "fact_text": "Every company needs one. Every. Single. One.",
        "bg_style": "coral",
    })


def generate_slide4(campaign_dir):
    _role_slide(campaign_dir, 4, _make_prompts(), {
        "number": "3", "kicker": "Role #3", "emoji": "✨",
        "role_line1": "Prompt", "role_line2": "Engineer",
        "skills": ["LLMs", "Creative thinking", "Any major", "Curiosity"],
        "fact_label": "The plot twist",
        "fact_text": "New role. Huge demand. You can break in now.",
        "bg_style": "mint",
    })


# ── Slide 5 — CONCLUSION / CTA ────────────────────────────────────────────────

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
    width:{w}px; height:{h}px; position:relative; overflow:hidden;
    background: linear-gradient(145deg, {DARK_NAVY} 0%, {DEEP_BLUE} 55%, {PURPLE} 100%);
}}
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(255,255,255,0.04) 1px, transparent 1px);
    background-size: 3px 3px; z-index:2;
}}
.logo {{ position:absolute; top:44px; left:44px; height:72px; opacity:0.95; z-index:25; }}
.badge {{
    position:absolute; top:52px; right:52px;
    background:{AMBER}; color:{DEEP_BLUE};
    padding:12px 28px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:15px;
    letter-spacing:2px; text-transform:uppercase;
    transform:rotate(-3deg);
    box-shadow: 0 8px 22px rgba(255,177,32,0.45); z-index:25;
}}
.kicker {{
    position:absolute; top:205px; left:60px;
    font-family:DM Sans; font-weight:700; font-size:24px;
    color:{AMBER}; text-transform:uppercase; letter-spacing:4px; z-index:20;
}}
.headline {{
    position:absolute; top:248px; left:60px;
    font-family:Inter; font-weight:700;
    font-size:160px; line-height:0.88;
    color:white; letter-spacing:-7px; z-index:20;
}}
.headline .accent {{
    display:block; color:{AMBER}; font-style:italic;
    text-shadow: 6px 6px 0 {CORAL};
}}
.pills {{
    position:absolute; top:630px; left:60px;
    display:flex; gap:16px; z-index:20;
}}
.pill {{
    padding:12px 24px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:18px;
    border:2px solid rgba(255,255,255,0.25); color:white;
    background:rgba(255,255,255,0.1);
}}
.pill.p1 {{ border-color:{PURPLE}; background:rgba(123,92,230,0.3); }}
.pill.p2 {{ border-color:{CORAL}; background:rgba(255,107,107,0.2); }}
.pill.p3 {{ border-color:{MINT}; background:rgba(127,219,182,0.2); color:{MINT}; }}
.cta {{
    position:absolute; bottom:58px; left:60px; right:60px;
    background:{AMBER}; padding:28px 38px; border-radius:22px;
    display:flex; align-items:center; justify-content:space-between;
    border:3px solid {DARK_NAVY}; box-shadow:6px 6px 0 {DARK_NAVY}; z-index:20;
}}
.cta-text {{
    font-family:Inter; font-weight:700; font-size:28px;
    color:{DEEP_BLUE}; line-height:1.2;
}}
.cta-url {{
    font-family:Inter; font-weight:700; font-size:20px;
    color:{DARK_NAVY}; opacity:0.7; margin-top:4px; display:block;
}}
.cta-arrow {{
    width:70px; height:70px; background:{DEEP_BLUE};
    border-radius:50%; display:flex; align-items:center; justify-content:center;
    flex-shrink:0;
}}
.sp {{ position:absolute; z-index:14; }}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>
    {logo_img}
    <div class="badge">Get Hired</div>
    <div class="kicker">Your next move</div>
    <div class="headline">
        BREAK<br><span class="accent">IN.</span>
    </div>
    <div class="pills">
        <div class="pill p1">🤖 AI/ML</div>
        <div class="pill p2">📊 Data</div>
        <div class="pill p3">✨ Prompt Eng</div>
    </div>
    <div class="cta">
        <div class="cta-text">
            Find your first AI role.
            <span class="cta-url">internwise.co.uk →</span>
        </div>
        <div class="cta-arrow">
            <svg width="36" height="36" viewBox="0 0 36 36">
                <path d="M8 18 L26 18 M20 10 L28 18 L20 26"
                    stroke="white" stroke-width="4" fill="none"
                    stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
    <svg class="sp" style="top:180px;right:90px;" width="32" height="32" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="{AMBER}" opacity="0.7"/>
    </svg>
    <svg class="sp" style="top:520px;right:200px;" width="20" height="20" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="white" opacity="0.35"/>
    </svg>
    <svg class="sp" style="top:150px;left:660px;" width="16" height="16" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="{MINT}" opacity="0.5"/>
    </svg>
</div>
</body></html>"""
    _render(html, os.path.join(campaign_dir, "slide_5.png"))


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating AI Jobs Carousel (Gen Z Edition v3)...")
    hook_photo = _fetch_hook_photo()
    generate_slide1(campaign_dir, hook_photo)
    generate_slide2(campaign_dir)
    generate_slide3(campaign_dir)
    generate_slide4(campaign_dir)
    generate_slide5(campaign_dir)
    print("✓ AI Jobs carousel complete!")
