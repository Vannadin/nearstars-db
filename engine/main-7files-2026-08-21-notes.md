<!-- main 체크아웃의 미커밋 7파일 = 2026-08-21 20:21–20:31 작업의 잔여(Dante 521 km 전파 절반), 그리고 engine/prototype 과의 분기. 병렬석 기록, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (MAIN-7FILES-2026-08-21.md, 19:40:33 KST), body unedited. The seven files are untouched (no add/stash/checkout); their disposition is the owner's decision. -->

# main 체크아웃 미커밋 7파일 = 2026-08-21 잔여작업, 그리고 브랜치 분기
Parallel seat, 2026-09-04. main 체크아웃(`/Users/vana/Desktop/NearStars`)은 `git status`·`git diff`·
`git log`·`stat` 만 사용했고 add/stash/checkout 없음. 판단 없이 병치.
아래 본문은 2026-09-04 에 nearstars-77 로 보낸 메시지 그대로입니다.

⚠ **먼저 브리프 전제 정정 두 개.**
① 이 7파일은 **크래시 전 최근 세션이 아니라 2026-08-21 20:21–20:31 의 작업**입니다(파일 mtime 7개 전부
그 10분 안). ② 그리고 `phase4/alpha_centauri.yaml` 의 미커밋 부분은 **521 km·78× 를 identity 행에
전파하는 중간 작업이 맞지만, bulk 행(mass/radius)은 건드리지 않습니다** — bulk 행은
**engine/prototype 브랜치가 이미 커밋으로 갖고 있고 main 은 아직 900 입니다**. 두 브랜치가 이 파일에서
갈라져 있습니다.

# 1. 7파일 diff 요약 (`+97 / −42`)

| 파일 | 변경 | 요지 |
|---|---|---|
| `docs/reference/tidal-heating-methodology.md` | 1 hunk (`@@ -460`) | Dante 삼축 기복 재계산. 삭제: "Dante's `J₂ = 0.039` / `C₂₂ = 0.0118` give `a = 549.6`, `b = 512.7`, `c = 500.7 km`, … relief of **48.9 km**". 추가: "`J₂ = 0.039` through the volume-conserving synchronous figure of `body-figure-methodology.md` (`a/R = 1 + 7J₂/3`, `b/R = 1 − 2J₂/3`, `c/R = 1 − 5J₂/3`) gives `a = 568.4`, `b = 507.4`, `c = 487.1 km`: … relief of **81.2 km** … sea level … imposed at the polar radius" |
| `ko/docs/reference/tidal-heating-methodology.md` | +8 | 같은 문단의 미러, 같은 수(568.4/507.4/487.1, 81.2 km). **미러 정합** |
| `phase3/stability-sim/DANTE_HEAT_TRANSPORT_EVIDENCE.md` | `@@ -157` | 같은 재계산 + **자기정정 문단**: "*Correction:* an earlier pass of this file used a = R(1 + J₂/2 + 3C₂₂) and reported 48.9 km. **That form is not volume-conserving and is not the project convention**; the numbers above supersede it." 그리고 "relief a−c = **81.2 km**, i.e. **16.7 % of the polar radius, which reproduces the board's existing 'a−c ~16 % egg' note**", `scripts/refs/body_figure.py::ellipsoid_ratios`, 협곡 예산 "up to 81 km … (Valles Marineris is 7 km deep)" |
| `phase3/stability-sim/checklist.md` | +3/−3 | 두 항목 `[ ] → [x]`: "Author the `tidal-heating-methodology.md` §6 extension … — §6.1–6.5, **`c29204a5`**", "Index row + ko mirror wording update … build_docs; check.sh". 남은 미체크: "Phase 4 rows to re-run once the doc lands: Dante bulk (radius/mass/gravity —" |
| `phase3/stability-sim/hypotheticals/alpha_centauri.json` | +6/−6 | **Dante `mass_kg` 8e+21 → 1.552e+21, `radius_km` 900 → 521**; **Hades `eccentricity` 0.05 → 0.01, `inclination_deg` 11.0 → 5.0**; 파일 끝 개행 추가. `_comment` 에 `[2026-08-21 revision]` 문단 삽입 — "Dante resized 900 -> 521 km … because the surface heat-transport check rejects 900 km: at 11,500 W/m2 a 5% lava-lake area would need 230 kW/m2, 2.1x the maximum ever measured … Hades moved to e 0.01 / inclination 5 deg: the shipped e 0.05 / i 11 deg is **chaotically lost to Polyphemus at ~56 kyr (impact, not escape) in 20/20 phase realizations**. The two changes together survive **4/4 phases over 1e5 yr**" |
| `…/results/_snapshot500/alpha_centauri_massB_input.json` | +6/−6 | **위 파일과 바이트 동일한 변경**(같은 두 hunk + 같은 `_comment`). 두 파일 정합 |
| `phase4/alpha_centauri.yaml` | +74/−16 | 아래 상세 |

