"""
Internwise - Company Research Beyond Glassdoor (Week 8, Day 5)
Design language: DETECTIVE CORKBOARD / RED STRING INVESTIGATION. Cork texture,
pinned index cards at angles, red thread connecting evidence, push pins,
polaroid-style clue cards, rubber-stamp verdicts.
7 slides. Accent: RED_STRING + PIN_RED on CORK.
"""
import os, base64, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; DEEP_BLUE = "#264D7E"; OFF_WHITE = "#FAF5EC"

CORK       = "#B98A52"   # corkboard base
CORK_DARK  = "#9A6F3E"
CARD       = "#FDFBF3"   # index card
CARD_LINED = "#F2EEE0"
RED_STRING = "#D42D22"
PIN_RED    = "#E5342A"
PIN_BLUE   = "#2E6BE8"
PIN_YELLOW = "#F5B02E"
INK        = "#22303C"
STAMP      = "#C0392B"

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

# Cork texture — layered speckle
CORK_BG = (f"background:{CORK};"
           "background-image:"
           "radial-gradient(rgba(90,60,25,0.30) 1.4px,transparent 1.4px),"
           "radial-gradient(rgba(140,100,55,0.32) 1.1px,transparent 1.1px),"
           "radial-gradient(rgba(60,40,15,0.16) 2.2px,transparent 2.2px);"
           "background-size:9px 9px, 14px 14px, 27px 27px;"
           "background-position:0 0, 5px 7px, 13px 3px;")

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;{CORK_BG}}}
.c{{width:1080px;height:1080px;position:relative;padding:34px 40px;display:flex;flex-direction:column;}}
.vig{{position:absolute;inset:0;z-index:1;pointer-events:none;
      background:radial-gradient(ellipse at 50% 42%,transparent 42%,rgba(40,25,8,0.42) 100%);}}
"""

def _pin(color=PIN_RED, size=22):
    """Push pin with highlight + shadow."""
    return f"""<div style="width:{size}px;height:{size}px;border-radius:50%;
             background:radial-gradient(circle at 33% 30%,#fff8 0%,{color} 46%,{color} 100%);
             box-shadow:0 3px 5px rgba(0,0,0,0.5), inset 0 -2px 3px rgba(0,0,0,0.3);
             position:relative;z-index:30;flex-shrink:0;"></div>"""

def _card(inner, rot=0, w=None, pin_color=PIN_RED, lined=False, extra=""):
    """Pinned index card."""
    width = f"width:{w}px;" if w else ""
    bg = CARD_LINED if lined else CARD
    lines = ("background-image:repeating-linear-gradient(180deg,transparent 0px,transparent 33px,"
             "rgba(60,90,130,0.16) 33px,rgba(60,90,130,0.16) 34px);") if lined else ""
    return f"""<div style="{width}background:{bg};{lines}border-radius:2px;padding:22px 24px;
             transform:rotate({rot}deg);box-shadow:0 8px 22px rgba(0,0,0,0.45);
             position:relative;{extra}">
  <div style="position:absolute;top:-9px;left:50%;transform:translateX(-50%);">{_pin(pin_color)}</div>
  {inner}
</div>"""

def _stamp(text, rot=-11, color=STAMP):
    return f"""<div style="display:inline-block;border:4px solid {color};color:{color};
             padding:7px 16px;border-radius:5px;font-family:Inter;font-weight:700;
             font-size:22px;letter-spacing:3px;text-transform:uppercase;
             transform:rotate({rot}deg);opacity:0.82;">{text}</div>"""

def _thread(x1, y1, x2, y2, sag=26):
    """Red string between two points with gravity sag."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + sag
    return (f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" stroke="{RED_STRING}" '
            f'stroke-width="2.6" fill="none" opacity="0.9"/>')

def _header(kicker, headline_html, stamp_text=None):
    stamp_html = f'<div style="flex-shrink:0;">{_stamp(stamp_text, 4)}</div>' if stamp_text else ""
    return f"""<div style="display:flex;justify-content:space-between;align-items:flex-start;
             flex-shrink:0;position:relative;z-index:25;gap:20px;">
  <div>
    <div style="font-family:'DM Sans';font-weight:700;font-size:19px;color:#FFEBC4;
                 text-transform:uppercase;letter-spacing:3px;
                 text-shadow:0 2px 4px rgba(0,0,0,0.6);">{kicker}</div>
    <div style="font-family:Inter;font-weight:700;font-size:52px;color:white;letter-spacing:-2px;
                 line-height:1.02;margin-top:6px;word-break:keep-all;hyphens:none;
                 text-shadow:0 3px 8px rgba(0,0,0,0.6);">{headline_html}</div>
  </div>
  {stamp_html}
</div>"""


# ─── Slide 1: Hook — the board with string ────────────────────────────────
def _slide1(out):
    f = _fonts()
    c1 = _card(f"""
<div style="font-family:'DM Sans';font-weight:700;font-size:17px;color:#8B99A8;
             letter-spacing:2px;text-transform:uppercase;margin-bottom:7px;">Exhibit A</div>
<div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};line-height:1.15;">
  Glassdoor rating</div>
