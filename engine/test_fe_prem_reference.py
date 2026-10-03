# C148 수락 9 · 10 (c) · 4 의 모양 — 기준 단열선 표가 생성기에서 비트까지 다시 나오는가, 다섯 값, 마디에서 열압력이 정확히 0 인가, 기록 세 칸이 엔진의 검사를 통과하는가
"""python3 engine/test_fe_prem_reference.py   (prereg-c148-fe-prem-reference-adiabat 198f3abd)

- Acceptance 9: `tools/reference_adiabats.py --check` rebuilds `reference_adiabats.json` byte-for-byte (fresh process,
  ~5 s); five fe_prem values are pinned.
- Acceptance 10 (c): at every node of fe_prem's table, T = T_ref(P) gives ΔT = 0 and P_th = 0 exactly.
- Placement: only fe_prem reads the table; the silicate phases keep today's form; without the table entry (the negative
  control's monkeypatch) fe_prem is back to today's form, bit for bit.
- Records (shape of acceptance 4 and 5): the fe_prem and silicate field triples pass `payload.check_provenance`.
"""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import eos
import interior
import payload

HERE = Path(__file__).resolve().parent
fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


# ── acceptance 9: rebuild and pins ──
r = subprocess.run([sys.executable, str(HERE / "tools" / "reference_adiabats.py"), "--check"],
                   capture_output=True, text=True, cwd=HERE)
check(r.returncode == 0, f"table rebuild differs: {r.stdout.strip()} {r.stderr.strip()[-300:]}")
print(f"  acceptance 9: {r.stdout.strip()}")
ref = eos.REFERENCE_ADIABAT["fe_prem"]
PINS = {136e9: 2529.40, 330e9: 3108.07, 1000e9: 4031.53, 3000e9: 5072.76, 12000e9: 6432.07}     # K, to 0.01 K (re-pinned at the C157 reference re-freeze; E0 values before)
for p, t in PINS.items():
    check(abs(ref(p) - t) < 0.01, f"T_ref({p / 1e9:g} GPa) = {ref(p):.4f} K, pinned {t}")
print("  pins: " + " · ".join(f"{p / 1e9:g} GPa {ref(p):.2f} K" for p in PINS))

# ── acceptance 10 (c): the identity at the nodes ──
ph = eos.FE_PREM.phases[0]
worst = 0.0
for lnp, t in zip(ref.lnp, ref.t):
    p = math.exp(lnp)
    if not (ph.p_min <= p <= ph.p_max):
        continue
    dt = ph.delta_t(t, 1600.0, p)
    pth = ph.thermal_pressure(t, 1600.0, p)
    worst = max(worst, abs(dt), abs(pth))
check(worst == 0.0, f"identity: at a table node ΔT or P_th is not exactly 0 (worst {worst!r})")
print(f"  acceptance 10 (c): ΔT and P_th at all {len(ref.lnp)} nodes — worst {worst!r}")

# ── placement and the negative control's switch ──
check(set(eos.REFERENCE_ADIABAT) == {"fe_prem"}, f"tables in use: {sorted(eos.REFERENCE_ADIABAT)}")
si = eos.MATERIALS["silicate"].phases[0]
check(si.delta_t(3000.0, 300.0, 5e9) == 3000.0 * (1.0 - si.t_ref / 300.0), "silicate left today's form")
saved = eos.REFERENCE_ADIABAT.pop("fe_prem")
try:
    today = ph.delta_t(3000.0, 300.0, 500e9)
finally:
    eos.REFERENCE_ADIABAT["fe_prem"] = saved
check(today == 3000.0 * (1.0 - ph.t_ref / 300.0), "without the table fe_prem is not today's form")
check(ph.delta_t(3000.0, 300.0, 500e9) == 3000.0 - ref(500e9), "with the table fe_prem is not T − T_ref(P)")
try:
    ph.delta_t(3000.0, 300.0)
    check(False, "fe_prem ΔT without a pressure did not refuse")
except ValueError:
    pass

# ── records: the field triples pass the engine's own check ──
fake = object()
interior._REF_INFO[id(fake)] = {"fe_steps": 10, "fe_beyond": 4, "fe_dt_min": 2000.0, "fe_dt_max": 5000.0,
                                "si_steps": 3, "si_gap_min": -9000.0}
try:
    v = interior._reference_values(fake)
finally:
    interior._REF_INFO.pop(id(fake))
for pre in ("fe_prem_thermal", "silicate_thermal_pressure"):
    payload.check_provenance(pre, {"grade": v[f"{pre}_grade"], "source": v[f"{pre}_source"],
                                   "counter_evidence_searched": v[f"{pre}_counter_evidence_searched"]})
check(v["fe_prem_dt_beyond_steps"] == 4 and v["silicate_thermal_pressure_steps"] == 3, f"record counts: {v}")
check(len(interior._reference_notes(v)) == 2, "record notes missing")
print(f"  records: fe_prem and silicate triples pass check_provenance · width {interior.REF_DT_WIDTH:.2f} K")

for f in fails:
    print("FAIL", f)
print("test_fe_prem_reference:", "FAIL" if fails else "ok")
sys.exit(1 if fails else 0)
