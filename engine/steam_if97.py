# IAPWS-IF97 region 1·2·3 의 물 — 브리프 23 의 벽(p≲0.1 GPa · 500–1000 K)을 메우는 전사
"""IAPWS-IF97 basic equations for regions 1, 2 and 3, transcribed.

Source: IAPWS R7-97(2012), *Revised Release on the IAPWS Industrial Formulation 1997
for the Thermodynamic Properties of Water and Steam* — cached as
`docs/phase3/_papers/IAPWS-IF97-Rev.pdf` and transcribed from the typeset pages
(the text layer drops the powers of ten, so every table below was read from the page
images; Brief 25, 2026-08-31). Closed-form Gibbs functions — no fitting, no table baking,
no runtime dependency.

What is here and what is not:
- **Region 1** (liquid): eq. (7), Table 2's 34 coefficients. Valid 273.15–623.15 K,
  p_sat(T) ≤ p ≤ 100 MPa.
- **Region 2** (vapor / low-density supercritical): eqs. (15)–(17), Tables 10–11.
  Valid T ≤ 623.15 K below p_sat; 623.15–863.15 K below the B23 line; 863.15–1073.15 K
  to 100 MPa.
- **B23 boundary** eq. (5), Table 1; **saturation line** eq. (30), Table 34.
- **Region 3** (623.15–863.15 K between B23 and 100 MPa): eq. (28), Table 30's 40
  Helmholtz coefficients, with ρ(p, T) by branch-aware bisection — transcribed later the
  same day, after the post-steam refusal spy showed the wall's remnant sat exactly in
  this triangle (18–97 MPa × 635–661 K on the Uranus end-B trials).
- Region 5 (above 1073.15 K) stays out, by name.

Verification: `verify()` recomputes every printed computer-program verification value —
Table 5 (region 1), Table 15 (region 2), Table 33 (region 3, plus an inversion
round-trip), Table 35 (saturation), and the B23 point — and
returns the worst relative error. The test suite calls it; the standard prints the values
to 9 significant digits.

∇_ad comes from the same Gibbs derivatives: with v = R·T·π·γ_π/p one gets
(∂v/∂T)_p = (R/p*)(γ_π − τ·γ_πτ), so
    ∇_ad = (P/T)·(dT/dP)_S = −π (γ_π − τ γ_πτ) / (τ² γ_ττ),
where for region 2 every γ-derivative is the ideal + residual sum (γ°_π = 1/π, γ°_πτ = 0).
"""
from __future__ import annotations

R = 461.526                 # J/kg/K — R7-97 eq. (1)
T_MAX_K = 1073.15           # region 2 upper edge (above it: region 5, not transcribed)
P_MAX_PA = 100e6            # 100 MPa

# ── B23 (regions 2/3 boundary), eq. (5), Table 1 ────────────────────────
_B23 = (0.34805185628969e3, -0.11671859879975e1, 0.10192970039326e-2,
        0.57254459862746e3, 0.13918839778870e2)


def p_b23_pa(t_k: float) -> float:
    """식 (5): π = n1 + n2 θ + n3 θ² (p* = 1 MPa, T* = 1 K). 623.15–863.15 K."""
    return (_B23[0] + _B23[1] * t_k + _B23[2] * t_k * t_k) * 1e6


# ── saturation line, eq. (30), Table 34 ─────────────────────────────────
_SAT = (0.11670521452767e4, -0.72421316703206e6, -0.17073846940092e2,
        0.12020824702470e5, -0.32325550322333e7, 0.14915108613530e2,
        -0.48232657361591e4, 0.40511340542057e6, -0.23855557567849,
        0.65017534844798e3)


