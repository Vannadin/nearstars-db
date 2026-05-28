<!-- 40 Eridani C Phase 3 합성. cfg-ready 결정과 근거 -->
# 40 Eridani C — Phase 3 Synthesis

40 Eridani C (GJ 166 C, HIP 19849 C, 변광성 명 DY Eri) 는 40 Eri 삼중계의
M4.5 Ve 플레어성 구성원입니다. 태양에서 5.01 pc 떨어져 있으며, DA2.9
백색왜성 40 Eri B 와 230.09 년 주기의 시각-분광 궤도를 그립니다 (Mason,
Hartkopf & Miles 2017, e = 0.4300, a = 6.93″, 평균 분리 ≈ 33 AU). 안쪽
BC 짝은 다시 K0.5 V 주성 40 Eri A 주위를 약 83″ 의 각분리로 돕니다.
미해결된 약 8000 년 외궤도입니다 (Tokovinin MSC 2018). V = 11.17, 수십
분의 일 등급 시각 변광을 가진 C 는 가장 가까운 광학 활동성 M 왜성 중
하나이며 고전적인 플레어성 관측 대상입니다. DY Eri 변광성 지정은 단발성
폭발이 아니라 지속적인 Hα 방출과 광도 플레어 활동을 반영합니다.

2026-05-29 에 검증된 Phase 2 앵커는 C 를 다음과 같이 단단히 묶습니다.
이중성 역학질량 M = 0.2041 ± 0.0064 M☉ (Mason 2017), Mann et al. 2015
분광 Table 5 반지름 R = 0.274 ± 0.011 R☉ 와 유효 온도 T_eff = 3167 ± 61
K, Cifuentes 2020 CARMENES 볼로메트릭 광도 L = (6.51 ± 0.13) × 10⁻³ L☉,
Mann 2015 [Fe/H] = -0.21 ± 0.08, 그리고 Bond et al. 2017 의 WD 전구체
IFMR 분석에서 나온 시스템 공시각 나이 1.8 ± 0.5 Gyr. 활동성 관련 두
값 — Shan et al. 2024 의 P_rot = 8.56 d 와 다중-서베이 Hα 등가폭 범위
pEW ≈ -2 ~ -4 Å — 은 DB `meta_notes` 에 기록되지만 recommended 측정값으로는
**아닙니다**. Shan 2024 자체가 8.56 d 주기를 quality D (debated, 같은
논문의 166 개 CARMENES 주기 중 27 개가 debated) 로 표시합니다. Hα 는
단일-논문 앵커가 없습니다.

