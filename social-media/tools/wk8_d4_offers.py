"""
Internwise - Handling Multiple Offers (Week 8, Day 4)
Design language: SPORTS SCOREBOARD / VS MATCHUP. LED dot-matrix scoreboard,
stadium dark bg, big VS divider, team colour blocks, period-by-period stat table.
7 slides. Accent: LED_AMBER + TEAM_A/TEAM_B on STADIUM.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; OFF_WHITE = "#FAF5EC"

STADIUM   = "#0A0E14"   # dark stadium
BOARD     = "#12181F"   # scoreboard body
BOARD_IN  = "#080B0F"   # inset LED panel
LED_AMBER = "#FFA724"   # classic scoreboard amber
LED_GREEN = "#3DFF88"
LED_RED   = "#FF3D5A"
TEAM_A    = "#2E7BE8"   # offer A blue
TEAM_B    = "#E8462E"   # offer B red
LED_DIM   = "#4A5462"

MONO = "Menlo,Monaco,'Courier New',monospace"

LOGO_W = None
def _load_logos():
    global LOGO_W
    if LOGO_W is None:
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

# LED dot-matrix grid overlay
LED_GRID = (".led{position:absolute;inset:0;z-index:8;pointer-events:none;"
            "background-image:radial-gradient(rgba(0,0,0,0.45) 1.1px,transparent 1.1px);"
            "background-size:4px 4px;}")

# stadium floodlight glow at top
GLOW = ("position:absolute;top:-180px;left:50%;transform:translateX(-50%);"
        "width:900px;height:340px;border-radius:50%;"
        "background:radial-gradient(ellipse,rgba(255,167,36,0.16) 0%,transparent 70%);z-index:1;")

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{STADIUM};}}
.c{{width:1080px;height:1080px;position:relative;padding:36px 40px;display:flex;flex-direction:column;}}
{LED_GRID}
.board{{background:{BOARD};border:4px solid #1E2833;border-radius:14px;
        box-shadow:0 0 0 2px #000, 0 16px 44px rgba(0,0,0,0.7), inset 0 2px 0 rgba(255,255,255,0.05);
        position:relative;overflow:hidden;}}
"""

def _led(text, size, color=LED_AMBER, weight=700, spacing=-2):
    return (f'<span style="font-family:{MONO};font-weight:{weight};font-size:{size}px;'
            f'color:{color};letter-spacing:{spacing}px;'
            f'text-shadow:0 0 18px {color}66, 0 0 4px {color}99;">{text}</span>')

def _panel_label(text, color=LED_DIM):
    return (f'<div style="font-family:{MONO};font-weight:700;font-size:18px;color:{color};'
            f'letter-spacing:3px;text-transform:uppercase;">{text}</div>')

def _clock_bar(period, clock):
    return f"""<div style="display:flex;justify-content:center;align-items:center;gap:26px;
             background:{BOARD_IN};border-top:2px solid #1E2833;padding:12px 0;">
  {_panel_label(period, LED_AMBER)}
  <div style="width:2px;height:16px;background:#1E2833;"></div>
  {_led(clock, 24, LED_GREEN, 700, 1)}
</div>"""


