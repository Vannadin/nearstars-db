<!-- δ Pavonis Phase 3 합성: cfg-ready 결정과 근거 -->
# δ Pavonis — Phase 3 Synthesis

δ Pavonis (HD 190248, HIP 99240, GJ 780) 는 태양에 가장 가까운 G 형
subgiant 별 중 하나로, 거리는 6.10 ± 0.005 pc 입니다 (Gaia DR3 시차
163.95 ± 0.12 mas). 분광형 G8IV (Gray 2006 NStars, Houk & Cowley 1975)
는 주계열을 막 벗어난 단계를 의미합니다. 중심 수소가 소진되고 수소
껍질 연소가 외피를 부풀리기 시작한 시점입니다. 반지름·온도·광도는 Rains
2020 의 VLTI/PIONIER 간섭계 각지름에 anchor 합니다 (θ_LD = 1.828 ± 0.025
mas → R = 1.197 ± 0.016 R☉, Teff = 5571 ± 48 K, L = 1.24 ± 0.03 L☉).
남반구에서 가장 밝은 G subgiant 이자 인근 subgiant 연구의 교과서적
표적입니다.

δ Pav 에는 확정된 행성이 없고 (초고정밀 RV — Tinney 2005, Mawet 2017 —
와 직접 촬영 Lannier 2017 이 1 AU 밖 ~3 M_Jup 이상의 거대행성을 배제),
일부 옛 카탈로그 주장과 달리 **잔해 원반도 없습니다**. 가장 깊은 관측
(Eiroa 2013 DUNES, Herschel/PACS 70/100/160 µm) 이 δ Pav 를 비검출
(non-excess) 별로 분류하며, 표본에서 가장 낮은 축의 분율 광도 상한
L_dust/L_★ < 5×10⁻⁷ 을 줍니다.

