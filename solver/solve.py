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

import math
from dataclasses import dataclass, field

from solver import closure as cl
from solver import context, events, legacy_materials as lm, lid, refusals, result, rhs
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
    sopt = st.Options(rtol=opt.rtol, floors=rhs.floors(mass, r_scale), h0=1e-3 * mass, h_min=1e-15 * mass,
                      h_max=mass / 20.0, max_steps=opt.max_steps_solve,
                      event_min_progress=opt.event_min_progress * mass,
                      event_restarts_step=opt.event_restarts_step, event_restarts_run=opt.event_restarts_solve)
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
    m, y = M, (R, p_s, t_pot, t_pot, 0.0)
    start = len(layers) - 1
    if layers[-1].thermal == "conductive":
        lt = layers[-1]
        got = lid.lid_pass(views[lt.id], M, R, lt.extent.value, p_s, sf.t_s, t_pot, rs,
                           rhs.PassOptions(rtol=opt.rtol, eps=opt.eps, r_floor_frac=opt.r_floor_frac,
                                           max_steps=opt.max_steps_solve,
                                           event_min_progress=opt.event_min_progress),
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
                y = (y[0], y[1], y[2] + jump, y[3] + jump, y[4])
    bottom = views[layers[0].id]
    got = bottom.state(y[1], y[2], None)
    if isinstance(got, st.Stop):
        return got
    out.m, out.y, out.rho_end = m, y, got[0]
    out.F = rhs.residual(m, y[0], got[0], rs)
    return out


def _views(body):
    sf = body.surface
    p_stop = 0.0
    top = lm.interior.MATERIALS.get(body.layers[-1].material)
    if top is not None:
        p_stop = getattr(top, "p_floor", 0.0) or 0.0
    out = {}
    for l in body.layers:
        v = lm.resolve(l, sf.t_pot or 0.0, p_stop)
        if v is None:
            return refusals.make("input.unknown_material", f"{body.name}.layers.{l.id}", layer_id=l.id,
                                 material=l.material)
        out[l.id] = v
    return out


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
    if stop.kind == "layer_order":
        return refusals.make("solve.layer_order", where, **rec, **common)
    if stop.kind == "max_steps":
        return refusals.no_answer("unconverged", where, budget_name="MAX_STEPS_SOLVE",
                                  budget_value=rec["budget"], last_residual=None, x=x, pass_kind=pass_kind)
    return refusals.make("solve.material_domain", where, material_id="?", axis="?", bound=float("nan"),
                         bound_kind="unknown", source=stop.kind, message_old=repr(rec), **common)


def _quantities(body, p: PassOut, sid: str, x):
    M, R = body.mass, p.R
    prov = result.Provenance("judgment", result.SolverInfo(sid, counters=tuple(sorted(p.counters.items()))),
                             consumed_observations=(("radius",) if body.closure.kind != "R" else ()))

    def q(key, unit, val, where):
        return result.Quantity(key, unit, val, "exact", "direct", where, prov, band_reason=result.BAND_NOT_MEASURED)
    body_w = result.Where("body")
    m_e, (r_e, p_e, tad_e, t_e, i_e) = p.m, p.y
    p_c = p_e + 2.0 * math.pi / 3.0 * rhs.G * p.rho_end ** 2 * r_e ** 2       # constant-density centre series
    i_tot = i_e + 0.4 * m_e * r_e ** 2
    has_t = body.surface.t_pot is not None       # no declared T_pot: no temperature path, no T quantities (c8)
    out = [q("radius", "m", R, body_w), q("nmoi", "1", i_tot / (M * R * R), body_w),
           q("core_pressure", "Pa", p_c, body_w)]
    if has_t:
        out.append(q("core_temperature", "K", t_e, body_w))
    cmb = body.interface("cmb")
    for name, _k, m_b, r_b, p_b, t_up, t_lo in p.boundaries:
        if cmb is not None and name == cmb.name:
            bw = result.Where("boundary", cmb.name, "upper")
            out += [q("core_radius", "m", r_b, bw), q("cmb_pressure", "Pa", p_b, bw),
                    q("core_mass_fraction", "1", m_b / M, body_w)]
            if has_t:
                out.append(q("cmb_temperature", "K", t_up, bw))
    return tuple(out)


def _not_yet(body):
    """(rule, detail) for a declaration phase 1 does not implement, else None (r2 S7 B2/B3). Each is a named
    refusal until its step lands, never a silent misreading."""
    for i, l in enumerate(body.layers):
        if l.thermal == "isothermal":
            return ("thermal_isothermal_not_in_phase1",
                    f"layer '{l.id}' declares an isothermal profile; phase 1 integrates adiabatic layers and one "
                    "conductive top lid only")
        if l.thermal == "conductive" and i != len(body.layers) - 1:
            return ("conductive_not_top", f"layer '{l.id}' is conductive but not the top layer")
        if l.thermal == "conductive" and (l.extent is None or l.extent.kind != "depth_from_surface"):
            return ("conductive_extent", f"the conductive top layer '{l.id}' must be bounded by depth_from_surface")
    if body.closure.kind == "composition":
        return ("composition_closure_not_yet",
                f"closure on {body.closure.layer}.{body.closure.name} lands with S10 (Mars, Dante)")
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
        h.update(repr(getattr(v, "material_id", type(v).__name__)).encode())
        if getattr(v, "mat", None) is None:
            h.update(repr(vars(v)).encode())
    return h.digest()


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


def solve(body, options: context.Options = context.Options(), warm=None, views=None):
    """Returns (Outcome, warm). Outcome is result.Answer, result.Refusal or result.NoAnswer.
    `views` (layer id → material view) replaces the adapter's resolution; it exists for physics fixtures only and is
    not reachable from Body, options or the context."""
    where = f"{body.name}.solve"
    nyi = _not_yet(body)                              # r2 S7 B2/B3: refuse by name what phase 1 does not implement
    if nyi is not None:
        return refusals.make("input.cross_field", where, rule=nyi[0], detail=nyi[1]), warm
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

    def F(x):
        got = inward(body, views, x, options)
        if isinstance(got, st.Stop):
            return got
        return got.F if got.F is not None else st.Stop("no_residual", {"x": x})

    out = cl.solve_scalar(F, body.closure.lo, body.closure.hi, options.n_scan)
    for t in out.trials:                              # design §A1.5: passes tagged scan / wall / brent
        ctx.record(t.kind, x=t.x, F=t.F, stop=None if t.stop is None else t.stop.kind)
    unlocated = [w for w in out.walls if not w.located]
    if out.kind != "root" and unlocated:
        # note 2 item 8: a wall whose position WALL_SHOTS could not fix leaves the search incomplete
        return refusals.no_answer("unconverged", where, budget_name="WALL_SHOTS", budget_value=cl.WALL_SHOTS,
                                  last_residual=None, x=unlocated[0].x, pass_kind="wall"), warm
    if out.kind == "root":
        x = out.roots[0]
        for v in views.values():                      # count only the accepted pass's fallbacks (M1)
            if hasattr(v, "surface_fallbacks"):
                v.surface_fallbacks = 0
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
        notes = []
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
                          "P": tuple(n[1][1] for n in path), "T": tuple(n[1][3] for n in path)}
                    for lid, path in acc.profiles.items()}
        # solve_id after the accepted pass, so every data file the solve opened is in the material bytes
        sid = context.solve_id_of(_canonical(body), _material_bytes(views), options)
        ans = result.Answer(_quantities(body, acc, sid, x), lbs, profiles, (), tuple(notes))
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
