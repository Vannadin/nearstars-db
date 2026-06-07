<!-- alpha Cen A b 동역학 연구 + 이번 세션 작업 정리 (방법론·도구·결과·재현) -->
# Alpha Centauri A b — A Dynamical Habitability Study of the Real-Life Polyphemus

**Session writeup, 2026-06-07.** Methods, tools, results, and reproducibility
for the NearStars work on α Centauri A b (Beichman et al. 2025's JWST/MIRI
candidate "S1"), its identification with *Avatar*'s gas giant **Polyphemus**,
and whether a habitable **Pandora**-class moon can survive there. Includes the
supporting N-body stability framework built/extended this session.

---

## Abstract

We treat the JWST/MIRI direct-imaging candidate α Cen A b (Beichman et al. 2025;
Saturn-class, ~1.6 AU, in α Centauri A's habitable zone) as the real-life
*Polyphemus* of *Avatar* and ask whether its canonical moon Pandora could be
dynamically stable. Using REBOUND with a hybrid integrator policy (WHFast +
MEGNO as a screen; TRACE for close-encounter fidelity; **IAS15 as the canonical
integrator for α Cen, whose forcing is secular from a massive distant companion
rather than close-encounter — TRACE is inaccurate there**), we find: (1) the
**observed favored orbit (e≈0.4, mutual inclination ≈50° to the α Cen AB
plane) is eccentric-Kozai-Lidov unstable** — eccentricity is pumped past 0.95
within ~30 kyr, dropping periastron below 0.08 AU and crashing toward the star
over ~10⁵ yr (tidal disruption); (2) of Beichman's four proposed orbit families,
**two survive** 10⁵ yr (both retrograde, bounded but hot at e_max≈0.83); both
prograde families (~50°, a≈1.6 and a≈2.1 AU) disrupt; (3) the
**habitable-zone-stable region** is a≈1.4–1.75 AU with mutual inclination ≲35°
and eccentricity ≲0.18, asymmetric about 90° (octupole EKL); (4) the *Avatar*
canon distance of 1.2 AU is **interior to α Cen A's habitable zone** —
dynamically stable (e_max≈0.14) but too warm, not a stability failure;
and (5) on a stability-selected orbit (a=1.6 AU, e=0.1, mutual
i≈16° — the median of the stable range), Polyphemus stays in the HZ over 10⁵ yr
and a **0.45 M⊕ Pandora-mass moon is Hill-stable** at 225,000 km. The complete
α Cen A → Polyphemus → Pandora hierarchy (perturbed by α Cen B) is dynamically
viable — just not on the favored *observed* orbit.

---

## 1. Background

α Cen A b ("S1") was reported by Beichman et al. 2025 (*Worlds Next Door I*,
arXiv:2508.03814) + Sanghi & Beichman 2025 (*II*, arXiv:2508.03812): a single
JWST/MIRI F1550C (15.5 µm, 3.5±1.0 mJy, S/N 4–6) detection in Aug 2024 at 1.5″
(~2 AU) from α Cen A, not recovered in two 2025 epochs (~52% of stable orbits
are consistent with non-recovery via orbital motion). It is linked to the 2019
VLT/NEAR candidate C1 (Wagner et al. 2021). Inferred properties: Saturn-class
(90–150 M⊕), ~1–1.1 R_Jup, T_eq≈225 K, eccentric (e≈0.4) on one of four
dynamically-stable orbit families spanning P=2–3 yr and mutual inclination
≈50° (prograde) / ≈130° (retrograde) to the α Cen AB binary plane.

The popular and scientific press immediately connected this to *Avatar*: NPR
(2025-08-07) and Live Science called it "a real-life Pandora," and Sellers et
al.'s *Seeking the Worlds of Avatar* (Astrobiology, 2025) assessed the
prospects for detecting HZ moons of exactly this giant. In *Avatar* canon,
**Polyphemus** is a Saturn-class gas giant orbiting α Cen A in its HZ with 14
moons; the fifth, **Pandora**, is the habitable Na'vi homeworld (~0.45 M⊕,
~0.75 R⊕, 0.8 g, dense N₂/O₂/CO₂ atmosphere, ~27 h tidally-locked day, 29°
axial tilt). This study asks the underlying real-science question: **can such a
system be dynamically stable, and on what orbit?**

