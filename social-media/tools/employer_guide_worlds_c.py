"""Third bank of employer guide design worlds (week 26+). Registered into
employer_guide_worlds.WORLDS alongside banks 1 and 2.

    chat        - a messaging app: questions as sent bubbles, a phone on the cover
    rolodex     - a card index: ruled index cards with coloured tabs, a file box
    chalkboard  - a classroom board: chalk type, taped instant photos, chalk ticks
    letter      - letter writing: cream sheets, postage-stamp badges, a wax seal
    boardgame   - a board game: a winding path of squares, counters and a dice
"""
import lanes_common as L
import lane_employer_guide as E
import employer_guide_worlds as A
from employer_guide_worlds_b import logo, icon

ab, pill, hi_wrap, check, photo = A.ab, A.pill, A.hi_wrap, A.check, E.photo
SERIF = "font-family:IWSerif;font-style:italic;font-weight:400;letter-spacing:0;"


def kick(text, color, extra=""):
    return (f"<div style=\"position:absolute;right:56px;top:78px;font-family:'DM Sans';font-weight:800;font-size:21px;"
            f"letter-spacing:4px;color:{color};{extra}\">{text}</div>")


def step_label(g, i, default):
    return f"{g.get('unit', default).upper()} {i + 1} OF {len(g['steps'])}"


# =====================================================================================
#  CHAT - the interview is a conversation; every question is a sent message
# =====================================================================================
C_BG1, C_BG2, C_VIO, C_INK, C_GREY, C_MUT, C_GREEN, C_SUN = (
    "#F4F1FF", "#E2DBFF", "#6A4CFF", "#1B1440", "#ECE9F7", "#7A7396", "#22C26E", "#FFD66B")


def _c_bg():
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,{C_BG1},{C_BG2});'></div>"
            f"<div style='{ab(-160, 900, 520, 520)}border-radius:50%;background:rgba(106,76,255,.08);'></div>"
            f"<div style='{ab(820, -120, 420, 420)}border-radius:50%;background:rgba(106,76,255,.07);'></div>")


def _avatar(pid, size, x=None, y=None, ring="#fff"):
    pos = ab(x, y) if x is not None else "position:relative;"
    return (f"<div style='{pos}flex:none;width:{size}px;height:{size}px;border-radius:50%;"
            f"background:url({photo(pid)}) center/cover;box-shadow:0 0 0 4px {ring};'></div>")


def _sent(text, size=22, maxw=290, pad="14px 18px"):
    return (f"<div style='display:flex;justify-content:flex-end;'><div style=\"max-width:{maxw}px;background:{C_VIO};color:#fff;"
            f"border-radius:22px 22px 6px 22px;padding:{pad};font-family:Inter;font-weight:600;font-size:{size}px;"
            f"line-height:1.28;\">{text}</div></div>")


def _typing(size=12):
    d = "".join(f"<span style='width:{size}px;height:{size}px;border-radius:50%;background:{C_MUT};opacity:{o};'></span>"
                for o in (.9, .6, .35))
    return (f"<div style='display:inline-flex;gap:{size // 2 + 2}px;background:#fff;border-radius:22px 22px 22px 6px;"
            f"padding:{size + 6}px {size + 10}px;box-shadow:0 4px 12px rgba(27,20,64,.08);'>{d}</div>")


def chat_cover(g):
    t = _c_bg() + logo() + kick(g["kicker"], C_INK)
    t += (f"<div style='{ab(56, 196, 580)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:62px;line-height:1.04;letter-spacing:-2px;color:{C_INK};\">{g['title_pre']}</div>"
          f"<div style=\"{SERIF}font-size:112px;line-height:1.02;color:{C_VIO};\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:62px;line-height:1.04;letter-spacing:-2px;color:{C_INK};\">{g['title_post']}</div>"
          f"<div style=\"display:inline-block;margin-top:30px;background:#fff;border-radius:26px 26px 26px 8px;padding:18px 26px;"
          f"font-family:'DM Sans';font-weight:700;font-size:28px;line-height:1.25;color:{C_INK};box-shadow:0 8px 22px rgba(27,20,64,.10);\">"
          f"{g['sub']}</div></div>")
    # interviewer photo + badge
    t += (f"<div style='{ab(56, 760, 500, 380)}border-radius:36px;background:url({photo(g['cover_photo'])}) center/cover;"
          f"box-shadow:0 22px 44px rgba(27,20,64,.22);'></div>")
    n, lab = g["badge"]
    t += (f"<div style='{ab(456, 680, 170, 170)}border-radius:50% 50% 50% 12px;background:{C_VIO};display:flex;flex-direction:column;"
          f"align-items:center;justify-content:center;transform:rotate(-6deg);box-shadow:0 14px 28px rgba(106,76,255,.35);'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:66px;line-height:1;color:#fff;\">{n}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:17px;letter-spacing:3px;color:#fff;\">{lab}</div></div>")
    # the phone
    msgs = "".join(f"<div style='margin-top:16px;'>{_sent(g['steps'][k]['points'][0])}</div>" for k in range(3))
    t += (f"<div style='{ab(644, 176, 384, 940)}border-radius:62px;background:{C_INK};padding:14px;box-sizing:border-box;"
          f"box-shadow:0 34px 60px rgba(27,20,64,.30);'>"
          f"<div style='position:relative;width:100%;height:100%;border-radius:50px;background:#FBFAFF;overflow:hidden;'>"
          f"<div style='{ab(120, 14, 116, 26)}border-radius:14px;background:{C_INK};'></div>"
          f"<div style='{ab(0, 58, 356, 96)}display:flex;align-items:center;gap:14px;padding:0 22px;box-sizing:border-box;"
          f"border-bottom:2px solid {C_GREY};'>{_avatar(g['cover_inset'], 56)}"
          f"<div><div style=\"font-family:Inter;font-weight:800;font-size:24px;color:{C_INK};\">Candidate</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:17px;color:{C_MUT};display:flex;align-items:center;gap:6px;\">"
          f"<span style='width:10px;height:10px;border-radius:50%;background:{C_GREEN};'></span>online</div></div></div>"
          f"<div style='{ab(18, 170, 320)}'>"
          f"<div style='text-align:center;'><span style=\"font-family:'DM Sans';font-weight:700;font-size:15px;letter-spacing:2px;"
          f"color:{C_MUT};background:{C_GREY};border-radius:10px;padding:5px 12px;\">INTERVIEW · TODAY</span></div>"
          f"{msgs}<div style='margin-top:18px;'>{_typing()}</div></div>"
          f"<div style='{ab(18, 806, 320, 64)}border-radius:32px;background:{C_GREY};'></div>"
          f"<div style='{ab(282, 812, 52, 52)}border-radius:50%;background:{C_VIO};display:flex;align-items:center;justify-content:center;'>"
          f"<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='3' stroke-linecap='round' "
          f"stroke-linejoin='round'><path d='M5 12h13M13 6l6 6-6 6'/></svg></div></div></div>")
    return t + E.footer(g["cta_url"], ink=C_INK, swipe_ink=C_VIO)


