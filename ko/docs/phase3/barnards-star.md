<!-- 바너드 별 Phase 3 합성. cfg-ready 결정과 근거 -->
# Barnard's Star — Phase 3 Synthesis

바너드 별 (GJ 699, HIP 87937, V2500 Oph) 은 1.83 pc 거리의 M4.0 Ve
적색왜성으로, 태양에 가장 가까운 단독성입니다 (더 가까운 건 α
Centauri 삼중성뿐입니다). 또한 하늘의 어떤 천체보다 고유운동이 큰
별로, μ ≈ 10.3 arcsec/yr (Barnard 1916) 에 이릅니다. 이 속도라면
하늘에서 보름달 지름 하나를 가로지르는 데 약 175 년이 걸립니다.
나이가 많고 금속이 빈약한 중간 종족 II / 고속도 원반 별이며 (태양
기준 공간속도 ~140 km/s), 그에 걸맞게 알려진 M 왜성 중 자기적으로
가장 조용한 축에 듭니다. 색채권 지수 log R'HK = −5.82 (Toledo-Padrón
et al. 2019) 는 M 왜성 활동도의 바닥 근처에 자리하며, M 왜성 census
를 지배하는 활동적인 flare star 들보다 한 자릿수 낮습니다.

기본 파라미터는 frozen Phase 2 레이어에서 가져옵니다. 질량
M = 0.162 ± 0.007 M☉ 와 광도 L = 0.003558 ± 0.000072 L☉ 는 둘 다
Schweitzer et al. 2019 (CARMENES) 에서 왔고, 반지름 R = 0.187 ±
0.001 R☉ 도 마찬가지입니다. 이 반지름은 **기원이 간섭계** 입니다.
Boyajian et al. 2012b 가 CHARA 어레이로 사지 어두워짐을 보정한
각지름 θ_LD = 0.952 mas 를 측정했고, Schweitzer 2019 가 그 θ_LD 를
Gaia DR2 거리와 결합해 R = 0.187 R☉ 를 다시 계산했습니다. 유효온도
Teff = 3195 ± 28 K 는 González Hernández et al. 2024 (ESPRESSO
master spectrum, SteParSyn) 에서 온 가장 최근의 고분해능 측정이자
Phase 2 recommended 값이며, 분광 분석 간 ~80 K 폭의 차가운 쪽 끝에
자리합니다 (Canonical alternatives 참조). 금속도는 태양 아래로
[Fe/H] = −0.39 ± 0.03 (Jahandar et al. 2023, SPIRou 근적외선) 가
recommended 값입니다 — 다만 기기 간 금속도 편차가 크고 (~0.4 dex),
이것이 이 합성의 두 번째 documented divergence 입니다.

NearStars 에서 바너드 별을 규정하는 건 극적임이 아니라 극단적인
정적 상태와 노령입니다. 나이는 ~8.5 ± 1.5 Gyr (Ribas et al. 2018,
운동학) 로, 두꺼운 원반 / 헤일로를 스치는 운동학에서 추론되는 더
넓은 7–10 Gyr 범위와 일관됩니다. 카탈로그에서 가장 늙은 별 중
하나입니다. 자전 주기는 매우 길어 P_rot = 145 ± 15 d (Toledo-Padrón
et al. 2019, 광도 측정) 인데, 이는 수 Gyr 의 자기 braking 이 별을
거의 완전히 spin down 시킨 결과입니다 (v sin i 는 측정 불가능할
만큼 작아, R 과 P 로부터 ~0.07 km/s 가 함의됩니다). 같은 모니터링
캠페인은 ~10 yr 규모의 장기 활동 사이클도 보고합니다 — 그밖에는
활동도 바닥 근처인 색채권 위에 얹힌 느리고 태양 같은 사이클
변조입니다. 정적임에도 이 별은 드물게 flare 를 냅니다. 2019 년에
강한 원자외선 flare 가 포착됐는데 (HST), 이렇게 비활동적이고 늙은 M
왜성조차 간헐적 flare 코로나를 유지함을 확인해 줍니다.

