"""
Internwise — ChatGPT Prompts Carousel
Post 4: 5-slide Instagram carousel (1080x1080)
Integrates DiceBear avataaars for practical AI job search tips.
"""

import os
import base64
import requests
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

DEEP_BLUE = "#264D7E"
TEAL = "#5B9291"
MEDIUM_BLUE = "#3E77B1"
LIGHT_BLUE = "#5FA7E5"
AMBER = "#FFB120"
GPT_GREEN = "#10a37f"


def _load_file_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _build_font_faces():
    fonts = {
        "Inter": [
            ("Inter-Bold.ttf", 700), ("Inter-SemiBold.ttf", 600),
            ("Inter-Medium.ttf", 500), ("Inter-Regular.ttf", 400),
        ],
        "DM Sans": [
            ("DMSans-Bold.ttf", 700), ("DMSans-Medium.ttf", 500),
            ("DMSans-Regular.ttf", 400),
        ],
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


def _fetch_dicebear_avatar(seed, style="avataaars", scale=100):
    url = f"https://api.dicebear.com/7.x/{style}/png?seed={seed}&scale={scale}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return base64.b64encode(resp.content).decode()
    except Exception:
        pass
    return None


def _render(html, output_path, width=1080, height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()
    print(f"  ✓ {output_path}")


def generate_slide1(campaign_dir):
    """Slide 1: Hook with 4 avatars"""

    w, h = 1080, 1080
    font_faces = _build_font_faces()
    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""

    avatars = [_fetch_dicebear_avatar(f"gpt_{i}", "avataaars", 100) for i in range(4)]
    avatar_grid = "".join(f'<img src="data:image/png;base64,{av}" class="avatar">' for av in avatars if av)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, {DEEP_BLUE} 0%, #1a3d5e 100%);
}}

.logo-wrap {{ position:absolute; top:30px; left:30px; z-index:25; }}
.logo {{ height:70px; opacity:0.9; }}

.top-bar {{ position:absolute; top:0; left:0; right:0; height:5px;
    background: linear-gradient(90deg, {TEAL}, {MEDIUM_BLUE}, {LIGHT_BLUE}, {AMBER}); z-index:30; }}

.content {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    width:90%; z-index:10;
}}

.headline {{
    font-family:Inter; font-weight:700;
    font-size:44px; line-height:1.3;
    color:white; text-align:center;
    margin-bottom:50px;
}}

.headline .highlight {{ color:{AMBER}; }}

.avatar-grid {{
    display:grid;
    grid-template-columns:repeat(2, 1fr);
    gap:30px;
    margin-bottom:30px;
}}

.avatar {{
    width:280px; height:280px;
    border-radius:16px;
    background:#f5f5f5;
    object-fit:contain;
    padding:10px;
}}

.subtext {{
    font-family:DM Sans; font-size:16px;
    color:rgba(255,255,255,0.85);
    text-align:center; line-height:1.5;
}}
</style>
</head><body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="logo-wrap">{logo_img}</div>
    <div class="content">
        <div class="headline"><span class="highlight">4 ChatGPT</span><br>Prompts That Work</div>
        <div class="avatar-grid">{avatar_grid}</div>
        <div class="subtext">Save hours. Use these proven prompts to accelerate your job search.</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_1.png"))


def generate_slides_2_5(campaign_dir):
    """Slides 2-5: One prompt per slide with avatar and content"""

    prompts = [
        {
            "title": "Tailor My CV",
            "prompt": '"Rewrite my CV to highlight my [SKILL] and [ACHIEVEMENT] for a [JOB TITLE] role."',
            "num": "2"
        },
        {
            "title": "Mock Interview",
            "prompt": '"Conduct a [COMPANY] interview for [JOB TITLE]. Ask tough questions."',
            "num": "3"
        },
        {
            "title": "Company Research",
            "prompt": '"What should I know about [COMPANY]? Culture, recent news, interview tips."',
            "num": "4"
        },
        {
            "title": "Cover Letter Boost",
            "prompt": '"Write a cover letter for [COMPANY]\'s [JOB TITLE] role. I have [EXPERIENCE]."',
            "num": "5"
        }
    ]

    font_faces = _build_font_faces()

    for i, prompt_data in enumerate(prompts):
        avatar = _fetch_dicebear_avatar(f"gpt_prompt_{i}", "avataaars", 120)
        avatar_html = f'<img src="data:image/png;base64,{avatar}" class="avatar-main">' if avatar else ""

        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1080px; overflow:hidden; }}

.canvas {{
    width:1080px; height:1080px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, #1a3d5e 0%, {DEEP_BLUE} 100%);
}}

.grid {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:grid;
    grid-template-columns:320px 1fr;
    gap:40px;
    width:90%; z-index:10;
}}

.avatar-main {{
    width:320px; height:380px;
    border-radius:20px;
    background:#f5f5f5;
    object-fit:contain;
    padding:10px;
}}

.content {{
    display:flex;
    flex-direction:column;
    justify-content:center;
}}

.number {{
    font-family:DM Sans; font-size:13px;
    color:rgba(255,255,255,0.6);
    text-transform:uppercase; letter-spacing:1px;
    margin-bottom:10px;
}}

.title {{
    font-family:Inter; font-weight:700;
    font-size:40px; color:white;
    line-height:1.3; margin-bottom:20px;
}}

.prompt-box {{
    background:rgba(16,163,127,0.15);
    border:1px solid {GPT_GREEN};
    border-radius:12px;
    padding:20px;
    font-family:DM Sans; font-size:14px;
    color:{GPT_GREEN};
    line-height:1.6;
    font-weight:500;
}}

.prompt-copy {{
    font-family:DM Sans; font-size:12px;
    color:rgba(255,255,255,0.6);
    margin-top:15px;
    text-align:right;
}}
</style>
</head><body>
<div class="canvas">
    <div class="grid">
        <div>{avatar_html}</div>
        <div class="content">
            <div class="number">Prompt {prompt_data['num']}</div>
            <div class="title">{prompt_data['title']}</div>
            <div class="prompt-box">{prompt_data['prompt']}</div>
            <div class="prompt-copy">✓ Copy & paste into ChatGPT</div>
        </div>
    </div>
</div>
</body></html>
"""
        _render(html, os.path.join(campaign_dir, f"slide_{i+2}.png"))


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("📸 Generating ChatGPT Prompts Carousel (Post 4)...")
    generate_slide1(campaign_dir)
    generate_slides_2_5(campaign_dir)
    print("✓ ChatGPT Prompts carousel complete!")
