# 매끄러운 읽기 보기 — 기록이 이름 붙인 조각별 매끄러운 읽기를 엔진의 보기 규약(state → ρ, dT/dP)으로 감싸고, 읽기의 사건·거절·T 점프 핀을 엔진에 넘김 (read-view 등록 rewrite/read-view/prereg-read-view.frozen.md, note 1)
"""The engine's view of a record served by its piecewise-smooth read (read-view registration §1, §4; frozen at artifacts
main 99df438b8, post-freeze note 1 at 9ff9ecaf6).

- `load(files, stamp, root)`: the read named by a record's `assemblage.read` (files, stamp). The stamp is sha256 over,
  for each file in the order written, its repo path, a NUL, its bytes, a NUL (registration §1, 68 n1). The first file
  is the read's loader module (a .py inside the repo, stamped with the rest); its `load_read(paths)` gets the other
  files' absolute paths and returns the read. A missing file or a stale stamp is `ReadUnavailable`, never a fallback.
  A module the loader newly imports from inside the repo must be one of the stamped files, or an engine module under
  solver/ outside solver/tests/ (those are bound by solve_id's solver_code_bytes). The guard sees only modules new to
  sys.modules during the load: one already imported is not re-checked. A git-ignored .py under solver/ is outside solver_code_bytes
  and so bound by neither the read stamp nor solve_id (68 on a5de93a4).
- `ReadView(read, p_stop, record_id)`: `state(p, t, guess_rho) → (ρ, dT/dP, ())` or `Stop("read_refusal", …)`;
  `events(t_index)`; per-pass counters `read_retried` (by kind) and `curve_end_steps`; the T-jump pin table (§4.5).
  A refusal is an exception whose class is named ReadRefusal and that carries `.kind` (c8's proto/inv.py); only
  "extent" and "past_deepest" are retryable (§4.4). Any other exception escaping the read propagates: an engine error.

Imported by solver/solve.py only, so it stays outside `fall_sets.closure()` (registration §1, A2)."""
from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import sys
from pathlib import Path

from solver import stepper as st

Q_MAX = 0.9                                                 # reg-coexistence note 6 step 3 (68 GO, 5b9dfac53)
RETRYABLE = frozenset({"extent", "past_deepest"})          # §4.4: a trial stage outside the read's built extent
KINDS = frozenset({"extent", "past_deepest", "cut", "invalid_state", "tjump_untagged", "p_negative", "field_unknown"})


class ReadUnavailable(Exception):
    """A record names a read that cannot be served: a missing file or a stale stamp (selector, A7)."""

    def __init__(self, reason: str, detail: str):
        super().__init__(f"{reason}: {detail}")
        self.reason, self.detail = reason, detail


def stamp_of(files, root) -> str:
    h = hashlib.sha256()
    for rel in files:
        h.update(str(rel).encode() + b"\0" + (Path(root) / rel).read_bytes() + b"\0")
    return h.hexdigest()


