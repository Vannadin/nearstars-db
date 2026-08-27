# 뜨거운 조밀한 물 P(ρ,T) — 액체·플라스마·초이온을 한 적합으로. 얼음거대행성 외피가 이걸 먹는다
"""Pressure of hot dense water, from Mazevet+ 2019's analytic free-energy fit.

    from water_hot import pressure

    pressure(rho=3.0e3, t=5000.0)    → Pa. 천왕성 얼음 맨틀쯤

**왜 별도의 재료인가.** 이 저장소의 물 사다리(eos.py 의 ice_ih … ice_x)는 전부 응축상
고체이고 20 ~ 1800 K 에서 끝난다. 얼음거대행성의 '얼음' 맨틀은 그 위에서 시작해 위로
간다 — 깊은 내부가 100 GPa 에서 5000 ~ 7000 K, 중심이 천왕성 5700 K · 해왕성 5500 K 다
(Scheibe+ 2019). 겹치는 구간이 없으므로 사다리를 늘리는 것이 아니라 **다른 상** 을 들이는
것이고, 그래서 파일이 갈린다.

**출처.** Mazevet, Licari, Chabrier & Potekhin 2019, A&A 621, A128
(arXiv:1810.05658). 그들이 헬름홀츠 자유에너지를 해석적으로 적합해 "liquid and plasma
regimes and extending to the super-ionic and gas regimes" 를 한 형태로 덮었고, 초록이
"valid for the entire density range relevant to planetary modeling ... and for temperatures
below 50,000K" 라고 적는다. Scheibe+ 2019 가 천왕성·해왕성 모형을 이 EOS 위에 세운다.

**논문이 아니라 저자들의 참조 구현에서 옮겼다.** 논문 본문이 중밀도 항(F_low)의 명시적
형태를 싣지 않아서, 정본은 논문이 URL 로 가리키는 eoswater21.f 다
(http://www.ioffe.ru/astro/H2O/). 그 파일이 2021-08-18 수정을 달고 있고 그 수정이 논문
버전보다 나중이므로, 여기 상수는 전부 그 구현에서 왔다.

**페르미 적분은 그 구현을 따르지 않았다.** 참조는 Antia 1993 의 Padé 근사로 계산하는데
계수표가 270개쯤이고 전부 물과 무관한 수치 라이브러리다. Padé 는 그 함수의 1993년
포트란용 근사이지 정본이 아니고, 정본은 닫힌 정적분이다. 그래서 fermi.py 가 정의를 쓴다 —
사정과 측정된 오차(4.5e-7)가 그 파일에 있다.

**압력과 내부에너지를 옮겼다. 해석적 미분은 옮기지 않았다.** 참조는 비열과 두 로그미분을
닫힌 형태로 낸다. 여기서는 그 셋을 P 와 U 의 유한차분으로 얻는다 — 적분기가 요구하는 것이
ρ(P,T) 와 단열 기울기뿐이고, 미분 사슬을 손으로 옮기면 검산할 수 없는 코드가 길어진다.
유한차분의 몫은 아래 gruneisen 주석에 적었다.

**이 이식이 맞는지는 주장이 아니라 검사 대상이다.** 논문이 자기 적합의 액체-기체 임계점을
683 K · 0.331 g/cc 로 적어 두었고(실측은 647 K · 0.322), 이 이식이 683.1 K · 0.3305 g/cc 를
낸다. 그 하나가 분자항·혼합함수·이상항을 한꺼번에 짚는다. 저밀도 극한이 이상기체로
가는 것과, 유효전하 Z* 를 논문 eq. (9) 와 참조 구현 양쪽에서 따로 읽어 맞춰 보는 것이
나머지 둘이다. test_water_hot.py 가 셋을 다 돌린다.
"""
from __future__ import annotations

import math

from fermi import f_half, f_three_half, inverse_f_half

