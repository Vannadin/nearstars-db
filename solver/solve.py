# 풀이 입구 — Body 하나를 겉에서 안쪽으로 층마다 적분하고, 자유 변수 하나를 중심 잔차로 닫아 Answer/Refusal/NoAnswer 를 낸다 (설계 §A1)
"""`solve(body, options, warm) -> (Outcome, warm)`: the only public entry of the phase-1 solver.

Frozen design: rewrite/phase1-design.frozen.md §A1, §A6, §X; registration rewrite/phase1-a1-impl.frozen.md S7
with notes 1–2. The body comes validated (c8's `validate` / `from_v1`); the solver never reads yaml.

One trial x of the closure scalar = one inward pass through every layer, top to bottom:
- R = x for closure «R», else the declared radius; a boundary_mass closure sets that layer's mass fraction to x.
- a `conductive` top layer is the lid (lid.py); every other layer is an adiabatic segment (rhs + stepper + events);
- a layer ends at the top of the layer below: a radius_from_centre value (event in r), a mass level when every layer
  below (or every layer above) is mass-declared, or the base of a depth_from_surface layer above;
- same-material boundaries are still step ends (note 2 item 5); a declared temperature jump is added at its
  boundary, inner side hotter;
- the pass ends at m_ε or at the r floor; F is the centre residual (rhs.residual).
A refusing trial is a wall of the closure scan (closure.py); only a refusal at the root, or when nothing solves,
is the outcome.
"""
from __future__ import annotations

import dataclasses
import math
from dataclasses import dataclass, field

from solver import closure as cl
from solver import context, events, legacy_materials as lm, lid, refusals, result, rhs
from solver import fixed_grid
from solver import stepper as st


@dataclass
class PassOut:
    F: float | None
    m: float
    y: tuple
    rho_end: float
    stop: st.Stop | None
    boundaries: list = field(default_factory=list)      # (name, kind, m, r, p, t_upper, t_lower)
    profiles: dict = field(default_factory=dict)        # layer id → path tuple
    graze: object = None
    floor_end: bool = False
    entered: list = field(default_factory=list)          # layer ids the pass integrated, top to bottom
    events: list = field(default_factory=list)           # every landed event name, in order (phase, seam, onset, …)
    counters: dict = field(default_factory=dict)
    R: float = 0.0
    r_scale: float = 0.0


def _value(d):
    return getattr(d, "value", d)


def _radius_of(body, x):
    return x if body.closure.kind == "R" else float(_value(body.radius))


def _fractions(body, x):
    out = {}
    for l in body.layers:
        if body.closure.kind == "boundary_mass" and l.id == body.closure.layer:
            out[l.id] = x
        elif l.extent is not None and l.extent.kind == "mass_fraction":
            out[l.id] = l.extent.value
    return out


def _top_of(body, j, x, R):
    """('r', radius) or ('m', mass) at the top of layer j (index from the centre)."""
    layers, M = body.layers, body.mass
    lj = layers[j]
    if lj.extent is not None and lj.extent.kind == "radius_from_centre":
        return ("r", lj.extent.value)
    fr = _fractions(body, x)
    below = layers[:j + 1]
    if all(l.id in fr for l in below):
        return ("m", M * sum(fr[l.id] for l in below))
    above = layers[j + 1:]
    if above and all(l.id in fr for l in above):
        return ("m", M * (1.0 - sum(fr[l.id] for l in above)))
    if j + 1 < len(layers) and layers[j + 1].extent is not None \
            and layers[j + 1].extent.kind == "depth_from_surface":
        return ("r", R - layers[j + 1].extent.value)
    return None


def _jump(body, lower, upper):
    name = f"{lower.id}/{upper.id}"
    b = next((b for b in body.boundaries if b.name == name), None)
    for key in (name, getattr(b, "interface", None)):
        if key and key in body.jumps:
            return float(_value(body.jumps[key]))
    return 0.0


def _segment(view, mass, m0, y0, end, r_scale, opt, monitor, extra_events=()):
    """One adiabatic layer from (m0, y0) down to `end` (('m', m) | ('r', r) | None for the centre)."""
    evs = [st.Event("r_floor", lambda m, y: y[0] - opt.r_floor_frac * r_scale, scale=r_scale)]
    m_end = opt.eps * mass
    if end is not None and end[0] == "r":
        evs.append(st.Event("layer_end", (lambda m, y, rr=end[1]: y[0] - rr), scale=r_scale))
    elif end is not None:
        m_end = end[1]
    evs += events.layer_events(view.mat, getattr(view, "p_stop", 0.0)) + list(extra_events)
    if opt.fixed_dr > 0.0:
        r_end, name = (end[1], "layer_end") if end is not None and end[0] == "r" else \
            (opt.r_floor_frac * r_scale, "r_floor")
        return fixed_grid.run_r(rhs.make_rhs(view), m0, y0, m_end, r_end, name, opt.fixed_dr, evs[1:] if
                                end is None or end[0] != "r" else evs[2:], on_accept=monitor,
                                max_steps=opt.max_steps_solve, event_min_progress=opt.event_min_progress * r_scale,
                                event_restarts_step=opt.event_restarts_step,
                                event_restarts_run=opt.event_restarts_solve, m_scale=mass)
    sopt = st.Options(rtol=opt.rtol, floors=rhs.floors(mass, r_scale), h0=1e-3 * mass, h_min=1e-15 * mass,
                      h_max=mass / 20.0, max_steps=opt.max_steps_solve,
                      event_min_progress=opt.event_min_progress * mass,
                      event_restarts_step=opt.event_restarts_step, event_restarts_run=opt.event_restarts_solve,
                      event_rewalks=opt.event_rewalks,
                      h_cap=None if getattr(view, "mat", None) is None else events.step_cap(view.mat))
    return st.run(rhs.make_rhs(view), m0, y0, m_end, sopt, evs, on_accept=monitor)


