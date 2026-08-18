"""
Internwise - The Hidden Job Market (Week 7, Day 2)
Trendy: Newsprint/halftone aesthetic, torn-paper big number, taped-note stickers.
Single statcard. Accent: OFF_WHITE bg + DEEP_BLUE + CORAL.
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
OFF_WHITE = "#FAF5EC"; HOT_PINK = "#FF3D8A"; LIME = "#D4FF3D"

LOGO_C = None
def _load_logos():
    global LOGO_C
    if LOGO_C is None:
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

# Halftone dot pattern (bigger dots, low opacity)
HALFTONE = ("background-image:radial-gradient(rgba(22,45,74,0.18) 2px,transparent 2px);"
            "background-size:12px 12px;")

# Newsprint paper texture bg
NEWSPRINT = (f"background:{OFF_WHITE};background-image:"
             "radial-gradient(rgba(22,45,74,0.05) 1px,transparent 1px),"
             "radial-gradient(rgba(22,45,74,0.03) 1px,transparent 1px);"
             "background-size:4px 4px, 8px 8px;background-position:0 0, 2px 2px;")

TAPE_STICKER = "background:rgba(255,177,32,0.85);padding:8px 22px;transform:rotate({rot}deg);box-shadow:0 3px 6px rgba(0,0,0,0.15);"


def _statcard(out):
    f = _fonts()
    channels = [
        ("Referrals",       "40%", CORAL,     "Warm intros from people inside. Highest converting channel by 20x."),
        ("Direct outreach", "22%", DEEP_BLUE, "Cold DMs to hiring managers. Skips the ATS entirely if the message is good."),
        ("Alumni networks", "18%", AMBER,     "University alumni working at your target company. Built-in warm connection."),
        ("SME direct",      "12%", PURPLE,    "SMEs rarely post publicly. They hire the first great person who reaches out."),
        ("Public job posts", "8%", "#999999", "The one channel everyone uses. Where 92% of grads are fighting for 8% of roles."),
    ]
    rows = ""
    for i, (name, pct, color, action) in enumerate(channels):
        rows += f"""<div style="display:flex;align-items:center;gap:20px;padding:14px 20px;
             background:{OFF_WHITE};border:3px solid {DARK_NAVY};border-radius:14px;
             box-shadow:4px 4px 0 {DARK_NAVY};">
  <div style="font-family:Inter;font-weight:700;font-size:52px;color:{color};letter-spacing:-2px;
               min-width:110px;flex-shrink:0;">{pct}</div>
  <div style="flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{DARK_NAVY};letter-spacing:-0.5px;">{name}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:20px;color:rgba(22,45,74,0.65);margin-top:4px;line-height:1.35;">{action}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;{NEWSPRINT}}}
.c{{width:1080px;height:1080px;position:relative;padding:40px 50px;display:flex;flex-direction:column;}}
</style></head><body><div class="c">
<!-- Halftone bg block behind number -->
<div style="position:absolute;top:130px;left:-40px;width:520px;height:340px;{HALFTONE}z-index:1;
             transform:rotate(-4deg);"></div>

<!-- Header row: logo + tape sticker -->
<div style="display:flex;justify-content:space-between;align-items:center;position:relative;z-index:20;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:62px;">
  <div style="{TAPE_STICKER.replace('{rot}', '4')}font-family:Inter;font-weight:700;font-size:20px;
               color:{DARK_NAVY};letter-spacing:2px;text-transform:uppercase;">Hidden market</div>
</div>

<!-- Top row: torn-paper 70% + headline -->
<div style="display:flex;gap:30px;margin-top:34px;position:relative;z-index:10;align-items:flex-start;">
  <div style="flex-shrink:0;transform:rotate(-3deg);">
    <div style="background:{OFF_WHITE};padding:18px 34px;border:4px solid {DARK_NAVY};
                 box-shadow:8px 8px 0 {DARK_NAVY};">
      <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
                   text-transform:uppercase;letter-spacing:3px;margin-bottom:4px;">Never advertised</div>
      <div style="font-family:Inter;font-weight:700;font-size:140px;color:{DARK_NAVY};
                   line-height:0.9;letter-spacing:-8px;">70%</div>
      <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:24px;
                   color:{DARK_NAVY};letter-spacing:-1px;margin-top:2px;">of jobs are never posted.</div>
    </div>
  </div>
  <div style="flex:1;padding-top:14px;">
    <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:0.98;
                 color:{DARK_NAVY};letter-spacing:-2px;word-break:keep-all;hyphens:none;">
      You're fighting for <em style="color:{CORAL};font-style:italic;">the 8%.</em>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:22px;
                 color:rgba(22,45,74,0.7);margin-top:16px;line-height:1.4;">
      Public job boards show a fraction of what's out there. The other 92% is where the real access is.
    </div>
  </div>
</div>

<!-- Channels list -->
<div style="flex:1;margin-top:32px;display:flex;flex-direction:column;gap:10px;position:relative;z-index:10;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{DARK_NAVY};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:2px;">
    Where jobs actually get filled
  </div>
  {rows}
</div>

<!-- Footer row: CTA + sources -->
<div style="display:flex;justify-content:space-between;align-items:center;margin-top:18px;
             position:relative;z-index:20;">
  <div style="background:{DARK_NAVY};color:{OFF_WHITE};padding:14px 26px;border-radius:50px;
               font-family:Inter;font-weight:700;font-size:20px;
               border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {CORAL};">
    Find hidden roles at internwise.co.uk &#8594;
  </div>
  <div style="font-family:'DM Sans';font-weight:400;font-size:16px;color:rgba(22,45,74,0.5);">Sources: BLS 2025, LinkedIn Talent Insights 2026</div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Hidden Job Market (Week 7, Day 2)...")
    _load_logos()
    _statcard(os.path.join(campaign_dir, "statcard_hiddenmarket.png"))
    register_design("newsprint_halftone_tornpaper_statcard", "week7/d2-hiddenmarket", "week7")
    print("Done - hidden market complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week7/d2-hiddenmarket")
