<!-- C30 — 조석열을 내부구조 열 예산에 배선: 사전등록 → 스크래치 dry-run 기록 → 판도라 결과 → 착지 -->
# Tidal heating wired into the interior heat budget (C30) — context notes

*Doc line numbers cited in this section are those of 839b2c7c (before b29b556e's contract blocks); add 18 (tidal en) / 15 (tidal ko) / 1 (heat, below :44) for the current files.*

2026-09-04, evening. Owner-approved brief (directing seat). Prepared in the work seat's scratch during a computation stop
(~19:45–20:05), then released by the owner ("조석 배선 다시 가보자") and landed the same night. §1–§2 were written while the
item was frozen; §3's Pandora capture ran on the scratch copy after the release, before the worktree write.

## §1 Pre-registration (written 2026-09-04 ~19:30 KST, before any worktree run; ⚠ the scratch dry-runs listed in §3 ran
## after this list was fixed in the brief but before this file was written — evidence level stated, not claimed)

Ⓟ Pandora reproduces the board's 45 W/m² within 5 % (tidal tidal-heating-methodology.md@«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶» with a 252 393 km · e 0.005 · k₂/Q 0.0016 · M_p 120 M⊕ ·
R 5724 km), its §6.2 mode on the total flux is **heat pipe**, its §6.1 regime "vigorous silicate volcanism, possible magma
ocean", and the total-heat floor is refused by name (heat-pipe guard) · Ⓠ reproduction misses by > 5 % → re-check the input
sources, do not land · Ⓡ Earth, A b, Luhman 16 A/B carry no tidal inputs → `tidal_heating` cannot-say (no orbit), and every
**pre-existing** key of every other result identical (as written on 2026-09-04 this clause said "every other result
bit-identical", which was too loose and the audit said so: Earth's `internal_heat_nontidal` gains five keys by design,
`l_int_total` · `t_int_total` · `mantle_temperature_floor_total_min`/`_max`/`_verdict`) · Io self-check: Ė from the doc's printed inputs (:479–480) lands **inside** the printed band 0.6–1.6e14 W
(:100) and P_orb 1.769 d; outside → the law or a constant is wrong, do not land.

## §2 Design (as drafted)

- `engine/tidal_heating.py`: `@recipe("tidal_heating")` → power [W], surface_flux [W/m²], io_power_ratio (÷ the printed
  ~1e14 W; the §6.5 Dante rows invert to 1.016e14, 1.6 % off — convention), heat_transport_regime (§6.1 strings verbatim;
  10⁻³–10⁻² has no row → "unclassified (between table rows)"), orbital_period. `@recipe("heat_transport_mode")` → mode
  (§6.2: plate tectonics / stagnant lid / heat pipe, on the TOTAL surface flux = tidal + l_int/4πR²; the gap 0.14–2.5 W/m² is
  "unclassified"), total_surface_flux; `resurfacing_rate` not emitted (no formula printed). Not emitted: radius_ceiling,
  plains_temperature (the Dante lid axis) — the two chain edges carrying them (:626, :650) become `status: gap`, dated.
  `tidal_transport.derive_potential_temperature` is not consulted (validation-failed label; Pandora is not a §6 lid case,
  tidal-heating-methodology.md@«> **Scope — lid-bearing bodies only.**»). Two Io flux anchors carry their different sources in comments: ~2 W/m² Veeder+ 2012 (ABSENT), 2.5 W/m²
  Kankanamge & Moore 2019 (HELD).
- `radiogenic.py` (`internal_heat_nontidal`): existing outputs untouched; new `l_int_total`, `t_int_total`,
  `mantle_temperature_floor_total_min/max/_verdict` — emitted only when `tidal_heating` supplied `power`; the floor is
  re-inverted against the total (tidal counted in the mantle, declared) only in a boundary-layer mode; under a heat pipe the
  verdict is "cannot-say (heat-pipe regime: the boundary-layer inversion does not apply; radiogenic.py:183)". New Need
  `tidal_power` [W] (chain :653 via power).
- chain.yaml: `tidal_heating` outputs rewritten (old kept in note), `heat_transport_mode` outputs [mode, total_surface_flux]
  (old kept), :631 units note, :632 via mantle_radiogenic_power → radiogenic_power (dated), :653 via power (built), :686 note
  (from-node now has a recipe; dynamo_rocky still reads nothing → gap stands). Contract blocks for both recipes added to the
  tidal doc (en + ko); the heat doc's Returns/Needs extended (en + ko). `registry.load_all` gains `tidal_heating`;
  `check.sh` gains `test_tidal_heating.py`. `bodies/pandora.yaml` gains the four tidal inputs with sources and an
  `expected.surface_flux: 45 W/m²` comparison row.

