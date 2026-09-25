# 기저층 두께 훑기 — 층을 쌓은 화성에서 황 맞춤이 오너 상자 13–19 wt% 에 드는가 (구조 기저층 사전등록 §1)
"""The first question of `prereg-structure-basal-layer.md` (frozen `c2221c9c`): with a basal layer of
density 4050 kg/m³ (Khan+ 2023, grade analog) and thickness `D_d`, and the core target reduced to
1845 − D_d km (⚠ the apparent core + layer radius held at 1845 km — an assumption; Samuel 2019 has
R_l 1780 ± 20), does the sulphur fit land in the owner's box 13–19 wt%? A report, not a verdict.

    python3 engine/tools/basal_sulphur_scan.py [--jobs N] [--halvings N]

Per D_d: the fitted S, the core radius, nmoi (C59: the board has 0.3634), the pressure and state at the
layer base, and the fit bracket's two ends and the axis near its peak (C108's window moves with the axis).
The declarations are `bodies/mars.yaml`'s; nothing in it changes.
"""
from __future__ import annotations

import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))
import interior                        # noqa: E402

D_DS = [0.0, 50.0, 100.0, 135.0, 150.0, 165.0, 168.8, 200.0]   # prereg §6 ② — ours + Khan 150 ± 15 ends
DENSITY = 4050.0                                                # Khan+ 2023, analog (bml-molten-density-sources)
TARGET_KM = 1845.0
BOX = (0.13, 0.19)
PEAK_S = 0.245                                                  # C108: the axis peaks at S 24–24.5 wt%
NMOI_BOARD = 0.3634


def _declared() -> dict:
    import yaml
    d = yaml.safe_load((ENGINE / "bodies" / "mars.yaml").read_text())
    body = d["inputs"]

    def val(k):
        v = body[k]
        return v["value"] if isinstance(v, dict) else v
    return {k: val(k) for k in ("mass_earth", "radius_earth", "potential_temperature", "basal_iron_number",
                                "light_element_fixing")}


def _one(args):
    d_d, halvings = args
    dec = _declared()
    kw = dict(potential_temperature=dec["potential_temperature"], basal_iron_number=dec["basal_iron_number"],
              basal_layer_thickness_km=d_d or None, basal_layer_density=DENSITY if d_d else None)
    t0 = time.perf_counter()
    target = TARGET_KM - d_d
    w_s, res = interior.fit_sulphur_to_core_radius(dec["mass_earth"], dec["radius_earth"], target,
                                                   dec["light_element_fixing"], halvings=halvings, **kw)
    ends = {}
    for s in (0.13, PEAK_S, 0.25):
        r = interior.solve_with_core_sulphur(dec["mass_earth"], dec["radius_earth"], s, dec["light_element_fixing"],
                                             **kw)
        ends[s] = (r.values["core_radius_fraction"] * dec["radius_earth"] * interior.EARTH_RADIUS_M / 1e3
                   if r.applicable else None)
    out = {"d_d": d_d, "target_km": target, "secs": time.perf_counter() - t0, "ends": ends,
           "w_s": w_s, "applicable": res.applicable}
    if res.applicable:
        v = res.values
        out.update(core_km=v["core_radius_fraction"] * dec["radius_earth"] * interior.EARTH_RADIUS_M / 1e3,
                   nmoi=v["nmoi"], layer_km=v["basal_layer_thickness_km"], top_km=v["core_plus_layer_radius_solved_km"],
                   p_base=v["cmb_pressure"], state=v["basal_silicate_state"], cmf=v.get("core_mass_fraction"))
    else:
        out["reason"] = str(getattr(res, "reason", ""))[:200]
    return out


def main() -> int:
    argv = sys.argv[1:]
    jobs = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 4
    halvings = int(argv[argv.index("--halvings") + 1]) if "--halvings" in argv else None
    t0 = time.time()
    with ProcessPoolExecutor(jobs) as ex:
        rows = list(ex.map(_one, [(d, halvings) for d in D_DS]))
    print("기저층 두께 훑기 — 보고(판정 아님). 층 밀도 4050 kg/m³ (Khan+ 2023, analog) · 핵 목표 1845 − D_d km "
          "(⚠ 겉보기 핵 + 층 반지름을 1845 로 두는 가정; Samuel 2019 R_l 1780 ± 20)")
    print(f"  황 괄호 {interior.SULPHUR_FIT_BRACKET} · 오너 상자 {BOX} · 보드 nmoi {NMOI_BOARD}\n")
    print("  D_d km | 목표 핵 | 맞춘 S wt% | 상자 | 핵 km | 층 두께 | 꼭대기 | nmoi (대 보드) | 층 밑 P GPa · 상태 | "
          "축: S 13 · 24.5 · 25 → 핵 km")
    for r in rows:
        e = r["ends"]
        axis = " · ".join("—" if e[s] is None else f"{e[s]:.2f}" for s in (0.13, PEAK_S, 0.25))
        if r["applicable"] and r["w_s"] is not None:
            inbox = BOX[0] <= r["w_s"] <= BOX[1]
            print(f"  {r['d_d']:>6.1f} | {r['target_km']:.1f} | {r['w_s'] * 100:.4f} | {'안' if inbox else '밖'} | "
                  f"{r['core_km']:.2f} | {r['layer_km']:.1f} | {r['top_km']:.1f} | {r['nmoi']:.5f} "
                  f"({r['nmoi'] - NMOI_BOARD:+.5f}) | {r['p_base']:.2f} · {r['state']} | {axis} | {r['secs']:.0f} s")
        else:
            print(f"  {r['d_d']:>6.1f} | {r['target_km']:.1f} | 거절 — 괄호가 목표를 안 감싼다 | 축 {axis} | "
                  f"{r.get('reason', '')[:90]}")
    print(f"\n전체 {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
