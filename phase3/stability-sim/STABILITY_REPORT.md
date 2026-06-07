# Phase 3 Stability Report — 10,000 yr N-body Integration

**Generated:** 2026-06-07
**Integrator policy:** REBOUND 5.0 **WHFast + MEGNO** as the fast first-pass
screen; **TRACE** (Lu, Hernandez & Rein 2024) re-verification for any system
WHFast flags chaotic or unstable. **IAS15** available for spot-checks.
**Horizon:** 10,000 yr (Principia play window).
**Phase initialisation:** `raw.omega_deg` from DB where available; Ω and M
randomised with a deterministic seed (`phase_seed=0`).

## Two diagnostics, two questions

The verdict separates *what actually happened* from *chaos risk* — they are
not the same and are read together:

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

**Why the hybrid policy:** WHFast is fast and gives MEGNO, but it is
inaccurate during close encounters — it can report a *spurious* ejection
(see AU Mic). TRACE integrates close encounters accurately (≈IAS15) but has
no MEGNO. So WHFast supplies the chaos flag and TRACE supplies the
trustworthy a/e outcome for the flagged systems; the canonical result for a
flagged system uses TRACE, with its WHFast MEGNO carried in the table below.

## Verdict summary (12 systems)

`MEGNO` is the WHFast screen value (chaos indicator). `e_max` / `Δa/a` are
from the canonical integrator in the last column.

| System | Bodies | MEGNO (WHFast) | e_max | max Δa/a | verdict | canonical |
|---|---|---|---|---|---|---|
| Proxima Cen | 3 (b/c/d) | 2.000 | <0.001 | 8×10⁻⁴ | **stable (regular)** | whfast |
| 55 Cnc | 5 | 1.961 | 0.12 | 3.3×10⁻² | **stable (regular)** | whfast |
| 61 Vir | 3 | 1.962 | 0.39 | 1.1×10⁻³ | **stable (regular)** | whfast |
| HD 219134 | 6 | 2.000 | 0.068 | 2.8×10⁻³ | **stable (regular)** | whfast |
| HD 69830 | 3 | 1.998 | 0.20 | 7.8×10⁻⁴ | **stable (regular)** | whfast |
| tau Cet | 4 | 2.001 | 0.24 | 3.6×10⁻⁴ | **stable (regular)** | whfast |
| Teegarden's Star | 3 | 2.000 | 0.091 | 6.1×10⁻⁴ | **stable (regular)** | whfast |
| TRAPPIST-1 | 7 | 1265 | 0.021 | 5.9×10⁻³ | **chaotic, bounded** | TRACE |
| Barnard's Star | 4 | 248 | 0.106 | 8.3×10⁻⁴ | **chaotic, bounded** | TRACE |
| YZ Cet | 3 | 8.024 | 0.103 | 2.0×10⁻³ | **chaotic, bounded** | TRACE |
| AU Mic | 4 | 6249 | 0.63 | 3.5 (b's a triples) | **chaotic, hot but bounded** | TRACE |
| α Cen A b (in AB binary) | planet + 2 stars | n/a (trace) | 0.998 | 1.3 | **UNSTABLE — Kozai-Lidov** | trace |

Eleven of the twelve are stable or chaotic-but-bounded under the accurate
integrator: seven regular (MEGNO ≈ 2), three formally chaotic but tightly
bounded (TRAPPIST-1, Barnard, YZ Cet — tight inner M-dwarf chains, consistent
with the literature), and AU Mic dynamically hot but bounded. **The lone
genuine instability is the S-type candidate α Cen A b**, driven to e → 0.99 by
Kozai-Lidov at its 50° mutual inclination (below). The α Cen AB binary itself
is stable (B: e = 0.514–0.519, a-drift < 0.6%).

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

## α Centauri A b — Kozai-Lidov unstable at the 50° mutual inclination

The binary loader now injects the S-type candidate **α Cen A b** (a ≈ 1.6 AU,
e ≈ 0.4, m ≈ 120 M⊕) around star A, placed at the same node as B so its mutual
inclination to the AB plane is exactly **50°** (Beichman 2025, prograde) —
inside the Kozai-Lidov window (39.2°–140.8°). Integrated with TRACE (the
near-equal binary masses break WHFast's small-perturber assumption).

**Result — the planet is dynamically unstable:**

| Body | a range (AU) | e range | status |
|------|--------------|---------|--------|
| α Cen B | 23.57–23.70 | 0.514–0.519 | stable (binary unaffected) |
| α Cen A b | 1.04–2.37 | 0.081 → **0.998** | **unstable** |

The eccentric companion drives **eccentric Kozai-Lidov (octupole)**
oscillations that pump the planet's eccentricity to **e ≈ 0.998 within a few
thousand years** — a periastron of a(1−e) ≈ 0.005 AU, barely above α Cen A's
radius (0.0057 AU). The planet would be tidally disrupted / circularized;
as a 1.6 AU world it does **not survive** the inclined configuration.

**This is conditional on the inclination, and that's the point.** A
**coplanar** α Cen A b at 1.6 AU is well inside the literature's ~3 AU S-type
stability limit and would be stable — α Cen A planets are only unstable when
*inclined* into the Kozai window. So the verdict is: *if* α Cen A b is real
*and* near the Beichman-favored prograde 50° mutual inclination, it is
Kozai-unstable; a low-inclination orbit would survive. The retrograde ~130°
family is also in the window. (Energy error rises to |ΔE/E| ≈ 8×10⁻⁴ during
the deep near-stellar periastra; the e ≥ 0.9 verdict is robust regardless.)

**Follow-up:** a mutual-inclination sweep (coplanar → 90°) would map the exact
Kozai-stable inclination band for this system, and tidal damping (absent from
the point-mass sim) would set where an inclined planet circularizes rather
than disrupts.

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
