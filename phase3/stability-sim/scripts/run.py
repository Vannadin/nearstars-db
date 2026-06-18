#!/usr/bin/env python3
# 안정성 시뮬레이션 메인 엔트리. WHFast + MEGNO 로 N-body 적분 후 보고서 생성.
from __future__ import annotations

import argparse
import csv
import json
import math
import os
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
    build_solar_system,
    add_hypotheticals,
    hill_radius,
    KM_PER_AU,
)

SYSTEMS = {
    "trappist_1": ("planetary", PROJECT_ROOT / "db/systems/trappist_1.json"),
    "proxima_cen": ("planetary", PROJECT_ROOT / "db/systems/proxima_cen.json"),
    "alpha_centauri": ("binary", PROJECT_ROOT / "db/systems"),
    # Single-star multi-planet Phase 3 systems (generic planetary loader).
    "55_cnc": ("planetary", PROJECT_ROOT / "db/systems/55_cnc.json"),
    "61_vir": ("planetary", PROJECT_ROOT / "db/systems/61_vir.json"),
    "au_mic": ("planetary", PROJECT_ROOT / "db/systems/au_mic.json"),
    "barnards_star": ("planetary", PROJECT_ROOT / "db/systems/barnards_star.json"),
    "hd_219134": ("planetary", PROJECT_ROOT / "db/systems/hd_219134.json"),
    "hd_69830": ("planetary", PROJECT_ROOT / "db/systems/hd_69830.json"),
    "tau_cet": ("planetary", PROJECT_ROOT / "db/systems/tau_cet.json"),
    "teegardens_star": ("planetary", PROJECT_ROOT / "db/systems/teegardens_star.json"),
    "yz_cet": ("planetary", PROJECT_ROOT / "db/systems/yz_cet.json"),
    "solar_system": ("solar", None),   # Sun + 8 planets (J2000), real-mass benchmark
}


def build(system: str, hyp_path: Path | None, acen_incl=50.0, acen_a=None, acen_e=None):
    kind, src = SYSTEMS[system]
    if kind == "planetary":
        sim, meta = build_planetary_system(src)
    elif kind == "solar":
        sim, meta = build_solar_system()
    else:
        sim, meta = build_alpha_cen_ab(src, mutual_incl_deg=acen_incl,
                                       a_override=acen_a, e_override=acen_e)
    hypos = []
    if hyp_path is not None:
        hypos = add_hypotheticals(sim, meta, hyp_path)
    meta["hypotheticals"] = hypos
    return sim, meta


def configure_integrator(sim: rebound.Simulation, meta: dict, integrator: str = "whfast"):
    """Set the integrator with dt = P_innermost / 50.

    MEGNO needs variational equations (WHFast / IAS15). TRACE does not support
    them, so it is skipped there and the verdict falls back to a/e-drift bounds
    + energy error — which is exactly what's wanted for close-encounter /
    high-e cases TRACE is chosen for.
    """
    sim.integrator = integrator
    # innermost orbit period — computed relative to each body's TRUE primary.
    # The default Jacobi `p.a` is wrong for the alpha Cen planet: with the
    # near-equal companion B at index 1, Jacobi makes the planet's primary the
    # A+B barycenter, returning ~3.75 AU instead of the A-relative 1.6 AU — so
    # dt came out 3.59x too large and corrupted the fixed-step (WHFast/TRACE)
    # high-e runs. Planets and companion B orbit star A; moons orbit their parent.
    star = sim.particles[0]
    periods = []
    for pm in meta["planets"]:
        orb = sim.particles[pm["name"]].orbit(primary=star)
        if 0 < orb.a < 1e6:
            periods.append(2 * math.pi * math.sqrt(orb.a**3 / (sim.G * star.m)))
    for h in meta.get("hypotheticals", []):
        primary = sim.particles[h["parent"]]
        orb = sim.particles[h["name"]].orbit(primary=primary)
        if 0 < orb.a < 1e6:
            periods.append(2 * math.pi * math.sqrt(orb.a**3 / (sim.G * primary.m)))
    p_min = min(periods) if periods else 1.0
    # dt = P_inner/50 by default; STAB_DT_DIV finer-steps a packed config to test
    # whether an ejection is real or a fixed-step resolution artifact (e.g. AU Mic).
    sim.dt = p_min / (50.0 * float(os.environ.get("STAB_DT_DIV", "1")))
    megno_enabled = integrator != "trace"
    if megno_enabled:
        sim.init_megno(seed=42)
    meta["megno_enabled"] = megno_enabled
    meta["integrator"] = integrator
    return p_min