## §3 Scratch dry-run record (before the computation stop; not a worktree run)

`test_tidal_heating.py`: PASS — Io Ė 9.343e13 W (band), P 1.769 d; Pandora F 45.34 W/m² (+0.75 % vs 45), 187× Io, regime
vigorous, mode heat pipe; ×Io column scales as R⁵ (1200/78), W/m² as R³ (11500/2231); Dante 521 km 79.3× on 1e14 (doc 78× on
1.016e14). `test_radiogenic.py` PASS unchanged; `check_contracts` 13/13; `chain.py check` PASS; `check_via --gate` PASS after
gapping :626/:650; `backflow` ok; Earth chain run: internal_heat_nontidal keeps every pre-existing key and adds the five `*_total` ones,
tidal_heating cannot-say (no orbit),
heat_transport_mode → plate tectonics at 0.0418 W/m² (radiogenic only).

**Pandora, full chain under C30 (scratch copy, after the release; run.py, hook-free):**

| node | value |
|---|---|
| `tidal_heating` | power **1.866e16 W** · surface_flux **45.33 W/m²** · io_power_ratio **186.6** · regime **vigorous silicate volcanism, possible magma ocean** · orbital_period 32.0 h |
| `heat_transport_mode` | **heat pipe** · total_surface_flux 45.36 W/m² (tidal 45.33 + radiogenic 0.0334) |
| `internal_heat_nontidal` | radiogenic-only values unchanged (l_int 1.374e13 W, t_int 27.7 K, floor 1017–1468 K) · **l_int_total 1.868e16 W · t_int_total 168.2 K** · mantle_temperature_floor_total_min/max **None** · verdict **cannot-say (heat-pipe regime: the boundary-layer inversion does not apply; radiogenic.py:183)** |
| `dynamo_rocky` | unchanged from C29(c): alive by declaration, B_eq 41.37 µT |
| expected | surface_flux engine 45.33 vs board 45 (0.7 %, tol 1 %) 일치; b_eq 41.37 vs 75 (44.8 %, comparison) |

**Outcome: Ⓟ** — reproduction inside 0.75 %, regime and mode as pre-registered, the total floor refused by name; every
pre-existing key of Earth's results identical (the five new `*_total` keys are the point of the change, not a
regression); A b and Luhman 16 A/B have no tidal inputs → `tidal_heating` cannot-say (no orbit) — Ⓡ's clause holds for
them too. The Io band check passed (9.343e13 W inside 0.6–1.6e14).

## §4 The parallel seat's check tables (scratch scripts re-run by the work seat, 2026-09-04)

