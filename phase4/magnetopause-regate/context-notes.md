# Context notes — magnetopause re-gate

Append-only. Every derivation and every choice, with the reasoning, so the next
session does not re-derive them.

Calculator: `scripts/refs/magnetopause_geometry.py` (run with no arguments to
reproduce every number below).

## 1. The ram-pressure convention was already consistent, and reproduces

Both Proxima boards scale the stellar wind as `p = 2.0 nPa × (Mdot/Mdot_sun) / a_AU²`.
That was never written down anywhere, but it back-solves exactly from the
recorded values: Proxima b's 170 nPa at 0.04848 AU and Proxima c's 0.178 nPa at
1.5 AU both come out to four figures. Adopted as the stated convention.

Chapman-Ferraro then reproduces the recorded standoffs to within a quarter of a
percent for both Proxima planets: b 1.542 against a recorded 1.54, c 11.942
against 11.905. Those two noses are sound and are carried forward unchanged.

## 2. Polyphemus's recorded nose does not reproduce

The board records 23.5 R_p. The same formula with the board's own inputs
(B_eq 170 uT, 0.5 Mdot_sun at 1.6 AU, so p_ram 0.391 nPa, f = 2) gives
**22.14 R_p**. Using the board's own stated ram figure of 0.38 nPa instead
gives 22.24. Neither reaches 23.5; recovering it would need f = 2.36 rather
than the documented 2. Treated as an arithmetic drift in the earlier pass.

## 3. But the vacuum-dipole formula is the wrong one for a magnetodisc giant

This is the substantive finding of the re-gate, and it is not specific to
NearStars — Part A of the methodology has the same gap.

Chapman-Ferraro assumes the planetary field is a vacuum dipole out to the
boundary. A giant with a rotating, plasma-loaded magnetodisc inflates well
beyond that. The size of the discrepancy is measurable at Jupiter, because
Rutala 2025 fits `r_SS = 38.0 · p_SW^−0.25` R_J to the observed crossings:

