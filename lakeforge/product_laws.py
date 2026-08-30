# Copyright (c) 2026 Martial Systems LLC
"""Refuse laws. Verify-before-done is the finish gate."""

from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from lakeforge.graphs.completeness import build_graph as completeness
    from lakeforge.graphs.inland_bar import build_graph as inland_bar
    from lakeforge.graphs.no_hero import build_graph as no_hero
    from lakeforge.graphs.snow_only import build_graph as snow_only

    return [
        {
            "id": "lake.snow_only",
            "build": snow_only,
            "state": {
                "used_elements": ["SNOW"],
                "prcp_as_snow": False,
                "liquid_as_snow": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "lake.completeness",
            "build": completeness,
            "state": {"complete_frac": 0.80, "incomplete_in_pairs": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "lake.inland_bar",
            "build": inland_bar,
            "state": {
                "inland_id": "USW00093819",
                "same_winter_pairs": True,
                "named_miss_ids": ["USC00125604", "USW00004846"],
                "readme_hero_has_holes": True,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "lake.no_hero",
            "build": no_hero,
            "state": {
                "p_sfha_feature": False,
                "p_sfha_label": False,
                "hero_inches": False,
                "page_in_scope": False,
                "n_figures": 2,
            },
            "allow_decisions": ["allow"],
        },
    ]
