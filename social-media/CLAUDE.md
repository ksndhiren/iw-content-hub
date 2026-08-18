# Social Media AI Agents Team — Job Board Brand

This file defines the architecture, agent roles, tools, and workflows for the social media AI agents team. Claude Code should use this as the source of truth when building, running, or extending the system.

---

## Project overview

An multi-agent system that autonomously produces social media content (copy, graphics, audio/video) for a job board brand. A central orchestrator plans campaigns and routes tasks to three specialist agents. All agents share a brand memory layer. Human review gates content before publishing.

---

## Repository structure

```
/
├── CLAUDE.md                   # This file — start here
├── .env                        # API keys (never commit)
├── agents/
│   ├── orchestrator.py         # Campaign planner + task router
│   ├── content_writer.py       # Caption, post copy, hashtags
│   ├── graphics_producer.py    # Image gen + template assembly
│   └── av_producer.py          # Voiceover + video assembly
├── tools/
│   ├── search.py               # Web search + trend API wrapper
│   ├── image_gen.py            # Image generation API wrapper
│   ├── tts.py                  # Text-to-speech wrapper
│   ├── video_gen.py            # Video assembly wrapper
│   ├── scheduler.py            # Social platform publisher
│   └── brand_memory.py         # Read/write shared brand context
├── memory/
│   ├── brand_guidelines.md     # Voice, tone, colors, logo rules
│   ├── past_posts.json         # Archive of published content
│   └── analytics.json          # Engagement data per post
├── templates/
│   ├── graphics/               # Brand-locked image templates
│   └── video/                  # Intro/outro, lower-third assets
├── campaigns/
│   └── briefs/                 # Input campaign brief files (.json)
└── tests/
    ├── test_orchestrator.py
    ├── test_content_writer.py
    ├── test_graphics_producer.py
    └── test_av_producer.py
```

---

## Environment variables

Create a `.env` file at the project root with:

```env
# Anthropic
ANTHROPIC_API_KEY=your_key_here

# Web search
SERPER_API_KEY=your_key_here         # or BRAVE_API_KEY

# Image generation
OPENAI_API_KEY=your_key_here         # for DALL-E 3
# STABILITY_API_KEY=your_key_here    # alternative: Stable Diffusion

# Audio / video
ELEVENLABS_API_KEY=your_key_here     # text-to-speech
RUNWAY_API_KEY=your_key_here         # video generation (optional)

# Social publishing
BUFFER_ACCESS_TOKEN=your_key_here    # or use platform SDKs directly
LINKEDIN_ACCESS_TOKEN=your_key_here
INSTAGRAM_ACCESS_TOKEN=your_key_here

# Memory store (optional: use Redis for production)
REDIS_URL=redis://localhost:6379
```

---

## Agent definitions

### Orchestrator agent

**File:** `agents/orchestrator.py`

**Model:** `claude-opus-4-5` (most capable — this agent does all the planning)

**Responsibilities:**
- Parse incoming campaign briefs
- Decompose into tasks for each specialist agent
- Enforce brand guidelines before dispatching
- Collect outputs from all specialists
- Trigger human review checkpoint
- Publish approved content via the scheduler

**System prompt:**

```
You are the orchestrator of a social media content team for a job board brand.
When given a campaign brief, you:
1. Identify the target platform(s), audience, and content goal
2. Break the campaign into tasks: copy task → graphics task → video task (run in parallel when possible)
3. Load brand guidelines from memory before routing any task
4. Review all specialist outputs for brand alignment before approval
5. Route approved content to the scheduler with correct platform metadata
6. Log the campaign outcome to memory for future reference

Always produce a structured task plan in JSON before dispatching agents.
Never publish without a human_approved: true flag in the content package.
```

**Input schema:**

```json
{
  "campaign_id": "string",
  "topic": "string",
  "platforms": ["linkedin", "instagram", "x", "tiktok"],
  "audience": "string",
  "goal": "awareness | engagement | conversion",
  "tone_override": "optional string",
  "publish_at": "ISO 8601 datetime or null"
}
```

**Output schema:**

```json
{
  "campaign_id": "string",
  "task_plan": [...],
  "content_package": {
    "copy": {...},
    "graphics": {...},
    "video": {...}
  },
  "human_approved": false,
  "publish_status": "draft | approved | published"
}
```

---

### Content writer agent

**File:** `agents/content_writer.py`

**Model:** `claude-sonnet-4-5`

**Responsibilities:**
- Generate platform-specific post copy (character limits enforced)
- Write hashtag sets (researched, not generic)
- Draft CTAs aligned to the campaign goal
- Adapt tone per platform (professional on LinkedIn, casual on Instagram/TikTok)
- Flag trending topics relevant to job market / hiring

