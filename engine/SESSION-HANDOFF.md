<!-- 지휘 세션이 교대할 때 넘기는 문서 — 현재 상태·대기 작업·규율 -->
# Session handoff — the directing seat

Written 2026-08-31, when the directing session's context filled and the owner cleared it.
Read this, then `engine/interior-core.md`, then take the seat.

## Where the work lives

**All of it is on `engine/prototype`, in a worktree.** As of this writing that is ~140 commits
ahead of `main`, and `main` is not ahead at all. A session sitting in the main checkout sees
the last work as tidal heating and the stability simulation, and is **not wrong** — that is
what `main` contains.

```
/Users/vana/Desktop/NearStars                      main
/Users/vana/Desktop/NearStars-wt/engine-prototype  engine/prototype   ← the work
/Users/vana/Desktop/NearStars-wt/site              gh-pages
```

The branch is pushed to `origin/engine/prototype`. **`main` has not been merged and no PR was
opened** — that is the owner's call, deliberately not taken.

**Do not write in the work worktree** unless you are the work session; it is in active serial
use. The git stash stack is shared across all three worktrees, so **never use bare
`git stash`** — a temporary WIP commit is the safe way to set work aside.

**And when you do write there, stage what you wrote, not what the file holds.** A
path-scoped `git add <file>` is not scoped enough in a shared worktree: on 2026-08-31 the
directing seat's C6 commit (`66fffaa7`) swept in the work session's uncommitted rule
paragraph for Brief 22, because both seats had edited `interior-core.md` at once. The
content was sound and landed in the right place, so nothing was rewritten — but the commit
message described one change and the commit contained two, which is a false label on a
commit. **Run `git diff --stat <file>` before staging it**, and if the diff contains someone
else's lines, either wait or name them in the message.

## The four seats

| seat | what it does |
|---|---|
| **directing** (this one) | writes briefs, hands them to the work session, verifies what comes back, reports each completed item to the audit session, relays the audit's feedback. **Does not implement.** |
| **main work** | implements one item at a time, serially. Owns the worktree while working. |
| **parallel** | literature only — "does this paper carry a transcribable X?" Never writes to the repository, because it shares the worktree. |
| **audit** | evaluates each completed item independently. Never implements, so it never audits its own work. |

Session names change on restart. Use `ListAgents` and confirm each one's cwd, branch and
current task rather than assuming. As of the handoff: `nearstars-db` works, `nearstars-74`
surveys, `nearstars-1e` audits.

**Verification runs in every direction.** During the last two days the work session caught the
directing session's briefs five times, the directing session caught the audit's ledger and a
misread pair of numbers, and the audit caught everyone. A number handed down, up or sideways
is not thereby verified.

## Where things stand — rewritten 2026-09-01, the core list is closed

**`engine/interior-core.md` is still the one place that says what remains.** Read it before
acting. What changed since the last handoff is that **it no longer has an open row.**

- **C1–C13 all closed.** C6 stays a standing watch — material ceilings need nothing unless a
  body the roster wants is refused by one. It fired twice today and both are recorded.
- **C13 closed 2026-09-01 as a *named refusal*, which is the ending the audit proposed and the
  owner chose.** The deficit is real (−15.8 % / −11.4 % after radius is stripped) and three
  axes were measured, each stopping somewhere this recipe can point at. **Not claimed**: that a
  fuzzy core cannot account for it. **Claimed**: that this recipe cannot decide it, and why.
- **C11's open question was settled by declining it** — the grid is the answer and no declared
  pair is elected. Anything downstream needing one number declares its own and carries the
  label.

**The single most important thing a new seat should know about today's numbers:**

> **26 % / 41 % (C13's rock axis) and 39.7 % / 60.0 % (Brief 26's gradient span) were
> measurements of a table choice, not of the planet.** With the 66 repairable clamped `grad_ad`
> nodes assembled instead of read, both stop converging entirely. A number that exists on one
> grounded route and will not converge on the other was never robust to that choice. **Which
> route is nearer the truth is unknown** — the truth is in the original authors' unpublished
> calculation. Every affected number now carries that condition beside it.

