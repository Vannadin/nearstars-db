---
title: Interstellar travel feasibility — gate 0
status: active
created: 2026-06-28
---

# Interstellar travel feasibility — gate 0

**NearStars와의 연결고리.** NearStars 항성계에 도달하는 것은 **post-RP-1
엔드게임 확장 콘텐츠**로 설계되었다. 즉 플레이어가 현실의 RP-1 테크 트리를
모두 완료한 *이후*에 등장하는 콘텐츠다. 그 확장의 테크 트리와 추진,
시스템별 과학 점수를 설계하기에 앞서, 모든 것을 좌우하는 단 하나의 질문이
있다. **NearStars의 실제(미압축) 거리에서, RSS + Principia + RP-1 스택
위에서 성간 여행이 정말로 구현 가능하고 플레이 가능한가**라는 물음이다. 이
문서는 그 gate-0 분석과 거기서 도출된 아키텍처 결정을 기록한다.

**범위.** 포함하는 것은 Δv / 시간 / 추진 트레이드 공간, 상대론적 한계,
warp 모드 조사, 그리고 그로부터 나온 빌드 결정이다. 제외하는 것은 실제
테크 트리 설계, 추진 모드 RO 설정, 시스템별 과학 점수다(이들은 하류 작업이며
이 분석에 게이트된다). 여기서 cfg는 배포하지 않는다 — emit은 프로젝트 말미로
미루어 두며, 여행 플러그인 자체는 C#이다(슐츠 담당,
[[project-nearstars-mod-plugins-schultz]] 참조).

**인터랙티브 동반 자료.** 상대론적 Δv 맵(라이브 슬라이더).
https://claude.ai/code/artifact/43636b83-6e8d-48e3-ae63-025cc89c6c57

---

## 1. Executive summary

| Question | Finding |
|----------|---------|
| Can reaction drives reach the stars fast? | **No.** Chem/NTR/nuclear-ion/adv-electric are impossible at every interstellar setting. Only torch (Isp 10⁶ s) and antimatter (10⁷ s) close — and only over **100–500 yr**. |
| Is there a hard speed limit? | Yes — **the light-speed floor.** Min Earth-frame travel time = distance in ly (Proxima 4.2 yr … TRAPPIST-1 40.7 yr). Faster = FTL = warp-only. |
| Does relativity matter? | Only when pushing toward the floor (>0.3c). There the relativistic rocket Δv (rapidity) explodes — even a photon rocket struggles, antimatter becomes impossible. Below ~0.1c it's negligible. |
| Do the warp mods work with Principia? | **No — both KSPIE and Blueshift are Principia-incompatible** (they reposition vessels without thrust; Principia undoes it). Any warp here is a custom build. |
| Build decision | **Build the interstellar gameplay on the premise of Principia-incompatibility** → two install profiles. May let us skip the custom Principia plugin entirely. |

---

## 2. The Δv trade space (real distances)

거리는 모두 실제 값이며 `db/systems/*.json`에서 가져왔다(미압축, pc → ly
×3.261564). 연속 추력 방식의 **brachistochrone** 궤적이다(중간 지점까지
가속한 뒤 뒤집어서 감속). 사용한 관계식은 교과서 수준의 것뿐이다(로켓 방정식,
상대론적 로켓 / rapidity).

- 지구 기준계 평균 속도 `β = d / (c·T)` — **β < 1을 요구한다**.
- Rapidity `φ = 2·atanh(β)`. Δv `= 2φ·c`(정지) 또는 `φ·c`(flyby).
- 최고 속도 `β_peak = tanh φ`, `γ = 1/√(1−β_peak²)`.
- 승무원(고유) 시간 `τ = T·φ/sinh φ` — 높은 β에서는 지구 시간 T와 크게
  벌어진다.
- 질량비 `MR = exp(Δv / v_e)`, `v_e = Isp·g₀`.

추진 방식별 배기 속도(공학적 참고치). Fusion (Daedalus) 10⁵ s
= 0.0033c · Torch 10⁶ s = 0.033c · Antimatter 10⁷ s = 0.33c · Photon rocket = c.

