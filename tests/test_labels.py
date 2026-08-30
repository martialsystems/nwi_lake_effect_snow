# Copyright (c) 2026 Martial Systems LLC
from datetime import date

from nwisnow.labels import complete_enough, is_snow_day, ndjfm_ndays, winter_id_of


def test_winter_id_november_belongs_to_next_january() -> None:
    assert winter_id_of(date(2010, 11, 1)) == 2011
    assert winter_id_of(date(2010, 12, 31)) == 2011
    assert winter_id_of(date(2011, 1, 1)) == 2011
    assert winter_id_of(date(2011, 3, 31)) == 2011


def test_snow_day_is_depth_not_trace_liquid() -> None:
    assert is_snow_day(0.10)
    assert not is_snow_day(0.09)
    assert not is_snow_day(0.0)


def test_completeness_uses_ndjfm_length() -> None:
    assert ndjfm_ndays(2011) == 151
    assert ndjfm_ndays(2012) == 152
    assert complete_enough(121, 2011)
    assert not complete_enough(120, 2011)
