---
title: ModuleManager 패치 DSL & ConfigNode (기둥 ④)
status: draft
created: 2026-06-30
---

# ModuleManager 패치 DSL & ConfigNode

범용 Module Manager(MM) 패치 언어와 그것이 동작하는 기반인 ConfigNode — NearStars의 **모든** cfg 작성기가 그 위로 출력하는 계층이다. 그라운딩 정책과 범례는 [`README`](README.md) 참고.

**그라운딩(평소보다 강함).** 스톡 KSP와 달리 ModuleManager는 **오픈소스**(`sarbian/ModuleManager`)이다 — 따라서 여기 모든 주장은 **파서 소스 그 자체**에서 입증된다(저장소의 `README.md`에는 문법 문서가 없고, KSP 포럼의 "MM Handbook"은 M 등급에 불과하다). 플래그가 붙지 않은 모든 행은 **H**이며, v4.2.3 `c4561925f983e7ae81d9dfd4d11356a35cb6b9b6`에 핀고정된다.

**범위 / 정렬(반드시 읽을 것).** 이 문서는 **범용 DSL만** 정의한다. 다음은 다시 서술하지 않는다.
- NearStars cfg 컨벤션(`NearStarsSystem` 태그, `NearStars/BodyName` 식별자, Sol/RSS 듀얼 호환, 파일 분리, Principia의 no-`:FOR` 규칙) → [`mod-release-layout.md` §2](../mod-release-layout.md)가 소유한다.
- per-mod 노드 스키마 → cfg 스킬(`kopernicus-cfg`, `firefly-cfg`, `principia-cfg`, `researchbodies-cfg`)이 소유한다.

§10은 프로젝트의 실제 MM 헤더를 아래 DSL 기능으로 매핑한다(스킬이 in-repo 입증자다).

---

## 1. ConfigNode 기초
**노드**는 `NAME { … }`, **값**은 `key = value`이며, `//`는 줄 끝까지 주석이다. MM은 노드 *이름*과 값 *키*에서 앞뒤 연산자 문자(아래)를 파싱하고, 그 외에는 ConfigNode 포맷을 손대지 않는다.

## 2. 노드 연산자(노드 이름 / 서브키의 선두 문자)
`CommandParser.Parse` — `switch(name[0])` (`CommandParser.cs:15-54`; enum `Command.cs:5-24`).

| Op | Command | 의미 |
|---|---|---|
| *(없음)* | Insert | 새 노드/값 삽입(기본) |
| `@` | Edit | 기존 노드/값 편집 |
| `%` | Replace | **편집-또는-생성**(있으면 편집, 없으면 생성) |
| `+` / `$` | Copy | 기존 노드/값 복사 |
| `-` / `!` | Delete | 노드/값 삭제 |
| `|` | Rename | 이름 변경 |
| `#` | Paste | 붙여넣기 |
| `*` | Special | special 마커(§7 이름-와일드카드 메커니즘과 ≠) |
| `&` | Create | 생성 |

## 3. 값 연산자(`@key <op>= value`)
`OperatorParser.Parse` (`OperatorParser.cs:7-54`; enum `Operator.cs:5-14`). 연산자는 **키의 마지막 문자이며, 앞에 공백/탭이 있을 때만 인식된다**(`OperatorParser.cs:15`) — 그래서 `@key += 5`는 산술이지만 `@key+=5`는 `key+`라는 이름의 리터럴 키다.

| 표기 | Operator | 의미 |
|---|---|---|
| `@key = v` | Assign | 설정(기본) |
| `@key += v` | Add | |
| `@key -= v` | Subtract | |
| `@key *= v` | Multiply | |
| `@key /= v` | Divide | |
| `@key != v` | **Exponentiate** | 거듭제곱 — 뒤따르는 `!`로 식별("not-equals" 아님) |
| `@key ^= v` | RegexReplace | 기존 값에 정규식 찾기/치환 |

> **정정(통념 대비):** 거듭제곱은 `!=` → Exponentiate
> (`OperatorParser.cs:40-42`)이며, `^=`는 정규식 치환이지 거듭제곱이 아니다.

