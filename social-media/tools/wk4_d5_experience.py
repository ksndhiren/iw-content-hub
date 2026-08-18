"""
Internwise - Build Experience Carousel (Week 4, Day 5) - v4
7-slide carousel: how to build experience when you have none
v4: hybrid layout - human photos on slides 1,3,5,7; SVG graphics on 2,4,6
    Fixed slide 1 heading, 4 unique persons (no repeats), cleaner BG queries
"""
import os, base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_cutout

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B";     PURPLE = "#7B5CE6";    MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"; LIGHT_BLUE = "#5FA7E5"

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

def _src(path):
    if not path: return ""
    b64 = _b64(path)
    if not b64: return ""
    mime = "image/png" if path.endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{b64}"

def _fonts():
    variants = {
        "Inter":   [("Inter-Bold.ttf",700),("Inter-SemiBold.ttf",600),("Inter-Regular.ttf",400)],
        "DM Sans": [("DMSans-Bold.ttf",700),("DMSans-Medium.ttf",500),("DMSans-Regular.ttf",400)],
    }
    css = ""
    for family, vv in variants.items():
        for fn, w in vv:
            b = _b64(os.path.join(FONTS_DIR, fn))
            if b: css += f"@font-face{{font-family:'{family}';src:url(data:font/truetype;base64,{b}) format('truetype');font-weight:{w};}}"
    return css

def _render(html, path):
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width":1080,"height":1080}, device_scale_factor=2)
        pg.set_content(html, wait_until="networkidle")
        pg.screenshot(path=path, type="png")
        br.close()
    print(f"  ok {path}")

LOGO_B64 = None
def _logo_b64():
    global LOGO_B64
    if LOGO_B64 is None:
        LOGO_B64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    return LOGO_B64

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"

