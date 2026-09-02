<!-- 하부맨틀 광물 격자 열전도도 서베이 ⑲/⑳ 기록 — Manthilake 2011 사슬과 Ohta 2012 직접 측정이 CMB 에서 1.6배 어긋난다 -->
# Lattice thermal conductivity of lower-mantle minerals — what surveys ⑲/⑳ measured (context notes)

2026-09-03. **Documentation only** — preserving the parallel seat's surveys ⑲ (Manthilake+
2011) and ⑳ (Ohta+ 2012) before a session teardown. No code touched; materials in `eos.py`
still answer density, specific heat and adiabatic gradient and nothing else, and
`tidal_transport.py` still borrows its `k = 4.0 W/(m·K)` from Kankanamge & Moore 2019 Table 5.
**This note is the grounding a thermal-conductivity brief would consume, not an adoption.**
Verifiers per item: (병) = parallel seat measured, (직) = directing seat reproduced, (여기) =
work seat re-read from the cached PDF before landing.

**Verification status, stated plainly.** The k(P, T) chain and its closure (§3) were computed
by the parallel seat and reproduced independently by the directing seat from the SI equations
(Table S1 self-recovery exact for γ, q, K_T, K′_T on both phases). **The audit seat's third leg
is outstanding as of this commit.** The work seat re-read every *printed* number below at its
place in the source but did **not** re-run the thermodynamic chain; where a number is a chain
output it carries (병, 직) only.

