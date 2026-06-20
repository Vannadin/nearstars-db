<!-- 폴리페무스(α Cen A b) 비주얼 art-direction Phase 4 초안 — 사용자 창작 영역, 미게이팅 -->
# Phase 4 Draft — Polyphemus (α Cen A b) Visual Art Direction

**Status:** DRAFT · **Phase 4a creative input** · NOT gated, NOT in the DB. Phase 4 is
not yet implemented (see [`README.md`](README.md)); this records the creative target and
the 고증 analysis so it can be activated when Phase 4 is built. The per-axis **gated
conclusions** (orbit / banding / haze / aurora / rings / Pandora) live in the decision
board [`alpha_centauri.yaml`](alpha_centauri.yaml) — this `.md` is the 4a scratch that
feeds it, not the record of record.

This is the **user's creative domain**. The science doc stays separate and
untouched — the Phase 3 synthesis below is quoted only as the window this
art-direction is checked against.

---

## The body

α Centauri A b is the real-life candidate for **Polyphemus**, the *Avatar* gas
giant whose moon Pandora is the Na'vi homeworld. DB / Phase 3 facts:

- Saturn-class (~120 M⊕), a ≈ 1.6 AU around α Cen A (G2V, 1.521 L☉).
- T_eq ≈ 225 K (favored a < 2 AU family); a cold-to-temperate giant.
- Atmosphere: H₂/He, metal-enriched, **water the condensing cloud species
  (NH₃ rained out at 225 K)** → near the Sudarsky Class I/II boundary.

## Creative target (the art-direction)

A **banded "blue Jupiter" carrying white, gold, and blue stripes** — the *Avatar*
Polyphemus look. The intended read is a *luminous, pale* giant (a bright, warm
Class I/II world, not a dark one) with a strong three-tone banded character:

- **White zones** (upwelling bands) — clean reflective cloud tops (ammonia / water);
  the bright base tone.
- **Gold / yellow bands** — clouds tinted by **photochemical chromophores + haze**
  (S / P / NH₄SH / hydrocarbon tholins), the Saturn-gold / Jupiter-tan mechanism.
- **Blue belts** (downwelling, cloud-cleared bands) — clearer air revealing
  **methane red-absorption + Rayleigh** below; the Uranus/Neptune mechanism. A few
  read as sharper, deeper blue so the banding has rhythm, not a uniform gradient.
- **A signature storm** — one large cyclonic vortex (a Jupiter Great-Red-Spot
  homage, as in the films), the planet's focal landmark, set in a belt.
- **The Roche-zone ring** (from the Phase 3 synthesis) as a thin, dark framing
  line across the disk — narrow and unobtrusive, not a Saturn-scale ring system.

**Colour physics (three coexisting mechanisms, all banded by the zonal jets):**

| band | colour | mechanism | analogue |
|---|---|---|---|
| zone | white | clean NH₃ / H₂O cloud | Jupiter zones |
| haze | gold/yellow | photochemical chromophore + haze | Saturn gold |
| belt | blue | cleared → CH₄ absorption + Rayleigh | Uranus/Neptune |

Self-consistent at **~250–350 K** (warm Class I/II): water-cloud white zones, a
photochemical gold haze, and methane-blue in the cleared belts — and that warm
temperature also fits a habitable Pandora. Key assumptions (art-direction within
the physical window): enough methane to colour the cleared belts, and a
Saturn-gold (not Jupiter-red) chromophore. This is the **Phase 4a** creative target;
the **Phase 4b** gate must check it against the Phase 3 atmosphere synthesis (below).

**From Pandora's sky.** This is the view the moon is famous for: from Pandora's
surface Polyphemus spans **~36°** of the sky (computed in stability-sim — a 1
R_Jup giant at 225,000 km), so the banded cream-and-blue body, its storm, and
the dark ring fill the daylit sky. The art-direction has to read at *that* scale
— a near-filling skyline — not just as a distant disk.

