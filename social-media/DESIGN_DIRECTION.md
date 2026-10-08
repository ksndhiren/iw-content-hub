# Internwise Design Direction

Last updated: 2026-09-29

This is the approved creative direction for future Internwise social graphics. Treat it as product memory: local tools, Codex agents, and any other generator must preserve this direction unless the user explicitly changes it.

## Approved Direction

- Designs should feel editorial, premium, and intentionally composed, not like a corporate SaaS template.
- Each post needs one clear visual idea, not a repeated layout with swapped text.
- Use expressive typography. Inter can stay for functional text, but hero words should use contrasting treatments such as Georgia serif italic, oversized scale, colour shifts, underlines, or isolated word placement.
- Design key words differently when they carry the meaning. Example: in "Is your cover letter too polite?", the word "Polite?" should be the visual hook, not just another word in the same font.
- Nuno must be relevant to the post topic. Use cover-letter poses for cover-letter content, CV poses for CV content, planning poses for workflow/search/process content, and avoid generic founder cutouts when the pose does not support the message.
- In a carousel, the CTA/outro Nuno pose must not reuse the hook/cover slide pose. CTA/outro poses must also be unique across education carousels within the same week, so two different carousel outros do not end on the same Nuno image. Treat hook and CTA as separate beats, not a repeated image. If only one perfect custom cutout exists, use it on the hook and use the cleanest relevant alternate on the CTA rather than repeating it.
- If a Nuno cutout has poor background removal, visible haloing, or crops hands/arms at the canvas edge, do not ship it. Pick a cleaner existing cutout or regenerate the asset before publishing.
- The laughing/welcoming LinkedIn cover pose and thumbs-up CTA pose are banned for education carousels. LinkedIn/profile topics must use a LinkedIn/profile-frame visual motif or another clearly profile-related treatment, never just a generic Nuno cutout.
- Fonts should not feel uniformly corporate. Mix type roles deliberately: Inter for UI/clarity, DM Sans for labels and small navigation, Georgia serif/italic for editorial emphasis and emotional words.
- Do not rely on dark navy panels, rounded cards, and Inter-only headlines as the default skin. If two posts in a week look like they came from the same template family, redesign one.
- Featured jobs can remain utility-led, but should still feel like a premium editorial/job poster, not a generic ad tile.
- Featured-job post descriptions/captions must not mention employer/company names. Keep the role title, field, location, format, duration, and direct Internwise job link.
- Featured-job descriptions must add useful context that is different from the text on the graphic. Do not repeat the graphic hook as the caption body.
- Featured jobs should publish to Google Business Profile when connected, because they are directly relevant local/candidate opportunities.
- The core week must render five reviewable graphics per weekday: News, Education, Quote, Employer, and Poll/Conversation. Featured jobs are a separate optional sixth lane and must not be used to make up the five.
- The fifth post is Poll/Conversation, not the old fun/meme lane and not a generic engagement filler. It must be useful, conversion-aware, and able to stand alone even if nobody comments: decision prompts, A/B choices, comparison prompts, save/apply nudges, or practical conversation starters.
- Every Poll/Conversation graphic must include a visible comment prompt such as `Comment A, B or C below` inside the image to encourage engagement, placed clear of options, faces, logos, and CTA text.
- Monday-level typography and highlighted-word treatment is the baseline for every day of the week, not a one-off. Tuesday-Friday should not fall back to plain corporate cards.
- Direction does not mean template. Do not copy the same diagonal split, Nuno placement, cream/plum palette, serif word treatment, or content blocks across the week. Each post needs a distinct layout metaphor: profile frame, scoreboard, notebook, desk/flatlay, pipeline, newspaper, proof board, checklist, quote poster, etc. If day cards look like siblings at thumbnail size, regenerate until they are visibly different.
- Every carousel must end with a true outro/CTA slide: explicit action text, `internwise.co.uk`, and CTA-first composition. The final slide cannot read like another content slide.
- Poll/Conversation posts must use a unique visual world per weekday. Do not force every poll through the same `decision` layout; use the design ledger and maintain at least five distinct poll worlds for a five-day week.
- LinkedIn/profile education posts must look like LinkedIn/profile content: profile frame, phone/social UI, or another clear social-profile motif. Do not use CV, cover-letter, portfolio-document, or generic laptop poses for LinkedIn topics. If no relevant Nuno pose exists, generate or request a new one instead of reusing an unrelated asset.
- Do not repeat Nuno inside a carousel unless the repeated appearance serves a different visual beat. Prefer graphic-led CTA slides for platform/profile topics so the final slide does not feel like the hook image recycled.

## News Direction

