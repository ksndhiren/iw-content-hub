"""
Internwise - Write a Cover Letter That Gets Read (Week 5, Day 3) - v2
7-slide carousel. PURPLE accent, Gen Z style.
Hook (slide 1): DARK_NAVY bg, giant ghost "8s", person floating free (no arch) — unique.
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

LOGO_W = None
LOGO_C = None
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

def _num_badge(n, bg=PURPLE, fg="white"):
    return f'<div style="position:absolute;top:44px;left:44px;width:56px;height:56px;border-radius:50%;background:{bg};border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:24px;color:{fg};z-index:25;">{n}</div>'


# ── Slide 1: Hook — DARK_NAVY + giant ghost "8s" + person floating, no arch ──
def _slide1(out, photo_src):
    f = _fonts()
    person_html = ""
    if photo_src:
        person_html = f"""
<div style="position:absolute;bottom:0;right:0;width:480px;height:720px;
            z-index:10;filter:drop-shadow(0 20px 50px rgba(0,0,0,0.5));">
  <img src="{photo_src}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1e3560 100%);}}
{GRAIN}
.ghost{{position:absolute;right:-60px;top:50%;transform:translateY(-52%);
    font-family:Inter;font-weight:700;font-size:660px;color:{PURPLE};
    opacity:0.07;line-height:1;z-index:3;pointer-events:none;letter-spacing:-30px;}}
.col{{position:absolute;top:0;left:50px;right:530px;bottom:0;
      display:flex;flex-direction:column;justify-content:center;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:18px;color:{PURPLE};
    text-transform:uppercase;letter-spacing:4px;margin-bottom:20px;}}
.hl{{font-family:Inter;font-weight:700;font-size:80px;line-height:1.0;
    color:white;letter-spacing:-4px;margin-bottom:26px;
    word-break:keep-all;hyphens:none;}}
.hl em{{color:{PURPLE};font-style:italic;}}
.bar{{width:72px;height:5px;background:{PURPLE};border-radius:3px;margin-bottom:24px;}}
.sub{{font-family:'DM Sans';font-weight:500;font-size:26px;
    color:rgba(255,255,255,0.55);line-height:1.5;}}
.badge{{position:absolute;top:44px;right:44px;background:{PURPLE};color:white;
    padding:12px 28px;border-radius:50px;font-family:Inter;font-weight:700;
    font-size:14px;letter-spacing:2px;text-transform:uppercase;
    border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};z-index:20;}}
