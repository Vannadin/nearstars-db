<!-- 티가든 별 Phase 3 합성. cfg-ready 결정과 근거 -->
# Teegarden's Star — Phase 3 Synthesis

티가든 별 (GJ 번호 없음. Karmn J02530+168. LSPM J0253+1652) 은
3.831 pc 거리의 M7.0 V 초저온 왜성으로 (Gaia 시차 261.01 mas), 태양에서
24번째로 가까운 별이자 M7 V 이후 분광형 가운데 가장 밝은 대표
천체입니다 (Zechmeister et al. 2019). 이렇게 가까운데도 맨눈에는 보이지
않습니다. V = 15.08 (J = 8.39) 으로 광학 플럭스가 분자 밴드에 거의 다
질식당하고, 별은 압도적으로 근적외선에서 복사합니다. NearStars
카탈로그에서 가장 차가운 호스트 중 하나로, Teff = 2904 K 의 광구는
바너드 별 (3195 K) 보다 약 290 K 차갑고 더 깊고 진한 빨강으로
렌더링됩니다.

기본 파라미터는 frozen Phase 2 레이어에서 가져오며, 모두 Schweitzer
et al. 2019 (CARMENES) 에서 옵니다. 유효온도 Teff = 2904 ± 51 K 는
PHOENIX 합성 스펙트럼 피팅에서 왔고, 광도 L = 0.00073 ± 0.00001 L☉
는 — 태양의 약 1/1370 로 이 집합에서 가장 어둡습니다 — bolometric
flux (Gaia DR2 시차 + 통합 측광) 에서 왔으며, 반지름 R = 0.107 ±
0.004 R☉ 는 L 과 Teff 로부터 **Stefan-Boltzmann 법칙** 을 통해
나왔지, 간섭계에서 온 게 아닙니다. 이 점은 분명히 짚을 가치가
있습니다. 3.831 pc 거리에 R = 0.107 R☉ 라면 사지 어두워짐 보정
각지름은 겨우 ~0.032 mas 로, 기존 어떤 광학 간섭계의 분해능 바닥보다도
한 자릿수 이상 아래입니다 — 그래서 바너드 별 (0.95 mas 지름을 CHARA
가 직접 분해)과 달리 티가든 별은 **간섭계 반지름이 없고 지상에서는
앞으로도 결코 얻을 수 없습니다**. SED 피팅이 유일한 길입니다. 질량
M = 0.089 ± 0.009 M☉ 는 Schweitzer 가 그 SED 반지름에 적용한 자체
선형 질량-반지름 관계에서 옵니다. 금속도 [Fe/H] = −0.19 ± 0.16
(Schweitzer 2019) 은 recommended 값이지만 documented divergence 를
안고 있고 (Canonical alternatives 참조), 반지름/질량 자체도 Dreizler
2024 재유도와의 두 번째 divergence 를 안습니다.

NearStars 에서 티가든 별을 규정하는 건 주계열 맨 밑바닥에서의 극단적인
노령과 극단적인 정적 상태입니다. 나이는 7 ± 3 Gyr (Zechmeister et al.
2019) 로, PARSEC Bayesian 추정이며 두꺼운 원반 운동학 (W = −58.7 km/s)
및 Hα 활동도 바닥에서 나온 8.0(+0.5/−1.0) Gyr 와 일관됩니다 — 별은
은하의 진화한 종족에 속합니다. 자전은 그에 걸맞게 매우 느려서
P_rot = 96.2 d (Lafarga et al. 2021, 분광 활동 지표. Dreizler 2024 가
채택) 인데, 이는 느리게 자전하는 극저질량 왜성 가운데서도 티가든 별을
거의 outlier 로 만듭니다. 코로나 활동은 낮습니다. log(Lx/Lbol) = −4.9
(Fuhrmeister et al. 2025, 정적 Chandra 검출) 이고, 색채권은 M7 V
치고 조용합니다 — 평균 Hα 는 방출이 아니라 채워져 있습니다. "조용함" 이
무력함을 뜻하지는 않습니다. 같은 Fuhrmeister 2025 캠페인은 큰 TESS
flare 둘 (총 에너지 ~10³¹–10³² erg, 가장 큰 태양 flare 에 필적)
과 분출하는 프로미넌스의 단서를 포착했습니다.

