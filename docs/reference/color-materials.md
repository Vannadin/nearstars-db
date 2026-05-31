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
- **Exotic-but-real** (halogen-gas tints, iodine-vapor violet, a transition-metal
  chromophore mineral, a chromophore that exists but isn't an expected formation
  outcome) → **lane 2: cfg-artistic override**, the same flagged downstream layer
  as moons and synthetic eccentricity. Confidence=low, documented divergence,
  **but carries a genuine chemistry hook** — not fabrication.
- **Life-dependent** (chlorophyll green, retinal "Purple Earth", halophile pinks)
  → lane 2, flagged speculative.

**3. No real material/mechanism, or it contradicts measured data → REJECT.**
Fabricating a chromophore is the delta-Pav-disk failure mode.

> Recompute, don't copy: T_eq = 278.3·L^0.25/√a, S = L/a² from the curated L
> and a (see SKILL physical-plausibility gates). Incandescent/blackbody colors
> follow surface T; scattering/reflectance colors follow composition + grain
> size + stellar SED.

---

## Color physics — why some colors are easy and some are hard

Read this before reaching for a color; it explains why we keep landing on
yellow-green instead of pure green, and where the vivid colors actually live.

- **The band-pass rule (why pure green is hard).** A green look needs to absorb
  *both* red and blue while passing green — a band-pass. Common atmospheric
  gases absorb only one side: CH₄ eats red → the result reads blue/cyan, not
  green. Single-absorber atmospheres slide toward blue or toward red/brown,
  never cleanly green. Pure green needs two complementary absorbers (chlorophyll)
  or an intrinsically green gas (Cl₂/ClO₂) → that's why atmospheric green is
  almost always lane 2.
- **Emission can be vivid where reflectance cannot.** Reflectance/scattering is
  broadband — you're filtering a continuum, so it tends pale or muddy. Emission
  lines are narrow and monochromatic, so airglow/aurora can show *pure,
  saturated* hues (O I 557.7 nm green, N₂⁺ 427.8 nm violet-blue) no reflective
  atmosphere can match. **For a vivid pure color, reach for a glow, not a tint.**
- **Transition-metal d-orbital (crystal-field) absorption is the main *inorganic*
  vivid color.** Fe, Cr, Cu, Mn do the heavy lifting — no life required. This is
  the lever for a vivid-but-grounded surface.
- **Oxidation state and fresh-vs-weathered set the hue.** Fe²⁺ → greens (olivine,
  serpentine, green clays); Fe³⁺ → reds/yellow-browns (hematite, goethite). Same
  element, opposite color, depending on redox. Fresh/reducing = green;
  weathered/oxidizing = red-yellow. Mn-oxide varnish blackens exposed rock over time.
- **Biology makes the most vivid colors** because pigments are tuned narrow-band
  absorbers (chlorophyll notches red+blue; phycoerythrin ~530–570 nm; retinal
  ~568 nm). The reflected complement is saturated. But it's life-dependent →
  speculative lane. (Melanin is the exception — a *broadband* absorber → dark
  brown/black, not vivid.)
- **Cool stars red-shift the sky.** Rayleigh ∝ λ⁻⁴, but you can only scatter the
  blue the star emits. An M-dwarf's red/IR-peaked SED leaves little short-λ flux
  → the same clear atmosphere reads wan grey-blue, not vivid blue. The illuminant
  is the variable, not the scattering.
- **Incandescence is set by temperature, not composition** — blackbody, first
  visible dull-red glow at the Draper point (~800 K), through orange/yellow to
  white-hot (≳1500 K). Route only if surface T actually clears the threshold.
- **Cloud color follows a condensation-temperature ladder.** Cold→hot:
  CH₄/N₂/H₂O/NH₃ ices (white) → NH₄SH + tholin (brown/tan) → H₂SO₄ (yellow-white)
  → low-T salts/sulfides KCl, ZnS, Na₂S, MnS, Cr (~600–1400 K) → silicate/iron/
  corundum (~1300–2000 K, grey mineral dust). Pick the species from cloud-deck T.
