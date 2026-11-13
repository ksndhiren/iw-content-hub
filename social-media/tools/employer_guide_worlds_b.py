"""Second bank of employer guide design worlds (week 25+), so a lane week never
reuses last week's looks. Registered into employer_guide_worlds.WORLDS.

    transit    - a route map: one coloured line, numbered stations, window-framed photos
    swiss      - Swiss poster: electric blue blocks, huge numerals, duotone photos, hard rules
    blueprint  - technical drawing: blue paper, white grid, week ruler, dimension brackets
    kanban     - a whiteboard: sticky notes, magnets, marker writing
    ticket     - boarding passes: perforated stubs, departure times, window-shaped photos
"""
import lanes_common as L
import lane_employer_guide as E
import employer_guide_worlds as A

NAVY, DEEP, AMBER, CORAL = E.NAVY, E.DEEP, E.AMBER, E.CORAL
MONO = A.MONO
ab, pill, hi_wrap, check, photo = A.ab, A.pill, A.hi_wrap, A.check, E.photo


def logo(dark=True):
    return f"<img src='{L.DARKLOGO if dark else L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"


def icon(name, size, x, y, bg="#fff", border=None, extra=""):
    bd = f"border:{border};" if border else ""
    return (f"<div style='{ab(x, y, size, size)}border-radius:50%;background:{bg};{bd}display:flex;align-items:center;"
            f"justify-content:center;{extra}'><svg viewBox='0 0 200 200' width='{int(size * .78)}' height='{int(size * .78)}'>"
            f"{E.SPOTS[name]}</svg></div>")


# =====================================================================================
#  TRANSIT - the guide is a route; every step is a stop on one line
# =====================================================================================
T_BG, T_LINE, T_YEL, T_INK, T_MUT = "#F3F0E8", "#6C3BD1", "#FFC93C", "#16133A", "#6E6A86"


def _t_bg():
    return (f"<div style='position:absolute;inset:0;background:{T_BG};'></div>"
            f"<div style='position:absolute;inset:0;background-image:linear-gradient(rgba(22,19,58,.045) 2px,transparent 2px),"
            f"linear-gradient(90deg,rgba(22,19,58,.045) 2px,transparent 2px);background-size:90px 90px;'></div>")


def _t_station(x, y, label, on=False, done=False, size=56):
    fill = T_LINE if done else "#fff"
    ring = f"box-shadow:0 0 0 12px rgba(108,59,209,.18);" if on else ""
    tc = "#fff" if done else T_INK
    return (f"<div style='{ab(x - size // 2, y - size // 2, size, size)}border-radius:50%;background:{T_YEL if on else fill};"
            f"border:8px solid {T_INK if on else T_LINE};display:flex;align-items:center;justify-content:center;{ring}"
            f"box-sizing:border-box;font-family:Inter;font-weight:900;font-size:{int(size * .4)}px;color:{T_INK if on else tc};'>{label}</div>")


def _t_window(pid, x, y, w, h, r=46):
    return (f"<div style='{ab(x, y, w, h)}border-radius:{r}px;background:{T_INK};padding:14px;box-sizing:border-box;"
            f"box-shadow:0 24px 50px rgba(22,19,58,.25);'><div style='width:100%;height:100%;border-radius:{r - 12}px;"
            f"background:url({photo(pid)}) center/cover;'></div></div>")


def transit_cover(g):
    t = _t_bg() + logo()
    t += (f"<div style=\"position:absolute;right:56px;top:74px;padding:10px 20px;border-radius:30px;background:{T_LINE};"
          f"font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:4px;color:#fff;\">{g['kicker']}</div>")
    t += (f"<div style='{ab(56, 200, 600)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:88px;line-height:1;letter-spacing:-3px;color:{T_INK};\">{g['title_pre']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:108px;line-height:1.02;letter-spacing:-4px;color:{T_LINE};\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:88px;line-height:1;letter-spacing:-3px;color:{T_INK};\">{g['title_post']}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:32px;color:{T_MUT};margin-top:26px;\">{g['sub']}</div></div>")
    t += _t_window(g["cover_photo"], 690, 190, 334, 430)
    # the route: snake with numbered stations and stop names
    n = len(g["steps"])
    xs = [140, 400, 660, 920]
    pts = [(xs[0], 760), (xs[1], 760), (xs[2], 760), (xs[3], 760), (xs[3], 980), (xs[2], 980), (xs[1], 980), (xs[0], 980)][:n]
    path = f"M{pts[0][0]} {pts[0][1]}"
    for k in range(1, n):
        (x0, y0), (x1, y1) = pts[k - 1], pts[k]
        if y0 != y1:
            path += f" C{x0 + 110} {y0} {x1 + 110} {y1} {x1} {y1}"
        else:
            path += f" L{x1} {y1}"
    t += (f"<svg style='{ab(0, 0)}' width='1080' height='1350'><path d='{path}' fill='none' stroke='{T_LINE}' stroke-width='22' "
          f"stroke-linecap='round' stroke-linejoin='round'/></svg>")
    for k, (x, y) in enumerate(pts):
        t += _t_station(x, y, str(k + 1), on=(k == 0), size=64)
        t += (f"<div style=\"{ab(x - 120, y + 48, 240)}text-align:center;font-family:Inter;font-weight:800;font-size:24px;"
              f"line-height:1.15;color:{T_INK};\">{g['steps'][k]['title']}</div>")
    n_, lab = g["badge"]
    t += (f"<div style=\"{ab(56, 1120)}display:flex;align-items:center;gap:14px;font-family:'DM Sans';font-weight:800;"
          f"font-size:24px;letter-spacing:3px;color:{T_INK};\"><span style='width:48px;height:16px;border-radius:8px;background:{T_LINE};'></span>"
          f"{n_} {lab} TO YOUR NEXT HIRE</div>")
    return t + E.footer(g["cta_url"], ink=T_INK, swipe_ink=T_LINE)


