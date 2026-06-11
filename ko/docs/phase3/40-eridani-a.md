# 40 에리다니 A — Phase 3 합성

40 에리다니 A (HD 26965, HR 1325, GJ 166 A, 케이드)는 5.01 pc 거리에
위치한 K0.5 V 왜성입니다. 40 에리다니 삼중성계의 가장 밝은 성분으로,
Ma 2018 이 발견했다고 발표했던 가상의 행성 "벌컨"이 Burrows 등 2024
에 의해 활성도 잡음으로 반박된 별이기도 합니다. 같은 계에는 DA 백색
왜성 40 에리다니 B (`docs/phase3/40-eridani-b.md`)와 M4.5 Ve 플레어
스타 40 에리다니 C / DY Eri (`docs/phase3/40-eridani-c.md`)가
포함되며, B-C 쌍은 A 로부터 약 83″ (투영 거리 약 400 AU) 떨어진
위치에서 중력적으로 묶여 있고 외측 궤도는 Tokovinin MSC 2018 기준
약 8000 년으로 추정되어 케플러 궤도 적합이 불가능한 상태입니다.

별의 기본 항성 파라미터는 두 개의 독립적인 간섭계 측정 결과가 1σ
수준에서 일치할 만큼 매우 잘 정해져 있습니다. Boyajian 등 2012 의
CHARA Classic H 밴드 관측은 θ_LD = 1.504 ± 0.006 mas, R =
0.8061 ± 0.0036 R☉, Teff = 5143 ± 14 K, L = 0.4078 ± 0.0032 L☉
값을 제시합니다 (Table 6, 샘플에서 GJ 166 A 로 식별). Rains 등
2020 은 VLTI/PIONIER 4 망원경 결합으로 θ_LD = 1.486 ± 0.012 mas
→ R = 0.804 ± 0.006 R☉, Teff = 5126 ± 30 K, L = 0.40 ± 0.01 L☉
을 독립적으로 측정합니다 (Table 4. 40 Eri A 는 표 1 의 16 개 중
7 번째). 두 측정값 모두 Phase 2 DB 에 들어가 있으며, Boyajian
2012 가 fractional uncertainty 가 더 작아서 (두 측정 모두
interferometry 인 동률 상황에서의 tiebreak) 권장 primary 가
됩니다.

질량의 anchor 는 Ma 등 2018 의 M = 0.78 ± 0.08 M☉ 입니다 (Table
2, Torres 등 2010 의 M-R 관계 + 분광 Teff/[Fe/H] 조합). 동일
논문이 지금은 반박된 "벌컨" 후보를 발표했던 paper 입니다. Diaz 등
2018 의 SPECIES isochrone 은 독립적으로 0.76 ± 0.03 M☉ 을 산출해
1σ 안에서 일치합니다. A-BC 외측 궤도가 너무 길어 케플러 적합이
안 되기 때문에 (Tokovinin MSC 2018 이 "Keplerian solution 없음"
으로 분류) 동역학적 질량은 존재하지 않습니다.

**Age 는 이번 합성의 documented divergence 입니다.** Ma 등 2018 의
PARSEC isochrone fitting 은 6.9 ± 4.7 Gyr 을 제시합니다. K 왜성
isochrone 의 전형적인 결과이며 Gyr 스케일에서의 K 왜성 나이
부정확성이 그대로 드러나는 값입니다 (SPECIES Diaz 2018 은 같은
평탄한 χ² 바닥 위에서 9.23 ± 4.84 Gyr 을 보고합니다). Bond 등
2017 §6.2 는 백색왜성의 initial-final mass relation 을 이용해
시스템 공통 나이를 **~1.8 Gyr** 로 유도합니다. 40 Eri B 의
M_final = 0.573 M☉ 이 ~1.8 M☉ 의 progenitor 를 시사하고, 주계열
수명 ~1.7 Gyr + 냉각 나이 122 Myr 이 그 합산값입니다. Bond 는
"새 질량 이후 excessive age 우려는 해소된 것으로 보인다" 고
명시합니다. 즉 K 왜성 isochrone 의 옛 노년 나이는 역사적으로
유효했지만 WD progenitor 분석은 그 값을 지지하지 않습니다. 이번
Phase 3 합성은 cfg age 로 ~1.8 Gyr 을 채택합니다. IFMR 기반
시스템 공통 나이가 60+% 상대 불확실도를 가진 K 왜성 isochrone
단일값보다 물리적으로 더 강하게 제약되기 때문입니다. K 왜성
isochrone alternative 는 `## Canonical alternatives` 에 보존합니다.

금속도는 다소 sub-solar 이며 [Fe/H] = −0.29 ± 0.12 입니다 (Diaz
2018 SPECIES; Bensby 2014 thin/thick-disk 서베이의 −0.31 ± 0.10
이 1σ 안; Ma 2018 의 −0.42 ± 0.04 가 marginally 더 낮음). Burrows
등 2024 가 NEID line-by-line 활성도 분석에서 도출한 자전 주기는
~42 일 입니다 (paper 는 formal uncertainty 없이 "∼42 days" 라고만
명시) — 이 자전 변조가 바로 가짜 "벌컨" 42 일 RV 신호를 만들어낸
원흉입니다. Burrows 이전 문헌은 더 짧은 자전 주기를 제시합니다
(Saar & Osten 1997 의 Mt. Wilson HK 기반 ~37–38 일; Diaz 2018 의
HARPS S-index ~38 일). 그 차이는 현재 문헌상 미해결입니다.
색층권 활성도 log R'HK = −4.99 (Jenkins 2011) 는 40 Eri A 를 태양
평균보다 약간 더 활동적인 조용한 K 왜성으로 분류합니다. X-ray
모니터링은 빈약합니다. ROSAT 전천 서베이의 baseline 은 0.5–2 keV
대역에서 log L_X ≈ 27.5 cgs 입니다.

