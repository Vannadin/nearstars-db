<!-- X-ray/플레어 sweep 결정 로그 — append-only -->
# X-ray / flare sweep — context notes

## Scope decisions (2026-06-11)

- **One schema axis, not two.** `xray_measurements` only. Flare *rates*
  (FFD slopes, flares/day) are NOT a schema category: no mod field
  consumes them numerically (Kerbalism radiation_surface is one scalar),
  and FFD parametrizations vary per paper. Flare character goes into
  entry `notes` + the Phase 3 basis text (Proxima flare boost stays a
  synthesis judgment, now anchored to a measured quiescent L_X).
- **Two value keys.** `value_log_lx_ergs` (log10 L_X, erg/s — store the
  band in notes; ROSAT 0.1–2.4 keV unless stated) and `value_log_rx`
  (log10 L_X/L_bol) — papers report either; DB principle stores what's
  published, no silent conversion. derived layer resolves recommended.
- **Methods.** `x_ray_photometry` (any imaging X-ray flux measurement —
  survey or pointed; instrument goes in notes), `unverified` escape
  hatch. No per-instrument methods: technique is identical.
- **Precedent.** Follows the per-axis batch pattern of 61e0ad9 (mass
  loss), 6b5b3d7, 8ed58a1 (cycles): schema commit → one curation commit
  across all data-bearing hosts → Phase 3 consumption commit. Anchor bib
  = docs/phase3/_bib/stellar-wind.yaml (append).
- **Sun anchor for Phase 3.** radiation_surface_relative_sun will be
  anchored as ~ (L_X / L_X,⊙) with L_X,⊙ cycle-mean — the exact solar
  value + any non-linearity is a Phase 3 decision, recorded there; the
  DB stores only per-star measurements.

## Value-check log

All recommended values main-thread-verified (agent reports re-grepped in
docs/phase3/_papers/ or the named VizieR catalog) before writing.

- **αCen A 26.78** — 1612.06570.md: "detected in the first XMM observation
  in 2003 with L X ≈ 6 × 10 26"; band line "0.2 – 2.0 keV range"; cycle
  "about 15 – 20 years", contrast "nearly one order".
- **αCen B 27.04 (rec)** — 1009.1652.md: "Twenty-seven ROSAT pointings …
  averaging L X = 1.1 ( ± 0.26) × 10 27". Alt 27.60 — 1612.06570.md:
  "spectral modelling of the 2012 XMM data … L X ≈ 4 × 10 27 …
  brightest"; "P act ≈ 8 − 9 yr"; amplitude "about 6 – 9".
- **Proxima R_X −4.4 (rec)** — 1610.03447.md line 197 Table 3 row
  `| Prox Cen | M5.5V | 0.12 | -4.4 | 1.5 | 7.1 | 83 | 90 |` + line 187.
  Alt 27.22 — NEXXUS VizieR J/A+A/417/651 Gl 551 rows: S 27.22 / P 26.81
  / F 27.74 (2026-06-11 query); matches the 27.2 quoted in 0808.2986.md.
- **Barnard 25.3 / −5.8 (rec)** — PRIMARY-VERIFIED after fetching France
  2020 (arXiv 2009.01259, pinned in _bib/stellar-wind.yaml):
  2009.01259.md line 49 "F X ≈ 4.8 × 10 -14 erg cm -2 s -1 ; log10(L X) =
  25.3; L X / L bol = 1.6 × 10 -6"; flare rate line 83 "rate of roughly 6
  per day incident … Sun emitted approximately 4 flares per day". Alt
  25.85 — Wood 2021 2105.00019.md Table 3 line 173 + NEXXUS VizieR Gl 699
  (S 25.85 / P 25.74). Alt 25.53±0.54 — 2310.04302.md line 310.
- **tau Cet 26.69** — Wood 2021 2105.00019.md Table 3 line 194 +
  provenance line 220 ("based mostly on ROSAT all-sky survey … Schmitt &
  Liefke 2004") + NEXXUS VizieR Gl 71 (S 26.69 / H 26.54).
- **40 Eri A 27.52 (rec)** — NEXXUS VizieR Gl 166A rows: S 27.52 /
  H 27.17. **Boyajian 2012 divergence**: 1208.2431.html Table 6 GJ 166A
  ratio 1.03E-05 → implies log L_X ≈ 28.2, ~5× above both NEXXUS modes
  (HR1→flux conversion overestimate suspected). Kept as non-recommended
  entry with a do-not-use note — this was the sweep's main catch.
- **eps Ind A 27.39 (rec)** — Wood 2005 astro-ph_0506401.html table row
  "ϵ Ind K5 V 3.63 68 64 0.5 27.39 0.56" + md line "ROSAT All-Sky Survey
  measurements (see Paper 2)". Alt R_X −5.62 — 2205.08077.md line 27
  "R X = − 5.62 … from the ROSAT all-sky survey bright source catalog
  (Voges et al., 1999)".

Band caveat for Phase 3: αCen values are 0.2–2.0 keV (XMM-era), Barnard
rec is Chandra 0.3–10 keV, the rest are RASS 0.1–2.4 keV. Sun-relative
ratios must use a matching solar anchor per band (Phase 3 decision).
