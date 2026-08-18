"""
Internwise - Assessment Centres: What They Actually Test (Week 5, Day 1) - v2
7-slide carousel. CORAL accent, Gen Z style.
Hook (slide 1): full CORAL bg, pure typography, no photo — unique from all others.
"""
import os, base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_cutout

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"

LOGO_W = None   # white logo — dark backgrounds
LOGO_C = None   # coloured logo — light/coral backgrounds
def _load_logos():
    global LOGO_W, LOGO_C
    if LOGO_W is None:
        LOGO_W = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    if LOGO_C is None:
        LOGO_C = _b64(os.path.join(BRANDING_DIR, "PNG", "Internwise.Com-Horizontal logo.png")) or ""

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
GRAIN_DARK = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(0,0,0,0.04) 1px,transparent 1px);background-size:3px 3px;}"

def _spark(s, t, l, c, o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:3;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'

def _logo_white():
    return f'<img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:44px;left:44px;height:68px;opacity:0.95;z-index:25;">'

def _logo_color():
    return f'<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:44px;left:44px;height:68px;z-index:25;">'

def _num_badge(n, bg=CORAL, fg="white"):
    return f'<div style="position:absolute;top:44px;left:44px;width:56px;height:56px;border-radius:50%;background:{bg};border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:24px;color:{fg};z-index:25;">{n}</div>'


# ── Slide 1: Hook — full CORAL, pure typography, "AC" ghost, no photo ────────
def _slide1(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{CORAL};}}
{GRAIN_DARK}
.ghost{{position:absolute;bottom:-80px;right:-60px;font-family:Inter;font-weight:700;
    font-size:580px;color:{DARK_NAVY};opacity:0.07;line-height:1;z-index:1;
    pointer-events:none;letter-spacing:-20px;}}
.col{{position:absolute;top:0;left:56px;right:60px;bottom:0;
      display:flex;flex-direction:column;justify-content:center;z-index:10;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:18px;color:{DARK_NAVY};
    text-transform:uppercase;letter-spacing:4px;margin-bottom:26px;opacity:0.6;}}
.hl{{font-family:Inter;font-weight:700;font-size:96px;line-height:0.93;
    color:{DARK_NAVY};letter-spacing:-5px;margin-bottom:30px;
    word-break:keep-all;hyphens:none;}}
.hl em{{color:white;font-style:italic;}}
.bar{{width:72px;height:6px;background:{DARK_NAVY};border-radius:3px;margin-bottom:28px;opacity:0.35;}}
.sub{{font-family:'DM Sans';font-weight:600;font-size:27px;color:{DARK_NAVY};
    line-height:1.45;opacity:0.65;max-width:700px;}}
.badge{{position:absolute;top:44px;right:44px;background:{DARK_NAVY};color:white;
    padding:12px 28px;border-radius:50px;font-family:Inter;font-weight:700;
    font-size:14px;letter-spacing:2px;text-transform:uppercase;z-index:20;}}
.hint{{position:absolute;bottom:44px;left:56px;font-family:Inter;font-weight:700;
    font-size:20px;color:{DARK_NAVY};opacity:0.35;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_color()}
<div class="ghost">AC</div>
<div class="badge">AC Guide</div>
<div class="col">
  <div class="kicker">Beyond the interview</div>
  <div class="hl">Assessment<br>centres.<br><em>Decoded.</em></div>
  <div class="bar"></div>
  <div class="sub">What assessors actually look for - at each stage. A slide at a time.</div>
</div>
<div class="hint">Swipe for the playbook &#8594;</div>
{_spark(22,260,840,DARK_NAVY,0.1)}
{_spark(14,440,780,"white",0.2)}
{_spark(18,180,900,DARK_NAVY,0.07)}
</div></body></html>"""
    _render(html, out)


# ── Slide 2: Typical AC day — 6 timed blocks ─────────────────────────────────
def _slide2(out):
    f = _fonts()
    blocks = [
        (AMBER,    "09:00",       "Briefing + introductions",   "Overview of the day and assessor introductions"),
        (CORAL,    "09:30 - 60m", "Group exercise",             "Highest weighting - assessed on collaboration"),
        (PURPLE,   "11:00 - 30m", "Written test / e-tray",      "Prioritisation under time pressure"),
        (MINT,     "12:00",       "Lunch + social",             "Still being assessed - every interaction counts"),
        (DEEP_BLUE,"13:00 - 45m", "Case study / presentation",  "Structured problem-solving and communication"),
        (AMBER,    "14:30 - 45m", "Competency interview",       "STAR-format questions with senior assessors"),
    ]
    rows = ""
    for bg, time, name, desc in blocks:
        rows += f"""
<div style="display:flex;align-items:stretch;border-bottom:2px solid rgba(255,255,255,0.07);">
  <div style="width:6px;flex-shrink:0;background:{bg};"></div>
  <div style="width:190px;flex-shrink:0;padding:16px 20px;display:flex;align-items:center;
              border-right:2px solid rgba(255,255,255,0.06);">
    <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{AMBER};line-height:1.2;">{time}</div>
  </div>
  <div style="flex:1;padding:16px 26px;">
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:white;
                margin-bottom:4px;word-break:keep-all;hyphens:none;">{name}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:20px;
                color:rgba(255,255,255,0.5);line-height:1.3;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;padding:44px 50px;}}
{GRAIN}
.header{{padding-left:72px;margin-bottom:28px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{CORAL};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{CORAL};font-style:italic;}}
.table{{flex:1;display:flex;flex-direction:column;justify-content:space-between;
    background:rgba(255,255,255,0.03);border-radius:16px;overflow:hidden;
    border:2px solid rgba(255,255,255,0.07);}}
