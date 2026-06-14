# 3D Star Map Viewer — Checklist

Builder: `scripts/viz/build_starmap.py` → `docs/starmap.html` (self-contained, GitHub-Pages hostable).

## Builder (Python)
- [x] Korean file-header comment
- [x] Read all `db/systems/*.json`; import `to_file_slug` from `scripts/pipeline/_naming.py`
- [x] Teff → blackbody RGB (Helland approx, perceptual)
- [x] Spectral class parse (O/B/A/F/G/K/M/X; dM*→M, pulsar/WD→X)
- [x] Union-find clustering @ 0.4 ly; representative + label derivation
- [x] `binary_orbit_ref` same-cluster assertion (build fails loudly otherwise)
- [x] Marker size ladder (luminosity → spectral proxy → min)
- [x] Attach components[] + planets[] (orbital elements for AU view)
- [x] Hardcode Solar System (Sun + 8 planets, canonical elements) at origin
- [x] Emit embedded JSON payload (ly coords, 4-dp rounded, `</script>` escaped)
- [x] `--self-check` validation

## Viewer (HTML/JS, emitted)
- [x] Three.js + OrbitControls via CDN importmap
- [x] Map view: cluster sprites, Sol at origin, ICRS grid + range rings
- [x] Blackbody-colored markers, size = baked rep_radius
- [x] Click → info panel (v2 glass card): name, distance, components, planets
- [x] Hover labels + confirmed-set persistent labels (anti-clutter)
- [x] Distance filter slider; beyond-50ly toggle
- [x] Spectral legend (8 v2 chips)
- [x] System view (AU scale): fly-in + origin-rebasing, host star(s) + planet orbits + spokes + back button
- [x] Solar System explorable like other systems
- [x] KO/EN toggle (chrome strings dict)
- [x] Inline v2 design tokens

## Verify
- [x] `python3 scripts/pipeline/validate.py` (DB valid first)
- [x] `build_starmap.py --self-check` (counts: 157 files, 142 DB clusters +Sol=143, 227 planets +8=235)
- [x] Manual: `python3 -m http.server` in docs/, open, click α Cen → fly-in, Sol → 8 planets
- [x] Run `scripts/check.sh` — no NEW regressions (one pre-existing gate-5 FAIL on docs/wiki/plans__doc-tool-sprawl-audit.html, unrelated; documented in project memory)

## v2 — continuous zoom + real size + correct orbits (user follow-ups)
- [x] Drop lines from stars to the ICRS plane (+ toggle)
- [x] Continuous zoom (floating origin + log depth + zoom-to-cursor), no mode switch
- [x] Real-size bodies (R_sun / R_earth) + HTML crosshairs when zoomed
- [x] Correct Keplerian orbits (a/e/i/Ω/ω/M, focus at star) — math verified
- [x] Multi-star: components at measured ICRS epoch separation, planets around real host
- [x] Solar System with real J2000 elements (calibration showcase)
- [x] Re-verify: self-check + JS syntax + DOM/i18n + orbit-math sanity

## Commits (semantic)
- [x] builder + template + emitted viewer + Sol data
- [x] drop lines
- [x] continuous-zoom rewrite (real size, crosshairs, Keplerian orbits, multi-star)
- [ ] docs/index.html link — SKIPPED (index.html is a 2442-line generated app; starmap.html is directly reachable)

## v3 — in-flight improvements (2026-06-15)
- [x] **1. HD 219134 b/c ~perpendicular to siblings.** Fixed: no-disk fallback plane =
      mean plane of the cluster's measured-i planets (template ~line 446).
- [~] **2. AU Mic stability diverges.** Diagnosed: b,d → e≈9.2/16.9 (unbound); d ~7 mutual
      Hill radii from b, ejects on the FIRST snapshot → likely real over-packing of the
      speculative 4-planet (b,c+cand d,e) config (energy err 0.5%). Finer-dt re-run to
      confirm real vs numerical: STAB_DT_DIV=4 TRACE 1 Myr running (run.py knob). Barnard
      dt/4 running in parallel as the matched diagnostic.
- [x] **3. Apoapsis/periapsis + inclination charts** — drawStabChart(): q–Q band + inc vs t,
      cursor tracks slider; 📈 toggle in the stability panel.
- [x] **4. Focus planet from right-panel row** — planet rows wired to flyToBody().
- [x] **5. #info covers #zoomctl** — zoomctl shifts left (desktop) / up (mobile) when info open.
- [x] Rebuilt; check.sh green (gate-5 known false positive only); JS syntax OK.
- [ ] When dt/4 runs finish: pick up CSVs, rebuild viewer, commit results.
