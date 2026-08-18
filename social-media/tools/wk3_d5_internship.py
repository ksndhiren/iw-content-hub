"""
Internwise — Turn Your Internship Into a Graduate Job Offer (Week 3, Day 5)
7-slide carousel: dark design, action-oriented, one photo on slide 6
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
    print(f"  ✓ {path}")

LOGO_B64 = None
def _logo(dark=False):
    global LOGO_B64
    if LOGO_B64 is None:
        LOGO_B64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    if not LOGO_B64: return ""
    filt = "filter:invert(1) sepia(1) saturate(3) hue-rotate(190deg);opacity:0.7;" if dark else "opacity:0.95;"
    return f'<img src="data:image/png;base64,{LOGO_B64}" style="height:72px;{filt}">'

def _spark(s,t,l,c,o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:14;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'

DARK_BASE = f"background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);"
GRAIN_CSS = "background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);background-size:3px 3px;"

def _dark_slide(extra_css, body, badge="", out=""):
    f = _fonts()
    badge_html = f'<div style="position:absolute;top:44px;right:50px;background:{AMBER};color:{DEEP_BLUE};padding:12px 26px;border-radius:50px;font-family:Inter;font-weight:700;font-size:15px;letter-spacing:2px;text-transform:uppercase;transform:rotate(4deg);box-shadow:0 8px 22px rgba(255,177,32,0.45);z-index:20;">{badge}</div>' if badge else ""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;{DARK_BASE}}}
.grain{{position:absolute;inset:0;z-index:2;pointer-events:none;{GRAIN_CSS}}}
.logo{{position:absolute;top:44px;left:44px;z-index:20;}}
.url{{position:absolute;bottom:44px;left:50px;font-family:Inter;font-weight:700;
    font-size:20px;color:rgba(255,255,255,0.3);z-index:20;}}
{extra_css}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="logo">{_logo()}</div>
{badge_html}{body}
<div class="url">internwise.co.uk</div>
</div></body></html>"""
    _render(html, out)


def _arch_photo(photo_path, accent, bottom=20, right=20, w=390, h=480):
    """Full-photo arch — no bg removal needed."""
    if not photo_path: return ""
    b64 = _b64(photo_path)
    if not b64: return ""
    mime = "image/png" if str(photo_path).endswith(".png") else "image/jpeg"
    src = f"data:{mime};base64,{b64}"
    return f"""
<div style="position:absolute;bottom:{bottom}px;right:{right}px;
            width:{w}px;height:{h}px;
            border-radius:195px 195px 40px 40px;
            overflow:hidden;z-index:5;
            box-shadow:0 20px 50px rgba(0,0,0,0.45);">
  <img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:center top;">
  <div style="position:absolute;inset:0;background:linear-gradient(to bottom,transparent 40%,{accent}cc 100%);"></div>
</div>"""


def _slide1(out, photo=None):
    photo_html = _arch_photo(photo, AMBER, bottom=20, right=20, w=400, h=500) if photo else ""
    right_margin = "440px" if photo else "50px"
    _dark_slide(
        extra_css=f"""
.hl{{position:absolute;top:160px;left:50px;right:{right_margin};
    font-family:Inter;font-weight:700;font-size:76px;line-height:1.0;
    color:rgba(255,255,255,0.5);letter-spacing:-3px;z-index:20;}}
.hl2{{position:absolute;top:400px;left:50px;right:{right_margin};
    font-family:Inter;font-weight:700;font-size:64px;line-height:1.0;
    color:white;letter-spacing:-3px;z-index:20;}}
.hl2 em{{color:{AMBER};font-style:italic;}}
.sub{{position:absolute;bottom:80px;left:50px;
    font-family:'DM Sans';font-weight:600;font-size:26px;
    color:rgba(255,255,255,0.55);z-index:20;}}
""",
        body=f"""
<div class="hl">Most interns<br>finish and leave.</div>
<div class="hl2">Here's what the ones<br>who got <em>offers</em><br>did differently.</div>
<div class="sub">Swipe for the playbook →</div>
{photo_html}
{_spark(24,560,820,AMBER,0.5)}{_spark(16,750,900,CORAL,0.4)}
""",
        out=out
    )


