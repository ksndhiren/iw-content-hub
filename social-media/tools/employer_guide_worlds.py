"""Alternative design worlds for the employer guide lane, so each guide in a week
has its own look and layout. lane_employer_guide.py keeps the original
"playbook" world; a spec picks its world with `"world": "<name>"`.

    document   - a job description page on a desk: ruled lines, divider tabs, red-pen notes
    pipeline   - dark recruiting dashboard: stage tracker, app windows, toggle checklist
    editorial  - magazine spread: full-bleed photos, giant numerals, three-column copy
    pop        - bright startup stickers: blob photos, speech bubbles, hard shadows
"""
import math
import lanes_common as L
import lane_employer_guide as E

NAVY, DEEP, AMBER, CORAL, TEAL, SKY, CREAM = E.NAVY, E.DEEP, E.AMBER, E.CORAL, E.TEAL, E.SKY, E.CREAM
MONO = "'Courier New',Courier,monospace"
photo = E.photo


def ab(x, y, w=None, h=None, extra=""):
    s = f"position:absolute;left:{x}px;top:{y}px;"
    if w is not None:
        s += f"width:{w}px;"
    if h is not None:
        s += f"height:{h}px;"
    return s + extra


def pill(text_pre, url, bg, ink, x=56, y=1150, shadow=None, border=None):
    sh = f"box-shadow:{shadow};" if shadow else ""
    bd = f"border:{border};" if border else ""
    return (f"<div style='{ab(x, y)}display:inline-flex;align-items:center;gap:16px;height:96px;padding:0 40px;"
            f"border-radius:48px;background:{bg};{sh}{bd}'>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:24px;color:{ink};\">{text_pre}</span>"
            f"<span style=\"font-family:Inter;font-weight:900;font-size:32px;color:{ink};\">{url}</span>"
            f"<svg width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='{ink}' stroke-width='3' stroke-linecap='round' "
            f"stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>")


def hi_wrap(text, hi, style):
    if hi and hi in text:
        a, b = text.split(hi, 1)
        return f"{a}<span style=\"{style}\">{hi}</span>{b}"
    return text


def check(color, sz=22, sw=3.6):
    return (f"<svg width='{sz}' height='{sz}' viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='{sw}' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M4 12.5l5 5 11-11'/></svg>")


# =====================================================================================
#  DOCUMENT  - the guide is the job description itself, being written on a desk
# =====================================================================================
DESK, RULE, PEN = "#DCE6EF", "#C9D7E4", "#E5484D"


def _desk():
    return (f"<div style='position:absolute;inset:0;background:{DESK};'></div>"
            f"<div style='position:absolute;inset:0;background-image:radial-gradient(rgba(14,33,65,.10) 2px,transparent 2px);"
            f"background-size:28px 28px;'></div>")


def _paperclip(x, y, rot=0):
    return (f"<svg style='{ab(x, y)}transform:rotate({rot}deg);z-index:5;' width='54' height='130' viewBox='0 0 54 130'>"
            f"<path d='M38 30v66a14 14 0 0 1-28 0V22a10 10 0 0 1 20 0v70a5 5 0 0 1-10 0V34' fill='none' stroke='#8D99A8' "
            f"stroke-width='6' stroke-linecap='round'/></svg>")


def _clipped_photo(pid, x, y, w, h, rot=3):
    return (f"<div style='{ab(x, y, w, h)}transform:rotate({rot}deg);background:#fff;padding:10px;"
            f"box-shadow:0 10px 24px rgba(14,33,65,.22);'>"
            f"<div style='width:100%;height:100%;background:url({photo(pid)}) center/cover;'></div></div>"
            + _paperclip(x + w - 70, y - 44, rot + 4))


def _stamp(text, x, y, rot=-12, size=40, color=PEN):
    return (f"<div style=\"{ab(x, y)}transform:rotate({rot}deg);padding:14px 26px;border:5px solid {color};border-radius:12px;"
            f"outline:2px solid {color};outline-offset:5px;font-family:{MONO};font-weight:700;font-size:{size}px;letter-spacing:4px;"
            f"color:{color};opacity:.88;\">{text}</div>")


def _pen_arrow(x, y, w, h, path):
    return (f"<svg style='{ab(x, y)}overflow:visible;' width='{w}' height='{h}'>"
            f"<defs><marker id='pa{x}{y}' markerWidth='12' markerHeight='12' refX='6' refY='6' orient='auto'>"
            f"<path d='M0 0L12 6L0 12' fill='none' stroke='{PEN}' stroke-width='2.6' stroke-linecap='round'/></marker></defs>"
            f"<path d='{path}' fill='none' stroke='{PEN}' stroke-width='4' stroke-linecap='round' marker-end='url(#pa{x}{y})'/></svg>")


