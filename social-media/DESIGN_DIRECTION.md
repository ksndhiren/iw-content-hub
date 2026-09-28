# Internwise Design Direction

Last updated: 2026-09-28

This is the approved creative direction for future Internwise social graphics. Treat it as product memory: local tools, Codex agents, and any other generator must preserve this direction unless the user explicitly changes it.

## Approved Direction

- Designs should feel editorial, premium, and intentionally composed, not like a corporate SaaS template.
- Each post needs one clear visual idea, not a repeated layout with swapped text.
- Use expressive typography. Inter can stay for functional text, but hero words should use contrasting treatments such as Georgia serif italic, oversized scale, colour shifts, underlines, or isolated word placement.
- Design key words differently when they carry the meaning. Example: in "Is your cover letter too polite?", the word "Polite?" should be the visual hook, not just another word in the same font.
- Nuno must be relevant to the post topic. Use cover-letter poses for cover-letter content, CV poses for CV content, planning poses for workflow/search/process content, and avoid generic founder cutouts when the pose does not support the message.
- Fonts should not feel uniformly corporate. Mix type roles deliberately: Inter for UI/clarity, DM Sans for labels and small navigation, Georgia serif/italic for editorial emphasis and emotional words.
- Do not rely on dark navy panels, rounded cards, and Inter-only headlines as the default skin. If two posts in a week look like they came from the same template family, redesign one.
- Featured jobs can remain utility-led, but should still feel like a premium editorial/job poster, not a generic ad tile.

## News Direction

- News should look like a news article or newspaper page, not a generic briefing card.
- Keep article cues: branded masthead, date, section label, headline hierarchy, byline row, columns, pull quote, and article texture.
- The approved news header is locked: Internwise blue band, large centered white Internwise logo, amber rule, then the article starts on newsprint.
- `JOB MARKET NEWS` sits centered inside a white strip with black rules. Do not add a repeated "Job Market Briefing" label above or below it.
- The news headline is centered and editorial; the byline row should read `THE INTERNWISE WIRE` only.
- Do not use fake volume/issue metadata such as `VOL. I` or `NO. 03`; it adds noise without improving trust.
- Make news more attractive through editorial hierarchy, stronger headline spacing, a useful sidebar, and one pull quote.
- The graphic is a short article-style front page; full source/detail continues in the caption.

## Topic Freshness

- Education topics, quote IDs/authors, and news stories are strict no-repeat surfaces. If the available bank cannot fill the week without a recent repeat, the build must fail instead of quietly recycling content.
- The only allowed exception is an operator-visible emergency run with `IW_ALLOW_TOPIC_REPEAT=1`; do not leave that override set in normal local, cloud, or scheduled runs.

## Weekly Freshness

- The weekly design-freshness gate in `tools/design_ledger.py` is mandatory. Do not bypass it to ship stale designs.
- If the build fails because a lane lacks fresh worlds, author new worlds. Only use `IW_ALLOW_STALE_DESIGN=1` as an explicit emergency exception and tell the user.
- Quote content freshness is also mandatory: recent quote IDs/authors should not repeat just because the graphic style changed.
