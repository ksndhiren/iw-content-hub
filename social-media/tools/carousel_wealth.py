"""
Internwise — 5 Types of Wealth Carousel (Gen Z Edition v3)
Post 9: 5-slide Instagram carousel (1080x1080)

Design:
- Slide 1: Stacked wealth bars — dark canvas, 5 coloured neobrutalist bars
- Slides 2-5: Arch + real photo cutout per wealth type, bold left-side text
"""

import os
import base64
from playwright.sync_api import sync_playwright
from pexels_utils import get_cutout, get_photo

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR  = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"
DARK_NAVY = "#162d4a"
AMBER     = "#FFB120"
CORAL     = "#FF6B6B"
PURPLE    = "#7B5CE6"
MINT      = "#7FDBB6"
OFF_WHITE = "#FAF5EC"


def _load_file_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _img_data_src(path):
    b64 = _load_file_base64(path)
    if not b64:
        return ""
    mime = "image/png" if path.endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def _build_font_faces():
    fonts = {
        "Inter":   [("Inter-Bold.ttf", 700), ("Inter-SemiBold.ttf", 600),
                    ("Inter-Medium.ttf", 500), ("Inter-Regular.ttf", 400)],
        "DM Sans": [("DMSans-Bold.ttf", 700), ("DMSans-Medium.ttf", 500),
                    ("DMSans-Regular.ttf", 400)],
    }
    css = ""
    for family, variants in fonts.items():
        for filename, weight in variants:
            b64 = _load_file_base64(os.path.join(FONTS_DIR, filename))
            if b64:
                css += f"""
@font-face {{
    font-family: '{family}';
    src: url(data:font/truetype;base64,{b64}) format('truetype');
    font-weight: {weight}; font-style: normal;
}}"""
    return css


