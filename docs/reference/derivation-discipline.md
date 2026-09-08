<!-- 도출값을 사람 기억이 아니라 기계가 지키게 만드는 규율 — 왜 이렇게 정했는지의 근거 기록 -->
# Derivation discipline: why the recipes are built the way they are

NearStars derives a lot of numbers. A body's dipole field, its tidal heating, its
magnetopause standoff, the colour of its rings — each comes from a methodology document
that says how to get it from measured inputs and published physics.

That worked, and it also kept going wrong. Not spectacularly; quietly, in the way that a
number written in three places drifts in one of them and nobody notices for months. This
document records the disciplines adopted in response, and the specific failure behind each
one, so that a later reader can tell which rules are load-bearing and which are taste.

Every failure quoted below is one this project actually had.

---

## What kept going wrong

**A value moved and its dependants did not.** Proxima's magnetopause nose was updated from
23.5 to 35.33. `outer_compression` and `outer_extension` are functions of it and stayed at
their old values. Nothing caught it, because the relationship between the three numbers
existed only in the head of whoever last worked on that row.

**A worked example drifted from the formula it illustrated.** The dynamo scaling table
listed ε Ind A b's dipole moment as ~3 700 × Earth. Recomputing from the document's own
power law gives ~201 000 — a factor of 54. The table had been typed by hand and had not
been re-derived since an input changed.

**Two documents contradicted each other in the open.** The tidal-heating methodology and
the moon energy-budget methodology disagreed about whether the solid-body tidal term is
global or local. Both were published, both were being used, and the disagreement had no
owner because nothing compared them.

**Prose hid whether a recipe even applied.** A survey of which methodology documents state
their domain of validity returned "eight have none". Reading them showed the real number
was two: the other six state it perfectly well under headings nobody thought to search
for. The content was fine; the form made it unfindable, including to us.

**A vocabulary that rejected nothing.** The Phase 4 gate appeared to validate field names
against a menu. It did not — it only checked the axis key's suffix, and the field names
that actually ship went unchecked. Injecting `ZZZ_totally_bogus_name` into a board passed
with zero errors. Under that gate, 158 distinct field names accumulated, 36 of them used
exactly once, and `base_color` and `base_colour` shipped side by side. The duplicate was
recorded in three separate audit files; the fourth file simply added both spellings to the
menu, which made the drift legal.

The pattern is the same every time. **The knowledge was real but it lived in a person, and
people forget.** None of these were physics mistakes.

---

## The disciplines

### 1. A recipe returns a state, not a number

Every derivation returns the value *plus* the exact inputs it used, the regime it decided
it was in, a machine-written sentence saying why, a confidence grade, its citations, and
whether it converged. A bare number cannot be audited later; a state can.

Lives in `engine/payload.py`.

### 2. Out of domain is a return value, not an exception

When a recipe is handed a body it cannot handle, it returns that fact with a reason,
rather than raising or — worse — extrapolating. The giant-dynamo recipe declines brown
dwarfs explicitly, because the source refuses to supply the luminosity track that branch
would need. Declining is an answer. Guessing is not.

This is what the heat-transport contradiction cost us: neither document declined, so both
applied.

### 3. Anchor on published values, never on our own output

A recipe's tests reproduce numbers other people published for known bodies — Jupiter at
9.0 G, ε Eri b at 19 G — within a stated tolerance. Testing our output against our output
verifies nothing at all. This discipline is what surfaced the 54× table error.

### 4. Tables are generated, never hand-keyed

Any worked example in a methodology document is regenerated from the same code that
implements it, and the check fails on drift. A hand-typed table is a copy of a value, and
copies drift.

Lives in `engine/dynamo_table.py`, wired into `scripts/check.sh`.

### 5. Dependencies are declared in a file, not remembered

