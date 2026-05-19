# principia-cfg — Context Notes

Decisions made during skill construction and the reasoning behind them. Append continuously. The next session should not have to re-derive these from code.

---

## Scope decisions (set at user-question step before coding)

### MVP = Sol real scale only, stars only

**Decision**: Emit `Real_NearStars-GravityModel.cfg` + `Real_NearStars-InitialState.cfg` for Sol real scale. Skip Sol quarter, RSS, and planets.

**Reasoning**:
- Sol real scale is the project's primary integration target.
- Sol quarter needs a different `solar_system_epoch` (`JD 2433465.0` vs `JD 2433282.5`), so the Cartesian coords are not reusable — a separate emission pipeline. Defer until Sol quarter is actually used.
- RSS uses the same epoch as Sol real, so coords ARE reusable, but the NEEDS tag differs. Tiny addition once Sol real is shipping.
- Planets require ICRF Cartesian state, which the DB does not currently provide. The Keplerian → Cartesian + frame-rotation problem (star pole orientation, KSP frame ↔ ICRF) is not solved. See `references/planet-contract.md` for the forward path.

**User confirmation**: explicit at decision time — "1번으로 가되, 어떤 행성계를 만들지 선택해서 페이즈2를 진행하면 필요한 자료가 충분히 모일거야".

### Distance scope = all of `db/systems/`

**Decision**: No distance filter in the emit script. Emit every star in the DB.

**Reasoning**:
- NearStars project policy is "all bodies within 50 ly" (per user clarification 2026-05-20).
- The DB pipeline already enforces this — max distance in current DB is 49.7 ly (HD 238090).
- Principia engine technically supports up to ~80 ly (per `docs/reference/guideline.md` §3.1), but the project does not use that band. No Principia-only entries for the 50–80 ly range; no special handling needed.
- If a future change pushes a 50+ ly star into the DB, this assumption needs revisiting (Kopernicus may not accept it; Principia would need to be `Principia-only` form).

### Strict abort on incomplete DB

**Decision**: If any star is missing `principia.gravitational_parameter_km3_s2` or `derived.icrs_*`, collect all errors and abort. No partial emit.

**Reasoning**:
- Per Principia constraint (§Key Constraints in reference doc): if `principia_initial_state` is present, every body in `FlightGlobals.Bodies` must have entries in both gravity_model and initial_state.
- A partial emit looks healthy until KSP load time, then crashes. Loud failure at build time is safer.
- Errors are batched so the operator gets a single complete punch-list, not one-at-a-time fixes. User confirmed: "Strict abort + 전체 에러 수집해 표시".

---

## Schema / format decisions

### Body name normalization

**Decision**: Split on whitespace, drop non-alphanumeric per token, then: if any uppercase letter exists, keep verbatim; if all lowercase, capitalize first letter.

**Examples**:
- `Alpha Centauri A` → `AlphaCentauriA`
- `GJ 1002` → `GJ1002` (uppercase prefix preserved)
- `Barnard's star` → `BarnardsStar` (lowercase "star" capitalized)
- `eps Eri` → `EpsEri`

**Reasoning**:
- The first attempt (just strip non-alphanum, preserve case) produced `Barnardsstar` from `Barnard's star` — wrong because the DB has lowercase "star".
- Pure `str.title()` would break all-uppercase catalog prefixes like `GJ`, `HD`, `TRAPPIST`.
- The chosen rule respects intent: tokens already typed with capitalization are intentional (`AU`, `TRAPPIST`), tokens that are sloppy (`star`, `eps`) get fixed.
- Override available via optional `stars[].kopernicus_body_name` for cases the rule doesn't handle (e.g. `eps Eri` → user-preferred `EpsilonEridani`).

### `:NEEDS[NearStarsSystem,SolSystem]` over `:NEEDS[SolSystem]:FOR[NearStarsSystem]`

**Decision**: Principia patches use `@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem]`, omitting `:FOR[NearStarsSystem]`.

**Project context**: `docs/reference/guideline.md` §5.1 example for `@EVE_CLOUDS` uses the `:NEEDS[SolSystem]:FOR[NearStarsSystem]` form. This is the project's general convention.

