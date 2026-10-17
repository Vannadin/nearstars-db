# 전환 등록 시험 — 기록 뷰의 사건 · 옛 물질과의 패스 동일성(SW1) · 기록 거절의 대응 (switch-over registration §2, §6)
"""Switch-over registration (rewrite/switchover-registration.frozen.md) §2 and §6, the parts that land before the
resolver switches: a record view's events, the identity of a pass through fe_prem_legacy with the legacy fe_prem
(r2 SW1), and a record view's refusals reaching the solver's refusal registry; step 2's put-back identity.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_switchover
"""
import math
import unittest

from solver import context, events, from_v1, legacy_materials as lm, material_registry as mr, material_view as mv
from solver import refusals, solve as sv
from solver import stepper as st
from solver.from_v1 import thaw


def _record(rid):
    reg = mr.load()
    if isinstance(reg, mr.LoadStop):
        raise AssertionError(f"registry STOP: {reg.id} {dict(reg.evidence)}")
    return thaw(reg.records[rid])


def _shipped_bse():
    reg = mr.load()
    return isinstance(reg, mr.Registry) and "silicate_slb_default_bse" in reg.tables


class RecordEvents(unittest.TestCase):
    def test_h2o_events_from_its_declarations(self):
        """Seams, solid–solid curves (seam events), melting curves (terminal) and the 130 K source-seam isotherm."""
        v = mv.RecordView(_record("h2o"), 300.0)
        evs = events.layer_events(v)
        kinds = {(e.terminal, e.seam) for e in evs}
        self.assertIn((False, True), kinds)                                   # seams and solid–solid curves
        melts = events.melting_events(v)
        self.assertTrue(melts)
        self.assertEqual({e.name for e in evs if e.terminal}, set(melts))      # every melting curve is terminal
        self.assertIn("source_seam:ih_cold|Ih", {e.name for e in evs})
        self.assertEqual(len([e for e in evs if e.name.startswith("seam:")]), len(v.seams()))   # noqa: test-side name

    def test_h2o_vi_vii_curve_lands_under_the_clamp(self):
        """68 N2 / directing 10-17 (b): h2o's VI|vii_x solid–solid curve carries component 1 and lands under the old-side
        clamp. Walked inward from 2.0 GPa, 340 K, on h2o's own ice VI, with a planted far side: past the curve, ice VI's
        state at the curve 4 % denser and with dT/dP 4 % lower, because h2o's vii_x source (french_redmer2015) refuses
        just past the line at 330–354 K (its ρ bracket; logged for the h2o range list). Unheld (component None, the
        mutant) the landing chatters."""
        import dataclasses
        from solver import rhs
        v = mv.RecordView(_record("h2o"), 340.0)
        (vi,) = [e for e in events.layer_events(v) if e.name == "phase:VI|vii_x"]
        self.assertEqual((vi.component, vi.seam, vi.terminal), (1, True, False))

        class Past:
            def state(self, p, t, guess):
                g = vi.g(0.0, (0.0, p, t, t, 0.0, 0.0))
                if g is not None and g > 0.0:
                    s = v.state((p - g) * (1.0 - 1e-9), t, guess)
                    return s if isinstance(s, st.Stop) else (s[0] * 1.04, s[1] * 0.96, s[2])
                return v.state(p, t, guess)
        m_, r_ = 5.972e24, 6.371e6
        rs = rhs.r_scale_of(m_, 3.0 * m_ / (4.0 * math.pi * r_ ** 3))
        opt = st.Options(rtol=1e-10, floors=rhs.floors(m_, rs), h0=3e-4 * m_, h_min=1e-15 * m_, h_max=m_ / 50.0,
                         max_steps=200000)
        for comp, want in ((1, ("end", ["phase:VI|vii_x"])), (None, ("chatter", []))):
            res = st.run(rhs.make_rhs(Past()), m_, (r_, 2.0e9, 340.0, 340.0, 0.0, 0.0), 0.995 * m_, opt,
                         [dataclasses.replace(vi, component=comp)])
            self.assertEqual((res.stop.kind, [e[0] for e in res.events]), want, comp)

    def test_curve_scale_is_its_largest_p_b(self):
        """Pre-run C1 on 68e47ffc: a record curve event's landing scale is its curve's largest |P_b| over 50–10 000 K,
        so its tolerance is relative to P as phase 1's seams (scale = p_b); a fixed 1e9 was 1e-3 Pa. Absent everywhere:
        1e9."""
        class View:
            def boundary_pressure(self, curve, t):
                return None if not curve["lo"] <= t <= curve["hi"] else 1.0e10 + 2.0e6 * t
        v = View()
        self.assertEqual(events.curve_p_scale(v, {"lo": 1000.0, "hi": 3000.0}), 1.0e10 + 2.0e6 * 3000.0)
        self.assertEqual(events.curve_p_scale(v, {"lo": 20000.0, "hi": 30000.0}), 1.0e9)
        hv = mv.RecordView(_record("h2o"), 340.0)
        (vi,) = [e for e in events.layer_events(hv) if e.name == "phase:VI|vii_x"]
        self.assertGreater(vi.scale, 1.0e9)

    def test_gibbs_scale_is_the_boundary_terms(self):
        """68 on C1, the same class: a gibbs boundary's g is (G_a − G_b)/(v_a − v_b), a P, and its scale the largest
        P + T·|Δs/Δv| at the boundary, not a fixed 1e3 on ΔG (1e-9 J/kg, 4–100× under the landing's spread). Planted
        linear G = v·P − s·T: the boundary is P = 1.333e7·T, where the scale is 2P (8e9 Pa at 300 K). SeaFreeze's own
        Ih|water1 too. Mutant: a fixed scale."""
        class Lib:
            def __init__(self, v, s):
                self.v, self.s = v, s

            def at(self, p, t):
                return {"rho": 1.0 / self.v, "g": self.v * p - self.s * t}
        got = events.gibbs_scale(Lib(1.0e-3, 0.0), Lib(1.09e-3, 1200.0), box=(1.0e6, 1.0e10, 250.0, 300.0))
        self.assertGreater(got, 0.5 * 8.0e9)
        self.assertLess(got, 1.5 * 8.0e9)
        from solver import material_library as ml
        ih, wa = ml.SeaFreezePhase("Ih"), ml.SeaFreezePhase("water1")
        self.assertGreater(events.gibbs_scale(ih, wa), 1.0e7)
        from types import SimpleNamespace                  # and record_events takes it for a library boundary
        stub = SimpleNamespace(phases=(SimpleNamespace(id="Ih", library=ih), SimpleNamespace(id="water1", library=wa)),
                               seams=lambda: (), source_seams=lambda: (),
                               transitions=lambda: ((("Ih", "water1"), "solid_solid", {"form": "library"}),))
        (ev,) = events.record_events(stub)
        self.assertEqual(ev.scale, events.gibbs_scale(ih, wa))

    def test_gibbs_boundary_lands_held_on_the_old_side(self):
        """Directing 10-17: a gibbs boundary lands with its stages held on the old side (component 1), as a curve does.
        Its g is (G_a − G_b)/(v_a − v_b). (1) Planted linear G whose boundary is test_assemblage_boundaries' sloped curve
        (23.83 GPa, 9.4e6 Pa/K, ρ 3717 → 3720 and dT/dP −4 % across): held it lands at three first-step sizes, unheld
        (component None, the mutant) it chatters, as the curve did (Mars 1774 K). (2) SeaFreeze's own Ih|water1 on an
        inward walk from 1 MPa, 270 K (crossing near 30 MPa, a 9 % density step): held it lands at three sizes."""
        import dataclasses
        from types import SimpleNamespace
        from solver import material_library as ml, rhs
        pb, k, va, vb = 23.83e9, 9.4e6, 1.0 / 3717.0, 1.0 / 3720.0
        dv = va - vb

        class Lib:
            def __init__(self, a):
                self.a = a

            def at(self, p, t):
                if self.a:
                    return {"rho": 1.0 / va, "g": va * p - dv * k * t + dv * (k * 1600.0 - pb)}
                return {"rho": 1.0 / vb, "g": vb * p}

        def walk(ev, state, y0, m_, r_, h0s, comp, end=0.5):
            rs = rhs.r_scale_of(m_, 3.0 * m_ / (4.0 * math.pi * r_ ** 3))
            out = []
            for h0 in h0s:
                o = st.Options(rtol=1e-10, floors=rhs.floors(m_, rs), h0=h0 * m_, h_min=1e-15 * m_, h_max=m_ / 20.0,
                               max_steps=200000)
                got = st.run(rhs.make_rhs(state), m_, y0, end * m_, o, [dataclasses.replace(ev, component=comp)])
                out.append((got.stop.kind, [e[0] for e in got.events]))
            return out

        def stub(a, b, la, lb):
            return SimpleNamespace(phases=(SimpleNamespace(id=a, library=la), SimpleNamespace(id=b, library=lb)),
                                   seams=lambda: (), source_seams=lambda: (),
                                   transitions=lambda: (((a, b), "solid_solid", {"form": "library"}),))
        (ev,) = events.record_events(stub("a", "b", Lib(True), Lib(False)))
        self.assertEqual(ev.component, 1)

        class Sloped:
            def state(self, p, t, guess):
                new = p > pb + k * (t - 1600.0)
                return (3720.0 if new else 3717.0), (9.2e-9 if new else 9.6e-9)
        y0, h0s = (6.371e6, 0.0, 1600.0, 1600.0, 0.0, 0.0), (1e-3, 7.3e-4, 1.37e-3)
        self.assertEqual(walk(ev, Sloped(), y0, 5.972e24, 6.371e6, h0s, 1), [("end", ["phase:a|b"])] * 3)
        self.assertEqual([r[0] for r in walk(ev, Sloped(), y0, 5.972e24, 6.371e6, h0s, None)], ["chatter"] * 3)
        ih, wa = ml.SeaFreezePhase("Ih"), ml.SeaFreezePhase("water1")
        (ev,) = events.record_events(stub("Ih", "water1", ih, wa))

        class Ice:
            def state(self, p, t, guess):
                a, b = ih.at(p, t), wa.at(p, t)
                c = a if a["g"] < b["g"] else b
                return c["rho"], c["dtdp"], ()
        got = walk(ev, Ice(), (2.0e6, 1.0e6, 270.0, 270.0, 0.0, 0.0), 1.0e23, 2.0e6, (1e-3, 1.37e-3, 3e-3), 1, 0.95)
        self.assertEqual(got, [("end", ["phase:Ih|water1"])] * 3)

    def test_onset_scale_is_its_largest_t(self):
        """68 on C1: an onset event's scale is its curve's largest T_onset over 1 bar–400 GPa (tolerance 1e-12 of T, the
        seams' rule), not ONSET_SCALE. Mutant: ONSET_SCALE."""
        class Mat:
            def onset_curves(self, p, t):
                return [("sol", 1500.0 + 1.0e-8 * p)]
        self.assertEqual(events.onset_t_scale(Mat(), "sol"), 1500.0 + 1.0e-8 * max(events.ONSET_SCALE_PS))
        self.assertEqual(events.onset_t_scale(Mat(), "liq"), events.ONSET_SCALE)
        Mat.onset_curve_names = ("sol",)
        (ev,) = events.onset_events(Mat())
        self.assertEqual(ev.scale, 1500.0 + 1.0e-8 * max(events.ONSET_SCALE_PS))

    @unittest.skipUnless(_shipped_bse(), "no shipped default_bse record with its table (the engine branch without records)")
    def test_edge_lands_at_its_p_scale(self):
        """Pre-run C1 on 68e47ffc: earth O9 2135.35 K's landing on default_bse's edge427 (wa+gt+fp|gt+fp) at 16.9 GPa,
        captured at the step that crossed it (adaptive, the solve's own options). At scale 1e9 (tolerance 1e-3 Pa) the
        re-steps reproduce P only to ~±4e-3 Pa there and no new-side iterate falls inside: event_unlanded (the mutant).
        At the curve's P scale it lands."""
        import dataclasses
        from solver import material_assemblage as ma, rhs
        reg = mr.load()
        rid = "silicate_slb_default_bse"
        got = reg.records[rid]
        hid = got["assemblage"]["handover"]
        ho = ma.HandOver(thaw(reg.records[hid]), reg.tables[hid], rid, 1.5 * float(got["assemblage"]["p_dataset"]))
        v = ma.view(thaw(got), reg.tables[rid], 2135.3511104889826, 0.0, 0.0, ho)
        (ev,) = [e for e in events.record_events(v) if e.name == "phase:edge427:wa+gt+fp|gt+fp"]
        x = 5.902044125836793e+24
        y = (3372110.8592750556, 15773166429.591904, 2501.797174057437, 2501.797174057437, 5.519101142731295e+35, 0.0)
        k1 = (2.0319501618785867e-18, -2.4243255396972823e-13, -4.304052193708393e-21, -4.304052193708393e-21,
              -7580754431493.836, -0.0)
        opt = st.Options(rtol=1e-10, floors=(3.5073921716089398e-06, 1.0e5, 10.0, 10.0, math.inf, math.inf),
                         h0=5.972e+21, h_min=5972000000.000001, h_max=2.986e+23, max_steps=200000,
                         event_min_progress=5972000000000001.0, event_restarts_step=4, event_restarts_run=2000)
        f, s_hi = rhs.make_rhs(v), -5.972e+21
        out_hi = st.step(f, x, y, s_hi, k1)
        self.assertLess(ev.g(x, y), 0.0)
        self.assertGreater(ev.g(x + s_hi, out_hi[0]), 0.0)                   # the step crosses the curve
        for scale, landed in ((ev.scale, True), (1.0e9, False)):
            e = dataclasses.replace(ev, scale=scale)
            r = st._land(f, e, x, y, k1, s_hi, out_hi, e.g(x, y), opt, st.Counters())
            self.assertEqual(not isinstance(r, st.Stop), landed, (scale, getattr(r, "kind", None)))
        self.assertGreater(ev.scale, 1.5e10)

    def test_onset_curves_hook_is_present_and_empty(self):
        """68 N63: the graze monitor reads a record view's onset_curves (legacy's signature); none are declared today,
        and a record declaring onset data STOPs at load as an unknown key until the schema has it."""
        v = mv.RecordView(_record("fe_prem"), 1600.0)
        self.assertEqual(v.onset_curves(1.0e11, 4000.0), [])
        rec = _record("fe_prem")
        rec["onset_curves"] = [{"name": "고상선"}]
        self.assertEqual(mr.check_record(rec, "fe_prem.yaml").id, "material.unknown_key")

    def test_a_legacy_view_keeps_its_events(self):
        """A legacy view (or its bare material) builds exactly the events it built before the switch-over."""
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        leg = sv._views(body)["mantle"]
        a = [(e.name, e.terminal, e.seam) for e in events.layer_events(leg)]
        b = [(e.name, e.terminal, e.seam) for e in events.layer_events(leg.mat)]
        self.assertEqual(a, b)
        self.assertTrue(a)


