# Copyright (c) 2026 Martial Systems LLC
"""Call sites for refuse laws."""

from __future__ import annotations

from typing import Any

from lakeforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from lakeforge.graphs.completeness import build_graph as build_complete
from lakeforge.graphs.inland_bar import build_graph as build_inland
from lakeforge.graphs.no_hero import build_graph as build_hero
from lakeforge.graphs.snow_only import build_graph as build_snow


def require_snow_only(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "lake_snow"))
    state = {
        "used_elements": ["SNOW"],
        "prcp_as_snow": False,
        "liquid_as_snow": False,
    }
    state.update(flags)
    require_law(
        build_snow(),
        state,
        allow_decisions=["allow"],
        law_id="lake.snow_only",
        thread_id=thread_id,
        raise_error=True,
    )


def require_completeness(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "lake_complete"))
    state = {
        "complete_frac": 0.80,
        "incomplete_in_pairs": False,
    }
    state.update(flags)
    require_law(
        build_complete(),
        state,
        allow_decisions=["allow"],
        law_id="lake.completeness",
        thread_id=thread_id,
        raise_error=True,
    )


def require_inland_bar(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "lake_inland"))
    state = {
        "inland_id": "USW00093819",
        "same_winter_pairs": True,
        "named_miss_ids": ["USC00125604", "USW00004846"],
        "readme_hero_has_holes": True,
    }
    state.update(flags)
    require_law(
        build_inland(),
        state,
        allow_decisions=["allow"],
        law_id="lake.inland_bar",
        thread_id=thread_id,
        raise_error=True,
    )


def require_no_hero(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "lake_hero"))
    state = {
        "p_sfha_feature": False,
        "p_sfha_label": False,
        "hero_inches": False,
        "page_in_scope": False,
        "n_figures": 2,
    }
    state.update(flags)
    require_law(
        build_hero(),
        state,
        allow_decisions=["allow"],
        law_id="lake.no_hero",
        thread_id=thread_id,
        raise_error=True,
    )