`engine/chain.yaml` records which derivation needs which, in four kinds: `requires` (a
numeric input), `selects` (chooses which model applies), `influences` (forces a recheck
without necessarily changing the value), and `excludes` (considered and rejected — worth
recording so it is not reconsidered from scratch). Cycles are allowed but must be declared
with a citation; an undeclared one fails the check.

`engine/chain.py affects <node>` then answers "what do I have to look at again", which is
the question that used to be answered from memory.

### 6. Shipped values flow back, so model that too

A dependency graph over methodologies is not enough, because this is a curation
repository: values are decided, written down, and then *reused*. `geopotential_j2 = 0.023`
is not a conclusion — it is an argument to a 21-hour moon integration whose result becomes
another recorded decision, and the stability report notes that the oblateness reverses
which moon orbit is chosen. Change the interior and that run re-opens.

So the layer records three more relations: which node should produce each shipped field,
which shipped fields are computed from other shipped fields, and what consumes them.
The Proxima failure is exactly the second kind, and a methodology-only graph cannot see it.

Lives in `engine/bindings.yaml` and `engine/backflow.py`.

### 7. A vocabulary is only real if something rejects what is not in it

Field names are checked against a single enumeration, and a name outside it fails. There
is exactly one such list, because two lists drift against each other. Widening the list is
itself checked: a spelling variant cannot be admitted to the menu, since that was how the
last duplicate survived four audits.

### 8. Prose explains; typed fields carry

Where a decision was recorded as prose, several quantities ended up bundled into one
string — one field packs a body's composition, mass, equilibrium temperature and cloud
class together, and no machine can take it apart. Values belong in typed fields, one
quantity each with its unit. Narrative stays as the settings-book text that explains them.

Existing approved narrative is not rewritten. The work is to lift the values out of it.

### 9. Derive physical state; let an adapter encode it

What the recipes produce is a body's physics, not a config file for whatever renders it.
An adapter turns the physical state into the target's fields.

```
recipes  →  physical state (target-agnostic)  →  adapter  →  KSP cfg
```

This is not tidiness. Sixteen `pause_*` parameters were being maintained by hand on the
boards, and they are not physics — they parametrise a shape function in the game engine.
The physics is one number, the magnetopause standoff. Sixteen hand-kept encodings of one
value is what produced the Proxima failure; the same shape repeats in the radiation-belt
shell fields. Recorded as physical state, the encodings are regenerated on every build and
cannot disagree with their source.

It also answers a question that otherwise has no floor: what stops the vocabulary growing
forever? Each layer is bounded for its own reason. The engine is bounded by physics — a
body's state is a finite list of quantities, and the admission test is *"is this a quantity
with a unit, or a declared dimensionless or categorical state?"* A description is not a
quantity. The adapter is bounded by a schema we do not own and that does not grow with our
ambition. Neither bound pushes on the other.

### 10. What a seat owes a claim

The nine disciplines above are what the machine owes a value. This one is what a person owes a
claim while relaying it — in a brief, a report, a note. Every line was written after it fired, and
of the fourteen errors on the day this section was compiled the gate caught zero: what got through
was never a wrong value, it was **a right value carrying a status it had not earned**. Each rule is
one line; the indented lines under a rule are the cases that were merged into it, kept for their
evidence, with the line they came from in `engine/SESSION-HANDOFF.md` at `2269a8d5`.

**없다 · 몇 개다 · 누구 탓이다 — 이 셋은 조회를 붙이지 않으면 말하지 않는다.** *Absent, how many, whose fault: none of the three is said without the query that produced it.*

**What a relayed number carries**

- **A number cannot enter without its label** — the quantity's name, its location, its condition, checked at that place in the source. Not "5500–6300 K" but "central temperature 5500–6300 K, Scheibe Table 1". Three seats, one disease.
  - ↳ *False provenance: a false label is worse than none, because the label stops the checking. Sender quotes only what is in quotation marks; receiver checks a number attributed to it against what it actually sent.* (line 276)
  - ↳ *A brief's number carries its condition AND a commit anchor; three of four errors in one day were right numbers wrongly paired, the fourth an inequality not pushed to its conclusion.* (line 280)
  - ↳ *The ± is part of the number, and so is the composition; a relay that keeps the digits and drops either has not relayed the number, worst in summaries.* (line 304)
  - ↳ *Inside a declared window, say which edge the number is measured from; prefer the curve the code evaluates.* (line 315)
  - ↳ *A number whose source was not stated is quoted without one; an invented source is harder to catch than a missing one.* (line 411)