**The default path is the published table** (owner, 2026-09-01) — not because it is judged
truer, but because there is no ground to elect either. `engine/hhe_repair.py` is an **opt-in
instrument**: nothing imports it, the baked table still carries its 72 clamped cells, and the
anchors were never refreshed. **Verify that before trusting a comparison.**

## What is running, and what the owner has decided

**Rewritten 2026-09-01 evening, end of day. Briefs 22–33 landed, every one gate-clean.**
All three seats are idle with nothing computing; the working tree is clean and no stash was
used. **Sample the process table yourself rather than trusting this sentence** — a listing is
an instant, not a state, and this seat has already caused one duplicate heavy run by
reporting from a single `ps`.

**The adopted set as it actually resolved** — the order in the last handoff (AQUA → Queyroux →
carbon) survived, but **two of the three did not end as adoptions**:

- **AQUA — not built.** Zero reachable cells. See the parked-decisions section.
- **Queyroux — landed, but not as the briefed election.** The owner rejected both "choose a
  side" and a three-way mean, and took the **mean of two measurements below the kink**. The
  brief's own framing ("choosing a side in a live debate") turned out to apply only *above*
  14.6 GPa. Full terms and the three label conditions are in the parked-decisions section.
- **Carbon's fluid axis — half its rationale was retracted by the surveyor who wrote it.**
  Do **not** brief it from the last handoff's sentence, which said Militzer 2024 has "a
  quantity theory". It does not; those numbers are fitted model parameters. And the same
  sentence's claim that **"our column does not have ammonia" is wrong** — `engine/ammonia_table.py`
  carries it from C4. What we lack is methane (C4 closed that half as unbuilt because methane
  dissociates) and the hydrogen-poor C–N–H polymer species the separation produces. It now
  needs an owner scope decision before a brief.

**Two findings arrived after the core list closed, both about `ice_x`, and neither is briefed:**

- **The superionic gate asserts something false and passes.** `test_interior.py:220`'s
  `MILLOT_SUPERIONIC = (100.0e9, 2000.0)` treats the superionic floor as **flat**, and the
  gate checks `ICE_VII_X_T_MAX (1800 K) < 2000 K`. The real boundary rises to a maximum near
  200 GPa and then **descends through 1800 K somewhere in 305–375 GPa** (two independent
  figure renderings; the maximum agrees to 0.7 % in T and 5 % in P, the crossing disagrees by
  29 GPa and **was not adjudicated**). So the promise in `eos.py:1929-1934` — that superionic
  ice will not be quietly called ice X — is reachable. **No current answer is wrong**: both
  ice giants' mantles bottom out at 2553 K. **Whether a cold *trial* path enters is unmeasured,
  and that is what separates a labelling defect from a convergence defect.**
- **And the attribution on those constants is false.** Millot+ 2019's "exceeding 100 GPa …
  above 2,000 kelvin" is that paper restating **refs 6–12's prediction** — verified verbatim
  in the cached PDF by this seat — not its own result. The constants carry a Millot label on
  someone else's number. Separately, `eos.py`'s `SUPERIONIC_MIN_T`/`_P` are **defined and never
  read**; the live copy is the test's, unlinked to them.
- **`ice_x` now has three different ceilings**, and the code uses the largest: **data ≈355 GPa**
  (above it, extrapolation — C6), **stability ≈520 GPa** (where the ice region closes in the
  very potential `ice_x` is fitted to), **printed 1000 GPa** (the knot box, and what
  `ICE_X_P_MAX` says). This is C6's subject and belongs in its row.

