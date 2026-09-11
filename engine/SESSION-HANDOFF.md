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

Rules moved to `derivation-discipline.md@«10. What a seat owes a claim»` (commit d38d8e2c); the original text of this section is readable at `2269a8d5`, the last sha it lived in.

## What 2026-09-01 added to the rules — read these, they are new

Rules moved to `derivation-discipline.md@«10. What a seat owes a claim»` (commit d38d8e2c); the original text of this section is readable at `2269a8d5`, the last sha it lived in.
Its two chronicle entries (the `.md` render regeneration, and the hand-made-file overwrite) moved to the end of the 2026-09-03 section below.

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

## Resume pointer — latest (written 2026-09-11 ~20:00, parallel seat, covering since the 18:00 block)

- **Seats** c3 directing · 21 work · 70 parallel · 45 audit. Brief counter at **194**; ledger items run to **C78**.
- **Remote `engine/prototype`** = **`f681afbd`** (verified with `git ls-remote`, not relayed: `f681afbd2e6d0578bc5309f405fa93d381963a5b`), **17 commits on the branch today**. **189 is closed in both commits** — `5c5b48d3` emitted convergence as values from `interior_layers` and wired eleven solver sites, `e9e4295d` refreshed the C70 path fingerprint, `f681afbd` wired the remaining nine modules into the convergence trace.
- **190 is in flight.** Registered at **`bfeea1c2`** (the draft has moved since — see the drafts list below), and its commit carries two riders: the new **`NOTICE` §5 ENGINE RUNTIME DEPENDENCIES** section and the **C74 status** line. Its substantive decision is the **XC column**: the shipped ice VII/X set takes the authors' recommended **HSE parametrization of Eq. (9)**, while today's constants and SeaFreeze's `VII_X_French` spline are **PBE** — a deliberate change of about 1 % in P at ρ 2.2566 g/cm³ · 1000 K, with a parse-time guard `a0 < 0` that identifies the HSE column by itself. **Sha placeholder for 190's commit: this commit.**
- **Owner decisions since 18:00.** ⑥ and ⑧ are **decided** — the REBOUND rule governs BurnMan and SeaFreeze alike, with Q4 and Q7 closed together by «compute at runtime, commit nothing derived» and no release bundle; SeaFreeze needed no install because it was already there. ① is **no longer urgent**: the owner fetched ten papers at ~19:00, closing B42–B51, and **192** will compare the liquid-iron sources instead of choosing between them. ⑦'s default is **keep-empty**. ③ is now tied to **193**, since `has_inner_core_solved` is one of the nine duplicate-producer keys.
- **Drafts awaiting the audit**, with hashes: **191** `ec3059b7` (BurnMan install into `engine/.venv`, five print-only checks) · **192** `8c009a35` (liquid-Fe third source, print-only, closes ① by measurement) · **193** `59aef92c` (C68 merge rule, reporting first) · **194** `f106e1d1` (C73 lockstep checker). None of the four changes engine behaviour; 192 and 194 need no gate at all.
- **Numbers recounted tonight rather than carried.** C73 is **39 one way and 1 the other** (`tidal_locking.t_lock` in `outputs` with no contract behind it), not the forty in its row. C68's duplicate-producer set is **9**, matching `chain.py@«DUPLICATE_PRODUCER_KEYS = {»` with no drift, and **none of C73's 39 keys would collide** if declared. `graph.order(g)` is total over all 51 nodes — 33 units, the 16-node cycle ordered alphabetically — so «who wins today» is answerable for every duplicate key; what is **not** derivable from the graph is whether both producers are *applicable* to a given body.
- **Paper cache: 311 of 311 primary files carry provenance**, from 67 with none this afternoon. New holdings tonight: the ten owner downloads (B42–B51) installed under their ADS bibcodes with field-by-field identity checks; Millot 2018's Supplementary; the PREM model table (⚠ its own header mislabels density as `g/m^3`; the values are kg/m³); Dorogokupets 2017's five supplementary files (⚠ the `.xls` are formula calculators, not tables — the printed grid is Table S3 in the `.doc`); SeaFreeze 1.1.0's source archive as a reading copy. One request remains open and gated: **Huang 2018's Supporting Information**, HTTP 403 from the publisher for both the article page and the SI link.
- **Rules added since 18:00** (all in force, each bought by a specific mistake):
  1. **An assertion is evaluated against the failure it is written for**, not only against the correct data — a guard that passes on the broken parse is not a guard.
  2. **Read a source's coverage from where the fit is defined**, not from where the simulations are described. This fired twice in two items.
  3. **«Absent» is stated per interpreter, never per machine.**
  4. **A second evaluation of one source is a reproduction, not a confirmation.**
  5. **Print the list; the count is derived from it.**
  6. **When `git status --porcelain` is non-empty, a read is labelled «worktree @\<tip\> + uncommitted»**, or taken from a clean clone.
