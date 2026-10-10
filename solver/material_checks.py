# 물질 기록 검산식 — 기록의 상수와 상태로만 계산하는 작은 문법; 검산(formula_check)과 띠 오차 식(method)을 평가 (phase-2 impl note 3 C4)
"""The formula-check grammar (rewrite/phase2-impl.frozen.md note 3 C4: «a small grammar the checker evaluates: the
record's constants, the view's quantities and arithmetic; no step depends on a model reading the paper»).

An expression is arithmetic (+ − × ÷ **, unary −, numbers, parentheses), `max`/`min`/`abs`, and names:
- a name from the check's `state` (e.g. T, T0, P, rho);
- a record constant by a path inside the phase: `pressure.alpha_k`, `sets[0].c_v`, `sets[1].t_ref`,
  `params.k0`, `reference.t`, or `sets[1].evaluator.v0`;
- a bare constant name (`alpha_k`) only when exactly one constant in the phase has that name; otherwise
  `material.check_ambiguous` names the candidates, so a reader never has to guess which one was meant.
Two view functions read a thermal set at a state and compare it with a printed value:
`gamma_spread(sets[i] @ P=…, T=… ; printed=…)` and `dpdt_spread(…)`, each |X_set(P, T)/printed − 1| (c8's definition).
Nothing else is callable; anything else is `material.check_grammar`.
"""
from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class CheckStop:
    """A check that cannot be evaluated: an id (material.check_grammar | check_ambiguous | check_unknown_name) and why."""
    id: str
    why: str


class _Stop(Exception):
    def __init__(self, id_, why):
        super().__init__(why)
        self.stop = CheckStop(id_, why)


_SPREAD_CALL = "__spread__"
_CURVE_CALL = "__curve__"
_MELT_CALL = "__melt__"
_CURVE = re.compile(r"curve\(\s*boundaries\[(\d+)\]\s*@\s*T\s*=\s*([^)]*)\)")
_MELT = re.compile(r"melt_p\(\s*([A-Za-z_][\w]*)\s*,\s*([A-Za-z_][\w]*)\s*@\s*T\s*=\s*([^)]*)\)")
_SPREAD = re.compile(r"(gamma_spread|dpdt_spread)\(\s*(sets\[\d+\])\s*@\s*([^;]*);\s*printed\s*=\s*([^)]*)\)")
_OPS = MappingProxyType({ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
                         ast.Div: lambda a, b: a / b, ast.Pow: lambda a, b: a ** b})


def _v(c) -> float:
    return float(c["value"]) if isinstance(c, Mapping) else float(c)


def _constants(phase: Mapping) -> dict:
    """Every constant of a phase by its path (the names a check may use)."""
    out = {}
    for k, c in (phase["thermal"].get("pressure") or {}).items():
        out[f"pressure.{k}"] = _v(c)
    for k, c in (phase["eos"].get("params") or {}).items():
        out[f"params.{k}"] = _v(c)
    ref = phase["eos"]["reference"]
    for k in ("p", "t"):
        if k in ref:
            out[f"reference.{k}"] = _v(ref[k])
    for i, s in enumerate(phase["thermal"].get("sets", ())):
        for k, c in (s.get("constants") or {}).items():
            out[f"sets[{i}].{k}"] = _v(c)
        if "t_ref" in s:
            out[f"sets[{i}].t_ref"] = _v(s["t_ref"])
        for k, c in ((s.get("evaluator") or {}).get("params") or {}).items():
            out[f"sets[{i}].evaluator.{k}"] = _v(c)
    return out


