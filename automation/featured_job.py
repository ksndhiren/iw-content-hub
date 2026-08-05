"""
Internwise - Featured Job post generator (portrait 1080x1350, 4:5 feed format).
One post per featured job listing. Trendy, on-brand, keeps ALL job details, and
pairs a Pexels cutout of a relevant person with role-specific 3D clipart motifs.

Reference brief: same family as the previous purple "FEATURED JOB" template, but
fresh, creative, and per-role. NOT an exact copy.

Usage: configure JOBS dict, call generate(job_key, out_dir).
Mobile-safe type: role title 60px+, body 30px+, labels 20px+.
"""
import os, base64, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# dedup/pexels are only needed for the photo/character sample variants. The automated
# featured-job pipeline uses the graphic-cluster mode, which needs none of it, so keep
# the import optional so this module runs standalone (e.g. in a cloud routine).
try:
    from dedup import get_used_hashes, register_used_hashes, register_design, get_cutout_unique
except Exception:
    def get_used_hashes(*a, **k): return set()
    def register_used_hashes(*a, **k): pass
    def register_design(*a, **k): pass
    def get_cutout_unique(*a, **k): raise RuntimeError("pexels/dedup unavailable in this environment")
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Asset dirs are overridable so this module runs both in the tools tree and when
# vendored into another repo (e.g. the content-hub automation folder / a cloud routine).
BRANDING_DIR = os.environ.get("IW_BRANDING_DIR") or os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.environ.get("IW_FONTS_DIR")    or os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; PURPLE = "#7B5CE6"; MINT = "#7FDBB6"
OFF_WHITE = "#FAF5EC"; HOT_PINK = "#FF3D8A"; LIME = "#D4FF3D"

W, H = 1080, 1350

LOGO_W = LOGO_C = None
def _load_logos():
    global LOGO_W, LOGO_C
    if LOGO_W is None:
        LOGO_W = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""
        LOGO_C = _b64(os.path.join(BRANDING_DIR, "PNG", "Internwise.Com-Horizontal logo.png")) or ""

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

def _src(path):
    b = _b64(path)
    return f"data:image/png;base64,{b}" if b else ""

def _fonts():
    variants = {
        "Inter":   [("Inter-Bold.ttf",700),("Inter-SemiBold.ttf",600),("Inter-Regular.ttf",400)],
        "DM Sans": [("DMSans-Bold.ttf",700),("DMSans-Medium.ttf",500),("DMSans-Regular.ttf",400)],
    }
    css = ""
    for family, vv in variants.items():
        for fn, w in vv:
            b = _b64(os.path.join(FONTS_DIR, fn))
            if b: css += f"@font-face{{font-family:'{family}';src:url(data:font/truetype;base64,{b}) format('truetype');font-weight:{w};}}"
    return css

def _render(html, path):
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width":W,"height":H}, device_scale_factor=2)
        pg.set_content(html, wait_until="networkidle")
        pg.screenshot(path=path, type="png")
        br.close()
    print(f"  ok {path}")

GRAIN = ".grain{position:absolute;inset:0;z-index:2;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,0.04) 1px,transparent 1px);background-size:3px 3px;}"

# ── role-specific 3D clipart motif packs (inline SVG, glossy 3D-ish) ─────────
def _svg_swatches(accent):
    # stacked colour swatch chips (design/brand roles)
    chips = ""
    cols = ["#FF6B6B", "#FFB120", "#7FDBB6", "#5AA9E8", "#7B5CE6"]
    for i, c in enumerate(cols):
        chips += (f'<div style="width:96px;height:120px;border-radius:14px;background:{c};'
                  f'box-shadow:0 14px 26px rgba(0,0,0,0.32),inset 0 3px 5px rgba(255,255,255,0.4);'
                  f'transform:rotate({-16+i*8}deg) translateY({(i%2)*-18}px);margin-left:{-34 if i else 0}px;'
                  f'border:3px solid rgba(255,255,255,0.5);"></div>')
    pen = f"""<svg width="150" height="150" viewBox="0 0 150 150" style="position:absolute;top:-70px;right:-30px;transform:rotate(24deg);filter:drop-shadow(0 12px 20px rgba(0,0,0,0.35));">
      <rect x="64" y="10" width="26" height="86" rx="10" fill="#5AA9E8"/>
      <path d="M64 96 L90 96 L82 128 L77 140 L72 128 Z" fill="#EDEDED"/>
      <path d="M77 128 L77 140 L72 128 Z" fill="#333"/>
      <rect x="70" y="104" width="14" height="20" fill="#333" opacity="0.25"/>
    </svg>"""
    return f'<div style="position:relative;display:flex;align-items:flex-end;">{chips}{pen}</div>'

def _sparkles(color, count=3):
    s = ""
    spots = [("6%","20%",46,0),("88%","10%",34,20),("80%","64%",40,-12)]
    for i in range(min(count,len(spots))):
        top,left,size,rot = spots[i]
        s += (f'<div style="position:absolute;top:{top};left:{left};transform:rotate({rot}deg);z-index:6;">'
              f'<svg width="{size}" height="{size}" viewBox="0 0 40 40"><path d="M20 2 L24 16 L38 20 L24 24 L20 38 L16 24 L2 20 L16 16 Z" fill="{color}"/></svg></div>')
    return s

