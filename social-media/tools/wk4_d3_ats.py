"""
Internwise — ATS Guide Carousel (Week 4, Day 3) — v4
8-slide carousel: why CVs get filtered before a human reads them
v4: replaced all human photos with topically-relevant SVG illustrations
    (no Pexels, no rembg). Each slide has a custom graphic.
"""
import os, base64
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B";     PURPLE = "#7B5CE6";    MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"; LIGHT_BLUE = "#5FA7E5"

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

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


# ── SVG Illustration helpers ───────────────────────────────────────────────────

def _illus_panel(svg_content):
    """Wraps illustration SVG into the right-half panel."""
    return f"""
<div style="position:absolute;top:0;right:0;width:534px;height:1080px;
            z-index:5;overflow:hidden;">
  <svg width="534" height="1080" viewBox="0 0 534 1080"
       xmlns="http://www.w3.org/2000/svg" style="display:block;">
    {svg_content}
  </svg>
</div>"""

def _mini_cv(x, y, w=58, h=74, fill="rgba(255,255,255,0.08)",
             stroke="rgba(255,255,255,0.25)", header_fill="rgba(255,255,255,0.18)"):
    """Mini CV document icon."""
    lines = "".join(
        f'<rect x="{x+9}" y="{y+22+i*11}" width="{[38,28,34,20][i]}" height="3" rx="1.5" fill="rgba(255,255,255,0.18)"/>'
        for i in range(4)
    )
    return f"""
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"
      fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>
<rect x="{x}" y="{y}" width="{w}" height="14" rx="5"
      fill="{header_fill}"/>
<rect x="{x}" y="{y+9}" width="{w}" height="5" fill="{header_fill}"/>
<rect x="{x+9}" y="{y+7}" width="22" height="5" rx="2.5" fill="rgba(255,255,255,0.45)"/>
{lines}"""

def _x_badge(cx, cy, r=12, color=CORAL):
    d = r * 0.42
    return f"""
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.92"/>
<line x1="{cx-d:.1f}" y1="{cy-d:.1f}" x2="{cx+d:.1f}" y2="{cy+d:.1f}"
      stroke="white" stroke-width="2.2" stroke-linecap="round"/>
<line x1="{cx+d:.1f}" y1="{cy-d:.1f}" x2="{cx-d:.1f}" y2="{cy+d:.1f}"
      stroke="white" stroke-width="2.2" stroke-linecap="round"/>"""

def _check_badge(cx, cy, r=12, color=MINT):
    return f"""
<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.92"/>
<polyline points="{cx-5:.1f},{cy+1:.1f} {cx-1:.1f},{cy+5:.1f} {cx+6:.1f},{cy-4:.1f}"
          stroke="{DEEP_BLUE}" stroke-width="2.2" fill="none"
          stroke-linecap="round" stroke-linejoin="round"/>"""

# ── Illustration 1: ATS Funnel ─────────────────────────────────────────────────
def _illus_hook():
    """Slide 1: CVs enter at top, ATS filters, few pass through."""
    # Background glow
    bg = f'<circle cx="267" cy="460" r="300" fill="{CORAL}" opacity="0.04"/>'

    # 7 mini CVs at top
    positions = [(30,55),(110,50),(190,60),(270,50),(350,55),(430,50),(100,140)]
    cvs_top = "".join(_mini_cv(x, y) for x, y in positions)

    # Arrows pointing down into funnel
    arrows = "".join(
        f'<line x1="{x+29}" y1="{y+74}" x2="{x+29}" y2="{y+100}" stroke="{CORAL}" stroke-width="1.2" opacity="0.35" stroke-dasharray="4,3"/>'
        for x, y in positions
    )

    # Funnel trapezoid
    funnel = f"""
<path d="M 18 200 L 516 200 L 360 380 L 174 380 Z"
      fill="{CORAL}" opacity="0.07"/>
<line x1="18"  y1="200" x2="174" y2="380" stroke="{CORAL}" stroke-width="1.5" opacity="0.3"/>
<line x1="516" y1="200" x2="360" y2="380" stroke="{CORAL}" stroke-width="1.5" opacity="0.3"/>
<line x1="18"  y1="200" x2="516" y2="200" stroke="{CORAL}" stroke-width="1"   opacity="0.2"/>"""

    # ATS chip
    chip = f"""
<rect x="162" y="385" width="210" height="88" rx="14"
      fill="{DEEP_BLUE}" stroke="{AMBER}" stroke-width="1.5" opacity="0.95"/>
<text x="267" y="415" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="11" letter-spacing="3"
      fill="{AMBER}" opacity="0.7">APPLICANT TRACKING</text>
<text x="267" y="447" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="22" letter-spacing="1"
      fill="white">⚙ ATS FILTER</text>
<text x="267" y="465" text-anchor="middle"
      font-family="Inter" font-weight="400" font-size="11" letter-spacing="1"
      fill="rgba(255,255,255,0.4)">automated screening</text>"""

    # Pipe down from chip
    pipe = f'<line x1="267" y1="473" x2="267" y2="530" stroke="{CORAL}" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.4"/>'

    # Output: 6 rejected (X), 1 accepted (check)
    rej_pos = [(30,540),(115,555),(200,535),(370,545),(450,535),(490,570)]
    rejected = "".join(
        _mini_cv(x, y, fill=f"rgba(255,107,107,0.1)", stroke=f"rgba(255,107,107,0.3)") +
        _x_badge(x+29, y+37, r=14)
        for x, y in rej_pos
    )

    accepted = (
        _mini_cv(240, 540, fill="rgba(127,219,182,0.15)", stroke=MINT, header_fill=f"rgba(127,219,182,0.35)") +
        _check_badge(269, 577, r=16, color=MINT)
    )

    # Stat
    stat = f"""
<text x="267" y="660" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="64" fill="{CORAL}" opacity="0.9">75%</text>
<text x="267" y="690" text-anchor="middle"
      font-family="DM Sans,sans-serif" font-weight="600" font-size="15" fill="rgba(255,255,255,0.45)"
      letter-spacing="0.5">of CVs filtered before a human sees them</text>"""

    return bg + cvs_top + arrows + funnel + chip + pipe + rejected + accepted + stat


