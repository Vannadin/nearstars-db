<!-- 천체의 구-대비 변형(자전 편평 J2 + 조석고정 triaxial C22)을 근거화 계산해 Principia 중력모델에 채우는 방법 -->
# Body figure grounding — rotational oblateness (J₂) and tidal triaxiality (C₂₂)

Method reference for the degree-2 **figure** of every NearStars body: how far it
departs from a sphere, and which gravity coefficients capture that. Two physical
causes, two coefficients:

- **rotation** flattens a body into an oblate spheroid → zonal **J₂** (= −√5·C̄₂₀);
- **a permanent tidal bulge** on a synchronously-locked body makes it *triaxial*
  (long axis toward the primary) → adds a sectoral **C̄₂₂**.

This is the canonical home for the **method**. The *data + cfg-form* companion is
[`principia-geopotential-data.md`](principia-geopotential-data.md), which holds the
verbatim Solar-System coefficients, the normalization rules (J₂ = −√5·C̄₂₀,
J₂ = 10⁄3·C̄₂₂), and the proto↔KSP-cfg mapping — that document already works the
**Polyphemus** giant J₂ in full; this one generalizes the recipe across body types
and grounds the tidal C₂₂. J₂/C₂₂ is a **derived emit**, not an art-direction choice:
it follows deterministically from rotation + mass + radius + central condensation, so
it is computed per body like a unit conversion. Why it matters in-game: J₂ is the
dominant non-Keplerian perturbation on **artificial satellites** (nodal regression +
apsidal precession ∝ (R/a)²·cos i), and Principia integrates vessels in the full
geopotential — so it shapes every orbit a player flies around a body.

> Discipline. The figure follows from the **hydrostatic equilibrium** relations
> (Radau–Darwin, Maclaurin, the synchronous-satellite figure) — textbook results, the
> allowed exception to "derived values must be paper-grounded." What still gets cited:
> the **calibration anchors** (measured Solar-System J₂/C₂₂) and the moment-of-inertia
> bounds, resolved against NASA ADS.

## 1. The figure parameter

Both effects are governed by the dimensionless ratio of centrifugal (or tidal) to
self-gravitational acceleration at the surface:

    q  =  ω²·R³ / (G·M)            (rotational, ω = 2π/P_rot)

For a **non-locked** body ω is its sidereal spin rate. For a **synchronously locked**
body ω = n, the orbital mean motion, and the *static tide* from the primary adds a
term of the same order — because for a synchronous circular orbit
n²R³/(GM_body) = (M_primary/M_body)(R/a)³ to leading order, i.e. the rotational and
tidal parameters are comparable. We write the locked case as q_s = n²R³/(GM).

## 2. Rotational figure — Maclaurin vs Radau–Darwin

To first order in q, the flattening f = (R_eq − R_pol)/R_eq and J₂ obey the
hydrostatic relation

    J₂  =  (2/3)·f  −  (1/3)·q

The remaining freedom is **central condensation**, carried by the normalized moment
of inertia NMoI = C/(M R²) (0.4 = uniform sphere; smaller = more condensed):

- **Homogeneous (Maclaurin) limit**, NMoI = 0.4: f = (5/4)q, hence **J₂ = q/2**. This
  is the *uniform-density upper bound* on flattening.
- **Centrally condensed bodies** (all real planets/stars), NMoI < 0.4: use the
  **Radau–Darwin** relation, which ties J₂, q and NMoI (Helled et al. 2011, the form
  reproduced in `principia-geopotential-data.md`):

      NMoI = (2/3)·[1 − (2/5)·√(5q/(q + 3J₂) − 1)]
      inverted →  J₂ = (q/3)·[5/(s²+1) − 1],   s = (5/2)·(1 − (3/2)·NMoI)

  A more condensed body flattens **less** for the same q, so J₂/q falls below ½.

### Calibration (always verify on the real bodies first)

| body | type | q | NMoI | J₂/q | measured J₂ |
|---|---|---|---|---|---|
| Earth | rocky | 3.45e-3 | 0.331 | 0.31 | 1.083e-3 |
| Mars | rocky | 4.6e-3 | 0.364 | ~0.43* | 1.96e-3 |
| Jupiter | giant | 0.083 | 0.265 | 0.177 | 1.470e-2 |
| Saturn | giant | 0.140 | 0.220 | 0.116 | 1.629e-2 |
| Sun | star | ~2e-5 | ~0.06 | ~0.01 | 2.1e-7 |

