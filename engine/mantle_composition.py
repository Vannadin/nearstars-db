# 맨틀 조성 선언(산화물)을 읽고 상부 맨틀 창의 광물 집합 표(밀도 · αK · c_V · γ)를 짓고 읽는 모듈 (C74-2)
"""Mantle composition declaration → upper-mantle assemblage (prereg-c74-2-mantle-composition, frozen `2571123c`,
implementation choices in its addendum 3).

`burnman.equilibrate` minimises Gibbs energy inside a *given* phase list and does not choose phases, so the table
builder tries a fixed list of candidate assemblages at every (P, T) node and keeps the converged one with the lowest
Gibbs energy per atom. The engine never calls BurnMan: it reads the JSON table named by the composition's fingerprint
(`mantle_tables/<key>.json`, the body name is inside)
and interpolates bilinearly in (ln P, T). Only building the table and the A′ plumbing check need BurnMan.

    engine/.venv-gate/bin/python3 engine/mantle_composition.py --build earth   # or mars

Scope (frozen decisions): Earth = Workman & Hart 2005 Bulk DMM, Mars = Khan+ 2022 Table 1 (grade analog — model mix),
used for the **thermal term and the density** of the upper-mantle phases only (surface to `eos.SILICATE_EN_TO_PREM`);
the lower mantle stays on its own phases. A body without the field keeps pure-MgSiO₃ (bit-identical).
"""
from __future__ import annotations

import bisect
import hashlib
import json
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLE_DIR = Path(os.environ["MANTLE_TABLE_DIR"]) if os.environ.get("MANTLE_TABLE_DIR") else HERE / "mantle_tables"

#: 선언 칸이 받는 산화물 — 원문 표의 칸 이름(W&H 2005 Table 3 · Khan+ 2022 Table 1 · Y&M 2020 Table 3 의 합집합).
OXIDES = ("SiO2", "TiO2", "Al2O3", "Cr2O3", "FeO", "MnO", "MgO", "NiO", "CaO", "Na2O", "K2O", "P2O5")
#: 합 허용 — 원문 표 합이 100 ± 이 안(정규화 전 표 · 미량 산화물 빠진 표를 받기 위한 폭; 결정은 구현 판에서 고정).
SUM_TOLERANCE_WT = 2.0
#: 광물 집합을 계산하는 BurnMan 체계의 산화물 — Khan+ 2022 의 CFMASNa(CaO-FeO-MgO-Al₂O₃-SiO₂-Na₂O).
CFMASNA = ("CaO", "FeO", "MgO", "Al2O3", "SiO2", "Na2O")


def read_mantle_composition(decl) -> tuple[dict[str, float] | None, str | None]:
    """`mantle_composition` 선언을 `(산화물 wt% 사전, 거절 문장)` 으로. 없으면 `(None, None)`.

    세 칸(grade · source · counter_evidence_searched)은 `payload.check_provenance` 가 본다 — 여기는 값만."""
    if decl is None:
        return None, None
    value = decl.get("value") if isinstance(decl, dict) else None
    if not isinstance(value, dict):
        return None, "`mantle_composition.value` 는 산화물 → wt% 사전이어야 한다"
    bad = sorted(k for k in value if k not in OXIDES)
    if bad:
        return None, f"`mantle_composition` 의 산화물 {bad} 는 어휘 밖 — {' · '.join(OXIDES)}"
    wt = {}
    for k, v in value.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0.0:
            return None, f"`mantle_composition.{k}` {v!r} 는 0 이상의 수가 아니다"
        wt[k] = float(v)
    total = math.fsum(wt.values())       # C143 — 올바르게 반올림된 합: 파이썬 판과 무관한 마지막 비트
    if abs(total - 100.0) > SUM_TOLERANCE_WT:
        return None, f"`mantle_composition` 합 {total:.2f} wt% 가 100 ± {SUM_TOLERANCE_WT:g} 밖"
    missing = [k for k in CFMASNA if k not in wt]
    if missing:
        return None, f"`mantle_composition` 에 CFMASNa 산화물 {missing} 가 없다 — 집합을 계산할 수 없다"
    return wt, None