**NearStars 시나리오 선택. 활동성 적색 M4.5 V 플레어성으로 렌더링하여,
가상의 인근 관측자에게 짙은 적색 광을 비추고 DY Eri 급 변광성에 맞는
cfg 박자로 H-알파 플레어를 애니메이트합니다.** 큐레이션된 행성은 없습니다
(주성 A 주위의 HD 26965 b 는 Burrows 2024 가 반박했고, C 로 확장된 적도
없습니다). 13 개 cfg 픽은 canonical 파라미터 셋을 따르며, 4 개의 tie-break
픽은 가상의 C-궤도 관측자에서 본 시각 hex 색조와 이중성 이벤트
지오메트리에 해당합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.5 Ve | high | Gray & Garrison 커뮤니티 canonical. SIMBAD M4.5Ve. Mann 2015 Table 5 는 M4.7 (MK 산포 범위 내). e 접미는 DY Eri 플레어 활동과 일관된 색채권 방출을 표시 |
| `mass_msun` | 0.2041 ± 0.0064 | high | Mason, Hartkopf & Miles 2017 §3. BC 이중성 역학 fit, P = 230.09 yr, 총질량 0.776 ± 0.024 M☉ 를 Heintz 1974 질량비 + van Leeuwen 2007 시차로 분할 |
| `radius_rsun` | 0.274 ± 0.011 | high | Mann et al. 2015 Table 5 'Gl 166 C' 행. 간섭계 M 왜성 샘플로 보정된 M_K 밴드 반지름 관계 + BT-Settl 대기 모델 fit |
| `teff_k` | 3167 ± 61 | high | Mann et al. 2015 Table 5. 저분해 SNIFS 광학 + SpeX NIR 스펙트럼을 BT-Settl 대기 그리드에 fit |
| `luminosity_lsun` | 6.51e-3 ± 0.13e-3 | high | Cifuentes et al. 2020 CARMENES 카탈로그 Karmn J04153-076 행 (VizieR J/A+A/642/A115). Gaia DR2 거리 기반 다중 밴드 SED 적분 |
| `metallicity_fe_h_dex` | -0.21 ± 0.08 | high | Mann et al. 2015 Table 5. Mann 2013a 저분해 분광 [Fe/H] 보정, 태양형 동반자 대비 |
| `age_gyr` | 1.8 ± 0.5 | medium | Bond et al. 2017 §6.2. 시스템 공시각. B 전구체 IFMR 이 M_initial ≈ 1.8 M☉ 와 1.7 Gyr 의 pre-WD 수명 + 0.12 Gyr WD 냉각 ≈ 총 1.8 Gyr. 불확실성은 큐레이터 추정치 |
| `rotation_period_days` | n/a (Shan 2024 8.56 d "debated" 표기) | low | Shan et al. 2024 (CARMENES VII) 는 P_rot = 8.56 d 를 quality D 로 표시. DB meta_notes 에만 기록, recommended 측정값 아님. Open item |
| `activity_log_rhk` | n/a (M 왜성 영역, 대신 H-alpha 사용) | low | Ca II H&K log R'HK 는 완전 대류 M4–M5 왜성의 활동 추적자로 부적합 (포화 색채권 플럭스). Hα 등가폭이 적절한 proxy |
| `activity_h_alpha_pew_a` | -2 ~ -4 (서베이 간 범위) | medium | 다중 서베이. CARMENES (Schöfer 2019), Newton 2017, Reiners 2018 의 GJ 166 C Hα pEW 가 이 범위. 단일 논문 앵커 없음. 변광성 DY Eri 의 활동 사이클에 따라 변동 |
| `activity_cycle_years` | n/a | low | 40 Eri C 의 색채권 사이클 문서화 없음. 수십 년 ASAS-SN / TESS 시계열에서 사이클 제약 결과가 아직 발표되지 않음 |
| `x_ray_log_lx_cgs_qualitative` | 활동성 M4.5 V 기대치만큼 밝음 | low | ROSAT All-Sky Survey 는 BC 페어를 검출하지만 B 의 광구 연 X 선 기여와 블렌딩됨. 40 Eri C 단독 log L_X 발표 없음. Open item |
| `flare_rate_per_day` | n/a (변광성 DY Eri 지정. 빈도 정량화 없음) | low | 광학 광도 변화와 Hα 방출이 플레어 활동을 확정. 서베이 기반 정량 빈도는 우리 참고문헌에 아직 없음. Open item |
| `agb_mass_transfer_spinup_narrative` | true | medium | Bond et al. 2017 §6.2 가 Fuhrmann et al. 2014 를 명시 인용. C 가 B 전구체의 AGB 단계 중 강착으로 spin-up 됐을 가능성. 내러티브 항목이며 단일 cfg 필드 아님 |
| `visual_surface_tint_hex_primary` | `#d97f4a` (따뜻한 적-주황) | low | Tie-break. interesting-first. 3167 K Planck 자취 흑체 + Hα 방출 색조 부스트가 일반 둔한 적색보다 채도 높은 적-주황 쪽으로 지각 색을 밀어냄. Visual styling 에서 문서화 |
| `stellar_color_temp_k` | 3167 | high | Teff 유도 |
| `visual_companion_event_b_visible_as_blue_point` | true | medium | BC 궤도 평균 분리 ≈ 33 AU (Mason 2017). C 에서 본 B 의 겉보기 등급 V ≈ -13 (M_V ≈ 11.0 + 거리 modulus −24), 보름달 밝기와 비슷. B 의 T_eff ≈ 17 200 K 를 반영해 청-백색 점. 렌더링 임계값 tie-break |
| `visual_companion_event_a_visible_as_orange_distant_point` | true | medium | A-BC 평균 분리 ≈ 2000 AU. C 에서 본 A 의 겉보기 등급 V ≈ -9 (M_V ≈ 5.9 + 거리 modulus −15). A 의 K0.5 V T_eff ≈ 5126 K 가 주황 색조. 렌더링 임계값 tie-break |
| `habitable_zone_inner_au` | 0.067 (유도, 보수적) | medium | Kopparapu et al. 2014 M 왜성 HZ 내부 경계 (runaway-greenhouse) 를 √(L / L☉) = √(6.51e-3) 로 스케일링. 큐레이션 행성 없음. 컨텍스트 값 |
| `habitable_zone_outer_au` | 0.21 (유도) | medium | Kopparapu et al. 2014 M 왜성 HZ 외부 경계 (maximum greenhouse) 를 같은 인자로 스케일링. 컨텍스트 값 |

