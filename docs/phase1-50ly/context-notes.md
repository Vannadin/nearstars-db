# Phase 1 Curation — Context Notes

Append-only log of decisions made during this curation pass.

## 2026-05-19 — Session start

**Trigger:** User invoked the `nearstars-add-star` skill with "50광년 이내 행성 호스트 전체에 대한 Phase 1 자료조사".

**Baseline state (post-reset commit `1f023d0`):**
- `planets_curated.json`: empty `{}`
- `stellar_props_curated.json`: 3 entries (α Cen A, α Cen B, Barnard) — high-quality preserved
- `validate.py`: FAIL 0, WARN 282 (back to pre-bulk-fill)
- 121 planet hosts, 223 planets exist in `db/systems/*.json` from auto-fetched raw data.

**Why we are here:** Prior commit `0e42da6` bulk-filled curated entries from NASA Archive `pscomppars` (composite). Policy [[feedback-planet-curation]] requires per-paper attribution. Skill-validation test: redo it properly this time.

## Decisions

### Source table: `ps` not `pscomppars`

`fetch_planets.py` currently queries `pscomppars` (one row per planet, NASA-merged composite values). For Phase 1 we need per-paper rows from the `ps` table filtered by `default_flag=1`. NASA marks one paper as authoritative per planet — those values + that paper's bibcode become our source.

Trade-off: `ps` default may lag the latest paper. Acceptable for Phase 1 (single-source policy); Phase 2 walks the full literature anyway.

### PoC choice: 3 hosts representing the main cases

- **GJ 179** — 1 RV planet, single star, simple case.
- **GJ 581** — 3 RV planets, well-studied, tests multi-planet handling and likely has Pourbaix/Mann-style host paper.
- **GJ 1132** — 2 planets, transiting + RV, tests TEPCat interaction (build_systems applies `curated > tepcat > nasa_archive`).

### Workflow choice (after user prompt)

User picked "PoC first" not committing to a single workflow upfront. PoC will determine whether:
- ADS WebFetch per planet is feasible at 223-planet scale, or
- bibcode extraction from raw HTML reference field is sufficient with sample-based verification.

If WebFetch per planet costs ~2 minutes each, 223 × 2 = 7.5 hours — within the 5-15h policy budget. If much slower, fall back to sample verification.

### Preserve high-quality manual entries

α Cen A, α Cen B (Pourbaix & Boffin 2016), and Barnard's star (Mann 2015 / Rains 2021) already in `stellar_props_curated.json`. **Do not overwrite.** Any auto-curation step must check for existing entry before writing.

### File locations

Plan/checklist/context-notes live in `docs/phase1-50ly/` (not at repo root). This keeps the repo root clean and signals these are scoped to this curation pass, not project-wide docs.

## Surprises / discoveries (append below as work proceeds)

### 2026-05-19 — ADS pages are JS-rendered

WebFetch against `https://ui.adsabs.harvard.edu/abs/<bibcode>/abstract` (and `/exportcitation`, `/link_gateway/...`) returns empty content because the ADS UI is a JavaScript SPA. No per-bibcode WebFetch verification is feasible without an ADS API token.

**Decision:**
- bibcode (parsed from `pl_refname` HTML in NASA `ps` table) is the primary source-of-truth identifier — it's already a canonical ADS code and is structurally validatable (year-journal-volume-page-author pattern).
- DOI is recorded as best-effort via Crossref's public bibliographic search, with the constructed bibcode-derived terms (author, year, journal name, volume, page). Crossref unauthenticated API works fine.
- Where Crossref can't resolve confidently, DOI stays null. The curated entry still has full bibcode + reference attribution, which satisfies the [[feedback-planet-curation]] policy "bibcode/doi 명시".

### 2026-05-19 — build_systems.py dedup limitation

Line 643: planet curated source is only appended to `sources[]` if `doi` is present (no bibcode fallback). Hardcoded `"bibcode": None` at line 647 even when curated entry has one.

**Decision:** Extend dedup to accept `bibcode or doi`, and propagate `bibcode` from the curated entry into the `sources[]` row. Small fix, applied in this pass.

### 2026-05-19 — Method label for stellar mass/radius is heuristic, not measured

The `ps` table gives per-row `st_mass` / `st_rad` with `st_refname`, but no `st_method` field. My bulk builder hard-codes `method: "spectroscopic_calibration"` for stellar mass and `method: "evolutionary_model"` for radius — these are common-case defaults for the M-dwarf-heavy 50 ly sample, but they are not extracted from the source paper.

**Why this is acceptable for Phase 1:**
- The source attribution (bibcode + reference + DOI) IS correct — those identify the actual paper.
- The method label only governs `recommended` selection when multiple measurements exist for the same star. Phase 1 has exactly one measurement per star, so `recommended: true` is set regardless of method.
- Phase 2 escalation reads each paper individually and corrects the method label — this is one of the things Phase 2 explicitly does (per [[feedback-planet-curation]]).

**Future improvement:** add a `method_inferred: true` flag, or add a per-paper method override table for hosts where the default-flag paper is known to use a non-default method (e.g. interferometric radii).

### 2026-05-19 — Backup convention

Pre-bulk-fill backup saved at `/tmp/nearstars_backup/` (outside repo, no recursion risk).

### 2026-05-19 — URL-encoded bibcodes in `st_refname`

NASA Archive inconsistently encodes `&` in ADS URLs. Some rows ship literal `&` (e.g. `2024A&A...688A.112V` in `pl_refname`); others URL-encode it as `%26` (e.g. `2013A%26A...549A..48T` in `st_refname` for HD 40307). The original regex `[0-9A-Za-z\.\&\+\-]+` missed encoded ones, silently dropping A&A bibcodes for ~10+ hosts.

**Fix:** added `%` to the regex character class and `urllib.parse.unquote()` on the captured group. Verified all 115 unique planet bibcodes and 114 host bibcodes now parse cleanly.

### 2026-05-19 — Remaining gaps are honest gaps

After all fixes, 2 planet hosts still lack mass (GJ 163, Ross 458) and 22 lack radius. Verified via direct NASA TAP query that these hosts have **zero** rows with the missing parameter — not a parser bug, NASA Archive simply does not host the value. Phase 2 would need to look outside NASA (Mann 2015 calibrations, Gaia DR3 GSP-Phot, interferometric catalogs, etc.) for those — out of scope here.

### 2026-05-19 — `ps` default rows reveal real per-paper attribution

Sanity check on PoC hosts shows the `ps` table `default_flag=1` rows give exactly what Phase 1 needs:

| Planet | Default paper | Discovery? |
|---|---|---|
| GJ 179 b | Howard et al. 2010 | yes — discovery |
| GJ 1132 b | Xue et al. 2024 | no — reanalysis (discovery 2015) |
| GJ 1132 c | Wang et al. 2026 (preprint) | yes — discovery |
| GJ 581 b, c, e | Vincenzi et al. 2024 (or similar 2024 A&A) | no — full-system reanalysis |

NASA's default is contextual — sometimes discovery, sometimes the most-recent reanalysis. Both are valid Phase 1 sources. The earlier `pscomppars` bulk-fill obscured this; `ps` exposes it.
