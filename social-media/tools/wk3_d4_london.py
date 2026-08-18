"""
Internwise — London vs Regional Stat Card (Week 3, Day 4)
Single 1080x1080 stat card: split canvas with two salary figures + person photo
"""
import os, base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_photo

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


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating London vs Regional Stat Card (Week 3, Day 4)...")

    print("  ↓ Fetching city photos...")
    manchester_src = ""
    london_src = ""
    try:
        p = get_photo("Manchester city skyline northern quarter street", index=0, orientation="landscape")
        print(f"    ✓ Manchester: {p}")
        b64 = _b64(p)
        if b64: manchester_src = f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        print(f"    ! Manchester photo failed: {e}")
    try:
        p = get_photo("London city skyline Thames skyscrapers", index=0, orientation="landscape")
        print(f"    ✓ London: {p}")
        b64 = _b64(p)
        if b64: london_src = f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        print(f"    ! London photo failed: {e}")

    f = _fonts()
    logo_b64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="height:72px;opacity:0.95;">' if logo_b64 else ""

    # City photo backgrounds — full-panel photo with dark gradient overlay so text stays legible
    mcr_bg = f"""
<div style="position:absolute;inset:0;z-index:4;">
  <img src="{manchester_src}" style="width:100%;height:100%;object-fit:cover;object-position:center;">
  <div style="position:absolute;inset:0;background:linear-gradient(160deg,{DEEP_BLUE}e0 0%,{DEEP_BLUE}99 60%,transparent 100%);"></div>
</div>""" if manchester_src else ""

    lon_bg = f"""
<div style="position:absolute;inset:0;z-index:4;">
  <img src="{london_src}" style="width:100%;height:100%;object-fit:cover;object-position:center;">
  <div style="position:absolute;inset:0;background:linear-gradient(160deg,{DARK_NAVY}e8 0%,{DARK_NAVY}aa 60%,transparent 100%);"></div>
</div>""" if london_src else ""

    # Even split at 540px so divider, VS badge, and panels all align
    SPLIT = 540

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;font-family:Inter;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{DARK_NAVY};}}
.grain{{position:absolute;inset:0;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);
    background-size:3px 3px;}}
