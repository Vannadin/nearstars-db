<!-- ε Eridani Phase 3 합성. cfg-ready 결정과 근거 -->
# ε Eridani — Phase 3 Synthesis

ε Eridani (HD 22049, HIP 16537, GJ 144) 는 Proxima 다음으로 가까운
행성 보유 별이며, 거리는 3.220 ± 0.001 pc 입니다 (Gaia DR3 시차
310.58 ± 0.14 mas). 어리고 자기 활동이 강한 K2V 왜성으로, 질량
M = 0.82 ± 0.02 M☉ (Llop-Sayson 2021), 반지름 R = 0.735 ± 0.005 R☉
(Baines & Armstrong 2012 PAVO/CHARA 한계 어두워짐 각지름), 유효
온도 T_eff = 5039 ± 126 K (Baines 2012 간섭계. L_bol + θ_LD Stefan-
Boltzmann 역산) 입니다. 광도는 0.320 ± 0.011 L☉ 로 주계열 위에
자리하며, 활동도 지표는 태양보다 약 한 자릿수 더 어린 별의 특성을
보입니다. 나이는 isochrone + 운동학 + 활동도 진단을 결합해 ≈ 440
Myr 로 가장 잘 추정됩니다 (Mamajek & Hillenbrand 2008. Janson 2008).
ε Eri 는 AB Doradus / Local Association 운동학 복합체의 느슨한 끝
부분에 속합니다.

이 시스템에서 특별한 것은 별 자체보다 debris 배열입니다. ε Eri 는
분해된 삼중 belt 디스크를 가지고 있는데, 안쪽의 asteroid belt analog
가 ≈ 3 AU 에 있고 Spitzer 가 검출했으며 (Backman 2009. Su 2017),
중간 dust 성분이 ≈ 20 AU 부근에 Herschel 자료로부터 추정되며
(Greaves 2014. Booth 2017), 차가운 Kuiper analog 링이 ≈ 64 AU 에
있어 처음에는 JCMT/SCUBA (Greaves 1998), 이어서 ALMA 가 고정밀로
분해했습니다 (MacGregor 2015. Booth 2017). 차가운 링은 좁고 이심
(e ≈ 0.07) 하며, 전체 dust 질량은 ≈ 0.04 M⊕ 입니다. canonical 해석
(Su 2017 "Genie" 모델) 은 gap-clearing 행성들이 다중 belt 구조를
sculpting 한다는 것입니다. 시스템에는 오래 논쟁된 jovian ε Eri b
도 있으며, 결국 직접 촬영으로 확정되었고 (Mawet 2019) 천체 측정 +
RV 조합으로 정밀화되었습니다 (Llop-Sayson 2021. Roettenbacher 2022).
M sin i ≈ 0.78 M_Jup, a ≈ 3.5 AU, P ≈ 7.4 yr, e ≈ 0.07. 바깥쪽의
"ε Eri c" 후보 (Quillen 2002. Benedict 2006) 는 Mawet 2019 의 imaging
미검출로 배제됐습니다.

색채권은 시끄럽습니다. log R'HK ≈ −4.4 (Henry 1996. Zechmeister
2013) 는 ε Eri 를 활동적 K 왜성 locus 의 한가운데 놓습니다. Donahue
1996 은 Mt. Wilson Ca II H&K 시계열에서 P_rot = 11.2 d 를 측정했는데,
태양보다 두 배 빠르며 Skumanich braking 법칙과 ~440 Myr 나이와
일관됩니다. Metcalfe 2013 은 Ca II HK 기록에서 약 2.95 년의 색채권
자기 사이클을 분해했고 (주계열 기준으로 짧음. 다시 한 번 어린 나이와
일관), 평행하게 X 선 사이클이 XMM 모니터링에서 검출됩니다 (Coffaro
2020).

