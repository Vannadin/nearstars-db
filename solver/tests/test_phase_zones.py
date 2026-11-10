# 상 구간 행 시험 — 풀린 몸의 층별 행·이음·사건 끝·결정성·받아들인 패스만 읽기, 그리고 h2o·집합표 고정장치 (zones-prereg §4.2–§4.3, 사후 노트 1)
"""Tests of `rewrite/layers/zones-prereg.frozen.md` §4.2–§4.3 (artifacts blob 244711f0) and its post-freeze note 1.

Solved states (switch off): Earth 1700 K, Mars, Venus, Dante and Pandora as declared. Earth 1600 K with the switch on is
checked in the landing proof (solver/landing/zones_identity.py), not here (68 n1 on rev 1: ≈ 13 min). Every control
must go red. Fixtures (f) and (g) need no solve.

Run from the engine tree root:  <gate venv>/python -m unittest solver.tests.test_phase_zones
"""
import dataclasses
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from solver import context, fall_sets, from_v1, phase_zones as pz, result
from solver import solve as sv

REPO = Path(__file__).resolve().parents[2]


def _body(stem, t_pot=None):
    got = from_v1.load_v1(str(REPO / "engine" / "bodies" / f"{stem}.yaml"))
    body = got[0] if isinstance(got, tuple) else got
    if t_pot is not None:
        body = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=t_pot))
    return body


_CACHE = {}


def _solve(stem, t_pot=None):
    """(answer, warm, body, views, acc) of one solve, the accepted pass captured from collect's own call."""
    key = (stem, t_pot)
    if key not in _CACHE:
        seen = {}
        real = pz.collect

        def spy(body, views, acc):
            seen.update(views=views, acc=acc)
            return real(body, views, acc)
        pz.collect = spy
        try:
            body = _body(stem, t_pot)
            ans, warm = sv.solve(body, context.Options())
        finally:
            pz.collect = real
        _CACHE[key] = (ans, warm, body, seen.get("views"), seen.get("acc"))
    return _CACHE[key]


def _rows(ans, layer):
    return [z for z in ans.zones if z.layer == layer]


class Type(unittest.TestCase):
    def test_zoned_answer_is_a_result_answer_named_answer(self):
        ans = _solve("earth", 1700.0)[0]
        self.assertIsInstance(ans, result.Answer)
        self.assertIsInstance(ans, pz.Answer)
        self.assertEqual(type(ans).__name__, "Answer")

    def test_plain_bytes_are_z1(self):
        # frozen Z1: result.Answer's fields, then «zones»; without zones, the base Answer's plain form exactly
        ans = _solve("earth", 1700.0)[0]
        p = result.plain(ans)
        self.assertEqual(list(p), ["type"] + [f.name for f in dataclasses.fields(result.Answer)] + ["zones"])
        base = result.Answer(ans.quantities, ans.boundaries, ans.profiles, ans.missing, ans.notes)
        self.assertEqual({k: v for k, v in p.items() if k != "zones"}, result.plain(base))

    def test_result_py_edit_trips_the_fall_set_stamp(self):
        # post-freeze note 1: result.py is in the fall sets' read closure; a tree whose result.py differs refuses
        self.assertIn("result", fall_sets.closure(REPO))
        stamp = {"solver": {m: fall_sets.blob(REPO / "solver" / f"{m}.py") for m in fall_sets.closure(REPO)},
                 "engine_static": fall_sets.engine_static(REPO), "engine": {}, "solver_data": {},
                 "switches": fall_sets._switches()}
        fall_sets.check_stamp(stamp, REPO, "unplanted")                 # the unplanted tree passes its own stamp
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for top in ("engine",):
                os.symlink(REPO / top, root / top)
            (root / "solver").mkdir()
            for f in (REPO / "solver").iterdir():
                if f.name != "result.py":
                    os.symlink(f, root / "solver" / f.name)
            shutil.copy(REPO / "solver" / "result.py", root / "solver" / "result.py")
            with open(root / "solver" / "result.py", "a", encoding="utf-8") as fh:
                fh.write("\n# planted\n")
            with self.assertRaises(Exception) as cm:
                fall_sets.check_stamp(stamp, root, "planted")
            self.assertIn("solver/result.py", str(cm.exception))


