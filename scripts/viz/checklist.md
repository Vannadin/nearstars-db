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

## Commits (semantic)
- [x] builder + template + emitted viewer + Sol data (one feature unit)
- [ ] docs/index.html link — SKIPPED for v1 (index.html is a 2442-line generated app; linking is out of scope, starmap.html is directly reachable)