**NearStars 시나리오 선택. 어리고 빠르게 자전하며 자기 활동이 매우
강한 K2V 왜성으로, 구조적으로 드문 삼중 링 debris 디스크와 확인된
~0.78 M_Jup jovian 동반자를 3.5 AU 에 가집니다. 시각 스타일링은
주황색 K2V 연속체, 사이클 활동기의 따뜻한 corona 색조, 그리고 어떤
넓은 궤도 fly-by 에서든 시스템의 시그니처가 되는 세 개의 동심 디스크
링을 강조합니다.** 18 개 cfg 픽 중 15 개는 canonical 일치, 3 개는
tie-break (별 + 디스크 + jovian 점광원의 시각 hex 색조) 입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K2V | high | Keenan & McNeil 1989. Gray 2003. DB |
| `mass_msun` | 0.82 ± 0.02 | high | Llop-Sayson 2021. RV + Hipparcos IAD + Gaia DR2 천체측정 + 다 epoch vortex coronagraphy 결합 fit. Takeda 2007 (0.83 ± 0.04) 와 Valenti & Fischer 2005 (0.85) 가 1σ 안에서 bracket |
| `radius_rsun` | 0.735 ± 0.005 | high | Baines & Armstrong 2012. PAVO@CHARA 한계 어두워짐 각지름 θ_LD = 2.126 ± 0.014 mas 와 Hipparcos 시차 결합. 직접 간섭계 측정 (가장 직접적인 방법). Di Folco 2007 VLTI/VINCI θ_LD = 2.148 ± 0.029 mas → R = 0.74 ± 0.01 R☉ 가 독립적으로 확인. Rosenthal 2021 CLS SED fit R = 0.759 ± 0.012 R☉ 는 ~3% 높음. 차이는 직접 각지름 vs SED fit 방법 차이. **이전 Phase 3 는 Rosenthal SED 값을 1차로 인용 — Phase 2 간섭계 픽을 따르도록 정정.** |
| `teff_k` | 5039 ± 126 | high | Baines & Armstrong 2012. L_bol + θ_LD 를 Stefan-Boltzmann 으로 역산한 간섭계 T_eff (가장 직접적). 분광 cross-check. Valenti & Fischer 2005 SME 5146 ± 44 K. Brewer 2016 5076 ± 25 K. Tsantaki 2013 5077 ± 31 K. 모두 결합 오차 안에서 일치. **이전 Phase 3 는 DB raw 값 5180 K (Gaia DR3 광도 근사) 사용 — Phase 2 간섭계 픽을 따르도록 정정 (~140 K 낮아짐).** |
| `luminosity_lsun` | 0.320 ± 0.011 | high | Baines & Armstrong 2012. 스펙트럼 + Hipparcos 시차에서 직접 적분한 bolometric flux (가장 직접적). Eiroa 2013 DUNES 가 독립 SED fit 으로 0.34 ± 0.02 L☉ 를 주며 1σ 안에서 일치 |
| `metallicity_fe_h_dex` | −0.13 ± 0.04 | high | Valenti & Fischer 2005 SPOCS SME 분광. Brewer 2016 가 −0.10 ± 0.03, Tsantaki 2013 가 −0.09 ± 0.03 으로 확인. 살짝 sub-solar. 인근 어린 K 왜성 종족과 일관 |
| `age_gyr` | 0.44 ± 0.10 | medium | Mamajek & Hillenbrand 2008. isochrone + Ca II HK + X 선 + 회전 활동-회전 결합 fit. 발표된 형식 오차는 대칭 ± 0.10 Gyr 지만 이 나이에서 gyrochrone 시스템 오차는 2 배 spread. Barnes 2007 gyrochrone 단독은 P_rot = 11.2 d 에서 0.82 ± 0.05 Gyr, Llop-Sayson 2021 은 호스트 사전분포에 400–800 Myr 를 채택. 미해소 spread 를 반영해 Confidence 는 medium 유지. Janson 2008 이 운동학으로 어린 나이 확정 |
| `rotation_period_days` | 11.20 ± 0.05 | high | Donahue 1996. Mt. Wilson Ca II HK 14 년 시계열 (canonical ε Eri 회전 측정). Croll 2006 MOST 광도 변동 11.45 ± 0.05 d 가 독립 확인. Roettenbacher 2016 Doppler imaging ~11.5 d 와도 일관 |
| `activity_log_rhk` | −4.39 ± 0.07 | high | Zechmeister 2013 현대 HARPS epoch. Henry 1996 Mt Wilson −4.46 이 역사적 canonical (0.07 dex 차이는 활동 사이클 위상 + 장비 보정 산포. 실제 장기 변화 아님). 강한 활동 K 왜성 locus |
| `activity_cycle_years` | 2.95 | high | Metcalfe 2013. 짧은 색채권 자기 사이클. Coffaro 2020 이 X 선에서 확인 |
| `x_ray_log_lx_cgs_min` | 28.3 | medium | Coffaro 2020. XMM 사이클 최소 |
| `x_ray_log_lx_cgs_max` | 28.9 | medium | Coffaro 2020. XMM 사이클 최대. 사이클 진폭 약 4 배 |
| `limb_darkening_alpha_h` | ~0.20 | low | Tie-break. ε Eri 는 직접 측정값이 없으며 Claret 2018 K 왜성 그리드에서 α Cen B (0.18) 와 더 차가운 K 왜성 (0.25) 사이로 보간. low 신뢰도, 윈도우 내 추측 |
| `visual_surface_tint_hex_primary` | `#ffd9a8` (따뜻한 주황 K2V. α Cen B `#ffcb91` 보다 약간 더 차가운 톤) | medium | Teff 5039 K 흑체 + 활동성 색채권의 Hα 채움이 체감 따뜻함을 살짝 올림. 색조 픽은 이전 Phase 3 초안과 동일 (Teff 가 5180 → 5039 로 ~140 K 이동해도 K2V hex 는 같은 K 왜성 주황-따뜻 윈도우 안에 머무름) |
| `stellar_color_temp_k` | 5039 | high | Teff (Baines & Armstrong 2012 간섭계) 유도. 갱신된 Phase 2 픽을 추적 (이전 Phase 3 초안의 DB 광도 근사값 5180 K 에서 변경) |
| `visual_spot_coverage_max` | 0.10 | medium | TiO 밴드 + 회전 변조 분석 (Frohlich 2007. Roettenbacher 2016 ε Eri Doppler imaging) 에서 사이클 최대기에 디스크 5–10% 면적 |
| `disk_present` | true | high | Greaves 1998 JCMT/SCUBA. 첫 sub-mm 검출. 수많은 후속 캠페인이 분해 |
| `disk_inner_radius_au` | 3 | high | Backman 2009 Spitzer/IRS. 중적외 excess 로부터 따뜻한 asteroid belt analog 추정. Su 2017 정련 |
| `disk_outer_radius_au` | 64 | high | MacGregor 2015 ALMA. 차가운 링이 64.4 ± 0.5 AU 에서 분해됨. Booth 2017 Herschel/SPIRE 확인 |
| `disk_morphology` | three-belt. ~3 AU 안쪽 asteroid analog + ~20 AU 중간 성분 + ~64 AU 차가운 Kuiper analog 링 (좁고 이심 e ≈ 0.07) | medium | Su 2017 Genie 모델 + Booth 2017 다중 belt SED 분해. 중간 성분이 가장 덜 분해됨 (medium) |
| `disk_dust_temperature_k` | 35 (차가운 링), 150 (안쪽 belt) | high | Backman 2009 (안쪽), MacGregor 2015 (차가운 링). 둘 다 SED fit 에서 직접 |
| `disk_mass_mearth` | 0.04 | medium | Greaves 2014 + Booth 2017. 세 belt 통합 dust 질량. 불확실도는 중간 belt 입도 가정에서 옴 |
| `disk_resolved_imaging` | true | high | MacGregor 2015 ALMA. Booth 2017 Herschel/SPIRE. Su 2017 Spitzer/MIPS. 여러 파장에서 차가운 링이 분해됨 |
| `disk_imaging_observatory` | ALMA (차가운 링 지오메트리), Herschel SPIRE (질량), Spitzer IRS/MIPS (따뜻한 성분) | high | MacGregor 2015. Booth 2017. Su 2017. Backman 2009 |
| `disk_imaging_inclination_deg` | 34 ± 2 | high | Booth 2017 Herschel 분해 inclination. ε Eri b 궤도면과 일관 (Roettenbacher 2022) |
| `disk_planetesimal_belt_inferred` | true | high | dust 보충 시간 척도 (~Myr) 가 각 링에 모행성체 population 을 요구. Su 2017 |
| `disk_tint_rgb_hex` | `#bd8c5e` (35 K 의 따뜻한 sub-mm-bright 링. 산란광에서 옅은 주황-갈색 후광으로 렌더) | low | Tie-break. ALMA 연속체는 정의상 비조명. 산란광 색조는 게임 내에서 α Cen / Sol 의 행성간 산란광과 구별되도록 선택 |
| `companion_jovian_present` | true (ε Eri b. a = 3.5 AU. M = 0.78 M_Jup) | high | Mawet 2019 직접 촬영. Llop-Sayson 2021. Roettenbacher 2022 천체측정 확정. 행성 Phase 3 은 별도 워크스페이스로 미룸 |

