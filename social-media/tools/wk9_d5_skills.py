"""
Internwise - The Skills Employers Actually Pay For in 2026 (Week 9, Day 5)
Design language: ISOMETRIC INFOGRAPHIC. 3D isometric skill "towers"/blocks built
from stacked parallelogram faces, chunky data columns, a Pexels cutout of a person
standing among the blocks. Mint + amber + blue on soft grid.
7 slides. Accent: MINT + AMBER + BLUE.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import get_used_hashes, register_used_hashes, register_design, get_cutout_unique
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; DEEP_BLUE = "#264D7E"; OFF_WHITE = "#FAF5EC"

BG        = "#EEF3F0"
INK       = "#22303C"
GREY      = "#5B6875"
MINT      = "#4FC79E"; MINT_T = "#6FE0BA"; MINT_S = "#37A07D"   # top / side shades
AMBER     = "#FFC24A"; AMBER_T= "#FFD778"; AMBER_S= "#E5A122"
BLUE      = "#5AA9E8"; BLUE_T = "#84C2F2"; BLUE_S = "#3D8AD0"
PURPLE    = "#9B84E8"; PURPLE_T="#B7A6F0"; PURPLE_S="#7B62D6"
CORAL     = "#FF7A6B"

LOGO_C = None
def _load_logos():
    global LOGO_C
    if LOGO_C is None:
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

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{BG};
      background-image:linear-gradient(rgba(90,120,110,0.07) 1px,transparent 1px),
      linear-gradient(90deg,rgba(90,120,110,0.07) 1px,transparent 1px);
      background-size:46px 46px;}}
.c{{width:1080px;height:1080px;position:relative;padding:52px 56px;display:flex;flex-direction:column;}}
"""

# Isometric column builder
def _iso_column(color_top, color_left, color_right, base_w, height, cap_label=""):
    """
    Draw one isometric column. base_w = width of one visible face, height = tall face px.
    Top face is a rhombus; left and right faces drop down by `height`.
    """
    dw = base_w            # left face width
    dd = int(base_w*0.62)  # depth (right face horizontal span)
    dy = int(dd*0.5)       # vertical offset for iso
    total_w = dw + dd
    total_h = height + dy*2 + 6
    # top-face diamond corners: A top, B right, C bottom, D left
    A = (dd, 0)
    Bp = (total_w, dy)
    Cp = (dd, dy*2)
    Dp = (0, dy)
    top_pts = f"{A[0]},{A[1]} {Bp[0]},{Bp[1]} {Cp[0]},{Cp[1]} {Dp[0]},{Dp[1]}"
    # left face: D, C down
    left_pts = f"{Dp[0]},{Dp[1]} {Cp[0]},{Cp[1]} {Cp[0]},{Cp[1]+height} {Dp[0]},{Dp[1]+height}"
    # right face: C, B down
    right_pts = f"{Cp[0]},{Cp[1]} {Bp[0]},{Bp[1]} {Bp[0]},{Bp[1]+height} {Cp[0]},{Cp[1]+height}"
    cap = ""
    if cap_label:
        cap = f'<text x="{dd}" y="{dy+2}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="30" fill="{INK}">{cap_label}</text>'
    return f"""<svg width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg" style="overflow:visible;">
  <polygon points="{left_pts}" fill="{color_left}"/>
  <polygon points="{right_pts}" fill="{color_right}"/>
  <polygon points="{top_pts}" fill="{color_top}" stroke="rgba(255,255,255,0.25)" stroke-width="1"/>
  {cap}
</svg>"""

def _kicker(text, color=MINT_S):
    return (f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:19px;color:{color};'
            f'text-transform:uppercase;letter-spacing:3px;">{text}</div>')