.left{{position:absolute;top:0;left:0;width:{SPLIT}px;height:1080px;overflow:hidden;
    background:linear-gradient(160deg,{DEEP_BLUE} 0%,#1d3d6b 100%);z-index:3;}}
.right{{position:absolute;top:0;left:{SPLIT}px;width:{1080-SPLIT}px;height:1080px;overflow:hidden;
    background:linear-gradient(160deg,{DARK_NAVY} 0%,#0e1e33 100%);z-index:3;}}
/* Divider exactly on the split */
.divider{{position:absolute;top:0;left:{SPLIT-3}px;width:6px;height:1080px;
    background:{CORAL};z-index:10;box-shadow:0 0 18px {CORAL}88;}}
/* VS badge centred on divider */
.vs{{position:absolute;top:50%;left:{SPLIT}px;transform:translate(-50%,-50%);
    width:74px;height:74px;border-radius:50%;
    background:{CORAL};color:white;
    display:flex;align-items:center;justify-content:center;
    font-family:Inter;font-weight:700;font-size:22px;letter-spacing:1px;
    border:4px solid {DARK_NAVY};
    box-shadow:0 0 0 4px {CORAL},0 8px 24px rgba(255,107,107,0.5);
    z-index:20;}}
.logo{{position:absolute;top:44px;left:44px;z-index:30;}}
.badge{{position:absolute;top:44px;right:44px;z-index:30;
    background:{AMBER};color:{DEEP_BLUE};
    padding:10px 22px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(3deg);
    box-shadow:0 6px 16px rgba(255,177,32,0.45);}}
/* Kicker row above both columns */
.kicker-l{{position:absolute;top:128px;left:44px;z-index:15;
    font-family:'DM Sans';font-weight:700;font-size:20px;
    color:rgba(255,255,255,0.6);text-transform:uppercase;letter-spacing:3px;}}
.kicker-r{{position:absolute;top:128px;right:44px;z-index:15;text-align:right;
    font-family:'DM Sans';font-weight:700;font-size:20px;
    color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:3px;}}
/* Gross salary — secondary, small */
.salary-l{{position:absolute;top:158px;left:44px;z-index:15;
    font-family:'DM Sans';font-weight:600;font-size:26px;line-height:1;
    color:rgba(255,255,255,0.4);}}
.salary-r{{position:absolute;top:158px;right:44px;z-index:15;text-align:right;
    font-family:'DM Sans';font-weight:600;font-size:26px;line-height:1;
    color:rgba(255,255,255,0.3);}}
/* Hero label */
.net-label-l{{position:absolute;top:210px;left:44px;z-index:15;
    font-family:'DM Sans';font-weight:700;font-size:20px;
    color:{MINT};text-transform:uppercase;letter-spacing:2px;}}
.net-label-r{{position:absolute;top:210px;right:44px;z-index:15;text-align:right;
    font-family:'DM Sans';font-weight:700;font-size:20px;
    color:{CORAL};text-transform:uppercase;letter-spacing:2px;}}
/* Hero number — monthly net */
.net-l{{position:absolute;top:238px;left:44px;z-index:15;
    font-family:Inter;font-weight:700;font-size:110px;line-height:0.9;
    color:{AMBER};letter-spacing:-5px;
    text-shadow:0 4px 20px rgba(0,0,0,0.4);}}
.net-r{{position:absolute;top:238px;right:44px;z-index:15;text-align:right;
    font-family:Inter;font-weight:700;font-size:90px;line-height:0.9;
    color:rgba(255,255,255,0.35);letter-spacing:-5px;}}
/* City name */
.city-l{{position:absolute;top:440px;left:44px;z-index:15;
    font-family:Inter;font-weight:700;font-size:44px;
    color:white;letter-spacing:-1px;}}
.city-r{{position:absolute;top:440px;right:44px;z-index:15;text-align:right;
    font-family:Inter;font-weight:700;font-size:44px;
    color:rgba(255,255,255,0.5);letter-spacing:-1px;}}
/* Tag pills */
.tag-l{{position:absolute;top:498px;left:44px;z-index:15;
    background:{MINT};color:{DEEP_BLUE};
    padding:9px 22px;border-radius:30px;
    font-family:Inter;font-weight:700;font-size:17px;letter-spacing:1px;}}
.tag-r{{position:absolute;top:498px;right:44px;z-index:15;
    background:rgba(255,107,107,0.18);color:{CORAL};
    border:2px solid {CORAL};
    padding:9px 22px;border-radius:30px;
    font-family:Inter;font-weight:700;font-size:17px;letter-spacing:1px;}}
/* Cost breakdown rows */
.rows-l{{position:absolute;top:568px;left:44px;right:570px;z-index:15;}}
.rows-r{{position:absolute;top:568px;right:44px;left:570px;z-index:15;}}
.row{{padding:20px 24px;border-radius:16px;margin-bottom:14px;
    background:rgba(255,255,255,0.09);border:1px solid rgba(255,255,255,0.12);}}
.row-label{{font-family:'DM Sans';font-weight:700;font-size:15px;color:rgba(255,255,255,0.5);
    text-transform:uppercase;letter-spacing:2px;display:block;margin-bottom:6px;}}
.row-val{{font-family:Inter;font-weight:700;font-size:58px;line-height:1;letter-spacing:-2px;display:block;}}
/* Banner */
.banner{{position:absolute;bottom:0;left:0;right:0;height:130px;
    background:{DEEP_BLUE};z-index:25;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 44px;border-top:3px solid {DARK_NAVY};}}
.banner-text{{font-family:'DM Sans';font-weight:700;font-size:26px;
    color:rgba(255,255,255,0.9);line-height:1.3;}}
.banner-text strong{{color:{AMBER};}}
.banner-url{{font-family:Inter;font-weight:700;font-size:20px;color:rgba(255,255,255,0.4);white-space:nowrap;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="left">{mcr_bg}</div>
<div class="right">{lon_bg}</div>
<div class="divider"></div>
<div class="vs">VS</div>
<div class="logo">{logo_img}</div>
<div class="badge">Real maths</div>

<!-- Kickers -->
<div class="kicker-l">Manchester</div>
<div class="kicker-r">London</div>

<!-- Gross salary (secondary) -->
<div class="salary-l">£27,000 gross</div>
<div class="salary-r">£33,000 gross</div>

<!-- Monthly net (the hero number) -->
<div class="net-label-l">Monthly take-home</div>
<div class="net-l">~£950</div>
<div class="net-label-r">Monthly take-home</div>
<div class="net-r">~£750</div>

<!-- City labels -->
<div class="city-l">Manchester</div>
<div class="city-r">London</div>
<div class="tag-l">More left over</div>
<div class="tag-r">Less left over</div>

<!-- Cost breakdown -->
<div class="rows-l">
  <div class="row">
    <div class="row-label">Rent / mo</div>
    <div class="row-val" style="color:{MINT};">~£700</div>
  </div>
  <div class="row">
    <div class="row-label">Transport</div>
    <div class="row-val" style="color:{MINT};">~£80</div>
  </div>
</div>
<div class="rows-r">
  <div class="row">
    <div class="row-label">Rent / mo</div>
    <div class="row-val" style="color:{CORAL};">~£1,500</div>
  </div>
  <div class="row">
    <div class="row-label">Transport</div>
    <div class="row-val" style="color:{CORAL};">~£180</div>
  </div>
</div>

<div class="banner">
  <div class="banner-text">A <strong>£6K higher salary</strong> that leaves you with <strong>£200 less</strong> each month.</div>
  <div class="banner-url">internwise.co.uk</div>
</div>
</div></body></html>"""

    _render(html, os.path.join(campaign_dir, "statcard_london.png"))
    print("✓ London vs Regional stat card complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/wk3-d4-london")