**Sibling moons in Pandora's sky (memo, 2026-06-19).** The inner moons are clearly
visible from Pandora and shuttle across Polyphemus's huge disk (computed in stability-sim):
- **Dante** — apparent diameter 0.32–0.83° (vs Earth's Moon 0.52°), swings ≤26° from
  Polyphemus's centre, transit/occult cycle ~11 h; volcanic moonlet (orange lava flecks).
- **Hades** — 0.24–0.95°, swings ≤37°, cycle ~23 h; tidal-heated >900 K → a **faint red
  ember** even on its night side.
Because both orbit inside Pandora (225k), they never leave Polyphemus's vicinity — they
glide across its banded face and duck behind its limb. Great surface-view material: the
giant + two moons (one red-glowing, one volcanic) eclipsing each other every few hours.

**Art-direction intent — larger orbital inclinations (memo).** The current moon set is
near-coplanar (stability-optimised), so from Pandora they all track the *same* line across
Polyphemus. For a prettier visual spread (moons at different sky latitudes, not stacked on
one band), the owner wants **somewhat larger mutual inclinations.** This is a Phase 4a
target needing a **4b stability re-check**: modest inclinations are fine for moons deep in
the Hill sphere, but how large before Kozai/stability degradation needs a scan (next
session, alongside the M0≈180° 3:2-lock confirmation).

*(Proposed direction; the binding calls — how deep the blue goes, the storm's
placement/size — are left in "Open creative questions" below for the user to set.)*

## Aurora (atmospheric emission)

If Polyphemus has aurorae (magnetospheric, or driven by a moon plasma torus),
their colour is **set by the H₂/He atmosphere, not chosen** — so unlike the band
hue it is composition-locked, not a divergence option. Hydrogen dominates →
**rose-pink to magenta with a violet edge**, never Earth's green (there is no
atomic oxygen):

- Red base — H Balmer-α (656 nm) + H₂ Fulcher-α bands.
- Violet-blue — H Balmer-β/γ (486 / 434 nm) + H₂ Werner bands.
- He may add a faint D3 yellow (587.6 nm); CH₄ absorbs (auroral haze) rather than
  emits; water and metals are condensed out at auroral altitude → no contribution.
- Most auroral power is in the UV (H Lyman-α, H₂ Lyman/Werner), so the visible
  aurora is relatively faint for its total output.

Art-direction note: a polar **rose-magenta** aurora deliberately contrasts with
Pandora's **cyan/blue bioluminescence** — planet pink, moon teal. Exact sRGB
(H Balmer / H₂ bands / He D3) to be pulled from `db/refs/element_plasma_colors.yaml`
and `molecular_plasma_colors.yaml` when Phase 4 emits.

## 고증 window (from the Phase 3 atmosphere + dynamics synthesis)

The Phase 3 baseline ([`../docs/phase3/alpha-centauri-a-b.md`](../docs/phase3/alpha-centauri-a-b.md))
puts the *physical* default at a **pale cool-white water-cloud giant**
(`atmosphere_tint #dfe3e8`, `cloud_tint #eef1f4`) with **faint** zonal banding —
Sudarsky Class I/II, brighter and more uniform than Jupiter. Against that:

| Target element | Physics at T_eq ≈ 225 K | Verdict |
|---|---|---|
| Ivory / cream zones | pale water-cloud white + faint warm bias from G2V light | **inside window** — essentially the default |
| Banded structure | belt/zone dynamics are real (baseline already has faint banding) | **inside window** — push the contrast |
| **Muted** blue belts (slate / steel) | Rayleigh cast (bright G2V favors it) + cloud-cleared belts read deeper/bluer | **inside window** |
| **Deep Neptune cobalt** belts | needs ice-giant cold (~70–130 K); at 225 K methane is gaseous, no deep methane-blue | **outside window → documented divergence** |