# ── 3D brand-design object cluster (glossy, no human) ───────────────────────
def _cluster_branddesign(accent):
    """A hero cluster of 3D design objects: colour wheel, glossy pen, type card,
    swatch fan, cursor, sparkles. All CSS/SVG, glossy soft-shadow 3D look."""
    wheel = ("conic-gradient(#FF6B6B 0deg 60deg,#FFB120 60deg 120deg,"
             "#7FDBB6 120deg 180deg,#5AA9E8 180deg 240deg,#7B5CE6 240deg 300deg,"
             "#FF3D8A 300deg 360deg)")
    star = lambda s,c: (f'<svg width="{s}" height="{s}" viewBox="0 0 40 40">'
                        f'<path d="M20 2 L24 16 L38 20 L24 24 L20 38 L16 24 L2 20 L16 16 Z" fill="{c}"/></svg>')
    return f"""<div style="position:relative;width:600px;height:780px;">
  <!-- podium shadow -->
  <div style="position:absolute;bottom:44px;left:150px;width:320px;height:56px;border-radius:50%;
               background:radial-gradient(rgba(0,0,0,0.34),transparent 70%);"></div>

  <!-- colour wheel -->
  <div style="position:absolute;top:196px;left:196px;width:250px;height:250px;border-radius:50%;
               background:{wheel};transform:rotate(-12deg);
               box-shadow:0 26px 44px rgba(0,0,0,0.4),inset 0 4px 8px rgba(255,255,255,0.35);">
    <div style="position:absolute;inset:78px;border-radius:50%;background:#FAF5EC;
                 box-shadow:inset 0 3px 6px rgba(0,0,0,0.25);"></div>
  </div>

  <!-- big glossy pen (diagonal) -->
  <div style="position:absolute;top:150px;left:150px;transform:rotate(-40deg);transform-origin:center;">
    <div style="position:relative;width:340px;height:74px;">
      <div style="position:absolute;left:0;top:0;width:270px;height:74px;border-radius:38px;
                   background:linear-gradient(180deg,#7CA0F7 0%,#3B62D6 100%);
                   box-shadow:0 18px 30px rgba(30,50,120,0.45),inset 0 4px 6px rgba(255,255,255,0.5),
                   inset 0 -6px 10px rgba(0,0,0,0.25);"></div>
      <div style="position:absolute;left:20px;top:14px;width:230px;height:14px;border-radius:8px;
                   background:rgba(255,255,255,0.30);"></div>
      <!-- nib -->
      <div style="position:absolute;left:258px;top:5px;width:0;height:0;
                   border-top:32px solid transparent;border-bottom:32px solid transparent;
                   border-left:76px solid #E9EDF3;filter:drop-shadow(0 8px 10px rgba(0,0,0,0.3));"></div>
      <div style="position:absolute;left:318px;top:29px;width:0;height:0;
                   border-top:8px solid transparent;border-bottom:8px solid transparent;
                   border-left:18px solid #333A55;"></div>
      <div style="position:absolute;left:252px;top:24px;width:10px;height:26px;border-radius:4px;
                   background:rgba(51,58,85,0.35);"></div>
    </div>
  </div>

  <!-- type "Aa" card -->
  <div style="position:absolute;top:60px;left:30px;width:158px;height:190px;border-radius:24px;
               background:linear-gradient(160deg,#FFFFFF,#F0F0F4);transform:rotate(-11deg);
               box-shadow:0 22px 38px rgba(0,0,0,0.34),inset 0 3px 5px rgba(255,255,255,0.9);
               display:flex;align-items:center;justify-content:center;">
    <div style="font-family:Inter;font-weight:700;font-size:92px;color:{accent};letter-spacing:-4px;">Aa</div>
  </div>

  <!-- swatch fan (bottom) -->
  <div style="position:absolute;bottom:96px;left:110px;display:flex;align-items:flex-end;">
    {''.join(f'<div style="width:78px;height:100px;border-radius:12px;background:{c};margin-left:{-26 if i else 0}px;transform:rotate({-14+i*7}deg) translateY({(i%2)*-14}px);box-shadow:0 12px 22px rgba(0,0,0,0.3),inset 0 3px 4px rgba(255,255,255,0.45);border:3px solid rgba(255,255,255,0.55);"></div>' for i,c in enumerate(["#FF6B6B","#FFB120","#7FDBB6","#5AA9E8","#7B5CE6"]))}
  </div>

  <!-- pen-tool bezier -->
  <svg width="230" height="150" viewBox="0 0 230 150" style="position:absolute;top:430px;left:330px;filter:drop-shadow(0 8px 12px rgba(0,0,0,0.25));">
    <path d="M20 120 Q60 20 130 60 T210 30" stroke="#FAF5EC" stroke-width="4" fill="none" stroke-dasharray="1 0"/>
    <line x1="130" y1="60" x2="90" y2="30" stroke="{accent}" stroke-width="3"/>
    <line x1="130" y1="60" x2="170" y2="90" stroke="{accent}" stroke-width="3"/>
    <circle cx="90" cy="30" r="9" fill="{accent}"/><circle cx="170" cy="90" r="9" fill="{accent}"/>
    <rect x="12" y="112" width="16" height="16" rx="3" fill="#fff" stroke="{accent}" stroke-width="3"/>
    <rect x="202" y="22" width="16" height="16" rx="3" fill="#fff" stroke="{accent}" stroke-width="3"/>
  </svg>

  <!-- cursor -->
  <svg width="46" height="54" viewBox="0 0 46 54" style="position:absolute;top:400px;left:250px;filter:drop-shadow(0 6px 8px rgba(0,0,0,0.3));">
    <path d="M4 2 L4 44 L15 33 L23 50 L31 46 L23 30 L38 30 Z" fill="#fff" stroke="#2A2E45" stroke-width="2.5" stroke-linejoin="round"/>
  </svg>

  <!-- sparkles + dots -->
  <div style="position:absolute;top:150px;left:470px;">{star(48, LIME)}</div>
  <div style="position:absolute;top:470px;left:180px;transform:rotate(18deg);">{star(32, AMBER)}</div>
  <div style="position:absolute;top:250px;left:14px;width:22px;height:22px;border-radius:50%;background:{CORAL};box-shadow:0 4px 8px rgba(0,0,0,0.25);"></div>
  <div style="position:absolute;top:540px;left:500px;width:18px;height:18px;border-radius:50%;background:{MINT};box-shadow:0 4px 8px rgba(0,0,0,0.25);"></div>
</div>"""


def _star(s, c):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 40 40">'
            f'<path d="M20 2 L24 16 L38 20 L24 24 L20 38 L16 24 L2 20 L16 16 Z" fill="{c}"/></svg>')

GLOSS = ("box-shadow:0 18px 30px rgba(0,0,0,0.35),inset 0 3px 5px rgba(255,255,255,0.4),"
         "inset 0 -6px 10px rgba(0,0,0,0.2);")


