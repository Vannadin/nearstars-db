<!-- 지휘 세션이 교대할 때 넘기는 문서 — 현재 상태·대기 작업·규율 -->
# Session handoff — the directing seat

Written 2026-08-31, when the directing session's context filled and the owner cleared it.
Read this, then `engine/interior-core.md`, then take the seat.

## Where the work lives

**All of it is on `engine/prototype`, in a worktree.** Measured 2026-09-03 it is **230 commits
ahead of `main`, and `main` is not ahead at all** (`git rev-list --left-right --count
engine/prototype...main` → `230 0`). The "~140" that stood here was written on 2026-08-31 and
was never updated — **remeasure this line rather than quoting it.** A session sitting in the main checkout sees
the last work as tidal heating and the stability simulation, and is **not wrong** — that is
what `main` contains.

```
/Users/vana/Desktop/NearStars                      main
/Users/vana/Desktop/NearStars-wt/engine-prototype  engine/prototype   ← the work
/Users/vana/Desktop/NearStars-wt/site              gh-pages
```

The branch **is** pushed to `origin/engine/prototype`, as of 2026-09-03. **That sentence was
false when it was first written and stayed false for four days**: 124 commits existed only in
this worktree, with no backup anywhere, until the owner authorised a push on 2026-09-03
(fast-forward `7c84f2d4..f7271b1f`, verified against origin by two seats). **`main` has not been
merged and no PR was opened** — that is the owner's call, still deliberately not taken.
**Check the push state, do not read it here** — this line has been wrong once already.

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

**The paper cache is one directory, reached from every worktree by symlink.** `docs/phase3/_papers`
is gitignored, so each checkout used to grow its own copy: on 2026-09-03 the main checkout held
1399 files and the engine worktree 193, **189 of them — every paper the owner obtained that week —
existing nowhere else**, and a "cached" sweep run against the wrong copy reported 18 false claims
that were true in the other. The 189 were copied into main (`cp -Rn`, 0 collisions), the four
same-name files that differed were diffed on every value our files quote (all present in both; the
renders differ only in formatting), and the worktree directory was replaced by a symlink to
`/Users/vana/Desktop/NearStars/docs/phase3/_papers` (the ignore rule lost its trailing slash so the
symlink is ignored too). Two consequences: **`git clean -xdf` in a worktree removes the symlink**
(the target survives) and it must be re-created — `ln -s /Users/vana/Desktop/NearStars/docs/phase3/_papers
docs/phase3/_papers`; and until every worktree carries the link, **a "cached" claim is resolved against
the union of both directories**, never one. The owner decided **option ① only** — the symlink, no move
outside the repo — because the path is baked into five scripts, the SPEC and every methodology doc, and the
link buys the same thing for nothing.

