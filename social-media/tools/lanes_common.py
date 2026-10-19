"""Daily-5 engine - shared plumbing for the five content lanes.

Lanes: education, engagement/conversation, quote, news (fixed template),
employer (B2B). This module gives every lane the same brand vocabulary and a
single render harness, so each post stays bespoke while sharing the plumbing.

Nothing here dictates a *look* beyond the brand tokens - conversation/quote/employer
posts author their own design world per post; only the news card is templated.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wk11_base as b
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(BASE, "content")
OUTROOT = os.path.join(BASE, "campaigns", "outputs")

# --- brand (current Week 12 palette) ---
NAVY="#0E2141"; DEEP="#0A1830"; INK="#EAF2FB"; MUT="#93AAC9"
AMBER="#FFB120"; CORAL="#FF6B6B"; GREEN="#41D98A"
LOGO=100  # uniform weekly logo height (non-negotiable brand rule)
URL="internwise.co.uk"

F   = b.fonts()
WHT = "data:image/png;base64,"+b.LOGO_W
_dark = b._b64(os.path.join(BASE,"branding","PNG","Internwise.Com-Horizontal logo.png"))
DARKLOGO = "data:image/png;base64,"+_dark if _dark else WHT   # coloured logo for light bgs
ICONMARK = "data:image/svg+xml;base64,"+base64.b64encode(
    open(os.path.join(BASE,"assets","iw_icon_mark.svg"),"rb").read()).decode()

def img(path):
    return "data:image/png;base64,"+base64.b64encode(open(path,"rb").read()).decode()
def nuno_src(name):
    return img(os.path.join(BASE,"assets","nuno",name+".png"))

# --- icon set (shared with wk12) ---
_IC = {
 "user":"<circle cx='12' cy='8' r='4'/><path d='M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7'/>",
 "target":"<circle cx='12' cy='12' r='9'/><circle cx='12' cy='12' r='4.5'/><circle cx='12' cy='12' r='1.2' fill='currentColor' stroke='none'/>",
 "star":"<path d='M12 3.5l2.6 5.7 6.2.6-4.7 4.1 1.4 6.1L12 16.9 6.5 20.1l1.4-6.1L3.2 9.8l6.2-.6z'/>",
 "search":"<circle cx='11' cy='11' r='7'/><path d='M20 20l-4.5-4.5'/>",
 "doc":"<rect x='5' y='3' width='14' height='18' rx='2'/><path d='M8.5 8h7M8.5 12h7M8.5 16h4'/>",
 "rocket":"<path d='M12 3c3.4 2 5.4 5.4 5.4 9.4L12 16l-5.4-3.6C6.6 8.4 8.6 5 12 3z'/><circle cx='12' cy='10' r='1.7'/><path d='M9 16c-1.6 1-2.2 3-2.2 5 2 0 4-.6 5-2.2'/>",
 "check":"<path d='M4 12.5l5 5 11-11'/>",
 "x":"<path d='M6 6l12 12M18 6L6 18'/>",
 "clock":"<circle cx='12' cy='12' r='9'/><path d='M12 7.5v5l3.5 2.5'/>",
 "eye":"<path d='M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z'/><circle cx='12' cy='12' r='3'/>",
 "chat":"<path d='M4 5h16v10H10l-4 4v-4H4z'/>",
 "calendar":"<rect x='4' y='5' width='16' height='16' rx='2'/><path d='M4 10h16M8 3v4M16 3v4'/>",
 "arrowup":"<path d='M12 19V6M6 12l6-6 6 6'/>",
 "trend":"<path d='M3 17l6-6 4 4 8-8'/><path d='M15 7h6v6'/>",
 "refresh":"<path d='M20 11a8 8 0 1 0-.6 4'/><path d='M20 5v6h-6'/>",
 "bulb":"<path d='M9 18h6M10 21h4'/><path d='M8.5 14A5 5 0 1 1 15.5 14c-.6.6-1 1.3-1 2h-5c0-.7-.4-1.4-1-2z'/>",
 "heart":"<path d='M12 20s-6.6-4.3-8.6-8C1.8 8.4 4 5.4 7 6c2 .4 3.2 2 5 3.6C13.8 8 15 6.4 17 6c3-.6 5.2 2.4 3.6 6-2 3.7-8.6 8-8.6 8z'/>",
 "flag":"<path d='M6 21V4M6 4h11l-2 3.5L17 11H6'/>",
 "briefcase":"<rect x='3' y='8' width='18' height='12' rx='2'/><path d='M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2'/>",
 "handshake":"<path d='M8 13l2.5 2.5 2-2 2.5 2.5M4 9l4-3 4 2.5 4-2.5 4 3v5l-3 3'/>",
 "quote":"<path d='M7 7H4v6h4V9c0-1 .5-2 2-2V4C8 4 7 5.5 7 7zM17 7h-3v6h4V9c0-1 .5-2 2-2V4c-2 0-3 1.5-3 3z' fill='currentColor' stroke='none'/>",
 "users":"<circle cx='9' cy='8' r='3.5'/><path d='M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5'/><path d='M16 5.2A3.4 3.4 0 0 1 16 12M21 20c0-2.6-1.4-4.5-3.5-5.3'/>",
 "coin":"<circle cx='12' cy='12' r='9'/><path d='M12 7v10M9.3 9.2c0-1.2 1.2-1.8 2.7-1.8s2.7.7 2.7 1.9-1.2 1.7-2.7 1.7-2.7.6-2.7 1.8 1.2 1.9 2.7 1.9 2.7-.6 2.7-1.8'/>",
 "clipboard":"<rect x='6' y='4' width='12' height='17' rx='2'/><path d='M9 4V3h6v1'/><path d='M9 10h6M9 14h6M9 18h3'/>",
}
def ic(n): return _IC.get(n,"")
def svg(name,color,sz=30):
    return (f"<svg width='{sz}' height='{sz}' viewBox='0 0 24 24' fill='none' stroke='{color}' "
            f"stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>{ic(name)}</svg>")

# --- reusable furniture (brand-locked, look-neutral) ---
def logo_tl(left=56, top=44, h=LOGO):
    return f"<div style='position:absolute;left:{left}px;top:{top}px;'><img src='{WHT}' style='height:{h}px;'></div>"

def eyebrow(tag, left, top, color=AMBER):
    return (f"<div style=\"position:absolute;left:{left}px;top:{top}px;font-family:'DM Sans';font-weight:700;"
            f"font-size:22px;color:{color};letter-spacing:4px;\">{tag}</div>"
            f"<div style='position:absolute;left:{left}px;top:{top+34}px;width:64px;height:4px;"
            f"background:{color};border-radius:2px;'></div>")

def url_footer(left=56, bottom=44, color=MUT, roundel=AMBER, ink=DEEP, text=URL):
    return (f"<div style='position:absolute;left:{left}px;bottom:{bottom}px;display:flex;align-items:center;gap:13px;'>"
            f"<div style='width:34px;height:34px;border-radius:50%;background:{roundel};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='17' height='17' viewBox='0 0 24 24' fill='none' stroke='{ink}' stroke-width='2.6' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg></div>"
            f"<span style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{color};letter-spacing:1px;\">{text}</span></div>")

def url_pill(right=56, bottom=44, bg=AMBER, ink=DEEP):
    return (f"<div style='position:absolute;right:{right}px;bottom:{bottom}px;display:inline-flex;align-items:center;gap:11px;"
            f"height:52px;padding:0 24px;border-radius:26px;background:{bg};'>"
            f"<svg width='19' height='19' viewBox='0 0 24 24' fill='none' stroke='{ink}' stroke-width='2.6' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M7 17L17 7M9 7h8v8'/></svg>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:21px;color:{ink};letter-spacing:.3px;\">{URL}</span></div>")

def watermark(w=540, right=-90, bottom=-120, op=.05, tint="light"):
    """Large faint icon-mark bleeding off bottom-right; use on >=50%-empty slides.
    tint='light' -> white mark (dark bgs); tint='dark' -> black mark (light bgs)."""
    filt = "brightness(0) invert(1)" if tint == "light" else "brightness(0)"
    return (f"<img src='{ICONMARK}' style='position:absolute;right:{right}px;bottom:{bottom}px;width:{w}px;"
            f"filter:{filt};opacity:{op};pointer-events:none;'>")

def dots(css, color="rgba(255,177,32,.45)", w=176, h=120):
    return (f"<div style='position:absolute;{css}width:{w}px;height:{h}px;"
            f"background-image:radial-gradient({color} 3px,transparent 3px);background-size:24px 24px;'></div>")

def render(out_dir, filename, inner, page_css=""):
    """Render one 1080x1080 slide (device_scale_factor=2 -> 2160px)."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    html = (f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{F}"
            f"*{{margin:0;padding:0;box-sizing:border-box;}}"
            f"body{{width:1080px;height:1080px;overflow:hidden;}}"
            f".r{{width:1080px;height:1080px;position:relative;overflow:hidden;}}{page_css}"
            f"</style></head><body><div class='r'>{inner}</div></body></html>")
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width":1080,"height":1080}, device_scale_factor=2)
        pg.set_content(html, wait_until="networkidle")
        pg.screenshot(path=path, type="png"); br.close()
    print("  ok", os.path.relpath(path, BASE))
    return path

