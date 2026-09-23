# 판 2 A0 보고 — Λ 5–20 훑기 · 세 걸음 판 · 준정상 비교판 · 민감도를 한 번에 돌려 인쇄한다
"""Plate 2's A0 report (pre-registration v2 §5 and v2-3 … v2-8). Prints; decides nothing beyond A0's own
seven conditions, and the widths are ours (borrowed EDT1 σ), not an implementation tolerance.

    python3 engine/tools/samuel_a0_report.py <MOESM3 DATA_FIG1 dir> [profile.json]

Without `profile.json` the engine's Mars structure is solved once (~65 s) through `samuel_structure`.
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import samuel_run as sr                # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402

CAP_MYR = 10.0
LAMBDAS = [5.0 + i for i in range(16)]


def main() -> int:
    fig = Path(sys.argv[1])
    tc = sr.read_panel(fig / "PANEL_B" / "Tc.dat")
    tm = sr.read_panel(fig / "PANEL_B" / "Tm.dat")
    dlu = sr.read_panel(fig / "PANEL_A" / "Dlu.dat")
    prof = ss.load(Path(sys.argv[2])) if len(sys.argv) > 2 else ss.mars_profile(Path("bodies/mars.yaml"))
    g, g_c = prof.gravity(prof.radius_m), prof.gravity(st.R_CORE_NO_BML_M)
    print(f"구조 — {prof.source}")
    print(f"  엔진 R {prof.radius_m / 1e3:.3f} km · 판 R_p {st.R_PLANET_M / 1e3:.1f} km · 엔진 핵 {prof.core_radius_m / 1e3:.3f} km"
          f" · 판 R_c {st.R_CORE_NO_BML_M / 1e3:.3f} km · 차 {(prof.core_radius_m - st.R_CORE_NO_BML_M) / 1e3:+.3f} km")
    print(f"  g {g:.4f} (인쇄 3.7) · g_c(판 R_c) {g_c:.4f} (인쇄 3.1) m/s² — 식에는 g 만 들어간다(2021 (14)–(17) 인쇄꼴)")
    print("  폭은 우리가 고른 폭(EDT1 σ 를 빌림) — 구현 오차 폭이 아님\n")

    def setup(lam, **kw):
        return sr.Setup(lam=lam, profile=prof, g=kw.pop("g", g), g_c=g_c, **kw)

    def one(lam, cap=CAP_MYR, **kw):
        t0 = time.time()
        out = sr.run(setup(lam, **kw), cap)
        out["secs"] = time.time() - t0
        if "refused" not in out:
            out["a0"] = sr.a0(out["rows"], tc, tm)
        return out

    def line(tag, out):
        if "refused" in out:
            return f"  {tag:<28} 거절 @ {out['refused_at_gyr']:.3f} Gyr — {out['refused'][:90]}"
        c = out["a0"]["conditions"]
        pk = c["②"][0]
        return (f"  {tag:<28} ㉠c {c['㉠c'][0]:7.1f}{'✓' if c['㉠c'][1] else '✗'} ㉠m {c['㉠m'][0]:7.1f}{'✓' if c['㉠m'][1] else '✗'}"
                f" ㉡c {c['㉡c'][0]:6.1f}{'✓' if c['㉡c'][1] else '✗'} ㉡m {c['㉡m'][0]:6.1f}{'✓' if c['㉡m'][1] else '✗'}"
                f" ① {c['①'][0]:+7.1f}{'✓' if c['①'][1] else '✗'} ② {pk[0]:6.1f}@{pk[1]:.2f}{'✓' if c['②'][1] else '✗'}"
                f" ①′ {c['①′'][0]:+7.1f}{'✓' if c['①′'][1] else '✗'} {'A0 통과' if out['a0']['pass'] else ''}"
                f" [{out['n_steps']} 걸음 {out['secs']:.1f} s]")

    print(f"── A0 본판 — Λ 훑기 5–20, 걸음 상한 {CAP_MYR:g} Myr, 뚜껑 격자 ──")
    print("  목표: ㉠c 2081.49±40 · ㉠m 1867.39±50 · ㉡c ≤40 · ㉡m ≤50 · ① <0 · ② [0.5,2.0] · ①′ >0")
    scan = {}
    for lam in LAMBDAS:
        scan[lam] = one(lam)
        print(line(f"Λ {lam:4.1f}", scan[lam]))
        o = scan[lam]
        if "refused" not in o:
            worst, when = o["max_lambda_over_ceiling"]
            print(f"      천장 사용 최대 Λ/천장 {worst:.3f} @ {when:.3f} Gyr")
    ok = [lam for lam, o in scan.items() if "refused" not in o and o["a0"]["pass"]]
    print(f"  A0 통과 Λ: {ok if ok else '없음'}")

    def miss(o):
        c = o["a0"]["conditions"]
        return max(abs(c["㉠c"][0] - 2081.49) / 40, abs(c["㉠m"][0] - 1867.39) / 50, c["㉡c"][0] / 40, c["㉡m"][0] / 50)
    live = [lam for lam, o in scan.items() if "refused" not in o]
    ref = (ok[0] if ok else min(live, key=lambda lam: miss(scan[lam]))) if live else None
    if ref is None:
        print("  모든 Λ 가 거절 — 이하 생략")
        return 0
    print(f"  기준 Λ = {ref:g} ({'통과점' if ok else '가장 가까운 점 — 네 폭 대비 최대 초과가 가장 작음'})\n")

    print("── 적분기 — (h, h/2, h/4), 기준 Λ ──")
    for cap in (CAP_MYR, CAP_MYR / 2, CAP_MYR / 4):
        print(line(f"상한 {cap:g} Myr", one(ref, cap)))

    print("\n── 준정상 비교판 (v2-3 ②, 보고) ──")
    base, qs = scan[ref], one(ref, lid_mode="quasi_steady")
    print(line("격자(본판)", base))
    print(line("준정상", qs))
    if "refused" not in qs:
        for tt in (0.5, 1.0, 2.0, 3.0, 4.5):
            print(f"      D_l @ {tt:.1f} Gyr: 격자 {sr.at(base['rows'], 'd_l', tt) / 1e3:7.1f} · 준정상 "
                  f"{sr.at(qs['rows'], 'd_l', tt) / 1e3:7.1f} km")

    print("\n── A-뚜껑 (보고) — D_l + δ_u 대 PANEL_A/Dlu.dat ──")
    for tt, v in [row for row in dlu if row[0] in (0.5, 1.0, 2.0, 3.0, 4.5) or abs(row[0] - 4.5) < 1e-9]:
        mine = (sr.at(base["rows"], "d_l", tt) + sr.at(base["rows"], "delta_u", tt)) / 1e3
        print(f"      {tt:.1f} Gyr: 우리 {mine:7.1f} · 논문 {v:7.1f} km")

    print("\n── 민감도 (보고, A0 판정 아님), 기준 Λ ──")
    for tag, kw in (("ϵ_m 첫 걸음 얼림", {"eps_mode": "frozen"}), ("ϵ_m = 1", {"eps_mode": "one"}),
                    ("g 인쇄 3.7", {"g": 3.7}), ("P_m 대류층 위 끝", {"p_m_mode": "top"}),
                    ("P_m 대류층 아래 끝", {"p_m_mode": "bottom"}),
                    ("(13)(14) 정수압 3500·3.7", {"melt_pressure": "hydrostatic"}),
                    ("Stefan 전미분", {"stefan_mode": "total"})):
        print(line(tag, one(ref, **kw)))
    print("  ⚠ g_c 3.1 은 식에 안 들어간다 — 2021 (14)–(17) 이 g 하나를 인쇄한다. 인쇄만 한다.")
    st_min = min(r["stefan"] for r in base["rows"])
    print(f"\n  본판 Stefan 최소 {st_min:.4f} (인쇄 꼴은 음수가 될 수 있다 — V_melt 고정, 평균 φ 가 줄면 음)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
