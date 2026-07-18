<!-- Phase 4 emit-hardening 결정 로그 — 스키마 v2 설계 근거와 작업 중 내린 판단을 계속 append -->
# Phase 4 Emit-Hardening — Context Notes

Append-only decision log. Companion to `checklist.md`.

## 2026-07-10 — Schema v2 design decision (the load-bearing choice)

**Problem.** The review's dominant defects (MJ1 group-only axis, MJ2 prose `value`) come
from one row bundling many emit fields as prose. SPEC §3 v1 says "one row = one
`group.name` field" — taken literally, α Cen would explode to hundreds of atomic rows.

**Two candidate fixes:**
- (a) **Atomic rows** — one row per `group.name`. Faithful to v1 literal; very verbose.
- (b) **Group row + typed `fields:` map + `narrative:`** — keep one row per (body, axis
  *group*), add a machine-readable `fields:` list (one typed entry per emit field) and keep
  the human prose in `narrative:`.

**Chosen: (b).** Rationale:
- The owner explicitly wants "prose explanation + exact numbers together in a table" for
  the viewer — that is literally `narrative` + `fields` per (body, axis) row. The viewer
  renders one table row per decision, numbers from `fields`, prose in an expandable cell.
- Keeps the valuable curation prose instead of discarding it (a) or duplicating it.
- Still fully emit-parseable: a writer reads `fields[].{name,value,unit,op}`.
- The review already noted `discoverability_cfg` as "beneficial drift worth promoting" —
  same spirit: promote structured sub-objects into the schema rather than fight them.

**v2 row shape (canonical):**
```yaml
schema_version: 2                 # file-level; absence ⟹ legacy v1 (soft-checked)
decisions:
  - body: "Alpha Centauri A b"
    kopernicus_name: Polyphemus   # optional; the cfg-internal name emitters/RB need
    axis: bulk                    # a §0 group; or group.name for a single-field decision
    status: gated                 # passthrough|open|art-directed|gated|emitted|superseded
    driver: [window-selection, art-direction]
    narrative: >                  # human prose (KR ok; source-of-truth stays the fields)
      ...
    fields:                       # one typed entry per emit field (machine-readable)
      - name: radius              # → bulk.radius
        value: 1.0
        unit: R_jup
        op: set                   # set | scale | passthrough
        phase3_default: "1.0 R_Jup (low)"
        verdict: pass-in-window   # optional per-field; else inherits gate.verdict
        divergence_note: null     # required iff this field's verdict == documented-divergence
    gate:
      criterion: [observation]
      verdict: pass-in-window     # row-level default verdict
      evidence: >
        ...
      divergence_note: null       # required iff row verdict == documented-divergence
    refs: ["2508.03814"]          # bibcodes/arXiv ids, machine-readable list
    discoverability_cfg: {...}    # promoted structured block (identity axis)
```

**Enum additions.** `status` gains `superseded` (a decision replaced by a later one; the
row is retained for provenance but carries no live gate and is never emitted). `verdict:
partial` is NOT added — it is illegal; a "partial" row must split into a pass-in-window
part and a documented-divergence part.

**Validator policy.** `schema_version: 2` ⟹ strict (hard-fail on enum/gate/divergence
violations). Legacy files ⟹ soft warnings only, so the un-migrated boards keep check.sh
green while migration proceeds file-by-file. HARD fails: bad status, bad verdict,
documented-divergence with null note, axis group not in the §0 menu, passthrough row that
carries a gate. WARN: missing `evidence`, no machine-readable value on a gated row, no
`refs` on a gated row, `.name` not in the axis menu.

## Backlog / open
- BK6 (Pandora figure recompute on 0.645 M⊕) is a physics recompute, not a rename — needs
  the Radau-Darwin response redone at the new mean density; parked to step 4.
- Whether to also render Proxima on the α Cen viewer page or keep systems separate: the
  confirmed-set couples them ("α Centauri (+ Proxima)") — leaning toward one page, two
  system sections.

## 2026-07-11 — re-audit hardening pass (post model-switch second audit)

Trigger: 4-lens adversarial re-audit (validator bypass / board content / delta vs
review / skill+viewer). Full findings recorded in
`phase4/_audit/emit-readiness-review.md` §"Re-audit — 2026-07-11".

**Validator hardening (all bypasses were empirically confirmed first).** New hard
fails: missing/misspelled `decisions:` list, fields[] entry without name/value
(prose-only numbers now rejected — this closes the "gated override silently degrades
to Phase 3 passthrough" hole), off-enum `op`, non-list `refs`, non-#RRGGBB `colors`,
duplicate live `(body, axis)`, passthrough+gate (was warn; three docs already said
hard-fail, code now agrees). `schema_version` normalized (2/2.0/"2") in BOTH the
validator and the HTML builder so a quoting slip can't downgrade a strict board.
Per-board try/except so one crashing board no longer hides the rest. Superseded
pairs on the same (body, axis) remain legal — that IS the supersede mechanism.

**BK6 closed the right way.** `figure/values.md` Pandora recomputed on the gated
3.85e24 kg via `scripts/refs/body_figure.synchronous_figure` (old 0.72-M⊕ numbers
reproduced exactly first → provenance confirmed): J₂ 2.06e-3 · C̄₂₂ 6.2e-4 ·
a−c 47 km (0.83 %) · ratios 1.008:1.002:1.0. Conclusion unchanged (sphere to eye,
gravity-only). Board j2 rows for Dante/Hades/Pandora converted from prose blobs to
typed J₂ + C̄₂₂ fields (J₂ = 10/3·C̄₂₂ kept in `note`).

**Decision: field-level `note`/`window`/`colors`/`phase3_default` + row `depends_on`
are now schema-documented and viewer-rendered** — they were live in the α Cen board
but invisible to both the authoring card and the review pages (write-only gate data).

**Not done here (still open, unchanged priorities):** 5 v1 boards, absent
trappist_1/luhman_16 boards, every emitter contract (incl. RB emitter reading the
old top-level `discoverability:`), dead-link glob for `phase4/*.yaml`, `criterion`
vocabulary, 4 refs missing from `_papers`, Dante ~820× Io recheck at e=0.01.