def run_integration(sim: rebound.Simulation, meta: dict, t_end_yr: float, n_snapshots: int,
                    integrator: str = "whfast"):
    p_min = configure_integrator(sim, meta, integrator)
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
            # instantaneous orbital elements — let the viewer draw a smooth
            # analytic ellipse at each epoch that precesses/tilts/pumps over time
            # (positions alone under-sample and render as a polygon).
            inc = math.degrees(orb.inc); Om = math.degrees(orb.Omega)
            om = math.degrees(orb.omega); f = math.degrees(orb.f)
            s = summary[name]
            s["a_min"] = min(s["a_min"], a)
            s["a_max"] = max(s["a_max"], a)
            s["e_min"] = min(s["e_min"], e)
            s["e_max"] = max(s["e_max"], e)
            rows.append((t, name, a, e, round(inc, 5), round(Om, 5), round(om, 5), round(f, 5)))

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
    megno = sim.megno() if meta.get("megno_enabled", True) else None

    return {
        "elapsed_sec": elapsed,
        "integrator": meta.get("integrator", "whfast"),
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
        # Eccentricity tier — a separate axis from dynamical survival. "stable"
        # only means e stayed below the 0.9 near-unbound threshold; it does NOT
        # mean the orbit is calm. calm < 0.3, hot 0.3-0.9, extreme >= 0.9.
        ec = "extreme" if s["e_max"] >= 0.9 else ("hot" if s["e_max"] >= 0.3 else "calm")
        judgments[body] = {"flags": flags, "status": status,
                           "ecc_class": ec, "e_max": s["e_max"]}
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
    chaos = (megno is not None) and (megno > 5)
    lyap_yr = 2.0 * t_end_yr / (megno - 2.0) if (megno is not None and megno > 2.0) else float("inf")

    if dyn_unstable:
        overall = "unstable"
    elif chaos:
        overall = "chaotic_but_hill_stable"
    elif any(j["status"] == "flagged" for j in judgments.values()):
        overall = "flagged"
    else:
        overall = "stable"

    rank = {"calm": 0, "hot": 1, "extreme": 2}
    ecc_class_max = max((j.get("ecc_class", "calm") for j in judgments.values()),
                        key=lambda c: rank.get(c, 0), default="calm")

    return {
        "per_body": judgments,
        "overall": overall,
        "ecc_class_max": ecc_class_max,
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
            "integrator": report.get("integrator", "whfast"),
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
        w.writerow(["t_yr", "body", "a_au", "e", "inc_deg", "Omega_deg", "omega_deg", "f_deg"])
        w.writerows(report["rows"])

    return summary_path, ts_path


def print_report(meta: dict, report: dict, judgment: dict):
    print(f"\n=== {meta['system']} ===")
    print(f"  star mass: {meta['star']['mass_msun']:.4f} Msun")
    print(f"  bodies: {len(meta['planets'])} planet(s), {len(meta['hypotheticals'])} hypothetical(s)")
    print(f"  dt = {report['dt_yr']*365.25:.4f} d   (P_inner = {report['innermost_period_yr']*365.25:.3f} d)")
    print(f"  elapsed: {report['elapsed_sec']:.1f} s")
    print(f"  |ΔE/E|  = {report['energy_relative_error']:.2e}")
    if report["megno_final"] is not None:
        print(f"  MEGNO   = {report['megno_final']:.3f}  (≈2 → regular)")
    else:
        print(f"  MEGNO   = n/a  ({report.get('integrator','?')}: no variational eqs → a/e-drift verdict)")
    if judgment["is_chaotic"]:
        print(f"  Lyapunov ≈ {judgment['lyapunov_time_yr']:.1f} yr  (formal chaos detected)")
    print(f"  verdict: {judgment['overall'].upper()}   (hottest eccentricity: {judgment.get('ecc_class_max', '?')})")
    print()
    for name, s in report["per_body"].items():
        j = judgment["per_body"].get(name, {"flags": [], "status": "stable"})
        a_drift = (s["a_max"] - s["a_min"]) / s["a_min"] if s["a_min"] > 0 else float("nan")
        print(f"  {name:25s}  a∈[{s['a_min']:.5f},{s['a_max']:.5f}] AU  Δa/a={a_drift:.2e}  e∈[{s['e_min']:.4f},{s['e_max']:.4f}]  → {j['status']} [{j.get('ecc_class', '?')}]")
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
    ap.add_argument("--integrator", choices=["whfast", "trace", "ias15"], default="whfast",
                    help="whfast (default, fast symplectic + MEGNO); trace "
                         "(accurate through close encounters / high-e, no MEGNO); "
                         "ias15 (adaptive high-order gold standard + MEGNO, slow)")
    ap.add_argument("--acen-incl-deg", type=float, default=50.0,
                    help="alpha_centauri only: A b mutual inclination to the AB plane "
                         "(deg). 50 = Beichman prograde; ~120 = retrograde. For the "
                         "Kozai inclination sweep.")
    ap.add_argument("--acen-a-au", type=float, default=None,
                    help="alpha_centauri only: override A b semi-major axis (AU); "
                         "default = DB value (1.6). Use 2.1 for the a>2 family.")
    ap.add_argument("--acen-e", type=float, default=None,
                    help="alpha_centauri only: override A b eccentricity; default = DB (0.4)")
    ap.add_argument("--mass-incl-deg", type=float, default=None,
                    help="planetary systems only: scale every planet mass by 1/sin(i) "
                         "(RV minimum mass M·sin i → true mass at coplanar inclination i). "
                         "60 = isotropic-prior median (×1.155). Output is written to "
                         "{system}_i{deg}_* so the canonical edge-on summary is preserved.")
    args = ap.parse_args()

    sim, meta = build(args.system, args.hypotheticals,
                      acen_incl=args.acen_incl_deg, acen_a=args.acen_a_au, acen_e=args.acen_e)

    out_label = args.system
    if args.mass_incl_deg is not None:
        if SYSTEMS[args.system][0] != "planetary":
            ap.error("--mass-incl-deg applies only to planetary (single-star RV) systems")
        factor = 1.0 / math.sin(math.radians(args.mass_incl_deg))
        for pm in meta["planets"]:
            sim.particles[pm["name"]].m *= factor
            pm["mass_msun"] *= factor
            pm["mass_kind"] = f"true (i={args.mass_incl_deg:g}°, ×{factor:.3f})"
        meta["system"] += f" (true mass @ i={args.mass_incl_deg:g}°)"
        out_label = f"{args.system}_i{int(round(args.mass_incl_deg))}"

    report = run_integration(sim, meta, args.years, args.snapshots, args.integrator)
    judgment = verdict(report, args.years)
    print_report(meta, report, judgment)
    paths = save_results(out_label, meta, report, judgment, args.out_dir.resolve())
    for p in paths:
        try:
            print(f"  → wrote {p.relative_to(PROJECT_ROOT)}")
        except ValueError:
            print(f"  → wrote {p}")


if __name__ == "__main__":
    main()
