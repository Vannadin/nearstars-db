<!-- NS 시스템의 사이파이 / 대중문화 레퍼런스 인덱스 -->
# Cultural context — NS systems in science fiction

NearStars covers real nearby stars; several of those have prominent appearances in science fiction. This doc indexes the connections, distinguishes novel-fact from real-fact, and flags retracted-or-refuted planets that fiction has anchored to. Cultural references are NOT cfg-emitted — keep this doc as narrative reference only.

## Tau Ceti — *Project Hail Mary* (Andy Weir, 2021)

- **Body in novel**: "Adrian" = Tau Cet e
- **Status in real world**: Tau Cet e was reclassified to **"False Positive Planet"** by NASA Exoplanet Archive on 2026-04-09, citing Figueira et al. 2025 (`2025A&A...700A.174F`) ESPRESSO sub-10 cm/s RV non-detection. The novel was written from the Feng 2017 detection picture; that picture is now obsolete.
- **What the novel got right**: G8V spectral type, ~9 Gyr age (twice solar), Tau Ceti as a long-stable astrobiology target
- **What the novel got wrong (per current data)**: Adrian as a habitable super-Earth — the underlying RV signal is now considered stellar activity. The novel also omits the substantial debris disk (ALMA-resolved 6–55 AU, ~1.2 M⊕ dust, MacGregor 2016), which would pose a real navigation hazard.
- **NS DB**: e is correctly absent (NEA-inherited disposition). f/g/h remain `pl_controv_flag=1` but on retraction watch (Figueira 2025 also reports them at or below detection floor).

## 40 Eridani A — *Star Trek* (Vulcan) + *Project Hail Mary* (Erid)

- **Body in fiction**: 40 Eri A b serves as Vulcan in the *Star Trek* canon (Roddenberry's letter to *Sky & Telescope* 1991 confirmed 40 Eri over Epsilon Eri). The Eridians of *Project Hail Mary* (Rocky's species) also originate from 40 Eridani A.
- **Status in real world**: 40 Eri A b confirmed exoplanet (Ma 2018, `2018AJ....155..117M`); 8.5 d period, 8.5 M⊕ super-Earth. Not in the habitable zone in modern terms — the Vulcan fiction predates this discovery and assumed an Earth-like world.
- **NS DB**: `40_eridani_a.json` + `40_eridani_b.json` (white dwarf) + `40_eridani_c.json` (M dwarf) — multi-star system

## Epsilon Eridani — *Babylon 5* (Vorlon homeworld), early *Star Trek* (original Vulcan)

- **Body in fiction**: Vorlon Prime in *Babylon 5* (J. Michael Straczynski). Original Vulcan in early *Star Trek* lore before being retconned to 40 Eri A.
- **Status in real world**: ε Eri b confirmed RV planet (Hatzes 2000 + Mawet 2019 direct imaging) at ~3.5 AU, M sin i ~0.78 M_Jup — a gas giant, not Earth-like. Surrounded by a three-belt debris disk.
- **NS DB**: `eps_eri.json` (host + b in DB; Phase 3 synthesis at `docs/phase3/eps-eri.md` + `eps-eri-b.md`)

## Wolf 359 — *Star Trek: The Next Generation* (Battle of Wolf 359)

- **Body in fiction**: The Battle of Wolf 359 (TNG "The Best of Both Worlds", 1990) is a fictional Starfleet encounter with the Borg — set at the real star's location but with no canonical planet.
- **Status in real world**: Wolf 359 is an M6.5 flare star at 7.86 ly. No confirmed planets (deep RV upper limits).
- **NS DB**: `wolf_359.json` (host only, no planets)

## Alpha Centauri — *Avatar* (Pandora), *Three-Body Problem*, many

- **Body in fiction**: Pandora orbiting α Cen A in *Avatar* (Cameron 2009). The trisolaran homeworld of Liu Cixin's *Three-Body Problem* (the trisolaran problem is the canonical α Cen 3-body chaos).
- **Status in real world**: α Cen A/B with Proxima at ~13 000 AU. Proxima b confirmed habitable-zone Earth-mass; Proxima d candidate (Faria 2022). α Cen A/B planets remain unconfirmed (Beichman & Sanghi 2025 "S1" JWST/MIRI candidate at ~1.5 AU pending follow-up).
- **NS DB**: full triple system with Jacobi multi-star pipeline + Principia n-body export — the canonical hierarchical-multi-star showcase in NS

## Methodology note

Fiction does not override observation. When a novel anchors plot to a planet that is later refuted (like Tau Cet e), the NS DB follows real-world disposition. Cultural references are documented here as a narrative companion, not as cfg-emitted descriptions. If a future feature ships per-body description strings, this doc is the source of the fiction-aware flavor text — until then it is repo documentation only.

## Related

- [rex-data-comparison](rex-data-comparison.md) — Tau Cet e historical curation discussion (now resolved)
- [methodology](methodology.md) — provenance-first DB policy that this doc respects
- [`docs/phase3/eps-eri.md`](../phase3/eps-eri.md) — host synthesis with Babylon 5 / Trek note in scope
- [`docs/phase3/alpha-centauri-a.md`](../phase3/alpha-centauri-a.md) — host synthesis with Pandora / trisolaran context in scope
