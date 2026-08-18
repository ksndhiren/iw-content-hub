"""
Internwise - Reading Job Specs Like a Recruiter (Week 8, Day 2)
Design language: REDLINED DOCUMENT / EDITORIAL MARKUP. A real job spec on paper
with highlighter swipes, red pen circles, margin annotations in handwriting-italic,
paper drop-shadow, coffee-ring stain. Single statcard.
Accent: RED_PEN + HIGHLIGHT_YELLOW on PAPER.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; DEEP_BLUE = "#264D7E"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; OFF_WHITE = "#FAF5EC"

DESK       = "#3A4A5C"   # desk surface behind the paper
PAPER      = "#FFFDF7"   # paper white
RED_PEN    = "#E5342A"   # annotation red
HL_YELLOW  = "#FFF27A"   # highlighter
HL_GREEN   = "#B8F5C0"   # second highlighter
INK        = "#1A1A1A"   # document body ink

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

# Hand-drawn red circle around text
def _red_circle(w, h, rot=-2):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'style="transform:rotate({rot}deg);">'
            f'<ellipse cx="{w/2}" cy="{h/2}" rx="{w/2-6}" ry="{h/2-4}" '
            f'stroke="{RED_PEN}" stroke-width="3.5" fill="none" opacity="0.9"/></svg>')

# Hand-drawn red arrow pointing left (from margin note back to the spec line)
ARROW_LEFT_SM = f"""<svg width="44" height="28" viewBox="0 0 44 28" xmlns="http://www.w3.org/2000/svg">
  <path d="M42,15 Q28,7 16,14 T3,14" stroke="{RED_PEN}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
  <path d="M11,8 L2,14 L12,20" stroke="{RED_PEN}" stroke-width="2.6" fill="none"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

def _hl(text, color=HL_YELLOW):
    """Highlighter swipe behind text."""
    return (f'<span style="background:linear-gradient(180deg,transparent 8%,{color} 8%,'
            f'{color} 88%,transparent 88%);padding:0 3px;">{text}</span>')

def _strike(text):
    return f'<span style="text-decoration:line-through;text-decoration-color:{RED_PEN};text-decoration-thickness:2.5px;opacity:0.55;">{text}</span>'

def _margin_note(text, top, side="right", rot=-3):
    pos = "right:-8px;" if side == "right" else "left:-8px;"
    return f"""<div style="position:absolute;{pos}top:{top}px;width:230px;
             font-family:'DM Sans';font-weight:700;font-style:italic;font-size:22px;
             color:{RED_PEN};line-height:1.25;transform:rotate({rot}deg);z-index:30;
             text-align:{'left' if side=='right' else 'right'};">{text}</div>"""


