# M1 런타임 기록(S3 D2 §2.0) — 게이트 단계가 만드는 BurnMan 광물 클래스를 GATE_MASS_LOG 에 한 줄씩 적음 (sitecustomize 가 그 변수가 있을 때만 켬)
"""Loaded by scripts/gate_reads/sitecustomize.py when `GATE_MASS_LOG` is set (check.sh, full lane).

When the `burnman` package has finished importing in a process, `Mineral.__init__` is wrapped. Objects BurnMan builds
while it imports itself (its datasets construct ~130 at module level, e.g. HGP_2018_ds633) are BurnMan's, not the
project's, and are not recorded. The first time each
(module, class) is constructed in that process, one JSON line is appended to `$GATE_MASS_LOG`:
    {"step": $GATE_STEP, "module": ..., "class": ..., "pid": ...}
Written at once rather than at exit, so a forked worker that leaves through `os._exit` is still recorded.
`scripts/check_mass_formula.py --recorded $GATE_MASS_LOG` reads the file after the pool barrier.
Not seen: a process that imports BurnMan without this hook on its path (a step that clears PYTHONPATH)."""
import importlib.util
import json
import os
import sys

_LOG = os.environ.get("GATE_MASS_LOG")
_STEP = os.environ.get("GATE_STEP", "?")
_SEEN = set()
_TARGET = "burnman"


def _patch(mineral_cls):
    init = mineral_cls.__init__

    def wrapped(self, *a, **kw):
        init(self, *a, **kw)
        key = (type(self).__module__, type(self).__name__)
        if key not in _SEEN:
            _SEEN.add(key)
            line = json.dumps({"step": _STEP, "module": key[0], "class": key[1], "pid": os.getpid()}) + "\n"
            fd = os.open(_LOG, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
            try:
                os.write(fd, line.encode())
            finally:
                os.close(fd)
    mineral_cls.__init__ = wrapped


class _Finder:
    """One-shot: wraps the loader of the burnman package so Mineral is patched right after the package executes."""

    def find_spec(self, name, path, target=None):
        if name != _TARGET:
            return None
        sys.meta_path.remove(self)
        spec = importlib.util.find_spec(name)
        if spec is None or spec.loader is None:
            return spec
        real = spec.loader.exec_module

        def exec_module(module):
            real(module)
            _patch(sys.modules["burnman.classes.mineral"].Mineral)
        spec.loader.exec_module = exec_module
        return spec


def install():
    if not _LOG:
        return
    if _TARGET in sys.modules:
        _patch(sys.modules["burnman.classes.mineral"].Mineral)
    else:
        sys.meta_path.insert(0, _Finder())
