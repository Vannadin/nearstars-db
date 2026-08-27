# Shooting bracket — checklist

`_shoot_pressure` brackets the central pressure by multiplying a trial value by four until
the enclosed mass reaches the target. When one of those **trial** pressures pushes an outer
layer past its equation of state's ceiling, the resulting `PhaseGap` leaves the solver as a
refusal — as though the body could not be solved, when only the trial could not be
integrated.

## Why now

It has surfaced twice and been read as physics both times.

- **2026-08-26.** Earth-like rock was reported to stop at 6.84 M⊕. The converged solution
  there has a central pressure of 2741 GPa against the silicate fit's 3500, so the ceiling
  was never reached. Recorded in the deep-silicate commit, but the cause was left alone.
- **2026-08-27.** The `water` preset was reported to solve to 5.884 M⊕. Instrumenting
  `solve` shows the bracket already reaching the answer at 1565 GPa with an ice column base
  of 240.6 GPa, then stepping once more to 6260 GPa where the ice breaks at 3479 GPa. Hand
  shooting 8.0 M⊕ converges to a relative mass error of 1.8e-16 with the ice base at
  331.7 GPa, a third of its 1000 GPa ceiling, and solutions exist past 20 M⊕.

The second one understates a real gain by roughly a factor of four, and
`test_interior.py` pins it: a refusal test asserts that 8.0 M⊕ of `water` declines.

## The rule this restores

A refusal must describe the **converged** state, never a trial. The engine already holds
that rule elsewhere — "out of domain is a returned value", graded and reasoned from the
branch that decided it. A bracketing artifact wearing a refusal's clothes breaks it
silently, because the reason it prints is well-formed and cites a real ceiling.

## Tasks

- [x] Outer-layer `PhaseGap` during bracketing narrows the bracket instead of escaping.
      → verify: `water` at 8.0 M⊕ solves, and its ice column base is under 1 TPa.
- [x] A genuine refusal is still reachable and still names the outer layer.
      → verify: some mass exists where narrowing cannot bracket, and its message names the
      layer and pressure of the **narrowed** state rather than a discarded trial.
- [x] The anchors do not move.
      → verify: five rocky anchors, six roster moons, five icy satellites, Jupiter and
      Saturn all bit-identical.
- [x] The refusal test stops pinning the artifact.
      → verify: `test_interior.py` exercises the ice ceiling at a mass that actually
      reaches it, or by another route.
- [x] A regression test for the mechanism itself, not the symptom.
      → verify: a case whose trial pressures cross an outer ceiling while the answer does
      not, asserted to solve. Without it this returns a third time.
- [x] Measure and report the ceilings that move.
      → verify: `water` and any other composition whose limit was an artifact.

## Out of scope

- The refinement loop after bracketing. It stays inside `[lo, hi]`, so it cannot reach a
  pressure the bracket has already excluded.
- The inner material's ceiling. `p_ceiling` is the innermost material's `p_max` and that
  check is correct: the centre genuinely sits in that material, so exceeding it is a real
  refusal. This is only about layers above the centre.
- Re-measuring the giant or silicate ceilings beyond noting whether they move.

## What it found

- **The real gain was 3.7x what was reported.** The `water` preset's limit is 21.49 M⊕,
  not 5.884. The ice ladder work that landed it was sound; only the number describing its
  reach was a discarded trial pressure.
- **The three existing ceilings did not move by a digit** — `earth_like` 22.78, pure
  silicate 53.38, pure iron 24.92. Each is set by the innermost material, whose ceiling the
  bracket checks correctly because the centre genuinely sits in it. That contrast is the
  evidence for where the defect was, so `water` now sits beside them in the table.
- **A genuine refusal still exists and moved to where it belongs.** Past 21.49 M⊕ the
  converged ice column really does pass 1 TPa, and the message now names the outer layer
  and the narrowed state's pressure instead of the inner material's ceiling.
- **Cost.** Narrowing runs only on the path that used to escape, and stops as soon as it
  brackets — three or four integrations for a body that solves. The measured ceiling for
  `water` costs 19.5 s against ~4 s for the others, because its bisection crosses the
  narrowing path 28 times; that is the price of measuring rather than typing the number.
