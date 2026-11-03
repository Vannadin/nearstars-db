# 부호 검사의 NaN 규칙 — NaN 은 부호가 아니다(검사·괄호), 이분은 NaN 끝으로 옮기지 않는다(거절); 감사용 계수기 (engine/rootfind.py 와 같은 규칙)
"""The NaN rule for solver's sign tests, brackets and bisections (directing / c8 7335778d fold-b1; artifacts ea-jobA
pc/ea-f13b/nanbisect/plan.md; 68 pc/audit68-nanbisect 4911b80e). solver imports nothing from engine, so the rule's
helpers live here too (engine's are in engine/rootfind.py).

- A NaN is never a sign: `nan_free(*fs)` guards a sign or bracket test.
- A bisection never moves an end onto a NaN: each site refuses through its existing path when a probe is NaN.
- With NS_NAN_AUDIT=<file>, every NaN refusal (by site) and every bisection's return ratio |f| at the returned bracket
  end / max |f| over its initial ends (values already in hand) is appended to the file as it happens, one JSON line
  per event; behaviour is unchanged either way. The ratio watches the jump class (a finite sign change across a
  discontinuity), which this rule does not close. solver keeps no module-level mutable state (A6), so nothing is
  held in memory: the events are few in solver (engine/rootfind.py, which sees millions, counts in a registered
  counter instead).
The finite arithmetic is untouched, so a run without a NaN is bit-identical."""
import json
import os
import sys

_AUDIT_FILE = os.environ.get("NS_NAN_AUDIT")


def _event(kind: str, site: str, value) -> None:
    with open(_AUDIT_FILE, "a") as fh:
        fh.write(json.dumps({"module": "solver.signs", "pid": os.getpid(), "argv": sys.argv[:3],
                             "nan": {site: 1} if kind == "nan" else {},
                             "residual": {site: [value]} if kind == "residual" else {}}) + "\n")


def nan_seen(site: str) -> None:
    """Count a NaN refused at `site` (audit only)."""
    if _AUDIT_FILE:
        _event("nan", site, None)


def residual(site: str, f_end: float, *f_init: float) -> None:
    """Record |f_end| / max |f_init| for a bisection's return at `site` (audit only)."""
    if _AUDIT_FILE:
        m = max((abs(x) for x in f_init if x == x), default=0.0)
        _event("residual", site, abs(f_end) / m if m else None)


def nan_free(*fs: float, site: str | None = None) -> bool:
    """True when none of fs is NaN: a sign or bracket test is decided only on values that have a sign."""
    ok = not any(f != f for f in fs)
    if not ok and site:
        nan_seen(site)
    return ok
