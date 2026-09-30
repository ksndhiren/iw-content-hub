"""Quote lane - a LIBRARY of genuinely distinct design worlds (rotates per post, so
every quote looks different and nothing repeats within a month).

Each world is its OWN art direction - not the same skeleton recoloured:
  spotlight  -> cinematic portrait (dark stage, author as ghosted hero)
  colorblock -> brutalist coral poster (Swiss grid, monotone author bleed)
  split      -> editorial magazine (author duotone inside the colour panel)
  paper      -> pinned polaroid / scrapbook card
  editorial  -> vintage cream broadsheet

The quote AUTHOR is a low-opacity WATERMARK woven into each layout (behind the
text), not a full-opacity cut-out sticker. Drop a real portrait in
assets/quote_authors/<slug>.<ext>; quote rendering fails if the portrait is
missing so scheduled runs cannot silently ship blank or typographic stand-ins.

    render_quote(q, world, out_dir, "slide_1.png")   # world in WORLDS
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lanes_common as L
import wk11_base as b

NAVY, DEEP, INK, MUT = L.NAVY, L.DEEP, L.INK, L.MUT
AMBER, CORAL, GREEN = L.AMBER, L.CORAL, L.GREEN
WHT, DARK = L.WHT, L.DARKLOGO
Q = "&ldquo;"


def _logo(src, left=56, top=52, h=L.LOGO):
    return f"<div style='position:absolute;left:{left}px;top:{top}px;'><img src='{src}' style='height:{h}px;'></div>"

def _eyebrow(txt, color, right=60, top=76):
    return (f"<div style=\"position:absolute;right:{right}px;top:{top}px;font-family:'DM Sans';font-weight:700;"
            f"font-size:21px;color:{color};letter-spacing:5px;\">{txt}</div>")

def _cta_row(cta, ink, accent, left=56, right=70, bottom=50):
    return (f"<div style='position:absolute;left:{left}px;right:{right}px;bottom:{bottom}px;'>"
            f"<div style='height:2px;background:{ink};opacity:.18;margin-bottom:20px;'></div>"
            f"<div style='display:flex;align-items:center;gap:16px;'>"
            f"<div style='flex:0 0 auto;width:48px;height:48px;border-radius:50%;background:{accent};display:flex;align-items:center;justify-content:center;'>"
            f"<svg width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' "
            f"stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h14M13 6l6 6-6 6'/></svg></div>"
            f"<span style=\"font-family:Inter;font-weight:700;font-size:29px;color:{ink};letter-spacing:-.3px;\">{cta}</span></div></div>")


# --- author watermark -------------------------------------------------------
# Real author portrait, placed as a large, FAINT (low-opacity) watermark woven
# behind the quote text. Each world positions/tints its own.
_AUTH_DIR = os.path.join(L.BASE, "assets", "quote_authors")
_AUTH_CACHE = os.path.join(_AUTH_DIR, "_cutout")


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def author_image(author):
    """data URI for a real quote-author portrait, or None when missing."""
    slug = _slug(author)
    if not slug:
        return None
    raw = next((os.path.join(_AUTH_DIR, slug + "." + e)
                for e in ("jpg", "jpeg", "png", "webp")
                if os.path.exists(os.path.join(_AUTH_DIR, slug + "." + e))), None)
    return L.img(raw) if raw else None


def _wm(src, css, op=0.13, filt="grayscale(1)"):
    """One faint author watermark <img>. Empty string when no photo exists."""
    if not src:
        return ""
    op = min(float(op), 0.06)
    return (f"<img src='{src}' style='position:absolute;{css}opacity:{op};"
            f"filter:{filt};pointer-events:none;'>")


# ---- World 1: cinematic portrait (dark stage) ----
def w_spotlight(q, src=None):
    bg = f"<div style='position:absolute;inset:0;background:radial-gradient(80% 70% at 50% 30%,#183157,{NAVY} 62%,{DEEP});'></div>"
    # Author is the hero: large, centred, ghosted. A bottom scrim seats the text.
    wm = _wm(src, "left:50%;bottom:0;transform:translateX(-50%);height:940px;",
             op=.11, filt="grayscale(1) contrast(1.04) brightness(1.16)")
    scrim = (f"<div style='position:absolute;left:0;right:0;bottom:0;height:640px;"
             f"background:linear-gradient(180deg,rgba(10,24,48,0) 0%,rgba(10,24,48,.72) 46%,{DEEP} 88%);'></div>")
    eyebrow = (f"<div style=\"position:absolute;left:0;right:0;top:300px;text-align:center;font-family:'DM Sans';"
               f"font-weight:700;font-size:20px;color:{AMBER};letter-spacing:7px;\">QUOTE OF THE DAY</div>")
    body = (f"<div style='position:absolute;left:96px;right:96px;bottom:236px;text-align:center;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:70px;line-height:1.16;letter-spacing:-1.2px;color:{INK};word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:76px;height:5px;background:{AMBER};border-radius:3px;margin:34px auto 22px;'></div>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:29px;color:{AMBER};letter-spacing:1.5px;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:70px;text-align:center;font-family:Inter;font-weight:700;"
           f"font-size:26px;color:{MUT};letter-spacing:.3px;\">{q['cta']}</div>")
    logo = f"<div style='position:absolute;left:0;right:0;top:52px;text-align:center;'><img src='{WHT}' style='height:82px;'></div>"
    return bg + wm + scrim + logo + eyebrow + body + cta


# ---- World 2: brutalist coral poster (Swiss grid) ----
def w_colorblock(q, src=None):
    bg = f"<div style='position:absolute;inset:0;background:{CORAL};'></div>"
    bar = f"<div style='position:absolute;left:0;top:0;bottom:0;width:26px;background:{AMBER};'></div>"
    # Monotone author bleeding off the right, low opacity - a poster device.
    wm = _wm(src, "right:-72px;bottom:0;height:880px;", op=.11, filt="grayscale(1) brightness(1.06)")
    dots = L.dots("right:70px;top:150px;", color="rgba(255,255,255,.30)", w=210, h=150)
    kicker = (f"<div style=\"position:absolute;left:70px;top:210px;font-family:'DM Sans';font-weight:800;"
              f"font-size:20px;color:{DEEP};letter-spacing:6px;\">QUOTE OF THE DAY</div>")
    body = (f"<div style='position:absolute;left:70px;right:150px;top:270px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:88px;line-height:1.04;letter-spacing:-2.5px;color:#fff;word-break:keep-all;\">{q['text']}</div></div>")
    author = (f"<div style='position:absolute;left:70px;bottom:150px;display:flex;align-items:center;gap:16px;'>"
              f"<div style='width:26px;height:26px;background:{DEEP};'></div>"
              f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:34px;color:{DEEP};letter-spacing:-.5px;\">{q['author']}</span></div>")
    cta = (f"<div style='position:absolute;left:70px;bottom:56px;display:flex;align-items:center;gap:14px;'>"
           f"<div style='width:46px;height:46px;border-radius:50%;background:{DEEP};display:flex;align-items:center;justify-content:center;'>"
           f"<svg width='23' height='23' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h14M13 6l6 6-6 6'/></svg></div>"
           f"<span style=\"font-family:Inter;font-weight:700;font-size:26px;color:{DEEP};\">{q['cta']}</span></div>")
    return bg + bar + wm + dots + _logo(WHT) + kicker + body + author + cta


# ---- World 3: editorial magazine (colour panel + duotone author) ----
def w_split(q, src=None):
    PANEL = 428
    bg = "<div style='position:absolute;inset:0;background:#F3EADA;'></div>"
    # The navy panel is an overflow-clipped frame; the author lives INSIDE it as a
    # brightened duotone watermark - reads like a printed magazine masthead photo.
    panel_wm = _wm(src, "left:-24px;bottom:0;height:668px;", op=.17, filt="grayscale(1) brightness(1.5) contrast(1.05)")
    panel = (f"<div style='position:absolute;left:0;top:0;bottom:0;width:{PANEL}px;background:{NAVY};overflow:hidden;'>"
             f"{panel_wm}"
             f"<div style='position:absolute;left:40px;top:280px;font-family:Georgia,serif;font-weight:700;font-size:280px;line-height:.6;color:{AMBER};opacity:.9;'>{Q}</div>"
             f"<div style=\"position:absolute;left:56px;bottom:68px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{INK};letter-spacing:5px;\">QUOTE OF<br>THE DAY</div></div>")
    body = (f"<div style='position:absolute;left:{PANEL+52}px;right:64px;top:296px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:60px;line-height:1.14;letter-spacing:-1px;color:#152743;word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:80px;height:5px;background:{CORAL};border-radius:3px;margin:32px 0 22px;'></div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:30px;color:#152743;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:{PANEL+52}px;right:64px;bottom:56px;font-family:Inter;font-weight:700;font-size:25px;color:#8A7B62;\">{q['cta']}</div>")
    return bg + panel + _logo(WHT, left=44, top=48, h=76) + body + cta


# ---- World 4: pinned polaroid / scrapbook ----
def w_paper(q, src=None):
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#1a2f57,{NAVY} 60%,{DEEP});'></div>"
    grid = ("<div style='position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:56px 56px;'></div>")
    # Faint author washed across the board behind the pinned card.
    wm = _wm(src, "right:18px;bottom:18px;height:620px;object-fit:contain;object-position:center bottom;", op=.075, filt="grayscale(1) brightness(1.22)")
    card = (f"<div style='position:absolute;left:110px;right:110px;top:300px;background:#FBFCFE;border-radius:22px;"
            f"box-shadow:0 40px 80px rgba(0,0,0,.5);padding:56px 54px 48px;transform:rotate(-2deg);'>"
            f"<div style='font-family:Georgia,serif;font-weight:700;font-size:130px;line-height:.4;color:{AMBER};height:70px;'>{Q}</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:56px;line-height:1.14;letter-spacing:-1px;color:#1c2740;word-break:keep-all;\">{q['text']}</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:28px;color:#5b6b82;margin-top:28px;\">- {q['author']}</div></div>")
    tape = f"<div style='position:absolute;left:490px;top:286px;width:150px;height:44px;background:rgba(255,177,32,.7);transform:rotate(-4deg);'></div>"
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:80px;text-align:center;font-family:Inter;font-weight:700;font-size:27px;color:{AMBER};\">{q['cta']}</div>")
    return bg + grid + wm + tape + card + L.logo_tl() + cta


# ---- World 5: vintage cream broadsheet ----
def w_editorial(q, src=None):
    CREAM = "#F3EADA"; PAPER = "#EFE3CE"; NAVYT = "#152743"; COFFEE = "#8A7B62"
    bg = f"<div style='position:absolute;inset:0;background:radial-gradient(120% 100% at 15% 0%,{CREAM},{PAPER});'></div>"
    tex = ("<div style='position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(138,123,98,.12) 1.5px,transparent 1.5px);background-size:30px 30px;'></div>")
    # Sepia author watermark on the right, like a faded printed portrait.
    wm = _wm(src, "right:-34px;top:150px;height:770px;", op=.09, filt="grayscale(1) sepia(.4) contrast(1.03)")
    glyph = f"<div style='position:absolute;left:52px;top:322px;font-family:Georgia,serif;font-weight:700;font-size:240px;line-height:.7;color:{AMBER};'>{Q}</div>"
    body = (f"<div style='position:absolute;left:60px;right:70px;top:520px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:78px;line-height:1.12;letter-spacing:-1.5px;color:{NAVYT};word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:96px;height:6px;background:{CORAL};border-radius:3px;margin:40px 0 26px;'></div>"
            f"<div style='display:inline-flex;align-items:center;gap:16px;'>"
            f"<div style='width:52px;height:52px;border-radius:50%;background:{NAVYT};display:flex;align-items:center;justify-content:center;'>{L.svg('user',AMBER,26)}</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:34px;color:{NAVYT};\">{q['author']}</div></div></div>")
    return bg + tex + wm + glyph + _logo(DARK) + _eyebrow("QUOTE OF THE DAY", COFFEE) + body + _cta_row(q['cta'], NAVYT, CORAL)


# ---- World 6: premium amber-arc (navy, wk12 furniture) ----
def w_arc(q, src=None):
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(150deg,#1c3560,{NAVY} 58%,{DEEP});'></div>"
    # A large amber ring behind the author, bottom-right - the premium arc device.
    arc = ("<div style='position:absolute;right:-190px;bottom:-190px;width:760px;height:760px;border-radius:50%;"
           f"border:60px solid {AMBER};opacity:.9;'></div>")
    ring2 = ("<div style='position:absolute;right:-60px;bottom:-60px;width:470px;height:470px;border-radius:50%;"
             f"border:3px solid {GREEN};opacity:.55;'></div>")
    wm = _wm(src, "right:-30px;bottom:0;height:720px;", op=.16, filt="grayscale(1) contrast(1.05) brightness(1.1)")
    kicker = (f"<div style=\"position:absolute;left:60px;top:210px;font-family:'DM Sans';font-weight:800;"
              f"font-size:20px;color:{AMBER};letter-spacing:6px;\">QUOTE OF THE DAY</div>")
    body = (f"<div style='position:absolute;left:60px;right:300px;top:266px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:74px;line-height:1.1;letter-spacing:-1.6px;color:{INK};word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:84px;height:5px;background:{GREEN};border-radius:3px;margin:34px 0 22px;'></div>"
            f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:32px;color:{AMBER};letter-spacing:-.3px;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:60px;right:300px;bottom:60px;font-family:Inter;font-weight:700;"
           f"font-size:26px;color:{MUT};\">{q['cta']}</div>")
    return bg + arc + ring2 + wm + _logo(WHT) + kicker + body + cta


# ---- World 7: blueprint / technical (teal ground, measured grid) ----
def w_blueprint(q, src=None):
    TEAL = "#1f4f4d"
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#245a57,{TEAL} 70%,#173b39);'></div>"
    grid = ("<div style='position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),"
            "linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:60px 60px;'></div>")
    ticks = ("<div style='position:absolute;left:0;right:0;top:150px;height:1px;background:rgba(255,255,255,.25);'></div>"
             "<div style='position:absolute;left:0;right:0;bottom:150px;height:1px;background:rgba(255,255,255,.25);'></div>"
             "<div style='position:absolute;left:60px;top:0;bottom:0;width:1px;background:rgba(255,255,255,.16);'></div>")
    wm = _wm(src, "right:-30px;bottom:150px;height:640px;", op=.10, filt="grayscale(1) brightness(1.1)")
    kicker = (f"<div style=\"position:absolute;left:60px;top:186px;font-family:'DM Mono',monospace;font-weight:700;"
              f"font-size:19px;color:{AMBER};letter-spacing:6px;\">// QUOTE OF THE DAY</div>")
    body = (f"<div style='position:absolute;left:60px;right:110px;top:250px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:78px;line-height:1.08;letter-spacing:-1.8px;color:#fff;word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:120px;height:6px;background:{AMBER};border-radius:2px;margin:36px 0 20px;'></div>"
            f"<div style=\"font-family:'DM Mono',monospace;font-weight:700;font-size:28px;color:{AMBER};letter-spacing:-.2px;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:60px;right:110px;bottom:64px;font-family:'DM Mono',monospace;font-weight:600;"
           f"font-size:24px;color:rgba(255,255,255,.82);\">{q['cta']}</div>")
    return bg + grid + ticks + wm + _logo(WHT) + kicker + body + cta


# ---- World 8: headline band (cream, bold navy band) ----
def w_band(q, src=None):
    CREAM = "#F3EADA"; COFFEE = "#8A7B62"
    bg = f"<div style='position:absolute;inset:0;background:{CREAM};'></div>"
    wm = _wm(src, "right:-40px;bottom:0;height:430px;", op=.10, filt="grayscale(1) sepia(.25)")
    kicker = (f"<div style=\"position:absolute;left:64px;top:170px;font-family:'DM Sans';font-weight:800;"
              f"font-size:20px;color:{COFFEE};letter-spacing:6px;\">QUOTE OF THE DAY</div>")
    glyph = f"<div style='position:absolute;right:70px;top:120px;font-family:Georgia,serif;font-weight:700;font-size:170px;line-height:.5;color:{AMBER};opacity:.5;'>{Q}</div>"
    rule_t = f"<div style='position:absolute;left:0;right:0;top:322px;height:6px;background:{AMBER};'></div>"
    band = (f"<div style='position:absolute;left:0;right:0;top:328px;background:{NAVY};padding:56px 64px 60px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:72px;line-height:1.1;letter-spacing:-1.6px;color:#fff;word-break:keep-all;\">{q['text']}</div></div>")
    author = (f"<div style='position:absolute;left:64px;bottom:150px;display:flex;align-items:center;gap:16px;'>"
              f"<div style='width:24px;height:24px;background:{CORAL};'></div>"
              f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:34px;color:{NAVY};letter-spacing:-.4px;\">{q['author']}</span></div>")
    cta = (f"<div style=\"position:absolute;left:64px;bottom:64px;font-family:Inter;font-weight:700;font-size:25px;color:{COFFEE};\">{q['cta']}</div>")
    return bg + wm + kicker + glyph + rule_t + band + author + cta + _logo(DARK)


# ---- World 9: minimal serif (calm white, high whitespace) ----
def w_minimal(q, src=None):
    INKN = "#152743"
    bg = "<div style='position:absolute;inset:0;background:#FFFFFF;'></div>"
    wm = _wm(src, "left:50%;bottom:40px;transform:translateX(-50%);height:520px;", op=.06, filt="grayscale(1)")
    rule_t = f"<div style='position:absolute;left:180px;right:180px;top:250px;height:2px;background:{GREEN};opacity:.5;'></div>"
    rule_b = f"<div style='position:absolute;left:180px;right:180px;bottom:250px;height:2px;background:{GREEN};opacity:.5;'></div>"
    kicker = (f"<div style=\"position:absolute;left:0;right:0;top:290px;text-align:center;font-family:'DM Sans';font-weight:700;"
              f"font-size:19px;color:{GREEN};letter-spacing:7px;\">QUOTE OF THE DAY</div>")
    body = (f"<div style='position:absolute;left:110px;right:110px;top:360px;text-align:center;'>"
            f"<div style=\"font-family:Georgia,serif;font-weight:700;font-size:66px;line-height:1.2;letter-spacing:-.5px;color:{INKN};word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:70px;height:4px;background:{AMBER};border-radius:3px;margin:34px auto 20px;'></div>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:27px;color:{INKN};letter-spacing:.5px;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:170px;text-align:center;font-family:Inter;font-weight:700;"
           f"font-size:24px;color:#8A93A3;\">{q['cta']}</div>")
    return bg + wm + rule_t + rule_b + _logo(DARK) + kicker + body + cta


# ---- World 10: speech bubble (teal, conversational) ----
def w_bubble(q, src=None):
    TEAL = "#2c6e6a"
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(155deg,#34817c,{TEAL} 68%,#1f4f4d);'></div>"
    dots = L.dots("right:70px;top:150px;", color="rgba(255,255,255,.22)", w=200, h=140)
    wm = _wm(src, "right:-40px;bottom:0;height:520px;", op=.09, filt="grayscale(1) brightness(1.1)")
    kicker = (f"<div style=\"position:absolute;left:60px;top:214px;font-family:'DM Sans';font-weight:800;"
              f"font-size:20px;color:{AMBER};letter-spacing:6px;\">QUOTE OF THE DAY</div>")
    card = (f"<div style='position:absolute;left:60px;right:110px;top:280px;background:#FBFCFE;border-radius:30px;"
            f"box-shadow:0 34px 70px rgba(0,0,0,.32);padding:52px 52px 46px;'>"
            f"<div style='font-family:Georgia,serif;font-weight:700;font-size:120px;line-height:.4;color:{AMBER};height:66px;'>{Q}</div>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:62px;line-height:1.12;letter-spacing:-1.3px;color:#1c2740;word-break:keep-all;\">{q['text']}</div></div>")
    tail = f"<div style='position:absolute;left:150px;top:606px;width:56px;height:56px;background:#FBFCFE;transform:rotate(45deg);box-shadow:0 34px 70px rgba(0,0,0,.10);'></div>"
    author = (f"<div style='position:absolute;left:60px;bottom:150px;display:flex;align-items:center;gap:14px;'>"
              f"<div style='width:44px;height:44px;border-radius:50%;background:{AMBER};display:flex;align-items:center;justify-content:center;'>{L.svg('user',TEAL,24)}</div>"
              f"<span style=\"font-family:'DM Sans';font-weight:800;font-size:32px;color:#fff;letter-spacing:-.3px;\">{q['author']}</span></div>")
    cta = (f"<div style=\"position:absolute;left:60px;bottom:64px;font-family:Inter;font-weight:700;font-size:25px;color:rgba(255,255,255,.85);\">{q['cta']}</div>")
    return bg + dots + wm + _logo(WHT) + kicker + card + tail + author + cta


# ---- World 11: marquee (dark plaque, amber double-frame + bulbs) ----
def w_marquee(q, src=None):
    bg = f"<div style='position:absolute;inset:0;background:radial-gradient(90% 80% at 50% 24%,#183157,{NAVY} 60%,{DEEP});'></div>"
    wm = _wm(src, "left:50%;bottom:0;transform:translateX(-50%);height:880px;", op=.07,
             filt="grayscale(1) brightness(1.15)")
    frame = (f"<div style='position:absolute;left:70px;right:70px;top:250px;bottom:250px;border:3px solid {AMBER};"
             f"border-radius:26px;box-shadow:inset 0 0 0 10px rgba(255,177,32,.14);'></div>")
    # corner bulbs
    bulbs = "".join(
        f"<div style='position:absolute;{css}width:18px;height:18px;border-radius:50%;background:{AMBER};box-shadow:0 0 16px {AMBER};'></div>"
        for css in ("left:92px;top:272px;", "right:92px;top:272px;", "left:92px;bottom:272px;", "right:92px;bottom:272px;"))
    logo = f"<div style='position:absolute;left:0;right:0;top:70px;text-align:center;'><img src='{WHT}' style='height:78px;'></div>"
    kicker = (f"<div style=\"position:absolute;left:0;right:0;top:322px;text-align:center;font-family:'DM Sans';font-weight:800;"
              f"font-size:20px;color:{AMBER};letter-spacing:7px;\">QUOTE OF THE DAY</div>")
    body = (f"<div style='position:absolute;left:130px;right:130px;top:404px;text-align:center;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:64px;line-height:1.16;letter-spacing:-1.2px;color:{INK};word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:76px;height:5px;background:{AMBER};border-radius:3px;margin:34px auto 22px;'></div>"
            f"<div style=\"font-family:'DM Sans';font-weight:800;font-size:30px;color:{AMBER};letter-spacing:1px;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:150px;text-align:center;font-family:Inter;font-weight:700;"
           f"font-size:26px;color:{MUT};\">{q['cta']}</div>")
    return bg + wm + frame + bulbs + logo + kicker + body + cta


# ---- World 12: stamp (teal, clean card + circular seal) ----
def w_stamp(q, src=None):
    TEAL = "#1f4f4d"; NAVYT = "#152743"; COFFEE = "#5b6b6a"
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(158deg,#276460,{TEAL} 70%,#143432);'></div>"
    dots = L.dots("right:70px;bottom:70px;", color="rgba(255,255,255,.16)", w=180, h=120)
    wm = _wm(src, "right:-30px;bottom:0;height:520px;", op=.07, filt="grayscale(1) brightness(1.1)")
    kicker = (f"<div style=\"position:absolute;left:74px;top:186px;font-family:'DM Sans';font-weight:800;"
              f"font-size:20px;color:{AMBER};letter-spacing:6px;\">QUOTE OF THE DAY</div>")
    card = (f"<div style='position:absolute;left:70px;right:70px;top:250px;bottom:228px;background:#FBFCFE;border-radius:28px;"
            f"box-shadow:0 34px 70px rgba(0,0,0,.34);padding:56px 56px 48px;'>"
            f"<div style='font-family:Georgia,serif;font-weight:700;font-size:130px;line-height:.4;color:{AMBER};height:72px;'>{Q}</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:58px;line-height:1.14;letter-spacing:-1px;color:{NAVYT};word-break:keep-all;\">{q['text']}</div>"
            f"<div style=\"position:absolute;left:56px;bottom:46px;font-family:'DM Sans';font-weight:800;font-size:30px;color:{NAVYT};\">{q['author']}</div></div>")
    seal = (f"<div style='position:absolute;right:104px;top:206px;width:132px;height:132px;border-radius:50%;background:{AMBER};"
            f"border:5px solid #FBFCFE;box-shadow:0 14px 30px rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center;'>"
            f"{L.svg('star', NAVYT, 58)}</div>")
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:120px;text-align:center;font-family:Inter;font-weight:700;"
           f"font-size:25px;color:rgba(255,255,255,.9);\">{q['cta']}</div>")
    return bg + dots + wm + _logo(WHT) + kicker + card + seal + cta


WORLDS = {"editorial": w_editorial, "spotlight": w_spotlight, "colorblock": w_colorblock,
          "split": w_split, "paper": w_paper,
          "arc": w_arc, "blueprint": w_blueprint, "band": w_band,
          "minimal": w_minimal, "bubble": w_bubble,
          "marquee": w_marquee, "stamp": w_stamp}

# Only q001-q005 in the bank carry a "cta"; the rest don't, so fall back on-brand.
_DEFAULT_CTA = "Find your internship at internwise.co.uk"


def render_quote(q, world, out_dir, filename="slide_1.png"):
    author = q.get("author", "")
    src = author_image(author)
    if not src:
        raise FileNotFoundError(
            f"Quote author portrait missing for {author!r}; add assets/quote_authors/{_slug(author)}.(jpg|jpeg|png|webp)"
        )
    # Author is now a faint watermark, not a corner sticker, so the long CTA no
    # longer collides with a photo - keep the full CTA line.
    cta = q.get("cta") or _DEFAULT_CTA
    q = {**q, "cta": cta}
    inner = WORLDS[world]({**q}, src)
    return L.render(out_dir, filename, inner)


if __name__ == "__main__":
    qs = L.load("quotes_bank.json")["quotes"]
    for i, (world, q) in enumerate(zip(WORLDS.keys(), qs)):
        render_quote(q, world, os.path.join(L.OUTROOT, "week14", "_qtest", world))
