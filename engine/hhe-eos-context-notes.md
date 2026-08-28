<!-- 수소-헬륨 외피 상태방정식 — 조사 과정과 판단의 근거 -->
# H/He envelope EOS — context notes

## The (A)/(B)/(C) question, answered before any code: **(A)**

**(A) is live. The tables are distributed, reachable, and in the form this solver wants.**

The paper's stated address (`perso.ens-lyon.fr/gilles.chabrier/DirEOS`) is a directory
listing carrying two archives, `DirEOS2019.tar.gz` (12.0 MB) and `DirEOS2021.tar.gz`
(16.4 MB). The 2019 archive unpacks to eight tables plus a README:

| file | what |
|---|---|
| `TABLE_H_TP_v1`, `TABLE_HE_TP_v1` | pure H, pure He, in (log T, log P) |
| `TABLE_H_Trho_v1`, `TABLE_HE_Trho_v1` | the same in (log T, log ρ) |
| `TABLEEOS_HHE_TP_IVL_Y0.275_v1` | **the mixture, Y = 0.275, Z = 0, in (log T, log P)** |
| `TABLEEOS_HHE_TP_IVL_Y0.292_v1` | the mixture at Y_eff = 0.292, which folds Z = 0.017 in |
| `TABLEEOS_HHE_Trho_IVL_Y0.275_v1`, `…Y0.292…` | the same two in (log T, log ρ) |

The README names the publication (Chabrier, Mazevet & Soubiran 2019, ApJ 872, 51), states
the grid (121 isotherms log T = 2.0 … 8.0 by 0.05; 441 pressures log P = −9 … +13 by 0.05,
in GPa), and the units. Ten columns per row; the two this recipe needs are **log ρ** and
**grad_ad**.

So (B) never has to be attempted. The reconstruction route would have needed Chabrier &
Potekhin 1998 for the functional form, Caillabet+ 2011 eq. (24) for the fit, and a
numerical statement of the d(ρ) revision that Chabrier+ 2019 describes only in words — the
exact shape that stopped ammonia and methane. It is moot: the published numbers are here.

## Three decisions the tables force, recorded before writing code

### 1. Y = 0.275, not Y = 0.292 — this is the double-counting trap

The archive offers the mixture at two helium fractions and the README says what they are:
"2 helium mass fractions: Y=0.275 (Z=0) and Y=Y_eff=0.292 (Z=0.017)". The second is not a
different helium abundance; it is the first with a metal mass fraction *folded into the
helium* so that a two-component table can stand in for a three-component mixture.

This repository already carries `envelope_z` as a declared metal mass fraction and mixes it
into the envelope with the additive volume law. Taking Y_eff = 0.292 **and** applying
`envelope_z` on top would put the metals in twice. That is trap three, and it is the same
shape as the two the repository has already walked into (Jupiter's Z, Earth's geotherm).

So the material is the Z = 0 table, and the metals stay where they already are.

### 2. The table hands over grad_ad, so the adiabat stops being reconstructed

Column ten is ∇_ad = (∂ ln T / ∂ ln P)_S, computed by the authors from their own entropy.
`interior.py` currently builds its adiabatic gradient out of γ = (∂P/∂T)_V/(ρ c_V) and
K_S, because that is all a Birch-Murnaghan phase can offer. Here the published quantity is
the gradient itself, and using it is strictly better than rebuilding it: dT/dP = ∇_ad·T/P.

This is what closes the temperature hole. `hhe_n1` had no thermal constants at all, so
`cold_phases()` named it and the potential temperature landed on top of the ice mantle
rather than on the surface.

### 3. The distributed table has flaws inside the planetary rectangle, and they are named

The README says so up front: "numerical oscillations or flaws in the calculations of the
various thermodynamic quantities are expected", and separately that values "in the solid
phase or beyond the limit of the first order quantum correction for the ions are
unphysical". Measured over log T ∈ [2.0, 4.4] × log P ∈ [−4, 4] (the planetary rectangle,
49 × 161 = 7889 cells) in the Y = 0.275 (log T, log P) table:

* **7 cells carry a sentinel** log ρ = −8.8603 where a density belongs. All seven sit at
  500–710 K and 8–225 GPa — the pressure-dissociation region at low temperature. The same
  seven places show up in the Y = 0.292 table as a *non-monotonic* log ρ instead, and in the
  primary (log T, log ρ) table as seven cells where log P falls as density rises, which is
  thermodynamically impossible. So it is one flaw seen three ways, not three flaws.
* **887 cells (11 %) have grad_ad pinned at exactly 0.1 or exactly 0.5**, the two ends of a
  clamp. All are at T ≤ 3550 K, concentrated at low temperature.

Neither region is reachable by a convective giant envelope. Integrating the table's own
grad_ad outward from 1 bar gives, for the coldest start anyone would declare:

| adiabat from | at 1 GPa | at 100 GPa |
|---|---|---|
| 60 K at 1 bar | 945 K | 2371 K |
| 100 K at 1 bar | 1520 K | 3829 K |
| 165 K at 1 bar (Jupiter) | 2359 K | 5634 K |

