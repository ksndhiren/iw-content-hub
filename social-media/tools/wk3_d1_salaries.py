"""
Internwise — Graduate Starting Salaries by Industry 2026 (Week 3, Day 1)
8-slide carousel: salary data by sector, Gen Z dark design v2

Data sources: High Fliers 2026, HESA Graduate Outcomes 2022/23,
Aldi/Lidl Careers UK, MI5 Careers, ISE 2025/26
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
def _logo():
    global LOGO_B64
    if LOGO_B64 is None:
        LOGO_B64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    return f'<img src="data:image/png;base64,{LOGO_B64}" style="height:72px;opacity:0.95;">' if LOGO_B64 else ""

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"

def _spark(s,t,l,c,o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:14;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'


# ── Slide 1: Hook ──────────────────────────────────────────────────────────────
def _slide1(out):
    f = _fonts()
    # Salary bars data - ranked worst to best
    bars = [
        ("Hospitality", "£22K-28K",  22, CORAL),
        ("Marketing",   "£25K-29K",  32, PURPLE),
        ("Tech / Eng",  "£30K-55K",  52, MINT),
        ("Finance / Law","£35K-65K+", 72, AMBER),
        ("Wild cards",  "£40K-52K+", 62, LIGHT_BLUE),
    ]
    bar_html = ""
    for label, salary, pct, color in bars:
        bar_html += f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
  <div style="width:130px;font-family:'DM Sans';font-weight:700;font-size:17px;
              color:rgba(255,255,255,0.65);text-align:right;flex-shrink:0;">{label}</div>
  <div style="flex:1;height:36px;background:rgba(255,255,255,0.08);border-radius:8px;overflow:hidden;
              border:1.5px solid rgba(255,255,255,0.1);">
    <div style="width:{pct}%;height:100%;background:{color};border-radius:6px;
                display:flex;align-items:center;justify-content:flex-end;padding-right:10px;">
      <span style="font-family:Inter;font-weight:700;font-size:14px;color:{DEEP_BLUE};white-space:nowrap;">{salary}</span>
    </div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.logo{{position:absolute;top:44px;left:44px;z-index:20;}}
.badge{{position:absolute;top:44px;right:50px;
    background:{AMBER};color:{DEEP_BLUE};
    padding:12px 28px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:15px;
    letter-spacing:2px;text-transform:uppercase;
    transform:rotate(4deg);
    box-shadow:0 8px 22px rgba(255,177,32,0.45);z-index:20;}}
.kicker{{position:absolute;top:148px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:4px;z-index:20;}}
.hl{{position:absolute;top:186px;left:50px;right:60px;
    font-family:Inter;font-weight:700;font-size:82px;line-height:1.0;
    color:white;letter-spacing:-3px;z-index:20;}}
.hl em{{color:{AMBER};font-style:italic;text-shadow:4px 4px 0 {CORAL};}}
.divider{{position:absolute;top:455px;left:50px;right:50px;
    height:2px;background:rgba(255,255,255,0.1);z-index:20;}}
.sub-label{{position:absolute;top:472px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:18px;
    color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.bars-wrap{{position:absolute;top:508px;left:50px;right:50px;z-index:20;}}
.hint{{position:absolute;bottom:40px;left:50px;
    font-family:Inter;font-weight:700;font-size:20px;
    color:rgba(255,255,255,0.38);z-index:20;}}
.hint strong{{color:rgba(255,255,255,0.7);}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="logo">{_logo()}</div>
<div class="badge">2026 Data</div>
<div class="kicker">Graduate salaries</div>
<div class="hl">What UK employers<br><em>actually</em> pay you<br>in 2026</div>
<div class="divider"></div>
<div class="sub-label">Ranked by sector</div>
<div class="bars-wrap">{bar_html}</div>
<div class="hint">Swipe to break down every sector <strong>→</strong></div>
{_spark(28,152,740,AMBER,0.6)}
{_spark(18,430,880,'white',0.25)}
</div></body></html>"""
    _render(html, out)


