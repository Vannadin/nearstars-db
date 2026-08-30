# Reading Malamud & Prialnik 2015 — context notes (F3)

Third follow-up. C7 closed on a stated limit — *"only the abstracts were read … cannot say
whether it is transcribable"* — and C9 cited the same paper from its abstract. The full text
is in the cache; this item removes the limit. **No code moved.** C7 and C9 stay closed.

## Provenance

Malamud, U. & Prialnik, D. 2015, *Modeling Kuiper belt objects Charon, Orcus and Salacia by
means of a new equation of state for porous icy bodies*, Icarus 246, 21–36
([`2015Icar..246...21M`](https://ui.adsabs.harvard.edu/abs/2015Icar..246...21M), doi
[10.1016/j.icarus.2014.02.027](https://doi.org/10.1016/j.icarus.2014.02.027)). Read from
`docs/phase3/_papers/2015Icar..246...21M.pdf`; first page carries "Icarus 246 (2015) 21–36"
and the title above; the bibcode was checked by title. Text extracted with `pdftotext`; the
equations of §3.3, whose signs the extraction dropped, were re-read from a rendered image of
p. 26. Everything quoted below is from the full text unless marked *(abstract)*.

## Question 1 — is the treatment transcribable?

**Yes, and it was designed to be: the equation of state is an equilibrium closed form in
(P, T, X_d) with every coefficient printed.** Their §3.1.3: *"Since we are interested in the
equilibrium EOS, the compaction rate equation of Leliwa-Kopystyński and Kossacki (2000) is
incompatible with our calculation"* — the compaction curves are taken as equilibrium
porosity–pressure relations, not rates. The time axis lives in the *evolution code* (§4.2,
eqs. (10)–(16)) that consumes the EOS, not in the EOS itself.

The EOS, §3.3, eqs. (1)–(7), all in cgs with P in dyn/cm²:

| eq. | as printed | constants (Table 1 and §3.3) |
|---|---|---|
| (1) | ρ(P, T, X_d) = 1 / [ Z_w/(1 − ψ_w(P, T)) + Z_d/(1 − ψ_d(P, T)) ] | two-layer model: each solid compacts on its own curve, volumes add |
| (2) | Z_d = X_d / [X_d + (1 − X_d)(1 − X_ℓ)] · (X_u ρ_p + X_p ρ_u)/(ρ_u ρ_p) | ρ_u = 3.25 + 2.15×10⁻¹² P, ρ_p = 2.7 + 3.41×10⁻¹² P g/cm³ |
| (3) | Z_w = (1 − X_d)(1 − X_ℓ) / [X_d + (1 − X_d)(1 − X_ℓ)] · (X_a ρ_c + X_c ρ_a)/(ρ_a ρ_c) | ρ_a = ρ_c = 0.917 g/cm³ |
| (4) | ψ_w(T, P) = ψ_w0 exp(−β_w(T/T_m) √P) | ψ_w0 = 0.45 |
| (5) | ψ_d(P, T) = ψ_d0 exp(−β_d P) Γ(T) | ψ_d0 = 0.4, β_d = 1.28×10⁻¹⁰ cm² dyn⁻¹ |
| (6) | β_w(T/T_m) = β_w1 + β_w2 / (1 + exp(β_w3 (1 − T/T_m))) | β_w1 = 4.7434×10⁻⁵, β_w2 = 31.7434×10⁻⁵ cm dyn⁻¹ᐟ², β_w3 = 11 |
| (7) | Γ(T) = 1 / (1 + exp(15 (T_max/675) − 1)) — **as printed** | see the note below |

Subscripts: d rock (u unprocessed, p processed), a amorphous ice, c crystalline ice, ℓ liquid;
X are mass fractions; T_m is the ice melting temperature (the "homologous temperature" is
T/T_m). Eq. (1) prints ψ_d(h, T) where h is evidently P — a typographical slip, read as P.

**A transcription note on eq. (7).** As printed, the exponent is 15(T_max/675) − 1, which
gives Γ(675 K) = 8×10⁻⁷ and Γ(425 K) = 2×10⁻⁴. The text says the function *"declines from 1
to 0, around a temperature of 675 K"*, is *"centered exactly around a temperature of 675 K"*
(§5.2), and that below 425 K the compaction curve *"should be almost unaffected by
temperature"*. Only 15(T_max/675 − 1) does that: Γ = 0.996 at 425 K, 0.5 at 675 K, 0.004 at
925 K. A transcription must use the text-consistent form and say so; the printed form is a
typesetting error, not a second reading. **Γ takes T_max, the maximum temperature the shell
ever reached** — "thermal memory" (§3.2.2) — which is the one history variable in the EOS.

**Spot checks against the sources named in the text** (the fit reproduces what it says it
fits): ψ_w at 100 MPa, 70 K = 0.100 and at 120 K = 0.098 — Durham+ 2005's *"significant
porosity remained even with pressures in excess of 100 MPa"*; ψ_d at 80 and 764 MPa, cold, =
0.36 and 0.15 — the Leliwa-Kopystyński+ 1994 range. Sensitivity from the paper's own §6:
*"Increasing the coefficients by 50%, or decreasing them by the same amount results in
differences in the model bulk densities of only 1% and 3%, for rock and ice respectively."*

**Data and sources.** No data are published and no repository is pointed to; nothing is
needed, because the fit is the product. The porosity curves are fits to three experimental
papers — Durham, McKinnon & Stern 2005 (GRL 32, L18202; cold ice, 70 and 120 K, to 150 MPa),
Yasui & Arakawa 2009 (JGR Planets 114, E09004; warm ice and ice–silica, 206 and 263 K) and
Leliwa-Kopystyński+ 1994 (PSS 42, 545; lherzolite grains, 213 K, 80–764 MPa) — reachable in
principle (two AGU, one Elsevier), not fetched here, and needed only for a grade above
"transcribed fit". The grain densities are shock EOS (Watt & Ahrens 1986 enstatite; Tyburczy+
1991 serpentine) linearised in P; a transcription would not carry these — the engine's own
Birch–Murnaghan silicate and Hilairet antigorite are the better grain EOS, and the paper's
own choice of 2.7 g/cm³ for processed rock lands where Hilairet's ρ₀ = 2640 does.

**Where the source reaches — the stated limits.**

- Pressure: fits to 150 MPa (ice) and 764 MPa (rock); Fig. 3 plots the EOS to 800 MPa.
  Bodies *"with radii of a few hundred km"* (abstract and §1); the sample is 427–604 km.
- Ice phase: *"the objects considered in this paper are not large enough to permit any ice
  phase other than ice-I"* (§3.1.2); the compaction data are ice-I data.
- Rock: no rock melting, *"objects larger than Charon are excluded"* (§2); Γ is centred at
  675 K and the authors call the temperature correction *"hypothetical, yet relies on strong
  and consistent observations"* (§3.2.2). Grain sizes are millimetre (rock) and millimetre
  ice grains; the paper says grain size and texture *"remain unclear"* (§6).
- Timescale: the curves are laboratory compaction. The text says *"the kinetics of compaction
  is extremely slow in nature"* and uses the low-temperature lab curve as the baseline with
  the Γ correction standing in for geologic time. So ψ_d is a **lab-cold upper bound** on
  rock void below 675 K — the same character Bierson's relation has in this recipe — and
  creep (C9's Neumann branch) would close it further.

At Callisto's and Titan's core pressures (2.73 and 3.28 GPa) eq. (5) is beyond its range and
gives ψ_d ≈ 0.01 and 0.006 even cold: **the EOS does not deliver void space in those cores.**
In the outer few hundred km (P ≲ 0.3–0.6 GPa) it is inside its pressure range, outside its
ice-I range beyond ~0.2 GPa, and gives ψ_w ≲ 0.03 and ψ_d ≤ 0.27 (cold, lab). So the
*deciding region* of C10's three moons — the core — is not reached; the crust is.

## What the full text does to C7's two reasons

**"It is a reaction" — confirmed, and bounded to where liquid water reached.** §4: *"We take
into account serpentinization, the transition of unprocessed rock into chemically processed
rock by absorption of liquid water. The resulting heat release, in the amount of 2.5×10⁹
erg g⁻¹ … The reaction involves a change in the rock's specific density by 20% and local
depletion of water. The serpentinization reaction continues only so long as there is
available liquid water. At temperatures below melting point, or when water has migrated out,
the rock will remain unprocessed."* Result (§5.1, Salacia): *"The rock in the core is
completely chemically processed by serpentinization, whereas the rock in ice-enriched mantle
is mostly unprocessed."*

**"It is a process" — confirmed.** Differentiation is the multiphase flow of eqs. (11)–(15)
(vapour flux J_v, liquid flux J_ℓ with permeabilities φ_v, φ_ℓ) integrated for 4.6 Gyr; the
final structure is read off the run.

**One sentence of C7 was too broad and is corrected in the row.** C7 wrote *"no mixing rule
for an ice-bearing layer exists, and no published bound on the error of using one."* The full
text carries one, for the state C7's refusal did not need to reach — **cold, unreacted grains
of ice and rock**: the two-layer model of Yasui & Arakawa 2009, adopted as eq. (1). §3.1.3:
*"The two layer model assumes that ice and silica are independently compressed with pressure,
following the compaction curve of each pure material, instead of the compaction curve of the
mixture … Despite the fact that the two-layer model ignores mutual interactions that probably
take place between ice grains and silica beads, it does a very good job of reproducing the
compaction curve of the mixture. The fact that it works rather well, means that at least on
some scale, ice and rock can be considered separately."* That is volume additivity between
two solids — the shape C10 approved for antigorite plus enstatite — with an empirical
justification and a stated caveat (the Leliwa-Kopystyński experiments showed *"the presence
of rock fragments strongly inhibited the compaction process"*, an interaction the two-layer
model ignores). No numerical error bound is printed in this paper; one would be in Yasui &
Arakawa 2009. C7's *conclusion* — the intermediate, partially differentiated state is not a
mixture — stands, because that state contains reacted rock and a front placed by transport.
The corrected sentence: a mixing rule exists for the never-wet grain mixture, and none for
the reacted, partially differentiated body.

## Question 2 — the middle rung

**How is the undifferentiated primordial crust treated?** As a grain mixture with the rock as
matrix and ice in its pores (Prialnik & Merk's conceptual model, Fig. 1(b)), compacted by the
two-layer EOS, **with reactions only where liquid water exists** (the quotation above). The
never-melted material is unprocessed rock plus crystalline ice, and at the surface amorphous
ice (6–25 km, Table 3).

A caveat the middle rung must carry: in this model the outer mantle is **not primordial in
composition**. It is "ice-enriched": water that melted in the core migrated outward and
refroze in the mantle's pores (§5.1: *"Ice, resulting from refreezing of water that has
migrated outward from the core, fills the pores of the rocky matrix"*), so the mantle's rock
fraction is below the initial 0.75 and the mantle is *"mostly"* — not entirely — unprocessed.
At the front there is a thin, nearly pure ice layer (Salacia, ~275 km from the centre, at
the ice grain density; Charon, ~10 km thick at ~500 km). A declared crust therefore needs a
declared rock fraction too, and the primordial value is an upper bound on it.

**Is there an EOS for the cold mixed layer, transcribable?** Yes — eqs. (1), (4)–(6) with
Γ = 1, which is exactly the never-melted case (T_max < T_m gives Γ = 0.9999 by the
text-consistent form): the crust EOS is then a function of the *local* (P, T, X_d) with no
history variable at all. Its limits are the pressure and ice-I limits above; at ψ = 0 it
reduces to plain volume additivity of the engine's ice ladder and silicate, which the
`Mixture` rule already computes for rock and metal.

**Does the model summarise the front as a single state variable?** **No.** The front is an
output of the time integration; the structural summaries the paper offers — Table 3's *"size
of ice enriched mantle"* 150/120/107 km for Salacia/Orcus/Charon, the correlation *"the
degree of differentiation, too, is determined by the object's mass"* *(abstract, and §6.1)* —
are read off the runs, and there is no input parameter for how far melting reached. The
paper names the declared-front practice and does not follow it: §3.1.1, *"Some theoretical
models overcome this difficulty by assuming that differentiation somehow occurred, without
actually computing how."*

So the load-bearing answer is: the literature (this paper) supplies the **crust EOS** the
middle rung needs and the **three-zone final shape** it would declare (Fig. 10: processed-rock
core / ice-enriched unprocessed-rock mantle / amorphous-ice skin), and it does **not** supply
the front. The front would be this recipe's declaration, of the same kind as
`serpentinisation` in C10 — declared, not fitted, and it drops the grade. The paper regards
that shortcut as a way of not computing the answer, which is fair; it is also the only way a
hydrostatic recipe can hold a partially differentiated body at all.

## Proposal — the C7 middle rung (grounds only; scope is the owner's)

**The item.** A declared differentiation front for icy bodies: `differentiation_front`
(a radius, or a fraction of the rock that reached the core) plus a crust rock fraction, giving
a static three-zone body — rock core (with C10's `serpentinisation` axis, because water
reached it), a water/ice mantle on the existing ladder, and a **cold ice–rock grain crust**
at additive volume, grounded by Malamud & Prialnik 2015 §3.1.3 / Yasui & Arakawa 2009,
with the paper's eqs. (4)–(6) as an optional porosity term (Γ = 1) carried as an upper bound.
C7's refusal of `differentiated: false` with ice stays; this is a different declaration with
its own path, not a lifting of the refusal.

**What it needs.**
- `Mixture` to accept the ice material as a component. Today it mixes rock and metal; ice
  brings the C3 dispatch (phase by local P, T) and the cold-component pass-through corner
  noted in F2 (`Mixture.grad_ad`). This is the real build cost.
- A third-zone in `solve`: the crust sits above the mantle, with its own material and a
  declared mass. A declared front becomes a mass partition — the same plumbing the
  three-layer band already exercises.
- Optionally eqs. (4)–(6) as a porosity factor on the crust, in SI, with the text-consistent
  Γ and the pressure/ice-I limits enforced by name.
- A test: the crust at ψ = 0 must reproduce the additive-volume density of its components;
  the porosity spot checks above (Durham 100 MPa; Leliwa-Kopystyński 80 and 764 MPa) as the
  transcription check.
- Anchors: none carries a crust, so all stay bit-identical; `ice_giant_anchor.json`
  re-freezes for the fingerprint if `solve` gains a path.

**Who consumes it.** Callisto and Titan first — C10 showed no serpentinisation fraction in
[0, 1] reaches their published C/MR² (0.3549, 0.3414 against band tops 0.3321, 0.3334), and
rock held in the crust raises C/MR² in the direction the layered bands cannot go; the front
is the axis that reaches. Not Enceladus (C9's consumer; small and hot). On the roster: any
icy body the owner chooses to declare partially differentiated.

**What it costs and what it does not promise.** The direction is right; whether a front in
[0, 1] *reaches* Callisto's 0.3549 is the same question C10 asked of serpentinisation, and it
is answered by running the sweep, not by this note. The declared front and crust fraction are
two declarations, so the grade is declared. Porosity in the crust pulls C/MR² the other way
(mass moves inward), so the crust's maximum C/MR² is the ψ = 0 case and the porosity term only
lowers it — which is why it is optional and a bound. The one open thread this must not touch
is F2's: Callisto and Titan at f = 0.75 ran past the sweep's budget in the 2.3–5 GPa,
500–1000 K liquid band, an EOS gap on the `water2` shelf, not a crust question.

## What this does to C9

The abstract-derived sentence in C9 is confirmed from the text, with the weights: heat from
serpentinisation is *"the second-most important heating mechanism"*, about an order of
magnitude below radioactivity over the whole run but *"about twice as high"* in the first
200–235 Myr; compaction's gravitational energy *"has little effect … about two orders of
magnitude less than serpentinization"* (§5.1). Tidal heating, impacts and convection are not
carried — satellites are excluded from the sample for exactly the first two (§2).

What the full text adds to C9 is a **second kind of heated-compaction relation**, distinct
from Neumann & Kruse's: a closed form in (P, T_max), eq. (5) with eq. (7), where the whole
thermal history is compressed into one number per shell — the maximum temperature reached.
That is a declaration this recipe can take today (T_max ≥ T, and using the present T gives
the *maximum* porosity, a bound consistent with the row's other bounds). It does not replace
Neumann (rheology, creep, time) or Bierson (general, validated over 123–2326 km); it is a
third relation with its own shelf — ≤ 0.8 GPa, ice I, no rock melt, a postulated step at
675 K. C9's "reached, no consumer" is therefore, for this relation, a **choice** about the
missing history rather than an absence: the history it needs is one declared number.

## What moved

Nothing numeric, no code. This file, its checklist, *revisited* lines on C7 and C9, a
pointer in the C7 and C9 notes, and the "abstract only" condition in the methodology docs (EN
and KO) rewritten to what was read. Gate: `scripts/check.sh` and `check_contracts.py` run
clean; no anchor was touched.