# ── Illustration 2: ATS pipeline flow ────────────────────────────────────────
def _illus_ats_flow():
    """Slide 2: 4-step ATS pipeline: Submit → Scan → Score → Result."""
    steps = [
        (LIGHT_BLUE, "📄", "YOU SUBMIT",   "CV uploaded online"),
        (AMBER,      "⚙",  "ATS SCANS",    "Keywords + structure checked"),
        (CORAL,      "▣",  "CV SCORED",    "Below threshold = auto-reject"),
        (MINT,       "👤", "HUMAN READS",  "Only top scorers pass"),
    ]
    out = f'<circle cx="267" cy="500" r="320" fill="rgba(255,255,255,0.02)"/>'

    for i, (color, icon, label, sub) in enumerate(steps):
        cy = 160 + i * 195
        # Circle icon
        out += f'<circle cx="267" cy="{cy}" r="52" fill="{color}" opacity="0.12"/>'
        out += f'<circle cx="267" cy="{cy}" r="44" fill="{color}" opacity="0.18" stroke="{color}" stroke-width="1.5"/>'
        out += f'<text x="267" y="{cy+10}" text-anchor="middle" font-size="28">{icon}</text>'
        # Label
        out += f'<text x="267" y="{cy+68}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="14" fill="white" letter-spacing="2">{label}</text>'
        out += f'<text x="267" y="{cy+86}" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="500" font-size="13" fill="rgba(255,255,255,0.45)">{sub}</text>'
        # Connector arrow
        if i < 3:
            ay = cy + 54
            out += f'<line x1="267" y1="{ay}" x2="267" y2="{ay+94}" stroke="{color}" stroke-width="1.5" stroke-dasharray="5,4" opacity="0.4"/>'
            out += f'<polygon points="261,{ay+96} 267,{ay+110} 273,{ay+96}" fill="{color}" opacity="0.4"/>'
    return out


# ── Illustration 3: Wrong Format (multi-column CV) ────────────────────────────
def _illus_cv_format():
    """Slide 3: CV with two-column layout - ATS can't parse it."""
    # CV doc base (large, centered)
    doc_x, doc_y, doc_w, doc_h = 84, 120, 366, 480
    out = f"""
<rect x="{doc_x}" y="{doc_y}" width="{doc_w}" height="{doc_h}" rx="10"
      fill="white" opacity="0.94" filter="drop-shadow(0 8px 24px rgba(0,0,0,0.3))"/>
<!-- Header -->
<rect x="{doc_x}" y="{doc_y}" width="{doc_w}" height="50" rx="10" fill="{DEEP_BLUE}"/>
<rect x="{doc_x}" y="{doc_y+38}" width="{doc_w}" height="12" fill="{DEEP_BLUE}"/>
<rect x="{doc_x+16}" y="{doc_y+14}" width="90" height="12" rx="6" fill="rgba(255,255,255,0.8)"/>
<rect x="{doc_x+16}" y="{doc_y+30}" width="60" height="7" rx="3.5" fill="rgba(255,255,255,0.4)"/>"""

    # Two-column layout divider
    col_div = doc_x + 164
    out += f"""
<!-- Left column (sidebar) -->
<rect x="{doc_x+12}" y="{doc_y+60}" width="{col_div-doc_x-20}" height="400" rx="4"
      fill="{CORAL}" opacity="0.06" stroke="{CORAL}" stroke-width="1.5" stroke-dasharray="5,3"/>
<!-- Right column (main) -->
<rect x="{col_div+8}" y="{doc_y+60}" width="{doc_x+doc_w-col_div-20}" height="400" rx="4"
      fill="{CORAL}" opacity="0.06" stroke="{CORAL}" stroke-width="1.5" stroke-dasharray="5,3"/>"""

    # Filler lines in left col
    for i in range(9):
        lw = [70, 50, 65, 45, 70, 55, 60, 42, 68][i]
        out += f'<rect x="{doc_x+16}" y="{doc_y+72+i*36}" width="{lw}" height="6" rx="3" fill="rgba(0,0,0,0.12)"/>'

    # Filler lines in right col
    for i in range(9):
        lw = [140, 120, 138, 100, 130, 115, 128, 108, 135][i]
        out += f'<rect x="{col_div+14}" y="{doc_y+72+i*36}" width="{lw}" height="6" rx="3" fill="rgba(0,0,0,0.12)"/>'

    # Big X over the two-column layout
    out += f"""
<line x1="{doc_x+20}" y1="{doc_y+65}" x2="{doc_x+doc_w-20}" y2="{doc_y+doc_h-15}"
      stroke="{CORAL}" stroke-width="3" stroke-linecap="round" opacity="0.5"/>
<line x1="{doc_x+doc_w-20}" y1="{doc_y+65}" x2="{doc_x+20}" y2="{doc_y+doc_h-15}"
      stroke="{CORAL}" stroke-width="3" stroke-linecap="round" opacity="0.5"/>"""

    # Warning badge
    out += f"""
<rect x="130" y="630" width="274" height="52" rx="10"
      fill="{CORAL}" opacity="0.15" stroke="{CORAL}" stroke-width="1.5"/>
<text x="267" y="651" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="13" fill="{CORAL}" letter-spacing="1">ATS CANNOT PARSE COLUMNS</text>
<text x="267" y="670" text-anchor="middle" font-family="DM Sans,sans-serif"
      font-size="13" fill="rgba(255,255,255,0.5)">Use single-column layout only</text>"""
    return out


