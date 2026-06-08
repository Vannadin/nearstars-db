# 임의 대기 조성(분자 몰분율) → 온도별 플라스마 발광색을 엔진으로 산출하는 CLI
"""Compute the LTE plasma color vs temperature for an ARBITRARY atmosphere
composition — the spectrum-level mixer.

Give it a molecular composition (mole/volume fractions); it converts to atomic
fractions, auto-selects the molecular band systems whose atoms are all present,
runs the saha_boltzmann engine (Saha + Boltzmann + dissociation, mixed at the
SPECTRUM level, then CIE), and prints the color vs temperature. This is the
correct way to get a mixed-atmosphere color — you mix spectra, never colors.

Supported emitting elements: H, He, C, N, O (the engine's atomic DB). Other
elements (Ar, S, ...) are reported and dropped (no atomic data); the rest is
renormalized. Atomic-only + LTE — same model + caveats as the per-composition
table (see plasma-color-methodology-review.md).

Usage:
    python3 scripts/refs/emit_atmosphere_color.py "CO2:0.95,N2:0.05"
    python3 scripts/refs/emit_atmosphere_color.py "H2:0.86,He:0.14" --html
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cie_color                       # noqa: E402
import saha_boltzmann as sb            # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TEMPS = list(range(1000, 15001, 1000))
SUPPORTED = set(sb.ELEMENTS)           # H, He, C, N, O
_FORMULA = re.compile(r"([A-Z][a-z]?)(\d*)")


def parse_formula(f: str) -> dict:
    """'CO2' -> {'C':1,'O':2}."""
    out: dict = {}
    for el, n in _FORMULA.findall(f):
        if not el:
            continue
        out[el] = out.get(el, 0) + (int(n) if n else 1)
    return out


def composition_to_atoms(spec: str):
    """'CO2:0.95,N2:0.05' -> (atomic_fraction_dict, dropped_elements, molecules)."""
    molecules = {}
    for part in spec.split(","):
        name, _, frac = part.partition(":")
        molecules[name.strip()] = float(frac)
    atoms: dict = {}
    for formula, mf in molecules.items():
        for el, cnt in parse_formula(formula).items():
            atoms[el] = atoms.get(el, 0.0) + mf * cnt
    dropped = {el: v for el, v in atoms.items() if el not in SUPPORTED}
    kept = {el: v for el, v in atoms.items() if el in SUPPORTED}
    tot = sum(kept.values()) or 1.0
    return {el: v / tot for el, v in kept.items()}, dropped, molecules


def select_bands(elems: dict, mol_db: dict) -> list:
    """Active band systems = those whose constituent atoms are all present."""
    present = set(elems)
    out = []
    for name, bs in mol_db["band_systems"].items():
        mol = mol_db["molecules"][bs["molecule"]]
        if set(mol["forms_from"]) <= present:
            out.append(name)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("composition", help='e.g. "CO2:0.95,N2:0.05"')
    ap.add_argument("--t-elec", type=float, default=None, dest="t_elec",
                    help="electron temp [K] for 2-temperature non-LTE (lights N2-family blue); "
                         "default = LTE. For velocity-driven reentry use reentry_color.py")
    ap.add_argument("--html", action="store_true", help="write /tmp/atmosphere_color.html + open")
    args = ap.parse_args()

    atomic, mol_db = sb.load_dbs()
    elems, dropped, molecules = composition_to_atoms(args.composition)
    if not elems:
        print("No supported emitting elements (H/He/C/N/O) in composition.", file=sys.stderr)
        return 1
    bands = select_bands(elems, mol_db)

    print(f"input molecules: {molecules}")
    if dropped:
        print(f"dropped (no atomic data, renormalized): {dropped}")
    print(f"atomic fractions (emitting): " + ", ".join(f"{e}={f:.3f}" for e, f in sorted(elems.items())))
    print(f"active band systems: {bands or '(none — atomic only)'}")
    print()
    print("    T        color    dominant")
    cells = []
    for T in TEMPS:
        inten, diag = sb.slab_spectrum_custom(elems, bands, T, atomic, mol_db, t_elec=args.t_elec)
        hexv = cie_color.spectrum_to_hex(inten)
        cells.append((T, hexv))
        dom = ("thermal" if diag["emission_fraction"] < 0.10 else
               "molecular bands" if diag["molecular_fraction"] >= 0.20 else
               "ionic" if diag["ionization_fraction"] >= 0.20 else "atomic lines")
        print(f"  {T:6d}K  {hexv}   {dom}  "
              f"(ionz={diag['ionization_fraction']:.2f} mol={diag['molecular_fraction']:.2f})")

    if args.html:
        sw = "".join(f'<div style="display:inline-block;width:54px;height:40px;background:{h};'
                     f'color:#fff;font-size:9px;text-align:center;line-height:40px">{t//1000}k</div>'
                     for t, h in cells)
        out = Path("/tmp/atmosphere_color.html")
        out.write_text(f'<html><body style="background:#111;color:#ddd;font-family:sans-serif;padding:20px">'
                       f'<h3>{args.composition}</h3><div>{sw}</div></body></html>')
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