# ── Sector slides 2-7 ─────────────────────────────────────────────────────────
SECTORS = [
    {
        "n": 2,
        "label": "Hospitality and retail",
        "range": "£22K - £28K",
        "accent": CORAL,
        "tag": "Lowest-paid sector",
        "facts": [
            ("Travel and hospitality", "~£22,705 avg"),
            ("Retail management", "£23K - £30K"),
            ("High street roles", "Often near NMW"),
        ],
        "insight": "High competition, lower pay. But transferable skills are real. Top retail grad schemes can reach £40K+.",
        "photo_key": "hospitality",
        "slide_num_label": "01 / 06",
    },
    {
        "n": 3,
        "label": "Marketing, HR and comms",
        "range": "£25K - £29K",
        "accent": PURPLE,
        "tag": "Below average to start",
        "facts": [
            ("Marketing and advertising", "£24K - £28K"),
            ("Digital marketing", "£27K - £49K"),
            ("HR and people ops", "£28K - £35K"),
        ],
        "insight": "Digital and HR tracks pay better. Fast progression if you pick the right company.",
        "photo_key": "marketing",
        "slide_num_label": "02 / 06",
    },
    {
        "n": 4,
        "label": "Tech, engineering and consulting",
        "range": "£30K - £55K",
        "accent": MINT,
        "tag": "Widest range of any sector",
        "facts": [
            ("Startups and SMEs", "£28K - £35K"),
            ("Large tech firms", "£36K - £55K"),
            ("Top-tier consulting", "~£50K base"),
        ],
        "insight": "AI Engineer is the fastest-growing grad job title in 2026. Learn to build - earnings follow.",
        "photo_key": "tech",
        "slide_num_label": "03 / 06",
    },
    {
        "n": 5,
        "label": "Finance, law and accounting",
        "range": "£35K - £65K+",
        "accent": AMBER,
        "tag": "Highest ceiling",
        "facts": [
            ("Large accounting firms", "£28K - £33K"),
            ("Investment banking", "£55K - £65K base"),
            ("Top City law firms", "£56K trainee"),
        ],
        "insight": "IB year-one total comp averages £84K. Brutal process - but the ceiling is genuinely high.",
        "photo_key": "finance",
        "slide_num_label": "04 / 06",
    },
    {
        "n": 6,
        "label": "The wild cards",
        "range": "£40K - £52K+",
        "accent": LIGHT_BLUE,
        "tag": "Not finance. Not law.",
        "facts": [
            ("Leading supermarket scheme", "£52,020 + company car"),
            ("Discount retailer scheme", "£40,000 + car"),
            ("Intelligence services", "£40,428 - £44,190"),
        ],
        "insight": "A supermarket grad scheme pays more than most banks on base salary. Not what you expected, right?",
        "photo_key": "wildcard",
        "slide_num_label": "05 / 06",
    },
    {
        "n": 7,
        "label": "The baseline to know",
        "range": "£30,500",
        "accent": MINT,
        "tag": "Know your floor",
        "facts": [
            ("Broader market average", "£30,500"),
            ("Top 100 employers median", "£35,000"),
            ("5-year salary growth", "+16.7% since 2021"),
        ],
        "insight": "Never accept below the market average without a reason. Know the number before you apply.",
        "photo_key": "baseline",
        "slide_num_label": "06 / 06",
    },
]


def _sector_slide(sector, photos, out):
    f = _fonts()
    accent = sector["accent"]
    dark_accent = accent in (AMBER, MINT, LIGHT_BLUE)  # light accents need dark text
    accent_text = DEEP_BLUE if dark_accent else "white"

    # Build fact rows
    facts_html = ""
    for label, val in sector["facts"]:
        facts_html += f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            padding:13px 18px;background:rgba(255,255,255,0.06);
            border-radius:12px;margin-bottom:8px;
            border-left:3px solid {accent};">
  <span style="font-family:'DM Sans';font-weight:600;font-size:19px;
               color:rgba(255,255,255,0.7);">{label}</span>
  <span style="font-family:Inter;font-weight:700;font-size:20px;
               color:{accent};white-space:nowrap;margin-left:12px;">{val}</span>
</div>"""

    # Right-side visual: cutout photo (arch bg) or accent block
    if sector["photo_key"] and sector["photo_key"] in photos:
        src = _src(photos[sector["photo_key"]])
        right_html = f"""
<!-- Arch shape behind photo -->
<div style="position:absolute;bottom:20px;right:20px;
            width:400px;height:500px;
            background:linear-gradient(145deg,{accent},{accent}99);
            border-radius:200px 200px 40px 40px;z-index:5;
            box-shadow:0 20px 50px rgba(0,0,0,0.3);"></div>