tidal_check.py — Pandora: e 0.005 · k₂/Q 0.0016 → Ė 1.8667e16 W, F 45.337 W/m² (1.0075× board 45); e 0.007215 (sim e_max) →
94.42 W/m²; e 0.000164 (sim e_min) → 0.049 W/m²; k₂/Q 0.015 (Io-like) at e 0.005 → 425 W/m². Inversion: 45 W/m² needs k₂/Q
0.001588 at e 0.005. Dante: R 521 km → Ė 7.928e15 W, F 2 324 W/m² (0.2021× the board's 11 500; doc 2 231); R 900 km → 11 982
W/m² (1.0419× 11 500). tidal_check3.py — (900/521)³ = 5.1548 vs 11500/2231 = 5.1546; (900/521)⁵ = 15.38 vs 1200/78 = 15.38 →
the ×Io column is an OUTPUT ratio; both Dante rows imply Io ≈ 1.016e14 W. io_anchor.py — see `io-anchor-notes.md`.

## §5 Note 7 — Dante's stale board rows (recorded, NOT repaired; board changes go through C31's emit path)

Source: `dante-board-900km-notes.md` (parallel seat, 19:35). (a) The tidal block `phase4/alpha_centauri.yaml:1524–1607`
never mentions a radius; `DANTE_HEAT_TRANSPORT_EVIDENCE.md@«combo. Hades e_rms 0.033–0.046 and Dante e_rms 0.017–0.022 both bracket the board's existing 0.0385 / 0.0186, so the tidal-heating rows move because of SIZE, not eccentricity.»` says "the tidal-heating rows move because of SIZE, not
eccentricity". (b) Rows resting on the 900 km draft: `:1553` "~1200× Io" and `:1554` "~11,500 W/m²" (521 km: 78× · 2 231
W/m², tidal-heating-methodology.md@«adopted by [arXiv:2305.03410](https://arxiv.org/abs/2305.03410)).»), plains 360 K (doc 223 K), area-weighted 673 K (452 K), melt area 5.7 %, crust 2.1 / 2.4 m, the albedo and
glow rationales at 360 K, and `:1480` `geopotential_j2 reference_radius_km: 900` against `:1477` reference_radius 521.
(c) The doc labels those values "drafted" (`tidal:445–447`); the board carries them unlabelled in adopted slots. The board
of record is the **main checkout's** copy, which holds uncommitted changes — not touched (owner decision).

## Corrections, 2026-09-05 (the C30 audit's five findings, and three more found while C31 landed)

The audit approved C30's numbers and rejected five citations or sentences around them. None of the five moves a value.

- **(a) A self-citation that pointed at the wrong line of its own file.** `HEAT_PIPE_FLOOR` named
  `radiogenic.py:183`, which is the band note's ζ prose; the decision it describes is at `:265-267` and its explanation
  at `:167-171`. The string is *shipped as a result value* and copied into two rows of this file, so the wrong line
  travelled. Now `radiogenic.py _total_heat:265-267`: naming the function as well as the line means the next block
  inserted above it degrades the citation instead of falsifying it. `0ace3863` refreshed 53 refs and missed this one
  because it lives inside a string constant, not in a comment.
- **(b) `tidal_heating.py@«inputs, REFS) if k2_over_q is None»` cited `tidal-heating-methodology.md@«> and comfortably below the 384 kW/m² bare-melt ceiling.»` for `F ∝ R³`.** That line is now the 384 kW/m² bare-melt ceiling; the
  scaling sentence is `:458`. Two more of the same kind in the same file, found by the directing seat: lines 4 and 59
  cited `:58` for `n = √(GM_p/a³)`, and `:58` is now inside the `heat_transport_mode` contract block that b29b556e
  itself added, while line 113 of the same file already cited that sentence correctly as `:76`. One file, one sentence,
  two numbers, one of them broken by yesterday's own commit. All three now `:76` / `:458`.
- **(c) The `transport_mode` docstring said the table's gap runs from 0.09 W/m².** The branch below it reads
  `0.09 * 1.5 = 0.135`, and both the test docstring and the pre-registration above say 0.14. Only the docstring was
  behind; it now says 0.14 and names the +50 % reading.
- **(d) "every other result bit-identical" was too loose**, here and in 53856339's commit body and this file's ledger
  row. Earth's `internal_heat_nontidal` gains five keys by design. Corrected in place above to "every pre-existing key
  identical". The commit body stands as written; this is the record.
- **(e) The contract printed a Need the engine cannot read.** `tidal_heating`'s Needs said `semi_major_axis_m` [m]
  while `_from_state` reads `semi_major_axis_km`, so a body written from the contract earns a named refusal. Fixed on
  the code side, because the contract checker compares the doc against `Result.inputs`: `solve()` now takes
  `semi_major_axis_km` and converts at the call, so the declared name, the recorded input and the state key are one
  name. The doc (and its ko mirror) print `semi_major_axis_km` [km]. The same class one node over is *not* a bug but is
  now written down: `internal_heat_nontidal`'s Need `tidal_power` arrives under the state key `power`, a generic name
  with exactly one emitter today, and a second emitter of `power` would be summed in silently. Named in the contract
  block as a **State-key note** and beside the line that reads it.

Three more, from the audit of C31's tool (`engine/tools/refresh_board_rows.py`):

- **The tool trusted the satellites table without checking the rows it was about to overwrite.** On the engine
  worktree's board, where bulk was ahead (radius 521) and the table behind (900), it would have read 900, reported
  1219.58× Io with confidence, and written the 2026-08-21 resize back out. Same tool, same command, opposite direction,
  and only the board differs. It now refuses by name when the table and the bulk row disagree about radius or mass,
  printing both values and both line numbers.
- **The a-sensitivity exponent was 6 where it should be 7.5.** `n = √(GM_p/a³)` is computed from the same `a`, so
  `Ė ∝ a⁻⁷·⁵` — the doc's §3 is titled that. The 110,044.5 vs 110,000 km choice is 0.30 % in Ė, not 0.24 %.
  (`fc8532be`'s body says "through a⁻⁶"; this is the correction.)
- **A footnote that was simply wrong.** It said the `e_rms` justification rested on an uncommitted file. The cited
  sentence has been committed since `8b9f0408`; only the file's later edits were uncommitted, and those landed in
  `24587c5f`. Removed from the docstring and the report, with the citation left at `:154-155`.

Also from that audit: `sha()` now reports `-dirty`, so a board note cannot stamp a clean commit that lacks the code
that wrote it; a re-run on an already-refreshed board is a no-op rather than a second stamp; and the explorer's
`moon_energy_budget` label was respaced to match.
