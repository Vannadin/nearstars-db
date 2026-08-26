# 암석 로스터의 증거 등급 규칙을 고정한다 — 추정 반지름에 역산이 걸리면 여기서 잡힌다
"""Pin the rocky roster's evidence grading.

    python3 engine/test_rocky_roster.py
    python3 engine/rocky_roster.py --md      문서용 표

이 표의 값어치는 숫자가 아니라 **분류** 다. 셋을 한 칸에 섞으면 "17개 중 16개가
풀렸다" 는 문장이 나오는데, 사실이면서 오도한다 — 그 16개 중 여덟은 측정되지 않은
반지름에 역산을 건 것이라 남의 관계식을 되읽은 값이다.

그래서 이 파일이 지키는 것은 등급 규칙이지 C/MR² 값이 아니다.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rocky_roster as rr  # noqa: E402

# 로스터에 반드시 있어야 하는 천체와 그 등급. DB 가 바뀌어 조용히 빠지면 잡는다.
EXPECTED = {
    "TRAPPIST-1 b": rr.MEASURED, "TRAPPIST-1 c": rr.MEASURED,
    "TRAPPIST-1 d": rr.MEASURED, "TRAPPIST-1 e": rr.MEASURED,
    "TRAPPIST-1 f": rr.MEASURED, "TRAPPIST-1 g": rr.MEASURED,
    "TRAPPIST-1 h": rr.MEASURED,
    "Barnard b": rr.ESTIMATED, "Barnard c": rr.ESTIMATED,
    "Barnard d": rr.ESTIMATED, "Barnard e": rr.ESTIMATED,
    "Proxima Cen b": rr.ESTIMATED, "Proxima Cen d": rr.ESTIMATED,
    "40 Eridani A c": rr.ESTIMATED, "40 Eridani A d": rr.ESTIMATED,
    "40 Eridani A b": rr.MASS_ONLY, "Proxima Cen c": rr.MASS_ONLY,
}


def main() -> int:
    fails: list[str] = []
    data = {r["name"]: r for r in rr.rows()}

    print("증거 등급 — 오차의 유무가 판정하는가")
    for name, want in EXPECTED.items():
        row = data.get(name)
        if row is None:
            fails.append(f"{name}: 로스터에서 사라졌다")
            continue
        if row["grade"] != want:
            fails.append(f"{name}: 등급 {row['grade']}, 기대 {want}")
    ok = not fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {len(EXPECTED)}개가 기대한 등급에 있다 "
          f"(측정 7 · 추정 8 · 질량만 2)")
    for f in fails:
        print(f"         {f}")

    # 검출 방식 문자열은 DB 안에서 표기가 갈린다. 판정은 오차 쪽에 걸려 있어야 한다.
    print("\n판정 근거 — 검출 방식 문자열이 아니라 오차 필드인가")
    cases = (
        ("오차 있는 반지름 → 측정", {"radius_rearth": 1.0, "radius_err_rearth": 0.01},
         rr.MEASURED),
        ("오차 없는 반지름 → 추정", {"radius_rearth": 1.0, "radius_err_rearth": None},
         rr.ESTIMATED),
        ("반지름 없음 → 질량만", {"radius_rearth": None, "radius_err_rearth": None},
         rr.MASS_ONLY),
    )
    for label, raw, want in cases:
        got = rr.grade(raw)
        good = got == want
        if not good:
            fails.append(f"등급 규칙: {label} — {got}")
        print(f"  [{'PASS' if good else 'FAIL'}] {label}")

    # 이 파일이 존재하는 이유. 추정 반지름에 역산이 걸리면 도출값처럼 보이는 순환값이
    # 표에 실린다. 규칙이 아니라 **결과** 를 확인한다.
    print("\n순환 방지 — 추정 반지름에는 역산을 걸지 않는가")
    leaked = [r["name"] for r in rr.rows()
              if r["grade"] == rr.ESTIMATED and rr.evaluate(r)[0] is not None]
    if leaked:
        fails.append(f"순환: 추정 반지름에 역산이 걸렸다 — {', '.join(leaked)}")
    print(f"  [{'PASS' if not leaked else 'FAIL'}] 추정 등급 8개 전부 보류로 나온다")

    # 그리고 측정 등급은 실제로 역산돼야 한다. 위 검사만 있으면 전부 보류시켜도 통과한다.
    #
    # 기본값은 **대표 하나** 다. 역산 한 번이 축을 훑고 이분법까지 돌아 6~7초씩 걸리고,
    # 일곱을 다 돌리면 이 파일 하나가 게이트 전체(1분 55초)를 40 % 늘린다. 같은 코드
    # 경로를 위성 로스터가 이미 게이트에서 여섯 번 돌리므로, 여기서 지켜야 하는 것은
    # 적분의 정확도가 아니라 **측정 등급이 역산으로 흘러간다는 배선** 이다. 하나면 는다.
    # 일곱 전부는 `--full`, 그리고 표를 낼 때(`rocky_roster.py`)마다 실제로 돈다.
    full = "--full" in sys.argv
    targets = [r for r in rr.rows() if r["grade"] == rr.MEASURED]
    if not full:
        targets = targets[:1]
    inverted = [r for r in targets
                if (rr.evaluate(r)[0] is not None) and rr.evaluate(r)[0].applicable]
    good = len(inverted) == len(targets)
    if not good:
        fails.append(f"측정 등급 {len(inverted)}/{len(targets)} 만 역산됐다")
    scope = f"{len(targets)}개" + ("" if full else " (대표 1개 — 전수는 --full)")
    print(f"  [{'PASS' if good else 'FAIL'}] 측정 등급이 실제로 역산된다 — {scope}")

    print("\nMsini — 하한이라는 사실이 출력에 남는가")
    pc = next((r for r in rr.rows() if r["name"] == "Proxima Cen c"), None)
    said = pc is not None and "Msini" in rr._outcome(pc)[1]
    if not said:
        fails.append("Msini: 순방향 결과가 하한이라는 것을 말하지 않는다")
    print(f"  [{'PASS' if said else 'FAIL'}] Proxima Cen c 가 Msini 임을 적는다")

    # 거절 훑기도 역산을 깨우면 안 된다. 위에서 이미 계산된 것(캐시)과 순방향으로
    # 끝나는 것만 본다 — 측정 등급의 전수 거절 확인은 --full 이 켜졌을 때 딸려 온다.
    print("\n남은 거절 — 암석 쪽에 실제로 막힌 것은 무엇인가")
    declined = []
    for r in rr.rows():
        if r["grade"] == rr.MEASURED and r["name"] not in rr._CACHE:
            continue
        res, _ = rr.evaluate(r)
        if res is not None and not res.applicable:
            declined.append((r["name"], res.reason))
    for name, why in declined:
        print(f"  [거절] {name} — {why[:110]}")
    # 지금 하나다. 늘거나 줄면 그 자체가 소식이므로 표에 드러나야 한다.
    seen = sum(1 for r in rr.rows() if r["name"] in rr._CACHE)
    print(f"         거절 {len(declined)}건 (평가한 {seen}개 중)")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
