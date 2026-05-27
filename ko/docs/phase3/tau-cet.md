<!-- τ Ceti Phase 3 합성. cfg-ready 결정과 근거 -->
# τ Ceti — Phase 3 Synthesis

τ Ceti (HD 10700, HIP 8102, GJ 71) 는 태양에 가장 가까운 단독 G 형
별로 거리 3.652 ± 0.002 pc / 11.91 ly 에 있습니다. Gaia DR3 시차
273.81 ± 0.17 mas (DB Phase 2). 분광형은 G8V (Gray 2006) 로 솔라
analog 분포의 차갑고 어두운 끝에 자리잡으며, 질량 M =
0.783 ± 0.012 M☉ (Feng 2017), 반지름 R = 0.793 ± 0.004 R☉ (Teixeira
2009 asteroseismology + Di Folco 2007 간섭계), 유효 온도 Teff =
5344 ± 50 K (Pavlenko 2012) 입니다. 가까운 G 왜성들 사이에서
가장 두드러진 특징은 이례적으로 낮은 금속도로, [Fe/H] = −0.55 ± 0.05
(Pavlenko 2012; Santos 2013 의 −0.49 ± 0.05 와 잘 일치) — 행성을
거느린 별로서는 매우 철-결핍이며 α Cen A 기준치 보다 약 0.8 dex
낮습니다.

τ Ceti 의 다른 큰 특징은 오래되고 운동학적으로 조용한 역사와
두드러진 차가운 잔해 원반입니다. Pavlenko 2012 는 τ Ceti 를
Eggen 1971 의 오래된 원반 종족 별 super-population 에 위치시킵니다.
이를 34 일 회전 주기 (Baliunas 1996 Mt Wilson Ca II H&K 모니터링)
및 Mamajek & Hillenbrand 2008 gyrochronology 보정과 결합하면 나이는
7 ± 1.5 Gyr 입니다. 색채권 활동도는 *조용한* 방향으로 극단적입니다.
log R'HK = −4.95 (Pavlenko 2012) 는 τ Ceti 를 HK 서베이에서 가장
불활성한 G 왜성 중 하나로 두며, X 선 방출은 EXOSAT 검출 임계값
아래입니다 (Schmitt 1985, log L_X ≤ 26.5). 별 주위에는 차갑고 넓은
잔해 원반이 있는데, Greaves 2004 가 SCUBA 서브밀리 초과로 처음
검출하고 MacGregor 2016 가 ALMA Band 6 영상으로 약 6–55 AU 범위의
단일 고리로 분해했습니다. 총 먼지 질량은 태양의 카이퍼 벨트
대비 ~10–20 배로, 우리 외태양계와 가장 닮은 가까운 분해 잔해 원반
analog 입니다.

Phase 2 DB 는 Feng 2017 로부터 네 개의 확인 행성 (e, f, g, h) 을
기록하지만, `db/systems/tau_cet.json` 에는 τ Ceti e 가 빠진 상태로
f, g, h 만 존재합니다. rex-data-comparison 참조 문서는 이 점을
큐레이션 질문으로 표시합니다 (Feng 2017 은 네 행성 모두에 동일한
dispute flag 를 부여). 이 항성 합성은 따라서 host 만 다루며, 행성
f / g / h Phase 3 작업은 별도의 follow-up 워크스페이스로 미루고,
τ Cet e 큐레이션 질문은 Open item 으로 남깁니다.

