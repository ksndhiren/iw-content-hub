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
import os, re, sys, json, datetime
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
    # --- added week22 ---------------------------------------------------------
    # The bank held exactly 9 carousel worlds and the lane picks 3 a week while
    # blocking the last 2 weeks, so selection was a locked 3-week cycle and every
    # weekday's look came back on a fixed timetable. Three more give it slack.
    # ledger : LIGHT ruled accounting ledger, numbers live in the margin rule
    "ledger": {"bg": "background-color:#FBF6EA;", "grid": False, "accent": "#C0531F",
               "ink": "#2A2016", "mut": "#7A6A55", "deep": "#2A2016"},
    # grid   : DARK indigo modular blueprint, crosshair + corner coordinates
    "grid": {"bg": "background:linear-gradient(150deg,#241F57,#11102E 74%);", "grid": True, "accent": "#8FA6FF",
             "ink": "#ECEDFB", "mut": "#A6A8CE", "deep": "#0C0B22"},
    # strip  : DARK forest contact-sheet, sprocket holes down both edges
    "strip": {"bg": "background:linear-gradient(170deg,#12342A,#071913 76%);", "grid": False, "accent": "#F2C14E",
              "ink": "#EAF6EF", "mut": "#9CC4AF", "deep": "#06140F"},
}

# Cover poses hug the RIGHT edge (compact, right-weighted) so they clear the left
# text column. CTA poses read confident/positive. (See original notes on excluded
# poses: nuno_cv_1 loses its laptop, nuno_utility_2 loses a white sheet on rembg.)
COVER_POOL = ["nuno_cv", "nuno_cv_2", "nuno_cv_3",
              "nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3",
              "nuno_authority_1", "nuno_authority_2", "nuno_authority_3", "nuno_authority_4",
              "nuno_planning_1", "nuno_planning_2", "nuno_planning_3",
              "nuno_cvpile", "nuno_utility_3", "nuno_howto_4"]
# NOTE: welcoming/offers/tablet cover poses are TOPIC-ONLY (networking/offer/tech) -
# they must NOT be in the general fallback pool or they land on unrelated topics
# (e.g. a "welcoming" pose on a Graduate Schemes cover). Kept only in TOPIC_POSES.
# nuno_dothis_1 is pixel-identical to nuno_thumbsup (see nuno_identity.py), and the
# thumbs-up is banned on education carousels, so it is in no CTA pool.
CTA_POOL = ["nuno_dothis_2", "nuno_offers_1",
            "nuno_dothis_4", "nuno_offers_4", "nuno_dothis_5", "nuno_howto_4"]   # + week21 fresh cutouts
CTA_TOPIC_POSES = {
    "linkedin": ["nuno_phone", "nuno_tablet", "nuno_phone_2"],
    "tech": ["nuno_tablet", "nuno_tablet_cover", "nuno_phone"],
    "networking": ["nuno_phone", "nuno_authority_4", "nuno_authority_1"],
    "apply": ["nuno_dothis_2", "nuno_offers_1", "nuno_dothis_4", "nuno_offers_4", "nuno_dothis_5", "nuno_phone_2", "nuno_howto_4"],
    "cv": ["nuno_dothis_2", "nuno_offers_1", "nuno_dothis_4", "nuno_offers_4", "nuno_dothis_5", "nuno_phone_2", "nuno_howto_4"],
    "bullet_cv": ["nuno_cv_5", "nuno_cv_2", "nuno_cv_3"],
    "job_description": ["nuno_cv_3"],
    "followup": ["nuno_followup_phone", "nuno_phone", "nuno_tablet"],
}

# ------------------------------------------------------------ topic-matched hook
# The hook (cover) is the scroll-stopper, so its Nuno must MATCH the topic - not
# just the tone. We narrow the cover pool to the family that fits the carousel's
# subject; the ledger then picks the freshest one in that family (no-repeat).
# Only COVER-SAFE poses appear here (right-weighted, they clear the left text
# column). Topics with no fitting cover-safe pose map to "__need:<family>", which
# logs a request for the specific shot we're missing instead of forcing a wrong
# pose (see request_cover_pose + feedback_request_nuno_pics).
TOPIC_POSES = {
    "bullet_cv":  ["nuno_cv_4"],
    "job_description": ["nuno_job_description"],
    "cv":         ["nuno_cv_proof_highlight", "nuno_cv_5", "nuno_cv", "nuno_cv_2", "nuno_cv_3", "nuno_cv_4", "nuno_cvpile", "nuno_cv_6", "nuno_cv_8"],
    "apply":      ["nuno_cv_5", "nuno_cv", "nuno_cv_2", "nuno_cv_3", "nuno_cv_4", "nuno_cv_6", "nuno_cv_8"],
    "interview":  ["nuno_interview_door", "nuno_authority_4", "nuno_authority_1", "nuno_authority_2", "nuno_authority_3"],
    "confidence": ["nuno_authority_4", "nuno_authority_1", "nuno_authority_2", "nuno_authority_3", "nuno_howto_4"],
    "plan":       ["nuno_planning_1", "nuno_planning_2", "nuno_planning_3"],
    "mistake":    ["nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3"],
    "think":      ["nuno_thoughtful_1", "nuno_thoughtful_2", "nuno_thoughtful_3"],
    "skills":     ["nuno_utility_4", "nuno_utility_3", "nuno_planning_1", "nuno_planning_2"],
    # Cover-safe poses added week16 (compact, right-weighted, verified rembg-clean).
    "linkedin":   ["nuno_phone", "nuno_tablet", "nuno_phone_2"],
    "networking": ["nuno_authority_4", "nuno_authority_1", "nuno_authority_2"],
    "offer":      ["nuno_offers_cover"],
    "tech":       ["nuno_tablet_cover"],
    "tracker":    ["nuno_tracker_dashboard"],
    "followup":   ["nuno_followup_phone", "nuno_phone", "nuno_tablet"],
}
# Substring found in eyebrow/headline/slide text -> topic key above.
TOPIC_KEYWORDS = [
    ("turn 1 internship into 3 bullets", "bullet_cv"), ("3 bullets", "bullet_cv"), ("into 3 bullets", "bullet_cv"),
    ("decode job descriptions", "job_description"), ("decode job", "job_description"), ("job descriptions", "job_description"), ("job description", "job_description"),
    ("cover letter", "cv"), ("resume", "cv"), ("cv", "cv"),
    ("application", "apply"), ("apply", "apply"), ("ats", "apply"),
    ("interview", "interview"), ("assessment", "interview"),
    ("follow-up", "followup"), ("follow up", "followup"),
    ("imposter", "confidence"), ("confidence", "confidence"), ("nerv", "confidence"),
    ("timeline", "plan"), ("deadline", "plan"), ("schedule", "plan"),
    ("plan", "plan"), ("first day", "plan"),
    ("mistake", "mistake"), ("avoid", "mistake"), ("reject", "mistake"), ("wrong", "mistake"),
    ("strategy", "think"), ("research", "think"), ("hidden", "think"), ("think", "think"),
    ("tracker", "tracker"), ("tracking", "tracker"), ("track", "tracker"),
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
        "at": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z"})
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


def topic_key_for(copy):
    primary = " ".join([copy.get("eyebrow", ""), copy.get("headline", "")]).lower()
    body = " ".join(s.get("title", "") + " " + s.get("tag", "") for s in (copy.get("slides") or [])).lower()
    for hay in (primary, primary + " " + body):
        for kw, topic in TOPIC_KEYWORDS:
            if kw in hay:
                return topic
    return None


def cta_pool_for(copy):
    return CTA_TOPIC_POSES.get(topic_key_for(copy), CTA_POOL)


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

def _fit_h(pose, h, max_w):
    """Height that keeps the cutout within `max_w`. Measures the PNG on disk (the
    rendered src is an inlined data URI, so it cannot be measured). Falls back to
    `h` if the file is missing, so a bad pose name never breaks a render."""
    try:
        from PIL import Image
        f = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "assets", "nuno", str(pose) + ".png")
        w0, h0 = Image.open(f).size
        return int(h0 * max_w / w0) if w0 / h0 * h > max_w else h
    except Exception:
        return h



# Most of the library is portrait (median aspect 0.88), so a height alone used to
# be a safe size. A handful of cutouts are LANDSCAPE - nuno_cv_8 holds the CV out
# at arm's length at 1.47:1 - and at h=740 that is 1086px wide on a 1080px canvas,
# so the cutout reached right across the text column. Cap the drawn WIDTH too and
# let height give way: portrait poses are untouched, wide ones stop overrunning.
MAX_NUNO_W = 700


def _nuno_whole(pose, h=820, right=-40, bottom=0, max_w=MAX_NUNO_W):
    """Founder cut-out placed WHOLE (no crop/zoom/distort) with a soft ground."""
    src = L.nuno_src(pose)
    h = min(h, _fit_h(pose, h, max_w))
    # The ground shadow has to travel with him. It used to be pinned at a literal
    # right:150px, so any world that nudged `right` to clear the type left the
    # shadow behind under empty background.
    ground = (f"<div style='position:absolute;right:{right + 190}px;bottom:30px;width:520px;height:66px;border-radius:50%;"
              f"background:radial-gradient(ellipse,rgba(0,0,0,.5),rgba(0,0,0,0) 70%);'></div>")
    img = f"<img src='{src}' style='position:absolute;right:{right}px;bottom:{bottom}px;height:{h}px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.5));'>"
    return ground + img