- News should look like a news article or newspaper page, not a generic briefing card.
- News is not generated by the weekly evergreen batch. It must be generated by the day-prior news job only, then scheduled for the next morning.
- Standard cadence is Mon-Fri. Weekend news is allowed only for an explicit temporary catch-up window, such as week18 ending Sunday 2026-10-04 after posting started late on Wednesday.
- Every generated news card must include one relevant editorial/news image. Use the approved repo/Codex news asset bank first when a matching asset exists; otherwise the unattended cloud workflow may use Pexels as a relevant, non-repeated fallback.
- If neither an approved asset nor a relevant unused Pexels image is available, the news build must fail instead of falling back to a text-only pull quote or an irrelevant/repeated image.
- Keep article cues: branded masthead, date, section label, headline hierarchy, byline row, columns, pull quote, and article texture.
- The approved news header is locked: Internwise blue band, large centered white Internwise logo, amber rule, then the article starts on newsprint.
- `JOB MARKET NEWS` sits centered inside a white strip with black rules. Do not add a repeated "Job Market Briefing" label above or below it.
- The news headline is centered and editorial; the byline row should read `THE INTERNWISE WIRE` only.
- Do not use fake volume/issue metadata such as `VOL. I` or `NO. 03`; it adds noise without improving trust.
- Make news more attractive through editorial hierarchy, stronger headline spacing, a useful sidebar, and one pull quote.
- The graphic is a short article-style front page; full source/detail continues in the caption.
- News article body, sidebar, and pull quote must never end mid-sentence or with ellipses. If the copy does not fit, shorten to complete sentences; do not clip with overflow.

## Quote Direction

- Quote graphics must include a real sourced author portrait as a low-opacity watermark. A typographic name/initials fallback is not acceptable for scheduled quote graphics.
- If a real author portrait is unavailable in `assets/quote_authors/`, the build must fail until the portrait is added or the quote is changed.
- Prefer cached cutout portraits from `assets/quote_authors/_cutout/` whenever available. If only a raw portrait exists, generate the cutout before final scheduling whenever practical.
- Keep the author portrait behind the quote as an atmospheric editorial layer; it should support the quote, not become a full-opacity sticker. Use the current +10% watermark-opacity lift as the baseline unless readability is harmed.
- Quote portrait opacity should stay faint enough that the copy remains dominant. Use the attached Abraham Lincoln reference only for the portrait-watermark feeling, not as a template to copy.

## Layout QA

- Before publishing or scheduling a weekly batch, run the overlap QA gate: `PYTHONPYCACHEPREFIX=/private/tmp/iw-pycache python3 social-media/tools/qa_week_graphics.py week18 --ack-overlap-review`.
- The QA gate must confirm five core posts per weekday: News, Education, Quote, Employer, and Poll/Conversation. Featured jobs are optional sixth posts only.
- The QA gate must fail on duplicate lanes per day, missing slide files, blank/tiny slide images, or quote posts without real author portraits.
- The QA gate produces an overlap contact sheet. Review it at dashboard thumbnail size and full size before acknowledging. If text overlaps faces, Nuno, logos, buttons, image edges, or decorative shapes, fix and rerender.
- Shapes may frame or sit behind images, but they must not slice through faces, hands, primary objects, or readable text. Highlight strokes must never pass through letters unless deliberately designed as an underline with enough clearance.
- Logos need clear contrast and breathing room. Do not place light logos on light images or let brand marks touch headlines.

## Publishing Rules

- Every Instagram feed post must have a matching Instagram Story companion for reach. The publisher should create Story jobs automatically; do not rely on a manual `--stories` flag.
- Facebook Stories should mirror Instagram Stories once a Facebook Page is connected in Ayrshare.

## Employer Direction

- Nuno must sit above the process/workflow visual layer when the concept implies him presenting or guiding the workflow.
- Process bars, checklist chips, and workflow graphics must sit behind Nuno or clear him entirely. They must never visually cover his face, torso, hands, or props.
- Employer graphics must always show `internwise.co.uk/employers`, with the footer kept clear of Nuno, logos, and CTA buttons.
- Logos cannot overlap headline/body text, and white logos must sit on dark/contrasting areas only.

## Topic Freshness

- Education topics, quote IDs/authors, and news stories are strict no-repeat surfaces. If the available bank cannot fill the week without a recent repeat, the build must fail instead of quietly recycling content.
- Poll/conversation ideas are also strict no-repeat surfaces across both current `engagement` posts and legacy `fun` posts. A format can return, but the hook/concept cannot. Do not source new fifth posts from the old `fun_ideas.json` bank.
- The Ayrshare posted ledger is the hard ignore list. Anything already sent or scheduled in `social-media/content/ayrshare_posted.json` must be treated as used forever for topic planning: education titles, quote IDs/authors, poll/conversation hooks, and news headlines cannot be selected again unless an explicit emergency override is set.
- The only allowed exception is an operator-visible emergency run with `IW_ALLOW_TOPIC_REPEAT=1`; do not leave that override set in normal local, cloud, or scheduled runs.

## Weekly Freshness

- The weekly design-freshness gate in `tools/design_ledger.py` is mandatory. Do not bypass it to ship stale designs.
- If the build fails because a lane lacks fresh worlds, author new worlds. Only use `IW_ALLOW_STALE_DESIGN=1` as an explicit emergency exception and tell the user.
- Quote content freshness is also mandatory: recent quote IDs/authors should not repeat just because the graphic style changed.
