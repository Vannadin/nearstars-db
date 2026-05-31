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
  or charge-transfer chromophore mineral, structural iridescence) → **lane 2:
  cfg-artistic override**, the same flagged downstream layer as moons and
  synthetic eccentricity. Confidence=low, documented divergence, **but carries a
  genuine chemistry hook** — not fabrication.
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

Read this before reaching for a color; it names the mechanisms and explains why
some hues are cheap and some are exotic.

- **The band-pass rule (why pure green/magenta are hard).** A green look must
  absorb *both* red and blue while passing green; magenta must pass red *and*
  blue while notching out green. Common single absorbers kill one side only
  (CH₄ eats red → reads blue/cyan), so they slide toward blue or red/brown,
  never cleanly green or magenta. Those need a tuned narrow-notch absorber
  (chlorophyll, retinal) or an intrinsically colored species → usually lane 2.
- **The three inorganic color engines.** Vivid mineral color comes from one of:
  (1) **d-d crystal field** — a transition-metal ion's d-orbital transition
  (Cu²⁺ blue/green, Cr³⁺ green *or* red, Mn²⁺ pink, Mn³⁺ purple, Co²⁺ pink,
  V³⁺ violet); (2) **intervalence charge transfer (IVCT)** — an electron hops
  between two adjacent metal ions, a *very* strong absorber so a trace gives a
  deep color (Fe²⁺→Ti⁴⁺ sapphire blue, Fe²⁺→Fe³⁺ vivianite); (3) **radiation
  color centers** — irradiation + a trace dopant traps a defect (amethyst purple,
  purple fluorite, amazonite blue-green). Crystal field gives most hues; IVCT
  gives the *deepest blues*; color centers give irradiated purples/blues.
- **The band-gap ruler (semiconductor warm series).** For sulfide/oxide
  semiconductors the band gap sets the color and slides smoothly:
  Eg ≳ 3.0 eV → white (S₈-poor, TiO₂) · ~2.6 eV → **yellow** (S₈, orpiment) ·
  ~2.2 eV → **orange-red** (hematite) · ~2.0 eV → **deep red** (cinnabar) ·
  ≲ 1.7 eV → **black**. Lowering Eg walks yellow→orange→red→black — that's why
  the S / As–S / Hg–S / Fe-oxide series is one gradient, not four coincidences.
- **Emission can be vivid where reflectance cannot.** Reflectance/scattering is
  broadband → pale or muddy. Emission lines are narrow → airglow/aurora show
  *pure, saturated* hues (O I 557.7 nm green, N₂⁺ 427.8 nm violet-blue) no
  reflective surface can match. **For a vivid pure color, reach for a glow.**
- **Structural color is a separate category** (see its own section). Color from
  wavelength-scale *structure* (thin films, lamellae, sphere lattices)
  interfering with light, not from absorption. It is **goniochromic** — the hue
  shifts with viewing angle (opal fire, labradorite flash, oil-slick) — and
  cannot be faked with a flat diffuse tint; it needs an iridescence/specular
  shader.
- **Metallic luster is a finish, not a hue.** Pyrite gold, native gold, an
  M-type metal world (16 Psyche) read metallic because of high *specular*,
  angle-independent reflection — the cfg cue is a metallic/specular material,
  not a diffuse albedo color. And exposed Fe-Ni reads *dark gunmetal*, not a
  bright mirror (Psyche visible albedo ~0.1–0.3).
- **Oxidation state and fresh-vs-weathered set the hue.** Fe²⁺ → greens
  (olivine, serpentine); Fe³⁺ → reds/yellow-browns (hematite, goethite). Same
  element, opposite color. Fresh/reducing = green; weathered/oxidizing =
  red-yellow. Mn-oxide varnish blackens exposed rock over time.
- **Biology makes the most vivid colors** because pigments are tuned narrow-band
  absorbers (chlorophyll notches red+blue; phycoerythrin ~530–570 nm; retinal
  ~568 nm → magenta). But it's life-dependent → speculative. (Melanin is the
  exception — broadband → dark brown/black, not vivid.)
