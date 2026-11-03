# 로드 센서스의 자식 프로세스 갈고리 — 센서스가 띄운 파이썬 자식마다 올라온 모듈·연 파일·손자 프로세스를 끝날 때 보고하고, 경로 뒤의 다음 sitecustomize 를 이어 부름(sg-gate G1, 68 on db1a128b)
"""Loaded only when derived/load_census.py puts this directory first on a child's PYTHONPATH (LOAD_CENSUS_REPORT set).
It loads load_census.py by file under a private name (no sys.path change, so nothing in the child resolves
differently), installs the census hooks, then runs the next sitecustomize.py on sys.path (scripts/gate_reads,
scripts/c143_naive_sum), which this file would otherwise shadow."""
import os
import sys

if os.environ.get("LOAD_CENSUS_REPORT"):
    import importlib.util as _u
    _here = os.path.dirname(os.path.abspath(__file__))
    _spec = _u.spec_from_file_location("_load_census_child", os.path.join(os.path.dirname(_here), "load_census.py"))
    _lc = _u.module_from_spec(_spec)
    sys.modules["_load_census_child"] = _lc
    _spec.loader.exec_module(_lc)
    _lc.child_setup()
    _after = False
    for _d in list(sys.path):
        if os.path.abspath(_d or ".") == _here:
            _after = True
            continue
        if _after and os.path.isfile(os.path.join(_d, "sitecustomize.py")):
            import runpy
            runpy.run_path(os.path.join(_d, "sitecustomize.py"), run_name="sitecustomize_chained")
            break
