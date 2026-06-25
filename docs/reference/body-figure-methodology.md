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
the Sun's slow spin gives J₂ ≈ 2×10⁻⁷ (one of the roundest bodies known). **The
Sun row is the *measured* value** — the Radau–Darwin inversion is only valid for
NMoI ≳ 0.13 and returns a spurious (negative) J₂ at stellar central condensation
(NMoI ~0.05–0.08), so stars are not run through it: they are recorded as negligible
and never emitted (slow rotators all fall below the ~10⁻⁶ threshold).

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

**Near–far asymmetry (octupole / teardrop).** The two tidal bulges are equal only at
degree 2 (C̄₂₂, an even P₂ deformation). The next tidal term is the **odd P₃ octupole**:
the primary's pull is stronger on the near side, so the **sub-primary bulge is slightly
larger than the anti-primary one** — a faint teardrop/pear shape (pointier toward the
primary). The asymmetry scales as ≈ **R/a** (body radius / orbital distance) times the
quadrupole bulge — sub-percent here (Dante R/a ≈ 0.8 %, Hades ≈ 0.5 %), so it is
**recorded, not emitted by default**. Notes: (1) gravity-side it is a **degree-3** term,
dynamically negligible; (2) it is **not representable by the symmetric `CustomEllipsoid`**
mesh — a visual teardrop would need a small degree-3 **heightmap** bump at the terrain pass.
Real echo: the Moon's center of figure is offset toward Earth.

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

## 5. High-degree geoid for rocky bodies — synthetic now, heightmap later

§2–§3 fix the **degree-2** figure (rotation + tide) deterministically. Real rocky
bodies also carry a *lumpy* degree-3+ field — the gravitational fingerprint of their
unique interior density anomalies and topography (Earth's, the Moon's mascons, Mars's
Tharsis). A fictional body has no such measured fingerprint, and only **four** Solar-
System bodies even have a rich high-degree field to imitate (Earth deg 2159, Moon 900,
Mars 120, Venus 180; the Galilean moons, Titan and Enceladus are effectively degree-2
only). So a complex geoid must be **synthesized**, not looked up. Two stages:

**Stage A — Kaula-spectrum synthetic field (now).** Real planetary gravity spectra obey
**Kaula's rule** (Kaula 1966): the per-coefficient RMS of the fully-normalized harmonics
falls as a power law,

    s_n  =  rms(C̄ₙₘ, S̄ₙₘ)  ≈  K / n²        (Earth: K ≈ 1×10⁻⁵)

→ degree variance σ²ₙ = (2n+1)·s²ₙ ∝ 1/n³. To synthesize a body's geoid:

1. **Keep degree 2 from §2–§3** — J̄₂₀ = −J₂/√5 (and C̄₂₂ for locked bodies) stay the
   grounded rotational/tidal values; only degree ≥ 3 is synthesized.
2. For each n = 3…N_max, m = 0…n, draw C̄ₙₘ, S̄ₙₘ ~ Gaussian(0, s_n), s_n = K/n².
3. **Seed the RNG deterministically per body** (name hash) — same body → same field,
   preserving the reproducibility invariant; flag it `synthetic` in the curated layer.
4. **Calibrate K to the body class.** Earth (active tectonics) ≈ 1×10⁻⁵; airless,
   uneroded, mascon-rich bodies (Moon/Mercury-like) are *rougher* → larger K (the GRAIL
   team applies the Moon its own Kaula constraint); small differentiated/icy bodies fall
   off faster. K is the one tunable; state it.
5. **N_max ≈ 8–10** — enough for realistic low-orbit perturbation (Principia's bundled
   Earth is truncated at degree 10); higher degrees are dynamically irrelevant except at
   the surface. Emit as full cos/sin `geopotential_row`, `reference_radius` = R_eq.

This gives statistically Earth-like lumpiness — and the mascon-like low-orbit dynamics
(unstable / frozen low orbits over airless bodies) that make it worth doing — while being
honestly **synthesis-grade**: not tied to anything visible.

**Stage B — heightmap-derived field (at the terrain pass).** Once a body's terrain
(PQS/Parallax heightmap) exists, the degree-3+ field is *recomputed* from the topography
under Airy/Pratt isostatic compensation (gravity-topography admittance — Wieczorek's
Treatise method, standard practice; EGM2008 itself fills data-poor regions this way). The
result is **self-consistent with the visible mountains/basins** and **replaces** the Kaula
placeholder. Degree 2 (rotation/tide) is unchanged across both stages. Roadmap:
**degree 2 permanent · degree 3+ Kaula-now → heightmap-later.**