# ── Surveying / construction 3D cluster ─────────────────────────────────────
def _cluster_surveying(accent):
    window = f'<div style="width:26px;height:30px;border-radius:5px;background:{accent};opacity:0.85;"></div>'
    floors = ""
    for i in range(4):
        w = 170 - i * 8
        floors += (f'<div style="width:{w}px;height:76px;margin:0 auto;border-radius:10px;'
                   f'background:linear-gradient(180deg,#EDE7DA,#CFC6B4);{GLOSS}display:flex;'
                   f'align-items:center;justify-content:space-around;padding:0 14px;">'
                   f'{window}{window}{window}</div>')
    return f"""<div style="position:relative;width:600px;height:780px;">
  <div style="position:absolute;bottom:44px;left:150px;width:320px;height:56px;border-radius:50%;
               background:radial-gradient(rgba(0,0,0,0.34),transparent 70%);"></div>

  <!-- 3D building tower -->
  <div style="position:absolute;bottom:96px;left:300px;width:170px;">
    {floors}
    <div style="width:186px;height:22px;margin:6px auto 0;border-radius:8px;background:#B7AE9B;{GLOSS}"></div>
  </div>

  <!-- hard hat hero -->
  <div style="position:absolute;top:250px;left:120px;transform:rotate(-6deg);">
    <div style="width:240px;height:56px;border-radius:120px/56px;background:linear-gradient(180deg,{accent},#C98A15);{GLOSS}"></div>
    <div style="position:absolute;top:-92px;left:38px;width:164px;height:110px;border-radius:82px 82px 0 0;
                 background:linear-gradient(180deg,#FFD778,{accent});{GLOSS}"></div>
    <div style="position:absolute;top:-92px;left:110px;width:20px;height:96px;border-radius:8px;
                 background:rgba(0,0,0,0.12);"></div>
  </div>

  <!-- rolled blueprint -->
  <div style="position:absolute;top:120px;left:40px;transform:rotate(-16deg);">
    <div style="width:180px;height:64px;border-radius:14px;background:linear-gradient(180deg,#5AA9E8,#2E6BB0);{GLOSS}
                 background-image:linear-gradient(90deg,rgba(255,255,255,0.25) 1px,transparent 1px),linear-gradient(rgba(255,255,255,0.25) 1px,transparent 1px);background-size:18px 18px;"></div>
    <div style="position:absolute;top:0;left:-10px;width:24px;height:64px;border-radius:12px;background:#EDE7DA;{GLOSS}"></div>
    <div style="position:absolute;top:0;right:-10px;width:24px;height:64px;border-radius:12px;background:#EDE7DA;{GLOSS}"></div>
  </div>

  <!-- ruler -->
  <svg width="300" height="80" viewBox="0 0 300 80" style="position:absolute;top:430px;left:300px;transform:rotate(24deg);filter:drop-shadow(0 12px 18px rgba(0,0,0,0.3));">
    <rect x="0" y="26" width="280" height="34" rx="8" fill="#FAF5EC"/>
    {''.join(f'<line x1="{20+i*26}" y1="26" x2="{20+i*26}" y2="{44 if i%2 else 52}" stroke="{accent}" stroke-width="3"/>' for i in range(10))}
  </svg>

  <!-- magnifier -->
  <svg width="120" height="120" viewBox="0 0 120 120" style="position:absolute;top:400px;left:210px;filter:drop-shadow(0 10px 14px rgba(0,0,0,0.3));">
    <circle cx="46" cy="46" r="34" fill="rgba(255,255,255,0.9)" stroke="#2A3550" stroke-width="8"/>
    <rect x="70" y="70" width="42" height="16" rx="8" transform="rotate(45 70 70)" fill="#2A3550"/>
  </svg>

  <div style="position:absolute;top:150px;left:470px;">{_star(48, LIME)}</div>
  <div style="position:absolute;top:470px;left:180px;transform:rotate(18deg);">{_star(30, '#FFD778')}</div>
  <div style="position:absolute;top:250px;left:14px;width:22px;height:22px;border-radius:50%;background:{CORAL};box-shadow:0 4px 8px rgba(0,0,0,0.25);"></div>
</div>"""


# ── Marketing 3D cluster ────────────────────────────────────────────────────
def _cluster_marketing(accent):
    return f"""<div style="position:relative;width:600px;height:780px;">
  <div style="position:absolute;bottom:44px;left:150px;width:320px;height:56px;border-radius:50%;
               background:radial-gradient(rgba(0,0,0,0.34),transparent 70%);"></div>

  <!-- megaphone hero -->
  <div style="position:absolute;top:220px;left:150px;transform:rotate(-18deg);">
    <div style="width:150px;height:120px;background:linear-gradient(160deg,#FFD778,{accent});{GLOSS}
                 clip-path:polygon(0 22%,60% 0,60% 100%,0 78%);"></div>
    <div style="position:absolute;top:22px;left:88px;width:70px;height:76px;border-radius:14px;
                 background:linear-gradient(180deg,#FF8A7A,{CORAL});{GLOSS}"></div>
    <div style="position:absolute;top:52px;left:8px;width:22px;height:44px;border-radius:8px;background:#333A55;transform:rotate(-8deg);"></div>
    <!-- sound arcs -->
    <svg width="120" height="140" viewBox="0 0 120 140" style="position:absolute;top:-6px;left:150px;">
      <path d="M10 40 Q40 70 10 100" stroke="{LIME}" stroke-width="7" fill="none" stroke-linecap="round"/>
      <path d="M44 24 Q92 70 44 116" stroke="{LIME}" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.7"/>
    </svg>
  </div>

  <!-- bar-chart card -->
  <div style="position:absolute;bottom:120px;left:290px;width:200px;height:180px;border-radius:22px;
               background:linear-gradient(160deg,#FFFFFF,#F0F0F4);{GLOSS}display:flex;align-items:flex-end;
               gap:16px;padding:24px;">
    <div style="width:36px;height:56px;border-radius:8px 8px 0 0;background:#7FDBB6;"></div>
    <div style="width:36px;height:92px;border-radius:8px 8px 0 0;background:#5AA9E8;"></div>
    <div style="width:36px;height:130px;border-radius:8px 8px 0 0;background:{accent};"></div>
    <svg width="150" height="120" viewBox="0 0 150 120" style="position:absolute;top:12px;left:24px;">
      <path d="M10 100 L55 60 L90 78 L138 20" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M120 20 L138 20 L138 38" stroke="{CORAL}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>

  <!-- heart bubble -->
  <div style="position:absolute;top:120px;left:400px;width:110px;height:110px;border-radius:28px 28px 28px 6px;
               background:linear-gradient(160deg,#FF8A7A,{CORAL});{GLOSS}display:flex;align-items:center;justify-content:center;">
    <svg width="56" height="52" viewBox="0 0 56 52"><path d="M28 48 C6 32 4 16 15 12 C23 9 28 17 28 21 C28 17 33 9 41 12 C52 16 50 32 28 48 Z" fill="#fff"/></svg>
  </div>

  <!-- target -->
  <svg width="120" height="120" viewBox="0 0 120 120" style="position:absolute;top:430px;left:250px;filter:drop-shadow(0 12px 16px rgba(0,0,0,0.3));">
    <circle cx="60" cy="60" r="52" fill="#FAF5EC"/><circle cx="60" cy="60" r="36" fill="none" stroke="{accent}" stroke-width="8"/>
    <circle cx="60" cy="60" r="16" fill="{CORAL}"/>
  </svg>

  <div style="position:absolute;top:150px;left:120px;">{_star(46, LIME)}</div>
  <div style="position:absolute;top:470px;left:470px;transform:rotate(18deg);">{_star(32, '#FFD778')}</div>
  <div style="position:absolute;top:300px;left:500px;width:22px;height:22px;border-radius:50%;background:{MINT};box-shadow:0 4px 8px rgba(0,0,0,0.25);"></div>
</div>"""


