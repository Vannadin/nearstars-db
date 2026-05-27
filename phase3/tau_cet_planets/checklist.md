# τ Cet f / g / h — Phase 3 checklist

Three planets from Feng 2017 RV detection. All `pl_controv_flag=1` in
NEA (disputed). RV-only, no transit, no direct imaging. Expect
Confidence=low to medium on most Decisions rows.

## Stage 0 — pre-flight
- [x] Phase 2 present (`db/systems/tau_cet.json` curated f / g / h orbital + Msini)
- [x] Host Phase 3 done (`docs/phase3/tau-cet.md`)
- [x] User input reviewed (h period discrepancy: user said P=4562 d / 5 AU, DB has P=49.41 d / 0.243 AU — DB is authoritative; flag as open item)

## Stage 1 — classification log
- [x] Per-row classification table per planet
- [x] Report canonical-aligned / tie-break / divergence counts

## Stage 2 — English drafts
- [x] f — header + intro + Decisions + 4 prose sections + bibliography + open items
- [x] g — header + intro + Decisions + 4 prose sections + bibliography + open items
- [x] h — header + intro + Decisions + 4 prose sections + bibliography + open items

## Stage 3 — Korean mirrors
- [x] f mirror — block-parity match with English
- [x] g mirror — block-parity match with English
- [x] h mirror — block-parity match with English

## Stage 4 — verification + HTML
- [x] `python3 scripts/phase3/check_block_parity.py tau-cet-f tau-cet-g tau-cet-h`
- [x] `python3 scripts/phase3/build_html.py tau-cet-f`
- [x] `python3 scripts/phase3/build_html.py tau-cet-g`
- [x] `python3 scripts/phase3/build_html.py tau-cet-h`
- [x] `bash scripts/check-mirrors.sh`
