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
curated JSON. EXCEPTION: narrative fields `meta_notes` and `sources_extra`
are preserved from the existing entry when omitted from YAML — this
prevents routine measurement updates from silently wiping curator notes
and supporting references. To explicitly delete a preserved field, set
it to `null` in YAML.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from schema import canonical_json

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


# 화이트리스트된 narrative 필드 — YAML 이 이 키를 명시하지 않으면 기존 값 보존.
# meta_notes 와 sources_extra 는 측정 배열과 다른 라이프사이클을 가져서
# (한 번 큐레이팅 후 거의 변경 없음), 일상적인 mass/radius YAML 갱신이
# 실수로 wipe 하는 사고를 방지. YAML 에 `meta_notes: null` 처럼 명시적 null
# 을 적으면 삭제도 가능 (`is None` 으로 구분).
_STELLAR_PRESERVE_IF_ABSENT = ("meta_notes", "sources_extra", "floor_na")


def merge(yaml_data: dict) -> tuple[dict, dict]:
    """Return (new_stellar, new_planets) — db merged with YAML overrides.

    Stellar host 처리는 whole-entry replacement 가 기본이지만,
    _STELLAR_PRESERVE_IF_ABSENT 의 narrative 필드는 YAML 에서 키 자체가
    부재할 때 기존 값을 자동 보존. 명시적 삭제는 YAML 에 `<field>: null` 로
    적어서 가능.
    Planets host 는 종전대로 list 통째로 교체.
    """
    with open(STELLAR, encoding="utf-8") as f:
        stellar = json.load(f)
    with open(PLANETS, encoding="utf-8") as f:
        planets = json.load(f)

    for host, entry in (yaml_data.get("stellar") or {}).items():
        existing = stellar.get(host) or {}
        new_entry = dict(entry)
        for key in _STELLAR_PRESERVE_IF_ABSENT:
            if key not in new_entry and key in existing:
                new_entry[key] = existing[key]
        stellar[host] = new_entry
    for host, plist in (yaml_data.get("planets") or {}).items():
        planets[host] = plist

    return stellar, planets


def _data_categories(entry: dict) -> set:
    """측정-데이터 카테고리 키 (whole-entry replacement 에서 silently 사라지면
    안 되는 것). *_measurements + compact_object. narrative 필드(meta_notes 등)는
    이미 _STELLAR_PRESERVE_IF_ABSENT 로 보존되므로 제외."""
    return {k for k in entry if k.endswith("_measurements")} | (
        {"compact_object"} if "compact_object" in entry else set())


def category_drops(yaml_data: dict) -> dict:
    """호스트별로, apply 가 (YAML 에 없어서) JSON 에서 삭제하게 될 데이터
    카테고리. stellar-wind 류 직접-JSON 큐레이션이 stale YAML 로 wipe 되는
    사고를 막는 가드. {host: [categories]} (drop 없으면 빈 dict)."""
    with open(STELLAR, encoding="utf-8") as f:
        stellar = json.load(f)
    drops = {}
    for host, entry in (yaml_data.get("stellar") or {}).items():
        existing = stellar.get(host) or {}
        lost = _data_categories(existing) - _data_categories(dict(entry))
        if lost:
            drops[host] = sorted(lost)
    return drops


def _serialize(d: dict) -> str:
    return canonical_json(d)


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
    ap.add_argument("--force", action="store_true",
                    help="Override the data-loss guard (apply even if it drops JSON-only categories)")
    args = ap.parse_args()

    data = load_yaml(args.slug)

    # ── data-loss guard ──────────────────────────────────────────────────
    # whole-entry replacement 이 YAML 에 없는 측정 카테고리를 조용히 삭제하는 것을
    # 막음. stellar-wind/inclination 처럼 JSON 직접 큐레이션된 카테고리가 stale
    # YAML 로 wipe 되는 사고 방지 (apply_phase2 의 알려진 footgun).
    drops = category_drops(data)
    if drops:
        lines = "\n".join(f"    {h}: {cats}" for h, cats in drops.items())
        msg = (f"[GUARD] {args.slug}: YAML 이 JSON 에만 있는 카테고리를 삭제하려 합니다 "
               f"(stale YAML?):\n{lines}\n"
               f"    → 이 카테고리를 YAML 에 추가하거나, 의도된 삭제면 --force 로 강행.")
        print(msg)
        if not args.check and not args.force:
            return 2                       # block the write; --check is read-only (warn only)
        if args.force:
            print("    --force: 가드 무시하고 진행.")

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
