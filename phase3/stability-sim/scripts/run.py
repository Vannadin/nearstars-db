#!/usr/bin/env python3
# 안정성 시뮬레이션 메인 엔트리. WHFast + MEGNO 로 N-body 적분 후 보고서 생성.
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

import rebound

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from load import (  # noqa: E402
    build_alpha_cen_ab,
    build_planetary_system,
    add_hypotheticals,
    hill_radius,
    KM_PER_AU,
)

SYSTEMS = {
    "trappist_1": ("planetary", PROJECT_ROOT / "db/systems/trappist_1.json"),
    "proxima_cen": ("planetary", PROJECT_ROOT / "db/systems/proxima_cen.json"),
    "alpha_centauri": ("binary", PROJECT_ROOT / "db/systems"),
}


def build(system: str, hyp_path: Path | None):
    kind, src = SYSTEMS[system]
    if kind == "planetary":
        sim, meta = build_planetary_system(src)
    else:
        sim, meta = build_alpha_cen_ab(src)
    hypos = []
    if hyp_path is not None:
        hypos = add_hypotheticals(sim, meta, hyp_path)
    meta["hypotheticals"] = hypos
    return sim, meta


def configure_integrator(sim: rebound.Simulation, meta: dict):
    """Set WHFast + MEGNO with dt = P_innermost / 50."""
    sim.integrator = "whfast"
    # innermost orbit period — particles[1:] excludes the central body
    periods = []
    for p in sim.particles[1:]:
        if p.a > 0 and p.a < 1e6:
            periods.append(2 * math.pi * math.sqrt(p.a**3 / (sim.G * sim.particles[0].m)))
    p_min = min(periods) if periods else 1.0
    sim.dt = p_min / 50.0
    sim.init_megno(seed=42)
    return p_min


def run_integration(sim: rebound.Simulation, meta: dict, t_end_yr: float, n_snapshots: int):
    p_min = configure_integrator(sim, meta)
    e0 = sim.energy()
    bodies = [meta["star"]["name"]] + [p["name"] for p in meta["planets"]]
    bodies += [h["name"] for h in meta.get("hypotheticals", [])]
    primary_lookup = {h["name"]: h["parent"] for h in meta.get("hypotheticals", [])}

    times = [t_end_yr * (i + 1) / n_snapshots for i in range(n_snapshots)]
    rows = []  # (t, body, a, e)
    summary = {b: {"a_min": math.inf, "a_max": -math.inf, "e_min": math.inf, "e_max": -math.inf} for b in bodies[1:]}
    hill_track = {h["name"]: {"frac_max": 0.0, "bound": True} for h in meta.get("hypotheticals", []) if h["type"] == "moon"}

    t0 = time.time()
    for t in times:
        sim.integrate(t, exact_finish_time=0)
        for name in bodies[1:]:
            p = sim.particles[name]
            primary_name = primary_lookup.get(name, meta["star"]["name"])
            primary = sim.particles[primary_name]
            orb = p.orbit(primary=primary)
            a, e = orb.a, orb.e
            s = summary[name]
            s["a_min"] = min(s["a_min"], a)
            s["a_max"] = max(s["a_max"], a)
            s["e_min"] = min(s["e_min"], e)
            s["e_max"] = max(s["e_max"], e)
            rows.append((t, name, a, e))

            if name in hill_track:
                parent_meta = next((pp for pp in meta["planets"] if pp["name"] == primary_name), None)
                if parent_meta is not None:
                    r_hill = hill_radius(parent_meta["a_au"], parent_meta["mass_msun"], meta["star"]["mass_msun"])
                    frac = a / r_hill
                    hill_track[name]["frac_max"] = max(hill_track[name]["frac_max"], frac)
                    if a <= 0 or e >= 1.0 or frac > 1.5:
                        hill_track[name]["bound"] = False

    elapsed = time.time() - t0
    e1 = sim.energy()
    de = abs((e1 - e0) / e0) if e0 != 0 else float("nan")
    megno = sim.megno()

    return {
        "elapsed_sec": elapsed,
        "dt_yr": sim.dt,
        "innermost_period_yr": p_min,
        "energy_relative_error": de,
        "megno_final": megno,
        "per_body": summary,
        "hill_track": hill_track,
        "rows": rows,
    }


