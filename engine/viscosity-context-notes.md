<!-- 맨틀 점성 서베이 ㉑ 기록 — 형태는 전사 가능하나 상수는 전부 선언, 캐시에 점성을 측정한 논문이 없다 -->
# Mantle viscosity — what survey ㉑ measured (context notes)

**The form is transcribable but every constant in it is a declaration. Nothing in our cache
*measures* a mantle viscosity.**

2026-09-03. **Documentation only** — preserving the parallel seat's survey ㉑. No code touched;
tidal response and convection still hang on a declared rheology, and this note does not change
that. Verifiers per item: (병) = parallel seat measured, (직) = directing seat reproduced,
(여기) = work seat re-read from the cached PDF or recomputed before landing. Line numbers are
`pdftotext` (no `-layout`) extraction lines of the cached files.

## 0. Correct the record first — "zero viscosity sources in the cache" was wrong

An earlier claim from the directing seat, *"zero viscosity sources in the cache"*, came from a
**first-page title scan** and is **wrong**. Full-text extraction over all 58 cached PDFs finds
**five papers that *use* viscosity with printed constants**; none is *about* it, which is why
titles missed them. **The instrument and its failure are recorded here because the same scan
shape will be reached for again**: a title scan answers "is there a paper about X", not "does
any paper carry a value of X".

## 1. Two transcribable dimensional laws — both solid mantle rock, both dimensionally clean

