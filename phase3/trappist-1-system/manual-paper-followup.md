# Manual paper follow-up — TRAPPIST-1 system Phase 3

These papers were surfaced by ADS but have **no arXiv preprint
available** at retrieval time (2026-05-21 to 2026-05-22). I cannot
auto-fetch them. They are listed here in the order most likely to
refine the existing Phase 3 syntheses.

If you can access any of these (Claude for Chrome, institutional
library, conference proceedings PDF), paste the abstract or full text
back into a Phase 3 session and the synthesis files can be updated.

## Tier A — likely to change cfg decisions

These papers either supersede current synthesis citations or fill
known gaps. **Highest priority for manual fetch.**

| Bibcode | Year | Planet | Title | Why it matters |
|---|---|---|---|---|
| 2026NatAs.tmp...88. | 2026 | b, c | The innermost planets in the TRAPPIST-1 system do not have thick atmospheres | Likely a Nature Astronomy publication consolidating Greene 2023 / Zieba 2023 / Ducrot 2025; may tighten atmosphere upper limits |
| 2026NatAs.tmp...65G | 2026 | b, c | No thick atmosphere around TRAPPIST-1 b and c from JWST thermal phase curves | Likely the published version of 2509.02128 (Ducrot 2025); confirm if there are revised constraints |
| 2024ESS.....510106L | 2024 | f | TRAPPIST-1 Atmospheric Reconnaissance with JWST: First Look at the Habitable-Zone Exoplanet TRAPPIST-1 f with NIRISS | **Only direct JWST observation of f**, currently cited from ADS abstract only. Full text could clarify atmosphere constraints. |
| 2024ESS.....562710L | 2024 | c | Potential Atmospheric Compositions of TRAPPIST-1 c constrained by JWST | Possibly a precursor / conference version of Lincowski 2023 (arXiv 2308.05899) — confirm consistency |
| 2025epsc.conf..605N | 2025 | b, c, e (?) | Predicted atmospheric evolutionary pathways for the TRAPPIST-1 planets | Could supply system-wide evolutionary framework |
| 2025EGUGA..2718054S | 2025 | b | Modelling surface mineral diversity of atmosphere-free rocky exoplanets | **Directly informs `surface_tint_rgb_hex_primary` for b** — mineralogy modeling for airless rocky exoplanets |
| 2024EPSC...17..649T | 2024 | b, c | Reflectance and Emission Modelling of Airless Exoplanets | **Informs surface colors / albedo for airless b and c** |
| 2024MNRAS.530L..13P | 2024 | g, h | Fundamentals for habitable scenarios for Earth-like planets in the TRAPPIST-1 system | Could refine the snowball/ocean choices for outer planets |
| 2018AJ....155..239J | 2018 | h | Dynamical Constraints on Nontransiting Planets Orbiting TRAPPIST-1 | Constrains additional resonance partners that could affect h's tidal evolution |

## Tier B — useful context

| Bibcode | Year | Planet | Title | Why it matters |
|---|---|---|---|---|
| 2024AGUFMP11E.3011L | 2024 | e | Coupled Atmospheric Chemistry, Radiation, and Dynamics of an Exoplanet (TRAPPIST-1 e) | Refinement of GCM input for e's atmosphere |
| 2024EPSC...17..168C | 2024 | e | Haze Optical Depth in Exoplanet Atmospheres Varies with Rotation Rate | Cloud / haze visibility modeling |
| 2024ESS.....562504V | 2024 | e | Who Run the World? (Flares): Ozone production in steam atmospheres during M-dwarf flares | O₃ visual tint refinement |
| 2024ESS.....562907W | 2024 | e | What If The Earth Orbited TRAPPIST-1 Instead of the Sun? | Pedagogical / context |
| 2024eas..conf..697C / 2024EGUGA..2611513C | 2024 | e, g | Impact of CO2 on water outgassing on rocky planets around TRAPPIST-1 | Atmosphere composition refinement for e/g |
| 2024ApJ...970L...4D | 2024 | h | Updated Spectral Characteristics for the Ultracool Dwarf TRAPPIST-1 | Could update Teff / spectral type used in visual styling |
| 2022AGUFM.P35C1897A | 2022 | h | Transition from XUV Driven Ion Escape to Hydrodynamic Escape | Atmospheric retention regime for h |
| 2020EPSC...14..355A | 2020 | c, g | Assessing the habitability of observed Super Earths | Context |
| 2018AGUFM.P44B..06M | 2018 | d, f | Insights into the atmospheres of the TRAPPIST-1 planets from the laboratory | Aerosol / chemistry lab work |
| 2025epsc.conf..580B | 2025 | b | High-Resolution Transmission Spectroscopy of Venus: A Proxy for Atmospheric Characterization | Methodology |
| 2025epsc.conf..178P | 2025 | d | TRAPPIST-1 d: A Case Study in Atmospheric Loss | Likely conference abstract of Piaulet-Ghorayeb 2025 (already covered via 2508.08416) |
| 2025EGUGA..27.6151S | 2025 | e | Is It Possible to Detect Airless Exomoons Through Thermal Phase Curves? | Methodology |

## Tier C — proceedings & catalogs (skip unless context needed)

These are mostly conference proceedings (BAAS, AAS, AGU, EAS, EGU,
EPSC) that summarize already-published work, plus VizieR data catalogs.
43 such papers exist across the 6 planets' bibliographies. Listed
exhaustively in `phase3/trappist-1-system/_manual-followup-source.json`.
Generally safe to skip; they cite the same primary references already
read.

## Fetching tips

1. **ADS bibcodes** like `2026NatAs.tmp...88.` → search at
   <https://ui.adsabs.harvard.edu/abs/2026NatAs.tmp...88./abstract>
   (replace dots if URL needs them).
2. **Nature Astronomy 2026 papers**: probably have arXiv preprints
   filed days-to-weeks later; try a re-fetch of bibliographies in
   2026-06+ to see if `2026NatAs.tmp...88.` and `2026NatAs.tmp...65G`
   now resolve.
3. **Conference papers (EPSC, EGU, AGU)**: usually have abstracts only;
   may not be worth chasing unless the title is highly specific to a
   cfg-relevant question.
4. **For Claude for Chrome**: navigate to the ADS abstract page, then
   "Open with Claude Code" → "Save abstract + any linked DOI text".
5. After paste, the workflow is: add the text to a new file under
   `docs/phase3/_papers/<bibcode>.md`, then re-read the synthesis and
   integrate any cfg-relevant numbers.

## Related

- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
