<!-- 방사성 가열 축 서베이 ㉓ 기록 — 캐시에 존재량을 와트로 바꾸는 출처가 없다, 툴팁 2배 오표기 수리, 단수명 핵종은 이름 붙인 거절 -->
# Radiogenic heating — what survey ㉓ measured, and Brief 40 (context notes)

2026-09-03. **Documentation plus one tooltip edit; no engine code.** Verifiers per item: (병)
parallel seat, (직) directing seat, (여기) work seat re-read from the cached PDF or the repo.

**Headline (㉓ branch ③): not one cached source computes a radiogenic budget.** Seven consume
one, one gives abundances without rates, and **nobody in the cache converts an abundance into
watts.** The missing half is the *conversion* (decay constants and heat production per kg per
isotope), not the composition. The axis therefore needs papers, and they are with the owner
(§5). What needs no paper is in §2 and §3.

## 1. The eight sources — and two more, reconciled

Full text of every cached PDF swept (병: 57; 여기: 58, re-grepped for radiogenic / radioactive /
radionuclide), each hit read in context.

| source | what it actually has | usable |
|---|---|---|
| **Kankanamge 2016 thesis** `2016PhDT.......206K` | 71 hits, **all dimensionless**: initial H = 10, half-life 0.2 time units, *"chosen for numerical convenience"*; long/short-lived split H_LL:H_SL 1:9 → 4:6, half-lives 0.2 and 10, dimensionless again (병). Prose: *"more than half of the energy currently in the mantle comes from the decay of radioactive isotopes (Gando et al., 2011)"* (line 898, 여기) — a consumer of KamLAND, no rate | no |
| **Malamud & Prialnik 2015** `2015Icar..246...21M` | **The only isotope table in the cache.** Table 1 nominal mass abundances, *"typical of meteorites"*: X₀(²³⁵U) 6.16×10⁻⁹, X₀(⁴⁰K) 1.13×10⁻⁶, X₀(²³⁸U) 2.18×10⁻⁸, X₀(²³²Th) 5.52×10⁻⁸ (lines 856–857, 902–962, 여기) | **half** — abundances only, **no half-life, no W/kg** |
| **Monteux+ 2016** `2016E_PSL.448..140M` | **Neglects** radiogenic heating with its reasoning printed (lines 185–196, 여기) — the ²⁶Al/⁶⁰Fe half-lives in §3 are the **only dimensional radiogenic constants in the whole cache** | no, but load-bearing |
| **Rovira-Navarro+ 2021** `2021PSJ.....2..119R` | *"Radiogenic heating is computed assuming chondritic composition of the mantle (Schubert et al. 1986)"* (lines 378–380, 여기) — a prescription by citation, no value | no |
| **Kankanamge & Moore 2019** `2019JGRE..124..114K` | H is a constant; Table 5's H = 3×10⁻⁶ W/m³ at one significant figure is already `paper-defects.md`-adjacent (Brief 35) | no |
| **Stixrude+ 2020** `2020NatCo..11..935S` | H symbol in the evolution equations (line 516); Methods: the model does not include radioactive heating (병) | no |
| **Moore+ 2017** `2017E_PSL.474...13M` | prose only — heat production *"decreases by a factor of four"* over time (병) | no |
| **Manthilake 2011**, **Britt & Consolmagno 2003** | false positives — "chondrite" matched a porosity review (병); Manthilake's one hit is "distribution of radiogenic isotopes between mantle and core" (line 70, 여기) | no |
| **Yasui+ 2009** `2009JGRE..114.9004Y` *(여기 only)* | compaction of ice–silica mixtures; radioactive elements named once as an early heat source for small icy bodies (lines 100, 109) | no |
| **Vazan+ 2019** `arXiv:1908.10682` *(여기 only)* | Uranus luminosity; U/K/Th heating *"was taken as in Nettelmann et al. (2011) for the fraction of the rock in the ice+rock mixture"* (line 156) — a prescription by citation, nothing printed | no; names **Nettelmann+ 2011** as a giant-side source |

The two rows found only by the work seat's sweep do not move the verdict; they are the size of
hit (two mentions) that a sweep skims past, recorded so the next sweep does not re-find them.

## 2. Our own defect — the `radiogenic_heat_w_m2` tooltip (fixed, `e2bd4ad1`)

`scripts/phase3/field_tooltips.py` said *"지구 ≈ 0.087"* / *"Earth ≈ 0.087"* W/m² for a field
named for **radiogenic** heat. **0.087 W/m² is Earth's total surface heat flux.** Our own
methodology is careful and correct — `internal-heat-luminosity-methodology.md:306`: *"~0.087
W/m², split roughly half radiogenic (U/Th/⁴⁰K decay) and half secular"*, and line 192 with its
sources (Sclater, Jaupart & Galson 1980; Davies 2013) (직, 여기 both read). The tooltip attached
the **total** to a field named for the **part** — a 2× mislabel, user-visible, same shape as the
K&M *"∼1 TW"* trap: sound in its own document, wrong where re-quoted. **Ours, so fixed here and
not indexed in `paper-defects.md`.**

**Not simply halved.** The split hangs on the bulk-Earth U/Th budget, which is what the
geoneutrino measurements (KamLAND, Borexino) exist to constrain. The new wording gives the total,
says radiogenic is roughly half (~0.04–0.05 W/m²), and says the split is contested — both
languages. Landed **before anything emits into that field**, so the first emitted value is not
calibrated against a doubled anchor. No generated HTML on this branch carried the old text.