def _t_line_bar(i, n, y=200):
    x0, x1 = 120, 960
    gap = (x1 - x0) / (n - 1)
    t = (f"<div style='{ab(x0, y - 9, x1 - x0, 18)}border-radius:9px;background:rgba(108,59,209,.22);'></div>"
         f"<div style='{ab(x0, y - 9, int(gap * i), 18)}border-radius:9px;background:{T_LINE};'></div>")
    for k in range(n):
        t += _t_station(int(x0 + gap * k), y, str(k + 1), on=(k == i), done=(k < i), size=72 if k == i else 52)
    return t


def transit_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    t = _t_bg() + logo()
    t += (f"<div style=\"position:absolute;right:56px;top:72px;font-family:'DM Sans';font-weight:800;font-size:22px;"
          f"letter-spacing:4px;color:{T_LINE};\">{g.get('unit', 'stop').upper()} {i + 1} OF {n}</div>")
    t += _t_line_bar(i, n, 214)
    t += (f"<div style=\"{ab(56, 300, 968)}font-family:Inter;font-weight:900;font-size:76px;line-height:1.02;letter-spacing:-2.6px;"
          f"color:{T_INK};\">{hi_wrap(s['title'], s.get('hi'), f'color:{T_LINE};')}</div>")
    t += _t_window(s["photo"], 56, 480, 440, 660, 54)
    t += icon(s["icon"], 150, 390, 1020, "#fff", f"6px solid {T_INK}")
    rows = "".join(f"<div style='display:flex;align-items:center;gap:18px;padding:26px 24px;margin-bottom:18px;border-radius:18px;"
                   f"background:{T_INK};'><span style='flex:none;width:20px;height:20px;border-radius:50%;background:{T_YEL};'></span>"
                   f"<span style=\"font-family:Inter;font-weight:700;font-size:29px;line-height:1.22;color:#fff;\">{p}</span></div>"
                   for p in s["points"])
    t += f"<div style='{ab(530, 480, 494)}'>{rows}</div>"
    t += (f"<div style='{ab(530, 960, 494, 180)}padding:24px 26px;border-radius:18px;background:{T_YEL};box-sizing:border-box;'>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:4px;color:{T_INK};\">TRAVEL TIP</div>"
          f"<div style=\"font-family:Inter;font-weight:700;font-size:26px;line-height:1.25;color:{T_INK};margin-top:6px;\">{s['tip']}</div></div>")
    return t + E.footer(g["cta_url"], ink=T_INK, swipe_ink=T_LINE)


def transit_cta(g):
    t = (f"<div style='position:absolute;inset:0;background:{T_INK};'></div>" + logo(False))
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), f"color:{T_YEL};")
    t += (f"<div style=\"{ab(56, 190, 968)}font-family:Inter;font-weight:900;font-size:82px;line-height:1.04;letter-spacing:-2.8px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 390, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:#B7B2D6;\">{g['cta_sub']}</div>")
    n = len(g["steps"])
    y0, gap = 500, 104
    t += f"<div style='{ab(108, y0, 18, gap * (n - 1))}border-radius:9px;background:{T_LINE};'></div>"
    for k, s in enumerate(g["steps"]):
        y = y0 + gap * k
        t += (f"<div style='{ab(89, y - 28, 56, 56)}border-radius:50%;background:#fff;border:8px solid {T_LINE};box-sizing:border-box;"
              f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:22px;color:{T_INK};'>{k + 1}</div>"
              f"<div style=\"{ab(176, y - 20)}font-family:Inter;font-weight:800;font-size:30px;color:#fff;\">{s['title']}</div>")
    t += _t_window(g["steps"][0]["photo"], 700, 520, 324, 420)
    return t + pill("Post your internship at", g["cta_url"], T_YEL, T_INK, y=1150, shadow=f"8px 8px 0 {T_LINE}")


# =====================================================================================
#  SWISS - international typographic poster: grid, rules, one loud blue
# =====================================================================================
S_BLUE, S_INK, S_BG, S_RED = "#2440F0", "#0B0B0F", "#F7F7F4", "#FF4B2B"


def _duo(pid, x, y, w, h):
    return (f"<div style='{ab(x, y, w, h)}background:{S_BLUE};overflow:hidden;'>"
            f"<div style='width:100%;height:100%;background:url({photo(pid)}) center/cover;filter:grayscale(1) contrast(1.15);"
            f"mix-blend-mode:multiply;opacity:.95;'></div></div>")


def _rule(x, y, w, c=S_INK, h=4):
    return f"<div style='{ab(x, y, w, h)}background:{c};'></div>"


