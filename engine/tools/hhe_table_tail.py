import math

# ── 평가 ────────────────────────────────────────────────────────────────
#
# 격자가 log 공간에서 균일하므로 Catmull-Rom 이중 3차로 보간한다. 굳힌 값이 맞는지와
# 별개로 **보간 오차가 새 오차원** 이고, 그건 fermi.py 가 자기 표에 대해 이미 세운 규율이다.
# 아래 두 수는 재서 적은 것이다 — 매 두 번째 마디를 빼고 나머지에서 재고(밀도 3.1e-2,
# grad_ad 1.4e-1), 4차 수렴을 가정해 16으로 나눈 값이다. test_giant.py 가 다시 잰다.
INTERP_RHO_WORST = 2.0e-3
INTERP_GRAD_WORST = 9.1e-3

# 압력 바닥. 굳힌 창의 아래 끝(1 bar)이고, 기체 외피의 적분이 여기서 멈춘다 — 기체에는
# P = 0 인 표면이 없고, 발표된 거대행성 반지름이 전부 이 준위의 값이다.
P_FLOOR_PA = 10.0 ** LOGP_LO * 1e9
T_FLOOR_K = 10.0 ** LOGT_LO


def in_domain(p_pa, t_k):
    """이 (P, T) 가 굳힌 표 안이고 도달 가능 영역 안인가."""
    if p_pa <= 0.0 or t_k <= 0.0:
        return False
    lp = math.log10(p_pa / 1e9)
    lt = math.log10(t_k)
    if lt < LOGT_LO or lt > LOGT_LO + (NT - 1) * STEP:
        return False
    if lp < LOGP_LO or lp > LOGP_LO + (NP - 1) * STEP:
        return False
    return lt >= REACH_A + REACH_B * lp


def _cr(y0, y1, y2, y3, t):
    """Catmull-Rom. t 는 y1 과 y2 사이의 [0, 1]."""
    a = 2.0 * y1
    b = y2 - y0
    c = 2.0 * y0 - 5.0 * y1 + 4.0 * y2 - y3
    d = -y0 + 3.0 * y1 - 3.0 * y2 + y3
    return 0.5 * (a + t * (b + t * (c + t * d)))


def _row(table, i, j, n):
    """등온선 i 에서 j-1..j+2 네 점. 끝에서는 있는 값을 되풀이한다."""
    r = table[i]
    m = n - 1
    return (r[j - 1 if j >= 1 else 0],
            r[j],
            r[j + 1 if j + 1 <= m else m],
            r[j + 2 if j + 2 <= m else m])


def _bicubic(table, lt, lp):
    x = (lt - LOGT_LO) / STEP
    y = (lp - LOGP_LO) / STEP
    i = int(x)
    j = int(y)
    if i >= NT - 1:
        i = NT - 2
    if j >= NP - 1:
        j = NP - 2
    if i < 0:
        i = 0
    if j < 0:
        j = 0
    u = x - i
    v = y - j
    col = []
    for k in (i - 1, i, i + 1, i + 2):
        kk = 0 if k < 0 else (NT - 1 if k > NT - 1 else k)
        n = KEEP[kk]
        jj = j if j <= n - 1 else n - 1
        col.append(_cr(*_row(table, kk, jj, n), v if jj == j else 1.0))
    return _cr(col[0], col[1], col[2], col[3], u)


def density(p_pa, t_k):
    """압력 [Pa] 과 온도 [K] 에서 수소-헬륨 혼합의 밀도 [kg/m^3]."""
    lp = math.log10(p_pa / 1e9)
    lt = math.log10(t_k)
    return 10.0 ** _bicubic(LOGRHO, lt, lp) * 1e3


def grad_ad(p_pa, t_k):
    """(dlnT/dlnP)_S. 표가 들고 있는 값이지 다시 만든 것이 아니다."""
    lp = math.log10(p_pa / 1e9)
    lt = math.log10(t_k)
    return _bicubic(GRAD_AD, lt, lp)


def dlrho(p_pa, t_k):
    """(dln rho/dln T)_P 와 (dln rho/dln P)_T. 위 밀도 표의 유한차분이다 —
    새 표가 아니라 같은 표의 기울기이므로 굳힌 자료가 늘지 않는다."""
    lp = math.log10(p_pa / 1e9)
    lt = math.log10(t_k)
    h = 0.5 * STEP
    # 가장자리에서는 한쪽 차분으로 바꾼다. 창 밖으로 반 칸이라도 나가면 스텐실이
    # 잘려서 기울기가 물리를 잃는다 — 1 bar 에서 gamma 가 0.47 대신 6.1 로 나왔다.
    dt = _slope(LOGRHO, lt, lp, h, True)
    dp = _slope(LOGRHO, lt, lp, h, False)
    return dt, dp


def _slope(table, lt, lp, h, along_t):
    lo_t, hi_t = LOGT_LO, LOGT_LO + (NT - 1) * STEP
    lo_p, hi_p = LOGP_LO, LOGP_LO + (NP - 1) * STEP
    a, b = (lt - h, lt + h) if along_t else (lp - h, lp + h)
    lo, hi = (lo_t, hi_t) if along_t else (lo_p, hi_p)
    if a < lo:
        a, b = lo, lo + 2.0 * h
    elif b > hi:
        a, b = hi - 2.0 * h, hi
    if along_t:
        return (_bicubic(table, b, lp) - _bicubic(table, a, lp)) / (b - a)
    return (_bicubic(table, lt, b) - _bicubic(table, lt, a)) / (b - a)


def gruneisen(p_pa, t_k):
    """gamma = (dlnT/dln rho)_S. **항등식이지 새 표가 아니다.**

    단열선을 따라 dln rho = [(dln rho/dln P)_T + (dln rho/dln T)_P * grad_ad] dln P 이고
    dln T = grad_ad dln P 이므로, 셋을 나누면 닫힌다. 셋 다 위 표에서 온다."""
    g = grad_ad(p_pa, t_k)
    dt, dp = dlrho(p_pa, t_k)
    den = dp + dt * g
    return 0.0 if den == 0.0 else g / den


def dpdt_v(p_pa, t_k):
    """(dP/dT)_rho [Pa/K] = -(dln rho/dln T)_P / (dln rho/dln P)_T * P/T."""
    dt, dp = dlrho(p_pa, t_k)
    if dp == 0.0:
        return 0.0
    return -dt / dp * p_pa / t_k


def heat_capacity_p(p_pa, t_k):
    """정압비열 c_P [J/kg/K]. 혼합의 단열 기울기가 이걸 가중치로 쓴다."""
    lp = math.log10(p_pa / 1e9)
    lt = math.log10(t_k)
    return _bicubic(C_P, lt, lp)
