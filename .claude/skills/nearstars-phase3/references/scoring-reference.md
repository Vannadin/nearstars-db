<!-- Phase 3 점수 시스템 참조 — authority+relevance 채점 schema, 임계값 결정 근거 -->
# Phase 3 paper scoring — reference

`scripts/phase3/score_papers.py` annotates each paper with three
scores. This file documents the schema, threshold rationale, and
common edge cases.

## Authority score (0–10)

Baseline: 3 (neutral). Adjustments:

| Signal | Δ |
|---|---|
| Top journal (Nature, NatAs, Sci, ApJ, A&A, PSJ, AJ, MNRAS, …) | +3 to +5 by tier |
| Conference proceedings (EPSC, EGU, AGU, AAS, BAAS, DPS, …) | −3 |
| Observing proposal (jwst.prop, hst.prop, etc.) | −4 |
| Data catalog (VizieR, yCat, zndo, …) | −3 |
| Erratum / retraction | −2 |
| Has arXiv preprint | +2 |
| Has DOI | +1 |

The +2 for arXiv preprint reflects reproducibility (full text
accessible) rather than peer-review status — peer-reviewed
preprints get an additional journal bonus.

Top journal full table:

| Bibcode segment | Δ |
|---|---|
| `Nature` (1976+) | +5 |
| `NatAs` (Nature Astronomy 2017+) | +5 |
| `Sci` (Science) | +5 |
| `PNAS` | +4 |
| `ApJ`, `ApJL`, `A&A`, `A&AL`, `PSJ`, `AJ`, `AJL`, `MNRAS`, `MNRASL` | +4 |
| `Icar`, `JGRE`, `EPSL`, `GeCoA`, `AsBio`, `PASP`, `PASA` | +3 |
| `P&SS`, `AcAau` | +2 |

Conference penalty list:

| Bibcode segment | Δ |
|---|---|
| `epsc.conf`, `EPSC`, `EGUGA`, `AGUFM`, `DPS`, `BAAS`, `AAS`, `EAS`, `AbSciCon`, `absc.conf`, `ESS` | −3 |
| `IAU` | −2 |

## Relevance score (0–10)

Baseline: 0. Score builds up from signal hits:

| Signal | Δ |
|---|---|
| System name in title (e.g. "TRAPPIST-1") | +4 |
| System name in abstract only | +2 |
| Planet letter in title (e.g. "TRAPPIST-1 d") | +5 |
| Planet letter in abstract only | +3 |
| ≥2 relevant topic keywords | +1 |
| ≥4 relevant topic keywords | +2 |
| ≥6 relevant topic keywords | +3 |
| Skip pattern hit (SETI, biofluorescence, tardigrade, etc.) | −5 |
| Other system primary subject (LHS 1140, K2-18, Proxima, etc.) | −3 |

Relevant topic keywords include the full vocabulary of
cfg-decision-relevant physics: atmosphere/CO2/N2/O2/H2O/cloud/haze/
aerosol/greenhouse/climate/GCM/photochemistry/escape/outgassing/
transmission spectrum/emission spectrum/eclipse depth/phase curve/
dayside/nightside/equilibrium temperature/albedo/habitable zone/
habitability/ocean/snowball/aquaplanet/magma ocean/volcanism/
tectonic/interior structure/water mass fraction/core mass/
density/magnetic field/cosmic shoreline/M dwarf/ultracool/XUV/flare/
stellar wind/moon/satellite/ring.

The full list with regex patterns lives in `score_papers.py`
`RELEVANT_TOPICS`.

## Combined score thresholds

| Combined (auth + rel) | Decision | Action |
|---|---|---|
| ≥ 14 | must-read | deep-read in full, extract cfg numbers |
| 10 ≤ score ≤ 13 | keep | OK to cite in bibliography, skim only |
| 8 ≤ score ≤ 9 | borderline | judgment call; usually cite-only |
| < 8 | skip | mark `status: skipped`; not worth fetching |

Threshold choice rationale:

- A peer-reviewed top-journal paper (auth 9–10) about another system
  with 4+ topic hits: auth 9 + rel 2 = 11 → keep (worth citing)
- A peer-reviewed top-journal paper directly about the planet
  (auth 9 + rel 8) = 17 → must-read
- A conference proceeding mentioning the planet in passing
  (auth 0 + rel 4) = 4 → skip
- A proposal abstract for JWST observations of this planet
  (auth -1 + rel 8) = 7 → skip (low confidence, observations may
  not have happened)
- A top-tier system-wide review (auth 9 + rel 6 system-in-title) =
  15 → must-read

## Score distribution sanity check

For TRAPPIST-1 d (439 papers after expansion):

```
score=10: ~112 papers (mostly comparison-system papers)
score=14: ~8   papers (peer-reviewed direct planet observations)
score=17: ~20  papers (high-impact JWST results, system-wide reviews)
score=20: ~6   papers (top-tier direct planet results — Nature, PSJ)
```

If the distribution is heavily skewed toward 10 (combined of
mid-authority + mid-relevance), the citation expansion brought in
mostly comparison-object papers. This is expected for tightly-cited
planetary-science work.

## Edge cases

- **Multi-planet papers** (e.g. "TRAPPIST-1 d, e, f atmospheric retrieval")
  may not score highest for any single planet but are critical
  context. The system-level bib (`_system-<slug>.yaml`) catches these.
- **Methodology papers using the planet as a test case** (e.g. Aurora
  retrieval framework tested on TRAPPIST-1 d) score high on
  relevance but contribute only methodology to the cfg. They're
  legitimate "must-read" entries — they constrain the observability
  framing in the Atmosphere section.
- **Recent Nature Astronomy papers without arXiv preprints**
  (2026NatAs.tmp...) score high but are unfetchable. Document them
  in `manual-paper-followup.md` Tier A.

## How to adjust thresholds

If the filtered set is too noisy (still >50 must-read per planet),
raise `--keep-threshold` from 8 to 10 or 12. The fetch step then
processes fewer papers but the synthesis prose loses some context.

If the filtered set is too thin (<10 must-read), lower threshold to 6
and re-run scoring. Most likely cause: the system has few JWST
observations yet (e.g. a recently-discovered exoplanet system) and
the bib is dominated by theoretical predictions.

The TRAPPIST-1 keep-threshold of 8 was tuned empirically against the
deep-read set that the user validated.