## 4. Pass / 순서 디렉티브 + `:FOR` vs `:NEEDS` 구분
Pass 실행 순서(`PatchList.GetEnumerator`, `PatchList.cs:108-126`).
**`:INSERT` → `:FIRST` → legacy(태그 없는 `@…`) → per-mod[ `:BEFORE[m]` → `:FOR[m]` →
`:AFTER[m]` ] → `:LAST[m]` → `:FINAL`.**

**`:FOR` vs `:NEEDS` — 프로젝트에 결정적인 구분**(서로 다른 코드 경로).
- **`:FOR[mod]`** — `ForPassSpecifier.CheckNeeds` (`ForPassSpecifier.cs:18-24`)가
  `needsChecker.CheckNeeds(mod)`를 호출한다. `mod`이 없으면 패치는 **버려진다**. 이것은 이중 역할을 한다. (a) 패치를 그 mod의 pass 슬롯에 스케줄링하고, 동시에 (b) **`mod`을 패치-작성자 신원으로 선언한다**(`:FOR[X]`의 이름은 이후 `:NEEDS`/`:BEFORE`/`:AFTER`가 검사하는 mod 목록에 추가된다). ⇒ **`:FOR[X]`는 X가 *당신의* mod일 때만 사용하라** — 다른 mod이 작성한 노드에 사용하면 작성자임을 거짓으로 주장하게 된다.
- **`:NEEDS[mod]`** — 순수한 **조건 필터**(`NeedsChecker`, §5)로, 있을 때만 적용한다. 순서 슬롯도 없고 신원 주장도 없다.
- `:BEFORE[m]`/`:AFTER[m]`는 `m`이 설치되어 있어야 한다(없으면 drop). **`:LAST[m]`은 그렇지 않다**(`LastPassSpecifier.cs:16`이 무조건 `true` 반환). `:FIRST`/`:FINAL`은 mod 인자를 받지 않는다.

이것이 바로 NearStars가 `@Kopernicus:FOR[NearStarsSystem]`을 쓰는(우리가 작성하므로) 반면 Principia 패치는 **`:FOR` 없이** `@principia_…:NEEDS[…]`를 쓰는(Sol-Configs가 작성한 루트를 편집하므로 — `:FOR`는 작성자임을 거짓 주장할 것이다) 이유다. [`mod-release-layout.md` §2.1](../mod-release-layout.md)과 `principia-cfg` 스킬 참고.

## 5. `:NEEDS[...]` 불리언 문법
`NeedsChecker.CheckNeedsExpression` (`NeedsChecker.cs:42-70`); 추출은 `:102-116`(대소문자 무시 `:NEEDS[`, 첫 `]`까지의 내용, 태그는 이름에서 제거됨).

| 문법 | 의미 |
|---|---|
| `,` and `&` | **AND** — 동등(`Split(',', '&')`, `:46`). `[A&B]` ≡ `[A,B]` |
| `\|` | AND-그룹 내의 **OR**(`:49`) |
| `!` (토큰 접두) | **NOT**, 토큰의 첫 문자(`:54`). `[!A]` |
| 우선순위 | AND가 최외곽, OR는 그룹 내, NOT은 토큰별 → `[A&B\|C]` = `A AND (B OR C)` |
| `X/Y` | 디렉터리 `GameData/X/Y`가 존재해도 충족(`:79-100`) |

Mod 매칭은 대소문자 무시(`:39`). `:NEEDS` 내부에 **괄호 중첩 불가**(추출이 첫 `]`에서 멈춤, `:110`). 중첩 노드/값에 재귀적으로 적용됨(`:118-185`).

## 6. `:HAS[...]` 필터
`MMPatchLoader.CheckConstraints` (`MMPatchLoader.cs:~1459`). 최상위 `,` = AND이며, 선두 문자가 디스패치한다.

| 형태 | 의미 |
|---|---|
| `@NODE[name]` | 노드 존재(이름 매칭 선택적) |
| `!NODE[name]` | 노드 부재 |
| `#key[value]` | 값이 존재하고 일치(와일드카드 / 숫자) |
| `~key[value]` | 값이 부재이거나, **또는** 존재하지만 value와 ≠ |
| `#key[<N]` / `#key[>N]` | 숫자 미만 / 초과 |
| `@NODE[n]:HAS[…]` | 중첩(매칭된 서브노드로 재귀) |

