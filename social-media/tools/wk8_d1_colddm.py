"""
Internwise - Cold DMs That Actually Work (Week 8, Day 1)
Design language: TERMINAL / CODE EDITOR. Monospace, IDE chrome, syntax-colored
text, blinking cursor block, line numbers, tab bar. Dark IDE background.
7 slides. Accent: TERM_GREEN + TERM_CYAN on IDE_BG.

Mobile font rules held: headline 52px+, body 28px+, card title 26px+, kicker 18px+.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DARK_NAVY = "#162d4a"; AMBER = "#FFB120"; CORAL = "#FF6B6B"
OFF_WHITE = "#FAF5EC"

# IDE palette
IDE_BG      = "#0D1B2A"   # deep editor bg
IDE_PANEL   = "#12263C"   # slightly lighter panel
IDE_GUTTER  = "#0A1420"   # line-number gutter
TERM_GREEN  = "#7FDBB6"   # strings / success
TERM_CYAN   = "#5BC8E8"   # keywords
TERM_AMBER  = "#FFB120"   # warnings / emphasis
TERM_PINK   = "#FF6B9D"   # functions
TERM_GREY   = "#5A7189"   # comments

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

SCANLINE = (".scan{position:absolute;inset:0;z-index:3;pointer-events:none;"
            "background:repeating-linear-gradient(0deg,rgba(255,255,255,0.022) 0px,"
            "rgba(255,255,255,0.022) 1px,transparent 1px,transparent 3px);}")

def _titlebar(tab_name, n_total=7, n_cur=1):
    """macOS-style window chrome with traffic lights + tab."""
    dots = ""
    for c in ["#FF5F57", "#FEBC2E", "#28C840"]:
        dots += f'<div style="width:14px;height:14px;border-radius:50%;background:{c};"></div>'
    return f"""<div style="display:flex;align-items:center;gap:16px;background:{IDE_GUTTER};
             border-bottom:2px solid rgba(255,255,255,0.08);padding:14px 20px;flex-shrink:0;">
  <div style="display:flex;gap:9px;">{dots}</div>
  <div style="background:{IDE_BG};border-top:3px solid {TERM_CYAN};padding:8px 20px;
               border-radius:6px 6px 0 0;margin-bottom:-16px;font-family:{MONO};
               font-size:19px;color:{TERM_CYAN};font-weight:700;">{tab_name}</div>
  <div style="margin-left:auto;font-family:{MONO};font-size:18px;color:{TERM_GREY};">
    {n_cur} / {n_total}
  </div>
</div>"""

def _code_lines(lines, start=1):
    """lines = list of (indent_level, html_content). Renders gutter + code."""
    out = ""
    for i, (indent, content) in enumerate(lines):
        pad = indent * 28
        out += f"""<div style="display:flex;align-items:flex-start;min-height:40px;">
  <div style="width:64px;flex-shrink:0;text-align:right;padding-right:18px;font-family:{MONO};
               font-size:20px;color:{TERM_GREY};line-height:1.65;user-select:none;">{start+i}</div>
  <div style="flex:1;padding-left:{pad}px;font-family:{MONO};font-size:26px;line-height:1.65;
               color:#C8D8E8;word-break:break-word;">{content}</div>
</div>"""
    return out

def _cursor():
    return f'<span style="display:inline-block;width:13px;height:26px;background:{TERM_GREEN};vertical-align:-4px;margin-left:3px;"></span>'

def _comment(t):  return f'<span style="color:{TERM_GREY};">{t}</span>'
def _kw(t):       return f'<span style="color:{TERM_PINK};font-weight:700;">{t}</span>'
def _str_(t):     return f'<span style="color:{TERM_GREEN};">{t}</span>'
def _fn(t):       return f'<span style="color:{TERM_CYAN};">{t}</span>'
def _warn(t):     return f'<span style="color:{TERM_AMBER};font-weight:700;">{t}</span>'

def _shell(inner, tab_name, n_cur):
    """Full IDE window wrapper."""
    return f"""<div class="c">
