# 조석 가열률을 내부 온도·리소스피어 두께로 바꾸는 수송 축 — Kankanamge & Moore 2019 heat-pipe 계
"""Ė → (internal temperature, lithosphere thickness) under a DECLARED transport mode.

    python3 engine/tidal_transport.py            이오 재현 상태와 라벨 예시를 출력

Brief 35 (2026-09-01). 수송 모드는 **선언**이고 도출이 아니다 — Ė(T) 소산 곡선은
평형을 *예측*할 때 필요하고, 주어진 가열률에서 변환을 평가하는 데는 필요 없다.
Kankanamge & Moore 2019 §6이 이오에 대해 하는 것이 정확히 그것이다 ("the internal
heating rate is chosen to satisfy the observed thermal emission"). 우리 Ė도 계산된
입력이므로, 모드를 선언하고 Ė를 주어진 것으로 받으면 계가 닫힌다.

**검증 상태: 실패 (사전등록 분기 ③+④, tidal-interior-context-notes.md §4).**
이 모듈은 Kankanamge & Moore 2019의 인쇄된 계 — eq. (36)+(38), 보조식 (1)–(21),
Table 1 — 를 축자 전사해 기계 잔차(~1e-14)까지 푼다. 전사는 PDF 텍스트 레이어로
축자 대조했다. 그런데 논문 자신의 이오 결과(1471 K, 12.6 km)는 자연 독법의 상수
어디에서도 재현되지 않고, (1471 K, 12.6 km)이 인쇄된 계의 근이 되는 상수를 정확히
역산하면 α = 8.71e-7 1/K (암석의 ~1/34), ΔT_rh = 354 K (암석 유변 스케일 ~40–100 K의
수 배)라는 비물리 값이 나온다. 논문의 무차원 Tables 2–4도 인쇄된 식과 행별 정합이
깨진다(복원되는 잠열 L이 행마다 0.3→10.8로 표류). 그러므로 여기서 나오는 수는
**unvalidated 라벨을 달고 측정으로만** 쓰인다. 채택 금지.

숫자는 라벨 없이 들어오지 않는다. 이 파일의 모든 상수는 출처 위치·조건을 달고,
채워 넣은 값(α)은 채워 넣었다고 말한다.
"""
from __future__ import annotations

import math

# ── Kankanamge & Moore 2019 (2019JGRE..124..114K, doi 10.1029/2018JE005800) ──
# Table 1 (그들의 수치실험 적합):
A_RH = 2.4    # Kankanamge & Moore 2019 Table 1, a_rh (Solomatov 1995; Solomatov & Moresi 2000)
A_C = 1.7     # Kankanamge & Moore 2019 Table 1, a_c (Solomatov & Moresi 2000)
A_U = 0.63    # Kankanamge & Moore 2019 eq. 21 아래 본문, a_u — 그들 자신의 적합 (Figure 3)

# Table 5 (이오 적용, §6) — 축자 전사. 주의: α(열팽창계수)는 Table 5에 **없다**.
# §6은 "Material parameter values are typical mantle rock values from Schubert et
# al. (2001)"로 위임한다. 아래 ALPHA_SCHUBERT가 그 채움값이다.
IO_TABLE5 = dict(
    g=1.8,            # m/s², Table 5
    D=1.0e6,          # m (1000 km 맨틀 깊이), Table 5
    T_s=100.0,        # K 표면온도, Table 5
    T_sol0=1395.0,    # K 표면 솔리더스 (Hirschmann 2000), Table 5
    dTsol=0.362e-3,   # K/m 솔리더스 기울기 (Hirschmann 2000, 2 GPa에서), Table 5
    rho=3000.0,       # kg/m³, Table 5
    c_p=1000.0,       # J/(kg K), Table 5
    L=5.0e5,          # J/kg 융해 잠열, Table 5
    H=3.0e-6,         # W/m³ 부피 가열률, Table 5 — 유효숫자 1자리 인쇄.
                      # §6의 인쇄 플럭스(F_m 2.5 + F_c 0.009)는 HD=2.509를 함의한다(노트 §4).
    k=4.0,            # W/(m K), Table 5
    eta0=1.0e17,      # Pa s 기준 점성, Table 5
    T0=1400.0,        # K 기준 온도, Table 5
    alpha=3.0e-5,     # 1/K — **채워 넣은 값** (Schubert, Turcotte & Olson 2001의 맨틀 대표값;
                      # Table 5에 α가 없어 §6의 위임을 따라 채움. 노트 §2 ①)
)

