# 착지당 한 번 도는 C¹ 전체 꺾임 조사 — 시험 묶음 밖(파일 이름이 test_ 아님), PC 회차가 기록마다 한 단계로 돌리고 위반이 있으면 실패로 끝남
"""The full kink scan (68 ruling 4: «the full scan as a HEAVY test per landing on the PC», i.e. once per landing).

It ran as test_assemblage_c1's test_kinks_named_and_bounded_full under NEARSTARS_HEAVY; evc_acceptance.physics() sets
that flag, so the ~75 min scan ran inside each of the round's three EVC suites (directing 10-18). It is now outside the
suite (this file is not a test_*.py), and the round runs it once per record as its own phase-1 task: the task fails
(exit 1) on any kink outside the named classes or above their bounds, which STOPs the round. The in-suite subset
(test_kinks_named_and_bounded_subset) stays in every suite.

Run from the worktree root:  <solver venv>/python -m solver.tests.landing_kink_scan OUT.json [record …]
(default: the three SLB records). OUT.json gets {record: {"kinks": n, "violations": [...]}}."""
import json
import sys

from solver import material_registry as mr
from solver.tests import kinkscan as ks
from solver.tests.test_assemblage_c1 import RECORDS, _shipped, _view


def full(reg, rid):
    """The full scan of one record: every line kinkscan.full_lines gives, in both directions; (kinks, violations). The
    «interior-end hold (b′)» class is counted apart (ks.violations_with_hold, full=True): an accepted member is a
    violation above HOLD_BOUND. A member failing C⁰ at t_e is an edge T-end step: when every field failing there is in
    E26's census (ks.e26_census_match, 68 §9 with amendment 1) it leaves the generic count as «E26 (census)», counted and
    printed; otherwise it is one violation, its own (b′) entry, not also a generic one (68 README §15, §18, §20 B1)."""
    v = _view(reg, rid)
    ts, ps = ks.full_lines(v)
    kinks = ks.scan(v, p_lines=ts, t_lines=ps)
    members = ks.holds(v, kinks)
    e26, miss = [], []
    for k, h in members[0]:
        if h["c0"]["ok"]:
            continue
        bad = [f["field"] for f in h["c0"]["fields"] if not f["ok"]] or ["rho", "dtdp", "c_p"]
        out = [f for f in bad if f == "rho" or ks.e26_census_match(v, {**k, "field": f, "T": h["t_e"]},
                                                                    end=(h["curve"], h["side"])) is None]
        (miss if out else e26).append((k, h, out))
    viol, _m = ks.violations_with_hold(v, kinks, rid, full=True, members=members, apart=[k for k, _h, _o in e26 + miss])   # each counted once
    for k, h, out in miss:
        viol.append({**k, "class": ks.HOLD, "c0_fails_outside_e26": out, "curve": h["curve"], "t_e": h["t_e"]})
    print(f"{rid}: (b′) members {len(members[0])}, accepted {sum(h['accepted'] for _k, h in members[0])}, "
          f"E26 (census) {len(e26)}, C⁰-failing outside the census {len(miss)}", flush=True)
    return kinks, viol


def main(argv):
    out, rids = argv[0], argv[1:] or list(RECORDS)
    if not _shipped():
        print("STOP: the tip ships no SLB records with their tables; the landing scan has nothing to read")
        return 2
    reg = mr.load()
    res, bad = {}, 0
    for rid in rids:
        if rid not in RECORDS:
            print(f"STOP: {rid} is not an SLB record ({', '.join(RECORDS)})")
            return 2
        kinks, viol = full(reg, rid)
        res[rid] = {"kinks": len(kinks), "violations": [repr(x) for x in viol]}
        bad += len(viol)
        print(f"{rid}: {len(kinks)} kinks, {len(viol)} outside the named classes or above their bounds", flush=True)
    with open(out, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
