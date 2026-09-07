<!-- 인용한 논문 자체의 결함 색인 — 발견 자리는 그대로 두고 여기서 가리킨다 -->
# Defects found in papers we cite

**An index, not a record.** Each defect stays written where it was found, with its quotes at
their place in the source and its verifier named; this file exists so a session can ask *"have
we already read this paper, and did it bite us?"* without grepping every note — and so that a
**new paper by the same author or group** arrives with the earlier finding attached.

**Scope.** Defects in the *sources*, not in our transcription of them. Our own errors live in
the briefs and in `engine/SESSION-HANDOFF.md`'s rules section; a mistake we made reading a
sound paper does not belong here.

**Adding a row.** Name the quantity, say what the paper prints versus what is right, name where
the correction comes from, and point at the note that carries the full case. **If a wrong value
would silently produce a wrong answer, say whether a gate catches it.**

---

## The index

| # | Source | Defect | Consequence if taken as printed | Full case |
|---|---|---|---|---|
| 1 | **Monteux+ 2016** (EPSL 448, 140) — *as rendered by a widely-cited secondary source* | Low-pressure solidus scale printed as `1336 × 10⁹` Pa; the primary text (line 275) has **`1.336 × 10⁹`** | Solidus **750 K cold across the entire moon and small-planet range** | `engine/silicate-melt-context-notes.md`; **gate trap pin fires at −745.6 K on the 20 GPa join** |
| 2 | **Millot+ 2019** (Nature 569, 251) | Abstract's *"exceeding 100 GPa … above 2,000 K"* is that paper **restating its own refs 6–12's prediction**, not its result; its 100–400 GPa × 2 000–3 000 K is an experimental window, not a boundary | Constants carried a **Millot label on someone else's number**, and the label stopped the checking | `engine/superionic-ceiling-context-notes.md`, `interior-core.md` C6 |
| 3 | **Kankanamge & Moore 2019** (JGR Planets 124, 114) | §6's *"totaling ∼1 TW"* against its own printed 2.5 W/m² — Io's area gives **104 TW** | Two orders low; a body of 178 km would be needed | `docs/reference/tidal-heating-methodology.md` citation block |
| 4 | **Kankanamge & Moore 2019** | Same symbol, two values: **`T₀ (= 1)`** (line 141, §2) vs **`T₀ = 1400 K`** (Table 5) | Which one entered §6 is undecidable from the paper | `engine/tidal-interior-context-notes.md` §7 |
| 5 | **Kankanamge & Moore 2019** | Eq. (2) evaluated with the paper's own Table 5 misses its own stated threshold (~8) by **six orders in both directions**; the printed reading gives ΔT in **inverse kelvin** | The dimensional presentation cannot be closed at all | `engine/tidal-interior-context-notes.md` §7 |
| 6 | **Spencer, Katz & Hewitt 2021** (Icarus 359, 114352) | Table 1 prints thermal diffusivity as **`10⁶ m²/s`**; rock is **`10⁻⁶`** — a dropped minus sign | 12 orders; same family as #1 | `engine/tidal-interior-context-notes.md` §7 |
| 7 | **Deng+ 2023** (PRB 107, 064103) | Printed triple point **180 GPa / 6420 K**, but the two printed equations cross at **173.6 GPa / 6413 K** | 6.4 GPa; the triple point comes from the source data, not the fits | `engine/silicate-melt-context-notes.md` |
| 8 | **Nguyen Quang Hoc+ 2024** (JAP 136, 045103) | Abstract headline **"up to 1400 GPa"** exists only in a figure; the printed ε table stops at **100 GPa** | A 14× gap between claimed and data range — C6's disease | `engine/silicate-melt-context-notes.md` (recorded as not-adopted) |
| 9 | **Militzer 2024** (PNAS 121, e2403981121) | Three simulation labels are **exactly 2× the paper's own eq. [3]** (`H₁ = N_H/2N_O`): O₈₄H₂₂₆ is **1.345**, printed as 2.69 (same for H₂₈₂, H₃₉₆). The control passes — eq. [2] and Table 1 reproduce exactly, so the defect is confined to those three | The method interpolates *as a function of hydrogen fraction*, so placing the deposited file on that axis needs the right scale and the paper prints both | `engine/carbon-*-context-notes.md` (survey ⑯) |
| 10 | **Buono & Walker 2011** (GCoA 75, 2072) | Eq. (5), the 14 GPa liquidus polynomial, prints its constant as **−2140.2** — so T(x=0) = −2140.2 K, a negative melting point. Read +2140.2 it continues the monotone pure-Fe intercept rise (1808.9 → 2093.0 → 2140.2 K), and the 6 GPa intercept matches the paper's own prose to 6 K, so the family is sound and one sign is not | The x = 0 intercepts are the transcription check for the whole polynomial set; the paper itself says eqs. (2)/(5) were not used to calibrate its model | `engine/core-melt-depression-context-notes.md` (survey ⑰) |
| 11 | **Soubiran & Militzer 2018** (Nat. Commun. 9, 3883) | Reference 11 prints *Geochem. Geophys. Geosyst.* **17**, 1935–1956 **(2006)**. Volume and pages are right; the year is **2016** — [`2016GGG....17.1935O`](https://ui.adsabs.harvard.edu/abs/2016GGG....17.1935O), Olson, P., *Mantle control of the geodynamo: Consequences of top-down regulation*, confirmed through ADS by title (pdftotext extraction line 875) | Load-bearing: that one citation carries **both** the `Rm > 40` onset **and** the `Ro_ℓ ≤ 0.1` dipolar cutoff, so a session chasing "Olson 2006" lands in the wrong decade of a prolific author's output. **No gate catches a citation year** | `engine/electrical-conductivity-context-notes.md` (survey ⑱) |
| 12 | **Manthilake+ 2011** (PNAS 108, 17901) | Table 1 heads its reference-density row **`ρ_ref (cm³/mol)`**; the values (3.71–4.49) are **densities in g/cm³** at T_ref = 700 K, P_ref = 8 GPa (periclase) / 26 GPa (perovskite). Four independent confirmations: (1) magnitude — MgO's molar volume is ~11.2 cm³/mol and MgSiO₃ perovskite's ~24.5, so 3.71 / 4.45 are off by 3× / 5.5×; (2) the authors' own thermodynamic model (SI eqs. S6–S12) at their own reference states gives **MgO 3.708, MgSiO₃ 4.448 g/cm³** against printed 3.71 / 4.45 (0.05 %), while molar volume there is 10.87 / 22.57; (3) **a header transplant** — SI Table S1 heads a genuine molar-volume column `V₀ (cm³/mol)` (MgO 11.24, MgSiO₃ 24.45, from Xu+ 2008) and the parent's Table 1 carried that header onto a density row; (4) Ohta+ 2012, adopting the same eq. 1, prints Pv `ρ_ref = 4.89 g/cm³` at 62 GPa / 300 K, and our chain gives 4.882 there (0.17 %) | ρ_ref sits inside `(ρ/ρ_ref)^g` with g of order 4–7, so reading it as a molar volume **inverts the ratio and amplifies it**: k wrong by orders of magnitude and *decreasing* with depth. Nothing in the table contradicts the wrong reading — the numbers look dimensionless. **No gate catches it**; the transcription check is the SI model closure in (2) | `engine/thermal-conductivity-context-notes.md` (surveys ⑲/⑳) |
| 13 | **Rodríguez-Mozos & Moya 2022** (RM22, A&A 661, A101; ar5iv render `2203.01065.md`) | Table 8 prints Mars's mass as **`0,1074`** — a comma decimal in an otherwise dot-decimal table; and one paragraph carries three values for the multipolar collapse (OC06 *"of the order of 0.05"*, its own *"about 0.06"*, and Grießmeier's 0.15, which is a different quantity — Earth's present moment as denominator for one configuration) | A machine read of Table 8 drops or mis-parses Mars; the 0.15 was carried for a day as a same-quantity alternative and made a 2.5× spread that did not exist | `engine/rocky-dynamo-context-notes.md` step 4 (2026-09-04) |
| 14 | **Rodríguez-Mozos & Moya 2022** (RM22) | Table 6 prints λ_m = **1.32 m²/s** and σ = 1.36×10⁶ S/m, both sourced to (D) = Pozzo+ 2012, yet its own eq. 24, λ_m = 1/(μ₀σ), gives **0.585 m²/s** — a 2.26× disagreement between two values of one source (arithmetic reproduced by the work seat) | Any Ro_ℓ or Rm built from Table 6 carries a factor 2.26 that the paper does not resolve | `engine/regime-gate-context-notes.md` §1 (C16, 2026-09-04) |
| 15 | **Rodríguez-Mozos & Moya 2022** (RM22) | The 0.12 dipolar/multipolar boundary is called a *"local Rossby number"* in §5.2 and *"the Rayleigh number above the critical value of 0.12"* in the four-zone paragraph — one threshold, two names for two different quantities | A reader following the second name looks up Ra_Q, not Ro_ℓ | `engine/regime-gate-context-notes.md` §1 |
| 16 | **Rodríguez-Mozos & Moya 2022** (RM22) | The printed Ro_ℓ equation does not reproduce the paper's own Table 8: normalised so ν and λ cancel, Ra_Q^(2/5) alone gives Mercury 0.94 · Venus 1.24 · Mars 0.88 · Ganymede 0.75 of the printed values while the full form with Ω^(1/3) D^(2/3) gives 0.26 · 0.20 · 0.96 · 1.02 — 4–5× off on the slow rotators (**parallel seat's measurement, not yet reproduced by the work seat**); and Table 8 is a fit, not a validation (*"the core thermal conductivity better fitting the observed magnetic moment and local Rossby number is 60 W/m/K"*) | Whichever form of Ro_ℓ is executed disagrees with the paper somewhere; the five Solar-System rows cannot serve as an independent check | `engine/regime-gate-context-notes.md` §1 |
| 17 | **ADS result lists** (a search instrument, not a paper) | A truncated list title *"…Super-Earth and Su…"* was read as sub-Neptune; the full title was **Super-Venus** | A paper about the wrong class enters a survey on the strength of a cut title | `engine/regime-gate-context-notes.md` §1 (parallel seat, 2026-09-04) |
| 18 | **`2022AGUFM.P45B..06Z`** (AGU Fall Meeting abstract) | Title is exactly the C18 question; it is a conference abstract — no body, citation count 0 | A same-title hit that answers nothing; counted as literature only by title | `engine/interior-core.md` C18 |
| 19 | **Zhang & Rogers 2022** (`2208.06523`) | Cites sub-Neptune surface fields as *"≲ 3 G (Bonati+ 2021)"*, but Bonati+ 2021 models **rocky planets without an H/He envelope (0.8–2 M⊕)** — a secondary citation stretched to a class the primary did not model | The 3 G would be quoted as a sub-Neptune value; it is not one | `engine/interior-core.md` C18 / C23 |
| 20 | **Ramstad+ 2017a** (JGR Space Physics 122, 7279, doi 10.1002/2017JA024098) | Eq. (12) states *"n_sw and v_sw are defined in units of cm⁻³ and **km/s**"*, but the fitted exponents only reproduce the paper's own short form when **v is in 100 km/s**. Checked against its eq. (13), `L_n(p) ≈ 0.13 p^(−0.30) + 0.49`: at (2 cm⁻³, 400 km/s) the short form gives 0.6468 and the full form gives **0.6459** in 100 km/s units against **0.4937** in km/s | The velocity term all but vanishes and the constant `d = 0.49` takes over, putting the IMB subsolar point at **1.11 instead of 1.24 R_p — about 130 km** | `engine/induced-magnetosphere-source-check-notes.md` |
| 21 | **Ramstad+ 2017a**, same equation block | Eq. (13) prints *"with p_dyn and L_n in units of **nT** and R_M"*. `p_dyn` is a dynamic pressure and nT is a magnetic-field unit; the values only work as **nPa** | Read literally the short form has no valid input at all; it is the check equation that catches #20, so a reader who stops at the printed unit loses the one cross-check the paper supplies | same |