def chat_step(g, i):
    s = g["steps"][i]
    t = _c_bg() + logo() + kick(step_label(g, i, "set"), C_INK)
    t += (f"<div style=\"{ab(56, 186, 780)}font-family:Inter;font-weight:900;font-size:80px;line-height:1.02;letter-spacing:-3px;"
          f"color:{C_INK};\">{hi_wrap(s['title'], s.get('hi'), SERIF + f'color:{C_VIO};')}</div>")
    t += icon(s["icon"], 132, 892, 180, "#fff", extra="box-shadow:0 12px 26px rgba(27,20,64,.12);")
    rows = ""
    for p in s["points"]:
        rows += (f"<div style='display:flex;justify-content:flex-end;align-items:flex-end;gap:16px;margin-bottom:34px;'>"
                 f"<div><div style=\"max-width:780px;background:{C_VIO};color:#fff;border-radius:36px 36px 8px 36px;padding:28px 36px;"
                 f"font-family:Inter;font-weight:700;font-size:39px;line-height:1.24;box-shadow:0 10px 22px rgba(106,76,255,.22);\">{p}</div>"
                 f"<div style=\"text-align:right;font-family:'DM Sans';font-weight:700;font-size:17px;letter-spacing:1px;color:{C_MUT};"
                 f"margin-top:6px;\">Sent</div></div>{_avatar(g['cover_photo'], 62)}</div>")
    t += f"<div style='{ab(56, 384, 968)}'>{rows}</div>"
    t += (f"<div style='{ab(56, 1066, 968)}background:#FFF6D6;border-left:10px solid {C_SUN};border-radius:18px;padding:20px 30px;"
          f"box-sizing:border-box;box-shadow:0 8px 20px rgba(27,20,64,.08);'>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:3px;color:#B7861A;\">PINNED · LISTEN FOR</div>"
          f"<div style=\"font-family:Inter;font-weight:700;font-size:28px;line-height:1.25;color:{C_INK};margin-top:6px;\">{s['tip']}</div></div>")
    return t + E.footer(g["cta_url"], ink=C_INK, swipe_ink=C_VIO)


def chat_cta(g):
    t = (f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#5B3DF5,#2A1680);'></div>" + logo(False))
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), SERIF + f"color:{C_SUN};")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.04;letter-spacing:-3px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 400, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:#D9D1FF;\">{g['cta_sub']}</div>")
    rows = "".join(
        f"<div style='display:flex;align-items:center;gap:20px;padding:14px 22px;background:#fff;border-radius:22px;margin-bottom:12px;'>"
        f"<div style='flex:none;width:62px;height:62px;border-radius:50%;background:{C_BG1};display:flex;align-items:center;justify-content:center;'>"
        f"<svg viewBox='0 0 200 200' width='46' height='46'>{E.SPOTS[s['icon']]}</svg></div>"
        f"<div style='flex:1;'><div style=\"font-family:Inter;font-weight:800;font-size:29px;color:{C_INK};\">{s['title']}</div>"
        f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:20px;color:{C_MUT};\">{len(s['points'])} questions</div></div>"
        f"<div style=\"flex:none;width:40px;height:40px;border-radius:50%;background:{C_VIO};color:#fff;display:flex;align-items:center;"
        f"justify-content:center;font-family:Inter;font-weight:900;font-size:20px;\">{len(s['points'])}</div></div>"
        for s in g["steps"])
    t += f"<div style='{ab(56, 478, 968)}'>{rows}</div>"
    return t + pill("Post your internship at", g["cta_url"], C_SUN, C_INK, y=1150, shadow="8px 8px 0 #fff")


# =====================================================================================
#  ROLODEX - the job description is a set of index cards in a file box
# =====================================================================================
R_DESK, R_CARD, R_RED, R_RULE, R_INK, R_BOX, R_MUT = (
    "#E9E1D0", "#FFFDF6", "#E2574C", "#BCD3EA", "#22313F", "#2F6B5B", "#7B8794")
R_TABS = ["#F5B841", "#5FB3A1", "#E2574C", "#7C9FD9", "#C58BD6"]


def _r_bg():
    return (f"<div style='position:absolute;inset:0;background:{R_DESK};"
            f"background-image:repeating-linear-gradient(98deg,rgba(80,60,30,.035) 0 3px,transparent 3px 17px);'></div>")


