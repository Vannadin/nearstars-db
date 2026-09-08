<!-- engine/tools 의 표 생성기 목록 — 각 생성기의 소스가 어디 있고, 무엇을 보관하고 무엇을 명령으로 남기는지의 관례 -->
# Table generators — what they read, and where the source lives

The engine's equations of state that are not analytic fits are **baked tables**: plain-Python literals
committed under `engine/*_table.py`, each headed *"generated file, do not edit by hand"* with the generator
named. The generators here run **once, in the development venv, never at runtime** — `check.sh` runs on
system Python and never calls them. That is the same replaceable-versus-irreplaceable split the paper cache
has, one layer up: the baked table is replaceable from the source; the source may not be.

## Audit — 2026-09-03 (Brief 50), every source checked on disk

| generator | bakes | source | on disk now |
|---|---|---|---|
| `make_water_table.py` | `water_table.py` | SeaFreeze **v1.1.0** `water1` (venv package) | ✓ `engine/.venv` (v1.1.0 verified) |
| `make_water2_table.py` | `water2_table.py` | SeaFreeze **v1.1.0** `water2` (venv package) | ✓ same venv |
| `make_ammonia_table.py` | `ammonia_table.py` | Bethkenhagen+ 2013 Table I, parsed from the cached PDF | ✓ paper cache |
| `make_aqua_table.py` | (generator + cached grid; module not committed, Brief 32) | `docs/phase3/_papers/aqua/eos_pt.dat` (CDS, 62 MB) + `PROVENANCE.txt` | ✓ paper cache |
| `make_ice_melt_table.py` | ice melting constants | `git clone https://github.com/BingqingCheng/highP-ice` (command in header) | ✓ recorded command |
| `make_hhe_table.py` | `hhe_table.py` (129 KB, the ice-giant envelope) | Chabrier DirEOS2019 archive → `docs/phase3/_papers/chabrier_direos2019/DirTABLES-EOS2019/` (the argument) | ✓ **landed 2026-09-03 (Brief 51)**, owner-fetched; regeneration reproduces the committed table **byte for byte** (5,495 cells) |

`hhe_table_tail.py` is a template fragment `make_hhe_table.py` appends; `methane_thresholds.py` is a
measurement tool, not a generator.

**The gap, closed.** `hhe_table.py`'s source, `DirEOS2019.tar.gz` (11,970,972 B, sha256 `736de2a0…149b`),
was nowhere on disk on 2026-09-03 morning; the owner fetched it (and the 2021 archive) the same day and both
are now in the cache with `PROVENANCE.txt`. `engine/.venv/bin/python engine/tools/make_hhe_table.py
docs/phase3/_papers/chabrier_direos2019/DirTABLES-EOS2019` reproduces the committed table byte for byte.
**This is the convention's first real instance on the "keep" side**: an archive from a personal academic
page, kept rather than commanded, because the page has no index behind it and can vanish.
`chabrier_direos2021/` (Chabrier & Debras 2021, Paper II) is **held, unused** — a physics candidate on the
interior board (C6), not a source of anything.

**The inconsistency the audit found.** `aqua/` and `militzer2024_zenodo/` are kept in the cache; the Chabrier
archive was not. Same kind of thing, opposite treatment, and until now nothing said which is right.

## The convention (written 2026-09-03)

- **A generator's source is kept when it is a one-off download; a command is recorded when it is a package
  or a repository.** `aqua/eos_pt.dat` and the Zenodo deposit live in `docs/phase3/_papers/<name>/` with a
  `PROVENANCE.txt`; `make_ice_melt_table.py` records its `git clone` line, which is sufficient because the
  repository is the source of truth.
- **A package's version is pinned where it is named.** SeaFreeze is v1.1.0 in both water generators, both
  baked headers and `eos.py`'s references. The venv is gitignored and exists in this worktree only; to
  rebuild it: `python3 -m venv engine/.venv && engine/.venv/bin/pip install SeaFreeze==1.1.0`. If the pin
  and the installed version ever disagree, the baked tables say which they came from.
- **A one-off archive from a personal academic page is the fragile case and must be kept** — the page can
  change or vanish and there is no index behind it. `DirEOS2019.tar.gz` is the standing example of what
  happens when it is not.
- **A count is only as symmetric as its filter, and the filter belongs in the report.** Two instances from
  one audit (2026-09-03, Brief 51): a grep for `-8.86` returned 0 because the Chabrier tables store the
  placeholder as `-0.886030E+01`; and `b < −5 and a > −5` — a one-directional filter — was reported as
  "three placeholders across the entire table" when the symmetric count is ten (three in 2021 where 2019 has
  values, seven in 2019 where 2021 has values). The grep is one case of the general failure: parse, count with
  the selection written out, and say which direction it looks in. Third instance (Brief 53): a clamp filter
  that tested {0.1, 0.5} against both Chabrier editions and never tested 0.4 — 2021's clamp — put every
  2021 cell clamped at 0.4 into "genuine" (288 / 442 instead of 497 / 233). The first two were about which
  direction a filter looks; this one is about which edition each side is. **A comparison's filter has to know
  what each side means.** Fourth instance (Brief 61): a node regex `^  ([a-z_]+):` — no digits in the
  class — counted 46 nodes where the file has 48, silently dropping `k2q_class_table` and `omega0_class_table`.
  **The general form, stated once so instances need not accrete: a pattern is a hypothesis about the data's
  shape, and reporting its output as a count asserts that hypothesis silently.** Say the pattern beside the
  count, and have a second reader re-measure with a different one — every one of these four was caught by a
  re-measurement, none by the author noticing.
- **Read the generator before measuring its source.** `make_hhe_table.py:32` had carried `SENTINEL =
  -8.8603` with the comment *"우리 창 안에 7칸 있다"* — the value, the convention and the exact count — the
  whole time; two seats re-derived it from the tables, one of them wrongly, before either looked there.
  Third instance the same day (Brief 53): line 113 of the same generator names the grad_ad clamps
  (*"0.1/0.5 로 눌린 grad_ad"*), and the C6 entry's "max 0.40" between the two Chabrier editions was
  exactly those clamps (0.5 vs 0.4 conventions) re-discovered as a physical change. The first two were
  about log ρ; this one shows the same file also answered a grad_ad question.
- **Every kept source directory carries a `PROVENANCE.txt`** (who obtained it, when, from where, what is in
  it). `militzer2024_zenodo/` lacked one until 2026-09-03; added.

## Backlog — 2026-09-05 (C33)

- ~~**Tighten the contract-heading anchors to a unique Need item, where one exists.**~~ **Done
  2026-09-05, and the measurement is the result: of 35 contract-heading anchors, exactly **two** could
  tighten. The payload names repeat across the five contract blocks of the heat document —
  `core_radius` five times, `cmb_pressure`, `cmb_temperature` and `nmoi` four each, `mass` not at all —
  which is the same property that let one line number serve 30 edges. The other 33 keep the heading,
  and the reason is this paragraph.
- ~~**Re-grade the engine notes once the migration is done.**~~ **Done 2026-09-05**: a dead landing now
  fails in any `engine/*.md` that does not declare itself a preserved record, same as in wiring and
  code. Counted before tightening: zero new failures, because the exemptions that remain (external
  paper sources, dated quotations, declared records) already covered every one.

- **One helper owns the failure marker, at all 60 call sites.** `check.sh` has 60 `|| fail=1`, and
  after the fix above three of them also echo a `[FAIL]`. The right shape is
  `run_check() { "$@" || { echo "  [FAIL] $1"; fail=1; }; }` wrapping every call, so that **every
  check — including ones added later — reports failure in one format**, and a log-watching loop can
  be complete rather than mostly complete. ⚠ Not done now: it touches 60 lines and belongs in its own
  commit, not bolted onto a documentation round. The three above are the ones that print nothing at
  all today, which is what made the watcher blind rather than merely inconsistent.

Superseded backlog entries, kept for the reasoning:

- **Tighten the contract-heading anchors to a unique Need item, where one exists.** The
  shared-target rule reports them as loosely aimed and it is right: five edges cite
  `## Contract — \`cmb_heat_flux\`` for five different payloads, none of which the heading names.
  Some tighten cleanly (`` `mantle_radiogenic_power` [W] `` occurs exactly once in the heat
  document), some cannot (`core_cmb_temperature_solved` occurs five times, `t_body` none), so the
  pass is "tighten where it is unique, keep the heading and say why where it is not".
- **Re-grade the engine notes once the migration is done.** `check_refs.py` currently warns rather
  than fails on a dead landing in any `engine/*.md`, because a preserved note records what was true
  when it was written. But that directory also holds living documents — `interior-core.md`,
  `SESSION-HANDOFF.md`, `backflow-checklist.md` — which should be held to the wiring's standard. The
  split is by the header declaration `is_preserved()` already reads.

## A rule for citations that ship (2026-09-05, C33)

**A string that reaches a user carries no line number.** `HEAT_PIPE_FLOOR` in `radiogenic.py` is
emitted as `mantle_temperature_floor_total_verdict`, so its citation is read by whoever reads the
verdict. A line number there is guaranteed to rot on the next refactor, and it rotted twice in one
day: the audit found it three sections away from what it described, and the repair that added the
function name still had the line three lines off. It now names the function alone,
`radiogenic.py@«def _total_heat(»`, which a reader can find and which the checker resolves — an
anchor whose only failure mode is the function being renamed, and a rename should invalidate it.

The same holds for any note or reason that leaves the engine. Inside the engine, an anchor with a
phrase is fine anywhere; what must not travel outward is a number that means nothing to the reader
and everything to the next edit.

## What an anchor can still get wrong (2026-09-05, C33)

Anchors end the failure where a document grows under a line number, and they cut the one where a
reused citation inherits whatever now sits there. They do **not** touch the third: a citation that
was aimed at the wrong place to begin with resolves perfectly forever. `c32-o-anchor-risk-notes.ko.md`
is the measurement behind that; read it before extending this scheme.