The flawed cells are several times colder than that at the same pressure. So the answer is
not to repair published numbers, it is to **declare the reachable region and decline
outside it** — the same move `t_max` makes for ice VII.

## What could not be coarsened, and why the table is stored at native resolution

The obvious economy — keep every second node and interpolate — does not survive
measurement. Against the distributed values over the same rectangle:

| grid | nodes | worst |Δρ|/ρ | rms |
|---|---|---|---|
| native, 0.05 dex | 49 × 161 | 2.1×10⁻⁴ | 1.8×10⁻⁵ |
| every 2nd, 0.10 dex | 25 × 81 | 3.2×10⁻¹ | 1.9×10⁻² |
| every 4th, 0.20 dex | 13 × 41 | 2.3×10⁻¹ | 2.0×10⁻² |

The worst coarse-grid errors are not spread out; they sit at **112 K and 200–500 bar**,
where molecular hydrogen is near its own condensation line and the surface has real
structure. Median error at half resolution is still only 2.8×10⁻⁵, but a 30 % error
anywhere in a table is not a table. Native resolution it is.

## What the four giants measured, with the table in

All four use the **1-bar temperature** as the declared potential temperature, which is what
the boundary condition now means: a gas has no P = 0 surface, so the integration stops at
the table's pressure floor (1 bar) and that is the level the published radii are quoted at.

| body | before | after | T_c derived | T_c published |
|---|---|---|---|---|
| Jupiter (T = 165 K at 1 bar) | +0.6 % | **−0.69 %** | 14 490 K | ~20 000 K |
| Saturn, Z = 0 (135 K) | +20.7 % | **+2.09 %** | 4 800 K | — |
| Uranus (76 K) | +23.8 % | **+5.4 %** | 6 150 K | 5 700 K (Scheibe+ 2019) |
| Neptune (72 K) | +29.2 % | **declines** | — | 5 500 K |

Radii are against the IAU mean radius, the comparison the giant tests already use.

**Jupiter got slightly worse and that was expected.** The +0.6 % was the result of a
constant fitted to Jupiter; −0.69 % is what a published mixture EOS says about the same
planet with no freedom left. The sign flipped and the magnitude is the same, which is the
best evidence that the old agreement was a fit rather than a prediction.

**Neptune now declines for a different reason, and it is a three-kelvin miss.** Its ice
mantle top comes out at 1797 K against the 1800 K floor of the hot-water EOS (Mazevet+ 2019,
whose §3.1 sets that floor itself). So the two fluid EOS this recipe carries — H/He down to
100 K, water up from 1800 K — leave a seam, and Neptune sits three kelvin inside it. That is
a domain row, not a failure of the envelope.

**The unresolved-2 question is half closed.** Uranus's central temperature moves from being
untestable (the old branch had no envelope temperature at all) to 6150 K against Scheibe+
2019's 5700 K, an 8 % overshoot in the same direction as its 5.4 % radius. Neptune cannot be
re-measured until the seam above is dealt with, so its gap is neither confirmed nor closed.

## Open defect: the Z-loaded envelope does not converge reliably

Saturn with `envelope_z > 0` is not trustworthy yet, and the reason is structural rather
than numerical.

Fixing the surface at 1 bar instead of at P = 0 makes the surface mass **non-monotonic in
central pressure**. Measured on Saturn at Z = 0.02, marching the central pressure by decades:

| P_c | 10⁸ | 10⁹ | 10¹⁰ | 10¹¹ | 10¹² |
|---|---|---|---|---|---|
| surface mass (10²⁶ kg) | 2.79 | 0.93 | 0.84 | 2.09 | 8.07 |
| radius (10⁴ km) | 48.0 | 15.1 | 6.85 | 5.69 | 5.96 |

There are two roots. The physical one is the compact branch on the right; the left branch is
a body puffed out to hundreds of thousands of kilometres whose 1-bar surface still encloses
the target mass. The secant's second probe used to be `hi × 10⁻³`, which lands on the
spurious branch, and the shoot then reported a 6.5-million-kilometre Saturn with
`converged=True`. Moving that probe to `hi / 4` when a gas is outermost fixes the worst of
it, but Z = 0.05 still lands at +43 % and Z ≥ 0.10 runs the temperature loop into the
table's upper wall.

**What it needs is a root selector, not a tolerance.** The right guard is to verify after
convergence that the mass still rises with the central pressure and to decline otherwise —
one extra integration, paid only when a gas is outermost. That is the next thing to write.

Until it exists, **Saturn's fitting Z has not been measured** and the question the brief
asked — where inside the Guillot budget it moves — is open. What is known is the direction:
Z = 0 now gives +2.09 % instead of +20.7 %, so whatever the fitting Z turns out to be, it is
far below the 0.200 the polytrope needed. The old value was compensating for the envelope,
exactly as the brief suspected.

## Cost

