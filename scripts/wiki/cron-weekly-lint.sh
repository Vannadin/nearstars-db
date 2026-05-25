#!/bin/sh
# 주간 위키 lint cron 스크립트 — 매주 일요일 03:00 실행 권장

REPO_ROOT="/Users/vana/Desktop/claude"
LOG="$REPO_ROOT/.wiki-lint-cron.log"

cd "$REPO_ROOT" || exit 1

if ! command -v claude >/dev/null 2>&1; then
  echo "[$(date -Iseconds)] cron-weekly-lint: claude CLI not in PATH" >> "$LOG"
  exit 0
fi

echo "[$(date -Iseconds)] cron-weekly-lint: starting" >> "$LOG"
claude -p "/wiki-lint" >> "$LOG" 2>&1
echo "[$(date -Iseconds)] cron-weekly-lint: done (rc=$?)" >> "$LOG"
