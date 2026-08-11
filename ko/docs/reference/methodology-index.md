<!-- NS의 논문-근거화 derived-value 방법론 문서 전체 인덱스 (Phase 3/4가 도출에 사용) -->
# 방법론 인덱스: 논문-근거화 도출값 레시피

NearStars는 많은 물리값을 **측정이 아니라 도출**합니다. 천체의 색, 자기장, 대기, 내부열 등이 그렇습니다.
이런 값마다 전용 **방법론 레퍼런스**가 있고, 각각 ADS로 검증한 레시피(관계식 + 적용영역 + 워크드 예시 +
인용 검증된 주석 참고문헌)입니다. `planetary-dynamo-scaling.md`를 gold standard 템플릿으로 삼았습니다.

이 문서는 그 레시피들의 단일 인덱스입니다. Phase 3가 이 방법론들로 cfg-ready 값을 도출하고, Phase 4가
오너 아트디렉션을 이 게이트에 대고 검증합니다. 모든 방법론 문서는 `ko/docs/reference/`에 한글 미러가 있습니다.

> 규율: 인용은 ad-hoc 웹검색이 아니라 NASA ADS(등록 API 토큰)로 해소하고, arXiv id가 있으면 그것을,
> 없으면 권위 있는 ADS bibcode를 씁니다. 교과서 관계식(Darwin–Radau, Planck 함수 등)은 "도출값은
> 논문 근거화" 원칙의 허용된 예외입니다.

## 자기장·구조·동역학

