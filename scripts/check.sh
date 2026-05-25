#!/usr/bin/env bash
# 릴리스 전 일괄 건강 점검 — 수동 실행 전용, 훅 미설치
set -u
cd "$(git rev-parse --show-toplevel)"
fail=0

echo "── 1. 스키마 검증 (db/systems/*.json + curated) ──"
python3 scripts/pipeline/validate.py || fail=1

echo ""
echo "── 2. 영한 미러 상태 (missing = 실패, stale = 경고) ──"
# check-mirrors.sh 는 missing 과 stale 둘 다 exit 1 로 묶음.
# 이 PR 시점에서는 stale 26+ 건이 별도 작업이므로 경고로 강등.
mirror_out=$(./scripts/check-mirrors.sh 2>&1) || true
echo "$mirror_out"
if echo "$mirror_out" | grep -q "Missing Korean mirrors"; then fail=1; fi

echo ""
echo "── 3. Markdown dead-link 스캔 ──"
python3 scripts/check_dead_links.py || fail=1

echo ""
echo "── 4. 컨벤션 점검 ──"
# 4a. 같은 라이브 스킬이 두 트리에 동시 존재 금지
for d in .claude/skills/*/; do
  name=$(basename "$d")
  if [ -d ".agents/skills/$name" ]; then
    echo "  [FAIL] skill duplicated: .claude/skills/$name vs .agents/skills/$name"
    fail=1
  fi
done
# 4b. phase3 시스템 디렉토리는 snake_case (또는 _private / 알려진 topic)
for d in phase3/*/; do
  name=$(basename "$d")
  case "$name" in
    _*|html-pipeline|stability-sim) ;;  # allowlist
    *[-]*) echo "  [FAIL] phase3 non-snake_case system dir: $name"; fail=1 ;;
  esac
done
if [ $fail -eq 0 ]; then echo "  [PASS] 컨벤션 점검 통과"; fi

echo ""
echo "── 5. 경로 마이그레이션 잔여물 점검 ──"
patterns="alpha-cen-proxima-system|trappist-1-system|docs/wiki|llm-wiki|skills-lock"
hits=$(git grep -lE "$patterns" 2>/dev/null || true)
dup_skill=$(git grep -lE "\.agents/skills/(firefly-cfg|nearstars-phase3|find-skills|kopernicus-cfg|nearstars-add-star)/" 2>/dev/null || true)
if [ -n "$hits" ] || [ -n "$dup_skill" ]; then
  [ -n "$hits" ] && { echo "  옛 경로 잔존:"; echo "$hits" | sed 's/^/    /'; }
  [ -n "$dup_skill" ] && { echo "  옛 스킬 경로 잔존:"; echo "$dup_skill" | sed 's/^/    /'; }
  echo "  [FAIL] 위 파일을 점검하세요."
  fail=1
else
  echo "  [PASS] 경로 마이그레이션 잔여물 없음"
fi

echo ""
if [ $fail -eq 0 ]; then
  echo "──────── 모든 점검 통과 ────────"
else
  echo "──────── 일부 점검 실패 ────────"
fi
exit $fail
