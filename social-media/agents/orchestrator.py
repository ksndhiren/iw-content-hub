"""Orchestrator agent — campaign planner and task router."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

# Add project root to path for tool/agent imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.brand_memory import get_brand_memory, save_post, update_analytics
from tools.scheduler import schedule_post
from agents.content_writer import generate_copy
from agents.graphics_producer import generate_graphics
from agents.av_producer import produce_video

MODEL = "claude-opus-4-5-20250514"

SYSTEM_PROMPT = """You are the orchestrator of a social media content team for Internwise — the UK and Europe's internship recruitment specialist. Internwise connects global employers with ambitious students and recent graduates since 2010.

When given a campaign brief, you:
1. Identify the target platform(s), audience (candidates vs employers), and content goal
2. Tag the campaign with its content pillar (career inspiration, market insights, practical advice, employer spotlight, platform & community)
3. Break the campaign into tasks: copy task → graphics task → video task (run in parallel when possible)
4. Load Internwise brand guidelines from memory before routing any task
5. Review all specialist outputs for brand alignment — warm, encouraging, human tone; correct hashtag strategy; no clichés, competitor mentions, or overpromising
6. Route approved content to the scheduler with correct platform metadata
7. Log the campaign outcome to memory for future reference

Always produce a structured task plan in JSON before dispatching agents.
Never publish without a human_approved: true flag in the content package."""

AGENT_REGISTRY = {
    "content_writer": generate_copy,
    "graphics_producer": generate_graphics,
    "av_producer": produce_video,
}


def setup_logging(campaign_id: str) -> logging.Logger:
    """Configure campaign-specific logging."""
    log_dir = PROJECT_ROOT / "campaigns" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{campaign_id}.log"

    logger = logging.getLogger(f"orchestrator.{campaign_id}")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def load_brief(brief_path: str) -> dict:
    """Load and validate a campaign brief JSON file."""
    path = Path(brief_path)
    if not path.exists():
        raise FileNotFoundError(f"Brief not found: {brief_path}")

    brief = json.loads(path.read_text())

    required_fields = ["campaign_id", "topic", "platforms", "audience", "goal"]
    for field in required_fields:
        if field not in brief:
            raise ValueError(f"Missing required field in brief: {field}")

    return brief


def create_task_plan(brief: dict) -> list[dict]:
    """Decompose a campaign brief into a task plan for specialist agents."""
    tasks = []

    for platform in brief["platforms"]:
        # Copy task — always needed
        tasks.append({
            "task_id": f"{brief['campaign_id']}-copy-{platform}",
            "agent": "content_writer",
            "platform": platform,
            "type": "copy",
            "status": "pending",
        })

        # Graphics task — all platforms except pure text
        tasks.append({
            "task_id": f"{brief['campaign_id']}-graphic-{platform}",
            "agent": "graphics_producer",
            "platform": platform,
            "type": "graphic",
            "status": "pending",
        })

        # Video task — only for video-friendly platforms
        if platform in ("tiktok", "instagram", "linkedin"):
            tasks.append({
                "task_id": f"{brief['campaign_id']}-video-{platform}",
                "agent": "av_producer",
                "platform": platform,
                "type": "video",
                "status": "pending",
            })

    return tasks


def run_campaign(brief: dict, dry_run: bool = False) -> dict:
    """Execute a full campaign from brief to content package.

    Args:
        brief: Campaign brief dict.
        dry_run: If True, use mock outputs from all agents.

    Returns:
        Content package dict ready for human review.
    """
    campaign_id = brief["campaign_id"]
    logger = setup_logging(campaign_id)
    logger.info(f"Starting campaign: {campaign_id}")
    logger.info(f"Topic: {brief['topic']}")
    logger.info(f"Platforms: {brief['platforms']}")

    # Load brand guidelines
    brand = get_brand_memory()
    logger.info("Brand guidelines loaded")

    # Create task plan
    task_plan = create_task_plan(brief)
    logger.info(f"Task plan created: {len(task_plan)} tasks")

    # Set up output directory
    output_dir = PROJECT_ROOT / "campaigns" / "outputs" / campaign_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # Execute tasks
    content_package = {"copy": {}, "graphics": {}, "video": {}}

    for task in task_plan:
        logger.info(f"Executing task: {task['task_id']}")
        task["status"] = "in_progress"

        try:
            if task["type"] == "copy":
                result = generate_copy(
                    platform=task["platform"],
                    topic=brief["topic"],
                    audience=brief["audience"],
                    goal=brief["goal"],
                    tone_override=brief.get("tone_override"),
                    dry_run=dry_run,
                )
                content_package["copy"][task["platform"]] = result

                # Save copy output
                copy_path = output_dir / f"copy_{task['platform']}.json"
                copy_path.write_text(json.dumps(result, indent=2))

            elif task["type"] == "graphic":
                copy_text = content_package["copy"].get(task["platform"], {}).get("copy", "")
                result = generate_graphics(
                    platform=task["platform"],
                    topic=brief["topic"],
                    goal=brief["goal"],
                    copy_text=copy_text,
                    output_dir=str(output_dir),
                    dry_run=dry_run,
                )
                content_package["graphics"][task["platform"]] = result

            elif task["type"] == "video":
                copy_text = content_package["copy"].get(task["platform"], {}).get("copy", "")
                result = produce_video(
                    platform=task["platform"],
                    topic=brief["topic"],
                    goal=brief["goal"],
                    copy_text=copy_text,
                    output_dir=str(output_dir),
                    dry_run=dry_run,
                )
                content_package["video"][task["platform"]] = result

            task["status"] = "completed"
            logger.info(f"Task completed: {task['task_id']}")

        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            logger.error(f"Task failed: {task['task_id']} — {e}")

    # Build final package
    package = {
        "campaign_id": campaign_id,
        "task_plan": task_plan,
        "content_package": content_package,
        "human_approved": False,
        "publish_status": "draft",
        "created_at": datetime.utcnow().isoformat(),
        "brief": brief,
    }

    # Save package summary
    summary_path = output_dir / "package_summary.json"
    summary_path.write_text(json.dumps(package, indent=2, default=str))
    logger.info(f"Content package saved to: {summary_path}")
    logger.info("Campaign ready for human review. Set human_approved: true to publish.")

    return package


def publish_campaign(package_path: str) -> dict:
    """Publish an approved content package.

    Args:
        package_path: Path to the package_summary.json file.

    Returns:
        Dict with publish results per platform.
    """
    path = Path(package_path)
    if not path.exists():
        raise FileNotFoundError(f"Package not found: {package_path}")

    package = json.loads(path.read_text())

    if not package.get("human_approved"):
        raise ValueError(
            "Content must be human-approved before publishing. "
            "Set 'human_approved': true in package_summary.json."
        )

    logger = setup_logging(package["campaign_id"])
    logger.info(f"Publishing campaign: {package['campaign_id']}")

    results = {}
    publish_at = package.get("brief", {}).get("publish_at")

    for platform, copy_data in package["content_package"].get("copy", {}).items():
        content = {
            "copy": copy_data.get("copy", ""),
            "hashtags": copy_data.get("hashtags", []),
            "image_url": package["content_package"].get("graphics", {}).get(platform, {}).get("image_url"),
            "human_approved": True,
        }

        result = schedule_post(
            platform=platform,
            content=content,
            publish_at=publish_at,
        )
        results[platform] = result
        logger.info(f"Published to {platform}: {result.get('status')}")

        # Save to memory
        save_post(platform, {
            "campaign_id": package["campaign_id"],
            "copy": copy_data.get("copy", ""),
            "published_at": datetime.utcnow().isoformat(),
            **result,
        })

    # Update package status
    package["publish_status"] = "published"
    package["publish_results"] = results
    path.write_text(json.dumps(package, indent=2, default=str))
    logger.info("Campaign published successfully")

    return results


def main():
    parser = argparse.ArgumentParser(description="Social Media Campaign Orchestrator")
    parser.add_argument("--brief", help="Path to campaign brief JSON file")
    parser.add_argument("--publish", help="Path to approved package_summary.json to publish")
    parser.add_argument("--dry-run", action="store_true", help="Use mock outputs (no API calls)")
    args = parser.parse_args()

    if args.publish:
        results = publish_campaign(args.publish)
        print(json.dumps(results, indent=2, default=str))
    elif args.brief:
        brief = load_brief(args.brief)
        package = run_campaign(brief, dry_run=args.dry_run)
        print(json.dumps({
            "campaign_id": package["campaign_id"],
            "status": package["publish_status"],
            "tasks_completed": sum(1 for t in package["task_plan"] if t["status"] == "completed"),
            "tasks_total": len(package["task_plan"]),
        }, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
