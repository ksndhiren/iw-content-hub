"""
Internwise brand context for the brief-driven generator.
Provides the Claude API system prompt and per-slide user prompt builder.
"""

# ---------------------------------------------------------------------------
# System prompt — injected into every API call.
# {{FONTS_CSS}} is replaced with base64 font-face declarations before sending.
# {{LOGO_SRC}} is left as-is here; generate.py replaces it in the returned HTML.
# ---------------------------------------------------------------------------

BRAND_SYSTEM_PROMPT = """You are a visual HTML/CSS designer generating 1080x1080px Instagram carousel slides for Internwise (internwise.co.uk) — a UK Gen Z job board connecting students and graduates with internships and entry-level roles.

## Output format
Return ONLY a complete, self-contained HTML document. No explanation, no markdown, no code fences.
The HTML must be renderable by headless Chromium at a 1080x1080px viewport with device_scale_factor=2.

## Canvas
body { width:1080px; height:1080px; overflow:hidden; margin:0; padding:0; }
All positioned elements use position:absolute relative to the canvas div (position:relative).

## Fonts
Paste this exactly inside your <style> tag — do not modify it:
{{FONTS_CSS}}
Always use font-family:'Inter' for headlines, numbers, badges, labels.
Always use font-family:'DM Sans' for body copy, descriptors, insight text.

## Logo
When a slide needs the logo (hook and conclusion slides only), use exactly:
<img src="{{LOGO_SRC}}" style="position:absolute;top:44px;left:44px;height:72px;opacity:0.95;z-index:25;">
CRITICAL: Place this img tag directly inside the canvas div — never inside a parent div with position:absolute. Otherwise the logo double-positions itself and lands in the wrong place.
Content/sector slides use a numbered circle instead of the logo.

## Brand colours — use ONLY these hex values
Deep Blue:  #264D7E   primary backgrounds, card fills, borders
Dark Navy:  #162d4a   darkest backgrounds, neobrutalist shadow colour
Amber:      #FFB120   primary accent, CTAs, headline accents, kickers
Coral:      #FF6B6B   secondary accent, italic shadow colour
Purple:     #7B5CE6   tertiary accent
Mint:       #7FDBB6   fresh/positive accent
Off White:  #FAF5EC   light slide backgrounds
Light Blue: #5FA7E5   data/info accent

## Typography rules
- Headlines: Inter Bold, 80–180px, letter-spacing -3px to -8px, line-height 0.85–1.0
- Kickers: DM Sans Bold, 20–24px, UPPERCASE, letter-spacing 3–4px, colour Amber
- Body / labels: DM Sans Medium or Bold, 18–26px
- Fact values: Inter Bold, 18–22px, colour = slide accent colour
- Minimum font size anywhere: 14px

## Gen Z neobrutalist design rules
- Card borders and shadows: border:3px solid #162d4a; box-shadow:6px 6px 0 #162d4a; border-radius:16–22px
- Sticker badge (top-right): background Amber, colour Deep Blue, padding:12px 26px, border-radius:50px, font Inter Bold 15px UPPERCASE letter-spacing:2px, transform:rotate(3–5deg), box-shadow:0 8px 22px rgba(255,177,32,0.4)
- Grain texture on dark slides: background-image:radial-gradient(rgba(255,255,255,0.035) 1px,transparent 1px); background-size:3px 3px
- Sparkle SVG accents: small 4-pointed star SVGs at low opacity, scattered around
- Arch shape for photo/illustration zone: border-radius:230px 230px 40px 40px
- Left accent bar on content slides: position:absolute; top:0; left:0; width:6px; height:100%; background:[accent colour]; box-shadow:0 0 20px [accent colour]66
- Canvas must be DENSE — fill every zone, minimal dead space

## Slide-type layout rules

### hook
- Background: linear-gradient(145deg, #162d4a 0%, #1a2d50 100%)
- Logo img top-left (44,44,72px)
- Sticker badge top-right
- Kicker + massive headline top-left below logo (headline starts around top:170px)
- Visual (bar chart, tags, or illustration) fills right 40–50% of canvas
- Swipe hint tagline near bottom-left

### content / sector
- Background: linear-gradient(145deg, #162d4a 0%, #1a2d50 100%)
- NO logo — use numbered circle top-left: width/height 96px, border-radius 50%, background Amber, colour Deep Blue, Inter Bold 40px, transform:rotate(-5deg), box-shadow:0 10px 28px rgba(0,0,0,0.25), z-index:25
- Slide number label top-right (e.g. "02 / 06"), low opacity, Inter Bold 15px
- Left accent bar (6px wide, full height, accent colour)
- Tag pill top:130px left:50px — MUST be below logo area (logo bottom = top:44+72=116px; tag starts at 130px so there is no overlap)
- Sector/content name top:186px, Inter Bold 44px, right edge stops at ~right:440px
- Large value/range top:312px, Inter Bold 112px, accent colour, letter-spacing -5px
- Fact rows left side below large value, each row: semi-transparent dark card, border-left accent colour 3px, label DM Sans 19px rgba(white,0.7), value Inter Bold 20px accent colour
- Insight bottom-left, DM Sans 20px rgba(white,0.6), border-top separator
- URL bottom-right: internwise.co.uk, Inter Bold 16px, low opacity
- Visual fills bottom-right: arch shape (accent colour gradient bg) + illustration/SVG on top, OR neobrutalist stat block card

### conclusion
- Background: linear-gradient(145deg, #162d4a 0%, #1a3050 100%)
- Logo img top-left (44,44,72px)
- Sticker badge top-right
- Kicker + massive italic amber headline with coral text-shadow (6px 6px 0 #FF6B6B)
- 4-stat row (horizontal flex) around top:580px
- CTA pill full width near bottom: Deep Blue bg, white action text Inter Bold 26px, amber URL below it, amber arrow circle right
- Sparkle SVG accents scattered

### tipcard
- Top zone (~540px): dark navy/purple gradient, massive OWN IT-style headline, logo
- Bottom zone (~540px): Off White background, 4 tip cards
- Tip card: white bg, Deep Blue neobrutalist border+shadow, amber number circle (52px), emoji (34px), DM Sans Bold 25px text with one word in Coral Bold
- CTA card at very bottom: Deep Blue bg, white action text, amber URL, amber arrow circle

## Content rules
- Never mention specific company or brand names — use generic descriptors
- Never use em dashes (use commas, colons, or full stops instead)
- CTA URL always reads: internwise.co.uk →
- All text must come from the slide spec — never invent content
- No placeholder text, no lorem ipsum"""