# ── Social / content 3D cluster ─────────────────────────────────────────────
def _cluster_social(accent):
    return f"""<div style="position:relative;width:600px;height:780px;">
  <div style="position:absolute;bottom:44px;left:150px;width:320px;height:56px;border-radius:50%;
               background:radial-gradient(rgba(0,0,0,0.34),transparent 70%);"></div>

  <!-- camera hero -->
  <div style="position:absolute;top:250px;left:150px;transform:rotate(-6deg);">
    <div style="position:absolute;top:-26px;left:44px;width:70px;height:34px;border-radius:10px 10px 0 0;
                 background:linear-gradient(180deg,#5C6480,#3A4160);"></div>
    <div style="width:250px;height:170px;border-radius:26px;background:linear-gradient(160deg,#4A5170,#2A2F4A);{GLOSS}"></div>
    <div style="position:absolute;top:34px;left:74px;width:104px;height:104px;border-radius:50%;
                 background:radial-gradient(circle at 38% 34%,#8FC7F5,#2E6BB0);box-shadow:inset 0 4px 8px rgba(255,255,255,0.4),inset 0 -8px 12px rgba(0,0,0,0.4);"></div>
    <div style="position:absolute;top:58px;left:98px;width:56px;height:56px;border-radius:50%;background:#12203A;"></div>
    <div style="position:absolute;top:66px;left:106px;width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,0.5);"></div>
    <div style="position:absolute;top:16px;left:200px;width:30px;height:22px;border-radius:6px;background:{accent};"></div>
  </div>

  <!-- play button -->
  <div style="position:absolute;top:130px;left:400px;width:120px;height:120px;border-radius:50%;
               background:linear-gradient(160deg,#FF8A7A,{CORAL});{GLOSS}display:flex;align-items:center;justify-content:center;">
    <div style="width:0;height:0;border-top:26px solid transparent;border-bottom:26px solid transparent;
                 border-left:42px solid #fff;margin-left:10px;"></div>
  </div>

  <!-- chat bubble w/ heart -->
  <div style="position:absolute;top:120px;left:40px;width:140px;height:104px;border-radius:26px 26px 6px 26px;
               background:linear-gradient(160deg,#FFFFFF,#EDEFF4);{GLOSS}display:flex;align-items:center;justify-content:center;gap:10px;">
    <svg width="40" height="38" viewBox="0 0 40 38"><path d="M20 34 C5 24 3 12 11 9 C17 6.5 20 12 20 15 C20 12 23 6.5 29 9 C37 12 35 24 20 34 Z" fill="{CORAL}"/></svg>
    <div style="width:14px;height:14px;border-radius:50%;background:{accent};"></div>
  </div>

  <!-- little house (home staging) -->
  <svg width="130" height="120" viewBox="0 0 130 120" style="position:absolute;top:440px;left:290px;filter:drop-shadow(0 12px 16px rgba(0,0,0,0.3));">
    <path d="M20 54 L65 18 L110 54 L110 104 L20 104 Z" fill="#FAF5EC"/>
    <path d="M10 58 L65 14 L120 58" stroke="{accent}" stroke-width="9" fill="none" stroke-linejoin="round"/>
    <rect x="52" y="70" width="26" height="34" rx="3" fill="{CORAL}"/>
  </svg>

  <div style="position:absolute;top:160px;left:250px;">{_star(46, LIME)}</div>
  <div style="position:absolute;top:470px;left:470px;transform:rotate(18deg);">{_star(32, '#FFD778')}</div>
  <div style="position:absolute;top:520px;left:200px;width:22px;height:22px;border-radius:50%;background:{MINT};box-shadow:0 4px 8px rgba(0,0,0,0.25);"></div>
</div>"""


