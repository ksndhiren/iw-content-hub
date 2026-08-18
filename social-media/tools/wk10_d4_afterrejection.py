"""
Internwise - What To Do After a Rejection (Week 10, Day 4)
Design language: COMIC BOOK / POP-ART. Halftone dots, bold black panel borders,
speech bubbles, action bursts, primary pop colours. 7 slides.
Accent: pop YELLOW + red burst on cream halftone.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

INK      = "#141018"
CREAM    = "#FBF3DD"
POP_YEL  = "#FFD23F"
POP_RED  = "#FF3B3B"
POP_BLUE = "#3B7DFF"
POP_PINK = "#FF5CA8"
PAPER    = "#F7ECCB"

LOGO_DARK = None; LOGO_W = None
def _load_logos():
    global LOGO_DARK, LOGO_W
    if LOGO_DARK is None:
        LOGO_DARK = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_Blue Logo.png")) \
                 or _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_blue logo.png")) or ""
        LOGO_W = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""

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

def _halftone(color, opacity):
    return (f"background-image:radial-gradient({color} 22%,transparent 23%);"
            f"background-size:26px 26px;opacity:{opacity};")

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{CREAM};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px;overflow:hidden;}}
.frame{{position:absolute;inset:22px;border:8px solid {INK};border-radius:6px;pointer-events:none;z-index:40;
        box-shadow:0 0 0 4px {CREAM},0 0 0 12px {INK};}}
.ht{{position:absolute;inset:0;pointer-events:none;}}
"""

def _burst(text, bg, rot, size=30):
    # star burst badge
    pts = "50% 0%,61% 20%,84% 12%,77% 36%,100% 43%,80% 57%,92% 80%,66% 74%,58% 100%,45% 76%,20% 84%,27% 60%,3% 55%,24% 40%,10% 18%,36% 24%,42% 3%"
    box = int(size * 4.7)
    return (f'<div style="clip-path:polygon({pts});background:{bg};width:{box}px;height:{box}px;'
            f'display:flex;align-items:center;justify-content:center;transform:rotate({rot}deg);">'
            f'<span style="font-family:Inter;font-weight:700;font-size:{size}px;color:{INK};'
            f'transform:rotate({-rot}deg);text-align:center;line-height:0.95;letter-spacing:-0.5px;max-width:70%;">{text}</span></div>')

def _bubble(text, tail="left"):
    tail_css = ("left:60px;border-width:26px 22px 0 0;border-color:{0} transparent transparent transparent;".format(CREAM)
                if tail == "left" else
                "right:60px;border-width:26px 0 0 22px;border-color:{0} transparent transparent transparent;".format(CREAM))
    return f"""<div style="position:relative;display:inline-block;background:{CREAM};border:5px solid {INK};
             border-radius:28px;padding:20px 30px;box-shadow:6px 6px 0 {INK};">
  <span style="font-family:Inter;font-weight:700;font-size:34px;color:{INK};line-height:1.1;">{text}</span>
  <div style="position:absolute;bottom:-26px;{tail_css}border-style:solid;width:0;height:0;
        filter:drop-shadow(0 4px 0 {INK});"></div>
</div>"""

def _shell(inner, f, bg=CREAM, ht_color="rgba(0,0,0,0.10)", ht_op="1"):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_base_css(f)}</style></head>
<body><div class="c" style="background:{bg};">
  <div class="ht" style="{_halftone(ht_color, ht_op)}"></div>
  {inner}
  <div class="frame"></div>
</div></body></html>"""

def _panel_num(n):
    return (f'<div style="position:absolute;top:44px;left:44px;background:{INK};color:{POP_YEL};'
            f'width:56px;height:56px;border-radius:6px;display:flex;align-items:center;justify-content:center;'
            f'font-family:Inter;font-weight:700;font-size:26px;z-index:30;transform:rotate(-4deg);'
            f'box-shadow:4px 4px 0 rgba(0,0,0,0.25);">{n}</div>')


def _slide1(out):
    f = _fonts()
    inner = f"""