티가든 별은 **온대 지구질량 행성의 조밀한 시스템** 을 거느립니다. b 와
c (각각 최소질량 ~1.1 M⊕, P = 4.91 d 와 11.4 d. Zechmeister et al.
2019) — 시선속도로 초저온 왜성 주위에서 발견된 첫 지구질량 행성들 —
에 더해 세 번째 행성 d (0.82 M⊕, P = 26.13 d. Dreizler et al. 2024)
입니다. 각각은 개별 Phase 3 합성 (`teegardens-star-b/c/d`) 에서
다룹니다.

**NearStars 시나리오 선택. 고대의, 깊은 붉은빛의, 매우 조용한 M7 V
초저온 왜성으로 — 자기 분광형에서 가장 밝지만 카탈로그에서 가장 어두운
호스트 — 96 일 주기로 매우 느리게 자전하며, 낮은 정적 활동도에 드문
큰 flare 가 박혀 있는 모습으로 렌더링합니다.** 항성 레이어는 frozen
Phase 2 출처 (Schweitzer 2019 의 Teff/광도/반지름/질량/금속도,
Zechmeister 2019 의 나이와 분광형, Lafarga 2021 의 자전 — Dreizler
2024 경유 —, Fuhrmeister 2025 의 활동) 위에 정박합니다. 두 파라미터가
문헌에 걸쳐 documented divergence 를 안고 있는데 — 반지름/질량 쌍
(Schweitzer SED 대 Dreizler 진화모델, 반지름에서 ~3σ) 과 금속도
(Schweitzer 대 Rojas-Ayala, ~0.36 dex) — `## Canonical alternatives`
에서 다룹니다. tie-break 하나가 2904 K M7 V SED 의 시각 표면 색조를
정합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M7.0 V | high | Alonso-Floriano et al. 2015 (Zechmeister 2019 Table 1 경유). 초저온 왜성으로, M7 V 이후 분광형 중 가장 밝은 대표 천체 |
| `mass_msun` | 0.089 ± 0.009 | high | Schweitzer et al. 2019 — CARMENES, SED 반지름에 적용한 선형 질량-반지름 관계 (Phase 2 recommended). DOCUMENTED DIVERGENCE. Dreizler 2024 진화모델 재유도는 0.097 ± 0.010 — Canonical alternatives 참조 |
| `radius_rsun` | 0.107 ± 0.004 | high | Schweitzer et al. 2019 — L 과 Teff 로부터 Stefan-Boltzmann (SED 피팅). **간섭계 반지름 불가능** (θ_LD ~0.032 mas, 간섭계 바닥보다 한참 아래). DOCUMENTED DIVERGENCE. Dreizler 2024 는 0.120 ± 0.012 (~3σ) — Canonical alternatives 참조 |
| `teff_k` | 2904 ± 51 | high | Schweitzer et al. 2019 — CARMENES 스펙트럼에 PHOENIX 합성 스펙트럼 피팅 (Phase 2 recommended). 바너드 별보다 ~290 K 차갑고, 이 집합에서 가장 차가운 호스트 중 하나 |
| `luminosity_lsun` | 0.00073 ± 0.00001 | high | Schweitzer et al. 2019 — Gaia DR2 시차 + 통합 측광에서 구한 bolometric flux (Phase 2 recommended). 태양의 약 1/1370 로, 카탈로그에서 가장 어두운 호스트 |
| `metallicity_fe_h_dex` | −0.19 ± 0.16 | medium | Schweitzer et al. 2019 — 고분해능 분광 (Phase 2 recommended). DOCUMENTED DIVERGENCE. Rojas-Ayala 2012 K-band 는 −0.55 ± 0.17 (~0.36 dex) — Canonical alternatives 참조 |
| `age_gyr` | 7 ± 3 | medium | Zechmeister et al. 2019 — PARSEC Bayesian (운동학 / 두꺼운 원반. W = −58.7 km/s). Hα 활동도 바닥 나이 8.0(+0.5/−1.0) Gyr 및 더 넓은 8–10 Gyr 범위와 일관 |
| `rotation_period_days` | 96.2 | medium | Lafarga et al. 2021 (분광 활동 지표), Dreizler 2024 가 채택 (Phase 2 recommended). 형식 불확실도는 제시되지 않음. 독립 추정들이 96–100 d 에 모임 (Terrien 2022, Kemmer 2023) |
| `activity_log_lx_lbol` | −4.9 | high | Fuhrmeister et al. 2025 — 정적 Chandra X-선 검출 (Phase 2 recommended). XMM-Newton 정적 범위 −5.0 ~ −4.81 로 일관. Zechmeister 2019 상한 <−4.23 을 대체 |
| `flare_state` | rare large flares | medium | Fuhrmeister et al. 2025 — TESS flare 둘, 총 에너지 ~10³¹–10³² erg (가장 큰 태양 flare 에 필적), 분출 프로미넌스 단서. flare 율 ~2.6 ± 1.8 / 100 d 이나 집중됨 — 대부분 시간은 정적 |
| `v_sin_i_km_s` | ~0.06 | low | R = 0.107 R☉ 과 P_rot = 96.2 d 에서 유도 (적도 속도 ~0.056 km/s). 어떤 분광 선폭 임계값보다도 한참 아래 — 선폭 측면에서 사실상 비자전체 |
| `visual_surface_tint_hex_primary` | `#c23a1c` (M7 V 의 깊고 진한 빨강) | medium | Tie-break. 2904 K 흑체에서 TiO/VO/H₂O 분자 밴드가 파란 쪽을 강하게 억제한 뒤. M4 V 바너드 `#cf5a30` (Teff 가 ~290 K 더 뜨거움) 과 M5.5 Proxima `#c54c2a` 보다 붉고 진함 |
| `stellar_color_temp_k` | 2904 | high | Teff 유도 (Schweitzer 2019) |
| `apparent_magnitude_v_from_earth` | 15.08 | high | Zechmeister 2019 / Carmencita. 3.831 pc 근접에도 맨눈 가시성에 한참 못 미침. 0.00073 L☉ 의 작은 광도 때문 (J 에서는 8.39 mag 로 훨씬 밝음) |
| `distance_pc` | 3.831 ± 0.004 | high | Gaia DR2 (Zechmeister 2019 경유). 태양에서 24번째로 가까운 별 |

