# Bethkenhagen, French & Redmer 2013 의 Table I(암모니아 EOS)를 캐시된 PDF 에서 읽어 engine/ammonia_table.py 를 생성한다. 개발 전용, 런타임 아님
"""Generate `engine/ammonia_table.py` from the printed Table I of Bethkenhagen, French &
Redmer 2013, *Equation of state and phase diagram of ammonia at high pressures from ab
initio simulations*, J. Chem. Phys. 138, 234504 (2013JChPh.138w4504B,
doi 10.1063/1.4810883).

    python3 engine/tools/make_ammonia_table.py

**This script is not a runtime dependency.** It needs `pdftotext` (poppler) and the cached
PDF at `docs/phase3/_papers/2013JChPh.138w4504B.pdf`; its output is a plain-Python module
with no imports, the same discipline as `make_hhe_table.py` and `make_water_table.py`.

**The printed table is the distribution.** The paper has no repository, no data-availability
statement and no analytic fit; Appendix B, Table I (four columns, ρ g/cm³ · T K · p GPa ·
u kJ/g, across two pages) is the only form the data exist in. So the table is *parsed* from
the PDF's text layer — `pdftotext -layout` keeps the columns; plain `pdftotext` scatters
them — and then checked: 93 rows, no duplicates, eleven isotherms, nine densities, the six
absent cold-dense cells absent, and ten asterisks (five flagged rows, on p *and* u each).
Any of those failing stops the generator. `test_ammonia.py` re-checks the baked constants
against values read from the printed page by eye.

**Convention, stated once here and in the module.** The caloric column *includes* the
vibrational (nuclear-quantum) correction — Appendix B: "The latter one includes the
vibrational correction u^vc_vv(ρ, T) based on the power spectra that were computed
self-consistently from the simulations"; Fig. 7's caption says the same. Bethkenhagen+ 2017
§II.4 removed that correction from this very data set for consistency with their other
simulations. This repository bakes the printed (corrected) values, because they are the only
ones printed and the physically corrected ones; the consequence for mixing is written in
`engine/ammonia-table-context-notes.md`.

**Grid and interpolation.** The grid is ragged: 500 K has five densities (0.5–1.5), 700 K
seven (0.5–2.0), 1000 K and above nine (0.5–3.0). Nothing is interpolated across the absent
cells — the domain at a temperature is the intersection of its two bracketing isotherms'
density ranges. Along an isotherm log p is linear in log ρ and u is linear in log ρ; between
isotherms both are linear in T. The interpolation error is measured leave-one-out below and
written into the module.
"""
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PDF = os.path.join(ROOT, "docs", "phase3", "_papers", "2013JChPh.138w4504B.pdf")
TARGET = os.path.join(HERE, "..", "ammonia_table.py")

EXPECT_T = (500, 700, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000)
EXPECT_RHO = (0.5, 0.75, 1.0, 1.3, 1.5, 1.8, 2.0, 2.5, 3.0)
# 인쇄된 표의 빠진 칸 여섯. 파서가 떨어뜨린 것이 아니라 논문이 계산하지 않은 자리다.
EXPECT_ABSENT = {(500, 1.8), (500, 2.0), (500, 2.5), (500, 3.0), (700, 2.5), (700, 3.0)}
EXPECT_ROWS = 93
EXPECT_FLAGGED = 5

# 한 행: 밀도  온도  압력[*]  − 내부에너지[*]. 그림 축 숫자가 같은 줄 앞에 붙을 수 있어
# 줄 머리를 고정하지 않는다. 마이너스는 PDF 의 U+2212 다.
ROW = re.compile(r"(?<![\d.])([0-3]\.\d{1,2})\s+(\d{3,5})\s+(\d+\.\d+)(\*?)\s+[−-]\s*(\d+\.\d+)(\*?)")


