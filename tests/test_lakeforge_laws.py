# Copyright (c) 2026 Martial Systems LLC
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from lakeforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from lakeforge.gate import require_completeness, require_inland_bar, require_no_hero, require_snow_only
from lakeforge.product_laws import laws


def test_laws() -> None:
    require_snow_only(used_elements=["SNOW"], thread_id="t.s.ok")
    with pytest.raises(LawBlockedError):
        require_snow_only(used_elements=["PRCP"], prcp_as_snow=True, thread_id="t.s.prcp")
    with pytest.raises(LawBlockedError):
        require_snow_only(liquid_as_snow=True, thread_id="t.s.liq")
    require_completeness(complete_frac=0.80, thread_id="t.c.ok")
    with pytest.raises(LawBlockedError):
        require_completeness(complete_frac=0.50, thread_id="t.c.lo")
    require_inland_bar(thread_id="t.i.ok")
    with pytest.raises(LawBlockedError):
        require_inland_bar(inland_id="USW00014827", thread_id="t.i.fw")
    with pytest.raises(LawBlockedError):
        require_inland_bar(named_miss_ids=[], readme_hero_has_holes=True, thread_id="t.i.miss")
    with pytest.raises(LawBlockedError):
        require_inland_bar(readme_hero_has_holes=False, thread_id="t.i.hero")
    require_no_hero(n_figures=2, page_in_scope=False, thread_id="t.h.ok")
    with pytest.raises(LawBlockedError):
        require_no_hero(page_in_scope=True, thread_id="t.h.page")
    with pytest.raises(LawBlockedError):
        require_no_hero(p_sfha_feature=True, thread_id="t.h.p")
    with pytest.raises(LawBlockedError):
        require_no_hero(hero_inches=True, thread_id="t.h.in")
    assert {row["id"] for row in laws()} == {
        "lake.snow_only",
        "lake.completeness",
        "lake.inland_bar",
        "lake.no_hero",
    }