## Surface synthesis

티가든 별은 카탈로그에서 가장 깊고 진한 붉은 광구를 가집니다.
Teff = 2904 K (Schweitzer 2019) 에서 SED 는 근적외선 ~1.0 μm 깊숙이
에서 정점을 이루고, 광학 연속체는 거의 완전히 억제됩니다 — 이 온도
에서는 TiO, VO, 물 밴드가 스펙트럼을 너무 철저히 지배해, Fuhrmeister
2025 가 적었듯 "늦은 M 왜성은 식별 가능한 연속체를 보이지 않습니다."
이것이 별이 가장 밝은 M7 V 대표인데도 지구에서는 V = 15.08 로만 빛나면서
근적외선에서는 J = 8.39 에 이르는 이유입니다. R = 0.107 R☉ 에서 광도는
겨우 0.00073 L☉ — 태양의 약 1/1370 — 이라 티가든 별은 이 집합에서 가장
어두운 호스트입니다.

반지름 자체가 핵심 표면 사실입니다. 0.187 R☉ 가 직접 분해된 CHARA
간섭계 지름에 정박한 바너드 별과 달리, 티가든 별은 기존 어떤 간섭계로도
분해할 수 없습니다. 사지 어두워짐 보정 각지름이 겨우 ~0.032 mas 로,
분해능 바닥보다 열 배 이상 아래이기 때문입니다. 그래서 cfg 반지름은 SED
량입니다 — Schweitzer 2019 가 Gaia 측광에서 L 을, 분광 피팅에서 Teff 를
얻은 뒤 Stefan-Boltzmann 으로 R 을 닫았습니다. 이것이 주계열 맨 밑바닥
에서 쓸 수 있는 유일한 길이며, 반지름이 Dreizler 2024 진화모델 값
(0.120 R☉) 과 documented ~3σ divergence 를 안는 이유입니다. 태양 아래
금속도 [Fe/H] = −0.19 (Schweitzer 2019) 는 태양형 금속도 M7 V 대비 분자
밴드 blanketing 을 미세하게 줄이지만, 이는 게임 내 조명 색의 분해능에서는
보이지 않습니다.