# ── Illustration 4: Missing Keywords ─────────────────────────────────────────
def _illus_cv_keywords():
    """Slide 4: JD vs CV keyword comparison with match/mismatch rows + score gauge."""
    out = f'<circle cx="267" cy="500" r="300" fill="{AMBER}" opacity="0.035"/>'

    # Column headers
    out += f"""
<text x="128" y="88" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="11" fill="{MINT}" letter-spacing="3" opacity="0.9">JOB DESCRIPTION</text>
<text x="392" y="88" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="11" fill="{CORAL}" letter-spacing="3" opacity="0.9">YOUR CV</text>
<line x1="267" y1="68" x2="267" y2="820" stroke="rgba(255,255,255,0.07)" stroke-width="1"/>"""

    # Keyword pairs: (jd_term, cv_term, match)
    pairs = [
        ("Data Analyst",       "Data Specialist",     False),
        ("Python",             "Python",              True),
        ("SQL",                "Database querying",   False),
        ("Stakeholder reports","Communication skills", False),
        ("Excel / Power BI",   "MS Office",           False),
        ("Agile methodology",  "Agile methodology",   True),
    ]

    for i, (jd, cv, match) in enumerate(pairs):
        row_y = 108 + i * 108
        badge_color = MINT if match else CORAL
        cv_color    = MINT if match else CORAL
        jd_color    = MINT

        # JD pill
        jd_w = min(len(jd) * 9 + 24, 210)
        out += f"""
<rect x="{24}" y="{row_y}" width="{jd_w}" height="32" rx="8"
      fill="{jd_color}" opacity="0.18" stroke="{jd_color}" stroke-width="1.5"/>
<text x="{24 + jd_w//2}" y="{row_y+21}" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="13" fill="{jd_color}">{jd}</text>"""

        # CV pill
        cv_w = min(len(cv) * 9 + 24, 210)
        out += f"""
<rect x="{288}" y="{row_y}" width="{cv_w}" height="32" rx="8"
      fill="{cv_color}" opacity="0.18" stroke="{cv_color}" stroke-width="1.5"/>
<text x="{288 + cv_w//2}" y="{row_y+21}" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="13" fill="{cv_color}">{cv}</text>"""

        # Centre badge (check or X)
        if match:
            out += _check_badge(267, row_y+16, r=14, color=MINT)
        else:
            out += _x_badge(267, row_y+16, r=14, color=CORAL)

        # Sub-rule line
        row_sub = f"exact match" if match else "not matched"
        sub_color = MINT if match else "rgba(255,107,107,0.6)"
        out += f"""<text x="267" y="{row_y+52}" text-anchor="middle"
      font-family="DM Sans,sans-serif" font-size="11" fill="{sub_color}"
      opacity="0.85">{row_sub}</text>"""

    # Score gauge at bottom
    matched = sum(1 for _,_,m in pairs if m)
    total   = len(pairs)
    pct     = int(matched / total * 100)
    bar_w   = int(414 * matched / total)

    out += f"""
<rect x="44" y="784" width="446" height="86" rx="14"
      fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
<text x="267" y="810" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="12" fill="rgba(255,255,255,0.45)" letter-spacing="2">ATS KEYWORD MATCH SCORE</text>
<rect x="60" y="820" width="414" height="16" rx="8" fill="rgba(255,255,255,0.08)"/>
<rect x="60" y="820" width="{bar_w}" height="16" rx="8" fill="{CORAL}" opacity="0.75"/>
<text x="267" y="856" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="14" fill="{CORAL}">{pct}% match - auto-rejected</text>"""

    return out


# ── Illustration 5: Wrong Section Headings ────────────────────────────────────
def _illus_cv_headings():
    """Slide 5: Wrong section names vs ATS-standard names."""
    headings = [
        ('"My Journey"',      "Work Experience", False),
        ('"Things I\'ve built"', "Projects",      False),
        ('"What I know"',     "Skills",          False),
        ('"About me"',        "Personal Profile",False),
    ]
    out = f"""
<text x="267" y="112" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="16" fill="rgba(255,255,255,0.35)" letter-spacing="2">SECTION HEADING</text>
<text x="155" y="140" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="700"
      font-size="13" fill="{CORAL}" letter-spacing="1">WHAT YOU WROTE</text>
<text x="379" y="140" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="700"
      font-size="13" fill="{MINT}" letter-spacing="1">ATS EXPECTS</text>
<line x1="267" y1="150" x2="267" y2="780" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>"""

    for i, (wrong, right, _) in enumerate(headings):
        row_y = 180 + i * 155
        # Wrong (left)
        out += f"""
<rect x="22" y="{row_y}" width="222" height="56" rx="10"
      fill="{CORAL}" opacity="0.1" stroke="{CORAL}" stroke-width="1.2"/>
<text x="133" y="{row_y+23}" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="15" fill="{CORAL}">{wrong}</text>
{_x_badge(133, row_y+44, r=11, color=CORAL)}"""
        # Arrow
        out += f'<text x="267" y="{row_y+32}" text-anchor="middle" font-size="18" fill="rgba(255,255,255,0.3)">→</text>'
        # Correct (right)
        out += f"""
<rect x="290" y="{row_y}" width="222" height="56" rx="10"
      fill="{MINT}" opacity="0.1" stroke="{MINT}" stroke-width="1.2"/>
<text x="401" y="{row_y+23}" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="15" fill="{MINT}">{right}</text>
{_check_badge(401, row_y+44, r=11, color=MINT)}"""

    # Rule below
    out += f"""
<rect x="22" y="830" width="490" height="54" rx="12"
      fill="{MINT}" opacity="0.08" stroke="{MINT}" stroke-width="1"/>
<text x="267" y="852" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="13" fill="{MINT}" letter-spacing="1">USE EXACT STANDARD HEADINGS</text>
<text x="267" y="872" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="13"
      fill="rgba(255,255,255,0.4)">ATS won't find what it can't recognise</text>"""
    return out