- **Only the printed value travels.** Before carrying a number from one body to another, check whether it is what the source prints or something derived from it with the first body's own state — Earth's 3040 K is 4800 K over Earth's adiabat ratio, and Mars has its own.
- **A band is the opposite of a knob only when its width comes from the physics.** A width that is the interval over which our code happened not to fail is a numerical boundary, and carrying it ships the failure as a range.
- **Judgment-changing numbers are reproduced before they are reported on.** Downward, no unlabelled number in a brief; upward, a number that opens or closes a row, claims a match, moves an anchor or a grade is re-derived by the directing seat — and the audit's leg stays separate, three legs not one.
- **Numbers first, interpretation second, as separate messages.** Two seats then read the numbers independently; mixed together, the reading is not a check.

**A negative carries its instrument**

- **A narrow instrument's output is not a general fact.** State the instrument beside the finding, and if the finding is a negative, say what the instrument cannot see — a title scan found no viscosity source where full text found five.
  - ↳ *"Not found" is a legitimate ending; say what was searched and how.* (line 345)
  - ↳ *A truncated view of a correct query is a wrong answer that looks right: `head`, `tail`, `cut` clip silently, so re-run unfiltered or make the truncation visible before reporting a negative or a count.* (line 403)

**Pre-registration**

- **Pre-register outcomes before running, and register the kind of unregistered result afterwards** so the classification learns. Five branches are standard for a retrial, including "the source does not reach the deciding region" and "the source disagrees with both candidates".
  - ↳ *A discriminating test states the assumption beside each prediction, and registers "all predictions miss" as the test itself failing, its product being the name of the wrong assumption.* (line 333)
- **Do not tune a declaration until the answer comes out right.** Declare, integrate, report; three items in a row declined to write the value that would have closed their gap, once by 0.0012.
- **A check whose own error exceeds its criterion cannot raise a grade** — and its mirror: a check can be precise while the thing it checks is simply wrong.
- **A check must prove it can pass and can fail before its result is written down.** A check that always fires is a constant; this holds for a test, for a scratch script whose numbers get reported, and for a shell one-liner.
  - ↳ *Three checks read correctly and were wrong when run — `pgrep -x python3`, `pgrep -P`, `git diff --quiet` — and two healthy gates died of the first; point a check at the case you expect to pass, not only the one you expect to fail.* (line 1447)
- **Read what the brief names before building it** — existing code, a declared limit, the paper's own sentence, our own rule. Seven of seven times in one day, reading changed the build.

**Two operating rules**, in no cluster, kept because they are written nowhere else

- **No new runtime dependency in `engine/`**; `check.sh` runs on system Python.
- **Clear the work session's context at item boundaries**, after confirming the notes carry what the next session needs, especially the approaches tried and rejected. The owner types `/clear`; a session cannot clear itself.

**See also** — rules that already live elsewhere, one pointer each, with the cases merged under them

- Anchors bit-identical, a moved number reported with its cause, `--refresh` in the same commit → enforced by `engine/test_ice_giant.py@«--refresh»`; the principle is §3 above.
- Gate FAIL 0 → `CLAUDE.md@«8. Run Tests Before Marking Complete»`, widened to: say what your work adds to the gate's time.
  - ↳ *A runtime estimate belongs to the commit it was measured on.* (line 373)
  - ↳ *`check.sh` is ~20 minutes and the foreground tool limit is 10; run it backgrounded and watch the tail. An external signal's sender candidates include the harness itself.* (line 430)
