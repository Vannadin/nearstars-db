<!-- 다음 세션에서 돌릴 Phase 4 아웃풋 일관성 감사의 착수 브리프 -->
# Phase 4 output consistency audit — brief

Written 2026-07-28, at the owner's request, for the **next** session to execute.

## Why this exists

The 2026-07-26/28 work was a prose-readability pass that turned into a physics
audit and then a mod-layer removal. It moved in small hops across bodies, axes,
validators and docs. Every individual change was checked, but nothing checked the
**result as a whole**. The owner's concern is exactly that: consistency.

So the audit's question is not "is each row defensible" (the gate answers that).
It is **"do the 82 + 135 rows read as one document written by one hand?"**

## Ground rules for the auditor

- **Read-only first.** Produce findings, then let the owner choose what to fix.
  Do not start rewriting rows while auditing; the last session's damage came from
  editing and checking in the same motion.
- **Never run unanchored regex over the boards.** Four separate corruptions came
  from that in one session (details in commit `4b8d73b`). Edit row-scoped, and
  after any edit run all three: YAML parses, no bibcode token altered
  (`new ⊆ old`), structural key counts match (`gate:`/`criterion:`/`fields:`…).
- Scope is the **output**, not the contract. SPEC/skill changes only if the audit
  finds the contract itself contradicts what six boards actually do.

## What the boards should look like now (the rules to audit against)

Canonical: `phase4/SPEC.md` §3.1, the `nearstars-phase4` skill Step 4, and
`phase4/prose-readability/context-notes.md`. Established or changed this session:

1. `narrative` = reader-facing story, conclusion first, ≤6 sentences.
2. No dates / owner-decision history in narrative. **Verified zero board-wide.**
3. No bibcodes / paths / equations / parameter dumps in narrative.
4. No **workflow vocabulary** in narrative — passthrough·통과, emit, 앵커,
   Phase 3/4, 보드, 게이트, 전용 행, union rule, field names. **Verified zero.**
   *(new this session; not yet written into SPEC — see open items)*
5. `gameplay` is the biome exception, in three parts: what is distinctive about
   going there (nothing generic to the body class) → biome list with a ≤1-clause
   descriptor each → the single most interesting place.
6. An axis with nothing to say gets `없음.` / `None.`, not a padded sentence.
7. One fact, one row: stated in full in the row that owns it, referenced by name
   elsewhere (`Chaos.satellites`).
8. `provenance` ≤ 4 lines per dated entry; detours go to context-notes.
9. `evidence` = conclusion + the check performed; derivation delegated to the
   tool or methodology doc.
10. No em-dashes in rendered prose. Natural Korean, no calques.
11. Arbitrary-looking values are labelled as such (`임의 값`), not dressed up as
    decisions.

## Where inconsistency is most likely — start here

**A. Only alpha_centauri got the full pass.** Its 82 rows follow rules 1–11. The
other five boards (proxima_cen 53, 40_eridani 54, barnards_star 11, fomalhaut 10,
tau_cet 7) got *only* the discoverability removal. Expect them to still be
parameter dumps with workflow vocabulary, em-dashes and owner references. Quantify
the gap per board before proposing work — the owner may want them left alone.

**B. Em-dashes outside the stars.** 26 remained in rendered prose at the time of
writing (evidence 17, evidence_ko 8, narrative 1) on non-star bodies of
alpha_centauri. Rule 10 covers them; they were out of the session's scope.

**C. Register drift inside alpha_centauri.** Rows were written at different times
in different voices. Known tension: A/B `bulk`, A `bulk.spin_axis_orientation`,
B `bulk.geopotential_j2` are deliberately terse value-lists (owner's call, since
they carry no decision), while `activity`/`appearance`/`stellar_wind` on the same
pages are full prose. Confirm that reads as intentional rather than unfinished.

**D. `없음.` consistency.** Chaos magnetism and satellites use it. Check whether
other empty axes across all six boards still pad a sentence instead.

**E. The `fictional: true` flag.** Eight bodies carry it (Dante, Hades, Pandora,
Cassandra, Chaos, 40 Eri A c, 40 Eri A d, Proxima Cen c I). Verify: exactly the
bodies absent from `db/`, no more and no fewer, and that
`check_pipeline_flow.py` exempts precisely those.

**F. Cross-row claims that may have drifted apart.** This session found three
live contradictions of exactly this kind, so look for more:
- the Polyphemus `radiation_belts` row put Cassandra inside the outer belt while
  Cassandra's own row said it was outside (fixed);
- Chaos's magnetism and radiation rows recorded Chaos's own orbital radius,
  21 R_p, as the magnetopause, which is at 23.5 R_p (fixed);
- Chaos surface temperature and albedo violated the ice-stability calculation
  (fixed). Check the remaining moon↔parent and body↔body couplings the same way:
  belt geometry vs per-moon dose, eclipse/temperature chains, ring plane vs the
  supplying moon's orbit.

**G. refs parity.** Sibling rows on comparable bodies should cite comparable
methodology docs. Chaos `bulk` was missing both refs its Hades counterpart had
until this session. Sweep for the same asymmetry elsewhere.

**H. Art-override honesty.** `owner-override` rows should state plainly that the
physics does not support the choice, and why it was taken anyway. Chaos plumes
and albedo 0.91 are the worked examples. Check every other override row says as
much, now that the viewer's legend promises the reader it does.

## Open items the audit should also settle

- **Rule 4 is not in SPEC yet.** The workflow-vocabulary ban was applied to the
  boards but never written into `phase4/SPEC.md` §3.1, the skill, or the prose
  memory. Until it is, a later session will reintroduce `emit`/`앵커`/`Phase 3`.
- Cassandra's magnetic-field **strength** is still not derived ("weak" is not a
  number); needs a rocky-planet dynamo run for a 0.151 M⊕ core.
- Pandora's ocean tidal dissipation is bounded but unquantified (trigger: fixing
  the ocean depth; method: Matsuyama 2018).
- Chaos's obliquity 15° is a chosen number, like α Cen A's 7°, but only the star
  is labelled `임의 값`.

## Useful commands

```
python3 scripts/check_phase4_gate.py                     # 0 errors expected
python3 scripts/check_pipeline_flow.py                   # fictional exemption
for s in alpha_centauri proxima_cen 40_eridani barnards_star fomalhaut tau_cet; do
  python3 scripts/phase4/build_phase4_html.py $s; done
./scripts/check.sh
```

Board pages carry a build stamp (`빌드 <time> · <sha>[+미커밋]`) at the bottom, so
a stale browser tab is identifiable.
