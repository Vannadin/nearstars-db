# Dante-Hades 내측 위성 쌍의 평균운동공명(MMR) 후보를 정밀 검증 — 안정성 + 공명각 libration 분석
"""Inner-pair mean-motion-resonance study for Polyphemus's moons.

The 1-D scan (resonance_scan.py) only varied Hades and mapped stable-vs-chaotic.
Here we test specific Dante:Hades resonance candidates that dodge Pandora's
(fixed, observation-pinned) resonance locations, and — crucially — compute the
**resonant argument** from the timeseries to tell whether the pair is actually
*locked* (the argument librates about a center) or merely near a period ratio
(the argument circulates). A true lock is what, with tides, would keep Hades's
eccentricity pumped — the physical justification for the canon tidal heating.

  .venv/bin/python phase3/stability-sim/scripts/resonance_lock_study.py
"""
import csv
import json
import math
import subprocess
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PY = REPO / ".venv/bin/python"
RUN = ROOT / "scripts/run.py"
BASE = ROOT / "hypotheticals/alpha_centauri.json"
YEARS = 300
SNAPS = 1500

# (label, a_Dante_km, a_Hades_km, resonance (p:q) outer:inner to analyse)
CONFIGS = [
    ("3:2  D100/H128", 100_000, 128_000, (3, 2)),
    ("3:2  D100/H130", 100_000, 130_000, (3, 2)),
    ("3:2* D100/H131", 100_000, 131_000, (3, 2)),   # exact 3:2
    ("3:2  D100/H132", 100_000, 132_000, (3, 2)),
    ("gap  D100/H135", 100_000, 135_000, (3, 2)),   # current config — expect circulation
    ("2:1  D105/H167", 105_000, 166_677, (2, 1)),
]


def f_to_M(f_deg, e):
    f = math.radians(f_deg)
    E = math.atan2(math.sqrt(max(0.0, 1 - e * e)) * math.sin(f), e + math.cos(f))
    return E - e * math.sin(E)           # radians


def wrap180(x):
    return (x + 180.0) % 360.0 - 180.0


def coverage_deg(phis):
    """360 minus the largest circular gap → how much of the circle the argument
    spans. ~360 = circulation; small = libration (this value ≈ libration width)."""
    s = sorted(p % 360.0 for p in phis)
    if len(s) < 2:
        return 360.0
    gaps = [s[i + 1] - s[i] for i in range(len(s) - 1)] + [360.0 - s[-1] + s[0]]
    return 360.0 - max(gaps)


def analyse(csv_path, p, q):
    # collect Dante/Hades elements per time
    byt = {}
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            if r["body"] in ("Dante", "Hades"):
                byt.setdefault(r["t_yr"], {})[r["body"]] = r
    phi_pH, phi_pD = [], []
    for t, bd in byt.items():
        if "Dante" not in bd or "Hades" not in bd:
            continue
        D, H = bd["Dante"], bd["Hades"]
        lamD = (float(D["Omega_deg"]) + float(D["omega_deg"])
                + math.degrees(f_to_M(float(D["f_deg"]), float(D["e"]))))
        lamH = (float(H["Omega_deg"]) + float(H["omega_deg"])
                + math.degrees(f_to_M(float(H["f_deg"]), float(H["e"]))))
        pomD = float(D["Omega_deg"]) + float(D["omega_deg"])
        pomH = float(H["Omega_deg"]) + float(H["omega_deg"])
        # outer=Hades, inner=Dante: phi = p*lamH - q*lamD - (p-q)*pom
        phi_pH.append(wrap180(p * lamH - q * lamD - (p - q) * pomH))
        phi_pD.append(wrap180(p * lamH - q * lamD - (p - q) * pomD))
    cH, cD = coverage_deg(phi_pH), coverage_deg(phi_pD)
    return min(cH, cD), cH, cD


def main():
    base = json.load(open(BASE))
    tmp = Path(tempfile.mkdtemp(prefix="reslock_"))
    rows = []
    try:
        for label, aD, aH, (p, q) in CONFIGS:
            spec = json.loads(json.dumps(base))
            for b in spec["bodies"]:
                if b["name"] == "Dante":
                    b["semi_major_axis_km"] = aD
                if b["name"] == "Hades":
                    b["semi_major_axis_km"] = aH
            jp = tmp / f"{aD}_{aH}.json"
            json.dump(spec, open(jp, "w"))
            od = tmp / f"out_{aD}_{aH}"
            subprocess.run(
                [str(PY), str(RUN), "--system", "alpha_centauri",
                 "--hypotheticals", str(jp), "--acen-a-au", "1.6", "--acen-e", "0.1",
                 "--acen-incl-deg", "16", "--integrator", "ias15",
                 "--years", str(YEARS), "--snapshots", str(SNAPS), "--out", str(od)],
                cwd=REPO, capture_output=True,
            )
            s = json.load(open(od / "alpha_centauri_summary.json"))
            megno = s["integration"]["megno_final"]
            hb = s["hill_track"]["Hades"]
            he = s["per_body"]["Hades"]["e_max"]
            cov, cH, cD = analyse(od / "alpha_centauri_timeseries.csv", p, q)
            lock = "LIBRATES (locked)" if cov < 320 else "circulates (not locked)"
            rows.append((label, p, q, megno, hb["bound"], he, cov, lock))
            print(f"  {label}  megno={megno:8.1f}  bound={hb['bound']}  "
                  f"Hades_emax={he:.3f}  φ-coverage={cov:.0f}°  {lock}", flush=True)
    finally:
        out = ROOT / "results" / "_moons_resonance_lock.md"
        with out.open("w") as f:
            f.write(f"# Inner-pair MMR lock study (Dante:Hades, IAS15 {YEARS} yr, "
                    f"{SNAPS} samples)\n\n")
            f.write("Pandora fixed at 225,000 km (observation). `φ-coverage` = how much "
                    "of the 0–360° circle the resonant argument spans: small = the "
                    "argument **librates** (true resonance lock); ~360 = it **circulates** "
                    "(not locked, just near a period ratio).\n\n")
            f.write("| config | resonance | MEGNO | bound | Hades e_max | φ-coverage | verdict |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for (label, p, q, m, b, he, cov, lock) in rows:
                f.write(f"| {label} | {p}:{q} | {m:,.1f} | {'✅' if b else '✗'} | "
                        f"{he:.3f} | {cov:.0f}° | {lock} |\n")
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n→ wrote {out}")


if __name__ == "__main__":
    main()