## 7. 와일드카드
`*` → `.*`, `?` → `.`(단일 문자), `^…$`로 앵커, 나머지는 `Regex.Escape` 처리(`MMPatchLoader.cs:1556-1567`). 노드 이름 `name`은 `,` 또는 `|`로 구분된 여러 패턴을 나열할 수 있다(교차, 임의-매칭 — `NodeMatcher.cs:25`). (`?` 단일-문자 형태는 실제로 존재하지만 커뮤니티 문서에서는 자주 생략된다.)

## 8. 인덱싱(`@MODULE[name],0`)
`]` 뒤의 `,index` 트레일러는 `TagListParser`가 **포착한다**(태그의 `trailer` 필드, `TagListParser.cs:65-90,127-153`) — **H**. apply 시점의 *의미론*(`,0` = 첫 매칭, `,*` = 전부, last-index)은 다운스트림에서 해소되며 apply 지점에서 **입증되지 않았다** — **M**(커뮤니티 문서와는 일치하나 여기서 소스로 확인되지 않음).

## 9. MM 변수(`#`/`&`-vars/`@/` 경로) — 미검증
값-치환/변수 서브시스템은 fetch한 파일들에서 **입증되지 않았다**(`#` = Paste 명령 + `:HAS` 값 마커가 유일하게 입증된 `#` 용도). **L / 미검증** — 추가 타깃 fetch 없이는 MM 변수를 그라운딩된 것으로 문서화하지 말 것.

---

## 10. NearStars 사용 → DSL 기능(in-repo 입증자)
컨벤션은 [`mod-release-layout.md` §2](../mod-release-layout.md)와 cfg 스킬이 소유한다. 이 표는 위의 DSL을 프로젝트의 실제 헤더에 닻 내릴 뿐이다.

| 프로젝트 헤더 | DSL 기능 | 소유 |
|---|---|---|
| `@Kopernicus:FOR[NearStarsSystem]` | `@` 편집 + `:FOR` pass/작성자(우리가 바디 정의를 작성) | `kopernicus-cfg`; layout §2.1 |
| `ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]` | 최상위 노드 + `:NEEDS` 조건 | `firefly-cfg` |
| `@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem]` | `@` 편집 + `,`-AND `:NEEDS`, **`:FOR` 없음**(Sol이 작성한 루트를 편집) | `principia-cfg`; layout §2.1 예외 |
| `@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]` | `,`-AND + `!`-NOT `:NEEDS`(quarter-scale 제외) | `principia-cfg` |
| `RESEARCHBODIES:NEEDS[ResearchBodies&Kopernicus]` `loadAs=mod` | `&`-AND `:NEEDS` | `researchbodies-cfg` |
| `@EVE_CLOUDS:NEEDS[SolSystem]:FOR[NearStarsSystem]` | `:NEEDS`(조건) + `:FOR`(우리 작성/pass) 결합 | layout §2.1 |

---

## Gaps / 미검증
- 인덱스 apply 의미론(`,0`/`,*`/last) — 트레일러 포착(H), apply 의미는 **M**.
- MM 변수 — **L / 미검증**.
- `:AFTER` 설치 검사 — `:BEFORE`와의 **대칭으로 H**(전용 파일은 열지 않음).

## Provenance
`sarbian/ModuleManager` @ `c4561925f983e7ae81d9dfd4d11356a35cb6b9b6` (v4.2.3), 파서 소스를 raw fetch로 읽음. Permalink base —
https://github.com/sarbian/ModuleManager/blob/c4561925f983e7ae81d9dfd4d11356a35cb6b9b6/

## Related
- [`README`](README.md) — KB 인덱스 + 그라운딩 정책
- [`mod-release-layout.md` §2](../mod-release-layout.md) — canonical NearStars cfg 컨벤션(이 문서가 이쪽으로 위임)
- cfg 스킬 `kopernicus-cfg` / `firefly-cfg` / `principia-cfg` / `researchbodies-cfg` — per-mod 스키마(§10 입증자)
