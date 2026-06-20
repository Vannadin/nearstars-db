# 위성에 점증하는 경사각 spread를 줘 (시각적 sky-위도 분산용) 동역학 안정 한계를 찾는 스캔
"""Inclination-spread scan for Polyphemus's moons.

Art-direction wants larger orbital inclinations so the moons spread over different
sky latitudes from Pandora (instead of stacking on one line). This scans a spread
parameter s: each moon is tilted proportionally (Pandora kept at its canon
equatorial plane), and MEGNO / bound / peak eccentricity are recorded to find how
large the spread can get before Kozai or mutual-inclination instability sets in.

Base = the gated coplanar config (Hades 135k). Runs concurrently.

  .venv/bin/python phase3/stability-sim/scripts/inclination_scan.py
"""
import json
import os
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
YEARS = 300
SNAPS = 800
# Set STAB_J2=0.023 to inject Polyphemus's J2 (forwarded to run.py --j2).
# With J2 the per-step Python force makes IAS15 (~12 force-calls/step) impractical,
# so J2 runs use TRACE (~1-2 calls/step, ~11x faster, handles the binary; no MEGNO).
J2 = os.environ.get("STAB_J2")
J2_ARGS = ["--j2", J2] if J2 else []
INTEG = "trace" if J2 else "ias15"
WORKERS = 4                 # leave a core for the parallel long-confirm run
SPREADS = [3, 6, 10, 15, 20, 25, 30, 40]   # degrees

# inclination_deg assigned per moon as a function of spread s (Pandora stays 0;
# Cassandra/Chaos are retrograde ~180, tilted off the retrograde plane).
def incl(name, s):
    return {"Dante": 0.5 * s, "Hades": 1.0 * s, "Pandora": 0.0,
            "Cassandra": 180.0 - 0.7 * s, "Chaos": 180.0 - 1.2 * s}[name]


def one(tmp, base, s):
    spec = json.loads(json.dumps(base))
    for b in spec["bodies"]:
        b["inclination_deg"] = incl(b["name"], s)
    jp = tmp / f"s_{s}.json"
    json.dump(spec, open(jp, "w"))
    od = tmp / f"out_{s}"
    subprocess.run(
        [str(PY), str(RUN), "--system", "alpha_centauri", "--hypotheticals", str(jp),
         "--acen-a-au", "1.6", "--acen-e", "0.1", "--acen-incl-deg", "16",
         "--integrator", INTEG, "--years", str(YEARS), "--snapshots", str(SNAPS),
         *J2_ARGS, "--out", str(od)],
        cwd=REPO, capture_output=True,
    )
    s_j = json.load(open(od / "alpha_centauri_summary.json"))
    hill = s_j["hill_track"]
    allbound = all(m["bound"] for m in hill.values())
    # worst (highest) eccentricity among the moons + which
    emap = {n: s_j["per_body"][n]["e_max"] for n in hill}
    worst = max(emap, key=emap.get)
    res = (s, s_j["integration"]["megno_final"], allbound, worst, emap[worst])
    mg = f"{res[1]:9.1f}" if res[1] is not None else "    n/a  "
    print(f"  spread={s:3d}°  megno={mg}  all_bound={allbound}  "
          f"worst e_max={emap[worst]:.3f} ({worst})", flush=True)
    return res


def main():
    base = json.load(open(BASE))
    tmp = Path(tempfile.mkdtemp(prefix="inclscan_"))
    try:
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            rows = sorted(ex.map(lambda s: one(tmp, base, s), SPREADS))
    finally:
        out = ROOT / "results" / "_moons_inclination_scan.md"
        with out.open("w") as f:
            f.write(f"# Inclination-spread scan ({INTEG.upper()} {YEARS} yr"
                    f"{', J2='+J2 if J2 else ', point-mass'})\n\n")
            f.write("Spread `s` (deg): Dante 0.5s, Hades 1.0s, Pandora 0 (canon "
                    "equatorial), Cassandra 180−0.7s, Chaos 180−1.2s (retrograde). "
                    "Tests how large a visual sky-latitude spread stays dynamically "
                    "stable.\n\n")
            f.write("| spread s | MEGNO | all bound | worst moon e_max |\n")
            f.write("|---|---|---|---|\n")
            for (s, m, ab, worst, we) in rows:
                mg = f"{m:,.1f}" if m is not None else "n/a"
                f.write(f"| {s}° | {mg} | {'✅' if ab else '✗ EJECT'} | "
                        f"{we:.3f} ({worst}) |\n")
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n→ wrote {out}")


if __name__ == "__main__":
    main()
