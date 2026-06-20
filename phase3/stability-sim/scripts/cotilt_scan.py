# 내측 쌍(Dante+Hades)을 공통 틸트 θ로 함께 기울여 3:2 락 생존 + 상호경사 드리프트를 보는 스캔
"""Inner-pair co-tilt scan for Polyphemus's moons (J2-aware).

The inclination_scan tilts each moon by a *different* amount (Dante 0.5s, Hades
1.0s), which gives the inner pair a mutual inclination and detunes the 3:2 lock.
This scan instead tilts Dante and Hades by the SAME angle θ with the same node
(load.add_hypotheticals gives every moon the parent's node), so the inner pair
stays mutually coplanar at t=0 — the user's "co-tilt" idea to combine the
self-consistent 3:2 heating with a visual sky-latitude offset from equatorial
Pandora.

For each θ it measures, from the timeseries:
  - 3:2 φ-libration coverage (lock persistence; <320° = locked),
  - Dante-Hades mutual inclination over time (the prime detune risk — differential
    nodal precession from different a; J2 is expected to SUPPRESS this drift),
  - bound / MEGNO / Hades e_max.

Base = the 3:2-lock variant (Hades 131k, M0=180). Set STAB_J2=0.023 to inject J2.

  STAB_J2=0.023 .venv/bin/python phase3/stability-sim/scripts/cotilt_scan.py
"""
import json
import math
import os
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
BASE = ROOT / "hypotheticals/_acen_3to2lock.json"
YEARS = 300
SNAPS = 2000
WORKERS = 4
TILTS = [0, 10, 15, 20, 25, 30]   # common θ (deg) applied to Dante and Hades
J2 = os.environ.get("STAB_J2")
J2_ARGS = ["--j2", J2] if J2 else []
# J2 runs use TRACE (IAS15's ~12 force-calls/step makes the Python J2 force too slow).
INTEG = "trace" if J2 else "ias15"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resonance_lock_study import f_to_M, wrap180, coverage_deg  # noqa: E402


def mutual_incl_max(csv_path):
    """Max Dante-Hades mutual inclination (deg) over the run."""
    import csv
    byt = {}
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            if r["body"] in ("Dante", "Hades"):
                byt.setdefault(r["t_yr"], {})[r["body"]] = r
    worst = 0.0
    for bd in byt.values():
        if "Dante" not in bd or "Hades" not in bd:
            continue
        i1, O1 = math.radians(float(bd["Dante"]["inc_deg"])), math.radians(float(bd["Dante"]["Omega_deg"]))
        i2, O2 = math.radians(float(bd["Hades"]["inc_deg"])), math.radians(float(bd["Hades"]["Omega_deg"]))
        c = math.cos(i1) * math.cos(i2) + math.sin(i1) * math.sin(i2) * math.cos(O1 - O2)
        worst = max(worst, math.degrees(math.acos(max(-1.0, min(1.0, c)))))
    return worst


def phi_coverage(csv_path, p=3, q=2):
    """3:2 resonant-argument coverage (min over the two pericenter choices)."""
    import csv
    byt = {}
    with open(csv_path) as f:
        for r in csv.DictReader(f):
            if r["body"] in ("Dante", "Hades"):
                byt.setdefault(r["t_yr"], {})[r["body"]] = r
    phi_pH, phi_pD = [], []
    for bd in byt.values():
        if "Dante" not in bd or "Hades" not in bd:
            continue
        D, H = bd["Dante"], bd["Hades"]
        lamD = float(D["Omega_deg"]) + float(D["omega_deg"]) + math.degrees(f_to_M(float(D["f_deg"]), float(D["e"])))
        lamH = float(H["Omega_deg"]) + float(H["omega_deg"]) + math.degrees(f_to_M(float(H["f_deg"]), float(H["e"])))
        pomD = float(D["Omega_deg"]) + float(D["omega_deg"])
        pomH = float(H["Omega_deg"]) + float(H["omega_deg"])
        phi_pH.append(wrap180(p * lamH - q * lamD - (p - q) * pomH))
        phi_pD.append(wrap180(p * lamH - q * lamD - (p - q) * pomD))
    return min(coverage_deg(phi_pH), coverage_deg(phi_pD))


def one(tmp, base, theta):
    spec = json.loads(json.dumps(base))
    for b in spec["bodies"]:
        if b["name"] in ("Dante", "Hades"):
            b["inclination_deg"] = float(theta)
    jp = tmp / f"th_{theta}.json"
    json.dump(spec, open(jp, "w"))
    od = tmp / f"out_{theta}"
    subprocess.run(
        [str(PY), str(RUN), "--system", "alpha_centauri", "--hypotheticals", str(jp),
         "--acen-a-au", "1.6", "--acen-e", "0.1", "--acen-incl-deg", "16",
         "--integrator", INTEG, "--years", str(YEARS), "--snapshots", str(SNAPS),
         *J2_ARGS, "--out", str(od)],
        cwd=REPO, capture_output=True,
    )
    s = json.load(open(od / "alpha_centauri_summary.json"))
    csv_path = od / "alpha_centauri_timeseries.csv"
    megno = s["integration"]["megno_final"]
    bound = all(m["bound"] for m in s["hill_track"].values())
    he = s["per_body"]["Hades"]["e_max"]
    cov = phi_coverage(csv_path)
    imut = mutual_incl_max(csv_path)
    lock = "LIBRATES" if cov < 320 else "circulates"
    mg = f"{megno:9.1f}" if megno is not None else "    n/a  "
    print(f"  θ={theta:3d}°  megno={mg}  bound={bound}  Hades_emax={he:.3f}  "
          f"φ-cov={cov:.0f}°  i_mut_max={imut:.2f}°  {lock}", flush=True)
    return (theta, megno, bound, he, cov, imut, lock)


def main():
    base = json.load(open(BASE))
    tmp = Path(tempfile.mkdtemp(prefix="cotilt_"))
    try:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            rows = sorted(ex.map(lambda th: one(tmp, base, th), TILTS))
    finally:
        out = ROOT / "results" / "_moons_cotilt_scan.md"
        with out.open("w") as f:
            f.write(f"# Inner-pair co-tilt scan (3:2-lock base, {INTEG.upper()} {YEARS} yr"
                    f"{', J2='+J2 if J2 else ', point-mass'})\n\n")
            f.write("Dante and Hades tilted by the SAME angle θ with a shared node "
                    "(mutual inclination 0 at t=0), on the 3:2-lock base (Hades 131k, "
                    "M0=180°). `φ-cov` <320° = the 3:2 lock survives the tilt; "
                    "`i_mut_max` = peak Dante-Hades mutual inclination (detune risk — "
                    "J2 should suppress it).\n\n")
            f.write("| θ | MEGNO | bound | Hades e_max | φ-coverage | i_mut max | lock |\n")
            f.write("|---|---|---|---|---|---|---|\n")
            for (th, m, b, he, cov, imut, lock) in rows:
                mg = f"{m:,.1f}" if m is not None else "n/a"
                f.write(f"| {th}° | {mg} | {'✅' if b else '✗ EJECT'} | {he:.3f} | "
                        f"{cov:.0f}° | {imut:.2f}° | {lock} |\n")
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n→ wrote {out}")


if __name__ == "__main__":
    main()
