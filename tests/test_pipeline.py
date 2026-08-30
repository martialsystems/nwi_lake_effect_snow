# Copyright (c) 2026 Martial Systems LLC
from pathlib import Path

from nwisnow.pipeline import stage0_fixture


def test_fixture_plants_lake_over_inland(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["fixture"] is True
    assert report["n_pairs"] > 0
    assert report["mean_delta_in"] > 5.0
    assert report["mean_delta_days"] > 0
    assert report["share_belt_gt_inland_in"] == 1.0
    assert report["liquid_as_snow"] is False
    assert report["cocorahs_snow"] == "skipped"
    assert report["figures"] == ["scatter.png", "station_map.png"]
    assert (tmp_path / "scatter.png").is_file()
    assert (tmp_path / "station_map.png").is_file()
    assert (tmp_path / "stage0_report.json").is_file()
