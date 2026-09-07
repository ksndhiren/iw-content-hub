"""Quote lane - a LIBRARY of distinct design worlds (rotates per post, so every
quote looks different and nothing repeats within a month; also lets the future
automation pick a fresh world each time).

Each world takes q = {text, author, cta} and renders one 1080x1080 slide.
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


# ---- World 1: cream editorial ----
def w_editorial(q):
    CREAM="#F3EADA"; PAPER="#EFE3CE"; NAVYT="#152743"; COFFEE="#8A7B62"
    bg = f"<div style='position:absolute;inset:0;background:radial-gradient(120% 100% at 15% 0%,{CREAM},{PAPER});'></div>"
    tex = ("<div style='position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(138,123,98,.12) 1.5px,transparent 1.5px);background-size:30px 30px;'></div>")
    glyph = f"<div style='position:absolute;left:52px;top:322px;font-family:Georgia,serif;font-weight:700;font-size:240px;line-height:.7;color:{AMBER};'>{Q}</div>"
    wm = L.watermark(w=520, right=-70, bottom=-130, op=.05, tint="dark")
    body = (f"<div style='position:absolute;left:60px;right:70px;top:520px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:78px;line-height:1.12;letter-spacing:-1.5px;color:{NAVYT};word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:96px;height:6px;background:{CORAL};border-radius:3px;margin:40px 0 26px;'></div>"
            f"<div style='display:inline-flex;align-items:center;gap:16px;'>"
            f"<div style='width:52px;height:52px;border-radius:50%;background:{NAVYT};display:flex;align-items:center;justify-content:center;'>{L.svg('user',AMBER,26)}</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:34px;color:{NAVYT};\">{q['author']}</div></div></div>")
    return bg+tex+wm+glyph+_logo(DARK)+_eyebrow("QUOTE OF THE DAY",COFFEE)+body+_cta_row(q['cta'],NAVYT,CORAL)

# ---- World 2: dark spotlight ----
def w_spotlight(q):
    bg = f"<div style='position:absolute;inset:0;background:radial-gradient(80% 70% at 50% 32%,#183157,{NAVY} 60%,{DEEP});'></div>"
    glow = f"<div style='position:absolute;left:0;right:0;top:130px;text-align:center;font-family:Georgia,serif;font-weight:700;font-size:520px;line-height:.6;color:{AMBER};opacity:.09;'>{Q}</div>"
    body = (f"<div style='position:absolute;left:90px;right:90px;top:360px;text-align:center;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:66px;line-height:1.18;letter-spacing:-1px;color:{INK};word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:80px;height:5px;background:{AMBER};border-radius:3px;margin:38px auto 24px;'></div>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:30px;color:{AMBER};letter-spacing:1px;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:70px;text-align:center;font-family:Inter;font-weight:700;"
           f"font-size:27px;color:{MUT};\">{q['cta']}</div>")
    return bg+glow+L.logo_tl()+body+cta

# ---- World 3: coral color-block ----
def w_colorblock(q):
    bg = f"<div style='position:absolute;inset:0;background:{CORAL};'></div>"
    panel = f"<div style='position:absolute;left:0;top:0;bottom:0;width:26px;background:{AMBER};'></div>"
    dots = L.dots("right:60px;top:150px;", color="rgba(255,255,255,.35)", w=240, h=200)
    glyph = f"<div style='position:absolute;left:70px;top:150px;font-family:Georgia,serif;font-weight:700;font-size:230px;line-height:.7;color:#fff;opacity:.9;'>{Q}</div>"
    body = (f"<div style='position:absolute;left:70px;right:80px;top:430px;'>"
            f"<div style=\"font-family:Inter;font-weight:800;font-size:82px;line-height:1.08;letter-spacing:-2px;color:#fff;word-break:keep-all;\">{q['text']}</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:32px;color:{DEEP};margin-top:34px;\">- {q['author']}</div></div>")
    cta = (f"<div style='position:absolute;left:70px;right:80px;bottom:56px;display:flex;align-items:center;gap:14px;'>"
           f"<div style='width:46px;height:46px;border-radius:50%;background:{DEEP};display:flex;align-items:center;justify-content:center;'>"
           f"<svg width='23' height='23' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'><path d='M5 12h14M13 6l6 6-6 6'/></svg></div>"
           f"<span style=\"font-family:Inter;font-weight:700;font-size:27px;color:{DEEP};\">{q['cta']}</span></div>")
    return bg+panel+dots+glyph+_logo(WHT)+body+cta

# ---- World 4: split panel ----
def w_split(q):
    bg = "<div style='position:absolute;inset:0;background:#F3EADA;'></div>"
    panel = f"<div style='position:absolute;left:0;top:0;bottom:0;width:400px;background:{NAVY};'></div>"
    pglyph = f"<div style='position:absolute;left:40px;top:300px;font-family:Georgia,serif;font-weight:700;font-size:300px;line-height:.6;color:{AMBER};'>{Q}</div>"
    plabel = (f"<div style=\"position:absolute;left:56px;bottom:70px;font-family:'DM Sans';font-weight:700;font-size:22px;color:{INK};letter-spacing:5px;\">QUOTE OF<br>THE DAY</div>")
    body = (f"<div style='position:absolute;left:452px;right:64px;top:300px;'>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:60px;line-height:1.14;letter-spacing:-1px;color:#152743;word-break:keep-all;\">{q['text']}</div>"
            f"<div style='width:80px;height:5px;background:{CORAL};border-radius:3px;margin:32px 0 22px;'></div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:30px;color:#152743;\">{q['author']}</div></div>")
    cta = (f"<div style=\"position:absolute;left:452px;right:64px;bottom:56px;font-family:Inter;font-weight:700;font-size:25px;color:#8A7B62;\">{q['cta']}</div>")
    return bg+panel+pglyph+plabel+_logo(WHT,left=44,top=48,h=76)+body+cta

# ---- World 5: paper card ----
def w_paper(q):
    bg = f"<div style='position:absolute;inset:0;background:linear-gradient(160deg,#1a2f57,{NAVY} 60%,{DEEP});'></div>"
    grid = ("<div style='position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:56px 56px;'></div>")
    card = (f"<div style='position:absolute;left:110px;right:110px;top:300px;background:#FBFCFE;border-radius:22px;"
            f"box-shadow:0 40px 80px rgba(0,0,0,.5);padding:56px 54px 48px;transform:rotate(-2deg);'>"
            f"<div style='font-family:Georgia,serif;font-weight:700;font-size:130px;line-height:.4;color:{AMBER};height:70px;'>{Q}</div>"
            f"<div style=\"font-family:Inter;font-weight:700;font-size:56px;line-height:1.14;letter-spacing:-1px;color:#1c2740;word-break:keep-all;\">{q['text']}</div>"
            f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:28px;color:#5b6b82;margin-top:28px;\">- {q['author']}</div></div>")
    tape = f"<div style='position:absolute;left:490px;top:286px;width:150px;height:44px;background:rgba(255,177,32,.7);transform:rotate(-4deg);'></div>"
    cta = (f"<div style=\"position:absolute;left:0;right:0;bottom:80px;text-align:center;font-family:Inter;font-weight:700;font-size:27px;color:{AMBER};\">{q['cta']}</div>")
    return bg+grid+tape+card+L.logo_tl()+cta


WORLDS = {"editorial": w_editorial, "spotlight": w_spotlight, "colorblock": w_colorblock,
          "split": w_split, "paper": w_paper}

# --- author photo watermark ----------------------------------------------
# Drop a photo in assets/quote_authors/<slug>.<ext>; we rembg it once (cached in
# _cutout/) and place the cut-out author on their quote slide, like a signature.
_AUTH_DIR = os.path.join(L.BASE, "assets", "quote_authors")
_AUTH_CACHE = os.path.join(_AUTH_DIR, "_cutout")
# Per-world placement of the author cut-out (CSS on an absolute <img>), chosen so
# it lands in each layout's empty zone and clears the text/CTA.
AUTHOR_POS = {
    "spotlight":  "right:70px;bottom:0;height:452px;",
    "colorblock": "right:64px;bottom:0;height:470px;",
    "split":      "left:44px;bottom:0;height:486px;",
    "paper":      "right:70px;bottom:56px;height:360px;",
    "editorial":  "right:70px;bottom:0;height:430px;",
}


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


def _author_overlay(author, world):
    src = author_cutout(author)
    if not src:
        return ""
    pos = AUTHOR_POS.get(world, "right:70px;bottom:0;height:430px;")
    return (f"<img src='{src}' style='position:absolute;{pos}"
            f"filter:drop-shadow(0 16px 26px rgba(0,0,0,.45));pointer-events:none;'>")

# Only q001-q005 in the bank carry a "cta"; the rest (exposed once quotes rotate
# weekly) don't, so fall back to an on-brand default rather than KeyError.
_DEFAULT_CTA = "Find your internship at internwise.co.uk"


def render_quote(q, world, out_dir, filename="slide_1.png"):
    overlay = _author_overlay(q.get("author", ""), world)
    # When the author cut-out occupies a bottom corner, use the SHORT url CTA so
    # the (otherwise long) CTA line clears the photo.
    cta = "internwise.co.uk" if overlay else (q.get("cta") or _DEFAULT_CTA)
    q = {**q, "cta": cta}
    inner = WORLDS[world](q) + overlay
    return L.render(out_dir, filename, inner)


if __name__ == "__main__":
    qs = L.load("quotes_bank.json")["quotes"]
    for i, (world, q) in enumerate(zip(WORLDS.keys(), qs)):
        render_quote(q, world, os.path.join(L.OUTROOT, "week14", "_qtest", world))
