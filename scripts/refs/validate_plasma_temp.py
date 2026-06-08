# plasma_temperature_colors.yaml 의 구조·값범위·hex형식·빌드 재현성을 검증
"""Validate db/refs/plasma_temperature_colors.yaml.

Checks: the _blackbody + composition grids are complete over their temperature
ranges; every hex is 6-digit lowercase; every rgb is 3 ints in 0-255; the
physics fractions are in [0,1]; `dominant` is one of the known regimes; and the
file is reproducible (re-running the builder yields the same bytes).

Exit non-zero on any failure (suitable for check.sh).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_plasma_temperature_colors as B  # noqa: E402
import build_molecular_temperature_colors as M  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
YAML = ROOT / "db" / "refs" / "plasma_temperature_colors.yaml"
ELEM_YAML = ROOT / "db" / "refs" / "element_temperature_colors.yaml"
MOL_YAML = ROOT / "db" / "refs" / "molecular_temperature_colors.yaml"
HEX = re.compile(r"^#[0-9a-f]{6}$")
DOMINANT = {"thermal incandescence", "molecular bands", "ionic lines", "atomic lines"}
MOL_DOMINANT = {"thermal", "molecular bands", "ionic", "atomic lines"}


def _hex_ok(h) -> bool:
    return isinstance(h, str) and bool(HEX.match(h))


def _rgb_ok(rgb) -> bool:
    return (isinstance(rgb, list) and len(rgb) == 3
            and all(isinstance(c, int) and 0 <= c <= 255 for c in rgb))


def validate() -> list[str]:
    errs: list[str] = []
    data = yaml.safe_load(YAML.read_text(encoding="utf-8"))

    bb = data.get("_blackbody", {})
    for T in B.BB_TEMPS:
        cell = bb.get(T)
        if not cell:
            errs.append(f"_blackbody missing {T}K")
            continue
        if not _hex_ok(cell.get("hex")):
            errs.append(f"_blackbody {T}K bad hex {cell.get('hex')!r}")
        if not _rgb_ok(cell.get("rgb")):
            errs.append(f"_blackbody {T}K bad rgb")

    for key in B.LABELS:
        comp = data.get(key)
        if not comp:
            errs.append(f"composition {key} missing")
            continue
        if not comp.get("label_en") or not comp.get("label_ko"):
            errs.append(f"{key} missing label")
        colors = comp.get("colors", {})
        for T in B.COMP_TEMPS:
            c = colors.get(T)
            if not c:
                errs.append(f"{key} missing {T}K")
                continue
            if not _hex_ok(c.get("combined_hex")):
                errs.append(f"{key} {T}K bad hex {c.get('combined_hex')!r}")
            if not _rgb_ok(c.get("rgb")):
                errs.append(f"{key} {T}K bad rgb")
            for f in ("ionization_fraction", "molecular_fraction", "emission_fraction"):
                v = c.get(f)
                if not isinstance(v, (int, float)) or not (0.0 <= v <= 1.0):
                    errs.append(f"{key} {T}K {f}={v} out of [0,1]")
            if c.get("dominant") not in DOMINANT:
                errs.append(f"{key} {T}K bad dominant {c.get('dominant')!r}")

    # reproducibility: rebuilding yields identical bytes
    rebuilt = B.HEADER + yaml.dump(B.build(), Dumper=B.NoAliasDumper,
                                   sort_keys=False, allow_unicode=True,
                                   default_flow_style=False)
    if rebuilt != YAML.read_text(encoding="utf-8"):
        errs.append("not reproducible — rebuild differs (run build_plasma_temperature_colors.py)")
    return errs


def validate_elements() -> list[str]:
    """Structural check of element_temperature_colors.yaml (no rebuild — its build
    needs the NIST line cache, so reproducibility isn't enforced in check.sh)."""
    errs: list[str] = []
    if not ELEM_YAML.exists():
        return ["element_temperature_colors.yaml missing"]
    data = yaml.safe_load(ELEM_YAML.read_text(encoding="utf-8"))
    elems = data.get("elements", {})
    if not elems:
        return ["element_temperature_colors.yaml: no elements"]
    for sym, e in elems.items():
        colors = e.get("colors", {})
        if not colors:
            errs.append(f"{sym}: no colors"); continue
        for T, c in colors.items():
            if not _hex_ok(c.get("hex")):
                errs.append(f"{sym} {T}K bad hex {c.get('hex')!r}")
            if not _rgb_ok(c.get("rgb")):
                errs.append(f"{sym} {T}K bad rgb")
            v = c.get("ionization_fraction")
            if not isinstance(v, (int, float)) or not (0.0 <= v <= 1.0):
                errs.append(f"{sym} {T}K ionization_fraction={v} out of [0,1]")
    return errs


def validate_molecules() -> list[str]:
    """Structure + reproducibility of molecular_temperature_colors.yaml. Its build
    reads only local YAML (no NIST fetch), so reproducibility IS enforced."""
    errs: list[str] = []
    if not MOL_YAML.exists():
        return ["molecular_temperature_colors.yaml missing"]
    data = yaml.safe_load(MOL_YAML.read_text(encoding="utf-8"))
    mols = data.get("molecules", {})
    if not mols:
        return ["molecular_temperature_colors.yaml: no molecules"]
    for formula, e in mols.items():
        colors = e.get("colors", {})
        if not colors:
            # legitimate only when no engine-supported atoms
            if not e.get("note"):
                errs.append(f"{formula}: no colors and no note")
            continue
        for T, c in colors.items():
            if not _hex_ok(c.get("hex")):
                errs.append(f"{formula} {T}K bad hex {c.get('hex')!r}")
            if not _rgb_ok(c.get("rgb")):
                errs.append(f"{formula} {T}K bad rgb")
            for f in ("ionization_fraction", "molecular_fraction"):
                v = c.get(f)
                if not isinstance(v, (int, float)) or not (0.0 <= v <= 1.0):
                    errs.append(f"{formula} {T}K {f}={v} out of [0,1]")
            if c.get("dominant") not in MOL_DOMINANT:
                errs.append(f"{formula} {T}K bad dominant {c.get('dominant')!r}")
    if M.render(M.build()) != MOL_YAML.read_text(encoding="utf-8"):
        errs.append("not reproducible — rebuild differs "
                    "(run build_molecular_temperature_colors.py)")
    return errs


def main() -> int:
    errs = validate() + validate_elements() + validate_molecules()
    if errs:
        print(f"[FAIL] plasma color tables — {len(errs)} issue(s):")
        for e in errs[:20]:
            print(f"  - {e}")
        return 1
    print("[PASS] plasma_temperature_colors.yaml (reproducible) + "
          "element_temperature_colors.yaml (structure) + "
          "molecular_temperature_colors.yaml (reproducible) OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
