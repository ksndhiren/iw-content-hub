"""
Internwise - Video Interview Mastery (Week 7, Day 1)
Trendy: Duotone person photo, chrome-gradient headline, rotated 'HOT TAKE' sticker,
hand-drawn scribble arrow. Y2K-flavored hook. 7 slides.
Accent: HOT_PINK + CHROME.
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

CHROME_CSS = (
    "background:linear-gradient(180deg,#F5F5F5 0%,#B8B8B8 40%,#E8E8E8 55%,#7C7C7C 90%);"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;"
    "filter:drop-shadow(3px 3px 0 rgba(0,0,0,0.35));"
)

# rotated sticker with border+shadow
def _sticker(text, bg, fg, rot=-6, top=None, left=None, right=None):
    pos = f"top:{top};" if top else ""
    pos += f"left:{left};" if left else ""
    pos += f"right:{right};" if right else ""
    return (f'<div style="position:absolute;{pos}background:{bg};color:{fg};'
            f'padding:14px 22px;border:3px solid {DARK_NAVY};border-radius:14px;'
            f'box-shadow:5px 5px 0 {DARK_NAVY};font-family:Inter;font-weight:700;'
            f'font-size:22px;letter-spacing:2px;text-transform:uppercase;'
            f'transform:rotate({rot}deg);z-index:35;">{text}</div>')

# hand-drawn scribble arrow SVG
SCRIBBLE_ARROW = """<svg width="180" height="120" viewBox="0 0 180 120" xmlns="http://www.w3.org/2000/svg">
  <path d="M20,20 Q40,10 60,25 T110,35 T160,55" stroke="#162d4a" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M155,45 L165,58 L150,62" stroke="#162d4a" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

def _checklist(items, dot_bg, dot_fg, text_color):
    svg = f'<svg width="11" height="9" viewBox="0 0 11 9"><polyline points="1,4.5 4,7.5 10,1" stroke="{dot_fg}" stroke-width="2" fill="none"/></svg>'
    rows = ""
    for t in items:
        rows += (f'<div style="display:flex;align-items:center;gap:12px;">'
                 f'<div style="width:22px;height:22px;border-radius:50%;background:{dot_bg};'
                 f'display:flex;align-items:center;justify-content:center;flex-shrink:0;">{svg}</div>'
                 f'<div style="font-family:DM Sans,sans-serif;font-weight:600;font-size:28px;color:{text_color};">{t}</div></div>')
    return rows

def _logo_white(top=44, left=None, right=None):
    p = f"left:{left}px;" if left else f"right:{right}px;" if right else "left:44px;"
    return f'<img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:{top}px;{p}height:62px;z-index:25;">'
def _logo_color(top=44, left=None, right=None):
    p = f"left:{left}px;" if left else f"right:{right}px;" if right else "left:44px;"
    return f'<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:{top}px;{p}height:62px;z-index:25;">'

def _num_badge(n, bg=HOT_PINK, fg="white"):
    return f'<div style="position:absolute;top:44px;left:44px;width:54px;height:54px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};border:3px solid {DARK_NAVY};box-shadow:3px 3px 0 {DARK_NAVY};z-index:25;">{n}</div>'

def _kicker(text, color=HOT_PINK):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">{text}</div>'


# ─── Slide 1: Hook — duotone person, chrome headline, sticker ───────────────
def _slide1(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;}}
{GRAIN}
.duotone{{filter:brightness(0.9) contrast(1.05) sepia(1) hue-rotate(300deg) saturate(4);}}
</style></head><body><div class="c">
<div class="grain"></div>
<!-- Duotone photo bottom-right -->
<div style="position:absolute;bottom:0;right:0;width:640px;height:820px;overflow:hidden;z-index:5;">
  <div style="position:absolute;inset:0;background:{HOT_PINK};z-index:1;"></div>
  <img src="{photo_src}" class="duotone" style="position:absolute;bottom:0;right:-60px;height:820px;object-fit:contain;z-index:2;mix-blend-mode:multiply;">
