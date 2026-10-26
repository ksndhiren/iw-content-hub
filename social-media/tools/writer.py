"""Daily-5 writer - LLM copywriting for on-screen text + captions.

Turns sourced content (an RSS item, a quote, a fun idea, an employer angle, or an
education topic) into brand-safe copy: reworded news, per-platform captions,
education carousel slides. All brand rules live in SYSTEM so every call obeys
them. Used by the build step; runs unattended in the cloud (needs OPENAI_API_KEY).

    from writer import write_news, write_captions, write_education, write_topic_angles
"""
import os, json, sys, re

MODEL = os.getenv("OPENAI_MODEL") or "gpt-4o"   # empty-string safe (cloud var may be unset)

SYSTEM = """You are the copywriter for Internwise, a UK internship & graduate-jobs platform.
Audience: UK students and recent graduates (and, for the employer lane, UK hiring managers).
Voice: warm, encouraging, mentor-like, plain English, credible. Never salesy or hype.
Write with warmth and momentum: short punchy sentences, concrete specifics, speak directly to the reader as "you". Sound like a switched-on older friend who has your back - not a press release. Avoid corporate filler, buzzwords and cliches ("in today's competitive landscape", "unlock your potential", "game-changer").

NON-NEGOTIABLE BRAND RULES:
- NEVER use em dashes or en dashes. Use a hyphen "-" or rephrase.
- Internwise believes ALL internships should be PAID. Never frame paid-vs-unpaid as a debate or as acceptable; never write "when should an internship be paid" style content.
- Never invent statistics. Only use numbers that are given to you in the input. If a number is not provided, do not state one.
- For NEWS: never copy the source's exact wording. Reword everything in Internwise's own voice (this is anti-plagiarism). Keep every fact accurate to the input. Do not add facts that are not in the input.
- The on-screen graphic shows the website URL only. Never put "link in bio" on the graphic text.
- "link in bio" belongs ONLY in the Instagram/Facebook caption. LinkedIn and X captions keep the clickable URL "internwise.co.uk".
- No stereotypes, no politics, no competitor names (except real "trusted by" brands supplied to you), no exaggerated claims.
- British spelling.

Respond with a single valid JSON object and nothing else."""


def _client():
    from openai import OpenAI
    return OpenAI()   # reads OPENAI_API_KEY from env


def _lc_hashtags(obj):
    """Force every generated hashtag to lowercase (#techjobs, never #TechJobs).
    Brand rule: on-screen + caption hashtags stay lowercase. Applied to every
    writer output so no capitalised tag ever reaches weeks.json."""
    def lc(t):
        return "#" + t[1:].lower() if isinstance(t, str) and t.startswith("#") else t
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "hashtags":
                if isinstance(v, list):
                    obj[k] = [lc(x) for x in v]
                elif isinstance(v, dict):
                    for pk, pv in v.items():
                        if isinstance(pv, list):
                            v[pk] = [lc(x) for x in pv]
            else:
                _lc_hashtags(v)
    elif isinstance(obj, list):
        for x in obj:
            _lc_hashtags(x)
    return obj


# Brand rule (feedback): never write "paid"/"unpaid" next to internship/opportunity/
# role/job wording - Internwise says just "internship". The system prompt asks for
# this, but the LLM still slips "paid internships" into CTAs, so we scrub every
# output deterministically as a hard backstop.
_PAID_ADJ = re.compile(r"\b(?:un)?paid\s+(?=intern|opportunit|role|position|job|vacanc|placement|work\b)", re.I)
_PAID_POST = re.compile(r"\s*[,-]?\s*(?:that are|which are|are|is|and)\s+(?:un)?paid\b", re.I)


def _scrub_text(s):
    if not isinstance(s, str):
        return s
    s = _PAID_ADJ.sub("", s)
    s = _PAID_POST.sub("", s)
    return re.sub(r"  +", " ", s)


