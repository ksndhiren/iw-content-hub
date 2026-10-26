"""The education outro slide must print internwise.co.uk exactly once.

The address lives in each world's own chrome (the accent pill, or the footer on
the singles). The writer also used to be asked for a cta "pointing to
internwise.co.uk", and render_education APPENDED the URL when it was missing, so
the final slide carried the address twice - once in the sentence, once in the
pill - and the sentence itself degraded to "Discover more at internwise.co.uk",
which says nothing about the lesson just taught.
"""

import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import lane_education as E

COPY = {"eyebrow": "Quick Check", "headline": "Evaluate Internships Fast",
        "tone": "practical",
        "slides": [{"tag": "Skills", "title": "Real skills", "body": "Body copy."}] * 3,
        "points": ["One", "Two", "Three"]}


class TestCloseLine:
    @pytest.mark.parametrize("cta,expected", [
        ("Explore more internships at internwise.co.uk", "Explore more internships."),
        ("Strengthen your pitch at internwise.co.uk", "Strengthen your pitch."),
        ("Find your internship at www.internwise.co.uk", "Find your internship."),
        ("Build a CV that gets read. Start today.", "Build a CV that gets read. Start today."),
    ])
    def test_strips_the_address_and_keeps_the_sentence(self, cta, expected):
        assert E.close_line(cta) == expected

    @pytest.mark.parametrize("cta", [
        "Discover more at internwise.co.uk",   # nothing left but a stub
        "Explore more at internwise.co.uk",
        "internwise.co.uk",
        "",
        None,
    ])
    def test_a_bare_address_becomes_a_conclusive_line(self, cta):
        line = E.close_line(cta)
        assert "internwise" not in line.lower()
        assert line == E.FALLBACK_CTA

    def test_never_leaves_the_address_in_the_sentence(self):
        for cta in ("Go to internwise.co.uk", "Visit internwise.co.uk today",
                    "Compare roles on internwise.co.uk."):
            assert "internwise" not in E.close_line(cta).lower()


class TestOutroChrome:
    @pytest.mark.parametrize("world", sorted(E.CAROUSEL))
    def test_address_appears_exactly_once(self, world):
        copy = {**COPY, "cta": E.close_line("Discover more at internwise.co.uk")}
        html = E.CAROUSEL[world]["cta"](E.PAL[world], copy, 5, "nuno_dothis_5")
        assert html.count("internwise.co.uk") == 1


class TestSingleChrome:
    """A single slide has no outro, so its one slide must carry the address. Five
    of these worlds printed it ONLY inside the cta sentence, so stripping the
    duplicate left them with no address at all."""

    @pytest.mark.parametrize("world", sorted(E.SINGLE))
    def test_address_appears_exactly_once(self, world):
        copy = {**COPY, "points": ["One", "Two", "Three", "Four"],
                "cta": E.close_line("Explore more at internwise.co.uk")}
        assert E.SINGLE[world](copy).count("internwise.co.uk") == 1


class TestNunoWidth:
    def test_landscape_cutout_is_reined_in(self):
        # nuno_cv_8 is 1.47:1; at h=740 it would be ~1086px on a 1080px canvas.
        assert E._fit_h("nuno_cv_8", 740, E.MAX_NUNO_W) < 740

    def test_portrait_cutout_is_untouched(self):
        assert E._fit_h("nuno_dothis_5", 740, E.MAX_NUNO_W) == 740

    def test_unknown_pose_falls_back_to_the_requested_height(self):
        assert E._fit_h("nuno_does_not_exist", 740, E.MAX_NUNO_W) == 740
