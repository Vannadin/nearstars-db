# Queyroux at the seam (F4) — context notes

The last follow-up on C3's seam. **Parked at the gate, 2026-08-30**: the individual values
the Letter prints inside the disputed band are not melting measurements, and F1's criterion
does not let a fit reopen anything. What was read, why it does not serve, and what would, are
below. The criterion is written before any number, as F1's was.

## Provenance

Queyroux, J.-A., Hernandez, J.-A., Weck, G., Ninet, S., Plisson, T., Klotz, S., Garbarino, G.,
Guignot, N., Mezouar, M., Hanfland, M., Itié, J.-P. & Datchi, F. 2020, *Melting Curve and
Isostructural Solid Transition in Superionic Ice*, Phys. Rev. Lett. 125, 195501
([`2020PhRvL.125s5501Q`](https://ui.adsabs.harvard.edu/abs/2020PhRvL.125s5501Q), doi
[10.1103/PhysRevLett.125.195501](https://doi.org/10.1103/PhysRevLett.125.195501)). Cached
as `docs/phase3/_papers/2020PhRvL.125s5501Q.pdf` — the six-page Letter; **the Supplemental
Material (Tables S1–S2, Figs. S1–S5) is not held.** First page and title checked against the
bibcode. Its seat: inside the band 16.5–20.6 GPa it is the only melting measurement (Kimura &
Murakami 2023 measure from 25.9 GPa, and their rows below 21.3 GPa take their temperature
*from Queyroux's curve*), so it is the arbiter's seat, not a second source; and it is
independent of Kimura 2023, which it precedes and does not cite (its ref. [25] is Kimura,
Kuwayama & Yagi 2014, JCP 140). Kimura's asterisked rows must not be counted as confirming
Queyroux — that would be the same curve twice.

## The criterion, fixed before comparing (F1's three clauses, reused)

1. Where Queyroux **measures**, "sits with" means the residual is inside the **printed
   uncertainty** — Queyroux prints its own: triple point 14.6(5) GPa · 850(20) K; the band
   value quoted in the brief, 18.4(9) GPa. Verdict per point, inside / outside.
2. Where there is no measurement, a **fit** (Table I's Simon–Glatzel) may be evaluated but
   **cannot trigger a reopening**.
3. It ends in a table of residuals per pressure point, not in an adjective.

Pre-registered outcomes: with Reinhardt / with IAPWS / between / **the source does not reach
the deciding region** — the fourth firing here if the printed points are not melting
measurements. Carried beside any number: Queyroux's melting temperatures run *"systematically
100–150 K lower"* than the laser-heated family (their §Melting curve, Refs. [19,20]) — a
disagreement between experimental families, not ours to adjudicate; and the upper-branch
Simon–Glatzel coefficients are loose, a = 3.44(216), b = 4.33(200) (Table I, 90 % confidence
on the last digits) against 1.555(14), 2.557(14) below the triple point.

## The gate — what the printed numbers are

Read at their place in the text, §*Isostructural transition*, p. 195501-3, right column:

> "XRD patterns of ice were collected in a RH run along two isotherms at 905 and 944 K, from
> the melting pressures up to 39 and 33 GPa, respectively. At all P–T conditions, the pattern
> is consistent with the Pn-3m structure of ice VII but, as seen in Fig. 3(a), a discontinuous
> shift of the lattice parameter a of about −0.7(1)% — corresponding to a volume shift of
> −2.2(1)% — is observed on both isotherms, at 15.6(2) GPa at 905 K, and 18.4(9) GPa at 944 K
> (see also Fig. S2 of the SM)."

So **18.4(9) GPa at 944 K is the ice VII″ → VII′ isostructural solid–solid transition on the
944 K isotherm, and 15.6(2) GPa at 905 K is the same transition on the 905 K isotherm.
Neither is a melting point.** Fig. S2, which the sentence cites, is the lattice-parameter
evidence for that transition (not held; the caption is not in the Letter). The audit's
"14.6 GPa · 905 K" pairs two different things: the triple point is **14.6(5) GPa · 850(20) K**
(abstract; §Melting curve, *"a triple point at 14.6(5) GPa and 850(20) K"*; Table I), and
905 K is the temperature of the first isotherm — the Letter mentions *"our experimental
melting point at 905 K"* (§AIMD comparison) **without printing its pressure**. Fig. 1's
legend keeps the two data sets apart: *"Red squares and blue circles: experimental data for
the melting line and the isostructural solid transition, respectively."* The individual
melting points are in Table S1 (*"see also Table S1 of the SM"*, §Melting curve), and the
Letter's own definition of a melting pressure is *"the midpoint of the pressure interval
where melting was observed"* along an isotherm.

**Verdict at the gate: the fourth branch fires.** No melting point with a printed
uncertainty inside 16.5–20.6 GPa is available from the Letter, and Table I's fit cannot
reopen C3 (clause 2). The item is parked.

## What the Letter does give in the band — a bound, recorded as a bound

Two printed observations at 944 K bracket the melting pressure on that isotherm, and one of
them lies in the band:

- Fig. 2(a)'s caption: an XRD image *"above the melting temperature … at 15.4 GPa–944 K in a
  RH run"* — **liquid at 15.4 GPa, 944 K**.
- The transition sentence above: **solid (ice VII″) at 18.4(9) GPa, 944 K**.

So 15.4 GPa < P_m(944 K) < 18.4(9) GPa, i.e. **T_m(18.4 GPa) > 944 K**: whatever the melting
curve is, ice is still solid at 944 K there. Set against the two curves at 18.4 GPa (this
recipe's own values: IAPWS eq. (5) for ice VII, `water_t_melt`; Reinhardt+ 2022's liquid line
interpolated linearly between its 15 and 20 GPa data points, `ice_melt_table.LIQUID_LINE`):

| at 18.4 GPa | T_m (K) | observation: solid at 944 K | reading |
|---|---|---|---|
| IAPWS eq. (5), ice VII branch | 690 | 944 − 690 = **+254 K** solid above the curve | excluded there |
| Reinhardt+ 2022 liquid line | 801 | **+143 K** solid above the curve | also too cold there |
| Queyroux Table I upper branch (a fit, clause 2) | 1009 | consistent | orientation only |

**This is a bound, not a point**, and the criterion's clause 1 has nothing to put a residual
inside of — which is why it parks the item rather than deciding it. What it says without a
verdict: **both curves are too cold at 18.4 GPa, IAPWS by more than a quarter of a thousand
kelvin, Reinhardt by 143 K** — the same direction and about the size of Kimura's one
out-of-band point (+171 K above Reinhardt at 25.9 GPa, F1). It cannot make Queyroux "sit
with" either; it does say the seam's step is in the right direction and may not be large
enough. The audit's orientation figure (Reinhardt ≈ 801 K at 18.4 GPa, +143 K) is verified
here from the baked line; it is arithmetic on a solid-transition pressure, and its meaning is
only the bound above.

## Grade

Unchanged; F1 could not raise it because Kimura's own error (8–11 %) exceeded the 5 % scale,
and Queyroux's per-point errors are in Table S1, which is not held. The triple point's
±20 K on 850 K is 2.4 % — under the bar — so if Table S1 carries that quality inside the
band, the grade question can be answered when it arrives.

## What would run this item

Table S1 of the Supplemental Material (free from APS,
`link.aps.org/supplemental/10.1103/PhysRevLett.125.195501`) — the individual melting points
with uncertainties, of which at least the 905 K and 944 K isotherms' melting pressures lie in
or beside the band. With it, clause 1 applies inside the band and the four branches decide C3.
The owner has been asked for it. Until then: nothing moves, no code, no anchor.