<div style="font-family:'DM Sans';font-weight:500;font-style:italic;font-size:21px;
             color:{STAMP};margin-top:8px;">gamed. mostly leavers.</div>""",
        rot=-4, w=270, pin_color=PIN_RED)

    c2 = _card(f"""
<div style="font-family:'DM Sans';font-weight:700;font-size:17px;color:#8B99A8;
             letter-spacing:2px;text-transform:uppercase;margin-bottom:7px;">Exhibit B</div>
<div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};line-height:1.15;">
  The careers page</div>
<div style="font-family:'DM Sans';font-weight:500;font-style:italic;font-size:21px;
             color:{STAMP};margin-top:8px;">marketing. written by an agency.</div>""",
        rot=3, w=270, pin_color=PIN_BLUE)

    c3 = _card(f"""
<div style="font-family:'DM Sans';font-weight:700;font-size:17px;color:#8B99A8;
             letter-spacing:2px;text-transform:uppercase;margin-bottom:7px;">Exhibit C</div>
<div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};line-height:1.15;">
  Their last 6 job ads</div>
<div style="font-family:'DM Sans';font-weight:500;font-style:italic;font-size:21px;
             color:#1E7A3E;margin-top:8px;">the actual truth. free.</div>""",
        rot=-2, w=270, pin_color=PIN_YELLOW)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="vig"></div>

<!-- red string: swags across the three exhibit pins, then runs down to the verdict box.
     Pin x-centres match the space-between layout below (175 / 540 / 905). -->
<svg style="position:absolute;inset:0;width:1080px;height:1080px;z-index:12;pointer-events:none;"
     viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  {_thread(175, 286, 540, 286, 40)}
  {_thread(540, 286, 905, 286, 40)}
  {_thread(905, 286, 830, 664, 30)}
</svg>

{_header("Case file / company research", 'They are <span style="color:#FFD98A;font-style:italic;">telling you</span> everything.', "Classified")}

<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px;
             margin-top:34px;flex-shrink:0;position:relative;z-index:20;">
  {c1}{c2}{c3}
</div>

<div style="flex:1;"></div>