**NearStars 의 시나리오 선택: 큐레이션된 행성이 없는 조용하고 약간
나이 든 K0.5 V 별로, ~83″ 떨어진 B-C 쌍이 한 점으로 보이는 원격
binary 시점에서 렌더링합니다.** 14 개의 canonical-aligned cfg 픽은
모두 paper-verified 파라미터 셋을 그대로 따릅니다. Age 는
documented divergence 입니다 (Bond 2017 IFMR 가 Ma 2018 K 왜성
isochrone 보다 우선). 한 개의 tie-break 은 K0.5 V SED 의 시각
표면 색조를 정합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K0.5 V | high | Keenan & McNeil 1989 — IAU MK 분류 |
| `mass_msun` | 0.78 ± 0.08 | high | Ma 등 2018 — M-R 관계 (Torres 2010) + 분광 Teff/[Fe/H]; Diaz 2018 SPECIES 의 0.76 ± 0.03 이 1σ 안에서 일치 |
| `radius_rsun` | 0.8061 ± 0.0036 | high | Boyajian 등 2012 — CHARA Classic H 밴드 간섭계, θ_LD = 1.504 ± 0.006 mas; Rains 2020 VLTI/PIONIER 의 0.804 ± 0.006 도 일치 |
| `teff_k` | 5143 ± 14 | high | Boyajian 등 2012 — 간섭계 θ_LD + 볼로메트릭 플럭스; Rains 2020 의 5126 ± 30 가 1σ 안에서 일치 |
| `luminosity_lsun` | 0.4078 ± 0.0032 | high | Boyajian 등 2012 — 볼로메트릭 플럭스 적분; Rains 2020 의 0.40 ± 0.01 이 일치 |
| `metallicity_fe_h_dex` | −0.29 ± 0.12 | high | Diaz 등 2018 — SPECIES 고분해 분광; Bensby 2014 의 −0.31 ± 0.10 thin-disk 서베이가 보강 |
| `age_gyr` | 1.8 | medium | Documented divergence: Canonical alternatives 참조. Bond 2017 §6.2 의 IFMR 기반 시스템 공통 나이 (initial mass ~1.8 M☉, MS 수명 1.7 Gyr + 냉각 122 Myr) |
| `rotation_period_days` | 42 | medium | Burrows 등 2024 — NEID line-by-line 활성도 분석; paper 는 "∼42 days" 만 명시하고 formal σ 없음. 가짜 벌컨 RV 신호의 정체와 동일 |
| `activity_log_rhk` | −4.99 | medium | Jenkins 등 2011 — Ca II H&K HARPS 색층권 서베이; Henry 1996 의 −4.94 가 보강 |
| `x_ray_log_lx_cgs` | ~27.5 | low | ROSAT 전천 서베이 baseline 0.5–2 keV; 전용 XMM/Chandra 장기 사이클 모니터링 출간본 없음 |
| `vulcan_disposition` | Refuted (Burrows 2024) | high | Burrows 등 2024 NEID line-RV + 활성도 상관 + depth dependence; 16 년 다기기 RV (HIRES, PFS, CHIRON, HARPS, NEID); 42 일 신호는 별의 자전이지 케플러 궤도 아님 |
| `visual_surface_tint_hex_primary` | `#ffd5a8` (K0.5 V 의 따뜻한 오렌지-크림) | medium | Tie-break: 5143 K K0.5 V 흑체를 태양보다 약간 더 차분한 톤의 크림으로 렌더링; 동반성 C 의 짙은 빨강과의 interesting-first 대비 |
| `stellar_color_temp_k` | 5143 | high | Teff 에서 유도 |
| `star_apparent_diameter_arcsec_from_bc_barycenter_at_400au` | 1.9 | high | 유도값: 2 R★ / a × (180·3600/π); a = B-C 까지의 투영 분리 400 AU |
| `visual_companion_event_b_c_pair_separation_arcsec_from_a` | ~83 | high | WDS J04153−0739; A-BC 외측 궤도 미적합 (Tokovinin MSC 2018) 이라 분리각은 ~8000 년 스케일에서 천천히 변동 |
| `apparent_magnitude_v_from_earth` | 4.43 | high | Hipparcos van Leeuwen 2007; 에리다누스 자리의 육안 별, 전통 이름 케이드 |

## Surface synthesis

40 Eridani A 의 광구는 전형적인 K0.5 V 왜성의 모습을 보여줍니다.
태양의 G2 V 보다 약간 더 차갑고, 중간형 K 왜성 특유의 크림-오렌지
조명이 두드러집니다. Teff = 5143 K 에서 SED 피크는 녹황색 ~563 nm
이며, 태양의 ~501 nm 피크에서 ~600 K 더 차가운 광구 때문에 이동한
값입니다. 색도 좌표상 따뜻한 오렌지 색조에 해당해서, 0.65 AU 의
거주 가능 영역 내측 가장자리 (지구와 같은 조도) 에 가상의
관측자가 있다면 약간 호박색 "태양" 으로 보일 것입니다.

