# R research prompt — grounding the synthetic-eccentricity policy parameters (run in NearStars, ADS)

Copy everything below the line into a NearStars session (it has the ADS API token and the
`scripts/phase3/build_bibliography.py` pattern for `https://api.adsabs.harvard.edu/v1/search/query`).
The output report comes back to the Phase-4 / cfg-emit session, which will fix the two parameters.

---

## Task

You are grounding **two numerical policy parameters** of the NearStars "synthetic
eccentricity" cfg-layer feature in the literature. Produce
`plans/principia-interstellar-branch/research/R-synthetic-eccentricity.md` (or the agreed
`docs/`/`plans/` path) — a self-contained report with numbers, bibcodes, and short verbatim
quotes. **Another session will set the two parameters from your report alone**, so include
the evidence (the distribution fits, the sigma values, the stability limits, the bibcodes,
short quotes), not just conclusions.

The two parameters to ground:
1. **The upper cap on seeded eccentricity** (provisionally the arbitrary `e ≲ 0.05`) — the
   maximum synthetic e the emitter is allowed to draw.
2. **The shape of the seed distribution** — the functional form and its parameter(s) the
   emitter draws from (e.g. Rayleigh with some σ_e, vs a Beta distribution, vs uniform),
   ideally resolved **per body class** (isolated wide-orbit planet vs compact multi vs
   tidally-circularized short-period planet).

## Context (what was built / decided; do not re-derive)

NearStars is a KSP planet-pack pipeline. Many catalogued planets carry `eccentricity = 0.0`
(or null → default 0) not because it was *measured* but because the orbit fit fixed or left
e unconstrained. Perfectly circular orbits are physically unreal (tidal circularization
leaves a small residual — Venus 0.007, Earth 0.017; secular forcing from other planets
pumps e even from circular initial conditions). So the pipeline's **downstream cfg-emit
stage** perturbs those default-zero eccentricities with a small **seeded** value, for
realism and gameplay variety. This is a specific case of the broader Phase-4
"synthetic orbital noise" policy (`phase4/synthetic-orbit-noise.md`).

Guardrails already decided (do **not** relitigate these — they are fixed inputs):
- **Measured eccentricities are never touched.** Only orbital blocks whose e is a
  default/assumption (fit-fixed, consistent-with-0, or null-filled) are eligible. The DB
  records `orbital.source`/`orbital.bibcode` per planet — that provenance is the gate.
  TTV-locked compact chains (TRAPPIST-1) and tidally-circularized hot planets are treated
  as genuinely ~0 and excluded.
- **DB is immutable.** The synthetic e lives only in the cfg / emit layer as a flagged
  artistic value; `db/planets_curated.json` keeps `e = 0.0`. Build is reproducible:
  `cfg = f(db, phase3, phase4, per-system seed)`.
- **Seeded / deterministic**, per-star-system seed key (each system an independent,
  re-rollable realization; re-rolling one system does not disturb others). No build-to-build
  RNG.
- **Provisionally seeded e ≲ 0.05** (the value this report must justify or replace).
- **Multi-planet / resonant systems must pass the REBOUND stability sim**
  (`phase3/stability-sim/`, REBOUND + MEGNO, Hill-sphere + ejection checks) after
  perturbation; single isolated wide planets skip it. Note the physical coupling: in a
  multi-planet or resonant system e is coupled through AMD / mean-motion resonance, so the
  per-planet draws are not independent and the cap interacts with stability.
- A soft **upper physical ceiling** is already noted at e ≳ 0.1: beyond it a 1:1
  tidal lock breaks to pseudo-synchronous rotation and T_eq / insolation cascade through
  Phase 3 re-derivation. So the cap of interest sits somewhere in ~0.02–0.1.

**Roster / data to sanity-check against (verify live from the repo):**
- `db/planets_curated.json` — per-planet `orbital.eccentricity` + `orbital.source`.
  At time of writing: **204 planet orbital blocks — 20 with exact `e = 0`, 35 with null e
  (both are seeding candidates), 149 with a nonzero measured e.** Verify these counts and
  report the actual distribution of the *measured* nonzero e values (this is the real
  in-project reference distribution the synthetic tail should not obviously overshoot).