def inward(body, views, x, opt: context.Options) -> PassOut | st.Stop:
    M = body.mass
    R = _radius_of(body, x)
    rho_mean = 3.0 * M / (4.0 * math.pi * R ** 3)
    rs = rhs.r_scale_of(M, rho_mean)
    sf = body.surface
    top_view = views[body.layers[-1].id]
    p_s = sf.p_s if sf.p_s is not None else (top_view.p_floor or 0.0)
    t_pot = sf.t_pot or 0.0
    out = PassOut(None, M, (), float("nan"), None, R=R, r_scale=rs)
    layers = body.layers
    m, y = M, (R, p_s, t_pot, t_pot, 0.0, 0.0)
    start = len(layers) - 1
    if layers[-1].thermal == "conductive":
        lt = layers[-1]
        got = lid.lid_pass(views[lt.id], M, R, lt.extent.value, p_s, sf.t_s, t_pot, rs,
                           rhs.PassOptions(rtol=opt.rtol, eps=opt.eps, r_floor_frac=opt.r_floor_frac,
                                           max_steps=opt.max_steps_solve,
                                           event_min_progress=opt.event_min_progress, fixed_dr=opt.fixed_dr,
                                           event_rewalks=opt.event_rewalks),
                           lid_iters=opt.lid_iters, lid_t_tol=opt.lid_t_tol, layer_id=lt.id,
                           events=events.layer_events(views[lt.id].mat, getattr(views[lt.id], "p_stop", 0.0))
                           if getattr(views[lt.id], "mat", None) is not None else ())
        if isinstance(got, st.Stop):
            return got
        m, y = got.m, got.y
        out.entered.append(lt.id)
        out.profiles[lt.id] = got.path
        for k, v in got.counters.items():
            out.counters[k] = out.counters.get(k, 0) + v
        start = len(layers) - 2
        if start >= 0:
            out.boundaries.append((f"{layers[start].id}/{lt.id}", "layer", m, y[0], y[1], y[3], y[3]))
    graze_mon = None
    for j in range(start, -1, -1):
        layer = layers[j]
        view = views[layer.id]
        end = _top_of(body, j - 1, x, R) if j > 0 else None
        if j > 0 and end is None:
            return st.Stop("layer_order", {"layer_id": layer.id, "rule": "end", "expected": "a determinable base",
                                           "got_m": m, "got_r": y[0]})
        if end is not None and end[0] == "m" and end[1] >= m:
            return st.Stop("layer_order", {"layer_id": layer.id, "rule": "mass_fraction",
                                           "expected": f"base mass {end[1]:.6g} below the top {m:.6g}",
                                           "got_m": m, "got_r": y[0]})
        graze_mon = events.GrazeMonitor(view.mat, getattr(view, "p_stop", 0.0))
        out.entered.append(layer.id)
        res = _segment(view, M, m, y, end, rs, opt, graze_mon)
        out.profiles[layer.id] = res.path
        out.events += [e[0] for e in res.events]
        if graze_mon.best is not None and (out.graze is None or abs(graze_mon.best.g) < abs(out.graze.g)):
            out.graze = graze_mon.best
        for k, v in vars(res.counters).items():
            out.counters[k] = out.counters.get(k, 0) + v
        kind = res.stop.kind
        if kind not in ("end", "event"):
            return res.stop
        m, y = res.x, res.y
        if kind == "event" and res.event == "r_floor":
            out.floor_end = True
            break
        # the base is reached at its radius event, or at its mass level (x1); reaching the centre end (m_ε) while
        # waiting for a radius event is not the base (that layer below is then never entered)
        reached = (kind == "event" and res.event == "layer_end") or (kind == "end" and end is not None
                                                                      and end[0] == "m")
        if j > 0 and not reached:
            break                                 # the pass reached the centre end before this layer's base
        if j > 0:
            below = layers[j - 1]
            jump = _jump(body, below, layer)
            out.boundaries.append((f"{below.id}/{layer.id}", "layer", m, y[0], y[1], y[3], y[3] + jump))
            if jump:
                y = (y[0], y[1], y[2] + jump, y[3] + jump, *y[4:])
    bottom = views[layers[0].id]
    got = bottom.state(y[1], y[2], None)
    if isinstance(got, st.Stop):
        return got
    out.m, out.y, out.rho_end = m, y, got[0]
    out.F = rhs.residual(m, y[0], got[0], rs)
    return out


