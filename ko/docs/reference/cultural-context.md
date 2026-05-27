<!-- NS 시스템의 사이파이 / 대중문화 레퍼런스 인덱스 -->
# Cultural context — NS 시스템의 사이파이 레퍼런스

NearStars 는 실재 가까운 별을 다루고, 그중 일부는 사이파이에서 주요 무대로 등장합니다. 이 문서는 그 연결을 인덱스화하고, 소설 사실과 실제 사실을 구분하며, 소설이 plot 을 anchor 한 retracted / refuted 행성을 표시합니다. Cultural reference 는 cfg 로 emit 되지 않습니다 — 이 doc 는 narrative reference 전용입니다.

## Tau Ceti — *Project Hail Mary* (Andy Weir, 2021)

- **소설의 행성**: "Adrian" = Tau Cet e
- **실제 status**: Tau Cet e 는 2026-04-09 NASA Exoplanet Archive 에서 **"False Positive Planet"** 으로 재분류 되었습니다 (Figueira 외 2025, `2025A&A...700A.174F` ESPRESSO sub-10 cm/s RV 비검출 인용). 소설은 Feng 2017 검출 picture 기반으로 집필 되었고, 그 picture 는 이제 obsolete 입니다.
- **소설이 맞춘 점**: G8V 분광형, ~9 Gyr 나이 (태양의 두 배), 안정적 astrobiology 대상으로서의 Tau Ceti
- **소설이 틀린 점 (현 데이터 기준)**: Adrian 이 거주 가능한 super-Earth 라는 가정 — 기반 RV 신호가 이제는 항성 활동으로 간주됨. 또 실재의 잔해 원반 (ALMA-resolved 6–55 AU, ~1.2 M⊕, MacGregor 2016) 도 소설에 없는데, 실제 진입 시 항해 위험.
- **NS DB**: e 는 정상적으로 누락 상태 (NEA-inherited). f/g/h 는 여전히 `pl_controv_flag=1` 이지만 retraction watch (Figueira 2025 가 detection floor 근처/이하 보고).

## 40 Eridani A — *Star Trek* (Vulcan) + *Project Hail Mary* (Erid)

- **소설의 행성**: 40 Eri A b 가 *Star Trek* 의 Vulcan (Roddenberry 가 1991년 *Sky & Telescope* 편지에서 Epsilon Eri 가 아닌 40 Eri 로 확정). *Project Hail Mary* 의 Eridian (Rocky 종족) 도 40 Eridani A 출신.
- **실제 status**: 40 Eri A b 는 확정된 외계행성 (Ma 2018, `2018AJ....155..117M`); 주기 8.5 d, 8.5 M⊕ super-Earth. 현대 기준 거주 가능 영역 밖 — Vulcan 픽션이 발견 이전이라 Earth-like 세계를 가정함.
- **NS DB**: `40_eridani_a.json` + `40_eridani_b.json` (백색왜성) + `40_eridani_c.json` (M 왜성) — 다중성계

## Epsilon Eridani — *Babylon 5* (Vorlon homeworld), 초기 *Star Trek* (원래 Vulcan)

- **소설의 행성**: *Babylon 5* (J. Michael Straczynski) 의 Vorlon Prime. 40 Eri A 로 retcon 되기 전 초기 *Star Trek* 의 Vulcan.
- **실제 status**: ε Eri b 는 확정된 RV 행성 (Hatzes 2000 + Mawet 2019 직접 영상), ~3.5 AU, M sin i ~0.78 M_Jup — 가스 거인이지 Earth-like 아님. 세 띠 잔해 원반으로 둘러싸여 있음.
- **NS DB**: `eps_eri.json` (host + b 등재. Phase 3 합성 `docs/phase3/eps-eri.md` + `eps-eri-b.md`)

## Wolf 359 — *Star Trek: The Next Generation* (Battle of Wolf 359)

- **소설의 행성**: TNG "The Best of Both Worlds" (1990) 의 Battle of Wolf 359 는 Starfleet 의 Borg 조우 — 실제 별 위치 사용하지만 canonical 행성 없음.
- **실제 status**: Wolf 359 는 7.86 ly 의 M6.5 플레어 별. 확정된 행성 없음 (깊은 RV 상한).
- **NS DB**: `wolf_359.json` (host 만, 행성 없음)

## Alpha Centauri — *Avatar* (Pandora), *삼체*, 다수

- **소설의 행성**: *Avatar* (Cameron 2009) 의 Pandora 는 α Cen A 궤도. 류츠신 *삼체* 의 trisolaran 모성 (canonical 한 α Cen 3-body chaos 가 trisolaran problem 의 원조).
- **실제 status**: α Cen A/B + Proxima 가 ~13,000 AU 떨어진 hierarchical triple. Proxima b 는 거주 가능 영역 Earth-mass 확정. Proxima d 후보 (Faria 2022). α Cen A/B 행성은 미확정 (Beichman & Sanghi 2025 의 "S1" JWST/MIRI 후보 ~1.5 AU, follow-up 대기).
- **NS DB**: Jacobi 다중성 파이프라인 + Principia n-body export 가 적용된 완전 triple — NS 의 canonical hierarchical 다중성 쇼케이스

## 방법론 노트

픽션은 관측을 overrule 하지 않습니다. 소설이 plot 을 anchor 한 행성이 추후 refuted 되면 (Tau Cet e 처럼) NS DB 는 현실의 disposition 을 따릅니다. Cultural reference 는 narrative companion 으로 문서화되지 cfg-emitted description 으로는 안 됩니다. 미래에 per-body description string feature 가 ship 되면 이 doc 는 fiction-aware flavor text 의 source 가 됩니다 — 그때까지는 repo documentation 전용입니다.

## Related

- [rex-data-comparison](rex-data-comparison.md) — Tau Cet e 의 역사적 큐레이션 논의 (해결됨)
- [methodology](methodology.md) — 이 doc 가 존중하는 provenance-first DB 정책
- [`docs/phase3/eps-eri.md`](../phase3/eps-eri.md) — 호스트 합성 (Babylon 5 / Trek 노트 범위)
- [`docs/phase3/alpha-centauri-a.md`](../phase3/alpha-centauri-a.md) — 호스트 합성 (Pandora / trisolaran 컨텍스트 범위)
