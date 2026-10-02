# C148 — 기준 단열선 표(fe_prem 은 값, 규산염 둘은 기록용)를 만드는 유일한 스크립트: 오늘의 꼴에서 지구 CMB 를 풀고, 각 재질의 ΔT = 0 단열선을 ln P 에서 RK4 로 적분해 굳힌다
"""python3 engine/tools/reference_adiabats.py [--check]

prereg-c148-fe-prem-reference-adiabat (198f3abd) §1.2–1.3 and §2:
- **fe_prem**: anchored at this engine's Earth CMB, solved under today's form (1 M⊕, cmf 0.325, T_pot = t_ref = 1600 K;
  under today's form Earth's ΔT is identically 0, so the anchor does not depend on the table it seeds), integrated both
  ways in ln P up to 0.999 × fe_prem's ceiling and down to 0.1 GPa.
- **silicate**, **silicate_chondritic** (the §2 note only, never values): from 1 bar at t_ref up to 0.999 × the ceiling.
- Each step is RK4 in ln P with Δln P = 0.005 on dT/d ln P = P · `interior._adiabatic_dtdp(m, P, ρ, T, t_ref)` at
  T_pot = t_ref, so ΔT = 0 and P_th = 0 along it (the E0's rule, `pc/c148/e0_variants.py`, `e0_silicate.py`).
The engine is imported with `NEARSTARS_REFERENCE_BUILD=1`, so it runs today's form while the table is built.
`--check` rebuilds in memory and compares byte-for-byte with the committed file (acceptance 9).
"""
from __future__ import annotations

import contextlib
import io
import json
import math
import os
import sys
from pathlib import Path

os.environ["NEARSTARS_REFERENCE_BUILD"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import eos        # noqa: E402
import interior   # noqa: E402

DLNP = 0.005
OUT = eos.REFERENCE_ADIABATS_PATH


def adiabat(mat, p0: float, t0: float, p_hi: float, p_lo: float) -> tuple[list[float], list[float]]:
    t_ref = mat.phases[0].t_ref

    def f(lnp, t):
        p = math.exp(lnp)
        return interior._adiabatic_dtdp(mat, p, mat.density(p, t, t_ref), t, t_ref) * p
    out = {math.log(p0): t0}
    for h, end in ((DLNP, math.log(p_hi)), (-DLNP, math.log(p_lo))):
        lnp, t = math.log(p0), t0
        while (lnp + h < end) if h > 0 else (lnp + h > end):
            k1 = f(lnp, t)
            k2 = f(lnp + h / 2, t + h / 2 * k1)
            k3 = f(lnp + h / 2, t + h / 2 * k2)
            k4 = f(lnp + h, t + h * k3)
            t += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            lnp += h
            out[lnp] = t
    rows = sorted(out.items())
    return [x for x, _ in rows], [y for _, y in rows]


def build() -> str:
    t_ref = eos.FE_PREM.phases[0].t_ref
    with contextlib.redirect_stdout(io.StringIO()):
        earth = interior.solve(1.0, body_class="rocky", core_mass_fraction=0.325, potential_temperature=t_ref).values
    p0, t0 = earth["cmb_pressure"] * 1e9, earth["cmb_temperature"]
    tables = {}
    lnp, t = adiabat(eos.FE_PREM, p0, t0, 0.999 * eos.FE_PREM.p_max, 1e8)
    tables["fe_prem"] = {"anchor": {"p_pa": p0, "t_k": t0, "how": "the engine's Earth CMB, mantle side (structure convention: "
                                    "mantle adiabat from T_pot 1600 K to the CMB, no D″ jump)"}, "lnp": lnp, "t": t}
    for name in ("silicate", "silicate_chondritic"):
        mat = eos.MATERIALS[name]
        lnp, t = adiabat(mat, 1e5, mat.phases[0].t_ref, 0.999 * mat.p_max, 1.0001e5)
        tables[name] = {"anchor": {"p_pa": 1e5, "t_k": mat.phases[0].t_ref, "how": "1 bar at t_ref"},
                        "lnp": lnp, "t": t}
    doc = {"provenance": {"registration": "prereg-c148-fe-prem-reference-adiabat 198f3abd",
                          "generator": "engine/tools/reference_adiabats.py",
                          "rule": f"RK4 in ln P, dlnP {DLNP}, dT/dlnP = P * interior._adiabatic_dtdp at T_pot = t_ref",
                          "use": "fe_prem: Phase.delta_t (values). silicate*: the C148 §2 note only (no values)."},
           "tables": tables}
    return json.dumps(doc, indent=1) + "\n"


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        same = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        print(f"reference_adiabats.json rebuild {'identical' if same else 'DIFFERS'}")
        sys.exit(0 if same else 1)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.name}: " + " · ".join(f"{k} {len(v['lnp'])} rows" for k, v in json.loads(text)["tables"].items()))
