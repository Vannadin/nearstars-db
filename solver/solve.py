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
from collections.abc import Mapping
import math
from types import MappingProxyType
from dataclasses import dataclass, field

from solver import body as bd
from solver import closure as cl
from solver import context, events, legacy_materials as lm, lid, material_notes, refusals, result, rhs
from solver import material_registry as mr, material_view as mv
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
    band_grazes: list = field(default_factory=list)      # notes 13 §1 / 13a: steps accepted at the band floor
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


def _plan(view):
    """(layer events, step cap) of one view, built once and kept on the view (S1: G1-SP-07, G2-SP-06). A view is built
    per solve (or per trial on a composition closure), so nothing outlives the solve that owns it. Events are frozen
    and their g functions pure; the cap's table constant is per phase. A view that takes no attribute is rebuilt."""
    got = getattr(view, "_s1_plan", None)
    if got is None:
        got = (tuple(events.layer_events(view, getattr(view, "p_stop", 0.0))),
               events.step_cap(getattr(view, "mat", None) or view))
        try:
            view._s1_plan = got
        except (AttributeError, TypeError):
            pass
    return got


def _band(view):
    """Notes 13 §1 / 13a / 13b: the view's band test factory (None without a legacy table phase), kept on the view as
    _plan; each stepper run takes a fresh test from it."""
    got = getattr(view, "_a4_band", None)
    if got is None:
        got = (events.band_check(getattr(view, "mat", None) or view),)
        try:
            view._a4_band = got
        except (AttributeError, TypeError):
            pass
    return got[0]


def _segment(view, mass, m0, y0, end, r_scale, opt, monitor, extra_events=()):
    """One adiabatic layer from (m0, y0) down to `end` (('m', m) | ('r', r) | None for the centre)."""
    evs = [st.Event("r_floor", lambda m, y: y[0] - opt.r_floor_frac * r_scale, scale=r_scale)]
    m_end = opt.eps * mass
    if end is not None and end[0] == "r":
        evs.append(st.Event("layer_end", (lambda m, y, rr=end[1]: y[0] - rr), scale=r_scale))
    elif end is not None:
        m_end = end[1]
    layer_evs, h_cap = _plan(view)
    evs += list(layer_evs) + list(extra_events)
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
                      h_cap=h_cap, step_check=None if _band(view) is None else _band(view)())
    return st.run(rhs.make_rhs(view), m0, y0, m_end, sopt, evs, on_accept=monitor)


