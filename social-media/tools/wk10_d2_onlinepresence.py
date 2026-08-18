"""
Internwise - Clean Up Your Online Presence (Week 10, Day 2)
Design language: RETRO DESKTOP OS. Light desktop, app windows with title bars +
traffic lights, browser tabs, cursor, notification badges, a "profile audit" scan.
7 slides. Accent: DEEP_BLUE window chrome + CORAL alerts on a soft desktop.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"; CORAL = "#FF6B6B"
MINT = "#7FDBB6"; OFF_WHITE = "#FAF5EC"; PURPLE = "#7B5CE6"
DESKTOP1 = "#DCE6F5"; DESKTOP2 = "#C4D3EC"
INK = "#1C2A3A"; GREY = "#64748b"
WIN = "#FFFFFF"; BAR = "#EEF2F8"

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

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;
      background:radial-gradient(ellipse at 30% 20%,{DESKTOP1} 0%,{DESKTOP2} 100%);}}
.c{{width:1080px;height:1080px;position:relative;padding:0;display:flex;flex-direction:column;}}
.menubar{{height:40px;background:rgba(255,255,255,0.55);display:flex;align-items:center;
          justify-content:space-between;padding:0 22px;flex-shrink:0;
          font-family:Inter;font-weight:600;font-size:16px;color:{INK};backdrop-filter:blur(6px);}}
.body{{flex:1;position:relative;padding:44px 52px;display:flex;flex-direction:column;}}
"""

def _titlebar(title, accent=DEEP_BLUE):
    return f"""<div style="height:44px;background:{BAR};border-radius:14px 14px 0 0;display:flex;
             align-items:center;padding:0 16px;gap:8px;border-bottom:1px solid #E2E8F0;">
  <div style="width:13px;height:13px;border-radius:50%;background:#FF5F57;"></div>
  <div style="width:13px;height:13px;border-radius:50%;background:#FEBC2E;"></div>
  <div style="width:13px;height:13px;border-radius:50%;background:#28C840;"></div>
  <div style="flex:1;text-align:center;font-family:Inter;font-weight:700;font-size:17px;color:{GREY};
               margin-right:52px;">{title}</div>
</div>"""

def _window(title, inner, extra="", accent=DEEP_BLUE):
    return f"""<div style="background:{WIN};border-radius:16px;box-shadow:0 20px 50px rgba(40,77,126,0.22);
             overflow:hidden;{extra}">
  {_titlebar(title, accent)}
  <div style="padding:26px 28px;">{inner}</div>
</div>"""

def _cursor(top, left, rot=0):
    return f"""<svg width="40" height="46" viewBox="0 0 40 46" style="position:absolute;top:{top};left:{left};
             transform:rotate({rot}deg);z-index:40;filter:drop-shadow(0 3px 5px rgba(0,0,0,0.3));">
  <path d="M4 2 L4 38 L13 30 L20 44 L27 41 L20 27 L33 27 Z" fill="#fff" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/></svg>"""

def _menubar():
    return f"""<div class="menubar">
  <div style="display:flex;gap:20px;"><span style="font-weight:700;">&#63743;</span><span>Profile</span><span>Edit</span><span>View</span></div>
  <div style="display:flex;gap:16px;"><span>&#128246;</span><span>100%</span><span>Fri 09:41</span></div>
</div>"""

def _shell(body_inner, f):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_base_css(f)}</style></head>
<body><div class="c">{_menubar()}<div class="body">{body_inner}</div></div></body></html>"""

def _kicker(t, c=CORAL):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{c};text-transform:uppercase;letter-spacing:3px;">{t}</div>'

def _head(html, size=56):
    return f'<div style="font-family:Inter;font-weight:700;font-size:{size}px;line-height:1.0;color:{INK};letter-spacing:-2px;word-break:keep-all;hyphens:none;">{html}</div>'


# ── Slide 1: Hook ───────────────────────────────────────────────────────────
def _slide1(out):
    f = _fonts()
    audit = f"""
<div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;">
  <div style="width:56px;height:56px;border-radius:14px;background:{CORAL};display:flex;align-items:center;
               justify-content:center;font-size:30px;">&#128269;</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:{INK};">Scanning your public profile...</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:19px;color:{GREY};">What a recruiter sees in 30 seconds</div>
  </div>
</div>
<div style="height:12px;background:#EEF2F8;border-radius:6px;overflow:hidden;">
  <div style="height:100%;width:72%;background:linear-gradient(90deg,{CORAL},{AMBER});border-radius:6px;"></div>
</div>
<div style="display:flex;justify-content:space-between;margin-top:10px;font-family:'DM Sans';font-weight:600;font-size:17px;color:{GREY};">
  <span>3 things to fix found</span><span style="color:{CORAL};">72%</span>
</div>"""
    body = f"""
<div style="flex-shrink:0;">
  {_kicker("Before you apply")}
  <div style="margin-top:14px;">{_head('Google yourself.<br>Then <span style="color:'+CORAL+';">clean it up.</span>', 72)}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:29px;color:{GREY};margin-top:20px;max-width:600px;line-height:1.35;">
    75% of recruiters check your socials before they call. Beat them to it.
  </div>
</div>
<div style="flex:1;display:flex;align-items:center;">
  <div style="width:640px;">{_window("Profile Audit", audit)}</div>
