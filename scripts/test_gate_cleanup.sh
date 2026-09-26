#!/usr/bin/env bash
# 게이트 시작의 옛 스크래치 정리 갈래가 도는 게이트의 풀 · 살아 있는 pid 디렉토리를 안 지우는지 묻는 시험
# check.sh 의 그 고리 본문을 그대로 뽑아 가짜 $TMPDIR 에서 돌린다 — 사본이 아니라 실제 코드를 시험한다.
set -u
here=$(cd "$(dirname "$0")" && pwd)
block=$(awk '/^  for old in "\$\{TMPDIR:-\/tmp\}"\/gate-\*; do$/{f=1} f{print} f&&/^  done$/{exit}' "$here/check.sh")
[ -n "$block" ] || { echo "  [FAIL] check.sh 에서 정리 고리를 못 찾음"; exit 1; }
fake=$(mktemp -d); trap 'rm -rf "$fake"' EXIT
sleep 300 & live=$!
dead=999999; while kill -0 "$dead" 2>/dev/null; do dead=$((dead-1)); done
mkdir "$fake/gate-pool.AbCdEf" "$fake/gate-deadbee-$live" "$fake/gate-deadbee-$dead"
TMPDIR="$fake" bash -c "$block" >/dev/null
kill "$live" 2>/dev/null; wait "$live" 2>/dev/null
fails=0
check() { if eval "$2"; then echo "  [PASS] $1"; else echo "  [FAIL] $1"; fails=$((fails+1)); fi; }
check "도는 게이트의 풀 디렉토리(gate-pool.XXXX)는 남음" '[ -d "$fake/gate-pool.AbCdEf" ]'
check "살아 있는 pid 의 스크래치는 남음" '[ -d "$fake/gate-deadbee-$live" ]'
check "죽은 pid 의 스크래치는 지워짐" '[ ! -e "$fake/gate-deadbee-$dead" ]'
[ "$fails" -eq 0 ] && echo "  test_gate_cleanup — 모두 통과" || echo "  test_gate_cleanup — 실패 $fails"
exit "$fails"
