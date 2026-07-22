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
| Magnetopause shield | `radiation_pause` (small negative) | the shield comes from *having* a pause at `pause_radius`; the value itself is small and stock-uniform (~−0.01), NOT scaled to standoff |
| Belt extent | `inner_dist`/`inner_radius`, `outer_dist`/`outer_radius` (body radii) | Part A bounds |
| Belt intensity (rad/h) | `radiation_inner`/`radiation_outer` | Part B regime: source − loss, K–P-capped — **set from the stated source/loss, not from B** |
| Dipole-axis direction | `geomagnetic_pole_lat`/`lon` | = `magnetic_dipole_tilt_deg` |
| Belt existence gate | (belts present at all) | `B_eq ≳ 0.1× Earth`; below this no stable trapping |

### The RadiationModel geometry (grounded in Kerbalism source)

Kerbalism models each field as a signed-distance shape, all lengths **in body radii**
([Kerbalism modding docs](https://kerbalism.readthedocs.io/en/latest/modders/radiation.html);
stock values from `KerbalismConfig/System/Radiation.cfg`):

- **inner belt** = a torus: `inner_dist` (major radius = ring-center distance) + `inner_radius` (section radius).
- **outer belt** = a hollow shell (a torus minus a slightly smaller one, faded by `outer_border_start/end`): `outer_dist` + `outer_radius`.
- **magnetopause** = a sphere `pause_radius`, deformable toward the star (`*_compression`) and into a tail (`*_extension`); `*_deform`/`*_quality` are cosmetic.
- Intensities + axis live on the `RadiationBody`: `radiation_inner/outer/pause` (rad/h, pause negative), `geomagnetic_pole_lat/lon`.

**`inner` and `outer` are always two tori with `inner_dist < outer_dist`** — but whether
they *look* like two separated Van Allen belts or one nested/concentric structure is set
by the section-radius-vs-spacing ratio:

| Stock model | inner `dist / radius` | outer `dist / radius` | `pause_radius` | `radiation_inner / outer / pause` | look |
|---|---|---|---|---|---|
| **earth** (Kerbin) | 0.81 / 0.70 | 2.63 / 2.48 | 13.65 | 10.4 / 2.2 / −0.011 | two **separated** belts |
| **giant** (Jool) | 2.2 / 1.0 | 6.0 / 6.0 | 60 | 200 / 11 / −0.012 | outer section = its radius → hole closes → **concentric** look enclosing the inner |

So the body-class choice is: **rocky / Earth-like → `earth`-style (distinct tori, separated
belts); giant → `giant`-style (fat overlapping tori, concentric look).** Both are just
inner+outer with different `dist/radius` ratios — the "concentric vs separated" question that
recurs in NearStars is a rendering consequence, not two different mechanisms.

Two stock-anchored facts that correct earlier NearStars drafts:
- `radiation_pause` is **small and roughly body-independent in stock** (Kerbin −0.011, Jool
  −0.012) — it is *not* a large standoff-scaled shield term. (An earlier Pandora draft used
  −3.8, a Promised-Worlds pack tuning; regrounded to the ~−0.01 stock scale.)
- `geomagnetic_pole_lat ≈ 80` for an Earth-tilt body matches stock Kerbin (80.37).

### Sol / RSS anchors (NearStars is Sol-based — prefer these over stock)

NearStars runs at Sol real-scale, so the **ROKerbalism / RSS** radiation config is the
better anchor than stock Kerbin/Jool (ROKerbalism `KerbalismConfig/System/Radiation.cfg`
+ KerbalismConfig `Support/RSS.cfg`):

| Body | geometry (R_body) | `radiation_inner / outer / pause` | note |
|---|---|---|---|
| Sun | heliopause, `pause_radius` 1000 | surface 46.5, cycle 11 yr | dose source + GCR shield |
| Earth | inner 0.81/0.70, outer 2.63/2.48, pause 15 | 10.4 / 2.2 / **−0.010**, pole 80.4 | **separated** belts |
| Jupiter | inner 6.0/1.0, outer 6.5/6.5, pause 60 | 300 / 50 / **−0.010**, pole −81 | **concentric** (inner at the outer shell's inner edge) |
| Saturn | outer 7/7 only (**no inner**), pause 20 | — / 150 / **−0.011** | inner belt absent — **rings sweep it** (Cooper 1983) |
| Uranus | offset dipole | 75 / 4 / −0.010, pole 31, `geomagnetic_offset` 0.3 | tilted/offset |
| Neptune | offset dipole | 39 / 2.5 / −0.007, pole 43, `geomagnetic_offset` 0.55 | strongly offset |

Three facts this settles for NearStars:
1. **`radiation_pause` ≈ −0.01 for every body** (Earth/Jupiter −0.010, Saturn −0.011,
   Neptune −0.007) — confirms it is a small body-independent term, not a shield
   magnitude. (Pandora's −0.01 is right.)
2. **Gas giant → concentric, rocky → separated** is real-body, not just stock KSP.
3. **A ringed / heavily-mooned giant loses its inner belt** — Saturn is modeled with
   *outer only, no inner*, the ring-absorption loss (Part D) baked straight into the
   cfg. **So Saturn, not Jupiter, is the template for Polyphemus** (ring + five moons).
   `geomagnetic_offset` (Uranus 0.3, Neptune 0.55) is the handle for the offset/
   multipolar dipoles of ice giants like Proxima c.

## Part D — moon ↔ parent interaction (embedded magnetospheres)

A moon orbiting *inside* a giant's magnetosphere is a common NearStars case (every
Polyphemus moon). It is not a scaled-down planet: three couplings dominate, all
radiation-relevant, and the moon's *own* field is a minor player.

1. **The moon lives inside the parent's belt.** The radiation the moon's surface
   sees is overwhelmingly the *parent's* trapped flux at the moon's L-shell — not
   anything the moon generates. So the first question is always *where in the
   parent's belt does the moon sit* (orbital distance in R_parent, bounded by the
   parent standoff from Part A): a moon deep in the belt is baked (Io; Dante,
   1.54 R_p), a moon in a belt gap is spared (Pandora, 3.53 R_p). The moon's own
   field only *modulates* this ambient dose by shielding.

2. **The moon is a loss (or source) term for the parent's belt.** A solid moon or
   ring **absorbs** trapped particles sweeping past it, carving depletion corridors
   and, for a whole moon+ring system, pulling the parent's belt well *below* its
   Kennel–Petschek ceiling (Cooper 1983 — Saturn is the archetype, its rings and
   moons gut its belts). This is why a heavily-mooned giant is **not** automatically
   Jupiter-class: the moons + ring are a large distributed sink. Conversely a
   volcanic moon is a **source** — Io / Dante feed a plasma torus that drives the
   belt up toward the ceiling (Bagenal 1994). The same moon can be both: Dante
   feeds the torus globally while sweeping particles locally.

3. **The moon's own mini-magnetosphere** (only if it has an intrinsic dynamo).
   Its standoff balances the moon's field against the **parent's co-rotating
   magnetospheric plasma**, not the stellar wind — Part A with `P_ram` = the parent
   plasma. Ganymede is the sole Solar-System example (Kivelson 1996). Properties:
   - **Small and partly open.** The parent's field threads the moon; where the
     moon's field is only a few× the local parent field, field lines reconnect and
     the magnetosphere leaks at the poles (Ganymede: ~6× local Jovian field →
     standoff ~2 R_G, open polar caps). A stronger moon field → a larger, less-leaky
     mini-magnetosphere.
   - **Own belt is weak and source-starved.** The closed-field trapping volume is
     tiny and the only sources are inward diffusion from the parent's belt (low if
     the moon is in a gap) + CRAND from any atmosphere. The own belt therefore rarely
     reaches its K–P ceiling — it is **source-limited, not field-limited**, and is a
     single narrow belt (no room for Earth's two).
   - **Net role = shield, not generator.** The mini-magnetosphere's main effect on
     surface habitability is deflecting the *parent's* belt flux; the particles it
     does trap and precipitate feed aurorae rather than baking the ground. An
     intrinsic moon field is protective, not a self-inflicted hazard.

**Kerbalism mapping (embedded moon):** give the moon its own compact `RadiationModel`
(small `pause_radius` in moon radii; a single narrow belt) + a `RadiationBody` with a
*weak* `radiation_inner` (source-starved) and a small stock-scale `radiation_pause`
(~−0.01; the shield is the *presence* of a pause at `pause_radius`, not a big value).
The moon's net surface dose = the parent's belt at its L-shell, reduced by its own pause.

**Worked (Pandora vs Ganymede):** Pandora (75 µT, 3.53 R_p, in Polyphemus's belt gap)
→ field ~19× the local parent field → standoff ~2.5 R_p, one weak belt
(`radiation_inner ≈ 2` rad/h, ~0.2× stock Kerbin's 10.4 because it is gap-starved),
`radiation_pause ≈ −0.01` (stock scale). Ganymede (0.72 µT, ~6× local Jovian) →
standoff ~2 R_G, a negligible own belt. Pandora's mini-magnetosphere is the more
robust of the two, yet its habitability still rests on the *shield*, not on any
belt it makes.

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
  the ring + five moons sweep particles (loss). Because of that ring, the Kerbalism
  template is **Saturn (RSS), not Jupiter**: a strong *outer* belt (`radiation_outer` ~150,
  Saturn's value) with the inner belt suppressed/absent (ring-swept), a large `pause_radius`,
  and the small stock-scale `radiation_pause` (~−0.01). Dante's volcanism still feeds an
  inner plasma torus locally, so a reduced inner belt (not fully zero) is defensible.
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
