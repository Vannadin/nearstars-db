# Local Interstellar Medium kinematics & the heliosphere/ISM-wind viewer

Reference for `db/refs/lism_kinematics.yaml` (the 55 ly LISM census) and the 3D viewer's
**heliosphere** + **interstellar-wind** layers built from it. Korean mirror:
`ko/docs/reference/lism-kinematics.md`.

## What this is

The viewer can show, per star, the **astrosphere** (stellar-wind bubble + downwind tail)
and, across local space, the **interstellar wind field**. Both come from one curated
dataset of local cloud kinematics plus each star's space velocity. The orientation model is
validated against published astrosphere measurements.

## Dataset — `db/refs/lism_kinematics.yaml`

A bibcode-pinned census of the local interstellar medium within ~17 pc (55 ly),
independently verified (6/6 core values matched, 2026-06-16).

| block | source | content |
|---|---|---|
| `clouds` (15) | Redfield & Linsky 2008, `2008ApJ...673..283R` (Tables 16 & 18) | warm-cloud heliocentric velocity vectors = the interstellar-wind **field** |
| `astrospheres` (27) | Wood et al. 2021, `2021ApJ...915...37W` (Tables 2 & 3) | measured astrospheres — **validation + cloud assignment + wind strength**, NOT field anchors |
| `astrospheres_xray` (3) | Kislyakova et al. 2024, `2024NatAs...8..596K` | X-ray-detected astrospheres (higher mass-loss; method tension, kept separate) |
| `insitu_he` | Bzowski/McComas 2015, `2015ApJS..220...28B` | in-situ IBEX He inflow at the Sun |

**Conventions (critical).**
- Cloud `(l_deg, b_deg)` = the **downwind** direction (where the gas flows *toward*),
  Galactic, with `v0_kms > 0`. Heliocentric (solar-rest) frame. The upwind/source apex is
  the antipode `(l−180, −b)`.
- `insitu_he` is given as the **ecliptic inflow** direction — mind the frame/convention
  difference vs the cloud vectors when combining.
- `astrospheres[].v_ism_stellar_kms` is in the **stellar rest frame** (the ISM-vs-star flow
  speed an astrosphere constrains) — **not** heliocentric. Use it for cloud assignment and
  wind strength, never as a heliocentric field anchor. The cloud vectors are the field.
- 3D cloud depths are weakly constrained: sky direction is solid; `near_pc` is an **upper
  limit on the near edge**, not a position.

## Model (hybrid)

Per star, the heliocentric ISM velocity is

```
v_ISM(pos) = blend( IDW over cloud vectors by sky angular distance,  LIC vector,  w_local )
w_local = exp( -(distance_pc) / 4 )          # LIC envelops the Sun → dominates nearby
v_rel = v_star(heliocentric) − v_ISM         # nose = +v_rel (faces the wind), tail = −v_rel
```

- **IDW over cloud vectors** weights each cloud by `1/(θ² + θ0²)`, θ = angular distance from
  the star's sky direction to the cloud's region centre. `θ0 = 20°` in the model.
- **LIC-local blend** is essential and must not be removed: the Local Interstellar Cloud
  surrounds the Sun, so within ~4 pc it dominates. Pure directional IDW mis-assigned nearby
  stars (which are really inside the LIC) to distant clouds whose sky region overlapped,
  throwing heliosphere noses off by 30–90°. The blend matches Wood et al.'s within-7-pc
  LIC default.
- The Sun itself uses the in-situ IBEX He vector (`v_star = 0 → v_rel = −v_ISM`).
- Galactic→ICRS via the standard J2000 matrix (`_GAL2ICRS` in `build_starmap.py`).

**Dependency:** v_rel needs the star's *full 3D* space velocity, so a missing radial
velocity corrupts the nose direction. See [[project-nearstars-rv-gap]] — 21 RV-less stars
were curated via `MANUAL_RV` precisely so this model works.

## Validation (vs the literature)

Sun's astrosphere nose → ecliptic λ=75.8°, β=−5.2° = **IBEX upwind exactly**.

Model θ (angle of the upwind/nose to our sightline) vs Wood et al. 2021 measured θ:

| star | model | Wood | star | model | Wood |
|---|---|---|---|---|---|
| HD 219134 | 60° | 60° | α Cen | 87° | 79° |
| Barnard | 45° | 43° | τ Cet | 55° | 59° |
| 61 Vir | 96° | 98° | ε Eri | 76° | 76° |

(ε Eri only matched after its missing RV was curated — the diagnostic that found the RV gap.)
v_rel magnitudes likewise track Wood's stellar-frame V_ISM. Physically: fast stars' noses
point along their own motion; the Sun (near-rest in the LIC) points purely upwind, i.e.
opposite the downwind wind-field arrows — which is correct, not a bug.

**Cloud-to-cloud spread:** directions are fairly coherent (mean 21° from LIC; the core
clouds within ~10°), but **speeds vary >4×** (Blue/Hyades ~14 km/s … Aql/Cet ~60 km/s).

## Viewer layers

- **Heliosphere** toggle (system view): speckled teardrop astrosphere (THREE.Points) for the
  7 stellar-wind hosts + Sol. Blunt nose upwind (`wind.nose`), long downwind tail. Colour =
  radiation grade (medium = amber, high = red; pinned in `HELIO_GRADE`, a Phase-3 conclusion
  not yet a DB field), size ∝ `mass_loss_solar`. Schematic scale.
- **ISM wind** toggle (map view): a 3D lattice (8 ly step, within 50 ly) of arrows = local
  `v_ISM`, one `LineSegments` draw call. **Arrow length ∝ ISM speed** (exaggerated for
  legibility — the raw 4× speed spread is the real differentiator since directions are
  similar), **colour by dominant cloud** (+ legend). The grid samples with a **sharper IDW
  (θ0 = 12°)** than the model so cloud regions read distinct; grid-only, no model impact.

**Code:** `build_starmap.py` `load_lism` / `_ism_velocity` / `wind_for` / `heliosphere_for`
emit `wind` (per cluster) and `heliosphere` (per host); `lism` (cloud field) for the grid.
`starmap_template.html` `ismSample` (grid sampling) / `makeHeliosphere` (bubble) render them.

## Provenance / honesty

- Cloud vectors are the standard R&L 2008 set; no later work supersedes them (only refines
  morphology/columns). Astrosphere sample is small (~20 ever measured) but complete here.
- `radiation_surface` grade is a Phase-3 synthesis conclusion, pinned in code until the
  kerbalism-cfg pipeline formalizes it ([[project-nearstars-stellar-wind-kerbalism]]).
- The interstellar-wind field varies by sky direction (clouds are angular regions); the
  inner ~10 ly being uniform LIC is real (we are inside it), differences grow outward.