- **Hot Jupiters default dark; bright ones are the exception.** Broad Na/K D-line
  wings (plus TiO/VO in the hottest) drink the optical → most measured hot
  Jupiters are low-albedo (TrES-2 b ≈ black). High albedo needs reflective
  silicate/metal clouds outscattering the alkali absorption (HD 189733 b, LTT 9779 b).

---

## Vivid color playbook (color-indexed; the primary entry point)

"I want a green world" → here are the plausible realizations across domains and
which lane they land in. Detail rows are in the per-domain tables below.

### Vivid blue  *(easiest to ground)*
- **Atmosphere** — strong Rayleigh (clear, deep N₂/CO₂; bright shortwave star)
  · CH₄ absorption on a cold H₂/He giant (Neptune). lane 1.
- **Hot Jupiter** — silicate-cloud reflection + Na absorption → cobalt blue;
  *measured* on HD 189733 b (Evans 2013). lane 1.
- **Surface** — Cu²⁺ azurite, lazurite/lapis (S₃⁻ radical) ultramarine, glacial
  blue ice (thick clear ice). lane 1–2.
- **Ocean** — deep pure liquid water. lane 1.

### Cyan / teal
- **Atmosphere** — CH₄ + thin high haze (Uranus pale vs Neptune deep). lane 1.
- **Surface** — Cu²⁺ turquoise / chrysocolla / atacamite (arid or saline Cu
  weathering). lane 1–2.
- **Ocean** — glacial rock-flour suspension scatters blue-green. lane 1.

### Green  *(hard as an atmosphere; easy on a surface)*
- **Emission (vivid, real)** — O I 557.7 nm airglow/aurora is the purest green
  there is; a strong-airglow / auroral world *glows* vivid green at the limb.
  tie-break, low-conf.
- **Surface, no life (best inorganic vivid green)** — **Cr³⁺ emerald green**
  (uvarovite, chrome diopside, fuchsite) is the most saturated inorganic green;
  **Cu²⁺ malachite** green; olivine/peridot + serpentine + green clays give a
  subtler olive/bottle green (fresh ultramafic). lane 1–2.
- **Biology (most iconic)** — chlorophyll vegetation (surface) / phytoplankton
  (ocean). lane 2 speculative.
- **Ocean** — dissolved Fe(II) "ferrous sea" (Archean hypothesis). lane 2.
- **Atmosphere (gas)** — only yellow-green: Cl₂ / ClO₂. No clean pure-green gas
  exists → atmospheric green is essentially artistic. lane 2 + weak hook.

### Purple / violet
- **Atmosphere** — I₂ (iodine) vapor is violet. lane 2 + hook.
- **Surface / biosphere** — retinal phototrophs reflect purple ("Purple Earth",
  DasSarma & Schwieterman). lane 2 speculative. Anthocyanin flora (pH-tunable).
- **Surface mineral** — fluorite/some Mn or Fe phosphates (subtle). lane 2.

### Yellow → orange → brown → red  *(well-grounded gradient)*
- Sulfuric-acid / sulfur aerosol (Venus pale yellow) → elemental sulfur surface
  (Io yellow, reddening when hot) → orpiment yellow / realgar red (As-S) →
  tholin photochemical haze (Titan/Pluto orange-brown) → goethite yellow-brown →
  hematite iron-oxide red (Mars) → cinnabar scarlet (HgS). lane 1, the As/Hg
  ones lane 2.

### Pink / rose / magenta
- **Surface mineral** — Mn²⁺ rhodochrosite / rhodonite rose. lane 1–2.
- **Ocean / biosphere** — halophile blooms (Dunaliella + Halobacterium
  carotenoids) dye a whole brine lagoon pink-red. lane 2 speculative.
- **Ice** — thin tholin over N₂/CH₄ ice cap (Triton/Pluto pinks). lane 1.

### White / grey / black
- White ← thick non-absorbing cloud, water/CO₂/N₂ ice, anorthosite, evaporite
  salt (gypsum/halite), Ceres sodium-carbonate faculae. Grey ← aerosol/silicate
  haze, mineral cloud (hot), basalt. Black ← carbon/organics, basalt, obsidian
  glass, Mn-oxide desert varnish, ultra-low-albedo hot Jupiter (Na/K + TiO/VO;
  e.g. TrES-2 b). lane 1.

