<!-- Phase 3 항성풍 합성 작업 체크리스트 -->
# Stellar-wind synthesis checklist

## ② Field spec (mod-grounded-fields.md)
- [x] New section "Kerbalism stellar wind / astrosphere fields (star body)"
- [x] Field table (radiation_surface, solar_cycle, astrosphere_standoff, apex RA/Dec, V_ISM, wind speed)
- [x] Sun anchor row + derivation formulas
- [x] Source priority list
- [x] Plugin-only note for apex direction
- [x] Cross-link to project-nearstars-stellar-wind-kerbalism + flux-tube-plugin
- [x] Decisions-table presentation rule (missing values: row always kept, status in value cell — a3be380)

## ① Per-star Decisions (docs/phase3/<host>.md + ko + HTML)
- [x] alpha-centauri-a — cycle 19.1 (tentative), Mdot 2, V_ISM 25, standoff ~176 AU, apex
- [x] alpha-centauri-b — cycle 8.84, shares αCen astrosphere
- [x] proxima-cen — cycle 7, Mdot<0.2, standoff <56 AU (limit), radiation_surface HIGH (flares)
- [x] tau-cet — Mdot<0.1, no cycle (flat), standoff upper bound
- [x] 40-eridani-a — cycle 8.70, no Mdot (astrosphere from astrometry/activity), apex
- [x] eps-ind-a — cycle 5.65, Mdot 0.5, V_ISM 68, standoff ~32 AU (compact)
- [x] Barnard / Fomalhaut / TRAPPIST-1 — Barnard done (limits, no cycle row → restored in a3be380); Fomalhaut / TRAPPIST-1 skipped (no wind/cycle data → no section)
- [x] ko mirrors + build_site HTML + check.sh

## Gates
- [x] check.sh 6/6
- [x] memory updated (synthesis section started)

Done in d27f69e (spec ②) + 27decd7 (per-host ①) + a3be380 (notation rule).
Deferred to the next track: X-ray/flare sweep (radiation_surface confidence),
kerbalism-cfg writer, heliotail Harmony plugin.
