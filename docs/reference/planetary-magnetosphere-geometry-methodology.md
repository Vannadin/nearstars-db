<!-- 쌍극 자기장 세기+항성풍에서 자기권 크기·모양과 방사선대 강도(다요인)를 도출해 Kerbalism 지오메트리로 매핑하는 방법(논문 근거) -->
# Planetary magnetosphere geometry grounding: standoff, belts, and Kerbalism mapping

Method reference for turning a body's **dipole field strength** (from the
[rocky](rocky-planet-dynamo-methodology.md) or [giant](planetary-dynamo-scaling.md)
dynamo recipes) into the **shape and size of its magnetosphere** — the
magnetopause standoff, the radiation-belt extent, and the belt intensity — and
for mapping those onto the fields Kerbalism actually consumes. Kerbalism carries
no physical field in Tesla; it models the radiation environment as *geometry*
(`RadiationModel` belt/pause shells) + *intensity* (`radiation_inner/outer/pause/
surface` in rad/h) + a dipole-axis direction (`geomagnetic_pole_lat/lon`). This
doc is the recipe that derives those from the physics.

**Key discipline (the reason this doc exists):** the field strength sets the
*container*, not the *contents*. Standoff and belt radii scale with the field,
but **belt intensity is governed by separate factors** — the particle source and
loss balance, capped by the Kennel–Petschek stably-trapped-flux limit — and is
*not* a function of field strength alone. Deriving belt intensity from B is the
classic mistake this doc guards against.

## Part A — geometry (shape + size) from the field

### Magnetopause standoff (Chapman–Ferraro balance)

The dayside magnetopause sits where the planetary magnetic pressure balances the
ambient ram pressure (Chapman & Ferraro 1931, `1931TeMAE..36...77C`; empirical
form Shue et al. 1997/1998, `1997JGR...102.9497S` / `1998JGR...10317691S`).
With the dipole field falling as `B(r) = B_eq·(R_p/r)³` and the Chapman–Ferraro
surface currents roughly doubling the field at the boundary (factor `f ≈ 2`):

    R_mp / R_p  =  [ f² · B_eq² / (2 μ₀ · P_ram) ]^(1/6)      (μ₀ = 4π×10⁻⁷)

where `P_ram = ρ v²` is the ram pressure of whatever flows past the body —
the **stellar wind** for a planet, or the **parent's co-rotating magnetospheric
plasma** for an embedded moon (see regimes). The `^(1/6)` power makes the standoff
very robust to input error: an 8× error in either B or P moves R_mp by only 2×.

Only the **equatorial (sub-solar) field** enters — the magnetopause nose is on the
magnetic equator. The polar field never appears here; for a pure dipole it is just
`2·B_eq` and carries no independent geometric information (it becomes informative
only for multipolar fields — see regimes).

### Belt extent

Trapped particles ride closed dipole field lines (L-shells), so the belts are
**bounded outside by the magnetopause** (`R_outer ≲ 0.6–0.8 R_mp`) and inside by
the atmosphere/surface (`R_inner ≈ 1.1–2 R_p`). A stronger field → larger standoff
→ room for belts farther out. This is the one place field strength directly sizes
the belts.

## Part B — belt intensity is multi-factor (NOT field strength)

Belt intensity is a **source − loss balance, capped by a field/plasma ceiling**:

1. **Source** sets the floor: stellar-wind capture; **CRAND** — cosmic-ray albedo
   neutron decay, the inner-belt proton source (Lenchek 1961, `1961JGR....66.4027L`);
   radial diffusion transporting particles inward (Schulz & Lanzerotti 1974,
   `1974pdrb.book.....S`); and **internal plasma sources** — a volcanic moon can
   dominate everything (Io feeds ~1 ton/s into Jupiter's belts; Bagenal 1994 Io
   torus, `1994JGR....9911043B`; Divine & Garrett 1983 Jovian model, `1983JGR....88.6889D`).