---

## Per-domain tables

Columns: **color · material/mechanism · conditions · persistence → lane ·
real example · in-game hook**. Persistence collapses the routing decision
(common→Phase 3 / rare→cfg-artistic / impossible→reject).

### Atmosphere — scattering & absorption

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| blue | Rayleigh scattering | clear molecular gas, no strong absorber, bright shortwave star | common → P3 | Earth | molecular sky scatters blue |
| deep blue | strong Rayleigh, large clear gas column | thick clear N₂/CO₂, no aerosol, hot bright (F/G) star | common → P3 | Earth at depth | a deep clear ocean of air |
| wan grey-blue | Rayleigh under a red SED | M-dwarf peaks red/IR → little blue to scatter | common → P3 | TRAPPIST-1 worlds (synth) | a sky too starved of blue to be blue |
| cyan / blue | CH₄ absorbs red | cold H₂/He giant + CH₄ | common → P3 | Uranus, Neptune | methane swallows the red light |
| teal / aquamarine | CH₄ + thin high haze softening | cold giant, CH₄ + high haze (Uranus vs Neptune) | common → P3 | Uranus (pale) vs Neptune (deep) | methane blue softened by haze |
| white | optically thick non-absorbing deck | high cloud albedo | common → P3 | Venus top | unbroken bright cloud deck |
| grey / hazy | generic aerosol; silicate haze (hot) | dust load; hot mineral vapor | common → P3 | hazy sub-Neptunes, hot Jup | mineral haze greys the sky |

### Atmosphere — colored gases (intrinsic gas color; exotic)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| yellow-green | Cl₂ (chlorine) gas | halogen-rich, exotic outgassing | rare → artistic | (none natural) | a chlorine-green pall over the air |
| yellow-green (more saturated) | ClO₂ (chlorine dioxide) gas | exotic Cl-O chem, > 11 °C | rare → artistic | (none natural) | a sickly chlorine-dioxide green |
| violet | I₂ (iodine) vapor | iodine volatile, warm | rare → artistic | (none natural) | iodine vapor stains the sky violet |
| red-brown | Br₂ (bromine) vapor | warm, bromine volatile | rare → artistic | (none natural) | bromine vapor, red-brown |
| red-brown | NO₂ / N₂O₄ | warm oxidized-N chem (darkens as T rises) | rare → artistic | (smog analog) | nitrogen-dioxide haze, brown and acrid |
| pale yellow | F₂ (fluorine) gas | extreme reactive halogen chem | rare → artistic (pale) | (none natural) | a faint fluorine-yellow tint |
| pale blue | O₃ (ozone) gas | very thick O₃ column (faint at planetary scale) | rare → artistic (pale) | (Earth O₃ too thin to see) | a faint ozone-blue cast |
| cherry red | S₃ (trisulfur) vapor | hot sulfur vapor (~440 °C) | rare → artistic | volcanic sulfur vapor | trisulfur glows cherry-red in hot air |

### Atmosphere — photochemical haze

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| orange / brown | tholin (CH₄+N₂ → UV-cracked organics) | reducing atmosphere + UV/cosmic-ray flux | common → P3 | Titan, Pluto, Triton | UV-cooked organic smog |
| pale yellow-tan | sulfur / polysulfur photochemical haze | S-bearing volcanic gas + photolysis | common → P3 | Venus upper haze, Io plume tops | a sulfur-tinted photochemical veil |
| upper-sky tint | generalized stratospheric absorber (any stratified absorbing species) | a UV-absorbing layer aloft (O₃, CH₄, SO₂, tholin, NO₂…) | common → P3 | Scatterer useOzone slot (generic) | a high absorbing layer paints the upper sky |

