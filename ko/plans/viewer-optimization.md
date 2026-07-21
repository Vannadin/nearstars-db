# 3D 성도 뷰어 — 정리(recap) + 최적화 계획

깨끗한 세션으로 넘기기 위한 인계 문서다. 자체 완결형이며, 뷰어가 하는 일을 정리하고
실행 + 검증할 우선순위별 최적화 계획을 제시한다.

## 상태 (2026-07-21) — surface 간 내비게이션 + field 페이로드

- **surface 간 내비게이션 — 완료.** 문서 surface 네 개(DB `index.html`, 3D `starmap.html`,
  `reports.html`, `firefly-colors.html`)가 서로와 GitHub 위키를 잇는 공용 내비바를 갖게
  됐습니다. `firefly-colors.html`은 들어오는 링크가 없어 고아였는데 이제 도달 가능합니다.
  위키 링크는 상단바만(오너 선택). 주입 위치는 surface별로 다릅니다. `index.html`은 직접,
  나머지는 `build_reports_index` / `render_color_visualizer` / `starmap_template` 생성기.
- **field 레이어 페이로드 — 부분 완료.** 1314개 field 별이 항목마다
  `id`/`is_field`/`distance_pc`/`distance_ly`/`beyond_50ly`를 실었는데 전부 유도 가능하거나
  상수라, 빌더에서 빼고 뷰어가 로드 시 복원하게 했습니다. field 494→373 KB,
  페이로드 1241→1120 KB, 파일 1379→1258 KB.
- **남은 최적화 (플래그, 미완 — 뷰어 수술이 더 위험):**
  - **field `components` (~214 KB).** field 별마다 전체 컴포넌트 객체를 실음
    (name=label, rgb=rep_rgb, is_primary=true, offset_au=[0,0,0], radius_rsun=클래스 프록시,
    그리고 spectype/spec_class/teff_k/vmag_v). 실제 정보는 spectype/spec_class/teff_k뿐이고
    상세 패널(약 1135행)과 AU 스케일 별 메시(약 779행)가 읽습니다. 슬리밍하려면 두 경로 모두에
    뷰어 기본값이 필요하니 브라우저 스모크와 함께 신중히. 남은 최대 절감처.
  - **field 항목마다 `planets:[]` (~18 KB)** — 뷰어가 `c.planets`를 기본값 처리하면 제거 가능.
  - **stability 287 KB** — 2026-06-16의 215 KB보다 다시 커짐(안정성 런을 가진 시스템 증가).
    변형별 캡 + 잔여 부동소수 반올림 재점검.
- **이번 라운드 검증:** 자체검증(157→143 클러스터, 237 행성), 모듈 `node --check`,
  재현성 빌드(md5 동일), dead-link·신선도 게이트 통과. **field 유도 변경에 대한 시각적
  브라우저 스모크는 아직 권장**(마커 1314개 + 상세 패널 + 거리 게이트).

## 상태 (2026-06-16)
- **P1 — payload — 완료.** 안정성 시계열을 variant당 ≤100 스냅샷으로 다운샘플
  (`math.ceil(len/100)`), 행별 시간 컬럼 제거(균일 간격 → 뷰어가 로드 시 variant별
  `t0`/`t_end`로 `t`를 한 번 재구성하므로 하류 인덱싱은 그대로), 반올림 강화
  (e 3dp, 각도 2dp), 쌍성/Kepler 궤적 다운샘플(~154→~110 pts). 재생 증분 0.5→0.25로
  낮춰 스냅샷이 절반이어도 루프 길이를 동일하게 유지. 결과: **payload 793.5→436.5 KB
  (−45%), 파일 882→526 KB (−40%)**; 안정성 553.6→215.4, 궤적 74.0→53.8. ≥100 스냅샷
  하한을 의도적으로 유지(장기(secular) 디테일)했으므로 payload는 ~400이 아니라 ~436에
  안착 — 근사 목표보다 가드레일을 우선했다.
- **P2 — 프레임별 비용 — 완료**(이전, 커밋 `4d2fda0`): 버퍼 재사용 + 일시정지 시
  dirty-skip.
- **P3 — 객체 위생:** 평가 완료 — 런타임 지오메트리/머티리얼 churn 없음(모든 THREE
  객체는 한 번만 생성), 누수 없음; 조치 불필요.
- **P4 — 유지보수성:** 보류(선택, 동작 변화 없음).

