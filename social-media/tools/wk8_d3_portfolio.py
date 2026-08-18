"""
Internwise - The Portfolio Play for Non-Designers (Week 8, Day 3)
Design language: TRADING CARD / PANINI STICKER. Holographic foil gradient borders,
stat blocks, rarity badges, glossy shine sweep, card-back texture.
7 slides. Accent: HOLO gradient + FOIL_GOLD on CARD_VOID.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; DEEP_BLUE = "#264D7E"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; OFF_WHITE = "#FAF5EC"

CARD_VOID  = "#0B1020"   # deep space bg
CARD_FACE  = "#161E38"   # card interior
FOIL_GOLD  = "#FFD24A"
HOLO_1     = "#FF6BD6"
HOLO_2     = "#5BC8E8"
HOLO_3     = "#7FFFB0"
STAT_GREY  = "#8A9BB8"

HOLO_GRAD = ("linear-gradient(115deg,#FF6BD6 0%,#FFD24A 22%,#7FFFB0 44%,"
             "#5BC8E8 66%,#B98BFF 84%,#FF6BD6 100%)")

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

# Starfield / sparkle dots on the void
VOID_BG = (f"background:{CARD_VOID};"
           "background-image:radial-gradient(rgba(255,255,255,0.14) 1px,transparent 1px),"
           "radial-gradient(rgba(255,210,74,0.10) 1px,transparent 1px);"
           "background-size:34px 34px, 71px 71px;background-position:0 0, 19px 23px;")

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;{VOID_BG}}}
.c{{width:1080px;height:1080px;position:relative;padding:40px 44px;display:flex;flex-direction:column;}}
.shine{{position:absolute;inset:0;z-index:12;pointer-events:none;border-radius:inherit;
        background:linear-gradient(105deg,transparent 34%,rgba(255,255,255,0.16) 46%,
        rgba(255,255,255,0.05) 52%,transparent 60%);}}
"""

def _holo_frame(inner_html, pad=5, radius=22, extra=""):
    """Holographic foil border wrapping a card face."""
    return f"""<div style="background:{HOLO_GRAD};padding:{pad}px;border-radius:{radius}px;
             box-shadow:0 12px 40px rgba(0,0,0,0.55);position:relative;{extra}">
  <div style="background:{CARD_FACE};border-radius:{radius-4}px;position:relative;overflow:hidden;height:100%;">
    {inner_html}
    <div class="shine"></div>
  </div>
</div>"""

def _rarity(text, color=FOIL_GOLD):
    return (f'<div style="display:inline-block;background:{color};color:{CARD_VOID};'
            f'padding:5px 13px;border-radius:4px;font-family:Inter;font-weight:700;'
            f'font-size:16px;letter-spacing:2px;text-transform:uppercase;">{text}</div>')

def _stat_bar(label, value, pct, color):
    return f"""<div style="margin-bottom:11px;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;">
    <div style="font-family:Inter;font-weight:700;font-size:18px;color:{STAT_GREY};
                 letter-spacing:2px;text-transform:uppercase;">{label}</div>
    <div style="font-family:Inter;font-weight:700;font-size:22px;color:{color};">{value}</div>
  </div>
  <div style="height:9px;background:rgba(255,255,255,0.10);border-radius:5px;overflow:hidden;">
    <div style="height:100%;width:{pct}%;background:{color};border-radius:5px;"></div>
  </div>
</div>"""

def _card_number(n, total=7):
    return (f'<div style="font-family:Inter;font-weight:700;font-size:18px;color:{STAT_GREY};'
            f'letter-spacing:2px;">{n:02d} / {total:02d}</div>')


