# 매끄러운 읽기 보기 시험 — 읽기 사건 배선, 거절의 이름과 재시도, 선택기, 지각층 두 사건 묶음, 패스별 집계, 곡선 끝 걸음, 흔적 감시 무해 (read-view 등록 A3·A4·A7·A8·A9, §4.8–4.9, N2–N4; C1)
"""Read-view registration (rewrite/read-view/prereg-read-view.frozen.md, artifacts main 99df438b8; note 1 at 9ff9ecaf6):
the C1 lines on a fixture read with analytic fields, and the mutants that must fail them.

Run from the worktree root:  PY -B -m unittest solver.tests.test_read_view
"""
import dataclasses
import inspect
import math
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from solver import body as b
from solver import context, events, lid, read_view as rv, refusals, rhs
from solver import solve as sv
from solver import stepper as st
from solver.tests._mutants import variant


class ReadRefusal(ValueError):
    """The read's refusal class, as c8's proto/inv.py defines it (agreed 11-18): .kind and .why, str(e) == why."""

    def __init__(self, kind, why):
        super().__init__(why)
        self.kind, self.why = kind, why


class Curve:
    """P_b(T) = p0 + k (T − t0) on [t_lo, t_hi], None outside (a curve's T range)."""

    def __init__(self, name, p0, k=0.0, t0=1600.0, t_lo=-math.inf, t_hi=math.inf):
        self.name, self.p0, self.k, self.t0, self.t_lo, self.t_hi = name, p0, k, t0, t_lo, t_hi

    def p_b(self, t):
        return None if not (self.t_lo <= t <= self.t_hi) else self.p0 + self.k * (t - self.t0)


class FixtureRead:
    """Two fields per curve side, analytic: below a curve's P_b the field keeps ρ and dT/dP; each curve crossed adds
    `drho` to ρ. `refuse(p, t)` → a kind or None plants a refusal."""

    def __init__(self, curves, rho=3300.0, drho=300.0, dtdp=1e-8, refuse=None):
        self.curves, self.rho, self.drho, self.dtdp, self.refuse = curves, rho, drho, dtdp, refuse
        self.calls = []

    def state(self, p, t, field=None, pin=None):
        self.calls.append((p, t))
        if self.refuse is not None:
            k = self.refuse(p, t)
            if k is not None:
                raise ReadRefusal(k, f"planted {k} at P {p:.6g}, T {t:.6g}")
        n = sum(1 for c in self.curves if c.p_b(t) is not None and p >= c.p_b(t))
        return {"rho": self.rho + n * self.drho, "dtdp": self.dtdp, "s": 0.0, "c_p": 1200.0, "alpha": 3e-5,
                "K_T": 1.5e11, "field": f"f{n}"}

    def events(self, t_index=2):
        out = []
        for c in self.curves:
            def g(m, y, c=c, ti=t_index):
                pb = c.p_b(y[ti])
                return None if pb is None else y[1] - pb
            out.append(st.Event(c.name, g, scale=max(abs(c.p0), 1.0), terminal=False, seam=True, component=1))
        return out


M = 5.0e24


def _body(t_pot=1600.0):
    layers = (b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.5)), b.Layer("mantle", "mantle", "y"))
    return b.Body("fixture", "planet", b.SurfaceState(M, t_pot=t_pot), layers, b.Closure("R", 1e5, 1e8))


class Uniform:
    def __init__(self, rho):
        self.rho, self.mat, self.p_floor = rho, None, 0.0

    def state(self, p, t, guess):
        return (self.rho, 0.0, ())


R0 = 6.0e6
OPT = context.Options()


def _pass(read, t_pot=1600.0):
    view = rv.ReadView(read, 0.0, "fixture_read")
    return sv.inward(_body(t_pot), {"core": Uniform(9000.0), "mantle": view}, R0, OPT), view