So the *banded ivory + muted-blue* reading is physically defensible; only the
**fully saturated Neptune-cobalt** is a divergence (the temperature is wrong for
it — the deep methane-blue mechanism needs a much colder body). See the colour
mechanism + ice-giant saturation reasoning in
[`../phase3/stability-sim/ALPHA_CEN_AB_DYNAMICS_STUDY.md`](../phase3/stability-sim/ALPHA_CEN_AB_DYNAMICS_STUDY.md)
context and `docs/reference/color-materials.md`.

## Pandora canon reference (Avatar) — researched 2026-06-15

Canonical parameters from the official guidebook (*Avatar: A Confidential Report…*),
Pandorapedia, and the James Cameron's Avatar Wiki. Tier: [CANON] = film/official,
[WIKI] = guidebook-derived fan-wiki.

- **System:** Pandora orbits a gas giant (**Polyphemus**) of **α Centauri A**, a G-type
  yellow dwarf. [CANON]
- **Polyphemus:** Saturn-class gas giant, **helium-rich** (~72% H / 24% He), a giant
  **eye-shaped vortex storm** bigger than Jupiter's Great Red Spot, **no rings** [CANON],
  **14 moons** (Pandora is the 5th). Mass "more massive than Saturn" (no number).
- **Pandora day = 27 h** [CANON/WIKI] — matches our assumption.
- **Gravity 0.8 g**, **mass 0.72 M⊕**, **diameter 11,447 km** (~0.90 R⊕) [CANON/WIKI].
  (0.72 M⊕ at that radius → ~0.89 g, a minor canon self-inconsistency vs the stated 0.8 g.)
- **Atmosphere:** O₂ ~21% but unbreathable due to **CO₂ >18%, H₂S >1%, xenon 5.5%**;
  pressure ~1.1 atm, density ~1.2× Earth. [CANON]
- **Climate:** tropical/hot, **warm via a dense greenhouse + explicit tidal heating**
  (canon states the warmth is *not* from proximity to the star) → high volcanism, fast
  continental drift. [CANON] — directly supports our greenhouse + tidal-heating model.
- **Strong magnetosphere + "flux vortices"** (field-overlap funnels, levitating
  unobtanium) [CANON] — supports the NearStars flux-tube plugin / internal-heating idea.
- **Frequent ("almost daily") eclipses** as Polyphemus blocks the sun. [CANON]

### Observation-vs-canon divergences (Phase 4 gate decisions, 2026-06-15)
α Cen A b is a **real JWST candidate** (Beichman 2025), so where the real observation and
the Avatar canon disagree, NearStars takes the **observation** (the mod's first purpose is
reproducing real bodies) and records the divergence:

- **Polyphemus distance — KEEP 1.6 AU (observation).** Canon states 1.2 AU; we use 1.6 AU
  = Beichman's favored a < 2 AU family from the temperature fit. (Canon's 1.2 AU would be
  warmer, T_eq ≈ 259 K vs our 225 K — but 1.6 AU is the measured-favored value.)
- **Polyphemus ring — KEEP the ring (observation).** Canon says Polyphemus has no rings;
  our thin ring comes from Beichman §5.3's ring-model radius fit. Observation wins.
- **Pandora mass — ADOPT canon 0.72 M⊕** (was 0.45). Pandora is fictional, so canon is the
  authority for it. Updated in `hypotheticals/alpha_centauri.json`; **re-verified Hill-stable**
  (0.02 R_Hill, bound=True — moon mass is negligible vs the 120 M⊕ planet).
- **Polyphemus mass** (~120 M⊕) is consistent with canon's "more massive than Saturn" (≳95 M⊕).

## Polyphemus system & moons (Avatar canon) — researched 2026-06-19

Recorded as reference only — **whether/how to implement is a separate decision** (this
file is a staged Phase 4 draft, nothing gated/emitted).

**α Centauri A system (canon):** 2 rocky inner planets + 3 gas giants. **Polyphemus =
the 4th planet = the 2nd of the 3 gas giants.** Canon: "slightly smaller and denser
than Jupiter, **no rings**, **14 moons**."

