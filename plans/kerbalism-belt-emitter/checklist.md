# Kerbalism radiation cfg emitter — checklist

Goal: emit Kerbalism RadiationModel/RadiationBody cfg from the fitted belt
geometry (plans/belt-sdf-fit). First output = the 7 solar-system bodies
(owner will propose these upstream to the devs); the emitter itself is
general so NearStars fictional bodies can feed it later.

- [x] Working trio (this dir)
- [x] `scripts/pipeline/emit_kerbalism_radiation.py` — consumes the phys
      entries of `render_belts_bodies.BODIES` (single source of truth),
      emits `dist/NearStars-Configs/Patches/Kerbalism/NearStars-SolarSystemRadiation.cfg`
      (330 lines, 7 bodies)
- [x] Per-body geomagnetic pole lat/lon table with citations (polarity is
      not encoded in the meridian renders — explicit here)
- [x] Intensity policy: physical values (owner decision 2026-07-24),
      conf-low regime calls flagged in comments
- [x] All citations emitted as clickable ADS URLs (owner rule 2026-07-24,
      saved to memory as standing preference)
- [x] Round-trip check: re-parse emitted cfg, compare to BODIES phys — OK
- [x] tools.md index §14 (+ ko mirror)
- [x] Wiki "The physical cfg" section (en+ko, parallel agent)
- [x] check.sh green, commit
