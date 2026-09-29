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
    img = f"<img src='{src}' style='position:absolute;z-index:8;right:{right}px;bottom:0;height:{h}px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.5));'>"
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
    return _bg(BG1,BG2)+_nuno(pose)+L.logo_tl()+head+blist+trust+_cta(a["cta"])+L.url_footer(color=SUBT, text=EMP_URL)

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
    return _bg(BG1,BG2)+_nuno(pose, right=-55)+L.logo_tl()+head+stat+_cta(a["cta"])+L.url_footer(color=SUBT, text=EMP_URL)

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
    flow = f"<div style='position:absolute;z-index:3;left:58px;top:400px;width:548px;'>{rows}</div>"
    return _bg(BG1,BG2)+L.logo_tl()+head+flow+_nuno(pose, right=-120)+_cta(a["cta"])+L.url_footer(left=58, color=SUBT, text=EMP_URL)

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
    grid = (f"<div style='position:absolute;left:58px;top:400px;width:590px;display:grid;grid-template-columns:1fr 1fr;gap:18px;'>{cells}</div>")
    return _bg(BG1, BG2) + _nuno(pose, right=-150) + L.logo_tl() + _tag() + head + grid + _cta(a["cta"]) + L.url_footer(color=SUBT, text=EMP_URL)

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
    cta = (f"<div style='position:absolute;left:218px;bottom:92px;height:64px;padding:0 30px;border-radius:32px;background:{NAVYT};display:flex;align-items:center;'>"
           f"<span style=\"font-family:Inter;font-weight:800;font-size:25px;color:#fff;\">{a['cta']}</span></div>")
    return bg + rail + logo + tag + head + body + nuno + cta + L.url_footer(left=218, color=COFFEE, text=EMP_URL)

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
    return bg + _nuno(pose, h=760, right=-130) + L.logo_tl() + _tag() + head + board + _cta(a['cta']) + L.url_footer(color=SUBT, text=EMP_URL)


WORLDS = {"benefits": w_benefits, "bigstat": w_bigstat, "process": w_process,
          "trust": w_trust, "statement": w_statement,
          "kpi": w_kpi, "cards": w_cards,
          "pipeline": w_pipeline, "proofboard": w_proofboard}

def render_employer(angle, world, out_dir, filename="slide_1.png", week_id="adhoc"):
    pose = nuno_ledger.pick(EMP_POOLS.get(world, ["nuno_authority_1"]), week_id, label=f"employer/{world}")
    return L.render(out_dir, filename, WORLDS[world](angle, pose))


if __name__ == "__main__":
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    demo = [("benefits","e001"),("bigstat","e004"),("process","e003"),("trust","e005"),("statement","e002")]
    for world, aid in demo:
        render_employer(angles[aid], world, os.path.join(L.OUTROOT, "week14", "_etest", world))
