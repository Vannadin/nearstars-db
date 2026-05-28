# Phase 2 측정값 YAML 을 db/stellar_props_curated.json + db/planets_curated.json 에 적용하는 제네릭 스크립트
"""Apply a system's Phase 2 measurements from declarative YAML into the curated DB files.

Replaces the per-system `phase2/<system>/apply_phase2.py` pattern. Each
system now ships a single `phase2/<system>/measurements.yaml` whose shape
is isomorphic to the subset of `db/stellar_props_curated.json` +
`db/planets_curated.json` that Phase 2 writes.

Usage:
    python3 scripts/pipeline/apply_phase2.py <system_slug>
    python3 scripts/pipeline/apply_phase2.py <system_slug> --check

`<system_slug>` matches the directory name under `phase2/`, e.g.
`alpha_centauri_proxima` or `trappist_1`.

YAML shape (top-level keys, all optional but at least one required):

    stellar:
      "<Host Name>":
        teff_k: <float>           # optional top-level
        spectype: "<str>"         # optional top-level
        mass_measurements: [ {...}, ... ]
        radius_measurements: [ ... ]
        teff_measurements: [ ... ]
        luminosity_measurements: [ ... ]
        age_measurements: [ ... ]
        metallicity_measurements: [ ... ]
        rotation_measurements: [ ... ]
        activity_measurements: [ ... ]
    planets:
      "<Host Name>":
        - pl_name: "<Planet Name>"
          orbital: {...} | [ {...}, ... ]    # Phase 1 dict OR Phase 2 array
          physical: {...} | [ {...}, ... ]

Merge semantics: each `<Host Name>` REPLACES the host's full entry in the
curated JSON. No per-field partial merge. To preserve existing fields,
include them in YAML.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
STELLAR = ROOT / "db" / "stellar_props_curated.json"
PLANETS = ROOT / "db" / "planets_curated.json"


def load_yaml(slug: str) -> dict:
    path = ROOT / "phase2" / slug / "measurements.yaml"
    if not path.exists():
        sys.exit(f"[FAIL] {path.relative_to(ROOT)} not found")
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        sys.exit(f"[FAIL] {path}: top-level must be a mapping")
    unknown = set(data.keys()) - {"stellar", "planets"}
    if unknown:
        sys.exit(f"[FAIL] {path}: unknown top-level keys {sorted(unknown)}")
    return data


def merge(yaml_data: dict) -> tuple[dict, dict]:
    """Return (new_stellar, new_planets) — db merged with YAML overrides."""
    with open(STELLAR, encoding="utf-8") as f:
        stellar = json.load(f)
    with open(PLANETS, encoding="utf-8") as f:
        planets = json.load(f)

    for host, entry in (yaml_data.get("stellar") or {}).items():
        stellar[host] = entry
    for host, plist in (yaml_data.get("planets") or {}).items():
        planets[host] = plist

    return stellar, planets


def _serialize(d: dict) -> str:
    return json.dumps(d, indent=2, ensure_ascii=False)


def write_if_changed(path: Path, new: dict) -> bool:
    new_text = _serialize(new)
    if path.read_text(encoding="utf-8") == new_text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("slug", help="phase2/<slug>/measurements.yaml")
    ap.add_argument("--check", action="store_true",
                    help="Compute merged result but don't write; exit 1 if it would change anything")
    args = ap.parse_args()

    data = load_yaml(args.slug)
    new_stellar, new_planets = merge(data)

    stellar_changed = _serialize(new_stellar) != STELLAR.read_text(encoding="utf-8")
    planets_changed = _serialize(new_planets) != PLANETS.read_text(encoding="utf-8")

    if args.check:
        if stellar_changed or planets_changed:
            print(f"[DIFF] {args.slug} would change: "
                  f"stellar={'Y' if stellar_changed else 'N'} "
                  f"planets={'Y' if planets_changed else 'N'}")
            return 1
        print(f"[CLEAN] {args.slug} matches current db state")
        return 0

    s_wrote = write_if_changed(STELLAR, new_stellar)
    p_wrote = write_if_changed(PLANETS, new_planets)
    print(f"applied {args.slug}: "
          f"stellar={'wrote' if s_wrote else 'unchanged'}, "
          f"planets={'wrote' if p_wrote else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