def doc_cover(g):
    t = _desk() + f"<img src='{L.DARKLOGO}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
    t += (f"<div style=\"position:absolute;right:56px;top:78px;font-family:{MONO};font-weight:700;font-size:22px;"
          f"letter-spacing:3px;color:{NAVY};\">{g['kicker']}</div>")
    # the page
    t += (f"<div style='{ab(70, 190, 940, 1040)}background:#fff;transform:rotate(-1deg);box-shadow:0 30px 60px rgba(14,33,65,.20);'>"
          f"<div style='position:absolute;left:70px;top:0;bottom:0;width:3px;background:rgba(229,72,77,.35);'></div>"
          f"<div style=\"{ab(110, 64)}font-family:{MONO};font-weight:700;font-size:22px;letter-spacing:5px;color:#7A8797;\">"
          f"JOB DESCRIPTION</div>"
          f"<div style='{ab(110, 104, 520, 3)}background:{NAVY};'></div>"
          f"<div style='{ab(110, 150, 520)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:80px;line-height:1;letter-spacing:-2.6px;color:{NAVY};\">{g['title_pre']}</div>"
          f"<div style=\"font-family:IWSerif;font-style:italic;font-size:84px;line-height:1.02;color:{PEN};margin-top:8px;width:470px;\">{g['title_hi']}</div>"
          f"<div style='position:relative;display:inline-block;margin-top:10px;'>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:80px;line-height:1;letter-spacing:-2.6px;color:{NAVY};\">{g['title_post']}</span>"
          f"<svg style='position:absolute;left:-26px;top:-20px;overflow:visible;' width='460' height='130' viewBox='0 0 460 130'>"
          f"<path d='M40 18C150 -6 420 2 440 52 456 104 250 124 120 116 20 110 -4 70 18 40 34 18 90 10 150 8' fill='none' "
          f"stroke='{PEN}' stroke-width='5' stroke-linecap='round'/></svg></div>"
          f"<div style=\"font-family:{MONO};font-weight:700;font-size:28px;color:{NAVY};margin-top:34px;\">{g['sub']}</div></div>")
    # blank form fields
    fields = ["Role", "Team", "Dates", "Apply by"]
    t += "".join(f"<div style='{ab(110, 640 + k * 74, 470)}display:flex;align-items:flex-end;gap:14px;'>"
                 f"<span style=\"font-family:{MONO};font-weight:700;font-size:26px;color:#7A8797;\">{f}:</span>"
                 f"<span style='flex:1;border-bottom:3px dotted #9FB0C2;height:28px;'></span></div>" for k, f in enumerate(fields))
    t += "</div>"
    t += _clipped_photo(g["cover_photo"], 650, 350, 320, 390, 4)
    t += _clipped_photo(g["cover_inset"], 680, 790, 280, 250, -3)
    n, lab = g["badge"]
    t += _stamp(f"{n} {lab}", 650, 1090, -9, 38)
    t += (f"<div style=\"{ab(700, 262)}transform:rotate(-4deg);font-family:IWSerif;font-style:italic;font-size:36px;color:{PEN};\">"
          f"copy &amp; adapt</div>" + _pen_arrow(660, 286, 40, 60, "M34 4 Q 0 10 6 50"))
    return t + E.footer(g["cta_url"], ink=NAVY)


def _tabs(i, n):
    t = ""
    for k in range(n):
        on = k == i
        bg = PEN if on else ("#AFC2D5" if k < i else "#EEF3F8")
        tc = "#fff" if on else NAVY
        t += (f"<div style='{ab(900, 196 + k * 168, 130 if on else 108, 156)}background:{bg};border-radius:0 14px 14px 0;"
              f"box-shadow:0 6px 14px rgba(14,33,65,.12);display:flex;align-items:center;justify-content:flex-end;padding-right:16px;'>"
              f"<span style=\"font-family:{MONO};font-weight:700;font-size:26px;color:{tc};\">{k + 1:02d}</span></div>")
    return t


def doc_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    t = _desk() + f"<img src='{L.DARKLOGO}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
    t += (f"<div style=\"position:absolute;right:56px;top:80px;font-family:{MONO};font-weight:700;font-size:24px;"
          f"letter-spacing:3px;color:{NAVY};\">{g.get('unit', 'part').upper()} {i + 1:02d} / {n:02d}</div>")
    t += _tabs(i, n)
    rows = "".join(f"<div style='display:flex;gap:20px;align-items:flex-start;padding:20px 0 18px;border-bottom:3px solid {RULE};'>"
                   f"<span style='flex:none;width:38px;height:38px;border:3px solid {NAVY};border-radius:6px;position:relative;margin-top:2px;'>"
                   f"<svg style='position:absolute;left:-2px;top:-12px;' width='46' height='46' viewBox='0 0 24 24' fill='none' "
                   f"stroke='{PEN}' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'><path d='M4 12.5l5 5 13-14'/></svg></span>"
                   f"<span style=\"font-family:Inter;font-weight:600;font-size:29px;line-height:1.28;color:{NAVY};\">{p}</span></div>"
                   for p in s["points"])
    t += (f"<div style='{ab(60, 176, 860, 1080)}background:#fff;box-shadow:0 26px 50px rgba(14,33,65,.18);'>"
          f"<div style='position:absolute;left:62px;top:0;bottom:0;width:3px;background:rgba(229,72,77,.35);'></div>"
          f"<div style=\"{ab(96, 60)}font-family:{MONO};font-weight:700;font-size:22px;letter-spacing:5px;color:#7A8797;\">"
          f"SECTION {i + 1:02d}</div>"
          f"<div style=\"{ab(96, 104, 470)}font-family:Inter;font-weight:900;font-size:70px;line-height:1.02;letter-spacing:-2.4px;color:{NAVY};\">"
          f"{E.marker(s['title'], s.get('hi'), '#FFD873')}</div>"
          f"<div style='{ab(96, 404, 700)}'>"
          f"<div style=\"font-family:{MONO};font-weight:700;font-size:24px;letter-spacing:4px;color:{PEN};\">{g.get('points_label', 'WHAT TO WRITE')}:</div>"
          f"{rows}</div>"
          f"<svg style='{ab(650, 880)}' width='150' height='150' viewBox='0 0 200 200'>{E.SPOTS[s['icon']]}</svg>"
          f"</div>")
    t += _clipped_photo(s["photo"], 610, 196, 270, 300, 4)
    # red-pen margin note
    t += (f"<div style=\"{ab(150, 1000, 520)}transform:rotate(-2deg);font-family:IWSerif;font-style:italic;font-size:33px;"
          f"line-height:1.22;color:{PEN};\"><span style=\"font-family:{MONO};font-style:normal;font-weight:700;font-size:22px;"
          f"letter-spacing:3px;\">TIP &#8594; </span>{s['tip']}</div>")
    return t + E.footer(g["cta_url"], ink=NAVY)


