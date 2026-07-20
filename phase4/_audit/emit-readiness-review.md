<!-- Phase 4 산출물의 cfg-emit 적합성 다각도·적대적 리뷰 (5-에이전트 + 메인 검증, 2026-07-10) -->
# Phase 4 — Emit-Readiness Review (adversarial, multi-lens)

Date: 2026-07-10. Method: 5 parallel review agents (schema conformance / numeric-emit
parse / visual-emit parse / gate-integrity red-team / coverage-consistency red-team),
key findings then re-verified on the main thread by direct grep/read. Scope: all six
`phase4/*.yaml` boards + `phase4/figure/*` against `phase4/SPEC.md`, the cfg-writer
skills (`principia-cfg`, `kopernicus-cfg`, `firefly-cfg`, `researchbodies-cfg`), and the
live emitter scripts.

The owner's question: **"are the Phase-4 outputs in a format suitable for later cfg emit?"**

## Bottom line

**No — not as written.** Only `barnards_star.yaml` and the numeric orbit/eccentricity
rows of `alpha_centauri.yaml` are directly emit-parseable. The other ~90% of rows fail on
two *structural* (not content) axes, plus the whole gate has no enforcement. The intent
and even the exact numbers/hexes almost always exist — but as prose, not typed fields.

Three root causes, in priority order:

1. **The gate is unenforced.** SPEC §4/§6 require a `check.sh` validator that fails the
   build on ungated/undocumented emits. It was never built (`scripts/check.sh` runs 6
   gates; none parse a single `gate:` block). Every defect below reaches emit silently.
2. **Boards drifted off their own schema.** SPEC §3 says one row = one emit field
   (`axis: group.name`, typed `value`, `evidence`/`divergence_note`). Reality: most rows
   are `axis: group` only, with a multi-quantity prose `value:` and renamed gate keys
   (`note`/`paper`/`rationale`). A writer cannot field-extract from prose.
3. **The emitters and the boards were built to different contracts.** The RB emitter,
   Firefly emitter, and Kopernicus star/ring color path all read inputs the boards do not
   contain — so several "gated" decisions are dead on arrival even if perfectly formatted.

## Coverage (roster × board)

| System | Board | State |
|---|---|---|
| α Centauri (+ Proxima) | `alpha_centauri.yaml` / `proxima_cen.yaml` | ✅ full, internally clean |
| 40 Eridani | `40_eridani.yaml` | ✅ full |
| Fomalhaut | `fomalhaut.yaml` | ✅ 8 axes |
| Barnard | `barnards_star.yaml` | ⚠️ skeletal (2 rows) |
| Tau Ceti | `tau_cet.yaml` | ⚠️ skeletal (5 rows, star-only) |
| **TRAPPIST-1** | — | ❌ **absent** (DB exists) |
| **Luhman 16** | — | ❌ **absent** (DB exists) |

`grep status:` returns **zero `open`/`art-directed` rows** — the boards that exist read as
"done." The real gap is missing boards + skeletal blanket-passthrough, not tracked TODOs.

---

## BLOCKERS

**BK1 — No Phase-4 validator exists (enforcement = zero).**
`scripts/check.sh` gates: schema (db/systems + curated), plasma-temp, ko-mirrors,
dead-links, conventions, path-migration. None parse `gate:`/`verdict`/`divergence_note`.
SPEC §6 makes the validator a hard activation precondition. *Consequence:* nothing catches
BK2–BK7 or MJ1–MJ8; all depart silently. *Fix:* `scripts/check_phase4_gate.py` (per row:
if a writer emits the axis → require `status ∈ {gated,emitted}`, `verdict ∈ {pass-in-window,
documented-divergence}`, and `documented-divergence ⟹ divergence_note` non-null), wired as
check.sh gate 7. Also extend `check_dead_links.py:48` to glob `phase4/**/*.yaml`.

**BK2 — ResearchBodies emit is a no-op today (input-contract mismatch).**
`emit_researchbodies_cfg.py:4,70` reads a top-level `discoverability:` list. The boards
store discoverability **only** as per-row `decisions[].discoverability_cfg:` sub-objects
(αCen 6, 40 Eri 6, proxima 5, tau 1, fomalhaut 1, barnard 0) — **zero** top-level lists
(verified). Running the emitter prints "Nothing to emit"; **all 19 authored discoverability
decisions are dead on arrival.** Compounding: `ONDISCOVERY` message text exists nowhere
(no `message:` field), and `ref:` is editorial prose (e.g. `40_eridani.yaml:21`
`"naked-eye (V=4.43, Eridanus)"`), not the bibcode the skill's convention #5 requires for
candidate/disputed bodies. *Fix:* reconcile one side — teach the emitter to walk
`decisions[].discoverability_cfg`, or emit a flat `discoverability:` list; add `message` +
bibcode `ref`.