# Table 5의 A = 15는 인쇄된 단위가 없다(노트 §2 ②). 자연 독법 후보 —
# eq. 1의 Frank-Kamenetskii 선형화 A = E/(R·T₀²), T₀ = 1400 K (Table 5):
A_KARATO_WET = 240e3 / (8.314 * 1400.0**2)   # = 0.01473 1/K; E = 240 kJ/mol 습윤 감람석
                                             # (Karato & Wu 1993 — 논문이 유변학에 인용)
A_KARATO_DRY = 300e3 / (8.314 * 1400.0**2)   # = 0.01841 1/K; E = 300 kJ/mol 건조 감람석

# (1471 K, 12.6 km)을 인쇄된 계의 정확한 근으로 만드는 유일한 상수쌍 — 역산 결과
# (test_tidal_transport.py가 고정). 비물리적이라는 사실 자체가 분기 ③의 산출물이다.
RECOVERED_A = 2.82403e-3      # 1/K → ΔT_rh = 354.1 K. 암석 유변 온도 스케일이 아니다.
RECOVERED_ALPHA = 8.71415e-7  # 1/K. 맨틀 암석 α(2–4e-5)의 ~1/34.
RECOVERED_H = 2.509e-6        # W/m³ = §6 인쇄 플럭스가 함의하는 HD/D (F_m + F_c 폐합).

# 인쇄된 이오 결과 (§6) 와 사전등록 허용오차 (노트 §3, 실행 전 커밋 e719b5d7):
IO_PRINTED_T = 1471.0     # K
IO_PRINTED_DELTA = 12.6e3  # m
IO_TOL_T = 21.0           # K  (§5: 내부온도 상대오차 "<1.4%")
IO_TOL_DELTA = 1.9e3      # m  (초록: "<15%")

# §6.2 세 모드 사다리 (tidal-heating-methodology.md §6.2) — 선언 메뉴.
TRANSPORT_MODES = ("heat-pipe", "stagnant-lid", "plate-tectonics")


def residuals(p: dict, A: float, T_i: float, delta: float):
    """인쇄된 계의 잔차 — eq. (36)·(38)과 등가인 안정화 형태.

    원식의 c₁·exp(+ρC_p v δ/k) 항은 근에서 멀면 지수 폭발 × 근접 상쇄로 평가
    불능이라, (36)에서 c₁을 해석적으로 소거해 exp(−Pe)만 남긴 등가형을 쓴다.
      rA = HD − F_m − G − (F_conv − G)·e^{−Pe}          [W/m², eq. 36 재배열]
      rB = Hδ/(ρC_p v) + (F_conv−G)(1−e^{−Pe})/(ρC_p v)
           + T_s − [T_sol0 + (dT_sol/dz)(δ+δ_rh) − a_rh·ΔT_rh]   [K, eq. 37+17에 36 대입]
    근에서 두 형태는 비트까지 같은 해를 갖는다(대수 동치).
    """
    dT_rh = 1.0 / A                                        # eq. 3
    eta = p['eta0'] * math.exp(max(-700.0, min(700.0, -A * (T_i - p['T0']))))  # eq. 1
    kappa = p['k'] / (p['rho'] * p['c_p'])
    Dd = p['D'] - delta
    if Dd <= 0:
        return None
    Ra = p['rho'] * p['g'] * p['alpha'] * dT_rh * Dd**3 / (kappa * eta)        # eq. 5
    if Ra <= 0:
        return None
    d_rh = (A_RH / A_C) * Dd * Ra**(-1.0/3.0)              # eq. 9
    v_m = A_U * kappa / Dd * math.sqrt(Ra)                 # eq. 13 (a_u 적합)
    dT_m = T_i - p['T_sol0'] - p['dTsol'] * (delta + d_rh)  # eq. 16·17의 멜트존 강하
    if dT_m <= 0:
        return None                                        # 멜트 없음 — heat-pipe 불성립
    v = p['c_p'] * v_m * dT_m / p['L']                     # eq. 21
    Tmid = 0.5 * (T_i + p['T_sol0'] + p['dTsol'] * (delta + d_rh))  # eq. 19
    F_m = p['rho'] * v * (p['L'] + p['c_p'] * (Tmid - p['T_s']))    # eq. 20
    F_conv = p['k'] * A_RH * dT_rh / d_rh                  # eq. 6 = eq. 36 첫 항
    rcv = p['rho'] * p['c_p'] * v
    Pe = rcv * delta / p['k']
    G = p['k'] * p['H'] / rcv
    HD = p['H'] * p['D']
    emP = math.exp(-min(Pe, 700.0))
    rA = HD - F_m - G - (F_conv - G) * emP
    rB = (p['H'] * delta / rcv + (F_conv - G) * (1.0 - emP) / rcv + p['T_s']
          - (p['T_sol0'] + p['dTsol'] * (delta + d_rh) - A_RH * dT_rh))
    return rA, rB, dict(Ra=Ra, d_rh=d_rh, v_m=v_m, dT_m=dT_m, v=v, F_m=F_m,
                        F_conv=F_conv, Pe=Pe, G=G, dT_rh=dT_rh,
                        F_c=HD - F_m)


