# Partial differentiation — context notes

C7 closes without new physics; the deliverable is the refusal's reason and the fence around
C10.

## What was searched, and what came back

Additive-volume, ideal and linear mixing applied to rock + ice, and interior models of
undifferentiated icy bodies (2026-08-30). What surfaces under "additive volume + silicate +
water" is silicate-melt and mineral–fluid geochemistry, a different problem. No mixing rule
for an ice-bearing layer, no bound on the error of one.

The three papers that do treat the arrangement are all Icarus / Elsevier with no preprint;
ADS shows no open-access flag on any. **Only the abstracts were read.** From the abstracts:

| paper | what the abstract says it does |
|---|---|
| Malamud & Prialnik 2015 (2015Icar..246...21M) | initial homogeneous ice–rock; multiphase flow of water through porous rock; consequent differentiation and aqueous alteration; heat from long-lived radionuclides, serpentinisation, compaction's gravitational energy, amorphous-ice crystallisation; density from hydrostatic equilibrium through changing composition, P and T |
| Malamud & Prialnik 2013 (2013Icar..225..763M) | serpentinisation as an exothermic reaction; runaway possible; Enceladus and Mimas |
| Prialnik & Merk 2008 (2008Icar..197..211P) | the 1-D adaptive-grid thermal-evolution code for porous icy bodies both stand on |

So the closure can say *a treatment exists and it is thermal evolution with reaction and
transport*; it cannot say whether anything in it is transcribable into a hydrostatic
solver. That limit is written into the row, not softened.

## Why the reason had to be raised

"The mixture rule handles rock and metal only" describes the code and sends the next reader
after a rule that does not exist. The raised reason names the two facts that make the rule
impossible: water in silicate is a **reaction** (hydrated minerals with their own density
and heat — which is also why C10 could find no closed-form hydrated-rock EOS), and the
intermediate state is a **process** (how far the water got), which the literature carries as
a stage of thermal evolution rather than a composition. The refusal string in `solve` now
says this and points at the row.

## The C10 fence

C7's conclusion is about mixing water *into* silicate. C10 will mix antigorite with
enstatite/PREM — two solids coexisting as grains, each with a measured equation of state,
which is what a partially serpentinised rock is. Volume additivity between two solids is the
standard treatment and is the very rule this recipe already uses for rock and metal. C10's
one declared axis is *how serpentinised*; nothing in C7 forbids it. Written into the row so
the next session does not apply C7 where it does not belong.

## What moved

Nothing numeric. The refusal string lives in `solve`, a path-fingerprint function, so the
ice-giant anchor was re-frozen: fingerprint only, values bit-identical.
