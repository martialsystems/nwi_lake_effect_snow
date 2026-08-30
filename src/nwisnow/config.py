# Copyright (c) 2026 Martial Systems LLC
"""Locked NDJFM lake-belt snow vs inland Indianapolis. Snow depth, not liquid."""

from __future__ import annotations

from pathlib import Path

QUESTION = (
    "Does the NWI lake belt get more NDJFM snow days and snow inches "
    "than inland Indiana on the same winters?"
)
USER_AGENT = "MartialSystemsResearch/nwi_lake_effect_snow"
MAX_FIGURES = 2
MM_PER_INCH = 25.4
COMPLETE_FRAC = 0.80
SNOW_DAY_IN = 0.10
SAMPLE_FIRST_WINTER = 2011  # NDJFM 2010-11
SAMPLE_LAST_WINTER = 2025  # NDJFM 2024-25
NORMAL_FIRST = 1991
NORMAL_LAST = 2020
BELT_STATIONS = (
    ("USW00014848", "South Bend"),
    ("USC00124837", "LaPorte"),
    ("USC00124244", "Indiana Dunes"),
)
NAMED_MISS = (
    ("USC00125604", "Michigan City"),
    ("USW00004846", "Valparaiso"),
)
INLAND_STATION = ("USW00093819", "Indianapolis")
NDJFM_MONTHS = (11, 12, 1, 2, 3)
GHCND_STATION_URL = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/by_station/{sid}.csv.gz"
GHCND_STATIONS_URL = "https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
NORMALS_URL = "https://www.ncei.noaa.gov/data/normals-monthly/1991-2020/access/{sid}.csv"
INDEX_GIST = "https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3"
PRECIP_GIST = "https://gist.github.com/martialsystems/b5f900aad37487bb8c0206a321c1ed5c"
AMOUNT_SHA = "ac36f0f"
JJA_MISS_SHA = "1416da1"
WINTER_LAKE_SHA = "6b47f21"
DJF_SNOW_SHA = "9aa7935"
REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_SCATTER_SUBTITLE = (
    "Fixture planted lake-belt snow over Indianapolis. Does not rescue live."
)
FIXTURE_MAP_SUBTITLE = "Fixture mean NDJFM inches. Does not rescue live."
LIVE_SCATTER_SUBTITLE = (
    "NDJFM snow inches. Lake belt vs Indianapolis on the same winters. Snow depth, not liquid."
)
LIVE_MAP_SUBTITLE = (
    "Mean NDJFM snow inches. Snow depth, not water, not a storm."
)