**Brief 34 is the repair** and is designed but unwritten: measure whether trials enter the
false region · replace the flat inequality with a (P, T)-dependent check · fix the attribution
and remove the unlinked duplicate · record the three ceilings as one notation.

## Standing rules — each exists because something got through

- **Anchors bit-identical.** If a solved number moves, it is reported with its cause, never
  absorbed. `test_ice_giant.py --refresh` goes in the same commit whenever a path-fingerprint
  function or its constants change.
- **Gate FAIL 0**, and say what your work adds to its time.
- **A number cannot enter without its label** — the quantity's name, its location, its
  condition, checked at that place in the source. Not "5500–6300 K" but "central temperature
  5500–6300 K, Scheibe Table 1". **This disease is independent of role**: it fired once in each
  of the three seats.
- **False provenance** (subspecies 7): a number carrying a label that is *false* is worse than
  one carrying none, because the label stops the checking. Sender: quote only what is in
  quotation marks; if you filled a number in, say you filled it in. **Receiver: a number
  attributed to you is checked against what you actually sent before you accept it.**
- **Verification without relay, both ways**: downward, no unlabelled numbers in briefs; upward,
  **judgment-changing numbers are reproduced by the directing seat before being reported on**.
  Triggers: (a) a number that changes a row's open/closed/reopened state, (b) a claim that a
  published value is matched or reproduced, (c) a number that moves an anchor, (d) a number
  that changes a grade. **The directing seat's reproduction does not replace the audit's** —
  the point is three legs, not a relocated one.
- **Prose that carries a number carries the duty to update it.** So does prose carrying a
  condition, and a row carrying a prediction carries the duty to correct it.
- **Bake a source only after sweeping its claimed range against pre-registered physicality
  criteria, and record the effective ceiling with the table.** SeaFreeze's `water2` returns
  negative density inside its own knot box; the printed validity range is not the executed one.
- **A regenerated table that differs**: which side is right is settled by a separate trace.
  Do not correct the table to the code, or the code to the table, on the name alone.
- **A discriminating test states the assumption beside each prediction**, and registers "all
  predictions miss = the test itself failed, and the product is the name of the wrong
  assumption" as an ending.
- **A check whose own error exceeds its criterion cannot raise a grade** — and its mirror: a
  check can be precise while the thing being checked is simply wrong.
- **Do not tune a declaration until the answer comes out right.** Declare, integrate, report.
  Three items in a row declined to write the value that would have closed their gap, once by
  0.0012.
- **Pre-register outcomes before running**, and register the *kind* of unregistered result
  afterwards so the classification learns. Five branches are now standard for any retrial,
  including "the source does not reach the deciding region" and "the source disagrees with both
  candidates".
- **"Not found" is a legitimate ending.** Say what was searched and how.
- Papers through `ADS_API_TOKEN` and the `docs/phase3/_papers/` cache (gitignored). **No
  WebSearch.** Identifiers read, not made, checked **by title**; where one file cites two
  papers, the label carries the paper's name.
- No new runtime dependency in `engine/` — `check.sh` runs on system Python.
- Commits in English, one logical change each, identity `VaNnadin <vannadin00@gmail.com>`.
- **Clear the work session's context at item boundaries** (`/clear`, which the owner types —
  a session cannot clear itself), after confirming the notes carry what the next session needs,
  especially the approaches that were tried and rejected.

## What 2026-09-01 added to the rules — read these, they are new

Every one is in `interior-core.md`'s rules section with its case. The short forms:

- **A process listing is an instant, not a state**, and a serial chain shows nothing between
  its steps. This seat reported "the run never started" from one `ps` and caused a duplicate
  heavy run. Report process state with its sampling; **a session about to relaunch checks for
  itself**, whatever the report says.
- **A runtime estimate belongs to the commit it was measured on.** "~15 minutes" was honest
  when taken and false when quoted, because the code had changed between.
- **A number whose source was not stated is quoted without one** — do not supply the
  provenance. An invented source is harder to catch than a missing one, because a reader who
  sees one stops looking.
