<!-- Brief 50 — 베이크된 상태방정식 표의 소스 관리 감사: 생성기별 소스 소재, hhe 소스 유실, 보관 관례 -->
# Baked data tables — how their sources are kept (Brief 50, context notes)

2026-09-03. Documentation only. Verifiers: (직) directing seat (the audit), (여기) work seat (every claim
re-checked on disk before writing). The owner asked how the data he supplies is managed.

**Result — branch ① with one ③.** SeaFreeze's version is pinned (v1.1.0 in both generators, both baked
headers, and `eos.py`) and matches the venv (`SeaFreeze 1.1.0` from `importlib.metadata`), so the two water
tables are re-bakeable and **only `hhe_table.py` is at risk** — its source archive is not on disk. ③: the
Zenodo deposit `militzer2024_zenodo/` had **no `PROVENANCE.txt`** (aqua's had one); written now, asserting only
what the handoff recorded and not the owner's fetch date or method. ④ verified rather than taken: `aqua/`
(62 MB) and `militzer2024_zenodo/` are in the main checkout's cache, reached by every worktree through the
symlink — one physical copy, which is the shared cache by design and also the only one.

**Two things not recorded before, now written**: the venv rebuild line (the venv is gitignored and exists
only in this worktree), and the keep-versus-command convention. Both in `engine/tools/README.md`; the hhe gap
and the request list in `engine/SESSION-HANDOFF.md`. `DirEOS2019.tar.gz` was **not fetched** — it goes to the
owner.

## Instrumenting a solver's material calls records what was *asked*, not what was *accepted* (c4, placed by Brief 56)

A hook placed *before* the material call logs every trial the shooting bracket proposes, including
the ones the fence refuses on the spot. That is why an instrumented gas-giant run showed apparent
T_max of 10⁵–2×10⁵ K while every converged column stayed inside the H/He window (14 314 / 19 423 /
22 917 K at t_pot 165 / 1000 / 2000 K; radii monotone 10.88 → 11.36 → 11.73 R⊕). Two consequences:
the gas-giant "in box" request counts include rejected trials, a **second** reason beyond sampling
density to read them as "present, magnitude not established"; the ice-giant zero is unaffected —
zero requests implies zero accepted. Instrument *after* acceptance, or count converged columns, when
the question is what the solver used.
