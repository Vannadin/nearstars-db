# 풀이 하나의 상태 묶음 — 선언 상수, 층별 물질 보기, 따뜻한 출발, 흔적; 모듈 상태 없음 (설계 §A6)
"""One state bundle per solve (frozen design §A6; registration S4).

Nothing here is module state: a `SolveContext` is built per solve and dropped with it. Counters and pass records go
to `trace`, never to a module dict. Building a context resets the old engine's registered process state through the
adapter (r2 M11), so a solve cannot inherit a previous solve's memories.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Mapping

SOLVER_VERSION = "phase1-0"


@dataclass(frozen=True)
class Options:
    """Declared constants (registration §6 and note 1). Changing one is a new registration note."""
    rtol: float = 1e-10
    eps: float = 1e-6
    r_floor_frac: float = 1e-3
    close_tol: float = 1e-12
    close_iters: int = 100
    n_scan: int = 17
    wall_tol: float = 1e-6
    wall_shots: int = 24
    lid_iters: int = 8
    lid_t_tol: float = 1e-7            # × T_b (registration note 3: the fixed-point map jitters at ~1e-8 in the melt window)
    basal_iters: int = 8
    basal_tol: float = 1e-9            # × R
    event_min_progress: float = 1e-9   # × M
    event_restarts_step: int = 4
    event_restarts_solve: int = 2000
    event_rewalks: int = 32            # secant re-steps per event landing (A1 impl note 8: 8 left an isolated onset
                                       # landing unlanded at Earth 2064.76 K and turned it into a false wall)
    max_steps_solve: int = 200000      # per pass
    band_pass: bool = False            # owner Q4 ②: the rtol/10 band only in sample checks or on demand
    sensitivity_dt: float = 10.0       # K, the warm T_pot + δ solve (registration note 5 item 3f); 0 switches it off
    fixed_dr: float = 0.0              # m; > 0 integrates every layer on the old engine's fixed grid (fixed_grid.py,
                                       # T2 method-term registration). 0 is the adaptive DP5(4) of record
    materials: str = "registry"        # switch-over §1: "registry" (records first) or "legacy" (the switch off, the §5
                                       # baseline). Not hashed into solve_id: its whole effect is in the material bytes


@dataclass(frozen=True)
class SolveContext:
    options: Options
    materials: Mapping                 # layer id → material view
    warm: float | None = None
    solve_id: str = ""
    trace: list = field(default_factory=list)

    def record(self, kind: str, **data) -> None:
        self.trace.append({"kind": kind, **data})


#: Options whose effect solve_id already holds elsewhere (materials: the material bytes name every view's record).
UNHASHED_OPTIONS = ("materials",)


def require_git_tree() -> None:
    """P1R-G2-R-07: solve_id reads git (material_bytes, solver_code_bytes) after the accepted pass; outside a git work
    tree that raised only then. Called before any pass, it fails at once with the reason named. An environment fault,
    not a body's refusal."""
    import os
    import subprocess
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        ok = subprocess.run(["git", "-C", repo, "rev-parse", "--is-inside-work-tree"], capture_output=True,
                            text=True).stdout.strip() == "true"
    except OSError:
        ok = False
    if not ok:
        raise RuntimeError(f"solve_id needs the solver's git work tree ({repo}): material and code bytes are read "
                           "from git (design §A6; P1R-G2-R-07)")


def solver_code_bytes() -> bytes:
    """Phase-1 design note 17 §5 (G2-R-06): the solver's own code, as material_bytes binds engine/ (G3-T-08's pattern):
    git's blob ids of the tracked solver/*.py files outside solver/tests/, plus the content hash of each such file that
    is modified in the work tree or untracked (r2 on note 17: a new module before its commit). A fixed function of
    the tree, no machine paths."""
    import os
    import subprocess
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    counts = lambda p: p.endswith(".py") and not p.startswith("solver/tests/") and "/__pycache__/" not in p
    git = lambda *a: subprocess.run(["git", "-C", repo, *a, "--", "solver"], capture_output=True, text=True,
                                    check=True).stdout
    h = hashlib.sha256()
    for line in sorted(git("ls-files", "-s").splitlines()):
        meta, path = line.split("\t", 1)
        if counts(path):
            h.update(f"{path} {meta.split()[1]}\n".encode())
    # --relative: diff names paths from the top level otherwise, ls-files from -C's directory (68 on f9fdc396)
    changed = set(git("diff", "--name-only", "--relative").split()) | set(git("ls-files", "--others",
                                                                               "--exclude-standard").split())
    for path in sorted(p for p in changed if counts(p)):
        full = os.path.join(repo, path)
        content = open(full, "rb").read() if os.path.isfile(full) else b"<deleted>"
        h.update(f"changed {path} ".encode() + hashlib.sha256(content).digest())
    return h.digest()


def solve_id_of(body_canonical: Mapping, material_bytes: bytes, options: Options) -> str:
    """sha256 of (canonical Body, material data bytes, options, solver version, solver code); no clock (design §A6,
    D-A3-3; note 17 §5 adds the code digest beside SOLVER_VERSION, which stays the human label)."""
    h = hashlib.sha256()
    h.update(json.dumps(body_canonical, sort_keys=True, separators=(",", ":")).encode())
    h.update(material_bytes)
    opts = {k: v for k, v in asdict(options).items() if k not in UNHASHED_OPTIONS}
    h.update(json.dumps(opts, sort_keys=True).encode())
    h.update(SOLVER_VERSION.encode())
    h.update(solver_code_bytes())
    return h.hexdigest()


def build(options: Options, materials: Mapping, warm: float | None = None, solve_id: str = "",
          reset_legacy: bool = True) -> SolveContext:
    if reset_legacy:
        from solver import legacy_materials
        touched = legacy_materials.reset_engine_state()
    else:
        touched = []
    ctx = SolveContext(options, dict(materials), warm, solve_id)
    ctx.record("legacy_reset", entries=len(touched))
    return ctx