def _r_card(x, y, w, h, inner="", rot=0, red_at=100, rule_from=None, gap=62, shadow=True):
    rf = rule_from if rule_from is not None else red_at + gap
    sh = "box-shadow:0 18px 34px rgba(34,49,63,.20);" if shadow else "box-shadow:0 2px 0 rgba(34,49,63,.12);"
    return (f"<div style='{ab(x, y, w, h)}transform:rotate({rot}deg);background:{R_CARD};border-radius:10px;{sh}'>"
            f"<div style='{ab(0, rf - gap + 2, w, h - rf + gap - 10)}background:repeating-linear-gradient(to bottom,transparent 0 {gap - 2}px,"
            f"{R_RULE} {gap - 2}px {gap}px);'></div>"
            f"<div style='{ab(0, red_at, w, 3)}background:{R_RED};opacity:.75;'></div>{inner}</div>")


def _r_tab(x, y, w, color, text, size=22):
    return (f"<div style=\"{ab(x, y, w, 60)}background:{color};border-radius:14px 14px 0 0;display:flex;align-items:center;"
            f"justify-content:center;font-family:'DM Sans';font-weight:800;font-size:{size}px;letter-spacing:3px;color:#fff;\">{text}</div>")


def rolodex_cover(g):
    t = _r_bg() + logo() + kick(g["kicker"], R_INK)
    t += (f"<div style='{ab(56, 196, 968)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:80px;line-height:1.02;letter-spacing:-3px;color:{R_INK};\">{g['title_pre']}</div>"
          f"<div style=\"{SERIF}font-size:116px;line-height:1.04;color:{R_RED};\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:80px;line-height:1.02;letter-spacing:-3px;color:{R_INK};\">{g['title_post']}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:30px;color:{R_MUT};margin-top:18px;\">{g['sub']}</div></div>")
    # cards standing in the file box, tabs labelled with each part's key word
    for k, s in enumerate(g["steps"]):
        y = 640 + k * 40
        t += _r_tab(96 + (k % 3) * 196, y - 54, 186, R_TABS[k % len(R_TABS)], s.get("hi", s["title"]).upper(), 19)
        t += _r_card(86, y, 620, 330, red_at=70, gap=40, shadow=False)
    t += (f"<div style='{ab(56, 880, 680, 300)}background:{R_BOX};border-radius:16px 16px 22px 22px;"
          f"box-shadow:0 26px 40px rgba(34,49,63,.30), inset 0 8px 0 rgba(255,255,255,.12);'>"
          f"<div style='{ab(230, 96, 220, 108)}background:{R_CARD};border-radius:10px;border:4px solid #CFC6B2;display:flex;"
          f"flex-direction:column;align-items:center;justify-content:center;'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:52px;line-height:1;color:{R_INK};\">{g['badge'][0]}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:4px;color:{R_RED};\">{g['badge'][1]}</div></div></div>")
    t += (f"<div style='{ab(762, 610, 262, 330)}transform:rotate(5deg);background:#fff;padding:14px;box-sizing:border-box;"
          f"box-shadow:0 18px 30px rgba(34,49,63,.25);'><div style='width:100%;height:100%;background:url({photo(g['cover_photo'])}) center/cover;'></div></div>")
    t += A._paperclip(860, 586, 8)
    return t + E.footer(g["cta_url"], ink=R_INK, swipe_ink=R_RED)


def rolodex_step(g, i):
    s = g["steps"][i]
    col = R_TABS[i % len(R_TABS)]
    t = _r_bg() + logo() + kick(step_label(g, i, "part"), R_INK)
    t += _r_tab(96, 252, 300, col, f"PART {i + 1:02d}", 24)
    pts = "".join(f"<div style='display:flex;gap:18px;align-items:flex-start;'>"
                  f"<span style='flex:none;width:34px;height:34px;margin-top:19px;border:3px solid {R_INK};border-radius:6px;display:flex;"
                  f"align-items:center;justify-content:center;'>{check(R_RED, 22, 4)}</span>"
                  f"<span style=\"font-family:Inter;font-weight:700;font-size:31px;line-height:74px;color:{R_INK};\">{p}</span></div>"
                  for p in s["points"])
    inner = (f"<div style=\"{ab(44, 30, 600)}font-family:Inter;font-weight:900;font-size:60px;line-height:1.04;letter-spacing:-2px;"
             f"color:{R_INK};\">{hi_wrap(s['title'], s.get('hi'), SERIF + f'color:{R_RED};')}</div>"
             f"<div style='{ab(44, 180, 590)}'>{pts}</div>"
             f"<div style='{ab(44, 560, 690)}transform:rotate(-1deg);background:#FFF2B8;padding:22px 28px;box-sizing:border-box;"
             f"box-shadow:0 6px 14px rgba(34,49,63,.14);'>"
             f"<span style=\"font-family:{A.MONO};font-weight:700;font-size:22px;letter-spacing:3px;color:{R_RED};\">TIP </span>"
             f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;line-height:1.3;color:{R_INK};\">{s['tip']}</span></div>")
    t += _r_card(56, 310, 968, 740, inner, rot=-0.6, red_at=168, gap=74)
    t += (f"<div style='{ab(752, 336, 250, 300)}transform:rotate(4deg);background:#fff;padding:12px;box-sizing:border-box;"
          f"box-shadow:0 14px 26px rgba(34,49,63,.22);'><div style='width:100%;height:100%;background:url({photo(s['photo'])}) center/cover;'></div></div>")
    t += A._paperclip(830, 312, 6)
    t += icon(s["icon"], 132, 852, 850, "#fff", border=f"5px solid {col}")
    return t + E.footer(g["cta_url"], ink=R_INK, swipe_ink=R_RED)