Sources, all cached in `docs/phase3/_papers/` and title-checked:
- `2011PNAS..10817901M.pdf` + `.SI.pdf` — Manthilake, de Koker, Frost & McCammon, *Lattice
  thermal conductivity of lower mantle minerals and heat flux from Earth's core*
  ([ADS](https://ui.adsabs.harvard.edu/abs/2011PNAS..10817901M)). "Parent" below.
- `2012E&PSL.349..109O.pdf` — Ohta, Yagi, Taketoshi, Hirose, Komabayashi, Baba, Ohishi &
  Yagi, *Lattice thermal conductivity of MgSiO₃ perovskite and post-perovskite at the
  core–mantle boundary*, EPSL 349–350, 109
  ([ADS](https://ui.adsabs.harvard.edu/abs/2012E%26PSL.349..109O)).
- Line numbers are `pdftotext` (no `-layout`) extraction lines of those files.

## 1. The model — parent eq. 1 and Table 1

    k(P,T) = k_ref · (T_ref/T)^a · (ρ/ρ_ref)^g                    parent eq. [1]
    g = 3γ + 2q − 1/3          (oxide, ferropericlase)               parent line 95
    g = γ + 2q + K′_T − 4/3    (perovskite)                          parent line 100

with γ the Grüneisen parameter, q = −(∂ln γ/∂ln ρ)_T, K′_T the pressure derivative of the
isothermal bulk modulus (parent lines 204–205). Table 1 (parent lines 221–261, 여기 read
verbatim), **T_ref = 700 K, P_ref = 8 GPa (periclase) / 26 GPa (perovskite)**:

| composition | k_ref (W/(m·K)) | a | ρ_ref (**g/cm³** — see §2) |
|---|---|---|---|
| Pe (MgO) | 21.0 | 0.76 | 3.71 |
| PeFe05 | 8.94 | 0.24 | 3.84 |
| PeFe20 | 6.02 | 0.24 | 4.21 |
| Pv (MgSiO₃) | 12.8 | 0.43 | 4.45 |
| PvFe03 | 4.46 | 0.20 | 4.49 |
| PvAl02 | 3.69 | 0.22 | 4.45 |

## 2. Defect #12 — Table 1's `ρ_ref (cm³/mol)` is a density in g/cm³

Recorded in `docs/reference/paper-defects.md` #12 with its four confirmations. The short form:
the header says molar volume, the numbers are densities at the reference states (the authors'
own SI model gives 3.708 / 4.448 g/cm³ there, 병·직 to four figures; SI Table S1 heads the
*genuine* molar-volume column `V₀ (cm³/mol)` = 11.24 / 24.45 from Xu+ 2008, SI lines 427–466,
여기; Ohta+ 2012 prints ρ_ref = 4.89 g/cm³ for the same equation, line 796, 여기). **Reading it
as printed inverts (ρ/ρ_ref)^g with g ≈ 4–7 and k falls with depth by orders of magnitude.**

## 3. ⚠ The transcription instruction — recovered, not read: evaluate g at the target state

**`g` is not a constant.** γ and q vary through the SI's finite-strain form — SI line 382,
*"This expression allows q to vary with density"* (여기) — so along the chain g falls from
**6.79 → 4.10 (Pe)** and **6.09 → 4.72 (Pv)** between the reference state and the CMB (병, 직).

That makes eq. [1] **ambiguous as printed**: g at the reference state, g at the target state,
or the integral ∫g d ln ρ. **The parent never says which.** The choice was recovered by closing
against the parent's own published prediction for a pure 80 % Pv + 20 % Pe Hashin–Shtrikman
aggregate, **18.9 ± 1.6 / 15.4 ± 1.4 W/(m·K)** at the top / base of the thermal boundary layer
(parent lines 509–510, 여기; the ± are printed and the dispatch omitted them):

| reading of g | top / base (W/(m·K)) | ratio to printed | |
|---|---|---|---|
| **target-state g** | **19.05 / 15.01** | 1.01× / 0.97× | **closes** |
| reference-state g | 28.43 / 22.08 | 1.50× / 1.43× | misses |
| integral ∫g d ln ρ | 22.57 / 17.71 | 1.19× / 1.15× | misses |

(병, 직 independently.) **So: evaluate g at the target (P, T).** The reference-state reading is
the natural one to write down and it is wrong by half — that is why this is a warning and not a
footnote. **The one input not from the papers**: the pressures at the two depths (~127 GPa at
2695 km, ~135.8 GPa at 2891 km) came from PREM, supplied by the parallel seat; the parent
prints depth and temperature along a model geotherm (its ref. 29, line 372), not pressure.

Beside the pure aggregate, the parent's own headline prediction for the **Fe/Al-bearing**
aggregate is **9.1 ± 1.2 / 8.4 ± 1.2 W/(m·K)** (lines 506–508, 여기) — recorded here because it
is the number the parent itself carries forward, and it happens to sit near Ohta's, which §4
shows the *pure* chain does not. Not a closure; a context line.

## 4. The condition that must ride with every k this chain returns

**At CMB conditions this recipe returns ~1.6× the only direct high-pressure measurement of
the same quantity.** Manthilake's chain gives **14.65** (pure Pv) against Ohta+ 2012's published
**9.0 ± 1.6** (line 802, 여기), and **15.98** (80/20 aggregate) against Ohta's **11.0 ± 2.0**
(line 809, 여기) — both at 135 GPa / 3700 K, **no overlap on either** (병, 직).

- **It is not an extrapolation failure.** The ratio is already **1.80 at 22 GPa**, below
  Manthilake's own 26 GPa reference, and it *improves* toward the conditions of interest
  (1.8–2.2× at 300 K, 1.63× at 3700 K) (병, 직).
- **The two are not independent.** Ohta adopts Manthilake's eq. 1 as its eq. (4) (lines 779–
  797), takes **a = 0.43** from it (line 799, *"We use the a value of 0.43 for MgSiO₃ Pv
  (Manthilake et al., 2011)"*), and uses Manthilake's periclase data for the aggregate
  (line 807) (여기).
- **Why the disagreement matters structurally**: Manthilake measures in *temperature* at one
  pressure (26 GPa, 473–1073 K) and extrapolates in pressure; Ohta measures in *pressure* at
  one temperature (11–144 GPa, 300 K) and extrapolates in temperature. **Their extrapolations
  are perpendicular, and the CMB is the only place they cross.** That crossing is the first and
  only test either has had, and it does not pass.
- **An external check that did pass**: Ohta quotes Manthilake's g range as **4.5–6.2** (line
  708, 여기: *"to be 4.5–6.2. We obtained similar g value of 5.6 ± 0.4"*); our independently
  built chain gives **4.52–6.09** (병, 직). A third party quoting the first, matching our
  reconstruction to two figures.

## 5. Measured box versus applied box — and no stated validity range

| | measured | applied (CMB) |
|---|---|---|
| perovskite | 26 GPa, **473–1073 K** (SI Table S5, lines 777–800, 여기 — lowest is 473 K, not 373) | ~136 GPa, ~4100 K |
| ferropericlase | 8 and 14 GPa, ≤ 1273 K | same |

**No validity range is stated in either the parent or the SI.** The thermodynamic models are
taken from Xu et al. (2008) (SI line 389), which we do not have. Record this as *the bound does
not exist to be compared* — worse than a narrow bound, because nothing signals it.

## 6. Ohta+ 2012's data, for the record

Pulsed-light thermoreflectance in a diamond anvil cell (line 96), MgSiO₃ Pv from 11 to
144 GPa **all at 300 K** (line 656) — 13 points as counted by the parallel seat; the work seat
reads 11 Pv + 2 PPv values in the k column of Ohta's table (lines 470–512). PPv at 135 and
141 GPa: **61.8 and 65.0 W/(m·K)** (lines 509–510, and used as k_ref at line 797). CMB values
**9.0 ± 1.6 (Pv)** and **16.8 ± 3.7 (PPv)** at 135 GPa / 3700 K (lines 802–803), both
**extrapolated in temperature** with a = 0.43 assumed for PPv *"because no data is available
so far"* (line 800–801). Aggregates: 11.0 ± 2.0 (Pv + Pe), 17.8 ± 3.9 (PPv + Pe).

⚠ Soubiran & Militzer 2018 quotes that **16.8 bare** — without its ± 3.7 and without the fact
that it is a temperature extrapolation. Carry both.

**Manthilake's ×2 post-perovskite rule is confirmed.** It came from CaIrO₃ analogues; Ohta
measures real MgSiO₃ and gets **16.8 / 9.0 = 1.87×**. The analogue was a good analogue. *(An
earlier survey-⑲ estimate suggesting the rule was off by ~1.8× compared an 80/20 aggregate
against a pure phase; flagged as indicative at the time, now withdrawn.)*

## 7. What this means for the engine

- A material-level `k(P, T)` for Pe/Pv is transcribable from §1 with the §2 unit and the §3
  instruction — **and only with the §4 condition on every value it returns.**
- The thing `tidal_transport.py` borrows (Io mantle k = 4.0, K&M Table 5) is a different
  regime (a few GPa, ~1500 K, solid); this chain at 8–26 GPa reference is the nearest grounded
  material answer, and its measured box (§5) covers the moons' pressures but not a hot
  silicate liquid — Soubiran's liquid k = 31 / 28 / 8 W/(m·K) at 240–500 GPa is the other end
  (`engine/electrical-conductivity-context-notes.md` §4).
- **Implementation is deliberately not in this note.** The §3 closure is a verdict-changing
  number standing on two legs; the audit's third is outstanding, and if it falls this note is
  the record of why and no code has to be unwound.

## Related

- [`docs/reference/paper-defects.md`](../docs/reference/paper-defects.md) — #12
- [`engine/electrical-conductivity-context-notes.md`](electrical-conductivity-context-notes.md) — survey ⑱, the liquid end
- [`engine/tidal-interior-context-notes.md`](tidal-interior-context-notes.md) — where k = 4.0 was borrowed
- [`engine/SESSION-HANDOFF.md`](SESSION-HANDOFF.md) — "three missing properties"