def doc_cta(g):
    t = _desk() + f"<img src='{L.DARKLOGO}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
    ch = g.get("cta_hi", "")
    q = hi_wrap(g["cta_title"], ch, f"font-family:IWSerif;font-style:italic;font-weight:400;color:{PEN};letter-spacing:0;")
    rows = "".join(f"<div style='display:flex;align-items:baseline;gap:14px;padding:12px 0;'>"
                   f"<span style=\"font-family:{MONO};font-weight:700;font-size:26px;color:{PEN};\">{k + 1:02d}</span>"
                   f"<span style=\"font-family:Inter;font-weight:800;font-size:29px;color:{NAVY};\">{s['title']}</span>"
                   f"<span style='flex:1;border-bottom:3px dotted #9FB0C2;'></span>{check(PEN, 30, 3.4)}</div>"
                   for k, s in enumerate(g["steps"]))
    t += (f"<div style='{ab(70, 170, 940, 940)}background:#fff;transform:rotate(.8deg);box-shadow:0 30px 60px rgba(14,33,65,.2);'>"
          f"<div style=\"{ab(70, 64, 800)}font-family:Inter;font-weight:900;font-size:76px;line-height:1.02;letter-spacing:-2.4px;color:{NAVY};\">{q}</div>"
          f"<div style=\"{ab(70, 254, 800)}font-family:{MONO};font-weight:700;font-size:26px;line-height:1.3;color:#5A6878;\">{g['cta_sub']}</div>"
          f"<div style='{ab(70, 370, 520)}'><div style=\"font-family:{MONO};font-weight:700;font-size:22px;letter-spacing:5px;color:#7A8797;"
          f"padding-bottom:8px;border-bottom:3px solid {NAVY};\">CONTENTS</div>{rows}</div></div>")
    t += _clipped_photo(g["steps"][-1]["photo"], 730, 560, 250, 320, 5)
    t += _stamp("READY TO POST", 640, 960, -10, 34)
    return t + pill("Post your internship at", g["cta_url"], AMBER, DEEP, y=1170, shadow=f"8px 8px 0 {NAVY}")


# =====================================================================================
#  PIPELINE  - a dark recruiting dashboard
# =====================================================================================
PBG, PANEL, PLINE, MINT, PTXT, PMUT = "#08191D", "#10292F", "rgba(255,255,255,.10)", "#3EE6B0", "#EAF6F3", "#8FB3AE"
P_ICON = {"clipboard": "clipboard", "chart": "trend", "bulb": "bulb", "users": "users", "pen": "doc", "mail": "chat",
          "target": "target", "star": "star", "calendar": "calendar", "flag": "flag", "handshake": "handshake",
          "heart": "heart", "rocket": "rocket", "magnifier": "search", "idcard": "user", "megaphone": "chat", "phone": "chat"}


def _pbg():
    return (f"<div style='position:absolute;inset:0;background:{PBG};'></div>"
            f"<div style='position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.06) 1.6px,transparent 1.6px);"
            f"background-size:30px 30px;'></div>"
            f"<div style='position:absolute;right:-260px;top:-260px;width:820px;height:820px;border-radius:50%;"
            f"background:radial-gradient(rgba(62,230,176,.20),transparent 65%);'></div>")


