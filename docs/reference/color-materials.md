<!-- 행성/위성 색을 실제 물질·메커니즘으로 정당화하는 큐레이션 카탈로그 + 관측 veto 게이트 -->
# Color materials & the plausibility gate

A justification tool, not a transcription of observed colors. The mod biases
toward **visually interesting** worlds (the mod's gameplay-variety bias); this
reference lets us back an *interesting* color choice with a real material or
mechanism, route it to the right layer, and write a one-line in-game hook —
**unless observation directly forbids it.**

Most planetary colors in this mod are **synthesized, not measured** — no
exoplanet has a measured surface/ocean/aurora color, and only a handful of hot
Jupiters have a measured reflected-light color. So color is a Phase 3 synthesis
judgment, gated by physics, vetoed by data.

---

## The gate (run in this order)

**1. Observational veto — does a real measurement *directly contradict* the
proposal?** If yes → **REJECT**, however interesting. This is the hard floor.
See the veto table below. Distinguish three data states:

- **Contradicted** — a measurement rules it out (thick atmosphere on a
  bare-rock-confirmed planet; a CH₄-cyan look on a planet with a *measured*
  CO₂ atmosphere; a rocky surface tint on a body whose density says gas
  envelope). → REJECT, offer the nearest non-contradicted alternative.
- **Unconstrained** — non-transiting / no atmosphere or albedo ever measured.
  Then there is *nothing to contradict* → the proposal is free, gated only by
  step 2. (Most NearStars planets are RV-only → this is the common case.)
- **Consistent** — a measurement supports or is compatible with it. → grounded.

**2. Plausibility / persistence — is there a real material or mechanism that
produces this color under *this body's* conditions (T, pressure, composition,
stellar SED), and how stable/expected is it?**

- **Common chemistry** (Rayleigh blue, CH₄ cyan, iron-oxide red, sulfur yellow,
  tholin orange, water-ice white) → **lane 1: Phase 3 grounded**, normal
  confidence.