표면의 결정적 특성은 주계열 맨 밑바닥에서의 정적 상태입니다. 티가든
별은 "자기 분광형치고 자기적으로 비교적 조용" 합니다 (Zechmeister
2019). Reiners & Basri 2010 의 M7–M7.5 V 왜성 24개 중 Hα 가 이만큼
어두운 건 하나뿐입니다. 평균 log(LHα/Lbol) = −5.25 는 별을 West 2008
활동도 임계값 아래에 놓아 — M7 V 치고 형식적으로 비활동적이며, 노령의
지문입니다. cfg 렌더링에서는 이것이 흑점 면적이 낮은 거의 균일한 깊은
붉은 디스크를 뜻하며, 카탈로그 다른 곳의 진한 어린 flare star 와
의도적으로 대비됩니다. Granulation 은 M-왜성 전형으로, 얕은 광구 압력
스케일 높이가 정하는 작은 대류 셀을 가집니다.

## Atmosphere synthesis

티가든 별의 외곽 대기는 드문 격렬한 박자가 박힌 정적 상태에
지배됩니다. 코로나 활동 log(Lx/Lbol) = −4.9 (Fuhrmeister 2025, 정적
Chandra 검출. XMM-Newton 정적 범위 −5.0 ~ −4.81) 은 낮고, 색채권은
조용합니다. 평균 Hα 는 방출이 아니라 채워져 있고, He I 적외선 삼중선은
모든 스펙트럼에서 부재합니다 — 둘 다 그 분광형의 낮은 정적 활동도
바닥의 표지입니다. 96 일 자전 주기와 그로 인한 매우 큰 Rossby number 는
별을 비포화, 자기 braking 된 영역 깊숙이 놓는데, 거기서는 자전-활동
관계가 정확히 바닥 수준 방출을 예측합니다.

결정적 단서 하나는 표준 색채권 지수 Ca II H&K log R'HK 가 티가든 별에
대해 지상에서 **측정 불가능** 하다는 점입니다. M7 V 에서는 지수를
정의할 식별 가능한 광구 연속체가 없어, 활동도는 방출선 (Hα, 더 높은
Balmer 선) 의 pseudo-equivalent width 와 X-선으로 대신 특성화해야
합니다 — 바로 Fuhrmeister 2025 가 택한 길입니다. 이것은 open item 으로
표시합니다. cfg 는 더 뜨거운 호스트에 쓰는 log R'HK 대신
log(Lx/Lbol) = −4.9 를 활동도 정박값으로 씁니다.

정적이라고 무력한 건 아닙니다. Fuhrmeister 2025 TESS 모니터링은 총
광학 에너지 ~10³¹–10³² erg 의 — 지금껏 기록된 가장 큰 태양 flare 에
필적하는 — 큰 flare 둘에 더해, X-선 flare (하나는 Neupert 효과를 보여
경 X-선 생성을 함의) 와 코로나 질량 방출을 구동했을지 모를 분출
프로미넌스의 단서를 포착했습니다. 함의되는 flare 율은 ~2.6 ± 1.8 /
100 d 이지만, flare 둘이 단일 TESS 섹터에 몰려 있어 별이 잔잔한 구간과
더 활동적인 에피소드 사이를 오감을 시사합니다. cfg 측면에서 flare 는
드문 사건의 박자 찍기일 뿐 — 활동적인 어린 M 왜성의 거의 연속적인
flare 와는 다릅니다 — 그밖에는 낮은 정적 XUV 배경에 올라탑니다.
가까운 지구질량 행성들 (b 는 P = 4.91 d) 에 대해 시간 평균 조사량은
부드럽지만, 드문 큰 flare 와 궤도 근접성은 그래도 별의 수 Gyr 수명에
걸쳐 무시할 수 없는 누적 XUV 선량을 부과합니다.

## Rotation & spin synthesis

96.2 일 자전 주기 (Lafarga et al. 2021, 분광 활동 지표에서. Dreizler
2024 가 채택) 는 M 왜성 카탈로그에서 가장 긴 축에 들며 나이의 직접적
지문입니다. ~7 Gyr 수명 동안 티가든 별은 자기 (Skumanich 식) braking
으로 초기 각운동량 거의 전부를 잃고 현재의 거의 정지에 가까운 상태로
spin down 했습니다. 독립 측정들이 빡빡하게 모입니다 — 96 d (Lafarga
2021), ~100 d (Terrien 2022), 98 d (Kemmer 2023) — 그래서 형식
불확실도가 제시되지 않았어도 주기는 robust 합니다. cfg 는 medium
confidence 로 기록합니다. 함의되는 적도 속도는 겨우 ~0.056 km/s 라,
v sin i 는 어떤 분광 선폭 분석의 검출 임계값보다도 한참 아래입니다 —
측정값이 아니라 유도량으로서 low confidence 의 ~0.06 km/s 로 기록합니다.

