<!-- Principia가 싣고 있는 태양계 천체별 지오포텐셜(J2·구면조화) 실제 값 — 우리 천체 작성용 레퍼런스 -->
# Principia Geopotential Data — Solar System Bodies (verbatim)

The real oblateness / spherical-harmonic gravity data that **Principia** ships for
the Solar System, copied verbatim so we can write our own bodies (e.g. Polyphemus)
the same way. This is the *data* companion to the cfg *schema* in
[`principia-cfg-reference.md`](principia-cfg-reference.md).

## Source

- Repo: **`mockingbirdnest/Principia`**, file **`astronomy/sol_gravity_model.proto.txt`** (`master`).
- Last commit touching it: `55f4f93` (2019-08-10).
- File header conventions (verbatim): axis directions / radii / reference angles /
  angular frequencies from *IAU WGCCRE 2009* (Archinal et al.), at JD 2451545.0
  (2000-01-01 12:00 TDB); gravitational parameters from the DE431 SPICE kernel
  (`gm_de431.tpc`). **"Degree 2 order 1 is systematically omitted in the geopotentials."**

## Format — three forms, and the proto↔cfg mapping

Principia's bundled data is **protobuf text** (`field : value`, nested
`geopotential { row { column {…} } }`). The KSP-side mod cfg
([`principia-cfg-reference.md`](principia-cfg-reference.md)) uses the same numbers in
KSP node syntax (`field = value`, `geopotential_row { geopotential_column {…} }`).
Oblateness appears in **three** forms:

| form | used by | proto.txt | KSP cfg equivalent |
|---|---|---|---|
| **scalar J2** | Sun | `j2 : 2.11e-07` | `j2 = 2.11e-07` |
| **zonal `j:` rows** | the 4 giants | `geopotential { row { degree: N, column { order: 0, j: …, sin: 0 } } }` | `geopotential_row { degree = N, geopotential_column { order = 0, cos = … } }` |
| **full cos/sin rows** | Earth, Mars, Moon | `column { order: M, cos: …, sin: … }` | `geopotential_column { order = M, cos = …, sin = … }` |

**Normalization (important).** The two coefficient styles are **not** the same
normalization:
- **`j2` and the zonal `j:` fields are UNNORMALIZED** zonal harmonics Jₙ (the
  textbook J2 = 0.0147 for Jupiter, etc.).
- **`cos` / `sin` are NORMALIZED** Stokes coefficients C̄ₙₘ / S̄ₙₘ (Earth C̄₂₀ = −4.84e‑04).
- Conversion for the zonal degree-2 term: **J₂ = −√5 · C̄₂₀**. Check: Earth
  −√5 × (−4.84169e‑04) = **1.0826e‑03** = Earth's known J₂ ✓.

`reference_radius` is mandatory whenever any geopotential/J2 is present (the radius
the coefficients are scaled to — **not** necessarily the mean radius).

---

## Sun — scalar J2 only

```
  body {
    # J2 coefficient and reference radius from http://ilrs.gsfc.nasa.gov/docs/2014/196C.pdf
    name                    : "Sun"
    gravitational_parameter : "1.3271244004193938e+11 km^3/s^2"
    reference_instant       : "JD2451545.000000000"
    mean_radius             : "696000.0 km"
    axis_right_ascension    : "286.13 deg"
    axis_declination        : "63.87 deg"
    reference_angle         : "84.176 deg"
    angular_frequency       : "14.1844000 deg / d"
    j2                      : 2.1106088532726840e-07
    reference_radius        : "696000.0 km"
  }
```
Tiny J₂ (~2e‑07) — and this is the **real measured value**, not an in-game
simplification: the Sun's true flattening is ≈ 9×10⁻⁶ (equator only ~6–10 km larger
than the pole out of 696,000 km), one of the roundest natural bodies known. It rotates
slowly (~25 d) against enormous self-gravity, so centrifugal flattening is negligible —
the opposite of a ~10 h gas giant. (A solar J₂ this small also keeps Mercury's perihelion
precession a clean GR test.)

---

## Jupiter — zonal `j:`, degrees 2–12

