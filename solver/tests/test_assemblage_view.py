# 광물 집합 뷰 시험 — C¹ 표 읽기(레거시 smooth_table 과 같은 값), 창·열 꼭대기·136 GPa 컷·200 K·1 bar 바닥, dT/dP 장, phase 1 녹음 창, 노트, 레거시 속성 (규산염 기록 등록 §3, 사후 노트 3)
"""Tests of AssemblageView (rewrite/phase2-silicate-record-registration.frozen.md §3 with post-freeze note 3) on a
synthetic compact table: a smooth analytic field so interpolation errors are visible and every planted change is the
only one. The melt window is checked against legacy `interior._adiabatic_dtdp` and `eos.Material.density` (r2 Q-E1:
each regime to 1e-12, with a stub solid equal to legacy's own).

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_assemblage_view
"""
import copy
import math
import unittest

from solver import legacy_materials as lm
from solver import material_assemblage as ma
from solver import material_view as mv
from solver import stepper as st

PS = [1e5 * 1.5 ** i for i in range(30)]                       # 0.1 MPa … ~13 GPa
TS = [200.0 + 50.0 * k for k in range(93)]                     # 200 … 4800 K


def rho_of(p, t):
    """Curved in T, so slope rules (end slope, extrapolation) give values that differ from a linear read."""
    return 3300.0 * (1.0 + p / 1.3e11) * (1.0 - 3e-5 * (t - 300.0) - 2e-9 * (t - 300.0) ** 2)


def table(tops=None, refused=()):
    """Every column to 4800 K unless `tops` gives a column (index) its own top; frozen below 400 K."""
    tops = tops or {}
    cells, cols = [], []
    for i, p in enumerate(PS):
        top = tops.get(i, TS[-1])
        for t in TS:
            if t > top:
                continue
            fr = t < 400.0
            c = {"p": p, "t": t, "kind": "frozen" if fr else ("above_solidus" if t > 1600.0 else "equilibrium"),
                 "assemblage": "ol+opx", "rho": rho_of(p, t), "c_p": 1200.0 + 0.1 * t, "dtdp_s": 1e-8 * t / 1000.0,
                 "freeze_t": 400.0 if fr else None, "freeze_class": "convergence edge" if fr else None,
                 "dtdp_eq_band": None if fr else 2.5e-4 * (1.0 + t / 1e4)}
            c["dtdp_eq"] = None if (i, t) in refused else c["dtdp_s"] * (1.0 + 0.1 * math.sin(math.log(p)))
            c["c_p_eq"] = None if fr or (i, t) in refused else c["c_p"] * 1.03
            cells.append(c)
        cols.append({"p": p, "t_sol": 1500.0, "t_window_top": top,
                     "window": {"cause": "grid_end"} if top == TS[-1] else {"cause": "eos_edge", "phase": "opx"}})
    return {"cells": cells, "columns": cols, "p_dataset": PS[-3]}


def record(p_dataset=PS[-3]):
    return {"id": "silicate_slb_test", "kind": "assemblage",
            "assemblage": {"p_dataset": p_dataset, "melt_variant": "peridotitic", "sha256": "a" * 64,
                           "dtdp": {"band_origin": "test band origin"},
                           "floor_band": {"origin": "the floor node's own compressibility"}},
            "phases": [{"id": "slb_assemblage"}]}


def view(tb=None, rec=None, **kw):
    tb = tb or table()
    rec = rec or record(tb["p_dataset"])
    return ma.view(rec, tb, 1600.0, **kw)


def solid(v, p, t):
    got = v._solid(p, t)
    assert not isinstance(got, st.Stop), got
    return got