def _comp(layer) -> dict:
    v = getattr(layer.composition, "value", None) if layer.composition is not None else None
    return dict(v) if v is not None else {}


def _param(layer, name):
    v = (layer.params or {}).get(name)
    return getattr(v, "value", v)


def _view_for(body, layer, x, p_stop):
    """One layer's view; `x` is the closure value when the closure acts on this layer (note 5 item 3a). Returns a view,
    or (None, why) for a material the adapter cannot build."""
    t_pot = body.surface.t_pot or 0.0
    on_me = body.closure.kind == "composition" and body.closure.layer == layer.id
    if layer.material == "fe_core_light":                       # note 5 item 3b
        comp = _comp(layer)
        if on_me and body.closure.name != "S":
            return None, ("closure_axis", f"fe_core_light fits S only, not {body.closure.name!r}")
        o, c = comp.get("O"), comp.get("C")
        if not isinstance(o, (int, float)) or not isinstance(c, (int, float)):
            return None, ("core_light_elements", "fe_core_light needs declared O and C (no silent 0)")
        if not any(v["O"] == o and v["C"] == c for v in lm.interior.LIGHT_ELEMENT_PINS.values()):
            return None, ("core_light_elements", f"O {o}, C {c} is not one of the old engine's box ends "
                                                 f"{dict(lm.interior.LIGHT_ELEMENT_PINS)}")
        s = x if on_me else comp.get("S")
        if not isinstance(s, (int, float)):
            return None, ("core_light_elements", "core S neither declared nor the closure axis")
        mat = lm.build_fe_core_light(float(s), float(o), float(c))
        return lm.LegacyView(mat.name, mat, t_pot, p_stop), None
    if layer.material == "silicate_decl":                      # note 5 item 3c
        if on_me:
            return None, ("closure_axis", "silicate_decl has no fit axis in phase 1")
        mat, why = lm.build_silicate_decl(_comp(layer))
        if mat is None:
            return None, ("unknown_material", why)
        return lm.LegacyView("silicate_decl", mat, t_pot, p_stop), None
    if layer.material == lm.BASAL_CONST:                       # r2 S10 B1: the basal layer's thermal base
        rho = _param(layer, "density")
        if rho is None:
            return None, ("unknown_material", "silicate_basal_const needs params.density")
        decl = next((l for l in body.layers if l.material == "silicate_decl"), None)
        base = lm.interior.MATERIALS["silicate"]
        if decl is not None:                                    # the old run built it inside the `_mantle` swap
            base, why = lm.build_silicate_decl(_comp(decl))
            if base is None:
                return None, ("unknown_material", why)
        return lm.LegacyView(lm.BASAL_CONST, lm.interior.BasalConstDensity(float(rho), base=base), t_pot,
                             p_stop), None
    if on_me and body.closure.name == "initial_porosity":      # note 5 item 3d (Dante)
        mat = lm.interior.MATERIALS.get(layer.material)
        if mat is None or layer.material in lm.NOT_PORTED or lm._has_water(mat):
            return None, ("unknown_material", "not in the phase-1 adapter")
        cap = _param(layer, "porosity_p_cap")
        return lm.LegacyView(layer.material, mat, t_pot, p_stop, phi0=float(x),
                             p_cap=None if cap is None else float(cap)), None
    if on_me:
        return None, ("closure_axis", f"no fit axis {body.closure.name!r} on material {layer.material!r}")
    v = lm.resolve(layer, t_pot, p_stop)
    return (v, None) if v is not None else (None, ("unknown_material", "not in the phase-1 adapter"))


def _p_stop(body) -> float:
    top = lm.interior.MATERIALS.get(body.layers[-1].material)
    return (getattr(top, "p_floor", 0.0) or 0.0) if top is not None else 0.0


def _views(body, x=None):
    out = {}
    p_stop = _p_stop(body)
    for l in body.layers:
        on_closure = body.closure.kind == "composition" and body.closure.layer == l.id
        v, fail = _view_for(body, l, body.closure.lo if (on_closure and x is None) else x, p_stop)
        if v is None:                                # fail = (typed kind, detail text); only the kind is read
            kind_, detail = fail
            where = f"{body.name}.layers.{l.id}"
            if kind_ == "unknown_material":
                return refusals.make("input.unknown_material", where, layer_id=l.id, material=l.material)
            return refusals.make("input.cross_field", where, rule=kind_, detail=detail)
        out[l.id] = v
    return out


def _views_at(body, views, x):
    """The views for trial x: only the closure's own layer is rebuilt (composition closure)."""
    if body.closure.kind != "composition":
        return views
    layer = next(l for l in body.layers if l.id == body.closure.layer)
    if hasattr(views.get(layer.id), "at"):           # a fixture view that knows its own x-dependence
        return {**views, layer.id: views[layer.id].at(x)}
    v, why = _view_for(body, layer, x, _p_stop(body))
    if v is None:
        raise RuntimeError(f"closure layer view failed at trial {x!r} after it built at lo: {why}")
    return {**views, layer.id: v}


