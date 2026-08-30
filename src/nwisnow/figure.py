# Copyright (c) 2026 Martial Systems LLC
"""Two figures: paired scatter, station mean inches map."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from nwisnow.claims import require_clean
from nwisnow.config import (
    FIXTURE_MAP_SUBTITLE,
    FIXTURE_SCATTER_SUBTITLE,
    LIVE_MAP_SUBTITLE,
    LIVE_SCATTER_SUBTITLE,
    MAX_FIGURES,
)
from nwisnow.errors import FigureCapError


def _cap(n: int) -> None:
    if n > MAX_FIGURES:
        raise FigureCapError("this tree stops at {0} figures".format(MAX_FIGURES))


def write_scatter(dest: Path, *, rows: list[dict[str, Any]], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig1_title")
    require_clean(subtitle, source="fig1_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = {
        "USW00014848": "#1d4ed8",
        "USC00124837": "#b45309",
        "USC00124244": "#047857",
    }
    fig, ax = plt.subplots(figsize=(6.4, 6.2))
    xs: list[float] = []
    ys: list[float] = []
    for sid, color in colors.items():
        pts = [r for r in rows if r["station_id"] == sid]
        if not pts:
            continue
        x = [r["inland_in"] for r in pts]
        y = [r["belt_in"] for r in pts]
        xs.extend(x)
        ys.extend(y)
        ax.scatter(x, y, s=28, c=color, label=pts[0]["city"], zorder=3)
    lo = min(xs + ys)
    hi = max(xs + ys)
    pad = 0.05 * (hi - lo + 1.0)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="#0f172a", lw=1.0, label="1:1")
    ax.set_xlabel("Indianapolis NDJFM snow (in)")
    ax.set_ylabel("lake-belt NDJFM snow (in)")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.subplots_adjust(bottom=0.16, top=0.92)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return dest


def write_map(dest: Path, *, means: list[dict[str, Any]], title: str, subtitle: str) -> Path:
    require_clean(title, source="fig2_title")
    require_clean(subtitle, source="fig2_sub")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lon = [r["lon"] for r in means]
    lat = [r["lat"] for r in means]
    val = [r["mean_belt_in"] for r in means]
    fig, ax = plt.subplots(figsize=(6.6, 6.8))
    sc = ax.scatter(
        lon,
        lat,
        c=val,
        cmap="Blues",
        s=64,
        edgecolors="#0f172a",
        zorder=3,
    )
    for r in means:
        ax.annotate(r["city"], (r["lon"], r["lat"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("lon")
    ax.set_ylabel("lat")
    ax.set_title(title, fontsize=10)
    fig.colorbar(sc, ax=ax, shrink=0.72, label="mean NDJFM inches")
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.subplots_adjust(bottom=0.16, top=0.92)
    fig.text(0.5, 0.04, subtitle, ha="center", fontsize=8)
    fig.savefig(dest, dpi=130, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return dest


def write_two(log_dir: Path, *, rows: list[dict[str, Any]], means: list[dict[str, Any]], live: bool) -> list[Path]:
    paths = [
        write_scatter(
            log_dir / "scatter.png",
            rows=rows,
            title="NDJFM snow inches, same winters",
            subtitle=LIVE_SCATTER_SUBTITLE if live else FIXTURE_SCATTER_SUBTITLE,
        ),
        write_map(
            log_dir / "station_map.png",
            means=means,
            title="Mean NDJFM snow inches",
            subtitle=LIVE_MAP_SUBTITLE if live else FIXTURE_MAP_SUBTITLE,
        ),
    ]
    _cap(len(paths))
    return paths