# ── Generic 3D cluster (fallback for sectors without a bespoke one) ──────────
def _cluster_generic(accent):
    return f"""<div style="position:relative;width:600px;height:780px;">
  <div style="position:absolute;bottom:44px;left:150px;width:320px;height:56px;border-radius:50%;
               background:radial-gradient(rgba(0,0,0,0.34),transparent 70%);"></div>

  <!-- briefcase -->
  <div style="position:absolute;top:250px;left:170px;transform:rotate(-6deg);">
    <div style="width:250px;height:170px;border-radius:26px;background:linear-gradient(160deg,#FFD778,{accent});{GLOSS}"></div>
    <div style="position:absolute;top:-30px;left:80px;width:90px;height:44px;border-radius:12px 12px 0 0;
                 border:12px solid {accent};border-bottom:none;background:transparent;"></div>
    <div style="position:absolute;top:56px;left:0;width:250px;height:16px;background:rgba(0,0,0,0.18);"></div>
    <div style="position:absolute;top:62px;left:104px;width:42px;height:30px;border-radius:6px;background:#FAF5EC;"></div>
  </div>

  <!-- rising chart card -->
  <div style="position:absolute;bottom:120px;left:300px;width:190px;height:170px;border-radius:22px;
               background:linear-gradient(160deg,#FFFFFF,#F0F0F4);{GLOSS}display:flex;align-items:flex-end;
               gap:14px;padding:22px;">
    <div style="width:32px;height:52px;border-radius:8px 8px 0 0;background:#7FDBB6;"></div>
    <div style="width:32px;height:88px;border-radius:8px 8px 0 0;background:#5AA9E8;"></div>
    <div style="width:32px;height:122px;border-radius:8px 8px 0 0;background:{accent};"></div>
  </div>

  <!-- star badge -->
  <div style="position:absolute;top:130px;left:410px;width:110px;height:110px;border-radius:28px;
               background:linear-gradient(160deg,#FF8A7A,{CORAL});{GLOSS}display:flex;align-items:center;justify-content:center;">
    {_star(56, '#fff')}
  </div>

  <!-- check bubble -->
  <svg width="120" height="120" viewBox="0 0 120 120" style="position:absolute;top:430px;left:250px;filter:drop-shadow(0 12px 16px rgba(0,0,0,0.3));">
    <circle cx="60" cy="60" r="50" fill="#FAF5EC"/>
    <path d="M40 60 l14 14 l28 -30" stroke="{accent}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>

  <div style="position:absolute;top:150px;left:120px;">{_star(46, LIME)}</div>
  <div style="position:absolute;top:470px;left:470px;transform:rotate(18deg);">{_star(32, '#FFD778')}</div>
  <div style="position:absolute;top:300px;left:500px;width:22px;height:22px;border-radius:50%;background:{MINT};box-shadow:0 4px 8px rgba(0,0,0,0.25);"></div>
</div>"""


# ── Sector -> visual style mapping + config builder for scraped jobs ─────────
# Each style: (accent, accent_dark, bg1, bg2, spark, cluster_fn, hook)
# One distinct colour scheme per sector so featured posts read as varied.
SECTOR_STYLES = {
    "design":    (PURPLE,   "#5B3FC4", "#2B1E63", "#4A2F9E", LIME, _cluster_branddesign,
                  "Love turning ideas into visuals that stop the scroll? Build your portfolio with a real brand."),
    "tech":      ("#3FD0E0", "#2AA9B8", "#141F4A", "#2E3E9E", LIME, _cluster_generic,
                  "Love building things that work? Ship real features with an engineering team."),
    "social":    ("#5AA9E8", "#2E6BB0", "#123A66", "#1E6FAE", LIME, _cluster_social,
                  "Love creating scroll-stopping content? Shoot, edit and post for a real brand."),
    "property":  (AMBER,    "#D18E14", "#0E4433", "#1B7B58", LIME, _cluster_surveying,
                  "Curious how property really works? Get hands-on with real projects across London."),
    "finance":   ("#FFC24A", "#D18E14", "#14233F", "#2A4470", LIME, _cluster_generic,
                  "Good with numbers and detail? Get real experience across accounts and finance."),
    "pr":        ("#2FBFB0", "#1E8A80", "#0C3B38", "#17706A", LIME, _cluster_marketing,
                  "Love telling stories that land? Own the press, profile and publicity for a growing brand."),
    "media":     ("#FF5CA8", "#D63D88", "#5A1440", "#A32473", LIME, _cluster_social,
                  "Obsessed with content and culture? Help shape what a brand puts out into the world."),
    "sales":     ("#FF9F45", "#E5771E", "#5A2A12", "#A85A1E", LIME, _cluster_marketing,
                  "A natural at winning people over? Learn to pitch, close and grow real revenue."),
    "marketing": (CORAL,    "#D2415C", "#7E2038", "#C43F5C", LIME, _cluster_marketing,
                  "Ready to run real campaigns? Own content, socials and growth for a busy team."),
    "generic":   ("#5FC7A6", "#3FA985", "#26343F", "#43586A", LIME, _cluster_generic,
                  "Kickstart your career with a hands-on internship at a growing UK company."),
}

# keyword -> style key (first match wins; ordered by specificity). Maps the fixed
# Internwise sector taxonomy to a distinct colour per sector.
_SECTOR_KEYWORDS = [
    ("tech",     ["information technology", "web development", "software"]),
    ("design",   ["graphic design", "web design", "brand design"]),
    ("social",   ["photography", "videography", "home staging"]),
    ("property", ["surveying", "real estate", "property management", "construction", "architecture"]),
    ("finance",  ["accountancy", "accounting", "financial services", "banking"]),
    ("pr",       ["public relations", "(pr)", "communications"]),
    ("sales",    ["sales"]),
    ("marketing",["marketing", "advertising"]),
    ("media",    ["new media", "journalism", "broadcast"]),  # only pure-media roles
]

def _pick_style(fields_text):
    t = (fields_text or "").lower()
    for key, kws in _SECTOR_KEYWORDS:
        if any(kw in t for kw in kws):
            return key
    return "generic"

def _sanitize(s):
    """Strip em/en dashes (brand rule) and collapse whitespace."""
    if not s: return ""
    s = s.replace("—", "-").replace("–", "-").replace("&", "&amp;")
    return re.sub(r"\s+", " ", s).strip()

def strip_year(s):
    """Reduce a scraped listing title to just the job role. Drops:
      - a trailing employer mention: '... at M&K Accountants'
      - a trailing parenthetical: a year '(2026)' or type '(Part-Time)'/'(Full Time)'.
    Keeps the role itself intact. Rule applies to all future graphics + captions."""
    if not s: return ""
    # strip a trailing " at <employer>" (case-insensitive)
    s = re.sub(r"\s+\bat\b\s+.+$", "", s, flags=re.I)
    # strip a trailing year or employment-type in parentheses
    s = re.sub(r"\s*\(\s*(?:(?:19|20)\d{2}|(?:part|full)[\s-]?time)\s*\)\s*$",
               "", s, flags=re.I)
    return s.strip()