바너드 별은 **확정된 sub-Earth 네 개로 이루어진 조밀한 시스템** 을
거느립니다. "Barnard b" (P ≈ 3.15 d, M sin i ≈ 0.30 M⊕) 와 형제
행성 c·d·e (P ≈ 4.12, 2.34, 6.74 d. M sin i 0.19–0.34 M⊕) 로, 모두
거주 가능 영역 훨씬 안쪽의 암석질 sub-Earth 입니다. ESPRESSO 캠페인이
검출했고 (González Hernández et al. 2024), Basant et al. 2025 가
독립적인 MAROON-X 데이터로 확정하며 후보였던 c·d·e 를 정식 행성으로
승격시켰습니다. (앞선 Ribas et al. 2018 의 "Barnard b" super-Earth,
P ≈ 233 d 는 이후 철회됐고 — Lubin et al. 2021 — 같은 천체가
아닙니다.) 각각은 개별 Phase 3 합성 (`barnards-star-b/c/d/e`) 에서
다룹니다.

**NearStars 시나리오 선택. 고대의, 깊은 붉은빛의, 극단적으로 조용한
M4 V 왜성으로 — 가장 가까운 단독성 — 145 일 주기로 느리게 자전하며
희미한 ~10 yr 활동 사이클과 드문 flare 만 있는 모습으로 렌더링
합니다.** 항성 레이어는 frozen Phase 2 출처 (Schweitzer 2019 의
질량/반지름/광도, González Hernández 2024 의 Teff, Jahandar 2023 의
금속도, Toledo-Padrón 2019 의 자전/활동, Ribas 2018 의 나이, Boyajian
2012b 의 간섭계 각지름) 위에 정박합니다. 두 파라미터가 문헌에 걸쳐
documented divergence 를 안고 있는데 — 금속도 (~0.4 dex 폭) 와 Teff
(~80 K 폭) — `## Canonical alternatives` 에서 다룹니다. tie-break
하나가 M4 V SED 의 시각 표면 색조를 정합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.0 Ve | high | Phase 2 DB spectype. "e" 는 별이 지금은 극단적으로 조용한데도 붙은 역사적 Hα-방출/flare 표기 (변광성 이름 V2500 Oph) |
| `mass_msun` | 0.162 ± 0.007 | high | Schweitzer et al. 2019 — CARMENES spectroscopic_calibration (Phase 2 recommended). Mann et al. 2015 의 M_K 경험 관계는 0.161 ± 0.006 로 1σ 안에서 일치 |
| `radius_rsun` | 0.187 ± 0.001 | high | Schweitzer et al. 2019 — 간섭계. Boyajian 2012b 의 사지 어두워짐 보정 θ_LD = 0.952 mas (CHARA) 를 Gaia DR2 거리와 결합 (Phase 2 recommended) |
| `teff_k` | 3195 ± 28 | high | González Hernández et al. 2024 — ESPRESSO master spectrum, SteParSyn (Phase 2 recommended). Documented divergence. Jahandar/Marfil/Schweitzer 와 ~80 K 폭 — Canonical alternatives 참조 |
| `luminosity_lsun` | 0.003558 ± 0.000072 | high | Schweitzer et al. 2019 — bolometric flux (Phase 2 recommended). 태양 광도의 약 1/280 |
| `metallicity_fe_h_dex` | −0.39 ± 0.03 | medium | Jahandar et al. 2023 — SPIRou 근적외선 분광 (Phase 2 recommended). DOCUMENTED DIVERGENCE. Schweitzer 2019 VIS (−0.15) 및 Marfil 2021 (−0.57) 과 ~0.4 dex 폭 — Canonical alternatives 참조 |
| `age_gyr` | 8.5 ± 1.5 | medium | Ribas et al. 2018 — 두꺼운 원반 / 고속도 멤버십에서 구한 운동학 나이 (Phase 2 recommended). 중간 종족 II 원반 별의 더 넓은 7–10 Gyr 범위와 일관 |
| `rotation_period_days` | 145 ± 15 | high | Toledo-Padrón et al. 2019 — 광도 자전 변조. 긴 주기는 수 Gyr 의 자기 braking 을 반영 |
| `activity_log_rhk` | −5.82 ± 0.08 | high | Toledo-Padrón et al. 2019 — Ca II H&K 색채권 지수. M 왜성 활동도 바닥 근처로, 알려진 가장 조용한 M 왜성 중 하나 |
| `activity_cycle_years` | ~10 | medium | Toledo-Padrón et al. 2019 — 활동 지수 시계열의 장기 사이클 변조. ~10 yr 규모, 성격이 태양 같음 |
| `v_sin_i_km_s` | ~0.07 | low | R = 0.187 R☉ 과 P_rot = 145 d 에서 유도 (적도 속도 ~0.065 km/s). 어떤 분광 v sin i 측정의 분해능보다도 낮음 — 선폭 측면에서 사실상 비자전체 |
| `visual_surface_tint_hex_primary` | `#cf5a30` (M4 V 의 깊은 주황-빨강) | medium | Tie-break. 3195 K 흑체 + TiO/VO 분자 밴드 억제. M1V AU Mic `#e0743a` 보다 붉고 (Teff 가 ~470 K 더 뜨거움), M5.5 Proxima `#c54c2a` 보다 살짝 따뜻함 (Teff 가 ~145 K 더 차가움) |
| `stellar_color_temp_k` | 3195 | high | Teff 유도 (González Hernández 2024) |
| `apparent_magnitude_v_from_earth` | 9.51 | high | Hipparcos / 표준 측광. 1.83 pc 근접에도 맨눈 가시성에 한참 못 미침. 광도가 낮기 때문 (M_V ≈ 13.2) |
| `proper_motion_arcsec_per_yr` | 10.36 | high | Barnard 1916 / Gaia. 알려진 별 중 고유운동이 가장 큼 ("바너드의 폭주성") |