| 22 | **Barnes 2017** ([`2017CeMDA.129..509B`](https://ui.adsabs.harvard.edu/abs/2017CeMDA.129..509B)) | Eq. (6) gives the CPL equilibrium rotation period in two branches whose conditions point the same way — `P` for `e < √(1/19)` and `2P/3` for `e ≤ √(1/19)`. The prose one paragraph above says *"but above it"*, so the second branch is `e ≥ √(1/19)` | Read literally the cases overlap below the threshold and nothing covers `e` above it — the branch the equation exists to define. ⚠ Separately, plain-text extraction of this page drops the radical: `√(1/19) = 0.2294` becomes `1/19 = 0.0526`, a factor of 4.4, and that moves the Moon from far below the threshold to just above it — i.e. from agreeing with the observed 1:1 to predicting 3:2 | verified on the page image, p. 8 |

| 23 | **Neumann+ 2019** ([`2019ApJ...882...47N`](https://ui.adsabs.harvard.edu/abs/2019ApJ...882...47N)) | §2.3 defines `f_i` as *"the number of atoms of **the stable** isotope per 1 kg"* and then prints `f_i = 10³ x_i N_A / m_{a,i}` *"with the relative mass fraction x_i of the stable isotope, the molar mass of **the radioactive** isotope"*. Counting ²⁷Al atoms needs 26.98, not 26 | Every ²⁶Al heat number inherits a **3.77 % overstatement** if the formula is followed as printed. It moves no verdict in C21 — the `t₀` threshold shifts under 2 % — but it silently propagates into any absolute heat budget. ✅ **Confirmed 2026-09-07 from the paper's own Table 2 — no new source was needed.** The earlier hesitation was that Ruedas 2017 gives ²⁶Al an atomic mass of 25.986891863 u, its own, so the printed molar mass might be a convention. **A convention cannot change sign, and this one does.** Applying the printed formula to all seven of Table 2's rows: ²⁶Al **+3.83 %** and ⁵³Mn **+3.77 %** (the radionuclide is lighter than its stable reference), but ⁶⁰Fe **−6.67 %** and ⁴⁰K **−2.50 %** (heavier), while ²³²Th and the two U rows come out **exact** because `Z_i = 1` there makes the reference nuclide the radionuclide itself. So the printed formula is exact only where the two molar masses coincide and wrong in both directions elsewhere — a slip in the subscript, not a convention, and the definition's *"atoms of the stable isotope"* is the phrase that is right. ⚠ **No value in this repo moves**: these numbers appear in documents only, because C21's pulse node is not built. Discriminant recorded: `H₀ = 2.041×10⁻⁷ W/kg` (26.98) vs `2.119×10⁻⁷` (25.99) for ordinary chondrite | C21 (b), 2026-09-07 |
| 24 | **Korenaga 2009** ([`2009GeoJI.179..154K`](https://ui.adsabs.harvard.edu/abs/2009GeoJI.179..154K)) | §4 prints the constants used for every dimensionalized example as `k = 4 W m⁻¹ K⁻¹`, **`α = 2 × 10⁻³ K⁻¹`**, `κ = 10⁻⁶ m² s⁻²`, `ρ₀ = 4000 kg m⁻³`. Two are wrong as printed: **`α` is 100× a mantle thermal expansivity** (Nimmo+ 2004 Table 2 prints ~2–3 × 10⁻⁵ K⁻¹, and this repo's `engine/mantle_flux.py` carries that value), and **`κ`'s units are `m² s⁻²`** where a diffusivity is `m² s⁻¹`. ⚠ Read from the **page image** of p. 163, not the text layer, so neither is an extraction artefact | **Harmless inside the paper, harmful if transcribed.** The pre-exponential factor `b` is fitted so Earth returns 50 mW/m², which absorbs any constant multiplying `Ra_i` — so the paper's own figures are unaffected and `α` never had to be right. ⚠ **Sharpened 2026-09-08**: the inherited error depends on what else is lifted. Taking `α` **together with** the paper's own recipe for `b` (re-fit so Earth returns 50 mW/m²) inherits **nothing** — the fit absorbs it exactly, which is what C47 (c) and (d) did. Taking `α` and supplying `b` from elsewhere — a rheology paper, a textbook viscosity — inherits the full 100× in `Ra_i`, i.e. `10^{2β}` ≈ **4.6× in `Nu`** at `n = 1`. **The hazard is mixing the two sources, not the constant alone.** ⚠ **This repo transcribed nothing**: C47 (c) evaluated the law with `b` re-fitted on the paper's own Earth condition, so `α` cancels in every Earth→Mars ratio reported there | C47 (c), 2026-09-07 |

---

⚠ **#20 and #21 are one defect, not two.** The equation whose unit is misprinted (#21) is the same
short form that catches the misprinted unit in the fitted equation (#20). A reader who trusts the
printed units loses the only cross-check the paper supplies, and the two slips conceal each other. A
defect that disables the check for another defect deserves its own line here, because the pattern is
not additive.

## Two that are not paper defects, kept here because they read like one

- **SeaFreeze `water2`** returns **negative density inside its own knot box** — the printed
  validity range is not the executed one. That is a *library* behaving worse than its
  documentation, found by a pre-registered sweep, and it is why baking a source now requires
  measuring its effective ceiling. `engine/water2-context-notes.md`.
- **The IF97 PDF's text layer dropped every power of ten.** An *extraction* failure, not a
  printing one — which is why a machine-extracted numeric table is checked against a different
  rendering rather than against check values that rode the same extraction.
  `engine/steam-context-notes.md`.

---

## What the pattern says

**Twelve defects across the sources we have actually transcribed from.** Five are magnitude or
sign slips in a single printed value (#1, #6, #8, #9, #10), three are a paper disagreeing with
itself (#4, #5, #7), one is a claim range wider than the data behind it (#8), one is an
attribution that points at the wrong owner (#2), one is a citation with the wrong year (#11),
and one is a correct unit transplanted onto the wrong quantity (#12).

Three consequences we now work from:

- **Transcribe from the primary source.** #1 was in a secondary rendering and the primary was
  clean; the difference was 750 K where our moons live.
- **Check a transcription against something the paper states independently** — its own printed
  extrapolation point, a self-closure, or a second equation. #7 and #9 were both caught that
  way, and #5 is what happens when the paper cannot pass its own check.
- **A number's label is checked at its place in the text.** #2 looked sound until the sentence
  was read whole.

## Related

- [`engine/SESSION-HANDOFF.md`](../../engine/SESSION-HANDOFF.md) — the rules these produced
- [`engine/interior-core.md`](../../engine/interior-core.md) — C6, where material-ceiling defects land
