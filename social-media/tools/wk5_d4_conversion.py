"""
Internwise - Internship to Full-Time Offer (Week 5, Day 4) - v2
6-slide carousel: Gen Z design language, massive type, neobrutalist elements.
Slides 1, 6: arch+cutout photos. Slides 2-5: bold typographic/graphic treatment.
"""
import os, base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_cutout

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"; LIGHT_BLUE = "#5FA7E5"

LOGO_B64 = None
def _load_logo():
    global LOGO_B64
    if LOGO_B64 is None:
        LOGO_B64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    return LOGO_B64

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
    print(f"  ok {path}")

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"

def _arch_photo(src, accent):
    if not src: return ""
    return f"""
<div style="position:absolute;bottom:0;right:0;width:460px;height:610px;
            background:linear-gradient(155deg,{accent},{accent}88);
            border-radius:230px 230px 0 0;z-index:5;
            box-shadow:-10px 0 40px rgba(0,0,0,0.2);"></div>
<div style="position:absolute;bottom:0;right:0;width:500px;height:700px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.35));overflow:hidden;">
  <img src="{src}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""

def _spark(s, t, l, c, o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:3;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'


# ── Slide 1: Hook ─────────────────────────────────────────────────────────────
def _slide1(out, photo_src):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.badge{{position:absolute;top:44px;right:44px;background:{MINT};color:{DEEP_BLUE};
    padding:11px 26px;border-radius:50px;font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(4deg);
    box-shadow:0 8px 22px rgba(127,219,182,0.4);z-index:20;}}
.col{{position:absolute;top:0;left:0;right:534px;bottom:0;
      display:flex;flex-direction:column;justify-content:flex-start;
      padding:148px 30px 60px 56px;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;
    color:{MINT};text-transform:uppercase;letter-spacing:4px;margin-bottom:18px;}}
.hl{{font-family:Inter;font-weight:700;font-size:88px;line-height:1.0;
    color:white;letter-spacing:-4px;margin-bottom:22px;word-break:keep-all;}}
.hl em{{color:{MINT};font-style:italic;}}
.accent-bar{{width:70px;height:5px;background:{MINT};border-radius:2px;margin-bottom:24px;}}
.sub{{font-family:'DM Sans';font-weight:600;font-size:23px;
    color:rgba(255,255,255,0.62);line-height:1.45;}}
.hint{{position:absolute;bottom:44px;left:56px;z-index:20;
    font-family:Inter;font-weight:700;font-size:18px;color:rgba(255,255,255,0.35);}}
.hint strong{{color:rgba(255,255,255,0.65);}}
</style></head><body><div class="c">
<div class="grain"></div>
{_arch_photo(photo_src, MINT)}
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:25;">
<div class="badge">Internship guide</div>
<div class="col">
  <div class="kicker">Turn it into a job</div>
  <div class="hl">You're in.<br>Now<br><em>convert it.</em></div>
  <div class="accent-bar"></div>
  <div class="sub">Most interns wait<br>and hope. The ones<br>who get offers<br>play differently.</div>
</div>
<div class="hint">Swipe for the playbook <strong>-&gt;</strong></div>
{_spark(24,210,430,MINT,0.45)}
{_spark(14,390,400,"white",0.18)}
</div></body></html>"""
    _render(html, out)


