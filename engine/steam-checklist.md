# IAPWS steam for the wedge — checklist

Brief 25, 2026-08-31 (owner-approved; prerequisite of the ice axis ③). Fill the wall
Brief 23 named — liquid/vapor water at **p ≲ 0.1 GPa × 500–1000 K** (92–94 % of the
end-B trial deaths), the tri-corner of water1's 500 K top, water2's 0.1 GPa floor and
Mazevet's 1000 K floor.

## Pre-registered BEFORE the source document is opened

**Source intent**: IAPWS-IF97 (the industrial formulation), whose **region 2** claims
exactly the window (T ≤ 1073.15 K at p ≤ 100 MPa) as a closed-form Gibbs function with
printed coefficients and **printed computer-program verification values** — transcribe the
equations, never fit or digitize; the verification table is the transcription gate. If
region 2's claimed validity does not actually cover the wedge, that is branch 4.

**Physicality criteria, fixed before any sweep** (the water2 rule; C6 showed printed
ranges are claims):
- ρ finite and > 0, monotonically increasing with P along every isotherm;
- 500 < c_P < 15 000 J/kg/K over the wedge (steam c_P runs ~2000–3000; the lower bound is
  set below water's liquid range on purpose — vapor c_P near 2000 is physical);
- 0 < ∇_ad < 1;
- seams measured and recorded, no tolerance asserted where they are findings: steam↔water1
  along T = 500 K (p ≤ 0.1 GPa), steam↔water2 along p = 0.1 GPa (500–1000 K),
  steam↔Mazevet along T = 1000 K (p ≤ 0.1 GPa).

**Outcome branches, five.**
1. The window is covered completely.
2. Covered partially → the remaining hole in coordinates.
3. Covered but unphysical at a seam → record the effective ceiling and stop there.
4. IAPWS is not actually valid there → a legitimate ending.
5. Outside the register → name it.

**Acceptance**: rerun the ice axis's four end-B solves. `conv=True` is what "the wall is
filled" means, and only then may gap-covered percentages exist; if not, the product is
**the next wall's coordinates**.

**Must carry (from `7769be6e`)**: steam fills the wedge's water-EOS gap, **not its mixing
gap** — the band is outside Soubiran & Militzer's validation (2–70 GPa × 1000–6000 K), so
any crossing rides on unvalidated additive mixing; the result and the grade note must say
so.

**Hard constraints**: anchors bit-identical; gate FAIL 0 with measured delta; **no new
runtime dependency** (closed-form transcription into a plain module, dev-venv only if a
generator is needed); English commits, one logical unit each.

## Work items

- [x] IF97 release cached (`IAPWS-IF97-Rev.pdf`, 49 pp, R7-97(2012), title checked;
      iapws.org now serves HTML at the old URL — the PDF came from the Internet Archive's
      capture of the canonical path)
- [x] Transcribed regions 1, 2 **and 3** (the post-steam refusal spy showed the wall's
      remnant was exactly the region-3 triangle, 18–97 MPa × 635–661 K) + B23 + saturation;
      all tables read from page images (the text layer drops the powers of ten).
      verify() = worst 3.2e-9 against Tables 5/15/33/35 + B23 point + a ρ round-trip
- [x] Physicality sweep (500–1070 K × 0.1–100 MPa, r1·2): 0 violations; c_P ∈
      [1981, 14040] J/kg/K (top near-critical, inside the registered bound)
- [x] Seams: water1 @100 MPa ρ 0.005 % · c_P 0.21 %; water2 @0.1 GPa ρ ≤0.02 % ·
      c_P ≤0.12 %; **Mazevet @1000 K low-P +88 %(100 MPa)…+994 %(20 MPa)** — the
      measurement of Mazevet's own ρ≳1 g/cc validity claim; steam must precede it
- [x] Wired (`_Steam` adapter, dispatch ahead of water1/Mazevet); in-column
      `liquid_material` wedge out of scope, recorded
- [x] **Acceptance ran (2026-09-01)** — after two more walls of its own: a duplicate
      chain (both killed) and the temperature loop's re-firing one-shot extension
      (found by tracing, fixed in 6d59730d — see the register below). Four solves in
      parallel, 165–263 s each: **conv=False on all four**, but the steam wall is
      retired — spy 100 PhaseGaps, **all h_he too_cold, zero water** (was 1102-of-1202
      on the water wedge). The next wall: the H/He window's cold floor (the
      adiabat-from-1 bar·50 K boundary) at 130–164 GPa; every converged attempt pins
      t_surface ≈ 355–363 K against t_pot = 76 K. Per the pre-registered acceptance,
      conv=False → **no gap-covered percentages**; the product is these coordinates
