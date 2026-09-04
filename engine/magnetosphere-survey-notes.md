<!-- magnetosphere_geometry·stellar_wind 레시피 등록 사전조사 — 문서가 인쇄한 식·입력·열린 자리, p_ram 관행, chain 간선. 병렬석 기록, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (MAGNETOSPHERE-SURVEY.md, 18:25 KST), body unedited. Its §5 (false ABSENT verdicts) is what became the check_paper_held.py sidecar repair, 844d0787. -->

# Pre-survey — magnetosphere_geometry + stellar_wind recipe registration
Parallel seat, 2026-09-04. Read-only; no repo writes. Line numbers are
`docs/reference/planetary-magnetosphere-geometry-methodology.md` unless named otherwise
(1301 lines, 94872 bytes, mtime 2026-08-24 16:49).

## 0. Two corrections to the brief's premises (printed facts, checked by opening the lines)

- **`magnetosphere_geometry` DOES carry a recipe key.** `engine/chain.yaml:389-394`:
  `kind: computed` / `recipe: planetary-magnetosphere-geometry-methodology` /
  `outputs: [r_mp, belt_extent, belt_intensity]`. Parsed with yaml, the nodes that are
  `kind: computed` with **no** recipe key are exactly seven: `tidal_response`,
  `xuv_history`, `stellar_wind`, `global_fluid_layer`, `t_eq_stellar`, `t_eff_body`,
  `surface_uv`. `magnetosphere_geometry` is not among them; `stellar_wind` is
  (`chain.yaml:384-388`, no recipe key).
- **The `:4` / `:83` refs are prose lines, not equations.**
  - `:4` = `Method reference for turning a body's **dipole field strength** (from the`
    (the sentence continues at :5 with the two dynamo-recipe links). So the b_eq edge's ref
    points at the sentence naming the dynamo recipes as the b_eq source, not at a formula.
  - `:83` = `the **stellar wind** for a planet, or the **parent's co-rotating magnetospheric`
    — inside the paragraph that *defines* P_ram (:82 `where \`P_ram = ρ v²\` is the ram
    pressure of whatever flows past the body —`). The formula itself is `:80`.

## 1. What each Part actually prints

### Part A — geometry (`:21`-`:322`)

| # | printed equation (line) | inputs (symbol · unit) | coefficient provenance |
|---|---|---|---|
| A1 | `:80` `R_mp / R_p = [ f² · B_eq² / (2 μ₀ · P_ram) ]^(1/6)`, `μ₀ = 4π×10⁻⁷` | `B_eq` [T], `P_ram` [Pa], `f ≈ 2` (Chapman–Ferraro surface-current doubling, stated at `:78-79`) | Chapman & Ferraro 1931 `1931TeMAE..36...77C`; empirical form Shue 1997/1998 `1997JGR...102.9497S` / `1998JGR...10317691S` (`:74-76`) |
| A2 | `:103` `R_mp = k(p) · R_CF`, `k(p) = 38.0 p^−0.25 / R_CF(Jupiter, p)` (magnetodisc inflation for giants) | `p` = p_SW [nPa] | Rutala 2025 `2025JGRA..13033842R` / arXiv 2502.09186, fitted to observed Jovian crossings (`:91-93`). Inflation falls as `p^−1/12` because CF goes `p^−1/6` and the fit `p^−1/4` (`:99-101`) |
| A3 | `:115-116` belt extent: outer `R_outer ≲ 0.6–0.8 R_mp`, inner `R_inner ≈ 1.1–2 R_p` | `R_mp`, `R_p` | no bibcode attached to the two ranges; the section's justification is L-shell closure (`:113-114`) |
| A4 | `:33-40` branch test `R_mp(B_eq) > r_ionopause` (airless: `> 1 R_p`) | `R_mp`, `r_ionopause` | Egan 2019 `2019MNRAS.488.2108E` (**HELD** as arXiv 1907.02978) |
| A5 | `:193-196` induced standoff — **no formula**: "Adopt `1.05–1.2 R_p` … there is no useful field parameter to derive it from"; Venus 330 km subsolar / 700 dusk / 1000 dawn | measured scale only | Brace 1980 `1980JGR....85.7663B` |
| A6 | `:216` induced nightside line `ρ = 1.13 − 0.101·X'` (5.77° flare) — **explicitly "not implemented"** (`:219`) | `X'` | Martinecz 2009 `2009JGRA..114.0B30M`; tested to 20 R_V by Edberg 2024 `2024JGRA..12932603E` (**HELD** as arXiv 2410.21856) |
| A7 | `:240-241` sub-Alfvénic tail `L = 150^M_A × nose` → `pause_extension = 2^α / 150^M_A` | `M_A`, `α` | owner decision 2026-08-17 (`:237`); lean `arctan M_A` |
| A8 | `:1023` Jupiter α fit `α = 0.28 + 1.08·p_SW` (nPa), calibrated 0.03-0.13 nPa | `p_SW` [nPa] | Rutala 2025, their "S97*" form, Table 2 |

