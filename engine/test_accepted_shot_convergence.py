# C139 — 받아들인 적분의 수렴만 AND 에 남는가: 기록기 단위 검사와, 받아들인 적분 안의 False 는 남는다는 음성 대조
"""python3 engine/test_accepted_shot_convergence.py   (prereg-c139-accepted-shot-convergence a5b910cb, checks 2–3)

Unit (convergence.Trace):
- without `settle` the trace is what today's sequential `note` calls give (shots merged as they end);
- `settle` keeps only the accepted shot in the AND; the others' False go to `trial_false`, their invalid brackets to
  `trial_invalid`; records outside any shot stay in the AND;
- a reused structure id resolves to the **last** shot with it; an unmatched id moves nothing;
- integrations do not nest.
Engine (negative control, check 3): a probe site noted False in **every** integration of a solve stays in
`unconverged_solvers` and makes `values["converged"]` False, because the accepted integration is one of them. The
positive side (a False only in trial integrations leaves the AND) is the map census of check 2; here a probe noted
True everywhere must leave no trace in either column.
"""
from __future__ import annotations

import contextlib
import io
import sys

import convergence
import interior

fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


def legacy(events):
    tr = convergence.Trace()
    for site, conv, valid in events:
        tr.note(site, conv, True, valid)
    return tr


# ── unit: unsettled == today's sequential notes ──
with convergence.start() as tr:
    convergence.note("outer.a", True)
    with convergence.shot() as h:
        convergence.note("x", False, bracket_valid=False)
        convergence.note("y", None)
        h[0] = 101
    convergence.note("outer.b", None)
    with convergence.shot() as h:
        convergence.note("x", True)
        convergence.note("y", True)
        h[0] = 102
ref = legacy([("outer.a", True, None), ("x", False, False), ("y", None, None), ("outer.b", None, None),
              ("x", True, None), ("y", True, None)])
check((tr.converged, tr.unconverged_sites, tr.bracket_invalid_sites, tr.no_criterion_sites)
      == (ref.converged, ref.unconverged_sites, ref.bracket_invalid_sites, ref.no_criterion_sites),
      f"unsettled trace differs from sequential notes: {tr.sites} vs {ref.sites}")

# ── unit: settle keeps the accepted shot only ──
moved = tr.settle(102, 0)
check(moved, "settle did not find shot 102")
check(tr.unconverged_sites == [] and tr.converged is True, f"after settle the AND still holds {tr.unconverged_sites}")
check(sorted(tr.trial_false) == ["x"] and sorted(tr.trial_invalid) == ["x"] and tr.bracket_invalid_sites == [],
      f"trial columns wrong: {tr.trial_false} {tr.trial_invalid} {tr.bracket_invalid_sites}")
check(tr.sites.get("outer.a") is True and "outer.b" in tr.sites, "records outside shots left the AND")

# ── unit: accepted shot's False stays; id reuse → last; unmatched → nothing ──
with convergence.start() as tr:
    for sid, conv in ((7, True), (7, False)):           # same id twice — the last one is the accepted structure
        with convergence.shot() as h:
            convergence.note("z", conv)
            h[0] = sid
    check(tr.settle(7, 0) and tr.unconverged_sites == ["z"], f"id reuse: last shot not taken ({tr.unconverged_sites})")
with convergence.start() as tr:
    with convergence.shot() as h:
        convergence.note("w", False)
        h[0] = 5
    check(not tr.settle(999, 0) and tr.unconverged_sites == ["w"], "unmatched settle moved records")
with convergence.start():
    try:
        with convergence.shot():
            with convergence.shot():
                pass
        check(False, "nested shots were allowed")
    except AssertionError:
        pass

# ── engine: negative control on a fast rocky solve ──
real = interior._integrate_raw


def solve_with_probe(conv):
    def probed(*a, **k):
        convergence.note("c139.probe", conv)
        return real(*a, **k)
    interior._integrate_raw = probed
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return interior.solve(1.0, body_class="rocky", core_mass_fraction=0.325, potential_temperature=1600.0)
    finally:
        interior._integrate_raw = real


neg = solve_with_probe(False).values
check("c139.probe" in neg["unconverged_solvers"] and neg["converged"] is False,
      f"negative control: a False inside the accepted integration left the AND ({neg['unconverged_solvers']})")
pos = solve_with_probe(True).values
check("c139.probe" not in pos["unconverged_solvers"] + pos["trial_unconverged"],
      "a probe that always closed left a trace")
print(f"negative control: probe False in every integration → unconverged_solvers {neg['unconverged_solvers']} · "
      f"converged {neg['converged']} · trial_unconverged {neg['trial_unconverged']}")

for f in fails:
    print("FAIL", f)
print("test_accepted_shot_convergence:", "FAIL" if fails else "ok")
sys.exit(1 if fails else 0)