### Atmosphere — *measured* exoplanet reflected color (strongest anchors)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| deep cobalt blue | reflective silicate ("glass rain") clouds scatter blue + Na absorbs > 450 nm | hot Jupiter, mid-altitude silicate clouds | measured → P3 | HD 189733 b (Evans 2013, Ag≈0.4 blue) | sodium and glass-rain clouds, cobalt blue |
| near-black | cloud-free + Na/K + TiO/VO swallow nearly all light | very hot Jupiter, cloud-poor dayside | measured → P3 | TrES-2 b (Ag < ~0.01) | darker than coal — a light-eating world |
| bright mirror-white | thick reflective silicate/metal clouds, very high albedo | metal-rich ultra-hot Neptune/Jupiter | measured → P3 | LTT 9779 b (Ag≈0.8), Kepler-7 b (≈0.38) | a giant metal-cloud mirror in the dark |
| grey / muddy | Na + K broad D-line wings dominate optical | hot Jupiter, cloud-poor | measured (typical) → P3 | most hot Jupiters | alkali vapor drinks the daylight |

### Emission / airglow / aurora (a glow, not reflectance — vivid pure colors)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| vivid green | O I 557.7 nm (atomic-oxygen forbidden line) | O-bearing atmosphere + particle precipitation, ~90–100 km | tie-break → artistic low-conf | Earth aurora/airglow | the classic auroral oxygen green |
| deep red | O I 630.0 nm (high, rarefied O) | thin high O, > 200 km, low-density thermosphere | tie-break → artistic low-conf | Earth high red aurora | high rarefied oxygen burning red |
| yellow | Na D 589 nm (sodium emission/airglow) | excited Na layer (meteoric/volcanic) | tie-break → artistic low-conf | Earth Na airglow, Io Na cloud | a sodium-yellow glow band |
| violet-blue | N₂⁺ 427.8 nm (first-negative band) | N₂ ionized by hard precipitation, < 100 km | tie-break → artistic low-conf | Earth low aurora fringe | the violet lower edge of the curtain |
| crimson (low edge) | N₂ first-positive bands | dense low aurora, energetic electrons | tie-break → artistic low-conf | Earth red-bottomed aurora | nitrogen's crimson skirt |
| faint red shimmer | H Balmer (H-alpha 656 nm) | H-rich (gas-giant) atmosphere + excitation | tie-break → artistic low-conf | gas-giant H₂ aurora | a faint hydrogen-red shimmer |

> Aurora/airglow needs three things: the emitting species, a particle-excitation
> source, and (for organized aurora) a magnetic field. On non-transiting planets
> the field is unmeasured → keep it a flagged low-confidence tie-break, never a
> default. Jupiter's aurora is the most *powerful* in the solar system yet mostly
> UV/IR — power is not visibility.

### Surface — transition-metal chromophores (the vivid-inorganic core)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| vivid emerald green | Cr³⁺ crystal-field (uvarovite, chrome diopside, fuchsite) | trace Cr³⁺ in Ca/Al/Mg silicate, ultramafic/chromite host | uncommon → P3/artistic | uvarovite, chrome diopside | chromium-stained emerald rock |
| rust red / ochre | Fe³⁺ oxide — hematite (α-Fe₂O₃) | oxidized iron + weathering/UV | common → P3 | Mars | oxidized iron bleeds red |
| yellow-brown / ochre | Fe³⁺ oxy-hydroxide — goethite/limonite | hydrated oxidized iron, damp weathering | common → P3 | bog iron, Mars dust | hydrated rust, yellow-brown |
| olive / bottle green | Fe²⁺ in olivine/peridot, pyroxene | fresh unoxidized ultramafic/mafic | common (fresh) → P3 | olivine sand (Papakōlea), peridot | unweathered ferrous-green mantle rock |
| green | Fe²⁺/Fe³⁺ in serpentine | hydrated (serpentinized) ultramafic | common → P3 | serpentinite | water-altered mantle green |
| grey-green (muted) | green clays (glauconite, celadonite, chlorite) | marine/altered-basalt clay, mixed-valence Fe | common → P3 | greensand, celadonite | iron-clay green earth |
| malachite green | Cu²⁺ carbonate (malachite) | secondary Cu, CO₂-rich oxidized weathering | uncommon → P3/artistic | malachite | copper-carbonate green crust |
| azure / deep blue | Cu²⁺ carbonate (azurite) | Cu oxidation zone, high carbonate | uncommon → P3/artistic | azurite | copper blue, azurite |
| bright turquoise / cyan | Cu²⁺ (turquoise, chrysocolla, atacamite) | arid Cu weathering; atacamite needs Cl-rich/saline | rare → artistic | turquoise, chrysocolla | desert copper turquoise |
| rose / pink | Mn²⁺ carbonate/silicate (rhodochrosite, rhodonite) | Mn-rich carbonate/metamorphic, reducing | uncommon → P3/artistic | rhodochrosite | manganese-pink rock |
| sooty black veneer | Mn³⁺/⁴⁺ oxides (desert varnish) | arid surface, Mn-oxide coating over time | common → P3 | desert varnish | manganese-blackened varnish |

