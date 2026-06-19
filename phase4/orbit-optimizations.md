<!-- 궤도 최적화 기록 — 안정성 시뮬로 최적화한 궤도의 과정·결론·cfg 반영 상태·미결 (Phase 4 게이트용) -->
# Phase 4 — Orbit-Optimization Records

Running log of orbits NearStars **optimizes** with the stability sim — used when
the observed (or maximal-variety) orbit is dynamically untenable, so a defensible
stable orbit is selected in its place. Each entry records the process, the
conclusion, where it is already reflected, and any cfg-frame open item the Phase 4
gate must close before the final cfg emit.

**Convention (2026-06-15).** Whenever an orbit is optimized:
1. The full process + numbers live in `phase3/stability-sim/STABILITY_REPORT.md`.
2. The cfg-ready conclusion (a / e / inclination) is written to the curated DB and
   the Phase 3 report (with confidence + `## Canonical alternatives` preserving the
   observed orbit).
3. A summary + any unresolved cfg-frame quantity is logged **here** so the Phase 4
   gate has the analysis pre-staged rather than re-derived.

---

## α Centauri A b (Polyphemus) · 2026-06-07

**Why optimized.** The Beichman 2025 imaging-favored orbit (e ≈ 0.4, mutual
inclination ≈ 50° to the α Cen AB plane) is Kozai–Lidov **unstable**: KL pumps e
past 0.95 within ~30 kyr and the periastron then crashes below the stellar radius
over ~10⁵ yr (tidal disruption; REBOUND/IAS15).

**Process.** Eccentricity + mutual-inclination scan across the HZ-stable window
(IAS15 — the α Cen AB secular Kozai forcing needs the high-order integrator;
TRACE/whfast under-resolve it). Stable window found: e ≈ 0–0.18 (–0.22), mutual
i ≈ 0–33 (–35)°; ≳35° drives the orbit out of α Cen A's HZ, ≳45° is KL-unstable.

**Conclusion (adopted).** Median of the stable window: **a = 1.6 AU (= observed),
e = 0.1, mutual inclination ≈ 16°.** Verified HZ-stable over 1e5 yr (e_max 0.15,
orbit stays 1.37–1.84 AU) and hosts a Hill-stable Pandora-class moon.

**Reflected in.**
- DB `Alpha Centauri A b` (curated): `semi_major_axis_au 1.6`, `eccentricity 0.1`
  (method `predicted`, stability-selected; commit 9051aff). Phase 2 representative
  reconciled 1.9 → 1.6 AU to track the favored a < 2 AU family.
- Phase 3 `docs/phase3/alpha-centauri-a-b.md`: a / e / mutual-inclination fields
  with confidence + `## Canonical alternatives` (observed Kozai-unstable orbit kept).
- Viewer: adopted (stable) ⇄ observed (Kozai-unstable) stability variants.

**OPEN ITEM (Phase 4 gate).** The constrained quantity is the **mutual** inclination
to the AB plane (16°); the **cfg-frame sky `inclination_deg` is unset**. Phase 4
must convert mutual-inclination-to-AB-plane → cfg sky-frame inclination (i_AB =
79.24°; the sky-plane solution is bimodal prograde/retrograde, Beichman Table 4)
before the final cfg emit. `a` and `e` emit directly today.

---

## Barnard's Star — eccentricity for fixed-step (Principia) stability · 2026-06-18

**Why optimized — engine-driven, not physics.** The 4-planet system (b, c, d, e;
Basant et al. 2025) is *physically* chaotic-but-Hill-stable at nominal mass: TRACE
(adaptive) holds it bounded over the 10⁴-yr play window, calm. The problem is the
**game engine**: Principia integrates bodies with a **fixed-step** symmetric
multistep (QUINLAN_TREMAINE_1990_ORDER_12, default 10 min) — same class as WHFast,
and symmetric multistep "fails catastrophically if not converged." A fixed-step
WHFast 1 Myr at the DB's β-prior eccentricities (0.03–0.08) **blew up numerically**
(|dE/E| = 6.2, e → 10²–10³, MEGNO 6.7×10⁴) — i.e. those eccentricities are
fixed-step-fragile and risk an *artificial* in-game ejection over long play.

**Process.** Re-run at the low-eccentricity reading. Basant §3.4: e > 0.02 → <80%
stable; e ≈ 0 → stable over 10⁹ orbits; the paper *favours* e < 0.02. Adopt e = 0.015
(within the favoured window) via `run.py --set '*.e=0.015'` (DB unchanged). WHFast 1 Myr:
**clean and bounded** — |dE/E| = 9.5×10⁻⁹, MEGNO 8.2 (Lyapunov ~3×10⁵ yr), every
planet e_max ≤ 0.031, a fixed to Δa/a ~10⁻⁴. Independent support: the system has
**survived ~10 Gyr** (8.5±1.5, Ribas 2018) → the long-lived real architecture is the
stable low-e one, not the fixed-step-fragile β-prior tail.

