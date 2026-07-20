<!-- 40 Eridani A d Phase 3 synthesis: fictional Project Hail Mary "Threeworld" analog (Astrophage breeding ground) — no real detection -->
# 40 Eridani A d — Phase 3 Synthesis (Fictional — *Project Hail Mary* Threeworld)

40 Eridani A d is a **fiction-canon body with no real detection**. It
implements the third planet of Rocky's home system in Andy Weir's
*Project Hail Mary* (2021, p. 393): a Moon-sized world with 0.2 g
surface gravity and a thin 84% CO₂ / 8% N₂ / 4% SO₂ atmosphere at
less than 1% of Earth's surface pressure — the Astrophage breeding
ground at the far end of 40 Eridani's Petrova arc, the system-local
analog of Adrian at Tau Ceti. The physical package (radius, gravity,
composition, pressure ceiling) comes straight from Weir's canon; the
orbit is a NearStars design validated by dynamics.

The orbit (a = 0.635 AU, e = 0.042, P = 209.27 d) was placed near a
2:1 period ratio outside the synthetic filler c and validated in the
same REBOUND integration as the rest of the system: 10⁵ yr with
WHFast, relative energy error 4.6×10⁻¹¹, MEGNO = 2.00 (regular), all
bodies stable with calm eccentricity evolution
(`phase3/stability-sim/results/40_eridani_summary.json`; d's
eccentricity stays within 0.013–0.047).

The happy accident of the design is the insolation: at 0.635 AU
around the 0.4078 L☉ primary, d receives **1.01 S⊕ — Earth's own
insolation** — yet it is Moon-sized. That contrast (an
Earth-temperate energy budget on a body far too small to keep an
Earth-like atmosphere) is the whole character of the world: a
freezing-point rock with a whisper of volcanic air, self-consistently
thin because a 2.6 km/s escape velocity can only hold what
outgassing continuously replaces.

**Scenario choice for NearStars: a cold, basalt-brown Moon-sized
world under a near-vacuum CO₂/SO₂ sky — pale sulfur-frost patches in
the cold traps, a crisp Mars-thin twilight limb, and the Petrova arc
of migrating Astrophage arcing toward the K0.5 V primary as the
system's signature fictional light feature.**

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `disposition` | Fictional (*Project Hail Mary* Threeworld; no detection) | high | The one high-confidence row: fiction canon implemented by project decision, per-body values `method: theoretical` in `db/planets_curated.json` |
| `mass_mearth` | 0.0149 | low | derived from canon: Moon-sized (R = 1737 km) at 0.2 g → M = g·R² = 0.0149 M⊕ |
| `radius_rearth` | 0.273 | low | PHM p. 393 canon — Moon-sized (1737 km) |
| `density_g_cc` | ~4.0 | low | derived M/R³ — denser than the Moon (3.34), consistent with a small iron core |
| `surface_gravity_g_earth` | 0.2 | low | PHM p. 393 canon |
| `equilibrium_temp_k` (A=0.3) | 255 | low | derived; (A=0) 279, (A=0.15 adopted) 268 |
| `insolation_s_earth` | ~1.01 | low | derived 0.4078 L☉ / (0.635 AU)² — Earth-level insolation on a Moon-sized body |
| `surface_temp_k` | ~275 mean | low | Teq(A=0.15) + Mars-scale thin-CO₂ greenhouse (~6 K); straddles the water frost line |
| `bond_albedo` | 0.15 | low | tie-break: dark basalt with partial bright frost patches |
| `tidally_locked` | false (slow rotator) | low | despinning at 0.635 AU is ~16× slower than at c's orbit — marginal at 1.8 Gyr; tie-break picks a partially despun slow rotator |
| `rotation_period_h` | ~240 | low | tie-break: ~10-day solar day drives visible frost-terminator lag |
| `atmosphere_composition` | 84% CO₂ / 8% N₂ / 4% SO₂ | low | PHM p. 393 canon; SO₂ implies active volcanic replenishment (see Atmosphere) |
| `atmosphere_surface_pressure_pa` | 800 | low | design value inside canon's "<1% of Earth" ceiling (0.79%); Mars-like column |
| `surface_tint_rgb_hex` | `#6f665e` (cold basalt brown-gray) | low | tie-break: volcanic basalt under K0.5 V light |
| `surface_tint_rgb_hex_secondary` | `#d8d09a` (pale sulfur frost) | low | tie-break: SO₂/sulfur frost in polar and nightside cold traps |
| `sky_tint_rgb_hex` | `#2e3550` (thin-air twilight steel blue) | low | ~800 Pa Rayleigh-thin sky, darker than Mars (less dust loading assumed) |

## Surface synthesis

