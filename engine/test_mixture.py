# 혼합 규칙 앵커 — 한 층에 두 물질이 섞였을 때, 그리고 문서 표를 다시 만든다
"""Anchor the additive volume law on its own algebra and on two measured planets.

    python3 engine/test_mixture.py
    python3 engine/test_mixture.py --table     문서 §Validation 의 혼합 표를 다시 낸다

혼합은 **새 상태방정식 형태가 아니라 있는 재료 둘을 합치는 규칙** 이다. 그래서 이 파일이
검사하는 것은 새 물리가 아니라, 규칙이 자기 대수를 지키는가와 그 규칙이 실제 천체를
움직이는가다.

세 층위로 검사한다.

1. **대수.** 성분이 하나면 그 재료 자신과 정확히 같아야 하고, 분율 0 인 성분은 답에도
   상한에도 영향이 없어야 한다. 여기가 어긋나면 Z = 0 이 기존 결과를 재현하지 못한다.
2. **측정된 행성.** 토성이 Guillot 1999 의 Z 예산 안에서 내려오는가. 이 갈래의 판정선이다.
3. **판별.** 미분화에는 측정된 C/MR² 앵커가 없다. 대신 측정값을 **가려내는** 검사를
   한다 — 수성을 미분화로 풀면 측정된 C/MR² 가 안 나와야 한다.
"""
from __future__ import annotations

import math
import sys

from eos import (AVL_VOLUME_DEVIATION, MATERIALS, SILICATE_PREM_TO_PV, Mixture,
                 mix)
from interior import EARTH_RADIUS_M, ENVELOPE_Z_MATERIAL, solve

# 목성 C/MR² 앵커. 출처와 기각한 값들은 test_giant.py 머리 주석에 있다.
JUPITER_NMOI_BAND = (0.2634, 0.2644)   # Neuenschwander+ 2021 ∪ Wahl+ 2017

# ── 발표값 ──────────────────────────────────────────────────────────────
#
# 중원소 총량은 Guillot 1999 (arXiv:astro-ph/9907402) 의 제약이다 — 목성 11~42 M⊕,
# 토성 19~31 M⊕. 질량으로 나눈 것이 아래의 Z 구간이고, **아무것도 맞추지 않았다.**
# 토성이 맞는 Z = 0.200 은 그 구간의 아래 끝이지 탐색해서 찾은 값이 아니다.
#
# 반지름은 IAU/IAG 실무그룹의 부피 평균반지름이다 (Archinal+ 2011). 비회전 구형
# 모형이므로 적도 1-bar 와 대조하면 2~3 % 틀린다.
JUPITER = ("Jupiter", 317.828, 69911, 11.0, 42.0)
SATURN = ("Saturn", 95.159, 58232, 19.0, 31.0)

# 수성. 미분화 판별 검사의 상대이고, 값은 test_interior.py 의 앵커와 같은 출처다
# (Margot+ 2012, MESSENGER 레이더).
MERCURY_MASS_ME = 0.0553
MERCURY_CMF = 0.70
MERCURY_NMOI = 0.3460

# **2026-08-28 에 이 검사의 내용이 바뀌었다.** 폴리트로프였을 때 토성은 Guillot 예산의
# 아래 끝(Z = 0.200)에서 −0.1 % 로 맞았고, 그 일치가 두 오차의 상쇄였다 — 외피를 세 배
# 부풀리는 관계식과, 그것을 도로 눌러 주는 큰 중원소 분율. 표가 들어오면서 같은 Z 가
# −9.8 % 로 지나쳐 버린다. 그래서 검사할 것은 "예산 안에서 맞는가" 가 아니라
# **예산 밖으로 나갔는가, 그리고 어느 쪽으로** 다. 맞는 Z 는 0.0825 (7.85 M⊕) 이고
# 예산 19–31 M⊕ 아래다. 방향에는 이유가 둘 있고 둘 다 같은 쪽을 민다 — 이 모형에는 핵이
# 없어서 중원소를 전부 외피에 넣어야 하고, 균질 분포는 실제(희석 핵)보다 더 누른다.
SATURN_BUDGET_OVERSHOOT = -0.05   # Z 예산 아래 끝에서 이보다 더 작아야 한다
EXACT = 1e-12            # Z = 0 은 "거의" 가 아니라 정확히 같아야 한다


def _km(res) -> float:
    return res.values["radius"] * EARTH_RADIUS_M / 1e3


# 1-bar 온도. 2026-08-28 부터 이 갈래의 경계조건이다 (Voyager 전파엄폐).
T_1BAR = {"Jupiter": 165.0, "Saturn": 135.0}