def cfmasna(wt: dict[str, float]) -> dict[str, float]:
    """CFMASNa 여섯으로 줄여 100 으로 정규화 — Khan+ 2022 Table 1 이 쓴 체계(«normalised to 100%»)."""
    sub = {k: wt[k] for k in CFMASNA}
    s = math.fsum(sub.values())          # C143 — 이 값이 표의 지문(`header_key`)으로 들어간다: 판과 무관해야 한다
    return {k: v * 100.0 / s for k, v in sub.items()}


# ── 표 짓기의 고정 선택 (덧붙임 3 ① ②) ──────────────────────────────────────
#: 후보 집합 — SLB 2022 이름의 줄임. ⚠ **목록 밖 상은 못 고른다** (grade judgment, 덧붙임 3 ①).
CANDIDATES = (("plg", "ol", "opx", "cpx"), ("sp", "ol", "opx", "cpx"), ("ol", "opx", "cpx", "gt"), ("ol", "cpx", "gt"),
              ("ol", "c2c", "cpx", "gt"), ("wa", "cpx", "gt"), ("wa", "gt"), ("wa", "ri", "gt"), ("ri", "gt"),
              ("ri", "cpx", "gt"), ("ri", "gt", "capv"), ("ol", "wa", "gt"), ("ol", "wa", "cpx", "gt"))
SLB_NAMES = {"plg": "plagioclase", "sp": "mg_fe_aluminous_spinel", "ol": "olivine", "opx": "orthopyroxene",
             "cpx": "clinopyroxene", "gt": "garnet", "c2c": "c2c_pyroxene", "wa": "wadsleyite", "ri": "ringwoodite",
             "capv": "ca_perovskite"}
#: 몰분율 음수 허용 — 이보다 작으면 그 집합은 이 조성에 없는 것(수렴해도 버린다).
NEG_TOL = -1e-9
P_FLOOR = 1e5                      # Pa. 격자 첫 점 — 이 밑은 이 점의 값(1 bar 차)
P_RATIO = 1.05                     # 등비 5 %
P_TOP = 25e9                       # Pa. 23.83 GPa(상부 창 끝) 위로 한 칸 남짓 — 끝 포함
T_LO, T_HI, T_STEP = 200.0, 4800.0, 50.0     # T_HI: 덧붙임 4 (범위 잡기 최고 4353.3 K × 1.1)
FIELDS = ("rho", "alpha_k", "c_v", "gamma")


def grid_p() -> list[float]:
    ps, p = [], P_FLOOR
    while p < P_TOP * (1.0 - 1e-12):
        ps.append(p)
        p *= P_RATIO
    ps.append(P_TOP)
    return ps


def grid_t() -> list[float]:
    n = int(round((T_HI - T_LO) / T_STEP))
    return [T_LO + i * T_STEP for i in range(n + 1)]


def atomic_bulk(wt: dict[str, float]) -> dict[str, float]:
    """CFMASNa wt% → 원소 몰(합 1). 원자 질량은 BurnMan 내장(`Composition`) — 표 머리에 판을 적는다."""
    from burnman import Composition
    c = Composition(cfmasna(wt), "weight")
    c.renormalize("atomic", "total", 1.0)
    return {k: float(v) for k, v in c.atomic_composition.items()}


def _phase(key: str, x=None):
    from burnman import minerals
    s = getattr(minerals.SLB_2022, SLB_NAMES[key])()
    if hasattr(s, "endmembers"):
        n = len(s.endmembers)
        s.set_composition(list(x) if x is not None else [0.8] + [0.2 / (n - 1)] * (n - 1))
    return s


def _props(rock, key: str) -> dict:
    return {"rho": float(rock.density), "alpha_k": float(rock.alpha * rock.isothermal_bulk_modulus_reuss),
            "c_v": float(rock.molar_heat_capacity_v / rock.molar_mass), "gamma": float(rock.grueneisen_parameter),
            "assemblage": key}


def _rock(cand, start):
    from burnman import Composite
    if start is None:
        phs = [_phase(k) for k in cand]
        return Composite(phs, [1.0 / len(phs)] * len(phs))
    return Composite([_phase(k, x) for k, x in zip(cand, start[0])], list(start[1]))


