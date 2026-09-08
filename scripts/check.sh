#!/usr/bin/env bash
# 릴리스 전 일괄 건강 점검 — 수동 실행 전용, 훅 미설치
set -u
cd "$(git rev-parse --show-toplevel)"
fail=0
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
gate_sha=$(git rev-parse --short HEAD)

# ── 층: 무엇이 바뀌었는지가 정한다. 사람이 "이번엔 문서만이야" 라고 판단하지 않는다 ──
# `--wiring` 은 물리 시험(약 24 분)을 건너뛴다. 언제 그래도 되는지는 바뀐 경로 목록이 답한다.
# 기본값은 전부 도는 것이다. 애매하면 전부 돈다 — 틀렸을 때 잃는 게 시간뿐인 쪽으로 기운다.
lane="full"
if [ "${1:-}" = "--wiring" ]; then
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

echo "GATE START sha=$gate_sha pid=$$ at=$(date +%T) lane=$lane"

echo "── 1. 스키마 검증 (db/systems/*.json + curated) ──"
python3 scripts/pipeline/validate.py || fail=1
python3 scripts/refs/validate_plasma_temp.py || fail=1

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
echo "── 3b. 사이트 내부 링크 (docs/ 404) ──"
# 생성 HTML 은 gh-pages 가 정본이라 main 에서 추적하지 않는다(.gitignore 참고).
# 갓 클론했거나 새 워크트리라면 docs/ 에 사이트가 없고, 그때 이 게이트는
# 존재하지 않는 파일을 향한 링크를 전부 404 로 신고한다 — 빌드하라는 뜻이지
# 링크가 깨졌다는 뜻이 아니므로, 빌드 여부를 먼저 확인하고 건너뛴다.
if [ -f docs/index.html ]; then
  python3 scripts/check_site_links.py || fail=1
else
  echo "  [SKIP] 사이트가 빌드되지 않은 트리 — run_pipeline.sh 후 다시 확인"
fi

echo ""
echo "── 3c. 인용 링크 (docs/reference bibcode/arXiv) ──"
python3 scripts/check_citation_links.py || fail=1

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
python3 scripts/check_language.py || fail=1
# 마크다운 표가 산문에 붙어 렌더 안 되는 자리 (2026-09-06). 예외는 스크립트 안에 이유와 함께.
python3 scripts/check_md_tables.py || fail=1
# 같은 절이 한 파일에 두 번 (2026-09-06). gate129 가 그런 파일을 초록으로 통과시킨 뒤 붙였다.
python3 scripts/check_md_dupes.py || fail=1

echo ""
echo "── 7. 빌드 산출물 신선도 + 매니페스트 커버리지 ──"
if [ -f docs/index.html ]; then
  python3 scripts/check_build_freshness.py || fail=1
else
  echo "  [SKIP] 사이트가 빌드되지 않은 트리"
fi

echo ""
echo "── 8. Phase 4 emit-게이트 (v2 strict / legacy soft) ──"
python3 scripts/check_phase4_gate.py || fail=1

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
python3 scripts/check_pipeline_flow.py || fail=1

echo ""
echo "── 11. 사이트맵 연결성 게이트 (신규 고아 페이지 감지) ──"
if [ -f docs/index.html ]; then
  python3 scripts/build_sitemap.py --audit-only || { echo "  [FAIL] build_sitemap"; fail=1; }
else
  echo "  [SKIP] 사이트가 빌드되지 않은 트리"
fi

echo ""
echo "── 12. 방법론 등재 게이트 (EN 인덱스 / KO 미러 / 위키 포털) ──"
python3 scripts/check_methodology_coverage.py || fail=1