**NearStars 시나리오 선택. 행성도 잔해 ring 도 없이 홀로 선, 늙고 매우
조용한 G8 subgiant 별입니다.** G8V 왜성보다 약간 부풀고 약간 더 붉습니다.
모든 항성 파라미터는 canonical 정렬이며 직접 측정에 anchor 합니다 (R/Teff/L
은 간섭계, 질량은 성진학). 본질적으로 불확실한 양은 나이 하나뿐으로, 두
isochrone 분석이 서로 발산합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G8IV | high | Gray 2006 NStars, Houk & Cowley 1975 MK 카탈로그. HR 도 위치로 subgiant 분류 확인 |
| `mass_msun` | 1.07 ± 0.13 | medium | Bruntt 2010 asteroseismic scaling (ν_max). Bensby 2014 진화값 1.03 과 1σ 내 일치 |
| `radius_rsun` | 1.197 ± 0.016 | high | Rains 2020 VLTI/PIONIER 간섭계, θ_LD = 1.828 ± 0.025 mas. Bruntt 2010 asteroseismic 1.20 과 일치 |
| `teff_k` | 5571 ± 48 | high | Rains 2020 간섭계 θ_LD + bolometric flux. Bruntt 2010 분광 5550 K 과 일치 (Gaia DR3 GSP-Phot 은 이 금속풍부 별에서 편향) |
| `luminosity_lsun` | 1.24 ± 0.03 | high | Rains 2020 bolometric flux 적분. Bruntt 2010 의 1.22 L☉ 와 일치 |
| `metallicity_fe_h_dex` | +0.36 ± 0.02 | high | Gomes da Silva 2021 AMBRE-HARPS. Bensby 2014 +0.37, Bruntt 2010 +0.33 이 뒷받침, super-solar |
| `age_gyr` | 9.3 (5.8–10.7) | medium | Holmberg 2009 GCS III isochrone. 매우 낮은 활동도 (log R'HK −5.13) + 느린 회전과 일관. Bensby 2014 isochrone 4.9 Gyr (3.3–9.6) 와 발산 — 두 범위가 겹쳐 나이는 본질적으로 불확실 |
| `rotation_period_days` | ~35 (불확실) | low | 측정된 주기 없음. vsini ≈ 1.7 km/s (Bruntt 2010) + R = 1.197 R☉ → P_rot ≲ 36 d (sin i ≤ 1). 매우 낮은 활동도가 느린 회전을 지지 |
| `activity_log_rhk` | −5.13 | high | Gomes da Silva 2021 HARPS (6002 스펙트럼, 2003–2016). Henry 1996 −4.999 와 일치. 알려진 G subgiant 중 색채권 활동이 가장 약한 축 |
| `activity_cycle_years` | 미상 | low | Mt. Wilson 장기 모니터링 커버리지 없음. 이 진화 단계의 subgiant 는 약화되거나 불규칙한 사이클을 보이는 경우가 많음 |
| `x_ray_log_lx_cgs_max` | 27.3 | medium | Hünsch 1998 ROSAT 검출 (0.073 ct/s) → log L_X ≈ 27.3 erg/s, log(L_X/L_bol) ≈ −6.4. 약하지만 검출된 코로나 |
| `limb_darkening_alpha_h` | 0.16 ± 0.02 | medium | Claret 2011 LD 표에서 Teff = 5571 (Rains 2020) 의 G8IV 로 유도. 간섭계 직접 LD 측정은 없음 |
| `visual_surface_tint_hex_primary` | `#ffe8c8` (G2V Sol 보다 더 붉은 amber-cream) | medium | Tie-break. G8IV 흑체 5571 K + +0.36 dex 금속도 reddening. subgiant envelope 부풀림이 disk integrated 색을 같은 Teff 의 G8V 보다 살짝 더 붉게 시프트 |
| `stellar_color_temp_k` | 5571 | high | Teff (Rains 2020) 유도 |
| `visual_corona_extent_radii` | 1.6 | low | Tie-break. 약한 색채권 + 낮은 log R'HK = −5.13 → 절제된 corona band. 태양형 더 밝은 halo 대신 얇은 ring 으로 렌더 |
| `disk_present` | false | high | Eiroa 2013 DUNES 비검출, L_dust/L_★ < 5×10⁻⁷ (Herschel/PACS 70/100/160 µm 전부 광구와 일치). 잔해 ring 없음 |

## Surface synthesis

δ Pavonis 는 짧지만 시각적으로 중요한 subgiant 단계에 있습니다. 중심
수소가 소진되고 얇은 수소 연소 껍질이 외피를 부풀리기 시작하며, 별은
subgiant 가지를 따라 적색거성 가지 바닥으로 올라가는 중입니다. 그 결과
광구는 같은 질량의 G8V 왜성보다 ~20% 크고 ~200 K 더 차갑습니다. 광도
1.24 L☉ 는 — 반지름 증가가 온도 하락을 앞지르기에 G8V 유사 별보다 살짝
더 밝습니다 — 색은 태양보다 붉으면서도 밝기는 약간 더 높은 역설적
성격을 줍니다.

disk integrated 색은 G2V 태양 대비 amber-cream 쪽으로 뚜렷이 이동합니다.
Teff = 5571 K 에서 흑체 정점은 약 520 nm — 여전히 황록이지만, 가시
파장에 걸친 기울기가 G2V 보다 완만해 Sol 보다 붉은 쪽이 많고 푸른 쪽이
적습니다. +0.36 dex 의 super-solar 금속도가 line blanketing 으로 가시
연속체를 더 붉히면서, cfg tint `#ffe8c8` 가 진화한 G8 별의 따뜻한 cream
을 담아냅니다. α Cen A 의 `#fff4e8` (5847 K G2V) 와의 대비는 나란히
렌더하면 실제로 보입니다.

Limb darkening 은 G2V 보다 강합니다. 더 차갑고 확장된 대기가 limb 근처
에서 광자 평균자유행로가 더 길기 때문입니다. H 밴드 α 지수 ≈0.16 (Claret
2011 LD 표를 G8IV 로 보간) 은 α Cen A 의 측정값 0.14 보다 ~15% 높아,
fly-by 렌더에서 limb 가 G2V 왜성보다 뚜렷이 더 그늘진 미묘하지만 실제적인
효과를 냅니다.

흑점 커버리지는 보통입니다. 측정된 자전 주기나 사이클이 없어 광도 변광
제약은 느슨하지만 (Hipparcos H_p 진폭 < 0.005 mag), log R'HK = −5.13
(Gomes da Silva 2021) 은 δ Pav 를 비활동 G subgiant 자리에 확고히
놓습니다 — α Cen A 보다 조용하고, Mt. Wilson 표본에서 자기적으로 가장
죽은 별들에 견줄 만합니다. cfg 렌더러에서는 흑점 밀도를 태양 극대값의
절반으로, 무작위 분포에 사이클 변조 없이 설정합니다.

## Atmosphere synthesis

δ Pav 의 색채권과 코로나도 그만큼 약합니다. 색채권 Ca II H&K 코어 플럭스
log R'HK = −5.13 (Gomes da Silva 2021, HARPS 6002 스펙트럼. Henry 1996
−4.999) 은 더 이상의 활동 감소가 관측되지 않는 색채권 "basal flux floor"
근처에 있습니다 — δ Pav 는 사실상 이 진화 단계의 자기 정적 점근선에
도달했습니다. ROSAT 검출 (Hünsch 1998) 은 log L_X ≈ 27.3 (cgs, 0.5–2
keV), 즉 log(L_X/L_bol) ≈ −6.4 을 주며, 약하지만 실재하는 코로나입니다.
태양 활동 극소보다 한 자릿수 약하며, 주계열을 벗어나며 대류가 약해지는
것과 일관됩니다.