## Surface synthesis

바너드 별은 카탈로그에서 가장 깊은 붉은 광구 중 하나를 가집니다.
Teff = 3195 K (González Hernández 2024) 에서 SED 는 근적외선
~0.91 μm 깊숙이에서 정점을 이루며, 광학 연속체는 ~0.7 μm 아래에서
TiO 와 VO 분자 밴드에 크게 억제되고 NIR 에서는 물 밴드에 의해
빚어집니다. R = 0.187 R☉ (Schweitzer 2019, 간섭계) 에서 광도는
겨우 0.003558 L☉ — 태양의 약 1/280 — 이라, 가장 가까운 단독성임에도
본질적으로 어둡습니다. 지구에서는 V ≈ 9.5 로만 빛나 맨눈에 보이지
않습니다.

어린 M 왜성의 부푼 전주계열 반지름과 달리, 여기 0.187 R☉ 는 수 Gyr
나이의 ~0.16 M☉ 별에 대한 완전히 정착된 주계열 반지름이며, 간섭계
정박 (Boyajian 2012b θ_LD = 0.952 mas, CHARA 어레이로 직접 측정한
사지 어두워짐 보정 지름) 덕에 잘 결정된 M 왜성 반지름 축에 듭니다.
태양 아래 금속도 [Fe/H] = −0.39 (Jahandar 2023) 는 태양형 금속도
M4 V 대비 분자 밴드 line blanketing 을 살짝 줄여 SED 를 미세하게
파란 쪽으로 밀지만, 이는 게임 내 조명 색의 분광 분해능에서는 보이지
않으며 채택한 색조를 약하게만 정당화합니다.

표면의 결정적 특성은 활동이 아니라 **정적 상태** 입니다.
log R'HK = −5.82 (Toledo-Padrón 2019) 로 바너드 별은 M 왜성 색채권
활동도의 경험적 바닥 근처에 자리합니다 — 흑점 면적이 작고 광도
자전 진폭도 작은데, 바로 그 때문에 145 일 자전 주기를 분해하려면
전용 장기 모니터링 캠페인이 필요했습니다. cfg 렌더링에서는 이것이
거의 균일한 붉은 디스크에 희미하고 느리게 떠도는 흑점 피처만 있는
모습을 뜻하며, 카탈로그의 다른 곳에 있는 흑점 면적이 큰 활동적 M
왜성 (AU Mic, Proxima) 과 의도적으로 대비됩니다. Granulation 은
M-왜성 전형으로, 얕은 광구 압력 스케일 높이가 정하는 작은 대류
셀을 가집니다.

