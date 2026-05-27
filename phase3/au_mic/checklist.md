# 작업 체크리스트 — AU Mic 행성 b, c, d, e Phase 3 합성

## Stage 1 — pre-flight + 결정 분류
- [x] Phase 2 입력 확인 (`db/systems/au_mic.json` 큐레이션 완료)
- [x] Host star synthesis 검토 (`docs/phase3/au-mic.md`)
- [x] AU Mic e의 `pl_controv_flag=1` 정책 — 모든 행에서 Confidence=low 처리
- [x] 행 분류 (context-notes.md)

## Stage 2 — 영문 마크다운 초안 작성
- [x] `docs/phase3/au-mic-b.md` (hot Neptune, atmosphere retention 핵심)
- [x] `docs/phase3/au-mic-c.md` (sub-Neptune, 후퇴된 H/He envelope)
- [x] `docs/phase3/au-mic-d.md` (TTV-only Earth-mass 후보)
- [x] `docs/phase3/au-mic-e.md` (Donati 2025 candidate, 논란)

## Stage 3 — 한글 미러
- [x] `ko/docs/phase3/au-mic-b.md`
- [x] `ko/docs/phase3/au-mic-c.md`
- [x] `ko/docs/phase3/au-mic-d.md`
- [x] `ko/docs/phase3/au-mic-e.md`

## Stage 4 — block-parity + HTML 빌드
- [x] check_block_parity au-mic-b
- [x] check_block_parity au-mic-c
- [x] check_block_parity au-mic-d
- [x] check_block_parity au-mic-e
- [x] build_html.py au-mic-b
- [x] build_html.py au-mic-c
- [x] build_html.py au-mic-d
- [x] build_html.py au-mic-e

## Stage 5 — verify
- [x] `bash scripts/check-mirrors.sh` exit 0