<!-- Cutout character -->
<div style="position:absolute;bottom:0;right:-20px;
            width:480px;height:620px;z-index:10;
            filter:drop-shadow(0 20px 40px rgba(0,0,0,0.4));">
  <img src="{src}" style="width:100%;height:100%;
       object-fit:contain;object-position:bottom center;">
</div>"""
    else:
        # No photo - fill with a bold stat visual block
        extra_label = "TOP SCHEME" if sector["n"] == 6 else "MARKET AVG"
        extra_sub   = "£52K+ to start" if sector["n"] == 6 else "Top 100: £35K"
        right_html = f"""
<div style="position:absolute;bottom:80px;right:50px;
            width:340px;height:380px;z-index:10;
            background:{accent};
            border:3px solid {DARK_NAVY};box-shadow:10px 10px 0 {DARK_NAVY};
            border-radius:28px;
            display:flex;flex-direction:column;
            align-items:center;justify-content:center;gap:10px;padding:30px;">
  <div style="font-family:Inter;font-weight:700;font-size:22px;
              color:{accent_text};text-transform:uppercase;
              letter-spacing:2px;text-align:center;">{extra_label}</div>
  <div style="width:60px;height:4px;background:{accent_text};opacity:0.3;border-radius:2px;"></div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:18px;
              color:{accent_text};opacity:0.75;text-align:center;">{extra_sub}</div>
  <div style="font-family:Inter;font-weight:700;font-size:72px;line-height:1;
              letter-spacing:-3px;color:{accent_text};text-align:center;">{sector['range'].replace('£','').replace(',','')}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
/* Left accent bar */
.bar{{position:absolute;top:0;left:0;width:6px;height:100%;background:{accent};z-index:10;
      box-shadow:0 0 20px {accent}66;}}
.logo{{position:absolute;top:44px;left:50px;z-index:20;}}
.slide-num{{position:absolute;top:44px;right:50px;
    font-family:Inter;font-weight:700;font-size:15px;
    color:rgba(255,255,255,0.35);letter-spacing:2px;z-index:20;}}
.tag-pill{{position:absolute;top:130px;left:50px;z-index:20;
    background:{accent};color:{accent_text};
    padding:8px 20px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:13px;
    letter-spacing:2px;text-transform:uppercase;
    display:inline-block;}}
.sector-name{{position:absolute;top:186px;left:50px;right:440px;
    font-family:Inter;font-weight:700;font-size:44px;line-height:1.1;
    color:white;letter-spacing:-1.5px;z-index:20;}}
.salary{{position:absolute;top:312px;left:50px;
    font-family:Inter;font-weight:700;font-size:112px;line-height:0.88;
    color:{accent};letter-spacing:-5px;z-index:20;
    text-shadow:4px 4px 0 rgba(0,0,0,0.2);}}
.facts-wrap{{position:absolute;top:430px;left:50px;right:450px;z-index:20;}}
.insight{{position:absolute;bottom:50px;left:50px;right:450px;
    font-family:'DM Sans';font-weight:600;font-size:20px;
    color:rgba(255,255,255,0.6);line-height:1.45;z-index:20;
    border-top:1.5px solid rgba(255,255,255,0.1);padding-top:14px;}}
