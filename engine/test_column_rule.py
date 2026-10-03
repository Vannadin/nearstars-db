# 맨틀 조성 표의 열이 수렴한 이웃을 따르는가 — 규칙 갈래 · 1 bar 와즐리아이트 막이 · 이름 대고 굳힘 · 고상선 위는 빈 칸 (C160)
"""prereg-c160-column-follows-neighbour (frozen 7adc71fd, with post-freeze note 1): N-rule, N-guard, N-none, N-edge.

    python3 engine/test_column_rule.py        (BurnMan: the gate venv)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mantle_composition as mc   # noqa: E402

fails: list[str] = []
MARS_KHAN2022 = {"SiO2": 46.66, "Al2O3": 3.49, "MgO": 32.81, "CaO": 2.66, "FeO": 13.68, "Na2O": 0.69}


def ok(cond: bool, label: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        fails.append(label)


def n_rule() -> None:
    prev = "plg+ol+opx+cpx"
    ok(mc._neighbour(prev, ["plg+ol+opx", "ol+cpx+gt", "ol+opx"]) == ("plg+ol+opx", "subset"),
       "N-rule ②: the largest converged proper subset of the previous winner (a phase exits)")
    got, why = mc._neighbour("ri+gt", ["wa+gt", "ri+gt+capv", "ol+cpx+gt"])
    ok(why == "neighbour" and sorted(got) == ["ri+gt+capv", "wa+gt"],
       "N-rule ③: no subset → the one-phase-different neighbours (one swapped, one added); far sets excluded")
    ok(mc._neighbour("ri+gt+capv", ["ri+gt", "wa+gt+capv"])[1] == "subset",
       "N-rule ②>③: a subset wins over a one-phase swap")
    ok(mc._neighbour(prev, ["wa+gt", "ri+gt", "wa+cpx+gt"]) == (None, "frozen"),
       "N-rule ④: nothing near the previous winner → a named freeze")


def n_guard() -> None:
    """덧붙임 5 의 경우 — 화성 조성, 1 bar, 400–1000 K 아래로 훑기: 와즐리아이트 든 집합은 이기지 못한다."""
    bulk = mc.atomic_bulk(MARS_KHAN2022)
    ts = [400.0 + 50.0 * k for k in range(13)]          # 400 … 1000 K, T_SEED 가 끝점
    col = mc._column((bulk, 1e5, ts))
    names = [(c or {}).get("assemblage") for c in col]
    wa = [(t, n) for t, n in zip(ts, names) if n and "wa" in n.split("*")[0].split("+")]
    ok(not wa, f"N-guard: no wadsleyite-bearing winner at 1 bar, 400–1000 K — {wa or names[:3]}")


def n_none() -> None:
    """아무 후보도 수렴하지 않는 점은 오늘처럼 이름 대고 굳는다 — 700 K 밑에서 `select_all` 이 빈 답."""
    bulk = mc.atomic_bulk(MARS_KHAN2022)
    real = mc.select_all
    mc.select_all = lambda b, p, t, warm=None: {} if t < 700.0 else real(b, p, t, warm)
    try:
        ts = [500.0 + 50.0 * k for k in range(11)]       # 500 … 1000 K
        col = mc._column((bulk, 3e9, ts))
    finally:
        mc.select_all = real
    below = [(c or {}).get("rule") for t, c in zip(ts, col) if t < 700.0]
    names = [(c or {}).get("assemblage") or "" for t, c in zip(ts, col) if t < 700.0]
    ok(below and all(r == "frozen" for r in below) and all(n.endswith("*frozen") for n in names),
       f"N-none: points where nothing converges freeze by name ({len(below)} points, rule {set(below)})")


def n_edge() -> None:
    """덧붙임 1 — 고상선 위 칸은 이름 댄 빈 칸, 그 밑 칸은 채워진다(화성 조성, 10 GPa, 1000–2600 K)."""
    bulk = mc.atomic_bulk(MARS_KHAN2022)
    p = 10e9
    t_sol = mc.solidus_edge(p)
    ts = [1000.0 + 50.0 * k for k in range(33)]          # 1000 … 2600 K
    col = mc._column((bulk, p, ts))
    above = [(t, (c or {}).get("assemblage")) for t, c in zip(ts, col) if t > t_sol and c is not None]
    below_last = max(t for t in ts if t <= t_sol)
    sub = col[ts.index(below_last)]
    ok(not above, f"N-edge: no filled cell above the solidus {t_sol:.0f} K at 10 GPa — {above[:3]}")
    ok(sub is not None and not sub["assemblage"].endswith("*frozen"),
       f"N-edge: the last sub-solidus cell ({below_last:.0f} K) still fills — {(sub or {}).get('assemblage')}")


if __name__ == "__main__":
    n_rule()
    n_guard()
    n_none()
    n_edge()
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    sys.exit(1 if fails else 0)