# ── A3: plan wiring (and N2) ─────────────────────────────────────────────────────────────────────────────────────
class PlanWiring(unittest.TestCase):
    def check(self):
        read = FixtureRead([Curve("c0", 2.0e10, 1e6)])
        view = rv.ReadView(read, 0.0, "fixture_read")
        evs, cap = sv._plan(view)
        self.assertEqual([e.name for e in evs], ["c0"])
        self.assertIsNone(cap)
        self.assertIsNone(sv._band(view))
        out, _ = _pass(read)
        self.assertIsInstance(out, sv.PassOut, out)
        self.assertIn("c0", out.events)                  # the read's curve is landed
        return out

    def test_read_events_drive_the_pass(self):
        out = self.check()
        p_land = [y[1] for (_l, n, _m, y) in out.events_at if n == "c0"][0]
        t_land = [y[2] for (_l, n, _m, y) in out.events_at if n == "c0"][0]
        self.assertLessEqual(abs(p_land - (2.0e10 + 1e6 * (t_land - 1600.0))), 1e-12 * 2.0e10 * 10)

    PLAN_ANCHOR = ("    if got is None and rv.is_read_view(view):         # read-view registration §1: the read's own events, "
                   "no table cap\n")

    def test_N2_identity_passes_mutant_fails(self):
        """N2: _plan rebuilt from source (identity) passes A3's check; without the read branch it fails."""
        with mock.patch.object(sv, "_plan", variant(sv._plan)):
            self.check()
        mut = variant(sv._plan, self.PLAN_ANCHOR, "    if False:\n")
        with mock.patch.object(sv, "_plan", mut):
            with self.assertRaises((AssertionError, AttributeError, TypeError)):
                self.check()

# ── A4 (a) at C1, and N3: a refusal the path reaches surfaces as solve.read_refusal ─────────────────────────────
class Refusals(unittest.TestCase):
    def run_cut(self):
        read = FixtureRead([], refuse=lambda p, t: "cut" if p > 4.0e10 else None)
        out, view = _pass(read)
        self.assertIsInstance(out, st.Stop)
        ref = sv._to_refusal(out, "fixture", R0, "R", "scan")
        return out, ref

    def test_on_path_cut_surfaces_named(self):
        out, ref = self.run_cut()
        self.assertEqual(ref.id, "solve.read_refusal")
        ev = dict(ref.evidence)
        self.assertEqual(ev["kind"], "cut")
        self.assertIn("planted cut", ev["why"])
        self.assertGreaterEqual(ev["read_retried"].get("cut", 0), 1)   # r2 B6: the refused pass keeps its count
        self.assertIn("state", ev)

    def test_N3_identity_passes_mutant_fails(self):
        """N3: _to_refusal rebuilt from source maps the read refusal; without its branch it raises «unmapped»."""
        out, _ = self.run_cut()
        self.assertEqual(variant(sv._to_refusal)(out, "fixture", R0, "R", "scan").id, "solve.read_refusal")
        src = inspect.getsource(sv._to_refusal)
        a = src[src.index('    if stop.kind == "read_refusal":'):src.index('    if type(rec).__name__ == "RecordRefusal":')]
        mut = variant(sv._to_refusal, a, "")
        with self.assertRaisesRegex(RuntimeError, "unmapped solver stop"):
            mut(out, "fixture", R0, "R", "scan")

    def test_other_exception_is_an_engine_error(self):
        def boom(p, t):
            if p > 4.0e10:
                raise ZeroDivisionError("a read bug")
        read = FixtureRead([])
        read.refuse = None
        orig = read.state
        read.state = lambda p, t, field=None, pin=None: (boom(p, t), orig(p, t, field))[1]
        with self.assertRaises(ZeroDivisionError):
            _pass(read)


# ── A4 (b)'s mechanism at C1: an off-path extent refusal is retried, the run ends on the unplanted answer ───────
class OffPathExtent(unittest.TestCase):
    A, W = 1.0, 3.0

    def run_with(self, refuse):
        pmax = 2 * self.A / self.W
        read = FixtureRead([], refuse=refuse)
        view = rv.ReadView(read, 0.0, "fixture_read")

        def f(x, y):
            got = view.state(y[1], 1600.0)
            if isinstance(got, st.Stop):
                return got
            return (0.0, self.A * math.sin(self.W * x), 0.0, 0.0, 0.0, 0.0)
        opt = st.Options(rtol=1e-8, floors=(1.0, 1e-9, 1.0, 1.0, 1.0, 1.0), h0=3.0, h_min=1e-12, h_max=50.0,
                         max_steps=100000, event_tol=1e-12, event_rewalks=32, event_min_progress=1e-9)
        return st.run(f, 0.0, (1.0, 0.0, 1.0, 1.0, 0.0, 0.0), 4.0, opt), view, pmax

    def test_retried_and_same_answer(self):
        r0, _v0, pmax = self.run_with(None)
        r1, v1, _ = self.run_with(lambda p, t: "extent" if p > 1.5 * 2 * self.A / self.W else None)
        self.assertEqual(r1.stop.kind, "end")
        self.assertLessEqual(abs(r1.y[1] - r0.y[1]), 10 * 1e-8 * max(abs(r0.y[1]), 1e-9))
        self.assertGreaterEqual(v1.read_retried.get("extent", 0), 1)
        self.assertGreaterEqual(r1.counters.refused_stage, 1)


