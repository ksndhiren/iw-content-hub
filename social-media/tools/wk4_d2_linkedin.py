"""
Internwise — LinkedIn Profile Stat Card (Week 4, Day 2) — v3
Single 1080x1080: LinkedIn profile SVG graphic on right, stats on left.
v3: replaced human photo (which overlapped stats) with relevant LinkedIn
    profile card SVG illustration. Full dark background. Larger text.
"""
import os, base64
from playwright.sync_api import sync_playwright

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
FONTS_DIR    = os.path.join(BASE_DIR, "assets", "fonts")

DEEP_BLUE = "#264D7E"; DARK_NAVY = "#162d4a"; AMBER = "#FFB120"
CORAL = "#FF6B6B"; MINT = "#7FDBB6"; LIGHT_BLUE = "#5FA7E5"
LI_BLUE = "#0077B5"

def _b64(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f: return base64.b64encode(f.read()).decode()

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
        pg = br.new_page(viewport={"width":1080,"height":1080}, device_scale_factor=2)
        pg.set_content(html, wait_until="networkidle")
        pg.screenshot(path=path, type="png")
        br.close()
    print(f"  ok {path}")

STATS = [
    (AMBER,      DEEP_BLUE, "9 in 10",  "recruiters check your profile before they meet you"),
    (MINT,       DEEP_BLUE, "21x",       "more views with a professional photo"),
    (CORAL,      "white",   "40x",       "more weekly engagement with a completed About section"),
    (LIGHT_BLUE, DEEP_BLUE, "70%+",      "of hiring decisions influenced by online presence"),
]

# LinkedIn profile card SVG — positioned in right half of canvas
LINKEDIN_SVG = f"""
<svg width="430" height="720" viewBox="0 0 430 720"
     style="position:absolute;right:38px;top:50%;transform:translateY(-50%);z-index:10;
            filter:drop-shadow(0 24px 60px rgba(0,0,0,0.55));"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="card-clip"><rect width="430" height="720" rx="22"/></clipPath>
    <clipPath id="avatar-clip"><circle cx="72" cy="72" r="60"/></clipPath>
  </defs>

  <!-- Card base -->
  <rect width="430" height="720" rx="22" fill="white"/>

  <!-- LinkedIn blue header -->
  <rect width="430" height="148" rx="0" fill="{LI_BLUE}" clip-path="url(#card-clip)"/>
  <rect y="126" width="430" height="22" fill="{LI_BLUE}"/>

  <!-- LinkedIn logo top-right (official icon paths, viewBox 0 0 24 24 scaled to 38x38) -->
  <g transform="translate(376,12) scale(1.583)">
    <rect width="24" height="24" rx="3" fill="#0A66C2"/>
    <path fill="white" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
  </g>

  <!-- Open-to-work green ring -->
  <circle cx="82" cy="178" r="68" fill="none" stroke="#22C55E" stroke-width="7"
          stroke-dasharray="12 5"/>

  <!-- Avatar white border -->
  <circle cx="82" cy="178" r="60" fill="white"/>

  <!-- Avatar fill -->
  <circle cx="82" cy="178" r="55" fill="{LI_BLUE}"/>

  <!-- Person silhouette -->
  <circle cx="82" cy="164" r="22" fill="white" opacity="0.92"/>
  <ellipse cx="82" cy="204" rx="32" ry="22" fill="white" opacity="0.92"/>

  <!-- Name + title -->
  <text x="162" y="175" font-family="Inter,sans-serif" font-size="20" font-weight="700" fill="#1a1a1a">Alex Johnson</text>
  <text x="162" y="197" font-family="Inter,sans-serif" font-size="13" fill="#555">Graduate | Seeking opportunities</text>
  <text x="162" y="215" font-family="Inter,sans-serif" font-size="13" fill="{LI_BLUE}" font-weight="600">500+ connections</text>

  <!-- Open to Work badge -->
  <rect x="162" y="226" width="132" height="24" rx="5" fill="#E7F5E7"/>
  <text x="172" y="242" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="#16a34a">#OpenToWork</text>

  <!-- Divider -->
  <line x1="20" y1="270" x2="410" y2="270" stroke="#E5E7EB" stroke-width="1"/>

  <!-- Analytics header -->
  <text x="22" y="298" font-family="Inter,sans-serif" font-size="15" font-weight="700" fill="#1a1a1a">Profile analytics</text>

  <!-- Stat box: views -->
  <rect x="22" y="310" width="185" height="86" rx="12" fill="#F0F7FF"/>
  <text x="114" y="348" font-family="Inter,sans-serif" font-size="28" font-weight="700"
        fill="{LI_BLUE}" text-anchor="middle">1,247</text>
  <text x="114" y="368" font-family="Inter,sans-serif" font-size="12" fill="#555"
        text-anchor="middle">profile views</text>
  <text x="114" y="386" font-family="Inter,sans-serif" font-size="11" fill="#22C55E"
        text-anchor="middle" font-weight="600">+21x w/ photo</text>

  <!-- Stat box: impressions -->
  <rect x="218" y="310" width="190" height="86" rx="12" fill="#F0F7FF"/>
  <text x="313" y="348" font-family="Inter,sans-serif" font-size="28" font-weight="700"
        fill="{LI_BLUE}" text-anchor="middle">4,892</text>
  <text x="313" y="368" font-family="Inter,sans-serif" font-size="12" fill="#555"
        text-anchor="middle">post impressions</text>
  <text x="313" y="386" font-family="Inter,sans-serif" font-size="11" fill="#22C55E"
        text-anchor="middle" font-weight="600">+40x w/ About section</text>

  <!-- Divider -->
  <line x1="20" y1="412" x2="410" y2="412" stroke="#E5E7EB" stroke-width="1"/>

  <!-- Recruiter notice -->
  <rect x="22" y="422" width="386" height="60" rx="12" fill="#FFF8EC"/>
  <text x="42" y="447" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="#B45309">9 in 10 recruiters</text>
  <text x="42" y="447" font-family="Inter,sans-serif" font-size="13" fill="#92400E">
    <tspan dx="112"> check your profile before interview</tspan>
  </text>
  <text x="42" y="467" font-family="Inter,sans-serif" font-size="12" fill="#92400E">Your profile IS your CV. Make it work.</text>

  <!-- Divider -->
  <line x1="20" y1="498" x2="410" y2="498" stroke="#E5E7EB" stroke-width="1"/>

  <!-- Recent activity -->
  <text x="22" y="524" font-family="Inter,sans-serif" font-size="15" font-weight="700" fill="#1a1a1a">Recent activity</text>

  <rect x="22" y="534" width="120" height="82" rx="10" fill="#F3F4F6"/>
  <rect x="152" y="534" width="120" height="82" rx="10" fill="#F3F4F6"/>
  <rect x="282" y="534" width="126" height="82" rx="10" fill="#F3F4F6"/>

  <!-- Post lines -->
  <rect x="22" y="626" width="180" height="10" rx="5" fill="#E5E7EB"/>
  <rect x="22" y="643" width="130" height="10" rx="5" fill="#E5E7EB" opacity="0.6"/>
  <rect x="22" y="660" width="220" height="10" rx="5" fill="#E5E7EB" opacity="0.4"/>

  <!-- Like icon -->
  <circle cx="280" cy="648" r="14" fill="#F0F7FF"/>
  <text x="280" y="654" font-family="serif" font-size="14" text-anchor="middle" fill="{LI_BLUE}">👍</text>
  <text x="305" y="653" font-family="Inter,sans-serif" font-size="12" fill="#555">24 likes</text>
</svg>"""


def generate(campaign_dir):
    os.makedirs(campaign_dir, exist_ok=True)
    print("Generating LinkedIn Stat Card v3 (Week 4, Day 2)...")

    f = _fonts()
    logo_b64 = _b64(os.path.join(BRANDING_DIR, "PNG", "IW.com_Horizontal_white logo.png")) or ""

    GRAIN = """<div style="position:absolute;inset:0;z-index:2;pointer-events:none;
        background-image:radial-gradient(rgba(255,255,255,0.03) 1px,transparent 1px);
        background-size:3px 3px;"></div>"""

    stats_html = ""
    for bg, ct, num, desc in STATS:
        stats_html += f"""
<div style="display:flex;align-items:center;gap:18px;
     background:rgba(255,255,255,0.07);border:1.5px solid rgba(255,255,255,0.12);
     border-radius:14px;padding:16px 20px;">
  <div style="font-family:Inter;font-weight:700;font-size:42px;line-height:1;
              color:{bg};flex-shrink:0;min-width:100px;letter-spacing:-1px;">{num}</div>
  <div style="font-family:'DM Sans';font-weight:600;font-size:21px;
              color:rgba(255,255,255,0.82);line-height:1.35;flex:1;">{desc}</div>
</div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{f}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{width:1080px;height:1080px;overflow:hidden;}}
.c{{width:1080px;height:1080px;position:relative;overflow:hidden;
    background:linear-gradient(145deg,{DARK_NAVY} 0%,#1a2d50 100%);}}
.badge{{position:absolute;top:44px;right:44px;z-index:20;
    background:{AMBER};color:{DEEP_BLUE};
    padding:10px 22px;border-radius:50px;
    font-family:Inter;font-weight:700;font-size:13px;
    letter-spacing:2px;text-transform:uppercase;transform:rotate(4deg);
    box-shadow:0 6px 18px rgba(255,177,32,0.4);}}
.col{{position:absolute;top:44px;left:50px;right:530px;
    display:flex;flex-direction:column;gap:0;z-index:20;}}
.kicker{{font-family:'DM Sans';font-weight:700;font-size:20px;
    color:{AMBER};text-transform:uppercase;letter-spacing:4px;
    margin-top:108px;margin-bottom:10px;}}
.hl{{font-family:Inter;font-weight:700;font-size:58px;line-height:0.96;
    color:white;letter-spacing:-3px;margin-bottom:10px;}}
.hl em{{color:{AMBER};font-style:italic;}}
.sub{{font-family:'DM Sans';font-weight:600;font-size:20px;
    color:rgba(255,255,255,0.5);margin-bottom:20px;}}
.sub strong{{color:rgba(255,255,255,0.85);}}
.stats{{display:flex;flex-direction:column;gap:10px;}}
.url{{position:absolute;bottom:36px;left:50px;z-index:20;
    font-family:Inter;font-weight:700;font-size:18px;color:rgba(255,255,255,0.3);}}
</style></head><body><div class="c">
{GRAIN}
{LINKEDIN_SVG}
<img src="data:image/png;base64,{logo_b64}" style="position:absolute;top:44px;left:44px;height:66px;opacity:0.95;z-index:25;">
<div class="badge">Profile audit</div>
<div class="col">
  <div class="kicker">Your CV has moved online</div>
  <div class="hl">Your profile<br>is your<br><em>CV now.</em></div>
  <div class="sub">The numbers that <strong>prove it.</strong></div>
  <div class="stats">{stats_html}</div>
</div>
<div class="url">internwise.co.uk →</div>
</div></body></html>"""

    _render(html, os.path.join(campaign_dir, "statcard_linkedin.png"))
    print("Done - LinkedIn stat card v3 complete!")


if __name__ == "__main__":
    generate("campaigns/outputs/week4/d2-linkedin")
