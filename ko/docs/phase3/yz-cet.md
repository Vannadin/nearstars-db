<!-- YZ Cet Phase 3 합성. cfg-ready 결정과 근거 -->
# YZ Cet — Phase 3 Synthesis

YZ Cet (GJ 54.1. Gaia DR3 2358524597030794112) 은 3.717 pc 거리의
M4.5 V 적색왜성으로 (Gaia DR3 시차 269.06 mas), 약 12.1 광년 떨어져
있으며 태양에서 21번째로 가까운 항성계입니다. 기본 파라미터는 frozen
Phase 2 레이어에서 가져옵니다. 유효온도 Teff = 3100 K (Cifuentes et
al. 2020, SED 피팅. 세 독립 측정이 3056–3151 K 에 분포), 광도
L = 0.0022 ± 0.00005 L☉ (Cifuentes 2020, bolometric flux), 반지름
R = 0.1571 ± 0.0052 R☉ 와 질량 M = 0.1368 ± 0.0033 M☉ (둘 다
Schweitzer et al. 2019, CARMENES) 입니다. UV-Ceti / BY-Draconis 부류의
폭발 변광성 (flare star) 으로, P_rot = 68.4 d 로 느리게 자전하고
(Stock et al. 2020, V-band 측광) 색채권 활동 지표는 log R'HK = −4.71 ±
0.21 (Astudillo-Defru et al. 2017) — 중간-M 왜성치고 적당히 활동적이며,
느리게 변조되는 starspot 배경 위에 잦은 광학 flare 가 얹혀 있습니다.

NearStars 에서 YZ Cet 을 특별하게 만드는 것은 광구가 아니라
자기권입니다. YZ Cet 은 **항성-행성 자기 상호작용(SPI)의 전파 검출이
확인된 최초의 외계행성계** 입니다. Pineda & Villadsen 2023 은 VLA 로
~100% 원편광된 2–4 GHz coherent 전파 버스트를 검출했고, 그 재발 주기가
최내측 행성 b 의 2.02 일 궤도를 거의 따라갔으며, Trigilio et al. 2023
은 uGMRT 550–900 MHz 관측으로 SPI 를 4.37σ 로 확인하면서 오로라 전파
방출(ARE) 을 모델링해 항성 극자기장 B_p ≈ 2.4 kG 와 **b 의 행성
자기장이 최소 0.4 G** 임을 추론했습니다 — 외계행성 자기장의 첫 (간접)
측정입니다. 따라서 이 호스트는 목성-이오 식 flux tube 를 안쪽 행성까지
드리우고, 전자 사이클로트론 메이저 전파 오로라를 띠며, 평범한 flare
활동까지 한꺼번에 보입니다.

