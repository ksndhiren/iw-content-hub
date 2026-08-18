"""
Internwise - The Follow-Up Email Nobody Sends (Week 7, Day 4)
Trendy: iMessage chat-bubble aesthetic, texting-style headline, warm coral+mint combo.
7 slides. Accent: CORAL + MINT.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"; HOT_PINK = "#FF3D8A"; LIME = "#D4FF3D"
IMSG_BLUE = "#0A84FF"; IMSG_GRAY = "#E5E5EA"

LOGO_W = LOGO_C = None
def _load_logos():
    global LOGO_W, LOGO_C
    if LOGO_W is None:
        LOGO_W = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
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

GRAIN_DARK = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(0,0,0,0.06) 1px,transparent 1px);background-size:3px 3px;}"

def _num_badge(n, bg=CORAL, fg="white"):
    return f'<div style="position:absolute;top:44px;left:44px;width:54px;height:54px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};border:3px solid {DARK_NAVY};box-shadow:3px 3px 0 {DARK_NAVY};z-index:25;">{n}</div>'

def _kicker(text, color=CORAL):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">{text}</div>'

def _bubble(text, side, color, txt_color, tail=True):
    """iMessage-style bubble. side='left' or 'right'."""
    align = "flex-end" if side == "right" else "flex-start"
    radius = "22px 22px 6px 22px" if side == "right" else "22px 22px 22px 6px"
    return (f'<div style="display:flex;justify-content:{align};margin:6px 0;">'
            f'<div style="max-width:75%;background:{color};color:{txt_color};padding:14px 22px;'
            f'border-radius:{radius};font-family:DM Sans,sans-serif;font-weight:500;font-size:24px;'
            f'line-height:1.35;">{text}</div></div>')

# ─── Slide 1: Hook — Big chat bubble mockup ─────────────────────────────────
def _slide1(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:44px;left:44px;height:62px;z-index:25;">
<!-- sticker -->
<div style="position:absolute;top:52px;right:60px;background:{CORAL};color:white;
             padding:14px 22px;border:3px solid {DARK_NAVY};border-radius:14px;
             font-family:Inter;font-weight:700;font-size:22px;letter-spacing:2px;text-transform:uppercase;
             transform:rotate(4deg);z-index:35;box-shadow:5px 5px 0 {DARK_NAVY};">Copy this</div>

<div style="padding-top:130px;position:relative;z-index:5;">
  {_kicker("THE FOLLOW-UP", CORAL)}
  <div style="font-family:Inter;font-weight:700;font-size:78px;line-height:0.95;color:{DARK_NAVY};
               letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    The email <em style="color:{CORAL};font-style:italic;">nobody</em><br>sends.
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(22,45,74,0.7);
               margin-top:20px;max-width:640px;line-height:1.4;">
    3 lines. 30 seconds to write. Puts you back at the top of their inbox and their memory.
  </div>
</div>

<!-- Phone-style bubble stack -->
<div style="flex:1;margin-top:34px;background:white;border:3px solid {DARK_NAVY};border-radius:32px;
             padding:26px 22px;box-shadow:8px 8px 0 {DARK_NAVY};position:relative;z-index:5;
             display:flex;flex-direction:column;justify-content:flex-end;">
  <div style="text-align:center;font-family:'DM Sans';font-weight:500;font-size:16px;
               color:rgba(22,45,74,0.4);margin-bottom:12px;">Today 9:42</div>
  {_bubble("Just applied for the Product Analyst role - loved the recent launch of your climate dashboard.", "right", CORAL, "white")}
  {_bubble("Would love to be considered. My 60-second pitch attached if useful.", "right", CORAL, "white")}
  {_bubble("Thanks for making time to read this - excited about the work you're doing.", "right", CORAL, "white")}
  {_bubble("Hi - thanks for reaching out directly. Let's set up a chat this week.", "left", IMSG_GRAY, DARK_NAVY)}
  <div style="font-family:'DM Sans';font-weight:500;font-size:14px;color:rgba(22,45,74,0.4);text-align:right;margin-top:2px;">Read 9:57</div>
</div>

<div style="position:absolute;bottom:44px;right:60px;font-family:'DM Sans';
             font-weight:500;font-size:20px;color:rgba(22,45,74,0.5);z-index:20;">SWIPE →</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 2: The Data ───────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("THE DATA", CORAL)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{DARK_NAVY};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Only <em style="color:{CORAL};font-style:italic;">4%</em> of applicants follow up.
  </div>
</div>
<div style="flex:1;display:flex;gap:22px;margin-top:38px;position:relative;z-index:5;">
  <div style="flex:1;background:white;border:3px solid {DARK_NAVY};border-radius:20px;
               padding:34px 28px;box-shadow:6px 6px 0 {CORAL};">
    <div style="font-family:Inter;font-weight:700;font-size:92px;color:{CORAL};letter-spacing:-4px;line-height:1;">4%</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:{DARK_NAVY};margin-top:20px;line-height:1.35;">
      of applicants ever send a follow-up email after applying.
    </div>
  </div>
  <div style="flex:1;background:white;border:3px solid {DARK_NAVY};border-radius:20px;
               padding:34px 28px;box-shadow:6px 6px 0 {MINT};">
    <div style="font-family:Inter;font-weight:700;font-size:92px;color:{DEEP_BLUE};letter-spacing:-4px;line-height:1;">3x</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:{DARK_NAVY};margin-top:20px;line-height:1.35;">
      more likely to get an interview if you send a well-timed follow-up.
    </div>
  </div>
  <div style="flex:1;background:{DARK_NAVY};color:white;border:3px solid {DARK_NAVY};border-radius:20px;
               padding:34px 28px;box-shadow:6px 6px 0 {AMBER};">
    <div style="font-family:Inter;font-weight:700;font-size:92px;color:{AMBER};letter-spacing:-4px;line-height:1;">48h</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:white;margin-top:20px;line-height:1.35;">
      is the sweet spot. Send too fast, you look pushy. Too late, they've moved on.
    </div>
  </div>
</div>
<div style="flex-shrink:0;margin-top:20px;font-family:'DM Sans';font-weight:400;font-size:20px;
             color:rgba(22,45,74,0.5);position:relative;z-index:5;text-align:right;">Sources: Jobvite Recruiter Report 2026, LinkedIn Talent Insights</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 3: The 48h After Applying Template ────────────────────────────────
def _slide3(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(3)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("48H AFTER APPLYING", CORAL)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{DARK_NAVY};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    The <em style="color:{CORAL};font-style:italic;">post-apply</em> nudge.
  </div>
</div>
<div style="flex:1;margin-top:28px;background:white;border:3px solid {DARK_NAVY};border-radius:20px;
             padding:30px 34px;box-shadow:6px 6px 0 {DARK_NAVY};position:relative;z-index:5;">
  <div style="border-bottom:2px dashed rgba(22,45,74,0.15);padding-bottom:14px;margin-bottom:18px;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:rgba(22,45,74,0.5);letter-spacing:2px;text-transform:uppercase;">Subject</div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{DARK_NAVY};margin-top:4px;">Application for [Role] - one more thing worth knowing</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{DARK_NAVY};line-height:1.55;">
    Hi [Name],<br><br>
    I applied for the [Role] role yesterday and wanted to briefly flag one thing my CV doesn't capture:
    <span style="background:{LIME};padding:2px 6px;">[one specific, relevant thing you did]</span>.<br><br>
    Would love to chat about how that could translate to [Company]. Happy to send a short Loom if it's easier than reading.<br><br>
    Thanks for reading,<br>[Your name]
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 4: Post-Interview Thank You ───────────────────────────────────────
def _slide4(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("2H AFTER INTERVIEW", CORAL)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{DARK_NAVY};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    The <em style="color:{CORAL};font-style:italic;">post-interview</em> thank you.
  </div>
</div>
<div style="flex:1;margin-top:28px;background:white;border:3px solid {DARK_NAVY};border-radius:20px;
             padding:30px 34px;box-shadow:6px 6px 0 {DARK_NAVY};position:relative;z-index:5;">
  <div style="border-bottom:2px dashed rgba(22,45,74,0.15);padding-bottom:14px;margin-bottom:18px;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:rgba(22,45,74,0.5);letter-spacing:2px;text-transform:uppercase;">Subject</div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{DARK_NAVY};margin-top:4px;">Thanks for today - and one thought on [topic they raised]</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{DARK_NAVY};line-height:1.55;">
    Hi [Name],<br><br>
    Really enjoyed our conversation today, particularly the part about
    <span style="background:{MINT};padding:2px 6px;">[specific thing they said]</span>.<br><br>
    One thought after reflecting: [1-2 lines showing you thought about it more, or an answer you'd give better now].<br><br>
    Excited about the possibility of joining the team. Any next steps I should know about?<br><br>
    Best,<br>[Your name]
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 5: The Chase-Up ───────────────────────────────────────────────────
def _slide5(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(5)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("7 DAYS LATER, NO REPLY", CORAL)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{DARK_NAVY};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    The <em style="color:{CORAL};font-style:italic;">gentle</em> chase.
  </div>
</div>
<div style="flex:1;margin-top:28px;background:white;border:3px solid {DARK_NAVY};border-radius:20px;
             padding:30px 34px;box-shadow:6px 6px 0 {DARK_NAVY};position:relative;z-index:5;">
  <div style="border-bottom:2px dashed rgba(22,45,74,0.15);padding-bottom:14px;margin-bottom:18px;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:rgba(22,45,74,0.5);letter-spacing:2px;text-transform:uppercase;">Subject</div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:{DARK_NAVY};margin-top:4px;">Following up - [Role] at [Company]</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{DARK_NAVY};line-height:1.55;">
    Hi [Name],<br><br>
    Just circling back on my application/interview from
    <span style="background:{AMBER};padding:2px 6px;">[date]</span>.
    Wanted to make sure my email didn't get lost.<br><br>
    I'm still very interested and would love to know if there's a decision timeline I should plan around.<br><br>
    Happy to answer anything else you need from me.<br><br>
    Thanks,<br>[Your name]
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 6: What NOT to send ───────────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    donts = [
        ("Just checking in!!!", "Vague. Zero new information. Sounds needy."),
        ("Any update on my application?", "Puts the emotional burden on them. Reads as chasing."),
        ("Hi, I applied 3 days ago and haven't heard back?", "Too soon and too passive-aggressive."),
        ("Bumping this to the top of your inbox!", "You're not their boss. Sounds entitled."),
    ]
    rows = ""
    for text, why in donts:
        rows += f"""<div style="background:white;border:3px solid {CORAL};border-radius:16px;padding:26px 30px;box-shadow:5px 5px 0 {CORAL};">
  <div style="font-family:Inter;font-weight:700;font-style:italic;font-size:30px;color:{CORAL};margin-bottom:12px;line-height:1.2;">"{text}"</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:{DARK_NAVY};line-height:1.4;">{why}</div>
