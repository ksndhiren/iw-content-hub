"""
Internwise - Graduate Scheme Timeline (Week 10, Day 5)
Design language: AIRPORT DEPARTURE BOARD / BOARDING PASS. Split-flap board,
mono type, boarding-pass tickets with perforated stubs, gate/time rows.
7 slides. Accent: departures AMBER on board-black + boarding-pass teal.
"""
import os, base64, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup import register_design
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
BRANDING_DIR = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__)))), "branding")
FONTS_DIR    = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__)))), "assets", "fonts")

BOARD    = "#0C0F14"
BOARD2   = "#161B22"
AMBER    = "#FFB120"
FLAP     = "#1C222B"
TEAL     = "#1FB8A6"
TEAL_D   = "#137F72"
PASS_BG  = "#F4EEE0"
INK      = "#14202B"
GREEN    = "#3FD07A"

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

MONO = "'DM Mono','Courier New',ui-monospace,monospace"

def _base_css(f):
    return f"""{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;background:{BOARD};}}
.c{{width:1080px;height:1080px;position:relative;padding:60px 64px;display:flex;flex-direction:column;
    background:radial-gradient(ellipse at 50% 0%,{BOARD2} 0%,{BOARD} 70%);}}
.scan{{position:absolute;inset:0;pointer-events:none;z-index:2;
       background:repeating-linear-gradient(0deg,rgba(255,255,255,0.028) 0px,rgba(255,255,255,0.028) 1px,transparent 2px,transparent 4px);}}
"""

# split-flap char tile
def _flap(ch, col=AMBER):
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;min-width:44px;height:60px;'
            f'background:{FLAP};color:{col};font-family:{MONO};font-weight:700;font-size:40px;margin:0 3px;'
            f'border-radius:5px;box-shadow:inset 0 -2px 0 rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.06);'
            f'border-top:1px solid rgba(255,255,255,0.05);position:relative;">'
            f'<span style="position:absolute;top:50%;left:0;right:0;height:1px;background:rgba(0,0,0,0.55);"></span>{ch}</span>')

def _flap_word(word, col=AMBER):
    return '<div style="display:inline-flex;">' + "".join(_flap(c, col) for c in word) + '</div>'

def _kicker(t, col=TEAL):
    return (f'<div style="font-family:{MONO};font-weight:700;font-size:19px;color:{col};'
            f'letter-spacing:5px;text-transform:uppercase;">{t}</div>')

def _shell(inner, f):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{_base_css(f)}</style></head>
<body><div class="c">{inner}<div class="scan"></div></div></body></html>"""

def _board_header(right_label):
    return f"""<div style="display:flex;justify-content:space-between;align-items:center;flex-shrink:0;position:relative;z-index:5;">
  <img src="data:image/png;base64,{LOGO_W}" style="height:46px;">
  <div style="display:flex;align-items:center;gap:12px;font-family:{MONO};font-weight:700;font-size:18px;color:{AMBER};letter-spacing:3px;">
    <span style="width:11px;height:11px;border-radius:50%;background:{GREEN};box-shadow:0 0 10px {GREEN};"></span>{right_label}
  </div>
</div>"""

# departure row: time | destination | status
def _row(time, dest, status, status_col=GREEN, dim=False):
    op = "0.5" if dim else "1"
    return f"""<div style="display:flex;align-items:center;gap:20px;padding:16px 24px;background:{BOARD2};
       border-radius:10px;border:1px solid rgba(255,255,255,0.05);opacity:{op};">
  <div style="font-family:{MONO};font-weight:700;font-size:30px;color:{AMBER};min-width:130px;letter-spacing:1px;">{time}</div>
  <div style="flex:1;font-family:Inter;font-weight:700;font-size:27px;color:#EAF0F6;letter-spacing:-0.3px;">{dest}</div>
  <div style="font-family:{MONO};font-weight:700;font-size:17px;color:{status_col};letter-spacing:2px;
       border:1.5px solid {status_col};border-radius:6px;padding:5px 12px;text-transform:uppercase;">{status}</div>
</div>"""


def _slide1(out):
    f = _fonts()
    inner = f"""
{_board_header("DEPARTURES")}
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:5;">
  {_kicker("Graduate schemes / 2026-27")}
  <div style="margin-top:22px;">{_flap_word("BOARDING", AMBER)}</div>
  <div style="font-family:Inter;font-weight:700;font-size:82px;color:#EDF2F8;letter-spacing:-3px;line-height:0.98;margin-top:26px;word-break:keep-all;">
    Grad schemes<br>have a <span style="color:{AMBER};">gate time.</span>
  </div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:29px;color:#93A2B4;margin-top:24px;max-width:640px;line-height:1.4;">
    Miss the window and you wait a whole year. Here's the timeline to board on time.
  </div>