def rolodex_cta(g):
    t = (f"<div style='position:absolute;inset:0;background:{R_BOX};"
         f"background-image:repeating-linear-gradient(98deg,rgba(255,255,255,.03) 0 3px,transparent 3px 17px);'></div>" + logo(False))
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), SERIF + "color:#F5B841;")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.04;letter-spacing:-3px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 400, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:#CFE4DD;\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='display:flex;align-items:center;gap:20px;height:72px;'>"
                   f"<span style=\"flex:none;width:46px;height:46px;border-radius:10px;background:{R_TABS[k % len(R_TABS)]};color:#fff;"
                   f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:22px;\">{k + 1}</span>"
                   f"<span style=\"flex:1;font-family:Inter;font-weight:800;font-size:30px;color:{R_INK};\">{s['title']}</span>"
                   f"{check(R_RED, 30, 3.6)}</div>" for k, s in enumerate(g["steps"]))
    t += _r_card(56, 500, 968, 520, f"<div style=\"{ab(40, 22)}font-family:{A.MONO};font-weight:700;font-size:22px;letter-spacing:4px;"
                 f"color:{R_RED};\">CHECKLIST</div><div style='{ab(40, 84, 888)}'>{rows}</div>", rot=-0.8, red_at=74, gap=72)
    return t + pill("Post your internship at", g["cta_url"], "#F5B841", R_INK, y=1150, shadow="8px 8px 0 #fff")


# =====================================================================================
#  CHALKBOARD - feedback is teaching; every habit is chalked up on the board
# =====================================================================================
K_BOARD, K_WOOD, K_CHALK, K_YEL, K_PINK, K_BLUE = "#213A30", "#9A6A3F", "#F4F1E8", "#F7D774", "#F49AC1", "#9AD0F5"


def _k_bg():
    return (f"<div style='position:absolute;inset:0;background:{K_WOOD};'></div>"
            f"<div style='{ab(22, 22, 1036, 1306)}border-radius:8px;background:"
            f"radial-gradient(ellipse at 28% 18%,rgba(255,255,255,.07),transparent 42%),"
            f"radial-gradient(ellipse at 78% 72%,rgba(255,255,255,.06),transparent 46%),"
            f"radial-gradient(ellipse at 60% 40%,rgba(255,255,255,.035),transparent 30%),{K_BOARD};"
            f"box-shadow:inset 0 0 0 5px #7A4F2C, inset 0 0 60px rgba(0,0,0,.35);'></div>")


def _chalk_line(x, y, w, c=K_YEL):
    return (f"<svg style='{ab(x, y)}' width='{w}' height='26' viewBox='0 0 {w} 26'><path d='M4 16 C {w * .2} 6, {w * .35} 22, {w * .55} 12 "
            f"S {w * .85} 8, {w - 6} 14' fill='none' stroke='{c}' stroke-width='6' stroke-linecap='round' opacity='.9'/></svg>")


def _chalk_tick(c=K_YEL, sz=40):
    return (f"<svg width='{sz}' height='{sz}' viewBox='0 0 40 40' style='flex:none;margin-top:4px;'><path d='M6 22 L16 31 L35 8' fill='none' "
            f"stroke='{c}' stroke-width='5.5' stroke-linecap='round' stroke-linejoin='round' opacity='.95'/></svg>")


def _polaroid(pid, x, y, w, h, rot):
    return (f"<div style='{ab(x, y, w, h)}transform:rotate({rot}deg);background:#FBFAF5;padding:16px 16px 64px;box-sizing:border-box;"
            f"box-shadow:0 18px 34px rgba(0,0,0,.45);'><div style='width:100%;height:100%;background:url({photo(pid)}) center/cover;'></div>"
            f"<div style='{ab(w // 2 - 70, -20, 140, 40)}background:rgba(244,241,232,.75);transform:rotate(-4deg);'></div></div>")


def _k_point(p):
    if p.lower().startswith("example:"):
        body = p.split(":", 1)[1].strip()
        txt = (f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:21px;letter-spacing:3px;color:{K_PINK};\">SAY </span>"
               f"<span style=\"{SERIF}font-size:44px;line-height:1.2;color:{K_CHALK};\">{body}</span>")
        mark = _chalk_tick(K_PINK)
    else:
        txt = f"<span style=\"font-family:Inter;font-weight:700;font-size:38px;line-height:1.25;color:{K_CHALK};\">{p}</span>"
        mark = _chalk_tick()
    return f"<div style='display:flex;gap:20px;align-items:flex-start;margin-bottom:30px;'>{mark}<div>{txt}</div></div>"


def chalkboard_cover(g):
    t = _k_bg() + f"<img src='{L.WHT}' style='{ab(62, 56)}height:{L.LOGO}px;'>" + kick(g["kicker"], K_CHALK, "top:92px;right:70px;opacity:.9;")
    t += (f"<div style='{ab(70, 214, 940)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:80px;line-height:1.02;letter-spacing:-2px;color:{K_CHALK};\">{g['title_pre']}</div>"
          f"<div style=\"{SERIF}font-size:150px;line-height:1.0;color:{K_YEL};\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:80px;line-height:1.02;letter-spacing:-2px;color:{K_CHALK};margin-top:6px;\">{g['title_post']}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:32px;color:{K_CHALK};opacity:.85;margin-top:22px;\">{g['sub']}</div></div>")
    t += _chalk_line(70, 405, 520)
    n, lab = g["badge"]
    t += (f"<svg style='{ab(90, 760)}' width='280' height='280' viewBox='0 0 280 280'><path d='M140 18 C 230 14, 266 90, 262 146 C 258 220, 190 266, 132 262 "
          f"C 60 258, 14 200, 20 132 C 26 66, 80 22, 150 26' fill='none' stroke='{K_CHALK}' stroke-width='6' stroke-linecap='round' opacity='.85'/></svg>"
          f"<div style='{ab(90, 760, 280, 280)}display:flex;flex-direction:column;align-items:center;justify-content:center;'>"
          f"<div style=\"{SERIF}font-size:130px;line-height:.9;color:{K_YEL};\">{n}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:22px;letter-spacing:5px;color:{K_CHALK};\">{lab}</div></div>")
    t += (f"<svg style='{ab(360, 880)}' width='230' height='120' viewBox='0 0 230 120'><path d='M10 80 C 70 20, 150 20, 210 60' fill='none' "
          f"stroke='{K_CHALK}' stroke-width='5' stroke-linecap='round' stroke-dasharray='2 14' opacity='.8'/>"
          f"<path d='M188 42 L212 62 L184 74' fill='none' stroke='{K_CHALK}' stroke-width='5' stroke-linecap='round' stroke-linejoin='round' opacity='.8'/></svg>")
    t += _polaroid(g["cover_photo"], 600, 650, 400, 500, 5)
    return t + E.footer(g["cta_url"], ink=K_CHALK, swipe_ink=K_YEL)