## `phase4/alpha_centauri.yaml` 미커밋 hunk 전부 (7군데)

| hunk | 내용 |
|---|---|
| `@@ -278`·`-285` | Polyphemus 서사: 위성 경사 "about 10°" → "**5–10°**"(영/한 미러 둘 다) |
| `@@ -295`·`-299`·`-307`·`-310` | evidence: "inner Dante/Hades/Pandora ~9–11°" → "**inner Dante 9° / Hades 5° / Pandora 10°**"; epoch 진동값 "Hades ~16°/Pandora ~18°, Cassandra ~168°" → "**Hades ~12°/Pandora ~14°, Cassandra ~169°**"; 추가 "**Hades moved 11° → 5° on 2026-08-21** for 1e5-yr survival (satellites row, `stability_scans.dante_resize_2026_08_21`); the shared node line and the 'coherent warp' reading are unchanged, and **the spin axis stays at 5°**" (한글 미러 동일) |
| `@@ -1436` | Dante identity `body_type`: "silicate volcanic moon (**900 km, 8.0e21 kg**, ρ ~2620)" → "(**521 km, 1.552e21 kg**, ρ ~2620)" |
| `@@ -1444`·`-1445`·`-1448` | Dante identity narrative: "powered by the **~1200× Io** flux in the bulk.tidal_heating row" → "**~78× Io**"; 한 줄 신설 "**The radius was 900 km until 2026-08-21; the surface heat-transport check retired it (bulk row).**"(한글 미러 동일) |
| `@@ -3301`·`-3309` | satellites evidence 추가 "[2026-08-21] That 1000-yr verdict holds but was not enough: at a 1e5-yr horizon the shipped Hades (e 0.05 · i 11°) **falls into Polyphemus at ~56 kyr**, so the design moved to Hades e 0.01 · i 5° plus a 521 km Dante, which **survives 4/4**"; refs 에 `phase3/stability-sim/results/hades_rescue/README.md` 추가 |
| `@@ -3372` (+25행) | `stability_scans.dante_resize_2026_08_21` 신규 절 — Hades 소실이 이탈이 아니라 충돌(근점 1.45 → 0.60 R_p, 강체 로슈 1.31 통과), 순방향 20/20·역방향 3/4 사망, 쌍별 Hill 간격표(Dante–Hades 16.2 / Hades–Pandora 4.15 / Pandora–Cassandra 6.09 / Cassandra–Chaos 11.5, 갈릴레이 14–16), 반장축 스캔 35후보 중 생존 3, 채택안, 역행 기각 근거, Hades 자리 쌍성 기하 불가, 그리고 ⚠ 부산물 — "**현재 Dante(110k)는 동기궤도(119,392 km = 1.67 R_p) 안쪽이라 그 자체로 0.3–0.9 Myr에 로슈에 닿는다** … k₂/Q 0.5/3e4–1e5 목성 유추 — 채택 전 근거화 필요" |
| `@@ -3389` (+10/−5) | `satellites` 스냅샷 5행 전부 재산출(`results/_snapshot500/elements_2026-08-21.log`). Dante `mass_kg 8.0e21 → 1.552e21`, `radius_km 900 → 521`, 요소 `a 109890.2→110044.5 · e 0.01334→0.02432 · inc 7.341→4.301` 등; Hades `design.e 0.05→0.01 · design.inc 11.0→5.0`, 요소 `inc 16.245→12.023`; Pandora `e 0.00589→0.00366 · inc 18.212→14.045`; Cassandra `a 599190.2→586417.9 · inc 168.118→168.988`; Chaos `a 1574350.1→1558804.0 · inc 176.540→176.816`. 주석에 "다섯 위성 각도가 전부 갱신된 것은 같은 이유(위상 탈상관)이고, 한 런에서 나온 값이라야 표가 자기일관하므로 Pandora·Cassandra·Chaos도 같이 갱신", "Pandora e 0.00366(해양한계 0.0075 내)", "**1e5yr 재검증(validate_orbits moons 셀)은 대기 중**" |

## 정합성 — 브리프가 물은 세 점

| 물음 | 답 (main 워킹카피 현재 상태) |
|---|---|
| `tidal_heating :1553-1554` 가 여전히 1200×/11,500 인가 | **그렇습니다.** main 워킹카피 `:1555` `tidal_heating = "~1200× Io (…)"`, `:1556` `tidal_surface_flux = "~11,500 W/m² (…)"` — 미커밋 diff 가 이 두 행을 **건드리지 않습니다** |
| identity 행만 78× 로 바뀐 것인가 | **그렇습니다.** `body_type`(`:1436→1440`)과 identity narrative 만 521/78× 로 갔고, 조석 행·bulk 행은 그대로 |
| `geopotential_j2` `reference_radius_km: 900` | **그대로 900 입니다** — main 워킹카피 `:1482`. 그리고 main 은 그 위 `reference_radius` 도 **900**(`:1479`), `mass 8.0e21`(`:1475`), `radius 900`(`:1476`), `gravity 0.659`(`:1477`) |

