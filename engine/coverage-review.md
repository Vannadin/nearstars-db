# Interior solver — external review, remaining coverage (2026-08-27)

Written by a review session at the owner's request, for the directing session to pick up.
Reviewed as of commit `35771c83` (core_state opened); all eight engine test files were run
and passed at commit `1bd0a1c4`, before the temperature/melting/core_state commits landed —
those three are reviewed by reading, not re-run.

## Verdict

The core is sound as a **general-purpose** solver: the physics core (`interior.py`,
`eos.py`) has no NearStars dependency, validation anchors are published solar-system
measurements, refusal discipline and the grade rule ("what does the answer lean on") are
strengths worth keeping exactly as they are. What remains is (a) two owner-flagged
discipline problems, and (b) a coverage map with two large holes and three smaller ones.

## Owner-flagged problem 1 — the test pool keeps collapsing to NearStars

The physics core is clean; the confinement lives in the survey/validation layer:

- `test_interior.py` `ROSTER` — six hand-typed NearStars moons. Fine as a *consumer*
  check, but it is not a generality test.
- `rocky_roster.py@«from interior import (EARTH_MASS_KG, EARTH_RADIUS_M,  # noqa: E402»` — `SYSTEMS = ("40_eridani", "barnards_star", "proxima_cen",
  "trappist_1")` hardcodes the implementation-candidate roster. The file already grades
  evidence (measured / estimated / mass-only); let the system list be data-driven from
  `db/systems` (or an external catalog) instead of a tuple.
- `interior.py@«break                        # 괄호가 잡혔다. 정밀도는 할선법의 일이다»` and `interior.py@«# 2026-08-31 — C13 끝 B 가 여기서 죽었다). 사다리의 1 TPa 는 French & Redmer 2015»` — notes say "보드가" (the board). Pipeline
  vocabulary inside general solver output. The declaration (`ice_allowed`) is general;
  only the sentence needs to say "the caller" instead of "the board".

Principle: the true generality pool is exoplanets with both mass and radius measured
(transit + RV). The NearStars roster should be one client of the solver, not the
definition of its test pool.

## Owner-flagged problem 2 — the methodology doc is becoming a dev note

`docs/reference/interior-structure-methodology.md` was 1383 lines at review, 1451 after
the melting/thermal commits — it is still growing, and the temperature checklist's own
"doc did not grow" item is failing. Split rule the owner endorsed:

> Keep only the sentences another project would need to use this solver.

- **Stays (methodology):** The relation, Porosity, Giants, Practical recipe, Validation,
  Domain of validity, Citations.
- **Moves to context-notes:** "What changed, and why each change had to" and all
  change-narrative added since.
- **Moves to project docs (phase3):** "What the roster asks for", "What the giant branch
  opens: Alpha Centauri A b", "Worked example: Pandora" (replace with an anonymous
  ~1 M⊕ water-world example if a worked example is wanted).

## Coverage map

### Closed since the review started

- Temperature: the integration carries T, `core_temperature` / `cmb_temperature` reach the
  output, `core_state` is wired (`a371e8c0`, `35771c83`).
- Melting curve: materials can answer "is this P·T solid" (`194701f7`) — the prerequisite
  for liquid layers.

### Large holes (both still open — these decide "any planet")

1. **Ice X / superionic EOS above 37.4 GPa.** Large water worlds (the common 2–3 R⊕
   ocean-world class) are refused entirely. The refusal already names French+ 2009;
   Salpeter & Zapolsky 1967 (TFD) is the same expansion family and is on the owner's
   paper-request list.
2. **Ice-giant envelope (water–ammonia–methane mixture).** `ice_giant` still sits in
   `FLUID_CLASSES` (`interior.py@«# **온도가 막은 것으로, 위로 던진다** — 더 뜨거우면 water2 의 천장이 오르고 1000 K 부터는»`), so the Uranus/Neptune class — the most common
   planet class — is refused. Needs a Redmer+ 2011-family EOS; the existing
   Mixture/polytrope infrastructure is the right substrate.

### Smaller holes

3. **Liquid-water ocean layer.** The melting curve *detects* molten ice but the solver
   cannot *integrate* a liquid layer. Europa-type three-layer structures (rock + ocean +
   ice shell) and their moment of inertia are inexpressible.
4. **Thermal branch validated only to 1.05 R⊕** (`UNTERBORN_TCMB_MAX_R`). Above that,
   honest analog demotion — but the checked window is narrow.
5. **Inversion is single-axis.** `infer_composition` solves one free fraction; three-layer
   inversion is out of reach by construction (couples to hole 3).

Not counted as holes (design boundaries, correctly refused by name): sub-Neptune (solves
if gas mass fraction is declared; the evolution model is deliberately not this recipe's
job), brown dwarfs, stars.

### Suggested order

Ice-giant envelope > ice X > ocean layer, by how much of the planet population each
unlocks. The roster/doc problems are discipline, not code — batch them into the next doc
cleanup pass.

### ⚠ The five holes above are closed — read them as of 2026-08-27, not as work

Added 2026-09-01. Holes 1–3 and 5 closed through the C1–C3 arc and `infer_three_layer`;
the whole C1–C13 core list is closed (`interior-core.md`). **Do not pick work from the list
above** — a stale list of open items is the same defect the handoff's parked-decisions
section had, where five already-closed questions sat waiting to be re-asked. This file is
kept as the 2026-08-27 review it says it is.

