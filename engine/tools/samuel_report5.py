# 판 5 보고 — F · B2 · A-뚜껑 · A-거리 · A-방향 · D · E 와 «기저층이 녹는가» · 1845 km 재료 표를 한 번에 인쇄한다
"""Plate 5's report (pre-registration v2-29, draft `9d9abdf2`). A report plate: nothing here passes or fails,
except A-direction — a reversed order means wiring, and the report says STOP.

    python3 engine/tools/samuel_report5.py <MOESM3 DATA_FIG1 dir> <run.py mars output> <its time -l file>
                                           [--jobs N]

The second and third arguments are today's engine run on `bodies/mars.yaml` (`run.py`) and its
`/usr/bin/time -l` output — F and B2 read `history_steps` and the old Nimmo plate's present values there.
Choices no paper prints are printed where they are used.
"""
from __future__ import annotations

import math
import re
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
import samuel_run as sr                # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402

CAP_MYR = 10.0
FE_TOP = 94.1306
PASS_4P = [(4.0, 8.0), (4.0, 9.0), (4.0, 10.0), (5.0, 9.0), (5.0, 10.0)]     # v2-28
BEST_4P = (4.0, 10.0)
REP_4 = (7.0, 10.0)                                                            # v2-26
EDT1 = {"T_p": (1510.0, 20.0), "T_m": (1540.0, 20.0), "T_c": (2760.0, 150.0)}  # 2023 EDT1 BML main, PDF p10
PHI_I = 0.05                                                                   # 2021 SI S1, (S4)–(S6)
_PROF = None


def _prof():
    global _PROF
    if _PROF is None:
        _PROF = ss.mars_profile(ENGINE / "bodies" / "mars.yaml")
    return _PROF


def lambda_d(v_m: float, v_d: float) -> float:
    """(S6): Λ_d = [V_m − φ_i (V_m − V_d)/2] / [V_d + φ_i (V_m − V_d)/2]."""
    return (v_m - PHI_I * (v_m - v_d) / 2) / (v_d + PHI_I * (v_m - v_d) / 2)


def _one(job: dict) -> dict:
    prof = _prof()
    kw = dict(job.get("setup", {}))
    model = kw.pop("model", "bml")
    if model == "declared_mars":
        # B2 ⓑ — our declaration: R_c + D_d = 1845 km (core_plus_layer_radius_km), R_c = the engine's core,
        # ‾Fe#_d 75 (basal_iron_number), uniform (no Fe#_di declared), Λ_d from (S6) — our choices, printed.
        r_c = prof.core_radius_m
        sr.MODELS["declared_mars"] = dict(sr.MODELS["bml"], r_c=r_c)
    s = sr.Setup(lam=job["lam"], profile=prof, g=prof.gravity(prof.radius_m), g_c=0.0, model=model,
                 layer=job.get("layer"), **kw)
    t0 = time.time()
    out = sr.run(s, CAP_MYR)
    out["secs"] = time.time() - t0
    out["job"] = job["name"]
    return out


def _layer(k_d, fe_top=FE_TOP, **extra):
    return {**dict(d_d=st.D_D_M, k_d=k_d, lambda_d=14.373, fe_mean=96.97, fe_top=fe_top, nodes=41, melting=True,
                   record=True, source="2023 Fig. 1 g–l · v2-24"), **extra}


def jobs() -> list:
    js = [{"name": "4 rep", "lam": REP_4[1], "layer": _layer(REP_4[0])}]
    for k, lam in PASS_4P:
        js.append({"name": f"4P {k:g},{lam:g}", "lam": lam, "layer": _layer(k), "setup": {"p_m_mode": "top"}})
        js.append({"name": f"4P uni {k:g},{lam:g}", "lam": lam, "layer": _layer(k, fe_top=None),
                   "setup": {"p_m_mode": "top"}})
    k, lam = BEST_4P
    js.append({"name": "4P 3-0", "lam": lam, "layer": _layer(k, melting=False), "setup": {"p_m_mode": "top"}})
    js.append({"name": "4P B", "lam": lam, "layer": _layer(k, iron_shift=False), "setup": {"p_m_mode": "top"}})
    for lid in (260.0, 330.0):
        js.append({"name": f"4P L1({lid:g})", "lam": lam, "layer": _layer(k),
                   "setup": {"p_m_mode": "top", "fixed_lid_m": lid * 1e3}})
    js.append({"name": "2", "lam": 20.0, "setup": {"model": "no_bml"}})
    js.append({"name": "2P", "lam": 10.0, "setup": {"model": "no_bml", "p_m_mode": "top"}})
    prof = _prof()
    r_c, r_top = prof.core_radius_m, 1845.0e3
    v_m = 4 / 3 * math.pi * (st.R_PLANET_M ** 3 - r_c ** 3)
    v_d = 4 / 3 * math.pi * (r_top ** 3 - r_c ** 3)
    decl = dict(d_d=r_top - r_c, k_d=k, lambda_d=lambda_d(v_m, v_d), fe_mean=75.0, fe_top=None, nodes=41,
                melting=True, record=True, source="bodies/mars.yaml declaration · our choices (B2 ⓑ)")
    js.append({"name": "B2 declared", "lam": lam, "layer": decl, "setup": {"model": "declared_mars", "p_m_mode": "top"}})
    return js