## Atmosphere synthesis

바너드 별의 외곽 대기는 극단적인 정적 상태에 지배됩니다. 색채권
Ca II H&K 지수 log R'HK = −5.82 (Toledo-Padrón 2019) 는 이 별을
지금껏 측정된 가장 비활동적인 M 왜성 축에 놓습니다 — 포화된 어린
flare star 보다 대략 한 자릿수 낮고, field-M-왜성 중앙값보다도
낮습니다. 145 일 자전 주기와 그로 인한 매우 큰 Rossby number 는
별을 비포화, 자기 braking 된 영역 깊숙이 놓는데, 거기서는 활동도가
자전에 가파르게 비례합니다. 느린 자전이 약한 dynamo 작용을 낳고,
약한 dynamo 가 조용한 코로나와 색채권을 낳습니다.

그럼에도 Toledo-Padrón 2019 캠페인은 색채권 지수 시계열에서
**~10 yr 규모의 장기 활동 사이클** 을 분해했습니다 — 그밖에는
바닥 수준인 활동도 위에 올라탄 느리고 태양 같은 사이클 변조입니다.
이것이 cfg `activity_cycle_years` 정박값이며, 렌더링에서는 극적인
폭발을 구동하는 대신 (이미 희미한) 흑점 패턴과 색채권 방출을 수십 년
시간 척도에서 변조합니다.

정적이라고 무력한 건 아닙니다. 2019 년 바너드 별에서 강한 원자외선
**flare** 가 포착됐는데 (HST 관측), 8–10 Gyr 나이의 바닥-활동도 M
왜성조차 상당한 일시적 XUV 출력이 가능한 간헐적 flare 코로나를
유지함을 보여 줍니다. cfg 측면에서 flare 는 드문 사건의 박자
찍기일 뿐이며 — AU Mic 의 거의 연속적인 flare 와는 다릅니다 — 정적
XUV 배경은 낮습니다. 가까운 sub-Earth 행성 후보들에 대한 함의는,
시간 평균 고에너지 조사량이 활동적 M 왜성 주위보다 훨씬 부드럽다는
것이지만, 드문 flare 와 후보 궤도의 근접성 (P ≈ 3 d) 은 그래도 별의
긴 수명에 걸쳐 무시할 수 없는 누적 XUV 선량을 부과합니다.

## Rotation & spin synthesis

145 일 자전 주기 (Toledo-Padrón 2019, 광도 변조) 는 M 왜성
카탈로그에서 가장 긴 축에 들며 나이의 직접적 지문입니다. ~8.5 Gyr
수명 동안 바너드 별은 자기 (Skumanich 식) braking 으로 초기 각운동량
거의 전부를 잃었고, 추정컨대 빨랐던 zero-age-main-sequence 자전에서
현재의 거의 정지에 가까운 상태로 spin down 했습니다. 함의되는 적도
속도는 겨우 ~0.065 km/s 라, v sin i 는 어떤 분광 선폭 분석의 검출
임계값보다도 한참 아래입니다 — cfg 는 이를 측정값이 아니라 순수
유도량으로서 low confidence 의 ~0.07 km/s 로 기록합니다.

이 느린 자전이 별의 정적 상태의 엔진입니다. M 왜성의 자전-활동
관계는 이 Rossby number 에서 관측된 바닥 수준 log R'HK = −5.82 를
정확히 예측합니다. 십 년 단위 활동 사이클 (~10 yr, Toledo-Padrón
2019) 이 유일한 유의한 시간 변화입니다. 렌더링할 빠른 자전 신호는
없고, 흑점 면적이 작아 자전 주기에서의 광도 변조도 저진폭입니다.

Asteroseismic 제약은 불가능합니다 — 바너드 별은 너무 차갑고 너무
작아 검출 가능한 p-mode 진동이 없습니다. 자전축 경사는 직접
측정으로 제약되지 않습니다. 시각 렌더링에서 NearStars 는 일반적인
축 방향을 채택하는데, 자전 속도가 거의 0 이라 spin 관련
foreshortening 이 시각적으로 무시할 만하기 때문입니다. 이 별에
대한 지배적 운동학 사실은 spin 이 아니라 **이동** 입니다. 10.3
arcsec/yr 고유운동과 ~140 km/s 공간속도로, 바너드 별은 하늘에서
가장 빠르게 움직이는 별이며, 향후 수천 년간 계속 접근해 서기
11800 년경 근일점 (~1.14 pc) 에 이른 뒤 멀어집니다.