def _state(rock) -> tuple:
    return ([list(ph.molar_fractions) if hasattr(ph, "endmembers") else None for ph in rock.phases],
            [max(f, 1e-6) for f in rock.molar_fractions])


#: 수렴하지 않은 후보에서 몰분율이 0 에 닿은 상을 빼고 다시 푸는 횟수 (덧붙임 7).
DROP_PHASES = 2
DROP_TOL = 1e-6


def _solve(bulk, cand, start, p_pa, t_k):
    """한 집합을 한 출발점에서 평형 — `(수렴?, rock)`. 예외는 (False, None)."""
    import warnings
    from burnman import equilibrate
    rock = _rock(cand, start)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sol, _ = equilibrate(bulk, rock, [["P", float(p_pa)], ["T", float(t_k)]])
    except Exception:
        return False, None
    return bool(sol.success) and min(rock.molar_fractions) >= NEG_TOL, rock


def select(bulk: dict[str, float], p_pa: float, t_k: float, warm: dict | None = None):
    """`select_all` 의 깁스 최소 — `(고른 칸 | None, 수렴한 후보 이름들, 고른 것의 상태)`. 예전 모양 그대로."""
    res = select_all(bulk, p_pa, t_k, warm)
    if not res:
        return None, [], None
    _g, props, st = min(res.values(), key=lambda r: r[0])
    return props, list(res), st


def select_all(bulk: dict[str, float], p_pa: float, t_k: float, warm: dict | None = None) -> dict:
    """(P, T) 에서 후보 집합을 전부 평형시켜 원자당 깁스 최소를 고른다 (덧붙임 3 ①).

    돌려주는 것은 수렴한 후보 전부 `{이름: (원자당 깁스, 칸, 상태)}` — 수렴한 차례대로(C160 이 이웃을 고르려고 쓴다).
    `warm` 은 집합 이름마다 앞 격자점에서
    수렴한 (상 조성들, 상 분율) — 기본 출발점에서 먼저 풀고, 안 되면 그 따뜻한 출발점으로 한 번 더(덧붙임 5).
    ⚠ 둘 다 안 되면 멈춘 자리에서 몰분율 ≤ `DROP_TOL` 인 상을 빼고 남은 상으로 다시(덧붙임 7, `DROP_PHASES` 번까지) —
    참 집합이 후보의 부분집합일 때 경계에서 멈춘 풀이를 버리던 것을 막는다."""
    res: dict = {}
    for cand0 in CANDIDATES:
        queue = [(tuple(cand0), 0)]
        while queue:
            cand, depth = queue.pop(0)
            key = "+".join(cand)
            starts = [None] + ([warm[key]] if warm and warm.get(key) else [])
            stuck = None
            for start in starts:
                good, rock = _solve(bulk, cand, start, p_pa, t_k)
                if good:
                    st = _state(rock)
                    if warm is not None:
                        warm[key] = st
                    if key not in res:
                        res[key] = (rock.molar_gibbs / sum(rock.formula.values()), _props(rock, key), st)
                    stuck = None
                    break
                if rock is not None:
                    stuck = rock
            else:
                if stuck is not None and depth < DROP_PHASES:
                    keep = tuple(k for k, f in zip(cand, stuck.molar_fractions) if f > DROP_TOL)
                    if 2 <= len(keep) < len(cand) and "+".join(keep) not in res:
                        queue.append((keep, depth + 1))
    return res


def frozen(key: str, st: tuple, p_pa: float, t_k: float) -> dict | None:
    """앞 점에서 고른 집합을 **조성 · 분율 그대로** 이 (P, T) 에 둔 값 — 평형을 다시 안 푼다(덧붙임 5 «굳힌 집합»)."""
    import warnings
    rock = _rock(tuple(key.split("+")), st)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            rock.set_state(float(p_pa), float(t_k))
            out = _props(rock, key + "*frozen")
    except Exception:
        return None
    return out if all(math.isfinite(out[f]) and out[f] > 0.0 for f in ("rho", "alpha_k", "c_v", "gamma")) else None