def inward(body, views, x, opt: context.Options, want_graze: bool = True) -> PassOut | st.Stop:
    """One pass at closure value x. `want_graze` False skips the graze monitor: a trial pass whose graze record no
    one reads (S1: G2-SP-02, G1-SP-03); the accepted and the sensitivity pass keep it."""
    M = body.mass
    R = _radius_of(body, x)
    rho_mean = 3.0 * M / (4.0 * math.pi * R ** 3)
    rs = rhs.r_scale_of(M, rho_mean)
    sf = body.surface
    top_view = views[body.layers[-1].id]
    if getattr(top_view, "surface_shell", None) is not None:
        # P1R-G1-C-10: §A1.2's analytic shell (ρ(P_s) → 0) exists on rhs.inward_pass, the physics tests' pass only; no
        # phase-1 material has one. Reaching it here is a bug, not a refusal: ρ = 0 would divide by zero in the rhs
        raise NotImplementedError(f"{body.name}: a surface shell (ρ(P_s) = 0) is not implemented in solve.inward")
    p_s = sf.p_s if sf.p_s is not None else (top_view.p_floor or 0.0)
    t_pot = sf.t_pot or 0.0
    out = PassOut(None, M, (), float("nan"), None, R=R, r_scale=rs)
    layers = body.layers
    m, y = M, (R, p_s, t_pot, t_pot, 0.0, 0.0)
    start = len(layers) - 1
    if layers[-1].thermal == "conductive":
        lt = layers[-1]
        lv_ = views[lt.id]
        lid_mat = getattr(lv_, "mat", None)
        got = lid.lid_pass(lv_, M, R, lt.extent.value, p_s, sf.t_s, t_pot, rs,
                           rhs.PassOptions(rtol=opt.rtol, eps=opt.eps, r_floor_frac=opt.r_floor_frac,
                                           max_steps=opt.max_steps_solve,
                                           event_min_progress=opt.event_min_progress, fixed_dr=opt.fixed_dr,
                                           event_rewalks=opt.event_rewalks,
                                           # P1R-G1-C-06: the context's restart caps reach the lid
                                           event_restarts_step=opt.event_restarts_step,
                                           event_restarts_run=opt.event_restarts_solve),
                           lid_iters=opt.lid_iters, lid_t_tol=opt.lid_t_tol, layer_id=lt.id,
                           events=events.layer_events(lv_, getattr(lv_, "p_stop", 0.0)) if lid_mat is not None else (),
                           # G1-C-04: the lid is the mantle material; it takes the same note-12 step cap, read at
                           # the lid's own T, y[3] (note 13a item 4), and the same band test
                           h_cap=events.step_cap(lid_mat, t_index=3) if lid_mat is not None else None,
                           step_check=events.band_check(lid_mat, t_index=3) if lid_mat is not None else None,  # a factory
                           # G1-R-02 = G2-R-01: the lid's landed events and its graze reach the pass record
                           monitor=(lambda: events.GrazeMonitor(lid_mat or lv_, getattr(lv_, "p_stop", 0.0)))
                           if want_graze else None)
        if isinstance(got, st.Stop):
            return _at(got, y, m)                    # a lid stop: the segment's start (note 13 §3)
        m, y = got.m, got.y
        out.entered.append(lt.id)
        out.profiles[lt.id] = got.path
        out.events += [e[0] for e in got.events]
        out.graze = got.graze
        out.band_grazes += list(got.band_grazes)
        for k, v in got.counters.items():                # G2-C-05: the accepted lid pass's steps only enter N_acc
            out.counters[k] = out.counters.get(k, 0) + v
        out.counters["lid_discarded_accepted"] = (got.discarded or {}).get("accepted", 0)   # cost, not tol_F
        start = len(layers) - 2
        if start >= 0:
            out.boundaries.append((f"{layers[start].id}/{lt.id}", "layer", m, y[0], y[1], y[3], y[3]))
    graze_mon = None
    for j in range(start, -1, -1):
        layer = layers[j]
        view = views[layer.id]
        end = _top_of(body, j - 1, x, R) if j > 0 else None
        if j > 0 and end is None:
            return _at(st.Stop("layer_order", {"layer_id": layer.id, "rule": "end", "expected": "a determinable base",
                                           "got_m": m, "got_r": y[0]}), y, m)
        if end is not None and end[0] == "m" and 0.0 < end[1] < opt.eps * M:
            # phase-1 design note 17 §4 (G2-C-12): a mass base strictly inside (0, m_ε) would reverse the next segment;
            # x-dependent on a boundary-mass closure, so at trial level it is a wall in x (as «mass_fraction» is)
            return _at(st.Stop("layer_order", {"layer_id": layer.id, "rule": "base_below_m_eps",
                                           "expected": f"a base mass ≥ m_ε = {opt.eps * M:.6g} or the centre",
                                           "got_m": end[1], "got_r": y[0]}), y, m)
        if end is not None and end[0] == "m" and end[1] >= m:
            return _at(st.Stop("layer_order", {"layer_id": layer.id, "rule": "mass_fraction",
                                           "expected": f"base mass {end[1]:.6g} below the top {m:.6g}",
                                           "got_m": m, "got_r": y[0]}), y, m)
        mat_j = getattr(view, "mat", None) or view
        if not want_graze:
            graze_mon = None
        elif graze_mon is None or getattr(graze_mon.mat, "name", None) != getattr(mat_j, "name", None) \
                or getattr(mat_j, "name", None) is None:
            # P1R-G1-C-09: the old detector cleared its history on a material change only; a same-material layer
            # boundary keeps the three-node window (the best graze so far is kept by the merge below either way)
            graze_mon = events.GrazeMonitor(mat_j, getattr(view, "p_stop", 0.0))
        out.entered.append(layer.id)
        res = _segment(view, M, m, y, end, rs, opt, graze_mon)
        out.profiles[layer.id] = res.path
        out.events += [e[0] for e in res.events]
        out.band_grazes += list(res.band_grazes)
        if graze_mon is not None and graze_mon.best is not None and (out.graze is None
                                                                       or abs(graze_mon.best.g) < abs(out.graze.g)):
            out.graze = graze_mon.best
        for k, v in vars(res.counters).items():
            out.counters[k] = out.counters.get(k, 0) + v
        kind = res.stop.kind
        if kind not in ("end", "event"):
            return _at(res.stop, res.y, res.x)
        m, y = res.x, res.y
        melts = events.melting_events(view)             # D-P3: phase 2 does not cross a melting boundary
        if kind == "event" and res.event in melts:
            return _at(st.Stop("melting_not_in_phase2", {"material_id": getattr(view, "material_id", layer.material),
                                                     "boundary": melts[res.event], "p": res.y[1], "t": res.y[2]}), y, m)
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
    # F's end density (design §A1.5, rhs.residual): one material for every end point, the bottom layer's, so F stays
    # continuous in x where the end switches layer. P1R-G2-C-11 is accepted under that convention (directing ruling R1,
    # 10-13): where the bottom material refuses the end state of a trial that stopped above the bottom layer, the trial
    # is a wall naming that material, and its reached state records the layer the pass ended in (reporting only).
    # Reading the ended layer's view instead (707aa7a4; as a domain-refusal fallback in 785868db) made F jump at the
    # switch: +30–90 % net instructions on Mars 1978–1989 and the cost line at 8/12
    got = views[layers[0].id].state(y[1], y[2], None)
    if isinstance(got, st.Stop):
        stop = _at(got, y, m)
        if out.entered and out.entered[-1] != layers[0].id and stop.state is not None:
            stop = dataclasses.replace(stop, state={**stop.state, "end_layer": out.entered[-1]})
        return stop
    out.m, out.y, out.rho_end = m, y, got[0]
    out.F = rhs.residual(m, y[0], got[0], rs)
    return out


def _comp(layer) -> dict:
    v = getattr(layer.composition, "value", None) if layer.composition is not None else None
    return dict(v) if v is not None else {}


def _param(layer, name):
    v = (layer.params or {}).get(name)
    return getattr(v, "value", v)


def registry_for(body, options, loaded=None):
    """Switch-over §1: the registry for this solve, None when the switch is off or no layer names a record file, or a
    Refusal for a registry-level STOP. `loaded` is a registry (or its LoadStop) the caller loaded once and owns (r2 on
    note 4: one load per run); without it the solve loads its own. Never a module-level cache (A6)."""
    if options.materials == "legacy":
        return None
    names = {f.stem for f in mr.MATERIALS_DIR.glob("*.yaml") if f.name not in mr.NOT_RECORDS}
    if options.silicate_records:                    # silicate registration §4: the silicate routes read records too
        names |= set(SILICATE_ROUTES)
    if not any(l.material in names for l in body.layers):
        return None
    reg = mr.load() if loaded is None else loaded
    if isinstance(reg, mr.LoadStop):
        return refusals.make("input.material_registry", f"{body.name}.materials", load_stop=reg.id,
                             detail=result.plain(dict(reg.evidence)))
    return reg


#: Silicate record registration §4: the layer materials the switch `silicate_records` routes to assemblage records,
#: each with its line. One Option gates all of them together (the map line, the composition-key match, and the
#: `record_composition` lift, which only an assemblage record takes); `silicate_basal_const` is not routed yet (its
#: record, Q6, is built with the basal step) and stays legacy under both settings.
SILICATE_ROUTES = MappingProxyType({
    "silicate": "silicate_slb_default_bse",        # Q-P2 (a) / Q2: no declared composition → default_bse
    "silicate_decl": None,                         # by composition key (material_assemblage.composition_key)
})
#: §4's named legacy line: Dante's porosity fit axis (Q5) keeps legacy silicate until the porosity modifier record.
SILICATE_LEGACY_AXES = ("initial_porosity",)


