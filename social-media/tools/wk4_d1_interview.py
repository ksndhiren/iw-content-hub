"""
Internwise -Interview Questions Carousel (Week 4, Day 1) -v3
8-slide carousel: 5 interview Q&As with answer frameworks
v3: logo pre-warm fix, 5 unique photos, larger body text
"""
import os, base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_cutout

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B";     PURPLE = "#7B5CE6";    MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"; LIGHT_BLUE = "#5FA7E5"

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

def _src(path):
    if not path: return ""
    b64 = _b64(path)
    if not b64: return ""
    mime = "image/png" if path.endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{b64}"

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

LOGO_B64 = None
def _load_logo():
    global LOGO_B64
    if LOGO_B64 is None:
        LOGO_B64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
    return LOGO_B64

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px);background-size:3px 3px;}"

def _spark(s,t,l,c,o=0.5):
    return f'<svg style="position:absolute;top:{t}px;left:{l}px;z-index:3;" width="{s}" height="{s}" viewBox="0 0 40 40"><path d="M20 4L23 17L36 20L23 23L20 36L17 23L4 20L17 17Z" fill="{c}" opacity="{o}"/></svg>'

def _arch_photo(src, accent):
    if not src: return ""
    return f"""
<div style="position:absolute;bottom:0;right:0;width:460px;height:610px;
            background:linear-gradient(155deg,{accent},{accent}88);
            border-radius:230px 230px 0 0;z-index:5;
            box-shadow:-10px 0 40px rgba(0,0,0,0.2);"></div>
<div style="position:absolute;bottom:0;right:0;width:500px;height:700px;
            z-index:10;filter:drop-shadow(0 20px 40px rgba(0,0,0,0.35));overflow:hidden;">
  <img src="{src}" style="width:100%;height:100%;object-fit:contain;object-position:bottom center;">
</div>"""


# ── Slide 1: Hook ─────────────────────────────────────────────────────────────
def _slide1(out, photo_src):
    f = _fonts()
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.badge{{position:absolute;top:44px;right:44px;
    background:{AMBER};color:{DEEP_BLUE};
    padding:11px 26px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(4deg);
    box-shadow:0 8px 22px rgba(255,177,32,0.45);z-index:20;}}
.content{{position:absolute;top:148px;left:50px;right:530px;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:20px;
    color:{AMBER};text-transform:uppercase;letter-spacing:4px;margin-bottom:14px;}}
.hl{{font-family:Inter;font-weight:700;font-size:80px;line-height:0.95;
    color:white;letter-spacing:-4px;margin-bottom:20px;}}
.hl em{{color:{AMBER};font-style:italic;}}
.accent-bar{{width:70px;height:4px;background:{AMBER};border-radius:2px;margin-bottom:20px;}}
.sub{{font-family:'DM Sans';font-weight:600;font-size:26px;
    color:rgba(255,255,255,0.65);line-height:1.4;}}
.hint{{position:absolute;bottom:44px;left:50px;z-index:20;
    font-family:Inter;font-weight:700;font-size:20px;color:rgba(255,255,255,0.38);}}
.hint strong{{color:rgba(255,255,255,0.7);}}
</style></head><body><div class="c">
<div class="grain"></div>
{_arch_photo(photo_src, AMBER)}
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:20;">
<div class="badge">Interview guide</div>
<div class="content">
  <div class="kicker">Get the offer</div>
  <div class="hl">5 questions<br>every recruiter<br><em>always</em> asks.</div>
  <div class="accent-bar"></div>
  <div class="sub">Here's the exact framework<br>to answer each one.</div>
