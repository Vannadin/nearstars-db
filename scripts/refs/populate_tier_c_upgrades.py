# element_plasma_colors.yaml 의 chart_approx 항목을 분광 자료 재검토로 격상/격하하는 일회용 도구
"""Re-categorize chart_approx entries in element_plasma_colors.yaml based on
spectroscopic review.

Three operations per element:

1. CANONICAL_UPGRADES — chart_approx → canonical_descriptor.
   Element has a well-documented named flame/emission color from a
   chemistry-literature source (not just the Helmenstine chart).
   Hex stays the same (matches the descriptor); basis/source updated;
   hex_basis label changes.

2. CIE_UPGRADES — chart_approx → cie_computed.
   Element has clear visible-band NIST emission lines. Add
   emission_lines, recompute hex via CIE, update basis/source.

3. DOWNGRADES_TO_INVISIBLE — chart_approx → not_visible_to_humans.
   Element's dominant emission is UV/IR; visible contribution
   perceptually negligible. Clear hex + hex_basis (schema requires
   null hex for non-visible status).

Run once after the initial v2 migration. Idempotent — re-running
overwrites the same fields.
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
# 1. canonical_descriptor upgrades — named flame colors with literature
# ─────────────────────────────────────────────────────────────────────

CANONICAL_UPGRADES = {
    "Al": {
        "hex": "#e8e8e8",
        "basis": "Al I 396.2/394.4nm UV-violet emission. Real Al combustion "
                 "(aluminum-powder pyrotechnics, thermite) appears brilliant "
                 "white from Al2O3 thermal incandescence — continuum rather "
                 "than atomic emission. Canonical descriptor is 'brilliant white'.",
        "source": "Pyrotechnic literature (Conkling); NIST Al I",
    },
    "Th": {
        "hex": "#e8e8e8",
        "basis": "ThO2-impregnated Welsbach gas mantle: brilliant white "
                 "thermal continuum + selective IR emission. Discovered "
                 "1885 (Auer von Welsbach), commercialized in gas lamps. "
                 "Canonical 'brilliant white' descriptor.",
        "source": "Wikipedia Gas mantle; Welsbach 1885 patent",
    },
    "U": {
        "hex": "#cfe83b",
        "basis": "Uranium signature green from two combined mechanisms: "
                 "(a) UO2 thermal incandescence in oxidizing flame and "
                 "(b) U(VI) fluorescence (uranyl ion ~520nm emission) "
                 "in uranium glass under UV. Both produce the same "
                 "yellow-green descriptor.",
        "source": "Wikipedia Uranium glass; Auer 1903 mantle observations",
    },
}


# ─────────────────────────────────────────────────────────────────────
# 2. cie_computed upgrades — NIST lines with visible-band confidence
# ─────────────────────────────────────────────────────────────────────

CIE_UPGRADES = {
    "Ti": {
        "lines": [(498.2, 200, "Ti I"),
                  (506.5, 250, "Ti I"),
                  (519.3, 250, "Ti I"),
                  (520.5, 300, "Ti I"),
                  (453.4, 100, "Ti II blue")],
        "basis": "Ti I green cluster 498/506/519/520nm + Ti II 453nm blue. "
                 "Atomic Ti emission in plasma/arc discharge is dominantly "
                 "green from the visible Ti I lines.",
        "source": "NIST Ti I + Ti II",
    },
    "Cr": {
        "lines": [(520.4, 350, "Cr I (a)"),
                  (520.6, 350, "Cr I (b)"),
                  (520.8, 350, "Cr I (c)"),
                  (425.4, 100, "Cr I violet"),
                  (427.5, 100, "Cr I")],
        "basis": "Cr I 520.4/520.6/520.8nm triplet — the famous 'chrome-green' "
                 "responsible for emerald color in chromium-containing minerals "
                 "(emerald, ruby, alexandrite). The chart's orange-yellow "
                 "depiction does not match chromium's true atomic spectrum.",
        "source": "NIST Cr I; classical chrome-green flame chemistry",
    },
    "Se": {
        "lines": [(473.1, 400, "Se I (a)"),
                  (479.9, 350, "Se I (b)"),
                  (506.1, 200, "Se I (c)")],
        "basis": "Se I 473.1/479.9nm blue doublet + 506nm green minor. "
                 "Selenium discharge is characteristically pale blue.",
        "source": "NIST Se I; selenium lamp discharge",
    },
    "Mo": {
        "lines": [(550.6, 400, "Mo I (a)"),
                  (553.3, 350, "Mo I (b)"),
                  (515.5, 200, "Mo I"),
                  (379.8, 100, "Mo I UV-violet")],
        "basis": "Mo I 550-553nm yellow-green doublet. Documented in "
                 "molybdenum arc discharges and molybdate flame chemistry.",
        "source": "NIST Mo I; Mo discharge tube",
    },
    "Te": {
        "lines": [(525.7, 400, "Te I band"),
                  (535.4, 350, "Te I"),
                  (566.9, 300, "Te I"),
                  (700.6, 100, "Te I red")],
        "basis": "Te I 525-567nm green band. Tellurium halide flame chemistry "
                 "gives characteristic pale green.",
        "source": "NIST Te I; Te halide flame literature",
    },
    "W": {
        "lines": [(540.1, 400, "W I (a)"),
                  (547.6, 350, "W I (b)"),
                  (522.5, 300, "W I"),
                  (560.6, 200, "W I")],
        "basis": "W I 540/547nm green cluster + 522/560 secondary. "
                 "Documented in tungsten lamp discharge spectra.",
        "source": "NIST W I; tungsten lamp discharge",
    },
    "Re": {
        "lines": [(488.9, 350, "Re I"),
                  (506.6, 400, "Re I"),
                  (527.6, 350, "Re I"),
                  (581.7, 200, "Re I yellow")],
        "basis": "Re I 488-528nm green cluster + 581nm yellow. "
                 "Atomic rhenium plasma emission falls in cyan-green to yellow.",
        "source": "NIST Re I",
    },
    "Y": {
        "lines": [(615.6, 400, "YO band (0,0)"),
                  (636.4, 350, "YO band"),
                  (648.2, 300, "YO band"),
                  (410.2, 100, "Y I violet")],
        "basis": "YO molecular band system 615-648nm orange-red dominates "
                 "yttrium flame chemistry (YCl3, YNO3 salts). Atomic Y I "
                 "410nm violet is weaker. The chart's yellow depiction "
                 "leans toward green-yellow rather than the spectroscopic "
                 "orange-red.",
        "source": "YO band system (Joshi et al.); NIST Y I",
    },
}


# ─────────────────────────────────────────────────────────────────────
# 3. downgrade to not_visible_to_humans — UV-dominant elements
# ─────────────────────────────────────────────────────────────────────

DOWNGRADES_TO_INVISIBLE = {
    "Ge": ("Ge I dominant emission UV (265/270/304nm electronic). Visible "
           "lines 535/572nm perceptually negligible vs thermal continuum. "
           "No documented characteristic flame color.",
           "NIST Ge I (mostly UV)"),
    "As": ("As I dominant UV (235/278/286nm). Visible 615nm orange faint single "
           "line. Real arsenic flame appears pale-bluish white from oxide "
           "incandescence rather than atomic As emission.",
           "NIST As I (mostly UV)"),
    "Sn": ("Sn I dominant UV (235/284nm). Visible 452/563nm minor lines; "
           "tin flame appearance is pale blue-white incandescence from SnO/SnO2 "
           "rather than characteristic atomic emission.",
           "NIST Sn I (mostly UV)"),
    "Sb": ("Sb I dominant UV (252/259nm). Visible 614/777nm faint. Antimony "
           "flame test appearance is pale blue-green from oxide incandescence "
           "rather than atomic Sb emission.",
           "NIST Sb I (mostly UV)"),
}


# ─────────────────────────────────────────────────────────────────────

def compute_hex(lines):
    pairs = [(wl, i) for (wl, i, _) in lines]
    return rgb_to_hex(mix_lines(pairs))


def main() -> int:
    with open(DB_PATH, encoding="utf-8") as f:
        db = yaml.safe_load(f)

    n_canonical = 0
    n_cie = 0
    n_invisible = 0

    for sym, data in CANONICAL_UPGRADES.items():
        af = db[sym]["regimes"]["atomic_flame"]
        af["hex"] = data["hex"]
        af["hex_basis"] = "canonical_descriptor"
        if "emission_lines" in af:
            del af["emission_lines"]
        af["basis"] = data["basis"]
        af["source"] = data["source"]
        n_canonical += 1

    for sym, data in CIE_UPGRADES.items():
        af = db[sym]["regimes"]["atomic_flame"]
        new_hex = compute_hex(data["lines"])
        af["hex"] = new_hex
        af["hex_basis"] = "cie_computed"
        af["emission_lines"] = [
            {"nm": float(wl), "intensity": float(i),
             **({"label": lbl} if lbl else {})}
            for (wl, i, lbl) in data["lines"]
        ]
        af["basis"] = data["basis"]
        af["source"] = data["source"]
        n_cie += 1

    for sym, (basis, source) in DOWNGRADES_TO_INVISIBLE.items():
        af = db[sym]["regimes"]["atomic_flame"]
        af["status"] = "not_visible_to_humans"
        af["hex"] = None
        af.pop("hex_basis", None)
        af.pop("emission_lines", None)
        af["basis"] = basis
        af["source"] = source
        n_invisible += 1

    ordered = {sym: db[sym]
               for sym in sorted(db.keys(), key=lambda s: db[s]["atomic_number"])}

    header = """\
# Per-element plasma colors — multi-regime schema (v2).
#
# Each element has a `regimes:` block. The atomic_flame regime is
# populated for every element (preserves v1 data). reentry_plasma
# and aurora regimes are added in subsequent passes for the species
# where they're meaningfully different from atomic_flame.
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

    print(f"canonical_descriptor upgrades:    {n_canonical}")
    print(f"cie_computed upgrades:            {n_cie}")
    print(f"not_visible_to_humans downgrades: {n_invisible}")
    print(f"total chart_approx changes:       {n_canonical + n_cie + n_invisible}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
