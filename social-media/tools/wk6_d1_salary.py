"""
Internwise - Salary Negotiation (Week 6, Day 1)
Hook: Two-panel split — left DEEP_BLUE giant £ number, right OFF_WHITE hook text.
Accent: DEEP_BLUE. 7 slides.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import get_used_hashes, register_used_hashes, register_design, get_cutout_unique
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")
CACHE_DIR    = os.path.join(BASE_DIR, "assets", "pexels_cache")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"

# ── Mobile-safe font sizes (1080px canvas, viewed ~390px wide on phone) ───────
# Headline:   52px min  |  Card title: 26px min
# Body text:  28px min  |  Kicker:     18px min  |  Fine print: 20px min

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

def _checklist(items, dot_bg, dot_fg, text_color):
    svg = f'<svg width="11" height="9" viewBox="0 0 11 9"><polyline points="1,4.5 4,7.5 10,1" stroke="{dot_fg}" stroke-width="2" fill="none"/></svg>'
    rows = ""
    for t in items:
        rows += (f'<div style="display:flex;align-items:center;gap:12px;">'
                 f'<div style="width:20px;height:20px;border-radius:50%;background:{dot_bg};'
                 f'display:flex;align-items:center;justify-content:center;flex-shrink:0;">{svg}</div>'
                 f'<div style="font-family:DM Sans,sans-serif;font-weight:600;font-size:26px;color:{text_color};">{t}</div></div>')
    return rows

def _logo_white(): return f'<img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:44px;left:44px;height:68px;z-index:25;">'
def _logo_color(): return f'<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:44px;left:44px;height:68px;z-index:25;">'
def _num_badge(n, bg=DEEP_BLUE, fg="white"):
    return f'<div style="position:absolute;top:44px;left:44px;width:52px;height:52px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};z-index:25;">{n}</div>'
def _kicker(text, color=AMBER):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:16px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">{text}</div>'
def _tag(text, bg=DEEP_BLUE, fg="white"):
    return f'<div style="position:absolute;top:44px;right:44px;background:{bg};color:{fg};padding:10px 22px;border-radius:50px;font-family:Inter;font-weight:700;font-size:13px;letter-spacing:2px;text-transform:uppercase;border:3px solid {DARK_NAVY};box-shadow:3px 3px 0 {DARK_NAVY};z-index:20;">'


# ── Slide 1: Hook — two-panel split, giant £ number ───────────────────────────
def _slide1(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.wrap{{width:1080px;height:1080px;display:flex;position:relative;}}
{GRAIN}
.left{{width:490px;height:1080px;background:{DEEP_BLUE};flex-shrink:0;
       display:flex;flex-direction:column;justify-content:center;align-items:center;
       padding:60px 40px;position:relative;}}
.right{{flex:1;background:{OFF_WHITE};display:flex;flex-direction:column;
        justify-content:center;padding:60px 50px 60px 50px;position:relative;}}
.big-num{{font-family:Inter;font-weight:700;font-size:140px;line-height:0.85;
           color:white;letter-spacing:-6px;}}
.big-label{{font-family:'DM Sans';font-weight:700;font-size:18px;color:rgba(255,255,255,0.5);
             letter-spacing:2px;text-transform:uppercase;margin-top:16px;}}
.divider{{position:absolute;right:-3px;top:0;width:6px;height:100%;background:{AMBER};z-index:10;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:16px;color:{DEEP_BLUE};
          text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;}}
.hl{{font-family:Inter;font-weight:700;font-size:58px;line-height:1.0;
      color:{DARK_NAVY};letter-spacing:-3px;word-break:keep-all;hyphens:none;}}
.hl em{{color:{CORAL};font-style:italic;}}
.sub{{font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(22,45,74,0.55);
       margin-top:24px;line-height:1.45;}}
.dot{{display:inline-block;width:10px;height:10px;border-radius:50%;background:{AMBER};margin-right:8px;}}
</style></head><body><div class="wrap">
<div class="grain"></div>
<div class="left">
  <img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:44px;left:44px;height:60px;z-index:25;">
  <div class="big-num">£3K</div>
  <div class="big-label">left on the table</div>
  <div class="divider"></div>
</div>
<div class="right">
  <div class="kicker">Salary negotiation</div>
  <div class="hl">The ask that<br>most people<br>never <em>make.</em></div>
  <div class="sub"><span class="dot"></span>Average graduate leaves £3K per year unclaimed.<br><span class="dot"></span>Most employers expect to negotiate.<br><span class="dot"></span>One conversation. Done.</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: Do employers expect negotiation? ─────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("73%", "of employers expect graduates to negotiate salary."),
        ("£3,000", "average gap between first offer and what was achievable."),
        ("84%", "of recruiters say a negotiation attempt does not hurt your chances."),
    ]
    cards = ""
    colors = [DEEP_BLUE, AMBER, CORAL]
    for i, (num, text) in enumerate(stats):
        cards += f"""<div style="flex:1;background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);
                         border-radius:16px;padding:32px 28px;display:flex;flex-direction:column;gap:14px;">
  <div style="font-family:Inter;font-weight:700;font-size:64px;line-height:1;
               color:{colors[i]};letter-spacing:-3px;">{num}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;
               color:rgba(255,255,255,0.75);line-height:1.4;">{text}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:32px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div style="padding-top:60px;">{_kicker("THE DATA")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Most employers <em style="color:{AMBER};font-style:italic;">expect</em> you to negotiate.</div></div>
