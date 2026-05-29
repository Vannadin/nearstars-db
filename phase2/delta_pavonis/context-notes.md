# Context notes — Delta Pavonis Phase 2

Append-only decision log. Newest at bottom.

## 2026-05-29 — why δ Pav, and the contamination to undo

δ Pav is Tier 1 host #1 (postmortem recommendation #5: "rewrite the Delta Pav
template from the Rains 2020 anchor; do not reuse 4d26495"). It is the first host
curated under `phase2/curation-data-contract/SPEC.md`.

**Current state (the inversion + contamination):**
- NO Phase 2 in `stellar_props_curated.json` (Phase 3 sits on Phase 1).
- Existing `docs/phase3/delta-pavonis.md` Decisions use model/indirect values:
  - `radius_rsun` 1.22 ± 0.02 (Bruntt 2010 asteroseismic)
  - `teff_k` 5604 (Gaia DR3 GSP-Phot)
  - These MISS the more direct Rains 2020 interferometry — the postmortem's flagged
    false-negative-interferometry pattern (template assumed δ Pav had no direct θ_LD).

**The anchor (postmortem-verified, must be the recommended radius/Teff source):**
- Rains et al. 2020, `2020MNRAS.493.2377R`, arXiv:2004.02343, VLTI/PIONIER.
- "Precision angular diameters for 16 southern stars with VLTI/PIONIER"; δ Pav is star #11/16.
- θ_LD = 1.828 ± 0.025 mas → R = 1.197 ± 0.016 R☉; Teff = 5571 ± 48 K.
- Observability: VLTI@Paranal (lat -24°), SUSI@Narrabri (lat -30°) both reach dec -66°;
  only CHARA (lat +34°) cannot. "Too far south for CHARA" ≠ "no interferometry".

## Candidate Phase 2 sources by category (from the md bibliography — verify each in cache)
- mass: Bensby 2014 (2014A&A...562A..71B) + Spada 2011 evolutionary fit
- radius: **Rains 2020 (rec)**; Bruntt 2010 asteroseismic (alt)
- teff: **Rains 2020 (rec)**; Bensby 2014 spectroscopic 5587±50; Gaia GSP-Phot 5604 (alt)
- luminosity: Rains 2020 bolometric if reported, else Eiroa 2013 DUNES SED 1.22 L☉
- age: Holmberg 2009 (2009A&A...501..941H) 6.6 Gyr; Spada 2011 subgiant 7.5 Gyr (isochrone)
- metallicity: Bensby 2014 FEROS high-res +0.33 ± 0.05 dex
- rotation: vsini ≈ 1.7 km/s (Bensby 2014) → P_rot lower bound only; low confidence
- activity: Henry 1996 log R'HK -5.10; Hünsch 1998 (1998A&A...335L..73H) ROSAT X-ray
- disk: Eiroa 2013 DUNES + Lawler 2014 + Beichman 2006 → `disks_curated` (debris belt)

## Method-label notes (avoid the 40 Eri A drift)
- Rains 2020 radius/teff = `interferometry`.
- Bruntt 2010 radius = `asteroseismology` (radius from p-modes) — NOT evolutionary_model.
- Mass from Spada/Bensby evolutionary fit = `evolutionary_model`; if from an empirical
  M-R relation, use `empirical_relation` (added to schema 2026-05-29, commit 76c9fc2).

## Open questions to resolve during curation
- Canonical host key in stellar_props_curated.json: "Delta Pavonis"? confirm via _naming / target_list.
- Does Rains 2020 report L directly, or only θ_LD + Teff (→ derive L)?
- Reconcile age: keep documented Holmberg/Spada spread; pick recommended per method tier.

## 2026-05-29 — Stage 1 lit search result (web subagent)
Rains 2020 (2004.02343) confirmed verbatim from PDF Table 4: θ_LD = 1.828 ± 0.025 mas,
R = 1.197 ± 0.016 R☉, Teff = 5571 ± 48 K, f_bol = 107.2 ± 2.5e-8 erg/s/cm²,
**L = 1.24 ± 0.03 L☉**. δ Pav = star #11/16. Author: Rains, Ireland, White, Casagrande,
Karovicova. So Rains 2020 directly anchors radius + teff + LUMINOSITY (3 categories).
Rains 2020 Table 1 input spectroscopy: Teff 5604±38, logg 4.26±0.06, [Fe/H] +0.33±0.03,
plx 164.05±0.36 mas.

It is the ONLY direct interferometric measurement (no 2nd-instrument cross-check; not in
Rains Table 5 literature-comparison = no prior interferometry). "No interferometry" was
historically true pre-2020, now FALSE. CHARA/NPOI (north) can't see dec -66°; VLTI/SUSI can.
No post-2020 paper supersedes the parameter set. Makarov 2021 (2105.03244) = companion
candidate only, not a parameter source. → luminosity recommended source upgraded from
Eiroa 2013 SED to Rains 2020 direct.