| body | before | table only | final (c_P-weighted mixture, converged badge) |
|---|---|---|---|
| Jupiter | ~0.2 s | 2.3 s | **5.4 s** |
| Saturn | ~0.2 s | 2.9 s | – |
| Uranus | 24–500 s | 148 s | **1038 s** |

The middle column is what this section first reported; the last column is what the
checklist measured at the end, after the mixture's adiabatic gradient became c_P-weighted
and `converged` started covering the temperature boundary condition — so solutions that
used to leave unconverged now iterate until they converge. The final numbers are the ones
to plan against (`speed-context-notes.md` takes them up).

One table lookup is 2.2 µs (bicubic, 16 nodes, pure Python), against roughly 0.5 µs for the
polytrope's closed form. That alone does not explain the ice giant; the iteration count does.

---

# 2026-08-28, later: two corrections from the owner, and what they turned up

## Neptune was a dispatch bug, and the fall-through would have been wrong anyway

The note above called the 3 K miss a seam between two EOS. That was wrong. The two water
materials **meet exactly**: `h2o` runs 20–1800 K, `h2o_hot` runs 1800 K up, and the ice X
work made that deliberate — a gate still checks it ("온도 축에 틈이 없다"). 1797 K is
inside the condensed ladder's declared domain.

The real cause is one line, `interior.py:960`:

    ice_material = "h2o_hot" if body_class in ICE_GIANT_CLASSES else "h2o"

The material is chosen by **class**, never by the local (P, T). So Neptune asks hot water a
question 3 K below its floor, and hot water refuses correctly.

**But the obvious repair — fall through to `h2o` near the boundary — would be wrong, and
that is the finding.** Before dispatching by (P, T) the question is whether 1797 K at
Neptune's envelope base is physically a condensed phase. It is not:

* The repository's own melting curve stops long before. IAPWS equation (5) ends at 715 K,
  which is 20.6 GPa, and `melt_free_phases()` already names `ice_x` as carrying no curve at
  all. So between 715 K and the superionic floor this recipe **has no curve** that separates
  solid from fluid.
* `ICE_VII_X_T_MAX = 1800 K` is not a phase boundary. It is the knot ceiling of SeaFreeze's
  `VII_X_French` representation, and `eos.py` says so where `t_max` is defined: it "말하지,
  물질이 어디서 상을 바꾸는가를 말하지 않는다" — it states where a fit is valid, not where
  the substance changes phase.
* Neptune's envelope base sits at tens of GPa. Water's melting line there is roughly a
  thousand kelvin, far below 1797 K, and Millot+ 2019 puts superionic water above 2000 K and
  100 GPa. Between those, water at these conditions is **fluid**.

So the ladder would hand Neptune an ice VII density where the physics says liquid. Two
consequences, and both are results rather than repairs:

1. Dispatching by (P, T) is right in principle but cannot use 1800 K as the switch, because
   1800 K is a fit ceiling and the phase boundary is somewhere else and lower.
2. **The 1800 K boundary is itself up for review**, which is the outcome the brief named. What
   is missing is a melting curve between 20.6 GPa and the superionic field — the same gap
   `melt_free_phases()` has been naming since the ice X work.

Neptune is therefore still declined, but for a stated reason one layer deeper than before.

## The Saturn selector: the diagnosis was right and `hi / 4` was not a fix

Owner's reading is correct and the arithmetic confirms it. The ×4 ladder climbs from a seed
until the surface mass reaches the target; with `lo` pinned at the floor the resulting
bracket **contains the minimum**, so there are two roots inside it and the secant's second
probe decides which one is found. `hi × 10⁻³` landed left, `hi / 4` landed right — neither
is a principle, which is why Z = 0.05 was still 43 % out.

What is in the tree now uses the ladder itself: `lo` becomes **the last rung whose surface
mass fell short of the target**. That rung is always at or past the minimum — on the falling
branch the mass keeps dropping, so if any rung is below target the last such rung cannot be
left of the minimum. The rung's mass is already computed, so the secant gets both of its
points for free and no integration is added.

| Saturn, envelope Z | 0.00 | 0.02 | 0.05 | 0.10 | 0.20 |
|---|---|---|---|---|---|
| radius vs IAU mean | **+2.09 %** | +11066 % | −5.03 % | −5.73 % | −13.60 % |

Monotone except Z = 0.02, and that one exposes the remaining case: when the ladder's **first**
rung already exceeds the target, no rung is recorded and the bracket falls back to the old
behaviour. Three attempts at that case (walking down past the minimum; refusing to break
until the mass turns up) each moved the failure somewhere else and the third broke Jupiter
outright, so they were reverted. The case is small and precisely stated, which is a better
place to leave it than a fourth guess.

## The three Z = 0 numbers were re-measured with the selector in, and did not move

This was the owner's most important request, and it holds.

| body | before the selector | after |
|---|---|---|
| Jupiter | −0.69 % | **−0.69 %** |
| Saturn, Z = 0 | +2.09 % | **+2.09 %** |
| Uranus | +5.4 %, T_c 6153 K | **+5.49 %, T_c 6159 K** |

So the improvement reported earlier is not an artefact of landing on a lucky root.
