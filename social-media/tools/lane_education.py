"""Education lane - a LIBRARY of distinct design worlds so education can auto-render.
Carousel worlds render cover -> content slides -> CTA (Nuno on cover + CTA, premium
furniture). Single worlds render one teaching slide. Copy comes from the writer
(writer.write_education): {eyebrow, headline, slides:[{title,body}] | points:[], cta}.

    render_education(copy, world, out_dir)   # writes slide_1..N.png
Carousel worlds: navy, plum, teal.  Single worlds: tipcard, statement.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import nuno_ledger

INK, MUT, DEEP = L.INK, L.MUT, L.DEEP
AMBER, CORAL, GREEN, NAVY = L.AMBER, L.CORAL, L.GREEN, L.NAVY

# palette per carousel world (Nuno pose is no longer fixed here - the ledger picks
# a fresh one each week from the pools below)
PAL = {
    "navy": {"bg": f"background-color:{NAVY};", "grid": True, "accent": AMBER, "ink": INK, "mut": MUT,
             "deep": DEEP},
    "plum": {"bg": "background:linear-gradient(160deg,#2a1840,#180d24);", "grid": False, "accent": CORAL,
             "ink": "#F4EAF9", "mut": "#B9A6CC", "deep": "#150a1f"},
    "teal": {"bg": "background:linear-gradient(160deg,#0c3038,#0a1d24);", "grid": True, "accent": GREEN,
             "ink": INK, "mut": "#9FC2C9", "deep": "#081418"},
}
# A cover pose must be RIGHT-WEIGHTED / compact (head+torso hug the right edge) so
# it clears the left headline column (_cover: left:56, width:520). Wide arms-spread
# or left-reaching poses put the figure under the headline - kept OUT of COVER_POOL.
# NOTE: nuno_cv_1 excluded - its rembg cutout loses the laptop against dark
# backgrounds (needs re-cutting before it goes back in).
COVER_POOL = ["nuno_cv", "nuno_cv_2", "nuno_cv_3",
              "nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3",
              "nuno_authority_1", "nuno_authority_2", "nuno_authority_3",
              "nuno_planning_1", "nuno_planning_2", "nuno_planning_3",
              "nuno_cvpile", "nuno_utility_2", "nuno_utility_3"]
# CTA poses read as CONFIDENT / positive (not celebratory) so they don't clash
# with evaluative topics. welcoming_2 (hand-on-heart, laughing) removed for that
# reason. Pool is thin - more CTA cutouts needed (see nuno_check).
CTA_POOL = ["nuno_thumbsup", "nuno_dothis_1", "nuno_dothis_2", "nuno_offers_1"]


def _bg(p):
    grid = ("<div style='position:absolute;inset:0;background-image:"
            "linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),"
            "linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);"
            "background-size:56px 56px;'></div>") if p["grid"] else ""
    return f"<div style='position:absolute;inset:0;{p['bg']}'></div>{grid}"

def _head(p, n, total):
    return (f"<div style='position:absolute;left:56px;top:44px;'><img src='{L.WHT}' style='height:{L.LOGO}px;'></div>"
            f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;"
            f"color:{p['mut']};letter-spacing:2px;\"><span style='color:{p['accent']};'>0{n}</span> / 0{total}</div>")

def _eyebrow(p, tag, top=200):
    return (f"<div style=\"position:absolute;left:58px;top:{top}px;font-family:'DM Sans';font-weight:700;"
            f"font-size:22px;color:{p['accent']};letter-spacing:4px;\">{tag[:26].upper()}</div>"
            f"<div style='position:absolute;left:58px;top:{top+34}px;width:64px;height:4px;background:{p['accent']};border-radius:2px;'></div>")

def _footer(p, swipe=True):
    f = (f"<div style='position:absolute;left:56px;bottom:44px;display:flex;align-items:center;gap:13px;'>"
         f"<div style='width:34px;height:34px;border-radius:50%;background:{p['accent']};display:flex;align-items:center;justify-content:center;'>"
         f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{p['deep']}' stroke-width='2.6' "
         f"stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
         f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{p['mut']};letter-spacing:1px;\">internwise.co.uk</span></div>")
    if swipe:
        f += f"<div style=\"position:absolute;right:58px;bottom:44px;font-family:'DM Sans';font-weight:600;font-size:23px;color:{p['accent']};\">Swipe &rarr;</div>"
    return f

def _nuno(p, pose, h=820):
    src = L.nuno_src(pose)
    arc = (f"<div style='position:absolute;right:-70px;bottom:-40px;width:760px;height:760px;border-radius:50%;"
           f"background:radial-gradient(circle at 50% 45%,{p['accent']}2e,{p['accent']}00 66%);'></div>")
    ground = (f"<div style='position:absolute;right:150px;bottom:30px;width:520px;height:66px;border-radius:50%;"
              f"background:radial-gradient(ellipse,rgba(0,0,0,.5),rgba(0,0,0,0) 70%);'></div>")
    img = f"<img src='{src}' style='position:absolute;right:-40px;bottom:0;height:{h}px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.5));'>"
    return arc + ground + img

def _urlpill(p):
    return (f"<div style='display:inline-flex;align-items:center;border:2px solid {p['accent']};border-radius:14px;padding:11px 24px;'>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;color:{p['accent']};\">internwise.co.uk</span></div>")


def _cover(p, copy, total, nuno_pose):
    return (_bg(p) + _nuno(p, nuno_pose) + _head(p, 1, total) + _eyebrow(p, copy.get("eyebrow", "INTERNWISE"))
            + f"<div style=\"position:absolute;left:56px;top:274px;width:520px;font-family:Inter;font-weight:700;"
              f"font-size:64px;line-height:1.02;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            + _footer(p, swipe=True))

def _content(p, n, total, slide):
    num = (f"<div style=\"position:absolute;right:70px;top:250px;font-family:Inter;font-weight:800;font-size:300px;"
           f"line-height:.8;color:{p['accent']};opacity:.10;\">0{n-1}</div>")
    return (_bg(p) + num + _head(p, n, total) + _eyebrow(p, slide.get("tag", "STEP " + str(n - 1)))
            + f"<div style=\"position:absolute;left:56px;top:280px;width:840px;font-family:Inter;font-weight:700;"
              f"font-size:58px;line-height:1.02;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>"
            + f"<div style=\"position:absolute;left:58px;top:470px;width:840px;font-family:'DM Sans';font-weight:500;"
              f"font-size:41px;line-height:1.4;color:{p['mut']};\">{slide['body']}</div>"
            + L.dots("left:58px;bottom:150px;", color=f"{p['accent']}55")
            + L.watermark(w=440, right=-70, bottom=-110, op=.05) + _footer(p, swipe=True))

def _cta(p, copy, total, nuno_pose):
    return (_bg(p) + _nuno(p, nuno_pose, h=780) + _head(p, total, total) + _eyebrow(p, "YOUR MOVE")
            + f"<div style=\"position:absolute;left:56px;top:274px;width:490px;font-family:Inter;font-weight:700;"
              f"font-size:60px;line-height:1.02;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            + f"<div style=\"position:absolute;left:58px;top:500px;width:490px;font-family:'DM Sans';font-weight:500;"
              f"font-size:36px;line-height:1.35;color:{p['mut']};\">{copy.get('cta','')}</div>"
            + f"<div style='position:absolute;left:58px;top:640px;'>{_urlpill(p)}</div>"
            + _footer(p, swipe=False))


# ---- single worlds (no Nuno) ----
def w_tipcard(copy):
    CREAM="#F3EADA"; NAVYT="#152743"; COFFEE="#8A7B62"
    bg = (f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
          f"<div style='position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(138,123,98,.12) 1.5px,transparent 1.5px);background-size:30px 30px;'></div>")
    logo = f"<div style='position:absolute;left:56px;top:52px;'><img src='{L.DARKLOGO}' style='height:{L.LOGO}px;'></div>"
    eb = (f"<div style=\"position:absolute;left:58px;top:196px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{COFFEE};letter-spacing:4px;\">{copy.get('eyebrow','TIP').upper()}</div>"
          f"<div style='position:absolute;left:58px;top:230px;width:64px;height:4px;background:{CORAL};border-radius:2px;'></div>")
    head = (f"<div style=\"position:absolute;left:56px;top:262px;width:760px;font-family:Inter;font-weight:700;font-size:62px;line-height:1.02;letter-spacing:-2px;color:{NAVYT};\">{copy['headline']}</div>")
    pts = copy.get("points", [])
    rows = ""
    for i, pt in enumerate(pts, 1):
        rows += (f"<div style='display:flex;gap:18px;align-items:center;background:#fff;border-radius:16px;box-shadow:0 14px 30px rgba(20,30,50,.1);padding:20px 24px;margin-bottom:16px;'>"
                 f"<div style='flex:0 0 46px;width:46px;height:46px;border-radius:12px;background:{AMBER};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:24px;color:{NAVYT};'>{i}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:29px;color:#1c2740;line-height:1.14;\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;right:64px;top:440px;'>{rows}</div>"
    cta = (f"<div style=\"position:absolute;left:58px;bottom:52px;font-family:Inter;font-weight:700;font-size:28px;color:{NAVYT};\">{copy.get('cta','internwise.co.uk')}</div>")
    return bg + logo + eb + head + body + cta

def w_statement(copy):
    bg = _bg(PAL["navy"])
    logo = L.logo_tl()
    eb = (f"<div style=\"position:absolute;left:58px;top:200px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{AMBER};letter-spacing:4px;\">{copy.get('eyebrow','LEARN').upper()}</div>"
          f"<div style='position:absolute;left:58px;top:234px;width:64px;height:4px;background:{AMBER};border-radius:2px;'></div>")
    head = (f"<div style=\"position:absolute;left:56px;top:270px;width:820px;font-family:Inter;font-weight:700;font-size:64px;line-height:1.0;letter-spacing:-2px;color:{INK};\">{copy['headline']}</div>")
    pts = copy.get("points", [])
    rows = ""
    for pt in pts:
        rows += (f"<div style='display:flex;gap:16px;align-items:center;margin-bottom:20px;'>"
                 f"<div style='flex:0 0 44px;width:44px;height:44px;border-radius:50%;background:{AMBER}1f;border:2px solid {AMBER};display:flex;align-items:center;justify-content:center;'>{L.svg('check',AMBER,24)}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:31px;color:{INK};letter-spacing:-.3px;\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:58px;right:64px;top:470px;'>{rows}</div>"
    cta = (f"<div style='position:absolute;left:56px;bottom:50px;'>{_urlpill(PAL['navy'])}</div>")
    return bg + logo + eb + head + body + cta + L.watermark(op=.04)


CAROUSEL = {"navy", "plum", "teal"}
SINGLE = {"tipcard": w_tipcard, "statement": w_statement}


def render_education(copy, world, out_dir, week_id="adhoc"):
    os.makedirs(out_dir, exist_ok=True)
    if world in CAROUSEL:
        p = PAL[world]
        slides = copy.get("slides", [])
        total = len(slides) + 2                       # cover + content slides + cta
        cover_pose = nuno_ledger.pick(COVER_POOL, week_id, label=f"education/{world}/cover")
        cta_pose   = nuno_ledger.pick(CTA_POOL,   week_id, label=f"education/{world}/cta")
        paths = [L.render(out_dir, "slide_1.png", _cover(p, copy, total, cover_pose))]
        for i, s in enumerate(slides, start=2):
            paths.append(L.render(out_dir, f"slide_{i}.png", _content(p, i, total, s)))
        paths.append(L.render(out_dir, f"slide_{total}.png", _cta(p, copy, total, cta_pose)))
        return paths
    return [L.render(out_dir, "slide_1.png", SINGLE[world](copy))]


if __name__ == "__main__":
    demo = {"eyebrow": "The CV clinic", "headline": "The CV line recruiters skip",
            "slides": [
                {"tag": "The problem", "title": "Duties are not proof", "body": "\"Responsible for the socials\" tells a recruiter nothing about what you actually did."},
                {"tag": "The fix", "title": "Lead with the result", "body": "Swap the duty for an outcome: action, skill, and a number where you have one."},
                {"tag": "Example", "title": "Before and after", "body": "Before: ran the newsletter. After: grew the newsletter to 2,000 readers in 3 months."}],
            "cta": "Build a CV that gets seen. Start free.", "points": ["Lead with results", "Add a number", "Cut vague duties", "Match the advert"]}
    for w in ["navy", "plum", "teal", "tipcard", "statement"]:
        render_education(demo, w, os.path.join(L.OUTROOT, "week14", "_edtest", w))