def chalkboard_step(g, i):
    s = g["steps"][i]
    t = _k_bg() + f"<img src='{L.WHT}' style='{ab(62, 56)}height:{L.LOGO}px;'>" + kick(step_label(g, i, "habit"), K_CHALK, "top:92px;right:70px;opacity:.9;")
    t += (f"<div style=\"{ab(70, 220, 610)}font-family:Inter;font-weight:900;font-size:94px;line-height:1.04;letter-spacing:-2px;"
          f"color:{K_CHALK};\">{hi_wrap(s['title'], s.get('hi'), SERIF + f'color:{K_YEL};font-size:112px;white-space:nowrap;')}</div>")
    t += _polaroid(s["photo"], 700, 190, 310, 380, 4)
    t += icon(s["icon"], 116, 920, 500, "#FBFAF5", extra="box-shadow:0 10px 20px rgba(0,0,0,.35);")
    t += f"<div style='{ab(70, 610, 940)}'>{''.join(_k_point(p) for p in s['points'])}</div>"
    t += (f"<div style='{ab(70, 1000, 940)}border:4px dashed rgba(244,241,232,.6);border-radius:20px;padding:20px 28px;box-sizing:border-box;'>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:4px;color:{K_YEL};\">REMEMBER</div>"
          f"<div style=\"font-family:Inter;font-weight:700;font-size:32px;line-height:1.28;color:{K_CHALK};margin-top:6px;\">{s['tip']}</div></div>")
    return t + E.footer(g["cta_url"], ink=K_CHALK, swipe_ink=K_YEL)


def chalkboard_cta(g):
    t = _k_bg() + f"<img src='{L.WHT}' style='{ab(62, 56)}height:{L.LOGO}px;'>"
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), SERIF + f"color:{K_YEL};")
    t += (f"<div style=\"{ab(70, 214, 940)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.04;letter-spacing:-2px;color:{K_CHALK};\">{q}</div>"
          f"<div style=\"{ab(70, 418, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:{K_CHALK};opacity:.85;\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='display:flex;gap:22px;align-items:center;height:92px;border-bottom:3px dashed rgba(244,241,232,.25);'>"
                   f"<span style=\"{SERIF}font-size:54px;color:{K_YEL};width:50px;\">{k + 1}</span>"
                   f"<span style=\"flex:1;font-family:Inter;font-weight:800;font-size:34px;color:{K_CHALK};\">{s['title']}</span>"
                   f"{_chalk_tick(K_YEL, 44)}</div>" for k, s in enumerate(g["steps"]))
    t += f"<div style='{ab(70, 500, 940)}'>{rows}</div>"
    return t + pill("Post your internship at", g["cta_url"], K_YEL, K_BOARD, x=70, y=1140)


# =====================================================================================
#  LETTER - the reference is a letter; every part is a paragraph on cream paper
# =====================================================================================
LT_BG, LT_PAPER, LT_INK, LT_CORAL, LT_GOLD, LT_MUT = "#0F4C5C", "#FBF7EE", "#1F2A33", "#E86A50", "#D9A441", "#8A8F86"


def _lt_bg():
    return (f"<div style='position:absolute;inset:0;background:{LT_BG};"
            f"background-image:radial-gradient(rgba(255,255,255,.06) 2px,transparent 2px);background-size:34px 34px;'></div>")


def _stamp(x, y, w, h, inner, color=LT_GOLD, rot=0):
    holes = (f"radial-gradient(circle 9px at 50% 0,transparent 98%,#000) 0 0/22px 51% repeat-x,"
             f"radial-gradient(circle 9px at 50% 100%,transparent 98%,#000) 0 100%/22px 51% repeat-x")
    return (f"<div style='{ab(x, y, w, h)}transform:rotate({rot}deg);filter:drop-shadow(0 10px 16px rgba(0,0,0,.25));'>"
            f"<div style='position:absolute;inset:0;background:{color};-webkit-mask:{holes};'></div>"
            f"<div style='{ab(14, 16, w - 28, h - 32)}background:{LT_PAPER};border:3px solid {color};box-sizing:border-box;display:flex;"
            f"flex-direction:column;align-items:center;justify-content:center;'>{inner}</div></div>")


def _seal(x, y, size, ico):
    return (f"<div style='{ab(x, y, size, size)}border-radius:47% 53% 50% 50%;background:radial-gradient(circle at 35% 30%,#F08A72,{LT_CORAL} 55%,#B9472F);"
            f"box-shadow:0 8px 16px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;'>"
            f"<div style='width:{int(size * .72)}px;height:{int(size * .72)}px;border-radius:50%;border:3px solid rgba(255,255,255,.35);display:flex;"
            f"align-items:center;justify-content:center;'><svg viewBox='0 0 200 200' width='{int(size * .5)}' height='{int(size * .5)}' "
            f"style='filter:grayscale(1) brightness(2.2);opacity:.85;'>{E.SPOTS[ico]}</svg></div></div>")


