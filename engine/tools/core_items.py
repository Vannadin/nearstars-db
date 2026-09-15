# 코어 항목 페이지(아티팩트)를 engine/interior-core.md 의 항목 표에서 직접 만들어 내는 생성기.
"""Core-items page generator — the statuses are read from the ledger, not typed.

    python3 engine/tools/core_items.py <sha>

⚠ **이 파일이 코어 항목 페이지의 정본 생성기다** (지휘석, 2026-09-12). 2026-09-14 (C90) 에
**원장을 직접 읽도록** 고쳤다. 그 전에는 상태 칸까지 손으로 옮긴 목록이었고, masthead 의 sha 는
«그 원장을 읽었다» 는 증거가 아니라 **타이핑된 인자**였다 — 그것이 C90 이 말한 결함이다.

⚠ **이 스크립트가 읽는 것 전부** (지휘석 규칙, 2026-09-14 — 스크립트는 자기 입력을 스스로 밝힌다):

| 입력 | 어디서 | 추적되는가 |
|---|---|---|
| `engine/interior-core.md` 의 항목 표 | `git show <sha>:engine/interior-core.md` | 레포 안 (추적됨) |
| 페이지 머리(HTML `<head>` 와 스타일) | **이 파일 안의 `HEAD_HTML`·`EXTRA_CSS`** | 이 파일 자신 |
| 한글 두 칸(무엇이 문제였나 · 지금은) | 이 파일 안의 `ITEMS` 리터럴 | 이 파일 자신 |

**바깥 파일은 원장 하나뿐이고, 그것도 sha 로 읽는다.** ⚠ 예전에는 머리를 `board-0908.html` 에서
잘라 썼는데 그 파일은 **추적되지 않는 스크래치 파일**이었고 사라졌다 — 그날 생성기는 아예 돌지
못했다 (C90 개정 3). 그래서 지금은 머리가 이 파일 안에 있다. 쓰는 곳은 현재 디렉터리 하나다.

⚠ **옛 사본은 대체됐다** — `…/2ce6256b-…/scratchpad/board/core_items_0912.py` (지휘석 스크래치,
추적 안 됨). 그 파일과 그 옆의 폴백은 더 쓰지 않는다. 정본은 이 경로다 (C90 개정 6).
"""
import html, os, pathlib, re, subprocess, datetime, sys

HEAD_HTML = """<title>코어 항목 목록</title>
<style>
  :root {
    --ground: #F7F8FA; --surface: #FFFFFF; --surface-sunk: #EFF2F6;
    --line: #DCE2EA; --line-strong: #C3CCD8;
    --ink: #131A24; --ink-mid: #3E4A59; --ink-soft: #66727F;
    --accent: #0E7C86; --accent-soft: #E2F1F2;
    --wait: #A85B12; --wait-soft: #FBEEDE;
    --done: #2F6F4F; --done-soft: #E6F0E9;
    --stop: #A6392E; --stop-soft: #FAEAE7;
    --park: #5B6672; --park-soft: #EDF0F4;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --ground: #10151C; --surface: #171E27; --surface-sunk: #1D2530;
      --line: #2A333F; --line-strong: #3A4550;
      --ink: #E4E9EF; --ink-mid: #B3BDC8; --ink-soft: #8391A0;
      --accent: #4FBEC6; --accent-soft: #16333A;
      --wait: #E0A063; --wait-soft: #33261A;
      --done: #6FBF92; --done-soft: #172A20;
      --stop: #E08C81; --stop-soft: #331E1B;
      --park: #8B96A3; --park-soft: #202834;
    }
  }
  :root[data-theme="dark"] {
    --ground: #10151C; --surface: #171E27; --surface-sunk: #1D2530;
    --line: #2A333F; --line-strong: #3A4550;
    --ink: #E4E9EF; --ink-mid: #B3BDC8; --ink-soft: #8391A0;
    --accent: #4FBEC6; --accent-soft: #16333A;
    --wait: #E0A063; --wait-soft: #33261A;
    --done: #6FBF92; --done-soft: #172A20;
    --stop: #E08C81; --stop-soft: #331E1B;
    --park: #8B96A3; --park-soft: #202834;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--ground); color: var(--ink); font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", sans-serif; font-size: 16px; line-height: 1.65; -webkit-font-smoothing: antialiased; }
  .wrap { max-width: 940px; margin: 0 auto; padding: 56px 28px 96px; display: flex; flex-direction: column; gap: 52px; }
  .masthead { display: flex; flex-direction: column; gap: 14px; }
  .eyebrow { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 11.5px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--ink-soft); }
  h1 { font-family: Newsreader, Georgia, serif; font-weight: 600; font-size: clamp(30px, 4.4vw, 42px); line-height: 1.12; letter-spacing: -0.01em; margin: 0; text-wrap: balance; }
  .standfirst { font-size: 17px; color: var(--ink-mid); max-width: 62ch; margin: 0; }
  .strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1px; background: var(--line); border: 1px solid var(--line); border-radius: 3px; overflow: hidden; }
  .stat { background: var(--surface); padding: 16px 18px; display: flex; flex-direction: column; gap: 3px; }
  .stat-label { font-family: "IBM Plex Mono", monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-soft); }
  .stat-value { font-family: Newsreader, Georgia, serif; font-size: 25px; font-weight: 600; line-height: 1.15; font-variant-numeric: tabular-nums; }
  .stat-note { font-size: 13px; color: var(--ink-soft); }
  .v-quiet { color: var(--done); } .v-wait { color: var(--wait); } .v-stop { color: var(--stop); }
  section { display: flex; flex-direction: column; gap: 20px; }
  .sec-head { display: flex; flex-direction: column; gap: 6px; border-top: 2px solid var(--ink); padding-top: 14px; }
  h2 { font-family: Newsreader, Georgia, serif; font-weight: 600; font-size: 26px; line-height: 1.2; margin: 0; letter-spacing: -0.005em; }
  .sec-sub { font-size: 14.5px; color: var(--ink-soft); margin: 0; }
  p { margin: 0 0 10px; max-width: 68ch; } p:last-child { margin-bottom: 0; }
  .prose { color: var(--ink-mid); }
  strong { font-weight: 600; color: var(--ink); } em { font-style: italic; }
  code { font-family: "IBM Plex Mono", monospace; font-size: 0.9em; background: var(--surface-sunk); padding: 1px 5px; border-radius: 2px; color: var(--ink-mid); }
  .chip { display: inline-flex; align-items: center; gap: 5px; font-family: "IBM Plex Mono", monospace; font-size: 10.5px; font-weight: 500; letter-spacing: 0.09em; text-transform: uppercase; padding: 3px 8px; border-radius: 2px; white-space: nowrap; }
  .c-stop { background: var(--stop-soft); color: var(--stop); } .c-wait { background: var(--wait-soft); color: var(--wait); }
  .c-done { background: var(--done-soft); color: var(--done); } .c-park { background: var(--park-soft); color: var(--park); } .c-acc { background: var(--accent-soft); color: var(--accent); }
  .runs { display: flex; flex-direction: column; gap: 0; border: 1px solid var(--line); border-radius: 3px; overflow: hidden; }
  .run { display: grid; grid-template-columns: 46px 1fr auto; gap: 16px; align-items: baseline; padding: 15px 18px; background: var(--surface); border-bottom: 1px solid var(--line); }
  .run:last-child { border-bottom: 0; }
  .run-n { font-family: "IBM Plex Mono", monospace; font-size: 13px; color: var(--accent); font-variant-numeric: tabular-nums; }
  .run-body { display: flex; flex-direction: column; gap: 3px; }
  .run-title { font-weight: 500; font-size: 15px; } .run-why { font-size: 13.5px; color: var(--ink-soft); }
  .run-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 5px; }
  .callout { background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--accent); border-radius: 2px; padding: 18px 20px; }
  .callout.stop { border-left-color: var(--stop); } .callout.wait { border-left-color: var(--wait); } .callout.done { border-left-color: var(--done); }
  .callout-label { font-family: "IBM Plex Mono", monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-soft); display: block; margin-bottom: 8px; }
  .quote { font-family: Newsreader, Georgia, serif; font-size: 16.5px; font-style: italic; color: var(--ink); border-left: 2px solid var(--line-strong); padding-left: 16px; margin: 0 0 10px; max-width: 64ch; }
  .parked { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 9px; }
  .parked li { display: flex; gap: 10px; align-items: baseline; font-size: 14.5px; color: var(--ink-mid); }
  .parked li::before { content: "—"; color: var(--line-strong); flex-shrink: 0; }
  table.grid { width: 100%; border-collapse: collapse; font-size: 13.5px; background: var(--surface); border: 1px solid var(--line); }
  table.grid th, table.grid td { padding: 9px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
  table.grid th { font-family: "IBM Plex Mono", monospace; font-size: 10.5px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-soft); font-weight: 500; background: var(--surface-sunk); }
  table.grid tr:last-child td { border-bottom: 0; }
  table.grid td.num { font-variant-numeric: tabular-nums; white-space: nowrap; }
  .tablewrap { overflow-x: auto; }
  footer { border-top: 1px solid var(--line); padding-top: 20px; font-size: 13.5px; color: var(--ink-soft); display: flex; flex-direction: column; gap: 6px; }
  @media (max-width: 560px) { .wrap { padding: 40px 18px 72px; gap: 42px; } .run { grid-template-columns: 40px 1fr; } .run-meta { grid-column: 2; align-items: flex-start; flex-direction: row; gap: 10px; } }
</style>
"""