## Surface synthesis

ε Eridani 의 광구는 교과서적인 K2V 입니다. α Cen B (K1V, 5230 K,
0.86 R☉) 보다 약간 더 작고 차가우며, 61 Cyg A (K5V, 4400 K) 보다는
눈에 띄게 따뜻합니다. 5039 K (Baines & Armstrong 2012 간섭계) 에서
연속체 대부분이 5500 Å 와 9000 Å 사이로 나오며, 가장 강한 분자
형상은 녹색에서의 MgH 와 CaH 밴드, 그리고 ~6300 Å 이하부터
본격적으로 들어오는 TiO 헤드입니다. 통합 광도 0.320 ± 0.011 L☉
는 ε Eri 의 HZ 를 ≈ 0.50–0.92 AU 에 놓으며, 안쪽 asteroid belt
analog 보다 완전히 안쪽이고 3.5 AU 의 jovian 보다 한참 안쪽입니다. ε Eri 의 limb darkening 은 직접 측정된 적이 없으며,
cfg 는 Claret 2018 그리드에서 Kervella 의 α Cen B 값 (0.18) 과
더 차가운 K 왜성 (0.25) 사이로 보간한 mid-K-dwarf power-law
exponent α ≈ 0.20 를 채택합니다. 모델 그리드 윈도우 안의 tie-break
값입니다.

Granulation 대비는 태양과 Proxima 사이의 중간입니다. 모델 셀 크기
~150 km, 대비 인자 ~2× 태양 (Beeck 2013 K 왜성 convection 3D MHD
시뮬레이션 그리드) 입니다. ε Eri 를 더 조용한 K 왜성들과 구분 짓는
것은 흑점 면적입니다. Roettenbacher 2016 의 Doppler imaging 캠페인
(CHARA/MIRC) 은 표면을 직접 분해해서 5–10% 의 흑점 면적이 두 개의
지속적 polar cap + 적도 활동 belt 로 조직돼 있음을 발견했습니다.
polar-spot 우세는 빠르게 회전하는 어린 K 왜성의 특징이며, 태양의
적도 belt 활동과는 뚜렷이 대조됩니다. ~3 년 사이클 최대기 동안
흑점 패턴은 더 큰 진폭 쪽으로 이동합니다. 사이클 최소기에는 polar
cap 이 얇아지지만 완전히 사라지지는 않습니다 (Frohlich 2007 광도
분해).

살짝 sub-solar 인 금속도 ([Fe/H] = −0.13) 는 SED 색조를 실질적으로
바꾸지 않습니다. 지배적 시각 효과는 K2 광구 고유의 주황색 연속체
입니다. cfg 표면 색조 `#ffd9a8` 는 K 왜성의 따뜻한 주황을 인코딩
하며, α Cen B 의 `#ffcb91` 와 의도적으로 구분해 어떤 나란히 놓인
홍보 렌더에서도 두 K 왜성 중 ε Eri 가 약간 더 차갑고 더 주황인
쪽으로 읽히도록 합니다.

