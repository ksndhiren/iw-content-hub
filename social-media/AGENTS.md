# Internwise Social Media — Agent Handoff (AGENTS.md)

Instructions for any coding agent (Codex, etc.) continuing this project. Read this fully before building.
Internwise is a UK internship & graduate-jobs platform. We produce two content streams:
1. **Weekly graphics** — bespoke social carousels/singles (interactive build; this is the active work).
2. **Featured jobs** — fully automated daily (GitHub Actions scrapes internwise.co.uk → generates graphics → commits to the hub).

## Single repo layout
- **`/Users/abhishekutkarsha/Claude/iw-content-hub`** is the canonical project repo, pushed to GitHub `ksndhiren/iw-content-hub` and auto-deployed to Cloudflare Pages: iw-content-hub.pages.dev. It holds dashboard files (`data/weeks.json`, `data/featured.json`, `images/`) plus the featured jobs automation.
- **`/Users/abhishekutkarsha/Claude/iw-content-hub/social-media`** is this build workspace inside the dashboard repo: generators, assets, models, memory, docs, and local render outputs. Local secrets (`.env`, `.canva_tokens.json`, `secrets/`, `analytics/ig_token.txt`) must stay ignored and must never be committed or printed.
- Legacy note: `/Users/abhishekutkarsha/Claude/IW social media` was the old standalone build folder. Do not use it for new work unless explicitly asked.

## Rendering pipeline
Graphics are HTML/CSS/SVG rendered to PNG via **Playwright headless Chromium** at 1080×1080, `device_scale_factor=2` (→2160px). Fonts (Inter, DM Sans) are base64-embedded from `assets/fonts/`.
- Build a week: `python3 tools/wk12.py` → writes to `campaigns/outputs/week12/<post>/slide_N.png`.
- **Python 3.9 gotcha:** no backslashes inside f-string `{...}` expressions. Hoist strings with escaped quotes into variables, or use single-quote inner HTML attributes.

## Current state (as of 2026-08-18)
- **Week 12 D1 "The CV Clinic"** is BUILT and LIVE on the dashboard (5-slide carousel, `tools/wk12.py`). It is the template for the week.
- **Week 12 D1–D5 are all BUILT**, each a distinct design world (see above), wired into the dashboard. Weekly mix = **3 carousels + 2 singles**; Nuno features in the carousels only.

## The Nuno system (founder as the face)
From Week 12, weekly graphics feature the founder **Nuno** instead of stock photos. AI clones generated in Google Gemini (identity-consistent, from a fixed reference) live in `~/Downloads/Nuno Pictures/` (`Solo/`, `Situational/`, `Full Scene/`). Cutouts are pre-processed into `assets/nuno/*.png` (a vetted library — pick the best pose per slide topic; no live gen).
**Cutout pipeline = `tools/nuno_cutout.py`** `cutout(src,dst)`:
`FSRCNN x4 super-res` (OpenCV `cv2.dnn_superres`, `models/FSRCNN_x4.pb`) → `rembg` → crop to bbox → tonal (**Shadows −30% deepen, Highlights 0%**) → **downscale** to 1700px (LANCZOS) → UnsharpMask (~110%) → alpha edge clean (MinFilter erode 1px + GaussianBlur 0.6). SR runs locally ~0.7s/image; x4-then-downscale = crisp. Requires `opencv-contrib-python` (cv2 5.x has `dnn_superres`).
- Use Nuno only in carousel posts. Do not use Nuno in single posts.
- On **dark backgrounds**, give Nuno depth with a soft grounding drop-shadow only — NOT a glow, NOT a brightness lift, NOT a separation shadow (all rejected by the client).
- Consent: founder's own likeness, he drives it — authorised.

