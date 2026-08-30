# Copyright (c) 2026 Martial Systems LLC
"""GHCND daily SNOW only. PRCP is refused as a snow label."""

from __future__ import annotations

import csv
import gzip
import io
from datetime import date
from pathlib import Path
from typing import Any, Callable

from nwisnow.config import GHCND_STATION_URL, MM_PER_INCH, NDJFM_MONTHS
from nwisnow.errors import FetchError
from nwisnow.http import get_bytes
from nwisnow.labels import complete_enough, is_snow_day, winter_id_of


def snow_in_from_mm(raw: float) -> float:
    return float(raw) / MM_PER_INCH


def parse_snow_daily(text: str) -> list[tuple[date, float]]:
    rows: list[tuple[date, float]] = []
    for rec in csv.reader(io.StringIO(text)):
        if len(rec) < 4:
            continue
        elem = rec[2].strip()
        if elem != "SNOW":
            continue
        qflag = rec[5].strip() if len(rec) > 5 else ""
        if qflag:
            continue
        try:
            raw = int(rec[3])
        except ValueError:
            continue
        if raw == -9999:
            continue
        day = date.fromisoformat("{0}-{1}-{2}".format(rec[1][0:4], rec[1][4:6], rec[1][6:8]))
        if day.month not in NDJFM_MONTHS:
            continue
        rows.append((day, snow_in_from_mm(float(raw))))
    return rows


def load_station_csv(sid: str, cache_dir: Path, getter: Callable[[str], bytes] = get_bytes) -> list[tuple[date, float]]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / "{0}.csv.gz".format(sid)
    if not path.is_file() or path.stat().st_size == 0:
        body = getter(GHCND_STATION_URL.format(sid=sid))
        if not body:
            raise FetchError("empty GHCND {0}".format(sid))
        path.write_bytes(body)
    raw = gzip.decompress(path.read_bytes()).decode("utf-8", errors="replace")
    rows = parse_snow_daily(raw)
    if not rows:
        raise FetchError("empty GHCND SNOW {0}".format(sid))
    return rows


def winter_totals(days: list[tuple[date, float]]) -> dict[int, dict[str, Any]]:
    buckets: dict[int, dict[str, Any]] = {}
    for day, inches in days:
        wid = winter_id_of(day)
        b = buckets.setdefault(wid, {"snow_in": 0.0, "snow_days": 0, "n_present": 0})
        b["snow_in"] += float(inches)
        b["n_present"] += 1
        if is_snow_day(inches):
            b["snow_days"] += 1
    out: dict[int, dict[str, Any]] = {}
    for wid, b in buckets.items():
        if complete_enough(int(b["n_present"]), int(wid)):
            out[int(wid)] = {
                "snow_in": float(b["snow_in"]),
                "snow_days": int(b["snow_days"]),
                "n_present": int(b["n_present"]),
            }
    return out
