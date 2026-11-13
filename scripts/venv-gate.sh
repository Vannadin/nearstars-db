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

# ⚠ **3.12 이상으로만 짓는다** (오너 2026-11-13 f075fa770). 맥의 /usr/bin/python3 은 3.9 라 예전 venv 가 3.9 였다.
#   PY312 로 줄 수 있고, 없으면 아래 후보를 차례로 묻는다; 어느 것도 3.12 이상이 아니면 이름 붙은 거절.
_py=""
for c in "${PY312:-}" python3.12 /opt/homebrew/opt/python@3.12/bin/python3.12 /usr/local/bin/python3.12 /usr/bin/python3 python3; do
  [ -n "$c" ] || continue
  command -v "$c" >/dev/null 2>&1 || continue
  if "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then _py=$(command -v "$c"); break; fi
done
[ -n "$_py" ] || { echo "  [FAIL] no Python 3.12 or newer found (PY312, python3.12, /usr/bin/python3) — the gate venv is 3.12 only"; exit 2; }
echo "  building $VENV from $_py ($("$_py" --version 2>&1))"
"$_py" -m venv "$VENV"
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
# ⚠ **무엇으로 지었는지를 venv 안에 적는다** (핀 출처). 게이트의 핀 가드는 경로만 보므로
#   «핀이 걸렸다» 는 알아도 «이 선언으로 지은 핀이다» 는 모른다. 이 한 줄이 그 칸을 채운다.
#   ⚠ 기록은 **venv 안**에 둔다 — 이것은 트리가 아니라 그 venv 를 기술하는 사실이고,
#   `engine/.venv-gate` 는 gitignore 된다.
git hash-object "$REQ" > "$VENV/gate-requirements.blob"
echo "  [OK] $VENV · $REQ blob $(cat "$VENV/gate-requirements.blob")"