def _window(pid, x, y, w, h, label="Review", pos="center"):
    br = "".join(f"<div style='{ab(bx, by, 46, 46)}border-{a}:5px solid {MINT};border-{b}:5px solid {MINT};'></div>"
                 for bx, by, a, b in [(26, 70, "top", "left"), (w - 72, 70, "top", "right"),
                                      (26, h - 72, "bottom", "left"), (w - 72, h - 72, "bottom", "right")])
    return (f"<div style='{ab(x, y, w, h)}border-radius:22px;overflow:hidden;background:{PANEL};border:2px solid {PLINE};"
            f"box-shadow:0 30px 60px rgba(0,0,0,.45);'>"
            f"<div style='height:48px;display:flex;align-items:center;gap:9px;padding:0 20px;background:#0C2227;border-bottom:2px solid {PLINE};'>"
            f"<span style='width:13px;height:13px;border-radius:50%;background:{CORAL};'></span>"
            f"<span style='width:13px;height:13px;border-radius:50%;background:{AMBER};'></span>"
            f"<span style='width:13px;height:13px;border-radius:50%;background:{MINT};'></span>"
            f"<span style=\"margin-left:14px;font-family:'DM Sans';font-weight:700;font-size:18px;letter-spacing:2px;color:{PMUT};\">{label}</span></div>"
            f"<div style='position:absolute;left:0;right:0;top:48px;bottom:0;background:url({photo(pid)}) {pos}/cover;'></div>"
            f"<div style='position:absolute;left:0;right:0;top:48px;bottom:0;background:linear-gradient(rgba(8,25,29,0) 55%,rgba(8,25,29,.55));'></div>"
            f"<div style='position:absolute;left:0;right:0;top:{int(h * .58)}px;height:3px;background:{MINT};"
            f"box-shadow:0 0 18px 4px rgba(62,230,176,.7);opacity:.85;'></div>"
            f"{br}</div>")


def _pfooter(url):
    return E.footer(url, ink=PMUT, swipe_ink=MINT)


def pipe_cover(g):
    t = _pbg() + f"<img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
    t += (f"<div style=\"position:absolute;right:56px;top:74px;display:flex;align-items:center;gap:12px;padding:10px 20px;"
          f"border:2px solid {MINT};border-radius:24px;font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:4px;color:{MINT};\">"
          f"<span style='width:11px;height:11px;border-radius:50%;background:{MINT};box-shadow:0 0 10px {MINT};'></span>{g['kicker']}</div>")
    t += (f"<div style='{ab(56, 196, 968)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:90px;line-height:1;letter-spacing:-3px;color:#fff;\">{g['title_pre']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:122px;line-height:1.02;letter-spacing:-4px;margin-top:4px;"
          f"background:linear-gradient(90deg,{MINT},{SKY});-webkit-background-clip:text;color:transparent;\">{g['title_hi']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:90px;line-height:1;letter-spacing:-3px;color:#fff;margin-top:4px;\">{g['title_post']}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:31px;color:{PMUT};margin-top:24px;\">{g['sub']}</div></div>")
    # funnel
    stages = [("Applications", 470, "#1E4A52"), ("Screened", 400, "#24686A"), ("Shortlist", 326, "#2C9A86"), ("Interview", 250, MINT)]
    for k, (lab, w, c) in enumerate(stages):
        x = 56 + (470 - w) // 2
        tc = PBG if k == 3 else PTXT
        t += (f"<div style='{ab(x, 690 + k * 104, w, 86)}background:{c};border-radius:16px;display:flex;align-items:center;"
              f"justify-content:center;font-family:Inter;font-weight:800;font-size:28px;color:{tc};'>{lab}</div>")
    n, lab = g["badge"]
    t += (f"<div style='{ab(170, 1124)}display:flex;align-items:center;gap:14px;padding:12px 24px;border-radius:30px;background:{PANEL};"
          f"border:2px solid {MINT};'><span style=\"font-family:Inter;font-weight:900;font-size:36px;color:{MINT};\">{n}</span>"
          f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:22px;letter-spacing:4px;color:{PTXT};\">{lab}</span></div>")
    t += _window(g["cover_photo"], 576, 676, 448, 540, "Review")
    return t + _pfooter(g["cta_url"])