| p_SW (nPa) | Chapman-Ferraro | Rutala fit | ratio |
|---|---|---|---|
| 0.03 | 46.2 R_J | 91.3 R_J | 1.98 |
| 0.13 (high) | 36.2 R_J | 63.3 R_J | 1.75 |
| 0.39 (Polyphemus') | 30.1 R_J | 48.1 R_J | **1.60** |

The ratio is not constant: Chapman-Ferraro goes as p^−1/6 and the Rutala fit as
p^−1/4, so the inflation factor itself falls as p^−1/12. Physically that reads
correctly — a harder wind squeezes the disc out of the magnetosphere and drives
the boundary back toward the vacuum-dipole answer. Evaluated at Polyphemus'
own 0.391 nPa the factor is **1.60**.

Polyphemus is if anything more disc-dominated than Jupiter: a ~1200x Io plasma
source against Jupiter's 1x, at a comparable spin (10.35 h against 9.93 h). So
1.60 is a floor, not a ceiling, for its inflation.

- Vacuum-dipole reading: **22.1 R_p**
- Disc-inflated reading (Jupiter's factor at this pressure): **35.3 R_p**

This cascades. At 22.1 R_p, Chaos (21 R_p) rides right at the boundary and the
board's "a gust of stellar wind can briefly leave it exposed" narrative holds
and in fact strengthens. At 35.3 R_p, Chaos sits comfortably inside and that
narrative fails. The belts are bounded at 0.6-0.8 R_mp, so they move too.

## 4. Polyphemus's alpha is an extrapolation either way

Rutala 2025 also fits `alpha = 0.28 + 1.08 · p_SW` (nPa), calibrated across the
observed Jovian range p_SW 0.03-0.13 nPa. Polyphemus sits at 0.391 nPa —
three times beyond the top of the calibration.

- Evaluating the fit anyway: **alpha = 0.702**
- Clamping to Jupiter's fitted ceiling: **alpha = 0.42**

Evaluating it is not obviously wrong: 0.702 lands between Earth's 0.58 and
Saturn's 0.736, both of which are measured, so the value is not out of family.
What is unsupported is the *linear* extrapolation that produced it. Saturn is
the counterexample that kills any universal pressure law — it carries the
highest measured alpha at one of the lowest pressures.

## 5. The moons split into two regimes, and the split is derived

The Alfven Mach number decides whether an embedded moon gets a Shue boundary or
a Ganymede-style sphere. The clean way to state it is as the density each moon
would need for M_A to reach 1, since the torus density profile is the uncertain
input and the threshold is not:

| moon | L (R_p) | v_rel (km/s) | parent B (uT) | n for M_A = 1 | as a multiple of the Io torus peak |
|---|---|---|---|---|---|
| Dante | 1.54 | 2.28 | 46.5 | 1.0e10 cm⁻³ | 5.0e6 x |
| Hades | 2.07 | 6.98 | 19.2 | 1.8e8 cm⁻³ | 9.0e4 x |
| Pandora | 3.53 | 28.79 | 3.87 | 4.3e5 cm⁻³ | 216 x |
| Cassandra | 7.0 | 74.61 | 0.50 | 1.1e3 cm⁻³ | **0.53 x** |
| Chaos | 21.0 | 247.53 | 0.018 | 0.13 cm⁻³ | 6.6e-5 x |

Dante, Hades and Pandora are sub-Alfvenic by margins nothing plausible closes —
Pandora would need 216x the *peak* Io torus density at 2.3x the source's
distance, where the density has fallen by orders of magnitude. Alfven-wing
regime, so a sphere.

Cassandra is the interesting one: its threshold is *below* the Io torus peak, so
with a ~1200x Io source it is very likely super-Alfvenic and does own a real bow
shock and swept tail. Chaos is unambiguously super-Alfvenic but has no field, so
nothing is owed either way.

Note Polyphemus's synchronous orbit is 1.663 R_p: Dante at 1.54 orbits *faster*
than the plasma corotates, so its relative flow is both tiny and reversed.

## 6. An embedded moon's standoff is set by magnetic pressure, not ram

At Pandora the parent's magnetic pressure is 5.943 uPa against 0.001 uPa of ram
— a factor of six thousand. Computing an embedded standoff from ram alone, the
way a planet's is computed, is simply the wrong balance.

Redone against total confining pressure:

- Pandora: **3.39 R_moon** (board records 2.6)
- Cassandra: **1.16 R_moon** (board records ~1.1 — this one holds)

Pandora's standoff is insensitive to the torus density precisely because ram is
negligible, so 3.39 is robust in a way the old 2.6 was not.

## 7. Proxima c's alpha moves on policy, not on new data

The board carries alpha 0.5 borrowed from Shue's Earth fit with a note that no
ice-giant fit exists. The methodology has since settled the ice-giant fallback
at Earth's **0.58**, justified by Voyager 2 finding Uranus and Neptune the
emptiest magnetospheres measured (Bridge 1986, Belcher 1989), which puts their
loading nearer Earth's than the gas giants'. Same reasoning, updated number.

The tail moves much further: the board's 125 R_c was a judgement call, and the
convention is now L = 150 x nose = **1791 R_c**.

## 8. Proxima b is on a template that contradicts its own field row

The board sets `radiation_model = irregular`, the stock template built for Mars'
crustal remanent magnetism — a body with *no* dynamo. Proxima b's own field row
says the opposite: an active, if weak, multipolar dynamo. Its standoff of 1.54
R_p is nearly Mercury's 1.45, and Mercury has a *fitted* Shue alpha of 0.5
(Winslow 2013), which makes it the right class analog rather than Mars.

Open question carried to the owner: `pause_deform 0.1`. It was removed from
Proxima c on the owner's judgement that multipolar fine structure reaching the
magnetopause is implausible. The same argument applies here, but b's board
treats the deformation as the point of the choice, so it is not mine to drop.

## 9. The waist beats compression, and by a lot

`pause_compression` pins the widest cross-section to the body plane. The real
boundary is widest *behind* the planet, and `pause_waist` is the only handle
that moves it. Dropping compression to 1 and letting the waist do the work
halves the residual against the Shue target:

| body | rms with compression | rms with waist | gain |
|---|---|---|---|
| Mercury | 0.445 | 0.162 | 64% |
| Earth | 6.094 | 3.101 | 49% |
| Jupiter | 9.303 | 5.389 | 42% |
| Saturn | 35.604 | 21.080 | 41% |
| Uranus | 10.969 | 5.581 | 49% |
| Neptune | 16.149 | 8.216 | 49% |
| Polyphemus | 5.127 | 3.115 | 39% |
| Proxima c | 7.278 | 3.703 | 49% |
| Proxima d | 4.581 | 2.331 | 49% |

Owner's idea, and it lands. An earlier attempt to close the same gap with
`pause_smooth` alone bought 9%, and only by driving smooth to 3x the nose,
which turns the piecewise-linear `px` into a quadratic. That is a change of
function family and was rejected; the waist does the job properly.

A separate correction on the way: `pause_smooth` is not a Shue-matching tool at
all. It exists to round the curvature discontinuity in the *cfg boundary itself*
at the terminator, where the second derivative jumps by ~2.2e4. Measuring it
against the Shue curve was the wrong question.

## 10. Proxima b: induced branch, tangent-anchored

b's clearance budget is 0.023 R_p and every decoration costs more than that:
`geomagnetic_offset` 0.25 alone drops the minimum to 0.9867, `pause_deform` 0.1
to 0.9958. Neither can be absorbed at a nose of 1.023.

Deriving the induced-boundary altitude did not help either: at the Garraffo
floor the neutral atmosphere reaches wind pressure at 164 km, at the Dong 2017
pressures 130 to 141 km, and the real ionopause sits *below* the neutral match
(calibrated on Venus, where the neutral match is 563 km against a measured 300).
So the boundary is at ~1.02 R_p whichever branch it is on.

Resolved by anchoring the thickness on the **tangent** radius rather than the
nose (owner call): the boundary has to be thick enough to carry the offset and
the deform, and that fixes nose 1.20 / tangent 1.373, clearance 1.049.

The branch itself is settled by Dong 2017 ([2017ApJ...837L..26D](https://ui.adsabs.harvard.edu/abs/2017ApJ...837L..26D)),
which finds b's dipole "not strong enough to fully protect the exoplanet" and
models it with a code built for Venus and Mars. The flaring ratio is therefore
the measured induced one, 1.144 (Mars), not Shue's 1.414.

**Recording 1.144 as a Shue alpha was tried and rejected.** log2(1.144) = 0.194
is below 0.5, and a Shue tail with alpha < 0.5 pinches itself shut - the owner
spotted it in the render. That contradicts the >=20 R_V induced tail measured at
Venus. The ratio is a local nose-to-terminator measurement and does not
generalise to a global exponent; same category error as fitting a bow-shock
conic to an induced boundary.

## 11. Multipolar and induced coexist, and Mars measures it

The question of what happens when a body has both was answered by Crider 2002
([2002GeoRL..29.1170C](https://ui.adsabs.harvard.edu/abs/2002GeoRL..29.1170C))
and Edberg 2008 ([2008JGRA..113.8206E](https://ui.adsabs.harvard.edu/abs/2008JGRA..113.8206E)):
crossings over strong crustal-field regions sit further out, by "local diversion
of shocked solar wind flow". The multipolar field lifts the induced boundary
**locally**, it does not displace it globally.

That splits the two cfg fields cleanly. `geomagnetic_offset` is the axisymmetric
component (dipole plus quadrupole, mathematically an offset dipole) and stays.
`pause_deform` is the non-axisymmetric component and is exactly the right
encoding for the local lifting. Both are kept for b.

An earlier claim in this session that "offset is not what a multipolar field
does" was wrong and is retracted. The Mars evidence is about the
non-axisymmetric part.

## 12. Two emitter bugs found while wiring this up

`load_nearstars_specs` read only `magnetism.radiation_belts` rows, so Proxima b
and d - which carry their pause on `magnetism.magnetic_field` - were recorded on
the board and silently dropped before cfg. Fixed by merging both axes per body.

`pause_deform` was in `MODEL_KEYS` but missing from the emitter's pause writer,
so the lobes of any multipolar body vanished from the output. Fixed.

## 13. The tail-length question, closed by a three-agent sweep (2026-08-16)

Three narrow literature agents, run on the owner's instruction, on the question
"if nothing goes to zero, what defines the end and at what value".

**There is no published magnetotail termination criterion.** Confirmed by an
explicit search for the phrasing. What exists is "extends at least to" detection
limits, and confirmation of the non-decay we had already computed: Slavin 1985
measures the lobe field flat at 9.2 nT from 120 to 225 R_E.

**The Earth detection record is 3100 R_E, not 225.** Intriligator 1979
(1979GeoRL...6..585I, Pioneer 7 plasma), with 1000 R_E on a plasma probe (Wolfe
1967) and 500 R_E on a magnetometer (Mariani 1969) below it. This breaks the sole
justification for `L = 150 x nose`, which gives Earth 1500 R_E. Kept anyway on
the owner's call; the doc now says plainly that it clears every magnetic
detection and is exceeded by one plasma detection.

**A real mechanism was found: current-sheet severance.** Kurth 1982 conjectured
disconnection of the distant Jovian tail; Goldstein 1985 confirmed it with a
sector crossing in the simultaneous Voyager 1 wind data. Topological, not
diffusive. It yields `L = v_wind x T_sector` with T_sector the synodic period of
the two-sector pattern against the orbit: every Solar-System planet lands near
3 AU, matching where the distant detections sit.

Computed for every body and **not adopted** (owner call). It matches 150 x nose
for giants and diverges by 2-3 orders for small bodies because it is an absolute
distance, and it is a duty cycle rather than a wall - severed tails keep
travelling, which is how comet 153P was seen 6.5 AU downstream.

**The flux budget fails too**, and its premise is false rather than merely
unhelpful: lobe flux does not drain downtail. Milan 2004 built the model and got
a length that swings 400 to 4000 R_E in three hours.

**Heliotail research is the only field that solved this**, and only by invoking
charge exchange with interstellar neutrals - jumps vanish at ~3000 AU, plasma
converges at 20,000-40,000 AU. Their phrase for the situation is the one to
keep: the downwind boundary "has diffusive nature". A planetary tail sits in
fully ionised plasma and has no such sink.

Net: the question is closed as unanswerable-in-principle for the diffusive
framing, with one topological mechanism that gives a number we chose not to use.
No further attempts.

## 14. Two plugin-side items left open (2026-08-16)

**`Pause_domain()` is the only real addition a Shue-native mode needs.** The SDF
itself is five lines, because Kerbalism never needs a true distance — the stock
pause is already a pseudo-distance, since scaling `x` by `compression` breaks the
metric, so anything negative inside and positive outside works. What has no
closed form is the bounding box: maximising `r(theta) * sin(theta)` for a
softened Shue curve tangles alpha and epsilon. Either scan it once at load, per
body rather than per frame, or precompute it offline and ship it as a field. The
offline route adds no engine code and `shue_to_stock()` already does the geometry.

**Particle-mesh sampling cost is noted and deferred** (owner call). Rejection
sampling throws points into the whole bounding box and keeps only the shell, so
the 150 x nose tail makes the box long while the yield stays thin. Jupiter is the
only body that hits the 250M sample cap, filling to about 62% of its 250,000
particles. Cosmetic only: dose comes from a direct SDF evaluation. Full numbers
in the derivation record. The fix, if wanted, is a per-body `pause_quality`
scaled against tail length rather than the flat 30 we emit today.