## Surface synthesis

40 Eridani C 의 광구는 후기 M 형 주계열 왜성의 차가운 적색 표면입니다.
T_eff = 3167 K 는 별을 부분 대류 전이 영역에 단단히 위치시키며, 이
영역에서는 복사 코어가 작거나 사라집니다. M = 0.2041 M☉ 의 별은 완전
대류 한계 (수소 연소 주계열별 기준 ≈ 0.35 M☉) 의 바로 위에 있습니다.
현대 항성 내부 모델 (Chabrier & Baraffe 1997, Baraffe 2015) 은 얇은 복사
코어가 잔존할 수 있지만 외피층의 열 수송은 대부분 대류임을 예측합니다.
이 대류 영역이 강한 자기 다이나모와 C 에게 DY Eri 변광성 명칭을 안긴
지속적인 Hα 방출을 직접적으로 만들어 냅니다.

가시 디스크는 후기 M 형의 canonical 분자 밴드 스펙트럼을 보입니다.
광학에서 강한 TiO 밴드 (γ 밴드 헤드 705 nm 부근이 C 의 적-주황 외관을
주도), 황색의 VO 흡수, 근적외선의 FeH 특성. 연속 불투명도는 H⁻ 가
H 밴드 영역에서 피크를 찍습니다. 3167 K 에서 통합된 Planck 자취 색은
CIE 색도 다이어그램의 따뜻한 적-주황 영역 (xy ≈ 0.55, 0.40) 에 위치하며,
Hα 방출은 656 nm 의 좁은 적색 부스트를 더합니다.

Mann et al. 2015 는 Gl 166 C 를 BT-Settl 대기 모델이 경험적 T_eff / R
결정과 전형적 하한보다 더 크게 어긋나는 세 별 중 하나로 특별히 지적합니다
(Mann 2015 §5.4, Figure 16 부근). 나머지 두 별은 PM I10430-0912 와 EQ
Peg B (Gl 896 B) 입니다. 이것이 Phase 3 에 중요한 이유는, 채택한 반지름과
T_eff 가 모델 fit 이 아니라 논문 측정값 (M_K 관계 + F_bol 적분) 이라는
점입니다. Mann 2015 Table 7 의 Dartmouth 모델 fit 은 R = 0.242 R☉ 와
T_eff = 3362 K 를 주는데, 둘 다 경험적 행과 약 11–13% 어긋나며, 이는
Mann 논문이 문서화한 바로 그 M 왜성 모델 편향입니다. DB Phase 2
recommended 항목은 경험적 Table 5 행입니다.

흑점 면적은 활동성 M4.5 V 답게 크고 시간에 따라 변동합니다. Mann 2015
는 178 별 샘플에서 Hα 등가폭 방출을 측정했지만 GJ 166 C 값은 단일 epoch
만 보고합니다. 다중 서베이의 산포는 pEW ≈ -2 ~ -4 Å (Schöfer 2019,
Newton 2017, Reiners 2018) 인데, epoch 간 수십 퍼센트 변동을 의미합니다.
C 의 거주가능영역 근처에서 본 가상의 관측자는 활동 최대기에 디스크의
10-30% 를 덮는 큰 흑점, plage 로 밝아진 활동 영역, 그리고 광학 파장에서
수 퍼센트의 국지 밝아짐으로 나타나는 occasional 킬로-Gauss 자장 플레어
플럭스 폭발 (M4.5 V 플레어성의 canonical 예. EV Lac, AD Leo) 을 보게
됩니다.

약간 금속이 부족한 [Fe/H] = -0.21 은 SED 에 미미한 영향만 줍니다.
BT-Settl 그리드에서 [Fe/H] = -0.2 vs 태양의 차이는 약 30 K 등가 reddening
인데, 큐레이션된 61 K 불확실성 안에 충분히 들어옵니다. C 의 [Fe/H] 는
40 Eri A 값 (-0.31, Sousa 2008) 과 1.5 sigma 안에서 일관되며, 시스템
공시각 기원을 뒷받침합니다.

## Atmosphere synthesis

40 Eri C 는 후기 M 형 플레어성에 전형적인 완전 색채권 활동성 M 왜성
대기를 가집니다. 색채권은 Hα, Ca II H&K, Hβ, He I D3, 그리고 폭넓은 UV
방출선 (GALEX FUV 의 Mg II h&k, HST/STIS 에 접근 가능한 Lyα) 으로
채워져 있습니다. DY Eri 변광성 지정은 색채권 활동 사이클 전반에서 광도
플레어와 지속적인 Hα 방출을 보여 준 수십 년 지상 모니터링에서 비롯됩니다.

