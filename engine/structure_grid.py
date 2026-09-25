# 바디마다 맨틀 포텐셜 온도 격자 위의 정적 구조 표 — 열진화(core_history)가 걸음마다 보간해 읽는다
"""Structure grid — the interior solved once on a mantle-potential-temperature grid, stored and reused.

    python3 engine/structure_grid.py --refresh earth      # 짓고 굳힌다 (이 단계에서만)
    python3 engine/structure_grid.py --check              # 굳힌 표 전부의 방아쇠 대조 (풀이 없음)

Pre-registration: prereg-structure-grid.md (addenda 1 · 2 · 7). Owner decision 2026-09-24: the structure ↔ thermal-history
coupling defaults to the interpolated table (research plate ⓑ, prereg-structure-coupling addenda 3–12).

What the table holds, per grid point: the six structure numbers `core_history.rates` reads (`p_cmb` · `r_cmb` · `r_b` ·
`r_p` · `g` · `d_mantle_m`) and the core mass fraction, which must be the same at every point — the composition is held
at its S0 value (the body's own structure at its declared potential temperature) and only the temperature moves.

What it refuses, by name: a missing table; a table whose triggers moved (declared values, code, EOS bytes) — it is not
silently rebuilt; a `t_m` below the grid (no extrapolation). Above the grid's top it holds the S0 values («못 봄») when the
structure itself refuses there (`t_ok`), and refuses otherwise.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
import os
#: ⚠ `STRUCTURE_GRID_DIR` 는 **시험 판 전용** — 격자 밀도 재기(prereg-structure-grid 덧붙임 9)가 굳힌 표를 안 덮고 다른 폴더에 짓는다.
GRID_DIR = Path(os.environ["STRUCTURE_GRID_DIR"]) if os.environ.get("STRUCTURE_GRID_DIR") else HERE / "structure_grid"
BODIES_DIR = HERE / "bodies"
N_POINTS = 9                 # 등간격 판(시험용 `--n`) — 노드용 표는 적응형 (덧붙임 11 · 12)
EPS = 5.858398154313838e-4   # 적응형 기준: 표 여섯 칸 상대 보간 오차 (덧붙임 13 — 화성 ε_9, 두 바디 중 작은 쪽)
START_POINTS = 5
MAX_DEPTH = 6
MIN_INTERVAL_K = 1.0
JUMP_RATIO = 10.0            # 값 칸 뜀: 두 반쪽 변화의 큰 쪽 / 작은 쪽 (덧붙임 16)
BELOW_K = 150.0              # 격자 아래 끝 = ⓐ 판 t_m 최저 − 150 K (prereg-structure-grid 덧붙임 7 ③)
ABOVE_K = 50.0               # 위 끝 = ⓐ 판 t_m 최고 + 50 K, 구조가 거절하면 T_ok 로
T_OK_WIDTH_K = 1.0
FIELDS = ("p_cmb", "r_cmb", "r_b", "r_p", "g", "d_mantle_m")
#: 표를 지을 때만 켠다 — 노드가 표 없이 오늘처럼 돌아 ⓐ 판과 S0 를 준다.
BUILDING = False

#: 열진화 선언 — 격자 범위(ⓐ 판의 t_m)를 정하므로 방아쇠에 든다.
THERMAL_KEYS = ("age_gyr", "core_initial_temperature", "mantle_initial_potential_temperature", "tectonic_regime",
                "lid_thickness_km", "surface_temperature_k", "radiogenic_concentration")
CODE_FILES = ("interior.py", "core_history.py", "eos.py")
BYTE_FILES = ("eos.py", "chain.yaml")     # chain.yaml: 표 짓기가 그래프로 S0 · ⓐ 판을 받는다 (9f, 덧붙임 24 고침)
#: 황 앵커는 바이트가 아니라 **표가 쓰는 값**(`fixings`)으로 — 그 파일은 코드 해시를 품어 코드를 고칠 때마다 바이트가 바뀐다 (덧붙임 24)
SULPHUR_ANCHOR = "mars_sulphur_anchor.json"


# ── 방아쇠 ────────────────────────────────────────────────────────────────
def structure_keys() -> tuple[str, ...]:
    """interior 구조 경로가 몸 파일 상태에서 읽는 키 — **코드에서 뽑는다**(AST 합집합, 덧붙임 2 · 7 ④)."""
    import interior
    tree = ast.parse((HERE / "interior.py").read_text(encoding="utf-8"))
    keys = set(interior.SULPHUR_ANCHOR_DECLARATIONS)
    for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
               and n.name in ("_from_state", "_solve_from_state", "_infer_from_state")):
        for n in ast.walk(fn):
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ("get", "get_optional")
                    and isinstance(n.func.value, ast.Name) and n.func.value.id in ("state", "declared")
                    and n.args and isinstance(n.args[0], ast.Constant)):
                keys.add(n.args[0].value)
            if (isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "state"
                    and isinstance(n.slice, ast.Constant)):
                keys.add(n.slice.value)
    return tuple(sorted(keys | set(THERMAL_KEYS)))


def _code_digest(path: Path) -> str:
    """docstring 을 뺀 AST 의 해시 — 주석 · docstring 만 바뀌면 안 움직인다."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if (isinstance(body, list) and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)):
            body.pop(0)
    return hashlib.sha256(ast.dump(tree).encode()).hexdigest()[:16]


