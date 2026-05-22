<!-- 큐레이션된 P3 entry 들 사이의 시각 / 아트 중복 audit + 차별화 후보 정리 -->
# Art-redundancy audit — 2026-05-22

목적은 현재 큐레이션된 12개 Phase 3 entry 의 in-game 시각 identity 를
서로 비교해 "거의 같은 그림" 이 되는 그룹을 식별하고, 각 그룹마다 어떤
대안 시나리오 / 어떤 문헌 근거로 차별화할 수 있는지 미리 정리해 두는
것입니다. 실제 cfg 변경은 이 문서에서 하지 않습니다 — 나중에 해당 entry
를 갱신할 때 해당 행만 펼쳐서 작업에 들어갈 수 있도록 후보 + 정책 위치
(canonical-aligned / tie-break / documented-divergence) 까지 같이 적습니다.

## Scope

12 entry 가 현재 큐레이션 완료 상태.

- TRAPPIST-1 시스템: b, c, d, e, f, g, h (행성 7) — 호스트 별 ★ 합성은 없음
- Alpha Centauri A (★)
- Alpha Centauri B (★)
- Proxima Cen (★)
- Proxima Cen b (행성)
- Proxima Cen d (행성)

호스트 별 ★ 합성 3 개 (α Cen A/B, Proxima) 는 G2V / K1V / M5.5V 로 분광형
이 모두 다르고, TRAPPIST-1 ★ 합성이 아직 없어서 별 entry 사이 중복은
없습니다. 행성 entry 9 개에서만 분석합니다.

## Art categories — 9 행성 분류

각 entry 의 시각 아이덴티티를 핵심 시나리오 한 문장으로 요약.

| Entry | Host SED | Surface state | Atmosphere | Substellar feature |
|---|---|---|---|---|
| T-1 b | M8V 2566 K | airless ultramafic | none | 신선한 magma 흔적 (induction-heated) |
| T-1 c | M8V 2566 K | 풍화된 basalt | 0.1 bar O₂ (fossil) | 없음 |
| T-1 d | M8V 2566 K | bare rock | ~0.01 bar trace | terminator H₂O-ice cloud band |
| T-1 e | M8V 2566 K | aquaplanet | 1 bar N₂+CO₂ | substellar 열린 물 디스크 ~60° |
| T-1 f | M8V 2566 K | aquaplanet (변형 1 bar CO₂) | 1 bar CO₂ | substellar 열린 물 디스크 ~40° (작음) |
| T-1 g | M8V 2566 K | 완전 snowball + sub-glacial ocean | 0.05 bar CO₂ | 없음 (전역 ice) |
| T-1 h | M8V 2566 K | 동결 sub-Mars rocky + CO₂ frost | 0.005 bar | 없음 (풍화 bedrock) |
| Proxima b | M5.5V 2980 K | aquaplanet | 1 bar N₂+CO₂ | substellar 열린 물 디스크 ~60° |
| Proxima d | M5.5V 2980 K | Mercury-analog bare rock | 10⁻⁹ Pa Na exosphere | 부분 용융 magma pond (insolation-driven) |

## 중복 그룹

### 그룹 A — M-dwarf eyeball aquaplanet (3-way)

| Entry | Host | atm pressure | atm comp | ocean lens deg |
|---|---|---|---|---|
| T-1 e | M8V 2566 K | 1 bar | N₂+CO₂ | 60 |
| T-1 f | M8V 2566 K | 1 bar | CO₂ 우세 | 40 |
| Proxima b | M5.5V 2980 K | 1 bar | N₂+CO₂ | 60 |

**중복 강도. 매우 높음.** 세 entry 모두 "M 왜성 아래 1 bar 대기 + 조석
고정 + substellar 열린 물 디스크" 의 같은 시각 recipe 를 따릅니다. 호스트
SED 색온도 차이 (2566 K vs 2980 K) 와 ocean lens 각도 차이는 옆에 놓고
비교하지 않으면 거의 분간이 안 됩니다.

#### 차별화 후보

각 entry 마다 어떤 시나리오로 옮길 수 있는지, 어느 문헌이 지지하는지,
정책 위치는 어떤지 정리.

