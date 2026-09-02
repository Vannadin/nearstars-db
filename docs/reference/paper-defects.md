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

---

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

**Eleven defects across the sources we have actually transcribed from.** Five are magnitude or
sign slips in a single printed value (#1, #6, #8, #9, #10), three are a paper disagreeing with
itself (#4, #5, #7), one is a claim range wider than the data behind it (#8), one is an
attribution that points at the wrong owner (#2), and one is a citation with the wrong year (#11).

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