def _state(y, m):
    return {"m": m, "r": y[0], "P": y[1], "T": y[3]} if y else None


def _to_refusal(stop: st.Stop, where: str, x, kind: str, pass_kind: str):
    common = {"x": x, "closure_kind": kind, "pass_kind": pass_kind}
    rec = stop.record
    if stop.kind == "refused" and isinstance(rec, st.Stop):
        stop, rec = rec, rec.record
    if isinstance(rec, lm.MaterialRefusal):
        return refusals.make("solve.material_domain", where, material_id=rec.material_id, axis="P",
                             bound=rec.p, bound_kind="table_edge", source="engine/eos.py (097a8aa3)",
                             message_old=rec.message_old, **common)
    if stop.kind == "chatter":
        return refusals.make("solve.event_chatter", where, event_name=rec["event"], count=rec["count"],
                             cap_name=rec["cap_name"], cap_value=rec["cap_value"], **common)
    if stop.kind == "h_min":
        return refusals.make("solve.unlocated_discontinuity", where, h=rec["h"], h_min=rec["h_min"],
                             m_at=rec["m_at"], err_norm=rec["err_norm"], rejected_in_row=rec["rejected_in_row"],
                             **common)
    if stop.kind == "lid_unconverged":
        return refusals.make("solve.lid_unconverged", where, layer_id=rec["layer_id"], trail=list(rec["trail"]),
                             iters=rec["iters"], tol=rec["tol"], **common)
    if stop.kind == "lid_input":
        if rec["field"] == "surface_temperature_k":
            return refusals.make("input.missing_key", where, key="surface_temperature_k")
        return refusals.make("input.extent_invalid", where, layer_id=rec["layer_id"],
                             why=f"conductive layer depth {rec['value']!r} must lie in (0, R) (R-LITHO-6)")
    if stop.kind == "lid_base_not_reached":
        return refusals.make("solve.layer_order", where, layer_id=rec["layer_id"], rule="depth_from_surface",
                             expected="the lid base reached before the centre end", got_m=rec["m"],
                             got_r=float("nan"), **common)
    if stop.kind == "layer_order":
        return refusals.make("solve.layer_order", where, **rec, **common)
    if stop.kind == "max_steps":
        return refusals.no_answer("unconverged", where, budget_name="MAX_STEPS_SOLVE",
                                  budget_value=rec["budget"], last_residual=None, x=x, pass_kind=pass_kind)
    # an unmapped stop kind is a bug in this mapping, not a refusal (design A3: exceptions mean bugs only; r2 S7)
    raise RuntimeError(f"unmapped solver stop {stop.kind!r}: {rec!r}")


def _quantities(body, p: PassOut, sid: str, x, views=None):
    M, R = body.mass, p.R
    prov = result.Provenance("judgment", result.SolverInfo(sid, counters=tuple(sorted(p.counters.items()))),
                             consumed_observations=(("radius",) if body.closure.kind != "R" else ()))

    def q(key, unit, val, where):
        return result.Quantity(key, unit, val, "exact", "direct", where, prov, band_reason=result.BAND_NOT_MEASURED)
    body_w = result.Where("body")
    m_e, (r_e, p_e, tad_e, t_e, i_e, v_pore) = p.m, p.y
    p_c = p_e + 2.0 * math.pi / 3.0 * rhs.G * p.rho_end ** 2 * r_e ** 2       # constant-density centre series
    i_tot = i_e + 0.4 * m_e * r_e ** 2
    has_t = body.surface.t_pot is not None       # no declared T_pot: no temperature path, no T quantities (c8)
    if views is not None and any(getattr(v, "phi0", 0.0) > 0.0 for v in views.values()):
        out_bp = v_pore / (4.0 / 3.0 * math.pi * R ** 3)       # comparator rulings 225888af A7 (Dante); V_p in the state
    else:
        out_bp = None
    out = [q("radius", "m", R, body_w), q("nmoi", "1", i_tot / (M * R * R), body_w),
           q("core_pressure", "Pa", p_c, body_w)]
    if has_t:
        out.append(q("core_temperature", "K", t_e, body_w))
    basal = next((l for l in body.layers if l.role == "basal_layer"), None)
    if basal is not None:                             # note 5 item 3g (R-C100-9/10 as the located layer)
        r_base = next((b[3] for b in p.boundaries if b[0].endswith(f"/{basal.id}")), None)
        r_top = next((b[3] for b in p.boundaries if b[0].startswith(f"{basal.id}/")), None)
        if r_base is not None and r_top is not None:
            out += [q("basal_layer_thickness_km", "km", (r_top - r_base) / 1e3, result.Where("layer", basal.id)),
                    q("core_plus_layer_radius_solved_km", "km", r_top / 1e3, result.Where("layer", basal.id))]
    cmb = body.interface("cmb")
    for name, _k, m_b, r_b, p_b, t_up, t_lo in p.boundaries:
        if cmb is not None and name == cmb.name:
            bw = result.Where("boundary", cmb.name, "upper")
            out += [q("core_radius", "m", r_b, bw), q("cmb_pressure", "Pa", p_b, bw),
                    q("core_mass_fraction", "1", m_b / M, body_w),
                    q("core_radius_fraction", "1", r_b / R, body_w)]        # comparator rulings 225888af A3
            if has_t:
                out.append(q("cmb_temperature", "K", t_up, bw))
    if out_bp is not None:
        out.append(q("bulk_porosity", "1", out_bp, body_w))
    return tuple(out)