- **Cool stars red-shift the sky.** Rayleigh ∝ λ⁻⁴, but you can only scatter the
  blue the star emits. An M-dwarf's red/IR-peaked SED leaves little short-λ flux
  → the same clear atmosphere reads wan grey-blue, not vivid blue. *Caveat:* a
  pure-violet/lavender Rayleigh sky is **not** physical under a Sun-like star
  (violet depletion + eye response) — don't route lavender to plain Rayleigh.
- **Incandescence is set by temperature, not composition** — blackbody, first
  dull-red glow at the Draper point (~800 K), through orange/yellow to white-hot
  (≳1500 K). Route only if surface T clears the threshold.
- **Cloud color follows a condensation-temperature ladder.** Cold→hot:
  CH₄/N₂/H₂O/NH₃ ices (white) → NH₄SH + tholin (brown/tan) → H₂SO₄ (yellow-white)
  → low-T salts/sulfides KCl, ZnS, Na₂S, MnS, Cr (~600–1400 K) → silicate/iron/
  corundum (~1300–2000 K, grey mineral dust). Pick the species from cloud-deck T.
- **Hot Jupiters default dark; bright ones are the exception.** Broad Na/K wings
  (plus TiO/VO in the hottest) drink the optical → most measured hot Jupiters are
  low-albedo (TrES-2 b ≈ black). High albedo needs reflective silicate/metal
  clouds (HD 189733 b blue, LTT 9779 b mirror).

---

## Vivid color playbook (color-indexed; the primary entry point)

"I want an *X* world" → here are the plausible realizations across domains and
which lane each lands in. Detail rows are in the per-domain tables below.

### Blue
- **Atmosphere** — Rayleigh (clear molecular column; vivid only under a bright
  blue-rich star) · CH₄ on a cold giant (Neptune) · measured cobalt on hot
  Jupiter HD 189733 b (silicate clouds + Na). lane 1.
- **Surface (vivid, no life)** — IVCT sapphire (Fe²⁺→Ti⁴⁺, the deepest) ·
  lazurite/lapis ultramarine (S₃⁻ radical) · Cu²⁺ azurite · hydrated copper
  sulfate (blue wet, white dry) · amazonite (Pb radiation centers). lane 1–2.
- **Ice / water** — glacial blue ice & deep water (O–H vibrational overtone
  absorbs red — needs depth/clarity). lane 1.
- **Emission** — N₂⁺ 427.8 nm violet-blue auroral fringe. tie-break.
- *Most grounded:* Rayleigh + deep-water/ice overtone (pure physics). *Most vivid:*
  sapphire IVCT / lazurite.

### Cyan / teal
- **Atmosphere** — CH₄ + high haze (Uranus pale vs Neptune deep). lane 1.
- **Surface** — Cu²⁺ turquoise / chrysocolla / atacamite (arid or saline Cu
  weathering). lane 1–2.
- **Ocean** — glacial rock-flour suspension · shallow water over bright sand. lane 1.

### Green
- **Surface (vivid, no life — the headline)** — Cr³⁺ emerald (uvarovite, chrome
  diopside, fuchsite) is the purest inorganic green; Cu²⁺ malachite; olivine/
  serpentine give a subtler olive. lane 1–2.
- **Emission** — O I 557.7 nm airglow/aurora is the purest green there is (a limb
  glow). tie-break.
- **Biology** — chlorophyll vegetation / phytoplankton. lane 2 speculative.
- **Ocean** — dissolved Fe(II) "ferrous sea" (Archean hypothesis). lane 2.
- **Atmosphere (gas)** — only yellow-green (Cl₂/ClO₂); no clean pure-green gas
  → atmospheric green is essentially artistic. lane 2 + weak hook.

### Purple / violet / indigo
- **Surface (vivid, no life)** — Mn³⁺ minerals (purpurite, sugilite, charoite)
  are the real purple chromophore — Mn³⁺ is to purple what Cr³⁺ is to green ·
  V³⁺ tanzanite blue-violet · amethyst & purple fluorite (radiation color
  centers). lane 2.