# ---------------------------------------------------------------------------
# Per-slide prompt builder
# ---------------------------------------------------------------------------

def slide_prompt(slide: dict) -> str:
    """Convert a slide spec dict into a Claude user prompt."""
    stype = slide["type"]
    lines = [f"Create a 1080x1080px Instagram carousel slide.\n\nTYPE: {stype}\n"]

    # ── Shared top elements ─────────────────────────────────────────────────
    if "badge" in slide:
        lines.append(f"BADGE (sticker, top-right, amber, rotated): {slide['badge']}")
    if "kicker" in slide:
        lines.append(f"KICKER (small amber uppercase text above headline): {slide['kicker']}")
    if "headline" in slide:
        lines.append(f"HEADLINE: {slide['headline']}")
    if "headline_accent" in slide:
        lines.append(
            f"HEADLINE_ACCENT: Make '{slide['headline_accent']}' italic Amber "
            f"with text-shadow:4px 4px 0 #FF6B6B"
        )

    # ── Hook ────────────────────────────────────────────────────────────────
    if stype == "hook":
        visual = slide.get("visual", {})
        vtype = visual.get("type", "none")

        if vtype == "bar_chart":
            lines.append(
                "\nVISUAL: Horizontal salary bar chart, right 55% of canvas "
                "(position:absolute; top:440px; left:220px; right:50px)."
            )
            lines.append("Add a divider line and 'Ranked by sector' label above the bars.")
            lines.append("Each bar: dark semi-transparent track, coloured fill, salary text inside bar.")
            lines.append("\nBar rows (label | display value | fill% | bar colour):")
            for b in visual.get("bars", []):
                lines.append(f"  {b['label']} | {b['value']} | {b['pct']}% | {b['color']}")

        elif vtype == "tags":
            lines.append("\nVISUAL: Floating tag pills, right side, stacked vertically with slight rotations.")
            for tag in visual.get("tags", []):
                lines.append(f"  - {tag}")

        elif vtype == "stat":
            lines.append(
                f"\nVISUAL: Large centred stat — "
                f"number '{visual['number']}' Inter Bold 140px Amber, "
                f"label '{visual['label']}' DM Sans 26px white below"
            )

        elif vtype == "illustration":
            lines.append(
                f"\nVISUAL: SVG illustration in arch shape on right side "
                f"(border-radius:230px 230px 40px 40px, background {visual.get('bg_color','#FFB120')}).\n"
                f"Theme: {visual.get('theme','abstract professional')}. "
                f"Clean geometric SVG, no text, brand colours."
            )

        if "tagline" in slide:
            lines.append(f"\nTAGLINE (bottom-left, rgba(white,0.38), Inter Bold 20px): {slide['tagline']}")
            lines.append("Add 'Swipe hint' strong-tagged word in rgba(white,0.7).")

    # ── Content / Sector ────────────────────────────────────────────────────
    elif stype in ("content", "sector"):
        accent = slide.get("accent_color", "#FFB120")
        num    = slide.get("number", "1")
        lines.append(f"\nACCENT COLOUR: {accent}")
        lines.append(f"NUMBERED CIRCLE (top-left, replaces logo): number '{num}', 96px, Amber bg, Deep Blue text, rotate(-5deg)")
        lines.append(f"SLIDE NUMBER LABEL (top-right, low opacity): {slide.get('slide_num_label','')}")
        lines.append(f"LEFT BAR: 6px full-height bar, colour {accent}, with glow box-shadow")
        lines.append(f"\nTAG PILL (top:130px left:50px, BELOW logo zone): {slide.get('tag','')}")
        lines.append(f"CONTENT LABEL (top:186px, Inter Bold 44px, right edge ~right:440px): {slide.get('label','')}")
        lines.append(f"LARGE VALUE (top:312px, Inter Bold 112px, {accent}): {slide.get('range', slide.get('value',''))}")

        lines.append("\nFACT ROWS (left side, below large value, right edge ~right:450px):")
        for label, val in slide.get("facts", []):
            lines.append(f"  [{label}] [{val}]")
        lines.append("Each row: background rgba(255,255,255,0.06), border-radius:12px, border-left:3px solid accent, padding:13px 18px, margin-bottom:8px")
        lines.append(f"Label: DM Sans 19px rgba(white,0.7) | Value: Inter Bold 20px {accent}")

        if "insight" in slide:
            lines.append(f"\nINSIGHT (bottom-left, above url, border-top separator): {slide['insight']}")

        # Right-side visual
        visual = slide.get("visual", {"type": "stat_block"})
        vtype  = visual.get("type", "stat_block")

        if vtype == "illustration":
            lines.append(
                f"\nVISUAL RIGHT: Arch shape (bottom:20px right:20px, 400x500px, "
                f"border-radius:230px 230px 40px 40px, background linear-gradient {accent}99->{accent}). "
                f"SVG illustration on top (bottom:0 right:-10px, 480x620px).\n"
                f"Theme: {visual.get('theme','professional character')}. "
                f"Generate a clean SVG figure — use brand colours, no text, geometric style."
            )
        elif vtype == "stat_block":
            primary   = visual.get("primary",   slide.get("range", ""))
            secondary = visual.get("secondary", "")
            lines.append(
                f"\nVISUAL RIGHT: Neobrutalist stat card (340x380px, bottom:80px right:50px).\n"
                f"Background: {accent}. Border+shadow: 3px solid #162d4a / 10px 10px 0 #162d4a. Border-radius:28px.\n"
                f"Primary text: '{primary}' Inter Bold 22px {slide.get('accent_text','#264D7E')} UPPERCASE.\n"
                f"Divider line. Secondary text: '{secondary}' DM Sans 18px opacity 0.75.\n"
                f"Large number from range: {slide.get('range','').replace('£','').replace(',','')} — Inter Bold 72px."
            )

    # ── Conclusion ──────────────────────────────────────────────────────────
    elif stype == "conclusion":
        lines.append(
            "\nHEADLINE STYLE: massive (140–160px), Inter Bold, italic, "
            "Amber colour, text-shadow:6px 6px 0 #FF6B6B, letter-spacing:-6px"
        )
        if "stats" in slide:
            lines.append("\nSTATS ROW (4 cards, horizontal flex, top:~580px, gap:16px):")
            for s in slide["stats"]:
                lines.append(f"  num='{s['num']}' label='{s['label']}'")
            lines.append(
                "Card style: Deep Blue bg, border:3px solid Dark Navy, box-shadow:5px 5px 0 Dark Navy, "
                "border-radius:18px, text-align:center. "
                "num: Inter Bold 36px Amber. label: DM Sans 15px rgba(white,0.65) line-height 1.3."
            )
        cta = slide.get("cta", "Find your role")
        lines.append(
            f"\nCTA PILL (bottom:58px, left:60px, right:60px, Deep Blue bg, "
            f"border:3px solid Dark Navy, box-shadow:6px 6px 0 Dark Navy, border-radius:22px):\n"
            f"  Left: white text '{cta}' Inter Bold 26–28px, below it amber 'internwise.co.uk →' Inter Bold 18–20px.\n"
            f"  Right: Amber circle (68px) with Deep Blue arrow SVG."
        )

    # ── Tipcard ─────────────────────────────────────────────────────────────
    elif stype == "tipcard":
        bg = slide.get("bg", "dark")
        lines.append(f"\nCANVAS SPLIT:")
        lines.append("  TOP ZONE (height ~540px): dark navy/purple gradient background")
        lines.append("  BOTTOM ZONE (height ~540px): Off White #FAF5EC background")
        lines.append("  Curved divider between zones: Off White div with border-radius:50% 50% 0 0 / 100% 100% 0 0")
        if bg == "light":
            lines.append("  Logo: add CSS filter to make it dark-coloured")

        if "tips" in slide:
            lines.append(f"\nTIPS ({len(slide['tips'])} tip cards in bottom zone, gap:10px):")
            for i, tip in enumerate(slide["tips"], 1):
                bold = tip.get("bold", "")
                lines.append(
                    f"  {i}. emoji:{tip['emoji']} | text:{tip['text']}"
                    + (f" (make '{bold}' Coral Bold)" if bold else "")
                )
            lines.append(
                "Tip card style: white bg, border:3px solid Deep Blue, border-radius:18px, "
                "box-shadow:6px 6px 0 Deep Blue, padding:12px 18px, display:flex align-items:center gap:16px.\n"
                "Num circle: 52px Amber gradient bg, Deep Blue text Inter Bold 24px.\n"
                "Emoji: 34px. Text: DM Sans Bold 25px Deep Blue."
            )
        cta = slide.get("cta", "Find your role — internwise.co.uk →")
        lines.append(
            f"\nCTA (position:absolute bottom:24px, full width minus 44px margins, Deep Blue bg, "
            f"border:3px solid Dark Navy, box-shadow:5px 5px 0 Dark Navy, border-radius:18px):\n"
            f"  Action text: white Inter Bold 20px. URL below: Amber Inter Bold 17px 'internwise.co.uk →'.\n"
            f"  Amber arrow circle right side."
        )
        lines.append(f"\nFull CTA text: {cta}")

    # ── Fallback / custom ───────────────────────────────────────────────────
    else:
        if "content" in slide:
            lines.append(f"\nCONTENT:\n{slide['content']}")

    lines.append("\n\nReturn ONLY the complete HTML document. No explanation, no code fences.")
    return "\n".join(lines)