**NearStars 시나리오 선택. 깊은 붉은빛의, 적당히 활동적인, 느리게
자전하는 M4.5 V flare star 로, 최내측 행성과 목성-이오 식 항성-행성
자기 상호작용을 정박시키는 모습으로 렌더링합니다.** 항성 레이어는
frozen Phase 2 출처 (Cifuentes 2020 Teff/광도, Schweitzer 2019
질량/반지름, Stock 2020 자전, Astudillo-Defru 2017 활동) 와 두 SPI
전파 논문 (Pineda & Villadsen 2023 검출, Trigilio 2023 확인 + 항성
자기장 추론) 위에 정박합니다. 알려진 주변 원반은 없습니다 — 검출 보고가
없으며 여기서 지어내지도 않습니다. tie-break 하나가 3100 K M4.5 V SED
의 시각 표면 색조를 정하고, SPI / 자기장 결정들은 기하가 모델 의존적
이라 medium-to-low 신뢰도에 둡니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.5 V | high | Astudillo-Defru et al. 2017. Pineda & Villadsen 2023 / Trigilio 2023 (폭발 변광성. UV-Cet / BY-Dra 부류) |
| `mass_msun` | 0.1368 ± 0.0033 | high | Schweitzer et al. 2019 — CARMENES 분광 보정 (Phase 2 recommended). 대안 0.1418 (Schweitzer), 0.1475 (Cifuentes 2020), 0.13 (Astudillo-Defru 2017) 모두 ~1σ 안 |
| `radius_rsun` | 0.1571 ± 0.0052 | high | Schweitzer et al. 2019 — SED 피팅 (Phase 2 recommended). Cifuentes 2020 은 0.1626, Astudillo-Defru 2017 은 0.168 |
| `teff_k` | 3100 | high | Cifuentes et al. 2020 — SED 피팅 (Phase 2 recommended). 세 측정이 3056 (Astudillo-Defru 2017) ~ 3151 K (Schweitzer 2019) 에 분포, 모두 중간-M 과 일관 |
| `luminosity_lsun` | 0.0022 ± 0.00005 | high | Cifuentes et al. 2020 — bolometric flux (Phase 2 recommended). Schweitzer 2019 은 0.002195 로 구분 불가 |
| `metallicity_fe_h_dex` | null (미큐레이션) | low | Phase 2 금속도 측정 없음. 프로젝트 정책에 따라 스킵 (고정 Teff 에서 색 효과 sub-perception) |
| `age_gyr` | ~5 (Phase 2 미큐레이션) | low | Phase 2 나이 배열 없음. 문헌은 YZ Cet 을 수 Gyr 로 봄 (Engle & Guinan 2017 이 68 d 자전으로 ~3.8 Gyr 제시). 느린 자전과 적당한 활동도가 중간 나이 원반 왜성과 일관. cfg 결정 수치는 아님 |
| `rotation_period_days` | 68.4 ± 0.05 | high | Stock et al. 2020 — 결합 V-band 측광 (ASH2+SNO+ASAS+ASAS-SN), Phase 2 recommended. R+I band 는 68.5 ± 1.0 d. Astudillo-Defru 2017 의 83 d 를 대체 |
| `activity_log_rhk` | −4.71 ± 0.21 | high | Astudillo-Defru et al. 2017 — Ca II H&K 지표 (Phase 2 recommended). 느리게 자전하는 중간-M 왜성치고 적당히 활동적 (Rossby number ~0.5. Pineda & Villadsen 2023) |
| `activity_h_alpha_log_lhalpha_lbol` | −4.32 | medium | Reiners 2018 (Pineda & Villadsen 2023 Table 1 경유). Hα 가 약한 방출 상태로, 폭발 변광성 분류와 일관 |
| `x_ray_log_lx_lbol` | −4.13 | medium | Stelzer 2013 (Pineda & Villadsen 2023 Table 1 경유). L_X ≈ 10^27.1 erg/s 로 태양값에 가까움 (Trigilio 2023) |
| `flare_state` | frequent optical flares | medium | TESS 광학 flare 가 광도곡선에 보임 (Pineda & Villadsen 2023). 비coherent gyrosynchrotron 전파 flare 도 2–4 GHz 에서 관측. UV-Cet / BY-Dra 폭발 변광성 |
| `magnetic_field_bf_kg` | ~2.2 | medium | Moutou et al. 2017 — Zeeman-broadening 평균장 ⟨Bf⟩ ≈ 2.2 kG (Pineda & Villadsen 2023 / Trigilio 2023 경유). Rossby number 대비 high outlier 라 과대평가 가능 (Reiners 2022) |
| `magnetic_field_polar_bp_kg` | ~2.4 | medium | Trigilio et al. 2023 — ARE 스펙트럼 (s=2 harmonic, ν_min ≈ 500 MHz → r_max 에서 B_min ≈ 90 G) 에서 추론한 대규모 극자기장 B_p ≲ 2.4 kG. Moutou 2017 ⟨Bf⟩ 와 일관 |
| `spi_radio_confirmed` | true | high | Trigilio et al. 2023 — SPI 의 ARE 가 4.37σ 로 확인 (uGMRT 550–900 MHz, 9회 중 4회 검출이 행성 b 의 두 궤도 위상 sector 로 folding). Pineda & Villadsen 2023 VLA 2–4 GHz 후보 검출 |
| `spi_driver_planet` | b | high | Pineda & Villadsen 2023. Trigilio 2023 — 버스트가 c 나 d 가 아니라 b 의 2.02087 d 궤도로 folding. b 가 최내측 (a/R★ ≈ 21.9) 이고 sub-Alfvénic 영역에 위치 |
| `spi_emission_frequency_ghz` | 0.5–4 | high | Trigilio 2023 (550–900 MHz uGMRT) + Pineda & Villadsen 2023 (2–4 GHz VLA). kG 코로나 자기장의 사이클로트론 harmonic 에서 ECM |
| `visual_surface_tint_hex_primary` | `#cf5630` (M4.5 V 의 깊은 적등색) | medium | Tie-break. 3100 K 흑체에서 TiO/VO 분자 밴드가 파란 쪽을 억제한 뒤. M4 V 바너드 `#cf5a30` (Teff 가 거의 같음) 와 사실상 동일, 더 따뜻한 K/M 호스트보다 붉음 |
| `stellar_color_temp_k` | 3100 | high | Teff 유도 (Cifuentes 2020) |
| `visual_spot_coverage_max` | 0.1 | low | Tie-break. BY-Dra 부류 자전 변조가 68.4 d 측광 주기를 만듦 (Stock 2020). 낮은-중간 cool-spot 비율이 이를 재현. 측정된 filling factor 는 아님 |
| `apparent_magnitude_v_from_earth` | 12.16 | high | Gaia DR3 V (변환). 3.717 pc 근접에도 맨눈 가시성에 한참 못 미침. 0.0022 L☉ 의 작은 광도 때문 |
| `distance_pc` | 3.717 | high | Gaia DR3 시차 269.06 mas. ≈ 12.1 ly, 21번째로 가까운 항성계 |
| `disk_present` | false | high | YZ Cet 의 잔해 원반 보고가 문헌에 없음. 지어내지 않음 (search-and-verify 정책) |

