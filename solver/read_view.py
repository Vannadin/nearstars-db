# 매끄러운 읽기 보기 — 기록이 이름 붙인 조각별 매끄러운 읽기를 엔진의 보기 규약(state → ρ, dT/dP)으로 감싸고, 읽기의 사건·거절·T 점프 핀을 엔진에 넘김 (read-view 등록 rewrite/read-view/prereg-read-view.frozen.md, note 1)
"""The engine's view of a record served by its piecewise-smooth read (read-view registration §1, §4; frozen at artifacts
main 99df438b8, post-freeze note 1 at 9ff9ecaf6).

- `load(files, stamp, root)`: the read named by a record's `assemblage.read` (files, stamp). The stamp is sha256 over,
  for each file in the order written, its repo path, a NUL, its bytes, a NUL (registration §1, 68 n1). The first file
  is the read's loader module (a .py inside the repo, stamped with the rest); its `load_read(paths)` gets the other
  files' absolute paths and returns the read. A missing file or a stale stamp is `ReadUnavailable`, never a fallback.
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
                and not Path(fn).resolve().is_relative_to(base / "solver"):
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

    def props(self, p, t, field=None):
        try:
            return self.read.state(p, t) if field is None else self.read.state(p, t, field=field)
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

    def events(self, t_index: int = 2):
        """The read's curve and seam events (§4.3). The lid's T_ad set (t_index 2 inside a conductive layer) is renamed
        «:ad» by the caller; every Event built here records its t_index (note 6 step 1b, C3)."""
        evs = list(self.read.events(t_index=t_index)) if t_index != 2 else list(self.read.events())
        return tuple(evs)

    def note_step(self, live, x0, y0, x1, y1):
        """§4.8: an accepted step at which a live curve's g is None at exactly one end."""
        for ev in live:
            g0, g1 = ev.g(x0, y0), ev.g(x1, y1)
            if (g0 is None) != (g1 is None):
                self.curve_end_steps.append((ev.name, y1[1]))


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