**BK3 — Planet/moon/figure layer has no consumer at all.**
`principia-cfg` MVP is **stars-only** (planets blocked; `j2`/`reference_radius` explicitly
omitted). `kopernicus-cfg` automated scope is **circumstellar-disk Rings only** (Properties/
Orbit/Atmosphere are "hand-write, out of scope"). Firefly globs `docs/phase3/*.md`, so
fiction bodies (no Phase-3 md) never emit. So Barnard/Tau Ceti/Polyphemus/40 Eri planet
orbits, masses, figures, and all fiction-body atmospheres (Pandora, Cassandra, Dante, Erid,
Chaos) currently have **no automated emit path**. SPEC §4 assumes these writers consume the
layer; they don't yet. *Fix:* this is the real "build Phase 4" work — extend the writers,
or accept a hand-write path and say so.

**BK4 — Fiction bodies have empty/absent DB records; `op: set` has nothing to bind to.**
`alpha_centauri.yaml:29-52` Polyphemus `orbit.semi_major_axis_au op:set 1.6` — but
`db/systems/alpha_centauri_a.json` has `kopernicus:{}`, `principia:[]`, `moons:None` for
that planet; no GM → Principia pre-flight aborts, and the unit lives only in the axis *name*
(no AU→m rule). The five moons (Dante/Hades/Pandora/Cassandra/Chaos) have no DB entry and
their mass/radius/orbit live inside prose `value:` blobs (`:478-486` etc.), violating SPEC
§3's "class-D row carries the full body definition as structured fields." *Fix:* give
fiction bodies a structured body-def block the writer can bind to.

**BK5 — Barnard orbit block cannot emit (null base for the `scale` ops).**
`barnards_star.yaml:22-27` `orbit.eccentricity op:scale 0.8` scales the DB default, but
`db/systems/barnards_star.json` has `kopernicus.eccentricity=null` and the whole
`kopernicus` block null; the real values sit at `raw.*` with no `raw→kopernicus` promotion
rule, and Kopernicus blocks generation on null `semi_major_axis_m`. The scale *arithmetic*
is exact (`per_planet_result*` checksums verified), but there is no base to apply it to.
LAN/argP/meanAnomaly are absent entirely. *Fix:* promotion rule or explicit emit values.

**BK6 — figure ledger is prose AND computed from a rejected mass.**
`phase4/figure/values.md` is a human Markdown ledger (per-body J₂/C̄₂₂/reference_radius in
prose), with "emit wiring deferred." Worse, `values.md:39` computes Pandora's hydrostatic
J₂ from **0.72 M⊕** — the mass the board (`alpha_centauri.yaml:672,1066`) explicitly
**rejects** as internally inconsistent in favour of **0.645 M⊕ (3.85e24 kg)**. So the
J₂/C̄₂₂ that would feed Principia gravity_model were derived on the wrong mass. *Fix:*
recompute Pandora figure on 0.645 M⊕; give the ledger a machine-readable emit form.

**BK7 — Fomalhaut belt geometry is emit-impossible in Kopernicus (self-admitted).**
`fomalhaut.yaml:104`: the Kopernicus Ring node is a flat circular annulus, so the cold
belt's e=0.11 "Eye of Sauron" offset, the three per-belt inclinations (47.8°/67.5°/65.6°)
and PAs, and the vertical thickness cannot be represented. *Consequence:* faithful disk
geometry either emits wrong (flat/coplanar/circular) or is dropped. *Fix:* out-of-engine
(Principia/custom/volumetric) or explicitly accept the approximation — the board already
documents it; make it a machine flag, not prose.

---

## MAJOR

**MJ1 — `axis: group` only (not `group.name`) — the dominant defect.**
SPEC §3: "`axis` is `group.name` … never a free-form field." Reality: ~40/48 rows in
40_eridani, 7/8 in fomalhaut, 4/5 in tau_cet, ~42 in proxima, ~45 in alpha are keyed by
group alone (`bulk`, `appearance`, `environment`…). A single `bulk` row (e.g.
`40_eridani.yaml:204`) bundles mass+radius+density+J₂+obliquity+spin into one prose blob,
but the emit unit is `bulk.mass`, `bulk.radius`, `bulk.geopotential_j2` *separately*. One
prose row cannot feed the six distinct cfg fields it describes.