X 선 방출은 밝지만 이 합성 단계에서는 정량적으로 제약이 약합니다.
ROSAT All-Sky Survey 는 BC 페어를 검출했지만 0.1–2.4 keV 연 X 선
성분은 C 의 색채권 코로나와 B 의 광구 열 X 선 기여를 블렌딩합니다.
40 Eri C 단독의 정량적 log L_X / L_bol 은 현재 우리 참고문헌에 없습니다.
이 나이의 M4.5 V 에 대한 정성적 기대값은 log L_X / L_bol ≈ -3 ~ -4
(전형적 M 왜성 활동 시퀀스, 예 Wright et al. 2011, Schmitt & Liefke 2004)
이며, 사이클 진폭은 몇 배 수준입니다. 플레어 X 선 피크는 정상상태보다
한 자릿수 더 높습니다. Open items 목록은 단독 성분 X 선 측정을 후속
대상으로 표시해 둡니다.

전이 영역은 M4–M5 활동성 별의 전형적인 Lyman-α 연속체 + Lyα 라인을
만듭니다. 표면 플럭스는 정상상태로 수 × 10⁵ erg s⁻¹ cm⁻², 플레어
강화로 두 자릿수까지 올라갑니다. Gyr 시간 스케일의 통합 XUV (10–100 nm)
광도는 잠재적 행성에 큰 의미가 있습니다. France et al. 2016 (MUSCLES)
는 활동성 M4–M5 왜성이 더 낮은 볼로메트릭 광도에도 불구하고 지구와
비교 가능한 누적 XUV 선량을 전달함을 발견했습니다 — 정상상태 XUV /
L_bol 비율이 태양값의 약 10⁴ 배이기 때문입니다. C 주위에 큐레이션
행성은 없으며, 이 영역은 시스템 수준 활동 컨텍스트에만 정보를 줍니다.

C 는 대기-광화학 결합으로 제약할 표면을 갖지 않습니다 (별이니까). 여기서
"대기" 는 자기 다이나모로 동작하는 색채권 – 전이 영역 – 코로나 구조를
뜻합니다. cfg 함의. C 주위의 미래 행성 후보는 색채권 모델에서 강한 XUV
환경을 상속받게 되며, 재진입 효과 렌더러는 Hα 가 우세한 광학 스펙트럼을
반영하도록 적색 파장을 포화시켜야 합니다.

## Rotation & spin synthesis

회전 주기는 진정으로 불확실합니다. Shan et al. 2024 (CARMENES VII) 는
Karmn J04153-076 = GJ 166 C 의 CARMENES 활동 지표 시계열 주기 8.56 d 를
보고하지만, 검출을 quality D 로 분류합니다 ("debated". 논문 Sect. 4 에
따르면 검출된 166 개 주기 중 27 개가 debated, 68 개가 provisional). Phase
2 DB 는 이를 `meta_notes` 에만 기록합니다 — `rotation_measurements`
recommended:true 항목이 없습니다. 2026-05-27 작업 노트의 "Kemmer 2025
~137 d" 라는 이전 attribution 은 교차 확인 시 철회됐습니다. Y. Shan 이
실제 논문의 제1저자 (Kemmer 는 47 명의 공저자 중 22 번째) 이고, 연도는
2025 가 아니라 2024 이며, 주기 값은 약 16 배 차이가 납니다.

NearStars 목적상 **C 의 cfg 회전 주기 필드는 N/A** 입니다. 다운스트림
cfg 작성자는 주기를 unset 으로 두고 명시적 갭으로 표시하거나, Shan 2024
의 허용 범위 안에서의 tie-break 임을 분명히 한 cfg 레벨 노트를 달아
interesting-first 자리표시자 (예. 9 d) 를 쓸 수 있습니다. 독립적 검증
— TESS 단주기 광도, RV 변조 위상 폴딩, ZDI 분광편광 — 이 들어오면
항목이 `n/a` 에서 `recommended:false`, 그리고 다음 패스에서
`recommended:true` 로 전환됩니다.

