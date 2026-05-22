# SKILL.md 슬림화 — 의사결정 로그
# Context notes

## Why now (2026-05-22)

직전 정책 강화 작업 (Step 9.0 추가, anti-patterns 2개, e/f canonical
example) 으로 SKILL.md 가 609줄까지 늘었음. skill-creator 가이드의
"본문 < 500줄" 권장을 넘어서면서, Step 9.0 같은 mandatory 게이트가
주변 설명에 묻힐 위험. progressive disclosure 원칙대로 깊이 있는
정의는 references/ 에 이미 있으므로 본문 중복분을 정리할 시점.

## Why a workspace (not in-place)

다른 세션이 현재 라이브 스킬을 사용 중. 편집 중인 SKILL.md 를
세션이 다시 읽으면 절단된 상태를 보게 됨. 따라서:

- `live-snapshot/` — 변경 전 기준점 (git stash 대신 명시적 보관)
- `draft/` — 편집 대상
- 작업 완료 + 다른 세션 종료 후에 swap

## 보존 원칙

이번 작업은 *형태만* 바꾸고 동작은 동등하게 유지:

- 새 step 추가/삭제 금지
- 새 policy 분기 추가 금지
- 14개 Step 헤딩 모두 그대로
- Step 9.0 + 9.1 분리 유지 (어제 정책 강화의 핵심)
- references/ 포인터 모두 보존

CLAUDE.md §3 (Surgical Changes) — 슬림화 작업이지만 "튀어나오는
이슈 옆에 있는 것 까지 손대지 말것" 은 동일하게 적용.

## 압축 우선순위의 근거

후보 1–9 중 영향도 큰 것부터:

- 후보 3 (Step 9.1 템플릿) + 후보 6 (Phase 3-specific policies) +
  후보 4 (Dual-track) — 합쳐서 ~60줄. references 중복 가장 큼.
- 후보 1 (Trigger Recap) + 후보 7 (Related documents) — 합쳐서
  ~22줄. frontmatter / 외부 reference 와 중복.
- 후보 2 / 후보 5 / 후보 8 / 후보 9 — 합쳐서 ~30줄. 작은 정리.

## Out of bounds (이번엔 안 건드림)

- Step 11 한글 미러 스타일 테이블 — 자주 직접 참조하는 즉시표
- Step 10 verify 절차 본체 — 가장 사고 많은 step, 두께 유지
- Autonomy guards / Common pitfalls — 이미 콤팩트
- 다른 references/*.md (mod-grounded-fields.md, scoring-reference.md,
  synthesis-template.md) — 본문에서 *덜어내기만* 하고 references 는
  추가 작업 없음
- 예외: conflict-resolution.md 는 후보 5 에서 failure-mode 4개 받음