class Rows(unittest.TestCase):
    def test_earth_1700_off(self):
        ans = _solve("earth", 1700.0)[0]
        lith, mantle, core = _rows(ans, "lithosphere"), _rows(ans, "mantle"), _rows(ans, "core")
        self.assertEqual([z.label for z in lith], ["mgsio3_en"])
        self.assertEqual([z.label for z in mantle], ["mgsio3_en", "mgsio3_prem"])
        self.assertEqual(mantle[0].base_by, "event:seam:2.383e+10")
        self.assertEqual(mantle[0].base, mantle[1].top)
        self.assertAlmostEqual(mantle[0].base[2], 2.383e10, delta=2.383e10 * 1e-9)
        self.assertFalse(any(z.top_by == "event:seam:2e+10" or z.base_by == "event:seam:2e+10" for z in ans.zones))
        self.assertEqual([z.label for z in core], ["fe_prem"])
        self.assertEqual(core[0].record_phases, 1)
        self.assertEqual(core[0].single_phase_why, pz.FE_PREM_WHY)
        self.assertEqual(pz.check_rows(ans), [])

    def test_mars_declared_off(self):
        ans, _w, _b, views, _acc = _solve("mars")
        self.assertEqual([z.label for z in _rows(ans, "mantle")], ["mantle_assemblage"])
        self.assertEqual([z.label for z in _rows(ans, "basal")], ["mantle_assemblage"])
        core = _rows(ans, "core")
        self.assertEqual(len(core), 1)
        self.assertTrue(core[0].label.startswith("fe_core_"), core[0].label)
        self.assertEqual(core[0].record_phases, max(1, len(views["core"].mat.phases)))
        self.assertEqual(pz.check_rows(ans), [])

    def test_venus_dante_pandora_rows_hold(self):
        for stem in ("venus", "dante_fixture", "pandora"):
            with self.subTest(body=stem):
                ans = _solve(stem)[0]
                self.assertIsInstance(ans, result.Answer, ans)
                self.assertTrue(ans.zones)
                self.assertEqual(pz.check_rows(ans), [])


class Checks(unittest.TestCase):
    def test_a_tiling_control_drop_one_row(self):
        ans = _solve("earth", 1700.0)[0]
        cut = dataclasses.replace(ans, zones=tuple(z for z in ans.zones if z.label != "mgsio3_en" or z.layer != "mantle"))
        self.assertTrue(pz.check_rows(cut))

    def test_b_control_events_ignored_splits_between_nodes(self):
        ans, _w, body, views, acc = _solve("earth", 1700.0)
        zones = pz.collect(body, views, dataclasses.replace(acc, events_at=[]))
        self.assertIn("between_nodes", [z.base_by for z in zones])
        self.assertTrue(pz.check_rows(dataclasses.replace(ans, zones=zones)))

    def test_b_control_label_from_the_event_node_is_red(self):
        # 68 B2 on rev 0: the landed node reads the upper side (mgsio3_en at 2.383e10); taking it as interior is red
        ans, _w, body, views, acc = _solve("earth", 1700.0)
        real = pz._segments

        def with_event_node(labels, cuts):
            return real([labels[0]] + [labels[i - 1] if i - 1 in cuts and i - 1 > 0 else labels[i]
                                       for i in range(1, len(labels))], cuts)
        pz._segments = with_event_node
        try:
            zones = pz.collect(body, views, acc)
        finally:
            pz._segments = real
        self.assertTrue(pz.check_rows(dataclasses.replace(ans, zones=zones)))

    def test_c_event_node_either_side_gives_equal_rows(self):
        ans, _w, body, views, acc = _solve("earth", 1700.0)
        real = pz._read
        for forced in ("mgsio3_en", "mgsio3_prem"):
            with self.subTest(forced=forced):
                pz._read = lambda view, mid, p, t, f=forced: f if p == 2.383e10 else real(view, mid, p, t)
                try:
                    zones = pz.collect(body, views, acc)
                finally:
                    pz._read = real
                self.assertEqual(zones, ans.zones)

    def test_d_determinism_and_warm_start(self):
        ans, warm, body, _v, _a = _solve("earth", 1700.0)
        again, _w2 = sv.solve(body, context.Options())
        self.assertEqual(result.plain(again.zones), result.plain(ans.zones))
        warmed, _w3 = sv.solve(body, context.Options(), warm)
        self.assertEqual(result.plain(warmed.zones), result.plain(ans.zones))

    def test_e_reads_only_the_accepted_pass(self):
        real, calls = pz._read, [0]

        def spy(*a):
            calls[0] += 1
            return real(*a)
        pz._read = spy
        try:
            ans, _w = sv.solve(_body("earth", 1700.0), context.Options())
        finally:
            pz._read = real
        interior = sum(max(0, len(cols["m"]) - 2) for cols in ans.profiles.values())
        self.assertEqual(calls[0], interior)