**System prompt:**

```
You are a social media copywriter for a job board brand.
You write scroll-stopping content about jobs, careers, hiring trends, and workplace culture.
You always:
- Match tone to platform: formal on LinkedIn, punchy on X, conversational on Instagram/TikTok
- Keep copy within platform character limits (LinkedIn: 3000, X: 280, Instagram caption: 2200, TikTok caption: 2200)
- Include 3-5 relevant hashtags (researched, not generic)
- End with a clear CTA matched to the campaign goal
- Reference current job market data when available
- Never make up job statistics — only cite data from the search tool

Return output as structured JSON only.
```

**Tools available:**
- `search(query)` — web search for trends and job market data
- `get_brand_memory()` — load voice/tone guidelines
- `get_past_posts(platform, limit=10)` — avoid repeating recent content

**Output schema:**

```json
{
  "platform": "linkedin",
  "copy": "string",
  "hashtags": ["#RemoteWork", "#TechJobs"],
  "cta": "string",
  "char_count": 280,
  "tone": "professional | casual | inspirational"
}
```

**Platform character limits to enforce:**

| Platform  | Limit  |
|-----------|--------|
| LinkedIn  | 3000   |
| X         | 280    |
| Instagram | 2200   |
| TikTok    | 2200   |

---

### Graphics producer agent

**File:** `agents/graphics_producer.py`

**Model:** `claude-sonnet-4-5`

**Responsibilities:**
- Generate image prompts aligned to brand style
- Call image generation API (DALL-E 3 default)
- Select and populate correct template (stat card, job spotlight, banner)
- Output image files with correct platform dimensions
- Ensure logo placement and color compliance

**System prompt:**

```
You are a graphic design agent for a job board brand.
Given a content brief, you generate images and visual assets for social media.
You always:
- Load brand colors and style from memory before generating
- Write detailed image generation prompts that match brand aesthetics (clean, professional, modern)
- Select the correct template type for the content goal
- Enforce correct dimensions per platform
- Never use competitor logos or copyrighted visual styles
- Return structured metadata alongside each generated asset

Return output as structured JSON with asset paths and metadata.
```

**Tools available:**
- `generate_image(prompt, size)` — calls DALL-E 3 or Stable Diffusion
- `get_brand_memory()` — loads color palette, font rules, logo guidelines
- `apply_template(template_name, data)` — overlays text/data onto brand templates

**Platform dimensions:**

| Platform  | Format    | Size       |
|-----------|-----------|------------|
| LinkedIn  | Banner    | 1200×627   |
| Instagram | Square    | 1080×1080  |
| Instagram | Story     | 1080×1920  |
| X         | Card      | 1200×675   |
| TikTok    | Vertical  | 1080×1920  |

**Template types:**
- `stat_card` — a key metric or job market stat (e.g. "50K+ remote jobs this week")
- `job_spotlight` — a featured job listing with role, company, salary range
- `employer_spotlight` — a hiring company feature with logo and open roles
- `tip_card` — career advice or resume tip formatted as a visual list
- `carousel` — multi-slide format (LinkedIn/Instagram), up to 10 slides

**Output schema:**

```json
{
  "platform": "instagram",
  "template": "stat_card",
  "image_url": "string",
  "dimensions": "1080x1080",
  "alt_text": "string",
  "brand_compliant": true
}
```

---

### Audio/video producer agent

**File:** `agents/av_producer.py`

**Model:** `claude-sonnet-4-5`

**Responsibilities:**
- Write video scripts (hook → body → CTA, under 60s)
- Generate voiceover audio via ElevenLabs
- Assemble short-form videos (B-roll + captions + voiceover)
- Export in platform-correct format and length
- Add captions/subtitles for accessibility

**System prompt:**

```
You are a short-form video producer for a job board brand.
You create engaging 15-60 second videos for TikTok, Instagram Reels, and LinkedIn Video.
You always:
- Open with a strong hook in the first 3 seconds
- Keep scripts punchy: one idea per sentence, short sentences
- Match energy to platform (high energy TikTok, measured LinkedIn)
- Include on-screen text/captions for silent viewing
- End with a verbal and on-screen CTA
- Keep total video under 60 seconds (TikTok/Reels) or under 3 minutes (LinkedIn)

Return the script, voiceover cues, and assembly instructions as structured JSON.
```

**Tools available:**
- `generate_voiceover(script, voice_id)` — ElevenLabs TTS
- `generate_video(prompt, duration)` — RunwayML or similar
- `assemble_video(voiceover_path, video_path, captions)` — ffmpeg wrapper
- `get_brand_memory()` — load approved voice IDs and music tracks