def header(wt: dict[str, float]) -> dict:
    """표의 방아쇠 — 이 가운데 하나라도 다르면 표는 낡았다 (덧붙임 3 ②)."""
    import burnman
    return {"composition_cfmasna_wt": {k: round(v, 12) for k, v in cfmasna(wt).items()},
            "candidates": ["+".join(c) for c in CANDIDATES], "slb": "SLB_2022", "burnman": burnman.__version__,
            "grid": {"p_floor": P_FLOOR, "p_ratio": P_RATIO, "p_top": P_TOP, "t_lo": T_LO, "t_hi": T_HI,
                     "t_step": T_STEP}, "neg_tol": NEG_TOL, "t_seed": T_SEED, "drop_phases": DROP_PHASES,
            "column_rule": COLUMN_RULE}


def header_key(h: dict) -> str:
    """버너만 판을 뺀 머리의 지문 — 엔진은 BurnMan 없이 이 수로 대조한다."""
    body = {k: v for k, v in h.items() if k != "burnman"}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


#: 따뜻한 출발의 씨 온도 — 여기서 위로, 다시 여기서 아래로 훑는다(덧붙임 5).
T_SEED = 1000.0


#: C160 (prereg-c160-column-follows-neighbour, 동결 7adc71fd) — 열이 따르는 규칙의 이름. 표 머리에 들어가 표 지문을 바꾼다.
COLUMN_RULE = "c160"


#: C160 덧붙임 1 — 표가 쓰이는 두 규산염 재질의 녹는곡선 변형. 표는 둘 다에 끼워지므로(`declared`) 더 낮은 쪽을 쓴다.
SOLIDUS_VARIANTS = ("peridotitic", "chondritic")


def solidus_edge(p_pa: float) -> float:
    """C160 덧붙임 1: 표의 물리적 위쪽 경계 — 이 P 에서 엔진의 규산염 고상선(`silicate_melt_fraction` 이 쓰는 것과
    같은 함수 · 변형, d_fe 없음). 두 변형의 낮은 쪽. 이 온도 위의 칸은 수렴하든 말든 짓지 않는다(이름 댄 빈 칸)."""
    import eos
    return min(eos.silicate_solidus(p_pa, v) for v in SOLIDUS_VARIANTS)


def _neighbour(prev: str, ok: list[str]) -> tuple[str | list[str] | None, str]:
    """C160 ② – ④: 앞 점의 승자 `prev` 가 이 점에서 수렴하지 않았을 때 이어 갈 이름과 그 갈래.

    ② 수렴한 후보 가운데 `prev` 의 **진부분집합**(사라진 상만 뺀 것)이 있으면 가장 큰 것 — 상이 나가는 경계.
    ③ 없으면 `prev` 와 **상 하나만 다른**(하나 바꿈 · 하나 더함) 후보들 — 실제 상전이. 호출부가 깁스로 가른다.
    ④ 둘 다 없으면 `None` — 이름 대고 굳힌다. ⚠ 덧붙임 5 의 막이는 이 모양으로 지켜진다: `prev` 의 이웃이 아닌 집합
    (1 bar 의 `plg+ol+opx+cpx` → `wa+gt` 같은)으로는 절대 안 건너간다."""
    pp = set(prev.split("+"))
    subs = [k for k in ok if set(k.split("+")) < pp]
    if subs:
        return max(subs, key=lambda k: len(k.split("+"))), "subset"
    nbrs = [k for k in ok if set(k.split("+")) != pp
            and len(set(k.split("+")) - pp) <= 1 and len(pp - set(k.split("+"))) <= 1]
    return (nbrs, "neighbour") if nbrs else (None, "frozen")