def _assemblage_view(body, layer, rid, p_stop, registry):
    """(AssemblageView, None) or (None, why) for record `rid` (silicate registration §3; 68 S1–S3)."""
    from solver import material_assemblage as ma
    got = registry.get(rid)
    if got is None or isinstance(got, mr.LoadStop):
        return None, ("record_unavailable", (rid, got if got is not None else mr.LoadStop(
            "material.assemblage_table", MappingProxyType({"file": f"{rid}.yaml", "why": "no such record"}))))
    table = registry.tables[rid]
    if table["boundaries"]["status"] == "pending" and not registry.development:    # 68 S3
        return None, ("record_boundaries_pending", f"the assemblage record {rid!r} has its phase boundaries pending "
                                                   "(registration §3.3); it is read only in development")
    from solver.from_v1 import thaw
    floor = getattr(lm.interior.MATERIALS.get(layer.material), "p_floor", 0.0) or 0.0    # legacy's, by name (§3.1)
    return ma.view(thaw(got), table, body.surface.t_pot or 0.0, p_stop, floor), None


def _silicate_route(body, layer, on_me, p_stop, registry):
    """Silicate registration §4 with the switch on: the assemblage view of a silicate layer, (None, why), or None for
    a layer the routes leave to legacy (Dante's porosity axis; any other material)."""
    from solver import material_assemblage as ma
    if layer.material not in SILICATE_ROUTES:
        return None
    if on_me and body.closure.name in SILICATE_LEGACY_AXES:
        return None
    if layer.material == "silicate" and layer.composition is not None:
        return None                                 # not routed: legacy refuses it first, as when switched off (68 NB)
    if on_me:                                       # an assemblage view has no fit axis: refuse as legacy does (68 B1)
        if layer.material == "silicate_decl":
            return None, ("closure_axis", "silicate_decl has no fit axis in phase 1")
        return None, ("closure_axis", f"no fit axis {body.closure.name!r} on material {layer.material!r}")
    if layer.material == "silicate":
        return _assemblage_view(body, layer, SILICATE_ROUTES["silicate"], p_stop, registry)
    comp = _comp(layer)
    try:
        key = ma.composition_key(comp)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as e:
        return None, ("unknown_material", f"silicate_decl composition has no CFMASNa reduction: {e!r}")
    hits = [rid for rid, r in registry.records.items() if r["kind"] == "assemblage" and r["composition_key"] == key]
    if len(hits) > 1:                                # load refuses this; a hand-built registry must not pick one
        return None, ("composition_key_ambiguous", f"records {sorted(hits)} share composition key {key}")
    if not hits:
        built = sorted(r["composition_key"] for r in registry.records.values() if r["kind"] == "assemblage")
        return None, ("no_table_for_composition", (key, built))
    return _assemblage_view(body, layer, hits[0], p_stop, registry)


def _record_view(body, layer, on_me, p_stop, registry):
    """(view, None), (None, why), or None when the registry holds no record for this layer (legacy resolves it)."""
    rid = layer.material                                      # switch-over step 2: fe_prem reads fe_prem
    got = registry.get(rid)
    if got is None:
        return None
    if isinstance(got, mr.LoadStop):                          # never a fallback to legacy (impl note 1 §6)
        return None, ("record_unavailable", (rid, got))
    if on_me:
        return None, ("closure_axis", f"the record {rid!r} has no fit axis {body.closure.name!r}")
    if got["kind"] == "assemblage":                           # a layer naming an assemblage record directly
        if layer.params:
            return None, ("record_params", f"layer {layer.id!r} declares {sorted(layer.params)} on the record "
                                           f"{rid!r}, which reads none of them")
        return _assemblage_view(body, layer, rid, p_stop, registry)
    if layer.composition is not None:                          # G4-C-01's class on the record path (r2, p1review)
        return None, ("record_composition", f"layer {layer.id!r} declares a composition on the record {rid!r}, "
                                            "which takes none (records with compositions: c8's silicate registration)")
    params = layer.params or {}
    if params:                                                 # a record reads no layer params (68 N69: any key, e.g.
        return None, ("record_params", f"layer {layer.id!r} declares {sorted(params)} on the record {rid!r}, which "
                                       "reads none of them")     # the basal path's density, not porosity only)
    from solver.from_v1 import thaw
    return mv.RecordView(thaw(got), body.surface.t_pot or 0.0, p_stop), None


def _view_for(body, layer, x, p_stop, registry=None, silicate=False):
    """One layer's view; `x` is the closure value when the closure acts on this layer (note 5 item 3a). Returns a view,
    or (None, why) for a material the adapter cannot build. With a registry, a record of the layer's id wins
    (switch-over §1)."""
    t_pot = body.surface.t_pot or 0.0
    on_me = body.closure.kind == "composition" and body.closure.layer == layer.id
    if registry is not None and silicate:             # silicate registration §4, before every other route
        got = _silicate_route(body, layer, on_me, p_stop, registry)
        if got is not None:
            return got
    if registry is not None:
        got = _record_view(body, layer, on_me, p_stop, registry)
        if got is not None:
            return got
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
    if layer.composition is not None:                          # P1R-G4-C-01: only the two builders read one
        return None, ("composition_not_consumed",
                      f"layer '{layer.id}' declares a composition on material {layer.material!r}, which the phase-1 "
                      "adapter builds without one; use fe_core_light (iron_alloy) or silicate_decl (silicate), or a "
                      "material record that takes a composition")
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


def _views(body, x=None, registry=None, silicate=False):
    out = {}
    p_stop = _p_stop(body)
    for l in body.layers:
        on_closure = body.closure.kind == "composition" and body.closure.layer == l.id
        v, fail = _view_for(body, l, body.closure.lo if (on_closure and x is None) else x, p_stop, registry, silicate)
        if v is None:                                # fail = (typed kind, detail text); only the kind is read
            kind_, detail = fail
            where = f"{body.name}.layers.{l.id}"
            if kind_ == "record_unavailable":
                rid, stop = detail
                return refusals.make("input.material_record_unavailable", where, layer_id=l.id, material_id=rid,
                                     load_stop=stop.id, detail=result.plain(dict(stop.evidence)))
            if kind_ == "unknown_material":
                return refusals.make("input.unknown_material", where, layer_id=l.id, material=l.material)
            if kind_ == "no_table_for_composition":
                key, built = detail
                return refusals.make("input.no_table_for_composition", where, layer_id=l.id, composition_key=key,
                                     built_keys=built)
            return refusals.make("input.cross_field", where, rule=kind_, detail=detail)
        out[l.id] = v
    return out


