# 재작성 솔버 패키지 — 내부구조 적분기(phase 1); 설계는 artifacts rewrite/phase1-design.frozen.md
import sys as _sys
from importlib.abc import MetaPathFinder as _Finder


class _FallSetsHook(_Finder):
    """E24 fall-sets registration rule 2 (reg-e24-fallsets.md): when solver.material_assemblage finishes executing,
    fall_sets.install sets AssemblageView._fall_set_load before the module reaches any importer. Every import path runs
    this package first, so no AssemblageView exists without the installed loader; material_assemblage.py stays
    byte-identical (its blob is pinned by the records' closure_terms)."""

    def find_spec(self, name, path, target=None):
        if name != "solver.material_assemblage":
            return None
        for finder in _sys.meta_path:
            if finder is self or not hasattr(finder, "find_spec"):
                continue
            spec = finder.find_spec(name, path, target)
            if spec is not None:
                break
        else:
            return None
        run = spec.loader.exec_module

        def exec_module(module):
            run(module)
            from solver import fall_sets
            fall_sets.install(module)
        spec.loader.exec_module = exec_module
        return spec


_FALL_SETS_HOOK = _FallSetsHook()
_sys.meta_path.insert(0, _FALL_SETS_HOOK)
if "solver.material_assemblage" in _sys.modules:              # never at package init; kept for a re-imported package
    from solver import fall_sets as _fs
    _fs.install(_sys.modules["solver.material_assemblage"])
