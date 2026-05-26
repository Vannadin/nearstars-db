# 분자 종 reentry/aurora 색상 DB 를 생성하는 스크립트 (db/refs/molecular_plasma_colors.yaml)
"""Build the molecular plasma color DB.

Diatomic + small polyatomic molecules dominate the visual signature of
reentry plasma and aurora in atmospheres where they're abundant.
Element DB captures atomic emission; this captures molecular bands.

Output: db/refs/molecular_plasma_colors.yaml

Schema per molecule:
    H2O:
      formula: H2O
      mass_amu: 18.02
      atoms: 3                         # 1 → mono, 2 → diatomic, 3+ → poly
      regimes:
        reentry_plasma:
          status: visible | not_emitter
          hex: "#rrggbb" | null
          hex_basis: cie_computed
          emission_bands:               # band centers + intensities
            - {nm: 656.3, intensity: 500, label: "Hα (dissociation product)"}
          basis: ...
          source: ...
        aurora:
          status: visible | not_emitter
          ...

For polyatomics that DON'T emit (CO2, NH3, CH4, H2O at aurora altitudes
photo-dissociate), status=not_emitter with `dissociation_products` field
listing the atomic species their dissociation feeds (those species
carry the actual emission in their element DB entries).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "db" / "refs" / "molecular_plasma_colors.yaml"

sys.path.insert(0, str(ROOT / "scripts" / "refs"))
from wavelength_to_rgb import mix_lines, rgb_to_hex


def compute_hex(lines):
    pairs = [(wl, i) for (wl, i, _) in lines]
    return rgb_to_hex(mix_lines(pairs))


# ─────────────────────────────────────────────────────────────────────
# Molecules data
# ─────────────────────────────────────────────────────────────────────

MOLECULES = {
    # ── Diatomic molecules — strong band emitters ────────────────────
    "N2": {
        "formula": "N2",
        "mass_amu": 28.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "canonical_hex": "#5060c0",   # Earth reentry blue-violet (observed)
                "lines": [(670.0, 500, "N2 1P (vibrational head)"),
                          (391.4, 600, "N2+ 1NG"),
                          (427.8, 400, "N2+ 1NG")],
                "basis": "N2 1P red + N2+ 1NG violet. Earth-reentry visual signature "
                         "is blue-violet — established by NASA reentry imaging. (Naive "
                         "CIE mix of NIST relative intensities gives yellow because "
                         "V(λ) heavily downweights violet at 391nm, but observed "
                         "absolute photon flux at 391nm is high enough to dominate.)",
                "source": "Air plasma optical spectra; NASA reentry imaging",
            },
            "aurora": {
                "canonical_hex": "#7070d0",   # Aurora N2 lower-border violet-blue (observed)
                "lines": [(670.0, 500, "N2 1P red lower border"),
                          (391.4, 800, "N2+ 1NG violet"),
                          (427.8, 500, "N2+ 1NG blue")],
                "basis": "Aurora — N2+ 391nm is the bright violet-blue band visible "
                         "at the lower altitude limit (~100km).",
                "source": "Earth aurora spectroscopy",
            },
        },
    },
    "N2+": {
        "formula": "N2+",
        "mass_amu": 28.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "canonical_hex": "#4060d0",
                "lines": [(391.4, 1000, "1NG (0,0)"),
                          (427.8, 600, "1NG (0,1)")],
                "basis": "Ionized N2+ — First Negative bands 391+427nm. Pure violet-blue.",
                "source": "Air plasma + auroral physics",
            },
            "aurora": {
                "canonical_hex": "#5060d8",
                "lines": [(391.4, 1000, "1NG (0,0)"),
                          (427.8, 600, "1NG (0,1)")],
                "basis": "N2+ 391nm violet is the bright lower-border auroral band.",
                "source": "Earth aurora spectroscopy",
            },
        },
    },
    "O2": {
        "formula": "O2",
        "mass_amu": 32.00,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "lines": [(762.0, 300, "Atmospheric A-band"),
                          (688.0, 200, "B-band"),
                          (628.0, 100, "γ-band")],
                "basis": "O2 itself contributes mild red bands in shock plasma. "
                         "Most visible emission from dissociation products (atomic O).",
                "source": "NIST O2 + reentry literature",
            },
            "aurora": {
                "status": "not_visible_to_humans",
                "basis": "O2 contributes mainly IR airglow at 864nm at aurora "
                         "altitudes. Visible signature comes from dissociation "
                         "product OI (see element DB).",
                "source": "Airglow spectroscopy",
            },
        },
    },
    "OH": {
        "formula": "OH",
        "mass_amu": 17.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "not_visible_to_humans",
                "basis": "OH A-X bands at 309/315nm are UV. Reentry plasma "
                         "perceptual contribution from OH is essentially nil.",
                "source": "NIST OH; H2O combustion spectra",
            },
            "aurora": {
                "status": "not_visible_to_humans",
                "basis": "OH Meinel bands at 700-880nm are near-IR airglow. "
                         "Sky cameras need IR sensors to capture them.",
                "source": "OH Meinel airglow literature",
            },
        },
    },
    "NO": {
        "formula": "NO",
        "mass_amu": 30.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "lines": [(237.0, 100, "NO γ-band UV (V≈0)"),
                          (440.0, 200, "NO β-band"),
                          (500.0, 200, "NO continuum (recombination)")],
                "basis": "NO from N+O recombination in shock layer. γ-band UV mostly "
                         "invisible; visible contribution faint blue-green from "
                         "broad continuum (Venus airglow analog).",
                "source": "Venus airglow studies; NIST NO",
            },
            "aurora": {
                "lines": [(500.0, 200, "NO recombination continuum"),
                          (440.0, 100, "")],
                "basis": "NO continuum from N+O recombination — pale blue-green. "
                         "Visible on Venus airglow.",
                "source": "Venus airglow",
            },
        },
    },
    "CO": {
        "formula": "CO",
        "mass_amu": 28.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "canonical_hex": "#50d098",
                "lines": [(520.0, 300, "CO Cameron a³Π-X¹Σ"),
                          (425.0, 200, "CO Ångström")],
                "basis": "CO Cameron bands green. Mars EDL camera footage shows this.",
                "source": "arXiv 2007.04869; NASA Mars EDL",
            },
            "aurora": {
                "canonical_hex": "#48c890",
                "lines": [(520.0, 400, "CO Cameron"),
                          (500.0, 300, "CO Cameron")],
                "basis": "CO Cameron green is the visible signature of Mars aurora.",
                "source": "Mars MAVEN aurora detection",
            },
        },
    },
    "CN": {
        "formula": "CN",
        "mass_amu": 26.02,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "canonical_hex": "#7080d0",   # CO2 reentry violet-blue (Mars EDL)
                "lines": [(388.3, 500, "CN violet B-X (0,0)"),
                          (387.1, 400, "CN violet (1,1)"),
                          (421.6, 300, "CN red")],
                "basis": "CN violet 388nm is the iconic violet-blue band of "
                         "CO2-atmosphere reentry plasma (Mars EDL signature).",
                "source": "arXiv 2007.04869; Mars EDL imaging",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "CN production requires N + C in vapor — possible in "
                         "tholin haze upper atmosphere (Titan), but emission "
                         "ratio in aurora-like conditions not well characterized.",
                "source": "Titan upper-atmosphere photochemistry studies",
            },
        },
    },
    "C2": {
        "formula": "C2",
        "mass_amu": 24.02,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "canonical_hex": "#5fc890",   # C2 Swan green-blue (Mars EDL + comet comas)
                "lines": [(516.5, 500, "C2 Swan d-a (0,0) green"),
                          (473.7, 400, "C2 Swan (1,2) blue-green")],
                "basis": "C2 Swan bands — bright green signature of carbon-rich "
                         "plasmas (Mars EDL + comet comas).",
                "source": "Comet coma + arXiv 2007.04869 CO2 plasma",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "C2 doesn't survive in low-density aurora environments; "
                         "any C is typically in CO or CN.",
                "source": "Upper atmosphere chemistry",
            },
        },
    },
    "H2": {
        "formula": "H2",
        "mass_amu": 2.02,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "lines": [(656.3, 800, "Hα (dissociation product)"),
                          (486.1, 200, "Hβ"),
                          (600.0, 300, "H2 Werner band visible")],
                "basis": "H2 mostly dissociates → atomic H Balmer dominates. "
                         "Pink-red plasma. Gas-giant reentry chemistry.",
                "source": "Brown dwarf aurora; H2 plasma physics",
            },
            "aurora": {
                "lines": [(656.3, 1000, "Hα (Lyman aurora secondary)"),
                          (486.1, 200, "Hβ")],
                "basis": "Jupiter/Saturn aurorae — dominantly UV (Lyman α 121nm + "
                         "H2 Werner/Lyman bands). Visible band shows weak Hα.",
                "source": "Jupiter Hubble aurora imaging",
            },
        },
    },
    "CH": {
        "formula": "CH",
        "mass_amu": 13.02,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "lines": [(431.3, 400, "CH A-X (0,0) blue"),
                          (387.1, 200, "CH B-X UV"),
                          (387.3, 200, "CH")],
                "basis": "CH 431nm blue from methane dissociation in shock layer. "
                         "Common in Titan / sub-Neptune reentry.",
                "source": "Hydrocarbon combustion; comet spectra",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "CH doesn't persist in low-density aurora; CH4 photolysis "
                         "products are mostly C2H, C2H2 (no strong visible emitter).",
                "source": "Titan photochemistry literature",
            },
        },
    },
    # ── Polyatomic molecules — generally NOT auroral emitters ────────
    "CO2": {
        "formula": "CO2",
        "mass_amu": 44.01,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "CO2 itself dissociates in shock layer. Visible plasma color "
                         "comes from products: CO Cameron green + C2 Swan + CN violet "
                         "+ atomic O. See CO, C2, CN, O entries.",
                "dissociation_products": ["CO", "C2", "CN", "O"],
                "source": "CO2 reentry chemistry; arXiv 2007.04869",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photo-dissociates above ~80 km. Emission goes to CO, O.",
                "dissociation_products": ["CO", "O"],
                "source": "Mars/Venus upper atmosphere photochemistry",
            },
        },
    },
    "H2O": {
        "formula": "H2O",
        "mass_amu": 18.02,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "H2O dissociates → atomic H (Balmer) + OH (Meinel UV). "
                         "Visible plasma is dominantly H Hα pink.",
                "dissociation_products": ["H", "OH"],
                "source": "Steam atmosphere reentry models",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photo-dissociates above ~80 km; emission from H Balmer + OH.",
                "dissociation_products": ["H", "OH"],
                "source": "Comet outgassing parallels",
            },
        },
    },
    "CH4": {
        "formula": "CH4",
        "mass_amu": 16.04,
        "atoms": 5,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "CH4 dissociates → CH (431nm blue) + C2 (Swan green) + Hα. "
                         "Titan reentry signature.",
                "dissociation_products": ["CH", "C2", "H"],
                "source": "Titan reentry; hydrocarbon combustion",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photo-dissociates; products mostly aliphatic radicals "
                         "without strong visible emission. Tholin chemistry forms haze.",
                "dissociation_products": ["CH", "C2H", "C2H2"],
                "source": "Titan upper-atmosphere photochemistry",
            },
        },
    },
    "NH3": {
        "formula": "NH3",
        "mass_amu": 17.03,
        "atoms": 4,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "NH3 dissociates → NH + H. Weak emission, mostly Hα + NH bands.",
                "dissociation_products": ["NH", "H", "N"],
                "source": "Ice-giant atmosphere chemistry",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photo-dissociates; products N + H carry emission.",
                "dissociation_products": ["N", "H"],
                "source": "Ice-giant photochemistry",
            },
        },
    },
    "SO2": {
        "formula": "SO2",
        "mass_amu": 64.06,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "lines": [(280.0, 100, "SO2 A-X UV (V≈0)"),
                          (340.0, 100, "SO2 UV"),
                          (470.0, 200, "SO continuum")],
                "basis": "SO2 dissociates to SO + O. Some weak visible continuum. "
                         "Venus / Io plume reentry territory.",
                "source": "Venus atmospheric chemistry; Io plume spectra",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photo-dissociates → SO + O. Io plasma torus has SO2+/S+/O+ "
                         "ion emission but that's a different regime.",
                "dissociation_products": ["SO", "O"],
                "source": "Io plasma torus studies",
            },
        },
    },

    # ── Tier 1: 2 new diatomic emitters ──────────────────────────────
    "SO": {
        "formula": "SO",
        "mass_amu": 48.06,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "canonical_hex": "#6c98a8",   # Venus airglow + Io plume pale blue-green
                "lines": [(470.0, 300, "SO A-X visible continuum"),
                          (250.0, 100, "SO A-X UV (V≈0)"),
                          (282.0, 100, "SO B-X UV")],
                "basis": "SO A 3Π - X 3Σ band system. Strong UV component + visible "
                         "continuum near 470nm gives pale blue-green appearance. "
                         "Co-emits with NO continuum in Venus airglow.",
                "source": "Venus airglow studies; Io plasma torus; NIST SO",
            },
            "aurora": {
                "canonical_hex": "#7aa8b8",
                "lines": [(470.0, 200, "SO A-X visible"),
                          (500.0, 150, "SO continuum")],
                "basis": "SO contributes to airglow + Io magnetosphere aurora. Pale blue-green continuum.",
                "source": "Io aurora observations; Venus night airglow",
            },
        },
    },
    "NH": {
        "formula": "NH",
        "mass_amu": 15.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "lines": [(336.0, 300, "NH A 3Π - X 3Σ (UV dominant)"),
                          (470.0, 80, "NH visible band (faint)"),
                          (630.0, 50, "NH (b 1Σ) faint")],
                "basis": "NH A 3Π - X 3Σ system. Dominant UV at 336nm; visible bands "
                         "weak but present. NH3 dissociation product in ice-giant reentry.",
                "source": "NIST NH; comet coma; ice-giant chemistry",
            },
            "aurora": {
                "lines": [(336.0, 400, "NH A-X UV"),
                          (470.0, 100, "NH visible faint")],
                "basis": "NH from NH3 photolysis in sub-Neptune / ice-giant upper atmosphere. "
                         "Mostly UV; faint visible blue.",
                "source": "Titan + ice-giant upper-atmosphere chemistry",
            },
        },
    },

    # ── Tier 1: 3 polyatomic precursors (not_emitter w/ dissociation) ──
    "H2S": {
        "formula": "H2S",
        "mass_amu": 34.08,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "H2S dissociates in shock layer → SH + H, then → S + H. "
                         "Visible plasma comes from SO continuum (if O present) + S atomic. "
                         "Volcanic outgassing reentry signature.",
                "dissociation_products": ["S", "SO", "H"],
                "source": "Venus + Io plume volcanic chemistry",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photo-dissociates in upper atmosphere → S + H. Sulfur "
                         "contributes to weak airglow if abundant.",
                "dissociation_products": ["S", "H"],
                "source": "Volcanic photochemistry; Io plume",
            },
        },
    },
    "O3": {
        "formula": "O3",
        "mass_amu": 48.00,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "O3 dissociates rapidly above ~600K → O2 + O. At reentry temps, "
                         "essentially zero O3 survives. Visible plasma from O atomic + "
                         "O2 bands. Chappuis-band blue color is absorption, not emission.",
                "dissociation_products": ["O2", "O"],
                "source": "Atmospheric photochemistry; Chappuis band literature",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "O3 photolysis above 80 km fuels OH Meinel airglow (O3 + hν → "
                         "O2 + O*; O* + H2O → 2 OH*). Indirect emitter via OH.",
                "dissociation_products": ["OH", "O", "O2"],
                "source": "OH Meinel airglow mechanism",
            },
        },
    },
    "HCN": {
        "formula": "HCN",
        "mass_amu": 27.03,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "HCN dissociates → CN + H in shock layer. Visible signature "
                         "is CN violet 388nm + Hα. Tholin haze + sub-Neptune reentry.",
                "dissociation_products": ["CN", "H"],
                "source": "Titan tholin chemistry; comet HCN observations",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photodissociates in upper atmosphere → CN + H. CN violet "
                         "from this process possible in Titan-class aurorae but observation limited.",
                "dissociation_products": ["CN", "H"],
                "source": "Titan upper-atmosphere photochemistry",
            },
        },
    },

    # ── Tier 2: stubs + refined entries ──────────────────────────────
    # Status decided after spectroscopic review. Where the literature
    # supports it, entries have been upgraded out of no_data (FeO
    # reentry → visible, NH2 aurora → visible). Where the molecule's
    # role is thermal opacity rather than plasma emission (TiO, VO),
    # no_data is retained with a note about the future thermal_emission
    # regime. Where the molecule dissociates rather than emits in
    # visible (HCl, HF), status is not_emitter with explicit dissociation
    # products pointing at the atomic species in element DB.

    "TiO": {
        "formula": "TiO",
        "mass_amu": 63.87,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "Titanium monoxide is primarily a *thermal opacity* signature, "
                         "not a plasma emitter. γ-system (A 3Φ - X 3Δ) red bands at "
                         "670/705/770nm dominate M-dwarf atmospheric opacity and lava-"
                         "world surface glow. α-system (B 3Π - X 3Δ) at 487nm contributes "
                         "blue-green minority. At reentry plasma temps (8000-15000 K) TiO "
                         "dissociates to Ti + O — direct emission negligible.",
                "source": "NIST TiO; M-dwarf opacity literature",
                "upgrade_when": "Future `thermal_emission` regime is added (covers lava-world surface + cool-dwarf atmosphere thermal radiation, not shock-heated plasma)",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Not applicable at typical aurora altitudes — TiO requires "
                         "high-T atmosphere where it's a thermal opacity signature, not "
                         "an electron-impact emitter.",
                "source": "—",
                "upgrade_when": "Hot-Jupiter Phase 3 with very high-T upper atmosphere",
            },
        },
    },
    "SiO": {
        "formula": "SiO",
        "mass_amu": 44.08,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "not_visible_to_humans",
                "basis": "Silicon monoxide emission is dominated by IR rotational-"
                         "vibrational bands (fundamental at 8μm + overtones). Electronic "
                         "transitions UV 220-280nm. Visible γ-system bands at 433/471nm "
                         "exist but are perceptually negligible vs IR thermal continuum. "
                         "Lava-world silicate vapor candidate.",
                "source": "NIST SiO; lava-planet atmosphere models",
                "upgrade_when": "Phase 3 lava world with explicit visible-band SiO emission scenario",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Not relevant at aurora altitudes (SiO requires high surface T).",
                "source": "—",
                "upgrade_when": "—",
            },
        },
    },
    "FeO": {
        "formula": "FeO",
        "mass_amu": 71.84,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "canonical_hex": "#ff6030",
                "lines": [(580.0, 400, "FeO B-X (0,0) orange"),
                          (597.0, 350, "FeO B-X (0,1)"),
                          (612.0, 300, "FeO B-X (0,2)"),
                          (560.0, 200, "FeO B-X high-v")],
                "basis": "Iron monoxide B-X orange band system 580-612nm is the iconic "
                         "afterglow color of meteor ablation — the orange streak you see "
                         "behind a bright meteor is largely FeO chemiluminescence "
                         "(Fe + O3 → FeO* + O2; FeO* → FeO + hν). Same chemistry in "
                         "meteor-class reentry of rocky bodies.",
                "source": "Meteor spectroscopy (Jenniskens 2007); NIST FeO B-X",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Meteor aurora signature is mostly atomic Fe (element DB) plus "
                         "the FeO orange afterglow in the wake. Whether 'aurora' "
                         "(magnetospheric) FeO emission exists for any natural body "
                         "is not well documented.",
                "source": "Meteor aurora literature",
                "upgrade_when": "—",
            },
        },
    },
    "MgO": {
        "formula": "MgO",
        "mass_amu": 40.30,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "MgO B 1Σ - X 1Σ green band system near 500nm exists, but in "
                         "plasma MgO dissociates rapidly and the visible signature is "
                         "dominated by atomic Mg b triplet (516.7/517.3/518.4nm — see "
                         "element DB Mg entry). MgO direct emission contribution to "
                         "perceived color is negligible vs atomic Mg.",
                "dissociation_products": ["Mg", "O"],
                "source": "NIST MgO; meteor spectroscopy",
                "upgrade_when": "Phase 3 lava-world scenario where MgO molecular band is explicitly modeled vs atomic Mg",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Atomic Mg b triplet dominates in low-density meteor aurora.",
                "dissociation_products": ["Mg", "O"],
                "source": "Meteor aurora literature",
                "upgrade_when": "—",
            },
        },
    },
    "VO": {
        "formula": "VO",
        "mass_amu": 66.94,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "Vanadium monoxide γ-system 570-580nm + α-system 786-854nm "
                         "(Wing-Ford band) is a diagnostic feature in late M-dwarf and "
                         "brown-dwarf atmospheric opacity. Same caveat as TiO: it's a "
                         "thermal-opacity signature, not a shock-plasma emitter. At "
                         "reentry temps dissociates to V + O.",
                "source": "NIST VO; late-M/brown-dwarf atmosphere literature (Allard et al.)",
                "upgrade_when": "Future `thermal_emission` regime, OR a NearStars planet around an L-dwarf",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Not applicable.",
                "source": "—",
                "upgrade_when": "—",
            },
        },
    },
    "HCl": {
        "formula": "HCl",
        "mass_amu": 36.46,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "HCl intrinsic emission is dominated by IR vibrational-"
                         "rotational fundamentals (~3.4μm) + UV electronic transitions "
                         "(170-220nm V→0). At plasma temps HCl dissociates rapidly to "
                         "H + Cl. Visible signature inherits from atomic H Balmer + "
                         "atomic Cl I (754nm + visible bands; see element DB).",
                "dissociation_products": ["H", "Cl"],
                "source": "NIST HCl; Venus atmospheric chemistry",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photodissociates above ~80km → H + Cl. Visible contribution "
                         "via atomic Cl (faint visible) + Hα.",
                "dissociation_products": ["H", "Cl"],
                "source": "Atmospheric photochemistry",
            },
        },
    },
    "HF": {
        "formula": "HF",
        "mass_amu": 20.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "HF intrinsic emission is dominantly IR (3μm vibrational) + UV "
                         "electronic. No significant visible band. At plasma temps "
                         "dissociates → H + F. F atomic emission also mostly UV/IR — "
                         "essentially invisible in this regime.",
                "dissociation_products": ["H", "F"],
                "source": "NIST HF; comet HF observations",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photodissociates; products invisible. HF rarely seen in "
                         "non-cometary aurora contexts.",
                "dissociation_products": ["H", "F"],
                "source": "Comet HF literature",
            },
        },
    },
    "C2H2": {
        "formula": "C2H2",
        "mass_amu": 26.04,
        "atoms": 4,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "Acetylene undergoes stepwise plasma dissociation: "
                         "C2H2 + e⁻ → C2H + H, C2H → C2 + H, 2C2H → C2 + C2H2. "
                         "Visible signature is the sum of C2 Swan (516/473nm green) + "
                         "CH (431nm blue) + atomic Hα. Titan tholin precursor + "
                         "Jupiter auroral hydrocarbon chemistry.",
                "dissociation_products": ["C2", "CH", "H"],
                "source": "Titan + sub-Neptune hydrocarbon photochemistry; Jupiter auroral H2/C chemistry",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photolyzes above ~80km in tholin chemistry. Products: "
                         "C2H, C2, CH, H — direct emission via C2 Swan + Hα in "
                         "Jovian-class aurora.",
                "dissociation_products": ["C2", "CH", "H"],
                "source": "Titan upper-atmosphere photochemistry; Jupiter Hubble observations",
            },
        },
    },
    "NH2": {
        "formula": "NH2",
        "mass_amu": 16.02,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "Amidogen — NH3 photolysis intermediate. At reentry plasma "
                         "temperatures NH2 dissociates rapidly to NH + H. Visible "
                         "signature inherits from NH bands (336nm UV + faint visible) "
                         "+ atomic Hα.",
                "dissociation_products": ["NH", "H"],
                "source": "NIST NH2; ice-giant chemistry",
            },
            "aurora": {
                "canonical_hex": "#e87850",
                "lines": [(597.6, 300, "NH2 α-band A-X (0,9,0)"),
                          (610.6, 350, "NH2 α-band (0,8,0)"),
                          (630.6, 400, "NH2 α-band (0,7,0)"),
                          (653.0, 350, "NH2 α-band (0,6,0)"),
                          (666.5, 300, "NH2 α-band (0,5,0)")],
                "basis": "NH2 A 2A1 - X 2B1 α-band system 597-666nm is famously observed "
                         "in comet comae (Halley's comet bright red α-band). In "
                         "ammonia-rich sub-Neptune / ice-giant upper atmospheres at low "
                         "density, NH2 from NH3 photolysis can persist long enough to "
                         "emit. Warm red-orange visual signature.",
                "source": "Comet NH2 spectroscopy (Halley 1986); NIST NH2",
            },
        },
    },
    "H2SO4": {
        "formula": "H2SO4",
        "mass_amu": 98.08,
        "atoms": 7,
        "regimes": {
            "reentry_plasma": {
                "status": "not_emitter",
                "basis": "Sulfuric acid undergoes thermal + photolytic cascade: "
                         "H2SO4 → SO3 + H2O → SO2 + ½ O2 → SO + O → S + O. Visible "
                         "signature comes from the cascade products: SO band (pale "
                         "blue-green) + S atomic. Venus cloud-droplet chemistry; "
                         "no direct H2SO4 emission.",
                "dissociation_products": ["SO3", "SO2", "SO", "S", "H2O"],
                "source": "Venus cloud + photochemistry literature",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photolyzes; products feed SO continuum + atomic S faint "
                         "emission at Venus mesosphere altitudes.",
                "dissociation_products": ["SO", "S", "OH"],
                "source": "Venus upper-atmosphere photochemistry",
            },
        },
    },
}


def build_regime(name: str, data: dict) -> dict:
    if data.get("status") in ("not_emitter", "not_visible_to_humans", "no_data"):
        result = {
            "status": data["status"],
            "hex": None,
            "basis": data["basis"],
            "source": data["source"],
        }
        if "dissociation_products" in data:
            result["dissociation_products"] = data["dissociation_products"]
        if "upgrade_when" in data:
            result["upgrade_when"] = data["upgrade_when"]
        return result

    # If `canonical_hex` is provided, use it (well-documented reentry/
    # aurora signature whose visual color is established by observation
    # rather than naive CIE mix of band intensities — molecular plasma
    # color depends on absolute photon flux that NIST relative-intensity
    # values don't capture).
    if "canonical_hex" in data:
        return {
            "status": "visible",
            "hex": data["canonical_hex"],
            "hex_basis": "canonical_descriptor",
            "emission_bands": [
                {"nm": float(wl), "intensity": float(i),
                 **({"label": lbl} if lbl else {})}
                for (wl, i, lbl) in data.get("lines", [])
            ],
            "basis": data["basis"],
            "source": data["source"],
        }

    lines = data["lines"]
    return {
        "status": "visible",
        "hex": compute_hex(lines),
        "hex_basis": "cie_computed",
        "emission_bands": [
            {"nm": float(wl), "intensity": float(i),
             **({"label": lbl} if lbl else {})}
            for (wl, i, lbl) in lines
        ],
        "basis": data["basis"],
        "source": data["source"],
    }


def main() -> int:
    db = {}
    for formula, m in MOLECULES.items():
        entry = {
            "formula": m["formula"],
            "mass_amu": m["mass_amu"],
            "atoms": m["atoms"],
            "regimes": {},
        }
        for regime_name, regime_data in m["regimes"].items():
            entry["regimes"][regime_name] = build_regime(regime_name, regime_data)
        db[formula] = entry

    header = """\
