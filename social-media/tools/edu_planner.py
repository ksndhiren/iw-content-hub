"""Hand-designed 'planner' education card (no Nuno): a ring-bound year planner
whose rows are month-by-month actions. Used for week26-fri-education.

  python tools/edu_planner.py <out.png>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L

NAVY, DEEP, AMBER, CORAL, GREEN = L.NAVY, L.DEEP, L.AMBER, L.CORAL, L.GREEN
PAPER = "#FBF6EC"
INK = "#14213D"

SPEC = {
    "eyebrow": "GRADUATE JOBS",
    "line1": "Plan your",
    "year": "2027",
    "line2": "job search now",
    "rows": [
        ("DEC", "Start networking early", CORAL),
        ("JAN", "Build one skill employers ask for", AMBER),
        ("FEB", "Research the roles you want", GREEN),
        ("MAR", "Tailor your CV for each role", "#6FA8FF"),
        ("APR", "Apply for internships", CORAL),
    ],
    "cta": "Start your 2027 plan today",
}


def card(spec):
    rings = "".join(
        f"<div style='position:absolute;top:-22px;left:{x}px;width:22px;height:46px;border-radius:11px;"
        f"background:linear-gradient(90deg,#9AA6B8,#E8EDF4 45%,#7C889A);box-shadow:0 2px 0 rgba(0,0,0,.25);'></div>"
        for x in range(70, 900, 96))
    rows = ""
    for i, (mon, text, col) in enumerate(spec["rows"]):
        rows += (f"<div style='display:flex;align-items:center;height:78px;border-top:2px dashed #E2D8C3;'>"
                 f"<div style='flex:none;width:88px;height:56px;border-radius:12px;background:{col};display:flex;"
                 f"align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:25px;"
                 f"letter-spacing:2px;color:{DEEP};'>{mon}</div>"
                 f"<div style=\"flex:1;margin-left:24px;font-family:Inter;font-weight:800;font-size:33px;"
                 f"letter-spacing:-.5px;color:{INK};\">{text}</div>"
                 f"<div style='flex:none;width:38px;height:38px;border-radius:9px;border:3px solid {INK};"
                 f"display:flex;align-items:center;justify-content:center;'>"
                 + (f"<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='{GREEN}' stroke-width='4' "
                    f"stroke-linecap='round' stroke-linejoin='round'><path d='M4 12l5 5L20 6'/></svg>" if i == 0 else "")
                 + "</div></div>")
    return (f"<div style='position:absolute;left:56px;top:428px;width:968px;height:500px;background:{PAPER};"
            f"border-radius:22px;box-shadow:14px 14px 0 rgba(0,0,0,.28);transform:rotate(-1.2deg);'>"
            f"{rings}"
            f"<div style='display:flex;justify-content:space-between;align-items:baseline;padding:40px 44px 14px;'>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:21px;letter-spacing:5px;color:#8A7C62;\">MY JOB SEARCH PLANNER</span>"
            f"<span style=\"font-family:Inter;font-weight:900;font-size:30px;color:{CORAL};letter-spacing:-.5px;\">{spec['year']}</span></div>"
            f"<div style='padding:0 44px;'>{rows}</div></div>")


def render(out):
    s = SPEC
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 85% 10%,#1C3A6B,{NAVY} 60%);'></div>"
          + L.dots("right:56px;top:300px;", w=200, h=96))
    ghost = (f"<div style=\"position:absolute;right:44px;top:22px;font-family:Inter;font-weight:900;font-size:180px;"
             f"letter-spacing:-10px;line-height:1;color:transparent;-webkit-text-stroke:3px rgba(255,177,32,.28);\">{s['year']}</div>")
    head = (f"<div style='position:absolute;left:56px;top:188px;'>"
            f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:22px;letter-spacing:5px;color:{AMBER};\">{s['eyebrow']}</div>"
            f"<div style=\"margin-top:14px;font-family:Inter;font-weight:900;font-size:70px;line-height:1.02;letter-spacing:-2.5px;color:#fff;\">"
            f"{s['line1']} <span style='color:{AMBER};'>{s['year']}</span><br>{s['line2']}</div></div>")
    foot = (f"<div style=\"position:absolute;left:56px;bottom:58px;font-family:Inter;font-weight:800;font-size:28px;color:#fff;\">{s['cta']}</div>"
            + L.url_pill(right=56, bottom=46))
    inner = bg + ghost + L.logo_tl() + head + card(s) + foot
    return L.render(os.path.dirname(os.path.abspath(out)), os.path.basename(out), inner)


if __name__ == "__main__":
    render(sys.argv[1])