# ── A7: the selector's loader (stamp, missing file, stale stamp) and its refusal ─────────────────────────────────
class Selector(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "reads").mkdir()
        (self.tmp / "reads" / "loader.py").write_text(
            "# 시험용 읽기 적재기\nimport json\n\ndef load_read(paths):\n    with open(paths[0]) as f:\n        return json.load(f)\n")
        (self.tmp / "reads" / "data.json").write_text('{"ok": 1}\n')
        self.files = ["reads/loader.py", "reads/data.json"]

    def test_matching_stamp_loads(self):
        stamp = rv.stamp_of(self.files, self.tmp)
        self.assertEqual(rv.load(self.files, stamp, self.tmp), {"ok": 1})

    def test_stale_stamp_refuses(self):
        stamp = rv.stamp_of(self.files, self.tmp)
        (self.tmp / "reads" / "data.json").write_text('{"ok": 2}\n')
        with self.assertRaises(rv.ReadUnavailable) as cm:
            rv.load(self.files, stamp, self.tmp)
        self.assertEqual(cm.exception.reason, "stale_stamp")

    def test_missing_file_refuses(self):
        stamp = rv.stamp_of(self.files, self.tmp)
        (self.tmp / "reads" / "data.json").unlink()
        with self.assertRaises(rv.ReadUnavailable) as cm:
            rv.load(self.files, stamp, self.tmp)
        self.assertEqual(cm.exception.reason, "missing_file")

    def test_paths_outside_the_repo_refuse(self):
        for files in (["../x.py"], [str(self.tmp / "reads" / "loader.py")], ["reads/data.json"]):
            with self.assertRaises(rv.ReadUnavailable) as cm:
                rv.load(files, "0" * 64, self.tmp)
            self.assertIn(cm.exception.reason, ("path_outside_repo", "loader_not_python"))

    def test_nothing_is_imported_before_the_stamp_matches(self):
        (self.tmp / "reads" / "loader.py").write_text("raise SystemExit('imported')\n")
        with self.assertRaises(rv.ReadUnavailable):
            rv.load(self.files, "0" * 64, self.tmp)

    def test_order_and_rename_move_the_stamp(self):
        self.assertNotEqual(rv.stamp_of(self.files, self.tmp), rv.stamp_of(self.files[::-1], self.tmp))

    def test_registry_reaches_a_loader_that_takes_it(self):     # 11-21: the solve's registry, the same object
        (self.tmp / "reads" / "loader.py").write_text(
            "# 시험용 읽기 적재기\nimport json\n\ndef load_read(paths, registry=None):\n"
            "    with open(paths[0]) as f:\n        return {**json.load(f), 'reg': registry}\n")
        stamp = rv.stamp_of(self.files, self.tmp)
        reg = object()
        self.assertIs(rv.load(self.files, stamp, self.tmp, registry=reg)["reg"], reg)
        self.assertIsNone(rv.load(self.files, stamp, self.tmp)["reg"])

    def test_registry_not_passed_to_a_loader_without_it(self):  # an older read package still loads
        stamp = rv.stamp_of(self.files, self.tmp)
        self.assertEqual(rv.load(self.files, stamp, self.tmp, registry=object()), {"ok": 1})

    def test_view_refusal_is_named(self):
        layer = _body().layers[1]
        ref = sv._view_refusal(_body(), layer, ("read_unavailable", ("rec_x", "stale_stamp", "declared a, files b")))
        self.assertEqual(ref.id, "input.material_read_unavailable")
        self.assertEqual(dict(ref.evidence)["reason"], "stale_stamp")