전이영역 UV 방출도 그만큼 희미하지만, δ Pav 는 IUE 와 HST/STIS 로
관측됐고 Mg II h&k 와 Si IV 방출선이 약하지만 0 이 아닌 강도로
검출됐습니다. 측정된 플레어는 없습니다 — δ Pav 는 인근 표본에서 가장
플레어가 조용한 별 중 하나로, 어떤 모니터링 캠페인에서도 사건이 보고된
적 없습니다. 적분 XUV 광도는 ≲ 10⁻⁵ L_bol 로, 시스템의 ~9 Gyr 전 기간에
걸쳐 안쪽 후보 행성의 대기를 침식할 임계보다 훨씬 낮습니다.

이 온화한 우주 날씨 상태는 가상의 (현재 미확정) 행성에 흥미로운 함의를
줍니다. δ Pav 의 거주가능영역 — Kopparapu 2013 보수적 한계를 1.24 L☉ 로
스케일하면 대략 1.0–1.7 AU — 에서 XUV 구동 대기 탈출은 시스템 전 수명에
걸쳐 무시할 만합니다. cfg 는 의미 있는 CME 플럭스가 없는 온화한 항성풍
환경을 인코딩해 인게임 대기 보존 모델링에 씁니다.

광구 자체의 항성 대기는 색채권 onset 에서 canonical 한 G8IV 온도 역전을
보입니다. T 는 τ=1 의 5571 K 에서 τ ≈ 10⁻⁴ 부근 약 4200 K 의 온도
최소로 떨어진 뒤, 색채권을 거쳐 ~10⁴ K, 전이영역에서 ~10⁵ K 로
상승합니다. 차가운 온도 최소는 G2V Sol 보다 깊고 넓으며, 더 크고 느리게
대류하는 외피의 낮은 음향 플럭스의 특징입니다.

## Rotation & spin synthesis

δ Pavonis 는 느리게 자전합니다 — 정확히 얼마나 느린지는 잘 모릅니다.
투영 자전 속도 v sin i ≈ 1.7 km/s (Bruntt 2010. Valenti & Fischer 2005
도 유사값) 와 R = 1.197 R☉ 를 결합하면 주기는 위로만 제한됩니다.
P_rot · sin i ≤ 36 d 이므로 i = 90° (적도 정면) 에서 P_rot ≤ 36 d, 전형
적 무작위 경사에서는 가장 그럴듯한 주기가 ~30 d 입니다.

G8V zero-age 주계열 자전 ~5 d 에서 출발해 ~9 Gyr 로 P ∝ √t 스케일한
Skumanich braking 은 ~55 d 를 예측합니다 — 다만 subgiant 팽창이 외피
부풀림에 따른 각운동량 보존으로 표면 자전을 더 늦춥니다. Spada & Lanzafame
2020 subgiant 자전 모델은 이 단계에서 30–45 d 를 예측합니다. cfg 는 35 d
를 window 내 추정으로 채택하고 Confidence=low 로 표기하며, 향후 광도
모니터링을 open item 으로 남깁니다.

성진학 진동은 검출됐습니다 — Bruntt 2010 이 p-mode 를 처음 측정했고,
Lund 2025 (TESS) 가 ν_max = 2269.8 ± 64.4 µHz, Δν = 107.9 ± 0.2 µHz 로
정밀화했습니다 — 그러나 어떤 캠페인도 아직 모드의 자전 분리를 분해하지
못했고, 그것이 주기와 경사를 고정할 것입니다. 향후 PLATO 캠페인이 이를
조일 것이며, cfg open item 이 그 의존성을 기록합니다.

Obliquity 는 관측적으로 미제약입니다. 자전축을 토크할 동반자가 없는 고립
단일 별이므로, 자전 각운동량 기준틀에 대해 obliquity = 0° 를 기본값으로
둡니다. cfg 는 시각적 연출을 위한 특별한 기울임 없이 0° 를 window 내
기본값으로 인코딩합니다.

## Visual styling