def triggers(inputs: dict) -> dict:
    keys = structure_keys()
    return {"declared": {k: inputs.get(k) for k in keys},
            "code": {f: _code_digest(HERE / f) for f in CODE_FILES},
            "bytes": {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest()[:16] for f in BYTE_FILES},
            "sulphur_fixings": json.loads((HERE / SULPHUR_ANCHOR).read_text(encoding="utf-8")).get("fixings")}


def _path_for(name: str) -> Path:
    return GRID_DIR / f"{name.lower()}.json"


# ── 표 읽기 ──────────────────────────────────────────────────────────────
class Grid:
    def __init__(self, doc: dict):
        self.doc = doc
        self.t = [float(x) for x in doc["t_pot"]]
        self.rows = doc["points"]
        self.t_ok = doc.get("t_ok")
        self.breaks = [(float(b[0]), float(b[1])) for b in doc.get("breaks", [])]

    def at(self, t_m: float):
        """(`"ok"`, 여섯 칸) · (`"hold"`, None) · (`"refused"`, 문구)."""
        if t_m < self.t[0]:
            return "refused", (f"구조 표 격자 아래 — t_m {t_m!r} K < {self.t[0]!r} K "
                               f"(외삽 없음, prereg-structure-grid 덧붙임 7 ①)")
        if t_m > self.t[-1]:
            if self.t_ok is not None:
                return "hold", None
            return "refused", f"구조 표 격자 위 — t_m {t_m!r} K > {self.t[-1]!r} K (외삽 없음)"
        for lo_b, hi_b in self.breaks:           # 뜀 1 K 안 — 보간이 건너지 않고 가까운 끝의 값 (덧붙임 16)
            if lo_b < t_m < hi_b:
                end = lo_b if t_m - lo_b <= hi_b - t_m else hi_b     # 정확히 가운데는 t₋ 쪽 (덧붙임 17)
                return "ok", {k: self.rows[self.t.index(end)][k] for k in FIELDS}
        j = 0
        while j < len(self.t) - 2 and t_m > self.t[j + 1]:
            j += 1
        w = (t_m - self.t[j]) / (self.t[j + 1] - self.t[j])
        a, b = self.rows[j], self.rows[j + 1]
        return "ok", {k: a[k] + w * (b[k] - a[k]) for k in FIELDS}


def load_for(state):
    """(Grid, None) 또는 (None, 거절 문구)."""
    path = _path_for(state.name)
    if not path.exists():
        return None, (f"구조 표가 없다 — `{path.relative_to(HERE.parent)}`. 열진화는 걸음마다 구조 표를 보간한다"
                      f"(오너 결정 2026-09-24). `python3 engine/structure_grid.py --refresh {state.name.lower()}` 로 짓는다")
    doc = json.loads(path.read_text(encoding="utf-8"))
    now = triggers(state.inputs)
    moved = [f"{part}.{k}" for part in ("declared", "code", "bytes")
             for k in sorted(set(now[part]) | set(doc["triggers"].get(part, {})))
             if now[part].get(k) != doc["triggers"].get(part, {}).get(k)]
    if now["sulphur_fixings"] != doc["triggers"].get("sulphur_fixings"):
        moved.append("sulphur_fixings")
    if moved:
        return None, (f"구조 표가 낡았다 — 방아쇠 {moved} 가 움직였다. 조용히 다시 풀지 않는다: "
                      f"`python3 engine/structure_grid.py --refresh {state.name.lower()}`")
    return Grid(doc), None


