"""Education lane - a LIBRARY of genuinely DISTINCT design worlds so education can
auto-render. Each carousel world is its own art direction (not the same skeleton
recoloured):

  teal  -> "spine"  : a full-height accent navigation spine down the left edge
  plum  -> "poster" : type-led editorial poster (no photo on the cover)
  navy  -> "bento"  : rounded-card / bento system, Nuno framed by a panel

Single worlds are also distinct from each other and from the carousels:
  tipcard   -> cream ruled "notepad" checklist
  statement -> dark "manifesto" with oversized ticks + accent band

Carousel worlds render cover -> content slides -> CTA. Copy comes from the writer
(writer.write_education): {eyebrow, headline, slides:[{tag,title,body}], points, cta, tone}.
Nuno is always placed WHOLE (never cropped, zoomed or distorted).

    render_education(copy, world, out_dir)   # writes slide_1..N.png
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import nuno_ledger

INK, MUT, DEEP = L.INK, L.MUT, L.DEEP
AMBER, CORAL, GREEN, NAVY = L.AMBER, L.CORAL, L.GREEN, L.NAVY

# palette per carousel world
PAL = {
    "navy": {"bg": f"background-color:{NAVY};", "grid": True, "accent": AMBER, "ink": INK, "mut": MUT, "deep": DEEP},
    "plum": {"bg": "background:linear-gradient(160deg,#2a1840,#180d24);", "grid": False, "accent": CORAL,
             "ink": "#F4EAF9", "mut": "#B9A6CC", "deep": "#150a1f"},
    "teal": {"bg": "background:linear-gradient(160deg,#0c3038,#0a1d24);", "grid": True, "accent": GREEN,
             "ink": INK, "mut": "#9FC2C9", "deep": "#081418"},
}

# Cover poses hug the RIGHT edge (compact, right-weighted) so they clear the left
# text column. CTA poses read confident/positive. (See original notes on excluded
# poses: nuno_cv_1 loses its laptop, nuno_utility_2 loses a white sheet on rembg.)
COVER_POOL = ["nuno_cv", "nuno_cv_2", "nuno_cv_3",
              "nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3",
              "nuno_authority_1", "nuno_authority_2", "nuno_authority_3",
              "nuno_planning_1", "nuno_planning_2", "nuno_planning_3",
              "nuno_cvpile", "nuno_utility_3"]
CTA_POOL = ["nuno_thumbsup", "nuno_dothis_1", "nuno_dothis_2", "nuno_offers_1"]


# --------------------------------------------------------------- shared bits
def _bg(p):
    grid = ("<div style='position:absolute;inset:0;background-image:"
            "linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),"
            "linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);"
            "background-size:56px 56px;'></div>") if p["grid"] else ""
    return f"<div style='position:absolute;inset:0;{p['bg']}'></div>{grid}"

def _logo(src=None, left=56, top=44, h=L.LOGO):
    return f"<div style='position:absolute;left:{left}px;top:{top}px;'><img src='{src or L.WHT}' style='height:{h}px;'></div>"

def _nuno_whole(pose, h=820, right=-40, bottom=0):
    """Founder cut-out placed WHOLE (no crop/zoom/distort) with a soft ground."""
    src = L.nuno_src(pose)
    ground = (f"<div style='position:absolute;right:150px;bottom:30px;width:520px;height:66px;border-radius:50%;"
              f"background:radial-gradient(ellipse,rgba(0,0,0,.5),rgba(0,0,0,0) 70%);'></div>")
    img = f"<img src='{src}' style='position:absolute;right:{right}px;bottom:{bottom}px;height:{h}px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.5));'>"
    return ground + img

def _arc(p, right=-70, bottom=-40, size=760):
    return (f"<div style='position:absolute;right:{right}px;bottom:{bottom}px;width:{size}px;height:{size}px;border-radius:50%;"
            f"background:radial-gradient(circle at 50% 45%,{p['accent']}2e,{p['accent']}00 66%);'></div>")

def _pill(p, dark_ink=False):
    ink = p['deep'] if dark_ink else p['accent']
    bd = p['accent']
    return (f"<div style='display:inline-flex;align-items:center;border:2px solid {bd};border-radius:14px;padding:11px 24px;"
            f"{'background:'+p['accent']+';' if dark_ink else ''}'>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;color:{ink};\">internwise.co.uk</span></div>")

def _footer(p, swipe=True, dark_ink=False):
    ink = p['deep'] if dark_ink else p['deep']
    f = (f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
         f"<div style='width:34px;height:34px;border-radius:50%;background:{p['accent']};display:flex;align-items:center;justify-content:center;'>"
         f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{p['deep']}' stroke-width='2.6' "
         f"stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
         f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{p['mut']};letter-spacing:1px;\">internwise.co.uk</span></div>")
    if swipe:
        f += f"<div style=\"position:absolute;right:58px;bottom:44px;font-family:'DM Sans';font-weight:600;font-size:23px;color:{p['accent']};\">Swipe &rarr;</div>"
    return f


# =================================================================================
#  WORLD 1  -  "spine"  (teal)  : full-height accent navigation spine, left edge
# =================================================================================
SPINE_W = 132

def _spine(p, n, total):
    """The signature device: a coloured rail down the left with the issue number
    and a progress ladder (current step filled)."""
    ticks = ""
    for i in range(1, total + 1):
        on = i <= n
        ticks += (f"<div style='width:{'40' if i==n else '22'}px;height:8px;border-radius:4px;margin:9px 0;"
                  f"background:{p['deep'] if on else 'rgba(255,255,255,.28)'};'></div>")
    return (f"<div style='position:absolute;left:0;top:0;bottom:0;width:{SPINE_W}px;background:{p['accent']};'>"
            f"<div style=\"position:absolute;left:0;right:0;top:52px;text-align:center;font-family:Inter;font-weight:800;"
            f"font-size:40px;color:{p['deep']};\">0{n}</div>"
            f"<div style=\"position:absolute;left:0;right:0;top:104px;text-align:center;font-family:'DM Sans';font-weight:700;"
            f"font-size:17px;color:{p['deep']};letter-spacing:2px;opacity:.6;\">OF 0{total}</div>"
            f"<div style='position:absolute;left:0;right:0;top:170px;display:flex;flex-direction:column;align-items:center;'>{ticks}</div>"
            f"<div style=\"position:absolute;left:0;right:0;bottom:52px;text-align:center;font-family:'DM Sans';font-weight:800;"
            f"font-size:16px;color:{p['deep']};letter-spacing:3px;writing-mode:vertical-rl;transform:rotate(180deg);margin:0 auto;\">INTERNWISE</div></div>")

def cover_spine(p, copy, total, pose):
    x = SPINE_W + 48
    return (_bg(p) + _spine(p, 1, total) + _arc(p) + _nuno_whole(pose, h=800)
            + _logo(left=x, top=48)
            + f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:700;font-size:22px;"
              f"color:{p['accent']};letter-spacing:4px;\">{copy.get('eyebrow','INTERNWISE')[:26].upper()}</div>"
            + f"<div style=\"position:absolute;left:{x}px;top:300px;width:540px;font-family:Inter;font-weight:700;"
              f"font-size:66px;line-height:1.03;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            + f"<div style=\"position:absolute;left:{x}px;bottom:48px;font-family:'DM Sans';font-weight:600;font-size:23px;"
              f"color:{p['accent']};\">Swipe to begin &rarr;</div>")

def content_spine(p, n, total, slide):
    x = SPINE_W + 48
    return (_bg(p) + _spine(p, n, total)
            + f"<div style=\"position:absolute;left:{x}px;top:150px;font-family:'DM Sans';font-weight:700;font-size:22px;"
              f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:30].upper()}</div>"
            + f"<div style='position:absolute;left:{x}px;top:190px;width:64px;height:4px;background:{p['accent']};border-radius:2px;'></div>"
            + f"<div style=\"position:absolute;left:{x}px;top:240px;width:820px;font-family:Inter;font-weight:700;"
              f"font-size:58px;line-height:1.04;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>"
            + f"<div style=\"position:absolute;left:{x}px;top:470px;width:820px;font-family:'DM Sans';font-weight:500;"
              f"font-size:41px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>"
            + L.watermark(w=420, right=-70, bottom=-110, op=.05))

def cta_spine(p, copy, total, pose):
    x = SPINE_W + 48
    return (_bg(p) + _spine(p, total, total) + _arc(p) + _nuno_whole(pose, h=760)
            + f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:700;font-size:22px;"
              f"color:{p['accent']};letter-spacing:4px;\">YOUR MOVE</div>"
            + f"<div style=\"position:absolute;left:{x}px;top:300px;width:470px;font-family:Inter;font-weight:700;"
              f"font-size:58px;line-height:1.03;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            + f"<div style=\"position:absolute;left:{x}px;top:520px;width:450px;font-family:'DM Sans';font-weight:500;"
              f"font-size:34px;line-height:1.35;color:{p['mut']};\">{copy.get('cta','')}</div>"
            + f"<div style='position:absolute;left:{x}px;top:660px;'>{_pill(p)}</div>")


# =================================================================================
#  WORLD 2  -  "poster"  (plum)  : type-led editorial poster, NO photo on cover
# =================================================================================
def cover_poster(p, copy, total, pose):
    # Photo-free, type-led. A big soft accent blob + oversized headline.
    blob = (f"<div style='position:absolute;right:-160px;top:-120px;width:660px;height:660px;border-radius:50%;"
            f"background:radial-gradient(circle at 40% 40%,{p['accent']}40,{p['accent']}00 62%);'></div>")
    blob2 = (f"<div style='position:absolute;left:-140px;bottom:-160px;width:560px;height:560px;border-radius:50%;"
             f"background:radial-gradient(circle at 60% 40%,{AMBER}22,{AMBER}00 62%);'></div>")
    mark = (f"<div style='position:absolute;right:64px;top:300px;font-family:Georgia,serif;font-weight:700;font-size:360px;"
            f"line-height:.6;color:{p['accent']};opacity:.12;'>&rdquo;</div>")
    eyebrow = (f"<div style='position:absolute;left:56px;top:210px;display:inline-flex;align-items:center;height:48px;padding:0 22px;"
               f"border-radius:24px;background:{p['accent']};'>"
               f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:21px;color:{p['deep']};letter-spacing:3px;\">{copy.get('eyebrow','INTERNWISE')[:24].upper()}</span></div>")
    head = (f"<div style=\"position:absolute;left:56px;right:70px;top:296px;font-family:Inter;font-weight:800;"
            f"font-size:104px;line-height:.98;letter-spacing:-3.5px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    rule = f"<div style='position:absolute;left:58px;bottom:150px;width:120px;height:8px;background:{p['accent']};border-radius:4px;'></div>"
    return _bg(p) + blob + blob2 + mark + _logo(left=56, top=44) + eyebrow + head + rule + _footer(p, swipe=True)

def content_poster(p, n, total, slide):
    numeral = (f"<div style=\"position:absolute;left:52px;top:236px;font-family:Inter;font-weight:800;font-size:150px;"
               f"line-height:.8;color:{p['accent']};letter-spacing:-6px;\">0{n-1}</div>")
    tag = (f"<div style=\"position:absolute;left:300px;top:262px;font-family:'DM Sans';font-weight:800;font-size:22px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:26].upper()}</div>"
           f"<div style='position:absolute;left:300px;top:298px;width:60px;height:4px;background:{p['accent']};border-radius:2px;'></div>")
    head = (f"<div style=\"position:absolute;left:56px;right:80px;top:440px;font-family:Inter;font-weight:700;"
            f"font-size:64px;line-height:1.02;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:58px;right:96px;top:620px;font-family:'DM Sans';font-weight:500;"
            f"font-size:42px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>")
    return (_bg(p) + numeral + tag + head + body
            + _logo(left=56, top=44)
            + f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:{p['mut']};letter-spacing:2px;\"><span style='color:{p['accent']};'>0{n}</span> / 0{total}</div>"
            + L.watermark(w=420, right=-70, bottom=-110, op=.05) + _footer(p, swipe=True))

def cta_poster(p, copy, total, pose):
    # Nuno is introduced only here (kept off the cover for the type-led look).
    return (_bg(p) + _arc(p) + _nuno_whole(pose, h=780)
            + f"<div style='position:absolute;left:56px;top:250px;display:inline-flex;align-items:center;height:48px;padding:0 22px;border-radius:24px;background:{p['accent']};'>"
              f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:21px;color:{p['deep']};letter-spacing:3px;\">YOUR MOVE</span></div>"
            + f"<div style=\"position:absolute;left:56px;top:326px;width:500px;font-family:Inter;font-weight:800;"
              f"font-size:66px;line-height:1.0;letter-spacing:-2.5px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            + f"<div style=\"position:absolute;left:58px;top:560px;width:470px;font-family:'DM Sans';font-weight:500;"
              f"font-size:34px;line-height:1.35;color:{p['mut']};\">{copy.get('cta','')}</div>"
            + f"<div style='position:absolute;left:58px;top:700px;'>{_pill(p, dark_ink=True)}</div>"
            + _logo(left=56, top=44))


# =================================================================================
#  WORLD 3  -  "bento"  (navy)  : rounded-card system, Nuno framed by a panel
# =================================================================================
def _card(inner, css, bg="rgba(255,255,255,.05)", bd="rgba(255,255,255,.10)", pad="34px 36px", radius=26):
    return (f"<div style='position:absolute;{css}background:{bg};border:1px solid {bd};border-radius:{radius}px;"
            f"padding:{pad};box-sizing:border-box;'>{inner}</div>")

def cover_bento(p, copy, total, pose):
    # A rounded accent panel on the right; Nuno stands WHOLE in front of it.
    panel = (f"<div style='position:absolute;right:44px;top:150px;bottom:150px;width:470px;border-radius:34px;"
             f"background:linear-gradient(160deg,{p['accent']}26,{p['accent']}08);border:1px solid {p['accent']}33;'></div>")
    chip = (f"<div style='position:absolute;right:64px;top:66px;display:inline-flex;align-items:center;height:42px;padding:0 18px;"
            f"border-radius:21px;background:{p['accent']};'><span style=\"font-family:Inter;font-weight:800;font-size:20px;color:{p['deep']};letter-spacing:1px;\">01 / 0{total}</span></div>")
    headcard = _card(
        f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:22px;color:{p['accent']};letter-spacing:4px;margin-bottom:18px;\">{copy.get('eyebrow','INTERNWISE')[:24].upper()}</div>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:62px;line-height:1.02;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>",
        css="left:56px;top:300px;width:520px;", pad="40px 42px")
    return (_bg(p) + panel + _nuno_whole(pose, h=760, right=10) + _logo(left=56, top=44) + chip + headcard
            + _footer(p, swipe=True))

def content_bento(p, n, total, slide):
    badge = (f"<div style='position:absolute;left:56px;top:236px;width:96px;height:96px;border-radius:24px;background:{p['accent']};"
             f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:52px;color:{p['deep']};'>0{n-1}</div>")
    tag = (f"<div style=\"position:absolute;left:176px;top:250px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>"
           f"<div style=\"position:absolute;left:176px;top:290px;width:760px;font-family:Inter;font-weight:700;font-size:52px;line-height:1.05;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    bodycard = _card(
        f"<span style=\"font-family:'DM Sans';font-weight:500;font-size:41px;line-height:1.42;color:{p['ink']};\">{slide['body']}</span>",
        css=f"left:56px;right:56px;top:{max(470, 470)}px;", bg="rgba(255,255,255,.06)", pad="40px 42px")
    return (_bg(p) + badge + tag + bodycard + _logo(left=56, top=44)
            + f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;color:{p['mut']};letter-spacing:2px;\"><span style='color:{p['accent']};'>0{n}</span> / 0{total}</div>"
            + _footer(p, swipe=True))

def cta_bento(p, copy, total, pose):
    panel = (f"<div style='position:absolute;right:44px;top:170px;bottom:150px;width:460px;border-radius:34px;"
             f"background:linear-gradient(160deg,{p['accent']}26,{p['accent']}08);border:1px solid {p['accent']}33;'></div>")
    card = _card(
        f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:22px;color:{p['accent']};letter-spacing:4px;margin-bottom:16px;\">YOUR MOVE</div>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:56px;line-height:1.02;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
        f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:33px;line-height:1.34;color:{p['mut']};margin-top:22px;\">{copy.get('cta','')}</div>",
        css="left:56px;top:280px;width:520px;", pad="40px 42px")
    return (_bg(p) + panel + _nuno_whole(pose, h=720, right=10) + _logo(left=56, top=44) + card
            + f"<div style='position:absolute;left:96px;bottom:120px;'>{_pill(p)}</div>")


# =================================================================================
#  SINGLE WORLDS
# =================================================================================
def w_tipcard(copy):
    """Cream ruled 'notepad' checklist - a warm, tactile counterpoint to the dark
    carousels."""
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#8A7B62"; LINE = "rgba(21,39,67,.10)"
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    # ruled lines like a notepad
    rules = ("<div style='position:absolute;left:0;right:0;top:420px;bottom:0;"
             f"background-image:linear-gradient({LINE} 2px,transparent 2px);background-size:100% 96px;'></div>")
    # bold header band
    band = (f"<div style='position:absolute;left:0;top:0;right:0;height:170px;background:{NAVYT};'></div>")
    logo = f"<div style='position:absolute;left:56px;top:44px;'><img src='{L.WHT}' style='height:{L.LOGO}px;'></div>"
    tab = (f"<div style='position:absolute;right:56px;top:56px;display:inline-flex;align-items:center;height:46px;padding:0 22px;"
           f"border-radius:23px;background:{AMBER};'><span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;color:{NAVYT};letter-spacing:2px;\">{copy.get('eyebrow','TIP')[:20].upper()}</span></div>")
    head = (f"<div style=\"position:absolute;left:56px;right:64px;top:214px;font-family:Inter;font-weight:700;"
            f"font-size:64px;line-height:1.02;letter-spacing:-2px;color:{NAVYT};word-break:keep-all;\">{copy['headline']}</div>")
    pts = copy.get("points", [])
    rows = ""
    for i, pt in enumerate(pts, 1):
        rows += (f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:26px;'>"
                 f"<div style='flex:0 0 52px;width:52px;height:52px;border-radius:14px;background:{AMBER};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:26px;color:{NAVYT};'>{i}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:33px;color:#1c2740;line-height:1.16;\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;right:70px;top:452px;'>{rows}</div>"
    cta = (f"<div style='position:absolute;left:56px;bottom:46px;display:flex;align-items:center;gap:13px;'>"
           f"<div style='width:34px;height:34px;border-radius:50%;background:{CORAL};display:flex;align-items:center;justify-content:center;'>"
           f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
           f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;color:{NAVYT};\">{copy.get('cta','internwise.co.uk')}</span></div>")
    return bg + rules + band + logo + tab + head + body + cta

def w_statement(copy):
    """Dark 'manifesto' - oversized ticks and a strong accent band, distinct from
    the carousels' number/spine systems."""
    p = PAL["navy"]
    bg = _bg(p)
    logo = L.logo_tl()
    eb = (f"<div style='position:absolute;left:58px;top:210px;display:inline-flex;align-items:center;height:46px;padding:0 22px;"
          f"border-radius:23px;background:{AMBER};'><span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;color:{DEEP};letter-spacing:3px;\">{copy.get('eyebrow','LEARN')[:20].upper()}</span></div>")
    head = (f"<div style=\"position:absolute;left:56px;right:70px;top:286px;font-family:Inter;font-weight:800;"
            f"font-size:70px;line-height:1.0;letter-spacing:-2.5px;color:{INK};word-break:keep-all;\">{copy['headline']}</div>")
    pts = copy.get("points", [])
    rows = ""
    for pt in pts:
        rows += (f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:22px;'>"
                 f"<div style='flex:0 0 52px;width:52px;height:52px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>{L.svg('check',DEEP,28)}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:33px;color:{INK};letter-spacing:-.3px;line-height:1.15;\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;right:64px;top:500px;'>{rows}</div>"
    band = (f"<div style='position:absolute;left:0;right:0;bottom:0;height:120px;background:{AMBER};display:flex;align-items:center;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:32px;color:{DEEP};margin-left:56px;letter-spacing:-.3px;\">{copy.get('cta','internwise.co.uk')}</span></div>")
    return bg + logo + eb + head + body + L.watermark(op=.04) + band


CAROUSEL = {
    "teal": {"cover": cover_spine, "content": content_spine, "cta": cta_spine},
    "plum": {"cover": cover_poster, "content": content_poster, "cta": cta_poster},
    "navy": {"cover": cover_bento, "content": content_bento, "cta": cta_bento},
}
SINGLE = {"tipcard": w_tipcard, "statement": w_statement}

COVER_TONE = {"serious": ["serious", "thoughtful", "practical"],
              "practical": ["practical", "confident", "serious"],
              "upbeat": ["confident", "positive", "practical"]}
CTA_TONE = {"serious": ["confident"], "practical": ["confident", "positive"],
            "upbeat": ["positive", "confident"]}


def render_education(copy, world, out_dir, week_id="adhoc"):
    os.makedirs(out_dir, exist_ok=True)
    if world in CAROUSEL:
        p = PAL[world]; w = CAROUSEL[world]
        slides = copy.get("slides", [])
        total = len(slides) + 2
        tone = copy.get("tone", "practical")
        cover_pose = nuno_ledger.pick(COVER_POOL, week_id, label=f"education/{world}/cover", tone=COVER_TONE.get(tone))
        cta_pose = nuno_ledger.pick(CTA_POOL, week_id, label=f"education/{world}/cta", tone=CTA_TONE.get(tone))
        paths = [L.render(out_dir, "slide_1.png", w["cover"](p, copy, total, cover_pose))]
        for i, s in enumerate(slides, start=2):
            paths.append(L.render(out_dir, f"slide_{i}.png", w["content"](p, i, total, s)))
        paths.append(L.render(out_dir, f"slide_{total}.png", w["cta"](p, copy, total, cta_pose)))
        return paths
    return [L.render(out_dir, "slide_1.png", SINGLE[world](copy))]


if __name__ == "__main__":
    demo = {"eyebrow": "The CV clinic", "headline": "The CV Line Recruiters Skip", "tone": "practical",
            "slides": [
                {"tag": "The problem", "title": "Duties are not proof", "body": "\"Responsible for the socials\" tells a recruiter nothing about what you actually did."},
                {"tag": "The fix", "title": "Lead with the result", "body": "Swap the duty for an outcome: action, skill, and a number where you have one."},
                {"tag": "Example", "title": "Before and after", "body": "Before: ran the newsletter. After: grew it to 2,000 readers in 3 months."}],
            "cta": "Build a CV that gets seen. Start today.",
            "points": ["Lead with results", "Add a number", "Cut vague duties", "Match the advert"]}
    for w in ["teal", "plum", "navy", "tipcard", "statement"]:
        render_education(demo, w, os.path.join(L.OUTROOT, "week14", "_edtest", w))
