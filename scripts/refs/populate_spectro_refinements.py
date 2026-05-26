# element_plasma_colors.yaml 의 chart_approx 항목을 분광 자료 정밀 재검토 결과로 추가 격상/격하
"""Apply spectroscopic-research refinements to chart_approx entries.

Subagent-delivered NIST + phosphor literature review (2026-05-26 session)
identified specific corrections to chart-derived entries. Applied here.

Six material changes:
- Zr: chart blue → canonical "brilliant white" (pyrotechnic Zr powder
  combustion; Conkling Ch.6)
- Gd: chart orange → not_visible_to_humans (Gd3+ lowest state at 312nm
  UV-C only; used as sensitizer not emitter)
- Yb: chart pale teal → not_visible_to_humans (Yb3+ has one excited
  state at 980nm IR only)
- Lu: chart pale cyan → no_data (Lu3+ 4f14 closed shell, no f-f
  transitions whatsoever)
- Pr: chart magenta → no_data (chart is anomalous; real flame is
  pale green or invisible, aqueous Pr3+ is pale green)
- Tm: chart pale cyan → cie_computed blue (Tm3+ 455nm narrow phosphor;
  chart's cyan-green is wrong direction)
- V: chart_approx yellow-green → canonical_descriptor (VO γ band system
  573-626nm dominant in oxidizing flame; matches WebElements / Conkling)

Plus basis-only refinements for 10 lanthanides (Ce, Eu, Tb, Ho, Er, Sm,
Dy, Nd) + 3 refractory metals (Nb, Ta, Hf) where hex stays but basis
honestly notes the regime mismatch (phosphor color in atomic_flame slot,
or arc-discharge color without flame-chemistry support).

Subagent research sources:
- NIST Atomic Spectra Database (atomic emission lines, intensities)
- Yen-Shionoya-Yamamoto "Phosphor Handbook" 2nd ed (2007)
- Blasse & Grabmaier "Luminescent Materials" (1994)
- Conkling "Chemistry of Pyrotechnics" 2nd ed (2010)
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
# Substantive changes (status / hex / basis all updated)
# ─────────────────────────────────────────────────────────────────────

# 1. canonical_descriptor upgrades — chemistry literature confirms color
CANONICAL_UPGRADES = {
    "Zr": {
        "hex": "#f5f5f5",
        "basis": "Zirconium powder combustion gives brilliant white from ZrO2 "
                 "thermal incandescence (refractory oxide >3000K). Zr is a "
                 "primary white-component in military parachute illumination "
                 "and photoflash composition. The chart's blue is unsupported "
                 "by pyrotechnic literature — it likely reflects arc-discharge "
                 "perception of Zr II UV + Zr I 386/396nm violet, not flame.",
        "source": "Conkling 'Chemistry of Pyrotechnics' 2nd ed Ch.6 (2010)",
    },
    "V": {
        "hex": "#e8e83b",
        "basis": "Vanadium flame color is yellow-green from VO γ molecular "
                 "band system (573-626nm), dominant in oxidizing flame and in "
                 "M-dwarf stellar opacity (VO γ at 573nm is a classifier). "
                 "Atomic V I 411-440nm blue cluster exists but only dominates "
                 "in arc discharge or ICP-OES (inert atmosphere). For the "
                 "flame regime, VO γ is canonical.",
        "source": "Conkling 'Chemistry of Pyrotechnics' Ch.6; Pearse & Gaydon",
    },
}

# 2. cie_computed upgrade — Tm phosphor blue (corrects chart direction)
CIE_UPGRADES = {
    "Tm": {
        "lines": [(455.0, 1000, "Tm3+ 1D2-3F4 (a)"),
                  (477.0, 400, "Tm3+ 1G4-3H6"),
                  (650.0, 200, "Tm3+ 1G4-3F4 minor red"),
                  (360.0, 100, "Tm3+ 1D2-3H6 UV")],
        "basis": "Tm3+ phosphor in LaOBr (LaOBr:Tm) emits narrow blue at 455nm — "
                 "historical blue component of rare-earth X-ray intensifying "
                 "screens (paired with Gd2O2S:Tb green and Y2O2S:Eu red for "
                 "tri-color X-ray imaging). The chart's pale cyan-green is "
                 "the wrong direction; true Tm3+ is saturated blue.",
        "source": "Yen-Shionoya-Yamamoto 'Phosphor Handbook' 2nd ed Ch.5 (2007)",
    },
}

# 3. downgrades to not_visible_to_humans — spectroscopy shows no visible
DOWNGRADES_TO_INVISIBLE = {
    "Gd": ("Gd3+ has lowest excited state 6P7/2 at ~32,000 cm⁻¹ = **312nm UV-C**. "
           "All Gd3+ emission is UV. Used in medical phototherapy lamps "
           "(311nm narrowband for psoriasis), not as visible phosphor. Gd is "
           "a sensitizer cation in many lanthanide phosphors (energy donor to "
           "co-dopant), never the emitter. The chart's orange is unsupported.",
           "Yen-Shionoya-Yamamoto Phosphor Handbook; medical lamp spec"),
    "Yb": ("Yb3+ has ONE excited 4f level (2F5/2) → ONE emission line at 980nm "
           "IR. No visible. Used as **sensitizer** in up-conversion phosphors "
           "(absorbs 980nm pump, transfers to Er/Ho/Tm co-dopant). Yb:YAG laser "
           "(1030-1080nm) is industrial workhorse. Pure Yb3+: zero visible. "
           "Chart's pale teal is unsupported.",
           "Yb:YAG laser literature; Yen-Shionoya-Yamamoto"),
}

# 4. downgrades to no_data (chart entries that are spectroscopically wrong
#    OR represent transitions that don't exist)
DOWNGRADES_TO_NO_DATA = {
    "Lu": ("Lu3+ has [Xe]4f¹⁴ — **filled f-shell, no f-f transitions exist**. "
           "Lu emits nothing in visible from its 4f electrons. Atomic Lu I/II "
           "has faint violet-blue arc lines but no characteristic flame color. "
           "Lu's main role is as **host cation** in scintillators "
           "(Lu2SiO5:Ce for PET scanners) — Lu provides density, Ce does the "
           "emission. The chart's pale cyan is unsupported.",
           "Yen-Shionoya-Yamamoto; LSO/PET scintillator literature"),
    "Pr": ("The chart's 'magenta' is anomalous — not corroborated by either "
           "atomic plasma color or aqueous Pr3+ color (both are pale green). "
           "Pr3+ phosphors in YAG host emit RED at 615nm (3P0→3H6), but classical "
           "Pr salt flame is faintly green-yellow. The most honest call: no_data "
           "for the flame regime. Phosphor regime if introduced would show red.",
           "Yen-Shionoya-Yamamoto; WebElements Pr aqueous"),
}


# ─────────────────────────────────────────────────────────────────────
# Basis-only refinements (hex stays; just acknowledge regime mismatch)
# ─────────────────────────────────────────────────────────────────────

BASIS_REFINEMENTS = {
    # Lanthanides where chart color is phosphor color in flame slot — keep hex
    # but document the regime mismatch.
    "Ce": ("Ce3+ has 5d→4f broadband emission (parity-allowed, host-dependent). "
           "In YAG:Ce host → yellow 535nm (white-LED phosphor). In Ce-glass / "
           "CeO2 → blue-violet to white. Classical flame test gives little. "
           "The chart's blue reflects either Ce3+ 5d-4f UV-violet tail or CeO2 "
           "incandescence — phosphor regime rather than atomic flame.",
           "Yen-Shionoya-Yamamoto; YAG:Ce white-LED literature"),
    "Eu": ("The named Eu signature is the solid-state Eu3+ red phosphor "
           "612nm (5D0→7F2, the iconic Y2O3:Eu TV red since 1964). Classical "
           "Eu salt in flame is very pale violet, barely visible. The chart's "
           "pale violet is actually a fair atomic-flame observation — one of "
           "the chart's better entries. The famous red is the phosphor regime, "
           "not flame.",
           "Yen-Shionoya-Yamamoto; Y2O3:Eu TV phosphor literature"),
    "Tb": ("Tb3+ 545nm green is the iconic fluorescent-lamp green phosphor "
           "(LaPO4:Ce,Tb tri-color lamp) and X-ray screen green (Gd2O2S:Tb). "
           "Classical Tb salt flame is barely visible. The chart's yellow-green "
           "represents phosphor color in flame slot — regime mismatch, color "
           "direction correct.",
           "Yen-Shionoya-Yamamoto; LaPO4:Ce,Tb fluorescent lamp"),
    "Ho": ("Ho3+ 540nm green dominant (Y2O3:Ho phosphor; up-conversion green "
           "from Yb,Ho co-doped IR pump). Classical flame is very faint. The "
           "chart's bright green is one of the more defensible Ln entries — "
           "matches phosphor color and is plausibly observable in concentrated "
           "salt flame.",
           "Yen-Shionoya-Yamamoto; up-conversion phosphor literature"),
    "Er": ("Er3+ 545nm green dominant + 1.5μm IR (Er-doped fiber amplifier, "
           "the basis of optical telecom). Classical flame faint. The chart's "
           "pale green reflects Er3+ phosphor color in flame slot — regime "
           "mismatch, color direction correct.",
           "EDFA literature; Yen-Shionoya-Yamamoto"),
    "Sm": ("Sm3+ 600nm orange dominant (Y2O3:Sm). Used as orange phosphor "
           "reference but not dominant display phosphor. Classical Sm salt "
           "flame is very faint; aqueous Sm3+ is pale yellow. The chart's "
           "pale peach reflects Sm3+ orange phosphor color in flame slot.",
           "Yen-Shionoya-Yamamoto; CaF2:Sm2+ Maiman ruby laser predecessor"),
    "Dy": ("Dy3+ has blue (480nm) + yellow (575nm) dual emission — used as "
           "single-dopant white-LED phosphor candidate. Classical Dy salt "
           "flame is very faint; aqueous Dy3+ is pale yellow-green. The "
           "chart's pale cyan-green picks up the blue component (480nm) but "
           "misses the dominant yellow.",
           "Yen-Shionoya-Yamamoto; CaSO4:Dy dosimeter"),
    "Nd": ("Nd3+ is fundamentally an IR emitter (1064nm, the Nd:YAG laser "
           "line). Visible 525/588/600nm transitions exist but very weak. "
           "Aqueous Nd3+ and didymium glass are pink-violet (CH4 absorbs "
           "yellow Na D-line). Classical Nd salt flame is very pale violet. "
           "The chart's violet is consistent with the aqueous color and "
           "didymium-glass appearance — defensible if read as solid/solution "
           "Nd3+ reference, not gas-phase atomic flame.",
           "Nd:YAG laser literature; didymium-glass welding goggles"),
    # Refractory metals where arc plasma color is the source (no flame chemistry)
    "Nb": ("Niobium has no documented characteristic flame test color "
           "(absent from Vogel's Qualitative Inorganic Analysis tables). "
           "The chart's blue traces to arc-discharge perception of Nb I "
           "405-410nm violet triplet — arc plasma context, not flame "
           "chemistry. Honest answer for true flame regime: no_data.",
           "NIST Nb I; Vogel's analytical chemistry (no entry)"),
    "Ta": ("Tantalum has no documented characteristic flame test color. "
           "The chart's blue traces to arc-discharge perception of Ta I "
           "474-491nm visible cluster — arc context, not flame chemistry. "
           "Ta has industrial use (capacitors, surgical implants) but no "
           "flame-chemistry tradition.",
           "NIST Ta I; absent from analytical flame test references"),
    "Hf": ("Hafnium has no documented characteristic flame test color "
           "(chemical homolog of Zr; would similarly white-incandesce if "
           "combusted as powder, but not used that way). The chart's pale "
           "gray-cyan is a placeholder, not chemistry-backed. Arc plasma "
           "shows UV-violet Hf I dim emission.",
           "NIST Hf I; Zr-analog combustion chemistry"),
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
    n_no_data = 0
    n_basis_only = 0

    for sym, data in CANONICAL_UPGRADES.items():
        af = db[sym]["regimes"]["atomic_flame"]
        af["status"] = "visible"
        af["hex"] = data["hex"]
        af["hex_basis"] = "canonical_descriptor"
        af.pop("emission_lines", None)
        af["basis"] = data["basis"]
        af["source"] = data["source"]
        n_canonical += 1

    for sym, data in CIE_UPGRADES.items():
        af = db[sym]["regimes"]["atomic_flame"]
        new_hex = compute_hex(data["lines"])
        af["status"] = "visible"
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

    for sym, (basis, source) in DOWNGRADES_TO_NO_DATA.items():
        af = db[sym]["regimes"]["atomic_flame"]
        af["status"] = "no_data"
        af["hex"] = None
        af.pop("hex_basis", None)
        af.pop("emission_lines", None)
        af["basis"] = basis
        af["source"] = source
        n_no_data += 1

    for sym, (basis, source) in BASIS_REFINEMENTS.items():
        af = db[sym]["regimes"]["atomic_flame"]
        af["basis"] = basis
        af["source"] = source
        n_basis_only += 1

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

    print(f"canonical_descriptor upgrades:    {n_canonical} (Zr, V)")
    print(f"cie_computed upgrades:            {n_cie} (Tm)")
    print(f"not_visible_to_humans downgrades: {n_invisible} (Gd, Yb)")
    print(f"no_data downgrades:               {n_no_data} (Lu, Pr)")
    print(f"basis-only refinements:           {n_basis_only}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