</div>
<div class="hint">Swipe for the full playbook <strong>→</strong></div>
{_spark(28,160,420,AMBER,0.5)}
{_spark(16,380,390,'white',0.2)}
</div></body></html>"""
    _render(html, out)


# ── Question slides 2-6 ───────────────────────────────────────────────────────
QUESTIONS = [
    {
        "n": 2, "num_label": "Q1 / 5", "accent": AMBER,
        "question": '"Tell me about yourself."',
        "formula_name": "Past - Present - Future",
        "steps": [
            ("P", "Past",    "Where you've been -degree, relevant roles, key things you learned."),
            ("P", "Present", "What you do well right now and what you bring to this role."),
            ("F", "Future",  "Why this role, this company, at this point in your career."),
        ],
        "tip": "Not your life story. Your pitch. Keep it under 90 seconds and practice out loud until it flows.",
    },
    {
        "n": 3, "num_label": "Q2 / 5", "accent": CORAL,
        "question": '"Why do you want to work here?"',
        "formula_name": "Research - Align - Aspire",
        "steps": [
            ("R", "Research", "Name something specific about this company -not just 'great reputation'."),
            ("A", "Align",    "Show how your skills directly match what they need right now."),
            ("A", "Aspire",   "What you want to build or learn in this specific environment."),
        ],
        "tip": "If your answer works for any company, you haven't done enough research. Be specific.",
    },
    {
        "n": 4, "num_label": "Q3 / 5", "accent": MINT,
        "question": '"What\'s your biggest weakness?"',
        "formula_name": "Real - Addressed - Growing",
        "steps": [
            ("R", "Real",      "Name an actual weakness. Not 'I work too hard' or 'I care too much'."),
            ("A", "Addressed", "What you're actively doing about it -a course, habit, or daily practice."),
            ("G", "Growing",   "Evidence it's improving -a result, piece of feedback, or measurable shift."),
        ],
        "tip": "They know you have weaknesses. Genuine self-awareness scores higher than deflecting.",
    },
    {
        "n": 5, "num_label": "Q4 / 5", "accent": PURPLE,
        "question": '"Tell me about a time you..."',
        "formula_name": "STAR Method",
        "steps": [
            ("S", "Situation", "Set the scene briefly -two sentences maximum."),
            ("T", "Task",      "What was your specific role or responsibility?"),
            ("A", "Action",    "What YOU did. Use 'I', not 'we'. Make it specific."),
            ("R", "Result",    "What changed? Quantify if possible. What did you learn?"),
        ],
        "tip": "Prepare 5 STAR stories before any interview. They cover around 80% of behavioural questions.",
    },
    {
        "n": 6, "num_label": "Q5 / 5", "accent": LIGHT_BLUE,
        "question": '"Where do you see yourself in 5 years?"',
        "formula_name": "Company - Growth - Honest",
        "steps": [
            ("C", "Company", "Show you want to grow within this organisation, not just use it as a stepping stone."),
            ("G", "Growth",  "Name specific skills or responsibilities you want to build here."),
            ("H", "Honest",  "You don't need a 5-year plan. Show genuine ambition and curiosity."),
        ],
        "tip": "They're testing ambition and cultural fit -not whether you have a perfectly mapped roadmap.",
    },
]

def _question_slide(q, photo_src, out):
    f = _fonts()
    accent = q["accent"]
    dark_accent = accent in (AMBER, MINT, LIGHT_BLUE)
    accent_text = DEEP_BLUE if dark_accent else "white"

    step_colors = [AMBER, CORAL, MINT, PURPLE, LIGHT_BLUE]
    steps_html = ""
    for i, (badge, label, desc) in enumerate(q["steps"]):
        sc = step_colors[i % len(step_colors)]
        sc_text = DEEP_BLUE if sc in (AMBER, MINT, LIGHT_BLUE) else "white"
        steps_html += f"""
<div style="display:flex;align-items:flex-start;gap:14px;
            padding:16px 18px;background:rgba(255,255,255,0.06);
            border-radius:12px;border-left:4px solid {accent};">
  <div style="width:48px;height:48px;border-radius:50%;flex-shrink:0;
              background:{sc};display:flex;align-items:center;justify-content:center;
              font-family:Inter;font-weight:700;font-size:20px;color:{sc_text};">{badge}</div>
  <div style="padding-top:3px;">
    <div style="font-family:Inter;font-weight:700;font-size:24px;
                color:{accent};line-height:1.1;margin-bottom:4px;">{label}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:21px;
                color:rgba(255,255,255,0.75);line-height:1.35;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.bar{{position:absolute;top:0;left:0;width:6px;height:100%;background:{accent};z-index:10;
      box-shadow:0 0 20px {accent}55;}}
