# R6 research prompt — grounding the gravity significance floor (run in NearStars, ADS)

Copy everything below the line into a NearStars session (it has the ADS API token and the
`scripts/phase3/build_bibliography.py` pattern for `https://api.adsabs.harvard.edu/v1/search/query`).
The output report comes back to the Principia session, which will fix the parameters.

---

## Task

You are grounding two numerical parameters of a gravity truncation scheme in the
literature. Produce `plans/principia-interstellar-branch/research/R6-significance-floor.md`
— a self-contained report with numbers, bibcodes, and short verbatim quotes. Another
session will set the parameters from your report alone, so include the evidence, not just
conclusions.

## Context (what was built; do not re-derive)

A Principia (KSP n-body mod) fork adds **per-pair far-field damping** of Newtonian
gravity, to (a) make vessels in the void between star systems exactly force-free and
(b) stop wasting computation on physically meaningless pairs (e.g. hundreds of
RSS-Origin asteroids all perturbing each other and a 40-ly-distant system).

Mechanism: each body gets a cutoff radius **r_c = √(μ/a_floor)** — the distance where its
point-mass acceleration falls to the floor `a_floor`. The potential (not the force) is
multiplied by a C² quintic sigmoid σ: untouched below r_c/3, smoothly ramped on
[r_c/3, r_c], **exactly zero** beyond r_c. For massive-massive pairs one σ is applied
symmetrically to both members (Newton's third law, momentum exact), with the pair cutoff
at max(r_c_a, r_c_b) — so an asteroid never stops feeling its star (the star's r_c
dominates), and asteroid↔asteroid or star↔star-across-lightyears pairs vanish.
Consequence worth noting: asteroid↔planet pairs survive (planet r_c ~ 133 AU), so the
belt's collective effect on planets is retained; only asteroid↔asteroid dies.

Provisionally `a_floor = 1e-12 m/s²` (solar-mass r_c ≈ 1.2 ly) and shell ratio
outer/inner = 3 (upstream HarmonicDamping convention). Both are so far **arbitrary** —
the owner wants them justified or replaced by literature-grounded values.

Use profile to weigh against: gameplay timescales up to ~centuries of timewarp; player
measurables are relative in-simulation quantities (orbits, encounters, maneuver
planning), not absolute coordinates; worst identified drift is ~500 m/yr (coherent
worst case at the cutoff boundary); rosters: RSS-Origin (hundreds of asteroid
celestials) and NearStars (multi-star; closest bound pair ~0.2 ly — VERIFY the actual
minimum from `db/binary_orbits.json` and report it).

## Research angles

### A. Planetary-ephemeris perturber selection (the strongest precedent)
How do DE, INPOP, EPM decide which asteroids to include as perturbers, and what do they
do with the rest?
- JPL DE430/431: Folkner et al. 2014 (IPN Progress Report 42-196); DE440/441: Park,
  Folkner, Williams & Boggs 2021 (AJ 161, 105). Asteroid perturber count (343?), the
  selection criterion (effect on Earth–Mars range over the data span? mass threshold?),
  and the stated magnitude of what is neglected.
- INPOP (Fienga et al., INPOP19a/21a papers): individual asteroid count + the
  **asteroid ring** used to aggregate the sub-threshold remainder — extract the ring's
  total mass and the argument for aggregating vs dropping.
- EPM (Pitjeva & Pitjev): count (~301?) + ring.
- Deliverable: the quantitative selection thresholds (in position-effect metres and/or
  acceleration), and whether "drop" vs "aggregate" matters at our fidelity.

### B. Detectability bound — the smallest coherent acceleration anyone has measured
Bounds what any observer (a fortiori a game) could notice.
- Yarkovsky-effect detections on NEAs: typical measured da/dt ↔ accelerations
  ~1e-15–1e-13 m/s², detected only via radar ranging over ≥ a decade (Chesley et al.
  2003, Golevka; Vokrouhlický et al.; Farnocchia et al. 2013 catalog). Extract:
  acceleration magnitude vs timespan vs ranging precision needed.
- Pioneer anomaly (~8.7e-10 m/s²) as the classic "edge of spacecraft-tracking
  detectability over decades" datum (Anderson et al.; Turyshev et al. resolution).
- Deliverable: a table acceleration ↔ what instrument/timespan it took to see it.

### C. Stellar dynamics — where star–star gravity stops being meaningful physics
If the Galactic tide (which we do NOT model) dominates the mutual attraction beyond
some separation, cutting there is *more* physical than keeping the bare two-body term.
- Wide-binary disruption / Jacobi (tidal) radius for ~1 M☉ pairs (~1.7 pc?): Jiang &
  Tremaine 2010; Chanamé & Gould; El-Badry reviews; the observed widest bound binaries
  (~0.1–1 pc).
- Extract: the tidal acceleration scale vs separation (Oort constants), the separation
  where a_tide ≈ a_mutual for 1+1 M☉, and how our r_c(1 M☉) compares.

### D. N-body numerical practice — force-error tolerances and outer-truncation precedent
- Long-term planetary integration error budgets: what relative force/energy error is
  the community standard (Wisdom & Holman; Rein & Spiegel 2015 IAS15; Rein & Tamayo
  WHFast; Hairer-type backward-error arguments). How does an O(a_floor) static force
  bias compare to accepted integrator truncation?
- Collisional vs collisionless force-accuracy standards: tree-code opening-angle ↔
  relative force error (Barnes & Hut 1986 and successors; Dehnen 2002); what force
  error star-cluster codes tolerate.
- Any precedent for OUTER smooth truncation of gravity (P³M/Ewald short-range
  switching, MOND-free outer cutoffs, etc.) and, if one exists, guidance on the
  switching-shell WIDTH (our outer/inner = 3 is currently convention, not physics).
  If the literature has nothing on shell width, say so explicitly — we will then keep
  the 3× convention justified by our internal energy-conservation tests.

### E. (secondary, non-ADS acceptable) Operational force-model practice
Spacecraft-navigation force models: which third bodies/asteroids are included for Mars
missions (JPL "Big16"?), what GMAT/Orekit defaults do. Documentation sources are fine
here; keep it brief — one paragraph.

## The synthesis question (answer explicitly)

The design must choose a **criterion type**, then a value:
1. absolute acceleration floor (current: cut where a < 1e-12 m/s²), vs
2. relative significance (cut where a_pair/a_dominant < ε — R3's vessel-path rule), vs
3. observable-effect based (cut what changes a measurable by < X over span T — the
   ephemeris-construction style).
Which does the evidence support for a self-consistent game simulation, and what value?
Give: recommended a_floor (or equivalent), an acceptable range, what each end of the
range trades (drift vs surviving pair count — recall the asteroid↔asteroid win needs
r_c(μ~1e9 m³/s²) below typical belt separations), and a sanity check against the
NearStars roster (no bound binary wider than the r_c of its primary; verify from db).
Also state a recommendation for the shell ratio with whatever support exists.

## Method requirements

- ADS API with targeted queries per angle (the phase3 bibliography pipeline is NOT
  needed — direct `search/query` calls suffice); read abstracts, and full text via
  arXiv/ar5iv for the load-bearing numbers. Do not cite numbers from WebFetch summaries;
  read the raw source. Pin every claim to a bibcode (+ arXiv id where available).
- ~15–25 papers is the expected scale; prefer primary sources over reviews except for
  angle C where a review is fine for the observed-population numbers.
- Structure the report by angle (A–E), each ending with a boxed "numbers extracted"
  list; final section = the synthesis answer above.
- If an angle comes up genuinely empty, record that as a finding (absence of precedent
  is itself an input — we then own the choice with internal tests).