</div>"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6)}
<div style="padding-top:74px;position:relative;z-index:5;">
  {_kicker("WHAT NOT TO SEND", CORAL)}
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:{DARK_NAVY};
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Delete these <em style="color:{CORAL};font-style:italic;">from your drafts.</em>
  </div>
</div>
<div style="flex:1;margin-top:28px;display:grid;grid-template-columns:1fr 1fr;gap:18px;position:relative;z-index:5;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ─── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{CORAL};}}
.c{{width:1080px;height:1080px;position:relative;padding:44px 50px;display:flex;flex-direction:column;}}
{GRAIN_DARK}
</style></head><body><div class="c">
<div class="grain"></div>
<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:44px;left:44px;height:62px;z-index:25;">
<div style="position:absolute;top:52px;right:60px;background:{DARK_NAVY};color:{OFF_WHITE};
             padding:14px 22px;border:3px solid {DARK_NAVY};border-radius:14px;
             font-family:Inter;font-weight:700;font-size:22px;letter-spacing:2px;text-transform:uppercase;
             transform:rotate(-4deg);z-index:35;box-shadow:5px 5px 0 rgba(0,0,0,0.15);">Send it today</div>

<div style="padding-top:140px;position:relative;z-index:10;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:20px;color:{DARK_NAVY};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:16px;opacity:0.7;">YOUR TURN</div>
  <div style="font-family:Inter;font-weight:700;font-size:96px;line-height:0.95;color:{DARK_NAVY};
               letter-spacing:-4px;word-break:keep-all;hyphens:none;">
    Pick one open<br>application.<br><em style="color:{OFF_WHITE};font-style:italic;">Follow up now.</em>
  </div>
</div>

<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;position:relative;z-index:10;">
  <div style="background:{OFF_WHITE};border:3px solid {DARK_NAVY};border-radius:18px;padding:26px 30px;
               box-shadow:6px 6px 0 {DARK_NAVY};max-width:640px;">
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:{DARK_NAVY};margin-bottom:12px;">The 30-second checklist:</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:{DARK_NAVY};line-height:1.5;">
      Right timing (48h post-apply, 2h post-interview)<br>
      One specific detail from the role or their work<br>
      One clear ask or offer<br>
      Signature and out
    </div>
  </div>
  <div style="margin-top:26px;display:inline-flex;align-items:center;gap:12px;background:{DARK_NAVY};
               color:{OFF_WHITE};padding:18px 30px;border-radius:60px;font-family:Inter;
               font-weight:700;font-size:24px;border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 rgba(0,0,0,0.2);
               width:fit-content;">
    Find roles at internwise.co.uk &#8594;
  </div>
</div>
</div></body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Follow-Up Email (Week 7, Day 4)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("imessage_chat_bubble_coral", "week7/d4-followup", "week7")
    print("Done - follow-up email complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week7/d4-followup")