def p_sat_pa(t_k: float) -> float:
    """식 (30). 273.15–647.096 K 의 포화압."""
    n = _SAT
    v = t_k + n[8] / (t_k - n[9])
    a = v * v + n[0] * v + n[1]
    b = n[2] * v * v + n[3] * v + n[4]
    c = n[5] * v * v + n[6] * v + n[7]
    return (2.0 * c / (-b + (b * b - 4.0 * a * c) ** 0.5)) ** 4 * 1e6


# ── region 1, eq. (7), Table 2 ──────────────────────────────────────────
_R1 = (
    (0, -2, 0.14632971213167), (0, -1, -0.84548187169114),
    (0, 0, -0.37563603672040e1), (0, 1, 0.33855169168385e1),
    (0, 2, -0.95791963387872), (0, 3, 0.15772038513228),
    (0, 4, -0.16616417199501e-1), (0, 5, 0.81214629983568e-3),
    (1, -9, 0.28319080123804e-3), (1, -7, -0.60706301565874e-3),
    (1, -1, -0.18990068218419e-1), (1, 0, -0.32529748770505e-1),
    (1, 1, -0.21841717175414e-1), (1, 3, -0.52838357969930e-4),
    (2, -3, -0.47184321073267e-3), (2, 0, -0.30001780793026e-3),
    (2, 1, 0.47661393906987e-4), (2, 3, -0.44141845330846e-5),
    (2, 17, -0.72694996297594e-15), (3, -4, -0.31679644845054e-4),
    (3, 0, -0.28270797985312e-5), (3, 6, -0.85205128120103e-9),
    (4, -5, -0.22425281908000e-5), (4, -2, -0.65171222895601e-6),
    (4, 10, -0.14341729937924e-12), (5, -8, -0.40516996860117e-6),
    (8, -11, -0.12734301741641e-8), (8, -6, -0.17424871230634e-9),
    (21, -29, -0.68762131295531e-18), (23, -31, 0.14478307828521e-19),
    (29, -38, 0.26335781662795e-22), (30, -39, -0.11947622640071e-22),
    (31, -40, 0.18228094581404e-23), (32, -41, -0.93537087292458e-25),
)
_R1_PSTAR = 16.53e6
_R1_TSTAR = 1386.0


def _r1_derivs(p_pa: float, t_k: float):
    """γ_π, γ_ππ, γ_τ, γ_ττ, γ_πτ — Table 4."""
    pi = p_pa / _R1_PSTAR
    tau = _R1_TSTAR / t_k
    a = 7.1 - pi
    b = tau - 1.222
    gp = gpp = gt = gtt = gpt = 0.0
    for i_, j_, n_ in _R1:
        ai = a ** i_
        bj = b ** j_
        gp += -n_ * i_ * a ** (i_ - 1) * bj if i_ else 0.0
        gpp += n_ * i_ * (i_ - 1) * a ** (i_ - 2) * bj if i_ >= 2 else 0.0
        gt += n_ * ai * j_ * b ** (j_ - 1) if j_ else 0.0
        gtt += n_ * ai * j_ * (j_ - 1) * b ** (j_ - 2) if j_ not in (0, 1) else 0.0
        gpt += -n_ * i_ * a ** (i_ - 1) * j_ * b ** (j_ - 1) if (i_ and j_) else 0.0
    return pi, tau, gp, gpp, gt, gtt, gpt