**Provenance [GAME] — corrected 2026-06-19.** The moon **names and their physical
descriptions** are *not* fan-speculation: they come from **James Cameron's Avatar: The
Game** (2009, Ubisoft) — a licensed, Cameron-involved expanded-canon title. So this is a
real source tier ([GAME], below [CANON] film/official but above [WIKI] fan-derived), and
several moons carry usable physical detail, not just names.

**The 14 moons = 5 named + 9 unnamed** (corrected 2026-06-19). Earlier I miscounted
Poly-L4/L5 into the 14 and the unnamed as ~7; the wiki is explicit: the fourteen are the
5 named (Dante, Hades, Pandora, Cassandra, Chaos) **+ 9 unnamed**, and **Poly-L4/L5 are
co-orbital *planetoids*, not moons** (counted separately).

### Per-moon data collected from the wiki (2026-06-19)

Only fields the wiki actually states; "—" = not stated. All [GAME] (*Avatar: The Game*,
datamined) unless noted. **No moon has a stated semi-major axis, period, or eccentricity
except via ordering** — only Pandora has mass/density. Order from the Polyphemus + Alpha
Centauri System pages:

| moon | order | diameter | other stated data |
|---|---|---|---|
| **Dante** | innermost (1st) | — | perpetual volcanism + moonquakes from Polyphemus's tidal forces; orbits as close as possible without tidal breakup (Roche edge) |
| **Hades** | 2nd | — | elliptical orbit grazing Dante → **T > 900 K** (627 °C); faint red glow; "near-fusion" (the ACS page says *full* fusion and inverts the Dante/Hades attribution — pages conflict) |
| (unnamed) | 3rd, 4th | — | — |
| **Pandora** | **5th** | **11,447 km** | mass 0.72 M⊕, gravity 0.8 g, density 1.2 ρ⊕, surface P 1.1 atm (0.9 at sea level), day 27 h, **axial tilt 29°**, atm N₂/O₂/CO₂ >18%/Xe 5.5%/CH₄/H₂S >1%, orbits *between* Polyphemus's two radiation belts, Fe core + unobtanium-strengthened dipole [Survival Guide + Game] |
| (unnamed) | 6th | — | also a **N–O atmosphere from a carbon-cycle biosphere** (the only other life-bearing moon noted) |
| **Cassandra** | outer | **> 6,500 km** | **2nd-largest** moon; N–H atmosphere + few % CO₂ → carbon-cycle life possible. Source: **Lightstorm's Joshua Izzo, OmatiCon 2024 panel** (semi-official, newer than the game) |
| **Chaos** | beyond Cassandra | — | **fractured Miranda-like**; cliffs **15–30 km**; cliffs likely from past tidal heating |

Co-orbital **planetoids** (NOT among the 14 moons):

| body | position | diameter | note |
|---|---|---|---|
| **Poly-L4** | L4, 60° ahead | **337 km** | planetoid; noted as orbiting retrograde vs the moons |
| **Poly-L5** | L5, 60° behind | **611 km** | planetoid (the larger of the pair); retrograde |

**The two outermost moons orbit retrograde** (opposite the rest), per the Polyphemus page.

**Host Polyphemus (for context):** diameter **123,900 km** (infobox) / ~119,000 km (prose
"74,000 mi, slightly smaller than Saturn"); rotation **10.1–10.6 h** (core/B-field 9.7 h);
atmosphere **H₂ >72% / He >24% / 4%** (CH₄, NH₃, H₂S, H₂O + trace acetylene/CO/ethane/
germane/phosphine/propane); metallic-hydrogen transition ~2 Mbar/~6000 K; molten iron
core; **no rings**; originally named "Crius." Innermost moonlets get **>4,500 rem/day**
(Io 3,200); Pandora sits just outside the main belts.

