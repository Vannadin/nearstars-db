# Phase 4 prose-readability pass — context notes (session handoff)

Last updated: 2026-07-27. Read this + `checklist.md` first. Hades, Dante, Pandora and
most of Cassandra are done; `gameplay` is Cassandra's last row.

## The task

Apply the **SPEC §3.1 prose readability contract** to every decision row in
`phase4/alpha_centauri.yaml`, rewriting `narrative` (EN) + `narrative_ko` (KO) so
each reads as a reader-facing story, not a parameter dump.

Canonical contract (3 locations, all say the same thing):
- `phase4/SPEC.md` §3.1
- `nearstars-phase4` skill, Step 4
- memory `feedback-phase4-prose-readability.md`

### The 7 contract criteria

1. narrative = reader-facing story, conclusion-first, **≤ 6 sentences**.
2. NO dates / owner-decision-logs in narrative ("오너가 …", "affirm", "2026-…" → out).
3. NO bibcodes / file-paths / equations / parameter-dumps in narrative
   (those live in `fields:` and `refs:`).
4. NO engine/mod mechanics in narrative (→ `gate.evidence` / `evidence_ko`).
   This includes **discoverability / ResearchBodies detection mechanics** — keep them out.
5. Natural Korean — no calques, no back-referencing "그 조석" constructions.
   Keep it short and close to the original; do NOT over-expand ("풀어쓸 필요 없는 건 안 풀어씀").
6. No em-dashes in rendered prose.
7. `refs:` must carry the real methodology grounding (see "Refs" below).

English prose must ALSO be natural (not a literal mirror of the Korean), and equally short.

## Hard workflow rules (the user is strict about these)

- **One row at a time.** Rewrite one axis, show **before → after** (Korean version alone
  is enough), then WAIT for the user's OK before touching the next row.
- **Never commit before showing the diffs.** (This was violated once on Pandora; the user
  was upset. Do not repeat.)
- Editing the YAML: use targeted `Edit` (exact-match on the folded scalar), never a full
  Write. Watch for accidental blank lines inside `>` folded scalars.
- Autonomy applies to mechanics (running the build, gate, computing numbers), NOT to prose
  decisions — those get confirmed row by row.

## Content decisions already locked in

- **Body names (user chose option "a"):** fictional NearStars bodies stay **Latin**
  (Pandora, Polyphemus, Dante, Hades). Real solar-system bodies go **Korean**
  (이오 = Io, 가니메데 = Ganymede).
- **No direct movie references in narrative** (Na'vi, floating Hallelujah mountains, cities,
  unobtanium). Movie-canon *reconciliation* may live in `gate.evidence`, not the narrative.
  Exception the user allowed: Polyphemus environment may name the moons "as the film's moons",
  but unobtanium stays fully out of the environment row.
- **Floating mountains retired everywhere** → replaced with "geometric natural rock
  formations / 기하학적 자연 지형". Unified across bodies.
- **Radiation numbers = OUR computed values, not canon floor.** Polyphemus inner belt
  = 300 rad/h; ×24 ≈ 7,200 rem/day, which exceeds the canon floor (>4,500). We cite our value
  and leave the canon note in evidence. (rad ≈ rem for this belt model.)
- **Metallicity [Fe/H]:** skip (low-impact, per standing convention).

## Refs / methodology grounding (contract criterion 7)

Derived rows must carry `refs:` pointing at a real methodology doc. Valid docs are listed in
`docs/reference/methodology-index.md`. Methodology docs are **English-only** — do NOT build
Korean mirrors of them (that infra was abandoned; the user said "아 그럼 냅둬").
The board renderer maps `docs/reference/*.md` → wiki reference page, `phase3/*.md` → GitHub blob.
Earlier audit filled 11 ref gaps across Pandora/Polyphemus/Dante; warnings dropped 45 → 34.
Remaining "no refs[]" gate warnings are acceptable (not errors).

## Hades — DONE (all 9 rows committed)

Resolved the parked `bulk.tidal_heating` question: the user chose the **nominal-vs-realized**
framing. The narrative now says the heat reaches ~400× Io when scaled from Io, but because the
moon is small and rigid most of it pushes the crust around instead of melting the surface. The
full reconciliation (low k2/Q, film gray > game >900K > wiki) stays in `gate.evidence`.