def _spark(s,t,l,c,o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:3;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'

def _arch_photo(src, accent):
    """Human photo in arch frame, right half."""
    if not src: return ""
    return f"""
<div style="position:absolute;bottom:0;right:0;width:480px;height:600px;
            background:linear-gradient(155deg,{accent},{accent}88);
            border-radius:240px 240px 0 0;z-index:5;
            box-shadow:-10px 0 40px rgba(0,0,0,0.2);"></div>
<div style="position:absolute;bottom:0;right:0;width:510px;height:680px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.35));overflow:hidden;">
  <img src="{src}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""

def _illus_panel(svg_content):
    """SVG illustration panel, right half."""
    return f"""
<div style="position:absolute;top:0;right:0;width:534px;height:1080px;
            z-index:5;overflow:hidden;">
  <svg width="534" height="1080" viewBox="0 0 534 1080"
       xmlns="http://www.w3.org/2000/svg" style="display:block;">
    {svg_content}
  </svg>
</div>"""


# ── SVG Illustration: Build Something (slide 2) ────────────────────────────────
def _illus_build():
    out = f'<circle cx="267" cy="500" r="300" fill="{AMBER}" opacity="0.04"/>'

    # Laptop screen
    lx, ly, lw, lh = 44, 140, 446, 290
    out += f"""
<rect x="{lx+6}" y="{ly+6}" width="{lw}" height="{lh}" rx="14" fill="rgba(0,0,0,0.35)"/>
<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="14"
      fill="#0d1520" stroke="{AMBER}" stroke-width="2"
      filter="drop-shadow(0 8px 28px rgba(0,0,0,0.45))"/>
<rect x="{lx+10}" y="{ly+10}" width="{lw-20}" height="{lh-20}" rx="10" fill="#0a1118"/>"""

    # Code editor lines
    code = [
        (MINT,       "function buildPortfolio() {"),
        (LIGHT_BLUE, "  const project = createApp();"),
        (AMBER,      "  deploy(project, 'GitHub');"),
        (CORAL,      "  return 'Experience earned';"),
        ("rgba(255,255,255,0.35)", "}"),
    ]
    for i, (col, line) in enumerate(code):
        out += f"""
<text x="{lx+22}" y="{ly+52+i*46}" font-family="monospace" font-size="19"
      fill="{col}" opacity="0.92">{line}</text>"""

    # Laptop base
    out += f"""
<rect x="{lx-22}" y="{ly+lh}" width="{lw+44}" height="20" rx="5"
      fill="#1e2d40" stroke="rgba(255,177,32,0.3)" stroke-width="1.5"/>
<rect x="{lx+lw//2-44}" y="{ly+lh+15}" width="88" height="7" rx="3"
      fill="{AMBER}" opacity="0.35"/>"""

    # GitHub contribution grid
    gx, gy = 44, 490
    out += f"""
<text x="{gx}" y="{gy-12}" font-family="Inter" font-weight="700" font-size="11"
      fill="rgba(255,255,255,0.35)" letter-spacing="3">GITHUB CONTRIBUTIONS</text>"""
    import random; random.seed(7)
    cols_g, rows_g, cell = 13, 5, 17
    for r in range(rows_g):
        for c in range(cols_g):
            lvl = random.choice([0,0,1,1,2,3,3,4])
            fills = ["rgba(255,255,255,0.05)", f"{MINT}30", f"{MINT}55", f"{MINT}85", MINT]
            out += f'<rect x="{gx+c*(cell+3)}" y="{gy+r*(cell+3)}" width="{cell}" height="{cell}" rx="3" fill="{fills[lvl]}"/>'

    # Status badges row
    badges = [
        (MINT,       "✓  Deployed"),
        (AMBER,      "★  14 stars"),
        (LIGHT_BLUE, "⑂  6 forks"),
    ]
    for i, (col, txt) in enumerate(badges):
        bx = 44 + i * 162
        by = 610
        out += f"""
<rect x="{bx}" y="{by}" width="148" height="42" rx="10"
      fill="{col}" opacity="0.15" stroke="{col}" stroke-width="1.3"/>
<text x="{bx+74}" y="{by+27}" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="16" fill="{col}">{txt}</text>"""

    # Skill chips
    skills = [("Python", MINT), ("React", LIGHT_BLUE), ("SQL", PURPLE), ("Figma", AMBER), ("Git", CORAL)]
    cx_s = 44
    for name, col in skills:
        sw = len(name) * 11 + 26
        out += f"""
<rect x="{cx_s}" y="680" width="{sw}" height="34" rx="8"
      fill="{col}" opacity="0.18" stroke="{col}" stroke-width="1.2"/>
<text x="{cx_s+sw//2}" y="702" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="14" fill="{col}">{name}</text>"""
        cx_s += sw + 10

    # Insight banner
    out += f"""
<rect x="44" y="740" width="446" height="62" rx="14"
      fill="{AMBER}" opacity="0.09" stroke="{AMBER}" stroke-width="1.2"/>
<text x="267" y="765" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="13" fill="{AMBER}" letter-spacing="2">ONE FINISHED PROJECT</text>
<text x="267" y="787" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="600"
      font-size="14" fill="rgba(255,255,255,0.5)">beats ten courses on your CV</text>"""

    return out


# ── SVG Illustration: Micro-internships (slide 4) ─────────────────────────────
def _illus_micro_intern():
    out = f'<circle cx="267" cy="480" r="290" fill="{MINT}" opacity="0.03"/>'

    steps = [
        (LIGHT_BLUE, "APPLY",    "Day 1",   "Submit profile, no experience needed"),
        (AMBER,      "BRIEF",    "Day 2",   "Receive real project from company"),
        (CORAL,      "DELIVER",  "Wk 2-4",  "Complete task, submit work"),
        (MINT,       "PAID",     "Wk 4+",   "Get paid + company name on CV"),
    ]

    for i, (col, label, time, desc) in enumerate(steps):
        cy = 120 + i * 205

        # Glow ring + circle
        out += f'<circle cx="267" cy="{cy}" r="52" fill="{col}" opacity="0.08"/>'
        out += f'<circle cx="267" cy="{cy}" r="42" fill="{col}" opacity="0.18" stroke="{col}" stroke-width="2"/>'
        out += f'<text x="267" y="{cy+6}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="14" fill="{col}" letter-spacing="1">{label}</text>'

        # Time chip (left)
        out += f"""
<rect x="148" y="{cy-15}" width="82" height="28" rx="7"
      fill="rgba(255,255,255,0.07)" stroke="{col}" stroke-width="1" opacity="0.6"/>
<text x="189" y="{cy+4}" text-anchor="middle" font-family="DM Sans,sans-serif"
      font-weight="700" font-size="12" fill="{col}" opacity="0.8">{time}</text>"""

        # Description below
        out += f"""
<text x="267" y="{cy+66}" text-anchor="middle" font-family="DM Sans,sans-serif"
      font-weight="600" font-size="13" fill="rgba(255,255,255,0.45)">{desc}</text>"""

        # Connector arrow
        if i < 3:
            ay = cy + 52
            out += f'<line x1="267" y1="{ay}" x2="267" y2="{ay+110}" stroke="{col}" stroke-width="1.5" stroke-dasharray="5,4" opacity="0.35"/>'
            out += f'<polygon points="261,{ay+112} 267,{ay+124} 273,{ay+112}" fill="{col}" opacity="0.35"/>'

    # Bottom stat
    out += f"""
<rect x="44" y="944" width="446" height="64" rx="14"
      fill="{MINT}" opacity="0.09" stroke="{MINT}" stroke-width="1.2"/>
<text x="267" y="969" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="13" fill="{MINT}" letter-spacing="2">DO 2-3 BACK TO BACK</text>
<text x="267" y="991" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="600"
      font-size="14" fill="rgba(255,255,255,0.5)">Real company names. Real CV credit.</text>"""

    return out


# ── SVG Illustration: Freelance workflow (slide 5) ───────────────────────────
def _illus_freelance():
    """Client brief → work delivered → invoice → payment received."""
    out = f'<circle cx="267" cy="500" r="300" fill="{PURPLE}" opacity="0.04"/>'

    # ── Step 1: Client message / brief ────────────────────────────────────
    out += f"""
<rect x="30" y="52" width="474" height="118" rx="14"
      fill="rgba(255,255,255,0.07)" stroke="{LIGHT_BLUE}" stroke-width="1.5"/>
<text x="52" y="78" font-family="Inter" font-weight="700" font-size="11"
      fill="{LIGHT_BLUE}" letter-spacing="3">CLIENT MESSAGE</text>
<rect x="52" y="88" width="36" height="36" rx="18" fill="{LIGHT_BLUE}" opacity="0.3"/>
<text x="70" y="111" text-anchor="middle" font-size="18">💼</text>
<rect x="100" y="90" width="170" height="12" rx="6" fill="rgba(255,255,255,0.6)"/>
<rect x="100" y="110" width="260" height="9" rx="4.5" fill="rgba(255,255,255,0.25)"/>
<rect x="100" y="126" width="200" height="9" rx="4.5" fill="rgba(255,255,255,0.18)"/>
<rect x="390" y="88" width="90" height="26" rx="8"
      fill="{AMBER}" opacity="0.25" stroke="{AMBER}" stroke-width="1"/>
<text x="435" y="106" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="11" fill="{AMBER}">NEW JOB</text>"""

    # ── Connector ─────────────────────────────────────────────────────────
    out += f'<line x1="267" y1="170" x2="267" y2="220" stroke="{PURPLE}" stroke-width="1.5" stroke-dasharray="5,4" opacity="0.4"/>'
    out += f'<polygon points="261,220 267,232 273,220" fill="{PURPLE}" opacity="0.4"/>'

    # ── Step 2: Work in progress card ────────────────────────────────────
    out += f"""
<rect x="30" y="234" width="474" height="140" rx="14"
      fill="rgba(255,255,255,0.07)" stroke="{PURPLE}" stroke-width="1.5"/>
<text x="52" y="260" font-family="Inter" font-weight="700" font-size="11"
      fill="{PURPLE}" letter-spacing="3">YOUR DELIVERABLE</text>
<rect x="52" y="272" width="240" height="86" rx="10"
      fill="rgba(123,92,230,0.15)" stroke="{PURPLE}" stroke-width="1"/>
<rect x="62" y="282" width="180" height="10" rx="5" fill="rgba(255,255,255,0.25)"/>
<rect x="62" y="300" width="140" height="8" rx="4" fill="rgba(255,255,255,0.15)"/>
<rect x="62" y="316" width="160" height="8" rx="4" fill="rgba(255,255,255,0.12)"/>
<rect x="62" y="332" width="100" height="8" rx="4" fill="rgba(255,255,255,0.1)"/>
<rect x="308" y="272" width="172" height="86" rx="10"
      fill="rgba(123,92,230,0.1)" stroke="{PURPLE}" stroke-width="1" stroke-dasharray="4,3"/>
<text x="394" y="310" text-anchor="middle" font-size="26">🎨</text>
<text x="394" y="335" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="11" fill="{PURPLE}" opacity="0.7">DESIGNED</text>"""

    # ── Connector ─────────────────────────────────────────────────────────
    out += f'<line x1="267" y1="374" x2="267" y2="424" stroke="{CORAL}" stroke-width="1.5" stroke-dasharray="5,4" opacity="0.4"/>'
    out += f'<polygon points="261,424 267,436 273,424" fill="{CORAL}" opacity="0.4"/>'

    # ── Step 3: Invoice ───────────────────────────────────────────────────
    out += f"""
<rect x="30" y="438" width="474" height="130" rx="14"
      fill="rgba(255,255,255,0.07)" stroke="{CORAL}" stroke-width="1.5"/>
<text x="52" y="464" font-family="Inter" font-weight="700" font-size="11"
      fill="{CORAL}" letter-spacing="3">INVOICE</text>
<text x="52" y="498" font-family="Inter" font-weight="700" font-size="28"
      fill="white">#INV-001</text>
<rect x="52" y="510" width="220" height="8" rx="4" fill="rgba(255,255,255,0.15)"/>
<rect x="52" y="526" width="160" height="8" rx="4" fill="rgba(255,255,255,0.1)"/>
<rect x="340" y="470" width="140" height="54" rx="10"
      fill="{CORAL}" opacity="0.18" stroke="{CORAL}" stroke-width="1.5"/>
<text x="410" y="492" text-anchor="middle" font-family="DM Sans,sans-serif"
      font-weight="700" font-size="12" fill="rgba(255,255,255,0.5)">TOTAL DUE</text>
<text x="410" y="516" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="22" fill="{CORAL}">£150</text>"""

    # ── Connector ─────────────────────────────────────────────────────────
    out += f'<line x1="267" y1="568" x2="267" y2="618" stroke="{MINT}" stroke-width="1.5" stroke-dasharray="5,4" opacity="0.4"/>'
    out += f'<polygon points="261,618 267,630 273,618" fill="{MINT}" opacity="0.4"/>'

    # ── Step 4: Payment received ──────────────────────────────────────────
    out += f"""
<rect x="30" y="632" width="474" height="80" rx="14"
      fill="{MINT}" opacity="0.14" stroke="{MINT}" stroke-width="2"/>
<text x="267" y="664" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="22" fill="{MINT}" letter-spacing="1">✓  PAYMENT RECEIVED</text>
<text x="267" y="691" text-anchor="middle" font-family="DM Sans,sans-serif"
      font-weight="600" font-size="14" fill="rgba(255,255,255,0.55)">£150 · Freelance Graphic Designer</text>"""

    # ── CV credit badge ───────────────────────────────────────────────────
    out += f"""
<rect x="30" y="736" width="474" height="62" rx="14"
      fill="{AMBER}" opacity="0.09" stroke="{AMBER}" stroke-width="1.2"/>
<text x="267" y="762" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="13" fill="{AMBER}" letter-spacing="2">NOW ON YOUR CV</text>
<text x="267" y="784" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="600"
      font-size="14" fill="rgba(255,255,255,0.5)">Freelance Graphic Designer · Self-employed</text>"""

    return out


# ── SVG Illustration: Online presence (slide 6) ───────────────────────────────
def _illus_online_presence():
    out = f'<circle cx="267" cy="500" r="300" fill="{LIGHT_BLUE}" opacity="0.03"/>'

    # Profile card
    pcx, pcy, pcw, pch = 30, 52, 474, 196
    out += f"""
<rect x="{pcx+5}" y="{pcy+5}" width="{pcw}" height="{pch}" rx="14" fill="rgba(0,0,0,0.3)"/>
<rect x="{pcx}" y="{pcy}" width="{pcw}" height="{pch}" rx="14"
      fill="rgba(255,255,255,0.07)" stroke="{LIGHT_BLUE}" stroke-width="1.5"/>"""

    # Avatar
    out += f"""
<circle cx="{pcx+68}" cy="{pcy+82}" r="50" fill="{LIGHT_BLUE}" opacity="0.22"/>
<circle cx="{pcx+68}" cy="{pcy+64}" r="22" fill="rgba(255,255,255,0.55)"/>
<ellipse cx="{pcx+68}" cy="{pcy+108}" rx="30" ry="20" fill="rgba(255,255,255,0.45)"/>"""

    # Name + title bars
    out += f"""
<rect x="{pcx+136}" y="{pcy+28}" width="140" height="16" rx="8" fill="rgba(255,255,255,0.65)"/>
<rect x="{pcx+136}" y="{pcy+54}" width="96" height="10" rx="5" fill="rgba(255,255,255,0.3)"/>"""

    # Open to work chip
    out += f"""
<rect x="{pcx+136}" y="{pcy+74}" width="118" height="26" rx="7"
      fill="{MINT}" opacity="0.22" stroke="{MINT}" stroke-width="1"/>
<text x="{pcx+195}" y="{pcy+91}" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="11" fill="{MINT}">#opentowork</text>"""

    # Stats
    for i, (val, lbl) in enumerate([("500+", "connections"), ("1.2k", "views"), ("47", "posts")]):
        sx = pcx + 136 + i * 114
        out += f"""
<text x="{sx+18}" y="{pcy+128}" font-family="Inter" font-weight="700" font-size="22" fill="white">{val}</text>
<text x="{sx+18}" y="{pcy+148}" font-family="DM Sans,sans-serif" font-size="11" fill="rgba(255,255,255,0.38)">{lbl}</text>"""

    # Findable badge
    out += f"""
<rect x="{pcx+pcw-96}" y="{pcy+12}" width="80" height="28" rx="8"
      fill="{MINT}" opacity="0.2" stroke="{MINT}" stroke-width="1"/>
<text x="{pcx+pcw-56}" y="{pcy+31}" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="11" fill="{MINT}" letter-spacing="1">FINDABLE</text>"""

    # Portfolio label
    out += f"""
<text x="30" y="286" font-family="Inter" font-weight="700" font-size="11"
      fill="rgba(255,255,255,0.35)" letter-spacing="3">PORTFOLIO</text>"""

    # 3 project cards
    proj_cols = [AMBER, CORAL, MINT]
    for i in range(3):
        px_ = 30 + i * 164
        py_ = 302
        col = proj_cols[i]
        out += f"""
<rect x="{px_}" y="{py_}" width="150" height="128" rx="12"
      fill="rgba(255,255,255,0.06)" stroke="{col}" stroke-width="1.3"/>
<rect x="{px_}" y="{py_}" width="150" height="44" rx="12" fill="{col}" opacity="0.22"/>
<rect x="{px_}" y="{py_+32}" width="150" height="12" fill="{col}" opacity="0.14"/>
<rect x="{px_+12}" y="{py_+60}" width="84" height="8" rx="4" fill="rgba(255,255,255,0.14)"/>
<rect x="{px_+12}" y="{py_+76}" width="64" height="8" rx="4" fill="rgba(255,255,255,0.1)"/>
<rect x="{px_+12}" y="{py_+92}" width="100" height="8" rx="4" fill="rgba(255,255,255,0.1)"/>
<text x="{px_+75}" y="{py_+24}" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="11" fill="{col}">Project {i+1}</text>"""

    # Activity feed
    out += f"""
<text x="30" y="472" font-family="Inter" font-weight="700" font-size="11"
      fill="rgba(255,255,255,0.35)" letter-spacing="3">RECENT ACTIVITY</text>"""

    activity = [
        (MINT,       "Shared: Data analysis case study"),
        (AMBER,      "Added Python project to portfolio"),
        (LIGHT_BLUE, "Endorsed for SQL, Excel, Power BI"),
    ]
    for i, (col, txt) in enumerate(activity):
        ay = 484 + i * 72
        out += f"""
<rect x="30" y="{ay}" width="474" height="56" rx="10"
      fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>
<circle cx="54" cy="{ay+28}" r="11" fill="{col}" opacity="0.75"/>
<text x="76" y="{ay+32}" font-family="DM Sans,sans-serif" font-weight="600"
      font-size="14" fill="rgba(255,255,255,0.7)">{txt}</text>"""

    # Bottom rule
    out += f"""
<rect x="30" y="706" width="474" height="62" rx="14"
      fill="{LIGHT_BLUE}" opacity="0.09" stroke="{LIGHT_BLUE}" stroke-width="1.2"/>
<text x="267" y="730" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="13" fill="{LIGHT_BLUE}" letter-spacing="2">BE FINDABLE BEFORE THEY SEARCH</text>
<text x="267" y="752" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="600"
      font-size="14" fill="rgba(255,255,255,0.5)">Google your name. What comes up?</text>"""

    return out


# ── Slide 1: Hook (human photo) ───────────────────────────────────────────────
def _slide1(out, photo_src):
    f = _fonts(); lb = _logo_b64()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.badge{{position:absolute;top:44px;right:44px;background:{AMBER};color:{DEEP_BLUE};
    padding:11px 26px;border-radius:50px;font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(4deg);
    box-shadow:0 8px 22px rgba(255,177,32,0.45);z-index:20;}}
.col{{position:absolute;top:44px;left:50px;right:534px;
    display:flex;flex-direction:column;gap:0;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_arch_photo(photo_src, AMBER)}
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:25;">
<div class="badge">Career builder</div>
<div class="col">
  <div style="font-family:'DM Sans';font-weight:700;font-size:19px;color:{AMBER};
              text-transform:uppercase;letter-spacing:4px;margin-top:108px;margin-bottom:12px;">Start from zero</div>
  <div style="font-family:Inter;font-weight:700;font-size:72px;line-height:0.96;
              color:white;letter-spacing:-4px;margin-bottom:18px;">How to build<br>experience<br>when you<br>have <span style="color:{AMBER};font-style:italic;">none.</span></div>
  <div style="width:70px;height:4px;background:{AMBER};border-radius:2px;margin-bottom:16px;"></div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:25px;
              color:rgba(255,255,255,0.65);line-height:1.4;">5 methods. No connections required.</div>
</div>
<div style="position:absolute;bottom:44px;left:50px;z-index:20;
    font-family:Inter;font-weight:700;font-size:20px;color:rgba(255,255,255,0.38);">
  Swipe for the full playbook <strong style="color:rgba(255,255,255,0.7);">→</strong>
</div>
{_spark(26,200,400,AMBER,0.45)}
</div></body></html>"""
    _render(html, out)


# ── Method slides shell ───────────────────────────────────────────────────────
METHODS = [
    {
        "n": 2, "num_label": "01 / 05", "accent": AMBER,
        "method": "Build something.",
        "subtitle": "Projects beat blank CVs every time.",
        "what": "Create something relevant to your target role and put it online.",
        "examples": [
            ("Aspiring marketers",  "Run a small social account or write a monthly newsletter."),
            ("Aspiring developers", "Build a simple app or website. Put it on GitHub."),
            ("Aspiring analysts",   "Clean a public dataset. Publish your findings."),
            ("Aspiring designers",  "Redesign a real brand's UX. Show before and after."),
        ],
        "tip": "One finished project beats ten courses completed. Show your work.",
        "visual": "svg_build",
    },
    {
        "n": 3, "num_label": "02 / 05", "accent": CORAL,
        "method": "Volunteer for responsibility.",
        "subtitle": "Unpaid experience still counts.",
        "what": "Find roles with real tasks - managing money, leading a team, running events.",
        "examples": [
            ("Society treasurer",    "Budget management, financial reporting - real finance skills."),
            ("Events lead",          "Project coordination, stakeholder management, logistics."),
            ("Sports captain",       "Leadership, performance under pressure, team management."),
            ("Charity support role", "Initiative, communication, and social impact on your CV."),
        ],
        "tip": "The key word is responsibility. Anyone can attend. Few people actually run things.",
        "visual": "photo_b",
    },
    {
        "n": 4, "num_label": "03 / 05", "accent": MINT,
        "method": "Apply for micro-internships.",
        "subtitle": "Short-term. Low barrier. Real CV credit.",
        "what": "Paid, project-based roles - usually 1-4 weeks. No prior experience required.",
        "examples": [
            ("What they are",      "Specific project tasks at real companies. You deliver, they pay."),
            ("Who offers them",    "Startups and SMEs often prefer project-based over formal schemes."),
            ("Where to find them", "Search 'project-based' or 'short-term' on internship job boards."),
            ("The result",         "Do 2-3 back to back and your CV has real company names on it."),
        ],
        "tip": "A micro-internship at a real company beats any course certificate.",
        "visual": "svg_intern",
    },
    {
        "n": 5, "num_label": "04 / 05", "accent": PURPLE,
        "method": "Freelance. Even once.",
        "subtitle": "One paying client changes how your CV reads.",
        "what": "Find one person or small business who needs a task done. Do it for a fee.",
        "examples": [
            ("Social content",   "Small businesses often need posts written or scheduled weekly."),
            ("Data or research", "Collect, clean, or analyse data for a local business."),
            ("Writing/editing",  "Blog posts, product descriptions, pitch decks."),
            ("Design work",      "Logos, flyers, Canva templates. One paid job counts."),
        ],
        "tip": "Write it as 'Freelance [role] - self-employed'. It is legitimate work experience.",
        "visual": "svg_freelance",
    },
    {
        "n": 6, "num_label": "05 / 05", "accent": LIGHT_BLUE,
        "method": "Build an online presence.",
        "subtitle": "Be findable. Let your work speak first.",
        "what": "Create a public record of what you know and what you've built.",
        "examples": [
            ("Profile",       "Complete and keyword-rich - gets found by recruiters passively."),
            ("GitHub repo",   "Even a few clean, documented projects signal technical credibility."),
            ("Personal blog", "Write about what you're learning. Thinking in public builds trust."),
            ("Portfolio page","Your 3 best projects and a way to contact you. That's all it needs."),
        ],
        "tip": "You don't need thousands of followers. You need to be findable when someone googles your name.",
        "visual": "svg_presence",
    },
]

def _method_slide(m, photo_src, out):
    f = _fonts(); lb = _logo_b64()
    accent = m["accent"]
    dark_accent = accent in (AMBER, MINT, LIGHT_BLUE)
    accent_text = DEEP_BLUE if dark_accent else "white"

    # Right panel: SVG illustration or human photo
    visual = m.get("visual", "")
    if visual == "svg_build":
        right_panel = _illus_panel(_illus_build())
    elif visual == "svg_intern":
        right_panel = _illus_panel(_illus_micro_intern())
    elif visual == "svg_freelance":
        right_panel = _illus_panel(_illus_freelance())
    elif visual == "svg_presence":
        right_panel = _illus_panel(_illus_online_presence())
    else:
        right_panel = _arch_photo(photo_src, accent)

    examples_html = "".join(f"""
<div style="display:flex;align-items:flex-start;gap:12px;
            padding:12px 14px;background:rgba(255,255,255,0.05);
            border-radius:9px;border-left:3px solid {accent};">
  <div style="width:8px;height:8px;border-radius:50%;flex-shrink:0;
              background:{accent};margin-top:7px;"></div>
  <div>
    <span style="font-family:Inter;font-weight:700;font-size:21px;color:{accent};">{lbl} - </span>
    <span style="font-family:'DM Sans';font-weight:500;font-size:21px;
                color:rgba(255,255,255,0.72);">{desc}</span>
  </div>
</div>""" for lbl,desc in m["examples"])

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.bar{{position:absolute;top:0;left:0;width:6px;height:100%;background:{accent};z-index:10;
      box-shadow:0 0 20px {accent}55;}}
.num{{position:absolute;top:48px;right:44px;font-family:Inter;font-weight:700;font-size:14px;
    color:rgba(255,255,255,0.3);letter-spacing:2px;z-index:25;}}
.url{{position:absolute;bottom:36px;right:44px;font-family:Inter;font-weight:700;font-size:14px;
    color:rgba(255,255,255,0.2);z-index:25;}}
.col{{position:absolute;top:44px;left:50px;right:534px;
      display:flex;flex-direction:column;gap:0;z-index:20;overflow:hidden;max-height:992px;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="bar"></div>
{right_panel}
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:50px;height:66px;opacity:0.95;z-index:25;">
<div class="num">{m['num_label']}</div>
<div class="url">internwise.co.uk</div>
<div class="col">
  <div style="align-self:flex-start;background:{accent};color:{accent_text};
              padding:7px 18px;border-radius:50px;font-family:Inter;font-weight:700;
              font-size:12px;letter-spacing:2px;text-transform:uppercase;
              margin-top:108px;margin-bottom:10px;">Method {m['num_label'].split('/')[0].strip()}</div>
  <div style="font-family:Inter;font-weight:700;font-size:50px;line-height:1.0;
              color:white;letter-spacing:-2px;margin-bottom:6px;">{m['method']}</div>
  <div style="font-family:'DM Sans';font-weight:700;font-size:21px;
              color:rgba(255,255,255,0.5);margin-bottom:10px;">{m['subtitle']}</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:21px;
              color:rgba(255,255,255,0.75);line-height:1.4;padding-bottom:12px;
              border-bottom:1.5px solid rgba(255,255,255,0.1);margin-bottom:12px;">{m['what']}</div>
  <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:12px;">{examples_html}</div>
  <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:13px 15px;
              border:1px solid rgba(255,255,255,0.1);">
    <div style="font-family:'DM Sans';font-weight:700;font-size:15px;
                color:{accent};text-transform:uppercase;letter-spacing:2px;">Key insight</div>
    <div style="font-family:'DM Sans';font-weight:600;font-size:21px;
                color:rgba(255,255,255,0.65);margin-top:4px;line-height:1.4;">{m['tip']}</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA (human photo) ────────────────────────────────────────────────
def _slide7(out, photo_src):
    f = _fonts(); lb = _logo_b64()
    chips = [
        (AMBER,      DEEP_BLUE, "Build a project"),
        (CORAL,      "white",   "Volunteer for responsibility"),
        (MINT,       DEEP_BLUE, "Micro-internship"),
        (PURPLE,     "white",   "One freelance job"),
        (LIGHT_BLUE, DEEP_BLUE, "Build your online presence"),
    ]
    chips_html = "".join(f"""
<div style="padding:12px 20px;border-radius:12px;background:{bg};color:{ct};
     font-family:Inter;font-weight:700;font-size:16px;
     border:2.5px solid {DARK_NAVY};box-shadow:3px 3px 0 {DARK_NAVY};
     display:inline-block;margin:4px;">{label}</div>""" for bg,ct,label in chips)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{OFF_WHITE};}}