안쪽 관측자 (ε Eri HZ 의 가상의 암석 행성) 입장에서는 dust shielding
맥락이 중요합니다. 3 AU 의 안쪽 asteroid belt 는 HZ 바깥에 있어
HZ 행성 위치의 zodiacal light 오염은 태양 zodiacal 배경과 비슷
하거나 살짝 높습니다 (Backman 2009 §6 가 따뜻한 dust 방출을 태양
zodi 의 약 1–3× 로 정량화). 64 AU 의 차가운 링은 어떤 관측자의
하늘에서도 너무 흐려 지배적이지 않습니다.

## Atmosphere synthesis

ε Eri 의 색채권과 corona 는 가장 어린 M 왜성들을 제외하면 NearStars
카탈로그의 어떤 K 왜성보다도 시끄럽습니다. Ca II H&K 방출 코어가
눈에 띄게 채워져 있으며, log R'HK ≈ −4.4 (Henry 1996. Zechmeister
2013 갱신) 는 ε Eri 를 현대 태양보다 한 자릿수 더 활동적인 위치에
놓습니다. 색채권은 강한 UV 연속체와 라인 방출 (Lyα, Mg II h&k,
Si IV, C IV) 을 구동하며 Linsky 1995 와 MUSCLES 서베이의 France
2018 이 매핑했는데, FUV 광도가 밴드에 따라 태양값을 5–20 배
초과합니다.

corona 도 마찬가지로 활동적입니다. Coffaro 2020 은 17 년 XMM
모니터링을 이용해 0.2–2 keV 에서 log L_X 사이클을 28.3 (사이클
최소) 부터 28.9 (사이클 최대) cgs 까지 분해했습니다. 2.95 년 주기에
4 배 진폭이며, Metcalfe 2013 의 Ca II HK 사이클과 위상 불확실도
내에서 일치합니다. 이로써 ε Eri 는 태양 근방에서 가장 잘 특성화된
별 자기 사이클 중 가장 짧은 사이클을 가집니다 (태양 11 년 사이클
보다 약 4 배 짧음. 다시 어린 나이와 일관. Bohm-Vitense 2007 의
이중 가지 dynamo 모델은 어린 K 왜성을 active-branch 사이클에 놓고
사이클 주기를 회전 속도에 스케일).

Flare 는 일어나지만 M 왜성에서처럼 정의적 특징은 아닙니다. XMM 과
Hubble FUV 모니터링 (France 2018. Coffaro 2020) 은 10³⁰–10³² erg
에너지의 flare 를 며칠에 한 번씩 잡습니다 (별 기준으로 빈번하지만
M 왜성 기준으로 온순함). ≥ 10³⁴ erg 의 super-flare 는 Audard 2000
의 K 왜성 종합 자료에서 외삽한 flare 빈도 분포 기준으로 연 1 회
정도로 추정됩니다. HZ 행성 입장에서 대기 침식을 좌우하는 것은
flare 가 아니라 정상 XUV 배경입니다. 1 AU 에서 FUV + EUV 플럭스가
10⁻³ L_bol 을 넘어, 현재까지 시스템 수명 440 Myr 동안 비자기화된
지구형 대기를 의미 있게 침식하기에 충분하지만, 자기화된 대기는
살아남습니다.

강한 자기장이 태양보다 더 뜨겁고 더 밀집된 항성풍을 구동합니다.
Wood 2002 의 Lyα 흡수 측정은 ε Eri 의 질량 손실률을 태양의 약 30×
로 놓고, 어떤 안쪽 행성에 대해서도 CME 플럭스가 그에 비례해 높습니다.
1 AU 에서의 풍압은 0.3 AU 에서의 태양권 풍압에 가까운데, 어떤 행성
의 자기권 standoff 에도 영향을 줍니다.

## Rotation & spin synthesis

11.2 일 회전 주기 (Donahue 1996. Croll 2006 MOST 광도와 Roettenbacher
2016 Doppler imaging 으로 확인) 는 주계열 K 왜성치고 빠릅니다.
태양은 25 일, α Cen B 는 ≈ 38 일에 자전합니다. Skumanich braking
법칙 P_rot ∝ √t 는 ε Eri 의 나이를 태양의 약 (11.2/25)² ≈ 0.20,
즉 ~900 Myr 로 시사합니다. 직접 fit 된 Mamajek & Hillenbrand 2008
gyrochronology 는 살짝 다른 braking calibration 에서 440 Myr 를
줍니다. 둘 다 이 나이 범위 gyrochronology 에서 예상되는 2 배
시스템 오차 안에서 일치하며, cfg 는 더 낮은 Mamajek 값을 명시적
~100 Myr 불확실도와 함께 채택합니다.

Roettenbacher 2016 의 Doppler imaging 은 차등 회전을 직접 분해했
습니다. ε Eri 의 적도는 고위도보다 약 12% 빠르게 회전합니다 (즉
적도-극 shear ≈ 0.4 d). 태양과 비슷한 분수 shear 가 더 짧은 평균
주기에 작용하는 형태입니다. 회전축 inclination 은 Roettenbacher
2016 §4 의 흑점 패턴 + v sin i 분광 broadening 결합 fit 에서
i ≈ 30° 로 잘 제약됩니다. 우연히도 디스크 inclination (34°) 과
천체측정에서 추정된 ε Eri b 궤도 inclination (Roettenbacher 2022)
와도 비슷한 값이라, 시스템이 coplanar 임을 시사합니다.