# ─── Slide 1: Hook — the big scoreboard ────────────────────────────────────
def _slide1(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="{GLOW}"></div>
<div class="led"></div>

<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;
             position:relative;z-index:20;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:52px;">
  <div style="background:{LED_RED};color:white;padding:9px 18px;border-radius:4px;
               font-family:{MONO};font-weight:700;font-size:18px;letter-spacing:3px;
               display:flex;align-items:center;gap:9px;">
    <div style="width:9px;height:9px;border-radius:50%;background:white;"></div>LIVE
  </div>
</div>

<!-- The scoreboard -->
<div class="board" style="margin-top:24px;flex-shrink:0;position:relative;z-index:20;">
  <div style="display:flex;align-items:stretch;">
    <!-- Team A -->
    <div style="flex:1;padding:34px 26px;border-right:2px solid #1E2833;">
      <div style="display:flex;align-items:center;gap:11px;margin-bottom:14px;">
        <div style="width:11px;height:32px;background:{TEAM_A};border-radius:2px;"></div>
        {_panel_label("Offer A", "#8A9BB0")}
      </div>
      <div style="font-family:Inter;font-weight:700;font-size:38px;color:white;
                   letter-spacing:-1px;line-height:1;">Big name</div>
      <div style="margin-top:18px;">{_led("&pound;34K", 84, TEAM_A)}</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:21px;color:#7A8A9E;margin-top:10px;">
        deadline: 5 days
      </div>
      <div style="border-top:1px solid #1E2833;margin-top:18px;padding-top:14px;
                   font-family:'DM Sans';font-weight:500;font-size:21px;color:#7A8A9E;line-height:1.4;">
        1 of 40 grads &middot; fixed ladder<br>name opens doors
      </div>
    </div>

    <!-- VS -->
    <div style="width:112px;background:{BOARD_IN};display:flex;flex-direction:column;
                 align-items:center;justify-content:center;gap:6px;">
      {_led("VS", 42, LED_AMBER, 700, 0)}
      <div style="width:34px;height:2px;background:#1E2833;"></div>
      {_panel_label("Q4", LED_DIM)}
    </div>

    <!-- Team B -->
    <div style="flex:1;padding:34px 26px;border-left:2px solid #1E2833;text-align:right;">
      <div style="display:flex;align-items:center;gap:11px;margin-bottom:14px;justify-content:flex-end;">
        {_panel_label("Offer B", "#8A9BB0")}
        <div style="width:11px;height:32px;background:{TEAM_B};border-radius:2px;"></div>
      </div>
      <div style="font-family:Inter;font-weight:700;font-size:38px;color:white;
                   letter-spacing:-1px;line-height:1;">Small team</div>
      <div style="margin-top:18px;">{_led("&pound;29K", 84, TEAM_B)}</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:21px;color:#7A8A9E;margin-top:10px;">
        deadline: 14 days
      </div>
      <div style="border-top:1px solid #1E2833;margin-top:18px;padding-top:14px;
                   font-family:'DM Sans';font-weight:500;font-size:21px;color:#7A8A9E;line-height:1.4;">
        1 of 3, direct to lead<br>whole problems, year 1
      </div>
    </div>
  </div>
  {_clock_bar("Decision window", "05 : 00 : 00")}
</div>

<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;
             position:relative;z-index:20;padding-bottom:8px;">
  {_panel_label("Two offers / one clock", LED_AMBER)}
  <div style="font-family:Inter;font-weight:700;font-size:96px;line-height:0.92;color:white;
               letter-spacing:-4px;word-break:keep-all;hyphens:none;margin-top:16px;">
    Two offers.<br>Zero <span style="color:{LED_AMBER};font-style:italic;">panic.</span>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:#8FA3BA;
               margin-top:22px;line-height:1.35;max-width:860px;">
    The exploding deadline is the pressure. Here's how to buy time and use the leverage properly.
  </div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:flex-end;position:relative;z-index:20;">
  <div style="font-family:{MONO};font-size:20px;color:{LED_DIM};">SWIPE &rarr;</div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 2: The Data ─────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("58%", "of grads accept the first offer without asking for more time", LED_RED),
        ("92%", "of employers will extend a deadline if you ask professionally", LED_GREEN),
        ("&pound;4.2K", "average uplift when a second offer is mentioned honestly", LED_AMBER),
    ]
    cards = ""
    for val, label, color in stats:
        cards += f"""<div class="board" style="flex:1;padding:28px 24px;display:flex;flex-direction:column;">
  <div style="flex:1;display:flex;align-items:center;">{_led(val, 68, color)}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#A8BACE;
               line-height:1.35;margin-top:14px;">{label}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="{GLOW}"></div><div class="led"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_panel_label("The tape", LED_AMBER)}
  <div style="font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;margin-top:12px;">
    Nearly everyone <span style="color:{LED_AMBER};font-style:italic;">folds early.</span>
  </div>
</div>
<div style="flex:1;display:flex;gap:20px;margin:34px 0 20px 0;position:relative;z-index:20;">{cards}</div>
<div style="flex-shrink:0;font-family:{MONO};font-size:19px;color:{LED_DIM};text-align:right;
             position:relative;z-index:20;">
  SOURCES: HIGH FLIERS 2026 / GLASSDOOR NEGOTIATION STUDY 2025
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 3: Buy time ─────────────────────────────────────────────────────
def _slide3(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="{GLOW}"></div><div class="led"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_panel_label("Move 01 / stop the clock", LED_AMBER)}
  <div style="font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;margin-top:12px;">
    Buy time <span style="color:{LED_AMBER};font-style:italic;">first.</span>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:20px;margin-top:32px;
             justify-content:center;position:relative;z-index:20;">
  <div class="board" style="padding:28px 32px;">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
      <div style="width:10px;height:10px;border-radius:50%;background:{LED_GREEN};"></div>
      {_panel_label("Say this", LED_GREEN)}
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:white;line-height:1.5;font-style:italic;">
      "Thank you, I'm really pleased. This is a big decision and I want to give it the attention it deserves.
      Could I come back to you by [date, 7-10 days out]?"
    </div>
  </div>
  <div class="board" style="padding:28px 32px;">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
      <div style="width:10px;height:10px;border-radius:50%;background:{LED_RED};"></div>
      {_panel_label("Never say this", LED_RED)}
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:#9FB0C4;line-height:1.5;font-style:italic;">
      "I'm waiting to hear back from another company." Honest, but it hands them a reason to move on.
      Ask for time on your own terms.
    </div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:{LED_AMBER};
               text-align:center;margin-top:6px;">
    92% say yes. An exploding deadline is a red flag about them, not a test of you.
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 4: Accelerate the other one ────────────────────────────────────
def _slide4(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="{GLOW}"></div><div class="led"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_panel_label("Move 02 / speed up the other side", LED_AMBER)}
  <div style="font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;margin-top:12px;">
    Tell the one you <span style="color:{LED_AMBER};font-style:italic;">actually want.</span>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:20px;
             margin-top:32px;position:relative;z-index:20;">
  <div class="board" style="padding:28px 32px;">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
      <div style="width:10px;height:10px;border-radius:50%;background:{LED_GREEN};"></div>
      {_panel_label("The email that works", LED_GREEN)}
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:white;line-height:1.5;font-style:italic;">
      "I wanted to be transparent: I've received an offer elsewhere with a deadline of [date].
      You're my first choice and I'd rather not decide without hearing from you.
      Is there any chance of an update before then?"
    </div>
  </div>
  <div style="display:flex;gap:20px;">
    <div class="board" style="flex:1;padding:24px 26px;">
      {_panel_label("Why it lands", LED_DIM)}
      <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#B0C0D2;
                   line-height:1.4;margin-top:10px;">
        It's honest, it's flattering, and it gives them a real reason to move. Recruiters respect it.
      </div>
    </div>
    <div class="board" style="flex:1;padding:24px 26px;">
      {_panel_label("The rule", LED_DIM)}
      <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#B0C0D2;
                   line-height:1.4;margin-top:10px;">
        Only say "first choice" if it's true. If they call your bluff and you decline, word travels.
      </div>
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 5: The real comparison table ───────────────────────────────────
def _slide5(out):
    f = _fonts()
    rows = [
        ("Base salary",        "&pound;34,000", "&pound;29,000", TEAM_A),
        ("Real take-home*",    "&pound;1,840/mo", "&pound;1,910/mo", TEAM_B),
        ("Who you learn from", "1 of 40 grads", "1 of 3, direct to lead", TEAM_B),
        ("Scope in year 1",    "one narrow slice", "whole problems", TEAM_B),
        ("Name on the CV",     "opens doors", "needs explaining", TEAM_A),
        ("Time to promotion",  "fixed 24mo ladder", "when you're ready", TEAM_B),
    ]
    trs = ""
    for label, a, b, winner in rows:
        a_col = "white" if winner == TEAM_A else "#7A8A9E"
        b_col = "white" if winner == TEAM_B else "#7A8A9E"
        a_dot = f'<div style="width:7px;height:7px;border-radius:50%;background:{TEAM_A};"></div>' if winner == TEAM_A else '<div style="width:7px;"></div>'
        b_dot = f'<div style="width:7px;height:7px;border-radius:50%;background:{TEAM_B};"></div>' if winner == TEAM_B else '<div style="width:7px;"></div>'
        trs += f"""<div style="display:flex;align-items:center;border-bottom:1px solid #1A222C;padding:15px 0;">
  <div style="flex:1;display:flex;align-items:center;gap:10px;justify-content:flex-end;padding-right:20px;">
    <div style="font-family:'DM Sans';font-weight:600;font-size:24px;color:{a_col};text-align:right;">{a}</div>
    {a_dot}
  </div>
  <div style="width:250px;flex-shrink:0;text-align:center;font-family:{MONO};font-weight:700;
               font-size:17px;color:{LED_DIM};letter-spacing:2px;text-transform:uppercase;">{label}</div>
  <div style="flex:1;display:flex;align-items:center;gap:10px;padding-left:20px;">
    {b_dot}
    <div style="font-family:'DM Sans';font-weight:600;font-size:24px;color:{b_col};">{b}</div>
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="{GLOW}"></div><div class="led"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_panel_label("Move 03 / the real tape", LED_AMBER)}
  <div style="font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;margin-top:12px;">
    Salary is <span style="color:{LED_AMBER};font-style:italic;">one line</span> of six.
  </div>
