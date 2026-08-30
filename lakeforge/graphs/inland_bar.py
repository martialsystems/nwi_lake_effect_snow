# Copyright (c) 2026 Martial Systems LLC
"""Indianapolis same-winter bar. Named Michigan City / Valpo holes stay in the hero."""

from __future__ import annotations

from typing import Any

from lakeforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if str(state.get("inland_id") or "") != "USW00093819":
        v.append("inland_id")
    if not state.get("same_winter_pairs"):
        v.append("same_winter_pairs")
    miss = state.get("named_miss_ids") or []
    if isinstance(miss, str):
        miss = [miss]
    miss_s = {str(x) for x in miss}
    if "USC00125604" not in miss_s or "USW00004846" not in miss_s:
        v.append("named_miss")
    if not state.get("readme_hero_has_holes"):
        v.append("readme_hero_has_holes")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="lake.inland_bar",
        evaluate=_evaluate,
        extra=["inland_id", "same_winter_pairs", "named_miss_ids", "readme_hero_has_holes"],
    )