def _scrub(obj):
    """Recursively strip paid/unpaid-vs-internship wording from every string."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = _scrub(v)
    elif isinstance(obj, list):
        return [_scrub(x) for x in obj]
    else:
        return _scrub_text(obj)
    return obj


def _chat(user, max_tokens=900):
    resp = _client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=max_tokens,
    )
    return _scrub(_lc_hashtags(json.loads(resp.choices[0].message.content)))


# The LLM occasionally returns a news object with a top-level key missing - most
# often "hashtags", which crashed the whole daily news build (KeyError) even
# though every other field was fine. Retry once, then patch the cosmetic keys
# from brand defaults; only the keys that are actually rendered are fatal.
NEWS_REQUIRED = ("headline", "brief", "sidebar", "pull", "captions", "hashtags")
NEWS_RENDERED = ("headline", "brief", "sidebar", "pull", "captions")
NEWS_FALLBACK_HASHTAGS = {
    "ig-fb": ["#internwise", "#ukjobs", "#graduatejobs", "#internships", "#earlycareers"],
    "linkedin": ["#ukjobmarket", "#graduatejobs", "#internships"],
    "x": ["#ukjobs", "#graduatejobs"],
}


def _patch_news(nc, missing):
    """Fill in the non-rendered keys the model left out; raise if a rendered one is gone."""
    fatal = [k for k in missing if k in NEWS_RENDERED]
    if fatal:
        raise RuntimeError(
            f"write_news: the model omitted required news copy {fatal} twice. "
            "Nothing was rendered; re-run the job to get a fresh generation."
        )
    if "hashtags" in missing:
        nc["hashtags"] = {k: list(v) for k, v in NEWS_FALLBACK_HASHTAGS.items()}
    nc.setdefault("kicker", "JOB MARKET")
    return nc


# --------------------------------------------------------------------------- news
def write_news(item):
    """item: {title, summary, source}. Returns reworded on-screen copy + captions."""
    user = f"""Rewrite this UK job-market news story for Internwise (anti-plagiarism: your own words, facts unchanged).

RULES (must follow):
- UK ONLY: this is a UK job board. The story must be about the UK job market. If it is about another country (US, etc.), do not frame it as UK news.
- NO NAMES / NO ENDORSEMENTS: do NOT name, endorse or publicise any individual person or private organisation (company, employer, university, college, recruiter, etc.). Report the facts generically instead ("a major UK employer", "a UK university", "a graduate"). The ONLY exception is UK government job schemes and government bodies (e.g. the Jobs Guarantee scheme, DWP, Ofsted) - these may be named. Never build a story around one named company's or person's success.
- NO STEREOTYPES: never frame jobs, skills or traits by gender, age or industry stereotype (e.g. do not say a job is "for men"/"for women"). Report roles and demand neutrally.
- EXPLANATORY NEWS CAPTIONS: write captions like short plain-English articles, not teaser bites. The reader should understand the story without opening the source, reading the graphic, or inferring the context.
- REQUIRED NEWS CAPTION FLOW: every news caption must explain, in this order: (1) what happened, (2) why it matters, (3) what students/graduates/early-career applicants or employers should understand, and (4) one practical takeaway.
- NO VAGUE BRIDGES: do not jump from a headline to generic lines about "internship journeys", "changing norms", "career foundations", or "adapting to shifts". Internships/Internwise may be mentioned only after the story is explained, and only if the link is specific to the practical lesson.
- SELF-CONTAINED CAPTIONS: the caption must tell the WHOLE story - every key fact, figure and piece of context - so the reader gets the full news without clicking away. NEVER write "link in bio", "read the full story", "read more", "see link", or any phrase that sends them elsewhere to read it.

SOURCE TITLE: {item.get('title','')}
SOURCE SUMMARY: {item.get('summary','')}
SOURCE NAME: {item.get('source','')}

