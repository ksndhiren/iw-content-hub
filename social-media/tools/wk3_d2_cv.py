"""
Internwise — CV with No Experience Tip Card (Week 3, Day 2)
Single 1080x1080 tip card: split dark/cream design
"""
import os, base64
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; OFF_WHITE = "#FAF5EC"; MINT = "#7FDBB6"

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
    print(f"  ✓ {path}")


TIPS = [
    ("Modules and projects",      "Name the relevant ones specifically."),
    ("Society roles",             "Treasurer, rep, events lead - all count."),
    ("Part-time work",            "Customer service is communication under pressure."),
    ("Freelance or side projects","Even one client counts."),
    ("Volunteering",              "Especially anything with responsibility or numbers behind it."),
]

def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating CV Tip Card (Week 3, Day 2)...")
    f = _fonts()
    logo_b64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="height:72px;opacity:0.95;">' if logo_b64 else ""

    tips_html = ""
    colors = [AMBER, CORAL, MINT, DEEP_BLUE, "#FF9961"]
    for i, (title, desc) in enumerate(TIPS):
        rot = -1.5 if i % 2 == 0 else 1.5
        c = colors[i]
        tips_html += f"""
<div style="display:flex;align-items:center;gap:18px;
     background:white;border:3px solid {DARK_NAVY};
     border-radius:16px;padding:14px 18px;
     box-shadow:5px 5px 0 {DARK_NAVY};
     transform:rotate({rot}deg);">
  <div style="width:52px;height:52px;border-radius:50%;flex-shrink:0;
       background:{c};display:flex;align-items:center;justify-content:center;
       font-family:Inter;font-weight:700;font-size:22px;
       color:{'#162d4a' if c in (AMBER, MINT, '#FF9961') else 'white'};">{i+1}</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:22px;
         color:{DEEP_BLUE};line-height:1.1;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:18px;
         color:rgba(38,77,126,0.65);margin-top:2px;">{desc}</div>
  </div>
</div>"""

    # CV document illustration SVG — sits top-right of hero zone
    cv_icon = f"""
<svg style="position:absolute;top:80px;right:60px;z-index:15;opacity:0.18;"
     width="220" height="260" viewBox="0 0 220 260" fill="none">
  <!-- Document body -->
  <rect x="20" y="10" width="160" height="210" rx="14"
        fill="white" stroke="white" stroke-width="2"/>
  <!-- Folded corner -->
  <path d="M140 10 L180 50 L140 50 Z" fill="{DARK_NAVY}" opacity="0.5"/>
  <!-- Text lines -->
  <rect x="40" y="70"  width="100" height="10" rx="5" fill="{AMBER}" opacity="0.9"/>
  <rect x="40" y="90"  width="80"  height="8"  rx="4" fill="white" opacity="0.6"/>
  <rect x="40" y="110" width="90"  height="8"  rx="4" fill="white" opacity="0.6"/>
  <rect x="40" y="130" width="70"  height="8"  rx="4" fill="white" opacity="0.6"/>
  <!-- Divider -->
  <rect x="40" y="150" width="100" height="2"  rx="1" fill="white" opacity="0.3"/>
  <!-- Bullet rows -->
  <circle cx="50" cy="168" r="5" fill="{MINT}" opacity="0.9"/>
  <rect x="62" y="164" width="70" height="8" rx="4" fill="white" opacity="0.5"/>
  <circle cx="50" cy="186" r="5" fill="{CORAL}" opacity="0.9"/>
  <rect x="62" y="182" width="55" height="8" rx="4" fill="white" opacity="0.5"/>
  <!-- Big tick -->
  <circle cx="160" cy="210" r="34" fill="{MINT}" opacity="0.9"/>
  <path d="M146 210 L156 222 L176 198" stroke="{DARK_NAVY}" stroke-width="7"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{OFF_WHITE};}}
.hero{{position:absolute;top:0;left:0;right:0;height:460px;
    background:linear-gradient(135deg,{DEEP_BLUE} 0%,{DARK_NAVY} 100%);
    border-radius:0 0 40px 40px;}}
.grain{{position:absolute;inset:0;height:460px;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);
    background-size:3px 3px;}}
.logo{{position:absolute;top:44px;left:44px;z-index:20;}}
.badge{{position:absolute;top:44px;right:50px;z-index:20;
    background:{AMBER};color:{DEEP_BLUE};
    padding:10px 24px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(4deg);
    box-shadow:0 6px 18px rgba(255,177,32,0.4);}}
.hl{{position:absolute;top:130px;left:50px;right:280px;z-index:20;
    font-family:Inter;font-weight:700;font-size:68px;line-height:0.92;
    color:white;letter-spacing:-3px;}}
.hl em{{color:{AMBER};font-style:italic;}}
.sub{{position:absolute;top:350px;left:50px;z-index:20;
    font-family:'DM Sans';font-weight:600;font-size:22px;
    color:rgba(255,255,255,0.65);}}
.sub strong{{color:white;}}
.tips{{position:absolute;top:478px;left:44px;right:44px;
    display:flex;flex-direction:column;gap:10px;z-index:20;}}
.cta{{position:absolute;bottom:28px;left:50px;right:50px;
    display:flex;justify-content:space-between;align-items:center;z-index:20;}}
.cta-text{{font-family:'DM Sans';font-weight:700;font-size:20px;color:{DEEP_BLUE};opacity:0.55;}}
.cta-url{{font-family:Inter;font-weight:700;font-size:22px;color:{DEEP_BLUE};}}
</style></head><body><div class="c">
<div class="hero"></div>
<div class="grain"></div>
{cv_icon}
<div class="logo">{logo_img}</div>
<div class="badge">CV tips</div>
<div class="hl">You have <em>more</em><br>experience than<br>you think.</div>
<div class="sub">5 things you're <strong>not</strong> putting on your CV.</div>
<div class="tips">{tips_html}</div>
<div class="cta">
  <div class="cta-text">Build a CV that gets past the filter.</div>
  <div class="cta-url">internwise.co.uk →</div>
</div>
</div></body></html>"""

    _render(html, os.path.join(campaign_dir, "tipcard_cv.png"))
    print("✓ CV tip card complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/wk3-d2-cv")