\*Mars carries a Tharsis non-hydrostatic excess; its *hydrostatic* J₂ is lower. The
giant calibration reproduces Jupiter to −0 % and Saturn to −10 % (first-order
truncation, grows with q) — so for a **fast rotator (large q) the first-order value
under-predicts** the true J₂ by ~10–20 %. Stars sit at the condensed extreme: even
the Sun's slow spin gives J₂ ≈ 2×10⁻⁷ (one of the roundest bodies known).

## 3. Tidal triaxiality — synchronously locked bodies

A locked body in a (near-)circular orbit raises a **permanent** tidal bulge toward
its primary. Its degree-2 figure is then **triaxial** (semi-axes a > b > c, with a
toward the primary and c the spin axis), carrying both J₂ **and** a real sectoral
C̄₂₂. In hydrostatic equilibrium the two are locked in a fixed ratio:

    J₂  =  (10/3)·C̄₂₂        (equivalently  C₂₂ = 0.3·J₂)

and the body is a triaxial ellipsoid with axis differences (a−c):(b−c) = 4:1. This
ratio is **confirmed on the measured synchronous moons** (Io, Europa, Ganymede,
Titan all give J₂/C₂₂ ≈ 10/3), which is why the locked case is *predictable*, not
unmeasurable. The magnitude is calibrated on those same bodies:

    J₂  ≈  (0.9–1.1)·q_s     for differentiated rocky/icy synchronous bodies
    C̄₂₂ ≈ 0.30·J₂

(Io J₂/q_s ≈ 1.08, Europa ≈ 0.88 — the spread is internal structure.) So unlike a
slow *free* rotator, a close-in locked body has a J₂ comparable to q_s itself,
because rotation and tide add.

> **Fossil-bulge caveat.** The Moon (J₂/C₂₂ ≈ 9, far from 10/3) and Mercury are **not**
> hydrostatic — their bulges are frozen-in records of an earlier, faster/closer state.
> We assume **hydrostatic** for our synchronous bodies (no history to fossilize a
> different figure) unless a body's lore implies one; the option is flagged where it
> could matter.

## 4. Regimes by body type

| body class | spin | figure | coefficients |
|---|---|---|---|
| **gas giant / fast free rotator** | fast, free | large oblate | scalar **J₂** (+ J₄ ≈ −4 % J₂, J₆), no tesseral |
| **free rocky** (rare; fast, non-locked) | P_rot | oblate, J₂ ∝ q | scalar **J₂** (tesseral unmeasurable → omit) |
| **synchronous rocky/icy** (much of the roster) | ω = n | **triaxial** | degree-2 full: **C̄₂₀ + C̄₂₂** (J₂ = 10⁄3·C₂₂) |
| **star** | usually slow | nearly round | scalar **J₂** (tiny; omit unless a fast rotator) |

`reference_radius` (the radius the coefficients are scaled to — the **equatorial**
radius for a rotational figure) is mandatory whenever any J₂/geopotential is emitted.
The cfg forms (scalar `j2`, zonal `geopotential_row`, full cos/sin) are tabulated in
[`principia-geopotential-data.md`](principia-geopotential-data.md).

## 5. Worked examples (NearStars roster, Phase 4 active set)

Inputs are the curated mass / radius / rotation; lock state from the
[tidal-locking-timescale method](tidal-locking-timescale-methodology.md).

| body | class | ω source | q (or q_s) | J₂ | C̄₂₂ | note |
|---|---|---|---|---|---|---|
| **Erid** (40 Eri A b) | free rocky | P_rot 5.1 h | **0.056** | **~0.017–0.019** | — | the roster's most oblate rocky body — f ≈ 5 %, an equatorial bulge visible in-game; first-order under-predicts (large q) |
| **Polyphemus** (α Cen A b) | gas giant | P_rot ~10 h | 0.19 | **~0.023–0.026** | — | worked in full in geopotential-data.md (NMoI ~0.23) |
| **TRAPPIST-1 b** | sync. rocky | n (P 1.51 d) | 1.5e-3 | ~1.5e-3 | **~4.6e-4** | close-in lock → real permanent tidal bulge, J₂ ≈ Earth's |
| **Proxima b** | sync. rocky | n (P 11.2 d) | 2.8e-5 | ~2.8e-5 | ~8e-6 | far enough that the figure is tiny (record; C₂₂ likely below emit threshold) |
| **Fomalhaut A** | star (A-type) | fast (A4V) | — | (omit) | — | the one fast-rotating roster star (spin axis measured, Le Bouquin 2009) so physically oblate, but no published oblateness figure — and its J₂ is dynamically irrelevant for the far-out disk / Fomalhaut b orbits (AU-scale). Record the spin pole, omit J₂. Sol-like K/M hosts → J₂ ~10⁻⁷, omit. |

