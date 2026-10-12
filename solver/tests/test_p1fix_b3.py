# 리뷰 수정 B3 시험 — 어댑터·멤버·오라클의 빈 시험 채우기: T_pot 상태의 풀이 온도·옛 사슬의 T_pot 덮어쓰기·table_read 의 거짓 갈래·old_values 단위·칸 상한 값·material_bytes 의 blob 절반
"""Post-phase-1 review fix batch B3 (rewrite/p1review/fix-plan.md (B)): tests only, for G3-T-01 … -05 and -08. Each
class names the finding and the mutation it kills.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_b3
"""
import dataclasses
import subprocess
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import context, from_v1, legacy_materials as lm, legacy_view as lv, member as mb, run_oracle as ro
from solver import solve as sv

OPT = context.Options(sensitivity_dt=0.0)
T_STATE = 2093.0


def _points(rec):
    return {q["key"]: q["point"] for q in rec["quantities"]}


class TPotStateIsSolvedAtItsTPot(unittest.TestCase):
    """G3-T-01: a T_pot record holds the solve at that T_pot (deleting run_oracle's surface replace fails it)."""

    def test_record_equals_the_solve_at_t(self):
        rec = ro.one("engine/bodies/earth.yaml", T_STATE, OPT, chain=False)
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        ans, _x = sv.solve(dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=T_STATE)), OPT)
        self.assertEqual(_points(rec), {q.key: q.point for q in ans.quantities})
        dec = ro.one("engine/bodies/earth.yaml", "declared", OPT, chain=False)
        self.assertNotEqual(_points(rec)["core_temperature"], _points(dec)["core_temperature"])


class ChainTPotOverride(unittest.TestCase):
    """G3-T-02: run_chain(..., t_pot=T) runs the old chain with potential_temperature T (dropping the override, or
    writing it under another key, fails it)."""

    @classmethod
    def setUpClass(cls):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        cls.ans_t, _x = sv.solve(dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=T_STATE)), OPT)
        cls.ans_d, _x = sv.solve(body, OPT)
        cls.chain_t = lv.run_chain("engine/bodies/earth.yaml", cls.ans_t, t_pot=T_STATE)
        cls.chain_d = lv.run_chain("engine/bodies/earth.yaml", cls.ans_d)

    def test_the_old_body_reads_t(self):
        cur = self.chain_t.body.inputs["potential_temperature"]
        dec = self.chain_d.body.inputs["potential_temperature"]
        if isinstance(dec, dict):
            self.assertEqual(cur, {**dec, "value": T_STATE})               # the dict branch keeps its other fields
        else:
            self.assertEqual(cur, T_STATE)
        self.assertNotEqual(dec if not isinstance(dec, dict) else dec["value"], T_STATE)

    def test_a_t_reading_node_moves(self):
        """Some old node that reads the potential temperature answers differently at T than at the declared state."""
        moved = [n for n, r in self.chain_t.body.results.items()
                 if n != "interior_layers" and r.applicable and n in self.chain_d.body.results
                 and "potential_temperature" in (r.inputs or {})
                 and dict(r.values) != dict(self.chain_d.body.results[n].values)]
        self.assertTrue(moved)


class TableReadFalseBranch(unittest.TestCase):
    """G3-T-03: table_read is true only for a returned grid whose blob is the oracle tree's committed one (the blob
    test forced True, the None check dropped, or any → all each fail a case)."""

    def _read(self, reads):
        rec = {}
        with mock.patch.object(ro, "_committed_blob", lambda path: "a" * 40):
            ro._legacy(rec, NS(body=NS(results={}), notes=(), table_reads=tuple(reads)))
        return rec["table_read"]

    def test_cases(self):
        good, other, p = "a" * 40, "b" * 40, "engine/structure_grid/x.json"
        for reads, want in (([(p, good, True)], True), ([(p, other, True)], False), ([(p, None, True)], False),
                            ([(p, good, False)], False), ([(p, other, True), (p, good, True)], True), ([], False)):
            with self.subTest(reads=reads):
                self.assertEqual(self._read(reads), want)


def _answer(**pts):
    return NS(quantities=[NS(key=k, point=v) for k, v in pts.items()])


class OldValuesUnits(unittest.TestCase):
    """G3-T-04: every converted value and unit of the injected interior_layers Result, from distinct planted points."""

    def test_values_and_units(self):
        a = _answer(radius=6.5e6, nmoi=0.33, core_radius=3.25e6, cmb_pressure=1.36e11, core_pressure=3.6e11,
                    cmb_temperature=2500.0, core_temperature=3100.0, core_mass_fraction=0.31)
        vals, units = lv.old_values(a, declared_imf=0.02)
        R = lv.EARTH_RADIUS_M
        self.assertEqual(R, 6.371e6)
        self.assertEqual(vals, {"nmoi": 0.33, "core_temperature": 3100.0, "cmb_temperature": 2500.0,
                                "cmb_temperature_core": 2500.0, "cmb_temperature_mantle": 2500.0,
                                "cmb_pressure": 136.0, "core_radius": 3.25e6 / R, "core_radius_fraction": 0.5,
                                "radius": 6.5e6 / R, "core_pressure": 360.0, "converged": True,
                                "core_mass_fraction": 0.31, "ice_mass_fraction": 0.02})
        self.assertEqual(units, {"nmoi": "dimensionless", "core_temperature": "K", "cmb_temperature": "K",
                                 "cmb_temperature_core": "K", "cmb_temperature_mantle": "K", "cmb_pressure": "GPa",
                                 "core_radius": "R_earth", "core_radius_fraction": "dimensionless", "radius": "R_earth",
                                 "core_pressure": "GPa", "converged": "", "core_mass_fraction": "dimensionless",
                                 "ice_mass_fraction": "dimensionless"})

    def test_absent_quantities(self):
        a = _answer(radius=6.5e6, nmoi=0.33, core_pressure=3.6e11)
        vals, units = lv.old_values(a)
        self.assertEqual((vals["core_radius"], vals["cmb_pressure"], vals["cmb_temperature"], vals["ice_mass_fraction"]),
                         (0.0, 0.0, 0.0, 0.0))
        self.assertNotIn("core_mass_fraction", vals)
        self.assertNotIn("core_mass_fraction", units)


