# 알베도 표 자기검증 — 여덟 행이 문서와 같은가 · 아무 행에도 점이 없는가 · 두 축이 실제로 어긋나는가
"""Hold the albedo table to the document it transcribes.

    python3 engine/test_albedo_table.py

Three claims, each machine-checked against `docs/reference/surface-color-albedo-methodology.md`
itself rather than against a second copy of the numbers:

1. **Every row's ends are the document's ends.** The table is parsed out of the Markdown, so a doc
   edit that moves a range fails here instead of silently disagreeing with the engine.
2. **No row carries a chosen point.** The document prints eight intervals and no midpoints. A row
   still emits — the game needs a number — but the filled middle goes out labelled `unchosen`, with
   its ends and their source beside it, so it can never be mistaken later for a reviewed decision.
3. **The two consequence axes really do disagree.** The row whose ends move `T_eq` most is not the
   row whose ends move visual brightness most — so any single "how wide is this" number would be
   reporting one axis and hiding the other.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from albedo_table import BOND_ALBEDO, PHASE_INTEGRAL, contrast_ratio, t_eq_ratio  # noqa: E402

DOC = Path(__file__).resolve().parents[1] / "docs" / "reference" / "surface-color-albedo-methodology.md"
ROW = re.compile(r"^\|\s*(.+?)\s*\|\s*~([0-9.]+)–([0-9.]+)\s*\|", re.M)


def main() -> int:
    fails: list[str] = []

    # 1. the document's own eight rows
    printed = {(float(lo), float(hi)) for _n, lo, hi in ROW.findall(DOC.read_text(encoding="utf-8"))}
    ours = {(b.low, b.high) for b in BOND_ALBEDO.values()}
    if len(BOND_ALBEDO) != 8:
        fails.append(f"1: the document prints eight surface types, the table holds {len(BOND_ALBEDO)}")
    missing = ours - printed
    if missing:
        fails.append(f"1: ranges not printed anywhere in the document: {sorted(missing)}")

    # 2. nobody has picked a point in any of them
    for name, band in BOND_ALBEDO.items():
        if band.chosen:
            fails.append(f"2: {name} carries a working point the document does not print")
        if band.kind != "interval":
            fails.append(f"2: {name} should be an interval, got {band.kind}")
        if band.bundle is not None:
            fails.append(f"2: {name} is an analog reading of A itself, not a factor of one — "
                         "the q·p bundle is the other path")
    # a row still emits — the game needs a number — but it goes out labelled unchosen, with its ends
    # and their source beside it, so nobody later reads the filled middle as a reviewed decision
    row = BOND_ALBEDO["volatile-ice plains (N₂/CH₄/CO₂)"]
    out = row.emit("albedo")
    if abs(out["albedo"] - 0.675) > 1e-12 or not out["albedo_pick"].startswith("unchosen"):
        fails.append(f"2: a row must emit its middle labelled unchosen, got {out}")
    if not {"albedo_min", "albedo_max", "albedo_width_source"} <= set(out):
        fails.append("2: the filled point must carry the ends and where they are printed")

    # 2b. all ten bands estimate the same quantity by two routes — one seat, not ten
    every = list(BOND_ALBEDO.values()) + list(PHASE_INTEGRAL.values())
    if {b.estimates for b in every} != {"A_Bond"}:
        fails.append("2b: every row and every q family is one estimate of A_Bond; a band that does "
                     "not say so gets counted as a separate decision the owner has to make")

    # 3. the axes disagree about which row matters most
    hottest = max(BOND_ALBEDO, key=lambda n: t_eq_ratio(BOND_ALBEDO[n]))
    starkest = max(BOND_ALBEDO, key=lambda n: contrast_ratio(BOND_ALBEDO[n]))
    if hottest == starkest:
        fails.append("3: the two axes agree here, so the asymmetry this table exists to show is gone")
    if not t_eq_ratio(BOND_ALBEDO[starkest]) < 1.02:
        fails.append(f"3: {starkest} is the widest in brightness and should barely move T_eq, "
                     f"got {t_eq_ratio(BOND_ALBEDO[starkest]):.3f}×")

    # the document prints q for two surface families only — the rest have none, and none was invented
    if len(PHASE_INTEGRAL) != 2:
        fails.append(f"q: the document prints two families, the table holds {len(PHASE_INTEGRAL)}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print(f"  [PASS] 알베도 표 — 여덟 행 전부 문서의 구간과 일치 · 고른 점 없음(미선택 라벨로 emit) · "
          f"두 축 어긋남(T_eq 최대 {hottest}, 대비 최대 {starkest}) · q 는 두 계열만 · 열 밴드 전부 A_Bond 한 자리")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