.note{{position:absolute;bottom:44px;right:50px;font-family:'DM Sans';font-weight:600;
    font-size:18px;color:rgba(255,255,255,0.22);}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div class="header">
  <div class="kicker">Typical AC day</div>
  <div class="hl">6 stages. One day.<br>Every one <em>scored.</em></div>
</div>
<div class="table">{rows}</div>
<div class="note">Lunch counts too.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: Group exercise — 4 things assessors score ────────────────────────
def _slide3(out):
    f = _fonts()
    items = [
        (CORAL,   "Listen actively",          "Build on what others say before adding your own point."),
        (AMBER,   "Lead without dominating",   "Move the group forward - don't take over the conversation."),
        (MINT,    "Manage conflict calmly",    "Disagree with the idea, not the person. Always."),
        (PURPLE,  "Watch the clock",           "Help the group reach a conclusion within the time given."),
    ]
    cards = ""
    for color, title, desc in items:
        cards += f"""
<div style="display:flex;align-items:stretch;gap:0;background:rgba(255,255,255,0.04);
            border-radius:14px;overflow:hidden;border:2px solid rgba(255,255,255,0.07);">
  <div style="width:10px;flex-shrink:0;background:{color};"></div>
  <div style="padding:24px 28px;flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:30px;color:white;
                margin-bottom:8px;word-break:keep-all;hyphens:none;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;
                color:rgba(255,255,255,0.55);line-height:1.35;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:0;}}
{GRAIN}
.bg-num{{position:absolute;right:-20px;top:-40px;font-family:Inter;font-weight:700;
    font-size:520px;color:rgba(255,107,107,0.05);line-height:1;z-index:1;pointer-events:none;}}
.header{{padding-left:72px;margin-bottom:28px;flex-shrink:0;z-index:5;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{CORAL};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{CORAL};font-style:italic;}}
.cards{{flex:1;display:flex;flex-direction:column;justify-content:space-between;gap:12px;z-index:5;}}
.rule{{flex-shrink:0;margin-top:16px;background:rgba(255,107,107,0.1);
    border:2px solid {CORAL};border-radius:12px;padding:16px 22px;
    font-family:Inter;font-weight:700;font-size:20px;color:{CORAL};z-index:5;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="bg-num">4</div>
{_num_badge(3)}
<div class="header">
  <div class="kicker">Group exercise</div>
  <div class="hl">4 things assessors<br>are <em>actually</em> scoring</div>
</div>
<div class="cards">{cards}</div>
<div class="rule">The mistake: talking the most rarely earns the highest score. Contributing clearly does.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: SCOPE method — full CORAL bg, dark cards ────────────────────────
def _slide4(out):
    f = _fonts()
    steps = [
        ("S", "Situation",  "Restate the problem in your own words. Show you understood it."),
        ("C", "Context",    "Identify key constraints - time, budget, stakeholders, risk."),
        ("O", "Options",    "Generate 3 options minimum. Don't jump to a solution early."),
        ("P", "Pick one",   "Choose one option and defend it clearly. Be decisive."),
        ("E", "Evidence",   "Back your choice with data, examples, or logical inference."),
    ]
    cards = ""
    for letter, word, desc in steps:
        cards += f"""
<div style="display:flex;align-items:center;gap:0;background:{DARK_NAVY};
            border-radius:14px;overflow:hidden;border:3px solid {DARK_NAVY};
            box-shadow:5px 5px 0 rgba(0,0,0,0.35);">
  <div style="width:80px;flex-shrink:0;background:{CORAL};display:flex;align-items:center;
              justify-content:center;align-self:stretch;">
    <div style="font-family:Inter;font-weight:700;font-size:38px;color:white;">{letter}</div>
  </div>
  <div style="padding:18px 26px;flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:white;margin-bottom:5px;">{word}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:21px;
                color:rgba(255,255,255,0.55);line-height:1.35;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;background:{CORAL};
    display:flex;flex-direction:column;padding:50px;gap:0;}}
{GRAIN_DARK}
.badge{{position:absolute;top:44px;right:44px;background:{DARK_NAVY};color:white;
    padding:12px 26px;border-radius:50px;font-family:Inter;font-weight:700;
    font-size:14px;letter-spacing:2px;text-transform:uppercase;z-index:20;}}
