# 시험이 «게이트 안에서 도는가» 와 «논문 캐시가 어디 있는가» 를 한 곳에서 답하는 도우미 (C134 개정 1 · C142)
"""Two answers the tests share, so no test re-derives them.

`in_gate()` — the gate (`scripts/check.sh`) always exports `GATE_RUNNING=1`. A test that would SKIP because
data, a tool or a dependency is missing FAILs with the same sentence inside the gate, and keeps its named SKIP
when a person runs it by hand (C96 ⓒ). `GATE_MACHINE` is not used for this: it is a knob people override.

`papers_dir()` — the paper cache: `$NEARSTARS_PAPERS`, else `<repo>/docs/phase3/_papers`. The gate fills the
variable from the **launching** tree, because its isolated clone has no gitignored `_papers` (C134 HOLD,
C142: J3R and J7 of `test_fe_hcp` never ran in an isolated gate until this).
"""
from __future__ import annotations

import os
from pathlib import Path

PAPERS_ENV = "NEARSTARS_PAPERS"


def in_gate() -> bool:
    return os.environ.get("GATE_RUNNING") == "1"


def papers_dir() -> Path:
    return Path(os.environ.get(PAPERS_ENV)
                or Path(__file__).resolve().parents[1] / "docs" / "phase3" / "_papers")