def _lines(x, y, w, n, gap=34, c="#D9D2C2"):
    return "".join(f"<div style='{ab(x, y + k * gap, int(w * (0.62 if k == n - 1 else 1)), 10)}border-radius:5px;background:{c};'></div>"
                   for k in range(n))


def letter_cover(g):
    t = _lt_bg() + logo(False) + kick(g["kicker"], "#CFE3E6")
    t += (f"<div style='{ab(56, 196, 540)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:70px;line-height:1.04;letter-spacing:-2px;color:#fff;\">{g['title_pre']}</div>"
          f"<div style=\"{SERIF}font-size:122px;line-height:1.0;color:{LT_GOLD};\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:70px;line-height:1.04;letter-spacing:-2px;color:#fff;\">{g['title_post']}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:30px;line-height:1.3;color:#CFE3E6;margin-top:22px;\">{g['sub']}</div></div>")
    # letter sliding out of an envelope
    sheet = (f"<div style='{ab(620, 190, 410, 560)}transform:rotate(4deg);background:{LT_PAPER};border-radius:6px;"
             f"box-shadow:0 22px 40px rgba(0,0,0,.35);'>"
             f"<div style='{ab(36, 40, 120, 12)}border-radius:6px;background:{LT_GOLD};'></div>"
             + _lines(36, 100, 200, 2, 26) + _lines(36, 190, 338, 5) + _lines(36, 370, 338, 3)
             + f"<svg style='{ab(36, 480)}' width='200' height='50' viewBox='0 0 200 50'><path d='M4 34 C 30 4, 44 46, 70 22 S 110 10, 128 30 "
             f"S 170 34, 196 12' fill='none' stroke='{LT_INK}' stroke-width='4' stroke-linecap='round'/></svg></div>")
    env = (f"<svg style='{ab(580, 640)}' width='470' height='330' viewBox='0 0 470 330'>"
           f"<rect x='4' y='4' width='462' height='322' rx='14' fill='#F1E8D6'/>"
           f"<path d='M4 18 L235 196 L466 18' fill='none' stroke='#D8CBB0' stroke-width='5'/>"
           f"<path d='M4 322 L190 160 M466 322 L280 160' stroke='#E3D6BC' stroke-width='5'/></svg>")
    t += sheet + env + _seal(770, 790, 110, "star")
    t += (f"<div style='{ab(56, 700, 470, 420)}border-radius:26px;border:8px solid {LT_PAPER};box-sizing:border-box;"
          f"background:url({photo(g['cover_photo'])}) center/cover;box-shadow:0 22px 40px rgba(0,0,0,.35);'></div>")
    n, lab = g["badge"]
    t += _stamp(420, 600, 180, 220,
                f"<div style=\"{SERIF}font-size:96px;line-height:.9;color:{LT_BG};\">{n}</div>"
                f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:4px;color:{LT_CORAL};\">{lab}</div>", rot=-7)
    return t + E.footer(g["cta_url"], ink="#fff", swipe_ink=LT_GOLD)


def letter_step(g, i):
    s = g["steps"][i]
    t = _lt_bg() + logo(False) + kick(step_label(g, i, "paragraph"), "#CFE3E6")
    pts = "".join(f"<div style='display:flex;gap:20px;align-items:baseline;padding:26px 0;border-bottom:2px solid #E7DFCD;'>"
                  f"<span style=\"flex:none;{SERIF}font-size:46px;color:{LT_GOLD};width:30px;\">{k + 1}</span>"
                  f"<span style=\"font-family:Inter;font-weight:600;font-size:37px;line-height:1.3;color:{LT_INK};\">{p}</span></div>"
                  for k, p in enumerate(s["points"]))
    inner = (f"<div style=\"{ab(64, 56)}font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:4px;color:{LT_BG};\">"
             f"{step_label(g, i, 'paragraph')}</div>"
             f"<div style=\"{ab(64, 108, 700)}font-family:IWSerif;font-size:88px;line-height:1.04;color:{LT_INK};\">"
             f"{hi_wrap(s['title'], s.get('hi'), SERIF + f'color:{LT_CORAL};')}</div>"
             f"<div style='{ab(64, 330, 120, 6)}border-radius:3px;background:{LT_GOLD};'></div>"
             f"<div style='{ab(64, 360, 840)}'>{pts}</div>"
             f"<div style='{ab(64, 760, 840)}display:flex;gap:18px;align-items:baseline;'>"
             f"<span style=\"flex:none;{SERIF}font-size:48px;color:{LT_CORAL};\">P.S.</span>"
             f"<span style=\"{SERIF}font-size:38px;line-height:1.3;color:{LT_INK};\">{s['tip']}</span></div>")
    t += (f"<div style='{ab(56, 168, 968, 960)}transform:rotate(-0.5deg);background:{LT_PAPER};border-radius:6px;"
          f"box-shadow:0 26px 46px rgba(0,0,0,.35);'>{inner}</div>")
    t += _stamp(840, 200, 150, 180, f"<svg viewBox='0 0 200 200' width='96' height='96'>{E.SPOTS[s['icon']]}</svg>",
                color=[LT_GOLD, LT_CORAL, "#5FA7E5", "#7FB89A", LT_GOLD][i % 5], rot=5)
    return t + E.footer(g["cta_url"], ink="#fff", swipe_ink=LT_GOLD)


