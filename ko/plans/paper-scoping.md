<!-- NearStars 논문화 탐색 단계 스코핑 노트 — 네 기둥별 주장/보유/공백 정직 정리 -->
# NearStars 논문화 — 스코핑 노트 (탐색 단계)

**상태:** ⏸ **PARKED (2026-06-18).** 사용자 결정 — 현 단계 액션은 "context-notes를 앞으로 더 꼼꼼히 쓰기"로 한정. 논문화는 탐색 기록만 남기고 능동 작업 없음. 재개하려면 이 문서가 출발점.
이 문서는 "무엇이 논문이 되고 무엇이 안 되는가"를 정직하게 정리해 둔 탐색 기록.
**작성:** 2026-06-18
**사용자 의향:** 프로젝트 전체 과정을 논문으로. 네 각도 전부 관심 — 재현 파이프라인(방법) · 다중성계 에포크 전파 · 균일 안정성 재검증 · 외부 관측자 벤치마크.

---

## 0. 큰 전제 (먼저 못 박을 것)

NearStars의 값 대부분은 **기존 출판 측정치의 재큐레이션·재유도**다. 새 관측이 없으므로 "별/행성에 대한 새 천문학적 발견"은 주장 불가. 논문의 신규성은 반드시 **방법 · 합성 · 재현성 · 교육** 축에 있어야 한다.

두 가지 함정.
- **라이선스**: 프로젝트는 CC-BY-NC-SA 4.0. NC는 OSI 승인이 아니라 JOSS 등 일부 오픈사이언스 venue의 라이선스 요건과 충돌. 소프트웨어-논문 트랙에서 실질 걸림돌.
- **측정 vs 합성 분리**: Phase 3 합성/아트 디렉션은 측정치가 아니다. 논문에서 섞이면 과대주장. "측정 게이트 위에 올린 art-direction 레이어"로 명확히 분리해 서술해야 함.

## 1. 실측 규모 (논문 본문에 들어갈 숫자)

- 시스템 파일 **157**개 (다성계는 컴포넌트별 1파일 레이아웃)
- 행성 **227**개
- `binary_orbit` 노드 보유 파일 **27**개 (다중성 처리가 실재함을 보여주는 수)
- 50광년 내 필드 별 레이어 **1314**개 (SIMBAD 척추 + Gaia 색)
- 안정성 시뮬레이션 결과 **13** 시스템
- Phase 3 웹 리포트 **78**개
- 외부 관측자 벤치마크 문서 1편 (13 KB, 완료)
- 출처 캐시: `docs/phase3/_papers`

> 주의: arxiv id 직접 검색은 24건만 잡혔으나 bibcode 인용은 별도라 실제 출처 커버리지는 더 높을 것. 논문화하려면 **"전체 값 중 출처 핀 비율"을 정확히 산출**해야 함 (provenance coverage 지표).

## 2. 네 기둥 — 주장 / 보유 / 공백

### 기둥 1. 재현 파이프라인 (방법) — *논문의 중심*
- **주장**: 출처추적형 종단 파이프라인. 측정치(arxiv/bibcode 핀 curation) → strictly-derived 레이어(단위변환·우선순위머지만, 기본값 가정 금지, null 보존) → Phase 3 합성(documented divergence) → 결정론적 cfg emit. 재현성은 check.sh 6종 게이트 + canonical JSON으로 강제.
- **보유**: 데이터 계약 SPEC, check.sh, _naming 단일모듈, build_systems strictly-derived 불변, 157계/227행성.
- **공백**: (a) 아키텍처 다이어그램 1장. (b) "한 명령으로 DB→cfg 재빌드" 재현성 선언 + 실측. (c) provenance coverage 정량화. (d) 기존 ad-hoc 방식 대비 비교표.

