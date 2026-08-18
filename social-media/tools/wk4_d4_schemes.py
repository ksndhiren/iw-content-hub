"""
Internwise — Graduate Schemes vs Direct Entry Stat Card (Week 4, Day 4) — v2
Single 1080x1080: split comparison with real human photos on each side
"""
import os, base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_cutout

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; MINT = "#7FDBB6"; LIGHT_BLUE = "#5FA7E5"

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


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Grad Schemes vs Direct Entry Stat Card v2 (Week 4, Day 4)...")

    print("  Fetching photos...")
    grad_src = direct_src = ""
    try:
        p = get_cutout("young graduate formal suit confident smiling isolated plain white background portrait studio", 0, orientation="portrait")
        grad_src = _src(p)
        print(f"    ok grad: {p}")
    except Exception as e:
        print(f"    ! grad photo failed: {e}")
    try:
        p = get_cutout("young professional casual confident smiling isolated plain white background portrait studio", 1, orientation="portrait")
        direct_src = _src(p)
        print(f"    ok direct: {p}")
    except Exception as e:
        print(f"    ! direct photo failed: {e}")

    f = _fonts()
    logo_b64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""

    SPLIT = 540

    # Full-height photos — fade out toward top so stats stay readable
    grad_photo_html = f"""
<div style="position:absolute;bottom:140px;left:0;width:{SPLIT}px;height:520px;
            z-index:8;overflow:hidden;
            -webkit-mask-image:linear-gradient(to top,black 0%,black 30%,transparent 80%);
            mask-image:linear-gradient(to top,black 0%,black 30%,transparent 80%);">
  <img src="{grad_src}" style="width:100%;height:100%;
       object-fit:contain;object-position:bottom center;opacity:0.22;">
</div>""" if grad_src else ""

    direct_photo_html = f"""
<div style="position:absolute;bottom:140px;left:{SPLIT}px;width:{1080-SPLIT}px;height:520px;
            z-index:8;overflow:hidden;
            -webkit-mask-image:linear-gradient(to top,black 0%,black 30%,transparent 80%);
            mask-image:linear-gradient(to top,black 0%,black 30%,transparent 80%);">
  <img src="{direct_src}" style="width:100%;height:100%;
       object-fit:contain;object-position:bottom center;opacity:0.18;">
</div>""" if direct_src else ""

    def _stat_rows(data):
        html = ""
        for label, val, bg, ct in data:
            html += f"""
<div style="margin-bottom:8px;padding:11px 16px;
            background:rgba(255,255,255,0.07);border-radius:11px;
            border:1px solid rgba(255,255,255,0.1);">
  <div style="font-family:'DM Sans';font-weight:700;font-size:15px;
              color:rgba(255,255,255,0.42);text-transform:uppercase;
              letter-spacing:2px;margin-bottom:4px;">{label}</div>
  <span style="display:inline-block;background:{bg};color:{ct};
               font-family:Inter;font-weight:700;font-size:26px;
               padding:5px 18px;border-radius:18px;">{val}</span>
</div>"""
        return html

    scheme_rows = _stat_rows([
        ("Acceptance rate",    "1-3%",        CORAL,  "white"),
        ("Application window", "Sep - Jan",   LIGHT_BLUE, DEEP_BLUE),
        ("Time to start",      "9-12 months", CORAL,  "white"),
        ("Training",           "Structured",  MINT,   DEEP_BLUE),
        ("Competition level",  "Very high",   CORAL,  "white"),
    ])
    direct_rows = _stat_rows([
        ("Acceptance rate",    "Higher",       MINT,   DEEP_BLUE),
        ("Application window", "Year-round",   AMBER,  DEEP_BLUE),
        ("Time to start",      "4-8 weeks",    MINT,   DEEP_BLUE),
        ("Training",           "On-the-job",   LIGHT_BLUE, DEEP_BLUE),
        ("Competition level",  "Lower at SMEs",MINT,   DEEP_BLUE),
    ])

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;font-family:Inter;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{DARK_NAVY};}}
.grain{{position:absolute;inset:0;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);
    background-size:3px 3px;}}
