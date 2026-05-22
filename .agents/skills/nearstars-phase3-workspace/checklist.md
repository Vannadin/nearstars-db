# SKILL.md 슬림화 체크리스트
# Checklist

## Setup

- [x] 워크스페이스 디렉터리 생성
- [x] live-snapshot 복사 (기준점 보존)
- [x] draft 복사
- [x] plan.md / checklist.md / context-notes.md 작성

## 본문 슬림화 (draft/SKILL.md)

- [x] 후보 1 — Trigger Recap 축약 (15 → 3줄)
- [x] 후보 2 — Step 5 스코어 테이블 압축 (7 → 1줄)
- [x] 후보 3 — Step 9.1 인라인 템플릿 축약 (26 → 8줄)
- [x] 후보 4 — Step 9 Dual-track 단락 압축 (23 → 8줄)
- [x] 후보 5 — Step 10 오류 사례 이동 (10줄 제거)
- [x] 후보 6 — Phase 3-specific policies 압축 (25 → 5줄)
- [x] 후보 7 — Related documents 축약 (19 → 5줄)
- [x] 후보 8 — Step 0 본문 정리 (-5줄)
- [x] 후보 9 — 인트로 + Scope 중복 제거 (-8줄)

## references/ 업데이트 (한 곳만)

- [x] conflict-resolution.md — 후보 5 에서 옮긴 failure-mode 4개 추가 (319 → 333줄)

## Verify

- [~] draft/SKILL.md 줄 수: 609 → **511** (목표 500 ± 11줄 마진)
- [x] Step 0–14 모두 보존 확인 (15 헤딩, 9.0 + 9.1 포함)
- [x] Step 9.0 mandatory 게이트 보존 (line 276)
- [x] references/ 포인터 5곳 + 인트로 박스 4곳 모두 살아있음
- [ ] diff 사용자 검토

## Apply (사용자 승인 후 별도 단계)

- [ ] 다른 세션 종료 확인
- [ ] draft → live 스왑
- [ ] 커밋 (commit message: 한 문장)