Shape policy (owner, 2026-08-14) quoted at `:222-223`; the α/shape decision table is `:225-230`.

### Part B — belt intensity (`:323`-`:481`)

| # | printed equation (line) | inputs | provenance |
|---|---|---|---|
| B1 | `:360-361` differential spectrum `j(E) = C·E·(kT(γ₁+1)+E)^(−γ₁−1)/(1+(E/E₀)^γ₂)`, pitch factor `sin^2s α` | `C, kT, γ₁, γ₂, E₀, s` | Mauk & Fox `2010JGRA..11512220M` (paper paywalled, no preprint — stated at `:346-348`); implementation ported from their Zenodo software `10.5281/zenodo.4782323` = `2021zndo...4782323M` |
| B2 | `:364` marginal stability `CmCk = L·R_p·w_i/(3·v_g)` (wave gain 3) | `L`, `R_p`, `w_i`, `v_g` | resonance eqs A4–A8 of Summers, Tang & Thorne 2009 `2009JGRA..11410210S`; independently confirmed Mourenas 2024 `2024JGRA..12932193M` |
| B3 | `:391` controlling variable `We/wpe ∝ B/√n_cold` — **not B, not B²** | `B`, `n_cold` | structural statement from B1/B2 |
| B4 | `:413-414` **the only rad/h formula in the doc**: `dose ≈ 10.4 × (B_eq/31 µT)^1.9`, anchors Earth 31 µT → 10.4 rad/h and Jupiter 428 µT → ~1500 rad/h; outer/inner ratio ~0.1 torus-driven, ~0.2 wind-fed (`:419-420`) | `B_eq` [µT] | **a two-anchor empirical fit, labelled "not the K–P scaling" (`:414-416`) and "Confidence remains low" (`:424`)**. No bibcode — the anchors are the audited Earth/Jupiter dose values |
| B5 | `:415-417` two hard checks: (a) below the computed K–P ceiling via `scripts/refs/kp_limit.py`; (b) source-starved belts stay plain regime calls | — | — |
| B6 | `:400-407` dose transport: SHIELDOSE-2, free-field ≈ 2.3×10⁻⁸ rad(Si) per e⁻cm⁻² at 1 MeV, de-rated ~10× behind ~2.5 mm Al; 1 MeV CSDA range ≈ 2.0 mm Al | — | Seltzer `1979ITNS...26.4896S`, `1992STIN...9315580S` |

Source/loss inventory with bibcodes: `:327-341` (CRAND Lenchek 1961 `1961JGR....66.4027L`; radial diffusion Schulz & Lanzerotti 1974 `1974pdrb.book.....S`; Io torus Bagenal 1994 `1994JGR....9911043B`; Jovian model Divine & Garrett 1983 `1983JGR....88.6889D`; K–P Kennel & Petschek 1966 `1966JGR....71....1K`; waves Thorne 2010 `2010GeoRL..3722107T`, Ripoll 2020 `2020JGRA..12526735R`; ring/moon sweeping Cooper 1983 `1983JGR....88.3945C`). Slot/hiss: Ripoll 2016 `2016GeoRL..43.5616R` (`:120-127`).

The doc's own verdict at `:349-352`: belt intensity "stays a **regime call with a stated source and loss**, not a formula output."

### Part C — Kerbalism mapping (`:482`-`:1040`)
Field table `:484-491`; per-field "what fixes it / derivation / couples to" table `:678-701`.
Derivation order printed at `:675-677`:

    B_eq + P_ram  →  R_mp (Part A)  →  pause fields
                                   →  belt L-shell bounds  →  fit_belts.py  →  belt geometry
    source − loss (Part B) + K–P ceiling  →  radiation_inner/outer
    radial profile shape                  →  radiation_*_gradient
    harmonic content / tilt / offset      →  deform, pole_lat/lon, geomagnetic_offset

Computable pieces: `pause_radius = R_mp × pause_compression` (`:486`); `α = log₂(pause_compression)` (`:682`); `pause_extension`: `L = pause_radius / extension` (`:683`); gradient floor `gradient ≥ *_radius / d_max` (`:616`, inverse at `:618`); `deform_xy` equatorial extent `(dist ± radius)/√deform_xy` (`:689`); pole `lat = 90° − magnetic_dipole_tilt_deg` (`:697`). `radiation_pause` is **stock-uniform ~−0.01, explicitly not scaled** (`:487`, `:686`). `radiation_surface` is **stars only** (`:701`).