---

## 2. Methods and tools

### 2.1 Integrator stack (REBOUND 5.0)

| Integrator | Role | Notes |
|---|---|---|
| **WHFast** | fast first-pass screen | 2nd-order symplectic Wisdom-Holman; bounded energy error for near-Keplerian orbits; supports MEGNO. dt = P_innermost/50. |
| **TRACE** (Lu, Hernandez & Rein 2024) | accurate re-verification | time-reversible hybrid (symplectic far / Bulirsch-Stoer in close encounters); ≈IAS15 accuracy at large speed-up; handles central-star approaches WHFast can't. **No variational equations → no MEGNO.** |
| **IAS15** | gold-standard spot-check | 15th-order adaptive; supports MEGNO; slow. |

Selectable via `run.py --integrator {whfast,trace,ias15}` (added this session).
**Policy:** WHFast screens all systems (gives the MEGNO chaos flag); any system
it flags chaotic/unstable is re-verified with TRACE, whose accurate a/e is the
canonical result. This matters because WHFast over-reports instability in
close-encounter regimes (see §3, AU Mic). **Exception — α Cen:** here the
perturbation is *secular* (Kozai-Lidov forcing from the massive, eccentric, far
companion B at 23.5 AU), not a close encounter. TRACE is built for the latter
and is inaccurate on this problem — at the observed e=0.4/i=50° orbit it shows
|ΔE/E|≈3.6×10⁻³ and a spurious semi-major-axis drift (a swinging 0.81–2.05 AU),
while IAS15 holds a essentially fixed at |ΔE/E|≈1×10⁻¹³ with MEGNO≈2. **The
canonical α Cen results below are therefore IAS15, not TRACE.** (Earlier α Cen
runs in this session used TRACE and were additionally corrupted by a dt bug — the
innermost-period computation used the default barycentric semi-major axis 3.75 AU
instead of the A-relative 1.6 AU, making dt 3.6× too large; fixed this session.)

### 2.2 Three diagnostics (independent axes)

- **a/e-drift bounds** — the actual *outcome*: did a body eject (a balloons,
  >10× excursion) or its orbit go unbound (e_max ≥ 0.9)? This is the pass/fail.
- **MEGNO** (Mean Exponential Growth of Nearby Orbits; Cincotta & Simó 2000) —
  the *chaos early-warning*: ⟨Y⟩→2 regular, growing = chaotic; Lyapunov time ≈
  2·T/(MEGNO−2). Chaos ≠ instability (TRAPPIST-1 is chaotic but bounded for Gyr).
  Unavailable under TRACE.
- **Eccentricity tier** (`ecc_class`, added this session): calm (e_max<0.3),
  hot (0.3–0.9), extreme (≥0.9). A separate axis so "stable" (survives) is not
  conflated with "calm" (low-e).

### 2.3 Moon / Hill-sphere handling

Hypothetical moons (`hypotheticals/<system>.json`) are integrated as full
hierarchy members. Hill radius r_H = a(m/3M)^(1/3); a moon is flagged unbound
if a_moon > r_H and warned above 0.5 r_H (Domingos et al. 2006 prograde limit).
**Fix this session:** moons are now placed relative to their *parent's orbital
plane*, not the sim reference frame — essential for α Cen, whose planet orbit
sits ~79° from the reference (the AB plane); an inclination_deg=0 moon was
otherwise spuriously Kozai-pumped to e→0.97.

### 2.4 Pipeline

`db/systems/<star>.json` (Phase 2 measurements) → `load.py` builds the REBOUND
`Simulation` (star μ→mass; recommended orbital + physical; Kepler back-out of a
from period when no semi-major axis is curated) → `run.py` integrates, scores,
writes `results/<system>_{summary.json,timeseries.csv}`. The α Cen A b orbit is
parameterized via `--acen-a-au / --acen-e / --acen-incl-deg` for the scans below.

---

## 3. The 12-system survey (10⁴ yr)

All NearStars Phase 3 multi-planet systems were screened. Verdicts (canonical
integrator in brackets):