# ── Slide 2: First 2 Weeks (Bento Grid) ──────────────────────────────────────
def _slide2(out):
    f = _fonts()
    cards = [
        (MINT,   DARK_NAVY, "1", "Learn first.",        "Ask 'What are you focused on right now?' Not 'How did you get here?'"),
        (AMBER,  DARK_NAVY, "2", "Find a quick win.",   "Something you can complete in full within the first 5 days."),
        (CORAL,  "white",   "3", "Under-promise.",      "Over-deliver on timing, every time. No exceptions."),
        (PURPLE, "white",   "4", "Share proactively.",  "Brief your manager on what you found, even if unsolicited."),
    ]
    cards_html = ""
    for bg, tc, num, title, desc in cards:
        desc_color = "rgba(0,0,0,0.55)" if tc == DARK_NAVY else "rgba(255,255,255,0.78)"
        cards_html += f"""
<div style="flex:1 1 45%;background:{bg};border-radius:20px;padding:32px 30px;
            border:3px solid {DARK_NAVY};box-shadow:6px 6px 0 {DARK_NAVY};
            display:flex;flex-direction:column;justify-content:space-between;">
  <div style="font-family:Inter;font-weight:700;font-size:96px;line-height:1;
              color:rgba(0,0,0,0.13);letter-spacing:-5px;">{num}</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:34px;line-height:1.1;
                color:{tc};margin-bottom:10px;word-break:keep-all;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:600;font-size:24px;line-height:1.4;
                color:{desc_color};">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);
    padding:44px 50px 50px 50px;display:flex;flex-direction:column;gap:24px;}}
{GRAIN}
.top{{display:flex;align-items:flex-start;justify-content:space-between;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:15px;color:{MINT};
    text-transform:uppercase;letter-spacing:4px;margin-bottom:8px;}}
.hl{{font-family:Inter;font-weight:700;font-size:68px;line-height:1.0;
    color:white;letter-spacing:-4px;word-break:keep-all;}}
.hl em{{color:{MINT};font-style:italic;}}
.num{{font-family:Inter;font-weight:700;font-size:14px;
    color:rgba(255,255,255,0.22);letter-spacing:2px;margin-top:6px;}}
.grid{{display:flex;flex-wrap:wrap;gap:18px;flex:1;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="top">
  <div>
    <img src="data:image/png;base64,{LOGO_B64}" style="height:54px;opacity:0.95;display:block;margin-bottom:14px;">
    <div class="kicker">Days 1-14</div>
    <div class="hl">Set the<br>ceiling <em>early.</em></div>
  </div>
  <div class="num">1 / 4</div>
</div>
<div class="grid">
{cards_html}
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: Mid-Point ────────────────────────────────────────────────────────
def _slide3(out):
    f = _fonts()
    steps = [
        (AMBER,      "Request a mid-point review",   "Book 30 minutes with your manager. Initiative - not just compliance."),
        (MINT,       "Name what's going well",        "Come with examples. Don't wait for them to remember your wins."),
        (CORAL,      "Ask what to improve",           "Two specific areas. Act on the feedback before it's forgotten."),
        (LIGHT_BLUE, "Raise your hand for more",      "Tell them when you have capacity. Interns who ask for more stand out."),
    ]
    steps_html = ""
    for bg, title, desc in steps:
        steps_html += f"""
<div style="background:rgba(255,255,255,0.04);border-radius:16px;padding:20px 22px;
            border:2px solid rgba(255,255,255,0.06);border-left:5px solid {bg};
            display:flex;gap:16px;align-items:flex-start;">
  <div style="width:12px;height:12px;border-radius:50%;background:{bg};
              flex-shrink:0;margin-top:9px;"></div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:{bg};
                margin-bottom:6px;line-height:1.1;word-break:keep-all;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:20px;
                color:rgba(255,255,255,0.60);line-height:1.4;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.left{{position:absolute;top:0;left:0;bottom:0;width:470px;
       display:flex;flex-direction:column;justify-content:flex-start;
       padding:148px 24px 60px 56px;z-index:10;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:15px;color:{AMBER};
    text-transform:uppercase;letter-spacing:4px;margin-bottom:18px;}}