짚어 둘 진짜 모호성이 하나 있습니다. Dreizler 2024 는 시선속도와 활동
지표에서 coherent 한 ~172 d 신호를 찾아 *그것* 이 진짜 자전 주기일지
(그러면 티가든 별이 극단적인 느린 자전 outlier 가 됩니다) 검토했지만,
보수적 해석은 172 d 가 활동 관련 신호이고 96 d 가 자전 주기라고
결론지었습니다. cfg 는 그 결론을 따릅니다. Dreizler 2024 는 추가로 RV
와 활동 지표 양쪽에서 ~2500 d 이상에 걸친 매우 장주기 변동을 보고하며
이를 장기 활동 사이클일 수 있다고 제안하는데 — 바너드 별의 십 년 단위
사이클과 유사하지만 여기서는 확정 주기로 분해되지는 않았습니다.

Asteroseismic 제약은 불가능합니다 — 티가든 별은 너무 차갑고 너무 작아
검출 가능한 p-mode 진동이 없습니다. 자전축 경사는 제약되지 않습니다.
시각 렌더링에서 NearStars 는 일반적인 축 방향을 채택하는데, 자전 속도가
거의 0 이라 spin 관련 foreshortening 이 시각적으로 무시할 만하기
때문입니다. 눈에 띄는 운동학적 우연이 하나 있습니다. 별의 황위가 겨우
0.30° 라, 티가든 별에서 보면 태양계 행성들이 태양면을 통과합니다 —
지구는 2044 년에 티가든의 통과 띠에 들어옵니다 (Zechmeister 2019).
이는 cfg-결정적 사실이라기보다 시점 호기심이지만, 이 시스템이 태양
황도면에 얼마나 거의 모로 누워 있는지를 강조합니다.

## Canonical alternatives

두 파라미터가 Phase 2 문헌에 걸쳐 documented divergence 를 안고
있습니다. 두 경우 모두 cfg 는 Phase 2 recommended 값을 채택하지만,
분석 간 편차가 명시적 문서화를 정당화할 만큼 큽니다.

| Field | cfg value (recommended) | Canonical alternatives | Why cfg picks this value |
|---|---|---|---|
| `radius_rsun` / `mass_msun` | R = 0.107 ± 0.004 R☉, M = 0.089 ± 0.009 M☉ (Schweitzer 2019, SED + Stefan-Boltzmann + 선형 M-R) | R = 0.120 ± 0.012 R☉, M = 0.097 ± 0.010 M☉ (Dreizler 2024, "This work" — 갱신된 SteParSyn Teff 를 먹인 진화모델 M-L 재유도) | 두 반지름이 ~3σ 만큼 다릅니다 (0.107 대 0.120 R☉) — 산포가 아니라 실제 방법론적 불일치입니다. **간섭계 반지름은 불가능** 한데 (θ_LD ~0.032 mas, 간섭계 바닥보다 한참 아래), 그래서 어느 값도 직접 분해된 지름과 대조할 수 없습니다. SED 피팅이 유일한 길입니다. cfg 는 Schweitzer 2019 SED 반지름을 유지하는데, Phase 2 recommended 값이자 카탈로그 전체 (바너드, GJ 표적들) 에 쓰인 균질한 CARMENES SED/Stefan-Boltzmann 방법이라 cross-host 일관성을 보존하기 때문입니다. 갱신된 Marfil-2021 식 SteParSyn Teff (3034 K) 와 진화모델 질량-광도 관계에서 유도된 Dreizler 2024 값은 더 최근의 재유도이며 대안으로 보존됩니다. 이 선택은 행성에서 본 디스크의 렌더 각크기에는 영향을 주지만 표면 색조에는 인지 불가능한 수준입니다. |
| `metallicity_fe_h_dex` | −0.19 ± 0.16 (Schweitzer 2019, CARMENES 고분해능 분광) | −0.55 ± 0.17 (Rojas-Ayala 2012, K-band) | 두 측정이 ~0.36 dex 만큼 다릅니다 — Zechmeister 2019 자신이 이를 "아주 차가운 끝에서의 항성 파라미터 결정 불일치" 로 명시합니다. M7 V 에서 금속도는 악명 높게 어렵습니다. 광학 연속체가 분자 밴드에 완전히 가려져, K-band 보정 (Rojas-Ayala 2012) 과 고분해능 PHOENIX 피팅 (Schweitzer 2019) 조차 크게 어긋납니다. cfg 는 Schweitzer 2019 값을 Phase 2 recommended 값이자 recommended Teff/L/R/M (모두 Schweitzer, 자기일관 파라미터 집합) 과 일관된 값으로서 채택합니다. 금속도는 렌더 SED 색에 약하게만 영향을 주므로 이 divergence 는 시각적으로 결정적이라기보다 문서적입니다. (참고. Zechmeister 2019 자신의 나이 추정은 PARSEC 입력으로 Rojas-Ayala −0.55 를 썼으므로, recommended 나이는 대안 금속도와 약하게 얽혀 있습니다.) |