<div class="scan"></div>
{_titlebar(tab_name, 7, n_cur)}
{inner}
</div>"""

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{IDE_BG};}}
.c{{width:1080px;height:1080px;position:relative;display:flex;flex-direction:column;}}
{SCANLINE}
"""


# ─── Slide 1: Hook — terminal boot + big statement ──────────────────────────
def _slide1(out):
    f = _fonts()
    lines = _code_lines([
        (0, _comment("// most grads never send one.")),
        (0, _comment("// the 4% who do get replies.")),
        (0, "&nbsp;"),
        (0, f'{_kw("const")} {_fn("coldDM")} = {{'),
        (1, f'{_fn("to")}: {_str_("&quot;hiring manager&quot;")},'),
        (1, f'{_fn("length")}: {_str_("&quot;under 90 words&quot;")},'),
        (1, f'{_fn("ask")}: {_str_("&quot;one specific question&quot;")},'),
        (1, f'{_fn("replyRate")}: {_warn("&quot;27%&quot;")}'),
        (0, "};"),
        (0, "&nbsp;"),
        (0, f'{_fn("send")}(coldDM); {_cursor()}'),
    ])
    inner = f"""
<div style="padding:26px 30px 0 0;position:relative;z-index:5;flex-shrink:0;">
  {lines}
</div>
<div style="flex:1;"></div>
<div style="flex-shrink:0;padding:0 50px 44px 50px;position:relative;z-index:5;">
  <div style="font-family:{MONO};font-size:19px;color:{TERM_GREEN};letter-spacing:2px;
               text-transform:uppercase;margin-bottom:14px;">&gt; cold_outreach.js</div>
  <div style="font-family:Inter;font-weight:700;font-size:82px;line-height:0.95;color:white;
               letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    The DM that<br>gets a <span style="color:{TERM_GREEN};font-style:italic;">reply.</span>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:28px;color:#8FA9C0;
               margin-top:20px;line-height:1.35;">
    Recruiters get 200 a week. Here's why 4% get read.
  </div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:26px;">
    <img src="data:image/png;base64,{LOGO_W}" style="height:44px;opacity:0.5;">
    <div style="font-family:{MONO};font-size:20px;color:{TERM_GREY};">SWIPE &rarr;</div>
  </div>
</div>
"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body>{_shell(inner, "cold_outreach.js", 1)}</body></html>"""
    _render(html, out)


# ─── Slide 2: The Data ──────────────────────────────────────────────────────
def _slide2(out):
    f = _fonts()
    stats = [
        ("27%", "reply rate on a specific, researched cold DM", TERM_GREEN),
        ("2%",  "reply rate on a generic 'I'd love to connect'", TERM_PINK),
        ("90",  "word ceiling before a DM gets skimmed and dropped", TERM_CYAN),
    ]
    cards = ""
    for val, label, color in stats:
        cards += f"""<div style="flex:1;background:{IDE_PANEL};border:2px solid rgba(255,255,255,0.10);
             border-left:5px solid {color};border-radius:10px;padding:30px 26px;">
  <div style="font-family:{MONO};font-size:76px;font-weight:700;color:{color};line-height:1;
               letter-spacing:-3px;">{val}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#A8C0D4;
               margin-top:18px;line-height:1.4;">{label}</div>
</div>"""
    inner = f"""
<div style="flex:1;padding:44px 50px;display:flex;flex-direction:column;position:relative;z-index:5;">
  <div style="font-family:{MONO};font-size:19px;color:{TERM_GREEN};letter-spacing:2px;
               text-transform:uppercase;margin-bottom:14px;">&gt; run stats.sh</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Specific beats <span style="color:{TERM_GREEN};font-style:italic;">polite.</span>
  </div>
  <div style="display:flex;gap:20px;margin-top:40px;flex:1;">{cards}</div>
  <div style="font-family:{MONO};font-size:20px;color:{TERM_GREY};margin-top:24px;text-align:right;">
    // sources: LinkedIn Talent Insights 2026, Lavender Outreach Report 2025
  </div>
</div>
"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body>{_shell(inner, "stats.sh", 2)}</body></html>"""
    _render(html, out)