class Interpolation(unittest.TestCase):
    def test_nodes_exact_and_c0_across_cells(self):
        v = view()
        r, g, cp, _ = solid(v, PS[10], TS[20])
        c = v._cells[(PS[10], TS[20])]
        self.assertEqual((r, g, cp), (c["rho"], c["dtdp_eq"], c["c_p_eq"]))      # non-frozen: c_p_eq (r2 B1)
        fr = v._cells[(PS[10], TS[2])]                                            # 300 K, frozen: the table's c_p
        self.assertEqual(solid(v, PS[10], TS[2])[2], fr["c_p"])
        p = PS[10]
        for t in (TS[20] - 1e-9, TS[20] + 1e-9):
            self.assertAlmostEqual(solid(v, p, t)[0], c["rho"], delta=1e-6)

    def test_matches_legacy_smooth_table(self):
        """The port is the algorithm of engine/smooth_table.py: same value on a ragged table."""
        import smooth_table
        tb = table(tops={7: 2350.0, 8: 1200.0})
        v = view(tb)
        for p, t in ((PS[7] * 1.2, 1130.0), (PS[3] * 1.1, 777.0), (PS[8] * 0.9, 1149.0)):
            ia = max(i for i in range(len(PS) - 1) if PS[i] <= p)
            ib = max(k for k in range(len(TS) - 1) if TS[k] <= t)
            val = lambda a, b: (v._cell(a, b) or {}).get("rho")
            want = smooth_table.cubic2(math.log(p), t, v.lnps, v.ts, val, ia, ib)
            self.assertEqual(solid(v, p, t)[0], want)

    def legacy_at(self, v, p, t, field="rho"):
        import smooth_table
        ia = max(i for i in range(len(PS) - 1) if PS[i] <= p)
        ib = max(k for k in range(len(TS) - 1) if TS[k] <= t)
        val = lambda a, b: (v._cell(a, b) or {}).get(field)
        return smooth_table.cubic2(math.log(p), t, v.lnps, v.ts, val, ia, ib)

    def test_ragged_edge_extrapolation(self):
        """68 V11: a read in a column's top cell, whose outer stencil node above the next column's top is
        extrapolated along that row's end slope, equals smooth_table's."""
        import smooth_table
        v = view(table(tops={7: 2350.0, 8: 1200.0}))
        n0 = smooth_table.EXTRAPOLATED_READS[0]
        want = self.legacy_at(v, PS[7] * 1.2, 1170.0)
        self.assertGreater(smooth_table.EXTRAPOLATED_READS[0], n0)           # the path is really taken
        self.assertEqual(solid(v, PS[7] * 1.2, 1170.0)[0], want)

    def test_zero_weight_grid_line(self):
        """68 V3: a read exactly on a P node whose neighbour row lacks the corner answers from its own row (the
        zero-weight rule), as smooth_table."""
        v = view(table(tops={6: 1200.0}))                    # the read's cell is [PS[6], PS[7]] with weight 0 on PS[6]
        got = solid(v, PS[7], 1220.0)[0]
        self.assertEqual(got, self.legacy_at(v, PS[7], 1220.0))
        self.assertIsInstance(v._solid(PS[7] * 0.99, 1220.0), st.Stop)        # off the line, the corner is needed

    def test_non_monotone_stencil(self):
        """68 V16: a non-monotone stencil (the end-slope ×3 clamp and zero inner slopes) equals smooth_table's."""
        tb = table()
        for c in tb["cells"]:
            if c["p"] in (PS[10], PS[11]):
                c["rho"] *= 1.0 + 0.03 * math.sin(c["t"] / 37.0)
            if c["p"] == PS[12] and c["t"] in (200.0, 250.0, 300.0):    # end node: d0 small, d1 opposite and large,
                c["rho"] = 3000.0 + {200.0: 0.0, 250.0: 1.0, 300.0: -10.0}[c["t"]]   # so the ×3 clamp acts
        v = view(tb)
        import smooth_table
        s_raw = ((2 * 50 + 50) * (1 / 50) - 50 * (-11 / 50)) / 100
        self.assertNotEqual(smooth_table._end_slope(50.0, 50.0, 1 / 50, -11 / 50), s_raw)   # the clamp is taken
        for p, t in ((PS[10] * 1.1, 1333.0), (PS[10] * 1.3, 222.0), (PS[10] * 1.01, 4790.0), (PS[12], 220.0)):
            with self.subTest(p=p, t=t):
                self.assertEqual(solid(v, p, t)[0], self.legacy_at(v, p, t))

    def test_dtdp_is_the_field_not_rho(self):
        """§3.2 (68 (i)): dT/dP is the dtdp_eq interpolant; a planted ρ inversion leaves it unchanged."""
        tb = table()
        a = solid(view(tb), PS[12] * 1.1, 1333.0)[1]
        tb2 = copy.deepcopy(tb)
        c = next(c for c in tb2["cells"] if c["p"] == PS[13] and c["t"] == 1350.0)
        c["rho"] = 0.5 * c["rho"]
        self.assertEqual(solid(view(tb2), PS[12] * 1.1, 1333.0)[1], a)


