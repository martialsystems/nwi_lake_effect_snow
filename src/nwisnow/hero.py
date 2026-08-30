# Copyright (c) 2026 Martial Systems LLC
"""README finding block after the question, before frozen-parent lines."""

from __future__ import annotations

from nwisnow.config import NAMED_MISS, QUESTION


def readme_hero(text: str) -> str:
    body = "\n".join(text.splitlines()[1:]).lstrip()
    if not body.startswith(QUESTION):
        return ""
    rest = body[len(QUESTION) :].lstrip()
    for marker in ("\nAmount science", "\nWrite-up:", "\n## "):
        i = rest.find(marker)
        if i != -1:
            rest = rest[:i]
    return rest.strip()


def hero_logs_named_holes(text: str) -> bool:
    hero = readme_hero(text)
    return all(sid in hero for sid, _city in NAMED_MISS)