def _views_at(body, views, x):
    """The views for trial x: only the closure's own layer is rebuilt (composition closure). It rebuilds through the
    legacy path (no registry, no silicate switch): safe because no record or assemblage route takes a fit axis —
    `_record_view` and `_silicate_route` refuse one (68 on aa48d1bf). A future route with a fit axis must pass both."""
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


def _at(stop, y, m):
    """The stop with the pass's reached state (phase-1 note 13 §3: the last accepted node), unless it has one."""
    return stop if stop.state is not None else dataclasses.replace(stop, state=_state(y, m))


def _to_refusal(stop: st.Stop, where: str, x, kind: str, pass_kind: str, scan=None):
    common = {"x": x, "closure_kind": kind, "pass_kind": pass_kind}
    if stop.state is not None:                         # phase-1 note 13 §3: the last accepted node
        common["state"] = stop.state
    if scan is not None:                               # no_solved: the scan in the evidence (§A1.5)
        common["scan"] = scan
    rec = stop.record
    if stop.kind == "refused" and isinstance(rec, st.Stop):
        stop, rec = rec, rec.record
    if type(rec).__name__ == "RecordRefusal":            # switch-over §2: a phase-2 record view refuses by its id
        return refusals.make("solve.material_record", where, material_id=rec.material_id, p=rec.p, t=rec.t,
                             refusal=rec.refusal, why=rec.why, **common)
    if stop.kind == "melting_not_in_phase2":
        return refusals.make("solve.melting_not_in_phase2", where, material_id=rec["material_id"],
                             boundary=rec["boundary"], p=rec["p"], t=rec["t"], **common)
    if isinstance(rec, lm.MaterialRefusal):
        # G2-R-03: the axis the engine named; `bound` is the reached value on that axis (the engine does not hand
        # over its limit, which stays in message_old), and `bound_kind` says so
        t_axis = rec.axis == "T"
        if rec.axis == "none":                             # 68 H1: the engine's ValueError channel, no edge named
            bk = "engine_value_error"
        elif t_axis:
            bk = "reached_t_below_floor" if rec.too_cold else "reached_t_above_ceiling"
        else:
            bk = "reached_p_outside_table"
        return refusals.make("solve.material_domain", where, material_id=rec.material_id, axis=rec.axis,
                             bound=rec.t if t_axis else rec.p, bound_kind=bk,
                             source="engine/eos.py (097a8aa3)", message_old=rec.message_old, t=rec.t, gap=rec.kind,
                             **common)
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
    # phase-1 design note 17 §6: the four stops that raised or misreported
    if stop.kind == "no_residual":
        return refusals.make("solve.non_finite", where, where_kind="residual", value=repr(rec.get("value")), **common)
    if stop.kind == "non_finite":
        return refusals.make("solve.non_finite", where, where_kind="state", value=repr(rec.get("y")), **common)
    if stop.kind == "centre_crossed":
        return refusals.make("solve.layer_order", where, layer_id="(pass)", rule="centre_crossed",
                             expected="r > 0 to the centre end", got_m=rec["m"], got_r=rec["r"], **common)
    if stop.kind == "event_undefined":
        return refusals.make("solve.event_undefined", where, event_name=rec["event"], **common)
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
        if l.extent is not None and l.extent.kind == "phase":       # P1R-G4-C-06: accepted at load, no solve branch
            return ("extent_phase_not_in_phase1",
                    f"layer '{l.id}' is bounded by the phase event '{l.extent.ref}'; phase-bounded extents are not "
                    "implemented in phase 1")
    if any(l.thermal == "conductive" for l in body.layers) and body.surface.t_pot is None:
        # phase-1 design note 17 §2b (G1-R-09, closes G4-C-12): R-LITHO-4 anchors the lid's T_ad on T_pot; without it the
        # lid's fixed point targets T_b = 0 and its relative test passes at 0 ≤ 0
        return ("lid_without_t_pot", "a conductive lid is anchored on the potential temperature (R-LITHO-4); this body "
                                     "declares none")
    if body.layers and all(l.thermal == "conductive" for l in body.layers):
        # phase-1 design note 13 §4 (G2-C-04): with no adiabatic layer below the lid, F would be taken at the lid
        # base as if it were the centre
        return ("lid_only_body", "phase 1 integrates the interior below a lid as adiabatic layers; this body declares "
                                 "none")
    if body.closure.kind != "R" and any(l.thermal == "conductive" for l in body.layers):
        # P1R-G4-C-08: owner Q3 / R-LITHO-6, as from_v1 refuses it on the v1 path: an inversion keeps no structural lid
        return ("lid_on_inversion",
                f"a conductive lid on a {body.closure.kind} closure is refused through phase 1 (R-LITHO-6, owner Q3): "
                "it would move the inferred core values")
    return None


def _canonical(body) -> dict:
    """The Body as solve_id binds it: only what the solve reads, as plain data with sorted keys and every number a
    float (P1R-G4-SP-01, with LOWs G4-C-15 and G4-R-11). Values, units and bands of the declarations the solve reads
    enter; grades, sources, notes, counter-evidence, the body's name and the fields the solver never reads
    (declarations, solver_flags, later_tools, surface_declared, notes) do not, so a prose edit keeps the id and an
    int/float spelling or a key order cannot move it."""
    def num(x):
        return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else x

    def plain(x):
        if isinstance(x, Mapping):
            return {str(k): plain(v) for k, v in sorted(x.items(), key=lambda kv: str(kv[0]))}
        if isinstance(x, (list, tuple)):
            return [plain(v) for v in x]
        return num(x)

    def decl(d):
        if d is None:
            return None
        if not isinstance(d, bd.Declared):
            return plain(d)
        return {"value": plain(d.value), "unit": d.unit, "band": plain(d.band), "uncertainty": num(d.uncertainty)}

    sf = body.surface
    return {
        "surface": {"m": num(sf.m), "p_s": num(sf.p_s), "p_s_source": sf.p_s_source, "t_s": num(sf.t_s),
                    "t_pot": num(sf.t_pot)},
        "radius": decl(body.radius),
        "layers": [{"id": l.id, "role": l.role, "material": l.material, "thermal": l.thermal,
                    "t_declared": num(l.t_declared), "system": l.system,
                    "extent": None if l.extent is None else {"kind": l.extent.kind, "value": num(l.extent.value),
                                                            "ref": l.extent.ref},
                    "composition": decl(l.composition),
                    "params": {k: decl(v) for k, v in sorted(l.params.items())}} for l in body.layers],
        "closure": {"kind": body.closure.kind, "lo": num(body.closure.lo), "hi": num(body.closure.hi),
                    "layer": body.closure.layer, "name": body.closure.name},
        "jumps": {k: decl(v) for k, v in sorted(body.jumps.items())},
    }