</div>
<div class="board" style="flex:1;margin-top:26px;padding:22px 26px;display:flex;
             flex-direction:column;justify-content:center;position:relative;z-index:20;">
  <div style="display:flex;align-items:center;padding-bottom:14px;border-bottom:2px solid #1E2833;">
    <div style="flex:1;text-align:right;padding-right:20px;">
      <div style="font-family:Inter;font-weight:700;font-size:26px;color:{TEAM_A};">Big name</div>
    </div>
    <div style="width:250px;flex-shrink:0;text-align:center;">{_led("VS", 24, LED_AMBER, 700, 0)}</div>
    <div style="flex:1;padding-left:20px;">
      <div style="font-family:Inter;font-weight:700;font-size:26px;color:{TEAM_B};">Small team</div>
    </div>
  </div>
  {trs}
  <div style="font-family:'DM Sans';font-weight:400;font-size:19px;color:{LED_DIM};
               text-align:center;margin-top:14px;">*after London rent differential</div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 6: Fouls / what not to do ──────────────────────────────────────
def _slide6(out):
    f = _fonts()
    fouls = [
        ("Bluffing an offer you don't have", "They call it. You have nothing. The role is gone and the recruiter remembers."),
        ("Accepting then reneging", "Legal, but the sector is small. Grad recruiters talk to each other constantly."),
        ("Negotiating both against each other", "Transparent to everyone involved. You lose trust on both sides at once."),
        ("Deciding on salary alone", "The &pound;5K gap disappears in year 2. The learning gap compounds for a decade."),
    ]
    rows = ""
    for title, why in fouls:
        rows += f"""<div class="board" style="padding:24px 26px;">
  <div style="display:flex;align-items:flex-start;gap:12px;">
    <div style="width:26px;height:26px;border-radius:4px;background:{LED_RED};flex-shrink:0;
                 display:flex;align-items:center;justify-content:center;font-family:{MONO};
                 font-weight:700;font-size:17px;color:white;">!</div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{LED_RED};
                 line-height:1.2;word-break:keep-all;hyphens:none;">{title}</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#A8BACE;
               margin-top:12px;line-height:1.4;">{why}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="{GLOW}"></div><div class="led"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_panel_label("Fouls / instant red card", LED_RED)}
  <div style="font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;margin-top:12px;">
    Four ways to <span style="color:{LED_RED};font-style:italic;">lose both.</span>
  </div>
</div>
<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:28px;
             align-content:center;position:relative;z-index:20;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 7: CTA — final whistle ─────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    checks = [
        "Ask for 7-10 days. In writing. Today.",
        "Email your first choice. Be honest about the clock.",
        "Score all six lines, not just salary.",
        "Decline the other one warmly. You'll meet them again.",
    ]
    rows = ""
    for i, c in enumerate(checks):
        rows += f"""<div style="display:flex;gap:14px;align-items:center;padding:9px 0;">
  <div style="width:26px;height:26px;border-radius:4px;background:{LED_GREEN};flex-shrink:0;
               display:flex;align-items:center;justify-content:center;font-family:{MONO};
               font-weight:700;font-size:15px;color:{STADIUM};">{i+1}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:white;">{c}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="{GLOW}"></div><div class="led"></div>