def _newton(p, A, T0g, d0g):
    """감쇠 뉴턴 다듬기. 정규화: rA는 HD, rB는 100 K."""
    T_i, d = T0g, d0g
    HD = p['H'] * p['D']

    def norm(r):
        return abs(r[0]) / HD + abs(r[1]) / 100.0

    r = residuals(p, A, T_i, d)
    if r is None:
        return None
    for _ in range(120):
        if abs(r[0]) < 1e-10 * HD and abs(r[1]) < 1e-8:
            return T_i, d
        hT = max(1e-7 * abs(T_i), 1e-5)
        hd = max(1e-7 * abs(d), 1e-4)
        rT = residuals(p, A, T_i + hT, d)
        rd = residuals(p, A, T_i, d + hd)
        if rT is None or rd is None:
            return None
        J = [[(rT[0] - r[0]) / hT, (rd[0] - r[0]) / hd],
             [(rT[1] - r[1]) / hT, (rd[1] - r[1]) / hd]]
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        if det == 0:
            return None
        dT = -(r[0] * J[1][1] - r[1] * J[0][1]) / det
        dd = -(-r[0] * J[1][0] + r[1] * J[0][0]) / det
        lam, cur, stepped = 1.0, norm(r), False
        while lam > 1e-8:
            Tn, dn = T_i + lam * dT, d + lam * dd
            if dn <= 0 or dn >= p['D'] or Tn <= p['T_sol0']:
                lam *= 0.5
                continue
            rn = residuals(p, A, Tn, dn)
            if rn is not None and norm(rn) < cur:
                T_i, d, r = Tn, dn, rn
                stepped = True
                break
            lam *= 0.5
        if not stepped:
            return None
    return None


def all_roots(p: dict, A: float, t_span: float = 800.0):
    """(T_i, δ) 평면 부호 스캔 + 뉴턴으로 인쇄된 계의 근을 전부 나열한다.

    단일-가지 이분법은 첫 근만 잡고 일부 A에서 근을 통째로 놓쳤다(노트 §4).
    """
    NT, ND = 200, 140
    Ts = [p['T_sol0'] + 0.1 + t_span * (i / NT)**1.5 for i in range(NT + 1)]
    log_lo, log_hi = 2.0, math.log10(p['D'] * 0.999)
    ds = [10.0**(log_lo + (log_hi - log_lo) * j / ND) for j in range(ND + 1)]
    S = {}
    for i, T in enumerate(Ts):
        for j, d in enumerate(ds):
            r = residuals(p, A, T, d)
            S[(i, j)] = None if r is None else (1 if r[0] > 0 else -1,
                                                1 if r[1] > 0 else -1)
    roots = []
    for i in range(NT):
        for j in range(ND):
            cell = [S[(i, j)], S[(i + 1, j)], S[(i, j + 1)], S[(i + 1, j + 1)]]
            if any(c is None for c in cell):
                continue
            if len({c[0] for c in cell}) > 1 and len({c[1] for c in cell}) > 1:
                s = _newton(p, A, 0.5 * (Ts[i] + Ts[i + 1]),
                            math.sqrt(ds[j] * ds[j + 1]))
                if s is None:
                    continue
                if not any(abs(s[0] - r0) < 0.05 and abs(s[1] - r1) < max(1.0, 1e-3 * r1)
                           for r0, r1 in roots):
                    roots.append(s)
    return sorted(roots, key=lambda x: x[1])