# ── A8: the lid carries both event sets (r2 B2) ─────────────────────────────────────────────────────────────────
M_E, R_E, T_S, T_POT, D = 5.972e24, 6.371e6, 293.0, 1600.0, 135e3
RS = rhs.r_scale_of(M_E, 5514.0)


class LidWiring(unittest.TestCase):
    def lid_read(self, refuse=None):
        # c_loc: crossed by the lid's own T only (T range 293–1200 K); c_ad: by T_ad only (1500–1800 K)
        return FixtureRead([Curve("c_loc", 1.0e9, t_lo=250.0, t_hi=1200.0),
                            Curve("c_ad", 2.0e9, t_lo=1500.0, t_hi=1800.0)], drho=10.0, refuse=refuse)

    def run_lid(self, read, wiring=None):
        view = rv.ReadView(read, 0.0, "fixture_read")
        w = wiring if wiring is not None else sv._lid_wiring(view)
        return lid.lid_pass(view, M_E, R_E, D, 0.0, T_S, T_POT, RS, **w), view, w

    def names(self, res):
        return [e[0] for e in res.events]

    def test_both_sets_live_and_landed(self):
        res, view, w = self.run_lid(self.lid_read())
        self.assertIsNone(w["h_cap"])
        self.assertIsNone(w["step_check"])
        self.assertEqual(sorted(e.name for e in w["events"]), sorted(["c_loc", "c_ad", "c_loc:ad", "c_ad:ad"]))
        self.assertNotIsInstance(res, st.Stop, res)
        self.assertIn("c_loc", self.names(res))        # lands on y[3]
        self.assertIn("c_ad:ad", self.names(res))      # lands on y[2]
        for name, comp, pb in (("c_loc", 3, 1.0e9), ("c_ad:ad", 2, 2.0e9)):
            y = [e[2] for e in res.events if e[0] == name][0]
            self.assertLessEqual(abs(y[1] - pb), 1e-12 * pb * 10)

    def test_each_set_removed_misses_its_curve(self):
        view = rv.ReadView(self.lid_read(), 0.0, "fixture_read")
        full = sv._lid_wiring(view)
        only3 = dict(full, events=tuple(e for e in full["events"] if not e.name.endswith(":ad")))
        only2 = dict(full, events=tuple(e for e in full["events"] if e.name.endswith(":ad")))
        r3, _, _ = self.run_lid(self.lid_read(), only3)
        r2, _, _ = self.run_lid(self.lid_read(), only2)
        self.assertNotIn("c_ad:ad", self.names(r3))
        self.assertNotIn("c_loc", self.names(r2))

    def test_refusal_at_t_ad_only_surfaces(self):
        read = self.lid_read(refuse=lambda p, t: "cut" if 1.5e9 < p < 2.5e9 and t >= 1600.0 else None)
        res, _, _ = self.run_lid(read)
        self.assertIsInstance(res, st.Stop)
        inner = res.record if isinstance(res.record, st.Stop) else res
        self.assertEqual(getattr(inner, "kind", None), "read_refusal")
        self.assertEqual(inner.record["kind"], "cut")


# ── §1 collection (r2 B3, B6) ──────────────────────────────────────────────────────────────────────────────────
class Collect(unittest.TestCase):
    def test_counts_sum_over_views_and_reset(self):
        r1 = FixtureRead([], refuse=lambda p, t: "extent")
        v1, v2 = rv.ReadView(r1, 0.0, "a"), rv.ReadView(r1, 0.0, "b")
        v1.state(1.0, 1.0)
        v1.state(1.0, 1.0)
        v2.state(1.0, 1.0)
        out = sv.PassOut(None, 0.0, (), 0.0, None)
        rv.with_counts(out, {"x": v1, "y": v2})
        self.assertEqual(out.read_counts["read_retried"], {"extent": 3})
        v1.reset_pass()
        self.assertEqual(v1.read_retried, {})

    def test_stop_with_and_without_state_carries_counts(self):
        r1 = FixtureRead([], refuse=lambda p, t: "past_deepest")
        v1 = rv.ReadView(r1, 0.0, "a")
        v1.state(1.0, 1.0)
        for s0 in (st.Stop("x"), st.Stop("x", state={"m": 1.0})):
            got = rv.with_counts(s0, {"v": v1})
            self.assertEqual(got.state["read_retried"], {"past_deepest": 1})
        self.assertEqual(rv.with_counts(st.Stop("x", state={"m": 1.0}), {"v": v1}).state["m"], 1.0)

    def test_refused_pass_keeps_its_count(self):
        out, ref = Refusals().run_cut()
        self.assertIn("read_retried", out.state)


