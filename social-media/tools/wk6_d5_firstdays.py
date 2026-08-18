"""
Internwise - First 30 Days at a New Job (Week 6, Day 5)
Hook: DEEP_BLUE bg, giant ghost "30", person floating bottom-CENTRE (not corner).
Different from D3 wk5 (floating person corner-right with ghost letter).
Accent: AMBER. 7 slides.
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
OFF_WHITE = "#FAF5EC"

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
def _num_badge(n, bg=AMBER, fg=DARK_NAVY):
    return f'<div style="position:absolute;top:44px;left:44px;width:52px;height:52px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};z-index:25;">{n}</div>'
def _kicker(text, color=AMBER):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">{text}</div>'


# ── Slide 1: Hook — DEEP_BLUE bg, ghost "30", person bottom-centre ─────────────
def _slide1(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DEEP_BLUE};}}
.c{{width:1080px;height:1080px;position:relative;}}
{GRAIN}
.ghost{{position:absolute;bottom:-80px;left:50%;transform:translateX(-50%);
         font-family:Inter;font-weight:700;font-size:700px;line-height:1;
         color:white;opacity:0.06;z-index:3;user-select:none;letter-spacing:-30px;
         white-space:nowrap;}}
.person{{position:absolute;bottom:0;left:50%;transform:translateX(-50%);
          width:500px;height:720px;z-index:10;
          filter:drop-shadow(0 20px 60px rgba(0,0,0,0.6));}}
.person img{{width:100%;height:100%;object-fit:contain;object-position:bottom center;}}
.top-text{{position:absolute;top:0;left:0;right:0;padding:44px 60px;z-index:20;
            display:flex;justify-content:space-between;align-items:flex-start;}}
.hl-left{{z-index:20;position:absolute;left:50px;top:150px;width:400px;}}
.hl-right{{z-index:20;position:absolute;right:50px;top:150px;width:380px;text-align:right;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_white()}
<div class="ghost">30</div>
<div class="person"><img src="{photo_src}"></div>
<div class="hl-left">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{AMBER};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:14px;">First 30 days</div>
  <div style="font-family:Inter;font-weight:700;font-size:72px;line-height:0.9;
               color:white;letter-spacing:-4px;word-break:keep-all;hyphens:none;">
    The month<br>that sets<br><em style="color:{AMBER};">everything.</em>
  </div>
</div>
<div class="hl-right">
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.5);
               line-height:1.4;margin-top:20px;">How you start shapes how they see you for the first year.</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: Week 1 — listen and observe ──────────────────────────────────────
def _slide2(out):
    f = _fonts()
    items = [
        ("Learn before you contribute", "You don't know what you don't know yet. In week 1, your job is to understand how decisions get made, not to make them."),
        ("Map the informal org chart", "Who actually influences things? Who do people go to with real problems? The org chart won't tell you this — watching will."),
        ("Ask questions you can't google", "How is success measured here? What does excellent work look like? Who should I make sure I meet?"),
    ]
    rows = "".join([f"""<div style="background:rgba(255,255,255,0.05);border-radius:14px;padding:22px 24px;
                          border-left:4px solid {AMBER};">
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;
               word-break:keep-all;hyphens:none;">{t}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;
               color:rgba(255,255,255,0.6);margin-top:7px;line-height:1.4;">{d}</div>