Other Hades outcomes worth carrying forward:
- `environment.radiation` now quotes a number instead of the bare grade "심함". Hades sits at
  the inner belt's peak L (2.07 R_p), and the belt model's inner intensity is 300 rad/h, so
  300 × 24 ≈ **7,200 rem/day** — the same grade as Dante further in. Field value + note + the
  two belt methodology refs added to match Dante's row.
- Ref parity check against the equivalent Dante rows caught two gaps: Hades `bulk`
  (body-figure + tidal-locking-timescale) and `bulk.tidal_heating` (tidal-heating). Filled.
  Gate warnings for alpha_centauri: 34 → 31. The remaining 4 Hades warnings (identity, surface,
  appearance, gameplay) mirror Dante exactly, so they are the accepted baseline.
- Biome lists belong in `fields`, never in the gameplay narrative (Dante set this precedent);
  the "Poles is geographic, not seasonal" rationale goes to `gate.evidence`.
- The user tends to hand back an edited version of the draft. Apply their wording verbatim,
  with one exception: they wrote "단테" in Hangul, but the locked naming rule keeps fictional
  NearStars bodies Latin, so it stays "Dante".

## Validation + build + commit (run at each body's closeout)

```
python3 scripts/check_phase4_gate.py                       # expect 0 errors; refs warnings OK
python3 scripts/phase4/build_phase4_html.py alpha_centauri # rebuilds docs/phase4/alpha-centauri/*.html
```
Commit only after the user confirms all of a body's rows. Commit message in English;
identity `VaNnadin <vannadin00@gmail.com>` (local git config already set).

## Where things are

- Editing target: `phase4/alpha_centauri.yaml` (the ONLY file being changed).
- Built HTML: `docs/phase4/alpha-centauri/{pandora,dante,alpha-centauri-a-b,hades,cassandra,chaos,...}.html`.
- Flattening/oblateness viewer (opened earlier for the user): `phase4/figure/distortion-viewer.html`.
- Full prior transcript (pre-compaction detail):
  `/Users/vana/.claude/projects/-Users-vana-Desktop-NearStars/4f7c6dfb-cfd5-47fe-b3f5-a4281368edcd.jsonl`

---

## Decision provenance moved off the board (2026-07-27)

`gate.evidence` **is rendered in the board viewer** — it has been since the viewer's first
commit (`b0a3a17`, 2026-07-10), as an `evidence`-tagged block, alongside the `verdict`
badge (`owner-override` renders as "오너 확정"). It is not an internal channel.

SPEC §3.1 bans dated decision-logs from `evidence` too, not just from `narrative`:
"Technical shorthand is fine; storytelling and dated decision-logs are not", with the
provenance directed to "the session checklist/context-notes, not on the board a stranger
reads". The regrounding work below had put that provenance into `evidence`; it was stripped
out and lives here instead. Only YAML comments (`#`) remain as an on-file internal channel —
the parser drops them, so the viewer never sees them.

### Where the record lives now

Per-row value history moved onto the board itself as a **`provenance:`** key (SPEC §3.1,
added 2026-07-27) — old value, when and why it changed, which owner call settled it, sitting
next to the value rather than in this pass-scoped file. Ten rows carry it: Dante
`bulk.tidal_heating` + `surface`; Hades `bulk.tidal_heating` + `surface` + `appearance` +
`gameplay`; Pandora `atmosphere`; Cassandra `atmosphere` + `magnetism.magnetic_field` +
`environment.radiation`.

A real key rather than a YAML comment, because nothing rewrites these boards today but the
schema has already migrated once (v1 → v2) and any future parse-and-redump would drop every
comment silently. Verified: the gate passes with the new key and the rendered HTML contains
none of it.

This file keeps what is genuinely per-session — the arc below, and the open items.

### The session arc (2026-07-26/27)

Started as a prose pass and turned into a physics audit. Grounding the greenhouse increment
(`greenhouse-warming-methodology`, new) showed Cassandra's and Pandora's temperatures rested
on an unsourced "+45–50 K / +70 K CIA greenhouse". Grounding the satellite energy budget
(`moon-energy-budget-methodology`, new) then showed every moon temperature had been computed
as if the moon were a planet — no eclipses, no parent illumination, no tidal term — and that
Dante's and Hades's recorded surface temperatures violated energy conservation against their
own tidal fluxes by 300–400 K. Investigating "the ocean's tidal budget" behind Pandora's 32 h
lock produced the stability scan that killed the lower-eccentricity option for Hades, and a
correction: the obliquity ocean-tide channel is starved because the spin axis is orbit-normal,
so the live channel is the eccentricity tide and it is a depth choice rather than a risk.
Separately, the owner's "everything lands on Earth's values" complaint produced the analog-row
rule in `exoplanet-atmosphere-methodology` §6 and a new Gate 4 there (species-selective
retention, Jeans parameter), after they asked whether gravity, stellar wind and temperature
were all covered — the first two were, temperature was not.