.hint{{position:absolute;bottom:44px;left:50px;font-family:Inter;font-weight:700;
    font-size:20px;color:rgba(255,255,255,0.3);z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{person_html}
{_logo_white()}
<div class="ghost">8s</div>
<div class="badge">Cover letter guide</div>
<div class="col">
  <div class="kicker">Write one worth reading</div>
  <div class="hl">Your cover<br>letter has<br><em>8 seconds.</em></div>
  <div class="bar"></div>
  <div class="sub">Here's how to make<br>every word count.</div>
</div>
<div class="hint">Swipe for the framework &#8594;</div>
{_spark(18,280,430,PURPLE,0.3)}
{_spark(12,460,400,"white",0.12)}
</div></body></html>"""
    _render(html, out)


# ── Slide 2: Three paragraphs structure — 3 bento cards ──────────────────────
def _slide2(out):
    f = _fonts()
    paras = [
        (PURPLE, "white",   "01", "The Hook",     "Why this role, this company, why now.\n3-4 lines max. Specific to this employer."),
        (AMBER,  DARK_NAVY, "02", "Your Value",   "3 skills from the JD paired with your best evidence.\nNo soft claims. Real examples only."),
        (MINT,   DARK_NAVY, "03", "The Close",    "Enthusiasm + availability + one confident ask.\nUnder 2 sentences. Never grovel."),
    ]
    cards = ""
    for bg, fg, num, title, body in paras:
        body_html = body.replace("\n", "<br>")
        cards += f"""
<div style="flex:1;background:{bg};border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
            border-radius:20px;padding:30px 28px;display:flex;flex-direction:column;gap:12px;">
  <div style="font-family:Inter;font-weight:700;font-size:46px;color:{'rgba(0,0,0,0.15)' if fg==DARK_NAVY else 'rgba(255,255,255,0.15)'};
              line-height:1;letter-spacing:-2px;">{num}</div>
  <div style="font-family:Inter;font-weight:700;font-size:30px;color:{fg};
              word-break:keep-all;hyphens:none;">{title}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:22px;
              color:{'rgba(0,0,0,0.6)' if fg==DARK_NAVY else 'rgba(255,255,255,0.65)'};
              line-height:1.4;">{body_html}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:24px;}}
{GRAIN}
.header{{padding-left:72px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{PURPLE};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{PURPLE};font-style:italic;}}
.cards{{flex:1;display:flex;gap:14px;}}
.rule{{flex-shrink:0;background:rgba(123,92,230,0.12);border:2px solid {PURPLE};
    border-radius:12px;padding:14px 22px;font-family:Inter;font-weight:700;
    font-size:20px;color:{PURPLE};}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div class="header">
  <div class="kicker">The structure</div>
  <div class="hl">Three paragraphs.<br><em>That's it.</em></div>
</div>
<div class="cards">{cards}</div>
<div class="rule">Golden rule: under 350 words. One full page. Always.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: Opening line — BAD vs GOOD ──────────────────────────────────────
def _slide3(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:20px;}}
{GRAIN}
.header{{padding-left:72px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{PURPLE};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{PURPLE};font-style:italic;}}
.cols{{display:flex;gap:18px;flex:1;}}
.panel{{flex:1;border-radius:20px;padding:28px;display:flex;flex-direction:column;gap:14px;}}
.bad{{background:rgba(255,107,107,0.08);border:3px solid {CORAL};}}
.good{{background:rgba(123,92,230,0.08);border:3px solid {PURPLE};}}
.plabel{{font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:3px;text-transform:uppercase;margin-bottom:4px;}}
.bad-label{{color:{CORAL};}}
.good-label{{color:{PURPLE};}}
.example{{font-family:'DM Sans';font-weight:600;font-size:22px;
    color:rgba(255,255,255,0.8);background:rgba(255,255,255,0.05);
    border-radius:10px;padding:16px 18px;font-style:italic;line-height:1.45;}}
.why{{font-family:'DM Sans';font-weight:500;font-size:21px;line-height:1.4;}}
.bad-why{{color:rgba(255,107,107,0.7);}}
.good-why{{color:rgba(255,255,255,0.45);}}
.rule{{flex-shrink:0;background:{PURPLE};border-radius:12px;padding:16px 22px;
    font-family:Inter;font-weight:700;font-size:19px;color:white;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(3)}
<div class="header">
  <div class="kicker">The opening line</div>
  <div class="hl">The only line that <em>actually matters</em></div>
</div>
<div class="cols">
  <div class="panel bad">
    <div class="plabel bad-label">&#10007; Gets skipped</div>
    <div class="example">"I am writing to apply for the graduate finance role at your company."</div>
    <div class="why bad-why">Generic. Could be sent to 100 employers. Tells the reader nothing about you or them.</div>
    <div class="example">"I have always been passionate about finance and believe I would be a great fit."</div>
    <div class="why bad-why">Passion without evidence is noise. Every applicant says this. None of them stand out.</div>
  </div>
  <div class="panel good">
    <div class="plabel good-label">&#10003; Gets read</div>
    <div class="example">"Your rotation scheme is exactly the kind of breadth I've been building toward - here's the evidence."</div>
    <div class="why good-why">Specific to this employer. Shows you've researched. Promises proof in the next paragraph.</div>
    <div class="example">"The fintech product you launched last quarter is why I want to build my career here, not just start it."</div>
    <div class="why good-why">References something real. Signals genuine interest. Opens a conversation they want to continue.</div>
  </div>
</div>
<div class="rule">Rule: if your opening line works for any other company, rewrite it.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: Evidence paragraph — match 3 JD skills ─────────────────────────
def _slide4(out):
    f = _fonts()
    skills = [
        (PURPLE,   "white",   "Skill from JD",       "Data analysis",      "Built a Python scraper tracking 2,000+ vacancies weekly for a personal project. Results published on GitHub."),
        (AMBER,    DARK_NAVY, "Skill from JD",       "Communication",      "Wrote weekly newsletter for 400 subscribers over 6 months. Open rate 42% - sector average is 21%."),
        (MINT,     DARK_NAVY, "Skill from JD",       "Project management", "Led a 4-person team event with 200 attendees, managing budget, suppliers, and comms end to end."),
    ]
    cards = ""
    for bg, fg, sublabel, skill, evidence in skills:
        cards += f"""
<div style="flex:1;background:{bg};border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
            border-radius:18px;padding:24px 26px;display:flex;flex-direction:column;gap:10px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:13px;
              color:{'rgba(0,0,0,0.4)' if fg==DARK_NAVY else 'rgba(255,255,255,0.4)'};
              text-transform:uppercase;letter-spacing:2px;">{sublabel}</div>
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:{fg};
              word-break:keep-all;hyphens:none;">{skill}</div>
  <div style="width:40px;height:3px;background:{'rgba(0,0,0,0.25)' if fg==DARK_NAVY else 'rgba(255,255,255,0.3)'};border-radius:2px;"></div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:20px;
              color:{'rgba(0,0,0,0.62)' if fg==DARK_NAVY else 'rgba(255,255,255,0.72)'};
              line-height:1.45;">{evidence}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:24px;}}
{GRAIN}
.header{{padding-left:72px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{PURPLE};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{PURPLE};font-style:italic;}}
.cards{{flex:1;display:flex;gap:14px;}}
.rule{{flex-shrink:0;background:rgba(123,92,230,0.1);border:2px solid {PURPLE};
    border-radius:12px;padding:14px 22px;font-family:Inter;font-weight:700;
    font-size:19px;color:{PURPLE};}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4)}
<div class="header">
  <div class="kicker">Paragraph 2 - your value</div>
  <div class="hl">Pick 3 skills from the JD.<br>Match each to <em>evidence.</em></div>
</div>
<div class="cards">{cards}</div>
<div class="rule">No soft claims. No "I am passionate about." Just skills matched to proof.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: The close — structure + word count rule ─────────────────────────
def _slide5(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:0;}}
{GRAIN}
.bg-num{{position:absolute;right:-30px;top:-50px;font-family:Inter;font-weight:700;
    font-size:520px;color:rgba(123,92,230,0.05);line-height:1;z-index:1;pointer-events:none;}}
.header{{padding-left:72px;margin-bottom:32px;flex-shrink:0;z-index:5;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{PURPLE};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{PURPLE};font-style:italic;}}
.sentences{{flex:1;display:flex;flex-direction:column;gap:16px;z-index:5;}}
.sent{{background:rgba(255,255,255,0.04);border-radius:14px;padding:24px 28px;
    border-left:6px solid {PURPLE};}}
.sent-num{{font-family:'DM Sans';font-weight:700;font-size:13px;color:{PURPLE};
    text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;}}
.sent-text{{font-family:'DM Sans';font-weight:600;font-size:25px;
    color:rgba(255,255,255,0.75);line-height:1.45;font-style:italic;}}
.sent-why{{font-family:'DM Sans';font-weight:500;font-size:20px;
    color:rgba(255,255,255,0.4);margin-top:6px;line-height:1.3;}}
.rule-box{{flex-shrink:0;margin-top:16px;background:{PURPLE};border-radius:12px;
    padding:18px 22px;display:flex;align-items:center;gap:16px;z-index:5;}}
.rule-num{{font-family:Inter;font-weight:700;font-size:48px;color:white;
    letter-spacing:-2px;line-height:1;}}
.rule-text{{font-family:Inter;font-weight:700;font-size:20px;color:rgba(255,255,255,0.85);
    line-height:1.3;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="bg-num">3</div>
{_num_badge(5)}
<div class="header">
  <div class="kicker">Paragraph 3 - the close</div>
  <div class="hl">Three sentences.<br>Then <em>stop.</em></div>
</div>
<div class="sentences">
  <div class="sent">
    <div class="sent-num">Sentence 1</div>
    <div class="sent-text">"This role aligns directly with the direction I am building toward because [specific reason]."</div>
    <div class="sent-why">Restate interest in one sentence. Make it specific, not effusive.</div>
  </div>
  <div class="sent">
    <div class="sent-num">Sentence 2</div>
    <div class="sent-text">"I would welcome the chance to discuss how my [X] could contribute to [Y]."</div>
    <div class="sent-why">Ask for the meeting, don't wait to be invited. Confident, not pushy.</div>
  </div>
  <div class="sent">
    <div class="sent-num">Sentence 3</div>
    <div class="sent-text">"I am available from [date] and look forward to hearing from you."</div>
    <div class="sent-why">Availability removes friction. Sign off. Nothing more.</div>
  </div>
</div>
<div class="rule-box">
  <div class="rule-num">350</div>
  <div class="rule-text">words maximum. One page. Read it aloud.<br>If it sounds stiff, rewrite the stiff parts.</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: Before / after — full comparison ────────────────────────────────
def _slide6(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:20px;}}
{GRAIN}
.header{{padding-left:72px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;color:{PURPLE};
    text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{PURPLE};font-style:italic;}}
.cols{{display:flex;gap:18px;flex:1;}}
.panel{{flex:1;border-radius:20px;padding:28px;display:flex;flex-direction:column;gap:16px;}}
.bad{{background:rgba(255,107,107,0.07);border:3px solid {CORAL};}}
.good{{background:rgba(123,92,230,0.08);border:3px solid {PURPLE};}}
.plabel{{font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:3px;text-transform:uppercase;margin-bottom:2px;}}
.bad-label{{color:{CORAL};}}
.good-label{{color:{PURPLE};}}
.letter-block{{font-family:'DM Sans';font-weight:500;font-size:19px;
    color:rgba(255,255,255,0.7);line-height:1.55;font-style:italic;
    background:rgba(255,255,255,0.04);border-radius:10px;padding:16px 18px;flex:1;}}
.verdict{{font-family:Inter;font-weight:700;font-size:17px;line-height:1.3;}}
.bad-verdict{{color:rgba(255,107,107,0.8);}}
.good-verdict{{color:rgba(123,92,230,0.9);}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6)}
<div class="header">
  <div class="kicker">Before and after</div>
  <div class="hl">The same role.<br>Two very <em>different letters.</em></div>
</div>
<div class="cols">
  <div class="panel bad">
    <div class="plabel bad-label">&#10007; Gets deleted</div>
    <div class="letter-block">I am writing to apply for the Graduate Analyst position. I have always been passionate about data and I believe my strong work ethic and eagerness to learn would make me an excellent fit for your team. I am a hardworking and dedicated individual who works well in teams.</div>
    <div class="verdict bad-verdict">No specifics. No evidence. Works for any company. Recruiter stops reading at line 2.</div>
  </div>
  <div class="panel good">
    <div class="plabel good-label">&#10003; Gets a call</div>
    <div class="letter-block">Your recent expansion into predictive analytics is exactly the space I have been building skills toward. Over the past year I built a Python pipeline tracking 2,000+ job postings weekly - the repo is live on GitHub. I want to bring that same rigour to a team that is already at the frontier of what I'm aiming for.</div>
    <div class="verdict good-verdict">Specific company reference. Concrete evidence. Live link. Ends with forward momentum.</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA — 5 checks, PURPLE arch, OFF_WHITE bg ───────────────────────
def _slide7(out, photo_path):
    f = _fonts()
    arch = ""
    if photo_path:
        ps = _src(photo_path)
        arch = f"""
<div style="position:absolute;bottom:0;right:0;width:460px;height:610px;
            background:{PURPLE};border-radius:230px 230px 0 0;z-index:5;"></div>
<div style="position:absolute;bottom:0;right:0;width:500px;height:700px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.15));overflow:hidden;">
  <img src="{ps}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""

    checks = [
        "Opening line is specific to this company",
        "Para 2 matches 3 skills from the JD",
        "Under 350 words - one page maximum",
        "Company name and role spelled correctly",
        "Read it aloud - if it sounds stiff, rewrite it",
    ]
    items_html = "".join(
        f'<div style="display:flex;align-items:center;gap:14px;">'
        f'<div style="width:28px;height:28px;border-radius:50%;background:{PURPLE};flex-shrink:0;'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-family:Inter;font-weight:700;font-size:14px;color:white;">&#10003;</div>'
        f'<span style="font-family:\'DM Sans\';font-weight:600;font-size:20px;color:{DARK_NAVY};">{item}</span>'
        f'</div>'
        for item in checks
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
.hl{{font-family:Inter;font-weight:700;font-size:62px;line-height:1.0;
    color:{DARK_NAVY};letter-spacing:-3px;margin-bottom:14px;
    word-break:keep-all;hyphens:none;}}
.hl em{{color:{PURPLE};font-style:italic;}}
.sub{{font-family:'DM Sans';font-weight:500;font-size:20px;
    color:rgba(22,45,74,0.5);line-height:1.5;margin-bottom:24px;}}
.checklist{{display:flex;flex-direction:column;gap:14px;margin-bottom:30px;}}
.cta{{display:inline-flex;align-items:center;gap:14px;background:{DARK_NAVY};
    color:white;padding:18px 30px;border-radius:50px;
    border:3px solid {DARK_NAVY};box-shadow:6px 6px 0 {PURPLE};
    font-family:Inter;font-weight:700;font-size:19px;width:fit-content;}}
.cta-arrow{{width:38px;height:38px;border-radius:50%;background:{PURPLE};flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    font-size:18px;color:white;font-weight:700;}}
</style></head><body><div class="c">
{arch}
{_logo_color()}
<div class="col">
  <div class="kicker">Before you hit send</div>
  <div class="hl">5 checks.<br>Every <em>application.</em></div>
  <div class="sub">Takes 3 minutes. Makes the difference.</div>
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
    print("Generating Cover Letter Carousel (Week 5, Day 3) v2...")
    _load_logos()

    CACHE_DIR = os.path.join(BASE_DIR, "assets", "pexels_cache")
    photos = {}

    # Slide 1: Asian woman, notebook — floating person (no arch)
    photos["hook"] = os.path.join(CACHE_DIR, "08853a424b54_nobg.png")

    # Slide 7: Fresh search for CTA person
    try:
        p = get_cutout("young mixed race woman confident smiling standing white background studio portrait", index=0, orientation="portrait")
        photos["cta"] = p
        print(f"    ok cta: {p}")
    except Exception as e:
        print(f"    ! cta failed: {e}")
        photos["cta"] = None

    for key in ["hook"]:
        path = photos[key]
        print(f"    ok {key}: {path}" if os.path.exists(path) else f"    ! {key} missing: {path}")

    _slide1(os.path.join(campaign_dir, "slide_1.png"), _src(photos.get("hook")))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photos.get("cta"))
    print("Done - cover letter carousel v2 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week5/d3-coverletter")
