# 창 가장자리 항목 시험 — 모든 걸음의 단계 묶음이 사격 질량 뜀을 없애고(끄면 되살아남), 녹는 곡선 이음매에 걸음이 착지하는가
"""python3 engine/test_window_edge.py — window-edge registration (frozen 59bee405, note 1 f6d22fa1); 68's B1 on 82e61195.

(a) The clamp. Venus's table point 1985.4441894853112 K, seams off: the shot's mass jumped at one p_c because an uncut
    step's k4 stage read below the 23.83 GPa en → prem bound (note 1 §1). The jump's p_c is bisected to adjacent
    doubles with STAGE_CLAMP_EVERY_STEP False, and the mass difference across it must be a jump there (> 1e-6 relative)
    and continuous with the clamp on (< 1e-9 relative).
(b) The landing. The same walk with seams on crosses 20 GPa: MELT_SEAM_CUTS > 0 and a step end sits at
    p_b(1 − 4e-12) within 1e-12·p_b; with MELT_SEAMS_LANDED False, no cut and no such end.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior  # noqa: E402
import structure_grid as sg  # noqa: E402
import run  # noqa: E402

fails = 0
T_POT, P_JUMP = 1985.4441894853112, 287.533162648e9


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


@contextlib.contextmanager
def switches(**sw):
    saved = {n: getattr(interior, n) for n in sw}
    try:
        for n, v in sw.items():
            setattr(interior, n, v)
        yield
    finally:
        for n, v in saved.items():
            setattr(interior, n, v)


def venus_calls():
    """The integrate calls of venus's table solve at T_POT, seams off and the clamp off (the refusing path)."""
    doc = json.loads(sg._path_for("venus").read_text(encoding="utf-8"))
    body, _ = run.load_body(sg.BODIES_DIR / "venus.yaml")
    solve, _how, _cmf = sg._solver(body, types.SimpleNamespace(values={"core_mass_fraction": doc["points"][0]["core_mass_fraction"]}))
    calls, orig = [], interior._integrate_raw

    def spy(*a, **k):
        calls.append((a, dict(k)))
        return orig(*a, **k)
    interior._integrate_raw = spy
    try:
        with switches(MELT_SEAMS_LANDED=False, STAGE_CLAMP_EVERY_STEP=False), contextlib.redirect_stdout(io.StringIO()):
            r = solve(T_POT)
    finally:
        interior._integrate_raw = orig
    return r, calls


def walk(args, p_c, **sw):
    a, k = args
    rec = []
    k = dict(k, record=rec)
    with switches(**sw), contextlib.redirect_stdout(io.StringIO()):
        interior._integrate_raw(p_c, *a[1:], **k)
    return rec


check("the shipped defaults: STAGE_CLAMP_EVERY_STEP and MELT_SEAMS_LANDED are True",
      interior.STAGE_CLAMP_EVERY_STEP is True and interior.MELT_SEAMS_LANDED is True)
r, calls = venus_calls()
check("seams off, clamp off: venus 1985.444 refuses with the shot's mass jump (the defect this item fixes)",
      (not r.applicable) and interior.BACKSTOP_REASON_HEAD in (r.reason or ""), (r.reason or "")[:60])
args = min(calls, key=lambda c: abs(c[0][0] - P_JUMP))

print("(a) the clamp on every step")
off = dict(MELT_SEAMS_LANDED=False, STAGE_CLAMP_EVERY_STEP=False)
lo, hi = P_JUMP * (1 - 2e-9), P_JUMP * (1 + 2e-9)
m = lambda rec: rec[-1][2]                                        # noqa: E731
m_lo, m_hi = m(walk(args, lo, **off)), m(walk(args, hi, **off))
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if mid in (lo, hi):
        break
    m_mid = m(walk(args, mid, **off))
    if abs(m_mid - m_lo) < abs(m_mid - m_hi):
        lo, m_lo = mid, m_mid
    else:
        hi, m_hi = mid, m_mid
jump_off = abs(m_hi - m_lo) / abs(m_lo)
# the shipped defaults (no switch passed), seams off so the pair is the same walk as the control's
jump_on = abs(m(walk(args, hi, MELT_SEAMS_LANDED=False)) - m(walk(args, lo, MELT_SEAMS_LANDED=False))) / abs(m_lo)
check("clamp off: the surface mass jumps across adjacent p_c (> 1e-6 relative)", jump_off > 1e-6,
      f"{jump_off:.3e} at p_c {lo / 1e9:.12f} GPa")
check("clamp on: continuous across the same pair (< 1e-9 relative)", jump_on < 1e-9, f"{jump_on:.3e}")

print("(b) the landing on the 20 GPa melt-curve seam")
p_t = 20e9 * (1.0 - 4e-12)
for landed in (True, False):
    c0 = interior.MELT_SEAM_CUTS[0]
    rec = walk(args, args[0][0]) if landed else walk(args, args[0][0], MELT_SEAMS_LANDED=False)   # landed = default
    cuts = interior.MELT_SEAM_CUTS[0] - c0
    on_seam = any(abs(x[1] - p_t) <= 1e-12 * 20e9 for x in rec)
    if landed:
        check("seams landed: MELT_SEAM_CUTS > 0 and a step end at 20 GPa·(1 − 4e-12)", cuts > 0 and on_seam,
              f"cuts {cuts}, on-seam end {on_seam}")
    else:
        check("seams not landed (control): no cut and no step end on the seam", cuts == 0 and not on_seam,
              f"cuts {cuts}, on-seam end {on_seam}")

print(f"test_window_edge: {'모두 통과' if not fails else f'FAIL {fails}'}")
sys.exit(1 if fails else 0)