.hl{{font-family:Inter;font-weight:700;font-size:86px;line-height:0.95;
    color:{DARK_NAVY};letter-spacing:-5px;word-break:keep-all;hyphens:none;
    margin-bottom:14px;margin-top:76px;}}
.sub{{font-family:'DM Sans';font-weight:700;font-size:23px;
    color:rgba(22,45,74,0.6);margin-bottom:24px;line-height:1.4;}}
.cards{{display:flex;flex-direction:column;gap:10px;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4, bg=DARK_NAVY, fg="white")}
<div class="badge">For case studies</div>
<div class="hl">The SCOPE<br>method.</div>
<div class="sub">One structured approach beats five scattered points every time.</div>
<div class="cards">{cards}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: Competency interviews — STAR ─────────────────────────────────────
def _slide5(out):
    f = _fonts()
    star = [
        ("S", "Situation", CORAL,    "Set the scene. One or two sentences max - don't over-explain."),
        ("T", "Task",      AMBER,    "What was your specific role or responsibility in this situation?"),
        ("A", "Action",    MINT,     "What did YOU do? Use 'I' not 'we'. Detail the steps you took."),
        ("R", "Result",    PURPLE,   "What happened? Quantify the outcome wherever you can."),
    ]
    rows = ""
    for letter, word, color, tip in star:
        rows += f"""
<div style="display:flex;align-items:center;gap:0;padding:18px 0;
            border-bottom:2px solid rgba(255,255,255,0.06);">
  <div style="width:70px;height:70px;border-radius:50%;background:{color};flex-shrink:0;
              display:flex;align-items:center;justify-content:center;
              border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};
              font-family:Inter;font-weight:700;font-size:28px;color:{DARK_NAVY};">{letter}</div>
  <div style="flex:1;padding-left:24px;">
    <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;margin-bottom:5px;">{word}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:23px;
                color:rgba(255,255,255,0.55);line-height:1.3;">{tip}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:0;}}
{GRAIN}
.header{{padding-left:72px;margin-bottom:24px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{CORAL};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{CORAL};font-style:italic;}}
.rows{{flex:1;display:flex;flex-direction:column;justify-content:space-around;}}
.rule{{flex-shrink:0;margin-top:16px;background:{CORAL};border-radius:12px;
    padding:16px 22px;font-family:Inter;font-weight:700;font-size:20px;color:white;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(5)}
<div class="header">
  <div class="kicker">Competency interview</div>
  <div class="hl">STAR in <em>practice</em></div>
</div>
<div class="rows">{rows}</div>
<div class="rule">Prepare 6-8 stories. One story can answer multiple questions if you frame it right.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: Written tests + e-trays — 2x2 bento ────────────────────────────
def _slide6(out):
    f = _fonts()
    tips = [
        (CORAL,    "white",   "Read the brief first",          "Understand the full scenario before touching any item. 60 seconds of reading saves 10 minutes of wrong work."),
        (AMBER,    DARK_NAVY, "You won't finish.\nThat's the point.", "Work high-impact items first. Incomplete with clear reasoning scores higher than rushed completions."),
        (PURPLE,   "white",   "Triage,\ndon't process",        "Label every item: urgent, delegate, defer, or ignore. Prioritise before you act."),
        (MINT,     DARK_NAVY, "Show your thinking",            "Assessors score your reasoning, not just the outcome. Write brief notes on why you chose each action."),
    ]
    chips = ""
    for bg, fg, name, desc in tips:
        name_html = name.replace("\n", "<br>")
        chips += f"""
