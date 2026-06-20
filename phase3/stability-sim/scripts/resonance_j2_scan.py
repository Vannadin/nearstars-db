# J2 켠 상태에서 Dante:Hades 공명 반장축을 쓸어 살아남는 공명 락이 있는지 찾는 스캔
"""J2-aware resonance scan for the Dante-Hades inner pair.

The point-mass resonance_lock_study found the 3:2 (Hades 131k, M0=180°) librates,
but with Polyphemus's J2 injected that lock ejects Hades (~510 yr) — J2's strong
inner-moon precession (R_Jup/a ≈ 0.5 at Hades) detunes it. This sweeps Hades's
semi-major axis across the low-a resonances that dodge Pandora (5:4, 4:3, 3:2)
WITH J2 on, to test whether any resonance survives — and whether J2 shifts the
working 3:2 location off 131k. A surviving lock would restore a self-consistent
tidal-heating eccentricity for Hades; none would confirm the documented limitation.

Hades starts at M0=180° (the phase that librated point-mass). J2=0.023, TRACE.

  .venv/bin/python phase3/stability-sim/scripts/resonance_j2_scan.py
"""
import csv
import json
import math
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PY = REPO / ".venv/bin/python"
RUN = ROOT / "scripts/run.py"
BASE = ROOT / "hypotheticals/_acen_3to2lock.json"   # has Hades M0=180
YEARS = 600
SNAPS = 2000
WORKERS = 4
J2 = "0.023"

# (label, a_Dante_km, a_Hades_km, resonance (p:q) outer:inner)
CONFIGS = [
    ("5:4  H116", 100_000, 116_000, (5, 4)),
    ("4:3  H121", 100_000, 121_000, (4, 3)),
    ("3:2  H129", 100_000, 129_000, (3, 2)),
    ("3:2* H131", 100_000, 131_000, (3, 2)),   # exact point-mass 3:2
    ("3:2  H133", 100_000, 133_000, (3, 2)),
    ("gap  H135", 100_000, 135_000, (3, 2)),   # off-resonance reference
]

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resonance_lock_study import f_to_M, wrap180, coverage_deg  # noqa: E402


def analyse(csv_path, p, q):
    """φ-coverage (min over the two pericenter choices) + Hades e over the run."""
    byt = {}
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            if r["body"] in ("Dante", "Hades"):
                byt.setdefault(r["t_yr"], {})[r["body"]] = r
    phi_pH, phi_pD, e_hist = [], [], []
    for t, bd in byt.items():
        if "Dante" not in bd or "Hades" not in bd:
            continue
        D, H = bd["Dante"], bd["Hades"]
        lamD = float(D["Omega_deg"]) + float(D["omega_deg"]) + math.degrees(f_to_M(float(D["f_deg"]), float(D["e"])))
        lamH = float(H["Omega_deg"]) + float(H["omega_deg"]) + math.degrees(f_to_M(float(H["f_deg"]), float(H["e"])))
        pomD = float(D["Omega_deg"]) + float(D["omega_deg"])
        pomH = float(H["Omega_deg"]) + float(H["omega_deg"])
        phi_pH.append(wrap180(p * lamH - q * lamD - (p - q) * pomH))
        phi_pD.append(wrap180(p * lamH - q * lamD - (p - q) * pomD))
        e_hist.append((float(t), float(H["e"])))
    cov = min(coverage_deg(phi_pH), coverage_deg(phi_pD))
    # mean Hades e over the last half (a sustained-high value = resonance maintaining it)
    e_hist.sort()
    last_half = [e for (t, e) in e_hist[len(e_hist) // 2:] if e < 1.0]
    e_late = sum(last_half) / len(last_half) if last_half else float("nan")
    return cov, e_late


def one(tmp, base, label, aD, aH, pq):
    spec = json.loads(json.dumps(base))
    for b in spec["bodies"]:
        if b["name"] == "Dante":
            b["semi_major_axis_km"] = aD
        if b["name"] == "Hades":
            b["semi_major_axis_km"] = aH   # M0=180 already in the base file
    jp = tmp / f"{aH}.json"
    json.dump(spec, open(jp, "w"))
    od = tmp / f"out_{aH}"
    subprocess.run(
        [str(PY), str(RUN), "--system", "alpha_centauri", "--hypotheticals", str(jp),
         "--acen-a-au", "1.6", "--acen-e", "0.1", "--acen-incl-deg", "16",
         "--integrator", "trace", "--years", str(YEARS), "--snapshots", str(SNAPS),
         "--j2", J2, "--out", str(od)],
        cwd=REPO, capture_output=True,
    )
    s = json.load(open(od / "alpha_centauri_summary.json"))
    bound = s["hill_track"]["Hades"]["bound"]
    he_max = s["per_body"]["Hades"]["e_max"]
    p, q = pq
    cov, e_late = analyse(od / "alpha_centauri_timeseries.csv", p, q)
    lock = "LIBRATES" if (cov < 320 and bound) else ("ejected" if not bound else "circulates")
    print(f"  {label}  bound={bound}  Hades e_max={he_max:8.3f}  e_late={e_late:.3f}  "
          f"φ-cov={cov:.0f}°  {lock}", flush=True)
    return (label, p, q, bound, he_max, e_late, cov, lock)


def main():
    base = json.load(open(BASE))
    tmp = Path(tempfile.mkdtemp(prefix="resj2_"))
    rows = []
    try:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            rows = list(ex.map(lambda c: one(tmp, base, *c), CONFIGS))
    finally:
        out = ROOT / "results" / "_moons_resonance_j2_scan.md"
        with out.open("w") as f:
            f.write(f"# J2-aware Dante:Hades resonance scan (TRACE {YEARS} yr, J2={J2}, Hades M0=180°)\n\n")
            f.write("Does any inner-pair resonance survive Polyphemus's J2? `φ-cov` <320° "
                    "with bound = a true lock; `e_late` = mean Hades eccentricity over the "
                    "last half (a sustained high value = the resonance is maintaining it for "
                    "tidal heating).\n\n")
            f.write("| config | resonance | bound | Hades e_max | e_late | φ-coverage | verdict |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for (label, p, q, bound, he_max, e_late, cov, lock) in rows:
                f.write(f"| {label} | {p}:{q} | {'✅' if bound else '✗ EJECT'} | "
                        f"{he_max:.3f} | {e_late:.3f} | {cov:.0f}° | {lock} |\n")
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n→ wrote {out}")


if __name__ == "__main__":
    main()