### Surface — non-metal vivid chromophores (rare but genuine inorganic)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| ultramarine blue | S₃⁻ trisulfur radical in aluminosilicate cage (lazurite) | S-bearing alkaline metamorphism, reducing-then-trapped | rare → artistic | lapis lazuli | trapped sulfur radicals glow blue |
| ruby red / orange | As–S charge-transfer (realgar α-As₄S₄) | low-T hydrothermal/volcanic As+S, fumaroles | rare → artistic | realgar | arsenic-sulfide ruby crust |
| golden yellow | As–S (orpiment As₂S₃) | higher-T As+S, hot-spring/fumarole | rare → artistic | orpiment | gold-yellow arsenic glass |
| scarlet / vermilion | HgS charge-transfer (cinnabar) | low-T Hg-rich hydrothermal/volcanic vents | rare → artistic | cinnabar | mercury-sulfide vermilion |

### Surface — common rock, ice, sulfur, carbon, melt

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| dark grey / black | basalt, mafic/ultramafic silicate | volcanic, unweathered | common → P3 | Moon maria, Mercury | fresh basaltic plains |
| light grey / white | anorthosite / plagioclase feldspar | feldspathic highland crust | common → P3 | lunar highlands | bright feldspathic rock |
| pinkish grey | granite (K-feldspar + quartz) | felsic continental crust | common → P3 | granite shields | pink-grey granite |
| bright white | sulfate/evaporite (gypsum, halite, anhydrite) | evaporated brine, arid basin | common → P3 | White Sands, salt flats | blinding white salt flat |
| brilliant white spot | sodium-carbonate brine evaporite | cryovolcanic brine reaching surface | common → P3 | Ceres / Occator faculae | bright salt-fountain residue |
| bright yellow | elemental sulfur (S₈, cool) | S volcanism/fumaroles, cold-quenched | common → P3 | Io plains | sulfur-paved volcanic plains |
| orange → red → black | hot sulfur allotropes (heat-shifted) | molten/hot sulfur near vents | common → P3 | Io hot flows | hot sulfur darkens toward the vent |
| bright white | clean water ice / frost | cold surface, fresh H₂O grains | common → P3 | Europa, Enceladus | clean water-ice shell |
| white | CO₂ / N₂ / CH₄ volatile frost | very cold, condensed volatiles | common → P3 | Mars caps, Triton, Pluto | frozen-volatile frost |
| glacial blue / cyan | thick clear ice — O–H overtone absorbs red over long path | dense, bubble-free, compressed/deep ice | common (needs depth) → P3 | glacial blue ice | deep ice swallows the red |
| red-brown / salmon | tholin staining on ice (irradiated CH₄+N₂) | UV/cosmic-ray-processed methane on cold ice | common → P3 | Pluto, Charon pole, Triton | radiation-tanned organic ice |
| very dark / black | graphite / soot / refractory organics | C-rich primitive material | common → P3 | C-type asteroids, comet crust | carbon-blackened crust |
| jet black (glassy) | obsidian / silicate volcanic glass | rapid-quenched felsic-intermediate melt | common → P3 | obsidian flows | glass-black quenched lava |
| dull red glow | blackbody incandescence onset (Draper ~800 K) | surface T ≳ 800 K | conditional → P3 if T clears | hot lava skin | first dull-red heat glow |
| orange → white-hot glow | hotter blackbody | T ≈ 1000–1500+ K | conditional → P3 | active lava, 55 Cnc e dayside | molten rock glowing in the visible |

> "Nitrogen-ice pink" is **not** intrinsic N₂ color — it's a thin tholin layer
> from irradiated methane on N₂/CH₄ ice. Attribute it to tholin, not nitrogen.