**Note for the appearance gate.** The game's stated Polyphemus atmosphere — NH₃, H₂S, CH₄,
H₂O all present — is chemically consistent with the white/gold/blue banding target: NH₃/H₂O
→ white clouds, H₂S / NH₄SH chromophores → gold/yellow, CH₄ → blue belts. Fiction-canon
([GAME]), but it *lines up* with the Phase 4a colour direction.

**Physics hooks** (Roche-edge Dante, tidal-heated Hades, fractured Chaos) are gameplay-rich
*and* sourced — good implementation candidates if the moon set is built. The Dante
"Roche edge" claim directly feeds the Roche-limit ring analysis.

**Canonicity caveat.** The Avatar Wiki flags the moon detail pages (Dante/Hades/Chaos/
Poly-L4/L5) as datamined *Avatar: The Game* content with a **non-canon disclaimer** — so
[GAME] = a real, licensed, *authored* source (not fan invention), but Lightstorm has not
ratified it as film canon. Cassandra's data traces to a 2024 Lightstorm panel (more
current). Treat as **soft canon** for art-direction; observation wins where they conflict.

**Canon ↔ observation tensions (to resolve IF implemented):**
1. **Density** — canon "denser than Jupiter"; the real α Cen A b imaging estimate is
   1.05 R_Jup, **0.40 g/cc** (much *less* dense). cfg must pick one.
2. **Rings** — canon "no rings"; our art-direction keeps a thin observation-based
   Roche-zone ring. (Ring placement = the Roche-limit analysis, not yet done.)

**Dynamics note (Trojan moons are real-physics-viable).** Pandora/Polyphemus mass ratio
≈ 0.006 ≪ 0.04 → Pandora's L4/L5 are stable for Trojan companions, so Poly-L4/L5 as
co-orbitals of Pandora is dynamically sound. A full 14-moon stable-placement check
(Roche limit → ~0.5 R_Hill ≈ 5.7×10⁶ km zone) is **not yet run** — separate task.

