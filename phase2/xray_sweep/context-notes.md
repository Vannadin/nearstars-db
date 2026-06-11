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

(appended as values are verified against cache)