- **Atmosphere** — I₂ (iodine) vapor is genuinely violet. lane 2 + hook.
- **Biology** — retinal "Purple Earth" (DasSarma & Schwieterman); anthocyanin
  flora (pH-tunable). lane 2 speculative.
- **Emission** — N₂⁺ 427.8 nm violet glow. tie-break.
- *Veto:* plain Rayleigh does **not** give a lavender sky under a Sun-like star.

### Pink / rose / magenta
- **Surface (no life)** — Mn²⁺ rhodochrosite/rhodonite rose · Co²⁺ erythrite
  ("cobalt bloom") crimson-pink · rose quartz (Fe-Ti inclusion IVCT, pale only).
  lane 1–2.
- **Biology** — halophile brine lagoons (carotenoids/bacterioruberin) ·
  retinal magenta · anthocyanins. lane 2 speculative.
- **Ice** — thin tholin over N₂/CH₄ ice (Triton/Pluto). lane 1.
- *Magenta is non-spectral* — needs a green-notch absorber → retinal (life),
  Co²⁺, or IVCT, never broadband scattering.

### Red / crimson / maroon
- **Surface** — hematite (Fe³⁺, the ubiquitous planetary red, Mars) · cinnabar
  (HgS, most saturated) · Cr³⁺ ruby (same ion as emerald, flipped by the host
  lattice) · realgar (As-S). lane 1 (hematite) / lane 2 (Hg, As, ruby).
- **Emission** — O I 630.0 nm red aurora (high rarefied O). tie-break.
- **Biology** — phycoerythrin red algae · far-red chlorophyll maroon (M-dwarf
  foliage). lane 2 speculative.
- **Incandescent** — dull-red glow at T ≳ 800 K. conditional.

### Orange
- **Atmosphere/haze** — tholin (low-pressure → orange-red; high-pressure →
  yellow). lane 1.
- **Surface** — hot sulfur allotropes (Io vents) · realgar · incandescent ~1000 K.
  lane 1.
- **Biology** — carotenoids. lane 2 speculative.

### Yellow
- **Surface (vivid, no life)** — elemental sulfur S₈ (band-gap yellow; Io plains)
  is grounded *and* vivid · orpiment (As-S) gold-yellow · jarosite/goethite
  yellow-brown. lane 1 (S₈) / lane 2 (As).
- **Cloud/haze** — H₂SO₄ + sulfur haze (Venus, pale) · high-pressure tholin. lane 1.
- **Emission** — Na D 589 nm sodium glow. tie-break.

### Gold / metallic *(a finish, not a hue)*
- **Surface** — pyrite FeS₂ brass-gold (ubiquitous, grounded) · native gold /
  electrum (true gold, rare) · peacock-ore bornite (iridescent tarnish, see
  structural) · specular hematite & Fe-Ni metal (steely). lane 1–2.
- **Whole world** — M-type metal asteroid (16 Psyche): real, but reads *dark
  gunmetal* with a specular sheen, not a bright mirror. lane 2, flag dark.
- *cfg cue:* high specular + metallic material, not a diffuse tint.

### Brown / tan *(the realistic baseline — intrinsically muddy)*
- Goethite/limonite ochre · NH₄SH belts · tholin haze · CDOM tea-water ·
  desert varnish · mixed regolith. All lane 1. No vivid option exists — use as
  the honest default, not the spectacle.

### White / grey / black / silver
- **White** ← volatile ice (H₂O/CO₂/N₂/CH₄), SO₂ frost (Io), anorthosite/feldspar,
  evaporite salt (gypsum/halite), Ceres Na-carbonate faculae, NH₃ cloud, metal-
  cloud LTT 9779 b. **Grey** ← basalt, weathered regolith, aerosol/silicate haze,
  hot mineral cloud (the no-chromophore default). **Black** ← carbon/organics,
  obsidian, Mn varnish, ultra-dark hot Jupiter (TrES-2 b). **Silver** ← Fe-Ni
  metal (specular, neutral). lane 1.

