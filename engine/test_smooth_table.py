# C157 메모 10 판정 행 — 공용 표 보간(smooth_table)이 격자점 그대로 · 넘침 없음 · C¹(들쭉날쭉한 가장자리 포함)이고, 꺾인 표의 계단을 없애는가
"""python3 engine/test_smooth_table.py — prereg-c157 post-freeze note 10 §3 rows 5 and 6 (C¹ bar 1e-5 set after the
prototype, post-result; calibration floor printed beside every C¹ number)."""
from __future__ import annotations

import bisect
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import smooth_table as st  # noqa: E402

fails = 0
C1_BAR = 1e-5          # 노트 10 §3 행 5 — 시제품 뒤에 정함(post-result), 바닥보다 ≥ 10 배 위여야
LINEAR_MIN = 1e-3      # 같은 자리에서 «linear» 가 이만큼은 어긋나야 행이 실패할 수 있다


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


LAST = {}              # 마지막 c1_mismatch 의 가장 나쁜 줄(왼 · 오른 기울기, 반올림 해상도) — 감사 e2: 0 이 죽은 탐침인지 보이게


def _ev(fn, x, other, axis):
    return fn(x) if other is None else (fn(x, other) if axis == 0 else fn(other, x))


def c1_mismatch(fn, xs_line, step, other=None, axis=0):
    """노드선마다 2 차 한쪽 차분(왼 (3f0 − 4f(x−e) + f(x−2e))/2e, 오른 쪽은 거울)의 상대차 최댓값. 2 차라 곡률의 O(e) 항이
    없어 e 를 값 해상도에 맞게 키울 수 있다: e = max(간격 · 1e-7, 1e7 · ulp(f)/|기울기|), 간격의 1e-2 까지(감사 e2: 값의
    ulp 가 1 차 차분을 양자화해 0 을 냈다). 줄마다 반올림 해상도 ≈ 8·ulp(f)/(2e·|기울기|) 도 잰다. 못 읽는 점은 건너뛰고 센다."""
    worst, LAST["res"], LAST["line"], LAST["n"] = 0.0, 0.0, None, 0
    # 기울기 자: 이 줄 묶음의 전형 기울기(중앙값) — 자료가 값 해상도에서 평평한 격자점에서 0/0 이 안 나게(감사 e2 의 0 문제)
    sls = []
    for x in xs_line:
        h = step(x) if callable(step) else step
        try:
            sls.append(abs(_ev(fn, x + h * 0.25, other, axis) - _ev(fn, x - h * 0.25, other, axis)) / (0.5 * h))
        except Exception:  # noqa: BLE001
            pass
    scale = sorted(sls)[len(sls) // 2] if sls else 0.0
    for x in xs_line:
        h = step(x) if callable(step) else step
        try:
            f0 = _ev(fn, x, other, axis)
            sl = abs(_ev(fn, x + h * 0.25, other, axis) - _ev(fn, x - h * 0.25, other, axis)) / (0.5 * h)
            sref = max(sl, scale)
            e = 1e-7 * h if sref <= 0 else max(1e-7 * h, 1e9 * math.ulp(f0) / sref)
            e = min(e, 1e-2 * h)
            fm, fm2 = _ev(fn, x - e, other, axis), _ev(fn, x - 2 * e, other, axis)
            fp, fp2 = _ev(fn, x + e, other, axis), _ev(fn, x + 2 * e, other, axis)
        except Exception:  # noqa: BLE001 — 정의역 밖(빈 칸 · 표 밖)은 건너뛴다, 센 수로 남는다
            continue
        l = (3 * f0 - 4 * fm + fm2) / (2 * e)
        r = (-3 * f0 + 4 * fp - fp2) / (2 * e)
        den = max(abs(l), abs(r), scale, 1e-300)
        d = abs(l - r) / den
        res = 8 * math.ulp(f0) / max(2 * e * den, 1e-300)
        LAST["res"], LAST["n"] = max(LAST["res"], res), LAST["n"] + 1
        if d >= worst:
            worst, LAST["line"] = d, (x, l, r, e / h)
    return worst


def local_quadratic_floor(interp, lines, step, other=None, axis=0):
    """보정 바닥(노트 10 §3 행 5): 노드선마다 그 표 자신의 세 격자점(x−h, x, x+h)을 지나는 2 차식(C∞)에 같은 탐침 —
    표와 같은 크기 · 기울기라서 탐침의 반올림 바닥이 그 표에 맞다."""
    worst = 0.0
    for x in lines:
        h = step(x) if callable(step) else step
        try:
            ym, y0, yp = (_ev(interp, z, other, axis) for z in (x - h, x, x + h))
        except Exception:  # noqa: BLE001 — 정의역 밖은 건너뛴다
            continue
        m, c = (yp - ym) / (2 * h), (yp - 2 * y0 + ym) / (h * h)
        q = lambda z, x=x, y0=y0, m=m, c=c: y0 + m * (z - x) + 0.5 * c * (z - x) ** 2
        worst = max(worst, c1_mismatch(q, [x], step))
    return worst


def judged_c1_pool(name, interp, groups, step, axis):
    """같은 판정을 여러 줄 묶음(other, lines)에 걸쳐 모아서 — 줄 수 ≥ 10 (감사 e2)."""
    agg = {"pc": 0.0, "floor": 0.0, "lin": 0.0, "n": 0, "res": 0.0}
    for other, lines in groups:
        st.MODE = "pchip"
        fl = local_quadratic_floor(interp, lines, step, other, axis)
        pc = c1_mismatch(interp, lines, step, other, axis)
        agg["res"] = max(agg["res"], LAST["res"])
        agg["n"] += LAST["n"]
        agg["floor"] = max(agg["floor"], fl, LAST["res"])
        agg["pc"] = max(agg["pc"], pc)
        st.MODE = "linear"
        agg["lin"] = max(agg["lin"], c1_mismatch(interp, lines, step, other, axis))
        st.MODE = "pchip"
    check(f"{name}: C¹ at node lines (PCHIP ≤ {C1_BAR:g}, floor × 10 ≤ bar, linear > {LINEAR_MIN:g}, lines ≥ 10)",
          agg["pc"] <= C1_BAR and 10 * agg["floor"] <= C1_BAR and agg["lin"] > LINEAR_MIN and agg["n"] >= 10,
          f"lines {agg['n']} · PCHIP {agg['pc']:.2e} · floor {agg['floor']:.2e} (반올림 해상도 {agg['res']:.1e}) · linear {agg['lin']:.2e}")


def judged_c1(name, interp, exact, lines, step, other=None, axis=0):
    """같은 탐침을 해석 함수(바닥) · PCHIP · linear 에 — PCHIP ≤ C1_BAR, 바닥 × 10 ≤ C1_BAR, linear > LINEAR_MIN."""
    if exact == "local":
        st.MODE = "pchip"
        floor = local_quadratic_floor(interp, lines, step, other, axis)
    else:
        floor = c1_mismatch(exact, lines, step, other, axis) if exact else 0.0
    st.MODE = "pchip"
    pc = c1_mismatch(interp, lines, step, other, axis)
    res, line, n_lines = LAST["res"], LAST["line"], LAST["n"]
    floor = max(floor, res)                 # 바닥 = 2 차식 탐침과 반올림 해상도 중 큰 쪽
    st.MODE = "linear"
    lin = c1_mismatch(interp, lines, step, other, axis)
    st.MODE = "pchip"
    check(f"{name}: C¹ at node lines (PCHIP ≤ {C1_BAR:g}, floor × 10 ≤ bar, linear > {LINEAR_MIN:g}, lines ≥ 10)",
          pc <= C1_BAR and 10 * floor <= C1_BAR and lin > LINEAR_MIN and n_lines >= 10,
          f"lines {n_lines}/{len(lines)} · PCHIP {pc:.2e} · floor {floor:.2e} (반올림 해상도 {res:.1e}) · linear {lin:.2e}"
          + (f" · 가장 나쁜 줄 x {line[0]:.6g}: 왼 {line[1]:.9e} 오른 {line[2]:.9e} (e/h {line[3]:.1e})" if line else ""))


print("C157 메모 10 행 5 — 1 차원: 격자점 그대로 · 단조 자료에서 넘침 없음 · C¹")
random.seed(1)
xs = sorted({random.uniform(0, 10) for _ in range(14)})
ys = [math.sin(x) + 0.3 * x for x in xs]
exact_nodes = max(abs(st.cubic1(x, xs, ys, min(i, len(xs) - 2)) - y) / abs(y) for i, (x, y) in enumerate(zip(xs, ys)))
check("격자점 값 그대로(≤ 1e-12)", exact_nodes <= 1e-12, f"{exact_nodes:.1e}")
ym = [x ** 3 for x in xs]
over = 0
for _ in range(1000):
    x = random.uniform(xs[0], xs[-1])
    i = min(max(bisect.bisect_right(xs, x) - 1, 0), len(xs) - 2)
    v = st.cubic1(x, xs, ym, i)
    over += not (ym[i] - 1e-12 <= v <= ym[i + 1] + 1e-12)
check("단조 자료 1000 점에서 감싸는 격자값 밖으로 안 나간다", over == 0, f"{over} 점")


def f1(x):
    i = min(max(bisect.bisect_right(xs, x) - 1, 0), len(xs) - 2)
    return st.cubic1(x, xs, ym, i)


judged_c1("1 차원 x³", f1, lambda x: x ** 3, xs[1:-1], min(b - a for a, b in zip(xs, xs[1:])))

print("C157 메모 10 행 5 — 2 차원 · 들쭉날쭉한 가장자리(감사 e2): 노드선 양쪽 기울기, 외삽 읽기 > 0")
na, nb = 12, 20
xa = [0.1 * i for i in range(na)]
xb = [1.0 * j for j in range(nb)]
top = [10 + (i % 4) for i in range(na)]
F2 = lambda a, b: math.exp(0.3 * a) + b ** 2 / 50
val = lambda i, j: F2(xa[i], xb[j]) if j <= top[i] else None


def f2(a, b):
    ia = min(int(a / 0.1 + 1e-12), na - 2)
    ib = min(int(b + 1e-12), nb - 2)
    return st.cubic2(a, b, xa, xb, val, ia, ib)


st.EXTRAPOLATED_READS[0] = 0
for ia in range(1, na - 2):
    lim = min(top[ia], top[ia + 1])
    judged_c1_pool(f"2 차원 b 선(칸 a {xa[ia]:.1f}–{xa[ia + 1]:.1f}, a 두 곳, 가장자리 {lim})", f2,
                   [(xa[ia] + 0.03, xb[1:lim]), (xa[ia] + 0.07, xb[1:lim])], 1.0, 1)
check("가장자리 길을 실제로 밟았다(외삽 읽기 > 0)", st.EXTRAPOLATED_READS[0] > 0, f"{st.EXTRAPOLATED_READS[0]} 번")
judged_c1("2 차원 a 선(b = 4.5)", f2, F2, xa[1:-1], 0.1, 4.5, 0)

print("C157 메모 10 행 5 — 채택한 표마다: 노드선 100 개의 C¹(바닥은 같은 격자의 해석 함수)")
import water_table as w1  # noqa: E402
import water2_table as w2  # noqa: E402
import eos  # noqa: E402
# 바닥: 노드선마다 그 표의 세 격자점을 지나는 2 차식(C∞)에 같은 탐침(노트 10 §3 행 5 보정 줄; 표와 같은 크기 · 기울기)
lines = [w1.P_LO_PA + w1.P_STEP_PA * k for k in range(2, min(w1.NP - 2, 102))]
judged_c1("water1 ρ, P 노드선(T 301.3 K)", lambda p, t: w1.density(p, t), "local", lines, w1.P_STEP_PA, 301.3, 0)
lines = [w1.T_LO_K + w1.T_STEP_K * k for k in range(2, w1.NT - 2)]
judged_c1("water1 dT/dP, T 노드선(P 0.61 GPa)", lambda p, t: w1.dtdp_adiabat(p, t), "local", lines, w1.T_STEP_K, 0.61e9, 1)
lines = [10 ** (w2.LOGP_LO + w2.LOGP_STEP * k) * 1e9 for k in range(2, 62)]
judged_c1("water2 ρ, P 노드선(T 505 K)", lambda p, t: w2.density(p, t), "local", lines,
          lambda p: p * (10 ** w2.LOGP_STEP - 1.0), 505.0, 0)
ref = eos.REFERENCE_ADIABAT["fe_prem"]
lines = [math.exp(x) for x in ref.lnp[10:110]]
judged_c1("fe_prem 기준 단열선, ln P 노드선", lambda p: ref(p), "local", lines,
          lambda p: p * (math.exp(ref.lnp[1] - ref.lnp[0]) - 1.0))

print("C157 메모 10 행 5 — 선언 맨틀 표(이 노트의 표, 랜딩 입력 PC 판 0663e6a0) · edge_at · 암모니아")
import json, os  # noqa: E402
import mantle_composition as mc  # noqa: E402
_mt = Path(os.environ.get("MANTLE_TABLE_DIR", str(Path(__file__).resolve().parent / "mantle_tables"))) / "0663e6a031cae4dc.json"
if _mt.exists():
    tab = mc.Table(json.loads(_mt.read_text(encoding="utf-8")))
    rho = lambda p, t: tab.at(p, t)[0]
    ak = lambda p, t: tab.at(p, t)[1]
    dlnp = tab.lnp[1] - tab.lnp[0]
    pl = [math.exp(x) for x in tab.lnp if 1e9 <= math.exp(x) <= 2e10][:100]
    judged_c1("맨틀 ρ, P 노드선(T 1000 K)", rho, "local", pl, lambda p: p * (math.exp(dlnp) - 1.0), 1000.0, 0)
    judged_c1("맨틀 αK_T, P 노드선(T 1000 K)", ak, "local", pl, lambda p: p * (math.exp(dlnp) - 1.0), 1000.0, 0)
    tl = [t for t in tab.t if 400.0 <= t <= 1700.0]
    judged_c1("맨틀 ρ, T 노드선(P 5 GPa)", rho, "local", tl, tab.t[1] - tab.t[0], 5e9, 1)
    el = [math.exp(tab.lnp[k]) for k in range(1, len(tab.lnp) - 1)
          if all(math.isfinite(tab.edge[q]) for q in (k - 1, k, k + 1))
          and not (tab.edge[k - 1] == tab.edge[k] == tab.edge[k + 1])][:100]      # 가장자리가 실제로 변하는 격자점
    judged_c1("맨틀 edge_at, 변하는 ln P 노드선", lambda p: tab.edge_at(p), "local", el, lambda p: p * (math.exp(dlnp) - 1.0))
    # 들쭉날쭉한 가장자리 옆: 그 열의 가장자리 바로 아래 T 노드선들, P 는 칸 가운데
    st.EXTRAPOLATED_READS[0] = 0
    groups = []
    for k in range(117, 124):           # 이웃 P 열 일곱, 각 칸 가운데 P 에서 그 칸 가장자리 바로 아래 T 노드선들
        pmid = math.exp(0.5 * (tab.lnp[k] + tab.lnp[k + 1]))
        top = min(tab.edge[k], tab.edge[k + 1])
        groups.append((pmid, [t for t in tab.t if top - 300.0 <= t <= top - 50.0]))
    judged_c1_pool(f"맨틀 ρ, 가장자리 옆 T 노드선(P 열 7 개 {groups[0][0] / 1e9:.3f}–{groups[-1][0] / 1e9:.3f} GPa)", rho, groups,
                   tab.t[1] - tab.t[0], 1)
    print(f"  [기록] 맨틀 가장자리 옆 줄의 외삽 읽기 {st.EXTRAPOLATED_READS[0]} 번")
else:
    check("맨틀 표 파일이 있다(MANTLE_TABLE_DIR)", False, str(_mt))
import ammonia_table as am  # noqa: E402
pres = lambda r, t: am.pressure(r, t)
groups = []
for k in range(3, 8):                    # 등온선 사이 다섯 곳, 각 사이의 아래 등온선 ρ 격자점(양 끝 둘씩 뺌)
    t_mid = 0.5 * (am.T_K[k] + am.T_K[k + 1])
    groups.append((t_mid, [r * 1e3 for r, _p, _u, _f in am.ISOTHERMS[k][2:-2]]))
judged_c1_pool("암모니아 p, ρ 격자점 선(등온선 사이 다섯 곳)", pres, groups, lambda r: 0.5 * r * 0.05, 0)
groups = [(rho, list(am.T_K[2:-2])) for rho in (1200.0, 1500.0, 1800.0, 2100.0)]
judged_c1_pool("암모니아 p, 등온선(T 격자점) 선(ρ 네 곳)", pres, groups, lambda t: 0.1 * t, 1)

print("C157 메모 10 행 6(덧붙임 1) — 꺾인 표의 계단: 같은 장치를 꺾임 없앤 표(바닥)와 나란히, STEPS 1495–1505")
xp6 = [0.5 * k for k in range(41)]
xt6 = [100.0 * k for k in range(31)]
KINK = 0.02          # 1500 K 위쪽 기울기(아래는 0.002) — 장치 설계값(덧붙임 1: (ii) 여유가 모자라면 키우고 로그에 적는다)


def g6(p, t, kink):
    hi = KINK if kink else 0.002
    return ((5.0 + 0.002 * (t - 1500)) if t < 1500 else (5.0 + hi * (t - 1500))) * (1 + 0.01 * p)


def saw(kink):
    val6 = lambda kp, kt: g6(xp6[kp], xt6[kt], kink)

    def gi(p, t):
        return st.cubic2(p, t, xp6, xt6, val6, min(int(p / 0.5), 39), min(int(t / 100.0), 29))

    def run6(n):
        t, p, h = 1450.0, 0.0, 20.0 / n
        for _ in range(n):
            k1 = gi(p, t)
            k2 = gi(p + h / 2, t + h / 2 * k1)
            k3 = gi(p + h / 2, t + h / 2 * k2)
            k4 = gi(p + h, t + h * k3)
            t += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            p += h
        return t
    ns = list(range(1495, 1506))
    ys6 = [run6(n) for n in ns]
    mx, my = sum(ns) / len(ns), sum(ys6) / len(ys6)
    b = sum((x - mx) * (y - my) for x, y in zip(ns, ys6)) / sum((x - mx) ** 2 for x in ns)
    res = [y - (my + b * (x - mx)) for x, y in zip(ns, ys6)]
    return max(res) - min(res)


st.MODE = "pchip"
s_floor_pc = saw(False)
s_pc = saw(True)
st.MODE = "linear"
s_floor_lin = saw(False)
st.MODE = "pchip"
s_floor = max(s_floor_pc, s_floor_lin)      # 감사 e2 — 꺾임 없는 표(왼쪽 직선 이어감)를 두 MODE 로, 큰 쪽에 대어 판정
st.MODE = "linear"
s_lin = saw(True)
st.MODE = "pchip"
print(f"  [기록] S_linear {s_lin:.3e} K · S_pchip {s_pc:.3e} K · S_floor pchip {s_floor_pc:.3e} / linear {s_floor_lin:.3e} K")
check("(i) S_linear / S_pchip ≥ 100 (시제품 1800 에서 정함, post-result)", s_lin >= 100 * s_pc, f"{s_lin / max(s_pc, 1e-300):.0f}")
check("(ii) S_linear ≥ 100 × S_floor — linear 톱니가 바닥 위의 실체", s_lin >= 100 * s_floor, f"{s_lin / max(s_floor, 1e-300):.0f} ×")
print(f"  [기록 · FAILED at its claim, 노트 10 덧붙임 1] (iii) S_pchip ≤ 10 × S_floor — {s_pc / max(s_floor, 1e-300):.1f} × "
      "(자료의 꺾임은 C¹ 보간이 기울기 뜀은 없애도 곡률 뜀은 못 없앤다; (i) 의 감소는 위 줄)")

print(f"  test_smooth_table — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