def _numbered_slide(n, color, headline, body_lines, out, photo=None):
    lines_html = "".join([
        f'<div style="font-family:\'DM Sans\';font-weight:600;font-size:24px;color:rgba(255,255,255,0.72);line-height:1.4;margin-bottom:6px;">{l}</div>'
        for l in body_lines
    ])
    photo_html = _arch_photo(photo, color, bottom=20, right=20, w=390, h=460) if photo else ""
    right_margin = "430px" if photo else "100px"
    accent_text = DEEP_BLUE if color in (AMBER, MINT) else "white"
    _dark_slide(
        extra_css=f"""
.badge{{position:absolute;top:44px;right:50px;
    width:86px;height:86px;border-radius:50%;
    background:{color};color:{accent_text};
    display:flex;align-items:center;justify-content:center;
    font-family:Inter;font-weight:700;font-size:40px;
    box-shadow:0 8px 22px rgba(0,0,0,0.3);z-index:20;}}
.kicker{{position:absolute;top:170px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:20px;
    color:{color};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.hl{{position:absolute;top:210px;left:50px;right:{right_margin};
    font-family:Inter;font-weight:700;font-size:66px;line-height:0.95;
    color:white;letter-spacing:-3px;z-index:20;}}
.body{{position:absolute;top:470px;left:50px;right:{right_margin};z-index:20;}}
""",
        body=f"""
<div class="badge">{n}</div>
<div class="kicker">Thing {n}</div>
<div class="hl">{headline}</div>
<div class="body">{lines_html}</div>
{photo_html}
""",
        out=out
    )


def _slide5(out):
    """The question slide - contrast bad vs good."""
    _dark_slide(
        extra_css=f"""
.kicker{{position:absolute;top:155px;left:50px;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;z-index:20;}}
.hl{{position:absolute;top:195px;left:50px;right:50px;
    font-family:Inter;font-weight:700;font-size:58px;line-height:0.9;
    color:white;letter-spacing:-2px;z-index:20;}}
.box{{position:absolute;left:50px;right:50px;z-index:20;
    border-radius:18px;padding:28px 32px;}}
.bad{{top:390px;background:rgba(255,107,107,0.12);
    border:2px solid {CORAL};}}
.good{{top:570px;background:rgba(127,219,182,0.12);
    border:2px solid {MINT};}}
.label{{font-family:'DM Sans';font-weight:700;font-size:16px;
    text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;}}
.q{{font-family:Inter;font-weight:700;font-size:30px;color:white;letter-spacing:-0.5px;}}
.then{{position:absolute;bottom:100px;left:50px;right:50px;z-index:20;
    font-family:'DM Sans';font-weight:700;font-size:24px;
    color:rgba(255,255,255,0.6);}}
.then strong{{color:{AMBER};}}
""",
        body=f"""
<div class="kicker">The question</div>
<div class="hl">Most interns ask<br>the wrong thing.</div>
<div class="box bad">
  <div class="label" style="color:{CORAL};">Wrong question</div>
  <div class="q">"Can I have a job?"</div>
</div>
<div class="box good">
  <div class="label" style="color:{MINT};">Right question</div>
  <div class="q">"What would I need to demonstrate<br>for a return offer?"</div>
</div>
<div class="then">Then go and <strong>demonstrate it.</strong></div>
""",
        out=out
    )


def _slide6(out, photo_path):
    """Warning slide with full-bleed photo + overlay."""
    f = _fonts()
    img_src = _src(photo_path) if photo_path else ""
    photo_block = f'<div style="position:absolute;inset:0;z-index:3;"><img src="{img_src}" style="width:100%;height:100%;object-fit:cover;opacity:0.25;"></div>' if img_src else ""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;{DARK_BASE}}}
.grain{{position:absolute;inset:0;z-index:4;pointer-events:none;{GRAIN_CSS}}}
.logo{{position:absolute;top:44px;left:44px;z-index:20;}}
.url{{position:absolute;bottom:44px;left:50px;font-family:Inter;font-weight:700;
    font-size:20px;color:rgba(255,255,255,0.3);z-index:20;}}
