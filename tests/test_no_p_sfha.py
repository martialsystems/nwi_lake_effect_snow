# Copyright (c) 2026 Martial Systems LLC
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_src_does_not_load_p_sfha_raster() -> None:
    hits = []
    for path in (ROOT / "src").rglob("*.py"):
        if path.name == "claims.py":
            continue
        text = path.read_text(encoding="utf-8")
        if "p_sfha.tif" in text or "HAND wet mask" in text:
            hits.append(str(path))
    assert hits == []
