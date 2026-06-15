<!-- Phase 4(게임용 art-direction 최종 확정) 미구현 — 그 전까지 art-direction 초안을 모아두는 스테이징 디렉터리 -->
# phase4/ — Art-Direction Drafts (pre-implementation)

**Phase 4 is NOT yet built.** This directory stages art-direction drafts so the
creative decisions are recorded now and ready to activate once Phase 4 is
formalized. Nothing here is gated or committed to the DB — these are drafts.

## Where Phase 4 sits

```
Phase 1  basic curation
Phase 2  paper-cited measurements
Phase 3  cfg-ready synthesis — PRESENTS options (tie-break / documented divergence)
Phase 4  user picks the art-direction → 고증 gate → final game cfg   ← these drafts
```

Phase 3 defines the *physically defensible window* and an interesting-first
default. Phase 4 is where the **user's creative art-direction** is chosen and
passed through a 고증 (canonical-consistency) gate: choices inside the window
emit directly; choices outside it are emitted as a **documented divergence**.

These drafts capture (a) the user's creative target, (b) the Phase 3 window it
must be checked against, and (c) where the target sits relative to that window —
so the eventual Phase 4 gate has the analysis pre-staged rather than re-derived.

## Drafts

- [`polyphemus-art-direction.md`](polyphemus-art-direction.md) — α Centauri A b
  (the real-life *Avatar* Polyphemus): a banded ivory + blue gas-giant look.

## Orbit-optimization records

When an orbit is **optimized** with the stability sim (the observed/maximal orbit
is dynamically untenable, so a defensible stable orbit is selected), the process +
conclusion are logged for the Phase 4 gate — with any unresolved cfg-frame quantity
flagged as an open item.

- [`orbit-optimizations.md`](orbit-optimizations.md) — running log. First entry:
  α Cen A b (stability-selected a 1.6 / e 0.1 / mutual i 16°; cfg-frame sky
  inclination is the open Phase 4 item).
