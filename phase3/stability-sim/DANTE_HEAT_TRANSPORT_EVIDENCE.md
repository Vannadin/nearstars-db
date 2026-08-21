<!-- Dante 크기 결정을 위한 표면 열수송 근거 모음 (ADS 검증, 2026-08-21). tidal-heating-methodology.md §6 확장분의 원재료 -->
# Surface heat transport evidence — for `tidal-heating-methodology.md` §6

Raw material for the §6 extension (the owner chose to fold this into the existing
tidal-heating doc rather than create a new one: generation and exit are one package).
Gathered by four ADS-disciplined research agents plus main-thread verification,
2026-08-21. **Every number below is pinned; do not re-research.**

## The law: heat leaves a high-flux body by advection, not conduction

- **Spencer, Katz & Hewitt 2020** ([arXiv:2003.08287](https://arxiv.org/abs/2003.08287),
  cached) — the governing surface energy balance. Eq. 33:
  `q_s = Ψ / [4πR²(ρL + ρc(T_m − T_s))]` gives the resurfacing rate from the
  dissipation rate; conduction is dropped because it is negligible. Reference
  solution: **99.5 % of surface heat transport is volcanic**, elastic thickness
  80 km, eruption rate 1.1 cm/yr, Io resurfacing 1.25 cm/yr. Eqs. 34–35 split
  erupted vs intruded: **80 % of Io's magma is emplaced in the crust, not erupted**.
  Table 1: ρ=3000, L=4e5 J/kg, c=1200 J/kg/K, T_m=1500 K, T_s=150 K, Ψ=1e14 W.
  The paper explicitly offers eq. 10 for other bodies: *"provides a means of
  estimating eruption rates for other tidally heated lava-worlds, utilising their
  tidal heating rate, size, and surface temperature"* — including TRAPPIST-1.
- **Kankanamge & Moore 2019** ([2019JGRE..124..114K](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K),
  doi 10.1029/2018JE005800) — quantitative parameterization of heat-pipe transport:
  melt-flux heat flux, mantle temperature, lid-base temperature, **lid thickness**,
  conductive flux. Validated <15 % against numerical simulation. No arXiv (bibcode/DOI).
  Notes Earth itself was in heat-pipe mode for its first billion-plus years.
- **O'Reilly & Davies 1981** ([1981GeoRL...8..313O](https://ui.adsabs.harvard.edu/abs/1981GeoRL...8..313O))
  — title is *"…a mechanism allowing a **thick** lithosphere"* (an earlier draft of
  this investigation had it as "thin"; the paper argues the opposite). Conduction-only
  would need a ~5 km lithosphere; advection permits a thick one.
- **Moore 2003** ([2003JGRE..108.5096M](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5096M))
  — solid-state convection *"falls an order of magnitude short"* of Io's observed
  flux, so melt segregation must dominate. **Moore & Webb 2017**
  ([2017E&PSL.474...13M](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.474...13M)):
  heat piping *"produces a thick, cold, and strong lithosphere"* despite high flux.
- **Reese, Solomatov & Moresi 1998** ([1998JGR...10313643R](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R))
  — stagnant-lid conduction can remove only **10–20 mW/m² (Venus), 15–30 (Mars)**
  before widespread melting. The citable basis for "the lid is not an exit".

## The three-mode ladder (the regime section)

| Mode | Anchor body | Surface flux |
|---|---|---|
| Plate tectonics (the plate carries the heat) | Earth **92.1 mW/m²** (47±2 TW, [2010SolE....1....5D](https://ui.adsabs.harvard.edu/abs/2010SolE....1....5D), 38,347 measurements) | ~0.09 W/m² |
| Stagnant lid (conduction only) | Venus / Mars | ceiling 10–30 mW/m² (Reese 1998) |
| Heat pipe (melt migration) | Io, early Earth, Dante | ≥ ~2.5 W/m² |

Io: mean flux **>~2.5 W/m²** ([1994JGR....9917095V](https://ui.adsabs.harvard.edu/abs/1994JGR....9917095V));
total thermal emission **≈106 TW**, volcanic edifices ≈56 TW
([arXiv:2310.12382](https://arxiv.org/abs/2310.12382), cached). Lithosphere ≥12 km
(mountain volume, [2003JGRE..108.5093J](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5093J)),
≥30 km (mountain distribution, [1998Icar..135..146C](https://ui.adsabs.harvard.edu/abs/1998Icar..135..146C)),
35–80 km in models — which passes only **3–7 % of Io's flux** by conduction.

## Plains sit at radiative equilibrium; the heat exits through discrete centres

- Io's background plains are **110–130 K, purely insolation-driven**: a frost model
  with Bond albedo 0.56 and thermal inertia 250 MKS fits 22 years of data
  ([arXiv:2405.19253](https://arxiv.org/abs/2405.19253), cached; equatorial frost
  106–116 K). Between hot spots the endogenic flux is **<1 W/m²**
  ([2004Icar..169..127R](https://ui.adsabs.harvard.edu/abs/2004Icar..169..127R)).
- Active volcanoes occupy **≈2 %** of Io's surface ([arXiv:2310.12382](https://arxiv.org/abs/2310.12382));
  **50 % of the heat flow comes from 1.2 % of the surface**
  ([2012Icar..219..701V](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V));
  patera floors are 2.5 % of the surface but host 64 % of detected hot spots
  ([2011Icar..214...91W](https://ui.adsabs.harvard.edu/abs/2011Icar..214...91W)).
- Henning, O'Connell & Sasselov 2009 ([arXiv:0912.1907](https://arxiv.org/abs/0912.1907), cached):
  tides alone are unlikely to open a *surface* magma ocean (*"half a million TW or
  more"* ≈ 980 W/m² on 1 R⊕), and *"thin-layer global resurfacing as on Io is
  unlikely for viscous lavas. This supports the notion of searching for small
  radiantly cooled hotspots on supertidal exoplanets."* — the literature itself
  predicts discrete lakes, not a global lava world.

## THE key constraint: two denominators, and the measured capacity of a lava lake

**Do not mix these.** Dividing a patera's power by its *geologic* area gives a
crust-dominated ~300 K number; dividing by the *fitted* equivalent-blackbody area
gives the crust-corrected proxy at 600–940 K.

| Object | Area | Areal flux | T_eff | Note |
|---|---|---|---|---|
| Loki Patera, geologic floor | 21,500 km² | **446–465 W/m²** | 298–301 K | Corroborated by JIRAM crust brightness 270–355 K ([arXiv:2410.10686](https://arxiv.org/abs/2410.10686), cached; area [2017Natur.545..199D](https://ui.adsabs.harvard.edu/abs/2017Natur.545..199D); power [2012Icar..219..701V](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V) 9.6e12 W) |
| Pele, fitted area | 6.5 km² | 44.3 kW/m² | 940 K | [2016Icar..264..198D](https://ui.adsabs.harvard.edu/abs/2016Icar..264..198D) |
| Nyamuragira 2014 (Earth) | 900 m² | **111 kW/m²** | 1,199 K | observed MAXIMUM; [2023FrEaS..1140199C](https://ui.adsabs.harvard.edu/abs/2023FrEaS..1140199C) Table 1 |
| Kilauea 2008 / Ambrym 2015 | 300 / 4,000 m² | 100 kW/m² | 1,167 K | same table |
| Erta Ale (FLIR) | ~1,000 m² | 45–76 kW/m² | 944–1,076 K | [2008GGG.....912008S](https://ui.adsabs.harvard.edu/abs/2008GGG.....912008S) |
| Nyiragongo 2017 | 50,000 m² | 24 kW/m² | 817 K | large ⇒ crusted |
| Kilauea 2015 | 30,000 m² | 23.3 kW/m² | 811 K | large ⇒ crusted |
| Erebus Ray Lake | 1,400 m² (lidar 535–1,709 m², [2015JVGR..295...43J](https://ui.adsabs.harvard.edu/abs/2015JVGR..295...43J)) | 21–25 kW/m² | 784–815 K | [2008JVGR..177..695C](https://ui.adsabs.harvard.edu/abs/2008JVGR..177..695C) |
| Kupaianaha stage 1 / 3 | sub-m² footprints | 22 / 4.9 kW/m² | 789 / 542 K | [1993JGR....98.6461F](https://ui.adsabs.harvard.edu/abs/1993JGR....98.6461F) |

- **Bare-melt ceiling**: σT_erupt⁴. Io eruption temperature was revised **1600 °C →
  ~1340 °C = 1613 K** ([2007Icar..192..491K](https://ui.adsabs.harvard.edu/abs/2007Icar..192..491K))
  → **384 kW/m²**. No lake reaches it: observed max 111 kW/m² is **59 %**.
- **Crust-free fraction**: 10⁻⁵ (quiescent, thick crust) to ~0.3 (vigorous). Organized
  lakes are *">80 % covered by a cooling skin"*; chaotic lakes are *"mostly crust-free
  and incandescent"* (Campion & Coppola 2023, citing [2019JVGR..381...16L](https://ui.adsabs.harvard.edu/abs/2019JVGR..381...16L)).
  Erta Ale often >90 % crust vs Marum ≤30 % ([2016JVGR..322..105R](https://ui.adsabs.harvard.edu/abs/2016JVGR..322..105R)).
- **Bigger lakes are MORE crusted** (see table). But that is supply-limited, not a
  capacity ceiling: surface speed correlates with gas flux / lake area
  ([2019JVGR..381...16L](https://ui.adsabs.harvard.edu/abs/2019JVGR..381...16L)), and
  crust lifetime falls with transit velocity ([2005JVGR..142..207H](https://ui.adsabs.harvard.edu/abs/2005JVGR..142..207H)).
  **So the test for a synthetic body is whether the REQUIRED areal flux (F_tidal / lake
  fraction) falls inside the measured capacity band, ≲111 kW/m².**
- **Published super-Io envelope**: 1–3 orders of magnitude above Io = **25–2,500 W/m²**,
  with the sustainable branch being *heat piping through a thick cold lid*, not a global
  melt ([2021PSJ.....2..119R](https://ui.adsabs.harvard.edu/abs/2021PSJ.....2..119R);
  adopted by [arXiv:2305.03410](https://arxiv.org/abs/2305.03410)). Magma ocean only
  above melt fraction 0.45 (disputed: 0.30 / 0.45 / 0.50 — see uncertainties).

## Uncertainties that must travel with any quoted number

1. **Emissivity is disputed** — 0.74 measured in the field at Erta Ale
   ([2002BVol...64..472B](https://ui.adsabs.harvard.edu/abs/2002BVol...64..472B)) vs
   0.95 assumed by Campion & Coppola. Flux scales with ε: **±28 %**.
2. **Erta Ale radiant output spans 3×** by method (5–30 vs 45–76 vs 100–400 MW):
   radiative-only vs total surface heat. Always state which.
3. **Campion & Coppola areas are photo estimates**; their fluxes are order-of-magnitude.
4. **~41–46 % of Io's heat flow is from unidentified sources**
   ([2012Icar..219..701V](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V),
   [2015Icar..245..379V](https://ui.adsabs.harvard.edu/abs/2015Icar..245..379V)).
5. **No published W/m² boundary** for stagnant-lid → heat-pipe → magma-ocean; the
   criterion is melt fraction and any flux boundary is a conversion, not a citation.
6. **Critical melt fraction disputed**: 0.30 / 0.45 / 0.50.
7. **Fitted single-blackbody temperatures are not physical temperatures**
   ([arXiv:1906.05426](https://arxiv.org/abs/1906.05426), cached).
8. Pre-arXiv/paywalled and therefore verified by bibcode + ADS abstract only:
   Kankanamge & Moore 2019, Moore 2001/2003, Moore & Webb 2017, Reese 1998,
   Veeder 1994/2012/2015, Matson 2001/2006, Davies 1996/2003, Harris 1999/2005/2008,
   Lev 2019, Campion's underlying sources. Harris 1999, Harris 2008 and Lev 2019 are
   the three whose full text would most improve the crust-fraction scaling — ask the
   owner for PDF access if §6 needs them at body-text level.

## Applied to Dante (the decision this evidence served)

Density held at 2,620 kg/m³; total output ∝ R⁵, surface flux ∝ R³, both anchored on
the shipped 900 km / 1,200× Io / 11,500 W/m².

| R | mass | output | flux | 5 %-lake required areal flux | verdict |
|---|---|---|---|---|---|
| 900 km (shipped) | 8.0e21 | 1,200× Io | 11,500 W/m² | 230 kW/m² | **2.1× the observed max — impossible** |
| 714 km | 3.99e21 | 377× | 5,742 | 114.8 kW/m² | at the record max |
| **521 km (chosen)** | **1.552e21** | **78×** | **2,231** | **44.6 kW/m²** | **Erta Ale class — inside the band** |
| 450 km | 1.0e21 | 38× | 1,438 | 28.8 kW/m² | Erebus class |

521 km also sits inside the published super-Io envelope (2,231 < 2,500 W/m²; the
envelope caps radius at 541 km), gives an area-averaged 452 K, and keeps the plains at
starlight equilibrium 223 K where elemental sulfur is stable and SO₂ frost is not
(frost needs ≤120 K, [1988Icar...75..450M](https://ui.adsabs.harvard.edu/abs/1988Icar...75..450M);
sulfur vacuum-boils by ~500 K).

**Dynamics: 4/4 with no moon lost** (leapfrog 1e5 yr, four initial phases, with Hades
at i 5° / e 0.01), against 0/5 for the shipped configuration and 85 % for the Hades-only
combo. Hades e_rms 0.033–0.046 and Dante e_rms 0.017–0.022 both bracket the board's
existing 0.0385 / 0.0186, so the tidal-heating rows move because of SIZE, not eccentricity.

**Figure (triaxial, from the board's J₂ 0.039 / C₂₂ 0.0118, which are radius-independent
at fixed density):** a = 549.6 km (sub/anti-planet), b = 512.7, c = 500.7 (polar).
Relief a−c = **48.9 km**. KSP forces a spherical ocean, so put the lava sea just below
c (~500.2 km) for zero global flooding and cut Grand Chasma's floor below it — and site
the chasm near the poles or the leading/trailing lows, where the figure is already
12–49 km below the tidal bulge.

## Related

- [`docs/reference/tidal-heating-methodology.md`](../../docs/reference/tidal-heating-methodology.md) — §6 is the destination for this evidence.
- [`results/hades_rescue/README.md`](results/hades_rescue/README.md) — the dynamics half of the same investigation.
