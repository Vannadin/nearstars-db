# 안정성 벽이 자기 등급을 말하는가 — rtpress 증기압 띠 · 스피노달 범위 벽 · 음성 대조 (C155)
"""prereg-c155-stability-walls (frozen baa302ba): S-class, S-W2, S-neg.

    python3 engine/test_stability_walls.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eos       # noqa: E402
import rtpress   # noqa: E402

fails: list[str] = []


def ok(cond: bool, label: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        fails.append(label)


def band(t: float) -> tuple[float, float]:
    """§1.1 의 띠를 등록본 수로 따로 잰다 — 두 인쇄 맞춤 ∓ 14 MPa (lo 는 0 에서 자름)."""
    fits = [math.exp(11.8 - 45000.0 / t), math.exp(12.45 - 49420.0 / t)]
    return max(0.0, min(fits) - 14.0), max(fits) + 14.0


# (이름, T [K], 목표 P [GPa], 등급, 문구에 꼭 있어야 할 조각) — §3 S-class 의 일곱 점
CASES = [
    ("rule 4 boils (5A)", 5345.3, 0.0001, "boils",
     ["규산염 증기압(Xiao & Stixrude 2018 두 맞춤 ± 두 상 폭 14 MPa: {lo:.1f}–{hi:.1f} MPa) 밑이라 암석이 끓는다; "
      "RTpress 에는 증기 가지가 없다 (C155 물리 벽)"]),
    ("rule 6 may boil (17B)", 5341.0, 0.03487, "may boil",
     ["규산염 증기압 근처(두 맞춤 ± 두 상 폭 {lo:.1f}–{hi:.1f} MPa 안)라 끓는지 정하지 않는다; "
      "RTpress 에는 증기 가지가 없다 (C155 미정)"]),
    ("rule 5 stable (4B)", 5351.3, 0.05517, "stable",
     ["실제 규산염은 안정한 액체(또는 초임계 유체)다 (증기압 {lo:.1f}–{hi:.1f} MPa 위); "
      "RTpress 꼴의 한계이지 물리 한계가 아니다 (C155 범위 벽)"]),
    ("rule 1 stable (12A)", 5770.6, 0.8605, "stable", ["(임계압 140 MPa 위)", "(C155 범위 벽)"]),
    ("rule 1 stable (8B)", 7470.2, 5.085, "stable", ["(임계압 140 MPa 위)", "(C155 범위 벽)"]),
    ("rule 2 stable (constructed)", 7500.0, 0.1, "stable", ["(임계온도 7000 K 위)", "(C155 범위 벽)"]),
    ("rule 3 may boil (constructed)", 6500.0, 0.1, "may boil",
     ["규산염 증기압 근처(임계온도 불확도 6450–7000 K 안)라 끓는지 정하지 않는다; "
      "RTpress 에는 증기 가지가 없다 (C155 미정)"]),
]


def s_class(report: bool = True) -> int:
    """일곱 점 — 등급과 정확한 문구. 돌려주는 값은 FAIL 수(음성 대조가 `report=False` 로 조용히 센다)."""
    bad = 0
    for name, t, p, want, parts in CASES:
        lo, hi = band(t)
        try:
            rtpress.volume_full(p, t)
            got, text = None, ""
        except eos.PhaseGap as gap:
            got, text = getattr(gap, "wall_class", None), gap.reason
        miss = [x for x in (q.format(lo=lo, hi=hi) for q in parts) if x not in text]
        good = got == want and not miss
        bad += not good
        if report:
            ok(good, f"S-class {name}: ({t:g} K, {p * 1e3:g} MPa) → {got}"
               + (f"; 빠진 문구 {miss[0][:50]}…" if miss else ""))
    return bad


def s_no_wall() -> None:
    """W1 벽이 없는 자리(P ≥ P_min)는 아무것도 안 던진다 — 등급 함수는 벽에서만 불린다."""
    try:
        rtpress.volume_full(1.0, 5345.3)
        ok(True, "S-class: (5345.3 K, 1 GPa) — 벽 없음, 던지지 않는다")
    except eos.PhaseGap as gap:
        ok(False, f"S-class: (5345.3 K, 1 GPa) 가 던졌다 — {gap.reason[:60]}")


def _material(name: str) -> eos.Material:
    return next(m for m in vars(eos).values() if isinstance(m, eos.Material) and m.name == name)


def s_w2() -> None:
    """fe_prem 과 mgsio3 상 하나를 스피노달 밖으로 — SpinodalGap · 등급 coverage · 가리키는 등록."""
    for mat, phase, pointer in (("fe_prem", "fe_prem", "고칠 길 C119 — 뜨거운 액체 철"),
                                ("silicate", "mgsio3_en", "고칠 길 C156 — 뜨거운 내부")):
        ph = next(x for x in _material(mat).phases if x.name == phase)
        _rho_s, p_s = ph._spinodal()
        try:
            ph._density_tension(2.0 * p_s, 20000.0)
            ok(False, f"S-W2 {phase}: 스피노달 밖인데 던지지 않았다")
        except eos.SpinodalGap as gap:
            want = (f" — {phase} 의 열압력 꼴(냉각 곡선 + 선형 열압력; 팽창 쪽 뒤집기는 등급 판단)의 범위 밖이라는 뜻이지, "
                    f"물질이 거기서 물리적으로 없다는 뜻이 아니다 (C155 범위 벽; {pointer})")
            ok(getattr(gap, "wall_class", None) == "coverage" and gap.reason.endswith(want)
               and "냉각 곡선의 스피노달" in gap.reason and gap.too_cold is False,
               f"S-W2 {phase}: SpinodalGap · coverage · {pointer.split(' — ')[0]}")


def s_neg() -> None:
    """등급 함수가 늘 한 등급만 내면 S-class 가 다른 등급의 점에서 실패해야 한다 — 픽스처가 규칙을 본다."""
    real = rtpress.vapour_class
    rtpress.vapour_class = lambda t, p: ("boils", real(5345.3, 0.0001)[1])
    try:
        bad = s_class(report=False)
    finally:
        rtpress.vapour_class = real
    want = sum(1 for c in CASES if c[3] != "boils")
    ok(bad == want, f"S-neg: 한 등급만 내면 {bad} 점 실패(기대 {want} — boils 아닌 점 전부)")


if __name__ == "__main__":
    print("S-class — rtpress 벽의 등급(C155 §1.1)")
    s_class()
    s_no_wall()
    print("S-W2 — 스피노달 범위 벽(C155 §1.2)")
    s_w2()
    print("S-neg — 음성 대조")
    s_neg()
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    sys.exit(1 if fails else 0)