**The merge fixed the files and nobody re-swept the claims — done 2026-09-03 by Brief 64.** Every
"not held / not cached / NOT HELD" written while the two caches were split was a check against one copy,
and the paragraph above already said the wrong-copy sweep had produced 18 false claims that were true in
the other. The follow-up — re-checking each claim against the merged cache — was the unfinished half. The
parallel seat's re-sweep found 25; the ones that were false are corrected in place, each with when it was
written and when the paper arrived, so the reader can see it was true at the time (most were) or never was.
**A negative about the cache is dated, and dated negatives are re-checked when the cache changes.**
**Gate on `959d8d78` (Brief 64, four docs-only commits): FAIL 0, 456 PASS, 17:37:07 → 17:58:15 = 1268 s**
(start/end stamps written by the launcher; Brief 60's run was 1265 s, so Brief 64 added nothing). ⚠ **The
first run of this gate was killed at 382 PASS / FAIL 0 by the launching tool, not by a failure**: a
backgrounded tool call carries a 10-minute ceiling and the gate takes ~20; the process vanished at ~17:32
with no end stamp. **Launch the gate under `nohup … &` (detached from the tool), stamp start and end in the
log, and read a run that died without an end stamp as *interrupted*, never as *failed*** — the same lesson
as the earlier "killed and read as an owner signal", from the other direction.
⚠ **The same misreading happened twice in three days, in two seats, with this warning already written
(2026-09-04)**: the directing seat once read a dead PID plus a mid-log "모두 통과" as "the gate finished"; the
main seat then read a test file's "모두 통과" (sixteen test files print exactly that line) as the gate's end,
committed three times into the tree while the gate ran, and launched a second gate on top of it — that run
(gate76) was killed and stamped *void*. Twice with the rule in place means a log-design fault, not a
person: the body's pass phrase looked like the end line. **So the gate now prints its own `GATE START sha=
pid= at=` and `GATE END sha= pid= at= rc=` lines** (`scripts/check.sh`), which no test file can imitate.
**The verdict "the gate finished" rests on the `GATE END` line alone** — with its sha naming the tree it
ran on — never on any "통과" text in the body, and never on a PID being gone. A gate whose `GATE END` sha
differs from HEAD ran on an older tree.
⚠ **Checks chained before a commit must run under `set -o pipefail`** (2026-09-04 daytime): a launch chain
of the form `python3 check_via.py --gate | tail -1 && git commit …` committed a tree whose via check had
FAILED, and launched a gate on it — because a pipe returns the exit status of its *last* command, and
`tail` succeeds. The cause is not `tail`; `head`, `grep`, `sort` mask a failure the same way. Either
`set -o pipefail` at the top of the chain, or run the check bare and read its status, or let the gate be
the only judge. The gate on that tree was killed and stamped void; the commit was amended.
⚠ **The power stamps are two-point samples** (start and end); a low-power interval *inside* a gate is
invisible to them. On 2026-09-04 two gates ran 2546 s and 1561 s with `powermode 2` at both ends, every
seat idle and no throttle record, and 300 s were about to be filed as "unexplained" — the owner then said
the machine had been moved mid-gate and low-power mode ran for a while. Not implemented (owner: stability
over speed): a stamp that answers "did the state change during this interval" would close the hole.

**Three owner-obtained PDFs had no PROVENANCE and now do (Brief 64; the files live in the gitignored
cache, so this line is their record in the repository)**: `2020PhRvL.125s5501Q_SM` (Queyroux SM, 08-31
00:26), `2023JChPh.158m4504K` (Kimura & Murakami, 08-30 11:29) and `2013JChPh.138w4504B` (Bethkenhagen+,
08-30 11:29). Each arrival is established three ways — the pre-merge backup's birth time, the owner's
words at that minute (*"파일 받았으니 확인해봐"* 1dbb5b4f 08-30 11:28; *"받음."* 06f20d69 08-31 00:26), and a
byte-identical original still in `~/Downloads` — with `2010Sci...328..740K` as the control (birth 01:42:50,
*"이거밖에 못받음"* 1588ff47 09-03 01:42). ⚠ **The 11:35 `cp -Rn` re-stamped every copied file**, so
arrival times are no longer readable from the cache itself; the backup directory in the crashed session's
scratchpad is where they survive, and this is why a PROVENANCE is written at fetch time, not later.

**Data tables have sources too, and one is missing.** The baked equations of state (`engine/*_table.py`)
are regenerated by `engine/tools/make_*.py`, never at runtime; the audit of 2026-09-03 (Brief 50) checked
every generator's source on disk and found one gone: **`hhe_table.py`'s Chabrier `DirEOS2019.tar.gz`**
(12.0 MB, `perso.ens-lyon.fr/gilles.chabrier/DirEOS`) — the ice-giant envelope cannot be re-baked until it
is fetched again. The convention that was practised but unwritten is now in `engine/tools/README.md`: keep a
one-off download (with `PROVENANCE.txt`), record a command for a package or repository, pin a package's
version where it is named (SeaFreeze v1.1.0; venv rebuild `pip install SeaFreeze==1.1.0`), and treat an
archive from a personal academic page as the fragile case that must be kept. **`DirEOS2019.tar.gz` and `DirEOS2021.tar.gz` were fetched by the
owner on 2026-09-03 and are in the cache with provenance (Brief 51); the 2019 archive reproduces the
committed `hhe_table.py` byte for byte.** **Request list — closed 2026-09-03 (Brief 55), no open
item. Rows are kept, not deleted, so a resolved request is distinguishable from one never made:**
- OC06 `2006E&PSL.250..561O` — **obtained** by the owner 2026-09-03, cached with PROVENANCE.
- Gaidos, Conrad, Manga & Hernlund 2010 `2010ApJ...718..596G` — **obtained** (arXiv preprint,
  parallel seat, 2026-09-03), cached with PROVENANCE.
- Korenaga 2008 `2008RvGeo..46.2007K` — **obtained** by the owner 2026-09-03, cached with PROVENANCE.
- Jaupart, Labrosse & Mareschal 2007 `2007mady.book..253J` (Urey ratio) — **withdrawn**. The owner
  hit a paywall (2026-09-03), no circumvention attempted; the measurement then showed we do not need
  it: Korenaga 2008 quotes the whole of what our documents wanted (global heat flux 46 ± 3 TW,
  oceanic 32 ± 2, continental 14 ± 1, the revision entirely in the continental term), and for heat
  production Ruedas 2017 says the Jaupart & Mareschal 2014 / Jaupart+ 2015 tabulations "merely quote"
  Rybach 1985, whose decay energy and power run 5.1 % / 3.3 % high — a relay to a source we already
  supersede. ⚠ Lookalike: "Jaupart 2007" hits at least two works (Jaupart/Labrosse/Mareschal 2007
  and Labrosse & Jaupart 2007).
- The canonical tabulation of long-lived isotope heat production — **obtained**: Ruedas 2017
  `2017GGG....18.3530R` (arXiv preprint, parallel seat, 2026-09-03), cached with PROVENANCE.
- Karato & Wu 1993 `1993Sci...260..771K` — **withdrawn**. Paywall first (owner, 2026-09-03), no
  circumvention; then c4's sweep of all 92 cached PDFs: eleven cite it, six attach a value, and every
  fitted constant is cited *jointly* with a second source (Nimmo+ 2004's 250–350 kJ/mol with
  Yamazaki+ 2000; Monteux+ 2016's η_s,0 = 256 Pa·s, B = 25.17 with Abe 1997). What it carries alone
  is the functional form, reproduced identically by three papers. **One labelled exception**:
  Rovira-Navarro+ 2021's E_a = 300 kJ/mol rests on Karato & Wu alone — an *unchecked secondary
  citation*, corroborated at range level (inside Nimmo's independently quoted 250–350, which is
  both derivable from those energies via ζ = E/(RT²) → 0.00481–0.01644 against the printed
  0.005–0.016 *and* cited to Solomatov 1995) but not at point level — and shown insensitive across
  ±100 kJ/mol by Foley & Smye 2018, who adopt the same 300 from Karato & Wu alone and run 200/400 as
  sensitivity cases consistent with their baseline (Brief 59). Labelled at `rheology.py@«# "Mantle solidus viscosity" 1·10¹⁶ Pa·s and "Activation energy" 300 kJ/mol, footnote 4 =»`
  and `viscosity-context-notes.md` §1. ⚠ Lookalike: Gaidos+ 2010's b ≈ 17 is cited to **Karato,
  Riedel & Yuen 2001**, not Karato & Wu 1993 — grepping "Karato" for a viscosity constant grabs the
  wrong paper.

**Do not commit into the shared worktree while another seat's gate is running.** The gate
certifies a tree state; a commit landing mid-run rides the push without review and makes the
FAIL count a statement about a tree that no longer exists. Docs-only is harmless and the habit is
not. *(2026-09-03: the directing seat's handoff edit landed at 04:19 inside a 04:18–04:38 gate and
was pushed unreviewed — and `git diff --stat` before staging was skipped on that same commit, the
last of a long night. The work seat flagged the extra commit rather than folding it into its own
count, which is how it was caught.)*

## The four seats

| seat | what it does |
|---|---|
| **directing** (this one) | writes briefs, hands them to the work session, verifies what comes back, reports each completed item to the audit session, relays the audit's feedback. **Does not implement.** |
| **main work** | implements one item at a time, serially. Owns the worktree while working. |
| **parallel** | literature ("does this paper carry a transcribable X?") **and parallel work** — the literature-only rule was retired by the owner: *"c4는 조사만 시키지 말고 병렬로도 써"* (1588ff47, 2026-09-03 02:34). Because it shares the worktree with the work seat, it takes a **file allocation** from the directing seat before writing, and never edits a file the work seat holds. |
| **audit** | evaluates each completed item independently. Never implements, so it never audits its own work. |

Session names change on restart. Use `ListAgents` and confirm each one's cwd, branch and
current task rather than assuming. **And ask the owner, not only the sessions** — the owner
assigns the seats, and a seat that assigns them itself will get it wrong (this happened twice on
2026-09-03, in the same hour, because this seat read `ListAgents` and never asked). As of
2026-09-03 16:20 (after the terminal crash re-seated everyone; owner's assignment): `nearstars-b0`
(Opus 5) directs, `nearstars-34` (Fable 5.1) works, `nearstars-cd` (Fable 5.1) audits, `nearstars-82`
(Opus 5) is parallel. *(Earlier that day: `nearstars-93` worked, `nearstars-c4` surveyed, `nearstars-f4`
audited, `nearstars-39` directed.)*

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

**Two findings arrived after the core list closed, both about `ice_x`. Brief 34 closed them the
same evening** (`438efd70`, `6ae41eb4`, `21f37436`; notes `engine/superionic-gate-context-notes.md`,
full record in C6's row). Summary, because the shape of the answer is the part worth carrying:

- **The gate was asserting something false and passing.** It compared `ICE_VII_X_T_MAX` (1800 K)
  against a **flat** 2 000 K superionic floor; the real boundary peaks near 200 GPa and
  **descends through 1800 K somewhere in 305–375 GPa** (two figure renderings; the maximum agrees
  to 0.7 % in T, the crossing disagrees by 29 GPa and **was not adjudicated** — a figure reading
  does not settle a figure disagreement). The floor's provenance was also false: that sentence in
  Millot+ 2019 restates **its own refs 6–12's prediction**, verified verbatim in the cached PDF.
- **Both ceilings do have a consumer — and it does not reach the answer.** Uranus's *trial*
  corridor makes **1,854** `ice_x` evaluations inside the region, traversing 355→535 GPa along an
  adiabat; the moons make zero and Neptune's corridor stops at 235 GPa. Then a ±5 % perturbation
  confined to the region **fired 1,754 times and moved nothing**, and refusal at first contact
  **fired once and left the trajectory identical** — five runs bit-identical, Δ exactly 0. So the
  answer is insensitive to the region's values *and* the trials that walk it are discardable.
- **Both candidate repairs were discarded by measurement, not preference.** "Assert it is never
  evaluated there" lost its **premise**; "refuse by name at the boundary" lost its **necessity**
  (refusing changes nothing → machinery without a consumer, C5). What landed is **tolerance plus
  labels**, with the gate now asserting the **measured invariance** (`_clamp_invariance`, +22 s):
  a claim about our code, which **fails loudly the day a solver change connects the corridor to
  the answer.**
- **Three transferable lessons.** A null result is believable only once the instrument is shown to
  have fired — hook-fire counts are what make Δ = 0 evidence rather than absence. A distribution
  refutes a story: the directing seat read "the temperature loop is riding the ceiling" and the
  T-histogram killed it (≥1799 K is 0.8 % of hits). And **`ICE_X_P_MAX` stays at 1 000 GPa** —
  A2 *weakened* the case for narrowing, because the only consumer is a corridor that does not
  reach the answer. The invariance is **measured for the current roster's Uranus and is not a
  general guarantee**; a body whose *converged* column enters the region reopens it, which is why
  C6 stays a standing watch.

**Brief 34 was the repair and it LANDED the same evening** (`438efd70`, `6ae41eb4`,
`21f37436`) — measure whether trials enter the false region · replace the flat inequality with a
(P, T)-dependent check · fix the attribution and remove the unlinked duplicate · record the three
ceilings as one notation. *(Corrected 2026-09-03, found by the audit seat: this sentence said
"designed but unwritten" while the paragraph ~30 lines above already said it closed that
evening. It mattered because the parked list's Millot ⑩/⑩b row points forward at exactly this
sentence, so the stale claim was reachable from inside the parked section.)*

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
- **A number in a brief carries its condition AND a commit anchor** (added 2026-09-02, after
  four directing-seat errors in one day, every one caught by someone else). *Condition* means
  which pressure, which curve, which range, which basis — three of the four were **right numbers
  wrongly paired**: a rejected draft's flux married to the adopted radius, a separation lifted
  from a grid point *outside* the adopted range, a 500 GPa comparison quoted as a 200 GPa seam.
  The fourth was an **inverted inequality** — an upper bound read as "certainly not molten" when
  it means "certainly molten above" — so **push an inequality through to its conclusion before
  writing it down**. *Anchor* means the commit or note the value came from (`11,500 W/m² @
  eddd3a6b`), because a condition alone does not reveal that **the condition itself was
  superseded** — that is the half the first error slips through, and the anchor makes staleness
  mechanically checkable. This is the directing seat's version of the work seat's pair gate, and
  the audit proposed it. **A brief arriving with an unanchored number is worth a question back.**
- **A narrow instrument's output is not a general fact, and this seat reported it as one twice in
  one day.** Added 2026-09-03. (i) A **first-page title scan** of the paper cache returned zero
  hits for viscosity, and that was reported as *"no source exists"*. Full-text extraction over the
  same 58 files then found **five** papers carrying printed viscosity constants, two of them
  transcribable dimensional laws — none is *about* viscosity, which is exactly why titles missed
  them. (ii) **One** cache file was found without a PROVENANCE record and the rule proposed from it
  was *"a cached paper without a PROVENANCE file is not a cached paper"* — measurement says only
  **8 of 57** carry one, so that rule would have declared 49 real papers unheld, including the
  three transcribed from that same day. **Both times the instrument was fit for what it measured
  and unfit for what was concluded**, and both times the hedge was stated when the scan ran and
  dropped from the conclusion written about it. **State the instrument beside the finding, and if
  the finding is a negative, say what the instrument cannot see.**
- **The ± is part of the number, and so is the composition.** Added 2026-09-03 after this seat
  stripped a different qualifier three times in one day, each caught by someone else: a σ value
  relayed with **no (P,T) condition** (the work seat refused to transcribe it and was right); a
  conductivity relayed to the owner as "14.65 against 9.0 ± 1.6" with **no composition label**,
  where the two are pure Pv and the same seat's own brief had labelled them correctly; and
  `18.9 / 15.4` relayed **bare** when the source prints `18.9 ± 1.6 / 15.4 ± 1.4`. This is *not*
  covered by "carry the condition" — that rule was in force all three times and the digits were
  right all three times. **A relay that keeps the digits and drops the ±, the composition or the
  condition has not relayed the number**, and the loss is invisible downstream because what
  arrives looks complete. It leaks worst in *summaries*: twice the qualifier was present in the
  brief and absent in the one-paragraph version.
- **When a value sits inside a declared window, say which edge the number is measured from.**
  Brief 36's notes gave a seam step against the pure-mineral centre while the line above it gave
  one against the implemented solidus — both true, exactly the declared half-width apart, and
  **indistinguishable by eye because the three candidate bases are evenly spaced**. Prefer the
  curve the code actually evaluates, so a reader can reproduce it.
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
- **A file in the paper cache is held only once it is shown to be a PDF.** Found 2026-09-03: a
  772-byte anti-bot HTML challenge (aanda.org DataDome, *"Please enable JS and disable any ad
  blocker"*) sat in `docs/phase3/_papers/` under a bibcode filename with a `.pdf` extension for
  eight days (Ni 2018, `2018A&A...613A..32N`). Nothing consumed it — the methodology doc already
  recorded the paper as unreachable — but a bibcode sweep would have counted it as held. It is
  now `*.FAILED-FETCH.html` with a `.NOT-OBTAINED.txt` beside it, kept as evidence. **Before
  recording a paper as held, run `file` on it; before reading a cached paper, check that the
  text layer opens.** A `.PROVENANCE.txt` beside the file is the record of *how* it was
  obtained and should exist for every new fetch — but its absence is **not** the check: as of
  this writing only 8 of the 58 cached PDFs carry one, and the other 50 are real papers.
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
- **The `.md` render is regenerated from the cached `.html`, and the extractor used to lose tables — fixed
  2026-09-03 (Brief 49).** History, kept because it is the evidence: the section walker reached only direct
  children of `ltx_section/subsection/subsubsection`, so **article-level floats** (Seager+ 2007, `0707.2895`,
  the source of `eos.py`'s `fe_eps`/`mgsio3_en` fits — eight of eleven values absent from the `.md`, present
  in the `.html`, transcription correct) and **appendix floats** (RM22 Tables 7–10, the ladder's Table 8)
  never reached the `.md`; and **table captions were never emitted anywhere** (11 of 729 `.md` carried
  "Table N:", all prose), which made a caption-based check see losses that were not there (Zhang & Rogers'
  five tables were always present). The walker now walks appendices, sweeps unreached floats, and emits
  captions; every ar5iv-rendered `.md` was regenerated (`fetch_arxiv_texts.py --regenerate-md`, idempotent).
  **Fallback rule**: for a table the `.md` does not show, read the `.html` and record the render; three
  residual shapes exist (a table not marked as a float, an empty float, a density-signal false positive —
  `scripts/check_paper_tables.py`, 46 → 3 rows on the cited set).
- **Regeneration overwrites hand-made `.md` files unless guarded.** 61 cached `.html` files are not ar5iv
  renders (arxiv.org abstract pages, search pages, a bot-block page) and five of their `.md` files had been
  made by hand from the PDF ("PDF-extracted text (ar5iv render failed …)"); the first regeneration pass
  turned those five into a title line. Restored from the same-session backup; `--regenerate-md` now skips
  non-ar5iv `.html` and any `.md` whose head carries a manual signature — and, after the audit, the
  invariant is **positive**: the generator stamps its first line (`<!-- generated by fetch_arxiv_texts.py
  from <id>.html, <date> -->`) and **only stamped files are ever overwritten**; an unstamped file is stamped
  without content change only when it is byte-identical to the extractor's output, otherwise skipped and
  counted. **Back up before a bulk rewrite, and check what a shrinking file was before accepting the
  shrink** — a file can be right and smaller (bibliography dropped by design) or a person's work destroyed.
  The backup taken before Brief 49's first pass is why five hand-made files were a near-miss, not a loss.
- **Check ADS `esources` before asking the owner for a paper.** The field names the free routes —
  `EPRINT_PDF` is arXiv, `ADS_PDF`/`ADS_SCAN` is ADS's own copy. Measured 2026-09-03: of seven papers the
  directing seat asked the owner to fetch, **three had a free route visible in a field the seat had already
  queried** (Pozzo 2012 and Nimmo & Primack 2020 on arXiv, Nimmo+ 2004 hosted by ADS). The habit, not the
  access, was missing. Query it; escalate only what is genuinely publisher-only.
- **A truncated view of a correct query is a wrong answer that looks right.** `head`, `tail`, `cut`
  and column limits clip *silently* — nothing marks where the output stopped, so a negative reads as
  absence and a partial list reads as complete. **Before reporting a negative or a count from a
  filtered command, re-run it unfiltered, or make the truncation visible** (`wc -l`, a trailing
  marker, `--color` on the match). Two instances 2026-09-03, two seats: the directing seat's
  `grep … | head -30` stopped at line 385 and produced a five-edge count from an eleven-edge list;
  the work seat's `grep … | cut -c1-220` clipped line 261 before the number and produced "38.2 is
  not in the source" for a number on the matched line.
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

> **Standing obligation, added 2026-09-01 on the audit session's finding.** The rule above
> only fires when someone happens to notice — five stale rows were found here because one
> seat cross-checked out of curiosity, not because anything required it. So: **whoever takes
> or hands over this seat cross-checks every row in this section against the commit log
> before writing anything else, and says in their first report that they did.** One pass, and
> it is cheap: each row names its subject, and `git log --oneline -40` shows whether that
> subject closed. A row that survives the pass is dated; a row that does not is moved to the
> resolved list with its SHA. The reason this is an obligation rather than advice is that a
> stale *open* row does not look wrong — it reads as work waiting, which is exactly what a new
> seat is looking for.

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
  8.7 K at 20.0 GPa; averaging does **not** shrink the uncertainty (carry the two curves'
  separation, never σ/√2); below 8.4 GPa is anchored interpolation, not measurement support.
  *Correction (`edf15772`, Brief 35 follow-up ⑤, directing seat's own misquote): the
  separation to carry is **max 16.1 K within the adopted 2.17–14.6 GPa interval, at the
  14.6 GPa kink** — as eos.py now writes it. The "≤54 K" that stood here came from the
  survey grid's curve set at 15.4 GPa, outside the adopted interval; the two adopted
  equations' own separation at 15.4 GPa is 18.0 K, so 54.1 is not re-derivable from these
  equations and nobody should try. Conservative direction (54 > 16), no verdict moved.*
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

**Resolved after that section was written — the tidal axis is wired, and its validation failed:**

- **Tidal heating → interior structure: built, and the validation it was adopted for does not
  reproduce** (Brief 35: `051a8a4c` registration, `e719b5d7` pre-registration committed *before
  the first run*, `e0628e59` the wiring, `bd32daae` the verdict; notes
  `engine/tidal-interior-context-notes.md` §4, code `engine/tidal_transport.py`).

  The cheapness finding stands and is why it was briefed: **Ė(T) is needed to *predict* an
  equilibrium, not to evaluate the conversion at a given heating rate**, which is what
  Kankanamge & Moore 2019 §6 does for Io, and our Ė is likewise a computed input. So declaring
  the transport mode closes the system, and the mode was never touched.

  **What failed is the acceptance test, and the failure is the paper's, not ours.** The printed
  system (36)+(38) was transcribed verbatim and solved to a machine residual of 1e-14; across
  the whole natural-reading constant grid Io comes out at **T_i 1447–1594 K** (which spans the
  target 1471 K) but **δ 97–534 km against the paper's 12.6 km — out by 8–42× everywhere.**
  Registered branches ③+④ fired, and the product is the **name of the wrong assumption**: *that
  the printed §4 system plus Table 5 is the closed system that produced §6's Io result.* Three
  legs, two of them reproduced independently by the directing seat:
  - **Table 5 has no thermal expansivity α at all** — read directly: g, D, Ts, Tsol0, dTsol/dz,
    ρ, cP, L, H, k, η₀, A, T0, and α appears zero times (§6 defers to Schubert 2001). `A = 15`
    carries **no printed units**; `H = 3×10⁻⁶ W/m³` is **one significant figure**; D = 1000 km.
  - **The paper violates its own closure by 16.4 %** — computed from Table 5's own values:
    H·D = 3.000 W/m² against §6's printed F_m + F_c = 2.509 W/m². Closure would need
    H = 2.509×10⁻⁶.
  - **The decisive leg, and the one the directing seat did NOT reproduce**: inverse-solving for
    the constants that make (1471 K, 12.6 km) a root of the printed system gives
    **α = 8.71×10⁻⁷ (1/34 of rock) and ΔT_rh = 354 K** — i.e. *no physically admissible filling
    exists.* If that leg falls, the verdict reverts to "we picked the wrong constants". It is
    with the audit.
  - **Independently of Io**, the paper's own dimensionless Tables 2–4 do not close against its
    printed equations: the latent heat L — **a single constant in the model** — drifts 0.3 → 10.8
    row by row, and eq. (36)'s v disagrees with eq. (37)'s by up to 4×. §7's *"we did refit a_u"*
    names undocumented refitting as the candidate cause. Also with the audit.

  **Two of the authors' own sentences matter here**: *"a correction for the spherical geometry of
  Io should be applied, but that is not included at this time"*, and *"The lid thickness is lower
  than expected, given the presence of ∼18-km-high mountains on Io"* — **the target we were
  matching is one the authors themselves call surprising.**

  ⚠ **Banned number, and it is easy to re-import**: §6's *"totaling ∼1 TW"*. At the 2.5 W/m²
  printed beside it, Io's area gives **104 TW** (reproduced); 1 TW would need a 178 km body. The
  **flux itself is sound**. And *"<15 %"* is §5's parameterization error **against their own
  simulation**, not accuracy against Io.

  **What landed is honest rather than adopted**: `transport_result()` separates declared
  (transport mode) from derived (T_i, δ, F_m, F_c), returns the **stability label** (Andrade →
  one stable point; Maxwell-plus-convection → conditionally stable with a runaway-cooling
  warning, per Rovira-Navarro — multiplicity was **corrected downward**, not multi-valued), and
  carries **`validation:"failed-io-reproduction"` permanently**, so the label itself blocks
  adoption. Io entered the gate as a check table (recorded choice, not a one-off) so that **if Io
  ever comes inside tolerance the test rings loudly — because the story would have changed.**
  Roster measurement with **zero adoption**: Dante and Hades both solve, and **both roots sit
  past the model's validated lid fraction** — Dante T_i 2122 K, lithosphere 147 km (51 % of the
  declared mantle depth); Hades T_i 1844 K, lithosphere 224 km (54 %) — against the paper's own
  validated δ/D ceiling of 0.26, so neither is adoptable and the zero-adoption headline stands.
  *Correction (`086bad3b`/`3b8a9739`): the "Dante has no root" that stood here was an input
  artifact — the rejected 900 km draft's flux (11,500 W/m²) married to the adopted 521 km
  radius; at the canonical §6.5 pair (2,231 W/m²) the root above exists. The reason nothing is
  adopted changed from "no root" to "a root outside the model's validated range".* Boards
  untouched, and the Dante/Hades radius question — a parked owner decision — untouched by design.

  **The unblock route is closed.** The paper's printed data address,
  `http://cas.hamptonu.edu/data-products`, was opened by the directing seat: DNS resolves, it
  redirects to https and returns **HTTP 404** ("Page not found – Center for Atmospheric
  Sciences"). The host is alive; **the path is gone**, and the site now has no data section at
  all. Archives, mirrors and alternate hosts were **deliberately not tried** — circumventing a
  dead link is what the discipline forbids, and **the failure mode is itself the result.**
  W. B. Moore is still listed as faculty there, so **author contact is viable and is the owner's
  call; it is parked, not declined.**

> ## ⚠ Read this first — the work order below has moved on
>
> **The owner cleared every session at this point (2026-09-02, late).** The four seats you are
> joining have no memory of the day; this document and the notes it points at are the whole
> handover. **The single most useful thing to know: work-order items 1 and 2 below have already
> been surveyed to their conclusion, and both conclusions are in the repository.**
> *(Corrected 2026-09-03, audit seat: this said "two of the three" and then named carbon and
> core-melt, which are **both item 2**. Item 1 — the tidal axis — is also closed, by Brief 37.
> So the banner undercounted what was done.)*
>
> - **Carbon is finished as an investigation and it does not build.** Militzer 2024's deposited
>   data covers **2 of the 7 simulated compositions** — one point on each axis, and the carbon
>   one is the hydrogen-free end — so there is **nothing to interpolate along**. The obvious
>   rescue was tried and refused: Bethkenhagen+ 2017's linear-mixing approximation is the right
>   *operation* but the wrong *domain*, and the paper says so itself — it names **"chemical
>   reactions involving carbon"** as its own error source and pushes **demixing** into future
>   work, and Militzer's layer is both. **Do not re-derive this**; it is in
>   `engine/carbon-deposit-context-notes.md`, and the five files to request are named there.
>   **What remains is author contact, which is the owner's call and was not initiated.**
> - **Core melting depression — BRIEF 38 LANDED 2026-09-02** (`543a88ff` → `311c03ee` →
>   `303f1d2e` → `958dab40`; gate FAIL 0, 1220 s, anchors bit-identical). **Nothing here is
>   waiting work** — read this bullet only for how it resolved, and see the resolved row below.
>   The bullet as first written said the measured
>   factor is **0.61–0.70 across five decades of pressure, essentially flat**; our
>   `IRON_LIGHT_ELEMENT_FACTOR = 0.80` is high everywhere, and its pedigree turns out to be a
>   **1981 estimate its own source calls a crude assumption**. Mori+ 2017 prints a Simon equation
>   in **the same algebraic form as our `iron_t_melt`**, transcription-checked against four of the
>   paper's own printed values — so this is **a second `melt` curve, not a scalar**, and the
>   interface does not change. Everything needed is in
>   `engine/core-melt-depression-context-notes.md`, including the trap that cost the directing
>   seat an error: **the denominator must be `FE_EPS`**, because `FE_PREM` already carries the
>   0.80 and using it yields a plausible-looking 0.79–0.83.
>   *Correction (Brief 38 §0, directing seat's own error — right numbers, wrong pairing): the
>   0.61–0.70 is the **Fe–Fe₃S eutectic**, the floor of the melting surface at a composition no
>   roster body runs; our 0.80 rides `fe_prem`, Earth's actual non-eutectic core, and
>   `0.63 < 0.81 < 1.0` is a correct ordering. The Sinmyo+ 2019 ICB check decides it: ×0.80 →
>   −0.12 σ, the eutectic → −2.56 σ (~950 K cold). **The scalar is NOT replaced** — Brief 38
>   stores the eutectic as a labelled bound and repairs the 0.80's provenance, value unmoved
>   (note §2's correction block carries the full case).*
> - **A new index exists**: `docs/reference/paper-defects.md` (+ ko mirror) — **ten defects in the
>   papers we cite**, each pointing at the note that carries its case. Read it before transcribing
>   from any source listed there, and **add a row when you find the eleventh**.

## 2026-09-03 — the properties axis, and the order after it

**Landed and pushed through `cf6b07ae`.** Briefs 39 (+ five follow-ups) and 40; surveys ⑱–㉓;
paper defects #11 and #12; the handoff's own stale rows.

**Brief 39 — the figure's relaxation verdict.** Viscosity's consumer turned out to be
`body_figure`, named by the owner: rotation and tides in, deformation out. The scope was cut to
**wiring only** — `scripts/refs/body_figure.py` is pre-interior-solver code and stays untouched;
the interior solver now *supplies* a verdict it can consume. Branch ① fired: hydrostatic is
supported for every body that has a temperature. ⚠ **The reason is about the roster, not the
code and not the planets** — `potential_temperature` has no floor (only a negative refusal at
`interior.py@«"brown_dwarf": ("중수소가 탄다. 13 M_J 위는 광도가 시간에 따라 변하고 "»`) and the anchors declare 76 K and 72 K, so the cold branch is reachable; the
bodies that currently reach the wrapper simply declare hot mantle tops. **The verdict is
insensitive to every ungrounded constant**: η_s over two orders and E_a over 80 % move the
4.5 Gyr threshold only 700→1009 K, because τ_M spans 20+ decades. That reason is written beside
the constants — *not* that they are trusted.

**Two debts paid that were not Brief 39's.** The anchor fingerprint had diverged at **Brief 36**
(`9ff07deb` edited `_stack`, `integrate` and `solve` without `--refresh`); values still matched,
so only `--fast` rang — and **`--fast` is the only mode that compared the fingerprint while the
gate runs full.** The rule and the gate disagreed for a day. Refreshed as its own commit, and
**the full run now compares too**, so a mismatch fails with "refresh in this commit".

**The three properties, resolved.** Thermal conductivity is transcribable (Manthilake's chain
closes against the paper's own 18.9/15.4 W/(m·K), verified on three independent implementations)
but **the exponent convention had to be recovered by closure, not read** — evaluate `g` at the
target state; the reference-state reading misses by 1.4–1.5× and is the natural one to write.
⚠ At CMB conditions it returns **~1.6× Ohta+ 2012's measurement**, and the two are **not
independent** (Ohta adopts Manthilake's equation, its temperature exponent and its periclase
data). Electrical conductivity is transcribable from Stixrude+ 2020 alone; **there is no
cross-check** — the two papers do not overlap in (P,T) *or* composition. Viscosity's forms are
transcribable and **every constant in them is a declaration**; Karato & Wu 1993, which four
cached papers cite for their constants and none reproduces, is **unobtained**.

**The order after this, and the reasoning that sets it — polish that revives existing depth
first, new axes last:**

1. **Radiogenic heating → structure.** Two consumers already declare by hand and say so in
   `chain.yaml` (`status: gap` on both). **Blocked on papers** — ㉓ established that not one
   cached source converts an abundance into watts; one partial abundance table and seven
   consumers. The short-lived (²⁶Al) half **closes as a named refusal** on our missing formation
   chronology. The `radiogenic_heat_w_m2` tooltip's 2× mislabel is fixed (Brief 40).
2. **The rocky dynamo — scoped 2026-09-03, and it is SMALL and needs NO paper.** `dynamo_rocky`
   is declared at `chain.yaml@«interior_layers:»` with 11 edges and no module registering its recipe. The
   methodology's two sections do **not** conflict: the first *derives*, the second *executes*,
   and the document says so — *"the whole recipe reduces to estimating the normalized moment
   ℳ/ℳ⊕ from the regime ladder"*. **The ladder is the recipe.**

   ⚠ **So `Rm > 40` is quoted and never evaluated. The file contains no formula for it** —
   verified: zero hits for `μ₀`, `Rm =`, or a magnetic-Reynolds equation; `conductivity`,
   `velocity` and `buoyancy flux` appear only in the derivation prose. It sits in the ladder as a
   disqualifier beside two *class judgements*. **The iron-conductivity paper request
   (`2012Natur.485..355P`) is therefore WITHDRAWN** — nothing in this recipe consumes σ, and
   transcribing it would be machinery without a consumer. It becomes needed only if the owner
   deliberately replaces the ladder with a computed gate, which is a different and much larger
   brief — and two of that gate's four ingredients (**velocity, buoyancy flux**) are *absent*
   rather than ungrounded, while a declared velocity would have to be anchored on Earth and then
   compared against a threshold Earth validated. **A closed circle; do not walk into it by
   having fetched the paper.**

   ⚠ **Two edges are promises nobody can keep, and both feed a gate** — the same class the file
   already records for `conductor_phase` as *"아무도 못 지키는 약속"*, which survived that
   cleanup. `tidal_locking → via rossby`: the supplier emits `[locked, t_lock, rotation_period]`
   and a Rossby number is not derivable from a rotation period — **it drives the ×0.06 multipolar
   collapse, the recipe's largest lever.** `heat_transport_mode → via cmb_heat_flux`: the
   supplier emits `[mode, resurfacing_rate]` and `mode` is a *label*, not a flux. **Re-mark both
   `status: gap`; do not build them.** (`cmb_heat_flux` is wanted by two consumers and emitted by
   none — one supplier, not two workarounds.)

   ⚠ **And step 3 points at a table that exists and is the wrong one.** *"ℳ_base from the
   mass/CMF class anchor (table below)"* — the table below is a per-**body** validation table
   (Earth, Mercury, …), not a per-**class** anchor. A reader following the pointer lands on
   something plausible. Two of the five prose regimes carry no value at all, so the ladder cannot
   be executed for a 2–2.5 M⊕ body without a declaration.

   **What the brief is**: five ladder steps over quantities already emitted (`mass`, `radius`,
   `n`, class, `core_radius`, `conductor_phase`, `t_body`), four declarations as a **family with a
   grid** (the regime multiplier is **OC06's own width {0.05, 0.10}**, 2×, base-heated only, with RM22's
   0.06 inside; *corrected three times on 09-03/04 — the 0.15 "Grießmeier" that made it 2.5× was a different
   quantity, the {0.05, 0.06} "1.2×" that replaced it for an hour was two non-independent points —
   `rocky-dynamo-context-notes.md` step 4*), and the closing relation
   `B_eq = 30·(ℳ/ℳ⊕)·(R/R⊕)⁻³`, already Solar-System-validated in the doc against five bodies.
3. **Fe₃S core alloy — demotion lifted 2026-09-03 (Brief 64).** The owner kept branch A (iron-core σ +
   FeS) in the queue — *"근데 설명을 들으니 A도 하기는 해야겠어"* (1588ff47, 09-03 14:26) — and the only
   blocker, the two Pommier 2018 papers, arrived at 14:32 (`2018E&PSL.496...37P`, `2018Icar..306..150P`,
   owner-pasted paths at 14:31, both with PROVENANCE). The order the directing seat then proposed was
   approved with *"ㄱㄱ"* (1588ff47, 09-03 15:23), and this row is its item 2. **The measured reasons below
   still hold and still bound the scope**; they no longer demote it. *(As first written:)* demoted, and
   the reason is measured. ⚠ The melting curve is on the
   **Fe–Fe₃S** join (Mori+ 2017's title, read at source), not FeS; and its 21–350 GPa domain
   reaches **no roster body** — Dante 0.26 GPa central, Hades 0.63, against a 21 GPa floor, and
   Ganymede-class at best lands in the 10–21 GPa hole we already refuse by name. Mars-class and
   up only. **Generality work, not roster work.** ⚠ **And the dependency this seat asserted —
   "Fe₃S gates the dynamo" — is false**: `core_state` answers today from `iron_t_melt` × 0.80,
   which Brief 38 verified at −0.12 σ. Fe₃S *refines*; it does not *enable*.
4. **Tidal axis revival.** A melt-thermostat family is the candidate; **the papers have not been
   read.** Register the reopening conditions before entering — this axis failed once.
5. **Stellar abundances → composition.** The one new axis worth pulling forward, because it
   **removes an input**: composition is a human declaration today.
6. **Tectonic regime — parked, not queued (recorded by Brief 64).** The owner wants only a per-regime
   likelihood for art direction (*"각 분류일 가능성을 %로만 주면"*, 1588ff47, 09-03 14:26), but the seven-regime
   scheme is blog-sourced, back-fitted (Venus → 15 km) and self-described as not a research simulation —
   it fails the grounding rule — and a classifier consumes q · η · Ra, so it cannot start before k and η are
   grounded. Full statement in `mantle-flux-consistency-context-notes.md` §5.

**⚠ A knife-edge found on the way, and it is not on the order above** (Brief 42). `core_state`'s
Earth verdict flips at **γ = 1.5140 against the declared 1.500 — 0.94 %** — and `GAMMA_RANGE_PA`
is 100–340 GPa while that column's centre is 358.6, so the exponent is already extrapolated.
K₀ has 3.4 % of room; **density has none at all — it cancels exactly**, because the adiabat uses
only a ratio on one curve (verified to ten decimals). The answer is right; the margin is not
reported, so a −17 K verdict and a −500 K one read identically.

**Papers not held — rewritten 2026-09-03 by Brief 64, every identifier checked against the merged cache
(0 hits each).** This list contradicted the *"Request list — closed, no open item"* sentence near the top
of this file: that sentence is about the *request* list (what has been asked of the owner), this is the
*not-held* list (what the notes cite and the cache lacks) — two different things, and the old version
mixed them. Removed from here because held or withdrawn: `2020ApJ...903L..37N` Nimmo & Primack (held and
consumed, Briefs 44/57); Karato & Wu, Sclater+ and Davies are *not* removed — other notes say they came
off the *request* list (paywall, withdrawn), which is consistent with their staying unheld. Still not held:
`2001E&PSL.185...49A` Allègre & Manhès · `2013GGG....14.4608D` Davies · `1980RvGSP..18..269S` Sclater+
(both cited by our own methodology) · `2020E&PSL.53416080T` Thompson+ · `2006JGRB..111.6209S` Seagle+ (Fe₃S)
· `1993Sci...260..771K` Karato & Wu (request withdrawn, paywall) · `2019CRGeo.351..154W` Wagle+ ·
`2012Natur.485..355P` Pozzo+ (request withdrawn — the recipe never computes σ, item 2; free arXiv route
`1203.4970` exists — **not fetched, free is not needed**, C5) ·
Solomatov 1995 (given up 15:18, paywall) · Fei+ 2000 (ADS candidate `2000AmMin..85.1830F` — ⚠ confirm against
Mori+ 2017's reference list before use) · Sata+ 2010 ·
**Tier 1 (09-04): `2011Icar..213...12D` Driscoll & Olson 2011** (c = 49, paywalled) — *RM22 delegates the
definition of `q_conv` and `γ_d = 0.2` to this paper and derives neither in its own text; two of C16's
unresolved inputs sit behind this one paper. Tang+ 2025 does not unlock it (0 citations of it there).*
Tier 2 (09-04): `2009Natur.457..167C` Christensen, Holzwarth & Reiners 2009 (c = 356; cited by our
`planetary-dynamo-scaling.md`, not held) · Christensen 2010, SSRv 152, 565 (Tang+ 2025's U scaling; not
needed until C16/C23 is actually built). Obtained 09-04 by the owner: **Tang+ 2025** `2025ApJ...989...28T`
(free arXiv 2410.21584; PROVENANCE) — C18's closure and C23's listing rest on it.
**Removed 09-04 — held after all: `2011ApJ...733....2N` Nettelmann+ 2011 is `docs/phase3/_papers/1010.0277.md`
/`.html` (arXiv-id filename), and `radiogenic-context-notes.md` §5 already said so — the same false negative
as RM22 on 09-03. Cause: the cache uses two naming rules (bibcode, arXiv id) plus sub-folders, so a
bibcode-prefix glob alone manufactures "not held". Check: glob both `<name>*` and `*/<name>*`, and read the
arXiv id from ADS's `identifier` field so both names are tried.** Grießmeier+ 2009 `2009Icar..199..526G`
(cited in this file's order section) is **held** — parallel seat, 09-04 01:25, free arXiv, PROVENANCE.
*(Lichtenberg+ 2019 `2019NatAs...3..307L` stood here for twenty minutes on 09-03 and was **obtained by the
owner the same evening** — arXiv v1 preprint with source, PROVENANCE written by the directing seat; see C21.)*
Added 09-03 by C22 (0 cache hits each): **Meyer+ 2015** (molecular aggregates in water–ammonia mixtures, cited
by Bethkenhagen+ 2017; ADS candidate `2015JChPh.143p4513M`, read 09-04, **candidate label kept**) ·
**Hirai+ 2009** (methane phase diagram, Bethkenhagen+ 2017 Fig. 6; ADS candidate `2009PEPI..174..242H`,
candidate). Neither is needed for C22.
Added 09-03 by C22's extrapolation-axis closure (identifiers from the parallel seat's ADS lookup, 0 cache hits
each, not needed — they bound what an extension would have to assert): `2014PhRvB..89q4103N` Ninet+ 2014
(ionic ammonia ~180 GPa) · `2014NatCo...5.3460P` Palasyuk+ 2014 (ammonium amide ~120 GPa) ·
`2021PhRvL.126b5003R` Ravasio+ 2021 (liquid → plasma, to ~350 GPa; free arXiv route `2101.06692` — not fetched,
not needed). Obtained the same evening by the owner:
**Li+ 2013** `2013JChPh.139m4505L` (ammonia Hugoniot; preprint + source, PROVENANCE by the directing seat).
A row here is a fact about the cache, not a request; requests go through the owner and are recorded near
the top of this file.

### Where the night stopped, and what unblocks it

**45 commits landed 2026-09-03**, through Briefs 39–43 and their follow-ups. All three seats are
idle and **nothing further can start without a paper.** That is the block, and it is a single one:
**`2020ApJ...903L..37N` (Nimmo & Primack) opens the radiogenic axis**, which is item 1.

**What the night established that a later seat should not re-derive:**

- **The three properties are resolved** — see the section above. Thermal conductivity's exponent
  convention had to be **recovered by closure, not read**; electrical conductivity has **no
  cross-check available**; viscosity's constants are **all declarations**, and its consumer turned
  out to be `body_figure`, not the tidal axis.
- **Two checks were added that fired on day one, against this seat's prediction both times.**
  The join/phase assertion found **7 of 14 melt-bearing phases** bridging a density fit to a
  melting curve on a different composition — six of them Brief 36's silicate proxy, never
  declared. The `via` check found **four wrong arrows in the canonical graph**, one of them
  `stellar_wind`'s only incoming edge.
- ⚠ **The most consequential single finding: `GAMMA_CORE = 1.5` is load-bearing for Earth having
  an inner core at all in this recipe.** The code quotes Alfè twice — solid ≈1.5, liquid
  1.51–1.52 — we use the **solid's** value on a **liquid** density fit (`fe_prem`, pinned by
  Brief 41), and at the liquid value the centre verdict turns liquid, which is wrong for Earth.
  The constant stays because moving it to make an answer come out is prohibited. **That
  prohibition has a cost and this is it.** Both γ bands are extrapolated at Earth's centre.
- **A stronger invariant than it reads**: removing all 19 `status: gap` edges leaves the strongly
  connected component at **exactly 16 = `coupled_core`.** The cycle is real coupling, not an
  artefact of unsatisfiable edges — and `chain.py check` cannot tell you that, because it includes
  gap edges in the ordering.

**Rules added 2026-09-03, all three the same shape — something that reads complete and is not:**
the **± and the composition are part of the number**; **a narrow instrument's output is not a
general fact**; and **a locator or a count without its rule is neither** (a line number without
its extraction mode, a threshold without the pressure it was read at, an SCC count without the
edge-kind rule). Each has three or more instances from this seat and others.

**And a standing caution for whoever sits here next**: this seat's prior that *"a check added now
will catch nothing today"* was **wrong twice in one night, in the same direction**. The quiet
places were quiet because nothing was checking them.

**The work order, set by the owner 2026-09-02 — follow it rather than re-deriving one:**

1. **The tidal axis, revived.** It closed in Brief 35 as *wired, validation failed* — and the
   failure is the paper's, not ours. What reopens it is **Spencer, Katz & Hewitt 2021**
   ([`2021Icar..35914352S`](https://ui.adsabs.harvard.edu/abs/2021Icar..35914352S), cached, open
   access): the same relation — tidal heating → lithospheric thickness on Io — from **a
   different group by a different method** (3-D tidal heating coupled to magmatic segregation).
   That looked like a genuinely independent second route to the acceptance test the first paper
   failed. **Survey ⑭ closed it: it is not one.** Spencer's Table 1 says *"**Chosen** to give an
   average lithospheric thickness of ~35 km"* and *"**Chosen** to give a total heating rate of
   10¹⁴ W"* — **both are calibration targets, not predictions**, so the paper cannot supply the
   leg. Worse, the two share an anchor: both take Io's observed heat output as an *input*, from
   different citations, landing 3.9 % apart. **Independent in method, not independent as a test.**
   Moore, Simon & Webb 2017 is not a third leg either (Moore is a 2019 co-author, and the letter
   defers its model to the thesis), and the thesis was the long shot it looked like — its
   parameter table is **non-dimensional, all 1.0**, which turned out to be the *explanation*
   rather than a dead end. **Brief 37 landed and this row is now closed** (`d86a33d4`,
   `994ac3ab`); the mechanism, the three causes, and the conditions that would reopen it are in
   `engine/tidal-interior-context-notes.md` §7. **Reopening needs a model built for the structure
   Khurana's induction signature implies — not more digging in that paper.**
2. **The two missing materials.** **Core alloys** — `melt_scale` sits in `eos.py` with the comment
   *"the alloy core's depression goes here"* and no alloy material fills it, so the **melting
   depression** is a declared convention rather than a material property. And the **C–N–H
   polymer** the carbon axis needs, which is the same thing as item 3's scope decision.

   ✅ **The melting half of this row closed with Brief 38 (2026-09-02), and not as expected.**
   The depression is *still* a declared convention and that is now the grounded answer, not a
   gap: 0.80 rides `fe_prem`, Earth's actual core, where Sinmyo+ 2019's ICB check puts it at
   **−0.12 σ**; the Fe–Fe₃S eutectic (0.61–0.70) is the *floor* at a composition no roster body
   runs, and it is stored as a labelled bound — `iron_fes_eutectic_t_melt`, `None` outside
   21–350 GPa, `IRON_FES_GAP_REASON` for the 10–21 GPa hole neither source covers. **The bound
   was measured and deliberately not wired**: the smallest margin between our declaration and
   the eutectic floor is **+407.5 K at ~48 GPa**, so no roster body can violate it — C5, no
   machinery without a consumer. It gains one the day a body declares an S-rich core. The
   **C–N–H polymer half is closed by carbon not building** (banner above). What is left on this
   row is only the two unobtained papers: **Fei+ 2000** (the eutectic curve's single anchor —
   **and contradicted at 20–21 GPa, where it is load-bearing, by Pommier+ 2018 which we hold: 1700 °C
   (±50) measured against Fei's predicted 1900 °C, a liquidus-shape dispute; obtaining Fei gives two
   disagreeing sources, not a settlement** — `core-melt-depression-context-notes.md` §8, Brief 58) and
   **Sata+ 2010** (load-bearing under Hakim's density table).

   ⚠ **Two corrections to how this row was first written** (2026-09-02, survey ⑮ + the owner).
   **The density half of it was wrong**: `earth_like` resolves to `fe_prem`, not pure iron
   (`interior.py@«"iron":       (1.000, 0.00, 0.00, "fe_eps"),»`; `fe_eps` is reached only by `composition="iron"`), and `fe_prem` is already
   alloy-grade — **7 050 kg/m³ at ambient against pure iron's 8 300, i.e. 0.849**, which is *below*
   Wicks+ 2018's measured Fe-15Si (7 168). So there is little density headroom on this axis, and
   the earlier claim that a pure-iron assumption drove a roster body's radius sensitivity is
   **withdrawn**. **And the reasoning was pointed the wrong way**: that sensitivity was measured on
   **Dante, whose mass and radius are both labelled `INVENTED`** — an art-directed body cannot
   motivate engine work, because when the tool and an invented pair disagree **the tool is what has
   grounding**. The standing goal for this solver is generality (*any* planet), and that is the
   only justification this row needs. **Do not fit the engine to the roster.**
3. **The three missing properties.** Materials currently answer density, specific heat and
   adiabatic gradient, and nothing else. **Thermal conductivity** — Brief 35 needed it and
   borrowed it from a paper's table. **Viscosity / rheology** — tidal response and convection
   both hang on it, and both are declarations today. **Electrical conductivity** — the dynamo
   needs it and it is nowhere in `eos.py` or `dynamo.py`. Thermal conductivity belongs with
   item 1 rather than on its own; survey ⑭ carries a rider asking whether those three papers
   print it.

   ⚠ **That last sentence is wrong and is withdrawn (2026-09-03).** The rider came back
   **negative** — Spencer 2021 and Moore 2017 print no conductivity and the thesis is
   dimensionless — and item 1 itself closed with Brief 37. **Binding thermal conductivity to item 1
   therefore makes it unschedulable**: the row is closed, its re-opening needs a model built for
   Khurana's structure which does not exist, and the literature that would have carried k prints
   none. The owner confirmed the sentence was a session's judgement, not an owner decision, so it
   is cut: **thermal conductivity belongs on this row, the materials axis, where the rider itself
   says our materials are silent.**

   **Status of the three, after surveys ⑱–⑳ (2026-09-03):**
   - **Electrical conductivity** — buildable today. **Stixrude+ 2020 prints an evaluable
     `σ = σ₀·T⁻¹·exp[−(E* + P·V*)/(R·T)]`** with all coefficients, validity = its simulated box
     100–140 GPa × 4000–6000 K, bulk-silicate-Earth composition, and the fit itself carries no
     calibration. **There is no cross-check**: Soubiran+ 2018 publishes regime values only, and the
     two do not overlap — 240 GPa / 7000 K against 140 GPa / 6000 K, plus iron-free against
     Fe/(Fe+Mg)=0.11, the one variable both papers name as dominant. ⚠ Do not rescue that by
     extrapolation; it gives 328 vs 216 Ω⁻¹cm⁻¹ and is inadmissible on two counts at once.
   - **Thermal conductivity** — the model is `k = k_ref·(T_ref/T)^a·(ρ/ρ_ref)^g` with Table 1's
     fitted coefficients, but `g` and `ρ(P,T)` were in an uncached supplement. **The SI Appendix
     arrived 2026-09-03** and survey ⑳ is testing whether the chain closes against the paper's own
     printed 18.9 / 15.4 W/(m·K). ⚠ Two traps ride with it: the measured box is 8–26 GPa / ≤1273 K
     against an application near 136 GPa / 4100 K, validated only by a *downward* step to 0 GPa
     that its own caption says fails at low T; and Table 1 labels `ρ_ref` **cm³/mol** when the
     values are **g/cm³**, which inside `(ρ/ρ_ref)^g` inverts and amplifies the error.
   - **Viscosity** — **no source at all.** A first-page scan of every PDF in the cache returns zero
     papers on viscosity, rheology or creep. The only η law we hold is one line inside Kankanamge &
     Moore 2019, a paper already on the defect index. This is the thinnest of the three and it is
     thin for lack of literature, not lack of work.

   **Consumer audit — Brief 54, 2026-09-03: this row is CLOSED without a new material method.**
   Viscosity's consumer is live and was already served by Brief 39 (`rheology.py` carries exactly
   survey ㉑'s two laws). Thermal conductivity refuses: its two holders are reproduction
   constants (k = 3.456 → 4.0 moves Nimmo's 42 TW closure 1614 → 1580 K). Electrical
   conductivity refuses: Gaidos's Rm route eliminates V and is blocked on φ, the core entropy
   production = the CMB heat flux nobody emits (`chain.yaml@«day_night_contrast:»`); σ moves Rm by its own
   factor against a gate cleared by decades. The transcriptions stay in their survey notes.
   Full measurement: `engine/property-consumer-audit-context-notes.md`.

   **A structural fact that decides where each one can land**, measured from `chain.yaml` on
   2026-09-03: `dynamo_rocky` sits **outside** the declared 16-node coupled core and reads its
   converged output, while `heat_transport_mode` is **inside** it. So electrical conductivity
   attaches where it cannot disturb convergence; thermal conductivity attaches inside the loop
   that has to converge.

**Still open (owner decisions, unordered):**
- **~~Carbon's fluid axis~~ — CLOSED 2026-09-03. The owner's word: "사실상 닫힘" (effectively
  closed).** The scope decision below was taken on 09-02 and then overtaken the same day by the
  banner above: the deposit is 2 of 7 compositions, so there is nothing to interpolate along and
  the axis does not build. The only re-opening route was author contact, and **the owner declined
  it on 09-03** (see the author-contact row). So this row is closed, not parked. The scope
  reasoning is kept below because it is the right answer *if* the data ever arrive — do not
  re-derive it, and do not re-open the row without new data.

  *(Original 09-02 decision, preserved:)* The
  owner's words were *"as always, general"*, which is the standing goal for this solver rather
  than a fresh judgement: filling the coverage map **is** the plan, not drift from it.

  What that settles, and what it does not. **Settled**: not a Uranus/Neptune special case. Half
  the rationale had been retracted by the surveyor who wrote it — the composition numbers are
  **fitted interior-model parameters, not chemistry outputs**, so the fluid and diamond axes
  *both* need declared quantities and the contrast that motivated picking fluid is narrower than
  it looked. General means it needs **four declarations per body** (two layer compositions, two
  boundary radii) against **two** published examples. **That is the shape that closed hot
  sub-Neptunes, and it is not the same case**: what closed those was a parameter with *no*
  published value anywhere. Here there are two worked examples, a printed stability inequality
  (H₃ < H₂), an exact endpoint (undepleted CH₄–NH₃ gives H = 1 by the printed definition), and a
  printed interpolation form — a floor to declare from. The recipe declares routinely; the rule
  is *say that you declared*.

  **Still binding on the build**: adopt it as a **declared family with a grid, never one elected
  quadruple** — C11's ending, where the grid is the answer and anything needing one number
  declares its own. And **this axis has no independent validation anywhere**: J₂/J₄ were the fit
  targets, not a prediction test, which is precisely the threshold the tidal axis cleared through
  Io and this one does not. **So the output is *structure consistent with the physics*, not
  *structure constrained by data*, and it must say so on every value it emits.**
- **~~Zenodo download permission~~ — RESOLVED. The record IS in the cache; this row was false-open
  for a day.** `docs/phase3/_papers/militzer2024_zenodo/13937364.zip`, 131,906 bytes, **7 files /
  130,650 bytes unpacked** — matching `carbon-deposit-context-notes.md`'s own count exactly. File
  timestamp 2026-09-02 22:34, *after* the commit (`af5e59c8`) that wrote the "nothing was
  downloaded" text below, and survey ⑯ then parsed every row of every file. The host block is
  moot. **This is the exact disease the section's own standing obligation exists to catch, and it
  survived one cross-check pass** — found 2026-09-03 only because a new seat checked the cache
  rather than reading the row. *(Original text, preserved for its reasoning about not
  circumventing a network block:)* Carbon's
  layer equations of state are **distributed as deposited data, not printed** — the AQUA/CDS
  shape we already accept. Record IDs, read from the cached paper's own text rather than relayed:
  **13937364** (data files, the one we need — the paper says the Fig. 1 equations of state are
  there), 13952386 (figure files), 13326881 (code). **Nothing was downloaded**: the Zenodo API
  returns **403 — *"restricted due to unusual traffic from your network"*** with a reference ID.
  **That was not circumvented, and should not be**: it is a network-level block that names itself,
  and the same discipline that refused to route around a dead link applies here. Four hosts
  refused us today (Wiley, A&A, ScienceDirect, Zenodo), so **our own request rate is a live
  suspect** — the right move is to stop knocking, not to change headers. **A browser will very
  likely fetch it in one click; ask the owner rather than re-running the API.**
- **Merging `engine/prototype` into `main`**, and whether to open a PR. **Still deferred — and
  the owner's 2026-09-03 decision was "push only", which is now done.** The branch is on origin;
  the merge and the PR are untouched and remain the owner's call. The cost of deferring: a session in the main checkout sees the last work as
  tidal heating and the stability simulation and is not wrong.
- **Dante · Hades radii — the owner restated the condition 2026-09-03, and it is more general
  than this row was.** Not "decide later" but: **when the tool and the node are finished.** And
  it is not about Dante — *"모든 천체가 다 마찬가지"*, every body is the same; boards get redone
  once the chain is tooled and re-run. Dante was **a temporary test**, and the owner's words on
  what that test is for are worth carrying verbatim: finding errors through it is good, *"그걸
  천체의 값을 지금 확정적으로 바꿀 이유가 되진 않잖아"* — it is not a reason to change a body's
  value now. So `f5db1989`'s measurement stands as **a measurement of the tool**, not a proposal
  for the board — and state it with the right subject, because the row said it backwards until
  2026-09-03: **the solver wants ~486 km at the adopted mass; the *family* on its own terms wants
  521, because its constant-density scaling law is supported and only its 2,620 constant is not**
  (the engine's dry-silicate floor is enstatite 3,220). ⚠ And the pair is **not unreachable**: the
  commit's own measurement has `serpentinisation = 1.0` reproducing **519.4 km, −0.3 %, inside the
  ±2 % tolerance** — it is rejected because antigorite contradicts a volcanic moon's identity, not
  because the tool cannot get there. A reader of this row alone would otherwise take 521 as
  unsupported by any route. *(Both corrections found by the audit seat.)*
  **Do not put this to the owner again as a three-way choice** — it is sequenced, not undecided.
- **Paper requests**: the ternary grid closed as not found. **French, Desjarlais & Redmer
  2016** (PRE 93, 022140, `2016PhRvE..93b2140F`) was **obtained by the owner 2026-09-01** and
  is cached with PROVENANCE; it prints **no** boundary equation or table, which is recorded as
  a legitimate *not found*.

  **Corrected 2026-09-03 — "Nothing is outstanding" was false, and false in the dangerous
  direction.** A row that reads *closed* when it is open stops a seat from looking at all, which
  is worse than the stale-*open* case the section's preamble warns about. Both the audit and the
  parallel seat found it independently. Actual state:

  - **Obtained 2026-09-03, all three by the owner, all three cached with PROVENANCE**:
    `2017PNAS..114.9009S` (Scipioni, Stixrude & Desjarlais — ⚠ **the same three authors as
    Stixrude 2020**, so not an independent check on it), `2011PNAS..10817901M.SI` (the Manthilake
    SI Appendix, 32 pp — this is what unblocks the thermal-conductivity axis), and
    `2012E&PSL.349..109O` (Ohta — the only measured MgSiO₃ post-perovskite conductivity we hold).
  - **Still unobtained, both from Brief 38's row**: **Fei+ 2000** (the Fe–FeS eutectic curve's
    single anchor — unobtained, load-bearing, **and contradicted at that pressure by the cached
    Pommier+ 2018**, `core-melt-depression-context-notes.md` §8; not re-added to the closed request
    list) and **Sata+ 2010** (load-bearing under Hakim's density table).
    **Superseded 2026-09-05**: the owner supplied five of the six, so Sata+ 2010, Fischer+ 2014,
    Komabayashi 2014, Noack & Lasbleis 2020 and a candidate for Chen+ 2008 are held, and
    `core-melt-depression-context-notes.md@«Five of the six cleared on 2026-09-05»` now carries the
    state. What is left is one paper, Fei+ 2000, and the Chen identification is unconfirmed.

- **Author contact — a row this section never had, and the owner has now closed it.** Two asks
  were recorded and never initiated, each in its own note rather than here: **carbon's five
  missing compositions** (`carbon-deposit-context-notes.md` §5, named there, priority
  `C₄₈N₁₂H₅₈`) and **the single tidal question** (`tidal-interior-context-notes.md` §7 — which T₀
  entered Kankanamge & Moore's §6 Io calculation, the dimensionless 1 or Table 5's 1400 K).
  **Owner, 2026-09-03: "둘 다 지금은 안 한다" — neither, for now.** Nothing was drafted and
  nothing was sent. Carbon's closure above follows from this half.

## 2026-09-04 evening — the magnetic-wiring day, written by the work seat at close

**Seats (owner's assignment after the terminal crash, ~17:50):** `nearstars-77` directs · **`nearstars-b2` (this
session, Fable 5.1, effort low) works** · `nearstars-5a` (Fable 5.1, low) audits · `nearstars-7a` (Opus, medium) is
parallel. Names change on restart — `ListAgents`, then ask the owner.
**From the night of 2026-09-04 the default assignment is every seat on Opus** (owner): Fable low was retired after its
usage limit stopped the audit seat and the work seat for about an hour each today. **C30's audit was not started** (the audit
seat hit its limit) — first audit tomorrow, baseline `results_53856339.json`.

**The day's question:** can the interior domain supply what the magnetic side asks for? Answer Ⓢ
(`interior-dynamo-handoff-context-notes.md`): the methodology's printed Needs (`rocky-planet-dynamo-methodology.md@«**Needs** — `mass_earth` [M_earth] · `radius_earth` [R_earth] · `conductor_phase` [—] · `stagnant_lid` [—] ·»`)
owe the interior exactly one quantity, `conductor_phase`, and it is supplied; the five interior → dynamo edges the chain draws
beyond that have no printed Need and no code consumer. Pandora's `conductor_phase` needed a declared potential temperature
(C29) and then still came out undecided (no core-side CMB temperature), so the owner declared the dynamo on (C29 c): engine
B_eq 41.4 µT against the board's 75 µT, recorded, board untouched.

**Landed tonight (engine/prototype, in order; gates 90–95 `GATE END … rc=0`, FAIL 0 (gate95 PASS 541); gate96 FAIL 1 (see its row); gate97 rc=0, PASS 542, FAIL 0 (22:19:03 → 23:30:34, 4 291 s — again slow, again unexplained)):**

| sha | what | audit status as known here |
|---|---|---|
| 0ac3a951 · 839b2c7c | C27 listed; §5 Ⓢ (1800 K = SeaFreeze knot box) — previous work seat, pre-crash | handed to audit |
| 35d6eead | ice_x temperature-ceiling refusal message: knot box, Millot 2019 dropped | directing seat verified; handed to audit |
| 3a08ac47 | C27 symptom per fraction (0.2 GPa unreproduced, removed); C24 heading-precedence note | from audit's catch |
| dd40c301 | §5 addendum (refusal point 923611757256.9896 Pa · 1800.0000005870 K, 7 PhaseGaps bit-identical) | audited numbers |
| 5ad8f56c | interior → dynamo handoff inventory + chain.yaml ref corrections | audited → two corrections in 37247c5d |
| 0cfad194 | four parallel-seat notes preserved | — |
| 37247c5d | handoff note: Ⓢ evidence level (written after the probe, not pre-registered); ten refs, not eleven | audit's catches |
| 844d0787 | check_paper_held.py reads `*.PROVENANCE.txt` sidecars (6 false ABSENT fixed; sidecars live in the gitignored cache) | pending |
| b8d86b68 | C28 dynamo ice fraction from `interior.COMPOSITIONS` | **audit hold** (named refusal regressed on 3 bodies) |
| 2493e72f | C29 Pandora `potential_temperature` 1600 K declared; core_state → undecided | pending |
| ffff413f | C28 fix: preset lookup behind the ladder's gates; 5 bodies × all nodes bit-identical to 5ad8f56c | closes the hold |
| 53856339 | C29(c) Pandora dynamo declared on; `dynamo_alive` only while undecided; 41.4 vs 75 µT | pending; ⚠ its commit body says "check_contracts 13/13" — the real count was **11/11** at that sha (13 is after C30); not amended because gate95 ran on it |
| b29b556e | C30 tidal heat → interior budget (tidal_heating + heat_transport_mode; totals + heat-pipe floor guard); Pandora 45.33 W/m² vs 45 | gate96 (20:20:12 → 22:15:58, **6 946 s** against gate95's 1 436 s — no cause found, no power stamp; the machine was idle on the work seat's side): **rc=1, PASS 540, FAIL 1** — the dead-link scan, on three relative links inside the preserved `tidal-wiring-facts-notes.md`; code, tests and contracts all PASS. ⚠ its four new Contract blocks carry no date string (same structure as the other recipes' blocks — whether that is an exception to the dated-addendum rule is the owner's call) |
| 0ace3863 | the 53 chain refs and the code citations b29b556e shifted (+18 tidal en / +15 ko / +1 heat) refreshed, old numbers kept; headers on the two records; `ref-drift-b29b556e-notes.md` preserved | docs only; parallel seat re-verified 23/23. ⚠ landed before the work seat had read gate96's rc |
| ba907dd3 | three link targets in `tidal-wiring-facts-notes.md` re-pointed to ../docs/reference/ (gate96's FAIL) | accepted by the directing seat after the fact (grep: no other engine/*.md carries such links); gate97 on this sha: rc=0, PASS 542, FAIL 0 (22:19:03 → 23:30:34, 4 291 s — again slow, again unexplained). ⚠ landed before the directing seat's approval |

**Push state:** `git rev-list --count origin/engine/prototype..HEAD` = **6** at the time of this commit — the directing
seat pushed the earlier part of the evening with the owner's leave. Remeasure; do not quote.

**C30 landed after all.** The owner stopped computation at ~19:45, then released it at ~20:10 ("조석 배선 다시 가보자");
b29b556e landed at 20:20 with the Pandora chain measured on the worktree (Ė 1.866e16 W · 45.33 W/m² · heat pipe · l_int_total
1.868e16 W · total floor cannot-say), gate96 on that sha — result in the row below. Record: `tidal-heating-context-notes.md`.

**Not landed — drafts in the work seat's scratch, which dies with the session:**
- C31 (Dante board rows refreshed from the C30 recipe): `scratchpad/c31/refresh_board_rows.py`, syntax-checked, never run, TODOs
  marked. Constraints: board of record = **main checkout's** `phase4/alpha_centauri.yaml`; dry-run (diff only) on the worktree copy
  first; `--apply` on main only by separate order; dependent rows get dated stale notes, no authored values.
- The tidal_locking recipe drafted earlier (`scratchpad/tl/`) is **on hold** by the owner — never written to the worktree; its
  input inventory is `tidal-locking-inventory-notes.md`.
- Tomorrow's order (owner): C31 → C32.

**Preserved tonight from the parallel seat's scratch (unedited, header only):** `aqua-substitution-context-notes.md`,
`dynamo-input-requirements-notes.md`, `paper-cache-sweep-2026-09-04.md`, `pandora-1600k-analogy-notes.md` (0cfad194);
`tidal-wiring-facts-notes.md`, `io-anchor-notes.md`, `dante-board-900km-notes.md` (b29b556e); `tidal-check-notes.md`,
`tidal-locking-inventory-notes.md`, `magnetosphere-survey-notes.md`, `main-7files-2026-08-21-notes.md`, `aqua-substitution-gaps/`
(3 JSON + README) — this commit. Twelve scratch notes, all in the repository now.

**⚠ The main checkout (`/Users/vana/Desktop/NearStars`) holds 7 uncommitted files.** They are the 2026-08-21 20:21–20:31
work (Dante 521 km propagation: identity rows, stability-sim json, evidence file, doc + ko mirror, checklist), **not** the
pre-crash session's — `main-7files-2026-08-21-notes.md` has the diff. Half of that work (the bulk rows) is committed on
engine/prototype as d6d78b63; the other half exists only in main's working copy, and engine/prototype does not have it.
**Do not add, stash, checkout or edit anything in the main checkout; their disposition is the owner's decision.**

**New rule (owner via the directing seat, 20:35):** a commit that inserts a block *above* lines a methodology document is
cited by updates, in the same commit, every `chain.yaml` ref and code comment carrying those line numbers — or appends the
block at the end of the document instead. b29b556e's contract blocks (+18 lines) moved 14 tidal edges and 39 heat edges; the
next commit repaired them. Backlog, un-numbered (after C32): chain refs by anchor phrase or sha instead of line number.

**Owner's push rule (20:35):** once ~10 gate-clean commits have piled up, the directing seat pushes without asking; the work
seat still never pushes.

**Two discipline facts for the ledger (directing seat, 22:25):** (1) 0ace3863 and ba907dd3 both landed before the END
line's `rc` had been read, or before approval — the work seat's launcher counted `[PASS]` lines and went on; from now the
launcher parses `GATE END … rc=` and stops on rc≠0. (2) gate96 ran 6 946 s (3.5–4.8× the evening's other gates) with no
parallel computation on the work seat's side, `caffeinate` holding the machine awake and no power stamp — cause unknown,
recorded as such. Also noted by the parallel seat, not repaired: chain refs heat:203 and :209 land on table-of-contents rows
and :255 on a `---` rule; they did so before b29b556e too (the shift preserved them) — whether to re-aim them is tomorrow's.

**Rules that bit tonight (short):** stage what you wrote (`git diff --stat` first) · the gate verdict is the `GATE END` line
with HEAD's sha, never a "모두 통과" in the body · a background tool call dies at 10 min — gates run under `nohup` · a sha
written into a note by the same commit is always wrong (the amend moves it) — point at the commit title instead · a named
refusal is a value: an ordering change that turns "'giant' … 암석 사다리 밖" into "no composition preset" is a regression even
when both are None (b8d86b68 → ffff413f) · when the directing seat's brief disagrees with the file, stop and quote the file.

**Owner principle, 19:57 (relayed by the directing seat), verbatim:** *"자기장 세기는 밴드로 출력하면 좋겠다. 하나의 묶음에서
다른 묶음으로 값이 오갈 때는 사용자한테 선택지가 있음 좋겠어."* Two rules follow, listed as **C32** in `interior-core.md`:
(1) strength-type derived values (`dynamo_rocky` b_eq, `dynamo_giant`, later `magnetosphere_geometry`) emit a `*_min/*_max`
band beside the point, with the width's source labelled (regime grid · multipolar 0.05–0.10 · declared range). (2) At a
bundle boundary — engine result → phase4 board, declared input vs computed value, canonical vs interesting-first — the engine
does not pick one: it emits a `choices` record (candidates + source + grade) and the owner records the pick on the board with
a reason. **No silent default.** Trigger: Pandora 41.4 µT (engine) vs 75 µT (board) tonight.

**Tomorrow's order (owner):** C30 → C31 → C32.

## 2026-09-05 overnight — C31 landed, and citations stopped being line numbers

Written by the work seat at close. Seats: directing `nearstars-77`, work (this), plus the audit and
parallel seats. All Opus. The work seat never pushed; the directing seat pushed twice, at `5dcf26c3`
and at `b5b88c94` (gate103 rc=0). **main has three unpushed commits of its own** (`7fd5a6ea`,
`30317daf`, `b99b16a9`) — the owner was asked whether to back those up.

**The owner's instruction, verbatim:** *"인용 부패 싹다 고쳐 — 방법론 문서와 우리 도구 범위에서."*
By close, `chain.yaml` carries **no line numbers at all**: 212 anchors, every one resolving exactly
once. This morning 202 of its citations were line numbers.

### C31 — Dante's board rows are on the 521 km figure

Landed in the MAIN checkout (`7fd5a6ea` · `30317daf` · `b99b16a9`), after the directing seat cleared
that checkout's seven uncommitted files (`24587c5f`). Seven values moved (mass, radius,
reference_radius, gravity, tidal_heating ~1200× → ~79× Io, tidal_surface_flux ~11,500 → ~2,324 W/m²,
and the `internal_heat` echo); the identity row's frozen sentence had one digit corrected, 78 → 79,
the old figure being the rounded 1200 scaled rather than the law's own 79.28; three rows no recipe can
produce (`surface_temperature`, `albedo`, `geopotential_j2`) kept their values and gained dated stale
notes, the last carrying the size of its own delay (0.039 against 900 km is 0.0131 against 521 km, a
factor 3 read literally). J₂, C₂₂, flattening and rotation_period do not move because the invariant is
**R³/M**, not R or M.

`engine/tools/refresh_board_rows.py` did it and is indexed in `docs/reference/tools.md` §13. It
**refuses by name** when the satellites table and the bulk rows disagree about radius or mass;
`--take-satellites-figure` is how the operator declares which side is current. The guard would
otherwise have blocked the very repair it exists for — the board disagreed with itself on purpose.

### C33 — the engine cites phrases

`<doc>.md@«a phrase that occurs exactly once in that document»`, resolved by `engine/check_refs.py`,
self-tested by `engine/test_check_refs.py`, wired into `check.sh`. Guillemets because a phrase carries
quotes and apostrophes and must survive YAML, Python and Markdown unescaped. In a recipe module that
declares `RECIPE = "<slug>"`, the bare word `doc` means its own document and **only** its own.

**Why line numbers were abandoned.** `internal-heat-luminosity-methodology.md@«**Returns** — `core_cmb_temperature_solved` [K] · `core_cmb_temperature_solved_min` [K] · `core_cmb_temperature_solved_max` [K] ·»` was a contract
block's Needs line when 30 edges were drawn against it, then a different block's Needs line, then a
Returns line — and that last move happened **inside the commit that went to fix citations**
(`25980fdc`). 24 of the 30 were wrong, 20 from birth, and no reader could see it: five contract blocks
in that one document carry near-identical Needs lines. A line number the directing seat had read by
hand with `sed` was off by four lines three hours later.

**The hard-wrap problem, and the third option taken.** Methodology prose wraps at ~80 columns, so a
sentence-length anchor cannot sit on one line. Matching happens against a copy where a newline plus the
following indent becomes one space; **nothing inside a line is touched**, so the strictness that is
doing work survives (`⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴` is unique only with its double spaces).

**The checker's own case history — the most useful thing to carry forward.** One disease, five
appearances, always the same shape: *the checker not saying that it did not look.*
1. `heat:119` — each new edge inherited whatever happened to be on that line.
2. The audit's five enumeration holes (upper-case names, non-`.md` targets, `bodies/*.yaml`, folded
   blocks, bare file names), closed in `5a056357` **with no test** — which is how the next two got in.
3. An unparseable `chain.yaml` reporting zero problems over the 8 % it could still read.
4. Citations inside YAML comments going silent when the scan moved to parsed values.
5. `<doc>.md:Contract`, a form in no bucket at all, found by the directing seat.
Each is now a named failure with an assertion behind it. **The rule this leaves: a commit that closes a
hole brings the test that reproduces it.**

**And the same inheritance mechanism was inside the checker.** Rule 2 read each citation's edge
endpoints with a regex over the citing line, so an edge written as a block mapping — `from:`, `to:` and
`ref:` on separate lines — silently inherited the previous flow-style edge's endpoints. The data had
been inheriting a document line; the checker was inheriting a neighbour's endpoints. Endpoints now come
from the parsed structure, queued per value so two edges sharing one ref are each judged against their
own. **If you read anything line by line, ask what it inherits from the line above.**

**The tool got ahead of the human once**, which is the point of building it: the parse-failure FAIL,
added an hour earlier, immediately caught the work seat's own sweep breaking `chain.yaml` with an
anchor containing a double quote.

### Gates, and why they were slow

`gate98` rc=1 on a preserved note that was 42.9 % hangul — it landed in `a01d7277`, **after** gate97
ran, so no gate had ever seen it (`ec707ad3` translated it). `gate100` rc=0. `gate101` rc=1 on seven
dead links from the newly preserved notes. `gate103` rc=0, 532 PASS, 24 min, and covers everything
above.

**Two or three gates were running at once** — that, not any single gate, is why some took 6 946 s.
⚠ `pgrep -f "scripts/check.sh"` counts **parent and child**, so one gate shows as two: treat 3+ as
"someone else is running one". And the verdict is the `GATE END … rc=` line only; a cancelled run is
not a verdict even with a thousand PASS lines behind it.

### State, and what is next

- **C31** built. **C33** in progress: 175 citations still on line numbers, in code and living notes;
  130 more sit inside preserved notes and are counted apart, because their line numbers were true when
  written. The place to tighten to "unmigrated → 0" is marked in a comment on `main()`'s last lines.
- **C34** listed, code verdicts untouched, awaiting the owner on one question: **what quantity the
  heat-transport table is fed** (four candidates for Earth, spanning 2.20×).
- Backlog in `engine/tools/README.md`: contract-heading anchors → unique Need items where one exists;
  and re-grade the living notes in `engine/` to the wiring's standard (a dead landing there only warns
  today, which is right for a preserved note and wrong for `interior-core.md`).
- The parallel seat's seven `.ko.md` files are **evidence records**, kept verbatim; every verdict they
  carry is in English in C33/C34 (`interior-core.md`).

### Overnight, 2026-09-05: the checker had to be checked

The migration finished the wiring and then spent the night on the instrument. Four things belong in
whatever comes next.

**1. An exemption ate the verdict, and no test caught it.** The `[인용문]` rule — a citation inside
quoted material is not migration work — was written so that a quotation *skipped classification
entirely*. The audit's control pair: the same dead citation bare → `rc=1`, wrapped in `*"…"` →
`rc=0`. "Wrap it in quotation marks and the gate goes quiet" was live for two hours. Two errors in
one: the date requirement went into one of three markers, and the exemption touched the verdict
rather than the count. It now excuses a citation from being **rewritten**, never from being
**resolved**, and only a file that declares itself a preserved record is exempt from failing. This
got in because the exemption shipped without a test, on the same day "a commit that closes a hole
brings the test that reproduces it" was written down.

**2. A warning count nobody could trust.** L-3's payload rule extracted `via:` with `[a-z_, ]+`,
which ran past the value into the next YAML key, so `ref` and `status` became payload names — and the
membership test was a substring test, so that `ref` matched inside the word "reference" and silenced
eight anchors. Narrowed to token equality, case-folded, with headings exempt: **26 warnings became
5**, so 21 of 26 had been noise. The lesson is not about this rule: **before judging a rule by how
much it fires, check that the number means what it says.** The five that remain are all symbol-versus-
name (`b_eq` against "dipole field strength", `column`/`gravity` against `C`/`g`) and stay, because a
symbol dictionary would cost more upkeep than the rule is worth.

**3. The preserved exemption depended on the citation's form.** It held when the citation was written as a line
number and not when the same citation was written as a phrase anchor. The audit's phrasing is the one to keep: *the exemption vanished at exactly the moment
it would be needed* — the migration reaches a preserved note, rewrites its citation into an anchor,
the gate reddens, and the only way back to green is editing the record that "preserved" exists to
protect.

**4. Read `engine/c32-o-anchor-risk-notes.ko.md` first.** It names the three decay mechanisms — the
document grows, a reused citation inherits what happened to be there, a citation is mis-aimed at
birth — and says plainly that anchors kill the first, cut the second, and **leave the third exactly
where it was**. Its §4-9 carries the working rule this night produced: two seats found the same class
of defect, one by doubting their own tool and one by being corrected; waiting to be corrected means
the wrong instruction has already gone out.

Numbers at close: 393 anchors, all resolving; 1 citation still on a line number; 257 inside preserved
notes; 13 into a paper's own source; 7 whole-document. Shipped strings carry a section symbol and the
anchor sits beside them in a comment (refusal 151 → 112 characters, Pandora's first note 282 → 164).

## Two healthy gates were killed by a liveness check that could not see the process — 2026-09-05

`gate110` and `gate111` were both discarded as stalled: no log growth for 45 s, parent bash at 0.0 %
CPU, and — the line that decided it — **`pgrep -x python3` returning 0, read as "the child is gone"**.
A low-memory kill was inferred from swap sitting at 3503 of 4096 MB, and the failure mode was written
up here as new.

It was wrong, and `gate112` showed why by looking alive under the same test. The interpreter that
runs the checks reports its `comm` as **`Python`**, not `python3` — it is the
CommandLineTools framework binary — so `pgrep -x python3` was never going to match it, on any run,
healthy or not. The check returned 0 the way a broken thermometer returns zero degrees.

What the three signals actually mean:

- **A 45-second flat log is normal.** `test_interior.py` runs the shooting solver over the roster and
  holds the log for minutes at a time. Both discarded gates stopped at a heavy test.
- **The parent at 0.0 % CPU is normal.** It is a `bash` waiting on a child; it is supposed to be idle.
- **The only signal that separates dead from busy is a child burning CPU**, and it has to be found by
  parentage rather than by name:

      P=$(pgrep -f "scripts/check.sh" | head -1)      # the gate's own parent
      pgrep -P "$P"                                   # its child, whatever the child is called
      ps -o %cpu=,etime=,command= -p <that child>     # busy, or not

So no gate has been observed dying without an `rc`. Two were killed by this session while working.
The rule that survives is the one that was already written — **judge only by the `GATE END` line** —
and the correction is to its inverse: *the absence of an END line is not evidence of death.* Before
discarding a run, find the child by parentage and look at its CPU. Guessing a process name is how a
healthy 40-minute gate gets thrown away twice, and how a swap statistic gets promoted to a cause.

## Fixing the concept does not fix the expression — 2026-09-05

The brief called the Bond-albedo band and the phase-integral band a bundle. They are not: the
document reaches `A_Bond` by an analog table **or** by `q·p`, and `A = q·p` already has `A` on the
left, so multiplying them is a category error rather than a wide band. That was caught, corrected,
written into the module, and quoted back to the seat that raised it.

Then the unchosen-defaults report listed ten seats — eight table rows and two phase-integral families,
flat, one line each. **The same confusion, one layer down.** An owner reading that count would decide
the same quantity ten times. The concept had been fixed in the prose and in the data, and the thing
that displays them had never been told.

The vocabulary that was missing, and now exists on `Band`:

- **`bundle` — chosen together.** Members move in step, and a corner grid may not cross them.
- **`estimates` — chosen instead of each other.** Bands naming the same quantity are alternative
  routes to it; the count is one seat with N options.

Two rules came out of it, and both are cheap:

1. **When a concept is corrected, grep for everything that renders it.** A count, a label, a summary
   line. The correction is not done while some other layer still speaks the old version.
2. **A count is only as true as the sentence under it.** The report's closing line still read "each
   line is a seat the owner has not chosen" after the grouping was right — the number said one seat,
   the sentence said ten, and a reader believes the sentence. Same failure as the `[미이행]` label
   earlier today, which was accurate about citations and wrong about the preserved notes it also
   printed itself over.

The fix that generalises: **the test forbids silence.** A band that does not say what it estimates
fails the gate, because a band that says nothing gets counted as a decision of its own.