**MJ2 — `value:` is a multi-sentence prose blob (systemic).**
tau_cet / fomalhaut / 40_eridani / proxima non-orbit rows, and αCen non-orbit rows. Load-
bearing numbers exist only in prose: `tau_cet.yaml:24-31` (M/R/Teff/L/age/P_rot/spin-i);
`fomalhaut.yaml:92-104` (3 belts × radii/i/PA/e/T/mass/colors); `alpha_centauri.yaml:87-102`
(Polyphemus radius, where the DB says 11.8 R⊕ but the board wants 11.2 R_Jup-equiv — the
prose override is unreadable, so the writer would emit the wrong radius). Sometimes a value
*is* near-structured (`alpha_centauri.yaml:515` `albedo: 0.30`) — the inconsistency itself
means no single extraction path is reliable.

**MJ3 — Gate blocks off-schema roster-wide (`evidence`/`divergence_note` mostly absent).**
Only `barnards_star.yaml` and the αCen numeric rows use `evidence`. 40_eridani/fomalhaut/
tau_cet have **zero** `evidence`/`divergence_note`; proxima invents `rationale`/
`aurora_divergence`/`palette_note`/`collapse_note`. A schema-keyed validator finds almost
no conforming rows and cannot tell "documented in prose" from "undocumented."

**MJ4 — `documented-divergence` verdicts with no `divergence_note` (guard would fail).**
`divergence_note:` present only in alpha (9) and proxima (2); **absent** in 40_eridani,
tau_cet, fomalhaut, barnards. Verified specific rows: `proxima_cen.yaml:117` (b
atmosphere) uses `rationale:`; `alpha_centauri.yaml:408` (A stellar_wind) and `:451` (B)
use `evidence:`; `proxima_cen.yaml:175` (b aurora) uses `aurora_divergence:`. Each is a real
departure whose SPEC-required note field is null. SPEC §4 makes a null note a build failure.

**MJ5 — Verdict inflation: departures gated as `pass-in-window` (the aurora bug, recurring).**
The coverage audit already caught one (aurora, since fixed). Still live:
- `40_eridani.yaml:271-288` (Erid appearance): film azure `#3a6db0` emitted over physical
  `#95bcc9`, text literally says "documented divergence(색)", verdict `pass-in-window`, no
  note. Direct repeat of the aurora precedent.
- `40_eridani.yaml:196-201` (Erid orbit, 5.1 h rotation vs tidal-lock methodology) and
  `:300-303` (magnetism) — prose "⚠️ documented divergence", verdict `pass-in-window`.
- `fomalhaut.yaml:34-41` (visual oblateness "가시 임계 ~5% 아래지만 오너가 채택") — owner-
  adopted appearance below the visibility threshold gated as a plain pass; same "임계 아래
  지만 채택" tell as the aurora case.

**MJ6 — Fiction body gated on inapplicable criteria (class-D gate skipped).**
`40_eridani.yaml:171-372` (Erid, fiction on the *refuted* 40 Eri A b candidate): all 11
axes `verdict: pass-in-window` on `criterion:[culture,classification]`. But a fiction body
has **no Phase-3 window** ("pass-in-window" is category-inapplicable), and SPEC §2 requires
class-D to gate on Hill+HZ stability + composition plausibility — never applied. Its orbit
(0.224 AU, part of the b–d 2:1 resonance) rode "PHM canon (Weir)" instead of the REBOUND
stability gate its siblings c/d used (`:405,540`).

**MJ7 — No machine-readable color/variant selector.**
Every color cell offers multiple hexes with the choice stated only in Korean prose:
tau_cet physical `#ffeddf` vs viewer tint `#ffe9c8` (`:39,47`); fomalhaut belts faithful
`#fff4e5` vs vivid `#ffe0b0`/`#ffe2b1` vs measured `#d6d8da` with "faithful 기본" in prose
(`:99-100`); proxima `cfg_colors_intrinsic` vs `cfg_colors_displayed` (`:144,169`); 40 Eri
film vs physical (`:276,281`). No `ring_color_variant`/`emit_value` field; the measured cold
belt has no "do-not-vivify" flag. And star colors are recomputed from Teff, ring colors from
`kopernicus_extras.yaml` — so these hexes feed nothing today anyway.