def _tracker(i, n):
    x0, x1, y = 86, 994, 210
    seg = (x1 - x0) / (n - 1)
    t = (f"<div style='{ab(x0, y - 2, x1 - x0, 4)}background:{PLINE};'></div>"
         f"<div style='{ab(x0, y - 2, int(seg * i), 4)}background:{MINT};'></div>")
    for k in range(n):
        cx = int(x0 + seg * k)
        if k < i:
            t += (f"<div style='{ab(cx - 22, y - 22, 44, 44)}border-radius:50%;background:{MINT};display:flex;align-items:center;"
                  f"justify-content:center;'>{check(PBG, 22, 3.6)}</div>")
        elif k == i:
            t += (f"<div style='{ab(cx - 34, y - 34, 68, 68)}border-radius:50%;background:{PBG};border:4px solid {MINT};"
                  f"box-shadow:0 0 0 8px rgba(62,230,176,.18),0 0 24px rgba(62,230,176,.5);display:flex;align-items:center;justify-content:center;"
                  f"font-family:Inter;font-weight:900;font-size:28px;color:{MINT};'>{k + 1}</div>")
        else:
            t += (f"<div style='{ab(cx - 22, y - 22, 44, 44)}border-radius:50%;background:{PBG};border:3px solid {PLINE};"
                  f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:20px;color:{PMUT};'>{k + 1}</div>")
    return t


def pipe_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    t = _pbg() + f"<img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
    t += (f"<div style=\"position:absolute;right:56px;top:80px;font-family:'DM Sans';font-weight:800;font-size:22px;"
          f"letter-spacing:4px;color:{MINT};\">STEP {i + 1:02d} / {n:02d}</div>")
    t += _tracker(i, n)
    t += (f"<div style=\"{ab(56, 290, 968)}font-family:Inter;font-weight:900;font-size:76px;line-height:1.02;letter-spacing:-2.6px;color:#fff;\">"
          f"{hi_wrap(s['title'], s.get('hi'), f'color:{MINT};')}</div>")
    t += _window(s["photo"], 56, 470, 470, 540, f"Step {i + 1}")
    ic = P_ICON.get(s["icon"], "check")
    t += (f"<div style='{ab(440, 924, 112, 112)}border-radius:28px;background:{MINT};display:flex;align-items:center;justify-content:center;"
          f"box-shadow:0 14px 30px rgba(0,0,0,.45);border:5px solid {PBG};'>{L.svg(ic, PBG, 56)}</div>")
    rows = "".join(f"<div style='display:flex;gap:18px;align-items:center;margin-top:16px;padding:20px 22px;background:{PANEL};"
                   f"border:2px solid {PLINE};border-radius:18px;'>"
                   f"<span style='flex:none;width:58px;height:32px;border-radius:16px;background:{MINT};position:relative;'>"
                   f"<span style='position:absolute;right:4px;top:4px;width:24px;height:24px;border-radius:50%;background:{PBG};'></span></span>"
                   f"<span style=\"font-family:Inter;font-weight:700;font-size:25px;line-height:1.26;color:{PTXT};\">{p}</span></div>"
                   for p in s["points"])
    t += (f"<div style='{ab(566, 470, 458)}'>"
          f"<div style=\"display:flex;justify-content:space-between;font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:4px;color:{PMUT};\">"
          f"<span>CHECKLIST</span><span style='color:{MINT};'>{len(s['points'])} ITEMS</span></div>{rows}</div>")
    t += (f"<div style='{ab(56, 1068, 968)}display:flex;gap:22px;align-items:flex-start;padding:24px 30px;background:{PANEL};"
          f"border-left:7px solid {MINT};border-radius:8px 18px 18px 8px;'>"
          f"<span style='flex:none;margin-top:2px;'>{L.svg('bulb', MINT, 36)}</span>"
          f"<div><div style=\"font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:4px;color:{MINT};\">NOTE</div>"
          f"<div style=\"font-family:Inter;font-weight:700;font-size:27px;line-height:1.26;color:{PTXT};margin-top:6px;\">{s['tip']}</div></div></div>")
    return t + _pfooter(g["cta_url"])


def pipe_cta(g):
    t = _pbg() + f"<img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), f"color:{MINT};")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:86px;line-height:1.02;letter-spacing:-3px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 400, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:{PMUT};\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='display:flex;align-items:center;gap:16px;padding:15px 0;border-bottom:2px solid {PLINE};'>"
                   f"<span style='flex:none;width:36px;height:36px;border-radius:50%;background:{MINT};display:flex;align-items:center;"
                   f"justify-content:center;'>{check(PBG, 20, 3.8)}</span>"
                   f"<span style=\"font-family:Inter;font-weight:800;font-size:27px;color:{PTXT};flex:1;\">{s['title']}</span>"
                   f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:17px;letter-spacing:3px;color:{MINT};\">DONE</span></div>"
                   for s in g["steps"])
    t += (f"<div style='{ab(56, 500, 600)}padding:28px 30px 20px;background:{PANEL};border:2px solid {PLINE};border-radius:24px;"
          f"box-shadow:0 30px 60px rgba(0,0,0,.4);'>"
          f"<div style=\"display:flex;justify-content:space-between;font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:4px;color:{PMUT};\">"
          f"<span>YOUR PROCESS</span><span style='color:{MINT};'>{len(g['steps'])}/{len(g['steps'])}</span></div>"
          f"<div style='height:10px;border-radius:5px;background:{MINT};margin:14px 0 6px;'></div>{rows}</div>")
    t += _window(g["steps"][-1]["photo"], 690, 560, 334, 470, "Shortlist")
    return t + pill("Post your internship at", g["cta_url"], MINT, PBG, y=1160)


# =====================================================================================
#  EDITORIAL  - magazine spread
# =====================================================================================
OFF, INK = "#F3EEE4", "#141414"
ED_ACC = [CORAL, AMBER, "#5FBFBE", SKY, "#F28CB1", "#8BCF7A"]


def ed_cover(g):
    t = (f"<div style='position:absolute;inset:0;background:url({photo(g['cover_photo'])}) center/cover;'></div>"
         f"<div style='position:absolute;inset:0;background:linear-gradient(rgba(10,10,10,.55),rgba(10,10,10,0) 22%,rgba(10,10,10,.15) 40%,"
         f"rgba(10,10,10,.88) 62%,rgba(10,10,10,.96));'></div>"
         f"<img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
         f"<div style=\"position:absolute;right:56px;top:72px;font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:5px;color:#fff;"
         f"padding-bottom:10px;border-bottom:3px solid {AMBER};\">{g['kicker']}</div>")
    n, lab = g["badge"]
    t += (f"<div style='position:absolute;left:56px;top:190px;width:190px;height:190px;border-radius:50%;background:{AMBER};"
          f"display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-8deg);'>"
          f"<span style=\"font-family:IWSerif;font-style:italic;font-size:96px;line-height:.9;color:{INK};\">{n}</span>"
          f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:4px;color:{INK};\">{lab}</span></div>")
    t += (f"<div style='position:absolute;left:56px;bottom:130px;width:968px;'>"
          f"<div style=\"font-family:IWSerif;font-size:84px;line-height:1;color:#fff;\">{g['title_pre']}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:200px;line-height:.92;letter-spacing:-8px;color:{AMBER};text-transform:uppercase;\">{g['title_hi']}</div>"
          f"<div style=\"font-family:IWSerif;font-style:italic;font-size:80px;line-height:1.05;color:#fff;\">{g['title_post']}</div>"
          f"<div style='width:120px;height:5px;background:{AMBER};margin:28px 0 20px;'></div>"
          f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:30px;color:rgba(255,255,255,.85);\">{g['sub']}</div></div>")
    return t + E.footer(g["cta_url"], ink="rgba(255,255,255,.85)", swipe_ink=AMBER)