# ── 표 짓기 ──────────────────────────────────────────────────────────────
def _params(v: dict, t_pot: float, m_kg: float) -> dict:
    import cmb_flux as cf
    r_p = v["radius"] * cf.R_EARTH_M
    r_cmb = v["core_radius"] * cf.R_EARTH_M
    return {"p_cmb": v["cmb_pressure"] * 1e9, "r_cmb": r_cmb, "r_b": v["cmb_temperature"] / t_pot,
            "r_p": r_p, "g": cf.G_NEWTON * m_kg / r_p ** 2, "d_mantle_m": r_p - r_cmb}


def _solver(body, s0):
    """S0 의 조성을 고정하고 T_pot 만 바꿔 푸는 함수 (덧붙임 7 ②)."""
    import copy
    import interior
    declared = body.inputs
    cmf0 = s0.values.get("core_mass_fraction")
    if declared.get("composition_intent") is not None or declared.get("core_mass_fraction") is not None:
        how = "declared composition"

        def solve(t):
            b = copy.deepcopy(body); b.results = {}
            b.inputs["potential_temperature"] = float(t)
            return interior._solve_from_state(b)
    elif interior._declared_value(declared.get("core_plus_layer_radius_km")):
        anchor = json.loads(interior.SULPHUR_ANCHOR_FILE.read_text(encoding="utf-8"))
        pin = interior._declared_value(declared.get("light_element_fixing"))
        w_s = anchor["fixings"][pin]["core_sulphur_wt"]
        how = f"fixed sulphur {w_s!r} ({pin}) and cmf {cmf0!r}"

        def solve(t):
            return interior.solve_with_fixed_sulphur(declared["mass_earth"], w_s, pin, cmf0, potential_temperature=float(t),
                                                     basal_iron_number=declared.get("basal_iron_number"))
    else:
        how = f"inferred cmf {cmf0!r} declared"

        def solve(t):
            b = copy.deepcopy(body); b.results = {}
            b.inputs["potential_temperature"] = float(t)
            b.inputs["core_mass_fraction"] = cmf0
            b.inputs["composition_intent"] = "earth_like"
            return interior._solve_from_state(b)
    return solve, how, cmf0


def _fingerprint(r) -> list:
    """층 구성 · 상 지문 — 이웃 점이 다르면 그 구간은 보간 금지 (덧붙임 12 ① · 14).

    ⚠ `silicate_melt_state` · `basal_silicate_state` 는 **넣지 않는다** — 둘 다 적분 뒤 표본을 곡선에 대는 라벨이고 밀도는
    고체 EOS 그대로다(`_silicate_melt_verdict` docstring). 넣으면 지구가 1800–2014 K 에서 거절된다(2026-09-25 확인).
    밀도가 용융을 읽게 되면 돌려 넣는다."""
    v = r.values
    return [r.regime, v.get("ice_column_state"), v.get("core_status")]