def load(files, stamp: str, root):
    """The read a record names, or ReadUnavailable (never a fallback to the table)."""
    files = [str(f) for f in files]
    base = Path(root).resolve()
    bad = [f for f in files if Path(f).is_absolute() or ".." in Path(f).parts
           or not (base / f).resolve().is_relative_to(base)]
    if bad:                                     # a data-named path never leaves the repo (directing on C1)
        raise ReadUnavailable("path_outside_repo", ", ".join(bad))
    if not files[0].endswith(".py"):
        raise ReadUnavailable("loader_not_python", files[0])
    missing = [f for f in files if not (base / f).is_file()]
    if missing:
        raise ReadUnavailable("missing_file", ", ".join(missing))
    got = stamp_of(files, root)
    if got != stamp:
        raise ReadUnavailable("stale_stamp", f"declared {stamp}, files give {got}")
    path = base / files[0]
    before = set(sys.modules)
    spec = importlib.util.spec_from_file_location(f"_read_loader_{got[:12]}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    read = mod.load_read([str(base / f) for f in files[1:]])
    named = {(base / f).resolve() for f in files}
    for name in set(sys.modules) - before:          # 68 n1: a module the loader pulled in from inside the root must
        fn = getattr(sys.modules[name], "__file__", None)    # be one of the stamped files
        if fn and Path(fn).resolve().is_relative_to(base) and Path(fn).resolve() not in named \
                and not (Path(fn).resolve().is_relative_to(base / "solver")
                         and not Path(fn).resolve().is_relative_to(base / "solver" / "tests")):
            raise ReadUnavailable("unstamped_module", str(Path(fn).resolve().relative_to(base)))
    return read


def _kind(e) -> str | None:
    """The refusal kind of an exception the read raised, or None when it is not a ReadRefusal."""
    if type(e).__name__ != "ReadRefusal" and not any(c.__name__ == "ReadRefusal" for c in type(e).__mro__):
        return None
    k = getattr(e, "kind", None)
    return k if k in KINDS else None


class ReadView:
    """A record's read as the engine's view (registration §1). Built per solve; its counters and pins are per pass."""

    def __init__(self, read, p_stop: float, record_id: str, stamp: str | None = None):
        self.read, self.p_stop, self.material_id, self.stamp = read, p_stop, record_id, stamp
        self.pins = {}                      # curve name → field label (§4.5; filled by the T-jump hook, C3)
        self.reset_pass()

    # ── per pass (§1 solve.inward row; r2 B3, B6) ─────────────────────────────────────────────────────────────────
    def reset_pass(self):
        self.read_retried = {}              # kind → count of refusals returned for a stage (retried or surfaced)
        self.curve_end_steps = []           # (curve, P) of accepted steps with g None at exactly one end (§4.8)
        self.pins = {}

    def counts(self) -> dict:
        return {"read_retried": dict(self.read_retried), "curve_end_steps": list(self.curve_end_steps)}

    # ── the read, as the engine's view ──────────────────────────────────────────────────────────────────────────
    def _refusal(self, p, t, e, kind):
        self.read_retried[kind] = self.read_retried.get(kind, 0) + 1
        return st.Stop("read_refusal", {"p": p, "t": t, "material_id": self.material_id, "kind": kind,
                                        "why": str(e), "retryable": kind in RETRYABLE})

    def _pinned(self, p, t, d):
        """note 6 step 3 / read-view §4.5: inside a jump's walk-side window [P_m, P_m + 2·band], a read whose own field
        is the jump's old field is re-read on the new field (the read serves it inside its built box, else refuses)."""
        for curve, (frm, to, pm, band, up) in self.pins.items():
            if (0.0 <= p - pm <= 2.0 * band) if up else (0.0 <= pm - p <= 2.0 * band):
                if d.get("field") == frm:
                    return self.read.state(p, t, field=to)
        return d

    def props(self, p, t, field=None):
        try:
            if field is not None:
                return self.read.state(p, t, field=field)
            d = self.read.state(p, t)
            return self._pinned(p, t, d) if self.pins else d
        except Exception as e:                                  # noqa: BLE001 — classified below, others re-raised
            kind = _kind(e)
            if kind is None:
                raise
            return self._refusal(p, t, e, kind)

    def state(self, p, t, guess_rho=None):
        d = self.props(p, t)
        return d if isinstance(d, st.Stop) else (d["rho"], d["dtdp"], ())

    def density(self, p, t):
        d = self.props(p, t)
        return d if isinstance(d, st.Stop) else d["rho"]

    def porosity(self, p):
        return 0.0

    def events(self, t_index: int = 2, conductive: bool = False):
        """The read's curve and seam events (§4.3), each recording its t_index (note 6 step 1b). A tagged curve (its
        Event.tag {curve, zone, tagged: True}) gets the engine's T-jump hook, built here from the tag and rd.folds
        (§4.5): the read constructs no protocol object. `conductive`: the lid's T_ad set (renamed «:ad» by the caller),
        whose jump shifts T_ad only."""
        evs = list(self.read.events(t_index=t_index)) if t_index != 2 else list(self.read.events())
        out = []
        for ev in evs:
            ev = dataclasses.replace(ev, t_index=t_index)
            tag = ev.tag or {}
            if tag.get("tagged"):
                ev = dataclasses.replace(ev, coexist=TJumpHook(self, tag.get("zone"), tag.get("curve"), conductive))
            out.append(ev)
        return tuple(out)

    def note_step(self, live, x0, y0, x1, y1):
        """§4.8: an accepted step at which a live curve's g is None at exactly one end."""
        for ev in live:
            g0, g1 = ev.g(x0, y0), ev.g(x1, y1)
            if (g0 is None) != (g1 is None):
                self.curve_end_steps.append((ev.name, y1[1]))


class TJumpHook:
    """The engine's T-jump hook on a tagged curve (read-view §4.5, reg-coexistence note 6): the read gives the jump
    (rd.t_jump) and the stored max|dP_b/dT| and walk reach (rd.folds); the engine computes the band, checks q and the
    reach, and pins the new field in the view until the stepper releases it (curve's own g) or a run starts."""

    def __init__(self, view, zone, curve, conductive=False):
        self.view, self.zone, self.curve, self.conductive = view, zone, curve, conductive

    def _fold(self):
        for f in (getattr(self.view.read, "folds", None) or []):
            if f.get("zone") == self.zone and f.get("curve") == self.curve:
                return f
        raise st.TJumpRefusal(f"refused: no stored fold for tagged curve {self.curve!r} in zone {self.zone!r}")

    def t_jump(self, m, y, upward):
        p, t_ad = y[1], y[2]
        try:
            got = dict(self.view.read.t_jump(p, t_ad, self.zone, self.curve, upward))
        except Exception as e:                                  # noqa: BLE001 — a ReadRefusal by kind; others re-raised
            if _kind(e) is None:
                raise
            raise st.TJumpRefusal(f"refused: read t_jump {_kind(e)}: {e}") from e
        fold = self._fold()
        k = fold.get("dPb_dT_max_Pa_per_K")
        if k is None:
            raise st.TJumpRefusal(f"refused: fold {self.curve!r} stores no dPb_dT_max_Pa_per_K")
        k = abs(float(k))
        moved = abs(got["dT"]) * k
        try:
            q = k * abs(self.view.read.state(p, got["T_new"], field=got["to"])["dtdp"])
        except Exception as e:                                  # noqa: BLE001 — as above
            if _kind(e) is None:
                raise
            raise st.TJumpRefusal(f"refused: read state at T_new {_kind(e)}: {e}") from e
        if not q < Q_MAX:
            raise st.TJumpRefusal(f"refused: path near-tangent to tip curve, q {q:.4g} ≥ {Q_MAX}")
        band = moved / (1.0 - q)
        reach = fold.get("walk_reach_pa")
        if reach is None or not 2.0 * band <= float(reach):
            raise st.TJumpRefusal(f"refused: walk reach short, 2·band {2.0 * band:.6g} Pa > walk_reach_pa {reach!r}")
        self.view.pins[self.curve] = (got["from"], got["to"], p, band, upward)
        got.update(dpb_dt_max=k, moved_pa=moved, path_curve_ratio=q, band_pa=band,
                   shift=(2,) if self.conductive else (2, 3))
        return got

    def release(self):
        self.view.pins.pop(self.curve, None)

    def run_start(self):
        self.view.pins.pop(self.curve, None)

    def enter(self, m, y):                              # never reached: the stepper decides the jump before enter
        return st.CoexistRecord("sharp", {"reason": "tjump_hook_enter"})


def is_read_view(view) -> bool:
    return isinstance(view, ReadView)


def with_counts(out_or_stop, views):
    """§1 (r2 B3, B6): the pass's read counters on its PassOut or on its Stop's state, summed over its ReadViews.
    `_at` adds the reached state only when a Stop has none, so the counts are added in both cases (r2 n on rev 5)."""
    rvs = [v for v in views.values() if isinstance(v, ReadView)]
    if not rvs:
        return out_or_stop
    tot = {"read_retried": {}, "curve_end_steps": []}
    for v in rvs:
        for k, n in v.read_retried.items():
            tot["read_retried"][k] = tot["read_retried"].get(k, 0) + n
        tot["curve_end_steps"] += v.curve_end_steps
    if isinstance(out_or_stop, st.Stop):
        return dataclasses.replace(out_or_stop, state={**(out_or_stop.state or {}), **tot})
    out_or_stop.read_counts = tot
    return out_or_stop