def _column(args):
    """P 한 줄: T_SEED 에서 위로, 다시 T_SEED 에서 아래로 — 앞 점의 수렴을 다음 점의 출발로(덧붙임 5).

    ⚠ **C160: 앞 점에서 이긴 집합이 이 점에서 수렴하지 않으면 수렴한 이웃을 따른다** — 그 집합의 진부분집합(상이
    나감), 없으면 상 하나만 다른 집합(상전이, 깁스 최소). 둘 다 없을 때만 그 집합을 굳혀(`frozen`) 이 점에 두고, 굳힌
    뒤로는 그 줄의 끝까지 굳힌 집합을 이어 간다(오늘과 같다). 진단(C124 뿌리 보고, 2026-10-03): 화성 표의 가열 쪽 굳힘
    시작 242 곳 전부가 상 하나의 몰분율 → 0 이었고 전부 다른 후보가 수렴했다 — 굳힘은 풀이가 아니라 옛 규칙이 만들었다.
    각 칸은 갈래 이름(`same` · `subset` · `neighbour` · `frozen`)을 `rule` 칸에 들고 나가고, 표는 그 수를 센다."""
    bulk, p, ts = args
    out = {}
    t_sol = solidus_edge(p)               # C160 덧붙임 1 — 이 위는 짓지 않는다
    i0 = min(range(len(ts)), key=lambda i: abs(ts[i] - T_SEED))
    for order in (range(i0, len(ts)), range(i0, -1, -1)):
        warm: dict = {}
        prev = None                       # (이긴 이름, 그 상태) — 굳히면 이름 끝에 *frozen
        for i in order:
            if ts[i] > t_sol:
                out.setdefault(i, None)   # 고상선 위 — 이름 댄 빈 칸(표의 `column_rule_counts["above-solidus"]`)
                continue
            if prev is not None and prev[0].endswith("*frozen"):
                got = frozen(prev[0][:-len("*frozen")], prev[1], p, ts[i])
                if got:
                    got["rule"] = "frozen"
            else:
                res = select_all(bulk, p, ts[i], warm)
                if prev is None or prev[0] in res:
                    pick, why = (min(res, key=lambda k: res[k][0]) if res else None), "same"
                else:
                    pick, why = _neighbour(prev[0], list(res))
                    if isinstance(pick, list):
                        pick = min(pick, key=lambda k: res[k][0])
                if pick is not None:
                    got = dict(res[pick][1], rule=why)
                    prev = (pick, res[pick][2])
                elif prev is not None:
                    got = frozen(prev[0], prev[1], p, ts[i])
                    if got:
                        got["rule"] = "frozen"
                    prev = (prev[0] + "*frozen", prev[1]) if got else None
                else:
                    got = None
            if i not in out:
                out[i] = got
    return [out[i] for i in range(len(ts))]


def build(body: str, wt: dict[str, float], procs: int = 4) -> Path:
    """표를 지어 `mantle_tables/<body>.json` 에 쓴다. T 한 줄씩 프로세스에 나눈다."""
    from multiprocessing import Pool
    bulk = atomic_bulk(wt)
    ps, ts = grid_p(), grid_t()
    with Pool(procs) as pool:
        cols = pool.map(_column, [(bulk, p, ts) for p in ps], chunksize=1)
    rows = [[cols[i][j] for i in range(len(ps))] for j in range(len(ts))]
    h = header(wt)
    out = {"body": body, "header": h, "key": header_key(h), "p": ps, "t": ts,
           "assemblage": [[c["assemblage"] if c else None for c in row] for row in rows]}
    # C160 — 칸마다 고른 갈래의 수(same · subset · neighbour · frozen · 빈 칸). 다시 짓기의 앞뒤 대조가 이 칸을 읽는다.
    counts: dict[str, int] = {}
    edges = [solidus_edge(p) for p in ps]
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            k = c.get("rule", "same") if c else ("above-solidus" if ts[j] > edges[i] else "empty")
            counts[k] = counts.get(k, 0) + 1
    out["column_rule_counts"] = counts
    for f in FIELDS:
        out[f] = [[c[f] if c else None for c in row] for row in rows]
    TABLE_DIR.mkdir(exist_ok=True)
    path = TABLE_DIR / f"{out['key']}.json"
    path.write_text(json.dumps(out, separators=(",", ":")) + "\n")
    return path


# ── 표 읽기 (덧붙임 3 ③) — BurnMan 없이 ────────────────────────────────────
_TABLES: dict[str, "Table"] = {}


class TableMiss(Exception):
    """표가 이 (P, T) 에 답하지 않는다 — 빈 칸이거나 격자 밖. 호출부가 `PhaseGap` 으로 옮긴다."""


