#!/usr/bin/env python3
# Pecaut & Mamajek 2013 SpT→mass·radius 표로 미큐레이션 항성에 spt_estimate 측정값을 주입하는 일회용 도우미
"""Backfill spt_estimate mass and radius for stars missing measurements.

This is a one-shot helper used only to verify the principia-cfg skill end-to-end
against the full DB. It writes both:
  - `db/stellar_props_curated.json`  (canonical source, survives pipeline rebuild)
  - `db/systems/<star>.json`         (rebuilt artifact; patched here so the emit
                                      script works without re-running build_systems.py)

If you re-run `scripts/pipeline/build_systems.py`, the system-file patches are
regenerated from the curated file — the duplication is intentional.

NOT part of the principia-cfg skill's runtime; lives in scripts/ purely as a
reproducible backfill helper. Marked `method: "spt_estimate"` so downstream
consumers can distinguish from real catalog measurements.

Source: Pecaut & Mamajek 2013, ApJS 208, 9 (Table 5 main-sequence dwarfs).
        Subgiant (IV) values are rough literature averages, not from PM13.
        White-dwarf default 0.6 M☉ is the WD mass distribution peak.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DB_DIR = REPO_ROOT / "db"
SYSTEMS_DIR = DB_DIR / "systems"
CURATED_PATH = DB_DIR / "stellar_props_curated.json"

GM_SUN = 1.32712440018e11       # km³/s²
R_SUN_KM = 695700.0             # km

# Pecaut & Mamajek 2013, main-sequence dwarfs (M☉, R☉) keyed by (class, subclass).
PM13_V = {
    ("O", 3): (120.0, 13.4),
    ("B", 0): (17.0, 7.4),
    ("B", 5): (4.0, 3.6),
    ("A", 0): (2.18, 2.36),
    ("A", 5): (1.92, 1.79),
    ("F", 0): (1.59, 1.42),
    ("F", 5): (1.33, 1.27),
    ("F", 8): (1.16, 1.16),
    ("G", 0): (1.06, 1.10),
    ("G", 2): (1.02, 1.012),
    ("G", 5): (0.96, 0.96),
    ("G", 8): (0.92, 0.91),
    ("K", 0): (0.88, 0.79),
    ("K", 2): (0.78, 0.72),
    ("K", 5): (0.71, 0.67),
    ("K", 7): (0.68, 0.63),
    ("M", 0): (0.59, 0.566),
    ("M", 2): (0.44, 0.434),
    ("M", 3): (0.36, 0.374),
    ("M", 4): (0.23, 0.323),
    ("M", 5): (0.16, 0.288),
    ("M", 6): (0.11, 0.243),
    ("M", 7): (0.09, 0.205),
    ("M", 8): (0.08, 0.165),
}

# Subgiant approximations (literature averages, not PM13)
PM13_IV = {
    ("G", 5): (1.20, 2.00),
    ("G", 8): (1.05, 2.20),
    ("K", 0): (1.10, 2.50),
}

WD_DEFAULT_MSUN = 0.60
WD_DEFAULT_RSUN = 0.013

SPT_RE = re.compile(r"^([OBAFGKM])(\d+(?:\.\d+)?)\s*([IV]+)?")
WD_RE = re.compile(r"^D[ABCOZQ]?\d")


def parse_spt(spt: str) -> tuple[str, float, str] | None:
    if not spt:
        return None
    spt = spt.strip()
    if WD_RE.match(spt):
        return ("WD", 0.0, "WD")
    m = SPT_RE.match(spt)
    if not m:
        return None
    cls = m.group(1)
    sub = float(m.group(2))
    lum = m.group(3) or "V"
    return cls, sub, lum


def interpolate(table: dict, cls: str, sub: float) -> tuple[float, float] | None:
    same = sorted(((s, mr) for (c, s), mr in table.items() if c == cls), key=lambda t: t[0])
    if not same:
        return None
    if sub <= same[0][0]:
        return same[0][1]
    if sub >= same[-1][0]:
        return same[-1][1]
    for i in range(len(same) - 1):
        s1, mr1 = same[i]
        s2, mr2 = same[i + 1]
        if s1 <= sub <= s2:
            frac = (sub - s1) / (s2 - s1)
            return (mr1[0] + frac * (mr2[0] - mr1[0]),
                    mr1[1] + frac * (mr2[1] - mr1[1]))
    return None


def estimate_from_spt(spt: str) -> tuple[float, float] | None:
    parsed = parse_spt(spt)
    if parsed is None:
        return None
    cls, sub, lum = parsed
    if cls == "WD":
        return (WD_DEFAULT_MSUN, WD_DEFAULT_RSUN)
    table = PM13_IV if lum == "IV" else PM13_V
    result = interpolate(table, cls, sub)
    if result is None and table is PM13_IV:
        result = interpolate(PM13_V, cls, sub)
    return result


def make_measurement(value: float, kind: str, spt: str) -> dict:
    field = "value_msun" if kind == "mass" else "value_rsun"
    return {
        field: round(value, 4),
        "uncertainty_" + ("msun" if kind == "mass" else "rsun"): None,
        "method": "unverified",
        "reference": f"spt_estimate: Pecaut & Mamajek 2013 ({spt} interpolation)",
        "bibcode": "2013ApJS..208....9P",
        "doi": "10.1088/0067-0049/208/1/9",
        "recommended": True,
    }


def has_spt_estimate(measurements: list, kind: str) -> bool:
    return any(str(m.get("reference", "")).startswith("spt_estimate:") for m in measurements)


def patch_star(star: dict, name: str) -> list[str]:
    """Mutate the star dict in place. Return list of changes applied."""
    raw = star.setdefault("raw", {})
    spt = raw.get("spectype")
    if not spt:
        return [f"{name}: no spectype, skipped"]

    est = estimate_from_spt(spt)
    if est is None:
        return [f"{name}: cannot parse spectype {spt!r}, skipped"]

    mass_msun, radius_rsun = est
    changes: list[str] = []

    mass_meas = raw.setdefault("mass_measurements", [])
    if not mass_meas or not any(m.get("recommended") for m in mass_meas):
        if not has_spt_estimate(mass_meas, "mass"):
            mass_meas.append(make_measurement(mass_msun, "mass", spt))
            changes.append(f"{name}: +mass {mass_msun:.4f} M☉ from {spt}")

    radius_meas = raw.setdefault("radius_measurements", [])
    if not radius_meas or not any(r.get("recommended") for r in radius_meas):
        if not has_spt_estimate(radius_meas, "radius"):
            radius_meas.append(make_measurement(radius_rsun, "radius", spt))
            changes.append(f"{name}: +radius {radius_rsun:.4f} R☉ from {spt}")

    # Recompute principia block to reflect the new measurements.
    principia = star.setdefault("principia", {})
    rec_mass = next((m.get("value_msun") for m in mass_meas if m.get("recommended")), None)
    rec_radius = next((r.get("value_rsun") for r in radius_meas if r.get("recommended")), None)
    if rec_mass is not None:
        principia["gravitational_parameter_km3_s2"] = round(rec_mass * GM_SUN, 3)
    if rec_radius is not None:
        principia["mean_radius_km"] = round(rec_radius * R_SUN_KM, 1)

    return changes


def patch_curated(curated: dict, star_name: str, spt: str) -> list[str]:
    """Add spt_estimate mass/radius to db/stellar_props_curated.json so the canonical
    source persists across pipeline rebuilds. Idempotent."""
    est = estimate_from_spt(spt)
    if est is None:
        return []
    mass_msun, radius_rsun = est
    entry = curated.setdefault(star_name, {})
    changes: list[str] = []

    mass_meas = entry.setdefault("mass_measurements", [])
    if not has_spt_estimate(mass_meas, "mass"):
        mass_meas.append(make_measurement(mass_msun, "mass", spt))
        changes.append(f"curated[{star_name}]: +mass")

    radius_meas = entry.setdefault("radius_measurements", [])
    if not has_spt_estimate(radius_meas, "radius"):
        radius_meas.append(make_measurement(radius_rsun, "radius", spt))
        changes.append(f"curated[{star_name}]: +radius")

    return changes


def main() -> int:
    curated = json.loads(CURATED_PATH.read_text(encoding="utf-8")) if CURATED_PATH.exists() else {}
    all_changes: list[str] = []

    for sys_path in sorted(SYSTEMS_DIR.glob("*.json")):
        data = json.loads(sys_path.read_text(encoding="utf-8"))
        file_changed = False
        for star in data.get("stars") or []:
            star_name = star.get("name", "?")
            gm = (star.get("principia") or {}).get("gravitational_parameter_km3_s2")
            if gm is not None:
                continue
            changes = patch_star(star, star_name)
            spt = (star.get("raw") or {}).get("spectype")
            if spt:
                all_changes.extend(patch_curated(curated, star_name, spt))
            if changes:
                all_changes.extend(changes)
                file_changed = True
        if file_changed:
            sys_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    CURATED_PATH.write_text(
        json.dumps(curated, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if not all_changes:
        print("no changes")
        return 0

    for c in all_changes:
        print(c)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