- Papers through `ADS_API_TOKEN` and the cache, no WebSearch, identifiers read and checked by title → `CONVENTIONS.md@«3.2 ADS paper discipline»`, `CONVENTIONS.md@«3.3 Paper references are links»`.
  - ↳ *A cache file is held only once shown to be a PDF — run `file` on it; a `.PROVENANCE.txt` records how it was obtained but its absence is not the check.* (line 349)
  - ↳ *Check ADS `esources` before asking the owner for a paper; three of seven requests had a free route in a field already queried.* (line 398)
- Commits in English, one logical change, fixed identity → `CONVENTIONS.md@«1.8 Git commit language»`, `CONVENTIONS.md@«1.9 Git identity»`, `CLAUDE.md@«9. Semantic Commits»`.
- A commit that closes a hole brings the test that reproduces it → `CLAUDE.md@«4. Goal-Driven Execution»`.
- A process listing is an instant, not a state; a session about to relaunch checks for itself → `engine/tools/README.md@«Telling a busy gate from a dead one»`, `engine/tools/README.md@«A gate is a process group»`.
- A sentinel carried in a variable something else re-arms is not a contract → `engine/interior-core.md@«A sentinel carried in a variable something else re-arms is not a contract»`.
- The cold flank's second form: the steering must be able to conclude → `engine/interior-core.md@«the climb hid the wall from the controller»`.
- A third party checks a solver by closure, not by A/B → `engine/interior-core.md@«A third party checks a solver by closure»`.
- An unreachable boundary condition closes as a named refusal → §2 above.
  - ↳ *Bake a source only after sweeping its claimed range against pre-registered physicality criteria, and record the effective ceiling with the table; the printed validity range is not the executed one.* (line 328)
- A new number is carried back to the old ones before it is used to clear them → §5 and §6 above (`chain.py affects`, backflow).
  - ↳ *Prose that carries a number carries the duty to update it; so does prose carrying a condition, and a row carrying a prediction.* (line 326)
- Tables and extractions → §4 above.
  - ↳ *A regenerated table that differs is settled by a separate trace; do not correct the table to the code or the code to the table on the name alone.* (line 331)
  - ↳ *When machine-extracting a numeric table, check against a different rendering, not against check values that rode the same extraction.* (line 427)
- Stage what you wrote, not what the file holds: `git diff --stat` before `git add` in a shared worktree → `engine/tools/README.md@«reading `git diff --stat`»` (the rule's other home is the owner's session memory, outside the repo).
- Do not widen the detector; write the data in the shape it already reads → §7 above; `engine/tools/README.md@«Four times the answer was to reshape the input»`.
- A count is only as true as the sentence under it → `engine/tools/README.md@«Counts and quotations are both only as true as the sentence over them»`.
- When you re-aim an anchor, re-read the sentence around it → `engine/tools/README.md@«Re-aiming an anchor is not the whole repair»`.
- The name was the evidence, and the name was wrong → `engine/tools/README.md@«Four names that read correctly and were wrong when checked»`.

---

## What this does not fix

These rules make errors *detectable*. They do not make the derivations right, and they add
real cost: every new value needs a binding, a citation, and usually a test.

One of the two structural gaps closed on 2026-08-25: interior structure is now derived
rather than assumed. The layer densities that four recipes each used to assume privately
are outputs of an integration, and the two lookup tables that stood in for them are gone.
What the solver cannot do it now **declines by naming the mechanism**, which is the part
that makes the remaining gaps actionable: three of the Alpha Centauri moons come back
"needs the equation of state for ices III, V and VI", not "too low density".

The other gap is still open. Nineteen shipped fields have no node that produces them at
all, mostly stellar appearance and activity, plus two (`color`, `ring_color`) that have
methodology documents but no entry in the graph.

## Related

- `engine/chain.yaml`, `engine/bindings.yaml` — the two declarations
- [Methodology index](methodology-index.md) — the recipes themselves
- [Tools](tools.md) — what to run
