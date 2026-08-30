# Copyright (c) 2026 Martial Systems LLC
"""Live GHCND SNOW + NDJFM normals. Empty SNOW stops. Liquid is not snow."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from nwisnow.config import BELT_STATIONS, INLAND_STATION, NAMED_MISS
from nwisnow.errors import FetchError
from nwisnow.ghcnd import load_station_csv, winter_totals
from nwisnow.http import get_bytes
from nwisnow.normals import load_normal

STATION_META = {
    "USW00014848": {"lat": 41.7072, "lon": -86.3164, "city": "South Bend"},
    "USC00124837": {"lat": 41.6117, "lon": -86.7297, "city": "LaPorte"},
    "USC00124244": {"lat": 41.6317, "lon": -87.0881, "city": "Indiana Dunes"},
    "USW00093819": {"lat": 39.7075, "lon": -86.2803, "city": "Indianapolis"},
}


def fetch_live(cache_dir: Path, getter: Callable[[str], bytes] = get_bytes) -> dict[str, Any]:
    wanted = list(BELT_STATIONS) + [INLAND_STATION]
    winters: dict[str, dict[int, dict[str, Any]]] = {}
    normals: dict[str, float] = {}
    stations: dict[str, dict[str, Any]] = {}
    for sid, city in wanted:
        days = load_station_csv(sid, cache_dir, getter=getter)
        w = winter_totals(days)
        if not w:
            raise FetchError("no complete NDJFM SNOW winters {0}".format(sid))
        winters[sid] = w
        normals[sid] = load_normal(sid, cache_dir, getter=getter)
        meta = dict(STATION_META[sid])
        meta["city"] = city
        stations[sid] = meta
    return {
        "source": "live",
        "stations": stations,
        "winters": winters,
        "normals": normals,
        "named_miss": [
            {"station_id": sid, "city": city, "reason": "no complete NDJFM SNOW in 2011-2025"}
            for sid, city in NAMED_MISS
        ],
        "cocorahs_snow": "skipped",
        "liquid_as_snow": False,
        "product": "GHCND SNOW",
        "cache_dir": str(cache_dir),
    }