# ─── Slide 1: Hook — the pack, one card pulled ─────────────────────────────
def _slide1(out):
    f = _fonts()
    card_inner = f"""
<div style="padding:26px 24px;height:100%;display:flex;flex-direction:column;">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    {_rarity("ULTRA RARE", FOIL_GOLD)}
    <div style="font-family:Inter;font-weight:700;font-size:17px;color:{STAT_GREY};letter-spacing:2px;">PROOF</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;
               text-align:center;padding:14px 0;">
    <div style="font-family:Inter;font-weight:700;font-size:88px;line-height:0.9;
                 background:{HOLO_GRAD};-webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;letter-spacing:-4px;">THE<br>WORK</div>
    <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{STAT_GREY};
                 letter-spacing:3px;text-transform:uppercase;margin-top:14px;">Beats the CV</div>
  </div>
  <div style="border-top:2px solid rgba(255,255,255,0.10);padding-top:14px;">
    {_stat_bar("Recall", "9.1", 91, HOLO_3)}
    {_stat_bar("Trust", "8.7", 87, HOLO_2)}
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">

<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:56px;">
  <div style="background:{HOLO_GRAD};padding:3px;border-radius:8px;transform:rotate(3deg);">
    <div style="background:{CARD_VOID};padding:10px 18px;border-radius:6px;
                 font-family:Inter;font-weight:700;font-size:19px;color:white;
                 letter-spacing:2px;text-transform:uppercase;">Collect all 5</div>
  </div>
</div>

<div style="flex:1;display:flex;align-items:center;gap:34px;margin-top:22px;">
  <div style="flex:1;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:19px;
                 background:{HOLO_GRAD};-webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;letter-spacing:4px;text-transform:uppercase;margin-bottom:16px;">
      Portfolio / not just designers
    </div>
    <div style="font-family:Inter;font-weight:700;font-size:76px;line-height:0.93;color:white;
                 letter-spacing:-3px;word-break:keep-all;hyphens:none;">
      You don't<br>need a<br><span style="background:{HOLO_GRAD};-webkit-background-clip:text;
      -webkit-text-fill-color:transparent;background-clip:text;font-style:italic;">degree in it.</span>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:#9FB3CE;
                 margin-top:22px;line-height:1.35;">
      You need one thing they can click. Here are 5 that work for any subject.
    </div>
  </div>
  <div style="width:342px;height:486px;flex-shrink:0;transform:rotate(4deg);">
    {_holo_frame(card_inner, pad=5, radius=22, extra="height:100%;")}
  </div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;">
  {_card_number(1)}
  <div style="font-family:'DM Sans';font-weight:500;font-size:20px;color:{STAT_GREY};">SWIPE &rarr;</div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 2: The Data ─────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("76%", "of hiring managers say a portfolio link changes their read of a CV", HOLO_3),
        ("11%", "of non-design grads actually have one", HOLO_1),
        ("1", "clickable thing is all it takes to be in the 11%", HOLO_2),
    ]
    cards = ""
    for i, (val, label, color) in enumerate(stats):
        inner = f"""<div style="padding:28px 24px;height:100%;display:flex;flex-direction:column;">
  {_rarity("STAT", color)}
  <div style="flex:1;display:flex;align-items:center;">
    <div style="font-family:Inter;font-weight:700;font-size:92px;color:{color};
                 letter-spacing:-4px;line-height:1;">{val}</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#B8C8DE;line-height:1.35;">{label}</div>
</div>"""
        cards += f'<div style="flex:1;">{_holo_frame(inner, pad=4, radius=18, extra="height:100%;")}</div>'
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:19px;
               background:{HOLO_GRAD};-webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;letter-spacing:4px;text-transform:uppercase;margin-bottom:12px;">The odds</div>
  <div style="font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Almost nobody <span style="background:{HOLO_GRAD};-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;background-clip:text;font-style:italic;">bothers.</span>
  </div>
</div>
<div style="flex:1;display:flex;gap:20px;margin:34px 0 20px 0;">{cards}</div>
<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;">
  {_card_number(2)}
  <div style="font-family:'DM Sans';font-weight:400;font-size:20px;color:{STAT_GREY};">
    Sources: LinkedIn Hiring Report 2026, Prospects Grad Survey 2025
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slides 3-6: The 5 portfolio cards ─────────────────────────────────────
def _card_slide(out, n, rarity_txt, rarity_col, title, subtitle, what, example, stats):
    f = _fonts()
    bars = ""
    for label, val, pct, color in stats:
        bars += _stat_bar(label, val, pct, color)
    card_inner = f"""