# ── Illustration 6: Fancy Formatting kills ────────────────────────────────────
def _illus_cv_fancy():
    """Slide 6: Actually-rendered problematic elements with X strikes."""
    out = f'<circle cx="267" cy="500" r="300" fill="{PURPLE}" opacity="0.04"/>'

    # ── Item 1: Skill progress bar ──────────────────────────────────────────
    y1 = 80
    out += f"""
<rect x="32" y="{y1}" width="470" height="100" rx="12"
      fill="rgba(255,255,255,0.06)" stroke="rgba(255,107,107,0.35)" stroke-width="1.5"/>
<text x="52" y="{y1+22}" font-family="Inter" font-weight="700" font-size="11"
      fill="rgba(255,255,255,0.3)" letter-spacing="2">SKILL BAR</text>
<text x="52" y="{y1+46}" font-family="Inter" font-weight="600" font-size="14"
      fill="rgba(255,255,255,0.75)">Python</text>
<rect x="52" y="{y1+54}" width="270" height="12" rx="6" fill="rgba(255,255,255,0.1)"/>
<rect x="52" y="{y1+54}" width="216" height="12" rx="6" fill="{PURPLE}" opacity="0.8"/>
<text x="332" y="{y1+64}" font-family="Inter" font-weight="700" font-size="12"
      fill="{PURPLE}" opacity="0.9">80%</text>
<text x="52" y="{y1+84}" font-family="Inter" font-weight="600" font-size="14"
      fill="rgba(255,255,255,0.75)">SQL</text>
<rect x="106" y="{y1+72}" width="185" height="12" rx="6" fill="rgba(255,255,255,0.1)"/>
<rect x="106" y="{y1+72}" width="111" height="12" rx="6" fill="{LIGHT_BLUE}" opacity="0.8"/>
<text x="300" y="{y1+82}" font-family="Inter" font-weight="700" font-size="12"
      fill="{LIGHT_BLUE}" opacity="0.9">60%</text>"""
    out += _x_badge(470, y1+18, r=16, color=CORAL)
    # Strikethrough diagonal
    out += f'<line x1="32" y1="{y1+8}" x2="502" y2="{y1+92}" stroke="{CORAL}" stroke-width="2" opacity="0.35" stroke-linecap="round"/>'

    # ── Item 2: Multi-column skill chips ───────────────────────────────────
    y2 = 210
    chips = ["Python", "SQL", "Excel", "Power BI", "Tableau"]
    out += f"""
<rect x="32" y="{y2}" width="470" height="80" rx="12"
      fill="rgba(255,255,255,0.06)" stroke="rgba(255,107,107,0.35)" stroke-width="1.5"/>
<text x="52" y="{y2+20}" font-family="Inter" font-weight="700" font-size="11"
      fill="rgba(255,255,255,0.3)" letter-spacing="2">SKILL CHIPS</text>"""
    cx_chip = 52
    for chip in chips:
        cw = len(chip) * 9 + 20
        out += f"""
<rect x="{cx_chip}" y="{y2+30}" width="{cw}" height="28" rx="6"
      fill="{LIGHT_BLUE}" opacity="0.25" stroke="{LIGHT_BLUE}" stroke-width="1"/>
<text x="{cx_chip + cw//2}" y="{y2+49}" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="12" fill="{LIGHT_BLUE}">{chip}</text>"""
        cx_chip += cw + 8
    out += _x_badge(470, y2+18, r=16, color=CORAL)
    out += f'<line x1="32" y1="{y2+8}" x2="502" y2="{y2+72}" stroke="{CORAL}" stroke-width="2" opacity="0.35" stroke-linecap="round"/>'

    # ── Item 3: Logo / crest placeholder ──────────────────────────────────
    y3 = 320
    out += f"""
<rect x="32" y="{y3}" width="470" height="88" rx="12"
      fill="rgba(255,255,255,0.06)" stroke="rgba(255,107,107,0.35)" stroke-width="1.5"/>
<text x="52" y="{y3+20}" font-family="Inter" font-weight="700" font-size="11"
      fill="rgba(255,255,255,0.3)" letter-spacing="2">COMPANY LOGO / CREST</text>
<rect x="52" y="{y3+28}" width="52" height="48" rx="6"
      fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.2)" stroke-width="1"/>
<text x="78" y="{y3+57}" text-anchor="middle" font-size="22">🏛</text>
<text x="120" y="{y3+46}" font-family="Inter" font-weight="700" font-size="14"
      fill="rgba(255,255,255,0.7)">University of Oxford</text>
<text x="120" y="{y3+65}" font-family="DM Sans,sans-serif" font-size="12"
      fill="rgba(255,255,255,0.4)">BA Economics  |  2:1  |  2024</text>"""
    out += _x_badge(470, y3+18, r=16, color=CORAL)
    out += f'<line x1="32" y1="{y3+8}" x2="502" y2="{y3+80}" stroke="{CORAL}" stroke-width="2" opacity="0.35" stroke-linecap="round"/>'

    # ── Item 4: Coloured section box ──────────────────────────────────────
    y4 = 438
    out += f"""
<rect x="32" y="{y4}" width="470" height="72" rx="12"
      fill="rgba(255,255,255,0.06)" stroke="rgba(255,107,107,0.35)" stroke-width="1.5"/>
<text x="52" y="{y4+20}" font-family="Inter" font-weight="700" font-size="11"
      fill="rgba(255,255,255,0.3)" letter-spacing="2">COLOURED SECTION HEADER</text>
<rect x="52" y="{y4+28}" width="340" height="30" rx="6"
      fill="{AMBER}" opacity="0.35"/>
<text x="222" y="{y4+48}" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="14" fill="{DEEP_BLUE}" opacity="0.9">▶  Technical Skills</text>"""
    out += _x_badge(470, y4+18, r=16, color=CORAL)
    out += f'<line x1="32" y1="{y4+8}" x2="502" y2="{y4+64}" stroke="{CORAL}" stroke-width="2" opacity="0.35" stroke-linecap="round"/>'

    # ── Divider + fix banner ───────────────────────────────────────────────
    out += f"""
<line x1="32" y1="540" x2="502" y2="540" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
<rect x="32" y="558" width="470" height="76" rx="14"
      fill="{MINT}" opacity="0.09" stroke="{MINT}" stroke-width="1.2"/>
<text x="267" y="585" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="13" fill="{MINT}" letter-spacing="2">THE FIX: PLAIN TEXT ONLY</text>
<text x="267" y="609" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="600"
      font-size="14" fill="rgba(255,255,255,0.55)">Bold headings. Bullet points.</text>
<text x="267" y="628" text-anchor="middle" font-family="DM Sans,sans-serif" font-weight="600"
      font-size="14" fill="rgba(255,255,255,0.55)">Nothing else.</text>

<!-- ATS cannot read this -->
<text x="267" y="690" text-anchor="middle" font-family="Inter" font-weight="700"
      font-size="36" fill="{CORAL}" opacity="0.18" letter-spacing="-1">ATS CANNOT READ THIS</text>"""

    return out


