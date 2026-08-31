"""Daily-5 writer - LLM copywriting for on-screen text + captions.

Turns sourced content (an RSS item, a quote, a fun idea, an employer angle, or an
education topic) into brand-safe copy: reworded news, per-platform captions,
education carousel slides. All brand rules live in SYSTEM so every call obeys
them. Used by the build step; runs unattended in the cloud (needs OPENAI_API_KEY).

    from writer import write_news, write_captions, write_education
"""
import os, json, sys

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


def _chat(user, max_tokens=900):
    resp = _client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=max_tokens,
    )
    return json.loads(resp.choices[0].message.content)


# --------------------------------------------------------------------------- news
def write_news(item):
    """item: {title, summary, source}. Returns reworded on-screen copy + captions."""
    user = f"""Rewrite this UK job-market news story for Internwise (anti-plagiarism: your own words, facts unchanged).

RULES (must follow):
- UK ONLY: this is a UK job board. The story must be about the UK job market. If it is about another country (US, etc.), do not frame it as UK news.
- NO NAMES / NO ENDORSEMENTS: do NOT name, endorse or publicise any individual person or private organisation (company, employer, university, college, recruiter, etc.). Report the facts generically instead ("a major UK employer", "a UK university", "a graduate"). The ONLY exception is UK government job schemes and government bodies (e.g. the Jobs Guarantee scheme, DWP, Ofsted) - these may be named. Never build a story around one named company's or person's success.
- NO STEREOTYPES: never frame jobs, skills or traits by gender, age or industry stereotype (e.g. do not say a job is "for men"/"for women"). Report roles and demand neutrally.
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
     "ig-fb": a self-contained caption that tells the whole story (all key facts and figures) in Internwise's voice, then one short line on how internships help early-career jobseekers. No link-teasing. End with "Source: {item.get('source','')}." (<=2200 chars),
     "linkedin": a professional, self-contained caption telling the whole story (all key facts and figures), then a brief internships angle. No link-teasing. End with "Source: {item.get('source','')}." (<=3000 chars),
     "x": one tweet under 280 chars giving the most important fact(s) plainly - no teaser, no "link in bio" - ending with "(Source: {item.get('source','')})",
     "threads": a SELF-CONTAINED caption UNDER 480 characters (Threads limit) that still tells the story's key facts in Internwise's voice, ending with the URL www.internwise.co.uk (written out, no "link in bio", no trailing period). Do NOT just truncate the ig-fb caption - write a tighter one.
  }},
  "hashtags": {{"ig-fb": [5 tags], "linkedin": [3 tags], "x": [2 tags]}}"""
    return _chat(user, max_tokens=1500)


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
  {shape},
  "cta": one line pointing to internwise.co.uk,
  "captions": {{
     "ig-fb": value-packed caption ending with a CTA to www.internwise.co.uk - write the URL out in full; do NOT say "link in bio" (<=2200),
     "linkedin": professional caption ending with "internwise.co.uk" (<=3000),
     "x": one tweet under 280 ending with "internwise.co.uk"
  }},
  "hashtags": {{"ig-fb": [5 tags], "linkedin": [3 tags], "x": [2 tags]}}"""
    return _chat(user, max_tokens=1400)


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
