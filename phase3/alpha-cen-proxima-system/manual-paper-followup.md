<!-- α Cen + Proxima Phase 3 — arXiv-less high-score 페이퍼 후속 관리 -->
# Manual paper follow-up — α Cen + Proxima Cen system

ADS 키워드 점수 ≥ 14 인데 arXiv 프리프린트가 없어서 본문을 자동 fetch
할 수 없는 페이퍼들. Tier A 는 cfg 결정에 직접 영향이 있는 것들 (사용자 paste
요청), Tier B 는 컨텍스트, Tier C 는 안전하게 스킵.

본문 없이도 abstract + secondary citations 로 합성에 쓸 수 있는 것은
그대로 사용하되, Decisions 표 Basis 컬럼에 `abstract-only` 또는
`cited via [paper X]` 라고 표기.

---

## Tier A — drives cfg decisions

### Proxima b

- **Del Genio et al. 2019** — *Habitable Climate Scenarios for Proxima
  Centauri b with a Dynamic Ocean* (`2019AsBio..19...99D`, AsBio)
  - 왜 중요한지: Boutle 2017 의 정적 슬랩 ocean 모델을 동적 ocean 으로
    확장. dayside 에서 nightside 로 열을 운반하는 ocean current
    역할이 atmosphere 만의 GCM 보다 강하다는 결론. 1 bar / N₂ + CO₂
    atmosphere + 동적 ocean → substellar 어디서나 open water 가능.
  - 합성에서의 활용: ocean dynamics 가 atmosphere 만의 모델보다
    eyeball-Earth 의 open water 영역을 더 넓게 만들 수 있음을
    Decisions 표 Basis 에 인용. cited via Sergeev 2020 / Salazar 2020 /
    Boutle 2017 (모두 본문 캐시 보유).
- **Noack et al. 2021** — *Interior heating and outgassing of Proxima Centauri b*
  (`2021A&A...651A.103N`)
  - 왜 중요: Proxima b 의 mantle convection rate, outgassing flux 추정.
    오늘날 atmosphere 가 photochemically 가능한지의 interior boundary
    condition.
  - 합성에서의 활용: atmosphere_source 결정 시 outgassing 우세 vs 외부
    delivery 의 가중치를 잡는 데 인용. abstract + citations 로 충분.

- **Herath et al. 2021** — *Characterizing the possible interior structures
  of the nearby Exoplanets Proxima Centauri b and Ross 128 b*
  (`2021MNRAS.500..333H`)
  - 왜 중요: interior CMF (core mass fraction) 가능 범위, mass-radius
    관계로 ice content 제약.
  - 합성에서의 활용: surface_composition + planet_radius 결정 시 인용.
    abstract-only 로도 핵심 결론 (Earth-like 부터 Mercury-like 까지의
    interior 변화) 활용 가능.

### α Cen A / B

- **DeWarf et al. 2010** — *X-Ray, FUV, and UV Observations of alpha
  Centauri B* (`2010ApJ...722..343D`)
  - 왜 중요: α Cen B 의 8.1-yr 활동 사이클 + 36-40 d 회전 주기의 1차
    측정. DB Phase 2 의 `rotation_measurements` 와 `activity_measurements`
    recommended 소스. α Cen A 의 22 d 회전 + log R'HK = −4.95 도 같은
    프로그램에서.
  - 합성에서의 활용: rotation_period_days, activity_cycle_years
    Decisions 행의 Basis 직접 인용. abstract + DB attribution 으로 충분.

- **Dumusque et al. 2012** — *An Earth-mass planet orbiting α Centauri B*
  (`2012Natur.491..207D`)
  - 왜 중요: α Cen Bb 발견 주장 (Nature). Rajpaul et al. 2016 의
    재분석으로 retracted (window-function artifact). α Cen B 페이지의
    `Open items` + 역사 문맥에 인용.
  - 합성에서의 활용: α Cen B 의 planet history 단락. abstract + Rajpaul
    2016 본문 (캐시 보유) 으로 retraction story 작성 가능.

---

## Tier B — useful context, can wait

- Krishnamurthy 2021 (`2021AJ....161..275K`) — ASTERIA transit search.
  Sets transit non-detection limits.
- Ayres 2020/2021 (`2020ApJS..250...16A`, `2021ApJ...916...36A`) —
  Sun-stellar UV/X-ray. Activity sequence context.
- Engelbrecht 2024 (`2024ApJ...964...89E`) — 3D radiation environment of
  Proxima b.
- Quick 2023 (`2023ApJ...956...29Q`) — cryovolcanic activity on cold
  ocean planets. Generic but relevant to b's frozen-ocean alternative.
- Eriksson 2024 (`2024MNRAS.527.9522E`) — Fe II fluorescence in K dwarfs.

---

## Tier C — safe to skip

- Maccone 2014 (radio bridge engineering)
- Rai 2022 (intensity interferometry simulation)
- Houelle 2026 (conference proceedings)
- Hill 2023 (catalog)
- Armas-Vázquez 2023 (prebiotic chemistry, out of scope)
- Sadovski 2018 (cosmic rays near Proxima b)
- Duvvuri 2025 (EUV stellar library)