# ── Illustration 7: ATS-proof checklist CV ───────────────────────────────────
def _illus_checklist():
    """Slide 7: Large single-column CV with annotated section checkmarks."""
    dx, dy, dw, dh = 38, 48, 458, 820
    out = ""

    # Drop shadow
    out += f'<rect x="{dx+6}" y="{dy+6}" width="{dw}" height="{dh}" rx="12" fill="rgba(0,0,0,0.35)"/>'

    # CV body
    out += f"""
<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="12"
      fill="white" opacity="0.97"/>"""

    # Header band
    out += f"""
<rect x="{dx}" y="{dy}" width="{dw}" height="70" rx="12" fill="{MINT}" opacity="0.9"/>
<rect x="{dx}" y="{dy+58}" width="{dw}" height="12" fill="{MINT}" opacity="0.9"/>"""

    # Name + title in header
    out += f"""
<rect x="{dx+20}" y="{dy+14}" width="130" height="14" rx="7"
      fill="{DEEP_BLUE}" opacity="0.55"/>
<rect x="{dx+20}" y="{dy+36}" width="82" height="8" rx="4"
      fill="{DEEP_BLUE}" opacity="0.32"/>"""

    # .docx badge on header — rule 1
    out += f"""
<rect x="{dx+dw-110}" y="{dy+18}" width="84" height="26" rx="6"
      fill="{DEEP_BLUE}" opacity="0.35"/>
<text x="{dx+dw-68}" y="{dy+36}" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="11"
      fill="{MINT}" letter-spacing="1">.docx format</text>"""
    out += _check_badge(dx+dw-118, dy+31, r=11, color=MINT)

    # Single-column indicator — rule 2
    out += f"""
<line x1="{dx+dw//2}" y1="{dy+70}" x2="{dx+dw//2}" y2="{dy+dh}"
      stroke="{MINT}" stroke-width="1" stroke-dasharray="4,4" opacity="0.15"/>
<text x="{dx+dw//2}" y="{dy+84}" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="9"
      fill="{MINT}" opacity="0.4" letter-spacing="2">SINGLE COLUMN</text>"""
    out += _check_badge(dx+dw-14, dy+76, r=11, color=MINT)

    # ── Sections ─────────────────────────────────────────────────────────
    sections = [
        ("Work Experience", [
            (220, "Software Intern - Tech company, 2024"),
            (180, "Analysed user data and presented findings"),
            (200, "Built internal dashboard using Python + SQL"),
        ]),
        ("Education", [
            (200, "BSc Computer Science  |  2:1  |  2024"),
            (160, "Relevant modules: Databases, Data Analysis"),
        ]),
        ("Skills", [
            (260, "Python, SQL, Excel, Power BI, Tableau"),
            (180, "Agile methodology, stakeholder reporting"),
        ]),
        ("Projects", [
            (200, "Sales forecasting model - Python, Pandas"),
            (170, "Visualised 12-month revenue trend (Excel)"),
        ]),
    ]

    cy = dy + 96
    for sec_idx, (sec_name, lines) in enumerate(sections):
        sec_color = DEEP_BLUE

        # Section heading label
        out += f"""
<rect x="{dx+14}" y="{cy}" width="{dw-28}" height="22" rx="4"
      fill="{DEEP_BLUE}" opacity="0.08"/>
<text x="{dx+20}" y="{cy+15}" font-family="Inter" font-weight="700"
      font-size="12" fill="{DEEP_BLUE}" opacity="0.75"
      letter-spacing="1">{sec_name.upper()}</text>"""
        out += _check_badge(dx+dw-22, cy+11, r=11, color=MINT)
        cy += 30

        for lw, label_text in lines:
            # bullet dot
            out += f'<circle cx="{dx+22}" cy="{cy+6}" r="2.5" fill="{DEEP_BLUE}" opacity="0.3"/>'
            # text line (placeholder bars)
            out += f'<rect x="{dx+32}" y="{cy+2}" width="{lw}" height="8" rx="4" fill="{DEEP_BLUE}" opacity="0.13"/>'
            cy += 18

        cy += 10

        # Section divider
        if sec_idx < len(sections) - 1:
            out += f'<line x1="{dx+14}" y1="{cy}" x2="{dx+dw-14}" y2="{cy}" stroke="{DEEP_BLUE}" stroke-width="0.8" opacity="0.1"/>'
            cy += 10

    # "No graphics / No text boxes" badge at bottom of doc
    out += f"""
<rect x="{dx+14}" y="{dy+dh-52}" width="{dw-28}" height="36" rx="8"
      fill="{MINT}" opacity="0.1" stroke="{MINT}" stroke-width="1"/>
<text x="{dx+dw//2}" y="{dy+dh-30}" text-anchor="middle"
      font-family="Inter" font-weight="700" font-size="11"
      fill="{MINT}" letter-spacing="1">NO GRAPHICS · NO TEXT BOXES · KEYWORDS MATCHED</text>"""
    out += _check_badge(dx+28, dy+dh-34, r=11, color=MINT)
    out += _check_badge(dx+dw-28, dy+dh-34, r=11, color=MINT)

    # ATS-APPROVED stamp (rotated)
    out += f"""
<g transform="translate(390,780) rotate(-22)">
  <rect x="-68" y="-26" width="136" height="52" rx="8"
        fill="none" stroke="{MINT}" stroke-width="3" opacity="0.55"/>
  <text x="0" y="-4" text-anchor="middle" font-family="Inter" font-weight="700"
        font-size="14" fill="{MINT}" opacity="0.6" letter-spacing="3">ATS</text>
  <text x="0" y="16" text-anchor="middle" font-family="Inter" font-weight="700"
        font-size="14" fill="{MINT}" opacity="0.6" letter-spacing="3">APPROVED</text>
</g>"""

    return out


