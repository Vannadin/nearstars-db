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
    max_steps_solve: int = 200000      # per pass
    band_pass: bool = False            # owner Q4 ②: the rtol/10 band only in sample checks or on demand


@dataclass(frozen=True)
class SolveContext:
    options: Options
    materials: Mapping                 # layer id → material view
    warm: float | None = None
    solve_id: str = ""
    trace: list = field(default_factory=list)

    def record(self, kind: str, **data) -> None:
        self.trace.append({"kind": kind, **data})


def solve_id_of(body_canonical: Mapping, material_bytes: bytes, options: Options) -> str:
    """sha256 of (canonical Body, material data bytes, options, solver version); no clock (design §A6, D-A3-3)."""
    h = hashlib.sha256()
    h.update(json.dumps(body_canonical, sort_keys=True, separators=(",", ":")).encode())
    h.update(material_bytes)
    h.update(json.dumps(asdict(options), sort_keys=True).encode())
    h.update(SOLVER_VERSION.encode())
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
