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
import os, sys, json, datetime
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
    # --- added week16 (new art directions, UK palette: navy/teal/yellow) ---
    "cream": {"bg": "background-color:#F3EADA;", "grid": False, "accent": GREEN,
              "ink": "#152743", "mut": "#6F6350", "deep": "#152743"},
    "midnight": {"bg": "background:radial-gradient(120% 100% at 22% 0%,#12294a,#0a1830 70%);", "grid": True,
                 "accent": AMBER, "ink": INK, "mut": "#9FB0C8", "deep": "#081020"},
    "slate": {"bg": "background:linear-gradient(155deg,#20504d,#123230 72%);", "grid": False, "accent": AMBER,
              "ink": INK, "mut": "#A9C6C4", "deep": "#0b201f"},
    # --- added week17 (three NEW art directions; UK palette navy/teal/yellow) ---
    # marker : LIGHT study-notes, amber highlighter swipe + hand underline
    "marker": {"bg": "background-color:#F4EFE4;", "grid": False, "accent": AMBER,
               "ink": "#152743", "mut": "#6F6350", "deep": "#152743"},
    # flash  : DARK diagonal-energy, corner wedge + slanted step tab
    "flash": {"bg": "background:linear-gradient(135deg,#152c4f,#0a1830 72%);", "grid": True, "accent": AMBER,
              "ink": INK, "mut": "#9FB0C8", "deep": "#081020"},
    # tabs   : TEAL chaptered "folder tabs" progress system
    "tabs": {"bg": "background:linear-gradient(160deg,#13423f,#0a1f1e 72%);", "grid": False, "accent": AMBER,
             "ink": INK, "mut": "#A9C6C4", "deep": "#071615"},
}

# Cover poses hug the RIGHT edge (compact, right-weighted) so they clear the left
# text column. CTA poses read confident/positive. (See original notes on excluded
# poses: nuno_cv_1 loses its laptop, nuno_utility_2 loses a white sheet on rembg.)
COVER_POOL = ["nuno_cv", "nuno_cv_2", "nuno_cv_3",
              "nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3",
              "nuno_authority_1", "nuno_authority_2", "nuno_authority_3", "nuno_authority_4",
              "nuno_planning_1", "nuno_planning_2", "nuno_planning_3",
              "nuno_cvpile", "nuno_utility_3"]
# NOTE: welcoming/offers/tablet cover poses are TOPIC-ONLY (networking/offer/tech) -
# they must NOT be in the general fallback pool or they land on unrelated topics
# (e.g. a "welcoming" pose on a Graduate Schemes cover). Kept only in TOPIC_POSES.
CTA_POOL = ["nuno_dothis_1", "nuno_dothis_2", "nuno_offers_1",
            "nuno_dothis_4", "nuno_offers_4"]   # + week17 fresh cutouts

# ------------------------------------------------------------ topic-matched hook
# The hook (cover) is the scroll-stopper, so its Nuno must MATCH the topic - not
# just the tone. We narrow the cover pool to the family that fits the carousel's
# subject; the ledger then picks the freshest one in that family (no-repeat).
# Only COVER-SAFE poses appear here (right-weighted, they clear the left text
# column). Topics with no fitting cover-safe pose map to "__need:<family>", which
# logs a request for the specific shot we're missing instead of forcing a wrong
# pose (see request_cover_pose + feedback_request_nuno_pics).
TOPIC_POSES = {
    "cv":         ["nuno_cv_5", "nuno_cv", "nuno_cv_2", "nuno_cv_3", "nuno_cv_4", "nuno_cvpile"],
    "apply":      ["nuno_cv_5", "nuno_cv", "nuno_cv_2", "nuno_cv_3", "nuno_cv_4"],
    "interview":  ["nuno_authority_4", "nuno_authority_1", "nuno_authority_2", "nuno_authority_3"],
    "confidence": ["nuno_authority_4", "nuno_authority_1", "nuno_authority_2", "nuno_authority_3"],
    "plan":       ["nuno_planning_1", "nuno_planning_2", "nuno_planning_3"],
    "mistake":    ["nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3"],
    "think":      ["nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3"],
    "skills":     ["nuno_utility_4", "nuno_utility_3", "nuno_planning_1", "nuno_planning_2"],
    # Cover-safe poses added week16 (compact, right-weighted, verified rembg-clean).
    "linkedin":   ["nuno_tablet_cover", "nuno_cv_5", "nuno_cv_4"],
    "networking": ["nuno_authority_4", "nuno_authority_1", "nuno_authority_2"],
    "offer":      ["nuno_offers_cover"],
    "tech":       ["nuno_tablet_cover"],
}
# Substring found in eyebrow/headline/slide text -> topic key above.
TOPIC_KEYWORDS = [
    ("cover letter", "cv"), ("resume", "cv"), ("cv", "cv"),
    ("application", "apply"), ("apply", "apply"), ("ats", "apply"),
    ("interview", "interview"), ("assessment", "interview"),
    ("imposter", "confidence"), ("confidence", "confidence"), ("nerv", "confidence"),
    ("timeline", "plan"), ("deadline", "plan"), ("schedule", "plan"),
    ("plan", "plan"), ("first day", "plan"),
    ("mistake", "mistake"), ("avoid", "mistake"), ("reject", "mistake"), ("wrong", "mistake"),
    ("strategy", "think"), ("research", "think"), ("hidden", "think"), ("think", "think"),
    ("skill", "skills"), ("portfolio", "tech"), ("project", "skills"), ("experience", "skills"),
    ("linkedin", "linkedin"), ("network", "networking"), ("referral", "networking"),
    ("offer", "offer"), ("salary", "offer"), ("negotiat", "offer"),
    # Career / programme topics -> confident, professional founder (best-fit until a
    # bespoke shot exists). Application-shaped topics -> the CV/apply poses.
    # Spread across families (not all -> authority) so Nuno poses don't collide:
    ("graduate scheme", "plan"), ("graduate", "plan"), ("scheme", "plan"),
    ("career", "confidence"), ("entry-level", "apply"), ("entry level", "apply"),
    ("placement", "apply"), ("first job", "apply"), ("internship", "think"),
]
# Human-readable description of the shot to generate when a topic has no pose.
NEED_DESC = {
    "welcoming": "Nuno warm/open, greeting - for networking & LinkedIn topics (right-weighted so it clears the left text column)",
    "offers": "Nuno celebrating a win / holding an offer letter - for offer & salary topics (compact, right side)",
    "tablet": "Nuno holding a tablet/laptop showing a portfolio - for tech & portfolio topics (right-weighted)",
}
COVER_REQUESTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "content", "nuno_cover_requests.json")


def request_cover_pose(family, copy, week_id):
    """Record that this topic needs a specific cover pose we don't have yet, so it
    surfaces in the Saturday build for the operator to generate (or hand to the
    user). Never blocks the render - the caller falls back to the general pool."""
    try:
        log = json.load(open(COVER_REQUESTS)) if os.path.exists(COVER_REQUESTS) else {"requests": []}
    except Exception:
        log = {"requests": []}
    log["requests"].append({
        "week": week_id, "family": family, "topic": copy.get("eyebrow", ""),
        "headline": copy.get("headline", ""), "need": NEED_DESC.get(family, family),
        "at": datetime.datetime.utcnow().isoformat() + "Z"})
    try:
        os.makedirs(os.path.dirname(COVER_REQUESTS), exist_ok=True)
        json.dump(log, open(COVER_REQUESTS, "w"), indent=2, ensure_ascii=False)
    except Exception:
        pass