# Molecular plasma colors — reentry + aurora regimes.
#
# Companion DB to db/refs/element_plasma_colors.yaml. Captures the
# molecular-band emission that dominates the visible signature of
# reentry plasma (8000–15000 K shock layer) and aurora (low-density
# upper atmosphere forbidden + allowed transitions) for atmospherically-
# abundant species.
#
# Schema per molecule:
#   formula:   string (chemical formula)
#   mass_amu:  molecular mass (atomic mass units)
#   atoms:     number of atoms (1=mono, 2=diatomic, 3+=polyatomic)
#   regimes:
#     reentry_plasma: { status, hex, emission_bands, basis, source }
#     aurora:         { status, hex, emission_bands, basis, source }
#
# For polyatomic molecules at aurora altitudes (CO2, H2O, CH4, NH3, SO2):
# status=not_emitter with `dissociation_products` listing the atomic
# species that carry emission (look those up in element DB).

"""

    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    body = yaml.dump(
        db,
        Dumper=NoAliasDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000,
    )
    DB_PATH.write_text(header + body, encoding="utf-8")

    n_total = len(db)
    n_diatomic = sum(1 for m in MOLECULES.values() if m["atoms"] == 2)
    n_polyatomic = sum(1 for m in MOLECULES.values() if m["atoms"] >= 3)
    print(f"wrote {DB_PATH.relative_to(ROOT)}")
    print(f"  total molecules:   {n_total}")
    print(f"    diatomic:        {n_diatomic}")
    print(f"    polyatomic:      {n_polyatomic}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
