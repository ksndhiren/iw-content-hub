"""Employer guide lane - practical "hiring an intern" carousels for employers.

Search-led (topics come from what employers Google: "how to hire an intern uk",
"intern job description", ...). Educational, no sales claims, no Nuno. The look
is a "hiring playbook": graph-paper pages, taped Pexels photos, flat vector spot
illustrations, a checklist card and a sticky-note tip per step.

Each guide is one spec in content/employer_guides/<slug>.json; photos live in
assets/employer_guide/<pexels id>.jpg.

    python3 tools/lane_employer_guide.py how-to-hire-an-intern [OUT_DIR]      # preview
    python3 tools/lane_employer_guide.py week week25 <mon-slug> <tue-slug> ...  # into the week
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L

W, H = 1080, 1350
PAPER, NAVY, DEEP = "#F5EFE3", "#0E2141", "#0A1830"
AMBER, CORAL, TEAL, SKY, CREAM = "#FFB120", "#FF6B6B", "#5B9291", "#5FA7E5", "#FFF8EC"
SPECS = os.path.join(L.BASE, "content", "employer_guides")
PHOTOS = os.path.join(L.BASE, "assets", "employer_guide")


def photo(pid):
    return "data:image/jpeg;base64," + L.img(os.path.join(PHOTOS, f"{pid}.jpg")).split(",", 1)[1]


# ---------- vector pieces ----------
SPOTS = {  # flat spot illustrations, viewBox 0 0 200 200
    "target": f"""<circle cx='92' cy='108' r='62' fill='{CORAL}'/><circle cx='92' cy='108' r='44' fill='{CREAM}'/>
      <circle cx='92' cy='108' r='26' fill='{CORAL}'/><circle cx='92' cy='108' r='9' fill='{NAVY}'/>
      <path d='M94 106L162 40' stroke='{NAVY}' stroke-width='7' stroke-linecap='round'/>
      <path d='M150 30l22-4-4 22-12 2-8-8z' fill='{AMBER}' stroke='{NAVY}' stroke-width='4' stroke-linejoin='round'/>""",
    "idcard": f"""<rect x='30' y='52' width='140' height='100' rx='14' fill='{CREAM}' stroke='{NAVY}' stroke-width='6'/>
      <rect x='30' y='52' width='140' height='26' rx='12' fill='{SKY}'/>
      <circle cx='70' cy='108' r='18' fill='{AMBER}' stroke='{NAVY}' stroke-width='4'/>
      <path d='M100 100h50M100 116h36M100 132h44' stroke='{NAVY}' stroke-width='6' stroke-linecap='round'/>
      <circle cx='150' cy='150' r='28' fill='{TEAL}' stroke='{NAVY}' stroke-width='5'/>
      <path d='M137 150l9 9 17-18' stroke='#fff' stroke-width='7' fill='none' stroke-linecap='round' stroke-linejoin='round'/>""",
    "pen": f"""<path d='M48 30h78l28 28v114H48z' fill='{CREAM}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M126 30v28h28' fill='{SKY}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M68 78h56M68 98h66M68 118h40' stroke='{NAVY}' stroke-width='6' stroke-linecap='round'/>
      <g transform='rotate(40 140 130)'><rect x='126' y='78' width='26' height='92' rx='4' fill='{AMBER}' stroke='{NAVY}' stroke-width='5'/>
      <path d='M126 170l13 22 13-22z' fill='{CORAL}' stroke='{NAVY}' stroke-width='5' stroke-linejoin='round'/></g>""",
    "megaphone": f"""<path d='M40 84h30l70-38v108l-70-38H40z' fill='{AMBER}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <rect x='26' y='84' width='24' height='32' rx='6' fill='{SKY}' stroke='{NAVY}' stroke-width='6'/>
      <path d='M66 116l10 40h20l-8-34' fill='{CREAM}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M158 74q16 26 0 52M172 58q28 42 0 84' stroke='{CORAL}' stroke-width='7' fill='none' stroke-linecap='round'/>""",
    "magnifier": f"""<rect x='34' y='34' width='96' height='122' rx='10' fill='{CREAM}' stroke='{NAVY}' stroke-width='6'/>
      <path d='M52 62h60M52 82h60M52 102h40' stroke='{NAVY}' stroke-width='6' stroke-linecap='round'/>
      <circle cx='124' cy='118' r='38' fill='{SKY}' fill-opacity='.55' stroke='{NAVY}' stroke-width='8'/>
      <path d='M151 145l28 28' stroke='{NAVY}' stroke-width='14' stroke-linecap='round'/>
      <path d='M108 106q8-12 22-10' stroke='#fff' stroke-width='6' fill='none' stroke-linecap='round'/>""",
    "rocket": f"""<path d='M100 22c30 20 40 56 32 96H68c-8-40 2-76 32-96z' fill='{CREAM}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <circle cx='100' cy='70' r='16' fill='{SKY}' stroke='{NAVY}' stroke-width='6'/>
      <path d='M68 92l-24 30 30 2zM132 92l24 30-30 2z' fill='{CORAL}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M80 124q20 70 40 0z' fill='{AMBER}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>""",
}

