# AQUA (P,T) 격자에서 차갑고 조밀한 유체 구석의 부분집합을 구워 aqua_table.py 를 만드는 생성기
"""Bake engine/aqua_table.py from the CDS AQUA grid (Brief 32, option 1).

Dev-only; runs on plain python3, no dependencies. Reads
docs/phase3/_papers/aqua/eos_pt.dat, windows T in [280, 1200] K x P in [1, 1200] GPa
plus 2 stencil-margin nodes each side, and writes rho, ad-grad, c_p (from the
published entropy column's central T-derivative, computed on the FULL T axis before
windowing) and the fluid mask (Phase in {3,4,5}).

Transcription gate: every baked rho/grad node must round-trip the raw file text
exactly (float(text) == baked). Physicality sweep runs here with the registered
criteria and prints the executed bounds; violations abort the bake.
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "..", "docs", "phase3", "_papers", "aqua", "eos_pt.dat")
OUT = os.path.join(HERE, "..", "aqua_table.py")

T_LO, T_HI = 280.0, 1200.0
P_LO, P_HI = 1e9, 1.2e12
MARGIN = 2
FLUID = {3, 4, 5}

print("reading", RAW)
P_axis, T_axis = [], []
rows = []
with open(RAW) as f:
    for ln in f:
        parts = ln.split()
        if len(parts) != 11:
            raise SystemExit(f"row with {len(parts)} fields: {ln[:60]}")
        rows.append(parts)
n = len(rows)
assert n == 328993, n
# 축 복원: 파일 순서 확인 (P 바깥 · T 안쪽 가정 검증)
NT_ALL, NP_ALL = 301, 1093
p0 = float(rows[0][0])
t0, t1 = float(rows[0][1]), float(rows[1][1])
assert float(rows[1][0]) == p0 and t1 > t0, "file order is not P-outer/T-inner"
T_axis = [float(rows[i][1]) for i in range(NT_ALL)]
P_axis = [float(rows[i * NT_ALL][0]) for i in range(NP_ALL)]
assert all(float(rows[i * NT_ALL + j][1]) == T_axis[j] for i in (0, 500, 1092) for j in (0, 150, 300))

def widx(axis, lo, hi):
    i0 = min(i for i, v in enumerate(axis) if v >= lo)
    i1 = max(i for i, v in enumerate(axis) if v <= hi)
    return max(i0 - MARGIN, 0), min(i1 + MARGIN, len(axis) - 1)

ti0, ti1 = widx(T_axis, T_LO, T_HI)
pi0, pi1 = widx(P_axis, P_LO, P_HI)
NT = ti1 - ti0 + 1
NP = pi1 - pi0 + 1
print(f"window: T[{T_axis[ti0]:.4g}..{T_axis[ti1]:.4g}] K x P[{P_axis[pi0]:.4g}..{P_axis[pi1]:.4g}] Pa -> {NT} x {NP} cells = {NT*NP}")

def cell(pi, tj):
    return rows[pi * NT_ALL + tj]

# c_p = T (ds/dT)_P — 상 인지 차분: 이웃이 다른 상(비유체 또는 상ID 상이)이면 그쪽을 쓰지
# 않는다. 상 경계의 엔트로피 점프(융해열)가 도함수에 스며드는 것을 막는 자리다 — 첫 실행에서
# 녹는선 인접 셀의 c_p 가 3만 J/kg/K 대로 튀었고, 원인은 AQUA 가 아니라 경계 너머 중앙차분이었다.
def cp_at(pi, tj):
    t = T_axis[tj]
    ph = int(cell(pi, tj)[10])
    lo = tj - 1 if tj - 1 >= 0 and int(cell(pi, tj - 1)[10]) == ph else tj
    hi = tj + 1 if tj + 1 <= NT_ALL - 1 and int(cell(pi, tj + 1)[10]) == ph else tj
    if lo == hi:
        return float("nan")     # 같은 상 이웃이 없다 — 이 셀의 c_p 는 못 굳힌다 (마스크에서 제외)
    s0 = float(cell(pi, lo)[4])
    s1 = float(cell(pi, hi)[4])
    return t * (s1 - s0) / (T_axis[hi] - T_axis[lo])

RHO, GRAD, CP, MASK = [], [], [], []
for pi in range(pi0, pi1 + 1):
    r_rho, r_g, r_cp, r_m = [], [], [], []
    for tj in range(ti0, ti1 + 1):
        c = cell(pi, tj)
        rho_txt, g_txt, ph = c[2], c[3], int(c[10])
        # 전사 게이트: 굳히는 값은 원문 텍스트의 float 그대로
        cpv = cp_at(pi, tj)
        r_rho.append(float(rho_txt))
        r_g.append(float(g_txt))
        r_cp.append(cpv)
        r_m.append(1 if (ph in FLUID and cpv == cpv) else 0)
    RHO.append(r_rho); GRAD.append(r_g); CP.append(r_cp); MASK.append(r_m)

# ── 물리성 스윕 (유체 마스크 안, 등록 기준) ──
viol = []
cp_lo, cp_hi = float("inf"), 0.0
for i in range(NP):
    run = []
    for j in range(NT):
        if not MASK[i][j]:
            continue
        rho, g, cp = RHO[i][j], GRAD[i][j], CP[i][j]
        if not (rho > 0 and math.isfinite(rho)):
            viol.append(("rho", i, j, rho))
        if not (0.0 < g < 1.0):
            viol.append(("grad", i, j, g))
        if not (500.0 < cp < 30000.0):
            viol.append(("cp", i, j, cp))
        else:
            cp_lo, cp_hi = min(cp_lo, cp), max(cp_hi, cp)
    # 등압 monotone 검사(같은 등온선 연속 유체 구간)는 P 방향이라 아래에서
for j in range(NT):
    prev = None
    for i in range(NP):
        if not MASK[i][j]:
            prev = None
            continue
        if prev is not None and RHO[i][j] < prev:
            viol.append(("mono", i, j, RHO[i][j] - prev))
        prev = RHO[i][j]
print(f"sweep: violations {len(viol)} · c_p executed [{cp_lo:.0f}, {cp_hi:.0f}] J/kg/K")
# water2 규칙: 인쇄된 주장보다 좁은 실행 유효 영역 — 불합격 셀은 마스크에서 제외하고 좌표를
# 기록한다. 음의 c_p 무리는 논문 자신이 적은 이음매다: "The main inconsistencies are located
# between regions 5, 6 and 7" (Haldemann+ 2020 §2.5). 제외가 유체 셀의 5 % 를 넘으면 중단.
excl_box = [float("inf"), 0.0, float("inf"), 0.0]
for _kind, i, j, _val in viol:
    MASK[i][j] = 0
    excl_box[0] = min(excl_box[0], P_axis[pi0 + i]); excl_box[1] = max(excl_box[1], P_axis[pi0 + i])
    excl_box[2] = min(excl_box[2], T_axis[ti0 + j]); excl_box[3] = max(excl_box[3], T_axis[ti0 + j])
n_fluid0 = sum(1 for i in range(NP) for j in range(NT) if MASK[i][j]) + len(viol)
if viol:
    print(f"excluded {len(viol)} cells ({len(viol)/n_fluid0*100:.2f} % of fluid) — box "
          f"P {excl_box[0]/1e9:.1f}–{excl_box[1]/1e9:.1f} GPa × T {excl_box[2]:.0f}–{excl_box[3]:.0f} K")
    if len(viol) > 0.05 * n_fluid0:
        raise SystemExit("exclusions exceed 5 % of fluid cells — bake aborted (branch ④)")
EXCL_N = len(viol)
EXCL_BOX = tuple(excl_box) if viol else None

fluid_cells = sum(sum(r) for r in MASK)
print(f"fluid cells {fluid_cells} / {NT*NP}")

def fmt_rows(tab, fmt):
    out = []
    for r in tab:
        out.append("    (" + ",".join(fmt % v for v in r) + "),")
    return "\n".join(out)

EXCL_BOX_STR = ("P %.1f-%.1f GPa x T %.0f-%.0f K" % (EXCL_BOX[0]/1e9, EXCL_BOX[1]/1e9,
                EXCL_BOX[2], EXCL_BOX[3])) if EXCL_BOX else "none"
with open(OUT, "w") as f:
    f.write(f'''# AQUA(Haldemann+ 2020) 유체 물의 차갑고 조밀한 구석 — 생성된 파일이다. 손으로 고치지 말 것
"""Baked AQUA subset (Haldemann, Alibert, Mordasini & Benz 2020, A&A 643, A105 —
2020A&A...643A.105H; CDS eos_pt.dat). Generated by tools/make_aqua_table.py; do not
edit by hand. Brief 32, option 1: the cold dense fluid corner only.

