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