Both checked against the standing dimensionless trap (Kankanamge & Moore 2019, `paper-defects.md`
#4/#5); neither is a re-dimensionalised model.

**Monteux+ 2016** (`2016E_PSL.448..140M`, EPSL 448, 140,
[ADS](https://ui.adsabs.harvard.edu/abs/2016E%26PSL.448..140M)) eq. (8), after Abe 1997:

    η_s = η_s,0 · exp(B · T_liq / T)        η_s,0 = 256 Pa·s,  B = 25.17

Line 342, 여기 read verbatim: *"We used η_s,0 = 256 Pa s, and B = 25.17 based on the olivine
rheology (Karato and Wu, 1993; Abe, 1997)."* Pressure enters **implicitly through T_liq(P)**;
the paper's own check is *"∼10²³ Pa s in the lowermost mantle"* along a 1600 K-potential
adiabat (lines 343–345).

**Rovira-Navarro+ 2021** (`2021PSJ.....2..119R`, PSJ 2, 119,
[ADS](https://ui.adsabs.harvard.edu/abs/2021PSJ.....2..119R)) eq. (5):

    η = η_s · exp[ (E_a / (R_g T_s)) · (T_s/T − 1) ]     η_s = 1×10¹⁶ Pa·s,  E_a = 300 kJ/mol

η_s and E_a are declared in the paper's parameter table (line 279 row: `… 300  1·10¹⁶ …`, 여기);
line 412: *"where η_s is the viscosity at the solidus temperature, E_a is the activation energy"*.
⚠ **E_a = 300 kJ/mol is an unchecked secondary citation** (Brief 55): its footnote is Karato & Wu
1993 alone, and that paper is withdrawn from the request list (paywall, then judged unneeded —
`SESSION-HANDOFF.md` request list). It is corroborated at *range* level — inside Nimmo+ 2004's
independently quoted 250–350 kJ/mol (Karato & Wu; Yamazaki+ 2000), a band also cited to Solomatov
1995 — but not at *point* level. Two lookalikes: Gaidos+ 2010's b ≈ 17 cites **Karato, Riedel &
Yuen 2001**, a different paper; "Jaupart 2007" names at least two works.

## 2. The one agreement on this axis — and the ratio it rides on is ours

At the solidus, Monteux/Abe gives **1.18×10¹⁶ Pa·s** against Rovira-Navarro's declared
**1×10¹⁶** — two unrelated sources, 18 % apart (병, 직, 여기 recomputed).

⚠ **That uses T_sol/T_liq = 0.80, which is the parallel seat's ratio, not printed anywhere.**
At 0.75 the law gives **9.6×10¹⁶** and at 0.85 **1.9×10¹⁵** (여기 recomputed), so the agreement
is real but the form is steep. **Carry the ratio as a declaration.**

## 3. ⚠ Monteux's form is not robust

The exponent B·T_liq/T reaches ≈ 45 at deep-mantle ratios, so d ln η / d ln(T_liq/T) ≈ 45 — **a
1 % error in the ratio moves η by 45 %.** It reproduces its own stated ~10²³ Pa·s at
(T_liq, T) = (4500, 2400) K and misses by **four orders** at (4000, 2600) K (병). Those pairs are
the parallel seat's; **the paper prints neither.**

## 4. What the cache does not have

- **Pressure dependence (activation volume V\*) is absent from the entire cache.** "Activation
  volume" occurs in **one** of the 58 PDFs (여기 re-grepped the full text of every file) — the
  Kankanamge 2016 thesis (`2016PhDT.......206K`), as a bare symbol in its eq. 2.6.2, no value.
  Three different ways of not having one are in the cache, all three recorded:
  - **Rovira-Navarro drop it and say so** (lines 413–421, 여기): *"We do not consider the change
    of activation energy with pressure … the activation pressure at Mars' mantle varies between
    300 KJ mol⁻¹ close to the surface to 540 KJ mol⁻¹ in the mid-mantle (Nimmo & Stevenson
    2000)."* — **the only quantification anywhere in the cache, and it is Mars' mantle**, quoted
    second-hand, with the paper's own word "activation pressure" for what its units say is an
    energy.
  - **Monteux/Abe substitute** the homologous-temperature form (§1).
  - **Kankanamge & Moore linearise it away** (Frank-Kamenetskii, `tidal_transport.py` line 57 ff.).
- **Grain size has no mantle value in the cache**, though the thesis names it as worth
  *"several orders of magnitude"* for diffusion creep (병).
- **The liquid axis has no cached source.** Stixrude+ 2020's η = 0.1 Pa·s (line 274, 여기, used
  only to show the magnetic Prandtl number is small) traces to **Karki & Stixrude 2010**
  (`2010Sci...328..740K`, ref. at line 707) — **not cached** (여기 checked), and that paper's own
  abstract says the quantity **varies by two orders over the mantle pressure regime** (병), so
  the 0.1 is a point quoted for a range. Safe inside Stixrude's Prandtl argument; **must not be
  lifted out of it.**

## 5. The spread, measured rather than asserted

Across the printed laws on a common temperature grid the disagreement is **~1 order over
1400–2000 K**, widening at the edges — **33× at 1400 K, 4.7× at 1600 K, 69× at 2000 K** (병, 직)
— **not the ≥ 2 orders expected.** The ≥ 2 orders live in the anchor, the missing V\* and the
missing grain size, not in the forms.

## 6. What a declaration should span — this axis's product

- Anchor **10¹⁵–10¹⁷ Pa·s at the solidus**, 10¹⁶ where the two sources converge (§2).
- Rising to **~10²¹–10²³ Pa·s in a cold lower mantle** per Monteux's own check (§1, §3).
- **Plus 1–2 orders** for the absent activation volume, and **several more** for grain size if
  diffusion creep dominates (§4).
- **Every value emitting from this axis says it was declared.**

## 6b. The family's reference form — Nimmo+ 2004 eq. 39 (placed by Brief 56, c4's text)

Nothing calls it; it is recorded as the form a fifth law would be measured against.
Nimmo, Price, Brodholt & Gubbins 2004, GJI 156, 363 (`2004GeoJI.156..363N`,
[ADS](https://ui.adsabs.harvard.edu/abs/2004GeoJI.156..363N)), eq. 39:

    η_b(T) = f · η₀ · exp[−ζ (T − T₁)]      Table 2: ζ = 1.0 ± 0.5 ×10⁻² K⁻¹, η₀ = 1.0 ×10²¹ Pa s,
                                              f = 10, T₁ = 3400 K, T₀ = 1573 K

Recorded because it is the only cached law satisfying all three at once: dimensionally clean
(unlike Kankanamge & Moore 2019's unitless A = 15), carrying a published uncertainty on ζ (which
Rovira-Navarro's re-use drops), and with its ζ verified to reproduce from the paper's own quoted
activation energies — ζ = E/(RT²) over E = 250–350 kJ/mol, T = 1600–2500 K gives 0.00481–0.01644
against the printed 0.005–0.016, the range independently attributed to Solomatov 1995 (직, 여기).
**Caveat that rides with it**: the adopted ζ = 0.01 back-converts to E ≈ 213 kJ/mol at 1600 K, below
the quoted 250 floor, re-entering at T ≈ 1734 K — internally consistent, but near the low edge of the
range that motivated it, not its midpoint. (The top-layer twin, eq. 35 with η₀ and T₀, is what
`mantle_flux.py:86` carries.)

## 7. A search-method trap worth its own line

The first ADS query for Karki & Stixrude 2010 returned **numFound 0**, because the citing
paper's reference line wraps and only the half before the colon was searched (직). **A wrapped
reference's first line is a way to manufacture a false "not found."** Search by the full title,
or by the bibcode read from ADS, never by a line of the citing paper's text layer.

## Related

- [`engine/thermal-conductivity-context-notes.md`](thermal-conductivity-context-notes.md) — the other declared-today property
- [`engine/electrical-conductivity-context-notes.md`](electrical-conductivity-context-notes.md) — where Stixrude's η = 0.1 lives
- [`engine/tidal-interior-context-notes.md`](tidal-interior-context-notes.md) — the rheology the tidal axis declares
- [`engine/SESSION-HANDOFF.md`](SESSION-HANDOFF.md) — "three missing properties"
