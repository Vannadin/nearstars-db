# Planet Curation Reference

How to populate `db/planets_curated.json` for a host star, by depth tier.
Default is Phase 1; only escalate to Phase 2 on explicit user request.

---

## Phase 1 — Default (every new planet host)

Goal: one solid published source per planet, overriding NASA Archive
where the published paper is more precise or recent.

### Procedure per planet

1. **Identify the canonical paper.**
   - Discovery paper if the system is well-characterized (no major
     follow-up reanalyses).
   - Most recent re-analysis if mass/radius/orbital parameters were
     refined after discovery.
   - Quick check: NASA Archive의 `ps` 테이블 `default_flag=1` 행을 우선
     채택 (NASA 큐레이터의 권위 paper 선택). `fetch_planets_ps.py` 사용.
     ADS abstract 직접 조회는 JS 렌더링 때문에 어시스턴트 도구로 불가.

2. **Cross-check NASA Archive `pl_refname`.** If Archive cites the same
   paper you found, the auto-fetch is already using the best source —
   you can still add a curated entry to make the provenance explicit and
   to pin down orbital elements (ω, M₀, T_peri) that Archive composites
   sometimes mix from different solutions.

3. **For RV-detected planets, check DACE if NASA Archive lacks `omega_deg`
   or `tperi_bjd`.** DACE typically has the full orbital element set
   including uncertainties. URL pattern:
   `https://dace.unige.ch/exoplanets/?planet=<name>`

4. **For transiting planets, TEPCat is already auto-matched.** No extra
   action needed unless you want to override TEPCat with a more recent
   transit-light-curve fit.

