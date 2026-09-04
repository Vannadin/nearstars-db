<!-- tidal_locking 레시피(보류)의 입력 인벤토리 — 천체별 a·e·주기·모체 질량·나이가 어느 파일 어느 줄에 있는가. 병렬석 기록, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (TIDAL-LOCKING-INVENTORY.md, 18:34 KST), body unedited. The tidal_locking recipe itself is on hold (owner, 2026-09-04 evening); its draft sits in the work seat's scratch and was never written to the worktree. -->

# A. tidal_locking input inventory — where each value lives
Parallel seat, 2026-09-04. Read-only. Paths relative to the engine worktree
`/Users/vana/Desktop/NearStars-wt/engine-prototype` at HEAD 839b2c7c (`git status --porcelain`
empty). ⚠ `phase3/stability-sim/hypotheticals/alpha_centauri.json` is one of the 7 files
uncommitted in the **main** checkout — the lines below are the worktree's **committed**
version; I did not open main's copy.

Inputs the recipe declares (`tidal-locking-timescale-methodology.md:58`,
`τ_lock ≈ (ω₀ − n)·(Q/k₂)·(I a⁶)/(3 G M_p² R⁵)`): `a`, `e`, `M_p` (perturber mass), `t_sys`,
plus the locking body's `m`, `R`. Chain edges: `orbit_elements → tidal_locking via [a,e]`
(`chain.yaml:612`), `system_age via t_sys` (`:614`), `mass_radius_relation` (`:613`),
`k2q_class_table via k2_over_q` (`:556`), `omega0_class_table via p_init` (`:557`).

| body | a | e | orbital period | parent mass | age |
|---|---|---|---|---|---|
| **earth** | **absent** | **absent** | **absent** | **absent** (no Sun mass anywhere in `engine/bodies/`) | 4.54 Gyr — `engine/bodies/earth.yaml:11` |
| **pandora** | 252 393 km — `phase3/stability-sim/hypotheticals/alpha_centauri.json:33` | 0.0 — same file `:34` | 32 h — `phase4/alpha_centauri.yaml:2137` (row says "Tidally locked", so rotation = orbit) | 120 M⊕ (Polyphemus) — `phase4/alpha_centauri.yaml:354` | 5.3 Gyr — `engine/bodies/pandora.yaml:8`; also `phase4/alpha_centauri.yaml:2142` |
| **alpha_centauri_a_b** (= **Polyphemus**, one body) | 1.6 AU — `phase4/alpha_centauri.yaml:50` | 0.1 — `phase4/alpha_centauri.yaml:70` | **absent** (no printed period row; rotation 10.35 h at `:329` is spin, not orbit) | 1.1055 M☉ (α Cen A) — `phase4/alpha_centauri.yaml:1393`; same value `db/systems/alpha_centauri_a.json:474` | 5.3 Gyr — `engine/bodies/alpha_centauri_a_b.yaml:10`; `phase4/alpha_centauri.yaml:360` |
| **luhman_16_a** | 3.557 AU (A–B relative orbit) — `db/systems/luhman_16_a.json:259` | 0.343 ± 0.005 — same file `:257-258` | 27.54 ± 0.4 yr — same file `:253-254` | companion 0.0273 M☉ (Luhman 16 B) — `db/systems/luhman_16_a.json:236` | 0.5 Gyr — `engine/bodies/luhman_16_a.yaml:11`; DB says 1.5 — `db/systems/luhman_16_a.json:140` |
| **luhman_16_b** | 3.557 AU (same relative orbit) — `db/systems/luhman_16_a.json:259` | 0.343 — same `:257` | 27.54 yr — same `:253` | companion 0.032 M☉ (Luhman 16 A) — `db/systems/luhman_16_a.json:225` | 0.5 Gyr — `engine/bodies/luhman_16_b.yaml:11`; DB 1.5 — `db/systems/luhman_16_b.json:140` |
| **Dante** (A b I) | 110 000 km — `…/alpha_centauri.json:9` | 0.01 — `:10` | 9.2 h — `phase4/alpha_centauri.yaml:1478` ("tidally locked (rotation = orbit)") | 120 M⊕ — `phase4/alpha_centauri.yaml:354` | 5.3 Gyr — `phase4/alpha_centauri.yaml:1483` |
| **Hades** (A b II) | 148 000 km — `…/alpha_centauri.json:21` | 0.05 — `:22` | 14.4 h — `phase4/alpha_centauri.yaml:1836` ("tidally locked (rotation = orbit)") | 120 M⊕ — `:354` | 5.3 Gyr — `:1841` |
| **Chaos** (A b V) | 1 500 000 km — `…/alpha_centauri.json:57` | 0.02 — `:58` | **absent** — the 9.5 h at `phase4/alpha_centauri.yaml:3008` is annotated "Free rotation (not synchronous)", so it is not the orbit | 120 M⊕ — `:354` | 5.3 Gyr — `:3011` |
| *Cassandra* (A b IV, not asked — same block) | 600 000 km — `…/alpha_centauri.json:45` | 0.05 — `:46` | **absent** — 39 h at `:2592` is "Free rotation (not synchronous, not resonance-locked)" | 120 M⊕ — `:354` | 5.3 Gyr — `:2596` |

