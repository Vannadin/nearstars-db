# 물질을 직접 추가하기

이 안내서는 AI나 엔진 좌석 없이 내부구조 솔버에 물질을 하나 추가하는 방법을 설명한다. 물질 하나는 `solver/materials/`의 YAML 파일 하나이고, 솔버가 쓰는 레지스트리가 이를 읽는다. 기계적인 일은 명령 세 개가 하고, 이 문서는 그 명령들이 사람에게 남기는 판단을 다룬다.

필요한 것은 저장소 루트에서 연 터미널과 솔버의 Python(`solver/.venv/bin/python`, 아래에서는 `python`으로 줄여 씀)이다.

## 물질 기록이란

기록 하나는 자료표 한 장이다.
- **상(phases)**: 상태방정식(`eos`), 열 모형, 안정 영역, 유효 창을 각각 가진다.
- **가장자리(edges)**: 창의 경계를 막 넘었을 때 무슨 일이 일어나는지 정한다.
- **출처(sources)**: 모든 숫자에 어디서 읽었는지 인용을 붙인다.
- **검산식(formula checks)**: 출처에 인쇄된 값을, 검사기가 기록에서 다시 계산해 맞춰 본다.

기록에는 출처가 인쇄한 값을 SI 단위로 담고, 숫자마다 인쇄된 문구를 곁에 둔다. 솔버는 추측하지 않는다. 선언한 범위 밖에서는 이름을 붙여 거절한다.

## 명령 세 개

| 명령 | 하는 일 |
|---|---|
| `python -m solver.materials new <kind> <id>` | `solver/materials/<id>.yaml`을 만든다. 필수 칸이 모두 들어 있고 스키마에서 가져온 주석이 달린다. 종류는 `single`, `branched`, `hand_over`, `table`이다. 모든 값은 `FILL`로 시작하고, `FILL`이 하나라도 남은 기록은 검사기가 거절한다. |
| `python -m solver.materials add-source <pdf> --citation "<저자 연도, 제목, 학술지>"` | PDF의 해시를 계산해 `solver/materials/sources.yaml`에 한 줄을 더하고, 붙여 넣을 인용 블록을 그대로 출력한다. 이 파일에 없는 `sha256`을 단 인용은 읽어 들일 때 거절된다. |
| `python -m solver.materials check <id>` (또는 `--all`) | 읽어 들이기 규칙을 모두 돌린 뒤, 그 기록의 생성 검사와 검산식을 돌린다. 문제마다 *칸 / 무엇이 틀렸는지 / 어떻게 고치는지*를 알려 준다. 종료 코드 0은 기록이 읽히고 검사도 통과했다는 뜻이다. |

`check`는 경고도 출력한다. 예를 들어 기록의 주 출처 계열 밖 출처가 쓰였을 때다. 경고는 검사를 실패시키지 않지만 읽어 두어야 한다.

## 예제: 캐시된 논문 두 편으로 고체 ε-철 만들기

목표는 0–100 GPa, 300–3000 K 범위의 hcp 철 단일 상 기록이다. 필요한 값은 캐시된 논문 두 편에 모두 있다.
- **Seager 외 2007**, 표 1의 «Fe (ε)» 행: Vinet 적합으로 K0 = 156.2 GPa, K0′ = 6.08, ρ0 = 8.30 Mg m⁻³이다. 표는 캐시된 프리프린트 `2007ApJ...669.1279S.pdf`의 15쪽에 있다.
- **Isaak & Anderson 2003**, 347쪽 식 (4) 아래 본문: 300 K에서 (αK_T) = 12.1 × 10⁻³ GPa K⁻¹이고, 비조화 기울기는 7.8 × 10⁻⁷ GPa K⁻²이다. 파일은 `2003PhyB..328..345I.pdf`이다.

열용량은 Dulong–Petit 극한 3R/M을 공식으로 밝혀 쓴다.

**1. 뼈대 만들기.**
```
python -m solver.materials new single fe_eps_example
```

