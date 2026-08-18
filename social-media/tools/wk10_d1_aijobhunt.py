"""
Internwise - Using AI to Job-Hunt (Week 10, Day 1)
Design language: SCI-FI AI HUD. Dark interface, neon cyan/green, bordered HUD
panels with corner brackets, circuit lines, monospace labels, glowing text.
7 slides. Accent: NEON_CYAN + NEON_GREEN on deep space.
Mobile floors: headline 52px+, body 28px+, card title 26px+, label 18px+.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; OFF_WHITE = "#FAF5EC"; CORAL = "#FF6B6B"; AMBER = "#FFB120"
HUD_BG    = "#060B18"; HUD_BG2 = "#0B1428"
CYAN      = "#22E3D6"; CYAN_DK = "#12A79C"
NEON      = "#8CFFB0"; NEON_DK = "#3FD07A"
GRID_LINE = "rgba(34,227,214,0.12)"
MONO = "Menlo,Monaco,'Courier New',monospace"

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

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;
      background:radial-gradient(ellipse at 70% 12%,{HUD_BG2} 0%,{HUD_BG} 70%);}}
.c{{width:1080px;height:1080px;position:relative;padding:52px 56px;display:flex;flex-direction:column;}}
.grid{{position:absolute;inset:0;z-index:1;pointer-events:none;
       background-image:linear-gradient({GRID_LINE} 1px,transparent 1px),
       linear-gradient(90deg,{GRID_LINE} 1px,transparent 1px);background-size:54px 54px;}}
.scan{{position:absolute;inset:0;z-index:2;pointer-events:none;
       background:repeating-linear-gradient(0deg,rgba(140,255,176,0.03) 0 2px,transparent 2px 4px);}}
"""

# HUD panel with corner brackets
def _panel(inner, extra="", border=CYAN):
    return f"""<div style="position:relative;border:1.5px solid {border}55;border-radius:12px;
             background:rgba(11,20,40,0.55);{extra}">
  <span style="position:absolute;top:-2px;left:-2px;width:16px;height:16px;border-top:2px solid {border};border-left:2px solid {border};"></span>
  <span style="position:absolute;top:-2px;right:-2px;width:16px;height:16px;border-top:2px solid {border};border-right:2px solid {border};"></span>
  <span style="position:absolute;bottom:-2px;left:-2px;width:16px;height:16px;border-bottom:2px solid {border};border-left:2px solid {border};"></span>
  <span style="position:absolute;bottom:-2px;right:-2px;width:16px;height:16px;border-bottom:2px solid {border};border-right:2px solid {border};"></span>
  {inner}
</div>"""

def _mono_label(text, color=CYAN):
    return (f'<span style="font-family:{MONO};font-size:18px;color:{color};letter-spacing:3px;'
            f'text-transform:uppercase;">{text}</span>')

def _neon_head(html, size=58):
    return (f'<div style="font-family:Inter;font-weight:700;font-size:{size}px;line-height:1.0;'
            f'color:#EAFBFF;letter-spacing:-2px;word-break:keep-all;hyphens:none;'
            f'text-shadow:0 0 22px rgba(34,227,214,0.35);">{html}</div>')

def _num(n):
    return (f'<div style="position:absolute;top:48px;left:56px;width:54px;height:54px;'
            f'border:1.5px solid {CYAN};border-radius:10px;display:flex;align-items:center;'
            f'justify-content:center;font-family:{MONO};font-weight:700;font-size:22px;color:{CYAN};'
            f'z-index:20;box-shadow:0 0 16px rgba(34,227,214,0.3);">{n:02d}</div>')

