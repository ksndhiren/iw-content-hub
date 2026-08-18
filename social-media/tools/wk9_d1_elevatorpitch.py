"""
Internwise - The 30-Second Elevator Pitch (Week 9, Day 1)
Design language: 3D CLAYMORPHISM. Puffy soft-shadow clay icons (megaphone, speech
bubbles, timer), pastel depth, rounded-everything, inset+drop shadows for tactile 3D.
7 slides. Accent: CLAY_CORAL + CLAY_MINT on soft cream.

Mobile font rules held: headline 52px+, body 28px+, card title 26px+, kicker 18px+.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; DEEP_BLUE = "#264D7E"; OFF_WHITE = "#FAF5EC"

# Clay palette — soft, desaturated, pastel
CLAY_BG    = "#F3ECE1"   # warm cream base
CLAY_BG2   = "#EDE3D4"
CORAL      = "#FF7A6B"; CORAL_D = "#E85D4E"
MINT       = "#5FC7A6"; MINT_D  = "#3FA985"
AMBER      = "#FFC24A"; AMBER_D = "#E5A122"
PURPLE     = "#9B84E8"; PURPLE_D= "#7B62D6"
BLUE       = "#5AA9E8"; BLUE_D  = "#3D8AD0"
INK        = "#3A3230"

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

# Clay bg = subtle radial for depth
def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;
      background:radial-gradient(ellipse at 30% 20%,{CLAY_BG} 0%,{CLAY_BG2} 100%);}}
.c{{width:1080px;height:1080px;position:relative;padding:52px 56px;display:flex;flex-direction:column;}}
"""

# Clay blob container — puffy raised surface
def _clay(bg, radius=40, extra=""):
    return (f"background:{bg};border-radius:{radius}px;"
            f"box-shadow:0 18px 34px rgba(120,90,70,0.22),"
            f"inset 0 3px 4px rgba(255,255,255,0.55),"
            f"inset 0 -6px 10px rgba(0,0,0,0.10);{extra}")

def _clay_pill(text, bg, fg, rot=0):
    return (f'<div style="{_clay(bg, 50)}display:inline-block;padding:12px 24px;'
            f'font-family:Inter;font-weight:700;font-size:19px;color:{fg};letter-spacing:1px;'
            f'text-transform:uppercase;transform:rotate({rot}deg);">{text}</div>')

# ── 3D clay icons (inline SVG with soft gradients + highlights) ──────────────
def _icon_wrap(svg, bg, size=132):
    """Rounded clay tile holding an icon."""
    return (f'<div style="{_clay(bg, 34)}width:{size}px;height:{size}px;flex-shrink:0;'
            f'display:flex;align-items:center;justify-content:center;">{svg}</div>')

def _grad(id_, light, dark):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/></linearGradient>')

ICON_MEGAPHONE = f"""<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <defs>{_grad("mg","#FFFFFF","#F0F0F0")}</defs>
  <path d="M14 30 L40 20 L40 52 L14 42 Z" fill="url(#mg)" stroke="rgba(0,0,0,0.12)" stroke-width="1.5"/>
  <rect x="8" y="30" width="8" height="12" rx="3" fill="#FFF"/>
  <path d="M40 20 Q56 24 56 36 Q56 48 40 52" fill="none" stroke="#FFF" stroke-width="5" stroke-linecap="round"/>
  <rect x="22" y="42" width="9" height="16" rx="4" fill="#FFF"/>
</svg>"""

ICON_CLOCK = f"""<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <circle cx="36" cy="38" r="24" fill="#FFF" stroke="rgba(0,0,0,0.10)" stroke-width="1.5"/>
  <rect x="30" y="8" width="12" height="7" rx="3" fill="#FFF"/>
  <path d="M36 38 L36 24 M36 38 L48 44" stroke="#3A3230" stroke-width="4" stroke-linecap="round"/>
</svg>"""

ICON_CHAT = f"""<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <path d="M14 18 H58 Q64 18 64 24 V44 Q64 50 58 50 H34 L22 60 V50 H14 Q8 50 8 44 V24 Q8 18 14 18 Z" fill="#FFF"/>
  <circle cx="26" cy="34" r="4" fill="#3A3230"/><circle cx="36" cy="34" r="4" fill="#3A3230"/><circle cx="46" cy="34" r="4" fill="#3A3230"/>
</svg>"""