**Eccentricity-reduction scan (2026-06-19).** How much reduction is actually needed?
WHFast 1 Myr at several scalings of the β-prior (c is the worst case, shown):

| config | c | \|dE/E\| | MEGNO | e_max | 1 Myr |
|---|---|---|---|---|---|
| β-prior | 0.080 | 6.2 (blow-up) | 6.7×10⁴ | →10³ | ✗ |
| ×0.9 | 0.072 | 2.4×10⁻⁸ | 11,016 | ≤0.096 | ✅ |
| ×0.8 | 0.064 | 7.5×10⁻⁹ | 10,563 | ≤0.085 | ✅ |
| ×3/4 | 0.060 | 1.0×10⁻⁸ | 1,569 | ≤0.079 | ✅ |
| ×2/3 | 0.053 | 2.3×10⁻⁸ | 4,092 | ≤0.071 | ✅ |
| ×0.5 | 0.040 | 1.4×10⁻⁷ | 336 | ≤0.053 | ✅ |
| set 0.015 | 0.015 | 9.5×10⁻⁹ | 8.2 | ≤0.031 | ✅ |

The blow-up/stable boundary sits between c ≈ **0.072 and 0.08** — even ×0.9 (a 10%
reduction) survives, so the β-prior at c = 0.08 sits *right at* the fixed-step edge and
just tips over. The needed correction is tiny. **Caveat:** the near-edge survivors
(×0.8/×0.9) run MEGNO ~10⁴ (strongly chaotic), so the exact tipping point is
phase-seed-sensitive — single-seed runs, the boundary is fuzzy. Lower e buys real chaos
margin (MEGNO drops to ~10² at ×0.5, ~8 at e=0.015). So the Phase 4 choice is a **band**
(c ≲ 0.06 gives comfortable margin; 0.06–0.072 survives but near the edge), trading
measurement fidelity (×0.9, closest to β-prior that still works) against chaos margin
(e = 0.015, the calmest). Scan runs: `results/_phase4_{e09,e08,e34,e23,halfe,lowe}/`.

**Conclusion (Phase 4 CANDIDATE — staged, not gated/emitted).** The whole **c ≲ 0.072
band** survives fixed-step 1 Myr, but only **c ≲ 0.06** gives comfortable chaos margin
(MEGNO ≲ few×10³); 0.064–0.072 survives yet sits near the edge (MEGNO ~10⁴, seed-fuzzy).
Default proposal **e = 0.015** (calmest, inside Basant favoured < 0.02). Measurement-
faithful end: ×0.75–0.9 (c 0.06–0.072) — closest to β-prior that holds, but the higher
the e the thinner the margin. Pick within the band per art-direction at Phase 4.
SPEC class A+B (window-selection + engine); gate `pass-in-window` (Basant favoured /
measured-band + stability-sim evidence above; 10 Gyr survival). Per `phase4/SPEC.md`.

**Reflected in.**
- Process + numbers: `phase3/stability-sim/STABILITY_REPORT.md` (β-prior blow-up vs
  low-e clean); run artifact `results/_phase4_lowe/` (reproduce: `run.py --set '*.e=0.015'
  --years 1000000 --integrator whfast`).
- NOT in the DB (Phase 2 keeps the β-prior measurement) and NOT emitted — this is a
  staged Phase 4 candidate.

**OPEN ITEM (Phase 4 gate).** Confirm e = 0.015 is the value to freeze (vs e = 0.01 /
exactly-circular); when Phase 4 activates, write it to `phase4/barnards_star.yaml`.

---

## Backlog

- **Barnard's Star** — physical stability is fine (TRACE, nominal mass, 10⁴ yr); the
  remaining item is the *fixed-step* eccentricity choice above (low-e candidate staged).
  The earlier "full candidate config ejects within 1 Myr" note referred to the
  confirmed/candidates-variant era + a fixed-step run — re-read as a fixed-step
  fragility, not a physical ejection.
- **AU Mic** — full candidate config dynamically unstable (ejects within 1 Myr,
  confirmed at dt/4); stable full-set element-space search still open. Viewer shows the
  confirmed-only stable subset + the full unstable set as variants. See
  `phase3/stability-sim/STABILITY_REPORT.md`.
