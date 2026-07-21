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
| [mass-radius-relation-methodology](mass-radius-relation-methodology.md) | 질량 ↔ 반경 ↔ 밀도 tie-break | Seager 2007; Zeng 2016; Fortney 2007; Chen & Kipping 2017 |
| [tidal-locking-timescale-methodology](tidal-locking-timescale-methodology.md) | 자전 상태 / 동기화 타임스케일 | Goldreich & Soter 1966; Hut 1981; Leconte 2015 |
| [tidal-heating-methodology](tidal-heating-methodology.md) | 조석가열 플럭스 (Io/Enceladus 캘리브레이션) | Peale, Cassen & Reynolds 1979; Segatz 1988; Henning 2009 |
| [body-figure-methodology](body-figure-methodology.md) | 자전 편평 J₂ + 조석 triaxial C₂₂ (Principia 중력모델) | Helled 2011 ([arXiv:1109.1627](https://arxiv.org/abs/1109.1627)); Murray & Dermott 1999; Radau–Darwin / Maclaurin; Io/Titan 앵커 |

## 궤도·에포크

| 방법론 | 근거화하는 값 | 핵심 참고문헌 |
|---|---|---|
| [emit-orbit-phase-match-methodology](emit-orbit-phase-match-methodology.md) | 직접검출 행성의 emit 궤도 위상(Ω/ω/M): 하늘 PA 정합 + 1950.0 에포크 되감기 | Beichman 2025 ([arXiv:2508.03814](https://arxiv.org/abs/2508.03814)); Pourbaix & Correia 2017; Murray & Dermott 1999 (교과서) |

## 대기·열

| 방법론 | 근거화하는 값 | 핵심 참고문헌 |
|---|---|---|
| [exoplanet-atmosphere-methodology](exoplanet-atmosphere-methodology.md) | 대기 보유 + 기압/조성 | Zahnle & Catling 2017 (cosmic shoreline); Owen 2019; Dong 2017/2018 |
| [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md) | 표면 온도 / 기후 상태 | Joshi 1997; Wordsworth 2015; Koll & Abbot 2016; Koll 2022 |
| [internal-heat-luminosity-methodology](internal-heat-luminosity-methodology.md) | 내부열 + 자발광 (T_int) | Burrows 1997; Baraffe 2003; Fortney 2007; Marley 2007 |

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

## 검증 (도출이 아니라 Phase-4 게이트)

- **궤도/안정성 시뮬레이션**: `phase3/stability-sim/`의 REBOUND N-body(WHFast / TRACE / IAS15) +
  MEGNO 카오스 지표 + Hill 안정성 + 공명 분석. Phase-4 궤도를 확정하기 전, 시스템 배치가 살아남는지
  (이심률 갇힘·이탈 없음) 확인합니다.
- [principia-cfg-reference](principia-cfg-reference.md) / [principia-geopotential-data](principia-geopotential-data.md): n-body 중력모델(J2/geopotential) cfg 규약.
- [gravity-significance-floor-methodology](gravity-significance-floor-methodology.md): Principia 포크의 far-field 중력 절단 floor `a_floor` + 스위칭-셸 비율을 문헌으로 근거화. Folkner 2014 / Park 2021(에페메리스 섭동체 선정), Chesley 2014(Yarkovsky 검출 한계), Jiang & Tremaine 2010(Jacobi 반경), Rein & Spiegel 2015(힘-오차 예산).
- [binary-epoch-pipeline](binary-epoch-pipeline.md): 다성계 Keplerian → ICRS 에포크 전파.

## 관련 문서

- [methodology](methodology.md): 이 레시피들이 먹여주는 상류 DB-빌드 워크플로우(Phase 1–3 데이터 파이프라인).
- [tools](tools.md): 도구/스크립트 인덱스.
