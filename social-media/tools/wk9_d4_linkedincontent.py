"""
Internwise - LinkedIn Content That Gets You Noticed (Week 9, Day 4)
Design language: PHONE MOCKUP / SOCIAL FEED. Realistic LinkedIn-style post UI inside
a 3D phone frame, reaction emoji clusters, notification badges, engagement counters.
7 slides. Accent: LinkedIn blue + amber notification + cream bg.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; DEEP_BLUE = "#264D7E"; OFF_WHITE = "#FAF5EC"

BG        = "#EAF1F7"   # soft blue-grey backdrop
LI_BLUE   = "#2D6BD4"; LI_BLUE_D = "#1E4FA3"
INK       = "#1C2530"
GREY      = "#5B6875"
CORAL     = "#FF6B6B"
AMBER     = "#FFB120"
GREEN_GO  = "#3FA877"
PHONE     = "#11161C"   # phone bezel

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
      background:radial-gradient(ellipse at 70% 15%,#F4F8FC 0%,{BG} 100%);}}
.c{{width:1080px;height:1080px;position:relative;padding:52px 56px;display:flex;flex-direction:column;}}
"""

# reaction emoji badges (drawn, not font emoji, for consistency)
def _react_like(s=44):
    return f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:{LI_BLUE};display:flex;align-items:center;justify-content:center;box-shadow:0 3px 6px rgba(0,0,0,0.25);border:2px solid #fff;"><svg width="{int(s*0.5)}" height="{int(s*0.5)}" viewBox="0 0 24 24"><path d="M6 10 H4 v9 h2 Z M8 19 h9 l3-8 v-1 h-6 l1-4 q0-2-2-2 l-4 6 Z" fill="#fff"/></svg></div>'
def _react_heart(s=44):
    return f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:{CORAL};display:flex;align-items:center;justify-content:center;box-shadow:0 3px 6px rgba(0,0,0,0.25);border:2px solid #fff;margin-left:-12px;"><svg width="{int(s*0.5)}" height="{int(s*0.5)}" viewBox="0 0 24 24"><path d="M12 21 C3 14 2 8 6 5.5 C9 3.6 12 7 12 9 C12 7 15 3.6 18 5.5 C22 8 21 14 12 21 Z" fill="#fff"/></svg></div>'
def _react_clap(s=44):
    return f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;box-shadow:0 3px 6px rgba(0,0,0,0.25);border:2px solid #fff;margin-left:-12px;font-size:{int(s*0.5)}px;line-height:1;">&#128079;</div>'

def _avatar(bg, initials, s=58):
    return (f'<div style="width:{s}px;height:{s}px;border-radius:50%;background:{bg};flex-shrink:0;'
            f'display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;'
            f'font-size:{int(s*0.4)}px;color:#fff;">{initials}</div>')

def _phone(inner, notif=None):
    """3D phone frame containing a feed card."""
    badge = ""
    if notif:
        badge = f"""<div style="position:absolute;top:-18px;right:-18px;background:{CORAL};color:#fff;
             min-width:52px;height:52px;border-radius:26px;padding:0 14px;display:flex;align-items:center;
             justify-content:center;font-family:Inter;font-weight:700;font-size:24px;z-index:40;
             box-shadow:0 8px 18px rgba(0,0,0,0.35);border:3px solid #fff;">{notif}</div>"""
    return f"""<div style="position:relative;width:430px;flex-shrink:0;">
  <div style="background:{PHONE};border-radius:46px;padding:14px;box-shadow:0 26px 50px rgba(30,50,80,0.4),
               inset 0 2px 3px rgba(255,255,255,0.15);">
    <div style="background:#fff;border-radius:34px;overflow:hidden;">
      <div style="height:34px;background:#fff;display:flex;align-items:center;justify-content:center;">
        <div style="width:120px;height:20px;background:{PHONE};border-radius:12px;"></div>
      </div>
      {inner}
    </div>
  </div>
  {badge}
</div>"""