def stability_label(rheology_pairing: str) -> dict:
    """Rovira-Navarro+ 2021 (2021PSJ.....2..119R)의 안정성 라벨.

    본문: "In both cases, there is a stable equilibrium point" — 불안정점은
    Maxwell+대류 조합에서만 하나 더 붙고, 저자들은 Andrade를 채택한다. 불안정점에
    앉은 천체는 "enters a runaway cooling phase". 분기(多价)는 방법의 성질이 아니라
    한 유변 조합의 성질이지만, 라벨은 항상 반환한다 — 맨 온도가 아니라 라벨 붙은 결과.
    """
    if rheology_pairing == "andrade":
        return dict(label="stable",
                    basis="Andrade 유변에서 평형점은 하나이고 안정 "
                          "(Rovira-Navarro+ 2021, 'In both cases, there is a stable equilibrium point'; 그들의 채택 유변)")
    if rheology_pairing == "maxwell+convection":
        return dict(label="conditionally-stable",
                    basis="Maxwell+대류 조합에서만 불안정 동반 평형점이 존재; 그 점에 앉은 "
                          "천체는 'enters a runaway cooling phase' (Rovira-Navarro+ 2021)")
    raise ValueError(f"미등록 유변 조합: {rheology_pairing!r} — andrade | maxwell+convection")


def transport_result(surface_flux_wm2: float, radius_m: float, *,
                     mode: str = "heat-pipe",
                     rheology_pairing: str = "andrade",
                     mantle_depth_m: float | None = None,
                     params: dict | None = None,
                     A: float = A_KARATO_WET) -> dict:
    """선언된 수송 모드 아래 Ė/면적 → 라벨 붙은 (내부 온도, 리소스피어 두께).

    `surface_flux_wm2` = Ė/(4πR²). 나오는 온도·두께는 **도출값**(derived-from-Ė)로
    라벨되지만, 이 축의 검증(이오 재현)이 실패했으므로 validation.status =
    "failed-io-reproduction"이 항상 붙는다 — 측정으로만 쓰고 채택하지 말 것.
    수송 모드와 맨틀 깊이는 선언이고 라벨에 그렇게 적힌다.
    """
    if mode not in TRANSPORT_MODES:
        raise ValueError(f"미등록 수송 모드: {mode!r} — {TRANSPORT_MODES}")
    validation = dict(
        status="failed-io-reproduction",
        note="Kankanamge & Moore 2019 인쇄 계는 자연 독법 상수로 자신의 이오 결과"
             "(1471 K, 12.6 km)를 재현하지 못한다 — tidal-interior-context-notes.md §4. "
             "기제(브리프 37, §7): 모형이 애초에 무차원이고 Table 5는 집필 시점의 "
             "재차원화라 폐합이 차원 표현에 없다 (§2 'T₀ (= 1)' 대 Table 5 '1400 K'). "
             "아래 수는 측정 전용, 채택 금지.")
    if mode != "heat-pipe":
        return dict(mode=dict(value=mode, provenance="declared"),
                    internal_temperature=None, lithosphere_thickness=None,
                    stability=stability_label(rheology_pairing),
                    validation=validation,
                    note="이 축이 푸는 것은 heat-pipe 변환뿐 — 다른 모드는 "
                         "tidal-heating-methodology.md §6.2의 용량 사다리로 판정만 한다.")
    p = dict(params or IO_TABLE5)
    D = mantle_depth_m if mantle_depth_m is not None else 0.549 * radius_m
    # 0.549 = Table 5의 이오 설정 D/R = 1000 km / 1821.6 km — 선언이고 라벨에 남는다.
    p['D'] = D
    p['H'] = surface_flux_wm2 / D                           # F_s = H·D (eq. 23)
    roots = all_roots(p, A)
    if not roots:
        return dict(mode=dict(value=mode, provenance="declared"),
                    internal_temperature=None, lithosphere_thickness=None,
                    stability=stability_label(rheology_pairing),
                    validation=validation,
                    note="인쇄된 계에 근 없음 (heat-pipe 선언이 이 입력에서 불성립 — "
                         "멜트존이 안 열리거나 (36)+(38) 동시해가 없다).")
    T_i, delta = roots[0]
    aux = residuals(p, A, T_i, delta)[2]
    return dict(
        mode=dict(value=mode, provenance="declared"),
        mantle_depth=dict(value_m=D,
                          provenance="declared" if mantle_depth_m is not None
                          else "declared (D/R = 0.549, Table 5 이오 설정 비율)"),
        internal_temperature=dict(value_K=T_i, provenance="derived-from-Edot",
                                  source="Kankanamge & Moore 2019 eqs. (36)+(38)"),
        lithosphere_thickness=dict(value_m=delta, provenance="derived-from-Edot",
                                   source="Kankanamge & Moore 2019 eqs. (36)+(38)"),
        melt_flux=dict(value_wm2=aux['F_m'], provenance="derived-from-Edot",
                       source="Kankanamge & Moore 2019 eq. (20)"),
        conductive_flux=dict(value_wm2=aux['F_c'], provenance="derived-from-Edot"),
        n_roots=len(roots),
        stability=stability_label(rheology_pairing),
        validation=validation,
    )