def cover_pool_for(copy, week_id):
    """Return the topic-relevant cover-pose pool for this carousel. Matches the
    HEADLINE/eyebrow first (the actual subject) before the slide bodies, so an
    incidental word in a slide (e.g. "CV" inside a Graduate Schemes carousel) can't
    hijack the pose. Falls back to the neutral COVER_POOL when nothing matches (and
    logs a request when the topic fits a family we lack a cover-safe pose for)."""
    primary = " ".join([copy.get("eyebrow", ""), copy.get("headline", "")]).lower()
    body = " ".join(s.get("title", "") + " " + s.get("tag", "") for s in (copy.get("slides") or [])).lower()
    for hay in (primary, primary + " " + body):
        for kw, topic in TOPIC_KEYWORDS:
            if kw in hay:
                poses = TOPIC_POSES.get(topic)
                if isinstance(poses, str) and poses.startswith("__need:"):
                    request_cover_pose(poses.split(":", 1)[1], copy, week_id)
                    return COVER_POOL      # graceful fallback until the shot exists
                if poses:
                    return poses
    return COVER_POOL


# --------------------------------------------------------------- shared bits
def _bg(p):
    grid = ("<div style='position:absolute;inset:0;background-image:"
            "linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),"
            "linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);"
            "background-size:56px 56px;'></div>") if p["grid"] else ""
    return f"<div style='position:absolute;inset:0;{p['bg']}'></div>{grid}"

def _logo(src=None, left=56, top=44, h=L.LOGO):
    return f"<div style='position:absolute;left:{left}px;top:{top}px;'><img src='{src or L.WHT}' style='height:{h}px;'></div>"

def _dot_texture(color, size=36):
    """Subtle dotted grain for otherwise-flat fields (esp. the light cream world)."""
    return (f"<div style='position:absolute;inset:0;background-image:radial-gradient({color} 2px,transparent 2px);"
            f"background-size:{size}px {size}px;'></div>")

def _glow(color, right=-90, bottom=-40, size=680):
    """Soft radial halo seated behind Nuno so he doesn't float on a flat field."""
    return (f"<div style='position:absolute;right:{right}px;bottom:{bottom}px;width:{size}px;height:{size}px;border-radius:50%;"
            f"background:radial-gradient(circle at 50% 45%,{color},transparent 66%);'></div>")

def _blob(color, css, size=180):
    """A small geometric accent (soft square) to break up empty corners."""
    return (f"<div style='position:absolute;{css}width:{size}px;height:{size}px;border-radius:32px;"
            f"background:{color};transform:rotate(12deg);'></div>")

def _barcode(css, color="rgba(255,255,255,.28)", h=64):
    """Boarding-pass barcode motif for the ticket world."""
    bars = "".join(f"<div style='width:{w}px;background:{color};'></div>"
                   for w in [3, 6, 2, 8, 3, 5, 2, 7, 3, 4, 6, 2, 5, 3, 8, 2, 4])
    return (f"<div style='position:absolute;{css}display:flex;gap:5px;align-items:stretch;height:{h}px;'>{bars}</div>")

# Topic -> brand icon (from lanes_common icon set) so every slide carries a
# relevant graphic, not just Nuno + text.
_ICON_MAP = [
    (("problem", "mistake", "avoid", "wrong", "reject", "risk", "trap", "myth"), "x"),
    (("fix", "solution", "solve", "improve", "better", "refresh", "update", "tweak"), "refresh"),
    (("example", "before", "after", "sample", "case", "show", "prove"), "eye"),
    (("result", "impact", "number", "stat", "grow", "boost", "metric", "trend"), "trend"),
    (("research", "find", "discover", "hidden", "search", "spot", "check the"), "search"),
    (("plan", "timeline", "deadline", "schedule", "step", "start", "first", "when"), "calendar"),
    (("network", "connect", "referral", "people", "team", "linkedin"), "users"),
    (("cv", "resume", "application", "apply", "document", "letter", "profile"), "doc"),
    (("interview", "question", "answer", "talk", "assessment"), "chat"),
    (("offer", "salary", "pay", "money", "negotiat", "worth"), "coin"),
    (("goal", "target", "aim", "focus", "match", "fit"), "target"),
    (("skill", "learn", "tip", "idea", "know", "strength"), "bulb"),
]
def _topic_icon(text):
    t = (text or "").lower()
    for keys, ic in _ICON_MAP:
        if any(k in t for k in keys):
            return ic
    return "check"

def _icon_badge(icon, p, css, size=76, radius=20, ink="#fff"):
    return (f"<div style='position:absolute;{css}width:{size}px;height:{size}px;border-radius:{radius}px;"
            f"background:{p['accent']};display:flex;align-items:center;justify-content:center;'>{L.svg(icon, ink, int(size*0.52))}</div>")

