# Copyright (c) 2026 Martial Systems LLC
from datetime import date

from nwisnow.ghcnd import parse_snow_daily, snow_in_from_mm, winter_totals
from nwisnow.labels import is_snow_day


def test_prcp_rows_are_not_snow() -> None:
    text = (
        "USC00125604,20110101,PRCP,250,,,\n"
        "USC00125604,20110101,SNOW,25,,,\n"
        "USC00125604,20110102,SNOW,-9999,,,\n"
    )
    rows = parse_snow_daily(text)
    assert len(rows) == 1
    assert rows[0][0] == date(2011, 1, 1)
    assert abs(snow_in_from_mm(25.0) - rows[0][1]) < 1e-9
    assert is_snow_day(rows[0][1])


def test_june_snow_is_out_of_ndjfm() -> None:
    text = "USW00014848,20110601,SNOW,250,,,\n"
    assert parse_snow_daily(text) == []


def test_winter_totals_need_completeness() -> None:
    days = [(date(2011, 1, 1), 1.0)]
    assert winter_totals(days) == {}
