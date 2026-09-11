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
exec 3>&2                     # step() 이 자식의 stderr 를 여기로 빼낸다 (아래 주석)

# ── 병렬 풀 (브리프 184) ──────────────────────────────────────────────────────────────────
# 첫 계측(gate226): 71 단계 합 **2681 s = 45 분**, 최대 RSS **57 MB**. 시간은 직렬 합이 원인이고
# 메모리는 문제가 아니다 — 그래서 단계를 동시에 돌린다. 논리 코어 15 에 대해 기본 8 을 쓴다.
#
# ⚠ **호출부를 하나도 안 고친다.** 풀에 들어갈 자격은 `step()` 이 **이름으로** 판정한다 —
#   `test_…` 와 `run.py …` 만 들어가고 나머지는 직렬로 남는다. 그러면 격리 검사·베이스 결정·
#   12b 계약/인용 블록·집계가 저절로 순서를 지킨다. 자격을 call-site 에 적으면 571 줄에 흩어진
#   `step` 마다 사람이 판단해야 하고, 그 판단이 한 번 틀리면 순서 의존이 조용히 깨진다.
#
# ⚠ **배경 서브셸의 `fail=1` 은 부모로 오지 않는다.** 그래서 자식은 **종료 코드를 파일로** 남기고,
#   `step_flush` 가 그것을 읽어 부모의 `fail` 을 센다. 이 경로가 실제로 무는지는 격리 하네스에서
#   실패를 주입해 증명했다 (커밋 메시지).
#
# ⚠ **`__pycache__` 경합을 먼저 막는다.** 게이트는 `PYTHONDONTWRITEBYTECODE` 를 켜지 않으므로,
#   같은 디렉토리에서 파이썬 여럿이 바이트코드를 동시에 쓰면 경합한다. 풀 단계에만 켠다.
#
# bash 3.2 라 `wait -n` 이 없다 — `jobs -rp` 폴링으로 자리를 기다린다.
#
# ⚠ **기본이 8 이다** (2026-09-11, 실측 뒤). 세 값을 같은 커밋에서 재 봤다 — 직렬 34.5–44.7 분 ·
#   풀 2 20–22 분 · **풀 8 12 분 8 초** (gate234, 71 단계 전부 집계, PASS 682, RSS 최대 57 MB).
#   바닥은 한 단계다 — 가장 긴 단계를 쪼개지 않으면 어떤 풀 크기도 full 을
#   6 분 아래로 못 내린다. **기계를 조용히 둬야 할 때는 환경변수로 `GATE_POOL=2`**, 완전 직렬은
#   `1` 이고, 세 값이 같은 코드 경로를 지난다 — 판정선이 «풀 크기» 하나만 다르다.
#
# ⚠ **바닥 수치는 sha 와 날짜를 달고 적는다.** 이 줄은 예전에 «`test_giant` 만 311 초» 라고
#   적혀 있었고, 그 수가 낡은 줄 모르고 시한을 재면 긴 단계가 6 분 만에 죽은 것으로 몰린다.
#   **@587842b3, 2026-09-11, 풀 2, 부하 적힘: `test_interior.py` 4114 s · `test_giant.py` 284 s.**
#   산문에 적힌 시간은 sha 와 날짜를 달거나, 적지 않는다.
GATE_POOL="${GATE_POOL:-8}"
# ⚠ **배리어의 단 하나의 천장** (C80). «살아 있지만 조용한» 워커에만 쓰고, 죽은 워커는 시한
#   없이 즉시 이름을 얻는다. 값은 **이 커밋을 낸 게이트의 가장 긴 단계 × 1.5** 이고 sha 와
#   날짜를 함께 적는다 — @3716708f, 2026-09-12, 가장 긴 단계 3035 s.
#   ⚠ *이 수는 낡는다*: 단계 목록이나 기계가 바뀌면 최신 게이트 로그의 `[TIME]` 과 다시 대조할
#   것. 단계마다 예산을 두는 쪽이 더 나은 설계이고 그것은 C81 이다 — 여기서 막지 않는다.
GATE_BARRIER_MAX="${GATE_BARRIER_MAX:-4553}"
# ⚠ **채워지지 않은 천장은 조용히 «천장 없음» 이 된다** (감사석, 2026-09-12): 천장 자리표시자가
#   남아 있으면 비교는 `[` 의 오류(상태 2)가 되고 `if` 는 그것을 거짓으로 읽어, 배리어가 영영
#   시한을 안 넘기며 0.2 초마다 쉘 오류만 뱉는다. 그래서 여기서 숫자인지 먼저 묻는다.
case "$GATE_BARRIER_MAX" in
  ''|*[!0-9]*) echo "  [FAIL] gate_barrier_max_unset — 배리어 천장 «${GATE_BARRIER_MAX}» 이 숫자가 아니다."; exit 1 ;;