# central AI core svg
def _ai_core(size=260):
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 260 260" xmlns="http://www.w3.org/2000/svg">
  <defs><radialGradient id="core" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{NEON}"/><stop offset="0.6" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN_DK}"/>
  </radialGradient></defs>
  <circle cx="130" cy="130" r="120" fill="none" stroke="{CYAN}" stroke-width="1.5" opacity="0.3" stroke-dasharray="4 8"/>
  <circle cx="130" cy="130" r="92" fill="none" stroke="{CYAN}" stroke-width="1.5" opacity="0.5"/>
  <circle cx="130" cy="130" r="60" fill="none" stroke="{NEON}" stroke-width="2" opacity="0.7"/>
  <circle cx="130" cy="130" r="34" fill="url(#core)"/>
  <text x="130" y="140" text-anchor="middle" font-family="Inter" font-weight="700" font-size="26" fill="#04121A">AI</text>
  <g fill="{CYAN}"><circle cx="130" cy="10" r="4"/><circle cx="250" cy="130" r="4"/><circle cx="130" cy="250" r="4"/><circle cx="10" cy="130" r="4"/></g>
  <g fill="{NEON}"><circle cx="222" cy="38" r="3"/><circle cx="222" cy="222" r="3"/><circle cx="38" cy="222" r="3"/><circle cx="38" cy="38" r="3"/></g>
</svg>"""


def _shell(inner, f):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_base_css(f)}</style></head>
<body><div class="c"><div class="grid"></div><div class="scan"></div>{inner}</div></body></html>"""


# ── Slide 1: Hook ───────────────────────────────────────────────────────────
def _slide1(out):
    f = _fonts()
    inner = f"""
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;position:relative;z-index:10;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:54px;">
  {_panel(f'<div style="padding:9px 18px;">{_mono_label("SYSTEM // JOBHUNT.AI", NEON)}</div>', border=NEON)}
</div>
<div style="flex:1;display:flex;align-items:center;gap:24px;position:relative;z-index:10;">
  <div style="flex:1;">
    <div style="margin-bottom:20px;">{_mono_label("MODULE 01 / AI + YOUR SEARCH", CYAN)}</div>
    {_neon_head('Use AI to<br>job-hunt.<br><span style="color:'+CYAN+';">Smarter,</span><br>not lazier.', 88)}
    <div style="font-family:'DM Sans';font-weight:500;font-size:29px;color:#9FC7D4;margin-top:24px;line-height:1.35;max-width:560px;">
      The tools are here. Most grads use them wrong. Here's the sharp way.
    </div>
  </div>
  <div style="width:300px;flex-shrink:0;display:flex;align-items:center;justify-content:center;
               filter:drop-shadow(0 0 30px rgba(34,227,214,0.4));">{_ai_core(280)}</div>
</div>
<div style="flex-shrink:0;display:flex;justify-content:flex-end;position:relative;z-index:10;">
  {_mono_label("SWIPE >>", CYAN)}
</div>
"""
    _render(_shell(inner, f), out)


# ── Slide 2: The Data ───────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("64%", "of recruiters now use AI to screen applications. You should use it too.", CYAN),
        ("4x", "faster to tailor a CV per role with AI - the biggest time sink, gone.", NEON),
        ("0", "AI tools can invent experience for you. It drafts; you verify. Always.", CORAL),
    ]
    cards = ""
    for val, label, col in stats:
        cards += _panel(f"""<div style="padding:32px 26px;height:100%;display:flex;flex-direction:column;">
  <div style="font-family:Inter;font-weight:700;font-size:72px;color:{col};letter-spacing:-3px;line-height:1;
               text-shadow:0 0 20px {col}66;">{val}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:25px;color:#B7D4DC;margin-top:18px;line-height:1.4;">{label}</div>
</div>""", extra="flex:1;", border=col)
    inner = f"""
<div style="flex-shrink:0;position:relative;z-index:10;">
  <div style="margin-bottom:12px;">{_mono_label("DATA STREAM", CYAN)}</div>
  {_neon_head('AI is already <span style="color:'+CYAN+';">in the loop.</span>', 54)}
</div>
<div style="flex:1;display:flex;gap:22px;margin:38px 0 18px 0;position:relative;z-index:10;">{cards}</div>
<div style="flex-shrink:0;font-family:{MONO};font-size:18px;color:#5E8894;text-align:right;position:relative;z-index:10;">
  SRC: LINKEDIN TALENT 2026 // JOBSCAN 2025
</div>
"""
    _render(_shell(inner, f), out)


