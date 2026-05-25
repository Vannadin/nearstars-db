# plans/ — 연구 노트

이 디렉터리는 **연구 노트** — DB 파이프라인, 스키마, 생성되는 cfg에는
(아직) 변경을 만들지 않는 일회성 조사 — 를 담는다.

코드나 데이터에 영향을 줄 작업이라면 여기가 아니다.
`phase2/<topic>/` 의 plan / checklist / context-notes 삼위일체를
사용하라. 판단 룰은
[AGENTS.md §2](../../AGENTS.md#2-document-hierarchy) 참조.

---

## 여기 들어가는 것

- upstream mod (Principia, Kopernicus, Persistent Thrust, …) 의 소스
  코드를 읽고 학습한 내용 정리.
- 출판된 논문의 방법론 학습 및 발견 사항 기록.
- 아직 구현 승인되지 않은 아이디어의 스코핑.
- 외부 데이터 소스 통합 결정 전 비교.

## 여기 들어가지 않는 것

- 체크리스트가 있는 능동적 구현 작업 → `phase2/<topic>/`
- 영구 reference 문서 (schema, methodology, format spec) →
  `docs/reference/`
- 향후 몇 세션 내에 코드/데이터 델타를 만들 plan → `phase2/<topic>/`

---

## 파일 컨벤션

1. **주제 하나당 파일 하나.** `plans/<short_kebab_topic>.md`.
   서브디렉터리 사용 금지.

2. **frontmatter 에 checklist 필드 없음.** checklist 는 구현 진행을
   함의. 연구 노트는 서술적이지 진행 추적용이 아니다. checklist 가
   필요하다고 느끼면 사실은 구현 작업을 하고 있는 것 — `phase2/<topic>/`
   로 이동.

3. **레포 상대경로만 사용.** `/home/<user>/...` 나 `C:\...` 금지.
   외부 코드 인용 시 GitHub URL.

4. **첫 문단에 NearStars 와의 연관성 명시.** 이 연구가 NearStars 에
   왜 중요한가. 없으면 이 레포에 있을 정당성 없음.

5. **템플릿에서 시작.** [`_template.md`](_template.md) 참조.

6. **영어가 source, 한글 미러는 `ko/plans/` 에.**
   [AGENTS.md §2.1](../../AGENTS.md#21-bilingual-mirror--ko-tree) 참조.
   연구 노트는 영어로 작성, `ko/plans/<same-name>.md` 로 미러. `ko/plans/`
   는 아직 없으면 첫 번째 plan 때 생성.

---

## 생애주기

`plans/` 문서의 상태는.

- **Active** — 현재 사이클에서 읽히거나 확장되는 중.
- **Promoted** — 영구 위치로 이동됨. `phase2/<topic>/` (active
  implementation) 또는 `docs/reference/` (장기 reference 문서, `ko/docs/reference/`
  미러 동반). **원본 `plans/` 파일은 같은 commit 에서 삭제한다.**
  archive 폴더 없음, stub redirect 없음. commit 메시지에
  `promoted from plans/<name>.md` 한 줄을 포함시키면 `git log` 가
  archive 역할.
- **Archived** — 대체되거나 폐기됨. 삭제. `git log` 가 히스토리를 보존하므로
  필요 시 `git log --all --full-history -- plans/<name>.md` 로 복원 가능.

연구 노트에는 "완료" 상태가 없다. reference 로 여전히 유용하거나 아니거나
둘 중 하나.
