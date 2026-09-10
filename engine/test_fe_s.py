# C55 1단계 테스트 — Xu+ 2021 이 인쇄한 Fe–S 부피 규칙 전사와, ρ₀ 가 없어 거절하는 자리 (브리프 178 B)
"""Anchors for the printed liquid Fe–S rules, and for the refusal that stands in for the density.

    python3 engine/test_fe_s.py        # the gate; ~0 s, this is arithmetic on two printed formulas

⚠ **This file's most important row is a refusal.** The owner decided to build a binary Fe–S material
first (C55, 2026-09-10), and Xu+ 2021 prints two of the three things a `Phase` needs — `K₀(X_S)` and
`K′(X_S)` — but **not `ρ₀(X_S)`** anywhere. Recovering it from Table 1's 7 GPa values by inverting their
eq. (3) would be *our* arithmetic, and this repository's rule is that a paper's printed derivation wins
over ours. So the material is **not built**, the attempt
refuses by name, and the reproduction anchors R4–R6 (the paper's own Fe–S density points) are registered
as **refusals** rather than as numbers.

⚠ **The first version of this file said the refusal would be filled when Table S1 arrived. The SI
arrived and that table does not exist**: what it holds is an end-member EOS and Margules coefficients,
because the paper's composition dependence is a non-ideal solution model rather than a
(ρ₀, K₀, K′) triple. So candidate B is not waiting on a document — it does not fit the `Phase` slot at
all, and the material that gets built is candidate A (Huang 2023, whose SI *does* print composition
derivatives at two Mars-core anchors).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eos                                # noqa: E402
import interior                           # noqa: E402

fails = 0


def _plant_floor(p_min: float) -> str:
    """`fe_prem` 을 베껴 바닥만 옮긴 재질을 등록하고 이름을 준다 (판정선 ⓒ)."""
    import dataclasses
    base = eos.MATERIALS["fe_prem"]
    ph = dataclasses.replace(base.phases[0], p_min=p_min)
    name = f"planted_{p_min / eos.GPA:.0f}gpa"
    eos.MATERIALS[name] = dataclasses.replace(
        base, name=name, phases=(ph,) + base.phases[1:])
    return name


def _shoot_gap(cmf: float, material: str, mass_kg: float = 0.1074 * 5.97219e24):
    """쏘아 본다. 거절하면 그 `PhaseGap`, 풀리면 None.

    ⚠ `shoot` 을 부른다. `_shoot_pressure` 를 직접 부르면 «답이 적합 밖이면 거절» 하는 자리를
    건너뛰어, 엔진이 안 내놓을 수를 시험만 통과시키게 된다 (C60 (c))."""
    try:
        interior.shoot(mass_kg, cmf, 0.0, material, potential_temperature=1600.0)
    except eos.PhaseGap as gap:
        return gap
    return None


def _shoot_ok(cmf: float, material: str, mass_kg: float = 0.1074 * 5.97219e24) -> bool:
    return _shoot_gap(cmf, material, mass_kg) is None


def _consumer_ok(cmf: float, material: str = "fe_s_13wt_19gpa") -> bool:
    """노드가 실제로 받는 층(`interior.solve`)이 이 조성을 답으로 내는가.

    `solve` 는 `core_material` 을 인자로 안 받고 조성 프리셋에서 읽으므로 이름 하나를 잠깐
    등록했다 지운다. 프리셋 표 자체는 안 바뀐다."""
    interior.COMPOSITIONS["_c55_probe"] = (cmf, 0.0, 0.0, material)
    try:
        res = interior.solve(0.1074, composition="_c55_probe",
                             potential_temperature=1600.0, body_class="rocky")
    finally:
        interior.COMPOSITIONS.pop("_c55_probe", None)
    return bool(res.applicable)


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


print("① 인쇄된 두 규칙의 끝점 — 논문의 상수가 그대로 나오는가 (Xu+ 2021 §2.4)")
row(eos.xu_fes_k0_pa(0.0) == 76.0 * eos.GPA,
    f"X_S = 0 → K₀ = {eos.xu_fes_k0_pa(0.0) / eos.GPA:.1f} GPa · 인쇄 «K_Fe = 76 GPa»")
row(eos.xu_fes_k0_pa(1.0) == 1.6 * eos.GPA,
    f"X_S = 1 → K₀ = {eos.xu_fes_k0_pa(1.0) / eos.GPA:.1f} GPa · 인쇄 «K_S = 1.6 GPa»")
row(eos.xu_fes_k0p(0.0) == 6.5 and eos.xu_fes_k0p(1.0) == 9.5,
    f"K′ = 6.5 + 3·X_S → 끝점 {eos.xu_fes_k0p(0.0)} · {eos.xu_fes_k0p(1.0)} (인쇄 «K′_Fe = 6.5», 계수 3)")

mid = eos.xu_fes_k0_pa(0.30)
row(abs(mid - (76.0 ** 0.70) * (1.6 ** 0.30) * eos.GPA) < 1.0,
    f"X_S = 0.30 → K₀ = {mid / eos.GPA:.4f} GPa — 지수 혼합을 여기서 다시 계산한 값과 같다 "
    "(전사가 규칙이지 표가 아니라는 뜻)")

print("\n② 어휘가 실재한다 — 원자분율 밖은 거절한다")
for bad in (-0.01, 1.01):
    try:
        eos.xu_fes_k0_pa(bad)
        row(False, f"X_S = {bad} 가 통과했다")
    except ValueError as e:
        row("원자분율" in str(e), f"X_S = {bad} → 거절 «{str(e)[:44]}…»")

print("\n③ ⚠ 등록된 거절 — ρ₀ 가 인쇄되지 않아 재질을 짓지 않는다 (이것이 오늘의 기대 결과다)")
try:
    eos.iron_fes_phase(0.30)
    row(False, "상이 만들어졌다 — ρ₀ 없이 만들어졌다면 어딘가에서 수를 지어낸 것이다")
except eos.PhaseGap as e:
    msg = str(e)
    row("Table S1" in msg and "우리 산수" in msg,
        f"거절이 **무엇이 없는지** 이름을 댄다: Table S1 · 역산 금지 사유 — «{msg[:60]}…»")
    row("형식 불일치" in msg or "슬롯에 애초에 들어가지 않는다" in msg,
        "그리고 **기다림이 아니라 형식 불일치**라고 말한다 — SI 는 도착했고 그 표는 없었다")

print("\n④ 융해 바운드는 이미 있고, 19 GPa 는 등록된 공백이다 (Mori+ 2017)")
row(eos.iron_fes_eutectic_t_melt(19.0e9) is None,
    "19 GPa → None. 화성 CMB 압력대의 아래쪽이 Mori 의 기준점(21 GPa) 밖이라 **공백이 답이다**")
row(abs(eos.iron_fes_eutectic_t_melt(21.0e9) - 1348.0) < 1e-9,
    f"21 GPa → {eos.iron_fes_eutectic_t_melt(21.0e9):.1f} K (식 (1) 의 기준점 그대로)")
row("10–21 GPa" in eos.IRON_FES_GAP_REASON,
    "그 공백은 이름과 이유를 이미 갖고 있다 (`IRON_FES_GAP_REASON`) — 이 브리프가 만든 것이 아니다")

print("\n⑤ 기존 두 철은 손대지 않았다")
fp = eos.MATERIALS["fe_prem"].phases[0]
fe = eos.MATERIALS["fe_eps"].phases[0]
row(fp.rho0 == 7050.0 and fp.k0 == 201.0 * eos.GPA and fp.fit_state == "liquid",
    f"fe_prem ρ₀ {fp.rho0:.0f} · K₀ {fp.k0 / eos.GPA:.0f} GPa · {fp.fit_state} — 그대로")
row(fe.fit_state == "solid" and "fe_s" not in eos.MATERIALS,
    "fe_eps 도 그대로이고, **`fe_s` 는 아직 MATERIALS 에 없다** — 지어지지 않았다는 사실이 "
    "레지스트리에서도 참이다")

print("\n⑥ 후보 A — Huang+ 2023 의 인쇄된 조성 도함수로 그 논문의 산수를 그대로 한다")
# R1·R2 — 순수 액체 Fe 의 두 기준점이 c_S = 0 에서 그대로 나와야 한다 (Table 1).
for anchor, rho, kt in (("19GPa", 8.083, 156.0), ("35GPa", 8.640, 215.0)):
    row(eos.huang_fes_density(0.0, anchor) == rho and eos.huang_fes_k_t_gpa(0.0, anchor) == kt,
        f"R1/R2 {anchor}: c_S = 0 → ρ {eos.huang_fes_density(0.0, anchor):.3f} g/cm³ · "
        f"K_T {eos.huang_fes_k_t_gpa(0.0, anchor):.0f} GPa — Table 1 인쇄값 그대로")

# R7 — Table S4 의 **독립** AIMD 점. 논문 자신이 NSP/SP 두 값을 인쇄하므로 그 사이가 통과다.
c4 = eos.HUANG_S4_CS
r7 = eos.huang_fes_density(c4)
mid = (eos.HUANG_S4_RHO_NSP + eos.HUANG_S4_RHO_SP) / 2.0
row(eos.HUANG_S4_RHO_NSP <= r7 <= eos.HUANG_S4_RHO_SP and abs(r7 - mid) / mid <= 0.025,
    f"R7 Fe₈₄S₂₄ (c_S = {c4:.4f}): 혼합식이 {r7:.4f} g/cm³ — 인쇄된 NSP {eos.HUANG_S4_RHO_NSP} 와 "
    f"SP {eos.HUANG_S4_RHO_SP} **사이**이고 중점에서 {abs(r7 - mid) / mid * 100:.2f} % (통과선 2.5 %)")

# R8·R9 — 적분이 닫힌 형과 같은가. 여기서 다시 적분해 대조한다(전사가 규칙임을 보이는 자리).
for anchor in ("19GPa", "35GPa"):
    a, b = eos.HUANG_S_DRHO[anchor]
    c = 0.18
    steps = 20000
    num = sum((a * (i + 0.5) * c / steps + b) * (c / steps) for i in range(steps))
    closed = eos.huang_fes_density(c, anchor) - eos.HUANG_FE_ANCHORS[anchor][2]
    row(abs(num - closed) / abs(closed) <= 0.01,
        f"R8/R9 {anchor}: c_S = 0.18 에서 수치적분 {num:+.5f} 대 닫힌 형 {closed:+.5f} g/cm³ "
        f"({abs(num - closed) / abs(closed) * 100:.4f} %, 통과선 1 %)")

row(eos.HUANG_S_DRHO["19GPa"] == (-3.505, -5.362) and eos.HUANG_S_DKT["19GPa"] == (-410.0, -228.0),
    "Table S5 의 S 열이 인쇄된 계수 그대로다 (19 GPa: ρ −3.505c−5.362 · K_T −410c−228)")
row("몰분율" in eos.HUANG_FES_SLOT_GAP or "고압 기준 BM2" in eos.HUANG_FES_SLOT_GAP,
    "⚠ 아직 `Phase` 슬롯에는 안 들어간다 — 이유가 이름을 갖고 있다: 이 재질의 기준점이 "
    "**19/35 GPa** 인데 `Phase.rho0` 는 영압 기준이다")

print("\n⑦ 고압 기준 BM2 — 새 form (브리프 179). ⚠ **아래 둘은 항등식이지 시험이 아니다**")
# ⚠ 감사석이 먼저 짚었다: BM2 는 정의상 자기 기준점에서 ρ_ref 를 돌려주므로, 앵커마다 상을 하나씩
#   만들어 «Table 1 의 두 점을 재현했다» 고 말하면 아무 것도 시험하지 않은 것이다. 그래서 여기서는
#   **form 이 기준을 옳은 자리에 놓았는지**(항등식이 실제로 성립하는지)만 보고, 진짜 시험은 위 ⑥ 의
#   **R7 — 독립 AIMD 점** 하나뿐임을 적어 둔다.
ph = eos.huang_fes_phase(eos.HUANG_S4_CS, "19GPa")
row(ph.form == "bm2_ref" and ph.p_ref == 19.0 * eos.GPA and ph.k0p == 4.0,
    f"상이 만들어진다: form {ph.form} · p_ref {ph.p_ref / eos.GPA:.0f} GPa · K′ {ph.k0p} "
    "(논문: «second-order BM … K₀′ equals 4»)")
row(abs(ph.pressure(ph.rho0) - ph.p_ref) < 1.0,
    f"기준점의 항등식: P(ρ_ref) = {ph.pressure(ph.rho0) / eos.GPA:.6f} GPa = p_ref — "
    "고압 기준이 실제로 그 자리에 놓였다는 뜻이다")
# ⚠ 저장값과 평가값은 **다른 단정**이다: 앞은 비트 동일, 뒤는 Newton 이 기준점을 다시 푸는
#   잔차라 3 ulp 가 남는다. 한 줄로 뭉치면 form 이 잘못 풀어도 «같다» 로 통과할 수 있다.
rel = abs(ph.density(19.0e9) - ph.rho0) / ph.rho0
row(rel <= 1e-12,
    f"평가값도 기준점으로 돌아온다: ρ(19 GPa) 상대잔차 {rel:.2e} ≤ 1e-12 (3 ulp 수준) — "
    "수치 역산이 기준을 다시 찾는다는 뜻이지 저장값이 같다는 뜻이 아니다")
row(repr(ph.rho0 / 1e3) == "6.804901234567901",
    f"슬롯에 **들어간** R7 이 함수와 마지막 자리까지 같다: {ph.rho0 / 1e3!r} g/cm³ "
    "(c_S = 24/108 을 반올림하면 여기가 갈린다 — 실제로 첫 판이 0.222 로 갈렸다)")
row(ph.melt == "iron_fes_eutectic" and ph.fit_state == "liquid" and ph.melt_scale == 1.0,
    "융해는 Mori 공정 **바운드**이고 `melt_scale` 은 쓰지 않는다 (내림폭이 곧 공정선이다)")

# 기존 상은 이 form 을 안 쓰므로 비트까지 그대로여야 한다.
row(repr(eos.MATERIALS["fe_prem"].phases[0].density(136.0e9)) == "9916.93698295698",
    f"fe_prem ρ(136 GPa) = {eos.MATERIALS['fe_prem'].phases[0].density(136.0e9)!r} — 비트 동일")
# ⚠ `MATERIALS` 에는 `phases` 가 없는 항목도 있다 (수소-헬륨 표) — 있는 것만 본다.
# ⚠ 그리고 «전부 0» 은 이제 거짓이다: 178 C 가 Fe–S 두 끝을 등록했고 그것들이 19 GPa 기준이다.
#   그래서 **이름으로 갈라** 본다 — 새 재질만 기준압을 갖고, 나머지는 전부 0 이어야 한다.
newref = sorted(k for k, m in eos.MATERIALS.items()
                if any(ph2.p_ref for ph2 in getattr(m, "phases", ())))
# ⚠ **기준선이 183 에서 움직였다**: 상자의 여덟 모서리도 같은 19 GPa 기준이라 이제 열이다.
#   이름으로 가르는 규칙은 그대로 — 기준압을 갖는 것은 «Huang 앵커에 놓인 액체 핵» 뿐이다.
_REFD = sorted(["fe_s_13wt_19gpa", "fe_s_19wt_19gpa"] + list(eos.CORE_BOX_MATERIALS))
row(newref == _REFD,
    f"기준압을 갖는 재질은 Huang 앵커의 액체 핵 {len(_REFD)} 뿐이다 (178 C 의 둘 + 183 의 여덟)")
row(all(ph2.p_ref == 0.0 for k, m in eos.MATERIALS.items()
        if k not in set(_REFD) for ph2 in getattr(m, "phases", ())),
    "그 열 말고는 모든 상의 `p_ref` 가 0 이다 — 새 필드가 옛 경로를 지나가지 않는다")

print("\n⑧ 융해곡선이 **분기까지** 있는가 — 라벨만 있으면 순수 철로 떨어진다 (브리프 178 C′)")
# ⚠ 178 C 는 `melt="iron_fes_eutectic"` 라벨을 붙였고 `MELT_CURVE_JOIN` 에도 등재했지만,
#   `Material.t_melt` 의 분기는 water/silicate/**나머지 → iron** 이라 그 라벨이 **순수 철의
#   융해온도**로 떨어지고 있었다. 오늘 값이 아무 데도 안 쓰였을 뿐 C37 의 모양 그대로다.
#   그래서 이 시험은 **라벨이 아니라 `Material.t_melt` 를 부른다.**
mat = eos.MATERIALS["fe_s_13wt_19gpa"]
for p_gpa, want in ((19.0, None), (20.65, None),
                    (25.0, 1417.448733427824), (35.0, 1576.9034966680556)):
    got = mat.t_melt(p_gpa * eos.GPA)
    ok = (got is None) if want is None else (got is not None and repr(got) == repr(want))
    row(ok, f"{p_gpa:>5} GPa → {got!r} (기대 {want!r})"
        + ("  — 공백이라 None, 그 None 이 거절로 이어진다" if want is None else ""))

# ⚠ 그리고 **등재된 곡선 이름 전부**가 실제 분기를 갖는지 본다. 분기가 없으면 순수 철로 떨어지므로,
#   철이 아닌 이름이 25 GPa 에서 `iron_t_melt` 와 같은 값을 내면 그것은 «분기 없음» 의 서명이다.
p25 = 25.0 * eos.GPA
iron25 = eos.iron_t_melt(p25)
unwired = []
for key in sorted(eos.MELT_CURVE_JOIN):
    if key == "iron":
        continue
    probe = eos.Material(f"probe_{key}", key,
                         (eos.Phase(f"probe_{key}", "bm2", 7000.0, 100.0 * eos.GPA, 4.0,
                                    400.0 * eos.GPA, "probe", melt=key),))
    v = probe.t_melt(p25)
    if v is not None and iron25 is not None and abs(v - iron25) < 1e-9:
        unwired.append(key)
row(not unwired,
    f"`MELT_CURVE_JOIN` 의 이름 {len(eos.MELT_CURVE_JOIN)}개가 전부 자기 분기를 갖는다 "
    f"(순수 철로 떨어지는 이름: {unwired or '없음'})")

# ⚠ 그리고 분기 없는 이름은 **이름을 대며 멈춘다** — 조용히 철로 떨어지지 않는다는 것을 직접 건다.
ghost = eos.Material("probe_ghost", "probe",
                     (eos.Phase("probe_ghost", "bm2", 7000.0, 100.0 * eos.GPA, 4.0,
                                400.0 * eos.GPA, "probe", melt="zz_no_branch"),))
try:
    ghost.t_melt(p25)
    row(False, "분기 없는 곡선 이름이 값을 냈다 — 그게 이 브리프가 고친 결함이다")
except eos.PhaseGap as e:
    row("분기가 없다" in str(e), f"분기 없는 이름 → 이름 대며 거절: «{str(e)[:66]}…»")

print("\n⑨ 10–21 GPa 는 곡선이 아니라 **괄호**다 (브리프 178 D)")
row(eos.iron_fes_eutectic_bracket(20.65 * eos.GPA) == (1023.0, 1473.0),
    f"20.65 GPa (화성 CMB) → 괄호 {eos.iron_fes_eutectic_bracket(20.65 * eos.GPA)} K — "
    "창 안 인쇄값의 최저·최고이고 압력으로 보간하지 않는다")
row(eos.iron_fes_eutectic_bracket(25.0 * eos.GPA) is None
    and eos.iron_fes_eutectic_bracket(5.0 * eos.GPA) is None,
    "창 밖(25 · 5 GPa)에는 괄호가 없다 — 21 GPa 위는 단일 곡선이 답하고 10 GPa 아래는 아무도 안 답한다")
row(eos.iron_fes_phase_verdict(2000.0, 20.65 * eos.GPA) == "liquid",
    "화성의 선언 T_c 2000 K 는 괄호 위끝 1473 K 보다 높다 → **liquid**, 걸치지 않는다 (등록된 예측)")
row(eos.iron_fes_phase_verdict(900.0, 15.0 * eos.GPA) == "solid",
    "양끝 아래면 solid")
row(eos.iron_fes_phase_verdict(1100.0, 15.0 * eos.GPA).startswith("cannot-say"),
    "⚠ 괄호를 걸치면 **cannot-say** — 걸침을 한쪽으로 밀지 않는 것이 이 괄호의 존재 이유다")
grades = {g for _p, _t, g in eos.IRON_FES_WINDOW_LOW_POINTS}
row(grades == {"본문 · Si 2 at% 장입", "본문 · Si 없음"},
    f"하한 세 점이 장입까지 구별해 등급을 든다: {sorted(grades)}")
row([g for _p, _t, g in eos.IRON_FES_WINDOW_LOW_POINTS][1] == "본문 · Si 없음",
    "⚠ Si 없는 점은 **가운데**(18.5 GPa) 하나뿐이다 — 괄호의 양끝은 둘 다 Si 장입이다")

print("\n⑩ 하한 미만 거절이 자기 문구를 갖는다 (브리프 178 E)")
try:
    eos.MATERIALS["fe_s_13wt_19gpa"].phase_at(5.0 * eos.GPA)
    row(False, "기준 아래에서 값을 냈다")
except eos.PhaseGap as e:
    msg = str(e)
    row("기준압 19 GPa 아래" in msg and "융해" not in msg.split("⚠")[0],
        f"5 GPa → 압력 바닥을 말한다 (융해가 아니라): «{msg[:70]}…»")
row(eos.Material.under_reason is not eos.Material.gap_reason,
    "`under_reason` 과 `gap_reason` 은 다른 문구다 — 바닥 아래와 상 **사이** 는 다른 사실이다")

print("\n⑪ 시행 중의 도메인 거절은 바디 판정이 아니다 (C60 (a), 브리프 181)")
row(eos.MATERIALS["fe_prem"].shoot_lo == 0.0
    and eos.MATERIALS["fe_s_13wt_19gpa"].shoot_lo == 19.0 * eos.GPA,
    f"`shoot_lo` 는 가장 안쪽 상의 바닥이다 — fe_prem 0 · fe_s "
    f"{eos.MATERIALS['fe_s_13wt_19gpa'].shoot_lo / eos.GPA:.0f} GPa")
row(eos.MATERIALS["fe_s_13wt_19gpa"].t_melt_band(20.65 * eos.GPA) == (1023.0, 1473.0)
    and eos.MATERIALS["fe_s_13wt_19gpa"].t_melt_band(30.0 * eos.GPA) is None
    and eos.MATERIALS["fe_prem"].t_melt_band(100.0 * eos.GPA) is None,
    "`t_melt_band` 는 창 안에서만 폭을 주고 나머지는 None — `t_melt` 의 반환형은 안 넓혔다")
_p = 20.65 * eos.GPA
row(isinstance(eos.MATERIALS["fe_prem"].t_melt(_p), float)
    and eos.MATERIALS["fe_s_13wt_19gpa"].t_melt(_p) is None,
    "⚠ 소비자 **열 자리**(호출 열하나)가 쓰는 `t_melt` 는 오늘과 같은 값·같은 형을 준다 — 밴드는 별도 접근자로만")

_MARS_KG = 0.1074 * 5.97219e24
row(all(_shoot_ok(c, "fe_s_13wt_19gpa") for c in (0.24, 0.27, 0.29, 0.295, 0.30, 0.303)),
    "ⓑ cmf 0.24–0.303 에서 Fe–S 가 중심에서 CMB 까지 걸어 나온다 (사격층) — 걸음 **안**의 자리는 바닥 값으로 "
    "읽고, 판정은 **프로파일에 적히는 것**에 대고 한다 (181 B)")
_cut_ok = _shoot_ok(0.302, "fe_s_13wt_19gpa")
_cut_gap = _shoot_gap(0.305, "fe_s_13wt_19gpa")
row(_cut_ok and _cut_gap is not None,
    "⚠ 자르는 자리가 **CMB 가 19 GPa 를 지나는 지점**이다 — 0.302 는 P_cmb 19.01809 GPa 로 풀리고 "
    "0.305 부터 거절한다. 클램프 자리가 아니라 경계 자리다 (C60 (c) 의 정정)")
row(_consumer_ok(0.302) and not _consumer_ok(0.303),
    "⚠ **소비 경로(`solve`)의 자르는 자리는 한 칸 앞이다** — 두 층이 기록하는 CMB 가 약 0.5 kPa "
    "어긋나고 19 GPa 바로 위에서 그 폭이 판정을 가른다. 살아남는 마지막 cmf 는 **0.302** 이고, "
    "0.303 은 사격층에서만 풀린다 (감사석 실측, 181 B)")
_gap325 = _shoot_gap(0.325, "fe_s_13wt_19gpa")
row(_gap325 is not None and "수렴한 답" in _gap325.reason,
    f"⚠ cmf 0.325 는 거절한다 (⚠ **화성이 선언한 값이 아니다** — C59 (a)) — **핵이 제 질량 몫을 "
    f"채우고도 기록된 경계가** {_gap325.pressure_pa / eos.GPA:.4f} GPa 로 적합의 기준 아래다. "
    "잘림 검사만으로는 못 잡는 자리이고, «바닥이 핵질량비를 고른다» 는 181 의 결론은 **철회됐다**")
row(_consumer_ok(0.24, "fe_s_13wt_19gpa") and _consumer_ok(0.24, "fe_s_19wt_19gpa"),
    "⚠ **화성이 실제로 선언한 cmf 0.24 에서는 Fe–S 두 재질이 다 풀린다** — 0.24 는 자름 자리 0.302 "
    "아래다. C60 (b) 가 «선언된 조성은 거절한다» 고 적은 것은 프리셋의 0.325 를 화성의 선언으로 "
    "읽은 탓이다 (C59 (a))")
row(all(_shoot_ok(c, "fe_s_13wt_19gpa", mass_kg=0.5 * 5.97219e24)
        for c in (0.20, 0.30, 0.40)),
    "⚠ 질량 축 — 0.5 M⊕ 는 cmf 0.20·0.30·0.40 이 전부 풀린다 (P_cmb 86.9–72.5 GPa). 바닥 근처가 "
    "아닌 천체에서는 이 규칙이 한 번도 발화하지 않는다")
_planted = _plant_floor(30.0 * eos.GPA)
_gap30 = _shoot_gap(0.325, _planted)
row(_gap30 is not None and "30.0000 GPa" in _gap30.reason,
    f"ⓒ 심은 `p_min` 30 GPa 재질은 여전히 이름을 대고 거절한다: «{_gap30.reason[:52]}…»")

print("\n⑫ 다원계 상자 — 인쇄된 도함수로 여덟 끝점을 우리가 다시 계산한다 (C55 2단계, 브리프 183)")
#: 병렬석 P21 §1 의 표. **받아쓴 것이 아니라 대조 상대**다 — 아래 행은 우리 코드가 낸다.
P21 = ((13, 1, 0.5, 6.737, 93.8, 7.454, 179.7), (13, 1, 1.4, 6.681, 96.2, 7.386, 186.2),
       (13, 4, 0.5, 6.382, 72.4, 7.147, 172.7), (13, 4, 1.4, 6.339, 75.2, 7.091, 179.0),
       (19, 1, 0.5, 6.244, 67.7, 7.045, 162.2), (19, 1, 1.4, 6.206, 71.0, 6.991, 169.1),
       (19, 4, 0.5, 5.934, 49.1, 6.774, 156.8), (19, 4, 1.4, 5.906, 52.6, 6.730, 163.4))
_off = []
for _S, _O, _C, _r19, _k19, _r35, _k35 in P21:
    _x = eos.core_mole_fractions({"S": _S / 100, "O": _O / 100, "C": _C / 100})
    _got = (eos.huang_core_density(_x, "19GPa"), eos.huang_core_k_t_gpa(_x, "19GPa"),
            eos.huang_core_density(_x, "35GPa"), eos.huang_core_k_t_gpa(_x, "35GPa"))
    if not (abs(_got[0] - _r19) < 6e-4 and abs(_got[2] - _r35) < 6e-4
            and abs(_got[1] - _k19) < 6e-2 and abs(_got[3] - _k35) < 6e-2):
        _off.append(f"S{_S}O{_O}C{_C}")
row(not _off, f"ⓑ 여덟 끝점이 인쇄 자릿수까지 재현된다 (두 좌석, 같은 도함수, 불일치 {len(_off)})")
row(abs(eos.huang_core_density(eos.core_mole_fractions({"S": 0.19, "O": 0.01, "C": 0.014}), "19GPa")
        - 6.2056) < 5e-4,
    "⚠ 경계 행 19/1/1.4 = 6.2056 — 창 위끝 6.2 를 **0.0056** 넘는다. 인쇄 도함수의 유효자리 아래라 "
    "«밖» 이 아니라 **경계**로 기록한다 (사전등록 ⓒ)")
#: ⚠ `len(MATERIALS)` 로 세지 않는다 — 위 ⓒ 행이 심은 가짜 재질이 그 표에 들어가 있어서 수가
#: 시험 순서에 달린다. 세는 것은 **상자 자신**이고, 기존 열셋은 이름으로 확인한다.
_BASE13 = ("fe_prem", "fe_eps", "fe_s_13wt_19gpa", "fe_s_19wt_19gpa", "silicate",
           "silicate_chondritic", "antigorite", "h2o", "h_he", "h2o_hot", "h2o_liquid",
           "h2o_liquid_dense", "nh3")
row(len(eos.CORE_BOX_MATERIALS) == 8 and all(n in eos.MATERIALS for n in _BASE13)
    and not (set(_BASE13) & set(eos.CORE_BOX_MATERIALS)),
    f"상자의 여덟 모서리가 **기존 열셋 옆에** 등재됐다 — 겹치는 이름 0")
_box = eos.MATERIALS["fe_s19_o4_c5permil_19gpa"]
row(_box.has_thermal and _box.phases[0].t_ref == 2100.0,
    f"⚠ ⓓ **열 상수를 든다** — `has_thermal` 이 참이고 `t_ref` 가 앵커의 2100 K 다. α 만 붙이고 "
    "`t_ref` 를 비우는 것이 C56 이 기록한 함정이고, 둘을 **함께** 적는 것이 그 함정을 피하는 길이다")
row(bool(_box.melt_free_phases()) and _box.t_melt(25.0 * eos.GPA) is None,
    "⚠ ⓓ **녹는곡선은 없다** — Fe–Fe₃S 공정선은 이원계의 것이고 다원계 인쇄 곡선은 보유 집합에 "
    "없다. 이름만 달지 않으므로 `melt_free_phases()` 가 이 상을 들고, 소비처가 그 이름으로 거절한다")
row(eos.MATERIALS["fe_s_13wt_19gpa"].has_thermal is False
    and eos.MATERIALS["fe_s_19wt_19gpa"].has_thermal is False,
    "ⓐ 이원계 두 재질은 **손대지 않았다** — 여전히 `has_thermal = False` 이고 열세 재질의 격자가 "
    "바이트동일이다 (새 열 상수는 새 빌더에만 붙는다)")

print("\n기록 — 178 D 의 정정을 181 이 다시 정정한다")
print("      178 D 는 «괄호로는 아무 칸도 안 열린다, 막는 것은 압력 바닥이다» 로 끝났고 그것은 맞았다.")
print("      181 이 그 바닥을 다뤘고, 칸에 처음으로 수가 들어왔다. 181 B 가 그 표를 **밴드로** 다시 쟀다 —")
print("      cmf 0.30·0.302 에서 13 wt% 의 핵 반지름 1828.0·1832.0 km 는 **창 안**(1820–1870)이고,")
print("      밀도 7.52 는 창(5.7–6.3) **밖**이다. ⚠ 축이 하나였다면 이 재질이 화성 핵을 맞춘다고")
print("      읽혔을 자리다 — C55 가 두 축을 다 들고 다니기로 한 이유가 이것이다.")
print("      밀도가 창 위로 벗어나는 방향은 Huang+ 2023 자신이 적은 «19 GPa 에서 이 결손을 메우려면")
print("      이원계는 S 가 최소 20 wt% 필요» 와 같고, 핵 밀도는 핵 크기가 아니라 재질이 정하므로")
print("      어느 cmf 에서도 가까워지지 않는다. tools/c55_cells.py 가 이 표를 낸다.")

print("\n기록 — 두 앵커를 서로에게 외삽하면 2.9 % 벌어진다 (판정 아님, 179 측정)")
a19, a35 = eos.huang_fes_phase(eos.HUANG_S4_CS, "19GPa"), eos.huang_fes_phase(eos.HUANG_S4_CS, "35GPa")
print(f"      19 GPa 앵커를 35 GPa 로 밀면 {a19.density(35.0e9):.1f} kg/m³, "
      f"35 GPa 앵커 자신은 {a35.rho0:.1f} — {abs(a19.density(35.0e9) - a35.rho0) / a35.rho0 * 100:.1f} %.")
print("      ⚠ 이것은 **우리 오차가 아니라 논문 자신의 두 적합 사이의 폭**이다. 어느 쪽이 맞는지는")
print("      이 파일이 말하지 않는다 — 화성 CMB 압력대(19–40 GPa)가 두 앵커를 다 지나므로, 어느")
print("      앵커로 푸느냐가 곧 선택이고 그 선택은 판정 칸에서 재야 한다 (C55).")

print("\n기록 — 재현 앵커 R4–R6 은 오늘 **거절**이 기대 결과다 (판정 아님)")
print("      Xu+ 2021 의 Fe–S 밀도점들과 대조하려면 ρ₀(X_S) 가 있어야 하는데, 그 논문은 그것을 표로")
print("      인쇄하지 않고 비이상 용액 모델의 출력으로 낸다 — 슬롯이 아니라 형식이 다르다.")
print("      순수 Fe 쪽 앵커(Huang+ 2023 의 19 GPa/2100 K ρ 8083 · K_T 156)는 **다른 기준점**에")
print("      놓여 있어 이 두 규칙(1 bar · 1900 K)과 직접 비교되지 않는다 — 비교하려면 둘 중 하나를")
print("      옮겨야 하고 그 옮김이 곧 우리 산수다. 그래서 여기서도 수로 만들지 않는다.")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
