#!/bin/sh
# 위키 자동화 1회 설치 스크립트
#   - git pre-commit 훅: scripts/wiki/precommit-ingest.sh를 .git/hooks/pre-commit으로 심볼릭 링크
#   - 주간 lint cron: 사용자가 직접 crontab -e 로 추가하도록 안내 출력
#
# 사용: ./scripts/wiki/install.sh

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

HOOK_SRC="$REPO_ROOT/scripts/wiki/precommit-ingest.sh"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit"

# 1. pre-commit 훅 설치
if [ -e "$HOOK_DST" ] && [ ! -L "$HOOK_DST" ]; then
  echo "WARNING: $HOOK_DST already exists as a regular file."
  echo "  Backing up to ${HOOK_DST}.backup before installing."
  mv "$HOOK_DST" "${HOOK_DST}.backup"
fi

ln -sf "../../scripts/wiki/precommit-ingest.sh" "$HOOK_DST"
chmod +x "$HOOK_SRC"
echo "installed: pre-commit hook → $HOOK_DST"

# 2. 주간 lint cron 안내
chmod +x "$REPO_ROOT/scripts/wiki/cron-weekly-lint.sh"
cat <<'EOF'

==========================================
주간 lint cron 설치 (수동)
==========================================

1) crontab -e
2) 다음 라인 추가 (매주 일요일 03:00 KST 실행):

   0 3 * * 0 /Users/vana/Desktop/claude/scripts/wiki/cron-weekly-lint.sh

3) 저장 후 확인: crontab -l

cron이 안 돌면 launchd plist도 가능 — 안내는 SKILL.md §8.3 참조.

==========================================
설치 후 검증
==========================================

  # pre-commit 훅 동작 확인 (실제 commit 안 들어감 — dry-run)
  echo "# test" > /tmp/wiki-hook-test.md
  cp /tmp/wiki-hook-test.md docs/_hook-test.md
  git add docs/_hook-test.md
  .git/hooks/pre-commit         # 훅 직접 호출
  git reset HEAD docs/_hook-test.md
  rm docs/_hook-test.md

훅이 "claude CLI not in PATH" 메시지를 내면 macOS launchd 컨텍스트에서 claude 인증/경로 문제가 있다는 뜻 — SKILL.md §8.4 참조.
EOF