def _adaptive(name, solve, lo, hi, eps, m_kg, cmf0):
    """성긴 5 점에서 시작해 구간 가운데를 풀어 보간 오차가 eps 를 넘는 구간만 반으로 (덧붙임 11 · 12)."""
    cache = {}

    def at(t):
        if t not in cache:
            r = solve(t)
            if not r.applicable:
                raise SystemExit(f"{name}: {t!r} K 에서 구조가 거절한다 — 격자 안에서 단조가 아니다: {r.reason}")
            cmf_t = r.inputs.get("core_mass_fraction")
            if cmf_t != cmf0:
                raise SystemExit(f"{name}: {t!r} K 의 cmf {cmf_t!r} 가 S0 {cmf0!r} 와 다르다 — 조성이 고정이 아니다")
            cache[t] = ({**_params(r.values, t, m_kg), "core_mass_fraction": cmf0}, _fingerprint(r))
        return cache[t]

    grid = [lo + (hi - lo) * i / (START_POINTS - 1) for i in range(START_POINTS)]
    todo = [(grid[i], grid[i + 1], 0) for i in range(START_POINTS - 1)]
    done, worst, depth_max, breaks = [], {k: 0.0 for k in FIELDS}, 0, []

    def ratio(pa, pm, pb, k):
        """(비, 왼쪽이 큰가). 큰 반쪽의 상대 변화가 ε 아래면 잡음 크기라 비 1 (덧붙임 17 절대 바닥)."""
        d1, d2 = abs(pm[k] - pa[k]), abs(pb[k] - pm[k])
        small, big = min(d1, d2), max(d1, d2)
        if big / abs(pm[k]) < eps:
            return 1.0, d1 >= d2
        return (big / small) if small > 0 else math.inf, d1 >= d2

    def confirm_jump(a, b, k):
        """큰 반쪽을 1 K 까지 이분 — 매 단계 비가 서야 뜀 (덧붙임 16). 뜀 [x, y] 또는 None."""
        x, y, steps = a, b, 0
        while y - x > MIN_INTERVAL_K:
            m = 0.5 * (x + y)
            r, left_big = ratio(at(x)[0], at(m)[0], at(y)[0], k)
            if r <= JUMP_RATIO:
                return None
            x, y = (x, m) if left_big else (m, y)
            steps += 1
        return x, y, steps
    while todo:
        a, b, d = todo.pop(0)
        pa, fa = at(a)
        pb, fb = at(b)
        if fa != fb:                                  # 불연속 — 이분으로 좁혀 이름 대고 거절
            x, y = a, b
            while y - x > MIN_INTERVAL_K:
                m = 0.5 * (x + y)
                if at(m)[1] == fa:
                    x = m
                else:
                    y = m
            raise SystemExit(f"{name}: 보간 불가 구간 [{x!r}, {y!r}] K — 지문 {fa} → {at(y)[1]}")
        m = 0.5 * (a + b)
        pm, fm = at(m)
        err = {k: abs(0.5 * (pa[k] + pb[k]) - pm[k]) / abs(pm[k]) for k in FIELDS}
        if max(err.values()) > eps and fm == fa:
            jump = None
            for k in FIELDS:
                r, _ = ratio(pa, pm, pb, k)
                if r > JUMP_RATIO:
                    jump = confirm_jump(a, b, k)
                    if jump:
                        x, y, steps = jump
                        size = (at(y)[0][k] - at(x)[0][k]) / abs(at(x)[0][k])
                        breaks.append([x, y, k, size, steps])
                        todo += [(a, x, d + 1), (y, b, d + 1)]
                        depth_max = max(depth_max, d + 1)
                        break
            if jump:
                continue
        if fm != fa or max(err.values()) > eps:
            if d + 1 > MAX_DEPTH or (b - a) / 2 < MIN_INTERVAL_K:
                raise SystemExit(f"{name}: [{a!r}, {b!r}] K 가 깊이 {MAX_DEPTH} · 폭 {MIN_INTERVAL_K} K 안에서 ε {eps!r} 에 "
                                 f"안 든다 (오차 {max(err.values())!r})")
            todo += [(a, m, d + 1), (m, b, d + 1)]
            depth_max = max(depth_max, d + 1)
        else:
            done.append((a, b))
            for k in FIELDS:
                worst[k] = max(worst[k], err[k])
    ts = sorted({t for ab in done for t in ab} | {t for br in breaks for t in br[:2]})
    return ts, [at(t)[0] for t in ts], [at(t)[1] for t in ts], worst, depth_max, len(cache), breaks