<div style="flex:1;display:flex;gap:20px;">{cards}</div>
<div style="font-family:'DM Sans';font-weight:500;font-size:18px;color:rgba(255,255,255,0.3);
             text-align:right;">Sources: Glassdoor Salary Survey 2025, NACE Job Outlook 2026</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: When and how to bring it up ──────────────────────────────────────
def _slide3(out):
    f = _fonts()
    steps = [
        ("Wait for the offer", "Never negotiate before an offer is made. You lose leverage the moment you bring salary up first."),
        ("Express genuine enthusiasm", "Start with: 'I'm really excited about this role.' Anchors the negotiation in a positive frame."),
        ("State your number", "Be specific. 'Based on my research and the role scope, I was hoping for £X.' Ranges get split at the bottom."),
        ("Then stop talking", "Silence is your most powerful tool after stating a number. Don't fill it. Wait for their response."),
    ]
    rows = ""
    for i, (title, desc) in enumerate(steps):
        rows += f"""<div style="display:flex;gap:20px;align-items:flex-start;
                        background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 24px;
                        border-left:4px solid {DEEP_BLUE};">
  <div style="width:40px;height:40px;border-radius:50%;background:{DEEP_BLUE};flex-shrink:0;
               display:flex;align-items:center;justify-content:center;font-family:Inter;
               font-weight:700;font-size:18px;color:white;">{i+1}</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;
                 word-break:keep-all;hyphens:none;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;
                 color:rgba(255,255,255,0.6);margin-top:6px;line-height:1.4;">{desc}</div>
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:24px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(3)}
<div style="padding-top:60px;">{_kicker("THE SCRIPT")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Four moves. In <em style="color:{AMBER};font-style:italic;">this</em> order.</div></div>
<div style="flex:1;display:flex;flex-direction:column;gap:14px;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: What to research first ──────────────────────────────────────────
def _slide4(out):
    f = _fonts()
    items = [
        ("Glassdoor & Levels.fyi", "Role + company + city. Use median, not average."),
        ("LinkedIn Salary Insights", "Filter by years of experience and location."),
        ("High Fliers / ISE reports", "Sector benchmarks for UK graduate roles specifically."),
        ("Your offer letter scope", "More responsibilities than the job title suggests = stronger case."),
    ]
    cards = "".join([f"""<div style="background:rgba(38,77,126,0.35);border:2px solid {DEEP_BLUE};
                          border-radius:14px;padding:24px 28px;">
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:{AMBER};
               word-break:keep-all;hyphens:none;">{t}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;
               color:rgba(255,255,255,0.65);margin-top:8px;line-height:1.4;">{d}</div>
</div>""" for t, d in items])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:24px;}}
{GRAIN}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4)}
<div style="padding-top:60px;">{_kicker("YOUR RESEARCH")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Know your <em style="color:{AMBER};font-style:italic;">number</em> before you call.</div></div>
<div class="grid">{cards}</div>
<div style="background:{DEEP_BLUE};border-radius:12px;padding:16px 24px;
             font-family:'DM Sans';font-weight:700;font-size:18px;color:white;">
Research the market range, not just the number you want. A justified ask is harder to refuse.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: What to do if they say no ───────────────────────────────────────
def _slide5(out):
    f = _fonts()
    rows_data = [
        ("Counter: ask for a review date", f'<em style="color:{AMBER};">"Can we schedule a salary review at 6 months if I hit X milestones?"</em>'),
        ("Counter: ask for a sign-on bonus", "One-time payment, doesn't affect headcount budget. Often easier to approve."),
        ("Counter: ask for additional benefits", "Extra annual leave, remote working, training budget, earlier promotion review."),
        ("Know your walk-away number", "Decide it before the call. A number you'll regret accepting is worse than a polite decline."),
    ]
    rows = "".join([f"""<div style="display:flex;gap:16px;align-items:flex-start;padding:18px 0;
                          border-bottom:1px solid rgba(255,255,255,0.08);">
  <div style="width:10px;height:10px;border-radius:50%;background:{DEEP_BLUE};flex-shrink:0;margin-top:8px;"></div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;word-break:keep-all;hyphens:none;">{t}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.6);margin-top:6px;line-height:1.4;">{d}</div>
  </div>