# ─── Slide 3: The anatomy (code-commented template) ─────────────────────────
def _slide3(out):
    f = _fonts()
    lines = _code_lines([
        (0, _comment("// 4 parts. In this order. No filler.")),
        (0, "&nbsp;"),
        (0, f'{_kw("1.")} {_fn("hook")}  {_comment("// the shared thing")}'),
        (1, _str_("&quot;Saw you led the Redis migration.&quot;")),
        (0, "&nbsp;"),
        (0, f'{_kw("2.")} {_fn("proof")} {_comment("// why you, in one line")}'),
        (1, _str_("&quot;I rebuilt our uni society&#39;s booking&quot;")),
        (1, _str_("&quot;system on the same stack.&quot;")),
        (0, "&nbsp;"),
        (0, f'{_kw("3.")} {_fn("ask")}   {_comment("// one question, easy yes")}'),
        (1, _str_("&quot;Was the caching layer the hard part?&quot;")),
        (0, "&nbsp;"),
        (0, f'{_kw("4.")} {_fn("exit")}  {_comment("// zero pressure")}'),
        (1, _str_("&quot;No worries if you&#39;re heads-down.&quot;")),
    ])
    inner = f"""
<div style="padding:36px 50px 0 50px;position:relative;z-index:5;flex-shrink:0;">
  <div style="font-family:{MONO};font-size:19px;color:{TERM_GREEN};letter-spacing:2px;
               text-transform:uppercase;margin-bottom:14px;">&gt; cat anatomy.txt</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Four parts. <span style="color:{TERM_GREEN};font-style:italic;">Ninety words.</span>
  </div>
</div>
<div style="flex:1;padding:28px 30px 0 0;position:relative;z-index:5;overflow:hidden;">{lines}</div>
"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body>{_shell(inner, "anatomy.txt", 3)}</body></html>"""
    _render(html, out)


# ─── Slide 4: Real message diff (bad vs good) ──────────────────────────────
def _slide4(out):
    f = _fonts()
    bad = [
        "Hi! I'm a final year student and I'd love",
        "to connect and learn more about your",
        "company. I'm very passionate about tech",
        "and would appreciate any opportunities.",
        "Please let me know. Thanks!",
    ]
    good = [
        "Hi Sarah - saw your talk on scaling the",
        "payments API. I built a smaller version",
        "for my uni society (Stripe + Postgres,",
        "~2k txns). Was rate-limiting the bit that",
        "bit you too? Happy to be ignored if busy.",
    ]
    def diff_block(rows, symbol, color, bg):
        r = ""
        for line in rows:
            r += (f'<div style="display:flex;gap:14px;padding:5px 18px;background:{bg};">'
                  f'<span style="font-family:{MONO};font-size:24px;color:{color};font-weight:700;'
                  f'flex-shrink:0;width:16px;">{symbol}</span>'
                  f'<span style="font-family:{MONO};font-size:24px;color:#C8D8E8;line-height:1.5;">{line}</span></div>')
        return r
    inner = f"""
<div style="padding:36px 50px 0 50px;position:relative;z-index:5;flex-shrink:0;">
  <div style="font-family:{MONO};font-size:19px;color:{TERM_GREEN};letter-spacing:2px;
               text-transform:uppercase;margin-bottom:14px;">&gt; git diff message.txt</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Same student. <span style="color:{TERM_GREEN};font-style:italic;">Different reply.</span>
  </div>
</div>
<div style="flex:1;padding:30px 50px 44px 50px;display:flex;flex-direction:column;gap:24px;
             position:relative;z-index:5;">
  <div style="background:{IDE_PANEL};border:2px solid rgba(255,107,157,0.35);border-radius:10px;
               overflow:hidden;">
    <div style="background:rgba(255,107,157,0.14);padding:12px 18px;font-family:{MONO};
                 font-size:20px;color:{TERM_PINK};font-weight:700;letter-spacing:1px;">
      - BEFORE &nbsp;&middot;&nbsp; 0 replies from 40 sent
    </div>
    <div style="padding:10px 0;">{diff_block(bad, "-", TERM_PINK, "rgba(255,107,157,0.06)")}</div>
  </div>
  <div style="background:{IDE_PANEL};border:2px solid rgba(127,219,182,0.4);border-radius:10px;
               overflow:hidden;">
    <div style="background:rgba(127,219,182,0.14);padding:12px 18px;font-family:{MONO};
                 font-size:20px;color:{TERM_GREEN};font-weight:700;letter-spacing:1px;">
      + AFTER &nbsp;&middot;&nbsp; 11 replies from 40 sent
    </div>
    <div style="padding:10px 0;">{diff_block(good, "+", TERM_GREEN, "rgba(127,219,182,0.06)")}</div>
  </div>
</div>
"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body>{_shell(inner, "message.txt", 4)}</body></html>"""
    _render(html, out)


