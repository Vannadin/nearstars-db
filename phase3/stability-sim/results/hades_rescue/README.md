# Hades rescue scan — can a minimal orbit change stop the ejection?

The shipped Hades (a = 148,000 km) is chaotically ejected at ~56 kyr, confirmed at two
step sizes (see `../../context-notes.md`, 2026-08-19). This scan asks whether a
**minimal change to Hades' orbit alone** produces a robustly stable placement, so the
moon can stay in the design rather than being moved wholesale or dropped.

Method: step one Hades element, hold everything else at its shipped value, and integrate
each candidate for **1e5 yr** — about twice the observed ejection time — in the exact
validation-cell configuration (leapfrog, 10-min step, C J2 force, 2,000 uniform
snapshots). Verdict = Hill-bound at the end AND e_max < 0.9. `collateral` flags any OTHER
moon that also ejects, which disqualifies a candidate even when Hades itself survives.

Re-run or extend with `scripts/hades_rescue_scan.py` (`--grid MIN:MAX:STEP`,
`--vary FIELD:v1,v2`, `--combo f=v,f=v`). Completed candidates are skipped, so an
interrupted scan resumes for free.

## Result: semi-major axis alone does not work

35 candidates across 122,000–190,000 km. Three survive, none robustly.

| a (km) | Δa | verdict | e_max | nearest low-order resonances | collateral |
|---|---|---|---|---|---|
| 122,000 | -17.6% | ejected | 9.999 | 5:4 Dante (7.0%) · 3:1 Pandora (0.8%) | Dante |
| 124,000 | -16.2% | ejected | 9.999 | 5:4 Dante (4.4%) · 3:1 Pandora (3.3%) | — |
| 126,000 | -14.9% | **BOUND** | 0.548 | 5:4 Dante (2.0%) · 11:4 Pandora (3.0%) | Dante |
| 128,000 | -13.5% | ejected | 9.999 | 5:4 Dante (0.4%) · 11:4 Pandora (0.7%) | — |
| 130,000 | -12.2% | ejected | 9.999 | 5:4 Dante (2.7%) · 8:3 Pandora (1.4%) | — |
| 132,000 | -10.8% | ejected | 9.999 | 4:3 Dante (1.4%) · 8:3 Pandora (0.9%) | — |
| 134,000 | -9.5% | **BOUND** | 0.381 | 4:3 Dante (0.8%) · 8:3 Pandora (3.2%) | Dante |
| 136,000 | -8.1% | ejected | 9.999 | 4:3 Dante (3.0%) · 5:2 Pandora (1.1%) | — |
| 138,000 | -6.8% | ejected | 9.999 | 4:3 Dante (5.1%) · 5:2 Pandora (1.1%) | — |
| 140,000 | -5.4% | ejected | 9.999 | 3:2 Dante (4.5%) · 5:2 Pandora (3.3%) | — |
| 142,000 | -4.1% | ejected | 9.999 | 3:2 Dante (2.3%) · 7:3 Pandora (1.5%) | — |
| 144,000 | -2.7% | ejected | 9.999 | 3:2 Dante (0.1%) · 7:3 Pandora (0.6%) | — |
| 146,000 | -1.4% | ejected | 9.999 | 3:2 Dante (1.9%) · 9:4 Pandora (1.0%) | — |
| 148,000 | +0.0% | ejected | 9.999 | 3:2 Dante (3.9%) · 9:4 Pandora (1.0%) | — |
| 150,000 | +1.4% | **BOUND** | 0.096 | 5:3 Dante (4.7%) · 9:4 Pandora (3.1%) | — |
| 152,000 | +2.7% | ejected | 9.999 | 5:3 Dante (2.6%) · 9:4 Pandora (5.2%) | — |
| 154,000 | +4.1% | ejected | 9.999 | 5:3 Dante (0.6%) · 2:1 Pandora (4.7%) | — |
| 156,000 | +5.4% | ejected | 9.999 | 5:3 Dante (1.3%) · 2:1 Pandora (2.8%) | Dante |
| 158,000 | +6.8% | ejected | 9.999 | 7:4 Dante (1.7%) · 2:1 Pandora (0.9%) | — |
| 160,000 | +8.1% | ejected | 9.999 | 7:4 Dante (0.2%) · 2:1 Pandora (0.9%) | — |
| 162,000 | +9.5% | ejected | 9.999 | 7:4 Dante (2.1%) · 2:1 Pandora (2.8%) | — |
| 164,000 | +10.8% | ejected | 9.999 | 7:4 Dante (3.9%) · 2:1 Pandora (4.8%) | — |
| 166,000 | +12.2% | ejected | 9.999 | 7:4 Dante (5.6%) · 7:4 Pandora (6.7%) | — |
| 168,000 | +13.5% | ejected | 9.999 | 2:1 Dante (6.0%) · 7:4 Pandora (5.0%) | — |
| 170,000 | +14.9% | ejected | 9.999 | 2:1 Dante (4.1%) · 7:4 Pandora (3.3%) | — |
| 172,000 | +16.2% | ejected | 9.999 | 2:1 Dante (2.3%) · 7:4 Pandora (1.6%) | — |
| 174,000 | +17.6% | ejected | 9.999 | 2:1 Dante (0.5%) · 7:4 Pandora (0.2%) | — |
| 176,000 | +18.9% | ejected | 9.999 | 2:1 Dante (1.2%) · 7:4 Pandora (1.9%) | — |
| 178,000 | +20.3% | ejected | 9.999 | 2:1 Dante (2.8%) · 5:3 Pandora (1.3%) | — |
| 180,000 | +21.6% | ejected | 9.999 | 2:1 Dante (4.5%) · 5:3 Pandora (0.4%) | — |
| 182,000 | +23.0% | ejected | 9.999 | 9:4 Dante (5.7%) · 5:3 Pandora (2.1%) | — |
| 184,000 | +24.3% | ejected | 9.999 | 9:4 Dante (4.0%) · 5:3 Pandora (3.7%) | — |
| 186,000 | +25.7% | ejected | 9.999 | 9:4 Dante (2.3%) · 3:2 Pandora (5.1%) | — |
| 188,000 | +27.0% | ejected | 9.999 | 9:4 Dante (0.7%) · 3:2 Pandora (3.6%) | — |
| 190,000 | +28.4% | ejected | 9.999 | 9:4 Dante (0.9%) · 3:2 Pandora (2.0%) | — |
The two inner survivors (126,000 and 134,000 km) eject **Dante** instead and let Hades'
eccentricity run to 0.55 / 0.38 — trading one ejection for another. That left 150,000 km
(+1.4%, e_max 0.096) as the only clean candidate, so it went through a robustness
battery: half the timestep, and three other initial mean anomalies.