SPOTS.update({
    "bulb": f"""<path d='M100 26a50 50 0 0 0-30 90c8 7 10 14 10 22h40c0-8 2-15 10-22a50 50 0 0 0-30-90z' fill='{AMBER}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <rect x='78' y='142' width='44' height='16' rx='5' fill='{SKY}' stroke='{NAVY}' stroke-width='5'/><rect x='84' y='160' width='32' height='14' rx='5' fill='{SKY}' stroke='{NAVY}' stroke-width='5'/>
      <path d='M88 96l12 14 12-14M100 110v30' stroke='{NAVY}' stroke-width='5' fill='none' stroke-linecap='round' stroke-linejoin='round'/>
      <path d='M30 70l-14-6M170 70l14-6M42 34l-10-10M158 34l10-10' stroke='{CORAL}' stroke-width='7' stroke-linecap='round'/>""",
    "chart": f"""<rect x='28' y='30' width='144' height='140' rx='12' fill='{CREAM}' stroke='{NAVY}' stroke-width='6'/>
      <rect x='50' y='110' width='22' height='40' rx='4' fill='{SKY}' stroke='{NAVY}' stroke-width='4'/><rect x='88' y='86' width='22' height='64' rx='4' fill='{AMBER}' stroke='{NAVY}' stroke-width='4'/>
      <rect x='126' y='60' width='22' height='90' rx='4' fill='{CORAL}' stroke='{NAVY}' stroke-width='4'/>
      <path d='M48 92l40-28 22 14 40-34' stroke='{NAVY}' stroke-width='6' fill='none' stroke-linecap='round' stroke-linejoin='round'/><circle cx='150' cy='44' r='8' fill='{TEAL}' stroke='{NAVY}' stroke-width='4'/>""",
    "users": f"""<circle cx='70' cy='78' r='24' fill='{AMBER}' stroke='{NAVY}' stroke-width='6'/><circle cx='132' cy='78' r='24' fill='{SKY}' stroke='{NAVY}' stroke-width='6'/>
      <path d='M28 160c0-30 18-46 42-46s42 16 42 46z' fill='{CORAL}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M92 160c0-30 16-46 40-46s42 16 42 46z' fill='{TEAL}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>""",
    "calendar": f"""<rect x='30' y='42' width='140' height='128' rx='14' fill='{CREAM}' stroke='{NAVY}' stroke-width='6'/>
      <path d='M30 56a14 14 0 0 1 14-14h112a14 14 0 0 1 14 14v22H30z' fill='{CORAL}' stroke='{NAVY}' stroke-width='6'/>
      <path d='M66 28v28M134 28v28' stroke='{NAVY}' stroke-width='8' stroke-linecap='round'/>
      <g fill='{SKY}'><rect x='50' y='94' width='22' height='18' rx='4'/><rect x='89' y='94' width='22' height='18' rx='4'/><rect x='50' y='126' width='22' height='18' rx='4'/><rect x='128' y='126' width='22' height='18' rx='4'/></g>
      <rect x='126' y='92' width='26' height='22' rx='5' fill='{AMBER}' stroke='{NAVY}' stroke-width='4'/><path d='M90 136l8 8 14-14' stroke='{NAVY}' stroke-width='6' fill='none' stroke-linecap='round'/>""",
    "star": f"""<path d='M100 24l22 46 50 6-37 34 10 50-45-25-45 25 10-50-37-34 50-6z' fill='{AMBER}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M100 62l8 18' stroke='#fff' stroke-width='7' stroke-linecap='round'/><circle cx='164' cy='162' r='10' fill='{CORAL}'/><circle cx='36' cy='158' r='7' fill='{TEAL}'/>""",
    "mail": f"""<rect x='26' y='52' width='148' height='100' rx='12' fill='{CREAM}' stroke='{NAVY}' stroke-width='6'/>
      <path d='M30 58l70 54 70-54' fill='none' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <circle cx='158' cy='56' r='22' fill='{CORAL}' stroke='{NAVY}' stroke-width='5'/><path d='M148 56l7 7 13-13' stroke='#fff' stroke-width='6' fill='none' stroke-linecap='round' stroke-linejoin='round'/>
      <path d='M8 92h22M14 112h16' stroke='{AMBER}' stroke-width='7' stroke-linecap='round'/>""",
    "clipboard": f"""<rect x='46' y='34' width='108' height='140' rx='12' fill='{CREAM}' stroke='{NAVY}' stroke-width='6'/>
      <rect x='74' y='22' width='52' height='26' rx='8' fill='{AMBER}' stroke='{NAVY}' stroke-width='6'/>
      <g stroke='{NAVY}' stroke-width='6' stroke-linecap='round' fill='none'><path d='M64 80l7 7 12-12M64 112l7 7 12-12M64 144l7 7 12-12'/><path d='M96 82h40M96 114h40M96 146h28'/></g>""",
    "handshake": f"""<path d='M20 84l34-22 30 14 26-6 36 26-30 40-36-6z' fill='{AMBER}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M180 84l-34-22-40 10-22 20 10 10 28-10 30 30 28-16z' fill='{SKY}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M76 128l12 12M90 118l14 14M106 110l14 14' stroke='{NAVY}' stroke-width='5' stroke-linecap='round'/>
      <path d='M40 42l6-14M100 30V14M160 42l-6-14' stroke='{CORAL}' stroke-width='7' stroke-linecap='round'/>""",
    "flag": f"""<path d='M58 176V28' stroke='{NAVY}' stroke-width='9' stroke-linecap='round'/>
      <path d='M62 34h96l-20 32 20 32H62z' fill='{CORAL}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <ellipse cx='70' cy='176' rx='44' ry='10' fill='{TEAL}'/><circle cx='150' cy='150' r='14' fill='{AMBER}' stroke='{NAVY}' stroke-width='5'/>""",
    "heart": f"""<path d='M100 168s-70-40-70-92c0-26 20-44 42-44 14 0 22 8 28 18 6-10 14-18 28-18 22 0 42 18 42 44 0 52-70 92-70 92z' fill='{CORAL}' stroke='{NAVY}' stroke-width='6' stroke-linejoin='round'/>
      <path d='M62 74q6-16 22-18' stroke='#fff' stroke-width='7' fill='none' stroke-linecap='round'/>""",
    "phone": f"""<rect x='62' y='22' width='76' height='156' rx='16' fill='{NAVY}'/><rect x='70' y='38' width='60' height='118' rx='6' fill='{SKY}'/>
      <circle cx='100' cy='168' r='5' fill='#fff'/><path d='M90 80l26 16-26 16z' fill='{AMBER}'/>
      <path d='M152 70q14 26 0 52M38 70q-14 26 0 52' stroke='{CORAL}' stroke-width='7' fill='none' stroke-linecap='round'/>""",
})