.grain2{{position:absolute;inset:0;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(0,0,0,0.025) 1px,transparent 1px);
    background-size:3px 3px;}}
.badge{{position:absolute;top:44px;right:44px;background:{DEEP_BLUE};color:white;
    padding:11px 24px;border-radius:50px;font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(-3deg);
    box-shadow:5px 5px 0 {DARK_NAVY};z-index:20;}}
.col{{position:absolute;top:44px;left:60px;right:534px;
      display:flex;flex-direction:column;gap:0;z-index:20;}}
.cta{{background:{DEEP_BLUE};color:white;padding:22px 28px;border-radius:16px;
    font-family:Inter;font-weight:700;font-size:22px;
    border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
    display:flex;align-items:center;justify-content:space-between;}}
.arrow{{width:52px;height:52px;background:{AMBER};border-radius:50%;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
</style></head><body><div class="c">
<div class="grain2"></div>
{_arch_photo(photo_src, DEEP_BLUE)}
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:60px;height:66px;opacity:0.95;z-index:25;filter:brightness(0) saturate(100%) invert(18%) sepia(34%) saturate(1289%) hue-rotate(183deg) brightness(94%) contrast(91%);">
<div class="badge">Start today</div>
<div class="col">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{AMBER};
              text-transform:uppercase;letter-spacing:4px;margin-top:108px;margin-bottom:10px;">You have more than you think</div>
  <div style="font-family:Inter;font-weight:700;font-size:70px;line-height:0.96;
              color:{DEEP_BLUE};letter-spacing:-4px;margin-bottom:18px;">You can build<br>experience<br><span style="color:{AMBER};font-style:italic;">right now.</span></div>
  <div style="margin-bottom:18px;">{chips_html}</div>
  <div class="cta">
    <div>
      <div>Find your first role at</div>
      <div style="font-family:Inter;font-weight:700;font-size:16px;color:{AMBER};margin-top:4px;">internwise.co.uk →</div>
    </div>
    <div class="arrow">
      <svg width="22" height="22" viewBox="0 0 24 24">
        <path d="M5 12L19 12M14 7L20 12L14 17" stroke="{DEEP_BLUE}" stroke-width="2.5"
              fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Main ──────────────────────────────────────────────────────────────────────
def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Build Experience Carousel v4 (Week 4, Day 5) - hybrid...")
    _logo_b64()

    print("  Fetching 4 unique human photos (slides 1,3,5,7)...")
    photos = {}

    # Slide 1 pinned — clean grey-suit studio portrait, perfect rembg edges
    _pin_a = os.path.join(BASE_DIR, "assets", "pexels_cache", "e73688bb2b4e_nobg.png")
    photos["a"] = _src(_pin_a) if os.path.exists(_pin_a) else ""
    print(f"    ok a (pinned): {_pin_a}")

    # Slide 3 pinned — young man in actual VOLUNTEER t-shirt, clean cutout
    _pin_b = os.path.join(BASE_DIR, "assets", "pexels_cache", "3ae958f15314_nobg.png")
    photos["b"] = _src(_pin_b) if os.path.exists(_pin_b) else ""
    print(f"    ok b (pinned): {_pin_b}")

    photo_queries = [
        ("c", "young woman casual smiling white background studio portrait isolated clean", 5),
        ("d", "young man happy smiling white background studio portrait isolated graduate", 2),
    ]
    for key, query, idx in photo_queries:
        try:
            photos[key] = _src(get_cutout(query, index=idx, orientation="portrait"))
            print(f"    ok {key}")
        except Exception as e:
            print(f"    ! {key} failed: {e}")
            photos[key] = ""

    # Assign: slide 1→a, 3→b, 5→c, 7→d (SVG slides 2,4,6 ignore photo)
    _slide1(os.path.join(campaign_dir, "slide_1.png"), photos.get("a",""))
    for m in METHODS:
        # Human-photo slides use their assigned key; SVG slides pass empty string
        if m["visual"] == "photo_b":
            ph = photos.get("b","")
        elif m["visual"] == "photo_c":
            ph = photos.get("c","")
        else:
            ph = ""
        _method_slide(m, ph, os.path.join(campaign_dir, f"slide_{m['n']}.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photos.get("d",""))
    print("Done - build experience carousel v4 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week4/d5-experience")
