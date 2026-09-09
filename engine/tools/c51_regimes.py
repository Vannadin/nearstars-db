# C51 커밋 D — 세 영역을 각자의 앵커에만 대조하고, 등록된 판정 칸 셋을 읽는다
"""C51's evaluation: each regime against its own anchor, and the three registered verdict cells.

    python3 engine/tools/c51_regimes.py            # the gate reads the exit code
    python3 engine/tools/c51_regimes.py --verbose  # every row, including the sensitivity fan

⚠ **The rule this file obeys.** A stagnant-lid law is scored against a stagnant-lid anchor, a mobile-lid
law against a measured surface flow, and the transitional law against nothing — because its inputs do not
exist here. **No law is scored against another regime's anchor**, which is the error C47 (b) named.

⚠ **Four printed values exist for Earth's mantle potential temperature** — our bodies declare 1600 K
(Unterborn+ 2019), Foley 2018 uses 1623, Korenaga 2009 1350 °C = 1623.15, Foley & Bercovici 2014 1650.
The verdict rows run on **our own declaration**; the others travel beside them as a fan, never averaged.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cmb_flux as cf                  # noqa: E402
import mantle_budget as mb             # noqa: E402
import mantle_flux as mf               # noqa: E402
import radiogenic as rg                # noqa: E402
import transitional_lid as tl          # noqa: E402
from interior import solve as isolve   # noqa: E402

VERBOSE = "--verbose" in sys.argv
fails = 0

#: ⚠ **게이트는 판정이 아니라 재현을 검사한다** (C47 (k) 의 `c47_step4.py` 와 같은 형식). 판정 칸 셋은
#: 아래에 `[판정]` 으로 찍히고 기록은 `engine/interior-core.md` 의 C51 (d) 가 진다 — 판정이 게이트를
#: 붉게 유지하면 다음 좌석이 그 붉음을 배경으로 읽게 되고, 그때 새 회귀는 보이지 않는다.
EXPECTED = {
    ("Earth", "declared", 100.0): (12.325, 6.09, +65.1, 2.450),
    ("Earth", "C20", 100.0): (7.104, 3.51, +84.2, 4.251),
    ("Mars", "declared", 350.0): (8.923, 1.04, +49.4, 1.742),
    ("Mars", "declared", 500.0): (8.923, 0.94, +67.1, 1.928),
    ("Mars", "C20", 350.0): (1.770, 0.21, +102.8, 8.780),
    ("Mars", "C20", 500.0): (1.770, 0.19, +125.1, 9.716),
}

# ── the two bodies, from the interior solve rather than typed in ────────────
BODIES = {
    "Earth": {"mass_earth": 1.0, "cmf": 0.325, "radius_earth": 1.0,
              "t_p_declared": 1600.0, "t_p_c20": 1517.34, "delta_m": (100.0e3, 100.0e3)},
    "Mars": {"mass_earth": 0.1074, "cmf": 0.24, "radius_earth": 0.5320,
             "t_p_declared": 1600.0, "t_p_c20": 1377.03, "delta_m": (350.0e3, 500.0e3)},
}
#: Foley 2018 §4.1 의 지구 뚜껑 «∼100 km»; 화성은 Breuer & Spohn 2003 의 인쇄 밴드 «350–500 km».
T_P_FAN = {"our declaration (Unterborn+ 2019)": 1600.0, "Foley 2018 T_r": 1623.0,
           "Korenaga 2009 (1350 °C)": 1623.15, "Foley & Bercovici 2014 §8.1": 1650.0}
#: Reese+ 1998 초록: 금성 10–20, 화성 15–30 mW/m² — **용융 한계 천장**, 그림 교점, n=3 습윤 유변학.
REESE_CEILING = {"Venus": (10.0, 20.0), "Mars": (15.0, 30.0)}
#: Parro+ 2017 초록: *"heat flows varying between 14 and 25 mW m⁻², with an average value of 19"*.
PARRO_MARS = (14.0, 25.0, 19.0)
#: Jaupart+ 2007 (지구 전구 측정) 과 Reese 의 지구 반사실 진술.
EARTH_GLOBAL_MEASURED = (86.0, 6.0)
REESE_EARTH_COUNTERFACTUAL_K = (700.0, 1500.0)


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def geometry(b: dict) -> dict:
    v = isolve(b["mass_earth"], core_mass_fraction=b["cmf"], potential_temperature=1600.0).values
    m_kg = b["mass_earth"] * cf.M_EARTH_KG
    r_p = b["radius_earth"] * cf.R_EARTH_M
    return {"r_p_m": r_p, "r_c_m": v["core_radius"] * cf.R_EARTH_M,
            "g": cf.G_NEWTON * m_kg / r_p ** 2,
            "q_man_w": rg.budget(m_kg * (1.0 - b["cmf"]))["mantle_w"]}


def stagnant(name: str, t_p: float, delta: float, geo: dict) -> dict:
    return mb.secular_cooling(t_p, delta, geo["q_man_w"], r_p_m=geo["r_p_m"], r_c_m=geo["r_c_m"],
                              g=geo["g"])["at_zero_melt"]


print("=" * 96)
print("C51 커밋 D — 세 영역, 각자의 앵커. 어떤 법칙도 다른 영역의 앵커로 채점되지 않는다 (C47 (b))")
print("=" * 96)

geo = {n: geometry(b) for n, b in BODIES.items()}

print("\n■ 정체뚜껑 — Foley 2018 식 (1)(3), Foley 세트 (c₁ 0.5 · k 5 · α 3e-5 · 퍼텐셜 T_p)")
print(f"{'바디':>6} {'T_p K':>8} {'δ km':>7} {'F_man mW/m²':>12} {'A·F TW':>8} {'Q_man TW':>9} "
      f"{'dT_p/dt K/Gyr':>14} {'Urey':>6}")
stag = {}
for name, b in BODIES.items():
    for t_p, lab in ((b["t_p_declared"], "declared"), (b["t_p_c20"], "C20")):
        for delta in sorted(set(b["delta_m"])):
            r = stagnant(name, t_p, delta, geo[name])
            key = (name, lab, delta)
            stag[key] = r
            exp = EXPECTED.get((name, lab, delta / 1e3))
            if exp is not None:
                got = (r["f_man_w_m2"] * 1e3, r["q_surface_w"] / 1e12, r["dtp_dt_k_gyr"], r["urey"])
                if max(abs(a - b) for a, b in zip(got, exp)) > 0.06:
                    row(False, f"회귀 — {name}/{lab}/δ{delta/1e3:.0f}km: {got} ≠ 기대 {exp}")
            print(f"{name:>6} {t_p:8.2f} {delta/1e3:7.0f} {r['f_man_w_m2']*1e3:12.3f} "
                  f"{r['q_surface_w']/1e12:8.2f} {geo[name]['q_man_w']/1e12:9.2f} "
                  f"{r['dtp_dt_k_gyr']:+14.1f} {r['urey']:6.3f}")

print("\n■ 이동뚜껑 — Nimmo+ 2004 식 34–36 (`mantle_flux.implied_flux`), 이미 있던 법칙")
print(f"{'바디':>6} {'T_p K':>8} {'q mW/m²':>10} {'전체 TW':>9}  비고")
mob = {}
for name, b in BODIES.items():
    for t_p, lab in ((b["t_p_declared"], "declared"), (b["t_p_c20"], "C20")):
        o = mf.implied_flux(t_p, geo[name]["g"], geo[name]["r_p_m"])
        mob[(name, lab)] = o
        note = o["extrapolation_note"] or ""
        print(f"{name:>6} {t_p:8.2f} {o['q_m_w']/(4*3.14159265*geo[name]['r_p_m']**2)*1e3:10.3f} "
              f"{o['q_m_w']/1e12:9.2f}  {note[:44]}")

print("\n■ 전이 — Foley & Bercovici 2014 식 (54)(58)(59)(60)")
ref = tl.solve_on_body()
print(f"  ⚠ 거절: {ref['refused'][:88]}…")
for m in ref["missing"]:
    print(f"      · {m}")

print("\n" + "=" * 96)
print("등록된 판정 칸 셋 — 사전등록에 실패 문장까지 미리 적혀 있다. **게이트는 위의 재현만 검사한다**")
print("=" * 96)

mars_f = {k: v["f_man_w_m2"] * 1e3 for k, v in stag.items() if k[0] == "Mars"}
lo, hi, avg = PARRO_MARS
print(f"\n[판정] 칸 ① 화성 정체뚜껑 F_man ∈ Parro+ 2017 [{lo:.0f}, {hi:.0f}] mW/m² (평균 {avg:.0f}) — **실패**")
for k, f in sorted(mars_f.items()):
    print(f"        T_p {k[1]:>8} · δ {k[2]/1e3:.0f} km → {f:.3f} mW/m² · {'안' if lo <= f <= hi else '**밖**'}")
print("        등록된 실패 문장: «예산이 정체뚜껑 열류가 인쇄된 유일한 암석체를 재현하지 못한다 —")
print("        물리보다 전사가 먼저 의심받는다.» ⚠ 화성이 밴드 아래끝 14 에 닿으려면 T_p **1673.6 K**")
print("        (선언 1600 보다 +74 K) 가 필요하다. 어느 조합도 밴드에 들어가지 않는다.")

e_dec = stag[("Earth", "declared", 100.0e3)]
e_mob = mob[("Earth", "declared")]
print(f"\n[판정] 칸 ② 지구 정체뚜껑은 **반사실** — 관측 46 ± 3 TW 로 채점하지 않는다 — **통과**")
print(f"        정체뚜껑 지구: F_man {e_dec['f_man_w_m2']*1e3:.3f} mW/m² · 손실 {e_dec['q_surface_w']/1e12:.2f} TW · "
      f"dT_p/dt {e_dec['dtp_dt_k_gyr']:+.1f} K/Gyr · Urey {e_dec['urey']:.3f}")
print(f"        같은 T_p 이동뚜껑(Nimmo 34–36): {e_mob['q_m_w']/1e12:.2f} TW — 정체뚜껑의 "
      f"{e_mob['q_m_w']/e_dec['q_surface_w']:.1f}배. 방향이 Reese 의 «700–1500 K 더 뜨거웠을 것» 과 같다.")

u_pairs = {"각자 C20 온도": (stag[("Earth", "C20", 100.0e3)]["urey"], stag[("Mars", "C20", 350.0e3)]["urey"]),
           "둘 다 선언 1600 K": (e_dec["urey"], stag[("Mars", "declared", 350.0e3)]["urey"])}
print(f"\n[판정] 칸 ③ Urey 방향 지구 < 화성 — ⚠ **미결정: 등록이 온도 행을 고정하지 않았다**")
for lab, (ue, um) in u_pairs.items():
    print(f"        {lab:16s} Urey 지구 {ue:.3f} · 화성 {um:.3f} → {'**일치**' if ue < um else '**반대**'}")
print("        ⚠ 두 짝짓기가 반대 답을 낸다. 통과하는 행을 골라 적는 것은 사후 선택이므로 하지 않는다 —")
print("        C51 사전등록의 결함으로 기록하고, 어느 짝짓기가 이 칸의 뜻인지는 오너·지휘석 몫이다.")
print("        (화성의 선언 1600 K 는 C47 (i) 0단계가 지구에서 **옮긴** 값이라, 둘을 같은 T_p 로 두면")
print("        Urey 비가 재려는 차이를 바로 그 옮김이 지운다 — 그것이 이 미결정의 물리적 내용이다.)")

print("\n" + "=" * 96)
print("이 평가가 실제로 말하는 것 — 판정 셋보다 큰 구조 (판정 아님, 기록)")
print("=" * 96)
fE_c20 = stag[("Earth", "C20", 100.0e3)]["f_man_w_m2"] * 1e3
fM_c20 = stag[("Mars", "C20", 350.0e3)]["f_man_w_m2"] * 1e3
g_ratio = (geo["Mars"]["g"] / geo["Earth"]["g"]) ** (1.0 / 3.0)
print(f"  · 같은 T_p 에서 이 법칙의 화성/지구 플럭스 비는 **중력만으로 {g_ratio:.3f}** 에 고정된다 "
      f"(F_man ∝ g^(1/3), 다른 것은 안 읽는다).")
print(f"  · 측정 비는 {avg:.0f}/{EARTH_GLOBAL_MEASURED[0]:.0f} = **{avg/EARTH_GLOBAL_MEASURED[0]:.3f}** 이다. "
      "중력만으로는 두 바디의 대비를 만들 수 없다.")
print(f"  · 각자 C20 온도에서는 비가 {fM_c20/fE_c20:.3f} — 측정 {avg/EARTH_GLOBAL_MEASURED[0]:.3f} 의 "
      f"{abs(fM_c20/fE_c20/(avg/EARTH_GLOBAL_MEASURED[0])-1)*100:.0f} % 안이다. **대비는 거의 전부 온도차가 만든다.**")
print(f"  · 그런데 절대값은 두 바디 모두 같은 방향으로 어긋난다 — 지구 {EARTH_GLOBAL_MEASURED[0]:.0f}/{fE_c20:.2f} = "
      f"**{EARTH_GLOBAL_MEASURED[0]/fE_c20:.1f}배**, 화성 {avg:.0f}/{fM_c20:.2f} = **{avg/fM_c20:.1f}배**.")
print("  · ⚠ 그래서 이 평가의 결론은 «비는 맞고 절대 스케일이 한 자릿수 틀렸다» 이고, 그것이 C47 (e) 의")
print("    «절대 스케일에 앵커가 없다» 를 **두 바디 · 수지 · 두 논문** 으로 확인한 것이다. 지구의 정체뚜껑")
print("    반사실은 앵커가 아니므로, 스케일을 고칠 앵커는 화성의 Parro 밴드 하나뿐이다.")

if VERBOSE:
    print("\n■ 감도 부채 — 지구 T_p 네 인쇄값 (평균 내지 않는다)")
    for lab, t_p in T_P_FAN.items():
        r = stagnant("Earth", t_p, 100.0e3, geo["Earth"])
        print(f"      {lab:34s} T_p {t_p:7.2f} → F_man {r['f_man_w_m2']*1e3:7.3f} mW/m² · "
              f"dT_p/dt {r['dtp_dt_k_gyr']:+8.1f} K/Gyr · Urey {r['urey']:.3f}")

print("\n" + ("재현 이상 없음 — 판정은 위의 [판정] 줄들이다" if not fails else f"{fails}건 회귀"))
sys.exit(1 if fails else 0)