class LegacyIdentity(unittest.TestCase):
    """r2 SW1: the step-1 identity rests on the record view reproducing the legacy pass, not only state(): the same
    events, the same landed nodes, the same residual, on Earth's accepted pass."""

    def test_earth_pass_through_fe_prem_legacy(self):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        opt = context.Options(sensitivity_dt=0.0)
        ans, x = sv.solve(body, opt)
        views = sv._views_at(body, sv._views(body), x)
        leg = views["core"]
        rec = mv.RecordView(_record("fe_prem_legacy"), body.surface.t_pot, getattr(leg, "p_stop", 0.0))
        self.assertEqual([(e.name, e.seam) for e in events.layer_events(rec)],
                         [(e.name, e.seam) for e in events.layer_events(leg)])
        a = sv.inward(body, views, x, opt)
        b = sv.inward(body, {**views, "core": rec}, x, opt)
        self.assertEqual(a.F, b.F)
        self.assertEqual(a.events, b.events)
        self.assertEqual(a.profiles["core"], b.profiles["core"])
        self.assertEqual(a.boundaries, b.boundaries)

    def test_control_the_corrected_record_moves_the_pass(self):
        """Control: the corrected fe_prem (step 2's record) does not reproduce the legacy pass."""
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        opt = context.Options(sensitivity_dt=0.0)
        _ans, x = sv.solve(body, opt)
        views = sv._views_at(body, sv._views(body), x)
        rec = mv.RecordView(_record("fe_prem"), body.surface.t_pot, getattr(views["core"], "p_stop", 0.0))
        self.assertNotEqual(sv.inward(body, views, x, opt).F, sv.inward(body, {**views, "core": rec}, x, opt).F)


