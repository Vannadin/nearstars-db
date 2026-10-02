# 범위 값(하한·상한·구간)은 자기가 묶는 방향으로만 판정한다 — 반대쪽은 «미정» (C154)
"""A bound decides only in the direction it bounds (prereg-c154-bound-verdicts).

    verdict(value, kind, threshold, above, below, undetermined, name) -> (verdict, reason)

`kind` says what `value` is:
- "exact": the value itself, so either side decides;
- "lower": the true quantity is ≥ value, so only «above the threshold» can be proved;
- "upper": the true quantity is ≤ value, so only «below the threshold» can be proved.
For an interval (lo, hi) use `interval_verdict`. Both report the unsupported side as `undetermined`, with a
reason that names the bound. They hold no state and are only comparisons, so a numeric value never moves.
"""
from __future__ import annotations

KINDS = ("exact", "lower", "upper")


def verdict(value: float, kind: str, threshold: float, above, below, undetermined, name: str = "value"):
    """`above` if the true quantity is provably > threshold, `below` if provably ≤ threshold, else `undetermined`."""
    if kind not in KINDS:
        raise ValueError(f"bound kind {kind!r} is not one of {KINDS}")
    is_above = value > threshold
    if kind == "exact" or (kind == "lower" and is_above) or (kind == "upper" and not is_above):
        return (above if is_above else below), ""
    side = "a lower bound" if kind == "lower" else "an upper bound"
    return undetermined, (f"{name} {value:.6g} is {side}, and it sits on the side of {threshold:.6g} "
                          f"that {side} cannot prove — undetermined (C154)")


def interval_verdict(lo: float, hi: float, threshold: float, above, below, undetermined, name: str = "value"):
    """`above` if lo > threshold, `below` if hi ≤ threshold, else (the interval straddles) `undetermined`."""
    if lo > threshold:
        return above, ""
    if hi <= threshold:
        return below, ""
    return undetermined, (f"{name} spans {lo:.6g}–{hi:.6g}, across {threshold:.6g} — undetermined (C154)")