| Entry | 대안 시나리오 | 문헌 근거 | 정책 위치 | 비고 |
|---|---|---|---|---|
| **Proxima b** | Venus-analog runaway greenhouse (~90 bar CO₂ + SO₂, 표면 안 보임, T_sf ~700 K, 황산 cloud deck) | Lee 2021 (2109.06963) Venus-like 대기에서 photochemical escape. Meadows 2018 §3 환경 상태 enumeration | **documented-divergence** | canonical Boutle/Del Genio 의 aquaplanet 으로부터 의도적으로 벗어남. ★ 추천 — 정책 도구의 첫 실전 use-case + 아트 차별화 동시 |
| **T-1 f** | 0.1 bar CO₂ snowball variant (open-water 없음, 전역 ice) | Turbet 2018 GCM consensus. f.md 의 기존 ## Canonical alternatives 섹션이 이미 이 변형을 기록 | tie-break flip (canonical 으로 변형) | 현재 cfg 가 documented-divergence 로 Wolf 2017 1 bar eyeball 을 선택. 그 선택을 뒤집어 canonical snowball 로 가면 g 와 비슷해지므로 별로 추천하지 않음 |
| **T-1 e** | 그대로 (canonical aquaplanet, M-dwarf HZ 의 대표 후보로 유지) | Wolf 2017 / Glidden 2025 / Sergeev 2020 컨센서스 | canonical-aligned | **유지 권장** — TRAPPIST-1 의 "iconic 거주 가능 후보" 역할 |

**권장 액션**. Proxima b 를 Venus-analog 로 격상 (documented-divergence).
이렇게 하면 e 가 TRAPPIST-1 의 aquaplanet 단일 대표가 되고 f 는 좁은
disk + 차가운 edge variant 로 e 와 살짝 구분되며, Proxima b 는 완전히
다른 장르 (cloud-shrouded hot Venus) 로 빠집니다.

### 그룹 B — Hot rocky with substellar magma (2-way)

| Entry | Host | Mass | Driver | Insolation |
|---|---|---|---|---|
| T-1 b | M8V 2566 K | 1.37 M⊕ | induction heating (Grayver 2022 exo-Io) | 4.3 S⊕ |
| Proxima d | M5.5V 2980 K | 0.26 M⊕ Msini | insolation only | ~17 S⊕ |

**중복 강도. 중간.** 둘 다 "뜨거운 바위 표면 + substellar 의 빨강 발광"
시각 패턴이지만, 메커니즘과 표면 detail 이 다릅니다. T-1 b 는
induction-driven 활성 volcanism (Io analog) 으로 sulfur tint + 활동성
plume 가 가능하고, Proxima d 는 insolation-driven 정적 partial melt 로
Mercury 식 craters + 작은 magma pond 만 있습니다.

#### 차별화 후보

| Entry | 강조 후보 | 문헌 근거 | 정책 위치 |
|---|---|---|---|
| **T-1 b** | Io-analog active volcanism — sulfur frost + 노란-주황 plume 가시화, multiple substellar 활성 vent | Barr 2018 / Dobos 2019 induction Io class. b.md 현재 cfg 가 sulfur 톤을 충분히 강조하지 않음 | tie-break 의 추가 정련 |
| **Proxima d** | Mercury-analog 정적 cratering 강조 — 활동성 vent 없음, Na exosphere만, antistellar volatile cold-trap 시각화 | Killen 2007 Mercury exosphere. Ipatov 2023 volatile delivery | 현 cfg 와 일관, tie-break 디테일 추가 |

**권장 액션**. cfg 수치 변경 없이 surface_tint / accent / morphology 의
디스크립션 prose 만 강화하면 충분합니다. T-1 b 에 활성 vent 묘사,
Proxima d 에 정적 cratering + cold-trap 묘사를 더 명시적으로.

### 그룹 C — Thin-atmo bare rocky (2-way)

| Entry | Host | atm pressure | Surface | Distinctive feature |
|---|---|---|---|---|
| T-1 c | M8V 2566 K | 0.1 bar O₂ | 풍화된 basalt | clear, no clouds |
| T-1 d | M8V 2566 K | ~0.01 bar trace | bare rock | terminator H₂O-ice cloud band |

**중복 강도. 낮음.** 둘 다 "얇은 대기 + 노출된 바위" 이지만 d 의
terminator cloud 가 명확한 시각 차별점이고 c 는 "fossil O₂ 의 산화
지질" 시각을 갖습니다. 이미 충분히 다른 entry.

#### 차별화 후보

| Entry | 강조 후보 | 문헌 근거 | 정책 위치 |
|---|---|---|---|
| **T-1 c** | "fossil O₂ rust" 산화된 표면 — 짙은 빨강-갈색 iron oxide 패턴 | Lincowski 2023 fossil O₂ 시나리오. Luger & Barnes 2015 hydrodynamic escape | tie-break 정련 (현 hex 색상 살짝 더 oxidation 쪽으로) |
| **T-1 d** | terminator H₂O-ice cloud band 시각 강화 — 현재보다 좀 더 dramatic 한 crescent geometry | Turbet 2023 GCM | tie-break 정련 |

