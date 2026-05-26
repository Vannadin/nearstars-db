# element_plasma_colors.yaml 에 reentry_plasma + aurora regime entry 를 채워넣는 일회용 도구
"""Populate reentry_plasma and aurora regimes for atmospherically-relevant species.

Reentry plasma (~8000–15000 K, shock-heated, high pressure):
  Dominated by ionized lines (X I and X II) plus broadband thermal continuum.
  Hand-curated NIST line sets emphasizing visible-band ions + strongest
  neutrals. Source per entry: NIST + reentry spectroscopy literature.

Aurora (low density, 100–500 km on Earth-like atmospheres):
  Dominated by forbidden transitions of atomic species (OI green, OI red)
  plus N2+ First Negative band. Limited to ~6 atomic species + a few
  diatomic molecules (molecules go in molecular DB, not here).
  Polyatomics get status=not_emitter with dissociation note.

Run once after the v2 migration. Idempotent — re-running overwrites only
the reentry_plasma + aurora regime blocks.
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
# Reentry plasma regime data
# ─────────────────────────────────────────────────────────────────────
# Atmospherically relevant species at ~10000K shock temperature.
# Lines combine neutral X I + ionized X II where the ionized contribution
# is significant. Intensities are perceptually-weighted NIST values.

REENTRY_DATA = {
    "H": {
        "lines": [(656.3, 500, "Hα"), (486.1, 200, "Hβ"), (434.0, 100, "Hγ"),
                  (410.2, 50, "Hδ")],
        "basis": "Balmer series fully populated at 10000K. Hα still dominant red, "
                 "but Hβ contribution grows relative to flame T. Slightly bluer pink.",
        "source": "NIST H I; reentry spectroscopy lit",
    },
    "He": {
        "lines": [(587.6, 500, "D3"), (667.8, 200, ""), (706.5, 200, ""),
                  (501.6, 150, ""), (471.3, 100, ""), (388.9, 200, "UV-blue")],
        "basis": "He I lines + more visible blue at high T. Slightly cooler than discharge tube peach.",
        "source": "NIST He I; reentry spectra",
    },
    "C": {
        "lines": [(516.5, 500, "C2 Swan d→a"), (473.7, 400, "C2 Swan high-v"),
                  (469.8, 300, "C2 Swan"), (438.3, 200, "CH band"),
                  (388.3, 400, "CN violet")],
        "basis": "At reentry temps C2 Swan green + CN violet dominate. "
                 "Earth blackbody continuum from soot is absent in shock plasma.",
        "source": "arXiv 2007.04869; Mars EDL camera footage",
    },
    "N": {
        "lines": [(391.4, 500, "N2+ 1NG"), (427.8, 300, "N2+ 1NG"),
                  (670.0, 250, "N2 1P"), (744.2, 100, "NI"),
                  (821.6, 150, "NI IR")],
        "basis": "N2+ 391nm First Negative + N2 1NG red — classic Earth reentry signature. "
                 "Blue-violet hue is canonical.",
        "source": "Air plasma optical spectra (ResearchGate); Earth reentry video",
    },
    "O": {
        "lines": [(777.4, 400, "OI triplet"), (615.7, 300, "OI"),
                  (557.7, 200, "OI green"), (630.0, 200, "OI red"),
                  (844.6, 200, "OI IR"), (436.8, 100, "OI II")],
        "basis": "Atomic O lines stronger at reentry T than flame T. Combined with N2 "
                 "in mixed atmospheres gives blue-violet (see N entry).",
        "source": "NASA reentry spectroscopy",
    },
    "Ne": {
        "lines": [(640.2, 500, ""), (614.3, 200, ""), (588.2, 150, ""),
                  (650.7, 200, ""), (540.1, 100, "")],
        "basis": "Reentry color similar to discharge tube — red-orange dominant.",
        "source": "NIST Ne I",
    },
    "Na": {
        "lines": [(589.0, 500, "D2"), (589.6, 300, "D1"),
                  (818.3, 100, ""), (819.5, 100, "")],
        "basis": "Na D-line still strongest at reentry T. Sub-Neptune alkali "
                 "trace species give bright yellow streak.",
        "source": "NIST Na I; lava world atmospheric models",
    },
    "Mg": {
        "lines": [(285.2, 100, "Mg I UV (V≈0)"), (517.3, 500, "Mg b1"),
                  (518.4, 400, "Mg b2"), (516.7, 400, "Mg b3"),
                  (448.1, 100, "Mg II 4481")],
        "basis": "Mg b triplet 516-518nm strong at reentry T (meteor green). "
                 "MgII 448 contributes mild blue.",
        "source": "Meteor spectroscopy; NIST Mg I+II",
    },
    "Al": {
        "lines": [(396.2, 500, "Al I"), (394.4, 400, "Al I"),
                  (705.7, 200, "Al II")],
        "basis": "Al I doublet UV-violet + Al II red. Hot rocky meteoroid green-violet.",
        "source": "NIST Al I+II; meteor spectroscopy",
    },
    "Si": {
        "lines": [(390.6, 300, "Si I"), (288.2, 100, "Si I UV"),
                  (634.7, 200, "Si II"), (637.1, 200, "Si II")],
        "basis": "Si I UV-violet weak + Si II red enhances. Hot rocky vaporization.",
        "source": "NIST Si I+II",
    },
    "S": {
        "lines": [(469.4, 200, "SI"), (545.4, 300, "S2 bands"),
                  (605.3, 200, "S2"), (392.4, 100, "")],
        "basis": "S2 + SO bands give pale blue-green. Venus-class outgassing trace.",
        "source": "NIST S I; Venus airglow",
    },
    "K": {
        "lines": [(766.5, 500, "K I"), (769.9, 400, "K I"),
                  (404.4, 200, "K I"), (404.7, 100, "")],
        "basis": "K resonance still dominant at reentry T. Alkali violet-pink "
                 "with stronger IR contribution.",
        "source": "NIST K I",
    },
    "Ca": {
        "lines": [(393.4, 500, "Ca II H"), (396.8, 500, "Ca II K"),
                  (422.7, 300, "Ca I"), (854.2, 200, "Ca II IR"),
                  (866.2, 200, "Ca II IR")],
        "basis": "Ca II H&K UV-violet very strong at reentry T (these are the famous "
                 "Fraunhofer H&K lines in stellar spectra). Mixed with Ca I → red-violet.",
        "source": "NIST Ca I+II",
    },
    "Fe": {
        "lines": [(404.6, 300, "Fe I"), (438.4, 300, "Fe I"),
                  (495.8, 200, "Fe I"), (526.9, 300, "Fe I"),
                  (516.7, 300, "Fe I"), (438.3, 200, "Fe I"),
                  (501.2, 200, "Fe I")],
        "basis": "Fe at reentry T shows complex visible spectrum. Meteor-class "
                 "ablation gives a characteristic gold-orange perceived hue from "
                 "the visible-line continuum.",
        "source": "Meteor spectroscopy; NIST Fe I",
    },
    "Ar": {
        "lines": [(696.5, 300, "Ar I"), (706.7, 200, "Ar I"),
                  (738.4, 150, "Ar I"), (763.5, 250, "Ar I"),
                  (415.9, 100, "Ar I violet"), (419.8, 100, "Ar I violet")],
        "basis": "Ar I visible spectrum similar to discharge tube. Trace noble gas signature.",
        "source": "NIST Ar I",
    },
}


# ─────────────────────────────────────────────────────────────────────
# Aurora regime data
# ─────────────────────────────────────────────────────────────────────
# Low-density forbidden lines + electron-impact-induced transitions.
# Limited to documented atmospheric species. Polyatomics → not_emitter.

AURORA_DATA = {
    "O": {
        "lines": [(557.7, 1000, "OI green forbidden ¹S→¹D"),
                  (630.0, 400, "OI red forbidden ¹D→³P"),
                  (636.4, 200, "OI red")],
        "basis": "OI 557.7nm green is the iconic auroral emission "
                 "(1S→1D forbidden, τ≈0.7s, needs >100km altitude). "
                 "630.0nm red dominates at higher altitudes (>200km, "
                 "1D→3P forbidden, τ≈110s).",
        "source": "NIST O I; Earth auroral physics literature",
    },
    "N": {
        "lines": [(346.6, 100, "NI forbidden UV"),
                  (519.8, 200, "NI ²D→⁴S"),
                  (520.0, 200, "NI"),
                  (746.8, 300, "NI IR")],
        "basis": "Atomic N contributes weak green-yellow forbidden lines. "
                 "Most visible 'aurora green' is actually OI 558nm, not N.",
        "source": "NIST N I auroral",
    },
    "H": {
        "lines": [(656.3, 1000, "Hα Balmer"),
                  (486.1, 200, "Hβ Balmer"),
                  (434.0, 100, "Hγ Balmer")],
        "basis": "H Balmer α dominant. Proton aurora — incoming protons "
                 "charge-exchange to neutral H, then emit Balmer. Diffuse, "
                 "less intense than electron aurora.",
        "source": "NIST H I; proton aurora literature",
    },
    "He": {
        "lines": [(587.6, 500, "D3"), (388.9, 300, "He I UV-blue")],
        "basis": "Rare; observed in proton aurorae and very high-energy events.",
        "source": "Aurora spectroscopy lit",
    },
    "Mg": {
        "lines": [(285.2, 100, "Mg I UV"), (518.4, 300, "Mg b2"),
                  (516.7, 300, "Mg b3"), (517.3, 300, "Mg b1")],
        "basis": "Meteor-class aurora — Mg b triplet from incoming dust ablation "
                 "in the upper atmosphere. Distinctive bright green meteor color.",
        "source": "Meteor spectroscopy; Mg I NIST",
    },
}


# Polyatomic dissociation status — element keys don't have polyatomics,
# but if user adds an entry for a molecular species (which would go in
# molecular DB, not here), the aurora regime would be not_emitter for
# polyatomics. For now, no element-level polyatomic markers needed.


# ─────────────────────────────────────────────────────────────────────

def compute_hex(lines: list) -> str:
    pairs = [(wl, i) for (wl, i, _) in lines]
    return rgb_to_hex(mix_lines(pairs))


def build_regime(name: str, data: dict) -> dict:
    """Compose a regime block from REENTRY_DATA / AURORA_DATA entry."""
    lines = data["lines"]
    return {
        "status": "visible",
        "hex": compute_hex(lines),
        "hex_basis": "cie_computed",
        "emission_lines": [
            {"nm": float(wl), "intensity": float(i),
             **({"label": lbl} if lbl else {})}
            for (wl, i, lbl) in lines
        ],
        "basis": data["basis"],
        "source": data["source"],
    }


def main() -> int:
    with open(DB_PATH, encoding="utf-8") as f:
        db = yaml.safe_load(f)

    n_reentry = 0
    n_aurora = 0

    for sym, data in REENTRY_DATA.items():
        if sym not in db:
            print(f"  [WARN] symbol {sym} not in DB; skipping reentry", file=sys.stderr)
            continue
        db[sym]["regimes"]["reentry_plasma"] = build_regime("reentry_plasma", data)
        n_reentry += 1

    for sym, data in AURORA_DATA.items():
        if sym not in db:
            print(f"  [WARN] symbol {sym} not in DB; skipping aurora", file=sys.stderr)
            continue
        db[sym]["regimes"]["aurora"] = build_regime("aurora", data)
        n_aurora += 1

    # Preserve atomic-number ordering
    ordered = {sym: db[sym] for sym in sorted(db.keys(), key=lambda s: db[s]["atomic_number"])}

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
    print(f"populated reentry_plasma: {n_reentry} species")
    print(f"populated aurora:         {n_aurora} species")
    return 0


if __name__ == "__main__":
    sys.exit(main())