class Window(unittest.TestCase):
    def test_neighbour_tops(self):
        """§3.1 (r2 HOLD on d08d6c5f): tops 2350 K and 4800 K side by side; a read between them at 3000 K refuses,
        naming the 2350 K column's cause; below 2350 K it answers."""
        v = view(table(tops={10: 2350.0}))
        got = v._solid(PS[10] * 1.2, 3000.0)
        self.assertIsInstance(got, st.Stop)
        self.assertEqual(got.record.refusal, "input.material_above_solid_window")
        self.assertIn("eos_edge", got.record.why)
        self.assertIn(f"{PS[10]:g}", got.record.why)
        self.assertNotIsInstance(v._solid(PS[10] * 1.2, 2300.0), st.Stop)

    def test_eos_edge_one_node_above(self):
        """68: a column ended by the EOS edge refuses one node above its last cell, with cause eos_edge."""
        v = view(table(tops={10: 2350.0}))
        got = v._solid(PS[10], 2400.0)
        self.assertEqual(got.record.refusal, "input.material_above_solid_window")
        self.assertIn("eos_edge", got.record.why)

    def test_p_dataset_cut(self):
        """§3.1 (68): a read just below p_dataset is bit-identical when every node above it is perturbed; above it,
        a direct read refuses naming the dataset top."""
        tb = table()
        p = tb["p_dataset"] * 0.99
        a = solid(view(tb), p, 1500.0)
        tb2 = copy.deepcopy(tb)
        for c in tb2["cells"]:
            if c["p"] > tb["p_dataset"]:
                c["rho"] *= 1.1
                c["dtdp_eq"] *= 1.1
        self.assertEqual(solid(view(tb2), p, 1500.0)[:3], a[:3])
        got = view(tb)._solid(tb["p_dataset"] * 1.01, 1500.0)
        self.assertEqual(got.record.refusal, "input.material_out_of_data")
        self.assertIn("dataset top", got.record.why)

    def test_below_200_k(self):
        got = view()._solid(PS[5], 199.0)
        self.assertEqual(got.record.refusal, "input.material_out_of_data")

    def test_below_one_bar_floor_band(self):
        """§3.1 (r2 N2): below 1 bar the value is the 1 bar node's at the same T, with the floor band note."""
        v = view()
        got = v.state(5e4, 300.0)
        self.assertNotIsInstance(got, st.Stop)
        self.assertEqual(got[0], solid(v, PS[0], 300.0)[0])
        bands = [n for n in got[2] if isinstance(n, mv.BandNote) and n.edge == "p_min floor"]
        self.assertEqual(len(bands), 1)
        k_t = rho_of(PS[0], 300.0) * (PS[1] - PS[0]) / (rho_of(PS[1], 300.0) - rho_of(PS[0], 300.0))   # 68 V23
        self.assertAlmostEqual(bands[0].error, (PS[0] - 5e4) / k_t, delta=1e-12 * bands[0].error)

    def test_refusal_names_the_solver_pressure(self):
        """ea's F4 gate reads the refusal's p: it is the solver's P (here below 1 bar), not the clamped 1 bar read."""
        got = view().state(5e4, 199.0)
        self.assertIsInstance(got, st.Stop)
        self.assertEqual(got.record.p, 5e4)
        got = view(p_stop=2e5).state(1e5, 199.0)                  # a read raised to p_stop names both pressures
        self.assertEqual(got.record.p, 1e5)
        self.assertIn("read at 200000 Pa", got.record.why)

    def test_refused_isentrope_node(self):
        """Note 3 §2 condition 4: a read whose cell corner has no dT/dP refuses by name."""
        v = view(table(refused={(10, 1500.0)}))
        got = v._solid(PS[10] * 1.1, 1520.0)
        self.assertEqual(got.record.refusal, "input.material_out_of_data")
        self.assertIn("no equilibrium isentrope", got.record.why)


