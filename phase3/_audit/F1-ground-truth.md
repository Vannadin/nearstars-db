# F1 ground truth — Barnard's Star + Teegarden's Star planets

Verification reference for the F1 re-synthesis (2026-06-03). Every Decisions
row in the 7 planet reports must trace to these paper-confirmed values or to a
deterministic recompute from them. Extracted on the main thread from the cached
discovery papers; cross-checked against `db/systems/*.json` `derived` blocks
(fully consistent).

## Barnard's Star (GJ 699) — M4.0 Ve

Host (frozen Phase 2): L = 0.003558 L☉, M = 0.162 M☉, R = 0.187 R☉,
Teff = 3195 K, [Fe/H] = −0.39, age ~8.5–10 Gyr, P_rot = 145 d, log R'HK = −5.82
(very quiet). Source: Schweitzer 2019 / González Hernández 2024 / Toledo-Padrón 2019.

Planets — **Basant et al. 2025** (arXiv 2503.08095, ApJL 982 L1), Table 3.
All four confirmed (b + c/d/e promoted from González Hernández 2024 candidates).
T_eq column is **A = 0, full heat redistribution** (paper footnote a).
S recomputed as L/a² (S⊕). All four orbit **interior** to the HZ (P = 10–42 d).
Stability (SPOCK) favors e < 0.02; non-transiting (Stefanov 2024, i < 87.9°).

| Planet | P (d) | a (AU) | e | ω (°) | M sin i (M⊕) | S (S⊕) | T_eq (K) | DB R (R⊕) |
|---|---|---|---|---|---|---|---|---|
| d | 2.3402 | 0.0188 | 0.04 | −51.8 | 0.263 ± 0.024 | 10.07 | 483 | 0.694 |
| b | 3.1542 | 0.0229 | 0.03 | +3.8  | 0.299 ± 0.026 | 6.78  | 438 | 0.720 |
| c | 4.1244 | 0.0274 | 0.08 | 90.8  | 0.335 ± 0.030 | 4.74  | 400 | 0.743 |
| e | 6.7392 | 0.0381 | 0.04 | −27.5 | 0.193 ± 0.033 | 2.45  | 340 | 0.637 |

Order by distance: d (hottest) → b → c → e (coolest). Barnard e ties Proxima d
as the lowest-mass RV-detected planet (0.19 M⊕). DB radii are mass-radius-relation
derived (non-transiting → no measured radius).

## Teegarden's Star (GJ 1729) — M7.0 V

Host (frozen Phase 2): L = 0.00073 L☉, M = 0.089 M☉, R = 0.107 R☉,
Teff = 2904 K, [Fe/H] = −0.19, age ~7–8 Gyr, P_rot = 96.2 d, log(LX/Lbol) = −4.9
(quiet for late-M). Source: Schweitzer 2019 / Zechmeister 2019 / Dreizler 2024 /
Fuhrmeister 2025.

Planets — **Dreizler et al. 2024** (arXiv 2402.00923, A&A 684 A117), Table 4;
b & c originally Zechmeister 2019. T_eq column is **A = 0.3** (paper assumption).
Non-transiting (TESS + SPECULOOS). The 7.7 d "3:2 chain" candidate is **NOT
confirmed** (favored in CARMENES-only, not in the full dataset) — do not synthesize it.

| Planet | P (d) | a (AU) | e | ω (°) | M sin i (M⊕) | S (S⊕) | T_eq (K) | ESI | DB R (R⊕) |
|---|---|---|---|---|---|---|---|---|---|
| b | 4.90634 | 0.0259 | ~0.03 | — | 1.16 | 1.08 | 277 | 0.90 | 1.050 |
| c | 11.416  | 0.0455 | 0.04 | 301 | 1.05 | 0.35 | 209 | 0.88 | 1.020 |
| d | 26.13   | 0.0791 | 0.07 | 345 | 0.82 | 0.12 | 159 | —    | 0.954 |

b: most Earth-like (S ≈ Earth, ESI 0.90, T_eq 277 K @ A=0.3) — in HZ.
c: ESI 0.88, "closely resembling Proxima b" — in HZ, colder (Mars-like instellation).
d: outside the HZ, cold (~159 K, "Jupiter/Ganymede-like" per Dreizler). M sin i 0.82.
Flares: SPECULOOS FFD → abiogenesis-zone flares (≳10³⁵ erg) ~once / 2.4 yr for b.

## Cached deep-read papers (verification source)

| arxiv_id | paper | drives |
|---|---|---|
| 2503.08095 | Basant 2025 — 4 sub-Earths from MAROON-X+ESPRESSO | Barnard b/c/d/e mass, a, e, T_eq, stability |
| 2410.00569 | González Hernández 2024 — ESPRESSO discovery | Barnard discovery, activity, P_rot |
| 2410.00577 | Stefanov 2024 — TESS no-transit | Barnard i < 87.9°, non-transiting |
| 2402.00923 | Dreizler 2024 — Teegarden revisited | Teegarden b/c/d mass, a, e, S, T_eq, ESI, flares |
| 1906.07196 | Zechmeister 2019 — CARMENES discovery | Teegarden b/c discovery, host params |
| 1812.06712 | Toledo-Padrón 2019 | Barnard P_rot, activity cycle |
