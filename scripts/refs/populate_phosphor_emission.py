# element_plasma_colors.yaml 에 phosphor_emission regime entry 를 추가 (lanthanide Ln3+ 형광)
# one-shot: adds phosphor_emission regime to element_plasma_colors.yaml, output committed
"""Populate the phosphor_emission regime for lanthanides.

Atomic_flame regime conflates two physically distinct phenomena for
f-block elements: (a) the gas-phase atomic emission (which is faint
multi-line for most Ln), and (b) the trivalent ion Ln3+ emission in
a solid host (the famous "rare-earth phosphor" colors that dominate
display industry — TV red, fluorescent lamp green, etc.).

The Helmenstine chart's lanthanide colors are mostly the (b) signature.
With phosphor_emission as a separate regime, we can honestly attribute
those colors to where they actually come from, and keep atomic_flame
honest about the gas-phase chemistry (which is mostly weak/invisible).

Sources:
- Yen-Shionoya-Yamamoto "Phosphor Handbook" 2nd ed (2007)
- Blasse & Grabmaier "Luminescent Materials" (1994)

Run once after schema validation update.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "db" / "refs" / "element_plasma_colors.yaml"

sys.path.insert(0, str(ROOT / "scripts" / "refs"))
from wavelength_to_rgb import mix_lines, rgb_to_hex


# ─────────────────────────────────────────────────────────────────────
# Phosphor emission data (Ln3+ in solid host, host listed in basis)
# ─────────────────────────────────────────────────────────────────────

PHOSPHOR_DATA = {
    "Ce": {
        "canonical_hex": "#ffd400",   # YAG:Ce yellow (white-LED phosphor)
        "lines": [(535.0, 1000, "Ce3+ 5d→4f broadband (YAG:Ce)"),
                  (450.0, 200, "Ce3+ 5d→4f (Lu2SiO5:Ce PET scintillator)")],
        "basis": "Ce3+ 5d→4f broadband emission, host-dependent. YAG:Ce "
                 "(Y3Al5O12:Ce) is THE yellow phosphor in white LEDs "
                 "(blue InGaN + YAG:Ce yellow → white). Lu2SiO5:Ce (LSO) "
                 "is the workhorse PET scanner blue scintillator. Parity-"
                 "allowed transition (not 4f-4f) so broadband, not narrow.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook Ch.6; white-LED literature",
    },
    "Pr": {
        "canonical_hex": "#f25a3a",   # YAG:Pr red-orange
        "lines": [(615.0, 1000, "Pr3+ 3P0→3H6 (YAG:Pr red)"),
                  (650.0, 400, "Pr3+ 3P0→3F2"),
                  (525.0, 300, "Pr3+ 3P0→3H5 (green)"),
                  (488.0, 200, "Pr3+ 3P0→3H4 (blue-green)")],
        "basis": "Pr3+ phosphor in YAG host: dominant 615nm red 3P0→3H6 + "
                 "minor green/blue lines. Studied as red phosphor for white "
                 "LEDs (alternative to Eu3+) and quantum-cutting phosphor "
                 "for Hg-free fluorescent lamps.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook Ch.5",
    },
    "Sm": {
        "canonical_hex": "#ff8c00",   # Y2O3:Sm orange
        "lines": [(600.0, 1000, "Sm3+ 4G5/2→6H7/2 (Y2O3:Sm)"),
                  (647.0, 600, "Sm3+ 4G5/2→6H9/2"),
                  (565.0, 200, "Sm3+ 4G5/2→6H5/2 yellow-green"),
                  (705.0, 200, "Sm3+ 4G5/2→6H11/2 deep red")],
        "basis": "Sm3+ phosphor in Y2O3 host: orange 600nm dominant (4G5/2→6H7/2). "
                 "Used as orange phosphor reference but not a dominant display "
                 "phosphor (Eu3+ takes the red niche). Sm2+ in CaF2 was a "
                 "historical optical-pumping ruby laser predecessor (Maiman).",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook Ch.5",
    },
    "Eu": {
        "canonical_hex": "#ff0a14",   # Y2O3:Eu iconic TV red (1964+)
        "lines": [(612.0, 1000, "Eu3+ 5D0→7F2 (Y2O3:Eu — iconic TV red)"),
                  (590.0, 200, "Eu3+ 5D0→7F1 orange MD"),
                  (632.0, 150, "Eu3+ 5D0→7F3"),
                  (707.0, 200, "Eu3+ 5D0→7F4 deep red"),
                  (579.0, 50, "Eu3+ 5D0→7F0 (often forbidden)")],
        "basis": "Eu3+ in Y2O3 or Y2O2S host: 612nm red 5D0→7F2 is THE iconic "
                 "red phosphor for CRT TVs (1964 onward), tri-color fluorescent "
                 "lamps, plasma displays. One of the sharpest and most efficient "
                 "narrow red emitters known. Eu2+ broadband phosphors (BAM blue, "
                 "SrAl2O4 green afterglow) exist but the famous color is Eu3+ red.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook Ch.5; Y2O3:Eu TV phosphor history",
    },
    "Tb": {
        "canonical_hex": "#4aff2e",   # LaPO4:Ce,Tb iconic fluorescent lamp green
        "lines": [(545.0, 1000, "Tb3+ 5D4→7F5 (LaPO4:Ce,Tb green)"),
                  (488.0, 200, "Tb3+ 5D4→7F6 blue-green"),
                  (587.0, 250, "Tb3+ 5D4→7F4 yellow"),
                  (622.0, 150, "Tb3+ 5D4→7F3 orange-red")],
        "basis": "Tb3+ in LaPO4:Ce,Tb (LAP) and Gd2O2S:Tb is THE standard green "
                 "phosphor for tri-color fluorescent lamps and X-ray intensifying "
                 "screens. The 545nm 5D4→7F5 transition is one of the most "
                 "efficient narrow green emitters known. Near photopic peak "
                 "sensitivity — perceptually very bright.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook Ch.5; tri-color lamp",
    },
    "Dy": {
        "canonical_hex": "#fff5b0",   # Y3Al5O12:Dy white (blue + yellow dual)
        "lines": [(575.0, 1000, "Dy3+ 4F9/2→6H13/2 (yellow — dominant)"),
                  (480.0, 400, "Dy3+ 4F9/2→6H15/2 (blue)"),
                  (663.0, 100, "Dy3+ 4F9/2→6H11/2 (red weak)")],
        "basis": "Dy3+ phosphor has dual blue (480nm) + yellow (575nm) emission — "
                 "studied as single-dopant white-LED phosphor. Y/B ratio is "
                 "host-dependent (lower symmetry → stronger yellow). CaSO4:Dy is "
                 "used in radiation dosimetry phosphors.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook; single-dopant white LED literature",
    },
    "Ho": {
        "canonical_hex": "#4aff3a",   # Y2O3:Ho green-dominant
        "lines": [(540.0, 1000, "Ho3+ 5S2,5F4→5I8 (Y2O3:Ho green)"),
                  (644.0, 400, "Ho3+ 5F5→5I8 red"),
                  (488.0, 100, "Ho3+ 5F3→5I8 blue weak")],
        "basis": "Ho3+ 540nm green dominant + 644nm red secondary. Y2O3:Ho phosphor. "
                 "Used in up-conversion phosphors with Yb3+ sensitizer (980nm IR pump "
                 "→ visible green) for anti-counterfeiting inks and biological "
                 "imaging. Ho:YAG laser at 2.1μm IR for medical applications.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook; up-conversion literature",
    },
    "Er": {
        "canonical_hex": "#50ff3a",   # Y2O3:Er green
        "lines": [(545.0, 1000, "Er3+ 4S3/2→4I15/2 (Y2O3:Er green)"),
                  (525.0, 400, "Er3+ 2H11/2→4I15/2 green"),
                  (660.0, 300, "Er3+ 4F9/2→4I15/2 red")],
        "basis": "Er3+ 545nm green dominant. Er-doped silica fiber is the basis "
                 "of Erbium-Doped Fiber Amplifier (EDFA) at 1.5μm — the foundation "
                 "of long-haul optical telecom. Er3+/Yb3+ up-conversion phosphors "
                 "convert IR pump to visible green.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook; EDFA literature",
    },
    "Tm": {
        "canonical_hex": "#1a3aff",   # LaOBr:Tm X-ray screen blue
        "lines": [(455.0, 1000, "Tm3+ 1D2→3F4 (LaOBr:Tm blue)"),
                  (477.0, 400, "Tm3+ 1G4→3H6 blue"),
                  (650.0, 200, "Tm3+ 1G4→3F4 red minor")],
        "basis": "Tm3+ 455nm blue dominant. LaOBr:Tm is the BLUE component of "
                 "rare-earth X-ray intensifying screens (paired with Gd2O2S:Tb "
                 "green and Y2O2S:Eu red for tri-color X-ray imaging). Tm:YAG "
                 "laser at 2.0μm IR for surgical applications.",
        "source": "Yen-Shionoya-Yamamoto Phosphor Handbook; X-ray screen literature",
    },
}


# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    with open(DB_PATH, encoding="utf-8") as f:
        db = yaml.safe_load(f)

    n_added = 0
    for sym, data in PHOSPHOR_DATA.items():
        if sym not in db:
            print(f"  [WARN] {sym} not in DB; skipping", file=sys.stderr)
            continue
        entry = {
            "status": "visible",
            "hex": data["canonical_hex"],
            "hex_basis": "canonical_descriptor",
            "emission_lines": [
                {"nm": float(wl), "intensity": float(i),
                 **({"label": lbl} if lbl else {})}
                for (wl, i, lbl) in data["lines"]
            ],
            "basis": data["basis"],
            "source": data["source"],
        }
        db[sym]["regimes"]["phosphor_emission"] = entry
        n_added += 1

    # Re-sort by atomic number
    ordered = {sym: db[sym]
               for sym in sorted(db.keys(), key=lambda s: db[s]["atomic_number"])}

    header = """\