</div>
<!-- Logo -->
{_logo_white(top=44, left=44)}
<!-- Sticker HOT TAKE -->
{_sticker("HOT TAKE", LIME, DARK_NAVY, rot=-8, top="52px", right="60px")}
<!-- Headline -->
<div style="position:absolute;top:180px;left:50px;z-index:20;max-width:640px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{LIME};
               text-transform:uppercase;letter-spacing:4px;margin-bottom:22px;">Video interviews /01</div>
  <div style="font-family:Inter;font-weight:700;font-size:120px;line-height:0.92;
               letter-spacing:-6px;word-break:keep-all;hyphens:none;{CHROME_CSS}">
    ON<br>CAMERA.
  </div>
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:62px;
               line-height:0.95;color:white;letter-spacing:-2px;margin-top:6px;
               word-break:keep-all;hyphens:none;">
    <span style="color:{HOT_PINK};">90%</span> of first<br>rounds. Now.
  </div>
</div>
<!-- Scribble arrow pointing at person -->
<div style="position:absolute;bottom:280px;left:340px;transform:rotate(15deg);z-index:22;filter:invert(1);">{SCRIBBLE_ARROW}</div>
<!-- Sticker bottom-left -->
{_sticker("SAVE THIS", HOT_PINK, "white", rot=4, top="880px", left="60px")}
<div style="position:absolute;bottom:44px;right:60px;font-family:'DM Sans';
             font-weight:500;font-size:20px;color:rgba(255,255,255,0.5);z-index:20;">SWIPE →</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 2: The Data ───────────────────────────────────────────────────────
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
  {_kicker("THE DATA", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Recruiters decide in <em style="color:{HOT_PINK};font-style:italic;">7 seconds.</em>
  </div>
</div>
<div style="flex:1;display:flex;gap:22px;margin-top:38px;position:relative;z-index:5;">
  <div style="flex:1;background:rgba(255,61,138,0.12);border:3px solid {HOT_PINK};border-radius:20px;
               padding:34px 28px;box-shadow:6px 6px 0 {HOT_PINK};">
    <div style="font-family:Inter;font-weight:700;font-size:88px;color:{HOT_PINK};letter-spacing:-4px;line-height:1;">90%</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:white;margin-top:20px;line-height:1.35;">
      of graduate first-round interviews are now conducted on video.
    </div>
  </div>
  <div style="flex:1;background:rgba(212,255,61,0.12);border:3px solid {LIME};border-radius:20px;
               padding:34px 28px;box-shadow:6px 6px 0 {LIME};">
    <div style="font-family:Inter;font-weight:700;font-size:88px;color:{LIME};letter-spacing:-4px;line-height:1;">7s</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:white;margin-top:20px;line-height:1.35;">
      is how long it takes an interviewer to form their first impression.
    </div>
  </div>
  <div style="flex:1;background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.3);border-radius:20px;
               padding:34px 28px;box-shadow:6px 6px 0 rgba(255,255,255,0.15);">
    <div style="font-family:Inter;font-weight:700;font-size:88px;color:white;letter-spacing:-4px;line-height:1;">55%</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:white;margin-top:20px;line-height:1.35;">
      of that impression comes from body language and setting - not what you say.
    </div>
  </div>
</div>
<div style="flex-shrink:0;margin-top:20px;font-family:'DM Sans';font-weight:400;font-size:20px;
             color:rgba(255,255,255,0.5);position:relative;z-index:5;text-align:right;">Sources: LinkedIn Talent Report 2026, Harvard Interview Study</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 3: The Setup Checklist ────────────────────────────────────────────
def _slide3(out):
    f = _fonts()
    items = [
        ("Camera at eye level",     "Not below - stack books under the laptop."),
        ("Light in front of you",   "Never a window behind you. It becomes a silhouette."),
        ("Neutral background",      "Plain wall > messy room. If unavoidable, blur it."),
        ("Wired connection",        "Ethernet if you can. WiFi drops during your best answer."),
        ("Headphones in",           "Wired earbuds. No echo. No AirPods dying mid-round."),
    ]
    rows = ""
    for i, (title, sub) in enumerate(items):
        rows += f"""<div style="display:flex;align-items:flex-start;gap:20px;padding:18px 0;
                  border-bottom:2px dashed rgba(255,255,255,0.12);">
  <div style="width:44px;height:44px;background:{LIME};color:{DARK_NAVY};border:3px solid {DARK_NAVY};
               border-radius:14px;box-shadow:3px 3px 0 {DARK_NAVY};display:flex;align-items:center;
               justify-content:center;font-family:Inter;font-weight:700;font-size:22px;flex-shrink:0;">{i+1}</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;letter-spacing:-0.5px;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:rgba(255,255,255,0.65);
                 margin-top:4px;">{sub}</div>
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
{_num_badge(3)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE SETUP", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    The room does <em style="color:{HOT_PINK};font-style:italic;">half the work.</em>
  </div>
</div>
<div style="flex:1;margin-top:24px;position:relative;z-index:5;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 4: First 60 Seconds ───────────────────────────────────────────────
def _slide4(out):
    f = _fonts()
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
  {_kicker("THE OPENING", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Your first <em style="color:{HOT_PINK};font-style:italic;">60 seconds.</em>
  </div>
</div>
<div style="flex:1;margin-top:32px;display:flex;flex-direction:column;gap:18px;position:relative;z-index:5;">
  <div style="background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.2);border-radius:16px;padding:24px 28px;">
    <div style="display:flex;align-items:center;gap:16px;">
      <div style="font-family:Inter;font-weight:700;font-size:36px;color:{LIME};min-width:110px;">0-10s</div>
      <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;">Smile before you unmute.</div>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:rgba(255,255,255,0.65);margin-top:8px;padding-left:126px;line-height:1.4;">
      They see you for 3 seconds before you speak. Make them count.
    </div>
  </div>
  <div style="background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.2);border-radius:16px;padding:24px 28px;">
    <div style="display:flex;align-items:center;gap:16px;">
      <div style="font-family:Inter;font-weight:700;font-size:36px;color:{LIME};min-width:110px;">10-30s</div>
      <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;">Thank them by name.</div>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:rgba(255,255,255,0.65);margin-top:8px;padding-left:126px;line-height:1.4;">
      'Thanks so much for making time today, [Sarah].' Warm. Confident. Human.
    </div>
  </div>
  <div style="background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.2);border-radius:16px;padding:24px 28px;">
    <div style="display:flex;align-items:center;gap:16px;">
      <div style="font-family:Inter;font-weight:700;font-size:36px;color:{LIME};min-width:110px;">30-60s</div>
      <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;">One line about the company.</div>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:rgba(255,255,255,0.65);margin-top:8px;padding-left:126px;line-height:1.4;">
      Reference their recent launch, campaign, or announcement. Shows you did the work.
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 5: Body Language ──────────────────────────────────────────────────
def _slide5(out):
    f = _fonts()
    dos = ["Look at the CAMERA, not the screen", "Nod slowly when they speak", "Keep hands visible", "Lean 5cm forward when engaged"]
    donts = ["Reading from notes on screen", "Fidgeting with hair or pens", "Cross-armed defensive posture", "Looking at your own tile"]
    def rows(items, color, symbol):
        r = ""
        for t in items:
            r += (f'<div style="display:flex;align-items:flex-start;gap:12px;padding:10px 0;">'
                  f'<div style="width:26px;height:26px;border-radius:50%;background:{color};color:{DARK_NAVY};'
                  f'display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;'
                  f'font-size:18px;flex-shrink:0;">{symbol}</div>'
                  f'<div style="font-family:DM Sans,sans-serif;font-weight:500;font-size:22px;color:white;line-height:1.35;">{t}</div></div>')
        return r
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
  {_kicker("BODY LANGUAGE", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    They watch <em style="color:{HOT_PINK};font-style:italic;">how</em> you listen.
  </div>
</div>
<div style="flex:1;margin-top:32px;display:flex;gap:24px;position:relative;z-index:5;">
  <div style="flex:1;background:rgba(212,255,61,0.10);border:3px solid {LIME};border-radius:16px;padding:28px;
               box-shadow:5px 5px 0 {LIME};">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{LIME};letter-spacing:2px;
                 text-transform:uppercase;margin-bottom:14px;">Do</div>
    {rows(dos, LIME, "✓")}
  </div>
  <div style="flex:1;background:rgba(255,61,138,0.10);border:3px solid {HOT_PINK};border-radius:16px;padding:28px;
               box-shadow:5px 5px 0 {HOT_PINK};">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{HOT_PINK};letter-spacing:2px;
                 text-transform:uppercase;margin-bottom:14px;">Don't</div>
    {rows(donts, HOT_PINK, "×")}
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 6: The Tech Rescue ────────────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    scenarios = [
        ("If they FREEZE",       "Stay still. Smile. Wait 10 seconds. Don't repeat yourself yet."),
        ("If YOU freeze",        "Turn camera off, back on. Type 'Sorry, brief blip - shall I continue?' in chat."),
        ("If audio dies",        "Switch to phone dial-in immediately. Don't scramble with settings."),
        ("If a housemate walks in", "Pause. 'One moment please.' Handle it. Return calm. It happens."),
    ]
    rows = ""
    for i, (title, action) in enumerate(scenarios):
        rows += f"""<div style="background:rgba(255,255,255,0.06);border:3px solid rgba(255,255,255,0.2);
             border-radius:18px;padding:22px 26px;">
  <div style="font-family:Inter;font-weight:700;font-size:22px;color:{HOT_PINK};letter-spacing:2px;
               text-transform:uppercase;">{title}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:white;margin-top:10px;line-height:1.4;">{action}</div>
</div>"""
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
  {_kicker("WHEN IT GOES WRONG", LIME)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Tech dies. <em style="color:{HOT_PINK};font-style:italic;">Composure wins.</em>
  </div>
</div>
<div style="flex:1;margin-top:28px;display:grid;grid-template-columns:1fr 1fr;gap:20px;position:relative;z-index:5;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 7: CTA — Duotone person + CTA ─────────────────────────────────────
def _slide7(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;}}
{GRAIN_DARK}
.duotone{{filter:brightness(0.95) contrast(1.05) sepia(1) hue-rotate(300deg) saturate(4);}}
</style></head><body><div class="c">
<div class="grain"></div>
<!-- duotone person right - pink block cropped narrower so it doesn't sit behind "again" -->
<div style="position:absolute;bottom:0;right:0;width:400px;height:820px;overflow:hidden;z-index:5;">
  <div style="position:absolute;inset:0;background:{HOT_PINK};z-index:1;"></div>
  <img src="{photo_src}" class="duotone" style="position:absolute;bottom:0;right:-90px;height:820px;object-fit:contain;z-index:2;mix-blend-mode:multiply;">
</div>
{_logo_color(top=44, left=44)}
{_sticker("READY?", LIME, DARK_NAVY, rot=-6, top="60px", right="70px")}
<div style="position:absolute;top:190px;left:50px;z-index:20;max-width:560px;">
  {_kicker("YOUR TURN", HOT_PINK)}
  <div style="font-family:Inter;font-weight:700;font-size:76px;line-height:0.95;color:{DARK_NAVY};
               letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    Practice. Then<br>practice <em style="color:{HOT_PINK};font-style:italic;">again.</em>
  </div>
  <div style="margin-top:26px;display:flex;flex-direction:column;gap:16px;max-width:500px;">
    {_checklist(["Record yourself answering 3 questions","Rewatch on mute - is your body open?","Do a full run 24h before the real thing","Get roles you actually want to interview for"], HOT_PINK, "white", DARK_NAVY)}
  </div>
  <div style="margin-top:36px;display:inline-flex;align-items:center;gap:12px;background:{DARK_NAVY};
               color:white;padding:18px 30px;border-radius:60px;font-family:Inter;
               font-weight:700;font-size:24px;border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {HOT_PINK};">
    Find roles at internwise.co.uk &#8594;
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Video Interview Mastery (Week 7, Day 1)...")
    _load_logos()
    used = get_used_hashes()
    photo1 = get_cutout_unique(
        "young professional headset laptop confident portrait studio white background",
        orientation="portrait", extra_exclude=used
    )
    h1 = os.path.basename(photo1).replace("_nobg.png", "")
    used |= {h1}
    photo7 = get_cutout_unique(
        "young woman professional smiling confident portrait studio white background",
        orientation="portrait", extra_exclude=used
    )
    h7 = os.path.basename(photo7).replace("_nobg.png", "")

    _slide1(os.path.join(campaign_dir, "slide_1.png"), photo1)
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photo7)

    register_used_hashes([h1, h7], "week7/d1-videointerview", "week7")
    register_design("duotone_chrome_hottake_sticker", "week7/d1-videointerview", "week7")
    print("Done - video interview complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week7/d1-videointerview")
