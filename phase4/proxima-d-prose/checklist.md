# Proxima d prose modernization — checklist

Owner decision (2026-08-07): bring the 10 old-style d rows up to the current
SPEC §3.1 prose contract (b / c I are the bar), one axis at a time, one commit
per axis. Values are frozen — this is a prose/taxonomy pass, not a re-gate.

Per-axis work items (apply to each row as relevant):
- narrative → story style, EN `narrative` + `narrative_ko` pair
- strip workflow vocab, G-tokens, raw field names, inline citations, dates
- evidence → fixed 3-part shape (conclusion → check performed → honest caveat)
- decision/value history → `provenance` (one line per change, newest last)
- verdict: recipe-computed rows migrate pass-in-window → methodology-derived

## Pre-flight
- [x] Commit the validator absence-row refs exemption (ad00ce0)

## Axes
- [x] identity (also: drop retired RB discoverability tuple from evidence) — 03f74a7
- [ ] orbit
- [ ] bulk (→ methodology-derived)
- [ ] atmosphere (→ methodology-derived)
- [ ] surface (→ methodology-derived)
- [ ] appearance (add EN narrative; already new-style otherwise)
- [ ] magnetism.magnetic_field
- [ ] environment (→ methodology-derived)
- [ ] rings
- [ ] satellites
- [ ] gameplay (drop retired 난도 value; 3-part shape; engine bits → evidence)

## Close-out
- [ ] check_phase4_gate.py 0 errors, no new warnings
- [ ] build_phase4_html.py proxima_cen (per commit)
- [ ] tick proxima-planet-reaudit stale checkboxes (done 2026-07-14, never ticked)