def _wrap_title(title):
    """Balance the title into up to 3 lines; return (html_with_br, font_size)."""
    words = title.split()
    if not words:
        return "", 74
    # greedily pack into lines of <= ~14 visual chars, max 3 lines
    lines, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) > 15 and cur:
            lines.append(cur); cur = w
        else:
            cur = cand
    if cur: lines.append(cur)
    if len(lines) > 3:
        # re-pack into 3 roughly equal lines
        per = -(-len(words) // 3)
        lines = [" ".join(words[i:i+per]) for i in range(0, len(words), per)]
    longest = max(len(l) for l in lines)
    size = 78 if longest <= 12 else 68 if longest <= 16 else 58 if longest <= 20 else 50
    return "<br>".join(lines), size

def build_config(job):
    """Turn a scraped job dict into a render config compatible with generate().
    job keys: title, company, fields, location, jtype, duration."""
    style = _pick_style(job.get("fields", ""))
    accent, accent_d, bg1, bg2, spark, art_fn, hook = SECTOR_STYLES[style]
    title_html, title_size = _wrap_title(_sanitize(strip_year(job["title"])))
    # primary sector = first comma-group, sanitized
    primary = _sanitize((job.get("fields", "") or "").split(",")[0]) or "Internship"
    details = [
        ("field", primary),
        ("location", _sanitize(job.get("location", "")) or "UK"),
        ("type", _sanitize(job.get("jtype", "")) or "Internship"),
        ("duration", _sanitize(job.get("duration", "")) or "Flexible"),
    ]
    return {
        "title": title_html,
        "title_size": title_size,
        "company": _sanitize(job.get("company", "")),
        "hook": hook,
        "details": details,
        "accent": accent, "accent_dark": accent_d,
        "bg1": bg1, "bg2": bg2, "spark": spark,
        "art_fn": art_fn,
        "_style": style,
    }


# ── Original 3D-style character (inline SVG, reference-spirit, not a copy) ────
def _char_designer(accent):
    """A friendly 3D-style character holding a giant pen. Built from scratch."""
    return f"""<svg width="500" height="720" viewBox="0 0 500 720" xmlns="http://www.w3.org/2000/svg"
     style="filter:drop-shadow(0 24px 34px rgba(0,0,0,0.4));">
  <defs>
    <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD3AE"/><stop offset="1" stop-color="#E9A87E"/></linearGradient>
    <linearGradient id="skinA" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFCBA0"/><stop offset="1" stop-color="#E09A6E"/></linearGradient>
    <linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6E4A30"/><stop offset="1" stop-color="#472F1E"/></linearGradient>
    <linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#37C7B4"/><stop offset="1" stop-color="#1E9184"/></linearGradient>
    <linearGradient id="topD" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2AA99A"/><stop offset="1" stop-color="#177669"/></linearGradient>
    <linearGradient id="trouser" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#333A55"/><stop offset="1" stop-color="#232840"/></linearGradient>
    <linearGradient id="pen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E96F5"/><stop offset="1" stop-color="#3B62D6"/></linearGradient>
    <linearGradient id="nib" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F4F8"/><stop offset="1" stop-color="#C7CFDC"/></linearGradient>
    <radialGradient id="bulb" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#FFE38A"/><stop offset="1" stop-color="#FFB120"/></radialGradient>
  </defs>

  <!-- ground shadow -->
  <ellipse cx="250" cy="686" rx="150" ry="26" fill="rgba(0,0,0,0.28)"/>

  <!-- BACK leg -->
  <path d="M232 470 q-8 90 -20 150 q-4 24 -2 46 l40 0 q4 -30 10 -60 q10 -70 14 -132 z" fill="url(#trouser)"/>
  <!-- back sneaker -->
  <path d="M206 660 q-6 18 4 28 q6 6 34 6 l24 0 q6 -2 4 -12 l-4 -22 z" fill="#EDEEF2"/>
  <path d="M204 682 q0 12 10 12 l58 0 q6 0 4 -8 l-72 0 z" fill="#2A2E45"/>

  <!-- FRONT leg -->
  <path d="M258 460 q18 84 30 148 q6 30 4 66 l-46 0 q-2 -34 -6 -66 q-8 -78 -20 -142 z" fill="url(#trouser)"/>
  <!-- front sneaker -->
  <path d="M244 662 q-8 20 2 30 q6 6 36 6 l30 0 q8 -2 6 -14 l-6 -24 z" fill="#FFFFFF"/>
  <path d="M242 686 q0 12 12 12 l64 0 q6 0 4 -10 l-80 0 z" fill="#2A2E45"/>
  <path d="M262 674 l40 6" stroke="{accent}" stroke-width="5" stroke-linecap="round"/>

  <!-- torso / top -->
  <path d="M214 300 q-14 90 6 176 q60 22 118 -2 q16 -92 -2 -178 q-58 -26 -122 4 z" fill="url(#top)"/>
  <path d="M300 300 q20 86 4 176 q16 -6 34 -6 q16 -92 -2 -178 q-18 4 -36 8 z" fill="url(#topD)" opacity="0.6"/>

  <!-- FAR arm (behind pen), reaching down-left -->
  <path d="M226 322 q-40 30 -70 78 q-8 12 2 22 q10 8 22 -2 q40 -44 74 -72 z" fill="url(#topD)"/>
  <circle cx="158" cy="418" r="20" fill="url(#skinA)"/>

  <!-- GIANT PEN diagonal -->
  <g transform="rotate(-38 250 400)">
    <rect x="150" y="372" width="250" height="56" rx="28" fill="url(#pen)"/>
    <rect x="150" y="380" width="250" height="12" rx="6" fill="#ffffff" opacity="0.28"/>
    <path d="M400 372 l64 28 l-64 28 q-6 -28 0 -56 z" fill="url(#nib)"/>
    <path d="M446 393 l18 7 l-18 7 z" fill="#333A55"/>
    <rect x="392" y="384" width="10" height="32" rx="3" fill="#333A55" opacity="0.35"/>
  </g>

  <!-- NEAR arm gripping pen -->
  <path d="M296 330 q46 6 92 40 q12 9 4 22 q-8 12 -22 4 q-40 -28 -80 -34 z" fill="url(#top)"/>
  <circle cx="386" cy="392" r="22" fill="url(#skin)"/>

  <!-- neck -->
  <path d="M236 250 q0 34 4 54 q30 14 60 0 q4 -22 4 -54 z" fill="url(#skinA)"/>

  <!-- head -->
  <circle cx="266" cy="196" r="72" fill="url(#skin)"/>
  <!-- ear -->
  <circle cx="196" cy="200" r="14" fill="url(#skinA)"/>
  <!-- hair -->
  <path d="M196 180 q4 -74 74 -74 q66 0 74 66 q2 20 -6 34 q-6 -34 -34 -44 q-40 -14 -78 6 q-24 12 -30 40 q-6 -14 0 -28 z" fill="url(#hair)"/>
  <path d="M330 150 q14 20 8 48 q-4 -18 -14 -30 z" fill="url(#hair)"/>
  <!-- face -->
  <circle cx="252" cy="196" r="6.5" fill="#2A2320"/>
  <circle cx="296" cy="196" r="6.5" fill="#2A2320"/>
  <path d="M250 222 q18 16 40 2" stroke="#B96A48" stroke-width="6" fill="none" stroke-linecap="round"/>
  <ellipse cx="238" cy="212" rx="9" ry="6" fill="#FF9C8A" opacity="0.5"/>
  <ellipse cx="304" cy="212" rx="9" ry="6" fill="#FF9C8A" opacity="0.5"/>

  <!-- floating lightbulb -->
  <g transform="translate(96 150)">
    <circle cx="0" cy="0" r="30" fill="url(#bulb)"/>
    <rect x="-11" y="24" width="22" height="12" rx="3" fill="#C9922A"/>
    <path d="M-6 -6 l6 8 l8 -12" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>
    <path d="M-40 -30 l-14 -10 M40 -30 l14 -10 M0 -46 l0 -16" stroke="#FFD778" stroke-width="5" stroke-linecap="round"/>
  </g>

  <!-- cursor + colour dots -->
  <g transform="translate(150 470)">
    <path d="M0 0 l0 30 l8 -8 l6 12 l6 -3 l-6 -12 l11 0 z" fill="#fff" stroke="#2A2E45" stroke-width="2"/>
  </g>
  <circle cx="430" cy="470" r="12" fill="#FF6B6B"/>
  <circle cx="462" cy="500" r="10" fill="#FFB120"/>
  <circle cx="446" cy="536" r="8" fill="#7FDBB6"/>
</svg>"""


def _detail_row(label, value, accent):
    icons = {
        "location": '<path d="M12 2 C7 2 3 6 3 11 c0 7 9 15 9 15 s9-8 9-15 c0-5-4-9-9-9 z M12 14 a3 3 0 1 0 0-6 a3 3 0 0 0 0 6 z" fill="#fff"/>',
        "type":     '<rect x="3" y="7" width="18" height="13" rx="2" fill="#fff"/><path d="M8 7 V5 a2 2 0 0 1 2-2 h4 a2 2 0 0 1 2 2 V7" fill="none" stroke="#fff" stroke-width="2"/>',
        "duration": '<circle cx="12" cy="12" r="9" fill="none" stroke="#fff" stroke-width="2"/><path d="M12 7 v5 l4 2" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "deadline": '<rect x="4" y="5" width="16" height="16" rx="2" fill="none" stroke="#fff" stroke-width="2"/><path d="M4 9 h16 M8 3 v4 M16 3 v4" stroke="#fff" stroke-width="2"/><path d="M9 15 l2 2 l4-4" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
        "field":    '<path d="M4 7 h16 v10 a2 2 0 0 1 -2 2 H6 a2 2 0 0 1 -2 -2 Z" fill="#fff"/><path d="M9 7 V5 h6 v2" fill="none" stroke="#fff" stroke-width="2"/>',
    }
    return f"""<div style="display:flex;align-items:center;gap:16px;">
  <div style="width:52px;height:52px;border-radius:14px;background:{accent};flex-shrink:0;
               display:flex;align-items:center;justify-content:center;box-shadow:0 6px 12px rgba(0,0,0,0.25);">
    <svg width="26" height="26" viewBox="0 0 24 24">{icons.get(label,'')}</svg>
  </div>
  <div style="flex:1;">
    <div style="font-family:'DM Sans';font-weight:700;font-size:18px;color:rgba(255,255,255,0.55);
                 text-transform:uppercase;letter-spacing:2px;">{label if label!='field' else 'sector'}</div>
    <div style="font-family:Inter;font-weight:700;font-size:26px;color:#fff;letter-spacing:-0.3px;line-height:1.15;">{value}</div>
  </div>
</div>"""


def generate(job, out_path, photo_path=None, art_mode="photo"):
    f = _fonts()
    accent   = job["accent"]
    accent_d = job["accent_dark"]
    bg1, bg2 = job["bg1"], job["bg2"]

    rows = ""
    for label, value in job["details"]:
        rows += _detail_row(label, value, accent)

    if art_mode == "graphic":
        # 3D object cluster (no human); self-contained, no separate motif
        art = (f'<div style="position:absolute;bottom:-30px;right:-20px;z-index:10;">'
               f'{job["art_fn"](accent)}</div>')
        motif_block = ""
    elif art_mode == "character":
        # 3D SVG character; motif lives inside the character, so skip the separate motif
        art = (f'<div style="position:absolute;bottom:-10px;right:-6px;z-index:10;">'
               f'{job["char_fn"](accent)}</div>')
        motif_block = ""
    else:
        photo = _src(photo_path)
        art = (f'<img src="{photo}" style="position:absolute;bottom:0;right:-30px;height:720px;'
               f'object-fit:contain;z-index:10;filter:drop-shadow(0 18px 30px rgba(0,0,0,0.4));">')
        motif = job["motif_fn"](accent)
        motif_block = f'<div style="position:absolute;bottom:250px;right:340px;z-index:8;">{motif}</div>'

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:{W}px;height:{H}px;overflow:hidden;
      background:linear-gradient(150deg,{bg1} 0%,{bg2} 100%);}}