별도의 Phase 3 내러티브 한 가지. 40 Eri C 의 회전 상태는 B 전구체로부터의
물질 이동의 fossil 흔적을 보존할 수 있습니다. Bond et al. 2017 §6.2 는
Fuhrmann et al. 2014 를 명시 인용합니다 — C 가 "40 Eri B 전구체의 AGB
단계 중 강착으로 더 높은 회전 속도로 spin-up 됐을 수 있다" 는 가설.
40 Eri B 전구체는 M_initial ≈ 1.8 M☉ 로 AGB 를 상승한 뒤 외피를 잃었으며,
잃어버린 외피의 일부분은 WD 잔재를 비껴 ≈ 33 AU 에 있는 C 에 포획됐을
가능성이 있습니다. 만약 debated 한 단주기 회전 (8.56 d 또는 비슷한 값)
이 결국 확정되면, AGB-spin-up 시나리오를 정성적으로 뒷받침하게 됩니다.
cfg 는 정량적 회전율 예측이 아니라 내러티브 힌트로 이것을 인코딩해야
합니다.

자전축 경사는 제약되지 않습니다. 시각 렌더링을 위해 NearStars 는 무작위
배향 자전축을 채택하며, 그럴듯하게는 BC 궤도면에 대해 ~30° 기울어진
정도입니다 (33 AU 분리에서 조석 동기화가 무의미한 다른 장기 MS+WD
이중성과 유추).

## Visual styling

NearStars 렌더러에서 40 Eridani C 는 작고 따뜻한 적-주황 M4.5 V 플레어성
으로 묘사됩니다. 3167 K Planck 자취 흑체는 `#d97f4a` 부근 (따뜻한 적-주황,
CIE xy ≈ 0.55, 0.40) 의 기본 색을 주며, Hα 656 nm 방출은 지각 색조를
포화된 적색 쪽으로 약간 더 밀어냅니다. Confidence: low tie-break 호출은
*interesting-first* 입니다. 3167 K Planck 자취 envelope 안에 합당한 hex
값의 범위가 있고, 포화된 적-주황 옵션이 혼합 시스템 렌더에서 K0.5 V 주성
A (따뜻한 황-주황) 와 청-백색 WD B 로부터 C 를 시각적으로 뚜렷이
구분합니다.

지구에서 5.01 pc 거리에서 보면 V = 11.17 이 40 Eri C 를 맨눈 한계 아래로
두지만 작은 망원경 범위 안입니다. C 의 거주가능영역 거리 (L = 6.51e-3 L☉
기반 ≈ 0.1 AU) 의 가상 관측자에서 보면 별이 ~1.5° (2 R★ / a) 의 각지름을
채웁니다 — 지구에서 본 태양 크기의 약 세 배입니다. 디스크 특징에는 큰
흑점 (활동 최대기에 10–30% 면적), occasional 광학 수 퍼센트 수준의
플레어 brightening, 그리고 분자 밴드 대기 특유의 강한 적-주황 limb
darkening 이 포함됩니다.

평균 분리 33 AU 에 있는 동반자 B (BC 궤도 Mason 2017, e = 0.4300 →
근일점 ~19 AU, 원일점 ~47 AU) 는 빛나는 청-백색 점으로, 그 밝기가
대단합니다. B 의 M_V ≈ 11.0 (DA WD, T_eff ≈ 17 200 K) 을 33 AU 관측자
에 대입하면 겉보기 등급은 약 V ≈ -13 (mag = M_V + 5·log₁₀(33 AU /
10 pc) ≈ 11.0 − 24). 지구에서 본 보름달과 비교 가능한 밝기로, 작지만
강렬한 청-백색 점이 C 의 적색 조명을 압도하며 conjunction 에서 가장
밝고 원일점에서도 (V ≈ -12) 여전히 두드러집니다. 궤도 운동은 수십 년
에서 1 세기 시간 스케일로 B 를 C-하늘에서 시각적으로 가로지르게
만듭니다.

평균 분리 ~2000 AU 에 있는 주성 A 는 훨씬 더 어두우나 여전히 맨눈으로
보이는 주황 "먼 태양" 으로 나타납니다. A 의 M_V ≈ 5.9 에 2000 AU 거리
modulus 를 더하면 겉보기 V ≈ -9 (mag = 5.9 − 15). 지구에서 본 어떤
행성보다도 훨씬 더 밝지만, B 와는 인상적으로 다른 스케일의 밝기입니다.
K0.5 V T_eff ≈ 5126 K 는 분명한 주황 색조를 줍니다. 삼중계는 C 의 하늘
에서 다음과 같이 나타납니다 — 가까운 C 디스크 조명 (지배적 적색 광원),
근-항성 청-백색 서치라이트 (B), 그리고 더 먼 주황 점 광원 A — 세 광원이
서로 매우 다른 강도와 시간 스케일을 가집니다 (B 는 수십 년에 걸쳐
시각적으로 이동하고, A 는 ~8000 년의 A-BC 궤도를 고려할 때 인간 시간
스케일에서는 사실상 고정).

