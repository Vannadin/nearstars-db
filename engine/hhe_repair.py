# 수소-헬륨 표의 눌린 grad_ad 노드를 조립값으로 수리하는 옵트인 계측 모듈 (브리프 31, 기본 비활성)
"""OPT-IN clamped-node repair for the baked H/He grad_ad table.

**Not imported by the engine.** Importing this module arms the repair (it rebinds
`hhe_table.GRAD_AD` in place); nothing in the default path imports it, so every answer
the engine gives without it is bit-identical to the clamped table. The owner decides
which table is the default; until then this is a measurement instrument
(`clamp-fallback-checklist.md` records the decision context). Measurement runners that
arm it should also consult `clamp_bad_stencil()` before trusting a grad_ad read — the
engine's own refusal machinery does not know about the 6 unrepairable cells unless the
consumer asks.

The distributed table carries clamp ends (exactly 0.1 or 0.5) where its own grad_ad
calculation failed — there is no published number at those nodes to preserve, so the
table-first rule does not apply there. At import this module rebinds
`hhe_table.GRAD_AD` with those nodes replaced by the assembly **from quantities the
same table publishes**:

    grad_ad = −(∂lnρ/∂lnT)_P · P / (T · ρ · c_p)

with the log-derivative from the density table's finite difference (`dlrho`) and c_p
from the C_P table — no grad_ad circularity. The interpolation structure is untouched
(node-level repair; `clamp-fallback-checklist.md` records why).

Cells where the assembly itself cannot stand — the density table has
(∂lnρ/∂lnT)_P ≥ 0 there, which is unphysical for this fluid — are NOT repaired:
their coordinates stay in `CLAMP_UNREPAIRED`, and `clamp_bad_stencil()` lets the
consumer (eos.HydrogenHelium) refuse by name when an interpolation stencil touches
them. Measured at registration: 66 of 72 clamped nodes assemble; the 6 that do not
sit at 63–89 GPa × 1585 K and 100–112 GPa × 1778 K.

**The assembled value is not truth either** — it is the surviving grounded route, not
the authors' unpublished calculation; the repair measures how far two grounded routes
diverge, nothing more. The baked file itself stays generated-pristine; this module is
the only place the repair lives.
"""
from __future__ import annotations

import math

import hhe_table as _H

CLAMP_ENDS = (0.1, 0.5)


def _assemble(i: int, j: int) -> float | None:
    lt = _H.LOGT_LO + i * _H.STEP
    lp = _H.LOGP_LO + j * _H.STEP
    p = 10.0 ** lp * 1e9
    t = 10.0 ** lt
    dlt, _dlp = _H.dlrho(p, t)
    cp = _H.heat_capacity_p(p, t)
    if dlt >= 0.0 or cp <= 0.0:
        return None
    return -dlt * p / (t * _H.density(p, t) * cp)


CLAMP_REPAIRED: dict[tuple[int, int], float] = {}
CLAMP_UNREPAIRED: set[tuple[int, int]] = set()

_rows = [list(r) for r in _H.GRAD_AD]
for _i in range(_H.NT):
    for _j in range(_H.KEEP[_i]):
        if _rows[_i][_j] in CLAMP_ENDS:
            _g = _assemble(_i, _j)
            if _g is None:
                CLAMP_UNREPAIRED.add((_i, _j))
            else:
                CLAMP_REPAIRED[(_i, _j)] = _g
                _rows[_i][_j] = _g
_H.GRAD_AD = tuple(tuple(r) for r in _rows)
del _rows


def clamp_bad_stencil(p_pa: float, t_k: float) -> bool:
    """grad_ad 의 쌍삼차 스텐실이 수리 불가 클램프 칸을 포함하는가 (_bicubic 의 클램프
    규칙을 그대로 재현 — eos 의 거절 판정용)."""
    if not CLAMP_UNREPAIRED:
        return False
    lt = math.log10(t_k)
    lp = math.log10(p_pa / 1e9)
    x = (lt - _H.LOGT_LO) / _H.STEP
    y = (lp - _H.LOGP_LO) / _H.STEP
    i = min(max(int(x), 0), _H.NT - 2)
    j = min(max(int(y), 0), _H.NP - 2)
    for k in (i - 1, i, i + 1, i + 2):
        kk = 0 if k < 0 else (_H.NT - 1 if k > _H.NT - 1 else k)
        n = _H.KEEP[kk]
        jj = j if j <= n - 1 else n - 1
        m = n - 1
        for c in (jj - 1 if jj >= 1 else 0, jj,
                  jj + 1 if jj + 1 <= m else m, jj + 2 if jj + 2 <= m else m):
            if (kk, c) in CLAMP_UNREPAIRED:
                return True
    return False
