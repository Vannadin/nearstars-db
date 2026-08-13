<!-- 브라우저에서 바로 열리는 뷰어·보고서 목록 -->
# 뷰어 갤러리

정식 릴리스를 기다릴 필요가 없습니다. 이 프로젝트가 만들어내는 모든 결과물은 지금 당장 브라우저로 볼 수 있고, 전부 데이터베이스에서 직접 생성한 정적 HTML이라서 지금 보고 있는 화면이 곧 모드가 빌드될 원본 그대로입니다. 가장 넓은 시야에서 시작해 근거 자료로 좁혀가며, 열어볼 만한 것들을 순서대로 소개합니다.

## [3D 성도](https://vannadin.github.io/nearstars-db/starmap.html)

연구 데이터베이스 전체를 공간에 펼쳐 놓은 화면입니다. 50광년 이내에 큐레이션된 모든 항성계가 Gaia 측성 데이터를 바탕으로 배치되어 있습니다. 항성계를 클릭하면 행성 궤도가 표시되는 AU 단위 화면으로 들어가며(비교를 위해 태양계도 포함되어 있습니다), 항성권(별마다의 astrosphere 거품), 성간풍 벡터, 항성 자전축(측정값과 가정값 구분), 공간 속도, 그리고 50광년 이내 약 1,300개 배경 항성 레이어를 각각 켜고 끌 수 있습니다. 한/영 토글도 내장되어 있습니다.

## [데이터베이스 뷰어](https://vannadin.github.io/nearstars-db/)

표 형태의 프론트엔드입니다. 모든 항성계, 별, 행성의 측정값, 출처, 도출값을 필터링하고 정렬할 수 있게 보여줍니다. 요약이 아니라 실제 `db/systems/` 내용을 그대로 렌더링한 것입니다.

## [궤도 뷰어](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/)

로스터에 포함된 6개 행성계의 n-body 시뮬레이션 결과를 Plotly로 인터랙티브 3D 렌더링한 것입니다. 회전하고 확대하며 안정성 시뮬레이션이 실제로 만들어낸 궤도를 직접 살펴볼 수 있습니다. 항성계별 결과는 [항성계 소개](star-systems.md) 페이지에서 확인할 수 있습니다.

## [방사선대 뷰어](https://vannadin.github.io/nearstars-db/belt-viewer.html)

Kerbalism 방사선장을 실시간으로 계산합니다. 인게임 signed-distance-field 모델
그대로에 모든 cfg 파라미터 슬라이더, 자화된 태양계 7개 천체 프리셋(실배포 스톡
cfg vs 물리 피팅판 나란히) + NearStars 바디, 3D 볼륨 레이마칭 모드, 현재 모양을
Kerbalism cfg 블록으로 내보내는 원클릭 복사까지 들어 있습니다. 각 프리셋의 물리
근거는 [방사선대](../reference/solar-system-radiation-belts.md) 페이지에 있습니다.

## [큐레이션 리포트](https://vannadin.github.io/nearstars-db/reports.html)

근거 자료 모음입니다. Phase 2 리포트는 모든 측정값을 출처 논문과 함께 제시하고, Phase 3 리포트는 모든 인게임 결정을 그 근거, 신뢰도와 함께 제시하며, 모드가 정설(canonical) 해석에서 벗어난 경우에는 그 대안을 문서화한 섹션도 함께 담고 있습니다. 각 리포트에는 영/한 토글이 있습니다.

## [Phase 4 보드](https://vannadin.github.io/nearstars-db/phase4/)

아트 디렉션 레이어입니다. 오너가 내린 최종 인게임 선택을 바디별 보드에 확정해 두었고, 각 선택은 Phase 2/3 근거 범위에 맞춰 게이트를 통과한 것입니다.

## [레퍼런스 라이브러리(렌더)](https://vannadin.github.io/nearstars-db/wiki/)

저장소 내부의 레퍼런스 문서와 계획 문서를 HTML로 렌더링한 것으로, [방법론 라이브러리](../reference/methodology-index.md)가 색인하는 것과 동일한 파일에 그 바탕이 된 연구 노트까지 함께 담고 있습니다.