# ── Slides 3-6: the four smart uses ─────────────────────────────────────────
def _use_slide(out, n, label, headline, prompt_title, prompt_body, rule):
    f = _fonts()
    inner = f"""
{_num(n)}
<div style="padding-top:78px;flex-shrink:0;position:relative;z-index:10;">
  <div style="margin-bottom:12px;">{_mono_label(label, CYAN)}</div>
  {_neon_head(headline, 54)}
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:20px;margin-top:34px;justify-content:center;position:relative;z-index:10;">
  {_panel(f'''<div style="padding:28px 30px;">
    <div style="font-family:{MONO};font-size:18px;color:{NEON};letter-spacing:2px;margin-bottom:12px;">&gt; {prompt_title}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:27px;color:#DCEEF2;line-height:1.45;font-style:italic;">"{prompt_body}"</div>
  </div>''', border=NEON)}
  <div style="display:flex;align-items:flex-start;gap:14px;padding:0 6px;">
    <div style="width:26px;height:26px;border-radius:50%;border:2px solid {CORAL};display:flex;align-items:center;
                 justify-content:center;font-family:{MONO};font-weight:700;font-size:15px;color:{CORAL};flex-shrink:0;margin-top:3px;">!</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#9FC7D4;line-height:1.4;">{rule}</div>
  </div>
</div>
"""
    _render(_shell(inner, f), out)

def _slide3(out): _use_slide(out, 3, "USE 01 / TAILOR",
    'Rewrite your CV <span style="color:'+CYAN+';">per role.</span>',
    "PROMPT",
    "Here's my CV and this job spec. Rewrite my summary and top 3 bullets to match their language, keeping every fact true.",
    "It mirrors their keywords (which beats the ATS). You check every line is still accurate.")

def _slide4(out): _use_slide(out, 4, "USE 02 / PREP",
    'Rehearse the <span style="color:'+CYAN+';">hard questions.</span>',
    "PROMPT",
    "Act as an interviewer for this role. Ask me one behavioural question, then critique my answer against the STAR method.",
    "You get unlimited reps and honest feedback. Say your answers out loud, not just in your head.")

def _slide5(out): _use_slide(out, 5, "USE 03 / RESEARCH",
    'Decode the <span style="color:'+CYAN+';">company fast.</span>',
    "PROMPT",
    "Summarise this company's last 3 announcements and give me two smart questions to ask that show I did my homework.",
    "Cross-check what it says against the real source. AI summarises; it also sometimes makes things up.")

def _slide6(out): _use_slide(out, 6, "USE 04 / POLISH",
    'Sharpen, don\'t <span style="color:'+CORAL+';">fake.</span>',
    "PROMPT",
    "Tighten this cover letter to 150 words, keep my voice, and flag anything that sounds generic or over-claimed.",
    "Editing is fair game. Inventing achievements is not - one probing interview question and it falls apart.")


# ── Slide 7: CTA ────────────────────────────────────────────────────────────
def _slide7(out):
    f = _fonts()
    steps = ["Tailor your CV to the next role you apply for","Run one mock interview out loud","Research before every call","Never let it invent - only assist"]
    rows = ""
    for i, s in enumerate(steps):
        rows += f"""<div style="display:flex;gap:14px;align-items:center;padding:8px 0;">
  <span style="font-family:{MONO};font-size:22px;color:{NEON};">[{i+1}]</span>
  <span style="font-family:'DM Sans';font-weight:500;font-size:27px;color:#DCEEF2;">{s}</span>
</div>"""
    inner = f"""
<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;position:relative;z-index:10;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:54px;">
  {_panel(f'<div style="padding:9px 18px;">{_mono_label("RUN CHECKLIST", NEON)}</div>', border=NEON)}
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:10;">
  {_neon_head('AI is your <span style="color:'+CYAN+';">co-pilot.</span><br>You still fly.', 74)}
  <div style="margin-top:30px;">{_panel(f'<div style="padding:28px 32px;">{rows}</div>', border=CYAN)}</div>
  <div style="margin-top:28px;display:inline-flex;align-items:center;gap:12px;background:{CYAN};color:{HUD_BG};
               padding:18px 32px;border-radius:10px;font-family:Inter;font-weight:700;font-size:24px;width:fit-content;
               box-shadow:0 0 26px rgba(34,227,214,0.5);">
    Find roles at internwise.co.uk &rarr;
  </div>
</div>
"""
    _render(_shell(inner, f), out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating AI Job-Hunt (Week 10, Day 1)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("scifi_ai_hud_neon", "week10/d1-aijobhunt", "week10")
    print("Done - AI job-hunt complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week10/d1-aijobhunt")
