#!/usr/bin/env bash
# 릴리스 전 일괄 건강 점검 — 수동 실행 전용, 훅 미설치
set -u
cd "$(git rev-parse --show-toplevel)"
fail=0
# ⚠ **비0 종료는 이름을 남긴다** (169 E). gate212 가 rc=1 로 끝났는데 로그 어디에도 `[FAIL]` 이
#   없었다 — 다섯 개의 `run.py` 중 하나가 조용히 1 을 돌려줬고, 어느 바디인지 스크래치를 다시
#   돌려서야 알았다. 시험 대부분은 자기 실패를 인쇄하지만 **인쇄하지 않는 것이 있고**, 그때
#   게이트가 «일부 점검 실패» 한 줄만 남기면 다음 사람은 처음부터 다시 찾아야 한다.
# ⚠ **169 F: 남은 자리를 전부 감쌌다.** `[FAIL]` 을 스스로 찍는 여덟 곳(자기 이름을 이미 인쇄하는
#   검사들)만 남기고, `|| fail=1` 로 조용히 끝나던 자리는 모두 이 헬퍼를 지난다. 불변식은 **세기가
#   아니라 «불리는 명령의 순서 있는 목록»** 이다 — 감싸면 `|| fail=1` 의 개수는 0 에 가까워지므로
#   그 수로는 아무 것도 못 지킨다. 이 커밋은 그 목록을 74 항목·같은 순서로 유지한다.
step() {                      # step <이름> <명령...>
  local name=$1; shift
  "$@" || { echo "  [FAIL] $name — 비0 종료 (이 단계가 fail=1 을 세웠다)"; fail=1; }
}
# 게이트 자신만 찍는 시작/종료선. 테스트 파일들이 찍는 "모두 통과" 와 겹칠 수 없는 형식이고,
# 종료선 없이는 "무엇이 언제 무슨 트리 위에서 끝났는지" 를 말할 수 없다 (2026-09-04, 두 좌석에서 같은 오독).
#
# ⚠ 그런데 그 규칙은 **통과 쪽에만** 적용된다. 판정은 비대칭이다 (2026-09-06):
#   - `rc=0` 은 끝까지 가야 안다. 본문의 "모두 통과" 는 판정이 아니다.
#   - **`[FAIL]` 한 줄은 나오는 즉시 "밀지 마라"를 확정한다.** 뒤에 무엇이 오든 rc 는 1 이다.
# 그러니 `[FAIL]` 을 보면 `rc=` 를 기다리지 말고 죽이고 고쳐라. 아래 블록 순서를 앞당긴 이유가
# 정확히 그것인데(문서 깨짐을 24분 뒤가 아니라 1분 안에 본다), gate135 에서 그 이득을 안 썼다 —
# 인용 링크 실패 두 줄이 로그 앞머리에 찍혀 있는 동안 24분을 기다렸다.
# ⚠ 단, 앞쪽 실패로 죽이면 뒤쪽 검사 결과는 못 본다. 고치고 다시 돌 때 또 걸릴 수 있음을 알고 하라.
# ── 인자: `--wiring` · `--from <sha>` · `--targeted` ───────────────────────────────────────
# 브리프마다 full 층(24분+)을 도는 것이 게이트 비용의 전부였다. 두 축을 나눈다.
#   `--from <sha>`         격리 실행. 그 sha 를 스크래치에 클론해 **그 안에서** 돈다. 워크트리 무접촉이므로
#                          ⚠ 이 모드에서는 «게이트 도는 동안 트리 쓰기 금지» 규칙이 해제된다 — 그것이 목적이다.
#   `--targeted`           표적 층. 13–14 의 물리 시험 중 **바뀐 경로에서 도출된 것만** 돈다.
#                          비교 base 는 인자가 아니라 도출값이다 (`origin/engine/prototype`).
# ⚠ **표적 시험을 사람이 고르게 만들지 않았다** (감사석 지적, 169). 위 18–21 줄의 기록된 결정이
#   «층은 바뀐 경로가 정한다, 사람이 «이번엔 문서만이야» 라고 판단하지 않는다» 이고, `--only <시험>` 은
#   바로 그 결정을 뒤집는다. 그래서 목록은 **diff 에서 도출**되고, 도출이 비면 full 로 되돌아간다.
# 운용: 브리프마다 `--from <sha> --targeted`, 푸시 직전(~10커밋)에만 `--from <sha>` full.
lane_req="full"
from_sha=""
# ⚠ base 는 **사람이 넣는 값이 아니다.** 푸시 tip 을 원격 이름으로 지목한다 — 격리 클론은 detached 라
#   `@{u}` 를 쓸 수 없고, base 를 인자로 열어 두면 "무엇에 대해 좁혔는지" 를 부르는 사람이 정하게 된다.
#   ⚠ 못 구하면 full 이다. 좁히기는 base 가 푸시 tip 일 때만 뜻이 있다.
# ⚠ **그 이름은 클론 안에서 다른 것을 가리킨다** (169, 첫 실행에서 잡혔다): 격리 클론의 `origin` 은
#   로컬 워크트리이므로 `origin/engine/prototype` 이 **푸시 tip 이 아니라 로컬 브랜치 tip** 을 가리킨다 —
#   즉 방금 커밋한 sha 자신이고, diff 는 0 경로가 되어 층이 조용히 «전부 문서» 로 좁혀진다. 그래서 base 는
#   진짜 원격이 보이는 **워크트리에서, 클론 전에** 도출해 sha 로 넘긴다 (`GATE_BASE_SHA`).
base_ref="${GATE_BASE_SHA:-origin/engine/prototype}"
while [ $# -gt 0 ]; do
  case "$1" in
    --wiring) lane_req="wiring"; shift ;;
    --from)
      from_sha="${2:-}"
      [ -n "$from_sha" ] || { echo "  [FAIL] --from 에 sha 가 없다"; exit 2; }
      shift 2 ;;
    --targeted) lane_req="targeted"; shift ;;   # ⚠ 인자를 받지 않는다 — base 는 도출값이다
    *) echo "  [FAIL] 모르는 인자: $1 (--wiring | --from <sha> | --targeted)"; exit 2 ;;
  esac