## Canonical alternatives

두 파라미터가 Phase 2 문헌에 걸쳐 documented divergence 를 안고
있습니다. 두 경우 모두 cfg 는 Phase 2 recommended 값을 채택하지만,
기기 간 편차가 명시적 문서화를 정당화할 만큼 큽니다.

| Field | cfg value (recommended) | Canonical alternatives | Why cfg picks this value |
|---|---|---|---|
| `metallicity_fe_h_dex` | −0.39 ± 0.03 (Jahandar 2023, SPIRou NIR) | −0.15 ± 0.16 (Schweitzer 2019, CARMENES VIS). −0.57 ± 0.10 (Marfil 2021) | 세 측정은 ~0.4 dex 에 걸쳐 있습니다 — 측정 산포가 아니라 실제 계통 불일치입니다. 차가운 M 왜성의 금속도는 근적외선이 선호되는데, 광학 (VIS) 연속체가 분자 밴드에 너무 심하게 가려져 pseudo-continuum 배치와 line-list 불완전성이 VIS 기반 [Fe/H] 를 편향시키기 때문입니다. NIR 분석 (Jahandar 2023, SPIRou) 은 더 깨끗한 분광 영역에서 작업합니다. 그래서 cfg 는 NIR 값 −0.39 를 채택하며, 이는 광학 Schweitzer (−0.15) 와 Marfil (−0.57) 극단 사이입니다. 금속도는 렌더 SED 색에 약하게만 영향을 주므로, 이 divergence 는 시각적으로 결정적이라기보다 문서적입니다. |
| `teff_k` | 3195 ± 28 (González Hernández 2024, ESPRESSO) | 3231 ± 21 (Jahandar 2023). 3254 ± 32 (Marfil 2021). 3273 ± 51 (Schweitzer 2019) | 네 분광 측정은 겨우 ~80 K (3195–3273 K) 에 걸쳐 있어 M 왜성 기준으로는 빡빡합니다. cfg 는 가장 차가운 González Hernández 2024 를 가장 최근 고분해능 ESPRESSO master-spectrum 분석이자 Phase 2 recommended 값으로서 채택합니다. 이 Teff 에서 80 K 이동은 렌더 색조의 인지 불가능한 변화에 해당하므로 (M4 V `#cf5a30` 렌더 허용 오차 안), 이 값들 사이 선택은 시각적으로 결정적이지 않습니다. divergence 는 파라미터 집합의 완전성을 위해 문서화합니다. |

Jahandar 2023 과 Schweitzer 2019 (그리고 Marfil 2021) 은 각자의
측정 배열 안에서 `recommended:false` 대안으로 Phase 2 DB 에 남아
audit trail 을 보존합니다. recommended 픽은 González Hernández
2024 (Teff) 와 Jahandar 2023 ([Fe/H]) 입니다.

## Visual styling

NearStars 렌더러에서 바너드 별은 깊은 붉은빛의 매우 희미한 M4 V
왜성으로 — 가장 가까운 단독성이지만 밝기 면에서는 눈에 띄지 않게 —
표현됩니다. 표면 색조는 `#cf5a30` 으로 인코딩되며, tie-break
선택입니다. 3195 K 흑체 연속체는 파란 쪽이 TiO/VO 분자 밴드에
억제된 뒤 깊은 주황-빨강으로 렌더링되며, 카탈로그 M-왜성 팔레트
에서 더 따뜻한 M1 V AU Mic (`#e0743a`, Teff 가 ~470 K 더 뜨거움) 과
더 차가운 M5.5 Proxima (`#c54c2a`, Teff 가 ~145 K 더 차가움) 사이에
자리합니다. 가까운 천체의 장면 조명 색온도는 3195 K SED 가 직접
구동합니다.