<div style="flex-shrink:0;position:relative;z-index:20;display:flex;align-items:flex-end;gap:24px;">
  <div style="background:rgba(12,20,28,0.86);border-radius:6px;padding:30px 34px;
               box-shadow:0 10px 30px rgba(0,0,0,0.5);flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:66px;line-height:0.95;color:white;
                 letter-spacing:-3px;word-break:keep-all;hyphens:none;">
      Stop reading<br>the <span style="color:#FF8A7A;font-style:italic;">reviews.</span>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:#C9D6E2;
                 margin-top:16px;line-height:1.35;">
      Four public sources tell you more in 20 minutes than Glassdoor tells you in an hour.
    </div>
  </div>
  <div style="width:296px;flex-shrink:0;">
    {_card(f'''
<div style="font-family:'DM Sans';font-weight:700;font-size:17px;color:#8B99A8;
             letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">The four sources</div>
<div style="font-family:'DM Sans';font-weight:600;font-size:23px;color:{INK};line-height:1.7;
             white-space:nowrap;">
  A &nbsp;their last 6 job ads<br>
  B &nbsp;LinkedIn tenure<br>
  C &nbsp;Companies House<br>
  D &nbsp;their eng blog
</div>
<div style="border-top:2px dashed rgba(0,0,0,0.16);margin-top:12px;padding-top:10px;
             font-family:'DM Sans';font-weight:700;font-style:italic;font-size:20px;color:{STAMP};">
  all free. all public.
</div>''', rot=2, pin_color=PIN_BLUE, lined=True)}
  </div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;
             position:relative;z-index:25;margin-top:14px;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:44px;background:{CARD};
        padding:7px 11px;border-radius:3px;box-shadow:0 5px 14px rgba(0,0,0,0.45);">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:#FFEBC4;
               text-shadow:0 2px 4px rgba(0,0,0,0.6);">SWIPE &rarr;</div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 2: The Data ────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("3.4", "average Glassdoor rating across all UK employers. It tells you almost nothing.", PIN_RED),
        ("71%", "of reviews are written by people on their way out or just after leaving.", PIN_BLUE),
        ("20", "minutes on four other sources gets you a genuinely useful picture.", "#1E7A3E"),
    ]
    cards = ""
    for i, (val, label, color) in enumerate(stats):
        rot = [-3, 2, -2][i]
        inner = f"""
<div style="font-family:Inter;font-weight:700;font-size:78px;color:{color};
             letter-spacing:-3px;line-height:1;">{val}</div>
<div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{INK};
             margin-top:14px;line-height:1.35;">{label}</div>"""
        cards += f'<div style="flex:1;">{_card(inner, rot=rot, pin_color=color, extra="height:100%;")}</div>'
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="vig"></div>
{_header("The evidence", 'Reviews are the <span style="color:#FFD98A;font-style:italic;">worst source.</span>')}
<div style="flex:1;display:flex;gap:24px;align-items:stretch;margin:40px 0 20px 0;
             position:relative;z-index:20;">{cards}</div>
<div style="flex-shrink:0;font-family:'DM Sans';font-weight:400;font-size:19px;color:#FFEBC4;
             text-align:right;text-shadow:0 2px 4px rgba(0,0,0,0.6);position:relative;z-index:25;">
  Sources: Glassdoor UK aggregate 2026, HBR Employer Review Bias Study 2025
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slides 3-6: The four sources ─────────────────────────────────────────
def _source_slide(out, n, exhibit, source, tagline, what, how, tell, pin_color):
    f = _fonts()
    # Card carries the exhibit detail; the page headline carries the tagline, so they
    # never repeat the same words.
    card_inner = f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:17px;color:#8B99A8;
               letter-spacing:2px;text-transform:uppercase;">Exhibit {exhibit}</div>
  <div style="font-family:'DM Sans';font-weight:700;font-size:17px;color:#8B99A8;
               letter-spacing:2px;">0{n-2} / 04</div>
</div>
<div style="font-family:Inter;font-weight:700;font-size:36px;color:{INK};line-height:1.05;
             letter-spacing:-1.5px;word-break:keep-all;hyphens:none;">{source}</div>
<div style="border-top:2px dashed rgba(0,0,0,0.16);margin:16px 0;"></div>
<div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{INK};line-height:1.4;">{what}</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="vig"></div>

<!-- string runs from the pinned exhibit card across to the "how to read it" panel -->
<svg style="position:absolute;inset:0;width:1080px;height:1080px;z-index:12;pointer-events:none;"
     viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  {_thread(232, 372, 620, 430, 26)}
</svg>

{_header(f"Source 0{n-2} / 04 &middot; exhibit {exhibit}",
         f'<span style="color:#FFD98A;font-style:italic;">{tagline.capitalize()}</span>')}

<div style="flex:1;display:flex;align-items:center;gap:30px;position:relative;z-index:20;
             padding:14px 0;">
  <div style="width:394px;flex-shrink:0;">
    {_card(card_inner, rot=-3, pin_color=pin_color, lined=True)}
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:18px;">
    <div style="background:rgba(12,20,28,0.84);border-radius:6px;padding:26px 28px;
                 box-shadow:0 8px 24px rgba(0,0,0,0.45);">
      <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{pin_color};
                   letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">How to read it</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#DCE6F0;line-height:1.4;">{how}</div>
    </div>
    <div style="background:rgba(12,20,28,0.84);border-radius:6px;padding:26px 28px;
                 box-shadow:0 8px 24px rgba(0,0,0,0.45);">
      <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{pin_color};
                   letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">The tell</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#DCE6F0;line-height:1.4;">{tell}</div>
    </div>
  </div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:flex-end;position:relative;z-index:25;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:38px;background:{CARD};
        padding:6px 9px;border-radius:3px;opacity:0.75;box-shadow:0 4px 12px rgba(0,0,0,0.4);">