EXTRA_CSS = """<style>
  table.grid td.id{font-family:"IBM Plex Mono",monospace;font-weight:500;color:var(--accent);white-space:nowrap}
  table.grid td.q{min-width:26ch} table.grid td.now{color:var(--ink-mid);min-width:26ch}
  table.grid td.dep{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink-soft);white-space:nowrap}
  table.grid tr.st-listed td{color:var(--ink-soft)}
  .grp{margin-top:6px}
</style>
"""

ITEMS = [
# id, state, ko_q(질문/문제), ko_now(지금), depends
("C1","closed","서브넵튠의 가스 외피를 솔버가 다룰 수 있는가, 그 실패 뒤에 숨은 결함은 무엇인가.","가스 30 %까지 풀고 그 위는 이유를 대며 거절. GJ 1214 b를 발표 범위 안에서 재현.",""),
("C2","closed","액체 물 층을 다른 상처럼 적분할 수 있는가, 세 층 역산이 축 하나 이상으로 답할 수 있는가.","바다 상을 걸음 경계에 고정하고 역산은 밴드로 답함. 얼음 앵커 둘은 좁아지고 셋은 아님.",""),
("C3","closed","얼음 재질이 국소 압력·온도가 아니라 천체 분류에서 골라져 융해곡선을 안 보는 구멍.","논문 융해선을 표로 구워 재질을 그것에 대고 고름. 기둥 양끝의 상을 이름으로 적음.",""),
("C4","open","얼음거대행성 외피를 순수 물로 대신하고 있는데, 물–암모니아–메탄 혼합과의 차이가 얼마인지 모름.","암모니아 반은 보유 논문의 상태방정식으로 지음. 메탄 반은 닿는 표가 없음.","C22"),
("C5","closed","거대행성의 희석 핵과 무거운 원소 기울기 외피, 두 잔여물에 책임지는 노드가 없었음.","둘 다 주인 노드를 정하고 하나는 선언 둘을 붙임. 구현은 안 함.",""),
("C6","watch","모든 재질 상태방정식은 근거가 끝나는 곳에서 멈춰야 하고, 천장에 닿으면 이름을 대고 거절해야 함.","영구 감시. 아래에 하위 감시 셋(γ = 1.5, 자기 레이놀즈 수 등).",""),
("C7","closed","완전히 섞이지도 완전히 층지지도 않은 천체를 암석·금속·얼음 혼합 규칙으로 적분할 수 있는가.","거절 유지. 얼음 든 층의 발표된 혼합 규칙도 오차 한계도 없음.",""),
("C8","closed","맨틀 단열선이 논문 검증 하나에만 서 있어 온도 가지를 믿을 수 있는 질량·조성 범위가 불명.","두 번째 논문의 핵–맨틀 경계 단열선으로 독립 검증. 유효 범위 0.8~2 지구질량.",""),
("C9","closed","가열된 천체의 공극을 상한이 아니라 값으로 추정할 수 있는가.","관계식은 있으나 공극 제거 과정 다섯을 빼서 상한만 줌. 행의 옛 추정치 정정.",""),
("C10","closed","얼음 위성 셋이 모든 세 층 밴드 위에 있어, 암석이 가정보다 가벼운(수화·다공) 것으로 보임.","근거 있는 수화암석 상태방정식을 찾아 씀. 축은 실재하나 측정값까지 닿지 않음.",""),
("C11","closed","녹은 깊이를 선언한 정적 천체(아래는 분화, 위는 안 녹은 암석–얼음 지각)를 C7 거절에도 표현할 수 있는가.","발표된 2층 혼합 규칙으로 표현 가능. 선언 쌍은 격자로 두고 하나를 고르지 않음.",""),
("C12","closed","확산 논문의 상태점 표가 물–암모니아–메탄 실제 밀도를 줘서 물 대체의 오차를 잴 수 있는가.","이미지로 읽음. 표는 있으나 그 밀도가 혼합물 것이 아니라 앵커 불가.",""),
("C13","closed","얼음거대행성의 계산 관성모멘트가 발표값보다 한참 낮은데, 퍼지 코어가 그 부호에 맞는 후보.","이름 붙인 거절로 닫힘. 결손은 실재, 축 셋을 재어 각각 이름 댈 수 있는 경계에서 멈춤.",""),
("C14","open","암석 핵이 지금도 대류하는지는 방사성 붕괴 이력만으론 모르고, 열진화가 다이나모 지오섬에 값을 줘야 함.","핵 에너지 균형은 지어져 참조표를 재현하나, 푼 지구가 내핵을 잃음. 간선은 gap.","C20"),
("C15","open","핵–맨틀 경계 열류 공급자는 있는데, 핵 엔트로피 예산과 대류 효율을 거쳐 암석 다이나모로 배선된 것이 없음.","엔트로피 생성은 지어져 논문 항을 재현하나 지구 밴드가 0을 걸쳐 판정 없음. 의도적 미배선.","C14, C20"),
("C16","open","조석고정 천체의 다이나모는 국소 로스비 수가 필요한데, 정의 안 된 양 셋 때문에 가지가 거절돼 있었음.","원 논문을 읽고 거절 하나 철회. 점성과 표 4~5배 불일치 남음, 게이트는 임시로만 닿음.","C36"),
("C17","open","바다 비율을 소비자 셋이 읽는데 아무 노드도 내지 않고, 셋이 뜻하는 것도 다름(표면 물, 지하 바다, 물 분류).","측정 후 일부 재개. 작지만 실재하는 온도 전환 있음, 메커니즘 문장은 인용 없음, 배선 없음.","C24"),
("C18","closed","서브넵튠은 구조는 풀리는데 다이나모 가지가 없어 철핵의 자기 모멘트를 계산할 곳이 없음.","거절로 닫힘. 세기 스케일링이 미발표라 간선 소멸, 존재 질문은 C23으로.",""),
("C19","closed","거대행성 다이나모가 질량·나이의 냉각 광도를 원하는데 아무 노드도 내지 않았음.","거대행성은 이미 나이로 배선돼 있었고 라벨만 틀림. 갈색왜성 가지는 측정 복사광도로 지음.",""),
("C20","built","핵의 현재 상태를 한 시점의 근 찾기로 닫고 있었고, 온도를 역사 따라 앞으로 적분하는 것이 없었음.","열이력 적분기를 열한 번째 레시피로 지음(사전등록 검사 통과). 엔트로피 밴드는 여전히 0을 걸침.",""),
("C21","open","형성기 단수명 방사성 원소(²⁶Al·⁶⁰Fe)의 가열이 장수명 예산을 지배하는가, 로스터 천체를 분화시키는가.","펄스는 장수명의 9.59배지만 형성 순서상 우리 다섯에겐 없음(오너 결정). 용융 문턱은 열림.","C14, C15, C17"),
("C22","blocked","얼음거대행성 맨틀의 암모니아 비율. 물–암모니아–메탄 혼합의 상태방정식 격자가 필요.","막힘. 인용된 격자가 발표된 적 없어 저자 문의만이 길. 오너 판단.","C4"),
("C23","built","세기는 접어두고, 서브넵튠 철핵이 다이나모를 돌리기는 하는가(발표된 on/off 기준으로).","논문 순서대로 게이트 둘을 지음. 둘째는 '선택 필요'에서 멈추고 세기는 여전히 불가.","C18"),
("C24","built","얼음 비율이 큰 지구질량 암석 천체가 온도 루프의 표면 조건에서 수렴하지 않음.","같은 날 진단·수리. 물 많은 기둥이 수렴하고 C17의 구조 반이 측정 가능해짐.",""),
("C25","listed","지구의 측정 핵–맨틀 경계 온도에서 모형의 핵 열류가 발표 범위 아래고, 범위를 맞추면 내핵이 사라짐.","","C14, C20"),
("C26","listed","얼음 상태방정식의 온도 천장(1800 K) 위에서 물을 어떻게 표현하나. 실제 물질은 유체 또는 초이온.","","C6"),
("C27","listed","중간 얼음 비율 셋(0.05·0.15·0.20)이 지구질량 암석 천체에서 아직 수렴하지 않아 커버리지에 구멍.","","C24"),
("C28","built","다이나모 사다리가 자기 얼음 비율 입력을 0 기본값으로 따로 받는데, 조성 프리셋이 같은 값을 이미 갖고 있었음.","선언이 이기고 없으면 프리셋을 참조. 프리셋도 없으면 0 대신 거절.",""),
("C29","open","천체의 맨틀 포텐셜 온도는 어디서 오나. 없으면 내부가 등온으로 풀리고 핵 상태가 거절함.","오너가 지구 유사값을 선언. 엔진 안에서 도출하는 것은 미착수. 화성 이전은 09-08 검증 통과.",""),
("C30","built","조석 가열된 위성의 온도는 조석 소산이 떠받치는데 내부 열 예산이 그걸 전혀 싣지 않았음.","조석 가열 레시피 + 수송 방식 레시피를 지음. 총열 바닥과 히트파이프 아래 거절 포함.",""),
("C31","built","로스터 위성 하나의 보드 행이 틀린 반지름에서 초안돼 조석값과 파생값이 전부 낡았음.","새 레시피로 갱신하고 날짜 메모. 파생 행은 위성 에너지수지 레시피 전까지 stale 표시.","C30"),
("C32","built","세기류 도출값은 폭의 출처를 단 밴드로 나가야 하고, 묶음 경계마다 오너에게 선택지를 줘야 함(기본값 금지).","구조 지음. 인스턴스 넷 착지, 세어 둔 선택지 약 열 개는 아직 미선택.",""),
("C33","built","인용이 줄번호를 가리켜 문서가 자라면 조용히 어긋남. 체인 간선 참조 대부분이 틀린 줄을 가리키고 있었음.","문서 본문 구절로 해석하는 검사기를 지음. 간선 30 중 24가 틀려 있었고 수리.",""),
("C34","blocked","열수송 표에 어떤 열류 양을 먹일 것인가, 인쇄된 문턱은 출처가 있는가.","C47 닫힘으로 질문이 바뀜 — \"고를 것이 없다\"가 아니라 \"무엇을 선언으로 받을지\". 브리프 163에서 재정의.","C46, C47"),
("C35","listed","항성풍 모듈은 돌아가는데 계약을 담을 방법론 문서가 없어 레시피로 등록할 수 없음.","","" ),
("C36","built","조석고정 노드에 등록 레시피가 없어 소비자 여덟이 기다리는 잠김 플래그가 계산된 적 없었음.","사전등록 답에 대한 A/B로 착지. 이미 시험된 배선 위에.",""),
("C37","closed","암석 다이나모가 자전주기 키를 아무 공급자도 안 쓰는 철자로 조회해 모든 천체에서 None을 받고 그걸 증거로 적음.","코드·계약·체인 라벨·증거 키를 통일. 값이 가지에 든 적 없어 판정은 안 움직임.",""),
("C38","conditional","조석고정 레시피가 상수 위상 지연 모형과 상수 시간 지연 모형을 섞는데 허용 근거가 없음.","기록으로 닫힘. 둘은 명시 안 된 가정 아래서만 일치하고, 둘째 출처는 읽을 수 없는 스캔.",""),
("C39","closed","같은 조석 품질 계수가 한 노드에선 천체별 선언, 다른 노드에선 분류 밴드로, 어느 쪽이 이기는지 규칙 없음.","선언 우선, 분류 밴드는 대체값으로 통일. 판정 안 움직임.",""),
("C40","listed","원하는 출력에서 역으로 맞춘 수는 인쇄값도 선택도 엔진값도 아니라, 값 어휘에 그 말이 없음.","","C32"),
("C41","conditional","이심률 공급 노드가 없어 조석고정 레시피가 0을 넣고 모든 천체를 동기 자전으로 만들었음.","오너가 문서의 미인쇄 틈 안 임시값을 골라, 출력이 분류를 거절하게 됨.","C42"),
("C42","listed","임시값을 풀어주는 가드가 '노드에 레시피가 생기는' 사건을 보는데, 측정 노드엔 그 사건이 영영 안 옴.","",""),
("C43","closed","항성 원반에서 형성되는 행성용 기준(페블 고립)이 위성에 적용되고, 항성 거리는 조용히 기본값.","오너 선택: 위성은 그 가지를 건너뜀. 단위 이름 질문도 함께 닫힘, 값 변화 없음.",""),
("C44","listed","측정 이심률을 담은 필드 이름이 이론적 강제항처럼 생겨, 좌석 둘이 이름만 보고 실측을 의심함.","","C37, C41"),
("C45","listed","계약 검사기가 문서의 Needs를 저자가 타이핑한 증거 키와 대조하고, 레시피가 실제 조회하는 문자열은 안 봄.","09-09 지어짐. 조회 지점 하나에서 (노드·키·hit/miss)를 기록해 세 클래스로 대조. 사전등록 ⓐ는 등록문 자기모순으로 실패 기록. 발견은 C50으로. (f) 09-10: 검사기가 안 세는 기본값 19(어댑터 리터럴 6·시그니처 기본값 19). 리터럴을 지워도 시그니처 기본값은 남음. 아무도 안 묻는 것은 «계약에 그 기본값을 선언한 줄이 있는가». 감사 도구가 검사기 자신의 파서로 재현(19).","C37"),
("C46","conditional","열수송 표에 문헌의 영역 전부가 없고, 발표 분류와 다른 축으로 가름.","플럭스 사다리를 지었다가 천장을 바닥으로 세운 것을 같은 날 정정. 행은 여전히 없음.","C47"),
("C47","closed","수송 표에 방사성 생산을 먹이는데 문턱은 표면 열류로 정의됨. 부정확이 아니라 다른 양.","09-08 이름만 붙여 닫힘. 0단계 통과(얇게), 4단계는 트랜스크립트에서 복구·승격해 판정 — 어느 α도 목표에 닿지 않음(비 1.51 vs 3.68/4.78). 절대 열류 emit은 근거 없음.","C20, C46"),
("C48","closed","열이력 적분기가 지구에서만 검증됐고 화성에서 발산함.","두 반으로 닫힘(09-08). 식의 정의역을 논문에서 선언하고, 적응 걸음 h = min(4 Myr, 0.1·τ)으로 화성이 완주.","C20, C47"),
("C49","listed","한 엔진 안에 핵 열전도도 k 선언이 둘 — 암석은 중점 50 ± 20(선언), 서브넵튠은 중점 거부 밴드 40/100(보정). 서브넵튠 쪽이 금지한 70이 암석 쪽 상단 코너로 쓰임.","09-09 등재. 통일은 오너 결정 ②의 일부. 서브넵튠 인용의 죽은 bibcode도 여기서 발견·정정.","C14, C15"),
("C50","conditional","계약 Needs에 있는데 로스터 어느 천체도 공급하지 않는 키 12개(C37 서명 4 + 호출부가 버티는 8). 계약이 틀렸거나 천체 선언이 빠졌거나.","09-09 등재(C45 도구가 찾음). 네 쌍은 허용목록으로 게이트 통과 중, 수리해 비우면 닫힘. 다섯째 형태(미스인데 상수로 증거 채움) 이름만 붙임.","C45"),
("C51","listed","우리 사슬에 없는 항 — 방사성 발열과 뚜껑 열류를 맨틀 열용량에 묶는 에너지 수지(장기 냉각이 그 결과). 셋째 길의 본체.","09-09 지어짐(브리프 167 A~D). 화성/지구 열류 대비 0.249(측정 0.221)는 재현, 절대값은 두 바디 모두 ~11× 낮음 — 절대 앵커 부재가 측정으로 확정. 칸 ① 실패·② 통과·③ 오너 결정으로 통과. 전이 법칙은 입력 미선언으로 거절.","C20, C47"),
("C52","listed","한 상수가 몇 노드의 재현 앵커에 걸려 있는지 아무도 세지 않음 — 핵 발열 공칭 하나를 바꾸자 열이력 앵커가 움직이고 무라벨 값 여섯이 낡음.","09-09 후보 등재. 첫 계수 6곳. 앵커는 조건에 고정해 수리했으나 결합 자체는 그대로.","C45"),
("C53","built","천체 선언 `stagnant_lid: true/false`를 원전이 «전형적으로 가정되는 이분 분포»라 이름 붙여 반박. 어느 문헌도 이분이 아니고 금성은 다섯 분류가 인쇄돼 논쟁 중.","09-09 저녁 지어짐(브리프 168 A/B, 3867c87d). tectonic_regime 밴드 여섯 + 파생 불리언, 세 천체 출력 비트 동일. contested → 꺼짐(오너 결정), transitional → 판단 불가, episodic/heat_pipe 는 이름 대며 거절(오너 대기). 발견: 화성은 이 축에 닿지 않음 → C54(같은 날 밤 닫힘). 168 C로 C28 순서 불변식 복구·판도라 실값 회귀.","C46"),
("C54","listed","화성의 다이나모 판정은 껍질 축 앞에 «핵이 액체인가»(conductor_phase)를 먼저 보는데 화성은 미정이라 껍질을 어떻게 선언해도 답이 «판단 불가»로 같음.","09-09 밤 뿌리 발견: 핵–맨틀 경계 온도 선언이 지구에만 있었음(172 a). 오너 결정 밴드 1900–2100 K → 중점 2000 K 선언(174, ec001e71). 화성 핵 liquid, 껍질 축이 화성에서 처음 판정(꺼짐), 화성 값 63개 신생, 지구·판도라 비트동일.","C53"),
("C55","open","화성 핵 인쇄 밀도 5.7–6.3 g/cm³(황 13–19 wt%)를 우리 철 재질 둘(fe_prem 7.6–8.2, fe_eps 9.0–9.6)이 못 덮음. Fe–S 상태방정식이 코드에 없음.","09-10 1단계 지어짐: Huang 2023 인쇄값(순철 기준점 + 황 도함수)으로 이원계 재질 둘(황 13·19 wt%), 독립점 재현 0.07 %. 화성 선언 핵질량비 0.24에서 풀림 — 반지름 어긋남 8.9→5.6 %, 관성 2.7→1.4 %, 밀도는 7.0 이상으로 창 밖. 논문 자신이 «이원계는 황 ≥20 % 필요». 2단계 = 다원계 Fe–S–O–C(오너: O 1–4 wt%, C 0.5–1.4, H 미선언), 성공선 = 두 축 최적 핵질량비 간격(0.12)이 줄어드는가. 09-10 저녁 2단계(183): 여덟 조성 인쇄 자릿수 재현(불일치 0). 화성 선언 핵질량비에서 여덟 중 여섯 거절 — 원인은 자료의 압력 바닥(19 GPa), 논문 창에 드는 가벼운 조성이 잘림. 판정선(반지름 3 %·관성 1 % 동시) 여덟 전부 실패: 반지름 최선 3.82 %, 관성 제약 하 6.76 %. «바닥이 가렸는가»=예. 다음: 저압 Fe–S 상태방정식 조사(시간 상자, 없으면 이름 붙은 거절).","C54, C57"),
("C56","closed","지구 액체 철 재질(fe_prem)의 밀도가 온도에 무반응으로 보임(병렬석 관찰).","결함 아님 — ΔT가 선언된 포텐셜 온도에 걸림. 다만 후속 조사(09-10)에서 fe_prem의 열 파라미터(열팽창·격자 비열)가 고체 hcp 철 값이라 액체 비열 보정항이 0.4가 아니라 0.003으로 나옴을 확인 → C58에서 액체 값으로 교체.",""),
("C57","conditional","내부구조 노드가 부르는 풀이 함수 안에 역산(조성 추론) 호출이 하나도 없음 — 역산 분기는 노드 경로에서 도달 불가, 시험과 로스터 스크립트만 부름.","09-10 오너 결정: 화성 핵질량비를 선언하지 않고 솔버가 역산. 182 A 사전등록 착지 — 발견: 조성 미선언은 공백이 아니라 조용한 earth_like 기본값(계약 이름과 코드 이름도 다름), 미선언 넷 중 픽스처 천체는 아무도 선언 안 한 0.325로 답을 냄, 알파센 b의 «철 천장» 거절은 사실 «조성 미선언». 반지름 최적(0.30)과 관성 최적(0.18)이 겹치지 않아 역산은 두 축을 같이 봐야 함. 182 B 구현 중. 182 B(167ac9ee) 푸시: 조성·핵질량비 둘 다 미선언인 천체만 역산, 픽스처는 판별식으로 다공성 축, 알파센 b 거절문 «조성 미선언». 일곱 천체 비트동일.","C45, C50"),
("C58","open","우리 열이력 적분기의 화성 끝점(3763 K, 지구 Nimmo 파라미터 이전)이 화성 문헌 CMB 온도(1900–2100 K)와 1700 K 어긋남.","09-10 재설계: 원인은 값 교체 문제가 아니라 맨틀 상수 여섯·핵 비열·점성 법칙이 지구 값으로 모듈에 박힌 것. 해법을 한 칸 위로 — 재질 층이 P·T에서 비열·단열 기울기를 돌려주게(13 재질 전부 이미 구현, 11개 실수값). 오너 결정: 핵 비열은 Nimmo 상수 840 대신 재질 인쇄값(Huang C_V·α·γ → ≈665–695). 선언은 재질이 못 주는 것만(초기온도·점성 법칙 형식·표면온도). 화성 파라미터 셋은 후보일 뿐 분기 아님. 사전등록 초안 v4.1, 착수는 183 뒤. 09-10 저녁 실측: 같은 핵에 γ 넷 공존(인쇄 2.74 저장만·유도 1.17–2.04가 단열 기울기 몲·core_state 상수 1.5·액체 범위 1.51–1.52), 구조 적분기 대 핵 상태 판정이 같은 핵을 다르게 데움(순철 +51 대 +237 K, 4.64배; Fe–S 등온 대 +541/+674 K). 맨틀 비열 한 양에 셋(1200·1250·1372). 순철 열 매개변수 840·447.5는 둘 다 액체 c_p가 아님(Nimmo 가정 상수·고체 격자). fe_eps는 고체가 맞으니 제외. 사전등록 초안 커밋 전 감사 대조 중. 오너 결정 대기: 액체 철 출처 논문·인쇄 γ 대 유도 γ·K_CORE 범위. 09-10 밤 구현(180 B, eec846df): Dorogokupets 액체 세트는 Huang 두 점에서 밀도 0.5 % 일치·열량 40 % 불일치 → 미채택. core_state·core_energy·cmb_flux가 core_gamma 한 함수를 읽고 빨강 재질은 폴백 1.5(인쇄·카운트·기록된 불일치), 적분기 보류(다섯 천체 +186 K 위험). role='core' 속성 판별. 부수: fe_eps 열팽창 2차 항 누락 수리, 뒤집힘점 0.8722. 오너 결정 대기: 액체 철 열 세트 (i)(ii)(iii). 09-11 새벽 180 C/D(83da7272 푸시): 순철 열 세트 = 압력 분할(≤35 GPa Huang 실측·위 Dorogokupets 등급, 오너 ①). 핵 노드 셋은 core_gamma(빨강이면 폴백 1.5, 경계/중심 갈림 키·카운터), 적분기는 재질 직접(세트 종류별 카운터). 화성 수리(γ 2.87), 지구·판도라·화성 핵 온도 +498/+428/+257 K(세트가 만든 이동, 예전 값 복귀는 구성상 불가). 서브넵튠 GJ 1214 b 회복(발표 대비 1.26→1.69 %), 물 기둥 imf 0.3 회복, imf 0.1은 이름 붙은 거절(원인 = 등급 세트, C69). γ 격차 5.5배→1.33배(두 논문 사이). 오너 검토: 등급 세트 미배달을 적분기까지 넓힐지.","C20, C54, C55"),
("C59","open","화성 핵 반지름·관성모멘트가 보드와 8.9 %·2.7 % 어긋나는데 어느 게이트도 안 잡았음 — 전체 게이트가 화성 출하값을 09-08 이후 한 번도 안 돌렸음.","09-10 기록된 어긋남으로 매 실행 인쇄(허용치·보드값 불변, 판정에 안 셈). 진짜 모양: 관측 1830 km를 재현하려면 핵질량비 ≈0.325가 필요한데 선언은 0.24 — 밀도 프로파일에 대한 진술. Fe–S 19 wt%로 두 어긋남 모두 줄어듦(5.6 %·1.4 %). C55 2단계와 C57이 닫음. 183 실측으로 «0.325 필요»는 철회 — 반지름·관성 최적이 스윕 양 끝에 붙어 간격은 절단 위치를 잼. 판정은 «동시 만족 cmf 존재»로만.","C55, C57"),
("C60","closed","새 Fe–S 재질(19 GPa 기준 아래 근거 없음)로 화성을 풀면 네 칸 전부 거절 — 처음엔 융해 공백으로 오독.","09-10 닫힘. 원인은 시행 걸음이었음: 적분기가 층 경계 아래로 한 걸음 딛어 보고 되돌리는 구조인데 그 버려질 걸음에서, 그리고 사격 괄호의 시행 중심압에서 재질 바닥 거절이 먼저 남. 규칙 교체 — 시행값이 아니라 수렴한 답으로만 판정. 기존 일곱 천체 비트동일. 남는 사실: 재질 바닥이 핵질량비 상한(0.302)을 정하고 그 상한은 물리(CMB = 바닥)에서 옴. (b) 09-10 저녁, 183 B(05da70ad): 같은 모양이 미분 스텐실에서 — k_t 중심차분 하한이 안 막혀 새 재질이 자기 기준압에서 열 성질을 거절. 바닥 클램프로 수리, 19 GPa에서 K_T 49.10 = 해석적 49.09.","C55"),
("C61","built","집계되지 않은 단계가 초록을 만든다 — gate229에서 풀 디렉터리가 사라지자 풀 단계 결과가 집계에 안 들고 rc=0(STEP 71·TIME 19·5분).","09-10 밤 등재·수리(184 B e74afbbb): 풀 디렉터리 부재 → FAIL, 시작/종료 수를 서로 다른 소스에서 세어 불일치 → FAIL, 삭제 주입으로 증명, 귀속 경로(풀 사망 뒤 셈 누락)까지 수리(eec846df). 169 E·C60과 같은 계열의 셋째. 원인 사례는 지휘석의 스크래치 정리.","C60"),
("C62","listed","조석 응답(k₂·Q) 노드가 없음 — 선언 k₂/Q만 있고 층상 점탄성 전파자 부재.","09-10 밤 사전등록 원장 이관(P28 축자). 오너 결정 넷: 액체층(막 한계/거절/보류), 층별 전단탄성률(선언/재질/둘), 레올로지 선출, 이 노드 k₂·Q가 선언값을 대체하는지(기본 emitter, C39 이음매 유지). 첫 빌드는 emitter.","C39, C40"),
("C63","closed","다공성 압밀 φ(P) 법칙이 코드에 없음 — 단테·하데스 반지름 의문의 자리.","09-10 밤 이름 붙은 거절: 보유 논문 일곱이 못 채움 — 넷은 1 MPa 아래 포화, 둘은 φ(P,T,t) 속도법칙, 하나는 충격, Bierson b는 30–80 MPa 적합인데 단테 중심 317 MPa. ²⁶Al 소결은 후보만. P29(8884e29a) 인용. 오너 (a)–(e) 대기.","C22"),
("C64","listed","한 값 키(entropy_history_verdict)를 두 노드가 내고, 읽기 경로에 따라 다른 값이 나옴 — core_entropy의 «cannot-say (needs C20)» 리터럴은 C20 완성 뒤에도 시험에 붙들려 있음.","09-11 사전등록(fbfe6b2a). 감사 실측으로 계약 168 키 중 중복 주장 6(dynamo 짝 셋은 클래스 배타 측정 0건·has_inner_core_solved는 값 일치·radius는 C65로 분리). losing 값을 읽는 출하 소비처 0 → 잠재. 수리는 코드·고정 시험·계약 문장 셋이 함께.","C20, C45, C68"),
("C65","built","radius를 interior_layers와 mass_radius_relation 둘이 내고(화성 −1.87 %, 픽스처 −12.5 %), 승자를 설계가 아니라 실행 순서가 정함 — 소비처 다섯은 오늘 우연히 맞는 값을 받음.","09-11 사전등록. 판정선 = «같은 이름을 두 노드가 내는 것이 허용되는가, 승자는 무엇으로 정하는가». 수리 = 소유자 선언(interior_layers)·mass_radius 출력 개명·순서 무관 시험. 병합 규칙 자체는 C68.","C64, C68"),
("C66","listed","코드 상수 63 중 아무도 안 읽는 것 7·시험만 읽는 것 5·인용만 1(감사 추적표) — 원소 단위(튜플 안 인쇄값) 패스는 예약.","09-11 감사 audit_value_trace. 죽은 GAMMA 별칭은 180 C에서 정리. 나머지는 항목별 브리프(브래킷 점들은 185가 읽게 됨).","C58"),
("C67","listed","core_state._adiabat이 단일 지수 γ(p_c)로 T ∝ ρ^γ를 씀 — 재질 γ가 핵 안에서 압력 따라 변하면(화성 2.87→1.5) 적분해야 함.","09-11 후보. 180 C에서 경계/중심 갈림을 키로 노출(core_gamma_cmb·center·split).","C58"),
("C68","built","두 노드가 같은 이름을 낼 때 resolved 병합 규칙이 «마지막 노드가 이김»뿐 — 소유자 개념 없음.","이름을 갈라 닫음(C68 B, 347f77d2) — has_inner_core(답)와 inner_core_branch_taken(가지). 중복 생산 상수는 9 → 8(fa122569). 게이트가 스스로 «사라진 것»을 인쇄한 뒤 지웠고, 지금은 그 줄이 0건.","C64, C65"),
("C69","listed","온도 고리의 비례 갱신 T_c·T_pot/T_surf가 급한 핵 단열선(등급 세트 γ)+얼음 기둥에서 1 % 근처 진동 바닥 — 물 기둥 imf 0.1 답을 잃음(예산 추가는 답 아님).","09-11 후보. 되돌림 = 완화계수(α<1, 갱신 규칙 변경이라 붙는 천체 경로도 바뀜 → 사전등록 필요). 닫는 열쇠는 고압 액체 철 실측 세트(B47–B51).","C58"),
("C70","listed","얼음거대행성 경로 지문의 감시 목록(함수 7)에 γ 경로 두 함수가 없음 — 값 불변 경로 편집만 지문·값 단정 두 그물을 다 빠져나감.","09-11 후보. 감시 목록 확장 + «감시하지 않는 함수 수» 인쇄. 로스터에 ice_giant·sub_neptune 0이라 감사 기준선에 시험 앵커 천체(천왕성·GJ 1214 b) 추가.","C60, C61"),
("C71","listed","수렴하지 못한 답이 값은 그대로 돌려주고, 경고는 산문 한 줄뿐이라 소비처가 읽을 수 없음.","측정으로 좁힘 — converged 는 값 사전 밖에 있어 구조적으로 닿지 않음. 후보 등재.",""),
("C72","listed","얼음거대행성 둘이 발표 반지름보다 크게 나오는데, 그 격차를 인쇄한 적이 없었음.","기준선으로 등재(천왕성 +5.48 %·해왕성 +8.94 %). ⚠ 판정이 아니라 기록임.",""),
("C73","listed","계약 문서가 돌려준다고 적은 이름을 그래프가 모름 — 층 셋이 서로를 안 봄.","194 가 보고 검사를 지음: 앞방향 39·반대방향 1 을 **집합**으로 고정, 판정은 안 함.",""),
("C74","open","규산염 슬롯이 적합에서 답해, «이 맨틀에 철이 더 많으면» 을 물을 수 없음.","라이선스 답과 설치는 닫힘(191, 별도 환경). 남은 것은 P34 의 A–I.",""),
("C75","closed","표 검사기가 행의 칸 수를 안 세어, 어긋난 표가 통과하고 있었음.","규칙을 넣고 32건 중 31건 수리·1건 이유 등재. 기준선 0.",""),
("C76","listed","깨끗한 나무에서 예외를 던지는 재질 메서드가 어떤 천체 기준선에도 안 잡힘.","평가자 세트에는 c_v_ref 가 없어 0 으로 나누는 자리. 도구 항목으로 등재.",""),
("C77","listed","예산 없는 무한 루프 셋 — 나가는 조건은 있으나 «다 썼다» 가 정의돼 있지 않음.","후보 등재(도구).",""),
("C78","listed","같은 (P, T) 에서 밀도는 답하는데 열 관련 메서드는 이름을 대며 거절함.","암모니아 6칸·물 2칸에서 확인. 후보 등재.",""),
("C79","closed","얼음 VII·X 의 열 답이 아무도 재현 못 하는 스플라인에서 온 상수 두 개였음.","190 이 논문의 인쇄된 자유에너지를 미분해 답하도록 바꿈(HSE 열, 압력 약 1 %).",""),
("C80","closed","풀 배리어가 시한 없이 기다려, 일꾼 하나를 잃으면 판정이 아예 안 나왔음.","195 가 사라진 일꾼에 이름을 붙임 — 죽은 일꾼 즉시, 조용한 일꾼은 천장까지.",""),
("C81","listed","단계 예산이 산문이라 게이트에는 예산이 없음 — 호출 65곳이 이름과 명령만 넘김.","후보 등재(도구). 195 의 천장 하나가 풀 전체를 덮고 있음.","C80"),
("C82","built","등록한 압력 창이 실제 영역보다 넓고, 밖에서는 역산이 조용히 포화됨.","실제 영역은 온도에 따라 달라지는 띠라 압력 한 축으로 적으면 과장. 197 이 클램프를 적힌 가지로 만들고, 190 C 가 벽을 거절 너머로 옮김.","C84"),
("C83","listed","«이건 거절한다» 고 적어 둔 문서 주석이 어떤 점검망에도 안 걸림.","기존 스윕은 수렴 조건만 잡고 거절 주장은 못 잡음. 후보 등재(도구).",""),
("C84","built","열 세트에 온도 상한 칸은 있고 하한 칸이 없어, 아래쪽 경계가 전부 산문임.","런타임 객체 여덟(소스 여섯, 얼음 팩토리가 두 상에서 호출) 중 넷이 상한 선언, 액체 철 둘은 온도 경계 없음. 앵커 평가기 호출의 48.1 %(11 922 중 5 736)가 295 K 아래 — 판정 경로가 아니라 평가기 스트림에서 잰 수. ⚠ «그래서 C82 가 닿는다»는 앞선 문장은 틀림 — C82 는 양쪽 격자 끝에서 발화하는 괄호 모양 문제이고 C84 는 covers_t 의 빠진 끝이며, 평가기 경로는 covers_t 를 아예 안 부름. 스키마는 8e26093e, 하한 선언은 198 B. 190 C 가 이탈을 셀 수 있게 만든 뒤 양성 대조의 답하는 적분 하나에서만 하한이 280 번 넘게 조회됨.","C82"),
("C85","listed","밀도 한 값이 1e-10 움직이면 한 걸음 안에서 인쇄 온도가 1e-5 움직임 — 증폭 약 2×10⁵배.","같은 풀이가 그 흔들림을 다시 흡수해 인쇄 다섯 키는 끝에서 동일. 어디서 흡수되는지는 추적 안 됨. 오너 판단으로 착수 보류.","C82"),
("C86","listed","커밋된 의존 그래프 페이지를 아무 검사도 다시 만들거나 대조하지 않아 조용히 어긋남.","chain.yaml 은 여섯 커밋 움직였는데 페이지는 0c494b05 이후 그대로. 간선 205 대 210, 1 230줄 차이. 개명은 재생성으로 안 지워짐. 후보 등재(도구).","C68"),
("C87","listed","이름에 매달린 감시는 그 몸통이 이름 뒤에서 빠져나가면 눈이 멂.","190 C 가 세 자리를 한 번에 때림 — 지문(__code__), getsource, signature. 이 레포에 세 자리 두 파일. wraps 가 둘을 살리고 지문은 튜플을 넓혀야 함. 후보 등재(도구).","C82"),
("C88","listed","지문이 움직일 때만 다시 굳히는 스냅샷은 변화가 미묘할 때 정확히 그때 낡음.","앵커는 f681afbd 이후 재굳힘 0, 그 사이 얼음 모듈을 건드린 커밋 7. bracket_invalid 가 190 이후 틀린 채였고 대조는 BIT_KEYS 넷뿐(21 중). 후보 등재(도구).","C87"),
("C89","listed","하네스가 CPU 시간·문맥교환·페이지 폴트를 재고 최대 RSS 한 줄만 남기고 버림.","두 경로 다 /usr/bin/time -l 로 돌면서 통계를 지움. 565초 실행의 CPU 값은 코드가 지웠고 복구 불가. 수리는 [COST] 둘째 줄 아홉 칸(커밋 c·d). 후보 등재(도구).","C88"),
("C90","listed","원장을 비춘다는 페이지가 손으로 옮긴 목록이고, 첫 전수 대조에서 열한 자리가 어긋났음.","옮겨적기 뒤집힘 다섯(재생성으로 안 고쳐짐)·접기 손실 여섯·빠진 행 셋. 생성기가 원장을 직접 읽고 대응표를 인쇄하며 못 접는 문구는 거절하는 것이 수리. 후보 등재(도구).","C86"),
("C91","listed","한 번 푸는 동안 `shoot` 이 여러 번 불리는데, 그중 어느 구조가 답인지를 아무도 인쇄하지 않음.","노드 경로 여섯 · dante_fixture 스물둘 · 직접 호출 하나. 답은 `t_center` 가 노드의 `core_temperature` 와 같은 구조다. 첫 덤프가 마지막 것을 떠서 «암석 천체엔 내부 온도가 없다» 고 읽었고 그 읽기는 철회됨. 후보 등재.","C90"),
("C92","listed","재질이 상을 하나 얻으면 `phases[0]` 을 읽는 자리 전부가 조용히 다른 상을 가리킴.","`core_state` 의 다섯 자리가 그렇고, P33 B 가 라벨 경로의 하나만 고쳤음(중심압 48.83 GPa 에서 대조 0 → 1). 오늘 출하 자릿수는 안 움직임(`fe_s_*` 를 고르는 조성 프리셋 0). 후보 등재.","C87"),
("C93","listed","상(相) 기반 재질 스물하나 중 여섯이 첫 상의 `p_min` 을 0 으로 들고 있어, 「바닥이 없다」와 「바닥이 0 이다」가 같은 값으로 읽힘.","여섯 중 다섯은 맞거나 이미 기록된 것이고, `fe_eps` 의 0 은 Seager+ 2007 이 스스로 선언한 선택임. 안 적힌 것은 압력 바닥이 아니라 **열(熱) 유효 범위**이고 그것은 C84 의 축. 그래서 이 항목은 등급 행이 아니라 노트로 섬.","C84"),
("C96","listed","`engine/test_paleos.py` 는 트리에 있는데 그것을 돌리는 게이트 단계가 없어, 누가 손으로 부를 때만 검사가 존재함.","C86 이 오늘 닫은 모양이 한 항목 뒤에서 또 나온 자리. `check.sh` 에 단계 하나(73 → 74)와 `[COST]` 한 줄을 붙이는 것이 사전등록돼 있고, ⚠ **PALEOS 표 셋이 없는 기계에서 그 단계가 이름 붙은 SKIP 을 낼지 FAIL 을 낼지는 오너 결정 칸으로 열려 있음.**","C86"),
("C94","closed","인용 검사가 띄어쓰기 하나와 백틱 하나로 꺼져, 그것을 찾으라고 있는 단계를 갈라 쓴 줄번호와 백틱 붙은 앵커가 그대로 통과함.","검출기 둘을 넣고 인용 24 건을 같은 커밋에서 이행. malformed 8 → 0 · 앵커 560 → 581. `engine/tools/README.md` 한 건은 SCAN 밖이라 원문 유지 — 그 문단이 이 결함의 첫 기록이자 반례.","C86"),
("C95","listed","앵커의 입력 방아쇠가 바이트를 세어, 주석만 고친 커밋과 코드를 고친 커밋이 그것에게는 같은 사건임.","값싼 길 둘(`__code__.co_code` · docstring 없는 AST 해시)을 이름 붙여 재현만 함. 어느 것을 쓸지는 「앵커가 무엇을 약속하는가」라 오너 칸. 코드 변경 0.","C88"),
("C97","listed","쉼표 뒤에 이어 붙인 맨 줄번호는 파일 이름도 `doc` 도 없어 네 그물 어디에도 안 걸림.","크기가 그물에 따라 81 건 19 파일과 47 건 17 파일로 갈려, 한 수로 적지 않고 둘 다 적음. 그물을 정하는 것이 이 항목의 첫 일.","C94"),
("C98","listed","`engine/tools/*.md` 가 `check_refs` 의 SCAN 에 없어 그 파일들은 열리지도 않음.","C94 에서 값을 매겨 분리 — 파일 2 · 줄번호 5 · span 1 · malformed 0. 서식으로 꺼진 규칙과 안 열린 파일은 다른 결함.","C94"),
]