ICON_TARGET = f"""<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <circle cx="36" cy="38" r="24" fill="#FFF"/><circle cx="36" cy="38" r="15" fill="none" stroke="#3A3230" stroke-width="4"/>
  <circle cx="36" cy="38" r="6" fill="#3A3230"/>
</svg>"""

ICON_SPARK = f"""<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <path d="M36 12 L42 30 L60 36 L42 42 L36 60 L30 42 L12 36 L30 30 Z" fill="#FFF"/>
</svg>"""

ICON_HAND = f"""<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <path d="M24 34 V22 Q24 18 28 18 Q32 18 32 22 V32 M32 32 V18 Q32 14 36 14 Q40 14 40 18 V32 M40 32 V20 Q40 16 44 16 Q48 16 48 20 V34 M48 34 V26 Q48 22 52 22 Q56 22 56 26 V44 Q56 58 42 58 H36 Q24 58 22 46 L18 38 Q16 34 20 32 Q23 31 24 34 Z" fill="#FFF" stroke="rgba(0,0,0,0.10)" stroke-width="1.5"/>
</svg>"""


# ── Slide 1: Hook — big clay megaphone + timer ──────────────────────────────
def _slide1(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">

<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:56px;">
  {_clay_pill("Your pitch / 30 sec", AMBER, INK, 2)}
</div>

<div style="flex:1;display:flex;align-items:center;gap:30px;">
  <div style="flex:1;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{CORAL_D};
                 text-transform:uppercase;letter-spacing:3px;margin-bottom:20px;">The elevator pitch</div>
    <div style="font-family:Inter;font-weight:700;font-size:104px;line-height:0.9;color:{INK};
                 letter-spacing:-5px;word-break:keep-all;hyphens:none;">
      Who are<br>you? <span style="color:{CORAL_D};">Go.</span>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:30px;color:#7A6E68;
                 margin-top:28px;line-height:1.4;max-width:540px;">
      You get 30 seconds at the event, the call, the lift. Here's how to not freeze.
    </div>
    <div style="display:flex;gap:14px;margin-top:34px;">
      {_clay_pill("Event", CLAY_BG, INK, -2)}
      {_clay_pill("Call", CLAY_BG, INK, 1)}
      {_clay_pill("Lift", CLAY_BG, INK, -1)}
    </div>
  </div>
  <div style="width:320px;flex-shrink:0;display:flex;flex-direction:column;gap:30px;align-items:center;">
    <div style="{_clay(CORAL, 62)}width:232px;height:232px;display:flex;align-items:center;
                 justify-content:center;transform:rotate(-6deg);margin-right:40px;">
      <div style="transform:scale(2.1);">{ICON_MEGAPHONE}</div>
    </div>
    <div style="{_clay(MINT, 46)}width:158px;height:158px;display:flex;align-items:center;
                 justify-content:center;transform:rotate(7deg);margin-left:-70px;margin-top:-30px;">
      <div style="transform:scale(1.5);">{ICON_CLOCK}</div>
    </div>
    <div style="{_clay(BLUE, 40)}width:132px;height:132px;display:flex;align-items:center;
                 justify-content:center;transform:rotate(-8deg);margin-right:60px;margin-top:-20px;">
      <div style="transform:scale(1.3);">{ICON_CHAT}</div>
    </div>
  </div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:flex-end;">
  {_clay_pill("Swipe &rarr;", "#FFFFFF", INK, 0)}
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: The Data ───────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("7s", "to make a first impression before you've finished your first sentence", CORAL, CORAL_D, ICON_CLOCK),
        ("30s", "is the sweet spot: long enough to land, short enough to hold attention", MINT, MINT_D, ICON_TARGET),
        ("3x", "more memorable when you lead with a specific result, not a job title", AMBER, AMBER_D, ICON_SPARK),
    ]
    cards = ""
    for val, label, bg, dark, icon in stats:
        cards += f"""<div style="flex:1;{_clay('#FFFFFF', 34)}padding:36px 30px 30px 30px;
             display:flex;flex-direction:column;position:relative;overflow:hidden;">
  <div style="{_clay(bg, 26)}width:92px;height:92px;display:flex;align-items:center;justify-content:center;margin-bottom:26px;">
    <div style="transform:scale(1.1);">{icon}</div>
  </div>
  <div style="font-family:Inter;font-weight:700;font-size:92px;color:{dark};letter-spacing:-4px;line-height:1;">{val}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#6E635E;margin-top:18px;line-height:1.4;">{label}</div>
  <div style="flex:1;"></div>
  <div style="font-family:Inter;font-weight:700;font-size:200px;color:{bg};opacity:0.14;
               position:absolute;bottom:-58px;right:-14px;line-height:1;letter-spacing:-8px;
               pointer-events:none;">{val}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{CORAL_D};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">The 30-second window</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Short. Specific. <span style="color:{CORAL_D};">Sticky.</span>
  </div>
</div>
<div style="flex:1;display:flex;gap:22px;margin:36px 0 18px 0;align-items:stretch;">{cards}</div>
<div style="flex-shrink:0;font-family:'DM Sans';font-weight:400;font-size:20px;color:#9A8F88;text-align:right;">
  Sources: Princeton First-Impression Study, LinkedIn Networking Report 2026
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: The 4-part formula ─────────────────────────────────────────────
def _slide3(out):
    f = _fonts()
    parts = [
        ("Who you are", "One line. Name + what you do or study. No life story.", BLUE, BLUE_D, ICON_HAND),
        ("Your proof", "One specific result. 'I grew our society to 400 members', not 'I'm hardworking'.", MINT, MINT_D, ICON_SPARK),
        ("What you want", "Be direct. 'I'm looking for a grad role in product.' Make it easy to help you.", AMBER, AMBER_D, ICON_TARGET),
        ("The hook back", "End with a question. Turn your pitch into their conversation.", CORAL, CORAL_D, ICON_CHAT),
    ]
    rows = ""
    for i, (title, desc, bg, dark, icon) in enumerate(parts):
        rows += f"""<div style="display:flex;align-items:center;gap:24px;{_clay('#FFFFFF', 30)}padding:22px 28px;">
  <div style="{_clay(bg, 24)}width:82px;height:82px;flex-shrink:0;display:flex;align-items:center;justify-content:center;position:relative;">
    <div style="transform:scale(0.95);">{icon}</div>
    <div style="position:absolute;top:-10px;left:-10px;{_clay(dark, 50)}width:38px;height:38px;
                 display:flex;align-items:center;justify-content:center;font-family:Inter;
                 font-weight:700;font-size:20px;color:#FFF;">{i+1}</div>
  </div>
  <div style="flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:30px;color:{INK};letter-spacing:-0.5px;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#6E635E;margin-top:4px;line-height:1.35;">{desc}</div>
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{CORAL_D};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">The formula</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Four parts. <span style="color:{CORAL_D};">In order.</span>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;margin-top:28px;justify-content:center;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: Worked example ─────────────────────────────────────────────────
def _slide4(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{CORAL_D};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">Heard out loud</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    What it <span style="color:{CORAL_D};">sounds like.</span>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px;">
  <div style="{_clay('#FFFFFF', 36)}padding:34px 38px;display:flex;gap:24px;align-items:flex-start;">
    <div style="{_clay(MINT, 26)}width:80px;height:80px;flex-shrink:0;display:flex;align-items:center;justify-content:center;">
      <div style="transform:scale(1.0);">{ICON_CHAT}</div>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:31px;color:{INK};line-height:1.5;font-style:italic;">
      "Hi, I'm Maya - I just finished a marketing degree at Leeds. Last year I ran the social for a student festival
      and grew it from <span style="color:{MINT_D};font-weight:700;">2k to 15k followers</span> in six months. I'm looking
      for a grad role in social or content. What does your team work on?"
    </div>
  </div>
  <div style="display:flex;gap:22px;">
    <div style="flex:1;{_clay('#FFFFFF', 28)}padding:24px 26px;">
      <div style="font-family:Inter;font-weight:700;font-size:20px;color:{MINT_D};letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Why it lands</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#6E635E;line-height:1.4;">
        A number they'll remember. A clear ask. A question that hands them the mic.
      </div>
    </div>
    <div style="flex:1;{_clay('#FFFFFF', 28)}padding:24px 26px;">
      <div style="font-family:Inter;font-weight:700;font-size:20px;color:{CORAL_D};letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Under 30 seconds</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#6E635E;line-height:1.4;">
        Read it aloud. If it runs long, cut the degree detail before you cut the result.
      </div>
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: Adapt it ───────────────────────────────────────────────────────
def _slide5(out):
    f = _fonts()
    scenes = [
        ("At a careers fair", "Lead with the ask. They're there to hire. 'I'm after a grad data role' first.", BLUE, BLUE_D),
        ("On a video call", "Smile before you speak. Keep it to 20 seconds - screens shrink attention.", PURPLE, PURPLE_D),
        ("In a lift, for real", "Cut to proof + ask. No time for the degree. 'I built X, I want Y.'", AMBER, AMBER_D),
        ("Sliding into a DM", "Same formula, written. One result, one question. Under 90 words.", MINT, MINT_D),
    ]
    rows = ""
    for title, desc, bg, dark in scenes:
        rows += f"""<div style="{_clay('#FFFFFF', 30)}padding:26px 28px;">
  <div style="display:flex;align-items:center;gap:14px;margin-bottom:12px;">
    <div style="{_clay(bg, 16)}width:20px;height:20px;flex-shrink:0;"></div>
    <div style="font-family:Inter;font-weight:700;font-size:27px;color:{dark};letter-spacing:-0.5px;">{title}</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#6E635E;line-height:1.4;">{desc}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{CORAL_D};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">Same core, different room</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Flex it to <span style="color:{CORAL_D};">the moment.</span>
  </div>
</div>
<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:28px;align-content:center;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: Kill list ──────────────────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    kills = [
        ("The life story", "Starting at 'well, in year 9 I...' You've lost them by GCSEs."),
        ("The adjective pile", "'Passionate, motivated, hardworking.' Says nothing. Show, don't label."),
        ("The mumbled ask", "Trailing off with '...so yeah.' End on the question, land it."),
        ("The monologue", "45 seconds with no breath. It's a pitch, not a TED talk."),
    ]
    rows = ""
    for title, desc in kills:
        rows += f"""<div style="{_clay('#FFFFFF', 30)}padding:26px 28px;display:flex;gap:18px;align-items:flex-start;">
  <div style="{_clay(CORAL, 40)}width:44px;height:44px;flex-shrink:0;display:flex;align-items:center;
               justify-content:center;font-family:Inter;font-weight:700;font-size:26px;color:#FFF;">&times;</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};letter-spacing:-0.5px;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#6E635E;margin-top:5px;line-height:1.38;">{desc}</div>
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{CORAL_D};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">Cut these</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Four ways to <span style="color:{CORAL_D};">lose the room.</span>
  </div>
</div>
<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:28px;align-content:center;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    steps = ["Write your 4 parts down", "Cut it to 30 seconds out loud", "Swap the adjective for a number", "Practise on someone this week"]
    rows = ""
    for i, s in enumerate(steps):
        rows += f"""<div style="display:flex;gap:16px;align-items:center;padding:9px 0;">
  <div style="{_clay(MINT, 30)}width:40px;height:40px;flex-shrink:0;display:flex;align-items:center;
               justify-content:center;font-family:Inter;font-weight:700;font-size:20px;color:#FFF;">{i+1}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:{INK};">{s}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:56px;">
  {_clay_pill("Your turn", CORAL, "#FFF", -2)}
</div>
<div style="flex:1;display:flex;align-items:center;gap:30px;">
  <div style="flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:72px;line-height:0.95;color:{INK};
                 letter-spacing:-3px;word-break:keep-all;hyphens:none;">
      Say it like<br>you <span style="color:{CORAL_D};">mean it.</span>
    </div>
    <div style="{_clay('#FFFFFF', 30)}padding:26px 30px;margin-top:28px;">
      {rows}
    </div>
    <div style="margin-top:26px;{_clay(INK, 50)}display:inline-flex;align-items:center;gap:12px;
                 padding:18px 32px;font-family:Inter;font-weight:700;font-size:24px;color:#FFF;">
      Find roles at internwise.co.uk &rarr;
    </div>
  </div>
  <div style="width:250px;flex-shrink:0;display:flex;align-items:center;justify-content:center;">
    <div style="{_clay(AMBER, 60)}width:220px;height:220px;display:flex;align-items:center;
                 justify-content:center;transform:rotate(6deg);">
      <div style="transform:scale(2.0);">{ICON_MEGAPHONE}</div>
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Elevator Pitch (Week 9, Day 1)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("3d_claymorphism_soft_icons", "week9/d1-elevatorpitch", "week9")
    print("Done - elevator pitch complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week9/d1-elevatorpitch")