def _path(nodes):
    """An accepted-node path (m, y, k) with y = (r, P, T_ad, T)."""
    return [(0.0, (1.0, p, t, t), None) for p, t in nodes]


def _collect(rid, t_pot, nodes):
    from types import SimpleNamespace as NS
    from solver import material_notes as mn
    v = mv.RecordView(_record(rid), t_pot)
    return v, mn.collect(NS(layers=[NS(id="L")]), {"L": v}, NS(profiles={"L": _path(nodes)}))


class Notes(unittest.TestCase):
    """Switch-over §4 / §6.4: what the accepted pass read reaches Answer.notes once per key, values untouched."""

    def test_h2o_declared_note_seam_and_disclosure(self):
        _v, got = _collect("h2o", 300.0, [(1e7, 90.0), (1e7, 120.0), (2e7, 140.0), (5e7, 200.0)])
        kinds = [n.kind for n in got]
        self.assertEqual(kinds.count("material_declared_note"), 1)            # IAPWS-06 below 100 K, three nodes
        seam = [n for n in got if n.kind == "material_source_seam"]
        self.assertEqual([(n.fields["t"], tuple(n.fields["between"])) for n in seam], [(130.0, ("ih_cold", "Ih"))])
        self.assertIsNotNone(seam[0].fields["step"])
        cross = [n for n in got if n.kind == "material_disclosure" and n.fields["of"] == "cross_check"]
        self.assertEqual([n.fields["phase"] for n in cross], ["Ih"])
        self.assertNotIn("material_grade", kinds)                              # h2o has no user-declared source

    def test_a_seam_touched_from_above_is_not_crossed(self):
        """Control: the upper side owns t, so a path from t = 130 K upward never crossed the seam."""
        _v, got = _collect("h2o", 300.0, [(1e7, 130.0), (2e7, 140.0)])
        self.assertFalse([n for n in got if n.kind == "material_source_seam"])
        self.assertFalse([n for n in got if n.kind == "material_declared_note"])

    def test_fe_prem_band_once_with_the_largest_error(self):
        nodes = [(3.3e11, 4000.0), (3.6e11, 4000.0), (3.7e11, 4000.0)]
        v, got = _collect("fe_prem", 1600.0, nodes)
        bands = [n for n in got if n.kind == "material_band"]
        self.assertEqual(len(bands), 1)
        errs = [n.error for p, t in nodes for n in v.state(p, t)[2] if isinstance(n, mv.BandNote)]
        self.assertEqual(bands[0].fields["error"], max(errs))
        self.assertEqual((bands[0].fields["p_min"], bands[0].fields["p_max"]), (3.6e11, 3.7e11))   # only past 350 GPa


