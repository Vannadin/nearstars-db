# Body-Tree Spec — Sun에 뿌리를 둔, 별들이 직속 자식인 구조

> 상태. **SPEC** (오너 승인 2026-07-18, s25 제안 R6/M-F). 파이프라인이 이미
> emit하고 있는 실제 구조를 기록한 문서이며, 새 emitter와 Principia 쪽 코드는
> 이 구조에 의존할 수 있습니다.

**스펙.** NearStars의 body tree는 **스톡 `Sun`에 단일 루트를 둔** 구조로,
모든 별(또는 근접 쌍성을 대신하는 barycenter)이 **`Sun`의 직속 자식**
(`referenceBody = Sun`)입니다. 행성/위성/원반은 평소처럼 자신의 별이나
barycenter에 parent됩니다. 따라서 성간 공간은 스톡 기준으로 보면 Sun의
SOI에 해당합니다. 각 별은 **스톡 Keplerian placeholder 궤도**를 Sun 주위에
가지고 있는데, 이는 KSP/Kopernicus가 tree를 구성할 수 있게 하는 대표 슬롯일
뿐 물리적 주장이 아니며, **실제 상태는 Principia-Cartesian**(바디별
`principia_initial_state`)입니다. Principia 관리 하에서는 placeholder와
공백에서의 스톡 SOI 역학이 무의미합니다. 스톡 SOI/궤도 semantics가 중요해지는
구간은 vessel이 Principia 관리에서 *풀려나는* 창구 뿐이며, 그중 주된 사례가
WS4 warp cruise입니다. 그 재편입 단계("목적지 별 주위의 목적지 스톡 궤도를
설정")가 바로 별들이 스톡 바디인 이 단일-루트 tree를 전제로 합니다.

**근거 (2026-07-18 검증됨).**

- Emitter. `.claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py`가
  모든 별 Body 노드에 대해 `referenceBody = Sun`을 emit합니다 (line ~857).
- 실사용 테스트 config. `test-configs/ws5-principia-probe/GameData/NearStars-Configs/`
  (`NearStars-Stars-Kopernicus.cfg` + `NearStars-StockKeplerian-Orbits.cfg`) —
  인게임 WS5/WS5-C 게이트가 실행된 바로 그 config입니다.
- 이는 Kopernicus 성간 팩의 표준 형태이기도 해서, 서드파티 툴링의 기대와도
  맞아떨어집니다.

**여기서 다루지 않는 것.** warp watchdog(타이밍/소유권은 여전히 별도 논의로
미룬 오너 미결 사항이며, 이 스펙에서 결정하지 않습니다).