.hl{{font-family:Inter;font-weight:700;font-size:72px;line-height:1.05;
    color:white;letter-spacing:-3px;margin-bottom:24px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.accent{{font-family:'DM Sans';font-weight:600;font-size:21px;
    color:rgba(255,255,255,0.48);line-height:1.5;}}
.right{{position:absolute;top:0;right:0;bottom:0;width:594px;
        display:flex;flex-direction:column;justify-content:center;
        gap:14px;padding:44px 48px 44px 18px;z-index:10;}}
.num{{position:absolute;top:48px;right:50px;font-family:Inter;font-weight:700;
    font-size:14px;color:rgba(255,255,255,0.22);letter-spacing:2px;z-index:20;}}
.divider{{position:absolute;top:80px;bottom:80px;left:470px;
    width:1px;background:rgba(255,255,255,0.08);z-index:5;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="divider"></div>
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:44px;height:60px;opacity:0.95;z-index:20;">
<div class="num">2 / 4</div>
<div class="left">
  <div class="kicker">Mid-point</div>
  <div class="hl">The<br>check&#8209;in<br>most interns<br>never <em>ask for.</em></div>
  <div class="accent">Your manager will<br>remember you asked.<br>That alone separates<br>you from most.</div>
</div>
<div class="right">
{steps_html}
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: Final 2 Weeks (Color split) ─────────────────────────────────────
def _slide4(out):
    f = _fonts()
    actions = [
        ("Write your accomplishment list",      "Every project, impact, and skill developed. You'll need this when you ask."),
        ("Document your work thoroughly",       "Templates, contacts, processes. A great handover shows you care."),
        ("Thank each person individually",      "A direct, specific message. Not a group email. Make it personal."),
        ("Ask for a reference before you leave","In person. Agree the format. Not a LinkedIn request later."),
        ("Stay in touch after you leave",       "A brief update at 3 months keeps the relationship warm."),
    ]
    actions_html = ""
    for i, (title, desc) in enumerate(actions):
        border = f"border-bottom:1px solid rgba(255,255,255,0.15);" if i < 4 else ""
        actions_html += f"""
<div style="display:flex;gap:16px;align-items:flex-start;padding:14px 0;{border}">
  <div style="width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.18);
              display:flex;align-items:center;justify-content:center;flex-shrink:0;
              font-family:Inter;font-weight:700;font-size:18px;color:white;">{i+1}</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;
                margin-bottom:4px;line-height:1.2;word-break:keep-all;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:22px;
                color:rgba(255,255,255,0.72);line-height:1.35;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.left{{position:absolute;top:0;left:0;bottom:0;width:416px;
       display:flex;flex-direction:column;justify-content:flex-start;
       padding:148px 24px 60px 56px;z-index:10;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:15px;color:{CORAL};
    text-transform:uppercase;letter-spacing:4px;margin-bottom:18px;}}
.hl{{font-family:Inter;font-weight:700;font-size:80px;line-height:1.0;
    color:white;letter-spacing:-4px;margin-bottom:24px;word-break:keep-all;}}
.hl em{{color:{CORAL};font-style:italic;}}
.sub{{font-family:'DM Sans';font-weight:600;font-size:21px;
    color:rgba(255,255,255,0.48);line-height:1.5;}}
.right{{position:absolute;top:0;right:0;bottom:0;width:664px;
        background:{CORAL};display:flex;flex-direction:column;
        justify-content:center;padding:56px 50px 56px 48px;z-index:10;}}
.right-label{{font-family:'DM Sans';font-weight:700;font-size:13px;color:{DEEP_BLUE};
    text-transform:uppercase;letter-spacing:4px;margin-bottom:20px;opacity:0.6;}}
.num{{position:absolute;top:44px;right:50px;font-family:Inter;font-weight:700;
    font-size:14px;color:{DEEP_BLUE};letter-spacing:2px;opacity:0.3;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:44px;height:60px;opacity:0.95;z-index:20;">
<div class="num">3 / 4</div>
<div class="left">
  <div class="kicker">Final 2 weeks</div>
  <div class="hl">Finish<br>stronger<br>than you<br><em>started.</em></div>
  <div class="sub">Most interns trail off.<br>The ones who get<br>offers accelerate.</div>
</div>
<div class="right">
  <div class="right-label">The 5 actions</div>
  {actions_html}
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: How to Ask (Full-canvas quote) ───────────────────────────────────
def _slide5(out):
    f = _fonts()
    rules = [
        (MINT,  "Ask before your final week - not on the last day."),
        (AMBER, "Frame it as curiosity, not a demand or expectation."),
        (CORAL, "Have your accomplishment list ready if they ask."),
    ]
    rules_html = "".join(f"""
<div style="background:rgba(255,255,255,0.05);border-radius:14px;
            padding:15px 20px;border:2px solid rgba(255,255,255,0.07);
            border-left:5px solid {bg};display:flex;gap:14px;align-items:center;">
  <div style="width:10px;height:10px;border-radius:50%;background:{bg};flex-shrink:0;"></div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:25px;
              color:rgba(255,255,255,0.76);line-height:1.35;">{text}</div>
</div>""" for bg, text in rules)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);
    display:flex;flex-direction:column;padding:44px 80px 50px 80px;}}
{GRAIN}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:15px;color:{MINT};
    text-transform:uppercase;letter-spacing:4px;margin-top:96px;margin-bottom:24px;
    text-align:center;}}
.qmark{{font-family:Georgia,'Times New Roman',serif;font-size:140px;line-height:0.8;
    color:{AMBER};margin-bottom:6px;}}
.quote-box{{background:rgba(255,255,255,0.05);border-radius:20px;
    padding:30px 34px;border:2px solid rgba(255,255,255,0.08);
    border-left:6px solid {AMBER};margin-bottom:28px;}}
.quote-label{{font-family:'DM Sans';font-weight:700;font-size:13px;
    color:rgba(255,255,255,0.32);text-transform:uppercase;letter-spacing:2px;
    margin-bottom:12px;}}
.quote-text{{font-family:'DM Sans';font-weight:600;font-size:30px;
    color:white;line-height:1.5;font-style:italic;}}
.rules-label{{font-family:'DM Sans';font-weight:700;font-size:14px;color:{MINT};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:14px;}}
.rules{{display:flex;flex-direction:column;gap:11px;}}
.num{{position:absolute;top:44px;right:80px;font-family:Inter;font-weight:700;
    font-size:14px;color:rgba(255,255,255,0.22);letter-spacing:2px;}}
</style></head><body><div class="c">
<div class="grain"></div>
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:80px;height:60px;opacity:0.95;z-index:20;">
<div class="num">4 / 4</div>
<div class="kicker">The exact words to use</div>
<div class="qmark">&ldquo;</div>
<div class="quote-box">
  <div class="quote-label">What to say - example</div>
  <div class="quote-text">I've really enjoyed this placement. Are there permanent or graduate roles that tend to come up in this team, and is there anything I should be doing now to be in a strong position?</div>
</div>
<div class="rules-label">3 rules for the ask</div>
<div class="rules">
{rules_html}
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: CTA (photo, light bg) ────────────────────────────────────────────
def _slide6(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path) if photo_path else ""
    checks = [
        (MINT,       DARK_NAVY, "1", "Mid-point review done and acted on"),
        (AMBER,      DARK_NAVY, "2", "Accomplishment list written and ready"),
        (CORAL,      "white",   "3", "Thank-you notes sent before last day"),
        (PURPLE,     "white",   "4", "Reference agreed and confirmed"),
        (LIGHT_BLUE, DARK_NAVY, "5", "Future roles conversation had directly"),
    ]
    checks_html = "".join(f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:11px;">
  <div style="width:36px;height:36px;border-radius:50%;flex-shrink:0;
              background:{bg};border:2px solid {DARK_NAVY};
              display:flex;align-items:center;justify-content:center;
              font-family:Inter;font-weight:700;font-size:16px;color:{ct};">{num}</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:19px;
              color:{DEEP_BLUE};line-height:1.3;white-space:nowrap;">{text}</div>
</div>""" for bg, ct, num, text in checks)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{OFF_WHITE};}}
.grain2{{position:absolute;inset:0;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(0,0,0,0.022) 1px,transparent 1px);
    background-size:3px 3px;}}