def swiss_cover(g):
    t = f"<div style='position:absolute;inset:0;background:{S_BG};'></div>"
    t += f"<div style='{ab(0, 0, 1080, 760)}background:{S_BLUE};'></div>" + logo(False)
    t += (f"<div style=\"position:absolute;right:56px;top:76px;font-family:Inter;font-weight:800;font-size:20px;letter-spacing:3px;"
          f"color:#fff;\">{g['kicker']}</div>")
    t += _rule(56, 186, 968, "#fff", 4)
    t += (f"<div style='{ab(50, 214, 980)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:168px;line-height:.9;letter-spacing:-8px;color:#fff;\">{g['title_pre']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:168px;line-height:.9;letter-spacing:-8px;color:{S_INK};\">{g['title_hi']}</div></div>")
    t += (f"<div style=\"{ab(56, 600, 560)}font-family:Inter;font-weight:800;font-size:56px;line-height:1.02;letter-spacing:-2px;"
          f"color:#fff;\">{g['title_post']}</div>")
    t += _duo(g["cover_photo"], 600, 560, 424, 560)
    t += f"<div style='{ab(600, 560, 424, 560)}border:4px solid {S_INK};box-sizing:border-box;'></div>"
    n, lab = g["badge"]
    t += (f"<div style='{ab(56, 820)}'><div style=\"font-family:Inter;font-weight:900;font-size:220px;line-height:.8;letter-spacing:-10px;"
          f"color:{S_RED};\">{n}</div><div style=\"font-family:Inter;font-weight:900;font-size:30px;letter-spacing:6px;color:{S_INK};"
          f"margin-top:20px;\">{lab}</div></div>")
    t += _rule(56, 1090, 500)
    t += (f"<div style=\"{ab(56, 1106, 500)}font-family:Inter;font-weight:600;font-size:28px;line-height:1.25;color:{S_INK};\">{g['sub']}</div>")
    return t + E.footer(g["cta_url"], ink=S_INK, swipe_ink=S_BLUE)


def swiss_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    t = f"<div style='position:absolute;inset:0;background:{S_BG};'></div>" + logo()
    t += (f"<div style=\"position:absolute;right:56px;top:76px;font-family:Inter;font-weight:800;font-size:22px;letter-spacing:3px;"
          f"color:{S_INK};\">{g.get('unit', 'part').upper()} {i + 1} / {n}</div>")
    t += _rule(56, 186, 968)
    t += (f"<div style=\"{ab(44, 196)}font-family:Inter;font-weight:900;font-size:300px;line-height:.86;letter-spacing:-16px;"
          f"color:{S_BLUE};\">{i + 1:02d}</div>")
    t += (f"<div style=\"{ab(520, 214, 504)}font-family:Inter;font-weight:900;font-size:72px;line-height:1;letter-spacing:-3px;"
          f"color:{S_INK};\">{hi_wrap(s['title'], s.get('hi'), f'color:{S_RED};')}</div>")
    t += _duo(s["photo"], 56, 500, 440, 520)
    rows = "".join(f"<div style='border-top:4px solid {S_INK};padding:18px 0 26px;display:flex;gap:18px;'>"
                   f"<span style=\"flex:none;font-family:Inter;font-weight:900;font-size:26px;color:{S_BLUE};width:44px;\">{chr(97 + k)}.</span>"
                   f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;line-height:1.2;color:{S_INK};\">{p}</span></div>"
                   for k, p in enumerate(s["points"]))
    t += f"<div style='{ab(540, 500, 484)}'>{rows}</div>"
    t += (f"<div style='{ab(56, 1060, 968)}background:{S_INK};padding:26px 32px;box-sizing:border-box;display:flex;gap:24px;align-items:center;'>"
          f"<span style=\"flex:none;font-family:Inter;font-weight:900;font-size:22px;letter-spacing:4px;color:{S_BLUE};"
          f"background:#fff;padding:8px 14px;\">NOTE</span>"
          f"<span style=\"font-family:Inter;font-weight:700;font-size:27px;line-height:1.25;color:#fff;\">{s['tip']}</span></div>")
    return t + E.footer(g["cta_url"], ink=S_INK, swipe_ink=S_BLUE)


def swiss_cta(g):
    t = f"<div style='position:absolute;inset:0;background:{S_BLUE};'></div>" + logo(False)
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), f"color:{S_INK};")
    t += _rule(56, 186, 968, "#fff")
    t += (f"<div style=\"{ab(56, 210, 968)}font-family:Inter;font-weight:900;font-size:96px;line-height:.98;letter-spacing:-4px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 430, 900)}font-family:Inter;font-weight:600;font-size:30px;color:#fff;opacity:.85;\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='border-top:3px solid rgba(255,255,255,.9);padding:16px 0;display:flex;gap:22px;align-items:baseline;'>"
                   f"<span style=\"font-family:Inter;font-weight:900;font-size:30px;color:{S_INK};width:56px;\">{k + 1:02d}</span>"
                   f"<span style=\"font-family:Inter;font-weight:800;font-size:32px;color:#fff;\">{s['title']}</span></div>"
                   for k, s in enumerate(g["steps"]))
    t += f"<div style='{ab(56, 530, 600)}'>{rows}</div>"
    t += (f"<div style='{ab(700, 540, 324, 420)}background:{S_INK};overflow:hidden;'><div style='width:100%;height:100%;"
          f"background:url({photo(g['steps'][1]['photo'])}) center/cover;filter:grayscale(1) contrast(1.1);'></div></div>")
    return t + pill("Post your internship at", g["cta_url"], "#fff", S_INK, y=1150, shadow=f"8px 8px 0 {S_INK}")


# =====================================================================================
#  BLUEPRINT - the programme is a technical drawing
# =====================================================================================
B_BG, B_LINE, B_INK, B_MUT, B_HI = "#14467E", "rgba(255,255,255,.13)", "#F2F7FF", "#A9C3E6", "#FFC24A"