The headline contrast: **Erid** (fast, free, hot super-Earth) is genuinely flattened,
while the locked habitable-zone rockies are nearly round except for a small permanent
tidal C₂₂ that grows sharply the closer the lock (TRAPPIST-1 b ≫ Proxima b). Stars are
point-like at the orbital distances that matter, so their figures are recorded but not emitted.

## 6. Procedure (per body)

1. Determine lock state (tidal-locking-timescale method) → free or synchronous.
2. Compute q (free: P_rot) or q_s (locked: orbital n), using the **equatorial** radius.
3. Pick NMoI from the body class (giant 0.20–0.26; rocky 0.30–0.36; star 0.05–0.08) —
   state the assumption + range.
4. Free rotator → J₂ via Radau–Darwin (Maclaurin q/2 as the homogeneous bound).
   Synchronous → J₂ ≈ (0.9–1.1)·q_s, C̄₂₂ = 0.3·J₂ (hydrostatic).
5. Emit threshold: skip C₂₂ (and J₂) below ~1×10⁻⁶ (record the value, omit the row) —
   it is dynamically irrelevant. Set `reference_radius` = equatorial radius.
6. Write through the **curated source layer**, not `db/systems/*` directly; rebuild.

## 7. Citations

All bibcodes verified against NASA ADS.

- **Helled, Anderson, Schubert & Stevenson 2011**, Icarus 216, 440 (`2011Icar..216..440H`,
  arXiv **1109.1627**) — the Radau–Darwin NMoI ↔ J₂ relation used for the giants; the
  inversion form in §2. Pinned in `principia-geopotential-data.md`.
- **Murray & Dermott 1999**, *Solar System Dynamics* (`1999ssd..book.....M`) §4 — the
  hydrostatic figure of rotating and synchronous bodies; the textbook home of the chain.
- **Tricarico 2014**, ApJ 782, 99 (`2014ApJ...782...99T`) — modern rigorous statement of
  the synchronous figure: J₂/C₂₂ ≈ 10⁄3 and (b−c)/(a−c) ≈ 1⁄4, with the higher-order
  Ω²/(πGρ) corrections. Paired with **Dermott 1979**, Icarus 37, 575 (`1979Icar...37..575D`),
  the classic derivation of satellite shapes and gravitational moments.
- **Chandrasekhar 1969**, *Ellipsoidal Figures of Equilibrium* (`1969efe..book.....C`) —
  Maclaurin spheroids (homogeneous rotational limit, f = 5q/4).
- **Zharkov & Trubitsyn 1978**, *Physics of Planetary Interiors* (`1978ppi..book.....Z`);
  **Hubbard 1984**, *Planetary Interiors* (`1984plin.book.....H`) — theory of figures, the
  q–f–J₂–NMoI chain.
- **Measured synchronous-figure anchors** (the J₂ = 10⁄3·C₂₂ calibration): Io — Anderson
  et al. 2001 (`2001JGR...10632963A`; figure axes a−c = 14.4 km, b−c = 3.6 km → 4:1,
  C/MR² = 0.3769); Europa — Anderson et al. 1998 *Science* four-encounter
  (`1998Sci...281.2019A`); Ganymede — Anderson et al. 1996 (`1996Natur.384..541A`, J₂ & C₂₂
  reported directly); Titan — Iess et al. 2010 *Science* (`2010Sci...327.1367I`; a−c = 410 m,
  b−c = 103 m → ratio 3.98 ≈ 4:1, C/MR² ≈ 0.34). All give J₂/C₂₂ ≈ 10⁄3.
- **Moon — non-hydrostatic / fossil bulge**: GRAIL gravity field, Zuber et al. 2013 *Science*
  (`2013Sci...339..668Z`); the J₂/C₂₂-derived moment of inertia + interior interpretation,
  Williams et al. 2014 (`2014JGRE..119.1546W`, I_s/MR² = 0.392728). J₂/C₂₂ ≈ 9 ≠ 10⁄3.
- **Fomalhaut A spin axis** — Le Bouquin et al. 2009, A&A 498, L41 (`2009A&A...498L..41L`,
  VLTI/AMBER): A4V, spin-axis PA 65° ⊥ the disk — confirms it is a fast rotator with a
  measured pole, though no oblateness figure is published (see §5 note).

## Related

- [`principia-geopotential-data.md`](principia-geopotential-data.md) — verbatim
  Solar-System coefficients, normalization, cfg forms, the Polyphemus giant worked example.
- [`principia-cfg-reference.md`](principia-cfg-reference.md) — the cfg schema (node syntax, units).
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md) — lock state (the figure's spin input).
- [`mass-radius-relation-methodology.md`](mass-radius-relation-methodology.md) — the radius input.
- [`methodology-index.md`](methodology-index.md) — the full methodology index.