CHARA Classic 간섭계 측정값 (Boyajian 2012) 은 각지름을 0.4%
정밀도로 정합니다. 문헌 안에서 가장 잘 정해진 K 왜성 직경 중
하나입니다. 독립적인 VLTI/PIONIER 결과 (Rains 2020) 도 θ_LD 와
유도 Teff 모두 1σ 안에서 일치합니다. 두 간섭계 어레이는 beam
combiner 도, 통과대역도 다르고 (CHARA H 밴드. PIONIER 도 H 밴드
지만 4 망원경), limb-darkening prescription 도 다릅니다. 그래서
이 일치는 fundamental 파라미터 셋에 대한 강력한 validation 입니다.

흑점 커버리지는 중간 수준입니다. log R'HK = −4.99 (Jenkins 2011)
는 40 Eri A 를 중간 활성도 K 왜성 기준으로는 조용한 별로 분류
하지만, 태양 quiet-cycle 평균값인 log R'HK ≈ −4.95 보다는 약간
더 활성도가 높습니다. 42 일 자전 주기 (Burrows 2024) 는 이 Teff
에서의 Noyes 1984 대류 turnover ~40 d 을 적용하면 Rossby 수
Ro ≈ 1.0 입니다. 즉 40 Eri A 는 unsaturated rotation-activity
영역에 속합니다. 활성 영역은 자전 위상에 따라 가시 반구에 분포
하며, 그 결과 수 m/s 의 RV jitter 가 발생해 42 일 벌컨 신호로
오해되었습니다.

약간 sub-solar 한 금속도 ([Fe/H] = −0.29) 는 게임 내 일반 조명
해상도에서 가시 색상 변화로 잡히지 않지만, optical blue 영역에서
몇 percent 수준의 SED 차이를 만듭니다. 즉 solar-metallicity
K0.5 V 보다 미세하게 더 푸른 continuum 입니다. 그래뉼레이션
패턴은 K 왜성 특유의 작은 대류 셀 구조를 가집니다. 더 차가운
광구의 얕은 대류층과 일관적입니다.

## Atmosphere synthesis

40 Eri A 의 대기는 chromosphere–transition-region–corona 구조를
갖춘 적당히 조용한 K 왜성 대기입니다. 색층권 Ca II H&K 방출은
log R'HK = −4.99 (Jenkins 2011) 에 해당하며, unsaturated
rotation-activity 영역에서의 K 왜성 평균값과 일관적입니다. α Cen A
나 HK Cet B 의 Mt. Wilson 커버리지에 비할 만한 장기 log R'HK
시계열이 40 Eri A 에는 출간되어 있지 않습니다. 그래서 색층권
사이클이 (있다면) 미구속 상태입니다. Burrows 2024 의 42 일 자전
주기는 16 년 다기기 RV baseline 안에서 관측되었지만 십년 단위
사이클은 특성화되지 않았습니다.

ROSAT 전천 서베이 포인트에서 도출한 X-ray 광도는 대략 log L_X =
27.5 cgs (0.5–2 keV) 입니다. 40 Eri A 를 대상으로 한 XMM-Newton
이나 Chandra 장기 모니터링 캠페인 출간본은 없습니다. 거주 가능
영역에서의 통합 XUV 플럭스는 따라서 전형적인 K0.5 V quiet-state
스케일링으로 결정됩니다. solar-twin G 왜성보다 fractional Lbol
이 약간 더 높습니다. K 왜성이 광구 flux 단위당 더 강한 색층권
가열을 유지하기 때문입니다. 가상의 내측 행성에 대한 hydrodynamic
대기 손실은 (그런 행성이 존재했다면. HD 26965 b 는 존재 안 함)
중강도일 가능성이 큽니다. K 왜성 XUV 플라토가 G 왜성 대응 시기
보다 더 길게 saturated 상태에 머무르기 때문입니다.

벌컨 가짜 검출을 만들어낸 활성도 기반 RV 신호 자체가 대기 현상
입니다. Burrows 2024 는 그 기원을 starspot 변조와 대류
blueshift 억제가 42 일 자전 주기로 함께 사이클링하는 조합으로
규명합니다. depth-dependent line-by-line 상관관계는 지배적인
기여가 순수한 측광 spot 변조가 아니라 활성 영역의 granular
convective blueshift 억제에서 온다는 것을 시사합니다. 이는 G/K
태양형 별에서 잘 알려진 "granulation-driven RV jitter" 와 동일한
메커니즘이며, K 왜성 sub-photosphere 대류 깊이로 스케일된
버전입니다.

## Rotation & spin synthesis

Burrows 등 2024 의 자전 주기 ~42 일은 현대의 canonical 값입니다.
NEID line-by-line 활성도 상관관계를 16 년 다기기 RV baseline
(HIRES, PFS, CHIRON, HARPS, NEID) 에서 분석해 도출되었습니다.
Paper 는 P_rot 에 대한 formal uncertainty 를 명시적으로 quote 하지
않습니다. 표현은 "rotationally modulated activity signal at a
period of ∼42 days" 이며, 따라서 cfg 는 confidence=medium 으로
42 일 point value 를 채택합니다.