done

# ── 격리: sha 를 스크래치에 클론해 거기서 다시 자기를 부른다 ──────────────────────────────
# `git archive | tar -x` 로는 안 된다. 게이트 본문이 git 을 직접 쓴다 — 첫 줄의 `--show-toplevel`,
# 5번의 `git grep`, 9a–9e 의 `git ls-files`. 클론이어야 full 층이 격리에서 성립한다 (169, 실측).
# ⚠ 클론에는 gitignore 된 `docs/phase3/_papers` 심링크가 없다. 게이트가 그 이름을 쓰는 자리는
#   전부 **제외 목록**이므로(check_language · check_md_tables · check_md_dupes · check_site_links ·
#   build_sitemap · check_refs — 169 에서 여섯 다 확인) 없는 것이 검사를 바꾸지 않는다.
if [ -n "$from_sha" ] && [ "${GATE_ISOLATED:-}" != "1" ]; then
  tree_sha=$(git rev-parse --short "$from_sha" 2>/dev/null) || {
    echo "  [FAIL] 그런 sha 가 없다: $from_sha"; exit 2; }
  dest="${TMPDIR:-/tmp}/gate-$tree_sha-$$"     # 같은 sha 를 다시 돌리면 새 디렉토리 (pid)
  # ⚠ 시작할 때 **모든** sha 의 잔재를 지운다 (169 D, ③ — 예전엔 같은 sha 만 봤다). 둘은 건너뛴다:
  #   `GATE-FAILED` 를 든 것(그 실패를 재현하려고 남겼다)과 **아직 도는 pid 의 것**(디렉토리 이름의
  #   꼬리가 그 게이트의 pid 다 — 살아 있으면 지우는 순간 그 실행을 죽인다).
  for old in "${TMPDIR:-/tmp}"/gate-*; do
    [ -d "$old" ] || continue
    [ -e "$old/GATE-FAILED" ] && continue
    # ⚠ pid 는 재사용된다 — 남의 pid 가 우연히 이 이름과 같으면 지울 수 있는 디렉토리를 건너뛴다.
    #   그 실패는 **증거를 남기는 쪽**이므로 고치지 않는다 (감사석 판정, 170 F).
    old_pid=${old##*-}
    case "$old_pid" in
      ''|*[!0-9]*) ;;                       # pid 로 안 읽히면 지우지 않는다
      *) kill -0 "$old_pid" 2>/dev/null && continue ;;
    esac
    echo "  옛 스크래치 정리: $old (실패 표시 없음 · 도는 게이트 아님)"
    rm -rf "$old"
  done
  git clone -q --shared . "$dest" || { echo "  [FAIL] clone 실패"; exit 2; }
  git -C "$dest" checkout -q --detach "$tree_sha" || { echo "  [FAIL] checkout 실패"; exit 2; }
  # ⚠ 게이트 논리는 **지금 실행 중인 것**을 복사해 넣는다. sha 가 이 층들보다 앞설 수 있어서
  #   트리의 판을 부르면 인자를 모른다. 그래서 스크래치는 한 파일만 sha 와 다르고, 그 사실을 찍는다.
  # ⚠ **원본은 CWD 가 아니라 실행본 옆이다** (169 D ①). 예전에는 상대경로 `scripts/check.sh` 를
  #   복사했는데, 그 경로는 `cd "$(git rev-parse --show-toplevel)"` 가 데려간 곳 기준이다. 그래서
  #   main 체크아웃에서 이 스크립트를 부르면 **main 판 check.sh 가 조용히 클론에 들어가** 인자를
  #   모른 채 돌고 START/END 줄조차 안 찍혔다. 실패는 조용하지 않아야 한다 — 못 복사하면 멈춘다.
  self_dir=$(cd "$(dirname "$0")" && pwd)
  self_differs=no
  for f in check.sh gate_targeted.py; do
    [ -f "$self_dir/$f" ] || { echo "  [FAIL] 게이트 논리 복사 실패 — $self_dir/$f 가 없다"; exit 2; }
    cmp -s "$self_dir/$f" "$dest/scripts/$f" || self_differs=yes
    cp "$self_dir/$f" "$dest/scripts/$f" || {
      echo "  [FAIL] 게이트 논리 복사 실패 — $self_dir/$f → $dest/scripts/$f"; exit 2; }
  done
  links=$(find "$dest" -type l -not -path "$dest/.git/*" | wc -l | tr -d " ")
  echo "── 격리 실행: $dest ──"
  echo "  트리 sha $tree_sha · 심링크 $links · 게이트 스크립트는 실행본 복사 (트리 판과 다름: $self_differs)"
  echo "  ⚠ 워크트리 무접촉 — 이 판정은 **커밋 sha 의 판정**이고 워크트리 상태의 판정이 아니다"
  # base 는 여기서 도출한다 — 여기서만 `origin` 이 진짜 원격이다.
  base_sha=$(git rev-parse --verify -q --short origin/engine/prototype || true)
  cd "$dest" || exit 2
  set --
  [ "$lane_req" = "wiring" ] && set -- --wiring
  [ "$lane_req" = "targeted" ] && set -- --targeted
  GATE_ISOLATED=1 GATE_TREE_SHA="$tree_sha" GATE_BASE_SHA="$base_sha" GATE_SCRATCH="$dest" exec bash "$dest/scripts/check.sh" "$@"
fi

gate_sha=$(git rev-parse --short HEAD)
# 격리 모드라면 우리가 그 sha 위에 있다는 것이 불변식이다. 아니면 클론이나 checkout 이 어긋난 것이다.
if [ "${GATE_ISOLATED:-}" = "1" ] && [ "$gate_sha" != "${GATE_TREE_SHA:-}" ]; then
  echo "  [FAIL] 격리 트리의 HEAD($gate_sha) 가 요청한 sha(${GATE_TREE_SHA:-}) 와 다르다"
  exit 2