def derive_potential_temperature(surface_flux_wm2: float, radius_m: float, **kw) -> dict:
    """조석 가열 천체의 potential_temperature 도출 — 선언이 도출값이 되는 자리.

    지금 솔버의 potential_temperature는 세 번째 선언이다(interior.py). 이 함수가
    그 값을 Ė에서 도출하되, 출력은 **어느 쪽인지** 반드시 말한다 — 수만 보면 도출과
    선언이 구별되지 않기 때문이다. 검증 실패 라벨이 그대로 실려 간다.
    """
    r = transport_result(surface_flux_wm2, radius_m, **kw)
    if r.get('internal_temperature') is None:
        return dict(potential_temperature=None, provenance="derived-from-Edot (근 없음)",
                    validation=r['validation'])
    return dict(potential_temperature=r['internal_temperature']['value_K'],
                provenance="derived-from-Edot — 선언 아님; Kankanamge & Moore 2019 "
                           "eqs. (36)+(38), 선언된 heat-pipe 모드 아래",
                validation=r['validation'],
                stability=r['stability'])



# ── 로스터 측정 입력 — 손 타이핑 금지, 출처에서 읽는다 (브리프 35 후속 ③) ──────────
# 같은 실수가 두 번 났다: 작업 세션이 단테에 기각된 900 km 초안의 플럭스(11,500)를
# 채택 반지름(521 km)과 짝지었고, 감사 세션은 하데스에서 천체별 g·T_s를 빼먹었다.
# 손으로 값을 타이핑하는 자리가 결함원이므로, 값은 정본 파일에서 읽고 짝의
# 자기일관성을 실행 전에 검사한다 — 안 맞으면 이름을 대고 거절한다.
#
# 정본 선택 (기록 의무):
#   Dante — docs/reference/tidal-heating-methodology.md §6.5 표 (지휘석 확인, 2026-09-01).
#     phase4 보드는 내부 분열 상태다: decisions의 radius 행은 521 km(채택)인데 moons
#     블록은 900 km 초안(mass 8.0e21)을 그대로 들고 있고, bulk.tidal_heating 행도
#     11,500 W/m²(900 km의 값)를 든다 — 단테 반지름 건이 오너 결정 대기라 보드가 아직
#     안 고쳐진 것. §6.5 표가 짝이 맞는 유일한 출처다 (521 → 78× → 2,231 W/m²).
#   Hades — phase4/alpha_centauri.yaml: bulk.tidal_heating 행(207 W/m²) +
#     surface_temperature 행(278 K) + moons 블록(M 5.0e21 kg, R 750 km).
#     하데스는 반지름 재설계가 없었어서 보드가 자기일관이다.
# 보드는 읽기 전용 — 반지름 건은 오너 결정 대기.

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_METHODOLOGY = _ROOT / "docs" / "reference" / "tidal-heating-methodology.md"
_BOARD = _ROOT / "phase4" / "alpha_centauri.yaml"
_G_NEWTON = 6.674e-11
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def _sci(mant: str, sup: str) -> float:
    return float(mant) * 10.0 ** int(sup.translate(_SUP))