Two specific hazards, both met tonight:

- **An identifier anchor rots when the identifier goes, and turns ambiguous when a second one
  arrives.** `chain.yaml@«body_age:»` is unique today. Add a second node whose block prints the same
  line and the anchor stops being able to say which — the checker will call it ambiguous, which is
  the right verdict, but it is a failure mode the "it only rots if removed" reading misses.
- **Note prose is the worst anchor target in this repo.** chain.yaml took 1 688 additions and 712
  deletions across 62 commits in a month, against 395/4 for the tidal document: its notes are the
  most-rewritten text we have, and four citations were anchored to them. They now point at the node
  key or the `from: … , to: …` pair of the edge whose note it was, which changes only when the graph
  changes.

## Two things the next migration will hit

- **A span may need the line *before*, not after.** The folding that lets an anchor cross a hard wrap
  is direction-agnostic, but the migrator only ever tried the following line, so it stalled on a
  target whose next line was blank — a `refs:` row that occurs twice in `phase4/luhman_16.yaml`. The
  line above it made the phrase unique. Try both directions.
- **You cannot use the citation syntax as an example in prose.** Write `<file>:<line>` or the anchor
  form inside a sentence and the checker reads it as a citation, because it is one. It happened twice
  in one day, in the C33 entry and again in this handoff. Describe the forms in words instead ("a
  citation written as a line number, and the same one written as a phrase anchor"), or put a backtick
  inside the token to break it. This is why the documentation of the scheme carries no literal
  examples of the scheme.
  **Three times in one day** (2026-09-05): the C33 entry in `interior-core.md`, the session handoff,
  and the corrections written for the paper-claim checker, whose own sentences contained the words
  that checker looks for. Three is not coincidence, it is the property: **a checker that reads prose
  will read the prose written about it.** Expect it, and write around it rather than exempting the
  file — an exemption is a hole, and the wording is cheap.

## Telling a busy gate from a dead one (2026-09-05)

`scripts/check.sh` is judged by one line, `GATE END sha= pid= at= rc=`. That rule was written to stop
a run full of PASS lines being read as a pass before it finished. It has a missing half, and the
missing half cost two healthy gates on 2026-09-05: **the absence of an END line is not evidence of
death.**

Three signals look like a stall and are all normal:

- **A flat log for a minute or more.** `test_interior.py` runs the shooting solver over the roster and
  holds the log while it works.
- **The parent at 0.0 % CPU.** It is a `bash` waiting on a child. It is supposed to be idle.
- **`pgrep -x python3` returning 0.** This one is not a signal at all. The interpreter that runs the
  checks reports its `comm` as **`Python`** (the CommandLineTools framework binary), so that pattern
  matches on no run, healthy or dead. It returns 0 the way a broken thermometer returns zero degrees.

Find the worker by **process group**, never by guessing its name — and not by one level of parentage
either, because `check.sh` runs its checks in a subshell, so the gate's immediate child is another
idle `bash` and a one-level lookup reports 0.0 % just as misleadingly:

    P=$(pgrep -f "scripts/check.sh" | head -1)              # the gate's own parent
    G=$(ps -o pgid= -p "$P" | tr -d ' ')                    # everything it spawned shares this group
    ps -A -o pgid=,pid=,%cpu=,etime=,comm= | awk -v g="$G" '$1==g'

A live gate shows three rows: the parent `bash` at 0.0 %, a subshell `bash` at 0.0 %, and one worker
near 100 %. **That worker is the only signal that separates busy from dead.** If the group holds
nothing but idle shells and the log has not grown, then discard the run — and even then, the run has
produced no verdict either way.

**A diagnostic gets run before it gets written down.** The paragraph above was first written as
"find the child by parentage" — and running it on a live gate returned that idle subshell, 0.0 %, the
same lie the process-name guess told. It was caught only because it was executed before it was
committed. This is the documentation half of the rule the engine already keeps for code: *a commit
that closes a hole brings the test that reproduces it.* A written-down diagnostic that has never been
run against the healthy case is a guess with formatting.

## An edit script that fails must not be followed by a commit (2026-09-05)

A one-off edit script asserted on a string that no longer matched, stopped, and changed nothing. The
commit ran anyway, in a separate step, carrying a message that described the table the script had not
written. Nothing was wrong with either half: the script failed loudly and the commit succeeded
honestly. **They were two statements and only one of them was checked.**

Chain them, and make an empty diff refuse:

    python3 - <<'PY' || exit 1
    ... the edit, which raises on any string it cannot find ...
    PY
    git diff --quiet -- <the files it should have changed> && {
        echo "the edit changed nothing — refusing to commit"; exit 1; }
    git add <files> && git commit ...

`git diff --quiet -- <path>` exits **0 when there is no change** and 1 when there is, which is the
opposite of what it reads like; the form above was run both ways before being written here. The
commit message is a claim about the tree, and a claim nobody checked is how a document ends up
describing a table it does not contain.

## Four names that read correctly and were wrong when checked (2026-09-05)

One of these is an anecdote. Three in a day is the reason the rule above exists, so they are kept
together — a rule with one example gets read as bad luck.

1. **`pgrep -x python3` as a liveness test.** The interpreter running the checks reports its `comm` as
   `Python`, so the pattern matched on no run at all. Read as "the child is gone", it got two healthy
   gates discarded and put an invented failure mode into the handoff for half an hour.
2. **`pgrep -P "$P"` as the fix for it.** `check.sh` runs each check in a subshell, so the gate's
   immediate child is another idle `bash` at 0.0 %. The corrected diagnostic told the same lie as the
   one it replaced, and was caught only because it was executed against a live gate before being
   committed.
3. **`git diff --quiet` as a commit guard.** It exits **0 when there is no change**. Written the way
   it reads, the guard would have refused exactly the commits that had something to commit — under
   the name of a guard protecting them.

A fourth is not a tool at all. `core_state.py`'s `CORELESS_CLASSES` lists `sub_neptune`, and the
refusal eight lines below says *"서브넵튠의 철핵은 가스 외피 아래 앉아 있지만"* — the constant's name
says there is no core, its own reason says there is one. **Three of the four were tools and one is
data**, which is the point worth keeping: this is not a bug class that lives in shell commands. It
lives wherever a name is allowed to stand in for the thing it names. (That one belongs to C23; it is
recorded here, not touched.)

What the four share is not carelessness. Each was written by someone who knew what they meant, and
each is a **plausible reading of a name**: a process called python is `python3`, a child is one level
down, a quiet diff means nothing happened, a list called coreless holds bodies without cores. The name
was the evidence, and the name was wrong.

So: **run the check against the case you expect to pass, not only the case you expect to fail.** All
three of the tools would have survived a test that only looked for the failure — a dead gate really does report no
`python3`, and an empty diff really is quiet. What none of them survived was being pointed at a
healthy run.

## Re-aiming an anchor is not the whole repair (2026-09-06)

Renaming a constant in `core_state.py` broke an anchor in `interior-core.md`, and `check_refs`
failed it — the citation work doing its own job on the same day it was finished. Before anchors, that
line would have kept a line number and pointed silently at whatever moved into place.

The repair had two halves and only one is mechanical. The anchor was re-aimed at the new constant;
the **sentence around it** still read that the contradiction was "recorded, not repaired", which had
just stopped being true. A checker can find the dead pointer. Nothing can find a live pointer wrapped
in a stale claim.

So: **when you re-aim an anchor, read the sentence it sits in and ask whether it is still true.** It
is the same rule as *a count is only as true as the sentence under it*, one layer down — and the same
failure the whole citation exercise exists to stop, since a citation that resolves while its sentence
lies is worse than one that visibly rots.

## Four times the answer was to reshape the input, not to widen the detector (2026-09-06)

The instinct when a check misses something is to make the check see more. Four decisions this week
went the other way, and together they are the reason to distrust that instinct.

1. **The citation checker's total-count reconciliation was dropped.** Making every citation add up to
   a single total meant maintaining a second accounting of what counts as a citation. Capture is by
   position instead: each match is classified where it sits.
2. **`--contradictions` kept its three-line window.** A wider window finds more, and more of what it
   finds is noise; more dismissing means the check gets ignored, and an ignored check is no check.
3. **An unrecognised citation form is caught by a general rule**, not by teaching the checker each new
   form: anything matched and unclassified is reported as *"a citation form this checker does not
   know; it was counted in no bucket"*. The catch-all is what makes the buckets trustworthy.
4. **A blocking paper is named with its bibcode** rather than teaching the tool author-year matching.
   Widening the denial vocabulary was tried first and measured: it still missed the case it was aimed
   at — C16, whose blocker is written *"Driscoll & Olson 2011"* — while surfacing nine hits, most of
   them adjudication rows that use the words while reporting the opposite. Adding the bibcode to that
   one line made the existing check reach it with no change to the tool.

The rule: **do not widen the detector; write the data in a shape the detector already reads.** A
wider detector costs precision everywhere to gain recall in one place, and precision is what makes
anyone read the output at all.

⚠ **One known imprecision, deliberately left.** `--contradictions` counts a line twice when the
bibcode appears in both a code span and its ADS link. It is harmless while that count is not aiming
at zero — but **if this check is ever tightened to require zero, deduplicate by (file, line, bibcode)
first**, or the target will be unreachable for a reason that has nothing to do with any paper.

## Two tables in one file make "the first match" unusable (2026-09-06)

`interior-core.md` gained a status table at its top on 2026-09-06, above the C14–C19 detail table that
was already there. Both have a row keyed `C19`. A repair script that reached for the first match landed
in the new table and moved three rows out of the old one.

**Once a file holds the same key in two tables, position stops identifying anything.** Select on cell
content that only one of them has — `:614` for the detail row — and never on order. This is not a fact
about this file: a summary table over an existing one is a shape we will add to other documents, and it
breaks first-match selection the moment it lands.

⚠ **And a repair script must not assume the defect it is repairing is absent.** The same script took
"a paragraph runs until a blank line" as its boundary while fixing a paragraph whose *missing blank
line* was the defect — so it swallowed the three table rows that followed. Caught before the commit by
reading `git diff --stat` (5 insertions, 5 deletions, no content lost), reverted, redone with the
paragraph's single-line extent asserted rather than inferred. → One of three, collected under
*"The checker was in the state it was checking for"* below.

**Scope of the sweep that followed.** "No others" was measured **in `interior-core.md`**. Across
`engine/**/*.md` there were three more: two in `composition-gradient-checklist.md`, now fixed, and one
in `c32-k4-basename-notes.ko.md`, **left broken on purpose**. That file's own header declares it
*"원문 무편집"* / *"Preserved verbatim from the parallel seat's scratch"*, and a third line separates
the author's own revisions from edits by the work seat. Inserting a blank line to rescue its rendering
would break the guarantee the file exists to make. A broken table there is the cheaper loss.

## The note that says it is gone, and greps as if it were here (2026-09-06)

`chain.yaml` carries a note reading *"이전엔 body_age → via cooling_luminosity, status: gap 이었다"* —
past tense, recording that a gap edge closed. `grep "status: gap"` matches it, because the phrase is
inside the note. Parsing the YAML gives the true answer: **no edge into `dynamo_giant` carries a
status, and no edge anywhere uses `via: cooling_luminosity`.**

⚠ **And the check that was believed to have avoided this trap had not avoided it.** The evidence used
was `grep "status: gap" chain.yaml | head -12`. Line 660 is match **15 of 28**, so `head` cut at match
12 (line 621) and the note never appeared. **The truncation removed a false positive**, so a method
that could not have shown the answer produced the right one anyway. Untruncated, that grep would have
displayed an apparent counterexample and only the parse could have refuted it.

⚠ **A third slip, inside the check of the check.** Confirming the above, `grep -n … | grep -c ":660:"`
returned 0 and was nearly read as "line 660 does not match". `grep -n` prefixes `660:` — the pattern
was searching for a shape that cannot occur. `^660:` gives the 15-of-28.

The rule, then, in the narrowest form that holds: **when a file's prose can quote its own schema, grep
is a search tool and not an oracle.** Parse the structure. And when a command is truncated for
display, the truncation is part of the evidence — `| head` is not a neutral rendering.

## `pgrep -f "scripts/check.sh"` counts other seats too (2026-09-06)

The habit is: before launching a gate, run `pgrep -f "scripts/check.sh"` and treat **3 or more** as
"another gate is already running", because the pattern matches the parent and its child. On 2026-09-06
it returned 5, and the extra three belonged to **another seat's timing experiment in a different
session's scratchpad** — a `zsh` whose command line happened to contain the string.

`-f` matches the whole command line, so it finds anything mentioning the script, in any worktree, in
any session. The count answers "how many processes mention this path", which is not the question.

What the question actually is: **is another gate running in _this_ tree?** Answer it by group and
working directory:

    for p in $(pgrep -f "scripts/check.sh"); do
      printf "%s %s %s\n" "$p" "$(ps -o pgid= -p $p | tr -d ' ')" \
        "$(lsof -a -p $p -d cwd 2>/dev/null | tail -1 | awk '{print $NF}')"
    done

Rows sharing a pgid are one gate; the `cwd` says whose tree it is. Two gates in two different
worktrees are independent for correctness and only compete for CPU; two in the same tree are the thing
to avoid, since `check.sh` reads the working tree.

Same family as the rest of this file: a matcher was taken for a measurement. The pattern was never
wrong — it answered exactly what it was asked, and the question was the wrong one.

## A phrase count reported as a claim about the concept (2026-09-06)

Reading Goldreich & Peale 1966 on Venus, this seat searched for `"atmospheric tide"` and `"thermal
tide"`, found zero, and wrote that the paper *"never mentions thermal or atmospheric tides anywhere"*.

The count was true. The sentence was not. The stem `atmospher` occurs three times and every one is
about torques on Venus's spin — including the paper calling atmospheric proposals *"quite
reasonable"*. The search asked about two phrases and the sentence answered for a concept.

⚠ **The same scan misleads in the other direction.** `therm` matches four times in that paper and all
four are **"Furthermore"**. A stem search is not a safer default; it is a different set of errors.

Both are today's standing rule seen once more — **a count is only as true as the sentence written over
it** — and on a scanned PDF there is a third hazard on top: OCR that reads cleanly is still OCR. When
a count is about to become an argument, quote the passages it found and the passages a neighbouring
search finds, and let the quotations carry the claim.

## Counts and quotations are both only as true as the sentence over them (2026-09-06)

Two failures on the same paper within half an hour, one in each direction, and they are one item.

**A count, generalised.** This seat searched Goldreich & Peale 1966 for `"atmospheric tide"` and
`"thermal tide"`, found zero, and wrote that the paper *"never mentions thermal or atmospheric tides
anywhere"*. The count was true of the phrases and false of the concept: the stem `atmospher` occurs
three times and every one is about torques on Venus's spin.

**A quotation, truncated.** The reply that caught it quoted the paper as calling atmospheric proposals
*"quite reasonable"* and cited the next sentence as agreement — stopping at the conditional clause.
The sentence continues: *"**However**, if the atmosphere is capable of pushing Venus through the
otherwise stable synchronous state of rotation, **present control of the rotation of Venus by the
earth would be hard to understand.**"* The paper raises the atmospheric explanation and then argues
against it. Verbatim, and the wrong way round.

So: **a quotation cut at a conjunction is not a quotation.** If the excerpt ends before a `However`,
`But`, `Although` or `Yet`, read to the end of the sentence before it becomes an argument. Both
failures are the standing rule — *a count is only as true as the sentence under it* — with quotation
added to counting.

⚠ **And the obvious repair for the first one is not a repair.** Searching by stem rather than phrase
looks safer and is only differently wrong: in the same paper `therm` matches four times and all four
are **"Furthermore"**. On a scanned PDF there is a third layer, since OCR that reads cleanly is still
OCR. When a search is about to become a claim, quote what it found *and* what a neighbouring search
finds, and let the quotations carry the claim.

## A gate is a process group, and every simpler handle fails (2026-09-06)

Three attempts at "is a gate running, and how do I stop it", each defeated by the same fact.

1. **By name.** `pgrep -x python3` matched nothing on any run, healthy or dead — the interpreter's
   `comm` is `Python`. Two healthy gates were discarded on that reading.
2. **By one level of parentage.** `pgrep -P` returns the subshell `check.sh` runs its checks in, idle
   at 0.0 %, so it looks stopped while the worker below is at 100 %.
3. **By pid, to stop one.** `kill <parent pid>` returned without error and the gate kept running for
   another eight minutes, overlapping the replacement gate in the same worktree. `kill -TERM -<pgid>`
   ended it at once.

⚠ And `pgrep -f "scripts/check.sh"` counts the **watch loops** too — a `while ... until grep -q "GATE
END"` shell has that path in its command line and is not a gate.

So the handle is the **process group**, and the question always has two halves — *which group*, and
*whose worktree*:

    for p in $(pgrep -f "scripts/check.sh"); do
      c=$(lsof -a -p $p -d cwd 2>/dev/null | tail -1 | awk '{print $NF}')
      [ "$c" = "$PWD" ] && [ "$(ps -o comm= -p $p)" = "bash" ] &&
        echo "pid $p pgid $(ps -o pgid= -p $p | tr -d ' ')"
    done

Filtering to `comm=bash` drops the watchers; the `pgid` is what to read CPU from and what to signal.

⚠ **The third of those is a worse grade than the first two.** A wrong name and a wrong parent level
both **give a false answer**, and a second measurement catches them. `kill <pid>` **succeeded** —
returned zero, printed nothing — and the gate went on running for eight more minutes. A query that
lies is caught by asking again; a command that fails quietly is caught only by checking the result.

So: **after killing a gate, confirm it is gone before starting the next one.** The six minutes of
overlap on 2026-09-06 cost nothing but CPU, and only because `check.sh` reads the tree without writing
it and has no timed checks. That is luck, not design.

## When output appeared is not when the work happened (2026-09-06)

The gate's per-check timings were read off a timestamped log, and the contract check was reported as
costing 2.4 seconds. It costs **84**. The 2.4 was the span between the contract check *printing its
result* and the gate ending; the 84 seconds of work sat in the silence **before** that print, and the
timestamp of the line was read as the moment the work finished.

Measured directly instead — running the check alone and timing it — gives 76.6 s, agreeing with the
84 s gap between consecutive log lines. The fast lane is therefore ~113 s, not ~36 s. Still 13× better
than 1486 s, so the decision it supported stands; the number in it did not.

⚠ **A pipe makes this worse, not better.** Output through `|` is block-buffered, so a line can appear
long after the work that produced it — or several lines can appear at once, all sharing a timestamp
none of them earned. `grep --line-buffered` and `awk`'s `fflush()` exist for exactly this.

This is the third member of one family in a single day, and all three read a tool's *presentation* as
a fact: `grep -n | head` truncating the evidence before the counterexample; a quotation cut at the
conjunction that reversed it; and now a log timestamp taken for a completion time.

**So: to time a step, time the step.** Run it alone with a clock around it. Deriving durations from
the gaps between log lines measures when things were printed, which is a different quantity that
usually agrees and did not here.

## The reader and the recorder were the same person, and they still diverged (2026-09-06)

`tidal_locking.py` opened by stating that **none** of the six sources its document cites was held. Four
arrived that afternoon; two of them were read closely enough to **reverse this recipe's conclusion
about Venus**, and the header saying they did not exist was left standing. Worse, the same sentence
sat in `Result.notes`, so every body the recipe touched shipped the claim.

There was no handoff to lose it across. The seat that read the papers and the seat that should have
updated the sentence were the same seat, in the same hour, in the same file. **A number in prose
acquires the duty to be updated, and proximity does not discharge it** — the work of reading and the
work of recording are different acts, and doing both does not make them one.

The repair is not "all six are held now" either. Four states, not two:

| state | which | what it means for the recipe |
|---|---|---|
| not held | Goldreich & Soter 1966 · Murray & Dermott 1999 | `τ_lock` is carried as *what the document prints* |
| held and read | Leconte 2015 · Goldreich & Peale 1966 | the Venus reasoning stands on the papers |
| held, unread | Barnes 2017 | nothing rests on it yet |
| ⚠ held as a scan | Hut 1981 | `ω_eq/n` **still** comes from the document — the file exists and cannot be searched |

That last row is the one no two-way split has room for. **Having a paper and being able to read it are
different facts**, and a status that collapses them will send someone to grep an image.

⚠ **And check the count with the tool that counts.** A neighbouring claim — that five of a *different*
six were still absent — was nearly asserted from memory, and a grep of the provenance files "found"
two of them, both false positives (a citation inside another paper's provenance, and a common
surname). `scripts/refs/check_paper_held.py` exists for exactly this. Run on those six bibcodes it
returns one held and five absent, which is what the sentence now says.

## A complete sentence can still be out of scope (2026-09-06)

Goldreich & Peale, on capture from a retrograde start: *"In all cases, the capture probability is less
than 10% at the present value of e."* Quoted here as a general fact about retrograde starts. The next
sentence says whose: *"**Therefore, an initially retrograde spin for Mercury** could easily have been
accelerated through the synchronous state to its present value."*

⚠ **Nothing was cut mid-sentence.** The quotation was a whole sentence, accurately transcribed. Its
**scope** lived in the sentence after it — and the same paper gives the opposite figure for the other
body: *"For 0.0549 and (B−A)/C = 2×10⁻⁴, **P = 0.71**"*, which is the Moon's eccentricity. Retrograde
starts reach synchronous 71 % of the time there. Mercury under 10 %, the Moon 71 %, one paper.

So the earlier rule — *a quotation cut at a conjunction is not a quotation* — is too narrow. It catches
`However`, `But`, `Although`, `Yet`; it does not catch a quotation that ends cleanly and is then
narrowed. **The question is not where the sentence ends but where the claim's subject is pinned**, and
that can be one sentence later, or in a figure caption (Fig. 12 carries `(B−A)/C = 10⁻⁴`; the Moon's
number uses twice that, so *both* variables differ between the two cases).

⚠ **What this nearly cost.** The rule about to be written was "a retrograde start is not classified
1:1". It would have thrown out the Moon — the document's own canonical 1:1 anchor — which is the same
body that killed an eccentricity threshold of 0.01 earlier the same day, for the same reason. Twice in
one day, a general rule was drafted from one body's number and the Moon caught it.

⚠ **Read as page images, the gap is wider than either seat had it.** The OCR gives the Moon's
quadrupole as `2X10~\`, an exponent that is simply not in the text layer — so it was recovered, not
read. On the page it is **2×10⁻⁴, and it is Jeffreys 1961's derived value**, not the authors' own.
The same page says **six of the seven trials trapped the moon at synchronous rotation**, which is the
empirical claim behind the analytic `P = 0.71`.

And the two figures differ in **three** ways, not two. Fig. 12's caption reads `(B−A)/C = 10⁻⁴`, Fig.
13's `10⁻⁶`, and both say **MacDonald's torques** — while the Moon's 0.71 comes from **Darwin's**
torque. The paper then declines to choose between the models: with Darwin's torque *"the capture
probability is >0.7 for e=0.2 and still >0.2 for e=0.1"*, i.e. Mercury-like eccentricities give the
opposite answer, and the authors write that they *"prefer to reserve judgment on this matter until
more information is available."*

So the "<10 %" is not a fact about retrograde starts, nor even about Mercury: it is a fact about
Mercury **under one of two tidal-torque models the paper refuses to pick between**.

The honest form: **retrograde does not decide the state.** Capture probability depends on `e` and
`(B−A)/C`, we compute neither, so a retrograde start is **recorded as a state and never used as a
classifier**.

(Third finding from an OCR scan today. The provenance warning written for Hut 1981 belongs on this
file too.)

## A confirmation that did not survive being checked (2026-09-06)

Almost everything recorded about `tidal_locking` on the day it was built is a defect, and a reader
meeting only that list would trust the recipe less than it deserves. So a confirmation was drafted — at the directing seat's request, and this seat agreed with the reason
and wrote it. **The request opened the slot and this seat filled it with something under-checked**;
recording only one half would let the next reader blame either the asking or the writing, and it took
both. A confirmation has to arrive on its own; a slot held open for one gets filled by whatever is
nearest.

The draft ran:
Goldreich & Peale compare two tidal-torque forms, and capture into Mercury's observed 3:2 resonance is
*"rather small (≲1/3)"* under MacDonald's but *">0.7 for e=0.2"* under **Darwin's with Q = const** —
so if our formula is the latter, the model this engine inherited predicts the state Mercury is
actually in.

**The identification does not hold.** It rested on the phrase *"constant Q"* matching our document's
*"constant-phase-lag (fixed-Q)"*. Read further, **both** of G&P's forms are phase-lag models: MacDonald's
puts a lag angle δ on a single bulge (*"we have used this expression for three different functional
forms of δ"* — the three curves in Figs. 12–13), while Darwin's expands the potential into Fourier
components and gives each one a lag with *"sin ε_i ≈ 1/Q"*. And Barnes 2017, which we hold, lists
**MacDonald 1964 and Goldreich & Soter 1966 in the same CPL camp**. Our formula cites Goldreich &
Soter, so CPL is established — and CPL does not separate G&P's two forms.

⚠ **So the confirmation is withdrawn, not weakened.** Which of G&P's two torques our `τ_lock`
corresponds to is not settled by anything held: the formula's own source is Goldreich & Soter 1966,
and it is not in the cache. **A wrong positive is worse than no positive**, because it is the entry a
later reader would lean on hardest.

What survives is smaller and real. Barnes 2017 **§2.1, "The Constant Phase Lag Model"**, says *"This
approach is commonly utilized in Solar System studies (e.g. **Goldreich and Soter 1966**; Greenberg
2009)"* — a section heading naming the model and citing our formula's source as an instance of it. So
**`τ_lock` is a constant-phase-lag form**, settled from a held paper. The finer question — which of
G&P's two phase-lag torques it is — stays open, because CPL does not separate them.

⚠ **Cite §2.1 and not the other list.** Elsewhere Barnes writes *"despite its relative success at
reproducing features in the Solar System, e.g. (MacDonald 1964; Hut 1981; Goldreich and Soter 1966;
Peale et al. 1979)"*, which reads like a CPL roster and is not one: **Hut 1981 also appears in Barnes's
CTL list** — *"the 'constant-timelag,' or CTL, model (Mignard 1979; Hut 1981; Greenberg 2009)"*. A
paper in both lists is the proof that the first is a list of successes, not of memberships. Leaning on
it would have handed the next reader an obvious objection.

⚠ **And that opens something about this recipe.** Its `τ_lock` comes from Goldreich & Soter — CPL by
§2.1 — while its equilibrium spin `ω_eq/n` comes from **Hut 1981, which Barnes cites for CTL**. Barnes
adds that the two *"reduce to the same set of governing equations **if** a linear dependence between
phase lags and tidal frequencies is assumed"*, so the mixture is safe only under that assumption, and
this recipe does not state it. ⚠ It cannot be checked either: Hut 1981 is held **as a scan**, so what
it actually assumes is unreadable here. Named, not resolved.

⚠ And the shape of the near-miss is the day's own: a technical phrase — *"constant Q"* — was matched
across two documents and taken for the same object. Same family as reading a name for a measurement,
one level up in abstraction. **The balancing entry the record wanted did not get to be written, and
that is the correct outcome.**
## (Superseded by the entry above) The draft confirmation, kept for its evidence

Almost everything recorded about `tidal_locking` on the day it was built is a defect — a table its own
formula cannot reproduce, a header claiming its sources were absent while standing on two of them, a
justification comment that fails on the body its test pins, a sign that read "not despun" as "locked".
A reader meeting only that list would trust this recipe less than it deserves. **A confirmation is
evidence too, and this one is worth its line.**

Goldreich & Peale compare two tidal-torque models. Under **MacDonald's**, capture into Mercury's 3:2
resonance is *"rather small (≲1/3)"* — which sits badly with Mercury being observed in exactly that
state. Under **Darwin's with Q = const**, *"the capture probability is >0.7 for e=0.2"*. Our
methodology document specifies the **constant-phase-lag (fixed-Q)** form, which is the second of those.
**The model this engine inherited is the one that predicts the state Mercury is actually in**, and the
alternative is the one that struggles with it.

⚠ **Credit it to the right thing.** This engine does not compute capture probabilities at all — it
classifies on eccentricity and a boolean quadrupole. So the agreement belongs to **the document's
choice of model**, not to any code here, and the green test does not test it. Same wiring/answer split
as everywhere else: the test says the pipe carries a value, and this paragraph is the only thing that
says the value's family is the right one.

⚠ And the number needed its subject to mean this. `>0.7` read alone says nothing; the antecedent two
sentences up is *the capture probability **at the 3/2 resonance***. Read without it, the same figure
supports the opposite reading — that our model predicts Mercury should be synchronous, which it is
not. The OCR flattens that sentence to `at the § resonance is rather small (<i)`, so the page image is
what settled it.

## The wanted conclusion picking the constant, three times in one day (2026-09-06)

One entry, not three, because the third only survived as long as it did by looking like the opposite
of the first two.

Venus will not despin under the printed formula with the printed `Q/k₂` class of 10²–10³; it needs
about 28. Three ways of resolving that came up, and all three are the same move — **the constant
chosen by the answer wanted, rather than by data.**

1. **Give Venus its own `Q/k₂`.** Rejected: the document prints no such number, and inventing one is
   the silent default this engine spent two days removing.
2. **Widen the class band until Venus falls inside.** Rejected for the same reason with a different
   handle — the band's ends come from the document or they are ours.
3. ⚠ **Distrust the inverted `ω₀` because it looks slow, and prefer the optimistic `Q/k₂`.** The
   inversion puts Venus's required initial period at **18.0–174.7 h**, and this seat called the slow
   end *"suspiciously slow for a primordial spin"* — which would have pushed `Q/k₂` toward its
   optimistic end for no reason but discomfort.

⚠ **The third looked like the opposite of the first two, and that is why it nearly passed.** One and
two try to let Venus **in**; three doubts Venus's own number. Opposite intentions, identical mechanics.
Whatever comes fourth will not look like these either.

**The measurement that killed it.** Barnes uses an initial period of **3 days = 72 h** for the Earth as
a worked example. The value called suspicious is **174.7 h = 7.3 days** — a factor of **2.4**. Not an
order of magnitude, and not against a limit: 72 h is itself an adopted value, so calling 175 h odd
while accepting 72 h states a preference and nothing more. **The literature gives no slow-side limit
at all** — that was established the same afternoon and then forgotten one message later.

**What is kept instead.** The mechanism, with the conclusion withheld: *the inversion constrains
`Q/k₂` the moment a slow-side limit on primordial spin exists, and no such limit exists, so it
constrains nothing today.* That sentence goes to work by itself when someone arrives with a limit. A
band narrowed now by intuition would be inherited as a number whose reason had evaporated — the exact
failure this file records elsewhere.

And the teeth are elsewhere: run the inversion on **every body whose present spin is measured** and see
whether the bands overlap at the same end of `Q/k₂`. That constrains without any slow-side limit, and
it can actually fail.

→ The same disease with a different organ: *"What converged was my arithmetic, not my input"* below,
where the machine chose the **precision** rather than the value.

## An absence claim about the literature is a search result, not an inference (2026-09-06)

Venus's moment of inertia was recorded here as *"not measured — no orbiter has determined it well"*.
The reasoning was sound and the conclusion was wrong: **Margot et al. 2021** (`2021NatAs...5..676M`,
Nature Astronomy, 53 citations) measures it from the spin-axis precession using **radar speckle
tracking from Earth** — *"which gives a normalized moment of inertia of 0.337 ± 0.024"*. Orbiters were
the wrong place to look, and "no orbiter did it" was quietly promoted to "nobody did it".

⚠ **The second time this shape has appeared.** On 2026-09-04, C18 was written as *"no held paper prints
this scaling"*, and the paper existed. Both were arrived at by reasoning about **what such a
measurement would require** and concluding from difficulty that it had not happened. Neither was a
search.

**So: an absence claim about the literature has to come from a query, not from an argument.** Two ADS
lines settle it. The argument only ever establishes that *we* have not seen it.

⚠ **And the correction changed the record's shape, not just a number.** The note about to be written
said the consistency window's two ends carry different **grades** — floor from measurements, ceiling
from an estimate. All four are measurements. What is true instead is a difference in **precision**:
Venus's `C/MR²` carries ±7 % (*"residual uncertainties of 7 % with the data obtained to date"*) where
Mercury's, the Moon's and Io's are far tighter. So the ceiling carries a band and the floor does not —
`α_Venus` moving from 0.313 to 0.361 slides the ceiling from 17.06 to 19.67 h, while the floor stays
at 4.597 h because a different body sets it.

Using the measured 0.337 rather than the assumed 0.33 moves the ceiling 17.98 → **18.36 h**. The
verdict does not change and the margin at the floor is untouched at +8.8 %, which is the point: the
correction was worth making for the record's honesty, not because it rescued a conclusion.

## What converged was my arithmetic, not my input (2026-09-06)

← The same family as *"The wanted conclusion picking the constant"* above: in both, a number's
authority came from a machine rather than from evidence. There it chose the **value**; here it chose
the **number of digits**, which is why the check is a different one — *did I look at where the input's
precision ends?* — and why it is filed separately.

Asked how much higher the `Q/k₂` ceiling would have to be to exclude this code's default `ω₀`, this
seat bisected until the answer stopped moving and reported **1087.4**. Five significant figures.

The constant it is a fraction of is written, in our own source, as `~10³`. **With the tilde.** The
document does not claim that boundary to one significant figure, so a crossing point expressed to five
is not a measurement of anything — the answer inherits the input's precision, and nobody had looked at
what that was.

**What made it look sound**: the bisection genuinely converged, to a floor of 5.000000 h. But a
bisection converges on the function it was handed, and the uncertainty was never in the function. **The
convergence was of the arithmetic, not of the input.**

⚠ **The confirming evidence pointed the wrong way, and that is the part to remember.** Three seats
computed this crossing and got **1086, 1087.4, 1089** — and the near-agreement read as corroboration.
It was the opposite: all three used bisection, so the spread is nothing but the input constants each
stood on, and three seats agreeing to three digits on differing inputs is a **measurement of how little
the third digit means**. Agreement in a digit that no input supports is not agreement.

There is even a real effect here, and it also does not survive the check: the window floor is **not**
exactly proportional to the ceiling (floor/ceiling drifts 4.6040 → 4.5890 across ceilings 500 → 2000,
which the `n` term makes real), so extrapolating from a bracket is genuinely the wrong method. ⚠ But
that drift is **0.3 %, smaller than the third-digit spread being argued over** — so the methodological
point, correct in itself, was already outside the precision the tilde allows. **Being right about the
method does not license a digit the input cannot support.**

**What is written instead**: *the 5 h default is excluded if the ceiling is under 10 % higher than the
printed one, and the printed one carries a tilde.* One digit, and it says the same thing.

**The check, before quoting a derived number**: find the *least* precise input it stands on and count
its significant figures. A tilde in a source is that count already — it is the source saying it will
not be read more closely than this.

## A square root that extracts as a lone letter, and the factor of 4.4 it cost (2026-09-06)

Barnes 2017's equation (6) sets the eccentricity at which the CPL model's equilibrium spin jumps from
1:1 to 3:2. A brief carried that threshold as **1/19 = 0.0526**, quoted from a plain-text extraction.
The page image says **√(1/19) = 0.2294**.

`pdftotext -raw` renders the radical as a bare `p` on its own line, and it lands in the middle of a
sentence:

    eccentricities below
    p
    1/19, the torque on the rotation by the tidal waves is insufficient

A lone `p` in running prose is not a word. That is the tell, and it is available without the image —
but only to a reader who notices that the sentence has a letter in it that cannot be there.

**What the factor of 4.4 decided**: at 0.0526 the Moon (e = 0.0549) sits 4 % *above* the threshold, so
CPL predicts 3:2 against the Moon's observed 1:1 — an apparent contradiction, and a brief was written
around resolving it. At 0.2294 the Moon is at 0.24 of the threshold, CPL predicts 1:1, and there is
nothing to resolve. **The body that actually lands near the threshold is Mercury**, at 0.90 of it —
and there the direction is reversed: CPL predicts 1:1 where the observation is 3:2, which is a
capture question, not an equilibrium one.

⚠ **The seat that wrote the brief had already written "verify equations (6), (15) and (16) on the page
image, the plain text mangles subscripts" into that same brief** — and then took its own quotation from
the text layer. Writing the precaution and applying it are separate acts, and the first does not
perform the second.

**The check**: when a quoted number comes from an extracted PDF, render the page. `pdftoppm -f <page>
-l <page> -r 150 -png <pdf> <out>` costs one command. Everything a maths glyph can lose in extraction —
a radical, an exponent, a subscript, a minus sign — loses it silently and leaves a plausible number
behind. Equations (15) and (16) came through the same extraction **correctly**, which is exactly why
the wrong one was believed.

## The checker was in the state it was checking for, three times (2026-09-06)

One entry, not three, because the check that catches all of them is the same one: **before trusting a
thing that inspects, inspect it with its own criterion.** They do not look alike otherwise, which is
why they were nearly filed apart.

1. **A repair script assumed the defect it was repairing was absent.** It took "a paragraph runs until
   a blank line" as its boundary while fixing a paragraph whose *missing blank line* was the defect,
   and swallowed the three table rows that followed. Recorded above under the two-tables entry.
2. **Guardrail ⑤ was checked against a set someone typed.** `recipe_arrived()` was proven to work by
   handing it a made-up node name — which shows the function returns the right thing, and does not
   make the gate red on the day a recipe actually lands. It reads the live registry now, and that
   distinction is written into the test beside the call.
3. **A diagnostic reported the wrong diagnosis.** `check_md_dupes.py` was extended to say whether a
   skip entry had excluded anything, precisely so that a skip doing no work would stop looking like a
   skip doing work. The first version asked `(ROOT / d).exists()` — **every skip target in this
   repository is nested** (`engine/.venv`, `docs/phase3/_papers`), so it reported `_papers` as absent
   from a tree that contains it. ⚠ The check existed to expose a claim that was not what it appeared;
   it made one.

**Why the third stings most**: it was written *in response to* the second, in the same hour, with the
lesson stated in its own docstring. Knowing the failure mode and being about to commit it are
compatible states.

**The check**: run the inspector against a case whose answer you already know **from outside the
inspector** — a repository where the thing is present, a set the registry really returns, a directory
you have listed by hand. A passing self-report is the weakest evidence available, because a checker
that does nothing reports success exactly the same way.

## A green gate needs the end; a red one does not (2026-09-06)

The rule written this morning — *the `GATE END … rc=` line is the verdict, never the body's "통과"
text* — was applied to failures as well, and it should not have been. **The two directions are not
symmetric.**

- **`rc=0` needs the whole run.** A check that has not run yet can still fail, so no amount of `[PASS]`
  in the body licenses a push.
- **One `[FAIL]` line settles it immediately.** Whatever follows, `rc` will be 1. There is nothing to
  wait for.

gate135 printed two `[FAIL]` lines for unlinked citations inside its first minute, and this seat waited
**24 minutes** for the `rc=` line before reading them. The failure was visible the whole time.

⚠ **The block order was moved earlier that same afternoon for exactly this** — so a broken document
reports in about a minute instead of at the end — and the benefit went unused, because the discipline
built around *not* trusting the body text was applied where the body text is conclusive.

⚠ **What killing early costs**: the checks after the failure never run, so the next round can surface
something new. That is still much cheaper than 24 minutes, a fix, and 24 more.

**The check**: watch the log for `[FAIL]`, not only for `GATE END`. On a hit, kill the process group,
fix, restart.

## Run the checks the file you touched is subject to, not the checks you wrote (2026-09-06)

The local dry run before that commit was three checks — the Markdown table renderer, the duplicate
section finder, and the recipe's own tests. All three were written by this seat in the preceding hours.
The file actually edited was `docs/reference/paper-defects.md`, and the check it is subject to —
citation links must be clickable ADS URLs — was not among them.

**The step that was missing is one line**: list the files in `git diff --name-only`, then find every
gate check that reads that path and run those. `grep -n "python3 scripts/" scripts/check.sh` prints
the whole set in one screen.

**Why it happened is worth naming**: recently-written checks are the ones in mind, and running them
feels like having run the checks. Familiarity is not coverage.

## Survey an output format from the logs, not from the source (2026-09-06)

The rule above — *watch the log for `[FAIL]`, not only for `GATE END`* — needs to know what a failure
looks like. Grepping the checks for the literal `[FAIL]` said seventeen files had it and sixteen engine
tests did not. **Both halves of that were wrong.**

- **Invisible to grep, present at runtime.** `print(f"  [{'PASS' if mono else 'FAIL'}] …")` emits
  `[FAIL]` and contains no such literal. Most of those sixteen were this.
- **Visible to grep, useless as a pattern.** Three more report failure only by returning 1 —
  `check_via.py`, `dynamo_table.py`, `build_sitemap.py` print no marker at all, so no log watcher can
  see them. They are fixed at the **call site** rather than in the tools: the format should belong to
  the gate, and those three are run by hand elsewhere.

Counting the real formats needed the logs, and there were four: `[FAIL]`, `실패 N건`, `N건 실패`, and
`test_silicate_melt: FAIL N`.

⚠ **Then the pattern itself had to be measured**, because the obvious one is wrong here too. `FAIL|실패`
matches **ten times in a fully green log** — a `FAIL: 0` counter, a section heading reading
*(missing = 실패, stale = 경고)*, and the word inside a `[PASS]` summary. A watcher on that pattern
would have woken on every run. Excluding the zero cases —
`\[FAIL\]|FAIL [1-9]|실패 [1-9][0-9]*건|[1-9][0-9]*건 실패` — gives **0 hits across three green logs
and exactly the two real lines in the red one.**

**The check**: to learn what a program prints, read what it printed. Source tells you what someone
typed, and a formatted string is assembled from pieces none of which is the output.

## The list of checks to run is made by a path, not by a person (2026-09-06)

The entry above says: run the checks the file you touched is subject to. The next question is who
builds that list, and the answer must not be "whoever is at the keyboard" — that is the failure being
repaired, one level up.

`bash scripts/check.sh --wiring` already does it. It reads `git diff --name-only`, decides from the
paths whether the physics lane is needed, and runs the documentation checks in about two minutes.
After the citation-link failure this seat picked six checks by hand, got all six right, and **still
did the wrong thing**: a correct hand-built list is one correct instance of a judgement that has
already failed once. The lane makes the same list from the paths every time.

## No value was wrong today, and that is not a property of the mistakes (2026-09-06)

Counting this seat's errors over one day: a threshold read as `1/19` where the page prints `√(1/19)`;
a crossing point quoted to five significant figures against a one-figure input; a bibcode shipped
without its ADS link; a presence check that asked the wrong directory; a log watcher that matched one
of four failure formats; a gate left running for 24 minutes after it had already failed.

**Exactly one of those could have reached a value**, and it was caught — on the page image, before it
was written anywhere. The rest were quality, not arithmetic.

⚠ **That is a fact about today, not about the class of mistake.** The reason nothing landed is that the
reproductions were tight: before-and-after measured on real bodies, tests written so that reverting the
change breaks them, patterns validated against known-green and known-red logs, anchors dry-run for
uniqueness before any file was touched. **Take one of those away and the same list ends differently** —
the five-significant-figure number was already committed and would have stood if it had shipped, and
the square root would have propagated into a brief, an item and a recipe.

**The reading to avoid**: *my errors tend not to touch values.* They tend not to **survive**, which is a
statement about the checking and not about the errors. Written down because the first reading is the
comfortable one, and it would quietly license loosening the second.

## The seat that built the check is the one it caught, twice in a day (2026-09-06)

Two failures reached the gate from newly written prose, and both broke a citation rule this repository
already enforces.

- **gate135**: a bibcode shipped without its ADS link, in a file where every other row carries one.
- **gate139**: `chain.yaml:96` — a line-number citation, in the file whose own C33 work replaced line
  numbers with phrase anchors **because line numbers drift**. The checker that caught it was written
  by this seat the day before.

⚠ **This is the sibling of the entry above.** There, the thing that inspects was in the state it
inspects for. Here, the person who wrote the rule broke the rule — and neither is carelessness in the
usual sense: **the rule was fresh enough to be top of mind and still did not fire while writing.**
Knowing a rule and applying it while composing a sentence are separate faculties, and only the second
one is checkable.

**Both were caught, both cost a gate run, and both were avoidable for 106 seconds.**
`bash scripts/check.sh --wiring` before the commit runs every documentation check the changed paths
are subject to. The lesson is not "remember the citation rules" — that is what failed twice. It is
**stop treating the pre-commit run as optional for prose**, since prose is where the citation rules
live.

## Every citation rule we have is a format check, and none of them reads the citation (2026-09-06)

Three citation disciplines were tightened or enforced today — phrase anchors instead of line numbers,
bibcodes as clickable ADS URLs, quotations checked against the sentence they sit in. **All three are
checks on the shape of the reference. None of them opens what is referenced.**

The gap showed itself at the end of the day. `chain.yaml:96` failed the line-number check, and the
cheapest repair was to swap the line number for a phrase from that line — form satisfied, gate green,
two minutes. Opening the node instead turned up that it is declared `kind: measured`: **it is supplied,
not computed, so the recipe this item was waiting for is never coming**, and the guardrail meant to
stop a placeholder becoming permanent watches an event that cannot happen. That became C42, and none
of it is visible from the citation's shape.

⚠ **The incentive runs the wrong way, and that is the part to keep.** *The cheapest way to fix a
citation is not to read what it cites.* Every format rule can be satisfied without opening the source,
and a fix made that way leaves a reference that is correctly formatted and wrong. **The checks catch
the class of error that costs least and cannot see the class that costs most.**

**What follows from it**: a citation repair is a reason to open the source, not a reason to avoid it.
Not because reading is a virtue — because a citation that needed repairing is evidence that whoever
wrote it had the source less firmly in hand than they thought.

## A directing seat's error does not stay local — it ships as an instruction (2026-09-06)

Counting the day's cross-seat corrections honestly, because the first count was wrong in a way worth
keeping.

This seat's summary claimed the directing seat had corrected three of its conclusions and been
corrected twice. **Two of those three were the other way round**, and one item was listed on both
sides:

- **√(1/19)** — the directing seat's brief carried the CPL threshold as `1/19`, taken from a
  plain-text extraction where the radical had dropped out. **This seat rendered the page and caught
  it.** Their error, our find.
- **The duplicate-heading predicate** — proposed by the directing seat as "one line is enough".
  **Measured here before building**: 11 files match, every one of them legitimate structure. Replaced
  with a body comparison. Their proposal, our correction.
- **The five significant figures** — this seat produced `1087.4` against an input printed with a
  tilde, and the directing seat caught it. Correctly attributed the first time.

⚠ **The asymmetry is the point, not the tally.** A working seat's error is one commit and lives until
a gate or a review finds it. **A directing seat's error becomes a brief**, is read as an instruction,
and gets built on before anyone checks it. The `√(1/19)` case is exactly that shape: had the page not
been rendered, the wrong threshold would have propagated into a brief, an item and a recipe — and the
recipe would have contradicted the Moon, our own anchor.

**So the checking is not symmetric either.** Verifying an instruction before acting on it is not
insubordination or duplicated effort; it is the only place that class of error can still be caught
cheaply. Both seats spent the day re-measuring what the other handed over, and that is what made the
pairing worth having.

⚠ **And getting the attribution right matters for the same reason the errors do.** A record that says
the directing seat caught three and made none teaches the next reader to take briefs at face value.

## A unit suffix and a frame difference look identical (2026-09-07)

C37 was `rotation_period` against `rotation_period_h`: one quantity, two spellings, a genuine
one-line bug. `semi_major_axis_km` against `semi_major_axis_au` has the same shape — same stem, a unit
suffix, two recipes reading one and one reading the other — and the same repair would have written a
wrong number into the engine.

They are **not one quantity in two units**. A moon's `semi_major_axis_km` is planetocentric; the
`semi_major_axis_au` that `body_class` consumes is the distance from the star, because its only
consumer asks where in the protoplanetary disc a core grew. Converting kilometres to AU produces a
number of the right dimension in the wrong frame, and Pandora's pebble-isolation boundary flips
BELOW→ABOVE on it.

⚠ **What makes this one worth its own entry**: the surface did not merely look like a generic naming
bug, **it looked like our own previous fix.** C37 was recent, correct, and shaped exactly like this,
which supplied both the pattern and the confidence. Matching against a repair you yourself made a day
earlier feels like experience rather than like guessing.

**The check that separates them**: for two names of an apparently identical quantity, ask what each
consumer *does* with the value, not what the names say. `pebble_isolation_mass` reads its argument as
a heliocentric distance; `despin_timescale_yr` reads its argument as an orbit about the perturber it
was handed. Two readings, so two quantities — visible in the consumers and in nothing else.

⚠ **A second thing in the same edit, and it is the same disease as the entry above.** The citations to
`body_class.py` were first written as `` `body_class.py`@«…» `` — a backtick after the filename rather
than around the whole citation. `check_refs` reported **406 anchors before the edit and 406 after**:
the new citations were not wrong, they were **invisible**, and the gate would have stayed green over
them. Caught by comparing the count across the change rather than by reading the `[PASS]` line. **A
format that is not parsed and a format that is correct produce the same green.**

## Never `git stash` here, and the reason is not tidiness (2026-09-07)

Comparing an anchor count across an edit needed the file in its pre-edit state for one command, and
this seat reached for `git stash -q --keep-index`, popped immediately, and verified the stack was
empty and the tree intact. **The execution was clean and the choice of tool was still wrong.**

**The stash stack is shared by every worktree of one repository.** This repository currently has
three — `NearStars` on `main`, `NearStars-wt/engine-prototype` on `engine/prototype`,
`NearStars-wt/site` on `gh-pages` — and several seats work across them. A push and a pop are separate
operations on one shared stack, so **another seat stashing at the same moment means this seat's pop
takes someone else's work.** Nothing about doing it carefully closes that window; it is not atomic.

**The replacement is read-only and touches nothing shared**:

    git show HEAD:engine/interior-core.md > /tmp/before.md

Compare against that. It cannot lose another seat's changes because it never writes.

## If a check counts something, check that the count grows (2026-09-07)

`check_refs` reports a total: *"앵커 406건 전부 대상 문서에서 정확히 1회 매치"*. Two code citations were
added and it reported **406 again** — because they were written `` `file`@«…» `` instead of
`` `file@«…»` `` and the parser did not recognise them as citations at all. Nothing to match, so
nothing to fail. `[PASS]`. After the form was corrected: **408.**

⚠ **This is the worst shape in today's family of blind checks.** The others — a skip that never
reached its directory, a guardrail watching an event that cannot occur — were checks doing *nothing*.
This one **did not recognise its own subject**: citations can be added indefinitely and the count will
not move, so the check never grows with what it is supposed to cover.

**The check on the check**: when a checker reports a total, occasionally confirm the total moves when
you have given it more to count. **A number that does not grow when the corpus grew is a checker that
has gone blind**, and it is indistinguishable from a passing one in every other respect.

## A wrong input produced a plausible table, and the table could not have caught it (2026-09-07)

Measuring C21's ²⁶Al pulse against each moon's gravitational binding energy needed five densities. The
board has all five. This seat typed them from expectation instead — 2000, 2620, 2830, 3000, 4900 kg/m³
— computed the table, and read it as a result.

Cassandra's real density is **5467 kg/m³**. The guess was **82 % low**, and the column it produced
looked entirely reasonable: monotonic with size, small moons dominated by the pulse, large moons not.
**Every qualitative feature the table was built to show survived the wrong number**, which is precisely
why reading the output would never have found it.

It was caught by re-deriving the densities from the board before reporting — not by the table looking
odd, because it did not.

⚠ **The general form, and it is the sharp end of a rule already in this file.** Elsewhere this file says
*read the actual error, do not pattern-match*. This is its input-side twin: **a fabricated input that is
the right order of magnitude yields output with the right shape, and output-shaped checks are blind to
it.** Plausibility is what a fabricated number is optimised for — it is generated by the same intuition
that will later judge whether the answer looks sensible, so the judge and the defendant are the same
faculty.

**The check**: any number that exists in a file must be read from the file, every time, including the
ones you are confident about. Confidence is the signal that the lookup will be skipped, not evidence
that it can be.

## A closure is only as independent as its least independent input (2026-09-07)

C21's ²⁶Al measurement produced a threshold of 1.42–1.44 Myr, and a paragraph elsewhere in the same
file quoted a published band of 1.3–1.9 Ma for the same quantity. This seat reported it as an
**independent** closure "from a different paper and a different method", and the directing seat agreed
it was the strongest result of the day — *"nobody designed this as a check and it closed anyway."*

**It is the same paper.** The band comes from Neumann & Kruse 2019, and every constant in the
measurement — decay energy, half-life, aluminium fraction, initial ratio — came from that paper's
Table 2. The method genuinely differs (a hand energy budget against their thermal-evolution model), so
the agreement does show the arithmetic and unit handling are sound. **It cannot show the constants or
the framing are right, because it inherited both from the thing it agrees with.**

⚠ **The word did the damage, not the number.** "Independent" is what made it read as outside
confirmation, and it survived a full round of cross-seat reporting — both seats treating it as the
day's best evidence — because neither compared the bibcodes. **The check is one line**: list the inputs
your result stands on, and strike any source that also produced the thing you are closing against. What
is left is the independence you actually have.

⚠ **A motive was first written here as the cause — "the measurement had contradicted its own
pre-registration and wanted corroborating" — and it is struck.** The owner pointed out that our bodies
are invented, so nothing had been refuted and there was no shortfall to make up. The story was
plausible, which is the whole problem with it.

**The rule that replaces it is stronger than "beware wrong motives":**

> **When a procedural cause and a motivational cause both fit, record only the procedural one.
> Procedure can be checked; motive cannot.**

The two failures in this file's neighbouring entries make the asymmetry concrete. A fabricated density
optimises for plausibility **and can still be caught** — the board holds the real number, so there is
something to compare against. A fabricated motive optimises for plausibility **and there is nothing to
compare against at all.** This one surfaced only because the owner knocked out its premise, not because
anyone inspected the story.

⚠ **This holds even when the motive happens to be true.** An unfalsifiable sentence earns little space
in a record regardless of its accuracy. Here the procedural cause is complete on its own — **the source
was named before it was checked** — and a reader can verify that by opening the same two bibcodes.

### Two near-misses, and only one of them can become a tool

The day's two most dangerous errors did not touch a value; each would have made a conclusion carry more
weight than it had earned. **No gate looks at that.** But they are not the same kind of thing, and
filing them together would bury the one that is fixable.

| the claim | why it was wrong | can a check find it? |
|---|---|---|
| *"an **independent** closure"* | the comparison's source was also the source of the inputs | **yes** — compare bibcodes |
| *"the pre-registration was **refuted**"* | our bodies are invented, so nothing could refute it | **no** — it asks what the objects are |

**The first is mechanisable, and the check is already written above**: list what a result stands on,
strike any source that also produced what it closes against. A crude form would catch the actual case —
*a section that claims independence while citing a bibcode that also appears among its own inputs.*
⚠ **Measured before proposing it**: "independent" appears 19 times in `interior-core.md` alone, so a
naive matcher would be noisy and would need the two bibcode sets, not the word. **Not built now** —
C45 comes first — but recorded here as a **candidate**, because filing it under "checks cannot catch
this" guarantees nobody looks again.

**The second is not mechanisable and should not be dressed up as if it were.** Whether a calculation
can be refuted depends on whether its subject is a thing in the world or a thing we chose, and that is
a question about the object, not about the text. **It took the owner one sentence.** ⚠ A record that
files both under "tooling gap" hides the fact that **one of them needs a person**, and pretending
otherwise is how the reading gets dropped.

⚠ **The claim also grew as it was passed along, and the growth is worth recording separately.** The
working seat wrote "closure" in its own section and "independent … from a different paper" alongside
it; the directing seat promoted that to *"the strongest result of the day"* and **sent it onward to the
owner**. Two seats, two steps, and **the amplification happened at the one that had to present it** —
the further from the arithmetic, the larger the claim. Neither step involved a check; each involved
agreeing with the previous one.

⚠ **Correcting it must not overshoot either.** Struck to "not independent" alone, the record would call
a real implementation check worthless: reproducing a paper's own threshold from its own constants does
rule out a dropped factor or a mistaken unit, which is exactly the failure class that cost this project
a square root, an atomic mass and five significant figures **the same day**. **What it is and what it is
not have to be written as one pair**, or the next correction over-corrects.

## A proposed shape is a sketch until someone measures it (2026-09-07)

Twice in two days the directing seat handed over a detector's shape and the working seat measured it
before building, and both times the shape was wrong:

- **The duplicate-section check** — proposed as *"one line is enough: the same `##` twice in one file"*.
  Measured first: **11 files match and every one is legitimate structure** — per-planet sections,
  per-field sections, a per-case template. Rebuilt on identical bodies with a length floor, which gives
  zero false positives.
- **The independence check** — proposed with the suggestion that the word could carry it. Measured
  first: **`independent` occurs 19 times in `interior-core.md` alone**, so a word matcher would be
  noise and the real predicate needs two bibcode sets.

⚠ **A third instance was claimed in conversation — the Markdown table checker — and this record does not
support it.** That checker's header says only that the obvious test *"was tried first and is wrong
here"*, attributing it to nobody. **Two verified, one unattributed**, which is the count that goes in.

**What this is not**: a claim that the directing seat proposes badly. A first shape is *supposed* to be
the obvious one — that is what makes it worth measuring, and the obvious form is the right place to
start. **What it is**: the measuring step is not optional politeness toward a proposal, it is the step
that decides whether the proposal survives. Both surviving detectors look nothing like their first
draft.

⚠ **And the direction matters for whoever reads a brief next.** A shape arriving as an instruction is
easy to build as given; measuring it first can feel like doubting the sender. **Neither of the two
above would have worked as sent**, and each was cheap to check — one `grep -c`, one small script.
**At that price, whether checking counts as doubt cannot be the question.** Measure, then build, and
put the measurement in the checker's own header so the dead end stays marked rather than merely
avoided.

⚠ **A count offered against oneself still needs checking.** The "three times" above came from the
directing seat as self-criticism, and self-criticism is the form of claim least likely to be audited —
disagreeing with it feels like arguing for someone's comfort rather than for accuracy. It was still
**counted from memory, and the record supports two.**

**The mirror image from earlier the same day is verified too**, and by the same kind of one-line query:
a `main` commit count reported as 2 where there were 7.

    git log --oneline 4ab21351..163c7735   # 4ab21351 was origin/main, 163c7735 the local HEAD → 7

⚠ **An earlier draft of this paragraph filed that one as "their account, not verified", because it does
not appear in `interior-core.md`.** It was in `main`'s history the whole time. **"Not in the record I
was reading" is not the same as "not checkable"**, and treating them as equivalent is how a verifiable
claim gets archived as hearsay — the conservative-looking move, and still wrong.

**The pair is the useful part.** One count too low, one too high, opposite directions, **the same
cause: a number recalled instead of queried** — and each separated from the truth by a single command.
Whether the recollection flatters or accuses changes nothing about which it is. ⚠ Note which direction
each ran: the morning's error made a mistake sound **smaller**, the afternoon's made one sound
**larger**. Memory does not err in a consistent direction, so "it was against my own interest" predicts
nothing about accuracy.

## The absence rule applies to our own repository too (2026-09-07)

An earlier rule in this file says: *an absence claim about the literature is a search result, not an
inference.* It was written about ADS. **It holds for `grep` as well, and this is the case that shows
it.**

C21's melting requirement was published here twice saying latent heat was excluded *"because no held
source gives one for silicate"*. `engine/eos.py` line 1989:

    SILICATE_MELT_DH = 4.0e5      # J/kg. Monteux+ 2016 Table 1, ΔH (Ghosh & McSween 1998)

⚠ **The measurement called `eos.silicate_solidus` from that same file.** The constant sat six lines from
a function already in use, cited, in a paper already held and already quoted elsewhere in the same
section. Nothing was hidden; nothing was searched.

**Why "our own code" is the harder case.** An absence claim about the literature at least feels like a
claim — you know you have not read everything. A claim about your own repository feels like knowledge,
because you wrote it. **Familiarity is what makes the search feel unnecessary**, which is the same
sentence this file already carries about running the checks you wrote rather than the ones the file is
subject to.

**The check is the same as the literature one, pointed inward**: before writing *we do not have X*, run
the query. `grep -rn "latent\|MELT_DH" engine/` costs a second and is the whole difference between a
recorded fact and a recorded guess.

## An unevaluated term is not evidence for either side (2026-09-07)

Both seats predicted that adding the missing latent heat would sink the 50 % rock row. It survives at
**1.25×**: `ΔH` is 24 % of the sensible heat, not a term of comparable size.

⚠ **Both guesses ran the same direction** — each assumed the unquantified term was large enough to
overturn the result. That is not symmetric error; it is a shared bias toward treating *unknown* as
*decisive*, which reads as caution and functions as a prediction.

**What it cost**: the section carried "latent heat could erase this margin by itself" as a live caveat
across several rounds of reporting, shaping how the result was described, and the number that settles
it was one multiplication away the whole time.

**The check**: when a missing term is named, either evaluate it or say only that it is missing.
**Saying it might overturn the result is a claim about its size**, and if you can make that claim you
can compute it.

## An absence claim also fails by reading the query for the shape you wanted (2026-09-07)

This file already carries two faces of the same rule — *an absence claim about the literature is a
search result, not an inference*, and its inward form for `grep`. **Here is the third, and it is the
one no amount of searching fixes.**

Branch B of C21 is "a body that orbits a star directly". The directing seat reported that the roster
had no such body. It had run the query. **`bodies/earth.yaml` — `kind: planet`, `parent: Sun` — was in
its own output**, and was read past while looking for a *small* body.

⚠ **This is not the failure of not searching.** The search ran, returned the right rows, and the answer
was still wrong. **The filter was in the reading**: a mental picture of what branch B would look like —
an asteroid, a belt object — and Earth did not match the picture even while matching the definition.

**Why it is the hardest of the three.** Not searching is fixable by a rule you can follow; this one
happens *inside* the step that is supposed to catch it, and it leaves the same evidence as success — a
query was run, output was read, a conclusion was drawn.

**The check that would have caught it**: state the criterion in the query's own terms and apply it to
every row mechanically. Branch B's criterion is `parent` is a star. Five rows, five checks, no picture
required. **When a definition exists, match rows against the definition and not against the example you
have in mind** — the example is what the definition was written to generalise past.

## Adding an output and forgetting its contract, twice in one day (2026-09-07)

Two commits added values to a recipe's `Result` and neither updated the methodology document's
`Returns` line. `check_contracts` caught both, at the cost of a full-lane gate each time:

- **C43** added `is_satellite` to `body_class`'s inputs. Caught at the *next* gate, which was a
  24-minute run whose only finding was this.
- **C46** added `regime_candidates`, `regime_excluded` and `regime_flux_cannot_decide` to
  `heat_transport_mode`. Caught the same way, 25 minutes later.

⚠ **Both were preceded by a local dry run that could not have caught them.** The pre-commit checks used
were the markdown and citation ones plus the recipe's own tests — and `check_contracts` was in neither
set, because it takes minutes and reads every body. **The habit recorded earlier this week — run the
checks the file you touched is subject to — was followed, and the file touched was a `.py` whose
contract lives in a `.md` two directories away.**

**The check that costs seconds**: after changing any recipe's `values`, `inputs` or `units`, run
`cd engine && python3 check_contracts.py`. It is not fast, but it is far faster than the gate that will
run it anyway.

⚠ **And note which half of that checker works.** C45 records that `check_contracts` never sees the keys
a recipe *looks up* — it compares the labels a recipe puts on its evidence. **The `Returns` side it does
see**, and it caught both of these. The blind spot is the input side only, which makes the working half
worth using deliberately rather than waiting for the gate to use it.

## Every anchor we scored with defined the cell it was scored against (2026-09-07)

C46's ladder was checked against four solar-system bodies and reported 3 of 4, then 2 of 2 under a
different form. ⚠ **All four bodies are where the rungs came from.** §6.2's plate rung *is* Earth, its
stagnant rung *is* the Venus–Mars pair, its heat-pipe rung *is* Io. **The score measured arithmetic:
does a number exceed the rung it was used to set?**

**Both seats did this for two days without seeing it**, and the working seat had already written the
narrow version of the observation — *Mercury and Mars cannot be scored, because the 10–30 mW/m² the
document attaches to them is the stagnant rung itself.* ⚠ **The same sentence covers Earth and Io, and
neither seat extended it.** A correct observation was made about two bodies and stopped there.

**What broke it was fetching a body that is in no rung.** The Moon: undisputed one-plate, *in situ*
measurement, absent from every rung. It passes, and **that pass is the first one carrying information.**

**The rule**: when a scale's rungs are values from known bodies, **a body that supplied a rung cannot
test the scale.** List the rungs, list the scored bodies, and strike the intersection. What is left is
the test — and here it was one body out of five.

⚠ **Report the halves separately.** "Independent 1/1, self-scored 4/4" is honest; "5/5" is a tautology
wearing a score. **Adding them is the whole error**, because the large number comes from the part that
could not have failed.

⚠ **And a second thing fell out of the same look.** The stagnant rung's Venus half — 10–20 mW/m², from
a 1998 paper we do not hold — is superseded by Smrekar+ 2023's measured **78**, four to eight times
higher. **The rung has not moved.** Checking who set a rung also tells you when they set it, and a
twenty-five-year-old rung deserves that question asked out loud.

## A sweep that swept nothing, because a default binds at definition time (2026-09-08)

C48 needed one number: does Mars still diverge when C20's integration step is reduced? Four steps were
run — 4, 1, 0.25 and 0.1 Myr — and all four printed "diverged". The conclusion "the step is not the
cause" was one keystroke from being written into the item.

**All four ran at 4 Myr.**

```python
def integrate(params, t_c0, t_m0, age_gyr, step_myr: float = STEP_MYR)   # core_history.py:97
```

`ch.STEP_MYR = step` rebinds the module global. **The default was already evaluated when the function
was defined**, so it stays 4.0, and `solve` calls `integrate` with no fifth argument. The knob was not
connected to anything.

⚠ **What makes this family dangerous is not the bug, it is the plausibility of the output.** "Reducing
the step does not help" is a physically sensible result. Nothing about four identical answers looks
wrong; four identical answers are what a real negative result looks like. Same shape as C45, where a
checker compared labels and never read the lookup key it was supposed to check — **both were honestly
green, and both had looked at nothing.**

⚠ **And the rule against it was already written, twice.** `engine/test_interior.py`: an indicator must
*"fire above the threshold and stay silent below — **if it always fires it is a constant**"*. And
`CLAUDE.md` §4: write the failing test first. **A dead sweep makes its own knob a constant**, which is
exactly the condition that comment names.

**Why it got through anyway: the rule was attached to *tests*, and this was a throwaway measurement
script.** Nobody thinks of a scratch script as something that needs proving. So the widening, rather
than a new rule:

> **A script whose numbers you will report is a test.** Show that changing the input changes the
> output — if it never changes, that input is a constant, not a knob — and only then run the real
> thing.

**Applied immediately, and it works**: `prove_live()` runs Earth at 4 and 200 Myr and checks the step
count differs (1135 steps against a failure). One extra run.

**The script is on disk as [`mars_step_sweep.py`](mars_step_sweep.py), and its header exists to stop
the next seat rewriting it from memory** — which would mean falling into the same default-argument
trap. ⚠ It is a diagnostic, not a generator: it bakes nothing and belongs to no table above.