def _giant(mass_earth: float, z: float = 0.0, t_pot: float = 165.0):
    return solve(mass_earth, core_mass_fraction=0.0, ice_mass_fraction=0.0,
                 gas_mass_fraction=1.0, body_class="giant", envelope_z=z,
                 potential_temperature=t_pot)


def _z_rows(planet):
    """한 행성을 Z 예산의 양 끝과 몇 눈금에서 푼다."""
    name, m, _r, z_lo, z_hi = planet
    fracs = [z_lo / m, (z_lo + z_hi) / 2 / m, z_hi / m]
    for z in fracs:
        yield z, _giant(m, z, T_1BAR.get(name, 165.0))


def table() -> None:
    """문서 §Validation 의 혼합 표를 다시 낸다. 손으로 친 표는 어긋난다."""
    print("| body | Z (M⊕) | Z fraction | R derived | R mean (IAU) | ΔR | C/MR² | grade |")
    print("|---|---|---|---|---|---|---|---|")
    for planet in (JUPITER, SATURN):
        name, m, r_mean, z_lo, z_hi = planet
        base = _giant(m, 0.0, T_1BAR.get(name, 165.0))
        print(f"| {name} | 0 | 0.000 | {_km(base):.0f} km | {r_mean} km | "
              f"{(_km(base) / r_mean - 1) * 100:+.1f} % | {base.values['nmoi']:.4f} | "
              f"{base.grade} |")
        for z, res in _z_rows(planet):
            if not res.applicable:
                print(f"| {name} | {z * m:.0f} | {z:.3f} | declined | {r_mean} km | – | "
                      f"– | – |")
                continue
            print(f"| {name} | {z * m:.0f} | {z:.3f} | {_km(res):.0f} km | {r_mean} km | "
                  f"{(_km(res) / r_mean - 1) * 100:+.1f} % | {res.values['nmoi']:.4f} | "
                  f"{res.grade} |")