TICK = (f"<svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='{NAVY}' stroke-width='3.6' "
        f"stroke-linecap='round' stroke-linejoin='round'><path d='M4 12.5l5 5 11-11'/></svg>")


def spot(name, x, y, size=190, rot=0):
    return (f"<div style='position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;"
            f"background:#fff;border:4px solid {NAVY};box-shadow:7px 7px 0 {NAVY};transform:rotate({rot}deg);'>"
            f"<svg viewBox='0 0 200 200' width='{size - 8}' height='{size - 8}'>{SPOTS[name]}</svg></div>")


def sparkle(x, y, s=40, c=AMBER, rot=0):
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg);' width='{s}' height='{s}' viewBox='0 0 40 40'>"
            f"<path d='M20 0C22 14 26 18 40 20 26 22 22 26 20 40 18 26 14 22 0 20 14 18 18 14 20 0z' fill='{c}'/></svg>")


def squiggle(x, y, w, h, path, c=NAVY, head=True):
    """Hand-drawn dashed arrow. `path` is in the box's own coords; the head sits on the last point."""
    mk = (f"<defs><marker id='h{x}{y}' markerWidth='10' markerHeight='10' refX='5' refY='5' orient='auto'>"
          f"<path d='M0 0L10 5L0 10' fill='none' stroke='{c}' stroke-width='2.4' stroke-linecap='round'/></marker></defs>") if head else ""
    end = f"marker-end='url(#h{x}{y})'" if head else ""
    return (f"<svg style='position:absolute;left:{x}px;top:{y}px;overflow:visible;' width='{w}' height='{h}'>{mk}"
            f"<path d='{path}' fill='none' stroke='{c}' stroke-width='4' stroke-dasharray='3 11' stroke-linecap='round' {end}/></svg>")


