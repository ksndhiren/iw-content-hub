"""
Internwise - How to Write a Personal Statement (Week 6, Day 3)
Hook: DARK_NAVY bg, arch+cutout LEFT side (mirrored), ghost "PS" text, PURPLE accent.
7 slides.
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

def _logo_white(): return f'<img src="data:image/png;base64,{LOGO_W}" style="position:absolute;top:44px;right:44px;height:68px;z-index:25;">'
def _logo_color(): return f'<img src="data:image/png;base64,{LOGO_C}" style="position:absolute;top:44px;left:44px;height:68px;z-index:25;">'
def _num_badge(n, bg=PURPLE, fg="white"):
    return f'<div style="position:absolute;top:44px;left:44px;width:52px;height:52px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:22px;color:{fg};z-index:25;">{n}</div>'
def _kicker(text, color=PURPLE):
    return f'<div style="font-family:\'DM Sans\';font-weight:700;font-size:18px;color:{color};text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">{text}</div>'


# ── Slide 1: Hook — arch+cutout LEFT, ghost "PS", DARK_NAVY ───────────────────
def _slide1(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;}}
{GRAIN}
.arch{{position:absolute;bottom:0;left:0;width:460px;height:680px;
       background:{PURPLE};border-radius:230px 230px 0 0;z-index:5;}}
.person{{position:absolute;bottom:0;left:0;width:520px;height:740px;z-index:10;
          filter:drop-shadow(0 20px 50px rgba(123,92,230,0.5));}}
.person img{{width:100%;height:100%;object-fit:contain;object-position:bottom center;}}
.ghost{{position:absolute;right:-40px;top:50%;transform:translateY(-50%);
         font-family:Inter;font-weight:700;font-size:560px;line-height:1;
         color:{PURPLE};opacity:0.07;z-index:3;user-select:none;letter-spacing:-20px;}}
.content{{position:absolute;top:0;right:0;width:560px;height:1080px;
           padding:44px 50px;display:flex;flex-direction:column;justify-content:center;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_white()}
<div class="ghost">PS</div>
<div class="arch"></div>
<div class="person"><img src="{photo_src}"></div>
<div class="content">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{PURPLE};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:16px;margin-top:80px;">Personal statement</div>
  <div style="font-family:Inter;font-weight:700;font-size:68px;line-height:0.95;
               color:white;letter-spacing:-4px;word-break:keep-all;hyphens:none;">
    Stop writing<br>for the<br>reader.<br><em style="color:{PURPLE};">Write for<br>the role.</em>
  </div>
  <div style="margin-top:24px;font-family:'DM Sans';font-weight:500;font-size:26px;
               color:rgba(255,255,255,0.5);line-height:1.4;">
    A personal statement that works for every role works for none of them.
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 2: What recruiters actually read ────────────────────────────────────
def _slide2(out):
    f = _fonts()
    facts = [
        ("30s", "Under 30 seconds", "Average time a recruiter spends on a personal statement before deciding to read on."),
        ("3", "Top 3 lines decide it", "If your opening paragraph doesn't anchor them, they skim or skip the rest."),
        ("0%", "Generic = instant skip", "If your statement could apply to three different roles, it reads as zero effort."),
    ]
    cards = "".join([f"""<div style="flex:1;background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.1);
                          border-radius:16px;padding:28px 24px;display:flex;flex-direction:column;gap:10px;">
  <div style="font-family:Inter;font-weight:700;font-size:36px;line-height:1;color:{PURPLE};
               letter-spacing:-1px;word-break:keep-all;hyphens:none;">{n}</div>
  <div style="font-family:'DM Sans';font-weight:700;font-size:28px;color:white;word-break:keep-all;hyphens:none;">{t}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.55);line-height:1.4;">{d}</div>
</div>""" for n, t, d in facts])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:28px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(2)}
<div style="padding-top:60px;">{_kicker("WHAT THEY ACTUALLY DO")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
30 seconds. That's your <em style="color:{PURPLE};font-style:italic;">budget.</em></div></div>
<div style="flex:1;display:flex;gap:18px;">{cards}</div>
<div style="background:rgba(123,92,230,0.2);border:2px solid {PURPLE};border-radius:12px;
             padding:16px 24px;font-family:'DM Sans';font-weight:700;font-size:18px;color:{PURPLE};">
The hook is your one line that makes them read the second line. Everything else follows from that.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 3: The four-part structure ──────────────────────────────────────────
def _slide3(out):
    f = _fonts()
    parts = [
        ("01", "The hook", PURPLE, "Why this role, this organisation, right now. One sentence. Specific. No cliches."),
        ("02", "Your evidence", AMBER, "Two or three achievements that map directly to what they're hiring for. Named, quantified where possible."),
        ("03", "What you bring", CORAL, "The skills the role actually needs — tied to real proof, not adjectives like 'passionate' or 'hardworking'."),
        ("04", "The forward link", MINT, "Where you want to go next and why this role is the logical step. Shows you've thought past the application."),
    ]
    rows = "".join([f"""<div style="display:flex;gap:0;border:2px solid rgba(255,255,255,0.08);
                          border-radius:14px;overflow:hidden;background:rgba(255,255,255,0.03);">
  <div style="width:70px;flex-shrink:0;background:{bg};display:flex;align-items:center;
               justify-content:center;font-family:Inter;font-weight:700;font-size:22px;
               color:rgba(22,45,74,0.6) if bg=='{AMBER}' or bg=='{MINT}' else rgba(255,255,255,0.7);">{num}</div>
  <div style="flex:1;padding:18px 22px;display:flex;align-items:center;gap:16px;">
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;
                 min-width:180px;flex-shrink:0;word-break:keep-all;hyphens:none;">{title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;
                 color:rgba(255,255,255,0.55);line-height:1.35;">{desc}</div>
  </div>
