# Copyright (c) 2026 Martial Systems LLC
"""Refuse a completeness floor under 80%."""

from __future__ import annotations

from typing import Any

from lakeforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    floor = float(state.get("complete_frac") or 0.0)
    if floor + 1e-12 < 0.80:
        v.append("complete_frac")
    if state.get("incomplete_in_pairs"):
        v.append("incomplete_in_pairs")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="lake.completeness",
        evaluate=_evaluate,
        extra=["complete_frac", "incomplete_in_pairs"],
    )
