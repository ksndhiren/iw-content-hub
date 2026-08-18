"""Tests for the graphics producer agent."""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.graphics_producer import (
    generate_graphics,
    PLATFORM_DIMENSIONS,
    TEMPLATE_TYPES,
)


class TestGenerateGraphics:
    def test_dry_run_instagram(self):
        result = generate_graphics(
            platform="instagram",
            topic="50K remote jobs this week",
            goal="awareness",
            template_type="stat_card",
            dry_run=True,
        )
        assert result["platform"] == "instagram"
        assert result["template"] == "stat_card"
        assert result["dimensions"] == "1080x1080"
        assert result["brand_compliant"] is True
        assert result["mock"] is True

    def test_dry_run_linkedin(self):
        result = generate_graphics(
            platform="linkedin",
            topic="Top hiring companies",
            goal="engagement",
            template_type="employer_spotlight",
            dry_run=True,
        )
        assert result["platform"] == "linkedin"
        assert result["dimensions"] == "1200x627"

    def test_dry_run_tiktok(self):
        result = generate_graphics(
            platform="tiktok",
            topic="Resume tips",
            goal="awareness",
            template_type="tip_card",
            dry_run=True,
        )
        assert result["dimensions"] == "1080x1920"


class TestPlatformDimensions:
    def test_all_platforms_defined(self):
        for platform in ["linkedin", "instagram", "x", "tiktok"]:
            assert platform in PLATFORM_DIMENSIONS
            assert "size" in PLATFORM_DIMENSIONS[platform]
            assert "format" in PLATFORM_DIMENSIONS[platform]


class TestTemplateTypes:
    def test_all_template_types_defined(self):
        expected = ["stat_card", "job_spotlight", "employer_spotlight", "tip_card", "carousel"]
        for t in expected:
            assert t in TEMPLATE_TYPES