.num{{position:absolute;top:48px;right:44px;font-family:Inter;font-weight:700;font-size:14px;
    color:rgba(255,255,255,0.3);letter-spacing:2px;z-index:25;}}
.url{{position:absolute;bottom:36px;right:44px;font-family:Inter;font-weight:700;font-size:14px;
    color:rgba(255,255,255,0.2);z-index:25;letter-spacing:0.5px;}}
.col{{position:absolute;top:126px;left:50px;right:534px;
      display:flex;flex-direction:column;gap:0;z-index:20;overflow:hidden;max-height:910px;}}
.pill{{align-self:flex-start;background:{accent};color:{accent_text};
    padding:8px 22px;border-radius:50px;font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;}}
.question{{font-family:Inter;font-weight:700;font-size:50px;line-height:1.06;
    color:white;letter-spacing:-2px;margin-bottom:16px;}}
.divider{{height:2px;background:rgba(255,255,255,0.1);margin-bottom:14px;}}
.formula-label{{font-family:'DM Sans';font-weight:700;font-size:16px;
    color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;}}
.steps{{display:flex;flex-direction:column;gap:10px;margin-bottom:16px;}}
.tip{{background:rgba(255,255,255,0.05);border-radius:12px;
    padding:16px 18px;border:1px solid rgba(255,255,255,0.1);}}
.tip-label{{font-family:'DM Sans';font-weight:700;font-size:15px;
    color:{accent};text-transform:uppercase;letter-spacing:2px;}}
.tip-text{{font-family:'DM Sans';font-weight:600;font-size:21px;
    color:rgba(255,255,255,0.68);margin-top:5px;line-height:1.4;}}
</style></head><body><div class="c">
<div class="grain"></div>
<div class="bar"></div>
{_arch_photo(photo_src, accent)}
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:50px;height:66px;opacity:0.95;z-index:25;">
<div class="num">{q['num_label']}</div>
<div class="url">internwise.co.uk</div>
<div class="col">
  <div class="pill">{q['formula_name']}</div>
  <div class="question">{q['question']}</div>
  <div class="divider"></div>
  <div class="formula-label">The framework</div>
  <div class="steps">{steps_html}</div>
  <div class="tip">
    <div class="tip-label">Key insight</div>
    <div class="tip-text">{q['tip']}</div>
  </div>
</div>
{_spark(16,240,420,accent,0.2)}
</div></body></html>"""
    _render(html, out)


# ── Slide 7: What they're scoring ─────────────────────────────────────────────
def _slide7(out, photo_src):
    f = _fonts()
    criteria = [
        (AMBER, "Clarity",        "Can you think and communicate clearly under pressure? Every answer tests this."),
        (CORAL, "Self-awareness", "Do you actually know your strengths and weaknesses? They'll find out if you don't."),
        (MINT,  "Fit",            "Does your story match what this team needs? Research makes the difference."),
    ]
    criteria_html = ""
    for color, label, desc in criteria:
        ct = DEEP_BLUE if color in (AMBER, MINT) else "white"
        criteria_html += f"""
<div style="display:flex;align-items:flex-start;gap:16px;
            padding:20px 22px;background:rgba(255,255,255,0.06);
            border-radius:14px;border-left:4px solid {color};">
  <div style="width:50px;height:50px;border-radius:50%;flex-shrink:0;
              background:{color};display:flex;align-items:center;justify-content:center;">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{ct}"
         stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
  </div>
  <div>
    <div style="font-family:Inter;font-weight:700;font-size:24px;color:{color};line-height:1;">{label}</div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:20px;
                color:rgba(255,255,255,0.68);margin-top:5px;line-height:1.4;">{desc}</div>
  </div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
{GRAIN}
.col{{position:absolute;top:44px;left:50px;right:534px;
      display:flex;flex-direction:column;gap:0;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:18px;color:{AMBER};
    text-transform:uppercase;letter-spacing:4px;margin-top:108px;margin-bottom:12px;}}