# ── region 2, eqs. (15)–(17), Tables 10–11 ──────────────────────────────
_R2_IDEAL = (
    (0, -0.96927686500217e1), (1, 0.10086655968018e2), (-5, -0.56087911283020e-2),
    (-4, 0.71452738081455e-1), (-3, -0.40710498223928), (-2, 0.14240819171444e1),
    (-1, -0.43839511319450e1), (2, -0.28408632460772), (3, 0.21268463753307e-1),
)
_R2 = (
    (1, 0, -0.17731742473213e-2), (1, 1, -0.17834862292358e-1),
    (1, 2, -0.45996013696365e-1), (1, 3, -0.57581259083432e-1),
    (1, 6, -0.50325278727930e-1), (2, 1, -0.33032641670203e-4),
    (2, 2, -0.18948987516315e-3), (2, 4, -0.39392777243355e-2),
    (2, 7, -0.43797295650573e-1), (2, 36, -0.26674547914087e-4),
    (3, 0, 0.20481737692309e-7), (3, 1, 0.43870667284435e-6),
    (3, 3, -0.32277677238570e-4), (3, 6, -0.15033924542148e-2),
    (3, 35, -0.40668253562649e-1), (4, 1, -0.78847309559367e-9),
    (4, 2, 0.12790717852285e-7), (4, 3, 0.48225372718507e-6),
    (5, 7, 0.22922076337661e-5), (6, 3, -0.16714766451061e-10),
    (6, 16, -0.21171472321355e-2), (6, 35, -0.23895741934104e2),
    (7, 0, -0.59059564324270e-17), (7, 11, -0.12621808899101e-5),
    (7, 25, -0.38946842435739e-1), (8, 8, 0.11256211360459e-10),
    (8, 36, -0.82311340897998e1), (9, 13, 0.19809712802088e-7),
    (10, 4, 0.10406965210174e-18), (10, 10, -0.10234747095929e-12),
    (10, 14, -0.10018179379511e-8), (16, 29, -0.80882908646985e-10),
    (16, 50, 0.10693031879409), (18, 57, -0.33662250574171),
    (20, 20, 0.89185845355421e-24), (20, 35, 0.30629316876232e-12),
    (20, 48, -0.42002467698208e-5), (21, 21, -0.59056029685639e-25),
    (22, 53, 0.37826947613457e-5), (23, 39, -0.12768608934681e-14),
    (24, 26, 0.73087610595061e-28), (24, 40, 0.55414715350778e-16),
    (24, 58, -0.94369707241210e-6),
)
_R2_PSTAR = 1e6
_R2_TSTAR = 540.0


def _r2_derivs(p_pa: float, t_k: float):
    """γ_π, γ_ππ, γ_τ, γ_ττ, γ_πτ (이상 + 잔여) — Tables 13–14."""
    pi = p_pa / _R2_PSTAR
    tau = _R2_TSTAR / t_k
    gt = gtt = 0.0
    for j_, n_ in _R2_IDEAL:
        gt += n_ * j_ * tau ** (j_ - 1) if j_ else 0.0
        gtt += n_ * j_ * (j_ - 1) * tau ** (j_ - 2) if j_ not in (0, 1) else 0.0
    gp, gpp, gpt = 1.0 / pi, -1.0 / (pi * pi), 0.0
    b = tau - 0.5
    for i_, j_, n_ in _R2:
        pii = pi ** i_
        bj = b ** j_
        gp += n_ * i_ * pi ** (i_ - 1) * bj
        gpp += n_ * i_ * (i_ - 1) * pi ** (i_ - 2) * bj if i_ >= 2 else 0.0
        gt += n_ * pii * j_ * b ** (j_ - 1) if j_ else 0.0
        gtt += n_ * pii * j_ * (j_ - 1) * b ** (j_ - 2) if j_ not in (0, 1) else 0.0
        gpt += n_ * i_ * pi ** (i_ - 1) * j_ * b ** (j_ - 1) if j_ else 0.0
    return pi, tau, gp, gpp, gt, gtt, gpt


