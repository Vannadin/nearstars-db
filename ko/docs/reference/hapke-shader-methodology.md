<!-- Sol의 Hapke 셰이더 값(_Hapke 지형/스케일드)을 앵커 보간 + 광도 문헌으로 처방하는 방법 -->
# Hapke 셰이더 값 근거화: Sol 앵커 패밀리 + 광도 regime

NearStars 바디마다 Sol(RSS-Reborn) 렌더링 스택이 요구하는 **`_Hapke` 셰이더 값
두 개** — 지상 룩을 정하는 **Parallax 지형** 머티리얼의 `_Hapke`와 궤도/맵 뷰의
원반 룩을 정하는 **`Custom/HapkeScaled`** 머티리얼의 `_Hapke` — 를 배정하는 방법
문서다. 이 노브들은 Hapke 반사 이론의 이름을 딴 엔진 룩 파라미터이므로, 레시피는
두 층으로 선다. Sol-Configs 자체에서 읽어 낸 **경험 앵커 표**(canonical cfg 소스)와,
그 앵커들이 왜 그렇게 뭉치는지·새 바디를 그 사이 어디에 둘지를 근거 짓는
**광도 문헌 층**이다.

**정직 유보.** 셰이더 자체는 컴파일된 에셋 번들로 배포되어, `_Hapke`가 정확히
어떤 항(역산란 게인인지 위상함수 지수인지)에 곱해지는지는 소스로 읽을 수 없다.
아래 내용은 (a) Sol이 바디마다 실제로 배정한 관측 가능한 값과, (b) 그 배정이
따라가는 실제 광도 물리에만 근거한다. `_Hapke`는 **실측 천체에 캘리브레이션된
룩 파라미터**로 취급하고, 측정된 Hapke 모델 계수로 취급하지 않는다.

## Canonical 소스 (비-ADS 예외, 핀 고정)

