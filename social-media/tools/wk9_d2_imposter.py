"""
Internwise - Imposter Syndrome in Your First Role (Week 9, Day 2)
Design language: WARM JOURNAL / SCRAPBOOK. Lined-paper base, washi tape, a real
Pexels portrait as a taped polaroid, handwritten-italic margin notes, doodle hearts
and stars, coffee ring. Single statcard.
Accent: warm terracotta + sage on paper.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import get_used_hashes, register_used_hashes, register_design, get_cutout_unique
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; DEEP_BLUE = "#264D7E"; OFF_WHITE = "#FAF5EC"

PAPER     = "#FBF6EA"
PAPER_LN  = "rgba(90,120,150,0.14)"   # ruled line
TERRA     = "#D8663F"; TERRA_D = "#B94E2C"
SAGE      = "#7A9B6E"; SAGE_D  = "#5E7E53"
MUSTARD   = "#E0A93E"
INK       = "#3A342E"
INK_SOFT  = "#6E655C"
TAPE      = "rgba(224,169,62,0.55)"
TAPE_SAGE = "rgba(122,155,110,0.5)"

LOGO_C = None
def _load_logos():
    global LOGO_C
    if LOGO_C is None:
        LOGO_C = _b64(os.path.join(BRANDING_DIR, "PNG", "Internwise.Com-Horizontal logo.png")) or ""

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

def _src(path):
    b = _b64(path)
    return f"data:image/png;base64,{b}" if b else ""

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

# doodle SVGs (hand-drawn)
HEART = lambda c: f'<svg width="46" height="42" viewBox="0 0 46 42"><path d="M23 38 C6 26 4 14 12 9 C18 5 23 11 23 15 C23 11 28 5 34 9 C42 14 40 26 23 38 Z" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round"/></svg>'
STAR = lambda c: f'<svg width="40" height="40" viewBox="0 0 40 40"><path d="M20 4 L24 16 L37 16 L26 24 L30 36 L20 28 L10 36 L14 24 L3 16 L16 16 Z" fill="none" stroke="{c}" stroke-width="3" stroke-linejoin="round"/></svg>'
ARROW = lambda c: f'<svg width="120" height="90" viewBox="0 0 120 90"><path d="M108 14 Q70 6 46 28 T14 52" stroke="{c}" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M26 40 L12 54 L30 60" stroke="{c}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
UNDERLINE = lambda c: f'<svg width="300" height="20" viewBox="0 0 300 20"><path d="M6 12 Q80 4 150 10 T294 8" stroke="{c}" stroke-width="4.5" fill="none" stroke-linecap="round"/></svg>'


def _statcard(out, photo_path):
    f = _fonts()
    photo = _src(photo_path)

    facts = [
        ("70%", "of people feel like a fraud at work at some point. It is the norm, not a defect.", TERRA_D),
        ("Day 1", "you were hired from a pool of hundreds. Someone experienced chose you on purpose.", SAGE_D),
        ("90 days", "is how long the wobble usually lasts. Competence arrives before the feeling does.", MUSTARD),
    ]
    fact_rows = ""
    for i, (big, txt, col) in enumerate(facts):
        fact_rows += f"""<div style="display:flex;gap:18px;align-items:flex-start;padding:14px 0;
             border-bottom:2px dotted rgba(90,120,150,0.25);">
  <div style="font-family:Inter;font-weight:700;font-size:38px;color:{col};min-width:120px;
               flex-shrink:0;letter-spacing:-1px;">{big}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{INK};line-height:1.4;">{txt}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{PAPER};
      background-image:repeating-linear-gradient(180deg,transparent 0 47px,{PAPER_LN} 47px 48px);}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;}}
.marg{{position:absolute;top:0;bottom:0;left:118px;width:2px;background:rgba(216,102,63,0.35);}}
</style></head><body><div class="c">
<div class="marg"></div>