<div style="padding:26px 24px;height:100%;display:flex;flex-direction:column;">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    {_rarity(rarity_txt, rarity_col)}
    <div style="font-family:Inter;font-weight:700;font-size:17px;color:{STAT_GREY};letter-spacing:2px;">{n-2:02d}/05</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding:16px 0;">
    <div style="font-family:Inter;font-weight:700;font-size:44px;line-height:0.98;color:white;
                 letter-spacing:-2px;word-break:keep-all;hyphens:none;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:700;font-style:italic;font-size:22px;
                 color:{rarity_col};margin-top:8px;">{subtitle}</div>
  </div>
  <div style="border-top:2px solid rgba(255,255,255,0.10);padding-top:14px;">{bars}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex:1;display:flex;align-items:center;gap:36px;">
  <div style="width:330px;height:470px;flex-shrink:0;transform:rotate(-3deg);">
    {_holo_frame(card_inner, pad=5, radius=22, extra="height:100%;")}
  </div>
  <div style="flex:1;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:19px;color:{rarity_col};
                 letter-spacing:4px;text-transform:uppercase;margin-bottom:14px;">{rarity_txt}</div>
    <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;color:white;
                 letter-spacing:-2px;word-break:keep-all;hyphens:none;margin-bottom:22px;">{title}</div>
    <div style="background:rgba(255,255,255,0.05);border-left:4px solid {rarity_col};
                 border-radius:0 12px 12px 0;padding:20px 22px;margin-bottom:18px;">
      <div style="font-family:Inter;font-weight:700;font-size:18px;color:{STAT_GREY};
                   letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">What it is</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:#D0DDEC;line-height:1.4;">{what}</div>
    </div>
    <div style="background:rgba(255,255,255,0.05);border-left:4px solid {rarity_col};
                 border-radius:0 12px 12px 0;padding:20px 22px;">
      <div style="font-family:Inter;font-weight:700;font-size:18px;color:{STAT_GREY};
                   letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Real example</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:#D0DDEC;line-height:1.4;">{example}</div>
    </div>
  </div>
</div>
<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;">
  {_card_number(n)}
  <img src="data:image/png;base64,{LOGO_W}" style="height:38px;opacity:0.45;">
