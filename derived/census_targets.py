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



def fall_sets_sweep() -> int:
    """7-fall-sets: the build's record × region sweep (fall_sets.engine_census, the `_CENSUS_MAIN` child) on the three
    shipped records. The check (test_fall_set_stamp) re-hashes and never runs it, so without this the sweep's child
    loads would go unjudged (68 on db1a128b)."""
    sys.path.insert(0, str(ENGINE.parent))
    from solver import fall_sets as fs
    cen = fs.engine_census(("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022"),
                           fs.directory())
    print(f"sweep: {len(cen['engine'])} engine files loaded in the child")
    return 0