- ⚠ **The tree is dirty right now**: `NOTICE`, `engine/eos.py`, `engine/interior-core.md` modified and `engine/ice_fr2015.py` untracked — 190's work in progress. Any read of those files before 190 lands must carry the worktree label, per rule 6 above.

## Resume pointer — 2026-09-11 ~18:00 (superseded by the block above)

- **Seats renamed** after the restart: **c3 directing · 21 work · 70 parallel · 45 audit** (the 13:20 block's c3/3d/92/7b are the same four roles, previous names). Brief counter at **190**; ledger items run to **C76** in the tree, with **C77 and C78 proposed and not yet rowed** — both land with 189, so a reader who greps the ledger for them at `7ae0ed27` will not find them and that is expected, not a loss.
- **Remote `engine/prototype`** = **`7ae0ed27`** (verified with `git ls-remote`, not relayed: `7ae0ed278cc8ae252ad6889e9996fbd4fff5eed4`). Two commits landed since the 13:20 block: **`20dc2fe6`** (C75) and **`7ae0ed27`** (187). 14 commits on the branch today.
- **Landed since 13:20**: **C75 closed** (`20dc2fe6`) — `check_md_tables.py` gained a cell-count rule (split on every unescaped pipe, `\|` the only escape, no code-span stripping, a row ragged when its cell count differs from its header, rows running delimiter to next blank line); the rule found **32** ragged rows at `a5021766`, **31 repaired and 1 registered as an exception with its reason** (`engine/c32-m-batch-a-notes.ko.md`, a «원문 무편집» record), baseline now 0; gate full rc=0, 698 PASS. **187 closed** (`7ae0ed27`) — `fe_eps` got a measured hcp thermal set from Dorogokupets+ 2017 Table 1, reproduced against the SI's Table S3 at three (P,T) rows to five digits; `c_p` repaired on evaluator sets; `fe_prem`'s 30 raising cells now return numbers. **C76** rowed from that repair (a material method that raised on the clean tree and was invisible to every body-level baseline).
- **C74 is open, not started** — owner-pending on A–I (P34) plus the licence questions; the ledger row says so. P34 is at **`10034d9c085a6dde`** (19376 B) and does not move again today; the C74 ledger section cites it by hash and **P34 does not cite the ledger back** — the pointer is deliberately one-directional, because hashes in both files falsify each other on every edit.
- **189 is staged as two commits** (work seat) with sha placeholders here: commit 1 = `5c5b48d3`, commit 2 = this commit. Its registered definition is the part to read before touching any solver: **`converged` is three-state per site — `True` · `False` · `None`**, where `None` means «no criterion branch; the loop runs its full count by design» (four bisections are in that state — `core_state.py`:322, `mantle_flux.py`:139, `stagnant_lid.py`:360, `ammonia_table.py`:274 — and adding a criterion is forbidden because an early `break` returns a different midpoint). At a node, `converged` is the AND over sites that have a criterion branch **and ran**; `unconverged_solvers` lists the False sites; `bracket_invalid` lists sites whose entry sign check failed. ⚠ **If every site in a node is `None`, the node is `None`, not `True`** — «nothing to ask» and «everything passed» must not print the same. Files by hash: draft `drafts/189-c71-unconverged-delivered-prereg.md` **`24a5cf77050e8624`**, loop census `c71-loop-census-7ae0ed27.txt` **`19599ae6a5fdcb1e`**, criterion branches `c71-criterion-branches-7ae0ed27.txt` **`200c72b6adbe322d`**. The C76 call-surface baseline is `c76-callsurface-7ae0ed27.txt` **`60c75ee934d1a85c`**.
- **190 is registered and waiting** — `drafts/190-h2o-ice-thermal-prereg.md` **`9cfc56cffb99927c`** (22555 B, Amendments 1–2). The `h2o` ice phases would get c_V/α/γ from French & Redmer 2015's printed potential (Eq. (6) assembled from Eqs. (9), (11), (15); Eq. (13) is the temperature-part fit the verification tests) over the **fit grid, (ρ, T) = 1.6–4.25 g/cm³ × 295–2000 K**, plus Millot+ 2018's held SI Tables 7/8 differenced on their printed grid for the superionic and fluid fields. ⚠ **It does not start until the audit re-takes the anchor baseline at `7ae0ed27`** — the pinned one (`anchor-baseline-c2a6a324.txt`, `6747d42f2757c5d4`) is four commits stale and 187 moved `fe_eps` and `fe_prem`; the audit is staged with script `379ccd7aa53153f8` and reports the three bodies cell by cell, so «nothing moved» is a stated result rather than an absence. SeaFreeze is **not** used by 190, so owner item ⑧ does not block it.
- **Papers and data taken today** (all read-only, all with PROVENANCE, none committed): Millot+ 2018 **SI** `2018NatPh..14..297M-si.pdf` (publisher ESM, no login, 24 pp) · **PREM model table** `1981PEPI...25..297D-model-prem-burnman-v2.1.txt` from BurnMan v2.1 pinned to commit `8175d647be944656039f00d89c779b66a7c847f3` — ⚠ its own header mislabels density as `g/m^3` and the values are kg/m³ · **SeaFreeze v1.1.0** source archive as a reading copy, GPL-3.0, sha256 `c7574f3e9b9628d2…` — ⚠ **no v1.1.0 tag exists in the GitHub repo** and the sdist ships no licence file · Dorogokupets+ 2017 **SI** five files, whose `.xls` are formula calculators rather than tables, the printed grid being Table S3 in the `.doc` · French & Redmer 2015 now has a PROVENANCE file that claims **no route** («route unverified») with identity verified instead.
- **Owner decisions waiting** — one page, `~/Desktop/NearStars-artifacts/2026-09-11-interior-state/OWNER-DECISIONS-0911.md` (Korean, **①–⑧ + ⑥-2**). New today: **⑧ SeaFreeze licence** in the ⑥ family — GPL-3.0, a different version from BurnMan's GPL-2.0-or-later, asking whether an install is allowed given that every ice thermal constant already comes from evaluations this machine cannot reproduce. **⑦'s default is keep-empty** (low-P Fe–S stays an empty slot). Owner-facing pages: `NIGHT-SUMMARY-0911.md`, `OWNER-DECISIONS-0911.md`, `owner-paper-requests.md` (B36 closed today — the Dorogokupets SI arrived by an OA route, no owner action needed), and the board source prepared but **not published** (`board/board-0909.html`, `c9698641c629b8d6`, publishing is the directing seat's).
- **Rules added 09-11 afternoon** (all in force):
  1. **`tee`, never `tail`**, for gate output — a killed run must leave a readable log.
  2. **`--from <sha>` is the sha being judged**, not the baseline; the run is isolated and clones that sha.
  3. **`--targeted`'s base is derived, not chosen.**
  4. **An audit OK binds the exact hash**, one-line additions included — change a clause after the OK and the OK is void; ask again.
  5. **A revert and its new hash travel in one message**, and an artifact that moved says so in the same breath.
  6. **A printed definition comes before any comparand** — if the definition is not printed, there is nothing to compare against.
  7. **A test must be evaluated at its sites before it is registered**: a flag that is always true, or always false, is worse than none, because it reads as evidence of a check that never ran.
  8. **Mechanical and judged findings are separated into their own sections** in any census or review.
  9. **A cross-seat hash pointer is one-directional** — the citing document holds the hash, the cited one does not point back.
  10. **A relayed fact is re-read at its source before it is printed** — three of today's corrections were caught only this way, and one of them was inside a label another seat had dictated.

## Resume pointer — 2026-09-11 ~13:20 (superseded by the block above)

- **Seats** unchanged (c3 directing · 3d work · 92 parallel · 7b audit). Brief counter continues from **185 B**; ledger items run to **C74** (C64–C74 candidates/open; C62 first build landed). **Quiet mode is on** (owner): one gate at a time, `GATE_POOL=2`, no heavy runs beside a gate.
- **Remote `engine/prototype`** = **`fba92180`** (C62 first build) — pushed after gate242 rc=0. Everything since 09-10 evening is pushed; gate216–242 passed except three that were caught and repaired as separate commits (235 dpdt_v signature → 180 D; 237 table format → 185 B; 240 Declared-optional exempt set → C64 B).
- **Landed today (09-11)**: C15/C64 pre-reg + 180 C pre-reg (`fbfe6b2a`) · 180 C/D = C58 implementation (`83da7272`; integrator reads material directly with set-type counters, three core nodes read `core_gamma` with named fallback; GJ 1214 b/imf 0.3 recovered, imf 0.1 named refusal → C69) · 185/185 B Fe–S bracket upper 1423 K, point-kind field (`20aa5c4a`) · C65 radius owner (`a60c0fc0`: `radius_mr_screen`, two chain edges moved to interior_layers, preset counter) · C64/C64 B stale literal removed, C45 (f) 19→18 (`c2a6a324`) · **C62 tidal_response first build** (`fba92180`): liquid core via Saito 1974 §2.3 eqs 17–20 (held, image-only, audited against page 130) + solid layers via Beuthe 2015 eqs 13–18, emitter only (`k2_over_q_emitted`, declared k₂/Q untouched), homogeneous-sphere printed closed forms reproduced to 3.6e-5, Earth two-layer k₂ 0.311/h₂ 0.564 vs Wahr 0.302/0.609; sub-shell ocean and solid inner core are named refusals (C62 (c) follow-up; T&S 1972 not held); static limit whole body (Beuthe eq. 22); no roster body runs it today (declaration-only, ①).
- **Owner decisions taken 09-11**: ① fe_prem liquid set = pressure split (≤35 GPa Huang / above Dorogokupets graded); ② low-P Fe–S left empty (Balog 2003 received, parameters only → P33 later); ③ C62 four (membrane/label · shear both, declaration wins · rheology band · print only); ⑤ work↔audit direct channel on judgement-line items. Silicate slot: BurnMan runtime · S&LB 2022 · chemistry declaration → sourced assemblage → mineral override.
- **Owner decisions waiting** — one page: `~/Desktop/NearStars-artifacts/2026-09-11-interior-state/OWNER-DECISIONS-0911.md` (Korean, ①–⑦ + ⑥-2). Urgent only ①: whether graded-set non-delivery extends to the integrator. Directing-seat defaults in force and labelled: (A) γ·c_p only, density path solid; (2) non-delivery for `core_gamma` consumers only; ⓐ′ integrator reads material; 185 upper 1423 K; C65 edges moved; C65→C68 merge rule split; P34 J = union, K = all participating species, C = exclude 11 author-not-recommended species (2024 README silent → «unknown»).
- **Next in queue**: C74 silicate slot ledger transfer (work-seat draft `drafts/C74-silicate-slot-ledger-draft.md` 3d2fb312…, P34 a37dd5be…) — docs only, **no BurnMan install** until licence row (Q1–Q7, HeFESTo README «no redistribution of modified data», both READMEs held in P30-data) is answered → then coverage programme (P32 map, P33 low-P Fe–S interpolation pre-reg) → old queue (C15 (a) impl, C14/C16, C34). Candidates C66–C73 each need their own brief (C71 unconverged value delivered; C73 chain.yaml outputs 40 behind contract Returns).
- **Rules added 09-11**: drafts live under any `drafts/` in the artifacts folder and are never moved once cited; citing seat computes hashes; `.md` edits → run `check_refs` + `check_md_tables` locally; Declared-optional edits → run `test_check_refs` locally; a consumer calling a phase/material of unknown kind → run all-kind tests (`test_ice_giant`, `test_giant`) first; pre-commit audit requests carry hashes of **all** changed files; when a decision's number changes, grep every place that prints/explains it; widening an exempt set or adding a node no body runs → measure first what the first real user will see; audit reports name the body classes a run did/did not touch (roster has 0 ice_giant/sub_neptune — anchor baseline `anchor-baseline-c2a6a324.txt` covers Uranus·Neptune·GJ 1214 b; C72 candidate: ice-giant radii +5.5/+8.9 % vs published).
- **Owner-facing**: `NIGHT-SUMMARY-0911.md` (final + morning lines), `OWNER-DECISIONS-0911.md`, `owner-paper-requests.md` (Korean-only, open 11 / institutional / held 143 / Downloads filename map), board artifact (work account URL 41975d57…) has «week's progress 09-04→09-11» on top.

## Resume pointer — 2026-09-11 ~07:00 (superseded by the block above)

- **Seats** unchanged (c3 directing · 3d work · 92 parallel · 7b audit). Brief counter continues from **185**; ledger items run to **C70** (C64–C70 are candidates/open).
- **Remote `engine/prototype`** at the time of writing = `fbfe6b2a` (C15/C64/180 C pre-reg). Unpushed and gated: `61374a86` (180 C implementation, gate235 rc=1 — kept as parent) + **`83da7272` (180 D)** under gate236 — pushed if rc=0. Gate216–234 passed; gate235 was the first real catch since 09-10 02:33 (dpdt_v signature).
- **Owner decisions 09-11 morning**: ① fe_prem liquid thermal set = pressure split (≤35 GPa Huang measured / above Dorogokupets graded); ② low-P Fe–S left empty + Balog 2003 received (P31 §5; 10 wt%, parameters only); ③ C62 four = membrane limit+label / shear modulus both, declaration wins / rheology band / first build prints only; ⑤ work↔audit direct channel on judgement-line items; order = through step 3 → materials programme (silicate slot, P34 draft ready) → coverage programme (P32 map ready) → old queue.
- **180 C/D outcome (the night's main result)**: material γ now comes from the piecewise set; three core nodes read `core_gamma` (fallback 1.5 when the label is red, printed/counted, `core_gamma_cmb`/`_center`/`_split`); the **integrator reads the material directly** (set-type counters); graded-set non-delivery applies to `core_gamma` consumers only (directing-seat decisions (2), (A), ⓐ′ — all owner-review). Mars fixed (γ 2.87 in the measured window). Earth/Pandora/Mars core temperatures moved (+498/+428/+257 K, named by set type; bit-identity vs `fbfe6b2a` is *structurally impossible* for those three). GJ 1214 b recovered (published-radius distance 1.26→1.69 %), water-column imf 0.3 recovered (shooting budget extended, trial-step only), **imf 0.1 is a named refusal** (cause = graded set above 35 GPa; tracked **C69** temperature-loop relaxation). Integrator↔core-node γ gap changed in kind: 5.5× (constant vs unlabeled solid) → 1.33× (two papers, both labelled); closes only with a high-pressure liquid-Fe measured set (owner one-click B47–B51).
- **Owner decisions waiting (morning)**: (a) whether graded-set non-delivery extends to the integrator (three options, each loses something — see NIGHT-SUMMARY-0911 ③); (b) review of ⓐ′/(A)/(2)/185 upper bound 1423 K/C65→C68 split; (c) has_inner_core_solved owner; (d) C62 (a) now has five options since Saito 1974 is held (P24 §4); (e) BurnMan licence Q1–Q7 (HeFESTo README forbids redistributing modified data; 17 species not recommended by the authors).
- **Next in queue** (work seat): 185 (Fe–S bracket from Li 2001 Table 1: upper 1423 K primary, off-window label, B&W 2011 Table 1 printed spread as the "bracket not curve" evidence; P16 final `f2164f6a2328d4a6`) → C65 (radius owner) → C64 (stale literal) → C62 first build → P34 silicate pre-reg transfer (no install). Rules added tonight: drafts live in `~/Desktop/NearStars-artifacts/2026-09-11-interior-state/drafts/` (so the audited hash survives the commit); citation hashes computed by the citing seat; a consumer that calls a phase/material without knowing its kind must be tested across all kinds (`test_ice_giant`, `test_giant`) locally first — the roster has zero ice_giant/sub_neptune bodies, so audit baselines now include test-anchor bodies (Uranus, GJ 1214 b); an rc-free exception list, if ever made, needs a pinned baseline constant, FAIL on growth, additions only after pre-registration.
- **Owner-facing files**: `NIGHT-SUMMARY-0911.md` (08:25), `owner-paper-requests.md` (Korean-only, restructured: open 11 / institutional / held 143 / Downloads filename map), `OPTIMIZATION-STUDY-0910.md`, board artifact has a "week's progress 09-04→09-11" section on top (account-bound URL — check `list` before republishing).

## Resume pointer — 2026-09-10 ~23:00 (superseded by the block above)

- **Seats** unchanged (c3 directing · 3d work · 92 parallel · 7b audit; `nearstars-cc` is the owner's own session). Brief counter continues from **184 B**; ledger items run to **C63**.
- **Remote `engine/prototype`** = `eec846df` (180 B) at the time of writing; `f0b0c356` (C61 index row · C62 · C63 doc commit) is under gate232 and is pushed if rc=0; this handoff commit follows it. Everything gated today passed: gate216–232.
- **Landed tonight**: 182 B (`167ac9ee`) · 183 stage-2 Fe–S–O–C (`b5687b0a`, verdict *failed by the 19 GPa floor*, «did the floor hide the verdict» = yes) · 183 B stencil clamp (`05da70ad`) · C58 pre-registration (`5e7f6993` + amendments in `e36e4535`) · **184 gate pool** (`e36e4535`/`da3c65f8`, default pool 2 tonight; gate 45 → 20 min) · **184 B** pool hardening + **C61** «an untallied step makes green» (`e74afbbb`) · **180 B = C58 implementation** (`eec846df`): one `core_gamma(material,P,T)` read by core_state·core_energy·cmb_flux, `role="core"` attribute instead of a name list, named fallback 1.5 when `thermal_source_state` is red (printed·counted·recorded_disagreement·gamma_flip both distances), `no-thermal-set` branch, `CoreGammaMisuse` outside core layers; **integrator deliberately not unified** (five bodies without declared T_cmb would shift +186 K); Dorogokupets 2017 liquid set **not adopted** — reproduces Huang density to 0.5 % but C_V/α/γ off by 40 % (ⓐ′ table in the ledger); fe_eps `alpha_k` second-order term bug fixed; flip point 0.8722 (0.8723 was a rounded-pressure artefact).
- **Owner decisions waiting (first thing on return)**: ① fe_prem liquid thermal set — (i) Huang two points (declare 19–35 GPa, refuse outside) / (ii) Dorogokupets as «disagrees with Huang» grade / (iii) keep solid (check red). This is the key that closes C58's fourth consumer (integrator). ② low-pressure Fe–S (P31, named refusal): (a) Xu Margules model / (b) Terasaki ternary (Ni grade) / (c) leave empty + Balog 2003 one-click (B40). ③ C62 tidal_response four (liquid layer · shear modulus source · rheology election · does node k₂/Q replace declared — default emitter, C39 seam kept). ④ review two directing-seat calls: C58 composition mismatch = *grade*, not fail; core_state fallback (나′). ⑤ work↔audit direct channel on judgement-line items (trialled tonight, halves round-trips). ⑥ BurnMan licence questions (P30 §6). Silicate slot is decided: BurnMan runtime · S&LB 2022 · chemistry-ratio declaration → sourced assemblage rule → mineral-ratio override.
- **Rules added tonight**: pre-registration text is hash-checked by audit *before* commit; doc-only fixes ride the next code commit; the citing seat computes citation hashes itself (P29 relay hash pointed at a version no longer on disk); gate scratch (`$TMPDIR/gate-*`, `gate-pool.*`) is cleaned only after GATE END and never for a live pid (gate229 incident → C61); quiet mode when the owner asks: one gate at a time, pool 2, no heavy runs beside a gate; materials rule 0 — roster relevance is never the reason to skip a slot.
- **Night summary for the owner**: `~/Desktop/NearStars-artifacts/2026-09-10-interior-state/NIGHT-SUMMARY-0910.md` (parallel seat, Korean, decision table). Optimisation study: `OPTIMIZATION-STUDY-0910.md`. Audit baselines for C58 ⓓ: `eos_thermal_05da70ad.json` 1cf7dbed15230301 · `c58_thermal_table_05da70ad.txt` 0b7fe36525aa9c69 · `c58_thermal_mismatch_167ac9ee.txt` c76441233760ed6b · `thermal_5e7f6993.json` e07977cfd77fd8ed (seconds stripped).
- **Next**: pool 8 daytime measurement (184 verdict wall-clock) · C15 pre-registration (draft file only tonight) · then the old queue (C14/C16, C34) unless the owner answers ① first.

## Resume pointer — 2026-09-10 16:00 (superseded by the block above)

- **Seats** unchanged (c3 directing · 3d work · 92 parallel · 7b audit; a fifth session `nearstars-cc` exists and is the owner's own — not a seat, leave it alone). Brief counter continues from **183**. Remote `engine/prototype` = `3a4f6b37`; `167ac9ee` (182 B = C57, inverse cmf on the node path) is under gate221 (`--targeted`, 37 items, started 15:40:21) — **push it when its END line says rc=0**; the work seat's uncommitted edit in `engine/interior-core.md` is the 183 pre-registration in progress, do not touch it.
- **Owner direction (15:xx)**: *materials programme first, then the old queue.* Order: 182 B (landed) → **183** = C55 stage 2, multi-component Fe–S–O–C (O 1–4 wt%, C 0.5–1.4, H undeclared; endpoints P21, extrapolation labels P22; verdict = the gap between the radius-optimal and nmoi-optimal cmf, 0.12 with `fe_prem` → 0.020 with `fe_s_19wt`, must shrink further and a cmf must satisfy both windows; the new phases **must** carry Huang's α/γ so `has_thermal=True`, else Mars's centre flattens to 2000 K below the 2140.6 K centre melt and flips to “frozen”; a column “did the 19 GPa floor mask the verdict” is mandatory) → **180 A/B = C58 redesign** (layer 1 = the material returns c_p·∇_ad·α at P,T — all 13 materials implement them, 11 return numbers; `fe_prem`'s 447.5 is a *solid hcp* thermal parameter set on a liquid phase, replace with printed liquid values; owner decision (c): core c_p from printed values, retire `core_energy.C_P = 840`; four things named `C_P` exist — only the core scalar and the iron phases change; P17 v4.1 sha 4103e440… · P25 · P26 · P27) → **tidal_response node** (P28 sha 92b95059…: Beuthe 2015 eqs 13–18 propagator + Bagheri 2022 rheologies, three-rheology bands, fluid core = membrane limit labelled, shear modulus must be declared per layer) → **compaction** = named refusal (P29: the seven held papers do not fill the cold φ(P) slot; ²⁶Al sintering as a declared bool is owner-pending (d), not urgent) → then the old queue (C15 entropy, C14/C16 dynamo gaps, C34).
- **Paywalled and settled**: Fei 2000 · Li 2001 · Williams & Nimmo 2004 body · Konopliv 2011 · Alfe 2001 · Takeuchi & Saito 1972 · Karato & Wu 1993 · Hirth & Kohlstedt 2003 — proceed at secondary-citation grade, do not ask again. Newly held today: 49 owner downloads + 7 (P1 materials) + 27 (P2/P3) + Alfe 2002 · Stixrude & L-B 2005 (image-only) · PALEOS 2026 (tables “claimed distributed, unverified” — Zenodo 504, one retry on 09-11 then refuse) · Dorogokupets 2017 · Journaux 2020 · Bagheri 2022 review · Henning 2009 · Beuthe 2015.
- **Materials-gap guardrails (memory `feedback_materials_gap_guardrails`)**: described ≠ distributed; which quantity first; keep provenance; never regenerate over hand-made extractions; time-box → named refusal.
- **Rules added today**: no `reset --hard`/`checkout -- .`/`stash` in the shared worktree (measure in a scratch clone); cite the code line before reporting what a rule does; keep the “inferred/extrapolated” tag when relaying a number; an existing self-physics refusal beats a composition-undeclared refusal. **2026-09-11**: when a decided value changes, `grep` every place that prints or explains it — **code comments included** — and fix them in the same commit (missed three times in one night: `core_state.py`'s `recorded_disagreement` line, C58 (a)'s `core_gamma_used`, and `eos.py`'s 1348-era bracket comments); and **a commit that edits any `.md` runs both `check_refs.py` and `check_md_tables.py` locally** — the failure was not that the draft lived outside the tree but that the local pre-check set was a **subset** (anchors only, table renderer never run). `check_md_tables.py`'s own header records the same class caught by eye **twice on 2026-09-06**, «each costing a report, a repair and a 24-minute re-gate»; gate237 is the third. **A check that is right only while nothing exercises it is not right — and that shape appeared twice on 2026-09-11.** gate240 failed because the `Declared-optional` exemption set had been *widened* without moving the registered set, and every other checker stayed silent; C62's contract listed **eight** `Returns` while the node emitted **seventeen**, and it passed only because **no body runs that node** — the first body to declare a block would have met a checker that had never seen nine of its values. ⚠ *Both are the same class: the direction that grows, on the path nothing walks.* So when a change widens a registered set or adds a node no sample exercises, the question to ask before the commit is **«what would the first thing that actually uses this see?»**, and the answer has to be measured, not assumed. **And touching a contract's `Declared-optional` means running `engine/test_check_refs.py` locally before the commit** — that file holds the registered exemption set, and gate240 failed rc=1 on `+mass_radius_relation.composition` `+mass_radius_relation.composition_intent` because C65's follow-up widened the set without moving it. ⚠ *The direction matters: the exemption list getting **wider** is the case the other checkers stay silent on* — `check_contracts`, `check_refs` and `check_md_tables` all passed. That set is the only net for it, and it is pinned as a **set**, not a count, precisely so one key leaving and another arriving cannot cancel out. **And an uncommitted cross-seat check carries the hash of every changed file, not the ledger's alone** — on C64 the ledger sat still at `a82f0431f921ba33` while four other files moved under the audit seat's reading, so a single hash named a state that no longer existed; the audit seat pinned its verdict to nine hashes instead, and that is the form to send. *Keeping drafts outside the tree stands; the cost it carries — the checkers do not see them there — is answered by running the checkers after the move, and a candidate for later is a path argument on `check_md_tables.py` so a draft can be checked before it is folded in.*
- **Owner-pending**: C34 feed; 167 D (a)/(b); episodic/heat_pipe; melting-curve family (Rivoldini (f) needs three labelled readings — the paper is self-inconsistent in four places); C58 (a) undeclared body → refuse vs default, (b) F_DEEP/T_1 under Arrhenius, layer-2 form; H in the core; compaction (a)–(e) incl. ²⁶Al; composition-from-stellar-abundance forward path (conflicts with the [Fe/H] skip — surfaces after C57).
- **Shared folder** `~/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/`: P4–P30 (P23 = parallel inventory with every sha; P30 in flight = machine-readable silicate dataset, BurnMan/S&LB 2011), `owner-paper-requests.md` (★ block + «물성 공백(0910)» section, 103+86 bibcodes); audit tools 43 files in `…/2026-09-08-c47-step4/audit/` (baselines for 183: `c55_cells_167ac9ee.txt`, `audit_cmf_sweep.py` 634a970e… prints both optima; for C58: `thermal_3a4f6b37.json`, `eos_thermal_3a4f6b37.json`, `const_census_3a4f6b37.txt`). State document for outside review: `~/Desktop/NearStars-artifacts/2026-09-10-interior-state/INTERIOR-ENGINE-STATE-0910.md`.
- **Artifacts** exist as one set per account; after an account switch, update *that* account's old URLs (memory `user_account_rotation`), never create new ones.


## Journal

The dated day-by-day sections (2026-09-03 → 2026-09-10, earlier resume pointers included) live in `engine/SESSION-HANDOFF-journal.md`. This file keeps only what a seat needs to resume: where things live, the seats, standing rules, parked owner decisions, and the latest resume pointer. Split 2026-09-10 (owner: handoff reading 209 KB → current state only).