Return JSON with:
  "headline": a short reworded headline (max ~48 chars, not the source's exact words),
  "brief": array of exactly 3 short paragraphs - para 1 states what happened (facts only, reworded), para 2 what it means for students/graduates, para 3 how internships help,
  "sidebar": array of exactly 3 short "what it means for you" bullets (max ~40 chars each),
  "pull": one punchy pull-quote line (max ~60 chars),
  "kicker": one of "JOB MARKET","SKILLS","CAREERS",
  "captions": {{
     "ig-fb": 3-5 short paragraphs that explain the story in plain English using the required flow. No vague internship bridge, no link-teasing. End with "Source: {item.get('source','')}." (<=2200 chars),
     "linkedin": 3-5 professional short paragraphs that explain the story in plain English using the required flow. No vague internship bridge, no link-teasing. End with "Source: {item.get('source','')}." (<=3000 chars),
     "x": one tweet under 280 chars that explains the core story and practical takeaway plainly - no teaser, no "link in bio" - ending with "(Source: {item.get('source','')})",
     "threads": a SELF-CONTAINED caption UNDER 480 characters (Threads limit) that explains the core story and takeaway in Internwise's voice, ending with the URL www.internwise.co.uk (written out, no "link in bio", no trailing period). Do NOT just truncate the ig-fb caption - write a tighter one.
  }},
  "hashtags": {{"ig-fb": [5 tags], "linkedin": [3 tags], "x": [2 tags]}}

Every key above is REQUIRED. Never omit one."""
    for attempt in (1, 2):
        nc = _chat(user, max_tokens=1800)
        missing = [k for k in NEWS_REQUIRED if not nc.get(k)]
        if not missing:
            return nc
        print(f"  ! write_news omitted {missing} (attempt {attempt}/2)")
    return _patch_news(nc, missing)


# --------------------------------------------------------------------- captions only
def write_captions(lane, title, on_screen_text, url_cta=None):
    """Per-platform captions for a quote/fun/employer post whose visual copy is fixed."""
    extra = f'\nThe on-screen CTA is: "{url_cta}"' if url_cta else ""
    user = f"""Write social captions for an Internwise {lane} post.
POST TITLE: {title}
ON-SCREEN TEXT: {on_screen_text}{extra}

Return JSON:
  "captions": {{
     "ig-fb": caption ending with a soft call to find internships at www.internwise.co.uk - write the URL out in full; do NOT say "link in bio" (<=2200),
     "linkedin": professional caption ending with "internwise.co.uk" (<=3000),
     "x": one tweet under 280 ending with "internwise.co.uk"
  }},
  "hashtags": {{"ig-fb": [5 tags], "linkedin": [3 tags], "x": [2 tags]}}"""
    return _chat(user)


# ---------------------------------------------------------------------- education
def write_education(topic, fmt="carousel", slides=5):
    """topic: {title, hook, promise, core_takeaway, proof_points, cta} from the topic engine.
    Returns carousel/single copy sized to fit the design template."""
    shape = (f'"slides": array of exactly {slides} TEACHING slides that form the body of the lesson - '
             f'do NOT include the opening hook or the closing CTA here (those are separate). '
             f'Each slide = {{"tag": a 2-3 word section label, "title": short headline max ~34 chars, '
             f'"body": 1-2 short lines max ~90 chars}}. '
             f'IMPORTANT: never prefix titles or tags with words like "Hook:", "Step:", "Slide:", "CTA:" - just the content itself.'
             if fmt == "carousel" else
             '"points": array of 4-6 short bullets (max ~48 chars each)')
    user = f"""Write an Internwise EDUCATION {fmt} that teaches this topic to students/graduates.
TOPIC: {topic.get('title','')}
HOOK: {topic.get('hook','')}
PROMISE: {topic.get('promise','')}
KEY TAKEAWAY: {topic.get('core_takeaway','')}
PROOF POINTS: {topic.get('proof_points', [])}

Return JSON with:
  "eyebrow": a 1-3 word section label,
  "headline": the cover headline (max ~40 chars),
  "tone": ONE of "serious" (evaluative/cautionary/analytical), "practical" (how-to/steps/tips), or "upbeat" (encouraging/celebratory) - pick the one that best fits how this topic should feel,
  {shape},
  "cta": the closing line for the FINAL slide - ONE conclusive sentence (max ~70 chars) that lands what this lesson proved and names the next move. Write NO web address and do not mention Internwise: the slide design prints the address itself, so a URL here would show it twice. "Discover more" and "Explore more" say nothing about the lesson - be specific to THIS topic,
  "captions": {{
     "ig-fb": value-packed caption ending with a CTA to www.internwise.co.uk - write the URL out in full; do NOT say "link in bio" (<=2200),
     "linkedin": professional caption ending with "internwise.co.uk" (<=3000),
     "x": one tweet under 280 ending with "internwise.co.uk"
  }},
  "hashtags": {{"ig-fb": [5 tags], "linkedin": [3 tags], "x": [2 tags]}}"""
    return _chat(user, max_tokens=1400)


def write_topic_angles(clusters, blocked_titles, per_cluster=1):
    """Write fresh education topic angles for the topic engine's signal clusters.

    clusters: [{"cluster": key, "signals": [headline, ...]}] - the scored signal
    clusters the engine found this week.
    blocked_titles: every education title already used or scheduled. The model
    must not restate any of them.

    This is what makes topic supply unbounded. The engine's static angle bank
    (angle_for_cluster) is a dictionary of ten fixed titles, so it could only
    ever emit one title per cluster - against a permanent posted-title ledger
    that grows five rows a week, exhaustion was arithmetic, not bad luck.

    Returns {"angles": [{cluster, title, hook, promise, takeaway, cta,
    proof_points}]}. The engine falls back to the static bank for any cluster
    the model skips, so a missing key or a failed call degrades, never breaks.
    """
    want = len(clusters) * per_cluster
    listed = "\n".join(
        f"- cluster \"{c['cluster']}\": " + " | ".join(c.get("signals", [])[:5])
        for c in clusters
    )
    avoid = "\n".join(f"- {t}" for t in blocked_titles) or "- (nothing yet)"
    user = f"""Write {want} education topic angles for Internwise short-form content.

Each angle becomes one teaching carousel for UK students and graduates.

SIGNAL CLUSTERS (what the audience is actually asking about this week):
{listed}

ALREADY PUBLISHED - do NOT restate any of these topics. A new angle on the same
cluster is good and expected, but it must teach something materially different
and must not reuse the distinctive wording of these titles:
{avoid}

Rules for every angle:
- The title is a specific claim or question, max ~46 chars, no colons, title case.
- Give {per_cluster} angle(s) per cluster listed above, and set "cluster" to that
  exact cluster key.
- Titles must be distinct from each other as well as from the published list.
- Teach one concrete, actionable idea. No generic "tips for success" framing.
- Obey every brand rule, including the paid-internship rule.

Return JSON with:
  "angles": array of {{
     "cluster": the cluster key,
     "title": the topic title,
     "hook": one spoken opening line that names the reader's problem,
     "promise": one line starting "I will show you..." or similar,
     "takeaway": the single thing they should do differently, one line,
     "cta": one line pointing to internwise.co.uk,
     "proof_points": array of 2-3 short factual reasons this is true (no invented numbers)
  }}"""
    return _chat(user, max_tokens=2200)


if __name__ == "__main__":
    # smoke test (needs OPENAI_API_KEY in env)
    demo = {"title": "Graduate job vacancies hit all-time low in July",
            "summary": "Just 8,383 jobs for people leaving university were advertised in July, says Adzuna; the lowest since 2016.",
            "source": "The Guardian / Adzuna"}
    out = write_news(demo)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    # em-dash guard
    blob = json.dumps(out)
    print("\nEM-DASH CHECK:", "FAIL - contains em/en dash" if ("—" in blob or "–" in blob) else "ok, none")