.col{{position:absolute;top:0;left:0;bottom:0;right:534px;
      display:flex;flex-direction:column;justify-content:flex-start;
      padding:148px 24px 50px 60px;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:15px;color:{MINT};
    text-transform:uppercase;letter-spacing:4px;margin-bottom:14px;}}
.big{{font-family:Inter;font-weight:700;font-size:80px;line-height:1.0;
    color:{DEEP_BLUE};letter-spacing:-4px;margin-bottom:22px;word-break:keep-all;}}
.big em{{color:{MINT};font-style:italic;}}
.checks{{display:flex;flex-direction:column;margin-bottom:20px;}}
.cta{{background:{DEEP_BLUE};color:white;padding:18px 22px;border-radius:16px;
    font-family:Inter;font-weight:700;font-size:19px;
    border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
    display:flex;align-items:center;justify-content:space-between;}}
.arrow{{width:46px;height:46px;background:{MINT};border-radius:50%;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
.badge{{position:absolute;top:44px;right:44px;background:{DEEP_BLUE};color:white;
    padding:11px 24px;border-radius:50px;font-family:Inter;font-weight:700;font-size:13px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(-3deg);
    box-shadow:5px 5px 0 {DARK_NAVY};z-index:25;}}
</style></head><body><div class="c">
<div class="grain2"></div>
<div style="position:absolute;bottom:0;right:0;width:460px;height:610px;
            background:linear-gradient(155deg,{DEEP_BLUE},{DEEP_BLUE}88);
            border-radius:230px 230px 0 0;z-index:5;
            box-shadow:-10px 0 40px rgba(0,0,0,0.15);"></div>
<div style="position:absolute;bottom:0;right:0;width:500px;height:700px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.25));overflow:hidden;">
  <img src="{photo_src}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:60px;height:60px;opacity:0.95;z-index:25;filter:brightness(0) saturate(100%) invert(18%) sepia(34%) saturate(1289%) hue-rotate(183deg) brightness(94%) contrast(91%);">
<div class="badge">Internship done right</div>
<div class="col">
  <div class="kicker">Your conversion checklist</div>
  <div class="big">Leave<br>nothing<br>on the<br><em>table.</em></div>
  <div class="checks">{checks_html}</div>
  <div class="cta">
    <div>
      <div>Find your next placement</div>
      <div style="font-family:Inter;font-weight:700;font-size:15px;color:{MINT};margin-top:4px;">internwise.co.uk -&gt;</div>
    </div>
    <div class="arrow">
      <svg width="22" height="22" viewBox="0 0 24 24">
        <path d="M5 12L19 12M14 7L20 12L14 17" stroke="{DEEP_BLUE}" stroke-width="2.5"
              fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Main ──────────────────────────────────────────────────────────────────────
def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Internship Conversion Carousel (Week 5, Day 4) v2...")
    _load_logo()

    photos = {}
    fetch_list = [
        ("a", "cheerful young white man arms open smiling wide standing white background studio", 1),
        ("b", "young asian woman professional confident smiling standing arms at sides white background studio isolated portrait", 2),
    ]
    for key, query, idx in fetch_list:
        try:
            photos[key] = get_cutout(query, index=idx, orientation="portrait")
            print(f"    ok {key}: {photos[key]}")
        except Exception as e:
            print(f"    ! {key} failed: {e}")
            photos[key] = None

    _slide1(os.path.join(campaign_dir, "slide_1.png"), _src(photos.get("a")))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"), photos.get("b"))
    print("Done - internship conversion carousel v2 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week5/d4-conversion")
