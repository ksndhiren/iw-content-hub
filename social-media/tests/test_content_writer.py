"""Tests for the content writer agent."""

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.content_writer import generate_copy, _parse_json_output, CHAR_LIMITS


class TestGenerateCopy:
    def test_dry_run_linkedin(self):
        result = generate_copy(
            platform="linkedin",
            topic="Remote work trends",
            audience="tech professionals",
            goal="awareness",
            dry_run=True,
        )
        assert result["platform"] == "linkedin"
        assert result["mock"] is True
        assert "hashtags" in result
        assert "cta" in result
        assert result["tone"] == "professional"

    def test_dry_run_instagram(self):
        result = generate_copy(
            platform="instagram",
            topic="Top 5 resume tips",
            audience="job seekers",
            goal="engagement",
            dry_run=True,
        )
        assert result["platform"] == "instagram"
        assert result["tone"] == "casual"

    def test_dry_run_x(self):
        result = generate_copy(
            platform="x",
            topic="Hiring surges in AI",
            audience="developers",
            goal="awareness",
            dry_run=True,
        )
        assert result["platform"] == "x"
        assert result["tone"] == "casual"

    def test_dry_run_with_tone_override(self):
        result = generate_copy(
            platform="linkedin",
            topic="New feature launch",
            audience="recruiters",
            goal="conversion",
            tone_override="excited and urgent",
            dry_run=True,
        )
        assert result["mock"] is True
        assert "cta" in result


class TestParseJsonOutput:
    def test_parse_clean_json(self):
        text = '{"platform": "linkedin", "copy": "Hello", "hashtags": ["#test"], "cta": "Click", "char_count": 5, "tone": "professional"}'
        result = _parse_json_output(text, "linkedin")
        assert result["platform"] == "linkedin"
        assert result["copy"] == "Hello"

    def test_parse_json_in_code_block(self):
        text = '```json\n{"platform": "x", "copy": "Tweet", "hashtags": [], "cta": "", "char_count": 5, "tone": "casual"}\n```'
        result = _parse_json_output(text, "x")
        assert result["platform"] == "x"

    def test_parse_plain_text_fallback(self):
        text = "This is not JSON at all"
        result = _parse_json_output(text, "instagram")
        assert result["parse_error"] is True
        assert result["platform"] == "instagram"

    def test_truncation_for_x(self):
        long_copy = "A" * 500
        text = json.dumps({
            "platform": "x",
            "copy": long_copy,
            "hashtags": [],
            "cta": "",
            "char_count": 500,
            "tone": "casual",
        })
        result = _parse_json_output(text, "x")
        assert len(result["copy"]) <= CHAR_LIMITS["x"]
        assert result.get("truncated") is True


class TestCharLimits:
    def test_all_platforms_have_limits(self):
        for platform in ["linkedin", "x", "instagram", "tiktok"]:
            assert platform in CHAR_LIMITS
            assert isinstance(CHAR_LIMITS[platform], int)
