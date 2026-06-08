# 행성 진입 속도(+대기 조성) → 대표 재진입 플라스마 온도 → 색을 산출하는 CLI (속도-온도 매핑 + 2온도 비-LTE)
"""Per-planet reentry plasma color from entry velocity + atmosphere composition.

Maps an atmospheric ENTRY VELOCITY to a representative radiating shock-layer
temperature, then runs the engine on the atmosphere composition to get the
reentry plasma color. Non-LTE (two-temperature) is ON by default — faster
entries get a hotter electron temperature, which lights up the N2-family
blue-violet (N2+ 1NG 391nm), the way real air reentry looks.

Velocity → temperature (EMPIRICAL, anchored to air reentry, not engineering):
  T_gas  ≈ 502 · V^1.25      (LEO 7.8 km/s → ~6500K, lunar 11 km/s → ~10000K)
  T_elec ≈ max(1000·V, T_gas) (electron temp behind the shock; only affects the
                               nlte-tagged N2 bands, i.e. N2-bearing atmospheres)
both snapped to the 1000K grid and clamped to [1000, 15000/20000]K. Above the
table range (e.g. Jupiter ~47 km/s) it clamps + flags — extreme entries exceed
LTE and this table.

Entry velocity ≈ planet escape velocity + approach speed. Rough refs (km/s):
  Earth LEO 7.8 · Earth lunar-return 11 · Mars 5.5 · Venus 11 · Titan 6 ·
  Saturn 30 · Neptune 23 · Jupiter 47.

Usage:
    python3 scripts/refs/reentry_color.py --velocity 11 "N2:0.78,O2:0.21"
    python3 scripts/refs/reentry_color.py --velocity 5.5 "CO2:0.95,N2:0.05" --lte
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cie_color                        # noqa: E402
import saha_boltzmann as sb             # noqa: E402
import emit_atmosphere_color as eac     # noqa: E402

T_MAX = 15000
TE_MAX = 20000


def _snap(t, lo, hi):
    return max(lo, min(hi, round(t / 1000) * 1000))


def velocity_to_temps(v_kms: float):
    t_gas = _snap(502.0 * v_kms ** 1.25, 1000, T_MAX)
    t_elec = _snap(max(1000.0 * v_kms, t_gas), t_gas, TE_MAX)
    return t_gas, t_elec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("composition", help='molecular mole fractions, e.g. "N2:0.78,O2:0.21"')
    ap.add_argument("--velocity", type=float, required=True, help="entry velocity [km/s]")
    ap.add_argument("--lte", action="store_true", help="force strict LTE (no non-LTE blue)")
    args = ap.parse_args()

    atomic, mol_db = sb.load_dbs()
    elems, dropped, molecules = eac.composition_to_atoms(args.composition)
    if not elems:
        print("No supported emitting elements (H/He/C/N/O/S).", file=sys.stderr)
        return 1
    bands = eac.select_bands(elems, mol_db)
    t_gas, t_elec = velocity_to_temps(args.velocity)
    has_nlte = any(mol_db["band_systems"][b].get("nlte") for b in bands)

    inten, diag = sb.slab_spectrum_custom(elems, bands, t_gas, atomic, mol_db,
                                          t_elec=(t_gas if args.lte else t_elec))
    hexv = cie_color.spectrum_to_hex(inten)
    lte_inten, _ = sb.slab_spectrum_custom(elems, bands, t_gas, atomic, mol_db)
    lte_hex = cie_color.spectrum_to_hex(lte_inten)

    print(f"entry velocity: {args.velocity} km/s")
    print(f"  → T_gas  = {t_gas} K   T_elec = {t_elec} K"
          + ("  (LTE forced)" if args.lte else ""))
    print(f"atmosphere: {molecules}"
          + (f"   (dropped {dropped})" if dropped else ""))
    print(f"  atomic: " + ", ".join(f"{e}={f:.2f}" for e, f in sorted(elems.items())))
    print(f"  bands: {bands or '(atomic only)'}"
          + ("   [N2-family non-LTE active]" if has_nlte and not args.lte else ""))
    print()
    print(f"  REENTRY COLOR:  {hexv}   (ionz={diag['ionization_fraction']:.2f})")
    print(f"  (LTE-only ref:  {lte_hex})")
    if args.velocity * 1000 > TE_MAX or 502.0 * args.velocity ** 1.25 > T_MAX:
        print(f"\n  NOTE: {args.velocity} km/s exceeds the table/LTE range — clamped. "
              f"Extreme entries (gas giants) are strongly non-equilibrium beyond this model.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