<div style="position:absolute;inset:22px;background:{POP_RED};z-index:1;"></div>
<div class="ht" style="{_halftone('rgba(0,0,0,0.14)','1')};z-index:2;inset:22px;"></div>
<div style="position:absolute;top:70px;left:70px;z-index:20;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:50px;filter:brightness(0);">
</div>
<div style="position:absolute;top:56px;right:52px;z-index:25;">{_burst("OUCH!", POP_YEL, 12, 24)}</div>
<div style="position:absolute;top:300px;left:70px;right:70px;z-index:20;">
  <div style="display:inline-block;background:{INK};padding:6px 22px;transform:rotate(-2deg);margin-bottom:22px;">
    <span style="font-family:'DM Sans';font-weight:700;font-size:22px;color:{POP_YEL};letter-spacing:3px;text-transform:uppercase;">Got rejected?</span>
  </div>
  <div style="font-family:Inter;font-weight:700;font-size:96px;line-height:0.92;color:{CREAM};
       letter-spacing:-3px;text-shadow:5px 5px 0 {INK};word-break:keep-all;">
    It&#39;s not<br>the end.<br><span style="color:{POP_YEL};">It&#39;s data.</span>
  </div>
</div>
<div style="position:absolute;bottom:70px;left:70px;z-index:20;">
  {_bubble("Turn a 'no' into your next 'yes' &rarr;", "left")}
</div>
"""
    _render(_shell(inner, f, bg=POP_RED), out)


def _slide2(out):
    f = _fonts()
    stats = [("2%","of applicants get an offer from a single role. Rejection is the default, not the exception.", POP_BLUE),
             ("5x","more interviews come from applicants who ask for feedback and reapply.", POP_YEL),
             ("24h","is all you need to feel it, then get moving again.", POP_PINK)]
    cards = ""
    for i,(v,l,col) in enumerate(stats):
        rot = [-2,1.5,-1][i]
        cards += f"""<div style="flex:1;background:{CREAM};border:6px solid {INK};border-radius:8px;padding:26px 22px;
             transform:rotate({rot}deg);box-shadow:7px 7px 0 {INK};">
  <div style="display:inline-block;background:{col};border:4px solid {INK};padding:2px 14px;border-radius:6px;">
    <span style="font-family:Inter;font-weight:700;font-size:52px;color:{INK};letter-spacing:-2px;">{v}</span>
  </div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:23px;color:{INK};margin-top:16px;line-height:1.35;">{l}</div>
</div>"""
    inner = f"""
{_panel_num(1)}
<div style="position:relative;z-index:20;padding:36px 24px 0 120px;">
  <div style="font-family:Inter;font-weight:700;font-size:56px;color:{INK};letter-spacing:-2px;line-height:1;">
    The <span style="background:{POP_YEL};padding:0 8px;box-shadow:4px 4px 0 {INK};">real</span> numbers.
  </div>
</div>
<div style="position:absolute;left:44px;right:44px;top:270px;display:flex;gap:24px;z-index:20;padding:0 20px;">{cards}</div>
<div style="position:absolute;bottom:60px;left:70px;z-index:20;font-family:'DM Sans';font-weight:400;font-size:19px;color:{INK};opacity:0.7;">
  Sources: Jobvite Recruiter Nation 2026, LinkedIn Talent Study
</div>
"""
    _render(_shell(inner, f), out)


def _act_slide(out, n, act, headline, bubble_text, body_lines, col):
    f = _fonts()
    lines = ""
    for t in body_lines:
        lines += f"""<div style="display:flex;gap:14px;align-items:flex-start;margin-bottom:16px;">
  <div style="flex-shrink:0;width:34px;height:34px;background:{col};border:4px solid {INK};border-radius:50%;
       display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:18px;color:{INK};">&#10003;</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:27px;color:{INK};line-height:1.35;padding-top:2px;">{t}</div>
</div>"""
    inner = f"""
{_panel_num(n)}
<div style="position:relative;z-index:25;padding:30px 66px 0 120px;display:flex;justify-content:flex-end;">
  {_burst(act, col, 8, 19)}