### Part D — moon ↔ parent (`:1041`-`:1143`)
Three couplings, no new equations: the moon's dose is the parent's trapped flux at its
L-shell (`:1046-1055`); the moon is a loss **or** source term (`:1057-1065`); the moon's own
standoff uses **Part A with `P_ram` = the parent's co-rotating plasma**, not the stellar wind
(`:1067-1069`). Regime list `:1150-1176`; sub-regime 3b has "No Solar-System exemplar (low
conf)" (`:1170`).

### Worked-example numbers (`:1146-1148` validation, `:1177-1205` examples)

| body | inputs printed | output printed |
|---|---|---|
| Earth | B_eq 31 µT, P_ram ≈ 2 nPa | R_mp/R_p ≈ 9.6 (obs ~10) ✓; inner ~1.2 R_E, outer ~3–7 R_E |
| Jupiter | ~4.3 G equatorial + Io source | belts at/past the K–P limit — "intensity ≠ f(B)" |
| A b (Polyphemus) | 170 µT vs α Cen A wind ram **0.38 nPa** | R_mp ≈ 22 R_p (board's independent 23.5) |
| A b (Kerbalism) | A b I volcanism ~820× Io (source) vs ring + 5 moons (loss) | Jupiter template: `radiation_inner` ~300 rad/h, lesser outer, `radiation_pause` ~−0.01 |
| A b inner belt (Part C worked, `:665-669`) | peak at A b II's L = 2.07 R_p, 0.70 R_p below boundary, `inner_radius` 1.159 | `gradient` **1.65** (board still carries 3.3) |
| A b III (Pandora) | own 75 µT; standalone ~17 R_moon; compressed ~7×; 19× dominance | ~2.6 R_moon mini-magnetosphere; sits in the belt gap; `radiation_inner ≈ 4` rad/h |
| Proxima Cen d (`:176-178`) | one shell fitted L 1.0–5.0 | IoU 0.986, gradient 1.005, peak 5000 rad/h at 2.65 R_p = 0.35 R_mp |
| Polyphemus K–P check (`:395-399`, `:417-418`) | L = 2.07, B_local ≈ 129× Earth L=5, torus 10²–5×10³ cm⁻³ | 1 MeV ceiling ≥ 5×10²–10¹⁶× Earth's — never binding; 300 rad/h ≈ 29× Earth passes |
| Pandora belt (`:419`) | source-starved | 0.4× Earth, plain regime call |

## 2. stellar_wind — where n_sw · v_sw · p_ram could come from

`grep -ril "stellar wind\|항성풍\|p_ram" docs/reference/` returns exactly three files:
`lism-kinematics.md`, `planetary-magnetosphere-geometry-methodology.md`,
`solar-system-radiation-belts.md`.

**No document prints a recipe for n_sw or v_sw.** What exists:

| where | what is printed | status |
|---|---|---|
| magnetosphere doc `:82` | `P_ram = ρ v²` — the *definition*, ρ and v unresolved | definition only |
| magnetosphere doc `:1146`, `:1148` | P_ram used as a **given**: Earth ≈ 2 nPa, α Cen A 0.38 nPa @1.6 AU | inputs, not derivations |
| `solar-system-radiation-belts.md:582` | "Useful for exoplanets, where `P_dyn` follows from the stellar wind." | a pointer with no formula |
| `phase3/stellar_wind_synthesis/context-notes.md:28-30` | astrosphere standoff `r_ap ∝ sqrt(Ṁ·v_w / (n_ISM·V_ISM²))`, reduced to `r_ap,star = 120 AU · sqrt(Ṁ_rel) · (V_ISM,⊙/V_ISM,star)` with **`v_w = 400 km/s` (Wood's universal assumption)** and `V_ISM,⊙ ≈ 26 km/s` | this is the *astrosphere nose*, not a planet-orbit p_ram |
| same file `:64` | `stellar_wind_speed_kms = 400` (assumed, Wood) unless measured | **this is the only v_sw value in the repo, and it is an assumption** |
| `scripts/refs/magnetopause_geometry.py:34,42-49` | `P_SOLAR_1AU_NPA = 2.0` and `ram_pressure_nPa(mdot_sun, a_au) = 2.0 · Ṁ/a_AU²` | **implemented convention.** Its own docstring states the assumption: "the speed cancels between the mass flux and the v² factor only if it is held equal to the solar value, which is what every board in this repo assumes" |
| `phase4/magnetopause-regate/context-notes.md:11` | "Both Proxima boards scale the stellar wind as `p = 2.0 nPa × (Mdot/Mdot_sun) / a_AU²`" — recorded Proxima b 170 nPa @0.04848 AU, Proxima c 0.178 nPa | the convention's audit trail; α Cen A b comes out 0.3906 nPa (`:23`) vs the board's stated 0.38 (`:24`) |

So: **p_ram has an implemented convention with a stated assumption and no bibcode for its
2.0 nPa solar anchor; n_sw has nothing at all; v_sw has one assumed constant (400 km/s,
attributed to Wood).** The continuity step that would give n_sw from Ṁ
(`n = Ṁ/(4π r² v m_p)`) is not printed anywhere I could find.

**Existing data fields (grep only, no reads of values beyond what is shown):**
- `db/systems/*.json`: `mass_loss_measurements[]` (e.g. `alpha_centauri_a.json:219`) and
  `mass_loss_solar` (`:280`, value 2.0 for the α Cen pair). Same `mass_loss_measurements`
  block in `db/stellar_props_curated.json` at lines 1596, 1974, 3223, 3509, 3867.
  Files carrying stellar-wind fields: `alpha_centauri_a`, `barnards_star`, `proxima_cen`,
  `eps_ind_a`, `tau_cet`.
- `phase4/*.yaml`: axis `environment.stellar_wind`, rows `{ name: stellar_wind, value: …,
  unit: Mdot_sun }` (e.g. `phase4/alpha_centauri.yaml:1045,1058` A = 0.5 Ṁ⊙;
  `:1176,1189` B = 1.5 Ṁ⊙). `:1067` records the ripple "A b magnetosphere ram
  0.75→0.38 nPa @1.6 AU, R_mp 21→~23.5 R_p".
- `phase3/stellar_wind_synthesis/checklist.md:14-19`: per-host Ṁ and standoff already
  synthesized for α Cen A, Proxima, τ Cet, 40 Eri A, ε Ind A.
- `docs/reference/lism-kinematics.md:23,87`: `mass_loss_solar` used for astrosphere size;
  `:23` notes X-ray-derived mass-loss is kept separate (Kislyakova 2024 `2024NatAs...8..596K`).

## 3. Where each declared input comes from in chain.yaml today

`magnetosphere_geometry` inbound edges (`chain.yaml:739-753`):

| via | from | that node's kind / recipe | edge status |
|---|---|---|---|
| `p_ram` | `stellar_wind` | `computed`, **no recipe key** (`:384-388`) | plain requires (`:739`) |
| `b_eq` | `dynamo_giant` | `computed`, recipe `planetary-dynamo-scaling` | requires (`:740`) |
| `b_eq` | `dynamo_rocky` | `computed`, recipe `rocky-planet-dynamo-methodology` | requires (`:741`) |
| `regime` | `dynamo_rocky` | as above | selects (`:742`) |
| discriminator `ionosphere` | `atmosphere_choice` | — | selects; note says the consumer forms it from pressure·composition (`:743`) |
| discriminator `plasmasphere_slot` | `atmosphere_choice` | — | selects (`:744`) |
| (orbit) | `orbit_elements` | layer 0, `measured`, outputs `[a,e,i,lan,aop,n]` | influences, sign negative (`:745`) |
| `power`, scope parent | `tidal_heating` | `computed`, recipe `tidal-heating-methodology` | requires (`:746-752`) |
| (ring sweeping) | `ring_system` | — | influences, **status: gap** (`:753`) |

`stellar_wind` inbound: **one edge only** — `system_age → stellar_wind via t_sys`
(`chain.yaml:738`, with the comment at `:736-737` explaining that the previous
`star_physical via age` edge pointed at an output no node emits).

**Inputs the doc/script need that have no chain edge (flagged separately as asked):**

| needed quantity | needed by | nearest chain node | why it is missing |
|---|---|---|---|
| `Ṁ` (mass-loss, Ṁ⊙) | `ram_pressure_nPa` and the whole p_ram convention | `star_physical` outputs `[mass, radius, teff, luminosity, sed, v_sin_i, p_rot]` (`chain.yaml:78`) — **no `mass_loss`**; `grep mass_loss chain.yaml` returns nothing | the DB carries `mass_loss_measurements` / `mass_loss_solar`, but no node declares it as an output, so there is no edge to draw |
| `a` (orbital distance, AU) | same convention (`p ∝ 1/a²`) | `orbit_elements.a` exists (`:100`) and already edges to `magnetosphere_geometry` (`:745`) — but **no `orbit_elements → stellar_wind` edge** | p_ram is per-planet, yet `stellar_wind` is wired as if it were star-level |
| `v_w` | `P_ram = ρv²`, and n_sw if ever derived | none | assumed 400 km/s in `phase3/stellar_wind_synthesis/context-notes.md:64` |
| `n_cold` (cold-plasma density at the belt) | the K–P check `kp_limit.py` (`:391`, `:417`) | none | the doc calls it "a stated assumption" for a fiction torus (`:423-424`) |
| `ℓ` (dominant harmonic degree) | `deform_scale = k/5`, `k = ℓ/R_mp` (`:784`) | `dynamo_*` emit `regime` / `ladder_regime`, not `ℓ` | ⚗ plugin-pending field |
| `magnetic_dipole_tilt_deg` | `geomagnetic_pole_lat/lon` (`:697`) | not an output of any node in the parsed node list | — |
| `spe_fluence` (adjacent, for contrast) | `surface_dose` | `star_physical`, **status: gap** already declared (`chain.yaml:786`) | shows the house style for exactly this situation |

## 4. Places the doc itself leaves open (quoting only its own sentences)

- `:195-196` — induced standoff: "Adopt `1.05–1.2 R_p` for an Earth-to-Venus-class
  atmosphere and **say which end you took**; there is no useful field parameter to derive
  it from."
- `:219` / `:223` — the published induced boundary form "is **not implemented**", and the
  fallback rule is "**only where Shue geometrically cannot represent the boundary**, or
  where **no fitted α exists** to use."
- `:414-416`, `:423-424` — the rad/h interpolation "is an **empirical dose-anchor
  interpolation** … it is *not* the K–P scaling"; "Confidence remains low — the
  interpolation exponent is a two-anchor fit, and **n_cold for a fiction torus is a stated
  assumption**".
- `:349-352` — "Belt intensity therefore stays a **regime call with a stated source and
  loss**, not a formula output."
- `:765-773` — "### ⚗ Fields that do not exist yet — the KerbalismShuePause plugin … Five of
  the knobs the belt viewer exposes are **not consumed by any shipped Kerbalism**", kept in
  `PENDING_MODEL_KEYS` and "**never** written as cfg lines".
- `:871` — "Recorded as ⚗ pending" (the compression/extension deformation case).
- `:1170` — sub-regime 3b: "**No Solar-System exemplar (low conf)**."
- `:1201-1205` — "belt intensity is **low** by nature … which is exactly why it is a
  documented regime call rather than a computed number."

## 5. ⚠ check_paper_held.py reports a false ABSENT for this doc's core sources

I queried 24 bibcodes; **3 HELD, 21 ABSENT**. But three of the ABSENT ones are on disk under
descriptive filenames, which is a **fourth cache naming class** beyond the three the tool's
own docstring records (bibcode, arXiv new/old, `&`→`_`):

- `2010JGRA..11512220M` (Mauk & Fox) → `mauk_fox_2010_electron_belts.pdf` (+ `mauk_fox_2010.json`, `mauk_fox_KP_run.pdf`, `mauk_fox_KP.nb`, `mauk_fox_KP_doc.docx`)
- `2009JGRA..11410210S` (Summers, Tang & Thorne) → `summers_tang_thorne_2009_kp_limit.pdf`
- `2014JGRA..119.6313S` (Summers 2014) → `summers_2014_limiting_spectrum.pdf`
- `1997JGR...102.9497S` / `1998JGR...10317691S` (Shue) → `_shue1997.pdf` / `_shue1998.pdf`
  — a **fifth** class: leading underscore + author-year.

The doc's own claim at `:367-369` ("With the three source papers in the local cache … 
owner-downloaded PDFs in `docs/phase3/_papers/`") is therefore correct, and the ABSENT lines
are the tool's naming blind spot, exactly as its docstring warns
(`scripts/refs/check_paper_held.py:29-33`: "DOUBT THAT THIS TOOL KNOWS EVERY CACHE NAMING
RULE … when a paper you can see on disk comes back ABSENT, the 'checked …' list says which
names were tried — compare it with `ls` before believing it"). I did not verify the
remaining 16 ABSENT bibcodes against `ls`; the ones I grepped for by author keyword
(chapman, ferraro, kennel, lenchek, schulz, bagenal, divine, garrett, cooper, ripoll,
bertucci, brace, martinecz, kivelson, heller, zuluaga, mourenas, seltzer) produced no hits
other than `kennel_petschek_recipe.md`, which is a generated recipe note, not the 1966 paper.
