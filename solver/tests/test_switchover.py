# 전환 등록 시험 — 기록 뷰의 사건 · 옛 물질과의 패스 동일성(SW1) · 기록 거절의 대응 (switch-over registration §2, §6)
"""Switch-over registration (rewrite/switchover-registration.frozen.md) §2 and §6, the parts that land before the
resolver switches: a record view's events, the identity of a pass through fe_prem_legacy with the legacy fe_prem
(r2 SW1), and a record view's refusals reaching the solver's refusal registry.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_switchover
"""
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
        self.assertEqual(len([n for n in _notes_of(_record("h2o"), [(1e7, 200.0)])     # no boundary: every read
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
            def inward(body, vs, x, opt):
                Planted.armed = arm_at_root or x != x_root
                try:
                    return real(body, vs, x, opt)
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
    """An Answer's values for the step-1 identity: quantities with solve_id masked (it names the material bytes, so it
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
        self.assertEqual(on["core"].material_id, "fe_prem_legacy")             # step 1's one-line map
        self.assertTrue(all(isinstance(v, lm.LegacyView) for k, v in on.items() if k != "core"))
        self.assertIsNone(sv.registry_for(self.earth, context.Options(materials="legacy")))
        off = sv._views(self.earth)
        self.assertIsInstance(off["core"], lm.LegacyView)

    def test_a_body_naming_no_record_loads_no_registry(self):
        mars, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        self.assertIsNone(sv.registry_for(mars, context.Options()))

    def test_an_unavailable_record_refuses_and_never_falls_back(self):
        from types import SimpleNamespace as NS
        stop = mr.LoadStop("material.library_pin", {"file": "fe_prem_legacy.yaml", "why": "planted pin mismatch"})
        reg = NS(get=lambda rid: stop if rid == "fe_prem_legacy" else None)
        got = sv._views(self.earth, registry=reg)
        self.assertEqual((got.id, got.evidence["material_id"], got.evidence["load_stop"]),
                         ("input.material_record_unavailable", "fe_prem_legacy", "material.library_pin"))

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


class Step1Identity(unittest.TestCase):
    """§6.6: Earth and Venus through fe_prem_legacy reproduce the switch-off answers (solve_id masked)."""

    def _pair(self, path):
        body, _aside = from_v1.load_v1(path)
        on, _x = sv.solve(body, context.Options(sensitivity_dt=0.0))
        off, _x2 = sv.solve(body, context.Options(sensitivity_dt=0.0, materials="legacy"))
        return on, off

    def test_earth(self):
        on, off = self._pair("engine/bodies/earth.yaml")
        self.assertIsInstance(on, sv.result.Answer)
        self.assertEqual(_values(on), _values(off))
        self.assertNotEqual(on.quantities[0].provenance.solver.solve_id,
                            off.quantities[0].provenance.solver.solve_id)          # the material bytes moved

    def test_venus(self):
        on, off = self._pair("engine/bodies/venus.yaml")
        self.assertEqual(type(on), type(off))
        self.assertEqual(_values(on), _values(off))


class RecordRefusals(unittest.TestCase):
    def test_a_record_refusal_maps_to_its_registry_id(self):
        r = mv.RecordRefusal("h2o", 5.0e9, 120.0, "input.material_out_of_data", "past t_min")
        got = sv._to_refusal(st.Stop("refused", r), "fixture.solve", 1.0, "R", "scan")
        self.assertEqual((got.id, got.evidence["refusal"], got.evidence["material_id"]),
                         ("solve.material_record", "input.material_out_of_data", "h2o"))
        self.assertIn("solve.material_record", refusals.REGISTRY)

    def test_melting_stop_maps(self):
        got = sv._to_refusal(st.Stop("melting_not_in_phase2", {"material_id": "h2o", "boundary": ("water1", "VI"),
                                                               "p": 1.0e9, "t": 300.0}),
                             "fixture.solve", 1.0, "R", "accepted")
        self.assertEqual(got.id, "solve.melting_not_in_phase2")


if __name__ == "__main__":
    unittest.main()