- **Regular stable** (MEGNO≈2): Proxima Cen (b/c/d), 55 Cnc, 61 Vir, HD 219134,
  HD 69830, τ Cet, Teegarden's Star [whfast].
- **Chaotic but bounded** (high MEGNO, no ejection): TRAPPIST-1 (1265), Barnard
  (248), YZ Cet (8.0) [TRACE-verified].
- **Unstable**: only α Cen A b's favored orbit (below).

**AU Mic — why the hybrid policy.** WHFast flagged AU Mic UNSTABLE (planet d
ejected to ~7 AU, e→0.99). Under TRACE, d is bounded (a 0.09–0.35 AU, e≤0.63):
the ejection was a close-encounter **artifact**. The system is dynamically hot
(orbits cross) but survives 10⁴ yr. TRACE on a quiet system (HD 219134) is
byte-identical to WHFast — no spurious drift. (Candidate AU Mic d/e have
period-only data; a is Kepler-derived.)

---

## 4. α Cen A b dynamics

All runs at a=1.6 AU (the observed favored semi-major axis) unless noted;
**IAS15** (the secular forcing here makes TRACE inaccurate — see §2.1), 10⁵ yr;
mutual inclination is measured to the α Cen AB plane; HZ taken as 1.18–2.05 AU
(conservative; α Cen A L=1.521 L☉, EEID 1.23 AU). Periastron q and apastron Q
are read from the timeseries; "disrupts" = e first exceeds 0.95 (near-radial,
periastron then collapsing toward the star).

### 4.1 The observed orbit is Kozai-Lidov unstable

At the favored e≈0.4, mutual i≈50°, eccentric Kozai-Lidov (octupole, driven by
the e_B=0.52 companion) pumps the planet's eccentricity past **0.95 within
~30 kyr** (IAS15; the first big EKL spike), dropping periastron below **0.08 AU**.
Over the following Kozai cycles e climbs toward unity (the audit's IAS15 run
reaches ~0.9997 by ~10⁵ yr), at which point periastron falls below α Cen A's
radius (0.0057 AU) — tidal disruption. So the disruption timescale is **~10⁴–10⁵
yr, not "a few kyr"** (the earlier "e→0.998 within a few kyr" was a TRACE +
dt-bug artifact). The AB binary itself is unaffected.

### 4.2 Orbit-family scan — 2 of Beichman's 4 survive

| Family | a, i_mut | e_max | verdict |
|---|---|---|---|
| prograde, a<2 (favored) | 1.6 AU, ~50° | disrupts (~32 kyr) | **UNSTABLE** |
| retrograde, a<2 | 1.6 AU, ~120° | 0.83 | stable (hot) |
| prograde, a>2 | 2.1 AU, ~50° | disrupts (~20 kyr) | **UNSTABLE** |
| retrograde, a>2 | 2.1 AU, ~120° | 0.84 | stable (hot) |

So "α Cen A b is unstable" is too blunt, but the corrected (IAS15) picture is
sharper than the earlier TRACE pass: **both prograde families (~50°) disrupt —
not just the favored inner one** — while **both retrograde families (~120°)
survive**, bounded but hot (e~0.83). Survival is conditional on retrograde
geometry, the textbook prograde/retrograde octupole asymmetry. (The earlier TRACE
run wrongly kept the wide prograde family "stable, marginal"; IAS15 disrupts it.)

### 4.3 Mutual-inclination sweep — the stable band

Sweeping i_mut at a=1.6, e=0.4 (IAS15, 10⁵ yr): stable at i ≲ 45° (prograde) and
≳ 115° (retrograde); the ~45–110° band is Kozai-unstable, peaking at i=90° (orbit
flip — disrupts in ~1.3 kyr). The band is **asymmetric about 90°** — the
retrograde side survives even at high e_max (0.55–0.88, bounded), the textbook
octupole asymmetry. The prograde cliff at ~45° sits just *above* the 39.2°
quadrupole Kozai threshold, as theory expects (the earlier TRACE pass put it at
~30°, *below* threshold — a now-corrected artifact). Even coplanar (i=0) the
planet is hot (e_max 0.48) — the massive eccentric companion stirs it at all
inclinations.