.hl{{font-family:Inter;font-weight:700;font-size:60px;line-height:0.96;
    color:white;letter-spacing:-3px;margin-bottom:18px;}}
.hl em{{color:{AMBER};font-style:italic;}}
.divider{{height:2px;background:rgba(255,255,255,0.1);margin-bottom:18px;}}
.criteria{{display:flex;flex-direction:column;gap:14px;margin-bottom:20px;}}
.footer{{font-family:'DM Sans';font-weight:600;font-size:22px;
    color:rgba(255,255,255,0.45);line-height:1.4;}}
.footer strong{{color:rgba(255,255,255,0.75);}}
.badge{{position:absolute;top:44px;right:44px;background:rgba(255,255,255,0.1);
    color:rgba(255,255,255,0.7);padding:9px 22px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:13px;letter-spacing:2px;
    text-transform:uppercase;z-index:20;border:1.5px solid rgba(255,255,255,0.15);}}
</style></head><body><div class="c">
<div class="grain"></div>
{_arch_photo(photo_src, AMBER)}
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:25;">
<div class="badge">The hidden scorecard</div>
<div class="col">
  <div class="kicker">What they're really scoring</div>
  <div class="hl">3 things they<br><em>listen for</em><br>in every answer.</div>
  <div class="divider"></div>
  <div class="criteria">{criteria_html}</div>
  <div class="footer">The best answers are <strong>prepared, not improvised.</strong></div>
</div>
{_spark(26,150,420,AMBER,0.45)}
</div></body></html>"""
    _render(html, out)


# ── Slide 8: CTA ──────────────────────────────────────────────────────────────
def _slide8(out, photo_src):
    f = _fonts()
    checks = [
        (AMBER,  DEEP_BLUE, "1", "Past - Present - Future for your intro"),
        (CORAL,  "white",   "2", "5 STAR stories practiced and ready"),
        (MINT,   DEEP_BLUE, "3", "Company-specific research done"),
        (PURPLE, "white",   "4", "A real weakness with a real fix"),
    ]
    checks_html = "".join(f"""
<div style="display:flex;align-items:center;gap:14px;">
  <div style="width:38px;height:38px;border-radius:50%;flex-shrink:0;
              background:{bg};display:flex;align-items:center;justify-content:center;
              font-family:Inter;font-weight:700;font-size:17px;color:{ct};">{num}</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:22px;color:{DEEP_BLUE};">{text}</div>