<div style="flex:1 1 calc(50% - 10px);background:{bg};
            border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
            border-radius:18px;padding:26px 28px;display:flex;flex-direction:column;gap:10px;">
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:{fg};
              word-break:keep-all;hyphens:none;line-height:1.15;">{name_html}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:21px;
              color:{'rgba(0,0,0,0.62)' if fg==DARK_NAVY else 'rgba(255,255,255,0.75)'};
              line-height:1.4;">{desc}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:20px;}}
{GRAIN}
.header{{padding-left:72px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{CORAL};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{CORAL};font-style:italic;}}
.grid{{display:flex;flex-wrap:wrap;gap:14px;flex:1;}}
.foot{{font-family:'DM Sans';font-weight:700;font-size:18px;
    color:rgba(255,255,255,0.22);flex-shrink:0;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6)}
<div class="header">
  <div class="kicker">Written tests + e-trays</div>
  <div class="hl">How to score well when<br>time runs <em>out</em></div>
</div>
<div class="grid">{chips}</div>
<div class="foot">The test is designed so no one finishes. You are scored on what you prioritise.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA — pre-AC checklist, CORAL arch, OFF_WHITE bg ────────────────
def _slide7(out, photo_path):
    f = _fonts()
    arch = ""
    if photo_path:
        ps = _src(photo_path)
        arch = f"""
<div style="position:absolute;bottom:0;right:0;width:460px;height:610px;
            background:{CORAL};border-radius:230px 230px 0 0;z-index:5;"></div>
<div style="position:absolute;bottom:0;right:0;width:500px;height:700px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.15));overflow:hidden;">
  <img src="{ps}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""

    checklist = [
        "Research the company's grad scheme structure",
        "Prepare 6-8 STAR stories covering different skills",
        "Know your CV cold - every bullet",
        "Charge your laptop the night before",
        "Eat a proper meal before you go",
    ]
    items_html = "".join(
        f'<div style="display:flex;align-items:center;gap:14px;">'
        f'<div style="width:28px;height:28px;border-radius:50%;background:{CORAL};flex-shrink:0;'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-family:Inter;font-weight:700;font-size:14px;color:white;">&#10003;</div>'
        f'<span style="font-family:\'DM Sans\';font-weight:600;font-size:20px;color:{DARK_NAVY};">{item}</span>'
        f'</div>'
        for item in checklist
    )

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{OFF_WHITE};}}
.col{{position:absolute;top:0;left:50px;right:520px;bottom:0;
      display:flex;flex-direction:column;justify-content:center;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{DEEP_BLUE};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;}}
.hl{{font-family:Inter;font-weight:700;font-size:68px;line-height:1.0;
    color:{DARK_NAVY};letter-spacing:-4px;margin-bottom:14px;
    word-break:keep-all;hyphens:none;}}
.hl em{{color:{CORAL};font-style:italic;}}
.sub{{font-family:'DM Sans';font-weight:500;font-size:20px;
    color:rgba(22,45,74,0.5);line-height:1.5;margin-bottom:26px;}}
.checklist{{display:flex;flex-direction:column;gap:14px;margin-bottom:30px;}}
.cta{{display:inline-flex;align-items:center;gap:14px;background:{DARK_NAVY};
    color:white;padding:18px 30px;border-radius:50px;
    border:3px solid {DARK_NAVY};box-shadow:6px 6px 0 {CORAL};
    font-family:Inter;font-weight:700;font-size:19px;width:fit-content;}}
.cta-arrow{{width:38px;height:38px;border-radius:50%;background:{CORAL};flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    font-size:18px;color:white;font-weight:700;}}
</style></head><body><div class="c">
{arch}
{_logo_color()}
<div class="col">
  <div class="kicker">Pre-AC checklist</div>
  <div class="hl">Show up<br><em>ready.</em></div>
  <div class="sub">5 things to do before the day.</div>
  <div class="checklist">{items_html}</div>
  <div class="cta">
    Find roles at internwise.co.uk
    <div class="cta-arrow">&#8594;</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── generate ──────────────────────────────────────────────────────────────────
def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Assessment Centres Carousel (Week 5, Day 1) v2...")
    _load_logos()

    CACHE_DIR = os.path.join(BASE_DIR, "assets", "pexels_cache")
    photos = {
        "a": os.path.join(CACHE_DIR, "e5fd45321c1a_nobg.png"),  # Black male, studio laptop
    }
    for key, path in photos.items():
        print(f"    ok {key}: {path}" if os.path.exists(path) else f"    ! {key} missing: {path}")

    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photos.get("a"))
    print("Done - assessment centres v2 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week5/d1-assessment")
