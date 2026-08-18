"""
Internwise — Campaign Close Carousel
Post 10: 5-slide Instagram carousel (1080x1080)

Design concept: "Campaign Celebration"
- Light background with gradient
- Where to find internships framework
- 5 platforms: LinkedIn, University, Direct Outreach, etc.
- Celebration CTA to end campaign on high note
"""

import os
import base64
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


def _render(html, output_path, width=1080, height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()
    print(f"  Rendered: {output_path}")


def generate_slide_1(campaign_dir):
    w, h = 1080, 1080
    font_faces = _build_font_faces()
    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo">' if logo_b64 else ""

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

.top-bar {{ position:absolute; top:0; left:0; right:0; height:5px;
    background: linear-gradient(90deg, {TEAL}, {MEDIUM_BLUE}, {LIGHT_BLUE}, {AMBER}); z-index:30; }}

.logo {{ position:absolute; top:30px; left:30px; height:70px; opacity:0.9; z-index:25; }}

.content {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    width:90%; z-index:10;
}}

.headline {{
    font-family:Inter; font-weight:700;
    font-size:48px; line-height:1.2;
    color:white; text-align:center;
    margin-bottom:30px;
}}

.headline .highlight {{ color:{AMBER}; }}

.subtext {{
    font-family:DM Sans; font-size:16px;
    color:rgba(255,255,255,0.85);
    text-align:center; line-height:1.5;
}}
</style>
</head><body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="logo">{logo_img}</div>
    <div class="content">
        <div class="headline">Your Journey Starts <span class="highlight">Here</span></div>
        <div class="subtext">We've covered the mindset. Now let's find your internship.</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_1.png"))


def generate_slide_2(campaign_dir):
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, #f0f4f9 0%, #ffffff 100%);
}}

.content {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    width:90%; z-index:10;
}}

.title {{
    font-family:Inter; font-weight:700;
    font-size:42px; color:{DEEP_BLUE};
    text-align:center; line-height:1.3;
    margin-bottom:20px;
}}

.description {{
    font-family:DM Sans; font-size:16px;
    color:{DEEP_BLUE}; opacity:0.8;
    text-align:center; line-height:1.6;
}}
</style>
</head><body>
<div class="canvas">
    <div class="content">
        <div class="title">1. <span style="color:{AMBER}">LinkedIn</span></div>
        <div class="description">The largest professional network. Use advanced search filters to find companies and roles. Direct messaging works.</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_2.png"))


def generate_slide_3(campaign_dir):
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, {DEEP_BLUE} 0%, #162d4a 100%);
}}

.content {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    width:90%; z-index:10;
}}

.title {{
    font-family:Inter; font-weight:700;
    font-size:42px; color:white;
    text-align:center; line-height:1.3;
    margin-bottom:20px;
}}

.description {{
    font-family:DM Sans; font-size:16px;
    color:rgba(255,255,255,0.8);
    text-align:center; line-height:1.6;
}}
</style>
</head><body>
<div class="canvas">
    <div class="content">
        <div class="title">2. University <span style="color:{AMBER}">Career Services</span></div>
        <div class="description">Your institution often has partnerships and job boards. Use them! They filter for students and understand your schedule.</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_3.png"))


def generate_slide_4(campaign_dir):
    w, h = 1080, 1080
    font_faces = _build_font_faces()

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: linear-gradient(135deg, #f0f4f9 0%, #ffffff 100%);
}}

.content {{
    position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    width:90%; z-index:10;
}}

.title {{
    font-family:Inter; font-weight:700;
    font-size:42px; color:{DEEP_BLUE};
    text-align:center; line-height:1.3;
    margin-bottom:20px;
}}

.description {{
    font-family:DM Sans; font-size:16px;
    color:{DEEP_BLUE}; opacity:0.8;
    text-align:center; line-height:1.6;
}}
</style>
</head><body>
<div class="canvas">
    <div class="content">
        <div class="title">3. <span style="color:{AMBER}">Direct Outreach</span></div>
        <div class="description">Find a company you love. Look up their hiring contacts. Send a thoughtful email. Most don't expect it — you'll stand out.</div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_4.png"))


def generate_slide_5(campaign_dir):
    w, h = 1080, 1080
    font_faces = _build_font_faces()

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

.glow {{
    position:absolute;
    width:600px; height:600px;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    border-radius:50%;
    background: radial-gradient(circle,
        rgba(255,177,32,0.1) 0%,
        transparent 70%
    );
    z-index:1;
    filter: blur(50px);
}}

.content {{
    position:absolute;
    top:50%; left:50%;
    transform:translate(-50%,-50%);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    width:90%;
    z-index:10;
    text-align:center;
}}

.headline {{
    font-family:Inter; font-weight:700;
    font-size:48px; color:white;
    line-height:1.3; margin-bottom:30px;
}}

.headline .highlight {{ color:{AMBER}; }}

.cta {{
    font-family:DM Sans; font-size:16px;
    color:rgba(255,255,255,0.85);
}}

.cta-highlight {{
    color:{AMBER}; font-weight:700;
}}
</style>
</head><body>
<div class="canvas">
    <div class="glow"></div>
    <div class="content">
        <div class="headline">The Best Time to Start is <span class="highlight">Now</span></div>
        <div class="cta">Begin your internship journey today<br><span class="cta-highlight">www.internwise.co.uk</span></div>
    </div>
</div>
</body></html>
"""
    _render(html, os.path.join(campaign_dir, "slide_5.png"))


def main():
    campaign_dir = os.path.join(OUTPUT_DIR, "wk2-day5-campaign-close")
    os.makedirs(campaign_dir, exist_ok=True)
    print("\n📸 Generating Campaign Close Carousel (Original Design)...")
    generate_slide_1(campaign_dir)
    generate_slide_2(campaign_dir)
    generate_slide_3(campaign_dir)
    generate_slide_4(campaign_dir)
    generate_slide_5(campaign_dir)
    print("✅ Campaign Close carousel complete with original design!")
    print(f"   Output: {campaign_dir}")


if __name__ == "__main__":
    main()