파일: `scripts/viz/build_starmap.py`(빌더, `db/systems/*.json`을 읽음) +
`scripts/viz/starmap_template.html`(뷰어; 인라인 JS 1377줄) → `docs/starmap.html`
(자체 완결형, GitHub-Pages 호스팅). 재빌드: `python3 scripts/viz/build_starmap.py`.
JS 문법 검사: 모듈 `<script>`를 추출해 `node --check`.

## 뷰어가 지금 하는 일 (기능, 이번 세션 작업 포함)
- 맵 뷰: ICRS(ly)에 클러스터 스프라이트 143개, 원점에 Sol; AU 시스템 뷰(호스트 별 +
  행성 궤도 + 디스크)로 연속적인 부동소수점 원점(floating-origin) 줌.
- `skyBasis(pos,i,Ω,ω)`로 하늘에 충실한 궤도면(Sol→별 시선 좌표계에서의 궤도 법선).
  디스크는 기울어진 리본으로 렌더.
- **궤도면 폴백**(`hostPlane`): i/Ω가 측정되지 않은 행성은 호스트의 i-측정 행성들
  평균면을, 없으면 디스크면을, 없으면 정면(face-on)을 쓴다(호스트별).
- **안정성 시뮬 패널**: REBOUND 시계열 → 변형(morph)되는 궤도 애니메이션; 재생/슬라이더;
  **confirmed ⇄ candidates variant 토글**(id 기반; variant에 없는 행성은 숨김);
  **차트**(📈): 근점-원점 밴드 + 이심률(오른쪽 축) + 경사각, 부드러운 2차 곡선, 선
  스타일 키, 행성별 구분 팔레트; 큰 차트용 **확대 모달**(⤢); 모바일 미세조정.
- **항성 자전축**: 금색 = 측정 i★(Vega/Fomalhaut는 +PA), 흐린 파랑 = 자전-궤도 정렬
  가정; `spinAxisDir(pos,i★,PA)` + 디스크 법선 재기울임 폴백. 상단 바에서 토글.
- 행성 행 클릭 → 날아가기(fly-to); 열린 상세 패널을 피해 줌 도크가 이동.

## 현재 상태 (2026-06-15 측정)
- `docs/starmap.html` 902 KB; 임베드 JSON payload **813 KB**.
- 키별 payload: **planets 629 KB (77%)**, components 132 KB, disks 1.6 KB.
  - planets 대부분 = **안정성 데이터: 58 variants × ~200 snapshots = 11,550 rows**의
    `[t,a,e,inc,Ω,ω,f]`.
  - components 대부분 = 쌍성 N-body **궤적: 19 arrays, 2923 pts**.
- 프레임별 핫 패스(`tick`→`updateScene`→`updateStability`, 매 프레임):
  - `updateStability`가 활성 궤도마다 `BufferGeometry`를 매 프레임 처음부터 재구성한다 —
    180-세그먼트 타원을 다시 계산하고 rec마다 위치+색용 `Float32BufferAttribute`를 새로
    할당, **일시정지 중에도** 그렇다.
  - `drawStabChart` / `drawBigChart`가 차트/모달이 열려 있으면 매 프레임 캔버스 전체를
    다시 그린다, **일시정지 중에도**(커서가 안 움직이는데도).
  - `updateScene`이 매 프레임 클러스터 143개 전부를 순회한다(글로우/가시성/라벨).

## 최적화 계획 (우선순위순)

### P1 — Payload 크기 (가장 큰 이득; 목표 813 KB → ≤ ~400 KB)
1. **안정성 데이터**(`build_starmap.load_stability` / `_load_stab_dir` 안):
   - variant당 ~100점으로 다운샘플(뷰어가 이미 스냅샷 사이를 lerp하므로 장기 형태에는
     적어도 충분). 현재 `step=max(1,len//110)`은 200을 200으로 남긴다. 상한을 ~100으로
     낮추고, 변형이 여전히 부드럽게 읽히는지 검증.
   - 행별 시간 `t` 제거: 스냅샷이 균일 → variant당 `t_end` + 개수를 한 번 저장하고
     뷰어에서 `t`를 재구성. 7개 컬럼 중 1개 절약.
   - `a`(4dp), `e`(3dp), `inc/Ω/ω/f`(2dp) 반올림 — 대부분 이미 됨; 떠도는 긴 부동소수점
     감사.
   - 예상: ~629 KB → ~250~300 KB.