### Iridescent / structural *(goniochromic — needs a special shader)*
- Opal play-of-color (silica sphere lattice) · nacre · labradorite/spectrolite
  flash · moonstone structural blue · bornite/bismuth tarnish-film rainbows ·
  oil-slick/frost films. Vivid but **viewing-angle dependent** → lane 2 artistic
  with a rendering caveat (not a flat tint). See the structural section.

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
| orange / brown | tholin (CH₄+N₂ → UV-cracked organics), low-pressure | reducing atmosphere + UV/cosmic-ray flux | common → P3 | Titan, Pluto, Triton | UV-cooked organic smog |
| yellow-tan | tholin (high-pressure films) / sulfur photochemical haze | denser organic haze; or S-bearing gas + photolysis | common → P3 | deep Titan haze, Venus, Io tops | a sulfur-and-organic photochemical veil |
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
> the field is unmeasured → keep it a flagged low-confidence tie-break.

### Surface — crystal-field & charge-transfer chromophores (the vivid-inorganic core)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| vivid emerald green | Cr³⁺ crystal field (uvarovite, chrome diopside, fuchsite) | trace Cr³⁺ in Ca/Al/Mg silicate, ultramafic/chromite host | uncommon → P3/artistic | uvarovite | chromium-stained emerald rock |
| blood-red | Cr³⁺ crystal field in corundum (strong field flips it red) | trace Cr in Al₂O₃, short Cr–O bonds | rare → artistic | ruby | chromium ruby-red (same ion as emerald) |
| rust red / ochre | Fe³⁺ oxide — hematite (α-Fe₂O₃) | oxidized iron + weathering/UV | common → P3 | Mars | oxidized iron bleeds red |
| yellow-brown | Fe³⁺ oxy-hydroxide — goethite/limonite/jarosite | hydrated oxidized iron; jarosite = acid-sulfate | common → P3 | bog iron, Mars dust | hydrated rust, yellow-brown |
| olive / bottle green | Fe²⁺ in olivine/peridot, pyroxene | fresh unoxidized ultramafic/mafic | common (fresh) → P3 | olivine sand (Papakōlea) | unweathered ferrous-green mantle rock |
| green | Fe²⁺/Fe³⁺ in serpentine / green clays | hydrated (serpentinized) ultramafic; or marine clay | common → P3 | serpentinite, greensand | water-altered mantle green |
| malachite green | Cu²⁺ carbonate (malachite) | secondary Cu, CO₂-rich oxidized weathering | uncommon → P3/artistic | malachite | copper-carbonate green crust |
| azure / deep blue | Cu²⁺ carbonate (azurite) | Cu oxidation zone, high carbonate | uncommon → P3/artistic | azurite | copper blue, azurite |
| turquoise / cyan | Cu²⁺ (turquoise, chrysocolla, atacamite) | arid Cu weathering; atacamite needs Cl-rich/saline | rare → artistic | turquoise | desert copper turquoise |
| vivid blue (bleaches dry) | Cu²⁺ d-d in hydrated [Cu(H₂O)₆]²⁺ | hydrated copper-sulfate efflorescence, arid Cu weathering | uncommon → P3/artistic | chalcanthite | copper salt, blue when wet, white when dry |
| rose / pink | Mn²⁺ carbonate/silicate (rhodochrosite, rhodonite) | Mn-rich carbonate/metamorphic, reducing | uncommon → P3/artistic | rhodochrosite | manganese-pink rock |
| violet → royal purple | Mn³⁺ crystal field (purpurite, sugilite, charoite) | oxidized Mn in phosphate/alkaline silicate | rare → artistic | sugilite | manganese purple (purple's Cr³⁺) |
| crimson → pink | Co²⁺ crystal field (erythrite, "cobalt bloom") | secondary hydrated Co-arsenate over Co ore | rare → artistic | erythrite | a crimson cobalt-bloom crust |
| blue-violet (pleochroic) | V³⁺ crystal field in zoisite | trace vanadium in Ca-Al silicate, metamorphic | rare → artistic | tanzanite | vanadium-stained zoisite, blue-violet |
| deep sapphire blue | Fe²⁺→Ti⁴⁺ intervalence charge transfer (IVCT) | trace Fe+Ti on adjacent Al sites in Al₂O₃ | rare → artistic | sapphire | iron-titanium electron-trade burns it blue |
| blue → indigo (in light) | Fe²⁺→Fe³⁺ internal photo-oxidation of iron(II) phosphate | anoxic, P-rich, Fe-rich sediment; deepens in light/air | uncommon → P3/artistic | vivianite | ferrous phosphate that oxidizes itself blue |
| pale rose | Fe–Ti IVCT in dumortierite-like nanofiber inclusions | massive quartz with trace Ti+Fe borosilicate fibers | rare → artistic (pale) | rose quartz | a faint rose-quartz blush |
| sooty black veneer | Mn³⁺/⁴⁺ oxides (desert varnish) | arid surface, Mn-oxide coating over time | common → P3 | desert varnish | manganese-blackened varnish |

### Surface — band-gap semiconductor, radical & color-center chromophores

> Band-gap ruler: lowering Eg walks **yellow → orange → red → black** (S₈ ~2.6 →
> hematite ~2.2 → cinnabar ~2.0 eV). Radical and color-center routes are separate
> mechanisms grouped here.

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| lemon → golden yellow | elemental sulfur S₈ band-gap (~2.6 eV) | cold-quenched S volcanism/fumaroles | common → P3 | Io plains | sulfur-yellow volcanic pavement |
| golden yellow | orpiment As₂S₃ band-gap | higher-T As+S fumarole/hot-spring | rare → artistic | orpiment | a gold-yellow arsenic glass |
| ruby red / orange | realgar α-As₄S₄ band-gap/charge transfer | low-T hydrothermal/volcanic As+S | rare → artistic | realgar | arsenic-sulfide ruby crust |
| scarlet / vermilion | cinnabar HgS band-gap (~2.0 eV) | low-T Hg-rich hydrothermal/volcanic vents | rare → artistic | cinnabar | mercury-sulfide vermilion |
| ultramarine blue | S₃⁻ trisulfur radical in aluminosilicate cage (lazurite) | S-bearing alkaline metamorphism, reducing-then-trapped | rare → artistic | lapis lazuli | trapped sulfur radicals glow blue |
| purple (heat-fades to yellow) | Fe³⁺ + γ-irradiation → hole color center in quartz | trace Fe in quartz + U/Th/K-40 dose | uncommon → P3/artistic | amethyst | irradiated iron-doped quartz; citrine when heated |
| green→blue→purple | colloidal-Ca + F-center color centers in fluorite | CaF₂ near radioactive host, irradiated | rare → artistic | purple fluorite | radiation-grown calcium colloids |
| blue-green | Pb + water radiation color centers in microcline | K-feldspar with Pb + bound H₂O, irradiated | rare → artistic | amazonite | irradiated lead-bearing feldspar |

### Surface — metallic / specular luster (a distinct LOOK — high specular, angle-independent)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| brass-gold (metallic) | pyrite FeS₂ metallic luster | sulfidic/hydrothermal Fe-S deposits | common → P3 | pyrite ("fool's gold") | a brassy metallic sheen, fool's gold |
| true / pale gold | native gold / electrum (Au, Ag-alloyed) | native-metal concentration, hydrothermal | rare → artistic | native gold | a buttery native-gold luster |
| steely silver-grey | specular hematite + iron-nickel metal | exposed metal/specularite, polished oxide | uncommon → P3/artistic | specularite, meteoric Fe-Ni | a polished steel-grey sheen |
| dark gunmetal (metallic) | M-type asteroid Fe-Ni metal regolith (exposed-core analog) | disrupted differentiated body, metal-rich crust | rare → artistic (dark, not mirror) | 16 Psyche | a stripped metal core, gunmetal-dull |

### Surface — common rock, ice, sulfur, carbon, melt

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| dark grey / black | basalt, mafic/ultramafic silicate | volcanic, unweathered | common → P3 | Moon maria, Mercury | fresh basaltic plains |
| light grey / white | anorthosite / plagioclase feldspar | feldspathic highland crust | common → P3 | lunar highlands | bright feldspathic rock |
| pinkish grey | granite (K-feldspar + quartz) | felsic continental crust | common → P3 | granite shields | pink-grey granite |
| mid-grey (featureless) | space-weathered mixed regolith | airless body, micrometeorite + solar-wind gardening | common → P3 | most airless surfaces | weathered regolith greys to a default |
| bright white | sulfate/evaporite (gypsum, halite, anhydrite) | evaporated brine, arid basin | common → P3 | White Sands, salt flats | blinding white salt flat |
| brilliant white spot | sodium-carbonate brine evaporite | cryovolcanic brine reaching surface | common → P3 | Ceres / Occator faculae | bright salt-fountain residue |
| bright yellow | elemental sulfur (S₈, cool) | S volcanism/fumaroles, cold-quenched | common → P3 | Io plains | sulfur-paved volcanic plains |
| white frost | SO₂ frost (high-scattering condensate) | active S volcanism + cold traps; vents stay dark | common → P3 | Io (Colchis Regio) | volcanic sulfur-dioxide frost whitens the plains |
| orange → red → black | hot sulfur allotropes (heat-shifted) | molten/hot sulfur near vents | common → P3 | Io hot flows | hot sulfur darkens toward the vent |
| bright white | clean water ice / frost | cold surface, fresh H₂O grains | common → P3 | Europa, Enceladus | clean water-ice shell |
| white | CO₂ / N₂ / CH₄ volatile frost | very cold, condensed volatiles | common → P3 | Mars caps, Triton, Pluto | frozen-volatile frost |
| glacial blue / cyan | thick clear ice — O–H overtone absorbs red over long path | dense, bubble-free, compressed/deep ice | common (needs depth) → P3 | glacial blue ice | deep ice swallows the red |
| red-brown / salmon | tholin staining on ice (irradiated CH₄+N₂) | UV/cosmic-ray-processed methane on cold ice | common → P3 | Pluto, Charon pole, Triton | radiation-tanned organic ice |
| very dark / black | graphite / soot / refractory organics | C-rich primitive material | common → P3 | C-type asteroids, comet crust | carbon-blackened crust |
| jet black (glassy) | obsidian / silicate volcanic glass | rapid-quenched felsic-intermediate melt | common → P3 | obsidian flows | glass-black quenched lava |
| dull red → white-hot glow | blackbody incandescence (Draper ~800 K → ≳1500 K) | surface T clears the threshold | conditional → P3 if T clears | active lava, 55 Cnc e dayside | molten rock glowing in the visible |

> "Nitrogen-ice pink" is **not** intrinsic N₂ color — it's a thin tholin layer
> from irradiated methane on N₂/CH₄ ice. Attribute it to tholin, not nitrogen.

### Ocean / surface liquid

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| deep blue | pure water — overtone red-absorption + scattering of blue | clear deep water column | common → P3 | Earth open ocean | water eats the red, scatters the blue |
| turquoise / milky cyan | glacial rock flour suspended (scatters blue-green) | fine mineral suspension from erosion | common → P3 | Lake Louise | rock dust turns the water turquoise |
| tropical cyan | short-path scattering over a bright shallow floor | shallow clear water over carbonate/quartz sand | common → P3 | tropical lagoons | shallow water over bright sand glows cyan |
| green | dissolved Fe(II) opens a green window (absorbs blue + red) | anoxic, ferruginous (Archean-type) | uncommon → P3/artistic | early-Earth "green ocean" hypothesis | a ferrous sea under an oxygen-free sky |
| rusty red | suspended ferric iron oxide | oxidized iron-laden water, river plumes | uncommon → P3/artistic | iron-stained estuaries | iron rust clouding the shallows |
| brown / tea | CDOM (dissolved organics, tannins) absorbs blue+UV | organic-rich, swampy catchment | common → P3 | Rio Negro, blackwater rivers | tannin-stained tea-dark water |
| dark / near-black | liquid hydrocarbons (CH₄/C₂H₆), low albedo | very cold (~90 K) hydrocarbon cycle | common (cold) → P3 | Titan, Kraken Mare | a methane-ethane sea, black and still |
| pale / colorless | liquid sulfuric acid / concentrated brine | hot S-rich (acid) or evaporite brine | uncommon → P3/artistic | Venus-droplet analog | a caustic glassy surface liquid |
| glowing orange-red | incandescent molten silicate (lava lake) | T_surf ≳ ~1000–1300 K, active volcanism | conditional → P3 if T clears | Io paterae, 55 Cnc e | molten rock glowing like an ember |
| pink / red | halophile carotenoids (Dunaliella + Halobacterium/Salinibacter) | hypersaline brine, high UV | speculative → artistic | Lake Hillier | a brine lagoon dyed by salt-loving microbes |
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
| white | ammonia (NH₃) ice cloud (pure) | cold giant, NH₃ condenses (~150 K) | common → P3 | Jupiter pure-NH₃ regions | frozen-ammonia cloud tops |
| bright white | methane/ethane ice cloud | very cold ice-giant atmosphere | common → P3 | Neptune bright clouds, Titan | high methane-ice cirrus |
| brown / tan | NH₄SH — colorless fresh, radiolysis/UV products absorb blue | giant-planet belt chemistry, warm layer | common → P3 | Jupiter belts | ammonium-sulfide brown belts |
| yellowish-white | sulfuric-acid (H₂SO₄) aerosol droplets | S volcanism, hot thick atmosphere | common → P3 | Venus | a sulfuric-acid cloud veil |
| red (uncertain) | unknown chromophore — radiolyzed NH₄SH / S-P photochem / Carlson NH₃+acetylene | upwelling lifts S/P gas to UV-lit cloud tops | uncertain → P3 low-conf | Jupiter Great Red Spot | a photochemical red on the storm tops |
| grey / muddy (hot) | silicate + iron + corundum mineral clouds | hot (L-dwarf / hot-Jupiter), ~1300–2000 K | measured (BDs) → P3 | L dwarfs, hot Jupiters | clouds of molten rock and iron dust |
| salt-and-sulfide haze | low-T mineral clouds — KCl, ZnS, Na₂S, MnS, Cr | ~600–1400 K (T-dwarf / warm giant) | measured → P3 | T dwarfs | salt-and-sulfide haze in a warm sky |
| very red (NIR) | thick mineral-dust clouds redden a young/dusty atmosphere | dusty L-dwarf / low-gravity giant | measured → P3 | HR 8799 b/c/d, ULAS J2227 | dust so thick the whole world glows red |

---

## Structural & interference color (goniochromic — a separate category)

Color from wavelength-scale **physical structure** (thin films, lamellae, sphere
lattices) interfering with light, not from absorption. Unlike everything above,
the hue **shifts with viewing/lighting angle (goniochromism)** and **cannot be
reproduced by a flat diffuse tint** — it needs an iridescence/specular shader, an
environment map, or at minimum a strong specular+fresnel pass. Route to **lane 2
/ artistic with a rendering caveat**: real and groundable, but a *material-finish*
decision, not a flat surface color (the way emission is a special mechanism, not
a tint). Vivid but directional.

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| shifting spectral patches | photonic lattice — Bragg diffraction off ordered ~150–300 nm silica spheres | hydrated silica deposits into a regular sphere lattice | rare → artistic (play-of-color) | precious opal | a buried sphere-lattice fires color as it turns |
| blue/green/gold flash | multilayer interference off ~128–252 nm exsolution lamellae | slow-cooled Ca-rich plagioclase (Bøggild gap) | rare → artistic (directional flash) | labradorite / spectrolite | feldspar lamellae flash labradorite blue |
| floating blue-white sheen | Rayleigh scattering off sub-λ feldspar lamellae (structural, not pigment) | orthoclase-albite intergrowth, lamellae ~120–150 nm | rare → artistic (goniochromic) | moonstone (adularescence) | sub-wavelength lamellae scatter a moonlit blue |
| pastel blue-green sheen | aragonite-platelet thin-film + edge diffraction | layered ~0.5 µm carbonate tablets + organic sheets | rare → artistic (iridescent) | nacre / mother-of-pearl | a layered shell-stack shimmers nacreous |
| rainbow blue-purple-gold | thin-film interference in a wavelength-thin tarnish on Cu-Fe sulfide | bornite surface grows an oxide film ~λ thick | rare → artistic (iridescent) | bornite "peacock ore" | a tarnish-film rainbow over copper ore |
| full-spectrum rainbow | thin-film interference in a bismuth-oxide surface film | bismuth oxidizes on cooling in air | rare → artistic (iridescent) | bismuth crystal | an oxide-film rainbow on bare metal |
| moving rainbow | thin-film interference in a liquid/ice film of varying thickness | a transparent film ~λ thick over a reflective base | conditional → artistic (iridescent) | oil slick, soap bubble, frost film | a thin film of varying depth paints a rainbow |

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
| lavender / violet Rayleigh sky | basic optics — violet depletion + eye response means clear-air scattering reads blue, not violet, under a Sun-like star | (route violet to I₂ gas / Mn³⁺ surface / aurora instead) |

When vetoed, offer the nearest non-contradicted alternative (e.g. thick
atmosphere vetoed on TRAPPIST-1 b → dark basaltic bare-rock surface, thin/no
sky).

---

## Worked examples

**Tau Ceti e — vivid green (the PHM concept).** RV-only (non-transiting): radius,
atmosphere, albedo never measured → **unconstrained**, no veto. A green *gas*
atmosphere has no clean mechanism (Cl₂/ClO₂ only reach yellow-green → lane 2,
weak). But a green *world* is easy: route green to the **surface** (Cr³⁺ emerald /
serpentine, inorganic) or **vegetation** (chlorophyll, lane 2 speculative), ±
an **O I 557.7 nm green airglow**. **Verdict: keep the green** — as a green
surface ± airglow, not a green gas. In-game: *"a chromium-and-serpentine green
crust under a faint oxygen-green airglow."*

**Pick-your-engine — vivid color with no life.** The inorganic palette is wide:
**blue** (IVCT sapphire / lazurite / Cu azurite), **green** (Cr³⁺ emerald /
Cu malachite), **purple** (Mn³⁺ sugilite / amethyst), **red** (cinnabar / Cr³⁺
ruby / hematite), **yellow** (S₈ / orpiment), **pink** (Co²⁺ erythrite / Mn²⁺
rhodochrosite), **gold-metallic** (pyrite / native gold), **iridescent** (opal /
labradorite). None needs a biosphere — the green section is no longer the only
deep one. Each lands lane 1–2 with a real chemistry hook; structural/metallic
ones carry a finish/shader caveat.

**"Thick atmosphere on TRAPPIST-1 b" — rejected.** JWST emission (Greene 2023)
shows a bare-rock dayside → thick atmosphere **vetoed at step 1**. Alternative:
dark basaltic/ultramafic bare-rock surface tint, no sky.

---

## Notes on use
- This catalog uses textbook/established color chemistry. Rows marked **rare /
  artistic / speculative / uncertain** carry low confidence and **must be
  source-pinned at point-of-use** (value-check discipline) when written into a
  real body's Phase 3 doc or cfg.
- For the purest saturated colors, prefer **emission** (airglow/aurora) or a
  **transition-metal / IVCT / biological** chromophore over a gas tint or generic
  scattering — broadband scattering tends pale.
- **Structural and metallic** colors are *material-finish* decisions (specular,
  iridescence, angle), not flat tints — flag the rendering need.
- Reflectance vs starlight convention follows `disk-color.md`: intrinsic
  material color, with the renderer/star applying illumination. For the disk
  domain use the Mie engine (`scripts/phase3/disk_color_mie.py`), not this table.
- Aurora *emission-line* colors (exact wavelengths) are cataloged in
  [`element-plasma-colors.md`](./element-plasma-colors.md); firefly
  `composition-color.md` covers reentry-plasma bulk-gas colors.
- Wiring into the synthesis flow (a formal color gate in SKILL.md + a
  `## Color` proposal section) is pending the idea-#2 architecture decision
  (Phase 3 extension vs Phase 4). This doc is the architecture-neutral
  foundation both would use.
