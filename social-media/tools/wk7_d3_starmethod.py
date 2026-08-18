"""
Internwise - STAR Method for Behavioural Interviews (Week 7, Day 3)
Trendy: Y2K starburst SVG as the literal STAR, expressive display italic type,
gradient star sticker, punchy purple+lime combo. 7 slides.
Accent: PURPLE + LIME.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import get_used_hashes, register_used_hashes, register_design, get_cutout_unique
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

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"
GRAIN_DARK = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(0,0,0,0.06) 1px,transparent 1px);background-size:3px 3px;}"

def _starburst(size, color, spikes=12):
    import math
    cx = cy = size / 2
    r_out = size / 2
    r_in = r_out * 0.55
    pts = []
    for i in range(spikes * 2):
        r = r_out if i % 2 == 0 else r_in
        a = i * math.pi / spikes - math.pi / 2
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}"><polygon points="{" ".join(pts)}" fill="{color}"/></svg>'

def _num_badge(n, bg=LIME, fg=DARK_NAVY):
    return f'<div style="position:absolute;top:44px;left:44px;width:54px;height:54px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};border:3px solid {DARK_NAVY};box-shadow:3px 3px 0 {DARK_NAVY};z-index:25;">{n}</div>'

def _kicker(text, color=LIME):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">{text}</div>'


# ─── Slide 1: Hook — Big starburst, expressive type ─────────────────────────
def _slide1(out):
    f = _fonts()
    burst_lg = _starburst(720, LIME, spikes=14)
    burst_sm = _starburst(120, HOT_PINK, spikes=10)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{PURPLE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
<!-- Big starburst behind -->
<div style="position:absolute;top:180px;right:-140px;transform:rotate(15deg);z-index:3;
             filter:drop-shadow(8px 8px 0 {DARK_NAVY});">{burst_lg}</div>
<!-- Small starburst top-left -->
<div style="position:absolute;top:170px;left:44px;transform:rotate(-12deg);z-index:6;
             filter:drop-shadow(4px 4px 0 {DARK_NAVY});">{burst_sm}</div>

<img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:44px;left:44px;height:62px;z-index:25;">
<!-- Sticker top-right -->
<div style="position:absolute;top:52px;right:60px;background:{DARK_NAVY};color:{LIME};
             padding:14px 22px;border:3px solid {DARK_NAVY};border-radius:14px;
             font-family:Inter;font-weight:700;font-size:22px;letter-spacing:2px;text-transform:uppercase;
             transform:rotate(4deg);z-index:35;box-shadow:5px 5px 0 {LIME};">Interview framework</div>

<!-- Big STAR word ON the starburst -->
<div style="position:absolute;top:320px;right:60px;z-index:12;transform:rotate(-4deg);">
  <div style="font-family:Inter;font-weight:700;font-size:200px;color:{DARK_NAVY};
               letter-spacing:-10px;line-height:0.9;">STAR.</div>
</div>

<!-- Bottom text -->
<div style="position:absolute;bottom:120px;left:50px;right:50px;z-index:20;">
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:78px;
               color:white;line-height:0.95;letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    The answer<br>structure <span style="color:{LIME};">that</span><br>gets you <em style="color:{LIME};">hired.</em>
  </div>
</div>

<div style="position:absolute;bottom:44px;right:60px;font-family:'DM Sans';
             font-weight:500;font-size:20px;color:rgba(255,255,255,0.6);z-index:20;">SWIPE →</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 2: The Problem — Rambling Answers ─────────────────────────────────
def _slide2(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{PURPLE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE PROBLEM", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:60px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    "Tell me about a time..." then <em style="color:{LIME};font-style:italic;">chaos.</em>
  </div>
</div>
<div style="flex:1;margin-top:38px;display:flex;flex-direction:column;gap:20px;position:relative;z-index:5;">
  <div style="background:rgba(255,255,255,0.08);border:3px solid rgba(255,255,255,0.25);
               border-radius:18px;padding:26px 30px;">
    <div style="font-family:Inter;font-weight:700;font-size:22px;color:{HOT_PINK};letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">Without a structure</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:white;line-height:1.4;font-style:italic;">
      "Well, so basically, when I was in second year, well actually before that I did this thing, and there was this project, kind of, and we were meant to..."
    </div>
  </div>
  <div style="background:{LIME};color:{DARK_NAVY};border:3px solid {DARK_NAVY};
               border-radius:18px;padding:26px 30px;box-shadow:6px 6px 0 {DARK_NAVY};">
    <div style="font-family:Inter;font-weight:700;font-size:22px;color:{DARK_NAVY};letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">With STAR</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:{DARK_NAVY};line-height:1.4;">
      Situation. Task. Action. Result. Four sentences. Clear beginning, clear end. The interviewer stays with you the whole way.
    </div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:rgba(255,255,255,0.7);
               text-align:center;margin-top:6px;">92% of interviewers say structured answers score higher on 'communication'.</div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slides 3-6: S, T, A, R breakdowns ───────────────────────────────────────
def _star_slide(out, n, letter, word, kicker_text, headline, body_lines, example):
    f = _fonts()
    burst = _starburst(340, LIME, spikes=12)
    lines_html = "".join(
        f'<div style="display:flex;gap:14px;align-items:flex-start;margin-bottom:14px;">'
        f'<div style="width:8px;height:8px;background:{LIME};border-radius:50%;margin-top:12px;flex-shrink:0;"></div>'
        f'<div style="font-family:DM Sans,sans-serif;font-weight:500;font-size:26px;color:white;line-height:1.4;">{ln}</div>'
        f'</div>' for ln in body_lines
    )
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{PURPLE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(n)}
<!-- Burst top-right holding the letter -->
<div style="position:absolute;top:80px;right:-40px;transform:rotate({8 if n%2 else -6}deg);z-index:3;
             filter:drop-shadow(6px 6px 0 {DARK_NAVY});">{burst}</div>
<div style="position:absolute;top:190px;right:110px;z-index:8;">
  <div style="font-family:Inter;font-weight:700;font-size:180px;color:{DARK_NAVY};letter-spacing:-8px;
               line-height:0.9;">{letter}</div>
</div>

<div style="padding-top:74px;position:relative;z-index:5;max-width:620px;">
  {_kicker(kicker_text, LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:60px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    {word}
  </div>
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:38px;color:{LIME};
               margin-top:8px;line-height:1.1;letter-spacing:-1px;">{headline}</div>
</div>

<div style="flex:1;margin-top:34px;position:relative;z-index:5;max-width:620px;">
  {lines_html}
</div>

<div style="background:{LIME};color:{DARK_NAVY};border:3px solid {DARK_NAVY};
             border-radius:16px;padding:20px 26px;box-shadow:5px 5px 0 {DARK_NAVY};
             position:relative;z-index:5;">
  <div style="font-family:Inter;font-weight:700;font-size:18px;color:{DARK_NAVY};
               letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Example line</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:{DARK_NAVY};
               line-height:1.4;font-style:italic;">"{example}"</div>
</div>
</div></body></html>"""
    _render(html, out)


