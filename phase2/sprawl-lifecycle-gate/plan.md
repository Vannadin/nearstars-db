# Plan — sprawl-lifecycle-gate (repo layout + artifact lifecycle)

Promoted 2026-07-19 from [`plans/doc-tool-sprawl-audit.md`](../../plans/doc-tool-sprawl-audit.md)
(2026-06-03 audit), scope expanded after a 2026-07-18 re-audit found the
phase-convention divergence the original audit did not cover.

## Problem

Two related gaps:

1. **Lifecycle (June audit, half-executed).** F1 (gate-5 false positive) and part
   of F3 were fixed; F4 (un-indexed `scripts/refs/*.py`), F5 (loose session logs,
   `_audit/` scratch+canonical mix), F7 (AGENTS.md §2.1 mirror-scope drift), the
   §2.4 lifecycle rule, and the sprawl gate were never done.
2. **Phase-convention divergence (new).** phase4/ is absent from the AGENTS.md §2
   document homes, so its root accreted 4 viewer HTML + 6 loose review/audit .md
   beside the `<system>.yaml` boards. Audits live in three different conventions
   (phase3/_audit/, phase4 root, plans/). Committed `.log` files escaped the
   .gitignore (root-only patterns). Slugs diverge across phases (tau_cet vs
   tau_ceti; alpha_centauri_proxima vs two phase4 boards).

## Fix bundles (this effort)

1. **Rules first** — AGENTS.md §2: register phase4/ as a documentation home with a
   fixed root taxonomy; generalize §2.1 mirror scope (F7); add §2.4 artifact
   lifecycle rule; legalize plans/ subdirs for multi-doc research programs.
2. **Mechanical relocation** — phase4 root loose files into `_audit/` /
   `art-direction/` / `policies/` / `viewers/` (filenames preserved — prose
   references cite bare filenames); phase2 session logs into `tier1-stellar/`;
   `phase3/_audit/` scratch JSON into gitignored `_scratch/`; ignore + untrack
   stability-sim `results/**` logs.
3. **Guardrail** — check.sh gate 9: phase-root layout allowlists, empty dirs,
   tracked `*.log`, un-indexed `scripts/refs/*.py`.
4. **Index backfill** — 8 missing `scripts/refs/*.py` lines in tools.md (+ko),
   one-shot/regenerable header markers.

## Deferred (separate session)

- **Slug unification** (tau_ceti → tau_cet; alpha Cen board split policy) — needs
  reference tracing across phase4 YAML + docs/phase4 + emit scripts; must land
  before emit wiring.
- docs/ root versioned duplicates (`index.v1.html`, `style.v2.css`, …) — deletion
  needs owner confirmation.
- stability-sim `results/_viewers/` stays where it is (sim-owned output tree);
  only logs are reaped.
