# Copyright (c) 2026 Martial Systems LLC
from pathlib import Path

from nwisnow.claims import scan_text
from nwisnow.config import PRECIP_GIST, QUESTION, SCIENCE_SHA
from nwisnow.hero import hero_logs_named_holes, readme_hero

REPO = Path(__file__).resolve().parents[1]


def test_readme_opens_with_the_question() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    body = "\n".join(text.splitlines()[1:]).lstrip()
    assert body.startswith(QUESTION)
    hero = readme_hero(text)
    assert SCIENCE_SHA in hero
    assert "31.81" in hero
    assert "9.55" in hero
    assert "0.95" in hero
    assert "+0.45" in hero
    assert "+10.10" in hero
    assert "three stations" in hero
    assert "fatter storms" in hero
    assert hero_logs_named_holes(text)
    assert "USC00125604" in hero
    assert "USW00004846" in hero
    assert "ac36f0f" in text
    assert "1416da1" in text
    assert "6b47f21" in text
    assert "9aa7935" in text
    assert "Open_the_research_console-2e7d32" in text
    assert "martialsystems.github.io/indiana_wx_pages" in text
    assert any(
        "[![Precip writeup]" in line and "[![Open the research console]" in line
        for line in text.splitlines()
    )
    assert PRECIP_GIST.split("/")[-1] in text
    assert ".github/blob/main/RESEARCH.md" not in text
    assert "scatter.png" in text
    assert "station_map.png" in text
    assert scan_text(text) == []
    assert "\u2014" not in text
    assert "What it is not" not in text
