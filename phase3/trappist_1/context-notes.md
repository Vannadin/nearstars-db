# TRAPPIST-1 system Phase 3 — context notes

Append-only log of decisions made while extending Phase 3 synthesis to
the remaining six TRAPPIST-1 planets (b, c, e, f, g, h). d is the
already-completed pilot.

## 2026-05-21 — Scope and depth

User confirmed: full d-level depth for all 6, parallelized fetches.
Each planet gets ~300 lines of synthesis: decisions table (~30 rows),
Surface / Atmosphere / Rotation / Visual sections, full bibliography
with Read / context / instrument / not-read categories.

## 2026-05-21 — Per-planet observational state going in

This drives how heavily synthesis vs. measurement each planet leans:

- **b** — innermost. JWST MIRI 12.8 μm emission (Greene 2023):
  Tday ≈ 503 K, A_B = 0.0 ± 0.1, atmosphere-free or trace. The
  cleanest "definitely bare rock" case. Lava world potential at
  3.4 S⊕ insolation.
- **c** — JWST MIRI 15 μm emission (Zieba 2023): Tday ≈ 380 K
  consistent with bare rock + low albedo OR very thin (≲10 bar) CO₂.
  Also constrained, slightly more atmosphere room than b.
- **d** — DONE. JWST NIRSpec transmission (Piaulet 2025) flat,
  most-atmospheres-excluded. Adopted thin-atmosphere + terminator
  H₂O ice cloud scenario.
- **e** — habitable zone center. No JWST transmission yet published
  in the same depth. Way 2025 ROCKE-3D GCM explores
  Venus/Earth/Dead variants. Best HZ candidate. Will rely heavily on
  Wolf 2017, Turbet 2018, Way 2025, Lustig-Yaeger 2024 (if available)
  GCM predictions.