def _statcard(out):
    f = _fonts()

    # (spec_line_html, margin_note_html, note_rotation)
    reqs = [
        (f'{_hl("2+ years", HL_YELLOW)} experience in a data role',
         'means "we&#39;d like it".<br>internships count.<br><u>apply anyway.</u>', -2),
        (f'Advanced {_hl("SQL", HL_GREEN)} and {_hl("Python", HL_GREEN)}',
         'the <u>REAL</u> filter.<br>everything else<br>is negotiable.', 2),
        (f'{_strike("Experience with Looker, Tableau,")}<br>{_strike("PowerBI, dbt, Airflow")}',
         'nobody has all five.<br>name the two<br>you actually know.', -2),
        (f'{_hl("Stakeholder communication", HL_GREEN)} skills',
         'buried. but it&#39;s why<br>people fail at<br>final stage.', 2),
        (f'{_strike("Degree in a quantitative discipline")}',
         'rarely enforced<br>if you show<br>the work.', -1),
    ]

    # Each row = bullet + spec text (left) and the red note (right), so they always align.
    rows_html = ""
    for text, note, rot in reqs:
        rows_html += f"""<div style="display:flex;align-items:flex-start;gap:18px;margin-bottom:20px;">
  <div style="flex:1;display:flex;gap:14px;align-items:flex-start;">
    <div style="width:8px;height:8px;border-radius:50%;background:{INK};margin-top:13px;
                 flex-shrink:0;opacity:0.7;"></div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:{INK};line-height:1.45;">{text}</div>
  </div>
  <div style="width:44px;flex-shrink:0;padding-top:6px;">{ARROW_LEFT_SM}</div>
  <div style="width:250px;flex-shrink:0;font-family:'DM Sans';font-weight:700;font-style:italic;
               font-size:21px;color:{RED_PEN};line-height:1.25;transform:rotate({rot}deg);">{note}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DESK};
      background-image:radial-gradient(rgba(0,0,0,0.18) 1px,transparent 1px);background-size:5px 5px;}}
.c{{width:1080px;height:1080px;position:relative;padding:34px 40px;display:flex;flex-direction:column;}}
u{{text-decoration-color:{RED_PEN};text-decoration-thickness:2px;}}
</style></head><body><div class="c">

<!-- Header on the desk -->
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;
             margin-bottom:16px;position:relative;z-index:40;">
  <div>
    <div style="font-family:'DM Sans';font-weight:700;font-size:19px;color:{HL_YELLOW};
                 text-transform:uppercase;letter-spacing:3px;">Read it like a recruiter</div>
    <div style="font-family:Inter;font-weight:700;font-size:48px;color:white;letter-spacing:-2px;
                 line-height:1.05;margin-top:4px;word-break:keep-all;hyphens:none;">
      What the job spec <span style="color:{HL_YELLOW};font-style:italic;">actually means.</span>
    </div>
  </div>
  <div style="background:{RED_PEN};color:white;padding:11px 20px;border-radius:4px;
               font-family:Inter;font-weight:700;font-size:19px;letter-spacing:2px;
               text-transform:uppercase;transform:rotate(3deg);flex-shrink:0;
               box-shadow:3px 3px 0 rgba(0,0,0,0.25);">Marked up</div>
</div>

<!-- The paper -->
<div style="flex:1;background:{PAPER};border-radius:3px;padding:32px 34px 26px 34px;
             position:relative;box-shadow:0 18px 44px rgba(0,0,0,0.42);
             transform:rotate(-0.6deg);display:flex;flex-direction:column;">

  <!-- coffee ring stain -->
  <div style="position:absolute;bottom:104px;right:56px;width:104px;height:104px;border-radius:50%;
               border:10px solid rgba(140,90,40,0.11);z-index:1;"></div>

  <!-- Document header -->
  <div style="border-bottom:2.5px solid {INK};padding-bottom:14px;margin-bottom:20px;
               position:relative;z-index:5;flex-shrink:0;">
    <div style="font-family:Inter;font-weight:700;font-size:38px;color:{INK};letter-spacing:-1px;">
      Graduate Data Analyst
    </div>
    <div style="position:relative;display:inline-block;margin-top:5px;">
      <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:#555;">
        London (hybrid) &middot; &pound;32,000 - &pound;36,000 &middot; Closing 31 July
      </div>
      <div style="position:absolute;top:-9px;left:-12px;z-index:20;pointer-events:none;">{_red_circle(556, 46, rot=-0.8)}</div>
    </div>
  </div>

  <div style="font-family:Inter;font-weight:700;font-size:24px;color:{INK};
               text-transform:uppercase;letter-spacing:2px;margin-bottom:18px;
               position:relative;z-index:5;flex-shrink:0;">
    What we're looking for
  </div>

  <div style="position:relative;z-index:5;">{rows_html}</div>

  <div style="flex:1;"></div>

  <!-- Bottom-of-paper verdict note -->
  <div style="border-top:2px dashed rgba(0,0,0,0.18);padding-top:18px;position:relative;z-index:5;
               flex-shrink:0;display:flex;align-items:center;gap:18px;">
    <div style="font-family:'DM Sans';font-weight:700;font-style:italic;font-size:26px;
                 color:{RED_PEN};line-height:1.3;transform:rotate(-1deg);">
      verdict: 2 hard requirements, not 5.<br>you're closer than the spec makes you feel.
    </div>
  </div>
</div>

<!-- Bottom bar on the desk -->
<div style="flex-shrink:0;margin-top:18px;display:flex;justify-content:space-between;
             align-items:center;position:relative;z-index:40;">
  <div style="background:{PAPER};color:{DARK_NAVY};padding:13px 24px;border-radius:4px;
               font-family:Inter;font-weight:700;font-size:21px;
               box-shadow:3px 3px 0 rgba(0,0,0,0.3);transform:rotate(-1deg);">
    Find roles at internwise.co.uk &rarr;
  </div>
  <img src="data:image/png;base64,{LOGO_C}" style="height:46px;background:{PAPER};
        padding:7px 12px;border-radius:4px;box-shadow:3px 3px 0 rgba(0,0,0,0.3);">
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Job Specs (Week 8, Day 2)...")
    _load_logos()
    _statcard(os.path.join(campaign_dir, "statcard_jobspecs.png"))
    register_design("redlined_document_editorial_markup", "week8/d2-jobspecs", "week8")
    print("Done - job specs complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week8/d2-jobspecs")