## Surface synthesis

YZ Cet 은 중간-M 왜성에 전형적인 깊은 붉은 광구를 가집니다.
Teff = 3100 K (Cifuentes 2020) 에서 SED 는 근적외선 ~0.93 μm 부근에서
정점을 이루고, 광학 연속체는 TiO 와 VO 분자 밴드에 강하게 억제됩니다 —
다만 더 차가운 M7 V 티가든 별 (2904 K) 만큼 완전히 질식하지는
않습니다. 세 독립 Teff 측정이 3056–3151 K 안에 그치므로 온도는
견고하고 렌더링되는 색도 잘 제약됩니다. R = 0.1571 R☉ (Schweitzer
2019) 과 L = 0.0022 L☉ 에서 별은 태양 광도의 약 1/450 이라, 12.1 광년
근접에도 맨눈으로는 너무 어둡습니다 (V = 12.16).

규정하는 표면 속성은, 느리게 자전하는 spotted 한 flaring 원반으로
표현되는 적당한 자기 활동입니다. Ca II H&K 지표 log R'HK = −4.71
(Astudillo-Defru 2017) 은 YZ Cet 을 중간 활동 영역에 둡니다. Hα 는
약한 방출 상태이고 (log L_Hα/L_bol = −4.32, Reiners 2018, Pineda &
Villadsen 2023 경유), 코로나 X-선 광도 log L_X/L_bol = −4.13 (Stelzer
2013) 은 L_X ≈ 10^27.1 erg/s 로 조용한 태양에 필적합니다 (Trigilio
2023). 별은 형식적으로 UV-Ceti / BY-Draconis 부류의 폭발 변광성입니다.
TESS 광도곡선에 잦은 광학 flare 가 보이고 (Pineda & Villadsen 2023),
cool starspot 에 의한 자전 밝기 변조가 68.4 d 측광 주기를 정의합니다
(Stock 2020). cfg 렌더링에서는, 68 일 자전을 따라 떠도는 낮은-중간
cool-spot 비율을 띤 깊은 붉은 원반에 밝은 flare 가 박힌 모습이
됩니다 — 매우 조용한 노령 왜성 (바너드, 티가든) 보다 활기차지만 AU Mic
같은 젊은 M 왜성의 거의 연속적인 flaring 은 아닙니다.

