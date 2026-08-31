<!-- 지휘 세션이 교대할 때 넘기는 문서 — 현재 상태·대기 작업·규율 -->
# Session handoff — the directing seat

Written 2026-08-31, when the directing session's context filled and the owner cleared it.
Read this, then `engine/interior-core.md`, then take the seat.

## Where the work lives

**All of it is on `engine/prototype`, in a worktree.** As of this writing that is ~105 commits
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

## Where things stand

**`engine/interior-core.md` is the one place that says what remains.** Read it before acting.

- **C1–C12 closed.** C6 is a standing watch — material ceilings need nothing unless a body the
  roster wants is refused by one.
- **C13 open.** The ice-giant moment of inertia sits 11–16 % below publication after radius is
  removed. The rock-redistribution axis was measured and **covers only 26 % (Uranus) / 41 %
  (Neptune)** of that gap, so it cannot close it. The ice axis is untested. *Three legs, all
  landed (`19360f72`)*: the audit found the float residual, the previous directing seat
  pre-registered and ran the ε ladder, and the work session reproduced every digit and
  retired both caveats — Neptune's P_c 984 GPa is not wall-adjacent (a probe at 1010 GPa
  integrates, mass closure 1.000000) and the grid 1500 → 6000 drift is 3.7–3.9e-4.
- **Follow-ups F1–F5, water2, the C/MR² check and the Queyroux flip experiment are all closed**
  and all audited.

## What the owner approved, in this order

**① The cold-flank general fix.** The refusal machinery exists to make answers honest, but the
shooting and temperature loops put *trial* solutions through the same refusals — so a solve can
die in a state no converged answer would ever occupy. **Three occurrences in two days** is how
the committed diagnosis counts it (`f3f3a3fd`): C11's over-broad refusal, the Queyroux
experiment's Neptune path death, and C13's end B — whose sharpest form is a **1 ULP**
difference in `ice_mass_fraction` deciding between a 1-second refusal and a 112-second
convergence (the same event, not a fourth). Counting C1's false ceiling — its ladder seed and
F2's bulk-modulus finite difference are literally trial paths hitting evidence the answer does
not use — makes it four; say which basis you are using, because the two documents differ.
The proposed shape is to route trial-path refusals into steering the bracket rather than
killing the solve.

**This unblocks ② and ③.** C13 cannot close properly without it, and the Queyroux adoption
needs it too.

**② Adopt Queyroux's melting curve, or not.** The cost table is complete: **no physics verdict
flips in the current roster**, and the cost is three pieces of work — trial-path hardening
(that is ①), a window-edge splice rule (+69 K at 8.4 GPa, −239 K at 44.7 GPa against
Reinhardt), and F4's grade wording. Our curve is 210–300 K colder than the only measurement in
16–20 GPa.

**③ Measure the ice axis.** Same method as the rock axis. Do it **after ①**, otherwise it will
be measured through the phantom-stub device again rather than properly.

**④ Three surveys, dispatched to the parallel session on 2026-08-31**, in this order: AQUA
(water's ceiling — most likely to pay), the radiative–convective boundary (opens hot
sub-Neptunes, which the recipe barely answers today), and a third melting-curve candidate.
Reports will arrive addressed to the directing seat.

## Where Brief 25 stands — 2026-08-31, ~20:00 KST

*This section replaces one written minutes earlier that said the work was uncommitted on
disk. It was already landing as `544d8730` while that was being written — a stale number
committed by the directing seat, in the same hour as the rule about stale numbers. Left
visible rather than quietly overwritten.*

**Brief 25 (bake IAPWS-95/IF97 steam) is landed but its acceptance is not run.** The owner
paused compute (fan/throttle; one run was externally killed), so the four ice-axis ends and
the full `check.sh` are deferred. `544d8730` carries the code:

- **IF97 regions 1, 2 and 3** transcribed into `engine/steam_if97.py` — pure Python closed
  form, **no new runtime dependency**. Verified against the standard's own printed check
  values (Tables 5, 15, 33, 35, the B23 point, a density round trip): **worst 3.2e-9**, and
  the gate re-runs it.
- **The coefficient tables were read from the typeset images, not the text layer** — the
  archived PDF's text layer drops every power of ten, so transcribing it would have been
  silent fabrication. That is the right call and it is why this took as long as it did.