def _material_bytes(views) -> bytes:
    """«Material data bytes» of solve_id: the adapter's record of engine modules and data files read
    (`legacy_materials.material_bytes`), plus each layer's view id and material id; a fixture view without a material
    contributes its repr; a record view contributes its record as canonical JSON (switch-over note 4)."""
    import hashlib
    import json
    h = hashlib.sha256(lm.material_bytes())
    for lid in sorted(views):
        v = views[lid]
        h.update(lid.encode())
        if getattr(v, "record", None) is not None:      # a record view: its record, canonical (never a repr: addresses)
            h.update(json.dumps(result.plain(v.record), sort_keys=True, separators=(",", ":")).encode())
        elif getattr(v, "mat", None) is None:
            h.update(repr(vars(v)).encode())
    return h.digest()


#: P1R-G2-C-09: declared Options the solve does not read (the closure reads closure.py's constants).
INERT_OPTIONS = ("close_tol", "close_iters", "wall_tol", "wall_shots", "basal_iters", "basal_tol", "band_pass")

SENSITIVE_KEYS = ("core_temperature", "cmb_temperature", "radius")


def _with_sensitivity(body, views, x, opt, acc, qs, supplied=False, ctx=None, registry=None):
    """Note 5 item 3f: one warm solve at T_pot + δ (δ = opt.sensitivity_dt), forward differences d q / d T_pot on
    SENSITIVE_KEYS. Omitted, with a note, when the located-boundary set changes between the two states (r2) or the
    warm solve does not answer."""
    dt = opt.sensitivity_dt
    b2 = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=body.surface.t_pot + dt))
    v2 = dict(views) if supplied else _views(b2, x, registry, opt.silicate_records)
    if isinstance(v2, result.Refusal):
        return qs, result.Note("sensitivity_not_measured", "the T_pot + δ views could not be built", {"dt": dt})

    kept = {}                                         # SR1: the (a″) probe passes, kept while `keep` is on

    def F2(xx):
        vx = _views_at(b2, v2, xx)
        if isinstance(vx, st.Stop):
            return vx
        got = inward(b2, vx, xx, opt, want_graze=False)     # a trial: its graze is never read
        if kept.get("on"):
            kept[xx] = got
        return got if isinstance(got, st.Stop) else got.F
    # phase-1 note 15 §2: start from the root already found; any refusal or no bracket falls back unchanged
    out = cl.refine(F2, x, b2.closure.lo, b2.closure.hi)
    if out is None:
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
    # phase-1 design note 13 §2 (G2-C-03): the sensitivity root gets notes 8/12's checks; a failure omits the
    # sensitivity with its reason (the answer stands), a failing probe side keeps it and discloses
    if any(not w.located for w in out.walls):
        return qs, result.Note("sensitivity_not_measured", "the T_pot + δ scan left a wall unlocated",
                               {"dt": dt, "reason": "unlocated_wall"})
    rt2 = None
    if opt.fixed_dr <= 0.0 and x2 in out.detail.get("brackets", {}):
        rt2 = _root_tolerance(x2, acc2, opt, out.detail["brackets"][x2], out.trials)
        if not abs(acc2.F) <= rt2["tol_F"]:
            return qs, result.Note("sensitivity_not_measured", "the T_pot + δ root closed on a jump of F (note 8 (a))",
                                   {"dt": dt, "reason": "closure_discontinuous", "F": acc2.F, "tol_F": rt2["tol_F"]})
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
    notes = []
    if rt2 is not None:
        kept["on"] = True
        sides = [_side_check(F2, x2, acc2.F, -1.0, rt2, b2.closure.lo, b2.closure.hi),
                 _side_check(F2, x2, acc2.F, 1.0, rt2, b2.closure.lo, b2.closure.hi)]
        kept["on"] = False
        if not all(sd["ok"] for sd in sides):
            ratios = [sd["deviation"] / sd["allowed"] for sd in sides if sd.get("deviation") is not None]
            notes.append(result.Note(
                "sensitivity_probe_disclosure", "the local probe found F off one line beside the T_pot + δ root "
                "(note 13 §2): the sensitivity stands, disclosed",
                {"dt": dt, "x": x2, "delta": rt2["delta"], "dev_ratio": max(ratios) if ratios else None,
                 "sides": [{k: sd.get(k) for k in ("side", "stop", "deviation", "allowed", "ok")} for sd in sides]}))
        if any(q.sensitivity is not None for q in new):
            notes.append(_sensitivity_resolution(b2, x2, acc2, q2, new, dt, rt2, out.trials, sides, kept))
    return tuple(new), (notes or None)


