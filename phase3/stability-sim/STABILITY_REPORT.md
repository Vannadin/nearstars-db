# Phase 3 Stability Report — 10,000 yr N-body Integration

**Generated:** 2026-06-07
**Integrator policy:** REBOUND 5.0 **WHFast + MEGNO** as the fast first-pass
screen; **TRACE** (Lu, Hernandez & Rein 2024) re-verification for any system
WHFast flags chaotic or unstable. **IAS15** for spot-checks — and as the
*canonical* integrator for α Cen, whose forcing is secular (a far, massive,
eccentric companion) rather than close-encounter, where TRACE is inaccurate.
**Horizon:** 10,000 yr (Principia play window).
**Phase initialisation:** `raw.omega_deg` from DB where available; Ω and M
randomised with a deterministic seed (`phase_seed=0`).

## Three diagnostics — survival, chaos, eccentricity

The verdict separates *what actually happened* from *chaos risk* from *how
eccentric the orbit got* — three distinct axes, read together:

- **a/e-drift bounds** (per-body a_min/a_max, e_min/e_max) — the **actual
  outcome**: did a body eject (a balloons) or its orbit go unbound/crossing
  (e → 1)? This is the **final pass/fail** for shipping a system (the
  game-relevant question is "does a planet escape or collide"). Thresholds:
  `e_max ≥ 0.9` or `a_max/a_min ≥ 10×` → unstable. Its accuracy depends on
  the integrator.
- **MEGNO** — the **chaos early-warning**: time-averaged divergence of nearby
  orbits. ⟨Y⟩ → 2 = regular; growing = chaotic. Flags long-term sensitivity
  *before* any large excursion, but **chaos ≠ instability** (a chaotic system
  can stay bounded for Gyr — e.g. TRAPPIST-1). Needs variational equations, so
  it is **unavailable under TRACE**.
- **Eccentricity tier** (`ecc_class`, from e_max) — *how* eccentric the orbit
  becomes, a separate axis from survival: **calm** (e_max < 0.3,
  Solar-System-like), **hot** (0.3–0.9, bound but violently eccentric — extreme
  seasons, deep periastron passes), **extreme** (≥ 0.9 = the near-unbound /
  disruption threshold, which is also the `unstable` cut). **Key point:
  "stable" only means e stayed below 0.9 — it does NOT mean calm.** A planet
  can be "stable" yet on an e ≈ 0.8 orbit (α Cen A b's surviving families, or
  AU Mic).

**Why the hybrid policy:** WHFast is fast and gives MEGNO, but it is
inaccurate during close encounters — it can report a *spurious* ejection
(see AU Mic). TRACE integrates close encounters accurately (≈IAS15) but has
no MEGNO. So WHFast supplies the chaos flag and TRACE supplies the
trustworthy a/e outcome for the flagged systems; the canonical result for a
flagged system uses TRACE, with its WHFast MEGNO carried in the table below.
**The exception is α Cen**, where the perturbation is *secular* (the far,
massive, eccentric companion B) not a close encounter — TRACE is built for the
latter and is inaccurate here (|ΔE/E| ≈ 3.6×10⁻³, with a spurious semi-major-axis
drift), so the canonical α Cen integrator is **IAS15** (|ΔE/E| ≈ 1×10⁻¹³,
MEGNO ≈ 2). It is adaptive, so it also sidesteps the fixed-step dt that a
companion-corrupted Jacobi `p.a` got wrong before this was caught.

## Verdict summary (12 systems)

`MEGNO` is the WHFast screen value (chaos indicator). `e_max` / `Δa/a` are
from the canonical integrator in the last column.