**Video format specs:**

| Platform       | Aspect ratio | Max length | Format |
|----------------|--------------|------------|--------|
| TikTok         | 9:16         | 3 min      | MP4    |
| Instagram Reel | 9:16         | 90 sec     | MP4    |
| LinkedIn Video | 16:9 or 1:1  | 10 min     | MP4    |

**Output schema:**

```json
{
  "platform": "tiktok",
  "script": "string",
  "voiceover_url": "string",
  "video_url": "string",
  "duration_seconds": 45,
  "captions_srt": "string",
  "thumbnail_url": "string"
}
```

---

## Shared memory layer

**File:** `tools/brand_memory.py`

All agents call `get_brand_memory()` at the start of every task. The memory layer loads:

- `memory/brand_guidelines.md` — voice, tone, colors, logo rules, what to avoid
- `memory/past_posts.json` — last 30 published posts per platform
- `memory/analytics.json` — top performing post formats and topics

After publishing, the orchestrator writes the new post back to `past_posts.json` and updates `analytics.json`.

**Brand guidelines to populate (`memory/brand_guidelines.md`):**

```markdown
# Brand guidelines

## Voice and tone
- Professional but approachable
- Empowering — we help people find better opportunities
- Data-informed — cite real numbers when available
- Never salesy or pushy

## Visual identity
- Primary color: #1A1A2E (deep navy)
- Accent color: #E94560 (vibrant coral-red)
- Background: #F5F5F5 (light gray) or white
- Font: Inter (headings), DM Sans (body)
- Logo: always top-left or center, minimum 40px clear space

## Content pillars
1. Job market insights and trends
2. Career advice and tips
3. Featured remote / hybrid jobs
4. Employer spotlights
5. Community milestones (10K jobs posted, etc.)

## What to avoid
- Stereotypes about any industry, gender, or age group
- Exaggerated salary claims without sources
- Competitor mentions
- Political commentary
```

---

## Running a campaign

### 1. Create a brief

Save a file to `campaigns/briefs/` as JSON:

```json
{
  "campaign_id": "wk-2026-14-remote-tech",
  "topic": "Remote tech jobs are surging this week — highlight top categories",
  "platforms": ["linkedin", "instagram", "tiktok"],
  "audience": "software engineers and product managers, 25-40",
  "goal": "awareness",
  "tone_override": null,
  "publish_at": "2026-04-07T09:00:00Z"
}
```

### 2. Run the orchestrator

```bash
python agents/orchestrator.py --brief campaigns/briefs/wk-2026-14-remote-tech.json
```

### 3. Review outputs

Generated content lands in `campaigns/outputs/<campaign_id>/`:

```
campaigns/outputs/wk-2026-14-remote-tech/
├── copy_linkedin.json
├── copy_instagram.json
├── copy_tiktok.json
├── graphic_linkedin.png
├── graphic_instagram.png
├── video_tiktok.mp4
├── video_tiktok.srt
└── package_summary.json
```

### 4. Approve and publish

Open `package_summary.json`, review, set `"human_approved": true`, then:

```bash
python agents/orchestrator.py --publish campaigns/outputs/wk-2026-14-remote-tech/package_summary.json
```

---

## Dependencies

```txt
anthropic>=0.25.0
openai>=1.30.0
elevenlabs>=1.0.0
requests>=2.31.0
pillow>=10.0.0
ffmpeg-python>=0.2.0
python-dotenv>=1.0.0
redis>=5.0.0
pydantic>=2.0.0
```

Install:

```bash
pip install -r requirements.txt
```

---

## Testing

Run all agent tests:

```bash
pytest tests/ -v
```

Run a dry-run campaign (no API calls, uses mocked responses):

```bash
python agents/orchestrator.py --brief campaigns/briefs/example.json --dry-run
```

---

## Extending the team

To add a new specialist agent:

1. Create `agents/new_agent.py` following the same input/output schema pattern
2. Add its tool dependencies to `tools/`
3. Register it in the orchestrator's `AGENT_REGISTRY` dict
4. Add its output key to the content package schema
5. Write tests in `tests/test_new_agent.py`

---

## Notes for Claude Code

- Always read `memory/brand_guidelines.md` before generating any content or prompts
- Use `--dry-run` during development to avoid burning API credits
- The orchestrator is the only agent that writes to memory — specialists are read-only
- Human approval (`human_approved: true`) is a hard gate — do not bypass it in any script
- Log all errors to `campaigns/logs/<campaign_id>.log` for debugging