</div>""" for t, d in items])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:26px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div style="padding-top:60px;">{_kicker("WEEK 1")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Don't impress. <em style="color:{AMBER};font-style:italic;">Understand.</em></div></div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;">{rows}</div>
<div style="background:rgba(255,177,32,0.15);border:2px solid {AMBER};border-radius:12px;
             padding:16px 24px;font-family:'DM Sans';font-weight:700;font-size:18px;color:{AMBER};">
The fastest way to earn trust in week 1 is to ask smart questions, not to have all the answers.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: Week 2 — first visible contribution ──────────────────────────────
def _slide3(out):
    f = _fonts()
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
<div style="padding-top:60px;">{_kicker("WEEK 2")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Own one thing. <em style="color:{AMBER};font-style:italic;">Deliver it.</em></div></div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;">
  <div style="flex:1;background:rgba(255,177,32,0.1);border:2px solid {AMBER};
               border-radius:16px;padding:26px 28px;">
    <div style="font-family:Inter;font-weight:700;font-size:22px;color:{AMBER};margin-bottom:12px;word-break:keep-all;hyphens:none;">
      Pick the right first task</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.7);line-height:1.45;">
      Not the biggest, flashiest project. Something with a clear output that you can finish cleanly in the first 2 weeks.
      Finish it early. Document it. Let the right people see the outcome.
    </div>
  </div>
  <div style="display:flex;gap:16px;">
    <div style="flex:1;background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 20px;">
      <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;margin-bottom:8px;word-break:keep-all;hyphens:none;">
        Avoid</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.5);line-height:1.4;">
        Spreading across 5 tasks and completing none well. Half-done work in week 2 sets a pattern that's hard to reverse.</div>
    </div>
    <div style="flex:1;background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 20px;">
      <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;margin-bottom:8px;word-break:keep-all;hyphens:none;">
        Do instead</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.5);line-height:1.4;">
        One task. Clear deadline. Over-deliver on quality, not quantity. Then ask what's next.</div>
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: Build relationships early ────────────────────────────────────────
def _slide4(out):
    f = _fonts()
    targets = [
        ("Your direct manager", AMBER, "Get 30 minutes in week 1 to understand their priorities, not yours. Ask what a great first 3 months looks like to them."),
        ("The person who's been there longest", CORAL, "They know how things really work. The shortcuts, the politics, the unwritten rules. Worth one coffee."),
        ("Your peer group", PURPLE, "The people at your level in adjacent teams. They'll be your network in 5 years. Invest early."),
        ("Someone outside your team", MINT, "Reach across functions. Finance, ops, marketing. Breadth of connection is a career asset."),
    ]
    cards = "".join([f"""<div style="flex:1;background:rgba(255,255,255,0.04);border:2px solid rgba(255,255,255,0.08);
                          border-radius:14px;padding:20px 18px;">
  <div style="width:10px;height:10px;border-radius:50%;background:{c};margin-bottom:12px;"></div>
  <div style="font-family:Inter;font-weight:700;font-size:28px;color:white;word-break:keep-all;hyphens:none;">{t}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.5);
               margin-top:8px;line-height:1.35;">{d}</div>
</div>""" for t, c, d in targets])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:24px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4)}
<div style="padding-top:60px;">{_kicker("RELATIONSHIPS")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
4 conversations to <em style="color:{AMBER};font-style:italic;">prioritise.</em></div></div>
<div style="flex:1;display:flex;gap:16px;">{cards}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: Common mistakes ──────────────────────────────────────────────────
def _slide5(out):
    f = _fonts()
    mistakes = [
        ("Trying to fix everything immediately", "You don't understand why things are done the way they are. Ask before suggesting changes."),
        ("Being invisible on Slack/email", "Don't go quiet. Short, clear updates on your work keep you visible without being loud."),
        ("Skipping the social stuff", "Lunch, team drinks, all-hands — the informal is where culture is built and trust is formed."),
        ("Not asking for feedback early", "Ask at the end of week 2: 'What should I be doing more of?' before small things become patterns."),
    ]
    rows = "".join([f"""<div style="display:flex;gap:14px;align-items:flex-start;padding:15px 0;
                          border-bottom:1px solid rgba(255,255,255,0.07);">
  <div style="color:{CORAL};font-size:20px;flex-shrink:0;line-height:1.2;font-weight:700;">x</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;word-break:keep-all;hyphens:none;">{t}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;
                 color:rgba(255,255,255,0.5);margin-top:5px;line-height:1.35;">{d}</div>
  </div>
