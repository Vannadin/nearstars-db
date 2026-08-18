# Kerbalism radiation cfg emitter — context notes

## 2026-07-24 — opened

- Owner green-lit this emit ahead of the project-end emit batch (their own
  earlier deferral, their call to move now). Scope: radiation belts only.
- Owner decisions this session: intensities = **physical values** (option 1);
  "the main consumers will be the exoplanet bodies later — for the solar-system
  cfg I will propose it to the devs upstream." → the patch doubles as an
  upstream proposal: heavy provenance comments (bibcodes, fit IoU), clean
  standalone RadiationModel definitions + @RadiationBody rebinds.
- Single source of truth: the `*_phys` entries in
  `scripts/viz/render_belts_bodies.py` (fit output already lives there for the
  renders). The emitter imports that dict — no second copy of the numbers.
- Gradients (3.3/2.2) equal Kerbalism defaults (Radiation.cs ctor
  radiation_inner_gradient 3.3 / outer 2.2) → not emitted.
- Geomagnetic pole lat/lon cannot come from the render dict (meridian slices
  don't encode polarity/longitude) → explicit cited table in the emitter:
  Earth 80.37/-72.62 (IGRF, stock), Jupiter -80/0 (JRM33, reversed),
  Saturn 90 (Cao 2020 <0.007 deg), Uranus 31.4 (Ness 1986), Neptune 43
  (Ness 1989), Mercury 90 (Anderson 2012 tilt <0.8 deg; the 0.2 R_M north
  offset carries the asymmetry), Ganymede -86 (Kivelson 2002 tilt ~176 deg).
- MM mechanics: new RadiationModel nodes are plain (Kerbalism reads them all);
  rebinds are `@RadiationBody[Name]:NEEDS[RealSolarSystem]:AFTER[KerbalismConfig]`
  (must run after ROK's own Support/RSS.cfg body renames/copies). `%` used for
  fields absent on some stock bodies (Ganymede geomagnetics, its radiation_pause).
- dist/ is gitignored (repo convention) — the emitter is the committed artifact,
  the cfg is generated output.

## 2026-07-24 — NearStars-body extension

- Owner choices: Polyphemus outer belt = L 4.2–10 (Cassandra 8.4 submerged →
  "intermediate"); intensities re-derived from the methodology rather than
  picked from presets; Pandora = refit shape only (values preserved).
- Methodology upgraded first: Part B gained the **saturated-regime calibration**
  (Mauk & Fox 2010, [`2010JGRA..11512220M`](https://ui.adsabs.harvard.edu/abs/2010JGRA..11512220M), verified via ADS + cached) — two-anchor
  B² interpolation between Earth (31 µT → 10.4 rad/h) and Jupiter (428 µT →
  ~1500). Polyphemus 170 µT → 313 → 300 rad/h inner; outer = 0.1× (torus-driven
  Jupiter ratio) = 30. The board row cites the methodology doc per the
  refs-provenance rule, and Mauk & Fox lives in the doc, not the row.
- Board rows (alpha_centauri, validator 0 errors): new Polyphemus
  magnetism.radiation_belts row (gated, methodology-derived; structure pinned by
  canon moon L-shells — inner L 1.3–3.0 with peak at Hades 2.07, slot 3.0–4.2
  around Pandora 3.53, fit IoU .97/.97); Pandora row superseded + refit
  replacement (L 1.15–2.2, IoU .98; pause re-encoded nose 2.6 = 2.99/1.15).
  Both rows carry **individual cfg-named fields** (inner_dist … radiation_inner)
  — the packed radiation_model string format is retired.
- Emitter: `load_nearstars_specs()` parses gated radiation_belts rows from all
  phase4 boards → `dist/.../Kerbalism/NearStars-Radiation.cfg` (RadiationModel +
  RadiationBody per body, NEEDS[NearStarsSystem], refs as comments). Errors out
  loudly on legacy packed rows.
- Viewer builder now imports load_nearstars_specs — the Pandora/Polyphemus
  presets come from the gated board (same single source as the emitter); the
  hand-carried artifact sketch values are gone.

## 2026-07-24 — owner challenge: replace the B² interpolation with the exact recipe

Owner: "단순 보간으로 계산한거야? 방법론 규율대로 정확한 값을 구하는 법을 조사해줘."
Mode A methodology upgrade, three research legs (solo Opus agents):

1. **K–P formula recovered exactly** — not from the paywalled papers but from
   Mauk & Fox's own open Zenodo software ([`2021zndo...4782323M`](https://ui.adsabs.harvard.edu/abs/2021zndo...4782323M), doi
   10.5281/zenodo.4782323): the flexible spectral shape, Summers 2009 A4–A8
   relativistic resonance, A1/A2 growth integrals, and the marginal-stability
   condition CmCk = L·Rp·wi/(3·vg) with wave gain 3 (independently confirmed by
   Mourenas 2024, [`2024JGRA..12932193M`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932193M)). Cached: mauk_fox_KP.nb + rendered run
   (validation targets: wi=0.658455, CmCk peak 0.608 for Earth L=5) +
   kennel_petschek_recipe.md. Key scaling finding: the limit's controlling
   variable is We/wpe ∝ B/√n_cold + spectral/pitch indices — **NOT B²**.
2. **Flux→dose leg (the reframing)** — no single quotable per-intensity factor
   exists in ADS abstracts; the standard method is SHIELDOSE-2 (Seltzer
   [`1979ITNS...26.4896S`](https://ui.adsabs.harvard.edu/abs/1979ITNS...26.4896S), [`1992STIN...9315580S`](https://ui.adsabs.harvard.edu/abs/1992STIN...9315580S)). Load-bearing physics: Mauk & Fox
   show Earth/Jupiter/Uranus sit at COMPARABLE differential K–P caps near
   1 MeV, yet doses differ by orders — **dose contrast is driven by spectral
   hardness (the tail above the ~2 mm-Al transmission cutoff; 1 MeV e⁻ CSDA
   range ≈ 2.0 mm Al) and belt size, not the 1 MeV value**. Textbook free-field
   factor 2.3e-8 rad(Si)/(e·cm⁻²) at 1 MeV, de-rated ~10× behind ~2.5 mm Al.
   Recommendation adopted: anchor-ratio calibration (game Earth 10.4 rad/h)
   with the hardness factor made explicit, not a naked 1-MeV ratio.
3. **Python port** of the Zenodo notebook → scripts/refs/kp_limit.py
   (agent running; validates against the notebook's printed intermediates).

Implication for the methodology: the B² two-anchor interpolation empirically
bundled (KP plateau ratio ≈ O(1)) × (hardness factor) × (shield transport);
the upgrade decomposes it into stated factors with the KP plateau computed
exactly. The Polyphemus rad/h remains a calibrated regime call, but each
factor is now mechanistic and pinned.

## 2026-07-24 — validation gap closed (owner-downloaded PDFs)

- The three paywalled-to-bots papers are free (AGU 24-month archive); owner
  downloaded them and they now live in docs/phase3/_papers/ (gitignored):
  mauk_fox_2010_electron_belts.pdf, summers_tang_thorne_2009_kp_limit.pdf,
  summers_2014_limiting_spectrum.pdf.
- Summers 2009 Appendix A settled the reconstructed normalisations: norm1 is
  EXACTLY the A2 prefactor pi*me*(wr-We)/(N0*kr) (the fitted 3.1582 was pi to
  0.5%, drift = the relativistic gamma_R in the reconstructed pR0), norm2 is
  exactly the A3 prefactor. With the exact forms the Earth L=5 anchors match
  to ~1e-6/1e-7 (printed-digit exact) — the single-anchor-coefficient caveat
  in kp_limit.py is retired.
- Mauk & Fox Table 1 (per-planet spectra) + per-figure B/N/D extracted; the
  module self-test now validates all five planets at figure level: Earth L=4
  0.28 (below) / L=5 0.6079 (exact) / L=6 1.46 (near), Uranus 1.11 (at),
  Jupiter L=8.3 D=3 0.68 (near), Neptune peak 0.91 with 1 MeV factor 27.8
  below (paper: ~30). Their Jupiter L=3 ">=20x below KP" statement also
  directly confirms our "deep strong-field inner belts are not K-P-bound"
  regime call. B_nT direct-field + D override params added for these cases.

## 2026-08-17 — the viewer read the pause nose/tail as if smooth were 0

Every number the belt viewer derived from the pause used the stock closed
forms `pause_radius / pause_compression` (nose) and `pause_radius /
pause_extension` (tail). Those hold only when `pause_smooth = 0`. With
smoothing on, the raster/shader drew the right surface (both evaluate the
generalized SDF) while the Shue overlay anchor, the scene-extent autoscale,
the tail-vs-orbit legend and the Shue-native cfg back-computation all quoted
a body that does not exist. Proxima Cen b read nose 1.345 R_p where the board
gates 1.25, Pandora 3.64 R_moon against a gated 3.3857, Mercury 2.98 R_M
against Winslow's 1.45 — the smoothed sets themselves were fine, only the
read-back was wrong.

Closed form, from solving |px| = pause_radius on the axis:

    A = (comp+ext)/2,  B = |comp-ext|/2,  u = (A*rad -/+ B*sqrt(rad^2 + comp*ext*smooth^2)) / (comp*ext)

nose = u_minus + waist, tail = u_plus - waist. The discriminant collapses to
B^2 (rad^2 + comp*ext*smooth^2), so no iteration is needed, and at smooth = 0
it reduces exactly to the two stock divisions. `pauseNoseTail()` is now the
single source for all four call sites; a headless pass bisects the SDF for
every preset (both the base and the applied ⚗ plugin set) and matches to
1e-3, with all smooth = 0 presets bit-identical to the old output.

waist was already carried correctly (it translates the whole surface, so it
is added after u is solved, + on the nose and - on the tail) — it needed no
change beyond travelling through the new helper.

The Shue-native `pause_alpha` back-computation was the one place the fix is
not purely mechanical: methodology Part C maps alpha = log2(compression), but
the generalized form retires compression to 1.0 and log2(1) = 0. It now feeds
the shape's effective compression rad/u_nose, which reproduces the gated stock
compression exactly where both exist (Proxima Cen b: 1.43/1.2507 = 1.1434 vs
gated 1.144) and reduces to log2(comp) when smooth = waist = 0.

## 2026-08-18 — the gated smooth set is now the viewer's default shape

Owner report: "the smooth value reads 0 for everything I click." It did. Of
the 32 presets, 26 carry no smooth at all (their boards took the Shue-native
branch, so 0 is correct there), 2 carry it live in `pause` (Venus, Mars), and
4 parked it in `pending` behind the ⚗ button — Mercury, Ganymede, Pandora,
Proxima Cen b. Clicking any of those four showed the un-smoothed stock shape
with the slider at 0.

The parking came from the emitter: `pause_smooth` sits in PENDING_MODEL_KEYS
because stock Kerbalism cannot consume it, and the viewer inherited that
classification as "hide until the Harmony patch lands". But cfg-emittability
and what the viewer should *draw* are different questions, and the split was
not even self-consistent — Venus and Mars are the same induced branch and
were applied on load, while Proxima Cen b, whose board gates the set with no
`pending: true` flag (unlike Pandora's rows, which say "PLAN, not shipped"),
was hidden behind the button.

Owner's call: apply the set on load for all four, and invert the button to
"revert to stock". Rationale — the gated set is the shape the board decided
on, so it is what the viewer should open with; the stock shape is the
comparison, not the baseline. `deepset` now snapshots the stock values of the
same keys into `state.pauseStock` before overlaying `state.pending`, so the
toggle round-trips exactly (verified headlessly on all four).

One foot-gun this creates: "Copy Kerbalism cfg" now exports the smoothed
`pause_radius`/`compression` by default, and stock Kerbalism ignoring
`pause_smooth` would render a different nose from those same numbers. The
export now prints both — the true nose and the nose the stock engine will
produce — and says to use the board's non-smoothed values for shipping.

Also corrected in the help text: it still defined the overlay's r0 as
`pause_radius/comp`, the identity that yesterday's fix retired.

## 2026-08-18 — literature check on Proxima Cen d's field, and what it does to the belts

Owner asked three things after the belt row was gated: is there research on the
inner/outer contrast, does our own methodology even allow d a dynamo, and what
about the star's field acting on a metal-bearing d. All three landed on the same
place, so they are recorded together.

**Our own ladder gives d no magnetosphere at all.** RM22 (rocky-planet dynamo
methodology) on the gated inputs: M 0.3 M_E, R 0.72 R_E, density 0.804 rho_E, tidally
locked at 5.122 d, star ~5 Gyr. That density sits on the boundary of the doc's
regime 5 (low-density dry, Mars-analog, "likely dynamo-dead by a few Gyr, M = 0").
Taking the generous branch instead (alive, dry rocky class 1) and interpolating the
base moment between the Mercury and Earth anchors gives M_base 0.039 M_E; the
tidal-lock multipolar penalty (x0.06) leaves M 0.0023 M_E, i.e. B_eq 0.19 uT,
B_pol 0.38 uT. The board gates 16 G polar. The ratio is 4.3e6.

Fed through the same Chapman-Ferraro expression the board's standoff row uses
(f = 2, ram 5648 nPa):

| reading | B_pol | nose |
|---|---|---|
| RM22 ladder | 0.00038 G | 0.46 R_p (no magnetosphere; the wind reaches the ground) |
| paper's low end | 3 G | 4.30 R_p |
| gated (SPI median) | 16 G | 7.52 R_p |

So the board's note that "the 3 G low end is the theory-consistent one" does not
hold: 3 G is itself ~1e6 x the ladder. The honest statement is that the SPI field
and our dynamo methodology do not overlap at any point of the quoted range.

**The source paper is weaker on the field than the board reads it.** Zapatero
Osorio 2026 (2605.22925) sec 5.2, read in full: their Lanza 2012 / Saur 2013 /
Kavanagh 2022 formalisms (via Ilin 2024) require B_p ~1e3-1e4 G, which the authors
themselves reject as "physically implausible" since it exceeds the stellar surface
field and giant-exoplanet estimates (Cauley 2019). The 16.4 G survives only in
Lanza 2013's flux-tube Poynting formalism, and only with a chosen intermediate
geometry s = 2.5, a 600 G stellar field, a mean flare luminosity of 1e25 erg/s, and
a Mars radius; they state it is "about half as large if Proxima d has an Earth-size
radius", and our gated radius is 0.72 R_E, between the two. Crucially they also
compute the unmagnetized case: 1e24 erg/s in stretch-and-brake against an observed
6.5e24-4e26, i.e. short by ~6.5x at the low end, not excluded.

**The owner's induction idea is a real published branch, with a decisive caveat.**
Laine & Lin 2012 (2012ApJ...745....2L) treat close-in super-Earths as unipolar
inductors: a rocky planet is more conductive than the stellar envelope, the flux
tube slips, and the induced EMF drives an Io-Jupiter style DC current whose ohmic
dissipation makes stellar hot spots and heats the planet, with no planetary dynamo
required. But Lai 2012 (2012ApJ...757L...3L, 126 cit) puts an upper limit on that
circuit: too little resistance twists the flux tube until the circuit breaks, and
applying the limit, "for exoplanetary systems containing close-in Jupiters or
super-Earths, the magnetic torque and energy dissipation induced by the orbital
motion are negligible, except possibly during the early T Tauri phase, when the
stellar magnetic field is stronger than 1e3 G". Proxima is ~5 Gyr old with a
200 G large-scale field (Klein 2021; 600 G adopted by the SPI paper), so the pure
unipolar branch is negligible for d today by that criterion.

The related induction-heating literature (Kislyakova 2017 2017NatAs...1..878K
TRAPPIST-1 magma oceans; Kislyakova 2018 2018ApJ...858..105K around strongly
magnetized stars; Chyba 2021 2021Icar..36014360C analytic formulae) is a different
effect: it heats the interior, it does not build a magnetosphere. And the
conducting-interior induced-field template (Zimmer, Khurana & Kivelson 2000
2000Icar..147..329Z; Kivelson 2000 2000Sci...289.1340K) needs a conducting shell
in a time-varying external field, which for an airless bare rock is the deep
interior rather than an ionosphere.

**Why this decides the belt row.** An induced magnetosphere has no closed dipolar
field lines, which is exactly why Venus and Mars carry no belts on this project's
own boards. So the induction reading does not give d weaker belts, it gives it
none, and the RM22 ladder does not give it belts either since the boundary never
clears the surface. The gated belt row is correct given 16 G and wrong under either
alternative; it is not a value that can be tuned between them.

**On the inner/outer contrast (the caveat left open when the row was gated) there
is now an observational anchor.** Kao 2023 (2023Natur.619..272K, Nature 619, 272)
resolved a radiation belt around the ultracool dwarf LSR J1835+3259 at 8.4 GHz: a
double-lobed, axisymmetric structure "similar in morphology to the Jovian radiation
belts", lobes separated by up to 18 dwarf radii (so ~9 R each), 15 MeV electrons.
Climent 2023 (2023Sci...381.1120C) reports the same for a brown dwarf. Both are
Jupiter-shaped, a torus standing well off the body, rather than Earth-shaped with
the peak deep. That favours the outer shell carrying the peak, against the
Earth-anchored inner > outer split the Part B recipe hands down. Not applied: the
recipe change belongs in the methodology first, and the prior question is whether
d has belts at all.

## 2026-08-18 — owner kept the 16 G field, and the peak moved outward

Owner's call on the three readings: keep 16 G, and make it more interesting. That
settles the field question by adoption rather than by agreement, so two things
followed.

First the honesty side. The magnetic_field row's evidence claimed the bottom of the
published range, ~3 G, was the theory-consistent end. It is not: 3 G is still about
a million times what our rocky-dynamo ladder returns for this body, and the ladder's
own answer (0.38 uT polar) would put the boundary at 0.46 R_d, inside the planet, so
no magnetosphere at all. The row now states that, states that the paper's other
formulations need 1000-10000 G and are rejected by its own authors as implausible,
and states plainly that the adoption is an owner call for the more interesting body
rather than a point where the two lines of evidence meet. The dynamo methodology is
now cited alongside the SPI paper on that row.

Then the interesting side, which the Kao 2023 anchor had already set up. The Part B
recipe hands down an intensity scale and an outer/inner ratio, and both of its
anchors put the peak in the deep shell. That is an Earth artefact: Earth's inner
belt is CRAND-fed, cosmic rays hitting *air*, and a bare rock has no such source,
while wind- and diffusion-fed populations are injected at the outer boundary and
peak at intermediate L. The only resolved extrasolar belt agrees. So Part B gains a
rule (the peak belongs to the outer shell on airless bodies, the deep shell takes
the ratio; the scale is unchanged) and d's two intensities swapped: inner 1000,
outer 5000.

The resulting equatorial profile is worth recording, because it is now a structure
rather than a ramp:

| r (R_p) | dose (rad/h) |
|---|---|
| 1.0 | 7 |
| 1.5-1.75 | 1000 |
| 2.5 | 256 |
| 3.5-3.75 | 5000 |
| 5.0 and out | 0 (inside the pause, shielded) |

Two quiet corridors, one hugging the surface and one at the 2.5 R_p shell junction,
separated by hazard bands, with the killing torus at 3-4.5. The section render shows
the double-lobed morphology Kao imaged. Nobody has to fly the same altitude twice.

Not touched: the environment and gameplay narratives, which still read true (the
belts are still there and orbiting is still not free) and are owner-approved prose.
If the corridor structure is worth calling out to the player, that is a gameplay-row
edit for the owner to make.

## 2026-08-18 — the touching shells were wrong, and d finally has a magnetic axis

Owner asked whether the two shells sitting flush against each other was right, and
it was not. Each shell's dose ramps from zero at its *own* boundary
(`gradient·(-SDF)/radius`), so two shells that merely meet are both at zero exactly
where they join. The gated arrangement's equatorial profile collapsed to 5 rad/h at
2.5 R_p between flanks of 1000 and 5000 — a thousandfold notch that no source-loss
balance puts there, and an artifact of the engine's per-shell ramp rather than
anything physical.

The engine sums the shells, so overlapping them fills the region from both sides.
Refit to `L` 1.0-3.5 against 2.0-5.0 (IoU 0.988 / 0.977) and dropped both gradients
from 2.15 to their own floors, `*_radius / d_max` = 1.157 and 1.496. The floor is the
right value here rather than merely the legal minimum: its plateau shrinks to a single
point at the shell's deepest interior, giving a profile that peaks at one radius and
ramps linearly away, which is the torus being modelled. Above the floor the shell
grows a flat top instead.

Result, in the shells' own frame: a single peak of 5037 rad/h at 3.45 R_p = 0.46 R_mp,
no interior notch, against Earth's outer belt at 0.40-0.50 R_mp. Both rules are now in
methodology Part B (overlap, not touch; gradients at the floor) since the same trap is
waiting for every future airless body.

Candidates measured before choosing: a single broad shell (`L` 1.0-5.0, IoU 0.986)
also gives a clean single peak but puts it at 0.35 R_mp, and one shell cannot carry
both the torus and an inner floor. The overlap wins on the peak location.

**Magnetic axis, previously not gated at all.** d shipped with no
`geomagnetic_pole_lat`, i.e. a dipole aligned with the spin axis, while Proxima b
carries 60 with a 0.25 offset and every solar body has one. Gated 45 degrees of tilt
and a 0.25 R_p offset, by analogy with the ice giants (Uranus 59 and 0.3, Neptune 47
and 0.55, Mercury 0.198) rather than with Earth. The argument is the anomaly itself:
16 G on a 0.3 M_E slow rotator is far outside what an Earth-style compositional dynamo
produces, and the Solar System's non-Earth dynamo geometries are precisely the ones
that run strong and badly tilted. It is an analogy and the row says so; nothing about
the axis is observed.

Two things it buys. Orbital inclination now matters, since an orbit in the rotational
equator cuts the tilted belt obliquely instead of running down its middle. And the
offset pushes the deep shell into the ground on one hemisphere, so surface dose is
hemispherically asymmetric, which is the structure the surface row's two-tone polar
caps already describe.

## 2026-08-18 — one shell, because the second never earned itself

Owner, after the overlap fix: if overlapping them just sums into one peak, why keep
two? They hand-built a single-shell version in the viewer and reported it looked the
same. Measured, and they were right on both counts.

Their hand config (the fitted outer torus with the border carve opened inward and
gradient 1.2) scores IoU 0.969 against the L 1.0-5.0 dipole shell; fitting one shell to
that range directly gives 0.986, so the fit is kept rather than the hand values. Two
details their version had slightly off, both instructive: gradient 1.2 sits above the
floor 1.005, which grows a flat top (5000 across 2.5-3.0) instead of a single-radius
peak; and their shell reaches down to 0.875 R_p, below the surface, so ground-level dose
reads 428 rad/h against 14 for the fitted shell whose boundary is the surface itself.

The physics also came out better, and the correction is on my earlier reasoning rather
than theirs. I had justified moving the peak outward by Earth's outer-belt fraction,
~0.45 R_mp. That is the wrong target for a slotless body: Earth's outer belt is bounded
*below* by the slot, and the same missing hiss that removes the slot also removes the
dominant inner-zone loss, so an inward-diffusing population survives deeper and keeps
gaining energy as it goes. The peak should sit inside Earth's fraction, and the fitted
single shell puts it at 0.35 R_mp without being told. So the two-shell arrangement was
chasing a number that did not apply.

Final geometry: one shell, L 1.0-5.0, IoU 0.986, gradient at its floor 1.005, peak
5000 rad/h at 2.65 R_p = 0.35 R_mp, ramping to zero at the surface and at 5.01 R_p.
`has_inner` is gone from the cfg. Methodology Part B now says one shell is the default
for airless bodies (the Ganymede treatment) with the overlap rule kept only for the case
of two genuinely distinct source populations, plus the peak-depth argument above.

Renders cleaner too: each lobe is a filled blob with a hot core rather than the crescent
with a dark centre the two-shell version drew.

## 2026-08-18 — "airless means one shell" was over-generalised

Owner asked whether one shell really is the default for airless bodies. It is not, and
the rule as written yesterday generalised from a single case. Two corrections.

**The rule.** What an airless body actually loses is the *hiss-cleared slot*, because
that one needs a plasmasphere. It does not lose the ability to have a gap: Saturn's and
Uranus' gaps are cut by ring and moon sweeping at specific L, and an airless body with
sweeping moons would get the same. Nor was Ganymede ever evidence for the rule, since
its single shell follows from a ~2 R_G standoff leaving room for one shell either way
(Williams 1998), not from any slot argument. And two distinct source populations still
warrant two shells. So the rule is now stated as: **render a gap only when you can name
what carves it**, with one shell as what you get when nothing carves and there is one
population. Same conclusion for Proxima d, arrived at honestly instead of by a rule that
would have mislabelled the next body.

**The CRAND claim was too strong.** "Airless, so no CRAND source" is wrong: a regolith
is also a cosmic-ray target and its albedo neutrons are routinely measured, which is how
orbital neutron spectrometry maps airless surfaces at all (Mercury, Lawrence 2013). What
is missing is any body where that source is known to *build* a trapped belt, and the two
airless magnetized bodies available both fail for unrelated reasons (Mercury cannot trap
at all; Ganymede has room for one shell regardless). So a deep CRAND belt on an airless
body is **possible but unscaled**, not absent, and the board note now says that. d's
single shell still stands, since inventing an unscaled second population is worse than
carrying the whole interpolated scale in one.

Worth noting what this does not change: the peak-depth argument (no hiss removes the
inner-zone loss that bounds Earth's belt from below, so the peak sits inside Earth's
0.45 R_mp fraction) is independent of CRAND and unaffected.

## 2026-08-18 — d's tilt drawn, and c's magnetic axis was being dropped by the emitter

Two things, and the second was a pipeline bug rather than a missing value.

**d's tilt.** Owner asked for a draw in 30-45 rather than the round 45. The band is
what the ice-giant analogy supports; nothing in the evidence picks a point inside it, so
the point is a seeded draw rather than a number chosen to look chosen:
`random.Random('Proxima Cen d dipole tilt 2026-08-18').uniform(30, 45)` = 32.3 deg, i.e.
`geomagnetic_pole_lat` 57.7. The seed string is on the board so the draw reproduces.

**c's axis was gated and never shipped.** Proxima Cen c carries `geomagnetic_pole_lat`
40 and `geomagnetic_offset` 0.4 on its `magnetism.magnetic_field` row, and the emitted
RadiationBody had no geomagnetic line at all. The cause is in `load_nearstars_specs`:
it skips a magnetic_field row that carries no `pause_` field, on the theory that such a
row is descriptive only. But `geomagnetic_*` are BODY_KEYS, i.e. real cfg output, so any
body that put its axis on a descriptive field row lost it silently. The guard now tests
`pause_` **or** a BODY_KEYS field. A scan of every gated board found exactly one row
affected, c's, so nothing else moved.

Worth noting the shape of this bug: the value was gated, visible on the board, visible in
the viewer's pre-regate snapshot, and simply absent downstream. Nothing failed loudly.
The general lesson for the emitter is that "does this row contribute to cfg" should be
asked against the field lists that define cfg output, never against a name prefix.

## 2026-08-18 — sweeping the same bug class, and making it loud

Owner asked whether this will keep happening. It would have. Auditing every gated
magnetism field on every board against the emitter's key lists found two more values in
the same state as c's axis (gated, visible, absent downstream):

- **`pause_alpha_night` 0.52 on both Proxima c and d.** A real Shue-native plugin
  parameter, sibling to `pause_alpha` / `pause_nose` / `pause_tail` which are all in
  PENDING_MODEL_KEYS, and simply missing from that list. It reached neither the emit
  comments nor the viewer's overlay. Added to the list, and `build_belt_viewer` now
  reads it into `view.shue_an` from the board `pending` block, which it had only ever
  done through the Solar-System BODIES dict. Six presets now carry the 2-alpha wake
  form where four did before.
- **`magnetosphere` on Cassandra**, which is narrative and correctly not emitted, but was
  indistinguishable from a dropped value until it was classified.

The structural fix is a fourth list, `DESCRIPTIVE_KEYS`, plus a warning in
`load_nearstars_specs`: any field on a gated magnetism row that lands in none of
MODEL_KEYS / BODY_KEYS / PENDING_MODEL_KEYS / DESCRIPTIVE_KEYS is now printed to stderr
by name and body. It fires in both consumers, the emitter and the viewer build, so a new
field name announces itself the first time anyone builds. It earned itself immediately:
`magnetosphere` was found by the guard, not by the audit that motivated it.

Two other drop paths checked and clean: no gated body carries cfg fields without a
`radiation_model` (which would drop the body entirely), and the six emitted specs match
the six the boards define.

**One coupling remains unguarded.** Five of the six bodies have no `kopernicus_name` and
emit under their board name, so the cfg's `name =` is only correct as long as the board
name equals the in-game body name. Checking that against the DB does not work today,
because Polyphemus, Pandora and Cassandra are fictional and correctly absent from it,
and the boards carry no `fictional` flag to key on. There is nothing to reconcile
against until the Kopernicus writer exists, so the right place to close this is that
writer, and it is written down here rather than guessed at now.

## 2026-08-18 — kopernicus_name applied retroactively, from the bulk row

The one coupling left unguarded yesterday is closed. Every body's cfg name now comes
from a `kopernicus_name` field on its `bulk` row, 24 of them across the seven boards,
and `load_nearstars_specs` reads it there (the old row-level key still works and the
board body key is still the last resort, but neither is reached now).

The name is the **formal designation verbatim**, which settled two questions:

- **Designation, not culture name.** `Alpha Centauri A b III`, not `Pandora`. Kopernicus
  keeps the player-facing label in a separate field (`Properties { displayName }`), so
  the internal name is free to be the designation.
- **The whole designation, not its tail.** The short form the owner first sketched
  (`AbI`, `AbII`, ...) collides: `Alpha Centauri A b` and `40 Eridani A b` both reduce to
  `A b`, and once 40 Eri A b has moons their numerals collide too. Checked all 22
  designations for this; the full form is unique, 24 names with no duplicate.
- **Case is the repo's own.** The satellite numeral stays upper case per CONVENTIONS
  §5.2b (`A b I`-`A b V`) and IAU satellite practice (`Jupiter I` = Io). Owner asked
  twice about this and then asked for the existing convention, which is what this is.

`to_kopernicus_name` lives in `_naming.py` with the other canonical converters and is
deliberately an identity function: writers import one place instead of each inventing a
transform, and the three rules sit next to the thing they govern.

Six emitted bodies changed name: Polyphemus to Alpha Centauri A b, Pandora to
Alpha Centauri A b III, Cassandra to Alpha Centauri A b IV, and the three Proxima
planets from the board's `Proxima Cen x` shorthand to `Proxima Centauri x`. That last one
is the case this was meant to catch, since the board key and the designation genuinely
differed and the cfg had been shipping the board key.
