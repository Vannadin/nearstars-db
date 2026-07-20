# Context notes — pipeline-flow-program

Append-only. Started 2026-07-20.

## 2026-07-20 — program start

- Owner clarification: the "resolver" (WP1) is the **db → phase3 → phase4
  linkage layer**, not the cfg emitters. Emitters keep their job (formatting
  cfg syntax); the resolver is the single upstream merge they will all read at
  emit-wiring time.
- Owner decisions: floor backfill scope = **all curated hosts ≤ 50 ly** (not
  roster-only); WP0–3 greenlit now, WP4–5 separately scheduled.
- Execution order WP0 → WP2 → WP3 → WP1 (contract first, then lock with gates,
  then shapes, then the spine).
- Shared parser moved from WP1 into WP2 because the parse gate needs it; the
  resolver builds on it.
- Emitters are deliberately NOT rewired in this program — standing policy keeps
  emit wiring at project end. The contract records the target architecture and
  emit-hardening tracks the rewiring item.

## 2026-07-20 — execution decisions & findings

- **guideline.md §9 was the fossil**: it still carried the pre-rebuild Phase 1–4
  numbering (star skeleton/planets/visuals/polish). Replaced with a pointer to
  the contract; a historical note explains any doc using the old numbering.
- **dict→list migration rejected as mechanical work**: the list form requires
  `method`, which is a per-paper curation judgment. Fabricating it by script
  would violate the grounding discipline. Re-scoped to §A1 upgrade-on-touch +
  the gate-10e census; actual upgrades ride along the floor-backfill sessions.
- **Floor classifier gotcha**: lowercase dwarf-notation spectypes (`dM4`,
  `sdM1`) must not be read as white dwarfs (uppercase `DA/DB/…`). Ross 128 /
  Wolf 1069 were misclassified until the prefix strip landed.
- **Report slug wrinkle**: planet report files follow host-slug+letter, which
  equals the planet-name slug everywhere except Barnard (`Barnard b` →
  `barnards-star-b.md`). Gate and resolver accept both; contract §2 documents it.
- **Resolver dry-run finding (load-bearing)**: phase3 Decisions names and
  phase4 fields[] names never collide — the override layer semantically works
  but has no shared vocabulary to override *onto*. The field-alignment map
  (menu name ↔ decision key ↔ cfg key) is therefore the single biggest emit
  prerequisite. Raw material exists (curation SPEC "full cfg field inventory").
- **WP6 (owner mid-program directive)**: paper ids → links. Whitelist-safe
  converter (only `_bib`-known arXiv ids or `arXiv:`-prefixed convert; spans in
  code/links protected; idempotent — double-conversion bug caught in dry-run
  and fixed by re-protecting between regex passes). 1,967 links / 217 files;
  phase3 HTML + wiki re-rendered.

## 2026-07-20 — field-alignment map (the emit prerequisite, closed)

- **The disjointness had a simple cause**, found by listing both vocabularies
  side by side: phase4 boards write the owner's menu choice WITHOUT units
  (`mass: 0.78`, `radius: 0.806`, `rotation_period: 37–43`), phase3 Decisions
  bake the unit into the key (`mass_msun`, `radius_rsun`, `rotation_period_days`).
  305 phase3 keys vs 93 phase4 names, 0 collisions — not two unrelated
  ontologies, just one ontology written twice at different unit-awareness.
- **Map shape chosen accordingly**: per board menu name, a PRIORITY LIST of
  phase3 candidate keys. The resolver picks the first candidate present in that
  body's own report — which is how a unit-less board value lands on the correct
  unit variant per body class with no class logic in the resolver itself.
  `scripts/pipeline/field_alignment.yaml`, 93/93 covered.
- **Result**: override layer went from decorative to real — α Cen 0 → 24 real
  overrides, 40 Eri 36, tau Cet 4. `effective[]` now carries `board_name` +
  `overrides_phase3` so an emitter can tell a genuine override from a
  board-only field.
- **Empty `phase3:` is meaningful, not missing**: gameplay axes (difficulty,
  science_biomes, timewarp_limits, sphere_of_influence_tuning), ring textures,
  and fiction-body art are board-authoritative by design and emit unopposed.
  Recorded as such rather than left looking like coverage holes.
- **Unit traps found while mapping** (recorded in emit-hardening, must be
  handled at emit arithmetic): board `pressure` atm/bar vs phase3 Pa; board
  `surface_temperature`/`temperature` sometimes °C vs phase3 K; board `gravity`
  absolute m/s² vs phase3 g_earth. Also `base_colour`/`base_color` spelling
  duplicate — mapped both, normalize on next board touch.
- **Gate 10f** warns on unmapped board field names (verified it fires by
  removing an entry in a scratch run). Coverage is enforced, not asserted.