def _h2o_with_boundary(bd):
    rec = _record("h2o")
    rec["formula_checks"][8]["boundary"] = bd                     # the III–water1 disclosed fail (c8's pair)
    return rec


def _notes_of(rec, nodes):
    from types import SimpleNamespace as NS
    from solver import material_notes as mn
    v = mv.RecordView(rec, 300.0)
    return mn.collect(NS(layers=[NS(id="L")]), {"L": v}, NS(profiles={"L": _path(nodes)}))


class Note3(unittest.TestCase):
    """Switch-over note 3: a formula check's `boundary` narrows its disclosure; a re-read Stop is recorded; a
    user-declared record refuses at solve."""

    def test_boundary_load_rule(self):
        from solver.tests.test_materials_generated import _cache_cites

        def check(bd):
            rec = _h2o_with_boundary(bd)
            return mr.check_record(rec, "h2o.yaml", frozenset(s for _p, _n, s in _cache_cites(rec)))
        self.assertNotIsInstance(check(["III", "water1"]), mr.LoadStop)
        for bad in (["III", "nope"], ["III", "III"], ["III"]):
            self.assertEqual(check(bad).id, "material.bad_shape")

    def test_disclosure_only_where_the_pair_is_read(self):
        rec = _h2o_with_boundary(["III", "water1"])

        def fc(nodes):
            return [n for n in _notes_of(rec, nodes) if n.kind == "material_disclosure"
                    and n.fields["of"] == "formula_check"]
        self.assertEqual(fc([(1e7, 200.0), (5e7, 210.0)]), [])                        # Ih only
        got = fc([(2.5e8, 245.0), (3e8, 250.0)])                                        # III read
        self.assertEqual([tuple(n.fields["boundary"]) for n in got], [("III", "water1")])
        bare = _record("h2o")                          # the shipped record names the pair (c8, 7c7c48f1): drop it
        bare["formula_checks"][8].pop("boundary", None)
        self.assertEqual(len([n for n in _notes_of(bare, [(1e7, 200.0)])               # no boundary: every read
                              if n.kind == "material_disclosure" and n.fields["of"] == "formula_check"]), 1)

    def test_a_reread_stop_is_recorded(self):
        got = [n for n in _notes_of(_record("h2o"), [(1e7, 200.0), (1e7, 5000.0)])
               if n.kind == "material_reread_stop"]
        self.assertEqual([(n.fields["count"], n.fields["points"][0][2]) for n in got], [(1, "refused")])

    def test_a_user_declared_record_refuses_at_solve(self):
        """Planted: fe_prem_legacy with one source made user-declared; control: the record as shipped answers
        (NotesOnEarth)."""
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        leg = sv._views(body)
        rec = _record("fe_prem_legacy")

        def plant(x):
            if isinstance(x, dict):
                if "source" in x and isinstance(x["source"], dict):
                    x["source"] = {"user_declared": "planted control"}
                    return True
                return any(plant(v) for v in x.values())
            if isinstance(x, list):
                return any(plant(v) for v in x)
            return False
        self.assertTrue(plant(rec))
        views = {**leg, "core": mv.RecordView(rec, body.surface.t_pot, getattr(leg["core"], "p_stop", 0.0))}
        got, _x = sv.solve(body, context.Options(sensitivity_dt=0.0), views=views)
        self.assertEqual((got.id, got.evidence["material_id"]), ("input.declared_grade_not_wired", "fe_prem_legacy"))
        self.assertIn("input.declared_grade_not_wired", refusals.REGISTRY)


