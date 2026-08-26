---
name: nearstars-methodology
description: >
  Ground a NearStars derived value's methodology in the literature — build or
  upgrade an ADS-verified methodology reference doc
  (`docs/reference/<topic>-methodology.md`), or author/run a self-contained
  R-series research prompt that grounds specific numerical parameters for
  another session. Trigger this skill whenever a derived (not directly
  measured) physical quantity needs paper grounding — phrases like "방법론
  문서 만들어줘", "이 도출값 근거화", "방법론 그라운딩", "논문으로 근거
  찾아줘", "이 파라미터 문헌으로 정당화해줘", "ground this derived value",
  "write a methodology doc for X", "리서치 프롬프트 작성", "research prompt
  for X" — or any time Phase 3/4 (or Principia-branch) work surfaces a derived
  value whose recipe is missing from `docs/reference/methodology-index.md`.
  Back-of-envelope is banned for non-trivial astrophysical derivations, so a
  missing recipe is itself the trigger. Do NOT use for Phase 3 synthesis
  itself (nearstars-phase3), Phase 4 gating (nearstars-phase4), or star/
  measurement curation (nearstars-add-star) — this skill builds the recipes
  those consume.
---

# NearStars — Methodology Grounding

NearStars assigns many values that are **derived, not measured**: colors,
magnetic fields, internal heat, J₂, gravity-truncation floors. The project
rule (curation-contract SPEC; see also the derived-value-grounding feedback
memory) is that every such derivation must be **paper-grounded**: the method
comes from citable literature, with the citations verified against NASA ADS.
Textbook relations (Darwin–Radau, the Planck function, Kepler's third law)
are the one allowed exception.

This skill captures the procedure that built the 13-doc methodology program
(2026-06-25) and the Principia-branch R-series reports. Canonical index of
finished recipes: [`docs/reference/methodology-index.md`](../../../docs/reference/methodology-index.md).
Gold-standard template: [`docs/reference/planetary-dynamo-scaling.md`](../../../docs/reference/planetary-dynamo-scaling.md).

## Two output modes — pick one first

**Mode A — Methodology reference doc** (the default). A durable, reusable
recipe: relation + regimes + worked examples + annotated bibliography, saved
as `docs/reference/<topic>-methodology.md` + ko mirror, registered in the
index. Use when the derived value will recur across bodies (color, B-field,
tidal heating…).

**Mode B — R-series research prompt + report.** A one-shot grounding of
specific parameters, where the *consumer is another session* that will set
the values from the report alone. Two artifacts: a self-contained prompt file
(`...-PROMPT.md`) and the resulting report. Use when grounding engine/design
parameters (e.g. the gravity significance floor) rather than a reusable
per-body recipe. A Mode B report often graduates into a Mode A doc afterwards
(R6 → `gravity-significance-floor-methodology.md`).

**The owner's named deliverable overrides these heuristics.** If the owner
asked for a methodology *doc* ("방법론 문서", "근거 문서로 남겨줘", "document
the method"), the job is Mode A — even when the work shape looks like
one-shot parameter grounding. Run Mode B research first if the evidence
doesn't exist yet, but the task is not done until the Mode A doc exists;
"graduation can wait for reuse" applies only when the owner never asked for
the doc. Conversely, an explicit ask for a research prompt/report is Mode B.
**State the chosen mode and the reason to the owner before starting** —
silent mode substitution is how an owner asks for documentation and receives
research reports instead (2026-07-11 warpfx incident). If the instruction is
ambiguous, one clarifying line beats a wrong mode.

## Before writing anything — read the exemplars (mandatory)

The sections below describe *structure*; the exemplars carry the tone and
citation craft. A session that authors from the descriptions alone produces
structurally-correct but shallow output (observed in the first cross-repo run,
2026-07-11).

**Read them for citation craft and register, not for length.** "Density" here
means every line earning its place, and it has repeatedly been read as "write
more", which is how one doc reached 4.5x the reference. The Mode A section
below lists what not to write; that list wins over anything an exemplar
happens to contain.
Read the chosen mode's exemplars once, in full, in the authoring thread —
fan-out research agents do not need them (they receive the authored prompt
itself). Absolute paths so they resolve from any repo:

- **Both modes**: the discipline note at the top of
  `/Users/vana/Desktop/NearStars/docs/reference/methodology-index.md`.
- **Mode A**:
  `/Users/vana/Desktop/NearStars/docs/reference/planetary-dynamo-scaling.md`
  — the gold standard, end to end.
- **Mode B**:
  `/Users/vana/Desktop/NearStars/plans/principia-interstellar-branch/research/R6-significance-floor-PROMPT.md`
  (prompt craft) and
  `/Users/vana/Desktop/NearStars/docs/reference/gravity-significance-floor-methodology.md`
  (what a consumable grounded result looks like — angle-by-angle evidence
  with pinned citations feeding an explicit synthesis).

Cost: ~3–5k tokens, once per session. Cheap insurance against feeding a
million-token research fan-out a shallow prompt.

Mode B splits into two roles that may be different sessions: **authoring**
the prompt (this skill's main job — the deliverable can be the prompt alone)
and **executing** it (running the research; also covered by this skill when
asked). Both artifacts live under the consuming track's research directory —
`plans/<track>/research/` (the R1–R7 files sit under
`plans/principia-interstellar-branch/research/` because Principia is their
consumer, not because that path is canonical). No track directory yet? Put
them next to the plan that will consume the report.

Two execution rules:

- **Run the prompt in the executing session's main loop** — paste it as the
  session prompt. Do not hand the whole prompt to one agent: the prompt's
  embedded delegation instructions will make that agent spawn nested
  sub-agents, and the main-thread deterministic verification (plus cost and
  model-override visibility) disappears inside it. The fan-out stays one
  level deep, orchestrated by the session itself.
- **Executing from another repo?** The ADS token is a global shell export,
  so authenticated queries work anywhere — but repo assets are not global.
  Reference the paper cache by absolute path
  (`/Users/vana/Desktop/NearStars/docs/phase3/_papers/`) and write new
  fetches back there (the cache has one home), and make any sanity-check
  data paths absolute too, so agents don't silently skip a step over a
  dangling relative path.

## The ADS discipline (non-negotiable, both modes)

- **All paper discovery and verification goes through NASA ADS** with the
  registered `ADS_API_TOKEN` — never WebSearch, and never cite numbers from
  WebFetch summaries. Direct queries:

  ```bash
  curl -s -H "Authorization: Bearer $ADS_API_TOKEN" \
    "https://api.adsabs.harvard.edu/v1/search/query?q=<query>&fl=bibcode,title,first_author,year,citation_count,identifier&sort=citation_count+desc&rows=25"
  ```

  For a broad per-planet sweep, `scripts/phase3/build_bibliography.py` exists
  (ADS + arXiv → `docs/phase3/_bib/<slug>.yaml`); for targeted methodology
  grounding, direct `search/query` calls per research angle usually suffice.

- **Literature discovery is delegated, not dictated.** Spawn research agents
  that find papers *independently*, sorted by `citation_count desc` — do not
  hand them a pre-made paper list. (2026-06-23 lesson: dictating the list
  from memory produced wrong arXiv ids and missed papers. Naming a few
  *candidate anchors* per angle, as the R-prompts do, is fine — agents must
  still verify them against ADS and are free to replace them.)

- **Read the source, not the summary.** Load-bearing numbers come from
  abstracts and full text (arXiv/ar5iv), read directly. The full-text cache
  is `docs/phase3/_papers/<arxiv_id>.md` — check it before re-fetching, and
  add to it rather than re-searching the web.

- **Pin every claim**: arXiv id where one exists, else the ADS bibcode.
  Note explicitly when a paper has no preprint (e.g. Nature letters) and is
  therefore verified by bibcode only. **Every citation in doc prose is a
  clickable markdown link** (CONVENTIONS.md §3.3) — bibcode →
  `[2018Icar..305..262M](https://ui.adsabs.harvard.edu/abs/2018Icar..305..262M)`,
  arXiv → `[1007.1514](https://arxiv.org/abs/1007.1514)` (`&` → `%26` in the URL).
  Bare ids stay only in machine fields / code blocks.

- **Source outside ADS's scope?** The discipline's point is verifiability
  and anti-fabrication, not the index itself. Fall back in order:
  (1) check ADS anyway — it indexes physics broadly, all of arXiv, and many
  technical reports (JPL IPN Progress Reports have bibcodes); (2) an
  authoritative curated database is a canonical source in its own right
  (precedents: NIST ASD for plasma lines, the USGS spectral library for
  mineral colors, Pearse & Gaydon in book form) — pin by database version /
  report number; (3) otherwise pin by DOI and read the publisher's full
  text — "no numbers from summaries" applies unchanged; (4) whatever the
  route, mark the citation as a non-ADS exception stating how it was
  verified, so a later audit knows. In a Mode B prompt, declare such
  research angles "non-ADS acceptable" up front and keep them brief
  (the R6 angle-E pattern).

- **If the literature is silent, say so.** An explicit "no precedent found —
  we keep convention X, justified by our internal tests" is a valid, honest
  result. Never backfill a citation to make a chosen value look grounded
  (see the delta Pav disk fabrication incident).

## Mode A — writing the methodology doc

A methodology doc is a **manual for a recipe**, not an account of how the
recipe came to be. It is read by someone who wants to call the thing, and by
the machine that checks the contract against the code. Neither needs the story.

Structure (first line: one-line Korean HTML comment stating the doc's role;
then a title, `<quantity> grounding — <method name>`):

1. **Contract** — `## Contract — <node>` with `Returns`, `Needs`,
   `Discriminating keys`, `Grade`. `engine/check_contracts.py` parses this
   block and diffs it against what the recipe actually consumes and produces,
   so it is machine-checked, not decorative.
2. **The relation** — the governing equations with their source. State them;
   do not narrate deriving them.
3. **Constants / equations of state** — one table. Every row carries its
   source, table number, and validity limit. Values only; a constant that
   needs a paragraph belongs in Sources as one annotated line.
4. **The mechanisms this recipe models** — one short section each, only where
   the physics genuinely branches (e.g. porosity, compaction, phase ladders).
   Skip entirely if the relation in §2 is the whole method.
5. **Domain of validity** — the regime table with numeric conditions, and what
   the recipe returns in each. **Anchor results live here as a table**, because
   "how well does it work and where" is one question, not two. The table only —
   the surrounding prose is what made the last doc 4.5x the reference one.
6. **Sources** — annotated: full reference, bibcode, arXiv id, whether it is
   in the `_papers/` cache, and one sentence on the role it plays. **A choice
   between sources is one line here**, not a section elsewhere.

**Do not write these.** Every one of them has appeared, been asked to go, and
come back:

- a revision history, or a "what changed on <date> and why" section — that is
  what git log is
- worked examples walked through by hand — the tests generate them and
  `check.sh` runs them; a doc table that is not generated will drift
- the reasoning behind a choice, retold — the one-line annotation in Sources is
  the whole budget for it
- "what the roster asks for", or any section framed around our bodies rather
  than the method — a manual describes the tool, not today's inputs
- restating in prose what the tables above already say

The reference for length is `planetary-dynamo-scaling.md` at ~190 lines. A doc
past ~300 has almost certainly grown one of the sections above; check before
adding another.

Registration checklist (a Mode A doc is not done until all five):
- [ ] Row added to the right section of `docs/reference/methodology-index.md`.
- [ ] **The same row in `ko/docs/reference/methodology-index.md`** — the index has
      its own mirror, and adding only the English row is the failure that let the
      Korean index drift three recipes behind (2026-08-11).
- [ ] Korean mirror at `ko/docs/reference/<same-name>.md` — natural Korean,
      not literal translation; keep block structure.
- [ ] Cross-links: `## Related` in the new doc and in its nearest siblings.
- [ ] `python3 scripts/build_docs.py` — publishes the doc to the Pages surface
      (`docs/wiki/reference__<slug>.html`). Editing the markdown without this leaves
      the published page serving the old text; `check.sh` section 7 now fails on it.
- [ ] `./scripts/check.sh` green — gate 12 (`check_methodology_coverage.py`)
      enforces both index registrations above.

There used to be a third registration surface, the GitHub-repo wiki's
`Methodology-Library` portal. Publishing consolidated onto Pages on 2026-08-13
(`plans/wiki-consolidation/`), so that portal is retired: the wiki keeps a stub
pointing at the published index, and nothing needs to be pushed to the wiki repo
for a new recipe.

## Mode B — the R-series research prompt

The prompt file must be **self-contained**: the executing session gets no
other context, and the consuming session will act *from the report alone*.
Structure (model: the R6 prompt from the exemplars section above):

1. **Task** — what report file to produce, and the standard: "include the
   evidence (numbers, bibcodes, short verbatim quotes), not just conclusions."
2. **Context (do not re-derive)** — the design as built, the provisional
   values, and *why* they are provisional. Also the use-profile to weigh
   against (timescales, what the player/consumer can actually measure).
3. **Research angles** — 3–5 lettered angles, each with candidate anchor
   papers (to be ADS-verified, not trusted) and an explicit per-angle
   **deliverable** ("a table of acceleration ↔ instrument/timespan").
4. **The synthesis question** — the decision the evidence must support,
   stated as alternatives (criterion type A vs B vs C), plus required
   sanity checks against project data (`db/...`).
5. **Method requirements** — the ADS discipline above, expected paper scale
   (~15–25), primary-source preference, any allowed non-ADS exceptions
   (operational docs) marked as such.

Because the executing session gets no other context, the prompt must carry
its own copies of the operating rules: restate the ADS discipline in Method
requirements, and put the delegation instructions (one agent per angle,
`model: "opus"`, non-fork, pinned-findings return format) in the prompt
itself — the Delegation section below is written to the operator, but for
Mode B its content travels inside the authored prompt.

## Delegation & token discipline

- Fan out **one agent per research angle**, `model: "opus"` (never fork —
  forks ignore the model override). Each returns pinned findings:
  `(bibcode/arXiv id, the number, the quote or cache line)`.
- The main thread verifies **deterministically** — grep the `_papers/` cache,
  recompute the formula, re-run the validation step. Adversarial verify
  agents are per-report, not per-finding; never trust an agent's self-report.
- Estimate fan-out cost before launching; the constraint is the daily token
  quota, not session context.

## Related

- `nearstars-phase3` — consumes Mode A recipes to derive cfg-ready values.
- `nearstars-phase4` — gates owner art-direction against the recipes' windows.
- `docs/reference/methodology-index.md` — the living index; keep it current.
