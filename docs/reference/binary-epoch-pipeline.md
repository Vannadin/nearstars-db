# Binary / Multiple Star Epoch Pipeline Reference

> Source: research across mockingbirdnest/Principia, RSS-Reborn/Sol-Configs,
> CharonSSS/RSS-Origin, USNO/GSU orb6 catalog, Gaia DR3 NSS docs, Bond+ 2017,
> Akeson+ 2021, Kervella+ 2017.
> Purpose: Compute ICRF Cartesian state vectors at `solar_system_epoch = JD 2433282.5`
> (1950-01-01 TDB) for binary/triple/multiple star systems that have no JPL HORIZONS
> data. These vectors feed Principia's `principia_initial_state` for NearStars.

---

## 1. Why Linear Back-Propagation Fails, and How Sol/RSS Avoids It

### The naive failure mode

For a tight binary (Pluto-Charon ~6.4 d, binary asteroids ~hours-days), naive
back-propagation from J2000 to the game epoch using `x_t0 = x_J2000 − v · Δt`
treats motion as a straight line. The bodies have completed dozens to thousands
of mutual orbits in that gap, so the linear estimate puts them at random
positions on the ellipse.

### Sol/RSS/RSS-Origin pattern (the correct way)

| Epoch | JD | Calendar | Role |
|---|---|---|---|
| `solar_system_epoch` | 2433282.5 | 1950-01-01 TDB | State vectors provided here |
| `game_epoch` | 2433647.5 | 1951-01-01 TDB | KSP `UT = 0` |
| J2000 | 2451545.0 | 2000-01-01 TDB | **Not used** by these mods |

Three structural choices that together eliminate the problem:

1. **Pick `solar_system_epoch` before `game_epoch`** — no back-propagation in the
   first place. Principia's symplectic n-body integrator runs *forward* from
   `solar_system_epoch` to `game_epoch`, correctly handling all orbital motion
   in between (Pluto-Charon completes ~57 orbits in that 365-day gap; the
   integrator handles it natively).

2. **List both binary components as independent absolute Cartesian vectors at
   the same epoch.** No "primary/secondary" hierarchy in `principia_initial_state`.
   Each `body { name = X; x = ...; vx = ... }` is in ICRF, evaluated at
   `solar_system_epoch`. Kopernicus' `referenceBody` only sets the visual orbit
   line; Principia ignores it for dynamics.

3. **Get the state vectors from a high-precision source at exactly the epoch.**
   For Sol the source is JPL HORIZONS. For nearby stars there is no HORIZONS,
   so the orbital elements themselves serve as the propagator — see §3-5.

### Example: Pluto-Charon in Sol-Configs (`Real_Sol-InitialState.cfg`)

```
principia_initial_state {
  game_epoch         = JD2433647.5
  solar_system_epoch = JD2433282.500000000
  body { name = Pluto
    x  = -3.969308899525761e+09 km   y  = +3.031459117686943e+09 km
    z  = +2.141687156699421e+09 km
    vx = -2.220297402287733e+00 km/s  vy = -4.555001506883357e+00 km/s
    vz = -7.354838392738812e-01 km/s }
  body { name = Charon
    x  = -3.969297506358897e+09 km   y  = +3.031467748409172e+09 km
    z  = +2.141673752024598e+09 km
    vx = -2.320549242462520e+00 km/s  vy = -4.672609388474288e+00 km/s
    vz = -8.964243487721187e-01 km/s }
}
```

Position-vector difference = **19,595 km** (matches the known Pluto-Charon
semi-major axis ~19,591 km). Relative velocity 0.223 km/s — consistent with
the circular orbital speed at that separation.

RSS-Origin binary asteroids (Patroclus-Menoetius, Logos-Zoe, Lempo triple,
Ceto-Phorcys, Eurybates-Queta) all follow the same pattern: each component
gets its own `body { }` block with absolute ICRF Cartesian state at
`JD 2433282.5`. There is no per-binary `epoch` override.

---

## 2. Generalizing to Nearby Stars: The Math

For stars there is no HORIZONS. Replace it with **the orbital elements
themselves as propagator** — evaluate the Keplerian orbit analytically at
`solar_system_epoch`.

Inputs per binary: `P, T, e, a [AU], i, ω, Ω`, parallax `π [mas]`, masses
`M_A, M_B`, target epoch `t = JD 2433282.5`.

### Frame conventions

Sky-plane orthonormal frame `(P̂, Q̂, Ŵ)`:
- `P̂` = North (toward NCP, +Dec direction)
- `Q̂` = East (+RA direction on the sky)
- `Ŵ` = away from observer (positive radial velocity direction)

- `Ω` measured east from north on the sky (counterclockwise as observed)
- `ω` measured from ascending node, in direction of orbital motion, in
  orbital plane
- `i = 0` → orbit in sky plane, motion counterclockwise as observed
- `i = 90°` → edge-on
- `i = 180°` → face-on, motion clockwise

**Node-mirror ambiguity:** without radial velocity data,
`(i, ω, Ω)` and `(180°−i, −ω, Ω+180°)` produce identical apparent
sky motion. orb6 marks the resolved case with `*` after Ω. Pick a
convention and document it.

### Pipeline (per component; run twice for A and B)

1. **Mean anomaly:**
   `M = 2π(t − T) / P` (reduce mod 2π)

