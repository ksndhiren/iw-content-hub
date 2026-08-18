"""
Internwise - Side Projects That Impress (Week 5, Day 5) - v3
7-slide carousel. Gen Z: massive type, bold layouts, AMBER accent.
Slides 1,7: arch+cutout. Slides 2-6: completely different layouts from D4.
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

def _spark(s, t, l, c, o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:3;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'

def _logo_img():
    return f'<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:44px;height:72px;opacity:0.95;z-index:25;">'

def _num_badge(n, color=AMBER):
    return f'<div style="position:absolute;top:44px;left:44px;width:56px;height:56px;border-radius:50%;background:{color};border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:24px;color:{DARK_NAVY};z-index:25;">{n}</div>'


# ── Slide 1: Hook — arch+cutout, AMBER arch ───────────────────────────────────
def _slide1(out, photo_src):
    f = _fonts()
    logo = _logo_img()
    arch = ""
    if photo_src:
        arch = f"""
<div style="position:absolute;bottom:0;right:0;width:460px;height:610px;
            background:{AMBER};border-radius:230px 230px 0 0;z-index:5;"></div>
<div style="position:absolute;bottom:0;right:0;width:500px;height:700px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.35));overflow:hidden;">
  <img src="{photo_src}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1e3560 100%);}}
{GRAIN}
.badge{{position:absolute;top:44px;right:44px;background:{AMBER};color:{DARK_NAVY};
    padding:12px 28px;border-radius:50px;font-family:Inter;font-weight:700;font-size:15px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(-3deg);
    border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};z-index:20;}}
.col{{position:absolute;top:0;left:50px;right:520px;bottom:0;
      display:flex;flex-direction:column;justify-content:center;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:18px;
    color:{AMBER};text-transform:uppercase;letter-spacing:4px;margin-bottom:20px;}}
.hl{{font-family:Inter;font-weight:700;font-size:68px;line-height:1.05;
    color:white;letter-spacing:-3px;margin-bottom:26px;
    word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.bar{{width:72px;height:5px;background:{AMBER};border-radius:3px;margin-bottom:24px;}}
.sub{{font-family:'DM Sans';font-weight:500;font-size:24px;
    color:rgba(255,255,255,0.6);line-height:1.5;}}
.hint{{position:absolute;bottom:44px;left:50px;z-index:20;
    font-family:Inter;font-weight:700;font-size:20px;color:rgba(255,255,255,0.36);}}
</style></head><body><div class="c">
<div class="grain"></div>
{arch}
{logo}
<div class="badge">Portfolio guide</div>
<div class="col">
  <div class="kicker">Stand out before day 1</div>
  <div class="hl">Your degree<br>gets you in.<br>Your projects<br>get the <em>offer.</em></div>
  <div class="bar"></div>
  <div class="sub">What counts. How to<br>present it. For free.</div>
</div>
<div class="hint">Swipe for the playbook &#8594;</div>
{_spark(22,240,430,AMBER,0.4)}
{_spark(14,440,390,"white",0.15)}
</div></body></html>"""
    _render(html, out)


# ── Slide 2: What counts — giant BG number + editorial list ───────────────────
def _slide2(out):
    f = _fonts()
    items = [
        (AMBER,   "GitHub repo",        "Working code. Real README. Anyone can clone it."),
        (MINT,    "Personal website",   "Your name on a real URL with your work visible."),
        (CORAL,   "Newsletter / blog",  "Proves you write, think, and ship consistently."),
        (PURPLE,  "Case study",         "Deep analysis of a real problem. With findings."),
        (DEEP_BLUE,"App or tool",       "Built it for yourself? Ship it. That counts."),
        ("#5FA7E5","Open source PR",    "Any contribution. Even small ones signal skill."),
    ]
    rows = ""
    for bg, title, desc in items:
        rows += f"""
<div style="display:flex;align-items:center;gap:0;border-bottom:2px solid rgba(255,255,255,0.07);">
  <div style="width:16px;flex-shrink:0;height:100%;background:{bg};align-self:stretch;border-radius:4px 0 0 4px;"></div>
  <div style="display:flex;align-items:center;gap:20px;padding:16px 22px;flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;
                min-width:240px;word-break:keep-all;hyphens:none;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:27px;
                color:rgba(255,255,255,0.55);line-height:1.35;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px 44px 50px;gap:0;}}
{GRAIN}
.bg-num{{position:absolute;right:-40px;top:-60px;font-family:Inter;font-weight:700;
    font-size:560px;color:rgba(255,177,32,0.05);line-height:1;z-index:1;
    pointer-events:none;letter-spacing:-30px;}}