플레어 이벤트는 Firefly-cfg 측 플라즈마 색 선택을 추동합니다. 활동성
M4.5 V 플레어성은 Hα + Hβ + Ca II 방출이 우세한 광학 플레어 스펙트럼을
만들며, 플레어 플럭스 피크 동안 재진입 플라즈마를 포화 적색/분홍 팔레트
쪽으로 편향시킵니다. 정확한 팔레트 조립은 firefly-cfg 스킬 영역
(`firefly-cfg/` 의 플라즈마 색 주기율표 참고) 이지만, 여기서의 Phase 3
힌트는 다음과 같습니다 — **C 부근에서는 일반적 흰색 플라즈마 효과보다
강한 적색을 선호**하며, DY Eri 급 변광성 박자 (한 시간 미만 상승, 수
시간 감쇠 플레어 프로파일) 로 트리거되는 선택적 Hα-적색 플레어 이벤트
액센트.

흑점, faculae, prominence 는 (불확실한) 활동 사이클 동안 활동성 M 왜성
스케일로 렌더링되며, 사이클 위상은 논문이 확정한 사이클 주기가 나올
때까지 유보됩니다.

## Bibliography

### Read (decision-driving)

- **Mason B. D., Hartkopf W. I., Miles K. N. 2017** — *Binary Star
  Orbits. V. The Nearby White Dwarf/Red Dwarf Pair 40 Eri BC*,
  AJ 154, 200 (`2017AJ....154..200M`, arXiv:1707.03635,
  DOI 10.3847/1538-3881/aa803e). 갱신된 230.09 년 BC 시각-분광 궤도.
  총질량 0.776 ± 0.024 M☉, e = 0.4300, a = 6.93″. Heintz 1974 질량비와
  결합해 M_C = 0.2041 ± 0.0064 M☉ 산출. **C 역학질량의 주 앵커.**
- **Mann A. W., Feiden G. A., Gaidos E., Boyajian T., von Braun K.
  2015** — *How to Constrain Your M Dwarf: Measuring Effective
  Temperature, Bolometric Luminosity, Mass, and Radius*, ApJ 804, 64
  (`2015ApJ...804...64M`, arXiv:1501.01635, DOI 10.1088/0004-637X/804/1/64).
  경험적 M 왜성 보정. Table 5 'Gl 166 C' 행이 R = 0.274 ± 0.011 R☉,
  T_eff = 3167 ± 61 K, [Fe/H] = -0.21 ± 0.08, Hα EW 를 줌. **반지름 /
  T_eff / [Fe/H] 의 주 앵커.** Table 7 Dartmouth 모델 fit (R = 0.242,
  T_eff = 3362) 은 §5.4 + Figure 16 에서 문서화된 샘플 수준 모델 편향
  데이터포인트로 보존.
- **Cifuentes C., Caballero J. A., Cortés-Contreras M. et al. 2020** —
  *CARMENES input catalogue of M dwarfs. V. Luminosities, colours,
  and spectral energy distributions*, A&A 642, A115 (`2020A&A...642A.115C`,
  arXiv:2007.15077, DOI 10.1051/0004-6361/202038295). CARMENES M 왜성
  샘플의 다중 밴드 SED 적분. Karmn J04153-076 = GJ 166 C 항목 (VizieR
  J/A+A/642/A115) 이 L = (6.51 ± 0.13) × 10⁻³ L☉. **광도의 주 앵커.**
- **Bond H. E., Bergeron P., Bédard A. 2017** — *The aged
  Astrophysical Implications of a New Dynamical Mass for the Nearby
  White Dwarf 40 Eridani B*, ApJ 848, 16
  (`2017ApJ...848...16B`, arXiv:1709.00478, DOI 10.3847/1538-4357/aa8a63).
  40 Eri B 의 HST/COS UV 분광. 전체 시스템 재분석. §6.2 의 IFMR
  (Salaris et al. 2009, M_final = 0.134 M_initial + 0.331) 가 B 의 M_progenitor ≈ 1.8 M☉ 을 시사하며, 시스템
  공시각 총 나이 ≈ 1.8 Gyr 가 도출됩니다. 같은 섹션이 C 의 AGB 물질
  이동 spin-up 시나리오에 대해 Fuhrmann et al. 2014 를 인용. **나이 +
  AGB-spin-up 내러티브의 주 앵커.**
