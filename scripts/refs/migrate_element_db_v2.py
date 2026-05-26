# element_plasma_colors.yaml 을 multi-regime 스키마(v2)로 마이그레이션하는 일회용 도구
"""Migrate db/refs/element_plasma_colors.yaml to the multi-regime schema.

v1 shape:
    H:
      atomic_number: 1
      name: Hydrogen
      status: visible
      hex: "#ff5fa8"
      basis: ...
      source: ...

v2 shape:
    H:
      atomic_number: 1
      name: Hydrogen
      regimes:
        atomic_flame:
          status: visible
          hex: "#ff5fa8"
          hex_basis: cie_computed | canonical_descriptor | chart_approx
          emission_lines:          # present when hex_basis == cie_computed
            - {nm: 656.3, intensity: 500, label: Hα}
          basis: ...
          source: ...
        # reentry_plasma and aurora regimes added in subsequent migrations.

For elements where NIST emission lines are curated (CURATED_EMISSIONS
dict below): the script CIE-computes the hex from lines and stores
both the lines + the computed hex (`hex_basis: cie_computed`).

For canonical-descriptor elements (Li=crimson, Na=yellow, K=lilac etc.):
keeps the existing hex (which matches the standard color descriptor),
marks `hex_basis: canonical_descriptor`.

Everything else: marks `hex_basis: chart_approx`, preserves existing
hex. Visualizer can render those with a low-confidence indicator.

Run once. After migration, edits go directly into the v2 YAML.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
OUT_PATH = ROOT / "db" / "refs" / "element_plasma_colors_v2.yaml"

sys.path.insert(0, str(ROOT / "scripts" / "refs"))
from wavelength_to_rgb import mix_lines, rgb_to_hex


# ── Tier A: canonical descriptor — hex matches a standard color name ──
# These entries' hex values are deliberately picked to match how the
# named flame color is conventionally rendered (e.g. crimson = #DC143C
# is the standard CSS color "crimson"). Recomputing them via CIE on
# dominant single lines would give a different RGB that doesn't match
# the named color, so we keep the canonical mapping.
CANONICAL_DESCRIPTOR = {
    "Li", "Na", "K", "Rb", "Cs", "Ca", "Sr", "Ba", "Ra",
    "Cu", "Mg", "Tl", "Cd",
    "B", "P", "S",
    "Mn",
    # Complex spectra where a 5-line CIE mix gives wrong dominant hue:
    "Fe",   # gold flame from continuum of hundreds of weak visible lines
    "He",   # peach/pink discharge — D3 + many secondaries, hard to capture
    "Ar",   # violet/lilac discharge — broad UV+visible mix, not just red lines
}


# ── Tier B/C: NIST emission lines for CIE re-computation ──
# Each entry is (wavelength_nm, relative_intensity, label).
# Where multiple lines contribute perceptually, list them with NIST
# relative-intensity numbers (or proportional estimates).
# These produce the cie_computed hex.
CURATED_EMISSIONS: dict[str, list[tuple[float, float, str]]] = {
    "H":  [(656.3, 500, "Hα"), (486.1, 100, "Hβ"), (434.0, 50, "Hγ")],
    # He: moved to CANONICAL_DESCRIPTOR (peach descriptor more faithful than 4-line CIE)
    "Ne": [(640.2, 500, ""), (614.3, 200, ""), (588.2, 150, ""), (650.7, 200, "")],
    # Ar: moved to CANONICAL_DESCRIPTOR (violet descriptor; broad UV+visible mix)
    "Kr": [(557.0, 150, ""), (587.1, 200, ""), (758.7, 300, ""), (810.4, 250, "")],
    "Xe": [(467.1, 200, ""), (462.4, 150, ""), (823.2, 300, ""), (881.9, 250, "")],
    "Hg": [(404.7, 300, ""), (435.8, 800, ""), (546.1, 1000, ""), (577.0, 500, ""), (579.0, 500, "")],
    "C":  [(516.5, 500, "C2 Swan d→a"), (473.7, 400, "C2 Swan high-v"),
           (588.9, 200, "C2 Swan low-v"), (388.3, 300, "CN violet")],
    "N":  [(391.4, 500, "N2+ 1NG"), (427.8, 300, "N2+ 1NG"),
           (670.0, 200, "N2 1P band peak"), (337.1, 200, "N2 2P UV")],
    "O":  [(777.4, 500, "OI triplet"), (615.7, 200, "OI"),
           (557.7, 100, "OI green forbidden (low-T plasma weak)"),
           (630.0, 100, "OI red forbidden (low-T plasma weak)")],
    "F":  [(685.6, 200, "F I"), (690.2, 200, "F I"), (775.5, 150, "")],
    "Cl": [(754.7, 150, ""), (792.5, 150, ""), (837.6, 100, "")],
    "Br": [(478.5, 150, ""), (530.2, 150, ""), (827.2, 200, "")],
    "I":  [(511.0, 200, ""), (533.8, 150, ""), (546.5, 150, ""), (608.0, 200, "")],
    "Zn": [(481.0, 500, ""), (472.2, 400, "")],
    "Ga": [(403.3, 500, ""), (417.2, 400, "")],
    "In": [(410.2, 300, ""), (451.1, 500, "")],
    "Pb": [(405.8, 300, ""), (368.3, 100, "(UV)"), (722.9, 100, "")],
    "Bi": [(472.3, 300, ""), (422.8, 200, "")],
    # Fe omitted — the flame-test "gold" descriptor results from a continuum of
    # hundreds of weak visible lines that a 5-line CIE mix cannot capture
    # (it produces cyan from the UV-blue strongest lines). Better to leave Fe
    # as canonical_descriptor with the documented "gold" hex.
    # Note: Si, Co, Ni, Ag, Au, Pt, Ru, Rh, Pd, Os, Ir, La etc. — no curated
    # NIST visible lines that are perceptually significant. Stay chart_approx.
}

# Status override during migration: for elements where adding emission_lines
# justifies upgrading visibility (NIST has visible lines that v1 conservatively
# marked as not_visible_to_humans).
STATUS_OVERRIDE = {
    "F": "visible",
}


def parse_line_tuple(t):
    """Allow (nm, intensity) or (nm, intensity, label)."""
    if len(t) == 2:
        return (t[0], t[1], "")
    return t


def compute_cie_hex(lines: list) -> str:
    """Convert (nm, intensity, label) list → hex via CIE perceptual mix."""
    pairs = [(wl, i) for (wl, i, _) in (parse_line_tuple(t) for t in lines)]
    return rgb_to_hex(mix_lines(pairs))


def migrate() -> dict:
    with open(DB_PATH, encoding="utf-8") as f:
        v1 = yaml.safe_load(f)

    v2 = {}
    for sym, e in v1.items():
        old_status = e["status"]
        old_hex = e.get("hex")
        old_basis = e["basis"]
        old_source = e["source"]
        reentry_note = e.get("reentry_note")
        status = STATUS_OVERRIDE.get(sym, old_status)

        # Decide hex_basis + new hex
        if sym in CURATED_EMISSIONS and status == "visible":
            lines_data = CURATED_EMISSIONS[sym]
            cie_hex = compute_cie_hex(lines_data)
            new_hex = cie_hex
            hex_basis = "cie_computed"
            emission_lines = [
                {"nm": float(wl), "intensity": float(i), "label": lbl}
                for (wl, i, lbl) in (parse_line_tuple(t) for t in lines_data)
            ]
        elif sym in CANONICAL_DESCRIPTOR and status == "visible":
            new_hex = old_hex
            hex_basis = "canonical_descriptor"
            emission_lines = None
        else:
            new_hex = old_hex if status == "visible" else None
            hex_basis = "chart_approx" if (status == "visible" and new_hex) else None
            emission_lines = None

        atomic_flame = {
            "status": status,
            "hex": new_hex,
        }
        if new_hex is not None:
            atomic_flame["hex_basis"] = hex_basis
        if emission_lines:
            atomic_flame["emission_lines"] = emission_lines
        atomic_flame["basis"] = old_basis
        atomic_flame["source"] = old_source
        if reentry_note:
            atomic_flame["reentry_note"] = reentry_note

        v2[sym] = {
            "atomic_number": e["atomic_number"],
            "name": e["name"],
            "regimes": {
                "atomic_flame": atomic_flame,
            },
        }
    return v2


def main() -> int:
    v2 = migrate()

    # Sort by atomic number while preserving the symbol-as-key shape
    ordered = {sym: v2[sym] for sym in sorted(v2.keys(), key=lambda s: v2[s]["atomic_number"])}

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
    OUT_PATH.write_text(header + body, encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(ROOT)} (review before promoting to canonical path)")

    # Report
    visible = sum(1 for e in v2.values()
                  if e["regimes"]["atomic_flame"]["status"] == "visible")
    cie_count = sum(1 for e in v2.values()
                    if e["regimes"]["atomic_flame"].get("hex_basis") == "cie_computed")
    canonical = sum(1 for e in v2.values()
                    if e["regimes"]["atomic_flame"].get("hex_basis") == "canonical_descriptor")
    chart = sum(1 for e in v2.values()
                if e["regimes"]["atomic_flame"].get("hex_basis") == "chart_approx")

    print(f"migrated {len(v2)} entries to v2 schema")
    print(f"  atomic_flame.visible:     {visible}")
    print(f"  hex_basis breakdown:")
    print(f"    cie_computed:           {cie_count}")
    print(f"    canonical_descriptor:   {canonical}")
    print(f"    chart_approx:           {chart}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