class Table:
    def __init__(self, d: dict):
        self.body, self.key = d["body"], d["key"]
        self.lnp = [math.log(p) for p in d["p"]]
        self.t = d["t"]
        self.cols = {f: d[f] for f in FIELDS}
        self.assemblage = d["assemblage"]
        # 위쪽 가장자리 (덧붙임 6 ①): 열마다 T_LO 부터 끊김 없이 찬 마지막 T, 이웃 셋의 최소
        tops = []
        for i in range(len(self.lnp)):
            top = None
            for j in range(len(self.t)):
                if self.cols["rho"][j][i] is None:
                    break
                top = self.t[j]
            tops.append(top if top is not None else -math.inf)
        self.edge = [min(tops[max(i - 1, 0):i + 2]) for i in range(len(tops))]

    def edge_at(self, p_pa: float) -> float:
        """표 위쪽 가장자리 E(P) — `edge` 를 ln P 로 선형 보간(덧붙임 6 ①)."""
        x = math.log(max(p_pa, P_FLOOR))
        if x >= self.lnp[-1]:
            return self.edge[-1]
        i = min(max(bisect.bisect_right(self.lnp, x) - 1, 0), len(self.lnp) - 2)
        u = (x - self.lnp[i]) / (self.lnp[i + 1] - self.lnp[i])
        a, b = self.edge[i], self.edge[i + 1]
        if not (math.isfinite(a) and math.isfinite(b)):
            return -math.inf
        return a + u * (b - a)

    def frozen_near(self, p_pa: float, t_k: float) -> bool:
        """이 점을 둘러싼 네 격자점 가운데 굳힌 집합(`*frozen`)이 있는가 — 덧붙임 5 의 계수기."""
        x = math.log(max(p_pa, P_FLOOR))
        i = min(max(bisect.bisect_right(self.lnp, x) - 1, 0), len(self.lnp) - 2)
        j = min(max(bisect.bisect_right(self.t, t_k) - 1, 0), len(self.t) - 2)
        a = self.assemblage
        return any((a[jj][ii] or "").endswith("*frozen") for jj in (j, j + 1) for ii in (i, i + 1))

    def at(self, p_pa: float, t_k: float) -> tuple[float, float, float, float]:
        """(ρ, αK_T, c_V, γ) — (ln P, T) 쌍선형. 1e5 Pa 밑은 첫 점. 네 이웃 중 빈 칸이면 `TableMiss`."""
        x = math.log(max(p_pa, P_FLOOR))
        if x > self.lnp[-1] or not (self.t[0] <= t_k <= self.t[-1]):
            raise TableMiss(f"({p_pa / 1e9:.4f} GPa, {t_k:.1f} K) 가 표 격자(≤ {P_TOP / 1e9:g} GPa, "
                            f"{self.t[0]:g}–{self.t[-1]:g} K) 밖")
        i = min(max(bisect.bisect_right(self.lnp, x) - 1, 0), len(self.lnp) - 2)
        j = min(max(bisect.bisect_right(self.t, t_k) - 1, 0), len(self.t) - 2)
        u = (x - self.lnp[i]) / (self.lnp[i + 1] - self.lnp[i])
        v = (t_k - self.t[j]) / (self.t[j + 1] - self.t[j])
        w = ((1 - u) * (1 - v), u * (1 - v), (1 - u) * v, u * v)
        out = []
        for f in FIELDS:
            c = self.cols[f]
            q = (c[j][i], c[j][i + 1], c[j + 1][i], c[j + 1][i + 1])
            # ⚠ 무게 0 인 이웃은 안 본다 — 격자점 위의 물음이 옆 빈 칸 때문에 거절되지 않게(A′-배관이 잡음)
            if any(x is None and wx > 0.0 for x, wx in zip(q, w)):
                raise TableMiss(f"({p_pa / 1e9:.4f} GPa, {t_k:.1f} K) 둘레 격자점에 평형 집합이 없다 — "
                                f"후보 {len(CANDIDATES)} 개가 모두 수렴하지 않았거나 음수 몰분율")
            out.append(math.fsum(wx * x for x, wx in zip(q, w) if wx > 0.0))     # C143
        return tuple(out)