</div>
</div></body></html>"""
    _render(html, out)


def _slide3(out): _source_slide(out, 3, "A",
    "Their last 6 job ads", "the org chart, for free",
    "Every open role going back 6 months. Free on their careers page and on LinkedIn.",
    "Which teams are hiring tells you where the money and the momentum are. Three ops roles and no engineers means the product is done being built.",
    "The same role posted twice in 6 months means someone left. Posted three times means a manager problem.",
    PIN_YELLOW)

def _slide4(out): _source_slide(out, 4, "B",
    "LinkedIn tenure math", "who stays, who runs",
    "Filter their people by your target team. Then just read the start dates.",
    "If most of the team joined in the last 12 months, either they're growing fast or the last team left. The company's founding date tells you which.",
    "Nobody in the team past 2 years is the loudest signal on this list. Ask about it in the interview.",
    PIN_BLUE)

def _slide5(out): _source_slide(out, 5, "C",
    "Companies House", "the numbers they can't spin",
    "Free and public. Filed accounts, director changes, and any charges against the company.",
    "Check the cash position and whether directors are churning. A grad scheme at a company that just filed a going-concern note is a risk worth knowing about.",
    "Late filings and sudden director resignations, together, are the pattern to watch. Both are timestamped.",
    PIN_RED)

def _slide6(out): _source_slide(out, 6, "D",
    "Their eng or product blog", "how they actually think",
    "Whatever they publish: engineering blog, product changelog, conference talks.",
    "Read the most recent three posts. You learn their stack, their problems, and their taste. Then reference it in your application.",
    "Nothing published in 2 years usually means no time, no culture of sharing, or nothing worth sharing. All three are worth knowing.",
    "#1E7A3E")


# ─── Slide 7: CTA — case closed ───────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    checks = [
        ("A", "Read their last 6 job ads", PIN_YELLOW),
        ("B", "Do the LinkedIn tenure math", PIN_BLUE),
        ("C", "Pull the Companies House filing", PIN_RED),
        ("D", "Read their last 3 blog posts", "#1E7A3E"),
    ]
    rows = ""
    for letter, txt, col in checks:
        rows += f"""<div style="display:flex;gap:14px;align-items:center;padding:9px 0;">
  <div style="width:30px;height:30px;border-radius:50%;background:{col};flex-shrink:0;
               display:flex;align-items:center;justify-content:center;font-family:Inter;
               font-weight:700;font-size:16px;color:white;">{letter}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:{INK};">{txt}</div>
</div>"""
    card_inner = f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:#8B99A8;
               letter-spacing:2px;text-transform:uppercase;">The 20-minute sweep</div>
  {_stamp("Case closed", -6)}
</div>
{rows}
<div style="border-top:2px dashed rgba(0,0,0,0.16);margin-top:16px;padding-top:14px;">
  <div style="font-family:'DM Sans';font-weight:500;font-style:italic;font-size:24px;color:{STAMP};">
    Then walk into the interview knowing more than the other candidates. All of it is public.
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="vig"></div>

<svg style="position:absolute;inset:0;width:1080px;height:1080px;z-index:12;pointer-events:none;"
     viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
  {_thread(150, 300, 930, 300, 22)}
</svg>

{_header("Verdict", 'Twenty minutes. <span style="color:#FFD98A;font-style:italic;">All public.</span>')}

<div style="flex:1;display:flex;align-items:center;position:relative;z-index:20;">
  <div style="width:100%;">{_card(card_inner, rot=-1, pin_color=PIN_RED, w=None)}</div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;
             position:relative;z-index:25;">
  <div style="background:{CARD};color:{DARK_NAVY};padding:16px 28px;border-radius:3px;
               font-family:Inter;font-weight:700;font-size:24px;transform:rotate(-1deg);
               box-shadow:0 8px 22px rgba(0,0,0,0.45);">
    Find roles at internwise.co.uk &rarr;
  </div>
  <img src="data:image/png;base64,{LOGO_C}" style="height:44px;background:{CARD};
        padding:7px 11px;border-radius:3px;box-shadow:0 6px 16px rgba(0,0,0,0.45);">
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Company Research (Week 8, Day 5)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("detective_corkboard_red_string", "week8/d5-research", "week8")
    print("Done - company research complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week8/d5-research")