def _not_yet(body):
    """(rule, detail) for a declaration phase 1 does not implement, else None (r2 S7 B2/B3). Each is a named
    refusal until its step lands, never a silent misreading."""
    for i, l in enumerate(body.layers):
        if l.thermal == "isothermal":
            return ("thermal_isothermal_not_in_phase1",
                    f"layer '{l.id}' declares an isothermal profile; phase 1 integrates adiabatic layers and one "
                    "conductive top lid only")
        if l.extent is not None and l.extent.kind == "thickness_above":
            return ("thickness_above_not_in_phase1",
                    f"layer '{l.id}' is bounded by thickness_above('{l.extent.ref}'); §A1.6's basal fixed point is "
                    "not implemented in phase 1 (A1 impl note 7)")
        if l.thermal == "conductive" and i != len(body.layers) - 1:
            return ("conductive_not_top", f"layer '{l.id}' is conductive but not the top layer")
        if l.thermal == "conductive" and (l.extent is None or l.extent.kind != "depth_from_surface"):
            return ("conductive_extent", f"the conductive top layer '{l.id}' must be bounded by depth_from_surface")
    return None


def _canonical(body) -> dict:
    """The Body as plain, ordered data for solve_id: repr of every field, which is deterministic for the frozen types
    (mappingproxies keep insertion order)."""
    return {"repr": repr(body)}


def _material_bytes(views) -> bytes:
    """«Material data bytes» of solve_id: the adapter's record of engine modules and data files read
    (`legacy_materials.material_bytes`), plus each layer's view id and material id; a fixture view without a material
    contributes its repr."""
    import hashlib
    h = hashlib.sha256(lm.material_bytes())
    for lid in sorted(views):
        v = views[lid]
        h.update(lid.encode())
        if getattr(v, "mat", None) is None:
            h.update(repr(vars(v)).encode())
    return h.digest()


SENSITIVE_KEYS = ("core_temperature", "cmb_temperature", "radius")


def _with_sensitivity(body, views, x, opt, acc, qs, supplied=False, ctx=None):
    """Note 5 item 3f: one warm solve at T_pot + δ (δ = opt.sensitivity_dt), forward differences d q / d T_pot on
    SENSITIVE_KEYS. Omitted, with a note, when the located-boundary set changes between the two states (r2) or the
    warm solve does not answer."""
    dt = opt.sensitivity_dt
    b2 = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=body.surface.t_pot + dt))
    v2 = dict(views) if supplied else _views(b2, x)
    if isinstance(v2, result.Refusal):
        return qs, result.Note("sensitivity_not_measured", "the T_pot + δ views could not be built", {"dt": dt})

    def F2(xx):
        vx = _views_at(b2, v2, xx)
        if isinstance(vx, st.Stop):
            return vx
        got = inward(b2, vx, xx, opt)
        return got if isinstance(got, st.Stop) else got.F
    span = 1e-2 * abs(x) if x else 1e-3
    lo, hi = max(b2.closure.lo, x - span), min(b2.closure.hi, x + span)
    out = cl.solve_scalar(F2, lo, hi, 5)
    if out.kind != "root":
        out = cl.solve_scalar(F2, b2.closure.lo, b2.closure.hi, opt.n_scan)
    if out.kind != "root":
        return qs, result.Note("sensitivity_not_measured", f"the T_pot + δ solve gave {out.kind}", {"dt": dt})
    x2 = out.roots[0]
    if ctx is not None:
        for t in out.trials:
            ctx.record("sensitivity_" + t.kind, x=t.x, F=t.F, stop=None if t.stop is None else t.stop.kind)
    acc2 = inward(b2, _views_at(b2, v2, x2), x2, opt)
    if isinstance(acc2, st.Stop):
        return qs, result.Note("sensitivity_not_measured", f"the T_pot + δ pass stopped: {acc2.kind}", {"dt": dt})
    names1 = [b[0] for b in acc.boundaries] + acc.events
    names2 = [b[0] for b in acc2.boundaries] + acc2.events
    if names1 != names2 or (acc.graze is None) != (acc2.graze is None):
        return qs, result.Note("sensitivity_across_boundary_change", "the located-boundary set differs at T_pot + δ",
                               {"dt": dt, "at": names1, "at_plus": names2})
    q2 = {q.key: q.point for q in _quantities(b2, acc2, "", x2)}
    new = []
    for q in qs:
        if q.key in SENSITIVE_KEYS and q.key in q2 and not (q.key == "radius" and body.closure.kind != "R"):
            new.append(dataclasses.replace(q, sensitivity=(q2[q.key] - q.point) / dt))
        else:
            new.append(q)
    return tuple(new), None