.kicker{{position:absolute;top:155px;left:50px;z-index:20;
    font-family:'DM Sans';font-weight:700;font-size:22px;
    color:{CORAL};text-transform:uppercase;letter-spacing:3px;}}
.hl{{position:absolute;top:195px;left:50px;right:50px;z-index:20;
    font-family:Inter;font-weight:700;font-size:80px;line-height:0.9;
    color:white;letter-spacing:-4px;font-style:italic;}}
.sub{{position:absolute;top:500px;left:50px;right:50px;z-index:20;
    font-family:'DM Sans';font-weight:600;font-size:30px;
    color:rgba(255,255,255,0.6);}}
.sub strong{{color:{CORAL};}}
.wonder{{position:absolute;bottom:110px;left:50px;right:50px;z-index:20;
    font-family:Inter;font-weight:700;font-size:28px;
    color:rgba(255,255,255,0.45);font-style:italic;}}
</style></head><body><div class="c">
{photo_block}
<div class="grain"></div>
<div class="logo">{_logo()}</div>
<div class="kicker">What most interns do</div>
<div class="hl">Turn up.<br>Do the work.<br>Say goodbye.</div>
<div class="sub">And <strong>wonder</strong> why the offer didn't come.</div>
<div class="wonder">"I thought I did well..."</div>
<div class="url">internwise.co.uk</div>
</div></body></html>"""
    _render(html, out)


def _slide7(out):
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
    font-family:Inter;font-weight:700;font-size:90px;line-height:0.88;
    color:{DEEP_BLUE};letter-spacing:-4px;z-index:20;}}
.hl em{{color:{AMBER};font-style:italic;}}
.sub{{position:absolute;top:560px;left:60px;right:60px;
    font-family:'DM Sans';font-weight:600;font-size:28px;
    color:rgba(38,77,126,0.6);z-index:20;line-height:1.4;}}
.pill{{position:absolute;bottom:90px;left:60px;
    background:{DEEP_BLUE};color:white;
    padding:22px 44px;border-radius:60px;
    font-family:Inter;font-weight:700;font-size:28px;
    border:3px solid {DARK_NAVY};box-shadow:6px 6px 0 {DARK_NAVY};z-index:20;}}
</style></head><body><div class="c">
<div class="logo">{logo_dark}</div>
<div class="hl">Find internships<br>worth <em>converting.</em></div>
<div class="sub">Paid placements across tech, marketing,<br>finance and more. Apply today.</div>
<div class="pill">internwise.co.uk →</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating Internship Conversion Carousel (Week 3, Day 5)...")
    print("  ↓ Fetching photos...")
    photos = {}
    fetch_list = [
        ("hook",    "young professional confident smiling intern office portrait",         0),
        ("slide2",  "young woman interview professional attentive focused portrait",       0),
        ("slide3",  "young man presenting project whiteboard office portrait",             0),
        ("slide4",  "young professionals talking conversation office smiling portrait",    1),
        ("warning", "person leaving office walking away professional",                     0),
    ]
    for key, query, idx in fetch_list:
        try:
            photos[key] = get_photo(query, index=idx, orientation="portrait", size="medium")
            print(f"    ✓ {key}: {photos[key]}")
        except Exception as e:
            print(f"    ! {key} failed: {e}")
            photos[key] = None

    _slide1(os.path.join(campaign_dir, "slide_1.png"), photo=photos.get("hook"))
    _numbered_slide(1, AMBER,
        "Treat it like a<br>10&#8209;week interview.",
        ["Not a CV builder. Not work experience.", "An audition."],
        os.path.join(campaign_dir, "slide_2.png"),
        photo=photos.get("slide2"))
    _numbered_slide(2, MINT,
        "Own one project. Deliver it visibly.",
        ["Don't wait to be assigned credit.", "Make sure the right people see it."],
        os.path.join(campaign_dir, "slide_3.png"),
        photo=photos.get("slide3"))
    _numbered_slide(3, PURPLE,
        "Build relationships up and across.",
        ["Not just your manager.", "The people two levels up. The people in other teams.", "Conversations, not just LinkedIn connections."],
        os.path.join(campaign_dir, "slide_4.png"),
        photo=photos.get("slide4"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"), photos.get("warning"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    print("✓ Internship conversion carousel complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/wk3-d5-internship")