# ── 참조 구현의 상수 ────────────────────────────────────────────────────
# 전부 eoswater21.f 의 H2OFIT parameter 문에서 왔다. 주석의 단위도 그 파일의 것이다.
UN_T6 = 0.3157746          # 1 a.u. 온도 = 0.3157746 MK
Z_MEAN = 10.0 / 3.0        # 분자당 전자수 / 원자핵수
CMI_MEAN = 18.0 / 3.0      # 평균 원자량 (H2O 18 을 핵 3 개로)
DENS_CONV = 11.20587 * CMI_MEAN     # ρ[g/cc] → n_i[a.u.]
TNK_CONV = 8.31447e13 / CMI_MEAN    # n_i kT [erg/cc] = TNK_CONV·ρ·T6
A_VDW = 2.357              # van der Waals a [a.u.]
B_VDW = 340.8              # van der Waals b [a.u.]
# 유효전하 Z* 의 적합 상수. 논문 eq. (9) 와 같은 수다.
P1, P3, P4, P5, P7, P8 = 2.35, 5.9, 3.78, 17.0, 1.5, 0.09
# 분자항의 온도 보정과, 분자/플라스마를 잇는 페르미 함수의 상수.
QW, PW, PQ = 0.00123797, 2.384, 1.5
Q1, Q2, Q4 = 0.4, 90.0, 4.0
# 내부에너지에만 붙는 보정항. 압력에는 들어가지 않는다 (참조 구현의 F_T 항).
TCRIT_AU = 0.00205         # 임계온도 647.15 K 를 Ha 로
PC1, PC2, PC3, PC4 = 0.0069, 0.0031, 0.00558, 0.019

# 이 적합이 유효한 범위. 초록과 §3.1 이 적는 것이고, 우리가 고른 울타리가 아니다.
T_MAX = 50000.0            # K. "for temperatures below 50,000K"
RHO_MIN = 0.5e3            # kg/m³. 이 아래는 기체·이상해리 영역이고 같은 절이
                           # "less reliable in the domain of thermal ionization and
                           #  dissociation" 이라고 적는다
RHO_MAX = 100.0e3          # kg/m³. TFMD 와 맞춰 본 상한 (100 g/cc)
# **얼음 사다리와 겹치는 구간에서는 이 적합을 쓰지 않는다.** 같은 절이 스스로
# "limited applicability for the ice VII and ice X phases that occurs at T ≲ 2000 K in the
# range (0.02-0.5) Mbar ≲ P ≲ 3 Mbar" 라고 적고, 그 구간의 불일치를 "tens percent" 로
# 부른다. 그래서 이 재료는 1800 K 위에서만 쓰이고, 아래는 얼음 사다리가 받는다.
T_MIN = 1800.0             # K. eos.py 의 ICE_VII_X_T_MAX 와 같은 자리


def _electron_free_energy(dens_e: float, temp: float) -> tuple[float, float]:
    """이상 전자 페르미 기체의 (F/N_e kT, P/n_e kT). 참조의 ELECNR 그대로다."""
    cle = math.sqrt(2.0 * math.pi / temp)          # 전자 열파장 [a.u.]
    f_dens = math.sqrt(math.pi) * cle ** 3 * dens_e / 4.0
    chi = inverse_f_half(f_dens)                    # 화학포텐셜 μ_e/kT
    u_id = f_three_half(chi) / f_dens
    p_id = u_id / 1.5
    return chi - p_id, p_id


def _z_effective(rs: float, game: float, want_t: bool = False):
    """유효전하 Z* 와 d ln Z*/d ln ρ (그리고 want_t 면 d ln Z*/d ln T 도).

    논문 eq. (9) 와 참조 구현이 같은 함수를 적는다 — 두 출처가 독립으로 같은 상수를 주고,
    test_water_hot.py 가 그 일치를 검사한다."""
    game_sq = math.sqrt(game)
    zna = 1.0 + P8 / rs / game_sq
    zna1rs = -P8 / rs / game_sq
    zna1g = 0.5 * zna1rs
    znb = P1 * rs / zna
    znb1rs = znb * (1.0 - zna1rs / zna)
    znb1g = -znb * zna1g / zna
    znc = 1.0 + P5 / game
    zne = P3 * rs ** P4 / znc ** P7
    zne1rs = P4 * zne
    zne1g = zne * P7 / znc * P5 / game
    zn = 1.0 + znb + zne
    zn1rs = znb1rs + zne1rs
    zn1g = znb1g + zne1g
    zn1r = (zn1g - zn1rs) / 3.0        # d ZN / d ln ρ
    if want_t:
        return Z_MEAN / zn, -zn1r / zn, zn1g / zn
    return Z_MEAN / zn, -zn1r / zn