**Reasoning for divergence**:
- The guideline example is for nodes NearStars **creates** (EVE_CLOUDS). `:FOR[NearStarsSystem]` claims authorship of that new block — correct.
- Principia root nodes (`principia_gravity_model`, `principia_initial_state`) are created by Sol-Configs, not by NearStars. NearStars merely `@`-edits them.
- For `@` edits of existing nodes, `:FOR[NearStarsSystem]` is functionally a no-op (the patch already runs after the original `:FOR[SolSystem]` pass), so the shorter `:NEEDS[NearStarsSystem,SolSystem]` is preferred.
- Both forms work; this is a node-class-specific judgment within the guideline's spirit, not a contradiction of it.

### Output path: `Patches/Principia/` over `Patches/Sol/`

**Decision**: Cfg files land in `dist/NearStars-Configs/Patches/Principia/`.

**Project context**: `docs/reference/guideline.md` §4 directory tree puts solar-system-specific patches in `Patches/Sol/` and `Patches/RSS/`.

**Reasoning for divergence**:
- The Principia patches are single-file-per-variant (one GravityModel.cfg + one InitialState.cfg covering all 152 bodies), unlike per-body cfgs that fit cleanly in `Patches/Sol/`.
- Sol-Configs (the upstream we mirror) uses `Patches/Principia/` for its own Principia files. Authors familiar with Sol-Configs will look here first.
- Grouping all Principia files in one folder makes Sol-vs-RSS-vs-Quarter comparisons trivial when those variants are added later.
- The `NearStars-Configs/Patches/` prefix still matches the guideline's tree structure — the divergence is one level deeper.

### File header Korean comments

**Decision**: Both Python scripts have a one-line Korean comment directly after the shebang.

**Reasoning**: CLAUDE.md §6 — agents read files selectively and benefit from instant role context. The reference .md files don't get Korean headers (rule scopes to source code).

---

## Implementation decisions

### `--system` flag is repeatable

`--system alpha_centauri_a --system alpha_centauri_b` selects two stems; running with no `--system` selects all 152.

**Reasoning**: Single-stem `--system` could only test one body at a time, which made multi-body emit verification awkward (alpha-Cen-A/B needed both). Repeatable flag is the standard argparse pattern (`action="append"`) — no real complexity added.

### `dev_backfill_spt_mass.py` exists

A separate helper script that adds `unverified` mass/radius measurements (Pecaut & Mamajek 2013 SpT lookup) to 14 stars currently missing them.

**Reasoning**:
- 14 stars (5–15 pc range) are present in DB but have empty `mass_measurements` → `principia.gravitational_parameter_km3_s2 = null` → strict abort.
- For skill verification purposes, we needed a way to populate these without manually editing each file.
- The script writes to both `db/stellar_props_curated.json` (canonical source) and the 14 system files (build artifact, regenerated by `build_systems.py` — duplicated here so emit works without pipeline rebuild).
- Method = `unverified` (the schema-allowed method that best matches an estimated, non-catalog value); origin = `spt_estimate: Pecaut & Mamajek 2013 (...)` in the reference field.
- This helper is **not** part of the skill's runtime. It's for testing only.
- After verification, the 14 backfilled rows were reverted via `git checkout` — they're not in any committed state. Real curation should come from literature lookup, not from SpT estimates.

### `dist/` is gitignored

Build artifacts are deterministic from `db/`. Re-running the script produces byte-identical output if the DB hasn't changed. Committing them would create noisy diffs.

---

## Things deliberately NOT done (with reasoning)

- **No KSP load-test**. The skill produces syntactically valid cfg per the Principia source reference, but no KSP run has confirmed acceptance. Listed as open item in `checklist.md`.
- **No `principia_numerics_blueprint` patch**. Sol-Configs ships its own; modifying it would affect the entire simulation, not just NearStars bodies.
- **No `axis_right_ascension` / `axis_declination` per star**. DB has no rotation-pole measurements. Principia's default (`-90 deg / 90 deg`) aligns the pole with KSP's world frame — cosmetic only for stars at LY distance.
- **No `j2` / `geopotential_row`**. DB has no zonal-harmonic measurements for nearby stars.
- **No retry / continue-on-error logic in emit**. Strict abort is the chosen behavior; partial emits would be more dangerous than no emit.

---

## Recovery / history events worth noting

- **2026-05-20**: First commit (`b69f722`) accidentally bundled in `ko/` (12 unrelated files from another parallel session). Recovered via `git reset --soft HEAD~1` → `git restore --staged ko/` → recommit (`6c5a96e`). Root cause unclear (no active git hooks, `git add` was scoped to skill dir only). Likely concurrent session interaction. Take-away: always run `git diff --cached --stat` (no path filter) and inspect full output before committing in multi-session environments.
