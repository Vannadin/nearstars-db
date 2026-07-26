# Hades low-e scan (2026-07-26)

Question: can Hades's eccentricity be lowered enough to keep a cold (225 K) dark
surface, without killing Dante's forced eccentricity (its perpetual volcanism
depends on perturbations from the neighbouring moons)?

Answer: **no.** Hades's eccentricity is forced, not set by its initial value.

Settings identical to the 2026-06-21 design-of-record `_final32b`:

    scripts/run.py --system alpha_centauri --hypotheticals hypotheticals/_hades_eNNN.json \
      --acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16 --j2 0.023 --integrator trace --years 1000

| Hades e_init | Hades e range | Hades e_max | Dante e range | verdict |
|---|---|---|---|---|
| 0.05 (`_final32b`) | — | 0.0641 | 0.0002–0.031 | STABLE |
| 0.005 | 0.0044–0.0641 | 0.0641 | 0.0009–0.0301 | STABLE |
| 0.010 | 0.0031–0.0514 | 0.0514 | 0.0008–0.0289 | STABLE |
| 0.020 | 0.0096–0.0473 | 0.0473 | 0.0027–0.0279 | STABLE |

Dropping e_init by 10× leaves e_max exactly at the design-of-record value. e_max
is in fact *lowest* at e_init = 0.020, which reads as the free component partly
cancelling a forced component of roughly 0.02–0.03. The perturber is Pandora:
860× Hades's mass, period ratio 2.22.

Dante survives in all three (e_max 0.028–0.030 against 0.034 in the
design-of-record), so lowering Hades did **not** starve Dante's volcanism. The
option fails for the other reason.

Measured e_rms from the e005 timeseries: Dante 0.0186, **Hades 0.0385**,
Pandora 0.0044, Cassandra 0.0484. The Hades value feeds the Hades
`bulk.tidal_heating` row and
[`docs/reference/moon-energy-budget-methodology.md`](../../../../docs/reference/moon-energy-budget-methodology.md).

Consequence recorded on the board: at e_rms 0.0385 the rocky `k₂/Q` band
(1e-3–1e-2) gives 207–2071 W/m², i.e. 15–146× Io, against 141 W/m² of absorbed
starlight. Hades cannot be a 225 K body in this architecture; the owner took the
band's low end (207 W/m², T_eq 278 K) and dropped the ancient cratered terrain.

Caveat: the three runs were launched in parallel and all wrote to
`results/alpha_centauri_{summary.json,timeseries.csv}`, so only the e005 run's
machine-readable output survives (copied here as `e005_*`). The other two are
available as logs only, which carry the full per-body verdict tables.
