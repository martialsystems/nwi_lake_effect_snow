# Copyright (c) 2026 Martial Systems LLC
"""No p_sfha. No winter-page hero inches from this contrast."""

from __future__ import annotations

from typing import Any

from lakeforge.graphs._common import binary_graph

_FLAGS = ("p_sfha_feature", "p_sfha_label", "hero_inches", "page_in_scope")


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v = [k for k in _FLAGS if state.get(k)]
    n = int(state.get("n_figures") or 0)
    if n > 2:
        v.append("figure_cap")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="lake.no_hero",
        evaluate=_evaluate,
        extra=[*_FLAGS, "n_figures"],
    )