Dreizler 2024 (질량/반지름) 와 Rojas-Ayala 2012 (금속도) 는 각자의
측정 배열 안에서 `recommended:false` 대안으로 Phase 2 DB 에 남아 audit
trail 을 보존합니다. recommended 픽은 전반에 걸쳐 Schweitzer 2019
입니다.

## Visual styling

NearStars 렌더러에서 티가든 별은 카탈로그에서 가장 붉고 가장 어두운
M7 V 초저온 왜성으로 — 자기 분광형에서 가장 밝지만 밝기 면에서는
시각적으로 미미하게 — 표현됩니다. 표면 색조는 `#c23a1c` 으로 인코딩
되며, tie-break 선택입니다. 2904 K 흑체 연속체는 TiO/VO/H₂O 분자 밴드가
파랑과 초록을 거의 완전히 억제한 뒤 깊고 진한 주황-빨강으로 렌더링되며 —
M4 V 바너드 별 (`#cf5a30`, Teff 가 ~290 K 더 뜨거움) 과 M5.5 Proxima
(`#c54c2a`) 보다 붉고 진합니다. 가까운 천체의 장면 조명 색온도는
2904 K SED 가 직접 구동하며, 가까운 지구질량 행성들을 깊은 붉은빛의
적외선-우세 빛으로 적십니다.

디스크는 희미하고 느리게 떠도는 흑점 피처만 있는 거의 균일한 모습으로
렌더링됩니다 — 바닥 수준 색채권 활동 (Hα 가 West 2008 비활동 임계값
아래) 과 매우 느린 96 일 자전의 시각적 표현입니다. flare 레이어는
있지만 드문 사건의 박자 찍기입니다. Fuhrmeister 2025 의 TESS flare 둘
(각각 ~10³¹–10³² erg, 가장 큰 태양 flare 에 필적) 은 그밖에는 잔잔한
디스크 위에 가끔 찬란하게 일시적으로 밝아지는 모습으로, 거의 연속이
아니라 몰려서 렌더링됩니다. 가능한 ~2500 d 활동 사이클은, 실재한다면,
이미 미묘한 흑점 패턴을 게임 내 환산 수년에 걸쳐 느리게 변조합니다.

지구에서 티가든 별은 V = 15.08 천체입니다 — 3.831 pc 근접에도 맨눈
가시성에 한참 못 미치는데, 0.00073 L☉ 의 작은 광도 때문입니다 (근적외선
J = 8.39 에서는 훨씬 밝습니다). 실제 하늘에서의 signature 는 밝기가
아니라 거의 0 에 가까운 황위 (0.30°) 입니다. 별이 태양계 평면에 거의
정확히 자리해 그 시점에서 보면 태양의 행성들이 통과합니다. 가까운
지구질량 행성에서 봐도, 붉은 디스크는 적당한 각지름을 차지하며 풍경을
깊은 붉은빛의 적외선-우세 빛으로 적시는데, 수년간 잔잔하다가 가끔
찬란한 flare 로 밝혀집니다.

## Bibliography

### Read (drove Decisions above)