2. **궤적 / 주전원(epicycle)**(`build_starmap`): 다운샘플(예: ≤120 pts) + 4~5 dp 반올림.
   ~132 KB → ~60 KB.
3. **전역**: 내보내는 모든 좌표/요소를 뷰어가 필요로 하는 최소 dp로 반올림; 공백 없는
   `json.dumps(separators=(',',':'))` 보장. 셀프체크 개수가 변하지 않았는지 확인.

### P2 — 프레임별 렌더링 비용
1. `updateStability`: **버퍼 재사용** — 등록 시 rec별 위치/색 `Float32BufferArray`를 한 번
   미리 할당(seg+1 길이); 매 프레임 기존 배열에 쓰고 `new Float32BufferAttribute` 대신
   `geometry.attributes.position.needsUpdate=true`를 설정. 프레임별 할당/GC 제거.
2. **변한 게 없으면 작업 건너뛰기**: `!stabPlaying`이고 슬라이더/variant가 안 움직였으면
   궤도 재계산과 차트 재그리기를 건너뜀(dirty 플래그 추적). 특히 차트: 매 프레임이 아니라
   `stabIdx`/variant/lang 변경 시에만 다시 그림.
3. 숨겨진 rec(잘못된 variant)은 계산 전에 early-return 확인(이미 일부 적용됨).
4. (선택) `updateScene` 클러스터 순회: 클러스터가 멀거나 보이지 않으면 클러스터별 작업을
   단락(short-circuit).

### P3 — 객체/머티리얼 위생
- 메시가 재구성되거나 시뮬이 닫힐 때 지오메트리/머티리얼을 dispose(반복 열기/닫기 시
  누수 방지). `closeStability` / variant 전환 감사.
- `frustumCulled`은 지오메트리가 호스트-로컬인 곳에만(애니메이션 라인에는 이미 설정됨).

### P4 — 유지보수성 (선택, 동작 변화 없음)
- 템플릿은 인라인 JS 1377줄이다. 단일 자체 완결형 파일을 유지하되(GitHub Pages 제약)
  명확한 배너로 섹션을 나누고, 순수 헬퍼를 한데 모으고, 죽은 코드를 쓸어낸다. 모듈로
  분리하지 말 것(단일 파일 호스팅 모델이 깨진다).

## 검증 (각 P-단계 후 실행)
- `build_starmap.py` 셀프체크 통과(파일 157개, 클러스터 143개, 행성 개수 불변).
- 모듈 스크립트 추출 → `node --check`(문법).
- 재현 가능한 빌드: 두 번 재빌드해도 동일한 `docs/starmap.html`(diff 0).
- 각 단계 전후로 payload 크기 기록(이 문서의 수치가 기준선).
- 수동 스모크(http.server): 맵 로드; TRAPPIST-1 / Alpha Cen / Fomalhaut로 날아들기;
  안정성 시뮬 + 차트 + 확대 모달 + variant 토글 열기; 자전축 토글; 모바일 폭. 다운샘플
  후에도 안정성 변형이 여전히 부드러움.
- `./scripts/check.sh` green(gate-5 docs/wiki 오탐은 기존 문제).

## 리스크 / 가드레일
- 안정성을 너무 멀리 다운샘플하면 장기 디테일(e 진동, 이탈(ejection) 시작)이 사라진다.
  ≥ ~100 pts를 유지하고 Barnard/AU Mic candidate run(구조가 있는 것들)을 눈으로 확인.
- 버퍼 재사용 리팩터는 궤도 렌더링을 조용히 깨뜨릴 수 있다 — TRAPPIST 시뮬을 시각적으로
  검증하고 variant로 숨긴 행성이 계속 숨겨져 있는지 확인.
- 행별 `t` 제거는 균일한 스냅샷 간격을 가정한다 — 현재 run에서는 참이다. 비균일 run이
  잘못 렌더되는 대신 큰 소리로 실패하도록 빌더에서 단언(assert)할 것.

## 범위 / 비목표
- 여기서 새 뷰어 기능은 없다 — 최적화 + 정리뿐.
- 단일 파일, CDN-importmap, GitHub-Pages 모델 유지.
- 빌더의 emit(다운샘플/반올림) 외에 DB / 파이프라인 변경 없음.