**Burrows 이전 자전 문헌은 일관되지 않습니다.** Saar & Osten 1997
의 ROSAT 상관 코로나 활성도 추정은 37.10 일을 제시합니다. Diaz
등 2018 의 HARPS S-index 페리어도그램은 "[42 일 RV 신호와 매우
가까운] 38 일에서 emerging peak" 를 봅니다. Mt. Wilson Ca II HK
모니터링 (Baliunas 등 1995 시대) 은 더 긴 자기 사이클 항을 빼고
난 후 42.3 일 부근에서 power 를 보고합니다. 37 일과 42 일 사이의
factor-of-1.1 spread 는 차등 자전을 반영할 수 있습니다 (위도별
자전 속도. NEID 활성도 신호가 옛 데이터셋과 다른 활성 위도대를
샘플링한다는 시나리오). 그러나 40 Eri A 에 대한 출간된 차등 자전
측정값은 그 긴장을 매듭짓지 못합니다.

cfg 목적에서는 42 일이 최근 다기기 anchor 이자 벌컨 반박 결과를
이끌어낸 동일한 주기입니다. Confidence 는 formal σ 부재와
37–42 일 pre-Burrows spread 때문에 medium 입니다.

**차등 자전과 inclination.** 어느 쪽도 40 Eri A 에 대해 직접
측정되지 않았습니다. 차등 자전은 태양보다 약하게 예상됩니다 (K
왜성 경향. 얕은 대류층 → 약한 차등 shear). 그러나 문헌은
ε Eri 같은 활성 K 왜성에 대한 Doppler-imaging 캠페인에 견줄 만한
40 Eri A 캠페인이 부재합니다. 자전축 inclination 도 미구속이라,
시각적 렌더링에서 NearStars 는 황도면 기준 약 30° 기울어진 축을
채택합니다. 무작위 방향 가정과 일관적입니다.

**K 왜성 braking 하에서의 spin-down 역사.** P_rot = 42 일에서
gyrochronological 나이 추정 (Barnes 2007 + Mamajek & Hillenbrand
2008 보정) 은 B−V ≈ 0.82 에 대해 대략 4–6 Gyr 입니다. Ma 2018
K 왜성 isochrone 의 6.9 ± 4.7 Gyr 과는 대체로 일관되지만 Bond
2017 IFMR 의 ~1.8 Gyr 과는 일치하지 않습니다. 이는 Decisions
테이블에서 flag 한 동일한 age divergence 의 부산물입니다.
gyrochronology 보정 자체가 이 노년 영역에서 불확실합니다. K 왜성
spin-down 이 긴 P_rot 에서 부분적으로 stall 하기 때문입니다 (van
Saders 등 2016 의 약화된 braking 가설). 따라서 gyrochronological
나이는 자체 systematic floor 를 가지고 긴장을 해결하지 못합니다.

## Visual styling

NearStars 렌더러는 40 Eridani A 를 따뜻한 크림빛 K0.5 V 별로
그립니다. 태양형 analog 와 시각적으로 구분이 되도록 약간 더
차분한 톤의 오렌지-크림으로 인코딩합니다 (`#ffd5a8`. 태양의
`#fff8f0` 이나 따뜻한 크림 α Cen A 의 `#fff4e8` 와 대비). 이
선택은 엄밀한 K 왜성 흑체 색에 대한 tie-break 입니다. 5143 K
의 흑체 chromaticity 는 `#ffe2b6` 에 더 가깝지만, cfg 픽은 게임
내 별 팔레트의 시각 변별력을 위해 살짝 더 오렌지 쪽으로 밀어
넣습니다. K 왜성은 local-volume 인구의 dominant 부류이고,
단일 "K 왜성 따뜻한 크림" 톤으로 통일하면 시각적 단조로움이
생길 위험이 있어서입니다.

5.01 pc 거리에서 본 겉보기 등급 V = 4.43 은 40 Eridani A 를
에리다누스 자리의 육안 별로 만듭니다 (전통 이름 케이드. 아랍어
*al-qaid* "깨진 껍데기" 에서 유래). 별자리 남쪽 윤곽에 있으며,
리겔에서 남서쪽으로 약 16° 떨어진 위치에 자리합니다.

A 주위의 가상의 가까운 행성에서 보면, 동반성 B-C 쌍은 각분리
~83″ 의 unresolved 이중 점광원으로 나타납니다. A 의 거주 가능
영역에서는 쉽게 하나의 육안 천체로 보이는 정도입니다 (각분리는
0.65 AU HZ 내측 가장자리에서 약 30 arc-minutes 로, 지구에서 보는
보름달과 비슷합니다). B-C 쌍 자체는 230 년 주기로 상호 공전하는
K 왜성 질량 WD + M 왜성 binary 입니다. periastron 에서 B-C
분리는 ~26 AU 까지 줄어들고 C 의 방출에 대한 B 의 반사 밝기가
검출 가능해지지만, ~8000 년의 A-BC 궤도 시간 척도에서는 cfg
게임 내 epoch 동안 분리각이 기하학적으로 고정된 것으로 다룹니다.

