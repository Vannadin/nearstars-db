<!-- 병렬석 조사 기록 (원문 무편집). C33 batch M-A: what each remaining line-number citation lands on, per citer. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05. C33 batch M-A: what each remaining line-number citation lands on, per citer. -->
# M 배치 A — 죽은 착지 7건 + 우선순위 1·2 현황
Parallel seat, 2026-09-05. HEAD aa4910f4, 읽기 전용, 레포 쓰기 없음.
⚠ 작업석이 `engine/tidal_heating.py` 를 미커밋으로 들고 있습니다(제가 보는 동안 앵커화가 진행됐습니다 —
체커 첫 실행 176건 → 재실행 149건).

## ⚠ 우선순위 1·2 는 거의 닫혔습니다 — 남은 것은 성질이 다릅니다

체커 `--suspect` 를 재실행해 **citer 가 `.py` 인 미이행 건**을 전수로 뽑으면 다섯 건뿐이고, **전부
`main.tex` 를 가리킵니다.**

| citer | ref | 성질 |
|---|---|---|
| `engine/radiogenic.py:16` | `main.tex:420–421` | Nimmo & Primack 2020 의 **미발표 LaTeX 초안** — 레포 밖 |
| `engine/radiogenic.py:55` · `:64` | `main.tex:494-499` | 같음 (네 핵종 상수의 출처 표) |
| `scripts/phase3/field_tooltips.py:178` · `:179` | `main.tex:261` | 같음 |

**판정: 결함이 아니고 분류 문제입니다.** 체커가 이미 "레포 밖 인용 13건" 이라는 통을 갖고 있으므로,
이 다섯은 **그 통으로 옮기면 됩니다**(앵커화 대상이 아닙니다 — 레포에 없는 파일에는 앵커를 걸 수 없습니다).
⚠ 다만 `main.tex` 라는 이름만으로는 **어느 논문의 초안인지 알 수 없습니다.** 권고: 파일명 대신
bibcode/식별자를 앞에 붙이는 형태 — 예 `Nimmo & Primack 2020 (unpublished draft) main.tex:494-499`.
`radiogenic.py:62-64` 의 문서 주석이 이미 "Nimmo & Primack 2020's **unpublished draft table** (LaTeX
source after `\end{document}`; absent from the PDF)" 라고 적고 있어, 그 서술을 인용 자체에 넣으면
닫힙니다.

**즉 P1(출하 문자열)·P2(레시피 모듈)에 남은 in-repo 문서 인용은 0건입니다.** 아래 하나만 예외적으로
남습니다.

### P1 잔여 한 건 — 출하 문자열 안의 **자기 파일 줄번호**

`engine/radiogenic.py:249-251`:
```
HEAT_PIPE_FLOOR = ("cannot-say (heat-pipe regime: the boundary-layer inversion does not apply; "
                   "radiogenic.py _total_heat:265-267)")
```
이 문자열은 `internal_heat_nontidal` 의 **출하 verdict** 로 사용자에게 나갑니다
(`mantle_temperature_floor_total_verdict`). 함수명을 붙인 것은 이미 개선이지만 —

| 인용이 가리키는 곳 | 실제 내용 |
|---|---|
| `:265` | 표의 주인 문서를 이름으로 적는 **주석** (앵커 포함) |
| `:266` | `import tidal_heating` |
| `:267` | `mode = tidal_heating.transport_mode(total_flux)` |
| **`:268-270`** | **← 실제 가드**: `if mode == MODE_HEAT_PIPE or g_body is None:` → `verdict = HEAT_PIPE_FLOOR` |

즉 "the boundary-layer inversion does not apply" 를 **결정하는** 자리는 `:268-270` 이고 인용은
`:265-267`(모드를 *구하는* 자리)입니다. **권고: 출하 문자열에서 줄번호를 아예 떼고
`radiogenic.py _total_heat` 로.** 사용자에게 나가는 문자열에 줄번호가 들어가면 리팩터 한 번으로
반드시 썩고, 함수명만으로 독자는 찾을 수 있습니다.

## 배치 A 본체 — 죽은 착지 7건

전부 인용을 담은 문장을 읽어 의도를 확인하고, 도입 의도의 문장을 오늘 문서에서 찾았습니다.
앵커는 전부 `uniq=1` 확인.