# ── Slide 1: Hook — skyline of iso towers + person ──────────────────────────
def _slide1(out, photo_path):
    f = _fonts()
    photo = _src(photo_path)
    # a little skyline
    towers = f"""
<div style="display:flex;align-items:flex-end;gap:-10px;">
  <div style="margin-right:-38px;">{_iso_column(AMBER_T, AMBER, AMBER_S, 92, 150)}</div>
  <div style="margin-right:-38px;">{_iso_column(MINT_T, MINT, MINT_S, 92, 250)}</div>
  <div style="margin-right:-38px;">{_iso_column(BLUE_T, BLUE, BLUE_S, 92, 190)}</div>
  <div>{_iso_column(PURPLE_T, PURPLE, PURPLE_S, 92, 110)}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:54px;">
  <div style="background:{INK};color:#fff;padding:11px 22px;border-radius:50px;
               font-family:Inter;font-weight:700;font-size:19px;letter-spacing:2px;text-transform:uppercase;">
    Skills / 2026 data
  </div>
</div>

<div style="flex:1;display:flex;align-items:center;position:relative;">
  <div style="flex:1;z-index:5;">
    {_kicker("What employers pay for", MINT_S)}
    <div style="font-family:Inter;font-weight:700;font-size:88px;line-height:0.9;color:{INK};
                 letter-spacing:-4px;margin-top:16px;word-break:keep-all;hyphens:none;">
      Build the<br>right <span style="color:{MINT_S};font-style:italic;">stack.</span>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:29px;color:{GREY};
                 margin-top:22px;line-height:1.4;max-width:500px;">
      Not every skill pays the same. Here's what actually moves a 2026 grad salary.
    </div>
  </div>
  <div style="width:440px;flex-shrink:0;position:relative;height:560px;display:flex;
               align-items:flex-end;justify-content:center;">
    <div style="position:absolute;bottom:70px;left:0;">{towers}</div>
    <img src="{photo}" style="position:relative;z-index:8;height:540px;object-fit:contain;
          filter:drop-shadow(0 20px 30px rgba(40,60,50,0.3));">
  </div>
</div>

<div style="flex-shrink:0;display:flex;justify-content:flex-end;">
  <div style="font-family:'DM Sans';font-weight:500;font-size:20px;color:{GREY};">SWIPE &rarr;</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: The ranking (iso bar chart) ────────────────────────────────────
def _slide2(out):
    f = _fonts()
    bars = [
        ("AI fluency", "+18%", 250, MINT_T, MINT, MINT_S),
        ("Data literacy", "+14%", 210, BLUE_T, BLUE, BLUE_S),
        ("Communication", "+11%", 175, AMBER_T, AMBER, AMBER_S),
        ("Project delivery", "+9%", 140, PURPLE_T, PURPLE, PURPLE_S),
    ]
    cols = ""
    for name, pct, h, t, l, s in bars:
        cols += f"""<div style="display:flex;flex-direction:column;align-items:center;gap:14px;">
  <div style="font-family:Inter;font-weight:700;font-size:34px;color:{s};letter-spacing:-1px;">{pct}</div>
  {_iso_column(t, l, s, 96, h)}
  <div style="font-family:Inter;font-weight:700;font-size:23px;color:{INK};text-align:center;max-width:170px;
               word-break:keep-all;hyphens:none;line-height:1.1;">{name}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  {_kicker("The salary premium", MINT_S)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Skills that move <span style="color:{MINT_S};font-style:italic;">the number.</span>
  </div>
</div>
<div style="flex:1;display:flex;align-items:flex-end;justify-content:space-around;gap:20px;
             padding:0 20px 30px 20px;">{cols}</div>
<div style="flex-shrink:0;font-family:'DM Sans';font-weight:400;font-size:20px;color:{GREY};text-align:right;">
  Median grad salary uplift vs baseline. Source: LinkedIn Skills Report + ONS 2026