fi

# ── 층: 무엇이 바뀌었는지가 정한다. 사람이 "이번엔 문서만이야" 라고 판단하지 않는다 ──
# `--wiring` 은 물리 시험(약 24 분)을 건너뛴다. 언제 그래도 되는지는 바뀐 경로 목록이 답한다.
# 기본값은 전부 도는 것이다. 애매하면 전부 돈다 — 틀렸을 때 잃는 게 시간뿐인 쪽으로 기운다.
lane="full"
# ⚠ 격리 클론의 origin 은 로컬 워크트리다 — `@{u}` 가 원격을 가리키지 않으므로 "무엇이 바뀌었는지"
#   를 말할 수 없다. 그러면 판단을 포기하고 전부 돈다 (기존 upstream-없음 경로와 같은 처분).
if [ "$lane_req" = "wiring" ] && [ "${GATE_ISOLATED:-}" = "1" ]; then
  echo "── 층: full (격리 클론에는 원격 upstream 이 없어 무엇이 바뀌었는지 말할 수 없다) ──"
  lane_req="full"
fi
if [ "$lane_req" = "wiring" ]; then
  # 비교 대상은 upstream. 없으면 판단을 포기하고 전부 돈다.
  base=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)
  if [ -n "$base" ]; then
    changed=$(git diff --name-only "$base"...HEAD; git diff --name-only; git ls-files --others --exclude-standard)
    # 코드가 하나라도 바뀌었으면 wiring 층은 성립하지 않는다. answer 시험이 거기 있다.
    if echo "$changed" | grep -qE '\.(py|yaml|yml|json|sh)$'; then
      echo "── 층: full (코드가 바뀌었다 — answer 시험은 어떤 경우에도 안 빠진다) ──"
    else
      lane="wiring"
      echo "── 층: wiring (바뀐 것이 전부 문서다 — 물리 시험을 건너뛴다) ──"
    fi
  else
    echo "── 층: full (upstream 이 없어 무엇이 바뀌었는지 말할 수 없다) ──"
  fi
fi

# ── 표적 층의 도출 ─────────────────────────────────────────────────────────────────────────
# ⚠ **매핑은 손으로 적지 않는다.** 규칙과 그 근거는 `scripts/gate_targeted.py` 의 독스트링에 있고,
#   import 그래프의 **추이 폐포**를 매 실행 계산한다 — 169 의 첫 판은 한 홉만 따라가서 저수준
#   모듈의 시험 집합을 크게 놓쳤다(`fermi` 1 대 33 · `eos` 1 대 31 · `registry` 1 대 25, 169 B 실측).
# ⚠ **좁히기가 조용히 틀리는 세 길을 각각 막는다** (감사석 독립 재현, 169). 셋 다 «초록 한 줄» 로
#   끝나므로 막지 않으면 층이 근거 없이 좁아진 것을 아무도 못 본다.
#   ① base 를 못 구한다 → full.  ② base 가 대상 sha **자신**이다 → diff 0 → full.
#   ③ base 가 대상의 **자손**이다 (지난 sha 를 다시 게이트하거나 base 가 오래됐다) → full.
# ⚠ 그리고 diff 는 세 점이 아니라 **트리 대 트리** 다 — 세 점은 merge-base 를 잡으므로 방향에 속는다.
targeted_tests=""
changed_n="n/a"        # ⚠ 계산하지 않은 것과 «0 개 바뀌었다» 는 다른 사실이다
base_sha=""
gap=""
head_sha=$(git rev-parse --short HEAD)
if [ "$lane_req" = "targeted" ]; then
  base_sha=$(git rev-parse --verify -q --short "$base_ref" 2>/dev/null || true)
  if [ -z "$base_sha" ]; then
    gap="(base «$base_ref» 를 찾을 수 없다)"
  elif [ "$base_sha" = "$head_sha" ]; then
    gap="(base 가 대상 sha 자신이다)"
  elif ! git merge-base --is-ancestor "$base_sha" "$head_sha"; then
    gap="(base 가 대상의 조상이 아니다)"
  else
    derived=$(python3 scripts/gate_targeted.py "$base_sha" "$head_sha") || derived=""
    if [ -z "$derived" ]; then
      gap="(도출 도구가 실패했다)"
    else
      changed_n=$(printf '%s\n' "$derived" | sed -n 1p)
      gap=$(printf '%s\n' "$derived" | sed -n 2p)
      targeted_tests=$(printf '%s\n' "$derived" | sed -n 3p)
    fi
  fi
  if [ -n "$gap" ]; then
    echo "── 층: full (이 매핑이 무엇을 시험해야 하는지 말할 수 없다: $gap) ──"
    targeted_tests=""
  else
    lane="targeted"
    echo "── 층: targeted (바뀐 경로 $changed_n · 도출:${targeted_tests:- 없음}) ──"
  fi
