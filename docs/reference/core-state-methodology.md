<!-- 핵이 다이나모를 돌릴 수 있는 액체인가 — 핵의 압력·온도를 철의 융해곡선에 대는 방법(논문 근거) -->
# Core state grounding: is the metal core a conducting liquid

[Interior structure](interior-structure-methodology.md) solves the core's **geometry**.
Whether that core can run a dynamo is a separate question with separate literature: the
rocky-dynamo recipe asks for "convective buoyancy flux through a conducting liquid-iron
core", and the word that matters is *liquid*. This recipe answers it by putting the core's
pressures and temperatures against the melting curve of iron.

## Contract — `core_state`

**Returns** — `conductor_phase` [—] · `cmb_melt_temperature` [K] ·
`center_melt_temperature` [K] · `core_cmb_temperature_used` [K] ·
`core_center_temperature_used` [K] · `icb_pressure` [GPa] ·
`center_margin` [K] · `cmb_margin` [K] · `center_margin_fraction` [—] · `gamma_flip` [—] ·
`gamma_flip_in_alfe_range` [—] · `k0_flip` [GPa] · `melt_splice_disagreement` [—] · `margin_condition` [—]
**Needs** — `core_pressure` [GPa] · `cmb_pressure` [GPa] · `core_temperature` [K] ·
`cmb_temperature` [K] · `core_material` [—] · `core_cmb_temperature` [K] ·
`body_class` [—]
**Discriminating keys** — whether `core_cmb_temperature` is declared, which selects the
bound branch or the adiabat branch; and the central pressure, which selects the melting
curve's piece.
**Grade** — never better than **analog**, dropping to **judgment** where the verdict is
`undecided`. Every path leans on a temperature this recipe cannot derive: with the
declaration it uses it directly, without it, it reads another recipe's geotherm as a bound.

`conductor_phase` is one of `liquid`, `solid`, `liquid_outer_solid_inner` and `undecided`.
`icb_pressure` is 0 when there is no inner-core boundary inside the core.
`k0_flip` null means **not computable** — a multi-phase core material, or no sign change of the centre margin within 0.5–2× K₀. It does not mean "no flip exists". `gamma_flip`, `gamma_flip_in_alfe_range` and `k0_flip` are null on the lower-bound branch, where there is no core adiabat to flip; `melt_splice_disagreement` is null outside the two iron fits' overlap (300–365 GPa). `margin_condition` is `thin` when `gamma_flip` lies inside Alfè+ 2002's own γ span 1.50–1.52 (solid 1.5; liquid 1.51–1.52 at 280–340 GPa), `comfortable` otherwise, or the named not-computable label.

`core_cmb_temperature` is the **core-side** temperature at the core-mantle boundary, and it
is a declaration in the same sense as `potential_temperature`, `initial_porosity` and
`envelope_z`: what sets it is the heat flux across the D″ thermal boundary layer, which is
`internal_heat_nontidal`'s output and does not exist yet. The edge is recorded in
`chain.yaml` as a gap for exactly that reason.

## The relation

Two curves, and the verdict is where they cross.

    T_melt(P)                       ← the melting curve of the core material
    T(P) = T_cmb · (ρ(P)/ρ_cmb)^γ   ← the core's adiabat, γ constant

The adiabat is the closed form of `dT/dP = γT/K_S` when γ does not vary, which is what the
ab-initio result below says for iron at core conditions. Where `T > T_melt` the metal is
liquid; where `T < T_melt` it is solid; a single crossing between the core-mantle boundary
and the centre is an inner-core boundary, and its pressure is returned.

The melting curve is steeper than the adiabat over this whole range, so the crossing is
always centre-side: crystallisation starts at the centre, as it does on Earth.

## Why the geotherm is used as a bound

`interior_layers` integrates one adiabat from the surface to the centre, so its core sits on
the **mantle's** adiabat. Two things are missing from that, and both have names.

The **D″ thermal boundary layer**. Unterborn+ 2019's eq. 7, the published check the interior
recipe's temperature is anchored on, is a mantle adiabat, and its 2635 K at 1 R⊕ is the
mantle-side value: that paper compares it against Lay+ 2008's 2500–2800 K "as determined
using a similar method to ours". The core-side value on Earth is 3760 ± 290 K. The jump is
over 1200 K, it is set by the CMB heat flux, and this repository does not derive that flux.
Zhang & Rogers 2022 report it as ~240 K for a 1 M⊕ planet and ~1880 K for 3 M⊕ **in their
models**, which is the point: it is model-dependent.

The **iron adiabatic slope**. `eos.py` closes γ as an identity from αK_T and c_V, which
matches SeaFreeze's own γ for the ices to four decimals. For iron that identity is fed
Seager+ 2007's αK₀ = 0.00121 GPa/K, a thermal-pressure constant chosen to get densities
right, and it lands at γ ≈ 0.22 at core pressures against the ab-initio 1.5.

