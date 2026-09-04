<!-- 조석식 대조 — 판도라 보드 45 W/m² 재현(0.75 %), Dante 521/900 km, "×Io" 열이 출력 비라는 판정. 병렬석 기록 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (TIDAL-CHECK.md, 19:41 KST). Scripts tidal_check{,2,3}.py were re-run by the work seat the same evening (identical numbers; outputs in tidal-heating-context-notes.md §4 when C30 lands). Translated from the original Korean message on 2026-09-05 for the English-source rule (gate98 section 6, 42.9 % hangul); every number, citation and table is the original's. -->

# The tidal law, checked: Pandora's 45 W/m² reproduced, Dante at 521 vs 900 km, and what "78×" is

Parallel seat, 2026-09-04. Scripts `tidal_check.py`, `tidal_check2.py`, `tidal_check3.py`.
Scratch only, no repo writes. Numbers, no verdicts.

**One line: the board's 45 W/m² reproduces to within 0.75 % under the law printed at `tidal:56`.**

## Constants

`G = 6.67430e-11 m³ kg⁻¹ s⁻²` (CODATA 2018 / NIST recommended), `M⊕ = 5.9722e24 kg` (IAU 2015
Resolution B3 nominal). `M_p = 120 M⊕ = 7.166640e26 kg` (`phase4/alpha_centauri.yaml:354`),
`a = 252 393 km` (`phase3/stability-sim/hypotheticals/alpha_centauri.json:33`),
`R = 5724 km` (`phase4:2132`). Side check: at this a and M_p, `n = 5.454371e-05 rad/s → P_orb =
31.9987 h`, which agrees with the board's 32 h tidal lock (`phase4:2137`).

The law is `tidal:56` verbatim: `Ė = (21/2)·(k₂/Q)·(G M_p² R⁵ n e²)/a⁶`, `n = √(G M_p/a³)`.

## Pandora, over the (e, k₂/Q) combinations

| e | source | k₂/Q | Ė [W] | F [W/m²] | ×Io (flux 2.5) | F/45 |
|---|---|---|---|---|---|---|
| 0.005 | board forced (`:2139`/`:2211`) | 0.0016 (`:2211`, fitted) | 1.8667e16 | **45.337** | 18.14 | **1.0075** |
| 0.005 | same | 0.015 (Io-like) | 1.7500e17 | 425.04 | 170.0 | 9.445 |
| 0.007215479742978246 | sim e_max (`summary.json`) | 0.0016 | 3.8874e16 | 94.416 | 37.77 | 2.098 |
| 0.007215… | same | 0.015 | 3.6444e17 | 885.15 | 354.1 | 19.670 |
| 0.00016422372329501632 | sim e_min | 0.0016 | 2.0137e13 | 0.0489 | 0.020 | 0.0011 |
| 0.000164… | same | 0.015 | 1.8879e14 | 0.4585 | 0.183 | 0.0102 |

**Inverted**: the k₂/Q that hits 45 W/m² exactly is **0.00158809** at e 0.005 (the board's printed
0.0016 rounded to two significant figures), 0.000762581 at e 0.007215, and 1.47212 at e 0.000164.

**Against the ~101 W/m² runaway ceiling at `phase4:2232`**: the adopted combination (0.005 · 0.0016)
at 45.34 is **0.449×**; e_max · 0.0016 at 94.42 is **0.935×**; the Io-like 0.015 at e 0.005, 425.04,
is **4.21×**, which is the case the board writes up as the "369 K steam world" (`:2215`).

## Dante, to check that the law is the board's law

| R | source | Ė [W] | F [W/m²] | vs the board's 11,500 | vs the doc's 2,231 |
|---|---|---|---|---|---|
| **521 km** (board-adopted, `phase4:1472`) | e 0.0186 · k₂/Q 0.0155 (`:1553`) | 7.9284e15 | **2 324.4** | 0.2021 | **1.0418** |
| **900 km** (sim json `:15`) | same | 1.2196e17 | **11 981.7** | **1.0419** | 5.3705 |

**The two ratios are 1.0418 and 1.0419, the same number**: a systematic 4.2 %, which corresponds to
e 0.018223 (or k₂/Q 0.014877) and is therefore explained by the rounding of the printed 0.0186 /
0.0155. So **the law is the same law**.

And here is what that separates: **the "~11,500 W/m²" at board `:1554` is the R = 900 km number,
while the radius the board adopts is 521 km (`:1472`)**. From the same inputs the flux at 521 km is
2,324 W/m² (the doc prints 2,231). The §6.5 table (`tidal:449-454`) already holds that comparison:
900 km (draft) 1,200× / 11,500 W/m² → 714 km 377× / 5,742 → **521 km (adopted) 78× / 2,231** →
450 km 38× / 1,438. The "~820× → ~1200× correction" recorded at board `:1486` moved the row toward
the 900 km draft, not toward the adopted value.

## ⚠ "78× Io" is Dante, not Pandora

The number the brief asked about as "Pandora ~78× Io?" is **the label on the doc's Dante-at-521 km
row, `tidal:453`**. The column's unit is settled by the doc's own two rows: `(900/521)³ = 5.1548`
against `11500/2231 = 5.1546`, and `(900/521)⁵ = 15.3824` against `1200/78 = 15.3846`, so **the "×Io"
column is a ratio of outputs (Ė) and the W/m² column is a flux**. Inverting Io's output from the two
rows gives 1.0163e14 and 1.0165e14 W (≈100 TW, Io's measured value), which fixes the convention.

Converting Pandora under the same convention, the adopted combination (e 0.005 · k₂/Q 0.0016) gives
**Ė = 1.8667e16 W = 186.7× Io by output**, and 18.1× Io by flux.

## Pandora's output ratios in full (Io_Ė = 1.0e14 W convention)

| e | k₂/Q | Ė [W] | ×Io (output) | F [W/m²] | ×Io (flux 2.5) |
|---|---|---|---|---|---|
| 0.005 | 0.0016 | 1.8667e16 | 186.7 | 45.337 | 18.13 |
| 0.005 | 0.015 | 1.7500e17 | 1750.0 | 425.038 | 170.02 |
| 0.007215 | 0.0016 | 3.8874e16 | 388.7 | 94.416 | 37.77 |
| 0.007215 | 0.015 | 3.6444e17 | 3644.4 | 885.152 | 354.06 |
| 0.000164 | 0.0016 | 2.0137e13 | 0.2 | 0.049 | 0.02 |
| 0.000164 | 0.015 | 1.8879e14 | 1.9 | 0.459 | 0.18 |

⚠ Worktree state at the time of writing: the work seat's uncommitted C28 changes were in
`engine/chain.yaml`, `dynamo_rocky.py`, `interior-core.md` and `test_dynamo_rocky.py`, and everything
this report cites (`phase4/*`, `docs/reference/*`, `hypotheticals/*`, `results/*`) is outside that
diff.

⚠ Established later the same day, after this report: the sim's e_max 0.007215 comes from
`results/_final32b/alpha_centauri_summary.json`, that is from the **Dante 900 km · Hades e 0.05 /
i 11° configuration**, and main's uncommitted 2026-08-21 snapshot writes the same quantity as
**e 0.00366**. See the end of `MAIN-7FILES-2026-08-21.md`.
