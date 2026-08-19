"""Automated topic discovery and script generation for Internwise shorts.

The engine is intentionally source-agnostic:
- Reddit is read through public RSS feeds, not the denied Data API.
- Google Trends uses pytrends when installed, with SerpApi as an optional fallback.
- YouTube competitor signals use the official YouTube Data API when a key exists.

No secrets are stored here. Optional keys are read from environment variables:
YOUTUBE_API_KEY and SERPAPI_API_KEY.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
DEFAULT_SOURCES = ROOT / "video" / "topic_sources.json"
DEFAULT_TOPICS = ROOT / "video" / "topics" / "auto.json"
DEFAULT_SHORTS = REPO_ROOT / "data" / "shorts.json"
DEFAULT_SCRIPTS = ROOT / "video" / "scripts"

USER_AGENT = "InternwiseTopicEngine/1.0 (+https://internwise.co.uk)"

KNOWN_CLUSTERS = {
    "internship-rights",
    "internship-quality",
    "cv",
    "interview",
    "rejection",
    "experience",
    "cover-letter",
    "assessment-centre",
    "linkedin",
    "graduate-jobs",
    "job-search",
}


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

PAIN_PATTERNS = [
    r"\breject(?:ed|ion|ions)?\b",
    r"\bfail(?:ed|ing)?\b",
    r"\bno experience\b",
    r"\bghost(?:ed|ing)?\b",
    r"\bconfus(?:ed|ing|ion)\b",
    r"\banxious\b",
    r"\bstuck\b",
    r"\bstruggl(?:e|ing)\b",
    r"\bnever hear back\b",
    r"\bwhat am i doing wrong\b",
]

AUDIENCE_PATTERNS = [
    r"\bintern(?:ship|ships)?\b",
    r"\bgraduate\b",
    r"\bgrad job\b",
    r"\bcv\b",
    r"\bresume\b",
    r"\bcover letter\b",
    r"\binterview\b",
    r"\bassessment centre\b",
    r"\blinkedin\b",
    r"\bjob search\b",
]

QUESTION_PATTERNS = [
    r"\bhow\b",
    r"\bwhy\b",
    r"\bwhat\b",
    r"\bshould i\b",
    r"\bdo i\b",
    r"\bany advice\b",
]


@dataclass
class Signal:
    source: str
    source_id: str
    title: str
    url: str = ""
    summary: str = ""
    published: str = ""
    score: float = 0.0
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return f"{self.title} {self.summary}".strip()


def clean_copy(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("—", "-").replace("–", "-")).strip()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:64] or "topic"


def fetch_text(url: str, timeout: int = 18) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def score_text(text: str, multiplier: float = 1.0) -> float:
    lowered = text.lower()
    pain = sum(1 for pattern in PAIN_PATTERNS if re.search(pattern, lowered))
    audience = sum(1 for pattern in AUDIENCE_PATTERNS if re.search(pattern, lowered))
    question = sum(1 for pattern in QUESTION_PATTERNS if re.search(pattern, lowered))
    specificity = min(4, len(re.findall(r"\b(?:cv|resume|interview|linkedin|cover letter|assessment centre|internship)\b", lowered)))
    return round((pain * 14 + audience * 9 + question * 6 + specificity * 4) * multiplier, 2)


def audience_hits(text: str) -> int:
    lowered = text.lower()
    return sum(1 for pattern in AUDIENCE_PATTERNS if re.search(pattern, lowered))


def parse_reddit_feed(xml_text: str, source: dict[str, Any]) -> list[Signal]:
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    signals: list[Signal] = []
    entries = root.findall("atom:entry", ns)
    if not entries:
        entries = root.findall(".//item")

    for entry in entries[:30]:
        if entry.tag.endswith("entry"):
            title = entry.findtext("atom:title", default="", namespaces=ns)
            summary = entry.findtext("atom:content", default="", namespaces=ns) or entry.findtext("atom:summary", default="", namespaces=ns)
            published = entry.findtext("atom:updated", default="", namespaces=ns)
            link = ""
            link_el = entry.find("atom:link", ns)
            if link_el is not None:
                link = link_el.attrib.get("href", "")
        else:
            title = entry.findtext("title", default="")
            summary = entry.findtext("description", default="")
            published = entry.findtext("pubDate", default="")
            link = entry.findtext("link", default="")

        title = clean_copy(re.sub(r"<[^>]+>", " ", title))
        summary = clean_copy(re.sub(r"<[^>]+>", " ", summary))
        if not title:
            continue
        score = score_text(f"{title} {summary}", float(source.get("weight", 1.0)))
        signals.append(
            Signal(
                source="reddit_rss",
                source_id=source["id"],
                title=title,
                url=link,
                summary=summary[:500],
                published=published,
                score=score,
                meta={"feed": source.get("label", source["id"])},
            )
        )
    return signals


def collect_reddit_rss(sources: list[dict[str, Any]], offline: bool = False) -> list[Signal]:
    signals: list[Signal] = []
    if offline:
        return signals
    for source in sources:
        last_error = None
        try:
            for attempt in range(3):
                try:
                    signals.extend(parse_reddit_feed(fetch_text(source["url"]), source))
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    if "429" not in str(exc) or attempt == 2:
                        break
                    time.sleep(6 + attempt * 5)
            time.sleep(3.0)
        except Exception as exc:
            last_error = exc

        if last_error is not None:
            signals.append(
                Signal(
                    source="system",
                    source_id=source["id"],
                    title=f"Reddit RSS unavailable: {source.get('label', source['id'])}",
                    summary=str(last_error),
                    score=0,
                    meta={"warning": True},
                )
            )
    return signals


def collect_pytrends(terms: list[str], country: str, offline: bool = False) -> list[Signal]:
    if offline:
        return []
    try:
        from pytrends.request import TrendReq  # type: ignore
    except Exception:
        return []

    signals: list[Signal] = []
    try:
        pytrends = TrendReq(hl="en-GB", tz=0)
        for term in terms:
            pytrends.build_payload([term], cat=0, timeframe="today 3-m", geo=country)
            related = pytrends.related_queries()
            rising = related.get(term, {}).get("rising")
            if rising is None:
                continue
            for _, row in rising.head(5).iterrows():
                query = clean_copy(str(row.get("query", "")))
                value = float(row.get("value", 0) or 0)
                if query:
                    signals.append(
                        Signal(
                            source="google_trends_pytrends",
                            source_id=term,
                            title=query,
                            score=score_text(query) + min(value / 10, 40),
                            meta={"seed": term, "rising_value": value},
                        )
                    )
            time.sleep(1.2)
    except Exception as exc:
        signals.append(Signal(source="system", source_id="pytrends", title="pytrends unavailable", summary=str(exc), score=0, meta={"warning": True}))
    return signals


def serpapi_get(params: dict[str, str], api_key: str) -> dict[str, Any]:
    params = dict(params)
    params["api_key"] = api_key
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    return json.loads(fetch_text(url))


def trend_value(raw: Any) -> float:
    if raw is None:
        return 0.0
    if isinstance(raw, (int, float)):
        return float(raw)
    value = str(raw).strip()
    if value.lower() == "breakout":
        return 5000.0
    value = value.replace("+", "").replace("%", "").replace(",", "")
    try:
        return float(value)
    except ValueError:
        return 0.0


def collect_serpapi_trends(terms: list[str], country: str, offline: bool = False) -> list[Signal]:
    if offline:
        return []
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return []
    signals: list[Signal] = []
    for term in terms:
        try:
            data = serpapi_get({"engine": "google_trends", "q": term, "geo": country, "data_type": "RELATED_QUERIES"}, api_key)
            for item in data.get("related_queries", {}).get("rising", [])[:5]:
                query = clean_copy(str(item.get("query") or item.get("title") or ""))
                value = trend_value(item.get("value", 0))
                if query:
                    signals.append(
                        Signal(
                            source="google_trends_serpapi",
                            source_id=term,
                            title=query,
                            score=score_text(query) + min(value / 10, 40),
                            meta={"seed": term, "rising_value": value},
                        )
                    )
            time.sleep(0.4)
        except Exception as exc:
            signals.append(Signal(source="system", source_id=f"serpapi-{term}", title="SerpApi Trends unavailable", summary=str(exc), score=0, meta={"warning": True}))
    return signals


def youtube_api(path: str, params: dict[str, str], api_key: str) -> dict[str, Any]:
    params = dict(params)
    params["key"] = api_key
    url = "https://www.googleapis.com/youtube/v3/" + path + "?" + urllib.parse.urlencode(params)
    return json.loads(fetch_text(url))


def collect_youtube(queries: list[str], offline: bool = False) -> list[Signal]:
    if offline:
        return []
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return []
    signals: list[Signal] = []
    for query in queries:
        try:
            search = youtube_api(
                "search",
                {
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "videoDuration": "short",
                    "maxResults": "8",
                    "order": "viewCount",
                    "publishedAfter": "2026-01-01T00:00:00Z",
                },
                api_key,
            )
            ids = [item["id"]["videoId"] for item in search.get("items", []) if item.get("id", {}).get("videoId")]
            if not ids:
                continue
            stats = youtube_api("videos", {"part": "statistics,snippet", "id": ",".join(ids), "maxResults": "8"}, api_key)
            for item in stats.get("items", []):
                title = clean_copy(item.get("snippet", {}).get("title", ""))
                view_count = int(item.get("statistics", {}).get("viewCount", 0) or 0)
                published = item.get("snippet", {}).get("publishedAt", "")
                days = days_since(published) or 1
                velocity = view_count / max(days, 1)
                score = score_text(title) + min(velocity / 250, 45)
                signals.append(
                    Signal(
                        source="youtube",
                        source_id=query,
                        title=title,
                        url=f"https://www.youtube.com/watch?v={item.get('id')}",
                        published=published,
                        score=round(score, 2),
                        meta={"query": query, "views": view_count, "views_per_day": round(velocity, 1)},
                    )
                )
            time.sleep(0.4)
        except Exception as exc:
            signals.append(Signal(source="system", source_id=f"youtube-{query}", title="YouTube API unavailable", summary=str(exc), score=0, meta={"warning": True}))
    return signals


def collect_search_questions(questions: list[str]) -> list[Signal]:
    return [
        Signal(
            source="seed_question",
            source_id="configured",
            title=question,
            score=score_text(question) + 18,
            meta={"configured": True},
        )
        for question in questions
    ]


def days_since(published: str) -> int | None:
    if not published:
        return None
    try:
        dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        return max(1, (datetime.now(timezone.utc) - dt).days)
    except ValueError:
        return None


def cluster_key(text: str) -> str:
    lowered = text.lower()
    labels = [
        ("internship-rights", ["unpaid internship", "legally a worker", "entitled to pay", "internship pay", "minimum wage"]),
        ("internship-quality", ["is this internship", "good internship", "internship at", "worth taking"]),
        ("cv", ["cv", "resume"]),
        ("interview", ["interview", "tell me about yourself"]),
        ("rejection", ["reject", "ghost", "never hear back"]),
        ("experience", ["no experience", "experience"]),
        ("cover-letter", ["cover letter"]),
        ("assessment-centre", ["assessment centre", "assessment center"]),
        ("linkedin", ["linkedin"]),
        ("graduate-jobs", ["graduate", "grad job"]),
        ("job-search", ["job search", "job hunting", "applications"]),
    ]
    for label, needles in labels:
        if any(needle in lowered for needle in needles):
            return label
    words = re.findall(r"[a-z0-9]+", lowered)
    return "-".join(words[:3]) or "career"


def angle_for_cluster(cluster: str, sample_title: str) -> dict[str, str]:
    bank = {
        "cv": {
            "title": "The CV Line Recruiters Skip",
            "promise": "I will show you the part of your CV that quietly loses interviews.",
            "takeaway": "Replace vague responsibility lines with proof: action, skill, result.",
            "cta": "Save this before you edit your CV tonight.",
        },
        "interview": {
            "title": "The Interview Answer That Sounds Too Generic",
            "promise": "Here is how to sound prepared without sounding scripted.",
            "takeaway": "Use one situation, one decision, one result, then stop.",
            "cta": "Save this for your next practice interview.",
        },
        "rejection": {
            "title": "Why Rejections Keep Repeating",
            "promise": "If every rejection feels random, track this one pattern.",
            "takeaway": "Separate CV problems, interview problems, and timing problems before changing everything.",
            "cta": "Save this before you apply again.",
        },
        "experience": {
            "title": "No Experience Is Not The Real Problem",
            "promise": "Let me show you what to put on your CV when you think you have nothing.",
            "takeaway": "Translate projects, societies, part-time work, and coursework into evidence.",
            "cta": "Save this and rewrite one bullet today.",
        },
        "cover-letter": {
            "title": "Your Cover Letter Is Too Polite",
            "promise": "Most students waste the first paragraph. Use it to prove fit.",
            "takeaway": "Lead with the role problem, then connect one specific proof point.",
            "cta": "Save this before writing your next cover letter.",
        },
        "assessment-centre": {
            "title": "Assessment Centres Are Not Looking For The Loudest Person",
            "promise": "Here is what assessors actually notice in group tasks.",
            "takeaway": "Make the group better: clarify, include, summarise, and move decisions forward.",
            "cta": "Save this before your next assessment centre.",
        },
        "linkedin": {
            "title": "Your LinkedIn Profile Is Too Empty To Trust",
            "promise": "Three small changes make a student profile look credible.",
            "takeaway": "Make your headline specific, your about section useful, and your projects visible.",
            "cta": "Save this and fix your headline first.",
        },
        "internship-rights": {
            "title": "When An Internship Should Be Paid",
            "promise": "If an internship looks unpaid, check this before you say yes.",
            "takeaway": "If the role has real worker duties, fixed hours, and business value, ask whether pay is legally required.",
            "cta": "Save this before accepting an unpaid internship.",
        },
        "internship-quality": {
            "title": "Is This Internship Worth Taking?",
            "promise": "Before you accept an internship, check whether it will actually move you forward.",
            "takeaway": "A useful internship gives real tasks, feedback, a named manager, and evidence you can show later.",
            "cta": "Save this before saying yes to an internship.",
        },
        "job-search": {
            "title": "Why Your Job Search Feels Random",
            "promise": "If applications feel chaotic, the problem may be your tracking system.",
            "takeaway": "Track role fit, CV version, application date, and response stage so you can see the real bottleneck.",
            "cta": "Save this before your next application batch.",
        },
    }
    return bank.get(
        cluster,
        {
            "title": clean_copy(sample_title)[:72],
            "promise": "Let me turn this common job-search problem into a practical next step.",
            "takeaway": "Make the next action specific enough that you can do it today.",
            "cta": "Save this for your next application session.",
        },
    )


def build_topics(signals: list[Signal], week_id: str) -> list[dict[str, Any]]:
    clusters: dict[str, list[Signal]] = {}
    for signal in signals:
        if signal.meta.get("warning"):
            continue
        key = cluster_key(signal.text)
        clusters.setdefault(key, []).append(signal)

    topics: list[dict[str, Any]] = []
    for cluster, items in clusters.items():
        items = sorted(items, key=lambda item: item.score, reverse=True)
        if cluster not in KNOWN_CLUSTERS and len(items) < 2:
            continue
        top = items[0]
        angle = angle_for_cluster(cluster, top.title)
        total_score = round(sum(item.score for item in items[:8]) / max(1, len(items[:8])) + min(len(items), 8) * 3, 1)
        normalized = max(1, min(5, round(total_score / 18)))
        topic_id = f"auto-{slugify(angle['title'])}"
        topics.append(
            {
                "id": topic_id,
                "title": angle["title"],
                "source_post": "automated-topic-engine",
                "source_cluster": cluster,
                "signal_score": total_score,
                "pain": max(3, normalized),
                "specificity": max(3, normalized),
                "curiosity": max(3, min(5, normalized + 1)),
                "utility": max(4, min(5, normalized + 1)),
                "timeliness": max(3, normalized),
                "discussion": max(3, normalized),
                "brand_fit": 5,
                "hook_candidates": [
                    hook_for_cluster(cluster),
                    f"If you are stuck on {cluster.replace('-', ' ')}, watch this before your next application.",
                ],
                "promise": angle["promise"],
                "proof_points": proof_points_for_cluster(cluster),
                "core_takeaway": angle["takeaway"],
                "cta": angle["cta"],
                "source_signals": [
                    {
                        "source": item.source,
                        "title": item.title,
                        "url": item.url,
                        "score": item.score,
                        "meta": item.meta,
                    }
                    for item in items[:6]
                ],
            }
        )
    return sorted(topics, key=lambda item: item["signal_score"], reverse=True)


def hook_for_cluster(cluster: str) -> str:
    hooks = {
        "cv": "Your CV is not being read the way you think it is.",
        "interview": "This is why your interview answer sounds generic.",
        "rejection": "A rejection does not always mean your application was bad.",
        "experience": "No experience is not the reason your CV feels empty.",
        "cover-letter": "Your cover letter should not start with politeness.",
        "assessment-centre": "The loudest person rarely wins the assessment centre.",
        "linkedin": "Your LinkedIn profile needs proof, not more adjectives.",
        "internship-rights": "Some internships should not be unpaid.",
        "internship-quality": "Not every internship is worth accepting.",
        "job-search": "Your job search feels random because nothing is being tracked.",
    }
    return hooks.get(cluster, "Most students are trying to fix the wrong job-search problem.")


def proof_points_for_cluster(cluster: str) -> list[str]:
    points = {
        "cv": [
            "Recruiters scan for role fit before they read every line.",
            "A task without a result feels like a job description, not evidence.",
            "Your strongest proof should appear above the fold, not hidden on page two.",
        ],
        "interview": [
            "Generic answers sound safe, but they are hard to remember.",
            "A specific moment proves judgement better than a list of traits.",
            "Stopping cleanly is part of confidence.",
        ],
        "rejection": [
            "CV rejection, interview rejection, and timing rejection need different fixes.",
            "Changing everything after every no makes your process noisier.",
            "Track where you drop off before deciding what to rewrite.",
        ],
        "experience": [
            "Experience is evidence, not just formal internships.",
            "Projects and part-time work can prove teamwork, ownership, and problem solving.",
            "The phrasing matters: show what changed because you were involved.",
        ],
        "cover-letter": [
            "The opening line should connect to the role, not repeat your enthusiasm.",
            "One specific company or role detail beats five generic compliments.",
            "The letter should make the CV easier to believe.",
        ],
        "assessment-centre": [
            "Assessors look for useful behaviour under pressure.",
            "Include quiet people and summarise decisions to show leadership.",
            "Do not dominate the room just to look confident.",
        ],
        "linkedin": [
            "A vague headline makes you harder to place.",
            "Visible projects reduce risk for recruiters.",
            "Your about section should point to the kind of work you want next.",
        ],
        "internship-rights": [
            "Work shadowing and real worker duties are not the same thing.",
            "Fixed hours, required output, and business value are signals to question.",
            "Ask for clarity in writing before you commit.",
        ],
        "internship-quality": [
            "The title matters less than the evidence you can build.",
            "Good internships include feedback, ownership, and useful exposure.",
            "If the role is vague, ask what you will actually do each week.",
        ],
        "job-search": [
            "Without tracking, every rejection feels like a mystery.",
            "Patterns only appear when you separate CV drop-offs from interview drop-offs.",
            "A simple tracker stops you changing everything at once.",
        ],
    }
    return points.get(
        cluster,
        [
            "Name the exact problem before choosing the fix.",
            "Make one visible improvement instead of rewriting everything.",
            "Track the result so you know whether the advice worked.",
        ],
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def run_script_generator(topics_path: Path, out_dir: Path, top: int) -> None:
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "shorts_script_generator.py"),
        "--topics",
        str(topics_path),
        "--out",
        str(out_dir),
        "--top",
        str(top),
    ]
    subprocess.run(cmd, check=True)


def load_script(script_path: Path) -> dict[str, Any]:
    return json.loads(script_path.read_text())


def write_dashboard(shorts_path: Path, topics_payload: dict[str, Any], top: int) -> None:
    posts = []
    for topic in topics_payload["topics"][:top]:
        script_path = DEFAULT_SCRIPTS / topics_payload["week_id"] / topic["id"] / "script.json"
        brief_path = DEFAULT_SCRIPTS / topics_payload["week_id"] / topic["id"] / "brief.md"
        script = load_script(script_path) if script_path.exists() else {}
        posts.append(
            {
                "id": f"{topics_payload['week_id']}-{topic['id']}",
                "topicId": topic["id"],
                "weekId": topics_payload["week_id"],
                "day": "Auto",
                "title": topic["title"],
                "platform": "TikTok / Reels / Shorts",
                "format": "Short/Reel",
                "status": "script-ready",
                "durationTargetSeconds": script.get("duration_target_seconds", topics_payload.get("default_duration_seconds", 45)),
                "viralScore": script.get("viral_score"),
                "signalScore": topic.get("signal_score"),
                "scriptPath": str(script_path.relative_to(REPO_ROOT)),
                "briefPath": str(brief_path.relative_to(REPO_ROOT)),
                "videoPath": None,
                "thumbnailPath": None,
                "heygenStatus": "manual",
                "spokenScript": script.get("spoken_script", ""),
                "scenePlan": script.get("beats", []),
                "selectionRationale": script.get("selection_rationale", []),
                "caption": script.get("caption_pack", {}).get("instagram", ""),
                "captions": script.get("caption_pack", {}),
                "hashtags": ["#internship", "#graduatejobs", "#careeradvice", "#jobsearch", "#internwise"],
                "sourceSignals": topic.get("source_signals", []),
            }
        )
    payload = {
        "id": "shorts",
        "label": "Shorts / Reels",
        "generatedAt": topics_payload["generated_at"],
        "status": "automated-topic-research",
        "posts": posts,
    }
    write_json(shorts_path, payload)


def fallback_signals(config: dict[str, Any]) -> list[Signal]:
    # Used only when every live source is unavailable, so the automation still
    # emits scripts and makes missing credentials visible.
    return collect_search_questions(config.get("search_questions", []))


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover and score hands-free shorts topics.")
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--topics-out", type=Path, default=DEFAULT_TOPICS)
    parser.add_argument("--shorts-out", type=Path, default=DEFAULT_SHORTS)
    parser.add_argument("--scripts-out", type=Path, default=DEFAULT_SCRIPTS)
    parser.add_argument("--top", type=int, default=None)
    parser.add_argument("--offline", action="store_true", help="Skip network sources and use configured seed questions.")
    parser.add_argument("--skip-scripts", action="store_true")
    args = parser.parse_args()

    load_env_file(REPO_ROOT / ".env")
    load_env_file(ROOT / ".env")

    config = json.loads(args.sources.read_text())
    top = args.top or int(config.get("refresh", {}).get("default_top", 5))
    country = config.get("refresh", {}).get("country", "GB")
    signals: list[Signal] = []
    signals.extend(collect_reddit_rss(config.get("reddit_rss", []), offline=args.offline))
    signals.extend(collect_pytrends(config.get("google_trends", {}).get("terms", []), country, offline=args.offline))
    signals.extend(collect_serpapi_trends(config.get("google_trends", {}).get("terms", []), country, offline=args.offline))
    signals.extend(collect_youtube(config.get("youtube_competitors", {}).get("queries", []), offline=args.offline))
    signals.extend(collect_search_questions(config.get("search_questions", [])))

    useful_signals = [
        signal for signal in signals
        if not signal.meta.get("warning")
        and (signal.source == "seed_question" or audience_hits(signal.text) > 0)
    ]
    if not useful_signals:
        useful_signals = fallback_signals(config)
        signals.extend(useful_signals)

    topics = build_topics(useful_signals, week_id=f"auto-{date.today().isoformat()}")
    payload = {
        "week_id": f"auto-{date.today().isoformat()}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "default_duration_seconds": 52,
        "source_summary": {
            "reddit_rss_signals": len([s for s in signals if s.source == "reddit_rss"]),
            "google_trends_signals": len([s for s in signals if s.source.startswith("google_trends")]),
            "youtube_signals": len([s for s in signals if s.source == "youtube"]),
            "seed_question_signals": len([s for s in signals if s.source == "seed_question"]),
            "warnings": [
                {"source": s.source_id, "title": s.title, "detail": s.summary}
                for s in signals
                if s.meta.get("warning")
            ],
        },
        "topics": topics,
        "fingerprint": hashlib.sha256(json.dumps([s.__dict__ for s in useful_signals], sort_keys=True).encode()).hexdigest()[:16],
    }
    write_json(args.topics_out, payload)

    if not args.skip_scripts:
        run_script_generator(args.topics_out, args.scripts_out, top=top)
        write_dashboard(args.shorts_out, payload, top=top)

    print(json.dumps({"topics": len(topics), "top": [topic["id"] for topic in topics[:top]], "source_summary": payload["source_summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
