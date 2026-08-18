"""
Internwise - The Referral Advantage (Week 6, Day 4)
Hook: CORAL bg, WARM INTRO vs COLD APPLY two-column comparison — pure typography, no person.
Different from D1 week5 (which was also full-color type-only but: that was one central message,
this is a direct side-by-side contrast layout).
Accent: CORAL. 7 slides.
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

GRAIN_DARK = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(0,0,0,0.06) 1px,transparent 1px);background-size:3px 3px;}"
GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"

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
def _num_badge(n, bg=CORAL, fg=DARK_NAVY):
    return f'<div style="position:absolute;top:44px;left:44px;width:52px;height:52px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};z-index:25;">{n}</div>'
def _kicker(text, color=DARK_NAVY):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;opacity:0.6;">{text}</div>'


# ── Slide 1: Hook — CORAL bg, two-column WARM vs COLD ─────────────────────────
def _slide1(out):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{CORAL};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;
    padding:50px 60px;}}
{GRAIN_DARK}
.cols{{flex:1;display:flex;gap:20px;margin-top:24px;}}
.col{{flex:1;border-radius:20px;padding:32px 28px;display:flex;flex-direction:column;gap:16px;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_color()}
<div style="margin-top:84px;">
  {_kicker("THE REFERRAL ADVANTAGE")}
  <div style="font-family:Inter;font-weight:700;font-size:74px;line-height:0.9;
               color:{DARK_NAVY};letter-spacing:-5px;word-break:keep-all;hyphens:none;">
    Warm intro<br>beats 100<br>cold applies.
  </div>
</div>
<div class="cols">
  <div class="col" style="background:rgba(22,45,74,0.12);">
    <div style="font-family:Inter;font-weight:700;font-size:18px;color:{DARK_NAVY};
                 text-transform:uppercase;letter-spacing:2px;opacity:0.6;">Cold apply</div>
    <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1;color:{DARK_NAVY};
                 letter-spacing:-2px;">2%</div>
    <div style="font-family:'DM Sans';font-weight:600;font-size:28px;color:{DARK_NAVY};opacity:0.7;
                 line-height:1.35;">Average callback rate from an ATS-screened cold application.</div>
  </div>
  <div style="width:4px;flex-shrink:0;background:{DARK_NAVY};opacity:0.15;border-radius:2px;margin:8px 0;"></div>
  <div class="col" style="background:rgba(22,45,74,0.12);">
    <div style="font-family:Inter;font-weight:700;font-size:18px;color:{DARK_NAVY};
                 text-transform:uppercase;letter-spacing:2px;opacity:0.6;">Warm referral</div>
    <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1;color:{DARK_NAVY};
                 letter-spacing:-2px;">40%</div>
    <div style="font-family:'DM Sans';font-weight:600;font-size:28px;color:{DARK_NAVY};opacity:0.7;
                 line-height:1.35;">Callback rate when referred by someone inside the company.</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: Why referrals work ───────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    facts = [
        ("Employee referrals", f'<em style="color:{CORAL};font-style:italic;">4x</em> more likely to get hired than a direct applicant.'),
        ("Time to hire", "Referred candidates are hired 55% faster than those from job boards."),
        ("Retention", "Referred hires stay 70% longer on average. Employers know this — they pay referral bonuses."),
    ]
    rows = "".join([f"""<div style="background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);
                          border-radius:14px;padding:22px 26px;display:flex;gap:16px;align-items:flex-start;">
  <div style="width:8px;height:8px;border-radius:50%;background:{CORAL};flex-shrink:0;margin-top:10px;"></div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;word-break:keep-all;hyphens:none;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.6);
                 margin-top:6px;line-height:1.4;">{desc}</div>
  </div>
