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

## The law

Rodríguez-Mozos & Moya 2022 (RM22, A&A 661, A176, arXiv **[2203.01065](https://arxiv.org/abs/2203.01065)**, cached)
estimate a rocky planet's magnetic moment from **mass + radius + orbital period
alone**, by (1) solving the internal structure (core radius `r₀`, core density
`ρ₀`) against a PREM-anchored equation of state, then (2) feeding that core into
the convection-driven dynamo scaling laws of Olson & Christensen 2006 (OC06,
`2006E&PSL.250..561O`). Unlike the giant case, the field is **not** set by total
luminosity; it is set by the **convective buoyancy flux** through a conducting
liquid-iron core:

    ℳ ∝ (dynamo scaling of the core buoyancy flux F, core geometry r₀, D)

OC06 identify four dimensionless controls. The pipeline treats three of them as
**gates**, because they decide whether a field exists at all and which regime it
sits in — this is why a rocky field is a *decision ladder*, not one closed form:

1. **Dynamo-alive gate** — the magnetic Reynolds number must exceed the critical
   `Rm > 40` (Gaidos 2010, `2010ApJ...718..596G`), else there is no self-sustained
   dynamo and `ℳ = 0`. A frozen, non-convecting, or too-slow core fails here.
2. **Regime gate (local Rossby number)** — `Ro_ℓ < 0.12` → **dipolar** (strong,
   organized field); `Ro_ℓ > 0.12` → **multipolar** (the moment collapses to
   `≈ 0.06 ×` its dipolar value; OC06's coefficient, which RM22 re-confirm on the
   Solar System, vs 0.15 in Grießmeier 2009).
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
   plate tectonics → low CMB heat flux), or `Rm < 40` → `ℳ = 0`, done.
3. **Base moment** `ℳ_base` from the mass/CMF class anchor (table below).
4. **Regime** — estimate rotation from tidal state (Grießmeier 2009 coupling test
   `2009Icar..199..526G`; for eccentric orbits the spin-orbit resonance from
   Dobrovolskis 2007 `2007Icar..192....1D`). Fast/free rotator → dipolar, keep
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
  regime penalty (Garraffo 2017, `2017ApJ...843L..33G`, arXiv 1706.04617) gives a
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

- **Rodríguez-Mozos & Moya 2022** (RM22), A&A 661, A176 (arXiv
  **[2203.01065](https://arxiv.org/abs/2203.01065)**). The method: internal
  structure (PREM-anchored EOS) → OC06 dynamo scaling → magnetic moment from
  M, R, orbital period, validated on the Solar System and applied to 176 TESS
  planets. **Cached** in `docs/phase3/_papers/2203.01065.md`.
- **Olson & Christensen 2006** (OC06), E&PSL 250, 561 (`2006E&PSL.250..561O`).
  "Dipole moment scaling for convection-driven planetary dynamos" — the buoyancy-flux
  scaling laws, the `Ro_ℓ = 0.12` dipolar/multipolar boundary, and the ~0.06
  multipolar reduction that RM22 build on.
- **Gaidos, Conrad, Manoj & Blake 2010**, ApJ 718, 596 (`2010ApJ...718..596G`).
  "Thermodynamic Limits on Magnetodynamos in Rocky Exoplanets" — the `Rm > 40`
  dynamo-onset gate and the no-solid-inner-core above ~2.5 M⊕ result.
- **Driscoll & Olson 2011**, Icarus 213, 12 (`2011Icar..213...12D`). "Optimal
  dynamos in the cores of terrestrial exoplanets" — liquid-core-until-shutdown
  and the core-surface-to-planet-surface field extrapolation.
- **Grießmeier, Stadelmann, Grenfell, Lammer & Motschmann 2009**, Icarus 199, 526
  (`2009Icar..199..526G`). Tidal-coupling test used to decide whether a planet is
  spin-locked (setting the rotation that feeds the regime gate).
- **Dobrovolskis 2007**, Icarus 192, 1 (`2007Icar..192....1D`). "Spin states and
  climates of eccentric exoplanets" — most-probable spin-orbit resonance for
  eccentric, tidally-influenced orbits.
- **Garraffo et al. 2017**, ApJL 843, L33 (`2017ApJ...843L..33G`, arXiv
  **[1706.04617](https://arxiv.org/abs/1706.04617)**, cached). Slow-rotation /
  sub-Alfvénic magnetic environment of TRAPPIST-1; the tidal-lock field context
  for M-dwarf planets.
- **Wang et al. 2025** (arXiv **[2504.16662](https://arxiv.org/abs/2504.16662)**).
  Planet-specific MHD override for TRAPPIST-1 e (Earth-analog field assumption).

## Related

- [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) — the giant /
  substellar energy-flux method; the two split at the rocky ↔ sub-Neptune boundary.
- [`mass-radius-relation-methodology.md`](mass-radius-relation-methodology.md) —
  supplies the M ↔ R ↔ density tie-break that seeds the internal-structure step.
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md) —
  decides the rotation state that feeds this method's regime gate.
- [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md) —
  consumes this method's `B_eq` to size the magnetosphere + belts (→ Kerbalism).
- `methodology-index.md` — the living index of all derived-value recipes.
