# Copyright (c) 2026 Martial Systems LLC
"""Same-winter lake belt minus Indianapolis. Inches and snow days."""

from __future__ import annotations

from typing import Any

from nwisnow.config import BELT_STATIONS, INLAND_STATION, SAMPLE_FIRST_WINTER, SAMPLE_LAST_WINTER


def paired_rows(
    *,
    winters: dict[str, dict[int, dict[str, Any]]],
    stations: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    inland_id = INLAND_STATION[0]
    inland = winters.get(inland_id) or {}
    rows: list[dict[str, Any]] = []
    for sid, city in BELT_STATIONS:
        belt = winters.get(sid) or {}
        meta = stations[sid]
        for wid, b in sorted(belt.items()):
            if wid < SAMPLE_FIRST_WINTER or wid > SAMPLE_LAST_WINTER:
                continue
            ind = inland.get(wid)
            if ind is None:
                continue
            rows.append(
                {
                    "station_id": sid,
                    "city": city,
                    "lat": meta["lat"],
                    "lon": meta["lon"],
                    "winter_id": int(wid),
                    "belt_in": float(b["snow_in"]),
                    "belt_days": int(b["snow_days"]),
                    "inland_in": float(ind["snow_in"]),
                    "inland_days": int(ind["snow_days"]),
                    "delta_in": float(b["snow_in"]) - float(ind["snow_in"]),
                    "delta_days": int(b["snow_days"]) - int(ind["snow_days"]),
                }
            )
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "n_pairs": 0,
            "mean_delta_in": None,
            "mean_delta_days": None,
            "share_belt_gt_inland_in": None,
            "share_belt_gt_inland_days": None,
        }
    n = len(rows)
    d_in = [r["delta_in"] for r in rows]
    d_days = [r["delta_days"] for r in rows]
    return {
        "n_pairs": n,
        "mean_delta_in": sum(d_in) / n,
        "mean_delta_days": sum(d_days) / n,
        "share_belt_gt_inland_in": sum(1 for x in d_in if x > 0) / n,
        "share_belt_gt_inland_days": sum(1 for x in d_days if x > 0) / n,
    }


def station_means(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by.setdefault(r["station_id"], []).append(r)
    out: list[dict[str, Any]] = []
    for sid, grp in by.items():
        n = len(grp)
        out.append(
            {
                "station_id": sid,
                "city": grp[0]["city"],
                "lat": grp[0]["lat"],
                "lon": grp[0]["lon"],
                "n": n,
                "mean_belt_in": sum(r["belt_in"] for r in grp) / n,
                "mean_inland_in": sum(r["inland_in"] for r in grp) / n,
                "mean_delta_in": sum(r["delta_in"] for r in grp) / n,
                "mean_delta_days": sum(r["delta_days"] for r in grp) / n,
            }
        )
    inland_rows = [r for r in rows]
    if inland_rows:
        # Indianapolis as a map point: mean of the inland inches across pairs (unique winters).
        winters = {}
        for r in inland_rows:
            winters[r["winter_id"]] = r["inland_in"]
        if winters:
            from nwisnow.fetch import STATION_META

            inland_meta = STATION_META[INLAND_STATION[0]]
            out.append(
                {
                    "station_id": INLAND_STATION[0],
                    "city": INLAND_STATION[1],
                    "lat": inland_meta["lat"],
                    "lon": inland_meta["lon"],
                    "n": len(winters),
                    "mean_belt_in": sum(winters.values()) / len(winters),
                    "mean_inland_in": sum(winters.values()) / len(winters),
                    "mean_delta_in": 0.0,
                    "mean_delta_days": 0.0,
                }
            )
    return out