.url{{position:absolute;bottom:44px;right:50px;
    font-family:Inter;font-weight:700;font-size:16px;
    color:rgba(255,255,255,0.25);z-index:20;letter-spacing:0.5px;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="bar"></div>
<div class="logo">{_logo()}</div>
<div class="slide-num">{sector['slide_num_label']}</div>
<div class="tag-pill">{sector['tag']}</div>
<div class="sector-name">{sector['label']}</div>
<div class="salary">{sector['range']}</div>
<div class="facts-wrap">{facts_html}</div>
<div class="insight">{sector['insight']}</div>
<div class="url">internwise.co.uk</div>
{right_html}
{_spark(18,240,460,accent,0.3)}
</div></body></html>"""
    _render(html, out)


# ── Slide 8: CTA ───────────────────────────────────────────────────────────────
def _slide8(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:{OFF_WHITE};}}
.grain2{{position:absolute;inset:0;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(0,0,0,0.025) 1px,transparent 1px);
    background-size:3px 3px;}}
.logo{{position:absolute;top:44px;left:44px;z-index:20;
    filter:brightness(0) saturate(100%) invert(18%) sepia(34%) saturate(1289%) hue-rotate(183deg) brightness(94%) contrast(91%);}}
.badge{{position:absolute;top:44px;right:50px;
    background:{DEEP_BLUE};color:white;
    padding:12px 28px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:15px;
    letter-spacing:2px;text-transform:uppercase;
    transform:rotate(-3deg);
    box-shadow:5px 5px 0 {DARK_NAVY};z-index:20;}}
.kicker{{position:absolute;top:175px;left:60px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:4px;z-index:20;}}
.big{{position:absolute;top:215px;left:60px;right:60px;
    font-family:Inter;font-weight:700;font-size:96px;line-height:1.0;
    color:{DEEP_BLUE};letter-spacing:-4px;z-index:20;}}
.big em{{color:{AMBER};font-style:italic;text-shadow:4px 4px 0 {CORAL};}}
.stats-row{{position:absolute;top:580px;left:60px;right:60px;
    display:flex;gap:16px;z-index:20;}}
.stat-box{{flex:1;background:{DEEP_BLUE};border-radius:18px;padding:20px 16px;
    border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
    text-align:center;}}
.stat-num{{font-family:Inter;font-weight:700;font-size:36px;color:{AMBER};line-height:1;}}
.stat-lbl{{font-family:'DM Sans';font-weight:600;font-size:15px;
    color:rgba(255,255,255,0.65);margin-top:5px;line-height:1.3;}}
.cta-pill{{position:absolute;bottom:64px;left:60px;right:60px;
    background:{DEEP_BLUE};color:white;
    padding:26px 44px;border-radius:22px;
    font-family:Inter;font-weight:700;font-size:28px;
    border:3px solid {DARK_NAVY};box-shadow:6px 6px 0 {DARK_NAVY};
    z-index:20;
    display:flex;align-items:center;justify-content:space-between;}}
.arrow-circle{{width:62px;height:62px;background:{AMBER};border-radius:50%;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
</style></head><body><div class="c">
<div class="grain2"></div>
<div class="logo">{_logo()}</div>
<div class="badge">Your move</div>
<div class="kicker">Now you know the numbers</div>
<div class="big">Find the roles<br>that <em>actually pay.</em></div>
<div class="stats-row">
  <div class="stat-box">
    <div class="stat-num">£35K</div>
    <div class="stat-lbl">Top 100<br>employer median</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">£52K</div>
    <div class="stat-lbl">Top grad<br>scheme start</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">+16.7%</div>
    <div class="stat-lbl">Grad salary growth<br>since 2021</div>
  </div>
  <div class="stat-box">
    <div class="stat-num">£65K+</div>
    <div class="stat-lbl">Finance and law<br>ceiling</div>
  </div>
</div>
<div class="cta-pill">
  <div>
    <div>Find your salary-matched role</div>
    <div style="font-family:Inter;font-weight:700;font-size:18px;color:{AMBER};margin-top:5px;opacity:0.85;">internwise.co.uk →</div>
  </div>
  <div class="arrow-circle">
    <svg width="28" height="28" viewBox="0 0 28 28">
      <path d="M6 14L20 14M15 8L21 14L15 20" stroke="{DEEP_BLUE}" stroke-width="3"
            fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
</div>
{_spark(32,175,840,AMBER,0.55)}
{_spark(20,460,930,CORAL,0.35)}
</div></body></html>"""
    _render(html, out)


# ── Main ───────────────────────────────────────────────────────────────────────
def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Graduate Salaries Carousel v2 (Week 3, Day 1)...")
    photos = {}
    print("  Fetching cutout photos...")
    for key, query, idx in [
        ("hospitality", "young woman apron smiling isolated plain background portrait studio", 1),
        ("marketing",   "young professional woman smiling isolated plain white background portrait", 1),
        ("tech",        "young man holding laptop smiling isolated plain background portrait studio", 0),
        ("finance",     "young man suit jacket smiling isolated plain background portrait studio", 1),
        ("wildcard",    "young woman surprised excited professional isolated plain background portrait", 0),
        ("baseline",    "young graduate confident arms crossed smiling isolated plain background portrait", 0),
    ]:
        photos[key] = get_cutout(query, index=idx, orientation="portrait")
        print(f"    ok {key}: {photos[key]}")

    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    for s in SECTORS:
        _sector_slide(s, photos, os.path.join(campaign_dir, f"slide_{s['n']}.png"))
    _slide8(os.path.join(campaign_dir, "slide_8.png"))
    print("Done - salaries carousel v2 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week3/d1-salaries")
