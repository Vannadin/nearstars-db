# C152 시험 — 공용 Brent 가 근을 좁히고, 근 없는 잔차는 거절로 남고, 실오라기 용융은 가족 뜀이 아닌가
"""python3 engine/test_rootfind.py — prereg-c152-straddle-root acceptance 5 (unit part; the loop-level runs are on the PC)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior  # noqa: E402
import rootfind  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def drive(f, a, b, xtol, budget=200):
    g = rootfind.brent(a, f(a), b, f(b), xtol)
    n = 0
    try:
        x = next(g)
        while n < budget:
            n += 1
            x = g.send(f(x))
    except StopIteration as fin:
        return fin.value, n
    return None, n


# ① 아는 근을 xtol 안에 · 매끄러운 잔차는 이분보다 적은 걸음
(x, fx, lo, hi), n = drive(lambda t: t ** 3 - 2.0, 0.0, 2.0, 1e-12)
check("Brent — x³ = 2 의 근을 xtol 안에", abs(x - 2.0 ** (1 / 3)) < 1e-11 and hi - lo <= 2e-12, f"{x!r} · {n} 걸음")
check("Brent — 매끄러운 잔차는 이분(≈ 41 걸음)보다 적게", n < 20, str(n))
# ② 로그 온도 1 K 괄호(화성 꼴): T_TOL 까지 T_PASSES 안
f_mars = lambda lt: (lt - 8.0798) * 1.5 + 4.0 * max(0.0, lt - 8.0799)      # 근 근처에서 기울기가 바뀌는 잔차
(x, fx, lo, hi), n = drive(f_mars, 8.0795, 8.0802, interior.T_TOL)
check("Brent — 기울기가 꺾이는 1 K 괄호를 T_PASSES 안에", n <= interior.T_PASSES and abs(fx) < 1e-6, f"{n} 걸음")
# ③ 음성 대조 — 근이 없는(같은 부호) 잔차는 이름 대고 거절, 뛰는 잔차는 뜀으로 좁혀지고 |f| 가 남는다
try:
    rootfind.brent(0.0, 1.0, 1.0, 2.0, 1e-9)
    check("음성 대조 — 같은 부호 양 끝은 거절", False, "통과함")
except ValueError as e:
    check("음성 대조 — 같은 부호 양 끝은 거절", "straddle" in str(e), str(e))
(x, fx, lo, hi), n = drive(lambda t: -1.0 if t < 1.3 else 1.0, 0.0, 2.0, 1e-9)
check("음성 대조 — 뛰는 잔차는 뜀 자리로 좁혀지고 |f| 가 허용 밖으로 남음", abs(x - 1.3) < 1e-8 and abs(fx) == 1.0, f"{x!r}")
# ④ 가족 판정 — 표본 하나짜리 실오라기는 뜀 아님, 표본 둘은 뜀, 화성 간격에서 문턱 0.5 GPa 그대로
dps = 0.39
check("가족 — 실오라기(한 표본)와 고체는 같은 가족", not interior._family_jump(None, (0.17, 0.17, dps)))
check("가족 — 두 표본 폭의 용융과 고체는 다른 가족", interior._family_jump(None, (0.17, 0.17 + dps, dps)))
check("가족 — 화성 간격에서 0.45 GPa 이동은 같은 가족(문턱 0.5)", not interior._family_jump((7.0, 15.0, dps), (7.45, 15.0, dps)))
check("가족 — 화성 간격에서 0.55 GPa 이동은 뜀(문턱 0.5 그대로)", interior._family_jump((7.0, 15.0, dps), (7.55, 15.0, dps)))
check("가족 — 성긴 표본(0.8 GPa)에서는 문턱 1.2 GPa", not interior._family_jump((7.0, 15.0, 0.8), (8.0, 15.0, 0.8))
      and interior._family_jump((7.0, 15.0, 0.8), (8.3, 15.0, 0.8)))
check("가족 — 207x 의 두 가족(p_hi 15.36 대 17.06)은 여전히 뜀", interior._family_jump((6.49, 15.36, dps), (6.87, 17.06, dps)))

print(f"  test_rootfind — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
