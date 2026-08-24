# The Solar System as an External Observer Would See It

> A Phase 2/3 calibration benchmark. We run the NearStars pipeline on
> the one planetary system whose ground truth we know cold — our own —
> while pretending to be an exoplanet astronomer 10 pc away. The point
> is to see what an external observer *recovers* and what they *miss*,
> and to check whether the pipeline's confidence tiers (measured vs.
> synthesized) line up with what is actually observable.
> No DB changes — Sol is "us," not a ≤50 ly catalog target. Findings only.
> Census numbers are reproducible:
> `phase3/_calibration/sol-external-observer/detectability.py`.

---

## TL;DR

> **From 10 pc the Sun is "a G2V with one cold Jupiter."** Jupiter is
> the only body cleanly detected (RV + astrometry + reflected-light
> imaging). Saturn shows up after ~30 years of data. The entire
> terrestrial habitable zone — Earth included — is below threshold in
> every channel.

> **Venus is the killer.** Its equilibrium temperature reads 227–299 K
> (depending on the albedo assumption), so an external observer
> synthesizes a temperate cloudy world. The actual surface is 737 K. The
> 92-bar CO₂ runaway greenhouse is invisible to T_eq. This is the single
> most important calibration result: *T_eq is a floor, not the surface.*

> **The confidence tiers hold up.** What NearStars marks high-confidence
> (mass-derived planet *class*) is exactly what survives external
> observation. What we mark synthesized / low (surface color, clouds,
> morphology) is exactly what is unobservable — so the interesting-first
> tie-breaks are load-bearing *and* unfalsifiable, which is the honest
> situation. The dangerous errors are not in the tie-breaks; they are
> upstream, in T_eq-driven climate reads (Venus).

---

## 1. The fiducial observer