# ── §4.8 curve ends inside a step (A9, a report line) and §4.9 the graze monitor ─────────────────────────────────
class CurveEndsAndGraze(unittest.TestCase):
    def test_curve_end_inside_a_step_is_counted_once(self):
        read = FixtureRead([Curve("c_end", 1.0e11, t_lo=1500.0, t_hi=1650.0)])
        view = rv.ReadView(read, 0.0, "fixture_read")
        evs = view.events()
        view.note_step(evs, 0.0, (1.0, 0.0, 1600.0, 1600.0, 0.0, 0.0), 1.0, (1.0, 1.0, 1700.0, 1700.0, 0.0, 0.0))
        view.note_step(evs, 1.0, (1.0, 1.0, 1700.0, 1700.0, 0.0, 0.0), 2.0, (1.0, 2.0, 1800.0, 1800.0, 0.0, 0.0))
        self.assertEqual([n for n, _p in view.curve_end_steps], ["c_end"])

    def test_graze_monitor_inert_on_a_read_view(self):
        view = rv.ReadView(FixtureRead([Curve("c0", 2.0e10)]), 0.0, "fixture_read")
        mon = events.GrazeMonitor(view, 0.0)
        for i in range(5):
            mon(float(i), (1.0, 1e9 * i, 1600.0, 1600.0, 0.0, 0.0))
        self.assertIsNone(mon.best)


# ── B1/B2 on C1 (68): solve_id binds the read and is deterministic; a successful Answer carries the counts ─────────
def _solve(stamp="s" * 64, read=None):
    view = rv.ReadView(read or FixtureRead([Curve("c0", 2.0e10, 1e6)]), 0.0, "fixture_read", stamp)
    return sv.solve(_body(), views={"core": Uniform(9000.0), "mantle": view})


def _sid(ans):
    return next(iter(ans.quantities)).provenance.solver.solve_id


class SolveIdAndNotes(unittest.TestCase):
    def test_solve_id_deterministic_and_binds_the_stamp(self):
        a1, _ = _solve()
        a2, _ = _solve()
        self.assertEqual(_sid(a1), _sid(a2))             # two fresh views, one answer id (no addresses, no counters)
        a3, _ = _solve(stamp="t" * 64)
        self.assertNotEqual(_sid(a1), _sid(a3))          # the read's stamp is bound

    def test_material_bytes_ignore_mutable_state(self):
        v = rv.ReadView(FixtureRead([Curve("c0", 2.0e10)]), 0.0, "fixture_read", "s" * 64)
        b0 = sv._material_bytes({"m": v})
        v.read_retried["extent"] = 5
        v.pins["c0"] = "f1"
        sv._plan(v)
        self.assertEqual(b0, sv._material_bytes({"m": v}))

    def test_successful_answer_carries_read_counts(self):
        ans, _ = _solve()
        notes = [n for n in ans.notes if n.kind == "read_counts"]
        self.assertEqual(len(notes), 1)
        self.assertIn("read_retried", notes[0].fields)
        self.assertIn("curve_end_steps", notes[0].fields)


# ── B3, B4 on C1: the selector end to end through _assemblage_view, with the pending guard first ────────────────
class FakeRegistry:
    def __init__(self, rec, status="built", development=False):
        self.rec, self.tables, self.development = rec, {"r_x": {"boundaries": {"status": status}}}, development

    def get(self, rid):
        return self.rec if rid == "r_x" else None


class SelectorEndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "reads").mkdir()
        (self.tmp / "reads" / "loader.py").write_text(
            "# 시험용 읽기 적재기\nimport json\n\ndef load_read(paths):\n    with open(paths[0]) as f:\n"
            "        return json.load(f)\n")
        (self.tmp / "reads" / "data.json").write_text('{"ok": 1}\n')
        self.files = ["reads/loader.py", "reads/data.json"]
        self.stamp = rv.stamp_of(self.files, self.tmp)

    def call(self, stamp=None, status="built", files=None, read=True):
        asm = {"read": {"files": files or self.files, "stamp": stamp or self.stamp}} if read else {}
        reg = FakeRegistry({"assemblage": asm}, status=status)
        with mock.patch.object(sv, "REPO_ROOT", self.tmp):
            return sv._assemblage_view(_body(), _body().layers[1], "r_x", 0.0, reg)

    def test_matching_stamp_gives_a_read_view(self):
        v, fail = self.call()
        self.assertIsNone(fail)
        self.assertIsInstance(v, rv.ReadView)
        self.assertEqual((v.material_id, v.stamp, v.read), ("r_x", self.stamp, {"ok": 1}))

    def test_stale_and_missing_refuse_with_the_record_id(self):
        v, fail = self.call(stamp="0" * 64)
        self.assertIsNotNone(fail, f"no refusal: {v!r}")
        self.assertEqual((v, fail[0], fail[1][0], fail[1][1]), (None, "read_unavailable", "r_x", "stale_stamp"))
        v, fail = self.call(files=["reads/loader.py", "reads/gone.json"])
        self.assertEqual((fail[0], fail[1][1]), ("read_unavailable", "missing_file"))

    def test_the_solve_registry_is_handed_to_the_read(self):   # 11-21: _assemblage_view passes its own registry
        seen = {}
        real = rv.load
        def spy(*a, **k):
            seen["registry"] = k.get("registry")
            return real(*a, **k)
        reg = FakeRegistry({"assemblage": {"read": {"files": self.files, "stamp": self.stamp}}}, status="built")
        with mock.patch.object(sv, "REPO_ROOT", self.tmp), mock.patch.object(rv, "load", spy):
            v, fail = sv._assemblage_view(_body(), _body().layers[1], "r_x", 0.0, reg)
        self.assertIsNone(fail)
        self.assertIs(seen["registry"], reg)

    def test_pending_boundaries_refuse_before_the_read(self):
        v, fail = self.call(status="pending")
        self.assertEqual((v, fail[0]), (None, "record_boundaries_pending"))

    def test_no_read_goes_to_todays_path(self):
        with mock.patch("solver.material_assemblage.view", return_value="TABLE_VIEW") as mv, \
                mock.patch("solver.from_v1.thaw", side_effect=lambda r: r):
            v, fail = self.call(read=False)
        self.assertEqual(v, "TABLE_VIEW")
        self.assertTrue(mv.called)

    def test_N4_identity_passes_mutant_fails(self):
        """N4 as registered: _assemblage_view rebuilt from source (identity) passes the stale/missing test; a version
        that falls back to the table on ReadUnavailable fails it."""
        patches = (mock.patch("solver.material_assemblage.view", return_value="TABLE_VIEW"),
                   mock.patch("solver.from_v1.thaw", side_effect=lambda r: r))
        with mock.patch.object(sv, "_assemblage_view", variant(sv._assemblage_view)), patches[0], patches[1]:
            self.test_stale_and_missing_refuse_with_the_record_id()
        mut = variant(sv._assemblage_view, '            return None, ("read_unavailable", (rid, e.reason, e.detail))\n',
                      "            rd_decl = None\n",
                      more=[("        return rv.ReadView(read, p_stop, rid, rd_decl[\"stamp\"]), None\n",
                             "        if rd_decl is not None:\n"
                             "            return rv.ReadView(read, p_stop, rid, rd_decl[\"stamp\"]), None\n")])
        with mock.patch.object(sv, "_assemblage_view", mut), patches[0], patches[1]:
            with self.assertRaises(AssertionError):
                self.test_stale_and_missing_refuse_with_the_record_id()