## Queued deliverable — the per-property coverage graph

**Owner's request, 2026-09-01: after the tool is finished, draw where each material property
is covered, from what to what.** Queued deliberately, not started: the standing rule is the
tool first, because the chain will be re-run once it is all tooled and a hand-made figure
would be redrawn. What follows is the design, recorded now because **every constraint in it
was earned today and will not be obvious later.**

**Splitting it early was proposed and declined by the owner the same day — do not re-propose
it.** The idea was to hand the *claimed-range* half (reading `eos.py`'s constants against each
source's printed range) to the parallel session immediately, since printed ranges do not change
when the tool does, so that half would not be redone. The owner chose to keep the whole item
until the tool is finished. Two hazards it would have run into anyway, worth keeping on record:
the parallel session shares this worktree and does not write to the repository, and `eos.py` was
under active edit at the time — **a sweep run against a half-edited `eos.py` returns numbers
that are quietly wrong**, which is the worst failure shape for a coverage measurement.

**The naive version of this graph is actively harmful.** A plot of each material's *printed*
range is a false-label machine at scale — it would draw exactly the claims that this week
disproved one at a time, with the authority of a figure. So:

1. **Three coverages per band, not one.** *Claimed* (the printed range), *executed* (where
   the material actually returns physical values), *data-supported* (where the source has
   data rather than a smooth continuation). They differ, sometimes by a factor of three:
   `ice_x` claims 1 000 GPa, is data-supported to ≈355 GPa, and the potential it is fitted to
   closes the ice region near ≈520 GPa. `water2` carries knots to 100 GPa and returns
   **negative density inside its own knot box** — executed ceiling 2.3 GPa at 360 K rising to
   30 GPa at 1000 K. AQUA claims a 150 K floor and its grid starts at 100 K.
2. **Per property, not per material.** In one table the three quantities have different
   coverage: `h_he`'s density is fine where its `grad_ad` is clamped (70 clamped cells above
   the reach line, Brief 29). So the row is (material × property), and a property whose
   values were clamped rather than computed is a different colour, not a footnote.
3. **A mixture's band is not a combination of its parts.** `eos.py@«# #   * 이성분 — "deviati»` takes
   `min(p_max for parts with w > 0)` — **weight-blind by design**, so the ceiling is the
   lowest component's whatever its weight. Brief 28 measured a veto from a component at
   weight 6.87 × 10⁻⁶, whose actual contribution sits 25–30× below the anchors' own jitter
   (crossing computed at w ≈ 1.7 × 10⁻⁴). Draw the mixture's real, narrower band and make
   the vetoing component nameable.
4. **The gaps are the product, not the leftovers.** The most consequential band all week was
   a *hole*: the 12–20.6 GPa gap between the melting curve and the ceiling, and the wall at
   p ≲ 0.1 GPa × 500–1000 K where **1 102 of 1 202** ice-axis refusals died. Gaps get drawn,
   labelled and counted, never left as whitespace — findability is the deliverable.
5. **Overlay where bodies actually go, trial paths included.** Uranus's mantle spans
   34.5–819.8 GPa · 2663–5948 K, Neptune's 39.2–1015.6 GPa · 2553–6066 K, and every moon
   phase call lands below 8.4 GPa. That overlay is what answers C5's and C6's standing
   question — does anything reach this? — and **converged columns are not enough**: cold
   trials walk the solid ladder far deeper than the answer does (Brief 34 item A, and the
   flip experiment's Neptune).
6. **Figure-read bounds carry their reading, and disagreements are drawn as disagreements.**
   The superionic boundary exists only as lines in two papers' figures; its crossing was read
   as 358 ± 15 and 329 ± 25 GPa and **was not adjudicated**. Such a bound is drawn with its
   uncertainty and marked a figure read — never as a transcribed curve. No digitizing for
   values.
7. **Generated from the code and from executed sweeps, never hand-drawn.** The executed band
   must come from *running* the material, not from reading its printed constant — otherwise
   the graph inherits the defect it exists to expose, and it will go stale like every
   hand-written number in this file did. `build_graph_page.py` is the precedent for
   generating a page from a declaration.

## Paper access ledger (for the SeaFreeze cross-check and future EOS work)

- **Owner request stands (paywalled, school account likely unlocks — AIP ×3, Springer ×1):**
  Choukroun & Grasset 2007 & 2010, Gagnon+ 1990, Dunaeva+ 2010 — the independent
  experimental check on the SeaFreeze-derived ice III/V/VI constants.
- **Open access but bot-challenged from here (owner can fetch in a browser):**
  Journaux+ 2020 (SeaFreeze paper itself), Durham+ 2005 (upgrade from abstract-only),
  Ni 2018 (provenance of the circulating 0.2756 Jupiter NMoI).
- **Nice-to-have paywalled (verification route already exists via Seager/IAPWS):**
  Anderson & Goto 1989, PREM 1981, Salpeter & Zapolsky 1967, Feistel & Wagner 2006,
  Britt+ 2002.

Delivered PDFs go to `docs/phase3/_papers/` under their bibcode; the citations section's
"non-ADS-fulltext exception" entries then get upgraded in place.