esac
_pool_dir=""
_pool_seq=0
# ⚠ **띄운 수와 거둔 수를 부모의 기억에 센다** (브리프 184 B). 디스크에만 세면 스풀이 사라질 때
#   세는 근거도 함께 사라진다 — gate229 가 정확히 그렇게 **초록으로 거짓 통과**했다: 풀 디렉터리가
#   실행 중에 지워져 자식들이 종료 파일을 쓸 곳을 잃고, flush 가 아무것도 못 읽고, 배리어가 그냥
#   통과해 71 단계 중 **52 개가 판정에 안 든 채** rc=0 이 나왔다. 169 E 와 같은 계열의 결함이다 —
#   «안 돈 단계» 가 «통과한 단계» 와 구별되지 않는 자리.
_pool_launched=0
_pool_drained=0
_pool_names=""

_pool_eligible() {            # _pool_eligible <이름>
  case "$1" in
    test_*|run.py*) return 0 ;;
    *) return 1 ;;
  esac
}

_pool_alive() {               # 스풀이 살아 있고 쓸 수 있는가 — 아니면 이름 대고 실패한다
  [ -n "$_pool_dir" ] || return 1
  if [ -d "$_pool_dir" ] && touch "$_pool_dir/.probe" 2>/dev/null; then
    rm -f "$_pool_dir/.probe"; return 0
  fi
  echo "  [FAIL] pool_dir — 풀 스풀 «${_pool_dir}» 이 없거나 쓸 수 없다. 이 상태에서는 풀 단계의"
  echo "         판정이 로그에 도착하지 못하고 게이트가 **거짓 초록**이 된다 (gate229)."
  fail=1
  return 1
}

