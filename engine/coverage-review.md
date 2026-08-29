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
- `rocky_roster.py:47` — `SYSTEMS = ("40_eridani", "barnards_star", "proxima_cen",
  "trappist_1")` hardcodes the implementation-candidate roster. The file already grades
  evidence (measured / estimated / mass-only); let the system list be data-driven from
  `db/systems` (or an external catalog) instead of a tuple.
- `interior.py:1085` and `interior.py:1122` — notes say "보드가" (the board). Pipeline
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
   `FLUID_CLASSES` (`interior.py:609`), so the Uranus/Neptune class — the most common
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
