# Proxima board normalization (gate warnings) + audit X4

Owner call 2026-08-03: after the Dante/Chaos pass, take the Proxima board's
convention layer. 53 rows, 0 gate errors, 31 warnings. Deterministic target: the
warning list shrinks to the ones that are genuinely owner decisions.

## Mechanical (warning-closing)

- [ ] `driver` vocabulary: 52 rows off the SPEC §1 five-class list
- [ ] `**` emphasis markup: 39 rows (renders literally in KO)
- [ ] em-dash in rendered fields: 44 rows (CONVENTIONS §1.10)
- [ ] banned calques: 가스자이언트 ×1, 구름덱 ×2
- [ ] deferred `difficulty` field authored: 4 rows (SPEC §0 defers the facet)

## Content (audit X4)

- [ ] Proxima Cen d `appearance` + `base_color` still derive from the retired
      `#34302c`; `surface` superseded it with `#3c3833` + a dark polar cap, and the
      appearance row drops the two-tone entirely
- [ ] `provenance` line on every row whose value moves

## Deliberately NOT in this pass

- refs backfill on the ~20 gated rows with no refs (needs paper/methodology lookup
  per row; owner deferred)
- `satellites` rows with no machine-readable fields (3) and `c/satellites` empty
  evidence
- a full consistency audit of this board

## Close-out

- [ ] `python3 scripts/check_phase4_gate.py` — warnings down, still 0 errors
- [ ] rebuild the proxima board pages
- [ ] `./scripts/check.sh`
- [ ] commits, one per logical change
