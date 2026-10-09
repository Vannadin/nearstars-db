# 순방향 표 구성원 — 역산 천체(금성·화성)를 선언 상태 답의 조성·경계 질량에 묶고 반지름을 풀어 O9 상태를 옛 표 구성원처럼 품
"""The forward table member of an inverse body, for O9 states (owner-direction «O9 for inverse bodies: compare like for
like», 2026-10-10 ~03:45; registration rewrite/oracle/o9-forward-member-note.md).

The old O4O9 entry-A record is the structure-grid member: a forward solve at the table's s0 composition with the radius
free. The rewrite's counterpart freezes everything the declared-state answer closed and frees R:
- every layer below the outermost gets extent mass_fraction = its mass in the declared answer (from the located
  boundaries), so a boundary_mass closure (Venus's core) and a radius-declared core and basal layer (Mars) both become
  mass levels;
- a composition closure's axis is written into its layer's composition (Mars: S = the declared answer's root);
- the closure becomes R over R_RANGE × the declared answer's radius.

R_RANGE is [0.8, 1.25], not the schema's [0.05, 30] R⊕. A Mars member at 2200 K has a solved window of only
3.56–3.9e6 m: below it the centre runs past the core fit's 350 GPa edge, above it the core fit leaves its pressure range
from below. The schema range's 17 log-spaced points are ×1.49 apart, so every one of them refused and the closure saw
no solved trial. At [0.8, 1.25] the spacing is ×1.028. The member is a perturbation of the declared state: the old O9
radii span 0.951–1.008 (Venus) and 0.998–1.08 (Mars) of the declared radius.
"""
from __future__ import annotations

import dataclasses

from solver import body as bd

R_RANGE = (0.8, 1.25)                  # × the declared answer's radius (see the module note)


def is_inverse(body) -> bool:
    return body.closure.kind != "R"


def member_of(body):
    """(member body, record) for an inverse body with a temperature path, from a fresh declared-state solve
    (sensitivity off); None for a forward body. A declared state that does not answer gives (None, record): its T_pot
    states are then refused by name (run_oracle). No memo here (§A6, r2): a caller that needs it for many states
    solves once and passes the result in."""
    if not is_inverse(body) or body.surface.t_pot is None:
        return None
    from solver import context, result, solve as sv
    a, x = sv.solve(body, context.Options(sensitivity_dt=0.0))
    if not isinstance(a, result.Answer):
        return None, {"declared_outcome": type(a).__name__, "x": None}
    fb = forward_member(body, a, x)
    return fb, {"x": x, "closure": body.closure.kind, "R_range": [fb.closure.lo, fb.closure.hi],
                "fractions": {l.id: l.extent.value for l in fb.layers if l.extent is not None}}


def forward_member(body, answer, x):
    """The forward body at the declared answer (an Answer of `body`, closure root `x`)."""
    top_mass = {}
    for b in answer.boundaries:                      # LocatedBoundary(name «lower/upper», kind, m, r, p, t)
        lower = b.name.split("/")[0]
        top_mass[lower] = b.m
    layers, below = [], 0.0
    for i, l in enumerate(body.layers):
        if i == len(body.layers) - 1:
            layers.append(dataclasses.replace(l, extent=None))
            break
        if l.id not in top_mass:
            raise ValueError(f"{body.name}: the declared answer has no located top for layer {l.id}")
        frac = (top_mass[l.id] - below) / body.mass
        below = top_mass[l.id]
        comp = l.composition
        if body.closure.kind == "composition" and body.closure.layer == l.id:
            comp = dataclasses.replace(comp, value={**dict(comp.value), body.closure.name: float(x)})
        params = dict(l.params)
        if body.closure.kind == "composition" and body.closure.layer == l.id and body.closure.name in params:
            params[body.closure.name] = float(x)
        layers.append(dataclasses.replace(l, extent=bd.Extent("mass_fraction", frac), composition=comp,
                                          params=params))
    r0 = next(q.point for q in answer.quantities if q.key == "radius")
    closure = bd.Closure("R", R_RANGE[0] * r0, R_RANGE[1] * r0)
    return dataclasses.replace(body, layers=tuple(layers), closure=closure)