def _pairing_check_dante(R_m, M_kg, F_wm2, rho, F_draft, R_draft_m) -> None:
    """짝 자기일관성 — 실패는 이름을 대고 거절한다."""
    scaled = F_wm2 * (R_draft_m / R_m) ** 3
    if abs(scaled - F_draft) > 0.01 * F_draft:
        raise ValueError(
            f"짝 자기일관성 실패 (Dante): F ∝ R³ 검산이 어긋난다 — "
            f"{F_wm2:.0f} W/m² × ({R_draft_m/1e3:.0f}/{R_m/1e3:.0f})³ = {scaled:.0f}, "
            f"초안 행은 {F_draft:.0f}. 반지름과 플럭스가 다른 설계의 것이다")
    m_rho = rho * (4.0 / 3.0) * math.pi * R_m ** 3
    if abs(m_rho - M_kg) > 0.01 * M_kg:
        raise ValueError(
            f"짝 자기일관성 실패 (Dante): 질량 {M_kg:.3e} ≠ ρ·(4/3)πR³ = {m_rho:.3e} "
            f"(ρ = {rho:.0f}) — 질량·밀도·반지름이 같은 행의 것이 아니다")


def _pairing_check_hades(R_m, M_kg, F_wm2, x_io) -> None:
    rho = M_kg / ((4.0 / 3.0) * math.pi * R_m ** 3)
    if not 2000.0 <= rho <= 4000.0:
        raise ValueError(
            f"짝 자기일관성 실패 (Hades): M/R³ 밀도 {rho:.0f} kg/m³ 가 암석 대역(2000–4000) "
            f"밖 — 보드의 'Moon-sized rocky body' 와 모순")
    io_power = F_wm2 * 4.0 * math.pi * R_m ** 2 / x_io
    if not 0.9e14 <= io_power <= 1.1e14:
        raise ValueError(
            f"짝 자기일관성 실패 (Hades): {F_wm2:.0f} W/m² × 4πR²/{x_io:.0f} = 이오 출력 "
            f"{io_power:.2e} W — 이오 전지구 열류 ~1e14 W (Veeder 2012 차수) 밖. "
            f"플럭스와 반지름이 짝이 아니다")