# ─── Slide 5: Finding who to message ───────────────────────────────────────
def _slide5(out):
    f = _fonts()
    steps = [
        ("alumni", "Search LinkedIn: your uni + target company. Same-uni DMs reply at 3x the rate."),
        ("authors", "Find whoever wrote their engineering blog or spoke at a meetup. They like talking about it."),
        ("hiring_mgr", "Not the recruiter. The person whose team has the gap. Title on the job spec is the clue."),
        ("recent_joiners", "Someone who started 3 months ago remembers being you. Highest empathy, fastest reply."),
    ]
    rows = ""
    for i, (key, desc) in enumerate(steps):
        rows += f"""<div style="display:flex;gap:20px;background:{IDE_PANEL};
             border:2px solid rgba(255,255,255,0.08);border-left:5px solid {TERM_CYAN};
             border-radius:10px;padding:22px 26px;">
  <div style="font-family:{MONO};font-size:24px;color:{TERM_GREY};flex-shrink:0;
               padding-top:2px;">0{i+1}</div>
  <div style="flex:1;">
    <div style="font-family:{MONO};font-size:26px;color:{TERM_CYAN};font-weight:700;">
      targets.{key}
    </div>
    <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#A8C0D4;
                 margin-top:8px;line-height:1.4;">{desc}</div>
  </div>
</div>"""
    inner = f"""
<div style="padding:36px 50px 0 50px;position:relative;z-index:5;flex-shrink:0;">
  <div style="font-family:{MONO};font-size:19px;color:{TERM_GREEN};letter-spacing:2px;
               text-transform:uppercase;margin-bottom:14px;">&gt; ls targets/</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Message the <span style="color:{TERM_GREEN};font-style:italic;">right human.</span>
  </div>
</div>
<div style="flex:1;padding:30px 50px 44px 50px;display:flex;flex-direction:column;gap:16px;
             justify-content:center;position:relative;z-index:5;">{rows}</div>
"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body>{_shell(inner, "targets/", 5)}</body></html>"""
    _render(html, out)