def parse(text: str):
    rows = {}
    n_star = 0
    for m in ROW.finditer(text):
        rho = float(m.group(1))
        t = int(m.group(2))
        p = float(m.group(3))
        u = -float(m.group(5))
        star_p, star_u = bool(m.group(4)), bool(m.group(6))
        if t not in EXPECT_T or rho not in EXPECT_RHO:
            continue
        if (t, rho) in rows:
            raise SystemExit(f"duplicate row ({rho}, {t})")
        if star_p != star_u:
            raise SystemExit(f"asterisk on one column only at ({rho}, {t})")
        n_star += int(star_p) + int(star_u)
        rows[(t, rho)] = (p, u, star_p)
    if len(rows) != EXPECT_ROWS:
        raise SystemExit(f"parsed {len(rows)} rows, expected {EXPECT_ROWS}")
    absent = {(t, r) for t in EXPECT_T for r in EXPECT_RHO} - set(rows)
    if absent != EXPECT_ABSENT:
        raise SystemExit(f"absent cells {sorted(absent)} != expected {sorted(EXPECT_ABSENT)}")
    if n_star != 2 * EXPECT_FLAGGED:
        raise SystemExit(f"{n_star} asterisks, expected {2 * EXPECT_FLAGGED}")
    return rows


def isotherms(rows):
    out = []
    for t in EXPECT_T:
        pts = sorted((r, p, u, f) for (tt, r), (p, u, f) in rows.items() if tt == t)
        ps = [p for _r, p, _u, _f in pts]
        if any(b <= a for a, b in zip(ps, ps[1:])):
            raise SystemExit(f"pressure not monotone in density on the {t} K isotherm")
        out.append(tuple(pts))
    return tuple(out)


# ── 보간(생성 모듈과 같은 식) — 자기 검사용으로 여기에도 둔다 ───────────────
def _interp_iso(iso, rho):
    rs = [r for r, _p, _u, _f in iso]
    if rho < rs[0] or rho > rs[-1]:
        raise ValueError
    for j in range(len(rs) - 1):
        if rs[j] <= rho <= rs[j + 1]:
            r0, p0, u0, _ = iso[j]
            r1, p1, u1, _ = iso[j + 1]
            x = (math.log(rho) - math.log(r0)) / (math.log(r1) - math.log(r0))
            return math.exp(math.log(p0) + x * (math.log(p1) - math.log(p0))), u0 + x * (u1 - u0)
    raise ValueError


# 얼음거대행성 맨틀이 실제로 밟는 자리: rho >= 1.0 g/cm^3, T >= 2000 K (엔진이 푼 천왕성·해왕성
# 맨틀은 35-1000 GPa 에서 2550-6070 K — tools/methane_thresholds.py; 중심은 6160-6300 K 로
# 5000·7000 K 등온선 사이). 이 영역의 보간 오차를 따로 재서 적는다 — 전체 격자의 최악은
# 저밀도·해리 모서리(5 % 표시가 앉은 자리)에서 나오고 그 자리는 맨틀이 아니다.
MANTLE_RHO_MIN, MANTLE_T_MIN = 1.0, 2000


def leave_one_out(isos, region=None):
    """격자점 하나를 빼고 이웃에서 예측한 값과의 차. 밀도 방향(같은 등온선)과 온도 방향(같은 밀도)."""
    worst_p, worst_u, where = 0.0, 0.0, ("", "")
    for i, iso in enumerate(isos):
        for j in range(1, len(iso) - 1):
            r, p, u, _ = iso[j]
            if region and not region(r, EXPECT_T[i]):
                continue
            sub = iso[:j] + iso[j + 1:]
            pp, uu = _interp_iso(sub, r)
            if abs(pp / p - 1.0) > worst_p:
                worst_p, where = abs(pp / p - 1.0), (f"rho {r} T {EXPECT_T[i]}", where[1])
            if abs(uu - u) > worst_u:
                worst_u, where = abs(uu - u), (where[0], f"rho {r} T {EXPECT_T[i]}")
    for i in range(1, len(isos) - 1):
        t0, t1, t2 = EXPECT_T[i - 1], EXPECT_T[i], EXPECT_T[i + 1]
        lo = {r: (p, u) for r, p, u, _ in isos[i - 1]}
        hi = {r: (p, u) for r, p, u, _ in isos[i + 1]}
        for r, p, u, _ in isos[i]:
            if region and not region(r, t1):
                continue
            if r in lo and r in hi:
                x = (t1 - t0) / (t2 - t0)
                pp = lo[r][0] + x * (hi[r][0] - lo[r][0])
                uu = lo[r][1] + x * (hi[r][1] - lo[r][1])
                if abs(pp / p - 1.0) > worst_p:
                    worst_p, where = abs(pp / p - 1.0), (f"rho {r} T {t1} (along T)", where[1])
                if abs(uu - u) > worst_u:
                    worst_u, where = abs(uu - u), (where[0], f"rho {r} T {t1} (along T)")
    return worst_p, worst_u, where