</div>
<div style="flex-shrink:0;display:flex;justify-content:space-between;align-items:center;position:relative;z-index:5;font-family:{MONO};font-weight:700;font-size:18px;color:{TEAL};letter-spacing:2px;">
  <span>GATE IW &middot; ON TIME</span><span style="color:{AMBER};">SWIPE &rarr;</span>
</div>
"""
    _render(_shell(inner, f), out)


def _slide2(out):
    f = _fonts()
    stats = [("70%","of grad schemes close applications before Christmas.", AMBER),
             ("4-6","months is a typical hiring cycle from apply to offer.", TEAL),
             ("1x","a year - most schemes open a single intake. Miss it, wait 12 months.", GREEN)]
    cards = ""
    for v,l,col in stats:
        cards += f"""<div style="flex:1;background:{BOARD2};border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:30px 24px;">
  <div style="font-family:{MONO};font-weight:700;font-size:58px;color:{col};letter-spacing:1px;">{v}</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:#C3CEDA;margin-top:16px;line-height:1.4;">{l}</div>
</div>"""
    inner = f"""
{_board_header("FLIGHT INFO")}
<div style="margin-top:40px;position:relative;z-index:5;">
  {_kicker("Why timing wins")}
  <div style="font-family:Inter;font-weight:700;font-size:56px;color:#EDF2F8;letter-spacing:-2px;margin-top:14px;line-height:1;">
    The clock is <span style="color:{AMBER};">already running.</span>
  </div>
</div>
<div style="flex:1;display:flex;gap:22px;align-items:center;position:relative;z-index:5;">{cards}</div>
<div style="flex-shrink:0;text-align:right;font-family:{MONO};font-weight:400;font-size:17px;color:#5C6B7A;position:relative;z-index:5;letter-spacing:1px;">
  SRC: ISE STUDENT RECRUITMENT SURVEY 2026, PROSPECTS
</div>
"""
    _render(_shell(inner, f), out)


def _timeline_slide(out, gate, title, rows_data, note):
    f = _fonts()
    rows = ""
    for t,d,s,c,dim in rows_data:
        rows += _row(t,d,s,c,dim) + '<div style="height:14px;"></div>'
    inner = f"""
{_board_header("GATE " + gate)}
<div style="margin-top:34px;position:relative;z-index:5;">
  {_kicker("Departure board")}
  <div style="font-family:Inter;font-weight:700;font-size:50px;color:#EDF2F8;letter-spacing:-1.5px;margin-top:12px;line-height:1.02;word-break:keep-all;">{title}</div>
</div>
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:5;">{rows}</div>
<div style="flex-shrink:0;background:{BOARD2};border-left:4px solid {AMBER};border-radius:8px;padding:18px 24px;position:relative;z-index:5;">
  <span style="font-family:{MONO};font-weight:700;font-size:16px;color:{AMBER};letter-spacing:2px;">TIP &middot; </span>
  <span style="font-family:'DM Sans';font-weight:600;font-size:24px;color:#D5DFEA;">{note}</span>
</div>
"""
    _render(_shell(inner, f), out)

def _slide3(out): _timeline_slide(out, "A1", "Summer &rarr; September:<br>get flight-ready.",
    [("JUN - AUG","Research schemes and build a target list","Boarding",GREEN,False),
     ("JUL - AUG","Draft your CV and a base cover letter","Boarding",GREEN,False),
     ("AUG - SEP","Practise online tests and psychometrics","On Time",TEAL,False),
     ("SEP","Set alerts - the big schemes start opening","Boarding",AMBER,False)],
    "Applications are often first-come - early birds clear assessment centres before slots fill.")

def _slide4(out): _timeline_slide(out, "B2", "September &rarr; December:<br>peak departures.",
    [("SEP - OCT","Most grad schemes open - apply early","Boarding Now",AMBER,False),
     ("OCT - NOV","Online tests and video interviews","Final Call",AMBER,False),
     ("NOV - DEC","Assessment centres and final rounds","Boarding",GREEN,False),
     ("DEC","Many schemes close - don't miss the gate","Last Call",TEAL,False)],
    "This is the rush. Applying in September beats applying in December for the same role.")

def _slide5(out): _timeline_slide(out, "C3", "January &rarr; Spring:<br>the second wave.",
    [("JAN - FEB","Offers roll out from autumn applicants","Departed",GREEN,True),
     ("JAN - MAR","Later schemes and rolling intakes open","Boarding",AMBER,False),
     ("FEB - APR","SME and startup grad roles pick up","On Time",TEAL,False),
     ("SPRING","Summer internships open for next year","Boarding",GREEN,False)],
    "Missed autumn? Rolling and spring intakes are your second boarding call - not a dead end.")

def _slide6(out):
    f = _fonts()
    # boarding pass ticket
    bars = "".join(f'<div style="height:8px;background:{INK};width:{w}%;"></div>' for w in [100,60,90,40,80,100,55,75])
    def _field(label, value, col="#14202B"):
        return f"""<div>
  <div style="font-family:{MONO};font-weight:700;font-size:14px;color:{TEAL_D};letter-spacing:2px;text-transform:uppercase;">{label}</div>
  <div style="font-family:Inter;font-weight:700;font-size:26px;color:{col};margin-top:4px;letter-spacing:-0.3px;">{value}</div>
