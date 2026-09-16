#!/usr/bin/env bash
# 게이트가 쓰는 단 하나의 venv 를 engine/requirements.txt 에서 만든다
#
# ⚠ **게이트는 이 venv 의 python3 을 경로로 부른다** (`scripts/check.sh` 첫머리). 그 전에는
#   맨 `python3` 이었고 어느 파이썬인지는 호출자의 PATH 가 정했다. BurnMan 이 런타임
#   의존이 된 뒤로 그 느슨함은 «기계마다 다른 판정» 이 된다.
# ⚠ **목록은 engine/requirements.txt 하나다.** 예전에는 BurnMan 이 자기 venv 를 따로 썼는데
#   (`engine/requirements-burnman.txt`), 그 분리의 근거는 «엔진은 BurnMan 을 import 하지
#   않는다» 였다. C74 가 그 전제를 끝냈다.
#
#     scripts/venv-gate.sh          # 만들고 버전을 인쇄한다
#
# 만든 뒤 다섯을 인쇄한다 — 이 venv 가 무엇인지 말하는 것은 주석이 아니라 그 인쇄다.
set -eu
cd "$(git rev-parse --show-toplevel)"

VENV="engine/.venv-gate"
REQ="engine/requirements.txt"

[ -f "$REQ" ] || { echo "  [FAIL] $REQ 가 없다"; exit 2; }

/usr/bin/python3 -m venv "$VENV"
"$VENV/bin/python3" -m pip install --disable-pip-version-check --quiet -r "$REQ"

"$VENV/bin/python3" - <<'PY'
import sys
print(f"  python      {sys.version.split()[0]}")
for name in ("burnman", "numpy", "mpmath", "yaml", "psutil"):
    try:
        mod = __import__(name)
        print(f"  {name:11s} {getattr(mod, '__version__', '?')}")
    except Exception as exc:                       # noqa: BLE001
        print(f"  {name:11s} 없음 — {type(exc).__name__}: {exc}")
        raise SystemExit(2)
PY
echo "  [OK] $VENV"