def _slide3(out): _star_slide(out, 3, "S", "Situation.",     "SET THE SCENE",
    "One sentence. That's it.",
    ["Give context in 15 seconds. Where, when, what team.",
     "Skip the backstory of the backstory.",
     "The interviewer needs enough to picture it. Not the full history."],
    "In my second-year group project, our team of four had to launch a fundraising campaign in 3 weeks.")
def _slide4(out): _star_slide(out, 4, "T", "Task.",          "THE CHALLENGE",
    "What YOU needed to do.",
    ["Make YOUR role obvious. Not the team's role.",
     "Name the specific problem you owned.",
     "This is where interviewers separate you from the group."],
    "I was responsible for the marketing plan and we had no budget and no prior audience.")
def _slide5(out): _star_slide(out, 5, "A", "Action.",        "WHAT YOU DID",
    "60% of your answer lives here.",
    ["Use 'I' not 'we'. Every sentence.",
     "Be specific about the moves you made and why.",
     "Show judgment, not just activity."],
    "I built a partnership approach - I reached out to 12 local businesses offering visibility for prizes.")
def _slide6(out): _star_slide(out, 6, "R", "Result.",        "THE PAYOFF",
    "Numbers. Always numbers.",
    ["Quantify the outcome. Even rough estimates land.",
     "Tie it back to the task in the first line.",
     "End with what you learned - shows self-awareness."],
    "We raised £3,400 - 40% above target - and I learned partnerships beat cold marketing every time.")


# ─── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    burst = _starburst(500, PURPLE, spikes=14)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{LIME};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
<div style="position:absolute;bottom:-100px;right:-80px;transform:rotate(-10deg);z-index:3;
             filter:drop-shadow(8px 8px 0 {DARK_NAVY});">{burst}</div>
<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:44px;left:44px;height:62px;z-index:25;">
<div style="position:absolute;top:52px;right:60px;background:{DARK_NAVY};color:{LIME};
             padding:14px 22px;border:3px solid {DARK_NAVY};border-radius:14px;
             font-family:Inter;font-weight:700;font-size:22px;letter-spacing:2px;text-transform:uppercase;
             transform:rotate(-4deg);z-index:35;box-shadow:5px 5px 0 {PURPLE};">Save this</div>

<div style="padding-top:130px;position:relative;z-index:10;">
  {_kicker("YOUR TURN", HOT_PINK)}
  <div style="font-family:Inter;font-weight:700;font-size:88px;line-height:0.95;color:{DARK_NAVY};
               letter-spacing:-4px;word-break:keep-all;hyphens:none;max-width:820px;">
    Pick 3 stories.<br>Drill them into<br><em style="color:{PURPLE};font-style:italic;">STAR shape.</em>
  </div>
</div>

<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;position:relative;z-index:10;">
  <div style="background:{OFF_WHITE};border:3px solid {DARK_NAVY};border-radius:18px;padding:26px 30px;
               box-shadow:6px 6px 0 {DARK_NAVY};max-width:640px;">
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:{DARK_NAVY};margin-bottom:12px;">The 3 stories every grad needs:</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{DARK_NAVY};line-height:1.5;">
      1. A time you led something<br>
      2. A time you handled conflict<br>
      3. A time you failed and learned
    </div>
  </div>
  <div style="margin-top:26px;display:inline-flex;align-items:center;gap:12px;background:{DARK_NAVY};
               color:{LIME};padding:18px 30px;border-radius:60px;font-family:Inter;
               font-weight:700;font-size:24px;border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {HOT_PINK};
               width:fit-content;">
    Find interviews at internwise.co.uk &#8594;
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating STAR Method (Week 7, Day 3)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("y2k_starburst_purple_lime_framework", "week7/d3-starmethod", "week7")
    print("Done - STAR method complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week7/d3-starmethod")