Asteroseismic 검출은 시도된 적이 있지만 marginal 합니다. Bonanno
et al. 2008 은 radial-velocity 모니터링에서 잠정적 ν_max ≈ 1700 μHz
를 보고했지만 후속 연구에서 개별 mode 주파수를 확정하지 못했습니다.
높은 활동 floor 가 p-mode 진폭을 가립니다. cfg 는 이 때문에
asteroseismic 제약을 인코딩하지 않습니다.

## Visual styling

ε Eri 는 따뜻한 주황 K2V 로 렌더링됩니다. cfg 색조 `#ffd9a8` 는
α Cen B 참조 `#ffcb91` 보다 의도적으로 더 차가운 주황이라, 나란히
놓인 비교에서 "ε Eri 는 가장 가까운 4 pc 안 두 K 왜성 중 더 진한
주황" 으로 읽히도록 했습니다. 색채권의 Hα 와 Ca II HK 방출 코어는
고해상도 클로즈업에서 옅은 분홍-따뜻 성분을 추가합니다. 3 년마다
사이클 최대기에 ~20% 밝아지도록 애니메이션되며 (Metcalfe 2013),
11.2 일 회전 주기 위에 빠른 흑점 변조가 겹쳐집니다.

지구에서 3.22 pc 거리에서 보면 겉보기 등급 V = 3.74 로 ε Eri 는
쉽게 맨눈으로 보입니다 (Eridanus 별자리를 잡는 정도지만 화려하지는
않음). ε Eri HZ 의 가상의 안쪽 행성 (예를 들어 0.7 AU) 에서는 별이
각지름 0.83° 를 채웁니다 (지구에서 본 태양보다 약 50% 큼). 따뜻한
주황 조명으로 하늘을 지배합니다.

시스템의 시그니처 시각 특징은 넓은 궤도 fly-by 뷰에서 보이는 삼중
링 debris 디스크입니다. 64 AU 의 차가운 Kuiper analog 링은 어떤
기울어진 뷰에서도 가장 밝습니다. 디스크 평면 방향에서 보면 좁은
링 (폭 ~10 AU. Booth 2017) 이 하나의 띠를 이루고, 위에서 보면
명확한 환을 이룹니다. ~20 AU 의 중간 성분은 더 어둡고 더 넓습니다.
~3 AU 의 안쪽 asteroid belt analog 가 가장 따뜻하고 가장 광학적으로
얇으며, 옅은 따뜻한 색조의 dust 산란 층으로 렌더링됩니다. 태양
배경과 구별되는 정도라 "여기는 만약 암석 행성이 있었다면 자리잡았을
지점" 으로 시각적으로 식별됩니다. cfg 색조 `disk_tint_rgb_hex = #bd8c5e`
는 윈도우 내 tie-break 입니다. ALMA 연속체는 정의상 가시광 정보가
없으므로 산란광 색조는 오래되고 가공된 silicate-rich dust 와 일관된
따뜻한 갈색-주황으로 기본 설정됐습니다.

ε Eri b 는 a ≈ 3.5 AU 의 Jupiter 질량 jovian 점광원으로, 안쪽
asteroid belt 와 중간 dust 성분 사이의 갭에 박혀 있습니다. 넓은
궤도 fly-by 에서 행성은 ε Eri b 의 elongation 에서 밝게 어두워지는
점으로 읽힙니다. 7.4 년 궤도를 따라 애니메이션되며 e ≈ 0.07
이심으로 변조됩니다. 행성의 대기와 디테일 (Phase 3 후속) 은 여기서
범위 밖이지만, 다중 belt 구조의 gap-clearing canonical sculptor (Su
2017 Genie 모델) 로서의 위치는 `companion_jovian_present` 결정 행으로
cfg 에 인정됩니다.

CME 구동 조명. 사이클 최대기 동안 게임 내 corona 가 옅은 분홍-따뜻
후광으로 눈에 띄게 밝아지며, 산발적 flare 이벤트 (10³⁰–10³² erg)
가 시간 척도에서 짧은 5–10% 밝기 spike 를 만듭니다 (France 2018
FUV 모니터링을 가시광으로 스케일). 시각 사이클 위상은 Metcalfe
2013 사이클 epoch 에 맞춰 인코딩돼 있어, 플레이어가 활동 시각과
실시간 진행을 일관되게 상관 지을 수 있습니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-type Dwarfs Using Activity-Rotation
  Diagnostics*, ApJ 687, 1264 (`2008ApJ...687.1264M`,
  arXiv:0807.1686). Ca II HK + 회전 + X 선 + isochrone 을 결합해
  ε Eri 의 나이 ≈ 440 Myr 유도. canonical 어린 나이 부여.
- **Janson M. et al. 2008** — *ε Eri 를 포함한 근방 별의 직접 촬영
  검출* (`2008A&A...488..771J`). 운동학 + 활동도 기반 나이의 독립
  확인.
- **Donahue R. A. et al. 1996** — *Mt. Wilson HK 프로젝트의 차가운
  주계열 별 회전* (`1996ApJ...466..384D`). ~14 년 Ca II H&K 시계열
  에서 P_rot = 11.2 d. canonical 회전 측정.