이 모든 것을 떠받치는 자기장은 강합니다. Zeeman-broadening 은 평균
표면장 ⟨Bf⟩ ≈ 2.2 kG (Moutou 2017) 을 주고, Trigilio 2023 의 SPI 전파
모델링은 오로라-전파-방출 스펙트럼에서 대규모 극자기장 B_p ≈ 2.4 kG
을 독립적으로 추론합니다. 이런 부류의 중간-M 왜성은 "강한 kG 의
축대칭 쌍극자 자기장 위상을 가지는 경향" 이 있고 (Kochukhov & Lavail
2017, Trigilio 2023 경유), YZ Cet 도 그 그림에 맞습니다 — 강하고
정연한 쌍극자가 바로 행성-항성 flux tube 를 충분히 효율적으로 만들어
검출 가능한 전파 오로라를 내게 합니다. (한 가지 caveat. Moutou 2017
Zeeman-broadening 값은 YZ Cet 의 Rossby number ~0.5 대비 high outlier
라, 느린 자전체에 대해 체계적으로 과대평가됐을 수 있습니다, Reiners
2022.)

Phase 2 레이어에 금속도가 큐레이션되어 있지 않고 여기서 합성하지도
않습니다. 고정 Teff 에서 금속도가 렌더링 M-왜성 색에 미치는 영향은
sub-perception 이고, 프로젝트 정책은 신규 호스트에 대해 이를 스킵
합니다. 잔해 원반도 없습니다. YZ Cet 주위 원반의 적외선 초과 검출이나
분해 영상 보고가 없으므로, 별은 원반 없이 렌더링됩니다.

## Atmosphere synthesis

주계열 별은 행성 cfg 의미의 "대기" 를 갖지 않습니다. 항성 합성에서 이
섹션은 색채권, 코로나, flare, 그리고 — YZ Cet 만의 특징인 — 이
시스템을 규정하는 자기권 전파 환경을 다룹니다.

YZ Cet 의 색채권과 코로나는 적당히 활동적인 중간-M 왜성의 것입니다.
색채권 Ca II H&K 지표 log R'HK = −4.71 (Astudillo-Defru 2017) 과 Hα
방출 (log L_Hα/L_bol = −4.32. Reiners 2018) 은 지속적으로 따뜻한
색채권을 가리키고, 코로나 X-선 출력 (log L_X/L_bol = −4.13. Stelzer
2013) 은 절대값으로 조용한 태양 수준에 가깝습니다 (L_X ≈ 10^27.1
erg/s. Trigilio 2023). 68.4 d 자전은 Rossby number Ro ≈ 0.5 (Pineda &
Villadsen 2023) 를 주어 YZ Cet 을 비saturated, 자기 제동 영역에
둡니다 — 활동적이지만 saturated 는 아닙니다. 항성풍은 적당합니다.
질량손실률 추정은 모델에 따라 Ṁ ≲ 0.2–5 Ṁ_⊙ 에 모입니다 (Pineda &
Villadsen 2023 은 현실적 Model B 에서 Ṁ ≈ 0.25 Ṁ_⊙, Trigilio 2023 은
Ṁ ≈ 0.2 Ṁ_⊙ 채택).