def build(name: str, n: int | None = None, points: list[float] | None = None, t_ok: float | None = None,
          eps: float = EPS, grade: str | None = None) -> dict:
    global BUILDING
    import registry
    import run
    import core_history as ch
    import cmb_flux as cf
    registry.load_all()
    body, _ = run.load_body(BODIES_DIR / f"{name.lower()}.yaml")
    rows_cap = {}
    orig = ch.integrate

    def cap(*a, **k):
        r = orig(*a, **k)
        rows_cap.setdefault("rows", r.get("rows"))
        return r
    BUILDING, ch.integrate = True, cap
    try:
        run.solve(body, run.load_chain())
    finally:
        BUILDING, ch.integrate = False, orig
    s0 = body.results["interior_layers"]
    hist = body.results["core_thermal_history"]
    if not (s0.applicable and hist.applicable and rows_cap.get("rows")):
        raise SystemExit(f"{name}: S0 구조 또는 ⓐ 판 열진화가 안 풀린다 — 표를 못 짓는다")
    t_ms = [r["t_m"] for r in rows_cap["rows"]]
    t_pot0 = float(body.inputs["potential_temperature"])
    solve, how, cmf0 = _solver(body, s0)
    check = solve(t_pot0)
    keys = ("radius", "nmoi", "core_radius", "core_radius_fraction", "cmb_pressure", "cmb_temperature")
    if not check.applicable or any(check.values.get(k) != s0.values.get(k) for k in keys):
        raise SystemExit(f"{name}: 조성 고정 풀이가 선언 온도에서 S0 과 비트가 다르다 ({how}) — 표를 못 짓는다")
    lo, hi = min(t_ms) - BELOW_K, max(t_ms) + ABOVE_K
    t_no = None
    top = solve(hi) if points is None else None
    if points is not None:
        pass                                  # 명시 격자(연구판과 같은 점, 덧붙임 9 (가)) — T_ok 도 받은 대로
    elif not top.applicable:
        a, b = lo, hi
        while b - a > T_OK_WIDTH_K:
            mid = 0.5 * (a + b)
            if solve(mid).applicable:
                a = mid
            else:
                b = mid
        t_ok, t_no, hi = a, b, a
    m_kg = body.inputs["mass_earth"] * cf.M_EARTH_KG
    adaptive = {}
    if points is None and n is None:
        grid, points, prints, worst, depth, solves, breaks = _adaptive(name, solve, lo, hi, eps, m_kg, cmf0)
        adaptive = {"eps": eps, "start_points": START_POINTS, "depth_max": depth, "points": len(grid),
                    "structure_solves": solves, "interp_error_max": worst, "discontinuities": "none",
                    "jumps": [{"t_lo": b[0], "t_hi": b[1], "field": b[2], "relative_size": b[3], "steps": b[4]}
                              for b in breaks],
                    "fingerprints": prints}
    else:
        grid = list(points) if points is not None else [lo + (hi - lo) * i / (n - 1) for i in range(n)]
        points = []
        for t in grid:
            r = solve(t)
            if not r.applicable:
                raise SystemExit(f"{name}: 격자 {t!r} K 에서 구조가 거절한다 — 단조가 아니다: {r.reason}")
            cmf_t = r.inputs.get("core_mass_fraction")
            if cmf_t != cmf0:
                raise SystemExit(f"{name}: 격자 {t!r} K 의 cmf {cmf_t!r} 가 S0 {cmf0!r} 와 다르다 — 조성이 고정이 아니다")
            points.append({**_params(r.values, t, m_kg), "core_mass_fraction": cmf0})
    doc = {"body": body.name, "axes": ["potential_temperature"], "t_pot": grid, "points": points, "adaptive": adaptive,
           # 표의 등급 — 적응형 · 자기 검증을 지난 표는 "adaptive", 등간격 임시 표는 그 까닭을 적는다(덧붙임 23)
           "grade": grade or ("adaptive" if adaptive else f"uniform N={len(grid)}"),
           "breaks": [[j["t_lo"], j["t_hi"], j["field"], j["relative_size"]] for j in adaptive.get("jumps", [])],
           "t_ok": t_ok, "t_no": t_no, "composition": how, "s0_potential_temperature": t_pot0,
           "history_t_m_range": [min(t_ms), max(t_ms)], "triggers": triggers(body.inputs)}
    GRID_DIR.mkdir(exist_ok=True)
    _path_for(body.name).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return doc


#: 자기 검증의 판정 양과 폭 (prereg-structure-coupling 덧붙임 11 (나) · structure-grid 덧붙임 12 ②)
VERDICT_T_C_K = 220.0
VERDICT_Q_REL = 0.40
MAX_HALVINGS = 2


def _node_verdict(name: str, grid_dir: Path) -> dict:
    """그 폴더의 표로 노드 열진화를 한 번 — 판정 양만."""
    global GRID_DIR
    import registry
    import run
    registry.load_all()
    saved, GRID_DIR = GRID_DIR, grid_dir
    try:
        body, _ = run.load_body(BODIES_DIR / f"{name.lower()}.yaml")
        run.solve(body, run.load_chain())
    finally:
        GRID_DIR = saved
    h = body.results["core_thermal_history"]
    if not h.applicable:
        raise SystemExit(f"{name}: 자기 검증 판이 안 풀린다 — {h.reason}")
    return {k: h.values[k] for k in ("core_cmb_temperature_present", "q_cmb_present", "inner_core_case",
                                     "entropy_history_verdict")}