</div>""" for num, title, bg, desc in parts])
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
<div style="padding-top:60px;">{_kicker("THE STRUCTURE")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Four parts. One <em style="color:{PURPLE};font-style:italic;">through-line.</em></div></div>
<div style="flex:1;display:flex;flex-direction:column;gap:14px;">{rows}</div>
<div style="background:rgba(255,255,255,0.04);border-radius:12px;padding:16px 24px;
             font-family:'DM Sans';font-weight:700;font-size:18px;color:rgba(255,255,255,0.4);">
Max 250 words for a grad scheme. Every sentence must earn its place.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 4: The hook sentence formula ───────────────────────────────────────
def _slide4(out):
    f = _fonts()
    bad = [
        '"I have always been passionate about finance and believe I would be a great fit."',
        '"I am a hardworking and dedicated individual who is looking to start my career in consulting."',
    ]
    good = [
        '"Your graduate scheme\'s cross-sector rotation is exactly the structure I\'ve been building toward - my 6 months tracking policy change at [charity] showed me why breadth matters in this industry."',
        '"After building a Python tool that tracked 2,000 job postings weekly for a personal project, I want to apply that analytical rigour to the work your team does on market analysis."',
    ]
    bad_cards = "".join([f"""<div style="background:rgba(255,107,107,0.08);border:2px solid {CORAL};
                              border-radius:12px;padding:18px 20px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:11px;color:{CORAL};
               text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">x gets skipped</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.7);
               line-height:1.5;font-style:italic;">{t}</div>
</div>""" for t in bad])
    good_cards = "".join([f"""<div style="background:rgba(127,219,182,0.08);border:2px solid {MINT};
                               border-radius:12px;padding:18px 20px;">
  <div style="font-family:'DM Sans';font-weight:700;font-size:11px;color:{MINT};
               text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">v gets read</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:rgba(255,255,255,0.7);
               line-height:1.5;font-style:italic;">{t}</div>
</div>""" for t in good])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:22px;}}
{GRAIN}
.cols{{flex:1;display:flex;gap:18px;}}
.col{{flex:1;display:flex;flex-direction:column;gap:12px;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(4)}
<div style="padding-top:60px;">{_kicker("THE HOOK LINE")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
The one line that <em style="color:{PURPLE};font-style:italic;">decides it.</em></div></div>
<div class="cols">
  <div class="col">{bad_cards}</div>
  <div class="col">{good_cards}</div>
</div>
<div style="background:rgba(123,92,230,0.15);border:2px solid {PURPLE};border-radius:12px;
             padding:14px 22px;font-family:'DM Sans';font-weight:700;font-size:20px;color:{PURPLE};">
Rule: if your opening line works for any other role at any other company, rewrite it.</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 5: Evidence paragraph method ───────────────────────────────────────
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
{_num_badge(5)}
<div style="padding-top:60px;">{_kicker("YOUR EVIDENCE PARAGRAPH")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
Skills from the JD.<br>Evidence from <em style="color:{PURPLE};font-style:italic;">your life.</em></div></div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;">
  <div style="background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 26px;
               border-left:4px solid {PURPLE};">
    <div style="font-family:'DM Sans';font-weight:700;font-size:14px;color:{PURPLE};
                 text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;">Step 1</div>
    <div style="font-family:Inter;font-weight:700;font-size:22px;color:white;word-break:keep-all;hyphens:none;">
      Pick 3 skills from the job description</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.55);
                 margin-top:8px;line-height:1.4;">
      Use the exact words. Not synonyms. ATS and human readers both scan for this.</div>
  </div>
  <div style="background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 26px;
               border-left:4px solid {AMBER};">
    <div style="font-family:'DM Sans';font-weight:700;font-size:14px;color:{AMBER};
                 text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;">Step 2</div>
    <div style="font-family:Inter;font-weight:700;font-size:22px;color:white;word-break:keep-all;hyphens:none;">
      Match each skill to one real example</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.55);
                 margin-top:8px;line-height:1.4;">
      Coursework, societies, projects, part-time work — all count. Quantify where you can.</div>
  </div>
  <div style="background:rgba(255,255,255,0.04);border-radius:14px;padding:22px 26px;
               border-left:4px solid {CORAL};">
    <div style="font-family:'DM Sans';font-weight:700;font-size:14px;color:{CORAL};
                 text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;">Step 3</div>
    <div style="font-family:Inter;font-weight:700;font-size:22px;color:white;word-break:keep-all;hyphens:none;">
      No soft claims without proof</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:rgba(255,255,255,0.55);
                 margin-top:8px;line-height:1.4;">
      "I am a strong communicator" means nothing. "I wrote a weekly newsletter to 400 subscribers" does.</div>
  </div>
</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 6: 5 things to cut ─────────────────────────────────────────────────
def _slide6(out):
    f = _fonts()
    cuts = [
        ("'I have always been passionate about...'", "Zero evidence. Says nothing recruiters haven't read 1,000 times."),
        ("Your hobbies and interests", "Unless they're directly relevant, this is filler. Use the space for evidence."),
        ("'I am a hardworking team player'", "Adjectives without proof are noise. Replace with a fact."),
        ("A generic career goal", "'I want to develop my skills in a fast-paced environment' tells them nothing about why here."),
        ("Anything over 250 words", "Every extra sentence is a reason to lose their attention. Edit ruthlessly."),
    ]
    rows = "".join([f"""<div style="display:flex;gap:14px;align-items:flex-start;padding:14px 0;
                          border-bottom:1px solid rgba(255,255,255,0.07);">
  <div style="color:{CORAL};font-size:22px;flex-shrink:0;line-height:1.2;">x</div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:white;
                 font-style:italic;word-break:keep-all;hyphens:none;">"{t}"</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;
                 color:rgba(255,255,255,0.5);margin-top:4px;line-height:1.35;">{d}</div>
  </div>