class CellCapValue(unittest.TestCase):
    """G3-T-05: Mars's mantle table cell factor pinned: exp(narrowest ln P cell) − 1 of table 0663e6a0 (256 nodes,
    narrowest 0.03651449780864624, widest 0.04879016416943216). min → max, a dropped − 1 or a dropped p each fail."""

    def test_value(self):
        body, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        body, _m = mb.member_of(body)
        ph = sv._views(body)["mantle"].mat.phase_at(5.0e9)
        self.assertEqual(ph.table_key, "0663e6a031cae4dc")
        self.assertAlmostEqual(lm.table_cell_factor(ph), 0.037189340881342625, delta=1e-15)
        self.assertAlmostEqual(lm.table_step_cap(ph, 5.0e9), 5.0e9 * 0.037189340881342625, delta=1e-3)
        self.assertIsNone(lm.table_cell_factor(NS()))                      # no table: no cap


class MaterialBytesBlobHalf(unittest.TestCase):
    """G3-T-08: a committed blob change of a counted engine file moves material_bytes and so solve_id, with a clean
    tree (the dirty half is not involved); an excluded path's blob does not. Deleting the blob loop, or reading the
    mode instead of the blob, fails it."""

    def _bytes(self, path=None):
        real = subprocess.run

        def run(args, *a, **k):
            out = real(args, *a, **k)
            if "ls-files" in args and path is not None:
                lines = []
                for line in out.stdout.splitlines():
                    meta, p = line.split("\t", 1)
                    if p == path:
                        mode, b0, stage = meta.split()
                        # the last hex digit flipped: the line keeps its place in material_bytes' sorted(ls), which
                        # sorts by mode and blob, so only the blob's own text can move the digest
                        line = f"{mode} {b0[:-1] + ('0' if b0[-1] != '0' else '1')} {stage}\t{p}"
                    lines.append(line)
                out = subprocess.CompletedProcess(out.args, out.returncode, "\n".join(lines) + "\n", out.stderr)
            if "diff" in args:
                out = subprocess.CompletedProcess(out.args, out.returncode, "", out.stderr)   # a clean tree
            return out
        with mock.patch("subprocess.run", run):
            return lm.material_bytes()

    def test_blob_change_moves_the_id(self):
        base = self._bytes()
        counted = self._bytes("engine/eos.py")
        excluded = self._bytes("engine/bodies/earth.yaml")
        self.assertNotEqual(base, counted)
        self.assertEqual(base, excluded)
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        c = sv._canonical(body)
        self.assertNotEqual(context.solve_id_of(c, base, OPT), context.solve_id_of(c, counted, OPT))


class StepCapBranches(unittest.TestCase):
    """G3-T-05, events.step_cap's own branches (68 on cc1d20f0): a PhaseGap or SpinodalGap at the step's P gives no
    cap, any other exception propagates, dP/dm = 0 gives no cap, and a material without a table phase has no cap."""

    @classmethod
    def setUpClass(cls):
        from solver import events as ev
        body, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        body, _m = mb.member_of(body)
        cls.ev = ev
        cls.mat = sv._views(body)["mantle"].mat
        cls.cap = staticmethod(ev.step_cap(cls.mat))

    def _raising(self, exc):
        return mock.patch.object(type(self.mat), "phase_at", side_effect=exc)

    def test_gaps_give_no_cap(self):
        k1 = (0.0, 1.0, 1.0e-8)
        y = (3.0e6, 5.0e9, 1900.0, 1900.0, 0.0, 0.0)
        self.assertIsNotNone(self.cap(0.0, y, k1))                          # control: a cap at that state
        for gap in (lm.eos.PhaseGap("silicate", 5.0e9, "planted"), type("SpinodalGap", (Exception,), {})("planted")):
            with self.subTest(gap=type(gap).__name__), self._raising(gap):
                self.assertIsNone(self.cap(0.0, y, k1))

    def test_other_exceptions_propagate(self):
        with self._raising(KeyError("planted")), self.assertRaises(KeyError):
            self.cap(0.0, (3.0e6, 5.0e9, 1900.0, 1900.0, 0.0, 0.0), (0.0, 1.0, 1.0e-8))

    def test_zero_pressure_slope_gives_no_cap(self):
        self.assertIsNone(self.cap(0.0, (3.0e6, 5.0e9, 1900.0, 1900.0, 0.0, 0.0), (0.0, 0.0, 1.0e-8)))

    def test_no_table_phase_no_cap(self):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        self.assertIsNone(self.ev.step_cap(sv._views(body)["mantle"].mat))


if __name__ == "__main__":
    unittest.main()
