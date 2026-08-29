# Porosity on a heated body — context notes

## The correction first

`interior-core.md` C9 predicted its own closure: "may close as 'the bound is the answer'".
The 2026-08-30 survey found a relation that carries three of Bierson's five exclusions, so
the prediction was wrong. It is corrected in the row, in words, not overwritten — the same
duty prose with a number carries, applied to a row with a guess.

## Provenance

Neumann & Kruse 2019, ApJ 882, 47 (2019ApJ...882...47N, doi 10.3847/1538-4357/ab2fcf) is
open access (ADS: OPENACCESS, PUB_OPENACCESS) with no preprint. It was not in the cache; the
publisher HTML was fetched through the ADS link gateway into
`docs/phase3/_papers/2019ApJ...882...47N.html` and a plain-text extraction placed beside it.
§2.5 ("Core Formation and Core Compaction by Creep") and Table 3 ("The Values of the Creep
Parameters Used … A1–A4: dry olivine; B1–B4: wet olivine; C1, C2: antigorite") were read
there. The three creep-law papers were checked on ADS by title: Mei & Kohlstedt 2000 parts 1
(diffusion) and 2 (dislocation), and Amiguet+ 2012 *Creep of phyllosilicates at the onset of
plate tectonics*.

What the text says, in its words: the core forms as "an agglomerate with pores that are
filled with water" behind a rising melting front; "compaction is a change of the density and
volume of a porous material that is being heated and applied pressure to. It is facilitated
by creep processes on a geologic timescale"; olivine compacts by Mei & Kohlstedt's law
covering "both 'dry' and 'wet' olivine", phyllosilicate-rich material by Amiguet's law "with
the Peierls stress". Abstract: core radius 185–205 km, porous core layer 4–70 km, ocean
≈10–27 km, ice crust ≈30–40 km; "No porosity is retained for an antigorite rheology, implying
that the core of Enceladus is not dominated by this mineral."

Table 3's coefficients were **not transcribed** into the engine. The extraction flattens the
table (units and columns interleave), and a branch that is not being wired does not need
numbers copied under those conditions; the row says where they are.

## Why "reached, no consumer" rather than wired

The relation is not a closed form in (P, T): it is a creep law — strain rate as a function of
stress, grain size, water, temperature — integrated over the body's thermal history, with
porosity as the time-evolving state. This recipe integrates hydrostatic equilibrium at one
instant and takes its temperatures by declaration. Wiring the branch means bringing a thermal
evolution the recipe does not have (the same gap the C7 closure named for partial
differentiation, and the same shelf: Malamud & Prialnik's evolution code). So the branch is
specified — which laws, which table, which body it was built on — and left for whoever brings
the history.

Consumers when it is wired: Enceladus (the paper's own body, on the icy roster, solved today with no
porosity declared), Europa, and the roster's tidally heated moons that declare
`tidal_heating`. Not the condensed anchors, whose `initial_porosity` is zero.

## The shape of the closure

Bierson's relation remains the general case because it is validated over 123–2326 km
diameter and Neumann is one 252 km body; a single-body evolution model cannot replace a
general bound. Neumann is the branch, analog. Two of the five exclusions (convection,
impacts) are carried by neither, and that is written rather than implied.

## The C10 discriminator, and its layer

Neumann's antigorite result is a rheology statement: a core made of antigorite does not
keep its pores, so *retained porosity argues against an antigorite-dominated core*. Vance+
2018's two routes to ~2700 kg/m³ (hydrous rock; anhydrous rock plus pores) are not
interchangeable once porosity is observed. Hilairet's antigorite ρ₀ is a density statement
and is untouched by this. C10 gets one declared axis (how serpentinised) and one
discriminator (whether pores survive); they must not be conflated into "antigorite is
refuted".

## What moved

Nothing numeric, no code. Two markdown files plus the cache. Gate cost: none.