def letter_cta(g):
    t = _lt_bg() + logo(False)
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), SERIF + f"color:{LT_GOLD};")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.04;letter-spacing:-3px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 400, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:#CFE3E6;\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='display:flex;gap:22px;align-items:baseline;padding:13px 0;border-bottom:2px solid #E7DFCD;'>"
                   f"<span style=\"{SERIF}font-size:40px;color:{LT_GOLD};width:34px;\">{k + 1}</span>"
                   f"<span style=\"font-family:Inter;font-weight:800;font-size:31px;color:{LT_INK};\">{s['title']}</span></div>"
                   for k, s in enumerate(g["steps"]))
    t += (f"<div style='{ab(56, 488, 968, 560)}transform:rotate(-0.6deg);background:{LT_PAPER};border-radius:6px;"
          f"box-shadow:0 22px 40px rgba(0,0,0,.35);'><div style='{ab(56, 40, 700)}'>{rows}</div></div>")
    t += _seal(860, 900, 130, g.get("cta_icon", "mail"))
    return t + pill("Post your internship at", g["cta_url"], LT_GOLD, LT_INK, y=1150, shadow="8px 8px 0 #fff")


# =====================================================================================
#  BOARD GAME - intern to hire is a game you win square by square
# =====================================================================================
G_BG, G_INK, G_CREAM = "#BFE6CF", "#1E1B3A", "#FFF6E2"
G_SQ = ["#FF6B6B", "#FFB120", "#5FA7E5", "#7FDBB6", "#B58BEA"]


def _g_bg():
    return (f"<div style='position:absolute;inset:0;background:{G_BG};"
            f"background-image:radial-gradient(rgba(30,27,58,.10) 2.5px,transparent 2.5px);background-size:30px 30px;'></div>")


def _pawn(x, y, c, s=1.0):
    w, h = int(56 * s), int(84 * s)
    return (f"<svg style='{ab(x, y)}' width='{w}' height='{h}' viewBox='0 0 56 84'>"
            f"<ellipse cx='28' cy='76' rx='26' ry='7' fill='{G_INK}' opacity='.25'/>"
            f"<path d='M10 74 C 12 56, 20 46, 22 40 L34 40 C 36 46, 44 56, 46 74 Z' fill='{c}' stroke='{G_INK}' stroke-width='3.5'/>"
            f"<circle cx='28' cy='24' r='15' fill='{c}' stroke='{G_INK}' stroke-width='3.5'/>"
            f"<circle cx='23' cy='19' r='4' fill='#fff' opacity='.7'/></svg>")


def _dice(x, y, size, rot=-10, face=5):
    pips = {5: [(25, 25), (75, 25), (50, 50), (25, 75), (75, 75)], 3: [(25, 25), (50, 50), (75, 75)]}[face]
    return (f"<svg style='{ab(x, y)}transform:rotate({rot}deg);' width='{size}' height='{size}' viewBox='0 0 100 100'>"
            f"<rect x='5' y='5' width='90' height='90' rx='20' fill='#fff' stroke='{G_INK}' stroke-width='5'/>"
            + "".join(f"<circle cx='{px}' cy='{py}' r='8' fill='{G_INK}'/>" for px, py in pips) + "</svg>")


def _sq(x, y, sz, c, label="", fs=22, extra=""):
    return (f"<div style=\"{ab(x, y, sz, sz)}background:{c};border:4px solid {G_INK};border-radius:14px;box-sizing:border-box;"
            f"display:flex;align-items:center;justify-content:center;font-family:'DM Sans';font-weight:800;font-size:{fs}px;"
            f"letter-spacing:2px;color:{G_INK};{extra}\">{label}</div>")


def boardgame_cover(g):
    t = _g_bg() + logo() + kick(g["kicker"], G_INK)
    t += (f"<div style='{ab(56, 196, 968)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:84px;line-height:1.02;letter-spacing:-3px;color:{G_INK};\">{g['title_pre']}</div>"
          f"<div style=\"{SERIF}font-size:136px;line-height:1.0;color:#E2483F;\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:84px;line-height:1.02;letter-spacing:-3px;color:{G_INK};\">{g['title_post']}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:30px;color:{G_INK};opacity:.75;margin-top:16px;\">{g['sub']}</div></div>")
    # board: a cream panel with a snaking path of squares from START to HIRED
    t += (f"<div style='{ab(40, 700, 640, 500)}background:{G_CREAM};border:5px solid {G_INK};border-radius:30px;"
          f"box-shadow:10px 10px 0 {G_INK};'></div>")
    path = [(70, 1080), (172, 1080), (274, 1080), (376, 1080), (478, 1080), (560, 990), (478, 900), (376, 900), (274, 900),
            (172, 900), (110, 800), (212, 760)]
    for k, (x, y) in enumerate(path[:-1]):
        lab = "START" if k == 0 else ""
        t += _sq(x, y, 96, G_SQ[k % len(G_SQ)] if k else "#fff", lab, 17)
    hx, hy = path[-1]
    t += _sq(hx, hy - 10, 150, "#FFD54A", "HIRED", 26, "box-shadow:6px 6px 0 " + G_INK + ";")
    t += _pawn(290, 1050, "#5FA7E5") + _pawn(190, 868, "#FF6B6B", 1.1)
    t += _dice(470, 740, 120, -12) + _dice(560, 800, 90, 14, 3)
    # move card with the photo
    t += (f"<div style='{ab(712, 590, 320, 450)}transform:rotate(6deg);background:#fff;border:5px solid {G_INK};border-radius:24px;"
          f"box-shadow:10px 10px 0 {G_INK};overflow:hidden;'>"
          f"<div style=\"height:64px;background:#E2483F;display:flex;align-items:center;justify-content:center;font-family:'DM Sans';"
          f"font-weight:800;font-size:22px;letter-spacing:5px;color:#fff;\">{g['badge'][0]} {g['badge'][1]}</div>"
          f"<div style='margin:16px;height:346px;border-radius:14px;background:url({photo(g['cover_photo'])}) center/cover;'></div></div>")
    return t + E.footer(g["cta_url"], ink=G_INK, swipe_ink="#E2483F")


