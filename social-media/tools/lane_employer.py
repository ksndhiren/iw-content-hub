"""Employer lane (B2B) - a LIBRARY of distinct Nuno-led layouts.
Verified Internwise benefits only (no pricing claims). Worlds rotate palette,
device and Nuno pose. Worlds: benefits, bigstat, process, trust, statement.

    render_employer(angle, world, out_dir, "slide_1.png")
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import nuno_ledger

# Layout-safe pose candidates per world (professional / compact, no wide left
# reach that would collide with the left copy column). The ledger picks the
# freshest each week; the world keeps its own `right` offset below.
EMP_POOLS = {
    "benefits":  ["nuno_authority_1", "nuno_authority_2", "nuno_authority_3", "nuno_thoughtful_1", "nuno_planning_1"],
    "bigstat":   ["nuno_authority_3", "nuno_authority_1", "nuno_authority_2", "nuno_offers_3", "nuno_planning_1"],
    "process":   ["nuno_planning_1", "nuno_planning_2", "nuno_planning_3"],
    "trust":     ["nuno_authority_2", "nuno_authority_1", "nuno_authority_3", "nuno_thoughtful_1"],
    "statement": ["nuno_cvpile"],
    # B2B: the founder should read confident/presenting to employers - authority poses.
    "kpi":       ["nuno_authority_1", "nuno_authority_4", "nuno_authority_2", "nuno_authority_3"],
    "cards":     ["nuno_authority_3", "nuno_authority_4", "nuno_authority_1", "nuno_authority_2"],
    "pipeline":  ["nuno_planning_2", "nuno_planning_3", "nuno_authority_4"],
    "proofboard": ["nuno_authority_4", "nuno_authority_2", "nuno_planning_2"],
    "command":   ["nuno_planning_2", "nuno_planning_3", "nuno_authority_4"],
    "talentmap": ["nuno_authority_1", "nuno_authority_2", "nuno_authority_4"],
    "goodcompany": ["nuno_authority_4", "nuno_thoughtful_1", "nuno_authority_3"],
    "fastmatch": ["nuno_cvpile", "nuno_authority_1", "nuno_authority_4"],
}

NAVY, DEEP, INK = L.NAVY, L.DEEP, L.INK
AMBER, CORAL = L.AMBER, L.CORAL
GREEN = "#5B9291"          # IW UK teal — employer accent (replaces off-brand mint)
BG1, BG2 = "#12213f", "#0A1830"   # IW UK navy background pair (all employer worlds)
EMP_URL = "internwise.co.uk/employers"


def _bg(c1, c2):
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(150deg,{c1},{c2});'></div>"
            f"<div style='position:absolute;inset:0;background-image:"
            f"linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),"
            f"linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:60px 60px;'></div>")

def _nuno(pose, h=800, right=-40):
    src = L.nuno_src(pose)
    arc = (f"<div style='position:absolute;z-index:4;right:-70px;bottom:-40px;width:760px;height:760px;border-radius:50%;"
           f"background:radial-gradient(circle at 50% 45%,{AMBER}2e,{AMBER}00 66%);'></div>")
    ground = (f"<div style='position:absolute;z-index:5;right:150px;bottom:34px;width:520px;height:70px;border-radius:50%;"
              f"background:radial-gradient(ellipse,rgba(0,0,0,.5),rgba(0,0,0,0) 70%);'></div>")
    img = f"<img src='{src}' style='position:absolute;z-index:30;right:{right}px;bottom:0;height:{h}px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.5));'>"
    return arc + ground + img

def _tag():
    return (f"<div style='position:absolute;left:58px;top:172px;display:inline-flex;align-items:center;gap:10px;"
            f"height:46px;padding:0 20px;border-radius:23px;background:{GREEN}1f;border:1.5px solid {GREEN}80;'>"
            f"{L.svg('briefcase',GREEN,22)}<span style=\"font-family:Inter;font-weight:700;font-size:19px;color:{INK};letter-spacing:2px;\">FOR EMPLOYERS</span></div>")

def _cta(text):
    # IW UK yellow button with navy text
    return (f"<div style='position:absolute;left:58px;bottom:120px;display:inline-flex;align-items:center;gap:14px;"
            f"height:66px;padding:0 32px;border-radius:33px;background:{AMBER};'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:26px;color:{DEEP};\">{text}</span>"
            f"<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.8' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h14M13 6l6 6-6 6'/></svg></div>")

def _cta_line(text, left=58, bottom=208, width=560):
    return (f"<div style='position:absolute;z-index:40;left:{left}px;bottom:{bottom}px;width:{width}px;'>"
            f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:25px;line-height:1.18;color:{INK};\">{text}</div>"
            f"<div style='margin-top:12px;width:210px;height:12px;border-radius:6px;background:{AMBER};'></div></div>")

def _sectorchips(items):
    chips = ""
    for i, s in enumerate(items):
        pop = i % 4 == 1
        col = DEEP if pop else INK
        bg = f"{AMBER}" if pop else f"{GREEN}1f"
        bd = "transparent" if pop else f"{GREEN}66"
        chips += (f"<span style=\"font-family:Inter;font-weight:700;font-size:24px;color:{col};background:{bg};"
                  f"border:1.5px solid {bd};border-radius:100px;padding:12px 24px;display:inline-block;margin:0 12px 14px 0;\">{s}</span>")
    return chips


# ---- benefits (approved sample) ----
def w_benefits(a, pose="nuno_authority_1"):
    SUBT="#9FC2C9"
    head = (f"<div style='position:absolute;left:58px;top:242px;width:580px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:60px;line-height:1.04;letter-spacing:-1.5px;color:{INK};word-break:keep-all;\">"
            f"Your next intern is <span style='color:{AMBER};'>already here.</span></div></div>")
    icons = ["users", "rocket", "clipboard"]
    rows = "".join(
        f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:22px;'>"
        f"<div style='flex:0 0 58px;width:58px;height:58px;border-radius:50%;border:2px solid {GREEN}88;background:{GREEN}14;"
        f"display:flex;align-items:center;justify-content:center;'>{L.svg(ic,GREEN,28)}</div>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:30px;color:{INK};letter-spacing:-.4px;line-height:1.12;\">{bn}</div></div>"
        for ic, bn in zip(icons, a["benefits"]))
    blist = f"<div style='position:absolute;left:58px;top:400px;width:600px;'>{rows}</div>"
    trust = (f"<div style='position:absolute;left:58px;top:690px;display:inline-flex;align-items:center;gap:12px;"
             f"height:52px;padding:0 24px;border-radius:26px;background:{GREEN}1f;border:1.5px solid {GREEN}55;'>"
             f"{L.svg('users',GREEN,24)}<span style=\"font-family:Inter;font-weight:700;font-size:22px;color:{INK};\">Trusted by 14,000+ UK employers</span></div>")
    return (_bg(BG1,BG2)+_nuno(pose, right=-150)+L.logo_tl()+head+blist+trust
            + _cta_line("Post the role. Shortlist faster. Meet your intern.", bottom=202)
            + _cta(a["cta"])+L.url_footer(color=SUBT, text=EMP_URL))

# ---- big stat ----
def w_bigstat(a, pose="nuno_authority_3"):
    SUBT="#9FB0C9"
    head = (f"<div style='position:absolute;left:58px;top:230px;width:560px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:44px;line-height:1.1;letter-spacing:-1px;color:{INK};\">Reach early-career talent</div></div>")
    stat = (f"<div style='position:absolute;left:58px;top:330px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:150px;line-height:.82;color:{AMBER};letter-spacing:-5px;\">400K</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:34px;color:{INK};margin-top:16px;\">UK students &amp;</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:34px;color:{INK};\">graduates</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:26px;color:{SUBT};margin-top:18px;\">14,000+ employers already hiring here</div></div>")
    return (_bg(BG1,BG2)+_nuno(pose, right=-150)+L.logo_tl()+head+stat
            + _cta_line("Turn reach into real applicants today.", bottom=210)
            + _cta(a["cta"])+L.url_footer(color=SUBT, text=EMP_URL))

# ---- process ----
def w_process(a, pose="nuno_planning_1"):
    SUBT="#9FB4B0"
    steps = [("Post your role in minutes"), ("Find candidates that fit"),
             ("Shortlist and interview"), ("Onboard and track progress")]
    head = (f"<div style='position:absolute;left:58px;top:230px;width:560px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:56px;line-height:1.04;letter-spacing:-1.5px;color:{INK};\">From role posted<br>to intern onboarded</div></div>")
    rows = ""
    for i, s in enumerate(steps, 1):
        rows += (f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:20px;'>"
                 f"<div style='flex:0 0 54px;width:54px;height:54px;border-radius:14px;background:{GREEN};display:flex;align-items:center;justify-content:center;'>"
                 f"<span style=\"font-family:Inter;font-weight:800;font-size:28px;color:#fff;\">{i}</span></div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:27px;color:{INK};letter-spacing:-.3px;line-height:1.15;\">{s}</span></div>")
    # Steps stay one line each in a column sized to the longest label, and Nuno
    # is pushed further off the right edge, so the longest step ("Onboard and
    # track progress") clears the figure instead of colliding with his shoulder.
    flow = f"<div style='position:absolute;z-index:2;left:58px;top:400px;width:548px;'>{rows}</div>"
    return (_bg(BG1,BG2)+L.logo_tl()+head+flow+_nuno(pose, right=-170)
            + _cta_line("Ready to hire? Register and post your role in minutes.", bottom=214)
            + _cta(a["cta"])+L.url_footer(left=58, color=SUBT, text=EMP_URL))

# ---- trust (logo wall) ----
def w_trust(a, pose="nuno_authority_2"):
    SUBT="#A9C7A9"
    head = (f"<div style='position:absolute;left:58px;top:236px;width:600px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:64px;line-height:1.02;letter-spacing:-1.5px;color:{INK};\"><span style='color:{AMBER};'>14,000+</span><br>UK employers<br>hire here.</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:28px;color:{SUBT};line-height:1.34;margin-top:22px;width:560px;\">From startups to household names, teams across every sector build their pipeline on Internwise.</div></div>")
    sectors = ["Finance","Marketing","Technology","Engineering","Healthcare","Media","Consulting","Design"]
    wall = (f"<div style='position:absolute;left:58px;top:640px;width:640px;'>{_sectorchips(sectors)}</div>")
    return _bg(BG1,BG2)+_nuno(pose)+L.logo_tl()+head+wall+_cta(a["cta"])+L.url_footer(color=SUBT, text=EMP_URL)

# ---- statement ----
def w_statement(a, pose="nuno_cvpile"):
    SUBT="#9FC2C9"
    head = (f"<div style='position:absolute;left:58px;top:280px;width:600px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:66px;line-height:1.06;letter-spacing:-1.5px;color:{INK};\">"
            f"Skip the CV pile. Go straight to the <span style='color:{AMBER};'>right candidate.</span></div>"
            f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:29px;color:{SUBT};line-height:1.34;margin-top:24px;\">Search candidates by sector, skills and location so you find the right fit, faster.</div></div>")
    return _bg(BG1,BG2)+_nuno(pose)+L.logo_tl()+head+_cta(a["cta"])+L.url_footer(color=SUBT, text=EMP_URL)


# ---- kpi strip (three tiles) ----
def w_kpi(a, pose="nuno_authority_1"):
    SUBT = "#9FC2C9"
    head = (f"<div style='position:absolute;left:58px;top:236px;width:560px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:56px;line-height:1.04;letter-spacing:-1.5px;color:{INK};word-break:keep-all;\">"
            f"One place to hire <span style='color:{AMBER};'>early-career talent.</span></div></div>")
    tiles = [("400K", "registered UK candidates"), ("14,000+", "employers hiring here"), ("Every", "sector, skill &amp; location")]
    cards = ""
    for i, (big, lab) in enumerate(tiles):
        cards += (f"<div style='flex:1;background:{GREEN}14;border:1.5px solid {GREEN}55;border-radius:22px;padding:30px 26px;'>"
                  f"<div style=\"font-family:Inter;font-weight:800;font-size:60px;line-height:.9;color:{AMBER};letter-spacing:-2px;\">{big}</div>"
                  f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:24px;color:{INK};margin-top:14px;line-height:1.2;\">{lab}</div></div>")
    strip = (f"<div style='position:absolute;left:58px;width:600px;top:420px;display:flex;gap:16px;'>{cards}</div>")
    return _bg(BG1, BG2) + _nuno(pose, right=-150) + L.logo_tl() + _tag() + head + strip + _cta(a["cta"]) + L.url_footer(color=SUBT, text=EMP_URL)

# ---- card grid (2x2 benefits) ----
def w_cards(a, pose="nuno_thoughtful_1"):
    SUBT = "#9FC2C9"
    head = (f"<div style='position:absolute;left:58px;top:236px;width:560px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:56px;line-height:1.04;letter-spacing:-1.5px;color:{INK};word-break:keep-all;\">Why teams hire with Internwise</div></div>")
    items = [("rocket", "Post a role in minutes"), ("search", "Search by sector, skills &amp; location"),
             ("clipboard", "Shortlist in one place"), ("users", "14,000+ employers already here")]
    cells = ""
    for ic, tx in items:
        cells += (f"<div style='background:{GREEN}14;border:1.5px solid {GREEN}55;border-radius:22px;padding:28px 26px;'>"
                  f"<div style='width:56px;height:56px;border-radius:14px;background:{GREEN};display:flex;align-items:center;justify-content:center;margin-bottom:18px;'>{L.svg(ic,'#fff',28)}</div>"
                  f"<div style=\"font-family:Inter;font-weight:700;font-size:27px;color:{INK};line-height:1.16;letter-spacing:-.3px;\">{tx}</div></div>")
    grid = (f"<div style='position:absolute;left:58px;top:382px;width:590px;display:grid;grid-template-columns:1fr 1fr;gap:16px;'>{cells}</div>")
    return (_bg(BG1, BG2) + _nuno(pose, right=-190) + L.logo_tl() + _tag() + head + grid
            + _cta_line("Keep the whole hiring journey in one place.", bottom=174)
            + _cta(a["cta"]) + L.url_footer(color=SUBT, text=EMP_URL))

# ---- pipeline timeline (editorial briefing) ----
def w_pipeline(a, pose="nuno_planning_2"):
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#6F6350"
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    rail = f"<div style='position:absolute;left:0;top:0;bottom:0;width:164px;background:{NAVYT};'></div>"
    logo = f"<img src='{L.ICONMARK}' style='position:absolute;left:50px;top:46px;width:64px;filter:brightness(0) invert(1);'>"
    tag = (f"<div style=\"position:absolute;left:218px;top:76px;font-family:'DM Sans';font-weight:800;font-size:20px;color:{COFFEE};letter-spacing:4px;\">HIRING PIPELINE</div>"
           f"<div style='position:absolute;left:218px;top:118px;width:72px;height:5px;background:{AMBER};border-radius:3px;'></div>")
    head = (f"<div style=\"position:absolute;left:218px;top:184px;width:470px;font-family:Georgia,serif;font-weight:700;font-size:64px;line-height:1.02;color:{NAVYT};\">"
            f"{a['headline']}</div>")
    steps = ["Role live", "Candidates arrive", "Shortlist fast", "Interview ready"]
    rows = ""
    for i, st in enumerate(steps, 1):
        rows += (f"<div style='display:flex;align-items:center;gap:18px;margin-bottom:22px;'>"
                 f"<div style='width:50px;height:50px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:22px;color:{NAVYT};'>{i}</div>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:31px;color:{NAVYT};letter-spacing:-.4px;\">{st}</div></div>")
    body = f"<div style='position:absolute;left:218px;top:470px;width:430px;'>{rows}</div>"
    nuno = _nuno(pose, h=700, right=-120)
    cta_line = (f"<div style='position:absolute;left:218px;bottom:178px;width:430px;'>"
                f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:25px;line-height:1.16;color:{NAVYT};\">Move from advert to interview without the admin pile.</div>"
                f"<div style='margin-top:12px;width:190px;height:12px;border-radius:6px;background:{AMBER};'></div></div>")
    cta = (f"<div style='position:absolute;left:218px;bottom:92px;height:64px;padding:0 30px;border-radius:32px;background:{NAVYT};display:flex;align-items:center;'>"
           f"<span style=\"font-family:Inter;font-weight:800;font-size:25px;color:#fff;\">{a['cta']}</span></div>")
    return bg + rail + logo + tag + head + body + nuno + cta_line + cta + L.url_footer(left=218, color=COFFEE, text=EMP_URL)

# ---- proof board (evidence led) ----
def w_proofboard(a, pose="nuno_authority_4"):
    SUBT = "#9FC2C9"
    bg = _bg(BG1, BG2)
    head = (f"<div style='position:absolute;left:58px;top:220px;width:560px;'>"
            f"<div style=\"font-family:Georgia,serif;font-weight:700;font-size:70px;line-height:1.02;color:{INK};\">Hire with proof, not guesswork.</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:27px;line-height:1.34;color:{SUBT};margin-top:22px;\">{a.get('body','Find early-career candidates by sector, skill and location.')}</div></div>")
    tiles = [("400K", "candidates"), ("14K+", "employers"), ("UK", "wide reach")]
    cards = ""
    for big, lab in tiles:
        cards += (f"<div style='background:rgba(255,255,255,.06);border:1.5px solid {GREEN}55;border-radius:8px;padding:24px 22px;'>"
                  f"<div style=\"font-family:Inter;font-weight:900;font-size:54px;color:{AMBER};letter-spacing:-2px;\">{big}</div>"
                  f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:22px;color:{INK};letter-spacing:1px;\">{lab}</div></div>")
    board = f"<div style='position:absolute;left:58px;top:590px;width:590px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;'>{cards}</div>"
    return (bg + _nuno(pose, h=760, right=-190) + L.logo_tl() + _tag() + head + board
            + _cta_line("Post once. Manage the whole shortlist from one place.", bottom=210)
            + _cta(a['cta']) + L.url_footer(color=SUBT, text=EMP_URL))


def w_command(a, pose="nuno_planning_2"):
    SUBT = "#9FC2C9"
    bg = _bg("#0A1830", "#102A4D")
    panel = (f"<div style='position:absolute;left:54px;top:178px;width:628px;height:644px;border-radius:22px;"
             f"background:rgba(255,255,255,.07);border:1.5px solid rgba(159,194,201,.32);"
             f"box-shadow:0 28px 70px rgba(0,0,0,.22);'></div>")
    label = (f"<div style=\"position:absolute;left:88px;top:218px;font-family:'DM Sans';font-weight:900;font-size:18px;"
             f"letter-spacing:4px;color:{AMBER};\">HIRING COMMAND CENTRE</div>")
    head = (f"<div style=\"position:absolute;left:88px;top:292px;width:520px;font-family:Inter;font-weight:900;"
            f"font-size:59px;line-height:1.02;letter-spacing:-1.8px;color:{INK};\">{a['headline']}</div>")
    rows = ""
    for i, item in enumerate(a.get("benefits", [])[:3], 1):
        rows += (f"<div style='height:68px;margin-bottom:16px;border-radius:12px;background:#fff;"
                 f"display:flex;align-items:center;gap:16px;padding:0 18px;box-shadow:0 14px 28px rgba(0,0,0,.14);'>"
                 f"<div style='width:34px;height:34px;border-radius:50%;background:{[AMBER,GREEN,CORAL][i-1]};"
                 f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:17px;color:{DEEP};'>{i}</div>"
                 f"<div style=\"font-family:Inter;font-weight:850;font-size:23px;line-height:1.08;color:{DEEP};\">{item}</div></div>")
    checklist = f"<div style='position:absolute;z-index:2;left:88px;top:548px;width:520px;'>{rows}</div>"
    status = (f"<div style='position:absolute;left:88px;top:752px;height:38px;padding:0 16px;border-radius:19px;"
              f"background:{GREEN};display:flex;align-items:center;font-family:'DM Sans';font-weight:900;font-size:16px;"
              f"letter-spacing:2px;color:#fff;'>READY TO SHORTLIST</div>")
    nuno = _nuno(pose, h=730, right=-150)
    return (bg + panel + L.logo_tl() + label + head + checklist + status + nuno
            + _cta_line("Keep every hiring step visible, simple and moving.", bottom=172)
            + _cta(a["cta"]) + L.url_footer(color=SUBT, text=EMP_URL))


def w_talentmap(a, pose="nuno_authority_1"):
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#6F6350"
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    map_shape = (f"<div style='position:absolute;right:42px;top:182px;width:430px;height:590px;border-radius:46% 54% 48% 52%;"
                 f"background:{NAVYT};box-shadow:0 18px 42px rgba(21,39,67,.18);'></div>"
                 f"<div style='position:absolute;right:150px;top:272px;width:240px;height:350px;border-radius:48% 52% 44% 56%;"
                 f"border:5px dashed rgba(255,255,255,.42);'></div>")
    pins = ""
    for x, y, col in [(730, 286, AMBER), (858, 386, GREEN), (780, 520, CORAL), (910, 650, AMBER)]:
        pins += f"<div style='position:absolute;left:{x}px;top:{y}px;width:26px;height:26px;border-radius:50%;background:{col};border:5px solid #fff;'></div>"
    label = (f"<div style=\"position:absolute;left:70px;top:188px;font-family:'DM Sans';font-weight:900;font-size:18px;"
             f"color:{GREEN};letter-spacing:5px;\">UK TALENT MAP</div>")
    head = (f"<div style=\"position:absolute;left:70px;top:250px;width:570px;font-family:Georgia,serif;font-weight:700;"
            f"font-size:72px;line-height:1.0;color:{NAVYT};\">{a['headline']}</div>")
    body = (f"<div style=\"position:absolute;left:74px;top:500px;width:500px;font-family:'DM Sans';font-weight:750;"
            f"font-size:29px;line-height:1.28;color:{COFFEE};\">{a.get('body','Reach early-career candidates across the UK.')}</div>")
    stat = (f"<div style='position:absolute;left:74px;top:660px;width:500px;display:flex;gap:18px;'>"
            f"<div style='width:210px;height:118px;background:#fff;border:3px solid {NAVYT};padding:18px 20px;'>"
            f"<div style=\"font-family:Inter;font-weight:950;font-size:44px;color:{AMBER};line-height:.9;\">400,000</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:17px;color:{NAVYT};margin-top:10px;letter-spacing:1px;\">CANDIDATES</div></div>"
            f"<div style='width:210px;height:118px;background:#fff;border:3px solid {NAVYT};padding:18px 20px;'>"
            f"<div style=\"font-family:Inter;font-weight:950;font-size:44px;color:{GREEN};line-height:.9;\">40+</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:17px;color:{NAVYT};margin-top:10px;letter-spacing:1px;\">SECTORS</div></div></div>")
    nuno = _nuno(pose, h=575, right=-96)
    cta = (f"<div style='position:absolute;left:74px;bottom:112px;height:64px;padding:0 30px;border-radius:32px;background:{NAVYT};"
           f"display:flex;align-items:center;font-family:Inter;font-weight:850;font-size:25px;color:#fff;'>{a['cta']}</div>")
    logo = f"<img src='{L.DARKLOGO}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"
    return bg + map_shape + pins + nuno + logo + label + head + body + stat + cta + L.url_footer(left=74, color=COFFEE, text=EMP_URL)


def w_goodcompany(a, pose="nuno_authority_4"):
    """Fresh trust proof page: badge wall + human presenter, avoiding the old sector-chip repeat."""
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#6F6350"
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    top = f"<div style='position:absolute;left:0;top:0;right:0;height:154px;background:{NAVYT};'></div>"
    logo = f"<img src='{L.WHT}' style='position:absolute;left:56px;top:42px;height:{L.LOGO}px;'>"
    label = (f"<div style=\"position:absolute;right:58px;top:58px;font-family:'DM Sans';font-weight:900;font-size:18px;"
             f"letter-spacing:4px;color:{AMBER};\">EMPLOYER PROOF</div>")
    head = (f"<div style=\"position:absolute;left:58px;top:214px;width:560px;font-family:Georgia,serif;font-weight:700;"
            f"font-size:76px;line-height:.98;color:{NAVYT};\">In good<br><span style='color:{GREEN};'>company.</span></div>")
    body = (f"<div style=\"position:absolute;left:62px;top:410px;width:500px;font-family:'DM Sans';font-weight:700;"
            f"font-size:29px;line-height:1.28;color:{COFFEE};\">{a.get('body','Teams across the UK use Internwise to find early-career talent.')}</div>")
    badges = ""
    sectors = ["Finance", "Tech", "Media", "Healthcare", "Design", "Consulting"]
    for i, sec in enumerate(sectors):
        x = 62 + (i % 2) * 230
        y = 560 + (i // 2) * 92
        badges += (f"<div style='position:absolute;left:{x}px;top:{y}px;width:200px;height:62px;background:#fff;"
                   f"border:3px solid {NAVYT};display:flex;align-items:center;gap:12px;padding:0 16px;"
                   f"box-shadow:8px 8px 0 rgba(21,39,67,.12);'>"
                   f"<span style='width:16px;height:16px;border-radius:50%;background:{[AMBER,GREEN,CORAL][i%3]};'></span>"
                   f"<span style=\"font-family:Inter;font-weight:950;font-size:22px;color:{NAVYT};\">{sec}</span></div>")
    stamp = (f"<div style='position:absolute;right:82px;top:224px;width:250px;height:250px;border-radius:50%;border:8px solid {AMBER};"
             f"display:flex;align-items:center;justify-content:center;transform:rotate(-8deg);'>"
             f"<div style=\"font-family:Inter;font-weight:950;font-size:52px;line-height:.9;text-align:center;color:{NAVYT};\">14K+<br><span style='font-size:22px;letter-spacing:2px;'>EMPLOYERS</span></div></div>")
    nuno = _nuno(pose, h=660, right=-150)
    cta_line = (f"<div style='position:absolute;left:62px;bottom:170px;width:520px;'>"
                f"<div style=\"font-family:'DM Sans';font-weight:950;font-size:27px;line-height:1.14;color:{NAVYT};\">Bring your role to the place employers already use.</div>"
                f"<div style='margin-top:12px;width:210px;height:12px;border-radius:6px;background:{AMBER};'></div></div>")
    cta = (f"<div style='position:absolute;left:62px;bottom:88px;height:62px;padding:0 28px;border-radius:31px;background:{NAVYT};display:flex;align-items:center;'>"
           f"<span style=\"font-family:Inter;font-weight:900;font-size:25px;color:#fff;\">{a['cta']}</span></div>")
    return bg + top + logo + label + stamp + nuno + head + body + badges + cta_line + cta + L.url_footer(left=62, color=COFFEE, text=EMP_URL)


def w_fastmatch(a, pose="nuno_cvpile"):
    """Fast-match employer page: search console, not the previous dark manifesto."""
    SUBT = "#9FC2C9"
    bg = _bg("#07172E", "#102A4D")
    logo = L.logo_tl()
    console = (f"<div style='position:absolute;left:52px;top:186px;width:642px;height:570px;border-radius:8px;"
               f"background:#F7F1E7;border:4px solid {AMBER};box-shadow:18px 18px 0 rgba(255,177,32,.18);'></div>"
               f"<div style='position:absolute;left:52px;top:186px;width:642px;height:72px;background:{AMBER};'></div>")
    dots = "".join(f"<span style='width:16px;height:16px;border-radius:50%;background:{c};display:inline-block;margin-right:10px;'></span>" for c in [CORAL, GREEN, NAVY])
    toolbar = f"<div style='position:absolute;left:82px;top:214px;'>{dots}</div>"
    head = (f"<div style=\"position:absolute;left:84px;top:306px;width:536px;font-family:Inter;font-weight:950;"
            f"font-size:62px;line-height:.98;letter-spacing:-2px;color:{DEEP};\">Skip the CV pile.<br><span style='color:{CORAL};'>Go straight</span> to the right candidate.</div>")
    rows = ""
    for i, txt in enumerate(["Sector fit", "Skills match", "Location ready"]):
        rows += (f"<div style='height:58px;margin-bottom:14px;border-radius:29px;background:#fff;border:2px solid {DEEP};"
                 f"display:flex;align-items:center;gap:14px;padding:0 18px;'>"
                 f"<div style='width:34px;height:34px;border-radius:50%;background:{[AMBER,GREEN,CORAL][i]};display:flex;align-items:center;justify-content:center;'>{L.svg('check',DEEP,20)}</div>"
                 f"<span style=\"font-family:Inter;font-weight:900;font-size:25px;color:{DEEP};\">{txt}</span></div>")
    filters = f"<div style='position:absolute;left:84px;top:558px;width:430px;'>{rows}</div>"
    nuno = _nuno(pose, h=650, right=-92)
    cta_line = _cta_line("Search with intent. Shortlist with confidence.", bottom=174, width=520)
    return bg + logo + console + toolbar + head + filters + nuno + cta_line + _cta(a["cta"]) + L.url_footer(color=SUBT, text=EMP_URL)


WORLDS = {"benefits": w_benefits, "bigstat": w_bigstat, "process": w_process,
          "trust": w_trust, "statement": w_statement,
          "kpi": w_kpi, "cards": w_cards,
          "pipeline": w_pipeline, "proofboard": w_proofboard,
          "command": w_command, "talentmap": w_talentmap,
          "goodcompany": w_goodcompany, "fastmatch": w_fastmatch}

def render_employer(angle, world, out_dir, filename="slide_1.png", week_id="adhoc"):
    pose = nuno_ledger.pick(EMP_POOLS.get(world, ["nuno_authority_1"]), week_id, label=f"employer/{world}")
    return L.render(out_dir, filename, WORLDS[world](angle, pose))


if __name__ == "__main__":
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    demo = [("benefits","e001"),("bigstat","e004"),("process","e003"),("trust","e005"),("statement","e002")]
    for world, aid in demo:
        render_employer(angles[aid], world, os.path.join(L.OUTROOT, "week14", "_etest", world))