- **Schweitzer A. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Different roads to radii and masses of the target
  stars*, A&A 625, A68 (`2019A&A...625A..68S`,
  doi:10.1051/0004-6361/201834965, arXiv:1904.03231). CARMENES
  기본 파라미터 편람. Phase 2 recommended Teff (2904 ± 51 K, PHOENIX
  피팅), 광도 (0.00073 ± 0.00001 L☉, bolometric flux), 반지름
  (0.107 ± 0.004 R☉, L 과 Teff 로부터 Stefan-Boltzmann — SED 피팅,
  간섭계 불가능), 질량 (0.089 ± 0.009 M☉, 선형 M-R 관계), 금속도
  (−0.19 ± 0.16) 의 출처. 이 논문에서 티가든 별은 CARMENES 표본에서
  분광형이 가장 늦은 (M7 V) 천체로 명시적으로 강조됩니다.
- **Zechmeister M. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Two temperate Earth-mass planet candidates around
  Teegarden's Star*, A&A 627, A49 (`2019A&A...627A..49Z`,
  doi:10.1051/0004-6361/201935460, arXiv:1906.07196). 행성 b 와 c
  (각각 ~1.1 M⊕, P = 4.91 d 와 11.4 d) 의 발견 논문. Phase 2
  recommended 나이 (7 ± 3 Gyr, PARSEC Bayesian / 두꺼운 원반 운동학)
  와 분광형 (M7.0 V, Alonso-Floriano 2015 경유) 의 출처. 또한 항성
  맥락. 거리 3.831 pc, V = 15.08, J = 8.39, Hα 활동도 바닥, 황위
  0.30°. 행성은 여기서 범위 밖이라 행성 follow-up 으로 표시.
- **Dreizler S. et al. 2024** — *The CARMENES search for exoplanets
  around M dwarfs. The enigmatic planetary system of Teegarden's
  Star*, A&A 684, A117 (`2024A&A...684A.117D`,
  doi:10.1051/0004-6361/202348033, arXiv:2402.00923). Phase 2
  recommended 자전 주기 (P_rot = 96.2 d, Lafarga 2021 분광 활동
  지표에서) 와 대안 질량/반지름 (0.097 ± 0.010 M☉, 0.120 ± 0.012 R☉,
  진화모델 재유도 — documented 반지름/질량 divergence) 의 출처. 행성
  d (0.82 M⊕, P = 26.13 d) 의 발견 논문. 172 d / 96 d 자전-대-활동
  논의와 ~2500 d 가능 활동 사이클도.
- **Fuhrmeister B. et al. 2025** — *Coronal and chromospheric activity
  of Teegarden's star* (arXiv:2504.02338). Phase 2 recommended 코로나
  활동 log(Lx/Lbol) = −4.9 (정적 Chandra 검출. XMM-Newton 정적 범위
  −5.0 ~ −4.81) 의 출처로, Zechmeister 2019 X-선 상한을 대체. 또한
  큰 TESS flare 둘 (~10³¹–10³² erg), Neupert 효과 X-선 flare, 분출
  프로미넌스/CME 단서, 색채권 그림 (정적 시 Hα 채워짐, He I 적외선
  삼중선 부재) 의 출처. 정적-에-드문-flare 시나리오와 log R'HK
  측정불가 open item 의 근거.

### Read (context / methodology, not decision-driving)

- **Marfil E. et al. 2021** — *The CARMENES search for exoplanets
  around M dwarfs. Stellar atmospheric parameters of target stars with
  SteParSyn*, A&A 656, A162 (`2021A&A...656A.162M`,
  doi:10.1051/0004-6361/202141980, arXiv:2110.07329). SteParSyn
  Teff = 3034 ± 45 K, [Fe/H] = −0.11 ± 0.28. Dreizler 2024 가 대안
  파라미터 집합을 얻으려고 재실행한 line list 와 모델 그리드. 반지름/
  질량 divergence 의 방법론 맥락.
- **Cifuentes C. et al. 2020** — *CARMENES input catalogue of M dwarfs.
  Photometric and astrometric properties* (CARMENES 초저온 별 입력
  카탈로그). 측광 데이터와 광도 cross-check. 맥락 정보뿐.

### Read (instrument-only / methodological references)

- **Rojas-Ayala B. et al. 2012** — *Metallicity and Temperature
  Indicators in M Dwarf K-band Spectra*, ApJ 748, 93. K-band
  금속도 [Fe/H] = −0.55 ± 0.17 (documented 금속도 대안) 와
  Teff = 2637 K. Canonical-alternatives 금속도 행의 출처.
- **Lafarga M. et al. 2021** — CARMENES 활동 지표 시계열 분석으로
  P_rot = 96.2 d 자전 주기를 줌 (Dreizler 2024 Table 2 경유 인용).
  자전 Decisions 행은 이 작업에 정박.