class SolveIdOfRecordViews(unittest.TestCase):
    """A6: solve_id's material bytes for a record view are its record, the same in every process (a repr of the view
    held object addresses and differed run to run)."""

    def test_same_bytes_in_two_processes_and_record_sensitive(self):
        import subprocess
        import sys
        code = ("from solver import material_registry as mr, material_view as mv, solve as sv\n"
                "from solver.from_v1 import thaw\n"
                "import sys\n"
                "v = mv.RecordView(thaw(mr.load().records[sys.argv[1]]), 300.0)\n"
                "print(sv._material_bytes({'L': v}).hex())\n")

        def run(rid):
            return subprocess.run([sys.executable, "-c", code, rid], capture_output=True, text=True,
                                  check=True).stdout.strip()
        a, b = run("h2o"), run("h2o")
        self.assertEqual(a, b)
        self.assertNotEqual(run("fe_prem"), run("fe_prem_legacy"))


class NotesOnEarth(unittest.TestCase):
    """§6.4 on a real solve: Earth's core through fe_prem_legacy (its band past 350 GPa)."""

    @classmethod
    def setUpClass(cls):
        cls.body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        cls.opt = context.Options(sensitivity_dt=0.0)
        leg = sv._views(cls.body)
        cls.views = {**leg, "core": mv.RecordView(_record("fe_prem_legacy"), cls.body.surface.t_pot,
                                                   getattr(leg["core"], "p_stop", 0.0))}

    def test_values_identical_with_collection_off(self):
        from unittest import mock
        from solver import material_notes as mn
        on, _x = sv.solve(self.body, self.opt, views=self.views)
        with mock.patch.object(mn, "collect", return_value=()):
            off, _x2 = sv.solve(self.body, self.opt, views=self.views)
        self.assertIsInstance(on, sv.result.Answer)
        self.assertEqual((on.quantities, on.boundaries, dict(on.profiles)),
                         (off.quantities, off.boundaries, dict(off.profiles)))
        self.assertTrue([n for n in on.notes if n.kind.startswith("material_")])   # noqa: test-side kind check
        self.assertFalse([n for n in off.notes if n.kind.startswith("material_")])  # noqa: test-side kind check
        self.assertFalse([n for n in on.notes if n.kind == "material_reread_stop"])   # 68 N65: every node re-reads

    def test_a_note_planted_in_trial_passes_never_reaches_the_answer(self):
        """Planted leak (A6 pattern): a view that notes every read while armed; armed in every pass but the one at the
        root, the note must not appear. Control: armed everywhere, it does."""
        from unittest import mock
        _ans, x_root = sv.solve(self.body, self.opt, views=self.views)
        core = self.views["core"]

        class Planted(mv.RecordView):
            armed = False

            def state(self, p, t, guess_rho=None):
                got = super().state(p, t, guess_rho)
                if Planted.armed and not isinstance(got, st.Stop):
                    return (got[0], got[1], got[2] + (mv.DeclaredNote(self.material_id, "planted", "planted"),))
                return got

        planted = Planted(_record("fe_prem_legacy"), self.body.surface.t_pot, core.p_stop)
        views = {**self.views, "core": planted}
        real = sv.inward

        def arming(arm_at_root):
            def inward(body, vs, x, opt, **kw):
                Planted.armed = arm_at_root or x != x_root
                try:
                    return real(body, vs, x, opt, **kw)
                finally:
                    Planted.armed = arm_at_root
            return inward

        def planted_notes(arm_at_root):
            Planted.armed = arm_at_root
            with mock.patch.object(sv, "inward", arming(arm_at_root)):
                ans, _x = sv.solve(self.body, self.opt, views=views)
            Planted.armed = False
            return [n for n in ans.notes if n.kind == "material_declared_note" and n.fields["phase"] == "planted"]

        self.assertEqual(planted_notes(False), [])
        self.assertEqual(len(planted_notes(True)), 1)


