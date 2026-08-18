"""
Internwise - Final-Round Interview Prep (Week 10, Day 3)
Design language: THEATRE / SPOTLIGHT MAIN-STAGE. Dark stage, red velvet curtains,
a spotlight cone, gold framing, a Pexels cutout stepping into the light.
7 slides. Accent: GOLD + deep CURTAIN red on stage black.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import get_used_hashes, register_used_hashes, register_design, get_cutout_unique
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; OFF_WHITE = "#FAF5EC"; CORAL = "#FF6B6B"
STAGE    = "#120A0E"; STAGE2 = "#1E0E14"
GOLD     = "#E9BC58"; GOLD_D = "#C99A34"
CURTAIN  = "#6E1220"; CURTAIN_D = "#3E0A12"; CURTAIN_L = "#9E1E30"
CREAM    = "#F3E9D8"

LOGO_W = None
def _load_logos():
    global LOGO_W
    if LOGO_W is None:
        LOGO_W = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

def _src(path):
    b = _b64(path); return f"data:image/png;base64,{b}" if b else ""

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

# curtain side panel (vertical velvet stripes)
def _curtain(side):
    pos = "left:0;" if side == "left" else "right:0;"
    return f"""<div style="position:absolute;top:0;{pos}width:150px;height:1080px;z-index:6;
             background:linear-gradient(90deg,{CURTAIN_D} 0%,{CURTAIN} 30%,{CURTAIN_L} 45%,{CURTAIN} 60%,{CURTAIN_D} 78%,{CURTAIN} 90%,{CURTAIN_D} 100%);
             box-shadow:inset 0 0 40px rgba(0,0,0,0.6);"></div>
  <div style="position:absolute;top:0;{pos}width:150px;height:64px;z-index:7;
             background:linear-gradient(180deg,{GOLD_D},{CURTAIN_D});"></div>"""

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{STAGE};}}
.c{{width:1080px;height:1080px;position:relative;padding:52px 66px;display:flex;flex-direction:column;}}
.spot{{position:absolute;top:-120px;left:50%;transform:translateX(-50%);width:760px;height:1000px;z-index:2;
       background:radial-gradient(ellipse at 50% 8%,rgba(233,188,88,0.22) 0%,rgba(233,188,88,0.06) 40%,transparent 68%);
       clip-path:polygon(42% 0,58% 0,100% 100%,0 100%);pointer-events:none;}}
.floor{{position:absolute;bottom:0;left:0;width:1080px;height:150px;z-index:1;
        background:linear-gradient(180deg,transparent,rgba(233,188,88,0.05));}}
"""

def _kicker(t, c=GOLD):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:19px;color:{c};text-transform:uppercase;letter-spacing:4px;">{t}</div>'

def _head(html, size=58):
    return f'<div style="font-family:Inter;font-weight:700;font-size:{size}px;line-height:1.02;color:{CREAM};letter-spacing:-2px;word-break:keep-all;hyphens:none;">{html}</div>'

def _marquee(text):
    return f"""<div style="display:inline-flex;align-items:center;gap:12px;background:{STAGE2};
             border:2px solid {GOLD};border-radius:50px;padding:12px 26px;
             font-family:Inter;font-weight:700;font-size:20px;color:{GOLD};letter-spacing:2px;
             text-transform:uppercase;box-shadow:0 0 30px rgba(233,188,88,0.25);">
  <span style="width:10px;height:10px;border-radius:50%;background:{GOLD};box-shadow:0 0 10px {GOLD};"></span>{text}
</div>"""

def _shell(inner, f, curtains=True):
    cur = (_curtain('left')+_curtain('right')) if curtains else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_base_css(f)}</style></head>
<body><div class="c"><div class="spot"></div><div class="floor"></div>{cur}{inner}</div></body></html>"""

def _num(n):
    return (f'<div style="position:absolute;top:48px;left:66px;width:54px;height:54px;border-radius:50%;'
            f'border:2px solid {GOLD};display:flex;align-items:center;justify-content:center;font-family:Inter;'
            f'font-weight:700;font-size:22px;color:{GOLD};z-index:20;">{n}</div>')


