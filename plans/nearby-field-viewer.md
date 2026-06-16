# All stars within 50 ly — full markers (uncurated) — viewer plan

Goal: show **every** star within 50 ly in the viewer **rendered exactly like the existing
curated markers** (Teff-colour glow sprite, luminosity-scaled size, hover label, click →
info panel, zoom-in → star body), so the user perceives stellar **density/distribution**
and can explore the full neighbourhood. NOT a curation task (no Phase 1–3).

These "field" stars are identical to curated markers EXCEPT the per-star things that need
research/curation, which are **omitted**:
- **spin axis** (no i★/PA measured) — skip the axis entirely (not even the default one).
- **stellar wind / heliosphere** (no wind data) — no bubble.
- **space motion trail** (excluded per user; also RV is often missing → motion unreliable).
- **planets / disks** — none curated, so system-view zoom shows just the bare star.
The existing 143 curated systems keep all of the above; field stars are the lightweight rest.

## Data source
- **Gaia Catalogue of Nearby Stars (GCNS; Gaia Collaboration / Smart et al. 2021,
  2021A&A...649A...6G)** — EDR3-based, vetted, ~331k stars within 100 pc; essentially
  complete within 15.33 pc (= 50 ly). This is the right catalog for "all nearby stars."
  - Query alternative: `gaiadr3.gaia_source` with `parallax > 65.24` (mas) = within 50 ly.
- **Bright-star gap (must handle):** Gaia saturates at G ≲ 3, so the brightest nearby
  stars — Sirius, Procyon, Altair, Vega, Fomalhaut, α Cen, … — have poor/no Gaia astrometry.
  Several are our showcase systems. So: **field = Gaia/GCNS + our own curated stars**
  (we already have accurate astrometry for the bright ones). Dedupe by position/crossmatch.
- Expected count within 50 ly: ~2,000–3,000 stars.

## What to fetch / bake (per field star, the same fields a curated marker uses)
From Gaia: `ra, dec, parallax` (→ ICRS xyz in ly), `teff_gspphot` (else `bp_rp`→Teff) →
`teff_to_rgb` colour + spectral class, `phot_g_mean_mag` + parallax → absolute mag →
luminosity estimate → marker size (same `marker_radius` model). Designation = a common
name if Gaia/SIMBAD has one, else the Gaia DR3 / catalogue id. NO pm/rv emitted (motion
omitted). Emit as ordinary cluster objects flagged `is_field:true`, single component,
empty planets — so the existing build loop renders them as normal markers.

## Pipeline
1. New `scripts/viz/fetch_nearby_field.py` → Gaia TAP (parallax > 65.24 mas = ≤50 ly;
   pull ra/dec/parallax/teff_gspphot/bp_rp/phot_g/source_id) → `db/nearby_field.json`
   (cached, like fetch_astrometry). **SIMBAD fallback** (same as fetch_astrometry): Gaia
   saturates G ≲ 3, so for the brightest nearby stars query SIMBAD for parallax/Teff —
   include the SIMBAD-fallback bright stars in the field so it isn't missing Sirius/Vega/
   Arcturus/Capella/Pollux/Altair/Procyon/Fomalhaut/α Cen etc. **Crossmatch-dedupe vs our
   curated set** (by position/parallax) so the ones we already curate aren't double-rendered
   (they show with full curated treatment; the field supplies the rest). **Gap check:** any
   G<4, ≤50 ly star in neither set → add via SIMBAD.
2. `build_starmap.py` reads `db/nearby_field.json` → builds field clusters
   (`is_field:true`, no spin/wind/motion/planets) alongside the curated ones.
3. Viewer: field clusters render through the SAME path; `is_field` gates OUT the spin axis,
   heliosphere, and motion-trail construction. Marker sprite + hover label + click info +
   zoom-to-star all reused.

## Viewer UX
- Toggle **"모든 별 / all stars"** (default OFF — adds ~2,000 markers; keep the default
  view the curated 143). On → the full 50 ly population appears as markers; density reads
  directly from how crowded they are (incl. the **Hyades cluster edge at ~47 ly**, a real
  overdensity inside range).
- Colour by Gaia Teff (same blackbody map as curated). Size by luminosity (same model).
- Labels: hover-only (2,000 always-on labels = chaos), matching the existing declutter.
- Click → info panel with what we have (designation, distance, est. Teff/spectral class);
  no planets/components beyond the star itself.
- Honest framing in UI/meta: density within 50 ly is ~uniform (real Galactic structure is
  farther); mild outward thinning is observational completeness, not true density.

## Performance (2,000+ extra markers)
- Field clusters are light (no orbits/disks/axes/motion/planets → those arrays empty).
- Default-off: nodes hidden, skipped early in the per-frame `updateScene` loop (already
  `if(!cl.node.visible) return`) → zero cost when toggled off.
- On: ~2,140 clusters in the loop; keep the per-field-star path minimal; if the per-frame
  glow-sizing walk is too heavy, short-circuit far/invisible clusters (P4 of the viewer-opt
  plan) or batch field glows. Measure before optimizing.

## Decisions (settled with user)
1. **Source**: Gaia GCNS within 15.33 pc (50 ly). ✓
2. **Colour**: by Gaia Teff/Bp-Rp (same blackbody map as curated). ✓
3. **Representation**: full markers identical to curated, MINUS spin axis / heliosphere /
   motion (and planets/disks, which are uncurated). ✓
4. **Bright stars**: covered by existing curated markers (Gaia saturates them); field =
   GCNS minus curated dupes; gap-check G<4. ✓
5. **Storage**: `db/nearby_field.json` cached fetch artifact (like astrometry_raw). ✓
6. **Default**: behind a toggle, OFF by default (recommended) — confirm.

## Honesty / caveats (note in UI + meta)
- GCNS completeness drops for the faintest M/L dwarfs and unresolved binaries (counted as
  one). Brightest stars are the curated markers, not Gaia.
- Field stars carry NO motion (static), no spin/wind/planets — uncurated, visualization only.
- Colour is a perceptual approximation, not a calibrated SED (same caveat as the markers).
- These stars are NOT in db/systems (no curation claim); they live in db/nearby_field.json.

## Verification
- Count sanity (~2–3k within 50 ly; α Cen / Sirius / Procyon NOT double-rendered).
- Field stars have no axis/heliosphere/motion/planets; curated ones unchanged.
- Reproducible build; payload size recorded; node --check; check.sh green.
- Visual: toggle on at map scale → density (incl. Hyades edge) reads; zoom into a field
  star → bare star, no overlays; floating-origin rebase stable; perf acceptable.

## Scope / non-goals
- No curation, no planets, no spin/wind/motion for field stars.
- Single-file viewer, CDN importmap, GitHub-Pages model unchanged.
- DB/pipeline unchanged except the new fetch + builder emit + `is_field` gating.