**2. 출처 등록.** 캐시된 PDF는 본 체크아웃의 `docs/phase3/_papers/`에 있다. 인용할 논문마다 `add-source`를 한 번씩 돌린다.
```
python -m solver.materials add-source <main checkout>/docs/phase3/_papers/2007ApJ...669.1279S.pdf \
    --citation "Seager, S. et al. 2007, Mass-Radius Relationships for Solid Exoplanets, ApJ 669, 1279"
python -m solver.materials add-source <main checkout>/docs/phase3/_papers/2003PhyB..328..345I.pdf \
    --citation "Isaak, D.G. & Anderson, O.L. 2003, Thermal expansivity of HCP iron at very high pressure and temperature, Physica B 328, 345"
```
출력의 뜻은 다음과 같다.
- `registered, sha256 …`: `solver/materials/sources.yaml`에 새 줄이 더해졌다. 이 파일이 바뀌었으니 기록과 함께 커밋한다.
- `already registered (sha256 …)`: 이미 목록에 있던 논문이다. 아무것도 바뀌지 않고, 준 인용 문구는 무시된다. 인용 블록은 출력되지 않으므로 `{cache: <파일 이름>, page: <인쇄된 쪽>, where: <표, 식 또는 절>, sha256: <출력된 해시>}`로 직접 만든다.
- `provenance stub: <경로>`: PDF 옆의 출처 메모다. 캐시된 논문은 자기 메모를 그대로 쓰므로 본 체크아웃에는 아무것도 쓰이지 않는다. 캐시 밖의 새 PDF라면 그 옆에 메모가 새로 생긴다.

각 논문의 출력된 `sha256`을 그 파일을 인용하는 모든 자리에 옮겨 적는다.

**3. 채우기.** 뼈대의 본문을 아래 기록으로 바꾼다. 이 기록은 뼈대의 `FILL`을 모두 채우고, 이 물질에 필요한 다음 두 가지를 더한 것이다.
- `p_max` 가장자리: 창의 P 상한이 유한하기 때문이다(뼈대에는 `t_min`, `t_max`만 있다).
- 뼈대가 주석으로 둔 열 관련 키(`pressure`, `gamma_window`, `phase_constants`).

인용은 쓰일 때마다 그 숫자의 `page`와 `where`를 담아 전부 다시 적는다. 아래의 `… same cite …`는 같은 블록을 다시 쓴다는 뜻이다. YAML 앵커는 쓰지 않는다.

```yaml
id: fe_eps_example
label: solid ε-iron (worked example)
kind: single
system: Fe
fit_composition: pure Fe, hcp
primary_family:
  name: Seager et al. 2007 Vinet fit
  sources: [2007ApJ...669.1279S.pdf]
  reason: the cold curve answers; the I&A constants and the Dulong–Petit c_V are thermal constants, not answering sources
phases:
  - id: fe_eps
    state: solid
    eos:
      form: vinet
      params:
        rho0: {value: 8300.0, unit: kg/m3, grade: read, printed: "8.30 Mg m^-3", source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1, Fe (ε) row", sha256: <printed by add-source>}}
        k0: {value: 1.562e11, unit: Pa, grade: read, printed: "156.2 GPa", source: {… same cite …}}
        k0p: {value: 6.08, unit: "1", grade: read, printed: "6.08", source: {… same cite …}}
      reference:
        kind: state
        p: {value: 0.0, unit: Pa, grade: read, note: "zero-pressure fit", source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1: ρ0 is the zero-pressure density", sha256: <Seager's>}}
        t: {value: 300.0, unit: K, grade: read, note: "room-temperature fits", source: {cache: 2007ApJ...669.1279S.pdf, page: "2", where: "§2: «use experimental data obtained at room temperature»", sha256: <Seager's>}}
        t_ref_kind: isotherm
    thermal:
      source_state: solid
      source_composition: pure-Fe-hcp
      pressure:
        alpha_k: {value: 1.21e7, unit: Pa/K, grade: read, printed: "(αK_T)300 K = 12.1 × 10^-3 GPa K^-1", conversion: "×1e9",
                  source: {cache: 2003PhyB..328..345I.pdf, page: "347", where: "text below eq. (4)", sha256: <from sources.yaml>}}
        alpha_k_dt: {value: 780.0, unit: Pa/K2, grade: read, printed: "7.8 × 10^-7 GPa K^-2", conversion: "×1e9", source: {… I&A cite …}}
        c_v: {value: 446.6539144775719, unit: J/kg/K, grade: declared, note: "Dulong–Petit limit",
              source: {formula: "3R/M, R = 8.314462618 J/mol/K, M = 0.055845 kg/mol"}}
      gamma_window: {p_min: 0.0, p_max: 1.0e11}
      phase_constants: {p_min: 0.0, p_max: 1.0e11, reason: "no thermal set: γ from the phase's own constants over the whole window"}
    field:
      kind: sourced
      box: {p_min: 0.0, p_max: 1.0e11}
      source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1, Fe (ε) row", sha256: <Seager's>}
    window: {p_min: 0.0, p_max: 1.0e11, t_min: 300.0, t_max: 3000.0}
    edges:
      p_max: {refusal: input.material_out_of_data}
      t_min: {refusal: input.material_out_of_data}
      t_max: {refusal: input.material_out_of_data}
formula_checks:
  - quantity: K0 as printed
    state: {}
    expected: 1.562e11
    unit: Pa
    tolerance: 0.0
    tolerance_reason: a transcription check of the printed value
    expression: params.k0
    source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1, Fe (ε) row", sha256: <Seager's>}
```

