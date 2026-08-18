"""Tests for the orchestrator agent."""

import json
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.orchestrator import load_brief, create_task_plan, run_campaign


SAMPLE_BRIEF = {
    "campaign_id": "test-campaign-001",
    "topic": "Remote work trends in tech",
    "platforms": ["linkedin", "instagram"],
    "audience": "software engineers, 25-40",
    "goal": "awareness",
    "tone_override": None,
    "publish_at": None,
}


class TestLoadBrief:
    def test_load_valid_brief(self, tmp_path):
        brief_file = tmp_path / "test_brief.json"
        brief_file.write_text(json.dumps(SAMPLE_BRIEF))
        result = load_brief(str(brief_file))
        assert result["campaign_id"] == "test-campaign-001"
        assert "linkedin" in result["platforms"]

    def test_load_missing_brief(self):
        with pytest.raises(FileNotFoundError):
            load_brief("/nonexistent/path/brief.json")

    def test_load_brief_missing_fields(self, tmp_path):
        brief_file = tmp_path / "bad_brief.json"
        brief_file.write_text(json.dumps({"campaign_id": "test"}))
        with pytest.raises(ValueError, match="Missing required field"):
            load_brief(str(brief_file))


class TestCreateTaskPlan:
    def test_creates_tasks_for_each_platform(self):
        tasks = create_task_plan(SAMPLE_BRIEF)
        platforms_with_copy = [t["platform"] for t in tasks if t["type"] == "copy"]
        assert "linkedin" in platforms_with_copy
        assert "instagram" in platforms_with_copy

    def test_includes_graphics_tasks(self):
        tasks = create_task_plan(SAMPLE_BRIEF)
        graphic_tasks = [t for t in tasks if t["type"] == "graphic"]
        assert len(graphic_tasks) == 2

    def test_includes_video_for_supported_platforms(self):
        tasks = create_task_plan(SAMPLE_BRIEF)
        video_tasks = [t for t in tasks if t["type"] == "video"]
        video_platforms = [t["platform"] for t in video_tasks]
        assert "instagram" in video_platforms
        assert "linkedin" in video_platforms

    def test_no_video_for_x(self):
        brief = {**SAMPLE_BRIEF, "platforms": ["x"]}
        tasks = create_task_plan(brief)
        video_tasks = [t for t in tasks if t["type"] == "video"]
        assert len(video_tasks) == 0

    def test_all_tasks_start_pending(self):
        tasks = create_task_plan(SAMPLE_BRIEF)
        assert all(t["status"] == "pending" for t in tasks)


class TestRunCampaign:
    def test_dry_run_produces_package(self):
        package = run_campaign(SAMPLE_BRIEF, dry_run=True)
        assert package["campaign_id"] == "test-campaign-001"
        assert package["publish_status"] == "draft"
        assert package["human_approved"] is False
        assert "copy" in package["content_package"]
        assert "graphics" in package["content_package"]

    def test_dry_run_creates_output_files(self):
        package = run_campaign(SAMPLE_BRIEF, dry_run=True)
        output_dir = PROJECT_ROOT / "campaigns" / "outputs" / "test-campaign-001"
        assert output_dir.exists()
        assert (output_dir / "package_summary.json").exists()

    def test_dry_run_copy_per_platform(self):
        package = run_campaign(SAMPLE_BRIEF, dry_run=True)
        copy = package["content_package"]["copy"]
        assert "linkedin" in copy
        assert "instagram" in copy
        assert copy["linkedin"].get("mock") is True