5. **Compose the `planets_curated.json` entry.** Schema is in
   [file-edits.md §6](file-edits.md#6-dbplanets_curatedjson--phase-1-default-for-planet-hosts).

### What to record vs leave null

| Field | When to fill | Source |
|---|---|---|
| `semi_major_axis_au` | Always | Discovery paper |
| `eccentricity` | Always | Discovery paper; null only if explicitly unconstrained |
| `inclination_deg` | If transit OR astrometric fit | Transit fits give 88-90°; RV-only is null |
| `omega_deg` | RV systems usually have this | DACE or discovery paper |
| `mean_anomaly_at_epoch_deg` + `epoch_jd` | If T_peri is published | Convert T_peri to M₀ at chosen epoch |
| `true_mass_mearth` | If astrometry/transit gives it | Otherwise `mass_mearth` with `mass_type: "Msini"` |
| `radius_rearth` | Only if transiting | Null otherwise |
| `mass_type` | Always | `"Msini"`, `"true mass"`, `"transit"`, etc. |

### ADS access — NOT via WebFetch

**Important (2026-05-19 발견)**: `ui.adsabs.harvard.edu`는 JS-rendered SPA라
`WebFetch` 도구로 접근 불가. 모든 abstract / search 페이지가 빈 응답 반환.
ADS API 토큰을 발급받지 않는 한 직접 abstract 읽기 불가능.

**채택된 우회 경로:**
- **bibcode 자체가 ADS 정식 ID**이므로 출처 진실로 사용. paper의 abstract을
  읽지 않아도 bibcode 명시만으로 출처 attribution이 정확함.
- DOI는 Crossref API로 보조 해석 (인증 불필요).
- batch curation 시 NASA Archive의 `ps` 테이블 + `default_flag=1`이 paper별
  출처를 이미 제공 — `pl_refname` / `st_refname`에서 bibcode 추출 가능.

### 권장 인프라 (batch curation)

신규 스크립트 2개로 자동화됨.

```bash
# 1) ps 테이블에서 default 행 fetch
python3 scripts/pipeline/fetch_planets_ps.py
#    → db/planets_ps_default.json (per-paper rows for each planet)

# 2) curated JSON 생성 (Crossref로 DOI 해석)
python3 scripts/pipeline/build_curated_from_ps.py
#    → db/planets_curated.json + stellar_props_curated.json
#    Auto-added entries get method="unverified" (Phase 2 격상 시 교체 대상).

# 3) 기존 파이프라인 실행
python3 scripts/pipeline/build_systems.py
python3 scripts/pipeline/validate.py
```

이 흐름은 별 1개 추가에도 동일하게 작동 — `target_list.json`에 entry
추가 후 위 3단계 실행.

### 수동 ADS 조회 필요 시

다음 케이스만 수동:
- Phase 2 격상 (method 라벨을 paper의 실제 method로 교체)
- NASA Archive에 없는 신규 발견 행성
- ADS bibcode가 NASA의 `pl_refname` URL parsing에 실패한 케이스

수동 조회는 사용자가 browser로 [ui.adsabs.harvard.edu](https://ui.adsabs.harvard.edu)에서 직접
확인 후 결과를 세션에 paste. 어시스턴트가 ADS web을 직접 접근 시도하지 말 것.

### When to skip Phase 1

- Planet was just announced (within 1-2 weeks) and not yet in NASA
  Archive — but discovery paper is available: add it manually with
  `retrieval_date: today`.
- Planet has been retracted: don't add a curated entry, and note in
  `meta.notes` of the host star file.
- All Archive values match the discovery paper exactly: curated entry
  still useful for explicit provenance, but optional.

---

## Phase 2 — Explicit escalation (in-game implementation)

Triggered by user phrases like:
- "Phase 2로 격상해줘"
- "이 시스템 인게임에 구현하자"
- "정밀 큐레이션 부탁해"
- "X 시스템 풀 큐레이션"

모호한 신호("더 깊이 봐줘", "자료 더 모아줘") 는 Phase 2 의도인지 먼저
확인. 단일 paper 추가 요청은 Phase 1 범위.

### 진입 전 필수 산출물 (CLAUDE.md §7)

Phase 2 는 시스템당 1-2시간 작업이라 코드 작성 전에 다음 두 파일을
작업 디렉토리에 생성한다.

- `checklist.md` — 행성별 priority 1-5 소스 확인을 체크박스로
- `context-notes.md` — paper 선택, tier 충돌 해소, recommended 결정
  사유를 작업 중 계속 append

이후 세션(또는 같은 세션 재개 시) 산출물 없이 Phase 2 재개 불가 — 작업
중 결정 맥락이 손실됨.

Goal: comprehensive measurement collection per the methodology's
five-priority order, with one explicitly chosen `recommended: true`
based on method tier.

### Procedure per planet

1. **Run Phase 1 first** if not already done (gets the baseline curated
   entry).

2. **Survey all five priority sources:**
   - Priority 1 — Individual paper (ADS): the discovery paper *and* any
     subsequent reanalysis. Add each as a separate measurement object.
   - Priority 2 — DACE: pull current orbital fit, especially for RV systems.
   - Priority 3 — TEPCat: for transiting planets, get all published
     transit-derived values, not just the latest.
   - Priority 4 — exoplanet.eu: usually a mirror; only add if it has
     something Archive doesn't.
   - Priority 5 — NASA Archive: already auto-fetched; no action.

3. **Accumulate measurements in arrays.** For Phase 2, expand the
   single-entry physical and orbital sections into arrays.
   
   **⚠ Prerequisite — code change first:** As of 2026-05-18,
   `build_planet_derived` in `scripts/pipeline/build_systems.py` reads
   `curated["physical"]` and `curated["orbital"]` as single dicts (via
   `(curated or {}).get("orbital") or {}`). Array-form curated entries
   will be silently ignored. Before any Phase 2 work:
   
   - Extend `build_planet_derived` to accept either dict or list-of-dict
     for `physical`/`orbital`. When list, pick the entry with
     `recommended: true` (parallel to `mass_measurements` logic).
   - Add a schema check in `schema.py` to enforce exactly-one
     `recommended: true` per array.
   - Update this skill's `references/planet-curation.md` to remove this
     warning.
   
   After the code change, the array form looks like this:

```json
"physical": [
  {
    "true_mass_mearth": 1.27,
    "uncertainty_mearth": 0.18,
    "mass_type": "Msini",
    "method": "RV",
    "source": "Anglada-Escudé 2016",
    "doi": "10.1038/nature19106",
    "recommended": false
  },
  {
    "true_mass_mearth": 1.07,
    "uncertainty_mearth": 0.06,
    "mass_type": "true mass",
    "method": "astrometric",
    "source": "Anglada-Escudé 2022 reanalysis",
    "doi": "10.1051/0004-6361/202242750",
    "recommended": true
  }
]
```

Note: this is an *extension* of the schema in
[file-edits.md](file-edits.md). `build_systems.py` needs an update to
handle array-form physical/orbital — verify before committing Phase 2
work. (As of 2026-05-18 the build script reads single-object form only.)

4. **Apply method hierarchy to set `recommended`:**

   | Tier | Method (decreasing priority) |
   |---|---|
   | 1 | astrometric / direct (true mass) |
   | 2 | TTV / dynamical |
   | 3 | RV (Msini) |
   | 4 | transit-only (radius only) |
   | 5 | predicted / theoretical |

   Tie within tier → smaller fractional uncertainty wins. Record the
   choice and tiebreaker reasoning in the host star file's `meta.notes`
   after the build runs.

5. **Conflict handling:**
   - If two measurements at the same tier disagree by ≥ 30%, surface to
     user — that's not a tiebreaker case.
   - If a measurement uses a method not in the hierarchy (e.g.
     "phase-curve thermal mapping" for radius), surface and ask user
     where to place it in priority order.

### TRAPPIST-1 as the canonical Phase 2 target

Likely first in-game implementation. Phase 2 should produce:
- 7 planet entries, each with discovery paper + Agol 2021 TTV + JWST
  atmospheric papers where relevant
- Mass measurements: Agol 2021 (dynamical, recommended) + Gillon 2017
  (discovery, non-recommended)
- Radius measurements: Agol 2021 (TTV-constrained) + JWST follow-ups

Estimated time: 1-2 hours.

---

## Quality checks

After editing `planets_curated.json`, verify:

```bash
python3 -c "import json; d=json.load(open('db/planets_curated.json')); 
print(f'Hosts: {len(d)}'); 
print(f'Planets: {sum(len(v) for v in d.values())}'); 
[print(f'  {h}: {[p[\"pl_name\"] for p in pls]}') for h, pls in d.items()]"
```

Then re-run the pipeline. Check that each new planet's
`derived` block in the system file has the curated values flowing through:

```bash
python3 -c "import json; d=json.load(open('db/systems/<host>.json'));
for p in d['planets']: print(p['name'], p['derived'])"
```

If curated values aren't appearing, check that `pl_name` exactly matches
between `planets_curated.json` and `planets_raw.json` (whitespace counts).