- **Shan Y., Reiners A., Fabbian D. et al. 2024** — *The CARMENES
  search for exoplanets around M dwarfs. VII. Photospheric rotation
  periods from the activity time series of 166 M dwarfs*, A&A 684, A9
  (`2024A&A...684A...9S`, arXiv:2401.09550,
  DOI 10.1051/0004-6361/202346794). CARMENES 활동 지표 시계열.
  Karmn J04153-076 P_rot = 8.56 d, quality flag D ("debated"). 166 개
  주기 중 27 개가 debated, 68 개가 provisional. **DB meta_notes 에만
  기록 — recommended 측정값 아님.**

### Read (context / methodology)

- **Heintz W. D. 1974** — *Astrometric study of four visual binaries*,
  AJ 79, 819 (`1974AJ.....79..819H`). Mason 2017 이 총질량 분할에 쓴
  역사적 BC 질량비를 제공.
- **van Leeuwen F. 2007** — *Validation of the new Hipparcos
  reduction*, A&A 474, 653 (`2007A&A...474..653V`). Mason 2017 의
  역학질량 유도에 쓰인 시차.
- **Cummings J. D., Kalirai J. S., Tremblay P.-E. et al. 2018** —
  *The white dwarf initial–final mass relation for progenitor masses
  up to 7.5 M☉*, ApJ 866, 21. Bond 2017 이 40 Eri B 의 전구체 질량
  반전에 쓴 IFMR.
- **Fuhrmann K., Chini R., Buda L.-S. & Pozo Nuñez F. 2014** —
  *On the Age of Gliese 86*, ApJ 785, 68 (`2014ApJ...785...68F`,
  DOI 10.1088/0004-637X/785/1/68). 주로 Gl 86 K+WD 이중성의 나이
  결정 논문. 40 Eri C 를 analog 사례로 인용해, M 왜성 동반자의 "상당한
  투영 회전 속도" 가 degenerate 동반자의 이전 AGB 단계 물질 손실에서
  유래한 것으로 봅니다. Bond 2017 §6.2 가 같은 spin-up 가설을 40 Eri C
  에 적용하면서 인용.
- **Tokovinin A. 2018** — *The updated multiple-star catalog*,
  ApJS 235, 6 (`2018ApJS..235....6T`). A-BC 페어를 ~8000 년 외궤도의
  unfitted 항목으로 등재.
- **Burrows A. et al. 2024** — *The Death of Vulcan: NEID Reveals
  That the Planet Candidate Orbiting HD 26965 Is Stellar Activity*,
  AJ 167, 243 (`2024AJ....167..243B`, DOI 10.3847/1538-3881/ad34d5).
  HD 26965 (= 40 Eri A) 의 NEID 정밀 RV 모니터링. Ma 2018 의 "Vulcan"
  행성 후보를 반박하고, 약 42 일 신호를 회전 변조된 항성 활동 (흑점 +
  convective blueshift 억제) 으로 귀속. C 와 직접 관련은 없지만 시스템의
  무행성 상태를 확립.
- **Kopparapu R. K., Ramirez R. M., SchottelKotte J. et al. 2014** —
  *Habitable zones around main-sequence stars: dependence on planetary
  mass*, ApJ 787, L29 (`2014ApJ...787L..29K`, arXiv:1404.5292). 40 Eri C
  의 HZ 컨텍스트 값 유도에 쓴 HZ 경계 스케일링.

### Read (instrument / non-cfg-decisive)

- **Schöfer P., Jeffers S. V., Reiners A. et al. 2019** —
  *The CARMENES search for exoplanets around M dwarfs.
  Activity indicators at visible and near-infrared wavelengths*,
  A&A 623, A44 (`2019A&A...623A..44S`, arXiv:1903.06803).
  CARMENES Hα EW 시계열. GJ 166 C 가 샘플에 포함. DB meta_notes 의
  Hα pEW 범위 -2 ~ -4 Å 에 쓰임.
- **Newton E. R., Mondrik N., Irwin J. et al. 2017** — *New rotation
  period measurements for M dwarfs in the southern hemisphere*,
  AJ 154, 224 (`2017AJ....154..224N`, arXiv:1611.04857). MEarth-South
  광도 회전 주기. 여러 서베이 Hα 교차 참조 중 하나.