.header{{z-index:5;padding-left:70px;margin-bottom:24px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;}}
.hl{{font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.list{{z-index:5;flex:1;display:flex;flex-direction:column;justify-content:space-between;
    background:rgba(255,255,255,0.03);border-radius:16px;overflow:hidden;
    border:2px solid rgba(255,255,255,0.08);}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="bg-num">6</div>
{_num_badge(2)}
<div class="header">
  <div class="kicker">What actually qualifies</div>
  <div class="hl">6 things that count as a <em>project</em></div>
</div>
<div class="list">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: GitHub — full AMBER canvas, dark stacked cards ───────────────────
def _slide3(out):
    f = _fonts()
    tips = [
        ("Pin 3-6 repos",       "Your best work front and centre. Curated, not everything."),
        ("Write a real README",  "What it does. How to run it. One screenshot. 5 mins of work."),
        ("Show commit history",  "Consistent commits = consistent person. Sporadic = crammer."),
        ("Deploy it live",       "A working URL beats a description every time. Use GitHub Pages."),
    ]
    cards = ""
    for title, desc in tips:
        cards += f"""
<div style="background:{DARK_NAVY};border-radius:14px;padding:22px 26px;
            border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 rgba(0,0,0,0.4);">
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;
              margin-bottom:8px;word-break:keep-all;hyphens:none;">{title}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:20px;
              color:rgba(255,255,255,0.6);line-height:1.4;">{desc}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;background:{AMBER};
    display:flex;flex-direction:column;padding:50px;gap:0;}}
{GRAIN.replace("rgba(255,255,255,0.035)","rgba(0,0,0,0.04)")}
.badge{{position:absolute;top:44px;right:44px;background:{DARK_NAVY};color:white;
    padding:12px 26px;border-radius:50px;font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;z-index:20;}}
.hl{{font-family:Inter;font-weight:700;font-size:96px;line-height:0.95;
    color:{DARK_NAVY};letter-spacing:-6px;word-break:keep-all;hyphens:none;
    margin-bottom:16px;margin-top:80px;}}
.sub{{font-family:'DM Sans';font-weight:700;font-size:22px;
    color:rgba(22,45,74,0.6);margin-bottom:30px;line-height:1.4;}}
.cards{{display:flex;flex-direction:column;gap:12px;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(3, DARK_NAVY)}
<div class="badge">For tech &amp; data roles</div>
<div class="hl">GitHub<br>is your<br>live CV.</div>
<div class="sub">For tech and data roles, it matters more than your degree grade.</div>
<div class="cards">{cards}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: Sectors — full-width horizontal bands ────────────────────────────
def _slide4(out):
    f = _fonts()
    sectors = [
        (MINT,    DARK_NAVY, "Tech &amp; Data",   "GitHub repos · deployed apps · Kaggle notebooks · data dashboards"),
        (CORAL,   "white",   "Marketing",         "Content campaigns with metrics · newsletter subscribers · brand decks"),
        (PURPLE,  "white",   "Finance",           "Excel/Python models · stock analysis · mock pitch decks"),
        (AMBER,   DARK_NAVY, "Consulting &amp; Ops","Process maps · research reports · structured problem-solution decks"),
    ]
    bands = ""
    for bg, fg, sector, desc in sectors:
        bands += f"""
<div style="flex:1;background:{bg};display:flex;align-items:center;gap:0;
            border-bottom:3px solid {DARK_NAVY};">
  <div style="width:280px;flex-shrink:0;padding:0 36px;border-right:3px solid {DARK_NAVY};">
    <div style="font-family:Inter;font-weight:700;font-size:30px;color:{fg};
                word-break:keep-all;hyphens:none;line-height:1.1;">{sector}</div>
  </div>
  <div style="flex:1;padding:0 36px;font-family:'DM Sans';font-weight:600;font-size:26px;
              color:{'rgba(0,0,0,0.6)' if fg==DARK_NAVY else 'rgba(255,255,255,0.75)'};
              line-height:1.4;">{desc}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;}}
{GRAIN}
.header{{padding:44px 50px 24px 120px;flex-shrink:0;background:{DARK_NAVY};}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.bands{{flex:1;display:flex;flex-direction:column;border-top:3px solid {DARK_NAVY};
    border:3px solid {DARK_NAVY};}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4)}
<div class="header">
  <div class="kicker">Sector by sector</div>
  <div class="hl">What your sector <em>actually</em> wants to see</div>
</div>
<div class="bands">{bands}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: CV listing — typographic BAD vs GOOD ─────────────────────────────
def _slide5(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:20px;}}
{GRAIN}
.header{{padding-left:70px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.cols{{display:flex;gap:18px;flex:1;}}
.panel{{flex:1;border-radius:20px;padding:30px;display:flex;flex-direction:column;gap:14px;}}
.bad-panel{{background:rgba(255,107,107,0.08);border:3px solid {CORAL};}}
.good-panel{{background:rgba(255,177,32,0.08);border:3px solid {AMBER};}}
.plabel{{font-family:Inter;font-weight:700;font-size:15px;
    letter-spacing:3px;text-transform:uppercase;margin-bottom:6px;}}
.bad-label{{color:{CORAL};}}
.good-label{{color:{AMBER};}}
.cv-line{{font-family:'DM Sans';font-weight:600;font-size:24px;line-height:1.45;
    color:rgba(255,255,255,0.75);background:rgba(255,255,255,0.05);
    border-radius:10px;padding:14px 16px;font-style:italic;}}
.why{{font-family:'DM Sans';font-weight:500;font-size:22px;
    line-height:1.4;}}
.bad-why{{color:rgba(255,107,107,0.7);}}
.good-why{{color:rgba(255,255,255,0.5);}}
.rule-box{{margin-top:auto;background:{AMBER};border-radius:12px;padding:16px 20px;
    font-family:Inter;font-weight:700;font-size:19px;color:{DARK_NAVY};line-height:1.4;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(5)}
<div class="header">
  <div class="kicker">On your CV</div>
  <div class="hl">How to <em>list it</em> so it lands</div>
</div>
<div class="cols">
  <div class="panel bad-panel">
    <div class="plabel bad-label">&#10007; Doesn't work</div>
    <div class="cv-line">"Personal project — web scraping (Python)"</div>
    <div class="why bad-why">No outcome. No scale. Could be a 20-minute tutorial copy-paste.</div>
    <div class="cv-line">"Side project: mobile app"</div>
    <div class="why bad-why">No link. No numbers. No evidence it even exists.</div>
    <div class="cv-line">"Interest in machine learning"</div>
    <div class="why bad-why">An interest is not a project. Never list it this way.</div>
  </div>
  <div class="panel good-panel">
    <div class="plabel good-label">&#10003; This lands</div>
    <div class="cv-line">"Built a job board scraper (Python) tracking 2,000+ vacancies weekly — github.com/you/repo"</div>
    <div class="why good-why">Tool named. Scale shown. Link provided. Verifiable in 10 seconds.</div>
    <div class="cv-line">"iOS habit app — 400+ downloads, App Store, 3 months post-launch"</div>
    <div class="why good-why">Real number. Real outcome. Employer can check it now.</div>
    <div class="rule-box">Format: [What] ([tools]) — [result] — [link]</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: Tools — large pill/chip grid layout ──────────────────────────────
def _slide6(out):
    f = _fonts()
    tools = [
        (AMBER,    DARK_NAVY, "GitHub Pages",    "Free hosting. Your project live at yourname.github.io"),
        (MINT,     DARK_NAVY, "Notion",          "Document your work. Share as a public case study."),
        (CORAL,    "white",   "Google Colab",    "Python & data in browser. Free. Share the notebook."),
        (PURPLE,   "white",   "Canva",           "Portfolios, decks, infographics. No design skills needed."),
        (DEEP_BLUE,"white",   "Substack",        "Free newsletter. Start writing. It grows over time."),
        (DARK_NAVY,"white",   "Vercel / Render", "Deploy apps in minutes. Live URL for anything you build."),
    ]
    chips = ""
    for bg, fg, name, desc in tools:
        chips += f"""
<div style="flex:1 1 calc(50% - 10px);background:{bg};
            border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
            border-radius:18px;padding:26px 28px;display:flex;flex-direction:column;gap:10px;">
  <div style="font-family:Inter;font-weight:700;font-size:30px;color:{fg};
              word-break:keep-all;hyphens:none;">{name}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;
              color:{'rgba(0,0,0,0.62)' if fg==DARK_NAVY else 'rgba(255,255,255,0.72)'};
              line-height:1.4;">{desc}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:44px 50px;gap:22px;}}
{GRAIN}
.header{{padding-left:70px;flex-shrink:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;
    color:{AMBER};text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;}}
.hl{{font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
    color:white;letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.grid{{display:flex;flex-wrap:wrap;gap:14px;flex:1;}}
.foot{{font-family:'DM Sans';font-weight:700;font-size:19px;
    color:rgba(255,255,255,0.3);flex-shrink:0;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6)}
<div class="header">
  <div class="kicker">Zero budget needed</div>
  <div class="hl">6 free tools to <em>start today</em></div>
</div>
<div class="grid">{chips}</div>
<div class="foot">The constraint is time, not money.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA — arch+cutout, OFF_WHITE bg ─────────────────────────────────
def _slide7(out, photo_path):
    f = _fonts()
    logo = _logo_img()
    arch = ""
    if photo_path:
        photo_src = _src(photo_path)
        arch = f"""
<div style="position:absolute;bottom:0;right:0;width:460px;height:610px;
            background:{AMBER};border-radius:230px 230px 0 0;z-index:5;"></div>
<div style="position:absolute;bottom:0;right:0;width:500px;height:700px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.15));overflow:hidden;">
  <img src="{photo_src}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""

    checklist = [
        "Pick one project idea — right now",
        "Build it rough. Ship it anyway.",
        "Add the link to your CV this week",
        "Push to GitHub. Make it public.",
    ]
    items_html = "".join(
        f'<div style="display:flex;align-items:center;gap:14px;white-space:nowrap;">'
        f'<div style="width:28px;height:28px;border-radius:50%;background:{AMBER};flex-shrink:0;'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-family:Inter;font-weight:700;font-size:15px;color:{DARK_NAVY};">&#10003;</div>'
        f'<span style="font-family:\'DM Sans\';font-weight:600;font-size:20px;color:{DARK_NAVY};">{item}</span>'
        f'</div>'
        for item in checklist
    )

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{OFF_WHITE};}}
{GRAIN}
.col{{position:absolute;top:0;left:50px;right:520px;bottom:0;
      display:flex;flex-direction:column;justify-content:center;z-index:20;gap:0;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:17px;
    color:{DEEP_BLUE};text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;}}
.hl{{font-family:Inter;font-weight:700;font-size:72px;line-height:1.0;
    color:{DARK_NAVY};letter-spacing:-4px;margin-bottom:12px;
    word-break:keep-all;hyphens:none;}}
.hl em{{color:{AMBER};font-style:italic;}}
.sub{{font-family:'DM Sans';font-weight:500;font-size:20px;
    color:rgba(22,45,74,0.5);line-height:1.5;margin-bottom:28px;}}
.checklist{{display:flex;flex-direction:column;gap:14px;margin-bottom:32px;}}
.cta{{display:inline-flex;align-items:center;gap:14px;background:{DARK_NAVY};
    color:white;padding:18px 30px;border-radius:50px;
    border:3px solid {DARK_NAVY};box-shadow:6px 6px 0 {AMBER};
    font-family:Inter;font-weight:700;font-size:19px;width:fit-content;}}
.cta-arrow{{width:38px;height:38px;border-radius:50%;background:{AMBER};flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    font-size:18px;color:{DARK_NAVY};font-weight:700;}}
</style></head><body><div class="c">
<div class="grain"></div>
{arch}
{logo}
<div class="col">
  <div class="kicker">Your next move</div>
  <div class="hl">You don't<br>need it<br><em>perfect.</em><br>You need<br>it <em>live.</em></div>
  <div class="sub">One project separates you from<br>80% of applicants. Start today.</div>
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
    print("Generating Side Projects Carousel (Week 5, Day 5) v3...")
    _load_logo()

    CACHE_DIR = os.path.join(BASE_DIR, "assets", "pexels_cache")
    photos = {
        "a": os.path.join(CACHE_DIR, "2ca33be9d2f7_nobg.png"),  # red suit, laptop under arm
        "b": os.path.join(CACHE_DIR, "d03ae825fab7_nobg.png"),  # brunette in white
    }
    for key, path in photos.items():
        print(f"    ok {key}: {path}" if os.path.exists(path) else f"    ! {key} missing: {path}")

    _slide1(os.path.join(campaign_dir, "slide_1.png"), _src(photos.get("a")))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photos.get("b"))
    print("Done - side projects carousel v3 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week5/d5-sideprojects")