def _sensitivity_resolution(b2, x2, acc2, q2, new, dt, rt2, trials, sides, kept):
    """SR1 (rewrite/sr1-sensitivity-resolution-registration.frozen.md): the sensitivity's root-placement resolution.
    x_res = max(2·tol_F2/s2, E): the guard's constant, and E, the contiguous extent around x2 of the δ-solve's own
    trials and probes with |F| ≤ tol_F2, sign changes among them included (a lower bound, limited by trial density).
    Per key: dq/dx from the + side's nearer probe pass (else the − side's), Δs_q = |dq/dx|·x_res/δ, reported as
    |Δs_q / s_q|. The fixed-x read is not in scope (§5)."""
    tol, s2 = rt2["tol_F"], rt2["s"]
    guard = 2.0 * tol / s2 if s2 > 0.0 else math.inf
    pts = sorted({(t.x, t.F) for t in trials if t.F is not None}
                 | {(sd[k], sd[f]) for sd in sides for k, f in (("x1", "F1"), ("x2", "F2")) if sd.get(f) is not None}
                 | {(x2, acc2.F)})
    i0 = min(range(len(pts)), key=lambda i: abs(pts[i][0] - x2))
    near = lambda i: abs(pts[i][1]) <= tol
    # the contiguous run of near trials (|F| ≤ tol_F2) around x2; a sign change inside the run is part of it, and a
    # crossing between a near trial and a far one is not extended past the near one (E stays a lower bound)
    lo = hi = i0
    while lo > 0 and near(lo - 1):
        lo -= 1
    while hi < len(pts) - 1 and near(hi + 1):
        hi += 1
    extent = pts[hi][0] - pts[lo][0]
    x_res = max(guard, extent)
    side_used, why = None, []
    qp, xp = None, None
    for sd in sorted(sides, key=lambda d: -d["side"]):      # the + side first (registration §2, r2 N1)
        got = kept.get(sd["x1"])
        if got is None or isinstance(got, st.Stop) or sd["x1"] == x2:
            # a stopped or missing probe pass, or a probe step below x2's resolution (δ rounds to 0 at x2)
            why.append(f"side {sd['side']:+.0f}: " + ("probe at x2" if got is not None and sd["x1"] == x2
                                                      else getattr(got, "kind", "not run")))
            continue
        qp = {q.key: q.point for q in _quantities(b2, got, "", sd["x1"])}
        xp, side_used = sd["x1"], sd["side"]
        break
    per_key = {}
    if qp is not None:
        for q in new:
            if q.sensitivity is not None and q.key in qp and q.key in q2 and q.sensitivity != 0.0:
                dqdx = (qp[q.key] - q2[q.key]) / (xp - x2)
                per_key[q.key] = abs(dqdx * x_res / dt / q.sensitivity)
    return result.Note("sensitivity_resolution", "the printed sensitivity's resolution from where the T_pot + δ root "
                       "lands in F's floor crossing set (SR1); the fixed-x read is not included",
                       {"x_res": x_res, "x_res_from": "trials" if extent > guard else "guard", "per_key": per_key,
                        "probe_side": side_used if side_used is not None else "; ".join(why) or None,
                        "scope": "root placement"})


def _regions(out) -> list:
    """Solved stretches of the scan, split at every refusing trial except an isolated one (A1 impl note 8 rule 2: an
    isolated refusal never splits a solved stretch; G2-C-07)."""
    regs, cur = [], []
    for t in sorted((t for t in out.trials if t.kind != "isolated"), key=lambda t: t.x):
        if t.F is None:
            if cur:
                regs.append([cur[0], cur[-1]])
            cur = []
        else:
            cur.append(t.x)
    if cur:
        regs.append([cur[0], cur[-1]])
    return regs


def _straddled_wall(out):
    """G2-R-04: the located wall between two solved neighbours whose F have opposite signs, else None. The root then lies
    inside the refusing stretch, so that wall's refusal is the outcome, not «F does not change sign»."""
    order = sorted((t for t in out.trials if t.kind != "isolated"), key=lambda t: t.x)
    solved = [t for t in order if t.F is not None]
    for a, b in zip(solved, solved[1:]):
        if a.F * b.F < 0.0 and any(a.x < t.x < b.x and t.F is None for t in order):
            inside = [w for w in out.walls if a.x <= w.x <= b.x]
            if inside:
                return min(inside, key=lambda w: w.x)
    return None


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


def _side_check(F, x, f_root, side, rt, lo=-math.inf, hi=math.inf) -> dict:
    """Phase-1 design note 9 (a″): one side of the root, both sides always (the rule, not the result, picks them).
    F at x + side·δ and x + side·2δ must lie on one line through F(x*) within 2·tol_F + ½·|F″_side|·δ², F″_side the
    second divided difference over (the side's reference point, x + side·2δ, x*), the reference being the nearest
    solved trial at least 4δ off the root on that side; the chord's slope must have the sign of the secant from x* to
    that point. A side with no solved trial is refused by name (its probes are not anchored). F has a slope change at its root by construction (the m_ε end for F > 0, the
    r-floor event for F < 0; rhs.residual), so a chord never straddles it."""
    d = rt["delta"]
    x1, x2 = x + side * d, x + side * 2.0 * d
    if not (lo <= x2 <= hi):                           # P1R-G2-R-10: a probe off the closure range is not taken
        return {"side": side, "x1": x1, "x2": x2, "F1": None, "F2": None, "stop": "outside_range", "ok": False}
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


#: Phase-1 design note 18 (draft): the accepted root failing note 8's residual check is re-closed once with the whole
#: solve at rtol / CLOSURE_RETRY_RTOL_DIV before it is refused (Mars 1773 K at the melt knee, 10-14)
CLOSURE_RETRY_RTOL_DIV = 10.0


#: Owner F12 ruling (owner-direction 82de8c46; solver-wide, switch or no switch: f3463ebe): where the closure F has two
#: roots, the answer is the root continuous with the warm-side T_pot sweep. The sweep steps T_pot up by WARM_STEP_K
#: (the sensitivity step when one is set) until one root is left, at most WARM_STEPS_MAX steps (200 K at 10 K; a declared
#: choice, named in silicate registration post-freeze note 4).
WARM_STEP_K = 10.0
WARM_STEPS_MAX = 20


def warm_continuation(solve_at, t0: float, roots0, step: float, n_max: int = WARM_STEPS_MAX):
    """The root of `roots0` (at T_pot t0) continuous with the warm-side sweep, and the trace.
    `solve_at(t)` gives ("root", x), ("two_roots", (x1, x2, …)) or ("other", id) for the closure at T_pot t.
    Steps t0 + k·step for k = 1 … n_max until one root is left, then walks back, taking at each T_pot the root nearest
    the one chosen at the next warmer T_pot. Returns (root or None, trace, why): None when the sweep meets anything but
    roots before one root is left, or never leaves two roots within n_max steps."""
    trace = [(t0, tuple(roots0))]
    for k in range(1, n_max + 1):
        t = t0 + k * step
        kind, val = solve_at(t)
        if kind == "root":
            trace.append((t, (val,)))
            chosen = val
            for _t, roots in reversed(trace[:-1]):
                chosen = min(roots, key=lambda r: abs(r - chosen))
            return chosen, trace, None
        if kind != "two_roots":
            trace.append((t, ()))
            return None, trace, f"the warm-side sweep met {val} at T_pot {t:g} K before one root was left"
        trace.append((t, tuple(val)))
    return None, trace, f"two roots persist over {n_max} warm steps of {step:g} K"


