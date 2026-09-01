# AQUA for the cold dense corner — context notes (Brief 32)

2026-09-01. Registration: `aqua-checklist.md`. Verdict: **branches ③+④ combined — at
option ①'s insertion points AQUA has zero reachable cells, so nothing landed in the
engine.** The generator, the cached grid, and this record are the products.

## §1 What was built and measured

The full pipeline ran: CDS grid cached with PROVENANCE (`docs/phase3/_papers/aqua/`,
328,993 rows verified); `tools/make_aqua_table.py` baked a windowed subset
(281.8–1174.9 K × 1.0–1183.5 GPa usable, stencil margins recorded; ρ/∇_ad as
published; c_p from the entropy column with **phase-aware differencing** — the first
run's 30,000+ J/kg/K spikes were my central difference eating the latent-heat jump
across AQUA's melt line, not AQUA); the registered physicality sweep then found **52
fluid cells with negative or sub-500 c_p at 15.9–26.9 GPa × 759–933 K** — the seam the
paper itself disclaims (*"The main inconsistencies are located between regions 5, 6
and 7"*, §2.5) — excluded per the water2 rule (1.25 % of fluid cells, coordinates in
the module header). Seams, measured: ρ vs water1 (2.0–2.3 GPa × 400–490 K) worst
0.13 %; vs water2 along its executed ceiling **0.00 %** (AQUA's region there IS
water2's source); vs Mazevet at 1000–1100 K worst 3.38 %.

## §2 The verdict — zero reachable cells

An exhaustive pass over the baked grid asked, cell by cell: fluid per AQUA's mask,
below 1000 K, and NOT already owned by steam/water1/water2? **Zero cells qualify.**
The corner option ① adopted AQUA for decomposes exactly into (a) territory the
existing four tables already serve — the survey's "six of AQUA's seven regions are
sources we already carry", now confirmed at cell grain — and (b) AQUA's own excluded
inconsistency seam, which is precisely where our recipe's refusals live
(the old named refusal at ~16–27 GPa × 760–930 K stays, and AQUA cannot take it:
its numbers there are the unphysical ones). A dispatch fallback with no reachable
state is a machine without a consumer (C5), so **the adapter and both dispatch
insertions were reverted, and the baked module was not committed** — the generator
rebakes it in under a minute when a real consumer appears (e.g. option ② replacing
the ladder's extrapolated span, which is a separate brief that must pre-register what
it expects to move).

## §3 What stays true

AQUA remains the right source for a future option ② (the ladder above ~355 GPa is
extrapolation — C6), and the generator carries the lessons forward: the transcription
round-trip gate, phase-aware entropy differencing, the fluid-stencil mask, and the
seam exclusion with the paper's own sentence attached. Nothing in the engine changed;
anchors untouched by construction (working tree clean of engine code).