Underlying source: **James Cameron's Avatar: The Game** (2009, Ubisoft) — the origin of
the moon names + physics. Accessible via Avatar Wiki:
[Polyphemus](https://james-camerons-avatar.fandom.com/wiki/Polyphemus),
[Cassandra](https://james-camerons-avatar.fandom.com/wiki/Cassandra),
[Hades](https://james-camerons-avatar.fandom.com/wiki/Hades),
[Pandora](https://james-camerons-avatar.fandom.com/wiki/Pandora),
[Alpha Centauri System](https://james-camerons-avatar.fandom.com/wiki/Alpha_Centauri_System).

## Pandora — surface climate over the orbit (estimate, 2026-06-15)

Polyphemus (and its moon Pandora) ride an eccentric heliocentric orbit (a = 1.6 AU,
e = 0.1 → periapsis 1.44 AU, apoapsis 1.76 AU around α Cen A). Insolation from A
swings **1.49×** over the 705-day orbit (α Cen B adds <1%). The periapsis↔apoapsis
temperature difference is **fundamentally ~10% of the absolute temperature**
(ΔT/T = 0.25·ΔS/S, independent of greenhouse/albedo).

**Pure radiative equilibrium (physics, no greenhouse):** ~244 K (periapsis) to ~213 K
(apoapsis) for Bond albedo 0.2–0.3, full redistribution → i.e. −30 to −60 °C. Cold,
because Polyphemus sits beyond α Cen A's outer HZ edge (consistent with the Phase 3
T_eq ≈ 225 K). A habitable Pandora therefore *requires* ~70 K of extra warming. **That
warming is GREENHOUSE, not tidal** — see the tidal-heating analysis (2026-06-21) below,
which shows tidal heating is a knife-edge that more likely sterilizes than gently warms.
The dense CO₂ greenhouse (canon: ~1.2× Earth pressure, CO₂-rich) is the physically sound,
canon-aligned warmer; the ~70 K lift is art-direction (the greenhouse strength is not
derived, but the *mechanism* is correct).

**Habitable scenario (target mean set as art-direction):** the seasonal (orbital)
swing scales as ~10% of the mean. For a temperate-to-tropical mean of ~288–295 K:
- bare equilibrium swing ≈ 29 K;
- with realistic atmospheric thermal inertia (~0.7 damping) ≈ **20 K** (e.g. 305↔285 K
  at a 295 K mean);
- with a deep ocean / strong inertia ≈ 14–15 K.

The **27-hour day governs the day↔night swing, NOT this seasonal swing** — a fast day +
thick atmosphere mixes longitudes so the diurnal range is only a few K (and justifies
the full-redistribution assumption); small daily ripples sit on top of the great season.
Convection/atmosphere both redistributes heat and provides the inertia that damps the
season; because the 705-day orbit is *slow*, damping is only partial (the surface largely
tracks equilibrium). Additional moon-specific terms raise the floor and slightly reduce
the relative season: tidal heating (constant internal), planetshine + Polyphemus thermal
IR, and a brief cooling dip each ~27 h orbit when Pandora crosses Polyphemus's shadow.

**Bottom line:** a tropical (~290 K) Pandora has a realistic **~15–25 K (best ~20 K)
periapsis-warmer "great season"** over each 705-day (~2 Earth-year) orbit — comparable
to a strong continental seasonal cycle, livable. This is a supporting reason the e = 0.1
orbit is fine to keep (a noticeable but habitable season, not a climate breaker).

## Pandora — tidal heating & the day-lock, reconsidered (2026-06-21)

A deeper look (driven by the J2 moon work) overturns the loose "tidal heating helps
warm Pandora" framing. **Tidal heating is not a free gentle warmer here — it is a
knife-edge that, at fiducial dissipation, sterilizes Pandora into a tidal Venus.**

**The forced eccentricity is intrinsic and unavoidable (sim-confirmed).** Pandora is set
e = 0, but the N-body sim (TRACE, J2 on) pumps it to a sustained **e ≈ 0.0045–0.0051**.
Source isolation: Pandora *alone* (siblings removed) still reaches e ≈ 0.0045 → the pump
is α Cen A/B's secular forcing on the moon (the same mechanism that gives Earth's Moon a
solar-forced e term), **not** Polyphemus's heliocentric eccentricity. Confirmed:
e is identical (0.00514) at Polyphemus e_helio = 0.03 / 0.05 / 0.10 → **lowering
Polyphemus's eccentricity does NOT help** (tested and rejected). Sibling moons add only
~15 % (alone 0.00445 → full 5-moon 0.00514). So there is **no orbital knob** that reduces
Pandora's forced e. (Forced e from the committed `results/_moons_j2/spread25`; the e_helio
and source-isolation checks were diagnostic runs — reproduce via `run.py … --acen-e {0.03,0.05}`
and reduced-moon hypotheticals — not committed.)

**At that e, tidal heating depends entirely on Pandora's interior dissipation k₂/Q** (the
only free parameter, since e, M_Polyphemus, R_Pandora, a are all fixed). Heating scales
∝ (k₂/Q)·e²·M_p^2.5·R_m^5·a^−7.5. Calibrated off Io (k₂/Q = 0.016 ⇒ 100 TW):

| body (real k₂/Q) | k₂/Q | → Pandora tidal flux | verdict |
|---|---|---|---|
| Moon | 0.0006 | 45 W/m² | habitable |
| Earth, solid body tide only | 0.0011 | 76 W/m² | habitable |
| **Mars** (Phobos decay) | **0.0019** | **134 W/m²** | habitable (just) |
| — threshold — | **0.0022** | **155 W/m²** | runaway edge |
| Venus | 0.0029 | 210 W/m² | tidal Venus |
| Io (molten) | 0.016 | 1139 W/m² | tidal Venus |
| **Earth, effective (ocean tides)** | 0.025 | 1780 W/m² | tidal Venus |

(Runaway-greenhouse ceiling ≈ 295 W/m²; stellar absorbed ≈ 140 W/m² → tidal budget ≈ 155.
Io's *own* surface tidal flux is only 2.4 W/m² — Pandora is bigger and deeper in the well.)

**The threshold (k₂/Q < 0.0022) sits exactly at Mars.** So a habitable Pandora is *not*
exotic — it just has to be a cold, rigid, **Mars/Moon-like** body (solid body tide), not
molten (Io), not large-liquid-cored (Venus/Mercury), and not ocean-tide-dominated (Earth's
*effective* k₂/Q is anomalously high because its basins are near-resonant with the lunar
tide). The body (solid) tide alone clears the bar; a strongly dissipative ocean is the risk.

**The sharp internal tension:** canon attributes Pandora's *volcanism + fast tectonics* to
tidal heating — but vigorous tidal geology needs **high** dissipation (low Q, Io-side),
which is exactly the regime that sterilizes the climate. **At e ≈ 0.005 you cannot have
both vigorous tidal volcanism and a temperate climate.** Adopted resolution: take the
**habitable** branch (high-Q, Mars/Moon-like, k₂/Q ≈ 0.0015 → tidal flux ≈ 100 W/m²),
keep Pandora temperate, and **downgrade canon's "Io-grade tidal volcanism" to modest
tectonics (documented divergence)**. Caveat: a runaway feedback (any partial melt → Q
drops → more heat → more melt) means the assumption is "starts cold and stays high-Q."

**The day = orbit lock is unavoidable — a is forced to 225,000 km.** Pandora's 27 h day
comes from tidal locking (day = orbital period → a = 225,000 km via Kepler). Idea tested:
put Pandora on a *wider* orbit (weaker e-tide) but give it a free 27 h *spin* instead of
locking. **Rejected on physics:** a non-synchronous moon suffers the *spin* tide (the bulge
sweeps the whole body, amplitude O(1) vs the e-tide's ~e), which is **~4000× larger** than
the e-tide — e.g. at a = 360,000 km the e-tide is 32 W/m² but the spin tide is 1.2×10⁵ W/m²
(instant melt) — and tides **despin it to synchronous in < 1 Myr**, so the free spin doesn't
persist (the day reverts to the long orbital period). Escaping the spin tide needs a ≳ 2×10⁶
km, where Polyphemus shrinks to a dot in the sky (losing the iconic Avatar visual). So day
and orbit can't be decoupled — every close moon is synchronous for this reason. **a stays
225,000 km; the only viable lever is the high-Q interior assumption.**

## Mapping to cfg (for the eventual Phase 4 emit)

- `atmosphere_tint` / `cloud_tint` — ivory zones, slate/steel-blue belts (rather
  than the uniform `#eef1f4` baseline).
- `cloud_morphology` — raise belt/zone contrast from "faint banding" to
  prominent stripes.
- Storm feature — optional canon cyclonic vortex (placement / size TBD); a
  texture/feature decision, not a tint field.
- Gate outcome — *muted-blue banded* = passes the 고증 gate directly;
  *deep-cobalt* = passes only as a flagged documented divergence.

## Open creative questions (resolve when Phase 4 is built)

- How far to push the blue — within-window slate, or canon cobalt (accepting the
  divergence flag)?
- Include the canon storm vortex? where / how large?
- How the Phase 3 Roche-zone **ring** reads against the banding.
- Pandora's own surface/atmosphere appearance — a separate Phase 4 draft (the
  moon is already dynamics-gated Hill-stable in stability-sim).

## References

- Phase 3 report — [`../docs/phase3/alpha-centauri-a-b.md`](../docs/phase3/alpha-centauri-a-b.md)
- Dynamics study — [`../phase3/stability-sim/ALPHA_CEN_AB_DYNAMICS_STUDY.md`](../phase3/stability-sim/ALPHA_CEN_AB_DYNAMICS_STUDY.md)
- Colour mechanisms — `docs/reference/color-materials.md`