### Chaos — the albedo / ring-feed detour (2026-07-27)

Two wrong turns of mine, recorded so nobody re-walks them. Both came out of one real
finding: exposed water ice cannot survive on Chaos. It sits at 1.30 AU-equivalent
insolation, where the board's albedo 0.70 strips 400 km of ice in 4.5 Myr against a
5.3 Gyr age, and the survival threshold (0.875) is outside the albedo methodology's own
fresh-water-ice band (0.6–0.8) and above Enceladus (0.81). The owner chose to keep the
bright ice as art and raise the albedo, landing on 0.91.

1. I then claimed sublimation had become the ring's mass budget, since a 134 K surface
   sheds ~134 kg/s. Wrong: sublimation sheds **vapour** and the ring is solid grains —
   its own colour grounding is grain scattering. Free-molecular gas drag against 0.023 g
   caps the liftable grain at 2e-10 m, smaller than a water molecule, so sublimation
   cannot supply dust at all. (Comets manage it because their flux is ~6 orders larger
   off km-scale nuclei with no gravity.)
2. I then moved the supply to impact ejecta. Also wrong-headed — the owner pointed out
   this body was designed as an Enceladus analogue from the start, and Saturn's E-ring is
   plume-fed. **The original plume-first value was correct all along.**

What the detour did earn: Chaos's 424 m/s escape velocity is higher than every real
dust-ring source body (Thebe 34, Amalthea 58, Phoebe 102 m/s are impact-fed; even
Enceladus at 239 m/s needed plumes). So *no* ejection mechanism we can ground supplies
this ring at its gated brightness. Moving the supply to the 9 unnamed canon moonlets
(escape velocities ~1 m/s, exactly how Jupiter's gossamer rings work) was offered and
declined: the owner kept the plumes and asked that they be marked as art direction, so
the satellites verdict rose to `owner-override`. The sublimation number survives as
`neutral_torus_supply` — a Europa-like neutral water torus beside the ring, not feeding it.

Side fact worth keeping: at the old albedo 0.70 the sublimation flux *could* lift 9 µm
grains. Choosing bright ice closed that channel, but since the supply is the plumes
anyway, the ring is unaffected.

### YAML length discipline (2026-07-27)

The owner asked whether the board was getting bloated. Measured: 3,181 lines / 222 KB at
that point, +12% in one session for 1.2 bodies, i.e. ~36 lines per decision. `gate` is
39% of the file (`evidence` + `evidence_ko`); `provenance` is only 2.7%, so provenance was
never the problem. Three rules adopted, and the Chaos rows above were trimmed to them:

1. **One fact, one row.** A fact is stated in full in the row that *owns* the decision;
   other rows point at it by row name (`Chaos.satellites`), as the board already did with
   `Chaos.surface divergence_note`. The 424 m/s assessment was duplicated across
   satellites, rings and surface; it now lives in satellites only.
2. **`provenance` ≤ 4 lines** — old value → new value, why, whose call. Detours and
   session narrative come here instead. (My Chaos provenance blocks had grown to 10 and
   14 lines, 2–5× the median, by narrating my own wrong turns.)
3. **`evidence` states the conclusion and the check performed**, and delegates the
   derivation to the tool or methodology doc rather than reproducing the arithmetic.

Not waste, and deliberately kept: `evidence_ko` is half of `gate`, which is the cost of
the bilingual viewer. Changing that is a viewer-policy question, not a cleanup.

### Open items

- **Cassandra's magnetic field strength is not derived.** "Weak" is not a number, and a
  standoff calculation against the outer belt's plasma pressure needs one. Pandora's 75 µT
  came through `rocky-planet-dynamo-methodology`; do the same for a 0.151 M⊕ core.
- **Ocean tidal dissipation for Pandora is unquantified.** Bounded, not computed — the
  eccentricity tide is resonant in ocean depth, so fixing the ocean depth is the trigger.
  Method: Matsuyama 2018.
- **Cassandra `gameplay` is the last row of the prose pass** and has not been touched.
- The Earth-default sweep across other systems was **deliberately dropped**: only
  alpha_centauri has had a real Phase 4 run, so findings on the other boards are noise.
