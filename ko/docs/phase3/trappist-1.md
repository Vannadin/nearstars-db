<!-- TRAPPIST-1 중심별 Phase 3 합성: M8V 초저온 왜성 — 차가운 H2-서모스탯 플레어, 저대비 반점, 빠른 자전 -->
# TRAPPIST-1 — Phase 3 Synthesis (host star)

TRAPPIST-1 은 NearStars 로스터의 초저온 앵커입니다. 12.467 pc 거리의
M8.0 V 왜성으로, 질량 0.0898 M☉ 로 수소 연소 한계 바로 위에 아슬아슬
하게 걸쳐 있으며, 반지름은 0.1192 R☉ — 목성만 한 크기의 별이 0.07 AU
안쪽에 통과하는 암석 행성 일곱 개를 거느립니다. 태양은 이 별보다 대략
2000 배 밝습니다. L = 5.22×10⁻⁴ L☉, Teff = 2566 K 에서 광구는 촛불
불꽃 바깥 껍질 온도에 놓이는데, 분자 화학 (TiO, VO, H₂O — 그리고
결정적으로 H₂) 이 스펙트럼은 물론 밝혀진 대로 플레어까지 좌우할 만큼
차갑습니다.

이 별의 물리 파라미터는 어떤 M 왜성보다도 잘 측정된 축에 듭니다. 행성
일곱 개가 통과하기 때문입니다. [Agol et al. 2021](https://arxiv.org/abs/2010.01074)
(통과 시각 측정 + 광역학) 이 질량, 반지름, Teff 를 고정하고,
[Van Grootel et al. 2018](https://arxiv.org/abs/1712.01911) 이
볼로메트릭 광도를 앵커링하며, [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018)
이 7.6 ± 2.2 Gyr 의 concordance 나이를 줍니다 — 운동학과 활동도가
일치하는 *늙은* 별이면서도 여전히 자기적으로 활발합니다. 평균 밀도는
~51 ρ☉ 로, NearStars 모든 중심별 중 가장 높습니다.

최근 두 결과가 이 별의 기본 아트 디렉션을 뒤집으며, 둘 다 cfg 에
반영됩니다. **첫째, 이 별의 플레어는 차갑습니다.**
[Shapiro et al. 2026](https://arxiv.org/abs/2601.00386) 은 밀도 높고
차가운 광구에서 분자 수소 해리가 서모스탯 역할을 하여 백색광 플레어를
~3500–4000 K 에서 상한을 걸어 버림을 보였습니다 — 모든 범용 렌더러가
가정하는 9000–10000 K 태양 플레어 흑체보다 거의 세 배 차갑습니다.
TRAPPIST-1 의 플레어는 청백색 섬광이 아니라 따뜻한 오렌지빛 밝아짐입
니다. **둘째, 이 별의 반점은 저대비입니다.**
[Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793) 는 2350–2550 K
에서 사라지는 자기 피처를 측정했는데 — 2566 K 광구보다 겨우 수백 켈빈
낮을 뿐이라 — 표면은 검게 반점 박힌 디스크가 아니라 은은한 얼룩무늬
입니다.

**NearStars 시나리오 선택. 깊은 오렌지빛에 은은하게 얼룩진 초저온 왜성
(`#ffcc70` 광구 색조) 으로, 따뜻한 오렌지 플레어가 잦게 일어나는 모습
으로 렌더링합니다 — 25 일마다 3500–4000 K 플레어 색의 슈퍼플레어 케이던스,
저대비 반점 얼룩, 그리고 얼룩무늬를 디스크 위로 눈에 띄게 실어 나르는
빠른 3.295 일 자전.**

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M8.0 V (±0.5) | high | Gillon et al. 2016 분류, [Van Grootel 2018](https://arxiv.org/abs/1712.01911) §1 에서 재진술 |
| `mass_msun` | 0.0898 ± 0.0023 | high | [Agol et al. 2021](https://arxiv.org/abs/2010.01074) — 광역학 fit. Phase 2 recommended 행 |
| `radius_rsun` | 0.1192 ± 0.0013 | high | [Agol et al. 2021](https://arxiv.org/abs/2010.01074) — 통과로 유도한 항성 밀도 + 시차 |
| `teff_k` | 2566 ± 26 | high | [Agol et al. 2021](https://arxiv.org/abs/2010.01074). [Radica 2024](https://arxiv.org/abs/2409.19333) §3 에서 문헌 prior 로 같은 값 사용 |
| `luminosity_lsun` | 5.22×10⁻⁴ ± 0.19×10⁻⁴ | high | [Van Grootel 2018](https://arxiv.org/abs/1712.01911) — 볼로메트릭 플럭스 적분 |
| `metallicity_fe_h_dex` | +0.04 ± 0.08 | medium | Gillon et al. 2016 저분해 분광. [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) 기준 CMD 위치가 살짝 metal-rich |
| `age_gyr` | 7.6 ± 2.2 | medium | [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) — 운동학 + 활동도 concordance |
| `rotation_period_days` | 3.295 ± 0.003 | high | [Vida et al. 2017](https://arxiv.org/abs/1703.10130) K2 광도. [Berardo 2025](https://arxiv.org/abs/2506.12140) 가 3.27 ± 0.04 d 로 독립 재확인 |
| `activity_log_lhalpha_lbol` | −4.85 to −4.60 | medium | [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) Table 1 — Hα, M 왜성 활동 프록시 (M8 에는 Ca II R'HK 없음) |
| `x_ray_log_lx_lbol` | −3.52 ± 0.17 | medium | [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018) Table 1, [Wheatley 2017](https://arxiv.org/abs/1605.01564) XMM 검출 기반 (Lx/Lbol 2–4×10⁻⁴) |
| `magnetic_field_kg` | 0.6 (+0.2/−0.4) | medium | Reiners & Basri 2010, [Van Grootel 2018](https://arxiv.org/abs/1712.01911) §4.2 에서 재진술 |
| `flare_ffd_cumulative_slope_beta` | 0.753 (+0.068/−0.050) | medium | [Vasilyev et al. 2026](https://arxiv.org/abs/2605.05468) — 10²⁹–10³³ erg 전 구간 단일 멱법칙. Vida β≈0.59 를 대체 (Atmosphere 참고) |
| `flare_rate_e30_per_year` | ~1000 | medium | [Shapiro et al. 2026](https://arxiv.org/abs/2601.00386) §I. Vasilyev 2026 정규화 (1.01×10³¹ erg 이상 0.240/day) 와 일관 |
| `superflare_e32_interval_days` | 25 | medium | [Vasilyev et al. 2026](https://arxiv.org/abs/2605.05468) — 2026 년 이전 추정보다 한 자릿수 더 잦음 |
| `flare_color_temp_k` | 3500–4000 | medium | [Shapiro et al. 2026](https://arxiv.org/abs/2601.00386) — H₂ 해리 서모스탯이 백색광 플레어에 상한. [Howard 2025](https://arxiv.org/abs/2512.04265) RADYN fit (2115–4010 K) 이 뒷받침. 플레어는 청백색이 아닌 따뜻한 오렌지로 렌더 |
| `spot_temp_k` | 2350–2550 | medium | [Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793) — 사라진 피처 Planck fit. "광구보다 차갑지만 기껏해야 수백 켈빈 차이" |
| `spot_feature_area_disk_pct` | 0.06–1.5 (per feature) | medium | [Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793) §3.4 — 검은 반점부터 반영 유사까지 범위. 오염 retrieval 은 반점 지배적 ([Radica 2024](https://arxiv.org/abs/2409.19333)) |
| `stellar_color_temp_k` | 2566 | high | = Teff. 광구 색 파이프라인 입력값 |
| `visual_surface_tint_hex_primary` | `#ffcc70` | medium | `stellar_photospheric_color.py` 를 통한 Pickles real-SED M 사다리. 2566 K 는 가장 차가운 앵커에서 clamp — 벽돌빛 붉은색이 아닌 옅은 따뜻한 오렌지 (Visual styling 참고) |
| `figure_j2` | 2.0×10⁻⁶ | medium | 빠른 3.295-d 자전에서 나온 q = 2.33×10⁻⁵ 에 Radau–Darwin 폴리트로프 분기 (NMoI 0.205, J₂/q = 0.084). 상시-emit 항성 J₂ 정책에 따름 ([body-figure-methodology](../reference/body-figure-methodology.md)) |

## Surface synthesis

광구는 2566 K 분자 대기입니다 — TiO/VO 밴드가 광학 플럭스를, H₂O 가
근적외선을 게이트하는데, 광구 색 파이프라인이 흑체 대신 실제 Pickles
SED 를 쓰는 이유가 여기 있습니다 (2566 K 흑체는 `#ffa94f` 로 렌더되어
밴드 구조를 반영한 실제값보다 눈에 띄게 붉습니다). 이 별은 또한 측정
가능한 수준으로 *팽창*해 있습니다. [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018)
은 반지름이 태양 금속도 진화 모델보다 8–14% 크다고 지적하는데, 활동적
M 왜성에서 자기장이 대류를 억제하는 전형적 신호입니다.

**반점은 존재하지만 대비가 은은합니다.** Kepler/K2 는 차갑고 안정한
반점을 확인했으며 (Luger 2017; Vida 2017), 행성들의 JWST 투과 스펙트럼은
반점 지배적 비균질 광구 때문에 100–500 ppm 수준으로 오염됩니다
([Radica 2024](https://arxiv.org/abs/2409.19333)). 가장 좋은 직접 온도
측정은 [Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793) 에서
나오는데, 이들은 플레어 동안 개별 자기 피처가 사라지는 것을 관측했습니다.
피처는 2350–2550 K 로 fit 되어 — 기껏해야 수백 켈빈의 대비이며, 피처당
투영 면적은 가시 디스크의 0.06% (완전히 검을 경우) 부터 1.5% (반영 유사
일 경우) 입니다. 렌더링 귀결은 *얼룩진* 디스크입니다. 3.295 일 자전과
함께 떠도는, 살짝 더 어둡고 살짝 더 붉은 패치이지, 고전적 반점 항성
텍스처의 딱딱한 검은 모반이 결코 아닙니다.

**반점–플레어 지오메트리 상관 없음.** Vida et al. 2017 은 모든 자전
위상에서 플레어를 발견했고, 광도 곡선 최소점을 약하게만 선호했습니다 —
따라서 렌더러의 플레어 배치는 반점 패턴을 따라갈 필요가 없습니다.

## Atmosphere synthesis

색채권과 코로나는 활동적이지만 후기 M 플레어성 기준으로는 온건합니다 —
[Van Grootel 2018](https://arxiv.org/abs/1712.01911) 은 이를 "저활동
M8" 로 부르고, [Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018)
은 인근 M7–M9 왜성 절반 이상보다 덜 활동적이라 자리매김하면서도 7.6 Gyr
에도 "여전히 활동적인 별로 남아 있다" 고 강조합니다. Hα 방출은
log L_Hα/L_bol = −4.85 to −4.60 에 놓이며, XMM X 선 검출
([Wheatley 2017](https://arxiv.org/abs/1605.01564)) 은 부드러운 2온도
코로나 (kT = 0.15, 0.83 keV) 와 함께 Lx/Lbol = 2–4×10⁻⁴ (log −3.52 ±
0.17) 를 줍니다 — 2000 배 어두운 별인데도 비율로는 *태양 플레어 수준*
의 X 선 가열이라, 별이 어둠에도 행성들의 방사선 환경이 가혹한 이유입니다.

**플레어 이야기가 이 합성의 하중을 지탱합니다.** 세 갈래가 다음처럼
화해합니다.

- **빈도.** K2 는 74 일에 42 개 플레어를 주었습니다 (중앙 대기 28.1 h,
  [Vida 2017](https://arxiv.org/abs/1703.10130)). 2026 년 JWST+K2 통합
  플레어 빈도 분포 ([Vasilyev 2026](https://arxiv.org/abs/2605.05468))
  는 10²⁹–10³³ erg 전 구간에 걸친 단일 멱법칙 (누적 기울기 β = 0.753)
  입니다 — ~10³⁰-erg 플레어가 연 ~1000 회, >10³² erg 슈퍼플레어가
  ~25 일마다 — 2026 년 이전 추정보다 열 배 더 잦습니다. cfg 는 2026 년
  법칙을 채택하며, Vida 의 더 완만한 β ≈ 0.59 와 Paudel 의 0.6 은 에너지
  구간이 제한된 fit 으로 이제 여기에 포섭됩니다.
- **온도 (색).** H₂ 서모스탯
  ([Shapiro 2026](https://arxiv.org/abs/2601.00386)). 차갑고 밀도 높은
  광구를 가열하면 H₂ 가 해리되어 에너지를 흡수하고 플레어 영역을 4000 K
  근처에서 상한합니다. 백색광 플레어는 3500–4000 K, 충격 단계에서 잠깐
  ~5000 K 를 찍고, 수십 분 동안 3000–3500 K 로 가라앉습니다.
  [Howard 2025](https://arxiv.org/abs/2512.04265) 는 JWST 플레어를
  RADYN 모델로 2115–4010 K 유효 온도 (filling factor 0.03–0.51%) 에서
  독립적으로 fit 했습니다. 고전적 9000–10000 K 플레어 흑체는 ~4000 K
  항성 Teff 아래에서는 작동하지 않는 *태양* 패러다임입니다.
- **UV 예외.** 원자외선에서
  [Berardo 2025](https://arxiv.org/abs/2506.12140) 는 디스크의 극히
  작은 ~0.011% 에서 ~11000 K 색온도의 시간 미만 ~10²⁹-erg 마이크로
  플레어를 발견합니다 — 광학의 ~3–4% 대비 Lyα 에서 400% 진폭입니다.
  뜨거운 플레어 *코어* 는 존재하지만 FUV 로 밝은 점일 뿐이며, 가시 밴드
  이벤트는 따뜻한 3500–4000 K 밝아짐으로 남습니다.

**XUV 예산 폭 (기록, 미해결).**
[Wheatley 2017](https://arxiv.org/abs/1605.01564) 은
L_XUV/L_bol = 6–9×10⁻⁴ (~1.2–1.8×10²⁷ erg/s) 로 범위를 잡습니다.
[Berardo 2025](https://arxiv.org/abs/2506.12140) 는 Lyα 로부터
1.83×10²⁸ erg/s 를 재구성하는데 — 이들이 인용하는 2017 년대 값
(6.28×10²⁶) 의 30 배이자, Howard 가 채택한 정상상태 3.75×10²⁷
(Wilson 2021) 의 ~5 배입니다. Decisions 표는 견고한 X 선 행만 담으며,
XUV 폭은 방사선 환경 레이어의 미해결 항목입니다.

## Rotation & spin synthesis

3.295 ± 0.003 d K2 주기 ([Vida 2017](https://arxiv.org/abs/1703.10130))
는 확실하며 HST 광도에서 3.27 ± 0.04 d 로 독립 재확인됩니다
([Berardo 2025](https://arxiv.org/abs/2506.12140)). 더 오래된 지상 관측
1.40 d 값 (Gillon 2016, Wheatley 2017 에서 반복) 은 대체됐습니다. 다만
분광 쪽에는 솔직한 긴장이 남아 있습니다. v sin i = 6 ± 2 km/s
(Reiners & Basri 2010) 는 이 반지름에서 P_rot ≈ 0.99 d (0.74–1.48 d) 를
함의하므로 — v sin i 와 맞았던 건 3.295 d 가 아니라 그 1.40 d 값이었고 —
3.295 d 에서의 적도 속도는 ~1.8 km/s 에 불과합니다. Vida 등은 K2 푸리에
스펙트럼에 유의미한 ~1 d 피처가 전혀 없다고 지적하며, cfg 는 두 번
확인된 측광 주기를 채택하고 v sin i 불일치는 문헌의 몫으로 남겨 둡니다.

**Figure.** 작고 밀도 높은 별의 빠른 자전은
q = Ω²R³/GM = 2.33×10⁻⁵ 를 줍니다. 완전 대류 Radau–Darwin 분기
(폴리트로프 NMoI 0.205, J₂/q = 0.084) 는 **J₂ ≈ 2.0×10⁻⁶** 를 내놓는데 —
Proxima (83.5-d 자전) 의 ~500 배이며 40 Eri C 의 빠른 자전 1.6×10⁻⁶ 를
근소하게 앞질러 로스터 최대 M 왜성 J₂ 가 됩니다 (전체로는 Fomalhaut A 의
1.0×10⁻⁴ 가 여전히 지배적). 역학적으로는 21 항성 반지름에 있는 행성 b
에도 무시할 만하지만 (GR 세차가 지배), 2026-07-12 상시-emit 정책에 따라
항은 계산되어 Principia 가 실어 나릅니다. 시각적 편평도
f ≈ 1.5×10⁻⁵ — 렌더 불가능이며, 디스크는 둥글게 유지됩니다.

7.6 Gyr 에서 ~4 Gyr 포화 spin-down 무릎 (Fleming 2020,
[Howard 2025](https://arxiv.org/abs/2512.04265) 경유) 과 함께, 이 별은
포화를 벗어났으면서도 여전히 며칠 단위로 자전합니다 — 초저온 왜성은
극도로 느리게 제동되며, 이것이 늙은 별이 여전히 젊은 별의 플레어
스케줄을 내놓는 이유입니다.

## Visual styling

- **광구 색조 `#ffcc70`** — Pickles real-SED 사다리에서 나옵니다
  (`scripts/refs/stellar_photospheric_color.py`). 2566 K 는 가장 차가운
  Pickles M 앵커 아래에 있어 색도가 사다리 바닥에서 clamp 됩니다. 색
  방법론에 따르면 이는 옅은 따뜻한 오렌지입니다. "벽돌빛 붉은 M 왜성"
  통념은 색지수 아티팩트일 뿐 색도가 아닙니다. 더 붉은 아트 디렉션이
  원한다면 2566 K 흑체 hex `#ffa94f` 가 하한이며 — Pickles 값이 데이터
  기반의 선택입니다.
- **검은 반점이 아닌 저대비 얼룩.** 2566 K 대비 ~2350–2550 K 반점 얼룩.
  색조를 국소적으로 몇 퍼센트 어둡게 하고 살짝 붉게 당깁니다. 개별
  피처는 디스크의 1% 미만부터 ~1.5% 까지. 3.295-d 자전과 함께 떠돌게
  합니다.
- **플레어는 따뜻한 오렌지, 잦고, 소면적.** 플레어 색을 3500–4000 K 로
  렌더 (≈ K 왜성 광구 따뜻함 — 같은 사다리에서 `#ffcc95` 영역), filling
  factor 는 디스크의 1% 훨씬 아래, 진폭은 광학에서 수 퍼센트. ~25 게임일
  마다의 >10³²-erg 슈퍼플레어가 대표 이벤트이며, ~매일의 작은 플레어가
  별을 눈에 띄게 살아 있게 유지합니다. 이 별에는 청백색 태양식 플레어를
  결코 렌더하지 마십시오.
- **하늘에서의 존재감.** 행성 e (0.029 AU) 에서 별은 ~2.4° 를 채웁니다 —
  태양 네댓 개 폭의 — 얼룩과 플레어가 직접 보이는 풍경이 되는 거대하고
  어두운 호박색 디스크이며, 위의 저대비 반점과 따뜻한 플레어 행이
  잡학이 아니라 게임플레이 대면 요소인 이유입니다.
- **Firefly 노트.** 여기서 플레어 색은 재진입 플라스마가 아니라 *항성
  표면* 렌더링입니다 — Firefly 조성 색 정책 (모드 원본 팔레트) 은
  영향받지 않으며, 이 행은 별 자체의 emissive 레이어를 먹입니다.

## Bibliography

### Read (deep-read, drives Decisions rows)

- **[Agol et al. 2021](https://arxiv.org/abs/2010.01074)** —
  *Refining the transit timing and photometric analysis of
  TRAPPIST-1*. 질량/반지름/Teff 앵커 (Phase 2 recommended 행). 캐시
  노트: 로컬 텍스트는 abstract 전용이라, 수치 행은 Phase 2 큐레이션
  (논문 검증) 과 Radica 2024 §3 에서 재진술된 2566 K prior 에 근거합니다.
- **[Van Grootel et al. 2018](https://arxiv.org/abs/1712.01911)** —
  *Stellar parameters for TRAPPIST-1*. 볼로메트릭 광도
  5.22×10⁻⁴ L☉. 밀도 51.1 ρ☉. 600 G 자기장 재진술. "저활동 M8"
  특성화.
- **[Burgasser & Mamajek 2017](https://arxiv.org/abs/1706.02018)** —
  *On the Age of the TRAPPIST-1 System*. 7.6 ± 2.2 Gyr concordance
  나이. Table 1 활동도 개요 (Hα, X 선, v sin i). 8–14% 반지름 팽창.
  "늙었지만 활동적" 틀.
- **[Vida et al. 2017](https://arxiv.org/abs/1703.10130)** — K2 플레어
  서베이: 74 d 에 42 플레어, 3.295 d 자전, 에너지 범위
  1.26×10³⁰–1.24×10³³ erg, 반점 위상 상관 없음.
- **[Wheatley et al. 2017](https://arxiv.org/abs/1605.01564)** —
  XMM-Newton X 선 검출: Lx/Lbol 2–4×10⁻⁴, 2온도 코로나, XUV/bol
  6–9×10⁻⁴.
- **[Vasilyev et al. 2025](https://arxiv.org/abs/2508.04793)** —
  플레어가 자기 피처 스펙트럼을 드러냄: 2350–2550 K 에서 사라지는 피처,
  피처당 디스크의 0.06–1.5%. MURaM M4 반점 대비.
- **[Shapiro et al. 2026](https://arxiv.org/abs/2601.00386)** — H₂
  플레어 서모스탯: 백색광 플레어가 ~3500–4000 K 에서 상한, 10³⁰ erg
  이상 ~1000/yr. 메커니즘은 ~4000 K Teff 위에서 멈춤.
- **[Vasilyev et al. 2026](https://arxiv.org/abs/2605.05468)** —
  네 에너지 자릿수에 걸친 단일 멱법칙 FFD (β = 0.753). 25 d 마다
  슈퍼플레어. 3500 K 플레어 연속체 채택.
- **[Berardo et al. 2025](https://arxiv.org/abs/2506.12140)** — HST
  Lyα: 잦은 FUV 마이크로플레어 (11000 K, 디스크의 0.011%), 자전 확인,
  XUV 재구성 1.83×10²⁸ erg/s.
- **[Radica et al. 2024](https://arxiv.org/abs/2409.19333)** — JWST
  NIRISS 항성 오염: 반점 지배적 retrieval, 100–500 ppm 신호, 2566 ± 50 K
  광구 prior, 반점 격자 바닥 2300 K / faculae ≤ +1000 K.
- **[Howard et al. 2025](https://arxiv.org/abs/2512.04265)** — RADYN
  NIR 플레어 모델링: fiducial 플레어 Teff 2115–4010 K, filling factor
  0.03–0.51%. 플레어가 JWST 통과의 50–70% 를 오염.

### Context (cited through the read set; not deep-read here)

- **[Gillon et al. 2016](https://ui.adsabs.harvard.edu/abs/2016Natur.533..221G)** /
  **[Gillon et al. 2017](https://ui.adsabs.harvard.edu/abs/2017Natur.542..456G)** —
  발견 논문. 최초 항성 파라미터와 대체된 1.40 d 자전 alias. [Fe/H]
  출처.
- **[Luger et al. 2017](https://ui.adsabs.harvard.edu/abs/2017NatAs...1E.129L)** —
  K2 일곱 행성 논문. 반점 확인과 오염 문헌이 인용하는 3.3 d 주기.
- **Reiners & Basri 2010** — 600 G 자기장과
  v sin i = 6 ± 2 km/s, Van Grootel 2018 과 Wheatley 2017 이 인용.
- **Wilson et al. 2021** — Howard 2025 가 쓴 정상상태 XUV 3.75×10²⁷ erg/s
  (XUV 폭의 한 갈래).
- **Fleming et al. 2020** — 초저온 왜성 spin-down 의 ~4 Gyr 포화 무릎.

### Not read — superseded or out of scope

- Stassun 2019 / Ducrot 2020 / Grimm 2018 항성 행 — 더 이르거나 오차가
  더 넓은 파라미터 셋으로, Phase 2 에서 Agol 2021 로 대체.
- 시스템 bib 의 행성 중심 대기/탈출 논문 — 호스트 리포트가 아니라 행성
  일곱 개의 개별 합성이 소비.

## Open items for follow-up

- **Agol 2021 캐시가 abstract 전용.** recommended M/R/Teff 행은 Phase 2
  검증됐지만, [2010.01074](https://arxiv.org/abs/2010.01074) 의 전문
  재-fetch 가 있으면 이 리포트의 Step 10 추적이 큐레이션 레이어 +
  Radica 재진술 대신 논문 자체 표에 착지할 수 있습니다.
- **XUV 예산 폭 (×10).** Wheatley 밴드 ~1.2–1.8×10²⁷ 대 Berardo Lyα
  재구성 1.83×10²⁸ erg/s. Kerbalism 방사선 레이어가 TRAPPIST-1 용으로
  재앵커된다면 이 폭을 먼저 해소해야 합니다 (정의 차이 — X 선+EUV 밴드
  대 Lyα 스케일 총량 — 이 대부분을 설명할 듯).
- **항성풍 측정 없음.** 2026-06-11 항성풍 합성 순회는 질량 손실이나
  astrosphere 데이터가 없어 TRAPPIST-1 을 건너뛰었습니다 — 그래서 여기
  풍/astrosphere 섹션이 없습니다. MHD 풍-행성 커플링 논문이 시스템 bib
  에 있으나 (시뮬레이션 전용), 관측 제약이 나타나면 재방문합니다.
- **반점 덮힘 분율은 피처당, 전역 아님.** Vasilyev 2025 는 개별 사라진
  피처를 측정 (디스크의 0.06–1.5%). 전역 반점 분율은 retrieval 축퇴로
  남아 있습니다 (Radica 의 0–50% prior). 저대비 렌더링 규칙은 이에
  견고하며, 전역 분율 행은 현재 지지할 수 없습니다.
- **활동 사이클 미지.** TRAPPIST-1 에는 사이클 주기가 존재하지 않습니다
  (플레어 모니터링 기저선이 너무 짧음). α Cen A/B 와 달리
  `activity_cycle_years` 행은 emit 하지 않습니다.

## Related

- [trappist-1-b](trappist-1-b.md) … [trappist-1-h](trappist-1-h.md) —
  이 호스트 리포트가 앵커링하는 일곱 행성 합성
- [alpha-centauri-a](alpha-centauri-a.md) — 항성 합성 구조 템플릿
  (G2V 대응물)
- [stellar-photospheric-color-methodology](../reference/stellar-photospheric-color-methodology.md) —
  `#ffcc70` 유도 경로 (Pickles real-SED 사다리)
- [body-figure-methodology](../reference/body-figure-methodology.md) —
  항성 J₂ 상시-emit 정책 + 여기 사용된 폴리트로프 분기
- [methodology](../reference/methodology.md) — Decisions 스키마
