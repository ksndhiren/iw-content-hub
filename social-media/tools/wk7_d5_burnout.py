"""
Internwise - Job Search Burnout (Week 7, Day 5)
Trendy: Chartreuse+navy bold combo, big italic display, handwritten annotations,
softer empathetic tone. 7 slides. Accent: LIME + DEEP_BLUE. No aggressive stickers.
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

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"
GRAIN_DARK = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(0,0,0,0.06) 1px,transparent 1px);background-size:3px 3px;}"

# Hand-drawn circle scribble SVG (highlight/underline)
UNDERLINE_SCRIBBLE = """<svg width="240" height="24" viewBox="0 0 240 24" xmlns="http://www.w3.org/2000/svg">
  <path d="M4,14 Q60,4 120,12 T232,10" stroke="{color}" stroke-width="5" fill="none" stroke-linecap="round"/>
</svg>"""

# Hand-drawn circle around text
CIRCLE_SCRIBBLE = """<svg width="340" height="120" viewBox="0 0 340 120" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="170" cy="60" rx="160" ry="50" stroke="{color}" stroke-width="5" fill="none" stroke-dasharray="0" transform="rotate(-2 170 60)"/>
</svg>"""

def _num_badge(n, bg=LIME, fg=DARK_NAVY):
    return f'<div style="position:absolute;top:44px;left:44px;width:54px;height:54px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};border:3px solid {DARK_NAVY};box-shadow:3px 3px 0 {DARK_NAVY};z-index:25;">{n}</div>'

def _kicker(text, color=LIME):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">{text}</div>'


# ─── Slide 1: Hook — Big italic, empathetic ─────────────────────────────────
def _slide1(out):
    f = _fonts()
    underline = UNDERLINE_SCRIBBLE.replace("{color}", LIME)
    circle = CIRCLE_SCRIBBLE.replace("{color}", LIME)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
<img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:44px;left:44px;height:62px;z-index:25;">

<!-- Handwritten note top-right -->
<div style="position:absolute;top:70px;right:60px;font-family:'DM Sans';font-weight:500;
             font-style:italic;font-size:24px;color:{LIME};transform:rotate(3deg);z-index:20;
             max-width:280px;text-align:right;">
  a real thing<br>we don't talk<br>about enough ↓
</div>

<!-- Main headline -->
<div style="position:absolute;top:220px;left:50px;right:50px;z-index:10;">
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:140px;line-height:0.9;
               color:white;letter-spacing:-6px;word-break:keep-all;hyphens:none;">
    50 no's.
  </div>
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:140px;line-height:0.9;
               color:{LIME};letter-spacing:-6px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Still nothing.
  </div>
  <!-- Scribble underline under "Still nothing." -->
  <div style="margin-top:-14px;margin-left:80px;">{underline}</div>
</div>

<!-- Subtext -->
<div style="position:absolute;bottom:180px;left:50px;right:50px;z-index:10;">
  <div style="font-family:'DM Sans';font-weight:500;font-size:32px;color:white;line-height:1.35;
               max-width:820px;">
    Job search burnout is real. And you're not lazy for feeling it.
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-style:italic;font-size:24px;
               color:{LIME};margin-top:14px;">Here's how to keep going without breaking.</div>
</div>

<div style="position:absolute;bottom:44px;right:60px;font-family:'DM Sans';
             font-weight:500;font-size:20px;color:rgba(255,255,255,0.6);z-index:20;">SWIPE →</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 2: The Reality ────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE REALITY", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    You're not <em style="color:{LIME};font-style:italic;">imagining</em> this.
  </div>
</div>
<div style="flex:1;margin-top:38px;display:grid;grid-template-columns:1fr 1fr;gap:22px;position:relative;z-index:5;">
  <div style="background:rgba(212,255,61,0.10);border:3px solid {LIME};border-radius:20px;padding:30px 26px;box-shadow:5px 5px 0 {LIME};">
    <div style="font-family:Inter;font-weight:700;font-size:76px;color:{LIME};letter-spacing:-3px;line-height:1;">63%</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:white;margin-top:16px;line-height:1.35;">
      of graduate job seekers report anxiety and burnout during their search.
    </div>
  </div>
  <div style="background:rgba(212,255,61,0.10);border:3px solid {LIME};border-radius:20px;padding:30px 26px;box-shadow:5px 5px 0 {LIME};">
    <div style="font-family:Inter;font-weight:700;font-size:76px;color:{LIME};letter-spacing:-3px;line-height:1;">140</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:white;margin-top:16px;line-height:1.35;">
      average applications per grad vacancy in 2026. The odds aren't personal.
    </div>
  </div>
  <div style="background:rgba(212,255,61,0.10);border:3px solid {LIME};border-radius:20px;padding:30px 26px;box-shadow:5px 5px 0 {LIME};">
    <div style="font-family:Inter;font-weight:700;font-size:76px;color:{LIME};letter-spacing:-3px;line-height:1;">6mo</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:white;margin-top:16px;line-height:1.35;">
      is now the average grad search length. Longer than any degree module.
    </div>
  </div>
  <div style="background:rgba(212,255,61,0.10);border:3px solid {LIME};border-radius:20px;padding:30px 26px;box-shadow:5px 5px 0 {LIME};">
    <div style="font-family:Inter;font-weight:700;font-size:76px;color:{LIME};letter-spacing:-3px;line-height:1;">2%</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:white;margin-top:16px;line-height:1.35;">
      average callback rate on cold applications. You'll hear no more than yes.
    </div>
  </div>
</div>
<div style="flex-shrink:0;margin-top:20px;font-family:'DM Sans';font-weight:400;font-size:20px;
             color:rgba(255,255,255,0.5);position:relative;z-index:5;text-align:right;">Sources: High Fliers 2026, Prospects Grad Wellbeing Report</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 3: Signs You're Burning Out ───────────────────────────────────────
def _slide3(out):
    f = _fonts()
    signs = [
        "Refreshing your inbox knowing nothing new is there",
        "Feeling worse after applying, not better",
        "Comparing your progress to LinkedIn strangers daily",
        "Rewriting your CV for the fifth time this week",
        "Snapping at people who ask 'any luck yet?'",
    ]
    rows = ""
    for s in signs:
        rows += f"""<div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;
             border-bottom:2px dashed rgba(255,255,255,0.15);">
  <div style="width:12px;height:12px;background:{LIME};border-radius:50%;margin-top:14px;flex-shrink:0;"></div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:white;line-height:1.35;">{s}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(3)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE SIGNS", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    You're <em style="color:{LIME};font-style:italic;">running on empty</em> if...
  </div>
