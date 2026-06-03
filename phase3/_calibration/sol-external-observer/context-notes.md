# Context notes — Solar System external-observer benchmark

Append-only decision log.

## Framing decisions (2026-06-03)
- This is **not a true blind test** (Claude knows the answers). It is a
  **methodology trace**: feed the documented Phase 3 decision procedure
  ONLY the degraded inputs an external observer would have, record what
  it outputs, then reveal ground truth and score. The value is exposing
  *systematic* failure modes (structural, blinding-independent), not
  proving Claude can't recognize Earth.
- Deliverable is a calibration reference, NOT a DB system. Sol is "us,"
  not a ≤50 ly addable target (per [[project-beyond-50ly-survey]] /
  principia-range cap). No db/ mutation.
- Fiducial distance 10 pc (standard exoplanet fiducial). Astrometry &
  imaging scale with distance; RV & transit do not — noted in census.

## Detectability physics (formulas used in detectability.py)
- RV: K = 28.4329 m/s × (1/√(1−e²)) × (Mp sin i / M_Jup) × ((M*+Mp)/M_sun)^(−2/3) × (P/yr)^(−1/3)
- Astrometry: α[arcsec] = (Mp/M*) × (a/AU) / d[pc]   (stellar reflex semi-major axis / distance)
- Transit: depth = (Rp/R*)² ; geometric prob ≈ R*/a (binary per system — alignment noted as scenario)
- Imaging: contrast = A_g × (Rp/a)² (full phase) ; separation = a/d
- Teq = 278.3 K × (1−A_B)^(1/4) × (a/AU)^(−1/2) × (L*/L_sun)^(1/4)

## Findings

### Stage 1 — detectability census @ 10 pc (verified)
Detected set: **Jupiter** (RV 12.5 m/s + astrometry 497 µas + imaging
4.5e-9 @ 0.52" — all YES) and **Saturn** (RV 2.8 m/s + astrometry 274 µas,
both at the ~30 yr baseline boundary; imaging 8.8e-10 just below floor → no).
Uranus/Neptune: astrometry marginal but need century+ baselines. **All four
terrestrials (+ Mercury): below threshold in every channel.** Titan (and any
moon): cannot be isolated by star channels at all.

Headline: from 10 pc the Sun is catalogued as **a G2V with one cold Jupiter
(plus Saturn after decades)**. The entire terrestrial HZ — including Earth —
is dark. Transit needs the alignment lottery (Earth 0.47%, Jupiter 0.09%).

### Killer result — Venus (greenhouse blindness)
Teq(assumed A=0.30) = 299 K; Teq(true A=0.77) = 227 K; actual Tsurf = 737 K.
Either way an external observer synthesizes a **temperate/cool cloudy world**
— the 92-bar CO₂ runaway is invisible to Teq. Earth shows the same defect
softer: Teq 255 K reads as frozen, greenhouse lifts it to 288 K liquid-water.

### Systematic failure modes (for Stage 5 aggregate)
1. Teq ≠ Tsurf (greenhouse blind) — Venus catastrophe, Earth frozen-vs-temperate.
2. No radius without transit → density/composition degenerate.
3. sin i only broken by astrometry (giants yes, terrestrials no).
4. All terrestrial masses below RV floor → no density even if transiting.
5. Iconic visual features (Saturn rings, Jupiter GRS, surface color) sub-resolution → pure tie-break territory.
6. Moons invisible → Titan/Europa/Enceladus class is a total blind spot.
7. Architecture selection bias → home reads as a sparse giant-only system.

### Calibration takeaway
NearStars confidence stratification maps cleanly onto observability:
mass-derived **class** (high-confidence) is exactly what survives external
observation; **surface color / clouds / morphology** (synthesized / low) is
exactly what's unobservable. Interesting-first tie-breaks are load-bearing
and unfalsifiable — and would plausibly land for surface color (Mars red,
Jupiter banded); the dangerous errors are Teq-driven (Venus temperate),
upstream of the tie-break.