### 4.4 Habitable-zone-stable region

Requiring the orbit to stay entirely within the HZ (q≥1.18, Q≤2.05) over 10⁵ yr
(IAS15): **a ≈ 1.40–1.75 AU, e_init ≲ 0.18, i_mut ≲ 35°.** The inner edge is
*geometric*, not dynamical — at e=0.1 the periastron a(1−e_max) clears the inner
HZ (1.18 AU) only for a≳1.40 (a=1.38 → q 1.169; a=1.40 → q 1.187). Orbits interior
to that (a=1.2–1.3) are **dynamically stable** (e_max≈0.14, MEGNO 2.0) — they are
simply *inside* α Cen A's HZ (too warm), not destabilized. (The earlier claim of
a secular resonance pumping e→0.6–0.7 at 1.2–1.3 AU was a TRACE + dt-bug artifact;
IAS15 finds no such pump.) The outer HZ edge (apastron ≤ 2.05) is crossed near
a≈1.75. a=1.6 sits comfortably central.

### 4.5 The boundary toward the observed orbit

How close to observed (e=0.4, i=50°) can one get while remaining stable (IAS15)?
- **Stay in the HZ**: up to **e≈0.18, i≈35°** (at a=1.6; beyond these the
  periastron drops below the inner HZ edge or Kozai kicks in).
- **Survive (eccentric, may leave HZ)**: at the observed **e=0.4 the prograde
  cliff is ~45°** — i=40° stays bounded (e_max 0.54), i=50° disrupts (~32 kyr).
  At the adopted low e=0.1, survival extends slightly further (i=45° bounded at
  e_max 0.77; i=50° disrupts ~55 kyr).
The observed e=0.4/i=50° orbit sits just past the ~45° prograde Kozai cliff.

### 4.6 Adopted orbit — median of the stable range

Taking the median of the HZ-stable ranges at a=1.6 (e: 0–0.18 → **0.1**;
i_mut: 0–35° → **16°**): verified HZ-stable over 10⁵ yr (IAS15, MEGNO 2.000,
e_max 0.157, orbit 1.345–1.854 AU). This is the orbit now in the DB (recommended)
and the Phase 3
report; the observed e≈0.4/i≈50° is retained as a `recommended:false`,
Kozai-unstable canonical alternative.

### 4.7 Pandora moon — Hill-stable

Pandora's ~27 h tidally-locked day → orbital period → Kepler back-out gives
**a_moon = 225,000 km** around the 120 M⊕ Polyphemus (Polyphemus spans ~36° of
Pandora's sky — the films' skyline). With the dt fix, the integrator now resolves
the moon's 1.12-day (≈27 h) orbit — dt = 0.022 d, |ΔE/E| = 3.6×10⁻¹⁰ (TRACE; the
earlier buggy dt of 50 d left the moon orbit wholly unresolved). At the adopted
orbit, the full hierarchy (α Cen A + Polyphemus + Pandora + α Cen B) gives:
Pandora a constant (Δa/a ≈ 1×10⁻⁵), **e ≈ 0 (max ~1×10⁻⁴), Hill fraction 0.02,
bound** — deep inside the 0.5 r_H limit. A habitable Pandora-class moon is
dynamically viable.

---

## 5. Tooling built/extended this session

- `run.py --integrator {whfast,trace,ias15}` — integrator selection; MEGNO
  gated off under TRACE with an a/e-drift verdict fallback.
- **dt-bug fix in `configure_integrator`** (audit follow-up): the innermost
  period now uses each body's semi-major axis *relative to its true primary*
  (star A for planets/companion, the parent planet for moons) rather than the
  default Jacobi `p.a`, which for the α Cen planet returned the A+B barycentric
  3.75 AU (dt 3.6× too large) and for the moon returned ~1.6 AU (the 1.12-day
  moon orbit left wholly unresolved). All α Cen boundary numbers were re-derived
  with IAS15 after the fix (`acen_boundary_scan.py`).
- Eccentricity tier (`ecc_class` calm/hot/extreme) in the verdict + report.
- Registry extended from 3 to 12 systems (generic planetary loader).
- `load.py` fixes: (a) `physical` may be a single dict not just a list; (b)
  Kepler back-out of a from period when semi-major axis is uncurated (AU Mic
  d/e); (c) hypothetical moons placed relative to the parent orbital plane;
  (d) α Cen A b orbit parameterization (`--acen-*`).
