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

## Backlog

- Barnard's Star / AU Mic — the full candidate configs are dynamically unstable
  (eject within 1 Myr, confirmed at dt/4). A **stable full-set solution search**
  (element-space scan like α Cen A b) is open; until then the viewer shows the
  confirmed-only stable subset + the full unstable set as variants. See
  `phase3/stability-sim/STABILITY_REPORT.md`.
