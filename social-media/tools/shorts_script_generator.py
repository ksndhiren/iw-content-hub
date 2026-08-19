"""Generate review-ready short-form video scripts for Internwise.

This does not call HeyGen. It creates production briefs that can be pasted into
HeyGen manually while the first shorts/reels format is being tested.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from textwrap import wrap


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TOPICS = ROOT / "video" / "topics" / "week12.json"
DEFAULT_OUT = ROOT / "video" / "scripts"

WEIGHTS = {
    "pain": 1.35,
    "specificity": 1.25,
    "curiosity": 1.2,
    "utility": 1.35,
    "timeliness": 0.85,
    "discussion": 0.85,
    "brand_fit": 1.15,
}

HASHTAGS = {
    "tiktok": ["#internship", "#graduatejobs", "#careeradvice", "#jobsearch", "#internwiselife"],
    "instagram": ["#internship", "#graduatejobs", "#careeradvice", "#jobsearch", "#internwise"],
    "youtube": ["#internship", "#careeradvice", "#graduatejobs"],
    "linkedin": ["#careeradvice", "#earlycareers", "#graduatejobs"],
}


@dataclass
class Topic:
    raw: dict

    @property
    def id(self) -> str:
        return self.raw["id"]

    @property
    def title(self) -> str:
        return self.raw["title"]

    @property
    def score(self) -> float:
        total = sum(float(self.raw.get(k, 0)) * weight for k, weight in WEIGHTS.items())
        max_score = 5 * sum(WEIGHTS.values())
        return round((total / max_score) * 100, 1)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def clean_copy(text: str) -> str:
    return text.replace("—", "-").replace("–", "-").strip()


def seconds_for_words(text: str) -> int:
    words = len(re.findall(r"\b\w+\b", text))
    return max(15, round(words / 2.45))


def choose_hook(topic: Topic) -> str:
    hooks = topic.raw.get("hook_candidates", [])
    if not hooks:
        return f"Most people get {topic.title.lower()} wrong."
    return hooks[0]


def split_scene_voiceover(parts: list[str]) -> list[str]:
    scenes = [
        " ".join(parts[:2]),
        " ".join(parts[2:4]),
        " ".join(parts[4:6]),
        parts[6],
    ]
    return [clean_copy(scene) for scene in scenes if scene.strip()]


def visual_scene(topic: Topic, idx: int, voiceover: str) -> dict:
    t = topic.raw
    cluster = t.get("source_cluster") or t.get("source_post") or "career-advice"
    scene_bank = [
        {
            "setting": "a modern internship interview waiting room with anxious candidates in soft focus behind Nuno",
            "camera": "medium close-up, Nuno seated forward, direct eye contact, documentary realism",
            "effect": "slow push-in from chest-up to close-up",
            "transition_out": "fast whip pan into the next scene",
        },
        {
            "setting": "a glass-walled interview room where a recruiter reviews a CV in the blurred background",
            "camera": "over-the-shoulder depth, Nuno half-profile then turns to camera",
            "effect": "subtle parallax drift with a slow zoom out",
            "transition_out": "blur dissolve into evidence close-up",
        },
        {
            "setting": "a close-up CV review board with highlighted sections, sticky notes, and recruiter marks",
            "camera": "Nuno beside the board, pointing to the strongest evidence area without readable text overlays",
            "effect": "slow lateral slide from CV detail to Nuno's face",
            "transition_out": "match cut on Nuno's hand movement",
        },
        {
            "setting": "calm office corridor after the interview, warm Internwise navy and amber accents in the environment",
            "camera": "confident close-up, Nuno walking slowly with the camera then stopping for the final line",
            "effect": "slow zoom out, slight background music lift",
            "transition_out": "fade to branded end card",
        },
    ]
    chosen = scene_bank[min(idx, len(scene_bank) - 1)]
    prompt = (
        f"Vertical 9:16 cinematic short-form video scene for Internwise. "
        f"Nuno is the presenter and main face of the scene. Topic context: {cluster}. "
        f"Scene setting: {chosen['setting']}. Camera: {chosen['camera']}. "
        f"Natural office lighting, realistic UK early-careers environment, premium but approachable, "
        f"navy and amber brand accents, no on-screen text, no subtitles, no logos except natural end-card later. "
        f"Voiceover meaning: {voiceover}"
    )
    image_prompt = (
        f"Create a vertical 9:16 photorealistic reference image for Gemini: Nuno in {chosen['setting']}, "
        f"{chosen['camera']}, Internwise navy and amber accents, realistic office detail, no on-screen text, no captions."
    )
    return {
        "scene": idx + 1,
        "target_seconds": min(15, seconds_for_words(voiceover)),
        "heygen_voiceover": voiceover,
        "video_prompt": clean_copy(prompt),
        "image_prompt": clean_copy(image_prompt),
        "effect": chosen["effect"],
        "transition_out": chosen["transition_out"],
    }


def make_script(topic: Topic, week_id: str, duration: int) -> dict:
    t = topic.raw
    hook = clean_copy(choose_hook(topic))
    points = [clean_copy(p) for p in t.get("proof_points", [])][:3]
    while len(points) < 3:
        points.append("Make the next step specific, visible, and easy to act on.")

    spoken_parts = [
        hook,
        t["promise"],
        f"First: {points[0]}",
        f"Second: {points[1]}",
        f"Third: {points[2]}",
        f"The rule is simple: {t['core_takeaway']}",
        t["cta"],
    ]
    spoken_script = clean_copy(" ".join(spoken_parts))

    actual_seconds = seconds_for_words(spoken_script)
    if actual_seconds > duration + 6:
        spoken_script = clean_copy(" ".join(spoken_parts[:6]))
        actual_seconds = seconds_for_words(spoken_script)

    scene_voiceovers = split_scene_voiceover(spoken_parts)
    scenes = [visual_scene(topic, idx, voiceover) for idx, voiceover in enumerate(scene_voiceovers)]

    caption = (
        f"{hook}\n\n"
        f"{t['core_takeaway']}\n\n"
        f"Save this before your next application or interview.\n\n"
        f"{' '.join(HASHTAGS['instagram'])}"
    )

    return {
        "id": t["id"],
        "week_id": week_id,
        "title": t["title"],
        "source_post": t.get("source_post"),
        "status": "script-ready",
        "created_at": date.today().isoformat(),
        "viral_score": topic.score,
        "selection_rationale": selection_rationale(topic),
        "recommended_platforms": ["tiktok", "instagram-reels", "youtube-shorts", "linkedin-video"],
        "duration_target_seconds": duration,
        "estimated_spoken_seconds": actual_seconds,
        "heygen_settings": {
            "format": "9:16",
            "resolution": "1080p",
            "presenter": "Nuno, approved founder/avatar",
            "max_single_scene_seconds": 15,
            "captions": "no on-screen text in the rendered video; captions can be platform-native after upload",
            "rendering": "scene-by-scene HeyGen generation, then stitch in Canva or CapCut"
        },
        "spoken_script": spoken_script,
        "scenes": scenes,
        "beats": scenes,
        "on_screen_text": [],
        "caption_pack": {
            "instagram": caption,
            "tiktok": caption,
            "youtube": f"{hook}\n\n{t['core_takeaway']}\n\n{' '.join(HASHTAGS['youtube'])}",
            "linkedin": (
                f"{hook}\n\n"
                f"{t['core_takeaway']}\n\n"
                "Short, practical, and built for students preparing for the next step.\n\n"
                f"{' '.join(HASHTAGS['linkedin'])}"
            )
        },
        "production_notes": [
            "Open with direct eye contact and no intro logo.",
            "Generate each scene as a separate HeyGen clip because single shots are capped at 15 seconds.",
            "Use light background music behind the voice and keep it low enough that speech stays clear.",
            "Do not add on-screen text to the video.",
            "Do not say 'link in bio' in the video. Put it only in IG/TikTok captions if needed.",
            "No em dashes in captions or overlays."
        ]
    }


def selection_rationale(topic: Topic) -> list[str]:
    t = topic.raw
    rationale = []
    if int(t.get("pain", 0)) >= 5:
        rationale.append("High candidate pain, likely to stop the scroll.")
    if int(t.get("specificity", 0)) >= 5:
        rationale.append("Concrete enough to feel immediately useful.")
    if int(t.get("curiosity", 0)) >= 4:
        rationale.append("Creates an open loop that earns the next few seconds.")
    if int(t.get("discussion", 0)) >= 4:
        rationale.append("Has comment/share potential.")
    if int(t.get("utility", 0)) >= 5:
        rationale.append("Save-worthy practical takeaway.")
    return rationale


def markdown_brief(script: dict) -> str:
    scenes = "\n\n".join(
        clean_copy(f"""### Scene {scene['scene']} ({scene['target_seconds']}s max)