def _values(ans):
    """An Answer's values for the put-back identity: quantities with solve_id masked (it names the material bytes, so it
    moves with the switch by design), boundaries and profiles."""
    from solver import result
    qs = []
    for q in ans.quantities:
        d = result.plain(q)
        d["provenance"]["solver"]["solve_id"] = "<masked>"
        qs.append(d)
    return qs, result.plain(ans.boundaries), result.plain(dict(ans.profiles))


class Resolution(unittest.TestCase):
    """Switch-over §1 / §6.1: records first, legacy otherwise, never a fallback; the switch off is the baseline."""

    @classmethod
    def setUpClass(cls):
        cls.earth, _aside = from_v1.load_v1("engine/bodies/earth.yaml")

    def test_record_first_and_legacy_otherwise(self):
        on = sv._views(self.earth, registry=sv.registry_for(self.earth, context.Options()))
        self.assertIsInstance(on["core"], mv.RecordView)
        self.assertEqual(on["core"].material_id, "fe_prem")                    # step 2: no map left
        self.assertTrue(all(isinstance(v, lm.LegacyView) for k, v in on.items() if k != "core"))
        self.assertIsNone(sv.registry_for(self.earth, context.Options(materials="legacy")))
        off = sv._views(self.earth)
        self.assertIsInstance(off["core"], lm.LegacyView)

    def test_a_body_naming_no_record_loads_no_registry(self):
        mars, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        self.assertIsNone(sv.registry_for(mars, context.Options()))

    def test_an_unavailable_record_refuses_and_never_falls_back(self):
        from types import SimpleNamespace as NS
        stop = mr.LoadStop("material.library_pin", {"file": "fe_prem.yaml", "why": "planted pin mismatch"})
        reg = NS(get=lambda rid: stop if rid == "fe_prem" else None)
        got = sv._views(self.earth, registry=reg)
        self.assertEqual((got.id, got.evidence["material_id"], got.evidence["load_stop"]),
                         ("input.material_record_unavailable", "fe_prem", "material.library_pin"))

    def test_a_composition_on_a_record_layer_refuses(self):
        """G4-C-01's class (p1review, r2): a declared composition on a record layer is refused by name, never ignored.
        Control: the same layer without it resolves (test_record_first_and_legacy_otherwise)."""
        import dataclasses
        from solver import body as bd
        core = next(l for l in self.earth.layers if l.id == "core")
        planted = dataclasses.replace(self.earth, layers=tuple(
            dataclasses.replace(l, system="iron_alloy", composition=bd.Declared({"S": 0.15})) if l is core else l
            for l in self.earth.layers))
        got = sv._views(planted, registry=sv.registry_for(planted, context.Options()))
        self.assertEqual((got.id, got.evidence["rule"]), ("input.cross_field", "record_composition"))

    def test_any_param_on_a_record_layer_refuses(self):
        """68 N69: a record reads no layer params, so any key refuses (planted: `density`, which legacy's basal path
        reads), not only porosity keys."""
        import dataclasses
        planted = dataclasses.replace(self.earth, layers=tuple(
            dataclasses.replace(l, params={"density": 9000.0}) if l.id == "core" else l for l in self.earth.layers))
        got = sv._views(planted, registry=sv.registry_for(planted, context.Options()))
        self.assertEqual((got.id, got.evidence["rule"]), ("input.cross_field", "record_params"))

    def test_a_registry_stop_refuses_the_body(self):
        from unittest import mock
        with mock.patch.object(mr, "load", return_value=mr.LoadStop("material.duplicate_id", {"file": "h2o.yaml", "id": "h2o"})):
            got, _w = sv.solve(self.earth, context.Options(sensitivity_dt=0.0))
        self.assertEqual((got.id, got.evidence["load_stop"]), ("input.material_registry", "material.duplicate_id"))

    def test_the_switch_is_not_in_solve_id(self):
        body = {"b": 1}
        self.assertEqual(context.solve_id_of(body, b"m", context.Options()),
                         context.solve_id_of(body, b"m", context.Options(materials="legacy")))