HEAD = '''# Bethkenhagen, French & Redmer 2013 Table I 의 암모니아 상태방정식 표 — 생성된 파일이다. 손으로 고치지 말 것
"""Baked ammonia equation of state, Bethkenhagen, French & Redmer 2013.

**Generated by `engine/tools/make_ammonia_table.py`; do not edit by hand.** The source is
Appendix B, Table I of Bethkenhagen, French & Redmer 2013, *Equation of state and phase
diagram of ammonia at high pressures from ab initio simulations*, J. Chem. Phys. 138,
234504 (2013JChPh.138w4504B, doi 10.1063/1.4810883) — FT-DFT-MD pressure and internal
energy on a (rho, T) grid, parsed from the cached PDF's text layer and checked against the
printed page (`test_ammonia.py`). The printed table is the only form the data exist in.

**Convention.** The internal energy column INCLUDES the vibrational (nuclear-quantum)
correction u = u* + u_vc (their eq. (1); Appendix B; Fig. 7 caption). Bethkenhagen+ 2017
removed that correction from this data set for their own consistency; this module keeps
the printed values. Pressure carries no such correction — the paper neglected p_vc as small
for this data set "However, this should not be understood as a general result" (Sec. II B).

**Uncertainty.** "In general, the pressure is converged within an error bar of 2%, except
for the data points marked with asterisk, which have an uncertainty of up to 5%. The caloric
EOS is of the same quality as the pressure." (Appendix B). The five flagged points are
carried as a flag on the row and reported by `uncertainty(rho, t)`.

**Grid.** Ragged: 500 K has densities 0.5-1.5, 700 K 0.5-2.0, 1000 K and above 0.5-3.0
g/cm^3. The six absent cold-dense cells are outside the table, not interpolated across.
Along an isotherm log p is linear in log rho and u is linear in log rho; between isotherms
both are linear in T. Units inside the tuples are the paper's (g/cm^3, K, GPa, kJ/g); the
accessors take and return SI.
"""

SOURCE = "Bethkenhagen, French & Redmer 2013 (2013JChPh.138w4504B) Appendix B Table I"
U_INCLUDES_VIBRATIONAL_CORRECTION = True
P_UNCERTAINTY = 0.02           # converged within 2 %, Appendix B
P_UNCERTAINTY_FLAGGED = 0.05   # asterisked points, up to 5 %
T_MIN_K = 500.0
T_MAX_K = 10000.0
P_MAX_PA = 333.2e9             # the table's largest pressure (3.0 g/cm^3, 10 000 K)
N_POINTS = 93
N_FLAGGED = 5
'''

