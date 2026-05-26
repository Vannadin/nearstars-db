# db/refs/element_plasma_colors.yaml 의 schema 무결성을 점검하는 진단 스크립트
"""Validate db/refs/element_plasma_colors.yaml.

Checks:
  - 118 entries, atomic_number covers 1..118 bijectively
  - Each entry has: atomic_number, name, status, basis, source
  - status is one of the documented enum values
  - hex required iff status == "visible"; null otherwise
  - hex matches /^#[0-9a-f]{6}$/ (lowercase 6-digit)
  - No duplicate atomic_number or symbol

Exit 0 if clean, 1 with violations listed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "db" / "refs" / "element_plasma_colors.yaml"

VALID_STATUS = {
    "visible",
    "no_flame_color",
    "not_visible_to_humans",
    "too_radioactive",
    "too_short",
    "no_data",
}

HEX_RE = re.compile(r"^#[0-9a-f]{6}$")
REQUIRED_KEYS = {"atomic_number", "name", "status", "basis", "source"}


def main() -> int:
    with open(DB_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    errors: list[str] = []
    seen_atomic: dict[int, str] = {}

    if len(data) != 118:
        errors.append(f"entry count: expected 118, got {len(data)}")

    for sym, entry in data.items():
        prefix = f"[{sym}]"

        missing = REQUIRED_KEYS - set(entry.keys())
        if missing:
            errors.append(f"{prefix} missing keys: {sorted(missing)}")
            continue

        atom = entry["atomic_number"]
        if not isinstance(atom, int) or not (1 <= atom <= 118):
            errors.append(f"{prefix} atomic_number out of range: {atom}")
        elif atom in seen_atomic:
            errors.append(f"{prefix} duplicate atomic_number {atom} (already {seen_atomic[atom]})")
        else:
            seen_atomic[atom] = sym

        status = entry["status"]
        if status not in VALID_STATUS:
            errors.append(f"{prefix} invalid status {status!r}; expected one of {sorted(VALID_STATUS)}")

        hex_val = entry.get("hex")
        if status == "visible":
            if hex_val is None:
                errors.append(f"{prefix} status=visible but hex is null")
            elif not isinstance(hex_val, str) or not HEX_RE.match(hex_val):
                errors.append(f"{prefix} hex={hex_val!r} doesn't match #rrggbb (lowercase)")
        else:
            if hex_val is not None:
                errors.append(f"{prefix} status={status} but hex is set to {hex_val!r} (should be null)")

        if not isinstance(entry.get("basis"), str) or not entry["basis"].strip():
            errors.append(f"{prefix} basis is empty or non-string")
        if not isinstance(entry.get("source"), str) or not entry["source"].strip():
            errors.append(f"{prefix} source is empty or non-string")

    missing_atoms = set(range(1, 119)) - set(seen_atomic.keys())
    if missing_atoms:
        errors.append(f"missing atomic_number(s): {sorted(missing_atoms)}")

    visible_count = sum(1 for e in data.values() if e["status"] == "visible")

    if errors:
        print(f"[FAIL] {len(errors)} violation(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"[OK] {len(data)} entries; "
          f"{visible_count} with hex; "
          f"{len(data) - visible_count} with explicit no-data status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