def _b_bg():
    return (f"<div style='position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#1D5A9C,{B_BG} 70%);'></div>"
            f"<div style='position:absolute;inset:0;background-image:linear-gradient({B_LINE} 1.5px,transparent 1.5px),"
            f"linear-gradient(90deg,{B_LINE} 1.5px,transparent 1.5px);background-size:30px 30px;'></div>"
            f"<div style='position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.18) 2px,transparent 2px),"
            f"linear-gradient(90deg,rgba(255,255,255,.18) 2px,transparent 2px);background-size:150px 150px;'></div>"
            f"<div style='{ab(24, 24, 1032, 1302)}border:3px solid rgba(255,255,255,.55);'></div>")


def _b_frame(pid, x, y, w, h):
    c = "".join(f"<div style='{ab(cx, cy, 34, 34)}border-{v}:5px solid {B_INK};border-{hz}:5px solid {B_INK};'></div>"
                for cx, cy, v, hz in [(x - 14, y - 14, 'top', 'left'), (x + w - 20, y - 14, 'top', 'right'),
                                      (x - 14, y + h - 20, 'bottom', 'left'), (x + w - 20, y + h - 20, 'bottom', 'right')])
    return (f"<div style='{ab(x, y, w, h)}background:{B_BG};overflow:hidden;'><div style='width:100%;height:100%;"
            f"background:url({photo(pid)}) center/cover;filter:grayscale(1) contrast(1.05) brightness(1.05);mix-blend-mode:luminosity;opacity:.9;'></div></div>"
            f"<div style='{ab(x, y, w, h)}background:rgba(20,70,126,.28);'></div>" + c)


def _b_weeks(g):
    """(start_week, end_week) per phase from the 'phase' labels, e.g. WEEKS 2-4."""
    out = []
    for s in g["steps"]:
        nums = [int(v) for v in s.get("phase", "").replace("WEEKS", "").replace("WEEK", "").strip().split("-") if v.strip().isdigit()]
        out.append((nums[0], nums[-1]) if nums else (1, 1))
    return out


def _b_ruler(g, x, y, w, hi=None, labels=False):
    total = 12
    cw = w / total
    t = f"<div style='{ab(x, y, w, 4)}background:{B_INK};'></div>"
    for k in range(total + 1):
        t += f"<div style='{ab(int(x + cw * k) - 2, y - 14, 4, 32)}background:{B_INK};'></div>"
    for k in range(total):
        t += (f"<div style=\"{ab(int(x + cw * k), y + 26, int(cw))}text-align:center;font-family:{MONO};font-weight:700;"
              f"font-size:22px;color:{B_MUT};\">{k + 1}</div>")
    for p, (a, b) in enumerate(_b_weeks(g)):
        on = hi is None or hi == p
        x0, x1 = int(x + cw * (a - 1)) + 6, int(x + cw * b) - 6
        col = B_HI if (hi == p) else (B_INK if hi is None else "rgba(242,247,255,.35)")
        t += (f"<div style='{ab(x0, y - 66, x1 - x0, 30)}border:4px solid {col};border-bottom:none;box-sizing:border-box;'></div>")
        if labels or hi == p:
            t += (f"<div style=\"{ab(x0, y - 106, max(x1 - x0, 60))}text-align:center;font-family:{MONO};font-weight:700;font-size:20px;"
                  f"color:{col};white-space:nowrap;\">{'P' + str(p + 1)}</div>")
        if on and hi == p:
            t += f"<div style='{ab(x0, y - 8, x1 - x0, 20)}background:{B_HI};opacity:.85;'></div>"
    return t


def blueprint_cover(g):
    t = _b_bg() + logo(False)
    t += (f"<div style=\"position:absolute;right:60px;top:78px;font-family:{MONO};font-weight:700;font-size:22px;letter-spacing:3px;"
          f"color:{B_INK};\">{g['kicker']}</div>")
    t += (f"<div style='{ab(60, 196, 600)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:64px;line-height:1.02;letter-spacing:-2px;color:{B_INK};\">{g['title_pre']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:150px;line-height:.96;letter-spacing:-6px;color:{B_HI};\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:88px;line-height:1;letter-spacing:-3px;color:{B_INK};\">{g['title_post']}</div>"
          f"<div style=\"font-family:{MONO};font-weight:700;font-size:28px;line-height:1.3;color:{B_MUT};margin-top:24px;width:560px;\">{g['sub']}</div></div>")
    t += _b_frame(g["cover_photo"], 700, 200, 320, 420)
    t += (f"<div style=\"{ab(700, 640, 320)}font-family:{MONO};font-weight:700;font-size:20px;color:{B_MUT};\">FIG. 1 - THE TEAM</div>")
    t += (f"<div style=\"{ab(60, 800)}font-family:{MONO};font-weight:700;font-size:22px;letter-spacing:4px;color:{B_INK};\">"
          f"PLAN VIEW · {len(g['steps'])} PHASES</div>")
    t += _b_ruler(g, 80, 960, 920, labels=True)
    # title block
    t += (f"<div style='{ab(560, 1060, 460, 120)}border:3px solid {B_INK};display:grid;grid-template-columns:1fr 1fr;'>"
          f"<div style=\"border-right:3px solid {B_INK};padding:14px 18px;font-family:{MONO};font-weight:700;font-size:18px;color:{B_MUT};\">"
          f"DURATION<div style=\"font-family:Inter;font-weight:900;font-size:40px;color:{B_INK};margin-top:4px;\">12 WKS</div></div>"
          f"<div style=\"padding:14px 18px;font-family:{MONO};font-weight:700;font-size:18px;color:{B_MUT};\">"
          f"PHASES<div style=\"font-family:Inter;font-weight:900;font-size:40px;color:{B_INK};margin-top:4px;\">{len(g['steps'])}</div></div></div>")
    return t + E.footer(g["cta_url"], ink=B_INK, swipe_ink=B_HI)