<!-- header -->
<div style="display:flex;justify-content:space-between;align-items:flex-start;position:relative;z-index:20;">
  <div style="padding-left:78px;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:19px;color:{TERRA_D};
                 text-transform:uppercase;letter-spacing:3px;">Dear first-year-you</div>
    <div style="font-family:Inter;font-weight:700;font-size:52px;color:{INK};letter-spacing:-2px;
                 line-height:1.02;margin-top:6px;word-break:keep-all;hyphens:none;">
      You're not a <span style="font-style:italic;color:{TERRA_D};">fraud.</span>
    </div>
    <div style="margin-top:2px;margin-left:2px;">{UNDERLINE(TERRA)}</div>
  </div>
  <img src="data:image/png;base64,{LOGO_C}" style="height:46px;background:{PAPER};padding:4px 8px;">
</div>

<!-- Taped polaroid photo, right -->
<div style="position:absolute;top:250px;right:56px;width:344px;transform:rotate(3deg);z-index:15;">
  <div style="background:#fff;padding:16px 16px 60px 16px;box-shadow:0 14px 30px rgba(60,40,25,0.32);">
    <div style="width:100%;height:360px;background:linear-gradient(160deg,{SAGE} 0%,{SAGE_D} 100%);
                 overflow:hidden;position:relative;">
      <img src="{photo}" style="position:absolute;bottom:0;left:50%;transform:translateX(-50%);
            height:400px;object-fit:contain;">
    </div>
    <div style="font-family:'DM Sans';font-weight:700;font-style:italic;font-size:24px;color:{INK};
                 text-align:center;margin-top:16px;">week one. terrified. hired anyway.</div>
  </div>
  <!-- washi tape -->
  <div style="position:absolute;top:-18px;left:40px;width:150px;height:44px;background:{TAPE};
               transform:rotate(-6deg);"></div>
  <div style="position:absolute;top:-14px;right:34px;width:120px;height:40px;background:{TAPE_SAGE};
               transform:rotate(5deg);"></div>
</div>

<!-- doodles -->
<div style="position:absolute;top:214px;right:404px;z-index:16;">{HEART(TERRA)}</div>
<div style="position:absolute;top:640px;right:410px;z-index:16;transform:rotate(-10deg);">{STAR(MUSTARD)}</div>
<div style="position:absolute;top:470px;right:400px;z-index:16;">{ARROW(SAGE_D)}</div>

<!-- Body: the facts, left column -->
<div style="position:absolute;top:262px;left:78px;width:560px;z-index:12;">
  <div style="font-family:'DM Sans';font-weight:700;font-style:italic;font-size:27px;color:{SAGE_D};
               margin-bottom:14px;">a few things worth writing down:</div>
  {fact_rows}
</div>

<!-- handwritten note bottom-left -->
<div style="position:absolute;bottom:150px;left:78px;width:560px;z-index:12;
             font-family:'DM Sans';font-weight:700;font-style:italic;font-size:29px;color:{TERRA_D};
             line-height:1.4;">
  the feeling that you're behind is not evidence that you are. it's just new.
</div>

<!-- CTA + coffee ring -->
<div style="position:absolute;bottom:52px;left:78px;z-index:20;display:flex;align-items:center;gap:20px;">
  <div style="background:{INK};color:{PAPER};padding:14px 26px;border-radius:6px;
               font-family:Inter;font-weight:700;font-size:21px;transform:rotate(-1deg);
               box-shadow:0 6px 14px rgba(0,0,0,0.25);">Find roles at internwise.co.uk &rarr;</div>
  <div style="font-family:'DM Sans';font-weight:400;font-size:16px;color:{INK_SOFT};">
    Source: Journal of Behavioral Science, 2025
  </div>
</div>
<div style="position:absolute;bottom:120px;right:120px;width:120px;height:120px;border-radius:50%;
             border:11px solid rgba(150,95,45,0.12);z-index:2;"></div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Imposter Syndrome (Week 9, Day 2)...")
    _load_logos()
    used = get_used_hashes()
    photo = get_cutout_unique(
        "young professional smiling warm portrait studio white background",
        orientation="portrait", extra_exclude=used
    )
    h = os.path.basename(photo).replace("_nobg.png", "")
    _statcard(os.path.join(campaign_dir, "statcard_imposter.png"), photo)
    register_used_hashes([h], "week9/d2-imposter", "week9")
    register_design("warm_journal_scrapbook_polaroid", "week9/d2-imposter", "week9")
    print("Done - imposter syndrome complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week9/d2-imposter")
