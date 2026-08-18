"""
Internwise — Programmatic Graphics Generator
Generates brand-compliant social media graphics using Pillow.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import json

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
BRANDING_DIR = os.path.join(BASE_DIR, "branding")
OUTPUT_DIR = os.path.join(BASE_DIR, "campaigns", "outputs")

# ── Brand Colors ───────────────────────────────────────────────────────
NAVY = (26, 26, 46)           # #1A1A2E
CORAL = (233, 69, 96)         # #E94560
LIGHT_GREY = (245, 245, 245)  # #F5F5F5
WHITE = (255, 255, 255)
DARK_TEXT = (26, 26, 46)
CORAL_SOFT = (233, 69, 96, 40)  # Translucent coral for accents

# ── Platform Dimensions ───────────────────────────────────────────────
PLATFORM_SIZES = {
    "instagram":       (1080, 1080),
    "instagram_story": (1080, 1920),
    "linkedin":        (1200, 627),
    "x":               (1200, 675),
    "tiktok":          (1080, 1920),
}

# ── Font Loader ────────────────────────────────────────────────────────
def load_font(name, size):
    """Load a font by name and size. Falls back to default if not found."""
    font_map = {
        "inter-bold":      "Inter-Bold.ttf",
        "inter-semibold":  "Inter-SemiBold.ttf",
        "inter-medium":    "Inter-Medium.ttf",
        "inter-regular":   "Inter-Regular.ttf",
        "dmsans-bold":     "DMSans-Bold.ttf",
        "dmsans-medium":   "DMSans-Medium.ttf",
        "dmsans-regular":  "DMSans-Regular.ttf",
    }
    font_file = font_map.get(name.lower(), "Inter-Regular.ttf")
    font_path = os.path.join(FONTS_DIR, font_file)
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        print(f"  ⚠ Font {font_path} not found, using default")
        return ImageFont.load_default()

# ── Drawing Helpers ────────────────────────────────────────────────────
def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_pill_badge(draw, text, center_x, y, font, text_color, bg_color, padding_h=20, padding_v=8):
    """Draw a pill-shaped badge with text."""
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x1 = center_x - tw // 2 - padding_h
    y1 = y
    x2 = center_x + tw // 2 + padding_h
    y2 = y + th + padding_v * 2
    draw.rounded_rectangle((x1, y1, x2, y2), radius=(y2 - y1) // 2, fill=bg_color)
    draw.text((center_x - tw // 2, y + padding_v), text, fill=text_color, font=font)
    return y2

def draw_step_card(draw, number, title, description, x, y, width,
                   num_font, title_font, desc_font, accent_color, is_last=False):
    """Draw a numbered step card with circle number, title, and description."""
    circle_r = 22
    circle_cx = x + circle_r
    circle_cy = y + circle_r

    # Number circle
    draw.ellipse(
        (circle_cx - circle_r, circle_cy - circle_r,
         circle_cx + circle_r, circle_cy + circle_r),
        fill=accent_color
    )
    # Number text centered in circle
    nbbox = num_font.getbbox(number)
    nw = nbbox[2] - nbbox[0]
    nh = nbbox[3] - nbbox[1]
    draw.text((circle_cx - nw // 2, circle_cy - nh // 2 - 2), number, fill=WHITE, font=num_font)

    # Title
    text_x = x + circle_r * 2 + 18
    draw.text((text_x, y + 2), title, fill=WHITE, font=title_font)

    # Description
    title_bbox = title_font.getbbox(title)
    desc_y = y + (title_bbox[3] - title_bbox[1]) + 10

    # Word wrap description
    words = description.split()
    lines = []
    current = ""
    max_w = width - (circle_r * 2 + 18) - 10
    for word in words:
        test = f"{current} {word}".strip()
        if desc_font.getbbox(test)[2] - desc_font.getbbox(test)[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    for line in lines:
        draw.text((text_x, desc_y), line, fill=(200, 200, 210), font=desc_font)
        desc_y += (desc_font.getbbox(line)[3] - desc_font.getbbox(line)[1]) + 6

    # Connector line (if not last)
    if not is_last:
        line_top = circle_cy + circle_r + 4
        line_bottom = line_top + 20
        draw.line((circle_cx, line_top, circle_cx, line_bottom), fill=(80, 80, 110), width=2)
        return desc_y + 20

    return desc_y + 10

def add_logo(img, position="top-left", max_height=40):
    """Overlay the Internwise logo on the image."""
    logo_path = os.path.join(BRANDING_DIR, "PNG", "Internwise.Com-Horizontal logo.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(BRANDING_DIR, "PNG", "Internwise.Com logo.png")
    if not os.path.exists(logo_path):
        print("  ⚠ Logo not found, skipping")
        return img

    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo proportionally
    ratio = max_height / logo.height
    new_w = int(logo.width * ratio)
    logo = logo.resize((new_w, max_height), Image.LANCZOS)

    margin = 40
    w, h = img.size

    if position == "top-left":
        pos = (margin, margin)
    elif position == "top-center":
        pos = ((w - new_w) // 2, margin)
    elif position == "bottom-center":
        pos = ((w - new_w) // 2, h - max_height - margin)
    elif position == "bottom-left":
        pos = (margin, h - max_height - margin)
    else:
        pos = (margin, margin)

    img.paste(logo, pos, logo)
    return img

def add_social_icon(img, position="bottom-right", size=36):
    """Overlay the IW social icon."""
    icon_path = os.path.join(BRANDING_DIR, "Social Icons", "IW.Com-Social Icon 01.jpg")
    if not os.path.exists(icon_path):
        return img

    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize((size, size), Image.LANCZOS)

    margin = 40
    w, h = img.size

    if position == "bottom-right":
        pos = (w - size - margin, h - size - margin)
    elif position == "bottom-left":
        pos = (margin, h - size - margin)

    img.paste(icon, pos, icon)
    return img

# ── Template: Tip Card ─────────────────────────────────────────────────
def generate_tip_card(platform, tag_text, title, steps, cta_text,
                      campaign_id, bg_color=NAVY):
    """
    Generate a tip card graphic.

    Args:
        platform: "instagram", "linkedin", "x", "tiktok"
        tag_text: Small pill badge text (e.g. "INTERVIEW TIP")
        title: Main heading in quotes
        steps: List of dicts with 'title' and 'description'
        cta_text: Call to action text at bottom
        campaign_id: For output file naming
    """
    width, height = PLATFORM_SIZES[platform]
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # ── Decorative elements ──
    # Subtle gradient overlay at top
    for i in range(min(200, height)):
        alpha = int(15 * (1 - i / 200))
        draw.line((0, i, width, i), fill=(CORAL[0], CORAL[1], CORAL[2], alpha))

    # Corner accent — subtle coral arc top-right
    draw.arc((width - 300, -150, width + 150, 300), 180, 270, fill=(*CORAL, 30), width=3)

    # ── Scale fonts based on platform ──
    is_tall = platform in ("tiktok", "instagram_story")
    is_wide = platform in ("linkedin", "x")

    if is_tall:
        tag_size, title_size, step_title_size, step_desc_size, num_size, cta_size = 22, 44, 24, 18, 20, 18
        margin_x = 80
        start_y = height // 6
    elif is_wide:
        tag_size, title_size, step_title_size, step_desc_size, num_size, cta_size = 16, 32, 20, 15, 16, 14
        margin_x = 60
        start_y = 50
    else:  # instagram square
        tag_size, title_size, step_title_size, step_desc_size, num_size, cta_size = 18, 38, 22, 16, 18, 15
        margin_x = 70
        start_y = 80

    # Load fonts
    tag_font = load_font("inter-semibold", tag_size)
    title_font = load_font("inter-bold", title_size)
    step_title_font = load_font("inter-semibold", step_title_size)
    step_desc_font = load_font("dmsans-regular", step_desc_size)
    num_font = load_font("inter-bold", num_size)
    cta_font = load_font("dmsans-medium", cta_size)

    center_x = width // 2
    content_width = width - margin_x * 2

    # ── Tag badge ──
    y = start_y
    badge_bottom = draw_pill_badge(
        draw, tag_text, center_x, y, tag_font,
        text_color=WHITE, bg_color=CORAL, padding_h=24, padding_v=10
    )

    # ── Title ──
    y = badge_bottom + 25
    # Center the title, handle multi-line
    title_lines = []
    words = title.split()
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = title_font.getbbox(test)
        if bbox[2] - bbox[0] <= content_width:
            current = test
        else:
            if current:
                title_lines.append(current)
            current = word
    if current:
        title_lines.append(current)

    for line in title_lines:
        bbox = title_font.getbbox(line)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        draw.text((center_x - lw // 2, y), line, fill=WHITE, font=title_font)
        y += lh + 8

    # ── Divider line ──
    y += 15
    div_w = min(120, content_width // 3)
    draw.line((center_x - div_w // 2, y, center_x + div_w // 2, y), fill=CORAL, width=3)
    y += 25

    # ── Subtitle: "The Magic Formula" ──
    subtitle_font = load_font("inter-medium", step_title_size + 2)
    subtitle = "The Magic Formula"
    sbbox = subtitle_font.getbbox(subtitle)
    sw = sbbox[2] - sbbox[0]
    draw.text((center_x - sw // 2, y), subtitle, fill=CORAL, font=subtitle_font)
    y += (sbbox[3] - sbbox[1]) + 30

    # ── Step cards ──
    for i, step in enumerate(steps):
        y = draw_step_card(
            draw, str(i + 1), step["title"], step["description"],
            margin_x, y, content_width,
            num_font, step_title_font, step_desc_font,
            CORAL, is_last=(i == len(steps) - 1)
        )

    # ── CTA at bottom ──
    y = max(y + 20, height - 120)
    # CTA background bar
    draw.rounded_rectangle(
        (margin_x, y, width - margin_x, y + 50),
        radius=25, fill=CORAL
    )
    cbbox = cta_font.getbbox(cta_text)
    cw = cbbox[2] - cbbox[0]
    ch = cbbox[3] - cbbox[1]
    draw.text((center_x - cw // 2, y + 25 - ch // 2), cta_text, fill=WHITE, font=cta_font)

    # ── Logo ──
    logo_h = 30 if is_wide else 35
    logo_pos = "bottom-center" if is_tall else "bottom-left"
    img = add_logo(img, position=logo_pos, max_height=logo_h)

    # ── Watermark / handle ──
    handle_font = load_font("dmsans-regular", 13)
    handle = "@internwise"
    hbbox = handle_font.getbbox(handle)
    hw = hbbox[2] - hbbox[0]
    draw.text((width - hw - 40, height - 30), handle, fill=(120, 120, 140), font=handle_font)

    # ── Save ──
    output_dir = os.path.join(OUTPUT_DIR, campaign_id)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"graphic_{platform}.png")
    img.save(output_path, "PNG", quality=95)
    print(f"  ✓ {platform}: {output_path} ({width}×{height})")
    return output_path


# ── Main: Generate campaign graphics ───────────────────────────────────
def generate_campaign_graphics(campaign_id, tag_text, title, steps, cta_text,
                                platforms=None):
    """Generate tip card graphics for all specified platforms."""
    if platforms is None:
        platforms = ["instagram", "linkedin", "x", "tiktok"]

    print(f"\n🎨 Generating graphics for campaign: {campaign_id}")
    print(f"   Topic: {title}")
    print(f"   Platforms: {', '.join(platforms)}\n")

    results = {}
    for platform in platforms:
        path = generate_tip_card(
            platform=platform,
            tag_text=tag_text,
            title=title,
            steps=steps,
            cta_text=cta_text,
            campaign_id=campaign_id
        )
        results[platform] = {
            "path": path,
            "dimensions": f"{PLATFORM_SIZES[platform][0]}×{PLATFORM_SIZES[platform][1]}",
            "format": "PNG"
        }

    # Save manifest
    manifest_path = os.path.join(OUTPUT_DIR, campaign_id, "graphics_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  📋 Manifest: {manifest_path}")

    return results


if __name__ == "__main__":
    # ── Tell Me About Yourself — Magic Formula ──
    CAMPAIGN_ID = "candidate-tmay-magic-formula"

    steps = [
        {
            "title": "PRESENT",
            "description": "Start with who you are right now. Your degree, your current focus, and what drives you."
        },
        {
            "title": "PAST",
            "description": "Briefly share the experience that led you here — a project, internship, or skill you built."
        },
        {
            "title": "FUTURE",
            "description": "Connect it to this role. Why this company? Why now? Show them you've done your research."
        }
    ]

    generate_campaign_graphics(
        campaign_id=CAMPAIGN_ID,
        tag_text="INTERVIEW TIP",
        title='"Tell me about yourself"',
        steps=steps,
        cta_text="Find your next internship → internwise.com",
        platforms=["instagram", "linkedin", "x", "tiktok"]
    )
