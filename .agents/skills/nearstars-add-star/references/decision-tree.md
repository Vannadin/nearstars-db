# Decision Tree

Use this when classifying a new star request. Each branch dictates which
files you'll edit and which references you'll consult.

---

## Step 0 — Is the request actionable?

Quick filter before doing any work.

```
User mentions a star or system name
├── Already exists in target_list.json?
│   ├── Yes → Is the user requesting Phase 2 upgrade?
│   │       ├── Yes → Go to Step 1 with planet-curation focus
│   │       └── No → Confirm with user (might be a typo / want different system)
│   └── No → Go to Step 1
└── Distance > 50 ly?
    ├── Yes →
    │   ├── 50–80 ly → could be Principia-only perturber (no Kopernicus
    │   │   body, gravity effect only) per guideline §3.1. Pipeline does
    │   │   not implement this mode yet. Stop, report option to user.
    │   └── > 80 ly → out of Principia range too. Stop, report distance.
    └── No → Proceed
```

How to confirm distance without bothering the user: SIMBAD parallax. The
helper script (`scripts/lookup_gaia.py`) prints distance. If parallax
gives distance > 50 ly, report back and stop.

---

## Step 1 — Classify the system

The four axes that determine workflow shape:

```
1. Multiplicity
   ├── Single → one component, no binary_orbits.json edit
   └── Binary/multiple → N components, must populate binary_orbits.json

2. Brightness (V magnitude)
   ├── V < ~6 (Vega, Sirius, Procyon, Pollux, Alpha Cen) → Gaia saturated
   │   ├── Astrometry: SIMBAD fallback (epoch becomes J2000.0)
   │   └── Photometry: must add to HIPPARCOS_V
   └── V > ~6 → Gaia DR3 normal path

3. Planets
   ├── None → no planets_curated.json edit
   ├── Confirmed in NASA Archive → Phase 1 curation default
   └── Recent discovery (post-2024, may not be in Archive yet)
       → Manual entry; mark with note

4. Spectral type
   ├── Normal M–O dwarf → standard treatment
   ├── L/T/Y brown dwarf → no Gaia photometry; vmag_v may be null
   └── White dwarf → SIMBAD spectype + literature mass; evolutionary
       models for WD are different from MS stars (use WD cooling models)
```

---

## Step 2 — Map classification to file edits

| Files | Single+normal | Single+bright | Binary+normal | Binary+bright | Y dwarf |
|---|---|---|---|---|---|
| `target_list.json` | ✓ | ✓ (gaia_source_ids=[]) | ✓ | ✓ | ✓ (gaia_source_ids=[]) |
| `stellar_props_curated.json` | ✓ | ✓ | ✓ (per component) | ✓ (per component) | ✓ |
| `HIPPARCOS_V` | — | ✓ | — | ✓ (per component) | — |
| `SIMBAD_ALIASES` | if name mismatch | if name mismatch | if name mismatch | if name mismatch | if name mismatch |
| `binary_orbits.json` | — | — | ✓ | ✓ | — (unless binary) |
| `planets_curated.json` | if planets | if planets | if planets | if planets | rarely (Y dwarfs as planet hosts are rare) |

---

## Concrete case studies

### Case A — Wolf 359 (single M dwarf, 1 planet)

```
Classification: single + normal + 1 planet + M-dwarf
Distance: 7.86 ly  ✓ within range

Edits:
1. target_list.json — append entry with Gaia source_id
2. stellar_props_curated.json — Wolf 359 mass (Mann 2015), radius (interferometry if available)
3. planets_curated.json — Wolf 359 b (Tuomi 2019 discovery + Maire 2023 reanalysis)

Estimated time: 10-15 min
```

### Case B — Vega (single, bright, no planets confirmed)