class RegistryLoads(unittest.TestCase):
    """68 H1 / r2 on note 4 (switch-over note 5): one load per solve, the sensitivity pass included; a caller's
    registry is reused with no load and gives the same answer as solves that load their own."""

    def test_one_load_per_solve_and_none_when_passed(self):
        from unittest import mock
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        real = mr.load
        with mock.patch.object(mr, "load", side_effect=real) as ld:
            own, _x = sv.solve(body, context.Options())                  # sensitivity on (δ = 10 K)
            self.assertEqual(ld.call_count, 1)
            reg = real()
            ld.reset_mock()
            a, _x = sv.solve(body, context.Options(), registry=reg)
            b, _x = sv.solve(body, context.Options(), registry=reg)
            self.assertEqual(ld.call_count, 0)
        self.assertEqual(_values(a), _values(own))
        self.assertEqual(_values(b), _values(own))
        self.assertEqual(a.quantities[0].provenance.solver.solve_id, own.quantities[0].provenance.solver.solve_id)

    def test_a_passed_registry_stop_refuses(self):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        stop = mr.LoadStop("material.duplicate_id", {"file": "h2o.yaml", "id": "h2o"})
        got, _w = sv.solve(body, context.Options(sensitivity_dt=0.0), registry=stop)
        self.assertEqual(got.id, "input.material_registry")


class SwitchReachesEverySolve(unittest.TestCase):
    """Switch-over note 6: a solve made on the caller's behalf (an inverse body's member) follows the caller's switch,
    so a baseline run is a baseline throughout (the T2 method term: MethodTermMaterials)."""

    def test_member_solve_follows_the_switch(self):
        from unittest import mock
        from solver import member as mb
        venus, _aside = from_v1.load_v1("engine/bodies/venus.yaml")
        seen = []
        real = sv.solve

        def spy(body, options=context.Options(), warm=None, views=None, registry=None):
            seen.append(options.materials)
            return real(body, options, warm, views, registry)
        with mock.patch.object(sv, "solve", spy):
            mb.member_of(venus, "legacy")
        self.assertEqual(seen, ["legacy"])



class MethodTermMaterials(unittest.TestCase):
    """Switch-over note 7 (68 N68): the T2 method term solves on the records the answers read. A body with a record that
    declares a field boundary no longer keeps legacy: its curve events carry component 1 (652004f9) and land under the
    fixed mode's clamp (68 N3 on 652004f9, directing)."""

    @staticmethod
    def _with_fe_prem(**extra):
        from types import MappingProxyType
        from solver.result import freeze
        reg = mr.load()
        return mr.Registry(MappingProxyType({**reg.records, "fe_prem": freeze({**thaw(reg.records["fe_prem"]), **extra})}),
                           reg.unavailable, reg.warnings)

    def test_switch_on_without_boundaries(self):
        from solver import method_term as mt
        earth, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        self.assertEqual(mt.materials_for(earth, mr.load()), "registry")
        planted = self._with_fe_prem(boundaries=[{"between": ["a", "b"], "kind": "solid_solid", "curve": {}}])
        self.assertEqual(mt.materials_for(earth, planted), "registry")     # a boundary no longer keeps legacy (N3)

    def test_fixed_mode_lands_a_curve_event(self):
        """The reason legacy is no longer kept: in the fixed mode (the method term's), a sloped curve event with
        component 1 lands at every grid step and the answer does not depend on dr (to 1e-5 m); free (component None),
        r moves by metres with dr. Toy: a curve as steep as Mars's swap 304, dT/dP dropping 4 % across it."""
        from solver import fixed_grid as fg, rhs, stepper as stp
        m_, r_, pb, k = 5.972e24, 6.371e6, 23.83e9, 9.4e6

        class Sloped:
            def state(self, p, t, guess):
                new = p > pb + k * (t - 1600.0)
                return (3720.0 if new else 3717.0), (9.2e-9 if new else 9.6e-9)
        f = rhs.make_rhs(Sloped())
        got = {}
        for comp in (1, None):
            for dr in (2e3, 7.3e3, 1.37e4):
                ev = stp.Event("phase:sloped", lambda m, y: y[1] - (pb + k * (y[2] - 1600.0)), scale=1e9,
                               terminal=False, seam=True, component=comp)
                res = fg.run_r(f, m_, (r_, 0.0, 1600.0, 1600.0, 0.0, 0.0), 0.5 * m_, 0.0, "r_end", dr, [ev], m_scale=m_)
                self.assertEqual([e[0] for e in res.events], ["phase:sloped"])
                got.setdefault(comp, []).append(res.y[0])
        self.assertLess(max(got[1]) - min(got[1]), 1e-5)
        self.assertGreater(max(got[None]) - min(got[None]), 1.0)          # the control: unheld, it depends on dr

    def test_every_solve_follows_it(self):
        """68 H1 on 13035f6e: every solve one_state makes, not only the first. With the shipped registry, the spy passes
        each call through (the old chain off, it is legacy and not a solve of this term) and records it: the declared
        state makes three (adaptive, run_oracle's adaptive and fixed records), a T_pot state two (adaptive, fixed). With a
        planted boundary the first call shows «registry» too (68 N3 on 652004f9). Earth is forward, so no member solve is made."""
        from unittest import mock
        from solver import method_term as mt, run_oracle as ro
        seen = []
        real = sv.solve

        class Stop(Exception):
            pass

        def spy(body, options=context.Options(), warm=None, views=None, registry=None):
            seen.append((options.materials, registry is not None, options.fixed_dr > 0.0))
            return real(body, options, warm, views, registry)

        def stop(body, options=context.Options(), warm=None, views=None, registry=None):
            seen.append((options.materials, registry is not None))
            raise Stop
        shipped = mr.load()
        with mock.patch.object(sv, "solve", spy), mock.patch.object(ro.lv, "run_chain", lambda *a, **k: None), \
                mock.patch.object(ro, "_legacy", lambda rec, chain: None):
            for state, want in (("declared", [("registry", True, False), ("registry", True, False),
                                              ("registry", True, True)]),
                                (2000.0, [("registry", True, False), ("registry", True, True)])):
                seen.clear()
                rec = mt.one_state("engine/bodies/earth.yaml", state, "t", registry=shipped)
                self.assertEqual(seen, want, state)
                self.assertEqual(rec["materials"], "registry")
        seen.clear()
        planted = self._with_fe_prem(boundaries=[{"between": ["a", "b"], "kind": "solid_solid", "curve": {}}])
        with mock.patch.object(sv, "solve", stop), self.assertRaises(Stop):
            mt.one_state("engine/bodies/earth.yaml", "declared", "t", registry=planted)
        self.assertEqual(seen, [("registry", True)])            # a planted boundary no longer keeps legacy (68 N3)