- `hypotheticals/alpha_centauri.json` — the Pandora moon test.
- `check-mirrors.sh` reverse-pass — catches stale/orphan ko mirrors outside
  docs/plans (it caught two stale STABILITY_REPORT ko mirrors this session).

---

## 6. Reproducibility

```bash
# Planet runs use IAS15 (secular forcing; TRACE inaccurate here — see §2.1)
.venv/bin/python phase3/stability-sim/scripts/run.py --system alpha_centauri --integrator ias15 --years 100000 \
    --acen-a-au 1.6 --acen-e 0.4 --acen-incl-deg 50    # observed: UNSTABLE (e>0.95 by ~30 kyr)
.venv/bin/python phase3/stability-sim/scripts/run.py --system alpha_centauri --integrator ias15 --years 100000 \
    --acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16    # adopted: HZ-stable (MEGNO 2.0, e_max 0.16)
# Full boundary re-derivation (inner/outer edge, e/i bounds, canon 1.2, families)
.venv/bin/python phase3/stability-sim/scripts/acen_boundary_scan.py
# Pandora moon (full hierarchy) — TRACE handles the close planet-moon pair; the
# moon's clean Keplerian sub-orbit doesn't need IAS15 (the IAS15 rule is for the
# planet's secular high-e evolution, not the deeply Hill-bound moon).
.venv/bin/python phase3/stability-sim/scripts/run.py --system alpha_centauri --integrator trace --years 100 \
    --acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16 \
    --hypotheticals phase3/stability-sim/hypotheticals/alpha_centauri.json
```

Key commits (this session, on `main`): integrator option, results policy,
eccentricity tier, α Cen A b Kozai + parameterization + inclination sweep,
moon-frame fix + Pandora test, DB HZ orbit, Phase 3 cultural context. See
`git log --grep stability-sim` and `--grep Polyphemus`.

---

## 7. Caveats and limitations

1. **Point-mass, no tides.** Tidal damping (absent here) would circularize a
   high-e/inclined orbit rather than always disrupt it — so the unstable
   families might instead tidally settle at small a. A real Pandora's habitability
   also depends on tidal heating, not modeled.
2. **10⁴–10⁵ yr horizon** — short vs Gyr ages; MEGNO and the resonance scan
   mitigate but do not replace a SPOCK-style long-term probability.
3. **Candidate, weak constraints.** α Cen A b is an unconfirmed single-roll
   detection; its orbit is two imaging points + dynamical families. The adopted
   e/i are a stability-informed *choice* within the allowed range, not a
   measurement — a documented divergence from the observed favored orbit.
4. **cfg-frame inclination** of the mutual 16° is an open item.
5. **Pandora is fiction.** It is modeled only as a hypothetical-moon viability
   test, not added to the real-planet DB.

## References

- Beichman et al. 2025, *Worlds Next Door I*, ApJL (arXiv:2508.03814);
  Sanghi & Beichman 2025, *II* (arXiv:2508.03812)
- Wagner et al. 2021 (VLT/NEAR C1); Zhao et al. 2018 (α Cen RV limits)
- Lu, Hernandez & Rein 2024, TRACE (arXiv:2405.03800); Rein & Liu 2012 (REBOUND)
- Cincotta & Simó 2000 (MEGNO); Domingos et al. 2006 (moon stability limit)
- Naoz 2016 (eccentric Kozai-Lidov review)
- *Seeking the Worlds of Avatar*, Astrobiology 2025; NPR 2025-08-07
- Avatar canon: Pandorapedia / Avatar Wiki (Polyphemus, Pandora)

## Related

- [STABILITY_REPORT](STABILITY_REPORT.md) — the 12-system verdict tables + α Cen sweep
- [alpha-centauri-a-b](../../docs/phase3/alpha-centauri-a-b.md) — the Phase 3 synthesis (cfg-ready) this feeds
- [scripts/run.py](scripts/run.py), [scripts/load.py](scripts/load.py) — the sim