def _regions(out) -> list:
    """Solved stretches of the scan, split at every refusing trial."""
    regs, cur = [], []
    for t in sorted(out.trials, key=lambda t: t.x):
        if t.F is None:
            if cur:
                regs.append([cur[0], cur[-1]])
            cur = []
        else:
            cur.append(t.x)
    if cur:
        regs.append([cur[0], cur[-1]])
    return regs


PROBE_SPAN = 50.0           # phase-1 design notes 8–9: δ = PROBE_SPAN·tol_F/s, so a side's chord s·2δ = 100·tol_F


def _root_tolerance(x, acc, options, bracket, trials) -> dict:
    """Phase-1 design notes 8–10 at the root x, in the closure's own variable (any closure kind).
    tol_F = 3·N_acc·rtol + 2·s·tol_x: 3·N_acc·rtol bounds the accepted pass's integration error in
    F = (r³ − …)/r_s³ with r_s = R (rho_mean is the bulk density at the pass's R, so r ≤ r_s and each accepted step
    moves r³/r_s³ by at most 3·rtol); 2·s·tol_x is Brent's stop bracket times the slope s.
    s is the secant of the points around the root: on each side, inside its solved stretch, the nearest scan point (a
    scan point at x itself is skipped), else the farthest solved trial (note 11). Note 10: a sign-change bracket can be a hair wide (a Brent or wall trial next to
    a scan point), where noise sets its secant and δ collapsed below the noise (Mars member at rtol/10, δ 5.5e-5 m).
    δ = PROBE_SPAN·tol_F/s, capped at an eighth of the scan pair's width."""
    scan = sorted((t.x, t.F) for t in trials if t.kind == "scan" and t.F is not None)
    solved = sorted((t.x, t.F) for t in trials if t.F is not None)
    refused = sorted(t.x for t in trials if t.F is None and t.kind != "isolated")

    def inside(q, sgn):
        """q lies on that side of x inside its solved stretch: no refused trial between q and x (r2 GB1, GB2). Every
        consumer of the solve's trials (the slope's points and each side's reference) goes through it."""
        wall = min((w for w in refused if (w - x) * sgn > 0.0), key=lambda w: abs(w - x), default=None)
        return (q[0] - x) * sgn > 0.0 and (wall is None or abs(q[0] - x) < abs(wall - x))

    def side_point(sgn):
        """Inside that side's solved stretch: the nearest scan point; with none, the farthest solved trial; so the
        secant never rests on a hair-wide pair nor spans a wall."""
        sc = [q for q in scan if inside(q, sgn)]
        if sc:
            return min(sc, key=lambda q: abs(q[0] - x))
        stretch = [q for q in solved if inside(q, sgn)]
        return max(stretch, key=lambda q: abs(q[0] - x)) if stretch else None

    lo_pt, hi_pt = side_point(-1.0), side_point(1.0)
    if lo_pt is None or hi_pt is None:                 # one side has no solved trial: the secant from x to the other
        lo_pt, hi_pt = (lo_pt or (x, acc.F)), (hi_pt or (x, acc.F))
    (xa, fa), (xb, fb) = lo_pt, hi_pt
    s = abs(fb - fa) / abs(xb - xa) if xb != xa else 0.0
    tol_x = 2.0 * 2.2e-16 * abs(x) + 0.5 * cl.CLOSE_TOL * abs(x)
    tol_f = 3.0 * acc.counters.get("accepted", 0) * options.rtol + 2.0 * s * tol_x
    # a probe that leaves the solved stretch (a wall within 2δ) refuses the solve by design (r2 on 55117864 (b))
    cap = 0.125 * abs(xb - xa)
    delta = min(PROBE_SPAN * tol_f / s, cap) if s > 0.0 else cap
    # each side's reference point: the nearest solved trial at least 4δ off the root inside that side's solved
    # stretch (r2 GB2: never beyond a wall); none → the side refuses «no_solved_reference»
    off = [q for q in solved if abs(q[0] - x) >= 4.0 * delta]
    left = [q for q in off if inside(q, -1.0)]
    right = [q for q in off if inside(q, 1.0)]
    far = (left[-1] if left else None, right[0] if right else None)
    return {"tol_F": tol_f, "s": s, "delta": delta, "far": far}