**HD 26965 b 는 documented divergence 로 포함합니다.** 벌컨 후보는
Burrows 2024 로 반박됐지만(아래), 프로젝트는 문화적 무게(Star Trek 의
Vulcan, *Project Hail Mary* 의 Erid)를 고려해 철회 이전 Ma 2018 값
(M sin i ≈ 8.5 M⊕, P ≈ 42.2 d, a ≈ 0.224 AU)으로 이 행성을 유지하기로
했습니다. canonical 판독은 "행성 없음"이고 42 일 신호는 별의 자전입니다.
그래서 아래 Refutation 섹션이 검출과 반박을 문서화하며, 이 천체는 refuted
disposition 을 답니다. cfg 는 항성 삼중성계에 이 문화적·반박표기 천체를
더해 렌더링합니다.

## Canonical alternatives

Age 는 이번 합성에서 유일한 documented divergence 입니다. cfg 는
WD-progenitor IFMR 의 Bond 2017 ~1.8 Gyr 을 채택합니다. K 왜성
단독 문헌만 보는 canonical reading 이라면 대신 Ma 2018 K 왜성
isochrone 을 채택했을 것입니다.

| Field | cfg value (Bond 2017 IFMR) | Canonical alternative (Ma 2018 K 왜성 isochrone) | cfg 가 다르게 픽한 이유 |
|---|---|---|---|
| `age_gyr` | ~1.8 (40 Eri B WD progenitor 분석에서 도출한 시스템 공통 나이) | 6.9 ± 4.7 (K 왜성 SED + PARSEC isochrone) | IFMR 기반 시스템 공통값은 K 왜성 isochrone systematic 과 무관한 물리적 종점 (WD progenitor 수명 + 냉각 트랙) 으로 나이를 anchor 합니다. Ma 2018 대안은 Gyr 스케일에서 나이가 잘 제약되지 않는 K 왜성 isochrone 분지에서 60+% 상대 불확실도를 가집니다. Bond 2017 §6.2 는 "수정된 WD 질량으로 excessive age 우려가 해소된 것으로 보인다" 고 명시적으로 적습니다. Gyrochronological cross-check (P_rot 42 d → Barnes 2007 기반 4–6 Gyr) 는 Ma 2018 에 더 가깝지만 노년에서 van Saders 2016 의 weakened-braking systematic 에 노출되어 긴장을 해결하지 못합니다. cfg 는 물리적으로 더 강하게 anchor 된 Bond reading 을 따릅니다. |

Ma 2018 isochrone 나이는 Phase 2 DB 의 `age_measurements` 안에서
`recommended:true` 로 남아 있습니다. A 자체의 유일한 직접 항성-
나이 측정값이기 때문입니다. Bond 2017 은 method `isochrone` 로
`recommended:false` 기록입니다 (IFMR progenitor 수명을 isochrone-
equivalent 제약으로 취급). Phase 2 권장값과 Phase 3 cfg 픽의 이
divergence 가 이 `## Canonical alternatives` 섹션의 존재 이유
입니다.

## Refuted planet — HD 26965 b ("Vulcan")

40 Eridani A 는 대중문화에서 스타 트렉의 스폭 모행성 벌컨의
호스트 별로 유명합니다. Gene Roddenberry 와 Sallie Baliunas 의
1991 년 편지가 이 식별을 공식 확인했습니다. Ma 등 2018 이 발표한
RV 검출 슈퍼지구 후보 — P = 42.4 d, M sin i ≈ 8.5 M⊕, a ≈
0.224 AU — 는 따라서 2010 년대 가장 문화적으로 주목받은 외계행성
검출 중 하나가 되었습니다.

**HD 26965 b 는 현재 Refuted 로 분류됩니다 (Burrows 등 2024,
AJ 167, 243).** Burrows 2024 의 NEID 정밀 도플러 캠페인이 16 년
간의 HIRES + PFS + CHIRON + HARPS 데이터 재분석과 결합되어, 42 일
RV 신호가 별의 자전 주기 (∼42 d) 와 동일한 신호임을 입증했습니다.
세 가닥의 증거는 다음과 같습니다. (1) bulk RV 와 classical
활성도 지표의 cross-correlation 이 multi-day lag 를 보이는데, 이는
케플러 궤도가 아닌 자전 변조와 일관적입니다. (2) line-by-line
RV 분석에서 활성 영역 가시도에 따라 변하는 convective-blueshift
suppression 을 시사하는 depth-dependent 상관이 나타납니다. (3)
활성도 지표 시계열에 대한 선형 detrending 이 RV 분산의 대부분을
제거합니다. 종합 증거는 "spot 과 convective blueshift 억제의
조합으로 가설을 세우는 ~42 일 자전 변조 활성도 신호가 RV 신호의
지배 요인" 이라는 결론과 일관적입니다 (Burrows 2024 abstract).

**Disposition: `db/planets_curated.json` 에 등재하지 않음.** Ma
2018 후보로부터 KSP 행성을 만들지 않습니다. NASA Exoplanet
Archive `ps` 테이블도 Burrows 기반 삭제 이후 HD 26965 에 대해
0 row 를 반환합니다. 2025 년이나 2026 년의 follow-up 논문이
대체 후보를 제시한 사례는 없습니다. "HD 26965 planet 2024-2026"
문헌 검색은 Burrows 반박과 그 후속 뉴스 요약만 surfacing
합니다.