# ── Slide shell ───────────────────────────────────────────────────────────────
def _dark_slide_shell(f, accent="", badge_text="", badge_bg=None, badge_color=None):
    badge_bg = badge_bg or CORAL
    badge_color = badge_color or "white"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.bar{{position:absolute;top:0;left:0;width:6px;height:100%;background:{accent or CORAL};z-index:10;
      box-shadow:0 0 20px {accent or CORAL}55;}}
.num{{position:absolute;top:48px;right:44px;font-family:Inter;font-weight:700;font-size:14px;
    color:rgba(255,255,255,0.3);letter-spacing:2px;z-index:25;}}
.url{{position:absolute;bottom:36px;right:44px;font-family:Inter;font-weight:700;font-size:14px;
    color:rgba(255,255,255,0.2);z-index:25;}}
.badge-pill{{position:absolute;top:44px;right:44px;background:{badge_bg};color:{badge_color};
    padding:10px 22px;border-radius:50px;font-family:Inter;font-weight:700;font-size:13px;
    letter-spacing:2px;text-transform:uppercase;z-index:25;}}
.col{{position:absolute;top:44px;left:50px;right:534px;
      display:flex;flex-direction:column;gap:0;z-index:20;overflow:hidden;max-height:992px;}}
</style>"""


# ── Slide 1: Hook ─────────────────────────────────────────────────────────────
def _slide1(out):
    f = _fonts(); lb = _logo_b64()
    html = f"""{_dark_slide_shell(f, CORAL, "ATS guide", CORAL, "white")}
</head><body><div class="c">
<div class="grain"></div>
{_illus_panel(_illus_hook())}
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:25;">
<div class="badge-pill">ATS guide</div>
<div class="col">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
              text-transform:uppercase;letter-spacing:4px;margin-top:108px;margin-bottom:12px;">The CV filter you can't see</div>
  <div style="font-family:Inter;font-weight:700;font-size:74px;line-height:0.95;
              color:white;letter-spacing:-4px;margin-bottom:18px;">Most CVs<br>never reach<br>a <span style="color:{CORAL};">human.</span></div>
  <div style="width:70px;height:4px;background:{CORAL};border-radius:2px;margin-bottom:18px;"></div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:25px;
              color:rgba(255,255,255,0.65);line-height:1.4;">Here's why - and exactly<br>how to fix it.</div>
</div>
<div style="position:absolute;bottom:44px;left:50px;z-index:20;
    font-family:Inter;font-weight:700;font-size:20px;color:rgba(255,255,255,0.38);">
  Swipe to see what's filtering you out <strong style="color:rgba(255,255,255,0.7);">→</strong>
</div>
{_spark(26,160,420,CORAL,0.45)}
</div></body></html>"""
    _render(html, out)


# ── Slide 2: What is ATS ──────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts(); lb = _logo_b64()
    steps = [
        (CORAL,  "1", "You submit your CV online."),
        (AMBER,  "2", "Software scans it for keywords, structure, and format."),
        (MINT,   "3", "Your CV is scored. Below the threshold, it's auto-rejected."),
        (PURPLE, "4", "Only top-scoring CVs ever reach a human recruiter."),
    ]
    steps_html = "".join(f"""
<div style="display:flex;align-items:flex-start;gap:14px;
            padding:14px 16px;background:rgba(255,255,255,0.06);
            border-radius:10px;border-left:3px solid {c};">
  <div style="width:42px;height:42px;border-radius:50%;flex-shrink:0;
              background:{c};display:flex;align-items:center;justify-content:center;
              font-family:Inter;font-weight:700;font-size:18px;
              color:{'#162d4a' if c in (AMBER,MINT) else 'white'};">{n}</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:21px;
              color:rgba(255,255,255,0.82);line-height:1.4;padding-top:8px;">{t}</div>
</div>""" for c,n,t in steps)

    html = f"""{_dark_slide_shell(f, CORAL)}
</head><body><div class="c">
<div class="grain"></div>
<div class="bar"></div>
{_illus_panel(_illus_ats_flow())}
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:50px;height:66px;opacity:0.95;z-index:25;">
<div class="num">01 / 06</div>
<div class="url">internwise.co.uk</div>
<div class="col">
  <div style="align-self:flex-start;background:{CORAL};color:white;
              padding:7px 18px;border-radius:50px;font-family:Inter;font-weight:700;
              font-size:12px;letter-spacing:2px;text-transform:uppercase;
              margin-top:108px;margin-bottom:12px;">What is ATS?</div>
  <div style="font-family:Inter;font-weight:700;font-size:50px;line-height:1.0;
              color:white;letter-spacing:-2px;margin-bottom:10px;">The software that<br>reads your CV first.</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:21px;
              color:rgba(255,255,255,0.55);line-height:1.4;margin-bottom:14px;">Most large employers use Applicant Tracking<br>Systems. Here's how the filter works:</div>
  <div style="display:flex;flex-direction:column;gap:9px;">{steps_html}</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── ATS killer slides 3-6 ─────────────────────────────────────────────────────