def _render(html, output_path, width=1080, height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()
    print(f"  ✓ {output_path}")


def _fetch_photos():
    print("  ↓ Fetching Pexels photos...")
    photos = {
        # Slide 2 — Financial: full photo (clipped to arch), UK pounds sterling
        "financial": get_photo("british pound notes sterling money cash savings finance",
                               index=0, orientation="portrait", size="medium"),
        # Slide 3 — Time: full photo (clipped to arch), no rembg needed
        "time":      get_photo("young woman laptop coffee remote work freedom lifestyle smiling",
                               index=0, orientation="portrait", size="medium"),
        # Slide 4 — Social: two people, studio/plain bg
        "social":    get_cutout("two young friends smiling studio white background portrait",
                                index=0, orientation="portrait"),
        # Slide 5 — Physical+Spiritual: full photo (clipped to arch), no rembg needed
        "spiritual": get_photo("woman yoga meditation lotus pose peaceful mindful wellness",
                               index=0, orientation="portrait", size="medium"),
        # Slide 1 hook bars — small thumbnails, no bg removal needed
        "bar_financial": get_photo("business professional smiling confident office portrait",
                                   index=0, orientation="portrait", size="medium"),
        "bar_time":      get_photo("laptop coffee work from home lifestyle relaxed",
                                   index=0, orientation="landscape", size="medium"),
        "bar_social":    get_photo("young people networking handshake meeting smiling",
                                   index=0, orientation="portrait", size="medium"),
        "bar_physical":  get_photo("young person fitness gym workout sport",
                                   index=0, orientation="portrait", size="medium"),
        "bar_spiritual": get_photo("woman meditation calm mindfulness peaceful",
                                   index=0, orientation="portrait", size="medium"),
    }
    for k, v in photos.items():
        print(f"    ✓ {k}: {v}")
    return photos


# ── Slide 1 — Stacked wealth bars hook ───────────────────────────────────────

def generate_slide1(campaign_dir, bar_photos):
    w, h = 1080, 1080
    font_faces = _build_font_faces()
    logo_b64 = _load_file_base64(
        os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="height:72px;opacity:0.95;">' \
               if logo_b64 else ""

    # Bento grid: 2 cards top row, 3 cards bottom row
    # Inner width: 1000px (40px L/R padding), gap: 12px
    PAD, GAP = 40, 12
    IW = w - PAD * 2   # 1000

    r1_h = 374          # row 1 height
    r2_h = 374          # row 2 height
    grid_y = 256        # grid top

    c1_w = 608          # big card (Financial)
    c2_w = IW - c1_w - GAP           # 380 (Time)
    c3_w = (IW - GAP * 2) // 3       # 325 (Social, Physical)
    c5_w = IW - c3_w * 2 - GAP * 2  # 328 (Spiritual, absorbs rounding)

    card_defs = [
        # Financial — big top-left
        dict(left=PAD,                   top=grid_y,
             width=c1_w, height=r1_h,
             num="01", name="Financial", accent="Wealth",
             tag="The salary. The bag. The passive income.",
             overlay=AMBER, fg=DEEP_BLUE, italic_fg=DEEP_BLUE,
             tag_fg="rgba(38,77,126,0.72)", num_fg=DARK_NAVY,
             name_sz=68, acc_sz=52, tag_sz=20, num_sz=200,
             photo_key="bar_financial"),
        # Time — medium top-right
        dict(left=PAD + c1_w + GAP,      top=grid_y,
             width=c2_w, height=r1_h,
             num="02", name="Time", accent="Wealth",
             tag="Work on your own terms.",
             overlay=CORAL, fg="white", italic_fg="white",
             tag_fg="rgba(255,255,255,0.82)", num_fg=DARK_NAVY,
             name_sz=58, acc_sz=46, tag_sz=19, num_sz=168,
             photo_key="bar_time"),
        # Social — bottom-left small
        dict(left=PAD,                   top=grid_y + r1_h + GAP,
             width=c3_w, height=r2_h,
             num="03", name="Social", accent="Wealth",
             tag="Network = net worth.",
             overlay=PURPLE, fg="white", italic_fg=MINT,
             tag_fg="rgba(255,255,255,0.82)", num_fg=DARK_NAVY,
             name_sz=50, acc_sz=40, tag_sz=17, num_sz=148,
             photo_key="bar_social"),
        # Physical — bottom-center small
        dict(left=PAD + c3_w + GAP,      top=grid_y + r1_h + GAP,
             width=c3_w, height=r2_h,
             num="04", name="Physical", accent="Wealth",
             tag="Energy to show up.",
             overlay=MINT, fg=DEEP_BLUE, italic_fg=DEEP_BLUE,
             tag_fg="rgba(38,77,126,0.72)", num_fg=DARK_NAVY,
             name_sz=46, acc_sz=37, tag_sz=17, num_sz=148,
             photo_key="bar_physical"),
        # Spiritual — bottom-right small
        dict(left=PAD + c3_w * 2 + GAP * 2, top=grid_y + r1_h + GAP,
             width=c5_w, height=r2_h,
             num="05", name="Spiritual", accent="Wealth",
             tag="Purpose > prestige.",
             overlay=DARK_NAVY, fg=AMBER, italic_fg=AMBER,
             tag_fg="rgba(255,177,32,0.8)", num_fg="white",
             name_sz=46, acc_sz=37, tag_sz=17, num_sz=148,
             photo_key="bar_spiritual"),
    ]

    cards_html = ""
    for c in card_defs:
        photo_src = _img_data_src(bar_photos[c["photo_key"]])
        cards_html += f"""
<div style="
    position:absolute;
    left:{c['left']}px; top:{c['top']}px;
    width:{c['width']}px; height:{c['height']}px;
    border-radius:22px; border:3px solid {DARK_NAVY};
    box-shadow:7px 7px 0 {DARK_NAVY};
    overflow:hidden; z-index:10;
">
    <div style="
        position:absolute; inset:0;
        background:url('{photo_src}') center/cover no-repeat;
    "></div>
    <div style="
        position:absolute; inset:0;
        background:{c['overlay']}; opacity:0.80;
    "></div>
    <div style="
        position:absolute; top:-14px; right:10px;
        font-family:Inter; font-weight:700;
        font-size:{c['num_sz']}px; line-height:1;
        color:{c['num_fg']}; opacity:0.14;
        pointer-events:none; white-space:nowrap;
    ">{c['num']}</div>
    <div style="position:absolute; bottom:22px; left:22px; right:14px;">
        <div style="
            font-family:Inter; font-weight:700;
            font-size:{c['name_sz']}px; line-height:0.88;
            color:{c['fg']}; letter-spacing:-2px;
        ">{c['name']}</div>
        <div style="
            font-family:Inter; font-weight:700; font-style:italic;
            font-size:{c['acc_sz']}px; line-height:1.0;
            color:{c['italic_fg']}; letter-spacing:-1.5px;
        ">{c['accent']}</div>
        <div style="
            font-family:DM Sans; font-weight:600;
            font-size:{c['tag_sz']}px; line-height:1.3;
            color:{c['tag_fg']}; margin-top:7px;
        ">{c['tag']}</div>
    </div>
</div>"""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}
.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(145deg, {DARK_NAVY} 0%, #1a2d50 100%);
}}
.grain {{
    position:absolute; inset:0; z-index:2; pointer-events:none;
    background-image: radial-gradient(rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 3px 3px;
}}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>

    <!-- Logo -->
    <div style="position:absolute; top:44px; left:44px; z-index:30;">{logo_img}</div>

    <!-- Badge -->
    <div style="
        position:absolute; top:36px; right:{PAD}px; z-index:30;
        background:{AMBER}; color:{DEEP_BLUE};
        padding:10px 22px; border-radius:50px;
        font-family:Inter; font-weight:700; font-size:14px;
        letter-spacing:2px; text-transform:uppercase;
        transform:rotate(3deg);
        box-shadow:0 8px 22px rgba(255,177,32,0.4);
    ">Real talk</div>

    <!-- Headline -->
    <div style="
        position:absolute; top:114px; left:{PAD}px; z-index:30;
        font-family:DM Sans; font-weight:700; font-size:17px;
        color:{AMBER}; text-transform:uppercase; letter-spacing:4px;
    ">5 Types of</div>
    <div style="
        position:absolute; top:134px; left:{PAD - 4}px; z-index:30;
        font-family:Inter; font-weight:700; font-style:italic;
        font-size:92px; line-height:0.88; letter-spacing:-4px;
        color:{AMBER}; text-shadow:5px 5px 0 {CORAL};
    ">WEALTH</div>
    <div style="
        position:absolute; top:220px; left:{PAD}px; z-index:30;
        font-family:DM Sans; font-weight:600; font-size:22px;
        color:rgba(255,255,255,0.65);
    ">Most people only chase <strong style='color:white;'>one.</strong></div>

    <!-- Bento cards -->
    {cards_html}

    <!-- CTA -->
    <div style="
        position:absolute; bottom:22px; left:{PAD}px; z-index:30;
        font-family:Inter; font-weight:700; font-size:19px;
        color:rgba(255,255,255,0.45);
    ">Swipe to build your <strong style='color:white;'>wealth stack →</strong></div>

    <!-- Sparkles -->
    <svg style="position:absolute;top:108px;right:340px;z-index:30;" width="22" height="22" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="white" opacity="0.45"/>
    </svg>
</div>
</body></html>"""
    _render(html, os.path.join(campaign_dir, "slide_1.png"))


# ── Wealth type slides (2-5) ─────────────────────────────────────────────────

def _wealth_slide(campaign_dir, slide_num, photo_path, config):
    w, h = 1080, 1080
    font_faces = _build_font_faces()
    photo_src  = _img_data_src(photo_path)
    use_full   = config.get("use_full_photo", False)

    styles = {
        "gold": {
            "canvas_bg":   f"linear-gradient(145deg, {DARK_NAVY} 0%, #1e3a60 100%)",
            "shape_bg":    f"linear-gradient(145deg, {AMBER}, #d97400)",
            "text_main":   "white",
            "text_accent": AMBER,
            "card_bg":     "rgba(255,255,255,0.95)",
            "card_text":   DEEP_BLUE,
        },
        "coral": {
            "canvas_bg":   f"linear-gradient(145deg, {OFF_WHITE} 0%, #f0ddd0 100%)",
            "shape_bg":    f"linear-gradient(145deg, {CORAL}, #c94500)",
            "text_main":   DEEP_BLUE,
            "text_accent": CORAL,
            "card_bg":     "white",
            "card_text":   DEEP_BLUE,
        },
        "purple": {
            "canvas_bg":   f"linear-gradient(145deg, {DARK_NAVY} 0%, #2a1f5e 100%)",
            "shape_bg":    f"linear-gradient(145deg, {PURPLE}, #4028b0)",
            "text_main":   "white",
            "text_accent": MINT,
            "card_bg":     "rgba(255,255,255,0.95)",
            "card_text":   DEEP_BLUE,
        },
        "mint": {
            "canvas_bg":   f"linear-gradient(145deg, #e2f7ef 0%, {OFF_WHITE} 100%)",
            "shape_bg":    f"linear-gradient(145deg, {MINT}, #1d9e6a)",
            "text_main":   DEEP_BLUE,
            "text_accent": "#1a8a60",
            "card_bg":     "white",
            "card_text":   DEEP_BLUE,
        },
    }
    s = styles[config["bg_style"]]
    dark_slide = config["bg_style"] in ("gold", "purple")
    num_bg  = AMBER if dark_slide else DEEP_BLUE
    num_fg  = DEEP_BLUE if dark_slide else "white"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: {s["canvas_bg"]};
}}
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(0,0,0,0.025) 1px, transparent 1px);
    background-size: 3px 3px; z-index:2;
}}
.number {{
    position:absolute; top:50px; left:50px;
    width:96px; height:96px; border-radius:50%;
    background:{num_bg}; color:{num_fg};
    display:flex; align-items:center; justify-content:center;
    font-family:Inter; font-weight:700; font-size:40px;
    transform:rotate(-5deg);
    box-shadow: 0 10px 28px rgba(0,0,0,0.25); z-index:25;
}}
.kicker {{
    position:absolute; top:76px; left:174px;
    font-family:DM Sans; font-weight:700; font-size:20px;
    color:{s["text_main"]}; opacity:0.55;
    text-transform:uppercase; letter-spacing:3px; z-index:20;
}}
.emoji-badge {{
    position:absolute; top:50px; right:50px;
    width:100px; height:100px; border-radius:26px;
    background:{AMBER};
    display:flex; align-items:center; justify-content:center;
    font-size:54px; transform:rotate(6deg);
    box-shadow: 8px 8px 0 {DEEP_BLUE}; z-index:25;
}}
.headline {{
    position:absolute; top:175px; left:50px;
    font-family:Inter; font-weight:700;
    font-size:106px; line-height:0.88;
    color:{s["text_main"]}; letter-spacing:-4px;
    z-index:20; max-width:630px;
}}
.headline .accent {{
    display:inline-block;
    background:{s["text_accent"]}; color:white;
    padding:2px 16px; transform:rotate(-1.5deg); font-style:italic;
}}
.desc {{
    position:absolute; top:430px; left:50px;
    font-family:DM Sans; font-weight:500; font-size:24px;
    color:{s["text_main"]}; opacity:0.8;
    max-width:510px; line-height:1.45; z-index:20;
}}
.arch {{
    position:absolute; bottom:20px; right:30px;
    width:460px; height:540px;
    background:{s["shape_bg"]};
    border-radius:230px 230px 40px 40px;
    z-index:5;
    box-shadow: 0 20px 50px rgba(0,0,0,0.2);
}}
.photo-wrap {{
    position:absolute; bottom:0; right:-20px;
    width:560px; height:680px;
    z-index:10;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.35));
}}
.photo-wrap img {{
    width:100%; height:100%;
    object-fit:contain; object-position:bottom;
}}
.full-photo {{
    position:absolute; bottom:20px; right:30px;
    width:460px; height:540px;
    border-radius:230px 230px 40px 40px;
    overflow:hidden; z-index:5;
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    border:3px solid {DARK_NAVY};
}}
.full-photo .pic {{
    position:absolute; inset:0;
    background-size:cover; background-position:center;
}}
.full-photo .tint {{
    position:absolute; inset:0;
    background:{s["shape_bg"]};
    opacity:0.45; mix-blend-mode:multiply;
}}
.full-photo .veil {{
    position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(0,0,0,0) 50%, rgba(0,0,0,0.25) 100%);
}}
.fact-card {{
    position:absolute; bottom:48px; left:50px;
    background:{DEEP_BLUE}; color:white;
    padding:22px 28px; border-radius:18px;
    max-width:490px; z-index:20;
    box-shadow: 0 12px 28px rgba(0,0,0,0.22);
}}
.fact-label {{
    font-family:DM Sans; font-weight:700; font-size:13px;
    color:{AMBER}; text-transform:uppercase;
    letter-spacing:2px; margin-bottom:5px;
}}
.fact-text {{
    font-family:Inter; font-weight:700; font-size:22px; line-height:1.25;
}}
.sp {{ position:absolute; z-index:14; }}
.sp1 {{ top:200px; right:520px; }}
.sp2 {{ top:400px; right:490px; }}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>
    <div class="number">{config["number"]}</div>
    <div class="kicker">Type #{config["number"]}</div>
    <div class="emoji-badge">{config["emoji"]}</div>
    <div class="headline">
        {config["title_line1"]}<br>
        <span class="accent">{config["title_line2"]}</span>
    </div>
    <div class="desc">{config["desc"]}</div>
    {('<div class="full-photo">'
      f'<div class="pic" style="background-image:url(' + photo_src + ');"></div>'
      '<div class="tint"></div>'
      '<div class="veil"></div>'
      '</div>') if use_full else
     ('<div class="arch"></div>'
      '<div class="photo-wrap">'
      f'<img src="{photo_src}">'
      '</div>')}
    <div class="fact-card">
        <div class="fact-label">{config["fact_label"]}</div>
        <div class="fact-text">{config["fact_text"]}</div>
    </div>
    <svg class="sp sp1" width="22" height="22" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z"
              fill="{s["text_accent"]}"/>
    </svg>
    <svg class="sp sp2" width="16" height="16" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="{AMBER}"/>
    </svg>
</div>
</body></html>"""
    _render(html, os.path.join(campaign_dir, f"slide_{slide_num}.png"))


# ── Per-slide wrappers ────────────────────────────────────────────────────────

def generate_slide2(campaign_dir, photo_path):
    _wealth_slide(campaign_dir, 2, photo_path, {
        "number": "1", "emoji": "💷",
        "title_line1": "Financial", "title_line2": "Wealth",
        "desc": "The salary, the savings, the side income.\nBuild this early - compounding is real.",
        "fact_label": "UK tech internship - first role",
        "fact_text": "£25k–£45k/yr. And it only goes up.",
        "bg_style": "gold",
        "use_full_photo": True,
    })


def generate_slide3(campaign_dir, photo_path):
    _wealth_slide(campaign_dir, 3, photo_path, {
        "number": "2", "emoji": "⏰",
        "title_line1": "Time", "title_line2": "Wealth",
        "desc": "Work when you want.\nGo where you want.\nNo permission required.",
        "fact_label": "AI & remote-first jobs",
        "fact_text": "83% offer flexible or async hours.",
        "bg_style": "coral",
        "use_full_photo": True,
    })


def generate_slide4(campaign_dir, photo_path):
    _wealth_slide(campaign_dir, 4, photo_path, {
        "number": "3", "emoji": "🤝",
        "title_line1": "Social", "title_line2": "Wealth",
        "desc": "Mentors, teammates, industry DMs.\nYour network is your net worth.",
        "fact_label": "The cheat code",
        "fact_text": "One internship = connections for life.",
        "bg_style": "purple",
    })


def generate_slide5(campaign_dir, photo_path):
    _wealth_slide(campaign_dir, 5, photo_path, {
        "number": "4+5", "emoji": "🧘",
        "title_line1": "Physical +", "title_line2": "Spiritual",
        "desc": "Energy. Health. Purpose.\nA career that actually means something.",
        "fact_label": "The real flex",
        "fact_text": "Burnout ≠ badge of honour. Choose wisely.",
        "bg_style": "mint",
        "use_full_photo": True,
    })


# ── Slide 6 — CONCLUSION / CTA ───────────────────────────────────────────────

def generate_slide6(campaign_dir):
    w, h = 1080, 1080
    font_faces = _build_font_faces()
    logo_b64 = _load_file_base64(
        os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = (f'<img src="data:image/png;base64,{logo_b64}" '
                f'style="position:absolute;top:44px;left:44px;height:72px;opacity:0.95;z-index:25;">')  \
               if logo_b64 else ""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}
.canvas {{
    width:{w}px; height:{h}px; position:relative; overflow:hidden;
    background: linear-gradient(145deg, {DARK_NAVY} 0%, #1a3050 100%);
}}
.grain {{
    position:absolute; inset:0;
    background-image: radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 3px 3px; z-index:2;
}}
.badge {{
    position:absolute; top:52px; right:52px;
    background:{AMBER}; color:{DEEP_BLUE};
    padding:12px 28px; border-radius:50px;
    font-family:Inter; font-weight:700; font-size:15px;
    letter-spacing:2px; text-transform:uppercase;
    transform:rotate(3deg);
    box-shadow: 0 8px 22px rgba(255,177,32,0.45); z-index:25;
}}
.kicker {{
    position:absolute; top:190px; left:60px;
    font-family:DM Sans; font-weight:700; font-size:24px;
    color:{AMBER}; text-transform:uppercase; letter-spacing:4px; z-index:20;
}}
.headline {{
    position:absolute; top:232px; left:60px;
    font-family:Inter; font-weight:700;
    font-size:150px; line-height:0.88;
    color:{AMBER}; letter-spacing:-6px;
    font-style:italic;
    text-shadow: 6px 6px 0 {CORAL}; z-index:20;
}}
.dots {{
    position:absolute; top:512px; left:60px;
    display:flex; gap:16px; z-index:20;
}}
.dot {{
    width:22px; height:22px; border-radius:50%;
}}
.sub {{
    position:absolute; top:556px; left:60px;
    font-family:DM Sans; font-weight:600; font-size:27px;
    color:rgba(255,255,255,0.7); line-height:1.45;
    max-width:640px; z-index:20;
}}
.cta {{
    position:absolute; bottom:58px; left:60px; right:60px;
    background:{DEEP_BLUE}; padding:28px 36px;
    border-radius:22px; z-index:20;
    display:flex; align-items:center; justify-content:space-between;
    border:3px solid rgba(255,255,255,0.1);
    box-shadow: 0 16px 40px rgba(0,0,0,0.3);
}}
.cta-text {{
    font-family:Inter; font-weight:700; font-size:26px;
    color:white; line-height:1.2;
}}
.cta-url {{
    font-family:Inter; font-weight:700; font-size:20px;
    color:{AMBER}; margin-top:4px; display:block;
}}
.cta-arrow {{
    width:68px; height:68px; background:{AMBER};
    border-radius:50%; display:flex; align-items:center; justify-content:center;
    flex-shrink:0;
}}
.sp {{ position:absolute; z-index:14; }}
</style>
</head><body>
<div class="canvas">
    <div class="grain"></div>
    {logo_img}
    <div class="badge">The Takeaway</div>
    <div class="kicker">Now you know</div>
    <div class="headline">BUILD<br>ALL 5.</div>
    <div class="dots">
        <div class="dot" style="background:{AMBER};"></div>
        <div class="dot" style="background:{CORAL};"></div>
        <div class="dot" style="background:{PURPLE};"></div>
        <div class="dot" style="background:{MINT};"></div>
        <div class="dot" style="background:#5FA7E5;"></div>
    </div>
    <div class="sub">Money matters. But it is not the only score.<br>Start with Financial. The rest follows.</div>
    <div class="cta">
        <div class="cta-text">
            Start your first internship today.
            <span class="cta-url">internwise.co.uk →</span>
        </div>
        <div class="cta-arrow">
            <svg width="34" height="34" viewBox="0 0 36 36">
                <path d="M8 18 L26 18 M20 10 L28 18 L20 26"
                    stroke="{DEEP_BLUE}" stroke-width="4" fill="none"
                    stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    </div>
    <svg class="sp" style="top:200px;right:80px;" width="36" height="36" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="{AMBER}" opacity="0.6"/>
    </svg>
    <svg class="sp" style="top:430px;right:220px;" width="22" height="22" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="white" opacity="0.3"/>
    </svg>
    <svg class="sp" style="top:155px;left:600px;" width="18" height="18" viewBox="0 0 40 40">
        <path d="M20 4 L23 17 L36 20 L23 23 L20 36 L17 23 L4 20 L17 17Z" fill="{CORAL}" opacity="0.5"/>
    </svg>
</div>
</body></html>"""
    _render(html, os.path.join(campaign_dir, "slide_6.png"))


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating Wealth Carousel (Gen Z Edition v3)...")
    photos = _fetch_photos()
    bar_photos = {k: photos[k] for k in photos if k.startswith("bar_")}
    generate_slide1(campaign_dir, bar_photos)
    generate_slide2(campaign_dir, photos["financial"])
    generate_slide3(campaign_dir, photos["time"])
    generate_slide4(campaign_dir, photos["social"])
    generate_slide5(campaign_dir, photos["spiritual"])
    generate_slide6(campaign_dir)
    print("✓ Wealth carousel complete!")