**NearStars 시나리오 선택. 태양 질량의 약 80%, 광도 46% 인 조용하고
오래되고 금속이 적은 G8V 별로, 태양보다 살짝 더 시원한 노란 색조를
띠며, ALMA 가 분해한 6–55 AU 의 넓은 잔해 벨트와 안쪽의 f / g / h
행성계가 희미한 점광원으로 보이는 모습으로 렌더링합니다.** 22 개
cfg 픽 중 18 개는 canonical-aligned, 4 개는 tie-break (시각 hex,
원반 hex, 원반 opacity, 원반 morphology 의 조성 추론) 입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G8V | high | Gray 2006. SIMBAD. DB |
| `mass_msun` | 0.783 ± 0.012 | high | Feng 2017. Mann 2015 보정의 M–K 관계. Teixeira 2009 asteroseismic 0.783 ± 0.012 일치 |
| `radius_rsun` | 0.793 ± 0.004 | high | Teixeira 2009 asteroseismic + Di Folco 2007 VLTI/VINCI 간섭계 |
| `teff_k` | 5344 ± 50 | high | Pavlenko 2012. 고분해 분광, 태양 대비 differential. Santos 2013 = 5333 ± 20 K 와 1σ 일치 |
| `luminosity_lsun` | 0.457 | high | R 과 Teff 로 Stefan–Boltzmann 유도 |
| `metallicity_fe_h_dex` | −0.55 ± 0.05 | high | Pavlenko 2012. 태양 대비 differential LTE 분석. Santos 2013 = −0.49 ± 0.05 와 1σ 일치 |
| `age_gyr` | 7.0 ± 1.5 | medium | Pavlenko 2012. Eggen 1971 super-population 운동학 + 색채권 활동도 proxy. Mamajek & Hillenbrand 2008 의 34 d 회전 gyrochronology 가 6–8 Gyr 로 일치 |
| `rotation_period_days` | 34 | high | Baliunas 1996. Mt Wilson Ca II H&K 시계열. Pavlenko 2012 확인 |
| `activity_log_rhk` | −4.95 | high | Pavlenko 2012. HK 서베이에서 가장 불활성한 G 왜성 중 하나 |
| `x_ray_log_lx_cgs_max` | 26.5 | medium | Schmitt 1985. EXOSAT 미검출 상한. Judge 2004 가 정적 FUV 방출 확인 |
| `visual_surface_tint_hex_primary` | `#ffe9c8` (태양보다 살짝 덜 노란 크림-노랑) | medium | Tie-break. G8V 흑체 5344 K + 금속이 적은 SED 는 같은 Teff 의 태양형 metal 대비 살짝 푸른 쪽으로 이동 ([Fe/H] = −0.55 에서 청색대 line blanketing 감소). interesting-first 룰에 따라 α Cen A 의 metal-rich 크림과 시각적으로 구분되는 선택 |
| `stellar_color_temp_k` | 5344 | high | Teff 유도 |
| `disk_present` | true | high | Greaves 2004 SCUBA 850 μm 초과. MacGregor 2016 ALMA Band 6 분해 영상 |
| `disk_inner_radius_au` | 6 | high | MacGregor 2016. ALMA 분해 fit, 안쪽 가장자리 ~6 AU |
| `disk_outer_radius_au` | 55 | high | MacGregor 2016. ALMA 분해 fit, 바깥쪽 가장자리 ~55 AU |
| `disk_dust_temperature_k` | 60 | high | MacGregor 2016 SED + Greaves 2004 의 60–80 K 와 일치 |
| `disk_tint_rgb_hex` | `#b8aa9c` (따뜻한 grey-brown, 금속이 적은 카이퍼 벨트 analog) | low | Tie-break. 조성은 직접 측정되지 않음. 모성이 metal-poor 라 원시 입자에 철이 덜 들어가 reddening 도 적었을 것이라는 가정으로 Sol KBO 기준보다 덜 붉은 색조를 채택. interesting-first 룰 적용 |
| `disk_opacity` | 0.15 | low | Tie-break. MacGregor 2016 의 먼지 질량 + 고리 기하에서 나오는 물리 광학적 깊이는 ~10⁻³ 이지만, 게임 내에서 우주 배경 대비 가시성을 살리기 위해 cfg 는 0.15 를 사용. 렌더 가시성 trade-off 로 문서화 |
| `disk_morphology` | "broad single ring, metal-poor analog of Kuiper Belt" | high | MacGregor 2016 §3. multi-belt 보다 단일 넓은 고리를 명시적으로 선호. 분해된 안쪽 갭 없음 |
| `disk_resolved_imaging` | true | high | MacGregor 2016. ALMA Band 6 분해 |
| `disk_imaging_observatory` | ALMA | high | MacGregor 2016 |
| `disk_mass_mearth` | 1.2 | medium | MacGregor 2016 fit. Sol KBO 먼지 대비 ~10–20× (Sol KBO ≈ 0.01 M⊕ 먼지) |
| `disk_planetesimal_belt_inferred` | true | high | MacGregor 2016 §5. 충돌 cascade 가 먼지를 보충하려면 부모 planetesimal 벨트가 필요 |