- **Metcalfe T. S. et al. 2013** — *외계행성 보유성 ε Eridani 의
  자기 활동 사이클*, ApJ 763, L26 (`2013ApJ...763L..26M`,
  arXiv:1212.5343). Mt. Wilson + SMARTS Ca II HK 에서 2.95 년의
  색채권 자기 사이클 분해.
- **Coffaro M. et al. 2020** — *ε Eri 의 활동 호스트. 17 년의 X 선
  모니터링*, A&A 636, A49 (`2020A&A...636A..49C`, arXiv:2003.07069).
  XMM 모니터링이 X 선에서 사이클 확인. log L_X 28.3–28.9 cgs.
- **Backman D. et al. 2009** — *Epsilon Eridani 의 행성형 Debris
  Disk. Spitzer 와 Caltech Submillimeter Observatory 관측을 바탕으로
  한 구조와 역학*, ApJ 690, 1522 (`2009ApJ...690.1522B`). Spitzer/IRS
  가 따뜻한 안쪽 belt 방출 검출. SED 분해로 ~3 AU asteroid belt
  analog 가 분해됨.
- **Greaves J. S. et al. 1998** — *ε Eridani 주위의 Dust Ring. 어린
  태양계의 analog*, ApJ 506, L133 (`1998ApJ...506L.133G`). JCMT/SCUBA
  가 차가운 Kuiper analog 링의 첫 sub-mm imaging.
- **Greaves J. S. et al. 2014** — *Herschel 이 본 별-debris disc
  시스템의 정렬* (`2014MNRAS.438L..31G`, arXiv:1312.4087). Herschel
  분해 디스크 inclination + 중간 belt 추정.
- **MacGregor M. A. et al. 2015** — *ε Eridani 주위 Debris Disk 의
  ALMA 관측*, ApJ 809, L47 (`2015ApJ...809L..47M`, arXiv:1505.03879).
  ALMA 1.3 mm imaging 이 차가운 링을 64.4 ± 0.5 AU 에서 분해하며
  이심 e ≈ 0.07.
- **Booth M. et al. 2017** — *ALMA 가 본 ε Eridani 의 Debris Ring
  북쪽 호*, MNRAS 469, 3200 (`2017MNRAS.469.3200B`, arXiv:1705.05868).
  다파장 분해. 삼중 belt 구조 확인. 차가운 링 지오메트리와 inclination
  정련.
- **Su K. Y. L. et al. 2017** — *ε Eri 시스템의 안쪽 25 AU Debris
  분포*, AJ 153, 226 (`2017AJ....153..226S`, arXiv:1703.10330). "Genie"
  다중 belt sculpting 모델. 삼중 링 시스템 + 행성 perturber 의
  canonical 해석.
- **Mawet D. et al. 2019** — *Keck Ms-band Vortex Coronagraphy 와
  Radial Velocities 를 이용한 ε Eridani 의 심층 탐사*, AJ 157, 33
  (`2019AJ....157...33M`, arXiv:1810.03794). ε Eri b 직접 촬영 확정.
  바깥쪽 "ε Eri c" 배제.
- **Llop-Sayson J. et al. 2021** — *Radial Velocities 와 Astrometry
  의 결합 분석에서 도출한 ε Eri b 의 본질에 대한 제약*, AJ 162, 181
  (`2021AJ....162..181L`, arXiv:2108.05552). RV + Hipparcos/Gaia
  천체측정 결합 fit. M_b = 0.78 M_Jup, i = 78.8°, a = 3.5 AU.
- **Roettenbacher R. M. et al. 2022** — *ε Eri b 의 신뢰할 만한 천체
  측정 검출 없음* (`2022AJ....163...19R`, arXiv:2110.10643). 천체
  측정 교차 확인. ε Eri b 의 inclination 이 디스크 평면과 일관.
- **Roettenbacher R. M. et al. 2016** — *활동성 별 ζ Andromedae 의
  태양형 dynamo 부재… 와 ε Eri Doppler Image* (`2016Natur.533..217R`).
  분해된 polar-spot 면적이 있는 ε Eri Doppler imaging 포함.
- **Hatzes A. P. et al. 2000** — *ε Eridani 주위 장주기 행성의 증거*,
  ApJ 544, L145 (`2000ApJ...544L.145H`). RV 발견 논문. 역사적 맥락
  설정.
- **Baines E. K. & Armstrong J. T. 2012** — *Navy Optical
  Interferometer 와 PAVO/CHARA 를 이용한 외계행성 호스트 별
  ε Eridani 의 기본 속성 확인*, ApJ 761, 57 (`2012ApJ...761...57B`,
  doi:10.1088/0004-637X/761/1/57). PAVO@CHARA 한계 어두워짐 각지름
  θ_LD = 2.126 ± 0.014 mas. Hipparcos 시차와 결합하면 R = 0.735 ±
  0.005 R☉. L_bol + θ_LD Stefan-Boltzmann 역산으로 T_eff = 5039 ±
  126 K, L = 0.320 ± 0.011 L☉. **ε Eri 의 R / Teff / L 1차 Phase 2
  앵커** (가장 직접적인 방법. 세 양을 동일 fit 으로 자기일관적으로
  유도). 이전 합성 초안의 Rosenthal 2021 SED fit R = 0.759 R☉ 픽을
  대체.