def blueprint_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    t = _b_bg() + logo(False)
    t += (f"<div style=\"position:absolute;right:60px;top:78px;font-family:{MONO};font-weight:700;font-size:24px;letter-spacing:3px;"
          f"color:{B_HI};\">PHASE {i + 1} / {n}</div>")
    t += _b_ruler(g, 80, 300, 920, hi=i)
    t += (f"<div style=\"{ab(60, 384)}font-family:{MONO};font-weight:700;font-size:26px;letter-spacing:4px;color:{B_HI};\">{s.get('phase', '')}</div>")
    title = s["title"].split(": ", 1)[-1]
    t += (f"<div style=\"{ab(60, 426, 960)}font-family:Inter;font-weight:900;font-size:84px;line-height:1;letter-spacing:-3px;"
          f"color:{B_INK};\">{title}</div>")
    t += _b_frame(s["photo"], 640, 560, 380, 440)
    t += icon(s["icon"], 132, 900, 920, B_INK, f"5px solid {B_HI}")
    rows = "".join(f"<div style='display:flex;gap:18px;align-items:flex-start;margin-bottom:30px;'>"
                   f"<span style=\"flex:none;width:46px;height:46px;border-radius:50%;border:3px solid {B_INK};display:flex;align-items:center;"
                   f"justify-content:center;font-family:{MONO};font-weight:700;font-size:22px;color:{B_INK};\">{k + 1}</span>"
                   f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;line-height:1.22;color:{B_INK};padding-top:4px;\">{p}</span></div>"
                   for k, p in enumerate(s["points"]))
    t += f"<div style='{ab(60, 580, 540)}'>{rows}</div>"
    t += (f"<div style='{ab(60, 1060, 960)}border:3px dashed {B_HI};padding:22px 28px;box-sizing:border-box;'>"
          f"<span style=\"font-family:{MONO};font-weight:700;font-size:22px;letter-spacing:3px;color:{B_HI};\">NOTE: </span>"
          f"<span style=\"font-family:Inter;font-weight:700;font-size:27px;line-height:1.25;color:{B_INK};\">{s['tip']}</span></div>")
    return t + E.footer(g["cta_url"], ink=B_INK, swipe_ink=B_HI)


def blueprint_cta(g):
    t = _b_bg() + logo(False)
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), f"color:{B_HI};")
    t += (f"<div style=\"{ab(60, 196, 960)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.02;letter-spacing:-3px;color:{B_INK};\">{q}</div>"
          f"<div style=\"{ab(60, 396, 900)}font-family:{MONO};font-weight:700;font-size:28px;color:{B_MUT};\">{g['cta_sub']}</div>")
    t += _b_ruler(g, 80, 620, 920, labels=True)
    rows = "".join(f"<div style='display:flex;gap:20px;align-items:baseline;padding:12px 0;border-bottom:2px solid rgba(242,247,255,.25);'>"
                   f"<span style=\"font-family:{MONO};font-weight:700;font-size:24px;color:{B_HI};width:52px;\">P{k + 1}</span>"
                   f"<span style=\"font-family:{MONO};font-weight:700;font-size:22px;color:{B_MUT};width:170px;\">{s.get('phase', '')}</span>"
                   f"<span style=\"font-family:Inter;font-weight:800;font-size:30px;color:{B_INK};\">{s['title'].split(': ', 1)[-1]}</span></div>"
                   for k, s in enumerate(g["steps"]))
    t += f"<div style='{ab(60, 730, 960)}'>{rows}</div>"
    return t + pill("Post your internship at", g["cta_url"], B_HI, DEEP, y=1150, shadow=f"8px 8px 0 {B_INK}")


# =====================================================================================
#  KANBAN - a whiteboard of sticky notes, magnets and marker pen
# =====================================================================================
K_BOARD, K_FRAME, K_INK, K_RED = "#FBFCFD", "#B9C2CC", "#1B2433", "#E0393E"
K_NOTES = ["#FFE066", "#8CE0C8", "#FFB3C7", "#9CC9FF", "#FFC48A"]


def _k_bg():
    return (f"<div style='position:absolute;inset:0;background:#7E8894;'></div>"
            f"<div style='{ab(18, 18, 1044, 1314)}background:{K_FRAME};border-radius:10px;'></div>"
            f"<div style='{ab(32, 32, 1016, 1286)}background:linear-gradient(135deg,#FFFFFF,{K_BOARD} 55%,#EEF2F6);border-radius:4px;"
            f"box-shadow:inset 0 0 0 2px rgba(0,0,0,.06);'></div>"
            f"<div style='{ab(-80, 160, 700, 40)}background:linear-gradient(90deg,transparent,rgba(255,255,255,.9),transparent);"
            f"transform:rotate(-32deg);opacity:.7;'></div>")


def _magnet(x, y, c=K_RED, s=40):
    return (f"<div style='{ab(x, y, s, s)}border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff3,{c} 45%);"
            f"box-shadow:0 5px 8px rgba(0,0,0,.3);z-index:4;'></div>")


def _note(text, x, y, w, h, c, rot, size=30, extra=""):
    return (f"<div style='{ab(x, y, w, h)}background:{c};transform:rotate({rot}deg);box-shadow:0 12px 18px rgba(27,36,51,.18);"
            f"padding:30px 26px;box-sizing:border-box;{extra}'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:{size}px;line-height:1.2;color:{K_INK};\">{text}</div></div>")