```
    # Geopotential and reference radius from Iess et al. (2018).
    name : "Jupiter"
    gravitational_parameter : "1.266865349218008e+08 km^3/s^2"
    mean_radius : "69911 km"   reference_radius : "71492 km"
    axis_right_ascension : "268.056595 deg"   axis_declination : "64.495303 deg"
    reference_angle : "284.95 deg"   angular_frequency : "870.5360000 deg / d"
    geopotential {
      row { degree: 2,  column {order: 0, j: 14696.572e-06, sin: 0}},
      row { degree: 3,  column {order: 0, j:    -0.042e-06, sin: 0}},
      row { degree: 4,  column {order: 0, j:  -586.609e-06, sin: 0}},
      row { degree: 5,  column {order: 0, j:    -0.069e-06, sin: 0}},
      row { degree: 6,  column {order: 0, j:    34.198e-06, sin: 0}},
      row { degree: 7,  column {order: 0, j:     0.124e-06, sin: 0}},
      row { degree: 8,  column {order: 0, j:    -2.426e-06, sin: 0}},
      row { degree: 9,  column {order: 0, j:    -0.106e-06, sin: 0}},
      row { degree: 10, column {order: 0, j:     0.172e-06, sin: 0}},
      row { degree: 11, column {order: 0, j:     0.033e-06, sin: 0}},
      row { degree: 12, column {order: 0, j:     0.047e-06, sin: 0}},
    }
```
J₂ = 14696.572e‑06 = **0.014696572**.

## Saturn — zonal `j:`, degrees 2–12

```
    # Geopotential and reference radius from Durante (2017).
    name : "Saturn"
    gravitational_parameter : "3.793120749865224e+07 km^3/s^2"
    mean_radius : "58232 km"   reference_radius : "60330 km"
    axis_right_ascension : "40.589 deg"   axis_declination : "83.537 deg"
    reference_angle : "38.90 deg"   angular_frequency : "810.7939024 deg / d"
    geopotential {
      row { degree: 2,  column {order: 0, j: 16290.564e-06, sin: 0}},
      row { degree: 3,  column {order: 0, j:     0.079e-06, sin: 0}},
      row { degree: 4,  column {order: 0, j:  -935.281e-06, sin: 0}},
      row { degree: 5,  column {order: 0, j:    -0.261e-06, sin: 0}},
      row { degree: 6,  column {order: 0, j:    86.395e-06, sin: 0}},
      row { degree: 7,  column {order: 0, j:     0.018e-06, sin: 0}},
      row { degree: 8,  column {order: 0, j:   -14.533e-06, sin: 0}},
      row { degree: 9,  column {order: 0, j:     0.190e-06, sin: 0}},
      row { degree: 10, column {order: 0, j:     4.746e-06, sin: 0}},
      row { degree: 11, column {order: 0, j:    -0.555e-06, sin: 0}},
      row { degree: 12, column {order: 0, j:    -0.960e-06, sin: 0}},
    }
```
J₂ = 16290.564e‑06 = **0.016290564**.

## Uranus — zonal `j:`, degrees 2 & 4 only

```
    # Spherical harmonic coefficients and reference radius from Jacobson (2014).
    name : "Uranus"
    gravitational_parameter : "5.793951322279009e+06 km^3/s^2"
    mean_radius : "25362 km"   reference_radius : "25559 km"
    axis_right_ascension : "257.311 deg"   axis_declination : "-15.175 deg"
    reference_angle : "203.81 deg"   angular_frequency : "-501.1600928 deg / d"
    geopotential {
      row { degree: 2, column {order: 0, j: 3510.7e-06, sin: 0}},
      row { degree: 4, column {order: 0, j:  -34.2e-06, sin: 0}},
    }
```
J₂ = **0.0035107**. (Angular frequency is **negative** — Uranus is retrograde.)

## Neptune — zonal `j:`, degrees 2 & 4 only

```
    # Spherical harmonic coefficients and reference radius from Jacobson (2009).
    name : "Neptune"
    gravitational_parameter : "6.835099502439672e+06 km^3/s^2"
    mean_radius : "24622 km"   reference_radius : "25225 km"
    axis_right_ascension : "299.36 deg"   axis_declination : "43.46 deg"
    reference_angle : "253.18 deg"   angular_frequency : "536.3128492 deg / d"
    geopotential {
      row { degree: 2, column {order: 0, j: 3408.428530717952e-06, sin: 0}},
      row { degree: 4, column {order: 0, j:  -33.398917590066e-06, sin: 0}},
    }
```
J₂ = **0.003408428530717952**.

> **Note the giants' pattern:** strong even zonals (J₂ ≫ J₄ ≫ J₆), negligible odd
> zonals, no tesseral (order > 0) terms — a fast-rotating fluid body is smooth and
> axisymmetric. J₄ is negative (the bulge falls off faster than a pure J₂). This is
> exactly the form a gas giant like Polyphemus should use.

---

## Earth — full normalized cos/sin, degrees 2–10