### Ocean / surface liquid

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| deep blue | pure water — overtone red-absorption + scattering of blue | clear deep water column | common → P3 | Earth open ocean | water eats the red, scatters the blue |
| turquoise / milky cyan | glacial rock flour suspended (scatters blue-green) | fine mineral suspension from erosion | common → P3 | Lake Louise, meltwater lakes | rock dust turns the water glacier-blue |
| green | dissolved Fe(II) opens a green window (absorbs blue + red) | anoxic, ferruginous (Archean-type) | uncommon → P3/artistic | early-Earth "green ocean" hypothesis | a ferrous sea under an oxygen-free sky |
| rusty red | suspended ferric iron oxide | oxidized iron-laden water, river plumes | uncommon → P3/artistic | iron-stained estuaries | iron rust clouding the shallows |
| brown / tea | CDOM (dissolved organics, tannins) absorbs blue+UV | organic-rich, swampy catchment | common → P3 | Rio Negro, blackwater rivers | tannin-stained tea-dark water |
| dark / near-black | liquid hydrocarbons (CH₄/C₂H₆), low albedo | very cold (~90 K) hydrocarbon cycle | common (cold) → P3 | Titan, Kraken Mare | a methane-ethane sea, black and still |
| pale / colorless | liquid sulfuric acid / concentrated brine | hot S-rich (acid) or evaporite brine | uncommon → P3/artistic | Venus-droplet analog | a caustic glassy surface liquid |
| glowing orange-red | incandescent molten silicate (lava lake) | T_surf ≳ ~1000–1300 K, active volcanism | conditional → P3 if T clears | Io paterae, 55 Cnc e | molten rock glowing like an ember |
| pink / red | halophile carotenoids (Dunaliella + Halobacterium) | hypersaline brine, high UV | speculative → artistic | Lake Hillier, saltern ponds | a brine lagoon dyed by salt-loving microbes |
| green / teal | phytoplankton / chlorophyll bloom | life, nutrient-rich shallows | speculative → artistic | Earth coastal blooms | bloom-tinted living shallows |

### Biological pigments (life-dependent → speculative, but the most vivid)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| vivid green | chlorophyll a/b — tuned band-pass (absorbs red ~660 + blue ~430) | oxygenic photosynthesis, Sun-like visible flux | speculative → artistic | Earth vegetation | the green of light-eating life |
| deep red / maroon | far-red chlorophyll f / bacteriochlorophyll (windows shifted to ~700–1000 nm) | photosynthesis under a red/M-dwarf SED | speculative → artistic | far-red cyanobacteria | foliage tuned to a red sun's light |
| orange / yellow | carotenoids (β-carotene, bacterioruberin) | accessory/photoprotective pigment | speculative → artistic | autumn foliage, Dunaliella | carotenoid-orange ground cover |
| deep red | phycoerythrin (absorbs green ~530–570 nm) | red algae / cyanobacteria, deeper water | speculative → artistic | red algae | algae reddened to catch deep green light |
| blue / blue-green | phycocyanin (absorbs orange-red ~610–660 nm) | cyanobacteria, surface films | speculative → artistic | cyanobacterial mats | a blue-pigmented microbial mat |
| purple / magenta | retinal (bacteriorhodopsin) — absorbs green ~568 nm | "Purple Earth" retinal phototrophy | speculative → artistic | hypothesis (DasSarma & Schwieterman) | a retinal-pigment biosphere, purple |
| red→purple→blue | anthocyanins — pH-dependent vacuolar pigment | plant tissue, stress/cold response | speculative → artistic | autumn / blue flowers | pH-tunable pigment painting the flora |
| brown / black | melanin — broadband absorber (NOT vivid) | photoprotective, high-UV surface | speculative → artistic | dark biological crusts | UV-shielding pigment darkening the surface |