2. **Kennel–Petschek ceiling** caps it: there is a *maximum stably-trapped flux*
   above which the particles' own whistler-mode waves grow and scatter them into
   the loss cone (Kennel & Petschek 1966, `1966JGR....71....1K`, 2600+ citations).
   The limit depends on the field and cold-plasma density but is **independent of
   source strength** — so a strong-source magnetosphere (Earth, Jupiter) *saturates*
   at the K–P ceiling, and adding more source does not raise the intensity.
3. **Losses** pull it down: wave–particle scattering (chorus/hiss/EMIC; Thorne 2010,
   `2010GeoRL..3722107T`; review Ripoll 2020, `2020JGRA..12526735R`), Coulomb/
   atmospheric losses, and **absorption by moons and rings** — Saturn's belts are
   swept out by its rings/moons (Cooper 1983, `1983JGR....88.3945C`).

Consequence for derivation: **you cannot read belt intensity off B_eq.** Two
bodies with identical fields can differ by orders of magnitude in belt dose
depending on source (a volcanic moon vs none) and loss (rings/moons sweeping). The
field tells you *whether* and *where* belts trap; the source/loss/K–P balance tells
you *how intense*. Belt intensity therefore stays a **regime call with a stated
source and loss**, not a formula output.

## Part C — mapping to Kerbalism

| Physical quantity | Kerbalism field | Derivation |
|---|---|---|
| Magnetopause standoff | `pause_radius` (+ `has_pause`) | R_mp/R_p from Part A |
| Shield quality (GCR) | `radiation_pause` (negative) | deeper standoff → stronger shield |
| Belt extent | `radiation_inner`/`outer` belt radii (DB `..._belt_radius_planet_radii`) | Part A bounds |
| Belt intensity (rad/h) | `radiation_inner`/`radiation_outer` | Part B regime: source − loss, K–P-capped — **set from the stated source/loss, not from B** |
| Dipole-axis direction | `geomagnetic_pole_lat`/`lon` | = `magnetic_dipole_tilt_deg` |
| Belt existence gate | (belts present at all) | `B_eq ≳ 0.1× Earth`; below this no stable trapping |

## Validation