def _icon_motif(icon, css, color, size=340):
    """A large, faint line-icon used as a background illustration for empty space."""
    return f"<div style='position:absolute;{css}line-height:0;'>{L.svg(icon, color, size)}</div>"

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
    # Canvas is 1080px wide. After the 132px spine the text starts at x~180, and
    # Nuno's head sits at ~x>=700, so the headline is bounded to width 460 (ends
    # ~x=640) and Nuno is nudged right, keeping the type clear of his face.
    return (_bg(p) + _spine(p, 1, total) + _arc(p) + _nuno_whole(pose, h=800, right=-70)
            + _logo(left=x, top=48)
            + f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:700;font-size:22px;"
              f"color:{p['accent']};letter-spacing:4px;\">{copy.get('eyebrow','INTERNWISE')[:26].upper()}</div>"
            + f"<div style=\"position:absolute;left:{x}px;top:300px;width:460px;font-family:Inter;font-weight:700;"
              f"font-size:66px;line-height:1.05;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
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
    return (_bg(p) + _spine(p, total, total) + _arc(p) + _nuno_whole(pose, h=760, right=-70)
            + f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:700;font-size:22px;"
              f"color:{p['accent']};letter-spacing:4px;\">YOUR MOVE</div>"
            + f"<div style=\"position:absolute;left:{x}px;top:300px;width:450px;font-family:Inter;font-weight:700;"
              f"font-size:58px;line-height:1.05;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            + f"<div style=\"position:absolute;left:{x}px;top:520px;width:430px;font-family:'DM Sans';font-weight:500;"
              f"font-size:34px;line-height:1.35;color:{p['mut']};\">{copy.get('cta','')}</div>"
            + f"<div style='position:absolute;left:{x}px;top:660px;'>{_pill(p)}</div>")


# =================================================================================
#  WORLD 2  -  "poster"  (plum)  : type-led editorial poster, NO photo on cover
# =================================================================================
def cover_poster(p, copy, total, pose):
    # Editorial poster: oversized type on the left, Nuno WHOLE on the right. Kept
    # type-led (no card chrome, no left rail - distinct from bento/spine) but the
    # founder now anchors the hook so it stops the scroll. Headline width is
    # constrained so it always clears Nuno on the right.
    blob = (f"<div style='position:absolute;right:-140px;top:-130px;width:560px;height:560px;border-radius:50%;"
            f"background:radial-gradient(circle at 40% 40%,{p['accent']}33,{p['accent']}00 62%);'></div>")
    eyebrow = (f"<div style='position:absolute;left:56px;top:214px;display:inline-flex;align-items:center;height:48px;padding:0 22px;"
               f"border-radius:24px;background:{p['accent']};'>"
               f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:21px;color:{p['deep']};letter-spacing:3px;\">{copy.get('eyebrow','INTERNWISE')[:24].upper()}</span></div>")
    # Canvas is 1080px wide (screenshot 2x). Nuno's head/shoulder sit at ~x>=500
    # in canvas space, so the headline is bounded to the left column (width 430)
    # and sized so even the longest word clears him - no overlap on any pose.
    head = (f"<div style=\"position:absolute;left:56px;width:430px;top:300px;font-family:Inter;font-weight:800;"
            f"font-size:68px;line-height:1.05;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    rule = f"<div style='position:absolute;left:58px;top:660px;width:120px;height:8px;background:{p['accent']};border-radius:4px;'></div>"
    return (_bg(p) + blob + _arc(p, right=-40, bottom=-40, size=720) + _nuno_whole(pose, h=800, right=-70)
            + _logo(left=56, top=44) + eyebrow + head + rule + _footer(p, swipe=True))

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
            + f"<div style=\"position:absolute;left:56px;top:326px;width:430px;font-family:Inter;font-weight:800;"
              f"font-size:60px;line-height:1.03;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            + f"<div style=\"position:absolute;left:58px;top:560px;width:410px;font-family:'DM Sans';font-weight:500;"
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
    is_linkedin = "linkedin" in (copy.get("headline", "") + " " + copy.get("eyebrow", "")).lower()
    panel = (f"<div style='position:absolute;right:44px;top:150px;bottom:150px;width:470px;border-radius:34px;"
             f"background:linear-gradient(160deg,{p['accent']}26,{p['accent']}08);border:1px solid {p['accent']}33;'></div>")
    linkedin_frame = ""
    if is_linkedin:
        linkedin_frame = (
            f"<div style='position:absolute;right:76px;top:198px;width:395px;height:520px;border-radius:30px;background:#F8FBFF;box-shadow:0 28px 60px rgba(0,0,0,.28);overflow:hidden;'>"
            f"<div style='height:106px;background:#0A66C2;'></div>"
            f"<div style='position:absolute;left:34px;top:36px;width:58px;height:58px;border-radius:10px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:33px;color:#0A66C2;'>in</div>"
            f"<div style='position:absolute;left:34px;top:130px;width:120px;height:120px;border-radius:50%;background:#DDE8F6;border:8px solid #F8FBFF;'></div>"
            f"<div style='position:absolute;left:34px;right:34px;top:282px;height:16px;border-radius:8px;background:#15274322;'></div>"
            f"<div style='position:absolute;left:34px;right:92px;top:318px;height:14px;border-radius:7px;background:#15274318;'></div>"
            f"<div style='position:absolute;left:34px;right:54px;top:368px;height:70px;border-radius:18px;background:#0A66C212;border:1px solid #0A66C233;'></div>"
            f"</div>")
    chip = (f"<div style='position:absolute;right:64px;top:66px;display:inline-flex;align-items:center;height:42px;padding:0 18px;"
            f"border-radius:21px;background:{p['accent']};'><span style=\"font-family:Inter;font-weight:800;font-size:20px;color:{p['deep']};letter-spacing:1px;\">01 / 0{total}</span></div>")
    headcard = _card(
        f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:22px;color:{p['accent']};letter-spacing:4px;margin-bottom:18px;\">{copy.get('eyebrow','INTERNWISE')[:24].upper()}</div>"
        f"<div style=\"font-family:Inter;font-weight:700;font-size:70px;line-height:1.02;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>",
        css="left:56px;top:300px;width:520px;", pad="40px 42px")
    return (_bg(p) + panel + linkedin_frame + _nuno_whole(pose, h=760, right=10) + _logo(left=56, top=44) + chip + headcard
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
#  WORLD 4  -  "frame"  (cream, LIGHT)  : gallery border + corner numeral
# =================================================================================
def _frame_border(p):
    return (f"<div style='position:absolute;left:34px;top:34px;right:34px;bottom:34px;"
            f"border:3px solid {p['deep']};border-radius:6px;'></div>"
            f"<div style='position:absolute;left:48px;top:48px;right:48px;bottom:48px;"
            f"border:1px solid {p['accent']};opacity:.5;'></div>")

def cover_frame(p, copy, total, pose):
    # SCROLL-STOPPING hook: a bold navy headline billboard (huge white type = the
    # dominant focal point, high contrast on cream), an amber energy burst behind a
    # prominent Nuno, and the contents preview demoted to a secondary chip strip.
    x = 56
    NAVYT = p["deep"]
    tex = _dot_texture("rgba(21,39,67,.05)")
    # Energy arc seated low-right behind Nuno (a clean quarter-ring, not a floating band).
    burst = (f"<div style='position:absolute;right:-200px;bottom:-200px;width:720px;height:720px;border-radius:50%;"
             f"border:54px solid {AMBER};opacity:.92;'></div>")
    glow = _glow("rgba(255,177,32,.16)", right=-60, bottom=-30, size=560)
    # Headline billboard kept in the LEFT column only (width 452) so it never overlaps
    # Nuno's head; he is pushed right and clears the card.
    card = (f"<div style='position:absolute;left:{x}px;top:196px;width:452px;background:{NAVYT};border-radius:28px;"
            f"padding:38px 38px 42px;box-shadow:0 34px 66px rgba(21,39,67,.30);'>"
            f"<div style='display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:21px;background:{AMBER};margin-bottom:22px;'>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:19px;color:{NAVYT};letter-spacing:3px;\">{copy.get('eyebrow','GUIDE')[:20].upper()}</span></div>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:72px;line-height:1.0;letter-spacing:-2.2px;color:#fff;word-break:keep-all;\">{copy['headline']}</div></div>")
    tags = [s.get("tag", "") for s in copy.get("slides", []) if s.get("tag")][:3]
    chips = "".join(
        f"<span style=\"display:inline-flex;align-items:center;gap:9px;margin:0 10px 10px 0;padding:10px 16px;border-radius:13px;"
        f"background:{NAVYT};font-family:'DM Sans';font-weight:700;font-size:20px;color:#fff;\">"
        f"<span style='width:22px;height:22px;border-radius:7px;background:{p['accent']};color:#fff;display:inline-flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:13px;'>{i}</span>{t}</span>"
        for i, t in enumerate(tags, 1))
    contents = (f"<div style='position:absolute;left:{x}px;bottom:132px;width:600px;'>"
                f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:15px;color:{p['mut']};letter-spacing:4px;margin-bottom:14px;\">IN THIS GUIDE</div>"
                f"<div style='display:flex;flex-wrap:wrap;'>{chips}</div></div>")
    swipe = (f"<div style=\"position:absolute;left:{x}px;bottom:56px;font-family:'DM Sans';font-weight:800;font-size:22px;"
             f"color:{NAVYT};\">Swipe to begin &rarr;</div>")
    return (_bg(p) + tex + glow + burst + _nuno_whole(pose, h=770, right=-150)
            + _logo(L.DARKLOGO, left=x, top=52) + card + contents + swipe)

def content_frame(p, n, total, slide):
    x = 78
    icon = _topic_icon(slide.get("tag", "") + " " + slide.get("title", ""))
    badge = _icon_badge(icon, p, f"left:{x}px;top:236px;", 78)
    tag = (f"<div style=\"position:absolute;left:{x+98}px;top:246px;font-family:'DM Sans';font-weight:800;font-size:22px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>"
           f"<div style='position:absolute;left:{x+98}px;top:286px;width:56px;height:4px;background:{p['accent']};border-radius:2px;'></div>")
    head = (f"<div style=\"position:absolute;left:{x}px;right:96px;top:362px;font-family:Inter;font-weight:700;"
            f"font-size:60px;line-height:1.04;letter-spacing:-1.6px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:{x}px;right:110px;top:578px;font-family:'DM Sans';font-weight:500;"
            f"font-size:41px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>")
    prog = (f"<div style=\"position:absolute;right:96px;bottom:92px;font-family:Inter;font-weight:700;font-size:24px;"
            f"color:{p['mut']};letter-spacing:2px;\"><span style='color:{p['accent']};'>0{n}</span> / 0{total}</div>")
    motif = _icon_motif(icon, "right:-24px;bottom:-30px;", "rgba(21,39,67,.055)", 360)
    return (_bg(p) + _dot_texture("rgba(21,39,67,.045)") + motif + _frame_border(p)
            + _logo(L.DARKLOGO, left=x, top=70) + badge + tag + head + body + prog)

def cta_frame(p, copy, total, pose):
    x = 78
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;top:296px;width:460px;font-family:Inter;font-weight:800;"
            f"font-size:58px;line-height:1.04;letter-spacing:-1.8px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:{x}px;top:540px;width:430px;font-family:'DM Sans';font-weight:500;"
           f"font-size:33px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + _dot_texture("rgba(21,39,67,.045)") + _glow("rgba(91,146,145,.18)") + _frame_border(p)
            + _nuno_whole(pose, h=700, right=-40)
            + _logo(L.DARKLOGO, left=x, top=70) + eyebrow + head + sub
            + f"<div style='position:absolute;left:{x}px;top:680px;'>{_pill(p, dark_ink=True)}</div>")


# =================================================================================
#  WORLD 5  -  "lens"  (midnight)  : circular spotlight framing Nuno
# =================================================================================
def _lens(p, cx="right:-120px", cy="top:150px", d=780):
    return (f"<div style='position:absolute;{cx};{cy};width:{d}px;height:{d}px;border-radius:50%;"
            f"background:radial-gradient(circle at 50% 45%,{p['accent']}30,{p['accent']}00 62%);'></div>"
            f"<div style='position:absolute;{cx};{cy};width:{d}px;height:{d}px;border-radius:50%;border:2px solid {p['accent']}55;'></div>")

def cover_lens(p, copy, total, pose):
    ring = (f"<div style='position:absolute;right:-150px;bottom:-120px;width:720px;height:720px;border-radius:50%;"
            f"border:56px solid {p['accent']};opacity:.9;'></div>")
    eyebrow = (f"<div style=\"position:absolute;left:56px;top:250px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">{copy.get('eyebrow','INTERNWISE')[:24].upper()}</div>")
    head = (f"<div style=\"position:absolute;left:56px;top:298px;width:470px;font-family:Inter;font-weight:800;"
            f"font-size:68px;line-height:1.04;letter-spacing:-1.8px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    rule = f"<div style='position:absolute;left:58px;top:604px;width:110px;height:7px;background:{p['accent']};border-radius:4px;'></div>"
    deco = (L.dots("left:58px;bottom:150px;", color="rgba(255,177,32,.38)", w=200, h=120)
            + L.watermark(w=320, right=70, bottom=300, op=.05, tint="light"))
    return (_bg(p) + ring + deco + _nuno_whole(pose, h=760, right=-60) + _logo(left=56, top=44) + eyebrow + head + rule
            + _footer(p, swipe=True))

def content_lens(p, n, total, slide):
    icon = _topic_icon(slide.get("tag", "") + " " + slide.get("title", ""))
    badge = (f"<div style='position:absolute;left:56px;top:238px;width:118px;height:118px;border-radius:50%;"
             f"border:5px solid {p['accent']};display:flex;align-items:center;justify-content:center;'>{L.svg(icon, p['accent'], 54)}</div>"
             f"<div style='position:absolute;left:150px;top:228px;width:42px;height:42px;border-radius:50%;background:{p['accent']};"
             f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:20px;color:{p['deep']};'>{n-1}</div>")
    tag = (f"<div style=\"position:absolute;left:210px;top:256px;font-family:'DM Sans';font-weight:700;font-size:22px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>"
           f"<div style=\"position:absolute;left:210px;top:296px;width:630px;font-family:Inter;font-weight:700;"
           f"font-size:52px;line-height:1.05;letter-spacing:-1.4px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:56px;right:90px;top:492px;font-family:'DM Sans';font-weight:500;"
            f"font-size:41px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>")
    prog = (f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;"
            f"color:{p['mut']};letter-spacing:2px;\"><span style='color:{p['accent']};'>0{n}</span> / 0{total}</div>")
    return (_bg(p) + _lens(p, "right:-260px", "top:340px", 620)
            + _icon_motif(icon, "right:-24px;bottom:-30px;", "rgba(255,255,255,.05)", 340)
            + L.dots("right:90px;top:150px;", color="rgba(255,177,32,.30)", w=170, h=110)
            + _logo(left=56, top=44) + badge + tag + body + prog + _footer(p, swipe=True))

def cta_lens(p, copy, total, pose):
    ring = (f"<div style='position:absolute;right:-150px;bottom:-120px;width:700px;height:700px;border-radius:50%;"
            f"border:56px solid {p['accent']};opacity:.9;'></div>")
    eyebrow = (f"<div style=\"position:absolute;left:56px;top:250px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:56px;top:298px;width:450px;font-family:Inter;font-weight:800;"
            f"font-size:58px;line-height:1.04;letter-spacing:-1.8px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:58px;top:540px;width:420px;font-family:'DM Sans';font-weight:500;"
           f"font-size:33px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + ring + _nuno_whole(pose, h=720, right=-60) + _logo(left=56, top=44) + eyebrow + head + sub
            + f"<div style='position:absolute;left:58px;top:690px;'>{_pill(p)}</div>")


# =================================================================================
#  WORLD 6  -  "ticket"  (slate)  : boarding-pass, perforated rail + index tab
# =================================================================================
def _perf(top):
    """A vertical dashed perforation line with punch-holes top and bottom."""
    return (f"<div style='position:absolute;left:250px;top:{top}px;bottom:0;width:0;border-left:3px dashed rgba(255,255,255,.35);'></div>")

def cover_ticket(p, copy, total, pose):
    stub = (f"<div style='position:absolute;left:0;top:0;bottom:0;width:96px;background:{p['accent']};"
            f"display:flex;align-items:center;justify-content:center;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:26px;color:{p['deep']};letter-spacing:6px;"
            f"writing-mode:vertical-rl;transform:rotate(180deg);\">INTERNWISE &middot; 01 / 0{total}</span></div>")
    eyebrow = (f"<div style=\"position:absolute;left:150px;top:250px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">{copy.get('eyebrow','INTERNWISE')[:22].upper()}</div>")
    head = (f"<div style=\"position:absolute;left:150px;top:298px;width:450px;font-family:Inter;font-weight:800;"
            f"font-size:66px;line-height:1.04;letter-spacing:-1.7px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    swipe = (f"<div style=\"position:absolute;left:150px;bottom:56px;font-family:'DM Sans';font-weight:700;font-size:22px;"
             f"color:{p['accent']};\">Swipe to board &rarr;</div>")
    deco = (_barcode("left:150px;top:640px;") + L.dots("left:150px;top:470px;", color="rgba(255,177,32,.32)", w=180, h=100)
            + L.watermark(w=300, right=60, bottom=320, op=.045, tint="light"))
    return (_bg(p) + deco + _nuno_whole(pose, h=760, right=-60) + stub + _logo(left=150, top=44) + eyebrow + head + swipe)

def content_ticket(p, n, total, slide):
    stub = (f"<div style='position:absolute;left:0;top:0;bottom:0;width:96px;background:{p['accent']};"
            f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:60px;"
            f"color:{p['deep']};'>0{n-1}</div>")
    perf = _perf(0).replace("left:250px", "left:96px")
    icon = _topic_icon(slide.get("tag", "") + " " + slide.get("title", ""))
    ibadge = _icon_badge(icon, p, "left:150px;top:214px;", 62, radius=16, ink=p['deep'])
    tag = (f"<div style=\"position:absolute;left:230px;top:230px;font-family:'DM Sans';font-weight:700;font-size:22px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>")
    head = (f"<div style=\"position:absolute;left:150px;right:80px;top:308px;font-family:Inter;font-weight:700;"
            f"font-size:56px;line-height:1.04;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    dash = f"<div style='position:absolute;left:150px;right:80px;top:496px;height:0;border-top:2px dashed rgba(255,255,255,.28);'></div>"
    body = (f"<div style=\"position:absolute;left:150px;right:96px;top:532px;font-family:'DM Sans';font-weight:500;"
            f"font-size:41px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>")
    prog = (f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;"
            f"color:{p['mut']};letter-spacing:2px;\"><span style='color:{p['accent']};'>0{n}</span> / 0{total}</div>")
    return (_bg(p) + stub + perf + _icon_motif(icon, "right:10px;bottom:150px;", "rgba(255,255,255,.06)", 300)
            + _barcode("right:70px;bottom:64px;", h=48) + _logo(left=150, top=44) + ibadge + tag + head + dash + body + prog)

def cta_ticket(p, copy, total, pose):
    stub = (f"<div style='position:absolute;left:0;top:0;bottom:0;width:96px;background:{p['accent']};"
            f"display:flex;align-items:center;justify-content:center;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:24px;color:{p['deep']};letter-spacing:6px;"
            f"writing-mode:vertical-rl;transform:rotate(180deg);\">YOUR MOVE</span></div>")
    head = (f"<div style=\"position:absolute;left:150px;top:298px;width:450px;font-family:Inter;font-weight:800;"
            f"font-size:56px;line-height:1.04;letter-spacing:-1.6px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:150px;top:540px;width:420px;font-family:'DM Sans';font-weight:500;"
           f"font-size:33px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + _nuno_whole(pose, h=720, right=-60) + stub + _logo(left=150, top=44) + head + sub
            + f"<div style='position:absolute;left:150px;top:690px;'>{_pill(p)}</div>")


# =================================================================================
#  SINGLE WORLDS
# =================================================================================
def w_tipcard(copy, week_id='adhoc'):
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

def w_statement(copy, week_id='adhoc'):
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


def w_bigidea(copy, week_id='adhoc'):
    """Bold single-statement 'big idea' - a teal field with an oversized headline
    and the tips as inline chips. Distinct from tipcard (notepad) & statement (list)."""
    p = PAL["slate"]
    bg = _bg(p)
    eb = (f"<div style='position:absolute;left:56px;top:210px;display:inline-flex;align-items:center;height:46px;padding:0 22px;"
          f"border-radius:23px;background:{p['accent']};'><span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;color:{p['deep']};letter-spacing:3px;\">{copy.get('eyebrow','LEARN')[:20].upper()}</span></div>")
    glyph = f"<div style='position:absolute;right:60px;top:150px;font-family:Georgia,serif;font-weight:700;font-size:200px;line-height:.5;color:{p['accent']};opacity:.16;'>&ldquo;</div>"
    head = (f"<div style=\"position:absolute;left:56px;right:70px;top:290px;font-family:Inter;font-weight:800;"
            f"font-size:82px;line-height:1.0;letter-spacing:-2.8px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    chips = ""
    for pt in copy.get("points", [])[:4]:
        chips += (f"<div style='display:inline-flex;align-items:center;gap:12px;margin:0 14px 14px 0;padding:14px 22px;"
                  f"border:1px solid {p['accent']}55;border-radius:16px;background:rgba(255,255,255,.05);'>"
                  f"<span style='width:10px;height:10px;border-radius:50%;background:{p['accent']};'></span>"
                  f"<span style=\"font-family:Inter;font-weight:700;font-size:29px;color:{p['ink']};\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;right:80px;top:640px;'>{chips}</div>"
    band = (f"<div style='position:absolute;left:0;right:0;bottom:0;height:112px;background:{p['accent']};display:flex;align-items:center;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:31px;color:{p['deep']};margin-left:56px;letter-spacing:-.3px;\">{copy.get('cta','internwise.co.uk')}</span></div>")
    return bg + L.logo_tl() + eb + glyph + head + body + band

def w_memo(copy, week_id='adhoc'):
    """Editorial memo single: white strip, serif headline and stamped action list."""
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#6F6350"
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    top = f"<div style='position:absolute;left:0;right:0;top:0;height:150px;background:{NAVYT};'></div>"
    logo = f"<img src='{L.WHT}' style='position:absolute;left:56px;top:42px;height:86px;'>"
    strip = (f"<div style='position:absolute;left:56px;right:56px;top:190px;height:70px;background:#fff;border-top:3px solid {NAVYT};border-bottom:3px solid {NAVYT};display:flex;align-items:center;justify-content:center;'>"
             f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:22px;color:{NAVYT};letter-spacing:4px;\">{copy.get('eyebrow','CAREER MEMO')[:24].upper()}</span></div>")
    head = (f"<div style=\"position:absolute;left:76px;right:76px;top:304px;text-align:center;font-family:Georgia,serif;font-weight:700;font-size:72px;line-height:1.0;color:{NAVYT};\">{copy['headline']}</div>")
    rows = ""
    for i, pt in enumerate(copy.get('points', [])[:4], 1):
        rows += (f"<div style='display:flex;gap:18px;align-items:flex-start;margin-bottom:20px;'>"
                 f"<div style='flex:0 0 44px;height:44px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:20px;color:{NAVYT};'>{i}</div>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:30px;line-height:1.14;color:{NAVYT};\">{pt}</div></div>")
    body = f"<div style='position:absolute;left:104px;right:104px;top:560px;'>{rows}</div>"
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:48px;text-align:center;font-family:'DM Sans';font-weight:800;font-size:25px;color:{COFFEE};\">{copy.get('cta','internwise.co.uk')}</div>")
    return bg + top + logo + strip + head + body + cta

def w_scorecard(copy, week_id='adhoc'):
    """Scorecard single: compact evaluation board with three marked criteria."""
    p = PAL['midnight']
    bg = _bg(p)
    eb = (f"<div style='position:absolute;left:56px;top:196px;height:46px;padding:0 22px;border-radius:6px;background:{p['accent']};display:flex;align-items:center;'>"
          f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:19px;color:{p['deep']};letter-spacing:3px;\">CAREER SCORECARD</span></div>")
    head = (f"<div style=\"position:absolute;left:56px;right:70px;top:282px;font-family:Inter;font-weight:900;font-size:68px;line-height:1.0;letter-spacing:-2px;color:{p['ink']};\">{copy['headline']}</div>")
    pts = (copy.get('points') or [])[:3]
    rows = ""
    for pt in pts:
        rows += (f"<div style='display:grid;grid-template-columns:70px 1fr 70px;align-items:center;gap:18px;border-bottom:1.5px solid rgba(255,255,255,.16);padding:20px 0;'>"
                 f"<div style='width:54px;height:54px;border-radius:10px;background:{p['accent']};display:flex;align-items:center;justify-content:center;'>{L.svg('check',p['deep'],28)}</div>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:30px;line-height:1.13;color:{p['ink']};\">{pt}</div>"
                 f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:22px;color:{p['accent']};\">PASS</div></div>")
    body = f"<div style='position:absolute;left:56px;right:64px;top:570px;'>{rows}</div>"
    return bg + L.logo_tl() + eb + head + body + _footer(p, swipe=False)

def w_splitcard(copy, week_id='adhoc'):
    """Two-panel single: navy header panel (hook + Nuno) over a cream list panel."""
    NAVYT = "#152743"; CREAM = "#F3EADA"; COFFEE = "#6F6350"
    pose = nuno_ledger.pick(cover_pool_for(copy, week_id), week_id, label="education/splitcard")
    top = (f"<div style='position:absolute;left:0;right:0;top:0;height:470px;background:{NAVYT};overflow:hidden;'>"
           f"<img src='{L.WHT}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"
           f"<div style='position:absolute;left:56px;top:170px;display:inline-flex;align-items:center;height:44px;padding:0 20px;border-radius:22px;background:{AMBER};'>"
           f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:19px;color:{NAVYT};letter-spacing:3px;\">{copy.get('eyebrow','LEARN')[:20].upper()}</span></div>"
           f"<div style=\"position:absolute;left:56px;right:360px;top:236px;font-family:Inter;font-weight:800;font-size:56px;line-height:1.02;letter-spacing:-1.8px;color:#fff;word-break:keep-all;\">{copy['headline']}</div>"
           f"<img src='{L.nuno_src(pose)}' style='position:absolute;right:-10px;bottom:-32px;height:470px;filter:drop-shadow(0 18px 28px rgba(0,0,0,.5));'></div>")
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    rows = ""
    for i, pt in enumerate(copy.get("points", [])[:4], 1):
        rows += (f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:24px;'>"
                 f"<div style='flex:0 0 54px;width:54px;height:54px;border-radius:14px;background:{GREEN};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:26px;color:#fff;'>{i}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;color:{NAVYT};line-height:1.16;\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;width:560px;top:540px;'>{rows}</div>"
    portrait = (f"<div style='position:absolute;right:56px;bottom:0;width:360px;height:548px;overflow:hidden;'>"
                f"<img src='{L.nuno_src(pose)}' style='position:absolute;right:-92px;bottom:-24px;height:560px;filter:drop-shadow(0 18px 28px rgba(21,39,67,.18));'>"
                f"</div>")
    cta = (f"<div style='position:absolute;left:56px;bottom:46px;display:flex;align-items:center;gap:13px;'>"
           f"<div style='width:34px;height:34px;border-radius:50%;background:{CORAL};display:flex;align-items:center;justify-content:center;'>"
           f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
           f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;color:{NAVYT};\">{copy.get('cta','internwise.co.uk')}</span></div>")
    return bg + top + portrait + body + cta


# =================================================================================
#  WORLD 7  -  "marker"  (cream, LIGHT)  : study-notes, amber highlighter swipe
# =================================================================================
def _hl_title(text, ink, accent, size=60):
    """Title text with a highlighter stripe painted behind the lower two-thirds -
    the signature 'study notes' device (auto-sizes to any line count)."""
    return (f"<span style=\"font-family:Inter;font-weight:700;font-size:{size}px;line-height:1.14;letter-spacing:-1.6px;"
            f"color:{ink};word-break:keep-all;display:inline;"
            f"background:linear-gradient(transparent 60%,{accent}80 60%);padding:0 4px;\">{text}</span>")

def cover_marker(p, copy, total, pose):
    x = 56
    NAVYT = p["deep"]
    tex = _dot_texture("rgba(21,39,67,.05)")
    glow = _glow("rgba(255,177,32,.16)", right=-60, bottom=-30, size=560)
    eyebrow = (f"<div style='position:absolute;left:{x}px;top:206px;display:inline-flex;align-items:center;height:46px;padding:0 20px;"
               f"border-radius:12px;background:{AMBER};'>"
               f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;color:{NAVYT};letter-spacing:3px;\">{copy.get('eyebrow','GUIDE')[:22].upper()}</span></div>")
    headblock = (f"<div style='position:absolute;left:{x}px;top:296px;width:452px;'>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:68px;line-height:1.04;letter-spacing:-2px;"
                 f"color:{NAVYT};word-break:keep-all;\">{copy['headline']}</div>"
                 f"<div style='margin-top:20px;width:236px;height:20px;background:{AMBER};opacity:.85;"
                 f"transform:rotate(-1.4deg);border-radius:3px;'></div></div>")
    swipe = (f"<div style=\"position:absolute;left:{x}px;bottom:56px;font-family:'DM Sans';font-weight:800;font-size:22px;"
             f"color:{NAVYT};\">Swipe to begin &rarr;</div>")
    return (_bg(p) + tex + glow + _nuno_whole(pose, h=770, right=-150)
            + _logo(L.DARKLOGO, left=x, top=52) + eyebrow + headblock + swipe)

def content_marker(p, n, total, slide):
    x = 78
    NAVYT = p["deep"]; GOLD = "#B07A12"
    icon = _topic_icon(slide.get("tag", "") + " " + slide.get("title", ""))
    numbadge = (f"<div style='position:absolute;left:{x}px;top:232px;width:84px;height:84px;border-radius:18px;background:{AMBER};"
                f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:44px;color:{NAVYT};'>0{n-1}</div>")
    tag = (f"<div style=\"position:absolute;left:{x+104}px;top:250px;font-family:'DM Sans';font-weight:800;font-size:22px;"
           f"color:{GOLD};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>"
           f"<div style='position:absolute;left:{x+104}px;top:290px;width:56px;height:4px;background:{AMBER};border-radius:2px;'></div>")
    titleblock = (f"<div style='position:absolute;left:{x}px;right:96px;top:372px;'>{_hl_title(slide['title'], NAVYT, AMBER, 60)}</div>")
    body = (f"<div style=\"position:absolute;left:{x}px;right:110px;top:540px;font-family:'DM Sans';font-weight:500;"
            f"font-size:41px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>")
    prog = (f"<div style=\"position:absolute;right:96px;bottom:92px;font-family:Inter;font-weight:700;font-size:24px;"
            f"color:{p['mut']};letter-spacing:2px;\"><span style='color:{GOLD};'>0{n}</span> / 0{total}</div>")
    motif = _icon_motif(icon, "right:-24px;bottom:-30px;", "rgba(21,39,67,.05)", 340)
    return (_bg(p) + _dot_texture("rgba(21,39,67,.045)") + motif
            + _logo(L.DARKLOGO, left=x, top=70) + numbadge + tag + titleblock + body + prog)

def cta_marker(p, copy, total, pose):
    x = 78
    NAVYT = p["deep"]; GOLD = "#B07A12"
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{GOLD};letter-spacing:5px;\">YOUR MOVE</div>")
    headblock = (f"<div style='position:absolute;left:{x}px;top:296px;width:452px;'>"
                 f"<div style=\"font-family:Inter;font-weight:800;font-size:58px;line-height:1.04;letter-spacing:-1.8px;"
                 f"color:{NAVYT};word-break:keep-all;\">{copy['headline']}</div>"
                 f"<div style='margin-top:18px;width:210px;height:18px;background:{AMBER};opacity:.85;"
                 f"transform:rotate(-1.4deg);border-radius:3px;'></div></div>")
    sub = (f"<div style=\"position:absolute;left:{x}px;top:560px;width:430px;font-family:'DM Sans';font-weight:500;"
           f"font-size:33px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + _dot_texture("rgba(21,39,67,.045)") + _glow("rgba(255,177,32,.16)")
            + _nuno_whole(pose, h=700, right=-40)
            + _logo(L.DARKLOGO, left=x, top=70) + eyebrow + headblock + sub
            + f"<div style='position:absolute;left:{x}px;top:700px;'>{_pill(p, dark_ink=True)}</div>")


# =================================================================================
#  WORLD 8  -  "flash"  (dark navy)  : diagonal energy, corner wedge + skew tab
# =================================================================================
def _wedge(color, css, size=420, op=.13, corner="bl"):
    clip = {"bl": "polygon(0 100%,0 0,100% 100%)", "tr": "polygon(0 0,100% 0,100% 100%)"}[corner]
    return f"<div style='position:absolute;{css}width:{size}px;height:{size}px;background:{color};clip-path:{clip};opacity:{op};'></div>"

def cover_flash(p, copy, total, pose):
    x = 56
    wedge = _wedge(p['accent'], "left:0;bottom:0;", 440, .12, "bl")
    slash = (f"<div style='position:absolute;left:{x}px;top:238px;width:60px;height:12px;background:{p['accent']};transform:skewX(-26deg);'></div>")
    eyebrow = (f"<div style=\"position:absolute;left:{x+80}px;top:230px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">{copy.get('eyebrow','INTERNWISE')[:22].upper()}</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;top:298px;width:470px;font-family:Inter;font-weight:800;"
            f"font-size:66px;line-height:1.04;letter-spacing:-1.8px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    rule = f"<div style='position:absolute;left:{x+2}px;top:604px;width:120px;height:7px;background:{p['accent']};border-radius:4px;transform:skewX(-26deg);'></div>"
    return (_bg(p) + wedge + _arc(p, right=-60, bottom=-120, size=680) + _nuno_whole(pose, h=760, right=-60)
            + _logo(left=x, top=44) + slash + eyebrow + head + rule
            + _footer(p, swipe=True))

def content_flash(p, n, total, slide):
    icon = _topic_icon(slide.get("tag", "") + " " + slide.get("title", ""))
    tab = (f"<div style='position:absolute;left:44px;top:232px;transform:skewX(-12deg);background:{p['accent']};padding:12px 30px;'>"
           f"<span style='display:inline-block;transform:skewX(12deg);font-family:Inter;font-weight:800;font-size:44px;color:{p['deep']};'>0{n-1}</span></div>")
    tag = (f"<div style=\"position:absolute;left:190px;top:250px;font-family:'DM Sans';font-weight:800;font-size:22px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>"
           f"<div style='position:absolute;left:190px;top:290px;width:56px;height:4px;background:{p['accent']};border-radius:2px;'></div>")
    head = (f"<div style=\"position:absolute;left:56px;right:90px;top:372px;font-family:Inter;font-weight:700;"
            f"font-size:60px;line-height:1.04;letter-spacing:-1.6px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:56px;right:100px;top:560px;font-family:'DM Sans';font-weight:500;"
            f"font-size:41px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>")
    prog = (f"<div style=\"position:absolute;right:58px;top:66px;font-family:Inter;font-weight:700;font-size:24px;"
            f"color:{p['mut']};letter-spacing:2px;\"><span style='color:{p['accent']};'>0{n}</span> / 0{total}</div>")
    return (_bg(p) + _wedge(p['accent'], "right:0;top:0;", 300, .08, "tr")
            + _icon_motif(icon, "right:-20px;bottom:-24px;", "rgba(255,255,255,.05)", 330)
            + _logo(left=56, top=44) + tab + tag + head + body + prog + _footer(p, swipe=True))

def cta_flash(p, copy, total, pose):
    x = 56
    wedge = _wedge(p['accent'], "left:0;bottom:0;", 400, .12, "bl")
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;top:298px;width:450px;font-family:Inter;font-weight:800;"
            f"font-size:58px;line-height:1.04;letter-spacing:-1.8px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:{x}px;top:540px;width:420px;font-family:'DM Sans';font-weight:500;"
           f"font-size:33px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + wedge + _arc(p, right=-60, bottom=-120, size=640) + _nuno_whole(pose, h=720, right=-60)
            + _logo(left=x, top=44) + eyebrow + head + sub
            + f"<div style='position:absolute;left:{x}px;top:690px;'>{_pill(p)}</div>")


# =================================================================================
#  WORLD 9  -  "tabs"  (teal)  : chaptered folder-tab progress system
# =================================================================================
def _folder_tabs(p, active, total, x=56, top=210):
    tabs = ""
    for i in range(1, total + 1):
        on = (i == active)
        tabs += (f"<div style='width:64px;height:{46 if on else 34}px;margin-right:12px;border-radius:13px 13px 0 0;"
                 f"background:{p['accent'] if on else 'rgba(255,255,255,.10)'};display:flex;align-items:flex-end;justify-content:center;"
                 f"padding-bottom:6px;font-family:Inter;font-weight:800;font-size:18px;"
                 f"color:{p['deep'] if on else p['mut']};'>{i:02d}</div>")
    return (f"<div style='position:absolute;left:{x}px;top:{top}px;display:flex;align-items:flex-end;'>{tabs}</div>"
            f"<div style='position:absolute;left:{x}px;right:0;top:{top+46}px;height:4px;background:{p['accent']};'></div>")

def cover_tabs(p, copy, total, pose):
    x = 56
    kicker = (f"<div style=\"position:absolute;left:{x}px;top:300px;font-family:'DM Sans';font-weight:800;font-size:21px;"
              f"color:{p['accent']};letter-spacing:5px;\">{copy.get('eyebrow','INTERNWISE')[:22].upper()}</div>")
    # Headline + an "in this guide" contents preview (fills the cover and reinforces
    # the folder-tab/chapter concept: each row maps to a numbered tab/slide).
    rows = ""
    for i, s in enumerate(copy.get("slides", []), start=2):
        tag = s.get("tag", "")
        if not tag:
            continue
        rows += (f"<div style='display:flex;align-items:center;gap:16px;margin-bottom:15px;'>"
                 f"<div style='width:46px;height:46px;border-radius:12px;background:{p['accent']};display:flex;align-items:center;"
                 f"justify-content:center;font-family:Inter;font-weight:800;font-size:19px;color:{p['deep']};'>{i:02d}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:28px;color:{p['ink']};letter-spacing:-.3px;\">{tag}</span></div>")
    contents = ("" if not rows else
                f"<div style='margin-top:38px;'>"
                f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:15px;color:{p['mut']};letter-spacing:4px;margin-bottom:18px;\">IN THIS GUIDE</div>"
                f"<div style='width:52px;height:4px;background:{p['accent']};border-radius:2px;margin-bottom:22px;'></div>{rows}</div>")
    block = (f"<div style='position:absolute;left:{x}px;top:346px;width:560px;'>"
             f"<div style=\"font-family:Inter;font-weight:800;font-size:66px;line-height:1.04;letter-spacing:-1.8px;"
             f"color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>{contents}</div>")
    swipe = (f"<div style=\"position:absolute;left:{x}px;bottom:56px;font-family:'DM Sans';font-weight:800;font-size:22px;"
             f"color:{p['accent']};\">Open chapter one &rarr;</div>")
    return (_bg(p) + _folder_tabs(p, 1, total) + _arc(p) + _nuno_whole(pose, h=760, right=-60)
            + _logo(left=x, top=44) + kicker + block + swipe)

def content_tabs(p, n, total, slide):
    x = 56
    icon = _topic_icon(slide.get("tag", "") + " " + slide.get("title", ""))
    badge = _icon_badge(icon, p, f"left:{x}px;top:326px;", 76, radius=18, ink=p['deep'])
    tag = (f"<div style=\"position:absolute;left:{x+98}px;top:336px;font-family:'DM Sans';font-weight:800;font-size:22px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>"
           f"<div style='position:absolute;left:{x+98}px;top:376px;width:56px;height:4px;background:{p['accent']};border-radius:2px;'></div>")
    head = (f"<div style=\"position:absolute;left:{x}px;right:90px;top:452px;font-family:Inter;font-weight:700;"
            f"font-size:58px;line-height:1.04;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:{x}px;right:100px;top:632px;font-family:'DM Sans';font-weight:500;"
            f"font-size:40px;line-height:1.42;color:{p['mut']};\">{slide['body']}</div>")
    return (_bg(p) + _folder_tabs(p, n, total, top=150)
            + _icon_motif(icon, "right:-20px;bottom:-24px;", "rgba(255,255,255,.05)", 320)
            + _logo(left=x, top=44) + badge + tag + head + body + _footer(p, swipe=True))

def cta_tabs(p, copy, total, pose):
    x = 56
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:300px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;top:346px;width:450px;font-family:Inter;font-weight:800;"
            f"font-size:56px;line-height:1.04;letter-spacing:-1.7px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:{x}px;top:566px;width:420px;font-family:'DM Sans';font-weight:500;"
           f"font-size:33px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + _folder_tabs(p, total, total) + _arc(p) + _nuno_whole(pose, h=720, right=-60)
            + _logo(left=x, top=44) + eyebrow + head + sub
            + f"<div style='position:absolute;left:{x}px;top:706px;'>{_pill(p)}</div>")


CAROUSEL = {
    "teal": {"cover": cover_spine, "content": content_spine, "cta": cta_spine},
    "plum": {"cover": cover_poster, "content": content_poster, "cta": cta_poster},
    "navy": {"cover": cover_bento, "content": content_bento, "cta": cta_bento},
    "cream": {"cover": cover_frame, "content": content_frame, "cta": cta_frame},
    "midnight": {"cover": cover_lens, "content": content_lens, "cta": cta_lens},
    "slate": {"cover": cover_ticket, "content": content_ticket, "cta": cta_ticket},
    "marker": {"cover": cover_marker, "content": content_marker, "cta": cta_marker},
    "flash": {"cover": cover_flash, "content": content_flash, "cta": cta_flash},
    "tabs": {"cover": cover_tabs, "content": content_tabs, "cta": cta_tabs},
}
SINGLE = {"tipcard": w_tipcard, "statement": w_statement,
          "bigidea": w_bigidea, "splitcard": w_splitcard,
          "memo": w_memo, "scorecard": w_scorecard}

COVER_TONE = {"serious": ["serious", "thoughtful", "practical"],
              "practical": ["practical", "confident", "serious"],
              "upbeat": ["confident", "positive", "practical"]}
CTA_TONE = {"serious": ["confident"], "practical": ["confident", "positive"],
            "upbeat": ["positive", "confident"]}


def render_education(copy, world, out_dir, week_id="adhoc"):
    os.makedirs(out_dir, exist_ok=True)
    copy = {**copy}
    cta = (copy.get("cta") or "").strip()
    if "internwise.co.uk" not in cta.lower():
        copy["cta"] = (cta.rstrip(".") + ". " if cta else "") + "Start at internwise.co.uk"
    if world in CAROUSEL:
        p = PAL[world]; w = CAROUSEL[world]
        slides = copy.get("slides", [])
        total = len(slides) + 2
        tone = copy.get("tone", "practical")
        cover_pose = nuno_ledger.pick(cover_pool_for(copy, week_id), week_id,
                                      label=f"education/{world}/cover", tone=COVER_TONE.get(tone))
        cta_pose = nuno_ledger.pick(CTA_POOL, week_id, label=f"education/{world}/cta",
                                    tone=CTA_TONE.get(tone), exclude={cover_pose})
        paths = [L.render(out_dir, "slide_1.png", w["cover"](p, copy, total, cover_pose))]
        for i, s in enumerate(slides, start=2):
            paths.append(L.render(out_dir, f"slide_{i}.png", w["content"](p, i, total, s)))
        paths.append(L.render(out_dir, f"slide_{total}.png", w["cta"](p, copy, total, cta_pose)))
        return paths
    return [L.render(out_dir, "slide_1.png", SINGLE[world](copy, week_id))]


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