def verdict(report: dict, t_end_yr: float) -> dict:
    """Apply success criteria. Distinguishes dynamical instability from formal chaos.

    A system can be 'chaotic but Hill-stable' (TRAPPIST-1) — Lyapunov-positive but no
    bodies escape on the simulated horizon. We treat that as PASS for game-play.
    """
    judgments = {}
    dyn_unstable = False
    for body, s in report["per_body"].items():
        flags = []
        if s["e_max"] >= 0.9:
            flags.append(f"e_max={s['e_max']:.3f} ≥ 0.9 (orbit nearly unbound)")
        if s["a_min"] > 0 and s["a_max"] > 10 * s["a_min"]:
            flags.append(f"a_max/a_min = {s['a_max']/s['a_min']:.1f}× ≥ 10")
        status = "unstable" if flags else "stable"
        judgments[body] = {"flags": flags, "status": status}
        if flags:
            dyn_unstable = True

    for moon, h in report["hill_track"].items():
        b = judgments.setdefault(moon, {"flags": [], "status": "stable"})
        if not h["bound"]:
            b["flags"].append("moon unbound from parent")
            b["status"] = "unstable"
            dyn_unstable = True
        elif h["frac_max"] > 0.5:
            b["flags"].append(f"max Hill fraction = {h['frac_max']:.2f} > 0.5 (Domingos+2006 warning)")
            if b["status"] == "stable":
                b["status"] = "flagged"

    megno = report["megno_final"]
    chaos = megno > 5
    lyap_yr = 2.0 * t_end_yr / (megno - 2.0) if megno > 2.0 else float("inf")

    if dyn_unstable:
        overall = "unstable"
    elif chaos:
        overall = "chaotic_but_hill_stable"
    elif any(j["status"] == "flagged" for j in judgments.values()):
        overall = "flagged"
    else:
        overall = "stable"

    return {
        "per_body": judgments,
        "overall": overall,
        "lyapunov_time_yr": lyap_yr,
        "is_chaotic": chaos,
    }


def save_results(system: str, meta: dict, report: dict, judgment: dict, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / f"{system}_summary.json"
    ts_path = out_dir / f"{system}_timeseries.csv"

    summary_payload = {
        "system": meta["system"],
        "star": meta["star"],
        "planets": meta["planets"],
        "hypotheticals": meta["hypotheticals"],
        "integration": {
            "elapsed_sec": report["elapsed_sec"],
            "dt_yr": report["dt_yr"],
            "innermost_period_yr": report["innermost_period_yr"],
            "energy_relative_error": report["energy_relative_error"],
            "megno_final": report["megno_final"],
        },
        "per_body": report["per_body"],
        "hill_track": report["hill_track"],
        "judgment": judgment,
    }
    with summary_path.open("w") as f:
        json.dump(summary_payload, f, indent=2)

    with ts_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_yr", "body", "a_au", "e"])
        w.writerows(report["rows"])

    return summary_path, ts_path


def print_report(meta: dict, report: dict, judgment: dict):
    print(f"\n=== {meta['system']} ===")
    print(f"  star mass: {meta['star']['mass_msun']:.4f} Msun")
    print(f"  bodies: {len(meta['planets'])} planet(s), {len(meta['hypotheticals'])} hypothetical(s)")
    print(f"  dt = {report['dt_yr']*365.25:.4f} d   (P_inner = {report['innermost_period_yr']*365.25:.3f} d)")
    print(f"  elapsed: {report['elapsed_sec']:.1f} s")
    print(f"  |ΔE/E|  = {report['energy_relative_error']:.2e}")
    print(f"  MEGNO   = {report['megno_final']:.3f}  (≈2 → regular)")
    if judgment["is_chaotic"]:
        print(f"  Lyapunov ≈ {judgment['lyapunov_time_yr']:.1f} yr  (formal chaos detected)")
    print(f"  verdict: {judgment['overall'].upper()}")
    print()
    for name, s in report["per_body"].items():
        j = judgment["per_body"].get(name, {"flags": [], "status": "stable"})
        a_drift = (s["a_max"] - s["a_min"]) / s["a_min"] if s["a_min"] > 0 else float("nan")
        print(f"  {name:25s}  a∈[{s['a_min']:.5f},{s['a_max']:.5f}] AU  Δa/a={a_drift:.2e}  e∈[{s['e_min']:.4f},{s['e_max']:.4f}]  → {j['status']}")
        for fl in j["flags"]:
            print(f"      ⚠ {fl}")
    for moon, h in report["hill_track"].items():
        print(f"    moon {moon}: max_hill_frac={h['frac_max']:.3f}, bound={h['bound']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", required=True, choices=SYSTEMS.keys())
    ap.add_argument("--years", type=float, default=10_000.0)
    ap.add_argument("--snapshots", type=int, default=200)
    ap.add_argument("--hypotheticals", type=Path, default=None,
                    help="Path to a hypotheticals JSON (optional)")
    ap.add_argument("--out-dir", type=Path, default=ROOT / "results")
    args = ap.parse_args()

    sim, meta = build(args.system, args.hypotheticals)
    report = run_integration(sim, meta, args.years, args.snapshots)
    judgment = verdict(report, args.years)
    print_report(meta, report, judgment)
    paths = save_results(args.system, meta, report, judgment, args.out_dir.resolve())
    for p in paths:
        try:
            print(f"  → wrote {p.relative_to(PROJECT_ROOT)}")
        except ValueError:
            print(f"  → wrote {p}")


if __name__ == "__main__":
    main()