## 3. Short-lived isotopes — closed as a named refusal

²⁶Al and ⁶⁰Fe deliver a **formation pulse** that can differentiate a body and then vanish, so
present structure can carry a fingerprint from heat that no longer exists. **We decline the term
because the input it needs does not exist here**: a formation epoch resolved to a few million
years. The recipe carries `body_age` in Gyr and nothing finer.

Two cached sources decline it on their own grounds; their sentences are the grounding for the
*numbers*, not for our conclusion:

- **Monteux+ 2016**, lines 187–191 (여기, verbatim): *"the decay of short-lived radioactive
  isotopes such as ²⁶Al and ⁶⁰Fe have probably played a major role especially for **10 to
  100 km size objects** (Yoshino et al., 2003). However, their **half-life times (0.73 My and
  1.5 My respectively)** (Carlson and Lugmair, 2000) are much shorter than the time at which the
  Moon forming impact is supposed to have occurred (between 30 and 100 Myrs after the formation
  of the first solids of the Solar System)."* Then, of the long-lived elements: *"their heat
  production rates are much smaller. Hence … negligible. Thus, we can reasonably neglect
  radiogenic heating in our models."* (lines 192–196).
- **Malamud & Prialnik 2015**, lines 859–860 (여기, verbatim): *"since formation in the KBO zone
  exceeds the life-times of short-lived radioactive nuclei, we do not take them into account."*

⚠ **The refusal rests on our missing input, not on borrowing their conclusions.** Monteux's
dismissal is specific to an Earth-mass body after a late giant impact; Malamud's is about KBO
formation timescales. **Neither says ²⁶Al is negligible for a small body that formed early** —
Monteux says the opposite for 10–100 km objects, a class the roster may want. So: *the term is
real and can dominate for small early bodies; we decline it because the input does not exist
here.* **What would reopen it**: a declared formation epoch (Myr after CAIs) on the body, plus
the two half-lives above and initial ²⁶Al/²⁷Al, ⁶⁰Fe/⁵⁶Fe ratios from a source we hold.

## 4. Prerequisites for the real brief, recorded now

- **One computation read at two depths, not two.** `interior_layers` wants the
  potential-temperature anchor; `core_state` wants the CMB flux across one boundary; a single
  H(r) gives both. **Present-day suffices for those two.** A third consumer, `internal_heat_nontidal
  → dynamo_rocky` via `geotherm` (`chain.yaml:395`), wants the **decay history**, because
  `Rm > 40` asks whether the core is *still* convecting. **Build present-day first; history is
  the second increment.**
- **Naming hazard, recorded not fixed.** `chain.yaml:99–102` already flags that
  `internal_heat_nontidal` outputs `geotherm` while `interior_layers` carries `cmb_temperature`
  — one word covering two quantities (a heat *budget* versus a T(P) *profile*), and the file
  says the geotherm-side name should be split. **Do that before wiring H(r) into either.**
  Nothing renamed here.
- **The Earth anchor must arrive with its own uncertainty**, not as a relayed round number:
  0.087 W/m² and "roughly half" come from Davies 2013 and Sclater+ 1980, both cited by our
  methodology and **neither held** (§5).

## 5. Papers requested from the owner (identifiers read from ADS by title, not attempted)

- ~~`2020ApJ...903L..37N` — Nimmo & Primack~~ — **obtained 2026-09-03 (owner), with source**; consumed by
  Brief 44 (`engine/radiogenic-budget-context-notes.md`). Its isotope table is a dead-LaTeX draft after
  `\end{document}`, absent from the PDF — read that note before citing anything from it.
- `2001E&PSL.185...49A` — Allègre & Manhès, bulk-Earth U/Th/K abundances.
- ~~`2013GGG....14.4608D` — Davies, and `1980RvGSP..18..269S` — Sclater, Jaupart & Galson~~ — **off
  the list (Brief 44)**: Nimmo & Primack 2020 `main.tex:261` cites both for exactly the number we
  wanted them for — total surface heat flow **42–47 TW**, 35–40 TW with the crust's radiogenic
  share removed, and total radiogenic production about **22 TW**. The Earth anchor pair now lives in
  `engine/radiogenic-budget-context-notes.md` and the Phase-3 tooltip.
- Candidate added by the reconciliation (§1): **Nettelmann+ 2011**, the giant-side prescription
  Vazan+ 2019 defers to. Not yet requested.
- **Added by Brief 44's audit — the canonical tabulation of long-lived isotope heat production**, so
  that `radiogenic.py`'s constants stop resting on an unpublished draft table. Candidate named from
  memory, **not read**: Ruedas 2017, *Geochem. Geophys. Geosyst.* (radioactive heat production of the
  geologically important nuclides). No table number is asserted. Until obtained, `REFS` says
  "standard-nuclear-data (not held)".

## Related

- [`docs/reference/internal-heat-luminosity-methodology.md`](../docs/reference/internal-heat-luminosity-methodology.md) — §5 (line 192) and the Earth calibration (line 306)
- [`engine/tidal-interior-context-notes.md`](tidal-interior-context-notes.md) — where K&M's H = 3×10⁻⁶ W/m³ sits
- [`engine/core-melt-depression-context-notes.md`](core-melt-depression-context-notes.md) — the FeS material that will need `core_state`'s CMB flux