# ─── Slide 6: Errors / what breaks it ──────────────────────────────────────
def _slide6(out):
    f = _fonts()
    errors = [
        ("ERR_NO_RESEARCH",  "Nothing specific to them. Instantly reads as a mass send."),
        ("ERR_ASK_TOO_BIG",  "'Can I pick your brain for 30 mins?' Too expensive to say yes."),
        ("ERR_WALL_OF_TEXT", "Over 90 words. They're on a phone between meetings. It gets archived."),
        ("ERR_NO_EXIT",      "No graceful out. Pressure kills replies. Give them permission to ignore you."),
    ]
    rows = ""
    for code, desc in errors:
        rows += f"""<div style="background:{IDE_PANEL};border:2px solid rgba(255,107,157,0.3);
             border-radius:10px;padding:22px 26px;">
  <div style="display:flex;align-items:center;gap:12px;">
    <div style="width:22px;height:22px;border-radius:50%;background:{TERM_PINK};
                 display:flex;align-items:center;justify-content:center;font-family:{MONO};
                 font-size:15px;font-weight:700;color:{IDE_BG};flex-shrink:0;">&times;</div>
    <div style="font-family:{MONO};font-size:24px;color:{TERM_PINK};font-weight:700;">{code}</div>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:26px;color:#A8C0D4;
               margin-top:10px;line-height:1.4;">{desc}</div>
</div>"""
    inner = f"""
<div style="padding:36px 50px 0 50px;position:relative;z-index:5;flex-shrink:0;">
  <div style="font-family:{MONO};font-size:19px;color:{TERM_PINK};letter-spacing:2px;
               text-transform:uppercase;margin-bottom:14px;">&gt; 4 errors, 0 warnings</div>
  <div style="font-family:Inter;font-weight:700;font-size:56px;line-height:1.0;color:white;
               letter-spacing:-2px;word-break:keep-all;hyphens:none;">
    Why yours got <span style="color:{TERM_PINK};font-style:italic;">ignored.</span>
  </div>
</div>
<div style="flex:1;padding:30px 50px 44px 50px;display:grid;grid-template-columns:1fr 1fr;
             gap:18px;align-content:center;position:relative;z-index:5;">{rows}</div>
"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body>{_shell(inner, "console", 6)}</body></html>"""
    _render(html, out)


# ─── Slide 7: CTA — build success output ───────────────────────────────────
def _slide7(out):
    f = _fonts()
    checks = [
        "Pick 5 people. Alumni first.",
        "Find one specific thing about each.",
        "Write 90 words. Ask one question.",
        "Send. Then forget about it.",
    ]
    rows = ""
    for c in checks:
        rows += (f'<div style="display:flex;gap:14px;align-items:center;padding:8px 0;">'
                 f'<span style="font-family:{MONO};font-size:26px;color:{TERM_GREEN};font-weight:700;">&check;</span>'
                 f'<span style="font-family:DM Sans,sans-serif;font-weight:500;font-size:28px;color:#C8D8E8;">{c}</span></div>')
    inner = f"""
<div style="flex:1;padding:44px 50px;display:flex;flex-direction:column;position:relative;z-index:5;">
  <div style="font-family:{MONO};font-size:19px;color:{TERM_GREEN};letter-spacing:2px;
               text-transform:uppercase;margin-bottom:14px;">&gt; npm run outreach</div>
  <div style="font-family:Inter;font-weight:700;font-size:74px;line-height:0.98;color:white;
               letter-spacing:-3px;word-break:keep-all;hyphens:none;">
    Build passed.<br><span style="color:{TERM_GREEN};font-style:italic;">Ship it.</span>
  </div>
  <div style="background:{IDE_PANEL};border:2px solid rgba(127,219,182,0.35);border-radius:10px;
               padding:28px 32px;margin-top:34px;">
    <div style="font-family:{MONO};font-size:20px;color:{TERM_GREEN};letter-spacing:1px;
                 margin-bottom:18px;font-weight:700;">&#10003; 4 checks passed in 30s</div>
    {rows}
  </div>
  <div style="flex:1;"></div>
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div style="display:inline-flex;align-items:center;gap:12px;background:{TERM_GREEN};
                 color:{IDE_BG};padding:18px 32px;border-radius:8px;font-family:{MONO};
                 font-weight:700;font-size:24px;">
      internwise.co.uk &rarr;
    </div>
    <img src="data:image/png;base64,{LOGO_W}" style="height:48px;opacity:0.6;">
  </div>
</div>
"""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{_base_css(f)}</style></head><body>{_shell(inner, "build", 7)}</body></html>"""
    _render(html, out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Cold DMs (Week 8, Day 1)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("terminal_ide_monospace_syntax", "week8/d1-colddm", "week8")
    print("Done - cold DMs complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week8/d1-colddm")
