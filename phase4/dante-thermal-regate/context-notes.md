# Context notes — Dante thermal re-gate, Chaos ice-stability grounding

## Where this came from

`phase4/_audit/consistency-audit-FINDINGS.md` left five owner-decision axes open.
Re-checking the board on 2026-08-03 found C4 (ring brightness), C6 (Chaos orbit vs
ring gap) and C8 (Chaos satellites narrative) already resolved on 07-28/07-29 — the
findings doc carries a `✓` per item but its summary was never updated, so the open
count read higher than it was. Only C5 and C9 were live.

## C5 — the owner's call, and why it costs less than expected

The 07-28 pass had resolved C5 by *admitting* the defect: ambient 673 K is above
sulfur's 388 K melting point, so the yellow sulfur plains were marked an
owner-override look with the instability spelled out in evidence. The owner's 08-03
call reverses the direction of the fix: keep the sulfur, lower the temperature.
Their reasoning is about which error a reader can catch — sulfur's melting point is
school chemistry, the tidal-heat partition needs the literature — so an error is
better hidden in the obscure layer.

It turns out no error is needed at all. What conservation pins is the *area-weighted*
`sigma T^4` mean (11,500 W/m2 tidal + 141 W/m2 absorbed starlight -> 673 K), which is
exactly what `tidal-heating-methodology.md` §7 refutation 1 says: you cannot buy a
cold surface with a hot interior. But that pins the mean, not the ambient. Letting
the heat escape through exposed melt at the 1350 K the row already cites:

    ambient 360 K (952 W/m2) over 94.3% + 1350 K melt over 5.7%  =  11,641 W/m2

The old row already assumed "1-5% hotspot coverage", so 5.7% is at the edge of its
own stated band rather than outside it. And this is Io's actual architecture, not a
departure from it: Io's ambient runs ~110 K while its heat leaves through paterae at
1300-1700 K. At 1200x Io's heating a larger exposed-melt fraction is the expected
consequence. So the partition is an art-directed choice inside a conserved budget,
which keeps the row `pass-in-window` instead of buying a divergence.

**Why 360 K and not 380 K.** Sulfur's melting point is 388 K, but orthorhombic
(bright yellow) sulfur transforms to monoclinic at 368.3 K. 360 K keeps the stable
phase the one whose colour the palette is built on, with 28 K of margin to melting.
The hotspot fraction is insensitive to this choice (5.6-5.8% across 340-388 K), so
the margin is free.

**Cascade.** The conductive lid follows the ambient flux, not the mean: with
k ~ 2 W/m/K, `d = k dT / q` goes from 0.12 m (677 K over 11,640 W/m2) to ~2.1 m
(990 K over 952 W/m2). The "hand's breadth of rock" line in the tidal-heating
narrative had to go with it. The Dante-vs-Hades ladder narrows further (360 K vs
278 K) and now rests on the exposed melt rather than on ambient temperature.

**What this buys back.** The albedo owner-override added on 07-28 is retired: solid
sulfur at 360 K is a stable phase, so albedo 0.30 (sulfur ~0.5 / basalt ~0.10) is
physically supported again and the appearance/gameplay rows no longer contradict
their own surface row.

## C9 — grounding, not relabelling

The sublimation-lifetime numbers on `Chaos/surface` and `Chaos/satellites` (albedo
0.875 survival threshold, 0.089 m/yr at albedo 0.70, 400 km stripped in 4.5 Myr)
come from the `docs/ice-stability.html` tool, while `refs` cited
`surface-color-albedo-methodology.md` (which has no sublimation treatment) plus three
papers lifted from inside the tool. That inverts the provenance rule: a reader cannot
tell a measurement from a recipe output. Fix is a real recipe doc, not a refs edit.
