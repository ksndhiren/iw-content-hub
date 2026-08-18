"""
Internwise - Reading the Room in Interviews (Week 9, Day 3)
Design language: POKER / CARD-TABLE READ. Green felt table, playing-card motifs
(suits, corner pips), 3D poker-chip icons, spotlight vignette, "tells" framing.
7 slides. Accent: felt green + gold chips + CORAL for red flags.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; OFF_WHITE = "#FAF5EC"

FELT      = "#1F6B4A"   # poker felt green
FELT_D    = "#124D34"
FELT_L    = "#2A8159"
GOLD      = "#E9BC58"; GOLD_D = "#C99A34"
CARD_W    = "#FBF8F0"   # playing card white
CORAL     = "#E5564A"   # red flag / red suit
GREEN_GO  = "#5FD39A"   # green flag
INK       = "#22303C"
CREAM     = "#F2E9D8"

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

# felt bg with spotlight + weave texture
def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;
      background:radial-gradient(ellipse at 50% 42%,{FELT_L} 0%,{FELT} 46%,{FELT_D} 100%);}}
.c{{width:1080px;height:1080px;position:relative;padding:52px 56px;display:flex;flex-direction:column;}}
.weave{{position:absolute;inset:0;z-index:1;pointer-events:none;opacity:0.5;
        background-image:radial-gradient(rgba(255,255,255,0.05) 1px,transparent 1px),
        radial-gradient(rgba(0,0,0,0.08) 1px,transparent 1px);
        background-size:7px 7px, 7px 7px;background-position:0 0, 3px 3px;}}
.rail{{position:absolute;inset:20px;border:3px solid rgba(233,188,88,0.35);border-radius:34px;z-index:2;pointer-events:none;}}
"""

# suit glyphs (unicode via drawn SVG for crispness)
SPADE = lambda c,s=30: f'<svg width="{s}" height="{s}" viewBox="0 0 30 30"><path d="M15 3 C15 3 26 12 26 19 C26 24 21 25 18 22 C19 25 20 27 22 28 L8 28 C10 27 11 25 12 22 C9 25 4 24 4 19 C4 12 15 3 15 3 Z" fill="{c}"/></svg>'
HEART = lambda c,s=30: f'<svg width="{s}" height="{s}" viewBox="0 0 30 30"><path d="M15 27 C4 19 3 11 8 8 C12 5.5 15 9 15 11.5 C15 9 18 5.5 22 8 C27 11 26 19 15 27 Z" fill="{c}"/></svg>'
CLUB = lambda c,s=30: f'<svg width="{s}" height="{s}" viewBox="0 0 30 30"><circle cx="15" cy="9" r="5.4" fill="{c}"/><circle cx="8.5" cy="16" r="5.4" fill="{c}"/><circle cx="21.5" cy="16" r="5.4" fill="{c}"/><path d="M13 16 h4 l2 11 h-8 Z" fill="{c}"/></svg>'
DIAMOND = lambda c,s=30: f'<svg width="{s}" height="{s}" viewBox="0 0 30 30"><path d="M15 3 L25 15 L15 27 L5 15 Z" fill="{c}"/></svg>'

def _chip(color, dark, size=118, label=""):
    """3D poker chip with dashed edge ring."""
    return f"""<div style="width:{size}px;height:{size}px;border-radius:50%;flex-shrink:0;
             background:radial-gradient(circle at 38% 32%,{color} 0%,{dark} 100%);
             box-shadow:0 12px 22px rgba(0,0,0,0.4),inset 0 3px 5px rgba(255,255,255,0.4),
             inset 0 -6px 10px rgba(0,0,0,0.25);position:relative;display:flex;
             align-items:center;justify-content:center;">
  <div style="position:absolute;inset:11px;border-radius:50%;border:4px dashed rgba(255,255,255,0.6);"></div>
  <div style="width:58%;height:58%;border-radius:50%;background:{CARD_W};display:flex;
               align-items:center;justify-content:center;box-shadow:inset 0 2px 4px rgba(0,0,0,0.2);">{label}</div>
</div>"""