def _side_check(F, x, f_root, side, rt) -> dict:
    """Phase-1 design note 9 (a″): one side of the root, both sides always (the rule, not the result, picks them).
    F at x + side·δ and x + side·2δ must lie on one line through F(x*) within 2·tol_F + ½·|F″_side|·δ², F″_side the
    second divided difference over (the side's reference point, x + side·2δ, x*), the reference being the nearest
    solved trial at least 4δ off the root on that side; the chord's slope must have the sign of the secant from x* to
    that point. A side with no solved trial is refused by name (its probes are not anchored). F has a slope change at its root by construction (the m_ε end for F > 0, the
    r-floor event for F < 0; rhs.residual), so a chord never straddles it."""
    d = rt["delta"]
    x1, x2 = x + side * d, x + side * 2.0 * d
    f1, f2 = cl._value(F, x1), cl._value(F, x2)
    out = {"side": side, "x1": x1, "x2": x2, "F1": None if isinstance(f1, st.Stop) else f1,
           "F2": None if isinstance(f2, st.Stop) else f2,
           "stop": next((z.kind for z in (f1, f2) if isinstance(z, st.Stop)), None)}
    if out["stop"] is not None:
        out["ok"] = False
        return out
    ref = rt["far"][1 if side > 0 else 0]
    if ref is None:
        out.update(ok=False, stop="no_solved_reference")
        return out
    xe, fe = ref
    curv = abs(2.0 * ((fe - f2) / (xe - x2) - (f2 - f_root) / (x2 - x)) / (xe - x))
    out["deviation"] = abs(f1 - 0.5 * (f_root + f2))
    out["allowed"] = 2.0 * rt["tol_F"] + 0.5 * curv * d * d
    secant = (fe - f_root) / (xe - x)
    out["ok"] = out["deviation"] <= out["allowed"] and (f2 - f_root) / (x2 - x) * secant > 0.0
    return out