### Not read — superseded or low-priority

대체된 Zechmeister 2019 X-선 상한 (log(Lx/Lbol) < −4.23, Fuhrmeister
2025 검출로 대체), recommended Lafarga 값을 넘어선 독립 자전 주기 확인
(Terrien 2022 ~100 d, Kemmer 2023 98 d — robustness 용 인용, 결정
구동 아님), 전용 티가든 별 엔트리가 없는 일반 초저온 왜성 활동 서베이,
그리고 Zechmeister 2019 과 Dreizler 2024 의 행성 발견 / 동역학 구조
부분은 항성 합성에 cfg-결정적 내용을 더하지 않습니다. 행성 논문은
행성 Phase 3 follow-up 워크스페이스로 미룹니다. 전체 필터링된 bib 는
`docs/phase3/_bib/teegardens-star.yaml` 에 보존됩니다.

## Open items for follow-up

- **지구질량 행성 Phase 3 follow-up 워크스페이스.** 시스템은 온대
  지구질량 행성 셋을 거느립니다 — b 와 c (~1.1 M⊕, P = 4.91 d 와
  11.4 d. Zechmeister 2019) 와 d (0.82 M⊕, P = 26.13 d. Dreizler
  2024). 이들은 항성 합성의 범위 밖입니다. 후보들의 Phase 2 측정이
  큐레이션되면 전용 follow-up 이 행성 Phase 3 합성을 만들어야 합니다.
- **M7 V 에서 log R'HK 는 지상에서 측정 불가능.** Ca II H&K 지수를
  정의할 식별 가능한 광구 연속체가 없어, cfg 는 더 뜨거운 호스트에
  쓰는 색채권 지수 대신 log(Lx/Lbol) = −4.9 (Fuhrmeister 2025) 를
  활동도 정박값으로 씁니다. 미래의 우주 UV 색채권 보정이 비교 가능한
  지수를 줄 수 있지만, 지상 기반 log R'HK 는 결코 존재하지 않을
  것입니다.
- **반지름/질량 divergence 해소.** Schweitzer 2019 SED 반지름
  (0.107 R☉) 과 Dreizler 2024 진화모델 반지름 (0.120 R☉) 이 ~3σ
  만큼 다르며, 간섭계는 결코 판정할 수 없습니다 (θ_LD ~0.032 mas).
  균질한 Teff 척도를 쓴 미래 SED 피팅 재분석, 또는 JWST/지상-NIR
  분광측광 재분석이 차가운 끝 반지름 척도를 좁히고 주계열 맨 밑바닥
  에서 어떤 질량-반지름 관계가 적절한지 확인할 수 있습니다.
- **활동 사이클 확인.** Dreizler 2024 는 RV 와 활동 지표에서 활동
  사이클일 수 있는 ~2500 d (~7 yr) 장주기 변동을 보고하지만 확정
  주기로는 분해되지 않았습니다. 지속적 모니터링이 티가든 별에
  바너드 같은 십 년 단위 사이클이 있는지 확인하고, cfg
  `activity_cycle_years` 렌더링을 날카롭게 할 수 있습니다.
- **flare 율 특성화.** Fuhrmeister 2025 는 TESS 사건 둘에서 ~2.6 ±
  1.8 flare / 100 d 를 추정하지만, 몰림이 활동/잔잔 에피소드를
  시사합니다. 더 긴 flare 센서스가 있으면 미래 cfg 가 그밖에는
  정적인 렌더링에 정량적 `flare_rate_per_day` 와
  `flare_energy_log_erg_max` 를 붙일 수 있습니다.
- **자전축 경사.** 제약되지 않음. 자전 속도가 거의 0 이라 spin 관련
  시각 효과가 무시할 만하므로 우선순위는 낮습니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 테이블의 스키마 출처
- [barnards-star](barnards-star.md) — 비교 M 왜성 (M4.0 Ve, ~8.5 Gyr). 다음으로 따뜻한 늙고 조용한 왜성 — 바너드의 간섭계 반지름·log R'HK 와 티가든의 SED 반지름·X-선 활동도 정박값을 대비
- [proxima-cen](proxima-cen.md) — 비교 초저온 계열 M 왜성 (M5.5 Ve, ~4.85 Gyr). 바너드와 티가든 사이 중간 온도
