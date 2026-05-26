# db/refs/element_plasma_colors.yaml (v2 multi-regime schema) 의 무결성을 점검하는 진단 스크립트
"""Validate db/refs/element_plasma_colors.yaml (v2 multi-regime schema).

Checks:
  - 118 entries, atomic_number covers 1..118 bijectively
  - Each entry has atomic_number, name, regimes
  - atomic_flame regime is present for every entry
  - Each regime has status; hex required iff status=visible
  - hex matches /^#[0-9a-f]{6}$/
  - hex_basis ∈ {cie_computed, canonical_descriptor, chart_approx} when hex present
  - emission_lines present iff hex_basis == cie_computed
  - Each emission_lines entry has nm (380–1000) + intensity (>0)
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
    "not_emitter",
}
VALID_HEX_BASIS = {"cie_computed", "canonical_descriptor", "chart_approx"}
VALID_REGIMES = {"atomic_flame", "reentry_plasma", "aurora", "phosphor_emission"}

HEX_RE = re.compile(r"^#[0-9a-f]{6}$")
REQUIRED_TOP = {"atomic_number", "name", "regimes"}


def validate_regime(prefix: str, regime_name: str, regime: dict, errors: list) -> None:
    if "status" not in regime:
        errors.append(f"{prefix}.{regime_name}: missing status")
        return
    status = regime["status"]
    if status not in VALID_STATUS:
        errors.append(f"{prefix}.{regime_name}: invalid status {status!r}; expected {sorted(VALID_STATUS)}")

    hex_val = regime.get("hex")
    hex_basis = regime.get("hex_basis")
    lines = regime.get("emission_lines")

    if status == "visible":
        if hex_val is None:
            errors.append(f"{prefix}.{regime_name}: status=visible but hex is null")
        elif not isinstance(hex_val, str) or not HEX_RE.match(hex_val):
            errors.append(f"{prefix}.{regime_name}: hex={hex_val!r} doesn't match #rrggbb (lowercase)")

        if hex_basis is None:
            errors.append(f"{prefix}.{regime_name}: status=visible requires hex_basis")
        elif hex_basis not in VALID_HEX_BASIS:
            errors.append(f"{prefix}.{regime_name}: invalid hex_basis {hex_basis!r}")

        # cie_computed REQUIRES emission_lines; canonical_descriptor MAY have
        # them as documentation (e.g., phosphor lines that ground the
        # canonical display color); chart_approx should NOT.
        if hex_basis == "cie_computed" and not lines:
            errors.append(f"{prefix}.{regime_name}: hex_basis=cie_computed requires emission_lines")
        if hex_basis == "chart_approx" and lines is not None:
            errors.append(
                f"{prefix}.{regime_name}: emission_lines present but hex_basis=chart_approx "
                f"(if lines exist with known intensities, basis should be cie_computed)"
            )
        if lines is not None:
            for i, ln in enumerate(lines):
                if not isinstance(ln, dict):
                    errors.append(f"{prefix}.{regime_name}.emission_lines[{i}]: not a mapping")
                    continue
                if "nm" not in ln or "intensity" not in ln:
                    errors.append(f"{prefix}.{regime_name}.emission_lines[{i}]: missing nm or intensity")
                    continue
                nm = ln["nm"]
                inten = ln["intensity"]
                if not isinstance(nm, (int, float)) or not (200 <= nm <= 2000):
                    errors.append(f"{prefix}.{regime_name}.emission_lines[{i}]: nm={nm} out of plausible range (200–2000)")
                if not isinstance(inten, (int, float)) or inten <= 0:
                    errors.append(f"{prefix}.{regime_name}.emission_lines[{i}]: intensity={inten} must be positive")
    else:
        if hex_val is not None:
            errors.append(f"{prefix}.{regime_name}: status={status} but hex={hex_val!r} (should be null)")
        if hex_basis is not None:
            errors.append(f"{prefix}.{regime_name}: status={status} but hex_basis={hex_basis!r} set")

    if not isinstance(regime.get("basis"), str) or not regime["basis"].strip():
        errors.append(f"{prefix}.{regime_name}: basis is empty or non-string")
    if not isinstance(regime.get("source"), str) or not regime["source"].strip():
        errors.append(f"{prefix}.{regime_name}: source is empty or non-string")


def main() -> int:
    with open(DB_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    errors: list[str] = []
    seen_atomic: dict[int, str] = {}

    if len(data) != 118:
        errors.append(f"entry count: expected 118, got {len(data)}")

    for sym, entry in data.items():
        prefix = f"[{sym}]"

        missing = REQUIRED_TOP - set(entry.keys())
        if missing:
            errors.append(f"{prefix} missing top-level keys: {sorted(missing)}")
            continue

        atom = entry["atomic_number"]
        if not isinstance(atom, int) or not (1 <= atom <= 118):
            errors.append(f"{prefix} atomic_number out of range: {atom}")
        elif atom in seen_atomic:
            errors.append(f"{prefix} duplicate atomic_number {atom} (already {seen_atomic[atom]})")
        else:
            seen_atomic[atom] = sym

        regimes = entry["regimes"]
        if not isinstance(regimes, dict) or not regimes:
            errors.append(f"{prefix} regimes block is empty or non-mapping")
            continue
        if "atomic_flame" not in regimes:
            errors.append(f"{prefix} missing atomic_flame regime (required for all elements)")
        unknown_regimes = set(regimes.keys()) - VALID_REGIMES
        if unknown_regimes:
            errors.append(f"{prefix} unknown regime(s): {sorted(unknown_regimes)}")

        for regime_name, regime in regimes.items():
            if regime_name not in VALID_REGIMES:
                continue
            validate_regime(prefix, regime_name, regime, errors)

    missing_atoms = set(range(1, 119)) - set(seen_atomic.keys())
    if missing_atoms:
        errors.append(f"missing atomic_number(s): {sorted(missing_atoms)}")

    # Summary stats
    atomic_visible = sum(
        1 for e in data.values()
        if e["regimes"]["atomic_flame"]["status"] == "visible"
    )
    reentry_visible = sum(
        1 for e in data.values()
        if e["regimes"].get("reentry_plasma", {}).get("status") == "visible"
    )
    aurora_visible = sum(
        1 for e in data.values()
        if e["regimes"].get("aurora", {}).get("status") == "visible"
    )

    if errors:
        print(f"[FAIL] {len(errors)} violation(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"[OK] {len(data)} entries; "
          f"atomic_flame visible: {atomic_visible}; "
          f"reentry_plasma visible: {reentry_visible}; "
          f"aurora visible: {aurora_visible}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