핵심 특징은 자기권 전파 오로라입니다. kG 규모의 정연한 쌍극자로 YZ
Cet 은 항성풍을 강하게 가둡니다. Trigilio 2023 은 풍 자기 confinement
파라미터 η★ ≈ 10^8 과 Alfvén 반지름 R_Alf ≈ 100 R★ 을 계산했고,
따라서 **세 행성 모두 별의 자기권 깊숙이** sub-Alfvénic 영역에서
공전합니다. 최내측 행성 b (a/R★ ≈ 21.9, 궤도속도 ~87.6 km/s) 는 닫힌
항성 자기장을 헤집고 지나가며, 그 perturbation 이 flux tube 를 따라
항성 극으로 되돌아가, 거기서 전자-사이클로트론-메이저 방출이 강하게
원편광된 오로라 전파 버스트를 냅니다 — 바로 목성-이오 메커니즘인데
별 크기로 일어납니다. 이는 ~100% 편광된 2–4 GHz 버스트 (Pineda &
Villadsen 2023, VLA) 와, 행성 b 의 두 대칭 궤도-위상 sector 로
folding 되는 550–900 MHz 버스트 (Trigilio 2023, uGMRT. 4.37σ) 로
검출됩니다. ECM 스펙트럼의 저주파 cutoff ν_min ≈ 500 MHz 는 방출
고도에서 B_min ≈ 90 G 를 함의하고, 추론된 극자기장은 B_p ≈ 2.4 kG
입니다.

flare 가 이 모두를 점점이 끊습니다. coherent SPI 버스트 외에도 YZ Cet
은 비coherent gyrosynchrotron 전파 flare (Pineda & Villadsen 2023,
Epoch 2) 와 TESS 광학 flare 를 보입니다 — UV-Ceti 별에 기대되는 평범한
폭발 변광 거동입니다. cfg 목적상 코로나 / 색채권 레이어는 "잦은 flare
를 동반한 적당히 활동적" 으로, 정적-with-드문-flare 노령 왜성과도,
saturated 젊은 flare star 와도 구별됩니다.

## Rotation & spin synthesis

YZ Cet 은 느리게 자전하며, 측광 주기는 P_rot = 68.4 ± 0.05 d (Stock
2020, 결합 V-band 측광. R+I band 는 68.5 ± 1.0 d) 입니다. 이는
Astudillo-Defru 2017 의 이전 83 d 추정과 Pineda & Villadsen 2023 이
synodic-period 위상 wrapping 에 쓴 ~68.5 d 값을 대체합니다. 68 일
주기는 느리지만 극단적이지는 않습니다 — 매우 노령인 티가든 (96 d) 이나
GJ 1151 (~130 d) 보다 훨씬 빠르고, 중간 나이의 적당히 활동적인 중간-M
왜성과 일관됩니다. Engle & Guinan 2017 은 자전으로 ~3.8 Gyr 나이를
추정합니다. Phase 2 에 형식 나이 배열이 없으므로 cfg 는 나이를 결정
입력이 아니라 low-confidence ~5 Gyr 맥락 수치로 다룹니다.

**KSP 구현 노트.** 항성 자전 주기 = 68.4 d = 5 909 760 s. Kopernicus
에서 항성 바디의 `rotationPeriod` 는 초 단위로 설정합니다. 느린
자전이라 spin 관련 시각 foreshortening 은 무시할 만합니다.

자전은 SPI 렌더링에 중요합니다. 버스트가 항성 자전 주기가 아니라
행성 궤도 주기 부근에서 재발하므로 SPI 신호는 진짜 행성 구동이지
자전 artefact 가 아닙니다 — 다만 ~68 d 항성 자전은 기하를 변조합니다.
Pineda & Villadsen 2023 의 두 epoch 사이 (~90 d, 자전 주기의 1.3 배)
에 기울어진 항성 쌍극자가 크게 회전했고, 그래서 버스트가 정확히 같은
궤도 위상에서 재발하지 않았습니다. 충실한 cfg 라면 전파-오로라
애니메이션을 주로 행성 b 의 2.02 일 궤도에 키잉하고 가시 극 기하를
느린 ~68 일로 변조해야 합니다.