def _feed_post(name, meta, avatar_bg, initials, body_html, likes, comments, verified=True):
    check = f'<svg width="20" height="20" viewBox="0 0 24 24" style="margin-left:6px;"><circle cx="12" cy="12" r="10" fill="{LI_BLUE}"/><path d="M7 12 l3 3 l7-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>' if verified else ""
    return f"""<div style="padding:22px 22px 18px 22px;">
  <div style="display:flex;align-items:center;gap:12px;">
    {_avatar(avatar_bg, initials, 56)}
    <div style="flex:1;">
      <div style="display:flex;align-items:center;"><span style="font-family:Inter;font-weight:700;font-size:23px;color:{INK};">{name}</span>{check}</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:17px;color:{GREY};">{meta}</div>
    </div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{LI_BLUE};">in</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:{INK};line-height:1.5;margin-top:16px;">{body_html}</div>
  <div style="display:flex;align-items:center;gap:8px;margin-top:18px;padding-top:14px;border-top:1px solid #E4E9EF;">
    <div style="display:flex;align-items:center;">{_react_like(34)}{_react_heart(34)}{_react_clap(34)}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:18px;color:{GREY};margin-left:8px;">{likes} &middot; {comments} comments</div>
  </div>
</div>"""

def _kicker(text, color=LI_BLUE):
    return (f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:19px;color:{color};'
            f'text-transform:uppercase;letter-spacing:3px;">{text}</div>')


# ── Slide 1: Hook — phone with a viral post ─────────────────────────────────
def _slide1(out):
    f = _fonts()
    post = _feed_post("Emily Hughes", "Final-year student &middot; 2h",
        "linear-gradient(135deg,#7B5CE6,#4A9BE8)", "EH",
        'I got rejected from 40 grad schemes.<br><br>So I started posting what I was learning instead. 3 months later, 2 companies messaged <span style="color:'+LI_BLUE+';font-weight:700;">me.</span><br><br>Here\'s what I posted...',
        "1,204", "186")
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:54px;">
  <div style="background:{LI_BLUE};color:#fff;padding:11px 22px;border-radius:50px;
               font-family:Inter;font-weight:700;font-size:19px;letter-spacing:2px;text-transform:uppercase;
               box-shadow:0 6px 14px rgba(45,107,212,0.35);">Post to get found</div>
</div>
<div style="flex:1;display:flex;align-items:center;gap:40px;">
  <div style="flex:1;">
    {_kicker("LinkedIn content", LI_BLUE)}
    <div style="font-family:Inter;font-weight:700;font-size:80px;line-height:0.92;color:{INK};
                 letter-spacing:-3px;margin-top:16px;word-break:keep-all;hyphens:none;">
      Stop applying.<br>Start <span style="color:{LI_BLUE};font-style:italic;">posting.</span>
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:29px;color:{GREY};
                 margin-top:22px;line-height:1.4;max-width:520px;">
      The best grads don't chase recruiters. They post so recruiters come to them.
    </div>
  </div>
  {_phone(post, notif="9+")}