| # | citer | 현재 ref | 착지 | 인용을 담은 문장이 대려던 근거 | **정답** | 앵커 구절 |
|---|---|---|---|---|---|---|
| 1 | `engine/backflow-checklist.md:73` | `…geometry-methodology.md:874` | **레포에 없는 파일명** | ":72-73 «An undeclared derived-value cycle, `pause_smooth ↔ pause_radius_smoothed`. Reading the doc showed it is a genuine fixed point»" | **파일명만 틀렸고 줄번호는 맞습니다** — `planetary-magnetosphere-geometry-methodology.md:874` | `` @«`pause_smooth` = 0.5 × `pause_radius` is solved as a fixed point» `` |
| 2 | `engine/giant-dynamo-age-context-notes.md:9` | `planetary-dynamo-scaling.md:34` (빈 줄) | 빈 줄 | ⚠ **이것은 인용이 아니라 인용문 안의 인용입니다** — 아래 별항 |
| 3 | `engine/interior-core.md:2333` | `rocky-planet-dynamo-methodology.md:108–109` (빈 줄) | 빈 줄 | ":2333-2334 «…the structure + thermal-evolution coupling `rocky…:108–109` **says this project does not re-run per body**»" | **`rocky:109`** | `@«NearStars does not re-run RM22's full internal-structure + thermal-evolution»` |
| 4 | `engine/property-consumer-audit-context-notes.md:31` | `rocky-planet-dynamo-methodology.md:60-64,103-104` (빈 줄) | 빈 줄 | ":30-32 «Electrical conductivity / magnetic Reynolds: … every hit saying **quoted, not evaluated**. No `sigma`, no `μ₀`, no velocity anywhere executable.»" | **두 자리** — `rocky:65` 와 `rocky:116` | `@«**quoted, not evaluated here**»` (uniq=1, `:65`) · `@«evaluated** — this document carries no magnetic-Reynolds formula»` (`:116`) |
| 5 | `engine/radiogenic-context-notes.md:38` | `internal-heat-luminosity-methodology.md:306` (빈 줄) | 빈 줄 | ":37-39 «**0.087 W/m² is Earth's total surface heat flux.** Our own methodology is careful and correct — `…md:306`: *"~0.087 W/m², split roughly half radiogenic (U/Th/⁴⁰K decay) and half secular"*»" | **`heat:478`** (172줄 아래 — 지휘석이 짚은 `field_tooltips.py` 와 같은 자리) | `@«**~0.087 W/m²**. How much of it is radiogenic»` |
| 6 | `engine/tidal-heating-context-notes.md:13` | `tidal-heating-methodology.md:56` (빈 줄) | 빈 줄 | ":13 «Pandora reproduces the board's 45 W/m² within 5 % (tidal `…md:56` with a 252 393 km · e 0.005 · k₂/Q 0.0016 …)»" — 즉 **Ė 공식** | **`tidal:74`** | `@«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶»` |
| 7 | `engine/tidal-heating-context-notes.md:31` | `tidal-heating-methodology.md:330–338` (빈 줄) | 빈 줄 | ":30-31 «Pandora is not a §6 lid case, `…md:330–338`»" — 즉 **§6.3 범위 상자**("Dante takes this branch; Pandora … takes the other one") | **`tidal:348`**(상자 시작, 끝은 `:356`) | `@«> **Scope — lid-bearing bodies only.**»` |

### ⚠ #2 는 성질이 다릅니다 — 고치면 기록이 훼손됩니다

`giant-dynamo-age-context-notes.md:8-11` 은 절 제목이 `## 1. What the edge says, and what the code says`
이고, 본문이 **2026-09-03 당시의 chain 간선을 축자로 인용**합니다 —

> `chain.yaml:644`: `body_age → dynamo_giant, kind: requires, via: cooling_luminosity, status: gap, ref:
> planetary-dynamo-scaling.md:34`, note (2026-09-03): *"the graph was more optimistic than the module — …"*

즉 `planetary-dynamo-scaling.md:34` 는 **노트 자신의 인용이 아니라, 인용된 간선 텍스트의 일부**입니다.
그 간선은 그 뒤 C19 가 `via: t_body` 로 바꾸고 ref 도 앵커로 옮겼습니다(현재
`chain.yaml:659` = `planetary-dynamo-scaling.md@«B_dip^pol(M, age) = 9 G · (age / 4.5 Gyr)^(−0.33) · (M / M_Jup)^0.93»`).

**권고: 앵커로 바꾸지 말고, 인용 블록임을 표시하십시오.** 예: 인용 뒤에 한 줄 —
"(이 간선은 C19(2026-09-04)로 `via: t_body` + 앵커 ref 로 대체됨 — 위 인용은 09-03 상태의 기록)".
줄번호를 오늘 자리로 갈아 끼우면 **2026-09-03 에 그렇게 적혀 있었다는 사실 자체가 사라집니다.**

⚠ **체커에 대한 함의**: 지금 체커는 *인용(citation)* 과 *인용문 안의 인용(quoted citation)* 을 구별하지
못합니다. 보존 노트가 과거 상태를 축자로 인용하는 것은 이 레포의 규율(`context-notes-log`, provenance
블록)이라 같은 부류가 더 있을 가능성이 큽니다. **규칙 제안**: 같은 줄 또는 앞 두 줄에 인용 표지
(`*"`, `> `, `` ` `` 로 감싼 간선 텍스트, 또는 `note (YYYY-MM-DD):`)가 있으면 **INFO 로 낮추고 자동
정정 대상에서 제외**.

## 배치 B 예고 (제 다음 몫)

남은 미이행 149건 중 citer 별 상위는 `interior-core.md` 10 · `tidal-wiring-facts-notes.md` 6 ·
`radiogenic-budget-context-notes.md` 5 · `property-consumer-audit-context-notes.md` 5 ·
`tidal-locking-inventory-notes.md` 4 · `magnetosphere-survey-notes.md` 4 입니다.
⚠ 그중 **`tidal-wiring-facts-notes.md`·`tidal-locking-inventory-notes.md`·`magnetosphere-survey-notes.md`·
`c32-*-notes.ko.md` 는 제가 어젯밤 쓴 스크래치 노트가 보존된 것**입니다 — 그 안의 줄번호는 **그 시점의
문서 상태를 기록한 것**이라 #2 와 같은 부류입니다(고치면 "그때 그 줄이 그랬다"는 기록이 사라집니다).
배치 B 에서 그 구분을 먼저 세우고 나머지를 표로 내겠습니다.