def ed_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    acc = ED_ACC[i % len(ED_ACC)]
    ph = 640
    t = (f"<div style='position:absolute;inset:0;background:{OFF};'></div>"
         f"<div style='{ab(0, 0, 1080, ph)}background:url({photo(s['photo'])}) center/cover;'></div>"
         f"<div style='{ab(0, 0, 1080, 220)}background:linear-gradient(rgba(10,10,10,.55),rgba(10,10,10,0));'></div>"
         f"<div style='{ab(0, ph - 12, 1080, 12)}background:{acc};'></div>"
         f"<img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
         f"<div style=\"position:absolute;right:56px;top:76px;font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:5px;color:#fff;\">"
         f"{g.get('unit', 'benefit').upper()} {i + 1} OF {n}</div>")
    # giant numeral straddling photo and page
    t += (f"<div style=\"position:absolute;right:40px;top:{ph - 210}px;font-family:Inter;font-weight:900;font-size:300px;line-height:1;"
          f"letter-spacing:-14px;color:{acc};-webkit-text-stroke:6px {INK};\">{i + 1:02d}</div>")
    t += (f"<div style='{ab(56, ph + 52, 600)}'>"
          f"<div style=\"display:flex;align-items:center;gap:12px;font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:5px;color:{INK};\">"
          f"<span style='width:14px;height:14px;border-radius:50%;background:{acc};border:2px solid {INK};'></span>{g.get('points_label', 'WHAT IT LOOKS LIKE')}</div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:66px;line-height:1.02;letter-spacing:-2.4px;color:{INK};margin-top:14px;\">"
          f"{hi_wrap(s['title'], s.get('hi'), 'font-family:IWSerif;font-style:italic;font-weight:400;letter-spacing:0;')}</div></div>")
    cols = "".join(f"<div style='flex:1;border-top:4px solid {INK};padding-top:14px;'>"
                   f"<div style=\"font-family:IWSerif;font-style:italic;font-size:40px;line-height:1;color:{INK};\">{k + 1}.</div>"
                   f"<div style=\"font-family:Inter;font-weight:600;font-size:24px;line-height:1.3;color:{INK};margin-top:8px;\">{p}</div></div>"
                   for k, p in enumerate(s["points"]))
    t += f"<div style='{ab(56, 920, 968)}display:flex;gap:34px;'>{cols}</div>"
    t += (f"<div style='{ab(56, 1124, 968)}display:flex;gap:18px;align-items:flex-start;'>"
          f"<span style=\"flex:none;font-family:IWSerif;font-size:110px;line-height:.7;color:{acc};-webkit-text-stroke:2px {INK};\">&#8220;</span>"
          f"<span style=\"font-family:IWSerif;font-style:italic;font-size:33px;line-height:1.22;color:{INK};\">{s['tip']}</span></div>")
    return t + E.footer(g["cta_url"], ink=INK, swipe_ink=INK)