- **Region 3 was needed too**: with regions 1 and 2 alone the ends still refused, and the
  refusal spy (1202 → 138) put every remaining water-side death on the **B23 edge of the
  region 3 triangle** (18–97 MPa × 635–661 K, measured).
- **A finding about our own table**: at 1000 K and low pressure, Mazevet is off by
  **+88 … +994 %** — its ρ ≳ 1 g/cc validity condition confirmed numerically — so the
  envelope dispatch now puts IF97 **in front of** Mazevet. Physicality sweep: zero
  violations. Seams: water1 0.005 %, water2 ≤ 0.02 %.
- Anchor bit-identical; `--refresh` in the same commit (fingerprint 425c011016a248cf →
  **be375eaec98efb01**, diff is fingerprint and seconds only, a solve-note string moved it).

**Resume point, from that session's own checklist**: ① run the four ice-axis ends
(`scratchpad/ice_axis_runs.py`) through the full r1·2·3 dispatch — convergence unknown, and
**gap-covered % only becomes quotable if `conv=True` appears**; ② the full `check.sh`. If no
end converges, **the next wall's coordinates are the product**, not a failure.

**Carry the label steam does not buy**: that window sits outside Soubiran & Militzer's
validated mixing band on both axes, so passing the wall happens over an unverified mixture
(`7769be6e`).

**Its landing chain, if a session's context has holes** (the owner reports some sessions lost
records to a re-login): `84b93530` Brief 24 → `ac8146c5` label correction → `544d8730` this.
Each checklist and note carries the prior state, so re-anchor from those files.

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

The four approved items are worked through: **① the cold-flank general fix landed**
(2026-08-31, Brief 22, three legs), **③ the ice axis was attempted and could not be
measured** (Brief 23 — the axis is expressible, no bracket end converges, and the reason is
named below), and **④ all three surveys landed**
(`engine/surveys-2026-08-31-context-notes.md`). **② is the one still open of the four**, and
it now has the paper it was waiting for.

- **② Adopt Queyroux's melting curve, or not — reframed, and unblocked.** Survey ③ found
  the 100–150 K disagreement already settled by Queyroux themselves; what is live is the
  curve's *shape* (continuous vs discontinuous melting, still argued in 2025), so adopting
  them is **choosing a side**, not repairing an error. Brief 22 removed one of the three
  cost items. **Prakapenka+ 2021 is now cached and has not been read against our curve or
  Queyroux's** — that comparison is the work this decision waits on, and it needs to be
  dispatched before the decision is taken.
- **⑥ Bake IAPWS-95/IF97 steam?** New, 2026-08-31, and it is **③'s precondition**: every
  ice-axis bracket end dies at one wall (p ≲ 0.1 GPa × 500–1000 K, the junction of water1's
  500 K ceiling, water2's 0.1 GPa floor and Mazevet's 1000 K floor — 1102 of 1202 refusals),
  and the published filler covers exactly that window. Bringing in a new source is the
  owner's call. **Its cost includes one thing steam does not buy**: the wall sits outside
  Soubiran & Militzer's validated mixing band (2–70 GPa × 1000–6000 K) on both axes, so
  filling it gives a water equation of state there and leaves the *mixture* ungrounded —
  the same shape as C6's ladder, a table standing where the data is not.
- **Adopt AQUA?** Not urgent, and the gain is now named twice over: the high-pressure
  300–1000 K corner is not merely untabulated, it is where our own ladder stops being data
  (C6). Cost is a 13.6 MB dependency and an interpolation seam inside our range.
- **Merging `engine/prototype` into `main`**, and whether to open a PR.
- **Which declared pair C11 should actually use** — the row gives the grid and does not choose.
- **Carbon as a separate phase.** Uranus's and Neptune's mantles cross every published
  dissociation threshold; that was measured and not judged. Opening it is a scope decision.
- **Paper requests**: only one is still open — the ternary EOS grid (author request only,
  Bethkenhagen's group at Rostock). The other two arrived 2026-08-31. **Millot+ 2019** is
  cached (`2019Natur.569..251M.pdf`) and the figure the notes named was the wrong one — the
  phase diagram is **Fig. 4**, not Fig. 3 — so the superionic constants are still
  abstract-sourced until someone reads Fig. 4 against them. **Prakapenka+ 2021** is cached
  (`2021NatPh..17.1233P.pdf`, the GFZ Potsdam repository's open-access author copy, found
  through Unpaywall after the publisher paywall held) and it is the paper decision ②
  should not be taken without.