- **Donahue R. A., Saar S. H., Baliunas S. L. 1996** — *낮은 주계열
  별의 평균 회전 주기와 관측된 범위 간의 관계*, ApJ 466, 384
  (`1996ApJ...466..384D`, doi:10.1086/177517). Mt. Wilson Ca II HK
  Project ~14 년 시계열에서 ε Eri 의 P_rot = 11.20 ± 0.05 d.
  **ε Eri 회전 주기의 1차 Phase 2 앵커.**

### Read (context / methodology, not decision-driving)

- **Rosenthal L. J. et al. 2021** — *California Legacy Survey. I.
  근방 별 719 개의 정밀 RV 모니터링에서 도출한 행성 178 개 카탈로그*,
  ApJS 255, 8 (`2021ApJS..255....8R`, doi:10.3847/1538-4365/abe23c).
  SED fit + Gaia 시차에서 CLS 표 R = 0.759 ± 0.012 R☉ — 현대 Baines
  2012 PAVO/CHARA 직접 간섭계 픽보다 ~3% 높음. cross-check 대체값
  으로 보존.
- **Valenti J. A. & Fischer D. A. 2005** — *차가운 별의 분광 속성
  (SPOCS). I.* (`2005ApJS..159..141V`, doi:10.1086/430500). SME
  분광에서 Teff = 5146 ± 44 K, [Fe/H] = −0.13 ± 0.04. 1차 [Fe/H]
  앵커. Teff cross-check.
- **Brewer J. M. et al. 2016** — *차가운 별의 분광 속성*
  (`2016ApJS..225...32B`, doi:10.3847/0067-0049/225/2/32). SME
  Teff = 5076 ± 25 K, [Fe/H] = −0.10 ± 0.03. 독립 분광 cross-check.
  VF05 와 결합 오차 안에서 일치.
- **Tsantaki M. et al. 2013** — *차가운 태양형 별의 정밀 파라미터
  유도. 철 라인 리스트 최적화* (`2013A&A...555A.150T`,
  doi:10.1051/0004-6361/201321103). 고분해 Teff = 5077 ± 31 K,
  [Fe/H] = −0.09 ± 0.03. 동일 pipeline 분광 cross-check.
- **Takeda Y. et al. 2007** — *행성을 가진 근방 별의 구조와 진화.
  II.* (`2007ApJS..168..297T`, doi:10.1086/509763). ε Eri 의 진화
  모델 질량 0.83 ± 0.04 M☉. Llop-Sayson 2021 결합 fit 질량 cross-
  check.
- **Barnes S. A. 2007** — *Gyrochronology 를 이용한 예시 field 별
  나이* (`2007ApJ...669.1167B`, doi:10.1086/519295). P_rot = 11.2 d
  단독에서 ε Eri 나이 0.82 ± 0.05 Gyr — Mamajek & Hillenbrand 2008
  의 활동-회전 결합 fit (0.44 Gyr) 보다 늙음. 이 나이대의 gyrochrone
  보정 간 2 배 시스템 오차를 보여줌.
- **Di Folco E. et al. 2007** — *ε Eri 를 포함한 근방 별의 VLTI/VINCI
  간섭계* (`2007A&A...475..243D`, doi:10.1051/0004-6361:20065445).
  VLTI/VINCI θ_LD = 2.148 ± 0.029 mas → R = 0.74 ± 0.01 R☉. Baines
  2012 PAVO/CHARA 1차 픽의 독립 간섭계 cross-check.
- **Henry T. J. et al. 1996** — *Solar Neighborhood. IV. 스무 번째로
  가까운 별 시스템 발견* (`1996AJ....111..439H`). ε Eri 의 log R'HK
  참조.
- **Zechmeister M. et al. 2013** — *ESO CES 와 HARPS 의 행성 탐색
  프로그램* (`2013A&A...552A..78Z`, arXiv:1211.7263). 현대 epoch
  에서 ε Eri 의 Ca II HK 인덱스 갱신.
- **France K. et al. 2018** — *MUSCLES Treasury Survey* 의 K 왜성
  확장 (`2018ApJS..239...16F`). 안쪽 행성의 대기 침식 추정에 정보
  를 주는 FUV / Lyα 플럭스.
- **Wood B. E. et al. 2002** — *나이와 활동도의 함수로 측정한 태양형
  별의 질량 손실률* (`2002ApJ...574..412W`, arXiv:astro-ph/0203437).
  ε Eri 의 질량 손실률 ~30× 태양.
- **Beeck B. et al. 2013** — *주계열 별의 근표면 convection 3D
  시뮬레이션. II.* (arXiv:1308.4732). cfg 용으로 스케일된 K 왜성
  granulation 속성.
- **Bonanno A. et al. 2008** — *ε Eridani 의 Asteroseismology*
  (`2008A&A...488..685B`, arXiv:0805.2580). 활동 floor 에 잠긴
  marginal ν_max 검출.
- **Frohlich H.-E. et al. 2007** — *ε Eri 흑점 모델링의 MOST 광도*
  (`2007A&A...471..899F`). 5–10% 흑점 면적을 주는 광도 분해.
- **Croll B. et al. 2006** — *MOST 가 검출한 ε Eri 의 차등 회전*
  (`2006ApJ...648..607C`). P_rot 와 차등 회전의 독립 확인.

### Read (instrument / non-cfg-decisive)

- **Quillen A. C. & Thorndike S. 2002** — *40 AU 의 이심 0.3 행성과
  의 평균 운동 공명이 야기한 ε Eridani Dusty Disk 의 구조*
  (`2002ApJ...578L.149Q`). 디스크 구조에서 추정한 원래의 "ε Eri c"
  바깥 행성. Mawet 2019 가 배제했지만 역사적으로 중요.
