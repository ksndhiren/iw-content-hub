"""
Internwise — UK Graduate Job Market 2026 (Week 3, Day 3)
8-slide carousel: data-driven, Gen Z dark design, human photos on select slides
"""
import os, base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_photo

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"; OFF_WHITE = "#FAF5EC"

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

def _src(path):
    if not path: return ""
    b64 = _b64(path)
    if not b64: return ""
    mime = "image/png" if str(path).endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{b64}"

def _arch_photo(photo_path, accent, bottom=20, right=20, w=400, h=500):
    """Full-photo arch block — no background removal needed."""
    if not photo_path:
        return ""
    src = _src(photo_path)
    if not src:
        return ""
    return f"""
<div style="position:absolute;bottom:{bottom}px;right:{right}px;
            width:{w}px;height:{h}px;
            border-radius:200px 200px 40px 40px;
            overflow:hidden;z-index:5;
            box-shadow:0 20px 50px rgba(0,0,0,0.4);">
  <img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:center top;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom,transparent 40%,{accent}cc 100%);"></div>
</div>"""

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
    print(f"  ✓ {path}")

GRAIN = "position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);background-size:3px 3px;"

LOGO_B64 = None
def _logo():
    global LOGO_B64
    if LOGO_B64 is None:
        LOGO_B64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    return f'<img src="data:image/png;base64,{LOGO_B64}" style="height:72px;opacity:0.95;">' if LOGO_B64 else ""

def _spark(s, t, l, c, o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:14;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'

def _base(extra_css="", body="", badge_text=""):
    f = _fonts()
    badge = f'<div style="position:absolute;top:44px;right:50px;background:{AMBER};color:{DEEP_BLUE};padding:12px 26px;border-radius:50px;font-family:Inter;font-weight:700;font-size:15px;letter-spacing:2px;text-transform:uppercase;transform:rotate(4deg);box-shadow:0 8px 22px rgba(255,177,32,0.45);z-index:20;">{badge_text}</div>' if badge_text else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
.grain{{position:absolute;inset:0;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);
    background-size:3px 3px;}}
.logo{{position:absolute;top:44px;left:44px;z-index:20;}}
.url{{position:absolute;bottom:44px;left:50px;font-family:Inter;font-weight:700;
    font-size:20px;color:rgba(255,255,255,0.35);z-index:20;}}
{extra_css}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="logo">{_logo()}</div>
{badge}
{body}
<div class="url">internwise.co.uk</div>
</div></body></html>"""


def _slide1(out, photo=None):
    photo_html = _arch_photo(photo, CORAL, bottom=20, right=20, w=400, h=500) if photo else ""
    right_margin = "440px" if photo else "60px"
    html = _base(
        extra_css=f"""
.hl{{position:absolute;top:148px;left:50px;right:{right_margin};
    font-family:Inter;font-weight:700;font-size:88px;line-height:1.05;
    color:white;letter-spacing:-4px;z-index:20;}}
.hl em{{color:{CORAL};font-style:italic;}}
.sub{{position:absolute;top:660px;left:50px;right:{right_margin};
    font-family:'DM Sans';font-weight:700;font-size:30px;
    color:rgba(255,255,255,0.7);line-height:1.45;z-index:20;}}
.sub strong{{color:{AMBER};}}
""",
        body=f"""
<div class="hl">The UK grad job<br>market in 2026<br>is <em>brutal.</em></div>
<div class="sub">But here's exactly<br>where the <strong>gaps are.</strong></div>
{photo_html}
{_spark(28,490,800,AMBER,0.6)}{_spark(18,700,900,CORAL,0.4)}
""",
        badge_text="2026 Market"
    )
    _render(html, out)


def _slide2(out, photo=None):
    photo_html = _arch_photo(photo, AMBER, bottom=160, right=30, w=370, h=420) if photo else ""
    right_margin = "420px" if photo else "50px"
    html = _base(
        extra_css=f"""