</div>""" for title, desc in facts])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:28px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2, bg=CORAL, fg=DARK_NAVY)}
<div style="padding-top:60px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">THE DATA</div>
  <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
               color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Why the numbers are <em style="color:{CORAL};font-style:italic;">this big.</em>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;">{rows}</div>
<div style="background:rgba(255,107,107,0.15);border:2px solid {CORAL};border-radius:12px;
             padding:16px 24px;font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};">
A referral doesn't bypass the process. It bypasses the pile. Sources: LinkedIn Talent Trends 2025, SHRM</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: Who to ask ───────────────────────────────────────────────────────
def _slide3(out):
    f = _fonts()
    tiers = [
        (CORAL, DARK_NAVY, "Tier 1 - Direct connection", "Alumni from your university, current employees you've met, previous managers or internship supervisors."),
        (AMBER, DARK_NAVY, "Tier 2 - Warm second degree", "Friend of a friend, LinkedIn connections who've engaged with your content, people from events you've attended."),
        (DEEP_BLUE, "white", "Tier 3 - Cold outreach", "Direct message to an employee at the target company. Lower hit rate, but one yes from here is worth 50 cold applications."),
    ]
    cards = "".join([f"""<div style="flex:1;background:{bg};border-radius:16px;padding:26px 24px;
                          border:3px solid {DARK_NAVY};box-shadow:4px 4px 0 {DARK_NAVY};">
  <div style="font-family:Inter;font-weight:700;font-size:18px;color:{fg};
               word-break:keep-all;hyphens:none;margin-bottom:12px;">{title}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;
               color:{'rgba(22,45,74,0.65)' if fg==DARK_NAVY else 'rgba(255,255,255,0.7)'};
               line-height:1.4;">{desc}</div>
</div>""" for bg, fg, title, desc in tiers])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:24px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(3, bg=CORAL, fg=DARK_NAVY)}
<div style="padding-top:60px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">WHO TO ASK</div>
  <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
               color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Start warm.<br>Work <em style="color:{CORAL};font-style:italic;">outward.</em>
  </div>
</div>
<div style="flex:1;display:flex;gap:16px;">{cards}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: How to ask without being awkward ─────────────────────────────────
def _slide4(out):
    f = _fonts()
    scripts = [
        ("Alumni cold message", f'"Hi [Name] - I noticed we both studied [X] at [Uni]. I\'m applying to [role] at [Company] and would love 10 minutes to ask you one question about the team. No obligation at all - completely understand if you\'re busy."'),
        ("Warm contact ask", f'"Hey [Name] - hope you\'re well. I\'m applying to [Company] for their grad intake and saw you work there. Would you be open to a quick chat, or even just a word with your team about my application? Happy to keep it very brief."'),
        ("The informational first", f'"I\'m researching [Company] before applying - would you be up for a 15-minute call about what the culture\'s actually like? Not asking for a referral, just trying to understand the role better."'),
    ]
    cards = "".join([f"""<div style="background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);
                          border-radius:16px;padding:22px 24px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:12px;color:{CORAL};
               text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;">{label}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.75);
               line-height:1.5;font-style:italic;">{script}</div>