| System | dist | light floor | feasible reaction-drive route |
|--------|------|-------------|-------------------------------|
| Proxima Cen | 4.2 ly | 4.2 yr | Torch ~200 yr · Antimatter ~50–100 yr |
| Alpha Cen | 4.4 ly | 4.4 yr | as Proxima |
| Barnard | 6.0 ly | 6.0 yr | Torch ~300 yr · Antimatter ~100 yr |
| Luhman 16 | 6.5 ly | 6.5 yr | Antimatter ~100 yr |
| Tau Ceti | 11.9 ly | 11.9 yr | Antimatter ~150–200 yr |
| 40 Eridani | 16.3 ly | 16.3 yr | Antimatter ~200 yr |
| Fomalhaut | 25.1 ly | 25.1 yr | Antimatter ~200–300 yr |
| TRAPPIST-1 | 40.7 ly | 40.7 yr | Antimatter only, multi-century; <100 yr needs photon-class |

**결론.** 성간 여행은 torch/antimatter급 추진(Isp 10⁶–10⁷ s)을 요구하며,
이는 RP-1의 화학/NTR/초기 핵 추진을 한참 넘어선다. 이는 성간 여행이 반드시
먼 미래의 확장이어야 한다는 점, 그리고 **추진이 진짜 병목**이라는 점을
확인해 준다. reaction drive로 "먼 별까지 빠르게 가기"는 물리적으로 불가능하다.
예컨대 TRAPPIST-1을 50 yr에 가려면 평균 0.81c → Δv ≈ 4.5c → antimatter MR
~10⁶(불가능), photon ~94가 된다.

---

## 3. The light-speed floor & the two clocks

- **광속 하한.** 지구 기준계 여행 시간은 결코 빛을 이길 수 없다.
  `T_min = d/c`다. 따라서 TRAPPIST-1(40.7 ly)은 어떤 reaction drive로도
  ~41 yr 미만으로는 도달할 수 없으며, **30 yr는 완전히 불가능하다**(FTL).
  이것이 현실주의 경로가 부딪히는 단단한 벽이다.
- **두 개의 시계.** 승무원의 고유 시간은 지구 시간보다 느리게 흐른다.
  TRAPPIST-1을 지구 기준 50 yr에 가면 승무원은 ~24 yr를 겪는다(γ≈5).
  현실주의 순항 플러그인은 이를 장부 관리해야 한다. 달력은 지구 연 단위로
  점프하는 반면, 승무원과 생명 유지 장치, 부품 노화는 승무원 연 단위로
  진행된다. 상대론이 게임플레이에 닿는 유일한 지점이 바로 여기이며,
  이는 물리 엔진 변경이 아니라 플러그인 장부 관리의 문제다.
- **상대론의 적용 범위.** ~0.1c 아래에서는 무시할 만하고(여유 있는 antimatter
  미션이 여기에 해당), 하한선으로 밀어붙일 때에만 결정적이 된다. 우리는 엔진
  안에서 상대론을 시뮬레이션하지 않는다(KSP에서는 불가능하다 — c 근방의
  float32, 단일 UT 시계, Principia 디싱크). 상대론은 전이 시간을 계산하는
  그 어떤 곳에든 공식으로 존재한다.

---

## 4. Warp-mod survey

두 후보 warp 모드를 비교했다(전체 출처는 아래). 핵심 요지는 다음과 같다.

| | KSPIE — Alcubierre Drive | Blueshift (Angel-125) |
|---|---|---|
| Mechanic | Alcubierre bubble, 78 warp factors; moves via orbit state-vector rewrite + rail-warp | FTL cruise + jump-gate; moves via per-frame `SetPosition()` |
| Energy | ExoticMatter + MegaJoules, mass-scaled, reactor-driven | Graviolium → GravityWaves (mined, arcade-themed) |
| Gravity well | gravity caps max speed; no atmo warp | SOI speed curve; ×1000 interstellar boost; location classes |
| RP-1 tone | "hard-adjacent" reactor progression | explicit Star-Trek arcade (worst RP-1 fit) |
| Maintenance | dormant (Nov 2021), community fork exists | **active (v1.16, Mar 2026)** |
| License | custom non-OSI | **code GPL-3.0** (forkable), art ARR |
| Principia | incompatible (inferred, near-certain) | **incompatible — named in Principia FAQ** |