def ed_cta(g):
    t = f"<div style='position:absolute;inset:0;background:{INK};'></div><img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""), f"font-style:italic;color:{AMBER};")
    t += (f"<div style=\"{ab(56, 190, 968)}font-family:IWSerif;font-size:88px;line-height:1.04;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 400, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:rgba(255,255,255,.75);\">{g['cta_sub']}</div>"
          f"<div style=\"{ab(56, 480, 968)}font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:5px;color:{AMBER};"
          f"padding-bottom:12px;border-bottom:2px solid rgba(255,255,255,.25);\">IN THIS GUIDE</div>")
    for k, s in enumerate(g["steps"]):
        x, y = 56 + (k % 2) * 494, 540 + (k // 2) * 196
        t += (f"<div style='{ab(x, y, 474, 172)}display:flex;gap:22px;align-items:center;'>"
              f"<div style='flex:none;width:150px;height:150px;background:url({photo(s['photo'])}) center/cover;"
              f"border-bottom:8px solid {ED_ACC[k % len(ED_ACC)]};'></div>"
              f"<div><div style=\"font-family:Inter;font-weight:900;font-size:44px;line-height:1;color:{ED_ACC[k % len(ED_ACC)]};\">{k + 1:02d}</div>"
              f"<div style=\"font-family:Inter;font-weight:800;font-size:28px;line-height:1.15;color:#fff;margin-top:8px;\">{s['title']}</div></div></div>")
    return t + pill("Post your internship at", g["cta_url"], AMBER, INK, y=1166)


# =====================================================================================
#  POP  - bright startup stickers
# =====================================================================================
BLK = "#151515"
POP_BG = ["#FFC53D", "#8CCBFF", "#B8EE8C", "#FFA9C6", "#C7B6FF", "#FFD873"]
BLOBS = ["58% 42% 46% 54% / 46% 52% 48% 54%", "42% 58% 60% 40% / 54% 40% 60% 46%", "50% 50% 38% 62% / 60% 44% 56% 40%"]


def _blob(pid, x, y, w, h, k=0, rot=0, pos="center"):
    return (f"<div style='{ab(x, y, w, h)}border-radius:{BLOBS[k % 3]};border:6px solid {BLK};box-shadow:14px 14px 0 {BLK};"
            f"background:url({photo(pid)}) {pos}/cover;transform:rotate({rot}deg);'></div>")


def _burst(x, y, size, color, rot, line1, line2, n_pts=14):
    pts = " ".join(f"{100 + (94 if j % 2 == 0 else 74) * math.cos(j * math.pi / n_pts)},"
                   f"{100 + (94 if j % 2 == 0 else 74) * math.sin(j * math.pi / n_pts)}" for j in range(2 * n_pts))
    return (f"<div style='{ab(x, y, size, size)}transform:rotate({rot}deg);'>"
            f"<svg width='{size}' height='{size}' viewBox='0 0 200 200' style='position:absolute;inset:0;overflow:visible;'>"
            f"<polygon points='{pts}' fill='{color}' stroke='{BLK}' stroke-width='6' stroke-linejoin='round'/></svg>"
            f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;'>"
            f"<span style=\"font-family:Inter;font-weight:900;font-size:{int(size * .36)}px;line-height:.9;color:{BLK};\">{line1}</span>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:{int(size * .11)}px;letter-spacing:3px;color:{BLK};\">{line2}</span></div></div>")


STICKER = f"background:#fff;border:5px solid {BLK};border-radius:18px;box-shadow:7px 7px 0 {BLK};"


def pop_cover(g):
    t = (f"<div style='position:absolute;inset:0;background:{CORAL};'></div>"
         + L.dots("right:40px;top:560px;", "rgba(21,21,21,.22)", 300, 220)
         + L.dots("left:30px;top:1150px;", "rgba(255,255,255,.35)", 220, 120)
         + f"<img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>"
         + f"<div style=\"position:absolute;right:56px;top:70px;transform:rotate(3deg);padding:10px 18px;{STICKER}border-radius:14px;"
           f"font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:3px;color:{BLK};\">{g['kicker']}</div>")
    t += (f"<div style='{ab(56, 200, 968)}'>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:96px;line-height:1;letter-spacing:-3.5px;color:{BLK};\">{g['title_pre']}</div>"
          f"<div style='display:flex;align-items:center;gap:26px;margin-top:16px;'>"
          f"<span style=\"display:inline-block;transform:rotate(-3deg);padding:4px 30px 12px;{STICKER}border-radius:26px;"
          f"font-family:Inter;font-weight:900;font-style:italic;font-size:124px;line-height:1;letter-spacing:-4px;color:{BLK};\">{g['title_hi']}</span>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:96px;line-height:1;letter-spacing:-3.5px;color:{BLK};\">{g['title_post'].split(' ', 1)[0]}</span></div>"
          f"<div style=\"font-family:Inter;font-weight:900;font-size:96px;line-height:1;letter-spacing:-3.5px;color:{BLK};margin-top:14px;\">"
          f"{g['title_post'].split(' ', 1)[1] if ' ' in g['title_post'] else ''}</div>"
          f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:31px;color:{BLK};margin-top:22px;\">{g['sub']}</div></div>")
    t += _blob(g["cover_photo"], 470, 690, 540, 520, 0, 3)
    t += _blob(g["cover_inset"], 70, 840, 330, 330, 1, -6)
    n, lab = g["badge"]
    t += _burst(330, 650, 200, AMBER, -12, n, lab)
    t += E.spot("rocket", 860, 610, 150, 10)
    t += E.squiggle(160, 1180, 300, 90, "M10 60 Q 120 0 280 40", c=BLK)
    return t + E.footer(g["cta_url"], ink=BLK, swipe_ink=BLK)


def pop_step(g, i):
    s, n = g["steps"][i], len(g["steps"])
    bg = POP_BG[i % len(POP_BG)]
    flip = i % 2 == 1
    t = (f"<div style='position:absolute;inset:0;background:{bg};'></div>"
         + L.dots(("left:30px;" if flip else "right:30px;") + "top:1010px;", "rgba(21,21,21,.18)", 260, 160)
         + f"<img src='{L.DARKLOGO}' style='{ab(56, 44)}height:{L.LOGO}px;'>")
    t += (f"<div style='position:absolute;right:56px;top:36px;width:120px;height:120px;border-radius:50%;background:{BLK};"
          f"display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(8deg);'>"
          f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:15px;letter-spacing:3px;color:{bg};\">STEP</span>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:50px;line-height:1;color:#fff;\">{i + 1}<span style='font-size:24px;color:{bg};'>/{n}</span></span></div>")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.12;letter-spacing:-3px;color:{BLK};\">"
          f"{hi_wrap(s['title'], s.get('hi'), f'display:inline-block;transform:rotate(-2deg);padding:0 18px 6px;{STICKER}border-radius:20px;')}</div>")
    px, bx = (56, 586) if flip else (556, 56)
    t += _blob(s["photo"], px, 450, 470, 540, i, 2 if not flip else -2)
    t += E.spot(s["icon"], (px + 20) if not flip else (px + 300), 360, 150, -8 if not flip else 8)
    bubbles = ""
    for k, p in enumerate(s["points"]):
        tail_side = "right" if not flip else "left"
        bubbles += (f"<div style='position:relative;margin-top:{0 if k == 0 else 34}px;padding:22px 26px 22px 80px;{STICKER}border-radius:28px;"
                    f"transform:rotate({(-1.5 if k % 2 == 0 else 1.5)}deg);'>"
                    f"<span style='position:absolute;left:20px;top:20px;width:42px;height:42px;border-radius:50%;background:{bg};border:4px solid {BLK};"
                    f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:22px;color:{BLK};'>{k + 1}</span>"
                    f"<span style=\"font-family:Inter;font-weight:700;font-size:27px;line-height:1.25;color:{BLK};\">{p}</span>"
                    f"<svg style='position:absolute;{tail_side}:-30px;top:30px;' width='34' height='30' viewBox='0 0 34 30'>"
                    f"<path d='{'M0 2L32 14L0 26' if not flip else 'M34 2L2 14L34 26'}' fill='#fff' stroke='{BLK}' stroke-width='5' stroke-linejoin='round'/></svg></div>")
    t += f"<div style='{ab(bx, 470, 444)}'>{bubbles}</div>"
    bolt = (f"<svg width='30' height='30' viewBox='0 0 24 24'><path d='M13 2L4 14h7l-1 8 9-12h-7z' fill='{AMBER}'/></svg>")
    t += (f"<div style='{ab(56, 1060, 968)}transform:rotate(-1deg);background:{BLK};border-radius:22px;padding:24px 32px 26px;"
          f"box-shadow:8px 8px 0 rgba(21,21,21,.25);'>"
          f"<div style=\"display:flex;align-items:center;gap:8px;font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:4px;color:{AMBER};\">"
          f"{bolt}QUICK WIN</div>"
          f"<div style=\"font-family:Inter;font-weight:700;font-size:28px;line-height:1.25;color:#fff;margin-top:8px;\">{s['tip']}</div></div>")
    return t + E.footer(g["cta_url"], ink=BLK, swipe_ink=BLK)


