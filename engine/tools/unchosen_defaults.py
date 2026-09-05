# 아직 아무도 고르지 않아 엔진이 중간값을 채워 내보내는 자리를 센다 (C32 Z-4)
"""Where is the engine still shipping a number nobody chose?

    python3 engine/tools/unchosen_defaults.py

A default is a way of **leaving a seat empty**, not of filling it. That only works if the empty seats
can be counted, so this walks the modules that hold bands and lists every one whose point is still
`unchosen` — the same shape as the C33 unmigrated-citation count, and read the same way: the number
is a to-do list for the owner, not a failure.

A band listed here is emitting its middle right now, labelled `unchosen`. When someone picks a point,
that line leaves this list and a `Collapse` records which end it came from and why.

Exit code is always 0. This counts; it does not judge.
"""
from __future__ import annotations

import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE))

from bands import Band  # noqa: E402

# 밴드를 들고 있는 모듈들. 새 밴드를 만들면 여기 한 줄 — 자동 스캔은 등록 실패를 조용히 지나간다.
SOURCES = ("albedo_table", "greenhouse_cases", "tidal_heating")


def _bands(obj, path: str, seen: set[int]) -> list[tuple[str, Band]]:
    if id(obj) in seen:
        return []
    seen.add(id(obj))
    if isinstance(obj, Band):
        return [(path, obj)]
    if isinstance(obj, dict):
        return [b for k, v in obj.items() for b in _bands(v, f"{path}[{k!r}]", seen)]
    return []


def main() -> int:
    rows: list[tuple[str, str, Band]] = []
    total = 0
    for mod_name in SOURCES:
        mod = __import__(mod_name)
        for attr in sorted(dir(mod)):
            if attr.startswith("_"):
                continue
            for path, band in _bands(getattr(mod, attr), attr, set()):
                total += 1
                if not band.chosen:
                    rows.append((mod_name, path, band))

    shipping = [r for r in rows if r[2].pairing != "unknown"]
    whole = [r for r in rows if r[2].pairing == "unknown"]

    # 같은 양을 추정하는 밴드들은 **한 자리의 여러 옵션**이다. 따로 세면 오너는 같은 양을
    # 두 번 고르는 것처럼 보게 된다 — `estimates` 가 그 구별을 들고 있다.
    alternatives: dict[str, list] = {}
    seats: list = []
    for row in shipping:
        key = row[2].estimates
        (alternatives.setdefault(key, []) if key else seats).append(row)

    n_seats = len(seats) + len(alternatives)
    print(f"미선택 자리 {n_seats}개 — 밴드 {total}건 중 고른 점이 없는 것 {len(shipping)}건")

    def _line(mod_name, path, band, indent="  "):
        mid = band.middle()
        mid_s = f"{mid:.4g}" if mid is not None else "—"
        print(f"{indent}{mod_name}.{path}")
        print(f"{indent}    {band.low}–{band.high} → {mid_s} ({band.mean}) · {band.width_source[:74]}")

    for quantity, opts in alternatives.items():
        print(f"\n  자리 «{quantity}» — 옵션 {len(opts)}개 중 **하나**를 고르는 자리다.")
        print("  같은 양의 서로 다른 추정이라 여러 개를 고르는 게 아니다.")
        for row in opts:
            _line(*row, indent="    ")
    for row in seats:
        _line(*row)

    if whole:
        print(f"\n중간값을 채우지 않는 자리 {len(whole)}건 — 짝짓기가 인쇄 안 된 묶음의 구성원이다.")
        print("각자 중간을 채우면 corners() 가 거절하는 그 조합을 그대로 다시 만든다. 사례를 통째로 고른다.")
        for mod_name, path, band in whole:
            print(f"  {mod_name}.{path}  ({band.bundle}, {band.low}–{band.high})")
    if not shipping and not whole:
        print("  없음 — 모든 밴드가 고른 점을 가지고 있다.")
    else:
        print("\n자리 하나를 고르면 그 자리 전체가 목록에서 사라지고 Collapse 하나가 남는다 — 옵션마다가")
        print("아니라 자리마다다. 위의 «…» 묶음은 옵션 목록이지 결정 목록이 아니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