</div>
</div></body></html>"""
    _render(html, out)


# ── Slides 3-6: the four skills, deep-dive ──────────────────────────────────
def _skill_slide(out, n, kicker, name, t, l, s, what, how, proof):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;display:flex;align-items:center;gap:28px;">
  <div style="flex-shrink:0;">{_iso_column(t, l, s, 84, 120, cap_label=str(n-2))}</div>
  <div>
    {_kicker(kicker, s)}
    <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
                 letter-spacing:-2px;margin-top:6px;word-break:keep-all;hyphens:none;">{name}</div>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:18px;margin-top:30px;justify-content:center;">
  <div style="background:#fff;border-radius:18px;padding:28px 32px;box-shadow:0 12px 26px rgba(40,70,60,0.12);border-left:8px solid {l};">
    <div style="font-family:Inter;font-weight:700;font-size:20px;color:{s};text-transform:uppercase;letter-spacing:2px;margin-bottom:9px;">What it really means</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:{INK};line-height:1.4;">{what}</div>
  </div>
  <div style="background:#fff;border-radius:18px;padding:28px 32px;box-shadow:0 12px 26px rgba(40,70,60,0.12);border-left:8px solid {l};">
    <div style="font-family:Inter;font-weight:700;font-size:20px;color:{s};text-transform:uppercase;letter-spacing:2px;margin-bottom:9px;">How to build it free</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:{INK};line-height:1.4;">{how}</div>
  </div>
  <div style="background:{l};border-radius:18px;padding:24px 32px;box-shadow:0 12px 26px rgba(40,70,60,0.18);">
    <div style="font-family:'DM Sans';font-weight:700;font-size:26px;color:#fff;line-height:1.4;">
      <span style="font-style:italic;">Prove it:</span> {proof}
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)

def _slide3(out): _skill_slide(out, 3, "Skill 01 / +18%", "AI fluency", MINT_T, MINT, MINT_S,
    "Not 'can use ChatGPT'. Can you make an AI tool actually save your team hours and check its work?",
    "Automate one real task this month - a report, an email triage, a data clean. Document what you built.",
    "A public write-up: 'I cut our society's admin from 4 hours to 20 minutes with an AI workflow.'")

def _slide4(out): _skill_slide(out, 4, "Skill 02 / +14%", "Data literacy", BLUE_T, BLUE, BLUE_S,
    "Reading numbers without panic. Spotting what a chart is hiding. Asking the second question.",
    "Take one public dataset and answer one question with one clean chart. Repeat monthly.",
    "A dashboard or a chart with a one-line insight recruiters can click through in 30 seconds.")

def _slide5(out): _skill_slide(out, 5, "Skill 03 / +11%", "Communication", AMBER_T, AMBER, AMBER_S,
    "Explaining a complex thing simply. Writing an email that gets a fast yes. Presenting without waffle.",
    "Write in public weekly. Every post is reps. Join a society committee and run one meeting well.",
    "A LinkedIn post that got real comments, or a talk you gave. Evidence you can move a room.")

def _slide6(out): _skill_slide(out, 6, "Skill 04 / +9%", "Project delivery", PURPLE_T, PURPLE, PURPLE_S,
    "Taking something from idea to shipped, on time, with other people involved. The rarest grad skill.",
    "Finish one thing end-to-end and get it in front of real users. A site, an event, a small product.",
    "A shipped project with an outcome: 'I ran it, 120 people came, here's what I'd change.'")


# ── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    stack = f"""
<div style="display:flex;flex-direction:column;align-items:center;">
  <div style="margin-bottom:-46px;z-index:4;">{_iso_column(MINT_T, MINT, MINT_S, 150, 70, cap_label="AI")}</div>
  <div style="margin-bottom:-46px;z-index:3;">{_iso_column(BLUE_T, BLUE, BLUE_S, 150, 70, cap_label="Data")}</div>
  <div style="margin-bottom:-46px;z-index:2;">{_iso_column(AMBER_T, AMBER, AMBER_S, 150, 70, cap_label="Comms")}</div>
  <div style="z-index:1;">{_iso_column(PURPLE_T, PURPLE, PURPLE_S, 150, 70, cap_label="Deliver")}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:54px;">
  <div style="background:{MINT_S};color:#fff;padding:11px 22px;border-radius:50px;
               font-family:Inter;font-weight:700;font-size:19px;letter-spacing:2px;text-transform:uppercase;">Build it</div>
</div>
<div style="flex:1;display:flex;align-items:center;gap:40px;">
  <div style="flex:1;">
    {_kicker("Your stack", MINT_S)}
    <div style="font-family:Inter;font-weight:700;font-size:78px;line-height:0.94;color:{INK};
                 letter-spacing:-3px;margin-top:14px;word-break:keep-all;hyphens:none;">
      Stack the<br>skills that <span style="color:{MINT_S};font-style:italic;">pay.</span>
    </div>
    <div style="background:#fff;border-radius:20px;padding:28px 32px;margin-top:28px;
                 box-shadow:0 14px 30px rgba(40,70,60,0.14);max-width:560px;">
      <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:{INK};line-height:1.5;">
        Pick <span style="font-weight:700;color:{MINT_S};">one</span> this month. Build it in public.
        Then the next. Four skills, four months, a stack recruiters chase.
      </div>
    </div>
    <div style="margin-top:26px;background:{INK};color:#fff;display:inline-flex;align-items:center;gap:12px;
                 padding:18px 32px;border-radius:50px;font-family:Inter;font-weight:700;font-size:24px;">
      Find roles at internwise.co.uk &rarr;
    </div>
  </div>
  <div style="width:280px;flex-shrink:0;display:flex;align-items:center;justify-content:center;">{stack}</div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Skills 2026 (Week 9, Day 5)...")
    _load_logos()
    used = get_used_hashes()
    photo = get_cutout_unique(
        "confident young professional standing full body studio white background",
        orientation="portrait", extra_exclude=used
    )
    h = os.path.basename(photo).replace("_nobg.png", "")
    _slide1(os.path.join(campaign_dir, "slide_1.png"), photo)
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_used_hashes([h], "week9/d5-skills", "week9")
    register_design("isometric_3d_skill_towers", "week9/d5-skills", "week9")
    print("Done - skills complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week9/d5-skills")