**4. 검사.**
```
python -m solver.materials check fe_eps_example
```
기대하는 출력은 다음과 같다.
```
fe_eps_example.yaml: loads
fe_eps_example.yaml: generated checks and formula checks pass
```

**5. 쓰기.** 이제 레지스트리가 이 기록을 id로 내준다. 천체는 옛 물질에서 위상 2 기록으로의 전환이 등록된 뒤에 위상 2 기록을 읽는다. 그때까지는 `check`와 시험에서만 쓰인다.

예제가 보여 주는 것은 다음과 같다.
- **모든 기록은 주 출처 계열을 밝힌다**(`primary_family`, 필수). 여기서는 Seager의 적합이 그 계열이다. 열 상수는 밀도를 내지 않으므로 계열 출처가 아니다.
- **모든 숫자에 인용**(`cache`, `page`, `where`, `sha256`)이나 밝힌 공식이 붙는다. `printed`에는 인쇄된 문구를, `conversion`에는 SI로 바꾼 방법을 적는다.
- **열 모형은 필수다.** 차가운 곡선만 있는 기록도 읽히기는 하지만 어디서도 답하지 않는다. 모든 지점에서 γ = αK_T/(ρc_V)를 묻기 때문이고, `check`가 «answers nowhere»로 알려 준다. 열 세트가 없으면 `phase_constants`가 그 상 자체의 `alpha_k`, `c_v`로 γ 창 전체를 덮어야 한다.
- **유한한 창 경계마다 가장자리가 있다.** 여기서는 모든 경계가 거절한다. 띠(band)는 근거를 밝혔을 때만 허용된다(아래).

## 판단 지점과 허용되는 선택

모양은 검사기가 강제한다. 아래 선택은 기록을 쓰는 사람의 몫이며, 각각 허용되는 답이 정해져 있다.

**주 출처 계열**(설계 노트 4). 물질마다 자기 일관된 출처 계열 하나를 고른다. 밀도, 열 항, 상 영역을 한 모형으로 가장 멀리까지 덮는 계열이다. `primary_family: {name, sources, reason}`로 밝히며, 모든 기록이 이를 가져야 한다. `sources`에는 계열 키를 적는다. 캐시된 파일 이름이거나, 인용한 그대로의 라이브러리 고정(`SeaFreeze@1.1.0`)이다. «답하는» 출처로 치는 것은 상태방정식 자체의 값(계수, 평가자 계수, 표)이다. 선언한 기준 상태나 열 상수는 치지 않는다. 사용자 선언 기록에는 캐시 키가 없으니, 이름을 붙이고 쓴 것을 적는다.

다른 출처는 모두 다음 둘 중 하나다.
- **계열이 닿지 않는 곳**: 아래의 테이퍼 규칙으로 잇는다.
- **교차 확인**: 답하지 않는다.

계열이 다 덮지 못하는 상은 그 상 전체에 출처 **하나**를 쓰고, 그 이유를 `multi_source_reason: {reach: beyond_primary | whole_phase, text}`에 적는다. 한 상 안을 T 선으로 쪼개는 것은 허용되지 않는다. 유일한 예외는 한 계열의 두 상 사이에 둔, 차이가 무시할 만한 출처 이음매다(설계 노트 5, 아래). 이유를 적기 전까지 검사기는 경고(`material.multi_source`)를 낸다.