class LoaderImports(unittest.TestCase):
    """n1 on C1: a module the loader pulls in from inside the root must be a stamped file."""

    def test_solver_tests_module_is_not_exempt(self):
        """68 on e0fb28eb: a module under solver/tests/ is bound by neither the read stamp nor solve_id."""
        tmp = Path(tempfile.mkdtemp())
        (tmp / "reads").mkdir()
        (tmp / "solver" / "tests").mkdir(parents=True)
        (tmp / "solver" / "tests" / "planted_mod_y.py").write_text("# 시험용 심은 모듈\nVALUE = 2\n")
        (tmp / "reads" / "loader.py").write_text(
            "# 시험용 읽기 적재기\nimport sys\nsys.path.insert(0, __file__.rsplit('/', 2)[0] + '/solver/tests')\n"
            "import planted_mod_y\n\ndef load_read(paths):\n    return planted_mod_y.VALUE\n")
        files = ["reads/loader.py"]
        import sys
        try:
            with self.assertRaises(rv.ReadUnavailable) as cm:
                rv.load(files, rv.stamp_of(files, tmp), tmp)
            self.assertEqual(cm.exception.reason, "unstamped_module")
        finally:
            sys.modules.pop("planted_mod_y", None)

    def test_mutant_old_exemption_fails(self):
        with mock.patch.object(rv, "load", variant(rv.load)):
            self.test_solver_tests_module_is_not_exempt()
        old = variant(rv.load, '                and not (Path(fn).resolve().is_relative_to(base / "solver")\n'
                               '                         and not Path(fn).resolve().is_relative_to(base / "solver" / "tests")):',
                      '                and not Path(fn).resolve().is_relative_to(base / "solver"):')
        with mock.patch.object(rv, "load", old):
            with self.assertRaises(AssertionError):
                self.test_solver_tests_module_is_not_exempt()

    def test_unstamped_import_refuses(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "reads").mkdir()
        (tmp / "reads" / "helper_mod_x.py").write_text("# 시험용 도움 모듈\nVALUE = 1\n")
        (tmp / "reads" / "loader.py").write_text(
            "# 시험용 읽기 적재기\nimport sys\nsys.path.insert(0, __file__.rsplit('/', 1)[0])\nimport helper_mod_x\n\n"
            "def load_read(paths):\n    return helper_mod_x.VALUE\n")
        files = ["reads/loader.py"]
        with self.assertRaises(rv.ReadUnavailable) as cm:
            rv.load(files, rv.stamp_of(files, tmp), tmp)
        self.assertEqual(cm.exception.reason, "unstamped_module")
        import sys
        sys.modules.pop("helper_mod_x", None)
        files2 = ["reads/loader.py", "reads/helper_mod_x.py"]
        self.assertEqual(rv.load(files2, rv.stamp_of(files2, tmp), tmp), 1)
        sys.modules.pop("helper_mod_x", None)


# ── A10 at C4: the retry filter; a non-retryable kind stops at once, extent is retried, the line's mutant fails ──
FILTER_LINE = ('            if isinstance(out.record, dict) and out.record.get("retryable") is False:\n'
               '                return stop("refused", out)             # read-view §4.4 (C4): the read said invalid, not unbuilt\n')