<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;
             position:relative;z-index:20;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:52px;">
  <div style="background:{LED_GREEN};color:{STADIUM};padding:9px 18px;border-radius:4px;
               font-family:{MONO};font-weight:700;font-size:18px;letter-spacing:3px;">FULL TIME</div>
</div>

<div style="flex-shrink:0;margin-top:36px;position:relative;z-index:20;">
  {_panel_label("Your play", LED_AMBER)}
  <div style="font-family:Inter;font-weight:700;font-size:84px;line-height:0.94;color:white;
               letter-spacing:-3px;word-break:keep-all;hyphens:none;margin-top:14px;">
    Two offers is<br>a <span style="color:{LED_AMBER};font-style:italic;">good problem.</span>
  </div>
</div>

<div class="board" style="margin-top:32px;padding:30px 34px;position:relative;z-index:20;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
    <div style="width:10px;height:10px;border-radius:50%;background:{LED_GREEN};"></div>
    {_panel_label("The 4-step play", LED_GREEN)}
  </div>
  {rows}
</div>

<div style="flex:1;"></div>

<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;
             position:relative;z-index:20;">
  <div style="background:{LED_AMBER};color:{STADIUM};padding:17px 30px;border-radius:6px;
               font-family:Inter;font-weight:700;font-size:24px;">
    Find roles at internwise.co.uk &rarr;
  </div>
  <div style="font-family:{MONO};font-size:19px;color:{LED_DIM};">07 / 07</div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Multiple Offers (Week 8, Day 4)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("led_scoreboard_vs_matchup", "week8/d4-offers", "week8")
    print("Done - multiple offers complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week8/d4-offers")
