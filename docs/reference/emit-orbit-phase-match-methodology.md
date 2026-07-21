<!-- 직접검출 행성의 emit 궤도 위상을 관측 하늘 PA에 정합하고 게임 에포크로 되감는 방법(관측 근거 + 교과서 천체역학) -->
# Observation-anchored emit orbital phase: sky-PA match + epoch rewind

Method reference for setting the **emit orbital phase** (longitude of ascending
node Ω, argument of periapsis ω, and mean anomaly M) of a planet that has a **real
direct-imaging or astrometric detection**, so that the in-game body reaches the
*observed sky position angle* at the time corresponding to the observation, with
the orbit quoted at the game solar-system epoch.

This replaces the previous practice of dropping in an arbitrary osculating snapshot
(e.g. "the state at t = 500 yr of the stability run") as the emit default. The phase
of a well-detected planet is not free. It is anchored, as far as the geometry
allows, to where the planet was actually seen. Bodies with **no** phase-constraining
detection (non-detected, or synthetic) keep a free/seeded phase and do not use this
recipe.

The governing relations here are **textbook celestial mechanics** (Kepler orbit →
sky projection; linear-in-time mean anomaly), which are the allowed exception to
"derived values must be paper-grounded." What *is* grounded, and ADS-verified, is
the single observational anchor: the measured sky position angle, separation, and
date from the discovery paper.

## The relations

**1. Sky projection of a Kepler orbit.** With the reference (x–y) plane taken as the
plane of the sky and the z-axis along the Earth line of sight, the on-sky offset of
the planet from its host is the standard 3-1-3 rotation of the orbital-plane position
by (ω, i, Ω). Adopting the visual-binary convention **+x = celestial North,
+y = East**, the position angle and projected separation are

    PA   = atan2(East, North) = atan2(y, x)   (mod 360°, measured N→E)
    ρ_AU = √(x² + y²)          ,   ρ_arcsec = ρ_AU / d_pc

This convention is consistent with how visual-binary orbital elements are tabulated
(Ω = position angle of the ascending node, measured N→E), so an orbit built directly
from a catalog solution needs **no reorientation**: see the precondition below.

**2. Mean anomaly is linear in time.** For a two-body orbit,

    M(t) = M(t₀) + n·(t − t₀) ,     n = 2π/P  (mean motion)

so a phase known at one epoch is transported to another by adding n·Δt and wrapping.
Only M transports this way; the slowly-varying plane elements (a, e, i, Ω, ω) are
treated as constant over the rewind (quantified in Domain of validity).

**3. The observational anchor (the only grounded input).** The discovery paper
supplies (PA_obs, ρ_obs, JD_obs): the measured position angle, separation, and date
of the detection. These are ADS-verified and read from the cached full text, never
from a summary.

## The procedure

**Precondition: the simulation must be sky-anchored.** The N-body build must feed
the host system's orbital elements (i, Ω, ω) **verbatim from the J2000 visual-binary
/ astrometric solution**, with no canonicalization or randomization of orientation.
Then REBOUND's reference plane *is* the plane of the sky and an absolute PA is
recoverable. (In NearStars this holds for the `alpha_centauri` loader; the generic
`build_planetary_system` loader instead subtracts 90° from transit inclinations and
randomizes Ω. Its frame is **not** sky-anchored and this recipe does not apply
without first adding an anchor.)

**Step 1: forward-only PA scan.** Integrate the adopted system and, at each sample,
compute the planet's sky offset (r_planet − r_host) → PA. Choose the epoch t\* that
minimizes |PA − PA_obs|. Prefer a crossing **near the integration start** (least
precession drift to the game epoch). Report the achieved PA error and the projected
separation.

> **Forward-only is mandatory.** TRACE + the Python-callback J₂ operator are
> symplectic; calling `sim.integrate()` to non-monotonic times (e.g. a ternary
> search that steps backward) corrupts the state: in testing this produced
> hyperbolic garbage (a < 0, e > 1, wrong separation). Scan strictly forward, and
> read the emit state from a **fresh build integrated once** to t\*.