fi
# ⚠ 도출된 목록을 START/END 줄에 적는다. `lane=targeted` 만으로는 **무엇이 검사되지 않았는지** 를
#   다음 좌석이 알 수 없고, 그러면 초록 한 줄이 full 층의 초록으로 읽힌다.
# ⚠ 세 필드는 **층과 무관하게** 찍는다 (감사석, 169 B). full 로 떨어진 실행에서도 base 와 gap 이
#   보여야 «왜 좁히지 않았는가» 를 나중에 읽을 수 있고, targeted 일 때만 찍으면 그 정보가 사라진다.
tgt_field=" base=${base_sha:-none} changed=$changed_n"
[ -n "$gap" ] && tgt_field="$tgt_field gap=\"$(echo $gap)\""
[ "$lane" = "targeted" ] && tgt_field="$tgt_field targeted=\"$(echo $targeted_tests)\""
iso_field=""
[ "${GATE_ISOLATED:-}" = "1" ] && iso_field=" isolated=$(pwd)"
# ⚠ **어느 게이트 스크립트가 돌았는지도 기록한다.** 격리 모드는 실행본을 스크래치에 복사하므로
#   트리의 sha 판과 다를 수 있고, 그 사실 없이는 초록 한 줄이 어느 논리의 초록인지 말할 수 없다.
# ⚠ 게이트 논리는 두 파일이므로 둘 다 대조한다 — 하나라도 트리 판과 다르면 `no` 다.
gate_dir=$(cd "$(dirname "$0")" && pwd)
self_hash=$(git hash-object "$gate_dir/check.sh" 2>/dev/null || echo unknown)
helper_hash=$(git hash-object "$gate_dir/gate_targeted.py" 2>/dev/null || echo unknown)
tree_hash=$(git rev-parse "$gate_sha:scripts/check.sh" 2>/dev/null || echo unknown)
tree_helper=$(git rev-parse "$gate_sha:scripts/gate_targeted.py" 2>/dev/null || echo unknown)
if [ "$self_hash" = "$tree_hash" ] && [ "$helper_hash" = "$tree_helper" ]; then
  matches_tree=yes
else
  matches_tree=no
fi
script_field=" script=${self_hash%"${self_hash#???????}"} matches_tree=$matches_tree"
echo "GATE START sha=$gate_sha pid=$$ at=$(date +%T) lane=$lane$tgt_field$iso_field$script_field"

echo "── 1. 스키마 검증 (db/systems/*.json + curated) ──"
step "scripts/pipeline/validate.py" bash -c 'python3 scripts/pipeline/validate.py'
step "scripts/refs/validate_plasma_temp.py" bash -c 'python3 scripts/refs/validate_plasma_temp.py'

echo ""
echo "── 2. 영한 미러 상태 (missing = 실패, stale = 경고) ──"
# check-mirrors.sh 는 missing 과 stale 둘 다 exit 1 로 묶음.
# 이 PR 시점에서는 stale 26+ 건이 별도 작업이므로 경고로 강등.
mirror_out=$(./scripts/check-mirrors.sh 2>&1) || true
echo "$mirror_out"
if echo "$mirror_out" | grep -q "Missing Korean mirrors"; then fail=1; fi

echo ""
echo "── 3. Markdown dead-link 스캔 ──"
step "scripts/check_dead_links.py" bash -c 'python3 scripts/check_dead_links.py'

echo ""
echo "── 3b. 사이트 내부 링크 (docs/ 404) ──"
# 생성 HTML 은 gh-pages 가 정본이라 main 에서 추적하지 않는다(.gitignore 참고).
# 갓 클론했거나 새 워크트리라면 docs/ 에 사이트가 없고, 그때 이 게이트는
# 존재하지 않는 파일을 향한 링크를 전부 404 로 신고한다 — 빌드하라는 뜻이지
# 링크가 깨졌다는 뜻이 아니므로, 빌드 여부를 먼저 확인하고 건너뛴다.
if [ -f docs/index.html ]; then
  step "scripts/check_site_links.py" bash -c 'python3 scripts/check_site_links.py'
else
  echo "  [SKIP] 사이트가 빌드되지 않은 트리 — run_pipeline.sh 후 다시 확인"
fi

echo ""
echo "── 3c. 인용 링크 (docs/reference bibcode/arXiv) ──"
step "scripts/check_citation_links.py" bash -c 'python3 scripts/check_citation_links.py'

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
    _*|html-pipeline|stability-sim|generic-driver|kopernicus-emit-workspace|circumstellar-disk-schema) ;;  # allowlist
    *[-]*) echo "  [FAIL] phase3 non-snake_case system dir: $name"; fail=1 ;;
  esac
done
if [ $fail -eq 0 ]; then echo "  [PASS] 컨벤션 점검 통과"; fi

echo ""
echo "── 5. 경로 마이그레이션 잔여물 점검 ──"
# 이 스크립트 자체(패턴 정의)와 sprawl-audit 문서(이 패턴들을 인용·논의하는
# 자기참조 감사 기록, 소스 .md + ko 미러 + docs/wiki 렌더 HTML 셋 다)는 제외.
# `docs/wiki` 는 이제 build_docs.py 가 정상 생성하는 라이브 렌더 경로라 패턴에서
# 뺀다(옛 flat 위키 경로 가드는 LLM-위키 롤백으로 무의미).
patterns="alpha-cen-proxima-system|trappist-1-system|llm-wiki|skills-lock"
hits=$(git grep -lE "$patterns" -- ':!scripts/check.sh' ':!plans/doc-tool-sprawl-audit.md' ':!ko/plans/doc-tool-sprawl-audit.md' ':!docs/wiki/plans__doc-tool-sprawl-audit.html' 2>/dev/null || true)
dup_skill=$(git grep -lE "\.agents/skills/(firefly-cfg|nearstars-phase3|find-skills|kopernicus-cfg|nearstars-add-star)/" -- ':!scripts/check.sh' 2>/dev/null || true)
if [ -n "$hits" ] || [ -n "$dup_skill" ]; then
  [ -n "$hits" ] && { echo "  옛 경로 잔존:"; echo "$hits" | sed 's/^/    /'; }
  [ -n "$dup_skill" ] && { echo "  옛 스킬 경로 잔존:"; echo "$dup_skill" | sed 's/^/    /'; }
  echo "  [FAIL] 위 파일을 점검하세요."
  fail=1
else
  echo "  [PASS] 경로 마이그레이션 잔여물 없음"
fi

echo ""
echo "── 6. 영문 source-of-truth 영역 한글 dominant 검사 ──"
step "scripts/check_language.py" bash -c 'python3 scripts/check_language.py'
# 마크다운 표가 산문에 붙어 렌더 안 되는 자리 (2026-09-06). 예외는 스크립트 안에 이유와 함께.
step "scripts/check_md_tables.py" bash -c 'python3 scripts/check_md_tables.py'
# 같은 절이 한 파일에 두 번 (2026-09-06). gate129 가 그런 파일을 초록으로 통과시킨 뒤 붙였다.
step "scripts/check_md_dupes.py" bash -c 'python3 scripts/check_md_dupes.py'