NearStars 렌더러에서 δ Pavonis 는 행성도 잔해 ring 도 동반자도 없는,
늙고 조용한 고립 G8 subgiant 로 묘사됩니다. 핵심 시각 선택은 다음과
같습니다.

- **Global appearance** — 따뜻한 amber-cream 항성 disk (`#ffe8c8`).
  α Cen A 의 cream-white 보다 뚜렷이 붉지만 K 왜성 orange 보다는 따뜻한
  tint 입니다. G2V Sol 과 나란히 두면 대비가 미묘하지만 실재하며, 행성
  하늘에 홀로 있으면 δ Pav 는 "살짝 붉고 살짝 큰, 지친 태양"으로 읽힙니다.
- **Disk detail** — 가상의 근접 fly-by 에서 광구 granulation 은 G2V 보다
  ~5% 낮은 대비로 렌더됩니다. 더 크고 느리게 대류하는 외피가 뜨거운 상승
  plume 과 차가운 intergranular lane 사이 온도차를 더 얕게 만들기
  때문입니다. Granulation cell 은 각크기가 ~30% 큽니다 (R★ 로 스케일).
- **Limb appearance** — α Cen A 보다 limb 쪽이 뚜렷이 더 어둡습니다. 더
  차가운 광구와 oblique 시야각에서 강한 H⁻ 불투명도 때문입니다. fly-by
  렌더에서 limb 가 눈에 띄게 그늘집니다.
- **Corona / chromosphere** — 1.6 R★ (`visual_corona_extent_radii`) 의
  얇고 희미한 ring 으로 렌더됩니다. 매우 약한 색채권·코로나 방출을
  반영합니다. 활동성 prominence 렌더 없음, 플레어 시각 없음.
- **Spots / faculae** — 태양 극소 진폭의 절반으로, 저위도에 무작위 분포
  하며 현재 cfg 에서 사이클 변조 없음.
- **No debris ring** — 초기 NearStars 초안은 30–80 AU 에 차가운 잔해
  ring 을 붙였지만, 이는 조작된 인용에서 비롯된 것으로 밝혀졌습니다.
  Eiroa 2013 DUNES 는 깨끗한 비검출입니다 (L_dust/L_★ < 5×10⁻⁷). δ Pav 는
  어떤 종류의 주위 ring 도 없이 렌더됩니다.
- **Apparent diameter from candidate HZ** — 1.3 AU 의 가상 1 M⊕ 행성은
  δ Pav 가 각지름 ~0.50° 를 채우는 것을 보게 됩니다. 지구에서 본 Sol
  (0.53°) 과 견줄 만합니다.