Both biases point **down**, so the number is a lower bound rather than noise. A lower bound
supports a one-sided verdict, and that is the recipe's first branch: if the melting
temperature at a depth is below the bound, the material there is liquid and no boundary
layer can undo it, because a boundary layer only adds heat. The converse does not follow, so
that branch never returns `solid`.

The **−17 % drift** the interior recipe records for its adiabat above 1.05 R⊕ moves in the
same safe direction: a lower bound that runs lower still yields fewer `liquid` verdicts and
more `undecided` ones, never a wrong `liquid`. The declared branch does not read the mantle
adiabat at all, so the drift does not reach it.

## Constants

| quantity | value | validity | source |
|---|---|---|---|
| iron melting, P ≤ 365 GPa | T_m = 1825 K (1 + P/57.723 GPa)^0.654 | fitted to 365 GPa; 1825 K at P = 0 against a measured 1811 K | Zhang+ 2015, abstract |
| iron melting, P > 365 GPa | T_m = 6469 K (1 + (P − 300 GPa)/434.82 GPa)^0.54369 | 300–5000 GPa; above 5 TPa the recipe declines | González-Cataldo & Militzer 2023, abstract |
| light-element depression | ×0.80 on `fe_prem`, none on `fe_eps` | a declaration, not a derivation | Stevenson+ 1983 convention, as used by Zhang & Rogers 2022 |
| core Grüneisen γ | 1.5 | checked at 100–300 GPa and 4000–6000 K; 1.51–1.52 on the liquid Hugoniot at 280–340 GPa | Alfè, Price & Gillan 2002 |