이 refutation 노트는 별도의 `docs/phase3/40-eridani-a-b.md`
파일 대신 Phase 3 markdown 안에 보존됩니다. (a) A 에 큐레이션된
행성이 없고 (b) 문화적 cross-reference 가 호스트-별 합성에
자연스럽게 들어가기 때문입니다. 가장 가까운 선례는 tau Cet e
refuted Phase 3 markdown (`tau-cet-e.md`) 으로, 발견 기록을
반박과 함께 보존하는 패턴입니다. 40 Eri A b 는 비슷한 기준을
따르되, Ma 2018 picture 의 역사적 Phase 3 가 존재하지 않으므로
파일 단위가 아닌 섹션 단위로 처리합니다.

## Bibliography

### Read (Decisions 를 이끈 문헌)

- **Boyajian T. S. 등 2012** — *Stellar Diameters and
  Temperatures II. Main-Sequence K- and M-Stars*, ApJ 757, 112
  (`2012ApJ...757..112B`, doi:10.1088/0004-637X/757/2/112). 40
  Eri A 가 GJ 166 A 로 포함된 CHARA Classic H 밴드 간섭계 각지름
  샘플. θ_LD = 1.504 ± 0.006 mas (Table 3); R = 0.8061 ± 0.0036
  R☉, Teff = 5143 ± 14 K, L = 0.4078 ± 0.0032 L☉ (Table 6). 두
  간섭계 측정 중 fractional uncertainty 가 더 작아 권장 Phase 2
  primary 로 R/Teff/L 을 anchor 합니다.
- **Rains A. D. 등 2020** — *Precision angular diameters for 16
  southern stars with VLTI/PIONIER*, MNRAS 493, 2377
  (`2020MNRAS.493.2377R`, doi:10.1093/mnras/staa282,
  arXiv:2004.02343). VLTI/PIONIER 4 망원경 H 밴드 간섭계. 40
  Eri A 는 Table 1 샘플의 16 개 중 7 번째. 독립적 cross-check:
  θ_LD = 1.486 ± 0.012 mas, R = 0.804 ± 0.006 R☉, Teff = 5126
  ± 30 K, L = 0.40 ± 0.01 L☉ (Table 4). 네 가지 값 모두에 대해
  Boyajian 2012 와 1σ 안에서 일치합니다.
- **Ma B. 등 2018** — *Very low-mass stellar and substellar
  companions to solar-like stars from MARVELS VI. A giant planet
  and a brown dwarf candidate in a close binary system HD 87646*
  는 같은 저자들의 관련 연구입니다. 40 Eri A 에 대한 본
  논문은 **Ma 등 2018 MNRAS 480, 2411**
  (`2018MNRAS.480.2411M`, doi:10.1093/mnras/sty1933) 으로 Dharma
  Planet Survey 의 HD 26965 b RV 검출을 보고합니다. Mass
  0.78 ± 0.08 M☉, age 6.9 ± 4.7 Gyr (PARSEC isochrone +
  다중 밴드 SED), Teff 5072 ± 53 K, [Fe/H] −0.42 ± 0.04
  (Table 2). 질량과 (대안) 나이/금속도의 Phase 2 anchor 인 동시에
  지금은 반박된 행성 후보의 source paper 이기도 합니다.
- **Bond H. E. 등 2017** — *Astrophysical Implications of a
  New Dynamical Mass for the Nearby White Dwarf 40 Eridani B*,
  ApJ 848, 16 (`2017ApJ...848...16B`, doi:10.3847/1538-4357/aa8a63,
  arXiv:1709.00478). 40 Eri B 의 HST FGS 동역학 질량 0.573 ±
  0.018 M☉; §6.2 가 IFMR (initial mass ~1.8 M☉ → MS 수명
  1.7 Gyr + 냉각 122 Myr) 로 시스템 공통 나이 ~1.8 Gyr 을
  유도합니다. Phase 3 cfg 가 Ma 2018 보다 이 값을 채택합니다 —
  `## Canonical alternatives` 참조.
- **Burrows A. 등 2024** — *The Death of Vulcan: NEID Reveals
  That the Planet Candidate Orbiting HD 26965 Is Stellar Activity*,
  AJ 167, 243 (`2024AJ....167..243B`, doi:10.3847/1538-3881/ad34d5,
  arXiv:2404.17494). NEID line-by-line RV + 활성도 지표 상관이
  Ma 2018 벌컨 후보를 반박합니다. 자전 주기는 formal σ 없이
  "∼42 days" 로 보고됩니다. `rotation_period_days` Decisions
  row 와 Refuted-planet 섹션의 source.
- **Diaz M. R. 등 2018** — *The Test Case of HD 26965:
  Difficulties Disentangling Weak Doppler Signals from Stellar
  Activity*, AJ 155, 126 (`2018AJ....155..126D`,
  doi:10.3847/1538-3881/aaa896, arXiv:1801.03970). HARPS 데이터로
  본 벌컨 신호의 pre-Burrows 검토. 활성도 대 행성 모호성을
  미리 짚어둔 paper. SPECIES atmospheric pipeline 으로부터의
  Phase 2 대안 mass (0.76 ± 0.03 M☉), Teff (5151 ± 55 K),
  [Fe/H] (−0.29 ± 0.12), age (9.23 ± 4.84 Gyr) (Table 1). Saar &
  Osten 1997 의 ~37 일 P_rot 과 HARPS S-index 의 ~38 일 peak
  를 언급합니다.