def _card_chip_row():
    """small decorative suit chips row."""
    return f"""<div style="display:flex;gap:12px;">
      {_chip(CORAL, "#B23A30", 52, HEART(CORAL,22))}
      {_chip(INK, "#0E1820", 52, SPADE("#fff",22))}
      {_chip(GOLD, GOLD_D, 52, DIAMOND(INK,22))}
    </div>"""

def _kicker(text, color=GOLD):
    return (f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:19px;color:{color};'
            f'text-transform:uppercase;letter-spacing:3px;">{text}</div>')

def _playing_card(rank, suit_fn, suit_col, big_inner, rot=0, w=210, h=300):
    """A playing-card shaped tile."""
    return f"""<div style="width:{w}px;height:{h}px;background:{CARD_W};border-radius:16px;
             box-shadow:0 14px 30px rgba(0,0,0,0.4);transform:rotate({rot}deg);position:relative;
             padding:16px;flex-shrink:0;overflow:hidden;">
  <div style="position:absolute;top:12px;left:14px;text-align:center;">
    <div style="font-family:Inter;font-weight:700;font-size:30px;color:{suit_col};line-height:0.9;">{rank}</div>
    {suit_fn(suit_col,22)}
  </div>
  <div style="position:absolute;bottom:12px;right:14px;text-align:center;transform:rotate(180deg);">
    <div style="font-family:Inter;font-weight:700;font-size:30px;color:{suit_col};line-height:0.9;">{rank}</div>
    {suit_fn(suit_col,22)}
  </div>
  <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">{big_inner}</div>
</div>"""


# ── Slide 1: Hook — dealt cards ─────────────────────────────────────────────
def _slide1(out):
    f = _fonts()
    cards = f"""
<div style="display:flex;align-items:center;justify-content:center;">
  {_playing_card("A", SPADE, INK, SPADE(INK,84), rot=-14, w=196, h=280)}
  <div style="margin-left:-60px;">{_playing_card("K", HEART, CORAL, HEART(CORAL,84), rot=-3, w=196, h=280)}</div>
  <div style="margin-left:-60px;">{_playing_card("Q", DIAMOND, GOLD_D, DIAMOND(GOLD_D,84), rot=8, w=196, h=280)}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="weave"></div><div class="rail"></div>

<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;position:relative;z-index:20;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:54px;">
  <div style="background:{GOLD};color:{INK};padding:11px 22px;border-radius:50px;
               font-family:Inter;font-weight:700;font-size:19px;letter-spacing:2px;
               text-transform:uppercase;box-shadow:0 6px 14px rgba(0,0,0,0.3);">Read the table</div>
</div>

<div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;
             text-align:center;position:relative;z-index:20;gap:30px;">
  {cards}
  <div>
    {_kicker("Interviews / spotting the tells", GOLD)}
    <div style="font-family:Inter;font-weight:700;font-size:82px;line-height:0.94;color:{CARD_W};
                 letter-spacing:-3px;margin-top:16px;word-break:keep-all;hyphens:none;">
      Read the <span style="color:{GOLD};font-style:italic;">room.</span>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:{CREAM};
                 margin-top:16px;line-height:1.35;max-width:760px;">
      An interview is a two-way read. Here's how to spot the buying signals and the red flags.
    </div>
  </div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:flex-end;position:relative;z-index:20;">
  <div style="font-family:'DM Sans';font-weight:500;font-size:20px;color:{CREAM};">SWIPE &rarr;</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: Why it matters ─────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("2-way", "An interview reads you AND you read them. Most candidates only play one side.", GOLD, GOLD_D, DIAMOND),
        ("55%", "of a room's mood is read from body language, not words. Watch the hands and eyes.", GREEN_GO, "#3FA877", CLUB),
        ("1", "green or red flag spotted early can save you months in the wrong job.", CORAL, "#B23A30", HEART),
    ]
    cards = ""
    for val, label, col, dark, suit in stats:
        cards += f"""<div style="flex:1;background:{CARD_W};border-radius:20px;padding:34px 28px;
             box-shadow:0 12px 26px rgba(0,0,0,0.32);display:flex;flex-direction:column;position:relative;overflow:hidden;">
  <div style="margin-bottom:20px;">{_chip(col, dark, 90, suit(col if col!=GOLD else GOLD_D,30))}</div>
  <div style="font-family:Inter;font-weight:700;font-size:64px;color:{dark};letter-spacing:-2px;line-height:1;">{val}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{INK};margin-top:16px;line-height:1.4;">{label}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="weave"></div><div class="rail"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_kicker("Why it matters", GOLD)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{CARD_W};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    You're playing <span style="color:{GOLD};font-style:italic;">both hands.</span>
  </div>