</div>
{_cursor("560px","640px",0)}
<div style="position:absolute;bottom:18px;right:24px;font-family:'DM Sans';font-weight:600;font-size:20px;color:{GREY};">Swipe &rarr;</div>
"""
    _render(_shell(body, f), out)


# ── Slide 2: The Data ───────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [("75%","of recruiters screen your online presence before an interview.",CORAL),
             ("54%","have rejected a candidate over something they found.",AMBER),
             ("1","strong, consistent profile makes you look hireable at a glance.",MINT)]
    cards = ""
    for val,label,col in stats:
        cards += f"""<div style="flex:1;">{_window("stat", f'''
  <div style="font-family:Inter;font-weight:700;font-size:66px;color:{col if col!=MINT else '#2FA97F'};letter-spacing:-3px;line-height:1;">{val}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{INK};margin-top:14px;line-height:1.4;">{label}</div>''')}</div>"""
    body = f"""
<div style="flex-shrink:0;">{_kicker("The reality")}<div style="margin-top:12px;">{_head('They <span style="color:'+CORAL+';">will</span> look.', 54)}</div></div>
<div style="flex:1;display:flex;gap:22px;align-items:center;">{cards}</div>
<div style="flex-shrink:0;font-family:'DM Sans';font-weight:400;font-size:19px;color:{GREY};text-align:right;">Sources: CareerBuilder 2025, Jobvite Recruiter Report 2026</div>
"""
    _render(_shell(body, f), out)


# ── Slides 3-6: the four fixes ──────────────────────────────────────────────
def _fix_slide(out, n, kicker, headline, win_title, do_html, dont_text):
    f = _fonts()
    body = f"""
<div style="flex-shrink:0;">{_kicker(kicker)}<div style="margin-top:12px;">{_head(headline, 54)}</div></div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:20px;">
  {_window(win_title, do_html)}
  <div style="display:flex;align-items:flex-start;gap:14px;padding:0 6px;">
    <div style="width:28px;height:28px;border-radius:8px;background:{CORAL};color:#fff;display:flex;align-items:center;
                 justify-content:center;font-family:Inter;font-weight:700;font-size:18px;flex-shrink:0;">&times;</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{GREY};line-height:1.4;">{dont_text}</div>
  </div>
</div>
<div style="position:absolute;top:16px;right:24px;width:44px;height:44px;border-radius:12px;background:{DEEP_BLUE};
             color:#fff;display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:20px;">{n}</div>
"""
    _render(_shell(body, f), out)

def _do_line(text, color=DEEP_BLUE):
    return f"""<div style="display:flex;align-items:center;gap:14px;padding:9px 0;">
  <div style="width:26px;height:26px;border-radius:50%;background:{color};display:flex;align-items:center;justify-content:center;flex-shrink:0;">
    <svg width="13" height="11" viewBox="0 0 13 11"><polyline points="1,5.5 4.5,9 12,1" stroke="#fff" stroke-width="2.4" fill="none"/></svg>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:{INK};">{text}</div>
</div>"""

def _slide3(out): _fix_slide(out, 3, "Fix 01", 'Audit what\'s <span style="color:'+CORAL+';">public.</span>', "Search: your name",
    _do_line("Google your full name in an incognito tab")+_do_line("Check page 1 images and results")+_do_line("Set old accounts to private or delete"),
    "Don't assume it's fine. Assume a recruiter is looking right now.")

def _slide4(out): _fix_slide(out, 4, "Fix 02", 'Make your handle <span style="color:'+CORAL+';">consistent.</span>', "@you everywhere",
    _do_line("Same name and handle across LinkedIn, X, IG")+_do_line("A clear, recent, friendly headshot")+_do_line("A one-line bio that says what you do"),
    "Don't be @xXgamerkid2004 on the account a recruiter finds first.")

def _slide5(out): _fix_slide(out, 5, "Fix 03", 'Turn your feed into <span style="color:'+CORAL+';">proof.</span>', "Your last 9 posts",
    _do_line("Pin or post one thing you've built or learned")+_do_line("Engage in your field, not just memes")+_do_line("Delete the drunk-night album from 2021"),
    "Don't leave your profile blank either - empty reads as 'not serious'.")

def _slide6(out): _fix_slide(out, 6, "Fix 04", 'Lock the <span style="color:'+CORAL+';">back door.</span>', "Privacy settings",
    _do_line("Tighten who can see old personal posts")+_do_line("Turn off tagging without review")+_do_line("Keep one account clearly professional"),
    "Don't nuke everything - a real, human presence beats a ghost profile.")


# ── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    checklist = (_do_line("Googled yourself")+_do_line("Consistent handle + photo")+
                 _do_line("Feed shows your field")+_do_line("Privacy locked down"))
    body = f"""
<div style="flex-shrink:0;">{_kicker("15-minute job")}<div style="margin-top:12px;">{_head('Be searchable<br>for the <span style="color:'+CORAL+';">right</span> reasons.', 62)}</div></div>
<div style="flex:1;display:flex;align-items:center;">
  <div style="width:660px;">{_window("Cleanup checklist", checklist)}</div>
</div>
<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;">
  <div style="background:{DEEP_BLUE};color:#fff;padding:16px 28px;border-radius:12px;font-family:Inter;font-weight:700;font-size:23px;">
    Find roles at internwise.co.uk &rarr;
  </div>
  <img src="data:image/png;base64,{LOGO_C}" style="height:44px;">
</div>
{_cursor("470px","690px",0)}
"""
    _render(_shell(body, f), out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Online Presence (Week 10, Day 2)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("retro_desktop_os_windows", "week10/d2-onlinepresence", "week10")
    print("Done - online presence complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week10/d2-onlinepresence")