- **Jenkins J. S. 등 2011** — *Chromospheric activities and
  kinematics for solar type dwarfs and subgiants: analysis of the
  activity distribution and the AVR*, A&A 531, A8
  (`2011A&A...531A...8J`, doi:10.1051/0004-6361/201016333). HARPS
  로 본 890 개 남쪽 FGK 별의 Ca II H&K 서베이. Phase 2 권장
  log R'HK = −4.99 의 source (이번 세션에서 CDS 표 row 단위
  직접 fetch 는 못함, Open items 참조).

### Read (K 왜성 파라미터 셋 + binary architecture 의 context)

- **Pourbaix D. & Boffin H. M. J. 2016** — α Centauri AB 의
  visual-spectroscopic binary 질량. 동일 기법이 역사적으로 40
  Eri AB 에도 적용되었지만 mutual 궤도가 너무 길어 케플러 적합이
  불가능하다는 점에서 인용합니다 (40 Eri A-BC ~8000 년).
- **Mason B. D., Hartkopf W. I. & Miles K. N. 2017** — *Binary
  Star Orbits. V. The Nearby White Dwarf-Red Dwarf Pair 40 Eri BC*,
  AJ 154, 200 (`2017AJ....154..200M`,
  doi:10.3847/1538-3881/aa803e). 내측 B-C 쌍의 grade-1 결정 궤도:
  P = 230.30 ± 0.68 yr, e = 0.4294 ± 0.0027. `db/binary_orbits.json`
  의 B-C 궤도 Phase 2 anchor.
- **Henry T. J. 등 1996** — *A Survey of Ca II H and K
  Chromospheric Emission in Southern Solar-Type Stars*, AJ 111,
  439 (`1996AJ....111..439H`, doi:10.1086/117796). 40 Eri A 를
  포함한 더 이른 색층권 활성도 서베이. Phase 2 대안 log R'HK
  = −4.94. 직접 CDS row 는 이번 세션에서 table-verify 못함;
  bibcode/title 은 확인됨.
- **Bensby T., Feltzing S. 등 2014** — *Exploring the Milky
  Way stellar disk*, A&A 562, A71 (`2014A&A...562A..71B`,
  doi:10.1051/0004-6361/201322631). thin/thick-disk 화학 abundance
  서베이의 714 F/G 왜성. 40 Eri A 에 대한 Phase 2 대안
  [Fe/H] = −0.31 ± 0.10. K0.5 V 분류는 sample boundary 에
  있음; bibcode/title 은 확인되었으나 row-level Table A1 은
  이번 세션에서 직접 fetch 안 함.
- **Tokovinin A. 2018** — *MSC — Catalogue of physical multiple
  stars* (2018 업데이트). 40 Eri A-BC 외측 궤도가 케플러 해
  없음으로 등재 (투영 a ~ 400 AU, P ~ 8000 yr). A 를 resolved
  binary 파트너가 아닌 독립 항성으로 다루는 cfg 결정의 anchor
  입니다.
- **Saar S. H. & Osten R. A. 1997** — *Lithium, X-ray activity,
  and rotation in an HR diagram of solar-type field stars*,
  MNRAS 284, 803. ROSAT 상관 코로나 활성도로부터 40 Eri A
  P_rot ≈ 37.10 일 보고. pre-Burrows 자전 alternative 로 인용 —
  Open items 참조.

### Read (instrument-only / methodological 참고)

- **Torres G., Andersen J. & Giménez A. 2010** — Ma 2018 의 질량
  계산 기반이 되는 경험적 mass-radius 관계.
- **Bressan A. 등 2012** + **PARSEC tracks** — Ma 2018 의
  isochrone 나이 계산 기반이 되는 항성 진화 트랙.
- **Soto M. G. & Jenkins J. S. 2018** — Diaz 2018 이 파라미터
  유도에 사용한 SPECIES atmospheric 파이프라인.

### Not read — superseded 또는 low-priority

2010 년 이전의 K 왜성 isochrone 서베이 (Valenti & Fischer 2005
SPOCS, Holmberg 등 2009 Geneva-Copenhagen); 40 Eri A 항목이 없는
일반 nearest-50-pc K 왜성 자전 서베이; Burrows 2024 NEID
baseline 에 의해 superseded 된 Mt. Wilson HK 플레이트-아카이브
논문들. pre-Burrows 시기 40 Eri A 를 대상으로 한 SETI / 외계행성
탐색 제안 논문들 (Ma 2018 follow-up 제안 포함). 이들은 bib
YAML 이 빌드되면 `status: skipped` 로 필터됩니다.

## Stellar wind / astrosphere

