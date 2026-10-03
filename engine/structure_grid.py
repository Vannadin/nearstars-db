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
GRID_POOL = int(os.environ.get("GRID_POOL", "8"))   # 덧붙임 44 — 한 깊이의 가운데 점들을 동시에 푸는 프로세스 수
SPEC_LEVELS = 2              # 덧붙임 55 — 이분 한 판에 미리 풀 나무 깊이. 풀 크기와 무관한 상수(판 · 풀이 집합이 풀과 무관)
KINK_MIN_K = 0.25            # 폭 바닥의 꺾임 구간만 이분 두 번 더 (덧붙임 43) — 꺾임의 선형 보간 오차는 폭에 비례
BELOW_K = 150.0              # 격자 아래 끝 = ⓐ 판 t_m 최저 − 150 K (prereg-structure-grid 덧붙임 7 ③)
ABOVE_K = 50.0               # 위 끝 = ⓐ 판 t_m 최고 + 50 K, 구조가 거절하면 T_ok 로
T_OK_WIDTH_K = 1.0
FIELDS = ("p_cmb", "r_cmb", "r_b", "r_p", "g", "d_mantle_m")
#: 표를 지을 때만 켠다 — 노드가 표 없이 오늘처럼 돌아 ⓐ 판과 S0 를 준다.
BUILDING = False

#: 열진화 선언 — 격자 범위(ⓐ 판의 t_m)를 정하므로 방아쇠에 든다.
THERMAL_KEYS = ("age_gyr", "core_initial_temperature", "mantle_initial_potential_temperature", "tectonic_regime",
                "lid_thickness_km", "surface_temperature_k", "radiogenic_concentration")
CODE_FILES = ("interior.py", "core_history.py", "eos.py", "mantle_composition.py")
#: C159 — 바이트로 해시하는 **데이터** 파일: 표 짓기가 실제로 여는 .py 밖 파일 중 다른 칸이 덮지 않는 것(파일 읽기 가드가 고른다,
#: `tools/table_reads_guard.py`). eos.py 는 뺐다 — `CODE_FILES` 의 AST 해시가 주석 말고는 다 덮는다.
#: chain.yaml 도 뺐다 — 바이트가 아니라 러너가 읽는 투영(`CHAIN_READS`)을 해시한다(설명 칸 편집에 표가 낡지 않게).
BYTE_FILES = ("reference_adiabats.json",)
#: C159 — 표 짓기가 여는데 바이트 칸에 안 넣는 데이터 파일과 그 까닭(가드가 이 목록 밖의 읽기를 멈춤으로 센다).
FILE_EXEMPT = {
    "chain.yaml": "러너가 읽는 투영으로 `chain_reads` 칸이 덮는다",
    "mars_sulphur_anchor.json": "표가 쓰는 값(`fixings`)으로 `sulphur_fixings` 칸이 덮는다 — 바이트는 코드 해시를 품어 늘 움직인다(덧붙임 24)",
    "mantle_tables/": "선언된 조성의 표 바이트로 `mantle_table` 칸이 덮는다(C74-2)",
    "bodies/": "몸 파일 — 표가 읽는 키는 `declared` 칸이 덮는다",
}
#: C159 메모 1 — `--check` 동안 `engine/` 아래에서 열린 파일(감사 훅이 채운다). 코드가 움직인 표를 다시 풀 때 읽기 가드가 이것을 본다.
_READS: set[str] = set()
GUARD_RUNS = [0]              # 읽기 가드가 돈 횟수(값 밖 셈, 시험이 «코드 움직임에서만 돈다» 를 본다)


REPO = HERE.parent
#: 파이썬 자신 · 시스템이 여는 자리 — 데이터 의존이 아니다(가드가 안 센다).
_SYSTEM_PARTS = ("site-packages", "/.venv", "/Library/Developer/", "/System/", "/usr/lib/", "/Library/Caches/com.apple.python",
                 "__pycache__", "/.git/", "/dev/")
#: C159 메모 1 (감사 e2 · 지휘 e0) — 저장소 **밖**에서 읽히는 데이터는 그 자리를 정하는 환경 변수 역할로 센다. 오늘은 읽히는 것이 없고
#: (Earth · Mars · Venus 가드), 역할만 이름 붙여 두며 **방아쇠도 예외도 아니다** — 읽히면 가드가 멈춤으로 센다(등록이 정할 때까지).
OUTSIDE_ROLES = ("NEARSTARS_PAPERS",)


def _reads_hook(event, args):
    """`--check` 동안 열린 파일 전부(저장소 안은 저장소 기준 경로, 밖은 절대 경로) — .py · .pyc · 시스템 자리는 뺀다.
    ⚠ 프로세스 전체에 쌓인다: 코드가 움직인 표의 가드는 그때까지 이 실행이 읽은 것의 **합집합**을 본다(읽기를 더할 뿐이라 보수적)."""
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        try:
            p = Path(os.fsdecode(args[0])).resolve()
        except (OSError, ValueError):
            return
        s_ = p.as_posix()
        if s_.endswith((".py", ".pyc")) or any(x in s_ for x in _SYSTEM_PARTS):
            return
        _READS.add(p.relative_to(REPO).as_posix() if REPO in p.parents else s_)


def guard_reads(opened) -> list[str]:
    """C159 규칙 1b — 연 데이터 파일 중 바이트 방아쇠도 예외 목록(`FILE_EXEMPT`, engine/ 기준)도 아닌 것. 저장소 안 engine/ 밖과
    저장소 밖(환경 변수 역할 `OUTSIDE_ROLES` 포함)은 목록에 없으면 전부 멈춤이다."""
    out = []
    grid = GRID_DIR.resolve()
    for f in sorted(opened):
        p = Path(f) if f.startswith("/") else REPO / f
        if p.resolve().parent in (grid, (HERE / "structure_grid").resolve()):   # 표 자신(`STRUCTURE_GRID_DIR` 로 옮긴 폴더 포함)
            continue
        if f.startswith("engine/"):
            g = f[len("engine/"):]
            if g in BYTE_FILES or g in FILE_EXEMPT or any(g.startswith(k) for k in FILE_EXEMPT if k.endswith("/")):
                continue
        role = next((r for r in OUTSIDE_ROLES if os.environ.get(r) and f.startswith(str(Path(os.environ[r]).resolve()))), None)
        out.append(f if role is None else f"{f} (env {role})")
    return out


