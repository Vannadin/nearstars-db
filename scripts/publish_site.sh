#!/usr/bin/env bash
# 빌드된 docs/ 트리를 gh-pages 브랜치로 동기화·커밋·푸시하는 사이트 퍼블리셔
#
# 빌드는 하지 않는다. run_pipeline.sh 와 각 빌더(build_docs.py, build_html.py,
# build_phase4_html.py …)가 docs/ 를 갱신한 뒤에 이 스크립트를 부른다.
#
#   scripts/publish_site.sh            # 동기화 → 커밋 → push
#   scripts/publish_site.sh --no-push  # 동기화 → 커밋까지만
#
# gh-pages 는 고아 브랜치이고 그 히스토리는 버려도 되는 빌드 로그다.
# main 은 소스만 들고 있으며 생성 HTML 을 추적하지 않는다.

set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$(pwd)"

SITE_WT="${NEARSTARS_SITE_WORKTREE:-$REPO/../NearStars-wt/site}"
BRANCH=gh-pages
PUSH=1

for arg in "$@"; do
  case "$arg" in
    --no-push) PUSH=0 ;;
    *) echo "알 수 없는 인자: $arg" >&2; exit 2 ;;
  esac
done

if [ ! -d "$REPO/docs" ]; then
  echo "ERROR: docs/ 가 없습니다. 저장소 루트에서 실행하세요." >&2
  exit 1
fi

# 생성 HTML 은 main 에서 추적하지 않는다. 갓 클론한 트리에는 없다는 뜻이고,
# 그 상태로 rsync --delete 를 돌리면 사이트를 통째로 지운다. 빌드 여부를
# 대표 산출물로 확인하고, 없으면 멈춘다.
for probe in index.html reports.html wiki/index.html; do
  if [ ! -f "$REPO/docs/$probe" ]; then
    echo "ERROR: docs/$probe 가 없습니다 — 사이트가 빌드되지 않은 트리입니다." >&2
    echo "       먼저 ./run_pipeline.sh 와 각 빌더를 돌린 뒤 다시 실행하세요." >&2
    exit 1
  fi
done

# 사이트 워크트리가 없으면 붙여준다 (브랜치는 이미 있어야 한다).
if [ ! -e "$SITE_WT/.git" ]; then
  echo "사이트 워크트리가 없습니다. 붙이는 중 → $SITE_WT"
  git worktree add "$SITE_WT" "$BRANCH"
fi

git -C "$SITE_WT" checkout -q "$BRANCH"
git -C "$SITE_WT" pull -q --ff-only origin "$BRANCH" 2>/dev/null || true

# 제외는 손으로 적은 짧은 deny 목록이다. main 의 .gitignore 에서 뽑아 쓰던
# 판본이 있었는데, 생성 사이트 HTML 이 .gitignore 에 등재되는 순간 그 목록이
# "퍼블리시할 파일 전부"가 되어 사이트가 영영 갱신되지 않았다. .gitignore 는
# "git 이 추적하지 않는 것"이고 여기 필요한 건 "공개하면 안 되는 것"이라,
# 두 목록은 겹치지 않는다.
#
# _papers/ 는 ADS/arXiv 논문 전문 캐시다. 저작권물이고, 첫 시도에서 실제로
# 공개 사이트로 새어 나갔다. 아래 하드 가드가 두 번째 그물이다.
EXCL=$(mktemp)
trap 'rm -f "$EXCL"' EXIT
printf '.git\n.gitignore\n.DS_Store\n_papers/\n' > "$EXCL"

echo "동기화: docs/ → $BRANCH"
rsync -a --delete --exclude-from="$EXCL" "$REPO/docs/" "$SITE_WT/"

# 하드 가드. 제외가 어떤 이유로든 실패하면 여기서 멈춘다.
for forbidden in _papers .DS_Store; do
  if find "$SITE_WT" -name "$forbidden" -not -path '*/.git/*' | grep -q .; then
    echo "ERROR: '$forbidden' 가 사이트 트리에 있습니다. 커밋을 중단합니다." >&2
    exit 1
  fi
done

if [ -z "$(git -C "$SITE_WT" status --porcelain)" ]; then
  echo "변경 없음. 사이트는 이미 최신입니다."
  exit 0
fi

CHANGED=$(git -C "$SITE_WT" status --porcelain | wc -l | tr -d ' ')
SRC=$(git -C "$REPO" rev-parse --short HEAD)

git -C "$SITE_WT" add -A
git -C "$SITE_WT" commit -q -m "site: rebuild from ${SRC} (${CHANGED} files)"
echo "커밋 완료: ${CHANGED}개 파일, 소스 ${SRC}"

if [ "$PUSH" -eq 1 ]; then
  git -C "$SITE_WT" push -q origin "$BRANCH"
  echo "push 완료 → origin/$BRANCH"
  echo "사이트: https://vannadin.github.io/nearstars-db/"
else
  echo "--no-push 지정됨. push 는 건너뜁니다."
fi