def self_checked_build(name: str) -> dict:
    """ε 로 짓고 ε/2 로 한 번 더 지어 판정 양이 0.1 × 폭 안에서 같은지 — 아니면 ε 를 반으로, 최대 두 번 (덧붙임 12 ②)."""
    import tempfile
    global GRID_DIR
    eps, log = EPS, []
    for halving in range(MAX_HALVINGS + 1):
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            saved = GRID_DIR
            try:
                GRID_DIR = Path(d1); doc = build(name, eps=eps)
                GRID_DIR = Path(d2); build(name, eps=eps / 2.0)
            finally:
                GRID_DIR = saved
            a, b = _node_verdict(name, Path(d1)), _node_verdict(name, Path(d2))
        d_t = abs(a["core_cmb_temperature_present"] - b["core_cmb_temperature_present"]) / VERDICT_T_C_K
        d_q = abs(a["q_cmb_present"] - b["q_cmb_present"]) / abs(b["q_cmb_present"]) / VERDICT_Q_REL
        same = a["inner_core_case"] == b["inner_core_case"] and a["entropy_history_verdict"] == b["entropy_history_verdict"]
        log.append({"eps": eps, "t_c_over_width": d_t, "q_cmb_over_width": d_q, "words_same": same})
        if d_t < 0.1 and d_q < 0.1 and same:
            doc["adaptive"]["self_check"] = {"halvings": halving, "log": log}
            GRID_DIR.mkdir(exist_ok=True)
            _path_for(doc["body"]).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            return doc
        eps /= 2.0
    raise SystemExit(f"{name}: ε 를 {MAX_HALVINGS} 번 반으로 줄여도 자기 검증이 안 선다 — {log}")


def check_all() -> int:
    import run
    bad = 0
    for path in sorted(GRID_DIR.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        body, _ = run.load_body(BODIES_DIR / f"{doc['body'].lower()}.yaml")
        _, why = load_for(body)
        print(f"  [{'FAIL' if why else 'PASS'}] {path.name} — {why or '방아쇠 그대로'}")
        bad += bool(why)
    return bad


def main(args: list[str]) -> int:
    if args[:1] == ["--refresh"] and len(args) == 2:
        d = self_checked_build(args[1])
        a = d["adaptive"]
        print(f"굳혔다 → {_path_for(d['body']).name} · 점 {a['points']} · 깊이 {a['depth_max']} · ε {a['eps']!r} · "
              f"오차 최대 {max(a['interp_error_max'].values())!r} · 불연속 {a['discontinuities']} · 뜀 {a['jumps']} · "
              f"자기 검증 {a['self_check']} · T_ok {d['t_ok']} · {d['composition']}")
        return 0
    if args[:1] == ["--refresh"] and len(args) >= 2:      # 시험 판: 등간격 `--n` · 명시 `--points` · `--eps`
        opt = dict(zip(args[2::2], args[3::2]))
        d = build(args[1], n=int(opt["--n"]) if "--n" in opt else None, eps=float(opt.get("--eps", EPS)),
                  points=[float(x) for x in opt["--points"].split(",")] if "--points" in opt else None,
                  t_ok=float(opt["--t-ok"]) if "--t-ok" in opt else None, grade=opt.get("--grade"))
        print(f"굳혔다 → {_path_for(d['body']).name} · 격자 {d['t_pot'][0]:.2f}–{d['t_pot'][-1]:.2f} K · "
              f"T_ok {d['t_ok']} · {d['composition']}")
        return 0
    if args == ["--check"]:
        return 1 if check_all() else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    # ⚠ **스크립트로 돌 때 이 파일은 `__main__` 이다** — core_history 가 읽는 `structure_grid.BUILDING` 은 다른 모듈
    #   객체라, 여기서 바꿔도 안 보인다(2026-09-24 첫 판이 «S0 … 안 풀린다» 로 멈춘 까닭). 이름으로 다시 가져와 그쪽을 돈다.
    sys.path.insert(0, str(HERE))
    import structure_grid
    sys.exit(structure_grid.main(sys.argv[1:]))
