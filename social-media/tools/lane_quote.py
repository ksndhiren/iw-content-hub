"""Quote lane - a LIBRARY of genuinely distinct design worlds (rotates per post, so
every quote looks different and nothing repeats within a month).

Each world is its OWN art direction - not the same skeleton recoloured:
  spotlight  -> cinematic portrait (dark stage, author as ghosted hero)
  colorblock -> brutalist coral poster (Swiss grid, monotone author bleed)
  split      -> editorial magazine (author duotone inside the colour panel)
  paper      -> pinned polaroid / scrapbook card
  editorial  -> vintage cream broadsheet

The quote AUTHOR is a low-opacity WATERMARK woven into each layout (behind the
text), not a full-opacity cut-out sticker. Drop a photo in assets/quote_authors/
<slug>.<ext>; we rembg + cache it once.

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
# Photo -> rembg cut-out (cached), then placed as a large, FAINT (low-opacity)
# watermark woven behind the quote text. Each world positions/tints its own.
_AUTH_DIR = os.path.join(L.BASE, "assets", "quote_authors")
_AUTH_CACHE = os.path.join(_AUTH_DIR, "_cutout")


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def author_cutout(author):
    """data-URI cut-out for a quote author if a photo exists, else None.
    rembg the raw photo once and cache the transparent, tight-cropped PNG."""
    slug = _slug(author)
    if not slug:
        return None
    os.makedirs(_AUTH_CACHE, exist_ok=True)
    cache = os.path.join(_AUTH_CACHE, slug + ".png")
    if not os.path.exists(cache):
        raw = next((os.path.join(_AUTH_DIR, slug + "." + e)
                    for e in ("jpg", "jpeg", "png", "webp")
                    if os.path.exists(os.path.join(_AUTH_DIR, slug + "." + e))), None)
        if not raw:
            return None
        from rembg import remove
        from PIL import Image
        import numpy as np
        out = remove(Image.open(raw).convert("RGBA"))
        a = np.asarray(out)[..., 3]
        ys, xs = np.where(a > 40)
        if len(xs) == 0:
            return None
        out.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)).save(cache)
    return L.img(cache)


def _wm(src, css, op=0.13, filt="grayscale(1)"):
    """One faint author watermark <img>. Empty string when no photo exists."""
    if not src:
        return ""
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
    wm = _wm(src, "right:-46px;bottom:-24px;height:760px;", op=.075, filt="grayscale(1) brightness(1.22)")
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


WORLDS = {"editorial": w_editorial, "spotlight": w_spotlight, "colorblock": w_colorblock,
          "split": w_split, "paper": w_paper}

# Only q001-q005 in the bank carry a "cta"; the rest don't, so fall back on-brand.
_DEFAULT_CTA = "Find your internship at internwise.co.uk"


def render_quote(q, world, out_dir, filename="slide_1.png"):
    src = author_cutout(q.get("author", ""))
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
