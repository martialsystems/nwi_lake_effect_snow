# Copyright (c) 2026 Martial Systems LLC
"""Planted lake-belt snow over Indianapolis. Does not rescue live."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from nwisnow.config import BELT_STATIONS, INLAND_STATION, SAMPLE_FIRST_WINTER
from nwisnow.ghcnd import winter_totals
from nwisnow.labels import winter_id_of


def _ndjfm_days(winter_id: int) -> list[date]:
    start = date(winter_id - 1, 11, 1)
    end = date(winter_id, 3, 31)
    days: list[date] = []
    cur = start
    while cur <= end:
        days.append(cur)
        cur += timedelta(days=1)
    return days


def _snow_series(*, belt: bool, winter_id: int) -> list[tuple[date, float]]:
    days = _ndjfm_days(winter_id)
    out: list[tuple[date, float]] = []
    for i, day in enumerate(days):
        assert winter_id_of(day) == winter_id
        if belt:
            inches = 0.8 if i % 3 == 0 else 0.0
        else:
            inches = 0.2 if i % 6 == 0 else 0.0
        out.append((day, inches))
    return out


def build_fixture() -> dict[str, Any]:
    stations = {
        "USW00014848": {"lat": 41.7072, "lon": -86.3164, "city": "South Bend"},
        "USC00124837": {"lat": 41.6117, "lon": -86.7297, "city": "LaPorte"},
        "USC00124244": {"lat": 41.6317, "lon": -87.0881, "city": "Indiana Dunes"},
        "USW00093819": {"lat": 39.7075, "lon": -86.2803, "city": "Indianapolis"},
    }
    winters: dict[str, dict[int, dict[str, Any]]] = {}
    sample = list(range(SAMPLE_FIRST_WINTER, SAMPLE_FIRST_WINTER + 8))
    for sid, _city in BELT_STATIONS:
        winters[sid] = {}
        for wid in sample:
            winters[sid].update(winter_totals(_snow_series(belt=True, winter_id=wid)))
    inland = INLAND_STATION[0]
    winters[inland] = {}
    for wid in sample:
        winters[inland].update(winter_totals(_snow_series(belt=False, winter_id=wid)))
    normals = {
        "USW00014848": 40.0,
        "USC00124837": 42.0,
        "USC00124244": 38.0,
        "USW00093819": 20.0,
    }
    return {
        "source": "fixture",
        "stations": stations,
        "winters": winters,
        "normals": normals,
        "cocorahs_snow": "skipped",
        "liquid_as_snow": False,
    }