The two melting pieces overlap on 300–365 GPa and differ by **4.0 to 7.5 %** there, the
González-Cataldo piece being the higher. That is narrower than the disagreement between the
two static-compression experiments at the same pressure (Anzellini+ 2013's 6230 ± 500 K
against Sinmyo+ 2019's 5500 ± 220 K, 13 % apart), so the pieces are spliced where the first
one's authors stop it rather than averaged, and the gap is measured by the test rather than
asserted.

The depression is applied to `fe_prem` and not to `fe_eps` because that split already exists
in the equation of state: `fe_prem` is a fit to PREM's outer core and therefore contains the
light elements already, while `fe_eps` is laboratory pure ε-iron. The 20 % is the convention
published thermal-evolution models use. An independent check lands beside it: Sinmyo+ 2019's
Earth inner-core-boundary temperature of 5120 ± 390 K against the pure-iron curve's 6331 K at
329 GPa is a 19.1 % depression. The two are not the same statement, so the agreement is a
consistency check and not a derivation.

## Validation

Earth is the decision line, because its core's two layers are measured. Every number in the
right-hand column is published, and none of it is this engine's output. Regenerated by
`python3 engine/test_core_state.py --table`.

| quantity | derived | published | source | Δ |
|---|---|---|---|---|
| CMB pressure | 135.2 GPa | 135.75 GPa | PREM | −0.4 % |
| core temperature at the PREM ICB | 5121 K | 5120 ± 390 K | Sinmyo+ 2019 | +0.0 % |
| ICB pressure | 352 GPa | 328.85 GPa | PREM | +7.0 % |
| conductor phase | liquid_outer_solid_inner | liquid outer core, solid inner core | seismology | – |

The second row is the check on γ: Sinmyo+ 2019 give two points on one Earth core adiabat, and
integrating from the first at γ = 1.5 reproduces the second. The third row is the honest
residual: near the centre the adiabat and the melting curve run almost parallel, so a 1 %
shift in melting temperature moves the boundary by tens of GPa, and the two experiments above
disagree by 13 %.

## Domain of validity

| regime | condition | what this recipe does | grade |
|---|---|---|---|
| declared core-side CMB temperature | `core_cmb_temperature` > 0 | integrates the core adiabat and returns `liquid`, `solid` or `liquid_outer_solid_inner` with the boundary's pressure | analog |
| **no declaration, bound above the curve** | melting temperature below `cmb_temperature` and `core_temperature` | returns `liquid`. The missing heat only adds, so the verdict cannot be undone by supplying it | analog |
| **no declaration, bound below the curve** | anything else | returns `undecided`, never `solid`: the bound is one-sided. The reason names the declaration that would settle it | judgment |
| no temperature at all | `potential_temperature` unset upstream | **declines**: the interior solution is isothermal and there is no geotherm to compare | — |
| **adiabat above the checked γ range** | central pressure above 340 GPa | integrates, with a note: γ is carried as a constant past the pressures Alfè+ 2002 confirmed it at | analog |
| **centre past the melting curve** | central pressure above 5 TPa | **declines**, naming the curve's end. The equations of state reach 12 TPa and the melting curve stops at 5 | — |
| coreless or undifferentiated | CMB pressure at or above the central pressure | **declines**: metal mixed through silicate has a solidus and a liquidus, not one melting point | — |
| core material with no curve | anything but `fe_prem` / `fe_eps` | **declines**, naming the material | — |
| giant, ice giant, sub-Neptune, brown dwarf, star | `body_class` | **declines**: those dynamos run on metallic hydrogen, which is `dynamo_giant`'s branch and has nothing to do with iron's melting curve | — |
| **inverted crossing** | adiabat below the curve at the boundary and above it at the centre | **declines**: the melting line is steeper than the adiabat everywhere in this range, so this arrangement means the inputs disagree, not that the core is inside out | — |

## Sources

- **Zhang, W.-J., Liu, Z.-Y., Liu, Z.-L. & Cai, L.-C. 2015**, Phys. Earth Planet. Inter.
  244, 69 ([`2015PEPI..244...69Z`](https://ui.adsabs.harvard.edu/abs/2015PEPI..244...69Z)).
  The Simon fit this recipe uses below 365 GPa, printed in the paper's own abstract, with the
  6345 K inner-core-boundary melting point it implies. *No arXiv preprint*: verified by
  bibcode.
- **González-Cataldo, F. & Militzer, B. 2023**, Phys. Rev. Research 5, 033194
  ([`2023PhRvR...5c3194G`](https://ui.adsabs.harvard.edu/abs/2023PhRvR...5c3194G)). The
  ab-initio melting line for 300–5000 GPa and its Simon fit, again in the abstract, together
  with the statement that the melting line is steeper than the adiabat so crystallisation
  always starts at the centre. *No arXiv preprint*: verified by bibcode.
- **Kraus, R. G. et al. 2022**, Science 375, 202
  ([`2022Sci...375..202K`](https://ui.adsabs.harvard.edu/abs/2022Sci...375..202K)). Iron's
  melting point measured to 1000 GPa at the National Ignition Facility, the experiment the
  high-pressure fit above is checked against, and the paper that ties core solidification to
  dynamo lifetime for 4–6 M⊕ planets. *No arXiv preprint*: verified by bibcode.
- **Anzellini, S., Dewaele, A., Mezouar, M., Loubeyre, P. & Morard, G. 2013**, Science 340,
  464 ([`2013Sci...340..464A`](https://ui.adsabs.harvard.edu/abs/2013Sci...340..464A)). One
  of the two experimental anchors at the inner-core boundary, 6230 ± 500 K. *No arXiv
  preprint*: verified by bibcode.
- **Sinmyo, R., Hirose, K. & Ohishi, Y. 2019**, Earth Planet. Sci. Lett. 510, 45
  ([`2019E&PSL.510...45S`](https://ui.adsabs.harvard.edu/abs/2019E%26PSL.510...45S)). The
  other anchor, 5500 ± 220 K, and the pair of Earth core temperatures the validation uses:
  3760 ± 290 K at the core-mantle boundary and 5120 ± 390 K at the inner-core boundary. *No
  arXiv preprint*: verified by bibcode.
- **Alfè, D., Price, G. D. & Gillan, M. J. 2002**, Phys. Rev. B 65, 165118
  ([`2002PhRvB..65p5118A`](https://ui.adsabs.harvard.edu/abs/2002PhRvB..65p5118A), arXiv
  **[cond-mat/0107307](https://arxiv.org/abs/cond-mat/0107307)**). **Cached** in
  `docs/phase3/_papers/cond-mat_0107307.md`. The constant core Grüneisen parameter: γ "varies
  little with pressure or temperature for 100 < p < 300 GPa and 4000 < T < 6000 K, and has a
  value of ca. 1.5", and 1.51–1.52 on the liquid Hugoniot.
- **Zhang, J. & Rogers, L. A. 2022**, ApJ 938, 131
  ([`2022ApJ...938..131Z`](https://ui.adsabs.harvard.edu/abs/2022ApJ...938..131Z), arXiv
  **[2208.06523](https://arxiv.org/abs/2208.06523)**). **Cached** in
  `docs/phase3/_papers/2208.06523.md`. The 20 % light-element depression as a working
  convention, and the CMB temperature jumps (~240 K at 1 M⊕, ~1880 K at 3 M⊕) that show the
  boundary layer is real, large and model-dependent. Its own transcription of Zhang+ 2015's
  Simon coefficients differs from that paper's abstract, which is why the coefficients here
  are read from the primary.
- **Dziewonski, A. M. & Anderson, D. L. 1981**, Phys. Earth Planet. Inter. 25, 297
  ([`1981PEPI...25..297D`](https://ui.adsabs.harvard.edu/abs/1981PEPI...25..297D)). PREM,
  which supplies the core-mantle and inner-core boundary pressures the validation compares
  against.

## Related

- [Body class](body-class-methodology.md) — derives the `body_class` key this recipe declines the six coreless classes on, and contrasts it against the declared one
- [Interior structure](interior-structure-methodology.md) — supplies the core pressures and
  the geotherm this recipe reads as a bound, and documents the water melting curve
- [Rocky-planet dynamo](rocky-planet-dynamo-methodology.md) — the consumer: it needs a
  conducting liquid core, and `conductor_phase` is what says whether there is one
- [Internal heat and luminosity](internal-heat-luminosity-methodology.md) — where the CMB
  heat flux that would replace the declaration has to come from
- [Derivation discipline](derivation-discipline.md) — why declining is a return value