Locking-body `m` / `R` (the recipe's other two), for completeness:

| body | mass | radius |
|---|---|---|
| earth | 1.0 M⊕ — `engine/bodies/earth.yaml:9` | 1.0 R⊕ — `:10` |
| pandora | 0.6447 M⊕ — `engine/bodies/pandora.yaml:7` (= board 3.85e24 kg, `phase4/alpha_centauri.yaml:2133`) | 5724 km — `phase4/alpha_centauri.yaml:2132` |
| alpha_centauri_a_b | 120 M⊕ — `engine/bodies/alpha_centauri_a_b.yaml:8`; board `:354` | 1.0 R_J — board `:199` |
| luhman_16_a | 10654 M⊕ (0.0320 M☉) — `engine/bodies/luhman_16_a.yaml:7` | — |
| luhman_16_b | 9089 M⊕ (0.0273 M☉) — `engine/bodies/luhman_16_b.yaml:7` | — |
| Dante | 1.552e21 kg — `phase4/alpha_centauri.yaml:1469` | 521 km — `:1472` |
| Hades | 5.0e21 kg — `:1831` | 750 km — `:1832` |
| Chaos | 5.4e20 kg — `:3000` | 400 km — `:3001` |
| Cassandra | 9.0e23 kg — `:2586` | 3400 km — `:2587` |

## Two printed-fact juxtapositions (no judgment)

1. **The sim input and the board disagree on three moons' mass/radius.** Both files are in
   the tree; I am placing the printed numbers side by side, not saying which is right.

| body | stability-sim JSON | phase4 board |
|---|---|---|
| Dante | `mass_kg 8e+21` (`:14`), `radius_km 900` (`:15`) | `1.552e21 kg` (`:1469`), `521 km` (`:1472`) |
| Hades | `5e+21` (`:26`), `750` (`:27`) | `5.0e21 kg` (`:1831`), `750 km` (`:1832`) — agree |
| Pandora | `4.3e+24` (`:38`), `5724` (`:39`) | `3.85e24 kg` (`:2133`), `5724 km` (`:2132`) |
| Cassandra | `9e+23` (`:50`), `3400` (`:51`) | agree |
| Chaos | `5.4e+20` (`:62`), `400` (`:63`) | agree |

   The sim file's own `_comment` (`:2`) prints the Dante radius it used as "a solid 900-km
   body" and calls the masses/radii "INVENTED except Pandora (0.72 M_earth, 11,447 km)" —
   a third pair, different from both columns above. `engine/bodies/pandora.yaml:7` carries
   0.6447 M⊕, matching the board.

2. **Luhman 16 age differs between the engine body file and the DB by 1.0 Gyr**, and the
   engine file says so itself: `engine/bodies/luhman_16_a.yaml:11` —
   `age_gyr: 0.5   # 보드 phase4/luhman_16.yaml (Gagné 2023 이동군); DB 는 1.5 ± 1.5 (범위
   중점) — O1, 이 가지는 나이를 읽지 않는다`.

## `:270` — what the ω₀ "hours–days" bound cites

**Nothing. The doc states outright that it is not a citation.**

- `tidal-locking-timescale-methodology.md:270-271`: "**The initial spin `ω₀` is unknown.**
  It enters linearly too, but it is bounded: a primordial spin period of hours–days spans
  only ~1–2 dex, and it only sets *how much* excess angular momentum must be removed, not
  the scaling."
- `:431-432` (the doc's own "Topics with no single canonical paper" section): "The *initial
  spin* `ω₀` has no canonical value (it is a primordial unknown); **it is bounded by
  argument, not cited.**"
- `chain.yaml:332` already records this as the node's note: `omega0_class_table` —
  `"원시 미지값. 인용이 아니라 논증으로 경계지어진다" — tidal-locking:431`.

So there is no bibcode to check for `:270`, and therefore no HELD/ABSENT verdict to give.
The neighbouring `Q/k₂` bands are the same kind (`:428-430`: "a synthesis of the Goldreich
& Soter 1966 / Murray & Dermott literature … not a single citable table").