def grid(c="rgba(14,33,65,.07)"):
    return (f"<div style='position:absolute;inset:0;background-image:linear-gradient({c} 1.5px,transparent 1.5px),"
            f"linear-gradient(90deg,{c} 1.5px,transparent 1.5px);background-size:45px 45px;'></div>")


def marker(text, hi, color=AMBER):
    """Wrap the highlight phrase in a highlighter-pen stroke."""
    if hi and hi in text:
        a, b = text.split(hi, 1)
        return (f"{a}<span style='background:linear-gradient(transparent 56%,{color} 56%,{color} 92%,transparent 92%);"
                f"padding:0 4px;margin:0 -4px;'>{hi}</span>{b}")
    return text


def footer(url, ink=NAVY, swipe=True, swipe_ink=None):
    s = ""
    if swipe:
        si = swipe_ink or ink
        s = (f"<div style=\"position:absolute;right:56px;bottom:46px;display:flex;align-items:center;gap:10px;"
             f"font-family:'DM Sans';font-weight:800;font-size:20px;letter-spacing:3px;color:{si};\">SWIPE"
             f"<svg width='46' height='20' viewBox='0 0 46 20'><path d='M2 10h40M33 2l9 8-9 8' fill='none' stroke='{si}' "
             f"stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/></svg></div>")
    return L.url_footer(left=56, bottom=44, color=ink, text=url) + s