</div>""" for label, script in scripts])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:22px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4, bg=CORAL, fg=DARK_NAVY)}
<div style="padding-top:60px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">EXACT SCRIPTS</div>
  <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
               color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    How to ask without <em style="color:{CORAL};font-style:italic;">cringing.</em>
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:14px;">{cards}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: Alumni networks ──────────────────────────────────────────────────
def _slide5(out):
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
{_num_badge(5, bg=CORAL, fg=DARK_NAVY)}
<div style="padding-top:60px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">ALUMNI ADVANTAGE</div>
  <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
               color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    The warmest cold <em style="color:{CORAL};font-style:italic;">call</em> you can make.
  </div>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;">
  <div style="background:rgba(255,107,107,0.1);border:2px solid {CORAL};border-radius:14px;
               padding:24px 28px;">
    <div style="font-family:Inter;font-weight:700;font-size:42px;line-height:1;color:{CORAL};
                 letter-spacing:-2px;margin-bottom:10px;">3x</div>
    <div style="font-family:'DM Sans';font-weight:600;font-size:26px;color:white;line-height:1.35;">
      Alumni respond at 3x the rate of cold connections. Same university = automatic shared identity.</div>
  </div>
  <div style="background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 26px;
               border-left:4px solid {AMBER};">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;margin-bottom:8px;word-break:keep-all;hyphens:none;">
      Where to find them</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.6);line-height:1.4;">
      LinkedIn: search [Company Name] + [Your University]. Most profiles list education. Start with people who graduated 2-5 years ahead of you - they remember what it was like to be in your position.</div>
  </div>
  <div style="background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 26px;
               border-left:4px solid {PURPLE};">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;margin-bottom:8px;word-break:keep-all;hyphens:none;">
      What to ask for</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.6);line-height:1.4;">
      Not a referral first. Ask one specific question about the role or team. The referral ask comes naturally in the follow-up, after they know who you are.</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: After the referral lands ────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    steps = [
        ("Say thank you immediately", "Same day. Brief. Name one specific thing you appreciated about their help. Don't make it transactional."),
        ("Keep them updated", "A short message when you get an interview. Another when you get the outcome. Nobody wants to wonder what happened to the person they helped."),
        ("Return the favour eventually", "When you're on the inside, pay it forward. The network you build now compounds over time."),
        ("Don't over-rely on the intro", "A referral gets you seen. The interview is still yours to win. Don't assume the work is done."),
    ]
    rows = "".join([f"""<div style="display:flex;gap:16px;align-items:flex-start;padding:16px 0;
                          border-bottom:1px solid rgba(255,255,255,0.07);">
  <div style="width:36px;height:36px;border-radius:50%;background:{CORAL};flex-shrink:0;
               display:flex;align-items:center;justify-content:center;font-family:Inter;
               font-weight:700;font-size:18px;color:{DARK_NAVY};">{i+1}</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;word-break:keep-all;hyphens:none;">{t}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.55);
                 margin-top:5px;line-height:1.35;">{d}</div>
  </div>
</div>""" for i, (t, d) in enumerate(steps)])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:22px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6, bg=CORAL, fg=DARK_NAVY)}
<div style="padding-top:60px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">AFTER THE INTRO</div>
  <div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
               color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Don't drop the <em style="color:{CORAL};font-style:italic;">follow-through.</em>
  </div>
</div>
<div style="flex:1;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA — arch+cutout RIGHT, OFF_WHITE bg ───────────────────────────
def _slide7(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    checks = _checklist(["Find 5 alumni at your target company", "Ask one specific question first",
                          "Referral ask comes in the follow-up", "Always update them on the outcome"],
                         CORAL, DARK_NAVY, DARK_NAVY)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;}}
{GRAIN_DARK}
.arch{{position:absolute;bottom:0;right:0;width:460px;height:680px;
       background:{CORAL};border-radius:230px 230px 0 0;z-index:5;}}
.person{{position:absolute;bottom:0;right:0;width:520px;height:740px;z-index:10;
          filter:drop-shadow(0 20px 50px rgba(255,107,107,0.4));}}
.person img{{width:100%;height:100%;object-fit:contain;object-position:bottom center;}}
.content{{position:absolute;top:0;left:0;width:580px;height:1080px;
           padding:44px 50px;display:flex;flex-direction:column;justify-content:center;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_color()}
<div class="arch"></div>
<div class="person"><img src="{photo_src}"></div>
<div class="content">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{CORAL};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;margin-top:80px;">WARM > COLD</div>
  <div style="font-family:Inter;font-weight:700;font-size:62px;line-height:0.95;
               color:{DARK_NAVY};letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    One intro.<br>Real <em style="color:{CORAL};">results.</em></div>
  <div style="margin-top:28px;display:flex;flex-direction:column;gap:12px;">
    {checks}
  </div>
  <div style="margin-top:32px;background:{CORAL};color:{DARK_NAVY};padding:16px 28px;
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
    print("Generating Referral Advantage (Week 6, Day 4)...")
    _load_logos()
    used_before = get_used_hashes()

    photo_path = get_cutout_unique(
        "young professional smiling handshake confident studio white background",
        orientation="portrait", extra_exclude=used_before
    )
    photo_hash = os.path.basename(photo_path).replace("_nobg.png", "")

    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), photo_path)

    register_used_hashes([photo_hash], "week6/d4-referral", "week6")
    register_design("coral_two_column_contrast_typography", "week6/d4-referral", "week6")
    print("Done - referral advantage complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week6/d4-referral")
