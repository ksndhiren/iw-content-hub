"""
Internwise - Networking Without Cringe (Week 6, Day 2)
Hook: Full MINT bg, SVG connection-web ghost, pure typography — no person.
Accent: MINT. Single statcard format (like D2 week 5 but totally different layout).
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"

LOGO_W = LOGO_C = None
def _load_logos():
    global LOGO_W, LOGO_C
    if LOGO_W is None:
        LOGO_W = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
        LOGO_C = _b64(os.path.join(BRANDING_DIR, "PNG", "Internwise.Com-Horizontal logo.png")) or ""

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

GRAIN_DARK = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(0,0,0,0.06) 1px,transparent 1px);background-size:3px 3px;}"

# SVG connection-web ghost (nodes + lines, low opacity)
NETWORK_SVG = """<svg style="position:absolute;inset:0;width:1080px;height:1080px;opacity:0.12;z-index:1;"
     viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#162d4a" stroke-width="2" fill="none">
    <line x1="200" y1="180" x2="480" y2="320"/>
    <line x1="480" y1="320" x2="750" y2="200"/>
    <line x1="750" y1="200" x2="920" y2="450"/>
    <line x1="480" y1="320" x2="600" y2="580"/>
    <line x1="200" y1="180" x2="100" y2="520"/>
    <line x1="100" y1="520" x2="350" y2="700"/>
    <line x1="350" y1="700" x2="600" y2="580"/>
    <line x1="600" y1="580" x2="850" y2="720"/>
    <line x1="920" y1="450" x2="850" y2="720"/>
    <line x1="350" y1="700" x2="280" y2="950"/>
    <line x1="600" y1="580" x2="540" y2="880"/>
    <line x1="850" y1="720" x2="980" y2="900"/>
  </g>
  <g fill="#162d4a">
    <circle cx="200" cy="180" r="14"/>
    <circle cx="480" cy="320" r="20"/>
    <circle cx="750" cy="200" r="12"/>
    <circle cx="920" cy="450" r="16"/>
    <circle cx="100" cy="520" r="10"/>
    <circle cx="350" cy="700" r="18"/>
    <circle cx="600" cy="580" r="22"/>
    <circle cx="850" cy="720" r="14"/>
    <circle cx="280" cy="950" r="10"/>
    <circle cx="540" cy="880" r="12"/>
    <circle cx="980" cy="900" r="10"/>
  </g>
</svg>"""


def _statcard(out):
    f = _fonts()

    methods = [
        ("Comment first, connect second",   "LOWEST BARRIER",  DARK_NAVY, "white",
         "Leave one genuinely useful comment on their post. Then connect. They know your name before the request arrives."),
        ("The 'coffee chat' ask",           "MOST EFFECTIVE",  CORAL,     "white",
         "15 minutes, specific topic, easy to say yes. Not 'Can I pick your brain?' - 'Could I ask you one question about X?'"),
        ("Event follow-up within 24h",      "HIGHEST CONVERT", DEEP_BLUE, "white",
         "Met someone at an event? Message within 24 hours. Reference one thing from your conversation. They remember you."),
        ("Alumni advantage",                "BUILT-IN WARMTH", AMBER,     DARK_NAVY,
         "Same university = automatic common ground. Alumni respond at 3x the rate of cold connections. Always start here."),
        ("Give before you ask",             "LONG GAME",       PURPLE,    "white",
         "Share their content. Reply with insight. Tag them in relevant posts. Build social proof before you ever ask for anything."),
    ]

    rows = ""
    for i, (name, pill, pill_bg, pill_fg, action) in enumerate(methods):
        connector = ""
        if i > 0:
            connector = f'<div style="width:4px;height:14px;background:{DARK_NAVY};margin:0 0 0 25px;opacity:0.3;"></div>'
        rows += f"""{connector}
<div style="display:flex;align-items:stretch;border:3px solid {DARK_NAVY};
             box-shadow:4px 4px 0 {DARK_NAVY};border-radius:12px;overflow:hidden;">
  <div style="width:54px;flex-shrink:0;background:{DARK_NAVY};display:flex;align-items:center;
               justify-content:center;font-family:Inter;font-weight:700;font-size:20px;
               color:rgba(255,255,255,0.4);">{i+1}</div>
  <div style="flex:1;background:rgba(22,45,74,0.06);padding:12px 18px;display:flex;align-items:center;gap:14px;">
    <div style="font-family:Inter;font-weight:700;font-size:28px;color:{DARK_NAVY};
                 min-width:230px;flex-shrink:0;word-break:keep-all;hyphens:none;">{name}</div>
    <div style="background:{pill_bg};color:{pill_fg};padding:4px 12px;border-radius:50px;
                 font-family:Inter;font-weight:700;font-size:10px;letter-spacing:1.5px;
                 white-space:nowrap;flex-shrink:0;">{pill}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:20px;
                 color:rgba(22,45,74,0.6);line-height:1.35;">{action}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:#FFFDE7;}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:40px 50px;}}
{GRAIN_DARK}
</style></head><body><div class="c">
{NETWORK_SVG}
<div class="grain"></div>
<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:40px;left:44px;height:62px;opacity:0.95;z-index:25;">
<div style="position:absolute;top:40px;right:44px;background:{DARK_NAVY};color:{MINT};
             padding:10px 22px;border-radius:50px;font-family:Inter;font-weight:700;
             font-size:18px;letter-spacing:2px;text-transform:uppercase;
             border:3px solid {DARK_NAVY};box-shadow:3px 3px 0 rgba(0,0,0,0.2);z-index:20;
             transform:rotate(-2deg);">Networking guide</div>
<div style="padding-top:74px;margin-bottom:18px;flex-shrink:0;position:relative;z-index:5;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{DARK_NAVY};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;opacity:0.6;">5 methods that actually work</div>
  <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
               color:{DARK_NAVY};letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    Network without<br>the <em style="color:{CORAL};font-style:italic;">cringe.</em>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:5;">{rows}</div>
<div style="flex-shrink:0;margin-top:14px;display:inline-flex;align-items:center;gap:12px;
             background:{DARK_NAVY};color:{MINT};padding:14px 26px;border-radius:50px;
             border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 rgba(0,0,0,0.2);
             font-family:Inter;font-weight:700;font-size:20px;width:fit-content;position:relative;z-index:5;">
  Find roles at internwise.co.uk &#8594;
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Networking Without Cringe (Week 6, Day 2)...")
    _load_logos()
    _statcard(os.path.join(campaign_dir, "statcard_networking.png"))
    register_design("mint_statcard_network_web", "week6/d2-networking", "week6")
    print("Done - networking statcard complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week6/d2-networking")