- **f** — outer HZ edge. Cooler than e, ~Teq 215 K. Turbet 2018 places
  it in the "Snowball Earth or thin CO₂" branch. Lim 2023 JWST/NIRISS
  transmission excludes H₂-rich (per the d paper's reference list).
- **g** — outer HZ. ~Teq 195 K. Even more snowball-prone than f. Less
  observational follow-up; relies on outgassing/escape models.
- **h** — outermost. ~Teq 169 K. Sub-Mars mass (0.33 M⊕). Permanently
  frozen analog; possible subsurface ocean if internally heated.

## 2026-05-21 — Methodology reuse from d

Constants reused for all 7 (host star is the same):

- Host: TRAPPIST-1 M8V, 2566 K, 0.1192 R☉, 0.0898 M☉, 0.000522 L☉
- Age: 7.6 ± 2.2 Gyr (Burgasser 2017)
- Stellar SED color tint: red-orange `~#ff7a1a` for visual sections
- Tidal lock baseline 1:1, obliquity 0
- Eccentricity: from Agol 2021 TTV (per planet)
- Mass / radius / a / P: Agol 2021 TTV
- "Sister planets in sky" geometry: near-coplanar (Agol 2021)
- ~8 Gyr age implies heavy impact accumulation on all surfaces

## 2026-05-21 — Per-planet expected scenario choices

Working hypothesis before reading papers (will revise as needed):

- **b** — bare hot rock (basaltic/melt-resurfaced). No atmosphere.
  Strong substellar magma-ocean residual? Way 2024 calls it "exo-Io"
  candidate from induction heating. Visual: dark basalt + iron oxide
  patches under fierce red glare, possibly fresh lava in patches.
- **c** — bare warm rock. No detectable CO₂ atmosphere down to thin
  limit. Similar palette to b but cooler, less melt.
- **e** — adopt habitable-temperate scenario: 1 bar N₂+CO₂+H₂O
  atmosphere, ocean-bearing, blue-tint with cloud cover. The classic
  "best habitable candidate" cfg variant.
- **f** — outer HZ, snowball/cold thin-CO₂ branch. Mostly icy
  surface, thin atmosphere. Possible subglacial liquid water but
  surface frozen.
- **g** — fully frozen, slightly thicker CO₂ to stave off complete
  collapse (Wordsworth 2017 cold-trap idea). Snowy surface.
- **h** — Mars/Pluto analog. Either fully frozen N₂/CO₂ ice with bare
  surface in places, or volatile-stripped bedrock. Tend toward icy
  given outer location.

## 2026-05-21 — Heading structure (frozen for ko mirror parity)

All six syntheses use the same H2 structure as d:
- (intro paragraphs, no H2)
- ## Decisions
- ## Surface synthesis
- ## Atmosphere synthesis
- ## Rotation & spin synthesis
- ## Visual styling
- ## Bibliography
- ### Read (visual-informative, drove decisions above)
- ### Read (context / methodology, not decision-driving)
- ### Read (instrument-only, not visual-informative)
- ### Not read — no arXiv preprint available (N papers)
- ## Open items for follow-up

If a category is empty for a given planet, the H3 heading is still
kept (with a brief "none for this planet" note) so the ko mirror
parses cleanly.

## Related

- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to

## 2026-07-20 — star-level (host) synthesis, WP4 of pipeline-flow-program

### Decisions-row classification (Step 9.0) — TRAPPIST-1 (star)

- spectral_type M8.0V ±0.5            → canonical-aligned (Gillon 2016 via VG18 §1)
- mass_msun 0.0898 ±0.0023            → canonical-aligned (Agol 2021, curated recommended)
- radius_rsun 0.1192 ±0.0013          → canonical-aligned (Agol 2021)
- teff_k 2566 ±26                     → canonical-aligned (Agol 2021; 2566±50 prior quoted in Radica 2024 §3)
- luminosity_lsun 5.22e-4             → canonical-aligned (Van Grootel 2018)
- metallicity_fe_h_dex +0.04 ±0.08    → canonical-aligned (Gillon 2016)
- age_gyr 7.6 ±2.2                    → canonical-aligned (Burgasser & Mamajek 2017)
- rotation_period_days 3.295 ±0.003   → canonical-aligned (Vida 2017; Berardo 2025 3.27±0.04 independent)
- activity_log_lhalpha_lbol −4.85…−4.60 → canonical-aligned (B&M 2017 Table 1)
- x_ray_log_lx_lbol −3.52 ±0.17       → canonical-aligned (B&M 2017 / Wheatley 2017)
- magnetic_field_kg 0.6 (+0.2/−0.4)   → canonical-aligned (Reiners & Basri 2010 via VG18 §4.2)
- flare_ffd_cumulative_slope_beta 0.753 → canonical-aligned (Vasilyev 2026; supersedes Vida β≈0.59 — reconciliation in prose)
- superflare_e32_interval_days 25     → canonical-aligned (Vasilyev 2026)
- flare_rate_e30_per_year ~1000       → canonical-aligned (Shapiro 2026 §I)
- flare_color_temp_k 3500–4000        → canonical-aligned (Shapiro 2026 H2 thermostat; Howard 2025 RADYN fits 2115–4010 K corroborate) — KEY Firefly-facing row
- spot_temp_k 2350–2550               → canonical-aligned (Vasilyev 2025)
- spot_feature_area_disk_pct 0.06–1.5 → canonical-aligned (Vasilyev 2025 §3.4, per-feature)
- stellar_color_temp_k 2566           → canonical-aligned
- visual_surface_tint_hex_primary #ffcc70 → tie-break/methodology (Pickles M-ladder clamp below coolest anchor; stellar-photospheric-color-methodology)
- figure_j2 2.0e-6                    → methodology-derived (Radau–Darwin polytrope branch J2/q 0.084, q=2.33e-5; closes the T-1 carry-over from the stellar-J2 sweep)

Counts: 18 canonical-aligned, 2 tie-break/methodology, 0 documented divergence.

### Extraction + verification notes

- Paper extraction delegated (11 cached texts); all load-bearing quotes
  grep-verified on main thread against docs/phase3/_papers/ before drafting.
- Agol 2021 cache (2010.01074.md) is ABSTRACT-ONLY — stellar M/R/Teff rows
  rest on the Phase 2 curated entries (paper-verified at curation) plus the
  2566 K literature quote embedded in Radica 2024 §3. Flagged in Open items.
- XUV discrepancy: Wheatley 2017 L_XUV/L_bol 6–9e-4 (~1.2–1.8e27 erg/s) vs
  Berardo 2025 reconstruction 1.83e28 erg/s (30× the 2017-era 6.28e26).
  Decisions carries the X-ray row only; XUV spread documented in prose +
  Open items (radiation-environment re-anchor candidate).
- Stellar wind: no measurement exists (wind synthesis 2026-06-11 skipped
  T-1) → no wind section; noted in Open items.
- **Step-10 catch (main-thread verify earned its keep):** first draft said
  v sin i 6±2 km/s is "consistent with" the 3.295 d period — Vida 2017 §3
  says the OPPOSITE: v sin i matches the superseded 1.40 d value (implying
  P_rot ≈ 0.99 d, 0.74–1.48 d), while 3.295 d gives v_eq ~1.8 km/s; K2
  shows no ~1 d signal. Rotation section rewritten to state the tension
  honestly; cfg keeps the twice-confirmed photometric period. NOTE: ko
  mirror agent launched before this fix — its Rotation paragraph must be
  re-synced after delivery.