TAIL = '''

def _bracket_t(t_k):
    """(i, j): the isotherms bracketing T. On an isotherm exactly, i == j — that isotherm
    alone, so the ragged edge of a neighbour does not narrow the domain there."""
    if t_k < T_MIN_K or t_k > T_MAX_K:
        raise ValueError(f"{t_k:.0f} K is outside {SOURCE} ({T_MIN_K:.0f}-{T_MAX_K:.0f} K)")
    for i, tk in enumerate(T_K):
        if t_k == tk:
            return i, i
    for i in range(len(T_K) - 1):
        if T_K[i] < t_k < T_K[i + 1]:
            return i, i + 1
    raise ValueError


def _interp_iso(iso, rho_gcc):
    rs = [r for r, _p, _u, _f in iso]
    # 격자점 위의 반올림 한 비트는 안으로 접는다 (density 의 이분법이 exp(log) 로 되돌아올 때).
    if rs[0] * (1.0 - 1e-12) <= rho_gcc < rs[0]:
        rho_gcc = rs[0]
    elif rs[-1] < rho_gcc <= rs[-1] * (1.0 + 1e-12):
        rho_gcc = rs[-1]
    if rho_gcc < rs[0] or rho_gcc > rs[-1]:
        raise ValueError(f"rho {rho_gcc:.3f} g/cm^3 is outside this isotherm of {SOURCE}")
    for j in range(len(rs) - 1):
        if rs[j] <= rho_gcc <= rs[j + 1]:
            r0, p0, u0, f0 = iso[j]
            r1, p1, u1, f1 = iso[j + 1]
            if rho_gcc == r0:          # 격자점은 굳힌 값 그대로 (exp/log 왕복의 반올림 없이)
                return p0, u0, f0
            if rho_gcc == r1:
                return p1, u1, f1
            x = (math.log(rho_gcc) - math.log(r0)) / (math.log(r1) - math.log(r0))
            return (math.exp(math.log(p0) + x * (math.log(p1) - math.log(p0))),
                    u0 + x * (u1 - u0), f0 or f1)
    raise ValueError


def _eval(rho_kgm3, t_k):
    """(p [GPa], u [kJ/g], flagged) at (rho, T). Raises ValueError outside the table."""
    i, j = _bracket_t(t_k)
    r = rho_kgm3 / 1e3
    p0, u0, f0 = _interp_iso(ISOTHERMS[i], r)
    if i == j:
        return p0, u0, f0
    p1, u1, f1 = _interp_iso(ISOTHERMS[j], r)
    x = (t_k - T_K[i]) / (T_K[j] - T_K[i])
    return p0 + x * (p1 - p0), u0 + x * (u1 - u0), f0 or f1


def pressure(rho_kgm3, t_k):
    """p [Pa] at rho [kg/m^3], T [K]."""
    return _eval(rho_kgm3, t_k)[0] * 1e9


def internal_energy(rho_kgm3, t_k):
    """u [J/kg] at rho [kg/m^3], T [K]. Includes the vibrational correction (see module doc)."""
    return _eval(rho_kgm3, t_k)[1] * 1e6


def uncertainty(rho_kgm3, t_k):
    """The paper's stated relative uncertainty of p (and u) at this point: 5 % if any grid
    point the interpolation touches is asterisked, else 2 %."""
    return P_UNCERTAINTY_FLAGGED if _eval(rho_kgm3, t_k)[2] else P_UNCERTAINTY


def rho_bounds(t_k):
    """(rho_lo, rho_hi) [kg/m^3] the table covers at T: the intersection of the two
    bracketing isotherms' density ranges (the grid is ragged below 1000 K)."""
    i, j = _bracket_t(t_k)
    a, b = ISOTHERMS[i], ISOTHERMS[j]
    return max(a[0][0], b[0][0]) * 1e3, min(a[-1][0], b[-1][0]) * 1e3


def p_bounds(t_k):
    """(p_lo, p_hi) [Pa] the table covers at T."""
    lo, hi = rho_bounds(t_k)
    return pressure(lo, t_k), pressure(hi, t_k)


def in_domain(p_pa, t_k):
    if t_k < T_MIN_K or t_k > T_MAX_K:
        return False
    lo, hi = p_bounds(t_k)
    return lo <= p_pa <= hi


def density(p_pa, t_k):
    """rho [kg/m^3] at p [Pa], T [K], by bisection of the isotherm-interpolated p(rho).
    Raises ValueError, naming the table, outside its (ragged) domain."""
    lo, hi = rho_bounds(t_k)
    p_lo, p_hi = pressure(lo, t_k), pressure(hi, t_k)
    if p_lo * (1.0 - 1e-12) <= p_pa < p_lo:      # 가장자리의 반올림 한 비트는 안으로
        p_pa = p_lo
    elif p_hi < p_pa <= p_hi * (1.0 + 1e-12):
        p_pa = p_hi
    if p_pa < p_lo or p_pa > p_hi:
        raise ValueError(f"{p_pa / 1e9:.2f} GPa at {t_k:.0f} K is outside {SOURCE} "
                         f"({p_lo / 1e9:.3f}-{p_hi / 1e9:.1f} GPa at this temperature)")
    a, b = math.log(lo), math.log(hi)
    for _ in range(60):
        m = 0.5 * (a + b)
        if pressure(math.exp(m), t_k) < p_pa:
            a = m
        else:
            b = m
    return math.exp(0.5 * (a + b))
'''