The size and gravity are canon; everything else follows from them.
A 1737-km body at 0.2 g works out to 0.0149 M⊕ and ~4.0 g/cc —
noticeably denser than the Moon, implying a small differentiated iron
core, which conveniently also supports the residual volcanism the
atmosphere needs (below). The 1.8 Gyr system age (Bond 2017 IFMR,
adopted in the host synthesis) helps here: a Moon-mass body is not
yet fully thermally dead at that age, unlike at the Moon's own
4.5 Gyr.

**A freezing-point world.** With Earth's insolation but a
near-vacuum atmosphere, the mean surface sits at ~275 K — almost
exactly on the water frost line. The synthesis leans into that:
equatorial daysides climb above freezing and bare dark basalt
dominates; poles and the slow nightside drop far below it and
collect frost. Water ice frosts form wherever any water is available;
SO₂ frost needs much colder traps (its ~32 Pa partial pressure
condenses only below ~175 K) and is confined to polar night — the
pale `#d8d09a` sulfur-frost patches are the visual signature.

**Volcanic terrain.** The SO₂ fraction in canon forces active sulfur
volcanism (see Atmosphere), so the terrain reading is young volcanic
plains punctuating an older cratered crust: dark flows, fissure
vents, and bright frost-rimmed cold traps. This is an Io palette at
Mars temperatures — sulfur tones muted and frozen rather than molten.
Per the plausibility gate there is **no** lava rendering at global
scale; at most, point-source vent glow is admissible as the
low-confidence volcanism flourish.

## Atmosphere synthesis

The composition and pressure ceiling are canon (84/8/4
CO₂/N₂/SO₂, < 1% Earth); the synthesis job is making them
physically coherent, and they turn out to cohere well.

**The thin pressure is self-consistent, not arbitrary.** At
2.6 km/s escape velocity and ~275 K, thermal escape of CO₂ is slow
but nonthermal stripping over Gyr is efficient — a Moon-mass body
cannot *keep* an atmosphere, it can only *sustain* one in steady
state between volcanic outgassing and escape. The ~800 Pa adopted
value is the Mars-like equilibrium column such a balance plausibly
holds; Weir's "< 1% of Earth" ceiling reads as exactly this regime.

**SO₂ is the smoking gun for active volcanism.** SO₂ photolyzes and
condenses on ~decade timescales; a 4% standing fraction is
impossible without continuous replenishment. The cfg therefore
treats ongoing sulfur volcanism as canon-implied, while flagging the
*heat source* as the honest weak point: tidal heating is negligible
(e = 0.042 at 0.635 AU on a Moon-mass body), so the budget must be
residual radiogenic + core-crystallization heat at 1.8 Gyr —
marginal, low confidence, and recorded as an open item.

**Greenhouse and climate.** An 800 Pa CO₂ column adds a Mars-scale
greenhouse (~6 K) — enough to matter at the frost line but not to
transform the climate. No liquid water is stable at this pressure
(the triple point is 611 Pa; only transient brines in the deepest
basins could skirt it — left as a texture-pass suggestion, not a cfg
claim).

**Astrophage context (fiction layer).** In PHM canon this world is
where 40 Eridani's Astrophage breed: the CO₂ atmosphere supplies the
carbon, and the Petrova arc connects it to the star. NearStars keeps
all Astrophage effects out of the physical rows — the arc is a
visual-layer feature only (see below), and no cfg physical value
depends on the fiction's biology.

## Rotation & spin synthesis

Tidal despinning scales steeply with distance: at 0.635 AU the
timescale is roughly 16× that of c at 0.4 AU, putting d on the
boundary between despun and primordial at the 1.8 Gyr system age.
Neither a pure synchronous state nor a fast primordial spin is
forced.

**Tie-break: a partially despun slow rotator at ~240 h.** A ~10-day
solar day is the most visually productive choice consistent with the
marginal despinning: long enough for the nightside to plunge and
frost over, short enough that the frost terminator visibly lags
sunrise — a moving frost line as the signature time-lapse feature.
Obliquity is left small but nonzero (~5°) so the polar cold traps
stay polar.

## Visual styling

- **Global appearance.** A small, cold, basalt-brown world
  (`#6f665e`) mottled with pale sulfur-frost patches (`#d8d09a`)
  concentrated at the poles and along the trailing nightside; thin
  crisp limb with a faint steel-blue twilight band (`#2e3550`).
- **Frost terminator lag.** The renderable consequence of the 240-h
  day: a bright frost fringe trailing the dawn terminator where the
  night's condensation has not yet sublimated.
- **Vent glow (low-confidence flourish).** Sparse point-source
  volcanic vents may glow faintly on the nightside — admissible under
  the plausibility gate as localized volcanism, never as lava fields.
