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

    print(f"미선택 기본값이 나가고 있는 자리 — 밴드 {total}건 중 {len(shipping)}건")
    for mod_name, path, band in shipping:
        mid = band.middle()
        mid_s = f"{mid:.4g}" if mid is not None else "—"
        print(f"  {mod_name}.{path}")
        print(f"      {band.low}–{band.high} → {mid_s} ({band.mean}) · {band.width_source[:78]}")

    if whole:
        print(f"\n중간값을 채우지 않는 자리 {len(whole)}건 — 짝짓기가 인쇄 안 된 묶음의 구성원이다.")
        print("각자 중간을 채우면 corners() 가 거절하는 그 조합을 그대로 다시 만든다. 사례를 통째로 고른다.")
        for mod_name, path, band in whole:
            print(f"  {mod_name}.{path}  ({band.bundle}, {band.low}–{band.high})")
    if not shipping and not whole:
        print("  없음 — 모든 밴드가 고른 점을 가지고 있다.")
    else:
        print("\n각 줄은 오너가 아직 고르지 않은 한 자리다. 고르면 그 줄이 사라지고 Collapse 가 남는다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