def _k_photo(pid, x, y, w, h, rot):
    return (f"<div style='{ab(x, y, w, h)}transform:rotate({rot}deg);background:#fff;padding:12px 12px 12px;box-shadow:0 14px 26px rgba(27,36,51,.22);'>"
            f"<div style='width:100%;height:100%;background:url({photo(pid)}) center/cover;'></div></div>")


def kanban_cover(g):
    t = _k_bg() + logo()
    t += (f"<div style=\"position:absolute;right:70px;top:78px;font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:4px;"
          f"color:{K_RED};\">{g['kicker']}</div>")
    t += (f"<div style='{ab(70, 200, 600)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:98px;line-height:1;letter-spacing:-3.5px;color:{K_INK};\">{g['title_pre']}</div>"
          f"<div style=\"font-family:IWSerif;font-style:italic;font-size:124px;line-height:1.02;color:{K_RED};\">{g['title_hi']}</div>"
          f"<svg width='470' height='30' viewBox='0 0 470 30'><path d='M6 18C120 4 300 26 464 10' fill='none' stroke='{K_RED}' stroke-width='7' stroke-linecap='round'/></svg>"
          f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:34px;color:{K_INK};margin-top:18px;\">{g['sub']}</div></div>")
    t += _k_photo(g["cover_photo"], 680, 190, 330, 400, 3) + _magnet(825, 172)
    n, lab = g["badge"]
    t += (f"<div style='{ab(70, 640, 940)}display:flex;align-items:center;gap:20px;'>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:26px;letter-spacing:4px;color:{K_INK};\">THE BOARD</span>"
          f"<span style='flex:1;height:4px;background:{K_INK};border-radius:2px;'></span>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:26px;letter-spacing:4px;color:{K_RED};\">{n} {lab}</span></div>")
    rots = [-3, 2, -1.5, 3, -2]
    for k, s in enumerate(g["steps"]):
        x = 64 + k * 192
        t += _note(s["title"], x, 730 + (k % 2) * 50, 180, 190, K_NOTES[k % 5], rots[k % 5], 27)
        t += _magnet(x + 70, 712 + (k % 2) * 50, [K_RED, "#2E6BE6", "#1FA36B", "#F08A00", "#7A3FE0"][k], 34)
    t += (f"<div style=\"{ab(70, 1040, 560)}font-family:IWSerif;font-style:italic;font-size:44px;line-height:1.15;color:{K_INK};\">"
          f"3 tasks per team, ready to hand over.</div>")
    t += A._pen_arrow(560, 1010, 120, 80, "M10 60 Q 60 0 110 20").replace(A.PEN, K_RED)
    t += _k_photo(g["cover_inset"], 720, 1000, 280, 230, -3) + _magnet(840, 984, "#2E6BE6")
    return t + E.footer(g["cta_url"], ink=K_INK, swipe_ink=K_RED)


def kanban_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    c = K_NOTES[i % 5]
    t = _k_bg() + logo()
    t += (f"<div style=\"position:absolute;right:70px;top:78px;font-family:'DM Sans';font-weight:800;font-size:22px;letter-spacing:4px;"
          f"color:{K_INK};\">{g.get('unit', 'team').upper()} {i + 1} / {n}</div>")
    t += (f"<div style='{ab(70, 190)}display:flex;align-items:center;gap:22px;'>"
          f"<span style='width:64px;height:64px;background:{c};transform:rotate(-4deg);box-shadow:0 6px 10px rgba(0,0,0,.15);'></span>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:{96 if len(s['title']) <= 11 else 64}px;line-height:1;letter-spacing:-3px;color:{K_INK};\">{s['title']}</span></div>")
    t += (f"<div style=\"{ab(70, 300, 600)}font-family:IWSerif;font-style:italic;font-size:40px;color:{K_RED};\">3 tasks to hand over</div>")
    t += _k_photo(s["photo"], 700, 170, 310, 330, 3) + _magnet(838, 152)
    rots = [-2, 1.5, -1]
    for k, p in enumerate(s["points"]):
        x, y = [(70, 420), (390, 470), (70, 760)][k]
        t += _note(p, x, y, 300, 300, c, rots[k], 32)
        t += (f"<div style=\"{ab(x + 22, y + 236)}transform:rotate({rots[k]}deg);font-family:{MONO};font-weight:700;font-size:22px;"
              f"color:rgba(27,36,51,.55);\">TASK {k + 1}</div>")
    t += icon(s["icon"], 230, 760, 600, "#fff", f"5px solid {K_INK}", "box-shadow:0 12px 20px rgba(0,0,0,.12);")
    t += (f"<div style='{ab(410, 860, 610)}'>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:4px;color:{K_RED};\">MANAGER NOTE</div>"
          f"<div style=\"font-family:IWSerif;font-style:italic;font-size:38px;line-height:1.2;color:{K_INK};margin-top:8px;\">{s['tip']}</div></div>")
    return t + E.footer(g["cta_url"], ink=K_INK, swipe_ink=K_RED)