**MJ8 — Skeletal boards → silent engine defaults.**
Barnard (2 rows) and Tau Ceti (5, star-only) blanket-declare "그 외 passthrough" instead of
the per-axis confirm rows the silent-passthrough policy requires. Silently defaulted cells:
Barnard d/b/c/e and Tau Ceti f/g/h `inclination_deg` (0/90), Ω/ω/M (null), obliquity (0),
spin_axis, rotation_period; TRAPPIST-1 b–h `e=0` (also the Kopernicus
`temperatureEccentricityBiasCurve` divide-by-zero trap). Tau Ceti's headline **cold debris
disk** (6–55 AU, 14 Phase-3 decisions incl. tint #ffe2bb, mass 1.2 M⊕) has **zero** rows.

---

## MINOR

- **MN1 — enum violations:** `alpha_centauri.yaml:187 verdict: partial`, `:310 status:
  superseded` (both outside SPEC §0/§2 enums). The ring supersession disambiguation is real
  but relies on an out-of-contract status value.
- **MN2 — invented axes:** `alpha_centauri.yaml:73 orbit.elements_residual`, `:152
  bulk.residual` (free-form `.name`).
- **MN3 — `value` misplaced / renamed:** value nested under `gate.value` (αCen magnetism/
  environment rows) or renamed `target:` (αCen appearance rows) — a writer keyed on
  `row.value` gets nothing.
- **MN4 — `refs` integrity:** present on 2 of ~120 gated rows; `alpha_centauri.yaml:40
  refs:["2025AJ....Beichman"]` is a malformed bibcode (the real arXiv:2508.03814 is only in
  prose). All other bibcodes buried in `paper:` strings, unparseable.
- **MN5 — e≈0 divide-by-zero mitigation is prose on one unrelated body** only
  (`alpha_centauri.yaml:176`); Proxima b/c I and TRAPPIST-1 need a per-body flag or e-floor.
- **MN6 — stale cross-layer prose:** `docs/phase3/alpha-centauri-a-b.md:261` still says
  Pandora "~225 000 km / ~27 h" vs the board's 252,393 km / 32 h (the coverage audit's owed
  follow-up). `silent-passthrough-audit.md:72` still lists fomalhaut.yaml under "boards to
  create" (it exists). `figure/values.md:113` says Fomalhaut oblate "not emitted by default"
  vs the board gating it to emit.
- **MN7 — criterion vocabulary drifted** (`culture`, `classification`, `retention`,
  `activity-proxy`, …) — none in SPEC §2's menu; unconstrained without a validator.
- **MN8 — non-deterministic emit residue (HARD RULE 2):** αCen absolute sky-frame
  inclination = "free emit orientation", Ω/ω/M "seed 가능" (seed unpinned); proxima ring
  "faithful/vivid" with no default selector. Reproducibility gap, minor in effect.

---

## What actually PASSES (honest)

- `barnards_star.yaml` is the reference-quality board: typed `value`, `op:scale`,
  `phase3_default`, `evidence` + a `reproduce:` command + STABILITY_REPORT pointer, `refs`.
  Scale arithmetic verified exact against the DB (`per_planet_result*` = value × raw base).
- αCen numeric orbit/eccentricity/radius rows are emit-parseable.
- Star-body Principia inputs (GM, ICRS state, radius) are present for the roster stars →
  the stars-only MVP would emit.
- Gate *discipline* is sound where the schema fields are used: αCen aurora/obliquity
  divergences carry real `divergence_note`s. The failures are the missing typed field layer,
  not bad reasoning.
- Verified NOT defects: the 500 µT→170 µT Phase-3 follow-up **is** done (`docs/phase3/
  alpha-centauri-a-b.md:95` + ko mirror); all board cross-references resolve; `figure/
  values.md` is roster-complete (all 8 systems).

---

## Remediation path (ordered)

1. **Build the validator (BK1).** Even before writers exist, `check_phase4_gate.py`
   converts every silent defect above into a build failure. Highest leverage.
2. **Normalize the schema (MJ1–MJ4, MN1–MN4).** Split group rows into `group.name` rows;
   lift prose numbers into typed `value`; rename gate keys to `evidence`/`divergence_note`;
   lift bibcodes into `refs`; fix the two enum violations and the Beichman ref. Consider a
   `discoverability:` promotion + a per-body `emit_value`/`ring_color_variant` selector.
3. **Fix the mislabeled verdicts (MJ5, MJ6).** Convert the film-over-physical and
   below-threshold departures to `documented-divergence` + note; re-gate Erid as class D.
4. **Reconcile the emitter contracts (BK2, BK3, BK6, MJ7).** Decide, per writer, whether
   the board conforms to the emitter or vice-versa; recompute Pandora figure on 0.645 M⊕.
5. **Close coverage (BK-adjacent, MJ8).** Create `trappist_1.yaml`, `luhman_16.yaml`; board
   Tau Ceti planets + disk; add Barnard/Tau-Ceti passthrough-confirm rows; fix stale prose.

