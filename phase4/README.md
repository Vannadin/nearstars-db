<!-- Phase 4(오너 art-direction → 고증 게이트 → 게임 cfg 확정) 결정 보드 트리 — canonical 절차는 nearstars-phase4 스킬, 계약은 SPEC.md -->
# phase4/ — Decision Boards (owner art-direction → gate → cfg)

Phase 4 is **operational**: schema v2 boards, a validator wired into
`check.sh` (gate 8), body↔db join checks (gate 10), a per-body HTML viewer,
and the `nearstars-phase4` skill as the canonical procedure. The one thing
still deferred is **emit** — boards are not yet read by the cfg writers
(project-end task; see `emit-hardening/checklist.md`).

## Where Phase 4 sits

```
Phase 1  basic curation
Phase 2  paper-cited measurements
Phase 3  cfg-ready synthesis — PRESENTS options (tie-break / documented divergence)
Phase 4  per-decision: owner art-directs → 고증 gate → final game cfg
```

Cross-phase flow, join keys, and the value-resolution order live in
[`docs/reference/pipeline-contract.md`](../docs/reference/pipeline-contract.md);
the resolver (`scripts/pipeline/resolve_emit_values.py` +
`field_alignment.yaml`) merges db → phase3 → phase4 per body.

## How Phase 4 works (contract: [`SPEC.md`](SPEC.md))

The unit is **one decision = (body × axis)**, each on its own clock:

- **4a — art-direction (owner)** states the intent for one axis, or leaves the
  Phase 3 default.
- **4b — gate (agent)** checks that target against Phase 2 + Phase 3 →
  `pass-in-window` / `documented-divergence`, and writes the cfg-ready value.

Axes come from a fixed menu, uniform across body types (§3.2 bulk template:
three body classes with fixed field sets + `na_reason`). Every axis is
presented as a choice — silent passthrough is not allowed. Naming contract
(SPEC §3): board filename = db system slug, `body:` keys = db names exactly,
fiction bodies marked `discoverability: fictional`.

## Boards (one `<system>.yaml` per dynamical host group)

`grep status:` on a board shows what is left; row states are
`passthrough / open / art-directed / gated / emitted / superseded`.

- [`alpha_centauri.yaml`](alpha_centauri.yaml) — the worked many-axis template
  (A b "Polyphemus" + fictional moons); schema v2 pilot.
- [`proxima_cen.yaml`](proxima_cen.yaml), [`barnards_star.yaml`](barnards_star.yaml),
  [`40_eridani.yaml`](40_eridani.yaml), [`tau_cet.yaml`](tau_cet.yaml),
  [`fomalhaut.yaml`](fomalhaut.yaml)
- Missing (tracked as gate-10 warnings): `trappist_1.yaml`, `luhman_16.yaml`;
  tau_cet planet rows.

Viewer: `scripts/phase4/build_phase4_html.py` → `docs/phase4/<system>.html`
(bilingual, status/verdict badges).

## Working trees under this root

- [`emit-hardening/`](emit-hardening/) — remediation checklist toward emit
  (validator done; field-alignment map done; emitter rewiring pending).
- [`figure/`](figure/) — J₂/C₂₂ figure program working files (values ledger,
  per-body research).
- [`art-direction/`](art-direction/) — free-form 4a creative drafts
  (e.g. [`polyphemus-art-direction.md`](art-direction/polyphemus-art-direction.md));
  feeds boards, never the record.
- [`policies/`](policies/) — cross-system rules
  (e.g. [`synthetic-orbit-noise.md`](policies/synthetic-orbit-noise.md)).