</div>""" for t, d in rows_data])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:24px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(5)}
<div style="padding-top:60px;">{_kicker("IF THEY SAY NO")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
No doesn't mean <em style="color:{CORAL};font-style:italic;">never.</em></div></div>
<div style="flex:1;">{rows}</div>
<div style="background:rgba(255,107,107,0.15);border:2px solid {CORAL};border-radius:12px;
             padding:16px 24px;font-family:'DM Sans';font-weight:700;font-size:20px;color:{CORAL};">
A polished 'no thank you' burns no bridges. Accepting a number you resent does.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: Exact scripts to use ────────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    scripts = [
        ("Opening move", f'"I\'m really excited about this offer. Based on my research into the market rate for this role in [city], I was hoping we could get to £[X]. Is there any flexibility there?"'),
        ("After pushback", f'"I understand. Could we agree to a salary review at the 6-month mark tied to specific milestones? I\'d feel confident about hitting those."'),
        ("Sign-on ask", f'"If the base isn\'t flexible, would a one-time sign-on bonus be something you could consider?"'),
    ]
    cards = "".join([f"""<div style="background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);
                          border-radius:16px;padding:26px 28px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{AMBER};
               text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;">{label}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.8);
               line-height:1.5;font-style:italic;">{script}</div>
</div>""" for label, script in scripts])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:24px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6)}
<div style="padding-top:60px;">{_kicker("EXACT SCRIPTS")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Words that <em style="color:{AMBER};font-style:italic;">work.</em> Use these.</div></div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;">{cards}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA — arch+cutout, OFF_WHITE bg ─────────────────────────────────
def _slide7(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    checks = _checklist(["Research your market rate first", "Express enthusiasm before asking",
                          "Have a walk-away number ready", "Silence after the ask is powerful"],
                         DEEP_BLUE, "white", DARK_NAVY)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;}}
{GRAIN_DARK}
.arch{{position:absolute;bottom:0;right:0;width:460px;height:680px;
       background:{DEEP_BLUE};border-radius:230px 230px 0 0;z-index:5;}}
.person{{position:absolute;bottom:0;right:0;width:520px;height:740px;z-index:10;
          filter:drop-shadow(0 20px 50px rgba(38,77,126,0.4));}}
.person img{{width:100%;height:100%;object-fit:contain;object-position:bottom center;}}
.content{{position:absolute;top:0;left:0;width:580px;height:1080px;
           padding:44px 50px;display:flex;flex-direction:column;justify-content:center;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_color()}
<div class="arch"></div>
<div class="person"><img src="{photo_src}"></div>
<div class="content">
  <div style="font-family:'DM Sans';font-weight:700;font-size:16px;color:{DEEP_BLUE};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;margin-top:80px;">BEFORE YOU SIGN</div>
  <div style="font-family:Inter;font-weight:700;font-size:60px;line-height:0.95;
               color:{DARK_NAVY};letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    Ask once.<br><em style="color:{CORAL};">Always.</em></div>
  <div style="margin-top:28px;display:flex;flex-direction:column;gap:12px;">
    {checks}
  </div>
  <div style="margin-top:32px;background:{DEEP_BLUE};color:white;padding:16px 28px;
               border-radius:50px;border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};
               font-family:Inter;font-weight:700;font-size:18px;display:inline-flex;
               align-items:center;gap:12px;width:fit-content;">
    Find roles at internwise.co.uk &#8594;
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Salary Negotiation (Week 6, Day 1)...")
    _load_logos()
    used_before = get_used_hashes()

    photo_path = get_cutout_unique(
        "young professional confident studio white background",
        orientation="portrait",
        extra_exclude=used_before
    )
    photo_hash = os.path.basename(photo_path).replace("_nobg.png", "")

    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photo_path)

    register_used_hashes([photo_hash], "week6/d1-salary", "week6")
    register_design("two_panel_split_number", "week6/d1-salary", "week6")
    print("Done - salary negotiation complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week6/d1-salary")
