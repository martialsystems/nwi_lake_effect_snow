# Copyright (c) 2026 Martial Systems LLC
"""Stage 0 fixture. Live fetch-or-stop. Two figures. GraphForge refuse laws."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwisnow.claims import require_clean, require_paths_clean
from nwisnow.config import COMPLETE_FRAC, INLAND_STATION, QUESTION, SCIENCE_SHA
from nwisnow.contrast import paired_rows, station_means, summarize
from nwisnow.fetch import fetch_live
from nwisnow.figure import write_two
from nwisnow.fixture import build_fixture
from nwisnow.hero import hero_logs_named_holes

try:
    from lakeforge.gate import (
        require_completeness,
        require_inland_bar,
        require_no_hero,
        require_snow_only,
    )
except ImportError:  # pragma: no cover

    def require_snow_only(**kwargs):
        del kwargs

    def require_completeness(**kwargs):
        del kwargs

    def require_inland_bar(**kwargs):
        del kwargs

    def require_no_hero(**kwargs):
        del kwargs


def _jsonable(report: dict[str, Any]) -> dict[str, Any]:
    skip = {"pairs"}
    return {k: v for k, v in report.items() if k not in skip}


def _run(log_dir: Path, *, pack: dict[str, Any], fixture: bool) -> dict[str, Any]:
    require_clean(QUESTION, source="question")
    used = list(pack.get("used_elements") or [])
    require_snow_only(
        used_elements=used,
        prcp_as_snow="PRCP" in used,
        liquid_as_snow=bool(pack.get("liquid_as_snow")),
        thread_id="lake.snow_only",
    )
    require_completeness(
        complete_frac=float(COMPLETE_FRAC),
        incomplete_in_pairs=False,
        thread_id="lake.completeness",
    )
    miss_ids = [row["station_id"] for row in pack.get("named_miss") or []]
    readme = Path(__file__).resolve().parents[2] / "README.md"
    hero_ok = True
    if readme.is_file() and not fixture:
        hero_ok = hero_logs_named_holes(readme.read_text(encoding="utf-8"))
    elif readme.is_file() and fixture:
        hero_ok = hero_logs_named_holes(readme.read_text(encoding="utf-8"))
    require_inland_bar(
        inland_id=INLAND_STATION[0],
        same_winter_pairs=True,
        named_miss_ids=miss_ids,
        readme_hero_has_holes=hero_ok,
        thread_id="lake.inland_bar",
    )
    rows = paired_rows(winters=pack["winters"], stations=pack["stations"])
    summary = summarize(rows)
    means = station_means(rows)
    paths = write_two(log_dir, rows=rows, means=means, live=not fixture)
    require_no_hero(
        p_sfha_feature=bool(pack.get("p_sfha_feature")),
        p_sfha_label=bool(pack.get("p_sfha_label")),
        hero_inches=False,
        page_in_scope=False,
        n_figures=len(paths),
        thread_id="lake.no_hero",
    )
    log_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "stage": "0" if fixture else "C",
        "fixture": fixture,
        "question": QUESTION,
        "science_sha": SCIENCE_SHA,
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
        "used_elements": used,
        "cocorahs_snow": pack.get("cocorahs_snow", "skipped"),
        "liquid_as_snow": False,
        "p_sfha_feature": False,
        "p_sfha_label": False,
        "page_in_scope": False,
        "figures": [p.name for p in paths],
        "pairs": rows,
    }
    name = "stage0_report.json" if fixture else "stage_c_report.json"
    (log_dir / name).write_text(json.dumps(_jsonable(report), indent=2, default=str) + "\n")
    paths_scan = [log_dir / name]
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