| System | Bodies | MEGNO (WHFast) | e_max (tier) | max Δa/a | verdict | canonical |
|---|---|---|---|---|---|---|
| Proxima Cen | 3 (b/c/d) | 2.000 | <0.001 · calm | 8×10⁻⁴ | **stable (regular)** | whfast |
| 55 Cnc | 5 | 1.961 | 0.12 · calm | 3.3×10⁻² | **stable (regular)** | whfast |
| 61 Vir | 3 | 1.962 | **0.39 · hot** | 1.1×10⁻³ | **stable (regular)** | whfast |
| HD 219134 | 6 | 2.000 | 0.068 · calm | 2.8×10⁻³ | **stable (regular)** | whfast |
| HD 69830 | 3 | 1.998 | 0.20 · calm | 7.8×10⁻⁴ | **stable (regular)** | whfast |
| tau Cet | 4 | 2.001 | 0.24 · calm | 3.6×10⁻⁴ | **stable (regular)** | whfast |
| Teegarden's Star | 3 | 2.000 | 0.091 · calm | 6.1×10⁻⁴ | **stable (regular)** | whfast |
| TRAPPIST-1 | 7 | 1265 | 0.021 · calm | 5.9×10⁻³ | **chaotic, bounded** | TRACE |
| Barnard's Star | 4 | 248 | 0.106 · calm | 8.3×10⁻⁴ | **chaotic, bounded** | TRACE |
| YZ Cet | 3 | 8.024 | 0.103 · calm | 2.0×10⁻³ | **chaotic, bounded** | TRACE |
| AU Mic | 4 | 6249 | **0.63 · hot** | 3.5 (b's a triples) | **chaotic, hot but bounded** | TRACE |
| α Cen A b (in AB binary) | planet + 2 stars | n/a (disrupts) | **>0.95 · extreme** | disrupts ~30 kyr | **UNSTABLE** in both prograde families (2 of 4 stable) | ias15 |

Eleven of the twelve are stable or chaotic-but-bounded under the accurate
integrator: seven regular (MEGNO ≈ 2), three formally chaotic but tightly
bounded (TRAPPIST-1, Barnard, YZ Cet — tight inner M-dwarf chains, consistent
with the literature), and AU Mic dynamically hot but bounded. The only
instability is the S-type candidate **α Cen A b** in its *favored* prograde
inner family (e → 0.95+ by Kozai-Lidov at i_mut ≈ 50°) — and a sweep shows 2 of
its 4 proposed orbit families survive (both retrograde; below). The α Cen AB
binary itself is stable (B: e = 0.514–0.519, a-drift < 0.6%).

On the **eccentricity** axis (last-column tier), most survivors are *calm*
(e_max < 0.3, Solar-System-like), but **61 Vir (0.39) and AU Mic (0.63) are
*hot*** — bound but on notably eccentric orbits. So "stable" in the verdict
column is not the same as "calm": a system can pass the survival test while
still being eccentrically stirred (most extreme: α Cen A b's surviving
families at e ≈ 0.79–0.88, in the α Cen section below).

## AU Mic — the case that justifies the hybrid policy

WHFast and TRACE *disagree* on AU Mic, and TRACE is right:

| integrator | AU Mic d | verdict |
|---|---|---|
| WHFast | a → **7.09 AU** (Δa/a = 84×), e → **0.99** | **unstable (ejection)** |
| TRACE | a ∈ [0.089, **0.354**] AU, e ≤ **0.63** | **stable (bounded)** |

WHFast's "ejection to 7 AU" is a **close-encounter artifact** — the 4-planet
candidate config produces orbit crossings that WHFast cannot integrate
accurately, so it flings d out. TRACE (accurate through close encounters)
shows the system is **dynamically hot** — b's a triples, eccentricities reach
~0.6, orbits cross — but **no body actually ejects** in 10⁴ yr. MEGNO = 6249
(Lyapunov ≈ 3.2 yr) correctly diagnosed strong chaos; the chaos is real, the
ejection was not.

**Caveat on AU Mic:** planets d (P = 12.74 d) and e (P = 33.11 d) are
**unconfirmed TTV candidates** with no curated semi-major axis — a is derived
from the measured period via Kepler III. The system is ~22 Myr old and the
candidate masses are uncertain. So this flags *the candidate 4-planet
configuration* as marginal/chaotic, not a confirmed instability. The orbit
crossings mean longer-baseline (10⁶ yr) or Monte-Carlo-over-mass follow-up
would refine it.

## α Centauri A b — Kozai-Lidov unstable only in the favored prograde family

The binary loader now injects the S-type candidate **α Cen A b** (a ≈ 1.6 AU,
e ≈ 0.4, m ≈ 120 M⊕) around star A, placed at the same node as B so its mutual
inclination to the AB plane is **50°** by default (Beichman 2025, prograde) —
inside the Kozai-Lidov window (39.2°–140.8°). Integrated with **IAS15** (the
forcing is secular from the far companion, not a close encounter, so TRACE is
inaccurate here — see the policy note above).

At the favored value the planet is **dynamically unstable**: the eccentric
companion drives **eccentric Kozai-Lidov (octupole)** oscillations that pump
its eccentricity **past 0.95 within ~30 kyr** (the first big EKL spike),
dropping periastron a(1−e) below **0.08 AU**; over the following Kozai cycles e
climbs toward unity and periastron falls below α Cen A's radius (0.0057 AU) →
tidal disruption on a **~10⁴–10⁵ yr** timescale. (An earlier TRACE pass, also
hurt by a since-fixed dt bug, wrongly read this as "e → 0.998 within a few
thousand years.") The AB binary itself is unaffected (B: a 23.57–23.70 AU, e
0.514–0.519). But this is **inclination-dependent**, so the loader takes
`--acen-incl-deg` (and `--acen-a-au` / `--acen-e`) for the Beichman orbit
families and a mutual-inclination sweep.

### Mutual-inclination sweep (a = 1.6 AU, e = 0.4, IAS15, 10⁵ yr)

| i_mut | e_max | verdict | | i_mut | e_max | verdict |
|---|---|---|---|---|---|---|
| 0° (coplanar) | 0.48 | stable (hot) | | 90° | 0.99 (flip) | **unstable** (~1.3 kyr) |
| 20° | 0.49 | stable (hot) | | 110° | 0.93 | **unstable** |
| 35° | 0.53 | stable (hot) | | 115° | 0.89 | stable (hot) |
| 40° | 0.54 | stable (hot) | | 130° | 0.68 | stable (hot) |
| 50° | 0.95 | **unstable** (~32 kyr) | | 145° | 0.55 | stable (hot) |
| 65° | 0.86 | stable (hot) | | 160° | 0.57 | stable (hot) |

**Stable inclination band: i_mut ≲ 45° (prograde) or ≳ 115° (retrograde); the
~45°–110° band is Kozai-unstable, peaking at 90° (orbit flip — disrupts in
~1.3 kyr).** The band is **asymmetric about 90°** — the retrograde side survives
even at high e_max (0.55–0.89, bounded), the textbook prograde/retrograde
octupole asymmetry. The prograde cliff sits at ~45°, just *above* the 39.2°
quadrupole Kozai threshold, as theory expects. (An earlier TRACE pass put it at
~30°, below threshold — a now-corrected dt-bug + integrator artifact.) Note that
even coplanar the planet is *hot* (e_max 0.48) — the massive eccentric companion
keeps it stirred at all inclinations.

### Beichman's four proposed orbit families — 2 of 4 survive

| Family | a, i_mut | e_max | verdict |
|---|---|---|---|
| prograde, a<2 (**favored**) | 1.6 AU, ~50° | disrupts (~32 kyr) | **UNSTABLE** |
| retrograde, a<2 | 1.6 AU, ~120° | 0.83 | stable (hot) |
| prograde, a>2 | 2.1 AU, ~50° | disrupts (~20 kyr) | **UNSTABLE** |
| retrograde, a>2 | 2.1 AU, ~120° | 0.84 | stable (hot) |

So the accurate statement is **not** "α Cen A b is unstable" but, sharpened by
IAS15: **both prograde families (~50°, a ≈ 1.6 and 2.1 AU) are Kozai-unstable,
while both retrograde families (~120°) keep the planet bounded (hot, e ≈ 0.83)
over 10⁵ yr.** If α Cen A b is real, its survival hinges on retrograde geometry.
(The earlier TRACE pass wrongly kept the wide prograde family marginally stable;
IAS15 disrupts it, so 2 survive, not 3.)

**Follow-up:** tidal damping (absent from the point-mass sim) would set where a
high-e/inclined orbit circularizes rather than disrupts, and a finer grid near
the 45° and 112° boundaries would sharpen the stable band.

### Polyphemus & Pandora (Avatar) — a HZ-stable orbit that hosts a moon

α Cen A b is the real-life candidate for **Polyphemus**, the *Avatar* gas giant
whose moon **Pandora** is the Na'vi homeworld (Beichman 2025 / NPR 2025 /
*Seeking the Worlds of Avatar*, Astrobiology 2025). Asking whether a habitable
Pandora could actually survive here drove a fine-tuning scan:

- **The Avatar canon distance (1.2 AU) is interior to the HZ** — at 1.2 AU the
  orbit is *dynamically* stable (e_max ≈ 0.14, MEGNO 2.0) but its periastron
  (~1.03 AU) sits inside α Cen A's conservative inner HZ edge (1.18 AU): too
  warm, not a stability failure. (An earlier TRACE pass mis-reported a secular
  resonance pumping e → 0.64 here; IAS15 finds no such pump.)
- **The HZ-stable zone is a ≈ 1.40–1.75 AU.** The DB/Phase-3 orbit takes the
  median of the stable range — e 0–0.18 → **e = 0.1**, mutual inclination
  0–35° → **≈ 16°** — at a = 1.6 AU (the observed semi-major axis): HZ-stable
  over 10⁵ yr (IAS15, MEGNO 2.000, orbit 1.345–1.854 AU, e_max 0.157).
- **Pandora is Hill-stable.** A 0.45 M⊕ moon at 225 000 km (Kepler back-out of
  Pandora's ~27 h tidally-locked day; Polyphemus spans ~36° of its sky) sits at
  ~0.02 R_Hill on a near-circular orbit (e ≈ 0, bound) — deep inside the
  Domingos+2006 limit. With the dt fix the moon's 1.12-day orbit is now properly
  resolved (dt 0.022 d, |ΔE/E| 3.6×10⁻¹⁰; the old dt of 50 d left it unresolved).
  The full Avatar hierarchy (α Cen A → Polyphemus → Pandora, perturbed by α Cen
  B) is dynamically viable on the stability-selected orbit, though not on the
  Kozai-unstable observed one. Test: `hypotheticals/alpha_centauri.json`, run
  with `--acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16` (moon: `--integrator
  trace`; planet boundaries: `--integrator ias15`).

## Barnard's Star — Msini → true-mass dynamical bound (coplanar inclination scan)

All four Barnard planets (d, b, c, e; 0.0188–0.0381 AU, sub-Earth) are RV
detections, so the DB masses are minima M·sin i. The true mass is M = M·sin i / sin i;
assuming the system is **coplanar** (one shared inclination i), lowering i scales every
planet's mass by 1/sin(i), strengthening the mutual perturbations. Walking i down finds
the inclination — equivalently the true-mass multiplier — at which the packed chain can
no longer survive the 10⁴-yr window. (`scripts/barnard_inclination_scan.py`,
phase_seed=0.)

| i (coplanar) | mass ×1/sin i | heaviest planet | e_max | TRACE outcome |
|---|---|---|---|---|
| 90° (nominal) | ×1.00 | 0.34 M⊕ | 0.11 | survives |
| 30° | ×2.00 | 0.67 M⊕ | 0.11 | survives |
| 20° | ×2.92 | 0.98 M⊕ | 0.11 | survives |
| **19° (boundary)** | **≈×3.1** | **≈1.0 M⊕** | — | **threshold** |
| 18° | ×3.24 | 1.08 M⊕ | 1.06 | **disrupts (b @ 5775 yr)** |
| ≤15° | ≥×3.9 | ≥1.3 M⊕ | →1 | disrupts faster |

**Result: i_crit ≈ 19° (bracket 18–20°).** The system is stable for true masses up to
≈3× the minimum (heaviest planet ≲ 1 M⊕); only a near-face-on geometry destabilizes it.
For randomly oriented orbits the prior probability of i < 19° is 1 − cos 19° ≈ **5.5 %**,
so dynamics exclude only ~5 % of orientations — a real but weak bound that **does not
exclude the nominal (edge-on) system**. The nominal verdict stands: chaotic
(Lyapunov ≈ 81 yr) but Hill-stable.

**Literature cross-check.** Both discovery papers ran their own stability analysis
(SPOCK + REBOUND, 10⁹ orbits of the 2.34 d planet) and reached the same ×3 ceiling:
González Hernández et al. 2024 state the m = 3·M·sin i case "would mean an orbital
inclination of i = 19.5°… in both cases [1× and 3×] the result is the same," and Basant
et al. 2025 find the four-planet system "stable for planet masses up to three times the
[Table-3] values… inclinations ranging from 20 to 90 degrees." Our i_crit ≈ 19° / ×3 from
a 10⁴-yr WHFast→TRACE screen reproduces their ~19.5–20° / ×3 from a 6-Myr ML-classifier
ensemble — an independent cross-validation in the spirit of the TRAPPIST-1 vs Agol+2021
check. Caveat: Basant warns stability is strongly eccentricity-sensitive (< 80 % stable
if any planet has e > 0.02); this scan adopts the DB's β-prior eccentricities
(0.03–0.08), so the exact boundary is conditional on that choice — the papers favor
e < 0.02.

**Methodology note — WHFast artifact caught by TRACE.** The WHFast first-pass screen
reported i=20° disrupting (Barnard b ejecting @ 8475 yr, e_max 0.96). TRACE re-verifies
i=20° as *stable* (e_max 0.11): the WHFast "ejection" was a spurious fixed-step
close-encounter artifact (the AU Mic failure mode). The boundary above is the TRACE
result. This is exactly why the suite's policy re-verifies every WHFast-flagged case.
Caveat: single phase realization (seed=0); a multi-seed survival-fraction refinement
near i_crit would sharpen the ~1° bracket, which sits at the precision floor of a
single-seed chaotic scan.

## Hypothetical moons — demonstration

The sim also resolves moons (extra bodies via `hypotheticals/<system>.json`).
With `hypotheticals/trappist_1.json` containing two test moons:

| Moon | Parent | a (km) | Hill frac | Outcome |
|------|--------|--------|-----------|---------|
| TRAPPIST-1 e moon (safe) | e | 20,000 | 0.23 | bound, stable |
| TRAPPIST-1 g moon (risky) | g | 110,000 | 0.64 → ∞ | **ejected within 1000 yr**, e → 358,283 |

The risky moon at 0.64 R_Hill exceeds the Domingos et al. 2006 prograde
stability limit (~0.5 R_Hill) and is ejected; its escape also perturbs
TRAPPIST-1 g (e_max grows from 0.013 to 0.028) — a small but real cascade
visible in the integration. This confirms the tool resolves the **full
star–planets–moons hierarchy** in one N-body sim: stellar tide on the moon,
mutual planet perturbations, and the moon's gravity back on its parent are all
tracked. (A deliberately-unstable demo; output in `results/with_moons/`.)

## Solar System — validation against secular theory

A `solar_system` run (8 planets at J2000 elements + masses, Earth+Moon merged;
WHFast, dt = P_Mercury/50, 1 Myr) calibrates the tool against the real, known
secular dynamics. Verified 2026-06-15.

- **Integrator fidelity:** ΔE/E = 1.2×10⁻⁹, MEGNO = 1.995 (regular).
- **Eccentricity:** the simulated secular ranges bracket every planet's present-day
  e and match Laskar/Milankovitch amplitudes — Earth 0.001–0.053 (Milankovitch
  ≈ 0.003–0.058) and Jupiter 0.024–0.061 (Laskar ≈ 0.025–0.061) are essentially
  exact; all eight bracket the J2000 value. Inclinations show the expected small,
  bounded oscillations.
- **Semi-major axes:** stable, no secular drift. The giants' apparent ~1% osculating
  spread is a heliocentric-element artifact — the Sun's barycentric wobble from
  Jupiter (~0.005 AU) aliased at the 5000-yr snapshot cadence — not real drift;
  energy conservation to 1e-9 confirms it.

**Scope.** Faithful for ~Myr secular (Milankovitch) behaviour. It does NOT reproduce
the real Solar System's weak chaos (Lyapunov ≈ 5 Myr): the 1 Myr run is shorter than
that and omits general relativity and lunar dynamics (Earth+Moon are a single point
mass), which drive Mercury's long-term chaotic diffusion.

## How to use

```bash
# Fast first-pass screen (WHFast + MEGNO)
.venv/bin/python phase3/stability-sim/scripts/run.py --system trappist_1 --years 10000

# Accurate re-verification of a flagged system (close encounters / high-e)
.venv/bin/python phase3/stability-sim/scripts/run.py --system au_mic --integrator trace

# Gold-standard spot-check (adaptive high-order, + MEGNO, slow)
.venv/bin/python phase3/stability-sim/scripts/run.py --system au_mic --integrator ias15

# alpha Cen — canonical IAS15 (secular forcing; TRACE inaccurate here)
.venv/bin/python phase3/stability-sim/scripts/run.py --system alpha_centauri \
    --integrator ias15 --years 100000 --acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16

# alpha Cen — full boundary re-derivation (inner/outer edge, e/i bounds, families)
.venv/bin/python phase3/stability-sim/scripts/acen_boundary_scan.py

# Barnard — Msini->true-mass coplanar inclination boundary (TRACE re-verify the WHFast screen)
.venv/bin/python phase3/stability-sim/scripts/barnard_inclination_scan.py --integrator trace

# With hypothetical moons / extra planets
.venv/bin/python phase3/stability-sim/scripts/run.py \
    --system trappist_1 --years 1000 \
    --hypotheticals phase3/stability-sim/hypotheticals/trappist_1.json \
    --out-dir phase3/stability-sim/results/with_moons
```

Registered systems: `trappist_1`, `proxima_cen`, `alpha_centauri`, `55_cnc`,
`61_vir`, `au_mic`, `barnards_star`, `hd_219134`, `hd_69830`, `tau_cet`,
`teegardens_star`, `yz_cet`. The generic planetary loader reads any
single-star `db/systems/<system>.json`.

## Caveats

1. **MEGNO vs a/e.** Pass/fail is the a/e outcome (does a body escape).
   MEGNO is the chaos early-warning, not a fail condition — three systems are
   chaotic yet ship-safe (bounded). Under TRACE there is no MEGNO; the a/e
   verdict carries it.
2. **Integrator choice matters at close encounters — and for secular forcing.**
   WHFast (and, in-game, Principia's fixed-step celestial ephemeris) lose
   accuracy during planet–planet close encounters; TRACE/IAS15 are the ground
   truth there, and the canonical result for a close-encounter-flagged system
   uses TRACE. **But TRACE is *not* the right tool for α Cen**, where the
   instability is secular (Kozai-Lidov from the far companion), not a close
   encounter: there TRACE drifts (|ΔE/E| ≈ 3.6×10⁻³) and IAS15 is canonical.
3. **Msini + coplanar.** Masses are DB-recommended (often Msini, a lower
   bound); inclinations default to coplanar. Real higher masses / mutual
   inclinations could be less stable, so a PASS is necessary, not sufficient.
   A Monte-Carlo-over-uncertainties pass is the natural upgrade.
4. **AU Mic d/e** semi-major axes are Kepler-derived from period (no curated
   a); candidates, uncertain masses, young system.
5. **α Cen A b** is integrated (IAS15) at the Beichman-favored 50° prograde
   mutual inclination; its Kozai instability is inclination-dependent — the
   prograde cliff is ~45°, so a low-inclination or retrograde orbit is stable.
   The verdict is conditional on that inclination.
6. **10⁴ yr is short** for true secular evolution; for the chaotic-but-bounded
   and hot cases a 10⁶-yr or SPOCK-style long-term-probability follow-up would
   strengthen the claim.

## Files

- `scripts/load.py` — DB JSON → REBOUND loader (handles list/dict `physical`;
  derives a from period when no curated semi-major axis).
- `scripts/run.py` — main entry; `--integrator {whfast,trace,ias15}`, WHFast +
  MEGNO by default, writes summary + timeseries.
- `hypotheticals/*.json` — per-system extra-body specs (moons / extra planets).
- `results/*_summary.json` — per-system numerical summary + verdict (the
  `integrator` field records which integrator produced it).
- `results/*_timeseries.csv` — sampled (t, body, a, e) for plotting.

## Related

- [phase3 procedure (skill)](../../.claude/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
- [principia-cfg-reference](../../docs/reference/principia-cfg-reference.md) — Principia's own integrators (Quinlan-Tremaine 1990 order-12 ephemeris); this sim is the pre-flight screen for that engine