- Confirmed implementation roster (α Cen, Barnard, τ Cet, 40 Eri, Fomalhaut, TRAPPIST-1,
  Luhman 16) — identify which of *their* planets are seeding candidates and what a chosen
  distribution would hand them.
- `phase3/stability-sim/` logs already contain eccentricity/inclination scans for several
  systems — reference any existing empirical stability bound on e they establish.

**Use profile to weigh against.** The consumer is a *game*, not an ephemeris: the seeded e
must (a) visibly break the "perfect circle" look, (b) stay statistically plausible against
the real observed small-planet eccentricity distribution, and (c) never push a multi-planet
system out of the already-validated stability envelope. There is no observational precision
to match — the target is population realism, not reproducing a specific system.

## Research angles

Fan out one agent per angle (`model: "opus"`, non-fork). Each angle ends with a boxed
"numbers extracted" list `(bibcode / arXiv id, the number, the quote or cache line)`. The
candidate anchor papers below are **starting points to ADS-verify, not a trusted list** —
verify each against ADS and replace freely; find the best-cited primary sources
independently (`sort=citation_count desc`).

### A. The observed eccentricity distribution of small / RV planets (the core of parameter 2)
What functional form and parameter best describe the eccentricity distribution of the
planet population NearStars actually seeds — low-mass RV planets and *Kepler* small planets?
- Candidate anchors: Kipping 2013 (Beta-distribution prior for eccentricity); Van Eylen et
  al. 2019 (eccentricity of *Kepler* small-planet / multi systems, near-circular);
  Xie et al. 2016 (statistical eccentricities from transit + TTV); Mills et al. 2019;
  Limbach & Turner 2015 (eccentricity vs multiplicity); Zakamska, Pan & Ford 2011 (RV
  eccentricity bias — fits *manufacture* small nonzero e, relevant to why catalogue e≈0).
- **Deliverable:** the recommended distribution shape (Rayleigh σ_e? Beta(a,b)? which),
  with the fitted parameter value(s) and the population each was fit to — split by
  **single-planet vs multi-planet**, since multis are systematically more circular. A
  quantitative Rayleigh σ_e (or its Beta equivalent) is the headline number.

### B. Tidal-circularization residual — the realistic *floor*, and the "not exactly zero" argument
How small is the residual eccentricity of a body that has tidally circularized but is not
mathematically zero, and what keeps it nonzero?
- Candidate anchors: Goldreich & Soter 1966 (Q, circularization); Hansen 2010 (tidal
  dissipation in exoplanets); Bolmont et al. / Barnes et al. (tidal evolution tracks);
  secular-forcing / AMD-equilibrium eccentricity in multi-planet systems (a companion keeps
  e off zero even after circularization). Solar-system residuals (Venus 0.007, Earth 0.017,
  0.05-ish for several) as calibration anchors.
- **Deliverable:** the order of magnitude of a realistic residual e for a circularized
  planet and the mechanism (secular forcing floor), i.e. the *lower* end of a sensible seed
  range and confirmation that a strictly-nonzero seed is physically motivated.

### C. Dynamical stability ceiling — how large a seeded e a packed system tolerates (the core of parameter 1)
Independent of what is *observed*, what upper e does dynamics permit before a compact /
resonant system destabilizes — i.e. the hard cap the stability gate will enforce anyway?
- Candidate anchors: Laskar & Petit 2017 (AMD stability criterion); Petit, Laskar & Boué
  2018 (AMD + MMR); Hill-stability / Gladman 1993 two-planet criterion;
  Pu & Wu 2015 (spacing / stability of *Kepler* multis, "dynamical packing"); Fabrycky et
  al. 2014 (architectures & stability of Kepler multis). Also any circularization-vs-secular
  work bounding equilibrium e in packed systems.
- **Deliverable:** the AMD / Hill e-budget for a typical compact multi (translate the
  criterion into an approximate max per-planet e for representative spacings), and a
  statement of how the observed distribution's tail (angle A) sits relative to this ceiling.
  This is the evidence that fixes the numeric cap.

