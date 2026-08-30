# 엔진이 푼 천왕성·해왕성 맨틀 (P, T) 프로파일이 발표된 메탄 해리 문턱을 지나는지 잰다 — 측정만, 판정 없음
"""Where the solved ice-giant mantles sit against the published methane dissociation thresholds.

    python3 engine/tools/methane_thresholds.py

Reads the frozen convergence point of Uranus and Neptune from `ice_giant_anchor.json`, runs
the one standalone integration `test_ice_giant.py` uses, and reports the (P, T) samples of
the ice layer against the thresholds Sherman, Wilson, Weeraratne & Militzer 2012
(2012PhRvB..86v4113S) collect in their introduction: carbon-carbon bond formation above
1100 K and 10 GPa (Hirai+, LHDAC), diamond above 3000 K (same), and the polymeric regime at
4000-5000 K (their own DFT-MD). This is a measurement for the C4 row; it decides nothing.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
os.chdir(os.path.join(HERE, ".."))
sys.argv = [sys.argv[0]]
import test_ice_giant as tig  # noqa: E402

THRESHOLDS = (("C-C bonds (Hirai+): T > 1100 K and P > 10 GPa", lambda p, t: t > 1100 and p > 10e9),
              ("diamond (Hirai+): T > 3000 K", lambda p, t: t > 3000),
              ("polymeric (Sherman+ 2012): T > 4000 K", lambda p, t: t > 4000),
              ("polymeric, upper end: T > 5000 K", lambda p, t: t > 5000))


def main() -> int:
    anc = json.load(open("ice_giant_anchor.json"))
    for name in ("Uranus", "Neptune"):
        sa = anc["bodies"][name]["standalone"]
        p_c, t_c = float(sa["p_center_pa"]), float(sa["t_center"])
        st = tig._standalone(name, p_c, t_c)
        s = sorted((p, t) for p, t in st.ice_samples if p > 0.0 and t > 0.0)
        print(f"{name}: ice mantle {s[0][0] / 1e9:.1f}-{s[-1][0] / 1e9:.1f} GPa, "
              f"{s[0][1]:.0f}-{s[-1][1]:.0f} K ({len(s)} samples); centre {p_c / 1e9:.0f} GPa, {t_c:.0f} K")
        for label, cond in THRESHOLDS:
            hit = [(p, t) for p, t in s if cond(p, t)]
            if hit:
                print(f"  {label}: crossed at {hit[0][0] / 1e9:.1f} GPa, {hit[0][1]:.0f} K; "
                      f"{len(hit)}/{len(s)} samples above, to the mantle base")
            else:
                print(f"  {label}: not reached")
        for p_gpa in (50, 100, 200, 300, 500):
            near = min(s, key=lambda x: abs(x[0] - p_gpa * 1e9))
            print(f"    ~{p_gpa} GPa: T = {near[1]:.0f} K (at {near[0] / 1e9:.1f} GPa)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