.label{{position:absolute;top:155px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.stat-block{{position:absolute;left:50px;right:{right_margin};z-index:20;
    display:flex;flex-direction:column;gap:24px;top:210px;}}
.stat{{background:rgba(255,255,255,0.07);border:2px solid rgba(255,255,255,0.12);
    border-radius:20px;padding:28px 32px;
    border-left:6px solid {CORAL};}}
.stat .num{{font-family:Inter;font-weight:700;font-size:90px;
    color:{CORAL};letter-spacing:-4px;line-height:0.85;}}
.stat .desc{{font-family:'DM Sans';font-weight:600;font-size:22px;
    color:rgba(255,255,255,0.75);margin-top:8px;}}
.good{{position:absolute;bottom:100px;left:50px;right:{right_margin};z-index:20;
    font-family:Inter;font-weight:700;font-size:26px;
    color:white;font-style:italic;}}
.good em{{color:{AMBER};}}
""",
        body=f"""
<div class="label">The reality</div>
<div class="stat-block">
  <div class="stat">
    <div class="num">140</div>
    <div class="desc">applications per vacancy at large employers</div>
  </div>
  <div class="stat" style="border-left-color:{AMBER};">
    <div class="num" style="color:{AMBER};font-size:76px;">7%</div>
    <div class="desc">fewer graduate vacancies than last year</div>
  </div>
</div>
<div class="good">That's the bad news. Here's the <em>good news.</em></div>
{photo_html}
"""
    )
    _render(html, out)


def _slide3(out):
    bars = [
        ("Big corporate schemes",    "10% fewer", CORAL,   False),
        ("Mid-level roles",          "10% fewer", "#e04040", False),
        ("Entry-level roles",        "6% fewer",  MINT,    True),
    ]
    bars_html = ""
    for label, stat, color, winner in bars:
        star = f'<span style="margin-left:12px;font-size:18px;color:{AMBER};">- Your target</span>' if winner else ""
        bars_html += f"""
<div style="background:rgba(255,255,255,0.06);border:2px solid rgba(255,255,255,0.1);
     border-left:8px solid {color};border-radius:16px;padding:22px 28px;
     display:flex;align-items:center;justify-content:space-between;
     {'box-shadow:0 0 0 2px '+MINT+';' if winner else ''}">
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:{'white' if winner else 'rgba(255,255,255,0.6)'};">{label}{star}</div>
  <div style="font-family:Inter;font-weight:700;font-size:32px;color:{color};">{stat}</div>
</div>"""

    html = _base(
        extra_css=f"""
.label{{position:absolute;top:155px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.hl{{position:absolute;top:195px;left:50px;right:50px;
    font-family:Inter;font-weight:700;font-size:54px;line-height:1.0;
    color:white;letter-spacing:-2px;z-index:20;}}
.bars{{position:absolute;top:340px;left:50px;right:50px;
    display:flex;flex-direction:column;gap:16px;z-index:20;}}
.insight{{position:absolute;bottom:100px;left:50px;right:50px;z-index:20;
    font-family:'DM Sans';font-weight:700;font-size:26px;
    color:rgba(255,255,255,0.7);}}
.insight strong{{color:{MINT};}}
""",
        body=f"""
<div class="label">The gap</div>
<div class="hl">Smaller than it feels.<br>Entry-level is the target.</div>
<div class="bars">{bars_html}</div>
<div class="insight">Entry-level hiring fell <strong>6%</strong>. Mid-level fell 10%.<br>That gap is your advantage.</div>
"""
    )
    _render(html, out)


def _slide4(out, photo=None):
    sectors = [
        ("AI and Technology",          PURPLE, "Fastest growing"),
        ("Health and Life Sciences",   MINT,   "Actively hiring"),
        ("Infrastructure and Engineering", AMBER, "High demand"),
    ]
    pills = ""
    for name, color, tag in sectors:
        pills += f"""
<div style="display:flex;align-items:center;gap:16px;
     background:rgba(255,255,255,0.06);border:2px solid {color};
     border-radius:18px;padding:22px 26px;
     box-shadow:0 0 0 1px rgba(255,255,255,0.05);">
  <div style="width:14px;height:14px;border-radius:50%;background:{color};flex-shrink:0;"></div>
  <div style="flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;letter-spacing:-0.5px;">{name}</div>
    <div style="font-family:'DM Sans';font-weight:600;font-size:17px;color:{color};margin-top:3px;">{tag}</div>
  </div>
</div>"""

    photo_html = _arch_photo(photo, MINT, bottom=20, right=20, w=380, h=460) if photo else ""

    html = _base(
        extra_css=f"""
.label{{position:absolute;top:155px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.hl{{position:absolute;top:195px;left:50px;right:430px;
    font-family:Inter;font-weight:700;font-size:56px;line-height:0.92;
    color:white;letter-spacing:-3px;z-index:20;}}
.hl em{{color:{MINT};font-style:italic;}}
.sectors{{position:absolute;top:390px;left:50px;right:{('430px' if photo else '50px')};
    display:flex;flex-direction:column;gap:16px;z-index:20;}}
""",
        body=f"""
<div class="label">Where to look</div>
<div class="hl">These sectors are<br><em>actively hiring</em> grads.</div>
<div class="sectors">{pills}</div>
{photo_html}
{_spark(20,700,900,MINT,0.4)}
"""
    )
    _render(html, out)


def _slide5(out):
    html = _base(
        extra_css=f"""
.label{{position:absolute;top:155px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.hl{{position:absolute;top:195px;left:50px;
    font-family:Inter;font-weight:700;font-size:68px;line-height:0.88;
    color:white;letter-spacing:-3px;z-index:20;}}
.split{{position:absolute;top:440px;left:50px;right:50px;
    display:flex;gap:20px;z-index:20;}}
.box{{flex:1;border-radius:20px;padding:30px;
    display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;}}
.box .pct{{font-family:Inter;font-weight:700;font-size:90px;line-height:0.85;letter-spacing:-4px;}}
.box .city{{font-family:Inter;font-weight:700;font-size:28px;margin-top:8px;}}
.box .desc{{font-family:'DM Sans';font-weight:500;font-size:18px;margin-top:6px;opacity:0.75;}}
.insight{{position:absolute;bottom:100px;left:50px;right:50px;z-index:20;
    font-family:'DM Sans';font-weight:700;font-size:24px;
    color:rgba(255,255,255,0.7);text-align:center;}}
.insight strong{{color:{AMBER};}}
""",
        body=f"""
<div class="label">The London trap</div>
<div class="hl">London gets<br>60% of applications.</div>
<div class="split">
  <div class="box" style="background:rgba(255,107,107,0.15);border:2px solid {CORAL};">
    <div class="pct" style="color:{CORAL};">60%</div>
    <div class="city" style="color:white;">London</div>
    <div class="desc" style="color:rgba(255,255,255,0.6);">of all grad applications</div>
  </div>
  <div class="box" style="background:rgba(127,219,182,0.15);border:2px solid {MINT};">
    <div class="pct" style="color:{MINT};">40%</div>
    <div class="city" style="color:white;">Everywhere else</div>
    <div class="desc" style="color:rgba(255,255,255,0.6);">same roles, far less competition</div>
  </div>
</div>
<div class="insight">Same roles. <strong>Half the competition.</strong> More of your salary left over.</div>
"""
    )
    _render(html, out)


def _slide6(out, photo=None):
    points = [
        ("No September deadline.",    AMBER),
        ("No 6-stage process.",       MINT),
        ("Hire when they need someone.", CORAL),
    ]
    pts_html = "".join([
        f'<div style="display:flex;align-items:center;gap:18px;"><div style="width:12px;height:12px;border-radius:50%;background:{c};flex-shrink:0;"></div><div style="font-family:\'DM Sans\';font-weight:700;font-size:26px;color:rgba(255,255,255,0.85);">{t}</div></div>'
        for t, c in points
    ])
    photo_html = _arch_photo(photo, MINT, bottom=130, right=20, w=390, h=440) if photo else ""
    right_margin = "430px" if photo else "50px"
    html = _base(
        extra_css=f"""
.label{{position:absolute;top:155px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.hl{{position:absolute;top:195px;left:50px;right:{right_margin};
    font-family:Inter;font-weight:700;font-size:72px;line-height:0.88;
    color:white;letter-spacing:-3px;z-index:20;}}
.pts{{position:absolute;top:430px;left:50px;right:{right_margin};
    display:flex;flex-direction:column;gap:22px;z-index:20;}}
.advantage{{position:absolute;bottom:100px;left:50px;right:{right_margin};
    font-family:Inter;font-weight:700;font-size:30px;
    color:{AMBER};font-style:italic;z-index:20;}}
""",
        body=f"""
<div class="label">The SME advantage</div>
<div class="hl">SMEs hire<br>year-round.</div>
<div class="pts">{pts_html}</div>
<div class="advantage">"Most students ignore them. That's your edge."</div>
{photo_html}
{_spark(22,620,880,AMBER,0.4)}
"""
    )
    _render(html, out)


def _slide7(out, photo=None):
    photo_html = _arch_photo(photo, CORAL, bottom=20, right=20, w=390, h=480) if photo else ""
    right_margin = "430px" if photo else "50px"
    html = _base(
        extra_css=f"""
.label{{position:absolute;top:155px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.big{{position:absolute;top:200px;left:50px;
    font-family:Inter;font-weight:700;font-size:220px;line-height:0.8;
    color:{CORAL};letter-spacing:-10px;z-index:20;}}
.pct{{position:absolute;top:200px;left:394px;
    font-family:Inter;font-weight:700;font-size:100px;
    color:{CORAL};z-index:20;}}
.desc{{position:absolute;top:480px;left:50px;right:{right_margin};z-index:20;
    font-family:'DM Sans';font-weight:700;font-size:28px;
    color:rgba(255,255,255,0.85);line-height:1.4;}}
.sub{{position:absolute;top:640px;left:50px;right:{right_margin};z-index:20;
    font-family:'DM Sans';font-weight:600;font-size:22px;
    color:rgba(255,255,255,0.55);line-height:1.4;}}
.sub strong{{color:{MINT};}}
""",
        body=f"""
<div class="label">The network problem</div>
<div class="big">44</div>
<div class="pct">%</div>
<div class="desc">of Gen Z say not having the right network is their biggest barrier to getting hired.</div>
<div class="sub">You can build one.<br>It just has to be <strong>intentional.</strong></div>
{photo_html}
{_spark(20,700,860,CORAL,0.3)}
"""
    )
    _render(html, out)


def _slide8(out):
    f = _fonts()
    logo_b64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    logo_dark = f'<img src="data:image/png;base64,{logo_b64}" style="height:72px;filter:invert(1) sepia(1) saturate(3) hue-rotate(190deg);opacity:0.7;">' if logo_b64 else ""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{OFF_WHITE};}}
.logo{{position:absolute;top:44px;left:44px;z-index:20;}}
.hl{{position:absolute;top:220px;left:60px;right:60px;
    font-family:Inter;font-weight:700;font-size:86px;line-height:0.88;
    color:{DEEP_BLUE};letter-spacing:-4px;z-index:20;}}
.hl em{{color:{CORAL};font-style:italic;}}
.sub{{position:absolute;top:560px;left:60px;right:60px;
    font-family:'DM Sans';font-weight:600;font-size:28px;
    color:rgba(38,77,126,0.6);z-index:20;line-height:1.4;}}
.sub strong{{color:{DEEP_BLUE};}}
.pill{{position:absolute;bottom:90px;left:60px;
    background:{DEEP_BLUE};color:white;
    padding:22px 44px;border-radius:60px;
    font-family:Inter;font-weight:700;font-size:28px;
    border:3px solid {DARK_NAVY};box-shadow:6px 6px 0 {DARK_NAVY};z-index:20;}}
</style></head><body><div class="c">
<div class="logo">{logo_dark}</div>
<div class="hl">Stop fighting<br>for the same<br><em>100 roles</em><br>as everyone else.</div>
<div class="sub">The gaps exist.<br><strong>You just have to know where to look.</strong></div>
<div class="pill">internwise.co.uk →</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating UK Job Market Carousel (Week 3, Day 3)...")

    print("  ↓ Fetching photos for slides 1, 2, 4, 6, 7...")
    photos = {}
    fetch_list = [
        ("slide1",  "frustrated student looking at laptop job search",              0, "portrait"),
        ("slide2",  "student overwhelmed applications cv laptop stressed portrait",  1, "portrait"),
        ("slide4",  "young professional woman smiling confident office portrait",    0, "portrait"),
        ("slide6",  "young professional relaxed startup office casual smiling",      0, "portrait"),
        ("slide7",  "young man professional networking handshake smiling portrait",  0, "portrait"),
    ]
    for key, query, idx, orient in fetch_list:
        try:
            photos[key] = get_photo(query, index=idx, orientation=orient)
            print(f"    ✓ {key}: {photos[key]}")
        except Exception as e:
            print(f"    ! {key} failed: {e}")
            photos[key] = None

    _slide1(os.path.join(campaign_dir, "slide_1.png"), photo=photos.get("slide1"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"), photo=photos.get("slide2"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"), photo=photos.get("slide4"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"), photo=photos.get("slide6"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photo=photos.get("slide7"))
    _slide8(os.path.join(campaign_dir, "slide_8.png"))
    print("✓ Job market carousel complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/wk3-d3-jobmarket")