def boardgame_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    t = _g_bg() + logo() + kick(step_label(g, i, "move"), G_INK)
    t += (f"<div style=\"{ab(56, 186, 968)}font-family:Inter;font-weight:900;font-size:80px;line-height:1.02;letter-spacing:-3px;"
          f"color:{G_INK};\">{hi_wrap(s['title'], s.get('hi'), SERIF + 'color:#E2483F;')}</div>")
    sz, gap = 150, (968 - 150 * n) // max(n - 1, 1)
    for k in range(n):
        x = 56 + k * (sz + gap)
        c = G_SQ[k % len(G_SQ)]
        if k < i:
            lab = check(G_INK, 56, 4)
            t += _sq(x, 440, sz, c, lab, extra="opacity:.85;")
        elif k == i:
            t += _sq(x, 440, sz, c, f"<span style='font-family:Inter;font-weight:900;font-size:70px;'>{k + 1}</span>",
                     extra=f"box-shadow:8px 8px 0 {G_INK};transform:translateY(-10px);")
            t += _pawn(x + 47, 356, "#fff", 1.0)
        else:
            t += _sq(x, 440, sz, "#fff", f"<span style='font-family:Inter;font-weight:900;font-size:58px;opacity:.35;'>{k + 1}</span>",
                     extra="border-style:dashed;")
        if k < n - 1:
            t += (f"<div style='{ab(x + sz + 8, 510, gap - 16, 8)}background-image:linear-gradient(90deg,{G_INK} 50%,transparent 50%);"
                  f"background-size:16px 8px;opacity:.5;'></div>")
    pts = "".join(f"<div style='display:flex;gap:16px;align-items:flex-start;margin-bottom:22px;'>"
                  f"<span style='flex:none;width:40px;height:40px;border-radius:50%;background:{G_SQ[i % len(G_SQ)]};border:3px solid {G_INK};"
                  f"display:flex;align-items:center;justify-content:center;margin-top:2px;'>{check(G_INK, 22, 4)}</span>"
                  f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;line-height:1.25;color:{G_INK};\">{p}</span></div>"
                  for p in s["points"])
    t += (f"<div style='{ab(56, 650, 968, 420)}background:#fff;border:5px solid {G_INK};border-radius:30px;box-shadow:10px 10px 0 {G_INK};overflow:hidden;'>"
          f"<div style=\"height:66px;background:{G_INK};display:flex;align-items:center;padding:0 30px;font-family:'DM Sans';font-weight:800;"
          f"font-size:22px;letter-spacing:5px;color:#fff;\">YOUR MOVE</div>"
          f"<div style='{ab(26, 92, 300, 300)}border-radius:18px;background:url({photo(s['photo'])}) center/cover;border:4px solid {G_INK};box-sizing:border-box;'></div>"
          f"<div style='{ab(360, 100, 570)}'>{pts}</div></div>")
    t += icon(s["icon"], 116, 892, 600, "#fff", border=f"5px solid {G_INK}")
    t += (f"<div style='{ab(56, 1106, 968)}display:flex;gap:22px;align-items:center;background:{G_INK};border-radius:22px;padding:18px 28px;box-sizing:border-box;'>"
          f"<svg width='54' height='54' viewBox='0 0 100 100' style='flex:none;'><rect x='5' y='5' width='90' height='90' rx='20' fill='#fff'/>"
          f"<circle cx='30' cy='30' r='9' fill='{G_INK}'/><circle cx='70' cy='70' r='9' fill='{G_INK}'/></svg>"
          f"<span style=\"font-family:Inter;font-weight:700;font-size:27px;line-height:1.28;color:#fff;\">{s['tip']}</span></div>")
    return t + E.footer(g["cta_url"], ink=G_INK, swipe_ink="#E2483F")


def boardgame_cta(g):
    t = (f"<div style='position:absolute;inset:0;background:{G_INK};"
         f"background-image:radial-gradient(rgba(255,255,255,.07) 2.5px,transparent 2.5px);background-size:30px 30px;'></div>" + logo(False))
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), SERIF + "color:#FFD54A;")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.04;letter-spacing:-3px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 400, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:#C9C6E6;\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='display:flex;align-items:center;gap:22px;margin-bottom:16px;'>"
                   + _sq(0, 0, 78, G_SQ[k % len(G_SQ)], f"<span style='font-family:Inter;font-weight:900;font-size:34px;'>{k + 1}</span>",
                         extra="position:relative;left:0;top:0;flex:none;border-color:#fff;")
                   + f"<span style=\"font-family:Inter;font-weight:800;font-size:32px;color:#fff;\">{s['title']}</span></div>"
                   for k, s in enumerate(g["steps"]))
    t += f"<div style='{ab(56, 484, 968)}'>{rows}</div>"
    t += _sq(820, 860, 170, "#FFD54A", "HIRED", 30, "border-color:#fff;box-shadow:8px 8px 0 #fff;transform:rotate(6deg);")
    return t + pill("Post your internship at", g["cta_url"], "#FFD54A", G_INK, y=1150, shadow="8px 8px 0 #fff")


WORLDS_C = {
    "chat": (chat_cover, chat_step, chat_cta),
    "rolodex": (rolodex_cover, rolodex_step, rolodex_cta),
    "chalkboard": (chalkboard_cover, chalkboard_step, chalkboard_cta),
    "letter": (letter_cover, letter_step, letter_cta),
    "boardgame": (boardgame_cover, boardgame_step, boardgame_cta),
}