앵커 값의 출처는 **RSS-Reborn/Sol-Configs** 커밋
[`f9e6fdf`](https://github.com/RSS-Reborn/Sol-Configs/tree/f9e6fdf4e26c4a5ba1364ba93babfa2ada3e5a5c)
(`*-ParallaxTerrain.cfg`, 실스케일 44바디; `Quarter_`/`Stock_` 변형은 자체 값이
없는 리스케일 셸)이다. ADS 규율의 fallback이 말하는 "권위 있는 큐레이션
데이터베이스"에 해당하며, 웹 요약이 아니라 핀된 커밋의 파일 직독으로 검증했다.

## 앵커 표 (Sol-Configs, 패밀리로 압축)

| 패밀리 | 바디(예) | 지형 `_Hapke` | 스케일드 `_Hapke` |
|---|---|---|---|
| 성숙 달형 레골리스 | Luna, Mimas, (Earth 육지) | **1.0** | **2.2** |
| 어두운 암석 레골리스 | Mercury, Ceres, Vesta, Phoebe, Styx/Nix/Hydra/Kerberos | **0.88** | **2.2** |
| 이젝타 덮인 소형 위성 | Phobos, Deimos | 0.88 | **1.6** |
| 얼음/어두운 입자 표면 | Ganymede, Callisto, 얼음 위성들, Pluto, Charon, Triton, 소행성(Ida, Eros, Psyche, Ryugu, Pallas) | **0.38–0.45** | **2.2** |
| 밝은 유리질 얼음/화산 서리 | Europa, Io | 0.44–0.45 | **2.0** |
| 연무 낀 고체(예외 쌍) | Titan, Proteus | 0.56 | 2.2 |
| 먼지 많은 옅은 대기 지구형 | Mars | **1.56** | **1.0** |
| 두꺼운 대기 지구형 | Earth, Venus | 1.0 / 1.15 | ~1.0–1.15 (Earth는 해양 셰이더 경로) |
| 가스/얼음 거대행성 | Jupiter, Saturn, Uranus, Neptune | (0.44 템플릿) | **1.6** |

두 노브를 읽는 법(하나의 물리 상수가 아니라 렌더 체제 둘).

- **스케일드 `_Hapke`**는 원반 전체의 위상 거동 — 림까지 원반이 얼마나 평평하게
  밝은지, 보름 위상 근처에서 얼마나 급하게 밝아지는지("달다움") — 을 정한다.
  Sol의 컨벤션은 촘촘하다. **무대기 레골리스/얼음 = 2.2**, 밝은 유리질 얼음 =
  2.0, 거대행성과 이젝타 덮인 소형 위성 = 1.6, 대기 있는 천체 ≈ 1.0.
- **지형 `_Hapke`**는 지상에서의 역산란 반응 — 태양을 등지고 볼 때 지면이 얼마나
  밝아지는지 — 을 정한다. Sol은 이 값을 **불연속 패밀리 프리셋**({0.38–0.45,
  0.56, 0.88, 1.0, 1.15, 1.56})으로, 즉 표면 아날로그별로 배정한 뒤 패밀리 안에서
  바디별 룩 튜닝을 한다.

## 물리 층: 패밀리가 이 순서로 서는 이유

이 노브의 이름은 Hapke 양방향 반사 프레임워크
(Hapke 1981, [`1981JGR....86.3039H`](https://ui.adsabs.harvard.edu/abs/1981JGR....86.3039H))에서
왔고, 위상 거동은 두 opposition 메커니즘과 입자 위상함수가 정한다.

- **그림자 숨김 opposition 효과(SHOE)** — 위상각 0에서 공극과 입자 그림자가
  사라진다. 어둡고 다공질인 성숙 레골리스에서 가장 강하다
  (Hapke 1986, [`1986Icar...67..264H`](https://ui.adsabs.harvard.edu/abs/1986Icar...67..264H)).
  달의 원반이 림까지 평평하게 밝은 이유가 이것이고, 전구 분해 Hapke 파라미터
  지도는 Sato et al. 2014
  ([`2014JGRE..119.1775S`](https://ui.adsabs.harvard.edu/abs/2014JGRE..119.1775S)),
  수성 레골리스가 달과 같은 급의 급증을 보인다는 것은 Warell 2004
  ([`2004Icar..167..271W`](https://ui.adsabs.harvard.edu/abs/2004Icar..167..271W))가
  앵커다. → 무대기 레골리스의 스케일드 패밀리(2.2).
- **간섭 역산란 opposition 효과(CBOE)** — 알베도와 다중 산란이 클수록 자라는
  좁은 간섭 스파이크다
  (Hapke 2002, [`2002Icar..157..523H`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..523H)).
  대표 실측은 엔셀라두스의 급증(Verbiscer et al. 2005,
  [`2005Icar..173...66V`](https://ui.adsabs.harvard.edu/abs/2005Icar..173...66V))이다.
  밝은 얼음 표면은 (더 좁은) 강한 급증을 유지해 Sol에서 2.0–2.2에 머물고, 지상
  반응은 레골리스보다 매끈하게 읽혀 지형 값은 0.38–0.45로 내려간다.
- **opposition 진폭은 알베도에 단조가 아니다** — 소행성 분류를 가로지르면 중간
  알베도에서 최대이고 아주 어두운 쪽과 밝은 쪽 모두에서 작아진다(Belskaya &
  Shevchenko 2000, [`2000Icar..147...94B`](https://ui.adsabs.harvard.edu/abs/2000Icar..147...94B)).
  지형 노브가 단일 알베도 공식이 아니라 패밀리 프리셋인 이유다. 중간 알베도
  얼음 위성들의 원반 분해 광도는 Buratti & Veverka 1984
  ([`1984Icar...59..392B`](https://ui.adsabs.harvard.edu/abs/1984Icar...59..392B))가 앵커다.
- **대기는 원반 위상 곡선을 씻어 낸다** — 매끈한 산란 쪽으로(Mars 스케일드 1.0,
  Earth/Venus는 아예 무대기 경로 밖). 그때 원반 룩은 지면 광도가 아니라
  구름과 연무다.

## 실전 레시피 (바디 클래스별)

1. **스케일드 값은 클래스로 고른다** — 단단한 절반이다.
   - 레골리스를 가진 무대기 암석/얼음 → **2.2**
   - 밝은 유리질/서리 갱신 얼음(Europa/Io급) → **2.0**
   - 이젝타 덮인 소형 위성(Phobos급) → **1.6**
   - 가스/얼음 거대행성 → **1.6**
   - 실제 대기를 가진 고체 천체 → **1.0** (연무 낀 Titan은 Sol의 2.2 예외 —
     아트 판단을 따르되 명기)
2. **지형 값은 가장 가까운 표면 아날로그의 패밀리로 고른 뒤** 그 안에서 튜닝한다.
   성숙 달형 레골리스 1.0 · 어두운 암석 레골리스 0.88 · 얼음/어두운 입자
   0.38–0.45 · 먼지 사막 1.56. 우리의 우주풍화 상태(색 방법론 §4)가 바디를
   패밀리 *안에서* 움직인다. 차폐로 신선한 레골리스는 어두운 성숙 프리셋보다
  위(Luna 1.0 쪽), 포화 풍화 지형은 그 이하.
3. **평균 시각 알베도는 기존 색 방법론에 얹는다** — appearance의 `albedo_mean`
   필드는 최종 팔레트의 면적가중 **기하**(시각) 알베도이고, 에너지 수지용 Bond
   값은 surface 행에 남는다. 정의와 변환은 색·알베도 방법론 §6.
4. 두 값을 해당 바디 Phase 4 appearance 행에 typed field(`hapke_terrain`,
   `hapke_scaled`)로 기록하고, refs는 이 문서를 단다.

### 검증: 레시피가 Sol 자신의 배정을 재현한다

규칙 1–2를 보류해 둔 Sol 바디들에 눈감고 적용하면, Vesta/Ceres(어두운 암석
레골리스) → 0.88 / 2.2 ✓, 천왕성 위성들(얼음 어두운 입자) → 0.43 / 2.2 ✓,
Phobos(이젝타 블랭킷) → 스케일드 1.6 ✓, Neptune(거대행성) → 1.6 ✓, Mars(먼지,
옅은 대기) → 스케일드 1.0 ✓. 규칙이 못 맞히는 Sol의 유일한 예외는 Titan의
스케일드 2.2(규칙 1은 1.0라고 말한다)로, 위에서 아트 판단으로 명기했다.

## 작업 예시 (NearStars)

| 바디 | 클래스 읽기 | 지형 | 스케일드 | 비고 |
|---|---|---|---|---|
| Proxima d | 무대기 현무암 레골리스, 자기권 차폐로 중위도가 수성보다 신선, 극관은 풍화 포화 | **0.95** | **2.2** | Mercury 0.88과 Luna 1.0 사이: 무차폐 수성보다 npFe⁰ 성숙이 덜함 |
| Proxima c I | 톨린 물든 물얼음 기반암(카론 아날로그) | **0.43** | **2.2** | 얼음 패밀리 그대로; Sol의 Charon 자신이 0.43/2.2 |
| Proxima b | 암석 세계, 0.3 bar 대기, 호수 + 야간 얼음 | **1.0** | **1.0** | 지형은 달형 패밀리 육지, 스케일드는 대기 경로 |
| Proxima c | 차가운 mini-Neptune | (해당 없음) | **1.6** | 거대행성 패밀리; 지형 셰이더 없음 |

## 인용

- **Hapke, B. 1981**, JGR 86, 3039 ([`1981JGR....86.3039H`](https://ui.adsabs.harvard.edu/abs/1981JGR....86.3039H)).
  셰이더 이름의 유래인 양방향 반사 프레임워크. arXiv 없음(1981), bibcode 검증.
  색 방법론과 공유.
- **Hapke, B. 1986**, Icarus 67, 264 ([`1986Icar...67..264H`](https://ui.adsabs.harvard.edu/abs/1986Icar...67..264H)).
  그림자 숨김 opposition 효과(시리즈 4편). bibcode 검증, 프리프린트 없음.
- **Hapke, B. 2002**, Icarus 157, 523 ([`2002Icar..157..523H`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..523H)).
  간섭 역산란 opposition 효과(시리즈 5편). bibcode 검증.
- **Sato, H. et al. 2014**, JGR Planets 119, 1775 ([`2014JGRE..119.1775S`](https://ui.adsabs.harvard.edu/abs/2014JGRE..119.1775S)).
  달 전구 분해 Hapke 파라미터 지도(LROC WAC) — 달 앵커.
- **Warell, J. 2004**, Icarus 167, 271 ([`2004Icar..167..271W`](https://ui.adsabs.harvard.edu/abs/2004Icar..167..271W)).
  수성 레골리스 광도 파라미터 vs 달 — 어두운 레골리스 앵커.
- **Verbiscer, A. et al. 2005**, Icarus 173, 66 ([`2005Icar..173...66V`](https://ui.adsabs.harvard.edu/abs/2005Icar..173...66V)).
  엔셀라두스 opposition 급증(HST) — 밝은 얼음 CBOE 앵커.
- **Belskaya & Shevchenko 2000**, Icarus 147, 94 ([`2000Icar..147...94B`](https://ui.adsabs.harvard.edu/abs/2000Icar..147...94B)).
  소행성 분류별 opposition 진폭 vs 알베도(비단조).
- **Buratti & Veverka 1984**, Icarus 59, 392 ([`1984Icar...59..392B`](https://ui.adsabs.harvard.edu/abs/1984Icar...59..392B)).
  Voyager 토성 위성 원반 분해 광도.
- **RSS-Reborn/Sol-Configs @ f9e6fdf** — 엔진 쪽 canonical 소스(비-ADS 예외;
  핀된 커밋의 파일 직독으로 검증).

## Related

- [`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md) —
  이 레시피의 지형 튜닝과 `albedo_mean`이 얹히는 팔레트·우주풍화 상태(§4)·
  Bond/기하 알베도 엔진(§6).
- [`planet-pack-techniques.md`](planet-pack-techniques.md) — 행성팩에서 캔
  이웃 시각 기법들.
- [methodology-index](methodology-index.md) — 도출값 레시피 전체 인덱스.