</div>
<div style="flex:1;display:flex;gap:22px;margin:34px 0 18px 0;position:relative;z-index:20;">{cards}</div>
<div style="flex-shrink:0;font-family:'DM Sans';font-weight:400;font-size:20px;color:{CREAM};
             text-align:right;position:relative;z-index:20;">
  Sources: Albert Mehrabian communication research, LinkedIn Interview Report 2026
</div>
</div></body></html>"""
    _render(html, out)


# ── Slides 3-4: green flags / red flags ─────────────────────────────────────
def _flag_slide(out, n, kicker, headline, flag_col, flag_dark, suit, is_green, items):
    f = _fonts()
    rows = ""
    for title, desc in items:
        mark = "&check;" if is_green else "&times;"
        rows += f"""<div style="display:flex;gap:20px;align-items:flex-start;background:{CARD_W};
             border-radius:16px;padding:22px 26px;box-shadow:0 10px 22px rgba(0,0,0,0.3);">
  <div style="width:46px;height:46px;border-radius:50%;background:{flag_col};flex-shrink:0;
               display:flex;align-items:center;justify-content:center;font-family:Inter;
               font-weight:700;font-size:24px;color:#fff;box-shadow:inset 0 -3px 5px rgba(0,0,0,0.2);">{mark}</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};letter-spacing:-0.5px;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#556;margin-top:5px;line-height:1.38;">{desc}</div>
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="weave"></div><div class="rail"></div>
<div style="flex-shrink:0;position:relative;z-index:20;display:flex;align-items:center;gap:22px;">
  {_chip(flag_col, flag_dark, 92, suit('#fff' if not is_green else INK,32))}
  <div>
    {_kicker(kicker, flag_col if is_green else CORAL)}
    <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;color:{CARD_W};
                 letter-spacing:-2px;margin-top:6px;word-break:keep-all;hyphens:none;">{headline}</div>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;margin-top:30px;justify-content:center;
             position:relative;z-index:20;">{rows}</div>
</div></body></html>"""
    _render(html, out)

def _slide3(out): _flag_slide(out, 3, "Green flags at the table", 'Signs they <span style="font-style:italic;">want you.</span>',
    GREEN_GO, "#3FA877", CLUB, True, [
    ("They start selling the role", "When they shift from testing you to pitching the team, you're in the lead."),
    ("The scope creep questions", "'What would you want in year two?' means they're picturing you there."),
    ("Time runs over", "A 30-min slot hitting 45 is interest, not bad planning. They're enjoying it."),
    ("They introduce you to others", "Pulling in a colleague mid-interview is a strong, spontaneous buy signal."),
])

def _slide4(out): _flag_slide(out, 4, "Red flags in the felt", 'Signs to <span style="font-style:italic;">walk away.</span>',
    CORAL, "#B23A30", HEART, False, [
    ("Nobody can describe success", "If three people give three different answers to 'what does good look like?', run."),
    ("They dodge the turnover question", "Ask why the last person left. A long pause is the answer."),
    ("Pressure to decide on the spot", "'We need a yes today' is a tactic, not a compliment. Good employers give you time."),
    ("Everyone looks exhausted", "The room's energy is data. Tired, guarded faces tell you more than the pitch does."),
])


# ── Slide 5: How to read live ───────────────────────────────────────────────
def _slide5(out):
    f = _fonts()
    tells = [
        ("Leaning in", "Genuine interest. Match it - lean in back, it builds rapport.", GREEN_GO),
        ("Checking the time", "You're losing them. Wrap your point and ask a sharp question.", GOLD_D),
        ("Note-taking spikes", "You just said something that landed. Do more of that.", GREEN_GO),
        ("Closed-off arms + short replies", "Disengaged or guarded. Change tack: ask about THEM.", CORAL),
    ]
    rows = ""
    for tell, read, col in tells:
        rows += f"""<div style="background:{CARD_W};border-radius:16px;padding:24px 28px;
             box-shadow:0 10px 22px rgba(0,0,0,0.3);border-left:8px solid {col};">
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:{INK};letter-spacing:-0.5px;">{tell}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#556;margin-top:6px;line-height:1.38;">{read}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="weave"></div><div class="rail"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_kicker("Live tells", GOLD)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{CARD_W};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Watch. Adjust. <span style="color:{GOLD};font-style:italic;">Repeat.</span>
  </div>
