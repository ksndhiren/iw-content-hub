"""Employer lane (B2B) - a LIBRARY of distinct Nuno-led layouts.
Verified Internwise benefits only (no pricing claims). Worlds rotate palette,
device and Nuno pose. Worlds: benefits, bigstat, process, trust, statement.

    render_employer(angle, world, out_dir, "slide_1.png")
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L

NAVY, DEEP, INK = L.NAVY, L.DEEP, L.INK
AMBER, CORAL, GREEN = L.AMBER, L.CORAL, L.GREEN
LOGOS = ["nike", "oracle", "o-1", "manutd"]


def _bg(c1, c2):
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(150deg,{c1},{c2});'></div>"
            f"<div style='position:absolute;inset:0;background-image:"
            f"linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),"
            f"linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:60px 60px;'></div>")

def _nuno(pose, h=800, right=-40):
    src = L.nuno_src(pose)
    arc = (f"<div style='position:absolute;right:-70px;bottom:-40px;width:760px;height:760px;border-radius:50%;"
           f"background:radial-gradient(circle at 50% 45%,{AMBER}2e,{AMBER}00 66%);'></div>")
    ground = (f"<div style='position:absolute;right:150px;bottom:34px;width:520px;height:70px;border-radius:50%;"
              f"background:radial-gradient(ellipse,rgba(0,0,0,.5),rgba(0,0,0,0) 70%);'></div>")
    img = f"<img src='{src}' style='position:absolute;right:{right}px;bottom:0;height:{h}px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.5));'>"
    return arc + ground + img

def _tag():
    return (f"<div style='position:absolute;left:58px;top:172px;display:inline-flex;align-items:center;gap:10px;"
            f"height:46px;padding:0 20px;border-radius:23px;background:{GREEN}1f;border:1.5px solid {GREEN}80;'>"
            f"{L.svg('briefcase',GREEN,22)}<span style=\"font-family:Inter;font-weight:700;font-size:19px;color:{INK};letter-spacing:2px;\">FOR EMPLOYERS</span></div>")

def _cta(text):
    return (f"<div style='position:absolute;left:58px;bottom:120px;display:inline-flex;align-items:center;gap:14px;"
            f"height:66px;padding:0 32px;border-radius:33px;background:{GREEN};'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:26px;color:{DEEP};\">{text}</span>"
            f"<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='2.8' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h14M13 6l6 6-6 6'/></svg></div>")

def _chip(name, w=132, h=66):
    src = L.img(os.path.join(L.BASE, "assets", "employer_logos", name+".png"))
    return (f"<div style='display:inline-flex;align-items:center;justify-content:center;height:{h}px;width:{w}px;"
            f"background:#FFFFFF;border-radius:12px;box-shadow:0 8px 20px rgba(0,0,0,.22);'>"
            f"<img src='{src}' style='max-width:{w-32}px;max-height:{h-22}px;object-fit:contain;'></div>")


# ---- benefits (approved sample) ----
def w_benefits(a):
    SUBT="#9FC2C9"
    head = (f"<div style='position:absolute;left:58px;top:242px;width:580px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:60px;line-height:1.04;letter-spacing:-1.5px;color:{INK};word-break:keep-all;\">"
            f"Your next intern is <span style='color:{GREEN};'>already here.</span></div></div>")
    icons = ["users", "rocket", "clipboard"]
    rows = "".join(
        f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:22px;'>"
        f"<div style='flex:0 0 58px;width:58px;height:58px;border-radius:50%;border:2px solid {GREEN}88;background:{GREEN}14;"
        f"display:flex;align-items:center;justify-content:center;'>{L.svg(ic,GREEN,28)}</div>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:30px;color:{INK};letter-spacing:-.4px;line-height:1.12;\">{bn}</div></div>"
        for ic, bn in zip(icons, a["benefits"]))
    blist = f"<div style='position:absolute;left:58px;top:400px;width:600px;'>{rows}</div>"
    trust = (f"<div style='position:absolute;left:58px;top:678px;'>"
             f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:19px;color:{SUBT};letter-spacing:2px;\">TRUSTED BY</div>"
             f"<div style='display:flex;gap:12px;margin-top:12px;'>{''.join(_chip(n) for n in LOGOS)}</div></div>")
    return _bg("#0B2B33","#0A1D24")+_nuno("nuno_authority_1")+L.logo_tl()+_tag()+head+blist+trust+_cta(a["cta"])+L.url_footer(color=SUBT)

# ---- big stat ----
def w_bigstat(a):
    SUBT="#9FB0C9"
    head = (f"<div style='position:absolute;left:58px;top:230px;width:560px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:44px;line-height:1.1;letter-spacing:-1px;color:{INK};\">Reach early-career talent</div></div>")
    stat = (f"<div style='position:absolute;left:58px;top:330px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:150px;line-height:.82;color:{AMBER};letter-spacing:-5px;\">398K+</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:34px;color:{INK};margin-top:16px;\">active candidates,</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:34px;color:{INK};\">ready to work</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:26px;color:{SUBT};margin-top:18px;\">14,000+ employers already hiring here</div></div>")
    return _bg("#12213f","#0A1830")+_nuno("nuno_authority_3", right=-55)+L.logo_tl()+_tag()+head+stat+_cta(a["cta"])+L.url_footer(color=SUBT)

# ---- process ----
def w_process(a):
    SUBT="#9FB4B0"
    steps = [("Post your role in minutes"), ("We surface pre-screened talent"),
             ("Shortlist and interview"), ("Onboard and track progress")]
    head = (f"<div style='position:absolute;left:58px;top:230px;width:560px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:56px;line-height:1.04;letter-spacing:-1.5px;color:{INK};\">From role posted<br>to intern onboarded</div></div>")
    rows = ""
    for i, s in enumerate(steps, 1):
        rows += (f"<div style='display:flex;gap:18px;align-items:center;margin-bottom:20px;'>"
                 f"<div style='flex:0 0 54px;width:54px;height:54px;border-radius:14px;background:{GREEN};display:flex;align-items:center;justify-content:center;'>"
                 f"<span style=\"font-family:Inter;font-weight:800;font-size:28px;color:{DEEP};\">{i}</span></div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:29px;color:{INK};letter-spacing:-.3px;\">{s}</span></div>")
    flow = f"<div style='position:absolute;left:58px;top:400px;width:600px;'>{rows}</div>"
    return _bg("#1c2433","#12161f")+_nuno("nuno_planning_1")+L.logo_tl()+_tag()+head+flow+_cta(a["cta"])+L.url_footer(color=SUBT)

# ---- trust (logo wall) ----
def w_trust(a):
    SUBT="#A9C7A9"
    head = (f"<div style='position:absolute;left:58px;top:240px;width:560px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:64px;line-height:1.02;letter-spacing:-1.5px;color:{INK};\">In good<br>company.</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:28px;color:{SUBT};line-height:1.34;margin-top:22px;\">From global brands to fast-growing teams, employers hire early talent on Internwise.</div></div>")
    grid = "".join(_chip(n, w=150, h=80) for n in LOGOS)
    wall = (f"<div style='position:absolute;left:58px;top:560px;width:640px;display:grid;grid-template-columns:1fr 1fr;gap:16px;'>{grid}</div>")
    return _bg("#123528","#0A1A14")+_nuno("nuno_authority_2")+L.logo_tl()+_tag()+head+wall+_cta(a["cta"])+L.url_footer(color=SUBT)

# ---- statement ----
def w_statement(a):
    SUBT="#9FC2C9"
    head = (f"<div style='position:absolute;left:58px;top:280px;width:600px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:66px;line-height:1.06;letter-spacing:-1.5px;color:{INK};\">"
            f"Skip the CV pile. Start with <span style='color:{GREEN};'>pre-screened</span> talent.</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:29px;color:{SUBT};line-height:1.34;margin-top:24px;\">We surface quality, ready-to-work candidates so you review the best, faster.</div></div>")
    return _bg("#0B2B33","#0A1D24")+_nuno("nuno_thoughtful_1")+L.logo_tl()+_tag()+head+_cta(a["cta"])+L.url_footer(color=SUBT)


WORLDS = {"benefits": w_benefits, "bigstat": w_bigstat, "process": w_process,
          "trust": w_trust, "statement": w_statement}

def render_employer(angle, world, out_dir, filename="slide_1.png"):
    return L.render(out_dir, filename, WORLDS[world](angle))


if __name__ == "__main__":
    angles = {a["id"]: a for a in L.load("employer_angles.json")["angles"]}
    demo = [("benefits","e001"),("bigstat","e004"),("process","e003"),("trust","e005"),("statement","e002")]
    for world, aid in demo:
        render_employer(angles[aid], world, os.path.join(L.OUTROOT, "week14", "_etest", world))
