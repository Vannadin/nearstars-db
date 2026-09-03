#!/usr/bin/env bash
# 릴리스 전 일괄 건강 점검 — 수동 실행 전용, 훅 미설치
set -u
cd "$(git rev-parse --show-toplevel)"
fail=0

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
  python3 scripts/build_sitemap.py --audit-only || fail=1
else
  echo "  [SKIP] 사이트가 빌드되지 않은 트리"
fi

echo ""
echo "── 12. 방법론 등재 게이트 (EN 인덱스 / KO 미러 / 위키 포털) ──"
python3 scripts/check_methodology_coverage.py || fail=1

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
# 암석 다이나모 사다리 (Brief 47). 문서 표 재현·RM22 Table 8 차이·게이트 라벨·격자 미선출이 앵커다.
(cd engine && python3 test_dynamo_rocky.py) || fail=1
# chain.yaml 의 via 가 공급자 outputs 에 있는가 (Brief 43). 허용목록(도출 8) · status:gap 밖의 via 는 실패다.
python3 engine/check_via.py --gate || fail=1
(cd engine && python3 check_contracts.py) || fail=1
python3 engine/dynamo_table.py --check || fail=1

echo ""
if [ $fail -eq 0 ]; then
  echo "──────── 모든 점검 통과 ────────"
else
  echo "──────── 일부 점검 실패 ────────"
fi
exit $fail