### Cloud (condensate + chromophore; cold → hot ladder)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| white | water-ice cloud (non-absorbing, high scattering) | T allows H₂O condensation | common → P3 | Earth | bright water-ice cloud deck |
| white | ammonia (NH₃) ice cloud | cold giant, NH₃ condenses (~150 K) | common → P3 | Jupiter/Saturn zones | frozen-ammonia cloud tops |
| bright white | methane/ethane ice cloud | very cold ice-giant atmosphere | common → P3 | Neptune bright clouds, Titan | high methane-ice cirrus |
| brown / tan | NH₄SH — colorless fresh, radiolysis/UV products absorb blue | giant-planet belt chemistry, warm layer | common → P3 | Jupiter belts | ammonium-sulfide brown belts |
| yellowish-white | sulfuric-acid (H₂SO₄) aerosol droplets | S volcanism, hot thick atmosphere | common → P3 | Venus | a sulfuric-acid cloud veil |
| red (uncertain) | unknown chromophore — radiolyzed NH₄SH / S-P photochem / Carlson NH₃+acetylene | upwelling lifts S/P gas to UV-lit cloud tops | uncertain → P3 low-conf | Jupiter Great Red Spot | a photochemical red on the storm tops |
| grey / muddy (hot) | silicate + iron + corundum mineral clouds | hot (L-dwarf / hot-Jupiter), ~1300–2000 K | measured (BDs) → P3 | L dwarfs, hot Jupiters | clouds of molten rock and iron dust |
| salt-and-sulfide haze | low-T mineral clouds — KCl, ZnS, Na₂S, MnS, Cr | ~600–1400 K (T-dwarf / warm giant) | measured → P3 | T dwarfs | salt-and-sulfide haze in a warm sky |
| very red (NIR) | thick mineral-dust clouds redden a young/dusty atmosphere | dusty L-dwarf / low-gravity giant | measured → P3 | HR 8799 b/c/d, ULAS J2227 | dust so thick the whole world glows red |

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
**unconstrained**, no veto possible. A green *atmosphere* (gas tint) has no clean
mechanism — Cl₂/ClO₂ only reach yellow-green → lane 2, weak hook. But a green
*world* is easy: route the green to the **surface** (Cr³⁺ emerald / serpentine /
olivine — inorganic, no life) or to **vegetation** (chlorophyll, lane 2
speculative), optionally with an **O I 557.7 nm green airglow** at the limb.
**Verdict: keep the green** — as a green surface (best-grounded) ± green airglow,
not as a green gas tint. In-game: *"Tau Ceti e wears a chromium-and-serpentine
green crust under a faint oxygen-green airglow."* (Value-check mineral color
claims against a source before committing the entry.)

**Vivid green, no life — the inorganic route.** When the user wants saturated
green without invoking biology: Cr³⁺ minerals (uvarovite/chrome diopside/fuchsite)
give the purest inorganic emerald; Cu²⁺ malachite a strong green; serpentine/
olivine a broader olive crust. All lane 1–2, no veto on a non-transiting world.

**"Thick atmosphere on TRAPPIST-1 b" — rejected.** JWST emission (Greene 2023)
shows a bare-rock dayside → thick atmosphere **vetoed at step 1**, regardless of
appeal. Alternative offered: dark basaltic/ultramafic bare-rock surface tint,
no sky.

---

## Notes on use
- This catalog uses textbook/established color chemistry. Rows marked **rare /
  artistic / speculative / uncertain** carry low confidence and **must be
  source-pinned at point-of-use** (value-check discipline) when written into a
  real body's Phase 3 doc or cfg.
- For the purest saturated colors, prefer an **emission** mechanism (airglow/
  aurora) or a **transition-metal/biological** chromophore over a gas tint or
  generic scattering — broadband scattering tends pale.
- Reflectance vs starlight convention follows `disk-color.md`: intrinsic
  material color, with the renderer/star applying illumination. For the disk
  domain use the Mie engine (`scripts/phase3/disk_color_mie.py`), not this table.
- Aurora *emission-line* colors (the exact wavelengths) are cataloged in
  [`element-plasma-colors.md`](./element-plasma-colors.md); firefly
  `composition-color.md` covers reentry-plasma bulk-gas colors.
- Wiring into the synthesis flow (a formal color gate in SKILL.md + a
  `## Color` proposal section) is pending the idea-#2 architecture decision
  (Phase 3 extension vs Phase 4). This doc is the architecture-neutral
  foundation both would use.