</div>""" for t, d in mistakes])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:22px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(5)}
<div style="padding-top:60px;">{_kicker("WHAT TO AVOID")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
4 mistakes new starters <em style="color:{CORAL};font-style:italic;">always</em> make.</div></div>
<div style="flex:1;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: The 30-day checklist ─────────────────────────────────────────────
def _check_item(item, color):
    svg = f'<svg width="10" height="8" viewBox="0 0 10 8"><polyline points="1,4 3.5,7 9,1" stroke="white" stroke-width="2" fill="none"/></svg>'
    return (f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;">'
            f'<div style="width:18px;height:18px;border-radius:50%;background:{color};'
            f'display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;">{svg}</div>'
            f'<div style="font-family:DM Sans,sans-serif;font-weight:600;font-size:26px;'
            f'color:rgba(255,255,255,0.75);line-height:1.35;">{item}</div></div>')

def _slide6(out):
    f = _fonts()
    week_data = [
        ("Week 1", AMBER, ["Understand your manager's top 3 priorities", "Map who the key people are in your team", "Ask 3 smart questions you can't Google"]),
        ("Week 2", CORAL, ["Deliver your first visible task early", "Have coffee with one peer or cross-functional colleague", "Send a brief update to your manager on progress"]),
        ("Week 3-4", PURPLE, ["Ask for feedback proactively", "Suggest one small improvement (with evidence)", "Set up a monthly 1:1 with your manager"]),
    ]
    cols = ""
    for period, c, items in week_data:
        item_html = "".join(_check_item(it, c) for it in items)
        cols += (f'<div style="flex:1;background:rgba(255,255,255,0.04);border-radius:16px;padding:22px 20px;">'
                 f'<div style="font-family:DM Sans,sans-serif;font-weight:700;font-size:14px;color:{c};'
                 f'text-transform:uppercase;letter-spacing:2px;margin-bottom:14px;">{period}</div>'
                 f'{item_html}</div>')
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
<div style="padding-top:60px;">{_kicker("30-DAY CHECKLIST")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
The moves. The <em style="color:{AMBER};font-style:italic;">timeline.</em></div></div>
<div style="flex:1;display:flex;gap:16px;">{cols}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA — arch+cutout RIGHT, AMBER arch, OFF_WHITE bg ───────────────
def _slide7(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    checks = _checklist(["Listen and observe in week 1", "One visible task by week 2",
                          "Ask for feedback before day 30", "Build relationships across the org"],
                         AMBER, DARK_NAVY, DARK_NAVY)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;}}
{GRAIN_DARK}
.arch{{position:absolute;bottom:0;right:0;width:460px;height:680px;
       background:{AMBER};border-radius:230px 230px 0 0;z-index:5;}}
.person{{position:absolute;bottom:0;right:0;width:520px;height:740px;z-index:10;
          filter:drop-shadow(0 20px 50px rgba(255,177,32,0.4));}}
.person img{{width:100%;height:100%;object-fit:contain;object-position:bottom center;}}
.content{{position:absolute;top:0;left:0;width:580px;height:1080px;
           padding:44px 50px;display:flex;flex-direction:column;justify-content:center;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_color()}
<div class="arch"></div>
<div class="person"><img src="{photo_src}"></div>
<div class="content">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{AMBER};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;margin-top:80px;">DAY 1 ONWARDS</div>
  <div style="font-family:Inter;font-weight:700;font-size:62px;line-height:0.95;
               color:{DARK_NAVY};letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    Start strong.<br><em style="color:{AMBER};">Stay strong.</em></div>
  <div style="margin-top:28px;display:flex;flex-direction:column;gap:12px;">
    {checks}
  </div>
  <div style="margin-top:32px;background:{DARK_NAVY};color:white;padding:16px 28px;
               border-radius:50px;border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 rgba(0,0,0,0.2);
               font-family:Inter;font-weight:700;font-size:18px;display:inline-flex;
               align-items:center;gap:12px;width:fit-content;">
    Find roles at internwise.co.uk &#8594;
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating First 30 Days (Week 6, Day 5)...")
    _load_logos()
    used_before = get_used_hashes()

    photo1 = get_cutout_unique(
        "young professional at work office smiling studio white background",
        orientation="portrait", extra_exclude=used_before
    )
    hash1 = os.path.basename(photo1).replace("_nobg.png", "")

    used_after_1 = used_before | {hash1}
    photo7 = get_cutout_unique(
        "graduate professional confident arms crossed studio white background",
        orientation="portrait", extra_exclude=used_after_1
    )
    hash7 = os.path.basename(photo7).replace("_nobg.png", "")

    _slide1(os.path.join(campaign_dir, "slide_1.png"), photo1)
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photo7)

    register_used_hashes([hash1, hash7], "week6/d5-firstdays", "week6")
    register_design("deep_blue_ghost_number_person_bottom_centre", "week6/d5-firstdays", "week6")
    print("Done - first 30 days complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week6/d5-firstdays")