ATS_KILLERS = [
    {
        "n": 3, "num": "02 / 06", "accent": CORAL,
        "killer_label": "ATS killer #1",
        "title": "Wrong format or layout.",
        "kills": [
            (CORAL, "Tables and columns",      "ATS reads left-to-right in one pass. Columns scramble the output."),
            (CORAL, "Text in headers/footers", "Most ATS systems ignore headers and footers entirely."),
            (CORAL, "Graphics and icons",       "ATS can't read images. Skills in an icon simply vanish."),
            (CORAL, "PDF (sometimes)",          "Some ATS still struggle with PDFs. Use .docx unless told otherwise."),
        ],
        "fix": "Single-column layout. No tables. No graphics. No headers or footers for key content.",
        "illus": "_illus_cv_format",
    },
    {
        "n": 4, "num": "03 / 06", "accent": AMBER,
        "killer_label": "ATS killer #2",
        "title": "Missing the right keywords.",
        "kills": [
            (AMBER, "Paraphrasing job titles",   "If the JD says 'Data Analyst', don't write 'Data Specialist'. Match exactly."),
            (AMBER, "Generic skill claims",       "'Good communication' scores nothing. Name the specific tool or method."),
            (AMBER, "No role-specific language",  "ATS searches for the exact phrases from the job description."),
            (AMBER, "Keywords buried at the end", "Put role titles and key skills near the top of each section."),
        ],
        "fix": "Read the job description. Use its exact phrases in your CV. That's what ATS searches for.",
        "illus": "_illus_cv_keywords",
    },
    {
        "n": 5, "num": "04 / 06", "accent": MINT,
        "killer_label": "ATS killer #3",
        "title": "Non-standard section headings.",
        "kills": [
            (MINT, '"My journey"',         "ATS looks for 'Work Experience'. Not creative alternatives."),
            (MINT, '"Things I\'ve built"', "Call it 'Projects'. Every time."),
            (MINT, '"What I know"',        "Call it 'Skills'. Keep headings literal."),
            (MINT, "Missing sections",     "Work Experience, Education, Skills - all three must be clearly labelled."),
        ],
        "fix": "Use exactly: Work Experience / Education / Skills / Projects. No variations.",
        "illus": "_illus_cv_headings",
    },
    {
        "n": 6, "num": "05 / 06", "accent": PURPLE,
        "killer_label": "ATS killer #4",
        "title": "Fancy formatting that breaks the scan.",
        "kills": [
            (PURPLE, "Skill progress bars",      "A 4/5 bar for Python tells ATS nothing. Write 'Python (proficient)' instead."),
            (PURPLE, "Multi-column skill chips",  "Decorative chips get scrambled. Use a comma-separated skills list."),
            (PURPLE, "Logos and crests",          "Company logos and school crests cause parsing errors. Remove them."),
            (PURPLE, "Coloured or shaded boxes",  "Highlighting sections with background colour confuses text extraction."),
        ],
        "fix": "Plain text only. Bold for headings and job titles. Bullet points for content. Nothing else.",
        "illus": "_illus_cv_fancy",
    },
]

ILLUS_MAP = {
    "_illus_cv_format":   _illus_cv_format,
    "_illus_cv_keywords": _illus_cv_keywords,
    "_illus_cv_headings": _illus_cv_headings,
    "_illus_cv_fancy":    _illus_cv_fancy,
}

def _killer_slide(k, out):
    f = _fonts(); lb = _logo_b64()
    accent = k["accent"]
    accent_text = DEEP_BLUE if accent in (AMBER, MINT) else "white"
    illus_svg = ILLUS_MAP[k["illus"]]()

    kills_html = "".join(f"""
<div style="display:flex;align-items:flex-start;gap:12px;
            padding:12px 14px;background:rgba(255,255,255,0.05);
            border-radius:9px;border-left:3px solid {accent};">
  <div style="width:20px;height:20px;flex-shrink:0;margin-top:2px;">
    <svg width="20" height="20" viewBox="0 0 20 20">
      <circle cx="10" cy="10" r="9" fill="{CORAL}" opacity="0.85"/>
      <line x1="6" y1="6" x2="14" y2="14" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
      <line x1="14" y1="6" x2="6" y2="14" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
  </div>
  <div>
    <span style="font-family:Inter;font-weight:700;font-size:21px;color:{accent};">{lbl} - </span>
    <span style="font-family:'DM Sans';font-weight:500;font-size:21px;color:rgba(255,255,255,0.68);">{desc}</span>
  </div>
</div>""" for _,lbl,desc in k["kills"])

    html = f"""{_dark_slide_shell(f, accent)}
</head><body><div class="c">
<div class="grain"></div>
<div class="bar"></div>
{_illus_panel(illus_svg)}
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:50px;height:66px;opacity:0.95;z-index:25;">
<div class="num">{k['num']}</div>
<div class="url">internwise.co.uk</div>
<div class="col">
  <div style="align-self:flex-start;background:{accent};color:{accent_text};
              padding:7px 18px;border-radius:50px;font-family:Inter;font-weight:700;
              font-size:12px;letter-spacing:2px;text-transform:uppercase;
              margin-top:108px;margin-bottom:12px;">{k['killer_label']}</div>
  <div style="font-family:Inter;font-weight:700;font-size:50px;line-height:1.0;
              color:white;letter-spacing:-1.5px;margin-bottom:14px;">{k['title']}</div>
  <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:14px;">{kills_html}</div>
  <div style="background:rgba(127,219,182,0.08);border-radius:12px;padding:14px 16px;
              border:1px solid rgba(127,219,182,0.25);border-left:4px solid {MINT};">
    <div style="font-family:'DM Sans';font-weight:700;font-size:15px;
                color:{MINT};text-transform:uppercase;letter-spacing:2px;">The fix</div>
    <div style="font-family:'DM Sans';font-weight:600;font-size:21px;
                color:rgba(255,255,255,0.78);margin-top:5px;line-height:1.4;">{k['fix']}</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: ATS-proof checklist ──────────────────────────────────────────────
def _slide7(out):
    f = _fonts(); lb = _logo_b64()
    checks = [
        (".docx format",       "unless the job post specifies PDF"),
        ("Single column",      "no tables, no multi-column layouts"),
        ("Standard headings",  "Work Experience / Education / Skills / Projects"),
        ("Keywords matched",   "copy exact phrases from the job description"),
        ("No graphics",        "no icons, logos, progress bars, or shaded boxes"),
        ("No text boxes",      "all content in the main body only"),
    ]
    checks_html = "".join(f"""
