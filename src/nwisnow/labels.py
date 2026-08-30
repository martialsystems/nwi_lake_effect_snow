# Copyright (c) 2026 Martial Systems LLC
"""NDJFM winter id and completeness. Snow day is depth, not liquid."""

from __future__ import annotations

import calendar
from datetime import date

from nwisnow.config import COMPLETE_FRAC, SNOW_DAY_IN


def winter_id_of(day: date) -> int:
    return day.year + 1 if day.month in (11, 12) else day.year


def ndjfm_ndays(winter_id: int) -> int:
    feb = 29 if calendar.isleap(int(winter_id)) else 28
    return 30 + 31 + 31 + feb + 31


def complete_enough(n_present: int, winter_id: int, *, floor: float = COMPLETE_FRAC) -> bool:
    return (n_present / float(ndjfm_ndays(winter_id))) >= floor


def is_snow_day(snow_in: float, *, thresh: float = SNOW_DAY_IN) -> bool:
    return float(snow_in) >= float(thresh)
