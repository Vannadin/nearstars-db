# 폴리페무스 내측 위성(Hades) 반장축을 훑어 궤도 공명 안정 지형을 매핑하는 스캔 (Dante·Pandora 고정)
"""Resonance-landscape scan for Polyphemus's named moons.

Holds Dante (100,000 km) and Pandora (225,000 km) fixed and steps Hades's
semi-major axis across the inner zone, running each config with IAS15 and
recording MEGNO (chaos), whether Hades stays Hill-bound, and the eccentricity
each inner moon reaches. Maps the stable gaps vs the chaotic resonance-overlap
zones, and labels the mean-motion resonance nearest each step (with Dante below
and Pandora above).

  .venv/bin/python phase3/stability-sim/scripts/resonance_scan.py
"""
import json
import subprocess
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PY = REPO / ".venv/bin/python"
RUN = ROOT / "scripts/run.py"
BASE = ROOT / "hypotheticals/alpha_centauri.json"

A_DANTE = 100_000.0
A_PAN = 225_000.0
YEARS = 40
GRID = list(range(125_000, 172_501, 2_500))

CANDIDATES = [(4, 3), (5, 4), (3, 2), (5, 3), (7, 4), (2, 1),
              (7, 3), (5, 2), (8, 3), (9, 4), (11, 4)]


def label_res(ratio):
    best = None
    for p, q in CANDIDATES:
        r = p / q
        if abs(r - ratio) < 0.015 * ratio:
            d = abs(r - ratio)
            if best is None or d < best[1]:
                best = (f"{p}:{q}", d)
    return best[0] if best else "—"


def main():
    base = json.load(open(BASE))
    tmp = Path(tempfile.mkdtemp(prefix="resscan_"))
    rows = []
    try:
        for aH in GRID:
            spec = json.loads(json.dumps(base))
            for b in spec["bodies"]:
                if b["name"] == "Hades":
                    b["semi_major_axis_km"] = aH
            jp = tmp / f"h_{aH}.json"
            json.dump(spec, open(jp, "w"))
            od = tmp / f"out_{aH}"
            subprocess.run(
                [str(PY), str(RUN), "--system", "alpha_centauri",
                 "--hypotheticals", str(jp), "--acen-a-au", "1.6", "--acen-e", "0.1",
                 "--acen-incl-deg", "16", "--integrator", "ias15",
                 "--years", str(YEARS), "--out", str(od)],
                cwd=REPO, capture_output=True,
            )
            s = json.load(open(od / "alpha_centauri_summary.json"))
            megno = s["integration"]["megno_final"]
            hb = s["hill_track"]["Hades"]
            he = s["per_body"]["Hades"]["e_max"]
            de = s["per_body"]["Dante"]["e_max"]
            pe = s["per_body"]["Pandora"]["e_max"]
            pr_d = (aH / A_DANTE) ** 1.5          # Hades:Dante period ratio
            pr_p = (A_PAN / aH) ** 1.5            # Pandora:Hades period ratio
            rows.append((aH, pr_d, label_res(pr_d), pr_p, label_res(pr_p),
                         megno, hb["bound"], hb["frac_max"], he, de, pe))
            print(f"  {aH:>7} km  megno={megno:9.1f}  bound={hb['bound']}  "
                  f"Hades_emax={he:.3f}  Dante_emax={de:.3f}", flush=True)
    finally:
        out = ROOT / "results" / "_moons_resonance_scan.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w") as f:
            f.write("# Polyphemus inner-moon resonance scan (Hades a, IAS15 "
                    f"{YEARS} yr)\n\n")
            f.write("Dante 100,000 km / Pandora 225,000 km fixed. `res(D)` = MMR with "
                    "Dante below; `res(P)` = MMR with Pandora above.\n\n")
            f.write("| Hades a (km) | P_H:P_D | res(D) | P_P:P_H | res(P) | MEGNO | "
                    "bound | Hill frac | Hades e_max | Dante e_max | Pandora e_max |\n")
            f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
            for (aH, prd, rd, prp, rp, m, b, hf, he, de, pe) in rows:
                f.write(f"| {aH:,} | {prd:.3f} | {rd} | {prp:.3f} | {rp} | "
                        f"{m:,.1f} | {'✅' if b else '✗'} | {hf:.2f} | {he:.3f} | "
                        f"{de:.3f} | {pe:.3f} |\n")
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n→ wrote {out}")


if __name__ == "__main__":
    main()