**둘 다 같은 근본 원인으로 Principia와 호환되지 않는다** — 추력 없이 함선을
재배치하는데, Principia가 매 틱마다 이를 되돌리기 때문이다. 참조 선택은
**Blueshift**다. GPL-3.0(법적으로 적응 가능)이고 적극적으로 유지되며, 중력
우물 게이트 + 위치 인지 속도 모델이 올바른 게임플레이 형태이기 때문이다(우물
안에서는 아광속, 평탄한 성간 공간에서는 거대한 부스트). RP-1 톤을 위해서는
**KSPIE의 질량 스케일 reactor/ExoticMatter 경제**를 빌려 온다. 빌려 오는 것은
*모델*이지 결코 *propagation*이 아니다.

---

## 5. Decision — build Principia-incompatible first (two profiles)

모든 warp 옵션(그리고 현실주의 torch-cruise)은 Principia를 인지하는 맞춤
엔지니어링을 필요로 하기 때문에, **성간 게임플레이를 Principia 비호환을
전제로 먼저 빌드한다.** 이는 자연스럽게 NearStars를 두 개의 자기 정합적인
설치 프로파일로 나눈다.

| | Principia profile | Non-Principia profile (interstellar) |
|---|---|---|
| Orbits | true n-body, real multi-star dynamics | stock patched-conics + **SigmaBinary** |
| Interstellar travel | effectively none (warp incompatible) | **warp works** |

- **핵심 이점.** 비-Principia 프로파일에서는 **SigmaBinary와 warp이 서로
  호환된다**(둘 다 비-Principia). 따라서 Blueshift 기반 warp을 거의 그대로
  사용할 수 있고, 비용이 큰 "Principia 인지 맞춤 propagation"은 **아예 생략**할
  수 있다(또는 미래의 "통합" 항목으로 무기한 미룰 수 있다). (b)
  Principia가-순항을-통합 게이트와 (c) 추력-하-time-warp 게이트는 이 프로파일에서
  무의미해진다.
- **트레이드.** 성간 플레이어는 Principia의 n-body를 포기한다 — 다중성계는
  SigmaBinary/conics로 되돌아간다. 합리적인 선택으로 받아들인다. 하드한
  n-body 리얼리즘과 warp 성간 판타지는 대체로 서로 다른 관객층이기 때문이다.
- **역할 경계.** 설계 / 스펙 / cfg(부품, 테크 배치, 과학 점수, warp 모델)는
  이쪽이고, warp/cruise C#(Blueshift 포크 포함)은 슐츠 담당이다
  ([[project-nearstars-mod-plugins-schultz]] 참조).

---

## 6. Open questions / next

- **게임플레이 루프 설계**(비-Principia 프로파일). warp 모델 세부, drive 부품,
  성간 미션 아크, 도착 경험.
- **추진 / drive 선택**. Blueshift 포크 warp 대 현실주의 torch 옵션, 그리고
  둘 다 제공할지 여부(warp = 주력, torch = 하드 모드 현실주의 대안).
- **테크 트리 배치 및 밸런스**. RP-1 트리를 지나 성간 분기가 어디에 붙는지(더
  넓은 확장 계획과 연결된다).
- **시스템별 과학 점수**. `docs/reference/science-system.md`와 확장 트리의
  노드 비용을 사용해 마지막에 설정한다.
- **거리 압축**은 이제 블로커가 아니라 *튜너*다 — 여행을 단축하거나 향후 Principia
  통합 부담을 덜기 위한 선택지다. 필요할 때에만 결정한다.

---

## Sources

- Principia FAQ (warp/SigmaBinary incompatibility): https://github.com/mockingbirdnest/Principia/wiki/Installing,-reporting-bugs,-and-frequently-asked-questions
- KSPIE Alcubierre: https://github.com/sswelm/KSP-Interstellar-Extended/blob/master/FNPlugin/Propulsion/AlcubierreDrive.cs · https://github.com/sswelm/KSP-Interstellar-Extended/wiki/Warp-Drives
- Blueshift: https://github.com/Angel-125/Blueshift · https://raw.githubusercontent.com/Angel-125/Blueshift/master/Source/Blueshift/WarpTech/WBIWarpEngine.cs
- RP-1 supported configs: https://github.com/KSP-RO/RP-1/wiki/Which-mods-have-RP1-Configurations%3F
- Distances: `db/systems/*.json`. Δv math: standard rocket / relativistic-rocket equations (textbook).

## Related

- [rp1-integration](../rp1-integration/plan.md) — the RP-1 career-layer integration this expansion sits on top of
- [science-system](../../docs/reference/science-system.md) — per-body science values (feeds the expansion's payoff)