**한 상 안의 두 출처**(구현 노트 3 Part A). 출처마다 `basis`(measured 또는 computed), 쪽수가 붙은 `data_range`, `sigma`, `sigma_kind`를 밝힌다. 겹침 구간은 두 출처의 창이 아니라 *데이터* 범위의 교집합이다. 그다음 아래 넷 중 하나를 고른다.
- **cross_check**: 우선 출처가 답한다. 다른 출처는 선언된 격자에서 비교되고, 그 |Δρ|/ρ는 띠에 들어가며, r > 2인 노드는 이름을 붙여 공개한다. 관문을 거치지 않는다.
- **blend**: 겹침 구간 안에서 두 출처가 함께 답하며, P에만 의존하는 C¹ smoothstep으로 가중한다(T 가중은 거절된다). 이것은 **관문을 거친다.** r = |Δρ|/σ_allow > 2인 노드가 하나라도 있으면 `material.source_conflict`로 읽어 들이기가 멈춘다. 한쪽이 답하지 못하는 노드가 있어도 마찬가지다. 겹침 구간은 두 데이터 범위 안에 있어야 하고, 표본 상자는 겹침 구간과 같아야 한다.
- **taper**: 측정 출처의 범위 밖에서, P_e에서 1.5·P_e까지(또는 이유를 단 선언 폭) 다른 출처 쪽으로 P만으로 섞는 부피 혼합이다. 밀도 계단 대신 쓴다.
- **seam**: 창이 맞닿기만 하는 곳의 한 점 이음이다. `seams()`에는 나오고 `transitions()`에는 나오지 않는다.

**관문이 멈췄을 때**(A6) 허용되는 답은 다음 셋이다.
1. 측정 범위 안에서는 측정값이 계산값을 이기고, 그 범위의 가장자리에 이음매를 둔다.
2. 다른 출처를 쓴다.
3. 창을 좁혀, 충돌 구역을 이름 붙은 거절로 만든다.

비교를 본 뒤에 그 출처의 다른 열을 골라 쓰는 것은 절대 허용되지 않는다.

**σ와 sigma_kind.**
- 인쇄되지 않은 σ는 `{kind: not_printed, where}`에 `sigma_kind: not_applicable`로 적고, 0으로 친다. 대신 쓰는 값은 절대 두지 않는다.
- 인쇄된 신뢰구간은 환산한다. ci90은 1.645로, ci95는 1.960으로 나눈다.
- 데이터를 공유하면(한 적합이 다른 쪽의 점을 포함하면) 최댓값으로, 아니면 제곱합의 제곱근으로 합친다.
- σ가 구역마다 다르면 `{kind: by_region, regions: […], else: …}`로 쓴다. 상자가 겹치면 가장 작은 값이 이긴다.

**가장자리에서 거절할지 띠를 둘지.** 창의 경계를 넘으면 기록은 거절하거나(`{refusal: input.material_out_of_data}`) 띠를 달고 답한다. 띠에는 `{form, error | method, grade, origin}`이 필요하고, origin은 밝힌 출처나 방법이어야 한다. 근거가 없으면 거절이다.

**γ 창**(G4). 열 세트는 출처가 인쇄한 범위(`printed_scope`) 안에 둔다. 그 너머는 밝힌 한계까지 선언한 `edge_above` 띠로만 갈 수 있다. γ 창 안에서는 세트와 `phase_constants`가 모든 압력을 덮어야 하고, γ를 상수에서 얻는 곳에서는 `alpha_k`와 `c_v > 0`이 둘 다 필요하다.

**출처가 있는 표와 사용자 선언 표**(Part B). 직접 표는 (P, T) 위의 `eos.form: table`이고, (ln P, T)에서 이중선형으로 읽는다.
- 모양: `first`는 P 노드[Pa], `t`는 T 노드[K]의 목록이고 둘 다 증가 순이다. 각 열(`rho`, `alpha`, `c_p`, 선택으로 `k_t`)은 P 노드마다 한 행씩 이루어진 목록이고, 각 행은 T 노드마다 값 하나씩이다.
- **α와 c_P 열이 반드시 있어야 한다.** dT/dP = αT/(ρc_P)를 열에서 읽고 미분하지 않기 위해서다(구현 노트 9). K_T는 선택이다.
- 열 블록은 `{source_state, source_composition}`만 둔다. γ와 dT/dP를 열에서 얻으므로 표 상에는 `gamma_window`, `sets`, `phase_constants`를 두지 않는다(검사기가 거절한다).
- 격자가 곧 창이고, 유한한 창 경계마다 가장자리가 필요하다.
- Maxwell 일관성은 선언한 `maxwell_tolerance` 안에서 검사한다. 이 값은 각 등압선을 따라 α와 −∂lnρ/∂T 사이(그리고 ∂c_P/∂P와 −T∂²v/∂T² 사이)에 허용하는 상대 오차다. 검사를 돌리기 전에 표의 간격을 보고 정한다. `alpha_range: [lo, hi]`로 정상 α 범위를 밝힌다.
- 검산식은 여기도 필요하다. 사용자 선언 표라면, 넣은 값과 맞춰 보는 노드 하나의 옮겨 적기 검사(예: `rho(<phase> @ P=…, T=…)`)에 `source: {user_declared: <이유>}`를 달면 충분하다.
- 논문의 표라면 그 논문을 인용한다. 가상이거나 특이한 물질의 표라면 `source: {user_declared: <이유>}`를 쓴다. 이 경우 그 물질을 쓰는 모든 결과의 등급이 «declared»가 되고, 현황판에 그 수가 집계된다. 허용되지만 숨겨지지 않는다.