## Surface synthesis

τ Ceti 의 광구는 더 차갑고 더 늙고 훨씬 더 철-결핍인 태양의 사촌
입니다. 유효 온도 5344 K 는 태양 5777 K 보다 433 K 낮으며, R =
0.793 R☉ 과 결합한 Stefan–Boltzmann 볼로메트릭 광도는 0.457 L☉ 로
태양 기준의 절반에 약간 못 미칩니다. G8V 분류 (Gray 2006) 는
τ Ceti 를 솔라 analog 대역의 차갑고 어두운 끝에 놓는데, 온도는
ε Eridani 의 K2V 와 비슷하지만 envelope 표면중력은 어린 K 별이
아닌 진짜 G 왜성의 그것입니다.

금속도 [Fe/H] = −0.55 (Pavlenko 2012) 가 가장 두드러진 특징입니다.
태양 대비 철이 약 4 배 적기 때문에 청색 연속체의 line blanketing 도
그만큼 약해지고, 통합 가시광 SED 는 같은 Teff 의 태양형 metallicity
G8V 보다 살짝 푸르게 보입니다. 차이 자체는 작지만 (~10–20 K 등가
청색 편이) cfg 표면 색조를 α Cen A 의 +0.24 dex 따뜻한 크림에서
좀 더 깨끗한 옅은 노랑 쪽으로 미는 데에는 충분합니다. Santos 2013
의 [Fe/H] = −0.49 ± 0.05 측정은 통계적으로 일관되어 그림을
보강하는데, 두 분석의 주요 차이는 사용한 모형 대기 격자입니다.
Pavlenko 2012 의 태양 대비 differential 분석이 더 깨끗한 관측치라
선호됩니다.

Granulation 은 직접 영상으로 잡히지 않지만 패턴은 태양형이고 시간
스케일은 광구 온도가 낮은 만큼 살짝 느릴 것으로 예측됩니다 (음향
컷오프가 √g/√T_eff 로 스케일하기 때문에 τ Ceti 의 p-mode 진동은
태양의 5분 진동보다 특성 주기가 약간 길어집니다). Teixeira 2009 가
HARPS 로 p-mode 스펙트럼을 검출했으며, Δν = 169.0 ± 0.5 μHz, ν_max
≈ 4490 μHz 로 위에서 채택한 asteroseismic 반지름과 질량과 일관
됩니다. H 밴드 limb darkening 은 직접 측정되지 않았습니다 (Kervella
2017 가 α Cen A 에 한 수준의 VLTI 간섭계 캠페인이 τ Ceti 에는
없습니다). cfg 는 `limb_darkening_alpha_h` 를 비워 두고 하위
렌더러에서 태양형 기본값을 사용합니다.

흑점 면적은 장기 지상 모니터링의 광도 정밀도로는 사실상 검출
불가능합니다. log R'HK = −4.95 로 τ Ceti 는 α Cen A 보다 분수만큼
덜 활동적이고 현대 태양보다 훨씬 아래에 있습니다. Baliunas 1996
기록에서 색채권 Ca II H&K 방출은 검출 가능한 사이클 없이 평탄하며,
이는 오래되고 느리게 자전하며 금속이 적은 G 왜성에서 기대되는
포화-조용 영역과 일관됩니다.

## Atmosphere synthesis

τ Ceti 의 chromosphere–transition-region–corona 구조는 조용한 G
왜성의 canonical 기준입니다. Pavlenko 2012 의 log R'HK = −4.95 는
색채권 Ca II H&K 방출을 basal flux floor — 음향 가열만으로 기대되는
최소값 — 근처에 두며, 자기 사이클 변조도 검출되지 않습니다. Hα 는
흡수로 나타나며 측정 가능한 변동성은 없습니다.

X 선 방출은 EXOSAT 검출 임계값 아래입니다. Schmitt 1985 는 상한
log L_X ≤ 26.5 cgs (0.1–2.4 keV) 를 보고합니다. 이후 XMM-Newton 과
Chandra 관측 (Judge 2004 와 후속 컴파일레이션에 정리) 도 깨끗한
검출을 만들지 못했고, 정적 코로나는 α Cen A 의 사이클 최소기보다
어둡습니다. X 선 활동 사이클 증거도 없습니다. FUV 연속체 방출
(Judge 2004) 역시 약하며, 이는 전이 영역이 현대 태양의 것보다 더
얇고 차갑다는 점을 시사합니다.