⚠ 즉 미커밋 상태의 main 보드는 **내부 불일치**입니다: `body_type` 은 521 km·1.552e21, bulk 행은
900 km·8.0e21. checklist 의 남은 미체크 항목이 정확히 그것을 예고합니다 — "Phase 4 rows to re-run once
the doc lands: **Dante bulk (radius/mass/gravity —**".

# 2. 어느 세션 것인지

- **파일 mtime 7개 전부 2026-08-21 20:21:21 ~ 20:31:30** (checklist 20:21:21 → sim json 둘 20:25:07 →
  phase4 20:30:08 → 영문 doc 20:31:04 → 증거파일 20:31:17 → ko 미러 20:31:30).
- transcripts 에서 `phase4/alpha_centauri.yaml` 에 대한 `Edit`/`Write`/`MultiEdit` 호출: **전 기간 0건**.
  이유는 보존 범위입니다 — `~/.claude/projects/-Users-vana-Desktop-NearStars/` 에 `.jsonl` 이
  **25개뿐이고 가장 오래된 것이 2026-08-29 15:45** 입니다. **08-21 세션의 transcript 는 남아 있지 않습니다.**
- 경로를 언급만 하는 transcript(참고): `a0402cc0…`(28회, 09-04 19:37) · `50b7abc7…`(50회 — 이 세션) ·
  `a641e8a4…`(31회) · `25f71c48…`(2회) 등. 전부 09-03 이후이고 편집 호출은 없습니다.
- 즉 **세션 id 로는 특정 불가**이고, 대신 그 작업이 남긴 자기 서명이 있습니다: `_comment` 의
  `[2026-08-21 revision]`, 보드의 `stability_scans.dante_resize_2026_08_21`, 스냅샷 로그 이름
  `elements_2026-08-21.log`, checklist 의 "owner decision 2026-08-21".

# 3. 브랜치 분기

`git diff --stat main engine/prototype -- phase4 docs/reference ko phase3/stability-sim` →
**31 파일, +6312 / −62**. 대부분은 engine 쪽이 새로 쓴 방법론 문서(interior-structure +2001,
body-class +229, core-state +193, derivation-discipline +172, paper-defects +79 등 + ko 미러)이고,
`phase3/stability-sim` 은 **한 파일도 diff 에 없습니다**(두 브랜치 동일).

`phase4/alpha_centauri.yaml` 은 **18행 다릅니다**:
- `@@ -1469,3 +1469,7` — engine 쪽이 `mass 8.0e21 → **1.552e21**`(+note "sized by the surface heat
  transport gate, DANTE_HEAT_TRANSPORT_EVIDENCE.md"), `radius 900 → **521**`(+note "…**rejected 900 km**
  — a 5 % melt lake would need 2.1x the observed maximum areal flux"), `gravity 0.659 → **0.382**`
- `@@ -1473 +1477` — `reference_radius 900 → **521**`
- `@@ -2402/-2422/-2713` — `base_colour → base_color` 필드명 개명 3곳(축 주석 포함)

이를 만든 커밋: `git log main..engine/prototype -- phase4/` →
**`d6d78b63` "fix(phase4): take the size the heat-transport gate chose for Dante"
(2026-08-25 18:42:43 +0900)**, 그 외 `d16f1d6a`·`58190f68`·`ad4d3de9`·`92041e6e`(field-standard 계열).

⚠ **그래서 08-21 작업이 두 갈래로 갈렸습니다.** bulk 행 절반은 `d6d78b63`(08-25)으로
**engine/prototype 에만** 커밋됐고, identity·서사·스냅샷·삼축기복·sim json 절반은 **main 에서
미커밋으로 남았습니다.** 그리고 engine/prototype 쪽에는 후자가 **없습니다** — 확인: engine 워크트리
`:1436` 은 아직 `body_type … (900 km, 8.0e21 kg …)`, `:1444` 은 `~1200× Io`, 조석 문서 `:472` 는
`a = 549.6 … 48.9 km`, 증거파일 `:158-159` 도 `549.6 … 48.9 km`, sim json 은
`mass_kg 8e+21 / radius_km 900`.

⚠ 하나 더 — 앞선 보고에서 인용한 **Pandora e_max 0.007215
(`results/_final32b/alpha_centauri_summary.json`)는 Dante 900 km · Hades e 0.05/i 11° 구성으로 돌린
결과**입니다. 08-21 스냅샷 주석은 같은 양을 `e 0.00366` 으로 적습니다(다른 런·다른 구성). 어느 쪽을
쓸지는 판단 사항이라 병치만 합니다.
