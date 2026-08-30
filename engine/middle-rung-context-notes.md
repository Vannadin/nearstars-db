# The middle rung (C11) — context notes

**Parked 2026-08-30, before the first commit, by the owner's decision: the liquid-water gap
(water2) is closed first, because putting ice into a mixture walks trial paths into that
gap.** C11 stays in the queue. What was built before parking is kept on the branch
`c11-wip-parked` (the stash commit's hash, e42ab852; the stash entry itself was dropped afterwards because the
stash stack is shared by the repository's three worktrees), so nothing is lost and nothing
uncommitted lingers in the worktree. Next time: a WIP commit on a branch, not a stash.

## Where it got to

Design, executed in `interior.py` and `porosity.py` on the parked branch:

- three declarations — `differentiation_front` (cumulative mass fraction from the centre
  that melted and differentiated; 1.0 = no crust), `crust_rock_fraction` (rock mass fraction
  inside the never-melted crust, the second declaration F3 insisted on), `crust_porosity`
  (optional, Malamud & Prialnik 2015 eqs. (4)–(6) with Γ = 1 on the crust) — threaded through
  `_stack` → `integrate` → `_shoot_pressure` → `shoot` → `solve` → `infer_three_layer`;
- `_stack` gains a fourth layer: core → rock (total rock minus the crust's) → ice (imf minus
  the crust's) → crust (`crust_primordial`: ice ladder + silicate as grains by additive
  volume) → gas; `solve` refuses inconsistent partitions with the numbers;
- the never-melted declaration is enforced: a crust step whose (P, T) is above the melting
  curve raises a `PhaseGap` naming C11 (a self-contradictory declaration, not a temperature
  bracket problem);
- `PorousCrust(Mixture)` applies the two-layer porosity to the crust's density only;
  Malamud's constants live in `porosity.py` with the eq. (7) note;
- smoke test on a 0.025 M⊕ icy body (core 0.1, ice 0.5): front 1.0 reproduces the default
  bit for bit; at 270 K a crust is refused (liquid); at 200 K, front 0.8 with crust rock 0.4
  gives C/MR² 0.3236 against 0.3020 without a crust (radius −1.1 %); with porosity 0.3181
  (direction as pre-registered: crust rock raises C/MR², porosity lowers it).

Not done: tests, `--refresh`, docs, chain.yaml, the Callisto/Titan sweep, the C11 row.

## What the sweep will need (noted while parking)

The moons' roster temperature is 270 K, at which any crust thicker than the surface skin is
above ice Ih/III/V's melting curve (251–273 K between 0.02 and 0.6 GPa), so the crust
declaration is self-contradictory there. The sweep needs a colder declared potential
temperature (e.g. 200–240 K), stated as part of the grid, with the no-crust reference re-run
at the same temperature. That is a consistency requirement of the declaration, not a knob.