.c{{width:{W}px;height:{H}px;position:relative;padding:54px 56px;display:flex;flex-direction:column;}}
{GRAIN}
</style></head><body><div class="c">
<div class="grain"></div>

<!-- soft diagonal light panel -->
<div style="position:absolute;top:0;right:0;width:620px;height:{H}px;z-index:1;
             background:linear-gradient(160deg,rgba(255,255,255,0.10),transparent 60%);
             clip-path:polygon(28% 0,100% 0,100% 100%,0 100%);"></div>

{_sparkles(job.get('spark', LIME))}

<!-- Header: FEATURED JOB tag + logo -->
<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-shrink:0;position:relative;z-index:20;">
  <div style="background:linear-gradient(100deg,{accent},{accent_d});color:#fff;
               padding:14px 26px;border-radius:50px;font-family:Inter;font-weight:700;
               font-size:24px;letter-spacing:4px;box-shadow:0 8px 18px rgba(0,0,0,0.3);">FEATURED JOB</div>
  <img src="data:image/png;base64,{LOGO_W}" style="height:66px;">
</div>

<!-- Hook line -->
<div style="margin-top:34px;position:relative;z-index:20;background:rgba(255,255,255,0.12);
             border:2px solid rgba(255,255,255,0.22);border-radius:18px;padding:20px 24px;max-width:640px;
             backdrop-filter:blur(4px);">
  <div style="font-family:'DM Sans';font-weight:500;font-size:24px;color:rgba(255,255,255,0.92);line-height:1.4;">
    {job['hook']}
  </div>
