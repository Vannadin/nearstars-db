# 기준 단열선 표의 다시 짓기 대조가 낡은 표를 잡는가 — C148 덧붙임 2 의 음성 대조(n2-b) · 차선이 그 단계를 고르는가(n2-e)
"""C148 post-freeze note 2, acceptances n2-b and n2-e.

    python3 engine/test_reference_adiabats.py

- 88a5931e's table (anchored at Earth's pre-C157 CMB, ~20 K off) fed to the generator's own `check()` must report
  DIFFERS on every machine. The test never re-implements the comparison, so a broken `--check` fails it.
- The committed table must report identical, judged on the reference machine only (`REFERENCE_MACHINE`); elsewhere
  it is a record (the Mac rebuild differs from the PC table by ≤ 2.7e-9 K in `t`, n2-c).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
import reference_adiabats as ra   # noqa: E402

STALE_SHA = "88a5931e"            # C153 §1.4 의 마지막 재빌드 — C157 이 지구 CMB 를 −20.39 K 옮기기 전
fails: list[str] = []


def ok(cond: bool, label: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        fails.append(label)


def main() -> int:
    stale = subprocess.run(["git", "show", f"{STALE_SHA}:engine/reference_adiabats.json"], cwd=HERE,
                           capture_output=True, text=True, check=True).stdout
    ok(not ra.check(stale), f"n2-b: {STALE_SHA}'s table (pre-C157 Earth anchor) → check() DIFFERS on this tree")
    sys.path.insert(0, str(HERE.parent / "scripts"))
    import gate_step_inputs as gsi
    hit, _missing = gsi.also(["engine/interior.py"], gsi.load(), gsi.step_names(), gsi.quick_steps())
    ok("engine/tools/reference_adiabats.py --check" in hit,
       "n2-e: a lane that passes only engine/interior.py still runs the --check step (its declared reads)")
    here = ra.machine()
    same = ra.check()
    if here == ra.REFERENCE_MACHINE:
        ok(same, f"n2-b: the committed table → check() identical on the reference machine ({here})")
    else:
        print(f"  [기록] the committed table → check() {'identical' if same else 'DIFFERS'} on {here} "
              f"(judged only on {ra.REFERENCE_MACHINE}, C148 note 2)")
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