def main() -> int:
    if "--table" in sys.argv:
        table()
        return 0

    fails: list[str] = []

    print("대수 — 규칙이 자기 항등식을 지키는가")
    si, fe, h = MATERIALS["silicate"], MATERIALS["fe_prem"], MATERIALS["h_he"]
    checks = (
        ("성분 하나면 그 재료 자신", mix("t", "t", (si, 1.0)) is si),
        ("분율 0 인 성분은 사라진다", mix("t", "t", (si, 1.0), (fe, 0.0)) is si),
        ("둘이면 Mixture 다", isinstance(mix("t", "t", (si, 0.5), (fe, 0.5)), Mixture)),
    )
    for label, cond in checks:
        if not cond:
            fails.append(f"대수: {label}")
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")

    # 부피 가법이 정말 부피를 더하는가. 손으로 쓴 항등식과 대본다.
    m2 = mix("t", "t", (si, 0.4), (fe, 0.6))
    p = 100e9
    want = 1.0 / (0.4 / si.density(p) + 0.6 / fe.density(p))
    d = abs(m2.density(p) - want) / want
    ok = d < EXACT
    if not ok:
        fails.append(f"부피 가법 항등식이 {d:.1e} 어긋난다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 1/ρ = Σ w/ρ 가 100 GPa 에서 성립 "
          f"({m2.density(p):.1f} kg/m³, 상대차 {d:.0e})")

    # 상한은 **가장 낮은** 성분이 정한다. 높은 쪽을 쓰면 근거 없는 외삽을 숨기게 된다.
    # 2026-08-28 에 그 성분이 바뀌었다 — 폴리트로프의 울타리(13 M_J 의 중심압)가 규산염의
    # 13.5 TPa 위에 있어서 규산염이 정하고 있었는데, 표의 굳힌 창이 10⁴ GPa 이라 이제
    # 수소-헬륨이 정한다. 검사는 소유자 이름이 아니라 **규칙** 을 본다.
    env = mix("t", "t", (h, 0.8), (si, 0.2))
    ok = env.p_max == min(si.p_max, h.p_max)
    if not ok:
        fails.append("혼합 상한이 가장 낮은 성분을 따르지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 혼합 상한 {env.p_max / 1e9:.0f} GPa = "
          f"성분 중 최소 (silicate {si.p_max / 1e9:.0f}, h_he {h.p_max / 1e9:.0f})")

    print("\nZ = 0 — 규칙이 켜지기 전과 정확히 같은 답인가")
    # 여기가 이 작업 전체의 안전선이다. 혼합이 순수 경로로 새면 앵커 다섯이 조용히 움직인다.
    for label, kwargs, want_n in (
            ("지구", dict(mass_earth=1.0, core_mass_fraction=0.325), 0.3297),
            ("달", dict(mass_earth=0.0123, core_mass_fraction=0.019), 0.3945)):
        got = solve(**kwargs).values["nmoi"]
        ok = abs(got - want_n) < 5e-4
        if not ok:
            fails.append(f"{label} C/MR² 가 {got:.4f} 로 움직였다 (기준 {want_n})")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} C/MR² {got:.4f} (기준 {want_n})")
    a, b = _giant(JUPITER[1], 0.0), _giant(JUPITER[1])
    ok = abs(a.values["radius"] - b.values["radius"]) < EXACT
    if not ok:
        fails.append("envelope_z=0 이 기본 호출과 다르다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 목성 envelope_z=0 이 기본 호출과 비트까지 같다 "
          f"({_km(a):.0f} km)")

    print("\n토성 — 이 갈래의 판정선. Guillot 1999 의 Z 예산 안에서 내려오는가")
    name, m, r_mean, z_lo, z_hi = SATURN
    base_off = _km(_giant(m, 0.0)) / r_mean - 1.0
    best = None
    for z, res in _z_rows(SATURN):
        if not res.applicable:
            print(f"  [ ?? ] Z {z:.3f} 거절 — {res.reason[:70]}")
            continue
        off = _km(res) / r_mean - 1.0
        if best is None or abs(off) < abs(best[1]):
            best = (z, off)
        print(f"         Z {z:.3f} ({z * m:.0f} M⊕) → {_km(res):.0f} km "
              f"({off * 100:+.1f} %)")
    ok = best is not None and best[1] < SATURN_BUDGET_OVERSHOOT
    if not ok:
        fails.append("토성이 Guillot 예산의 아래 끝에서 이미 지나쳐야 하는데 그러지 않는다 "
                     "— 폴리트로프의 상쇄가 돌아온 것일 수 있다")
    print(f"  [{'PASS' if ok else 'FAIL'}] Z = 0 에서 {base_off * 100:+.1f} % 였던 것이 "
          f"Guillot 예산 아래 끝 Z = {best[0]:.3f} 에서 {best[1] * 100:+.1f} % 로 "
          f"**지나친다** — 맞는 Z 는 예산 아래에 있다")
    print(f"         폴리트로프였을 때는 같은 Z = {best[0]:.3f} 가 −0.1 % 로 맞았다. 그 "
          f"일치가 두 오차의 상쇄였다는 것이 이 줄의 내용이다. 이 모형에 핵이 없어서 "
          f"중원소를 전부 외피에 넣어야 하고, 균질 분포는 실제(희석 핵)보다 더 누른다.")

    print("\n목성 — Z 를 넣으면 어떻게 되나. 2026-08-27 에 답이 바뀌었다")
    # 직전 판까지 이 절은 **거절** 을 검사했다. 목성 중심이 Z 를 넣으면 4 TPa 를 넘고
    # 규산염 적합이 3.5 TPa 에서 끝났기 때문이다. 규산염이 13.5 TPa 까지 이어지면서
    # 세 눈금이 전부 돌게 됐고, 이 절은 이제 그 결과를 재서 기록한다.
    rows = list(_z_rows(JUPITER))
    ok = all(r.applicable for _z, r in rows)
    if not ok:
        stuck = [(z, r.reason[:80]) for z, r in rows if not r.applicable]
        fails.append(f"목성 Z 가 아직 막힌다: {stuck}")
    print(f"  [{'PASS' if ok else 'FAIL'}] Guillot 구간 세 눈금이 전부 적분된다")
    for z, res in rows:
        if not res.applicable:
            print(f"         Z {z:.4f} 거절 — {res.reason[:80]}")
            continue
        print(f"         Z {z:.4f} ({z * JUPITER[1]:.0f} M⊕) → {_km(res):.0f} km "
              f"({(_km(res) / JUPITER[2] - 1) * 100:+.1f} %) · C/MR² "
              f"{res.values['nmoi']:.4f} · P_c {res.values['core_pressure'] / 1e3:.2f} TPa")
    # 중심압이 옛 천장 위, 새 천장 아래여야 한다. 그게 이 절이 무엇 때문에 열렸는지다.
    pcs = [r.values["core_pressure"] * 1e9 for _z, r in rows if r.applicable]
    ok = bool(pcs) and all(SILICATE_PREM_TO_PV < pc < MATERIALS["silicate"].p_max
                           for pc in pcs)
    if not ok:
        fails.append("목성 Z 의 중심압이 옛 천장과 새 천장 사이에 있지 않다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 중심압 {min(pcs) / 1e12:.2f}~{max(pcs) / 1e12:.2f} TPa "
          f"— 옛 상한 {SILICATE_PREM_TO_PV / 1e12:.1f} TPa 위, 새 상한 "
          f"{MATERIALS['silicate'].p_max / 1e12:.1f} TPa 아래다")
    # **반지름은 나빠진다. 그것도 결과다.** K 는 목성에 맞춰진 상수이고 실제 목성에는
    # Z 가 이미 들어 있으므로, Z 를 또 얹으면 이중계산이 된다.
    off0 = _km(_giant(JUPITER[1], 0.0)) / JUPITER[2] - 1.0
    offs = [_km(r) / JUPITER[2] - 1.0 for _z, r in rows if r.applicable]
    worse = all(abs(o) > abs(off0) for o in offs)
    if not worse:
        fails.append("목성에 Z 를 넣었는데 반지름이 나빠지지 않는다 — 이중계산 진단이 깨졌다")
    print(f"  [{'PASS' if worse else 'FAIL'}] 반지름은 Z = 0 의 {off0 * 100:+.1f} % 에서 "
          f"{min(offs) * 100:+.1f} % 까지 **나빠진다**")
    print(f"         이중계산이라서다. n = 1 의 K 는 Helled+ 2022 가 **실제 목성** 에 맞춘 "
          f"상수이고 실제 목성은 이미 Guillot 의 Z 를 들고 있다. 그 위에 Z 를 또 얹으면 "
          f"중원소가 두 번 들어간다 — 토성에서 Z 가 −0.1 % 로 내려오는 것과 방향이 반대인 "
          f"이유가 그것이다. 토성은 K 가 맞춰진 천체가 아니다.")
    # C/MR² 쪽은 반대로 앵커 밴드 안으로 들어온다. 반지름과 갈리는 것이 요점이라 재둔다.
    ns = [r.values["nmoi"] for _z, r in rows if r.applicable]
    inband = [n for n in ns if JUPITER_NMOI_BAND[0] <= n <= JUPITER_NMOI_BAND[1]]
    print(f"  [보고] C/MR² 는 반대로 움직인다 — Z = 0 의 "
          f"{_giant(JUPITER[1], 0.0).values['nmoi']:.4f} 에서 {min(ns):.4f}~{max(ns):.4f} 로 "
          f"올라가고, {len(inband)}/{len(ns)} 눈금이 앵커 밴드 "
          f"{JUPITER_NMOI_BAND[0]}–{JUPITER_NMOI_BAND[1]} 안에 든다 "
          f"(Neuenschwander+ 2021 ∪ Wahl+ 2017). 반지름과 C/MR² 가 서로 다른 Z 를 "
          f"가리키는 것이고, 그걸 화해시키는 것은 희석 핵이지 이 레시피가 아니다.")

    print("\n규산염 천장 — 이제 어디서 걸리나. 거절 문장이 여전히 정직한가")
    # 천장이 사라진 게 아니라 올라갔다. 올라간 자리에서도 혼합 거절이 순수 재료용
    # 전자축퇴 문장을 쓰면 안 된다 — 섞인 층에서는 성분 하나의 적합이 끝난 것뿐이다.
    huge = _giant(JUPITER[1], 0.75)
    # 이름 대야 하는 것은 **실제로 상한을 정한 성분** 이다. 표가 들어오면서 그게
    # 규산염에서 수소-헬륨으로 옮겨갔고, 거절 문장이 그 이름을 따라가야 한다.
    owner = ENVELOPE_Z_MATERIAL if si.p_max < h.p_max else h.name
    ok = not huge.applicable and owner in huge.reason
    if not ok:
        fails.append(f"천장 위 혼합 거절이 상한 소유자('{owner}')를 이름 대지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] Z = 0.75 는 여전히 거절하고 "
          f"'{ENVELOPE_Z_MATERIAL}' 의 상한을 이름 댄다")
    ok = "성분 하나" in huge.reason and "축퇴가 지배" not in huge.reason
    if not ok:
        fails.append("혼합 상한 거절이 순수 재료용 전자축퇴 문장을 쓴다 — 거짓이다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 그 이유가 전자축퇴가 **아니다** — 섞인 층에서는 "
          f"성분 하나의 적합이 끝난 것이지 축퇴 영역이 아니다")

    print("\n미분화 — 앵커가 없다. 대신 측정값을 가려내는가")
    und = solve(MERCURY_MASS_ME, core_mass_fraction=MERCURY_CMF, differentiated=False)
    ok = und.applicable
    if not ok:
        fails.append(f"미분화 수성이 풀려야 한다 — {und.reason[:70]}")
    else:
        off = (und.values["nmoi"] - MERCURY_NMOI) / MERCURY_NMOI
        ok = off > 0.05
        if not ok:
            fails.append(f"미분화 수성이 측정 C/MR² 와 구분되지 않는다 ({off * 100:+.1f} %)")
        print(f"  [{'PASS' if ok else 'FAIL'}] 미분화 수성 C/MR² {und.values['nmoi']:.4f} · "
              f"측정 {MERCURY_NMOI} ({off * 100:+.1f} %) — 수성이 분화했다고 맞게 말한다")
    print(f"         완전히 섞인 암석-금속 천체의 C/MR² 를 잰 사례는 찾지 못했다. Ceres 와 "
          f"Callisto 는 부분 분화이고 그건 다른 문제다. 그래서 이 값은 앵커가 아니라 "
          f"판별이고, 등급이 analog 다.")

    # 균질한 천체의 집중도는 자기압축만이 정한다 — 무엇으로 만들어졌는지가 아니라.
    # 그건 혼합 규칙의 예측이므로 우연이 아니라 검사 대상이다.
    flat = [solve(1.0, core_mass_fraction=w, differentiated=False).values["nmoi"]
            for w in (0.0, 0.325, 0.70)]
    spread = max(flat) - min(flat)
    ok = spread < 0.002
    if not ok:
        fails.append(f"미분화 C/MR² 가 금속분율에 {spread:.4f} 움직인다 — 평평해야 한다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 금속분율 0.0/0.325/0.70 에서 C/MR² "
          f"{flat[0]:.4f}/{flat[1]:.4f}/{flat[2]:.4f} — 폭 {spread:.4f}. 균질한 천체의 "
          f"집중도는 자기압축이 정하지 조성이 정하지 않는다")

    # 분화한 같은 천체와는 갈려야 한다. 안 갈리면 이 축이 아무것도 안 한 것이다.
    diff = solve(1.0, core_mass_fraction=0.325).values["nmoi"]
    gap = (flat[1] - diff) / diff
    ok = gap > 0.05
    if not ok:
        fails.append(f"미분화와 분화가 {gap * 100:.1f} % 밖에 안 갈린다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 지구 질량·조성에서 미분화 {flat[1]:.4f} 대 "
          f"분화 {diff:.4f} ({gap * 100:+.1f} %) — 핵이 있고 없고가 갈린다")

    print("\n거절 — 규칙 밖은 이름을 대는가")
    for label, kwargs, keyword in (
            ("미분화 + 얼음", dict(mass_earth=1.0, core_mass_fraction=0.3,
                                ice_mass_fraction=0.3, differentiated=False), "부분 분화"),
            ("외피 없는 Z", dict(mass_earth=1.0, core_mass_fraction=0.325,
                              envelope_z=0.2), "외피가 있어야"),
            ("Z 가 범위 밖", dict(mass_earth=120.0, core_mass_fraction=0.0,
                              ice_mass_fraction=0.0, gas_mass_fraction=1.0,
                              body_class="giant", envelope_z=1.0), "[0, 1)")):
        res = solve(**kwargs)
        ok = not res.applicable and keyword in res.reason
        if not ok:
            fails.append(f"{label}: 거절하며 '{keyword}' 를 이름 대야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

    print("\n등급 — 답이 검증할 수 없는 선언에 기대면 내려가는가")
    for label, res, want in (
            # 2026-08-28 부터 거대행성은 전부 analog 다. 포텐셜 온도가 선언이라서이고,
            # 질량이나 앵커 위치 때문이 아니다 (interior.GIANT_ANCHORS 옆 주석).
            ("목성 Z=0", _giant(JUPITER[1], 0.0), "analog"),
            ("토성 Z=0.200", _giant(SATURN[1], 19.0 / SATURN[1]), "analog"),
            ("미분화 지구", solve(1.0, core_mass_fraction=0.325,
                              differentiated=False), "analog")):
        ok = res.grade == want
        if not ok:
            fails.append(f"등급: {label} 가 {res.grade} 다, {want} 여야 한다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} → {res.grade}")
    print(f"         토성이 −0.1 % 로 맞는데도 analog 인 것이 요점이다. 맞은 것은 혼합 "
          f"규칙이지 이 레시피의 예측력이 아니다 — 조성을 논문에서 받아썼다.")

    print(f"\n  부피 가법 혼합의 유효 한계: 정압 부피 편차 "
          f"{AVL_VOLUME_DEVIATION * 100:.0f} % (Vorberger+ 2007, H-He, 분자 해리 구간). "
          f"암석-금속에는 그런 수가 없어서 옮겨 적지 않았다.")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