def _profile_avatar(left, top, size, border=8):
    src = L.img(os.path.join(L.BASE, "assets", "nuno", "linkedin_profile_blonde_professional.png"))
    inner = size - border * 2
    return (f"<div style='position:absolute;left:{left}px;top:{top}px;width:{size}px;height:{size}px;border-radius:50%;"
            f"background:#F8FBFF;border:{border}px solid #F8FBFF;overflow:hidden;box-shadow:0 8px 22px rgba(21,39,67,.16);'>"
            f"<img src='{src}' style='width:{inner}px;height:{inner}px;object-fit:cover;'>"
            f"</div>")

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
    # Canvas is 1080px wide. After the 132px spine the text starts at x~180. The
    # headline is bounded to width 440 (ends ~x=620) and Nuno is pushed a further
    # 70px off the right edge, so his hairline clears the longest headline line
    # rather than sitting right against it.
    return (_bg(p) + _spine(p, 1, total) + _arc(p) + _nuno_whole(pose, h=800, right=-140)
            + _logo(left=x, top=48)
            + f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:700;font-size:22px;"
              f"color:{p['accent']};letter-spacing:4px;\">{copy.get('eyebrow','INTERNWISE')[:26].upper()}</div>"
            + f"<div style='position:absolute;left:{x}px;top:296px;'>"
              + L.hero(copy['headline'], "stack", p['ink'], p['accent'], hi=p['accent'], size=81, width=440)
              + "</div>"
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
    head = (f"<div style='position:absolute;left:56px;top:298px;'>"
            + L.hero(copy['headline'], "serif_italic", p['ink'], p['accent'], hi=CORAL, size=81, width=430)
            + "</div>")
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
            f"{_profile_avatar(34, 130, 120, border=8)}"
            f"<div style='position:absolute;left:34px;right:34px;top:282px;height:16px;border-radius:8px;background:#15274322;'></div>"
            f"<div style='position:absolute;left:34px;right:92px;top:318px;height:14px;border-radius:7px;background:#15274318;'></div>"
            f"<div style='position:absolute;left:34px;right:54px;top:368px;height:70px;border-radius:18px;background:#0A66C212;border:1px solid #0A66C233;'></div>"
            f"</div>")
    chip = (f"<div style='position:absolute;right:64px;top:66px;display:inline-flex;align-items:center;height:42px;padding:0 18px;"
            f"border-radius:21px;background:{p['accent']};'><span style=\"font-family:Inter;font-weight:800;font-size:20px;color:{p['deep']};letter-spacing:1px;\">01 / 0{total}</span></div>")
    headcard = _card(
        f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:22px;color:{p['accent']};letter-spacing:4px;margin-bottom:18px;\">{copy.get('eyebrow','INTERNWISE')[:24].upper()}</div>"
        + L.hero(copy['headline'], "boxed", p['ink'], p['accent'], hi=p['accent'], size=81, deep=p['deep'], width=436),
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
    is_linkedin = "linkedin" in (copy.get("headline", "") + " " + copy.get("eyebrow", "")).lower()
    if is_linkedin:
        profile = (
            f"<div style='position:absolute;right:74px;top:214px;width:420px;height:600px;border-radius:34px;background:#F8FBFF;"
            f"box-shadow:0 30px 70px rgba(0,0,0,.30);overflow:hidden;'>"
            f"<div style='height:128px;background:#0A66C2;'></div>"
            f"<div style='position:absolute;left:34px;top:38px;width:70px;height:70px;border-radius:14px;background:#fff;"
            f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:950;font-size:38px;color:#0A66C2;'>in</div>"
            f"{_profile_avatar(34, 156, 124, border=8)}"
            f"<div style='position:absolute;left:34px;right:34px;top:316px;height:18px;border-radius:9px;background:#15274326;'></div>"
            f"<div style='position:absolute;left:34px;right:118px;top:354px;height:14px;border-radius:7px;background:#15274318;'></div>"
            f"<div style='position:absolute;left:34px;right:34px;top:418px;height:86px;border-radius:18px;background:#0A66C214;border:1px solid #0A66C233;'></div>"
            f"<div style='position:absolute;left:34px;right:34px;top:530px;height:34px;border-radius:17px;background:{AMBER};'></div>"
            f"</div>")
        card = _card(
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:22px;color:{p['accent']};letter-spacing:4px;margin-bottom:16px;\">YOUR MOVE</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:56px;line-height:1.02;letter-spacing:-2px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:33px;line-height:1.34;color:{p['mut']};margin-top:22px;\">{copy.get('cta','')}</div>",
            css="left:56px;top:280px;width:520px;", pad="40px 42px")
        return (_bg(p) + profile + _logo(left=56, top=44) + card
                + f"<div style='position:absolute;left:96px;bottom:120px;'>{_pill(p)}</div>")
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
    glow = ""
    # Headline billboard kept in the LEFT column only (width 452) so it never overlaps
    # Nuno's head; he is pushed right and clears the card.
    card = (f"<div style='position:absolute;left:{x}px;top:196px;width:452px;background:{NAVYT};border-radius:28px;"
            f"padding:38px 38px 42px;'>"
            f"<div style='display:inline-flex;align-items:center;height:42px;padding:0 20px;border-radius:21px;background:{AMBER};margin-bottom:22px;'>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:19px;color:{NAVYT};letter-spacing:3px;\">{copy.get('eyebrow','GUIDE')[:20].upper()}</span></div>"
            + L.hero(copy['headline'], "highlight", "#fff", AMBER, hi=CORAL, size=81, width=376) + "</div>")
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
    return (_bg(p) + tex + glow + burst + _nuno_whole(pose, h=720, right=-84)
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
    nuno_right = -40
    return (_bg(p) + _dot_texture("rgba(21,39,67,.045)") + _frame_border(p)
            + _nuno_whole(pose, h=700, right=nuno_right)
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
    head = (f"<div style='position:absolute;left:56px;top:296px;'>"
            + L.hero(copy['headline'], "outline", p['ink'], p['accent'], hi=p['accent'], size=81, width=470)
            + "</div>")
    rule = f"<div style='position:absolute;left:58px;top:640px;width:110px;height:7px;background:{p['accent']};border-radius:4px;'></div>"
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
    head = (f"<div style='position:absolute;left:150px;top:294px;'>"
            + L.hero(copy['headline'], "scalejump", p['ink'], p['accent'], hi=p['accent'], size=75, width=450)
            + "</div>")
    swipe = (f"<div style=\"position:absolute;left:150px;bottom:56px;font-family:'DM Sans';font-weight:700;font-size:22px;"
             f"color:{p['accent']};\">Swipe to board &rarr;</div>")
    jd = ""
    if "job description" in copy.get("headline", "").lower():
        jd = (f"<div style='position:absolute;right:72px;top:198px;width:340px;height:440px;background:#F7F1E7;"
              f"border:4px solid {p['accent']};transform:rotate(3deg);box-shadow:12px 12px 0 rgba(255,177,32,.18);'>"
              f"<div style=\"position:absolute;left:28px;top:30px;font-family:'DM Sans';font-weight:900;font-size:18px;color:{p['deep']};letter-spacing:3px;\">JOB DESCRIPTION</div>"
              f"<div style='position:absolute;left:28px;top:88px;width:250px;height:20px;background:{p['deep']};opacity:.9;'></div>"
              f"<div style='position:absolute;left:28px;top:136px;width:210px;height:16px;background:{p['mut']};opacity:.55;'></div>"
              f"<div style='position:absolute;left:28px;top:176px;width:260px;height:18px;background:{p['accent']};'></div>"
              f"<div style='position:absolute;left:28px;top:222px;width:230px;height:16px;background:{p['mut']};opacity:.55;'></div>"
              f"<div style='position:absolute;left:28px;top:264px;width:180px;height:18px;background:{CORAL};'></div>"
              f"<div style='position:absolute;left:28px;top:330px;width:120px;height:120px;border:5px solid {p['deep']};border-radius:50%;display:flex;align-items:center;justify-content:center;'>{L.svg('search',p['deep'],54)}</div></div>")
    deco = (_barcode("left:150px;top:640px;") + jd + L.dots("left:150px;top:470px;", color="rgba(255,177,32,.32)", w=180, h=100)
            + L.watermark(w=300, right=60, bottom=320, op=.045, tint="light"))
    nuno = _nuno_whole(pose, h=720, right=-118) if "job description" in copy.get("headline", "").lower() else _nuno_whole(pose, h=760, right=-60)
    return (_bg(p) + deco + nuno + stub + _logo(left=150, top=44) + eyebrow + head + swipe)

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
    image = _nuno_whole(pose, h=720, right=-60)
    if "job description" in copy.get("headline", "").lower():
        image = _nuno_whole(pose, h=700, right=-70)
    return (_bg(p) + image + stub + _logo(left=150, top=44) + head + sub
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
    head = (f"<div style='position:absolute;left:56px;top:210px;'>"
            + L.hero(copy['headline'], "underline", NAVYT, NAVYT, hi=AMBER, size=58, width=960) + "</div>")
    pts = copy.get("points", [])
    rows = ""
    for i, pt in enumerate(pts, 1):
        rows += (f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:26px;'>"
                 f"<div style='flex:0 0 52px;width:52px;height:52px;border-radius:14px;background:{AMBER};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:800;font-size:26px;color:{NAVYT};'>{i}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:33px;color:#1c2740;line-height:1.16;\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;right:70px;top:452px;'>{rows}</div>"
    cta = (f"<div style='position:absolute;left:56px;bottom:112px;width:560px;display:flex;align-items:center;gap:13px;'>"
           f"<div style='width:34px;height:34px;border-radius:50%;background:{CORAL};display:flex;align-items:center;justify-content:center;'>"
           f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
           f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;color:{NAVYT};\">{copy.get('cta','internwise.co.uk')}</span></div>")
    return bg + rules + band + logo + tab + head + body + cta + L.url_footer(left=56, bottom=46)

def w_statement(copy, week_id='adhoc'):
    """Dark 'manifesto' - oversized ticks and a strong accent band, distinct from
    the carousels' number/spine systems."""
    p = PAL["navy"]
    bg = _bg(p)
    logo = L.logo_tl()
    eb = (f"<div style='position:absolute;left:58px;top:210px;display:inline-flex;align-items:center;height:46px;padding:0 22px;"
          f"border-radius:23px;background:{AMBER};'><span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;color:{DEEP};letter-spacing:3px;\">{copy.get('eyebrow','LEARN')[:20].upper()}</span></div>")
    head = (f"<div style='position:absolute;left:56px;top:282px;'>"
            + L.hero(copy['headline'], "serif_italic", INK, AMBER, hi=AMBER, size=64, width=954) + "</div>")
    pts = copy.get("points", [])
    rows = ""
    for pt in pts:
        rows += (f"<div style='display:flex;gap:20px;align-items:center;margin-bottom:22px;'>"
                 f"<div style='flex:0 0 52px;width:52px;height:52px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>{L.svg('check',DEEP,28)}</div>"
                 f"<span style=\"font-family:Inter;font-weight:700;font-size:33px;color:{INK};letter-spacing:-.3px;line-height:1.15;\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;right:64px;top:500px;'>{rows}</div>"
    # The closing line no longer carries the address (it printed twice), so the
    # band has to show it: sentence at one end, internwise.co.uk at the other.
    band = (f"<div style='position:absolute;left:0;right:0;bottom:0;height:120px;background:{AMBER};display:flex;"
            f"align-items:center;justify-content:space-between;gap:32px;padding:0 56px;box-sizing:border-box;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:32px;color:{DEEP};letter-spacing:-.3px;\">{copy.get('cta','')}</span>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:24px;color:{DEEP};opacity:.74;letter-spacing:.6px;\">{L.URL}</span></div>")
    return bg + logo + eb + head + body + L.watermark(op=.04) + band

def w_message_lab(copy, week_id='adhoc'):
    """Creative DM lab: a bold message-composition interface for outreach topics."""
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#6F6350"
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    rail = f"<div style='position:absolute;left:0;top:0;bottom:0;width:154px;background:{NAVYT};'></div>"
    logo = f"<img src='{L.ICONMARK}' style='position:absolute;left:48px;top:44px;width:66px;filter:brightness(0) invert(1);'>"
    label = (f"<div style=\"position:absolute;left:210px;top:76px;font-family:'DM Sans';font-weight:900;font-size:18px;"
             f"letter-spacing:5px;color:{GREEN};\">MESSAGE LAB</div>"
             f"<div style='position:absolute;left:210px;top:116px;width:86px;height:6px;background:{AMBER};'></div>")
    head = (f"<div style='position:absolute;left:210px;top:174px;'>"
            + L.hero(copy['headline'], "highlight", NAVYT, NAVYT, hi=AMBER, size=56, width=470) + "</div>")
    phone = (f"<div style='position:absolute;right:62px;top:308px;width:300px;height:508px;border-radius:38px;background:{NAVYT};"
             f"box-shadow:16px 16px 0 rgba(21,39,67,.14);border:8px solid #fff;'></div>"
             f"<div style='position:absolute;right:112px;top:370px;width:204px;height:50px;border-radius:25px;background:#fff;'></div>"
             f"<div style='position:absolute;right:104px;top:454px;width:218px;min-height:100px;border-radius:24px 24px 6px 24px;background:{AMBER};padding:18px;'>"
             f"<div style=\"font-family:Inter;font-weight:950;font-size:24px;line-height:1.05;color:{NAVYT};\">Lead with proof, not a favour.</div></div>"
             f"<div style='position:absolute;right:178px;top:604px;width:142px;height:44px;border-radius:22px;background:#fff;'></div>"
             f"<div style='position:absolute;right:106px;top:684px;width:214px;height:82px;border-radius:24px 24px 6px 24px;background:{GREEN};'></div>")
    pts = copy.get("points", [])[:3]
    rows = ""
    for i, pt in enumerate(pts, 1):
        rows += (f"<div style='display:flex;align-items:center;gap:18px;margin-bottom:18px;'>"
                 f"<div style='width:50px;height:50px;border-radius:12px;background:{[AMBER,GREEN,CORAL][i-1]};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:950;font-size:23px;color:{NAVYT};'>{i}</div>"
                 f"<div style=\"font-family:Inter;font-weight:900;font-size:30px;line-height:1.08;color:{NAVYT};\">{pt}</div></div>")
    body = f"<div style='position:absolute;left:210px;top:522px;width:520px;'>{rows}</div>"
    # The footer sits at bottom:44 and stands 34px tall, so a pill at bottom:66
    # ran straight through it. Clear the footer's top edge (78) plus a gap.
    cta = (f"<div style='position:absolute;left:210px;bottom:106px;height:62px;padding:0 28px;border-radius:31px;background:{NAVYT};display:flex;align-items:center;'>"
           f"<span style=\"font-family:Inter;font-weight:900;font-size:26px;color:#fff;\">{copy.get('cta','internwise.co.uk')}</span></div>")
    return bg + rail + logo + label + head + phone + body + cta + L.url_footer(left=210, color=COFFEE)

def w_focus_studio(copy, week_id='adhoc'):
    """High-energy focus board: different from the dark statement list."""
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#6F6350"
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(135deg,{CREAM} 0%,#E9F3F1 100%);'></div>"
    logo = f"<img src='{L.DARKLOGO}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"
    label = (f"<div style='position:absolute;left:58px;top:172px;height:46px;padding:0 20px;background:{AMBER};"
             f"transform:rotate(-2deg);display:flex;align-items:center;'>"
             f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:19px;color:{NAVYT};letter-spacing:3px;\">FOCUS STUDIO</span></div>")
    # Was hardcoded to "Focus Your / Job Hunt" whatever the post said, so any topic
    # other than the one it was built for rendered someone else's headline.
    head = (f"<div style='position:absolute;left:58px;top:254px;'>"
            + L.hero(copy.get('headline', ''), "highlight", NAVYT, CORAL, hi=AMBER, size=68, width=620)
            + "</div>")
    target = (f"<div style='position:absolute;right:70px;top:236px;width:300px;height:300px;border-radius:50%;border:8px solid {NAVYT};'>"
              f"<div style='position:absolute;left:54px;top:54px;width:176px;height:176px;border-radius:50%;border:7px solid {GREEN};'></div>"
              f"<div style='position:absolute;left:116px;top:116px;width:54px;height:54px;border-radius:50%;background:{AMBER};'></div></div>")
    pts = copy.get("points", [])[:4]
    cards = ""
    for i, pt in enumerate(pts):
        x, y, rot, col = [(74, 592, -2, "#fff"), (392, 566, 2.4, AMBER), (688, 608, -1.5, GREEN), (260, 782, 1.5, "#fff")][i]
        cards += (f"<div style='position:absolute;left:{x}px;top:{y}px;width:286px;min-height:108px;background:{col};"
                  f"border:3px solid {NAVYT};box-shadow:10px 10px 0 rgba(21,39,67,.14);transform:rotate({rot}deg);padding:18px;'>"
                  f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:15px;color:{CORAL if col == '#fff' else NAVYT};letter-spacing:3px;\">FOCUS {i+1}</div>"
                  f"<div style=\"margin-top:8px;font-family:Inter;font-weight:950;font-size:27px;line-height:1.04;color:{NAVYT};\">{pt}</div></div>")
    cta = (f"<div style='position:absolute;right:70px;bottom:72px;width:330px;font-family:Inter;font-weight:950;font-size:31px;line-height:1.05;color:{NAVYT};'>"
           f"{copy.get('cta','Start at internwise.co.uk')}</div>")
    return bg + logo + label + head + target + cards + cta + L.url_footer(left=58, color=COFFEE)


def w_bigidea(copy, week_id='adhoc'):
    """Bold single-statement 'big idea' - a teal field with an oversized headline
    and the tips as inline chips. Distinct from tipcard (notepad) & statement (list)."""
    p = PAL["slate"]
    bg = _bg(p)
    eb = (f"<div style='position:absolute;left:56px;top:210px;display:inline-flex;align-items:center;height:46px;padding:0 22px;"
          f"border-radius:23px;background:{p['accent']};'><span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;color:{p['deep']};letter-spacing:3px;\">{copy.get('eyebrow','LEARN')[:20].upper()}</span></div>")
    glyph = f"<div style='position:absolute;right:60px;top:150px;font-family:IWSerif,Georgia,serif;font-weight:700;font-size:200px;line-height:.5;color:{p['accent']};opacity:.16;'>&ldquo;</div>"
    head = (f"<div style='position:absolute;left:56px;top:286px;'>"
            + L.hero(copy['headline'], "scalejump", p['ink'], p['accent'], hi=p['accent'], size=70, width=954) + "</div>")
    chips = ""
    for pt in copy.get("points", [])[:4]:
        chips += (f"<div style='display:inline-flex;align-items:center;gap:12px;margin:0 14px 14px 0;padding:14px 22px;"
                  f"border:1px solid {p['accent']}55;border-radius:16px;background:rgba(255,255,255,.05);'>"
                  f"<span style='width:10px;height:10px;border-radius:50%;background:{p['accent']};'></span>"
                  f"<span style=\"font-family:Inter;font-weight:700;font-size:29px;color:{p['ink']};\">{pt}</span></div>")
    body = f"<div style='position:absolute;left:56px;right:80px;top:640px;'>{chips}</div>"
    band = (f"<div style='position:absolute;left:0;right:0;bottom:0;height:112px;background:{p['accent']};display:flex;"
            f"align-items:center;justify-content:space-between;gap:32px;padding:0 56px;box-sizing:border-box;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:31px;color:{p['deep']};letter-spacing:-.3px;\">{copy.get('cta','')}</span>"
            f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:23px;color:{p['deep']};opacity:.74;letter-spacing:.6px;\">{L.URL}</span></div>")
    return bg + L.logo_tl() + eb + glyph + head + body + band

def w_memo(copy, week_id='adhoc'):
    """Tracker-board single: deliberately kinetic, built for job-search chaos."""
    CREAM = "#F3EADA"; NAVYT = "#152743"; COFFEE = "#6F6350"
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(135deg,{CREAM} 0%,#EAF4F2 100%);'></div>"
    noise = _dot_texture("rgba(21,39,67,.055)", size=28)
    navy = f"<div style='position:absolute;right:0;top:0;bottom:0;width:360px;background:{NAVYT};'></div>"
    logo = f"<img src='{L.DARKLOGO}' style='position:absolute;left:56px;top:46px;height:82px;'>"
    label = (f"<div style='position:absolute;left:58px;top:176px;height:46px;padding:0 20px;background:{AMBER};"
             f"transform:rotate(-1.5deg);display:flex;align-items:center;box-shadow:8px 8px 0 rgba(21,39,67,.12);'>"
             f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:19px;color:{NAVYT};letter-spacing:3px;\">{copy.get('eyebrow','SEARCH RESET')[:22].upper()}</span></div>")
    # The headline is split so the LAST word carries the serif/highlight emphasis
    # (the approved word-level treatment). Both halves come from the post - this
    # world used to hardcode "Stop Your Job Search / Chaos", which contradicted
    # the eyebrow and bullets on any other topic.
    _hl = (copy.get("headline") or "Stop Your Job Search Chaos").split()
    _lead, _emph = " ".join(_hl[:-1]) or _hl[-1], _hl[-1] if len(_hl) > 1 else ""
    _emph_size = 116 if len(_emph) <= 7 else (92 if len(_emph) <= 10 else 74)
    head = (f"<div style='position:absolute;left:58px;top:250px;width:660px;'>"
            f"<div style=\"font-family:Inter;font-weight:950;font-size:72px;line-height:.96;letter-spacing:-2.5px;color:{NAVYT};\">{_lead}</div>"
            + (f"<div style=\"display:inline-block;margin-top:4px;font-family:IWSerif,Georgia,serif;font-style:italic;font-weight:700;font-size:{_emph_size}px;line-height:.9;color:{CORAL};"
               f"background:linear-gradient(transparent 62%,{AMBER} 62%);padding:0 10px;transform:rotate(-2deg);\">{_emph}</div>" if _emph else "")
            + "</div>")
    scribble = (f"<svg style='position:absolute;left:72px;top:466px;width:500px;height:92px;' viewBox='0 0 500 92' fill='none'>"
                f"<path d='M8 74 C110 8,176 104,276 30 S420 18,492 62' stroke='{CORAL}' stroke-width='12' stroke-linecap='round' opacity='.75'/>"
                f"<path d='M22 54 C118 14,178 84,270 26 S398 20,474 50' stroke='{AMBER}' stroke-width='5' stroke-linecap='round'/></svg>")
    # Four cards on the board; a fifth bullet (when the post has one) becomes the
    # side pull rather than a sixth card, so it is never shown twice.
    pts = (copy.get('points') or [])
    board_pts = pts[:4]
    board = ""
    positions = [(88, 590, -3, AMBER), (378, 564, 2.5, GREEN), (666, 606, -1.8, CORAL),
                 (228, 790, 2.2, "#fff"), (548, 810, -2.8, AMBER)]
    for i, pt in enumerate(board_pts):
        left, top, rot, color = positions[i]
        dark = color in (AMBER, GREEN, CORAL)
        board += (f"<div style='position:absolute;left:{left}px;top:{top}px;width:252px;min-height:124px;background:{color};"
                  f"border:3px solid {NAVYT};box-shadow:10px 10px 0 rgba(21,39,67,.18);transform:rotate({rot}deg);padding:18px 18px 16px;'>"
                  f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:17px;color:{NAVYT if dark else CORAL};letter-spacing:3px;\">STEP {i+1}</div>"
                  f"<div style=\"margin-top:8px;font-family:Inter;font-weight:950;font-size:28px;line-height:1.04;color:{NAVYT};letter-spacing:-.8px;\">{pt}</div></div>")
    wire = ("<svg style='position:absolute;left:44px;top:540px;width:970px;height:390px;' viewBox='0 0 970 390' fill='none'>"
            f"<path d='M120 80 L410 60 L700 116 L290 280 L610 300' stroke='{NAVYT}' stroke-width='5' stroke-dasharray='14 14' opacity='.28'/></svg>")
    alert = (f"<div style='position:absolute;right:54px;top:230px;width:248px;height:248px;border-radius:50%;border:18px solid {AMBER};"
             f"display:flex;align-items:center;justify-content:center;'>"
             f"<div style=\"font-family:Inter;font-weight:950;font-size:116px;color:#fff;line-height:1;\">?</div></div>")
    # Side pull: a real line from the post (a 5th bullet beyond the four board
    # cards), never a hardcoded sentence. Empty when the post has nothing spare.
    _pull = (copy.get("pull") or (pts[4] if len(pts) > 4 else "")).strip()
    side = (f"<div style=\"position:absolute;right:70px;top:790px;width:220px;font-family:'DM Sans';font-weight:900;font-size:28px;"
            f"line-height:1.08;color:#fff;\">{_pull}</div>") if _pull else ""
    cta = (f"<div style='position:absolute;left:58px;bottom:118px;height:62px;padding:0 26px;border-radius:31px;background:{NAVYT};"
           f"display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:27px;color:#fff;'>{copy.get('cta','Organise at internwise.co.uk')}</div>")
    return bg + noise + navy + wire + logo + label + head + scribble + board + alert + side + cta + L.url_footer(left=58, bottom=48)

def w_scorecard(copy, week_id='adhoc'):
    """Scorecard single: compact evaluation board with three marked criteria."""
    p = PAL['midnight']
    bg = _bg(p)
    eb = (f"<div style='position:absolute;left:56px;top:196px;height:46px;padding:0 22px;border-radius:6px;background:{p['accent']};display:flex;align-items:center;'>"
          f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:19px;color:{p['deep']};letter-spacing:3px;\">CAREER SCORECARD</span></div>")
    head = (f"<div style='position:absolute;left:56px;top:278px;'>"
            + L.hero(copy['headline'], "shadow", p['ink'], p['accent'], hi=CORAL, size=58,
                     width=954) + "</div>")
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
           f"<div style='position:absolute;left:56px;top:222px;'>"
           + L.hero(copy['headline'], "stack", "#fff", AMBER, hi=AMBER, size=46, width=664) + "</div>"
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
    cta = (f"<div style='position:absolute;left:56px;bottom:112px;width:560px;display:flex;align-items:center;gap:13px;'>"
           f"<div style='width:34px;height:34px;border-radius:50%;background:{CORAL};display:flex;align-items:center;justify-content:center;'>"
           f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
           f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;color:{NAVYT};\">{copy.get('cta','internwise.co.uk')}</span></div>")
    return bg + top + portrait + body + cta + L.url_footer(left=56, bottom=46)


def w_answerbank(copy, week_id='adhoc'):
    """Highly-visual single for interview answer-bank topics.

    Uses a vault/card-index metaphor so it does not feel like the regular
    education singles or employer cards. Built with protected text zones and no
    duplicated Nuno image.
    """
    NAVYT = "#152743"; CREAM = "#F3EADA"; COFFEE = "#6F6350"
    pts = (copy.get("points") or [])[:5]
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(120% 90% at 72% 18%,#1D4E63 0%,{NAVYT} 48%,#07111F 100%);'></div>"
          f"<div style='position:absolute;inset:0;opacity:.22;background-image:linear-gradient(rgba(255,255,255,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.13) 1px,transparent 1px);background-size:44px 44px;'></div>")
    glow = (f"<div style='position:absolute;right:-190px;top:94px;width:620px;height:620px;border-radius:50%;background:{AMBER};opacity:.14;'></div>"
            f"<div style='position:absolute;left:-180px;bottom:-160px;width:500px;height:500px;border-radius:50%;background:{GREEN};opacity:.12;'></div>")
    logo = f"<img src='{L.WHT}' style='position:absolute;left:56px;top:44px;height:{L.LOGO}px;'>"
    eyebrow = (f"<div style='position:absolute;left:60px;top:172px;height:44px;padding:0 18px;border-radius:0;background:{AMBER};"
               f"box-shadow:8px 8px 0 rgba(0,0,0,.22);display:flex;align-items:center;transform:rotate(-1deg);'>"
               f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:18px;color:{NAVYT};letter-spacing:3px;\">{copy.get('eyebrow','INTERVIEW PREP')[:22].upper()}</span></div>")
    # Was hardcoded to "Build a / Smarter / Answer Bank" regardless of the post.
    title = (f"<div style='position:absolute;left:56px;top:244px;'>"
             + L.hero(copy.get('headline', ''), "highlight", "#fff", AMBER, hi=CORAL, size=62, width=560)
             + "</div>")
    vault = (f"<div style='position:absolute;right:58px;top:190px;width:360px;height:390px;border-radius:34px;background:{CREAM};"
             f"box-shadow:0 32px 70px rgba(0,0,0,.36);border:4px solid rgba(255,255,255,.36);overflow:hidden;'>"
             f"<div style='position:absolute;left:0;right:0;top:0;height:74px;background:{AMBER};'></div>"
             f"<div style=\"position:absolute;left:28px;top:24px;font-family:'DM Sans';font-weight:950;font-size:18px;letter-spacing:4px;color:{NAVYT};\">PROOF FILES</div>"
             f"<div style='position:absolute;left:58px;top:118px;width:244px;height:244px;border-radius:50%;border:18px solid {NAVYT};display:flex;align-items:center;justify-content:center;'>"
             f"<div style='width:126px;height:126px;border-radius:50%;background:{GREEN};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:950;font-size:64px;color:{NAVYT};'>5</div></div>"
             f"</div>")
    cards = ""
    colors = ["#fff", AMBER, GREEN, "#fff", CORAL]
    # Card 5 used to sit at x=510 and run under the CTA box (which starts at x~660)
    # whenever its line wrapped; cards 4-5 now finish left of it.
    positions = [(86, 622, -2), (328, 586, 2.2), (584, 628, -1.3), (96, 800, 1.5), (366, 826, -2.3)]
    for i, pt in enumerate(pts):
        left, top, rot = positions[i]
        color = colors[i]
        cards += (f"<div style='position:absolute;left:{left}px;top:{top}px;width:238px;min-height:112px;background:{color};"
                  f"border:3px solid {NAVYT};box-shadow:10px 10px 0 rgba(0,0,0,.22);transform:rotate({rot}deg);padding:16px 18px;'>"
                  f"<div style=\"font-family:'DM Sans';font-weight:950;font-size:14px;color:{NAVYT};letter-spacing:3px;\">CARD {i+1}</div>"
                  f"<div style=\"margin-top:8px;font-family:Inter;font-weight:950;font-size:25px;line-height:1.03;color:{NAVYT};letter-spacing:-.6px;\">{pt}</div></div>")
    connector = (f"<svg style='position:absolute;left:54px;top:548px;width:930px;height:360px;' viewBox='0 0 930 360' fill='none'>"
                 f"<path d='M44 140 C210 40,326 190,482 96 S748 42,884 210' stroke='{AMBER}' stroke-width='8' stroke-linecap='round' stroke-dasharray='18 18' opacity='.5'/>"
                 f"</svg>")
    cta = (f"<div style='position:absolute;right:58px;bottom:64px;width:314px;padding:22px 24px;border-radius:0;background:#fff;"
           f"box-shadow:10px 10px 0 {AMBER};border:3px solid {NAVYT};'>"
           f"<div style=\"font-family:Inter;font-weight:950;font-size:28px;line-height:1.05;color:{NAVYT};letter-spacing:-.6px;\">{copy.get('cta','Start at internwise.co.uk')}</div></div>")
    footer = f"<div style=\"position:absolute;left:58px;bottom:54px;font-family:'DM Sans';font-weight:900;font-size:21px;color:{CREAM};letter-spacing:.4px;\">internwise.co.uk</div>"
    return bg + glow + connector + logo + eyebrow + title + vault + cards + cta + footer


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
    if "first 30" in copy.get("headline", "").lower() or pose == "nuno_interview_door":
        pose = "nuno_interview_door"
        bg = (f"<div style='position:absolute;inset:0;background:#F4EFE4;'></div>"
              f"<div style='position:absolute;inset:0;opacity:.34;background-image:radial-gradient(rgba(21,39,67,.10) 1.7px,transparent 1.7px);background-size:34px 34px;'></div>")
        ink_slab = (f"<div style='position:absolute;right:0;top:0;width:420px;height:1080px;background:{NAVYT};'></div>"
                    f"<div style='position:absolute;right:260px;top:0;width:260px;height:1080px;background:{AMBER};clip-path:polygon(72% 0,100% 0,32% 100%,0 100%);opacity:.92;'></div>")
        stopwatch = (f"<svg style='position:absolute;right:106px;top:172px;width:520px;height:520px;opacity:.22;' viewBox='0 0 520 520' fill='none'>"
                     f"<circle cx='260' cy='282' r='192' stroke='#fff' stroke-width='16'/>"
                     f"<path d='M260 282V154M260 282L356 336' stroke='{AMBER}' stroke-width='18' stroke-linecap='round'/>"
                     f"<rect x='214' y='38' width='92' height='54' rx='18' fill='{AMBER}'/>"
                     f"</svg>")
        door = (f"<div style='position:absolute;right:126px;bottom:92px;width:252px;height:590px;border:4px solid rgba(255,255,255,.22);'></div>"
                f"<div style='position:absolute;right:158px;bottom:138px;width:176px;height:496px;background:rgba(255,255,255,.08);'></div>")
        head = (f"<div style='position:absolute;left:62px;top:242px;width:650px;'>"
                f"<div style=\"font-family:Inter;font-weight:950;font-size:78px;line-height:.92;letter-spacing:-3.2px;color:{NAVYT};\">Nail the</div>"
                f"<div style=\"margin-top:6px;font-family:IWSerif,Georgia,serif;font-style:italic;font-weight:700;font-size:168px;line-height:.82;color:{AMBER};text-shadow:7px 7px 0 {NAVYT};\">First</div>"
                f"<div style='display:flex;align-items:flex-end;gap:18px;margin-top:10px;'>"
                f"<div style=\"font-family:Inter;font-weight:950;font-size:164px;line-height:.78;letter-spacing:-8px;color:transparent;-webkit-text-stroke:5px {NAVYT};text-stroke:5px {NAVYT};\">30</div>"
                f"<div style=\"font-family:Inter;font-weight:950;font-size:64px;line-height:.9;color:{NAVYT};letter-spacing:-2px;margin-bottom:9px;\">SECONDS</div>"
                f"</div></div>")
        label = (f"<div style='position:absolute;left:64px;top:176px;height:46px;padding:0 20px;background:{NAVYT};display:flex;align-items:center;box-shadow:8px 8px 0 {AMBER};'>"
                 f"<span style=\"font-family:'DM Sans';font-weight:950;font-size:18px;color:#fff;letter-spacing:4px;\">INTERVIEW ENTRANCE</span></div>")
        note = (f"<div style='position:absolute;left:68px;top:704px;width:420px;font-family:\"DM Sans\";font-weight:850;font-size:28px;line-height:1.2;color:#6F6350;'>"
                f"Show calm before your first answer even starts.</div>")
        nuno = (f"<img src='{L.nuno_src(pose)}' style='position:absolute;right:40px;bottom:28px;height:710px;"
                f"filter:drop-shadow(0 24px 36px rgba(0,0,0,.38));'>")
        swipe = (f"<div style=\"position:absolute;left:64px;bottom:56px;font-family:'DM Sans';font-weight:900;font-size:24px;color:{NAVYT};\">Swipe in prepared &rarr;</div>")
        return bg + ink_slab + stopwatch + door + _logo(L.DARKLOGO, left=56, top=48) + label + head + note + nuno + swipe
    tex = _dot_texture("rgba(21,39,67,.05)")
    glow = _glow("rgba(255,177,32,.16)", right=-60, bottom=-30, size=560)
    eyebrow = (f"<div style='position:absolute;left:{x}px;top:206px;display:inline-flex;align-items:center;height:46px;padding:0 20px;"
               f"border-radius:12px;background:{AMBER};'>"
               f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;color:{NAVYT};letter-spacing:3px;\">{copy.get('eyebrow','GUIDE')[:22].upper()}</span></div>")
    headblock = (f"<div style='position:absolute;left:{x}px;top:292px;width:452px;'>"
                 + L.hero(copy['headline'], "underline", NAVYT, NAVYT, hi=AMBER, size=78, width=452)
                 + "</div>")
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
    if "proof" in copy.get("headline", "").lower():
        pose = "nuno_cv_proof_highlight"
        bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(120% 100% at 70% 18%,#203F66 0%,#11284A 46%,#071528 100%);'></div>"
              f"<div style='position:absolute;inset:0;opacity:.26;background-image:linear-gradient(rgba(255,255,255,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.13) 1px,transparent 1px);background-size:54px 54px;'></div>")
        evidence = (f"<div style='position:absolute;left:58px;top:182px;height:48px;padding:0 22px;border:3px solid {AMBER};display:flex;align-items:center;transform:rotate(-1.2deg);'>"
                    f"<span style=\"font-family:'DM Sans';font-weight:950;font-size:18px;color:{AMBER};letter-spacing:4px;\">EVIDENCE FIRST</span></div>"
                    f"<div style='position:absolute;left:720px;top:114px;width:320px;height:770px;border:3px solid rgba(255,255,255,.18);transform:rotate(4deg);'></div>"
                    f"<div style='position:absolute;left:760px;top:154px;width:280px;height:710px;border:3px solid rgba(255,177,32,.22);transform:rotate(-3deg);'></div>")
        head = (f"<div style='position:absolute;left:58px;top:284px;width:620px;'>"
                f"<div style=\"font-family:Inter;font-weight:950;font-size:84px;line-height:.9;letter-spacing:-3.5px;color:#fff;\">Add</div>"
                f"<div style=\"display:inline-block;margin-top:8px;font-family:IWSerif,Georgia,serif;font-style:italic;font-weight:700;font-size:152px;line-height:.82;color:{AMBER};background:linear-gradient(transparent 60%,{CORAL} 60%);padding:0 12px;transform:rotate(-2deg);\">Proof</div>"
                f"<div style=\"margin-top:16px;font-family:Inter;font-weight:950;font-size:78px;line-height:.9;letter-spacing:-3px;color:#fff;\">before you</div>"
                f"<div style=\"margin-top:8px;font-family:Inter;font-weight:950;font-size:78px;line-height:.9;letter-spacing:-3px;color:transparent;-webkit-text-stroke:3px #fff;text-stroke:3px #fff;\">polish</div></div>")
        chips = (f"<div style='position:absolute;left:62px;top:780px;display:flex;gap:14px;'>"
                 f"<div style='height:42px;padding:0 17px;border-radius:21px;background:#fff;display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:18px;color:{p['deep']};'>numbers</div>"
                 f"<div style='height:42px;padding:0 17px;border-radius:21px;background:{GREEN};display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:18px;color:{p['deep']};'>tools</div>"
                 f"<div style='height:42px;padding:0 17px;border-radius:21px;background:{CORAL};display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:18px;color:#fff;'>outcomes</div></div>")
        nuno = (f"<div style='position:absolute;right:-4px;bottom:-16px;width:650px;height:740px;border-radius:360px 0 0 0;background:radial-gradient(circle at 48% 48%,rgba(255,177,32,.16),transparent 60%);'></div>"
                f"<img src='{L.nuno_src(pose)}' style='position:absolute;right:-28px;bottom:-4px;height:610px;filter:drop-shadow(0 24px 38px rgba(0,0,0,.55));'>")
        return bg + evidence + _logo(left=56, top=44) + head + chips + nuno + _footer(p, swipe=True)
    wedge = _wedge(p['accent'], "left:0;bottom:0;", 440, .12, "bl")
    slash = (f"<div style='position:absolute;left:{x}px;top:238px;width:60px;height:12px;background:{p['accent']};transform:skewX(-26deg);'></div>")
    eyebrow = (f"<div style=\"position:absolute;left:{x+80}px;top:230px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">{copy.get('eyebrow','INTERNWISE')[:22].upper()}</div>")
    if "rejection" in copy.get("headline", "").lower():
        head = (f"<div style='position:absolute;left:{x}px;top:292px;width:560px;'>"
                f"<div style=\"font-family:Inter;font-weight:950;font-size:94px;line-height:.86;letter-spacing:-4px;color:{p['ink']};\">Break</div>"
                f"<div style=\"display:inline-block;margin-top:12px;font-family:IWSerif,Georgia,serif;font-style:italic;font-weight:700;font-size:100px;line-height:.88;color:{CORAL};"
                f"background:linear-gradient(transparent 58%,{p['accent']} 58%);padding:0 10px;transform:rotate(-2deg);\">Rejection</div>"
                f"<div style=\"margin-top:12px;font-family:Inter;font-weight:950;font-size:88px;line-height:.88;letter-spacing:-3px;color:transparent;"
                f"-webkit-text-stroke:3px {p['ink']};text-stroke:3px {p['ink']};\">Cycle</div></div>")
        rule = f"<div style='position:absolute;left:{x+6}px;top:708px;width:210px;height:9px;background:{p['accent']};border-radius:4px;transform:skewX(-26deg);'></div>"
    else:
        head = (f"<div style='position:absolute;left:{x}px;top:294px;'>"
                + L.hero(copy['headline'], "shadow", p['ink'], p['accent'], hi=CORAL, size=75, width=470)
                + "</div>")
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
    if "follow-up" in copy.get("headline", "").lower() or pose == "nuno_followup_phone":
        pose = "nuno_followup_phone"
        bg = (f"<div style='position:absolute;inset:0;background:linear-gradient(155deg,#0A3835 0%,#0B201F 72%);'></div>"
              f"<div style='position:absolute;left:-180px;top:520px;width:520px;height:520px;border-radius:50%;background:{AMBER};opacity:.12;'></div>"
              f"<div style='position:absolute;right:-130px;top:110px;width:620px;height:620px;border-radius:50%;background:{GREEN};opacity:.13;'></div>")
        composer = (f"<div style='position:absolute;left:532px;top:192px;width:432px;height:574px;border-radius:30px;background:#F4EFE4;box-shadow:0 36px 70px rgba(0,0,0,.34);overflow:hidden;transform:rotate(2deg);'>"
                    f"<div style='position:absolute;left:0;right:0;top:0;height:72px;background:#fff;border-bottom:3px solid {AMBER};'></div>"
                    f"<div style='position:absolute;left:30px;top:26px;width:14px;height:14px;border-radius:50%;background:{CORAL};'></div>"
                    f"<div style='position:absolute;left:56px;top:26px;width:14px;height:14px;border-radius:50%;background:{AMBER};'></div>"
                    f"<div style='position:absolute;left:82px;top:26px;width:14px;height:14px;border-radius:50%;background:{GREEN};'></div>"
                    f"<div style='position:absolute;left:34px;top:118px;width:330px;height:22px;border-radius:11px;background:rgba(21,39,67,.18);'></div>"
                    f"<div style='position:absolute;left:34px;top:174px;width:260px;height:18px;border-radius:9px;background:rgba(21,39,67,.13);'></div>"
                    f"<div style='position:absolute;left:34px;top:222px;width:348px;height:120px;border-radius:18px;background:#fff;border:3px solid rgba(21,39,67,.12);'></div>"
                    f"<div style='position:absolute;left:34px;bottom:34px;width:146px;height:50px;border-radius:25px;background:{AMBER};'></div>"
                    f"</div>")
        trail = (f"<svg style='position:absolute;left:76px;top:240px;width:900px;height:700px;' viewBox='0 0 900 700' fill='none'>"
                 f"<path d='M24 600 C198 364 354 516 488 302 S716 98 850 198' stroke='{AMBER}' stroke-width='8' stroke-linecap='round' stroke-dasharray='18 20' opacity='.55'/>"
                 f"<path d='M768 140 L868 196 L746 226 L768 140Z' fill='{AMBER}' opacity='.85'/>"
                 f"</svg>")
        head = (f"<div style='position:absolute;left:56px;top:268px;width:560px;'>"
                f"<div style=\"font-family:Inter;font-weight:950;font-size:76px;line-height:.9;letter-spacing:-3px;color:#fff;\">Craft a</div>"
                f"<div style=\"display:inline-block;margin-top:10px;font-family:IWSerif,Georgia,serif;font-style:italic;font-weight:700;font-size:112px;line-height:.86;color:{AMBER};background:linear-gradient(transparent 58%,{CORAL} 58%);padding:0 12px;transform:rotate(-2deg);\">Follow-Up</div>"
                f"<div style=\"margin-top:14px;font-family:Inter;font-weight:950;font-size:82px;line-height:.9;letter-spacing:-3px;color:#fff;\">Email</div></div>")
        label = (f"<div style='position:absolute;left:58px;top:190px;height:42px;padding:0 18px;border-radius:21px;background:rgba(255,255,255,.10);border:2px solid rgba(255,255,255,.18);display:flex;align-items:center;'>"
                 f"<span style=\"font-family:'DM Sans';font-weight:950;font-size:16px;color:{AMBER};letter-spacing:4px;\">SEND WITH INTENT</span></div>")
        steps = (f"<div style='position:absolute;left:60px;top:710px;display:flex;gap:14px;'>"
                 f"<div style='height:50px;padding:0 18px;border-radius:25px;background:#fff;display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:20px;color:#0B201F;'>timing</div>"
                 f"<div style='height:50px;padding:0 18px;border-radius:25px;background:{AMBER};display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:20px;color:#0B201F;'>clarity</div>"
                 f"<div style='height:50px;padding:0 18px;border-radius:25px;background:{GREEN};display:flex;align-items:center;font-family:Inter;font-weight:950;font-size:20px;color:#0B201F;'>interest</div></div>")
        nuno = f"<img src='{L.nuno_src(pose)}' style='position:absolute;right:-34px;bottom:8px;height:650px;filter:drop-shadow(0 22px 34px rgba(0,0,0,.58));'>"
        swipe = (f"<div style=\"position:absolute;left:58px;bottom:58px;font-family:'DM Sans';font-weight:900;font-size:24px;color:{AMBER};\">Open the email system &rarr;</div>")
        return bg + trail + composer + _logo(left=56, top=44) + label + head + steps + nuno + swipe
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
    block = (f"<div style='position:absolute;left:{x}px;top:342px;width:560px;'>"
             + L.hero(copy['headline'], "quoted", p['ink'], p['accent'], hi=p['accent'], size=75, width=560)
             + f"{contents}</div>")
    swipe = (f"<div style=\"position:absolute;left:{x}px;bottom:56px;font-family:'DM Sans';font-weight:800;font-size:22px;"
             f"color:{p['accent']};\">Open chapter one &rarr;</div>")
    if "tracker" in copy.get("headline", "").lower():
        nuno = (f"<div style='position:absolute;right:120px;bottom:32px;width:760px;height:760px;border-radius:50%;"
                f"background:radial-gradient(circle at 55% 52%,rgba(255,177,32,.16),transparent 64%);'></div>"
                f"<img src='{L.nuno_src(pose)}' style='position:absolute;right:-70px;bottom:0;height:570px;"
                f"filter:drop-shadow(0 22px 34px rgba(0,0,0,.45));'>")
    elif pose in {"nuno_followup_phone"}:
        nuno = _nuno_whole(pose, h=760, right=18)
    else:
        nuno = _nuno_whole(pose, h=760, right=-60)
    return (_bg(p) + _folder_tabs(p, 1, total) + _arc(p) + nuno
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
    if "tracker" in copy.get("headline", "").lower():
        pose = "nuno_tablet"
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:300px;font-family:'DM Sans';font-weight:800;font-size:21px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;top:346px;width:450px;font-family:Inter;font-weight:800;"
            f"font-size:56px;line-height:1.04;letter-spacing:-1.7px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:{x}px;top:566px;width:420px;font-family:'DM Sans';font-weight:500;"
           f"font-size:33px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + _folder_tabs(p, total, total) + _arc(p) + _nuno_whole(pose, h=720, right=-60)
            + _logo(left=x, top=44) + eyebrow + head + sub
            + f"<div style='position:absolute;left:{x}px;top:706px;'>{_pill(p)}</div>")



# =================================================================================
#  WORLD 10  -  "ledger"  (rust on cream) : ruled accounting ledger
# =================================================================================
def _rules(p, top=150, n=16, gap=52):
    rows = "".join(f"<div style='position:absolute;left:0;right:0;top:{top + i*gap}px;height:1px;"
                   f"background:rgba(42,32,22,.11);'></div>" for i in range(n))
    return (rows + f"<div style='position:absolute;left:196px;top:0;bottom:0;width:2px;background:{p['accent']};opacity:.55;'></div>"
                   f"<div style='position:absolute;left:206px;top:0;bottom:0;width:2px;background:{p['accent']};opacity:.25;'></div>")

def _ledger_no(p, n, total, top=168):
    return (f"<div style='position:absolute;left:56px;top:{top}px;'>"
            f"<div style=\"font-family:IWSerif,Georgia,serif;font-size:104px;line-height:.82;color:{p['accent']};\">{n:02d}</div>"
            f"<div style=\"margin-top:6px;font-family:'DM Sans';font-weight:800;font-size:17px;color:{p['mut']};"
            f"letter-spacing:3px;\">OF {total:02d}</div></div>")

def cover_ledger(p, copy, total, pose):
    x = 244
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:900;font-size:20px;"
               f"color:{p['accent']};letter-spacing:5px;\">{copy.get('eyebrow','INTERNWISE')[:24].upper()}</div>")
    head = (f"<div style='position:absolute;left:{x}px;top:296px;'>"
            + L.hero(copy['headline'], "stack", p['ink'], p['accent'], hi=p['accent'], size=75, width=430) + "</div>")
    entries = ""
    for i, sl in enumerate([sl for sl in copy.get("slides", []) if sl.get("tag")][:3], start=1):
        entries += (f"<div style='display:flex;align-items:center;gap:14px;margin-bottom:13px;'>"
                    f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:17px;color:{p['accent']};letter-spacing:2px;\">{i:02d}</span>"
                    f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;color:{p['mut']};\">{sl['tag']}</span></div>")
    index = (f"<div style='position:absolute;left:{x}px;bottom:150px;width:420px;'>"
             f"<div style=\"font-family:'DM Sans';font-weight:900;font-size:15px;color:{p['mut']};letter-spacing:4px;"
             f"margin-bottom:14px;\">ENTRIES</div>{entries}</div>" if entries else "")
    swipe = (f"<div style=\"position:absolute;left:{x}px;bottom:58px;font-family:'DM Sans';font-weight:900;font-size:22px;"
             f"color:{p['accent']};\">Open the ledger &rarr;</div>")
    return (_bg(p) + _rules(p) + _nuno_whole(pose, h=760, right=-70) + _logo(L.DARKLOGO, left=56, top=48)
            + _ledger_no(p, 1, total, top=660) + eyebrow + head + index + swipe)

def content_ledger(p, n, total, slide):
    x = 244
    tag = (f"<div style=\"position:absolute;left:{x}px;top:200px;font-family:'DM Sans';font-weight:900;font-size:21px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:26].upper()}</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;right:72px;top:262px;font-family:Inter;font-weight:800;"
            f"font-size:56px;line-height:1.06;letter-spacing:-1.6px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:{x}px;right:80px;top:466px;font-family:'DM Sans';font-weight:500;"
            f"font-size:40px;line-height:1.44;color:{p['mut']};\">{slide['body']}</div>")
    # The lower half of a ruled page reads as unfinished without an anchor.
    ghost = (f"<div style=\"position:absolute;right:62px;bottom:94px;font-family:IWSerif,Georgia,serif;"
             f"font-size:330px;line-height:.72;color:{p['accent']};opacity:.09;\">{n-1:02d}</div>")
    return (_bg(p) + _rules(p) + ghost + _logo(L.DARKLOGO, left=56, top=48) + _ledger_no(p, n, total)
            + tag + head + body
            + f"<div style=\"position:absolute;left:{x}px;bottom:58px;font-family:'DM Sans';font-weight:900;"
              f"font-size:21px;color:{p['accent']};\">Swipe &rarr;</div>")

def cta_ledger(p, copy, total, pose):
    x = 244
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:900;font-size:20px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;top:300px;width:420px;font-family:Inter;font-weight:800;"
            f"font-size:56px;line-height:1.04;letter-spacing:-1.7px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:{x}px;top:536px;width:400px;font-family:'DM Sans';font-weight:500;"
           f"font-size:32px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    pill = (f"<div style='position:absolute;left:{x}px;top:700px;height:58px;padding:0 26px;border-radius:12px;"
            f"background:{p['accent']};display:flex;align-items:center;'>"
            f"<span style=\"font-family:Inter;font-weight:900;font-size:24px;color:#fff;\">{L.URL}</span></div>")
    return (_bg(p) + _rules(p) + _nuno_whole(pose, h=720, right=-70) + _logo(L.DARKLOGO, left=56, top=48)
            + _ledger_no(p, total, total, top=660) + eyebrow + head + sub + pill)


# =================================================================================
#  WORLD 11  -  "grid"  (indigo) : modular blueprint, crosshair + coordinates
# =================================================================================
def _coords(p, n, total):
    return (f"<div style=\"position:absolute;right:58px;top:62px;font-family:'DM Sans';font-weight:800;font-size:19px;"
            f"color:{p['mut']};letter-spacing:4px;\">X{n:02d} &middot; Y{total:02d}</div>")

def _crosshair(p, cx, cy, r=260):
    return (f"<div style='position:absolute;left:{cx-r}px;top:{cy-r}px;width:{r*2}px;height:{r*2}px;border-radius:50%;"
            f"border:2px solid {p['accent']};opacity:.34;'></div>"
            f"<div style='position:absolute;left:{cx-r}px;top:{cy}px;width:{r*2}px;height:2px;background:{p['accent']};opacity:.26;'></div>"
            f"<div style='position:absolute;left:{cx}px;top:{cy-r}px;width:2px;height:{r*2}px;background:{p['accent']};opacity:.26;'></div>")

def cover_grid(p, copy, total, pose):
    x = 58
    eyebrow = (f"<div style='position:absolute;left:{x}px;top:230px;height:44px;padding:0 18px;border:2px solid {p['accent']};"
               f"display:flex;align-items:center;'>"
               f"<span style=\"font-family:'DM Sans';font-weight:900;font-size:19px;color:{p['accent']};letter-spacing:4px;\">{copy.get('eyebrow','INTERNWISE')[:22].upper()}</span></div>")
    head = (f"<div style='position:absolute;left:{x}px;top:300px;'>"
            + L.hero(copy['headline'], "boxed", p['ink'], p['accent'], hi=p['accent'], size=78, deep=p['deep'], width=460) + "</div>")
    ticks = "".join(f"<div style='width:{44 if i==0 else 22}px;height:6px;background:{p['accent']};"
                    f"opacity:{1 if i==0 else .3};margin-right:9px;'></div>" for i in range(total))
    bar = f"<div style='position:absolute;left:{x}px;bottom:150px;display:flex;align-items:center;'>{ticks}</div>"
    swipe = (f"<div style=\"position:absolute;left:{x}px;bottom:58px;font-family:'DM Sans';font-weight:900;font-size:22px;"
             f"color:{p['accent']};\">Swipe through the build &rarr;</div>")
    return (_bg(p) + _crosshair(p, 820, 420) + _nuno_whole(pose, h=760, right=-56) + _logo(left=x, top=44)
            + _coords(p, 1, total) + eyebrow + head + bar + swipe)

def content_grid(p, n, total, slide):
    x = 58
    module = (f"<div style='position:absolute;left:{x}px;top:230px;right:58px;bottom:150px;"
              f"border:2px solid {p['accent']};opacity:.22;'></div>")
    num = (f"<div style='position:absolute;left:{x}px;top:230px;width:96px;height:96px;background:{p['accent']};"
           f"display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:900;font-size:46px;"
           f"color:{p['deep']};'>{n-1:02d}</div>")
    tag = (f"<div style=\"position:absolute;left:{x+124}px;top:258px;font-family:'DM Sans';font-weight:900;font-size:21px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>")
    head = (f"<div style=\"position:absolute;left:{x+28}px;right:90px;top:390px;font-family:Inter;font-weight:800;"
            f"font-size:56px;line-height:1.06;letter-spacing:-1.6px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:{x+28}px;right:96px;top:600px;font-family:'DM Sans';font-weight:500;"
            f"font-size:40px;line-height:1.44;color:{p['mut']};\">{slide['body']}</div>")
    return (_bg(p) + _crosshair(p, 876, 834, 196) + module + _logo(left=x, top=44)
            + _coords(p, n, total) + num + tag + head + body)

def cta_grid(p, copy, total, pose):
    x = 58
    eyebrow = (f"<div style=\"position:absolute;left:{x}px;top:250px;font-family:'DM Sans';font-weight:900;font-size:20px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:{x}px;top:300px;width:450px;font-family:Inter;font-weight:800;"
            f"font-size:56px;line-height:1.04;letter-spacing:-1.7px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:{x}px;top:534px;width:420px;font-family:'DM Sans';font-weight:500;"
           f"font-size:32px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + _crosshair(p, 830, 560, 230) + _nuno_whole(pose, h=720, right=-56) + _logo(left=x, top=44)
            + _coords(p, total, total) + eyebrow + head + sub
            + f"<div style='position:absolute;left:{x}px;top:700px;'>{_pill(p)}</div>")


# =================================================================================
#  WORLD 12  -  "strip"  (forest) : contact sheet, sprocket holes down both edges
# =================================================================================
def _sprockets(p):
    holes = "".join(f"<div style='width:26px;height:36px;border-radius:5px;background:{p['deep']};margin:16px 0;'></div>"
                    for _ in range(14))
    col = (f"<div style='position:absolute;top:-20px;bottom:-20px;width:62px;background:{p['accent']};"
           f"display:flex;flex-direction:column;align-items:center;justify-content:space-around;opacity:.92;'>{holes}</div>")
    return (col.replace("position:absolute;", "position:absolute;left:0;")
            + col.replace("position:absolute;", "position:absolute;right:0;"))

def cover_strip(p, copy, total, pose):
    x = 104
    frame = (f"<div style='position:absolute;left:{x}px;top:170px;right:104px;bottom:150px;"
             f"border:3px solid rgba(255,255,255,.16);'></div>")
    eyebrow = (f"<div style=\"position:absolute;left:{x+28}px;top:238px;font-family:'DM Sans';font-weight:900;font-size:19px;"
               f"color:{p['accent']};letter-spacing:5px;\">{copy.get('eyebrow','INTERNWISE')[:22].upper()}</div>")
    head = (f"<div style='position:absolute;left:{x+28}px;top:292px;'>"
            + L.hero(copy['headline'], "quoted", p['ink'], p['accent'], hi=p['accent'], size=73, width=420) + "</div>")
    frames = (f"<div style=\"position:absolute;left:{x+28}px;bottom:200px;font-family:'DM Sans';font-weight:900;"
              f"font-size:17px;color:{p['mut']};letter-spacing:4px;\">FRAME 01 / {total:02d}</div>")
    swipe = (f"<div style=\"position:absolute;left:{x+28}px;bottom:70px;font-family:'DM Sans';font-weight:900;font-size:22px;"
             f"color:{p['accent']};\">Roll the sequence &rarr;</div>")
    return (_bg(p) + _sprockets(p) + frame + _nuno_whole(pose, h=740, right=-20) + _logo(left=x + 28, top=48)
            + eyebrow + head + frames + swipe)

def content_strip(p, n, total, slide):
    x = 104
    frame = (f"<div style='position:absolute;left:{x}px;top:170px;right:104px;bottom:150px;"
             f"border:3px solid rgba(255,255,255,.16);'></div>")
    num = (f"<div style=\"position:absolute;left:{x+28}px;top:220px;font-family:IWSerif,Georgia,serif;font-size:112px;"
           f"line-height:.8;color:{p['accent']};opacity:.9;\">{n-1:02d}</div>")
    tag = (f"<div style=\"position:absolute;left:{x+28}px;top:360px;font-family:'DM Sans';font-weight:900;font-size:21px;"
           f"color:{p['accent']};letter-spacing:4px;\">{slide.get('tag','STEP '+str(n-1))[:24].upper()}</div>")
    head = (f"<div style=\"position:absolute;left:{x+28}px;right:150px;top:410px;font-family:Inter;font-weight:800;"
            f"font-size:54px;line-height:1.06;letter-spacing:-1.5px;color:{p['ink']};word-break:keep-all;\">{slide['title']}</div>")
    body = (f"<div style=\"position:absolute;left:{x+28}px;right:160px;top:614px;font-family:'DM Sans';font-weight:500;"
            f"font-size:39px;line-height:1.44;color:{p['mut']};\">{slide['body']}</div>")
    foot = (f"<div style=\"position:absolute;left:{x+28}px;bottom:200px;font-family:'DM Sans';font-weight:900;"
            f"font-size:17px;color:{p['mut']};letter-spacing:4px;\">FRAME {n:02d} / {total:02d}</div>")
    return _bg(p) + _sprockets(p) + frame + _logo(left=x + 28, top=48) + num + tag + head + body + foot

def cta_strip(p, copy, total, pose):
    x = 104
    frame = (f"<div style='position:absolute;left:{x}px;top:170px;right:104px;bottom:150px;"
             f"border:3px solid rgba(255,255,255,.16);'></div>")
    eyebrow = (f"<div style=\"position:absolute;left:{x+28}px;top:238px;font-family:'DM Sans';font-weight:900;font-size:19px;"
               f"color:{p['accent']};letter-spacing:5px;\">YOUR MOVE</div>")
    head = (f"<div style=\"position:absolute;left:{x+28}px;top:292px;width:400px;font-family:Inter;font-weight:800;"
            f"font-size:54px;line-height:1.04;letter-spacing:-1.6px;color:{p['ink']};word-break:keep-all;\">{copy['headline']}</div>")
    sub = (f"<div style=\"position:absolute;left:{x+28}px;top:520px;width:380px;font-family:'DM Sans';font-weight:500;"
           f"font-size:31px;line-height:1.34;color:{p['mut']};\">{copy.get('cta','')}</div>")
    return (_bg(p) + _sprockets(p) + frame + _nuno_whole(pose, h=700, right=-20) + _logo(left=x + 28, top=48)
            + eyebrow + head + sub + f"<div style='position:absolute;left:{x+28}px;top:690px;'>{_pill(p)}</div>")


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
    "ledger": {"cover": cover_ledger, "content": content_ledger, "cta": cta_ledger},
    "grid": {"cover": cover_grid, "content": content_grid, "cta": cta_grid},
    "strip": {"cover": cover_strip, "content": content_strip, "cta": cta_strip},
}
def w_badge(copy, week_id='adhoc'):
    """First-day 'HELLO my name is' lanyard badge on a violet ground - for intro,
    first-week and networking topics, where the badge IS the metaphor. The badge
    carries the formula in handwriting; the steps sit on a ruled script card."""
    VIO, VIO2 = "#5B3FD0", "#33228A"
    RED = "#E5483F"; PAPER = "#FFF8EC"; NAVYT = "#152743"
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(90% 80% at 80% 10%,{VIO},{VIO2});'></div>"
          + L.dots("left:470px;top:120px;", color="rgba(255,255,255,.18)", w=150, h=110))
    logo = L.logo_tl()
    eb = (f"<div style='position:absolute;left:56px;top:196px;display:inline-flex;align-items:center;height:46px;padding:0 22px;"
          f"border-radius:23px;background:{AMBER};'><span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;"
          f"color:{DEEP};letter-spacing:3px;\">{copy.get('eyebrow','FIRST DAY')[:20].upper()}</span></div>")
    head = (f"<div style='position:absolute;left:56px;top:266px;width:500px;'>"
            + L.hero(copy['headline'], "scalejump", "#FFFFFF", AMBER, hi=AMBER, size=60, width=500) + "</div>")
    # Lanyard: two straps meeting at a clip, then the badge hanging slightly askew.
    straps = (f"<svg style='position:absolute;left:0;top:0;' width='1080' height='260' viewBox='0 0 1080 260'>"
              f"<path d='M742 -10 L800 168' stroke='{AMBER}' stroke-width='22' stroke-linecap='round'/>"
              f"<path d='M880 -10 L824 168' stroke='#E09A12' stroke-width='22' stroke-linecap='round'/></svg>")
    clip = ("<div style='position:absolute;left:792px;top:160px;width:40px;height:44px;border-radius:8px;"
            "background:linear-gradient(#D9DEE7,#A9B3C2);border:3px solid #0A1830;'></div>")
    write = copy.get("badge") or "Name, role, one interest, one question"
    badge = (f"<div style='position:absolute;left:612px;top:196px;width:400px;transform:rotate(4deg);"
             f"background:{PAPER};border:4px solid #0A1830;border-radius:26px;box-shadow:10px 12px 0 rgba(10,24,48,.55);overflow:hidden;'>"
             f"<div style='height:16px;'></div>"
             f"<div style='margin:0 18px;border-radius:14px;background:{RED};padding:16px 0 14px;text-align:center;'>"
             f"<div style=\"font-family:Inter;font-weight:900;font-size:66px;line-height:.95;color:#fff;letter-spacing:-1px;\">HELLO</div>"
             f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:24px;color:#fff;letter-spacing:1px;\">my name is</div></div>"
             f"<div style=\"padding:22px 30px 30px;font-family:IWSerif,Georgia,serif;font-style:italic;font-size:38px;line-height:1.18;"
             f"color:{NAVYT};text-align:center;\">{write}</div></div>")
    pts = copy.get("points", [])[:6]
    cells = ""
    for i, pt in enumerate(pts, 1):
        span = "grid-column:1/-1;" if i == len(pts) and len(pts) % 2 else ""   # no orphan gap on odd counts
        cells += (f"<div style='display:flex;gap:16px;align-items:center;{span}'>"
                  f"<div style='flex:0 0 48px;width:48px;height:48px;border-radius:50%;background:{VIO};display:flex;align-items:center;"
                  f"justify-content:center;font-family:Inter;font-weight:800;font-size:24px;color:#fff;'>{i}</div>"
                  f"<span style=\"font-family:Inter;font-weight:700;font-size:30px;line-height:1.14;color:{NAVYT};letter-spacing:-.3px;\">{pt}</span></div>")
    script = (f"<div style='position:absolute;left:44px;right:44px;top:636px;height:318px;box-sizing:border-box;padding:34px 36px;"
              f"background:{PAPER};border:4px solid #0A1830;border-radius:26px;box-shadow:10px 10px 0 rgba(10,24,48,.55);"
              f"display:grid;grid-template-columns:1fr 1fr;column-gap:34px;row-gap:26px;align-content:center;'>{cells}</div>")
    foot = (f"<div style='position:absolute;left:56px;right:56px;bottom:30px;display:flex;align-items:center;justify-content:space-between;gap:24px;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:27px;color:#fff;letter-spacing:-.2px;\">{copy.get('cta','')}</span>"
            f"<span style=\"flex:none;font-family:'DM Sans';font-weight:800;font-size:22px;color:{AMBER};letter-spacing:.6px;\">{L.URL}</span></div>")
    return bg + logo + eb + head + straps + clip + badge + script + foot



# ------------------------------------------------- object-metaphor singles
# The badge set the pattern: one illustrated object that IS the topic, carrying
# the formula in its own voice, over a ruled card of steps and a one-line close.
# These siblings reuse that skeleton with a different object, ground and hero move
# so a week of them never reads as one template.
OBJ_PAPER, NAVYT, EDGE = "#FFF8EC", "#152743", "#0A1830"


def _step_cells(pts, num_bg, ink=NAVYT, size=30):
    cells = ""
    for i, pt in enumerate(pts, 1):
        span = "grid-column:1/-1;" if i == len(pts) and len(pts) % 2 else ""   # no orphan gap on odd counts
        cells += (f"<div style='display:flex;gap:16px;align-items:center;{span}'>"
                  f"<div style='flex:0 0 48px;width:48px;height:48px;border-radius:50%;background:{num_bg};display:flex;align-items:center;"
                  f"justify-content:center;font-family:Inter;font-weight:800;font-size:24px;color:#fff;'>{i}</div>"
                  f"<span style=\"font-family:Inter;font-weight:700;font-size:{size}px;line-height:1.14;color:{ink};letter-spacing:-.3px;\">{pt}</span></div>")
    return cells


def _paper_card(inner, top=636, height=318, grid=True):
    layout = ("display:grid;grid-template-columns:1fr 1fr;column-gap:34px;row-gap:26px;align-content:center;"
              if grid else "display:flex;gap:40px;")
    return (f"<div style='position:absolute;left:44px;right:44px;top:{top}px;height:{height}px;box-sizing:border-box;padding:34px 36px;"
            f"background:{OBJ_PAPER};border:4px solid {EDGE};border-radius:26px;box-shadow:10px 10px 0 rgba(10,24,48,.55);{layout}'>{inner}</div>")


def _obj_foot(cta, ink="#fff", url_ink=AMBER):
    return (f"<div style='position:absolute;left:56px;right:56px;bottom:30px;display:flex;align-items:center;justify-content:space-between;gap:24px;'>"
            f"<span style=\"font-family:Inter;font-weight:800;font-size:27px;color:{ink};letter-spacing:-.2px;\">{cta}</span>"
            f"<span style=\"flex:none;font-family:'DM Sans';font-weight:800;font-size:22px;color:{url_ink};letter-spacing:.6px;\">{L.URL}</span></div>")


def _obj_pill(text, left, top, bg=AMBER, ink=DEEP):
    return (f"<div style='position:absolute;left:{left}px;top:{top}px;display:inline-flex;align-items:center;height:46px;padding:0 22px;"
            f"border-radius:23px;background:{bg};'><span style=\"font-family:'DM Sans';font-weight:800;font-size:20px;"
            f"color:{ink};letter-spacing:3px;\">{text[:22].upper()}</span></div>")


def w_swingtag(copy, week_id='adhoc'):
    """Clothes hanger with a kraft swing tag, on emerald - for dress-code and
    'how to present yourself' topics. The tag reads like a garment label
    (STYLE / FIT / CARE), so the advice arrives as the outfit's own spec."""
    EM, EM2, KRAFT, BROWN = "#17876A", "#0B4A3C", "#EBD3A2", "#7A5A2E"
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(95% 85% at 82% 8%,{EM},{EM2});'></div>"
          + L.dots("left:470px;top:110px;", color="rgba(255,255,255,.16)", w=130, h=110))
    head = (f"<div style='position:absolute;left:56px;top:266px;width:520px;'>"
            + L.hero(copy['headline'], "serif_italic", "#FFFFFF", AMBER, hi=AMBER, size=60, width=520) + "</div>")
    hanger = ("<svg style='position:absolute;left:0;top:0;' width='1080' height='300' viewBox='0 0 1080 300'>"
              "<path d='M826 104 L826 80 C826 50 864 44 866 70 C867 84 856 90 848 92' stroke='#DCE3EA' stroke-width='9' fill='none' stroke-linecap='round'/>"
              "<path d='M826 104 L664 190 Q648 202 670 202 L982 202 Q1004 202 988 190 Z' stroke='#DCE3EA' stroke-width='11' fill='none' stroke-linejoin='round'/>"
              "<path d='M826 202 C820 226 822 246 826 268' stroke='#F4ECDD' stroke-width='4' fill='none'/></svg>")
    rows = ""
    for lab, val in (copy.get("tag") or [["STYLE", "Smart-casual"], ["FIT", "One step smarter"]])[:3]:
        rows += (f"<div style='border-top:2px dashed rgba(122,90,46,.45);padding:8px 0 6px;'>"
                 f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:17px;letter-spacing:4px;color:{BROWN};\">{lab.upper()}</div>"
                 f"<div style=\"font-family:IWSerif,Georgia,serif;font-style:italic;font-size:33px;line-height:1.1;color:{NAVYT};\">{val}</div></div>")
    bars = "".join(f"<div style='width:{w}px;height:34px;background:{NAVYT};'></div>"
                   for w in (4, 2, 6, 3, 2, 5, 2, 7, 3, 2, 4, 6, 2, 3, 5, 2, 4))
    tag = (f"<div style='position:absolute;left:660px;top:244px;width:330px;transform:rotate(-5deg);transform-origin:50% 28px;"
           f"background:{KRAFT};border:4px solid {EDGE};box-shadow:10px 12px 0 rgba(4,30,24,.5);"
           f"clip-path:polygon(18% 0,82% 0,100% 12%,100% 100%,0 100%,0 12%);padding:52px 28px 18px;box-sizing:border-box;'>"
           f"<div style='position:absolute;left:50%;top:16px;width:22px;height:22px;margin-left:-11px;border-radius:50%;background:{EM2};border:3px solid {EDGE};'></div>"
           f"<div style=\"font-family:Inter;font-weight:900;font-size:22px;letter-spacing:3px;color:{NAVYT};text-align:center;margin-bottom:8px;\">{copy.get('tag_title','INTERVIEW FIT')}</div>"
           f"{rows}<div style='display:flex;gap:4px;justify-content:center;margin-top:10px;'>{bars}</div></div>")
    card = _paper_card(_step_cells(copy.get("points", [])[:6], EM))
    return bg + L.logo_tl() + _obj_pill(copy.get('eyebrow', 'DRESS CODE'), 56, 196) + head + hanger + tag + card + _obj_foot(copy.get('cta', ''))


def w_metro(copy, week_id='adhoc'):
    """A route map on a cream ground - for 'where to look / which channels'
    topics. Each channel is a station on one line; a single ticket from
    'applying everywhere' to 'your internship' carries the promise."""
    CREAM, LINE, MUTED = "#F4EFE6", "#E5483F", "#5B6B82"
    bg = (f"<div style='position:absolute;inset:0;background:{CREAM};"
          f"background-image:linear-gradient(rgba(21,39,67,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(21,39,67,.05) 2px,transparent 2px);"
          f"background-size:54px 54px;'></div>")
    logo = f"<div style='position:absolute;left:56px;top:44px;'><img src='{L.DARKLOGO}' style='height:{L.LOGO}px;'></div>"
    head = (f"<div style='position:absolute;left:56px;top:266px;width:560px;'>"
            + L.hero(copy['headline'], "highlight", NAVYT, NAVYT, hi=AMBER, size=60, width=560) + "</div>")
    frm, to = copy.get("ticket") or ["Applying everywhere", "Your internship"]
    notch = "radial-gradient(circle at 0 50%,transparent 18px,#000 19px) left/51% 100% no-repeat,radial-gradient(circle at 100% 50%,transparent 18px,#000 19px) right/51% 100% no-repeat"
    ticket = (f"<div style='position:absolute;left:660px;top:170px;width:360px;transform:rotate(6deg);filter:drop-shadow(10px 12px 0 rgba(10,24,48,.35));'>"
              f"<div style='background:{AMBER};-webkit-mask:{notch};mask:{notch};padding:24px 34px 26px;'>"
              f"<div style=\"display:flex;justify-content:space-between;font-family:'DM Sans';font-weight:800;font-size:17px;letter-spacing:4px;color:{NAVYT};\">"
              f"<span>SINGLE</span><span>ADULT</span></div>"
              f"<div style='border-top:3px dashed rgba(21,39,67,.35);margin:14px 0 12px;'></div>"
              f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:16px;letter-spacing:3px;color:rgba(21,39,67,.65);\">FROM</div>"
              f"<div style=\"font-family:IWSerif,Georgia,serif;font-style:italic;font-size:31px;line-height:1.1;color:{NAVYT};margin-bottom:10px;\">{frm}</div>"
              f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:16px;letter-spacing:3px;color:rgba(21,39,67,.65);\">TO</div>"
              f"<div style=\"font-family:Inter;font-weight:900;font-size:34px;line-height:1.05;color:{NAVYT};\">{to}</div></div></div>")
    stops = (copy.get("stops") or [])[:5]
    n = max(len(stops), 2)
    x0, x1, ly = 70, 922, 168                      # line ends and height inside the map card
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    svg = (f"<svg style='position:absolute;left:0;top:0;' width='992' height='340'>"
           f"<line x1='{x0-30}' y1='{ly}' x2='{x1+30}' y2='{ly}' stroke='{LINE}' stroke-width='18' stroke-linecap='round'/></svg>")
    nodes = labels = ""
    for i, ((name, note), x) in enumerate(zip(stops, xs)):
        last = i == len(stops) - 1
        d = 58 if last else 46
        nodes += (f"<div style='position:absolute;left:{x-d/2}px;top:{ly-d/2}px;width:{d}px;height:{d}px;border-radius:50%;box-sizing:border-box;"
                  f"background:{'#fff' if not last else NAVYT};border:7px solid {NAVYT};display:flex;align-items:center;justify-content:center;"
                  f"font-family:Inter;font-weight:900;font-size:{20 if not last else 22}px;color:{NAVYT if not last else '#fff'};'>{i+1}</div>")
        above = i % 2 == 0
        w = 300
        left = x - 26 if i == 0 else (x - w + 26 if last else x - w / 2)
        align = "left" if i == 0 else ("right" if last else "center")
        pos = f"bottom:{340-ly+44}px;" if above else f"top:{ly+44}px;"
        labels += (f"<div style='position:absolute;left:{left}px;width:{w}px;{pos}text-align:{align};'>"
                   f"<div style=\"font-family:Inter;font-weight:900;font-size:27px;line-height:1.05;color:{NAVYT};letter-spacing:-.4px;\">{name}</div>"
                   f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:21px;line-height:1.2;color:{MUTED};margin-top:5px;\">{note}</div></div>")
    route = (f"<div style='position:absolute;left:44px;top:600px;width:992px;height:340px;box-sizing:border-box;background:#fff;"
             f"border:4px solid {EDGE};border-radius:26px;box-shadow:10px 10px 0 rgba(10,24,48,.35);overflow:hidden;'>"
             f"{svg}{nodes}{labels}</div>")
    return (bg + logo + _obj_pill(copy.get('eyebrow', 'WHERE TO LOOK'), 56, 196, bg=NAVYT, ink="#fff") + head + ticket + route
            + _obj_foot(copy.get('cta', ''), ink=NAVYT, url_ink=LINE))


def w_scales(copy, week_id='adhoc'):
    """A level balance scale on deep blue - for two-sided answers (strengths and
    weaknesses, pros and cons). Each pan holds one side's rule; the card below
    splits the steps into the same two columns."""
    BL, BL2, BRASS = "#1D6FB8", "#0B2F5A", "#FFC34D"
    left_lab, right_lab = copy.get("sides") or ["Strengths", "Weaknesses"]
    left_pan, right_pan = copy.get("pans") or ["+ proof", "+ a fix"]
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(95% 85% at 80% 12%,{BL},{BL2});'></div>"
          + L.dots("left:440px;top:120px;", color="rgba(255,255,255,.16)", w=130, h=110))
    head = (f"<div style='position:absolute;left:56px;top:266px;width:540px;'>"
            + L.hero(copy['headline'], "underline", "#FFFFFF", "#FFFFFF", hi=AMBER, size=56, width=540) + "</div>")
    cx, by, lc, rc, py = 790, 196, 626, 954, 470     # post x, beam y, pan centres, pan y
    scale = (f"<svg style='position:absolute;left:0;top:0;' width='1080' height='640' viewBox='0 0 1080 640'>"
             f"<g stroke='{EDGE}' stroke-width='4' stroke-linejoin='round'>"
             f"<path d='M{cx-90} 600 Q{cx} 556 {cx+90} 600 Z' fill='{BRASS}'/>"
             f"<rect x='{cx-11}' y='{by}' width='22' height='{590-by}' fill='{BRASS}'/>"
             f"<rect x='{lc}' y='{by-10}' width='{rc-lc}' height='20' rx='10' fill='{BRASS}'/>"
             f"<circle cx='{cx}' cy='{by}' r='22' fill='{BRASS}'/><circle cx='{cx}' cy='{by-40}' r='14' fill='{BRASS}'/></g>"
             f"<g stroke='#F4ECDD' stroke-width='3'>"
             f"<line x1='{lc}' y1='{by}' x2='{lc-84}' y2='{py}'/><line x1='{lc}' y1='{by}' x2='{lc+84}' y2='{py}'/>"
             f"<line x1='{rc}' y1='{by}' x2='{rc-84}' y2='{py}'/><line x1='{rc}' y1='{by}' x2='{rc+84}' y2='{py}'/></g>"
             f"<g stroke='{EDGE}' stroke-width='4' fill='{BRASS}'>"
             f"<path d='M{lc-96} {py} Q{lc} {py+62} {lc+96} {py} Z'/><path d='M{rc-96} {py} Q{rc} {py+62} {rc+96} {py} Z'/></g></svg>")
    def pan_card(x, lab, val, col, rot):
        return (f"<div style='position:absolute;left:{x-82}px;top:{py-128}px;width:164px;height:124px;box-sizing:border-box;padding:14px 10px;"
                f"background:{col};border:4px solid {EDGE};border-radius:16px;transform:rotate({rot}deg);text-align:center;"
                f"box-shadow:6px 6px 0 rgba(10,24,48,.4);'>"
                f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:{15 if len(lab) <= 10 else 12}px;letter-spacing:{2.5 if len(lab) <= 10 else 1.2}px;color:{NAVYT};\">{lab.upper()}</div>"
                f"<div style=\"font-family:IWSerif,Georgia,serif;font-style:italic;font-size:34px;line-height:1.05;color:{NAVYT};margin-top:8px;\">{val}</div></div>")
    pans = pan_card(lc, left_lab, left_pan, GREEN, -3) + pan_card(rc, right_lab, right_pan, CORAL, 3)
    def col(lab, dot, items):
        li = "".join(f"<div style='display:flex;gap:14px;align-items:flex-start;margin-top:16px;'>"
                     f"<div style='flex:0 0 14px;height:14px;margin-top:11px;border-radius:50%;background:{dot};border:3px solid {EDGE};'></div>"
                     f"<span style=\"font-family:Inter;font-weight:700;font-size:28px;line-height:1.15;color:{NAVYT};letter-spacing:-.3px;\">{t}</span></div>"
                     for t in items)
        return (f"<div style='flex:1;'><div style=\"font-family:'DM Sans';font-weight:800;font-size:19px;letter-spacing:4px;color:{NAVYT};\">"
                f"{lab.upper()}</div>{li}</div>")
    card = _paper_card(col(left_lab, GREEN, copy.get("left", [])[:3])
                       + f"<div style='width:3px;background:rgba(21,39,67,.15);'></div>"
                       + col(right_lab, CORAL, copy.get("right", [])[:3]), grid=False)
    return bg + L.logo_tl() + _obj_pill(copy.get('eyebrow', 'INTERVIEW'), 56, 196) + head + scale + pans + card + _obj_foot(copy.get('cta', ''))



def w_planner(copy, week_id='adhoc'):
    """A spiral desk-diary page on warm orange - for 'what a day/week actually
    looks like' topics. The timetable IS the content; a sticky note carries the
    myth the post is busting."""
    OR, OR2, SUN = "#F28C3B", "#B84A1E", "#FFE27A"
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(95% 85% at 82% 8%,{OR},{OR2});'></div>"
          + L.dots("left:470px;top:110px;", color="rgba(255,255,255,.2)", w=130, h=110))
    head = (f"<div style='position:absolute;left:56px;top:266px;width:560px;'>"
            + L.hero(copy['headline'], "highlight", "#FFFFFF", NAVYT, hi=SUN, size=60, width=560) + "</div>")
    sticky = (f"<div style='position:absolute;left:690px;top:150px;width:320px;height:300px;box-sizing:border-box;padding:56px 30px 26px;"
              f"background:{SUN};transform:rotate(5deg);box-shadow:10px 12px 0 rgba(70,20,5,.35);border:4px solid {EDGE};'>"
              f"<div style='position:absolute;left:50%;top:-16px;width:120px;height:34px;margin-left:-60px;background:rgba(255,255,255,.55);transform:rotate(-4deg);'></div>"
              f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:17px;letter-spacing:4px;color:{OR2};\">{copy.get('note_label','MYTH')}</div>"
              f"<div style=\"font-family:IWSerif,Georgia,serif;font-style:italic;font-size:38px;line-height:1.12;color:{NAVYT};margin-top:10px;\">{copy.get('note','')}</div></div>")
    rings = "".join(f"<div style='position:absolute;top:-22px;left:{x}px;width:20px;height:44px;border-radius:10px;background:#D9DEE7;border:4px solid {EDGE};'></div>"
                    for x in range(70, 960, 74))
    rows = ""
    for t, what in (copy.get("day") or [])[:5]:
        rows += (f"<div style='display:flex;align-items:center;gap:26px;height:58px;border-bottom:2px solid rgba(21,39,67,.10);'>"
                 f"<div style=\"flex:0 0 104px;font-family:'DM Sans';font-weight:800;font-size:26px;color:{OR2};\">{t}</div>"
                 f"<div style=\"font-family:Inter;font-weight:700;font-size:29px;color:{NAVYT};letter-spacing:-.3px;\">{what}</div></div>")
    page = (f"<div style='position:absolute;left:44px;top:560px;width:992px;height:396px;box-sizing:border-box;padding:40px 44px 0;"
            f"background:{OBJ_PAPER};border:4px solid {EDGE};border-radius:22px;box-shadow:10px 10px 0 rgba(70,20,5,.4);"
            f"background-image:linear-gradient(90deg,transparent 168px,rgba(229,72,63,.35) 168px,rgba(229,72,63,.35) 171px,transparent 171px);'>"
            f"{rings}<div style=\"display:flex;justify-content:space-between;font-family:'DM Sans';font-weight:800;font-size:18px;letter-spacing:4px;color:{NAVYT};margin-bottom:6px;position:relative;background:{OBJ_PAPER};padding-bottom:6px;\">"
            f"<span>{copy.get('page_title','A TYPICAL DAY')}</span><span style='color:{OR2};'>{copy.get('page_day','TUESDAY')}</span></div>{rows}</div>")
    return bg + L.logo_tl() + _obj_pill(copy.get('eyebrow', 'INTERN LIFE'), 56, 196, bg=NAVYT, ink="#fff") + head + sticky + page + _obj_foot(copy.get('cta', ''))


def w_player(copy, week_id='adhoc'):
    """A music player with a spinning record, on magenta - for 'build your
    answer' topics with a time limit. Each step is a track with its own running
    time, so the tracklist adds up to the answer's length."""
    MG, MG2, APP = "#D0397A", "#5E1240", "#1E0F2B"
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(95% 85% at 82% 8%,{MG},{MG2});'></div>"
          + L.dots("left:450px;top:110px;", color="rgba(255,255,255,.18)", w=130, h=110))
    head = (f"<div style='position:absolute;left:56px;top:266px;width:540px;'>"
            + L.hero(copy['headline'], "serif_italic", "#FFFFFF", AMBER, hi=AMBER, size=56, width=540) + "</div>")
    grooves = "".join(f"<circle cx='190' cy='190' r='{r}' fill='none' stroke='rgba(255,255,255,.08)' stroke-width='2'/>" for r in range(80, 186, 12))
    record = (f"<svg style='position:absolute;left:640px;top:120px;' width='380' height='380' viewBox='0 0 380 380'>"
              f"<circle cx='190' cy='190' r='186' fill='#0B0710' stroke='{EDGE}' stroke-width='4'/>{grooves}"
              f"<path d='M190 20 A170 170 0 0 1 330 100' stroke='rgba(255,255,255,.22)' stroke-width='10' fill='none' stroke-linecap='round'/>"
              f"<circle cx='190' cy='190' r='74' fill='{AMBER}' stroke='{EDGE}' stroke-width='4'/>"
              f"<circle cx='190' cy='190' r='8' fill='{EDGE}'/>"
              f"<text x='190' y='176' text-anchor='middle' font-family='DM Sans' font-weight='800' font-size='15' letter-spacing='3' fill='{NAVYT}'>{copy.get('label_top','YOUR')}</text>"
              f"<text x='190' y='218' text-anchor='middle' font-family='DM Sans' font-weight='800' font-size='15' letter-spacing='3' fill='{NAVYT}'>{copy.get('label_bottom','ANSWER')}</text></svg>")
    tracks = ""
    for i, (name, dur) in enumerate((copy.get("tracks") or [])[:5], 1):
        live = i == 1
        tracks += (f"<div style='display:flex;align-items:center;gap:22px;height:56px;border-top:1px solid rgba(255,255,255,.10);'>"
                   f"<div style=\"flex:0 0 30px;font-family:Inter;font-weight:800;font-size:24px;color:{AMBER if live else 'rgba(255,255,255,.5)'};\">{i}</div>"
                   f"<div style=\"flex:1;font-family:Inter;font-weight:700;font-size:29px;color:#fff;letter-spacing:-.3px;\">{name}</div>"
                   f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:22px;color:rgba(255,255,255,.6);\">{dur}</div></div>")
    play = (f"<svg width='150' height='44' viewBox='0 0 150 44'>"
            f"<path d='M14 10v24M38 10 20 22l18 12z' fill='#fff' stroke='#fff' stroke-width='3' stroke-linejoin='round'/>"
            f"<circle cx='75' cy='22' r='21' fill='{AMBER}'/><path d='M68 12v20l16-10z' fill='{APP}'/>"
            f"<path d='M136 10v24M112 10l18 12-18 12z' fill='#fff' stroke='#fff' stroke-width='3' stroke-linejoin='round'/></svg>")
    app = (f"<div style='position:absolute;left:44px;top:546px;width:992px;height:412px;box-sizing:border-box;padding:28px 40px 0;"
           f"background:{APP};border:4px solid {EDGE};border-radius:26px;box-shadow:10px 10px 0 rgba(20,4,14,.5);'>"
           f"<div style='display:flex;align-items:center;justify-content:space-between;'>"
           f"<div><div style=\"font-family:'DM Sans';font-weight:800;font-size:16px;letter-spacing:4px;color:{AMBER};\">NOW PLAYING</div>"
           f"<div style=\"font-family:Inter;font-weight:900;font-size:34px;color:#fff;letter-spacing:-.5px;margin-top:4px;\">{copy.get('track','')}</div></div>{play}</div>"
           f"<div style='display:flex;align-items:center;gap:16px;margin:16px 0 14px;'>"
           f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:19px;color:rgba(255,255,255,.6);\">0:00</span>"
           f"<div style='flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.18);position:relative;'>"
           f"<div style='position:absolute;left:0;top:0;bottom:0;width:22%;border-radius:4px;background:{AMBER};'></div>"
           f"<div style='position:absolute;left:22%;top:50%;width:20px;height:20px;margin:-10px 0 0 -10px;border-radius:50%;background:#fff;'></div></div>"
           f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:19px;color:rgba(255,255,255,.6);\">{copy.get('length','1:00')}</span></div>"
           f"{tracks}</div>")
    return bg + L.logo_tl() + _obj_pill(copy.get('eyebrow', 'INTERVIEW'), 56, 196) + head + record + app + _obj_foot(copy.get('cta', ''))


def w_rec(copy, week_id='adhoc'):
    """A laptop mid-recording on a dark studio ground - for recorded and video
    interview topics. The REC light, countdown and on-screen question set the
    scene; a hand-drawn arrow points at the camera, which is the main lesson."""
    INKB, RED = "#151A26", "#FF4D4D"
    bg = (f"<div style='position:absolute;inset:0;background:radial-gradient(70% 60% at 78% 24%,#33405C,{INKB} 70%);'></div>"
          + L.dots("left:450px;top:110px;", color="rgba(255,255,255,.14)", w=130, h=110))
    head = (f"<div style='position:absolute;left:56px;top:266px;width:520px;'>"
            + L.hero(copy['headline'], "underline", "#FFFFFF", "#FFFFFF", hi=RED, size=56, width=520) + "</div>")
    q = copy.get("screen_q", "Q2 of 5: Why this role?")
    laptop = (f"<div style='position:absolute;left:600px;top:150px;width:420px;height:290px;box-sizing:border-box;padding:26px 18px 18px;"
              f"background:#0A0D14;border:4px solid {EDGE};border-radius:22px;box-shadow:10px 12px 0 rgba(0,0,0,.45);'>"
              f"<div style='position:absolute;left:50%;top:9px;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:#7CF0B0;box-shadow:0 0 10px #7CF0B0;'></div>"
              f"<div style='position:relative;width:100%;height:100%;border-radius:10px;overflow:hidden;background:linear-gradient(160deg,#4B5D80,#26324A);'>"
              f"<svg style='position:absolute;left:50%;bottom:0;margin-left:-80px;' width='160' height='150' viewBox='0 0 160 150'>"
              f"<circle cx='80' cy='52' r='34' fill='#9FB0CC'/><path d='M14 150c0-44 30-66 66-66s66 22 66 66z' fill='#9FB0CC'/></svg>"
              f"<div style='position:absolute;left:12px;top:12px;display:flex;align-items:center;gap:8px;height:30px;padding:0 12px;border-radius:15px;background:rgba(0,0,0,.45);'>"
              f"<div style='width:12px;height:12px;border-radius:50%;background:{RED};'></div>"
              f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:15px;letter-spacing:2px;color:#fff;\">REC</span></div>"
              f"<div style=\"position:absolute;right:12px;top:10px;font-family:Inter;font-weight:900;font-size:28px;color:#fff;\">{copy.get('timer','0:58')}</div>"
              f"<div style=\"position:absolute;left:12px;right:12px;bottom:12px;padding:10px 14px;border-radius:10px;background:rgba(0,0,0,.55);"
              f"font-family:Inter;font-weight:800;font-size:20px;color:#fff;\">{q}</div></div></div>"
              f"<div style='position:absolute;left:560px;top:436px;width:500px;height:22px;border-radius:0 0 18px 18px;background:#C9D1DD;border:4px solid {EDGE};'></div>")
    arrow = (f"<svg style='position:absolute;left:0;top:0;' width='1080' height='200' viewBox='0 0 1080 200'>"
             f"<path d='M700 92 C740 54 770 52 800 150' stroke='{AMBER}' stroke-width='5' fill='none' stroke-linecap='round'/>"
             f"<path d='M786 136 L801 156 L812 133' stroke='{AMBER}' stroke-width='5' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>"
             f"<div style=\"position:absolute;left:404px;top:66px;width:280px;text-align:right;font-family:IWSerif,Georgia,serif;font-style:italic;"
             f"font-size:32px;line-height:1.05;color:{AMBER};transform:rotate(-4deg);\">{copy.get('arrow_note','Look here, not at you')}</div>")
    card = _paper_card(_step_cells(copy.get("points", [])[:6], RED), top=512, height=370)
    return bg + L.logo_tl() + _obj_pill(copy.get('eyebrow', 'VIDEO INTERVIEW'), 56, 196, bg=RED, ink="#fff") + head + laptop + arrow + card + _obj_foot(copy.get('cta', ''))


SINGLE = {"tipcard": w_tipcard, "statement": w_statement, "badge": w_badge,
          "swingtag": w_swingtag, "metro": w_metro, "scales": w_scales,
          "planner": w_planner, "player": w_player, "rec": w_rec,
          "bigidea": w_bigidea, "splitcard": w_splitcard,
          "memo": w_memo, "scorecard": w_scorecard,
          "message_lab": w_message_lab, "focus_studio": w_focus_studio,
          "answerbank": w_answerbank}

COVER_TONE = {"serious": ["serious", "thoughtful", "practical"],
              "practical": ["practical", "confident", "serious"],
              "upbeat": ["confident", "positive", "practical"]}
CTA_TONE = {"serious": ["confident"], "practical": ["confident", "positive"],
            "upbeat": ["positive", "confident"]}


def choose_poses(copy, world, week_id="adhoc"):
    """Pick (and record in the ledger) the cover + CTA cutouts for a carousel.

    Split out of render_education so a caller can keep the chosen poses. The
    ledger is append-on-pick, so re-rendering a built post would otherwise make
    its own original poses look "recently used" and silently hand it different
    ones - see rerender_week.py, which stores what it gets back here.
    """
    if world not in CAROUSEL:
        return {}
    tone = copy.get("tone", "practical")
    cover_pose = nuno_ledger.pick(cover_pool_for(copy, week_id), week_id,
                                  label=f"education/{world}/cover", tone=COVER_TONE.get(tone))
    cta_pose = nuno_ledger.pick(cta_pool_for(copy), week_id, label=f"education/{world}/cta",
                                tone=CTA_TONE.get(tone), exclude={cover_pose})
    return {"cover": cover_pose, "cta": cta_pose}


# ------------------------------------------------------------------ closing line
# Every outro already carries the address in its own chrome (the accent pill, or
# the footer on the singles), so a cta sentence that ALSO ended in "... at
# internwise.co.uk" printed it twice on one slide. This used to append the URL
# when it was missing - exactly the wrong direction. Strip it instead and let the
# chrome own the address; what remains is the conclusive line.
_URL_TAIL = re.compile(
    r"[\s,;:\u2013\u2014-]*\b(?:at|on|via|visit|head\s+to|go\s+to|start\s+at|find\s+(?:us|more|out\s+more)\s+at)?"
    r"\s*(?:www\.)?internwise\.co\.uk[\s.!\u2192]*$", re.I)
# What is left once the address goes, when the whole sentence WAS the address.
# "Discover more at internwise.co.uk" -> "Discover more", which says nothing about
# the lesson the reader just swiped through.
_STUBS = re.compile(r"^(?:discover|explore|learn|find|see|read|browse|start|begin)"
                    r"(?:\s+(?:out)?\s*more|\s+now|\s+today|\s+here)?$", re.I)
FALLBACK_CTA = "Put one of these to work on your next application."


def close_line(cta):
    """The outro's conclusive sentence: the cta with the web address removed.

    Two shapes turn up. Usually the address trails the sentence ("Strengthen your
    pitch at internwise.co.uk"), and lopping the tail keeps a usable line. When it
    sits mid-sentence instead ("Visit internwise.co.uk today") there is no line to
    keep, so drop whole sentences that mention it and fall back if none survive.
    """
    line = _URL_TAIL.sub("", (cta or "").strip()).strip(" ,;:-\u2013\u2014")
    if "internwise" in line.lower():
        kept = [p for p in re.split(r"(?<=[.!?])\s+", line) if "internwise" not in p.lower()]
        line = " ".join(kept).strip(" ,;:-\u2013\u2014")
    if not line or _STUBS.match(line) or "internwise" in line.lower():
        return FALLBACK_CTA
    return line if line.endswith((".", "!", "?")) else line + "."


def render_education(copy, world, out_dir, week_id="adhoc", poses=None):
    """Render a post. `poses` replays an earlier choose_poses() result instead of
    drawing new cutouts, which is what makes a re-render reproducible."""
    os.makedirs(out_dir, exist_ok=True)
    copy = {**copy}
    copy["cta"] = close_line(copy.get("cta"))
    if world in CAROUSEL:
        p = PAL[world]; w = CAROUSEL[world]
        slides = copy.get("slides", [])
        total = len(slides) + 2
        chosen = poses if poses else choose_poses(copy, world, week_id)
        cover_pose, cta_pose = chosen.get("cover"), chosen.get("cta")
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