def kanban_cta(g):
    t = _k_bg() + logo()
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), f"font-family:IWSerif;font-style:italic;font-weight:400;color:{K_RED};letter-spacing:0;")
    t += (f"<div style=\"{ab(70, 196, 940)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.04;letter-spacing:-3px;color:{K_INK};\">{q}</div>"
          f"<div style=\"{ab(70, 400, 900)}font-family:'DM Sans';font-weight:700;font-size:32px;color:{K_INK};\">{g['cta_sub']}</div>")
    cols = ["TO DO", "DOING", "DONE"]
    for k, c in enumerate(cols):
        x = 70 + k * 315
        t += (f"<div style=\"{ab(x, 490, 290)}font-family:Inter;font-weight:900;font-size:26px;letter-spacing:4px;color:{K_INK};"
              f"padding-bottom:10px;border-bottom:4px solid {K_INK};\">{c}</div>")
    for k, s in enumerate(g["steps"]):
        col, row = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)][k]
        x, y = 70 + col * 315 + 10, 570 + row * 240
        t += _note(s["title"], x, y, 270, 200, K_NOTES[k % 5], [-2, 1.5, -1, 2, -1.5][k], 30)
    t += _k_photo(g["steps"][-1]["photo"], 720, 820, 280, 250, 3) + _magnet(840, 804)
    return t + pill("Post your internship at", g["cta_url"], AMBER, K_INK, y=1150, shadow=f"8px 8px 0 {K_INK}")


# =====================================================================================
#  TICKET - each step is a boarding pass for the intern's first day
# =====================================================================================
P_SKY, P_INK, P_ORA, P_MUT, P_TEAL = "#CFE8FF", "#13233F", "#FF7A2F", "#6B7A93", "#1C8C8C"


def _p_bg():
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(170deg,{P_SKY} 0%,#EAF4FF 55%,#FFF1E3 100%);'></div>"
            f"<svg style='{ab(0, 0)}' width='1080' height='1350'><g fill='#fff' opacity='.85'>"
            f"<ellipse cx='880' cy='1030' rx='170' ry='38'/><ellipse cx='800' cy='1010' rx='90' ry='44'/>"
            f"<ellipse cx='140' cy='600' rx='130' ry='30'/><ellipse cx='200' cy='585' rx='70' ry='36'/></g>"
            f"<path d='M120 1250 Q 540 1150 1000 1240' fill='none' stroke='{P_INK}' stroke-opacity='.18' stroke-width='3' stroke-dasharray='4 14' stroke-linecap='round'/></svg>")


def _p_window(pid, x, y, w, h):
    return (f"<div style='{ab(x, y, w, h)}border-radius:{w // 2}px;background:#fff;padding:18px;box-sizing:border-box;"
            f"box-shadow:0 20px 40px rgba(19,35,63,.22), inset 0 0 0 4px #E3E9F2;'>"
            f"<div style='width:100%;height:100%;border-radius:{w // 2 - 18}px;background:url({photo(pid)}) center/cover;"
            f"box-shadow:inset 0 0 0 6px rgba(19,35,63,.08);'></div></div>")


def _barcode(x, y, w, h, c=P_INK):
    bars, xx, k = "", 0, 0
    widths = [3, 6, 2, 4, 8, 2, 3, 5, 2, 7, 3, 2, 6, 4, 2, 3]
    while xx < w:
        bw = widths[k % len(widths)]
        if k % 2 == 0:
            bars += f"<rect x='{xx}' y='0' width='{bw}' height='{h}' fill='{c}'/>"
        xx += bw + 2
        k += 1
    return f"<svg style='{ab(x, y)}' width='{w}' height='{h}'>{bars}</svg>"


def _pass(x, y, w, h, body, stub, head_color=P_ORA, head="BOARDING PASS", stub_w=230, rot=0):
    """A boarding pass: header band, main body, perforation, stub."""
    return (f"<div style='{ab(x, y, w, h)}transform:rotate({rot}deg);filter:drop-shadow(0 22px 34px rgba(19,35,63,.22));'>"
            f"<div style='position:absolute;inset:0;background:#fff;border-radius:26px;"
            f"-webkit-mask:radial-gradient(circle 22px at {w - stub_w}px 0,transparent 98%,#000) top/100% 51% no-repeat,"
            f"radial-gradient(circle 22px at {w - stub_w}px 100%,transparent 98%,#000) bottom/100% 51% no-repeat;'></div>"
            f"<div style='{ab(0, 0, w, 70)}background:{head_color};border-radius:26px 26px 0 0;'></div>"
            f"<div style=\"{ab(34, 20)}font-family:'DM Sans';font-weight:800;font-size:22px;letter-spacing:5px;color:#fff;\">{head}</div>"
            f"<div style='{ab(w - stub_w - 2, 34, 4, h - 68)}background-image:linear-gradient({P_MUT} 50%,transparent 50%);"
            f"background-size:4px 16px;opacity:.6;'></div>"
            f"<div style='{ab(0, 70, w - stub_w, h - 70)}'>{body}</div>"
            f"<div style='{ab(w - stub_w, 70, stub_w, h - 70)}'>{stub}</div></div>")


def _field(label, value, size=34):
    return (f"<div><div style=\"font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:3px;color:{P_MUT};\">{label}</div>"
            f"<div style=\"font-family:Inter;font-weight:900;font-size:{size}px;color:{P_INK};margin-top:2px;\">{value}</div></div>")