| 방법론 | 근거화하는 값 | 핵심 참고문헌 |
|---|---|---|
| [planetary-dynamo-scaling](planetary-dynamo-scaling.md) | 거대행성/갈색왜성 자기장 세기 (에너지플럭스) | Christensen 2009; Reiners & Christensen 2010 ([arXiv:1007.1514](https://arxiv.org/abs/1007.1514)); Yadav & Thorngren 2017 |
| [rocky-planet-dynamo-methodology](rocky-planet-dynamo-methodology.md) | 암석형(지구/슈퍼지구) 자기모멘트 + 표면장 | Rodríguez-Mozos & Moya 2022 ([arXiv:2203.01065](https://arxiv.org/abs/2203.01065)); Olson & Christensen 2006; Gaidos 2010; Driscoll & Olson 2011 |
| [planetary-magnetosphere-geometry-methodology](planetary-magnetosphere-geometry-methodology.md) | 자기장에서 자기권 standoff + 방사선대 크기/강도 도출 (→ Kerbalism). 정확한 K–P 상한 계산기 `scripts/refs/kp_limit.py` 포함 | Chapman & Ferraro 1931; Shue 1997/98; Kennel & Petschek 1966; Summers 2009/2014; Mauk & Fox 2010 (+Zenodo 포팅); Seltzer 1979/92; Schulz & Lanzerotti 1974; Thorne 2010 |
| [mass-radius-relation-methodology](mass-radius-relation-methodology.md) | 질량 ↔ 반경 ↔ 밀도 tie-break | Seager 2007; Zeng 2016; Fortney 2007; Chen & Kipping 2017 |
| [tidal-locking-timescale-methodology](tidal-locking-timescale-methodology.md) | 자전 상태 / 동기화 타임스케일 | Goldreich & Soter 1966; Hut 1981; Leconte 2015 |
| [tidal-heating-methodology](tidal-heating-methodology.md) | 조석가열 플럭스 (Io/Enceladus 캘리브레이션) | Peale, Cassen & Reynolds 1979; Segatz 1988; Henning 2009 |
| [body-figure-methodology](body-figure-methodology.md) | 자전 편평 J₂ + 조석 triaxial C₂₂ (Principia 중력모델) | Helled 2011 ([arXiv:1109.1627](https://arxiv.org/abs/1109.1627)); Murray & Dermott 1999; Radau–Darwin / Maclaurin; Io/Titan 앵커 |
| [cassini-state-obliquity-methodology](cassini-state-obliquity-methodology.md) | 조석으로 감쇠된 천체의 평형 자전축 기울기 (고정됐다고 기울기 0은 아님) | Peale 1969; Ward 1975; Ward & Hamilton 2004; Bills 2005; Baland 2011; Margot 2007 (수성 앵커) |

## 궤도·에포크

| 방법론 | 근거화하는 값 | 핵심 참고문헌 |
|---|---|---|
| [emit-orbit-phase-match-methodology](emit-orbit-phase-match-methodology.md) | 직접검출 행성의 emit 궤도 위상(Ω/ω/M): 하늘 PA 정합 + 1950.0 에포크 되감기 | Beichman 2025 ([arXiv:2508.03814](https://arxiv.org/abs/2508.03814)); Pourbaix & Correia 2017; Murray & Dermott 1999 (교과서) |

## 대기·열

| 방법론 | 근거화하는 값 | 핵심 참고문헌 |
|---|---|---|
| [exoplanet-atmosphere-methodology](exoplanet-atmosphere-methodology.md) | 대기 보유 + 기압/조성 | Zahnle & Catling 2017 (cosmic shoreline); Owen 2019; Dong 2017/2018 |
| [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md) | 표면 온도 / 기후 상태 | Joshi 1997; Wordsworth 2015; Koll & Abbot 2016; Koll 2022 |
| [moon-energy-budget-methodology](moon-energy-budget-methodology.md) | 위성 T_eq: 별빛 − 식 + 행성 열복사 + 행성 반사 + 조석, 행성주위 거주가능 경계 대조; 계산기 `scripts/refs/moon_energy_budget.py` | Heller & Barnes 2013 ([arXiv:1209.5323](https://arxiv.org/abs/1209.5323)); Dobos 2017 ([arXiv:1703.02447](https://arxiv.org/abs/1703.02447)); Barnes 2013 ([arXiv:1203.5104](https://arxiv.org/abs/1203.5104)); Tyler 2008; Beuthe 2016; Hay & Matsuyama 2017 |
| [greenhouse-warming-methodology](greenhouse-warming-methodology.md) | 임의 기체 조합의 온실 상승폭 T_surf − T_eq. 4개 층(해석 모형 / 불투명도 자료 / iso-Ts 등온선 / 빌려온 계산) + 모항성 보정; 계산기 `scripts/refs/greenhouse_dt.py` | Robinson & Catling 2012 ([arXiv:1209.1833](https://arxiv.org/abs/1209.1833)); Karman 2019 (HITRAN CIA); Byrne & Goldblatt 2014a/b; Feulner 2012 ([arXiv:1204.4449](https://arxiv.org/abs/1204.4449)); Kopparapu 2013 ([arXiv:1301.6674](https://arxiv.org/abs/1301.6674)); Charnay 2013 ([arXiv:1310.4286](https://arxiv.org/abs/1310.4286)); Ramirez 2014/2018; Goldblatt 2009; Arney 2016 |
| [internal-heat-luminosity-methodology](internal-heat-luminosity-methodology.md) | 내부열 + 자발광 (T_int) | Burrows 1997; Baraffe 2003; Fortney 2007; Marley 2007 |
| [surface-radiation-dose-methodology](surface-radiation-dose-methodology.md) | 항성 입자 이벤트가 대기 기둥을 뚫고 지표에 남기는 선량 (Kerbalism 위험 층). 갇힌 방사선대 선량과는 별개 | Atri 2020 ([arXiv:1910.09871](https://arxiv.org/abs/1910.09871)); Atri 2017 ([arXiv:1606.07027](https://arxiv.org/abs/1606.07027)); Grießmeier 2016 ([arXiv:1603.06500](https://arxiv.org/abs/1603.06500)); MSL RAD 캘리브레이션 |
| [ice-stability-methodology](ice-stability-methodology.md) | 해당 궤도에서 드러난 얼음이 살아남는지: 승화 수명 + 알베도 생존 문턱값; 계산기 [`docs/ice-stability.html`](../../../docs/ice-stability.html) | Fray & Schmitt 2009 ([`2009P&SS...57.2053F`](https://ui.adsabs.harvard.edu/abs/2009P%26SS...57.2053F)); Feistel & Wagner 2007; Schörghofer 2008/2016; Hayne & Aharonson 2015; Marti & Mauersberger 1993 |

## 표면·지질

| 방법론 | 근거 대상 | 핵심 레퍼런스 |
|---|---|---|
| [crater-degradation-methodology](crater-degradation-methodology.md) | 크레이터투성이 vs 크레이터 없음: 채널별 크레이터 소거 시간척도(확산 / 매몰 / 점성 이완 / 유수 / 통째 갱신) 대 충돌 누적 | Fassett & Thomson 2014; Hartmann 1984; Zahnle 2003; Passey & Shoemaker 1981; Bland 2012; McKinnon 2016; Forsberg-Taylor 2004; Neish & Lorenz 2012; Strom 1994 |

## 색 (공용 CIE 1931 → sRGB 엔진)

반사/발광색 레시피 넷은 하나의 색측정 엔진(CIE 1931 CMF → XYZ → IEC 61966-2-1 sRGB)을 공유하며,
그 엔진은 반사색 문서가 소유합니다.

| 방법론 | 근거화하는 값 | 핵심 참고문헌 |
|---|---|---|
| [stellar-photospheric-color-methodology](stellar-photospheric-color-methodology.md) | 항성 백열(광구)색 (Teff → sRGB) | Husser 2013 (PHOENIX); Castelli & Kurucz 2003; Allard BT-Settl 2011; Mann 2015; Pickles 1998 |
| [atmosphere-reflected-color-methodology](atmosphere-reflected-color-methodology.md) | 하늘/구름 반사색 | Sneep & Ubachs 2005 (Rayleigh); Gao 2021; Irwin 2024; CIE 1931 / IEC sRGB |
| [surface-color-albedo-methodology](surface-color-albedo-methodology.md) | 표면 광물색 + Bond albedo | Burns 1993; Hapke 1981/2012; Kokaly (USGS) 2017; Grundy |
| [debris-disk-color-methodology](debris-disk-color-methodology.md) | 잔해원반 먼지 산란색 (Mie) | Draine 2003; Bohren & Huffman 1983; Khare 1984 |
| [element-plasma-colors](element-plasma-colors.md) | 발광/플라스마색 (오로라·재진입·선) | NIST ASD; Pearse & Gaydon; Park 1990 |
| [hapke-shader-methodology](hapke-shader-methodology.md) | Sol `_Hapke` 셰이더 값(지형+스케일드) 바디 클래스별 처방 | Sol-Configs @ f9e6fdf (앵커); Hapke 1981/1986/2002; Sato 2014; Warell 2004; Verbiscer 2005; Belskaya & Shevchenko 2000 |

## 검증 (도출이 아니라 Phase-4 게이트)

- **궤도/안정성 시뮬레이션**: `phase3/stability-sim/`의 REBOUND N-body(WHFast / TRACE / IAS15) +
  MEGNO 카오스 지표 + Hill 안정성 + 공명 분석. Phase-4 궤도를 확정하기 전, 시스템 배치가 살아남는지
  (이심률 갇힘·이탈 없음) 확인합니다.
- [principia-cfg-reference](principia-cfg-reference.md) / [principia-geopotential-data](principia-geopotential-data.md): n-body 중력모델(J2/geopotential) cfg 규약.
- [gravity-significance-floor-methodology](gravity-significance-floor-methodology.md): Principia 포크의 far-field 중력 절단 floor `a_floor` + 스위칭-셸 비율을 문헌으로 근거화. Folkner 2014 / Park 2021(에페메리스 섭동체 선정), Chesley 2014(Yarkovsky 검출 한계), Jiang & Tremaine 2010(Jacobi 반경), Rein & Spiegel 2015(힘-오차 예산).
- [binary-epoch-pipeline](binary-epoch-pipeline.md): 다성계 Keplerian → ICRS 에포크 전파.
- [solar-system-radiation-belts](solar-system-radiation-belts.md): 자기장을 가진 태양계 7개 천체(지구/목성/토성/천왕성/해왕성/수성/가니메데)에 대해 스톡 Kerbalism cfg와 ADS 근거 물리를 대조 — 자기권 형상 레시피의 캘리브레이션 축입니다. 인게임 SDF 단면 렌더는 [위키](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)에 있습니다. Joy 2002; Cooper 1983; Ness 1986/1989; Winslow 2013; Kivelson 2002; 외 18편.

## 관련 문서

- [methodology](methodology.md): 이 레시피들이 먹여주는 상류 DB-빌드 워크플로우(Phase 1–3 데이터 파이프라인).
- [tools](tools.md): 도구/스크립트 인덱스.
