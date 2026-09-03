<!-- 암석형 행성(지구/슈퍼지구)의 자기모멘트·표면장을 내부구조+OC06 다이나모 스케일링으로 도출하는 방법(논문 근거) -->
# Rocky-planet magnetic-field grounding: internal-structure + OC06 dynamo scaling

Method reference for deriving the dipole magnetic moment and surface field of
**rocky bodies** (Earth-mass and super-Earth, dry or water-rich), in the same
"cite the relation + calibration, not a fake measurement" spirit as the
[giant/substellar energy-flux method](planetary-dynamo-scaling.md). The two are
**different physics** and must not be cross-applied: the giant law (Christensen
2009 energy-flux scaling) is built for a convecting H/He envelope, while a rocky
field comes from an iron-core dynamo whose strength is set by the core's size,
density, and the heat crossing the core–mantle boundary. Citing Reiners &
Christensen 2010 for an Earth-mass planet is a citation error even though the
paper is real (the reverse mistake is caught in the giant doc's regime table).

This is the canonical home for the rocky-body method. It supersedes the scattered
prose in the Phase 3 skill's `mod-grounded-fields.md` (which now points here) and
the ad-hoc reasoning in the TRAPPIST-1 / AU Mic decisions.

## Contract — `dynamo_rocky`

**Returns** — `dipole_moment` [M_earth] · `dipole_moment_min` [M_earth] · `dipole_moment_max` [M_earth] ·
`b_eq` [uT] · `b_pol` [uT] · `b_eq_multipolar_min` [uT] · `b_eq_multipolar_max` [uT] · `regime` [—] ·
`ladder_regime` [—] · `dynamo_alive` [—]
**Needs** — `mass_earth` [M_earth] · `radius_earth` [R_earth] · `conductor_phase` [—] · `stagnant_lid` [—] ·
`age_gyr` [Gyr] · `ice_mass_fraction` [—] · `body_class` [—] · `dynamo_regime` [—]
**Discriminating keys** — the ladder regime (1 dry < 2 M⊕ · 2 dry 2–2.5 · 3 dry > 2.5 · 4 water-rich · 5
low-density dry), from mass, radius and the declared ice fraction; the alive gate, which is three labels
(`conductor_phase` from `core_state`, the declared `stagnant_lid`, the declared per-class death age) and
one quotation (`Rm > 40`, never evaluated); the regime gate, declared (`dynamo_regime`) or emitted both
ways.
**Grade** — **judgment**, always: both gates are labels and ℳ_base, the regime and the multipolar factor
are declarations. `dipole_moment` and `b_eq` are `null` for regimes 2 and 3 (the document prints no anchor;
the grid is emitted) and for cannot-say (undecided core, undeclared lid). `dynamo_alive` names why.

## The law

Rodríguez-Mozos & Moya 2022 (RM22, A&A 661, **A101**, arXiv **[2203.01065](https://arxiv.org/abs/2203.01065)**, cached)
estimate a rocky planet's magnetic moment from **mass + radius + orbital period
alone**, by (1) solving the internal structure (core radius `r₀`, core density
`ρ₀`) against a PREM-anchored equation of state, then (2) feeding that core into
the convection-driven dynamo scaling laws of Olson & Christensen 2006 (OC06,
[`2006E&PSL.250..561O`](https://ui.adsabs.harvard.edu/abs/2006E%26PSL.250..561O)). Unlike the giant case, the field is **not** set by total
luminosity; it is set by the **convective buoyancy flux** through a conducting
liquid-iron core:

    ℳ ∝ (dynamo scaling of the core buoyancy flux F, core geometry r₀, D)

⚠ **Every value this scaling emits for an exoplanet is an extrapolation, and by how much is stated here.**
OC06's fit was made on numerical dynamos whose *"model data space covers the ranges 3×10⁻⁶ ≤ E ≤ 10⁻²,
and 10⁴ ≤ Ra ≤ 1.5×10¹⁰, and also 0.06 ≤ Pm ≤ 24, 0.1 ≤ Pr ≤ 20. In all cases we use r* = 2.85"* (p. 564).
A planetary core sits near E ~ 10⁻¹² — **six decades below the lowest Ekman number the fit ever saw** — with
Pm far below 0.06. This is the same shape as the conductivity exponent's case: a narrow instrument's output
is not a general fact. RM22 apply the laws to the Solar System and recover the observed moments, which is
what licenses the ladder; it does not shrink the extrapolation, and the recipe's grade (judgment) says so.

OC06 identify four dimensionless controls. The pipeline treats three of them as
**gates**, because they decide whether a field exists at all and which regime it
sits in — this is why a rocky field is a *decision ladder*, not one closed form:

1. **Dynamo-alive gate** — the magnetic Reynolds number must exceed the critical
   `Rm > 40` (Gaidos 2010, [`2010ApJ...718..596G`](https://ui.adsabs.harvard.edu/abs/2010ApJ...718..596G)), else there is no self-sustained
   dynamo and `ℳ = 0`. A frozen, non-convecting, or too-slow core fails here. The formula: `Rm = V L / λ`,
   `λ = 1/(μ₀σ)` (Gaidos+ 2010; OC06 write `Rm = u d/λ`, and 40 is OC06's own measured onset, printed
   three times) — **quoted, not evaluated here**, because it needs V and σ that nothing we hold supplies.
   OC06's caveat rides with it: *"beyond Rm_crit there is no simple relationship between Lo_dip and Rm"* —
   an on/off gate, never a strength predictor. And Gaidos+ 2010 argue it is almost always satisfied
   (*"convective motions as small as 10⁻⁴ m/s are sufficient for Rem > 40"*, *"only very weakly dependent
   on planet mass"*), which is an argument **for** the class ladder below.
2. **Regime gate (local Rossby number)** — `Ro_ℓ < 0.12` → **dipolar** (strong,
   organized field); `Ro_ℓ > 0.12` → **multipolar** (the moment collapses to
   `≈ 0.06 ×` its dipolar value — **RM22's coefficient** (*"the reducing coefficient in the solar system
   is about 0.06"*), not OC06's: OC06 print *"across this transition the dipole moment falls by nearly a
   factor of 20"* (≈ 0.05×) and, separately, that the multipolar regime is *"reduced by a factor of 10 or
   more"*. Attribution corrected 2026-09-03 against both cached papers. ⚠ **Grießmeier 2009's 0.15 is not a
   value of this quantity** and was removed from the grid on 2026-09-04: their §2.2 gives 0.02–0.15 *M_E* —
   Earth's present moment as denominator — for one configuration (Earth-like, 0.2 AU, 0.5 M☉), adopting the
   maximum *"to obtain a lower limit for the cosmic ray flux"*; Table 1 prints 0.37/0.65/0.96 for other
   locked cases; the paper contains no Rossby number and no 0.12. The `Ro_ℓ = 0.12` boundary and the
   multipolar collapse are OC06's, executed by RM22 (their eqs for F, Ra_Q, Ro, Ro_ℓ and Table 6 inputs).
   The engine's grid is **OC06's own width, {0.05, 0.10}** — text *"nearly a factor of 20"*, abstract *"a factor
   of 10 or more"* — with RM22's Solar-System point 0.06 inside it (RM22 adopts 0.05, its reading of OC06; OC06
   prints no 0.05). ⚠ **Base-heated dynamos only** — OC06: internally heated cases are *"more gradual, show more
   scatter, and begin at smaller Ro_l"*; RM22 carries the condition (*"as is the case on Earth"*). Whether a
   roster body's core is base-heated is **not something this recipe can decide**, and the label rides on every
   multipolar value and on the 0.12 threshold itself.)
3. **Rotation** enters *only through the regime gate*, not the dipolar amplitude.
   In the dipolar linear zone the moment carries **no explicit angular-velocity
   dependence** (RM22 §5.1) — a crucial, counter-intuitive point: slow rotation
   does **not** directly weaken a dipolar field. It matters by pushing `Ro_ℓ`
   toward/over 0.12, tipping the dynamo into the weak multipolar regime.

### Surface field from the moment

RM22 §5.3 gives the dipolar field at the core surface `r₀`, then extrapolate to
the planet surface as a dipole, `B_s ∝ ℳ / R³` (Gaidos 2010; Driscoll & Olson
2011). Anchored on Earth (equatorial surface field 30 µT, polar 60 µT, moment
`ℳ⊕`), the directly-computable closing relation the pipeline uses is:

    B_s^eq (µT)  =  30 · (ℳ / ℳ⊕) · (R / R⊕)^(−3)
    B_s^pol      =  2 · B_s^eq

so the whole recipe reduces to estimating the **normalized moment `ℳ/ℳ⊕`** from
the regime ladder, then reading off the surface field. `ℳ/ℳ⊕` in normalized
Earth units is the value carried in the DB (`magnetic_dipole_moment_normalized_earth`).

## The practical procedure (calibrated to RM22's own Solar-System values)

NearStars does not re-run RM22's full internal-structure + thermal-evolution
solver per body. We instead anchor on the **moments RM22 tabulate** (Solar System
+ their TESS sample) and place each planet on the ladder:

1. **Classify the body** (mass, radius → density → dry / water-rich; see regimes).
2. **Alive?** Old + small (Mars-mass by ~7 Gyr), stagnant-lid (Venus-analog, no
   plate tectonics → low CMB heat flux), or `Rm < 40` → `ℳ = 0`, done. ⚠ **`Rm > 40` is quoted here, never
   evaluated** — this document carries no magnetic-Reynolds formula; the recipe uses `core_state`'s liquid-core
   verdict and a declared stagnant-lid judgement as the gate and says so on every result (owner condition,
   2026-09-03). Note also that RM22's own Table 8 *computes* Venus 0.0007 and Mars 0.084 ℳ⊕; the zeros in the
   validation table below are this ladder's class judgements, not the model's output.
3. **Base moment** `ℳ_base` from the mass/CMF class anchor — ⚠ **no per-class anchor table exists in this document**; the "table below" is the *per-body* validation table. The recipe (`engine/dynamo_rocky.py`) declares the anchors: regime 1 → 1.0, regime 4 → 2×10⁻³, regime 5 → 0, and **regimes 2 and 3 carry no printed value** and are emitted as grids without an elected number.
4. **Regime** — estimate rotation from tidal state (Grießmeier 2009 coupling test
   [`2009Icar..199..526G`](https://ui.adsabs.harvard.edu/abs/2009Icar..199..526G); for eccentric orbits the spin-orbit resonance from
   Dobrovolskis 2007 [`2007Icar..192....1D`](https://ui.adsabs.harvard.edu/abs/2007Icar..192....1D)). Fast/free rotator → dipolar, keep
   `ℳ_base`. Tidally-locked slow rotator that crosses `Ro_ℓ = 0.12` → multipolar,
   `ℳ ≈ 0.06 · ℳ_base`.
5. **Planet-specific override** — a dedicated MHD/dynamo paper for the actual
   planet supersedes the ladder (documented divergence; see TRAPPIST-1 e).

### Validation: the closing relation reproduces the Solar System

| Body | ℳ/ℳ⊕ (RM22 / obs) | R/R⊕ | formula B_eq | real B_eq | match |
|---|---|---|---|---|---|
| Earth | 1.0 | 1.00 | 30 µT | 30 µT | ✓ (anchor) |
| Mercury | 4×10⁻⁴ | 0.38 | 0.22 µT | ~0.3 µT | ✓ |
| Ganymede | 2×10⁻³ | 0.41 | 0.87 µT | ~0.72 µT | ✓ |
| Mars | 0 (frozen) | 0.53 | 0 | 0 (no global field) | ✓ |
| Venus | 0 (stagnant lid) | 0.95 | 0 | 0 (no dynamo) | ✓ |

RM22 validate their internal-structure + moment model against exactly these five
bodies and report "remarkably low or even negligible" errors; the closing
relation above then recovers the observed surface fields. Used **only** within the
rocky regime (M ≲ 10 M⊕, dry or water-rich, iron-core dynamo).

## Domain of validity: regimes by body class

RM22's grid runs 0.1–48 M⊕ but the physics branches sharply:

1. **Dry rocky, M < 2 M⊕**: an inner solid core can nucleate; its growth drives
   *compositional* buoyancy — the strongest, most Earth-like dynamos. Earth/PREM
   analog. `ℳ_base` up to ~1 ℳ⊕.
2. **Dry rocky, 2 ≲ M ≲ 2.5 M⊕**: core stays fully liquid until dynamo shutdown
   (Zuluaga 2013; Driscoll & Olson 2011); take convective-zone thickness `D = r₀`.
   Thermal dynamo, can exceed Earth's moment while young.
3. **Super-Earth, M > 2.5 M⊕**: no solid inner core forms (Gaidos 2010) → no
   compositional buoyancy, thermal convection only → dynamo is weaker and
   shorter-lived than a naive mass-scaling suggests. Flag confidence low.
4. **Water-rich rocky (ocean worlds)**: for the same mass and core size, the CMB
   heat flux `Q_c` is *lower* (cooler, lower-pressure CMB) → weaker moment.
   Ganymede analog (`ℳ ≈ 2×10⁻³`).
5. **Low-density dry (ρ < 0.8 ρ⊕, Mars-analog)**: small core, cools fast, likely
   dynamo-dead by a few Gyr → `ℳ = 0` today.

Above ~10 M⊕ the body is almost never dry rock (it accretes H/He and becomes a
sub-Neptune) — hand off to the [giant/sub-Neptune regime](planetary-dynamo-scaling.md),
whose §3 already flags sub-Neptune as *below* the validated giant domain.

## Worked examples (NearStars rocky planets)

Inputs are the curated Phase 2 mass/radius + Phase 3 rotation state.
`B_eq = 30 · (ℳ/ℳ⊕) · (R/R⊕)⁻³` µT; `B_pol = 2 B_eq`.

| Body | M (M⊕) | R (R⊕) | rotation | regime | ℳ/ℳ⊕ | B_eq | conf |
|---|---|---|---|---|---|---|---|
| AU Mic d | ~1.0 | ~1.0 | locked, 12.7 d | multipolar (young active core) | ~0.05 | **5 µT** | low |
| TRAPPIST-1 e | 0.69 | 0.92 | locked, 6.1 d | RM22: multipolar → ~2 µT | see note | **30 µT** (adopted) | med |

Notes:
- **AU Mic d**: Earth-mass, tidally locked at 12.7 d. RM22 ladder → a weak,
  likely-multipolar field from a young but slowly-rotating core; the slow-rotation
  regime penalty (Garraffo 2017, [`2017ApJ...843L..33G`](https://ui.adsabs.harvard.edu/abs/2017ApJ...843L..33G), arXiv [1706.04617](https://arxiv.org/abs/1706.04617)) gives a
  few µT. Adopted 5 µT equatorial — replaces an earlier, wrong citation to
  Reiners & Christensen 2010 (a giant/BD paper).
- **TRAPPIST-1 e**: the RM22 ladder derives ~2 µT (`ℳ < 0.1 ℳ⊕`) for a locked
  0.69-M⊕ core. The cfg instead adopts **30 µT / 0.3 ℳ⊕** — a *documented
  divergence*: Wang 2025 ([2504.16662](https://arxiv.org/abs/2504.16662)) MHD
  habitability simulations of e *assume* an Earth-analog 0.32 G field, and the
  interesting-first rule favors a recognizable Earth-style auroral oval over
  disorganized weak-field precipitation. The RM22-derived weak-field reading is
  preserved as a cfg variant (see the e Phase 3 report's Canonical alternatives).

Confidence is **low–medium**: the *method* is grounded and Solar-System-validated,
but the inputs (mass for non-transit planets, the internal core state, and above
all the rotation/thermal history) each carry real uncertainty, and `B_s` scales
as `ℳ/R³`. Tidal locking does not by itself null the field — it acts through the
regime gate, so a locked planet with an active core can still hold a modest field.

## Citations

- **Rodríguez-Mozos & Moya 2022** (RM22), A&A 661, A101 ([`2022A&A...661A.101R`](https://ui.adsabs.harvard.edu/abs/2022A%26A...661A.101R); the article number was printed here as A176 until 2026-09-03 — wrong) (arXiv
  **[2203.01065](https://arxiv.org/abs/2203.01065)**). The method: internal
  structure (PREM-anchored EOS) → OC06 dynamo scaling → magnetic moment from
  M, R, orbital period, validated on the Solar System and applied to 176 TESS
  planets. **Cached** in `docs/phase3/_papers/2203.01065.md` (the main checkout's cache; worktrees reach it through the symlink — see `engine/SESSION-HANDOFF.md`).
- **Olson & Christensen 2006** (OC06), E&PSL 250, 561 ([`2006E&PSL.250..561O`](https://ui.adsabs.harvard.edu/abs/2006E%26PSL.250..561O)).
  "Dipole moment scaling for convection-driven planetary dynamos" — the buoyancy-flux
  scaling laws, the `Ro_ℓ = 0.12` dipolar/multipolar boundary, and the multipolar collapse — printed as
  *"nearly a factor of 20"* (≈ 0.05×); the ~0.06 the ladder uses is RM22's Solar-System value, not OC06's.
  **Fit domain, p. 564**: *"3×10⁻⁶ ≤ E ≤ 10⁻², 10⁴ ≤ Ra ≤ 1.5×10¹⁰, 0.06 ≤ Pm ≤ 24, 0.1 ≤ Pr ≤ 20, r* = 2.85"*
  — see the extrapolation note in §The law.
- **Gaidos, Conrad, Manga & Hernlund 2010**, ApJ 718, 596 (author list corrected 2026-09-03 against ADS; the earlier row read "Manoj & Blake") ([`2010ApJ...718..596G`](https://ui.adsabs.harvard.edu/abs/2010ApJ...718..596G)).
  "Thermodynamic Limits on Magnetodynamos in Rocky Exoplanets" — the `Rm > 40`
  dynamo-onset gate and the no-solid-inner-core above ~2.5 M⊕ result.
- **Driscoll & Olson 2011**, Icarus 213, 12 ([`2011Icar..213...12D`](https://ui.adsabs.harvard.edu/abs/2011Icar..213...12D)). "Optimal
  dynamos in the cores of terrestrial exoplanets" — liquid-core-until-shutdown
  and the core-surface-to-planet-surface field extrapolation.
- **Grießmeier, Stadelmann, Grenfell, Lammer & Motschmann 2009**, Icarus 199, 526
  ([`2009Icar..199..526G`](https://ui.adsabs.harvard.edu/abs/2009Icar..199..526G)). Tidal-coupling test used to decide whether a planet is
  spin-locked (setting the rotation that feeds the regime gate).
- **Dobrovolskis 2007**, Icarus 192, 1 ([`2007Icar..192....1D`](https://ui.adsabs.harvard.edu/abs/2007Icar..192....1D)). "Spin states and
  climates of eccentric exoplanets" — most-probable spin-orbit resonance for
  eccentric, tidally-influenced orbits.
- **Garraffo et al. 2017**, ApJL 843, L33 ([`2017ApJ...843L..33G`](https://ui.adsabs.harvard.edu/abs/2017ApJ...843L..33G), arXiv
  **[1706.04617](https://arxiv.org/abs/1706.04617)**, cached). Slow-rotation /
  sub-Alfvénic magnetic environment of TRAPPIST-1; the tidal-lock field context
  for M-dwarf planets.
- **Wang et al. 2025** (arXiv **[2504.16662](https://arxiv.org/abs/2504.16662)**).
  Planet-specific MHD override for TRAPPIST-1 e (Earth-analog field assumption).

## Related

- [`interior-structure-methodology.md`](interior-structure-methodology.md): supplies the core radius this recipe consumes.
- [`surface-radiation-dose-methodology.md`](surface-radiation-dose-methodology.md) —
  consumes this doc's field strength as the weaker of its two shielding terms
  (dose ∝ B^−1.48, against the atmospheric column's ∝ C^−2…−3).
- [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) — the giant /
  substellar energy-flux method; the two split at the rocky ↔ sub-Neptune boundary.
- [`mass-radius-relation-methodology.md`](mass-radius-relation-methodology.md) —
  supplies the M ↔ R ↔ density tie-break that seeds the internal-structure step.
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md) —
  decides the rotation state that feeds this method's regime gate.
- [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md) —
  consumes this method's `B_eq` to size the magnetosphere + belts (→ Kerbalism).
- [methodology-index](methodology-index.md) — the living index of all derived-value recipes.
