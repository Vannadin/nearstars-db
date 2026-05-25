# nearstars-phase3 SKILL.md 슬림화
# Plan

Date: 2026-05-22
Workspace: `.agents/skills/nearstars-phase3-workspace/`
Live skill: `.claude/skills/nearstars-phase3/` (가동 중인 다른 세션 보호 — 작업 종료 후 스왑)

## Problem

`SKILL.md` 가 609줄로 skill-creator 권장 상한 500줄을 초과. 본문 안에
references/ 와 중복되는 인라인 템플릿/표, frontmatter description 과
중복되는 Trigger Recap, Step 본문과 중복되는 Phase 3-specific policies
섹션이 누적되어 있음. 메인 절차 (Step 0–14) 의 가독성을 떨어뜨려
Step 9.0 같은 mandatory 게이트가 묻힐 위험.

## Goal

- 본문은 *절차 + 판단 트리거* 만 유지, 깊이 있는 참조는 references/ 로
- 605줄 → 500줄 이하
- 동작상 동등 (모든 Step, 모든 policy 분기 보존)
- 다른 세션 가동 중이므로 live 는 건드리지 않고 draft 만 편집

## Approach (9 후보)

### Trim (본문 → references 또는 압축)

1. `## Trigger Recap` (15줄) → 3줄 — frontmatter description 과 중복
2. Step 5 스코어 테이블 (7줄) → 1줄 — scoring-reference.md 가 본판
3. Step 9.1 인라인 markdown 템플릿 (~26줄) → 헤딩 리스트만 — synthesis-template.md 본판
4. Step 9 Dual-track 단락 (~23줄) → 진단 질문 + 분기만 — conflict-resolution.md 본판
5. Step 10 오류 사례 4개 (~10줄) → conflict-resolution.md 로 이동
6. `## Phase 3-specific policies` (25줄) → 메모리 슬러그 4줄
7. `## Related documents` (19줄) → 5줄

### Compress (간단한 단락 정리)

8. Step 0 본문 (3단락) → 표 + 1단락
9. 인트로 + Scope 박스 중복 → Scope 박스만 유지

## Out of scope

- 다른 references/*.md 파일 수정 — 후보 5에서 conflict-resolution.md 에
  failure-mode 추가하는 것만 예외
- live skill 디렉터리 수정 — 사용자 승인 후 별도 단계에서 스왑
- 동작 변경 (Step 추가/삭제, policy 분기 추가) — 이번 작업은 *형태만*

## Verify

1. draft/SKILL.md 줄 수 ≤ 500
2. Step 0–14 의 14개 step 이 모두 보존
3. Step 9.0 mandatory 분류 게이트가 압축 후에도 또렷이 보임
4. references/ 4개 파일의 포인터가 본문에 모두 살아있음
5. (선택) 빈 세션에 draft 만 로드해서 "TRAPPIST-1 e 분류표 만들어줘" 프롬프트로
   Step 9.0 트리거 확인

## Out of this session

다른 세션 작업 종료 후 `mv draft/* live/` 스왑 — 별도 단계