def main():
    text = subprocess.run(["pdftotext", "-layout", PDF, "-"], check=True,
                          capture_output=True, text=True).stdout
    if "234504" not in text[:2000] or "ammonia" not in text[:2000].lower():
        raise SystemExit("the cached PDF's first page does not read as J. Chem. Phys. 138, 234504")
    rows = parse(text)
    isos = isotherms(rows)
    worst_p, worst_u, where = leave_one_out(isos)
    mantle_p, mantle_u, mwhere = leave_one_out(
        isos, lambda r, t: r >= MANTLE_RHO_MIN and t >= MANTLE_T_MIN)

    lines = [HEAD, "import math", "", "# 등온선 온도 [K].", f"T_K = {EXPECT_T!r}", "",
             "# 등온선마다 (rho [g/cm^3], p [GPa], u [kJ/g], 5 % 표시) — 인쇄된 순서대로.",
             "ISOTHERMS = ("]
    for t, iso in zip(EXPECT_T, isos):
        lines.append(f"    (  # {t} K")
        for r, p, u, f in iso:
            lines.append(f"        ({r!r}, {p!r}, {u!r}, {f!r}),")
        lines.append("    ),")
    lines.append(")")
    lines.append("")
    lines.append("# 보간 오차, leave-one-out 으로 잰 것: 격자점 하나를 빼고 이웃에서 예측한 값과의 차의")
    lines.append("# 최악. 격자 간격이 두 배가 된 자리의 수이므로 실제 격자 사이의 오차는 이보다 작다 —")
    lines.append("# 선형 보간의 오차가 간격의 제곱이면 약 1/4. test_ammonia.py 가 다시 잰다.")
    lines.append(f"INTERP_P_LOO_WORST = {worst_p:.4f}       # relative, at {where[0]}")
    lines.append(f"INTERP_U_LOO_WORST_KJG = {worst_u:.3f}   # absolute kJ/g, at {where[1]}")
    lines.append(f"# 같은 것을 맨틀 영역(rho >= {MANTLE_RHO_MIN} g/cm^3, T >= {MANTLE_T_MIN} K)에서만.")
    lines.append(f"MANTLE_RHO_MIN_GCC = {MANTLE_RHO_MIN!r}")
    lines.append(f"MANTLE_T_MIN_K = {float(MANTLE_T_MIN)!r}")
    lines.append(f"INTERP_P_LOO_MANTLE = {mantle_p:.4f}      # relative, at {mwhere[0]}")
    lines.append(f"INTERP_U_LOO_MANTLE_KJG = {mantle_u:.3f}  # absolute kJ/g, at {mwhere[1]}")
    lines.append(TAIL)
    open(TARGET, "w").write("\n".join(lines))

    print(f"wrote {TARGET}: {len(rows)} rows, {EXPECT_FLAGGED} flagged, "
          f"{len(EXPECT_T)} isotherms")
    print(f"  leave-one-out worst: p {worst_p * 100:.2f} % at {where[0]}; "
          f"u {worst_u:.3f} kJ/g at {where[1]}")
    print(f"  leave-one-out, mantle region: p {mantle_p * 100:.2f} % at {mwhere[0]}; "
          f"u {mantle_u:.3f} kJ/g at {mwhere[1]}")
    for (t, r), (p, u, f) in sorted(rows.items()):
        if f:
            print(f"  flagged: rho {r} T {t} p {p} u {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