echo ""
echo "── 12b. 계약 · 인용 앵커 · 밴드 (문서가 깨뜨릴 수 있는 것들, 물리보다 먼저) ──"
# 2026-09-06 에 게이트 맨 끝에서 여기로 옮겼다. 빨라져서가 아니다 — 총 시간은 그대로다.
# 문서 한 줄이 앵커나 계약을 깨뜨렸을 때 **24분 뒤가 아니라 2분 안에** 보이기 때문이다.
# 로컬로 미리 돌리는 습관이 없는 사람에게는 옛 순서가 곧 24분이었다. 이 블록은 약 80초이고
# 그중 77초가 check_contracts 다 (표본 천체로 레시피를 실제로 돌리므로 싼 검사가 아니다).
# chain.yaml 의 via 가 공급자 outputs 에 있는가 (Brief 43). 허용목록(도출 8) · status:gap 밖의 via 는 실패다.
python3 engine/check_via.py --gate || { echo "  [FAIL] check_via"; fail=1; }
(cd engine && python3 check_contracts.py) || fail=1
# 인용 앵커 (C33). 앵커 구절이 대상 문서에서 정확히 1회 매치돼야 한다 — 0회는 썩음, 2회 이상은 애매.
# 줄번호 인용은 아직 실패시키지 않고 미이행으로 센다(배치 이행 중). 체커 자기검증은 test_check_refs.py.
# 밴드 규칙 (C32). 세 상태 · 출처 없는 폭 거절 · 묶음 불가분 · 선택지 요건이 앵커다.
(cd engine && python3 test_bands.py) || fail=1
(cd engine && python3 test_albedo_table.py) || fail=1
(cd engine && python3 test_greenhouse_cases.py) || fail=1
(cd engine && python3 test_sub_neptune_dynamo.py) || fail=1
(cd engine && python3 test_stellar_wind.py) || fail=1
# 임시값 가드레일 다섯. ⑤ 는 레시피가 도착하면 FAIL — 그 발화를 시험이 오늘 증명한다.
(cd engine && python3 test_tidal_locking.py) || fail=1
(cd engine && python3 test_provisional.py) || fail=1
# 전이 기록 (Brief 153). 다른 천체의 값은 기록 없이 못 들어오고, state 인데 derived 면(3040 K 모양) 거절.
(cd engine && python3 test_transfers.py) || fail=1
# 정의역·방향 (Brief 155, C48). 법칙의 정의역은 callee 가 지켜 소비자가 우회 못 하고, 한계의 방향은 필드에서 부호가 난다.
(cd engine && python3 test_domain.py) || fail=1
(cd engine && python3 test_check_refs.py) || fail=1
python3 engine/check_refs.py || fail=1

if [ "$lane" = "wiring" ]; then
  echo ""
  echo "── 13–14 물리 시험 건너뜀 (wiring 층). 코드가 바뀐 커밋에서는 절대 건너뛰지 않는다 ──"
else