def expected_key(wt: dict[str, float]) -> str:
    """BurnMan 없이 머리 지문을 다시 짓는다(판 칸만 빼고 `header` 와 같은 사전)."""
    h = {"composition_cfmasna_wt": {k: round(v, 12) for k, v in cfmasna(wt).items()},
         "candidates": ["+".join(c) for c in CANDIDATES], "slb": "SLB_2022",
         "grid": {"p_floor": P_FLOOR, "p_ratio": P_RATIO, "p_top": P_TOP, "t_lo": T_LO, "t_hi": T_HI,
                  "t_step": T_STEP}, "neg_tol": NEG_TOL, "t_seed": T_SEED, "drop_phases": DROP_PHASES,
         "column_rule": COLUMN_RULE}
    return header_key(h)


def load(wt: dict[str, float]) -> tuple[Table | None, str | None]:
    """조성의 표를 읽는다. 없거나 낡았으면 `(None, 이름 대는 거절)` — 조용히 옛 표를 쓰지 않는다.
    파일 이름이 조성 지문이라, 조성 · 후보 · 격자가 바뀌면 다른 파일을 찾고 없으면 거절한다."""
    key = expected_key(wt)
    got = _TABLES.get(key)
    if got is not None:
        return got, None
    path = TABLE_DIR / f"{key}.json"
    if not path.exists():
        return None, (f"맨틀 조성 표 `mantle_tables/{key}.json` 가 없다(조성 · 후보 · 격자의 지문) — "
                      "`engine/.venv-gate/bin/python3 engine/mantle_composition.py --build <몸>` 로 짓는다")
    d = json.loads(path.read_text())
    if d.get("key") != key:
        return None, f"맨틀 조성 표 `{path.name}` 의 머리 지문 {d.get('key')} 가 파일 이름과 다르다"
    _TABLES[key] = Table(d)
    return _TABLES[key], None


# ── 엔진의 표 상 (덧붙임 3 ④) ──────────────────────────────────────────────
#: 표를 읽은 횟수와 그 가운데 등급이 내려가는 칸 — 풀이 앞뒤로 읽어 notes 에 싣는다(덧붙임 4 · 5).
TABLE_ASKS = {"calls": 0, "above_solidus": 0, "frozen": 0, "blend": 0, "outside": 0}
#: 섞임 띠 폭 (덧붙임 6 ②) — T 두 칸. 결과 전 고정.
BLEND_K = 100.0


def _h(s: float) -> float:
    s = min(max(s, 0.0), 1.0)
    return s * s * (3.0 - 2.0 * s)


def _table_phase_class():
    from dataclasses import dataclass
    import eos

    @dataclass(frozen=True)
    class TablePhase(eos.Phase):
        """상부 맨틀 창의 광물 집합 — 밀도 · (∂P/∂T)_V · c_V · γ 를 표에서 읽는다. 냉각 곡선 · 열압력 경로를 안 탄다."""
        table_key: str = ""

        old: object = None                # 원 상 `mgsio3_en` — 표 밖 · 섞임 띠의 짝 (덧붙임 6)

        def _w(self, p: float, t: float) -> float:
            if t is None:
                return 0.0
            tab = _TABLES[self.table_key]
            w = _h((tab.edge_at(p) - 0.5 * T_STEP - t) / BLEND_K) * _h((t - T_LO) / BLEND_K)
            TABLE_ASKS["calls"] += 1
            if w <= 0.0:
                TABLE_ASKS["outside"] += 1
            elif w < 1.0:
                TABLE_ASKS["blend"] += 1
            return w

        def _mix(self, p: float, t: float, k: int, old_value):
            """w · 표 + (1 − w) · 옛 상. w = 0 이면 표를 안 읽는다(옛 상 그대로)."""
            w = self._w(p, t)
            if w <= 0.0:
                return old_value()
            try:
                got = _TABLES[self.table_key].at(p, t)[k]
            except TableMiss as e:        # 가장자리 규칙상 안 닿는 자리 — 닿으면 이름 대고 멈춘다
                raise eos.PhaseGap(self.name, p, f"{self.name}: {e} (섞임 띠 안에서 — 덧붙임 6 ① 위반)")
            return got if w >= 1.0 else w * got + (1.0 - w) * old_value()

        def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
            rho = self._mix(p, t, 0, lambda: self.old.density(p, t, t_pot))
            if t and t > 0.0:
                tab = _TABLES[self.table_key]
                if t <= tab.t[-1] and tab.frozen_near(p, t):
                    TABLE_ASKS["frozen"] += 1
                sol = eos.silicate_solidus(p, self.melt_variant)
                if sol is not None and t > sol:
                    TABLE_ASKS["above_solidus"] += 1
            return rho

        def thermal_pressure(self, t: float, t_pot: float = 0.0) -> float:
            return 0.0            # 밀도가 이미 (P, T) 의 값이다 — 열압력을 따로 빼지 않는다

        def dpdt_v(self, t: float, t_pot: float = 0.0, p: float | None = None) -> float:
            if p is None:
                raise eos.ThermalSetAmbiguous(f"{self.name}: 표 상의 (∂P/∂T)_V 는 압력 없이 못 묻는다")
            return self._mix(p, t, 1, lambda: self.old.dpdt_v(t, t_pot, p))

        def c_v_at(self, p: float | None = None, t: float | None = None) -> float:
            if p is None or t is None:
                raise eos.ThermalSetAmbiguous(f"{self.name}: 표 상의 c_V 는 (P, T) 없이 못 묻는다")
            return self._mix(p, t, 2, lambda: self.old.c_v_at(p, t))

        def gruneisen(self, rho: float, t: float, t_pot: float = 0.0, p: float | None = None) -> float:
            if p is None:
                raise eos.ThermalSetAmbiguous(f"{self.name}: 표 상의 γ 는 압력 없이 못 묻는다")
            return self._mix(p, t, 3, lambda: self.old.gruneisen(self.old.density(p, t, t_pot), t, t_pot, p))

    return TablePhase


