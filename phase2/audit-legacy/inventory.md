# Phase 2/3 full inventory + status (2026-05-30)

Curated Phase 2/3 universe = 17 stellar systems (the only hosts with real multi-category
Phase 2; the other 125 stellar_props_curated entries are mass/radius auto-fill stubs, and
~110 planets_curated hosts are Phase 1 NASA-archive auto-fill — not Phase 2/3 work).

Legend: ✅ built/verified this session (clean by construction) · 🔍 legacy, audited this
session · ⬜ not yet audited.

| System | P2 stellar | P3 stellar | P3 planets | class |
|---|---|---|---|---|
| Barnard's Star | ✅ 8/8 | ✅ | — | this session (Tier 1 b2) |
| Teegarden's Star | ✅ 8/8 | ✅ | — | this session (Tier 1 b2) |
| Vega | ✅ 7/8 | ✅ | — (no planets) | this session (Tier 1) |
| Fomalhaut | ✅ 6/8 | ✅ | — | this session (Tier 1) |
| Delta Pavonis | ✅ 7/8 | ✅ | — | this session (Tier 1) |
| 40 Eridani A | ✅ 8/8 | ✅ | — | this session (Tier 3) |
| 40 Eridani B | ✅ 5/8 | ✅ | — | this session (Tier 3) |
| 40 Eridani C | ✅ 6/8 | ✅ | — | this session (Tier 3) |
| eps Eri | ✅ 8/8 | ✅ | 🔍 b | mixed: stellar this-session / planet audited |
| tau Cet | ✅ 8/8 | ✅ | 🔍 f,g,h (e=FP, archived) | mixed |
| AU Mic | ✅ 8/8 | ✅ | 🔍 b,c,d,e | mixed |
| HD 69830 | ✅ 8/8 (+Tier 2 P_rot) | ✅ | 🔍 b,c,d | mixed |
| 61 Vir | ✅ 8/8 | ✅ | 🔍 b,c,d | mixed |
| TRAPPIST-1 | 🔍 8/8 | — (no stellar P3 doc) | 🔍 b–h | legacy, audited |
| Alpha Centauri A | 🔍 8/8 | 🔍 | — | legacy, audited |
| Alpha Centauri B | 🔍 8/8 | 🔍 | — | legacy, audited |
| Proxima Cen | 🔍 8/8 | 🔍 | 🔍 b,d (c correctly absent) | legacy, audited |

**⬜ not yet audited: NONE.** Every curated Phase 2/3 body is either this-session-built or
audited this session.

**Audit issue status** (all audited systems have findings — see findings.md):
- TRAPPIST-1: 6 issues (densities d/c, b T_eq, metallicity attribution, +uncached stellar)
- Alpha Cen A/B: masses→Kervella2016 misattr, DB age drift, B fabricated Teff, desyncs
- Proxima: SM25 bibcode, activity −4.0 vs −5.55, stellar desyncs
- AU Mic planets: stale stellar values, Plavchan arXiv, scale-height arithmetic, ghost cites
- 61 Vir planets: Phase 2 CLEAN; Phase 3 fabricated arXiv (Bolmont/Howe), Vinson misattr
- HD 69830 planets: Atri+Mogan fabricated author, Atri misattr, Madhusudhan year, Hut calc
- tau Cet planets: stale stellar, Tomasko/Güdel fabricated, MacGregor→Lawler, arithmetic
- eps Eri b: ALL papers uncached, mass label+gravity errors, stale stellar (worst)

This-session-built systems are clean by construction (value-checked during build + disk audit).