# ── region 3, eq. (28), Table 30 (같은 날 후반 확장 — 벽의 잔여 좌표가 이 삼각형이었다) ──
T_CRIT_K = 647.096          # eq. (2)
_RHO_CRIT = 322.0           # eq. (4), kg/m³
_R3_N1 = 0.10658070028513e1
_R3 = (
    (0, 0, -0.15732845290239e2), (0, 1, 0.20944396974307e2), (0, 2, -0.76867707878716e1),
    (0, 7, 0.26185947787954e1), (0, 10, -0.28080781148620e1), (0, 12, 0.12053369696517e1),
    (0, 23, -0.84566812812502e-2), (1, 2, -0.12654315477714e1), (1, 6, -0.11524407806681e1),
    (1, 15, 0.88521043984318), (1, 17, -0.64207765181607), (2, 0, 0.38493460186671),
    (2, 2, -0.85214708824206), (2, 6, 0.48972281541877e1), (2, 7, -0.30502617256965e1),
    (2, 22, 0.39420536879154e-1), (2, 26, 0.12558408424308), (3, 0, -0.27999329698710),
    (3, 2, 0.13899799569460e1), (3, 4, -0.20189915023570e1), (3, 16, -0.82147637173963e-2),
    (3, 26, -0.47596035734923), (4, 0, 0.43984074473500e-1), (4, 2, -0.44476435428739),
    (4, 4, 0.90572070719733), (4, 26, 0.70522450087967), (5, 1, 0.10770512626332),
    (5, 3, -0.32913623258954), (5, 26, -0.50871062041158), (6, 0, -0.22175400873096e-1),
    (6, 2, 0.94260751665092e-1), (6, 26, 0.16436278447961), (7, 2, -0.13503372241348e-1),
    (8, 26, -0.14834345352472e-1), (9, 2, 0.57922953628084e-3), (9, 26, 0.32308904703711e-2),
    (10, 0, 0.80964802996215e-4), (10, 1, -0.16557679795037e-3), (11, 26, -0.44923899061815e-4),
)


def _r3_phi_derivs(rho: float, t_k: float):
    """φ_δ, φ_δδ, φ_τ, φ_ττ, φ_δτ — Table 32."""
    d = rho / _RHO_CRIT
    tau = T_CRIT_K / t_k
    fd = _R3_N1 / d
    fdd = -_R3_N1 / (d * d)
    ft = ftt = fdt = 0.0
    for i_, j_, n_ in _R3:
        di = d ** i_
        tj = tau ** j_
        fd += n_ * i_ * d ** (i_ - 1) * tj if i_ else 0.0
        fdd += n_ * i_ * (i_ - 1) * d ** (i_ - 2) * tj if i_ >= 2 else 0.0
        ft += n_ * di * j_ * tau ** (j_ - 1) if j_ else 0.0
        ftt += n_ * di * j_ * (j_ - 1) * tau ** (j_ - 2) if j_ not in (0, 1) else 0.0
        fdt += n_ * i_ * d ** (i_ - 1) * j_ * tau ** (j_ - 1) if (i_ and j_) else 0.0
    return d, tau, fd, fdd, ft, ftt, fdt


def _r3_pressure(rho: float, t_k: float) -> float:
    """p = ρ R T δ φ_δ — Table 31."""
    d, _tau, fd, *_ = _r3_phi_derivs(rho, t_k)
    return rho * R * t_k * d * fd


def _r3_density(p_pa: float, t_k: float) -> float:
    """ρ(p, T) 역산 — 이분법. T < T_c 는 포화선(식 30)으로 액체·증기 가지를 가른다.

    region 3 안의 안정 단상에서는 (∂p/∂ρ)_T > 0 이라 가지 안에서 근이 하나다. 브리프 25 의
    삼각형(623.15–863.15 K × B23–100 MPa)이 소비처이고, 임계 근방(650 K 에서 Δρ 300 에
    Δp 3.3 MPa — Table 33 의 두 점)이 제일 평평해 이분법을 80 회 돌린다."""
    if t_k < T_CRIT_K and p_pa < p_sat_pa(t_k):
        lo, hi = 0.1, _RHO_CRIT          # 증기 가지
    elif t_k < T_CRIT_K:
        lo, hi = _RHO_CRIT, 900.0        # 액체 가지
    else:
        lo, hi = 0.1, 900.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if _r3_pressure(mid, t_k) < p_pa:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _r3_cp(rho: float, t_k: float) -> float:
    """c_p — Table 31 의 관계식 그대로."""
    d, tau, fd, fdd, _ft, ftt, fdt = _r3_phi_derivs(rho, t_k)
    num = (d * fd - d * tau * fdt) ** 2
    den = 2.0 * d * fd + d * d * fdd
    return R * (-tau * tau * ftt + num / den)


