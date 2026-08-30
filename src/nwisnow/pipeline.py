# Copyright (c) 2026 Martial Systems LLC
"""Stage 0 fixture. Live fetch-or-stop. Two figures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwisnow.claims import require_clean, require_paths_clean
from nwisnow.config import QUESTION
from nwisnow.contrast import paired_rows, station_means, summarize
from nwisnow.fetch import fetch_live
from nwisnow.figure import write_two
from nwisnow.fixture import build_fixture


def _jsonable(report: dict[str, Any]) -> dict[str, Any]:
    skip = {"pairs"}
    return {k: v for k, v in report.items() if k not in skip}


def _run(log_dir: Path, *, pack: dict[str, Any], fixture: bool) -> dict[str, Any]:
    require_clean(QUESTION, source="question")
    if pack.get("liquid_as_snow"):
        raise ValueError("liquid catch is not a snow label")
    rows = paired_rows(winters=pack["winters"], stations=pack["stations"])
    summary = summarize(rows)
    means = station_means(rows)
    paths = write_two(log_dir, rows=rows, means=means, live=not fixture)
    log_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "stage": "0" if fixture else "C",
        "fixture": fixture,
        "question": QUESTION,
        "source": pack["source"],
        "units": "inches",
        "n_pairs": summary["n_pairs"],
        "mean_delta_in": summary["mean_delta_in"],
        "mean_delta_days": summary["mean_delta_days"],
        "share_belt_gt_inland_in": summary["share_belt_gt_inland_in"],
        "share_belt_gt_inland_days": summary["share_belt_gt_inland_days"],
        "normals": pack["normals"],
        "station_means": means,
        "named_miss": pack.get("named_miss", []),
        "cocorahs_snow": pack.get("cocorahs_snow", "skipped"),
        "liquid_as_snow": False,
        "p_sfha_feature": False,
        "p_sfha_label": False,
        "figures": [p.name for p in paths],
        "pairs": rows,
    }
    name = "stage0_report.json" if fixture else "stage_c_report.json"
    (log_dir / name).write_text(json.dumps(_jsonable(report), indent=2, default=str) + "\n")
    paths_scan = [log_dir / name]
    readme = Path(__file__).resolve().parents[2] / "README.md"
    if readme.is_file():
        paths_scan.append(readme)
    require_paths_clean(paths_scan)
    return report


def stage0_fixture(log_dir: Path) -> dict[str, Any]:
    return _run(log_dir, pack=build_fixture(), fixture=True)


def run_live(log_dir: Path, *, cache_dir: Path) -> dict[str, Any]:
    pack = fetch_live(cache_dir=cache_dir)
    extra = {"live": {"n_stations": len(pack["stations"]), "product": pack["product"]}}
    report = _run(log_dir, pack=pack, fixture=False)
    report.update(extra)
    name = log_dir / "stage_c_report.json"
    payload = json.loads(name.read_text(encoding="utf-8"))
    payload["live"] = extra["live"]
    name.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    return report