def pressure(rho: float, t: float) -> float:
    """압력 [Pa]. ρ 는 kg/m³, T 는 K.

    참조 구현의 압력 경로를 그대로 따른다 — 이상 이온항 + 분자항과 플라스마항을 페르미
    함수로 섞은 비이상항이다."""
    rho_cgs = rho / 1.0e3
    t6 = t / 1.0e6
    temp = t6 / UN_T6                   # T [a.u.]
    dens_i = rho_cgs / DENS_CONV        # 핵 수밀도 [a.u.]
    dens_mol = dens_i / 3.0
    rs = (0.75 / math.pi / dens_i / Z_MEAN) ** (1.0 / 3.0)
    game = 1.0 / rs / temp

    # 1. 초이온·플라스마 항
    zef, zdr = _z_effective(rs, game)
    fe, pe = _electron_free_energy(dens_i * zef, temp)
    f_si = fe * zef
    p_si = pe * (1.0 + zdr) * zef + fe * zef * zdr

    # 2. 비이상 분자 항 (van der Waals + ρ~1 g/cc 보정)
    c_w = 1.0 + (QW / temp) ** PW
    b_pq = (B_VDW * dens_mol) ** PQ
    f_mol = (-A_VDW * dens_mol / temp + B_VDW * dens_mol + b_pq * c_w / PQ) / 3.0
    p_mol = (-A_VDW * dens_mol / temp + B_VDW * dens_mol + b_pq * c_w) / 3.0

    # 3. 둘을 잇는다. 섞는 무게가 ρ 와 T 의 함수라 압력에 항이 하나 더 붙는다.
    x = Q4 * math.log(Q1 * rho_cgs + Q2 * temp)
    y_low = 1.0 if x < -40.0 else (0.0 if x > 40.0 else 1.0 / (1.0 + math.exp(x)))
    y_high = 1.0 - y_low
    x1r = Q4 * Q1 * rho_cgs / (Q1 * rho_cgs + Q2 * temp)
    yh1r = y_high * y_low * x1r
    p_nonideal = p_mol * y_low + p_si * y_high + (f_si - f_mol) * yh1r

    # 4. 이상 이온 항, 그리고 단위
    p_over_nkt = p_nonideal + 1.0 / 3.0
    return p_over_nkt * TNK_CONV * rho_cgs * t6 * 0.1     # erg/cc → Pa


def internal_energy(rho: float, t: float) -> float:
    """비내부에너지 [J/kg]. 단열 기울기가 이걸 먹는다 (비열이 여기서 나온다)."""
    rho_cgs = rho / 1.0e3
    t6 = t / 1.0e6
    temp = t6 / UN_T6
    dens_i = rho_cgs / DENS_CONV
    dens_mol = dens_i / 3.0
    rs = (0.75 / math.pi / dens_i / Z_MEAN) ** (1.0 / 3.0)
    game = 1.0 / rs / temp

    zef, zdr, zdt = _z_effective(rs, game, want_t=True)
    fe, pe = _electron_free_energy(dens_i * zef, temp)
    u_e = pe * 1.5                       # UEid = PEid·1.5
    f_si = fe * zef
    u_si = -((-u_e + pe * zdt) * zef + fe * zef * zdt)

    c_w = 1.0 + (QW / temp) ** PW
    c_w1t = -PW * (QW / temp) ** PW
    b_pq = (B_VDW * dens_mol) ** PQ
    f_mol = (-A_VDW * dens_mol / temp + B_VDW * dens_mol + b_pq * c_w / PQ) / 3.0
    u_mol = -(A_VDW * dens_mol / temp + b_pq * c_w1t / PQ) / 3.0

    x = Q4 * math.log(Q1 * rho_cgs + Q2 * temp)
    y_low = 1.0 if x < -40.0 else (0.0 if x > 40.0 else 1.0 / (1.0 + math.exp(x)))
    y_high = 1.0 - y_low
    x1t = Q4 * Q2 * temp / (Q1 * rho_cgs + Q2 * temp)
    yh1t = y_high * y_low * x1t
    u_over_nkt = u_mol * y_low + u_si * y_high - (f_si - f_mol) * yh1t + 0.5

    # 온도만의 보정항 두 개. 압력에는 안 들어가고 내부에너지만 고친다.
    ttc = temp / TCRIT_AU
    ulb = (PC4 * ttc) ** 2.5
    u_over_nkt += 2.5 / (1.0 + ulb)
    ttc2 = ttc * ttc
    u_over_nkt += ((2.0 * PC1 * ttc - PC2 * ttc2) / (1.0 + ttc2) - PC3) / temp

    n_kt = TNK_CONV * rho_cgs * t6        # erg/cc
    return u_over_nkt * n_kt / rho_cgs * 1.0e-4     # erg/g → J/kg