- **A sentinel carried in a variable something else re-arms is not a contract.** State that
  encodes a promise gets its own variable.
- **The cold flank has a second form: the climb hid the wall from the controller.** Brief 22
  taught trial refusals to steer the bracket; this says the steering must also be able to
  **conclude**, or the loop cycles instead of refusing by name.
- **A third party checks a solver by closure, not by A/B against a harness whose brackets it
  does not own.** The audit's own instrument was wrong twice and it judged the instrument, not
  the solver.
- **An unreachable boundary condition closes as a named refusal**, not as a failure to
  converge. That is what let C13 close.
- **A new number is carried back to the old ones before it is used to clear them.**
- **Stage what you wrote, not what the file holds** — `git diff --stat` before `git add`, in a
  worktree two seats are editing.
- **When machine-extracting a numeric table, check against a different rendering**, not
  against check values that rode the same extraction — they can be self-consistently wrong.
  The IF97 PDF's text layer dropped every power of ten.
- **`check.sh` is ~20 minutes and the foreground tool limit is 10.** Run it backgrounded and
  watch the log tail; twice it was killed and read as an owner signal. **An external signal's
  sender candidates include the harness itself.**

## Traps worth knowing before you step on them

- **Do not fix the band at 2.3–5 GPa / 500–1000 K by special-casing.** It is closed now
  (`water2`), but the pattern recurs: when a path dies in a gap, the fix belongs in the gap's
  equation of state, not in a detour.
- **`~/Downloads` may be unreadable** by directory listing (a macOS privacy grant that reset)
  — **the directing seat's grant only**; the work session read and copied named paths there
  without trouble. Named paths still read. Ask the owner for the exact filename, or have them move the file into
  the paper cache.
- **The owner's doubt has twice been right** where a session's report was wrong — once about a
  paper's tables, once about a plan's shape. Take it seriously rather than defending the
  report.
- **Open the rendered document** when the owner asks to see one: `./scripts/preview-md.sh <file>`
  then `open`. Do it unasked for anything newly written.

## Owner decisions still parked

**Rewritten 2026-09-01 evening. Four rows that stood here were already resolved and were
sitting stale** — ⑥ was listed as awaiting a decision after it had been transcribed and
landed, and a session reading this list would have re-asked a closed question. That is the
list's own rule (*prose that carries a number carries the duty to update it*) applied to
prose that carries an open/closed state. **Check a parked row against `git log` before
acting on it.**

**Resolved since the last rewrite — do not re-open these:**

- **② Queyroux's melting curve — landed, and not as either election.** The owner rejected
  both the lineage choice and a three-way mean, and chose the **unweighted mean of Queyroux+
  2020 and Prakapenka+ 2021 over 2.17–14.6 GPa** (Brief 33, `0e8dcc02`). Below the kink both
  lineages agree, so there is no side to take; above 14.6 GPa the dispatch is unchanged and
  the stretch where candidates disagree refuses by name. Our own curve was **excluded from
  the mean** because a three-way mean let the curve under review vote on its own trial — it
  landed 111–120 K *below* both real measurements at 20 GPa. Anchors bit-identical, gate
  FAIL 0. Label conditions live beside the constants: the two papers **share Datchi's
  triple-point anchor** (2.17 GPa · 354.8 K, identical to three figures in both), so the
  1.0 K agreement at 8.2 GPa is **not** independent confirmation — the independent number is
  8.7 K at 20.0 GPa; averaging does **not** shrink the uncertainty (carry the ≤54 K
  separation, never σ/√2); below 8.4 GPa is anchored interpolation, not measurement support.
- **⑥ IF97 steam — transcribed and landed** (Brief 25, `544d8730`, `bb1d3779`). It retired
  the water wall, and **the wall moved rather than cleared**: the ice axis now stops at
  h_he's low-temperature floor (`01271699`). So **③ is stopped again, by a different wall**,
  and is not an adoption candidate today.