```
Classification: single + bright (V=0.03) + 0 confirmed planets + A-dwarf
Distance: 25.04 ly  ✓ within range

Edits:
1. target_list.json — entry with empty gaia_source_ids
2. stellar_props_curated.json — Vega mass/radius (Yoon 2010 evolutionary)
3. fetch_photometry.py HIPPARCOS_V — "Vega": 0.03

Notes:
- Astrometry will come from SIMBAD path (J2000 epoch)
- A-type bright stars often have asteroseismology, prefer it over evolutionary

Estimated time: 10 min
```

### Case C — Luhman 16 AB (binary brown dwarfs, no confirmed planets)

```
Classification: binary + bright-ish (V≈18 — but Gaia *should* have it; check) + 0 planets + L/T transition

Distance: 6.5 ly  ✓ within range

Edits:
1. target_list.json — binary entry with two Gaia IDs (if Gaia has both)
2. stellar_props_curated.json — A and B masses separately
3. binary_orbits.json — Luhman 16 mutual orbit (Bedin 2024)

Notes:
- Brown dwarf masses depend on age estimate — record `method: "evolutionary_model"` with note
- vmag_v likely null for both (L/T objects faint in V)

Estimated time: 20-30 min (binary orbit research dominates)
```

### Case D — TRAPPIST-1 (single, 7 planets, currently active research)

```
Classification: single + normal-faint (V=18.8) + 7 confirmed planets + M-dwarf
Distance: 39.5 ly  ✓ within range

Phase 1 edits:
1. target_list.json
2. stellar_props_curated.json — Van Grootel 2018 mass + radius
3. planets_curated.json — b,c,d,e,f,g,h (7 entries) from Agol 2021 TTV analysis

Notes:
- TTV-dominated system — use Agol 2021 dynamical fit for masses (more accurate than transit-only)
- Each planet has tperi_bjd from TTV — must populate orbital epoch
- This is a candidate for Phase 2 escalation (in-game implementation likely)

Estimated time: 30-45 min for Phase 1, 1-2 hours for Phase 2
```

### Case E — White dwarf (rare in current target list)

```
Classification: single + bright-ish + 0 planets (usually) + WD
Distance: depends

Notes:
- Mass: WD cooling models (e.g. Bedard 2020). Method = "evolutionary_model"
- Radius: from M-R relation for WDs (NOT main-sequence relations)
- principia gravParameter calculation works the same (M⊙ × GM_sun) — WDs are dense but compact
- mean_radius_km will be much smaller than expected: ~7000 km vs 700,000 km for sun

Estimated time: 15-20 min
```

---

## When to stop and ask the user

The autonomy policy says don't ask about Gaia ID or recommended selection.
But surface these situations:

- **Ambiguous star name input**: user typed something that maps to
  multiple SIMBAD entries (e.g. "Cen A" → Alpha Cen A or Beta Cen?).
  Run `lookup_gaia.py` with several reasonable interpretations, list 2-3
  candidates with distance + spectral type, ask user to pick. Example:
  
  > "Cen A"는 두 가지 후보가 있습니다.
  > 1. Alpha Centauri A (G2V, 4.4 ly) — 가장 일반적
  > 2. Beta Centauri A (B1III, ~390 ly) — Kopernicus 범위 밖
  > 어느 쪽을 추가할까요?

- **Distance ambiguous**: SIMBAD parallax has error ≥ 30% (rare for nearby
  stars but happens for very faint sources)
- **Multiple discovery papers conflict by >30% on planet mass**: not a
  method-priority tiebreaker case — needs user judgment
- **Star has been retracted or downgraded** (e.g. exoplanet candidate
  later disproven): user should know before adding
- **System has 5+ confirmed planets**: confirm whether to apply Phase 1
  default or wait for Phase 2 decision
- **Mod-name or scope question** (e.g. "should this be in NearStars or
  in a Principia-only addon?"): out of scope for this skill
- **Distance in 50–80 ly band**: skill currently stops; offer the
  Principia-only option (not yet implemented) and let user decide
  whether to extend the pipeline or skip the star

For everything else, proceed and report results.
