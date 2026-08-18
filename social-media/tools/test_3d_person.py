"""
Test: 3D CSS-illustrated person — prototype for Networking carousel.
Uses gradients, shadows, highlights, and perspective for depth.
"""

import os
import base64
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

DEEP_NAVY = "#264D7E"
CORAL = "#FF9961"
TEAL = "#5B9291"
AMBER = "#FFB120"
LIGHT_BLUE = "#5FA7E5"


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
    print(f"  ✓ {output_path}")


def test_3d_people():
    w, h = 1080, 1080
    font_faces = _build_font_faces()
    logo_b64 = _load_file_base64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png"))
    logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="height:70px;">' if logo_b64 else ""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
{font_faces}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{w}px; height:{h}px; overflow:hidden; }}

.canvas {{
    width:{w}px; height:{h}px;
    position:relative; overflow:hidden;
    background: {DEEP_NAVY};
}}

.top-bar {{
    position:absolute; top:0; left:0; right:0; height:5px;
    background: {CORAL}; z-index:30;
}}

.logo-wrap {{ position:absolute; top:32px; left:44px; z-index:25; }}

.badge {{
    position:absolute; top:44px; right:44px;
    font-family:'Inter',sans-serif; font-weight:600; font-size:14px;
    letter-spacing:3px; text-transform:uppercase;
    color:{CORAL}; border:1.5px solid rgba(255,153,97,0.4);
    padding:8px 20px; border-radius:24px; z-index:25;
}}

/* ── 3D Person Styles ── */

.person-3d {{
    position:relative;
    display:flex;
    flex-direction:column;
    align-items:center;
    filter: drop-shadow(0 12px 20px rgba(0,0,0,0.25));
}}

/* ─ WOMAN A: Long wavy hair, warm skin, coral sweater ─ */
.woman-a {{}}