def solve(body, options: context.Options = context.Options(), warm=None, views=None, registry=None):
    """Returns (Outcome, warm). Outcome is result.Answer, result.Refusal or result.NoAnswer.
    `views` (layer id → material view) replaces the adapter's resolution; it exists for physics fixtures only and is
    not reachable from Body, options or the context. `registry`: a loaded material registry the caller owns and
    reuses across solves (switch-over note 5); without it the solve loads its own.
    A closure with two roots is answered by the owner's F12 rule (`_warm_root`)."""
    out, w = _solve(body, options, warm, views, registry)
    if isinstance(out, result.Refusal) and out.id == "solve.two_roots" and views is None \
            and body.surface.t_pot is not None:
        ans, x = _warm_root(body, options, registry, out)
        return (ans, x) if isinstance(ans, result.Answer) else (ans, w)   # an Answer's second value is its root (68)
    return out, w


def _warm_root(body, options, registry, refusal):
    """Owner F12 (82de8c46): the root continuous with the warm-side T_pot sweep, solved alone in its half of the scan
    range (split at the two roots' midpoint), with a `closure_root_choice` note naming the other root and the sweep.
    If the sweep cannot decide, or the chosen half does not answer alone, the two_roots refusal stands unchanged.
    Returns (outcome, the half solve's root or None); `solve` hands the root on as its second value (member_of)."""
    roots = tuple(sorted(refusal.evidence["roots"]))
    step = options.sensitivity_dt if options.sensitivity_dt > 0.0 else WARM_STEP_K
    quiet = dataclasses.replace(options, sensitivity_dt=0.0)

    def at(t):
        bt = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=t))
        o, x = _solve(bt, quiet, None, None, registry)
        if isinstance(o, result.Answer):
            return "root", x
        if isinstance(o, result.Refusal) and o.id == "solve.two_roots":
            return "two_roots", tuple(sorted(o.evidence["roots"]))
        return "other", getattr(o, "id", None) or getattr(o, "reason", None)
    chosen, trace, why = warm_continuation(at, body.surface.t_pot, roots, step)
    if chosen is None:                               # the refusal stands as it was: solve.two_roots's evidence fields
        return refusal, None                         # are C1's pinned set (test_node_additive), so the sweep is not added
    lo, hi = body.closure.lo, body.closure.hi
    i = roots.index(chosen)
    half_lo = lo if i == 0 else 0.5 * (roots[i - 1] + roots[i])
    half_hi = hi if i == len(roots) - 1 else 0.5 * (roots[i] + roots[i + 1])
    bh = dataclasses.replace(body, closure=dataclasses.replace(body.closure, lo=half_lo, hi=half_hi))
    ans, x_half = _solve(bh, options, None, None, registry)
    if not isinstance(ans, result.Answer):           # the chosen half does not answer alone: the refusal stands
        return refusal, None
    note = result.Note(
        "closure_root_choice", "the closure has two roots; the answer is the root continuous with the warm-side T_pot "
        "sweep (owner F12, owner-direction 82de8c46), the other root named", {
            "roots": list(roots), "chosen": chosen, "others": [r for r in roots if r != chosen],
            "closure": {"kind": body.closure.kind, "layer": body.closure.layer, "name": body.closure.name,
                        "range": [lo, hi], "solved_in": [half_lo, half_hi]},
            "warm_sweep": [[t, list(r)] for t, r in trace], "step_k": step})
    return result.Answer(ans.quantities, ans.boundaries, ans.profiles, ans.missing, tuple(ans.notes) + (note,)), x_half


def _with_first(outcome, first):
    """Note 18: every outcome of a retry other than an Answer carries the first attempt's residual failure (68 B1)."""
    if isinstance(outcome, result.Refusal):
        e = refusals.REGISTRY.get(outcome.id)
        if e is not None and e.solve and "first_attempt" not in outcome.evidence:
            return refusals.make(outcome.id, outcome.where, at=outcome.at, **dict(outcome.evidence), first_attempt=first)
    if isinstance(outcome, result.NoAnswer):
        e = refusals.NO_ANSWER_REGISTRY.get(outcome.reason)      # the registry says which reasons take it (X3)
        if e is not None and "first_attempt" in e.optional and "first_attempt" not in outcome.evidence:
            return refusals.no_answer(outcome.reason, outcome.where, at=outcome.at, **dict(outcome.evidence),
                                      first_attempt=first)
    return outcome


