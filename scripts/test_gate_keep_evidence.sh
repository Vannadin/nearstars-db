#!/usr/bin/env bash
# 게이트 증거(읽기·질량 기록)가 게이트 뒤에도 남는지 묻는 시험 — check.sh 의 _keep_evidence 본문을 그대로 뽑아 두 갈래를 실제로 돌림 (s4r2 EVIDENCE-SURVIVAL)
# 목 없음: 진짜 임시 파일과 진짜 디렉터리(있는 것 · 없는 것)로 복사·삭제·FAIL 을 확인한다. 끝에 check.sh 가 두 기록 모두 이 함수로 넘기는지 본다.
set -u
here=$(cd "$(dirname "$0")" && pwd)
fn=$(awk '/^_keep_evidence\(\) \{/{f=1} f{print} f&&/^\}$/{exit}' "$here/check.sh")
[ -n "$fn" ] || { echo "  [FAIL] check.sh 에서 _keep_evidence 를 못 찾음"; exit 1; }
box=$(mktemp -d); trap 'rm -rf "$box"' EXIT
fails=0
check() { if eval "$2"; then echo "  [PASS] $1"; else echo "  [FAIL] $1"; fails=$((fails+1)); fi; }

# 갈래 1: GATE_LOGS_DIR 가 있음 → 사본이 남고 임시 파일은 지워지며 fail 은 그대로 0
mkdir "$box/logs"; printf 'r1\n' > "$box/reads.tmp"
out1=$(bash -c "fail=0; GATE_LOGS_DIR='$box/logs'; $fn
_keep_evidence '$box/reads.tmp' reads-abc.jsonl; echo \"fail=\$fail\"")
check "있는 디렉터리: 사본이 같은 내용으로 남음" '[ "$(cat "$box/logs/reads-abc.jsonl" 2>/dev/null)" = r1 ]'
check "있는 디렉터리: 임시 파일은 지워짐" '[ ! -e "$box/reads.tmp" ]'
check "있는 디렉터리: fail=0 · [기록] 줄" 'printf "%s\n" "$out1" | grep -qx "fail=0" && printf "%s\n" "$out1" | grep -q "\[기록\] 게이트 증거 보존 — $box/logs/reads-abc.jsonl"'

# 갈래 2: GATE_LOGS_DIR 가 없음 → 이름 붙은 FAIL, fail=1, 임시 파일은 남고, 디렉터리를 만들지 않음
printf 'm1\n' > "$box/mass.tmp"
out2=$(bash -c "fail=0; GATE_LOGS_DIR='$box/nope'; $fn
_keep_evidence '$box/mass.tmp' mass-abc.jsonl; echo \"fail=\$fail\"")
check "없는 디렉터리: gate_evidence 실패 줄이 이름과 남은 경로를 댐" 'printf "%s\n" "$out2" | grep -q "\[FAIL\] gate_evidence — mass-abc.jsonl not kept: GATE_LOGS_DIR=$box/nope .*the log stays at $box/mass.tmp"'
check "없는 디렉터리: fail=1" 'printf "%s\n" "$out2" | grep -qx "fail=1"'
check "없는 디렉터리: 임시 파일은 그대로 남음" '[ "$(cat "$box/mass.tmp" 2>/dev/null)" = m1 ]'
check "없는 디렉터리: 디렉터리를 만들지 않음" '[ ! -e "$box/nope" ]'

# check.sh 가 두 기록을 모두 이 함수로 넘기고, 옛 «지우기만» 줄이 없는가
check "check.sh: 읽기·질량 기록 둘 다 _keep_evidence 로" '[ "$(grep -cE "^  _keep_evidence \"\\\$GATE_(READS|MASS)_LOG\"" "$here/check.sh")" = 2 ]'
check "check.sh: 기록을 바로 지우는 rm -f 줄 없음" '! grep -qE "^  rm -f \"\\\$GATE_(READS|MASS)_LOG\"" "$here/check.sh"'

[ "$fails" -eq 0 ] && echo "  test_gate_keep_evidence — 모두 통과" || echo "  test_gate_keep_evidence — 실패 $fails"
exit "$fails"
