#!/usr/bin/env bash
# 영어 원본과 ko/ 한글 미러의 누락·구버전 상태를 확인하는 도구

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

# Exclusion patterns — files in mirrored trees that are not user-facing
# reference material and therefore do not need a Korean mirror.
should_exclude() {
  case "$1" in
    */_papers/*|*/_archive/*|*/_*) return 0 ;;
    */checklist.md|*/context-notes.md) return 0 ;;
  esac
  return 1
}

mirrored=()
mirrored+=("README.md")
while IFS= read -r f; do
  if should_exclude "$f"; then continue; fi
  mirrored+=("$f")
done < <(find docs plans -name "*.md" 2>/dev/null | sort)

missing=()
stale=()
ok=0
total=0

git_ts() {
  local out
  out=$(git log -1 --format=%ct -- "$1" 2>/dev/null || true)
  echo "${out:-0}"
}

for src in "${mirrored[@]}"; do
  total=$((total + 1))
  mirror="ko/$src"
  if [ ! -f "$mirror" ]; then
    missing+=("$src")
    continue
  fi
  src_ts=$(git_ts "$src")
  mir_ts=$(git_ts "$mirror")
  # Only flag stale when both files are committed and src is newer.
  # Treat uncommitted mirrors (mir_ts=0) as up-to-date — the working
  # copy is the latest.
  if [ "$src_ts" -gt 0 ] && [ "$mir_ts" -gt 0 ] && [ "$src_ts" -gt "$mir_ts" ]; then
    stale+=("$src")
  else
    ok=$((ok + 1))
  fi
done

echo "Bilingual mirror check"
echo "======================"
echo "English docs scanned: $total"
echo "Mirrors OK:           $ok"

if [ ${#missing[@]} -gt 0 ]; then
  echo ""
  echo "Missing Korean mirrors (${#missing[@]}):"
  for f in "${missing[@]}"; do
    echo "  + $f  →  ko/$f"
  done
fi

if [ ${#stale[@]} -gt 0 ]; then
  echo ""
  echo "Potentially stale mirrors (${#stale[@]}) — English committed more recently:"
  for f in "${stale[@]}"; do
    echo "  ~ $f  vs  ko/$f"
  done
fi

if [ ${#missing[@]} -gt 0 ] || [ ${#stale[@]} -gt 0 ]; then
  echo ""
  echo "To fill gaps: ask Claude to mirror the listed files into ko/<same-path>." >&2
  exit 1
fi

echo ""
echo "All mirrors up to date."