</div>""" for bg, ct, num, text in checks)

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;background:{OFF_WHITE};}}
.grain2{{position:absolute;inset:0;z-index:2;pointer-events:none;
    background-image:radial-gradient(rgba(0,0,0,0.025) 1px,transparent 1px);
    background-size:3px 3px;}}
.col{{position:absolute;top:44px;left:60px;right:534px;
      display:flex;flex-direction:column;gap:0;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:19px;color:{AMBER};
    text-transform:uppercase;letter-spacing:4px;margin-top:130px;margin-bottom:12px;}}
.big{{font-family:Inter;font-weight:700;font-size:82px;line-height:1.0;
    color:{DEEP_BLUE};letter-spacing:-4px;margin-bottom:22px;}}
.big em{{color:{AMBER};font-style:italic;text-shadow:4px 4px 0 {CORAL};}}
.checks{{display:flex;flex-direction:column;gap:14px;margin-bottom:24px;}}
.cta{{background:{DEEP_BLUE};color:white;padding:22px 30px;border-radius:18px;
    font-family:Inter;font-weight:700;font-size:22px;
    border:3px solid {DARK_NAVY};box-shadow:5px 5px 0 {DARK_NAVY};
    display:flex;align-items:center;justify-content:space-between;}}
.arrow{{width:54px;height:54px;background:{AMBER};border-radius:50%;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;}}
.badge{{position:absolute;top:44px;right:44px;background:{DEEP_BLUE};color:white;
    padding:11px 24px;border-radius:50px;font-family:Inter;font-weight:700;font-size:14px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(-3deg);
    box-shadow:5px 5px 0 {DARK_NAVY};z-index:20;}}
</style></head><body><div class="c">
<div class="grain2"></div>
{_arch_photo(_src(photo_src), DEEP_BLUE)}
<img src="data:image/png;base64,{LOGO_B64}" style="position:absolute;top:44px;left:60px;height:66px;opacity:0.95;z-index:25;filter:brightness(0) saturate(100%) invert(18%) sepia(34%) saturate(1289%) hue-rotate(183deg) brightness(94%) contrast(91%);">
<div class="badge">Now go get it</div>
<div class="col">
  <div class="kicker">Your pre-interview checklist</div>
  <div class="big">Walk in<br><em>prepared.</em></div>
  <div class="checks">{checks_html}</div>
  <div class="cta">
    <div>
      <div>Find roles worth preparing for</div>
      <div style="font-family:Inter;font-weight:700;font-size:16px;color:{AMBER};margin-top:4px;">internwise.co.uk →</div>
    </div>
    <div class="arrow">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <path d="M5 12L19 12M14 7L20 12L14 17" stroke="{DEEP_BLUE}" stroke-width="2.5"
              fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
</div>
{_spark(28,175,420,AMBER,0.45)}
</div></body></html>"""
    _render(html, out)


# ── Main ──────────────────────────────────────────────────────────────────────
def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Interview Questions Carousel v3 (Week 4, Day 1)...")
    _load_logo()  # pre-warm LOGO_B64 before any slide function uses it

    print("  Fetching photos...")
    photos = {}
    # Slot "a" (slide 1 hook) pinned to approved cached portrait -bypasses Pexels lookup
    PINNED_A = os.path.join(BASE_DIR, "assets", "pexels_cache", "e43d462e906a_nobg.png")
    photos["a"] = PINNED_A if os.path.exists(PINNED_A) else None
    print(f"    ok a (pinned): {photos['a']}")

    for key, query, idx in [
        # All queries target plain white/neutral studio backdrops for clean BG removal
        ("b", "young man professional portrait plain white background studio headshot", 0),
        ("c", "woman career professional headshot isolated white background studio photography", 0),
        ("d", "young man graduate portrait plain white background studio headshot smiling", 0),
        ("e", "professional woman headshot white background photography studio portrait confident", 0),
        ("f", "young woman portrait plain white background studio headshot ambitious graduate", 1),
        ("g", "young man portrait plain white background studio headshot relaxed professional", 1),
        ("h", "young man business suit interview ready confident standing white background studio", 0),
    ]:
        try:
            photos[key] = get_cutout(query, index=idx, orientation="portrait")
            print(f"    ok {key}: {photos[key]}")
        except Exception as e:
            print(f"    ! {key} failed: {e}")
            photos[key] = None

    # 8 unique photos -one per slide, zero repeats
    photo_map = {
        1: photos.get("a"), 2: photos.get("b"), 3: photos.get("c"),
        4: photos.get("d"), 5: photos.get("e"), 6: photos.get("f"),
        7: photos.get("g"), 8: photos.get("h"),
    }

    _slide1(os.path.join(campaign_dir, "slide_1.png"), _src(photo_map[1]))
    for q in QUESTIONS:
        _question_slide(q, _src(photo_map[q['n']]), os.path.join(campaign_dir, f"slide_{q['n']}.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"), _src(photo_map[7]))
    _slide8(os.path.join(campaign_dir, "slide_8.png"), photo_map[8])
    print("Done - interview questions carousel v3 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week4/d1-interview")
