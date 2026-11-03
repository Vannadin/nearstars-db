# 로드 센서스 전용 대상 — 전체 빌드가 너무 긴 항목을 같은 빌드 함수로, 격자만 줄여 한 프로세스 안에서 돌림(G1 «one build», 1번 줄의 격자 한 점과 같은 꼴)
"""Census-only targets for derived/load_census.py --call. Each runs the entry's real build function with a reduced grid;
the build's own code path (and every import it makes) is unchanged. load_census replaces multiprocessing pools with an
in-process serial stand-in, so the work done in pool workers is seen."""
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent / "engine"


def mantle_one_column(body: str) -> str:
    """6-mantle-tables: mantle_composition.build for BODY on one pressure column (the grid's first P), all T."""
    sys.path.insert(0, str(ENGINE))
    import mantle_composition as mc
    mc.grid_p = lambda: [mc.P_FLOOR]
    return str(mc.build(body, mc._body_wt(body), 1))


def ammonia_table(papers: str) -> int:
    """9-ammonia-table: make_ammonia_table.main with its PDF at the stamped path ($NEARSTARS_PAPERS/…). The builder
    itself reads ROOT/docs/phase3/_papers (the tree's own cache); engine/ is not changed by the sg-gate prereg (§1.1),
    so the census points the module's PDF constant at the file the stamp hashes (note 1 §10)."""
    import os
    sys.path.insert(0, str(ENGINE / "tools"))
    import make_ammonia_table as m
    m.PDF = os.path.join(papers, os.path.basename(m.PDF))
    return m.main() or 0
