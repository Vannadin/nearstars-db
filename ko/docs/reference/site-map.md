<!-- docs/ 발행 페이지 사이트맵 + 연결성 감사 (build_sitemap.py 자동 생성) -->
# 사이트맵: 발행 문서 표면

> `python3 scripts/build_sitemap.py`로 생성. 손으로 고치지 말 것.
> 페이지 270개, 합계 21.6 MB, 내부 링크 4463개.
> gitignore된 논문 캐시(`docs/phase3/_papers/`)는 사이트가 아니라 로컬 캐시라 제외한다.

## 구조

| 구획 | 페이지 | 용량 | 역할 |
|---|---:|---:|---|
| `root` | 6 | 2.4 MB | Top-level surfaces |
| `wiki` | 58 | 2.8 MB | Rendered reference docs + plans |
| `phase2` | 77 | 1.1 MB | Per-host measurement reports |
| `phase3` | 81 | 5.8 MB | Per-planet synthesis reports |
| `phase4` | 48 | 9.4 MB | Decision boards + orbit viewers |

**허브**(아웃바운드 링크 최다):
- `reports.html` → 178
- `wiki/index.html` → 61
- `wiki/plans__derived-value-grounding-audit.html` → 61
- `wiki/plans__doc-tool-sprawl-audit.html` → 61
- `wiki/plans__nearby-field-viewer.html` → 61
- `wiki/plans__paper-scoping.html` → 61

주의: `index.html`은 목록을 `reports-manifest.json`에서 런타임에 만들기 때문에 정적 href가 거의 없다. 실제로는 phase2/phase3 리포트 전부로 이어지는 최대 허브다. 위키 페이지들이 61개씩 갖는 아웃바운드는 페이지마다 실린 전체 사이드바다.

## 결함

**고아 페이지 (인바운드 0, 클릭으로 도달 불가): 5**

- `belt-viewer.html`
- `ice-stability.html`
- `phase4/index.html`
- `phase4/orbit-viewers/alpha-centauri-validation/index.html`
- `phase4/orbit-viewers/index.html`

**막다른 페이지 (아웃바운드 0, 되돌아갈 링크 없음): 18**

- `belt-viewer.html`
- `ice-stability.html`
- `phase4/orbit-viewers/40-eridani/interactive.html`
- `phase4/orbit-viewers/40-eridani/orbit3d.html`
- `phase4/orbit-viewers/alpha-centauri-validation/moon_leapfrog.html`
- `phase4/orbit-viewers/alpha-centauri-validation/moon_megno.html`
- `phase4/orbit-viewers/alpha-centauri-validation/planets_leapfrog.html`
- `phase4/orbit-viewers/alpha-centauri-validation/planets_megno.html`
- `phase4/orbit-viewers/alpha-centauri/interactive.html`
- `phase4/orbit-viewers/alpha-centauri/orbit3d.html`
- `phase4/orbit-viewers/barnards-star/interactive.html`
- `phase4/orbit-viewers/barnards-star/orbit3d.html`
- `phase4/orbit-viewers/proxima-cen/interactive.html`
- `phase4/orbit-viewers/proxima-cen/orbit3d.html`
- `phase4/orbit-viewers/tau-cet/interactive.html`
- `phase4/orbit-viewers/tau-cet/orbit3d.html`
- `phase4/orbit-viewers/trappist-1/interactive.html`
- `phase4/orbit-viewers/trappist-1/orbit3d.html`

## CDN 의존

네트워크가 없으면 설계대로 렌더되지 않는 페이지들이다.

- `cdn.jsdelivr.net` — 68 페이지
- `fonts.googleapis.com` — 31 페이지

## 최대 용량 페이지

- `phase4/orbit-viewers/trappist-1/interactive.html` — 1431 KB
- `starmap.html` — 1258 KB
- `phase4/orbit-viewers/alpha-centauri/interactive.html` — 1023 KB
- `phase4/orbit-viewers/alpha-centauri-validation/moon_leapfrog.html` — 1019 KB
- `phase4/orbit-viewers/alpha-centauri-validation/moon_megno.html` — 1017 KB
- `firefly-colors.html` — 936 KB
- `phase4/orbit-viewers/barnards-star/interactive.html` — 776 KB
- `phase4/orbit-viewers/tau-cet/interactive.html` — 768 KB

<!-- generated 2026-08-07 17:24 -->