HeyGen voiceover:
{scene['heygen_voiceover']}

Video prompt:
{scene['video_prompt']}

Gemini image prompt:
{scene['image_prompt']}

Effect: {scene['effect']}
Transition out: {scene['transition_out']}""")
        for scene in script["scenes"]
    )
    rationale = "\n".join(f"- {r}" for r in script["selection_rationale"])
    notes = "\n".join(f"- {n}" for n in script["production_notes"])
    wrapped_script = "\n".join(wrap(script["spoken_script"], width=88))
    return clean_copy(f"""# {script['title']}

Status: {script['status']}
Viral score: {script['viral_score']}/100
Target: {script['duration_target_seconds']}s
Estimated spoken length: {script['estimated_spoken_seconds']}s

## Why This Topic
{rationale}

## HeyGen Setup
- Format: {script['heygen_settings']['format']}
- Resolution: {script['heygen_settings']['resolution']}
- Presenter: {script['heygen_settings']['presenter']}
- Captions: {script['heygen_settings']['captions']}
- Max single scene: {script['heygen_settings']['max_single_scene_seconds']}s

## Spoken Script
{wrapped_script}

## Copy/Paste Scene Prompts
{scenes}

## Production Notes
{notes}

## Instagram/TikTok Caption
{script['caption_pack']['instagram']}
""")


def load_topics(path: Path) -> tuple[dict, list[Topic]]:
    payload = json.loads(path.read_text())
    return payload, [Topic(t) for t in payload["topics"]]


def write_script(script: dict, out_root: Path) -> list[Path]:
    folder = out_root / script["week_id"] / script["id"]
    folder.mkdir(parents=True, exist_ok=True)
    json_path = folder / "script.json"
    md_path = folder / "brief.md"
    json_path.write_text(json.dumps(script, indent=2) + "\n")
    md_path.write_text(markdown_brief(script) + "\n")
    return [json_path, md_path]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Internwise short-form video scripts.")
    parser.add_argument("--topics", type=Path, default=DEFAULT_TOPICS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--top", type=int, default=3, help="Number of highest-scoring topics to generate.")
    parser.add_argument("--all", action="store_true", help="Generate every topic.")
    parser.add_argument("--topic-id", help="Generate one topic by id.")
    parser.add_argument("--duration", type=int, help="Target duration in seconds.")
    args = parser.parse_args()

    payload, topics = load_topics(args.topics)
    duration = args.duration or int(payload.get("default_duration_seconds", 42))

    if args.topic_id:
        selected = [t for t in topics if t.id == args.topic_id]
        if not selected:
            raise SystemExit(f"Unknown topic id: {args.topic_id}")
    elif args.all:
        selected = sorted(topics, key=lambda t: t.score, reverse=True)
    else:
        selected = sorted(topics, key=lambda t: t.score, reverse=True)[:args.top]

    written = []
    for topic in selected:
        script = make_script(topic, payload["week_id"], duration)
        written.extend(write_script(script, args.out))

    summary = {
        "week_id": payload["week_id"],
        "generated": [t.id for t in selected],
        "scores": {t.id: t.score for t in sorted(topics, key=lambda item: item.score, reverse=True)},
        "files": [str(p.relative_to(ROOT)) for p in written],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