# Per-element plasma colors — multi-regime schema (v2).
#
# Each element has a `regimes:` block. The atomic_flame regime is
# populated for every element (preserves v1 data). reentry_plasma
# and aurora regimes are added in subsequent passes for the species
# where they're meaningfully different from atomic_flame.
# phosphor_emission regime added for lanthanides where Ln3+ in a
# solid host matrix is the chemistry-dominant signature (display
# phosphors, X-ray screens, etc.).
#
# Schema per regime:
#   status:    visible | no_flame_color | not_visible_to_humans
#              | too_radioactive | too_short | no_data | not_emitter
#   hex:       #rrggbb (lowercase 6-digit), or null if status != visible
#   hex_basis: cie_computed | canonical_descriptor | chart_approx
#              - cie_computed: derived from emission_lines via CIE
#                (scripts/refs/wavelength_to_rgb.py)
#              - canonical_descriptor: matches a standard color name
#                (crimson, lilac, etc.) — not naively recomputed
#              - chart_approx: visual estimate from Helmenstine 2017
#                — lowest confidence
#   emission_lines (when cie_computed): NIST lines + relative intensities
#   basis:     spectroscopic justification (free text)
#   source:    canonical reference

"""

    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    body = yaml.dump(
        ordered,
        Dumper=NoAliasDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    )
    DB_PATH.write_text(header + body, encoding="utf-8")

    print(f"added phosphor_emission regime to {n_added} lanthanides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