#: C159 — chain.yaml 에서 러너(`graph` · `run`)가 실제로 읽는 칸. 설명(note · layer · domain)과 어휘 절은 안 든다.
CHAIN_READS = {"node": ("kind", "recipe", "outputs", "status"), "edge": ("from", "to", "kind", "scope"),
               "coupled_core": ("members",)}
#: 황 앵커는 바이트가 아니라 **표가 쓰는 값**(`fixings`)으로 — 그 파일은 코드 해시를 품어 코드를 고칠 때마다 바이트가 바뀐다 (덧붙임 24)
SULPHUR_ANCHOR = "mars_sulphur_anchor.json"


# ── 방아쇠 ────────────────────────────────────────────────────────────────
def structure_keys() -> tuple[str, ...]:
    """interior 구조 경로가 몸 파일 상태에서 읽는 키 — **코드에서 뽑는다**(AST 합집합, 덧붙임 2 · 7 ④)."""
    import interior
    tree = ast.parse((HERE / "interior.py").read_text(encoding="utf-8"))
    keys = set(interior.SULPHUR_ANCHOR_DECLARATIONS)
    for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
               and n.name in ("_from_state", "_solve_from_state", "_solve_from_state_body", "_solve_declared",
                              "_infer_from_state")):
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


def chain_reads_digest(path: Path | None = None) -> str:
    """C159 — chain.yaml 을 러너가 읽는 칸(`CHAIN_READS`)으로 투영해 정규 JSON 의 해시. 설명 칸 편집은 안 움직인다."""
    import yaml
    g = yaml.safe_load((path or HERE / "chain.yaml").read_text(encoding="utf-8"))
    proj = {"nodes": {n: {k: d.get(k) for k in CHAIN_READS["node"]} for n, d in (g.get("nodes") or {}).items()},
            "edges": [{k: e.get(k) for k in CHAIN_READS["edge"]} for e in (g.get("edges") or [])],
            "coupled_core": {k: (g.get("coupled_core") or {}).get(k) for k in CHAIN_READS["coupled_core"]}}
    return hashlib.sha256(json.dumps(proj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def triggers(inputs: dict) -> dict:
    keys = structure_keys()
    return {"declared": {k: inputs.get(k) for k in keys},
            "chain_reads": chain_reads_digest(),
            "code": {f: _code_digest(HERE / f) for f in CODE_FILES},
            "bytes": {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest()[:16] for f in BYTE_FILES},
            "sulphur_fixings": json.loads((HERE / SULPHUR_ANCHOR).read_text(encoding="utf-8")).get("fixings"),
            "mantle_table": _mantle_table_digest(inputs.get("mantle_composition"))}


def _mantle_table_digest(decl) -> str | None:
    """선언된 맨틀 조성의 광물 집합 표 바이트 (C74-2). 선언이 없으면 None — 표를 안 읽는 몸."""
    import mantle_composition as mc
    wt, _ = mc.read_mantle_composition(decl)
    if wt is None:
        return None
    f = mc.TABLE_DIR / f"{mc.expected_key(wt)}.json"
    return hashlib.sha256(f.read_bytes()).hexdigest()[:16] if f.exists() else "missing"


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
        # 덧붙임 50 — 받을 답 없는 구간: 안에서는 높은 T 쪽 끝(t₊)의 값, 종류 «gap»(냉각 이력)
        self.no_answer = [(float(g[0]), float(g[1])) for g in doc.get("no_answer", [])]

    def at(self, t_m: float):
        """(`"ok"`, 여섯 칸) · (`"hold"`, None) · (`"refused"`, 문구)."""
        if t_m < self.t[0]:
            return "refused", (f"구조 표 격자 아래 — t_m {t_m!r} K < {self.t[0]!r} K "
                               f"(외삽 없음, prereg-structure-grid 덧붙임 7 ①)")
        if t_m > self.t[-1]:
            if self.t_ok is not None:
                return "hold", None
            return "refused", f"구조 표 격자 위 — t_m {t_m!r} K > {self.t[-1]!r} K (외삽 없음)"
        for lo_g, hi_g in self.no_answer:
            if lo_g < t_m < hi_g:
                return "gap", {k: self.rows[self.t.index(hi_g)][k] for k in FIELDS}
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
    # ⚠ **런타임은 코드 칸을 안 본다** (prereg-value-based-staleness, 동결 668e1616 ②) — 코드가 움직였을 때의 검산은
    #   게이트 단계(`--check`)가 격자점 전부를 다시 풀어 한다. 데이터(선언 · .py 밖 바이트 · 황 고정 · 맨틀 표)는 즉시 낡음(⑤).
    moved, _code = _moved(doc["triggers"], now)
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

        def solve(t, p_hint=None):
            b = copy.deepcopy(body); b.results = {}
            b.inputs["potential_temperature"] = float(t)
            return interior._solve_from_state(b, p_hint)
    elif interior._declared_value(declared.get("core_plus_layer_radius_km")):
        anchor = json.loads(interior.SULPHUR_ANCHOR_FILE.read_text(encoding="utf-8"))
        pin = interior._declared_value(declared.get("light_element_fixing"))
        w_s = anchor["fixings"][pin]["core_sulphur_wt"]
        how = f"fixed sulphur {w_s!r} ({pin}) and cmf {cmf0!r}"

        def solve(t, p_hint=None):
            return interior.solve_with_fixed_sulphur(declared["mass_earth"], w_s, pin, cmf0, potential_temperature=float(t),
                                                     p_hint=p_hint,
                                                     basal_iron_number=declared.get("basal_iron_number"),
                                                     mantle_composition=interior._declared_value(
                                                         declared.get("mantle_composition")))
    else:
        how = f"inferred cmf {cmf0!r} declared"

        def solve(t, p_hint=None):
            b = copy.deepcopy(body); b.results = {}
            b.inputs["potential_temperature"] = float(t)
            b.inputs["core_mass_fraction"] = cmf0
            b.inputs["composition_intent"] = "earth_like"
            return interior._solve_from_state(b, p_hint)
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
    import interior
    cache = {}
    noans = {}                                  # 덧붙임 50 — 받을 답 아닌 점 → 까닭
    melt, fire_set, refines58 = {}, set(), []   # 덧붙임 58 · 59 — 점의 용융 상태 · 가족 검사가 선 찾아간 점 · 쪼갠 구간
    aux = {}                                    # 덧붙임 57 — 판정의 T−1 K 보조 점(힌트 없는 풀이) 기억, 값 밖
    spec = {}                                   # 덧붙임 55 ④ — 한 판의 미리 푼 결과(판 끝에 버림, 캐시 · 표 밖)
    spec_stats = {"dispatched": 0, "used": 0, "discarded": 0, "rounds": 0, "max_round": 0}

    def fetch(nodes):
        """덧붙임 55 ①② — 판의 나무 마디 (t, a, b, 부모) 중 안 푼 것을 한 번에 풀로(표는 힌트 없음, 덧붙임 57 ①)."""
        jobs = []
        for t, *_ in nodes:
            if t not in cache and t not in noans and t not in spec and all(j[0] != t for j in jobs):
                jobs.append((t, None))
        for (t, _h), r in zip(jobs, _pool_solve(solve, jobs, aux) if jobs else []):
            spec[t] = r
        spec_stats["dispatched"] += len(jobs)
        spec_stats["rounds"] += 1
        spec_stats["max_round"] = max(spec_stats["max_round"], len(jobs))

    def bisect(chains):
        """덧붙임 55 — 이분 사슬 여럿(서로 독립)을 판 단위로: 판마다 SPEC_LEVELS 깊이 나무를 한 번에 풀고, 결정은 지금 순서대로."""
        before = set(cache) | set(noans)
        chosen = _spec_rounds(chains, fetch)
        spec_stats["discarded"] += len(spec)
        spec.clear()
        leaked = (set(cache) | set(noans)) - before - chosen
        if leaked:     # 덧붙임 55 ④ — 결정이 찾지 않은 점이 캐시에 들면 표가 풀 크기 · 판 모양을 탄다
            raise SystemExit(f"{name}: 미리 푼 점이 찾기 전에 캐시에 들었다 {sorted(leaked)!r} (덧붙임 55 ④)")

    def _take(t, r):
        if getattr(r, "fired", False):
            fire_set.add(t)                     # 덧붙임 59 ① — 찾아간 점이면 역할 무관(받을 답이든 아니든)
        if not r.applicable:
            raise SystemExit(f"{name}: {t!r} K 에서 구조가 거절한다 — 격자 안에서 단조가 아니다: {r.reason}")
        tags = []
        why = interior.answer_verdict(r, tags)   # C130 — 수렴 표지 False 인 점을 표에 조용히 넣지 않는다
        if why is not None:
            noans[t] = why                     # 덧붙임 50 — 멈추지 않고 표시, 구간 처리가 받을 답 없는 구간으로 가른다
            return
        for tag in tags:                        # 덧붙임 4 — 표지는 짓기 로그에만(표 문서 키 무변경)
            print(f"표지 — {t!r} K · {tag}", flush=True)
        cmf_t = r.inputs.get("core_mass_fraction")
        if cmf_t != cmf0:   # 덧붙임 45 «거절문 전부» 밖 — 격자 한계가 아니라 조성 고정 위반(입력 비트 검사)
            raise SystemExit(f"{name}: {t!r} K 의 cmf {cmf_t!r} 가 S0 {cmf0!r} 와 다르다 — 조성이 고정이 아니다")
        cache[t] = ({**_params(r.values, t, m_kg), "core_mass_fraction": cmf0}, _fingerprint(r))
        melt[t] = (r.values.get("silicate_melt_state"), r.values.get("basal_silicate_state"))   # 덧붙임 58 ①

    def at(t, a=None, b=None):
        """t 의 표 칸. (a, b) 는 t 를 가운데로 둔 구간(덧붙임 57 ① 뒤로 힌트는 안 씀 — 부르는 쪽 모양 그대로)."""
        if t in noans:
            raise _NoAnswer(t, noans[t])
        if t not in cache:
            if t in spec:                       # 덧붙임 55 ④ — 이 판에 미리 푼 점은 **찾아올 때** 캐시로(찾는 순서대로)
                spec_stats["used"] += 1
                _take(t, spec.pop(t))
            else:
                _take(t, _pool_solve(solve, [(t, None)], aux)[0])
            if t in noans:
                raise _NoAnswer(t, noans[t])
        return cache[t]

    def prefetch(jobs):
        """덧붙임 44 ② — 아직 안 푼 점들을 풀로 한꺼번에(표는 힌트 없음, 덧붙임 57 ①)."""
        jobs = [(t, near) for t, near in dict.fromkeys(jobs) if t not in cache and t not in noans]
        if not jobs:
            return
        results = _pool_solve(solve, [(t, None) for t, _near in jobs], aux)
        for (t, _near), r in zip(jobs, results):
            if not r.applicable:   # 감사 9f 곁 — 묶음으로 미리 푸니 직렬판과 먼저 만나는 거절 점이 다를 수 있다: 묶음을 찍는다
                print(f"미리 풀기 묶음 {len(jobs)} 점 중 {t!r} K 가 거절(묶음 {[j[0] for j in jobs]!r})", flush=True)
            _take(t, r)

    grid = [lo + (hi - lo) * i / (START_POINTS - 1) for i in range(START_POINTS)]
    done, worst, depth_max, breaks, kinks, gaps = [], {k: 0.0 for k in FIELDS}, 0, [], [], []

    def answered(t, a, b):
        try:
            at(t, a, b)
            return True
        except _NoAnswer:
            return False

    def gap_around(a, b, t_bad, why, t_bad_hi=None):
        """덧붙임 50 ① — 받을 답인 끝점 a, b 사이의 불수락 점 t_bad(덧붙임 57 ⑤: 잇단 불수락 첫 점들이면 t_bad … t_bad_hi)
        둘레를 0.25 K 까지 이분 → [t₋, t₊]."""
        left = _Chain(a, t_bad, KINK_MIN_K, lambda c, m: c.go(m, c.y) if answered(m, c.x, c.y) else c.go(c.x, m))
        right = _Chain(t_bad if t_bad_hi is None else t_bad_hi, b, KINK_MIN_K, lambda c, m: c.go(c.x, m) if answered(m, c.x, c.y) else c.go(m, c.y))
        bisect([left, right])                   # 덧붙임 55 ② — 두 쪽을 한 판에
        return left.x, right.y

    def ratio(pa, pm, pb, k):
        """(비, 왼쪽이 큰가). 큰 반쪽의 상대 변화가 ε 아래면 잡음 크기라 비 1 (덧붙임 17 절대 바닥)."""
        d1, d2 = abs(pm[k] - pa[k]), abs(pb[k] - pm[k])
        small, big = min(d1, d2), max(d1, d2)
        if big / abs(pm[k]) < eps:
            return 1.0, d1 >= d2
        return (big / small) if small > 0 else math.inf, d1 >= d2

    def confirm_jump(a, b, k):
        """큰 반쪽을 1 K 까지 이분 — 매 단계 비가 서야 뜀 (덧붙임 16). 뜀 [x, y] 또는 None."""
        def step(c, m):
            r, left_big = ratio(at(c.x)[0], at(m, c.x, c.y)[0], at(c.y)[0], k)
            if r <= JUMP_RATIO:
                c.stopped = True
                return
            c.go(c.x, m) if left_big else c.go(m, c.y)
            c.steps += 1
        c = _Chain(a, b, MIN_INTERVAL_K, step)
        bisect([c])
        return None if c.stopped else (c.x, c.y, c.steps)
    prefetch([(t, None) for t in grid])
    # 덧붙임 57 ⑤ — 받을 답 아닌 첫 점은 가운데 점과 같게: 양쪽의 가장 가까운 받을 답 첫 점 사이에서 구간을 찾는다
    #   (덧붙임 50 의 «끝점은 받을 답» 문장 · 그 SystemExit 을 대신함). 잇단 불수락 첫 점은 한 구간. 격자 끝은 오늘 규칙.
    for end in (grid[0], grid[-1]):
        if end in noans:
            raise SystemExit(f"{name}: 격자 끝 {end!r} K 가 받을 답 아님 — {noans[end]}")
    ok_pts = [t for t in grid if t not in noans]
    todo = []
    for u, v in zip(ok_pts, ok_pts[1:]):
        bad = [t for t in grid if u < t < v]
        if not bad:
            todo.append((u, v, 0))
            continue
        t_minus, t_plus = gap_around(u, v, bad[0], noans[bad[0]], bad[-1])
        gaps.append([t_minus, t_plus, noans[bad[0]][:160]])
        print(f"받을 답 없는 구간 — [{t_minus!r}, {t_plus!r}] K 폭 {t_plus - t_minus:.3f} K · 첫 점 {bad!r} · "
              f"{noans[bad[0]][:100]}", flush=True)
        todo += [(u, t_minus, 1)] if t_minus > u else []
        todo += [(t_plus, v, 1)] if t_plus < v else []
    while todo:
        # 덧붙임 44 ② — 쌓인 구간들의 가운데 점을 먼저 한꺼번에(캐시에 없는 것만), 판정은 아래 지금 순서 그대로
        prefetch([(0.5 * (a_ + b_), a_) for a_, b_, _d in todo])   # 가운데 점(힌트 없음, 덧붙임 57 ①)
        a, b, d = todo.pop(0)
        try:
            pa, fa = at(a)
            pb, fb = at(b)
        except _NoAnswer as na:   # 덧붙임 57 ⑤ 뒤로 끝점은 늘 받을 답(첫 점 · 구간 끝) — 여기 오면 짓기 규칙 위반
            raise SystemExit(f"{name}: 구간 끝점 {na.t!r} K 가 받을 답 아님 — {na.why} (덧붙임 57 ⑤ 뒤로 일어나면 안 됨)")
        try:
            at(0.5 * (a + b), a, b)
        except _NoAnswer as na:
            t_minus, t_plus = gap_around(a, b, na.t, na.why)
            gaps.append([t_minus, t_plus, na.why[:160]])
            print(f"받을 답 없는 구간 — [{t_minus!r}, {t_plus!r}] K 폭 {t_plus - t_minus:.3f} K · {na.why[:100]}", flush=True)
            todo += [(a, t_minus, d + 1)] if t_minus > a else []
            todo += [(t_plus, b, d + 1)] if t_plus < b else []
            continue
        if fa != fb:                                  # 불연속 — 이분으로 좁혀 이름 대고 거절
            c = _Chain(a, b, MIN_INTERVAL_K, lambda c, m: c.go(m, c.y) if at(m, c.x, c.y)[1] == fa else c.go(c.x, m))
            bisect([c])                       # 덧붙임 55 — 지문 이분도 같은 판
            x, y = c.x, c.y
            raise SystemExit(f"{name}: 보간 불가 구간 [{x!r}, {y!r}] K — 지문 {fa} → {at(y)[1]} "
                             f"(걸린 것: 폭 바닥 — 폭 {y - x:.3f} K ≤ MIN_INTERVAL_K {MIN_INTERVAL_K} K, 깊이 {d}/{MAX_DEPTH})")
        m = 0.5 * (a + b)
        pm, fm = at(m, a, b)
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
            # 덧붙임 43 — 폭 바닥에 닿았고 뜀도 지문 불연속도 아니면 꺾임: 그 구간만 0.25 K 까지 더 반으로.
            #   이 가지는 옛 규칙이 거절하던 자리에서만 열린다(다른 표는 바이트 같음).
            if fm == fa and (b - a) / 2 >= KINK_MIN_K and (d + 1 > MAX_DEPTH or (b - a) / 2 < MIN_INTERVAL_K):
                k_worst = max(err, key=err.get)
                kinks.append([a, b, k_worst, err[k_worst]])
                todo += [(a, m, d + 1), (m, b, d + 1)]
                depth_max = max(depth_max, d + 1)
                continue
            if d + 1 > MAX_DEPTH or (b - a) / 2 < MIN_INTERVAL_K:
                # 덧붙임 45 — 걸린 한계를 수로. 꺾임 가지가 안 열린 까닭(지문 다름 · 반폭 바닥)도 한 낱말로.
                hit = ("꺾임 반폭 바닥" if fm == fa and (b - a) / 2 < KINK_MIN_K else
                       "지문 다름" if fm != fa else "깊이 상한" if d + 1 > MAX_DEPTH else "폭 바닥")
                raise SystemExit(f"{name}: [{a!r}, {b!r}] K 가 ε {eps!r} 에 안 든다 (오차 {max(err.values())!r}) — "
                                 f"걸린 것: {hit} · 깊이 {d}/{MAX_DEPTH} · 폭 {b - a:.3f} K · 폭 바닥 {MIN_INTERVAL_K} K · "
                                 f"꺾임 반폭 바닥 {KINK_MIN_K} K")
            todo += [(a, m, d + 1), (m, b, d + 1)]
            depth_max = max(depth_max, d + 1)
        else:
            # 덧붙임 58 ① — 보간이 ε 안이어도 두 끝의 용융 상태가 다르면 0.25 K 까지. 덧붙임 59 ② — 구간 [a, b] 안(끝 포함)에
            #   가족 검사가 선 찾아간 점이 하나라도 있으면(역할 무관) 그런 점이 없거나 폭 1 K 까지 반으로. 거절하지 않음.
            why58 = ("용융 상태" if melt[a] != melt[b] and (b - a) / 2 >= KINK_MIN_K else
                     "가족 검사" if b - a > MIN_INTERVAL_K and _holds_fire(a, b, fire_set) else None)
            if why58:
                refines58.append([a, b, why58])
                todo += [(a, m, d + 1), (m, b, d + 1)]
                depth_max = max(depth_max, d + 1)
                continue
            done.append((a, b))
            for k in FIELDS:
                worst[k] = max(worst[k], err[k])
    stale = [(a, b, sorted(t for t in fire_set if a <= t <= b)) for a, b in done
             if b - a > MIN_INTERVAL_K and any(a <= t <= b for t in fire_set)]
    if stale:      # 덧붙임 59 ④ — 닫힌 뒤에 찾아간 점이 서면 그 구간은 쪼개지지 않은 채 남는다: 이름 대고 거절
        raise SystemExit(f"{name}: 닫힌 구간 안에 가족 검사가 선 점이 남았다 (덧붙임 59 ④) — {stale[:5]!r}")
    print(f"덧붙임 58 쪼갬 — 용융 상태 {sum(1 for r in refines58 if r[2] == '용융 상태')} · 가족 검사 "
          f"{sum(1 for r in refines58 if r[2] == '가족 검사')} 구간", flush=True)
    print(f"미리 풀기(덧붙임 55) — 보냄 {spec_stats['dispatched']} · 씀 {spec_stats['used']} · 버림 {spec_stats['discarded']} · "
          f"판 {spec_stats['rounds']} · 한 판 최대 {spec_stats['max_round']} 점", flush=True)
    ts = sorted({t for ab in done for t in ab} | {t for br in breaks for t in br[:2]})
    return ts, [at(t)[0] for t in ts], [at(t)[1] for t in ts], worst, depth_max, len(cache), breaks, kinks, gaps


def _holds_fire(a, b, fire_set) -> bool:
    """덧붙임 59 ② — 구간 [a, b](끝 포함)에 가족 검사가 선 찾아간 점이 있나. 시험이 덧붙임 58 의 끝점 판으로 바꿔 끼운다."""
    return any(a <= t <= b for t in fire_set)


class _Chain:
    """덧붙임 55 — 이분 사슬 하나: 구간 [x, y], 폭 바닥, 결정 `step(사슬, 가운데)`(구간을 `go` 로 옮기거나 `stopped`)."""

    def __init__(self, x, y, width, step):
        self.x, self.y, self.width, self.step, self.stopped, self.steps = x, y, width, step, False, 0

    def go(self, x, y):
        self.x, self.y = x, y

    def live(self):
        return not self.stopped and self.y - self.x > self.width


def _spec_rounds(chains, fetch):
    """덧붙임 55 ① — 판마다 살아 있는 사슬들의 다음 SPEC_LEVELS 깊이 나무 마디를 `fetch` 로 한 번에 보내고,
    사슬마다 결정을 SPEC_LEVELS 번까지 지금 순서로. 마디: (t, a, b, 부모 t) — 부모는 같은 판 안의 윗마디(없으면 None).
    돌려주는 값: 결정이 실제로 찾은 가운데 점들(④ 대조용)."""
    chosen = set()
    while any(c.live() for c in chains):
        nodes = []
        for c in chains:
            if not c.live():
                continue
            level = [(c.x, c.y, None)]
            for _ in range(SPEC_LEVELS):
                nxt = []
                for a, b, parent in level:
                    if b - a <= c.width:
                        continue
                    m = 0.5 * (a + b)
                    nodes.append((m, a, b, parent))
                    nxt += [(a, m, m), (m, b, m)]
                level = nxt
        fetch(nodes)
        for c in chains:
            for _ in range(SPEC_LEVELS):
                if not c.live():
                    break
                m = 0.5 * (c.x + c.y)
                chosen.add(m)
                c.step(c, m)
    return chosen


class _NoAnswer(Exception):
    """덧붙임 50 — 이 점은 C130 이 받을 답 아니라고 했다."""

    def __init__(self, t, why):
        super().__init__(why)
        self.t, self.why = t, why


def _light(r):
    """풀 일꾼이 돌려주는 가벼운 결과 — 판정에 쓰는 칸만(결과 객체 전체는 피클하지 않음). `trail` 은 이 풀이의
    가족 기록(덧붙임 57, `interior._FAMILY_TRAIL` 사본 — 풀이 바로 뒤 같은 프로세스에서 읽는다)."""
    import copy
    import types
    import interior
    return types.SimpleNamespace(applicable=r.applicable, reason=r.reason, regime=r.regime,
                                 converged=r.converged, notes=tuple(r.notes or ()),
                                 inputs={"core_mass_fraction": r.inputs.get("core_mass_fraction")},
                                 values=dict(r.values) if r.applicable else {},
                                 trail=copy.deepcopy(interior._FAMILY_TRAIL))


def _solve_raw(solve, jobs):
    """(t, 힌트, 다시 닫기 입구) 들을 공용 도우미로(점마다 `process_state.reset()`), 입력 순서대로."""
    import parallel_points

    def one(t, hint, entry):
        import interior
        interior._ENTRY[0] = entry
        try:
            return _light(solve(t, p_hint=hint) if hint is not None else solve(t))
        finally:
            interior._ENTRY[0] = None
    return parallel_points.solve_points(one, jobs, GRID_POOL)


SETTLE_TRIALS = 4             # 덧붙임 58 ② — 가족 검사가 세는 끝 시행 수(melt-window §1.1 의 끝 창과 같은 수)


def _call_trials(r) -> list:
    """덧붙임 58 ② 노트 — 돌려준 구조를 낸 사격 호출(없으면 거절한 호출)의 시행 전부."""
    call = r.trail.get("answer_call")
    if call is None:
        call = r.trail.get("calls", 0) - 1
    return [x for x in r.trail["trials"] if x[3] == call]


def _fold_band() -> float:
    """C152 메모 1 — 두 갈래가 같이 쓰는 띠(표면 온도 허용). 시험이 0 으로 바꿔 끼워 띠가 막는지를 본다."""
    import interior
    return interior.T_SURFACE_TOL


def _fold(r) -> bool:
    """C152 메모 1 · 2 (iii) — 접힘 탐지기(보장 아님): 그 호출의 **사격이 닫힌** 시행을 ln T_c 순으로. 시행마다 오차
    e = S_max·τ(τ ≤ τ_lin), τ > τ_lin 은 판단 불가. |y| < 띠는 «근 위». 오차 + 띠를 넘는 부호 바뀜이 두 번 이상이거나,
    이웃 사이 역전이 두 오차 + 띠보다 크면 선다."""
    import interior              # C152 메모 4 — τ_lin · S_max 는 interior.SIGN_* 한 쌍(부호를 읽는 모든 자리가 같이 씀)
    band = _fold_band()
    pts = []
    for x in sorted(_call_trials(r), key=lambda x: x[1]):
        if len(x) < 6 or not x[5] or x[4] is None:
            continue
        tau = x[6] if len(x) > 6 and x[6] is not None else None
        if tau is None or tau > interior.SIGN_TAU_LIN:
            continue                                   # 판단 불가(메모 2)
        e = interior.SIGN_S_MAX * tau
        if abs(x[4]) < band + e:
            continue                                   # 근 위 · 오차 안
        pts.append((x[4], e))
    flips = sum(1 for (a, _ea), (b, _eb) in zip(pts, pts[1:]) if (a < 0.0) != (b < 0.0))
    if flips > 1:
        return True
    if len(pts) >= 3:
        trend = pts[-1][0] - pts[0][0]
        return any((b - a) * trend < 0.0 and abs(b - a) > ea + eb + band for (a, ea), (b, eb) in zip(pts, pts[1:]))
    return False


def _settled_trials(r) -> list:
    """덧붙임 58 ② — 돌려준 구조를 낸 사격 호출의 마지막 SETTLE_TRIALS 시행(그 호출이 짧으면 그 호출 전부, 앞 호출에서
    빌리지 않음). 돌려준 구조가 없으면(예외로 거절) 거절한 호출 = 마지막으로 시작한 호출 — 덧붙임 58 사전 정리 노트
    (첫 시행 전에 거절했으면 그 호출의 시행이 없어 창 없음)."""
    return _call_trials(r)[-SETTLE_TRIALS:]


def _families_visited(r) -> list:
    """풀이의 정착 창 시행 가족들(대표, 처음 본 순서) — 덧붙임 57 ② 를 덧붙임 58 ② 로 좁힘."""
    import interior
    reps = []
    for f, *_ in _settled_trials(r):
        if all(interior._family_jump(o, f) for o in reps):
            reps.append(f)
    return reps


def _fires(r) -> bool:
    """덧붙임 57 ② — 가족 검사: 힌트 없는 풀이가 가족 둘 이상을 거쳤거나 가족 거절 · «답 둘» 로 끝남."""
    import interior
    why = interior.answer_verdict(r) if r.applicable else None
    return (len(_families_visited(r)) >= 2 or bool(why) and (why.startswith(interior.FAMILY_OSCILLATION_NOTE)
                                                             or why.startswith(interior.FAMILY_TWO_NOTE))
            or _fold(r))                                                          # C152 메모 1 (iii)


def _contrib(r) -> list:
    """덧붙임 57 ④ — 한 멤버가 내놓는 닫힌 가족: 답 → 그 가족 하나 · «답 둘» → 이름 댄 닫힌 갈래들 · 그 밖 → 없음."""
    import interior
    why = interior.answer_verdict(r)
    if why is None:
        return [r.trail["answer"]]
    return list(r.trail["closed"]) if why.startswith(interior.FAMILY_TWO_NOTE) else []


def _entries(members) -> list:
    """덧붙임 57 ③(c) — a · b 의 시행 가족 + 닫힌 · 다시 닫은 갈래 + 답 가족을 이어 묶고, 닫히거나 다시 닫힌 적
    없는 묶음마다 입구 = 그 묶음의 마지막 시행(a 의 시행 다음 b 의 시행 순서)의 (중심 온도, 중심압)."""
    import interior
    items = []
    for r in members:
        items += [{"family": f, "done": False, "entry": (t, p)} for f, t, p, *_rest in r.trail["trials"]]
        items += [{"family": f, "done": True, "entry": None} for f in list(r.trail["closed"]) + list(r.trail["reclosed"])]
        if interior.answer_verdict(r) is None:
            items.append({"family": r.trail["answer"], "done": True, "entry": None})
    out = []
    for g in interior._family_groups(items):
        if any(i["done"] for i in g):
            continue
        order = [i for i in items if i in g and i["entry"] is not None]    # items 순서 = a 시행 다음 b 시행
        if order:
            out.append(order[-1]["entry"])
    return out


def _judge(t, a, b, cs):
    """덧붙임 57 ④ — 고정 출발 셋의 닫힌 가족 묶음으로 한 판정. 멤버 순서 a, b, c₁ …(같은 어긋남이면 앞)."""
    import types
    import interior
    members = [("a", a)] + ([("b", b)] if b is not None else []) + [(f"c{i + 1}", c) for i, c in enumerate(cs)]
    items = [{"family": f, "who": k, "r": r} for k, r in members for f in _contrib(r)]
    groups = interior._family_groups(items)
    say = " · ".join(f"{k} {'답' if interior.answer_verdict(r) is None else (interior.answer_verdict(r) or '')[:24]}"
                     for k, r in members)
    print(f"판정(덧붙임 57) — {t!r} K · 묶음 {len(groups)} · {say}", flush=True)
    if not groups:
        return a
    if len(groups) == 1:
        order = [k for k, _r in members]
        cand = [i for i in groups[0] if interior.answer_verdict(i["r"]) is None]
        best = min(cand, key=lambda i: ((i["r"].trail["dev"] if i["r"].trail["dev"] is not None else math.inf),
                                        order.index(i["who"])))
        return best["r"]
    names = " · ".join("고체" if g[0]["family"] is None else f"[{g[0]['family'][0]:.2f}, {g[0]['family'][1]:.2f}] GPa"
                       for g in groups)
    return types.SimpleNamespace(**{**vars(a), "converged": False,
                                    "notes": (interior.FAMILY_TWO_NOTE + f" — 덧붙임 57 출발 셋({', '.join(k for k, _ in members)})이 "
                                              f"다른 가족 묶음 {len(groups)} 개로 닫힘(고르지 않음): {names}",)})


def _core_p(r):
    """답인 풀이의 중심압 [Pa] — 덧붙임 57 ③(b) 의 T−1 K 격자 힌트. 받을 답 아니면 None(b 멤버 없음)."""
    import interior
    if interior.answer_verdict(r) is not None or not r.values.get("core_pressure"):
        return None
    return r.values["core_pressure"] * 1e9


def _pool_solve(solve, jobs, aux=None):
    """표의 점들을 푼다 — 덧붙임 57: 힌트는 버리고(①) 힌트 없는 풀이(a)를 풀로, 가족 검사가 서는 점만 고정 출발 셋
    (b = T−1 K 격자 힌트 · c = 안 닫힌 가족마다 다시 닫기)을 더 풀어 한 규칙으로 판정. `aux` 는 짓기 한 판의 a 풀이
    기억(T → 결과, 값은 순서와 무관 — 점마다 초기화 · 힌트 없음)."""
    aux = {} if aux is None else aux
    ts = [t for t, _h in jobs]
    new = [t for t in dict.fromkeys(ts) if t not in aux]
    for t, r in zip(new, _solve_raw(solve, [(t, None, None) for t in new]) if new else []):
        aux[t] = r
    fire = [t for t in dict.fromkeys(ts) if _fires(aux[t])]
    for t in dict.fromkeys(ts):           # 덧붙임 58 ② — 점마다 정착 창(호출 번호 · 시행 수 · 가족 수)
        w = _settled_trials(aux[t])
        print(f"창(덧붙임 58) — {t!r} K · 호출 {w[0][3] if w else None}(답 호출 {aux[t].trail.get('answer_call')}) · 시행 {len(w)} · 가족 "
              f"{len(_families_visited(aux[t]))} · 검사 {t in fire}", flush=True)
    if not fire:
        return [aux[t] for t in ts]
    new = [t - 1.0 for t in fire if t - 1.0 not in aux]
    for t, r in zip(new, _solve_raw(solve, [(t, None, None) for t in new]) if new else []):
        aux[t] = r
    b_jobs = [(t, _core_p(aux[t - 1.0]), None) for t in fire if _core_p(aux[t - 1.0]) is not None]
    bs = dict(zip([j[0] for j in b_jobs], _solve_raw(solve, b_jobs) if b_jobs else []))
    c_jobs = [(t, None, e) for t in fire for e in _entries([aux[t]] + ([bs[t]] if t in bs else []))]
    cs = {t: [] for t in fire}
    for (t, _h, _e), r in zip(c_jobs, _solve_raw(solve, c_jobs) if c_jobs else []):
        cs[t].append(r)
    judged = {t: _judge(t, aux[t], bs.get(t), cs[t]) for t in fire}
    for t in fire:
        judged[t].fired = True            # 덧붙임 58 ③ — 짓기가 이 점 둘레를 쪼갠다(값 밖 표시)
    return [judged.get(t, aux[t]) for t in ts]


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
    # 덧붙임 46 — 두 풀이는 같은 출발에서: 조성 고정 풀이에 S0 의 중심압을 힌트로. 이 점검은 결정성과 «S0 사슬이
    #   구조를 바꾸지 않음» 을 본다(«출발이 달라도 같은 답» 은 안 봄 — 그 흔들림은 T_TOL 급, 표 ε 의 1000 배 밑).
    p_c0 = s0.values.get("core_pressure")
    check = solve(t_pot0, p_hint=p_c0 * 1e9 if p_c0 else None)
    keys = ("radius", "nmoi", "core_radius", "core_radius_fraction", "cmb_pressure", "cmb_temperature")
    # 덧붙임 42 — 비트가 아니라 엔진 자신의 수렴 허용(SHOOT_TOL, 겉질량의 선을 여섯 칸에 옮긴 judgment) 안이면 같은 풀이다. 단계 벽 폴백(RK45 덧붙임 2)이
    #   S0 의 역산 시행과 조성 고정 풀이에서 다른 횟수로 밟혀 끝자리가 갈린다(화성 5.1e-11). 0 칸은 절대 0.
    import interior
    worst, where = 0.0, ""
    for k in keys:
        a, b = s0.values.get(k), check.values.get(k) if check.applicable else None
        d = 0.0 if a == b else (abs(b - a) / abs(a) if a and b is not None else math.inf)
        if d > worst:
            worst, where = d, k
    if not check.applicable or worst > interior.SHOOT_TOL:
        raise SystemExit(f"{name}: 조성 고정 풀이가 선언 온도에서 S0 과 다르다 ({how}; 최대 상대 차 {worst:.3e} at {where}, "
                         f"허용 SHOOT_TOL {interior.SHOOT_TOL:.0e}) — 표를 못 짓는다")
    print(f"자기 점검 — 조성 고정 풀이 대 S0 최대 상대 차 {worst:.3e} at {where or '-'} (허용 SHOOT_TOL {interior.SHOOT_TOL:.0e})")
    lo, hi = min(t_ms) - BELOW_K, max(t_ms) + ABOVE_K
    t_no = None
    top = solve(hi) if points is None else None
    if points is not None:
        pass                                  # 명시 격자(연구판과 같은 점, 덧붙임 9 (가)) — T_ok 도 받은 대로
    elif not top.applicable:
        got = {}                              # 덧붙임 55 — T_ok 이분도 같은 판(힌트 없음 그대로, 판 끝에 버림)

        def fetch(nodes):
            jobs = [(t, None) for t, *_ in nodes if t not in got]
            for (t, _h), r in zip(jobs, _pool_solve(solve, jobs) if jobs else []):
                got[t] = r
        c = _Chain(lo, hi, T_OK_WIDTH_K, lambda c, m: c.go(m, c.y) if got[m].applicable else c.go(c.x, m))
        _spec_rounds([c], fetch)
        t_ok, t_no, hi = c.x, c.y, c.x
    if points is None:
        print(f"T_ok 가지(덧붙임 55) — 위 끝 {top.applicable and '받음' or '거절 → 이분'} · t_ok {t_ok!r} · t_no {t_no!r}", flush=True)
    m_kg = body.inputs["mass_earth"] * cf.M_EARTH_KG
    adaptive = {}
    gaps = []
    if points is None and n is None:
        grid, points, prints, worst, depth, solves, breaks, kinks, gaps = _adaptive(name, solve, lo, hi, eps, m_kg, cmf0)
        for a, b, k, e in kinks:     # 덧붙임 43 — 로그에만(표 문서 키는 그대로)
            print(f"꺾임 — [{a!r}, {b!r}] K 폭 {b - a:.3f} K 를 더 반으로 · 칸 {k} · 오차 {e:.3e}", flush=True)
        adaptive = {"eps": eps, "start_points": START_POINTS, "depth_max": depth, "points": len(grid),
                    "structure_solves": solves, "interp_error_max": worst, "discontinuities": "none",
                    "jumps": [{"t_lo": b[0], "t_hi": b[1], "field": b[2], "relative_size": b[3], "steps": b[4]}
                              for b in breaks],
                    "fingerprints": prints}
    else:
        grid = list(points) if points is not None else [lo + (hi - lo) * i / (n - 1) for i in range(n)]
        points = []
        for t, r in zip(grid, _pool_solve(solve, [(t, None) for t in grid])):   # 덧붙임 44 ③ — 힌트 없음 그대로
            if not r.applicable:
                raise SystemExit(f"{name}: 격자 {t!r} K 에서 구조가 거절한다 — 단조가 아니다: {r.reason}")
            tags = []
            why = interior.answer_verdict(r, tags)   # C130
            if why is not None:
                raise SystemExit(f"{name}: 격자 {t!r} K 에서 받을 답 아님 — {why}")
            for tag in tags:                          # 덧붙임 4
                print(f"표지 — {t!r} K · {tag}", flush=True)
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
    if gaps:                                   # 덧붙임 50 ② — 구간이 없는 표는 칸을 안 쓴다(바이트 같음)
        doc["no_answer"] = gaps
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


def _moved(then: dict, now: dict) -> tuple[list[str], list[str]]:
    """(데이터 칸 움직임, 코드 칸 움직임) — `.py` 는 코드, 그 밖은 데이터(prereg-value-based-staleness ⑤)."""
    data, code = [], []
    for part in ("declared", "code", "bytes"):
        for k in sorted(set(now[part]) | set(then.get(part, {}))):
            if now[part].get(k) != then.get(part, {}).get(k):
                (code if part == "code" or (part == "bytes" and k.endswith(".py")) else data).append(f"{part}.{k}")
    if now.get("chain_reads") != then.get("chain_reads"):
        data.append("chain_reads")              # C159 — 옛 꼴 표(칸 없음)도 여기서 한 번 낡음으로 이름 댄다(규칙 4)
    if now["sulphur_fixings"] != then.get("sulphur_fixings"):
        data.append("sulphur_fixings")
    if now.get("mantle_table") != then.get("mantle_table"):
        data.append("mantle_table")
    return data, code


def _recheck(doc: dict, body) -> tuple[float, str]:
    """코드가 움직인 표의 검산 — 격자점 **전부**를 다시 풀어 저장 여섯 칸과의 최대 상대 차(②④). (차, 칸 이름)."""
    import types
    import cmb_flux as cf
    solve, _how, _cmf = _solver(body, types.SimpleNamespace(values={"core_mass_fraction": doc["points"][0]["core_mass_fraction"]}))
    m_kg = body.inputs["mass_earth"] * cf.M_EARTH_KG
    worst, where = 0.0, ""
    for t, row in zip(doc["t_pot"], doc["points"]):
        r = solve(t)
        if not r.applicable:
            return math.inf, f"{t!r} K 에서 거절 — {(r.reason or '')[:80]}"
        new = _params(r.values, t, m_kg)
        for k in FIELDS:
            d = abs(new[k] - row[k]) / abs(row[k])
            if d > worst:
                worst, where = d, f"{k} @ {t:.2f} K"
    return worst, where


def history_bodies() -> list[str]:
    """C159 규칙 3 — 열진화 입력(`core_initial_temperature`)을 선언한 출하 몸. 이 몸은 전부 표가 있어야 한다(예외 목록 없음)."""
    import yaml
    out = []
    for f in sorted(BODIES_DIR.glob("*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if "core_initial_temperature" in (doc.get("inputs") or {}):    # `run.load_body` 와 같은 자리
            out.append(f.stem)
    return out


def check_all() -> int:
    """방아쇠 대조 — 데이터가 움직이면 낡음(FAIL), **코드만** 움직이면 격자점 전부를 다시 풀어 ε 안이면 통과
    (prereg-value-based-staleness, 동결 668e1616). 못 봄: 격자점 사이에서만 곡선이 바뀌는 변경.
    C159 규칙 3 — 열진화 입력을 선언한 출하 몸에 표가 **없으면** FAIL(예전엔 표 파일만 돌아 조용했다: 금성)."""
    import run
    bad = 0
    for name in history_bodies():
        if not _path_for(name).exists():
            print(f"  [FAIL] {name} — 열진화 입력(core_initial_temperature)을 선언했는데 구조 표가 없다: "
                  f"열진화가 cannot-say 다. `--refresh {name}` (C159 규칙 3)")
            bad += 1
    for path in sorted(GRID_DIR.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        body, _ = run.load_body(BODIES_DIR / f"{doc['body'].lower()}.yaml")
        data, code = _moved(doc["triggers"], triggers(body.inputs))
        if data:
            print(f"  [FAIL] {path.name} — 데이터 방아쇠 {data} 가 움직였다 — `--refresh {doc['body'].lower()}`")
            bad += 1
            continue
        if not code:
            print(f"  [PASS] {path.name} — 방아쇠 그대로")
            continue
        worst, where = _recheck(doc, body)
        ok = worst <= EPS
        print(f"  [{'PASS' if ok else 'FAIL'}] {path.name} — 코드 움직임 {code} · 값 허용 {'안' if ok else '밖'}"
              f"(최대 상대 차 {worst:.3e} at {where}, ε {EPS:.4e}, 격자점 {len(doc['t_pot'])})"
              + ("" if ok else f" — `--refresh {doc['body'].lower()}`"))
        bad += not ok
        # C159 메모 1 — 읽기 가드는 **코드가 움직인 표에서만** 돈다: 읽는 파일이 바뀌려면 코드가 바뀌어야 하고, 그때 여기서
        #   격자점을 어차피 다시 푼다(덧값 없음). 데이터만 움직인 표는 위에서 이미 낡음(FAIL)이다.
        GUARD_RUNS[0] += 1
        unlisted = guard_reads(_READS)
        if unlisted:
            print(f"  [FAIL] {path.name} — 읽기 가드: 방아쇠도 예외도 아닌 데이터 파일을 읽었다 {unlisted} — "
                  f"`BYTE_FILES` 에 넣거나 `FILE_EXEMPT` 에 까닭과 함께 (C159 규칙 1b)")
            bad += 1
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
        sys.addaudithook(_reads_hook)      # C159 메모 1 — 가져오기 때 읽는 데이터까지 보려면 무엇보다 먼저
        return 1 if check_all() else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    # ⚠ **스크립트로 돌 때 이 파일은 `__main__` 이다** — core_history 가 읽는 `structure_grid.BUILDING` 은 다른 모듈
    #   객체라, 여기서 바꿔도 안 보인다(2026-09-24 첫 판이 «S0 … 안 풀린다» 로 멈춘 까닭). 이름으로 다시 가져와 그쪽을 돈다.
    sys.path.insert(0, str(HERE))
    import structure_grid
    sys.exit(structure_grid.main(sys.argv[1:]))