def _r3_grad_ad(rho: float, t_k: float, p_pa: float) -> float:
    """∇_ad = (P/T)(dT/dP)_S, (dT/dP)_S = T (∂v/∂T)_p / c_p,
    (∂v/∂T)_p = (1/ρ²)(∂P/∂T)_ρ / (∂P/∂ρ)_T — 둘 다 Table 31·32 의 도함수로 닫힌다."""
    d, tau, fd, fdd, _ft, ftt, fdt = _r3_phi_derivs(rho, t_k)
    dp_drho = R * t_k * (2.0 * d * fd + d * d * fdd)
    dp_dt = rho * R * d * (fd - tau * fdt)
    dv_dt = dp_dt / (rho * rho * dp_drho)
    return p_pa / t_k * (t_k * dv_dt / _r3_cp(rho, t_k))


def _r3_enthalpy(rho: float, t_k: float) -> float:
    d, tau, fd, _fdd, ft, *_ = _r3_phi_derivs(rho, t_k)
    return R * t_k * (tau * ft + d * fd)


# ── dispatch and properties ─────────────────────────────────────────────

def region(p_pa: float, t_k: float) -> int:
    """1·2·3 전부 전사됨 (3 은 브리프 25 후반, 같은 날 — 벽의 잔여가 그 삼각형이었다). 0 은 범위 밖."""
    if not (273.15 <= t_k <= T_MAX_K) or not (0.0 < p_pa <= P_MAX_PA):
        return 0
    if t_k <= 623.15:
        return 1 if p_pa >= p_sat_pa(t_k) else 2
    if t_k <= 863.15:
        return 2 if p_pa <= p_b23_pa(t_k) else 3
    return 2


def _derivs(p_pa: float, t_k: float):
    r = region(p_pa, t_k)
    if r == 1:
        return r, _r1_derivs(p_pa, t_k)
    if r == 2:
        return r, _r2_derivs(p_pa, t_k)
    return r, None            # 3 은 Helmholtz 라 별도 경로 (아래 각 함수의 분기)


def density(p_pa: float, t_k: float) -> float:
    """ρ [kg/m³] = p / (R T π γ_π). 영역 밖·region 3 은 ValueError (호출자가 이름 붙임)."""
    if region(p_pa, t_k) == 3:
        return _r3_density(p_pa, t_k)
    r, d = _derivs(p_pa, t_k)
    if d is None:
        raise ValueError(f"IF97: region {r} at {p_pa / 1e9:.4f} GPa · {t_k:.0f} K")
    pi, _tau, gp, *_ = d
    return p_pa / (R * t_k * pi * gp)


def c_p(p_pa: float, t_k: float) -> float:
    """c_P [J/kg/K] = −R τ² γ_ττ."""
    if region(p_pa, t_k) == 3:
        return _r3_cp(_r3_density(p_pa, t_k), t_k)
    r, d = _derivs(p_pa, t_k)
    if d is None:
        raise ValueError(f"IF97: region {r} at {p_pa / 1e9:.4f} GPa · {t_k:.0f} K")
    _pi, tau, _gp, _gpp, _gt, gtt, _gpt = d
    return -R * tau * tau * gtt


def enthalpy(p_pa: float, t_k: float) -> float:
    """h [J/kg] = R T τ γ_τ — 검증표 대조용."""
    if region(p_pa, t_k) == 3:
        return _r3_enthalpy(_r3_density(p_pa, t_k), t_k)
    r, d = _derivs(p_pa, t_k)
    if d is None:
        raise ValueError(f"IF97: region {r} at {p_pa / 1e9:.4f} GPa · {t_k:.0f} K")
    _pi, tau, _gp, _gpp, gt, *_ = d
    return R * t_k * tau * gt