## Re-audit — 2026-07-11 (post-remediation, 4-lens adversarial)

Second adversarial pass over the remediated state (validator + schema v2 + α Cen v2
board + viewer + skill). Four independent lenses: validator-bypass construction (all
counterexamples run, not reasoned), board content integrity, delta vs this review,
skill/viewer accuracy.

**Delta scoreboard (the 15 BLOCKER+MAJOR above): 1 resolved / 6 partial / 8 open.**
The remediation was a sound single-board pilot (α Cen) plus a validator that only
strictly enforces that one board; the emitter side (BK2/BK3/BK5/BK7, MJ7) was
untouched by design ("emit wiring at project end").

**New findings, and their same-day fixes:**
- **BK6 had regressed into a contradiction** — the board moved Pandora to 0.645 M⊕
  but `figure/values.md` still carried the rejected 0.72 M⊕ and its J₂.
  **FIXED:** recomputed via `body_figure.synchronous_figure` on 3.85e24 kg →
  hydrostatic J₂ 2.17e-3, φ0.95 → **J₂ 2.06e-3 · C̄₂₂ 6.2e-4 · a−c 47 km (0.83 %)**,
  ratios 1.008:1.002:1.0 (still sphere-to-eye). Ledger + board narrative + typed
  fields all updated; the old 0.72-derived pair reproduced exactly, confirming the
  provenance.
- **Validator bypasses (empirically confirmed):** misspelled/absent `decisions:` key
  → whole board silently passes; `schema_version: "2"` (quoted) → strict board
  downgrades to legacy soft path (and the viewer skips it); `fields[]` entries with
  no `value` (prose-only numbers) pass; off-enum `op`; bare-string `refs` (rendered
  per-character by the viewer); duplicate live `(body, axis)` rows; non-hex `colors`;
  passthrough+gate only warned while three docs said hard-fail.
  **FIXED:** all of the above are now hard fails (`check_phase4_gate.py`), with
  `schema_version` normalization shared by the viewer, per-board crash isolation,
  and a 10-case synthetic counterexample run verifying each rejection (superseded
  pairs stay legal). Real boards still pass.
- **Board content:** the Polyphemus rings narrative resurrected the rejected
  1.05 R_Jup solid radius ("1.05 유지, ~1.10 관측") — **FIXED** to 1.0 + ~1.05
  observed (matches its own evidence: √(1.0²+0.32²)). Dante/Hades/Pandora
  `geopotential_j2` prose blobs → typed J₂ + C̄₂₂ fields. Cassandra biome label
  "6" vs 7 color keys disambiguated; storm-eye tint vs biome-map hex annotated as
  intentionally distinct pipelines.
- **Skill/viewer:** SKILL.md pointed at legacy-v1 `barnards_star.yaml` as a
  reference exemplar (illegal-in-v2 gate keys) — **FIXED** (α Cen is the sole v2
  shape exemplar). Viewer silently dropped `window`/`colors`/`note`/
  `phase3_default`/`depends_on` — **FIXED** (all render; pages regenerated).
  `board-schema.md` now documents those keys and the new hard-fail list. Both tools
  registered in `docs/reference/tools.md` (§13) + ko mirror.

**Still open (unchanged priorities):** the five v1 boards (validator soft on them;
MJ1–MJ8's live cited rows all sit there), the absent `trappist_1`/`luhman_16`
boards, all emitter contracts (RB emitter reads top-level `discoverability:`, not
the v2 per-row `discoverability_cfg` → still emits nothing), `check_dead_links`
not globbing `phase4/*.yaml`, `criterion` vocabulary unvalidated, and four refs not
in the `_papers` cache (`1109.1627`, `2007.10783`, `1609.06324`, `2107.07434`).
Dante's ~820× Io tidal-heat figure should be reconfirmed against the final
e=0.01 roster (claimed mean forced e 0.0175 from oscillation — recheck at next
stability-sim run).

**Verified clean this pass:** Pandora 0.72-residual sweep (all mass-coupled values
recompute on 0.645), all six biome palettes vs the preview (hex/name/count, no
intra-body duplicates), v1→v2 migration row parity, viewer determinism +
HTML-escaping + `_naming` slugs, check.sh gate-8 crash propagation.

## Related
- `phase4/SPEC.md` — the data contract this review measures against
- `phase4/phase4-coverage-audit.md` — α Cen (body×axis) sweep
- `phase4/silent-passthrough-audit.md` — full-roster silent-default sweep
