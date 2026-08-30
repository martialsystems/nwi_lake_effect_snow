# Methodology: NWI lake-belt NDJFM snow vs inland Indianapolis

Question: Does the NWI lake belt get more NDJFM snow days and snow inches than inland Indiana on the same winters?

## Label

GHCND `SNOW` (depth), inches. Not `PRCP`. Not liquid equivalent. Season is Nov 1 through Mar 31. A snow day is daily SNOW ≥ 0.1 in. Drop a station-winter if fewer than 80% of NDJFM days have non-missing SNOW.

## Stations

Science lock `82ce0ce`.

Belt scored: South Bend `USW00014848`, LaPorte `USC00124837`, Indiana Dunes NP `USC00124244`. The belt is those three stations.

Named holes: Michigan City `USC00125604` and Valparaiso Porter County Airport `USW00004846` have no complete NDJFM SNOW in 2011-2025. Do not substitute their liquid catch.

Inland bar: Indianapolis `USW00093819` on the same winters. Not Fort Wayne.

1991-2020 NDJFM snowfall normal is a second column, not the headline bar.

CoCoRaHS snow-depth field was skipped. Daily liquid is not a snow label.

## Split

Measurement on a locked winter list: NDJFM 2010-11 through 2024-25 (winter labeled by the January year). Report every complete winter that exists at both a belt station and Indianapolis. No Ridge. No random day split.

## Figures

1. Paired NDJFM inches: belt vs Indianapolis, 1:1 line.
2. Station map of mean NDJFM inches. Snow depth, not water, not a storm.

## Claims

Allowed: NDJFM station snow days and inches; lake belt vs Indianapolis on the same winters; 1991-2020 normal as a second column; named GHCND holes.

Banned: "Indiana will get N inches"; flood warning; `p_sfha`; unmapped risk; casualty; liquid catch as snow; RadarOnly as a snow label; GaugeCorr; climate attribution slogans.

## Stages

| Stage | Job |
|-------|-----|
| 0 | Fixture winters with planted lake > inland. Completeness floor. No HTTP. |
| A | Fetch GHCND SNOW and 1991-2020 snow normals. Stop on empty SNOW at a pinned belt station. |
| B | Locked winter list. Paired deltas vs Indianapolis. Normal column. Named miss logged. |
| C | Two figures, claim scan, precip gist and index gist. |
