# Phase 4 prose-readability pass — context notes (session handoff)

Last updated: 2026-07-25. Read this + `checklist.md` first, then resume Hades.

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
