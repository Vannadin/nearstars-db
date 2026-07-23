# Belt SDF fit — checklist

Goal: make the wiki "physical" belt renders actually match the real belt
physics, by numerically fitting Kerbalism's exact SDF parameters to
dipole L-shell target regions (instead of the previous hand-eyeballed
torus placement). Deliverable = visualization (wiki PNGs + doc), NOT cfg emit.

- [x] Working trio (this dir) created
- [x] `scripts/viz/fit_belts.py`: dipole-shell / slab target regions + IoU fitter
      over (dist, radius, deform_xy, border_dist, border_radius, border_deform_xy)
- [x] Verify fitter on Earth inner belt (sanity: IoU > ~0.8, crescent shape) — 0.976
- [x] Fit all belts: Earth (inner/outer), Jupiter (inner/disc), Saturn (outer),
      Uranus (inner/outer), Neptune (inner/outer), Ganymede (single) — IoU ≥ .96
      everywhere except jupiter_disc .87 (torus-vs-slab ceiling)
- [x] Pause params re-derived with correct comp semantics (nose = radius/comp)
- [x] Update `render_belts_bodies.py` phys entries with fitted params
- [x] BONUS: stock entries were wrong too — corrected to verified KSP-RO/ROKerbalism
      cfg (Uranus/Neptune = generic saturn model 7/7, Saturn 7/7, Mercury tilt 6°)
- [x] Re-render wiki PNGs, eyeball against target overlays
- [x] Correct the doc's misread stock-vs-physical deltas
      (Earth outer belt position, pause_radius vs nose) — en done; ko delegated
- [x] ko mirrors synced (agent)
- [x] check.sh green
- [x] Wiki updated: 14 PNGs + Radiation-Belts en/ko page text (owner-approved push,
      wiki commit f7ca508; old single earth.png superseded by stock/phys pair)