</div>
<div style="flex:1;margin-top:24px;position:relative;z-index:5;">{rows}</div>
<div style="font-family:'DM Sans';font-weight:500;font-style:italic;font-size:22px;
             color:{LIME};text-align:center;margin-top:12px;position:relative;z-index:5;">
  If any 3 of these are true, this week isn't for applying. It's for resting.
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 4: The Rules That Actually Help ───────────────────────────────────
def _slide4(out):
    f = _fonts()
    rules = [
        ("Cap it at 5", "applications per day. Quality beats quantity every time."),
        ("Block off 2 mornings", "a week for search. Zero on the other days. Reclaim the rest."),
        ("Move your body", "before you open your laptop. 20 minutes. Non-negotiable."),
        ("Log 3 wins", "at the end of every session. Even 'sent a follow-up' counts."),
    ]
    rows = ""
    for i, (bold, rest) in enumerate(rules):
        rows += f"""<div style="display:flex;align-items:center;gap:20px;background:rgba(212,255,61,0.08);
             border:3px solid {LIME};border-radius:16px;padding:20px 26px;box-shadow:4px 4px 0 {LIME};">
  <div style="width:44px;height:44px;background:{LIME};color:{DARK_NAVY};border:3px solid {DARK_NAVY};
               border-radius:14px;box-shadow:3px 3px 0 {DARK_NAVY};display:flex;align-items:center;
               justify-content:center;font-family:Inter;font-weight:700;font-size:22px;flex-shrink:0;">{i+1}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:white;line-height:1.35;">
    <span style="font-family:Inter;font-weight:700;color:{LIME};">{bold}</span> {rest}
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE RULES", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    New rules for the <em style="color:{LIME};font-style:italic;">long haul.</em>
  </div>
</div>
<div style="flex:1;margin-top:34px;display:flex;flex-direction:column;gap:18px;position:relative;z-index:5;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 5: What to Do on a Bad Day ────────────────────────────────────────
def _slide5(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(5)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE BAD DAY PLAN", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    When you can't <em style="color:{LIME};font-style:italic;">apply to one more thing.</em>
  </div>
</div>
<div style="flex:1;margin-top:32px;display:flex;flex-direction:column;gap:18px;position:relative;z-index:5;">
  <div style="background:{LIME};color:{DARK_NAVY};border:3px solid {DARK_NAVY};border-radius:18px;
               padding:24px 30px;box-shadow:5px 5px 0 {DARK_NAVY};">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{DARK_NAVY};">Close the laptop.</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:{DARK_NAVY};margin-top:6px;line-height:1.4;">
      Not for an hour. For the day. The applications will still be there tomorrow.
    </div>
  </div>
  <div style="background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.25);border-radius:18px;
               padding:24px 30px;">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;">Do something you're already good at.</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:rgba(255,255,255,0.75);margin-top:6px;line-height:1.4;">
      Cook the meal. Play the game. Text the friend. Remind yourself you have skills that work.
    </div>
  </div>
  <div style="background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.25);border-radius:18px;
               padding:24px 30px;">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;">Talk to one human who isn't job hunting.</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:rgba(255,255,255,0.75);margin-top:6px;line-height:1.4;">
      A parent, a friend, a coach. Get out of the job-search echo chamber for one conversation.
    </div>
  </div>
  <div style="background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.25);border-radius:18px;
               padding:24px 30px;">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;">If it's been weeks, get support.</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:rgba(255,255,255,0.75);margin-top:6px;line-height:1.4;">
      Your uni careers service. A GP. Samaritans on 116 123. Not overkill. Common and effective.
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 6: Reframe ────────────────────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    circle = CIRCLE_SCRIBBLE.replace("{color}", LIME)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE REFRAME", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    A rejection is <em style="color:{LIME};font-style:italic;">information.</em>
  </div>
</div>
<div style="flex:1;margin-top:38px;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:5;">
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:46px;color:rgba(255,255,255,0.5);
               text-decoration:line-through;line-height:1.2;margin-bottom:20px;">
    "I'm not good enough."
  </div>
  <div style="position:relative;display:inline-block;width:fit-content;">
    <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:62px;color:{LIME};
                 line-height:1.1;letter-spacing:-2px;padding:20px 40px;">
      "Not this one. Next."
    </div>
    <div style="position:absolute;top:14px;left:0;">{circle}</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.8);
               margin-top:44px;max-width:820px;line-height:1.4;">
    Every no narrows the search. Every no is a data point about what to say differently next time. It's never the whole story about you.
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    underline = UNDERLINE_SCRIBBLE.replace("{color}", LIME)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{LIME};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:44px;left:44px;height:62px;z-index:25;">
<div style="position:absolute;top:70px;right:60px;font-family:'DM Sans';font-weight:500;font-style:italic;
             font-size:22px;color:{DARK_NAVY};transform:rotate(3deg);max-width:280px;text-align:right;">
  save this for the<br>day you need it ↓
</div>

<div style="padding-top:150px;position:relative;z-index:10;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{DARK_NAVY};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:16px;opacity:0.7;">A REMINDER</div>
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:100px;line-height:0.95;
               color:{DARK_NAVY};letter-spacing:-4px;word-break:keep-all;hyphens:none;">
    You are <em>not</em> your<br>job search.
  </div>
  <div style="margin-top:-8px;margin-left:14px;">{underline}</div>
</div>

<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;position:relative;z-index:10;">
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:{DARK_NAVY};line-height:1.4;
               max-width:820px;">
    The job will come. It comes for everyone eventually. Keep going, kindly. When you're ready, we'll be here.
  </div>
  <div style="margin-top:32px;display:inline-flex;align-items:center;gap:12px;background:{DARK_NAVY};
               color:{LIME};padding:18px 30px;border-radius:60px;font-family:Inter;
               font-weight:700;font-size:24px;border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 rgba(0,0,0,0.2);
               width:fit-content;">
    Find your next role at internwise.co.uk &#8594;
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Job Search Burnout (Week 7, Day 5)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("chartreuse_navy_italic_annotated", "week7/d5-burnout", "week7")
    print("Done - burnout complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week7/d5-burnout")
