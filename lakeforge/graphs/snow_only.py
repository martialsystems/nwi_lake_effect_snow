# Copyright (c) 2026 Martial Systems LLC
"""Refuse PRCP or liquid as the snow label. Flags must come from the parser."""

from __future__ import annotations

from typing import Any

from lakeforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    used = state.get("used_elements") or []
    if isinstance(used, str):
        used = [used]
    used_l = [str(x) for x in used]
    if "PRCP" in used_l:
        v.append("prcp_as_snow")
    if state.get("prcp_as_snow"):
        v.append("prcp_as_snow")
    if state.get("liquid_as_snow"):
        v.append("liquid_as_snow")
    if used_l and used_l != ["SNOW"]:
        v.append("snow_element")
    if not used_l:
        v.append("snow_element")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="lake.snow_only",
        evaluate=_evaluate,
        extra=["used_elements", "prcp_as_snow", "liquid_as_snow"],
    )