</div>

<!-- Role title + company -->
<div style="margin-top:34px;position:relative;z-index:20;max-width:640px;">
  <div style="font-family:Inter;font-weight:700;font-size:{job.get('title_size',74)}px;line-height:0.98;
               color:#fff;letter-spacing:-2.5px;word-break:keep-all;hyphens:none;">
    {job['title']}
  </div>
</div>

<!-- Detail card -->
<div style="margin-top:32px;position:relative;z-index:20;background:rgba(0,0,0,0.20);
             border:2px solid rgba(255,255,255,0.16);border-radius:22px;padding:28px 30px;max-width:640px;
             display:flex;flex-direction:column;gap:18px;">
  {rows}
</div>

<div style="flex:1;"></div>

<!-- CTA -->
<div style="position:relative;z-index:20;">
  <div style="display:inline-flex;align-items:center;gap:14px;
               background:linear-gradient(100deg,{accent},{accent_d});color:#fff;
               padding:22px 46px;border-radius:60px;font-family:Inter;font-weight:700;font-size:32px;
               letter-spacing:1px;box-shadow:0 12px 24px rgba(0,0,0,0.35);">
    APPLY NOW &rarr;
  </div>
  <div style="font-family:'DM Sans';font-weight:700;font-size:26px;color:#fff;margin-top:20px;">www.internwise.co.uk</div>
  <div style="font-family:'DM Sans';font-weight:500;font-size:22px;color:rgba(255,255,255,0.7);margin-top:2px;">(Link in the post)</div>
</div>

<!-- role motif behind/beside the art (photo mode only) -->
{motif_block}

<!-- art: Pexels cutout OR 3D SVG character, bottom-right -->
{art}
</div></body></html>"""
    _render(html, out_path)


# ── Job configs ─────────────────────────────────────────────────────────────
JOBS = {
    "brand-design": {
        "title": "Brand Design<br>Internship",
        "title_size": 78,
        "company": "JBROWN GLOBAL LIMITED",
        "hook": "Love turning ideas into visuals that stop the scroll? Build your design portfolio with a real brand.",
        "details": [
            ("field", "Graphic &amp; Brand Design"),
            ("location", "Central London"),
            ("type", "Part-time"),
            ("duration", "1 - 3 months"),
        ],
        "accent": PURPLE, "accent_dark": "#5B3FC4",
        "bg1": "#2B1E63", "bg2": "#4A2F9E", "spark": LIME,
        "motif_fn": _svg_swatches,
        "char_fn": _char_designer,
        "art_fn": _cluster_branddesign,
        "photo_query": "confident young professional standing arms crossed full body studio white background",
    },

    "surveying": {
        "title": "Real Estate<br>Surveying<br>Internship",
        "title_size": 68,
        "company": "JBROWN GLOBAL LIMITED",
        "hook": "Curious how property really works? Get hands-on with surveys, valuations and site visits across London.",
        "details": [
            ("field", "Surveying &amp; Real Estate"),
            ("location", "Central London"),
            ("type", "Part-time / Full-time"),
            ("duration", "7 - 12 months"),
        ],
        # deep construction green + hi-vis amber
        "accent": AMBER, "accent_dark": "#D18E14",
        "bg1": "#0E4433", "bg2": "#1B7B58", "spark": LIME,
        "art_fn": _cluster_surveying,
    },

    "marketing": {
        "title": "Marketing<br>Internship",
        "title_size": 78,
        "company": "M N K ACCOUNTANTS LTD",
        "hook": "Ready to run real campaigns? Own content, socials and growth for a busy London firm.",
        "details": [
            ("field", "Marketing &amp; Social Media"),
            ("location", "Camden Town, London"),
            ("type", "Part-time"),
            ("duration", "7 - 12 months"),
        ],
        # warm coral / magenta
        "accent": CORAL, "accent_dark": "#D2415C",
        "bg1": "#7E2038", "bg2": "#C43F5C", "spark": LIME,
        "art_fn": _cluster_marketing,
    },

    "social-content": {
        "title": "Social Media &amp;<br>Content Intern",
        "title_size": 62,
        "company": "LONDON PROPERTY STAGING LTD",
        "hook": "Love creating scroll-stopping content? Shoot, edit and post for beautifully staged London homes.",
        "details": [
            ("field", "Social, Photo &amp; Interiors"),
            ("location", "London, Greater London"),
            ("type", "Part-time"),
            ("duration", "1 - 3 months"),
        ],
        # editorial blue / cyan
        "accent": "#5AA9E8", "accent_dark": "#2E6BB0",
        "bg1": "#123A66", "bg2": "#1E6FAE", "spark": LIME,
        "art_fn": _cluster_social,
    },
}


def run(job_key, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    _load_logos()
    job = JOBS[job_key]
    generate(job, os.path.join(out_dir, f"{job_key}-graphic.png"), art_mode="graphic")
    register_design(f"featured_job_portrait_{job_key}", f"featured/{job_key}", "featured")
    print(f"Done - {job_key}")
    register_design(f"featured_job_portrait_{job_key}", f"featured/{job_key}", "featured")
    print(f"Done - {job_key}")


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "brand-design"
    run(key, "campaigns/outputs/featured-jobs")