## Design rules (NON-NEGOTIABLE — client feedback)
- **Brand:** navy `#0E2141` / deep `#0A1830`, amber `#FFB120`, coral `#FF6B6B`, green `#41D98A`, ink `#EAF2FB`, muted `#93AAC9`. Real logo = `branding/PNG/IW.com_Horizontal_white logo.png` (cap+bulb wordmark). Icon-only mark for watermarks = `assets/iw_icon_mark.svg`.
- **Logo:** uniform **100px** height on every weekly design. Featured: ~80–90px.
- **Mobile fonts:** graphics viewed on ~6" phones — body text ≥ **30px**, labels/captions ≥ **22px** on the 1080 canvas.
- **CTA:** graphic shows the **URL only** (`internwise.co.uk`). NEVER put "link in bio" on the graphic (it posts to all platforms). "link in bio" goes ONLY in the IG/FB + TikTok **caption**. LinkedIn/X captions keep the clickable URL.
- **No em dashes** anywhere (use "-"). **No mid-word hyphenation** in headlines (`word-break:keep-all`).
- **Bespoke art directions** — real CSS/SVG devices, never plain gradient+text.
- **Distinct design language per post** (pitch topics + languages together first).
- **Composition, not a template.** The gpt-image-2 study taught COMPOSITION only: clear hierarchy, a subject + a topic-specific device, icon-badge lists, an eyebrow+underline, a progress counter, a brand footer, a URL pill. **Every post gets its OWN design language** - a distinct palette, background and device. NEVER clone one post's skin onto another. Week 12 proves it: D1 dark-navy/CV-scan, D2 cream index-cards/teal, D3 coral sunrise/welcome-pass, D4 deep-ocean/iceberg, D5 plum/reset-line. Reusable helpers (`svg/ic`, per-post `bg/head/eyebrow/footer/list/nuno`) live in `tools/wk12.py`, but their colours/shapes are re-authored per post.
- **Empty-space watermark:** fill any slide that is ≥50% empty with a large faint `iw_icon_mark.svg` bleeding off the bottom-right (~5% opacity); skip full slides.
- **Align with flex rows**, not guessed absolute pixel offsets.

## weeks.json schema (dashboard)
Each week: `{id:"week12", label:"Week 12", weekCommencing:"2026-08-17", posts:[...]}`. Dashboard sorts newest week first (landing default). Post:
```
{id, day, title, platform:"Multi-Platform", format:"Carousel"|"Single",
 slides:["slide_1.png",...], status:"in-review",
 caption:<ig-fb>, captionThread:[...5 tweets, carousels only], hashtags:[...ig-fb],
 captions:{"ig-fb":..,"linkedin":..[,"x":.. for singles]},
 hashtagsByPlatform:{"ig-fb":[],"linkedin":[],"x":[]}}
```
Carousels use `captionThread` (one tweet per slide, each <280 chars) for X; singles use `captions.x`.

## Publish a post to the dashboard
1. Render (`python3 tools/wk12.py`), QA the PNGs.
2. Copy from this folder to the dashboard images folder: `cp campaigns/outputs/week12/<post>/slide_*.png ../images/week12/<post>/`.
3. Add/patch `../data/weeks.json` with per-platform captions.
4. In the repo root (`/Users/abhishekutkarsha/Claude/iw-content-hub`): `git add -A images/week12 data/weeks.json social-media && git commit && git pull --rebase && git push`. End commit messages with `Co-Authored-By:` as the client prefers; do NOT push unless asked.

## Featured jobs (automated — usually leave alone)
`iw-content-hub/automation/`: `sync_featured_jobs.py` (daily 06:00 UTC scrape+generate), `featured_job.py` (generator; `SECTOR_STYLES` = one distinct colour per sector — every sector must be visually distinct; regenerate committed images if a colour changes, they don't auto-recolour), `prune_approved.py` (daily 12:00 UTC removes approved/published posts). Mirror of `featured_job.py` also in `tools/`. Set `IW_BRANDING_DIR`/`IW_FONTS_DIR` env vars (to `automation/branding` and `automation/assets/fonts`) when running the generator standalone, or the logo+fonts break.

## Secrets (never commit / never print)
`.env`, `.canva_tokens.json`, `secrets/`, `analytics/ig_token.txt` (local, gitignored). OpenAI key + model (`gpt-image-2`) are in `~/Downloads/Secrets-Open AI.docx` (a one-off image-gen test lives in `tools/openai_carousel_test.py`; the HTML pipeline is the production path — image-gen was study-only, its logo/brand were invented).
