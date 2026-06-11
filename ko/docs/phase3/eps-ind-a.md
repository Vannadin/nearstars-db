<!-- eps Ind A Phase 3 합성. cfg-ready 결정과 근거 -->
# ε Indi A — Phase 3 Synthesis

ε Indi A (HD 209100, HIP 108870, GJ 845 A, HR 8387) 는 3.638 pc 거리의
K5 V 왜성으로 (Gaia DR3 시차 274.84 ± 0.10 mas), 약 11.9 광년 떨어져
있으며 태양에서 가장 가까운 항성계 중 하나의 호스트이자 주목할 만한
계층적 삼중성계의 주성입니다. 기본 파라미터는 frozen Phase 2 레이어에서
가져옵니다. 유효온도 Teff = 4700 ± 65 K (Lundkvist et al. 2024,
고분산 UVES 분광), 광도 L = 0.239 ± 0.001 L☉ (Feng et al. 2019,
bolometric flux), 반지름 R = 0.713 ± 0.006 R☉ (Lundkvist et al. 2024,
Rains et al. 2020 의 limb-darkened 각지름 θ_LD = 1.817 ± 0.013 mas 와
Gaia DR3 거리를 결합), 질량 M = 0.782 ± 0.023 M☉ (Lundkvist et al.
2024) 입니다. 이 질량은 측성지진학으로 결정됐다는 점에서 주목할 만합니다.
Lundkvist 2024 는 ν_max = 5265 ± 110 µHz 에서 태양형 진동을 검출했는데,
이는 어떤 별에서 측정된 것 중 가장 높은 주파수의 태양형 진동으로,
ε Indi A 를 진동이 측정된 가장 차가운 왜성으로 만듭니다. 이 별은 조용하고
느리게 자전하는 K 왜성입니다. 색채권 활동 지표는 log R'HK = −4.72
(Chen et al. 2022, Pace 2013 채택) 이고 자전 주기는 P_rot ≈ 35 d
(Feng et al. 2018), HARPS Ca II H&K 아카이브에서 검출된 색채권 활동
주기는 ≈ 2600 d (≈ 7.1 yr) 입니다 (Lundkvist 2024).

NearStars 에서 ε Indi A 를 특별하게 만드는 것은 그 시스템입니다. ε Indi A
는 **태양에 가장 가까운 직접 촬영 차가운 거대 외계행성** 인 ε Indi A b 를
거느립니다 — ~20.9 AU 궤도의 ~7.6 M_Jup 슈퍼목성으로, JWST 가 촬영한 첫
태양-나이 (~3.5 Gyr) 거대 외계행성이며 온도는 ~275 K 부근, 암모니아가
확인됐고 두꺼운 물-얼음 구름의 증거가 있습니다 (Matthews et al. 2024,
2026). 같은 별은 ~1459 AU 에서 **ε Indi B** 의 공전을 받는데, 이는 갈색왜성
쌍입니다 (Ba: T1–1.5, 66.9 M_Jup. Bb: T6, 53.3 M_Jup. Chen et al. 2022
역학 질량) — 하늘에서 가장 잘 특성화된 갈색왜성 축에 듭니다. 따라서 전체
ε Indi 시스템은 K 왜성, 차가운 슈퍼목성, 그리고 두 T-왜성 갈색왜성을
12 광년 안의 하나의 중력으로 묶인 계층 안에 담고 있습니다.