def _solve(body, options, warm, views, registry, _first=None, _id_options=None):
    """solve()'s body. `_first` / `_id_options` are note 18's retry: the first attempt's residual-check record, and
    the caller's options, which keep the solve_id the request's. The retry calls _solve, not the module's `solve`, so
    a patched solve never sees it (68 N2)."""
    registry_arg = registry
    views_arg = views
    context.require_git_tree()                        # P1R-G2-R-07: before any pass, not after the accepted one
    # P1R-G2-C-09: these declared Options enter solve_id but the closure reads its module constants (close_*, wall_*)
    # and nothing reads basal_* or band_pass (A1 impl note 7); a caller setting one would get a new id with an
    # unchanged computation, so a non-default value is refused here as not wired
    inert = [k for k in INERT_OPTIONS if getattr(options, k) != getattr(context.Options(), k)]
    if inert:
        raise NotImplementedError(f"Options {inert} are declared but not wired into the solve (P1R-G2-C-09)")
    where = f"{body.name}.solve"
    nyi = _not_yet(body)                              # r2 S7 B2/B3: refuse by name what phase 1 does not implement
    if nyi is not None:
        return refusals.make("input.cross_field", where, rule=nyi[0], detail=nyi[1]), warm
    supplied = views is not None
    registry = None
    if views is None:
        lm.reset_engine_state()                      # reset before any material is touched (r2 S7)
        registry = registry_for(body, options, registry_arg)   # switch-over §1; note 5: the caller's load, reused
        if isinstance(registry, result.Refusal):
            return registry, warm
        views = _views(body, registry=registry, silicate=options.silicate_records)
    else:
        views = dict(views)
    if isinstance(views, result.Refusal):
        return views, warm
    for l in body.layers:                             # switch-over note 3: no ungraded declared value ships
        v = views.get(l.id)
        if hasattr(v, "record") and mr.has_user_declared(v.record):
            return refusals.make("input.declared_grade_not_wired", f"{body.name}.layers.{l.id}", layer_id=l.id,
                                 material_id=v.material_id), warm
    ctx = context.build(options, views, warm,
                        reset_legacy=any(isinstance(v, lm.LegacyView) for v in views.values()))
    kind = body.closure.kind

    views_all = views                                 # F keeps the unbound views: the probes run after `views` is bound to x*

    def F(x):
        vx = _views_at(body, views_all, x)
        if isinstance(vx, st.Stop):
            return vx
        got = inward(body, vx, x, options, want_graze=False)   # a trial: its graze is never read
        if isinstance(got, st.Stop):
            return got
        return got.F if got.F is not None else st.Stop("no_residual", {"x": x, "value": None})   # value named (68)

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
                here = {"x": x, "F_root": acc.F, "tol_F": tol_f, "n_acc": acc.counters.get("accepted", 0),
                        "rtol": options.rtol, "bracket": bracket["final"]}
                if _first is None:
                    # note 18: where F's slope is below its per-pass noise (Mars's melt knee: ~5e-7 per m of R against
                    # ~1e-7 with tails to 8e-7 at rtol 1e-10) Brent can close on a noise sign change; the residual check
                    # catches it, and the solve is re-closed once at rtol/10 before it refuses
                    got, w = _solve(body, dataclasses.replace(options, rtol=options.rtol / CLOSURE_RETRY_RTOL_DIV),
                                    warm, views_arg, registry_arg, _first=here, _id_options=options)
                    return _with_first(got, here), w
                return refusals.make("solve.closure_discontinuous", where, x=x, closure_kind=kind,
                                     state=_state(acc.y, acc.m),     # note 13 §3: the node where F was taken
                                     pass_kind="accepted", check="residual", F_root=acc.F, tol_F=tol_f,
                                     n_acc=here["n_acc"], rtol=options.rtol,
                                     bracket=bracket["final"], probes=None, first_attempt=_first), x
        notes = []
        if _first is not None:                          # note 18: the retry is disclosed on the Answer it gave
            notes.append(result.Note("closure_retried", "the first closure failed note 8's residual check, so the solve "
                                     f"was re-closed once at rtol/{CLOSURE_RETRY_RTOL_DIV:g}",
                                     {"first_attempt": _first, "rtol": options.rtol,
                                      "F_root": acc.F if guard else None, "tol_F": tol_f if guard else None,
                                      "n_acc": acc.counters.get("accepted", 0)}))
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
        sid = context.solve_id_of(_canonical(body), _material_bytes(views), _id_options or options)
        qs = _quantities(body, acc, sid, x, views)
        if body.surface.t_pot is not None and options.sensitivity_dt > 0.0:
            qs, sens_note = _with_sensitivity(body, views, x, options, acc, qs, supplied=supplied, ctx=ctx,
                                              registry=registry)
            if isinstance(sens_note, list):
                notes.extend(sens_note)
            elif sens_note is not None:
                notes.append(sens_note)
        if guard:                                        # note 9 (a″): one-sided chords on both sides of x*
            sides = [_side_check(F, x, acc.F, -1.0, rt, body.closure.lo, body.closure.hi),
                     _side_check(F, x, acc.F, 1.0, rt, body.closure.lo, body.closure.hi)]
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
        for bg in acc.band_grazes:                       # notes 13 §1 / 13a: accepted at the band floor, disclosed
            notes.append(result.Note("band_graze", "a step on a legacy table phase reached the band test's floor with g "
                                     "still near a band edge: accepted there, the band's entry or exit may be a graze "
                                     "(phase-1 design notes 13 §1, 13a)", dict(bg)))
        notes += material_notes.collect(body, views, acc)   # switch-over §4: after every value, accepted pass only
        ans = result.Answer(qs, lbs, profiles, (), tuple(notes))
        return ans, x
    if out.kind == "two_roots":
        return refusals.make("solve.two_roots", where, x=None, closure_kind=kind, pass_kind="scan",
                             roots=list(out.roots), F_scan=[[t.x, t.F] for t in out.trials if t.F is not None],
                             n_scan=options.n_scan), warm
    if out.kind == "unconverged":
        budget = out.detail.get("budget", "CLOSE_ITERS")
        value = cl.MAX_SPLITS if budget == "MAX_SPLITS" else cl.CLOSE_ITERS
        # P1R-G2-R-08: the residual of the bracket that failed (closure's problem record), else the last solved trial
        failed = next((p for p in out.detail.get("problems", []) if p and p[0] == "unconverged"), None)
        last = failed[2] if failed is not None else next((t.F for t in reversed(out.trials) if t.F is not None), None)
        return refusals.no_answer("unconverged", where, budget_name=budget, budget_value=value,
                                  last_residual=last), warm
    walls = []
    for w in out.walls:
        mapped = _to_refusal(w.stop, where, w.x, kind, "wall")
        is_na = isinstance(mapped, result.NoAnswer)
        walls.append({"x": w.x, "outcome_kind": "no_answer" if is_na else "refusal",
                      "id_or_reason": mapped.reason if is_na else mapped.id,
                      "state": getattr(w.stop, "state", None), "located": w.located})
    if out.kind == "no_solved":
        first = min(out.trials, key=lambda t: t.x)
        scan = [[t.x, t.F, None if t.stop is None else t.stop.kind] for t in sorted(out.trials, key=lambda t: t.x)]
        return _to_refusal(first.stop, where, first.x, kind, "scan", scan=scan), warm
    straddled = _straddled_wall(out)
    if straddled is not None:
        scan = [[t.x, t.F, None if t.stop is None else t.stop.kind] for t in sorted(out.trials, key=lambda t: t.x)]
        return _to_refusal(straddled.stop, where, straddled.x, kind, "wall", scan=scan), warm
    # P1R-G2-C-13: design §A1.5's «the scan ends, F there»: F at the lowest and highest scan points (None where that
    # end refused), not at the extreme solved trials
    scan_pts = sorted((t for t in out.trials if t.kind == "scan"), key=lambda t: t.x)
    return refusals.make("solve.no_bracket", where, x=None, closure_kind=kind, pass_kind="scan",
                         x_lo=body.closure.lo, x_hi=body.closure.hi, F_lo=scan_pts[0].F if scan_pts else None,
                         F_hi=scan_pts[-1].F if scan_pts else None,
                         n_scan=options.n_scan, walls=walls, solved_regions=_regions(out)), warm
