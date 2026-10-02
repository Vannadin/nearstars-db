# C143 가드 전용 — builtins.sum 을 3.9 식(왼쪽부터 더하기)으로 바꾼다. `scripts/c143_guard.py` 가 PYTHONPATH 로만 켠다(엔진은 안 읽는다)
"""Left-to-right `sum()` (Python ≤ 3.11 behaviour) for the C143 guard. Loaded only when `c143_guard.py` puts this
directory on PYTHONPATH; never imported by the engine. Non-float results are left to the original `sum`."""
import builtins

_orig = builtins.sum


def sum(iterable, /, start=0):
    items = list(iterable)
    r = _orig(items, start)
    if not isinstance(r, float):
        return r
    acc = start
    for x in items:
        acc = acc + x
    return acc


builtins.sum = sum