echo ""
echo "── 7. 빌드 산출물 신선도 + 매니페스트 커버리지 ──"
if [ -f docs/index.html ]; then
  step "scripts/check_build_freshness.py" bash -c 'python3 scripts/check_build_freshness.py'
else
  echo "  [SKIP] 사이트가 빌드되지 않은 트리"
fi

echo ""
echo "── 8. Phase 4 emit-게이트 (v2 strict / legacy soft) ──"
step "scripts/check_phase4_gate.py" bash -c 'python3 scripts/check_phase4_gate.py'

echo ""
echo "── 9. Sprawl / 레이아웃 게이트 (AGENTS.md §2.4) ──"
g9=0
# 9a. phase4 루트 파일은 <system>.yaml + SPEC.md + README.md 만 허용
for f in $(git ls-files 'phase4/*' | grep -v '/.*/'); do
  base=$(basename "$f"); dir=$(dirname "$f")
  [ "$dir" != "phase4" ] && continue
  case "$base" in
    *.yaml|SPEC.md|README.md) ;;
    *) echo "  [FAIL] phase4 루트 비허용 파일: $f (→ _audit/ | policies/ | art-direction/ | viewers/ | <topic>/)"; g9=1 ;;
  esac
done
# 9b. phase2/phase3 루트에 loose 파일 금지 (디렉토리만)
for p in phase2 phase3; do
  for f in $(git ls-files "$p/*" | awk -F/ 'NF==2'); do
    echo "  [FAIL] $p 루트 loose 파일: $f (→ $p/<topic>/ 안으로)"; g9=1
  done
done
# 9c. 빈 디렉토리 (phase2/3/4 아래, gitignored _scratch 제외)
empties=$(find phase2 phase3 phase4 -type d -empty -not -path '*/_scratch*' 2>/dev/null)
if [ -n "$empties" ]; then
  echo "$empties" | sed 's/^/  [FAIL] 빈 디렉토리: /'; g9=1
fi
# 9d. 추적되는 *.log 금지 (보드가 evidence로 인용하는 allowlist 제외)
log_allow="phase3/stability-sim/results/_snapshot500/elements.log
phase3/stability-sim/results/_ring_clearing.log"
for f in $(git ls-files '*.log'); do
  echo "$log_allow" | grep -qx "$f" || { echo "  [FAIL] 추적되는 run log: $f (git rm --cached + gitignore)"; g9=1; }
