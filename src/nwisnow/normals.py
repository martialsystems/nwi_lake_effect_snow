# Copyright (c) 2026 Martial Systems LLC
"""1991-2020 monthly snowfall normals. NDJFM is Nov+Dec+Jan+Feb+Mar."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Callable

from nwisnow.config import NDJFM_MONTHS, NORMALS_URL
from nwisnow.errors import FetchError
from nwisnow.http import get_bytes


def parse_ndjfm_snow_normal(text: str) -> float:
    months: dict[int, float] = {}
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "MLY-SNOW-NORMAL" not in reader.fieldnames:
        raise FetchError("normals file missing MLY-SNOW-NORMAL")
    for rec in reader:
        try:
            month = int(float(rec.get("month") or rec.get("DATE") or "0"))
        except ValueError:
            continue
        raw = (rec.get("MLY-SNOW-NORMAL") or "").strip()
        if not raw or raw in {"-9999", ""}:
            continue
        try:
            months[month] = float(raw)
        except ValueError:
            continue
    need = set(NDJFM_MONTHS)
    if not need.issubset(months):
        raise FetchError("NDJFM snowfall normal incomplete")
    return float(sum(months[m] for m in NDJFM_MONTHS))


def load_normal(sid: str, cache_dir: Path, getter: Callable[[str], bytes] = get_bytes) -> float:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / "{0}_normals.csv".format(sid)
    if not path.is_file() or path.stat().st_size == 0:
        body = getter(NORMALS_URL.format(sid=sid))
        if not body:
            raise FetchError("empty normals {0}".format(sid))
        path.write_bytes(body)
    return parse_ndjfm_snow_normal(path.read_text(encoding="utf-8", errors="replace"))