class Step2PutBack(unittest.TestCase):
    """Switch-over step 2: fe_prem layers read fe_prem, whose two corrected constants (W-L1-01 αK_T, P5-F1 V0) are
    the only difference from the switch-off answers. Planted: both constants put back (test_p5_stages FIXTURES) give
    the switch-off values on Earth and Venus (solve_id masked); control: the record as shipped moves Earth's values."""

    @staticmethod
    def _registry(*findings):
        from types import MappingProxyType
        from solver.result import freeze
        from solver.tests.test_p5_stages import record
        reg = mr.load()
        return mr.Registry(MappingProxyType({**reg.records, "fe_prem": freeze(record(*findings))}),
                           reg.unavailable, reg.warnings)

    def _pair(self, path, registry):
        body, _aside = from_v1.load_v1(path)
        on, _x = sv.solve(body, context.Options(sensitivity_dt=0.0), registry=registry)
        off, _x2 = sv.solve(body, context.Options(sensitivity_dt=0.0, materials="legacy"))
        return on, off

    def test_earth_both_put_back(self):
        on, off = self._pair("engine/bodies/earth.yaml", self._registry("W-L1-01", "P5-F1"))
        self.assertIsInstance(on, sv.result.Answer)
        self.assertEqual(_values(on), _values(off))

    def test_venus_both_put_back(self):
        on, off = self._pair("engine/bodies/venus.yaml", self._registry("W-L1-01", "P5-F1"))
        self.assertEqual(type(on), type(off))
        self.assertEqual(_values(on), _values(off))

    def test_earth_as_shipped_moves(self):
        on, off = self._pair("engine/bodies/earth.yaml", None)
        self.assertIsInstance(on, sv.result.Answer)
        self.assertNotEqual(_values(on), _values(off))


class RecordRefusals(unittest.TestCase):
    def test_a_record_refusal_maps_to_its_registry_id(self):
        r = mv.RecordRefusal("h2o", 5.0e9, 120.0, "input.material_out_of_data", "past t_min")
        node = {"m": 1.0, "r": 1.0, "P": 4.9e9, "T": 121.0}
        got = sv._to_refusal(st.Stop("refused", r, node), "fixture.solve", 1.0, "R", "scan")
        self.assertEqual((got.id, got.evidence["refusal"], got.evidence["material_id"]),
                         ("solve.material_record", "input.material_out_of_data", "h2o"))
        self.assertIn("solve.material_record", refusals.REGISTRY)

    def test_melting_stop_maps(self):
        got = sv._to_refusal(st.Stop("melting_not_in_phase2", {"material_id": "h2o", "boundary": ("water1", "VI"),
                                                               "p": 1.0e9, "t": 300.0},
                                     {"m": 1.0, "r": 1.0, "P": 1.0e9, "T": 300.0}),
                             "fixture.solve", 1.0, "R", "accepted")
        self.assertEqual(got.id, "solve.melting_not_in_phase2")


if __name__ == "__main__":
    unittest.main()
