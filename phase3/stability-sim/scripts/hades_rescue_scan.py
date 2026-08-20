# Hades 이탈(5.6만 년)을 막는 최소 변경 궤도 탐색 — 장반경만 훑는 장기(10⁵년) 스캔.
"""Minimal-change rescue scan for Hades.

The shipped Hades (a = 148,000 km) is chaotically ejected at ~56 kyr (confirmed
at two step sizes). It sits 0.7% outside Pandora's 9:4 mean-motion resonance
(146.9k km; Pandora is 860x Hades' mass) and 2.6% outside Dante's 3:2 (144.1k).
The original resonance_scan.py mapped this zone with a 40-YEAR horizon — far too
short to see the 5e4-yr channel. This scan steps ONLY Hades' semi-major axis
across 138k–162k km (everything else fixed, same manifest-cell configuration)
and integrates each candidate for 1e5 yr — ~2x the observed ejection time — with
the standard leapfrog 10-min step and the C J2 force.

Verdict per candidate: Hill-bound at the end + max eccentricity + nearest
resonances with Dante (below) and Pandora (above), so the survivor map reads
directly against the resonance landscape.

  .venv/bin/python scripts/hades_rescue_scan.py [--jobs 6]

Each run ≈ 22 min; the full grid on 6 cores ≈ 1 h. Results land in
results/hades_rescue/a_<km>/ + a summary table on stdout and
results/hades_rescue/scan_summary.json.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
RUN = ROOT / "scripts" / "run.py"
BASE = ROOT / "hypotheticals" / "alpha_centauri.json"
OUT = ROOT / "results" / "hades_rescue"

GRID_KM = list(range(138_000, 162_001, 2_000))
YEARS = "1e5"
SNAPSHOTS = "2000"
# same cell configuration as the validation manifest's moon rows
CELL_ARGS = ["--acen-a-au", "1.6", "--acen-e", "0.1", "--acen-incl-deg", "16",
             "--j2", "0.023", "--j2-obliquity-deg", "5",
             "--integrator", "leapfrog", "--dt-minutes", "10"]

A_DANTE_KM = 110_000.0
A_PANDORA_KM = 252_393.0


def nearest_resonance(a_km: float, a_other_km: float, inner: bool) -> str:
    """Nearest LOW-ORDER period ratio to the other moon (q ≤ 4 — higher orders
    are dynamically too weak to matter for this map)."""
    ratio = (max(a_km, a_other_km) / min(a_km, a_other_km)) ** 1.5
    best = None
    for q in range(1, 5):
        for p in range(q + 1, 3 * q + 1):
            r = p / q
            off = abs(r - ratio) / ratio
            if best is None or off < best[0]:
                best = (off, p, q)
    off, p, q = best
    who = "Dante" if inner else "Pandora"
    return f"{p}:{q} {who} ({off * 100:.1f}%)"


# short aliases for the Hades fields a candidate may vary, and the directory tag
FIELDS = {"a": "semi_major_axis_km", "e": "eccentricity",
          "i": "inclination_deg", "ma": "mean_anomaly_deg"}


DT_MINUTES = 10.0          # set by --dt-minutes; halving it is the resolution test


def run_candidate(spec: dict) -> dict:
    """One candidate = a dict of {short_field: value} overrides on Hades."""
    # a-only keeps the original `a_<km>` directory name so the 35 completed
    # semi-major-axis runs are reused rather than recomputed
    tag = (f"a_{spec['a']:g}" if list(spec) == ["a"]
           else "_".join(f"{k}{spec[k]:g}" for k in sorted(spec)))
    if DT_MINUTES != 10.0:                 # keep the finer-step twin in its own dir
        tag += f"_dt{DT_MINUTES:g}"
    out_dir = OUT / tag
    summary = out_dir / "alpha_centauri_summary.json"
    if not summary.exists():
        hyp = json.loads(BASE.read_text())
        for m in hyp["bodies"]:
            if m["name"] == "Hades":
                for k, v in spec.items():
                    m[FIELDS[k]] = v
        out_dir.mkdir(parents=True, exist_ok=True)
        tmp = out_dir / "hypotheticals.json"
        tmp.write_text(json.dumps(hyp, indent=1))
        cell = list(CELL_ARGS)
        cell[cell.index("--dt-minutes") + 1] = f"{DT_MINUTES:g}"
        cmd = [PY, str(RUN), "--system", "alpha_centauri",
               "--hypotheticals", str(tmp), *cell,
               "--years", YEARS, "--snapshots", SNAPSHOTS,
               "--out-dir", str(out_dir)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        (out_dir / "run.log").write_text(r.stdout + r.stderr)
        if r.returncode != 0:
            return {"tag": tag, "spec": spec, "error": f"run failed rc={r.returncode}"}
    d = json.loads(summary.read_text())
    a_km = spec.get("a", 148_000)
    res = {"tag": tag, "spec": spec,
           "res_dante": nearest_resonance(a_km, A_DANTE_KM, inner=True),
           "res_pandora": nearest_resonance(a_km, A_PANDORA_KM, inner=False)}
    for name, pb in d["per_body"].items():
        bound = d["hill_track"].get(name, {}).get("bound", True)
        if name == "Hades":
            res.update(hades_bound=bound, hades_e_max=pb["e_max"])
        elif not bound or pb["e_max"] >= 0.9:
            res.setdefault("collateral", []).append(name)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--grid", action="append", metavar="MIN:MAX:STEP",
                    help="semi-major-axis range(s) in km (repeatable); default = the "
                         "built-in 138k–162k zone around the shipped orbit")
    ap.add_argument("--vary", action="append", metavar="FIELD:v1,v2,...",
                    help=f"vary one Hades field over a list; FIELD ∈ {sorted(FIELDS)} "
                         "(repeatable — each list is scanned separately, other fields "
                         "stay at their shipped values)")
    ap.add_argument("--combo", action="append", metavar="f=v,f=v",
                    help="one candidate with several fields set at once (repeatable)")
    ap.add_argument("--dt-minutes", type=float, default=10.0,
                    help="timestep for this invocation (default 10 = the Principia "
                         "proxy). Halve it to test whether a survivor is real or a "
                         "fixed-step artifact; results land in a separate `_dt<N>` dir.")
    args = ap.parse_args()

    global DT_MINUTES
    DT_MINUTES = args.dt_minutes

    specs = []
    if args.grid:
        for g in args.grid:
            lo, hi, step = (int(x) for x in g.split(":"))
            specs += [{"a": v} for v in range(lo, hi + 1, step)]
    for v in (args.vary or []):
        field, vals = v.split(":")
        specs += [{field: float(x)} for x in vals.split(",")]
    for c in (args.combo or []):
        specs.append({k: float(v) for k, v in (kv.split("=") for kv in c.split(","))})
    if not specs:
        specs = [{"a": v} for v in GRID_KM]

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        rows = list(ex.map(run_candidate, specs))

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"scan_summary_{len(rows)}.json").write_text(json.dumps(rows, indent=1))
    print(f"\n{'candidate':>16}  {'survives':8}  {'e_max':>7}  nearest resonances")
    for r in rows:
        if "error" in r:
            print(f"{r['tag']:>16}  {r['error']}")
            continue
        ok = "BOUND" if r["hades_bound"] and r["hades_e_max"] < 0.9 else "EJECTED"
        extra = f"  ! also: {','.join(r['collateral'])}" if r.get("collateral") else ""
        print(f"{r['tag']:>16}  {ok:8}  {min(r['hades_e_max'], 9.999):>7.3f}"
              f"  {r['res_dante']} · {r['res_pandora']}{extra}")


if __name__ == "__main__":
    main()
