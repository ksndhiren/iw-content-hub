"""Tests for the audio/video producer agent."""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.av_producer import produce_video, VIDEO_SPECS


class TestProduceVideo:
    def test_dry_run_tiktok(self):
        result = produce_video(
            platform="tiktok",
            topic="AI jobs are booming",
            goal="awareness",
            dry_run=True,
        )
        assert result["platform"] == "tiktok"
        assert result["mock"] is True
        assert "script" in result
        assert "voiceover_url" in result
        assert "video_url" in result
        assert result["duration_seconds"] > 0
        assert "captions_srt" in result

    def test_dry_run_instagram(self):
        result = produce_video(
            platform="instagram",
            topic="Top resume tips",
            goal="engagement",
            dry_run=True,
        )
        assert result["platform"] == "instagram"

    def test_dry_run_linkedin(self):
        result = produce_video(
            platform="linkedin",
            topic="Hiring trends Q2",
            goal="awareness",
            dry_run=True,
        )
        assert result["platform"] == "linkedin"


class TestVideoSpecs:
    def test_tiktok_specs(self):
        assert VIDEO_SPECS["tiktok"]["aspect_ratio"] == "9:16"
        assert VIDEO_SPECS["tiktok"]["max_length"] == 180
        assert VIDEO_SPECS["tiktok"]["format"] == "mp4"

    def test_instagram_reel_specs(self):
        assert VIDEO_SPECS["instagram_reel"]["aspect_ratio"] == "9:16"
        assert VIDEO_SPECS["instagram_reel"]["max_length"] == 90

    def test_linkedin_video_specs(self):
        assert VIDEO_SPECS["linkedin_video"]["aspect_ratio"] == "16:9"
        assert VIDEO_SPECS["linkedin_video"]["max_length"] == 600