def _slide1(out, photo):
    f = _fonts()
    inner = f"""
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;position:relative;z-index:20;padding:0 60px;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:52px;">
  {_marquee("Final Round")}
</div>
<div style="flex:1;display:flex;align-items:flex-end;position:relative;z-index:10;padding:0 40px;">
  <div style="flex:1;padding-bottom:40px;">
    {_kicker("Interviews / the last 5%")}
    <div style="margin-top:18px;">{_head('You made<br>the <span style="color:'+GOLD+';">final.</span><br>Now own it.', 86)}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:#C9B79E;margin-top:22px;max-width:480px;line-height:1.35;">
      They already like you. The final round is about fit, not proving you can do the job.
    </div>
  </div>
  <img src="{photo}" style="height:720px;object-fit:contain;position:relative;z-index:8;margin-right:-10px;
        filter:drop-shadow(0 0 40px rgba(233,188,88,0.35));">
</div>
<div style="flex-shrink:0;text-align:right;padding:0 60px;position:relative;z-index:20;">
  <span style="font-family:'DM Sans';font-weight:600;font-size:20px;color:{GOLD};">Swipe &rarr;</span>
</div>
"""
    _render(_shell(inner, f), out)


def _prep_slide(out, n, kicker, headline, body_lines, quote):
    f = _fonts()
    lines = ""
    for t in body_lines:
        lines += f"""<div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:16px;">
  <div style="color:{GOLD};font-family:Inter;font-weight:700;font-size:26px;line-height:1;margin-top:2px;">&#9733;</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:{CREAM};line-height:1.4;">{t}</div>
</div>"""
    inner = f"""
{_num(n)}
<div style="padding:78px 30px 0 30px;flex-shrink:0;position:relative;z-index:10;">
  {_kicker(kicker)}
  <div style="margin-top:12px;">{_head(headline, 56)}</div>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:0 30px;position:relative;z-index:10;">
  {lines}
</div>
<div style="flex-shrink:0;padding:0 30px 10px 30px;position:relative;z-index:10;">
  <div style="border-left:3px solid {GOLD};padding:8px 0 8px 20px;font-family:'DM Sans';font-weight:700;
               font-style:italic;font-size:24px;color:{GOLD};line-height:1.35;">{quote}</div>
</div>
"""
    _render(_shell(inner, f), out)

def _slide2(out):
    f = _fonts()
    stats = [("2-3","people usually make the final. It's yours to lose, not to win."),
             ("55%","of final-round decisions come down to fit and how you'd work with them."),
             ("1","memorable, specific question from you can tip a tie in your favour.")]
    cards = ""
    for v,l in stats:
        cards += f"""<div style="flex:1;background:{STAGE2};border:1.5px solid {GOLD}44;border-radius:16px;padding:30px 24px;">
  <div style="font-family:Inter;font-weight:700;font-size:64px;color:{GOLD};letter-spacing:-2px;line-height:1;">{v}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{CREAM};margin-top:16px;line-height:1.4;">{l}</div>
</div>"""
    inner = f"""
<div style="padding:0 30px;flex-shrink:0;position:relative;z-index:10;">{_kicker("The odds")}
  <div style="margin-top:12px;">{_head('It&#39;s <span style="color:'+GOLD+';">yours</span> to lose.', 54)}</div></div>
<div style="flex:1;display:flex;gap:20px;align-items:center;padding:0 30px;position:relative;z-index:10;">{cards}</div>
<div style="flex-shrink:0;padding:0 30px;text-align:right;font-family:'DM Sans';font-weight:400;font-size:19px;color:#8A7A66;position:relative;z-index:10;">Sources: SHRM Hiring Report 2026, LinkedIn Interview Study</div>
"""
    _render(_shell(inner, f), out)

