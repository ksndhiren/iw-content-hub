"""
Internwise - What Happens After You Hit Send (Week 5, Day 2) - v2
Single statcard. AMBER accent, Gen Z neobrutalist style.
5-stage pipeline from application to offer.
"""
import os, base64
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"

LOGO_W = None
def _load_logo():
    global LOGO_W
    if LOGO_W is None:
        LOGO_W = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""

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

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"


def _statcard(out):
    f = _fonts()

    stages = [
        (AMBER,    DARK_NAVY, "ATS scan",              "FILTER: KEYWORDS",     "Mirror the JD's exact phrases. Tables and graphics get you cut here."),
        (CORAL,    "white",   "Human review",          "FILTER: FIRST 8 SECS", "Under 30 seconds on average. Your strongest line must come first."),
        (PURPLE,   "white",   "Phone / video screen",  "FILTER: CULTURE FIT",  "Short fit check. Concise answers, questions prepared, energy high."),
        (MINT,     DARK_NAVY, "Final stage / AC",      "FILTER: CAPABILITY",   "Assessment centre or panel interview. Prepare differently from a standard interview."),
        (DEEP_BLUE,"white",   "The offer",             "FILTER: NEGOTIATION",  "First number is rarely final. Research the market. Always worth asking."),
    ]

    rows = ""
    for i, (bg, fg, name, filter_label, action) in enumerate(stages):
        connector = ""
        if i > 0:
            connector = f'<div style="width:4px;height:16px;background:{AMBER};margin:0 0 0 25px;opacity:0.45;"></div>'
        rows += f"""
{connector}
<div style="display:flex;align-items:stretch;gap:0;
            border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};border-radius:12px;overflow:hidden;">
  <div style="width:54px;flex-shrink:0;background:{bg};display:flex;align-items:center;
              justify-content:center;font-family:Inter;font-weight:700;font-size:22px;
              color:{'rgba(0,0,0,0.45)' if fg==DARK_NAVY else 'rgba(255,255,255,0.55)'};">{i+1}</div>
  <div style="flex:1;background:rgba(255,255,255,0.04);padding:12px 18px;
              display:flex;align-items:center;gap:16px;">
    <div style="font-family:Inter;font-weight:700;font-size:20px;color:white;
                min-width:210px;flex-shrink:0;word-break:keep-all;hyphens:none;">{name}</div>
    <div style="background:{bg};color:{fg};padding:4px 12px;border-radius:50px;
                font-family:Inter;font-weight:700;font-size:11px;letter-spacing:1.5px;
                white-space:nowrap;flex-shrink:0;">{filter_label}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:18px;
                color:rgba(255,255,255,0.5);line-height:1.35;">{action}</div>
  </div>
</div>"""

    logo_html = f'<img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:40px;left:44px;height:62px;opacity:0.95;z-index:25;">'

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:40px 50px 40px 50px;}}
{GRAIN}
.header{{margin-bottom:20px;flex-shrink:0;padding-top:74px;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{AMBER};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.pipeline{{flex:1;display:flex;flex-direction:column;justify-content:center;}}
.cta{{flex-shrink:0;margin-top:18px;display:inline-flex;align-items:center;gap:12px;
    background:{AMBER};color:{DARK_NAVY};padding:14px 26px;border-radius:50px;
    border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};
    font-family:Inter;font-weight:700;font-size:17px;width:fit-content;}}
.badge{{position:absolute;top:40px;right:44px;background:{AMBER};color:{DARK_NAVY};
    padding:10px 22px;border-radius:50px;font-family:Inter;font-weight:700;
    font-size:13px;letter-spacing:2px;text-transform:uppercase;
    border:3px solid {DARK_NAVY};box-shadow:3px 3px 0 {DARK_NAVY};z-index:20;
    transform:rotate(-2deg);}}
</style></head><body><div class="c">
<div class="grain"></div>
{logo_html}
<div class="badge">Application guide</div>
<div class="header">
  <div class="kicker">After you hit send</div>
  <div class="hl">5 stages between you<br>and the <em>offer.</em></div>
</div>
<div class="pipeline">{rows}</div>
<div class="cta">Find roles at internwise.co.uk &#8594;</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Application Statcard (Week 5, Day 2) v2...")
    _load_logo()
    _statcard(os.path.join(campaign_dir, "statcard_application.png"))
    print("Done - application statcard v2 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week5/d2-application")
