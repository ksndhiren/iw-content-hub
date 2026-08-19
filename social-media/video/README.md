# Internwise Shorts/Reels Script Pipeline

This folder is for short-form video topic discovery, planning, and script generation. HeyGen rendering is intentionally manual for now.

## Goal
Create review-ready scripts for TikTok, Instagram Reels, YouTube Shorts, and LinkedIn short video.

The pipeline stops before video generation:
1. Collect hands-free topic signals.
2. Score topics for short-form potential.
3. Generate scene-by-scene Nuno-led scripts.
4. Export JSON handoffs, Markdown production briefs, and dashboard-ready `data/shorts.json`.

## Hands-Free Topic Engine
Run from `social-media/`:

```bash
python3 tools/shorts_topic_engine.py
```

The source config lives at `video/topic_sources.json`.

Active sources:
- Reddit pain points through public RSS feeds.
- Configured search-question seeds.
- Google Trends through `pytrends` if installed.
- Google Trends through SerpApi if `SERPAPI_API_KEY` is set.
- YouTube competitor breakout detection if `YOUTUBE_API_KEY` is set.

Useful dry-run:

```bash
python3 tools/shorts_topic_engine.py --offline
```

Output:
- `video/topics/auto.json`
- `video/scripts/<auto-date>/<topic-id>/script.json`
- `video/scripts/<auto-date>/<topic-id>/brief.md`
- `../data/shorts.json`

## Viral Selection Rules
No one can guarantee virality. The system optimises for conditions that make sharing and retention more likely:
- **Pain:** the topic names a real student/graduate anxiety.
- **Specificity:** the hook is concrete, not generic career advice.
- **Curiosity gap:** the viewer wants the missing answer.
- **Practical payoff:** the viewer gets a usable next step within 45 seconds.
- **Safe contrarian angle:** challenges bad advice without dunking on candidates.
- **Comment potential:** invites disagreement, confession, or tagging a friend.
- **Save/share utility:** includes a checklist, phrase, template, or mental model.
- **Brand fit:** warm, mentor-like, no overpromising, no competitor mentions.

## Manual HeyGen Flow
For each generated brief:
1. Open HeyGen.
2. Choose the approved founder/avatar.
3. Set format to vertical 9:16.
4. Paste the `spoken_script`.
5. Generate each scene separately because HeyGen single scenes are capped at 15 seconds.
6. Export MP4.
7. Save the video in the matching output folder when ready.

Recommended starting length: 45-55 seconds. Do not add on-screen text inside the HeyGen scenes. Add platform-native captions after upload if needed.