def _slide3(out): _prep_slide(out, 3, "Prep 01 / Fit", 'Show you\'d <span style="color:'+GOLD+';">fit in.</span>',
    ["Learn who you'd work with and reference them by name.",
     "Mirror their energy - calm and measured, or fast and punchy.",
     "Talk in 'we' about their goals, like you're already on the team."],
    "Final rounds hire the person they'd want in the room every day.")

def _slide4(out): _prep_slide(out, 4, "Prep 02 / Depth", 'Go one layer <span style="color:'+GOLD+';">deeper.</span>',
    ["Re-tell your best story with the result they care about most.",
     "Have a number ready for every claim you make.",
     "Prepare the answer to 'what would you do in your first 90 days?'"],
    "Earlier rounds test if you can. The final tests how you think.")

def _slide5(out): _prep_slide(out, 5, "Prep 03 / Questions", 'Ask the <span style="color:'+GOLD+';">right</span> question.',
    ["'What does success look like in this role at 6 months?'",
     "'What's the biggest challenge the team is facing right now?'",
     "'What made you decide to move me to this stage?'"],
    "The candidate who asks the sharpest question is remembered.")

def _slide6(out): _prep_slide(out, 6, "Prep 04 / Close", 'Close with <span style="color:'+GOLD+';">intent.</span>',
    ["Say clearly that you want the role and why.",
     "Ask about next steps and timeline before you leave.",
     "Send a short, specific thank-you within a few hours."],
    "Enthusiasm, stated out loud, breaks ties more often than you'd think.")


def _slide7(out, photo):
    f = _fonts()
    checks = ["Show fit, not just skill","Numbers behind every claim","One standout question ready","State that you want it"]
    rows = ""
    for c in checks:
        rows += f"""<div style="display:flex;gap:14px;align-items:center;padding:8px 0;">
  <span style="color:{GOLD};font-size:22px;">&#9733;</span>
  <span style="font-family:'DM Sans';font-weight:500;font-size:26px;color:{CREAM};">{c}</span></div>"""
    inner = f"""
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;position:relative;z-index:20;padding:0 60px;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:52px;">
  {_marquee("Curtain up")}
</div>
<div style="flex:1;display:flex;align-items:flex-end;position:relative;z-index:10;padding:0 40px;">
  <div style="flex:1;padding-bottom:36px;">
    {_kicker("Your cue")}
    <div style="margin-top:14px;">{_head('Walk in like<br>it&#39;s <span style="color:'+GOLD+';">already yours.</span>', 60)}</div>
    <div style="background:{STAGE2};border:1.5px solid {GOLD}44;border-radius:16px;padding:24px 28px;margin-top:24px;max-width:520px;">
      {rows}
    </div>
    <div style="margin-top:26px;display:inline-flex;align-items:center;gap:12px;background:{GOLD};color:{STAGE};
                 padding:16px 30px;border-radius:50px;font-family:Inter;font-weight:700;font-size:23px;">
      Find roles at internwise.co.uk &rarr;
    </div>
  </div>
  <img src="{photo}" style="height:640px;object-fit:contain;position:relative;z-index:8;margin-right:-10px;
        filter:drop-shadow(0 0 40px rgba(233,188,88,0.35));">
</div>
"""
    _render(_shell(inner, f), out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Final Round (Week 10, Day 3)...")
    _load_logos()
    used = get_used_hashes()
    p1 = get_cutout_unique("confident young white caucasian businesswoman blazer suit smiling colour portrait studio white background",
                           orientation="portrait", extra_exclude=used)
    h1 = os.path.basename(p1).replace("_nobg.png","")
    used |= {h1}
    p7 = get_cutout_unique("young professional in suit confident arms crossed studio white background",
                           orientation="portrait", extra_exclude=used)
    h7 = os.path.basename(p7).replace("_nobg.png","")
    _slide1(os.path.join(campaign_dir, "slide_1.png"), _src(p1))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), _src(p7))
    register_used_hashes([h1, h7], "week10/d3-finalround", "week10")
    register_design("theatre_spotlight_stage", "week10/d3-finalround", "week10")
    print("Done - final round complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week10/d3-finalround")