class MeltWindow(unittest.TestCase):
    """r2 Q-E1: phase 1's full C120 rule with the table's solid terms."""

    def test_silicate_melt_mix_against_legacy(self):
        """Each regime (φ = 0, the window, its edge, φ ≥ 1) with a stub solid equal to legacy's own: ρ and dT/dP equal
        legacy `eos.Material.density` and `interior._adiabatic_dtdp` to 1e-12; a stub without the latent factor fails
        the window case."""
        eos, interior = lm.eos, lm.interior
        mat = eos.MATERIALS["silicate"]
        for p, t in ((5e9, 1500.0), (5e9, 2100.0), (5e9, 1905.0), (30e9, 2900.0), (5e9, 3500.0)):
            rho_s = mat.solid_density(p, t, 1600.0)
            real = eos.Material.melt_phi
            try:
                eos.Material.melt_phi = lambda self, pp, tt: 0.0
                g_s = interior._adiabatic_dtdp(mat, p, rho_s, t, 1600.0)
            finally:
                eos.Material.melt_phi = real
            cp_s = mat.c_p(p, t, 1600.0) - mat._latent_cp(mat.phase_at(p), p, t)
            rho, g, phi = lm.silicate_melt_mix(p, t, "peridotitic", rho_s, g_s, cp_s)
            rho_leg = mat.density(p, t, 1600.0)
            g_leg = interior._adiabatic_dtdp(mat, p, rho_leg, t, 1600.0)
            with self.subTest(p=p, t=t, phi=phi):
                self.assertLessEqual(abs(rho - rho_leg), 1e-12 * rho_leg)
                self.assertLessEqual(abs(g - g_leg), 1e-12 * abs(g_leg))
                if 0.0 < phi < 1.0 and mat._latent_cp(mat.phase_at(p), p, t) > 0.0:
                    lat = eos.Material.__dict__["_latent_cp"]          # the staticmethod object itself
                    try:
                        eos.Material._latent_cp = staticmethod(lambda ph, pp, tt: 0.0)
                        _, g0, _ = lm.silicate_melt_mix(p, t, "peridotitic", rho_s, g_s, cp_s)
                    finally:
                        eos.Material._latent_cp = lat
                    self.assertGreater(abs(g0 - g_leg), 1e-6 * abs(g_leg))

    def test_view_regimes(self):
        """φ = 0: the solid read exactly; φ ≥ 1: the liquid with no solid read (a column with no cell there still
        answers); the window: lm.silicate_melt_mix of the solid read."""
        v = view()
        p = PS[25]                                           # ~2.5 GPa
        t0 = 1200.0
        self.assertEqual(lm.silicate_melt_phi(p, t0, "peridotitic"), 0.0)
        r, g, cp, _ = solid(v, p, t0)
        self.assertEqual(v.state(p, t0)[:2], (r, g))
        hot = 4000.0
        self.assertGreaterEqual(lm.silicate_melt_phi(p, hot, "peridotitic"), 1.0)
        cut = view(table(tops={i: 2000.0 for i in range(len(PS))}))
        got = cut.state(p, hot)
        self.assertNotIsInstance(got, st.Stop)
        self.assertEqual(got[:2], lm.silicate_melt_mix(p, hot, "peridotitic", None, None, None)[:2])
        tw = next(t for t in range(1500, 3000, 5) if 0.2 < lm.silicate_melt_phi(p, t, "peridotitic") < 0.8)
        r, g, cp, _ = solid(v, p, float(tw))
        self.assertEqual(v.state(p, float(tw))[:2],
                         lm.silicate_melt_mix(p, float(tw), "peridotitic", r, g, cp)[:2])

    def test_rtpress_refusal(self):
        """68 V14: RTpress's own PhaseGap reaches the solve as a named out_of_data refusal."""
        import rtpress
        real = rtpress.liquid
        try:
            rtpress.liquid = lambda p, t: (_ for _ in ()).throw(lm.eos.PhaseGap("silicate", p, "planted"))
            got = view().state(PS[25], 4000.0)
        finally:
            rtpress.liquid = real
        self.assertIsInstance(got, st.Stop)
        self.assertEqual(got.record.refusal, "input.material_out_of_data")
        self.assertIn("RTpress", got.record.why)

    def test_window_reads_the_equilibrium_heat_capacity(self):
        """r2 B1 on note 3: in the window the solid's c_P is c_p_eq on non-frozen cells (dtdp_eq's basis), so changing
        c_p_eq changes the answer and changing the isomorphic c_p does not; φ = 0 reads neither."""
        p = PS[25]
        tw = float(next(t for t in range(1500, 3000, 5) if 0.2 < lm.silicate_melt_phi(p, t, "peridotitic") < 0.8))
        base = view().state(p, tw)[:2]
        tb = table()
        for c in tb["cells"]:
            if c["c_p_eq"] is not None:
                c["c_p_eq"] *= 1.5
        self.assertNotEqual(view(tb).state(p, tw)[1], base[1])
        tb = table()
        for c in tb["cells"]:
            if c["kind"] != "frozen":
                c["c_p"] *= 1.5
        self.assertEqual(view(tb).state(p, tw)[:2], base)

    def test_window_above_solid_top_refuses(self):
        """Note 3 §1: only 0 < φ < 1 above the window top refuses."""
        p = PS[25]
        tw = next(t for t in range(1500, 3000, 5) if 0.2 < lm.silicate_melt_phi(p, t, "peridotitic") < 0.8)
        cut = view(table(tops={i: 1400.0 for i in range(len(PS))}))
        got = cut.state(p, float(tw))
        self.assertIsInstance(got, st.Stop)
        self.assertEqual(got.record.refusal, "input.material_above_solid_window")