def pop_cta(g):
    t = (f"<div style='position:absolute;inset:0;background:{BLK};'></div>"
         + L.dots("right:40px;top:150px;", "rgba(255,255,255,.18)", 240, 160)
         + f"<img src='{L.WHT}' style='{ab(56, 44)}height:{L.LOGO}px;'>")
    q = hi_wrap(g["cta_title"], g.get("cta_hi", ""),
                f"display:inline-block;transform:rotate(-2deg);padding:0 16px 6px;background:{AMBER};color:{BLK};border-radius:18px;")
    t += (f"<div style=\"{ab(56, 196, 968)}font-family:Inter;font-weight:900;font-size:84px;line-height:1.14;letter-spacing:-3px;color:#fff;\">{q}</div>"
          f"<div style=\"{ab(56, 420, 900)}font-family:'DM Sans';font-weight:600;font-size:30px;color:rgba(255,255,255,.75);\">{g['cta_sub']}</div>")
    rows = "".join(f"<div style='display:flex;align-items:center;gap:16px;margin-top:{0 if k == 0 else 14}px;padding:14px 20px;"
                   f"background:{POP_BG[k % len(POP_BG)]};border:4px solid #fff;border-radius:18px;transform:rotate({(-1 if k % 2 == 0 else 1)}deg);'>"
                   f"<span style='flex:none;width:38px;height:38px;border-radius:50%;background:{BLK};display:flex;align-items:center;"
                   f"justify-content:center;'>{check('#fff', 20, 3.8)}</span>"
                   f"<span style=\"font-family:Inter;font-weight:800;font-size:27px;color:{BLK};\">{s['title']}</span></div>"
                   for k, s in enumerate(g["steps"]))
    t += f"<div style='{ab(56, 510, 560)}'>{rows}</div>"
    t += (f"<div style='{ab(660, 540, 370, 470)}border-radius:{BLOBS[1]};border:6px solid #fff;box-shadow:14px 14px 0 {CORAL};"
          f"background:url({photo(g['steps'][-1]['photo'])}) center/cover;transform:rotate(3deg);'></div>")
    t += E.spot(g.get("cta_icon", "rocket"), 880, 920, 150, 8)
    return t + pill("Post your internship at", g["cta_url"], AMBER, BLK, y=1160, shadow=f"8px 8px 0 {CORAL}", border=f"4px solid {BLK}")


WORLDS = {
    "document": (doc_cover, doc_step, doc_cta),
    "pipeline": (pipe_cover, pipe_step, pipe_cta),
    "editorial": (ed_cover, ed_step, ed_cta),
    "pop": (pop_cover, pop_step, pop_cta),
}

# Second bank of worlds (week 25+): transit, swiss, blueprint, kanban, ticket.
from employer_guide_worlds_b import WORLDS_B  # noqa: E402
WORLDS.update(WORLDS_B)