class Filter(unittest.TestCase):
    def case_off_path_cut(self):
        """A «cut» only a trial stage reaches (p above 1.5 × the path's maximum): the run ends at once, refused."""
        g = OffPathExtent()
        r, v, _ = g.run_with(lambda p, t: "cut" if p > 1.5 * 2 * g.A / g.W else None)
        self.assertEqual(r.stop.kind, "refused", r.stop)
        self.assertEqual(r.stop.record.kind, "read_refusal")
        self.assertEqual(r.stop.record.record["kind"], "cut")
        self.assertIs(r.stop.record.record["retryable"], False)
        self.assertEqual(r.counters.refused_stage, 1)
        self.assertEqual(v.read_retried, {"cut": 1})

    def case_on_path_cut_unretried(self):
        """A4 (a): the planted on-path «cut» surfaces with no retry counted."""
        out, ref = Refusals().run_cut()
        self.assertEqual(dict(ref.evidence)["read_retried"], {"cut": 1})

    def test_off_path_cut_ends_at_once(self):
        self.case_off_path_cut()

    def test_on_path_cut_unretried(self):
        self.case_on_path_cut_unretried()

    def test_off_path_extent_retried(self):
        OffPathExtent("test_retried_and_same_answer").test_retried_and_same_answer()

    def test_retryable_set(self):
        self.assertEqual(rv.RETRYABLE, frozenset({"extent", "past_deepest", "pin_unserved"}))   # read-view note 3 §2
        view = rv.ReadView(FixtureRead([]), 0.0, "fixture_read")
        for kind in sorted(rv.KINDS):
            self.assertIs(view._refusal(1.0, 1.0, ValueError("x"), kind).record["retryable"], kind in rv.RETRYABLE)

    def case_other_stops_retried(self):
        """68 on C4: an off-path Stop that is not a read refusal (a dict record without «retryable», or record None)
        is retried as before, and the run ends normally."""
        g = OffPathExtent()
        pmax = 2 * g.A / g.W
        for rec in ({"why": "a material refusal"}, None):
            opt = st.Options(rtol=1e-8, floors=(1.0, 1e-9, 1.0, 1.0, 1.0, 1.0), h0=3.0, h_min=1e-12, h_max=50.0,
                             max_steps=100000, event_tol=1e-12, event_rewalks=32, event_min_progress=1e-9)

            def f(x, y, rec=rec):
                if y[1] > 1.5 * pmax:
                    return st.Stop("material", rec)
                return (0.0, g.A * math.sin(g.W * x), 0.0, 0.0, 0.0, 0.0)
            r = st.run(f, 0.0, (1.0, 0.0, 1.0, 1.0, 0.0, 0.0), 4.0, opt)
            self.assertEqual(r.stop.kind, "end", (rec, r.stop))
            self.assertGreaterEqual(r.counters.refused_stage, 1, rec)

    def test_other_stops_retried(self):
        self.case_other_stops_retried()

    def test_mutant_is_not_true(self):
        old = 'out.record.get("retryable") is False'
        with mock.patch.object(st, "run", variant(st.run)):
            self.case_other_stops_retried()
        for new in ('out.record.get("retryable") is not True', 'True'):
            with mock.patch.object(st, "run", variant(st.run, old, new)):
                with self.assertRaises(AssertionError):
                    self.case_other_stops_retried()

    def test_mutant_without_the_line(self):
        for case in (self.case_off_path_cut, self.case_on_path_cut_unretried):
            with mock.patch.object(st, "run", variant(st.run)):
                case()
            with mock.patch.object(st, "run", variant(st.run, FILTER_LINE, "")):
                with self.assertRaises(AssertionError):
                    case()


# ── n3 on C1: Collect through real passes ──────────────────────────────────────────────────────────────────────
class CollectThroughPasses(unittest.TestCase):
    def once_then(self, p1, then=None):
        """An extent refusal the first time a stage passes p1 (a trial stage, retried shorter), then `then`."""
        seen = {"n": 0}

        def refuse(p, t):
            if p > p1 and seen["n"] == 0:
                seen["n"] += 1
                return "extent"
            return then(p, t) if then is not None else None
        return refuse

    def test_two_runs_one_pass_one_total(self):
        core = rv.ReadView(FixtureRead([], rho=9000.0, refuse=self.once_then(1.0e11)), 0.0, "core_read")
        mantle = rv.ReadView(FixtureRead([], refuse=self.once_then(1.0e10)), 0.0, "mantle_read")
        out = sv.inward(_body(), {"core": core, "mantle": mantle}, R0, OPT)
        self.assertIsInstance(out, sv.PassOut, out)
        self.assertEqual(out.read_counts["read_retried"], {"extent": 2})
        out2 = sv.inward(_body(), {"core": core, "mantle": mantle}, R0, OPT)
        self.assertEqual(out2.read_counts["read_retried"], {})     # reset per pass

    def test_retries_then_refuses_keeps_the_counts(self):
        mantle = rv.ReadView(FixtureRead([], refuse=self.once_then(
            1.0e10, then=lambda p, t: "past_deepest" if p > 4.0e10 else None)), 0.0, "mantle_read")
        out = sv.inward(_body(), {"core": Uniform(9000.0), "mantle": mantle}, R0, OPT)
        self.assertIsInstance(out, st.Stop)
        ref = sv._to_refusal(out, "fixture", R0, "R", "scan")
        rr = dict(ref.evidence)["read_retried"]
        self.assertEqual(rr.get("extent"), 1)
        self.assertGreaterEqual(rr.get("past_deepest", 0), 1)


if __name__ == "__main__":
    unittest.main()