## 2026-05-29 — Stage 3 value-check from cache (read directly, subagent socket-failed)
Bruntt 2010 (1002.4268.md) line 82, columns mapped via α Cen A / β Vir Rosetta
(cols: mass_direct | mass_model | R_direct | R_model | L_direct | L_model | Teff_direct | Teff_spec1 | Teff_spec2 | FeH1 | FeH2):
  δ Pav = mass 1.07±0.13 (asteroseismic, νmax-only, footnote d) | R 1.20±0.04 (asteroseismic)
  | L 1.22±0.04 | Teff 5550/5540 (spec) | [Fe/H] +0.38/+0.33. vsini≈1.7 km/s (logg table line 281).
  CATCH: the old Phase 3 md said "radius 1.22 (Bruntt 2010)" — but Bruntt's 1.22 is LUMINOSITY;
  its radius is 1.20. Template confused the columns. (Recommended R is Rains 1.197 anyway.)
  CROSS-CHECK (independent methods agree): Rains R 1.197 ≈ Bruntt 1.20; Teff 5571 ≈ 5550; L 1.24 ≈ 1.22.

Cache MISSES (survey tables stripped by ar5iv extraction → need VizieR): Bensby 2014 [Fe/H]/mass,
Holmberg 2009 age, Spada 2011 (no δ Pav row). Henry 1996 + Hünsch 1998 have no arXiv (VizieR).

Recommended-pick plan (method tier): radius=Rains interferometry (Bruntt asteroseismic alt);
teff=Rains interferometry (Bruntt spec alt); luminosity=Rains bolometric (Bruntt alt);
mass=Bruntt asteroseismology 1.07±0.13 (no binary orbit available, asteroseismology is top tier here);
[Fe/H]=Bruntt high_res +0.33 (Bensby agrees, value-check via VizieR); age=Holmberg/Spada via VizieR;
rotation=vsini 1.7 km/s (low conf); activity=Henry log R'HK + Hünsch X-ray via VizieR.

## 2026-05-29 — Stage 3 VizieR fills (age, activity, X-ray, Bensby cross-check)
- Age GCS III (Holmberg 2009, V/130/gcs3, HIP 99240): age=9.3 Gyr (range 5.8–10.7). NO mass column.
- Age Bensby 2014 (J/A+A/562/A71/tablec3, HIP 99240): 4.9 Gyr (3.3–9.6). → BIG age tension 9.3 vs 4.9.
- log R'HK Henry 1996 (J/AJ/111/439, HD 190248): R'HKm = -4.999 ± 0.018 (also R'HK -4.99). Nobs=5.
- X-ray Hünsch 1998 (J/A+AS/132/155): count 0.073±0.028 ct/s, HR -0.53±0.41, L_X 1.8e20 W = 1.8e27 erg/s
  → log L_X ≈ 27.26 (erg/s). With L_bol=1.24 Lsun=4.75e33 erg/s → log(Lx/Lbol) ≈ -6.4.
- Bensby 2014 DOES contain δ Pav (HIP 99240): [Fe/H] +0.37±0.20, mass 1.03 (0.96–1.10), Teff 5635±122.

CATCHES vs the contaminated Phase 3 md:
  (1) radius: md "1.22 (Bruntt)" — Bruntt R is 1.20, 1.22 was luminosity. Recommended = Rains 1.197.
  (2) age: md "7.0±0.5 (Holmberg 6.6 / Spada 7.5)" — fabricated midpoint; actual Holmberg=9.3, Bensby=4.9.
  (3) activity: md "log R'HK -5.10" — actual Henry 1996 = -4.99 (-4.999±0.018).

Proposed recommended picks (method tier): radius/teff/lum = Rains 2020 (interferometry/bolometric);
mass = Bruntt 2010 asteroseismology 1.07±0.13 (no binary orbit; asteroseismology top tier; Bensby 1.03 alt);
[Fe/H] = TBD (Bruntt +0.33 vs Bensby +0.37±0.20 — need uncertainty decision);
age = DOCUMENTED DIVERGENCE (Holmberg 9.3 vs Bensby 4.9 — both isochrone; pick + document);
rotation = vsini 1.7 km/s → P/sin i ≈ 36 d lower bound, low conf;
activity = Henry log R'HK -4.999±0.018 (rec) + Hünsch X-ray log(Lx/Lbol) -6.4 (2nd entry).

## 2026-05-29 — Stage 3 RECENCY check (user-requested; server-side subagent)
- Activity UPGRADE: Gomes da Silva 2021 (2021A&A...646A..77G, AMBRE-HARPS) log R'HK = -5.13
  (wmean -5.1315 / median -5.1338), replaces Henry 1996 -4.999. Modern, large-N, long baseline.
- [Fe/H]: GdS 2021 +0.36 ± 0.02 (AMBRE) — tightest + modern; Bensby +0.37, Bruntt +0.33 corroborate.
  → recommended [Fe/H] = GdS 2021 +0.36±0.02 (high_res_spectroscopy).
- Asteroseismology: Lund 2025 (2025A&A...701A.285L, arXiv 2508.08699, TESS) νmax=2269.8±64.4,
  Δν=107.9±0.2 µHz. NO modeled M/R/age published → keep Bruntt 2010 M/R; cite Lund as modern seismic.
- Age: nothing newer/better; Holmberg 9.3 vs Bensby 4.9 tension stands (ranges overlap 5.8-9.6).
  DEFAULT pick = Holmberg 2009 9.3 Gyr recommended — physically consistent with very low activity
  (-5.13) + slow rotation (old quiet subgiant); Bensby 4.9 as alt; document divergence in Phase 3.
- Rotation: no Prot exists; keep vsini 1.7 km/s → P_rot ≲ 36 d (sin i upper bound), low confidence.
- Gaia DR3 GSP-Phot/FLAME: REJECTED (Teff 5437 / [Fe/H] +0.03 / age 0.59 Gyr all biased for this
  bright metal-rich star).
