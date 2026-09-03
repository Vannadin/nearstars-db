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
- **Every kept source directory carries a `PROVENANCE.txt`** (who obtained it, when, from where, what is in
  it). `militzer2024_zenodo/` lacked one until 2026-09-03; added.
