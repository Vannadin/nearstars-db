<!-- 조석 감쇠된 천체의 평형 자전축 기울기(Cassini state obliquity)를 근거화 계산해 "고정=obliquity 0" 가정을 실제 평형값으로 대체하는 방법 -->
# Cassini-state obliquity — equilibrium spin-axis tilt of a damped body

Method reference for the **equilibrium obliquity ε** of a body whose spin has been
tidally damped into a **Cassini state**. It replaces the lazy "tidally locked ⟹
obliquity = 0 exactly" assumption with the true Cassini-state value — which is
**small but non-zero** for every well-measured synchronous body, and can be
*large* when a secular spin–orbit resonance intervenes.

Companion to [`body-figure-methodology.md`](body-figure-methodology.md) (supplies
the figure coefficients J₂, C̄₂₂) and
[`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md)
(supplies the lock state that makes the body a Cassini candidate).

> Discipline. The Cassini framework is textbook celestial mechanics
> (Colombo–Peale–Ward), stated as such and cited to the standard reference. What
> gets grounded on ADS: the **calibration anchors** (measured Cassini obliquities
> — Mercury, Titan, the Galileans) and the precession-constant coefficient for the
> synchronous case. Two coefficients are carried with an explicit uncertainty flag
> (§3, §6) rather than over-claimed.

## 1. What a Cassini state is

The primary (star, or planet for a moon) torques the body's rotational + tidal
bulge, so the **spin axis ŝ precesses about the orbit normal n̂** at a rate set by
the precession constant α. Meanwhile n̂ itself **precesses about the Laplace pole
k̂** at the orbital nodal rate g, holding a fixed inclination I. A **Cassini state**
is the equilibrium in the frame co-precessing with the orbit: ŝ, n̂, k̂ stay
**coplanar and precess together at the common rate g** (Colombo 1966
`1966AJ.....71..891C`; Peale 1969 `1969AJ.....74..483P`). Tidal dissipation shifts
ŝ slightly *out* of that plane (Su & Lai 2022 `2022MNRAS.509.3301S`).

There are up to **four** states (Peale 1969):

- **State 1** — low obliquity, ŝ near n̂. The branch a quietly tidally-damped body
  reaches. **This is the NearStars default for a locked body.**
- **State 2** — obliquity on the far side of the Laplace pole; **can be large**
  (tens of degrees); the other stable end-state.
- **States 3 & 4** — unstable.

Under dissipation only **states 1 and 2 are attractors** (Ward 1975
`1975AJ.....80...64W`). A body damped from near ε = 0 lands in **state 1**; a body
caught in / migrated through a secular spin–orbit resonance can be captured into
**state 2** at high obliquity (Millholland & Laughlin 2019 `2019NatAs...3..424M`).

## 2. Equilibrium-obliquity relation

With ε = obliquity (∠ ŝ,n̂), I = orbit inclination to the Laplace plane, g = Ω̇ < 0
the nodal precession rate, α > 0 the spin precession constant, the Cassini states
satisfy (Peale 1969 `1969AJ.....74..483P`; Ward & Hamilton 2004 `2004AJ....128.2501W`):

    α · cos ε · sin ε  +  g · sin(ε − I)  =  0                    (1)

**Number of roots** is set by |g|/α against a critical ratio (Henrard 1987
`1987CeMec..40..345H`; Ward & Hamilton 2004):

    (|g|/α)_crit = ( sin^(2/3) I + cos^(2/3) I )^(3/2)            (2)

|g|/α < crit → 4 roots (states 1–4); |g|/α > crit → 2 roots (states 2 & 3), state 1
having merged with state 4 and vanished. In the small-I limit (2) reduces to
|g|/α ≈ 1. *(The exact exponent grouping of (2) was an image in the cached source;
for the resonance flag the small-I form |g|/α ≈ 1 is all we need — verify the full
expression in Ward & Hamilton 2004 before quoting it.)*

**Small-angle State-1 solution** (ε, I small; Ward 1975; Fabrycky+ 2007
`2007ApJ...665..754F`):

    ε₁  ≈  |g| sin I / ( α + |g| cos I )                          (3)
    α ≫ |g|  ⟹  ε₁ ≈ (|g|/α) sin I  →  0                          (4)

**(4) is the key result for locked bodies**: when the bulge-driven spin precession
α greatly exceeds the orbital nodal rate |g|, the equilibrium obliquity is
suppressed to a *small but non-zero* value ≈ (|g|/α)·sin I — **not exactly zero**.
It becomes large only near the resonance |g|/α ~ 1 (state 2).

## 3. The precession constant α

**Free / fast rotator** (Néron de Surgy & Laskar 1997 `1997A&A...318..975N`;
Ward 1975), with n² = G M⋆ / a³ and the identity (C−A) = J₂·M R²:

    α = (3/2) · (n²/ω) · [ J₂ / (C/MR²) ] · (1−e²)^(−3/2)         (5)

Sanity check: Earth's solar-torque α from (5) (J₂ = 1.08e-3, C/MR² = 0.331,
ω = 2π/day, n = 2π/yr) ≈ 17″/yr, matching the known ~16″/yr solar contribution to
lunisolar precession.

**Synchronously locked body** (ω = n) — **the case NearStars needs**. The body is
triaxial (A < B < C); with hydrostatic figure coefficients J₂ and C̄₂₂ and
normalized MoI C̃ ≡ C/MR², the satellite literature (Bills 2005
`2005Icar..175..233B`; Baland+ 2011 `2011A&A...530A.141B`) uses:

    α_syn = (3/2) · n · ( J₂ + C̄₂₂ ) / (C/MR²)                    (6)

> **Coefficient caveat.** The rigid polar combination is (C−A)/C = (J₂ + 2C̄₂₂)/C̃;
> the benchmarked satellite-obliquity papers use (J₂ + C̄₂₂)/C̃ (6). For a
> hydrostatic synchronous body C̄₂₂ = 0.3·J₂, so the two differ by 1.3 J₂ vs 1.6 J₂
> — a ~20 % spread in α, hence ~20 % in ε. **Adopt (6) (Baland/Bills)** since those
> are calibrated on measured moons; carry the ±20 % as a modeling systematic, and
> confirm the exact coefficient in `2011A&A...530A.141B` / `2005Icar..175..233B`
> at point of use.

Because ω = n makes n²/ω = n, the locked α is far smaller than a fast rotator's,
and scales with (J₂ + C̄₂₂), which for a locked body *grows* as the orbit tightens
(figure doc §3: J₂ ≈ q_s, C̄₂₂ ≈ 0.3 J₂). So **the tightest locks are the
roundest-spun → smallest ε₁** — unless a resonance intervenes.

## 4. Getting the orbital nodal rate g

**(a) Planet in a multi-planet system — Laplace–Lagrange secular theory**
(Murray & Dermott 1999 `1999ssd..book.....M`, ch. 7). The nodal frequencies {g_i}
are eigenvalues of the inclination interaction matrix B; leading order:

    B_jk = +(1/4) n_j · [m_k/(M⋆+m_j)] · α_jk · ᾱ_jk · b^(1)_{3/2}(α_jk)
    B_jj = −Σ_{k≠j} B_jk

α_jk = ratio of semi-major axes (smaller/larger), b^(1)_{3/2} a Laplace
coefficient. **Inputs**: neighbor masses + semi-major axes + host mass. Use the
dominant mode's {g, I}. **For resonant chains** (e.g. TRAPPIST-1) Laplace–Lagrange
breaks down → use direct **N-body nodal frequency analysis** (Millholland+ 2024
`2024ApJ...961..203M`, [arXiv:2311.17908](https://arxiv.org/abs/2311.17908)).

**(b) Close-in moon — driven by the planet's oblateness J₂** (Murray & Dermott 1999):

    |g| = |Ω̇| ≈ (3/2) · J₂,planet · (R_planet/a)² · n · cos i     (7)

plus star and other-satellite/ring terms; the moon's Laplace-plane inclination I is
the balance between the planet's equator (J₂ term, dominant when close) and the
orbit about the star. **Inputs**: planet J₂, R_planet, moon a and n, other moons.

## 5. Calibration anchors (verify the recipe here first)

| body | state | measured obliquity | source | hydrostatic recipe reproduces? |
|---|---|---|---|---|
| **Mercury** (3:2) | 1 | **2.11 ± 0.1 arcmin** (0.035°) | `2007Sci...316..710M` Margot+ 2007 | **Yes** — Cassini relation + measured ε is *how* C/MR² is inferred; self-consistent with J₂, C₂₂ (`2009CeMDA.105..329M`). |
| **Moon** | **2** | 6.7° to ecliptic (≈1.54° to Laplace plane) | `1975Sci...189..377W` Ward 1975 | Framework **yes**, figure **no** — genuine state-2 value from a Cassini-state transition, but the Moon's **fossil bulge** (J₂/C₂₂≈9≠10/3) breaks the hydrostatic α. Fossil flag. |
| **Titan** | 1 | ≈0.3° | `2010AJ....139..311S` Stiles+ 2010 | **No** — rigid Titan under-predicts ~2–3×; the value needs a **subsurface ocean** (Cassini-state resonance of the shell), Baland+ 2011 `2011A&A...530A.141B`. Non-rigid flag. |
| **Io–Callisto** | 1 | ≈10⁻³–10⁻² deg (small, non-zero) | `2005Icar..175..233B` Bills 2005 | **Yes** (rigid); a liquid layer shifts them (`2012Icar..220..435B`). Confirms **locked ≠ 0**. |
| **Enceladus** | 1 | ≈0.0015° (rigid) | `2016Icar..268...12B` Baland+ 2016 | **Yes**; stays ≪ 0.05° even with an ocean (`2011Icar..214..779C`). |

**Headline**: every well-measured synchronous body sits in a *non-zero* Cassini
state 1 (Mercury 0.035°, Galileans 10⁻³–10⁻² deg, Titan 0.3° with ocean) —
**"exactly 0" is never right**, but the magnitude is sub-degree unless a resonance
(Moon = state 2) or a decoupled ocean (Titan) intervenes.

## 6. Regime guidance / expected magnitudes

- **Close-in rocky planet, a ≈ 0.03–0.05 AU around an M dwarf** (Proxima b-like,
  TRAPPIST-1-like): tight lock → large J₂+C₂₂ → large α_syn → by (4) **ε₁ is
  sub-degree** away from the |g|/α ≈ 1 resonance. Millholland+ 2024 find TRAPPIST-1
  planets most likely ε ≈ 0, **planet d the possible exception**. Default: compute
  ε ≈ 0.01–1°, not assumed zero.
- **Resonance-enhanced state 2 is real.** Guerrero+ 2024 `2024ApJ...975..256G`: of
  280 known M-dwarf multiplanet systems, **~75 % of planets *could* be captured
  into a stable high-obliquity state 2**, breaking effective locking and giving a
  real day/night cycle — a *gameplay-interesting* (interesting-first) branch. Flag
  per body whether |g|/α is near crit (2); if so a documented ε of tens of degrees
  is defensible.
- **Close-in ice moon, a ~ 4 R_p from a mini-Neptune (~950 km body)**: g from the
  planet's J₂ (7) is fast; α_syn small. Expect **sub-degree state-1 obliquity** like
  the Galileans (10⁻³–10⁻² deg), **unless** a subsurface ocean amplifies it toward
  Titan-like ~0.1–0.3° (a documented-divergence option). Check |g|/α for resonance.

## 7. Inputs needed per body (checklist)

From the figure doc + curated DB:
- **J₂** and, for locked bodies, **C̄₂₂**  · **C/MR²** (body class) · **spin ω**
  (= n if synchronous) and **mean motion n** · **e, a, host mass M⋆**.

For g:
- planet case: **masses + semi-major axes of neighboring planets** → Laplace–Lagrange
  dominant nodal mode {g, I} (or N-body frequency analysis for resonant chains);
- moon case: **planet J₂, R_planet, moon a, other moons/rings** → (7) + the moon's
  Laplace-plane I.

Then: α from (5) free or (6) locked → solve (1) for the state-1 root ((3)/(4) as the
small-angle check) → report ε. Test |g|/α against (2) to flag whether a large
state-2 solution exists.

## 8. Caveats (honest)

1. **Synchronous α coefficient** — (6) (J₂+C̄₂₂)/C̃ per Baland/Bills vs rigid
   (J₂+2C̄₂₂)/C̃: ~20 % spread; adopt Baland/Bills, carry the systematic.
2. **Critical-ratio (2) exact form** — small-I limit |g|/α ≈ 1 is robust; verify the
   full expression in Ward & Hamilton 2004 before quoting.
3. **Fossil bulges** (Moon, Mercury figure) — hydrostatic α is wrong when the figure
   is frozen; reuse the figure doc's fossil-bulge flag.
4. **Non-rigid amplification** (Titan) — a subsurface ocean can multiply ε by 2–3×;
   a documented option, not the default.
5. **Unknown g** — a poorly-constrained companion set leaves g (and ε) uncertain;
   state the assumed neighbors. Resonant chains *require* N-body frequency analysis.
6. **State 1 vs 2 is history-dependent** — dissipation selects state 1 by default,
   but resonance/migration capture into state 2 is plausible for ~75 % of M-dwarf
   planets (Guerrero 2024) — an interesting-first branch worth offering at Phase 4.

## Related

- [`body-figure-methodology.md`](body-figure-methodology.md) — §3 supplies J₂ and
  the tidal C̄₂₂ that feed the precession constant (6).
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md)
  — whether the body is locked (a Cassini candidate) at all.
- [`principia-geopotential-data.md`](principia-geopotential-data.md) — the cfg form
  of J₂/C₂₂; spin-axis orientation feeds the Principia/Kopernicus pole.
- [`methodology-index.md`](methodology-index.md) — the full methodology index.