- **Isolation cue** — α Cen 계의 쌍성 렌더와 달리 δ Pav 는 홀로 섭니다.
  두 번째 태양 없음, 궤도 합 사건 없음, ring 없음. 시각 연출은 subgiant
  색과 부풀어 limb darkening 된 disk 에 기댑니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Rains A. D. et al. 2020** — *Precision angular diameters for 16
  southern stars with VLTI/PIONIER* (`2020MNRAS.493.2377R`,
  [arXiv:2004.02343](https://arxiv.org/abs/2004.02343)). 직접 간섭계 θ_LD = 1.828 ± 0.025 mas → R = 1.197 ±
  0.016 R☉, Teff = 5571 ± 48 K, L = 1.24 ± 0.03 L☉. 반지름·온도·광도의
  anchor.
- **Bruntt H. et al. 2010** — *Accurate fundamental parameters for
  23 bright solar-type stars* (`2010MNRAS.405.1907B`,
  [arXiv:1002.4268](https://arxiv.org/abs/1002.4268)). δ Pav 의 성진학 + 분광 분석. 성진학 M = 1.07 ± 0.13
  M☉, R = 1.20 R☉, Teff ≈ 5550 K, [Fe/H] = +0.33, v sin i ≈ 1.7 km/s.
  질량과 자전의 anchor.
- **Gomes da Silva J. et al. 2021** — *Stellar chromospheric activity
  of 1674 FGK stars from the AMBRE-HARPS sample* (`2021A&A...646A..77G`).
  HARPS 6002 스펙트럼에서 log R'HK = −5.13. [Fe/H] = +0.36 ± 0.02.
  활동도와 금속도의 anchor.
- **Eiroa C. et al. 2013** — *DUNES: DUst around NEarby Stars,
  observational results* (`2013A&A...555A..11E`, [arXiv:1305.0155](https://arxiv.org/abs/1305.0155)).
  Herschel/PACS 서베이. δ Pav 는 **비검출 (non-excess)** 별로,
  L_dust/L_★ < 5×10⁻⁷ — `disk_present = false` 의 근거.
- **Bensby T. et al. 2014** — *Exploring the Milky Way stellar disk:
  714 F and G dwarf stars* (`2014A&A...562A..71B`, [arXiv:1309.2631](https://arxiv.org/abs/1309.2631)).
  FEROS 고분해 분광. [Fe/H] = +0.37, 질량 1.03 M☉, isochrone 나이 4.9
  Gyr — 나이 발산의 젊은 쪽.
- **Holmberg J., Nordström B., Andersen J. 2009** — *The
  Geneva-Copenhagen survey III* (`2009A&A...501..941H`,
  [arXiv:0811.3982](https://arxiv.org/abs/0811.3982)). Isochrone 나이 9.3 Gyr (5.8–10.7) — 채택한 (더 늙은)
  나이로, 매우 낮은 활동도와 일관.

### Read (context / methodology, not directly decision-driving)

- **Lund M. N. et al. 2025** — *The TESS Legacy Sample of Bright
  Stars. I.* (`2025A&A...701A.285L`, [arXiv:2508.08699](https://arxiv.org/abs/2508.08699)). δ Pav 의 현대
  TESS 성진학 검출. ν_max = 2269.8 ± 64.4 µHz, Δν = 107.9 ± 0.2 µHz
  (모델링된 M/R/age 는 미발표).
- **Spada F. et al. 2011** — *Stellar evolutionary models*
  (`2011MNRAS.416..447S`, [arXiv:1105.3125](https://arxiv.org/abs/1105.3125)). δ Pav 의 질량/나이에 대한
  subgiant 진화 맥락.
- **Mawet D. et al. 2017** — *Characterization of Exoplanets from
  Their Formation. I.* (`2017AJ....153...44M`, [arXiv:1609.06163](https://arxiv.org/abs/1609.06163)).
  NIRC2 vortex coronagraph. 1 AU 밖 ~3 M_Jup 동반자 한계.
- **Lannier J. et al. 2017** — *Combining direct imaging and radial
  velocity* (`2017A&A...603A..54L`, [arXiv:1705.03477](https://arxiv.org/abs/1705.03477)). SPHERE 직접
  촬영 서베이의 δ Pav. 동반자 미검출.
- **Tinney C. G. et al. 2005** — *The Anglo-Australian Planet Search*
  (`2005ApJ...623L.121T`). δ Pav RV 모니터링. 행성 미검출 — RV 비검출
  기준선.
- **Henry T. J. et al. 1996** — *A survey of Ca II H and K
  chromospheric emission in southern solar-type stars*
  (`1996AJ....111..439H`). log R'HK = −4.999. 비활동 분류를 뒷받침.
- **Hünsch M. et al. 1998** — *ROSAT all-sky survey catalogue of
  nearby stars* (`1998A&AS..132..155H`). δ Pav X 선 검출, 0.073 ct/s →
  log L_X ≈ 27.3 cgs.
- **Gray R. O. et al. 2006** — *NStars: Spectral Classifications of
  Nearby Stars* (`2006AJ....132..161G`, arXiv:astro-ph/0603770).
  G8IV 분류 확인.

## Open items for follow-up

- **TESS 모드 기반 성진학 질량/나이**. Lund 2025 가 δ Pav 의 ν_max + Δν
  를 발표했으나 모델링된 M/R/age 는 없습니다. scaling 관계나 grid 모델
  해 (또는 자전 분리를 분해하는 PLATO 캠페인) 가 질량을 조이고 Holmberg
  대 Bensby 나이 발산 (9.3 대 4.9 Gyr) 을 해소해 `age_gyr` Confidence 를
  high 로 올릴 것입니다.
- **광도 자전 주기**. TESS Cycle 4+ 가 δ Pav 를 관측해야 합니다 (남쪽
  적위 유리). 깨끗한 자전 주기 검출이 현재 Confidence=low 인 ~35 d
  추정을 대체할 것입니다.
- **금속도 불확실도**. Bensby 2014 카탈로그 [Fe/H] 오차가 깔끔히 고정되지
  않았습니다. 채택한 +0.36 ± 0.02 (Gomes da Silva 2021) 는 더 조인 함량이
  필요할 때 Bensby 의 형식 오차와 교차검증해야 합니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 표 스키마의 원본.
- [alpha-centauri-a](alpha-centauri-a.md) — G2V 비교 anchor (5847 K cream-white vs δ Pav 의 5571 K amber-cream).
- [conflict-resolution](../../../.claude/skills/nearstars-phase3/references/conflict-resolution.md) — 시각 색조와 corona extent 픽에 사용된 tie-break 정책.
