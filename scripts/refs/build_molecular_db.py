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

    # ── Tier 2: stubs (no_data; upgrade when Phase 3 encounters) ─────
    "TiO": {
        "formula": "TiO",
        "mass_amu": 63.87,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "Lava-world rock vapor + late M-dwarf atmosphere candidate. "
                         "Complex γ/γ' band system in red/IR; visible-band emission "
                         "not well characterized for our plasma temperature regime.",
                "source": "Late M-dwarf atmospheric models; meteor spectroscopy",
                "upgrade_when": "Phase 3 lava world synthesis cites TiO emission, OR M-dwarf surface mineral vapor analysis",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Not applicable in normal aurora altitudes; TiO would only appear "
                         "in extreme hot-jupiter upper atmospheres.",
                "source": "—",
                "upgrade_when": "Hot Jupiter Phase 3 synthesis",
            },
        },
    },
    "SiO": {
        "formula": "SiO",
        "mass_amu": 44.08,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "Lava-world silicate vapor. Strongest emission IR (8μm); "
                         "visible band emission near-UV (220nm) below human range. "
                         "Likely contributes via continuum.",
                "source": "Lava planet atmosphere models",
                "upgrade_when": "Phase 3 lava world synthesis with silicate vapor",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Not applicable at standard aurora altitudes.",
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
                "status": "no_data",
                "basis": "Iron oxide vapor in meteor + lava-world atmospheres. "
                         "Orange band system 580-620nm — but emission strength in "
                         "shock-heated plasma not curated.",
                "source": "Meteor spectroscopy",
                "upgrade_when": "Phase 3 cites FeO band; meteor-class entry effects",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Meteor-class aurora chemistry; mostly Fe I atomic.",
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
                "basis": "Magnesium oxide rock vapor. Green band system 500nm — but "
                         "emission largely overshadowed by atomic Mg b triplet "
                         "(see element DB Mg entry).",
                "source": "Meteor + lava chemistry",
                "upgrade_when": "Phase 3 specifies MgO band over atomic Mg",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Atomic Mg dominates over MgO in low-density aurora.",
                "source": "—",
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
                "basis": "Vanadium oxide. Cool-dwarf atmospheric opacity signature; "
                         "complex band system mostly in red/IR. Emission characteristics "
                         "in plasma not characterized.",
                "source": "Late M-dwarf + brown dwarf atmospheres",
                "upgrade_when": "Late-M-dwarf planet Phase 3 with surface vapor",
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
                "status": "no_data",
                "basis": "Hydrogen chloride trace. UV-dominant emission; visible "
                         "contribution faint. Venus + volcanic outgassing context.",
                "source": "Venus atmospheric chemistry",
                "upgrade_when": "Phase 3 Venus-class with HCl trace",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Photodissociates → H + Cl. Cl atomic emission cataloged in element DB.",
                "source": "—",
                "upgrade_when": "—",
            },
        },
    },
    "HF": {
        "formula": "HF",
        "mass_amu": 20.01,
        "atoms": 2,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "Hydrogen fluoride trace. Emission mostly IR rotational/vibrational. "
                         "Volcanic / cometary outgassing context.",
                "source": "Comet HF observations",
                "upgrade_when": "Phase 3 cometary outgassing scenario",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Photodissociates; products mostly invisible (Cl F UV).",
                "source": "—",
                "upgrade_when": "—",
            },
        },
    },
    "C2H2": {
        "formula": "C2H2",
        "mass_amu": 26.04,
        "atoms": 4,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "Acetylene — Titan tholin precursor + Jupiter aurora chemistry. "
                         "Dissociates to CH + CH or C2 + H2 + H. Reentry contribution "
                         "primarily via C2 Swan + CH bands (see C2, CH entries).",
                "dissociation_products": ["C2", "CH", "H"],
                "source": "Titan + sub-Neptune hydrocarbon photochemistry",
                "upgrade_when": "Phase 3 Titan-class tholin haze synthesis",
            },
            "aurora": {
                "status": "no_data",
                "basis": "Tholin photochemistry intermediate; not a direct emitter.",
                "dissociation_products": ["C2", "CH", "H"],
                "source": "—",
                "upgrade_when": "—",
            },
        },
    },
    "NH2": {
        "formula": "NH2",
        "mass_amu": 16.02,
        "atoms": 3,
        "regimes": {
            "reentry_plasma": {
                "status": "no_data",
                "basis": "Amidogen — NH3 photolysis intermediate. Visible band system "
                         "around 570-690nm (NH2 α-bands). Not characterized for our "
                         "plasma regime.",
                "source": "NIST NH2; comet spectra",
                "upgrade_when": "Phase 3 ammonia-rich atmosphere photochemistry",
            },
            "aurora": {
                "status": "no_data",
                "basis": "NH2 α-bands visible in comet comae; sub-Neptune aurora possible.",
                "source": "Comet NH2 imaging",
                "upgrade_when": "Sub-Neptune aurora Phase 3",
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
                "basis": "Sulfuric acid — Venus cloud chemistry. Dissociates → "
                         "SO3 + H2O → SO2 + O + ... Cascades to SO + S emission.",
                "dissociation_products": ["SO3", "SO2", "SO", "H2O", "H"],
                "source": "Venus cloud chemistry",
            },
            "aurora": {
                "status": "not_emitter",
                "basis": "Photolyzes; products feed SO + atomic S emission.",
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