**NearStars 시나리오 선택. 따뜻한 오렌지-호박색의, 조용하고, 느리게
자전하는 K5 V 왜성 — 세 번째로 가까운 맨눈 K 왜성 — 으로, 가장 가까운
직접 촬영 차가운 슈퍼목성과 멀리 떨어진 갈색왜성 쌍 동반체를 거느린
모습으로 렌더링합니다.** 항성 레이어는 frozen Phase 2 출처 (Lundkvist
2024 질량/반지름/Teff, Feng 2019 광도, Feng 2018 자전, Chen 2022 활동 +
나이) 와 Chen 2022 의 갈색왜성 쌍 맥락 위에 정박합니다. 알려진 주변
원반은 없습니다 — 적외선 초과나 영상 검출 보고가 없으며 여기서 지어내지도
않습니다. tie-break 하나가 4700 K K5 V SED 의 시각 표면 색조를 정하고,
나이와 자전은 Phase 2 나이 배열이 없고 자전 방법이 측광이 아니라
RV-활동지표라서 medium 신뢰도에 둡니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K5 V | high | Lundkvist et al. 2024 (제목. "the K5 V star ε Indi A"). DB raw.spectype. 오래된 카탈로그는 가끔 K4.5 V / K2 V (Feng 2019) 로 표기 — K5 V 가 권장 현대 분광형 |
| `mass_msun` | 0.782 ± 0.023 | high | Lundkvist et al. 2024 — 측성지진 ν_max 스케일링 (HARPS+UVES) 에 간섭계 R 적용 (Phase 2 recommended). Demory et al. 2009 0.762 ± 0.038 이 ~1σ 안에서 일치 |
| `radius_rsun` | 0.713 ± 0.006 | high | Lundkvist et al. 2024 — Rains 2020 θ_LD = 1.817 ± 0.013 mas + Gaia DR3 d = 3.648 pc (Phase 2 recommended). "Rains et al. 2020 의 값과 매우 잘 일치" |
| `teff_k` | 4700 ± 65 | high | Lundkvist et al. 2024 — 고분산 UVES 분광 (Phase 2 recommended). 문헌 중앙값 ≈ 4649 K (Lundkvist §2.3) 과 일관 |
| `luminosity_lsun` | 0.239 ± 0.001 | high | Feng et al. 2019 — bolometric flux (Phase 2 recommended). R 0.713, Teff 4700 과 Stefan–Boltzmann 으로 일관 |
| `metallicity_fe_h_dex` | null (Phase 2 미큐레이션) | low | Phase 2 금속도 배열 없음. 프로젝트 정책에 따라 스킵 (고정 Teff 에서 색 효과 sub-perception). 문헌. −0.17 ± 0.03 (Lundkvist 2024 UVES), −0.06 ± 0.08 (Santos 2004, Matthews 2026 경유) — 약간 sub-solar, cfg 결정 수치 아님 |
| `age_gyr` | ~3.5 (Phase 2 미큐레이션) | medium | Chen et al. 2022 — Bayesian 활동-나이 (log R'HK = −4.72 Pace 2013 + ROSAT R_X = −5.62) 가 3.48 (+0.78/−1.03) Gyr 제시. Feng 2019 ~4 Gyr, Cardoso 2012 3.7–4.3 Gyr 가 보강. Phase 2 나이 배열 없음. 문헌은 0.39–5 Gyr 에 분포 (Lundkvist 2024 intro), 활동 가지를 채택 |
| `rotation_period_days` | ~35 | medium | Feng et al. 2018 — RV + 분광 활동지표 (NaD/R'HK/BIS) 주기도. 17.8 d 신호는 ~35 d 의 half-rotation alias. 형식 σ 없음. 22 d (Saar & Osten 1997) 와 ~20 d (Lachaume 1999) 를 대체. 측광 아님 (출판된 측광 주기 없음 — Chen 2022) |
| `activity_log_rhk` | −4.72 | high | Chen et al. 2022 (Pace 2013 채택) — Ca II H&K 색채권 지표 (Phase 2 recommended). 조용하고 중간 나이의 K 왜성, 태양 평균보다 약간 덜 활동적 |
| `activity_cycle_years` | ~7.1 | medium | Lundkvist et al. 2024 §4.3 — 4293 개 HARPS 아카이브 log R'HK 점 (2003–2016) 을 위상 접은 ≈ 2600 d 사인 주기. 측성지진 진폭이 주기와 반비례로 변함 |
| `visual_surface_tint_hex_primary` | `#ffb870` (따뜻한 오렌지-호박색 K5 V) | medium | Tie-break. 4700 K 흑체에서 분자 밴드가 파란 쪽을 억제한 뒤, 더 따뜻한 K 왜성 (40 Eri A K0.5 V `#ffd5a8`, ε Eri K2 V `#ffd9a8`) 보다 깊은 호박색으로, M-왜성 적색보다는 따뜻하게 렌더링. K5 V 가 그 사이에 위치 |
| `stellar_color_temp_k` | 4700 | high | Teff 유도 (Lundkvist et al. 2024) |
| `visual_spot_coverage_max` | 0.05 | low | Tie-break. 느린 35 d 자전을 가진 조용한 K 왜성 (log R'HK = −4.72) 은 ~7 yr 주기를 변조하는 낮은 cool-spot 비율만 지지. 측정된 filling factor 는 아님 |
| `disk_present` | false | high | ε Indi A 의 잔해 원반 보고가 문헌에 없음. 지어내지 않음 (search-and-verify 정책) |
| `companion_planet_present` | true (ε Indi A b, ~20.9 AU 의 ~7.6 M_Jup 차가운 슈퍼목성) | high | Matthews et al. 2024 JWST/MIRI 발견 영상. Matthews 2026 두 번째 epoch + 정밀 질량. 행성 Phase 3 은 `docs/phase3/eps-ind-a-b.md` |
| `companion_brown_dwarf_pair_present` | true (ε Indi Ba T1–1.5 66.9 M_Jup + Bb T6 53.3 M_Jup, ~1459 AU) | high | Chen et al. 2022 — VLT/NACO 상대 + FORS2 절대 측성. 역학 질량 정밀도 <0.5%. DB 추가 대기 (아직 NearStars 바디 아님) |
| `apparent_magnitude_v_from_earth` | 4.66 | high | Gaia DR3 V (변환). 수수한 0.239 L☉ 광도에도 11.9 광년 근접 덕에 인두스자리의 맨눈 별 |
| `distance_pc` | 3.638 | high | Gaia DR3 시차 274.84 mas. ≈ 11.87 ly |

## Surface synthesis

ε Indi A 는 후기-K 왜성에 전형적인 따뜻한 오렌지-호박색 광구를 가집니다.
Teff = 4700 K (Lundkvist 2024) 에서 SED 는 적등색 ~620 nm 부근에서
정점을 이루고, 광학 연속체는 MgH 와 CaH 분자 밴드의 영향을 받으며 첫
TiO 머리가 ~6300 Å 아래에서 물어뜯기 시작합니다 — 진짜 M 왜성보다는
훨씬 덜 억제됐지만, 카탈로그의 더 이른 K 왜성 (5143 K 의 40 Eri A K0.5 V,
5039 K 의 ε Eri K2 V) 보다는 분명히 차갑고 더 오렌지색입니다. R = 0.713 R☉
과 L = 0.239 L☉ 에서 별은 태양 광도의 약 1/4 입니다. 11.9 광년 거리에서도
이는 맨눈 범위 안에 들어와 (V = 4.66), 남쪽 인두스자리에서 가장 밝은
별이 됩니다.

규정하는 표면 속성은 조용함입니다. 색채권 Ca II H&K 지표 log R'HK = −4.72
(Chen 2022, Pace 2013 채택) 는 ε Indi A 를 조용하고 중간 나이의 K 왜성으로
표시합니다 — 태양 평균 활동도보다 약간 낮고 ε Eri (−4.50) 같은 활동적인
K 왜성보다는 한참 아래입니다. 느린 ~35 d 자전 (Feng 2018) 은 ~3.5 Gyr
활동 나이와, 그리고 자기 제동된 비saturated 영역과 일관됩니다. Lundkvist
2024 는 13 년치 HARPS Ca II H&K 아카이브를 위상 접어 ≈ 2600 d (≈ 7.1 yr)
활동 주기를 복원했고, 측성지진 모드 진폭이 주기와 반비례로 변함을
보였습니다 (HARPS 로는 2011 년 주기 최소 부근에서, UVES 로는 2021 년 주기
최대 부근에서 우연히 포착). cfg 렌더링에서는 다년 주기에 맞춰 천천히
변조되는 낮은 cool-spot 비율 (`visual_spot_coverage_max ≈ 0.05`) 만 띤
따뜻한 오렌지-호박색 원반이 됩니다 — flaring 하는 것이 아니라 차분한
광구입니다.

측성지진 검출 자체가 주목할 표면 속성입니다. ν_max = 5265 ± 110 µHz 는
어떤 별에서 측정된 것 중 가장 높은 주파수의 태양형 진동 스펙트럼으로
(Lundkvist 2024), α Cen B 와 τ Ceti 를 능가합니다. 진동 진폭은 매우 작고
(~3.4 cm/s) — 차갑고 조용하며 저광도인 왜성에 걸맞으며 — 직접 보이는
특징은 아니지만, cfg 가 채택하는 측성지진 질량을 정박시킵니다.

Phase 2 레이어에 금속도가 큐레이션되어 있지 않고 여기서 합성하지도
않습니다. 문헌값은 약간 sub-solar 이지만 ([Fe/H] ≈ −0.17, Lundkvist
2024. −0.06, Santos 2004), 고정 Teff 에서 렌더링 K-왜성 색에 미치는
영향은 sub-perception 이고 프로젝트 정책은 이를 스킵합니다. 잔해 원반은
없습니다. ε Indi A 주위 원반의 적외선 초과 검출이나 분해 영상 보고가
없으므로, 별은 원반 없이 렌더링됩니다.

## Atmosphere synthesis

주계열 별은 행성 cfg 의미의 "대기" 를 갖지 않습니다. 항성 합성에서 이
섹션은 색채권, 코로나, 활동 주기를 다룹니다.

ε Indi A 의 색채권과 코로나는 조용하고 중간 나이인 K 왜성의 것입니다.
색채권 Ca II H&K 지표 log R'HK = −4.72 (Chen 2022, Pace 2013 채택) 는
태양 평균 아래에 있고, 코로나 X-선 활동도 그에 맞춰 낮습니다 — ROSAT
전천 서베이는 X-선-대-bolometric 비 R_X = log(L_X/L_bol) ≈ −5.62
(Chen 2022 의 활동-나이 분석 경유) 를 주는데, K 왜성치고 조용한 쪽
끝입니다. 느린 ~35 d 자전 (Feng 2018) 은 ε Indi A 를 비saturated,
자기 제동 영역에 두고, ~7.1 yr 색채권 주기 (Lundkvist 2024) 는 태양형
활동 주기입니다 — 태양의 11 yr 보다 짧지만 잘 정돈되고 사인꼴이며,
측성지진 진폭이 그와 반위상으로 변조됩니다.

여기에는 카탈로그의 활동적인 왜성과 달리 헤드라인 flaring 이나 자기권
현상이 없습니다. ε Indi A 는 차분하고 조용한 별로, 그 의미는 스스로의
활동이 아니라 행성·준항성 동반체에 있습니다. cfg 목적상 코로나 / 색채권
레이어는 "조용하고 태양형 ~7 yr 활동 주기를 가진" 으로, 거의-죽은-조용한
노령 M 왜성과도, 시끄러운 젊은/활동적인 K·M 왜성과도 구별됩니다.

충실한 렌더를 위해 인코딩할 만한 한 가지 미묘함은 활동 주기입니다. 주기
최대에서 색채권 방출과 cool-spot 변조가 적당히 강해지고 측성지진 모드
진폭이 약해지는 — 결합된 거동이라, 미래 cfg 가 렌더링한다면 느린 ~7 yr
밝아짐 / spot-coverage 애니메이션을 구동할 수 있습니다.

## Rotation & spin synthesis

ε Indi A 는 P_rot ≈ 35 d (Feng 2018) 로 느리게 자전합니다. 이 값은
측광 자전 주기가 아니라 — 별은 "출판된 측광 자전 주기가 없습니다"
(Chen 2022) — HARPS 시선속도를 분광 활동지표 주기도 (NaD1/NaD2, R'HK,
BIS) 와 결합해 유도했는데, 두드러진 17.8 d 신호는 진짜 ~35 d 주기의
half-rotation alias 입니다 (Feng 2018, "ε Indi 의 자전 주기는 약 35 d
로, 17.8 d 의 대략 두 배"). 형식 불확실도는 출판되지 않았습니다. 이
~35 d 값은 일부 초기 나이 결정에 쓰인 더 오래되고 짧은 추정 ~22 d
(Saar & Osten 1997) 와 ~20 d (Lachaume 1999) 를 대체하며, Feng 2019 이
보강합니다. cfg 는 35 d 를 medium 신뢰도로 채택하는데, σ 가 없고 방법이
비측광이기 때문입니다.

**KSP 구현 노트.** 항성 자전 주기 ≈ 35 d = 3 024 000 s. Kopernicus 에서
항성 바디의 `rotationPeriod` 는 초 단위로 설정합니다. 느린 자전이라 spin
관련 시각 foreshortening 은 무시할 만합니다.

자전은 나이로 이어집니다. ε Indi A 의 나이는 이 시스템의 오랜 미해결
문제 중 하나입니다 — Lundkvist 2024 는 자전·활동·운동학·진화 방법에 걸쳐
0.39–5 Gyr 에 분포하는 추정을 언급합니다. Lachaume 1999 가 쓴 더 짧은
자전 주기 (~20 d) 는 더 어린 나이 (0.8–2.0 Gyr) 를 냈고, 현대의 ~35 d
주기와 색채권 활동은 나이를 더 오래된 쪽으로 밉니다. Chen 2022 의
Bayesian 활동-나이 방법 (log R'HK + X-선 + Tycho 측광) 은 3.48
(+0.78/−1.03) Gyr 를 주는데, 이는 Feng 2019 의 ~4 Gyr 및 Cardoso 2012
진화론적 3.7–4.3 Gyr 와 일관됩니다 — 그리고 이 ~3.5 Gyr 가 cfg 가 채택하는
시스템 나이입니다 (갈색왜성 냉각 벤치마크와 행성 b 의 "태양-나이 거대
행성" 틀에도 관련). Phase 2 나이 배열이 없으므로 나이는 literature-direct
값으로 medium 신뢰도에 둡니다.

자전축 경사는 광구에 대해 제약되지 않습니다. NearStars 시각 렌더링에는
일반적인 축 배향을 채택합니다. 느린 자전 때문에 정확한 spin 축은 원반에
시각적으로 중요하지 않기 때문입니다.

## Visual styling

NearStars 렌더러에서 ε Indi A 는, 의미가 스스로의 수수하고 조용한 광구가
아니라 그 동반체에 있는 따뜻한 오렌지-호박색 K5 V 왜성으로 그려집니다.

- **전체 외형.** `#ffb870` 으로 인코딩한 따뜻한 오렌지-호박색 원반. 분자
  밴드가 파란 쪽을 억제한 뒤의 4700 K 흑체 연속체로 — 카탈로그의 더 따뜻한
  K 왜성 (40 Eri A K0.5 V `#ffd5a8`, ε Eri K2 V `#ffd9a8`) 보다 깊은
  호박색이고, M-왜성 적색 (바너드 `#cf5a30`) 보다 분명히 따뜻 (덜 붉음)
  합니다. K5 V 가 그 사이에 위치하며, 가까운 K 왜성 중 뚜렷이 오렌지인
  것으로 읽히도록 색조를 잡았습니다. 장면 조명 색온도는 4700 K SED 가
  구동합니다.
- **조용한 spotted 표면.** 35 d 자전과 ~7 yr 활동 주기에 맞춰 천천히
  변조되는 낮은 cool-spot 비율 (`visual_spot_coverage_max ≈ 0.05`). 차분한
  원반 — 활동적인 K 왜성의 분주한 spotted 표면이 아니라, 천천히 진화하는
  작은 spot 군집 몇 개입니다.
- **활동 주기 (미묘함).** ~7.1 yr 태양형 색채권 주기 (Lundkvist 2024) 는
  주기 최대에서 색채권 방출의 느리고 적당한 밝아짐과 spot 비율의 작은
  상승으로 표현할 수 있습니다 — ε Eri 의 시끄러운 2.9 yr 주기보다 훨씬
  약한, 부드러운 다년 애니메이션입니다.
- **flare 없음, 오로라 없음.** 카탈로그의 활동적인 왜성과 달리 ε Indi A 는
  규정하는 flaring 이나 자기권 특징이 없습니다. 꾸준하고 차분한
  오렌지-호박색 별로 렌더링됩니다.
- **하늘의 동반체 (헤드라인).** 시스템의 시각적 흥미는 동반체에 있습니다.
  차가운 슈퍼목성 ε Indi A b 는 ~20.9 AU 에서 공전합니다 — 별에서 보면
  멀고 희미한 점이고, 행성에서 보면 별은 ~1.1 arcmin (0.018°) 를 차지해
  지구에서 본 태양 각크기의 약 1/30, 눈부신 오렌지-호박색 점입니다. 훨씬
  멀리 ~1459 AU 에서는 갈색왜성 쌍 ε Indi B (Ba + Bb) 가 두 개의 희미한
  깊은-적색 T-왜성 점으로 빛납니다 — 지구에서 맨눈으로는 보이지 않을 만큼
  어둡지만 시스템의 광역 렌더에서는 인상적인 쌍입니다.
- **지구에서.** ε Indi A 는 인두스자리의 V = 4.66 맨눈 별로, 수수한
  0.239 L☉ 광도에도 11.9 광년 근접 덕에 망원경 없이 보입니다 — 하늘에서
  가장 가까운 맨눈 별 중 하나입니다.

## Bibliography

### Read (drove Decisions above)

- **Lundkvist M. S. et al. 2024** — *Low-amplitude solar-like
  oscillations in the K5 V star ε Indi A*, ApJ 964, 110
  (`2024ApJ...964..110L`, doi:10.3847/1538-4357/ad25f2,
  arXiv:2403.04509). ν_max = 5265 ± 110 µHz (역대 최고 주파수) 에서
  태양형 진동을 검출해, 간섭계 R = 0.713 ± 0.006 R☉ (Rains 2020 θ_LD +
  Gaia d) 와 ν_max 스케일링으로 측성지진 질량 M = 0.782 ± 0.023 M☉
  도출. UVES 에서 Teff = 4700 ± 65 K, [Fe/H] = −0.17. HARPS R'HK
  아카이브에서 ≈ 2600 d 활동 주기. 질량/반지름/Teff 의 Phase 2
  recommended 앵커.
- **Feng F. et al. 2019** — *Detection of the nearest Jupiter analog in
  radial velocity and astrometry data*, MNRAS 490, 5002
  (`2019MNRAS.490.5002F`, doi:10.1093/mnras/stz2912, arXiv:1910.06804).
  RV + Hipparcos/Gaia 측성으로 ε Indi A b 검출. 광도 (0.239 L☉) 의
  Phase 2 recommended 출처이며 ~35 d 자전과 ~4 Gyr 나이를 보강. 여기서의
  행성 궤도 (a ≈ 11.6 AU, ~3 M_Jup) 는 Matthews 2026 으로 대체.
- **Feng F. et al. 2018** — *Detection of the closest Jovian exoplanet
  in the ε Indi triple system* (`2018arXiv180308163F`, arXiv:1803.08163).
  arXiv 프리프린트. 자전 주기 (~35 d, RV + 활동지표 주기도. 17.8 d 신호는
  half-rotation alias) 의 Phase 2 recommended 출처. 심사 bibcode 없음 —
  행성 궤도는 Feng 2019 / Matthews 2026 으로 대체.
- **Chen M. et al. 2022** — *Precise Dynamical Masses of ε Indi Ba and
  Bb: Evidence of Slowed Cooling at the L/T Transition*, AJ 163, 288
  (`2022AJ....163..288C`, doi:10.3847/1538-3881/ac66d2,
  arXiv:2205.08077). VLT/NACO 상대 + FORS2 절대 측성으로 갈색왜성 쌍.
  Ba (T1–1.5) 66.92 ± 0.36 M_Jup, Bb (T6) 53.25 ± 0.29 M_Jup. ε Indi A
  활동 지표 (log R'HK = −4.72, Pace 2013) 와 채택 시스템 나이 (3.48
  +0.78/−1.03 Gyr, Bayesian 활동-나이) 의 Phase 2 recommended 출처 —
  갈색왜성 쌍 Decisions 행의 출처이기도.

### Read (context / methodology, not decision-driving)

- **Matthews E. C. et al. 2024** — ε Indi A b 의 JWST/MIRI 직접 촬영
  발견 (`2024Natur.633..789M`, arXiv:2503.01599). ~275 K 차가운
  슈퍼목성과 elevated-metallicity / 3–5 µm 흐림 맥락을 확립. 행성 b 합성
  (`docs/phase3/eps-ind-a-b.md`) 을 구동하며, 여기서는 시스템 틀을 위해
  인용. 캐시에 ar5iv 전문이 없어 (HTML-only stub), 숫자는 초록과 Matthews
  2026 의 요약에서 취함.
- **Matthews E. C. et al. 2026** — *A second visit to ε Ind Ab with
  JWST*, ApJL (doi:10.3847/2041-8213/ae5823, arXiv:2603.08780). 두 번째
  JWST/MIRI epoch 으로 암모니아 확인 + 두꺼운 물-얼음 구름 제안. 정밀 질량
  7.6 ± 0.7 M_Jup, a = 20.9 AU, e = 0.244. 행성 b 합성을 구동하며, 여기서는
  시스템 틀을 위해 인용.
- **Demory B.-O. et al. 2009** — VLTI/VINCI 간섭계 반지름/Teff/L
  (`2009A&A...505..205D`). Phase 2 대안 질량 0.762 ± 0.038 M☉ (Xia 2008
  M–L 관계 경유), Lundkvist 2024 와 1σ 안 일치. VizieR-only (ar5iv 본문
  없음). 이번 세션에서 표-검증 안 됨.
- **Santos N. C. et al. 2004** — 행성-호스트 별의 분광 금속도
  (`2004A&A...415.1153S`). ε Indi A 에 대해 [Fe/H] = −0.06 ± 0.08
  (Matthews 2026 경유). 스킵된 금속도 행의 맥락.

### Read (instrument-only, not visual-informative)

- Lundkvist 2024 의 측성지진 방법론 (HARPS/UVES RV 시계열, 가중 파워
  스펙트럼, ν_max 엔벨로프 피팅) 과 Chen 2022 의 측성 방법론 (NACO 상대 +
  FORS2 절대 측성, orvara 식 궤도 피팅) 은 질량과 나이 결정의 기기적
  골격이지만, 위에서 이미 쓴 값 이상의 직접 시각 필드를 주지는 않습니다.

### Not read — no arXiv preprint or low-priority (~handful)

Demory 2009 의 VLTI/VINCI 별별 간섭계 표는 ar5iv 본문이 아니라 VizieR
(J/A+A/505/205) 에 있어 bibliography 에서 manual_followup 으로 표시됐고,
그 질량값은 Phase 2 대안으로 보존됩니다. 더 오래된 자전/나이 추정
(Saar & Osten 1997 ~22 d, Lachaume 1999 ~20 d) 은 Feng 2018 ~35 d 주기와
Chen 2022 활동 나이로 대체되어 역사적 맥락으로만 보존됩니다. 읽을
잔해-원반 논문은 없습니다 (보고된 바 없음).

## Stellar wind / astrosphere

ε Ind A 는 교과서적인 **compact astrosphere** 입니다. 적당한
항성풍 (Ṁ = 0.5 Ṁ⊙) 이 빠른 ~68 km/s ISM 유입과 부딪치며 겨우
**~32 AU** 에서 standoff 합니다 — Wood 2005 가 이를 명시적으로
compact 라 부르며, 우리의 6D-측성 V_ISM (69 km/s) 이 Wood 의
68 km/s 를 재현해 방법을 검증합니다. **5.65 년** 주기로
사이클링합니다 (Laliotis 2023. Lovis 2011 의 4.71 년과 일치).
다소 활동적인 노년 K 왜성인데, 측정된 X-ray 출력은 **정온 태양의
~3×** 입니다 (Wood 2005 RASS log L_X 27.39, Chen 2022 R_X −5.62 도
동의) — 차분한 나이에 비해 입자 환경이 매운 편입니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | 5.65 | high | Laliotis 2023 S-index (Lovis 2011 의 4.71 yr 과 1.5σ 안에서 일치) |
| `stellar_wind_mass_loss_solar` | 0.5 | high | Wood 2005 astrospheric Lyα (compact astrosphere) |
| `local_ism_inflow_speed_kms` | 68 | high | Wood 2005. 6D-측성 계산값 (69) 이 확인 |
| `astrosphere_standoff_au` | ~32 (compact) | high | 120·√0.5·(25.4/68). Wood 의 서술과 일치 |
| `stellar_radiation_surface_relative_sun` | ~3 | medium | 측정: log L_X 27.39 (Wood 2005 RASS) ≈ 태양 사이클 평균 26.9 의 3×. Chen 2022 R_X −5.62 가 독립적으로 같은 결론 |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~110 / +2 | low | 6D 측성 대 LIC. **plugin-only** |

## Open items for follow-up

- **행성 Phase 3 합성.** ε Indi A b 는 별도 Phase 3 문서 (`eps-ind-a-b.md`)
  로 만들며, Matthews 2024/2026 위에 정박합니다. 가장 가까운 직접 촬영
  차가운 슈퍼목성이자 시스템의 헤드라인 특징입니다.
- **갈색왜성 쌍 ε Indi B (DB 추가 대기).** Ba (T1–1.5, 66.9 M_Jup) +
  Bb (T6, 53.3 M_Jup), ~1459 AU (Chen 2022) 는 아직 NearStars 바디가
  아닙니다. 이들을 — Chen 2022 역학 질량과 Ba–Bb 상호 궤도와 함께 —
  추가하면 cfg 가 전체 ε Indi 계층적 삼중성계를 렌더링할 수 있습니다. 이
  합성에서 언급하되 여기서 DB 나 Phase 3 문서를 만들지는 않습니다.
- **나이.** Phase 2 나이 배열 없음. ~3.5 Gyr Chen 2022 활동 나이는 medium
  신뢰도의 literature-direct 값입니다. 미래 큐레이션이 자이로크로놀로지,
  측성지진, 운동학 나이를 추가하면 cfg 나이를 교체해야 합니다. 0.39–5 Gyr
  문헌 분포 (Lundkvist 2024) 가 잔여 불확실성입니다.
- **자전 주기 불확실도.** Feng 2018 은 "~35 d" 를 형식 σ 없이, RV-활동지표
  (비측광) 방법으로 보고합니다. TESS 나 전용 측광 자전 측정이 있으면 값과
  자이로크로놀로지 나이 교차검증을 다듬을 수 있습니다.
- **금속도.** 프로젝트 정책에 따라 스킵. 문헌 ≈ −0.17 (Lundkvist 2024).
  미래 cfg 가 금속도-적화 보정을 필요로 하면 값은 있으나, 고정 Teff 에서
  색 효과는 sub-perception 입니다.
- **활동-주기 시각화 충실도.** ~7.1 yr 태양형 주기 (Lundkvist 2024) 는
  느린 밝아짐 / spot-coverage 변조의 tie-break 시각 선택입니다. 렌더러가
  표현 가능해지면 주기-위상을 게임 epoch 에 맞춰 다듬습니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 표의 스키마 출처
- [eps-ind-a-b](eps-ind-a-b.md) — 가장 가까운 직접 촬영 차가운 슈퍼목성 (~7.6 M_Jup, ~20.9 AU). JWST 암모니아 + 물-얼음 구름
- [eps-eri](eps-eri.md) — 비교용 가까운 K 왜성 (K2 V). 확인된 거대 행성과 분해된 삼중-고리 원반을 가짐. ε Eri 의 시끄러운 활동 + 원반을 ε Indi A 의 조용하고 원반 없는 광구와 대비
- [40-eridani-a](40-eridani-a.md) — 비교용 가까운 K 왜성 (K0.5 V). 삼중성계 안에 있고 더 따뜻하며 비슷하게 조용함
- [alpha-centauri-b](alpha-centauri-b.md) — 비교용 K1 V 왜성으로 측성지진이 측정됨. ε Indi A 의 ν_max 가 둘 중 더 높음
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX 는 ε Indi A 의 기본 항성 엔트리만 가짐. 차가운 슈퍼목성과 갈색왜성-쌍 계층은 NearStars 추가분