echo ""
echo "── 13. 엔진 그래프 + 역류 층 ──"
# chain.yaml 은 방법론끼리의 의존, bindings.yaml 은 이미 출하된 확정값이 어느
# 노드에서 나왔고 무엇이 그걸 먹는지. 후자가 없어서 Proxima pause_nose 사고가 났다.
python3 engine/chain.py check || fail=1
python3 engine/backflow.py check 2>&1 | grep -v "^  \[WARN\]" || true
python3 engine/backflow.py check >/dev/null 2>&1 || fail=1
(cd engine && python3 test_backflow.py) || fail=1
(cd engine && python3 test_dynamo.py) || fail=1
(cd engine && python3 run.py bodies/alpha_centauri_a_b.yaml) || fail=1
(cd engine && python3 run.py bodies/pandora.yaml) || fail=1
(cd engine && python3 run.py bodies/earth.yaml) || fail=1
(cd engine && python3 test_mass_radius.py) || fail=1
(cd engine && python3 test_fermi.py) || fail=1
(cd engine && python3 test_water_hot.py) || fail=1
(cd engine && python3 test_ammonia.py) || fail=1
(cd engine && python3 test_water2.py) || fail=1
# ⚠ ANSWER 시험 — 게이트에서 가장 긴 단일 구간(약 459 초, 전체의 31 %)이고, 그 시간이 사는 곳이다.
# 이 시험만이 엔진을 **현실**과 대조한다. 자기 헤더가 그렇게 적는다 — 앵커는 전부 측정값이고
# (반지름은 측지, C/MR² 는 중력장·세차), "우리 출력으로 우리를 시험하면 아무것도 검증되지 않는다".
# 다른 시험들은 배선이 도는지 본다. 이것은 답이 맞는지 본다.
# ⇒ 층을 나눌 때 **"느린 시험"으로 분류해 빼면 안 된다.** 뺄 수 있는 유일한 경우는 코드가 하나도
#    안 바뀐 커밋이고, 그 판단은 사람이 아니라 바뀐 경로 목록이 한다 (12b 위 주석 참조).
(cd engine && python3 test_interior.py) || fail=1
# 얼음거대행성 앵커. 천왕성·해왕성을 실제로 풀어(각 ~50 초) 굳힌 값과 비트까지 대조하고,
# 격자 위상·격자 수렴도 본다. 답을 바꾸는 작업은 --refresh 로 다시 굳혀 diff 에 남긴다.
(cd engine && python3 test_ice_giant.py) || fail=1
(cd engine && python3 test_core_state.py) || fail=1
(cd engine && python3 test_body_class.py) || fail=1
(cd engine && python3 test_porosity.py) || fail=1
(cd engine && python3 test_giant.py) || fail=1
(cd engine && python3 test_mixture.py) || fail=1
(cd engine && python3 test_rocky_roster.py) || fail=1
# 조석 수송 축 (Brief 35). 이오 재현 실패가 측정 불변량으로 고정되어 있다 —
# 이 테스트가 울리면 실패 서사 자체가 바뀐 것이니 멈추고 추적한다.
(cd engine && python3 test_tidal_transport.py) || fail=1
# 규산염 녹는곡선 사슬 (Brief 36). 전사 검산과 이음매 계단이 측정 불변량이다.
(cd engine && python3 test_silicate_melt.py) || fail=1
# 도형 완화 판정 (Brief 39). 전사 검산·문턱 가족의 불감성·라벨·지구 판정이 앵커다.
(cd engine && python3 test_rheology.py) || fail=1
# 밀도 적합 ↔ 녹는곡선의 조성·물질상 선언 (Brief 41). 다른 조인을 말없이 잇는 상이 생기면 여기서 잡힌다.
(cd engine && python3 test_eos_joins.py) || fail=1
# 방사성 예산 (Brief 44). 초안 표의 폐합 세 건·캡션 오독 11.59 TW·과거 방향 3.67 이 앵커다.
(cd engine && python3 test_radiogenic.py) || fail=1
# 함의 열류 일관성 (Brief 46). Table 2 전사 폐합(42 TW ← 1614 K)과 ζ 양방향 민감도, 판정 라벨이 앵커다.
(cd engine && python3 test_mantle_flux.py) || fail=1
echo "── CMB 열류 (Nimmo 식 37–39 폐합 · 단열 열류 · 거절 라벨) ──"
(cd engine && python3 test_cmb_flux.py) || fail=1
# 핵 에너지 수지 (C14). Nimmo 해석 핵으로 Table 4 성분별 재현·근 4152 K, 엔진 지구는 보고, 내핵 두 분기, 거절 라벨이 앵커다.
(cd engine && python3 test_core_energy.py) || fail=1
# 핵 엔트로피 생성 φ (C15). Nimmo 해석 핵으로 Table 4 의 여섯 엔트로피 항 성분별 재현, 엔진 지구는 밴드로 보고, 내핵 두 분기, 3 Gyr 거절 라벨이 앵커다.
(cd engine && python3 test_core_entropy.py) || fail=1
# 열진화 적분기 (C20). 지구 단일 실행(h = min(4 Myr, 0.1·τ) — Nimmo 의 4 Myr 은 상한, 브리프 157)이 사전등록 분기 ①②④③ 을 그 순서로 읽는다; 수렴 스윕은 온디맨드(--sweep, ~400 s).
(cd engine && python3 test_core_history.py) || fail=1
# 페이로드 등급 계약 (2026-09-04 오너 결정). authored 는 두 표지(gap:, consistent-with:) 없이는 생성되지 않는다.
(cd engine && python3 test_payload.py) || fail=1
# 상 곁표 (2026-09-04, 오너 채택 패턴). 키 집합 = eos 가 내는 상, 채운 칸은 등급·출처, authored 는 두 표지, 채움/전체를 출력한다.
(cd engine && python3 test_phase_tables.py) || fail=1
# 조석 가열 (C30). 이오 밴드 재현·판도라 보드 45 W/m² 재현(0.75 %)·×Io 규약 R⁵·§6.1/§6.2 라벨 표·거절 넷이 앵커다.
(cd engine && python3 test_tidal_heating.py) || fail=1
# 정체뚜껑 스케일링 (C47 (f), brief 148 단계 1). Korenaga 2009 Table 2 Δη=1 10행 eq. 29 대조가 앵커다
# — 이 엔진이 가진 유일한 행별 앵커이고, 절대 스케일에는 앵커가 없다(C47 (c)·(e)).
(cd engine && python3 test_stagnant_lid.py) || fail=1
# C47 4단계 방향 시험 (브리프 162). 기본 모드가 **현재 커밋의 기대표**를 검사한다 — 09-07 앵커는
# `--anchors` 로만 요구하며 커밋 1 에서만 통과한다. 판정은 C47 (k) 커밋 6 에 있고 여기서는 회귀만 막는다.
# ⚠ 게이트 시간에 ~62 s 를 더한다 (eq. 56 고정점이 1500 °C 행에서 120여 회 반복).
(cd engine && python3 tools/c47_step4.py --quiet) || fail=1
# C24 (2026-09-04). 물 기둥의 IF97 후보(마지막)·두 이음매 ≤ 0.05 %·얼음 0 양성 대조·물 많은 암석체 0.1/0.3.
(cd engine && python3 test_water_column_steam.py) || fail=1
# 암석 다이나모 사다리 (Brief 47). 문서 표 재현·RM22 Table 8 차이·게이트 라벨·격자 미선출이 앵커다.
(cd engine && python3 test_dynamo_rocky.py) || fail=1
python3 engine/dynamo_table.py --check || { echo "  [FAIL] dynamo_table"; fail=1; }

fi   # lane

echo ""
if [ $fail -eq 0 ]; then
  echo "──────── 모든 점검 통과 ────────"
else
  echo "──────── 일부 점검 실패 ────────"
fi
echo "GATE END sha=$gate_sha pid=$$ at=$(date +%T) lane=$lane rc=$fail"
exit $fail