def rms(rows, key, data, f=lambda x: x):
    win = [(t, v) for t, v in data if 0.5 <= t <= 4.5]
    return math.sqrt(sum((f(sr.at(rows, key, t)) - v) ** 2 for t, v in win) / len(win))


def main() -> int:
    argv = sys.argv[1:]
    fig, runout, timef = Path(argv[0]), Path(argv[1]), Path(argv[2])
    n_jobs = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 4
    tc = sr.read_panel(fig / "PANEL_H" / "Tc.dat")
    tm = sr.read_panel(fig / "PANEL_H" / "Tm.dat")
    dlu = sr.read_panel(fig / "PANEL_G" / "Dlu.dat")
    js = jobs()
    t0 = time.time()
    with ProcessPoolExecutor(n_jobs) as ex:
        res = {o["job"]: o for o in ex.map(_one, js)}
    print("판 5 보고 — 판정 없음(A-방향만 멈춤 사유). 폭은 우리가 고른 폭(EDT1 σ 를 빌림) — 구현 오차 폭이 아님")
    print(f"  실행 {len(js)} · {time.time() - t0:.0f} s · 3-1 본판 층상 Fe#_di {FE_TOP}\n")

    def today(name):
        o = res[name]
        return None if "refused" in o else o["rows"][-1]

    for name, o in res.items():
        if "refused" in o:
            print(f"  ⚠ {name}: 거절 @ {o['refused_at_gyr']:.3f} Gyr — {o['refused']}")

    # F
    text = runout.read_text()
    hs = re.search(r"history_steps=(\d+)", text)
    tcore = re.search(r"core_cmb_temperature_present=([\d.]+)", text)
    tpot = re.search(r"mantle_potential_temperature_present=([\d.]+)", text)
    tt = timef.read_text()
    instr_run = re.search(r"(\d+)\s+instructions retired", tt)
    real_run = re.search(r"([\d.]+) real", tt)
    print("F — 한 적분의 벽시계 · 걸음 수 (오늘 history_steps 와 나란히)")
    b = res[f"4P {BEST_4P[0]:g},{BEST_4P[1]:g}"]
    print(f"  새 모형 4P (4, 10): 걸음 {b['n_steps']} · 벽시계 {b['secs']:.0f} s(병렬 {n_jobs} 중 한 프로세스)")
    inst = _instr_one()
    print(f"  새 모형 한 적분 단독: instructions retired {inst[0]} · 벽시계 {inst[1]:.0f} s (구조 풀이 포함)")
    print(f"  오늘 core_thermal_history(화성 선언): history_steps {hs.group(1) if hs else '—'} · "
          f"run.py 전체(모든 노드) {real_run.group(1) if real_run else '—'} s · instructions retired "
          f"{instr_run.group(1) if instr_run else '—'}  ⚠ run.py 는 몸 전체 — 한 노드가 아님\n")

    # B2
    print("B2 — 오늘 Nimmo 판(옛 core_history, 화성 선언)과의 차, 폭")
    old_c = float(tcore.group(1)) if tcore else math.nan
    old_p = float(tpot.group(1)) if tpot else math.nan
    rs = [today(f"4P {k:g},{lam:g}") for k, lam in PASS_4P]
    rs = [r for r in rs if r]
    dc = [r["t_c"] - old_c for r in rs]
    dm = [r["t_m"] - old_p for r in rs]
    print(f"  옛 Nimmo 판: T_c {old_c:.0f} K · T_p {old_p:.0f} K (run.py 인쇄, 정수)")
    print(f"  ⓐ 재현 입력 4P 통과 점 {len(rs)}: T_c 차 {min(dc):+.0f} ~ {max(dc):+.0f} K · T_m − 옛 T_p {min(dm):+.0f} ~ {max(dm):+.0f} K"
          "  ⚠ T_m(뚜껑 아래 맨틀) 과 T_p(잠재 온도) 는 같은 양이 아님")
    d = res["B2 declared"]
    lay = d.get("layer") or {}
    print(f"  ⓑ 우리 선언 판: {lay.get('describe', '—')}")
    dj = next(j for j in js if j["name"] == "B2 declared")["layer"]
    print(f"     R_c(엔진 핵) {(1845e3 - dj['d_d']) / 1e3:.3f} km · D_d {dj['d_d'] / 1e3:.3f} km · Λ_d(S6, φ_i 0.05) {dj['lambda_d']:.3f} · "
          f"‾Fe#_d 75 · 균일 — 우리 선택")
    if "refused" not in d:
        r = d["rows"][-1]
        print(f"     오늘 T_c {r['t_c']:.1f} ({r['t_c'] - old_c:+.0f}) · T_m {r['t_m']:.1f} ({r['t_m'] - old_p:+.0f} 대 옛 T_p)\n")
    else:
        print("     거절 — 그 자체가 결과(위)\n")

    # A-lid, A-distance
    print("A-뚜껑 — D_l + δ_u 대 PANEL_G/Dlu (64.1 → 243.0 km)")
    for name in ["4 rep"] + [f"4P {k:g},{lam:g}" for k, lam in PASS_4P]:
        o = res[name]
        if "refused" in o:
            continue
        rows = [dict(r, dlu=r["d_l"] + r["delta_u"]) for r in o["rows"]]
        err = rms(rows, "dlu", dlu, lambda x: x / 1e3)
        print(f"  {name:>12}: RMS {err:.1f} km · 오늘 {rows[-1]['dlu'] / 1e3:.1f} km (목표 {dlu[-1][1]:.1f})")
    print("\nA-거리 — EDT1 BML main 삼중까지 (T_p 는 대응 미확인: 우리 적분기에 잠재 온도 칸 없음)")
    for name in ["4 rep"] + [f"4P {k:g},{lam:g}" for k, lam in PASS_4P]:
        r = today(name)
        if r:
            print(f"  {name:>12}: T_m {r['t_m'] - EDT1['T_m'][0]:+.1f} (σ {EDT1['T_m'][1]:g}) · "
                  f"T_c {r['t_c'] - EDT1['T_c'][0]:+.1f} (σ {EDT1['T_c'][1]:g}) · T_p 대응 없음")

    # A-direction
    print("\nA-방향 — L1(330) > L1(260) > L2 (T_m · T_c), 층 판 4P (4, 10)")
    l2, l260, l330 = today(f"4P {BEST_4P[0]:g},{BEST_4P[1]:g}"), today("4P L1(260)"), today("4P L1(330)")
    stop = False
    if l2 and l260 and l330:
        for key in ("t_m", "t_c"):
            ok = l330[key] > l260[key] > l2[key]
            stop |= not ok
            print(f"  {key}: L1(330) {l330[key]:.1f} · L1(260) {l260[key]:.1f} · L2 {l2[key]:.1f} → {'순서 맞음' if ok else '⚠ 반대 — 멈춤'}")
        for name in ("4P L1(260)", "4P L1(330)"):
            du = res[name]["rows"][-1]["delta_u"]
            print(f"  {name}: D_lu 자리에 {name[6:9]} km 를 D_l 로 넣었다 — 이 판의 껍질은 {name[6:9]} + δ_u 로 Samuel 보다 "
                  f"δ_u 만큼 두껍다 · δ_u 오늘 {du / 1e3:.1f} km")
    else:
        print("  ⚠ 거절된 판이 있어 순서를 못 셈")
        stop = True

    # D
    print("\nD — 녹음 (안 A: «Samuel+ 2021 이 인쇄한 그들의 선택») · 비교 안 B(철 항 없음, Duncan 한 점)")
    for name in [f"4P {BEST_4P[0]:g},{BEST_4P[1]:g}", "4P B", "4 rep", "B2 declared"]:
        o = res[name]
        if "refused" in o:
            continue
        L = o["layer"]
        h = L["history"]
        first = next((x for x in h if x[1] > 0.0), None)
        peak = max(h, key=lambda x: x[2])
        m = L["margin"]
        print(f"  {name:>12}: " + (f"처음 녹음 {first[0]:.3f} Gyr · " if first else "녹지 않음 · ")
              + f"녹은 부피 분율 최대 {peak[2]:.3f} @ {peak[0]:.2f} Gyr · 오늘 {h[-1][2]:.3f} (최대 φ {h[-1][1]:.3f}) · "
              f"녹음 거리 최소 {m[0]:.0f} K @ r {m[1] / 1e3:.1f} km · P {m[2]:.2f} GPa · {m[4]:.3f} Gyr")
    print(f"  [J] 안 B: {res['4P B']['layer']['describe'].split(' · ')[-1] if 'layer' in res['4P B'] and res['4P B']['layer'] else '—'}")

    # E
    print("\nE — 4P 통과 점의 폭 (본판 다섯 · 균일 넷+)")
    for label, pre in (("본판", "4P "), ("균일", "4P uni ")):
        vals = []
        for k, lam in PASS_4P:
            o = res[f"{pre}{k:g},{lam:g}"]
            if "refused" in o:
                continue
            a = sr.a_layer(o["rows"], tc, tm)["conditions"]
            vals.append((a["㉠"][0][0], a["㉠"][0][1], a["①"][0], a["②"][0][0], a["②"][0][1]))
        if vals:
            cols = list(zip(*vals))
            names = ["T_m 오늘", "T_c 오늘", "①", "② 최대", "② 시각"]
            print(f"  {label}: " + " · ".join(f"{n} {min(c):.1f}–{max(c):.1f}" for n, c in zip(names, cols))
                  + "  ⚠ k_d 하한 4 에 닿은 점 셋 — 폭이 상자 가장자리에 잘렸을 수 있음")

    # one page
    print("\n한 장 — «기저층이 녹는가»")
    A, B = res[f"4P {BEST_4P[0]:g},{BEST_4P[1]:g}"], res["4P B"]
    for label, o in (("안 A", A), ("안 B", B)):
        if "refused" in o:
            continue
        h = o["layer"]["history"]
        melted = any(x[1] > 0 for x in h)
        print(f"  {label}: {'예' if melted else '아니오'} — 오늘 녹은 부피 분율 {h[-1][2]:.3f} · 최대 {max(x[2] for x in h):.3f}")
    print("  ⚠ 두 답이 다르면 «녹는가» 는 철 항 선택에 딸린 답 — 안 A 는 Samuel 의 선택, 안 B 는 Fe# 25 한 점을 97 에 쓴 판")

    print("\n한 장 — 화성 1845 km 결정 재료 (결정은 안 함, 오너 칸)")
    print("  판           T_c − T_b(층 없음) / T_c − T′_b · T_c − T_i(층)   오늘 T_c   R_c        층 D_d")
    for name, rc, dd in (("2", st.R_CORE_NO_BML_M, 0.0), ("2P", st.R_CORE_NO_BML_M, 0.0),
                         ("4 rep", st.R_CORE_M, st.D_D_M), (f"4P {BEST_4P[0]:g},{BEST_4P[1]:g}", st.R_CORE_M, st.D_D_M),
                         ("B2 declared", None, None)):
        r = today(name)
        if not r:
            continue
        gap = f"{r['t_c'] - r['t_b']:+.1f}" + (f" · {r['t_c'] - r['layer']['t_i']:+.1f}" if r.get("layer") else "")
        rc_s = f"{rc / 1e3:.3f}" if rc else f"{(1845e3 - dj['d_d']) / 1e3:.3f}"
        dd_s = f"{dd / 1e3:.3f}" if dd is not None else f"{dj['d_d'] / 1e3:.3f}"
        print(f"  {name:>12}  {gap:>28}   {r['t_c']:.1f}   {rc_s} km   {dd_s} km")
    print(f"  선언 core_plus_layer_radius 1845 km · 재현 판 R_c 1646.176(층) / 1834.637(층 없음) km · 엔진 핵 {_prof().core_radius_m / 1e3:.3f} km")
    print(f"  ① 1 Gyr 까지 핵 가열: 4P 통과 점 " + ", ".join(
        f"{sr.at(res[f'4P {k:g},{lam:g}']['rows'], 't_c', 1.0) - res[f'4P {k:g},{lam:g}']['rows'][0]['t_c']:+.0f}"
        for k, lam in PASS_4P if 'refused' not in res[f'4P {k:g},{lam:g}']) + " K")
    if stop:
        print("\n⚠ A-방향 반대 부호 또는 셈 불가 — 판 5 멈춤, 지휘에 올림")
        return 2
    return 0


def _instr_one() -> tuple:
    """One integration alone under /usr/bin/time -l (cost ruler: instructions retired, not seconds)."""
    code = ("import sys; sys.path.insert(0, %r); import samuel_run as sr, samuel_structure as ss, samuel_thermal as st; "
            "from pathlib import Path; p = ss.mars_profile(Path(%r)); "
            "l = dict(d_d=st.D_D_M, k_d=4.0, lambda_d=14.373, fe_mean=96.97, fe_top=%r, nodes=41, melting=True); "
            "sr.run(sr.Setup(lam=10.0, profile=p, g=p.gravity(p.radius_m), g_c=0.0, model='bml', layer=l, p_m_mode='top'), %r)"
            ) % (str(ENGINE), str(ENGINE / "bodies" / "mars.yaml"), FE_TOP, CAP_MYR)
    t0 = time.time()
    r = subprocess.run(["/usr/bin/time", "-l", sys.executable, "-c", code], capture_output=True, text=True)
    m = re.search(r"(\d+)\s+instructions retired", r.stderr)
    return (m.group(1) if m else "—", time.time() - t0)


if __name__ == "__main__":
    sys.exit(main())