자전축 경사는 제약되지 않습니다. Trigilio 2023 의 기하적 ARE 모델은
궤도면 경사 i ≈ 30°–60° 를 선호하고 항성 쌍극자가 자전축과 대략
정렬되며 궤도면에 수직이라고 가정합니다. NearStars 시각 렌더링에는
일반적인 축 배향을 채택합니다. 느린 자전 때문에 정확한 spin 축은 광구
에는 시각적으로 중요하지 않고 (SPI flux-tube 기하에만 영향) 그렇습니다.

## Visual styling

NearStars 렌더러에서 YZ Cet 은, 시그니처가 수수한 광구가 아니라 자기
환경에 있는 깊은 적등색 M4.5 V flare star 로 그려집니다.

- **전체 외형.** `#cf5630` 으로 인코딩한 깊은 적등색 원반. TiO/VO 밴드가
  파란 쪽을 억제한 뒤의 3100 K 흑체 연속체로 — M4 V 바너드 별
  (`#cf5a30`, Teff 가 거의 같음) 과 사실상 같은 색조이고, 카탈로그의 더
  따뜻한 K/M 호스트보다 붉습니다. 세 행성의 장면 조명 색온도는 3100 K
  SED 가 직접 구동합니다.
- **Spotted 표면.** 68.4 일 자전을 따라 떠도는 낮은-중간 cool-spot 비율
  (`visual_spot_coverage_max ≈ 0.1`) 이 BY-Dra 부류 측광 변조를
  재현합니다. 균일한 원반이 아니라 천천히 진화하는 어두운 spot 군집
  입니다.
- **Flare.** 잦은 밝은 광학 flare (UV-Cet 폭발 변광성) — 바너드나 티가든
  보다 활동적이며, 반복되는 transient 밝아짐으로 렌더링하되 젊은 M
  왜성의 거의 연속적인 flaring 은 아닙니다.
- **전파 오로라 (헤드라인).** SPI 방출은 전파 현상이라 맨눈에 보이지는
  않지만, 시스템을 규정하는 특징이므로 시각적으로 표현해야 합니다.
  최내측 행성 b 를 항성 자기 극에 잇는 목성-이오 식 flux tube 로,
  오로라 footpoint 가 b 의 2.02 일 궤도 cadence 로 밝아지고 가시 극은
  68 일 자전으로 변조됩니다. b 의 시점에서 이는 flux tube 발치의 항성
  오로라입니다 — 카탈로그에서 YZ Cet 만의, 시각적으로 독특하고
  과학적으로 근거 있는 효과입니다.
- **행성 하늘에서의 별.** b (a = 0.0163 AU) 에서 별은 ~5.1° 를
  차지합니다 — 지구에서 본 태양의 약 10 배. c (~3.9°) 와 d (~2.9°) 에서는
  더 작지만 여전히 압도적입니다. 원반은 깊은 적등색이고, 각각 지구
  일사량의 8.2, 4.7, 2.7 배인 적외선이 풍부한 빛으로 가까운 세계들을
  적십니다.
- **지구에서.** YZ Cet 은 V = 12.16 의 망원경 천체로, 12.1 광년
  근접에도 0.0022 L☉ 의 작은 광도 때문에 맨눈에는 보이지 않습니다.

## Bibliography

### Read (drove Decisions above)

