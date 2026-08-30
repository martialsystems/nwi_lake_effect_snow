# Copyright (c) 2026 Martial Systems LLC
import pytest

from nwisnow.claims import require_clean, scan_text
from nwisnow.errors import ClaimBanError


def test_question_is_clean() -> None:
    from nwisnow.config import QUESTION

    assert scan_text(QUESTION) == []


def test_liquid_and_hero_and_p_sfha_fail() -> None:
    assert "hero_in" in scan_text("Indiana will get 40 inches this winter")
    assert "p_sfha" in scan_text("p_sfha overlay")
    assert "unmapped" in scan_text("unmapped risk downtown")
    with pytest.raises(ClaimBanError):
        require_clean("flood warning at Burns Ditch", source="t")