| variant | verdict | e_max |
|---|---|---|
| a=150,000 · dt5 | **BOUND** | 0.145 |
| a=150,000 · ma0 | ejected | 9.999 |
| a=150,000 · ma215 | **BOUND** | 0.131 |
| a=150,000 · ma75 | **BOUND** | 0.137 |
**150,000 km fails.** Surviving three of four phases means the candidate sits on the edge
of the chaotic zone, not inside a stable island — it cannot be shipped as canon.

## Why the whole zone is chaotic

Pandora is the cause. At 4.3e24 kg it is 860x Hades' mass and about a 1/170 mass ratio to
Polyphemus — Earth–Moon territory for a satellite system. Its low-order resonances
(3:1, 11:4, 8:3, 5:2, 9:4, 2:1, 7:4, 5:3) tile the entire Dante-to-Pandora corridor, and
the scan shows that landing within ~1% of any of them is fatal while the gaps between
them are too narrow to hold a robust orbit. The 1e4-yr runs of earlier sessions could not
see this: every one of these candidates looks stable on that horizon.

The 3:2 resonance-lock route is already closed for an independent reason — J2's apsidal
precession detunes the marginal libration and the moon ejects at ~510 yr
(`../../STABILITY_REPORT.md`).

## Next: smaller changes than moving the orbit (queued, not yet run)

Hades sits at inclination 11° while Polyphemus' obliquity is 5°, so it is ~6° off its
Laplace plane — a plausible pump for the eccentricity growth, and a one-number change
that leaves the orbit radius as designed. Queued battery (9 runs, ~45 min on 6 cores):

    .venv/bin/python scripts/hades_rescue_scan.py --jobs 6 \
      --vary i:5,7,9,13 --vary e:0,0.01,0.02 \
      --combo "i=5,e=0.01" --combo "a=150000,i=5,e=0.01"

Any survivor there must clear the same robustness battery (half step + three phases)
before it can be called canon.

If that fails too, the remaining options are structural, and the owner picks:
lower Pandora's mass, move Hades outside Pandora, or drop Hades.

## What is stored here

Per-candidate `alpha_centauri_summary.json`, its `hypotheticals.json`, and `run.log`.
The 2,000-snapshot `alpha_centauri_timeseries.csv` files are **gitignored for this
directory only** (1.3 MB x 40 = 52 MB of scan intermediate); every verdict in the tables
above comes from the summaries, and a candidate worth plotting can be re-run from its
stored `hypotheticals.json`.