def ticket_cover(g):
    t = _p_bg() + logo()
    t += (f"<div style=\"position:absolute;right:56px;top:76px;font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:4px;"
          f"color:{P_INK};\">{g['kicker']}</div>")
    t += _p_window(g["cover_photo"], 690, 180, 330, 460)
    t += (f"<div style='{ab(56, 210, 620)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:84px;line-height:1;letter-spacing:-3px;color:{P_INK};\">{g['title_pre']}</div>"
          f"<div style=\"font-family:IWSerif;font-style:italic;font-size:132px;line-height:1.02;color:{P_ORA};\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:84px;line-height:1;letter-spacing:-3px;color:{P_INK};\">{g['title_post']}</div></div>")
    n, lab = g["badge"]
    body = (f"<div style='{ab(34, 30, 640)}display:grid;grid-template-columns:1fr 1fr;row-gap:22px;column-gap:24px;'>"
            + _field("PASSENGER", "Your new intern") + _field("DESTINATION", "Day one")
            + _field("DEPARTS", g["steps"][1].get("time", "09:00")) + _field("STEPS", f"{n} {lab.lower()}")
            + f"</div><div style=\"{ab(34, 300, 620)}font-family:'DM Sans';font-weight:700;font-size:30px;color:{P_INK};\">{g['sub']}</div>")
    stub = (f"<div style='{ab(30, 30, 170)}'>" + _field("GATE", "1", 54) + "</div>"
            + f"<div style='{ab(30, 150, 170)}'>" + _field("SEAT", "Welcome", 30) + "</div>" + _barcode(30, 270, 170, 70))
    t += _pass(56, 700, 968, 420, body, stub, rot=-1.2)
    return t + E.footer(g["cta_url"], ink=P_INK, swipe_ink=P_ORA)


def ticket_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    t = _p_bg() + logo()
    t += (f"<div style=\"position:absolute;right:56px;top:76px;font-family:'DM Sans';font-weight:800;font-size:22px;letter-spacing:4px;"
          f"color:{P_INK};\">{g.get('unit', 'step').upper()} {i + 1} OF {n}</div>")
    t += (f"<div style='{ab(56, 196, 620)}'>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:28px;letter-spacing:5px;color:{P_ORA};\">{s.get('time', '')}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:80px;line-height:1.02;letter-spacing:-3px;color:{P_INK};margin-top:10px;\">"
          f"{hi_wrap(s['title'], s.get('hi'), f'font-family:IWSerif;font-style:italic;font-weight:400;letter-spacing:0;color:{P_ORA};')}</div></div>")
    t += _p_window(s["photo"], 720, 160, 300, 400)
    rows = "".join(f"<div style='display:flex;gap:16px;align-items:flex-start;padding:16px 0;border-bottom:2px dashed #D5DEEA;'>"
                   f"<span style='flex:none;width:36px;height:36px;border-radius:50%;background:{P_TEAL};display:flex;align-items:center;"
                   f"justify-content:center;margin-top:2px;'>{check('#fff', 20, 3.8)}</span>"
                   f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;line-height:1.22;color:{P_INK};\">{p}</span></div>"
                   for p in s["points"])
    body = f"<div style='{ab(34, 18, 660)}'>{rows}</div>"
    stub = (f"<div style='{ab(26, 26, 180)}'>" + _field("STEP", f"{i + 1:02d}", 64) + "</div>"
            + f"<div style='{ab(26, 150, 180)}'>" + _field("BOARDS", s.get('time', '').replace('THE WEEK BEFORE', 'Wk -1'), 30) + "</div>"
            + icon(s["icon"], 140, 40, 250, "#F2F6FB"))
    t += _pass(56, 590, 968, 440, body, stub, head=f"BOARDING PASS · {g.get('unit', 'step').upper()} {i + 1}")
    # luggage-tag tip
    t += (f"<div style='{ab(56, 1068, 968)}background:{P_INK};border-radius:18px 60px 60px 18px;padding:22px 34px;box-sizing:border-box;"
          f"display:flex;gap:22px;align-items:center;'>"
          f"<span style='flex:none;width:26px;height:26px;border-radius:50%;background:#EAF4FF;'></span>"
          f"<span style=\"font-family:Inter;font-weight:700;font-size:27px;line-height:1.25;color:#fff;\">{s['tip']}</span></div>")
    return t + E.footer(g["cta_url"], ink=P_INK, swipe_ink=P_ORA)


def ticket_cta(g):
    t = (f"<div style='position:absolute;inset:0;background:linear-gradient(170deg,{P_INK},#0B1730);'></div>" + logo(False))
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), f"font-family:IWSerif;font-style:italic;font-weight:400;color:{P_ORA};letter-spacing:0;")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:86px;line-height:1.04;letter-spacing:-3px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 400, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:#B9C8E0;\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='display:flex;align-items:center;gap:22px;padding:16px 26px;background:#fff;border-radius:16px;margin-bottom:14px;'>"
                   f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:22px;letter-spacing:2px;color:{P_ORA};width:200px;\">"
                   f"{s.get('time', '')}</span>"
                   f"<span style=\"font-family:Inter;font-weight:800;font-size:29px;color:{P_INK};\">{s['title']}</span>"
                   f"<span style='margin-left:auto;'>{check(P_TEAL, 30, 3.6)}</span></div>"
                   for s in g["steps"])
    t += f"<div style='{ab(56, 490, 968)}'>{rows}</div>"
    return t + pill("Post your internship at", g["cta_url"], P_ORA, "#fff", y=1150, shadow="8px 8px 0 #fff")


WORLDS_B = {
    "transit": (transit_cover, transit_step, transit_cta),
    "swiss": (swiss_cover, swiss_step, swiss_cta),
    "blueprint": (blueprint_cover, blueprint_step, blueprint_cta),
    "kanban": (kanban_cover, kanban_step, kanban_cta),
    "ticket": (ticket_cover, ticket_step, ticket_cta),
}