def load(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as fh:
        import json; return json.load(fh)


# ================================================================================
#  HERO TYPOGRAPHY  -  DESIGN_DIRECTION.md lines 11, 12, 17 and 35
# ================================================================================
# The direction says hook headlines must carry a distinctive typographic move: the
# word that holds the meaning gets a contrasting treatment (serif italic, a scale
# jump, a highlight, isolation) rather than sitting in the same Inter block as the
# rest of the line.
#
# That already existed, but ONLY as hardcoded branches - `if "follow-up" in
# headline`, `if "tracker" in headline` and four others - each with its hero word
# ("Follow-Up", "Proof", "First", "Smarter", "Job Hunt") written into the source.
# Any topic outside that fixed list, which is every topic the demand ranking has
# surfaced since, fell through to a flat single-weight Inter block. hero() makes
# the move general: it finds the meaning-bearing word in ANY headline and renders
# one of nine moves, so each world's hook has its own type personality.

# Words that never carry the meaning of a hook, so never become the hero word.
_STOP = {
    "a","an","and","are","as","at","be","but","by","can","do","does","for","from",
    "get","go","has","have","how","in","is","it","its","let","make","my","no","not",
    "of","on","or","our","out","so","that","the","their","them","then","there",
    "these","they","this","to","up","us","was","we","what","when","which","who",
    "why","will","with","you","your","into","more","most","now","just","about",
    "stand","keep","like","over","than","too","very","every","want","need",
}

def _is_content(w):
    return "".join(c for c in w.lower() if c.isalpha()) not in _STOP


def hero_split(text):
    """Split a headline into (lead, hero). The hero is the word that carries the
    meaning - the direction's own example is "Is your cover letter too polite?",
    where "Polite?" is the hook, not "letter".

    Preference order, which matches how the hand-built hooks chose their hero:
      1. the final word, if it is a content word of 4+ characters (hooks usually
         land on their point: "...Job Rejections", "...Work Experience")
      2. otherwise the longest content word in the line
      3. otherwise the final word, whatever it is
    A one-word headline is all hero and has no lead."""
    words = (text or "").split()
    if not words:
        return "", ""
    if len(words) == 1:
        return "", words[0]
    last = words[-1]
    if _is_content(last) and len(last.strip("?!.,:;")) >= 4:
        return " ".join(words[:-1]), last
    content = [w for w in words if _is_content(w) and len(w.strip("?!.,:;")) >= 4]
    if content:
        hero = max(content, key=lambda w: len(w))
        i = words.index(hero)
        # Keep reading order: anything after the hero joins the hero, never the lead.
        return " ".join(words[:i]), " ".join(words[i:])
    # Nothing long enough stands alone ("...Stand Out", "...Set Up"). Take the last
    # PAIR rather than a bare preposition, which reads as a typo at 100px.
    return " ".join(words[:-2]), " ".join(words[-2:])


# Each move is a different way of making the hero word the visual event. Worlds are
# assigned one each (HERO_MOVE below) so no two hooks in a week share a type idea.
MOVES = ("serif_italic", "highlight", "underline", "outline", "scalejump",
         "shadow", "boxed", "stack", "quoted")


def hero(text, move, ink, accent, hi=None, size=66, deep="#0A1830", width=None,
         lead_weight=800, align="left"):
    """Render a headline with the hero word given a distinctive typographic move.

    size   - type size of the LEAD words; the hero scales off this per move.
    ink    - lead colour.   accent - hero colour.   hi - highlight/secondary colour.
    Returns a positioned-free block; the caller wraps it in its own absolute div."""
    hi = hi or accent
    lead, h = hero_split(text)
    if not h:
        return ""
    # A long hero word has to come down in size or it overruns the column.
    n = len(h.strip("?!.,:;"))
    def fit(mult, cap=1.0):
        s = size * mult
        if n > 12:   s *= 0.70
        elif n > 9:  s *= 0.82
        elif n > 7:  s *= 0.92
        return round(s * cap)

    base = (f"font-family:Inter;font-weight:{lead_weight};font-size:{size}px;line-height:1.02;"
            f"letter-spacing:-1.8px;color:{ink};word-break:keep-all;")
    serif = "font-family:IWSerif,Georgia,serif;font-style:italic;font-weight:400;"
    lead_html = f"<div style=\"{base}\">{lead}</div>" if lead else ""

    if move == "serif_italic":
        hero_html = (f"<div style=\"{serif}font-size:{fit(1.45)}px;line-height:.92;color:{accent};"
                     f"margin-top:6px;letter-spacing:-1px;\">{h}</div>")
    elif move == "highlight":
        # line-height has to clear the descenders: a rotated inline-block does not
        # contribute its rotation to layout height, so a tight .9 leading let the
        # painted bar hang outside the parent card.
        hero_html = (f"<div style=\"display:inline-block;{serif}font-size:{fit(1.28)}px;line-height:1.06;"
                     f"color:{accent};background:linear-gradient(transparent 56%,{hi} 56%);"
                     f"padding:2px 12px 6px;margin-top:10px;transform:rotate(-2deg);\">{h}</div>")
    elif move == "underline":
        hero_html = (f"<div style=\"display:inline-block;font-family:Inter;font-weight:900;"
                     f"font-size:{fit(1.18)}px;line-height:.98;letter-spacing:-2.4px;color:{accent};"
                     f"margin-top:8px;padding-bottom:12px;border-bottom:10px solid {hi};\">{h}</div>")
    elif move == "outline":
        # A hairline stroke disappears at thumbnail size on a dark ground, which is
        # exactly where these are read. Scale the stroke with the type.
        stroke = max(4, round(fit(1.42) * 0.055))
        hero_html = (f"<div style=\"font-family:Inter;font-weight:900;font-size:{fit(1.42)}px;"
                     f"line-height:.94;letter-spacing:-3px;margin-top:8px;color:transparent;"
                     f"-webkit-text-stroke:{stroke}px {accent};\">{h}</div>")
    elif move == "scalejump":
        hero_html = (f"<div style=\"font-family:Inter;font-weight:900;font-size:{fit(1.70)}px;"
                     f"line-height:.84;letter-spacing:-4px;color:{accent};margin-top:4px;\">{h}</div>")
    elif move == "shadow":
        hero_html = (f"<div style=\"{serif}font-size:{fit(1.55)}px;line-height:.86;color:{accent};"
                     f"margin-top:8px;text-shadow:7px 7px 0 {hi};\">{h}</div>")
    elif move == "boxed":
        hero_html = (f"<div style=\"display:inline-block;font-family:Inter;font-weight:900;"
                     f"font-size:{fit(1.05)}px;line-height:1;letter-spacing:-2px;color:{deep};"
                     f"background:{accent};padding:12px 20px 16px;border-radius:14px;margin-top:12px;\">{h}</div>")
    elif move == "stack":
        hero_html = (f"<div style='width:64px;height:7px;background:{hi};border-radius:4px;margin:18px 0 14px;'></div>"
                     f"<div style=\"font-family:IWSerif,Georgia,serif;font-weight:400;font-size:{fit(1.22)}px;"
                     f"line-height:.95;letter-spacing:2px;color:{accent};\">{h}</div>")
    elif move == "quoted":
        g = round(fit(1.30) * 1.15)
        hero_html = (f"<div style='display:flex;align-items:flex-start;gap:6px;margin-top:6px;'>"
                     f"<span style=\"font-family:IWSerif,Georgia,serif;font-size:{g}px;line-height:.72;"
                     f"color:{hi};opacity:.55;\">&ldquo;</span>"
                     f"<span style=\"{serif}font-size:{fit(1.30)}px;line-height:.92;color:{accent};\">{h}</span></div>")
    else:
        hero_html = f"<div style=\"{base}color:{accent};margin-top:4px;\">{h}</div>"

    w = f"width:{width}px;" if width else ""
    # flow-root: without it the hero's margin-top collapses THROUGH this wrapper and
    # out of the caller's card, so the card measured short and the hero hung over
    # its bottom edge (seen on the cream billboard).
    return (f"<div style='{w}text-align:{align};display:flow-root;overflow:visible;'>"
            f"{lead_html}{hero_html}</div>")