def solve(body, options: context.Options = context.Options(), warm=None, views=None):
    """Returns (Outcome, warm). Outcome is result.Answer, result.Refusal or result.NoAnswer.
    `views` (layer id → material view) replaces the adapter's resolution; it exists for physics fixtures only and is
    not reachable from Body, options or the context."""
    where = f"{body.name}.solve"
    nyi = _not_yet(body)                              # r2 S7 B2/B3: refuse by name what phase 1 does not implement
    if nyi is not None:
        return refusals.make("input.cross_field", where, rule=nyi[0], detail=nyi[1]), warm
    supplied = views is not None
    if views is None:
        lm.reset_engine_state()                      # reset before any material is touched (r2 S7)
        views = _views(body)
    else:
        views = dict(views)
    if isinstance(views, result.Refusal):
        return views, warm
    ctx = context.build(options, views, warm,
                        reset_legacy=any(isinstance(v, lm.LegacyView) for v in views.values()))
    kind = body.closure.kind

    views_all = views                                 # F keeps the unbound views: the probes run after `views` is bound to x*

    def F(x):
        vx = _views_at(body, views_all, x)
        if isinstance(vx, st.Stop):
            return vx
        got = inward(body, vx, x, options)
        if isinstance(got, st.Stop):
            return got
        return got.F if got.F is not None else st.Stop("no_residual", {"x": x})

    out = cl.solve_scalar(F, body.closure.lo, body.closure.hi, options.n_scan)
    for t in out.trials:                              # design §A1.5: passes tagged scan / wall / brent
        ctx.record(t.kind, x=t.x, F=t.F, stop=None if t.stop is None else t.stop.kind)
    unlocated = [w for w in out.walls if not w.located]
    if out.kind in ("no_bracket", "no_solved") and unlocated:
        # note 2 item 8: a wall whose position WALL_SHOTS could not fix leaves the search incomplete
        return refusals.no_answer("unconverged", where, budget_name="WALL_SHOTS", budget_value=cl.WALL_SHOTS,
                                  last_residual=None, x=unlocated[0].x, pass_kind="wall"), warm
    if out.kind == "root":
        x = out.roots[0]
        for v in views.values():                      # count only the accepted pass's fallbacks (M1)
            if hasattr(v, "surface_fallbacks"):
                v.surface_fallbacks = 0
        views = _views_at(body, views, x)
        acc = inward(body, views, x, options)
        ctx.record("accepted", x=x, F=getattr(acc, "F", None), stop=getattr(acc, "kind", None))
        if not isinstance(acc, st.Stop):
            missing = [l.id for l in body.layers if l.id not in acc.entered]
            if missing:
                # r2 (note 3): at x* every declared layer must have been entered; a residual of 0 reached with a
                # layer never entered is a structurally wrong answer, refused by name
                lyr = missing[-1]
                return refusals.make("solve.layer_order", where, layer_id=lyr, rule="entered",
                                     expected="every declared layer entered at the root", got_m=acc.m,
                                     got_r=acc.y[0], x=x, closure_kind=kind, pass_kind="accepted"), x
        acc_fb = sum(getattr(v, "surface_fallbacks", 0) for v in views.values())
        if not isinstance(acc, st.Stop):
            acc.counters["surface_rho0_fallbacks"] = acc_fb
        if isinstance(acc, st.Stop):
            return _to_refusal(acc, where, x, kind, "accepted"), x
        guard = options.fixed_dr <= 0.0 and x in out.detail.get("brackets", {})   # a fixed grid has no rtol
        if guard:
            bracket = out.detail["brackets"][x]
            rt = _root_tolerance(x, acc, options, bracket, out.trials)
            tol_f = rt["tol_F"]
            if not abs(acc.F) <= tol_f:                  # note 8 (a): the root closed on a jump of F
                return refusals.make("solve.closure_discontinuous", where, x=x, closure_kind=kind,
                                     pass_kind="accepted", check="residual", F_root=acc.F, tol_F=tol_f,
                                     n_acc=acc.counters.get("accepted", 0), rtol=options.rtol,
                                     bracket=bracket["final"], probes=None), x
        notes = []
        if not guard and options.fixed_dr <= 0.0:       # r2 on 55117864 (a): never skipped silently
            notes.append(result.Note("closure_guard_skipped", "the root has no sign-change bracket (a solved point with "
                                     "F = 0), so phase-1 design notes 8–9's residual and probe checks did not run",
                                     {"x": x}))
        if acc.floor_end:
            notes.append(result.Note("centre_closed_at_floor", "the accepted pass ended at the r floor, not at m_ε",
                                     {"m_end_over_M": acc.m / body.mass, "r_floor_over_r_scale": options.r_floor_frac}))
        if acc.graze is not None:
            g = acc.graze
            notes.append(result.Note("graze", "an onset curve is grazed", {"curve": g.curve, "material": g.material,
                                                                         "p": g.p, "g": g.g}))
        lbs = tuple(result.LocatedBoundary(n, k, m_b, r_b, p_b, t_up) for n, k, m_b, r_b, p_b, t_up, _t in
                    acc.boundaries)
        if body.surface.t_pot is None:
            notes.append(result.Note("no_temperature_path", "no potential temperature is declared, so the structure "
                                     "has no temperature path and no temperature quantity is emitted", {}))
        profiles = {lid: {"m": tuple(n[0] for n in path), "r": tuple(n[1][0] for n in path),
                          "P": tuple(n[1][1] for n in path),
                          **({"T": tuple(n[1][3] for n in path)} if body.surface.t_pot is not None else {})}
                    for lid, path in acc.profiles.items()}
        # solve_id after the accepted pass, so every data file the solve opened is in the material bytes
        sid = context.solve_id_of(_canonical(body), _material_bytes(views), options)
        qs = _quantities(body, acc, sid, x, views)
        if body.surface.t_pot is not None and options.sensitivity_dt > 0.0:
            qs, sens_note = _with_sensitivity(body, views, x, options, acc, qs, supplied=supplied, ctx=ctx)
            if sens_note is not None:
                notes.append(sens_note)
        if guard:                                        # note 9 (a″): one-sided chords on both sides of x*
            sides = [_side_check(F, x, acc.F, -1.0, rt), _side_check(F, x, acc.F, 1.0, rt)]
            for sd in sides:
                for xx, ff in ((sd["x1"], sd["F1"]), (sd["x2"], sd["F2"])):
                    ctx.record("probe", x=xx, F=ff, stop=sd["stop"])
            if not all(sd["ok"] for sd in sides):
                # phase-1 design note 12 (directing): a probabilistic detector with false positives never refuses;
                # its finding rides on the answer by name, with each side's deviation / allowed
                ratios = [sd["deviation"] / sd["allowed"] for sd in sides if sd.get("deviation") is not None]
                notes.append(result.Note(
                    "closure_probe_disclosure", "the local probe found F off one line beside the root (phase-1 "
                    "design notes 9, 12): the root may sit on a shifted level of a jagged F; the answer stands, "
                    "disclosed", {"x": x, "delta": rt["delta"], "dev_ratio": max(ratios) if ratios else None,
                                  "sides": [{k: sd.get(k) for k in ("side", "stop", "deviation", "allowed", "ok")}
                                            for sd in sides]}))
        ans = result.Answer(qs, lbs, profiles, (), tuple(notes))
        return ans, x
    if out.kind == "two_roots":
        return refusals.make("solve.two_roots", where, x=None, closure_kind=kind, pass_kind="scan",
                             roots=list(out.roots), F_scan=[[t.x, t.F] for t in out.trials if t.F is not None],
                             n_scan=options.n_scan), warm
    if out.kind == "unconverged":
        budget = out.detail.get("budget", "CLOSE_ITERS")
        value = cl.MAX_SPLITS if budget == "MAX_SPLITS" else cl.CLOSE_ITERS
        last = next((t.F for t in reversed(out.trials) if t.F is not None), None)
        return refusals.no_answer("unconverged", where, budget_name=budget, budget_value=value,
                                  last_residual=last), warm
    walls = []
    for w in out.walls:
        mapped = _to_refusal(w.stop, where, w.x, kind, "wall")
        is_na = isinstance(mapped, result.NoAnswer)
        walls.append({"x": w.x, "outcome_kind": "no_answer" if is_na else "refusal",
                      "id_or_reason": mapped.reason if is_na else mapped.id, "state": None, "located": w.located})
    if out.kind == "no_solved":
        first = min(out.trials, key=lambda t: t.x)
        return _to_refusal(first.stop, where, first.x, kind, "scan"), warm
    solved = sorted((t for t in out.trials if t.F is not None), key=lambda t: t.x)
    return refusals.make("solve.no_bracket", where, x=None, closure_kind=kind, pass_kind="scan",
                         x_lo=body.closure.lo, x_hi=body.closure.hi, F_lo=solved[0].F, F_hi=solved[-1].F,
                         n_scan=options.n_scan, walls=walls, solved_regions=_regions(out)), warm
