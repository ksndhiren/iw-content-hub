"""Week 11 shared base - lean, photo-free, data-driven weekly graphics.
Distinct look per post via a `design` dict (bg + accent + kicker + motif)."""
import os, base64
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BR   = os.path.join(BASE, "branding", "PNG")
FN   = os.path.join(BASE, "assets", "fonts")

DEEP="#264D7E"; NAVY="#162d4a"; AMBER="#FFB120"; CORAL="#FF6B6B"; PURPLE="#7B5CE6"
MINT="#7FDBB6"; CREAM="#FAF5EC"; PINK="#FF3D8A"; LIME="#D4FF3D"; INK="#141018"

def _b64(p):
    return base64.b64encode(open(p,"rb").read()).decode() if os.path.exists(p) else ""
LOGO_W = _b64(os.path.join(BR,"IW.com_Horizontal_white logo.png"))
LOGO_B = _b64(os.path.join(BR,"IW.com_Horizontal_Blue Logo.png")) or _b64(os.path.join(BR,"IW.com_Horizontal_blue logo.png"))

def fonts():
    css=""
    for fam,vv in {"Inter":[("Inter-Bold.ttf",700),("Inter-SemiBold.ttf",600),("Inter-Regular.ttf",400)],
                   "DM Sans":[("DMSans-Bold.ttf",700),("DMSans-Medium.ttf",500),("DMSans-Regular.ttf",400)]}.items():
        for fn,w in vv:
            b=_b64(os.path.join(FN,fn))
            if b: css+=f"@font-face{{font-family:'{fam}';src:url(data:font/truetype;base64,{b});font-weight:{w};}}"
    return css

def render(body, path, bg):
    html=(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{fonts()}"
          "*{margin:0;padding:0;box-sizing:border-box;}"
          f"body{{width:1080px;height:1080px;overflow:hidden;}}"
          f".c{{width:1080px;height:1080px;position:relative;padding:64px;background:{bg};display:flex;flex-direction:column;}}"
          f"</style></head><body><div class='c'>{body}</div></body></html>")
    with sync_playwright() as p:
        br=p.chromium.launch(); pg=br.new_page(viewport={"width":1080,"height":1080},device_scale_factor=2)
        pg.set_content(html,wait_until="networkidle"); pg.screenshot(path=path,type="png"); br.close()
    print("  ok",os.path.basename(os.path.dirname(path)),os.path.basename(path))

def logo(d):
    src=LOGO_W if d["dark"] else LOGO_B
    return f"<img src='data:image/png;base64,{src}' style='height:52px;'>"

def pill(text,d):
    return (f"<span style=\"display:inline-flex;align-items:center;gap:10px;background:{d['acc']};color:{d['on']};"
            f"padding:11px 22px;border-radius:40px;font-family:Inter;font-weight:700;font-size:19px;letter-spacing:2px;"
            f"text-transform:uppercase;\">{text}</span>")

def head(html,size,color):
    return (f"<div style=\"font-family:Inter;font-weight:700;font-size:{size}px;line-height:1.0;color:{color};"
            f"letter-spacing:-2px;word-break:keep-all;hyphens:none;\">{html}</div>")

# ---- slide builders (design dict: dark,bg,acc,on,txt,sub,kick) ----
def hdr(d, right):
    return (f"<div style='display:flex;justify-content:space-between;align-items:center;flex-shrink:0;'>"
            f"{logo(d)}{pill(right,d)}</div>")

def hook(d, kick, head_html, sub):
    return d["bg"], (hdr(d,d["kick"])+
        f"<div style='flex:1;display:flex;flex-direction:column;justify-content:center;'>"
        f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:20px;color:{d['acc']};letter-spacing:3px;text-transform:uppercase;margin-bottom:20px;\">{kick}</div>"
        f"{head(head_html,72,d['txt'])}"
        f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:29px;color:{d['sub']};margin-top:26px;line-height:1.4;max-width:820px;\">{sub}</div>"
        f"</div>"
        f"<div style=\"font-family:'DM Sans';font-weight:600;font-size:20px;color:{d['acc']};text-align:right;\">Swipe &rarr;</div>")

def stats(d, title, rows, source):
    cards=""
    for n,l in rows:
        cards+=(f"<div style='flex:1;background:{d['card']};border:1.5px solid {d['acc']}55;border-radius:18px;padding:30px 24px;'>"
                f"<div style=\"font-family:Inter;font-weight:700;font-size:60px;color:{d['acc']};letter-spacing:-2px;line-height:1;\">{n}</div>"
                f"<div style=\"font-family:'DM Sans';font-weight:500;font-size:23px;color:{d['txt']};margin-top:16px;line-height:1.35;\">{l}</div></div>")
    return d["bg"], (hdr(d,"By the numbers")+
        f"<div style='margin-top:40px;'>{head(title,52,d['txt'])}</div>"
        f"<div style='flex:1;display:flex;gap:20px;align-items:center;'>{cards}</div>"
        f"<div style=\"font-family:'DM Sans';font-size:18px;color:{d['sub']};text-align:right;\">{source}</div>")

def tip(d, n, title, points):
    rows=""
    for pt in points:
        rows+=(f"<div style='display:flex;gap:16px;align-items:flex-start;margin-bottom:18px;'>"
               f"<span style=\"color:{d['acc']};font-family:Inter;font-weight:700;font-size:26px;line-height:1;\">&#9679;</span>"
               f"<span style=\"font-family:'DM Sans';font-weight:500;font-size:28px;color:{d['txt']};line-height:1.38;\">{pt}</span></div>")
    return d["bg"], (
        f"<div style='display:flex;align-items:center;gap:18px;flex-shrink:0;'>"
        f"<div style='width:58px;height:58px;border-radius:50%;background:{d['acc']};color:{d['on']};display:flex;align-items:center;justify-content:center;font-family:Inter;font-weight:700;font-size:26px;'>{n}</div>"
        f"<div style=\"font-family:'DM Sans';font-weight:700;font-size:19px;color:{d['sub']};letter-spacing:3px;text-transform:uppercase;\">Play {n}</div></div>"
        f"<div style='margin-top:26px;'>{head(title,54,d['txt'])}</div>"
        f"<div style='flex:1;display:flex;flex-direction:column;justify-content:center;'>{rows}</div>")

def cta(d, headline, checks):
    rows=""
    for c in checks:
        rows+=(f"<div style='display:flex;gap:14px;align-items:center;padding:9px 0;'>"
               f"<span style=\"color:{d['acc']};font-size:24px;\">&#10003;</span>"
               f"<span style=\"font-family:'DM Sans';font-weight:600;font-size:26px;color:{d['txt']};\">{c}</span></div>")
    return d["bg"], (hdr(d,"Your move")+
        f"<div style='flex:1;display:flex;flex-direction:column;justify-content:center;'>"
        f"<div style='margin-bottom:26px;'>{head(headline,58,d['txt'])}</div>{rows}"
        f"<div style=\"margin-top:30px;display:inline-flex;align-self:flex-start;align-items:center;gap:12px;background:{d['acc']};color:{d['on']};padding:18px 34px;border-radius:50px;font-family:Inter;font-weight:700;font-size:25px;\">Find roles at internwise.co.uk &rarr;</div>"
        f"</div>")
