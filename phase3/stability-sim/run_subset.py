# 한 시스템에서 지정한 행성만 남겨 안정성 적분(확정-행성 부분집합 variant용).
# 후보 포함 전체 배치가 불안정한 계(Barnard, AU Mic)의 "확정만" 안정 variant를
# 만든다. 전체(불안정) run 은 results/_observed/ 에, 이 부분집합(안정)은 results/ 에.
# 사용: python run_subset.py <system> <keep1,keep2,...>   (keep = 행성 짧은 이름)
import sys, os
from pathlib import Path
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "scripts"))
import rebound                                             # noqa: E402
import run as R                                            # noqa: E402

system = sys.argv[1]
keep = {k.strip() for k in sys.argv[2].split(",")}
YEARS = float(os.environ.get("SUBSET_YEARS", "1000000"))
SNAPS = int(os.environ.get("SUBSET_SNAPS", "200"))
INTEG = os.environ.get("SUBSET_INTEG", "whfast")
RES = Path(HERE) / "results"

sim, meta = R.build(system, None)
keep_full = {p["name"] for p in meta["planets"]
             if p["name"] in keep or p["name"].split()[-1] in keep}
drop = [p["name"] for p in meta["planets"] if p["name"] not in keep_full]
for nm in drop:
    sim.remove(nm)                                        # rebound 5.0: remove by name
meta["planets"] = [p for p in meta["planets"] if p["name"] in keep_full]
print(f"{system}: keep {sorted(keep_full)}  drop {drop}", flush=True)

report = R.run_integration(sim, meta, YEARS, SNAPS, INTEG)
judgment = R.verdict(report, YEARS)
R.print_report(meta, report, judgment)
R.save_results(system, meta, report, judgment, RES)
print("DONE", flush=True)
