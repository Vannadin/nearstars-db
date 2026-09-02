<!-- 규산염 액체 전기전도도 서베이 ⑱ 기록 — 두 논문이 조건에서 겹치지 않아 교차검증이 없다 -->
# Electrical conductivity of silicate liquid — what survey ⑱ measured (context notes)

2026-09-03. **Documentation only** — preserving the parallel seat's survey ⑱ (two cached
papers, both silicate *liquid*, both ab initio) before it evaporates with a session. No code
touched; nothing in `eos.py` or `dynamo.py` carries an electrical conductivity today, and this
note does not change that — **it is the grounding a Brief 39 on the electrical axis would
consume, not an adoption.** Verifiers per item: (병) = parallel seat measured, (직) = directing
seat reproduced, (여기) = work seat re-read from the cached PDF or recomputed before landing.

Both papers are in `docs/phase3/_papers/`, title-checked: `2018NatCo...9.3883S.pdf`
(Soubiran & Militzer, *Electrical conductivity and magnetic dynamos in magma oceans of
Super-Earths*, [ADS](https://ui.adsabs.harvard.edu/abs/2018NatCo...9.3883S)) and
`2020NatCo..11..935S.pdf` (Stixrude, Scipioni & Desjarlais, *A silicate dynamo in the early
Earth*, [ADS](https://ui.adsabs.harvard.edu/abs/2020NatCo..11..935S)). Line numbers below are
`pdftotext` (no `-layout`) extraction lines of those files.

## 1. The headline: the two papers never overlap in condition — there is no cross-check

| | Soubiran & Militzer 2018 | Stixrude+ 2020 |
|---|---|---|
| composition | MgO · SiO₂ · MgSiO₃, **iron-free** | bulk silicate Earth, **Fe/(Fe+Mg) = 0.11** (line 330) |
| conditions | three points, lowest **240 GPa / 7 000 K** | simulated box **100–140 GPa × 4 000–6 000 K** (line 19) |
| output | three DC values | an evaluable fit (§3) |

The gap is **100 GPa and 1 000 K** between Soubiran's lowest point and Stixrude's highest
corner, and the compositions differ in the one variable both papers name as dominant
(iron: Stixrude line 47, "the conductivity of the silicate liquid is greater than that of
SiO₂ because of the role of iron"). The abstract-level agreement — "of the order of
100 Ω⁻¹cm⁻¹" against "exceeds 10 000 S/m", the same order after unit conversion — is
**arithmetic on two numbers whose conditions were never paired**, and it does no work.

**Inadmissible extrapolation, recorded so nobody re-derives it hopefully** (병, 직, 여기):
pushing Stixrude's fit to Soubiran's MgSiO₃ point (240 GPa / 7 000 K) gives **328.2 Ω⁻¹cm⁻¹
(spin-polarized σ₀) or 369.4 (non-spin-polarized) against Soubiran's 216** — a factor 1.52 on
the spin-polarized branch. Inadmissible because it is 100 GPa and 1 000 K outside the fitted
box *and* iron-bearing against iron-free, two errors pushing opposite ways; the 1.52 is not a
measurement of anything.

**Lead, now in the cache and not yet read**: `2017PNAS..114.9009S` (Scipioni, Stixrude &
Desjarlais, *Electrical conductivity of SiO₂ at extreme conditions and planetary dynamos*) is
the only known place the two lineages meet at a shared composition — Soubiran cites it as
ref. 43 (line 429). Its three authors are **exactly the Stixrude 2020 author list** (ADS, both
bibcodes, 여기), so it is a shared-composition bridge to Soubiran, **not an independent check on
Stixrude**. Obtained by the owner 2026-09-03 with `.PROVENANCE.txt`; with the parallel seat.

## 2. Soubiran & Militzer 2018 — three DC points, no deposit

Method: DFT-MD + Kubo–Greenwood, DC value by linear extrapolation of σ(ω) to zero frequency.
Iron-free end-members, each at one liquid (P, T) chosen near the melting curve / Hugoniot
(conditions lines 179–184; σ lines 427–429; 여기 read verbatim):

| liquid | P / T | σ_DC (Ω⁻¹cm⁻¹) | solid companion (Ω⁻¹cm⁻¹, line 419) |
|---|---|---|---|
| MgO | 470 GPa / 12 000 K | **336** | 160 (B2) |
| SiO₂ | 500 GPa / 9 000 K | **488** | 90 (pyrite) |
| MgSiO₃ | 240 GPa / 7 000 K | **216** | 15 |

The abstract's *"of the order of 100 Ω⁻¹cm⁻¹"* is a **summary of those three, not a fourth
measurement** — do not carry it as a value.

**Data availability** (lines 828–831, 여기): *"available upon request … They are not publicly
available because of the large size of the output files."* No deposit exists; more points mean
author contact, which is the owner's call.

**Self-closure check** (병, 직, 여기): the printed Lorenz numbers (lines 452–453: 7.7 / 6.4 /
5.3 ×10⁻⁸ WΩ/K²) close on the paper's own σ and k (§4) to ≤ 0.4 % — recomputed 7.688 /
6.375 / 5.291 ×10⁻⁸ — so six printed numbers validate against a seventh. Magnetic diffusivity
η = 1/(μ₀σ) printed as **16–40 m²/s** (line 624; the 15.9 / 39.8 recomputed by 병 are the
σ = 500 / 200 Ω⁻¹cm⁻¹ endpoints) and, with Rm ≳ 40 (ref. 11 = Olson **2016**, see §5) and an
eddy size l ~ 10⁶ m, an onset velocity **v ~ 0.6–1.6 mm/s** (line 629; 0.64 / 1.59 recomputed).

## 3. Stixrude+ 2020 — an evaluable fit, and the transcription trap

Fig. 1 caption (page 2, 여기 read **as a page image**):

    σ = σ₀ · T⁻¹ · exp[ −(E* + P·V*) / (R·T) ],   σ_total = σ_el + σ_ion

| term | σ₀ | E* (kJ/mol) | V* (cm³/mol) |
|---|---|---|---|
| electronic, non-spin-polarized | 1.994×10⁹ | 108.6 | 0.0611 |
| electronic, spin-polarized | 1.754×10⁹ | 108.6 | 0.0611 |
| ionic | 1.0811×10⁹ | 131.0 | 0.437 |

Composition bulk silicate Earth, Fe/(Fe+Mg) = 0.11 (line 330). **Validity is the simulated
box: 100–140 GPa × 4 000–6 000 K** (line 19). The main figure's continuation down to
≈ 50 GPa / ≈ 2 500 K is the fit read along an isentrope, not simulated points.

⚠ **`pdftotext` drops both minus signs from that exponent.** Extraction line 178 reads
`exp½ðE þ PV Þ=RT` — the leading minus and the sign structure are gone. With the sign wrong
(직, 여기, each recomputed):

| condition | terms | wrong-sign σ (S/m) |
|---|---|---|
| 100 GPa / 4 000 K | electronic, non-spin-polarized, alone | 1.57×10⁷ |
| 120 GPa / 5 000 K | electronic spin-polarized + ionic | 2.35×10⁷ |
| 140 GPa / 4 000 K | electronic spin-polarized + ionic | 1.02×10⁸ |

Every one is one to two orders above the **10⁶ S/m** the paper's own sentence names for the
metallic outer core — *"although less than typical metallic conductivity (10⁶ S/m for the
Earth's outer core)"* (line 90) — so **the sign is settled by the paper at every condition and
branch combination tried; the refutation does not hang on one number.** Same family as the
IF97 extraction failure (`engine/steam-context-notes.md`): **read the caption as a page image,
never from the text layer.**

**Units, not an index row**: the caption gives σ₀ in **S/m** while the printed form requires
**S·K/m**. Units-only; following the equation gives the right magnitude, so it cannot silently
produce a wrong answer. Left out of `docs/reference/paper-defects.md` deliberately (병 proposed,
직 agreed).

**Fit reproduced over its own box** (병, 직 independently; 여기 recomputed with R = 8.314):
σ_total spans **13 779 – 34 752 S/m** on the spin-polarized branch (min at 140 GPa / 4 000 K,
max at 100 GPa / 6 000 K; 병/직 report 13 782 – 34 757, the difference is the gas-constant
rounding), consistent with the abstract's *"exceeds 10 000 S/m"*. Stixrude's illustrative
`Rm = 40 (v/1 cm/s)(L/300 km)(σ/10 000 S/m)` (line 86) evaluates to **37.7**, printed as 40 —
the paper's own words are *"using illustrative values"*.

**Calibration, in the displaced place** (line 531, 여기): Methods says *"The value of δ is
chosen to yield a present day temperature at the core–mantle boundary of 4000 K."* That is
upstream of the whole cooling history, so **Rm(t) and B(t) inherit a calibrated parameter —
but σ(P, T) itself does not.** The transcribable object is clean; the dynamo verdict built on
it is partly calibrated.

## 4. Rider payload — belongs to the thermal-conductivity axis, not this one

Soubiran also prints thermal conductivity for the same three liquid points (lines 439–440,
여기): **k = 31 / 28 / 8 W/(m·K)** for MgO / SiO₂ / MgSiO₃, and says the Wiedemann–Franz law
**underestimates k by a factor 2–3** here (lines 454–456, 699).

⚠ **8 W/(m·K) does NOT replace `tidal_transport.py`'s borrowed `k = 4.0`** (`IO_TABLE5`,
line 49). That 4.0 is Kankanamge & Moore 2019 Table 5's Io *mantle* value — solid, ~GPa,
~1 500 K; this 8 is *liquid* MgSiO₃ at 240 GPa / 7 000 K. Right quantity, wrong place. If the
thermal axis opens, this is one labelled point for it, not a substitute.

## 5. Defect found on the way — `paper-defects.md` #11

Soubiran's reference 11 prints *Geochem. Geophys. Geosyst.* 17, 1935–1956 **(2006)**; the
year is **2016** ([`2016GGG....17.1935O`](https://ui.adsabs.harvard.edu/abs/2016GGG....17.1935O),
Olson, P., confirmed through ADS by title; extraction line 875, 여기 read verbatim). That one
citation carries both the `Rm > 40` onset and the `Ro_ℓ ≤ 0.1` dipolar cutoff (lines 627–628,
650), so a session chasing "Olson 2006" lands in the wrong decade. No gate catches a citation
year.

## 6. What this means for `dynamo_rocky`

`chain.yaml:181` declares `dynamo_rocky` (recipe `rocky-planet-dynamo-methodology`, 11 edges:
9 wired, 2 recorded gaps, 5 of them `requires`) and **no module registers it**. An electrical
conductivity of the *silicate liquid* is an input a basal-magma-ocean dynamo would need; the
core dynamo needs the *iron* conductivity, which neither paper here prints. So this survey
grounds one candidate input to a node that does not exist, at conditions (≥ 100 GPa) that the
roster's moons never reach. **Nothing here is adoptable without a Brief that declares the
body, the layer and the (P, T) it is evaluated at, and says so on every value.**

## Related

- [`docs/reference/paper-defects.md`](../docs/reference/paper-defects.md) — #11
- [`engine/tidal-interior-context-notes.md`](tidal-interior-context-notes.md) — where `k = 4.0` was borrowed
- [`engine/SESSION-HANDOFF.md`](SESSION-HANDOFF.md) — "three missing properties"