.woman-a .hair-back {{
    position:absolute;
    width:120px; height:140px;
    background: radial-gradient(ellipse at 50% 30%, #3d2212 0%, #2a1508 80%);
    border-radius:55% 55% 45% 45%;
    top:0; left:50%; transform:translateX(-50%);
    z-index:1;
    box-shadow: inset -8px -10px 20px rgba(0,0,0,0.3),
                inset 8px 5px 15px rgba(80,50,30,0.2);
}}

/* Hair strands flowing down */
.woman-a .hair-strand-l {{
    position:absolute;
    width:35px; height:100px;
    background: linear-gradient(180deg, #3d2212 0%, #2a1508 60%, #1e0f05 100%);
    border-radius:0 0 20px 30px;
    top:80px; left:50%; transform:translateX(-72px);
    z-index:4;
    box-shadow: inset -4px 0 8px rgba(0,0,0,0.2);
}}
.woman-a .hair-strand-r {{
    position:absolute;
    width:35px; height:95px;
    background: linear-gradient(180deg, #3d2212 0%, #2a1508 60%, #1e0f05 100%);
    border-radius:0 0 30px 20px;
    top:80px; left:50%; transform:translateX(37px);
    z-index:4;
    box-shadow: inset 4px 0 8px rgba(0,0,0,0.2);
}}

.woman-a .head {{
    position:relative;
    width:100px; height:105px;
    background: radial-gradient(ellipse at 45% 35%, #e8b888 0%, #d4956b 40%, #c4845a 100%);
    border-radius:50% 50% 46% 46%;
    z-index:5;
    margin-top:15px;
    box-shadow: inset -6px -8px 16px rgba(0,0,0,0.12),
                inset 6px 6px 12px rgba(255,220,180,0.2),
                0 4px 8px rgba(0,0,0,0.1);
}}

/* Eyes */
.eye {{
    position:absolute;
    width:14px; height:15px;
    border-radius:50%;
    background: radial-gradient(circle at 40% 35%, #fff 20%, #2c1810 20%, #1a0e06 100%);
    box-shadow: inset 1px 1px 2px rgba(0,0,0,0.3);
}}
.woman-a .eye-l {{ top:40px; left:22px; }}
.woman-a .eye-r {{ top:40px; right:22px; }}

/* Eye shine */
.eye-shine {{
    position:absolute;
    width:5px; height:5px;
    border-radius:50%;
    background:white;
    top:3px; left:4px;
}}

/* Eyebrows */
.brow {{
    position:absolute;
    width:20px; height:6px;
    border-radius:4px 4px 0 0;
    border-top:3px solid;
}}
.woman-a .brow {{ border-color:#3d2212; }}
.woman-a .brow-l {{ top:30px; left:20px; transform:rotate(-5deg); }}
.woman-a .brow-r {{ top:30px; right:20px; transform:rotate(5deg); }}

/* Nose */
.nose {{
    position:absolute;
    left:50%; transform:translateX(-50%);
    width:12px; height:14px;
    background: linear-gradient(180deg, transparent 0%, rgba(180,120,80,0.3) 100%);
    border-radius:50%;
}}
.woman-a .nose {{ top:50px; }}

/* Mouth — warm smile */
.smile {{
    position:absolute;
    left:50%; transform:translateX(-50%);
    width:28px; height:12px;
    border-radius:0 0 14px 14px;
    background: linear-gradient(180deg, #c47050 0%, #a05838 100%);
    overflow:hidden;
}}
.smile .teeth {{
    position:absolute;
    top:0; left:3px; right:3px; height:5px;
    background:white;
    border-radius:0 0 4px 4px;
}}
.woman-a .smile {{ bottom:20px; }}

/* Cheek blush */
.blush {{
    position:absolute;
    width:18px; height:10px;
    border-radius:50%;
    background: rgba(230,130,100,0.25);
}}
.woman-a .blush-l {{ top:55px; left:10px; }}
.woman-a .blush-r {{ top:55px; right:10px; }}

/* Neck */
.woman-a .neck {{
    width:30px; height:22px;
    background: linear-gradient(180deg, #d4956b 0%, #c8896a 100%);
    margin-top:-8px;
    z-index:3;
    border-radius:0 0 4px 4px;
    box-shadow: inset -3px 0 6px rgba(0,0,0,0.08);
}}

/* Body — coral sweater */
.woman-a .torso {{
    position:relative;
    width:150px; height:130px;
    background: linear-gradient(180deg, #ff9961 0%, #e8854d 40%, #d97a42 100%);
    border-radius:35px 35px 20px 20px;
    margin-top:-10px;
    z-index:2;
    box-shadow: inset -10px -10px 25px rgba(0,0,0,0.12),
                inset 10px 8px 20px rgba(255,180,130,0.2),
                0 8px 16px rgba(0,0,0,0.15);
}}

/* Sweater neckline */
.woman-a .neckline {{
    position:absolute;
    top:-2px; left:50%; transform:translateX(-50%);
    width:50px; height:18px;
    border-radius:0 0 25px 25px;
    background: linear-gradient(180deg, #d4956b, #c8896a);
    z-index:1;
}}

/* Arms */
.arm-3d {{
    position:absolute;
    border-radius:20px;
    z-index:1;
}}

.woman-a .arm-l {{
    width:36px; height:100px;
    background: linear-gradient(180deg, #ff9961 0%, #e8854d 50%, #d97a42 100%);
    top:12px; left:-20px;
    transform:rotate(10deg);
    box-shadow: inset -4px 0 10px rgba(0,0,0,0.1),
                4px 4px 8px rgba(0,0,0,0.1);
}}
.woman-a .arm-r {{
    width:36px; height:100px;
    background: linear-gradient(180deg, #ff9961 0%, #e8854d 50%, #d97a42 100%);
    top:12px; right:-20px;
    transform:rotate(-10deg);
    box-shadow: inset 4px 0 10px rgba(0,0,0,0.1),
                -4px 4px 8px rgba(0,0,0,0.1);
}}

/* Hands */
.hand {{
    position:absolute;
    border-radius:50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}
.woman-a .hand-l {{
    width:28px; height:28px;
    background: radial-gradient(circle at 40% 35%, #e8b888, #d4956b);
    bottom:-12px; left:-24px;
}}
.woman-a .hand-r {{
    width:28px; height:28px;
    background: radial-gradient(circle at 40% 35%, #e8b888, #d4956b);
    bottom:-12px; right:-24px;
}}


/* ─ MAN A: Short hair, medium-dark skin, navy blazer with coral tie ─ */
.man-a {{}}

.man-a .hair {{
    position:absolute;
    width:98px; height:50px;
    background: radial-gradient(ellipse at 50% 70%, #1a1a1a 0%, #111 80%);
    border-radius:50px 50px 0 0;
    top:0; left:50%; transform:translateX(-50%);
    z-index:6;
    box-shadow: inset -5px -3px 10px rgba(50,50,50,0.3),
                inset 5px 3px 8px rgba(60,60,60,0.2);
}}

.man-a .head {{
    position:relative;
    width:96px; height:100px;
    background: radial-gradient(ellipse at 45% 35%, #dba373 0%, #c68642 40%, #b5763a 100%);
    border-radius:50% 50% 46% 46%;
    z-index:5;
    margin-top:25px;
    box-shadow: inset -6px -8px 16px rgba(0,0,0,0.12),
                inset 6px 6px 12px rgba(240,200,160,0.15),
                0 4px 8px rgba(0,0,0,0.1);
}}

.man-a .eye-l {{ top:38px; left:20px; }}
.man-a .eye-r {{ top:38px; right:20px; }}

.man-a .brow {{ border-color:#1a1a1a; }}
.man-a .brow-l {{ top:28px; left:18px; transform:rotate(-3deg); }}
.man-a .brow-r {{ top:28px; right:18px; transform:rotate(3deg); }}

.man-a .nose {{ top:48px; }}

.man-a .smile {{ bottom:18px; }}

.man-a .blush-l {{ top:52px; left:8px; }}
.man-a .blush-r {{ top:52px; right:8px; }}

/* Ears */
.ear {{
    position:absolute;
    width:14px; height:20px;
    border-radius:50%;
    box-shadow: inset -2px 0 4px rgba(0,0,0,0.1);
}}
.man-a .ear-l {{
    top:40px; left:-6px;
    background: radial-gradient(circle, #dba373, #c68642);
}}
.man-a .ear-r {{
    top:40px; right:-6px;
    background: radial-gradient(circle, #dba373, #c68642);
}}

.man-a .neck {{
    width:32px; height:20px;
    background: linear-gradient(180deg, #c68642, #b5763a);
    margin-top:-8px;
    z-index:3;
    border-radius:0 0 4px 4px;
    box-shadow: inset -3px 0 6px rgba(0,0,0,0.08);
}}

/* Body — navy blazer */
.man-a .torso {{
    position:relative;
    width:155px; height:135px;
    background: linear-gradient(180deg, #2d5a8c 0%, #264D7E 40%, #1e3f66 100%);
    border-radius:35px 35px 20px 20px;
    margin-top:-10px;
    z-index:2;
    box-shadow: inset -10px -10px 25px rgba(0,0,0,0.15),
                inset 8px 8px 20px rgba(60,110,170,0.15),
                0 8px 16px rgba(0,0,0,0.15);
}}

/* Shirt collar */
.man-a .collar-l {{
    position:absolute;
    top:-4px; left:42px;
    width:28px; height:26px;
    background: linear-gradient(135deg, #fff 0%, #eee 100%);
    clip-path:polygon(0 0, 100% 0, 60% 100%, 0 60%);
    z-index:3;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}}
.man-a .collar-r {{
    position:absolute;
    top:-4px; right:42px;
    width:28px; height:26px;
    background: linear-gradient(225deg, #fff 0%, #eee 100%);
    clip-path:polygon(0 0, 100% 0, 100% 60%, 40% 100%);
    z-index:3;
    box-shadow: -1px 1px 3px rgba(0,0,0,0.1);
}}

/* Tie */
.man-a .tie {{
    position:absolute;
    top:16px; left:50%; transform:translateX(-50%);
    z-index:4;
}}
.man-a .tie-knot {{
    width:16px; height:12px;
    background: linear-gradient(180deg, {CORAL}, #e8854d);
    border-radius:3px 3px 0 0;
    margin:0 auto;
}}
.man-a .tie-body {{
    width:14px; height:50px;
    background: linear-gradient(180deg, {CORAL} 0%, #e8854d 100%);
    clip-path:polygon(10% 0, 90% 0, 100% 100%, 0 100%);
    margin:0 auto;
    box-shadow: inset -3px 0 6px rgba(0,0,0,0.1);
}}

/* Lapels */
.man-a .lapel-l {{
    position:absolute;
    top:0; left:18px;
    width:30px; height:70px;
    border-right:2px solid rgba(255,255,255,0.06);
    z-index:2;
}}
.man-a .lapel-r {{
    position:absolute;
    top:0; right:18px;
    width:30px; height:70px;
    border-left:2px solid rgba(255,255,255,0.06);
    z-index:2;
}}

.man-a .arm-l {{
    width:38px; height:105px;
    background: linear-gradient(180deg, #2d5a8c 0%, #264D7E 50%, #1e3f66 100%);
    top:12px; left:-22px;
    transform:rotate(8deg);
    box-shadow: inset -4px 0 10px rgba(0,0,0,0.12),
                4px 4px 8px rgba(0,0,0,0.1);
}}
.man-a .arm-r {{
    width:38px; height:105px;
    background: linear-gradient(180deg, #2d5a8c 0%, #264D7E 50%, #1e3f66 100%);
    top:12px; right:-22px;
    transform:rotate(-8deg);
    box-shadow: inset 4px 0 10px rgba(0,0,0,0.12),
                -4px 4px 8px rgba(0,0,0,0.1);
}}

.man-a .hand-l {{
    width:28px; height:28px;
    background: radial-gradient(circle at 40% 35%, #dba373, #c68642);
    bottom:-14px; left:-26px;
}}
.man-a .hand-r {{
    width:28px; height:28px;
    background: radial-gradient(circle at 40% 35%, #dba373, #c68642);
    bottom:-14px; right:-26px;
}}

/* ─ Speech bubbles ─ */
.speech-3d {{
    position:relative;
    padding:16px 22px;
    border-radius:20px;
    font-family:'DM Sans',sans-serif;
    font-size:18px;
    line-height:1.4;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    max-width:230px;
}}
.speech-3d:after {{
    content:'';
    position:absolute;
    bottom:-10px;
    width:20px; height:20px;
    transform:rotate(45deg);
    border-radius:4px;
}}
.speech-left {{
    background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06));
    border:1px solid rgba(255,255,255,0.1);
    color:rgba(255,255,255,0.8);
}}
.speech-left:after {{
    background: rgba(255,255,255,0.08);
    border-right:1px solid rgba(255,255,255,0.1);
    border-bottom:1px solid rgba(255,255,255,0.1);
    left:30px;
}}
.speech-right {{
    background: linear-gradient(135deg, rgba(255,153,97,0.15), rgba(255,153,97,0.08));
    border:1px solid rgba(255,153,97,0.2);
    color:rgba(255,255,255,0.8);
}}
.speech-right:after {{
    background: rgba(255,153,97,0.1);
    border-right:1px solid rgba(255,153,97,0.2);
    border-bottom:1px solid rgba(255,153,97,0.2);
    right:30px;
}}

/* Scene layout */
.scene {{
    position:absolute;
    top:110px; left:0; right:0;
    display:flex;
    justify-content:center;
    gap:40px;
    z-index:10;
}}
.person-col {{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:16px;
}}

/* Title */
.title-zone {{
    position:absolute;
    bottom:130px; left:0; right:0;
    text-align:center; z-index:15; padding:0 70px;
}}
.headline {{
    font-family:'Inter',sans-serif; font-weight:800;
    font-size:62px; color:white; line-height:1.15;
    margin-bottom:20px;
}}
.headline .coral {{ color:{CORAL}; }}
.divider {{
    width:80px; height:4px; background:{CORAL};
    margin:0 auto 20px; border-radius:2px;
}}
.subline {{
    font-family:'DM Sans',sans-serif; font-weight:500;
    font-size:32px; color:rgba(255,255,255,0.5);
}}

.bottom-bar {{
    position:absolute; bottom:36px; left:0; right:0;
    display:flex; align-items:center; justify-content:center;
    z-index:25; gap:8px;
}}
.dot {{ width:8px; height:8px; border-radius:50%; background:rgba(255,255,255,0.25); }}
.dot.active {{ background:{CORAL}; width:28px; border-radius:4px; }}
.swipe {{
    position:absolute; bottom:38px; right:44px; z-index:25;
    font-family:'DM Sans',sans-serif; font-weight:500; font-size:16px;
    color:rgba(255,255,255,0.3);
}}

</style></head>
<body>
<div class="canvas">
    <div class="top-bar"></div>
    <div class="logo-wrap">{logo_img}</div>
    <div class="badge">Networking</div>

    <div class="scene">
        <!-- Woman A with speech -->
        <div class="person-col">
            <div class="speech-3d speech-left">Hi! I love your work in marketing...</div>
            <div class="person-3d woman-a">
                <div class="hair-back"></div>
                <div class="hair-strand-l"></div>
                <div class="hair-strand-r"></div>
                <div class="head">
                    <div class="eye eye-l"><div class="eye-shine"></div></div>
                    <div class="eye eye-r"><div class="eye-shine"></div></div>
                    <div class="brow brow-l"></div>
                    <div class="brow brow-r"></div>
                    <div class="nose"></div>
                    <div class="blush blush-l"></div>
                    <div class="blush blush-r"></div>
                    <div class="smile"><div class="teeth"></div></div>
                </div>
                <div class="neck"></div>
                <div class="torso">
                    <div class="neckline"></div>
                    <div class="arm-3d arm-l">
                        <div class="hand hand-l"></div>
                    </div>
                    <div class="arm-3d arm-r">
                        <div class="hand hand-r"></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Man A with speech -->
        <div class="person-col">
            <div class="speech-3d speech-right">Thanks! Let's grab coffee &#9749;</div>
            <div class="person-3d man-a">
                <div class="hair"></div>
                <div class="head">
                    <div class="ear ear-l"></div>
                    <div class="ear ear-r"></div>
                    <div class="eye eye-l"><div class="eye-shine"></div></div>
                    <div class="eye eye-r"><div class="eye-shine"></div></div>
                    <div class="brow brow-l"></div>
                    <div class="brow brow-r"></div>
                    <div class="nose"></div>
                    <div class="blush blush-l"></div>
                    <div class="blush blush-r"></div>
                    <div class="smile"><div class="teeth"></div></div>
                </div>
                <div class="neck"></div>
                <div class="torso">
                    <div class="collar-l"></div>
                    <div class="collar-r"></div>
                    <div class="tie">
                        <div class="tie-knot"></div>
                        <div class="tie-body"></div>
                    </div>
                    <div class="lapel-l"></div>
                    <div class="lapel-r"></div>
                    <div class="arm-3d arm-l">
                        <div class="hand hand-l"></div>
                    </div>
                    <div class="arm-3d arm-r">
                        <div class="hand hand-r"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="title-zone">
        <div class="headline">Nobody teaches you how to <span class="coral">network.</span></div>
        <div class="divider"></div>
        <div class="subline">So here is how.</div>
    </div>

    <div class="bottom-bar">
        <div class="dot active"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div>
    </div>
    <div class="swipe">Swipe &rarr;</div>
</div>
</body></html>"""

    out = os.path.join(OUTPUT_DIR, "wk2-day1-networking-carousel", "test_3d.png")
    _render(html, out)


if __name__ == "__main__":
    print("\n🧪 Testing 3D CSS People — Hook Slide Prototype")
    print("=" * 50)
    test_3d_people()
    print("\n✅ Test complete!")