Source comment: combined GRACE/GEOS model **GGM05C** (`ftp://ftp.csr.utexas.edu/pub/grace/GGM05/`).

```
    name                    : "Earth"
    gravitational_parameter : "3.9860043543609598e+05 km^3/s^2"
    mean_radius             : "6371.0084 km"
    axis_right_ascension    : "0.0 deg"
    axis_declination        : "90.0 deg"
    reference_angle         : "190.147 deg"
    angular_frequency       : "360.9856235 deg / d"
    reference_radius        : "6378.1363 km"
    geopotential {
      row { degree: 2,
        column {order:  0, cos: -4.8416945732000e-04, sin:  0},
        column {order:  2, cos:  2.4393734159398e-06, sin: -1.4002940118364e-06}},
      row { degree: 3,
        column {order:  0, cos:  9.5716475834116e-07, sin:  0},
        column {order:  1, cos:  2.0304466371688e-06, sin:  2.4824063468478e-07},
        column {order:  2, cos:  9.0476467441002e-07, sin: -6.1900662463325e-07},
        column {order:  3, cos:  7.2128525517036e-07, sin:  1.4144000651650e-06}},
      row { degree: 4,
        column {order:  0, cos:  5.3998153921365e-07, sin:  0},
        column {order:  1, cos: -5.3618081337028e-07, sin: -4.7357697696907e-07},
        column {order:  2, cos:  3.5049214427031e-07, sin:  6.6250516574391e-07},
        column {order:  3, cos:  9.9086103111508e-07, sin: -2.0095089980582e-07},
        column {order:  4, cos: -1.8849242252755e-07, sin:  3.0881857855702e-07}},
      row { degree: 5,
        column {order:  0, cos:  6.8650323458391e-08, sin:  0},
        column {order:  1, cos: -6.2914579409678e-08, sin: -9.4342598600045e-08},
        column {order:  2, cos:  6.5205860316915e-07, sin: -3.2334307981429e-07},
        column {order:  3, cos: -4.5183137844644e-07, sin: -2.1494236736021e-07},
        column {order:  4, cos: -2.9532340917041e-07, sin:  4.9810578844048e-08},
        column {order:  5, cos:  1.7481435046942e-07, sin: -6.6935467701596e-07}},
      row { degree: 6,
        column {order:  0, cos: -1.4997605610883e-07, sin:  0},
        column {order:  1, cos: -7.5943265879397e-08, sin:  2.6525683249700e-08},
        column {order:  2, cos:  4.8635603179946e-08, sin: -3.7376947326560e-07},
        column {order:  3, cos:  5.7251326495652e-08, sin:  8.9731654074799e-09},
        column {order:  4, cos: -8.5996937469007e-08, sin: -4.7142652438675e-07},
        column {order:  5, cos: -2.6716319362048e-07, sin: -5.3649603802896e-07},
        column {order:  6, cos:  9.4799107163032e-09, sin: -2.3738360514414e-07}},
      row { degree: 7,
        column {order:  0, cos:  9.0500819789642e-08, sin:  0},
        column {order:  1, cos:  2.8088622262423e-07, sin:  9.5159759814302e-08},
        column {order:  2, cos:  3.3039550420017e-07, sin:  9.3020287728326e-08},
        column {order:  3, cos:  2.5046335396041e-07, sin: -2.1709707579017e-07},
        column {order:  4, cos: -2.7498638931989e-07, sin: -1.2405070527179e-07},
        column {order:  5, cos:  1.6469638664557e-09, sin:  1.7930957773652e-08},
        column {order:  6, cos: -3.5879864059130e-07, sin:  1.5179288962731e-07},
        column {order:  7, cos:  1.5230586682001e-09, sin:  2.4103042687242e-08}},
      row { degree: 8,
        column {order:  0, cos:  4.9478326949545e-08, sin:  0},
        column {order:  1, cos:  2.3140759375679e-08, sin:  5.8905000941228e-08},
        column {order:  2, cos:  8.0020451775005e-08, sin:  6.5300088951785e-08},
        column {order:  3, cos: -1.9359078476200e-08, sin: -8.5941592936614e-08},
        column {order:  4, cos: -2.4434458705958e-07, sin:  6.9812156090700e-08},
        column {order:  5, cos: -2.5701616796151e-08, sin:  8.9205635687968e-08},
        column {order:  6, cos: -6.5971100477032e-08, sin:  3.0894511043496e-07},
        column {order:  7, cos:  6.7256526485194e-08, sin:  7.4864353638378e-08},
        column {order:  8, cos: -1.2403256812475e-07, sin:  1.2054023904735e-07}},
      row { degree: 9,
        column {order:  0, cos:  2.8022721711668e-08, sin:  0},
        column {order:  1, cos:  1.4214925632662e-07, sin:  2.1415689169158e-08},
        column {order:  2, cos:  2.1411871093739e-08, sin: -3.1680177946272e-08},
        column {order:  3, cos: -1.6060220449404e-07, sin: -7.4250161337509e-08},
        column {order:  4, cos: -9.3492553818025e-09, sin:  1.9898624014305e-08},
        column {order:  5, cos: -1.6315077786051e-08, sin: -5.4043600040799e-08},
        column {order:  6, cos:  6.2784132964798e-08, sin:  2.2296366358079e-07},
        column {order:  7, cos: -1.1798115451725e-07, sin: -9.6920684034663e-08},
        column {order:  8, cos:  1.8813248989960e-07, sin: -3.0019794719453e-09},
        column {order:  9, cos: -4.7558362699944e-08, sin:  9.6876870006845e-08}},
      row { degree: 10,
        column {order:  0, cos:  5.3345275002101e-08, sin:  0},
        column {order:  1, cos:  8.3753701278788e-08, sin: -1.3109438169724e-07},
        column {order:  2, cos: -9.3977781512067e-08, sin: -5.1264999905428e-08},
        column {order:  3, cos: -6.9910538916696e-09, sin: -1.5412815968052e-07},
        column {order:  4, cos: -8.4459158980573e-08, sin: -7.9023911359757e-08},
        column {order:  5, cos: -4.9285509081565e-08, sin: -5.0617431292160e-08},
        column {order:  6, cos: -3.7586959404344e-08, sin: -7.9771481050624e-08},
        column {order:  7, cos:  8.2571270822778e-09, sin: -3.0490009250716e-09},
        column {order:  8, cos:  4.0589757557591e-08, sin: -9.1710645675513e-08},
        column {order:  9, cos:  1.2538547435906e-07, sin: -3.7942358311393e-08},
        column {order: 10, cos:  1.0042327725658e-07, sin: -2.3863826960514e-08}},
    }
```