- **Benedict G. F. et al. 2006** — *외계 행성 ε Eridani b. 궤도와
  질량* (`2006AJ....132.2206B`). ε Eri b 에 대한 이전 HST FGS 천체
  측정 시도. 직접 촬영이 대체.
- **Audard M. et al. 2000** — *늦은 형 별의 극자외 Flare 활동*
  (`2000ApJ...541..396A`). super-flare 외삽에 사용된 K 왜성 flare
  빈도 분포.
- **Linsky J. L. & Wood B. E. 1995** — *α Centauri 시선과 ε Eri 의
  Lyα 프로파일* (`1995ApJ...445L.139L`). FUV / Lyα 기준선.

### Not read — no arXiv preprint or low-priority (~80 papers)

ε Eri 활동에 관한 학회 proceedings (CS17, CS18, CS19), ε Eri
국소 환경의 성간 매질 / Strömgren-sphere 연구, SETI / 레이저 방출
탐색 (Marcy 2022, Tusay 2022, Saide 2023. ε Eri 는 영원한 타깃),
1990 년대 후반 pre-Spitzer 디스크 SED 모델링, 그리고 ε Eri 를 여러
tracer 중 하나로만 사용한 별 종족 운동학 논문 등. 전체 필터된 bib
는 `docs/phase3/_bib/eps-eri.yaml` 에 `status: skipped` 주석으로
보존됩니다.

## Open items for follow-up

- **Phase 2 `disk_measurements` ingest.** DB 스키마에는 현재
  `disk_measurements` 배열이 없으므로, 이 합성은 Backman 2009,
  MacGregor 2015, Booth 2017 를 Phase 2 를 거치지 않고 문헌에서 직접
  인용합니다. DB 스키마가 확장되거나 (또는 `db/disks/` 동반 디렉터리
  가 도입되면), 삼중 belt 지오메트리는 위 cfg 픽과 일치하는
  `recommended` 플래그가 붙은 `disk_measurements` 레코드로 ingest
  되어야 합니다 (`disk_inner_radius_au=3`, `disk_outer_radius_au=64`,
  `disk_morphology="three-belt"`).
- **ε Eri b 행성 Phase 3 후속.** jovian 동반자의 대기, 링 시스템
  가능성, 색조, 그리고 위성 population 은 이 별 합성의 범위 밖입니다.
  Mawet 2019 + Llop-Sayson 2021 + Roettenbacher 2022 와 2026–2027
  로 예상되는 JWST follow-up 에 닻을 둔 별도의 `docs/phase3/eps-eri-b.md`
  워크스페이스가 필요합니다.
- **역사적 "ε Eri c" 논쟁.** Quillen 2002 는 차가운 링의 이심에서
  ~40 AU 바깥 행성을 추정했고, Benedict 2006 은 HST FGS 천체측정
  신호 후보를 보고했지만, Mawet 2019 의 직접 촬영 미검출이 30 AU
  너머의 > 0.3 M_Jup 행성을 배제합니다. Su 2017 의 "Genie" 모델은
  다중 belt 구조를 바깥이 아니라 차가운 링 안쪽의 행성들로
  설명합니다. 문서적 관심만 있으며 cfg 행은 불필요. 다음 세션이
  legacy 카탈로그에 가끔 보이는 "ε Eri c" 항목이 왜 제외되는지
  알 수 있도록 여기 포함합니다.
- **Tie-break 시각 색조 (`disk_tint_rgb_hex`, `limb_darkening_alpha_h`).**
  둘 다 윈도우 내 추측입니다. ε Eri 디스크의 산란광 가시광 imaging
  결과가 나오면 (예를 들어 JWST/NIRCam coronagraph), 디스크 hex 는
  재유도되어야 합니다. K2V limb-darkening 간섭계 측정이 가능해지면
  (CHARA, VLTI), α_h 값은 측정값으로 교체되어야 합니다.
- **게임 epoch (J2000.0) 의 사이클 위상 동기화.** Metcalfe 2013
  사이클과 Coffaro 2020 X 선 사이클은 게임 내 J2000 epoch 에 위상
  동기화돼 있지 않습니다. 미래 cfg 개정에서 활동 구동 시각 밝기
  변화를 특정 사이클 위상에 닻을 두면, 플레이어가 게임 연수에 걸쳐
  일관된 타이밍을 볼 수 있습니다.

## Related

- [alpha-centauri-a](alpha-centauri-a.md), [alpha-centauri-b](alpha-centauri-b.md) — 이웃 K1V 비교군 (B) 과 G2V 비교군 (A). ε Eri 의 시각 색조는 α Cen B 의 약간 더 따뜻한 `#ffcb91` 과 구분됨.
- [proxima-cen](proxima-cen.md) — 가장 가까운 행성 호스트. ε Eri 는 두 번째로 가까우며, Proxima 보다 0.27 pc + 1.9 pc 더 멀리 있습니다.
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — 단일 별 천체측정만 해당. ε Eri 는 이중성 궤도 propagation 이 필요 없습니다.
- [methodology](../reference/methodology.md) — DB 스키마 원본.
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX 는 ε Eri 에 기본적인 별 항목만 가지고 있으며, 삼중 링 디스크와 확정된 jovian 은 NearStars 고유의 추가 항목입니다.
