# 수렴 기록 부류(T · F · P)가 AND 와 내보내기 칸에 제대로 가는지 아는 판으로 가르는 시험 (prereg-c138 K2 · K3)
"""C138 known cases on the trace itself: a fallback (F) is counted outside the AND and shows in
fallback_solvers, not unconverged_solvers; the same site noted False (K3, the case that must fail the
F reading) does show as unconverged; a trial False (P) stays outside the AND in trial_unconverged."""
from __future__ import annotations

import sys

import convergence
import interior


def _run(fn):
    with convergence.start():
        fn()
        return interior._convergence_values()


def main() -> int:
    fails = 0
    cases = (
        ("K2 F → fallback 칸", lambda: convergence.note_fallback("interior._shoot_warm_start"),
         lambda v: v["converged"] is None and v["unconverged_solvers"] == [] and v["fallback_solvers"] == ["interior._shoot_warm_start"]),
        ("K3 같은 자리 False → 미수렴", lambda: convergence.note("interior._shoot_warm_start", False),
         lambda v: v["converged"] is False and v["unconverged_solvers"] == ["interior._shoot_warm_start"]),
        ("P 시행 False → AND 밖", lambda: (convergence.note("interior._shoot_pressure", False, trial=True),
                                          convergence.note("interior._surface_temperature", True)),
         lambda v: v["converged"] is True and v["unconverged_solvers"] == [] and v["trial_unconverged"] == ["interior._shoot_pressure"]),
    )
    for name, fn, ok_of in cases:
        v = _run(fn)
        ok = ok_of(v)
        fails += not ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — converged {v['converged']} · unconverged {v['unconverged_solvers']} · "
              f"fallback {v['fallback_solvers']} · trial {v['trial_unconverged']}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