디스크는 희미하고 느리게 떠도는 흑점 피처만 있는 거의 균일한
모습으로 렌더링됩니다 — 바닥 수준 활동도 (log R'HK = −5.82) 와 매우
느린 145 일 자전의 시각적 표현입니다. 극적인 flare 레이어는 없습니다.
flare 는 드문 사건의 박자 찍기이며 (2019 년 HST 원자외선 flare 가
문서화된 사례), AU Mic 의 거의 연속적인 flare 활동이 아니라 가끔
일시적으로 밝아지는 모습으로 렌더링됩니다. 십 년 단위 ~10 yr 활동
사이클은 게임 내 환산 수년에 걸쳐 이미 미묘한 흑점 패턴을 느리게
변조합니다.

지구에서 바너드 별은 V ≈ 9.5 천체 (절대등급 M_V ≈ 13.2) 입니다 —
1.83 pc 근접에도 맨눈 가시성에 한참 못 미치는데, 0.003558 L☉ 의
작은 광도 때문입니다. 실제 하늘에서의 시각 signature 는 밝기가
아니라 **운동** 입니다. 10.3 arcsec/yr 로 알려진 가장 빠르게
움직이는 별이며, 수 세기의 게임 내 시간에 걸친 NearStars 하늘
렌더링은 이 별이 Ophiuchus 배경 필드를 눈에 띄게 기어가는 모습을
보여 줄 것입니다. 가까운 sub-Earth 행성 후보 중 어느 시점에서 봐도,
붉은 디스크는 적당한 각지름을 차지하며 풍경을 깊은 붉은빛의
적외선-우세 빛으로 적실 것입니다. 희미한 ~10 yr 밝아짐 사이클이
유일한 느린 시간 변화이고, 드문 flare 가 유일한 갑작스러운
변화입니다.

## Bibliography

### Read (drove Decisions above)

- **Schweitzer A. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Different roads to radii and masses of the target
  stars*, A&A 625, A68 (`2019A&A...625A..68S`,
  doi:10.1051/0004-6361/201834965, arXiv:1904.03231). CARMENES
  기본 파라미터 편람. Phase 2 recommended 질량 (0.162 ± 0.007 M☉,
  spectroscopic calibration), 광도 (0.003558 ± 0.000072 L☉,
  bolometric flux), 반지름 (0.187 ± 0.001 R☉, 간섭계 — Boyajian
  2012b θ_LD 와 Gaia DR2 거리에서) 의 출처. 대안 Teff (3273 ±
  51 K) 와 대안 VIS 금속도 (−0.15 ± 0.16) 도 제공.
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star*, A&A 690, A79 (`2024A&A...690A..79G`,
  doi:10.1051/0004-6361/202451311, arXiv:2410.00569). ESPRESSO
  master-spectrum SteParSyn 분석. Teff = 3195 ± 28 K (Phase 2
  recommended). sub-Earth 행성 후보 Barnard b (P ≈ 3.15 d, M sin i
  ≈ 0.37 M⊕) 와 유의성이 더 낮은 후보 셋의 발견 논문 — 여기서는
  범위 밖이라 행성 follow-up 으로 표시.
- **Jahandar F. et al. 2023** — SPIRou 근적외선 고분해능 바너드 별
  abundance 분석 (arXiv:2310.12125). Phase 2 recommended 금속도
  [Fe/H] = −0.39 ± 0.03 (NIR, 차가운 M 왜성에 선호) 와 대안 Teff =
  3231 ± 21 K 의 출처. documented 금속도 divergence (Schweitzer VIS
  −0.15 및 Marfil −0.57 대비) 는 이 논문에 정박.
- **Marfil E. et al. 2021** — *The CARMENES search for exoplanets
  around M dwarfs. Stellar atmospheric parameters of target stars
  with SteParSyn*, A&A 656, A162 (`2021A&A...656A.162M`,
  doi:10.1051/0004-6361/202141980, arXiv:2110.07329). CARMENES
  VIS+NIR 파라미터 결정. Teff = 3254 ± 32 K 와 가장 금속이 빈약한
  값 [Fe/H] = −0.57 ± 0.10. 둘 다 Canonical-alternatives 표에 진입.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star: very slow rotation and evidence for long-term
  activity cycle*, MNRAS 488, 5145 (`2019MNRAS.488.5145T`,
  doi:10.1093/mnras/stz1647, arXiv:1812.06712). Phase 2 recommended
  자전 주기 (P_rot = 145 ± 15 d, 광도 측정) 와 색채권 활동
  (log R'HK = −5.82 ± 0.08), 그리고 ~10 yr 장기 활동 사이클의 출처.
  이 합성의 정적 상태 / 느린 자전 그림을 규정.
- **Ribas I. et al. 2018** — *A candidate super-Earth planet orbiting
  near the snow line of Barnard's star*, Nature 563, 365
  (`2018Natur.563..365R`). 두꺼운 원반 / 고속도 멤버십에서 구한
  Phase 2 recommended 운동학 나이 (~8.5 ± 1.5 Gyr) 의 출처. NOTE.
  이 논문이 발표한 super-Earth "Barnard b" 후보 (P ≈ 233 d) 는 이후
  철회됐고 (Lubin et al. 2021), González Hernández 2024 의 단주기
  후보와는 무관.
- **Boyajian T. S. et al. 2012b** — *Stellar Diameters and
  Temperatures II. Main-Sequence K- and M-Stars*, ApJ 757, 112
  (`2012ApJ...757..112B`, doi:10.1088/0004-637X/757/2/112,
  arXiv:1208.2431). 바너드 별의 CHARA 어레이 사지 어두워짐 보정
  각지름 θ_LD = 0.952 mas — Schweitzer 2019 recommended 반지름
  R = 0.187 R☉ 의 간섭계 기반.

### Read (context / methodology, not decision-driving)

- **Mann A. W. et al. 2015** — *How to Constrain Your M Dwarf:
  Measuring Effective Temperature, Bolometric Luminosity, Mass, and
  Radius*, ApJ 804, 64 (`2015ApJ...804...64M`,
  doi:10.1088/0004-637X/804/1/64, arXiv:1501.01635). M_K 기반 경험
  질량 관계로 M = 0.161 ± 0.006 M☉ 를 줌 — Phase 2 대안 질량으로,
  Schweitzer 2019 와 1σ 안에서 일치.

### Read (instrument-only / methodological references)

- **Barnard E. E. 1916** — *A small star with large proper motion*,
  AJ 29, 181. 별 이름의 유래인 10.3 arcsec/yr 고유운동의 발견.
  proper-motion Decisions 행의 출처.

### Not read — superseded or low-priority

철회된 Ribas 2018 233 일 super-Earth 후속 문헌 (Lubin et al. 2021
철회와 하류 재분석), 전용 바너드 별 엔트리가 없는 일반 근방-M-왜성
자전 서베이, 2019 HST 원자외선 flare 논문 (맥락 정보뿐 — frozen
Phase 2 레이어에서 cfg-결정적 측정이 아님), 그리고 성간 전구 미션
제안 (바너드 별은 오래된 flyby 표적) 은 항성 합성에 cfg-결정적인
내용을 더하지 않습니다. 행성 후보 논문 (González Hernández 2024 의
행성 부분과 2025+ 후속) 은 행성 Phase 3 follow-up 워크스페이스로
미룹니다. 전체 필터링된 bib 는 `docs/phase3/_bib/barnards-star.yaml`
에 보존됩니다.

## Stellar wind / astrosphere

바너드 별은 이 세트에서 **가장 작은 astrosphere** 를 가집니다. 알려진
별 중 고유운동이 가장 크기에 ~120 km/s 로 국소 ISM 을 헤치고 나아가는데,
항성풍이 약함에도 (Ṁ ≤ 0.2 Ṁ⊙, Wood 2021) ram pressure 가 항성풍 공동을
겨우 **≲11 AU** 의 standoff 로 압축합니다. 검출된 활동 사이클이 없는,
나이가 많고 자기적으로 조용한 M4 왜성으로 — 정온 코로나가 태양 X-ray
출력의 3% 에 불과하다고 이제 측정으로 확인됐습니다 (France 2020,
Chandra). 다만 X-ray+UV flare 는 여전히 하루 몇 차례씩 뚫고 나옵니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | none (not detected) | low | 나이 많고 자기적으로 조용한 M4 — 발표된 사이클 검출 없음, Phase 2 측정 없음 |
| `stellar_wind_mass_loss_solar` | ≤ 0.2 (upper limit) | medium | Wood 2021 astrospheric Lyα |
| `local_ism_inflow_speed_kms` | ~120 | medium | 6D astrometry 대 LIC (극단적 공간속도) |
| `astrosphere_standoff_au` | ≲ 11 (upper bound) | medium | 120·√(Ṁ_rel)·(V_⊙/V_ISM). 높은 V_ISM 이 공동을 압축한다. Sun 과 같은 항성풍 속도(V_⊙ ≈ 400 km/s, Wood et al. 2002/2005 의 고정속도 가정)를 전제하며, 별마다 달라지는 것은 Ṁ 과 V_ISM 뿐이다 |
| `stellar_radiation_surface_relative_sun` | ~0.1 | medium | 측정: log L_X 25.3 (France 2020 Chandra) = 정온 기준 태양의 0.03×. 하루 ~6회의 X-ray+UV flare 가 시간평균 선량을 끌어올림. 정온-만 canonical 대안: ~0.03 |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~97 / +37 | low | 6D astrometry 대 LIC. **plugin-only** |

## Open items for follow-up

- **sub-Earth 행성 후보 Phase 3 follow-up 워크스페이스.** González
  Hernández 2024 ESPRESSO 캠페인은 sub-Earth 후보 Barnard b
  (P ≈ 3.15 d, M sin i ≈ 0.37 M⊕) 와 유의성이 더 낮은 후보 셋을
  보고합니다. 이들은 항성 합성의 범위 밖입니다. 후보들의 Phase 2
  측정이 큐레이션되면 전용 follow-up 이 행성 Phase 3 합성을 만들어야
  합니다. 철회된 Ribas 2018 233 일 후보는 tau Cet e / 40 Eri A b
  처리를 본떠 refuted 로 기록해야 합니다.
- **금속도 divergence 해소.** NIR (Jahandar −0.39), VIS (Schweitzer
  −0.15), Marfil (−0.57) 측정 간 ~0.4 dex 폭은 실제 계통 차이입니다.
  미래의 큐레이션 패스가 추가 NIR abundance 분석 (예: 추가 SPIRou
  또는 CRIRES+ 작업) 을 ingest 해 차가운 M 왜성 금속도를 좁히고
  NIR 선호 값이 수렴하는지 확인할 수 있습니다.
- **활동 사이클 주기 정밀화.** ~10 yr 사이클 (Toledo-Padrón 2019)
  은 단일 장기 캠페인에서 자릿수 정밀도로 분해됐습니다. 지속적
  모니터링이 주기와 진폭을 정밀화하고 그것이 안정적인 태양형
  사이클인지 준주기 변조인지 확인하면, cfg `activity_cycle_years`
  렌더링이 날카로워집니다.
- **flare 율 특성화.** 2019 HST 원자외선 flare 는 간헐적 flare 를
  확인하지만, frozen Phase 2 레이어에는 정량적 flare 빈도 분포가
  없습니다. TESS / HST flare 센서스가 있으면 미래 cfg 가 그밖에는
  정적인 렌더링에 `flare_rate_per_day` 와 `flare_energy_log_erg_max`
  를 붙일 수 있습니다.
- **자전축 경사.** 제약되지 않음. 자전 속도가 거의 0 이라 spin 관련
  시각 효과가 무시할 만하므로 우선순위는 낮지만, 측정된 경사가
  있으면 희미한 흑점 변조를 올바른 foreshortening 으로 렌더링할 수
  있습니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 테이블의 스키마 출처
- [proxima-cen](proxima-cen.md) — 비교 M 왜성 (M5.5 Ve, ~4.85 Gyr). Proxima 의 더 높은 활동도와 바너드의 바닥 근처 정적 상태를 대비
- [au-mic](au-mic.md) — 비교 M 왜성 (어리고 활동적인 M1 Ve). 바너드의 늙고 조용한 M4 V 와 활동/나이의 정반대 극단
