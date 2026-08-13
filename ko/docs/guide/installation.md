<!-- 설치 방법과 모드 호환성 -->
# 설치 및 호환성

> **NearStars는 아직 출시되지 않았습니다.** 지금 당장 받을 수 있는 파일은 없습니다. 이 페이지는 출시 시점에 어떤 모습일지 가늠할 수 있도록 *예정된* 모드 스택을 설명하며, 세부 사항은 출시 전에 바뀔 수 있습니다.

## 대상 플랫폼

NearStars는 [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) 기반 Real Solar System 설치본 위에서 **KSP 1.12.x, Windows**를 대상으로 합니다. 실제 태양계 위에 항성계를 추가하는 방식이며, 스톡 시스템 자체를 대체하지는 않습니다.

## 예정된 의존성 스택

이 모드는 새로 만들기보다 이미 자리 잡은 RSS 비주얼·구조 스택을 그대로 활용합니다.

| 계층 | 모드 | 역할 |
|---|---|---|
| 코어 | [Kopernicus](https://github.com/Kopernicus/Kopernicus) | 항성·행성·위성 추가 (~50광년 범위) |
| 베이스 | [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) | NearStars가 확장하는 실제 태양계 |
| 비주얼 | Scatterer, EVE, [Firefly](https://forum.kerbalspaceprogram.com/topic/219890-firefly/) | 대기·구름, 물리적으로 근거화된 재진입 플라스마 색 |

## 두 가지 물리 프로파일 (예정)

성간 이동과 n-body 중력은 서로 반대 방향을 지향하는 요소라, NearStars는 하나의 프로파일로 둘 다 커버하는 척하지 않고 **두 가지 설치 프로파일**을 계획하고 있습니다.

- **Principia 프로파일**, 완전한 n-body 중력을 적용합니다. 쌍성은 실제로 질량중심을 공전하며, 이 모드의 궤도 해법 자체가 이를 전제로 만들어져 있습니다. 다만 정직한 물리 법칙에는 대가가 따릅니다. 별과 별 사이의 이동은 여러 세대에 걸친 일이 됩니다.
- **워프/엔드게임 프로파일**, 스톡 중력에 쌍성 운동을 위한 SigmaBinary를 더한 방식으로, 실전적인 성간 플레이를 위해 워프 드라이브 모드와 호환됩니다.

둘 중 하나를 설치하면 되고, cfg 자체는 양쪽 프로파일 모두를 위해 생성됩니다.

## 선택적 통합 (예정)

핵심 스택 외에도, 함께 사용하면 경험을 더 깊게 만들어주는 모드가 몇 가지 있습니다.

- **Kerbalism**은 실측된 X선 광도와 항성 활동으로부터 도출한 별마다의 방사선 환경을 제공합니다.
- **ResearchBodies**는 각 천체의 실제 발견 이력에 발견 난도를 대응시킵니다. 망원경으로 발견된 행성이라면 타겟팅하기 전에 먼저 찾아내야 합니다.
- **RP-1** 지원은 업스트림 Sol-Configs 쪽 RP-1 브릿지가 도착하면 계획되어 있습니다. NearStars는 Sol 기반을 유지하며, 별도로 포크하지 않고 그 브릿지에 올라탈 예정입니다.

## 라이선스

CC-BY-NC-SA 4.0입니다. 서드파티 데이터 출처 표기는 [NOTICE](https://github.com/Vannadin/nearstars-db/blob/main/NOTICE)에 들어 있습니다.