class Notes(unittest.TestCase):
    def test_frozen_above_solidus_and_band_notes(self):
        v = view()
        got = v.state(PS[5], 300.0)
        self.assertTrue(any(isinstance(n, mv.DeclaredNote) and "frozen" in n.text for n in got[2]))
        got = v.state(PS[29] * 0.95 if PS[29] * 0.95 < v.p_dataset else PS[20], 1000.0)
        self.assertTrue(any(isinstance(n, mv.BandNote) and n.dtdp_error is not None for n in got[2]))
        p = PS[27]
        t = next(float(t) for t in range(1650, 4000, 50) if lm.silicate_melt_phi(p, t, "peridotitic") < 1.0)
        got = v.state(p, t)
        self.assertTrue(any(isinstance(n, mv.DeclaredNote) and "above the solidus cap" in n.text for n in got[2]))


class LegacyAttributes(unittest.TestCase):
    def test_attributes(self):
        """§3.1's class sweep: onset names and curves as legacy silicate's; name is the record id; no parts or
        table_key; .record carries the compact sha (68 S1); a RecordView (68 S2)."""
        v = view()
        self.assertIsInstance(v, mv.RecordView)
        self.assertEqual(v.onset_curve_names, ["고상선"])
        self.assertEqual(v.onset_curves(5e9, 2000.0), lm.eos.MATERIALS["silicate"].onset_curves(5e9, 2000.0))
        self.assertEqual(v.name, "silicate_slb_test")
        self.assertFalse(hasattr(v, "parts") or hasattr(v, "table_key"))
        self.assertEqual(v.record["assemblage"]["sha256"], "a" * 64)
        self.assertEqual((v.seams(), v.transitions(), v.source_seams()), ((), (), ()))