class _NoReadView:
    """A duck-typed view the solver accepts with state() alone (test_solve's Uniform): no phase_read, no mat.phase_at."""

    def __init__(self, rho, mat=None):
        self.rho, self.mat, self.p_floor = rho, mat, 0.0

    def state(self, p, t, guess):
        return (self.rho, 0.0, ())


def _two_layer(mantle_mat=None):
    from solver import body as b
    layers = (b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.5)), b.Layer("mantle", "mantle", "y"))
    body = b.Body("fixture", "planet", b.SurfaceState(5.0e24, t_pot=0.0), layers, b.Closure("R", 1e5, 1e8))
    return body, {"core": _NoReadView(6000.0), "mantle": _NoReadView(3000.0, mantle_mat)}


class NoRead(unittest.TestCase):
    """Zones note 2: a view with no phase read gives one disclosed row per entered layer, never a raise and never a _read
    call; §4.3 (b) counts that row as a finding. Engine 55794a9f raised TypeError here (30 suite errors on the PC)."""

    def _solve(self, views_body):
        body, views = views_body
        real, calls = pz._read, [0]

        def spy(*a):
            calls[0] += 1
            return real(*a)
        pz._read = spy
        try:
            ans, _w = sv.solve(body, views=views)
        finally:
            pz._read = real
        return ans, calls[0]

    def test_no_read_layers_give_one_disclosed_row_each(self):
        ans, calls = self._solve(_two_layer())
        self.assertIsInstance(ans, pz.Answer, getattr(ans, "text", ans))
        self.assertEqual(calls, 0)
        self.assertEqual(set(ans.profiles), {"core", "mantle"})
        for lid in ("mantle", "core"):
            rows = _rows(ans, lid)
            self.assertEqual(len(rows), 1, rows)
            z, cols = rows[0], ans.profiles[lid]
            self.assertEqual((z.label, z.record_phases, z.single_phase_why, z.crossings),
                             (pz.ZONE_NO_READ, 1, pz.NO_READ_WHY, ()))
            self.assertEqual(z.top[0], cols["m"][0])
            self.assertEqual(z.base[0], cols["m"][-1])
        self.assertEqual([z.layer for z in ans.zones], ["mantle", "core"])
        self.assertEqual(_rows(ans, "mantle")[0].base_by, _rows(ans, "core")[0].top_by)
        bad = pz.check_rows(ans)
        self.assertEqual(sorted(x.split(":")[0] for x in bad), ["(b) core", "(b) mantle"], bad)

    def test_control_a_view_with_phase_at_is_read(self):
        ph = SimpleNamespace(name="y_ph", p_min=0.0, p_max=float("inf"), gamma_sets=None)
        mat = SimpleNamespace(phases=(ph,), phase_at=lambda p: ph)
        ans, calls = self._solve(_two_layer(mat))
        self.assertIsInstance(ans, pz.Answer, getattr(ans, "text", ans))
        self.assertGreater(calls, 0)
        self.assertEqual({z.label for z in _rows(ans, "mantle")}, {"y_ph"})
        self.assertEqual({z.label for z in _rows(ans, "core")}, {pz.ZONE_NO_READ})

    def test_control_planted_always_read_raises_as_55794a9f(self):
        real = pz._has_read
        pz._has_read = lambda view: True
        try:
            with self.assertRaisesRegex(TypeError, "has no phase read"):
                sv.solve(*_two_layer()[:1], views=_two_layer()[1])
        finally:
            pz._has_read = real


