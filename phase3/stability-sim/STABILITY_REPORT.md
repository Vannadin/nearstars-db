# Phase 3 Stability Report — 10,000 yr N-body Integration

**Generated:** 2026-06-07
**Integrator policy:** REBOUND 5.0 **WHFast + MEGNO** as the fast first-pass
screen; **TRACE** (Lu, Hernandez & Rein 2024) re-verification for any system
WHFast flags chaotic or unstable. **IAS15** available for spot-checks.
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
| α Cen A b (in AB binary) | planet + 2 stars | n/a (trace) | **0.998 · extreme** | 1.3 | **UNSTABLE** in favored family (3 of 4 families stable) | trace |

Eleven of the twelve are stable or chaotic-but-bounded under the accurate
integrator: seven regular (MEGNO ≈ 2), three formally chaotic but tightly
bounded (TRAPPIST-1, Barnard, YZ Cet — tight inner M-dwarf chains, consistent
with the literature), and AU Mic dynamically hot but bounded. The only
instability is the S-type candidate **α Cen A b** in its *favored* prograde
inner family (e → 0.99 by Kozai-Lidov at i_mut ≈ 50°) — but a sweep shows 3 of
its 4 proposed orbit families survive (below). The α Cen AB binary itself is
stable (B: e = 0.514–0.519, a-drift < 0.6%).

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
inside the Kozai-Lidov window (39.2°–140.8°). Integrated with TRACE (the
near-equal binary masses break WHFast's small-perturber assumption).

At the favored value the planet is **dynamically unstable**: the eccentric
companion drives **eccentric Kozai-Lidov (octupole)** oscillations that pump
its eccentricity to **e ≈ 0.998 within a few thousand years** — periastron
a(1−e) ≈ 0.005 AU, barely above α Cen A's radius (0.0057 AU) → tidal
disruption. The AB binary itself is unaffected (B: a 23.57–23.70 AU, e
0.514–0.519). But this is **inclination-dependent**, so the loader takes
`--acen-incl-deg` (and `--acen-a-au` / `--acen-e`) for the Beichman orbit
families and a mutual-inclination sweep.

### Mutual-inclination sweep (a = 1.6 AU, TRACE, 10⁴ yr)

| i_mut | e_max | verdict | | i_mut | e_max | verdict |
|---|---|---|---|---|---|---|
| 0° (coplanar) | 0.68 | stable | | 90° | flip (e≫1) | **unstable** |
| 20° | 0.61 | stable | | 115° | 0.86 | stable |
| 35° | 0.99 | **unstable** | | 130° | 0.79 | stable |
| 50° | 1.00 | **unstable** | | 145° | 0.60 | stable |
| 65° | 0.99 | **unstable** | | 160° | 0.56 | stable |

**Stable inclination band: i_mut ≲ 30° (prograde) or ≳ 110° (retrograde); the
~30°–100° band is Kozai-unstable.** The band is **asymmetric about 90°** —
the prograde side destabilizes earlier (~30°, below the 39° quadrupole
threshold) because octupole EKL + the already-eccentric (e = 0.4) planet +
eccentric companion conspire; the retrograde side (≥110°) survives (e_max
0.56–0.86, bounded), the textbook prograde/retrograde octupole asymmetry. Note
that even coplanar the planet is *hot* (e_max 0.68) — the massive eccentric
companion keeps it stirred at all inclinations.

### Beichman's four proposed orbit families — 3 of 4 survive

| Family | a, i_mut | e_max | verdict |
|---|---|---|---|
| prograde, a<2 (**favored**) | 1.6 AU, 50–70° | ≈1.0 | **UNSTABLE** |
| retrograde, a<2 | 1.6 AU, ~120° | 0.79 | stable |
| prograde, a>2 | 2.1 AU, ~50° | 0.88 | stable (marginal) |
| retrograde, a>2 | 2.1 AU, ~120° | 0.88 | stable (marginal) |

So the accurate statement is **not** "α Cen A b is unstable" but: **the
Beichman-*favored* prograde inner family (a ≈ 1.6 AU, i_mut 50–70°) is
Kozai-unstable, while the other three proposed families — retrograde inner,
and both outer (a ≈ 2.1 AU) families — keep the planet bounded over 10⁴ yr.**
If α Cen A b is real, its survival hinges on which family it actually occupies.

**Follow-up:** tidal damping (absent from the point-mass sim) would set where a
high-e/inclined orbit circularizes rather than disrupts, and a finer grid near
the 30° and 110° boundaries would sharpen the stable band.

### Polyphemus & Pandora (Avatar) — a HZ-stable orbit that hosts a moon

α Cen A b is the real-life candidate for **Polyphemus**, the *Avatar* gas giant
whose moon **Pandora** is the Na'vi homeworld (Beichman 2025 / NPR 2025 /
*Seeking the Worlds of Avatar*, Astrobiology 2025). Asking whether a habitable
Pandora could actually survive here drove a fine-tuning scan:

- **The Avatar canon distance (1.2 AU) is unusable** — a secular resonance near
  1.2–1.3 AU pumps e to ~0.64 even from a circular start, throwing Polyphemus
  out of the HZ.
- **The HZ-stable zone is a ≈ 1.4–1.6 AU.** The DB/Phase-3 orbit takes the
  median of the stable range — e 0–0.22 → **e = 0.1**, mutual inclination
  0–33° → **≈ 16°** — at a = 1.6 AU (the observed semi-major axis): HZ-stable
  over 10⁵ yr (orbit 1.37–1.84 AU, e_max 0.15).
- **Pandora is Hill-stable.** A 0.45 M⊕ moon at 225 000 km (Kepler back-out of
  Pandora's ~27 h tidally-locked day; Polyphemus spans ~36° of its sky) sits at
  ~0.02 R_Hill on a near-circular orbit (e ≈ 0, bound) — deep inside the
  Domingos+2006 limit. The full Avatar hierarchy (α Cen A → Polyphemus →
  Pandora, perturbed by α Cen B) is dynamically viable on the stability-selected
  orbit, though not on the Kozai-unstable observed one. Test:
  `hypotheticals/alpha_centauri.json`, run with
  `--acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16`.

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

## How to use

```bash
# Fast first-pass screen (WHFast + MEGNO)
.venv/bin/python phase3/stability-sim/scripts/run.py --system trappist_1 --years 10000

# Accurate re-verification of a flagged system (close encounters / high-e)
.venv/bin/python phase3/stability-sim/scripts/run.py --system au_mic --integrator trace

# Gold-standard spot-check (adaptive high-order, + MEGNO, slow)
.venv/bin/python phase3/stability-sim/scripts/run.py --system au_mic --integrator ias15

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
2. **Integrator choice matters at close encounters.** WHFast (and, in-game,
   Principia's fixed-step celestial ephemeris) lose accuracy during
   planet–planet close encounters; TRACE/IAS15 are the ground truth there.
   The canonical result for a flagged system uses TRACE.
3. **Msini + coplanar.** Masses are DB-recommended (often Msini, a lower
   bound); inclinations default to coplanar. Real higher masses / mutual
   inclinations could be less stable, so a PASS is necessary, not sufficient.
   A Monte-Carlo-over-uncertainties pass is the natural upgrade.
4. **AU Mic d/e** semi-major axes are Kepler-derived from period (no curated
   a); candidates, uncertain masses, young system.
5. **α Cen A b** is integrated at a fixed 50° mutual inclination (the
   Beichman-favored prograde value); its Kozai instability is
   inclination-dependent — a coplanar orbit would be stable, so the verdict is
   conditional on that inclination.
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