2. **Eccentric anomaly:** solve `M = E − e sin E` (Markley's method, robust to `e ≈ 0.9`).

3. **True anomaly and radius:**
   ```
   ν = 2 · atan2( √(1+e) sin(E/2), √(1−e) cos(E/2) )
   r = a (1 − e cos E)
   ```

4. **Perifocal state** (orbital plane; `x̂` → periastron, `ŷ` 90° ahead):
   ```
   x_p = r cos ν                            y_p = r sin ν
   n   = 2π / P
   vx_p = −(n·a/√(1−e²)) sin E              vy_p = (n·a/√(1−e²)) · √(1−e²) cos E
   ```
   Units: `a` in AU, `P` in years → velocity in AU/yr. Multiply by 4.74047 → km/s.

5. **Thiele-Innes rotation → sky frame.** The Thiele-Innes constants
   (`A, B, F, G, C, H`) encode `ω, Ω, i, a` jointly:
   ```
   A = a ( cos ω cos Ω − sin ω sin Ω cos i)
   B = a ( cos ω sin Ω + sin ω cos Ω cos i)
   F = a (−sin ω cos Ω − cos ω sin Ω cos i)
   G = a (−sin ω sin Ω + cos ω cos Ω cos i)
   C = a · sin ω · sin i
   H = a · cos ω · sin i
   ```
   Then (position):
   ```
   ΔN = (B/a)·x_p + (G/a)·y_p     (North, +Dec)
   ΔE = (A/a)·x_p + (F/a)·y_p     (East, +RA)
   ΔW = (H/a)·x_p + (C/a)·y_p     (away from observer)
   ```
   Velocities use the **same matrix** applied to `(vx_p, vy_p)`.

6. **ICRS embed via barycenter direction.** Compute unit vectors at the
   barycenter RA/Dec `(α, δ)`:
   ```
   r̂_los = ( cos δ cos α,  cos δ sin α,  sin δ )
   N̂     = (−sin δ cos α, −sin δ sin α,  cos δ )
   Ê     = (−sin α,         cos α,        0     )
   ```
   Relative ICRS position: `r_rel = ΔN·N̂ + ΔE·Ê + ΔW·r̂_los`.
   Split by mass ratio:
   ```
   q_A = M_B / (M_A + M_B)    q_B = M_A / (M_A + M_B)
   r_A_rel = − q_A · r_rel    r_B_rel = + q_B · r_rel
   ```
   (A is on the opposite side of the barycenter from the B − A vector.)
   Velocities split identically.

7. **Barycenter propagation.** Catalog astrometry is usually at J2016.0 (Gaia
   DR3) or J1991.25 (Hipparcos). Use `astropy.coordinates.SkyCoord.apply_space_motion`
   to propagate barycenter ICRS state to `JD 2433282.5`.

8. **Final assembly:**
   ```
   r_A(t) = R_bary(t) + r_A_rel(t)        v_A(t) = V_bary(t) + v_A_rel(t)
   r_B(t) = R_bary(t) + r_B_rel(t)        v_B(t) = V_bary(t) + v_B_rel(t)
   ```

These are the HORIZONS-equivalent state vectors. Feed directly to Principia's
`principia_initial_state` body blocks.

---

## 3. Catalog Access — USNO/GSU orb6

### URLs

| Resource | URL | Notes |
|---|---|---|
| Format spec | `http://www.astro.gsu.edu/wds/orb6/orb6format.txt` | Read first |
| Main catalog (fixed-width) | `http://www.astro.gsu.edu/wds/orb6/orb6orbits.txt` | Single source of truth |
| Notes file | `http://www.astro.gsu.edu/wds/orb6/orb6notes.txt` | Per-orbit comments |
| HTML index | `http://www.astro.gsu.edu/wds/orb6.html` | Browsing only |

**VizieR mirror:** `B/orb6` (catalog "Sixth Catalog of Orbits of Visual Binary
Stars"). Main table `B/orb6/orb6orbits`. TAP endpoint
`https://tapvizier.cds.unistra.fr/TAPVizieR/tap`. Lags upstream by months; use
VizieR for bulk ADQL queries, fall back to GSU file for the latest grade-1 fits.

There is no official CSV/TSV. Parse the fixed-width with a column-spec table.

### Field map (fixed-width byte ranges, 1-indexed inclusive)

| Field | Bytes | Type | Notes |
|---|---|---|---|
| WDS designation | 1–10 | A10 | `06451-1643` |
| Discoverer code | 19–25 | A7 | `AGC  1` (Sirius) |
| HD number | 38–43 | I6 | |
| Hipparcos number | 45–50 | I6 | |
| `P` (period) | 81–91 | F11.6 | value |
| `P_unit_code` | 92 | A1 | see below |
| `a` (semi-major axis) | 105–112 | F8.4 | value |
| `a_unit_code` | 113 | A1 | see below |
| `i` (inclination) | 126–133 | F8.3 | degrees |
| `Ω` (node) | 143–150 | F8.3 | degrees |
| `Ω_node_marker` | 151 | A1 | `*` if ascending node RV-resolved |
| `T` (periastron epoch) | 162–173 | F12.6 | value |
| `T_unit_code` | 174 | A1 | see below |
| `e` (eccentricity) | 188–195 | F8.6 | `0 ≤ e < 1` |
| `ω` (arg. periastron) | 206–213 | F8.3 | degrees, of secondary unless noted |
| Equinox | 233–236 | A4 | `1900`/`1950`/`2000` typically |
| Grade | 238 | I1 | 1–5 |
| Reference code | 246–253 | A8 | bibcode-like |
| Notes flag | 255 | A1 | `N` if entry in `orb6notes.txt` |

**Critical**: byte offsets drift by ±1 between revisions. Always cross-check
against the **current** `orb6format.txt`; treat this table as a starting
template.

### Unit code tables

**Period (col 92):**

| Code | Meaning | Convert to years |
|---|---|---|
| `m` | minutes | `P / (60·24·365.25)` |
| `h` | hours | `P / (24·365.25)` |
| `d` | days | `P / 365.25` |
| `y` | years (most common) | `P` |
| `c` | centuries | `P · 100` |

**Semi-major axis (col 113):**

| Code | Meaning | Convert to arcsec |
|---|---|---|
| `a` | arcseconds (most common) | `a` |
| `m` | milliarcseconds | `a / 1000` |
| `M` | arcminutes | `a · 60` |
| `u` | microarcseconds | `a / 1e6` |

**Periastron epoch (col 174):**

| Code | Meaning | Convert to JD (TT) |
|---|---|---|
| `y` | Besselian year (e.g., `1894.130`) | `JD = 2415020.31352 + (B−1900)·365.242198781` |
| `m` | Modified Julian Date | `JD = MJD + 2400000.5` |
| `d` | truncated JD | `JD = T + 2400000` |

Note: `y` is historically Besselian, but recent (post-2010) entries sometimes
mean Julian year by `y`. If `y` and epoch is post-2000, suspect Julian and
consult the reference paper.

### Grade filter

| Grade | Meaning | NearStars policy |
|---|---|---|
| 1 | Definitive — multiple orbits, residuals well-fit | use, `phase_reliable: true` |
| 2 | Good — most of one orbit observed | use, `phase_reliable: true` |
| 3 | Reliable — half or more of orbit observed | use, `phase_reliable: true` |
| 4 | Preliminary — minority covered, P uncertain | use elements, `phase_reliable: false` |
| 5 | Indeterminate — speculative, P often assumed | **skip orbit**, treat as static CPM pair |

Cutoff: `grade ≤ 3` ⇒ trust the 1950 phase. Grade 4 ⇒ embed elements but flag.
Grade 5 ⇒ degrade to a static separation vector using observed PA/sep at the
catalog epoch.

---

## 4. Catalog Access — Gaia DR3 NSS

### Tables

| Table | Use for |
|---|---|
| `gaiadr3.nss_two_body_orbit` | **Primary table.** Full Keplerian orbits, Thiele-Innes constants, SB1/SB2/astrometric solutions |
| `gaiadr3.nss_acceleration_astro` | Acceleration solutions — no period, not usable for state vectors |
| `gaiadr3.nss_non_linear_spectro` | SB orbits without astrometric component — usually unusable alone |
| `gaiadr3.nss_vim_fl` | Variability-induced movers — exotic, skip |

Join to `gaiadr3.gaia_source` on `source_id` for parallax, PM, RV, G mag.
Cross-match to Hipparcos via `gaiadr3.hipparcos2_best_neighbour`.

### Columns of interest in `nss_two_body_orbit`

| Quantity | Column | Unit | Notes |
|---|---|---|---|
| Source ID | `source_id` | — | join key |
| Solution type | `nss_solution_type` | string | filter |
| Period | `period` | days | convert to years |
| Periastron epoch | `t_periastron` | days, offset from a Gaia-internal reference | not JD — read docs carefully |
| Eccentricity | `eccentricity` | — | |
| Inclination | `inclination` | degrees | NaN for SB1-only |
| Arg. periastron | `arg_periastron` | degrees | of secondary (ω₂) |
| Node | `nodeangle` | degrees | sometimes `node` in older docs |
| Semi-major axis (astrometric, photocenter) | `semi_major_axis` | mas | |
| RV semi-amplitude | `rv_semiamplitude_primary` / `_secondary` | km/s | SB solutions |
| Mass ratio | `mass_ratio` | — | SB2 only |
| Barycenter parallax | `parallax` | mas | use this, not `gaia_source.parallax` |
| Barycenter PM | `pmra`, `pmdec` | mas/yr | |
| Thiele-Innes | `a_thiele_innes`, `b_thiele_innes`, `f_thiele_innes`, `g_thiele_innes` | mas | A, B, F, G only — no C, H published |

Verify exact column names against the official datamodel page on every parse:
`https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_non-single_stars_tables/ssec_dm_nss_two_body_orbit.html`

### Usable `nss_solution_type` values

| `nss_solution_type` | Astrometric? | i, Ω available? | Use? |
|---|---|---|---|
| `Orbital` | yes | yes | **yes — best case** |
| `OrbitalTargetedSearch` | yes | yes | **yes** |
| `OrbitalTargetedSearchValidated` | yes | yes | **yes** |
| `AstroSpectroSB1` | yes | yes (+RV resolves node) | **yes — node mirror auto-resolved** |
| `SB1` | spectroscopic only | no | skip unless supplemented |
| `SB2` | spectroscopic only | no | skip unless supplemented |
| `EclipsingBinary` | no | partial | skip for orbit |
| `Acceleration7/9` | no | no | **skip** |
| `FirstDegreeTrendSB1` | no | no | **skip** |

```sql
WHERE nss_solution_type IN (
  'Orbital',
  'OrbitalTargetedSearch',
  'OrbitalTargetedSearchValidated',
  'AstroSpectroSB1'
)
```

### Filling in C, H (Gaia publishes only A, B, F, G)

**Pathway 1 — Read Campbell columns directly (preferred).**
For `Orbital`/`OrbitalTargetedSearch` rows, Gaia DR3 publishes
`inclination`, `arg_periastron`, `nodeangle` alongside the Thiele-Innes
constants. Use them directly, then:
```
C = a · sin(ω) · sin(i)
H = a · cos(ω) · sin(i)
```

**Pathway 2 — Recover Campbell from Thiele-Innes (fallback).**
When Campbell columns are NULL:
```
u = (A² + B² + F² + G²) / 2
v = A·G − B·F
ω+Ω = atan2( B − F,  A + G)
ω−Ω = atan2(−B − F,  A − G)
ω   = ((ω+Ω) + (ω−Ω)) / 2
Ω   = ((ω+Ω) − (ω−Ω)) / 2
a   = sqrt( u + sqrt(u² − v²) )
i   = 2 · atan( sqrt( (u − sqrt(u²−v²)) / (u + sqrt(u²−v²)) ) )
```
Then compute C, H from the formula above.

The `ω − Ω` quadrant in Pathway 2 is the node-mirror ambiguity. Gaia's
Campbell columns (when published) have already made a choice — trust it
unless cross-checking with another source suggests otherwise.

---

## 5. Per-System Canonical Papers (Override orb6)

For marquee nearby systems, use the dedicated paper rather than orb6:

| System | Canonical reference |
|---|---|
| α Cen AB | Akeson et al. 2021, AJ 162, 14 |
| Proxima → α Cen barycenter | Kervella, Thévenin, Lovis 2017, A&A 598 L7 |
| Sirius AB | Bond et al. 2017, ApJ 840, 70 |
| Procyon AB | Bond et al. 2015, ApJ 813, 106 |
| 61 Cyg AB | Malkov et al. 2012 / Gorshanov et al. 2006 |
| Luyten 726-8 (UV + BL Cet) | Geyer 1975, refined Kervella 2016 |

Always cite the source in the DB entry's `source` field
(e.g., `"akeson_2021"`, `"orb6:grade=1"`, `"gaia_dr3_nss:Orbital"`).

---

## 6. Triple-System Handling

### Hierarchical Jacobi decomposition

A stable triple is always hierarchical. Decompose into two independent Kepler
problems:

```
          (AB+C barycenter, "G")
                  |
           +------+------+
           |             |
        (AB barycenter)   C
          "g"   |
            +---+---+
            |       |
            A       B
```

- **Inner orbit:** A and B around `g` (the AB barycenter). Mass ratio uses M_A, M_B.
- **Outer orbit:** `g` (treated as point mass `M_A + M_B`) and C around `G`. Mass ratio uses `M_AB = M_A + M_B` vs `M_C`.

### Composition

```
r_inner = (B − A) vector from Kepler/T-I pipeline on inner elements
r_outer = (C − g) vector from Kepler/T-I pipeline on outer elements

r_A_from_g = − (M_B  / M_AB)    · r_inner
r_B_from_g = + (M_A  / M_AB)    · r_inner
r_g_from_G = − (M_C  / M_total) · r_outer
r_C_from_G = + (M_AB / M_total) · r_outer

r_A_ICRS = R_bary + r_g_from_G + r_A_from_g
r_B_ICRS = R_bary + r_g_from_G + r_B_from_g
r_C_ICRS = R_bary + r_C_from_G
```

Velocities compose identically.

### Wide CPM companions (no orbit fit)

For wide common-proper-motion companions (typical ρ > 5″, P > 1000 yr) with
no fitted orbit:

- Skip orbital motion at the JD 2433282.5 epoch.
- Place at fixed offset from inner system, derived from observed `(ρ, θ)` at
  the catalog reference epoch.
- Share systemic proper motion and radial velocity with the primary.
- Flag `orbit_type: "static_cpm"`, mark LOS component as guess.

```python
sep_au  = rho_arcsec * (1000.0 / parallax_mas)   # small-angle, parsec definition
delta_N =  sep_au * cos(radians(theta_deg))
delta_E =  sep_au * sin(radians(theta_deg))
delta_W =  0.0   # unknown
```

### Schema reference

The full `binary_orbits.json` schema — component / orbit field tables,
conditional-required logic (`primary` vs `primary_is_barycenter_of`,
`a_arcsec` vs `a_au`, `T_jd_tt` when `phase_reliable=true`), hybrid
astrometry storage (component-level `astrometry_source` rules +
system-level `barycenter_astrometry` block, no per-component coords
in the file) — is defined in
[`methodology.md §Multiple-System Epoch`](methodology.md#multiple-system-epoch).
The math in this document produces the values that schema requires.

---

## 7. Code Snippets

### 7a. Kepler solver (PyAstronomy MarkleyKESolver)

```python
from PyAstronomy.pyasl import MarkleyKESolver
solver = MarkleyKESolver()  # closed-form Padé + Halley step; robust to e → 1
# Input:  M in radians, e in [0, 1)
# Output: E in radians, same branch as M
E = solver.getE(M, e)   # NOT solver.solveKE — that's an older API name
# For e = 0.9, M = 1.0 rad: returns E ≈ 1.8607 rad in microseconds
```

Markley is non-iterative and stable for `e > 0.8`. For `e ≥ 0.99` switch to a
universal-variable formulation; orb6 has essentially no such systems.

### 7b. Thiele-Innes rotation (numpy)

```python
import numpy as np

def perifocal_to_sky(x_p, y_p, vx_p, vy_p, A, B, F, G, C, H):
    """Perifocal (AU, AU/yr) -> sky-frame (N, E, W) relative offset and velocity.
       A..H here are dimensionless per-unit-a Thiele-Innes constants.
       Row convention: B,G -> N ; A,F -> E ; H,C -> W (line of sight).
    """
    M = np.array([[B, G],   # North
                  [A, F],   # East
                  [H, C]])  # away from observer
    pos = M @ np.array([x_p,  y_p])
    vel = M @ np.array([vx_p, vy_p])
    return pos, vel
```

The transposed-M bug is the single most common silent error in binary-orbit
code. Always cross-check against the source paper's labeling of which
constants are East-coefficients vs North-coefficients.

### 7c. Barycenter propagation (astropy)

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time

bary_now = SkyCoord(
    ra            = 219.9020833 * u.deg,
    dec           = -60.8339722 * u.deg,
    distance      = (1000.0 / 750.81) * u.pc,   # parallax_mas -> pc
    pm_ra_cosdec  = -3679.25 * u.mas / u.yr,    # Gaia pmra is already cos(δ)-multiplied
    pm_dec        =   473.67 * u.mas / u.yr,
    radial_velocity = -22.39 * u.km / u.s,
    obstime       = Time('J2016.0', scale='tcb'),   # Gaia DR3 ref epoch is TCB
    frame         = 'icrs',
)
bary_1950 = bary_now.apply_space_motion(new_obstime=Time('1950-01-01', scale='tdb'))
# bary_1950.cartesian.xyz  -> ICRS position
# bary_1950.velocity       -> ICRS velocity
```

### 7d. Angular separation → AU via parallax

```python
def arcsec_sep_to_au(sep_arcsec, parallax_mas):
    """Exact by parsec definition: 1 pc * 1 arcsec = 1 AU."""
    distance_pc = 1000.0 / parallax_mas
    return sep_arcsec * distance_pc

def gaia_ti_mas_to_au(ti_mas, parallax_mas):
    """Thiele-Innes constants in mas / parallax in mas -> AU directly."""
    return ti_mas / parallax_mas
```

### 7e. Node mirror resolution via RV

```python
import numpy as np
from PyAstronomy.pyasl import MarkleyKESolver

def predicted_rv_secondary(t, T, P, e, omega_deg, K2_kms, gamma_kms):
    """SB1 secondary RV at time t."""
    M = (2 * np.pi * (t - T) / P) % (2 * np.pi)
    E = MarkleyKESolver().getE(M, e)
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                        np.sqrt(1 - e) * np.cos(E / 2))
    w = np.radians(omega_deg)
    return gamma_kms + K2_kms * (np.cos(nu + w) + e * np.cos(w))

def resolve_node_mirror(t_rv, rv_obs, T, P, e, i_deg, omega_deg, Omega_deg,
                        K2_kms, gamma_kms):
    rv_A = predicted_rv_secondary(t_rv, T, P, e,  omega_deg,        K2_kms, gamma_kms)
    rv_B = predicted_rv_secondary(t_rv, T, P, e, (-omega_deg) % 360, K2_kms, gamma_kms)
    if abs(rv_A - rv_obs) <= abs(rv_B - rv_obs):
        return i_deg, omega_deg, Omega_deg, "primary_branch"
    return 180 - i_deg, (-omega_deg) % 360, (Omega_deg + 180) % 360, "mirror_branch"
```

K2 stays positive by convention across both branches — only ω flips
(carrying the phase change), and i flips with it.

---

## 8. Barycenter Astrometry — Decision Tree

Three options:
- **(A)** Primary's single-component astrometry + Kepler offset
- **(B)** Mass-weighted average of both components' single-component astrometry
- **(C)** Dedicated barycentric solution (Hipparcos multi-star annex, Gaia NSS)

```
Is there a Gaia DR3 NSS Orbital / AstroSpectroSB1 row?
├── YES → Option C: use nss_two_body_orbit.parallax / pmra / pmdec
│         (barycentric by construction)
│
└── NO  → Is the pair resolved (separation > Gaia resolution ≈ 0.4–1″)?
          ├── YES, both have full Gaia 5-param solutions
          │     → Option B: mass-weighted average
          │         barycenter_PM      = (M_A·PM_A + M_B·PM_B) / (M_A + M_B)
          │         barycenter_parallax = weighted average (usually within σ)
          │       Note: for P < 20 yr, each component's PM contains its
          │       orbital tangent velocity. Mass-weighted averaging CANCELS
          │       this — Option B is correct, not a hack.
          │
          └── NO (unresolved, single Gaia row)
                ├── Hipparcos multi-star solution available
                │   (DMSA flag 'C', 'O', 'V', 'X')
                │   └── YES → Option C': use Hipparcos barycentric solution;
                │             update PM from Gaia DR3 for the long-baseline
                │             precision if possible
                │
                └── NO → Option A with caveats: Gaia gaia_source astrometry
                        is a PHOTOCENTER solution. Photocenter wobble matters
                        when:
                          • P < 10 yr  AND  flux ratio < 10  AND  a_photo > 0.1 mas
                          • Adds coherent ~0.1–1 mas oscillation in PM/parallax
                          • Position error at 1950: up to (PM_error · 66 yr)
                            ≈ 60 mas for the nearest unresolved pairs
                        Flag astrometry_quality: "photocenter_contaminated".
```

Notes:
- **Photocenter wobble vs Gaia mission length (~5–10 yr):** matters when
  `P < mission`. For `5 < P < 30 yr` it leaks into PM/parallax. For `P > 50 yr`
  it appears as a slow drift absorbed into PM (biased but not detectable).
- **Resolved pairs (>2″):** each component has its own Gaia 5-param solution.
  Use Option B; per-component wobble is much smaller than PM error.
- **Hipparcos multi-star annex (1997):** 8542 systems with field H59 flag
  `C/O/V/X`; cross-reference via HIP number from orb6.
- **Default when nothing is known:** Option B if resolved, Option A flagged
  as photocenter-contaminated if not.

---

## 9. Worked Example 1 — α Centauri AB at JD 2433282.5

Elements (Akeson et al. 2021, ICRS J2000.0):

| Element | Value |
|---|---|
| P | 79.762 yr |
| T | 1955.564 (Besselian) → JD 2435291.6 |
| e | 0.51947 |
| a | 17.4930 arcsec |
| π | 750.81 mas → d = 1.3319 pc → a = 23.300 AU |
| i | 79.2430° |
| ω | 231.519° |
| Ω | 205.073° |
| M_A | 1.0788 M☉ |
| M_B | 0.9092 M☉ |
| q_A | M_B/M_tot = 0.4574 |
| q_B | M_A/M_tot = 0.5426 |

Barycenter at J2019.5 (ICRS): α = 14h 39m 36.494s, δ = −60° 50′ 02.37″,
μ_α* = −3639.95 mas/yr, μ_δ = +700.40 mas/yr, v_r = −22.3796 km/s.

### Steps at `t = JD 2433282.5`

```
1. Δt_yr = (2433282.5 − 2435291.6) / 365.25 = −5.500 yr
2. M  = 2π · (−5.500 / 79.762) = −0.4334 rad   (≡ 335.18°)
3. E  ≈ −0.7728 rad        (Markley solver)
4. ν  ≈ −1.1782 rad        r = 23.300·(1 − 0.51947·cos(−0.7728)) = 14.61 AU
5. Perifocal:
     n = 2π / 79.762 = 0.07879 rad/yr
     n·a / √(1−e²) = 2.1487 AU/yr
     x_p =  +5.587 AU      y_p = −13.50 AU
     vx_p = +1.985 AU/yr   vy_p = +1.932 AU/yr
6. Thiele-Innes (per-unit-a):
     A/a = +0.5021   F/a = −0.7578
     B/a = +0.3971   G/a = −0.4377
     C/a = −0.7683   H/a = −0.6121
7. Sky-frame relative (B − A):
     ΔN = +13.04 AU    vN = −0.467 AU/yr
     ΔE =  +8.13 AU    vE = −0.058 AU/yr
     ΔW =  +3.97 AU    vW = −2.708 AU/yr
   → B is ~4 AU behind A along the line of sight at 1950-01-01.
```

Embed in ICRS by:
- propagating barycenter astrometry from J2019.5 to JD 2433282.5 via
  `SkyCoord.apply_space_motion` (radial motion shifts d by ~328 AU);
- building `N̂, Ê, r̂_los` at the 1950 RA/Dec;
- splitting by `q_A, q_B` and adding `R_bary, V_bary`.

---

## 10. Worked Example 2 — Sirius AB at JD 2433282.5

Elements (Bond et al. 2017, Table 5; ICRS J2000.0):

| Element | Value |
|---|---|
| P | 50.1284 yr |
| T | 1994.5715 (Besselian) — **note: the often-quoted "1894.13" is one period earlier; same phase** |
| e | 0.59142 |
| a | 7.4957 arcsec |
| π | 379.21 mas → d = 2.6371 pc → a = 19.766 AU |
| i | 136.336° |
| ω | 149.161° (J2000) |
| Ω | 45.400° (J2000) |
| M_A | 2.063 M☉ |
| M_B | 1.018 M☉ |

### Steps at `t = JD 2433282.5` (using T = 1894.13 as the user-supplied reference; same phase as T = 1994.5715)

```
1. Δt = 55.871 yr     N_periods = 55.871 / 50.1284 = 1.1146
   Phase = 0.1146 past periastron
2. M = 2π · 0.1146 = 0.7200 rad   (≈ 41.25°)
3. Newton iteration: E₀ = 1.1098, E₁ = 1.2994, E₂ = 1.2882
   E ≈ 1.2881 rad   (73.81°)
4. ν = 2 · atan2( √1.59142·sin(0.6441), √0.40858·cos(0.6441) )
      = 2 · atan2( 0.7577, 0.5111 )
      = 1.9526 rad   (111.87°)
   r/a = 1 − e·cos E = 1 − 0.59142·0.2785 = 0.8353
   r = 0.8353 · 19.766 = 16.510 AU
5. Perifocal:
     n = 2π/50.1284 = 0.12534 rad/yr
     n·a/√(1−e²) = 3.0728 AU/yr,  with √(1−e²) = 0.8061
     x_p = 16.510 · cos(1.9526) = −6.155 AU
     y_p = 16.510 · sin(1.9526) = +15.321 AU
     vx_p = −3.0728 · sin(1.2881) = −2.953 AU/yr
     vy_p = +2.4773 · cos(1.2881) = +0.6872 AU/yr
6. Thiele-Innes (per-unit-a, with ω=149.161°, Ω=45.400°, i=136.336°):
     cω = −0.8587   sω = +0.5125
     cΩ = +0.7022   sΩ = +0.7120
     ci = −0.7235   si = +0.6903

     A/a = cω·cΩ − sω·sΩ·ci = −0.3390
     B/a = cω·sΩ + sω·cΩ·ci = −0.8718
     F/a = −sω·cΩ − cω·sΩ·ci = −0.8023
     G/a = −sω·sΩ + cω·cΩ·ci = +0.0714
     C/a = sω·si = +0.3538
     H/a = cω·si = −0.5928
7. Sky-frame relative (B − A):
     ΔN = (B/a)·x_p + (G/a)·y_p
        = (−0.8718)(−6.155) + (0.0714)(15.321) = +5.366 + 1.094 = +6.46 AU
     ΔE = (A/a)·x_p + (F/a)·y_p
        = (−0.3390)(−6.155) + (−0.8023)(15.321) = +2.087 − 12.292 = −10.20 AU
     ΔW = (H/a)·x_p + (C/a)·y_p
        = (−0.5928)(−6.155) + (0.3538)(15.321) = +3.649 + 5.421 = +9.07 AU

     vN = (−0.8718)(−2.953) + (0.0714)(0.6872)  = +2.624 AU/yr
     vE = (−0.3390)(−2.953) + (−0.8023)(0.6872) = +0.450 AU/yr
     vW = (−0.5928)(−2.953) + (0.3538)(0.6872)  = +1.994 AU/yr

   |Δr| = √(6.46² + 10.20² + 9.07²) ≈ 15.10 AU
8. Sanity check:
   T = 1894.13 puts periastron passages at 1894.13 + n·50.13. Nearest
   passages: 1944.26 and 1994.39. So 1950-01-01 is ~5.74 yr PAST the
   1944 periastron — early post-periastron expansion. Computed r = 16.5 AU
   matches this regime.
   (Caveat: the commonly cited "Sirius B disappeared into A's glare in
   the 1940s" refers to PROJECTED angular separation, which shrinks near
   periastron with i = 136° even as r grows. Physical separation in the
   mid-1940s was ~9 AU, growing to ~31 AU by apastron c. 1969.)
   Using Bond+ 2017's T = 1994.5715 directly: phase
   = (1950.0 − 1994.5715)/50.1284 = −0.889 ≡ 0.111 (mod 1) — same answer.
```

Rounding budget:
- Step 3 Newton truncation: ~10⁻⁴ rad → ~0.01 AU
- Step 6 trig truncation: ~10⁻⁴ → ~0.05 AU on position
- Total numerical noise ~0.1 AU. Element uncertainty (a ±0.03%, T ±0.006 yr)
  dominates only near periastron.

---

## 11. Known Pitfalls

### Time-scale and epoch conventions
- **Besselian vs Julian year:** `B → JD = 2415020.31352 + (B−1900)·365.242198781`;
  `J → JD = 2451545.0 + (J−2000)·365.25`. Agree at 1900, differ ~0.013 d by
  2000, ~0.03 d by 1894.
- **`y` ambiguity in orb6:** historically Besselian, post-2010 entries
  sometimes Julian. Consult reference paper if borderline.
- **TDB vs UTC for JD epochs:** TT − UTC = +29 s in 1950, +69 s in 2025.
  Negligible for orbit phase but always set `scale=` explicitly in astropy
  (`Time(..., scale='tdb')`); never default.
- **Equinox of Ω, ω:** pre-1990 orb6 entries often B1950; modern ones J2000;
  Gaia NSS effectively ICRS. B1950→J2000 precession rotates Ω by ~0.64°.
  Always precess to J2000/ICRS and store original equinox as metadata.
- **Gaia reference epoch:** DR3 = J2016.0 (TCB), DR2 = J2015.5, DR1 = J2015.0;
  Hipparcos = J1991.25. Read from catalog metadata, never hardcode.

### Astrometric / dynamical
- **Inclination convention:** visual binaries and astrometric solutions use
  `i ∈ [0°, 180°]` (prograde vs retrograde distinguishable). SB-only orbits
  often use `i ∈ [0°, 90°]` (no retrograde sense — that's the node mirror).
  Never normalize i into [0°, 90°] — that loses information.
- **Proper motion on a great circle, not a plane:** linear extrapolation
  `α + μ·t` has error `~μ²·t² / sin δ`. For Sirius (δ ≈ −16.7°,
  μ_α ≈ 546 mas/yr) over 66 yr: ~1.4″. Visible. Use
  `SkyCoord.apply_space_motion`, never roll your own for Δt > 10 yr.
  Near the poles (Polaris) the linear form is meaningless; unit-vector
  propagation is required.
- **Light-time and aberration:** annual aberration baked into Gaia ICRS already.
  Light-time across the orbit: Sirius (a = 20 AU) is 3 h / 50 yr =
  7·10⁻⁶ phase. Negligible.

### Convention pitfalls
- **ω₂ vs ω₁:** orb6, Gaia DR3 NSS, Hipparcos DMSA all publish argument of
  periastron of the **secondary** (ω₂). Some older SB-focused papers publish
  ω₁ = ω₂ + 180°. When in doubt, document and trust orb6.
- **Mass ratio convention:** A = brighter primary, B = secondary. `q = M_B/M_A`,
  with `0 < q ≤ 1`. Sirius A (main sequence) is brighter than Sirius B (WD),
  so the labeling is straightforward for nearby systems.
- **Gaia NSS `inclination` units:** degrees, not radians. Same convention as
  visual binaries (`i=0` face-on, `i=90` edge-on). Verify against the
  datamodel page — TAP unit metadata is sometimes incorrect.

### Floating-point and numerics
- `atan2(y, x)` always; never `atan(y/x)` — quadrants matter in ν conversion.
- Wrap M, E, ν to a single convention ([0, 2π) or [−π, π)) consistently.
- Near-circular orbits (e < 10⁻³): ω becomes ill-defined, T degenerate with
  phase. Switch to non-singular elements (h = e·sin(ω+Ω), k = e·cos(ω+Ω),
  λ = M+ω+Ω). orb6 won't publish e < 0.01 anyway; Gaia NSS occasionally does.
- High eccentricity (e > 0.95): Newton-Raphson oscillates. Markley solver
  handles it; don't roll your own.

### Position vs orbit equinox
Even if (Ω, ω) are precessed to J2000, the star's (α, δ) might be at a
different equinox (B1950 in old Hipparcos-era papers). Mixing B1950 RA/Dec
with J2000 (Ω, ω) gives an orbit rotated by 0.64° but anchored at the wrong
sky location. Always precess everything to ICRS/J2000 in the DB; store
original equinox as metadata; never mix.

---

## 12. Pipeline Summary

```
1.  Load orbital elements (orb6 / per-system paper / Gaia DR3 NSS).
2.  Normalize units: a→AU (via parallax), P→years, angles→radians,
    T→JD_TDB. Validate grade (≥3 for use-as-is, 4 flagged, 5 → static).
3.  Decide ascending-node convention (orb6 '*' marker / paper / RV).
4.  Compute Thiele-Innes (A,B,F,G,C,H) per unit a — STORE PER SYSTEM.
5.  At t=JD 2433282.5: solve Kepler → (x_p, y_p, vx_p, vy_p).
6.  Rotate via Thiele-Innes → (ΔN, ΔE, ΔW) position, (vN, vE, vW) velocity.
7.  Build (N̂, Ê, r̂_los) at the barycenter (α, δ) at epoch t.
8.  Split by mass ratio → (r_A_rel, r_B_rel, v_A_rel, v_B_rel) in ICRS.
9.  Propagate barycenter from catalog ref epoch → t via
    SkyCoord.apply_space_motion → R_bary(t), V_bary(t).
10. r_X(t) = R_bary(t) + r_X_rel(t);   v_X(t) = V_bary(t) + v_X_rel(t).
11. Write to binary_orbits.json (or equivalent) as ICRS Cartesian at
    solar_system_epoch = JD 2433282.5.
12. CFG build step emits `body { name = X; x = ...; vx = ... }` blocks
    in principia_initial_state.
```

This replicates the HORIZONS "exact state at epoch" capability for non-solar
system bodies. No interpolation, no n-body back-propagation: the orbital fit
**is** the propagator.

---

## 13. Sources

- mockingbirdnest/Principia repo, `astronomy/sol_initial_state_jd_2433282_500000000.cfg`
- RSS-Reborn/Sol-Configs: `Patches/Principia/Real_Sol-InitialState.cfg`
- CharonSSS/RSS-Origin: `principia@*.cfg` (Patroclus, Lempo, Logos, Ceto, Eurybates, Ida)
- USNO Sixth Catalog of Orbits of Visual Binary Stars: `http://www.astro.gsu.edu/wds/orb6.html`
  - Format: `orb6format.txt`. Data: `orb6orbits.txt`. VizieR: `B/orb6`.
- Gaia DR3 NSS datamodel:
  `https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_non-single_stars_tables/ssec_dm_nss_two_body_orbit.html`
- Akeson et al. 2021, AJ 162, 14 (α Cen AB precision orbit)
- Bond et al. 2017, ApJ 840, 70 (Sirius AB)
- Bond et al. 2015, ApJ 813, 106 (Procyon AB)
- Kervella, Thévenin, Lovis 2017, A&A 598 L7 (Proxima orbit)
- Pourbaix 1995, BABel 152, 55 (Thiele-Innes formalism)
- Halbwachs 2009, MNRAS 394, 1075 (perspective effects)
- orbitize reference implementation: `http://orbitize.info/en/latest/_modules/orbitize/kepler.html`
- PyAstronomy MarkleyKESolver:
  `https://pyastronomy.readthedocs.io/en/latest/pyaslDoc/aslDoc/keplerOrbitAPI.html`
