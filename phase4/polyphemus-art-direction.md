<!-- 폴리페무스(α Cen A b) 비주얼 art-direction Phase 4 초안 — 사용자 창작 영역, 미게이팅 -->
# Phase 4 Draft — Polyphemus (α Cen A b) Visual Art Direction

**Status:** DRAFT · user art-direction · NOT gated, NOT in the DB. Phase 4 is
not yet implemented (see [`README.md`](README.md)); this records the creative
target and the 고증 analysis so it can be activated when Phase 4 is built.

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

A **banded gas giant where Saturn-ivory and Neptune-blue coexist as stripes** —
the *Avatar* Polyphemus look. The intended read is a *luminous, pale* giant (it
is a bright Class I/II world, not a dark one) carrying a strong banded character:

- **Ivory / cream zones** (upwelling bands) — warm, soft, pale cloud tops; the
  dominant tone across the disk.
- **Blue belts** (downwelling, cloud-cleared bands) — cooler stripes showing
  through to deeper, clearer air; a few read as sharper, deeper blue against the
  cream so the banding has rhythm rather than a uniform gradient.
- **A signature storm** — one large cyclonic vortex (a Jupiter Great-Red-Spot
  homage, as in the films), the planet's focal landmark, set in a belt.
- **The Roche-zone ring** (from the Phase 3 synthesis) as a thin, dark framing
  line across the disk — narrow and unobtrusive, not a Saturn-scale ring system.

**From Pandora's sky.** This is the view the moon is famous for: from Pandora's
surface Polyphemus spans **~36°** of the sky (computed in stability-sim — a 1
R_Jup giant at 225,000 km), so the banded cream-and-blue body, its storm, and
the dark ring fill the daylit sky. The art-direction has to read at *that* scale
— a near-filling skyline — not just as a distant disk.

*(Proposed direction; the binding calls — how deep the blue goes, the storm's
placement/size — are left in "Open creative questions" below for the user to set.)*

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