- **Exotic-but-real** (halogen-gas green, iodine-vapor violet, a chromophore
  that exists but isn't an expected formation outcome) → **lane 2: cfg-artistic
  override**, the same flagged downstream layer as moons and synthetic
  eccentricity. Confidence=low,
  documented divergence, **but carries a genuine chemistry hook** — not
  fabrication.
- **Life-dependent** (chlorophyll green, retinal "Purple Earth") → lane 2,
  flagged speculative.

**3. No real material/mechanism, or it contradicts measured data → REJECT.**
Fabricating a chromophore is the delta-Pav-disk failure mode.

> Recompute, don't copy: T_eq = 278.3·L^0.25/√a, S = L/a² from the curated L
> and a (see SKILL physical-plausibility gates). Incandescent/blackbody colors
> follow surface T; scattering/reflectance colors follow composition + grain
> size + stellar SED.

---

## Vivid color playbook (color-indexed; the primary entry point)

"I want a green world" → here are the plausible realizations across domains and
which lane they land in. Detail rows are in the per-domain tables below.

### Vivid blue  *(easiest to ground)*
- **Atmosphere** — strong Rayleigh (clear, deep N₂/CO₂; bright shortwave star)
  · CH₄ absorption on a cold H₂/He giant (Neptune). lane 1.
- **Hot Jupiter** — silicate-cloud reflection + Na absorption → cobalt blue;
  *measured* on HD 189733 b (Evans 2013). lane 1.
- **Ocean** — deep pure liquid water. lane 1.

### Green  *(hardest; mostly lane 2)*
- **Atmosphere** — Cl₂ / halogen gas is genuinely yellow-green; sulfur-allotrope
  vapor. Exotic, not a standard outgassing product → lane 2 + hook.
- **Surface** — olivine/pyroxene fresh ultramafic exposure (subtle olive);
  chlorophyll vegetation (life → lane 2 speculative).
- **Ocean** — phytoplankton/chlorophyll (life); dissolved Fe(II) anoxic
  "ferrous sea" (hypothesis) → lane 2.

### Purple / violet
- **Atmosphere** — I₂ (iodine) vapor is violet. lane 2 + hook.
- **Surface / biosphere** — retinal phototrophs reflect purple ("Purple Earth",
  DasSarma & Schwieterman). lane 2 speculative.

### Yellow → orange → brown → red  *(well-grounded gradient)*
- Sulfuric-acid / sulfur aerosol (Venus pale yellow) → elemental sulfur surface
  (Io) → tholin photochemical haze (Titan/Pluto orange-brown) → iron-oxide
  surface (Mars red). All lane 1.

### White / grey / black
- White ← thick non-absorbing cloud, water/CO₂/N₂ ice, anorthosite. Grey ←
  aerosol/silicate haze, mineral cloud (hot). Black ← carbon/organics, basalt,
  ultra-low-albedo hot Jupiter (Na/K + TiO/VO; e.g. TrES-2 b). lane 1.

---

## Per-domain tables

Columns: **color · material/mechanism · conditions · persistence → lane ·
real example · in-game hook**. Persistence collapses the routing decision
(common→Phase 3 / rare→cfg-artistic / impossible→reject).

### Atmosphere (gas scattering + absorption + aerosol)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| blue | Rayleigh scattering | clear molecular gas, no strong absorber, bright shortwave star | common → P3 | Earth | molecular sky scatters blue |
| muted cyan-grey | Rayleigh under cool star | same, but M-dwarf SED red-shifts it dim | common → P3 | TRAPPIST-1 e (synth) | blue sky dimmed by a red sun |
| cyan / blue | CH₄ absorbs red | cold H₂/He giant + CH₄ | common → P3 | Uranus, Neptune | methane swallows the red light |
| orange / brown | tholin photochemical haze | CH₄+N₂ + UV flux | common → P3 | Titan, Pluto | UV-cooked organic smog |
| pale yellow | H₂SO₄ / sulfur aerosol | S volcanism, thick hot | common → P3 | Venus | sulfuric-acid cloud veil |
| **yellow-green** | **Cl₂ / halogen gas** | halogen-rich, exotic chem | **rare → artistic** | (none natural) | a chlorine-tinged sky |
| **violet** | **I₂ (iodine) vapor** | iodine volatile, warm | **rare → artistic** | (none natural) | iodine vapor stains it violet |
| white | optically thick non-absorbing deck | high cloud albedo | common → P3 | Venus top | unbroken bright cloud deck |
| grey / hazy | generic aerosol; silicate haze (hot) | dust load; hot mineral vapor | common → P3 | hazy sub-Neptunes, hot Jup | mineral haze greys the sky |
| cobalt blue | silicate-cloud reflection + Na | hot Jupiter, reflective clouds | measured (few) → P3 | HD 189733 b (Evans 2013) | sodium + glass clouds, cobalt |

### Surface (regolith / rock / ice; diffuse reflectance)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| red / orange | iron oxide (hematite, goethite) | oxidized Fe + weathering | common → P3 | Mars | rusted iron-oxide dust |
| dark grey / black | basalt, mafic/ultramafic silicate | volcanic, unweathered | common → P3 | Moon maria, Mercury | fresh basaltic plains |
| very dark | carbon / graphite / organics | C-rich primitive | common → P3 | C-type asteroids | carbon-blackened crust |
| light grey / white | anorthosite / feldspar | feldspathic highland crust | common → P3 | lunar highlands | bright feldspathic rock |
| bright white | water ice | cold surface, H₂O | common → P3 | Europa, Enceladus | clean water-ice shell |
| white | CO₂ / N₂ ice frost | very cold | common → P3 | Mars caps, Triton | frozen volatile frost |
| yellow | elemental sulfur / SO₂ frost | active S volcanism | common → P3 | Io | sulfur-paved volcanic plains |
| reddish-brown ice | tholin-stained ice | ice + irradiated organics | common → P3 | Charon pole, KBOs | radiation-tanned ice |
| olive green | olivine / pyroxene fresh | ultramafic fresh exposure | uncommon → P3/artistic | olivine beaches | olivine-green volcanic sand |
| glowing orange | incandescent silicate melt (blackbody) | T_sub ≳ ~1300 K (T_eq ≳ ~1000 K) **or** cited interior heating | conditional → P3 if T clears solidus | 55 Cnc e | molten rock glowing in the visible |
| green (bio) | chlorophyll vegetation | life | speculative → artistic | Earth | photosynthetic ground cover |
| purple (bio) | retinal phototrophs | life, "Purple Earth" | speculative → artistic | (hypothesis) | retinal-pigment biosphere |

### Ocean / surface liquid

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| blue | pure liquid water | water ocean | common → P3 | Earth | water absorbs red, scatters blue |
| green / teal (bio) | phytoplankton / chlorophyll | life | speculative → artistic | Earth coast | bloom-tinted shallows |
| green | dissolved Fe(II) ferrous | anoxic, Archean-type | uncommon → artistic | early Earth (hypothesis) | iron-rich primordial sea |
| brown / tea | dissolved organics (CDOM, tannins) | organic-rich, swampy | uncommon → artistic | blackwater rivers | tannin-stained water |
| dark / black | liquid hydrocarbons (CH₄/C₂H₆) | Titan-cold | common (cold) → P3 | Titan lakes | methane-ethane lake |

### Cloud

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| white | water / NH₃ / CH₄ ice | condensation | common → P3 | Earth, Jupiter zones, Neptune | bright ice-crystal cloud |
| yellowish-white | sulfuric acid | S, hot | common → P3 | Venus | sulfuric-acid haze |
| brown / tan | NH₄SH (ammonium hydrosulfide), tholin | giant-planet belt chem | common → P3 | Jupiter belts | ammonium-sulfide brown belts |
| red | P / S chromophores (debated) | photochemistry | uncertain → P3 low-conf | Jupiter GRS | photochemical red storm |
| grey / varied | silicate / iron clouds | hot giant / brown dwarf | measured → P3 | hot Jupiters, BDs | molten mineral clouds |

### Aurora
Emission colors, not reflectance — already cataloged. Use
[`element-plasma-colors.md`](./element-plasma-colors.md)
and firefly `composition-color.md`. Key lines: O I 557.7 nm green · O I 630.0 nm
red (high, thin) · N₂⁺ 427.8 nm violet-blue · N₂ bands red (low edge) · H Balmer
red on giants. **Conditions:** an atmosphere containing the emitting species +
magnetospheric particle precipitation (+ ideally a magnetic field). On
non-transiting planets the field/aurora is a tie-break → keep flagged
low-confidence.

---

## Observational vetoes (step 1 of the gate)

A proposal is **rejected** when a real measurement directly contradicts it.
Most NearStars planets are RV-only and hit *none* of these (→ unconstrained →
free). The veto only bites when a relevant measurement exists.

| proposal | vetoed by | example bodies |
|---|---|---|
| thick atmosphere | thermal phase curve / emission spectrum showing bare-rock dayside (no heat redistribution; brightness T ≈ substellar) | TRAPPIST-1 b (Greene 2023), TRAPPIST-1 c (Zieba 2023), LHS 3844 b (Kreidberg 2019) |
| atmosphere of composition X | a *measured* atmosphere of composition Y (color must match the real species) | 55 Cnc e — JWST CO₂/CO secondary atmosphere (Hu 2024) |
| solid/rocky surface tint, lava surface | bulk density (mass+radius) → mini-Neptune / gas envelope → no visible surface | any sub-Neptune with H/He envelope |
| reflected-light color | a *measured* geometric albedo / reflected color | HD 189733 b deep blue (Evans 2013); TrES-2 b near-black (low albedo) |
| liquid-water ocean | T_eq far above water critical / far below freezing without a greenhouse → no stable liquid water | hot/cold extremes |

When vetoed, offer the nearest non-contradicted alternative (e.g. thick
atmosphere vetoed on TRAPPIST-1 b → dark basaltic bare-rock surface, thin/no
sky).

---

## Worked examples

**Tau Ceti e — vivid green atmosphere (the PHM concept).** Tau Ceti e is
RV-only (non-transiting): radius, atmosphere, and albedo were never measured →
**unconstrained**, no veto possible. Green atmosphere ← halogen (Cl₂ yellow-
green) or sulfur-allotrope vapor: real chemistry, but not a standard outgassing
product → **lane 2 (cfg-artistic, flagged, low confidence)** with a genuine
hook. **Verdict: keep the green.** In-game: *"Tau Ceti e's yellow-green sky is
trace halogen gas filtering out red and blue — rare to form, but not
chemically impossible."* (Value-check the Cl₂/sulfur color claim against a
source before committing the entry.)

**"Thick atmosphere on TRAPPIST-1 b" — rejected.** JWST emission (Greene 2023)
shows a bare-rock dayside → thick atmosphere **vetoed at step 1**, regardless of
appeal. Alternative offered: dark basaltic/ultramafic bare-rock surface tint,
no sky.

---

## Notes on use
- This v1 uses textbook/established color chemistry. Rows marked **rare /
  artistic / speculative / debated** carry low confidence and **must be
  source-pinned at point-of-use** (value-check discipline) when written into a
  real body's Phase 3 doc or cfg.
- Reflectance vs starlight convention follows `disk-color.md`: intrinsic
  material color, with the renderer/star applying illumination. For the disk
  domain use the Mie engine (`scripts/phase3/disk_color_mie.py`), not this table.
- Wiring into the synthesis flow (a formal color gate in SKILL.md + a
  `## Color` proposal section) is pending the idea-#2 architecture decision
  (Phase 3 extension vs Phase 4). This doc is the architecture-neutral
  foundation both would use.
