# Belt SDF fit — context notes

## Why this exists (2026-07-24)

Owner: the previous session's research (solar-system-radiation-belts.md) was
good, but the *implementation* of the physics into Kerbalism's radiation-belt
representation was poor. Scope correction from owner mid-session: the
deliverable is **visualization** (the wiki stock-vs-physical renders), not cfg
emit.

## Root cause found (2026-07-24)

The previous session hand-placed torus parameters by copying paper numbers
directly into `dist`/`radius`, **misreading the SDF semantics**:

1. `inner_dist`/`outer_dist` live in deform_xy-squashed coordinates. Real
   equatorial extent is `(dist ± radius)/sqrt(deform_xy)`. Stock Earth outer
   (dist 2.6338, rad 2.48, dxy 0.7225, border 1.4412/1.4875/0.7225) actually
   spans **3.45–6.0 R_E at the equator** — close to the physical L 3–7 — while
   the doc claimed "centred ~2.6 R_E, inward of the real heart at L 4–5".
2. `pause_radius` is not the sub-solar standoff: dayside x is multiplied by
   `pause_compression` before the sphere test, so **nose = radius/comp**.
   Stock Earth (15, comp 1.5) → nose exactly 10 R_E, flank 15 (= Shue α 0.585).
   The doc's "stock 15 vs physical ~10" delta is wrong, and the hand-made
   "physical" render (rad 10, comp 1.5) actually put the nose at 6.7 R_E.
3. No fit-quality check existed at all — nothing compared the SDF region
   against the dipole-shell crescent it was supposed to represent.

## Approach

- Target regions in the meridian half-plane (body radii, dipole frame):
  dipole drift shell `{ L1 ≤ r³/ρ² ≤ L2, r ≥ r_cut }` (crescent with
  loss-cone cut); Jupiter magnetodisc = equatorial slab `{ρ1≤ρ≤ρ2, |y|≤h}`.
  Tilt/offset are exact cfg passthroughs (geomagnetic_pole_lat/offset) —
  fitting happens in the untilted dipole frame.
- Fit Kerbalism's exact torus−border SDF (reproduced from Radiation.cs,
  Unlicense) with Nelder-Mead multi-start, loss = 1 − IoU on a quarter-plane
  grid (region symmetric in y).
- comp/ext (day-night asymmetry) are NOT fitted — kept as mild hand values;
  the meridian target is axisymmetric.
- Belt L-ranges come from the ADS anchors already pinned in
  solar-system-radiation-belts.md. Where the doc only anchors a peak
  (Uranus/Neptune), the L-range keeps the previous session's reading; the fit
  fixes the *shape*, not the anchor.
- radiation_* intensities and gradients: unchanged (regime calls, out of scope).

## Second root cause: the "stock" renders were wrong too (2026-07-24)

Re-fetched the actual shipped cfgs (KSP-RO/ROKerbalism `System/Radiation.cfg` +
`Support/RSS.cfg`) instead of trusting the doc's "RSS anchor" columns:

- **Uranus and Neptune use the generic `saturn` RadiationModel** (single outer 7/7
  belt, pause 20/1.02/0.1) — the previous stock renders drew Earth-style two-belt
  shapes for them, which exist nowhere in the cfg. Their `radiation_inner` values
  (75 / 39) are dead cfg: the model has `has_inner = false`.
- Saturn's stock outer belt is 7/7 (equator 0–14 R_S), not the 4.5/3.0 the previous
  render used; stock Neptune's pause is 20 (shared model), not 26.5 as the doc claimed.
- Mercury stock: pole_lat 96 → tilt 6°; nose = 1.6/1.4 = 1.14 R_M (tight vs physical
  1.45, not "generous").
- RSS renames Jool→Jupiter via `+RadiationBody[Jool] { @name = Jupiter }`, so RSS
  Jupiter = the `jupiter` model (6/1, 6.5/6.5, 300/50) — the doc's stock column was
  right; the standalone `Jupiter`/jupiter2 entry (3/1, 150) is the non-RSS fallback.