def _fixture_acc(layer_id, path, events):
    return SimpleNamespace(profiles={layer_id: path}, boundaries=[], floor_end=False,
                           events_at=[(layer_id, name, m, y) for name, m, y in events])


class Fixtures(unittest.TestCase):
    def test_f_record_view_h2o_rows_split_at_landed_events(self):
        from solver import material_registry as mr, material_view as mv
        reg = mr.load()
        view = mv.RecordView(mv.thaw_plain(reg.records["h2o"]), 250.0)
        t = 250.0
        ps = [1e5 * 1.25 ** k for k in range(0, 45)]                  # 0.1 MPa to ≈ 2.3 GPa along 250 K
        reads = [view.phase_read(p, t) for p in ps]
        nodes, events = [], []
        for k, p in enumerate(ps):
            if k and reads[k] != reads[k - 1] and isinstance(reads[k], str) and isinstance(reads[k - 1], str):
                lo, hi = ps[k - 1], p                               # land the change by bisection, as a stepper would
                for _ in range(60):
                    mid = 0.5 * (lo + hi)
                    lo, hi = (mid, hi) if view.phase_read(mid, t) == reads[k - 1] else (lo, mid)
                m_e = float(len(nodes))
                nodes.append((m_e, (1.0, hi, t, t, 0.0, 0.0), None))
                events.append((f"phase:{reads[k - 1]}|{reads[k]}", m_e, nodes[-1][1]))
            nodes.append((float(len(nodes)), (1.0, p, t, t, 0.0, 0.0), None))
        layer = SimpleNamespace(id="ocean", material="h2o")
        zones = pz.collect(SimpleNamespace(layers=[layer]), {"ocean": view}, _fixture_acc("ocean", nodes, events))
        labels = [z.label for z in zones]
        self.assertEqual(labels, [r for i, r in enumerate(reads) if isinstance(r, str) and (i == 0 or r != reads[i - 1])])
        self.assertEqual([z.base_by for z in zones[:-1]], [f"event:{e[0]}" for e in events])
        self.assertEqual(zones[0].record_phases, len(view.phases))
        # a node whose read is a Stop reads stop:<kind> (§2.2, n5): one more interior node far outside the data
        stop_nodes = nodes[:2] + [(2.5, (1.0, 1e5, 5000.0, 5000.0, 0.0, 0.0), None), (3.0, nodes[2][1], None)]
        zs = pz.collect(SimpleNamespace(layers=[layer]), {"ocean": view}, _fixture_acc("ocean", stop_nodes, []))
        self.assertIn("stop:refused", [z.label for z in zs])

    def test_g_assemblage_rows_one_row_with_crossings(self):
        from solver import material_assemblage as ma

        class Fake(ma.AssemblageView):
            def __init__(self):
                self.material_id = "silicate_slb_fake"

            def phase_read(self, p, t):
                return "slb_assemblage"
        y = lambda p: (1.0, p, 1600.0, 1600.0, 0.0, 0.0)
        nodes = [(float(k), y(1e9 * k), None) for k in range(8)]
        events = [("seam:3e+09", 3.0, y(3e9)), ("phase:edge61:a|b", 2.0, y(2e9)),
                  ("coexist-in:phase:swap1:a|c", 4.0, y(4e9)), ("coexist-out:phase:swap1:a|c", 5.0, y(5e9))]
        layer = SimpleNamespace(id="mantle", material="silicate")
        zones = pz.collect(SimpleNamespace(layers=[layer]), {"mantle": Fake()}, _fixture_acc("mantle", nodes, events))
        self.assertEqual(len(zones), 1)
        self.assertEqual(zones[0].label, "slb_assemblage")
        self.assertEqual(zones[0].single_phase_why, pz.ASSEMBLAGE_WHY)
        self.assertEqual([c[0] for c in zones[0].crossings],
                         ["phase:edge61:a|b", "coexist-in:phase:swap1:a|c", "coexist-out:phase:swap1:a|c"])


if __name__ == "__main__":
    unittest.main()
