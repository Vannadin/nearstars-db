# Tier 1 Batch 2 — Barnard's Star + Teegarden's Star

Full Phase 2 stellar build (8 categories) + Phase 3 synthesis, FRESH.
Crashed prep dirs (`phase2/{barnards_star,teegardens_star}/measurements.yaml`) are
QUARANTINED — not referenced during synthesis; used only as a blind cross-check oracle
after each host is done. Divergences → focused re-investigation.

## Method (per host, Tier 1 pattern)
- [ ] Online discovery for 6 missing categories (+ re-derive existing anchors)
- [ ] Pin arxiv IDs → `docs/phase3/_bib/<slug>.yaml`
- [ ] `fetch_arxiv_texts.py` → `_papers/<id>.md` cache
- [ ] Value-check all 8 categories against cache (or named VizieR catalog)
- [ ] Write full DB entry → `db/stellar_props_curated.json`
- [ ] Phase 3 synthesis → `docs/phase3/<slug>.md` + ko mirror + html
- [ ] `build_systems.py` (stage target file only; restore date churn)
- [ ] `check.sh` 6-gate pass
- [ ] DIFF vs quarantined prep measurements.yaml → re-investigate divergences

## Barnard's Star  (key: "Barnard's star", slug: barnards-star)  ✅ DONE
- [x] discovery — ESPRESSO 2024 (2410.00569) anchor + Schweitzer/Marfil/Jahandar/Toledo-Padrón
- [x] pin + fetch — _bib/barnards-star.yaml (all anchors already cached)
- [x] value-check — 8 cats cache-backed; caught radius misattribution (was "Rains 2021", a southern-TESS paper → corrected to Schweitzer 2019 R_interf 0.187 via Boyajian θ_LD)
- [x] DB build — full 8-cat entry
- [x] Phase 3 — barnards-star.md + ko + html, 41 blocks paired
- [x] systems + check — check.sh green
- [x] prep diff — fresh consistently MORE accurate; prep had attribution errors (metallicity mislabeled as Marfil, activity -5.69 misattributed). No fixes needed.

## Teegarden's Star  (key: "Teegarden's Star", slug: teegardens-star)  ✅ DONE
- [x] discovery — Schweitzer/Zechmeister baseline + fetched Dreizler 2024 (2402.00923) + Fuhrmeister 2025 activity (2504.02338)
- [x] pin + fetch — _bib/teegardens-star.yaml
- [x] value-check — Dreizler unverified mass/radius (uncached) → Schweitzer 2019 recommended; M7V: no interferometry, no Ca II HK, rotation 96.2 d (Lafarga via Dreizler)
- [x] DB build — full 8-cat entry
- [x] Phase 3 — teegardens-star.md + ko + html, 41 blocks paired
- [x] systems + check — check.sh green
- [x] prep diff — fresh consistently accurate; prep had source-attribution drift. No fixes needed.

## Post-build integrity fix
- curated.json got reindented 1-space + key-reordered by build agents → renormalized to
  indent=2 + original key order; verified ONLY Barnard + Teegarden entries differ from HEAD.
- Teegarden agent's systems-restore had reverted barnard systems → rebuilt both via build_systems,
  restored date-churn on the other 149 system files.