- [x] Mixing-gap label + grade note carried (envelope-water note names IF97 and the
      Soubiran band; `7769be6e`'s label stands)
- [x] Anchors --fast bit-identical. The fingerprint DID move late (the solve-note string
      naming IF97 sits inside a fingerprinted function) → --refresh ran in this landing;
      anchor diff is fingerprint/date/seconds only. Full live gate deferred with the hold
- [x] Full gate — FAIL 0, exit 0, **1205 s measured** (2026-09-01, fresh run replacing
      the INVALID exit-143 one). Not directly comparable to the last valid full gate
      (~17 min, Brief 24 landing) — test content changed in between (steam verify +
      cold-flank sections). The controlled pair inside it: anchor `seconds` 23.4→21.9 /
      55.7→52.4 (−6 %) — ghost-process absence; the Newton inversion's share there is
      zero (anchor paths never enter region 3)

## Region-3 inversion speedup (owner-directed, 2026-09-01 pre-dawn) — REGISTERED BEFORE EDIT

The acceptance chain ran hours without printing solve 1 of 4: the "~15 min" estimate was
measured (by the directing seat: 195/246/213/212 s, all conv=False) on runs whose walks
STOPPED EARLY at the then-unfilled region-3 wall — not, as this register first said, on
1-s deaths; correction from the directing seat, 2026-09-01. With the wall filled, trials
integrate to full depth, and each region-3 density call costs a measured **1.15 ms**
(80 fixed bisection iterations) = 82× region 1, ~400× the water1 table. Owner directive:
kill, speed up the inversion (Newton), rerun the four solves **in parallel**.

**Registered invariants (all must hold, else revert):**
- root equivalence: new `_r3_density` vs the old 80-iteration bisection on a grid across
  the region-3 triangle (and both T<T_c branches) — worst relative diff ≤ 1e-9;
- `verify()` worst ≤ 1e-8 (same standard tables; the transcription gate re-passes);
- anchors `--fast` bit-identical (change is outside the fingerprinted corridor);
- speedup and new per-call cost measured and recorded.

**Branches:** ① all pass → adopt, relaunch chain. ② Newton unstable anywhere → bracket-
safeguarded fallback bisects that step (correctness unaffected); if equivalence still
fails → revert, back to bisection, record. ③ speedup insufficient (<4×) → keep whichever
is correct, parallelism alone carries the chain.

## Temperature-loop extension leak (found by the acceptance chain) — REGISTERED BEFORE EDIT

The four parallel end-B solves ran 6.6+ h wall each without printing; a `_shoot_pressure`
trace on U-ice measured the loop: every converged attempt lands at t_surface ≈ 355–363 K
regardless of t_center (target t_pot = 76 K — unreachable from below; too-cold refusals
at 130–152 GPa pin the reachable t_center ≥ ~3500 K), and the loop cycles down-ratio /
climb-×1.6 forever. Bound check: 51 converged attempts observed > the intended cap of
1 + T_PASSES + one extension = 29, with zero wall exceptions.

**Cause (code vs its own comment):** `bracketed = True` is re-armed every non-contracting
iteration by the devs check, so the "한 벌 더, **한 번만**" extension
(`passes = T_PASSES`) re-fires every time passes reaches 0 — the `bracketed = "extended"`
sentinel is overwritten. Termination then requires secant/stuck/done, none reachable when
every attempt lands hot-side (lo stays None). Pre-region-3 this was masked: trials died at
the steam wedge before the cycle could establish itself.

**Fix registered:** enforce the stated once-only contract with a dedicated flag
(`extended`), nothing else — no tuning, no new branches.

**Invariants:** anchors bit-identical in values (fingerprint moves — shoot is a
PATH_FUNCTION — so --refresh in the same commit, diff must be fingerprint/date/seconds
only); the four end-B solves must terminate; gate FAIL 0.

**Branches:** ① anchors identical + solves terminate → adopt; the solves' own verdict
(conv / wall coordinates) is then Brief 25's registered acceptance answer. ② anchors move
→ revert, escalate to cb (the fix touched answers it must not). ③ solves still don't
terminate → second cause exists; trace again, register separately.