# ---------- slides ----------
def cover(g):
    ts, hs = g.get("title_size", 98), g.get("hi_size", 138)
    t = (f"<div style='position:absolute;inset:0;background:{DEEP};'></div>" + grid("rgba(255,255,255,.05)")
         + f"<img src='{L.WHT}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"
         + f"<div style=\"position:absolute;right:56px;top:72px;padding:10px 18px;border:2px solid {TEAL};border-radius:24px;"
           f"font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:4px;color:#9FD3D2;\">{g['kicker']}</div>"
         + f"<div style='position:absolute;left:56px;top:196px;width:968px;'>"
           f"<div style=\"font-family:Inter;font-weight:900;font-size:{ts}px;line-height:1;letter-spacing:-3px;color:#fff;\">{g['title_pre']}</div>"
           f"<div style='display:flex;flex-wrap:wrap;align-items:baseline;column-gap:22px;margin-top:6px;'>"
           f"<span style=\"font-family:IWSerif;font-style:italic;font-size:{hs}px;line-height:1;color:{AMBER};\">{g['title_hi']}</span>"
           f"<span style=\"font-family:Inter;font-weight:900;font-size:{ts}px;line-height:1;letter-spacing:-3px;color:#fff;\">{g['title_post']}</span></div>"
           f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:32px;color:#B9CBE3;margin-top:22px;\">{g['sub']}</div></div>")
    # collage: arched photo, amber ghost arch, round inset, starburst badge
    t += (f"<div style='position:absolute;left:498px;top:564px;width:520px;height:640px;border-radius:260px 260px 30px 30px;"
          f"border:4px solid {AMBER};'></div>"
          f"<div style='position:absolute;left:474px;top:588px;width:520px;height:640px;border-radius:260px 260px 30px 30px;overflow:hidden;"
          f"background:url({photo(g['cover_photo'])}) center/cover;box-shadow:0 30px 60px rgba(0,0,0,.35);'></div>"
          f"<div style='position:absolute;left:96px;top:806px;width:330px;height:330px;border-radius:50%;border:10px solid #fff;"
          f"background:url({photo(g['cover_inset'])}) center 30%/cover;box-shadow:0 20px 40px rgba(0,0,0,.35);'></div>")
    burst = "".join(f"{100 + 92 * __import__('math').cos(i * 3.14159 / 12)},{100 + 92 * __import__('math').sin(i * 3.14159 / 12)} "
                    f"{100 + 76 * __import__('math').cos((i + .5) * 3.14159 / 12)},{100 + 76 * __import__('math').sin((i + .5) * 3.14159 / 12)} "
                    for i in range(24))
    n, lab = g["badge"]
    t += (f"<div style='position:absolute;left:330px;top:620px;width:220px;height:220px;transform:rotate(-10deg);'>"
          f"<svg width='220' height='220' viewBox='0 0 200 200' style='position:absolute;inset:0;'><polygon points='{burst}' fill='{CORAL}'/></svg>"
          f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;'>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:84px;line-height:.9;color:#fff;\">{n}</span>"
          f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:24px;letter-spacing:5px;color:{DEEP};\">{lab}</span></div></div>")
    t += sparkle(70, 600, 54, AMBER, 10) + sparkle(1000, 560, 36, "#9FD3D2") + sparkle(430, 1140, 30, AMBER)
    t += squiggle(150, 660, 180, 150, "M10 10 Q 0 90 60 130", c="#9FD3D2")
    return t + footer(g["cta_url"], ink="#B9CBE3", swipe_ink=AMBER)


def step(g, i):
    s = g["steps"][i]
    n = len(g["steps"])
    flip = i % 2 == 1                       # alternate photo side for rhythm
    px, cx = (554, 56) if flip else (56, 570)
    rot = 2.5 if flip else -2.5
    prog = "".join(f"<span style='width:30px;height:8px;border-radius:4px;background:"
                   f"{CORAL if k == i else (NAVY if k < i else 'rgba(14,33,65,.18)')};'></span>" for k in range(n))
    t = (f"<div style='position:absolute;inset:0;background:{PAPER};'></div>" + grid()
         + f"<img src='{L.DARKLOGO}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"
         + f"<div style='position:absolute;right:56px;top:66px;text-align:right;'>"
           f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:4px;color:{TEAL};\">HIRING PLAYBOOK</div>"
           f"<div style='display:flex;gap:6px;margin-top:12px;justify-content:flex-end;'>{prog}</div></div>")
    # number + title
    t += (f"<div style='position:absolute;left:56px;top:176px;width:968px;display:flex;align-items:center;gap:26px;'>"
          f"<span style=\"flex:none;font-family:IWSerif;font-style:italic;font-size:170px;line-height:.8;color:{CORAL};\">{i + 1:02d}</span>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:72px;line-height:1.02;letter-spacing:-2.4px;color:{NAVY};\">"
          f"{marker(s['title'], s.get('hi'))}</span></div>")
    # taped polaroid photo
    tape = lambda x, r: (f"<div style='position:absolute;left:{x}px;top:-18px;width:120px;height:38px;background:rgba(255,177,32,.72);"
                         f"transform:rotate({r}deg);box-shadow:0 2px 4px rgba(0,0,0,.08);'></div>")
    t += (f"<div style='position:absolute;left:{px}px;top:404px;width:470px;height:596px;background:#fff;padding:16px 16px 64px;"
          f"transform:rotate({rot}deg);box-shadow:0 18px 40px rgba(14,33,65,.22);'>"
          f"<div style='width:100%;height:100%;background:url({photo(s['photo'])}) center/cover;'></div>"
          f"{tape(-30, -28)}{tape(380, 26)}"
          f"<div style=\"position:absolute;{'left' if not flip else 'right'}:22px;bottom:14px;font-family:IWSerif;font-style:italic;font-size:30px;color:{NAVY};\">"
          f"{g.get('unit', 'step')} {i + 1} of {n}</div></div>")
    t += spot(s["icon"], (px + 330) if not flip else (px - 60), 860, 190, -6 if not flip else 6)
    # checklist card
    rows = "".join(f"<div style='display:flex;gap:16px;align-items:flex-start;margin-top:20px;'>"
                   f"<span style='flex:none;width:36px;height:36px;border-radius:9px;background:{AMBER};border:3px solid {NAVY};"
                   f"display:flex;align-items:center;justify-content:center;margin-top:1px;'>{TICK}</span>"
                   f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;line-height:1.24;color:{NAVY};\">{p}</span></div>"
                   for p in s["points"])
    t += (f"<div style='position:absolute;left:{cx}px;top:418px;width:454px;background:#fff;border:3px solid {NAVY};border-radius:22px;"
          f"box-shadow:9px 9px 0 {NAVY};padding:26px 28px 30px;'>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:5px;color:{TEAL};\">{g.get('points_label', 'DO THIS')}</div>"
          f"<div style='width:56px;height:4px;background:{CORAL};border-radius:2px;margin-top:10px;'></div>{rows}</div>")
    # sticky-note tip with a pushpin
    t += (f"<div style='position:absolute;left:{120 if not flip else 200}px;top:1062px;width:760px;background:{AMBER};padding:26px 34px 28px;"
          f"transform:rotate({-1.2 if not flip else 1.2}deg);box-shadow:0 14px 26px rgba(14,33,65,.20);border-radius:4px 4px 22px 4px;'>"
          f"<div style='position:absolute;{'left:64px' if not flip else 'right:64px'};top:-16px;width:30px;height:30px;border-radius:50%;background:{CORAL};"
          f"border:3px solid {NAVY};'></div>"
          f"<div style='display:flex;align-items:center;gap:10px;font-family:\"DM Sans\";font-weight:800;font-size:18px;letter-spacing:4px;color:{DEEP};'>"
          f"{L.svg('bulb', DEEP, 24)}PRO TIP</div>"
          f"<div style=\"font-family:Inter;font-weight:700;font-size:28px;line-height:1.25;color:{DEEP};margin-top:8px;\">{s['tip']}</div></div>")
    t += sparkle(1000 if not flip else 40, 1040, 34, CORAL, 12)
    return t + footer(g["cta_url"])


def cta(g):
    steps = "".join(f"<div style='display:flex;align-items:center;gap:16px;padding:13px 0;border-bottom:2px dashed rgba(14,33,65,.18);'>"
                    f"<span style='flex:none;width:34px;height:34px;border-radius:8px;background:{TEAL};display:flex;align-items:center;"
                    f"justify-content:center;'><svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='3.6' "
                    f"stroke-linecap='round' stroke-linejoin='round'><path d='M4 12.5l5 5 11-11'/></svg></span>"
                    f"<span style=\"font-family:IWSerif;font-style:italic;font-size:30px;color:{CORAL};width:44px;\">{k + 1:02d}</span>"
                    f"<span style=\"font-family:Inter;font-weight:800;font-size:27px;color:{NAVY};\">{s['title']}</span></div>"
                    for k, s in enumerate(g["steps"]))
    ch = g.get("cta_hi", "")
    q = g["cta_title"].replace(ch, f"<span style=\"font-family:IWSerif;font-style:italic;font-weight:400;color:{AMBER};letter-spacing:0;\">{ch}</span>") if ch else g["cta_title"]
    t = (f"<div style='position:absolute;inset:0;background:{DEEP};'></div>" + grid("rgba(255,255,255,.05)")
         + f"<img src='{L.WHT}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"
         + f"<div style=\"position:absolute;left:56px;top:190px;width:900px;font-family:Inter;font-weight:900;font-size:84px;line-height:1.02;"
           f"letter-spacing:-2.6px;color:#fff;\">{q}</div>"
         + f"<div style=\"position:absolute;left:56px;top:390px;width:900px;font-family:'DM Sans';font-weight:600;font-size:30px;color:#B9CBE3;\">{g['cta_sub']}</div>")
    # paper checklist with a vector clip
    t += (f"<div style='position:absolute;left:56px;top:500px;width:640px;background:{PAPER};border-radius:18px;padding:52px 34px 26px;"
          f"transform:rotate(-1.5deg);box-shadow:0 26px 50px rgba(0,0,0,.4);'>"
          f"<svg style='position:absolute;left:270px;top:-34px;' width='100' height='70' viewBox='0 0 100 70'>"
          f"<rect x='8' y='14' width='84' height='44' rx='10' fill='{NAVY}'/><rect x='30' y='0' width='40' height='26' rx='9' fill='none' stroke='{NAVY}' stroke-width='8'/></svg>"
          f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:5px;color:{TEAL};\">YOUR HIRING CHECKLIST</div>{steps}</div>")
    t += (f"<div style='position:absolute;left:728px;top:560px;width:300px;height:300px;border-radius:50%;border:4px solid {AMBER};'></div>"
          f"<div style='position:absolute;left:744px;top:576px;width:268px;height:268px;border-radius:50%;"
          f"background:url({photo(g['steps'][-1]['photo'])}) center/cover;'></div>"
          + spot(g.get("cta_icon", "rocket"), 800, 880, 170, 8) + sparkle(730, 520, 44, AMBER, 0) + sparkle(1000, 860, 30, "#9FD3D2"))
    t += (f"<div style='position:absolute;left:56px;top:1150px;display:inline-flex;align-items:center;gap:16px;height:96px;padding:0 40px;"
          f"border-radius:48px;background:{AMBER};box-shadow:8px 8px 0 #fff;'>"
          f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:24px;color:{DEEP};\">Post your internship at</span>"
          f"<span style=\"font-family:Inter;font-weight:900;font-size:32px;color:{DEEP};\">{g['cta_url']}</span>"
          f"<svg width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='{DEEP}' stroke-width='3' stroke-linecap='round' "
          f"stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>")
    return t


def render_guide(slug, out_dir):
    g = json.load(open(os.path.join(SPECS, slug + ".json")))
    slides = [cover(g)] + [step(g, i) for i in range(len(g["steps"]))] + [cta(g)]
    return [L.render(out_dir, f"slide_{k + 1}.png", html, w=W, h=H) for k, html in enumerate(slides)]


LANE, TIME = "employer_guide", "10:00"
DAYS = ["mon", "tue", "wed", "thu", "fri"]


def add_to_week(wid, slugs, upload=True):
    """Render one guide per weekday into images/<wid>/ and write them into the week's
    entry in data/weeks.json as `in-review` posts. The guides are prepared ahead of
    the Saturday batch, which preserves this lane when it rewrites the week."""
    import datetime
    os.environ["WEEK_ID"] = wid
    import build_week as B
    wid, wlabel, wc, mon = B.target_week()
    img = os.path.join(B.HUB, "images", wid)
    posts = []
    for di, slug in enumerate(slugs):
        g = json.load(open(os.path.join(SPECS, slug + ".json")))
        day = mon + datetime.timedelta(days=di)
        pid = f"{wid}-{DAYS[di]}-employerguide"
        paths = render_guide(slug, os.path.join(img, pid))
        caps, tags = g["captions"], g["hashtags"]
        posts.append({"id": pid, "day": day.strftime("%a %-d %b"), "lane": LANE, "title": g["post_title"],
                      "platform": "Multi-Platform", "format": "Carousel",
                      "slides": [os.path.basename(p) for p in paths], "status": "in-review", "time": TIME,
                      "caption": caps["ig-fb"], "hashtags": tags["ig-fb"], "captions": caps,
                      "hashtagsByPlatform": tags, "altText": g["altText"], "world": "playbook",
                      "guide": slug, "searchQuery": g.get("query", "")})
    data = json.load(open(B.WEEKS))
    week = next((w for w in data["weeks"] if w.get("id") == wid), None)
    if week is None:
        week = {"id": wid, "label": wlabel, "weekCommencing": wc, "posts": []}
        data["weeks"].append(week)
    ids = {p["id"] for p in posts}
    week["posts"] = [p for p in week["posts"] if p["id"] not in ids] + posts
    week["builtAt"] = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    json.dump(data, open(B.WEEKS, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {len(posts)} employer guides into {wid}")
    if upload:
        import r2
        if os.getenv("R2_ACCESS_KEY_ID"):
            for p in posts:
                r2.upload_tree(os.path.join(img, p["id"]), prefix=f"{wid}/{p['id']}/")
            print("uploaded to R2")
    return posts


if __name__ == "__main__":
    if sys.argv[1] == "week":            # lane_employer_guide.py week week25 slug-mon slug-tue ...
        add_to_week(sys.argv[2], sys.argv[3:])
    else:
        slug = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(L.BASE, "test_output_employer_guide", slug)
        render_guide(slug, out)