</div>
<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:28px;
             align-content:center;position:relative;z-index:20;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: Your questions that read them ──────────────────────────────────
def _slide6(out):
    f = _fonts()
    qs = [
        "\"What does someone need to do in the first 90 days to be seen as a success?\"",
        "\"Why did the last person in this role leave?\"",
        "\"What's the thing about working here you'd change if you could?\"",
        "\"How would you describe the team on a stressful week?\"",
    ]
    rows = ""
    for i, q in enumerate(qs):
        rows += f"""<div style="display:flex;gap:20px;align-items:center;background:{CARD_W};
             border-radius:16px;padding:24px 28px;box-shadow:0 10px 22px rgba(0,0,0,0.3);">
  {_chip(GOLD, GOLD_D, 60, f'<span style="font-family:Inter;font-weight:700;font-size:24px;color:{INK};">{i+1}</span>')}
  <div style="font-family:'DM Sans';font-weight:500;font-style:italic;font-size:26px;color:{INK};line-height:1.4;">{q}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="weave"></div><div class="rail"></div>
<div style="flex-shrink:0;position:relative;z-index:20;">
  {_kicker("Your reads", GOLD)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{CARD_W};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Questions that <span style="color:{GOLD};font-style:italic;">flip the table.</span>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;margin-top:28px;justify-content:center;
             position:relative;z-index:20;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div class="weave"></div><div class="rail"></div>
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;position:relative;z-index:20;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:54px;">
  {_card_chip_row()}
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:20;">
  {_kicker("Play both hands", GOLD)}
  <div style="font-family:Inter;font-weight:700;font-size:80px;line-height:0.95;color:{CARD_W};
               letter-spacing:-3px;margin-top:14px;word-break:keep-all;hyphens:none;">
    You're interviewing<br><span style="color:{GOLD};font-style:italic;">them too.</span>
  </div>
  <div style="background:{CARD_W};border-radius:20px;padding:30px 34px;margin-top:30px;
               box-shadow:0 14px 30px rgba(0,0,0,0.35);max-width:760px;">
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:{INK};margin-bottom:14px;">Your table read, in one line each:</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{INK};line-height:1.6;">
      <span style="color:#3FA877;font-weight:700;">Green:</span> they sell, they linger, they introduce you.<br>
      <span style="color:{CORAL};font-weight:700;">Red:</span> no clear success, dodged turnover, rushed yes.<br>
      <span style="color:{GOLD_D};font-weight:700;">Always:</span> ask the question that reads them back.
    </div>
  </div>
  <div style="margin-top:28px;background:{GOLD};color:{INK};display:inline-flex;align-items:center;gap:12px;
               padding:18px 32px;border-radius:50px;font-family:Inter;font-weight:700;font-size:24px;
               width:fit-content;box-shadow:0 8px 18px rgba(0,0,0,0.3);">
    Find roles worth reading at internwise.co.uk &rarr;
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Read the Room (Week 9, Day 3)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("poker_card_table_tells", "week9/d3-readtheroom", "week9")
    print("Done - read the room complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week9/d3-readtheroom")