- **Earth**: B_eq = 31 µT, solar-wind P_ram ≈ 2 nPa → R_mp/R_p = [2²·(3.1e-5)²/(2μ₀·2e-9)]^(1/6) ≈ **9.6** — matches the observed ~10 R_E sub-solar magnetopause. Inner belt ~1.2 R_E (CRAND protons), outer ~3–7 R_E (diffusion + chorus), intensity near the K–P ceiling. ✓
- **Jupiter**: the field alone (~4.3 G equatorial) would not predict the extreme belts; the Io plasma source drives them to (and past) the K–P limit for electrons — the textbook proof that intensity ≠ f(B). ✓
- **Polyphemus** (NearStars): 170 µT vs α Cen A wind ram 0.38 nPa → R_mp ≈ **22 R_p** (the Phase 4 board's independent 23.5 R_p, same balance). ✓

## Domain of validity: regimes

1. **Dipolar intrinsic** (Earth, Pandora): standoff formula applies; belts on
   L-shells; K–P-capped if the source is strong.
2. **Multipolar intrinsic** (Uranus/Neptune, Proxima c; rocky multipolar regime
   with `Ro_ℓ > 0.12`): offset/tilted field → **asymmetric, patchy belts** and
   an offset auroral oval. The standoff formula is only approximate, and here the
   **polar-to-equatorial ratio ≠ 2** genuinely encodes the multipole content —
   the one case where carrying both fields is informative rather than redundant.
3. **Embedded moon** (a moon inside a giant's magnetosphere; **Pandora = Ganymede
   analog**, Kivelson 1996 `1996Natur.384..537K`): the standoff balances against the
   **parent's co-rotating magnetospheric plasma**, not the stellar wind; the result
   is a mini-magnetosphere. Belt dose at the moon is set by the *parent's* belt at
   that L-shell (a loss/source term for the parent), plus the moon's own shielding.
4. **Induced / no dynamo** (Venus, Io, a dead rocky planet): no intrinsic trapping,
   no belts; the interaction is ionospheric/induced and the surface dose is the
   direct wind + GCR flux.
5. **Weak/airless**: `B_eq < 0.1× Earth` → no stable belts; surface dose direct.

## Worked examples (NearStars)

- **Polyphemus**: 170 µT → R_mp ≈ 22 R_p; **all five moons orbit inside the
  magnetosphere**. Belt intensity is a *source − loss* story, not a field readout:
  Dante's extreme volcanism (~820× Io) feeds an intense inner belt (source), while
  the ring + five moons sweep particles (loss, cf. Saturn). Kerbalism gets a large
  `pause_radius`, a high inner-belt `radiation_inner`, and a strong negative
  `radiation_pause`.
- **Pandora** (embedded, Ganymede analog): own 75 µT dipole → a mini-magnetosphere
  at 3.53 R_p *inside* Polyphemus's field. It sits in the **gap between Polyphemus's
  two belts** and its own field adds shielding → the physical basis for habitability.
  Standoff is computed against Polyphemus's local plasma, not the stellar wind.
- **Proxima b** (weak dipole ~0.06–0.1 ℳ⊕): a small magnetosphere, standoff only a
  few R_p; belts marginal; surface dose dominated by the direct M-dwarf wind + flares.
- **Proxima c** (ice-giant, offset/tilted multipolar): asymmetric belts, offset oval;
  standoff formula approximate; the tilt (47°) drives off-axis aurorae.

Confidence: standoff geometry is **medium** (robust `^(1/6)` law, validated on
Earth/Polyphemus); belt intensity is **low** by nature — it depends on source and
loss terms that are themselves uncertain for exoplanets, which is exactly why it is
a documented regime call rather than a computed number.

## Citations

- **Chapman & Ferraro 1931**, Terr. Magn. Atmos. Electr. 36, 77 (`1931TeMAE..36...77C`).
  Origin of the magnetopause / pressure-balance concept.
- **Shue et al. 1997 / 1998**, JGR 102, 9497 (`1997JGR...102.9497S`) / JGR 103, 17691
  (`1998JGR...10317691S`). Empirical magnetopause standoff + shape under varying wind.
- **Kennel & Petschek 1966**, JGR 71, 1 (`1966JGR....71....1K`). The stably-trapped
  flux limit — the source-independent ceiling on belt intensity. Load-bearing for Part B.
- **Schulz & Lanzerotti 1974**, *Particle Diffusion in the Radiation Belts* (`1974pdrb.book.....S`).
  Radial-diffusion transport that populates the belts.
- **Lenchek et al. 1961**, JGR 66, 4027 (`1961JGR....66.4027L`). CRAND inner-belt source.
- **Divine & Garrett 1983**, JGR 88, 6889 (`1983JGR....88.6889D`); **Bagenal 1994**,
  JGR 99, 11043 (`1994JGR....9911043B`). Jovian radiation + the Io internal plasma
  source — the canonical "intensity set by source, not field" case.
- **Thorne 2010**, GRL 37, L22107 (`2010GeoRL..3722107T`); **Ripoll et al. 2020**,
  JGRA 125, e26735 (`2020JGRA..12526735R`). Wave–particle acceleration and loss;
  modern belt-dynamics review.
- **Cooper 1983**, JGR 88, 3945 (`1983JGR....88.3945C`). Ring/moon absorption as a
  belt loss — the Polyphemus ring + moons case.
- **Kivelson et al. 1996**, Nature 384, 537 (`1996Natur.384..537K`). Ganymede's
  embedded magnetosphere — the Pandora analog.
- **Griessmeier et al. 2004**, A&A 425, 753 (`2004A&A...425..753G`); **Vidotto et al.
  2013**, A&A 557, A67 (`2013A&A...557A..67V`). Exoplanet magnetosphere size vs
  stellar wind / tidal locking — the close-in-planet standoff application.

## Related

- [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) and
  [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) — supply the `B_eq`
  this method consumes.
- `../../.claude/skills/nearstars-phase3/references/mod-grounded-fields.md` — the
  Kerbalism `RadiationBody`/`RadiationModel` field schema this method emits into.
- `methodology-index.md` — the living index of all derived-value recipes.