### 기둥 2. 다중성계 에포크 전파 — *차별점*
- **주장**: 계층적 다체 천문측정 전파 Kepler→Thiele-Innes→ICRS + 에포크 처리. REX·Stellarium이 제대로 못 하는 부분 (= NS 존재 이유).
- **보유**: `binary-epoch-pipeline.md` 레퍼런스, binary_orbit 27계, α Cen·Sirius 워크드 예시, REX·Stellarium 비교 문서 2편.
- **공백**: **검증 figure** — α Cen 예측 분리각/위치각(separation–PA)을 orb6 ephemeris와 시간축 비교, 오차 정량화. 지금은 "한다"는 서술만 있고 "맞다"는 그림이 없음.

### 기둥 3. 균일 안정성 재검증 — *검증 결과 A*
- **주장**: 근접 다행성계를 단일 정책으로 REBOUND 재검증(WHFast+MEGNO 스크린 → TRACE/IAS15). 3축 판정(생존/카오스/이심률 등급). 추가로 Msini→진질량 경계 스캔으로 동역학적 질량·경사각 제약 도출(바너드 선도 사례).
- **보유**: 13계 실행, STABILITY_REPORT, α Cen 경계 스캔, 에너지/MEGNO sanity, TRAPPIST-1 vs Agol+2021 교차검증.
- **공백**: **바너드 4행성 재실행 + 경사각 경계 스캔** (현재 summary는 b 1개만 담긴 stale 본 — F1 복구 이전). 전 다행성계 균일 표. 각 계의 출판 안정성 주장과 대조.

### 기둥 4. 외부 관측자 벤치마크 — *검증 결과 B*
- **주장**: 10pc 관측자가 동일 Phase 2/3 방법으로 태양계 바디에 대해 추론 가능/불가능한 것의 캘리브레이션. 신뢰도 등급 ↔ 관측가능성 1:1. 킬러 결과: 금성 온실 블라인드(Teq 227–299 K vs 실제 737 K).
- **보유**: 완성 문서 1편(13 KB, 2026-06-03).
- **공백**: methods-validation 섹션으로 재프레이밍. (선택) 바디 1개 클래스 확장.

## 3. 권고 형태

**단일 방법론 논문 (astro-ph.IM)** 으로 묶는 게 가장 자연스럽다.
- 기둥 1 = 방법 본체
- 기둥 2 = 차별점(왜 기존 도구로 안 되는가)
- 기둥 3·4 = 두 검증 결과
- arXiv 프리프린트로 먼저 DOI 확보 → 이후 IM 정식 심사 또는 RNAAS 단문으로 분할 승격 가능.
- **RNAAS 폴백**: 기둥 3 또는 4 하나만 ~1000단어로. "논문 냈다" 첫 경험에 최적.

## 4. 가장 싼 다음 한 걸음 (탐색·프로젝트 동시 이득)

**바너드 4행성 재검증 + 경사각(→진질량) 경계 스캔**을 끝낸다.
- 구체적 결과 1건 산출 + 안정성 기둥 최대 공백 메움 + "균일 안정성 서베이"가 기둥으로 설 수 있는지 시험.
- 부산물: 방법론·결정·근거를 stability-sim `context-notes.md`에 이어 기록(아까 우려한 방법론 기록 규율의 실천).

## 5. 미결 질문

- 저자 구성? Schultz(Principia)·Firefly 기여자 포함 여부.
- provenance coverage 목표치(예: 측정치 95% 이상 출처 핀)를 게이트로 둘지.
- 라이선스: 논문 부속 코드 릴리스를 위해 코드 부분만 OSI 라이선스로 분리할지(DB/아트는 CC-BY-NC-SA 유지).

## Related
- [stability-sim STABILITY_REPORT](../../phase3/stability-sim/STABILITY_REPORT.md)
- [external observer benchmark](../../docs/reference/solar-system-external-observer.md)
- [REX 비교](../../docs/reference/rex-data-comparison.md) · [Stellarium 비교](stellarium-binary-orbit-comparison.md)
