# NearStars 성간 브랜치 — 여기서 시작 (START HERE)

이 디렉토리는 NearStars 성간 정밀도(interstellar-precision) 작업의 설계 + 구현
스펙을 담는다. **코드와 스펙 모두 이 저장소(`Vannadin/Principia`)의 이 브랜치
(`nearstars-interstellar`)에 함께 산다.** 구현하는 데 다른 저장소는 필요 없다.

## 저장소 지도 (누가 누구인가)

```
mockingbirdnest/Principia        upstream, public open source — never edited, just the fork root
        │ fork
        ▼
Vannadin/Principia   ◀── YOU ARE HERE. The only working repo.
   branch: nearstars-interstellar
     ├─ docs/nearstars/        ← this spec (impl-spec.md + research/)
     └─ (all C++ changes land on this same branch, next to the code they describe)

Vannadin/nearstars-db            the NearStars mod repo — keeps a COPY of these docs as a
                                 design/decision record only. No code. Not needed to build.
schultz-dev0/principia-docs      Schultz's doc hub — PR #2 shares this spec with him (FYI/collab).
```

한 문장으로. **작업은 `Vannadin/Principia` @ `nearstars-interstellar`에서 이뤄진다.
나머지 세 저장소는 각각 포크의 뿌리, 기록용 사본, 그리고 슐츠에게 보내는 공유본이다.**

## 구현을 어디서 돌리나 (fable)

스펙은 opus 리서치 에이전트들이 작성했고, 구현은 **별도 Claude Code 세션의 fable**이
이 포크의 클론에서 직접 몰고 가는 것을 전제로 한다. 구체적으로.

1. **포크를 오래 살아남을 위치에 클론한다**(임시/scratch 디렉토리 금지 — 세션이
   바뀌어도 남아 있어야 한다). 예를 들어.
   ```
   git clone https://github.com/Vannadin/Principia ~/Desktop/Principia-nearstars
   cd ~/Desktop/Principia-nearstars
   git checkout nearstars-interstellar
   ```
2. **그 디렉토리에서 Claude Code를 시작**하고, 모델을 **fable**로 설정한 뒤
   (`/model fable`), 이 스펙을 가리킨다.
   > "Implement WS1 commit 1 from `docs/nearstars/impl-spec.md`. Read
   > `impl-spec.md §2–4` and `research/R1-fp-precision.md` first."
3. fable이 이 브랜치에서 C++를 편집·커밋하고 `Vannadin/Principia`로 다시 push한다.
   브랜치가 공유 상태이므로 각 세션은 이전 세션이 멈춘 지점부터 이어받는다.

참고.
- `research/R*.md`의 file:line 인용은 upstream master `440310a9` 기준이다. 브랜치가
  더 최신 master 위로 rebase됐다면 심볼 이름으로 다시 앵커하라(함수는 안정적이고,
  줄 번호는 밀린다).
- **빌드 게이트.** Principia의 빌드는 독자적이고 무겁다(MSVC/clang). 먼저 headless
  C++ 테스트를 검증하라 — WS1 commit 1(`interstellar_precision_test`)은 KSP 설치가
  필요 없다. KSP를 건드리는 커밋들(WS3, 그리고 WS1의 플러그인 배선)은 풀 빌드 + KSP가
  필요하며, 이게 느린 부분이다.

## 읽는 순서

1. `impl-spec.md` — 마스터. 세 workstream, 빌드 순서, 두 핵심 결정.
2. `research/R1-fp-precision.md` — WS1(장거리 FP 정밀도).
3. `research/R2-soi-code-map.md` + `research/R3-soi-numerics.md` — WS2(SOI cutoff).
4. `research/R4-thrust-under-warp.md` — WS3(timewarp 중 추력).
5. `design-draft.md` — 초기 서술본(SOI 문제에서는 R3가 대체함).
