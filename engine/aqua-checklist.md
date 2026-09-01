# AQUA for the cold dense corner — checklist (Brief 32)

Registered 2026-09-01, before the bake. Read first: `surveys-2026-08-31-context-notes.md`
§① — **AQUA does not raise any ceiling** (the 1 TPa wall was the cold ladder's; h2o_hot
reaches 407.5 TPa); the actual gains are ① the high-pressure 300–1000 K fluid corner
(no representation today: water2's per-isotherm ceiling tops out at 36.3 GPa, Mazevet
floors at 1000 K) and ② that corner is where our own ladder stops being data (C6:
extrapolated above ~355 GPa).

**Design choice, registered: option ① — fill the hole only.** AQUA slots in as the
LAST fallback exactly where `liquid_material` (in-column) and `_EnvelopeWater`
(envelope) currently refuse by name: fluid per our own melting/VII″ judgment, T below
water_hot.T_MIN, outside water1/water2. water1/water2/hot/steam dispatch order is
untouched. Replacing the ladder's extrapolated span (②) or all water (③) moves
published answers and is NOT this brief (a future brief must pre-register what is
expected to move).

**Canonical source**: Haldemann, Alibert, Mordasini & Benz 2020, **A&A 643, A105**
(2020A&A...643A.105H) — volume 643, not 638 (that pollution already happened once).
Grid: CDS `eos_pt.dat`, 328,993 rows = 1093 P × 301 T exactly (survey-verified),
cached gitignored at `docs/phase3/_papers/aqua/` with PROVENANCE.

**Bake** (`tools/make_aqua_table.py`, dev-only → `engine/aqua_table.py`): window
T ∈ [280, 1200] K × P ∈ [1, 1200] GPa **plus 2 stencil-margin nodes each side** (the
exact node bounds are recorded by the generator into the module — Brief 29's lesson:
an unbaked cell is its own sentence). Quantities: ρ and ∇_ad as published;
**c_p = T·(∂s/∂T)_P by central difference of the published entropy column** (the
same-table-slope rule, like hhe dlrho) computed on the full T-axis before windowing.
Plus a **fluid mask** (Phase ∈ {3 vapor, 4 liquid, 5 supercritical+superionic}):
evaluation refuses by name when the 4×4 stencil leaves the mask — AQUA's own phase
boundary is honored, no cross-phase smearing. Transcription gate: baked node values
byte-round-trip against the raw file rows.

**Labels carry AQUA's three survey-found defects**: phase labels are not source labels
(the 1 TPa·300 K row is labeled ice-X but its numbers are Mazevet); the grid runs
below its claimed 150 K floor (starts 100 K); region 7's upper half is unmarked
extrapolation. And the cost line: AQUA's Method-2 interpolation seam at 300–700 GPa
sits inside our ladder's span — irrelevant to option ① but part of the label.

**Physicality criteria, fixed before the sweep** (the water2 rule): within the baked
fluid mask — ρ finite, > 0, monotone non-decreasing in P along each isotherm's
contiguous fluid runs; 500 < c_p < 30,000 J/kg/K; 0 < ∇_ad < 1; seams measured and
recorded, not asserted: vs water1 (2.0–2.3 GPa × 400–500 K), vs water2 (along its
executed ceiling where both stand), vs h2o_hot (1000–1100 K overlap). The executed
effective ceiling/floor goes next to the printed claim.

**Identity & regression**: anchors bit-identical (trial paths change where refusals
become values, so this is MEASURED, not assumed — full anchor re-solve, not just
--fast); **base auto-check** (Brief 31's suite, unrepaired mode) must reproduce every
published base; --refresh only if values move, same commit with reason — but per
branch ② any value movement is unexpected and stops the brief first.

**Branches**: ① hole filled, existing answers bit-identical → success. ② filled but
answers move → UNEXPECTED: trace the cause and stop. ③ AQUA's executed ceiling
narrower than claimed → remaining hole in coordinates. ④ the grid fails physicality in
the corner → legitimate ending, water2's shape. ⑤ outside → name it.

**Hard constraints**: no new runtime dependency (baked module); gate background +
log-tail watch; the raw 51 MB/13.6 MB grid never enters git.

**Verdict (2026-09-01)**: branches ③+④ — the baked AQUA subset has **zero cells that
the existing tables do not already own**: the target corner = (already-served
territory) ∪ (AQUA's own region-5/6/7 inconsistency seam, 52 cells excluded by the
registered sweep at 15.9–26.9 GPa × 759–933 K, the paper's own §2.5 sentence). No
consumer → no landing: dispatch insertions reverted, baked module not committed;
generator + cached grid + PROVENANCE kept. Details: aqua-context-notes.md.