**Step 2: read the emit-frame osculating elements** at t\* (fresh build): a, e, i,
Ω, ω, and M_obs, in whatever frame the cfg writer consumes (for NearStars binaries,
the board's AB-plane frame). A self-check recomputes the sky PA from the fresh build
to confirm it reproduces Step 1 (no corruption).

**Step 3: rewind the mean anomaly to the game epoch.** The matched state is the
*observation-epoch* phase; the emit orbit must be quoted at the game solar-system
epoch **JD 2433282.5 = 1950.0** (Sol-Configs convention, epoch = 0 for all bodies):

    Δt      = (JD_obs − 2433282.5) / 365.25            [yr]
    M_epoch = (M_obs − 360°·Δt / P) mod 360°

with P the planet's sidereal period about its host (from the same integration). Keep
a, e, i, Ω, ω at their t\* values. Emit (a, e, i, Ω, ω, M_epoch).

**Step 4: record and gate.** Update the Phase 4 `orbit` fields (Ω/ω/mean_anomaly),
add the discovery-paper `refs`, and write the rationale + caveats into the narrative
(EN + KO). Validate with `scripts/check_phase4_gate.py`.

The tool implementing Steps 1–3 is
[`phase3/stability-sim/scripts/scan_pa_match.py`](../../phase3/stability-sim/scripts/scan_pa_match.py)
(Alpha Cen A b template).

## Validation: Alpha Centauri A b (Polyphemus)

Matched to the JWST/MIRI 15.5 µm candidate **S1** (Beichman et al. 2025): PA
**83.5° ± 4.9**, ρ 1.51″ (≈ 2.0 AU at 1.347 pc), detected **2024-08-10**
(JD 2460532.5), not recovered Feb/Apr 2025.

| Quantity | Value | Check |
|---|---|---|
| Matched sky PA at t\* = 2.185 yr | 83.66° | vs obs 83.5° → **err 0.16°** ✓ |
| Fresh-build self-check PA | 83.66° | reproduces Step 1 (no corruption) ✓ |
| Mutual inclination at t\* | 15.88° | vs design 16° ✓ |
| Sidereal period about A | 1.9307 yr | Kepler(a = 1.6 AU, M_A) ✓ |
| Δt (2024-08-10 → 1950.0) | 74.61 yr = 38.64 orbits | |
| Rewind: M_obs → M_epoch | 321.46° → **90.05°** | emit value |

Emitted orbit (AB-plane frame, epoch 1950.0): a = 1.6034 AU, e = 0.1024, i_mut =
15.88°, Ω = 273.10°, ω = 122.38°, **M = 90.05°**. In-game, 74.6 yr after epoch
(≈ 2024) the planet returns to PA 83.5°.

## Domain of validity & honest limits

- **Direction-only match.** The recipe matches PA, not separation. If the adopted
  orbit is smaller or rounder than the observed one, the projected separation along
  PA_obs falls short. For Alpha Cen A b the match sits at **0.75 AU vs the observed
  ~2.0 AU**, because PA 83.5° lies near the **minor axis** of the projected ellipse.
  The major axis lies along the real binary node (Ω = 204.85°), so the observed
  direction is intrinsically a short-separation direction for the stability-selected
  1.6 AU / e = 0.1 orbit. This shortfall is a property of the adopted orbit, cannot
  be removed within the fixed plane, and is accepted + documented (owner decision
  2026-07-21). When the adopted orbit *can* reach the observed separation, report
  both PA and ρ match.

- **Rewind assumes the in-game period.** M_epoch is computed with the integration's
  P. If the cfg writer's period (from a and the host GM) differs, the phase drifts by
  the fractional-period error times the number of orbits in Δt (here 38.6): a 0.1%
  period error ≈ 14° drift over 74 yr. Use the same a and host mass the writer will.

- **Plane precession over Δt.** Ω/ω are taken at t\* (≈ a few yr from epoch), not
  rigorously back-propagated to 1950; over ~74 yr the in-game plane precesses ~1°, so
  the observation-date PA can differ from the match by ~1°. Negligible relative to
  the separation sacrifice; note it rather than chase it.

- **Applicability.** Requires (a) a sky-anchored build and (b) a detection giving
  PA + epoch. Bodies without both keep free/seeded phase.

## Citations

- **Beichman et al. 2025**, "Worlds Next Door I", ApJL 989 L22, bibcode
  `2025ApJ...989L..22B`, arXiv **[2508.03814](https://arxiv.org/abs/2508.03814)**
  (cached `docs/phase3/_papers/2508.03814.md`). Table 2 row S1: the PA, separation,
  and date anchor. *Supplies the observational anchor.*
- **Sanghi & Beichman 2025**, "Worlds Next Door II", arXiv
  **[2508.03812](https://arxiv.org/abs/2508.03812)** (cached). Data-reduction /
  orbit-family companion; the non-detection and stable-orbit-family discussion.
  *Context for why the observed favored orbit is not the adopted one.*
- **Pourbaix & Correia 2017 / Kervella et al. 2016**, α Cen AB visual-binary orbit,
  equinox J2000, DOI `10.1051/0004-6361:20021249`. *The sky-anchoring elements
  (i = 79.205°, Ω = 204.85°, ω = 231.65°) fed verbatim into the build.*
- **Murray & Dermott 1999**, *Solar System Dynamics*: Kepler-orbit → Cartesian 3-1-3
  rotation and the linear mean-anomaly relation M(t) = M₀ + n·Δt. *Textbook relation,
  the allowed grounding exception.*

## Related

- [`body-figure-methodology`](body-figure-methodology.md): the other Principia-frame
  orbital-mechanics recipe (figure/gravity model), shares the "textbook relation +
  observational anchor" pattern.
- `phase3/stability-sim/`: the N-body harness this recipe runs inside; see the orbit
  stability-validation standard.
- `nearstars-phase4`: gates the emitted phase and records it in `phase4/<system>.yaml`.
- [methodology-index](methodology-index.md) — the index of all derived-value methodology recipes.