flare 는 검출되지 않습니다. 장기 광도 모니터링 (HIPPARCOS, Mt
Wilson) 은 잡음 위로 충격적 밝아짐 이벤트를 보이지 않으며, 표면
자기장은 가용한 고분해 분광에서 Zeeman 폭증의 검출 한계 ~50 G
아래입니다. 통합 XUV 광도는 10⁻⁵ L_bol 보다 훨씬 작아 f / g / h
어느 행성 궤도에서도 Gyr 시간 스케일에 걸쳐 지구형 대기를 의미
있게 침식하지 못합니다.

행성계에 대한 함의는 조용한 α Cen A 와 비교해서도 뚜렷이 더
온화한, 예외적으로 우호적인 우주환경입니다. 안쪽 행성의 대기 침식
계산은 K 와 M 왜성에서 규칙으로 자리잡은 stellar XUV 구동 유체역학
손실 없이 thermal Jeans 손실만으로 기본값을 잡을 수 있습니다.

## Rotation & spin synthesis

τ Ceti 의 회전 주기는 34 일입니다 (Baliunas 1996 Mt Wilson Ca II
H&K 모니터링, Pavlenko 2012 가 HK 와 광도 데이터 결합으로 확인).
최근 zeeman-doppler imaging (Boro Saikia 2018) 은 46 일 주기를
선호하지만, HK 추적의 34 일 값이 canonical 기준이며 7 Gyr G8V 의
Skumanich braking 기대치 — 태양의 25 일 자전을 4.6 Gyr 에 고정해
P_rot ∝ √t 로 외삽하면 7 Gyr 에 ~31 일 — 와 측정 산포 안에서
일치합니다.

느린 자전은 Pavlenko 2012 의 Eggen 1971 super-population 운동학
멤버십에서 나오는 오래된 나이와 Mamajek & Hillenbrand 2008 의
gyrochronology 보정 (34 일 주기와 B–V 색지수로 Skumanich 법칙
적용 시 6.5 Gyr) 모두와 일관됩니다. 결합 나이 추정치 7.0 ± 1.5 Gyr
가 cfg 채택값으로, 불확실성 범위는 gyrochronology 와 운동학 추정을
모두 포괄합니다.

Asteroseismic p-mode 진동은 Teixeira 2009 가 HARPS 8 야간 RV
모니터링에서 검출했습니다. Δν = 169.0 ± 0.5 μHz, ν_max ≈ 4490 μHz.
음향 시간 스케일 2π/Δν ≈ 1.6 h 는 더 작은 반지름과 더 높은 평균
음속으로 스케일하면 태양의 5분 진동보다 짧으며, 이로부터 질량
0.783 ± 0.012 M☉ 과 반지름 0.793 ± 0.004 R☉ 가 퍼센트 수준의
정밀도로 제약됩니다. Decisions 테이블이 채택한 값들입니다.

차등 회전은 분해되지 않습니다. 회전축 경사는 잘 제약되지 않아,
시각 렌더링을 위해 NearStars 는 무작위 정렬 자전축에 부합하는
시선 기준 ~30° 기울임을 기본값으로 채택했습니다.

## Visual styling

NearStars 렌더러에서 τ Ceti 는 α Cen A 보다 살짝 더 차갑고 눈에
띄게 더 옅은 노란 별로 묘사됩니다. 표면 색조 hex `#ffe9c8` 는 태양형
`#fff8f0` 이나 α Cen A 의 metal-rich `#fff4e8` 보다 따뜻함이 살짝
덜한 크림-노랑을 인코딩합니다. metal-poor SED 가 물리적 이유이며
tie-break 룰이 이를 포착합니다. 선택된 색조는 Sol-노랑과 가상의
순수 G8V 흑체 사이에 위치해, 카탈로그의 다른 노란 왜성들과 나란히
놓고 비교할 때 시각적으로 구분되게 편향했습니다.