**검산식과 공개된 실패**(C4).
- 검산식은 인쇄된 값을 기록에서 다시 계산한다. 식 문법은 경로로 가리키는 상수(`params.k0`, `sets[0].c_v`), 상태 값, `curve(boundaries[i] @ T=…)`, `melt_p(a, b @ T=…)`, `rho(<phase> @ P=…, T=…)`, 그리고 사칙연산이다.
- 허용 오차와 그 이유는 검사를 돌리기 전에 적는다. 빗나간 뒤에 넓히지 않는다.
- 실패하는 검산식을 **공개된 실패**로 둘 수 있는 것은, 캐시된 출처가 그 불일치를 쪽수와 함께 *인쇄*해 두었고 빗나감이 그 인쇄된 크기 안에 있을 때뿐이다. 공개된 실패가 통과하기 시작하면 낡은 것이므로 실패로 처리된다.

**T에서의 출처 이음매**(설계 노트 5). 한 물리적 물질의 두 상이 온도 t에서 만나도 되는 것은 두 조건을 다 갖출 때뿐이다. 양쪽이 한 계열이어야 하고(같은 정식화이거나 인용된 재적합), 측정된 차이가 무시할 만해야 한다(|Δρ|/ρ ≤ 1e-9, |Δα|/α와 |Δc_P|/c_P ≤ 1e-6, 올릴 수 없는 전역 상수). 낮은 T 쪽 상을 먼저 적고, t 자체는 높은 쪽이 가진다.

**조성 출처 종류**(물질이 아니라 천체의 층). 산화물 wt%를 선언하는 규산염 층은 `source_kind`를 밝힌다. `measured`(이 천체에 대한 논문 값으로, grade, source, counter_evidence_searched를 함께 단다), `owner_override`, `preset`, `default_bse` 중 하나다. 값은 인쇄된 그대로 저장하고, 인쇄된 합은 100 ± 2 wt% 안이어야 한다.

## `check` 메시지의 뜻

| 메시지 | 뜻과 고치는 법 |
|---|---|
| `placeholder` | `FILL`이 남아 있다. 채운다. |
| `unregistered source` | 인용의 sha256이 `sources.yaml`에 없다. `add-source`를 돌리고 출력된 해시를 옮겨 적는다. |
| `edge undeclared` | 안정 영역이 유한한 창 경계에 닿는데 가장자리 항목이 없다. 거절이나, 근거를 단 띠를 선언한다. |
| `answers nowhere` | 기록은 읽히지만 창 한가운데서 거절한다. 이유를 읽는다. «γ asked …»는 열 모형이 없다는 뜻이다. |
| `formula check «…»: got …, expected …` | 인쇄된 값과 단위를 다시 읽는다. 빗나간 뒤에 허용 오차를 넓히지 않는다. |
| `table check` | 표가 물리 검사에 걸렸다(ρ가 P와 함께 줄어듦, K_T ≤ 0, 빈 칸, α가 선언 범위 밖, Maxwell). 검사가 아니라 자료나 그 선언을 고친다. |
| `source conflict` | 혼합의 두 출처가 이름 붙은 노드에서 2σ를 넘게 어긋나거나, 한쪽이 답하지 못한다. 위의 A6 답 중 하나를 쓴다. |
| `gamma window` | 열 세트가 자기 창이나 인쇄 범위를 넘었거나, γ 창이 다 덮이지 않았거나, 상수에 alpha_k나 c_v가 없다. |
| 경고 `multi source` | 주 출처 계열 밖 출처가 어느 상에서 답한다. `multi_source_reason`을 적거나 계열 출처를 쓴다. |

## 하지 않는 것

- 인쇄된 값을 정규화하거나, 반올림하거나, 다시 적합하지 않는다. `printed`와 `conversion`을 달아 인쇄된 그대로 저장한다.
- 인쇄되지 않은 σ, γ, c_V, 범위를 다른 값으로 대신하지 않는다.
- 비교를 본 뒤에 허용 오차, 창, k, 열을 고르지 않는다.
- `db/systems/*.json`이나 다른 유도 파일을 손으로 고치지 않는다.