_TABLE_PHASE = None


def table_material(base, key: str):
    """규산염 재질 `base` 의 첫 상(표면 – 23.83 GPa)을 표 상으로 바꾼 새 재질. 나머지 상은 그대로(결정 ④ ⓑ)."""
    global _TABLE_PHASE
    from dataclasses import fields, replace
    import eos
    if _TABLE_PHASE is None:
        _TABLE_PHASE = _table_phase_class()
    first = base.phases[0]
    kw = {f.name: getattr(first, f.name) for f in fields(first)}
    kw.update(name="mantle_assemblage", table_key=key, old=first,
              ref=f"BurnMan 2.1.0 SLB 2022 광물 집합 표 `mantle_tables/{key}.json` (prereg-c74-2 덧붙임 3 · 5)",
              join="upper-mantle mineral assemblage (declared oxides)",
              join_note=("밀도 · 열 항은 선언된 산화물 조성의 평형 광물 집합(SLB 2022), 곡선은 맨틀 암석 솔리더스 — "
                         "원 상 `mgsio3_en` 의 녹는곡선 칸 그대로"),
              thermal_source_composition="mantle-assemblage")
    ph = _TABLE_PHASE(**kw)
    return replace(base, name=f"{base.name}_decl_{key[:8]}", phases=(ph,) + tuple(base.phases[1:]))


def declared(wt: dict[str, float] | None):
    """선언이 있으면 규산염 두 재질(`silicate` · `silicate_chondritic`)을 풀이 동안만 표 재질로 바꾼다.
    `(문맥, 거절 문장)` — 표가 없거나 낡았으면 문맥은 None 이다."""
    from contextlib import contextmanager, nullcontext
    import eos
    if wt is None:
        return nullcontext(), None
    tab, why = load(wt)
    if why:
        return None, why

    @contextmanager
    def swap():
        saved = {n: eos.MATERIALS[n] for n in ("silicate", "silicate_chondritic")}
        try:
            for n, m in saved.items():
                eos.MATERIALS[n] = table_material(m, tab.key)
            yield
        finally:
            eos.MATERIALS.update(saved)
    return swap(), None


def _body_wt(body: str) -> dict[str, float]:
    import yaml
    doc = yaml.safe_load((HERE / "bodies" / f"{body}.yaml").read_text())
    decl = (doc.get("inputs") or {}).get("mantle_composition")
    wt, why = read_mantle_composition(decl)
    if why or wt is None:
        sys.exit(f"{body}: {why or '`mantle_composition` 선언이 없다'}")
    return wt


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--build":
        name = sys.argv[2]
        procs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
        print(build(name, _body_wt(name), procs))
    else:
        sys.exit(__doc__)