def roster_inputs() -> dict:
    """정본 파일에서 (값, 출처)를 함께 읽고 짝 검사를 통과시킨 로스터 측정 입력."""
    text = _METHODOLOGY.read_text(encoding="utf-8")
    ad = re.search(r"\| \*\*521 km \(adopted\)\*\* \| \*\*([\d.]+)×10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)\*\* "
                   r"\| \*\*(\d+)×\*\* \| \*\*([\d,]+) W/m²\*\*", text)
    dr = re.search(r"\| 900 km \(drafted\) \| ([\d.]+)×10([⁰¹²³⁴⁵⁶⁷⁸⁹]+) \| ([\d,]+)× Io "
                   r"\| ([\d,]+) W/m²", text)
    rho = re.search(r"density at ([\d,]+) kg/m³", text)
    ts = re.search(r"plains at their external-budget (\d+) K", text)
    if not (ad and dr and rho and ts):
        raise ValueError("§6.5 표를 못 읽었다 — tidal-heating-methodology.md 의 워크드 예제가 "
                         "옮겨졌거나 형식이 바뀌었다. 정본 위치부터 확인할 것")
    R_d, M_d = 521e3, _sci(ad.group(1), ad.group(2))
    F_d = float(ad.group(4).replace(",", ""))
    rho_d = float(rho.group(1).replace(",", ""))
    _pairing_check_dante(R_d, M_d, F_d, rho_d, float(dr.group(4).replace(",", "")), 900e3)

    import yaml
    board = yaml.safe_load(_BOARD.read_text(encoding="utf-8"))
    F_h = Ts_h = x_io = None
    for row in board.get("decisions") or []:
        if row.get("body") != "Hades":
            continue
        for f in row.get("fields") or []:
            if f.get("name") == "tidal_heating" and row.get("axis") == "bulk.tidal_heating":
                m = re.search(r"~(\d+)× Io \((\d+) W/m²", str(f.get("value")))
                if m:
                    x_io, F_h = float(m.group(1)), float(m.group(2))
            if f.get("name") == "surface_temperature" and isinstance(f.get("value"), (int, float)):
                Ts_h = float(f["value"])
    M_h = R_h = None

    def _walk(node):
        nonlocal M_h, R_h
        if isinstance(node, dict):
            if node.get("name") == "Hades" and "mass_kg" in node:
                M_h, R_h = float(node["mass_kg"]), float(node["radius_km"]) * 1e3
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for v in node:
                _walk(v)
    _walk(board)
    if None in (F_h, Ts_h, M_h, R_h):
        raise ValueError(f"보드에서 Hades 입력을 못 읽었다 (F={F_h}, T_s={Ts_h}, M={M_h}, R={R_h})")
    _pairing_check_hades(R_h, M_h, F_h, x_io)

    return {
        "Dante (A b I)": dict(
            radius_m=R_d, mass_kg=M_d, flux_wm2=F_d, T_s=float(ts.group(1)),
            g=_G_NEWTON * M_d / R_d ** 2,
            source="docs/reference/tidal-heating-methodology.md §6.5 표 (정본; 채택 행 "
                   "521 km · 1.552e21 kg · 2,231 W/m², ρ 2,620, 평원 223 K)"),
        "Hades (A b II)": dict(
            radius_m=R_h, mass_kg=M_h, flux_wm2=F_h, T_s=Ts_h,
            g=_G_NEWTON * M_h / R_h ** 2,
            source="phase4/alpha_centauri.yaml (정본; bulk.tidal_heating 207 W/m² + "
                   "surface_temperature 278 K + moons 블록 M 5.0e21 · R 750 km)"),
    }


def roster_measurement() -> dict:
    """로스터 천체를 축에 통과시킨 측정 — 채택 아님, unvalidated 라벨 그대로."""
    out = {}
    for name, inp in roster_inputs().items():
        p = dict(IO_TABLE5)
        p["g"] = inp["g"]
        p["T_s"] = inp["T_s"]
        r = transport_result(inp["flux_wm2"], inp["radius_m"], params=p)
        r["inputs"] = inp
        out[name] = r
    return out

if __name__ == '__main__':
    p = dict(IO_TABLE5)
    print("이오, Table 5 축자 + α=3e-5 (Schubert 채움), 자연 독법 A 두 개:")
    for A, name in [(A_KARATO_WET, "Karato&Wu 습윤 240 kJ/mol"),
                    (A_KARATO_DRY, "Karato&Wu 건조 300 kJ/mol")]:
        for T_i, d in all_roots(p, A):
            aux = residuals(p, A, T_i, d)[2]
            print(f"  A={A:.5f} ({name}): T_i={T_i:.1f} K, δ={d/1e3:.1f} km "
                  f"(인쇄값 1471 K·12.6 km, 허용 ±21 K·±1.9 km → 불일치)")
    p2 = dict(IO_TABLE5, alpha=RECOVERED_ALPHA, H=RECOVERED_H)
    for T_i, d in all_roots(p2, RECOVERED_A):
        print(f"  역산 상수(비물리): T_i={T_i:.2f} K, δ={d/1e3:.3f} km — 인쇄값과 일치, "
              f"그러나 α·ΔT_rh가 암석이 아니다")
