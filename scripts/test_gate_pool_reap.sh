#!/usr/bin/env bash
# 천장을 넘긴 풀 워커를 죽이고 거두어 rc·출력·[TIME] 이 로그에 남는지 묻는 시험 (go-live s4r 2b)
# check.sh 의 풀 함수 본문을 그대로 뽑아 가짜 스풀에서 돌린다 — 사본이 아니라 실제 코드를 시험한다.
set -u
here=$(cd "$(dirname "$0")" && pwd)
src=${GATE_CHECK_SH:-$here/check.sh}          # 변형 시험이 다른 check.sh 를 넘길 수 있다
fn() { awk -v n="$1" '$0 ~ "^"n"\\(\\) \\{" {f=1} f{print} f&&/^}/{exit}' "$src"; }
body=""
for f in _measure _cost_fields _gate_bound _pool_drain _pool_alive _tree_leaves _pool_reap_live _pool_barrier _pool_launch; do
  b=$(fn "$f"); [ -n "$b" ] || { echo "  [FAIL] check.sh 에서 $f 를 못 찾음"; exit 1; }
  body="$body
$b"
done
fmt=$(grep -m1 '^_GNU_TIME_FMT=' "$src"); [ -n "$fmt" ] || { echo "  [FAIL] _GNU_TIME_FMT 없음"; exit 1; }
py=${GATE_PY:-python3}
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
mark="reap-probe-$$"
# 시나리오: 빠른 워커 하나(정상) + 조용히 오래 도는 워커 하나(flush 없이 한 줄 찍고 잠). 천장 2 s, 유예 10 s.
cat > "$work/run.sh" <<RUN
set -u
$fmt
_GATE_OS=\$(uname -s); _GATE_PERF=""; TMPDIR="$work"
GATE_POOL=4; GATE_BARRIER_MAX=2; GATE_REAP_GRACE=10
_pool_dir=\$(mktemp -d "$work/gate-pool.XXXXXX"); _pool_seq=0; _pool_launched=0; _pool_drained=0; _pool_names=""
_gate_max_s=0; _gate_max_name=""; fail=0
$body
_pool_launch test_fast "$py" -c 'print("fast-done")'
_pool_launch test_slow "$py" -c 'import time; print("partial-$mark"); time.sleep(600)  # $mark'
t0=\$SECONDS
_pool_barrier; _pool_drain
echo "RESULT fail=\$fail launched=\$_pool_launched drained=\$_pool_drained secs=\$((SECONDS - t0))"
RUN
# 파일로 받고 시한을 둔다 — 거두지 않는 check.sh 에서는 고아 워커가 파이프를 쥐어 `$(...)` 가 600 s 를 기다린다.
bash "$work/run.sh" > "$work/out.txt" 2>&1 &
runner=$!
waited=0
while kill -0 "$runner" 2>/dev/null && [ "$waited" -lt 40 ]; do sleep 0.5; waited=$((waited + 1)); done
hung=0; kill -0 "$runner" 2>/dev/null && hung=1
sleep 0.5
left=$(pgrep -f "#[ ]$mark" | wc -l | tr -d ' ')
for q in $(pgrep -f "#[ ]$mark"); do kill -KILL "$q" 2>/dev/null; done      # 이 시험이 띄운 표지 프로세스만
[ "$hung" = "1" ] && { kill -KILL "$runner" 2>/dev/null; wait "$runner" 2>/dev/null; }
out=$(cat "$work/out.txt")
fails=0
check() { if eval "$2"; then echo "  [PASS] $1"; else echo "  [FAIL] $1"; fails=$((fails+1)); fi; }
has() { printf '%s\n' "$out" | grep -qF -- "$1"; }
check "빠른 워커의 출력이 로그에 있음" 'has "fast-done"'
check "천장 FAIL 이 이름을 댐" 'has "pool_barrier_deadline" && has "아직 살아 있는 이름: test_slow"'
check "죽인 워커의 flush 안 된 출력이 남음 (PYTHONUNBUFFERED)" 'has "partial-$mark"'
check "죽인 워커의 비0 rc 가 로그에 있음" 'has "[FAIL] test_slow — 비0 종료"'
check "죽인 워커의 [TIME] 이 로그에 있음 (time 이 제 파일을 씀)" 'has "[TIME] test_slow"'
check "띄움 = 거둠, fail=1" 'has "RESULT fail=1 launched=2 drained=2"'
check "천장 + 유예 안에 끝남" '[ "$(printf "%s\n" "$out" | sed -n "s/.*secs=\([0-9]*\).*/\1/p")" -le 14 ]'
check "고아 프로세스 없음" '[ "$left" = "0" ]'
check "시나리오가 20 s 안에 끝남 (멈추지 않음)" '[ "$hung" = "0" ]'
[ "$fails" -eq 0 ] || printf '%s\n' "$out" | sed 's/^/    | /'
[ "$fails" -eq 0 ] && echo "  test_gate_pool_reap — 모두 통과" || echo "  test_gate_pool_reap — 실패 $fails"
exit "$fails"