- **The Petrova arc (fiction layer).** The system's signature
  fictional feature: the migrating Astrophage stream between d and
  the K0.5 V primary, canonically emitting at the 25.984 μm Petrova
  wavelength (thermal IR — physically invisible to the eye; the
  faint deep-red arc rendering is licensed artistic translation of
  the novel's own visual language). This cannot be expressed in
  Kopernicus/Scatterer cfg and is a **custom-plugin candidate** in
  the same class as the YZ Cet flux tube — backlogged for the plugin
  track, not emitted from this report.
- **Sky companions.** The white-dwarf B / red-dwarf C pair as
  brilliant points, per the system-wide skyscape.

## Canonical alternatives

**The canonical reading is no planet.** No detection of any kind
exists at this period; current catalogs list zero confirmed planets
around 40 Eridani A. The body exists as the *Project Hail Mary*
system-completion piece of the b/c/d documented-divergence ensemble.

| Reading | Content | Status |
|---|---|---|
| Canonical catalogs (2026) | no confirmed planets around 40 Eri A | observation |
| Weir's PHM canon (p. 393) | 3rd planet: Moon-sized, 0.2 g, 84/8/4 CO₂/N₂/SO₂, <1% Earth pressure, Astrophage breeding ground | fiction (worldbuilding) |
| **cfg pick** | PHM canon adopted verbatim for size/gravity/composition/pressure ceiling; orbit, rotation, tints filled by NS design + tie-break | documented divergence (canonical = no planet) |

## Bibliography

No discovery literature exists for a fictional body; the bibliography
records the canon source, the host grounding, and the dynamics
validation.

### Read (canon + grounding)

- **Weir A. 2021** — *Project Hail Mary* (novel), p. 393. The canon
  source: third planet of the Erid system, Moon-sized, 0.2 g,
  84% CO₂ / 8% N₂ / 4% SO₂ at < 1% Earth pressure, Astrophage
  Petrova-arc breeding ground. Cross-referenced in
  `docs/reference/cultural-context.md § 40 Eridani A`.
- **[Boyajian et al. 2012](https://arxiv.org/abs/1208.2431)** —
  CHARA interferometric luminosity of 40 Eridani A (0.4078 L☉),
  setting the insolation and temperature rows.
- **[Bond et al. 2017](https://arxiv.org/abs/1709.00478)** —
  IFMR system-coeval age (~1.8 Gyr) used in the interior-heat and
  despinning arguments.
- **NearStars stability run** —
  `phase3/stability-sim/results/40_eridani_summary.json`: REBOUND
  WHFast, 10⁵ yr, energy error 4.6×10⁻¹¹, MEGNO 2.00, all bodies
  stable/calm (d eccentricity 0.013–0.047).

### Method references

- Thin-atmosphere steady state (outgassing vs escape) and Mars-scale
  CO₂ greenhouse — textbook-level reasoning per the derived-value
  grounding policy's textbook exception; formulas in
  `docs/reference/methodology.md`.
- SO₂ photochemical lifetime / frost condensation — standard
  Io-literature background applied qualitatively; no numeric cfg row
  depends on it beyond the frost-placement tie-break.

## Open items for follow-up

- **Volcanic heat budget is the weak point.** A Moon-mass body
  sustaining sulfur volcanism at 1.8 Gyr on radiogenic heat alone is
  marginal. If a later pass wants firmer ground, options are a
  slightly higher design eccentricity (tidal assist) or accepting
  waning, episodic volcanism — both stay within canon's atmosphere.
- **Petrova arc plugin.** The arc is backlogged for the custom-plugin
  track (same class as the YZ Cet flux tube; C#/Harmony work is
  delegated per project policy). This report intentionally emits no
  cfg for it.
- **Rotation is pure tie-break.** Nothing in canon or physics pins
  the 240-h day; a Phase 4 board revision may re-pick it freely —
  the frost-terminator visual is the only thing at stake.
- **Transient brines.** Surface pressure (800 Pa) sits just above
  water's triple point (611 Pa); deepest-basin transient brines are
  physically admissible flavor for the texture pass but are
  deliberately not a cfg claim.

## Related

- [40-eridani-a](40-eridani-a.md) — host star Phase 3 (K0.5 V)
- [40-eridani-a-c](40-eridani-a-c.md) — inner neighbor (synthetic
  Mercury-analog filler)
- [40-eridani-a-b](40-eridani-a-b.md) — "Vulcan"/"Erid" (refuted
  detection, documented divergence; Weir's Erid is the *homeworld*,
  d is the *breeding ground*)
- [tau-cet-e](tau-cet-e.md) — sibling PHM world (Adrian, the Tau Ceti
  Astrophage breeding ground)
- [methodology](../reference/methodology.md) — Decisions schema
