<!-- Phase 3 항성풍 합성 작업 체크리스트 -->
# Stellar-wind synthesis checklist

## ② Field spec (mod-grounded-fields.md)
- [ ] New section "Kerbalism stellar wind / astrosphere fields (star body)"
- [ ] Field table (radiation_surface, solar_cycle, astrosphere_standoff, apex RA/Dec, V_ISM, wind speed)
- [ ] Sun anchor row + derivation formulas
- [ ] Source priority list
- [ ] Plugin-only note for apex direction
- [ ] Cross-link to project-nearstars-stellar-wind-kerbalism + flux-tube-plugin

## ① Per-star Decisions (docs/phase3/<host>.md + ko + HTML)
- [ ] alpha-centauri-a — cycle 19.1 (tentative), Mdot 2, V_ISM 25, standoff ~176 AU, apex
- [ ] alpha-centauri-b — cycle 8.84, shares αCen astrosphere
- [ ] proxima-cen — cycle 7, Mdot<0.2, standoff <56 AU (limit), radiation_surface HIGH (flares)
- [ ] tau-cet — Mdot<0.1, no cycle (flat), standoff upper bound
- [ ] 40-eridani-a — cycle 8.70, no Mdot (astrosphere from astrometry/activity), apex
- [ ] eps-ind-a — cycle 5.65, Mdot 0.5, V_ISM 68, standoff ~32 AU (compact)
- [ ] Barnard / Fomalhaut / TRAPPIST-1 — minimal (limits / A-type / model), as applicable
- [ ] ko mirrors + build_site HTML + check.sh

## Gates
- [ ] check.sh 6/6
- [ ] memory updated (synthesis section started)