| Parameter | Value |
|---|---|
| Distance | 10 pc (standard exoplanet fiducial) |
| RV precision | 0.1 m/s (ESPRESSO-class ≈ the Sun's own jitter floor) |
| RV baseline | ~30 yr (need ≈1 full orbit for a clean detection) |
| Astrometry | 20 µas mission signal (Gaia-class) |
| Transit | 20 ppm depth floor (PLATO / JWST) **+ geometric alignment** |
| Imaging | reflected-light contrast 1e-9 at ≥0.1″ inner working angle (Roman CGI / HWO / ELT) |

RV and transit signals do not depend on distance; astrometric and
imaging detectability do (both scale as 1/d), so the picture worsens
quickly beyond 10 pc and improves for the nearest stars.

---

## 2. Detectability census @ 10 pc

| Body | K_RV | Astrom. | Transit depth (prob) | Imaging C @ sep | T_eq(A=.30) | T_eq(true A) | T_surf | Detected? |
|---|---|---|---|---|---|---|---|---|
| Mercury | 0.008 m/s | 0.0 µas | 12 ppm (1.20%) | 2.5e-10 @ 0.04″ | 409 | 440 | 440 | **no** |
| Venus | 0.086 | 0.2 | 76 ppm (0.64%) | 2.2e-9 @ 0.07″ | 299 | 227 | **737** | **no** |
| Earth | 0.089 | 0.3 | 84 ppm (0.47%) | 7.9e-10 @ 0.10″ | 255 | 254 | 288 | **no** |
| Mars | 0.008 | 0.0 | 24 ppm (0.31%) | 3.8e-11 @ 0.15″ | 206 | 210 | 210 | **no** |
| **Jupiter** | **12.47** | **497** | 1.05% (0.09%) | **4.5e-9 @ 0.52″** | 112 | 102 | 165 | **YES** (RV+astrom.+imaging) |
| **Saturn** | 2.76 | 274 | 0.75% (0.05%) | 8.8e-10 @ 0.96″ | 82 | 81 | 134 | **marginal** (RV+astrom., decadal; no imaging) |
| Uranus | 0.30 | 84 | 1348 ppm (0.024%) | 3.9e-11 @ 1.92″ | 58 | 58 | 76 | marginal astrom. (century baseline) |
| Neptune | 0.28 | 155 | 1262 ppm (0.015%) | 1.3e-11 @ 3.01″ | 46 | 47 | 72 | marginal astrom. (century baseline) |
| Titan | — | — | (moon) | — | 82 | 83 | 94 | **invisible** (cannot isolate from Saturn) |

What an external observer would actually catalog at 10 pc: **one
confirmed giant (Jupiter)** — mass ≈ 1 M_Jup from RV + astrometry (the
two channels together break the sin i ambiguity), a ≈ 5.2 AU, T_eq ≈
110 K, reflected-light colors and a methane band from imaging
spectroscopy — and, after a multi-decade campaign, **a second, smaller
giant (Saturn)**. Nothing else. The system would be classified as a
sparse cold-giant architecture. The terrestrial zone is dark.

The transit column is the alignment lottery: depths are easily
detectable (Earth 84 ppm, Jupiter 1%), but the geometric probability of
*any* alignment is 0.05–1.2% per body, and they are not independent
(coplanar). For one specific system you either see transits or you don't.

---

## 3. Method — a trace, not a blind test

We cannot truly blind ourselves to the answer (we know Earth is blue).
So this is a **methodology trace**, not a blind experiment: feed the
documented Phase 3 decision procedure *only* the degraded inputs an
external observer would have, record what it outputs, then reveal the
truth and score it. The value is exposing the *systematic, structural*
failure modes — the ones that do not depend on blinding and would bite
any real external observer regardless of how clever they are.

We synthesize six bodies: the two detected giants (Jupiter, Saturn) and
four counterfactual "if it had been characterized" cases (Earth, Venus,
Mars, Titan). For each: what the observer has → what the pipeline
synthesizes → ground truth → score (✓ recovered / ~ partial / ✗ missed).

---

## 4. Per-body benchmark

### Jupiter — the one we get right

- **Observer has:** true mass ≈ 1 M_Jup (RV+astrometry), a ≈ 5.2 AU,
  e ≈ 0.05, T_eq ≈ 110 K, geometric albedo ≈ 0.5 and a CH₄ reflectance
  band from imaging spectroscopy. **No radius** (does not transit).
- **Pipeline synthesizes:** a cold (~110–165 K) H/He gas giant at 5 AU;
  high albedo → reflective cloud decks; CH₄ detected → methane in a
  reducing atmosphere with NH₃/H₂O clouds at depth. Surface color is a
  tie-break → interesting-first picks banded beige/tan.
- **Truth:** H/He + CH₄/NH₃, beige banded cloud tops, 165 K at 1 bar.
- **Score:** class ✓, mass ✓, albedo ✓, CH₄ ✓, banded tan ✓ (tie-break
  lands), radius/density ✗ (no transit), Great Red Spot ✗ (sub-resolution).
- **Lesson:** giants are forgiving — mass → class is robust, and the one
  body we detect well is also the one we synthesize well.

### Saturn — class right, identity lost

- **Observer has:** mass ≈ 0.3 M_Jup (after ~30 yr), a ≈ 9.6 AU,
  T_eq ≈ 80 K. No imaging (contrast just below floor), no radius.
- **Pipeline synthesizes:** a cold sub-Jupiter H/He giant at ~10 AU.
- **Truth:** yes — but **the rings are completely invisible.** Saturn's
  single most iconic feature does not register in any channel.
- **Score:** class ✓, mass ✓, rings ✗✗, all visual ✗.
- **Lesson:** defining-but-thin structures (rings) are sub-detection.
  An external observer would never guess Saturn looks like Saturn.

### Earth — reads as a snowball

- **Observer has:** *if* it transits, R ≈ 1 R⊕; T_eq ≈ 255 K (A=0.3).
  **Mass is unmeasurable** (K = 0.09 m/s, below the RV floor), so even a
  transit gives radius without density. A heroic transmission campaign
  might pull O₃/H₂O/CO₂.
- **Pipeline synthesizes:** a rocky world at the inner HZ edge with
  T_eq ≈ 255 K → *frozen / icy* surface. Density degenerate (no mass) →
  rocky-vs-water ambiguous. If O₂/O₃ is detected, the biosignature flag
  flips interesting-first toward oceans + life.
- **Truth:** 288 K, liquid-water oceans, N₂/O₂. The 33 K greenhouse that
  makes it habitable is unmodeled by T_eq.
- **Score:** HZ position ✓, rocky ~, frozen-vs-temperate ✗ (T_eq says
  frozen), oceans/blue ✓ only via biosignature + tie-break, mass ✗.
- **Lesson:** T_eq alone calls Earth a snowball; the greenhouse uplift
  that defines habitability is invisible without atmospheric modeling.

### Venus — the catastrophe

- **Observer has:** *if* it transits, R ≈ 0.95 R⊕; T_eq = 299 K (A=0.3)
  or 227 K (measured A=0.77 — Venus is very bright); mass unmeasurable;
  a strong CO₂ transmission feature, possibly SO₂/sulfate clouds.
- **Pipeline synthesizes:** a temperate-to-cool, highly reflective
  cloudy rocky world near the inner HZ — plausibly read as a wetter,
  cloudier Earth analog. The high albedo *lowers* the inferred
  temperature, reinforcing "temperate."
- **Truth:** **737 K**, 92-bar CO₂, sulfuric-acid clouds, a lead-melting
  runaway-greenhouse hellscape.
- **Score:** ✗✗✗ catastrophic — every climate-relevant decision inverted.
- **Lesson:** **T_eq is blind to the greenhouse, and high albedo (bright
  clouds) does not mean a cool surface.** The CO₂ feature is the only
  hint, and it does not quantify surface T. This is the canonical
  Venus/Earth degeneracy, and it is the strongest argument for treating
  T_eq as a *lower bound* whenever a greenhouse-capable atmosphere
  (CO₂/H₂O-rich) is present.

### Mars — recovered, if only it were detectable

- **Observer has:** *if* it transits, R ≈ 0.53 R⊕ (small); T_eq ≈ 206 K;
  mass unmeasurable; thin atmosphere → weak/absent transmission features.
- **Pipeline synthesizes:** a small, cold rocky world (T_eq ≈ 206 K →
  frozen desert); low gravity from small radius → thin escaped
  atmosphere inferred; surface color tie-break → oxidized iron red is a
  reasonable interesting-first pick for an old rocky surface.
- **Truth:** 210 K, thin CO₂, rusty red. Closely matches.
- **Score:** cold ✓, rocky ✓, thin atmosphere ✓, red ~ (tie-break could
  land). One of the better recoveries — *but it is never detected.*
- **Lesson:** "small + cold + far" → frozen desert is a robust read;
  the limitation for Mars-class worlds is detection, not synthesis.

### Titan — the invisible class

- **Observer has:** essentially nothing. A moon cannot be isolated by
  stellar RV/transit, and even its host (Saturn) is marginal. Titan
  contributes zero signal at 10 pc.
- **If somehow characterized:** R ≈ 0.40 R⊕, T_eq ≈ 82 K, a thick
  N₂ atmosphere with CH₄ → photochemical haze.
- **Truth:** 94 K, thick orange tholin haze, liquid-methane lakes.
- **Score:** detectability ✗✗ (the headline), cold ✓ and haze ~ only in
  the counterfactual.
- **Lesson:** the entire large-moon population — Titan, Europa,
  Enceladus, the richest small-body real estate in our system — is a
  total blind spot. "How alien would home look?" Our most interesting
  worlds do not even register.

---

## 5. Systematic failure modes

| # | Failure mode | Where it bit | Severity |
|---|---|---|---|
| 1 | **T_eq ≠ T_surf** (greenhouse blindness) | Venus (227–299 → 737 K), Earth (255 → 288 K) | catastrophic |
| 2 | **No radius without transit** → density/composition degenerate | Jupiter, Saturn (detected but radius-less) | high |
| 3 | **sin i** broken only by astrometry | giants yes; terrestrials no | medium |
| 4 | **All terrestrial masses below RV floor** → no density even when transiting | Earth, Venus, Mars | high |
| 5 | **Iconic visual features sub-resolution** | Saturn's rings, Jupiter's GRS, all surface color | medium (tie-break territory) |
| 6 | **Moons invisible** | Titan and the whole large-moon class | high (blind spot) |
| 7 | **Architecture selection bias** | home reads as a sparse giant-only system | framing |

---

## 6. Calibration takeaways for NearStars Phase 3

1. **Trust mass → class for giants; flag radius-less density as
   low-confidence.** The benchmark confirms the giant-planet class call
   is the most robust thing an external observer derives.

2. **Treat T_eq as a lower bound on surface temperature whenever a
   greenhouse-capable atmosphere is present.** Never synthesize surface
   conditions from T_eq alone for a CO₂/H₂O-rich world. Venus is the
   cautionary tale: a pipeline that reads surface climate off T_eq would
   synthesize a temperate Venus every time. Where a body's atmosphere
   suggests a strong greenhouse, the surface-T row should carry a wide
   unconstrained-uplift caveat, not a point estimate.

3. **The confidence stratification is honest.** Measured (high-confidence)
   = observable; synthesized (low-confidence) = unobservable. The map is
   nearly one-to-one. This is reassuring: we mark exactly the right
   things as uncertain.

4. **Interesting-first tie-breaks are load-bearing and unfalsifiable —
   and that is fine.** For *surface color / morphology* the observer has
   no data at all, so the tie-break is the only thing that can populate
   the row, and it cannot be proven wrong. The benchmark suggests these
   picks would often land plausibly (Mars red, Jupiter banded). The
   genuinely dangerous errors are not in the tie-breaks; they are
   upstream, in T_eq-driven *climate* reads — which is exactly where
   takeaway #2 puts the guardrail.

5. **Detection, not synthesis, is the binding constraint for small
   worlds.** Mars and Titan would be synthesized reasonably well *if*
   characterized — but at 10 pc they (and Earth, and Venus) are never
   detected. For the NearStars catalog this is the reassuring direction:
   the systems we curate are the ones near enough and favorable enough to
   actually have measured planets, so we operate on the detectable tail,
   not the dark majority.

---

## 7. Reproducing the census

```bash
python3 phase3/_calibration/sol-external-observer/detectability.py            # @ 10 pc
python3 phase3/_calibration/sol-external-observer/detectability.py --distance 5
```

The script encodes the RV, astrometry, transit, imaging, and T_eq
formulas (see its header) with NASA fact-sheet body parameters. Spot
checks: Jupiter K = 12.5 m/s and α = 497 µas; Earth K = 0.09 m/s; Venus
T_eq(A=0.30) = 299 K vs. T_surf = 737 K.