def grad_ad(p_pa: float, t_k: float) -> float:
    """(∂lnT/∂lnP)_S = −π (γ_π − τ γ_πτ) / (τ² γ_ττ) — 머리주석의 유도."""
    if region(p_pa, t_k) == 3:
        return _r3_grad_ad(_r3_density(p_pa, t_k), t_k, p_pa)
    r, d = _derivs(p_pa, t_k)
    if d is None:
        raise ValueError(f"IF97: region {r} at {p_pa / 1e9:.4f} GPa · {t_k:.0f} K")
    pi, tau, gp, _gpp, _gt, gtt, gpt = d
    return -pi * (gp - tau * gpt) / (tau * tau * gtt)


def in_domain(p_pa: float, t_k: float) -> bool:
    return region(p_pa, t_k) in (1, 2, 3)


# ── computer-program verification (the standard's own printed values) ───

_VERIFY = (
    # (p_pa, t_k, v m³/kg, h J/kg, c_p J/kg/K) — Tables 5 and 15
    (3e6, 300.0, 0.100215168e-2, 0.115331273e6, 0.417301218e4),
    (80e6, 300.0, 0.971180894e-3, 0.184142828e6, 0.401008987e4),
    (3e6, 500.0, 0.120241800e-2, 0.975542239e6, 0.465580682e4),
    (0.0035e6, 300.0, 0.394913866e2, 0.254991145e7, 0.191300162e4),
    (0.0035e6, 700.0, 0.923015898e2, 0.333568375e7, 0.208141274e4),
    (30e6, 700.0, 0.542946619e-2, 0.263149474e7, 0.103505092e5),
)
_VERIFY_SAT = ((300.0, 0.353658941e4), (500.0, 0.263889776e7), (600.0, 0.123443146e8))
_B23_POINT = (623.15, 0.165291643e8)


def verify() -> float:
    """표준이 인쇄한 검증값 전부를 재계산해 최악 상대오차를 돌려준다 (9유효숫자 인쇄)."""
    worst = 0.0
    for p_pa, t_k, v_ref, h_ref, cp_ref in _VERIFY:
        worst = max(worst, abs(1.0 / density(p_pa, t_k) / v_ref - 1.0),
                    abs(enthalpy(p_pa, t_k) / h_ref - 1.0),
                    abs(c_p(p_pa, t_k) / cp_ref - 1.0))
    for t_k, p_ref in _VERIFY_SAT:
        worst = max(worst, abs(p_sat_pa(t_k) / p_ref - 1.0))
    worst = max(worst, abs(p_b23_pa(_B23_POINT[0]) / _B23_POINT[1] - 1.0))
    # region 3, Table 33 — (T, ρ) 가 인자라 역산 없이 직접 대조; 역산은 왕복으로 따로
    for t_k, rho, p_ref, h_ref, cp_ref in (
            (650.0, 500.0, 0.255837018e8, 0.186343019e7, 0.138935717e5),
            (650.0, 200.0, 0.222930643e8, 0.237512401e7, 0.446579342e5),
            (750.0, 500.0, 0.783095639e8, 0.225868845e7, 0.634165359e4)):
        worst = max(worst, abs(_r3_pressure(rho, t_k) / p_ref - 1.0),
                    abs(_r3_enthalpy(rho, t_k) / h_ref - 1.0),
                    abs(_r3_cp(rho, t_k) / cp_ref - 1.0))
        worst = max(worst, abs(_r3_density(_r3_pressure(rho, t_k), t_k) / rho - 1.0))
    return worst


if __name__ == "__main__":
    print(f"IF97 검증 최악 상대오차: {verify():.2e}")