<div style="display:flex;align-items:center;gap:13px;
            padding:12px 15px;background:rgba(127,219,182,0.07);
            border-radius:10px;border:1px solid rgba(127,219,182,0.18);">
  <div style="width:32px;height:32px;border-radius:50%;flex-shrink:0;
              background:{MINT};display:flex;align-items:center;justify-content:center;">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <polyline points="2.5 8 6 12 13.5 4" stroke="{DEEP_BLUE}" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
  <div>
    <span style="font-family:Inter;font-weight:700;font-size:24px;color:{MINT};">{lbl} - </span>
    <span style="font-family:'DM Sans';font-weight:500;font-size:21px;color:rgba(255,255,255,0.65);">{desc}</span>
  </div>
</div>""" for lbl,desc in checks)

    html = f"""{_dark_slide_shell(f, MINT, "ATS-proof checklist", MINT, DEEP_BLUE)}
</head><body><div class="c">
<div class="grain"></div>
{_illus_panel(_illus_checklist())}
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:25;">
<div class="badge-pill">ATS-proof checklist</div>
<div class="col">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{MINT};
              text-transform:uppercase;letter-spacing:4px;margin-top:108px;margin-bottom:12px;">Before you submit</div>
  <div style="font-family:Inter;font-weight:700;font-size:60px;line-height:0.96;
              color:white;letter-spacing:-3px;margin-bottom:16px;">6 rules that<br>get you <span style="color:{MINT};">through.</span></div>
  <div style="height:2px;background:rgba(255,255,255,0.1);margin-bottom:14px;"></div>
  <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:14px;">{checks_html}</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:21px;
              color:rgba(255,255,255,0.4);">A clean CV gets <strong style="color:rgba(255,255,255,0.78);">read by a human.</strong> That's the only goal.</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 8: CTA ──────────────────────────────────────────────────────────────
def _slide8(out):
    f = _fonts(); lb = _logo_b64()
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
.col{{position:absolute;top:44px;left:60px;right:50px;
      display:flex;flex-direction:column;gap:0;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:21px;color:{CORAL};
    text-transform:uppercase;letter-spacing:4px;margin-top:130px;margin-bottom:12px;}}
.big{{font-family:Inter;font-weight:700;font-size:84px;line-height:1.0;
    color:{DEEP_BLUE};letter-spacing:-4px;margin-bottom:22px;}}
.big em{{color:{AMBER};font-style:italic;text-shadow:4px 4px 0 {CORAL};}}
.stats-row{{display:flex;gap:12px;margin-bottom:22px;}}
.stat-box{{flex:1;background:{DEEP_BLUE};border-radius:16px;padding:20px 14px;
    border:2.5px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};text-align:center;}}
.stat-num{{font-family:Inter;font-weight:700;font-size:38px;color:{AMBER};line-height:1;}}
.stat-lbl{{font-family:'DM Sans';font-weight:600;font-size:18px;
    color:rgba(255,255,255,0.65);margin-top:5px;line-height:1.3;}}
.cta{{background:{DEEP_BLUE};color:white;padding:24px 28px;border-radius:18px;
    font-family:Inter;font-weight:700;font-size:24px;
    border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
    display:flex;align-items:center;justify-content:space-between;}}
.arrow{{width:54px;height:54px;background:{AMBER};border-radius:50%;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
</style></head><body><div class="c">
<div class="grain2"></div>
<img src="data:image/png;base64,{lb}" style="position:absolute;top:44px;left:60px;height:66px;opacity:0.95;z-index:25;filter:brightness(0) saturate(100%) invert(18%) sepia(34%) saturate(1289%) hue-rotate(183deg) brightness(94%) contrast(91%);">
<div class="badge">Beat the filter</div>
<div class="col">
  <div class="kicker">Your CV is ready</div>
  <div class="big">Now it reaches<br>a <em>human.</em></div>
  <div class="stats-row">
    <div class="stat-box">
      <div class="stat-num">6</div>
      <div class="stat-lbl">ATS rules to follow every time</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">1</div>
      <div class="stat-lbl">Column only. No exceptions.</div>
    </div>
    <div class="stat-box">
      <div class="stat-num">JD</div>
      <div class="stat-lbl">Keywords from the job description</div>
    </div>
  </div>
  <div class="cta">
    <div>
      <div>Find roles worth applying for</div>
      <div style="font-family:Inter;font-weight:700;font-size:17px;color:{AMBER};margin-top:4px;">internwise.co.uk →</div>
    </div>
    <div class="arrow">
      <svg width="24" height="24" viewBox="0 0 24 24">
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
    print("Generating ATS Guide Carousel v4 (Week 4, Day 3) — SVG illustrations...")
    _logo_b64()  # pre-warm

    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    for k in ATS_KILLERS:
        _killer_slide(k, os.path.join(campaign_dir, f"slide_{k['n']}.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    _slide8(os.path.join(campaign_dir, "slide_8.png"))
    print("Done - ATS guide carousel v4 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week4/d3-ats")