**권장 액션**. 현 cfg 유지. 향후 시각 패스에서 c 의 표면 tint 를 좀 더
"녹슨 빨강" 으로, d 의 terminator cloud 를 좀 더 선명하게 다듬는 정도.

### 그룹 D — Frozen world (no overlap, comparison only)

| Entry | Host | atm pressure | Distinctive feature |
|---|---|---|---|
| T-1 g | M8V 2566 K | 0.05 bar CO₂ | 완전 snowball + sub-glacial ocean |
| T-1 h | M8V 2566 K | 0.005 bar | sub-Mars + CO₂ frost over weathered bedrock |

**중복 강도. 없음.** g 는 ocean world, h 는 sub-Mars rocky 로 mass +
geology 가 다릅니다. 같은 "cold" 카테고리지만 시각 identity 가 충분히
구분됩니다.

#### 추가 정련 후보

| Entry | 강조 후보 | 정책 위치 |
|---|---|---|
| **T-1 g** | sub-glacial cryovolcanic plume (Quick 2023 prospects for cryovolcanism on cold ocean planets — Tier B paper 활용) | tie-break 정련 (현 cfg 에 cryovolcanic vent 없음) |
| **T-1 h** | desiccated O₂+CO₂ post-runaway alternative — Lincowski 2018 의 counterintuitive habitability variant 를 cfg variant 로 명시 | cfg variant in Open items (이미 일부 기록됨) |

## Star entries — no redundancy

3개 star ★ 합성 (α Cen A G2V, α Cen B K1V, Proxima Cen M5.5V) 은 분광형이
모두 다르고, TRAPPIST-1 ★ 합성 (M8V) 이 아직 없어서 별 entry 사이의 시각
중복이 없습니다. TRAPPIST-1 ★ 합성을 추가할 때 Proxima Cen 과 비교해
중복 가능성을 다시 봐야 합니다 (M5.5V 빨강 + flare vs M8V 더 빨강 +
flare).

## 우선순위 권장 요약

1. **★ 추천. Proxima b → Venus-analog runaway greenhouse (documented-
   divergence).** Lee 2021 + Meadows 2018 지지. 그룹 A 의 3-way 중복을
   2-way 로 줄이고, 정책 도구 (## Canonical alternatives 섹션) 의 첫 실전
   사용. 작업 시간 ~1-2h.
2. **권장. T-1 b 와 Proxima d 의 prose 강화 (cfg 수치 변경 없음).**
   T-1 b 에 Io-analog 활성 volcanism 더 명시, Proxima d 에 Mercury 식
   정적 cratering + Na exosphere 강조. 작업 시간 ~30분 각각.
3. **선택. T-1 c 산화 표면 색상 정련, T-1 d terminator cloud 강화.** 시각
   패스에서 hex 색상만 살짝 조정. 작업 시간 ~15분 각각.
4. **선택. T-1 g cryovolcanic plume 추가.** Quick 2023 Tier B paper 활용.
   작업 시간 ~30분.

## Future considerations

향후 큐레이션 wave 에서 새 entry 가 추가될 때 이 audit 에 행을 추가하고
중복 그룹을 재평가합니다. 특히 주의할 후보.

- **TRAPPIST-1 ★ 별 합성을 추가할 때**: Proxima Cen 과의 M-dwarf flare
  star 중복 평가 필요.
- **다른 M 왜성 시스템 (예: GJ 1132, Wolf 1069, LHS 1140)** 의 행성을
  큐레이션할 때: 그룹 A 의 eyeball aquaplanet recipe 가 또 등장할 가능
  성. 각 시스템의 호스트 + 행성 mass-radius-insolation 조합으로 시나
  리오를 다양화 (steam, desiccated, ice ball, Venus, eyeball) 해야 함.
- **Sun-like 별 (α Cen A 같은 G/K dwarf) 의 행성을 큐레이션할 때**: 별
  자체는 unique 하지만 행성은 또 다른 그룹을 만들 가능성. 특히 α Cen A
  의 Beichman/Sanghi 2025 후보 giant 가 확인되면 첫 진짜 giant cfg 가
  필요해짐 (현재 카탈로그는 모두 terrestrial).

## 결정 게이트

위 권장 1~4 가운데 어느 것을 언제 실행할지는 사용자 결정. 이 audit 은
"준비 문서" 로서, 실제 cfg 변경을 트리거하지 않습니다. 변경할 entry 가
결정되면 해당 시스템 working dir 에 새 phase3 작업을 시작합니다 (예:
Proxima b Venus-analog 격상은 `phase3/alpha-cen-proxima-system/`
재방문).