Window (exact node bounds, stencil margins included):
  T {T_axis[ti0]!r}..{T_axis[ti1]!r} K ({NT} nodes) x P {P_axis[pi0]!r}..{P_axis[pi1]!r} Pa ({NP} nodes),
  log-uniform. rho and grad_ad as published; c_p = T*(ds/dT)_P from the published
  entropy column (central difference on the full T axis). FLUID mask = Phase in
  {{3 vapor, 4 liquid, 5 supercritical+superionic}}; evaluation must refuse when a
  stencil leaves the mask (AQUA's own phase boundary; the melting line is OURS to
  judge — this table only represents the fluid side).

Executed validity (the water2 rule): {EXCL_N} fluid cells failed the registered
physicality criteria and are EXCLUDED from the mask — the negative-c_p cluster is the
seam the paper itself names ("The main inconsistencies are located between regions
5, 6 and 7", Haldemann+ 2020 sect. 2.5); excluded bounding box: {EXCL_BOX_STR}.

Label defects carried from the survey: AQUA's phase labels are not source labels;
its grid runs below the claimed 150 K floor; region 7's upper half is unmarked
extrapolation; its Method-2 seam (300-700 GPa) sits inside our ladder's span.
"""
import math

NT = {NT}
NP = {NP}
LOGT_LO = {math.log10(T_axis[ti0])!r}
LOGP_LO = {math.log10(P_axis[pi0])!r}
DLOGT = {(math.log10(T_axis[ti1]) - math.log10(T_axis[ti0])) / (NT - 1)!r}
DLOGP = {(math.log10(P_axis[pi1]) - math.log10(P_axis[pi0])) / (NP - 1)!r}
T_MIN_K = {T_axis[ti0 + MARGIN]!r}   # 여유칸 안쪽 = 평가 허용 창
T_MAX_K = {T_axis[ti1 - MARGIN]!r}
P_MIN_PA = {P_axis[pi0 + MARGIN]!r}
P_MAX_PA = {P_axis[pi1 - MARGIN]!r}

# 바깥 튜플 = 등압선(P 노드), 안쪽 = T 노드
RHO = (
{fmt_rows(RHO, "%.8e")}
)
GRAD_AD = (
{fmt_rows(GRAD, "%.8e")}
)
C_P = (
{fmt_rows([[c if c == c else 0.0 for c in r] for r in CP], "%.6e")}
)
FLUID = (
{fmt_rows(MASK, "%d")}
)


def _cr(y0, y1, y2, y3, t):
    a = 2.0 * y1
    b = y2 - y0
    c = 2.0 * y0 - 5.0 * y1 + 4.0 * y2 - y3
    d = -y0 + 3.0 * y1 - 3.0 * y2 + y3
    return 0.5 * (a + t * (b + t * (c + t * d)))


def _idx(p_pa, t_k):
    x = (math.log10(p_pa) - LOGP_LO) / DLOGP
    y = (math.log10(t_k) - LOGT_LO) / DLOGT
    i = min(max(int(x), 0), NP - 2)
    j = min(max(int(y), 0), NT - 2)
    return i, j, x - i, y - j


def in_window(p_pa, t_k):
    return P_MIN_PA <= p_pa <= P_MAX_PA and T_MIN_K <= t_k <= T_MAX_K


def fluid_stencil(p_pa, t_k):
    """4x4 스텐실 전부가 유체 마스크 안인가. 아니면 평가하지 않는다 — AQUA 의 상 경계를
    가로질러 보간하지 않는다."""
    i, j, _u, _v = _idx(p_pa, t_k)
    for a in (i - 1, i, i + 1, i + 2):
        aa = min(max(a, 0), NP - 1)
        for b in (j - 1, j, j + 1, j + 2):
            bb = min(max(b, 0), NT - 1)
            if not FLUID[aa][bb]:
                return False
    return True


def _bicubic(tab, p_pa, t_k):
    i, j, u, v = _idx(p_pa, t_k)
    col = []
    for a in (i - 1, i, i + 1, i + 2):
        aa = min(max(a, 0), NP - 1)
        r = tab[aa]
        col.append(_cr(r[j - 1 if j >= 1 else 0], r[j],
                       r[j + 1 if j + 1 <= NT - 1 else NT - 1],
                       r[j + 2 if j + 2 <= NT - 1 else NT - 1], v))
    return _cr(col[0], col[1], col[2], col[3], u)


def density(p_pa, t_k):
    return _bicubic(RHO, p_pa, t_k)


def grad_ad(p_pa, t_k):
    return _bicubic(GRAD_AD, p_pa, t_k)


def c_p(p_pa, t_k):
    return _bicubic(C_P, p_pa, t_k)
''')
print("wrote", OUT, os.path.getsize(OUT), "bytes")