40 Eri A 는 빠르게 움직이는 K 왜성입니다 (국부 ISM 대비 V_ISM ≈
127 km/s). 따라서 ram pressure 가 astrosphere 를 강하게 압축할
테지만, 항성풍 Ṁ 이 **미측정** 이라 (Wood 의 HST Lyα 탐색에서 40
Eri 는 검출 가능한 astrosphere 가 없음) standoff 거리는 미구속
상태로 둡니다. 잘 정립된 **8.7 년 Ca II 활성도 사이클** 을 가집니다
(Laliotis 2023. 역사적으로는 ~10 년, Baliunas 1995). 적당히
활동적인 노년 K 왜성으로서 입자 환경은 태양보다 약간 아래입니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | 8.70 | high | Laliotis 2023 S-index (역사적으로 ~10.1 yr, Baliunas 1995) |
| `stellar_wind_mass_loss_solar` | (unconstrained) | — | Wood 샘플에 없음. 검출 가능한 astrosphere 없음 |
| `local_ism_inflow_speed_kms` | ~127 | medium | 6D 측성 대 LIC (높은 우주 속도) |
| `astrosphere_standoff_au` | (unconstrained) | — | 항성풍 측정이 필요 (Ṁ 미상) |
| `stellar_radiation_surface_relative_sun` | ~0.8 | low | 적당히 활동적인 노년 K — interesting-first, 태양 부근 |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~281 / −41 | low | 6D 측성 대 LIC. **plugin-only** |

## Open items for follow-up

- **Jenkins 2011 + Henry 1996 row-level log R'HK 검증.**
  색층권 활성도 값 −4.99 (Jenkins) 와 −4.94 (Henry) 는 2026-05-27
  prep notes 에서 이월된 값입니다. 이번 세션에서는 HD 26965 에
  대한 CDS table row 를 직접 fetch 하지 못했습니다. 향후
  큐레이션 패스에서 Jenkins 2011 의 CDS Table 4 (전체 표) 와
  Henry 1996 의 동등 표에 대해 row 단위로 재검증해야 합니다.
  두 값 모두 downstream paper 에서 광범위하게 quote 되고
  있고 정확할 가능성이 크지만 paper-Table 수준의 확인이
  필요합니다.
- **Bensby 2014 row-level [Fe/H] 검증.** 위와 동일한 caveat:
  −0.31 ± 0.10 값은 prep notes 출처이며, HD 26965 의 Table A1
  row 는 이번 세션에서 직접 fetch 하지 못했습니다.
- **Burrows 2024 자전 주기 불확실도.** Paper 는 formal σ 없이
  "∼42 days" 로만 보고합니다. pre-Burrows 의 37 일 Saar & Osten
  reading 과 38 일 Diaz 2018 HARPS S-index reading 은 표면적
  으로 42 일과 일관적이지 않습니다. Gaussian process 기반 RV +
  광도곡선 joint 분석 (Aigrain 2015 프레임워크나 Damasso 2020
  Proxima 방법론과 비슷한 접근) 이라면 42 일 신호가 실제 표면
  자전 주기인지, 아니면 차등 자전 기반 활성대의 더 오래 사는
  signature 인지를 매듭지을 수 있습니다.
- **Asteroseismology 로 age divergence 해결.** Ma 2018 의 ~7
  Gyr 대 Bond 2017 의 ~1.8 Gyr 나이의 fundamental cross-check
  는 40 Eri A 에서 p-mode 진동의 asteroseismic 검출을 요구
  합니다. K0.5 V 분광형은 ν_max 를 ~4000 µHz 근처에 두는데,
  이는 현재 정밀 RV 시계열 capability 의 가장자리에 있습니다.
  그러나 Bouchy & Carrier 2001 / de Meulenaer 2010 (α Cen A)
  에 견줄 만한 NEID 또는 ESPRESSO 다중-야간 전용 캠페인이라면
  결정적일 것입니다.
- **40 Eri A X-ray 사이클 특성화.** A 에 대한 장기 baseline 의
  XMM-Newton 이나 Chandra 모니터링 캠페인이 출간되지 않았습니다.
  활성도 log R'HK = −4.99 와 P_rot 42 일은 태양형 사이클의
  존재 가능성을 시사하지만 미구속 상태입니다. 전용 사이클 탐색
  (α Cen A 의 Robrade 2016 와 동일한 템플릿) 은 활성-사이클
  시각 렌더링에 cfg-decisive 입니다.
- **A-BC 외측 궤도 적합.** ~8000 년 궤도는 현재 미적합 상태
  (Tokovinin MSC 2018) 입니다. 십수년 단위의 Gaia 측성 모니터링
  이 결국 A-BC 파라미터를 좁힐 것입니다. 적합되면
  `db/binary_orbits.json` 에 A-BC entry 가 추가되고, 위
  Phase 3 visual styling 섹션의 "B-C 쌍이 ~83″ 떨어진 한 점
  광원" 진술은 시간 변동값이 됩니다.

## Related

- [40-eridani-b](40-eridani-b.md) — DA2.9 백색왜성 동반성. 위에서
  문서화된 시스템 나이 divergence 의 anchor 가 Bond 2017 IFMR
  입니다.
- [40-eridani-c](40-eridani-c.md) — M4.5 Ve 플레어 스타 (DY Eri).
  B 와 230 년 주기로 페어를 이룹니다.
- [tau-cet-e](tau-cet-e.md) — sibling refuted-planet Phase 3
  markdown. 위의 Refuted planet 섹션의 구조적 선례.
- [methodology](../reference/methodology.md) — Phase 2/3 schema
- [rex-data-comparison](../reference/rex-data-comparison.md) — 40
  Eri B 반박 비교 (rex 는 HD 26965 b 를 carry 했지만 NearStars
  는 올바르게 제외함)