</div>
<div style="flex-shrink:0;display:flex;justify-content:flex-end;">
  <div style="font-family:'DM Sans';font-weight:500;font-size:20px;color:{GREY};">SWIPE &rarr;</div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: The Data ───────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("0.9%", "of LinkedIn users post weekly. Posting at all puts you ahead of 99%.", LI_BLUE, _react_like),
        ("4x", "more profile views in the week you publish a post vs a week you don't.", GREEN_GO, _react_clap),
        ("60%", "of recruiters check your activity, not just your CV, before reaching out.", CORAL, _react_heart),
    ]
    cards = ""
    for val, label, col, react in stats:
        cards += f"""<div style="flex:1;background:#fff;border-radius:22px;padding:34px 28px;
             box-shadow:0 14px 30px rgba(40,70,120,0.14);display:flex;flex-direction:column;">
  <div style="margin-bottom:22px;">{react(64)}</div>
  <div style="font-family:Inter;font-weight:700;font-size:66px;color:{col};letter-spacing:-2px;line-height:1;">{val}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{GREY};margin-top:16px;line-height:1.4;">{label}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  {_kicker("The numbers", LI_BLUE)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Almost nobody <span style="color:{LI_BLUE};font-style:italic;">posts.</span>
  </div>
</div>
<div style="flex:1;display:flex;gap:22px;margin:36px 0 18px 0;">{cards}</div>
<div style="flex-shrink:0;font-family:'DM Sans';font-weight:400;font-size:20px;color:{GREY};text-align:right;">
  Sources: LinkedIn Creator Report 2026, Jobvite Recruiter Survey 2025
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: What to post ───────────────────────────────────────────────────
def _slide3(out):
    f = _fonts()
    ideas = [
        ("The learning log", "\"This week I learned X building Y.\" Shows momentum, invites help.", LI_BLUE),
        ("The teardown", "Analyse a brand/product you admire. Public thinking = free proof of skill.", GREEN_GO),
        ("The honest rejection", "What a 'no' taught you. Vulnerability outperforms highlight reels.", CORAL),
        ("The build-in-public", "Share a project as you make it. People root for a story in progress.", AMBER),
    ]
    rows = ""
    for i, (title, desc, col) in enumerate(ideas):
        rows += f"""<div style="background:#fff;border-radius:18px;padding:26px 28px;
             box-shadow:0 12px 26px rgba(40,70,120,0.12);border-top:6px solid {col};">
  <div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};letter-spacing:-0.5px;">{i+1}. {title}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{GREY};margin-top:8px;line-height:1.4;">{desc}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  {_kicker("What to post", LI_BLUE)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Four posts that <span style="color:{LI_BLUE};font-style:italic;">work.</span>
  </div>
</div>
<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:28px;align-content:center;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: Anatomy of a post (phone) ──────────────────────────────────────
def _slide4(out):
    f = _fonts()
    post = _feed_post("You", "Aspiring product manager &middot; now",
        "linear-gradient(135deg,#2D6BD4,#3FA877)", "YOU",
        '<span style="background:#FFF3D6;">I spent 6 hours on a cover letter and got rejected in 4 minutes.</span><br><br>So I rebuilt it as a 1-page teardown of their product instead.<br><br>They replied the same day. Here\'s the exact page &darr;',
        "842", "97")
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  {_kicker("Anatomy", LI_BLUE)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    The <span style="color:{LI_BLUE};font-style:italic;">hook</span> does the work.
  </div>
</div>
<div style="flex:1;display:flex;align-items:center;gap:40px;margin-top:10px;">
  {_phone(post, notif="1")}
  <div style="flex:1;display:flex;flex-direction:column;gap:18px;">
    <div style="background:#fff;border-radius:16px;padding:24px 26px;box-shadow:0 10px 22px rgba(40,70,120,0.12);border-left:6px solid {CORAL};">
      <div style="font-family:Inter;font-weight:700;font-size:22px;color:{CORAL};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Line 1: the hook</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{INK};line-height:1.4;">A specific, surprising confession. It stops the scroll before the '...see more'.</div>
    </div>
    <div style="background:#fff;border-radius:16px;padding:24px 26px;box-shadow:0 10px 22px rgba(40,70,120,0.12);border-left:6px solid {GREEN_GO};">
      <div style="font-family:Inter;font-weight:700;font-size:22px;color:{GREEN_GO};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Middle: the turn</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{INK};line-height:1.4;">One concrete action you took. Short lines. One idea per line.</div>
    </div>
    <div style="background:#fff;border-radius:16px;padding:24px 26px;box-shadow:0 10px 22px rgba(40,70,120,0.12);border-left:6px solid {LI_BLUE};">
      <div style="font-family:Inter;font-weight:700;font-size:22px;color:{LI_BLUE};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">End: the payoff + CTA</div>
      <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:{INK};line-height:1.4;">The result, then invite a reply. Comments are the algorithm's fuel.</div>
    </div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: Cadence / how often ────────────────────────────────────────────
def _slide5(out):
    f = _fonts()
    rules = [
        ("Post once a week", "Consistency beats virality. One good post every Tuesday builds a habit and an audience.", LI_BLUE),
        ("Comment 5x a day", "Thoughtful comments on bigger accounts get you seen faster than your own posts at first.", GREEN_GO),
        ("Reply to every comment", "It doubles your reach and it's just good manners. The algorithm rewards conversation.", AMBER),
        ("Give it 8 weeks", "Nobody's first 5 posts do numbers. The account that keeps going is the one that wins.", CORAL),
    ]
    rows = ""
    for title, desc, col in rules:
        rows += f"""<div style="background:#fff;border-radius:18px;padding:26px 28px;
             box-shadow:0 12px 26px rgba(40,70,120,0.12);display:flex;gap:20px;align-items:flex-start;">
  <div style="width:16px;height:16px;border-radius:50%;background:{col};margin-top:8px;flex-shrink:0;"></div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};letter-spacing:-0.5px;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{GREY};margin-top:5px;line-height:1.4;">{desc}</div>
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  {_kicker("The cadence", LI_BLUE)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Show up on <span style="color:{LI_BLUE};font-style:italic;">repeat.</span>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;margin-top:28px;justify-content:center;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: Kill list ──────────────────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    kills = [
        ("The humble-brag", "'Blessed and grateful to announce...' Everyone scrolls past. Say the real thing."),
        ("The engagement bait", "'Comment YES if you agree!' The algorithm and humans both hate it now."),
        ("The wall of text", "No line breaks. On mobile it's a grey brick. One idea per line, always."),
        ("The corporate voice", "'Leveraging synergies to drive impact.' Write like you'd talk to a friend."),
    ]
    rows = ""
    for title, desc in kills:
        rows += f"""<div style="background:#fff;border-radius:18px;padding:26px 28px;
             box-shadow:0 12px 26px rgba(40,70,120,0.12);display:flex;gap:18px;align-items:flex-start;">
  <div style="width:44px;height:44px;border-radius:50%;background:{CORAL};flex-shrink:0;display:flex;
               align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:26px;color:#fff;">&times;</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:27px;color:{INK};letter-spacing:-0.5px;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{GREY};margin-top:5px;line-height:1.38;">{desc}</div>
  </div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="flex-shrink:0;">
  {_kicker("Scroll-past signals", CORAL)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{INK};
               letter-spacing:-2px;margin-top:10px;word-break:keep-all;hyphens:none;">
    Four ways to <span style="color:{CORAL};font-style:italic;">get ignored.</span>
  </div>
</div>
<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:28px;align-content:center;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    steps = ["Pick one thing you did this week", "Write the confession as line 1", "Add 3 short lines + a question", "Post it Tuesday. Reply to everyone."]
    rows = ""
    for i, s in enumerate(steps):
        rows += f"""<div style="display:flex;gap:16px;align-items:center;padding:9px 0;">
  <div style="width:42px;height:42px;border-radius:12px;background:{LI_BLUE};flex-shrink:0;display:flex;
               align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:#fff;">{i+1}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:{INK};">{s}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body><div class="c">
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;">
  <img src="data:image/png;base64,{LOGO_C}" style="height:54px;">
  <div style="display:flex;align-items:center;">{_react_like(52)}{_react_heart(52)}{_react_clap(52)}</div>
</div>
<div style="flex:1;display:flex;align-items:center;gap:36px;">
  <div style="flex:1;">
    <div style="font-family:Inter;font-weight:700;font-size:74px;line-height:0.95;color:{INK};
                 letter-spacing:-3px;word-break:keep-all;hyphens:none;">
      Be the grad<br>they <span style="color:{LI_BLUE};font-style:italic;">find.</span>
    </div>
    <div style="background:#fff;border-radius:20px;padding:28px 32px;margin-top:28px;
                 box-shadow:0 14px 30px rgba(40,70,120,0.14);">
      <div style="font-family:Inter;font-weight:700;font-size:22px;color:{LI_BLUE};text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;">Your first post, in 4 steps</div>
      {rows}
    </div>
    <div style="margin-top:26px;background:{LI_BLUE};color:#fff;display:inline-flex;align-items:center;gap:12px;
                 padding:18px 32px;border-radius:50px;font-family:Inter;font-weight:700;font-size:24px;
                 box-shadow:0 8px 18px rgba(45,107,212,0.35);">
      Find roles at internwise.co.uk &rarr;
    </div>
  </div>
  <div style="width:190px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:0;">
    <div style="position:relative;">
      {_avatar('linear-gradient(135deg,#7B5CE6,#4A9BE8)', 'YOU', 150)}
      <div style="position:absolute;bottom:-6px;right:-6px;background:{GREEN_GO};color:#fff;
                   padding:8px 16px;border-radius:20px;font-family:Inter;font-weight:700;font-size:20px;
                   border:3px solid {BG};box-shadow:0 6px 12px rgba(0,0,0,0.2);">Open</div>
    </div>
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:{INK};margin-top:22px;text-align:center;">+312</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:19px;color:{GREY};text-align:center;">views this week</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating LinkedIn Content (Week 9, Day 4)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("phone_mockup_social_feed", "week9/d4-linkedincontent", "week9")
    print("Done - linkedin content complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week9/d4-linkedincontent")