- **Pineda J.S. & Villadsen J. 2023** — *Coherent radio bursts from
  known M-dwarf planet host YZ Ceti*, Nature Astronomy (arXiv:2304.00031).
  ~100% 원편광된 coherent 전파 버스트를 VLA 2–4 GHz 로 발견했고, 그
  재발이 행성 b 의 2.02087 d 궤도를 거의 따라갑니다. SPI-후보 검출,
  sub-Alfvénic 환경 (Model A/B 풍, Rossby number ~0.5), Table 1 항성
  파라미터 (M, R, Teff, log L_X/L_bol = −4.13, log L_Hα/L_bol = −4.32,
  ⟨Bf⟩ ≈ 2.2 kG, P_rot ~68.5 d), 행성 b 최소 자기장 추론의 출처.
  YZ Cet 을 핵심 SPI 모니터링 사례로 확립.
- **Trigilio C. et al. 2023** — *Star-Planet Interaction at radio
  wavelengths in YZ Ceti: Inferring planetary magnetic field*, ApJL
  (arXiv:2305.00809). uGMRT 550–900 MHz. 9회 중 4회 검출이 행성 b 의 두
  대칭 궤도-위상 sector 로 folding 되어 SPI 의 ARE 를 4.37σ (99.992%)
  로 확인. 확인-SPI 결정, ECM 스펙트럼에서 추론한 항성 극자기장
  B_p ≈ 2.4 kG (s=2, ν_min ≈ 500 MHz), η★ ≈ 10^8 / R_Alf ≈ 100 R★
  sub-Alfvénic 기하, 그리고 **행성 b 자기장 하한 B ≥ 0.4 G** — 첫
  간접 외계행성 자기장 측정 — 의 출처.
- **Stock S. et al. 2020** — *The CARMENES search for exoplanets around
  M dwarfs. Three temperate to warm super-Earths* (`2020A&A...636A.119S`,
  doi:10.1051/0004-6361/201936732). 자전 주기 (68.4 ± 0.05 d, 결합
  V-band 측광) 와 행성 b/c/d 궤도 및 최소질량의 Phase 2 recommended
  출처. Astudillo-Defru 2017 의 83 d 자전 주기를 대체.
- **Cifuentes C. et al. 2020** — *CARMENES input catalogue of M dwarfs.
  Photometric and astrometric properties* (`2020A&A...642A.115C`,
  doi:10.1051/0004-6361/202038295). 유효온도 (3100 K, SED 피팅) 와 광도
  (0.0022 L☉, bolometric flux) 의 Phase 2 recommended 출처.
- **Schweitzer A. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Different roads to radii and masses of the target
  stars* (`2019A&A...625A..68S`, doi:10.1051/0004-6361/201834965).
  질량 (0.1368 M☉) 과 반지름 (0.1571 R☉) 의 Phase 2 recommended 출처.