- **Reiners A., Zechmeister M., Caballero J. A. et al. 2018** —
  *The CARMENES search for exoplanets around M dwarfs. High-
  resolution optical and near-infrared spectroscopy of 324 survey
  stars*, A&A 612, A49 (`2018A&A...612A..49R`, arXiv:1711.06576).
  CARMENES 기기 논문. GJ 166 C 파라미터 행.
- **Wright N. J., Drake J. J., Mamajek E. E., Henry G. W. 2011** —
  *The stellar-activity-rotation relationship and the evolution of
  stellar dynamos*, ApJ 743, 48 (`2011ApJ...743...48W`). M 왜성
  log L_X / L_bol 보정에 정성적으로 사용.
- **France K., Loyd R. O. P., Youngblood A. et al. 2016** —
  *The MUSCLES treasury survey. I. Motivation and overview*,
  ApJ 820, 89 (`2016ApJ...820...89F`, arXiv:1602.09142). 활동성 M
  왜성 주변 XUV 환경의 컨텍스트.

### Not read — no arXiv preprint or low-priority (~12 papers)

전체 필터된 bib (이 항성 단독 합성에서는 40 Eri 의 Phase 3 driver /
system.yaml 이 아직 없어 재생성하지 않음) 에는 DY Eri 의 옛 다중 십
년 지상 광도 (Hertzsprung 1922 등), 역사적 스펙트럼 분류 (Joy 1947,
Gliese 1957), 그리고 다양한 활동 컨텍스트 M 왜성 카탈로그 논문이
포함됩니다. 위 read 셋이 이미 다룬 것 이외에 cfg 관련 Decisions 행을
추동하는 항목은 없습니다.

## Open items for follow-up

- **독립적 회전 주기 검증.** Shan 2024 의 8.56 d 는 quality D 로 표시됨.
  TESS 단주기 광도 (40 Eri C 는 TESS pointing 32 / 33), RV 위상 폴딩
  변조, ZDI 분광편광 매핑을 통한 독립 확인이 들어오면 Decisions 행이
  `n/a` 에서 recommended:false → true 항목으로 전환됩니다.
- **단일 논문 Hα 활동 앵커.** 다중 서베이 산포 pEW = -2 ~ -4 Å 는
  활동성 플레어성의 변동 성격을 잘 담아내지만, 전용 장기 시계열 측정
  (예. CARMENES 재방문, HARPS-N follow-up) 이 들어오면 범위 대신 논문
  앵커 평균 + 사이클 진폭을 기록할 수 있습니다.
- **40 Eri C 단독 X 선 측정.** ROSAT All-Sky Survey 는 BC 페어를
  블렌딩. Chandra 또는 XMM-Newton 의 전용 포인팅으로 C 를 B 의 광구
  열 X 선 기여에서 분리하면 논문 앵커된 log L_X / L_bol 값을 얻습니다.
  현재는 정성적이기만 함.
- **플레어 빈도 정량화.** DY Eri 변광성은 정성적으로 잘 알려져 있지만
  서베이 기반 정량 플레어 빈도 (에너지 임계값 이상 일일 플레어 수) 가
  현재 참고문헌에 없습니다. GJ 166 C 에 대한 TESS 섹터별 분석 또는
  Evryscope 플레어 서베이 결과가 이 갭을 메울 것.
- **AGB-spin-up 시나리오 확정.** Fuhrmann 2014 가 제안한, C 가 B 의
  AGB 단계 물질 이동으로 spin-up 됐다는 시나리오는 debated 한 단주기
  P_rot 과 일관됩니다 (단정은 아님). 확정된 단기 회전 주기에 더해 C
  대기에서의 화학 풍부도 시그너처 (s-process 강화, 헬륨 증가) 가 결정적
  검사가 됩니다. Phase 3 cfg 액션은 없음. 내러티브 완전성을 위해 기록.
- **분광형 M4.5 vs M4.7.** Mann 2015 Table 5 는 M4.7, 커뮤니티 canonical
  은 M4.5 Ve. 둘 다 MK 분류 산포 안. Phase 3 액션 불필요지만, 분광형을
  명시 참조 attribution 으로 기록하는 미래 스키마 단계 업그레이드에서
  명시할 만함.

## Related

- [40-eridani-a](40-eridani-a.md) — K0.5 V 주성. 반박된 Vulcan 행성. BC 와 ~83″ 미해결
- [40-eridani-b](40-eridani-b.md) — DA2.9 백색왜성 동반자. C 와 230.09 년 이중성 궤도
- [methodology](../reference/methodology.md) — Decisions 표 스키마의 원본
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — BC 시각-분광 궤도 Kepler→ICRS 구성에 적용