- **AQUA — closed as *not built*** (Brief 32, `b5c9cb97`). The full pipeline ran and the
  exhaustive question came back zero: **no baked fluid cell below 1000 K that steam/water1/
  water2 do not already own.** The target corner was already-served territory plus AQUA's own
  region-5/6/7 seam, which is where our named refusal lives and where AQUA's numbers are the
  unphysical ones. A fallback with no reachable state is a machine without a consumer (C5).
  Generator, cached grid and PROVENANCE kept; the baked module was not committed.
- **C11's declared pair — closed by declining to elect one** (`8bd564fe`). The grid is the
  answer; anything downstream needing one number declares its own and carries the label.
- **Ternary EOS grid — closed as *recorded, not found*** (`d8907784`).
- **Millot+ 2019's Fig. 4 — read** (surveys ⑩/⑩b, 2026-09-01), and it did not say what the
  constants claimed. See the next section; the repair is Brief 34, not a decision.

**Still open:**

- **Where the tidal-heating → interior axis goes in the queue.** It is now adoptable and
  **cheaper than the first reading**: Ė(T) is needed to *predict* an equilibrium, not to
  evaluate the conversion at a given heating rate, which is what Kankanamge §6 does for Io
  (1471 K internal, 12.6 km lithosphere, consistent with Galileo eruptive temperatures) —
  and our Ė is likewise a computed input. Multiplicity is one stable point, with an unstable
  one only in the Maxwell-plus-convection pairing. **This is the one decision that unblocks
  the queue.** The directing seat recommends it next.
- **Carbon's fluid axis — a scope decision, and half its rationale was retracted.** Survey ⑨
  found that the composition numbers this axis was adopted for are **fitted interior-model
  parameters, not chemistry outputs** — the first-principles part establishes that separation
  happens and that hydrogen depletion grows with pressure, and leaves the quantity free. So
  the fluid/diamond contrast narrows: **both need declared quantities.** For Uranus and
  Neptune it is buildable (their values are printed); as a *general* axis it needs **four
  declarations per body** (two layer compositions, two boundary radii) with **two** published
  examples. That is the shape that closed hot sub-Neptunes — **but not the same case**: what
  closed those was a parameter with *no* published value at all. Here there are two worked
  examples, a printed stability inequality (H₃ < H₂), an exact endpoint (undepleted CH₄–NH₃
  gives H = 1 by the printed definition), and a printed interpolation form. The recipe
  declares things routinely; the rule is *say that you declared*. **The genuine limit is that
  this axis has no independent validation anywhere** — J₂/J₄ were the fit targets, not a
  prediction test, which is exactly the threshold the tidal axis cleared via Io. So its
  output is *structure consistent with the physics*, not *structure constrained by data*, and
  must say so. Directing seat recommends adopting it as a **declared family with a grid**,
  never one elected quadruple.
- **Zenodo download permission.** Carbon's layer equations of state are **distributed as
  deposited data, not printed** (records named in survey ⑨; nothing was downloaded — the
  record IDs are the product). This is the AQUA/CDS shape, which we accept, but fetching from
  a new host is the owner's call.
- **Merging `engine/prototype` into `main`**, and whether to open a PR. Still deferred, and
  the cost of deferring is now visible: a session in the main checkout sees the last work as
  tidal heating and the stability simulation and is not wrong.
- **Dante · Hades radii** — board work, so it sits behind the engine by the standing
  tool-before-boards rule.
- **Paper requests**: the ternary grid closed as not found. **French, Desjarlais & Redmer
  2016** (PRE 93, 022140, `2016PhRvE..93b2140F`) was **obtained by the owner 2026-09-01** and
  is cached with PROVENANCE; it prints **no** boundary equation or table, which is recorded as
  a legitimate *not found*. Nothing is outstanding.