## Other terrestrials (format samples)

Rocky/irregular bodies use the **full cos/sin** form (tesseral terms present, because
solid mantles are lumpy and not axisymmetric):
- **Mars** — Konopliv et al. (2016) MRO field, degrees 2–10, full order. `reference_radius = 3396 km`, GM `4.282837362069909e+04 km^3/s^2`. Degree-2: `order 0 cos −0.8750220924537e‑03`, `order 2 cos −0.8463302655983e‑04 / sin 0.4893941832167e‑04`.
- **Moon** — GRAIL GRGM1200A, degrees 2–39 (~38 rows), full cos/sin. `reference_radius = 1738.0 km`.

---

## Applying to NearStars bodies

### Why it matters — artificial satellites (the primary driver)

J₂ is the **dominant non-Keplerian perturbation on low artificial satellites**: it drives
nodal regression + apsidal precession (∝ (R/a)²·cos i). Principia integrates vessels
(massless test particles) in the **full geopotential**, so a player's satellites precess
realistically in-game — sun-synchronous, frozen, and Molniya orbits all exploit exactly
this. So geopotential is a **first-order gameplay effect for any body players orbit craft
around** (≈ all of them), not just bodies with natural moons. (It is negligible for the
body's *own* heliocentric orbit; the impact is on whatever orbits **it**.)

### J₂ — a derived emit (set it broadly, near-zero manual cost)

J₂ follows deterministically from rotation + density + mass + radius (the **Darwin–Radau**
relation), so it is a *derived* emit field (like a unit conversion), auto-computed per body
— **not** an art-direction decision. By body type:

- **Gas giant / fast free rotator** (Polyphemus) → zonal **J₂** (+ optional **J₄** ≈ −4 %
  of J₂, **J₆**), no tesseral. Large: Jupiter 0.0147, Saturn 0.0163; Polyphemus (~10 h spin,
  0.47 g/cc, below Saturn's 0.69) → **J₂ ≈ 0.018–0.025**. Form: scalar `j2` (+ optional
  `geopotential_row` J₄/J₆), `reference_radius` = equatorial radius.
- **Free-rotating rocky** (rare — fast non-locked) → small zonal **J₂** (slow spin → tiny);
  tesseral (longitude lumps) is unmeasurable for an exoplanet → omit (J₂ only) or synthesize
  (class C). Form: scalar `j2`.
- **Tidally-locked rocky** (much of the roster — TRAPPIST-1, Proxima b …) → **NOT
  axisymmetric**: the permanent star-facing tidal bulge makes it triaxial, so degree 2 carries
  **J₂ (C̄₂₀) AND a real C̄₂₂ ≈ 0.3·J₂** (hydrostatic ratio J₂ = 10/3·C₂₂, verified on
  Io/Europa/Ganymede) — predictable, not unmeasurable. Rotation = orbital period (known).
  Form: full cos/sin degree 2 (`geopotential_row` degree 2: order 0 = C̄₂₀, order 2 = C̄₂₂).

### Deriving J₂ for an added giant — the Radau–Darwin method (literature-grounded)

A fictional giant has no measured J₂, so per the derived-value rule we ground the
**method** (not a fake measurement). Use the first-order **Radau–Darwin relation**
(Helled, Anderson, Schubert & Stevenson 2011, eq. 3, [arXiv:1109.1627](https://arxiv.org/abs/1109.1627); orig. Zharkov &
Trubitsyn 1978 / Murray & Dermott 1999 §4.4):

```
NMoI = C/(M R²) = (2/3)·[1 − (2/5)·√(5m/(m + 3·J₂) − 1)]      m = ω²·R̄³/(G·M)  (MEAN radius)
inverted →  J₂ = (m/3)·[5/(s²+1) − 1],   s = (5/2)·(1 − (3/2)·NMoI)
```

The one free input is the **normalized moment of inertia** NMoI = C/MR² (central
condensation). Bound it from the measured giants — Jupiter ≈ 0.264, Saturn ≈ 0.21, ice
giants ≈ 0.22–0.24 (Helled+2011/2020 [[arXiv:2007.10783](https://arxiv.org/abs/2007.10783)]; Fortney+2018 [[arXiv:1609.06324](https://arxiv.org/abs/1609.06324)];
homogeneous sphere = 0.40). A lower-mass / lower-density giant is *less* centrally
condensed than Saturn → slightly higher NMoI.

**Always calibrate the implementation on the real giants first** (the rule's verify step):
the same relation reproduces Jupiter's J₂ to **−0.0 %** (m 0.0834, NMoI 0.2648) and Saturn's
to **−10 %** (m 0.140, NMoI 0.220). The Saturn residual is the **first-order truncation
error**, which grows with m — so for a fast rotator (large m) the RD value is a slight
*under*-estimate of the true J₂.

**Worked — Polyphemus** (M = 120 M⊕, R_eq = 1.0 R_Jup, P_rot ≈ 10.1–10.6 h, NMoI ≈ 0.23
[0.21–0.26]): iterating the figure (f = 3⁄2·J₂ + 1⁄2·m → mean radius → m) gives m ≈ 0.19,
flattening ≈ 0.13, and **J₂ ≈ 0.023** (central). m ≈ 0.19 > Saturn's 0.14, so first-order
truncation under-predicts by ~10–20 % → true ≈ **0.025–0.026**. Range **0.017–0.033**
(dominated by the NMoI assumption). Calibration J₂ for the giants from Iess et al. 2018
(Jupiter) / Durante et al. 2017 (Saturn). State the NMoI assumption + range whenever this
value is used.

### Higher-degree from the heightmap (optional, terrain stage)

The lumpy **degree-3+** field can be derived from a body's **heightmap** once terrain exists
(Kopernicus PQS / Parallax): treat the topography as a crustal-density mass layer, apply
isostatic (Airy) compensation, take its spherical-harmonic transform → C̄ₙₘ/S̄ₙₘ **consistent
with the visible mountains/basins** (self-consistent gravity ↔ terrain). Caveats: needs an
assumed crustal density + compensation factor (raw topography *overstates* gravity — large
features float on low-density roots); for a fictional body these are synthesis-grade choices.
**Impact is tiny** — J₂ dominates satellite precession by 2–3 orders of magnitude; topography
terms (~10⁻⁵ and down) matter only for very low orbits / surface gravimetry. So this is a
self-consistency nicety, sequenced **after** terrain authoring, low priority. **NB the
heightmap does NOT give J₂** — J₂ is the rotational figure (Darwin–Radau), and the heightmap
is measured relative to that datum, so it carries no information about it.

## Related
- [`principia-cfg-reference.md`](principia-cfg-reference.md) — the cfg *schema* (node syntax, units, J2/geopotential fields)
- `phase3/stability-sim/context-notes.md` — J2 fidelity gap for moon sims (our REBOUND runs omit J2; Principia includes it)