</div>
<div style="position:relative;z-index:20;padding:0 50px;margin-top:-20px;">
  <div style="font-family:Inter;font-weight:700;font-size:60px;color:{INK};letter-spacing:-2px;line-height:0.98;word-break:keep-all;">{headline}</div>
  <div style="margin-top:26px;">{_bubble(bubble_text, "left")}</div>
</div>
<div style="position:absolute;left:60px;right:60px;bottom:70px;background:{CREAM};border:6px solid {INK};
     border-radius:10px;padding:30px 34px;box-shadow:8px 8px 0 {INK};z-index:20;">
  {lines}
</div>
"""
    _render(_shell(inner, f), out)

def _slide3(out): _act_slide(out, 2, "STEP 1", "Feel it. Then<br>file it away.", "Give yourself 24 hours, tops.",
    ["Let it sting for a day - that's normal and healthy.",
     "Don't fire off an angry reply you can't take back.",
     "Write down one thing that actually went well."], POP_PINK)

def _slide4(out): _act_slide(out, 3, "STEP 2", "Ask for the<br>feedback.", "One short, polite email. Always.",
    ["Thank them and ask what would've made you stronger.",
     "Keep it to three sentences - busy people reply to short.",
     "Save every reply - patterns tell you what to fix."], POP_BLUE)

def _slide5(out): _act_slide(out, 4, "STEP 3", "Fix the one<br>weak spot.", "Small tweak, big difference.",
    ["Turn the feedback into a single concrete change.",
     "Redo your weakest interview answer out loud, twice.",
     "Update your CV before you touch the next application."], POP_YEL)

def _slide6(out): _act_slide(out, 5, "STEP 4", "Reapply.<br>Seriously.", "The door isn't bolted shut.",
    ["Many teams re-hire candidates who improve and come back.",
     "Apply to 3 similar roles while your prep is fresh.",
     "Stay warm with the recruiter - a 'no' can become 'not yet'."], POP_RED)


def _slide7(out):
    f = _fonts()
    steps = ["Feel it (24h max)","Ask for feedback","Fix one weak spot","Reapply, improved"]
    rows = ""
    for i,s in enumerate(steps):
        rows += f"""<div style="display:flex;gap:16px;align-items:center;margin-bottom:14px;">
  <div style="width:44px;height:44px;background:{POP_YEL};border:4px solid {CREAM};border-radius:50%;
       display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{INK};">{i+1}</div>
  <span style="font-family:Inter;font-weight:700;font-size:30px;color:{CREAM};">{s}</span>
</div>"""
    inner = f"""
<div style="position:absolute;inset:22px;background:{INK};z-index:1;"></div>
<div class="ht" style="{_halftone('rgba(255,255,255,0.08)','1')};z-index:2;inset:22px;"></div>
<div style="position:absolute;top:60px;left:70px;z-index:20;">
  <img src="data:image/png;base64,{LOGO_DARK}" style="height:48px;filter:brightness(0) invert(1);">
</div>
<div style="position:absolute;top:56px;right:56px;z-index:25;">{_burst("YOU GOT THIS", POP_YEL, 10, 20)}</div>
<div style="position:absolute;top:210px;left:70px;right:70px;z-index:20;">
  <div style="font-family:Inter;font-weight:700;font-size:70px;color:{CREAM};letter-spacing:-2px;line-height:0.95;word-break:keep-all;">
    A 'no' is just<br><span style="color:{POP_YEL};">round one.</span>
  </div>
</div>
<div style="position:absolute;top:420px;left:70px;z-index:20;">{rows}</div>
<div style="position:absolute;bottom:70px;left:70px;z-index:20;">
  <div style="display:inline-flex;align-items:center;gap:12px;background:{POP_YEL};border:5px solid {CREAM};
       color:{INK};padding:16px 30px;border-radius:50px;font-family:Inter;font-weight:700;font-size:26px;
       box-shadow:6px 6px 0 rgba(0,0,0,0.4);">
    Next role &rarr; internwise.co.uk
  </div>
</div>
"""
    _render(_shell(inner, f, bg=INK), out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating After Rejection (Week 10, Day 4)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("comic_book_popart_halftone", "week10/d4-afterrejection", "week10")
    print("Done - after rejection complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week10/d4-afterrejection")