- **Astudillo-Defru N. et al. 2017** — *The HARPS search for southern
  extra-solar planets. A compact system of short-period super-Earths
  around YZ Ceti* (`2017A&A...605L..11A`, doi:10.1051/0004-6361/201731581).
  세 행성의 발견 논문. 활동 지표 (log R'HK = −4.71) 와 분광형의 Phase 2
  recommended 출처. 이전 Teff/질량/반지름 대안은 `recommended:false`
  로 보존.

### Read (context / methodology, not decision-driving)

- **Moutou C. et al. 2017** — YZ Cet 의 Zeeman-broadening 평균장
  ⟨Bf⟩ ≈ 2.2 kG (Pineda & Villadsen 2023 / Trigilio 2023 경유).
  자기장-강도 Decisions 행이 여기서 옴. Reiners 2022 가 느린-자전체
  과대평가 가능성을 표시.
- **Stelzer B. et al. 2013** & **Reiners A. et al. 2018** — 코로나 X-선
  (log L_X/L_bol = −4.13) 과 Hα (log L_Hα/L_bol = −4.32) 활동 지표,
  둘 다 Pineda & Villadsen 2023 Table 1 컴파일레이션 경유. 활동 행의
  맥락.
- **Engle S.G. & Guinan E.F. 2017** — ~3.8 Gyr 나이를 주는 자전-나이
  관계 (Trigilio 2023 경유). 맥락만. Phase 2 큐레이션 값은 아님.

### Read (instrument-only, not visual-informative)

- Pineda & Villadsen 2023 (CASA / VLA self-calibration, Stokes V 동적
  스펙트럼) 과 Trigilio 2023 (uGMRT band-4 보정, hollow-cone ARE 기하)
  의 전파-간섭계 방법론은 SPI 주장의 기기적 골격이지만, 위에서 이미 쓴
  버스트 통계 이상의 직접 시각 필드를 주지는 않습니다.

### Not read — no arXiv preprint or low-priority (~handful)

이전 Astudillo-Defru 2017 항성-파라미터 대안 (Teff = 3056 K,
R = 0.168 R☉) 은 recommended Cifuentes/Schweitzer 값으로 대체되었고
Phase 2 DB 감사 추적에만 보존됩니다. SPI 논문 안에 인용된 일반적인
느린-자전-M-왜성 전파-flare-통계 서베이 (Villadsen & Hallinan 2019,
Callingham 2021) 는 맥락용으로 읽었지만 YZ-Cet-고유 cfg 수치는 주지
않습니다. 읽을 잔해-원반 논문은 없습니다 (보고된 바 없음).

## Open items for follow-up

- **행성 Phase 3 합성.** 세 행성 (b, c, d) 은 별도 Phase 3 문서
  (`yz-cet-b/c/d.md`) 로 만듭니다. 행성 b 의 추론된 ≥ 0.4 G 자기장
  (Trigilio 2023) 이 SPI 구동체이고 b 합성에 직접 들어갑니다.
- **항성 자기장 기하.** YZ Cet 의 대규모 자기장 Zeeman-Doppler-Imaging
  (ZDI) 지도는 아직 없고, 두 SPI 논문 모두 Proxima Cen 의 위상에서
  스케일합니다. 직접 ZDI 지도가 있으면 쌍극자 기울기와 경사를 못박아
  cfg 의 전파-오로라 flux-tube 애니메이션을 다듬을 수 있습니다.
  Moutou 2017 ⟨Bf⟩ ≈ 2.2 kG 은 ZDI 기반 자기장이 나오면 재검토해야
  합니다 (Reiners 2022 가 느린-자전체 과대평가 가능성 제기).
- **나이.** Phase 2 나이 배열 없음. 미래 큐레이션이 자이로크로놀로지나
  운동학 나이를 추가하면 low-confidence ~5 Gyr 맥락 수치를 교체해야
  합니다.
- **Flare-율 정량화.** 폭발 변광성 분류는 정성적입니다. TESS flare
  census 가 있으면 미래 cfg 가 정량적 `flare_rate_per_day` 를 렌더링에
  붙일 수 있습니다.
- **SPI 전파-오로라 시각화 충실도.** b 의 2.02 d 궤도에 키잉하고 68 d
  자전으로 변조하는 flux-tube footpoint 밝아짐은 hollow-cone ARE 모델에
  근거한 tie-break 시각 선택입니다. 렌더러가 표현 가능해지면 다듬습니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 표의 스키마 출처
- [yz-cet-b](yz-cet-b.md) — 최내측 행성. 추론된 ≥ 0.4 G 자기장을 가진 SPI 구동체
- [yz-cet-c](yz-cet-c.md) — 중간 행성
- [yz-cet-d](yz-cet-d.md) — 최외측 행성
- [barnards-star](barnards-star.md) — 비교 M 왜성 (M4.0 Ve, Teff 거의 동일). 바너드의 노령 정적 near-floor 활동과 YZ Cet 의 적당한 활동 및 SPI 전파 오로라를 대비
- [teegardens-star](teegardens-star.md) — 비교용 더 차갑고 노령이며 훨씬 조용한 초저온 왜성 (M7 V, 96 d 자전)
- [proxima-cen](proxima-cen.md) — 비교 M 왜성이자 두 전파 논문이 YZ Cet 자기장을 스케일하는 데 쓴 SPI 유사체
