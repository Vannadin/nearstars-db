# 판 2 A0 보고 — Λ 5–20 훑기 · 세 걸음 판 · 준정상 비교판 · 민감도를 한 번에 돌려 인쇄한다
"""Plate 2's A0 report (pre-registration v2 §5 and v2-3 … v2-8). Prints; decides nothing beyond A0's own
seven conditions, and the widths are ours (borrowed EDT1 σ), not an implementation tolerance.

    python3 engine/tools/samuel_a0_report.py <MOESM3 DATA_FIG1 dir> [profile.json] [--post-2p]

`--post-2p` is the post-hoc plate 2P (pre-registration v2-11): P_m at the top of the convecting mantle,
R_l − δ_u. It does not replace plate 2's verdict, and its verdict is labelled as after a post-hoc change.

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
    fig = Path([a for a in sys.argv[1:] if a != "--post-2p"][0])
    tc = sr.read_panel(fig / "PANEL_B" / "Tc.dat")
    tm = sr.read_panel(fig / "PANEL_B" / "Tm.dat")
    dlu = sr.read_panel(fig / "PANEL_A" / "Dlu.dat")
    post = "--post-2p" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--post-2p"]
    prof = ss.load(Path(args[1])) if len(args) > 1 else ss.mars_profile(Path("bodies/mars.yaml"))
    base_pm = "top" if post else "mid"
    verdict = "사후 수정 후 통과" if post else "A0 통과"
    if post:
        print("사후 판 2P — 판 2 판정(불통과)을 대신하지 않음. P_m = 대류 맨틀 위 끝(R_l − δ_u) 압력 (v2-11)\n")
    g, g_c = prof.gravity(prof.radius_m), prof.gravity(st.R_CORE_NO_BML_M)
    print(f"구조 — {prof.source}")
    print(f"  엔진 R {prof.radius_m / 1e3:.3f} km · 판 R_p {st.R_PLANET_M / 1e3:.1f} km · 엔진 핵 {prof.core_radius_m / 1e3:.3f} km"
          f" · 판 R_c {st.R_CORE_NO_BML_M / 1e3:.3f} km · 차 {(prof.core_radius_m - st.R_CORE_NO_BML_M) / 1e3:+.3f} km")
    print(f"  g {g:.4f} (인쇄 3.7) · g_c(판 R_c) {g_c:.4f} (인쇄 3.1) m/s² — 식에는 g 만 들어간다(2021 (14)–(17) 인쇄꼴)")
    print("  폭은 우리가 고른 폭(EDT1 σ 를 빌림) — 구현 오차 폭이 아님\n")

    def setup(lam, **kw):
        kw.setdefault("p_m_mode", base_pm)
        return sr.Setup(lam=lam, profile=prof, g=kw.pop("g", g), g_c=g_c, **kw)

    def one(lam, cap=CAP_MYR, **kw):
        t0 = time.time()
        out = sr.run(setup(lam, **kw), cap)
        out["secs"] = time.time() - t0
        if "refused" not in out:
            out["a0"] = sr.a0(out["rows"], tc, tm)
        return out

    def guard_line(out):
        """δ_b guard bites in three layers: step starts, RK stages, fixed-point iterations (v2-14)."""
        rows = out["rows"]
        gap = min(rows, key=lambda r: r["tc_tb_gap"])
        raw = max(rows, key=lambda r: r["delta_b_raw_over_shell"])

        def layer(name, hits):
            if not hits:
                return f"{name} 0"
            worst = max(hits, key=lambda h: h[1])
            return (f"{name} {len(hits)} ({hits[0][0]:.4f}–{hits[-1][0]:.4f} Gyr, |T_c − T_b| 최대 {worst[1]:.3g} K"
                    f" @ {worst[0]:.4f})")
        # the gap at the iteration where the guard bit — the converged T_b of the step can sit far from it
        steps = [(r["t"], r["guard_gap"]) for r in rows if r["guarded"]]
        return ("δ_b 가드(v2-14, ½ 껍질) 걸림 — " + layer("걸음", steps) + " · "
                + layer("RK 단계", out["guard_stage_hits"]) + " · " + layer("고리 반복", out["guard_iter_hits"])
                + f" · 걸음 시작의 |T_c − T_b| 최소 {gap['tc_tb_gap']:.4f} K @ {gap['t']:.4f} Gyr"
                + f" · 누르기 전 δ_b/껍질 최대 {raw['delta_b_raw_over_shell']:.4f} @ {raw['t']:.4f} Gyr")

    def limit_line(out):
        """v2-17: the bracket solve of δ_u/δ_b — failures, evaluations with several inner roots, root jumps."""
        jumps = out.get("root_jumps", [])
        s_ = (f"괄호 풀이 — 실패 {len(out['fixed_point_limit_hits'])} · 근 여럿 평가 {out.get('multi_root_evals', 0)}"
              f" · 뜀 {len(jumps)}")
        for j in jumps:
            s_ += f" [{j[0]:.4f} Gyr δ_b {j[1] / 1e3:.1f}→{j[2] / 1e3:.1f} km, T_c−T_b {j[3]:+.3f} K]"
        return s_

    def line(tag, out):
        if "refused" in out:
            return f"  {tag:<28} 거절 @ {out['refused_at_gyr']:.3f} Gyr — {out['refused'][:90]}"
        c = out["a0"]["conditions"]
        pk = c["②"][0]
        return (f"  {tag:<28} ㉠c {c['㉠c'][0]:7.1f}{'✓' if c['㉠c'][1] else '✗'} ㉠m {c['㉠m'][0]:7.1f}{'✓' if c['㉠m'][1] else '✗'}"
                f" ㉡c {c['㉡c'][0]:6.1f}{'✓' if c['㉡c'][1] else '✗'} ㉡m {c['㉡m'][0]:6.1f}{'✓' if c['㉡m'][1] else '✗'}"
                f" ① {c['①'][0]:+7.1f}{'✓' if c['①'][1] else '✗'} ② {pk[0]:6.1f}@{pk[1]:.2f}{'✓' if c['②'][1] else '✗'}"
                f" ①′ {c['①′'][0]:+7.1f}{'✓' if c['①′'][1] else '✗'} {verdict if out['a0']['pass'] else ''}"
                f" [{out['n_steps']} 걸음 {out['secs']:.1f} s]")

    print(f"── A0 본판(δ_b 가드 판, v2-14) — Λ 훑기 5–20, 걸음 상한 {CAP_MYR:g} Myr, 뚜껑 격자 ──")
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
    print(f"  {verdict} Λ: {ok if ok else '없음'}")
    for lam in (5.0, 10.0, 15.0, 20.0):
        if "refused" not in scan[lam]:
            print(f"      Λ {lam:g}: " + guard_line(scan[lam]))
            print(f"      Λ {lam:g}: " + limit_line(scan[lam]))

    def miss(o):
        c = o["a0"]["conditions"]
        return max(abs(c["㉠c"][0] - 2081.49) / 40, abs(c["㉠m"][0] - 1867.39) / 50, c["㉡c"][0] / 40, c["㉡m"][0] / 50)
    live = [lam for lam, o in scan.items() if "refused" not in o]
    ref = (ok[0] if ok else min(live, key=lambda lam: miss(scan[lam]))) if live else None
    if ref is None:
        print("  모든 Λ 가 거절 — 이하 생략")
        return 0
    print(f"  기준 Λ = {ref:g} ({'통과점' if ok else '가장 가까운 점 — 네 폭 대비 최대 초과가 가장 작음'})\n")

    print("── 적분기 — (h, h/2, h/4, h/8), 기준 Λ ──")
    for cap in (CAP_MYR, CAP_MYR / 2, CAP_MYR / 4, CAP_MYR / 8):
        o = one(ref, cap)
        print(line(f"상한 {cap:g} Myr", o))
        if "refused" not in o:
            print("      " + guard_line(o))
            print("      " + limit_line(o))

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
                    ("g 인쇄 3.7", {"g": 3.7}),
                    *((("P_m 대류층 중간", {"p_m_mode": "mid"}),) if post else (("P_m 대류층 위 끝", {"p_m_mode": "top"}),)),
                    ("P_m 대류층 아래 끝", {"p_m_mode": "bottom"}),
                    ("(13)(14) 정수압 3500·3.7", {"melt_pressure": "hydrostatic"}),
                    ("Stefan 전미분", {"stefan_mode": "total"}),
                    ("δ_b 가드 ¼ 껍질", {"delta_b_cap_fraction": 0.25}),
                    ("δ_b 가드 1 껍질", {"delta_b_cap_fraction": 1.0}),
                    ("근 가지 — 가장 작은 근", {"root_branch": "smallest"}),
                    ("근 가지 — 가장 큰 근", {"root_branch": "largest"}),
                    ("근 가지 — 가운데 근", {"root_branch": "middle"})):
        print(line(tag, one(ref, **kw)))
    print("  ⚠ g_c 3.1 은 식에 안 들어간다 — 2021 (14)–(17) 이 g 하나를 인쇄한다. 인쇄만 한다.")
    print("\n── 판 2′ — L1 비교 판 (v2 §2, v2-2 ①), 기준 Λ ──")
    l1 = {}
    for d in (260.0, 330.0):
        l1[d] = one(ref, fixed_lid_m=d * 1e3)
        print(line(f"L1({d:g})", l1[d]))
        if "refused" not in l1[d]:
            du = [r["delta_u"] / 1e3 for r in l1[d]["rows"]]
            print(f"      「D_lu {d:g} 을 D_l 자리에 넣었다 — 이 판의 껍질은 {d:g} + δ_u 로 Samuel 보다 δ_u 만큼 두껍다」"
                  f" δ_u {min(du):.1f}–{max(du):.1f} km (오늘 {du[-1]:.1f})")
    if all("refused" not in o for o in l1.values()):
        def end(o, k):
            return o["rows"][-1][k]
        for k, name in (("t_m", "T_m"), ("t_c", "T_c")):
            a, b, c = end(l1[330.0], k), end(l1[260.0], k), end(base, k)
            print(f"  A-방향 {name}: L1(330) {a:.1f} > L1(260) {b:.1f} > L2 {c:.1f} — {'✓' if a > b > c else '✗'}")
    else:
        print(f"  L1 이 Λ {ref:g} 에서 천장에 걸렸다 — 방향 비교를 거절 없는 Λ 10 에서 한 번 더 (보고)")
        l1b = {d: one(10.0, fixed_lid_m=d * 1e3) for d in (260.0, 330.0)}
        l2b = scan[10.0]
        for d, o in l1b.items():
            print(line(f"L1({d:g}), Λ 10", o))
            if "refused" not in o:
                du = [r["delta_u"] / 1e3 for r in o["rows"]]
                print(f"      「D_lu {d:g} 을 D_l 자리에 넣었다 — 이 판의 껍질은 {d:g} + δ_u 로 Samuel 보다 δ_u 만큼 두껍다」"
                      f" δ_u {min(du):.1f}–{max(du):.1f} km (오늘 {du[-1]:.1f})")
        if all("refused" not in o for o in l1b.values()):
            for k, name in (("t_m", "T_m"), ("t_c", "T_c")):
                a, b, c = (l1b[330.0]["rows"][-1][k], l1b[260.0]["rows"][-1][k], l2b["rows"][-1][k])
                print(f"  A-방향 {name} (Λ 10): L1(330) {a:.1f} > L1(260) {b:.1f} > L2 {c:.1f} — {'✓' if a > b > c else '✗'}")

    print("\n── 진단 ② — 뚜껑 두께, PANEL_A/Dlu.dat 의 모든 시각 (km) ──")
    print("   t Gyr    D_l    δ_u  D_l+δ_u  논문 Dlu   차")
    first = None
    for tt, v in dlu:
        if tt < base["rows"][0]["t"]:
            continue
        dl = sr.at(base["rows"], "d_l", tt) / 1e3
        du = sr.at(base["rows"], "delta_u", tt) / 1e3
        if first is None and abs(dl + du - v) > 20:
            first = tt
        if abs(round(tt * 20) - tt * 20) < 1e-9:          # print every 0.05 Gyr, compare at every row
            print(f"  {tt:6.3f} {dl:7.1f} {du:6.1f} {dl + du:8.1f} {v:9.1f} {dl + du - v:+6.1f}")
    print(f"  |차| > 20 km 가 처음 되는 시각: {first}")

    print("\n── 진단 ③ — 식 20 부호: dD_l/dt 대 (뚜껑 바닥 전도 유출 − q_m) ──")
    rows_ = [r for r in base["rows"] if r["ddl"] != 0.0 and r["lid_net"] != 0.0]
    bad = [r for r in rows_ if (r["ddl"] > 0) != (r["lid_net"] > 0)]
    print(f"  부호가 다른 걸음 {len(bad)} / {len(rows_)}"
          + (f" — 첫 {bad[0]['t']:.4f} Gyr, 마지막 {bad[-1]['t']:.4f} Gyr" if bad else ""))
    print("  (지각 항 ρ_cr[L_m + C_m(T_m − T_s)]Ḋ_cr 이 있으므로 두 부호가 갈릴 수 있다 — 갈린 걸음은 그 항의 몫인지도 본다)")
    explained = [r for r in bad if (r["ddl"] > 0) == (r["lid_net"] + r["crust_term"] > 0)]
    print(f"  그중 지각 항을 더하면 부호가 맞는 걸음 {len(explained)} / {len(bad)}")
    full = [r for r in rows_ if (r["ddl"] > 0) != (r["lid_net"] + r["crust_term"] > 0)]
    print(f"  (유출 − q_m + 지각 항) 과 dD_l/dt 의 부호가 다른 걸음 {len(full)} — 0 이면 배선이 식 20(`−` 해석) 그대로")

    st_min = min(r["stefan"] for r in base["rows"])
    base_setup_shells = sr.Setup(lam=ref, profile=prof, g=g, g_c=g_c).melt_shells
    n_neg = sum(r["stefan"] < 0 for r in base["rows"])
    print(f"\n  본판 Stefan 최소 {st_min:.4f} · 음수 걸음 {n_neg} / {len(base['rows'])}"
          f" (껍질 {base_setup_shells} — 음수는 녹는 부피 경계가 껍질을 건너는 이산화 잡음이다, v2-10."
          " «V_melt 고정이라 음» 이라던 앞 설명은 철회)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
