# 거절 사전 — 입력 거절(A7)과 풀이 거절(A1)의 id · 근거 칸 · 문장 틀을 한곳에 둔다 (phase1-design D-A7-6).
"""The one refusal registry of the phase-1 solver (`rewrite/phase1-design.frozen.md` D-A7-6, D-A3-2, §A1.5).

Each id declares its evidence fields and a Korean text template. `make` builds a `Refusal` and checks the id and
the fields; `no_answer` does the same for a `NoAnswer`. The text is rendered from the fields and never parsed back:
consumers read `Refusal.id` and `Refusal.evidence` (X3). A7 owns this module; A1 registers the `solve.*` ids
(evidence sets as b9 sent them, 2026-10-09).
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from solver.body import CLOSURE_KINDS
from solver.result import NO_ANSWER_REASONS, NoAnswer, Refusal, Where


@dataclass(frozen=True)
class Entry:
    id: str
    fields: tuple          # required evidence fields (a field may hold None where the entry says so)
    template: str          # str.format over the evidence fields and `where`
    optional: tuple = ()   # evidence fields that may be absent
    preamble: str = ""     # lay sentence put before the technical one (R-C122-4)
    solve: bool = False    # a solver refusal: carries the common solve fields, checked below


#: Common fields of every `solve.*` id (b9): the closure scalar's trial or root value (or None), the closure kind,
#: the pass kind, and the reached state {m, r, P, T, layer_id} where one exists.
SOLVE_COMMON = ("x", "closure_kind", "pass_kind")
#: Optional on every solve.* id: the reached state, the scan trace, and the walls and solved regions (§A1.5: «the
#: refusal at the lowest-x wall is the Outcome, with the scan in the evidence»; b9 2026-10-09).
SOLVE_OPTIONAL = ("state", "scan", "walls", "solved_regions",
                  "first_attempt")   # phase-1 design note 18: a retried closure's first residual failure
PASS_KINDS = ("scan", "wall", "brent", "accepted", "band", "probe")
#: A wall record (b9 2026-10-09): the trial x, what stopped it (a refusal id or a NoAnswer reason), the reached state,
#: and whether the wall's position was located.
WALL_FIELDS = ("x", "outcome_kind", "id_or_reason", "state", "located")
EVENT_CAPS = ("EVENT_MIN_PROGRESS", "EVENT_RESTARTS_STEP", "EVENT_RESTARTS_SOLVE", "EVENT_REWALKS")

_SOLVE = (
    Entry("solve.no_bracket", ("x_lo", "x_hi", "F_lo", "F_hi", "n_scan", "walls", "solved_regions"),
          "닫힘 잔차가 선언 범위 [{x_lo}, {x_hi}] 에서 부호를 바꾸지 않는다 — F {F_lo} · {F_hi}, 훑기 {n_scan} 번"),
    Entry("solve.two_roots", ("roots", "F_scan", "n_scan"),
          "닫힘 잔차의 근이 둘 이상이다 — 근 {roots} (훑기 {n_scan} 번)"),
    Entry("solve.material_domain", ("material_id", "axis", "bound", "bound_kind", "source", "message_old", "t", "gap"),
          "물질 '{material_id}' 이(가) 값을 내지 않았다 — 축 {axis}, 종류 {bound_kind}, 도달값 {bound} (출처 {source})"),
    Entry("solve.unlocated_discontinuity", ("h", "h_min", "m_at", "err_norm", "rejected_in_row"),
          "걸음이 h_min {h_min} 밑으로 줄었는데 그 자리(m {m_at})에 찾은 경계가 없다 — 오차 {err_norm}, 연속 기각 {rejected_in_row}"),
    Entry("solve.event_chatter", ("event_name", "count", "cap_name", "cap_value"),
          "경계 사건 '{event_name}' 이(가) {count} 번 되풀이돼 {cap_name} {cap_value} 에 걸렸다", optional=("g", "tol")),
    Entry("solve.layer_order", ("layer_id", "rule", "expected", "got_m", "got_r"),
          "층 '{layer_id}' 의 경계({rule})가 순서를 어긴다 — 기대 {expected}, 실제 m {got_m} · r {got_r}"),
    Entry("solve.closure_discontinuous", ("check", "F_root", "tol_F", "n_acc", "rtol", "bracket", "probes"),
          "닫힘 잔차가 근 x {x} 에서 연속이 아니다 ({check}) — F {F_root}, 허용 {tol_F}, 마지막 괄호 {bracket}, 탐침 {probes}",
          preamble="잔차가 끊긴 자리에 근이 걸려 답을 믿을 수 없다."),
    Entry("solve.material_record", ("material_id", "p", "t", "refusal", "why"),
          "물질 기록 '{material_id}' 이(가) ({p} Pa, {t} K) 에서 답하지 않는다 — {refusal}: {why}"),
    Entry("solve.melting_not_in_phase2", ("material_id", "boundary", "p", "t"),
          "물질 기록 '{material_id}' 의 녹는 경계 {boundary} 에 닿았다 ({p} Pa, {t} K) — 위상 2 는 녹음을 건너지 않는다 (D-P3)"),
    Entry("solve.lid_unconverged", ("layer_id", "trail", "iters", "tol"),
          "전도층 '{layer_id}' 바닥 온도가 {iters} 번 안에 {tol} 로 닫히지 않았다 — 자취 {trail}"),
    Entry("solve.basal_unconverged", ("layer_id", "trail", "iters", "tol"),
          "기저층 '{layer_id}' 의 반지름 고정점이 {iters} 번 안에 {tol} 로 닫히지 않았다 — 자취 {trail}"),
    Entry("solve.basal_not_attached", ("layer_id", "crossings", "n_crossings"),
          "기저층 '{layer_id}' 이(가) 아래 층에 붙지 않는다 — 건넘 {n_crossings} 번 {crossings}"),
    # phase-1 design note 17 §6: a value that is not a finite number (the residual F at a trial, or the integrated state)
    Entry("solve.non_finite", ("where_kind", "value"),
          "수가 아닌 값이 나왔다 ({where_kind}) — {value}"),
    # note 17 §6 (G1-R-07): an event's g undefined at a secant iterate (its curve absent there), not a cap tripping
    Entry("solve.event_undefined", ("event_name",),
          "경계 사건 '{event_name}' 의 함수가 착지 탐색 중 정의되지 않았다 (곡선이 그 자리에 없다)"),
)

#: Input refusals (A7: D-A7-1..5, D-A2-7). `where` names the file and key, e.g. «mars.yaml:inputs.mass_earth».
_INPUT = (
    Entry("input.unreadable", ("path", "error"), "파일 '{path}' 을(를) 읽지 못했다 — {error}"),
    Entry("input.empty", ("path",), "파일 '{path}' 이(가) 비어 있다"),
    Entry("input.not_mapping", ("path", "got_type"), "파일 '{path}' 의 최상위가 사전이 아니라 {got_type} 이다"),
    Entry("input.duplicate_key", ("key", "line"), "키 '{key}' 가 {line} 번째 줄에서 한 번 더 나온다"),
    Entry("input.zero_extent", ("layer_id", "kind", "value"),
          "층 '{layer_id}' 의 범위 {kind} = {value} 는 0 이다 — 없는 층은 목록에서 빼서 선언한다"),
    Entry("input.param_not_for_material", ("layer_id", "key", "material"),
          "층 '{layer_id}' 의 params 키 '{key}' 는 물질 '{material}' 에 쓰지 않는다"),
    Entry("input.extent_overdetermined", ("interface", "sources"),
          "경계 '{interface}' 를 정하는 선언이 둘 이상이다 — {sources}"),
    Entry("input.extent_order", ("layers", "values"),
          "선언된 범위가 바깥으로 갈수록 단조롭지 않다 — {layers}: {values}"),
    Entry("input.role_material_class", ("layer_id", "role", "material", "material_class"),
          "층 '{layer_id}' 의 역할 '{role}' 과 물질 '{material}'({material_class}) 이 맞지 않는다 — 외피 무리는 압력 바닥이 있는 "
          "물질만, 그런 물질은 외피 무리에만 (R-LAYERGEN-2)"),
    Entry("input.jump_at_lithosphere", ("boundary", "why"),
          "경계 '{boundary}' 의 온도 도약은 받지 않는다 — {why} (R-LITHO-7)"),
    Entry("input.unknown_key", ("key", "nearest"), "모르는 키 '{key}' — 가장 가까운 키 '{nearest}'"),
    Entry("input.missing_key", ("key",), "필요한 키 '{key}' 가 없다"),
    Entry("input.null_value", ("key",), "키 '{key}' 의 값이 null 이다 — 없는 값은 키를 빼서 나타낸다"),
    Entry("input.not_number", ("key", "got"), "키 '{key}' 의 값 {got} 이(가) 수가 아니다"),
    Entry("input.not_boolean", ("key", "got"), "키 '{key}' 의 값 {got} 이(가) true/false 가 아니다"),
    Entry("input.not_text", ("key", "got"), "키 '{key}' 의 값 {got} 이(가) 글이 아니다"),
    Entry("input.not_in_vocabulary", ("key", "got", "allowed"), "키 '{key}' 의 값 {got} 이(가) 허용 목록 {allowed} 밖이다"),
    Entry("input.non_finite", ("key", "got"), "키 '{key}' 의 값 {got} 이(가) 유한한 수가 아니다"),
    Entry("input.out_of_domain", ("key", "value", "domain"), "키 '{key}' 의 값 {value} 이(가) 범위 {domain} 밖이다"),
    Entry("input.value_missing", ("key",), "키 '{key}' 의 블록에 value 가 없다 — 선언이 조용히 빠지지 않게 거절한다"),
    Entry("input.provenance_missing", ("key", "fields"), "키 '{key}' 의 출처 칸 {fields} 이(가) 비었다"),
    Entry("input.bad_grade", ("key", "grade", "allowed"), "키 '{key}' 의 등급 '{grade}' 이(가) 입력 등급 {allowed} 밖이다"),
    Entry("input.unit_mismatch", ("key", "got", "expected"), "키 '{key}' 의 단위 '{got}' 이(가) 스키마 단위 '{expected}' 와 다르다"),
    Entry("input.closure_count", ("count", "free"), "풀 미지수가 하나여야 하는데 {count} 개다 — {free}"),
    Entry("input.layer_order", ("pair", "rule"), "층 순서가 규칙을 어긴다 — {pair}: {rule}"),
    Entry("input.duplicate_layer_id", ("layer_id",), "층 id '{layer_id}' 가 두 번 나온다"),
    Entry("input.unknown_material", ("layer_id", "material"), "층 '{layer_id}' 의 물질 '{material}' 을(를) 물질 목록에서 찾지 못했다"),
    Entry("input.material_record_unavailable", ("layer_id", "material_id", "load_stop", "detail"),
          "층 '{layer_id}' 의 물질 기록 '{material_id}' 을(를) 쓸 수 없다 — {load_stop}: {detail} (옛 물질로 돌아가지 "
          "않는다, switch-over §1)"),
    Entry("input.material_registry", ("load_stop", "detail"),
          "물질 레지스트리가 열리지 않았다 — {load_stop}: {detail} (반쯤 열린 레지스트리로는 풀지 않는다, switch-over §1)"),
    Entry("input.declared_grade_not_wired", ("layer_id", "material_id"),
          "층 '{layer_id}' 의 물질 기록 '{material_id}' 에 사용자 선언 출처가 있다 — 등급 «declared» 전파가 아직 없다 "
          "(switch-over note 3)"),
    Entry("input.unknown_role", ("layer_id", "role"), "층 '{layer_id}' 의 역할 '{role}' 이(가) 역할 사전에 없다"),
    Entry("input.extent_invalid", ("layer_id", "why"), "층 '{layer_id}' 의 범위 선언이 맞지 않는다 — {why}"),
    Entry("input.mass_fraction_sum", ("total", "tol"), "질량 몫의 합 {total} 이(가) 1 에서 허용 {tol} 보다 멀다"),
    Entry("input.thickness_above_pattern", ("layer_id", "ref"),
          "층 '{layer_id}' 의 thickness_above('{ref}') 는 핵 바로 위 기저층 꼴에서만 받는다"),
    Entry("input.jump_boundary", ("boundary", "known"), "온도 점프의 경계 '{boundary}' 가 이 층 목록에 없다 — 있는 경계 {known}"),
    Entry("input.composition_window", ("layer_id", "component", "value", "window", "source"),
          "층 '{layer_id}' 의 조성 {component} = {value} 이(가) 물질 창 {window} 밖이다 — 출처 {source}"),
    Entry("input.composition_system", ("layer_id", "system", "known"),
          "층 '{layer_id}' 의 조성 체계 '{system}' 가 체계 목록에 없다 — 있는 것 {known}"),
    Entry("input.composition_component", ("layer_id", "system", "component", "known"),
          "층 '{layer_id}' 의 조성 성분 '{component}' 가 '{system}' 체계의 목록 밖이다 — 있는 것 {known}"),
    Entry("input.composition_missing", ("layer_id", "system", "missing"),
          "층 '{layer_id}' 의 '{system}' 조성에 꼭 있어야 할 성분 {missing} 가 없다"),
    Entry("input.composition_sum", ("layer_id", "system", "total", "target", "tolerance", "unit"),
          "층 '{layer_id}' 의 '{system}' 조성 합 {total} {unit} 이(가) {target} ± {tolerance} 밖이다"),
    Entry("input.composition_fraction", ("layer_id", "component", "value", "why"),
          "층 '{layer_id}' 의 조성 {component} = {value} 이(가) 맞지 않는다 — {why}"),
    Entry("input.source_kind", ("layer_id", "source_kind", "why"),
          "층 '{layer_id}' 조성의 출처 종류 '{source_kind}' 를 받을 수 없다 — {why}"),
    Entry("input.source_kind_not_built", ("layer_id", "source_kind"),
          "층 '{layer_id}' 조성의 출처 종류 '{source_kind}' 는 아직 만들지 않았다 (phase-2 note 1, (c))"),
    Entry("input.deviation", ("layer_id", "why"), "층 '{layer_id}' 조성의 편차 선언이 맞지 않는다 — {why}"),
    Entry("input.cross_field", ("rule", "detail"), "선언 사이가 맞지 않는다 — {rule}: {detail}"),
    Entry("input.duplicate_name", ("name", "paths"), "천체 이름 '{name}' 이(가) 여러 파일에 있다 — {paths}"),
    Entry("input.v1_unmapped", ("key", "detail"), "옛 꼴(v1) 키 '{key}' 에 층 목록 뜻이 없다 — {detail}"),
    Entry("input.composition_undeclared", ("body_class", "looked_for"),
          "조성이 선언되지 않았다 — {looked_for} 가 없고, '{body_class}' 는 반지름으로 조성을 역산할 수 있는 무리가 아니다. 선언이 필요하다"),
    Entry("input.class_out_of_scope", ("body_class", "why"), "'{body_class}' 는 이 내부구조 솔버 밖이다 — {why}"),
)

#: Chain-node refusals (rewrite/nodes/node-contract.frozen.md §2, prereg-t-eq-stellar.frozen.md §1). Their own group,
#: kept apart from _SOLVE / _INPUT so other additions do not interleave (c8, 2026-10-14). `where` names the node run.
_NODE = (
    Entry("node.out_of_domain", ("input", "value", "bound", "bound_kind"),
          "입력 '{input}' 값 {value} 이(가) 노드의 적용 범위 밖이다 — {bound_kind} {bound}"),
    Entry("node.input_missing", ("input", "from"), "입력 '{input}' 이(가) 없다 — '{from}' 이(가) 값을 내지 않았다"),
    Entry("node.source_not_cached", ("bibcode", "why", "outputs"),
          "출력 {outputs} 이(가) 캐시에 없는 논문 {bibcode} 에 기댄다 — {why}"),
    Entry("node.undeclared_read", ("key",), "노드가 명세에 없는 입력 '{key}' 을(를) 읽었다"),
    Entry("node.record_not_measured", ("file", "key", "method"),
          "기록 {file}:{key} 의 방법 '{method}' 은(는) 관측이 아니다 — 측정값으로 읽지 않는다"),
)

#: NoAnswer evidence sets (D-A3-2). `unconverged`: b9's set; GridExceeded maps to MAX_STEPS_SOLVE (r2 N3).
#: NODE_ITERATE_PASSES: `iterate.max_passes` of a chain node on a cycle (node-contract.frozen.md §3). Appended at the end.
NO_ANSWER_BUDGETS = ("CLOSE_ITERS", "MAX_STEPS_SOLVE", "WALL_SHOTS", "MAX_SPLITS", "NODE_ITERATE_PASSES")
_NO_ANSWER = (
    Entry("unconverged", ("budget_name", "budget_value", "last_residual"),
          "예산 {budget_name} = {budget_value} 안에 닫히지 않았다 — 마지막 잔차 {last_residual} (값 아님)",
          optional=("x", "pass_kind", "state", "scan", "m_at", "first_attempt")),
    Entry("span_too_long", ("t_lo", "t_hi", "width", "bound"),
          "[{t_lo}, {t_hi}] 폭 {width} 이(가) 잇기 한도 {bound} 보다 길어 빈 칸으로 둔다"),
)


def _index(entries: tuple) -> MappingProxyType:
    out = {}
    for e in entries:
        if e.id in out:
            raise ValueError(f"refusal id {e.id!r} registered twice")
        out[e.id] = e
    return MappingProxyType(out)


#: Phase-1 note 13 §3: refusals that a pass always reaches carry `state` (the last accepted node), required. Kinds
#: that may also fire before any pass (layer_order) keep it optional; a pass-time one fills it.
STATE_REQUIRED = ("solve.material_domain", "solve.material_record", "solve.melting_not_in_phase2",
                  "solve.event_chatter", "solve.unlocated_discontinuity", "solve.lid_unconverged",
                  "solve.basal_unconverged", "solve.closure_discontinuous")


def _solve_entry(e):
    req = e.id in STATE_REQUIRED
    return Entry(e.id, SOLVE_COMMON + e.fields + (("state",) if req else ()), e.template,
                 tuple(f for f in SOLVE_OPTIONAL if not (req and f == "state")) + e.optional, e.preamble, solve=True)


REGISTRY = _index(tuple(_solve_entry(e) for e in _SOLVE) + _INPUT + _NODE)
NO_ANSWER_REGISTRY = _index(_NO_ANSWER)
if tuple(NO_ANSWER_REGISTRY) != NO_ANSWER_REASONS:      # not an assert: it must hold under python -O too
    raise ImportError("NoAnswer registry and NO_ANSWER_REASONS disagree")


def _check_fields(e: Entry, evidence: dict) -> None:
    missing = [f for f in e.fields if f not in evidence]
    extra = [f for f in evidence if f not in e.fields and f not in e.optional]
    if missing or extra:
        raise ValueError(f"{e.id}: evidence fields missing {missing}, undeclared {extra}")


def render(e: Entry, where: str, evidence: dict) -> str:
    body = e.template.format(where=where, **evidence)
    return f"{e.preamble} {body}" if e.preamble else body


def _check_vocab(e: Entry, ev: dict) -> None:
    if "pass_kind" in ev and ev["pass_kind"] not in PASS_KINDS:
        raise ValueError(f"{e.id}: pass_kind {ev['pass_kind']!r} not in {PASS_KINDS}")
    if e.solve and ev["closure_kind"] not in CLOSURE_KINDS:
        raise ValueError(f"{e.id}: closure_kind {ev['closure_kind']!r} not in {CLOSURE_KINDS}")
    if e.id == "solve.event_chatter" and ev["cap_name"] not in EVENT_CAPS:
        raise ValueError(f"{e.id}: cap_name {ev['cap_name']!r} not in {EVENT_CAPS}")
    if e.id == "unconverged" and ev["budget_name"] not in NO_ANSWER_BUDGETS:
        raise ValueError(f"unconverged: budget_name {ev['budget_name']!r} not in {NO_ANSWER_BUDGETS}")
    for w in ev.get("walls") or ():
        if not isinstance(w, dict) or set(w) != set(WALL_FIELDS):
            raise ValueError(f"{e.id}: a wall is {{{', '.join(WALL_FIELDS)}}}, got {w!r}")
        if w["outcome_kind"] not in ("refusal", "no_answer") or not isinstance(w["located"], bool):
            raise ValueError(f"{e.id}: bad wall {w!r}")


def make(id: str, where: str, at: Where | None = None, **evidence) -> Refusal:
    """A `Refusal` of a registered id. Unknown ids, missing or undeclared fields and out-of-vocabulary values raise
    (a bug, not a refusal)."""
    e = REGISTRY.get(id)
    if e is None:
        raise ValueError(f"unregistered refusal id {id!r}")
    _check_fields(e, evidence)
    _check_vocab(e, evidence)
    return Refusal(id=id, where=where, evidence=evidence, text=render(e, where, evidence), at=at)


def no_answer(reason: str, where: str, at: Where | None = None, **evidence) -> NoAnswer:
    """A `NoAnswer` of a registered reason, with the same checks as `make`."""
    e = NO_ANSWER_REGISTRY.get(reason)
    if e is None:
        raise ValueError(f"unregistered no-answer reason {reason!r}")
    _check_fields(e, evidence)
    _check_vocab(e, evidence)
    return NoAnswer(reason=reason, where=where, evidence=evidence, text=render(e, where, evidence), at=at)