**Visual shape emit (Kopernicus).** J₂/C₂₂ are the *gravity* figure (Principia); the
*visible* shape is a separate mesh. The **VertexHeightOblateAdvanced** PQS Mod (James Glaze,
MIT) renders a body as an oblate/triaxial ellipsoid via `oblateMode = CustomEllipsoid` with
a:b:c ratios. From the degree-2 figure, normalized to the polar axis (c = 1): a triaxial
(synchronous, hydrostatic 4:1) body → a/R = 1 + 7J₂/3, b/R = 1 − 2J₂/3, c/R = 1 − 5J₂/3
(then ÷c); a free oblate rotator → a = b, c = R(1 − f). `scripts/refs/body_figure.py` →
`ellipsoid_ratios()` emits them — so one figure drives both the gravity and the visual,
automatically consistent. **Volume must be conserved** — the physical figure bulges one axis
while the others *contract* (Σ deviations ≈ 0). The c = 1-normalized a:b:c are all ≥ 1, so they
**inflate** the body by a·b·c (Dante ×1.22) unless the **`reference_radius` is set to the polar
radius** (= mean radius × c_physical), not the mean radius. Set reference_radius = polar; then
the ≥ 1 ratios reproduce the volume-preserving shape. **Hard dependency** (a body using the node
won't render its shape without the plugin), pulled in only by the bodies that emit a visible
figure (a/c ≳ 1.02); the cfg node + schema live in the `kopernicus-cfg` skill (filled at the emit stage).

## 6. Worked examples (NearStars roster, Phase 4 active set)

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

## 7. Procedure (per body)

1. Determine lock state (tidal-locking-timescale method) → free or synchronous.
2. Compute q (free: P_rot) or q_s (locked: orbital n), using the **mean** radius
   (Helled+2011 convention; the emit `reference_radius` is the equatorial radius).
3. Pick NMoI from the body class (giant 0.20–0.26; rocky 0.30–0.36; star 0.05–0.08) —
   state the assumption + range.
4. Free rotator → J₂ via Radau–Darwin (Maclaurin q/2 as the homogeneous bound).
   Synchronous → J₂ ≈ (0.9–1.1)·q_s, C̄₂₂ = 0.3·J₂ (hydrostatic).
5. **Rocky body wanting a complex geoid** → synthesize degree 3+ via Kaula (§5), seeded
   per body + flagged `synthetic`; keep the degree-2 from steps 4. Replace at the terrain pass.
6. Emit threshold: skip C₂₂ (and J₂) below ~1×10⁻⁶ (record the value, omit the row) —
   it is dynamically irrelevant. Set `reference_radius` = equatorial radius.
7. Write through the **curated source layer**, not `db/systems/*` directly; rebuild.

## 8. Citations

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
  measured pole, though no oblateness figure is published (see §6 note).
- **Synthetic high-degree field (§5)**: Kaula 1966, *Theory of Satellite Geodesy*
  (`1966tsga.book.....K`) — the degree-variance power law (Earth RMS ≈ 1×10⁻⁵/n²); GRAIL
  applies the Moon its own Kaula constraint (Lemoine et al. 2013, `2013JGRE..118.1676L`),
  confirming per-body recalibration. Heightmap→gravity (Stage B): Wieczorek, *Gravity and
  Topography of the Terrestrial Planets*, Treatise on Geophysics (`2015trge.book..153W`;
  orig. `2007plmo.book..165W`) — Airy/Pratt isostasy + gravity-topography admittance.

## Appendix — measured Solar-System gravity fields (analogs)

Reference anchors for the figure recipe and the Kaula calibration. "deg" = max recovered
spherical-harmonic degree; only Earth/Moon/Mars/Venus carry a genuinely *rich* high-degree
field (everything else is degree-2 to low-degree, recovered from flybys).

| body | model | deg | J₂ / C₂₂ (×10⁻⁶) | bibcode | dominant signal |
|---|---|---|---|---|---|
| Earth | EGM2008 | 2159 | 1082.6 / 1.57 | `2012JGRB..117.4406P` | the rich-geoid anchor (K ≈ 1e-5) |
| Moon | GL0900 / GRGM900 | 900 | (in model) | `2014GeoRL..41.1452K`, `2013JGRE..118.1676L` | **mascons** → unstable low orbits; own Kaula constant |
| Mars | MRO120D / GMM-3 | 120 | (in model) | `2016Icar..274..253K`, `2016Icar..272..228G` | Tharsis; high gravity-topo correlation |
| Venus | MGNP180U | 180 | (in model) | `1999Icar..139....3K` | very high gravity-topo correlation (thick lithosphere) |
| Mercury | HgM005 | 50 | (in model) | `2014JGRE..119.2417M`, `2019GeoRL..46.3625G` | low-degree; k₂ = 0.451 |
| Io | Galileo | 2 | hydrostatic | `1996Sci...272..709A` | degree-2 only |
| Europa | Galileo | 2 | hydrostatic | `1998Sci...281.2019A` | degree-2 only |
| Ganymede | Galileo / +Juno | 2 | (1996 model) | `1996Natur.384..541A`, `2022GeoRL..4999475G` | degree-2; Juno hints at regional anomalies |
| Callisto | Galileo | 2 | **32.7 / 10.2** | `2001Icar..153..157A` | degree-2; C/MR² = 0.355, partially differentiated |
| Titan | Cassini | 3 | k₂ ≈ 0.6 | `2012Sci...337..457I` | tidal → subsurface ocean |
| Enceladus | Cassini | 3 | **5435 / 1550** | `2014Sci...344...78I` | J₂/C₂₂ = 3.51, mildly non-hydrostatic (S-polar sea) |
| Vesta | Dawn | 20 | (in model) | `2014Icar..240..103K` | non-hydrostatic (Rheasilvia) |
| Ceres | Dawn | ~16 | hydrostatic | `2016Natur.537..515P` | isostatically compensated; MoI 0.37 |

## Related

- [`principia-geopotential-data.md`](principia-geopotential-data.md) — verbatim
  Solar-System coefficients, normalization, cfg forms, the Polyphemus giant worked example.
- [`principia-cfg-reference.md`](principia-cfg-reference.md) — the cfg schema (node syntax, units).
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md) — lock state (the figure's spin input).
- [`mass-radius-relation-methodology.md`](mass-radius-relation-methodology.md) — the radius input.
- [`methodology-index.md`](methodology-index.md) — the full methodology index.
