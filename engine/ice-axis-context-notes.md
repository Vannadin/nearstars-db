# The ice axis — context notes

Brief 23, 2026-08-31. Pre-registration in `ice-axis-checklist.md`. Method inherited from
the rock axis (C13): end A = anchor, end B = the component spread outward, everything
renormalized as I/(M·R_pub²) against N13's P_Voy mean-radius targets so the tables sit
side by side.

## §1 The mixing question, answered from sources before any code

The brief's blocking question: does additive-volume mixing of water into H/He have
published grounding? **Yes, twice over** — no delegation needed (two ADS queries + two
ar5iv fetches, main thread):

- **Soubiran & Militzer 2015** ([`2015ApJ...806..228S`](https://ui.adsabs.harvard.edu/abs/2015ApJ...806..228S),
  arXiv:1505.07885, fetched to cache): DFT-MD of liquid H₂O–H₂ mixtures over
  **2–70 GPa × 1000–6000 K** — the ice-giant envelope band. Their words: *"We compared our
  simulation results for the mixtures with an ideal mixing approximation … an additive
  volume law at constant pressure and temperature. The ideal mixing approximation was
  found to reproduce our simulation results for the mixtures well. Some small deviations
  of the order of a few percents (up to 10 % locally), in particular for the density and
  for the internal energy"* — and they conclude it is *"sufficiently accurate for the
  construction of most planetary interior models."* Also: miscible in all proportions in
  the band; the strongest non-ideal effect is hydrogen slightly altering water's
  dissociation fraction.
- **The target itself mixes this way.** Nettelmann+ 2013's envelopes are "hydrogen,
  helium, and water" on **LM-REOS** — the *Linear Mixing* Rostock EOS (Nettelmann+ 2008,
  [`2008ApJ...683.1217N`](https://ui.adsabs.harvard.edu/abs/2008ApJ...683.1217N),
  arXiv:0712.1019, fetched to cache: *"These EOS data for the major components were
  combined by linear mixing into a new data table LM-REOS"*). Matching N13's λ with a
  linearly-mixed water-bearing envelope is matching like with like.

So **branch 4 does not fire**: unlike C4's methane (no measured LMA error anywhere), this
axis has a source-measured mixing error (few %, ≤10 % locally) over the band where the
dissolved water carries mass. Outside that band (the shallow, cool envelope) the additive
rule is extension, not grounding — the solve's note says so.

## §2 The representation decision, written after it was made

`ENVELOPE_Z_MATERIAL` is a module constant ("silicate"); the axis was not measurable by a
knob. What changed:

- **One new declaration**: `envelope_z_rock_fraction` (default 1.0 = all-silicate Z, the
  legacy arrangement, bit-identical paths — the zero-weight silicate part is even kept so
  the mixture object's shape is unchanged). Below 1.0, the remainder of Z is dissolved
  water. Threaded through `_stack`/`integrate`/`_shoot_pressure`/`shoot`/`solve`/
  `_cold_phases` exactly as the C11 declarations were; validated ([0,1]; water in the
  envelope demands a declared potential temperature).
- **`_EnvelopeWater` ("h2o_env")**: the water component of the envelope mixture, a
  dispatching part — the step's own fluid/solid rules decide the representation at each
  (P, T): ladder where solid/undecided-within-knots (every ladder phase carries thermal
  constants — checked numerically before design), water2 where liquid below 1000 K and in
  domain, Mazevet at ≥1000 K. **water1 is unusable here**: it prints only dT/dP|_S, no
  c_P, and a Mixture weights ∇_ad by c_P — the same hole that confined C5(b)'s mantle
  rock to ≥2.3 GPa. The liquid sites water1 alone covers (≲0.1 GPa warm liquid, and the
  sub-360 K liquid sliver) refuse **by name**, too_cold, per Brief 22's principle.
- Grade: already analog for any envelope_z > 0; a dedicated note names the water share,
  the Soubiran & Militzer numbers and the band, and the extension beyond it.

End configurations (Scheibe compositions as in the gate):

| | imf | gmf′ | envelope_z | z_rock_fraction |
|---|---|---|---|---|
| U end B_ice | 0 | 0.94565 | 0.85450 | 0 |
| N end B_ice | 0 | 0.93935 | 0.86341 | 0 |
| U end B_both | 0 | 1.0 | 0.86241 | 0.06302 |
| N end B_both | 0 | 1.0 | 0.87169 | 0.06958 |

(B_both has no silicate layer left — the innermost material is the envelope mixture
itself, whose p_max is h_he's 10⁴ GPa; post-Brief-22 the corridor no longer needs a stub.)

One validator widened, with the reason written at the site: the ice_giant class gate read
only the **layer** ice fraction and refused imf = 0 — it predates dissolved ice. The class
means "ice-dominated", which an 85 %-water envelope satisfies; the gate now excepts
declarations with `envelope_z_rock_fraction < 1`, and still refuses a genuinely ice-free
ice_giant by the original sentence.

## §3 Measurements — four states, none converged, one named wall

| run | z | z_rock | λ | R (vs pub) | I/(M·R_pub²) | P_c | T_c | conv |
|---|---|---|---|---|---|---|---|---|
| Uranus B_ice | 0.8545 | 0 | 0.277743 | 3.7997 (−4.55 %) | 0.2531 | 868 GPa | 9044 K | **no** |
| Uranus B_both | 0.8624 | 0.0630 | 0.293085 | 3.7630 (−5.47 %) | 0.2619 | 410 GPa | 8253 K | **no** |
| Neptune B_ice | 0.8634 | 0 | 0.283513 | 3.7913 (−1.90 %) | 0.2729 | 1125 GPa | 9098 K | **no** |
| Neptune B_both | 0.8717 | 0.0696 | 0.286595 | 3.9939 (+3.35 %) | 0.3061 | 474 GPa | 11874 K | **no** |

**Why none converged, diagnosed not guessed.** Mass closes exactly (a standalone
integration at the returned point gives mass/target = 1.000000), but the surface sticks
near **1275 K against the 76 K boundary condition**. A refusal spy over a full Uranus
B_ice solve collected 1202 PhaseGaps of which **1102 are one wall**: liquid envelope water
at **p ≲ 0.1 GPa × 500–1000 K** — the tri-corner where water1's 500 K top, water2's
0.1 GPa floor and Mazevet's 1000 K floor meet (samples: 0.000–0.097 GPa · 645–1000 K, all
too_cold=True). Every path cold enough to reach 76 K at 1 bar must cross that wedge with
85 % dissolved water, and dies in it; the temperature loop settles on the hottest
surviving surface. (The remaining ~100 gaps are ordinary h_he cold-trial steering.)

The wedge was **pre-named before the run** (§2's caveat) and it is not the corridor
(post-Brief-22 those steer; these steer too — too_cold — but there is nothing hotter to
steer *to* at the surface, because the boundary condition itself is cold). The missing
piece has a published filler: **IAPWS-95 / IF97 steam** covers exactly p ≤ 1 GPa at
500–1000 K. Baking it is a new-source decision (the owner's), not this brief's.

**On the way, one real hole was closed**: water1's baked table now carries **c_P**
(regenerated by `tools/make_water_table.py`; the source's own Gibbs quantity, physicality
criteria registered before the sweep, interpolation error 4.5e-3 in the ocean band /
1.1e-2 whole-window, worst at the supercooled corner; ρ and dT/dP|_S rows byte-identical
— the diff is purely additive). `LiquidWater` gained `c_p`/`grad_ad`, consumed only by
mixtures that contain it — no anchor path touches them, and the crosscheck now compares
c_P against SeaFreeze at the same five points. This closes the c_P half of the hole that
confined C5(b)'s mantle rock to ≥ 2.3 GPa.

## §4 The branch judgment

**Branch 3, refined**: the axis is representable **except the steam wedge**, and the
blocker is named with its three walls and its published filler. Branches 1/2 are *not
reached* — a bracket end that does not meet the boundary condition is not a measured end,
so no gap-covered percentage is reported for the ice axis (the acceptance table above
carries conv=no in place of one).

*Observation, recorded not judged*: all four non-converged states sit **above** the
targets (renorm 0.2531–0.3061 vs 0.2300/0.2410), so the arrangement's reach is not the
question the way it was for the rock axis — representability at the cold boundary is.
Worth one more sentence: the wedge-crossing is partly an artifact of the bracket's
**uniform** Z — a physically graded profile tapers the dissolved water toward the 1-bar
level and would cross the wedge with far less water in it. A graded implementation (the
actual fuzzy-core shape) is therefore *not* blocked by this wall to the same degree; that
is for whoever builds, not for this measurement.

The sum question (B_both vs B_ice) is deferred with the axis — comparing two
non-converged states would be comparing artifacts.