def gruneisen(rho: float, t: float) -> float:
    """그뤼나이젠 계수 γ = (∂P/∂T)_ρ / (ρ c_V).

    **유한차분이다.** 참조 구현은 이 둘을 해석적으로 내지만, 그 미분 사슬을 손으로 옮기면
    검산할 수 없는 코드가 길어진다. 중앙차분의 절단오차는 h² 이고 h = 1 % 이므로 1e-4
    수준이라, 이 적합 자체의 폭(퍼센트)보다 네 자릿수 아래다."""
    h = 0.01 * t
    dpdt = (pressure(rho, t + h) - pressure(rho, t - h)) / (2.0 * h)
    c_v = (internal_energy(rho, t + h) - internal_energy(rho, t - h)) / (2.0 * h)
    if c_v <= 0.0:
        return 0.0
    return dpdt / (rho * c_v)


_LAST_DENSITY = (0.0, 0.0, 0.0)   # 직전 (P, T, ρ). 출발점일 뿐이다


def density(p: float, t: float) -> float:
    """압력에서 밀도 [kg/m³]. P(ρ) 가 단조증가라 뿌리가 하나다.

    **이 자리가 적분의 안쪽 고리다.** 적분 한 번에 이 함수가 수천 번 불리고, 한 번마다
    pressure 가 페르미 적분을 네 번쯤 먹는다. 그래서 이분법 200회로는 못 쓴다 — 처음에
    그렇게 짰다가 천왕성 하나가 10분을 넘겼다. log-log 할선법이 같은 답을 여덟 번쯤에
    내고, 괄호를 들고 다니므로 벗어나면 이분법으로 되돌린다."""
    lo, hi = RHO_MIN, RHO_MAX
    p_lo = pressure(lo, t)
    if p_lo >= p:
        return lo
    p_hi = pressure(hi, t)
    if p_hi <= p:
        return hi
    # log-log 는 거의 직선이다 (P ~ ρ^n, n ≈ 1~3). 두 끝점이 괄호이고, 출발점은
    # **직전 호출의 해** 를 쓴다 — 적분기가 매끄럽게 행진하므로 대개 한두 번이면 붙는다.
    x0, y0 = math.log(lo), math.log(p_lo / p)
    x1, y1 = math.log(hi), math.log(p_hi / p)
    global _LAST_DENSITY
    prev_p, prev_t, prev_rho = _LAST_DENSITY
    if prev_t == t and prev_p > 0.0 and 0.1 < p / prev_p < 10.0:
        x = math.log(prev_rho)
        if not (x0 < x < x1):
            x = x0 + (x1 - x0) * (-y0) / (y1 - y0)
    else:
        x = x0 + (x1 - x0) * (-y0) / (y1 - y0)
    for _ in range(60):
        rho = math.exp(x)
        y = math.log(pressure(rho, t) / p)
        if abs(y) < 1e-12:
            _LAST_DENSITY = (p, t, rho)
            return rho
        if y < 0.0:
            x0, y0 = x, y
        else:
            x1, y1 = x, y
        if y1 == y0:
            break
        nxt = x0 + (x1 - x0) * (-y0) / (y1 - y0)
        if not (x0 < nxt < x1):
            nxt = 0.5 * (x0 + x1)
        if abs(nxt - x) <= 1e-14 * abs(x):
            _LAST_DENSITY = (p, t, math.exp(nxt))
            return math.exp(nxt)
        x = nxt
    out = math.exp(0.5 * (x0 + x1))
    _LAST_DENSITY = (p, t, out)
    return out