def _path(node) -> str | None:
    """`a.b`, `a[0].b`, `a[0].b.c` as the dotted path string, else None."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _path(node.value)
        return None if base is None else f"{base}.{node.attr}"
    if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int):
        base = _path(node.value)
        return None if base is None else f"{base}[{node.slice.value}]"
    return None


class _Eval:
    def __init__(self, consts: dict, state: Mapping, spread=None, record_fns=None):
        self.consts, self.state, self.spread = consts, {k: float(v) for k, v in state.items()}, spread
        self.record_fns = record_fns

    def name(self, p: str) -> float:
        if p in self.state:
            return self.state[p]
        if p in self.consts:
            return self.consts[p]
        hits = [k for k in self.consts if k.rsplit(".", 1)[-1] == p]
        if len(hits) == 1:
            return self.consts[hits[0]]
        if hits:
            raise _Stop("material.check_ambiguous", f"«{p}» could be {sorted(hits)}; write the path")
        raise _Stop("material.check_unknown_name", f"«{p}» is neither a state value nor a constant of the phase")

    def __call__(self, node) -> float:
        if isinstance(node, ast.Expression):
            return self(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            x = _OPS[type(node.op)](self(node.left), self(node.right))
            if not isinstance(x, float) or not math.isfinite(x):          # 68 G3: a complex or non-finite result
                raise _Stop("material.check_grammar", f"«{ast.unparse(node)[:60]}»: arithmetic left the reals")
            return x
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            x = self(node.operand)
            return -x if isinstance(node.op, ast.USub) else x
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
            f = node.func.id
            if f in ("max", "min", "abs"):
                args = [self(a) for a in node.args]
                if (f == "abs" and len(args) != 1) or not args:                # 68 G2: arity
                    raise _Stop("material.check_grammar", f"{f} takes {'one argument' if f == 'abs' else 'arguments'}")
                return {"max": max, "min": min, "abs": abs}[f](*args)
            if f in (_CURVE_CALL, _MELT_CALL):
                if self.record_fns is None:
                    raise _Stop("material.check_grammar", "curve / melt_p need the record's view")
                if f == _CURVE_CALL:
                    return self.record_fns["curve"](node.args[0].value, self(node.args[1]))
                return self.record_fns["melt_p"](node.args[0].value, node.args[1].value, self(node.args[2]))
            if f == _SPREAD_CALL:
                kind_s, set_i = node.args[0].value, node.args[1].value
                if kind_s not in ("gamma_spread", "dpdt_spread"):
                    raise _Stop("material.check_grammar", f"unknown spread {kind_s!r}")
                p, t, printed_v = self(node.args[2]), self(node.args[3]), self(node.args[4])
                if self.spread is None:
                    raise _Stop("material.check_grammar", f"{kind_s} needs a view of the record")
                return self.spread(kind_s, set_i, p, t, printed_v)
        p = _path(node)
        if p is not None:
            return self.name(p)
        raise _Stop("material.check_grammar", f"«{ast.unparse(node)[:60]}» is outside the check grammar")


def _rewrite_spreads(expr: str) -> str:
    """`gamma_spread(sets[1] @ P=a, T=b ; printed=v)` → `_spread("gamma_spread", 1, (a), (b), (v))`."""
    def sub(m):
        kind, s, at, printed = m.group(1), m.group(2), m.group(3), m.group(4)
        kv = dict(x.split("=", 1) for x in (y.strip() for y in at.split(",")) if x)
        if set(kv) != {"P", "T"}:
            raise _Stop("material.check_grammar", f"{kind} takes «@ P=…, T=…», got {at!r}")
        return f'{_SPREAD_CALL}("{kind}", {int(s[5:-1])}, ({kv["P"]}), ({kv["T"]}), ({printed}))'
    for internal in (_SPREAD_CALL, _CURVE_CALL, _MELT_CALL):    # 68 G1: internal calls are not spellable by a record
        if internal in expr:
            raise _Stop("material.check_grammar", f"«{internal}» is internal")
    expr = _CURVE.sub(lambda m: f"{_CURVE_CALL}({int(m.group(1))}, ({m.group(2)}))", expr)
    expr = _MELT.sub(lambda m: f'{_MELT_CALL}("{m.group(1)}", "{m.group(2)}", ({m.group(3)}))', expr)
    return _SPREAD.sub(sub, expr)


def evaluate(expr: str, phase: Mapping, state: Mapping, spread=None, record_fns=None) -> float | CheckStop:
    """The value of `expr` for one phase of a record at `state`, or a CheckStop. `spread(kind, set_index, P, T,
    printed)` evaluates a set at a state (a RecordView supplies it)."""
    try:
        tree = ast.parse(_rewrite_spreads(expr), mode="eval")
        return _Eval(_constants(phase), state, spread, record_fns)(tree)
    except _Stop as s:
        return s.stop
    except SyntaxError as e:
        return CheckStop("material.check_grammar", f"not an expression: {e.msg}")
    except (ZeroDivisionError, OverflowError, ValueError, TypeError) as e:
        return CheckStop("material.check_grammar", f"arithmetic failed: {e}")


def view_spread(view, phase_index: int = 0):
    """The spread functions over a RecordView's phase: |X_set(P, T)/printed − 1| with X = γ or (∂P/∂T)_V."""
    def spread(kind, set_i, p, t, printed):
        s = view.phases[phase_index].sets[set_i]
        if s.evaluator is not None:
            got = s.evaluator.at(p, t)
            x = got["gruneisen"] if kind == "gamma_spread" else got["dpdt_v"]
        else:
            raise _Stop("material.check_grammar", f"{kind} reads an evaluator set; set {set_i} has none")
        return abs(x / printed - 1.0)
    return spread


