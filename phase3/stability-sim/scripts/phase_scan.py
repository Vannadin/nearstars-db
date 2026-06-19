# 3:2 후보(Dante/Hades)의 초기 위상(Hades 평균근점이각)을 훑어 공명 락이 위상-무관하게 불가능한지 검증
"""Initial-phase scan for the Dante:Hades 3:2 resonance candidate.

All earlier runs used a single fixed phase (every moon at pericenter, M=0). The
3:2 (Hades 131k) was the only capture candidate; resonance capture is phase-
sensitive, so this scans Hades's initial mean anomaly across the full circle and
checks whether *any* starting phase produces a libration (a true lock) instead of
the circulation seen at M=0. If all phases circulate, the no-lock conclusion is
phase-robust.

Runs concurrently (pool sized to the P-cores).

  .venv/bin/python phase3/stability-sim/scripts/phase_scan.py
"""
import csv
import json
import math
import subprocess
import tempfile
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PY = REPO / ".venv/bin/python"
RUN = ROOT / "scripts/run.py"
BASE = ROOT / "hypotheticals/alpha_centauri.json"

A_DANTE = 100_000
A_HADES = 131_000          # exact 3:2 with Dante
P, Q = 3, 2                # outer:inner = Hades:Dante
YEARS = 300
SNAPS = 1500
PHASES = list(range(0, 360, 30))   # Hades initial mean anomaly (deg)
WORKERS = 5                # match the M5 Pro performance cores


def f_to_M(f_deg, e):
    f = math.radians(f_deg)
    E = math.atan2(math.sqrt(max(0.0, 1 - e * e)) * math.sin(f), e + math.cos(f))
    return E - e * math.sin(E)


def wrap180(x):
    return (x + 180.0) % 360.0 - 180.0


def coverage_deg(phis):
    s = sorted(p % 360.0 for p in phis)
    if len(s) < 2:
        return 360.0
    gaps = [s[i + 1] - s[i] for i in range(len(s) - 1)] + [360.0 - s[-1] + s[0]]
    return 360.0 - max(gaps)


def analyse(csv_path):
    byt = {}
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            if r["body"] in ("Dante", "Hades"):
                byt.setdefault(r["t_yr"], {})[r["body"]] = r
    phiH, phiD = [], []
    for bd in byt.values():
        if "Dante" not in bd or "Hades" not in bd:
            continue
        D, H = bd["Dante"], bd["Hades"]
        lamD = (float(D["Omega_deg"]) + float(D["omega_deg"])
                + math.degrees(f_to_M(float(D["f_deg"]), float(D["e"]))))
        lamH = (float(H["Omega_deg"]) + float(H["omega_deg"])
                + math.degrees(f_to_M(float(H["f_deg"]), float(H["e"]))))
        pomD = float(D["Omega_deg"]) + float(D["omega_deg"])
        pomH = float(H["Omega_deg"]) + float(H["omega_deg"])
        phiH.append(wrap180(P * lamH - Q * lamD - (P - Q) * pomH))
        phiD.append(wrap180(P * lamH - Q * lamD - (P - Q) * pomD))
    return min(coverage_deg(phiH), coverage_deg(phiD))


def one(tmp, base, phase):
    spec = json.loads(json.dumps(base))
    for b in spec["bodies"]:
        if b["name"] == "Dante":
            b["semi_major_axis_km"] = A_DANTE
        if b["name"] == "Hades":
            b["semi_major_axis_km"] = A_HADES
            b["mean_anomaly_deg"] = phase
    jp = tmp / f"ph_{phase}.json"
    json.dump(spec, open(jp, "w"))
    od = tmp / f"out_{phase}"
    subprocess.run(
        [str(PY), str(RUN), "--system", "alpha_centauri", "--hypotheticals", str(jp),
         "--acen-a-au", "1.6", "--acen-e", "0.1", "--acen-incl-deg", "16",
         "--integrator", "ias15", "--years", str(YEARS), "--snapshots", str(SNAPS),
         "--out", str(od)],
        cwd=REPO, capture_output=True,
    )
    s = json.load(open(od / "alpha_centauri_summary.json"))
    cov = analyse(od / "alpha_centauri_timeseries.csv")
    res = (phase, s["integration"]["megno_final"], s["hill_track"]["Hades"]["bound"],
           s["per_body"]["Hades"]["e_max"], cov)
    print(f"  Hades M0={phase:3d}°  megno={res[1]:8.1f}  bound={res[2]}  "
          f"e_max={res[3]:.3f}  φ-coverage={cov:.0f}°  "
          f"{'LIBRATES' if cov < 320 else 'circulates'}", flush=True)
    return res


def main():
    base = json.load(open(BASE))
    tmp = Path(tempfile.mkdtemp(prefix="phasescan_"))
    try:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            rows = sorted(ex.map(lambda ph: one(tmp, base, ph), PHASES))
    finally:
        out = ROOT / "results" / "_moons_phase_scan.md"
        with out.open("w") as f:
            f.write(f"# Initial-phase scan — Dante:Hades 3:2 (Hades {A_HADES:,} km, "
                    f"IAS15 {YEARS} yr)\n\n")
            f.write("Scans Hades's initial mean anomaly (M0) across the full circle. "
                    "`φ-coverage` small = the 3:2 argument **librates** (locked); ~360 = "
                    "**circulates** (not captured at this phase).\n\n")
            f.write("| Hades M0 | MEGNO | bound | Hades e_max | φ-coverage | verdict |\n")
            f.write("|---|---|---|---|---|---|\n")
            for (ph, m, b, he, cov) in rows:
                f.write(f"| {ph}° | {m:,.1f} | {'✅' if b else '✗'} | {he:.3f} | "
                        f"{cov:.0f}° | {'LIBRATES (locked)' if cov < 320 else 'circulates'} |\n")
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n→ wrote {out}")


if __name__ == "__main__":
    main()