### D. Why a static seeded e is self-consistent — secular pumping from circular ICs
Justification that assigning a small *static* e at t=0 is not a physics violation: mutual
secular perturbations drive e to a nonzero forced/free amplitude regardless of the initial
value, so a zero start is *less* physical than a small seeded one.
- Candidate anchors: Laplace–Lagrange secular theory (textbook — allowed exception, cite a
  standard treatment e.g. Murray & Dermott); forced-vs-free eccentricity in observed systems;
  any Kepler-multi secular-amplitude study.
- **Deliverable:** one calibrated statement — the typical secular *forced* eccentricity
  amplitude in a compact multi, showing the seed magnitude the population implies is the
  same order as what secular dynamics would produce anyway. (Keep brief; this angle mainly
  confirms the concept, it need not drive a number.)

## The synthesis question (answer explicitly)

Recommend, with the range each choice trades off:

1. **Distribution shape (parameter 2).** Pick a functional form and its parameter(s):
   - **Rayleigh(σ_e)** — one scale parameter, simple, matches many population fits; recommend σ_e.
   - **Beta(a,b)** — Kipping-style, better tail behaviour; give (a,b) if preferred.
   - **uniform[0, e_cap]** — simplest, least physical; state why rejected or accepted.
   Resolve **per body class** if the evidence supports it: isolated wide planet (looser),
   compact multi (tighter, near-circular σ), tidally-circularized short-period (tightest /
   or excluded). State the σ_e (or equivalent) for each class.

2. **Upper cap (parameter 1).** Replace or justify `e ≲ 0.05`: give a recommended cap, an
   acceptable range, and what each end trades — realism/variety (higher) vs stability-gate
   pass rate and the tidal-lock ceiling at e ≳ 0.1 (lower). The cap should be consistent
   with *both* the observed-distribution tail (angle A) and the AMD/Hill ceiling (angle C);
   flag if those two disagree. Recommend whether the cap is a hard truncation of the chosen
   distribution or a per-class value.

3. **Sanity checks (required, against live repo data):**
   - Draw the recommended distribution for the current **20 exact-zero + 35 null**
     candidate planets (verify counts) and confirm the synthetic tail does not overshoot the
     **149 measured nonzero e** already in `db/planets_curated.json`.
   - For each confirmed-roster multi (α Cen, τ Cet, 40 Eri, TRAPPIST-1, …) state the max
     seeded e the chosen cap would allow and confirm it sits inside the empirical stability
     bound already found in `phase3/stability-sim/` logs (or flag that a fresh sim is needed).
   - Confirm the recommended floor/shape yields a *strictly nonzero* seed (never re-emits 0).

## Method requirements

- **ADS discipline (non-negotiable).** All paper discovery and verification through the NASA
  ADS API (`ADS_API_TOKEN`) with targeted `search/query` calls per angle — never WebSearch,
  and never cite numbers from WebFetch summaries. Read abstracts, and full text via
  arXiv/ar5iv for the load-bearing distribution/stability numbers; check the
  `docs/phase3/_papers/<arxiv_id>.md` cache before re-fetching and add to it. The phase3
  bibliography pipeline is not required; direct queries suffice.
- **Pin every claim** to a bibcode (+ arXiv id where one exists). Note explicitly when a
  paper has no preprint (verified by bibcode only).
- **Discovery is delegated, not dictated.** The anchors above are candidates only; verify
  each against ADS and find the best-cited primary sources independently.
- **Textbook relations are the allowed exception** (Laplace–Lagrange secular theory, the
  Beta/Rayleigh definitions themselves) — cite a standard treatment, no ADS entry needed.
- Expected scale **~15–25 papers**; prefer primary sources over reviews (a review is
  acceptable for angle A's population-level distribution summary).
- If an angle comes up genuinely empty — e.g. no literature fixes a seed *shape* for this
  use — **record that as a finding**: absence of precedent means we own the choice, justified
  by the observed distribution + the internal REBOUND stability tests. Never backfill a
  citation to make a chosen value look grounded.
- Structure the report by angle (A–D), each ending with a boxed "numbers extracted" list;
  final section = the synthesis answer above, giving the two parameters as concrete
  emitter-ready values with their ranges.
