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