def _repo_root():
    """⚠ **레포는 이 스크립트가 놓인 곳에서 찾는다** — 경로를 박아 두면 다른 체크아웃에서 남의
    트리를 읽는다 (수락선 ⑦a: 도구가 그 체크아웃 안에 있다). `git archive` 를 푼 곳에는 git 이
    없고, 그때는 스크립트가 놓인 곳이 곧 뿌리다."""
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        return subprocess.check_output(["git", "-C", here, "rev-parse", "--show-toplevel"],
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return os.path.dirname(os.path.dirname(here))          # engine/tools → 레포 뿌리


def short_sha(arg):
    """sha 를 짧게 — git 이 있으면 물어보고, 없으면(아카이브) 준 문자열을 그대로 쓴다."""
    try:
        return _sh("git", "-C", os.path.dirname(os.path.abspath(__file__)),
                   "rev-parse", "--short", arg, quiet=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return arg[:8]


REPO = None                      # `main` 에서 `_repo_root()` 로 채운다
LEDGER = "engine/interior-core.md"
TABLE_HEADER = "| # | what it is | state | next step, if open |"

STATE = {"closed": ("닫힘", "c-done"), "built": ("지어짐", "c-done"),
         "open": ("진행·열림", "c-wait"), "listed": ("미착수", "c-park"),
         "blocked": ("막힘·대기", "c-stop"), "watch": ("상시 감시", "c-acc"),
         "conditional": ("조건부 닫힘", "c-wait")}

# ⚠ **접는 규칙은 이 표 하나뿐이고, 표에 없는 문구는 거절한다** (사전등록 §2·§4).
#   첫 낱말 분류는 금지다 — 97 개 후보 칸의 첫 낱말은 서른 가지쯤이고 그중 여럿은 상태가 아니라
#   산문이다(`the` · `whether` · `three` · `a`). 그래서 **구절**로 접고, 우선순위를 숫자로 적는다.
#   우선순위가 필요한 이유: «반은 닫히고 반은 열림» 은 `closed` 와 `open` 을 **둘 다** 품는다.
PHRASE_RULES = [
    # (우선순위, 구절, 칩, 비고 — 페이지에 그대로 인쇄된다)
    (1, "half closed", "open", "부분 닫힘 — 닫힌 반은 칩에서 사라진다"),
    (1, "half open", "open", "부분 닫힘"),
    (1, "dominance closed · differentiation open", "open", "부분 닫힘 (C21)"),
    (1, "stages 1 and 2 built", "open", "부분 닫힘 — 단계가 남았다 (C55)"),
    (1, "open on P34", "open", "일부 축만 열림 (C74)"),
    (1, "as a recorded disagreement", "open", "기록된 불일치는 열린 항목이다 (C59)"),
    (1, "redesigned and pre-registered", "open", "재설계 + 사전등록, 일부는 지어짐 (C58)"),
    (1, "open, one reason of three retired", "open", "이유 셋 중 하나 철회 (C16)"),
    (1, "open (`status: gap`)", "open", "사슬이 gap 으로 표시한 간선"),
    (2, "one row still owner-pending", "conditional", "닫혔으나 남은 것이 있다 (C50)"),
    (2, "prediction 1 stays untested", "conditional", "닫혔으나 남은 것이 있다 (C57)"),
    (2, "rows still absent", "conditional", "닫혔으나 남은 것이 있다 (C46)"),
    (2, "closed by record", "conditional", "기록으로 닫힘 (C38)"),
    (2, "provisional landed", "conditional", "임시값이 들어간 채 닫힘 (C41)"),
    (3, "standing watch", "watch", "닫히지 않는 것이 정의다 (C6)"),
    (3, "held ", "blocked", "다른 결정 뒤에서 멈춤 (C34)"),
    (3, "blocked", "blocked", ""),
    (4, "closed ", "closed", "이름 붙인 거절도 닫힘이다"),
    (4, "resolved ", "closed", "같은 뜻의 다른 낱말 (C43)"),
    (4, "checked ", "closed", "«결함이 아님» 으로 닫힘 (C56)"),
    (5, "structure built", "built", "구조는 지어지고 인스턴스가 남음 (C32)"),
    (5, "built ", "built", ""),
    (5, "existence judged", "built", "게이트가 지어져 판정한다 (C23)"),
    (5, "diagnosed and fixed", "built", "같은 날 진단·수리 (C24)"),
    (5, "landed ", "built", "레시피가 착지함 (C36)"),
    (6, "listed", "listed", "후보 등재 — 아직 안 지어짐"),
    (6, "pre-registered", "listed", "등록됐고 아직 안 지어짐"),
    (6, "named and counted", "listed", "세기만 했고 검사기는 없음 (C52)"),
    (6, "candidate", "listed", ""),
]


def _sh(*args, quiet=False):
    """git 을 부른다. `quiet` 는 **있는지 물어보는** 자리에서만 쓴다 — 아카이브에는 `.git` 이
    없고, 그때 git 의 «fatal: not a git repository» 가 화면에 세 번 찍히면 그 줄이 실패로 읽힌다."""
    return subprocess.check_output(
        args, text=True, stderr=subprocess.DEVNULL if quiet else None)


def ledger_text(sha):
    """원장 본문을 돌려주고, **어디서 읽었는지**를 함께 돌려준다 (수락선 ⑦b·⑧).

    ⚠ **두 경우가 있고 둘 다 이름을 댄다.** git 작업 트리 안이면 `git show <sha>:경로` 로 읽고,
    같은 경로의 작업 트리 파일이 그것과 **다르면 거절한다** — 커밋 안 한 편집을 sha 의 것인 양
    비추지 않기 위해서다. `git archive <sha>` 를 푼 디렉터리에는 `.git` 이 없고, 거기서는 풀린
    **그 파일 자체가 그 sha 의 원장**이라 그대로 읽고 «아카이브» 라고 적는다.
    둘 다 아니면(파일도 git 도 없으면) 거절한다 — 옆에 굴러다니는 파일을 집지 않는다."""
    root = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):                      # engine/tools → engine → 레포 뿌리
        cand = os.path.join(root, LEDGER)
        if os.path.exists(cand):
            break
        root = os.path.dirname(root)
    else:
        cand = None
    try:
        text = _sh("git", "-C", os.path.dirname(os.path.abspath(__file__)),
                   "show", f"{sha}:{LEDGER}", quiet=True)
        if cand and pathlib.Path(cand).read_text(encoding="utf-8") != text:
            sys.exit(f"거절: 작업 트리의 {LEDGER} 이 {sha} 의 것과 다르다 — 커밋하고 다시 부르십시오.")
        return text, f"git show {sha}:{LEDGER}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        if cand:
            return pathlib.Path(cand).read_text(encoding="utf-8"), f"archive 트리의 {LEDGER}"
        sys.exit(f"거절: {LEDGER} 을 git 으로도 트리에서도 못 읽었다.")


def read_items(sha):
    """원장의 **항목 표**를 읽는다 — 머리글 행으로 찾고, 못 찾거나 둘 이상이면 거절한다.

    ⚠ 행 패턴(`^| C숫자 |`)으로 찾지 않는다. 그 그물은 파일 아래쪽 **다이나모 구멍 표**의
    C14–C19 간선 여섯 줄까지 항목인 양 비춘다 (사전등록 §3)."""
    text, _src = ledger_text(sha)
    lines = text.split("\n")
    hdr = [i for i, l in enumerate(lines) if l.strip() == TABLE_HEADER]
    if len(hdr) != 1:
        sys.exit(f"거절: 항목 표 머리글을 {len(hdr)} 번 찾았다 (정확히 1 이어야 한다) — {TABLE_HEADER}")
    i = hdr[0] + 2                      # 머리글 + 구분선
    rows = []
    while i < len(lines) and lines[i].startswith("|"):
        cells = lines[i].split(" | ")
        if len(cells) >= 4:
            ident = cells[0].lstrip("| ").strip().strip("*").strip()
            status = cells[2].strip()
            title = cells[1].strip()
            rows.append({"id": ident, "title": title, "status": status, "line": i + 1})
        i += 1
    return rows, len(hdr)


def net_counts(sha):
    """파일 **전체**에서 «C 번호로 시작하는 표 행» 이 몇 줄인가 — 두 그물로 센다.

    엄격 그물은 번호 뒤에 **칸 벽**을 요구하고, 느슨 그물은 안 한다. 둘의 차이는 소유격 셀
    (`| C20's own reference row | …`)이고, 어느 쪽도 **항목 표가 아니다** — 그래서 이 수들은
    인쇄만 하고 페이지에는 안 쓴다 (사전등록 §3·수정 2). 표 안의 수와 나란히 놓여야
    «무엇이 움직였나» 를 다음 사람이 읽는다."""
    text, _src = ledger_text(sha)
    strict = len(re.findall(r"^\| *\**C[0-9]+\** *\|", text, re.M))
    loose = len(re.findall(r"^\| *\**C[0-9]+\**", text, re.M))
    return strict, loose


def map_phrase(status):
    """상태 칸 → 칩 낱말. **표에 없으면 거절**하고, 여럿 걸리면 우선순위로 가른다."""
    plain = status.replace("**", "").replace("*", "")
    hits = [(pri, ph, chip) for pri, ph, chip, _ in PHRASE_RULES if ph in plain]
    if not hits:
        return None, 0, 0
    hits.sort(key=lambda h: h[0])
    top = [h for h in hits if h[0] == hits[0][0]]
    # ⚠ **두 수를 갈라 돌려준다**: 여러 규칙이 걸린 것과, 그 규칙들이 **서로 다른 칩**을 가리킨 것은
    #   다른 사실이다. 앞은 «같은 말을 두 구절이 담았다» 이고(무해), 뒤만 우선순위가 실제로 판정한다.
    return top[0][2], len(hits), len({h[2] for h in hits})


# ── 본체 ───────────────────────────────────────────────────────────────────────
if len(sys.argv) < 2:
    sys.exit("sha 를 인자로 주십시오: core_items_0912.py <sha>. HEAD 를 조용히 읽지 않는다.")
REPO = _repo_root()
sha = short_sha(sys.argv[1])

rows, header_hits = read_items(sha)
ids = [r["id"] for r in rows]
dups = {i: [r["line"] for r in rows if r["id"] == i] for i in ids if ids.count(i) > 1}
if dups:
    for i, ln in dups.items():
        print(f"거절: 항목 표 안에서 {i} 가 {len(ln)} 번 나온다 — 줄 {ln}", file=sys.stderr)
    sys.exit("거절: 번호가 겹치면 어느 행을 비출지 우연이 정한다 (사전등록 §3, 수정 1)")

unmapped, ties, chip_ties, tie_rows = [], 0, 0, []
for r in rows:
    chip, n, kinds = map_phrase(r["status"])
    if chip is None:
        unmapped.append(r)
    else:
        if n > 1:
            ties += 1
        if kinds > 1:
            chip_ties += 1
            tie_rows.append(r["id"])
    r["chip"] = chip
if unmapped:
    for r in unmapped:
        print(f"거절: 접을 수 없는 문구 — {r['id']} (줄 {r['line']}): «{r['status'][:90]}»", file=sys.stderr)
    sys.exit("거절: 대응표에 없는 문구는 추측하지 않는다 (사전등록 §4)")

PROSE = {it[0]: (it[2], it[3], it[4]) for it in ITEMS}
V19 = {it[0]: it[1] for it in ITEMS}          # ⚠ 옛 손목록의 상태 — **비교용으로만** 쓴다
missing_prose = [r["id"] for r in rows if r["id"] not in PROSE]
diff = [(r["id"], V19[r["id"]], r["chip"]) for r in rows
        if r["id"] in V19 and V19[r["id"]] != r["chip"]]

cnt = {}
for r in rows:
    cnt[r["chip"]] = cnt.get(r["chip"], 0) + 1

strict, loose = net_counts(sha)
print(f"[입력] 원장을 {ledger_text(sha)[1]} 에서 읽었다 · 페이지 머리는 이 스크립트 안")
print(f"[그물] 파일 전체에서 엄격 {strict} · 느슨 {loose} · 표 안 {len(rows)} · 서로 다른 번호 {len(set(ids))}")
print(f"[수락선 ③] C14–C19 의 칩은 항목 표에서 온다 — "
      + " · ".join(f"{i} {STATE[c][0]}" for i, c in
                   [(r["id"], r["chip"]) for r in rows if r["id"] in
                    ("C14", "C15", "C16", "C17", "C18", "C19")]))
print(f"[수락선 ②] 항목 표 머리글 {header_hits} 회 · 읽은 행 {len(rows)} · 서로 다른 번호 {len(set(ids))}")
print(f"[수락선 ⑤] 겹치는 번호 {len(dups)}")
print(f"[수락선 ④] 접은 행 {len(rows)} · 못 접은 문구 0 · 규칙 {len(PHRASE_RULES)}")
print(f"[우선순위] 규칙이 둘 이상 걸린 행 {ties} · 그중 **칩이 갈린 행** {chip_ties} {tie_rows}")
print(f"[수락선 ①] V19 손목록과 다른 칩 {len(diff)}")
for i, old, new in diff:
    print(f"          {i}: 손목록 {STATE[old][0]} → 원장 {STATE[new][0]}")
print(f"[산문] 한글 두 칸이 없는 행 {len(missing_prose)} {missing_prose}")
print("[칩 집계]", {STATE[k][0]: v for k, v in sorted(cnt.items())})

# ── 페이지 ─────────────────────────────────────────────────────────────────────
# ⚠ 머리는 **이 파일 안에 있다** — 바깥 스크래치 파일을 열지 않는다 (C90 수정 3, 수락선 ⑦).
head, extra = HEAD_HTML, EXTRA_CSS
body_rows = []
for r in rows:
    lab, cls = STATE[r["chip"]]
    q, now, dep = PROSE.get(r["id"], ("", "", ""))
    body_rows.append(
        f'<tr class="st-{r["chip"]}"><td class="id">{r["id"]}</td>'
        f'<td class="q">{html.escape(q) or "—"}</td>'
        f'<td class="now">{html.escape(now) or "—"}</td>'
        f'<td><span class="chip {cls}">{lab}</span></td>'
        f'<td class="dep">{html.escape(dep) or "—"}</td></tr>')

rule_rows = []
for pri, ph, chip, note in PHRASE_RULES:
    lab, cls = STATE[chip]
    rule_rows.append(
        f'<tr><td><code>{html.escape(ph)}</code></td>'
        f'<td><span class="chip {cls}">{lab}</span></td>'
        f'<td>{pri}</td><td>{html.escape(note) or "—"}</td></tr>')

diff_line = ("원장과 옛 손목록이 <strong>모든 행에서 일치</strong>합니다."
             if not diff else
             "⚠ <strong>원장과 옛 손목록이 " + str(len(diff)) +
             " 행에서 갈립니다</strong> — " +
             " · ".join(f"{i} 손목록 {STATE[o][0]} → 원장 {STATE[n][0]}" for i, o, n in diff) +
             ". 이 페이지는 <strong>원장을 따릅니다</strong>.")

body = f"""<div class="wrap">
  <div class="masthead">
    <span class="eyebrow">내부구조 솔버 · 코어 항목 · {datetime.date.today().isoformat()} · {sha}</span>
    <h1>코어 항목 {len(rows)}개 — 번호마다 무엇을 묻고, 지금 어디에 서 있는가</h1>
    <p class="standfirst">일일 보드가 "오늘 무엇이 움직였나"를 말한다면, 이 표는 <strong>번호가 가리키는 것이 무엇인지</strong>를 말합니다. ⚠ <strong>상태 칩은 이제 손으로 옮긴 것이 아니라 원장에서 읽습니다</strong> — <code>git show {sha}:engine/interior-core.md</code> 의 항목 표를 머리글 행으로 찾아 상태 칸을 그대로 읽고, 아래 대응표로 접습니다. 표에 없는 문구가 나오면 이 페이지는 만들어지지 않습니다. 한글 두 칸(무엇이 문제였나 · 지금은)은 여전히 <strong>손으로 쓴 요약</strong>입니다.</p>
  </div>
  <div class="strip">
    <div class="stat"><span class="stat-label">전체</span><span class="stat-value">{len(rows)}</span><span class="stat-note">{rows[0]['id']} ~ {rows[-1]['id']}</span></div>
    <div class="stat"><span class="stat-label">닫힘 · 지어짐</span><span class="stat-value v-quiet">{cnt.get('closed',0)+cnt.get('built',0)}</span><span class="stat-note">닫힘 {cnt.get('closed',0)} · 지어짐 {cnt.get('built',0)}</span></div>
    <div class="stat"><span class="stat-label">진행 · 조건부</span><span class="stat-value v-wait">{cnt.get('open',0)+cnt.get('conditional',0)}</span><span class="stat-note">열림 {cnt.get('open',0)} · 조건부 {cnt.get('conditional',0)}</span></div>
    <div class="stat"><span class="stat-label">미착수 · 막힘</span><span class="stat-value v-stop">{cnt.get('listed',0)+cnt.get('blocked',0)}</span><span class="stat-note">미착수 {cnt.get('listed',0)} · 막힘 {cnt.get('blocked',0)}</span></div>
  </div>
  <section>
    <div class="sec-head"><h2>읽는 법</h2><p class="sec-sub">상태 칩 일곱 가지와 마지막 열의 뜻입니다.</p></div>
    <p class="prose"><span class="chip c-done">닫힘</span> 질문에 답이 났거나 이름 붙인 거절로 끝남. <span class="chip c-done">지어짐</span> 코드와 레시피가 들어가 돌아감. <span class="chip c-wait">진행·열림</span> 일부 답이 났고 나머지가 남음. <span class="chip c-wait">조건부 닫힘</span> 닫혔으나 남은 것이 있음. <span class="chip c-park">미착수</span> 등재만 됨. <span class="chip c-stop">막힘·대기</span> 다른 결정이나 자료를 기다림. <span class="chip c-acc">상시 감시</span> 닫히지 않는 것이 정의.</p>
    <p class="prose">마지막 열 <strong>기다림</strong>은 그 항목이 명시적으로 기다리는 다른 항목입니다.</p>
  </section>
  <section>
    <div class="sec-head"><h2>전체 목록</h2><p class="sec-sub">상태는 <code>{sha}</code> 의 원장에서 읽은 것입니다.</p></div>
    <div class="tablewrap"><table class="grid">
      <tr><th>번호</th><th>무엇이 문제였나</th><th>지금은</th><th>상태</th><th>기다림</th></tr>
      {''.join(body_rows)}
    </table></div>
  </section>
  <section>
    <div class="sec-head"><h2>원장 문구 → 상태 칩 대응표</h2><p class="sec-sub">생성기가 실제로 쓰는 규칙 {len(PHRASE_RULES)} 개입니다. 여기 없는 문구를 만나면 페이지를 만들지 않고 그 문구와 줄번호를 대며 멈춥니다.</p></div>
    <div class="tablewrap"><table class="grid">
      <tr><th>원장 구절</th><th>칩</th><th>우선순위</th><th>비고</th></tr>
      {''.join(rule_rows)}
    </table></div>
    <p class="prose">⚠ <strong>첫 낱말로 가르지 않습니다</strong> — 원장의 상태 칸 첫 낱말은 서른 가지쯤이고 그중 여럿은 상태가 아니라 산문입니다. 그래서 구절로 접고, 두 규칙이 함께 걸리는 행은 오늘 {ties} 행이고, 그중 **서로 다른 칩을 가리켜 우선순위가 실제로 판정한 행은 {chip_ties} 행**입니다. {diff_line}</p>
  </section>
  <footer>
    <div>상태 칩: <code>git show {sha}:engine/interior-core.md</code> 의 항목 표에서 읽음 (머리글 {header_hits} 회, 행 {len(rows)}, 서로 다른 번호 {len(set(ids))}, 겹침 {len(dups)}) · 브랜치 <code>engine/prototype</code></div>
    <div>한글 두 칸은 손으로 쓴 요약입니다 — 생성기가 만들지 않습니다. 판정 근거는 원장 절에 있습니다.</div>
  </footer>
</div>
"""
out = "core-items-" + datetime.date.today().strftime("%m%d") + ".html"
open(out, "w", encoding="utf-8").write(head + extra + body)
print("[페이지]", out)