지구에서 11.91 ly (3.65 pc) 거리에서 보면 겉보기 등급 V = 3.5 로
τ Ceti 는 Cetus 자리에서 희미한 맨눈 단독성으로 쉽게 보입니다.
문화적으로는 가장 가까운 단독 태양형 별이며 Drake 의 1960 년
Project Ozma 이래 오래된 SETI 표적입니다. τ Ceti 거주가능영역의
후보 행성 (관련된 경우는 1.334 AU 의 행성 f) 에서 보면 별이 각지름
≈ 0.34° 를 채우는데, f 의 더 큰 궤도 반지름 때문에 지구에서 태양
(0.53°) 보다 작습니다. f 표면에서 본 조명 색은 같은 따뜻한 크림
색조가 metal-poor SED 와 더 낮은 Teff 의 조합으로 살짝 더 깨끗한
옅은 노랑 쪽으로 이동한 모습입니다.

흑점과 faculae 는 애니메이션 피처로 렌더링되지 않습니다. τ Ceti 는
NearStars 렌더러의 정밀도로는 분해 가능한 활동을 보이기에는 너무
조용합니다. X 선과 색채권 출력은 사이클 변조 없는 평탄한 기준선
으로 인코딩되어, α Cen A 의 19 년 태양형 사이클과 뚜렷이 대조됩니다.

이 시스템의 결정적인 시각 요소는 차가운 잔해 원반입니다. ALMA
Band 6 영상 (MacGregor 2016) 은 약 6 AU (안쪽 가장자리) 부터 ~55 AU
(바깥쪽 가장자리) 까지 뻗는 단일 넓은 고리를 분해하는데, 30 AU
근처에 표면 밀도 피크가 있고 총 먼지 질량은 약 1.2 M⊕ — 우리
카이퍼 벨트 먼지 인벤토리의 ~10–20 배입니다. NearStars 는 이를
τ Ceti 주위의 희미하고 넓고 어둑한 호박-회색 환대로 렌더링하며,
hex `#b8aa9c` 와 게임 내 opacity 0.15 로 인코딩합니다 (물리 광학적
깊이는 ~10⁻³ 이지만, cfg 는 깊은 우주 배경 대비 벨트가 알아볼 수
있게 더 높은 가시성 설정을 사용). ALMA 정밀도에서 분해된 안쪽 갭
이나 shepherding 구조는 없어서 cfg 고리는 6–55 AU 폭 전체에 걸쳐
균일합니다. metal-poor 모성이 Sol KBO analog 보다 철-reddening 이
덜한 입자를 형성했을 가능성이 있어, 태양형 metallicity 카이퍼
벨트의 더 따뜻한 황토색보다 좀 더 무채색에 가까운 grey-brown 을
정당화합니다. 이는 Basis 에 문서화된 tie-break 입니다.

행성 f / g / h 는 원반 안쪽 가장자리 안쪽의 희미한 점으로 모두
렌더링됩니다 (f 는 1.33 AU, h 는 0.24 AU, g 는 0.13 AU — 모두
6 AU 의 원반 안쪽 가장자리 훨씬 안쪽). 넓은 바깥쪽 먼지 벨트 대비
안쪽 행성계의 시각 대비가 NearStars 렌더러에서 시스템의 시그니처
프레이밍으로, 행성-만-안쪽 시스템 (TRAPPIST-1, Proxima) 과 이중성
페어 프레이밍 (α Cen A/B) 모두와 구분되는 모습입니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Greaves J. S. et al. 2004** — *The debris disk around τ Ceti:
  a massive analogue to the Kuiper Belt*, MNRAS 351, L54
  (`2004MNRAS.351L..54G`). JCMT/SCUBA 850 μm 차가운 먼지 초과 검출.
  τ Ceti 잔해 원반을 태양 카이퍼 벨트보다 ~10× 더 무거운 KBO
  analog 로 처음 식별.
- **MacGregor M. A. et al. 2016** — *Constraints on planetesimal
  collision models in debris disks*, ApJ 828, 113
  (`2016ApJ...828..113M`, arXiv:1607.06900). τ Ceti 원반의 ALMA
  Band 6 분해 영상. 단일 넓은 고리 6–55 AU. 먼지 질량 ~1.2 M⊕.
  충돌 cascade 가 부모 planetesimal 벨트를 요구. 모든 `disk_*`
  Decisions 행을 정박.