</div>"""
    inner = f"""
{_board_header("BOARDING PASS")}
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:5;">
  {_kicker("Your ticket")}
  <div style="font-family:Inter;font-weight:700;font-size:46px;color:#EDF2F8;letter-spacing:-1.5px;margin:14px 0 26px;line-height:1;">
    Don&#39;t board <span style="color:{AMBER};">unprepared.</span>
  </div>
  <div style="display:flex;background:{PASS_BG};border-radius:16px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.5);">
    <div style="flex:1;padding:32px 34px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;border-bottom:2px dashed #C7BCA5;padding-bottom:20px;">
        {_field("Passenger","Future Grad")}
        {_field("Gate","IW-01", AMBER if False else "#14202B")}
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:22px;">
        {_field("From","Application")}
        <div style="display:flex;align-items:center;color:{TEAL};font-size:26px;">&#9992;</div>
        {_field("To","Offer")}
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:22px;">
        {_field("Board by","Sept - Oct")}
        {_field("Seat","Yours")}
        {_field("Status","On Time", TEAL_D)}
      </div>
    </div>
    <div style="width:200px;background:{TEAL};padding:28px 20px;display:flex;flex-direction:column;
         justify-content:space-between;border-left:3px dashed {PASS_BG};">
      <div style="font-family:{MONO};font-weight:700;font-size:15px;color:#EAFBF7;letter-spacing:2px;">BOARDING</div>
      <div style="display:flex;flex-direction:column;gap:5px;">
        {bars}
      </div>
      <div style="font-family:{MONO};font-weight:700;font-size:22px;color:#EAFBF7;letter-spacing:1px;">IW &middot; 2026</div>
    </div>
  </div>
</div>
<div style="flex-shrink:0;text-align:center;font-family:{MONO};font-weight:700;font-size:17px;color:{TEAL};letter-spacing:3px;position:relative;z-index:5;">
  PREP CV &middot; TESTS &middot; STAR STORIES &middot; QUESTIONS
</div>
"""
    _render(_shell(inner, f), out)


def _slide7(out):
    f = _fonts()
    checks = [("Build your target list now","JUN - AUG"),
              ("CV and tests ready by September","AUG - SEP"),
              ("Apply as schemes open","SEP - OCT"),
              ("Rolling intakes if you miss the rush","JAN - SPR")]
    rows = ""
    for c,t in checks:
        rows += f"""<div style="display:flex;align-items:center;gap:18px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.07);">
  <span style="color:{GREEN};font-size:24px;">&#10003;</span>
  <span style="flex:1;font-family:Inter;font-weight:700;font-size:27px;color:#EAF0F6;">{c}</span>
  <span style="font-family:{MONO};font-weight:700;font-size:17px;color:{AMBER};letter-spacing:1px;">{t}</span>
</div>"""
    inner = f"""
{_board_header("FINAL CALL")}
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;position:relative;z-index:5;">
  {_kicker("Now boarding")}
  <div style="font-family:Inter;font-weight:700;font-size:64px;color:#EDF2F8;letter-spacing:-2.5px;line-height:0.96;margin:14px 0 28px;word-break:keep-all;">
    Your seat is<br><span style="color:{AMBER};">waiting.</span>
  </div>
  <div style="background:{BOARD2};border-radius:14px;padding:10px 30px;border:1px solid rgba(255,255,255,0.06);">
    {rows}
  </div>
</div>
<div style="flex-shrink:0;position:relative;z-index:5;">
  <div style="display:inline-flex;align-items:center;gap:12px;background:{AMBER};color:{BOARD};
       padding:18px 34px;border-radius:50px;font-family:Inter;font-weight:700;font-size:26px;">
    Find grad roles at internwise.co.uk &rarr;
  </div>
</div>
"""
    _render(_shell(inner, f), out)


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating Grad Timeline (Week 10, Day 5)...")
    _load_logos()
    _slide1(os.path.join(campaign_dir, "slide_1.png"))
    _slide2(os.path.join(campaign_dir, "slide_2.png"))
    _slide3(os.path.join(campaign_dir, "slide_3.png"))
    _slide4(os.path.join(campaign_dir, "slide_4.png"))
    _slide5(os.path.join(campaign_dir, "slide_5.png"))
    _slide6(os.path.join(campaign_dir, "slide_6.png"))
    _slide7(os.path.join(campaign_dir, "slide_7.png"))
    register_design("departure_board_boarding_pass", "week10/d5-gradtimeline", "week10")
    print("Done - grad timeline complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week10/d5-gradtimeline")