done
# 9e. scripts/refs/*.py 는 전부 tools.md 에 인덱스돼야 함
for f in scripts/refs/*.py; do
  base=$(basename "$f")
  grep -q "$base" docs/reference/tools.md || { echo "  [FAIL] tools.md 미등재: $f"; g9=1; }
done
if [ $g9 -eq 0 ]; then echo "  [PASS] sprawl/레이아웃 게이트 통과"; else fail=1; fi

echo ""
echo "── 10. 파이프라인 경계 게이트 (pipeline-contract.md §1) ──"
step "scripts/check_pipeline_flow.py" bash -c 'python3 scripts/check_pipeline_flow.py'

echo ""
echo "── 11. 사이트맵 연결성 게이트 (신규 고아 페이지 감지) ──"
if [ -f docs/index.html ]; then
  python3 scripts/build_sitemap.py --audit-only || { echo "  [FAIL] build_sitemap"; fail=1; }
else
  echo "  [SKIP] 사이트가 빌드되지 않은 트리"
fi

echo ""
echo "── 12. 방법론 등재 게이트 (EN 인덱스 / KO 미러 / 위키 포털) ──"
step "scripts/check_methodology_coverage.py" bash -c 'python3 scripts/check_methodology_coverage.py'

echo ""
echo "── 12b. 계약 · 인용 앵커 · 밴드 (문서가 깨뜨릴 수 있는 것들, 물리보다 먼저) ──"
# 2026-09-06 에 게이트 맨 끝에서 여기로 옮겼다. 빨라져서가 아니다 — 총 시간은 그대로다.
# 문서 한 줄이 앵커나 계약을 깨뜨렸을 때 **24분 뒤가 아니라 2분 안에** 보이기 때문이다.
# 로컬로 미리 돌리는 습관이 없는 사람에게는 옛 순서가 곧 24분이었다. 이 블록은 약 80초이고
# 그중 77초가 check_contracts 다 (표본 천체로 레시피를 실제로 돌리므로 싼 검사가 아니다).
# ⚠ 2026-09-09: 이 77초는 낡았다 — 오늘 세 실행이 136 · 141 · 136.22 s 로 같은 자리에 떨어졌다(셋째는
#   감사석). 조회 로그(C45 (b)) 탓이 아니다: 끄면 5 s 더 걸렸다. 77 은 09-06 순서 변경 때의 수이고 그 뒤로
#   부하가 늘었다 — 지금 레시피 14 · 계산 노드 35 를 표본 천체마다 돈다. 조정하지 않고 후보 원인만 적는다.
# chain.yaml 의 via 가 공급자 outputs 에 있는가 (Brief 43). 허용목록(도출 8) · status:gap 밖의 via 는 실패다.
python3 engine/check_via.py --gate || { echo "  [FAIL] check_via"; fail=1; }
step "check_contracts.py" bash -c 'cd engine && python3 check_contracts.py'
# 인용 앵커 (C33). 앵커 구절이 대상 문서에서 정확히 1회 매치돼야 한다 — 0회는 썩음, 2회 이상은 애매.
# 줄번호 인용은 아직 실패시키지 않고 미이행으로 센다(배치 이행 중). 체커 자기검증은 test_check_refs.py.
# 밴드 규칙 (C32). 세 상태 · 출처 없는 폭 거절 · 묶음 불가분 · 선택지 요건이 앵커다.
step "test_bands.py" bash -c 'cd engine && python3 test_bands.py'
step "test_albedo_table.py" bash -c 'cd engine && python3 test_albedo_table.py'
step "test_greenhouse_cases.py" bash -c 'cd engine && python3 test_greenhouse_cases.py'
step "test_sub_neptune_dynamo.py" bash -c 'cd engine && python3 test_sub_neptune_dynamo.py'
step "test_stellar_wind.py" bash -c 'cd engine && python3 test_stellar_wind.py'
# 임시값 가드레일 다섯. ⑤ 는 레시피가 도착하면 FAIL — 그 발화를 시험이 오늘 증명한다.
step "test_tidal_locking.py" bash -c 'cd engine && python3 test_tidal_locking.py'
step "test_provisional.py" bash -c 'cd engine && python3 test_provisional.py'
# 전이 기록 (Brief 153). 다른 천체의 값은 기록 없이 못 들어오고, state 인데 derived 면(3040 K 모양) 거절.
step "test_transfers.py" bash -c 'cd engine && python3 test_transfers.py'
# 정의역·방향 (Brief 155, C48). 법칙의 정의역은 callee 가 지켜 소비자가 우회 못 하고, 한계의 방향은 필드에서 부호가 난다.
step "test_domain.py" bash -c 'cd engine && python3 test_domain.py'
step "test_check_refs.py" bash -c 'cd engine && python3 test_check_refs.py'
step "engine/check_refs.py" bash -c 'python3 engine/check_refs.py'
# 논문 인용 규약 (C33 (b), 브리프 165). ⚠ **판정 아님 — 세기만 한다**: bibcode 없는 절의 "저자+연도"
# 인용 수를 인쇄하고 기준선(28 절 · 128 건)과 비교한다. 0 이 되면 FAIL 로 승격. 비용 ~0.1 s.
# ⚠ 기준선이 27·124 가 아니라 28·128 인 이유: 이 규칙을 설명하는 절(C33 (b))이 인용 **예시** 를 적어
#   스스로 4건 걸린다 — 오검출 종류로 도구 독스트링에 적혀 있다.
# ⚠ `|| fail=1` 을 붙이지 않는다: 이 도구는 항상 0 을 돌려주므로 붙여도 불발이고, 붙은 채 두면
#   "판정한다" 로 잘못 읽힌다 (B2, 감사 지적).
python3 engine/tools/check_citations.py --quiet

if [ "$lane" = "targeted" ]; then
  echo ""
  echo "── 13–14 중 도출된 물리 시험만 (targeted 층) ──"
  if [ -z "$targeted_tests" ]; then
    echo "  바뀐 것이 전부 문서다 — 물리 시험 0 건. 12b 의 계약·인용 검사는 위에서 전부 돌았다."
  fi
  for tt in $targeted_tests; do
    case "$tt" in
      run:*) step "run.py ${tt#run:}" bash -c 'cd engine && exec python3 run.py "$1"' _ "${tt#run:}" ;;
      # ⚠ 13 블록에는 `test_*.py` 가 아닌 게이트 단계가 셋 있다 (169 D ②). 그 셋을 부를 어휘가
      #   없으면 `engine/backflow.py` 를 고친 커밋이 자기를 검사하는 단계 없이 초록으로 지나간다.
      gate:backflow) python3 engine/backflow.py check >/dev/null 2>&1 || { echo "  [FAIL] backflow"; fail=1; } ;;
      gate:chain) step "engine/chain.py check" bash -c 'python3 engine/chain.py check' ;;
      gate:dynamo_table) python3 engine/dynamo_table.py --check || { echo "  [FAIL] dynamo_table"; fail=1; } ;;
      # ⚠ full 층이 `--quiet` 로 부르는 시험은 표적 층도 그렇게 불러야 한다 — 다른 인자는 다른 검사다.
      tools/c47_step4.py) step "tools/c47_step4.py" bash -c 'cd engine && exec python3 tools/c47_step4.py --quiet' ;;
      *) if [ -f "engine/$tt" ]; then step "$tt" bash -c 'cd engine && exec python3 "$1"' _ "$tt"
         else echo "  [FAIL] 도출된 시험 파일이 없다: engine/$tt"; fail=1; fi ;;
    esac
  done
elif [ "$lane" = "wiring" ]; then
  echo ""
  echo "── 13–14 물리 시험 건너뜀 (wiring 층). 코드가 바뀐 커밋에서는 절대 건너뛰지 않는다 ──"
else

echo ""
echo "── 13. 엔진 그래프 + 역류 층 ──"
# chain.yaml 은 방법론끼리의 의존, bindings.yaml 은 이미 출하된 확정값이 어느
# 노드에서 나왔고 무엇이 그걸 먹는지. 후자가 없어서 Proxima pause_nose 사고가 났다.
step "engine/chain.py" bash -c 'python3 engine/chain.py check'
python3 engine/backflow.py check 2>&1 | grep -v "^  \[WARN\]" || true
step "engine/backflow.py" bash -c 'python3 engine/backflow.py check >/dev/null 2>&1'
step "test_backflow.py" bash -c 'cd engine && python3 test_backflow.py'
step "test_dynamo.py" bash -c 'cd engine && python3 test_dynamo.py'
# ⚠ **바디 목록은 고정 셋이 아니라 디렉토리다** (169 E). 예전에는 셋(alpha·pandora·earth)을 손으로
#   적어 두었고, 그래서 `bodies/mars.yaml` 의 출하값 대조가 **09-08 이후 한 번도 안 돌았다** —
#   표적 층의 바디 규칙이 화성을 처음 돌렸을 때 8.9 % 어긋남이 그대로 있었다(C59). 왜 셋이었는지는
#   기록이 없다. 고정 목록은 여덟 번째 바디에서 같은 일을 반복하므로 글롭으로 바꾼다.
#   ⚠ 같은 글롭을 `scripts/gate_targeted.py` 의 `answer_bodies()` 도 쓴다 — 두 파일이 갈리지 않게
#   **디렉토리 자체가 유일한 출처**다.
#   ⚠ 라벨을 가른다: `expected:` 블록이 있는 바디는 **출하값 대조**, 없는 바디는 **연기 시험**
#   (완주하는지만 본다). 둘을 한 이름으로 부르면 «일곱 개 대조» 로 읽히는데 그건 사실이 아니다.
for _b in engine/bodies/*.yaml; do
  _name=$(basename "$_b")
  if grep -q '^expected:' "$_b"; then _kind="출하값 대조"; else _kind="연기 시험"; fi
  step "run.py bodies/$_name ($_kind)" bash -c 'cd engine && exec python3 run.py "bodies/$1"' _ "$_name"
done
step "test_mass_radius.py" bash -c 'cd engine && python3 test_mass_radius.py'
step "test_fermi.py" bash -c 'cd engine && python3 test_fermi.py'
step "test_water_hot.py" bash -c 'cd engine && python3 test_water_hot.py'
step "test_ammonia.py" bash -c 'cd engine && python3 test_ammonia.py'
step "test_water2.py" bash -c 'cd engine && python3 test_water2.py'
# ⚠ ANSWER 시험 — 게이트에서 가장 긴 단일 구간(약 459 초, 전체의 31 %)이고, 그 시간이 사는 곳이다.
# 이 시험만이 엔진을 **현실**과 대조한다. 자기 헤더가 그렇게 적는다 — 앵커는 전부 측정값이고
# (반지름은 측지, C/MR² 는 중력장·세차), "우리 출력으로 우리를 시험하면 아무것도 검증되지 않는다".
# 다른 시험들은 배선이 도는지 본다. 이것은 답이 맞는지 본다.
# ⇒ 층을 나눌 때 **"느린 시험"으로 분류해 빼면 안 된다.** 뺄 수 있는 유일한 경우는 코드가 하나도
#    안 바뀐 커밋이고, 그 판단은 사람이 아니라 바뀐 경로 목록이 한다 (12b 위 주석 참조).
step "test_interior.py" bash -c 'cd engine && python3 test_interior.py'
# 얼음거대행성 앵커. 천왕성·해왕성을 실제로 풀어(각 ~50 초) 굳힌 값과 비트까지 대조하고,
# 격자 위상·격자 수렴도 본다. 답을 바꾸는 작업은 --refresh 로 다시 굳혀 diff 에 남긴다.
step "test_ice_giant.py" bash -c 'cd engine && python3 test_ice_giant.py'
step "test_core_state.py" bash -c 'cd engine && python3 test_core_state.py'
step "test_body_class.py" bash -c 'cd engine && python3 test_body_class.py'
step "test_porosity.py" bash -c 'cd engine && python3 test_porosity.py'
step "test_giant.py" bash -c 'cd engine && python3 test_giant.py'
step "test_mixture.py" bash -c 'cd engine && python3 test_mixture.py'
step "test_rocky_roster.py" bash -c 'cd engine && python3 test_rocky_roster.py'
# 조석 수송 축 (Brief 35). 이오 재현 실패가 측정 불변량으로 고정되어 있다 —
# 이 테스트가 울리면 실패 서사 자체가 바뀐 것이니 멈추고 추적한다.
step "test_tidal_transport.py" bash -c 'cd engine && python3 test_tidal_transport.py'
# 규산염 녹는곡선 사슬 (Brief 36). 전사 검산과 이음매 계단이 측정 불변량이다.
step "test_silicate_melt.py" bash -c 'cd engine && python3 test_silicate_melt.py'
# 도형 완화 판정 (Brief 39). 전사 검산·문턱 가족의 불감성·라벨·지구 판정이 앵커다.
step "test_rheology.py" bash -c 'cd engine && python3 test_rheology.py'
# 밀도 적합 ↔ 녹는곡선의 조성·물질상 선언 (Brief 41). 다른 조인을 말없이 잇는 상이 생기면 여기서 잡힌다.
step "test_eos_joins.py" bash -c 'cd engine && python3 test_eos_joins.py'
# 방사성 예산 (Brief 44). 초안 표의 폐합 세 건·캡션 오독 11.59 TW·과거 방향 3.67 이 앵커다.
step "test_radiogenic.py" bash -c 'cd engine && python3 test_radiogenic.py'
# 함의 열류 일관성 (Brief 46). Table 2 전사 폐합(42 TW ← 1614 K)과 ζ 양방향 민감도, 판정 라벨이 앵커다.
step "test_mantle_flux.py" bash -c 'cd engine && python3 test_mantle_flux.py'
echo "── CMB 열류 (Nimmo 식 37–39 폐합 · 단열 열류 · 거절 라벨) ──"
step "test_cmb_flux.py" bash -c 'cd engine && python3 test_cmb_flux.py'
# 핵 에너지 수지 (C14). Nimmo 해석 핵으로 Table 4 성분별 재현·근 4152 K, 엔진 지구는 보고, 내핵 두 분기, 거절 라벨이 앵커다.
step "test_core_energy.py" bash -c 'cd engine && python3 test_core_energy.py'
# 핵 엔트로피 생성 φ (C15). Nimmo 해석 핵으로 Table 4 의 여섯 엔트로피 항 성분별 재현, 엔진 지구는 밴드로 보고, 내핵 두 분기, 3 Gyr 거절 라벨이 앵커다.
step "test_core_entropy.py" bash -c 'cd engine && python3 test_core_entropy.py'
# 열진화 적분기 (C20). 지구 단일 실행(h = min(4 Myr, 0.1·τ) — Nimmo 의 4 Myr 은 상한, 브리프 157)이 사전등록 분기 ①②④③ 을 그 순서로 읽는다; 수렴 스윕은 온디맨드(--sweep, ~400 s).
step "test_core_history.py" bash -c 'cd engine && python3 test_core_history.py'
# 정체뚜껑 맨틀 수지 (C51 1단계). Foley 2018 식 (1)–(4) 전사가 논문 인쇄 도출값(μ_r, Pe)을 재현하고, «cancel out» 이
# 항등식임을 재고, 식 (2) 는 없는 입력을 이름 대며 거절한다. 판정 칸 셋은 여기서 읽지 않는다 (커밋 D). ~0 s.
step "test_mantle_budget.py" bash -c 'cd engine && python3 test_mantle_budget.py'
# 전이 영역 스케일링 (C51 커밋 C). F&B 2014 Table 1 세 행·식 (54)(58)(59)(60) 전사. 폐합이 위·아래 열류를 맞추고,
# 논문 자기 반올림의 값어치와 (m,p) 세 행의 벌어짐을 재고, 바디 경로는 비차원 입력 일곱을 대며 거절한다. ~0 s.
step "test_transitional_lid.py" bash -c 'cd engine && python3 test_transitional_lid.py'
# C51 세 영역 평가 (커밋 D). 각 법칙을 자기 앵커에만 대조하고 등록된 판정 칸 셋을 찍는다.
# ⚠ 게이트가 검사하는 것은 **재현 여섯 행**이고 판정은 [판정] 줄로 인쇄만 한다 — 판정을 붉게 두면
# 다음 좌석이 그 붉음을 배경으로 읽는다 (c47_step4.py 와 같은 형식). ~0 s.
step "tools/c51_regimes.py" bash -c 'cd engine && python3 tools/c51_regimes.py'
# 페이로드 등급 계약 (2026-09-04 오너 결정). authored 는 두 표지(gap:, consistent-with:) 없이는 생성되지 않는다.
step "test_payload.py" bash -c 'cd engine && python3 test_payload.py'
# 상 곁표 (2026-09-04, 오너 채택 패턴). 키 집합 = eos 가 내는 상, 채운 칸은 등급·출처, authored 는 두 표지, 채움/전체를 출력한다.
step "test_phase_tables.py" bash -c 'cd engine && python3 test_phase_tables.py'
# 조석 가열 (C30). 이오 밴드 재현·판도라 보드 45 W/m² 재현(0.75 %)·×Io 규약 R⁵·§6.1/§6.2 라벨 표·거절 넷이 앵커다.
step "test_tidal_heating.py" bash -c 'cd engine && python3 test_tidal_heating.py'
# 정체뚜껑 스케일링 (C47 (f), brief 148 단계 1). Korenaga 2009 Table 2 Δη=1 10행 eq. 29 대조가 앵커다
# — 이 엔진이 가진 유일한 행별 앵커이고, 절대 스케일에는 앵커가 없다(C47 (c)·(e)).
step "test_stagnant_lid.py" bash -c 'cd engine && python3 test_stagnant_lid.py'
# C47 4단계 방향 시험 (브리프 162). 기본 모드가 **현재 커밋의 기대표**를 검사한다 — 09-07 앵커는
# `--anchors` 로만 요구하며 커밋 1 에서만 통과한다. 판정은 C47 (k) 커밋 6 에 있고 여기서는 회귀만 막는다.
# ⚠ 게이트 시간에 ~62 s 를 더한다 (eq. 56 고정점이 1500 °C 행에서 120여 회 반복).
step "tools/c47_step4.py" bash -c 'cd engine && python3 tools/c47_step4.py --quiet'
# C24 (2026-09-04). 물 기둥의 IF97 후보(마지막)·두 이음매 ≤ 0.05 %·얼음 0 양성 대조·물 많은 암석체 0.1/0.3.
step "test_water_column_steam.py" bash -c 'cd engine && python3 test_water_column_steam.py'
# 판구조 영역 밴드 (C53, 브리프 168 B). 세 로스터 바디의 파생 불리언이 168 B 전 값과 비트 동일하고,
# contested → DEAD_LID(필드 0) · transitional → UNDECIDED_LID(dead 아님) 를 **상수 동일성**으로 걸고,
# episodic·heat_pipe 는 이름을 대며 거절한다. 어휘 밖 값·등급·모양도 거절한다. 사다리의 도메인 게이트가
# 판구조 거절보다 먼저라는 C28 불변식도 여기서 지킨다 (168 C). ⚠ **~12 s** — 그중 8.5 s 가 판도라를
# 실제로 풀어 B_eq 41.37252479971432 을 자릿수까지 대조하는 값이다 (지구는 같은 검사를 71 s 에 산다).
step "test_tectonic_regime.py" bash -c 'cd engine && python3 test_tectonic_regime.py'
# 암석 다이나모 사다리 (Brief 47). 문서 표 재현·RM22 Table 8 차이·게이트 라벨·격자 미선출이 앵커다.
step "test_dynamo_rocky.py" bash -c 'cd engine && python3 test_dynamo_rocky.py'
python3 engine/dynamo_table.py --check || { echo "  [FAIL] dynamo_table"; fail=1; }

fi   # lane

echo ""
if [ $fail -eq 0 ]; then
  echo "──────── 모든 점검 통과 ────────"
else
  echo "──────── 일부 점검 실패 ────────"
fi
echo "GATE END sha=$gate_sha pid=$$ at=$(date +%T) lane=$lane$tgt_field$iso_field$script_field rc=$fail"

# ── ④ 스크래치 정리. rc=0 이면 지우고, **실패면 남긴다** — 재현할 것이 있는 쪽만 보관한다 ──
# ⚠ 169 는 아무것도 지우지 않았고 반나절에 네 벌 684 MB 가 쌓였다 (감사석 관측).
if [ "${GATE_ISOLATED:-}" = "1" ] && [ -n "${GATE_SCRATCH:-}" ]; then
  if [ "$fail" -eq 0 ]; then
    echo "  격리 스크래치 삭제: $GATE_SCRATCH (rc=0 — 재현할 것이 없다)"
    rm -rf "$GATE_SCRATCH"
  else
    date > "$GATE_SCRATCH/GATE-FAILED" 2>/dev/null || true
    echo "  격리 스크래치 보존: $GATE_SCRATCH (rc=$fail — 여기서 재현한다)"
  fi
fi
exit $fail
