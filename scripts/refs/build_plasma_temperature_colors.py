# 조성·온도별 플라스마 발광색을 LTE Saha/Boltzmann 엔진으로 산출해 db/refs/plasma_temperature_colors.yaml 로 생성
"""Build the temperature-resolved plasma color table from the LTE engine.

Two tables:
  _blackbody  — thermal blackbody color (Planck → CIE 1931, EXACT), 1000-20000K.
  <composition> — per bulk gas, the emergent visible color of an LTE isothermal
    slab at each temperature (saha_boltzmann.slab_spectrum), 1000-15000K. The
    low-T thermal incandescence, the mid-T molecular bands, and the high-T
    atomic/ionic lines all emerge from Saha ionization + Boltzmann excitation +
    dissociation equilibrium — no hand-tuned weight (the old w(T) ramp is gone).

Per composition row carries the computed color plus physics diagnostics
(ionization_fraction, molecular_fraction, emission_fraction) and a one-word
`dominant` regime label for the visualizer tooltip.

See the engine module for the (documented) modeling choices. NOTE the LTE
caveat: band systems whose upper state is high-lying (N2 1P/2P at 7-11 eV) are
faint in LTE; the observed reentry/auroral blue-violet of air is a NON-LTE
(electron-impact) effect and is not reproduced here — a documented divergence.

Usage:
    python3 scripts/refs/build_plasma_temperature_colors.py
    python3 scripts/refs/build_plasma_temperature_colors.py --sanity
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cie_color                       # noqa: E402
import saha_boltzmann as sb            # noqa: E402
from cie_color import rgb_to_hex       # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "db" / "refs" / "plasma_temperature_colors.yaml"

BB_TEMPS = list(range(1000, 20001, 1000))
COMP_TEMPS = list(range(1000, 15001, 1000))

LABELS = {
    "air":   ("N2 / O2 (Earth-like)", "N2 / O2 (지구형)"),
    "co2":   ("CO2 (Mars / Venus)", "CO2 (화성 / 금성)"),
    "h2_he": ("H2 / He (gas giant)", "H2 / He (가스자이언트)"),
    "ch4":   ("CH4 (Titan-class)", "CH4 (타이탄형)"),
    "h2o":   ("H2O (steam)", "H2O (수증기)"),
    "nh3":   ("NH3 (ice-giant ammonia)", "NH3 (아이스자이언트 암모니아)"),
}


def _bb_note(T: int) -> str:
    if T <= 1500:
        return "deep red — ember / lava glow"
    if T <= 3000:
        return "warm orange — lava / cool-star surface"
    if T <= 5000:
        return "warm white — K/G-star tint"
    if T <= 7000:
        return "near white — Sun-like"
    if T <= 11000:
        return "blue-white — A-star / hot reentry"
    return "blue — hot star"


def _dominant(d: dict) -> str:
    if d["emission_fraction"] < 0.10:
        return "thermal incandescence"
    if d["molecular_fraction"] >= 0.20:
        return "molecular bands"
    if d["ionization_fraction"] >= 0.20:
        return "ionic lines"
    return "atomic lines"


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def build() -> dict:
    atomic, mol_db = sb.load_dbs()
    out: dict = {}

    bb: dict = {}
    for T in BB_TEMPS:
        rgb, xy = cie_color.blackbody_srgb(T)
        bb[T] = {
            "temp_k": T,
            "hex": rgb_to_hex(rgb),
            "rgb": [max(0, min(255, round(c * 255))) for c in rgb],
            "chromaticity_xy": [round(xy[0], 4), round(xy[1], 4)],
            "note": _bb_note(T),
        }
    out["_blackbody"] = bb

    for key in sb.COMPOSITIONS:
        bands = mol_db["composition_bands"].get(key, [])
        active = sorted(sb.COMPOSITIONS[key]) + bands
        rows: dict = {}
        for T in COMP_TEMPS:
            inten, diag = sb.slab_spectrum(key, T, atomic, mol_db)
            rgb = cie_color.spectrum_to_srgb_hue(inten)
            rows[T] = {
                "temp_k": T,
                "combined_hex": rgb_to_hex(rgb),
                "rgb": [max(0, min(255, round(c * 255))) for c in rgb],
                "ionization_fraction": diag["ionization_fraction"],
                "molecular_fraction": diag["molecular_fraction"],
                "emission_fraction": diag["emission_fraction"],
                "dominant": _dominant(diag),
            }
        en, ko = LABELS[key]
        out[key] = {
            "label_en": en,
            "label_ko": ko,
            "active_species": active,
            "colors": rows,
        }
    return out


HEADER = """\
# Plasma emission color vs temperature (1000K steps), per bulk composition.
#
# FIRST-PRINCIPLES LTE — built by scripts/refs/build_plasma_temperature_colors.py
# from the saha_boltzmann.py engine. Read the engine docstring for the model.
#   _blackbody: thermal blackbody color (Planck -> CIE 1931), EXACT, 1000-20000K.
#   <composition>: emergent color of an LTE isothermal slab — thermal continuum
#     + atomic lines (NIST A-values) + molecular bands (band-as-effective-line),
#     with ionization (Saha), excitation (Boltzmann) and dissociation (law of
#     mass action) all computed. No hand-tuned weight.
#
# Diagnostics per row: ionization_fraction, molecular_fraction, emission_fraction
# (luminance share from lines/bands vs thermal), and a `dominant` regime label.
# Colors are hue at full brightness (max-channel normalized), not luminance.
#
# LTE CAVEAT (documented divergence): high-lying band systems (N2 1P/2P, 7-11 eV)
# are thermally faint, so air does NOT show the observed reentry/auroral
# blue-violet here — that is a NON-LTE (electron-impact) effect. C2 Swan (2.5 eV)
# and H Balmer are thermally accessible and do appear.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sanity", action="store_true", help="print a color march; do not write")
    args = ap.parse_args()

    data = build()

    if args.sanity:
        temps = [1000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 15000]
        print("         " + "  ".join(f"{t // 1000:>5}k" for t in temps))
        for key in sb.COMPOSITIONS:
            cells = [data[key]["colors"][t]["combined_hex"] for t in temps]
            print(f"  {key:6} " + "  ".join(cells))
        return 0

    body = yaml.dump(data, Dumper=NoAliasDumper, sort_keys=False,
                     allow_unicode=True, default_flow_style=False)
    OUT.write_text(HEADER + body, encoding="utf-8")
    n_comp = len([k for k in data if not k.startswith("_")])
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(BB_TEMPS)} blackbody temps, "
          f"{n_comp} compositions x {len(COMP_TEMPS)} temps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