class SolverHooks(unittest.TestCase):
    def test_record_events_carry_the_solidus(self):
        """§3.1's rows «events._melt_curve_names, curve_seams, onset_events»: the assemblage view's events hold phase 1's
        solidus onset event and its curve seams, as legacy silicate's layer events do."""
        from solver import events
        names = [e.name for e in events.layer_events(view())]
        legacy = [e.name for e in events.layer_events(lm.LegacyView("silicate", lm.eos.MATERIALS["silicate"], 1600.0))]
        self.assertIn("onset:고상선", names)
        self.assertEqual(sorted(n for n in names if n.startswith(("onset", "seam"))),
                         sorted(n for n in legacy if n.startswith("onset") or
                                n in {e.name for e in events.seam_events_of_curves(view())}))
        self.assertTrue({e.name for e in events.seam_events_of_curves(view())} <= set(legacy))

    def test_notes_reach_the_answer(self):
        """68 S2: material_notes.collect reads the view: the frozen cells' declared note and the record's disclosures
        reach the notes of an answer that read them."""
        import types
        from solver import material_notes
        rec = record()
        rec["assemblage"]["disclosures"] = ["Fe3+-free model (test)"]
        v = ma.view(rec, table(), 1600.0)
        body = types.SimpleNamespace(layers=[types.SimpleNamespace(id="mantle")])
        acc = types.SimpleNamespace(profiles={"mantle": [(0.0, (0.0, PS[5], 300.0, 300.0), 0),
                                                         (0.0, (0.0, PS[12], 1000.0, 1000.0), 0)]})
        notes = material_notes.collect(body, {"mantle": v}, acc)
        kinds = {(n.kind, n.fields.get("of")) for n in notes}
        self.assertIn(("material_declared_note", None), kinds)
        self.assertIn(("material_disclosure", "record"), kinds)
        self.assertIn(("material_band", None), kinds)


class BandLocation(unittest.TestCase):
    def test_dtdp_band_location_follows_its_maximum(self):
        """68 on 07772fca: the «dT/dP model consistency» note's p_at_max and t_at_max are where dtdp_error is largest,
        also when the larger band is read second."""
        import types
        from solver import material_notes
        tb = table()
        for c in tb["cells"]:
            if c["dtdp_eq_band"] is not None and c["p"] >= PS[20]:
                c["dtdp_eq_band"] = 5e-2                      # larger bands at higher P, read second
        v = ma.view(record(), tb, 1600.0)
        body = types.SimpleNamespace(layers=[types.SimpleNamespace(id="mantle")])
        acc = types.SimpleNamespace(profiles={"mantle": [(0.0, (0.0, PS[10] * 1.1, 1000.0, 1000.0), 0),
                                                         (0.0, (0.0, PS[22] * 1.1, 1000.0, 1000.0), 0)]})
        band = next(n for n in material_notes.collect(body, {"mantle": v}, acc)
                    if n.kind == "material_band" and n.fields["edge"] == "dT/dP model consistency")
        self.assertEqual(band.fields["dtdp_error"], 5e-2)
        self.assertEqual(band.fields["p_at_max"], PS[22] * 1.1)


if __name__ == "__main__":
    unittest.main()