- **Pavlenko Y. V. et al. 2012** — *Spectral analysis of τ Ceti:
  abundances and age*, MNRAS 422, 542 (`2012MNRAS.422..542P`,
  arXiv:1112.1709). 태양 대비 differential LTE 분석.
  [Fe/H] = −0.55 ± 0.05. log R'HK = −4.95. Eggen 1971
  super-population 나이 7 ± 1 Gyr. 금속도, 활동도, 나이 Decisions
  행을 정박.
- **Santos N. C. et al. 2013** — *SWEET-Cat: A catalogue of
  parameters for stars with exoplanets*, A&A 556, A150
  (`2013A&A...556A.150S`, arXiv:1307.0354). 독립 분광 측정으로
  [Fe/H] = −0.49 ± 0.05 와 Teff = 5333 ± 20 K 를 얻어 Pavlenko 2012
  를 1σ 안에서 확인.
- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). 네 행성 RV 발견 (e, f,
  g, h). 호스트 질량 M = 0.783 ± 0.012 M☉ 를 Decisions 테이블이
  채택. DB Phase 2 는 행성 f, g, h 만 저장하고 e 는 누락 (Open
  items 참조).
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved age
  estimation for solar-type dwarfs using activity-rotation
  diagnostics*, ApJ 687, 1264 (`2008ApJ...687.1264M`,
  arXiv:0807.1686). τ Ceti 의 34 일 회전에 적용한 gyrochronology
  보정이 ~6.5 Gyr 를 주어 Pavlenko 2012 의 운동학 나이와 일치.
- **Baliunas S. L. et al. 1996** — *Chromospheric variations in
  main-sequence stars II*, ApJ 438, 269 (`1995ApJ...438..269B`).
  Mt Wilson Ca II H&K 서베이. τ Ceti 회전 주기 34 일. 분해 가능한
  사이클 없는 예외적으로 평탄한 HK 기록.

### Read (context / methodology, not directly decision-driving)

- **Teixeira T. C. et al. 2009** — *Solar-like oscillations in
  τ Ceti*, A&A 494, 237 (`2009A&A...494..237T`, arXiv:0811.3989).
  HARPS p-mode 검출. Δν = 169.0 ± 0.5 μHz, ν_max ≈ 4490 μHz.
  asteroseismic 질량과 반지름 cross-check.
- **Di Folco E. et al. 2007** — *VLTI/VINCI interferometric
  diameters of nearby exoplanet host stars*, A&A 475, 243
  (`2007A&A...475..243D`, arXiv:0710.1731). VINCI K 밴드 각지름.
  Teixeira 2009 asteroseismic 반지름과 일관.
- **Schmitt J. H. M. M. et al. 1985** — *EXOSAT observations of
  nearby stars: τ Ceti upper limit*. log L_X ≤ 26.5 미검출. 정적
  코로나 기준.
- **Judge P. G. et al. 2004** — *FUV spectroscopy of τ Ceti from
  FUSE: chromospheric basal flux*, ApJ 613, 1306. 정적 색채권
  기준. basal flux floor.
- **Gray R. O. et al. 2006** — *Contributions to the Nearby Stars
  (NStars) Project: spectroscopy of stars within 40 pc — south*.
  G8V 분광 분류.
- **Boro Saikia S. et al. 2018** — *Solar-type magnetic activity
  on τ Ceti from ZDI*, A&A 620, L11. Zeeman-Doppler-imaging 이
  46 일 자전을 선호. cfg 는 Baliunas 1996 canonical 34 일을 유지
  (Decisions Basis 참조).

### Read (instrument / non-cfg-decisive)

- **Lawler S. M. et al. 2014** — *Debris disks of τ Ceti and
  ε Eridani: SED modeling* (arXiv:1409.0023). SED-fit 먼지 온도와
  추정 입자 크기. MacGregor 2016 분해 영상으로 대체.

### Not read — no arXiv preprint or low-priority (~40 papers)

SETI / 레이저 방출 탐색 (Tarter 1981 Project Ozma followup, Tellis
2017, Margot 2018), 학회 초록 (EPSC/AGU/DPS), 천체생물학적 거주
가능성 추정 논문은 호스트 별에 cfg-결정적인 내용을 더하지 않습니다.
전체 필터링된 bib 는 `docs/phase3/_bib/tau-cet.yaml` 에 `status:
skipped` annotation 으로 보존됩니다.