_pool_drain() {               # 끝난 단계의 로그를 **완료 순서**로 붙이고 rc 를 센다
  local f n
  [ -n "$_pool_dir" ] || return 0
  [ -d "$_pool_dir" ] || return 0
  for f in $(ls -1tr "$_pool_dir"/*.done 2>/dev/null); do
    n="${f%.done}"
    cat "$n.log" 2>/dev/null
    if [ "$(cat "$n.rc" 2>/dev/null || echo 1)" != "0" ]; then fail=1; fi
    rm -f "$f" "$n.log" "$n.rc" "$n.pid"
    _pool_drained=$((_pool_drained + 1))
  done
}

# ⚠ **예전의 배리어는 `wait` 한 줄이었고, 그래서 워커 하나가 사라지면 게이트가 실패하는 대신
#   멈췄다** (C80, 2026-09-11). `587842b3` 의 게이트는 72 단계 중 71 개의 판정을 스풀에 들고도
#   21:39–22:15 를 아무 말 없이 기다렸다. bash 3.2 에는 `wait -n` 도 `wait` 의 시한도 없으므로
#   배리어는 자리 대기 고리와 같은 모양으로 **폴링**한다.
#
# ⚠ **죽은 워커에는 시한이 필요 없다.** 스풀이 이미 상태를 구별한다 — «거둠»(파일이 없다) ·
#   «끝났는데 안 거둠»(`.done` 이 있다 — 거두면 된다) · «죽음»(`.pid` 가 남았는데 그 프로세스가
#   없고 `.done`·`.rc` 도 없고 **`.out` 이 남았다**). 마지막 것은 pid 가 사라진 **그 순간** 완성되는
#   신호라, 기다릴 이유가 없다. 시한은 «살아 있는데 조용한» 워커 하나에만 쓴다.
#
# ⚠ **다섯째 상태는 이름을 안 받는다**: 자식이 스풀-사라짐 가드에서 깨끗이 나가면 `.pid` 는 쓰였고
#   pid 는 죽었고 `.done` 도 없는데 **`.out` 도 없다**. 이 슬롯은 고아로 부르지 않고 지나가며,
#   `pool_incomplete` 의 셈에만 잡힌다 — FAIL 문구가 «아는 것만» 말하는 이유가 이 상태다.
#
# ⚠ **pid 를 먼저 읽고 `.done` 을 다시 읽는다** — 경합은 자식의 두 쓰기가 아니라 **부모의 두
#   읽기**에 있다. `.rc` 와 `.done` 은 서브셸 안에서 잇따른 문장이고 서브셸은 `.done` 뒤에야
#   끝나므로, 그 사이에는 pid 가 살아 있어 «pid 가 없다» 가 거짓이다. 진짜 창은 부모가 `.done` 을
#   먼저 보고 pid 를 나중에 보는 쪽이다 — 그 사이에 끝난 워커가 죽은 것처럼 보인다.
_pool_barrier() {             # 워커가 다 끝나거나, 죽은 워커를 이름 대어 실패시킬 때까지 폰다
  # ⚠ **스풀이 비었으면 아무것도 안 한다** (감사석, 2026-09-12). `_pool_alive` 가 실패해 `step()` 이
  #   `_pool_dir` 를 비우면 아래 글롭이 `"$_pool_dir"/*.pid` = `/*.pid` 가 되어 **파일시스템 루트**를
  #   읽는다. `step_flush` 의 가드는 «띄운 것이 있는가» 라 이 경우를 막아 주지 않는다.
  [ -n "$_pool_dir" ] || return 0
  local _t0=$SECONDS _pidf _pid _base _seq _nm _live _waited _livenames
  while :; do
    _pool_drain
    _live=0; _livenames=""
    for _pidf in "$_pool_dir"/*.pid; do
      [ -e "$_pidf" ] || continue
      _base="${_pidf%.pid}"
      _pid=$(cat "$_pidf" 2>/dev/null)
      # ⚠ **살아 있는지는 `kill -0` 로 묻는다** — 신호를 보내지 않고 존재만 확인한다. pid 재사용은
      #   이론상 거짓 «살아 있음» 을 만들 수 있지만, 재사용까지 걸리는 시간이 배리어가 도는 시간보다
      #   훨씬 길어서 여기서는 무시한다 (재사용은 게이트를 **멈추게** 하지 못하고 천장이 받는다).
      if [ -n "$_pid" ] && kill -0 "$_pid" 2>/dev/null; then
        _seq=$(basename "$_base"); eval "_nm=\$_pool_name_$((10#$_seq))"
        _live=$((_live + 1)); _livenames="$_livenames ${_nm:-$_seq}"; continue
      fi
      # pid 가 죽은 뒤에 **`.done` 을 다시 읽는다** — 부모의 두 읽기 사이에 끝난 워커가 죽은 것처럼
      # 보이는 창이 여기서 닫힌다. 거둔 슬롯은 `.pid` 가 이미 없어 이 고리에 들어오지도 않는다.
      # ⚠ **`.rc` 는 여기서 묻지 않는다** (감사석, 2026-09-12). `_pool_drain` 은 `*.done` 만 훑으므로
      #   `.rc` 는 있는데 `.done` 이 없는 슬롯은 **영원히 안 거둬진다** — 그것을 «살아 있음» 으로 세면
      #   아무도 안 살아 있는데 배리어가 천장까지 돌고 `pool_barrier_deadline` 이 뜬다. 가장 날카로운
      #   신호에 가장 느린 실패가 붙는 셈이다. `.done` 만 보면 그 슬롯은 아래 `.out` 검사로 떨어진다.
      [ -e "$_base.done" ] && { _live=$((_live + 1)); continue; }
      # ⚠ **`.out` 이 판별자다.** 자식은 `.log` 를 쓴 뒤 `.out` 을 지우고 `.rc`·`.done` 을 쓴다.
      #   그래서 «`.out` 이 남았다» 는 «출력을 내다 말았다» 이고, 그 사이의 좁은 창(`.out` 은 지웠고
      #   `.rc` 는 아직)은 이름 대어 죽었다고 하지 않는다 — 그 경우는 `pool_incomplete` 가 센다.
      [ -e "$_base.out" ] || continue
      _seq=$(basename "$_base"); eval "_nm=\$_pool_name_$((10#$_seq))"
      # ⚠ **아는 것만 말한다.** 스풀이 사라지는 가드로 깨끗이 나가도 같은 흔적이 남고, 그날의
      #   `log show` 는 그 소멸에 붙일 줄을 하나도 못 찾았다. 그래서 «죽였다» 가 아니다.
      echo "  [FAIL] pool_orphan ${_nm:-$_seq} — 판정도 없고 살아 있는 워커도 없다."
      fail=1
      rm -f "$_pidf"
    done
    [ "$_live" -gt 0 ] || break
    _waited=$((SECONDS - _t0))
    if [ "$_waited" -ge "$GATE_BARRIER_MAX" ]; then
      echo "  [FAIL] pool_barrier_deadline — 살아 있지만 조용한 워커 $_live 개를 ${_waited} s 기다렸다 (천장 ${GATE_BARRIER_MAX} s)."
      echo "         아직 살아 있는 이름:$_livenames"
      echo "         ⚠ 이 줄은 **아직 도는 워커**의 이름이다 — 띄운 전체 목록이 아니다."
      # ⚠ 이 길로 나가면 자식이 **아직 돌고 있는 채로** 배리어가 돌아간다 — 게이트는 그 뒤에 끝나고
      #   남은 자식은 EXIT 트랩이 스풀을 지울 때 갈 곳을 잃는다. FAIL 경로에서는 그게 옳다.
      fail=1
      break
    fi
    sleep 0.2
  done
}

step_flush() {                # 배리어 — 풀을 비우고, **띄운 수와 거둔 수가 같은지 센다**
  # ⚠ **가드는 «스풀이 있는가» 가 아니라 «띄운 것이 있는가» 다** (감사 지적, 184 B 안에서).
  #   `_pool_alive` 가 실패하면 `step()` 이 `_pool_dir` 를 비워 직렬로 강등하는데, 예전 가드는
  #   그때 **셈을 한 번도 돌리지 않고 빠져나갔다** — rc 는 이미 빨갛지만 «몇 개가, 어느 이름이»
  #   가 사라진다. 그 귀속이 이 셈의 존재 이유다.
  [ "$_pool_launched" -gt 0 ] || [ -n "$_pool_dir" ] || return 0
  _pool_barrier
  _pool_drain
  # ⚠ **이 셈이 없으면 «안 돈 단계» 가 «통과» 로 읽힌다.** 배리어가 통과하는 조건은 «자식이 다
  #   끝났다» 이지 «판정이 다 도착했다» 가 아니다 — 그 둘이 갈리는 순간이 gate229 였다.
  if [ "$_pool_drained" -ne "$_pool_launched" ]; then
    echo "  [FAIL] pool_incomplete — $((_pool_launched - _pool_drained)) 단계가 끝을 못 알렸다 (띄움 $_pool_launched · 거둠 $_pool_drained)."
    echo "         띄운 이름:$_pool_names"
    echo "         ⚠ 두 수는 **서로 다른 출처**에서 센다 — 띄움은 부모의 기억, 거둠은 자식이 남긴"
    echo "         종료 파일이다. 같은 로그를 두 번 grep 하면 로그가 비는 그 경우를 못 잡는다."
    echo "         판정이 없는 단계는 **통과가 아니다**. 스풀이 사라졌거나 자식이 죽었다."
    fail=1
  fi
}

step() {                      # step <이름> <명령...>
  # ⚠ **벽시계를 상시로 찍는다** (브리프 183 C). 게이트가 32 분인데 그중 어느 단계가 얼마인지
  #   말할 수 없었다 — 로그에 시간이 하나도 없어서 «미상 24 분» 이 어디 있는지 셀 수가 없다.
  #   측정 없이 층을 가르면 빠른 층에 느린 시험이 들어간다. 그래서 먼저 재고, 가르는 것은 그
  #   수가 나온 뒤의 별도 브리프다. `SECONDS` 는 bash 내장이라 이 줄이 게이트를 안 늦춘다.
  # ⚠ **최대 RSS 도 함께 찍는다** — 게이트를 둘 동시에 돌려도 되는지를 이 수로 정한다 (예전에
  #   메모리 부족으로 시험 묶음이 두 번 죽었다). `/usr/bin/time -l` 의 통계는 **자기 stderr** 로
  #   나가므로, 자식의 stderr 는 fd 3(진짜 stderr)으로 따로 빼서 진단 출력을 잃지 않는다 —
  #   그 둘을 한 파일에 섞으면 실패한 단계의 오류 문장이 통계 스무 줄에 묻힌다.
  local name=$1; shift
  if [ -n "$_pool_dir" ] && _pool_eligible "$name"; then
    if ! _pool_alive; then                     # 스풀이 죽었다 — 이 단계를 직렬로 돌려 판정을 지킨다
      _pool_dir=""
    fi
  fi
  if [ -n "$_pool_dir" ] && _pool_eligible "$name"; then
    while [ "$(jobs -rp | wc -l)" -ge "$GATE_POOL" ]; do sleep 0.2; _pool_drain; done
    _pool_seq=$((_pool_seq + 1))
    _pool_launched=$((_pool_launched + 1))
    _pool_names="$_pool_names $name"
    local _base
    _base=$(printf "%s/%04d" "$_pool_dir" "$_pool_seq")
    echo "  [STEP] $name — $(date "+%H:%M:%S") 시작 (풀)"
    (
      # ⚠ 스풀이 사라지면 **조용히 나간다** — 판정은 부모의 셈(`pool_incomplete`)이 하고, 자식이
      #   쉘 오류를 스무 줄 토하면 진짜 실패 문장이 그 속에 묻힌다.
      [ -d "$_pool_dir" ] || exit 0
      exec 2>/dev/null        # ⚠ 검사와 첫 쓰기 사이에 스풀이 사라지는 **경합**이 남는다. 그
                              #   리다이렉션 실패는 쉘이 토하는 소음이고, 판정은 부모의 셈이 한다.
      _s0=$SECONDS; _k0=$(date "+%H:%M:%S")
      _st=$(mktemp "${TMPDIR:-/tmp}/gate-step.XXXXXX")
      PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -l bash -c '"$@" 2>&1' _ "$@" \
        >"$_base.out" 2>"$_st"
      _rc=$?
      {
        cat "$_base.out"
        [ "$_rc" = "0" ] || echo "  [FAIL] $name — 비0 종료 (이 단계가 fail=1 을 세웠다)"
        echo "  [TIME] $name — $_k0 → $(date "+%H:%M:%S") · $((SECONDS - _s0)) s · RSS $(awk '/maximum resident set size/ {printf "%.0f", $1/1048576}' "$_st") MB"
      } > "$_base.log"
      rm -f "$_st" "$_base.out"
      [ -d "$_pool_dir" ] || exit 0
      echo "$_rc" > "$_base.rc"
      : > "$_base.done"
    ) &
    # ⚠ **예전에는 `$!` 를 버렸다** — 그래서 트리의 어디에도 워커의 pid 가 없었고, «이 단계가
    #   죽었다» 를 말할 근거가 없었다. 이름은 부모의 기억에 둔다 (스풀이 사라져도 남는다).
    echo "$!" > "$_base.pid"
    eval "_pool_name_$_pool_seq=\$name"
    return 0
  fi
  local _t0=$SECONDS _c0 _tf _rss
  _c0=$(date "+%H:%M:%S")
  # ⚠ **시작선을 먼저 찍는다** (183 D). `[TIME]` 은 단계가 **끝난 뒤** 나오므로, 실행 중인
  #   단계는 로그에 없다 — 그래서 «가장 긴 단계가 가장 늦게 보인다». 32 분 중 «미상» 이
  #   컸던 이유의 일부가 그것이고, 지켜보는 사람이 «지금 어디» 를 알 수 없었다.
  echo "  [STEP] $name — $_c0 시작"
  _tf=$(mktemp "${TMPDIR:-/tmp}/gate-step.XXXXXX")
  /usr/bin/time -l bash -c '"$@" 2>&3' _ "$@" 2>"$_tf" \
    || { echo "  [FAIL] $name — 비0 종료 (이 단계가 fail=1 을 세웠다)"; fail=1; }
  _rss=$(awk '/maximum resident set size/ {printf "%.0f", $1/1048576}' "$_tf")
  rm -f "$_tf"
  echo "  [TIME] $name — $_c0 → $(date "+%H:%M:%S") · $((SECONDS - _t0)) s · RSS ${_rss:-?} MB"
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
    gap="(base «${base_ref}» 를 찾을 수 없다)"
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
# ── 풀을 연다 (브리프 184). `GATE_POOL=1` 이면 예전과 같은 완전 직렬이다 (되돌릴 손잡이). ──
if [ "$GATE_POOL" -gt 1 ] 2>/dev/null; then
  _pool_dir=$(mktemp -d "${TMPDIR:-/tmp}/gate-pool.XXXXXX")
  trap 'rm -rf "$_pool_dir"' EXIT
fi
# ⚠ **어느 단계가 풀이었는지 로그에서 셀 수 있어야 한다** — 규칙을 여기 한 줄로 찍는다.
echo "GATE POOL size=${GATE_POOL} rule=\"이름이 test_* 또는 run.py* 인 단계만 풀, 나머지는 직렬\" dir=${_pool_dir:-none}"

echo "── 1. 스키마 검증 (db/systems/*.json + curated) ──"
step "scripts/pipeline/validate.py" bash -c 'python3 scripts/pipeline/validate.py'
step "scripts/refs/validate_plasma_temp.py" bash -c 'python3 scripts/refs/validate_plasma_temp.py'

echo ""
echo "── 2. 영한 미러 상태 (missing = 실패, stale = 경고) ──"
# check-mirrors.sh 는 missing 과 stale 둘 다 exit 1 로 묶음.
# 이 PR 시점에서는 stale 26+ 건이 별도 작업이므로 경고로 강등.
mirror_out=$(./scripts/check-mirrors.sh 2>&1) || true
echo "$mirror_out"
if echo "$mirror_out" | grep -q "Missing Korean mirrors"; then
  # ⚠ 169 F 가 놓친 자리 — 여기도 `[FAIL]` 없이 fail 만 세웠다 (gate212 와 같은 모양).
  echo "  [FAIL] 한글 미러 누락 — 위 목록의 파일을 ko/<same-path> 로 만들어라"; fail=1
fi

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
  step "build_sitemap" python3 scripts/build_sitemap.py --audit-only
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
step "check_via" python3 engine/check_via.py --gate
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
      gate:backflow) step "backflow" bash -c 'python3 engine/backflow.py check >/dev/null 2>&1' ;;
      gate:chain) step "engine/chain.py check" bash -c 'python3 engine/chain.py check' ;;
      gate:dynamo_table) step "dynamo_table" python3 engine/dynamo_table.py --check ;;
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
# 액체 Fe–S 부피 규칙 전사 (C55 1단계, 브리프 178 B). Xu+ 2021 의 K₀(X_S)·K′(X_S) 끝점과 지수 혼합,
# 그리고 ⚠ **ρ₀ 가 인쇄되지 않아 재질을 짓지 않는다는 거절**이 앵커다 — R4–R6 은 SI 도착 전까지
# 거절이 기대 결과다. Mori 공백(19 GPa → None)도 여기서 지킨다. ~0 s.
step "test_fe_s.py" bash -c 'cd engine && exec python3 test_fe_s.py'
# 밀도 적합 ↔ 녹는곡선의 조성·물질상 선언 (Brief 41). 다른 조인을 말없이 잇는 상이 생기면 여기서 잡힌다.
step "test_eos_joins.py" bash -c 'cd engine && python3 test_eos_joins.py'
# hcp 철 열 세트 (브리프 187). 저자의 Table S3 재현(보유 SI 에서 시험 시점에 읽는다) · g 와 g(1−g)
# 부호 · 두 축 등급 · 적분기와 핵 노드의 γ 일치 · **두 재질의 호출 표면이 두 구간 다에서 유한**
# (C76: 깨끗한 트리에서 `fe_prem.c_p` 가 던지고 있었는데 천체 기준선이 전부 초록이었다). ~1 s.
step "test_fe_hcp.py" bash -c 'cd engine && python3 test_fe_hcp.py'
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
# C55 판정 칸 (브리프 181 B). 선언된 조성(earth_like)에서 Fe–S 두 재질이 무엇을 내는지 인쇄한다 —
# 오늘은 둘 다 거절이고 그 거절이 **이름을 대는지**가 여기서 도는 이유다. 인자를 주면 cmf 밴드를 훑는다.
# ⚠ 도구는 `shoot` 으로 부른다 (C60 (c)) — `_shoot_pressure` 를 직접 부르면 «답이 적합 밖이면 거절»
#   하는 층 아래에서 인쇄해, 엔진이 안 내놓을 수를 표만 내놓는다. ~2 s.
step "tools/c55_cells.py" bash -c 'cd engine && python3 tools/c55_cells.py' 
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
step "dynamo_table" python3 engine/dynamo_table.py --check

fi   # lane

step_flush                    # ⚠ **집계 앞의 배리어** — 이 줄이 없으면 아직 도는 단계의 실패가 rc 에 안 든다

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