</div>""" for t, d in cuts])
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{DARK_NAVY};}}
.c{{width:1080px;height:1080px;position:relative;padding:50px 60px;
    display:flex;flex-direction:column;gap:22px;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>
{_num_badge(6)}
<div style="padding-top:60px;">{_kicker("CUT THESE NOW")}
<div style="font-family:Inter;font-weight:700;font-size:52px;line-height:1.0;
             color:white;letter-spacing:-2px;word-break:keep-all;hyphens:none;">
5 things that <em style="color:{CORAL};font-style:italic;">kill</em> your statement.</div></div>
<div style="flex:1;">{rows}</div>
</div></body></html>"""
    _render(html, out)


# ── Slide 7: CTA — arch+cutout LEFT, OFF_WHITE bg ─────────────────────────────
def _slide7(out, photo_path):
    f = _fonts()
    photo_src = _src(photo_path)
    checks = _checklist(["Hook names this specific role/company", "3 skills from the JD with real evidence",
                          "Under 250 words total", "Read aloud - rewrite stiff sentences"],
                         PURPLE, "white", DARK_NAVY)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{OFF_WHITE};}}
.c{{width:1080px;height:1080px;position:relative;}}
{GRAIN_DARK}
.arch{{position:absolute;bottom:0;left:0;width:460px;height:680px;
       background:{PURPLE};border-radius:230px 230px 0 0;z-index:5;}}
.person{{position:absolute;bottom:0;left:0;width:520px;height:740px;z-index:10;
          filter:drop-shadow(0 20px 50px rgba(123,92,230,0.35));}}
.person img{{width:100%;height:100%;object-fit:contain;object-position:bottom center;}}
.content{{position:absolute;top:0;right:0;width:540px;height:1080px;
           padding:44px 50px;display:flex;flex-direction:column;justify-content:center;z-index:20;}}
</style></head><body><div class="c">
<div class="grain"></div>
{_logo_color()}
<div class="arch"></div>
<div class="person"><img src="{photo_src}"></div>
<div class="content">
  <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:{PURPLE};
               text-transform:uppercase;letter-spacing:3px;margin-bottom:18px;margin-top:80px;">BEFORE YOU SUBMIT</div>
  <div style="font-family:Inter;font-weight:700;font-size:58px;line-height:0.95;
               color:{DARK_NAVY};letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    One role.<br>One <em style="color:{PURPLE};">statement.</em><br>Every time.</div>
  <div style="margin-top:28px;display:flex;flex-direction:column;gap:12px;">
    {checks}
  </div>
  <div style="margin-top:32px;background:{PURPLE};color:white;padding:16px 28px;
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
    print("Generating Personal Statement (Week 6, Day 3)...")
    _load_logos()
    used_before = get_used_hashes()

    photo1 = get_cutout_unique(
        "young professional writing notebook studio white background",
        orientation="portrait", extra_exclude=used_before
    )
    hash1 = os.path.basename(photo1).replace("_nobg.png", "")

    used_after_1 = used_before | {hash1}
    photo7 = get_cutout_unique(
        "graduate student confident smiling studio white background",
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

    register_used_hashes([hash1, hash7], "week6/d3-personalstatement", "week6")
    register_design("arch_cutout_left_purple", "week6/d3-personalstatement", "week6")
    print("Done - personal statement complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week6/d3-personalstatement")
