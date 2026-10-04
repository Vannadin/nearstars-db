# C148 수락 9 · 10 (c) · 4 의 모양 — 기준 단열선 표가 생성기에서 비트까지 다시 나오는가, 다섯 값, 마디에서 열압력이 정확히 0 인가, 기록 세 칸이 엔진의 검사를 통과하는가
"""python3 engine/test_fe_prem_reference.py   (prereg-c148-fe-prem-reference-adiabat 198f3abd)

- Acceptance 9: the generator's `check()` rebuilds `reference_adiabats.json` byte-for-byte, judged on the reference
  machine only since C148 note 2 (fresh process,
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
# C148 덧붙임 2 의 뒤따름 — 생성기 자신의 `check()` 를 **새 프로세스**에서 부른다(생성기는 NEARSTARS_REFERENCE_BUILD=1 을
#   세운 뒤에 엔진을 올려야 하는데 이 시험은 eos 를 먼저 올렸다). 바이트 판정은 기준 기계에서만, 그 밖은 [기록] —
#   맥 재빌드는 PC 표와 t 칸이 최대 2.7e-9 K 다르다(n2-c).
r = subprocess.run([sys.executable, "-c",
                    "import sys; sys.path.insert(0, 'tools'); import reference_adiabats as ra; "
                    "print(ra.check(), ra.machine(), ra.REFERENCE_MACHINE)"],
                   capture_output=True, text=True, cwd=HERE)
_last = (r.stdout.strip().splitlines() or [""])[-1]       # 엔진이 무엇을 찍든 마지막 줄이 check() 의 답이다
_same, _here, _ref = (_last.split() + ["?", "?", "?"])[:3]
if _here == _ref:
    check(r.returncode == 0 and _same == "True", f"table rebuild differs on the reference machine {_here}: "
                                                 f"{r.stdout.strip()} {r.stderr.strip()[-300:]}")
    print(f"  acceptance 9: rebuild {'identical' if _same == 'True' else 'DIFFERS'} ({_here}, judged)")
else:
    check(r.returncode == 0 and _same in ("True", "False"), f"check() did not run: {r.stderr.strip()[-300:]}")
    print(f"  [기록] acceptance 9: rebuild {'identical' if _same == 'True' else 'DIFFERS'} on {_here} "
          f"(judged only on {_ref}, C148 note 2)")
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