## Open items for follow-up

- **Phase 2 disk_measurements + 행성 측정치 재수집.** DB Phase 2 는
  현재 τ Ceti 에 대한 `disk_measurements` 블록이 없습니다. Greaves
  2004 와 MacGregor 2016 는 이 Phase 3 합성을 통해서만 인용되는
  상태입니다. 향후 DB 스키마 마이그레이션에서 별 단위로
  `disk_measurements: []` 배열을 추가하고 MacGregor 2016 의 적절한
  엔트리 (안쪽/바깥쪽 반경, 먼지 질량, 분해 영상 플래그) 를 넣어야
  합니다. 마찬가지로 행성 f / g / h curated 엔트리는 현재 Msini
  외의 물리 파라미터가 비어 있어, Feng 2017 원논문 대비 반지름
  컬럼을 재검증해야 합니다.
- **τ Ceti e 큐레이션 재방문.**
  [rex-data-comparison](../reference/rex-data-comparison.md) §6 은
  NearStars 가 Feng 2017 의 행성 f, g, h 를 저장하면서 e 는 누락
  한다고 문서화합니다. 원본에서 네 행성 모두 동일한
  `pl_controv_flag` 를 받았는데도 그렇습니다. 의도적으로 제외했거나
  (e 는 네 검출 중 가장 논란이 컸음 — Feng 2017 §6 은 amplitude-to-
  noise 비율이 떨어진다고 경고) Phase 2 ingest 의 누락일 수
  있습니다. 어느 쪽이든 `db/systems/tau_cet.json::meta.notes` 에
  문서화해야 하며, follow-up Phase 3 행성 워크스페이스에서 e 를
  포함할지 인용 근거로 정식 제외할지 결정해야 합니다.
- **행성 f / g / h Phase 3 follow-up 워크스페이스.** 이 항성 전용
  합성은 행성계를 별도의 Phase 3 워크스페이스로 미룹니다. 필요한
  입력은 Feng 2017 의 질량 / 주기 / 장반경 (DB 에 이미 있음) 과 DB
  가 아직 담고 있지 않은 문헌-직접 반지름 및 평형온도 추정입니다.
  첫 번째 항목에 따라 행성 Phase 2 측정치가 재수집되면 행성
  워크스페이스가 진행될 수 있습니다.
- **τ Ceti 나이 정밀도.** 채택한 7.0 ± 1.5 Gyr 는 Pavlenko 2012 의
  super-population 운동학 추정과 Mamajek 2008 의 gyrochronology
  추정을 모두 포괄합니다. 미래의 Gaia DR4 또는 τ Ceti 의 HARPS
  p-mode 에 Joyce & Chaboyer 2018 방법론을 적용한 asteroseismic-
  evolutionary 모델링 캠페인이 이를 ±0.5 Gyr 수준으로 좁힐 수
  있으며, 이는 행성 f / g / h follow-up 의 거주가능성-역사 모델링
  에 영향을 미칩니다.
- **원반 안쪽 가장자리 미세 구조.** MacGregor 2016 ALMA 영상은
  ~6 AU 의 깨끗한 안쪽 가장자리와 일관되지만, 잡음 임계값 너머의
  희미한 안쪽 확장이나 shepherding 피처를 배제하지는 않습니다.
  미래의 더 깊은 ALMA 캠페인이나 JWST/MIRI 직접 영상이 현재 cfg
  가 무시하는 안쪽 벨트 먼지를 검출할 수 있고, 후속 Phase 3
  개정에서 필요시 두 번째 안쪽 벨트 Decisions 행을 추가할 수
  있습니다.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — 가장 가까운 단독 G2V (metal-rich, +0.24 dex). 이 합성의 구조 템플릿
- [proxima-cen](proxima-cen.md) — 가장 가까운 M 왜성. 활동도와 시각 스타일링에서 뚜렷한 대비
- [methodology](../reference/methodology.md) — Decisions 테이블의 스키마 출처
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6 이 이 합성이 Open item 으로 남긴 τ Ceti e 큐레이션 갭을 문서화
- `docs/phase3/*.md` 의 다른 entity 페이지 — 자매 Phase 3 합성들
