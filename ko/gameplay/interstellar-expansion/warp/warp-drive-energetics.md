<!-- 워프 드라이브가 외래(음에너지) 물질을 왜, 얼마나 필요로 하는지 — 이론·방정식·외래물질 예산 레퍼런스 -->
---
title: 워프 드라이브 에너지론 — 이론, 방정식, 그리고 외래물질 예산
status: draft
created: 2026-06-30
---

# Warp-drive energetics

**이 문서의 정체.** 워프 드라이브가 *왜 외래(음에너지) 물질을 필요로 하고 그 양은 얼마인지*를
독립적으로 다루는 레퍼런스다. 알쿠비에레 메트릭의 배경 이론, 그것을 만들어내는 응력-에너지,
에너지 적분과 그 스케일링, 비용을 감당 가능하게 만들려는 전략들, 그리고 현대의 재평가까지를 담는다.
NearStars 성간 게임플레이 레이어
([`gameplay/interstellar-expansion/`](../) 참조)의 근거가 되며,
그 연료 수치는
[`prototypes/warp_exotic_matter.py`](../../../../gameplay/interstellar-expansion/warp/warp_exotic_matter.py)에서
나온다.

**근거화 정책.** 일반상대성의 교과서 결과(메트릭, 아인슈타인 방정식, 에너지 밀도 표현)는 표준으로
간주해 그대로 서술한다. *비자명한 정량적 주장*은 모두 ADS로 검증된 동료심사 논문에 결부시킨다(인용 수
표기, [References](#references) 참조). 유명한 수치가 논문 초록이 아니라 본문에만 있을 경우, 이 문서는
뒷받침할 수 없는 인용에 그것을 억지로 못 박는 대신 그 사실을 명시한다. 이것은 픽션에 인접한 게임플레이
근거화다. *방법*은 실제 물리이고, *가정*("외래물질은 존재하며 제조 가능하다")이 픽션이다.

> **부호 / 단위 규약.** 메트릭 시그니처는 `(−,+,+,+)`, `c`는 (1로 두지 않고) 명시적으로 표기해
> 게임플레이 코드가 SI를 직접 쓸 수 있게 한다. `β_s ≡ v_s/c`는 버블의 좌표 속도를 `c` 단위로 나타낸
> 것이며 **1을 넘을 수 있다** — 그것이 워프의 핵심이다(국소적으로는 무엇도 광속을 넘지 *않으면서*
> 버블 자체는 전역적으로 광속보다 빠르게 움직인다).

---

## 0. 비전문가용 요약 (수식 없이)

텐서 없이 이야기로만 읽고 싶은 독자를 위한 절이다. 아래 각 절이 여기 주장들을 수식과 인용으로 뒷받침한다.

1. **워프는 우주선을 빠르게 만드는 게 아니라 공간을 움직인다.** 공항 무빙워크 위에 가만히 서 있는
   것과 같다. 내 다리는 안 움직여도 바닥이 나를 실어 나른다. 워프 버블은 *앞쪽 공간을 수축시키고
   뒤쪽 공간을 팽창시켜* 그 안의 우주선을 통째로 실어 나른다. 국소적으로는 무엇도 빛을 넘지 않으니
   상대성이론 위반이 아니지만, 버블 전체로 보면 빛보다 먼저 목적지에 도착할 수 있다. 1994년
   알쿠비에레의 발상이다.
2. **그렇게 공간을 휘려면 "음에너지" 물질, 곧 이종물질이 필요하다.** 우리가 아는 모든 물질은
   에너지가 양수다. 아주 미세한 음에너지는 실재하지만(카시미르 효과), 워프 버블이 요구하는 크고
   안정적인 덩어리는 만들어본 적도 없고 존재하는지도 모른다. NearStars는 그저 *있다고 가정한다*.
   그 가정이 허구이고, 그 둘레의 물리는 진짜다.
3. **필요한 양은 액면 그대로면 절망적이다.** 빠를수록·클수록·벽이 얇을수록 더 든다. 그런데
   양자물리학이 버블 벽을 터무니없이 얇게(플랑크 길이 수준) 강제한다. 그래서 작고 얌전한 속도의
   버블조차 **관측 가능한 우주 질량의 약 1조 배**에 달하는 이종물질을 요구한다. 페닝과 포드는 이를
   "물리적으로 도달 불가능"이라 불렀다.
4. **꼼수로 줄일 수 있지만 한계가 있다.** 반 덴 브룩의 위상학적 "병목"은 거대한 내부를 미시적
   표면 뒤에 숨겨 비용을 *태양 몇 개분*까지 낮춘다("그램"으로 흔히 잘못 인용되지만 논문 원문은
   태양질량이다). 화이트의 NASA 연구(도넛형·두꺼운 벽·진동 버블)는 추가 감축을 주장하나 주변부이고
   미검증이라 이 문서는 그렇게 표시해 둔다.
5. **최근 "양에너지로도 되지 않을까?" 흐름과 그 반박.** 2020년대 들어 음에너지 없이 워프가
   가능하다는 논문이 여럿 나왔다. 비판자들(산티아고·슈스터·비서)은 그 구성들이 *일부* 관측자에게만
   괜찮아 보일 뿐, *모든* 관측자를 따지면 여전히 에너지 조건을 위배함을 보였다. 정리하면 *아광속*
   워프는 언젠가 양에너지로 될 수도 있는 열린 문제지만, 진정한 *초광속* 워프는 여전히 이종물질을
   요구한다. NearStars의 초광속 워프는 바로 그 "여전히 필수인" 영역에 놓인다.
6. **그래서 게임은 정직하게 눈속임한다.** 실제 수치는 약 60자릿수씩 출렁여 쓸 수 없다. NearStars는
   메트릭 계산을 버리고 이종물질을 *선체 질량에 비례하는 적재물*로, 에너지를 *거리 × 질량* 비용으로
   재정의한다. RP-1식 경제에 바로 얹히는 깔끔한 숫자다. 물리 표는 게임이 *왜* 그 도약을 할 수밖에
   없었는지를 보여주려고 남겨 둔 것이다.

**한 줄 요약** — 워프는 공간을 휘어 우주선을 실어 나르는 기술인데, 그러려면 존재할지도 모르는
음에너지 물질이 우주 하나만큼 필요하고, 온갖 꼼수로도 초광속이면 여전히 그것이 필수라서, 게임은
"있다고 치고" 선체 질량과 거리로 비용을 매긴다.

---

## 1. The Alcubierre metric — moving space, not the ship

알쿠비에레의 1994년 논문 [[A94]](#A94)은 평탄한 시공간을 가져와 거기에 국소화된 교란을 더한다 —
**버블 앞쪽 공간을 수축시키고 뒤쪽 공간을 팽창시키는** 교란이다. 버블 안에 가만히 있는 우주선은 공간
자체의 변형에 실려 운반되며, 국소적으로는 결코 `c`를 넘지 않으므로 버블 내부에서 특수상대성 위반은 없다.
선소(버블이 `x` 방향으로 속도 `v_s`로 이동)는 다음과 같다.

```
ds² = −c² dt² + (dx − v_s · f(r_s) · dt)² + dy² + dz²
```

- `x_s(t)`는 버블 중심이고 `v_s = dx_s/dt`다.
- `r_s = √[(x − x_s)² + y² + z²]`는 버블 중심으로부터의 거리다.
- `f(r_s)`는 **성형(탑햇) 함수**다. 내부에서는 `f ≈ 1`, 멀리 바깥에서는 `f ≈ 0`이며 두께 `Δ`의 벽을
  거쳐 전이한다. 흔히 쓰는 형태는
  `f(r_s) = [tanh(σ(r_s+R)) − tanh(σ(r_s−R))] / (2 tanh(σR))`이며, `R`은 버블 반경,
  `Δ ∼ 1/σ`는 벽 두께다.

내부(`f=1`)에서 메트릭은 평탄하다 — 승무원은 자유낙하 상태에 있어 조석 부하도, 가속도 부하도 느끼지
않는다. 모든 곡률은 `f`가 변하는 **벽**에 산다.

다운스트림에서 중요한 표준 재정식화가 둘 있다. **나타리오** [[N02]](#N02)는 드라이브를 **팽창 0**으로
다시 쓴다(부피 요소가 변하지 않고 흐름이 버블 옆으로 공간을 밀어낼 뿐이다) — 거의 모든 현대 재평가가
실제로 쓰는 것이 이 "팽창 0" 형태다. **요크-시간** 표현 [[W13]](#W13)은 응용공학 문헌이 채택한 형태다.

### 1.1 The expansion of space (the "surf" picture)

원래(비-나타리오) 드라이브의 경우 요크 외재곡률 대각합(국소 부피 팽창률)은

```
θ = v_s · (x − x_s)/r_s · df/dr_s
```

벽을 가로질러 `df/dr_s < 0`이므로 버블 뒤쪽에서는 `θ > 0`(공간 팽창), 앞쪽에서는 `θ < 0`(수축)이다.
버블은 자신이 만든 파동을 "서핑"한다. 이것이 또한 워프 운동이 **공간을 통한 물리적 속도가 아닌** 이유이며,
상대성 게임플레이 레이어가 워프 중인 함선을 예외 처리하는 데 이 사실을 쓴다
([relativity-mod.md](../relativity/relativity-mod.md) §2.6(ii)).

---

## 2. Why it needs negative energy

메트릭을 아인슈타인 장방정식 `G_{μν} = (8πG/c⁴) T_{μν}`에 대입하고, 오일러 관측자(4-속도 `n^μ`)가
측정하는 에너지 밀도 `T_{μν}n^μn^ν`를 읽어낸다. 알쿠비에레의 결과 [[A94]](#A94)는

```
T^{00} = −(c⁴/8πG) · (v_s²/4) · (ρ²/r_s²) · (df/dr_s)²        ρ² = y² + z²
```

우변은 `df/dr_s ≠ 0`인 곳(벽)이면 어디서나 **명백히 음수**다 — `−(양수)·(제곱)`이기 때문이다. 따라서
에너지 밀도는 **버블 벽 전역에서 음수**이며, 알려진 모든 고전 물질이 따르는 **약/널 에너지 조건**
(`T_{μν}n^μn^ν ≥ 0`)을 위반한다. 음의 에너지 밀도는 **외래물질**을 정의하는 성질이다. 소량은 실제로
존재하지만(카시미르 효과, 압축 진공), 워프 버블이 요구하는 *거시적이고 성형되고 지속되는* 분포는 한 번도
만들어진 적이 없다 — 그리고 양자장론은 필요한 양만큼의 그것을 금지하는 것으로 보인다 [[PF97]](#PF97).
준고전적으로는 속도가 빨라질수록 문제가 악화된다. 재규격화된 응력-에너지는 **버블 속도가 `c`에 다가갈수록
발산한다** [[H97]](#H97). **"외래물질은 존재하며 제조 가능하다"가 바로 NearStars 게임플레이 레이어가
허용해 주는 가정이다.**

---

## 3. The total energy and its scaling

`T^{00}`를 벽 전체에 대해 적분하면 총 (음의) 에너지가 나온다. 한계 분석의 정전(正典)은
Lobo & Visser [[LV04]](#LV04)다. 매개변수 의존성만 남기면(정확한 계수는 `f`에 따라 달라진다)

```
E ≈ −(c⁴ / 12G) · v_s² · (R² / Δ)          [order-of-magnitude]
```

비용을 정하는 손잡이는 셋이다.

| Knob | Effect | Why |
|------|--------|-----|
| `v_s² = β_s² c²` | 빠를수록 ⇒ 제곱으로 증가 | 왜곡이 파동의 속도에 비례해 커진다 |
| `R²` | 버블이 클수록 ⇒ 제곱으로 증가 | 음에너지가 퍼지는 벽 면적 |
| `1/Δ` | 벽이 얇을수록 ⇒ 선형으로 증가 | 가파른 `f`는 큰 `df/dr_s`를 뜻한다 |

가장 가혹한 부분은 `Δ`다. **양자 부등식**은 음에너지가 얼마나 오래/얼마나 집중되어 지속될 수 있는지를
제한해 `Δ`를 플랑크 길이 쪽으로 몰아붙인다. Pfenning & Ford [[PF97]](#PF97)는 벽이 **수백 플랑크 길이
정도보다 두꺼울 수 없음**을 보였고, 적분된 총 음에너지는 *"물리적으로 달성 불가능"*하다고 결론지었다.
(그들의 초록은 "달성 불가능"이라고 진술한다. 자주 인용되는 *"우주 전체의 질량-에너지보다 크다"*는 수치는
초록이 아니라 논문 본문에 있으므로, 이 문서는 특정 킬로그램 수치를 그 인용에 못 박지 않는다.) 상세한 양자
부등식 기구는 Pfenning의 박사학위 논문 [[P98]](#P98)에 있다.

> **프로토타입이 이 열에 대해 계산하는 값.** `R = 100 m`, `Δ = 10 ℓ_P`(`ℓ_P ≈ 1.6×10⁻³⁵ m`)일 때
> `R²/Δ` 인자만 해도 ~10³⁷이며, `β_s = 10`에서 `|E|/c²`는 **10⁶⁵ kg ≈ 10¹² 관측가능우주 질량** 규모가
> 된다. 이 천문학적 수치는 스케일링 공식에서 나온 **프로토타입 자체의 매개변수 추정**이다 — Pfenning-Ford의
> "달성 불가능"과 일관되며, 어떤 단일 초록에서 인용한 수치가 아니라 자릿수로 제시한 것이다.

균형을 위해 반론 하나를 적어 둔다. Krasnikov [[K03]](#K03)는 양자 부등식이 시공간 지름길을 범주적으로
금지하지는 **않는다**고 주장했다 — 경계가 제약을 가하긴 하지만 "불가능"이라는 평결이 빈틈없는 것은 아니다.

---

## 4. Making it (almost) affordable — reduction strategies

모든 감축 전략은 같은 `v_s² R²/Δ` 인자를 공략한다.

### 4.1 Van Den Broeck topological neck
Van Den Broeck [[VdB99]](#VdB99)는 두 번째 메트릭 왜곡을 통해 그 뒤에 크고 평탄한 내부 부피를 숨기면서
**미시적으로 작은 바깥 표면**("목")을 유지한다. 음에너지가 *바깥* 표면에 비례해 스케일링하므로 총 요구량은
**"수 태양질량"**의 음에너지(그에 상응하는 양에너지와 함께)로 떨어지며, 약에너지 조건의 양자 부등식을
만족시키고 워프 드라이브를 커다란 통과 가능 웜홀과 같은 질량 등급에 놓는다.

> **정정 노트.** "수 그램"이라는 수치가 종종 Van Den Broeck에게 잘못 귀속되는데, 그의 초록은 그램이 아니라
> **태양질량**을 진술한다. 프로토타입의 *최적화* 열(`R_eff = 10⁻¹⁵ m`, `Δ = 1 m` → 그램–kg)은 `R_eff`를
> 공격적으로 줄였을 때 스케일링 공식이 얼마나 크게 흔들리는지를 보이는 **예시용 매개변수 장난감**이다 —
> Van Den Broeck가 발표한 감축이 **아니므로** 그렇게 읽어서는 안 된다. 권위 있는 감축 수치는 §4.1의
> 태양질량 등급 수치와 §5의 현대 결과들이다.

### 4.2 Krasnikov tube
Krasnikov [[K98]](#K98)는 *인과율/제어* 문제(알쿠비에레 버블의 앞쪽에 내부에서 신호를 보낼 수 없다)를
미리 깔아 둔 "튜브" 기하로 해결해 임의로 짧은 왕복을 가능하게 했다. Everett & Roman [[ER97]](#ER97)이
널리 인용되는 에너지론 분석을 내놓았다. 음에너지 요구는 공유한다.

### 4.3 Warp-field optimization (White / Eagleworks) — fringe, treat with care
Harold White의 응용 프로그램 [[W13]](#W13), [[W03]](#W03)은 요구량을 완화하기 위해 **두껍게 한 벽**과
**진동하는** 세기를 가진 **토로이드(고리)** 워프 필드를 제안했고, 이후 "카시미르 공동 마이크로버블" 주장
[[W21]](#W21)을 내놓았다. **주의사항(정직하게 표시함).** 이들은 JBIS/저널 논문이며 **arXiv 프리프린트가
없고, 인용 수가 낮으며(≤17), 어떤 초록에도 정량적 에너지 수치가 없다.** 흔히 거론되는 "목성 질량 → 보이저
질량" 감축 수치는 이 문서가 검증할 수 없는 본문 전문에 있으므로 **여기서 인용하지 않는다.** 이 갈래는 위의
GR 결과와 같은 토대 위에 있지 않은 응용/프린지로 취급하라.

---

## 5. Modern reassessments (2020–2026) — and the pushback

워프가 적어도 광속 미만에서 **평범한(양의) 에너지**로 작동할 수 있는지 묻는 최근 연구의 물결이 있었다.

**주장들.**
- **일반 틀.** Bobrick & Martire [[BM21]](#BM21)는 워프 드라이브를 넓은 부류의 물질 "껍질"로 다시
  정식화하고, **최초의 광속 미만 양에너지** 구대칭 워프 드라이브를 구성했으며, 알쿠비에레의 음에너지
  요구를 **~2자릿수 줄이는** 최적화를 보고했다. 핵심 재구성은 다음과 같다 — 모든 워프 드라이브는 관성으로
  움직이는 물질 껍질이므로 *출발하려면 여전히 추진이 필요하고*, **초광속** 버전은 여전히 에너지 조건 위반을
  필요로 한다.
- **양에너지 솔리톤.** Lentz [[L21]](#L21)는 **순수하게 양인** 에너지 밀도(전도성 플라스마 + 고전 EM)로
  생성되는 초광속 솔리톤을 주장했다. Fell & Heisenberg [[FH21]](#FH21)는 **총 에너지가 태양질량보다
  ~4자릿수 낮은** 양반정부호 에너지 초광속 솔리톤을 찾았다.
- **광속 미만, 모든 조건 만족.** Fuchs 등 [[F24]](#F24)은 양의 ADM 질량을 가진 안정한 물질 껍질을 통해
  **모든** 에너지 조건을 만족한다고 주장하는 **등속 광속 미만** 워프 드라이브를 제시했다.

**비판들(컨센서스 정정).**
- Santiago, Schuster & Visser [[SSV22]](#SSV22)는 양에너지 주장이 *오일러* 관측자에 대해서만 성립함을
  보였다. 약에너지 조건은 **모든** 시간꼴 관측자를 요구한다. 일반적인 워프 드라이브는 — 수정 중력에서조차 —
  **NEC, WEC, SEC, DEC를 모두 위반한다.** 제목이 곧 결론이다 — *generic warp drives violate the null
  energy condition.*
- Schuster, Santiago & Visser [[SSV23]](#SSV23)는 명시적인 나타리오 예제를 들어 워프 시공간의 **ADM
  질량**을 분석해 조건 위반을 확인하고, 버블에서 "질량"과 "움직임"이 무엇을 뜻하는지 명료히 했다 — 양의 ADM
  질량 틀에 대한 직접 반박이다.

**정직한 결론.** *광속 미만* 워프에 대해서는 양에너지 구성이 열려 있고 논쟁적인 가능성이다. 진정한
**초광속** 워프에 대해서는, 2020년대 중반의 컨센서스가 **음(외래) 에너지가 여전히 필요하다**는 것이다 —
가능하다가 아니라 *필요하지만 아직 확보되지 않음*으로 정리되어 있다. NearStars는 의도적으로 그것을 가정으로
치워 버린다.

---

## 6. The three-model spectrum (what the prototype computes)

같은 에너지 적분, 세 가지 `(R_eff, Δ)` 선택, ~60자릿수에 걸친 범위다.

| Model | `(R_eff, Δ)` | `|E|/c²` at `β_s = 10c` | Status |
|-------|--------------|--------------------------|--------|
| **Classic Alcubierre / Pfenning-Ford** | `100 m`, `10 ℓ_P` | ~10¹² 우주 질량 *(프로토타입 추정)* | "물리적으로 달성 불가능" [[PF97]](#PF97) |
| **Optimized (illustrative toy)** | `10⁻¹⁵ m`, `1 m` | ~그램–kg *(장난감, 발표된 값 아님)* | 발표된 감축은 **태양질량 등급** [[VdB99]](#VdB99) → **~10⁻⁴ M_⊙** [[FH21]](#FH21) |
| **Gameplay (KSPIE-style)** | metric discarded | ExoticMatter ∝ ship mass | 유일하게 출하 가능한 모델 |

게임플레이 모델은 메트릭 적분을 완전히 포기한다. ExoticMatter는 **함선 질량에 비례하는 상시 부하**에
**거리×질량 MJ 드라이브 비용**을 더한 것이며, RP-1 스타일 경제에 깔끔하게 들어맞는 여행당 수치를 만들어낸다.
두 물리 열은 게임이 *왜* 그런 도약을 하는지 정당화하기 위해 존재한다 — 그리고 정정된 가운데 행은 문헌의 실제
감축이 (Van Den Broeck의) 태양질량 등급에서 (Fell-Heisenberg의) ~10⁻⁴ 태양질량까지에 안착하며 장난감의
그램이 **아님**을 기록한다. 수치와 시스템별 표는 `prototypes/warp_exotic_matter.py`를 실행해 얻는다.

---

## 7. Implications for NearStars

- 성간 엔드게임은 외래물질을 후기-테크 자원으로 허용한다. 플레이어가 체감하는 **비용 곡선**은 게임플레이
  모델(열 3)이며 cfg에서 튜닝한다.
- 워프 운동은 **물리적 β가 아니다** — 상대성 레이어가 이를 예외 처리하며(§2.6(ii)), §1.1이 그 물리적
  정당화다.
- 정직한 분위기 설정. FTL은 2020년대 중반 문헌이 대량으로 만들 수 없다고 말하는 물질로 사들이는 것이다 —
  그래서 그것이 테크트리의 필연이 아니라 *엔드게임* 역량이 된다. (광속 미만의 "물리적" 워프가 진정으로 열린
  질문이고, 외래물질 벽을 여전히 요구하는 쪽은 FTL이다.)

---

## References

ADS 검증(citation_count 정렬). 형식: tag — author (year), *title* — `bibcode` / arXiv. 인용 수는
2026-06-30 시점 ADS 보고 기준이다.

- <a id="A94"></a>**[A94]** Alcubierre (1994), *The warp drive: hyper-fast travel within general relativity* — `1994CQGra..11L..73A` / arXiv:gr-qc/0009013 — 351 cites
- <a id="LV04"></a>**[LV04]** Lobo & Visser (2004), *Fundamental limitations on 'warp drive' spacetimes* — `2004CQGra..21.5871L` / arXiv:gr-qc/0406083 — 106 cites
- <a id="N02"></a>**[N02]** Natário (2002), *Warp drive with zero expansion* — `2002CQGra..19.1157N` / arXiv:gr-qc/0110086 — 73 cites
- <a id="H97"></a>**[H97]** Hiscock (1997), *Quantum effects in the Alcubierre warp-drive spacetime* — `1997CQGra..14L.183H` / arXiv:gr-qc/9707024 — 56 cites
- <a id="PF97"></a>**[PF97]** Pfenning & Ford (1997), *The unphysical nature of 'warp drive'* — `1997CQGra..14.1743P` / arXiv:gr-qc/9702026 — 139 cites
- <a id="P98"></a>**[P98]** Pfenning (1998, PhD thesis), *Quantum inequality restrictions on negative energy densities in curved spacetimes* — `1998PhDT........38P` / arXiv:gr-qc/9805037 — 42 cites
- <a id="VdB99"></a>**[VdB99]** Van Den Broeck (1999), *A 'warp drive' with more reasonable total energy requirements* — `1999CQGra..16.3973V` / arXiv:gr-qc/9905084 — 88 cites
- <a id="K98"></a>**[K98]** Krasnikov (1998), *Hyperfast travel in general relativity* — `1998PhRvD..57.4760K` / arXiv:gr-qc/9511068 — 104 cites
- <a id="ER97"></a>**[ER97]** Everett & Roman (1997), *Superluminal subway: the Krasnikov tube* — `1997PhRvD..56.2100E` / arXiv:gr-qc/9702049 — 92 cites
- <a id="K03"></a>**[K03]** Krasnikov (2003), *Quantum inequalities do not forbid spacetime shortcuts* — `2003PhRvD..67j4013K` / arXiv:gr-qc/0207057 — 21 cites
- <a id="W03"></a>**[W03]** White (2003), *A discussion of space-time metric engineering* — `2003GReGr..35.2025W` — 17 cites *(no arXiv; applied/fringe)*
- <a id="W13"></a>**[W13]** White (2013), *Warp field mechanics 101* — `2013JBIS...66..242W` — 8 cites *(no arXiv; applied/fringe; no numeric energy figure in abstract)*
- <a id="W21"></a>**[W21]** White et al. (2021), *Worldline numerics applied to custom Casimir geometry generates unanticipated intersection with Alcubierre warp metric* — `2021EPJC...81..677W` — 7 cites *(no arXiv; applied/fringe)*
- <a id="BM21"></a>**[BM21]** Bobrick & Martire (2021), *Introducing physical warp drives* — `2021CQGra..38j5009B` / [arXiv:2102.06824](https://arxiv.org/abs/2102.06824) — 40 cites
- <a id="L21"></a>**[L21]** Lentz (2021), *Breaking the warp barrier: hyper-fast solitons in Einstein-Maxwell-plasma theory* — `2021CQGra..38g5015L` / [arXiv:2006.07125](https://arxiv.org/abs/2006.07125) — 30 cites
- <a id="FH21"></a>**[FH21]** Fell & Heisenberg (2021), *Positive energy warp drive from hidden geometric structures* — `2021CQGra..38o5020F` / [arXiv:2104.06488](https://arxiv.org/abs/2104.06488) — 26 cites
- <a id="F24"></a>**[F24]** Fuchs et al. (2024), *Constant velocity physical warp drive solution* — `2024CQGra..41i5013F` / [arXiv:2405.02709](https://arxiv.org/abs/2405.02709) — 12 cites
- <a id="SSV22"></a>**[SSV22]** Santiago, Schuster & Visser (2022), *Generic warp drives violate the null energy condition* — `2022PhRvD.105f4038S` / [arXiv:2105.03079](https://arxiv.org/abs/2105.03079) — 48 cites
- <a id="SSV23"></a>**[SSV23]** Schuster, Santiago & Visser (2023), *ADM mass in warp drive spacetimes* — `2023GReGr..55...14S` / [arXiv:2205.15950](https://arxiv.org/abs/2205.15950) — 13 cites

## Related

- [`gameplay/interstellar-expansion/feasibility.md`](../feasibility.md) — gate-0 Δv / light-floor / warp-mod survey
- [`gameplay/interstellar-expansion/warp-patch-draft.md`](../../../../gameplay/interstellar-expansion/warp/warp-patch-draft.md) — the minimal-fork warp implementation this fuels
- [`prototypes/warp_exotic_matter.py`](../../../../gameplay/interstellar-expansion/warp/warp_exotic_matter.py) — the 3-model fuel calculator
- [relativity-mod.md](../relativity/relativity-mod.md) — sub-light SR layer; §2.6(ii) warp exemption
