<!-- Phase 4(게임용 art-direction 최종 확정) 미구현 — 그 전까지 결정 보드·art-direction 초안을 모아두는 스테이징 디렉터리 -->
# phase4/ — Decision Boards + Art-Direction Drafts (pre-implementation)

**Phase 4 is NOT yet built.** This directory stages the decisions so they are
recorded now and ready to activate once Phase 4 is formalized. Nothing here is
gated into the DB or emitted — these are staged records.

## Where Phase 4 sits

```
Phase 1  basic curation
Phase 2  paper-cited measurements
Phase 3  cfg-ready synthesis — PRESENTS options (tie-break / documented divergence)
Phase 4  per-decision: owner art-directs → 고증 gate → final game cfg   ← staged here
```

## How Phase 4 works (see [`SPEC.md`](SPEC.md) §0)

Phase 4 is **not** sequential ("art-direct everything, then gate it"). The unit is
**one decision = (body × axis)**; each flows on its own clock through two roles:

- **4a — art-direction (owner)** states the intent for one axis (or leaves it to the
  Phase 3 default).
- **4b — gate (agent)** checks that target against Phase 2 + Phase 3 →
  `pass-in-window` / `documented-divergence`, and writes the cfg-ready value.

Axes come from a **fixed menu** (orbit / bulk / atmosphere / appearance / satellites),
uniform across all body types — never pruned by type (a rocky planet still has a
`rings` axis). Most axes are `passthrough` (Phase 3 default emits unchanged); Phase 4
is only the *deltas*.

## Decision boards (the progress record)

One `<system>.yaml` per system; one row per (body, axis) with a per-row `status`
(`passthrough` / `open` / `art-directed` / `gated` / `emitted`). The board **is** the
progress tracker — `grep status:` shows what is left.

- [`barnards_star.yaml`](barnards_star.yaml) — mass × 1.1547 (median true mass) and
  e × 0.8 (fixed-step-stable, closest-to-observed), both `gated`. Process + scan tables
  in `../phase3/stability-sim/STABILITY_REPORT.md`.
- [`alpha_centauri.yaml`](alpha_centauri.yaml) — α Cen A b (Polyphemus): orbit a/e
  `gated`, sky-frame inclination `open`; the white/gold/blue banding + ring + aurora +
  Pandora rows at various states. The worked template for a many-axis body.

## Art-direction drafts (4a creative input)

Free-form creative scratch that feeds the boards above; **not** the record.

- [`art-direction/polyphemus-art-direction.md`](art-direction/polyphemus-art-direction.md) — α Cen A b (the
  real-life *Avatar* Polyphemus): the banded ivory + blue gas-giant look, Avatar canon,
  Pandora climate. Its gated conclusions live in `alpha_centauri.yaml`.

## Policies

- [`policies/synthetic-orbit-noise.md`](policies/synthetic-orbit-noise.md) — de-perfecting default
  orbital elements (0 / 90 / e=0) with seeded, physically-bounded noise; never touches
  measurements, stability-gated. The transit-preserving inclination bound is the
  headline guardrail.