.left{{position:absolute;top:0;left:0;width:{SPLIT}px;height:1080px;
    background:linear-gradient(160deg,{DEEP_BLUE} 0%,#1d3d6b 100%);z-index:3;}}
.right{{position:absolute;top:0;left:{SPLIT}px;width:{1080-SPLIT}px;height:1080px;
    background:linear-gradient(160deg,{DARK_NAVY} 0%,#0e1e33 100%);z-index:3;}}
.divider{{position:absolute;top:0;left:{SPLIT-3}px;width:6px;height:1080px;
    background:{AMBER};z-index:10;box-shadow:0 0 18px {AMBER}88;}}
.vs{{position:absolute;top:50%;left:{SPLIT}px;transform:translate(-50%,-50%);
    width:72px;height:72px;border-radius:50%;
    background:{AMBER};color:{DEEP_BLUE};
    display:flex;align-items:center;justify-content:center;
    font-family:Inter;font-weight:700;font-size:20px;letter-spacing:1px;
    border:4px solid {DARK_NAVY};
    box-shadow:0 0 0 4px {AMBER},0 8px 24px rgba(255,177,32,0.5);
    z-index:20;}}
/* Left column — flex */
.col-l{{position:absolute;top:44px;left:44px;width:{SPLIT-88}px;
    display:flex;flex-direction:column;gap:0;z-index:15;}}
/* Right column — shifted right so VS circle (r=36) doesn't clip text */
.col-r{{position:absolute;top:44px;left:{SPLIT+50}px;width:{1080-SPLIT-94}px;
    display:flex;flex-direction:column;gap:0;z-index:15;}}
.col-kicker{{font-family:'DM Sans';font-weight:700;font-size:23px;
    color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:3px;
    margin-top:108px;margin-bottom:10px;}}
.col-head{{font-family:Inter;font-weight:700;font-size:44px;line-height:1.05;
    color:white;letter-spacing:-2px;margin-bottom:16px;}}
/* Bottom banner */
.banner{{position:absolute;bottom:0;left:0;right:0;height:140px;
    background:{DEEP_BLUE};z-index:25;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 44px;border-top:3px solid {DARK_NAVY};gap:24px;}}
.banner-text{{font-family:'DM Sans';font-weight:700;font-size:22px;
    color:rgba(255,255,255,0.9);line-height:1.4;flex:1;}}
.banner-text strong{{color:{AMBER};}}
.cta-btn{{display:flex;align-items:center;gap:12px;white-space:nowrap;
    background:{AMBER};color:{DEEP_BLUE};
    font-family:Inter;font-weight:700;font-size:17px;
    padding:14px 24px;border-radius:50px;letter-spacing:0.5px;
    box-shadow:0 4px 18px rgba(255,177,32,0.35);flex-shrink:0;}}
.cta-arrow{{width:32px;height:32px;background:{DEEP_BLUE};border-radius:50%;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="left"></div>
<div class="right"></div>
{grad_photo_html}
{direct_photo_html}
<div class="divider"></div>
<div class="vs">VS</div>
<img src="data:image/png;base64,{logo_b64}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:30;">
<div style="position:absolute;top:44px;right:44px;z-index:30;
    background:rgba(255,255,255,0.1);color:rgba(255,255,255,0.7);
    padding:9px 20px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:13px;
    letter-spacing:2px;text-transform:uppercase;
    border:1.5px solid rgba(255,255,255,0.15);">Career paths</div>
<div class="col-l">
  <div class="col-kicker">Graduate scheme</div>
  <div class="col-head">Structured.<br>Competitive.<br>Slower to start.</div>
  {scheme_rows}
</div>
<div class="col-r">
  <div class="col-kicker">Direct entry</div>
  <div class="col-head">Faster start.<br>Broader choice.<br>Less structure.</div>
  {direct_rows}
</div>
<div class="banner">
  <div class="banner-text">
    Neither is wrong. The question is: <strong>what do you need first?</strong><br>
    Most graduates only look at one path. Most opportunities are on the other.
  </div>
  <div class="cta-btn">
    <div>
      <div>Find your path at</div>
      <div style="font-size:15px;opacity:0.75;font-weight:600;">internwise.co.uk</div>
    </div>
    <div class="cta-arrow">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M3 8H13M9 4L13 8L9 12" stroke="{AMBER}" stroke-width="2.2"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
</div>
</div></body></html>"""

    _render(html, os.path.join(campaign_dir, "statcard_schemes.png"))
    print("Done - Grad Schemes vs Direct Entry v2 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week4/d4-schemes")
