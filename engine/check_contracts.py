# 방법론 문서의 계약 블록을 코드와 대조한다 — 문서가 읽히기만 하지 않고 검사받게
"""Check each recipe's documented contract against what the code actually does.

    python3 engine/check_contracts.py

문서에 `Returns` / `Needs` 를 적는 것만으로는 부족하다. 적어놓고 코드가 달라지면
문서가 조용히 거짓말이 된다 — 손으로 친 표가 54배 어긋났던 것과 같은 병이다.

`payload.Result` 는 레시피가 무엇을 먹었고 무엇을 냈는지 이미 들고 있다. 그래서
문서의 선언과 실행 결과를 맞춰볼 수 있고, 어긋나면 실패한다. 계약 블록이 서명이
되려면 이 검사가 있어야 한다.

계약 블록 형식 (방법론 문서 안)
--------------------------------
    ## Contract — `<노드 이름>`

    **Returns** — `a` [단위] · `b` [단위]
    **Needs** — `x` [단위] · `y` [단위]
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import yaml

import graph
import registry
from state import BodyState

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent / "docs" / "reference"
BODIES = HERE / "bodies"

#: C45 (b)/C50 의 클래스 ③ 기준선 — (노드 수, 고유 키 수). 2026-09-09 첫 측정.
#: ⚠ FAIL 이 아니다. 수리 뒤 0 이 되면 그때 FAIL 로 승격한다 (D 와 같은 경로).
#: ⚠ **(8, 8, 13) → (5, 2, 5), 브리프 170 B.** 왜 내려갔는지 없이는 갱신하지 않는다 — 조용히 덮으면
#: 어제의 죽은 기준선과 같아진다. 내려간 여덟은 전부 **한 결함**이었다: 계약의 `Needs` 한 단어가
#: «없으면 답을 못 낸다» 와 «레시피가 기본값을 선언하고 이유까지 적었다» 를 함께 가리켰고, 후자는
#: 구멍이 아니다. `Declared-optional` 줄이 그 여덟을 닫았고 출력은 하나도 안 움직였다.
#: ⚠ **그리고 (5, 2, 5) → (1, 1, 1), 같은 브리프의 둘째 커밋.** 지구가 `core_material: fe_prem` 을
#: 선언하자 네 핵 노드의 칸이 **한꺼번에** 비었다 — 이 검사가 묻는 것은 «어느 표본이든 공급하는가»
#: 이지 «모든 표본이 공급하는가» 가 아니기 때문이다. ⚠ 그 비대칭은 이 수리의 성질이기도 하다:
#: 화성·판도라는 여전히 아무 것도 선언하지 않았고 기본값 `"fe_prem"` 을 그대로 받는다. 칸이 빈 것이
#: 그 둘의 물음이 답해졌다는 뜻은 아니다 (C50 (b) 표 5행, 오너 대기).
#: ⚠ **그리고 (1, 1, 1) → (0, 0, 0), 브리프 170 D — 오너가 판도라의 두 선언을 내린 뒤.** 170 A 는
#: «이 브리프에서 0 이 되지 않는다» 를 등록했고 그것은 **기작에 대해 맞고 시점에 대해 틀렸다**:
#: 남은 칸들은 오너 결정을 기다리고 있었고, 그 결정이 같은 날 왔다.
#: ⚠ **0 은 «다 답해졌다» 가 아니다.** 이 검사는 «어느 표본이든 공급하는가» 를 묻는다. 화성의
#: `core_material` 은 여전히 **선언되지 않았고** 기본값 `"fe_prem"` 을 받는다 — 지구와 판도라가
#: 공급하니 칸이 비었을 뿐이다. 화성 행은 C50 (b) 표 5행에서 오너 대기로 살아 있다 (가벼운 원소가
#: 섞인 철 후보 조사 뒤 결정, 병렬석 P12).
CLASS3_BASELINE = (0, 0, 0)           # (노드, 고유 키, (노드,키) 쌍)
#: C45 (d) 클래스 ④ 기준선 — **선언된 기본값 어느 것과도 다른** 값이 미스한 조회 이름 아래 앉은 수.
#: ⚠ **사전등록은 0 을 예측했고 측정은 12 다** (171 B). 실패한 것은 코드가 아니라 등록이고, 12 는
#: 전부 `interior_layers` 의 `gas_mass_fraction`·`ice_mass_fraction` 이 표본 여섯 바디에서 `0.0` 으로
#: 기록된 것이다 — 선언된 기본값은 **`None`** 인데 레시피가 «없으면 0» 으로 정규화해 쓴 값이 증거에
#: 앉는다. ⚠ 그래서 이 12 는 **결함이 아니라 계약과 증거의 어긋남**이다: 계약은 «모른다»(None)라고
#: 말하고 증거는 «0» 이라고 말한다. 고치려면 정규화를 계약에 적거나 증거에 원값을 남겨야 하고,
#: 둘 다 출력을 건드릴 수 있어 이 브리프의 몫이 아니다 — 세어 두는 것이 먼저다 (C45 (d)).
#: ⚠ **12 → 0, 브리프 171 C — 계약 쪽을 고쳐서다.** 두 키의 `Declared-optional` 항목이 이제
#: «없을 때 증거에 `0.0` 이 기록된다» 를 **문장으로 선언**하고 파서가 그 문장을 읽는다. 무이름
#: 허용목록이 아니다 — 계약이 말하지 않은 정규화는 여전히 클래스 ④ 이고, 새 키가 같은 짓을 하면
#: 문장을 적기 전까지 걸린다. ⚠ **원값(`None`)을 증거에 남기는 쪽은 고르지 않았다**: 그쪽은 출력을
#: 건드릴 수 있고, 이 브리프의 약속은 이동 0 이었다.
CLASS4_BASELINE = 0

#: 클래스 ① (C37 의 서명) 의 **알려진 기존 사례** — 2026-09-09 첫 측정, C50 에 등재.
#: ⚠ **이 집합 밖의 사례는 FAIL 이다.** 기존 넷을 지금 고치는 것은 값을 움직일 수 있어 다음
#: 브리프의 몫이고, 그때 이 집합에서 지운다. 집합을 늘리는 것은 병을 늘리는 것이다.
#: ⚠ **비었다 — 브리프 170 B (C50 (b)) 에서 넷이 다 사라졌다.** 이 집합은 «알려진 클래스 ① 사례»
#: 이고, 여기 없는 클래스 ① 은 FAIL 이다. 넷이 어떻게 나갔는지는 각각 다르다:
#:   `body_class.gas_mass_fraction` · `.semi_major_axis_au` — 조건부 need 였다. 얼음거대행성 대
#:     가스거대행성 분기 안에서만 읽히고 그 분기는 없으면 이름을 대며 거절한다 → Declared-optional.
#:   `dynamo_rocky.dynamo_regime` — 미선언이 **설계된** 상태다(두 분기를 다 낸다, C11) → 같은 줄.
#:   `interior_layers.porosity_cap` — ⚠ 다른 이유다. 계약이 아니라 **증거**가 틀렸다: 역산 분기가
#:     모듈 상수를 조회 이름 아래 `inputs` 에 써 넣고 있었다. 그 덮어쓰기를 지웠다 (`interior.py`).
CLASS1_KNOWN: set[tuple[str, str]] = set()

FIELD = re.compile(r"`([a-z0-9_]+)`")
#: ⚠ **`Declared-optional` 은 더 좁게 읽는다** (170 E). 그 줄은 «왜 기본값이 있는가» 를 산문으로
#: 함께 적으라고 만든 줄이라 백틱이 항목 말고도 나온다 — dynamo 문서의 «the required input is
#: `composition_intent`» 가 그렇게 **진짜 need 를 면제로** 옮겨 놓았다. 그래서 항목은 «백틱 이름
#: 바로 뒤에 단위 대괄호» 라는 모양으로만 인정한다. Needs 줄은 산문을 섞지 않으므로 그대로 둔다.
#: 대괄호는 **닫힌 것만** 인정한다 — 열림만 보면 산문 안의 각괄호에 걸릴 수 있다 (감사석 제안).
OPTIONAL_FIELD = re.compile(r"`([a-z0-9_]+)`\s*\[[^\]]*\]")
#: ⚠ **계약이 «없을 때 증거에 무엇이 기록되는가» 를 말할 수 있어야 한다** (C45 (d) 의 12건, 171 C).
#: 레시피가 «없으면 0» 으로 정규화하면 계약은 `None` 이라 말하고 증거는 `0.0` 이라 말한다 — 그 어긋남을
#: 무이름 허용목록으로 덮지 않고 **계약이 직접 선언**하게 한다. 형식은 Declared-optional 줄 안에서
#: `` `key` [unit] (absent is recorded as `0.0`, …) `` 이고, 그 문장이 없으면 예전처럼 클래스 ④ 다.
NORMALISED = re.compile(r"`([a-z0-9_]+)`\s*\[[^\]]*\][^·]*?absent is recorded as `([^`]+)`")
# 항목이 많으면 줄이 넘어간다. 다음 **항목** 이나 빈 줄까지 이어 읽는다 —
# 문서를 한 줄에 욱여넣게 만들면 읽기 나빠지고, 그건 이 작업의 목적에 반한다.
# ⚠ **계약에 세 번째 줄이 생겼다** (C50 (b), 브리프 170 B): `Needs` 한 단어가 두 가지를 가리키고
#   있었다 — 없으면 답을 못 내는 입력과, 레시피가 **기본값을 선언하고 그 이유를 산문으로 적어 둔**
#   입력. 후자는 구멍이 아닌데 클래스 ③ 이 여덟 건을 구멍으로 세고 있었다. `Declared-optional` 은
#   그 여덟을 위한 줄이고, **새 기본값을 만드는 자리가 아니다** — 이미 코드에 있는 기본값만 옮긴다.
LINE = re.compile(r"^\*\*(Returns|Needs|Declared-optional)\*\*\s*[—-]\s*(.+?)(?=\n\s*\n|\n\*\*|\Z)",
                  re.M | re.S)


def parse_contract(doc: Path, node: str) -> dict[str, set[str]] | None:
    """문서에서 그 노드의 계약 블록을 뽑는다. 없으면 None."""
    text = doc.read_text(encoding="utf-8")
    head = re.search(rf"^##\s*Contract\s*[—-]\s*`{re.escape(node)}`\s*$", text, re.M)
    if not head:
        return None
    rest = text[head.end():]
    nxt = re.search(r"^##\s", rest, re.M)
    block = rest[:nxt.start()] if nxt else rest
    out: dict[str, set[str]] = {}
    for kind, body in LINE.findall(block):
        key = kind.lower().replace("-", "_")
        out[key] = set((OPTIONAL_FIELD if key == "declared_optional" else FIELD).findall(body))
        if key == "declared_optional":
            out["normalised"] = {k: ast.literal_eval(v) for k, v in NORMALISED.findall(body)}
    return out


def ast_lookup_literals(node: str) -> set[str]:
    """레시피 소스에서 `state.get("…")` · `state.get_optional("…")` · `state["…"]` 의 리터럴 키.

    C45 (b) 의 백스톱: 표본 천체가 밟지 않는 분기의 조회는 런타임 로그에 남지 않는다. `state`
    라는 이름에 대한 접근만 센다 — 다른 객체의 `.get("x")` 까지 긁으면 소음이 된다."""
    fn = registry.get(node)
    if fn is None:
        return set()
    src = Path(sys.modules[fn.__module__].__file__).read_text(encoding="utf-8")
    keys: set[str] = set()
    for n in ast.walk(ast.parse(src)):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr in ("get", "get_optional")
                and isinstance(n.func.value, ast.Name) and n.func.value.id == "state"
                and n.args and isinstance(n.args[0], ast.Constant)
                and isinstance(n.args[0].value, str)):
            keys.add(n.args[0].value)
        if (isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name)
                and n.value.id == "state" and isinstance(n.slice, ast.Constant)
                and isinstance(n.slice.value, str)):
            keys.add(n.slice.value)
    return keys


_NO_DEFAULT = object()


def ast_lookup_defaults(node: str) -> dict[str, object]:
    """`state.get("k", <상수>)` 의 **호출부 기본값** — 리터럴일 때만 (C45 (d)).

    ⚠ 이것이 다섯째 모양의 판정축이다. «미스했는데 증거에 수가 있다» 만으로는 **선언된 기본값**과
    **솔버 안에서 몰래 들어온 상수**를 못 가른다 — 전자는 `Declared-optional` 이 이름 붙인 정상이고
    후자가 C45 (c) 가 찾던 것이다. 둘의 차이는 기록된 값이 **그 기본값과 같은가** 이다.
    같은 키가 여러 번 다른 기본값으로 조회되면 판정하지 않는다(`_NO_DEFAULT`)."""
    fn = registry.get(node)
    if fn is None:
        return {}
    src = Path(sys.modules[fn.__module__].__file__).read_text(encoding="utf-8")
    out: dict[str, object] = {}
    for n in ast.walk(ast.parse(src)):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr in ("get", "get_optional")
                and isinstance(n.func.value, ast.Name) and n.func.value.id == "state"
                and n.args and isinstance(n.args[0], ast.Constant)
                and isinstance(n.args[0].value, str)):
            key = n.args[0].value
            if len(n.args) >= 2 and isinstance(n.args[1], ast.Constant):
                val = n.args[1].value
            elif len(n.args) == 1:
                val = None                      # `state.get(k)` 의 기본값은 None 이다
            else:
                val = _NO_DEFAULT               # 리터럴이 아니다 — 판정하지 않는다
            if val is _NO_DEFAULT:
                out[key] = _NO_DEFAULT
            elif out.get(key) is not _NO_DEFAULT:
                out.setdefault(key, set()).add(val) if isinstance(out.get(key), set) else out.__setitem__(key, {val})
    # ⚠ **기본값은 두 층이다** (171 B, 측정으로 배웠다). 어댑터의 `state.get(k, d)` 가 첫 층이고,
    #   레시피 함수의 **파라미터 기본값**이 둘째 층이다 — `ladder(..., ice_mass_fraction: float = 0.0)`
    #   처럼. 증거에 앉은 수가 둘 중 어느 것과도 같지 않을 때에만 «다른 데서 왔다» 고 말할 수 있다.
    #   ⚠ 같은 모듈의 **모든** 함수 파라미터를 이름으로 모으므로 이 쪽은 거칠다 — 거친 쪽이 안전한
    #   방향이다(놓치는 것이 아니라 봐 주는 쪽으로 틀린다). 그 거칢을 여기 적어 둔다.
    for n in ast.walk(ast.parse(src)):
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        args = n.args
        pairs = list(zip(args.args[len(args.args) - len(args.defaults):], args.defaults))
        pairs += [(a, d) for a, d in zip(args.kwonlyargs, args.kw_defaults) if d is not None]
        for arg, d in pairs:
            if isinstance(d, ast.Constant) and out.get(arg.arg) is not _NO_DEFAULT:
                out.setdefault(arg.arg, set())
                if isinstance(out[arg.arg], set):
                    out[arg.arg].add(d.value)
    return out


def explained_by_default(got, accepted) -> bool:
    """증거에 앉은 값이 **선언된 기본값 중 하나** 그대로인가 (C45 (d) 의 판정 한 줄).

    ⚠ 타입까지 본다: `False == 0` 이고 `True == 1` 이라, 타입을 안 보면 불리언 기본값이 0 이나 1 을
    설명해 버린다. 순수 함수로 떼어 둔 이유는 **음성 시험이 이 한 줄을 직접 겨눌 수 있어야** 해서다."""
    return any(got == a and type(got) is type(a) for a in accepted)


def lookup_sets(node: str, bodies: list[BodyState]) -> dict[str, set[str]]:
    """이 노드가 **실제로** 조회한 키들을 표본 전체에서 모은다 (C45 (b)).

    `hit` 는 어느 표본에서든 값이 있었다는 뜻이고, `miss` 는 어느 표본에서도 없었다는 뜻이다.
    ⚠ 마지막에 다시 확인한다 — 초반 회차에서 못 찾고 나중 노드가 공급한 키는 미스가 아니다."""
    hit: set[str] = set()
    asked: set[str] = set()
    hard_asked: set[str] = set()          # get_optional / `in` 이 아닌 조회
    for body in bodies:
        for owner, key, kind in body.lookups:
            if owner != node:
                continue
            asked.add(key)
            if kind.endswith("hit"):
                hit.add(key)
            if kind == "miss":
                hard_asked.add(key)
    for body in bodies:                   # 회차 끝의 상태로 다시 판정
        for key in list(asked - hit):
            found, _ = body._find(key)
            if found:
                hit.add(key)
    return {"asked": asked, "hit": hit, "miss": asked - hit, "hard": hard_asked}


def sample_bodies() -> list[BodyState]:
    """계약을 확인할 표본들.

    하나로는 부족하다. 레시피는 도메인 밖에서 값을 내지 않으므로, 거절하는
    천체만 보면 Returns 를 확인할 수 없다 — 거대행성 하나만 두었더니 암석
    레시피의 출력을 못 봤다. 천체를 훑어 그 레시피가 실제로 값을 내는 것을 쓴다.
    """
    out = []
    for path in sorted(BODIES.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        out.append(BodyState(name=doc["name"], kind=doc["kind"], parent=doc.get("parent"),
                             inputs=doc.get("inputs") or {}, units=doc.get("units") or {}))
    return out


def main() -> int:
    registry.load_all()
    g = graph.load()
    bodies = sample_bodies()
    import run
    for body in bodies:
        run.solve(body, g)
    fails: list[str] = []
    checked = 0
    #: C45 (b) 클래스 ③ — Needs 인데 로스터 어느 천체도 공급하지 않는 조회. **지금은 FAIL 이 아니다**:
    #: 계약이 틀렸는지 천체 선언이 빠졌는지가 아직 안 갈렸다(C50). 기준선보다 늘면 그 줄이 찍힌다.
    class3: dict[str, list[str]] = {}
    class1_seen: set[tuple[str, str]] = set()
    #: C45 (d) 클래스 ④ — 미스한 조회가 증거에 non-None 으로 나타난다. `class4_conv` 는 역산 규약이
    #: 설명하는 히트이고 **판정에서 빼되 인쇄한다** (허용목록이 아니라 결과가 스스로 밝힌 성질이다).
    class4: list[tuple] = []
    class4_conv: list[tuple] = []
    class4_undecided: list[tuple] = []

    for node in sorted(registry.registered()):
        nd = g["nodes"][node]
        slug = nd.get("recipe")
        if not slug:
            fails.append(f"{node}: chain.yaml 에 recipe 문서가 없다")
            continue
        doc = DOCS / f"{slug}.md"
        if not doc.exists():
            fails.append(f"{node}: 문서 {doc.name} 가 없다")
            continue
        declared = parse_contract(doc, node)
        if declared is None:
            fails.append(f"{node}: {doc.name} 에 '## Contract — `{node}`' 블록이 없다")
            continue

        # ⚠ **두 `continue` 위에 있어야 한다** (B2, 2026-09-09): 조회 로그는 노드가 도메인
        # 밖이든 Result 를 못 내든 무관하게 쌓이는데, 아래의 `res is None` · `not res.applicable`
        # 조기 이탈 뒤에 두면 **조회 부재가 그 노드를 못 돌게 만드는 오타는 영원히 안 잡힌다.**
        # ── C45 (b): 문서 Needs · 실제 조회 · AST 리터럴, 세 집합 ────────────────────────
        look = lookup_sets(node, bodies)
        needs = declared.get("needs", set())
        # 선언된 선택적 입력은 «공급되지 않음» 이 정상 상태다 — 클래스 ①·③ 과 오타 검사에서 뺀다.
        optional = declared.get("declared_optional", set())
        literals = ast_lookup_literals(node)
        # ① C37 의 정확한 형태 — 조회가 어느 표본에서도 미스인데 그 `None` 이 **같은 이름으로
        # 증거에 기재**된다. C37 이 초록으로 남은 방식이 바로 이것이다: 값은 없고 이름은 있다.
        never = sorted(((needs - optional) & look["asked"]) - look["hit"])
        filed = set()
        for body in bodies:
            res_b = body.results.get(node)
            if res_b is None:
                continue
            for key in never:
                if key in res_b.inputs and res_b.inputs[key] is None:
                    filed.add(key)
        new_filed = sorted(k for k in filed if (node, k) not in CLASS1_KNOWN)
        known_filed = sorted(k for k in filed if (node, k) in CLASS1_KNOWN)
        if new_filed:
            fails.append(f"{node}: 조회가 전부 미스인데 그 None 이 증거에 같은 이름으로 기재된다 — "
                         f"{', '.join(new_filed)} (C37 의 서명, 클래스 ①)")
        if known_filed:
            print(f"  [클래스 ① · 기존] {node}: {', '.join(known_filed)} — C50 에 등재된 사례")
        class1_seen.update((node, k) for k in filed)
        # ④ 다섯째 모양 (C45 (d)) — **조회가 전부 미스인데 증거에 진짜 수가 들어 있다.** 클래스 ①
        #    은 `is None` 을 보므로 상수나 솔버의 중간값이 앉으면 안 보인다. ⚠ 범위가 `Needs` 가
        #    아니라 **조회된 키 전부**다: `porosity_cap` 은 이제 Declared-optional 이라 `never` 에
        #    안 들어오고, 그러면 첫 사례를 자기 검출기가 못 보게 된다.
        #    ⚠ 예외는 **키가 아니라 regime 에** 건다 — 역산 결과(`inferred_…`)는 자기가 되읽은 축을
        #    그 축의 이름으로 보고하는 것이 이 저장소의 규약이고(170 C), 그 히트도 **인쇄한다**.
        missed_all = sorted(look["asked"] - look["hit"])
        defaults = ast_lookup_defaults(node)
        # 계약이 «없을 때 이 값이 기록된다» 고 적어 둔 것은 설명된 것이다 (171 C).
        for _k, _v in (declared.get("normalised") or {}).items():
            if isinstance(defaults.get(_k), set):
                defaults[_k].add(_v)
            elif _k not in defaults:
                defaults[_k] = {_v}
        for body in bodies:
            res_b = body.results.get(node)
            if res_b is None:
                continue
            inverted = str(getattr(res_b, "regime", "") or "").startswith("inferred_")
            for key in missed_all:
                if key not in res_b.inputs or res_b.inputs[key] is None:
                    continue
                accepted = defaults.get(key, _NO_DEFAULT)
                if accepted is _NO_DEFAULT or not isinstance(accepted, set):
                    class4_undecided.append((node, key, body.name, res_b.inputs[key]))
                    continue
                got = res_b.inputs[key]
                if explained_by_default(got, accepted):
                    continue                    # 선언된 기본값 중 하나가 그대로 기록됐다 — 정상이다
                default = sorted(accepted, key=repr)
                (class4_conv if inverted else class4).append(
                    (node, key, body.name, res_b.inputs[key], getattr(res_b, "regime", None), default))

        rest = sorted(set(never) - filed)
        if rest:
            class3[node] = rest
            print(f"  [클래스 ③] {node}: Needs 인데 어느 표본에서도 공급되지 않는다 — {', '.join(rest)}")
        # ② 철자 오류의 형태 — 선택적이라고 선언되지 않은 조회가 전부 미스이고 Needs 에도 없다.
        #    (클래스 나누기는 C45 (b) 정정 참조: 좁힌 것이 아니라 판정을 셋으로 나눈 것이다.)
        stray = sorted((look["miss"] & look["hard"]) - needs - optional)
        if stray:
            fails.append(f"{node}: 아무도 공급하지 않는 조회이고 Needs 에도 없다 — {', '.join(stray)}")
        # ③ 보고만 — 소스에는 있는데 어느 표본도 밟지 않은 조회, 그리고 아무도 조회하지 않는 Needs.
        unexercised = sorted(literals - look["asked"])
        unread = sorted(needs - look["asked"])
        if unexercised:
            print(f"  [기록] {node}: 소스에 있으나 표본이 밟지 않은 조회 — {', '.join(unexercised)}")
        if unread:
            print(f"  [기록] {node}: Needs 인데 조회되지 않는다 — {', '.join(unread)} "
                  f"(다른 노드의 출력으로 들어올 수 있다)")

        res = None

        union_in = union_out = union_units = None
        for body in bodies:
            # 그래프를 통째로 돌린 뒤에 읽는다. 레시피를 하나만 불러서는 **다른 노드의
            # 출력을 먹는 노드** 의 계약을 확인할 수 없다 — core_state 가 그렇다.
            candidate = body.results.get(node)
            if candidate is None:
                continue
            res = res or candidate
            if candidate.applicable:
                # 가지가 여럿인 레시피는 표본 하나로는 Returns 를 다 못 본다 — 값을 내는
                # 표본 전부의 입력·출력을 합친다 (C19: dynamo_giant 의 갈색왜성 가지).
                if union_in is None:
                    res = candidate
                    union_in, union_out, union_units = set(candidate.inputs), set(candidate.values), dict(candidate.units)
                else:
                    union_in |= set(candidate.inputs); union_out |= set(candidate.values); union_units.update(candidate.units)
        if res is None:
            print(f"  [건너뜀] {node}: 어느 표본 천체도 입력을 갖추지 못했다")
            continue
        if not res.applicable:
            print(f"  [건너뜀] {node}: 표본 천체가 전부 도메인 밖이다 "
                  f"— Returns 를 확인할 수 없다")
            continue
        actual_in = union_in
        actual_out = union_out
        checked += 1

        for label, want, got in (("Needs", declared.get("needs", set()) | optional, actual_in),
                                 ("Returns", declared.get("returns", set()), actual_out)):
            if want - got:
                fails.append(f"{node}: 문서가 {label} 에 적었는데 코드가 안 쓴다 — "
                             f"{', '.join(sorted(want - got))}")
            if got - want:
                fails.append(f"{node}: 코드가 쓰는데 문서 {label} 에 없다 — "
                             f"{', '.join(sorted(got - want))}")

        # 선언된 출력에는 전부 단위가 붙어야 한다. 무차원이면 그렇게 적어야 한다.
        for name in sorted(actual_out):
            if name not in union_units:
                fails.append(f"{node}: 출력 '{name}' 에 단위가 없다")


    gone = sorted(CLASS1_KNOWN - class1_seen)
    if gone:
        print(f"  [클래스 ① · 사라짐] {', '.join(f'{n}.{k}' for n, k in gone)} — "
              f"고쳐졌으면 CLASS1_KNOWN 에서 지울 것")
    n3_nodes = len(class3)
    n3_keys = len({k for v in class3.values() for k in v})
    n3_pairs = sum(len(v) for v in class3.values())
    got3 = (n3_nodes, n3_keys, n3_pairs)
    for node, key, body, val, reg, dflt in class4_conv:
        print(f"  [클래스 ④ · 규약] {node}: 미스한 '{key}' 가 {body} 의 증거에 {val!r} 로 있다 "
              f"(호출부 기본값 {dflt!r}) — 역산이 자기 축을 보고한 것이다 (regime {reg})")
    for node, key, body, val in class4_undecided:
        print(f"  [클래스 ④ · 판정 불가] {node}: '{key}' 의 호출부 기본값이 리터럴이 아니다 "
              f"({body} 의 증거는 {val!r}) — 이 검사가 판정하지 않는다")
    for node, key, body, val, reg, dflt in class4:
        print(f"  [클래스 ④] {node}: 조회가 전부 미스인데 증거에 {val!r} 가 있다 — '{key}' ({body}, "
              f"regime {reg}). 호출부 기본값은 {dflt!r} 이므로 그 수는 **다른 데서 왔다** (C45 (d))")
    got4 = len(class4)
    print(f"  [클래스 ④ 합계] 설명되지 않은 {got4}건 · 역산 규약 {len(class4_conv)}건 · "
          f"판정 불가 {len(class4_undecided)}건 "
          f"(기준선 {CLASS4_BASELINE}) — "
          f"{'변화 없음' if got4 == CLASS4_BASELINE else '⚠ 기준선과 다르다'}")
    print(f"  [클래스 ③ 합계] {n3_nodes} 노드 · 고유 키 {n3_keys} · 쌍 {n3_pairs} "
          f"(기준선 {CLASS3_BASELINE[0]} · {CLASS3_BASELINE[1]} · {CLASS3_BASELINE[2]}, C50) — "
          f"{'변화 없음' if got3 == CLASS3_BASELINE else '⚠ 기준선과 다르다'}")

    total = sum(1 for d in g["nodes"].values() if d.get("kind") == "computed")
    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        n_look = sum(len(b.lookups) for b in bodies)
        print(f"  [PASS] 계약 대조 {checked}건 — 문서와 코드가 일치 "
              f"(레시피 {len(registry.registered())} / 계산 노드 {total}); "
              f"조회 {n_look}건을 Needs·AST 와 대조 (C45 (b))")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