</div>
</div></body></html>"""
    _render(html, out)


def _slide3(out): _card_slide(out, 3, "COMMON", HOLO_2,
    "The teardown",
    "any subject, 1 weekend",
    "Pick a company you want to work for. Analyse one thing they do. Write 800 words on what you'd change and why.",
    "An English grad wrote a teardown of a fintech's onboarding copy. Got hired by their content team.",
    [("Effort", "LOW", 30, HOLO_3), ("Signal", "8.2", 82, HOLO_2), ("Reusable", "9.0", 90, FOIL_GOLD)])

def _slide4(out): _card_slide(out, 4, "RARE", HOLO_3,
    "The rebuild",
    "show, don't claim",
    "Rebuild a small piece of something that exists. Badly is fine. Ship it and write up what broke and what you learned.",
    "A history grad rebuilt their council's bin-collection lookup as a working web app. Two interviews from one link.",
    [("Effort", "MED", 58, AMBER), ("Signal", "9.4", 94, HOLO_3), ("Reusable", "7.5", 75, HOLO_2)])

def _slide5(out): _card_slide(out, 5, "RARE", HOLO_1,
    "The data story",
    "one chart, one insight",
    "Find a public dataset about something you care about. Ask one question. Answer it with one clear chart and 300 words.",
    "A geography grad mapped 5 years of local flooding data. It landed them an analyst role at an insurer.",
    [("Effort", "MED", 55, AMBER), ("Signal", "8.8", 88, HOLO_1), ("Reusable", "8.4", 84, HOLO_2)])

def _slide6(out): _card_slide(out, 6, "ULTRA RARE", FOIL_GOLD,
    "The receipts page",
    "the one everyone skips",
    "One page. Every project, with the outcome and a link. Not a CV. A menu of proof they can click through in 90 seconds.",
    "A Notion page, a free site, even a public Google Doc. The format matters far less than the fact it exists.",
    [("Effort", "LOW", 26, HOLO_3), ("Signal", "9.6", 96, FOIL_GOLD), ("Reusable", "10", 100, FOIL_GOLD)])


# ─── Slide 7: CTA — full pack spread ──────────────────────────────────────
def _slide7(out):
    f = _fonts()
    mini = ""
    labels = [("Teardown", HOLO_2), ("Rebuild", HOLO_3), ("Data story", HOLO_1),
              ("Receipts", FOIL_GOLD), ("Ship it", "#B98BFF")]
    for i, (lbl, col) in enumerate(labels):
        rot = -8 + (i * 4)
        inner = f"""<div style="padding:18px 12px;height:100%;display:flex;flex-direction:column;
             justify-content:space-between;align-items:center;text-align:center;
             background:linear-gradient(160deg,{col}22 0%,transparent 55%);">
  <div style="width:100%;height:5px;background:{col};border-radius:3px;"></div>
  <div style="font-family:Inter;font-weight:700;font-size:23px;color:white;
               letter-spacing:-0.5px;word-break:keep-all;hyphens:none;line-height:1.1;">{lbl}</div>
  <div style="font-family:Inter;font-weight:700;font-size:15px;color:{col};letter-spacing:2px;">0{i+1}</div>
</div>"""
        mini += f"""<div style="width:172px;height:244px;transform:rotate({rot}deg);
             margin-left:{-16 if i > 0 else 0}px;">
  {_holo_frame(inner, pad=3, radius=14, extra="height:100%;")}
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:56px;">
  <div style="background:{HOLO_GRAD};padding:3px;border-radius:8px;transform:rotate(-3deg);">
    <div style="background:{CARD_VOID};padding:10px 18px;border-radius:6px;
                 font-family:Inter;font-weight:700;font-size:19px;color:white;
                 letter-spacing:2px;text-transform:uppercase;">Full set</div>
  </div>
</div>

<div style="flex-shrink:0;margin-top:30px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:19px;
               background:{HOLO_GRAD};-webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;letter-spacing:4px;text-transform:uppercase;margin-bottom:14px;">Your turn</div>
  <div style="font-family:Inter;font-weight:700;font-size:78px;line-height:0.95;color:white;
               letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    Pick one. Ship it<br><span style="background:{HOLO_GRAD};-webkit-background-clip:text;
    -webkit-text-fill-color:transparent;background-clip:text;font-style:italic;">this weekend.</span>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:#9FB3CE;
               margin-top:18px;line-height:1.35;max-width:820px;">
    One clickable link puts you in the 11%. It does not need to be perfect. It needs to exist.
  </div>
</div>

<div style="flex:1;display:flex;align-items:center;justify-content:center;margin-top:-8px;">{mini}</div>

<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;">
  <div style="background:{HOLO_GRAD};padding:4px;border-radius:60px;">
    <div style="background:{CARD_VOID};padding:16px 30px;border-radius:56px;
                 font-family:Inter;font-weight:700;font-size:24px;color:white;">
      Find roles at internwise.co.uk &rarr;
    </div>
  </div>
  {_card_number(7)}
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Portfolio Play (Week 8, Day 3)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("holographic_trading_card_panini", "week8/d3-portfolio", "week8")
    print("Done - portfolio complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week8/d3-portfolio")