## Fit results (2026-07-24, fit_belts.py)

IoU: earth_inner .976, earth_outer .980, jupiter_inner .978, jupiter_disc .874
(torus-vs-slab ceiling; lens shape arguably closer to a real tapered disc),
saturn_outer .981, uranus_inner .972, uranus_outer .980, neptune_inner .980,
neptune_outer .970, ganymede_belt .964. uranus_outer ≡ earth_outer (same L 3–7
target) — expected, the fit is deterministic in the target.

## Owner review round (2026-07-24, post-push)

- Owner caught the Earth inner belt hugging the surface in the physical render.
  Root cause: target rcut 1.02 was "top of atmosphere", but the real inner-belt
  lower boundary is ~1000 km altitude (loss-cone depletion below; the SAA dip to
  ~200 km is the offset-dipole effect, which geomagnetic_offset already carries).
  Refit with rcut 1.157 → IoU 0.994, D-cut face lands at the 1000 km boundary.
  Notably stock's D-cut (equator 1.29 R_E) had respected this gap all along.
- That correctly shook confidence in the other assumed target params. Triage:
  anchor-pinned = Earth L-windows/slot, Saturn 2.3–6, Neptune peak L7 + Triton
  cut 14, Jupiter inner peak. Assumed = all other low-altitude cuts (1.03/1.05),
  Uranus L-windows (inherited from prev session; the "4.19 R_U" doc anchor is a
  magnetometer reading, not a belt), Neptune inner window, Jupiter disc slab
  numbers. Ganymede rcut 1.02 corrected to 1.0 immediately (airless — surface
  absorbs). Literature verification of the rest delegated to a solo ADS agent;
  wiki push held until the audit lands.

## ADS audit of all target params (2026-07-24, solo agent)

Verdicts on the 7 open items: 5 supported with firmer grounding, 2 adjusted.
- **Uranus corrected** (the one real error): the L=3 split was arbitrary and the
  "413 nT @ 4.19 R_U" doc anchor was a magnetometer reading, not a belt. Real
  structural boundaries are the moon L-shells — Krimigis 1986 "except inside the
  orbit of Miranda" + Cheng 1987 (1987JGR....9215315C, newly pinned) electron
  minima at Miranda/Ariel/Umbriel L 5.1/7.5/10.4 with broad maxima between.
  New windows: inner L 1.5–5 (inside Miranda), outer L 5–10 (Miranda→Umbriel);
  trapping detectable to Titania ~L 17. Refit IoU .98/.97.
- **Jupiter disc** half-thickness 2.5 → 3.0 R_J (Khurana canonical ~3–3.5);
  radial 3–16 documented as a frame truncation (real disc extends past 50 R_J).
- Supported: Jupiter inner (D&G continuous to atmosphere; synchrotron pin not
  found via ADS abstracts — grounded through D&G/Santos-Costa, conf medium),
  Saturn horns (bounce population fills field lines — a latitude bound would be
  wrong), Neptune windows (Proteus L 4.75 divider; Triton 14.4), Earth outer
  rcut 1.05 (outer electrons precipitate into the loss cone at low altitude —
  Liu 2024, 2024JGRA..12932171L, newly pinned), Ganymede L 1.1–1.9 with
  rcut 1.0 (airless, surface-absorbed; refit IoU .967).
- Paper cache relocated to canonical docs/phase3/_papers/ (agent had created a
  root _papers/ by mistake — my prompt's fault).

## Decisions

- Working dir under `plans/` (not phase2/): viz tooling, not curation.
- Wiki PNGs stay clean (no target overlay); fit diagnostics (target-outline
  overlays, IoU numbers) go to scratchpad + IoU noted in the doc.
- Kerbalism source re-fetched from GitHub master to scratchpad to confirm SDF
  semantics (Radiation.cs lines 60–125: Inner_func/Outer_func/Pause_func;
  Gsm_space line 422: coords in body radii, offset along magnetic axis;
  RadiationInBelt line 849: dose = clamp(grad·(−D)/radius, 0, 1)).