def view_record_fns(view):
    """curve(boundaries[i] @ T=…) = P_b(T) of a declared curve; melt_p(a, b @ T=…) = the P where gibbs phases a and b
    have equal G at T, bracketed inside both windows (c8: R14-08 verification values as formula checks)."""
    def curve(i, t):
        b = view.record["boundaries"][i]
        pb = view.boundary_pressure(b["curve"], t)
        if pb is None:
            raise _Stop("material.check_grammar", f"boundaries[{i}] is absent at {t:g} K")
        return pb

    def melt_p(a, b, t):
        pa = next((ph for ph in view.phases if ph.id == a), None)
        pb = next((ph for ph in view.phases if ph.id == b), None)
        if pa is None or pb is None or pa.library is None or pb.library is None:
            raise _Stop("material.check_grammar", f"melt_p needs two library phases of the record, got {a}, {b}")
        lo, hi = max(pa.p_min, pb.p_min, 1.0e5), min(pa.p_max, pb.p_max)
        try:
            f = lambda p: pa.library.at(p, t)["g"] - pb.library.at(p, t)["g"]     # noqa: E731
            flo, fhi = f(lo), f(hi)
            if flo * fhi > 0.0:
                raise _Stop("material.check_grammar", f"melt_p: G of {a} and {b} do not cross at {t:g} K in the windows")
            for _ in range(80):
                mid = 0.5 * (lo + hi)
                fm = f(mid)
                if (fm > 0.0) == (flo > 0.0):
                    lo, flo = mid, fm
                else:
                    hi = mid
        except _Stop:
            raise
        except Exception as e:
            raise _Stop("material.check_grammar", f"melt_p could not evaluate: {e}") from e
        return 0.5 * (lo + hi)
    return {"curve": curve, "melt_p": melt_p}


def _disclosure_allowance(bound, fc, phase, state, view, pi):
    """The allowed miss in the check's unit: the bound as given, or a bound in K times |dP/dT| from the record's own
    slope expression at the check's T."""
    if bound["unit"] == fc["unit"]:
        return float(bound["value"])
    if bound["unit"] == "K" and bound.get("slope"):
        slope = evaluate(bound["slope"], phase, state, None if view is None else view_spread(view, pi),
                         None if view is None else view_record_fns(view))
        if isinstance(slope, CheckStop):
            return slope
        return float(bound["value"]) * abs(slope)
    return CheckStop("material.check_grammar", f"disclosure bound in {bound['unit']} needs the check's unit "
                                               f"({fc['unit']}) or K with a slope")


def run_formula_checks(record: Mapping, view=None) -> list:
    """Each formula check of a record: {quantity, got, expected, tolerance, passed} or {quantity, stop}. A check is read
    against the first phase unless its state names `phase` (an index)."""
    out = []
    for fc in record["formula_checks"]:
        state = dict(fc["state"])
        pi = int(state.pop("phase", 0))
        got = evaluate(fc["expression"], record["phases"][pi], state,
                       None if view is None else view_spread(view, pi),
                       None if view is None else view_record_fns(view))
        if isinstance(got, CheckStop):
            out.append({"quantity": fc["quantity"], "stop": got})
            continue
        exp, tol = float(fc["expected"]), float(fc["tolerance"])
        within = abs(got - exp) <= tol
        disc = fc.get("disclosed_fail")
        row = {"quantity": fc["quantity"], "got": got, "expected": exp, "tolerance": tol,
               "within": within, "disclosed": None if disc is None else disc["why"]}
        if disc is None:
            row["passed"] = within
        else:                                               # owner-direction 44ff625: stale, or beyond the bound, fails
            if "bound" not in disc:                         # step 1 of 44ff625: until records carry it (then required)
                row["passed"] = not within
                out.append(row)
                continue
            allowed = _disclosure_allowance(disc["bound"], fc, record["phases"][pi], state, view, pi)
            if isinstance(allowed, CheckStop):
                out.append({"quantity": fc["quantity"], "stop": allowed})
                continue
            row["allowed_miss"] = allowed
            row["passed"] = (not within) and abs(got - exp) <= allowed
        out.append(row)
    return out
