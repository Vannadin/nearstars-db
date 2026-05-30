<!-- 시각 다양성 배치 1 — 6개 Phase-1 시스템을 Phase 2 격상 + Phase 3 시각 합성 + 위성/논쟁바디 추가 -->
# Visual-richness batch 1 — checklist

6 already-in-DB (Phase 1) systems escalated to in-game-implementation depth
(Phase 2 stellar + planet curation → Phase 3 visual synthesis), under the
gameplay-variety policy: add moons, include mild-dispute bodies, exclude only
the genuinely-nothing-there cases.

Systems (distance, visual hook):
- **YZ Cet** (12.1 ly) — first exoplanet radio aurora + flare M dwarf + tight 3 rocky
- **eps Ind A** (11.9 ly) — JWST-imaged cold super-Jupiter + brown-dwarf pair (eps Ind B)
- **GJ 9066** (14.6 ly) — Saturn-class RV (M sin i, Feng 2020) — kept per richness policy
- **GJ 896 A** (20.4 ly) — astrometric ~2.3 MJ giant (Curiel 2022); M+M binary
- **HD 219134** (21.3 ly) — 6 planets incl. transiting rocky; bright K dwarf
- **55 Cnc** (41 ly) — lava super-Earth e + cold giant d (ring) + 5 planets; K0+M binary

## Per-system (each: pre-research → Phase 2 → Phase 3 → moons)

### YZ Cet
- [ ] Pre-research: Gaia DR3 id, parallax, structure confirmed (in DB?)
- [ ] Phase 2 stellar: teff/R/L/mass/age + rotation + activity (M flare star)
- [ ] Phase 2 planets: b, c, d (confirmed) + any disputed/extra
- [ ] Phase 3 visual: stellar color/flare, aurora (star-planet B-field), rocky tints
- [ ] Moons (cfg/downstream, artistic): n/a small rocky — likely none

### eps Ind A
- [ ] Pre-research: A vs brown-dwarf pair eps Ind B (Ba+Bb) — scope decision
- [ ] Phase 2 stellar (K5V) + planet b (RV mass Feng 2019 / JWST Matthews 2024)
- [ ] Phase 3 visual: cold super-Jupiter color/atmosphere, ring (artistic flag), BD pair
- [ ] Moons (cold giant → icy moons candidate)

### GJ 9066
- [ ] Pre-research + verify signal robustness (Feng 2020 RV, M sin i)
- [ ] Phase 2 stellar (M4.5V) + planet c
- [ ] Phase 3 visual: warm Saturn-class, eccentric
- [ ] Moons

### GJ 896 A
- [ ] Pre-research: binary GJ 896 A+B mutual orbit (binary_orbits.json)
- [ ] Phase 2 stellar (M3.5Ve) + planet b (Curiel 2022 astrometry)
- [ ] Phase 3 visual: warm giant + active M; companion B
- [ ] Moons

### HD 219134
- [ ] Pre-research (K3V, 6 planets) — confirm full inventory + disputed
- [ ] Phase 2 stellar + planets b,c (transiting rocky),d,e,f,g,h
- [ ] Phase 3 visual: rocky tints, transiting pair, cold Saturn h
- [ ] Moons (cold Saturn h)

### 55 Cnc
- [ ] Pre-research: 55 Cnc A (K0IV-V) + B (M dwarf companion) binary
- [ ] Phase 2 stellar + planets e (lava),b,c,f,d (cold giant)
- [ ] Phase 3 visual: lava e (glow), cold giant d (ring artistic), warm giants
- [ ] Moons (cold giant d → moons)

## Gate (run on main after each system)
- [ ] `build_systems.py` + `validate.py` FAIL=0
- [ ] `check.sh` green (canonical, schema, mirror parity, dead-link)
- [ ] Phase 3 en+ko block parity + HTML rebuild
- [ ] semantic commit per system
