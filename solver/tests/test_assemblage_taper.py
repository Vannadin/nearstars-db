# 데이터셋 상단 위 테이퍼 시험 — 인계 기록으로의 혼합, 136·끝 두 이음의 연속, 창 거절, ρ 상승 검사, 아래쪽 비트 동일 (규산염 기록 등록 §3.4, note 7)
"""Tests of the taper above p_dataset (silicate record registration §3.4, post-freeze notes 2, 3 §5 and 7).

A planted table (test_assemblage_view's grid, p_dataset = PS[-3], so the zone runs to 1.5·PS[-3] = PS[-2]) and a planted
hand-over: BM2 ρ near the table's at the dataset top, and a thermal block whose dT/dP and c_P differ from the table's,
so a blend that took the wrong source shows.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_assemblage_taper
"""
import math
import unittest

from solver import material_assemblage as ma
from solver import material_view as mv
from solver import stepper as st
from solver.tests.test_assemblage_boundaries import table as btable
from solver.tests.test_assemblage_view import PS, TS, record, table

PD = PS[-3]
PE = 1.5 * PD


def ho_dtdp(p, t):
    return 1.2e-8 * t / 1000.0 * (p / PD) ** -0.5


def ho_cp(p, t):
    return 1250.0 + 0.05 * t


def handover(rho0=3300.0, k0=1.3e11, p_max_at=None, refused=(), n=8):
    """A planted hand-over record and its table: nodes from PD up on 1.5, every T row of the table; `p_max_at` {T:
    the last node index} cuts a row's window; `refused` rows refuse."""
    nodes = [PD * 1.5 ** k for k in range(n)]
    rows = []
    for t in TS:
        last = (p_max_at or {}).get(t, n - 1)
        r = {"t": t, "dtdp": [ho_dtdp(p, t) for p in nodes[:last + 1]], "c_p": [ho_cp(p, t) for p in nodes[:last + 1]],
             "p_max": nodes[last], "cut": {"bound": "0 < alpha <= 2.0e-4 /K"}, "band_1": 1e-4, "band_eq": 2e-3}
        if t in refused:
            r["refused"] = "planted"
        rows.append(r)
    rec = {"id": "silicate_prem_test", "phases": [{"eos": {"params": {"rho0": {"value": rho0}, "k0": {"value": k0},
                                                                      "k0p": {"value": 4.0}}},
                                                    "window": {"p_max": nodes[-1]},
                                                    "thermal": {"grade": "planted hand-over grade"}}]}
    tb = {"id": "silicate_prem_test",
          "blocks": {"silicate_slb_test": {"p_nodes": nodes, "p_neighbour": PS[-4], "rows": rows}}}
    return ma.HandOver(rec, tb, "silicate_slb_test", PE)


def view(ho=None, tb=None):
    tb = tb or table()
    return ma.view(record(tb["p_dataset"]), tb, 1600.0, handover=ho)


def solid(v, p, t):
    got = v._solid(p, t)
    assert not isinstance(got, st.Stop), got.record.why
    return got


class Taper(unittest.TestCase):
    def test_read_past_the_top_gets_the_tapered_value(self):
        """A read past p_dataset answers the blend of note 7 §1; the planted control (no hand-over) refuses as before."""
        ho = handover()
        v = view(ho)
        p, t = math.sqrt(PD * PE), 2000.0
        rho, dtdp, cp, _ = solid(v, p, t)
        w = ma._smoothstep((p - PD) / (PE - PD))
        lift = v._lifted(p, t)
        cut0, lift0 = v._table_read(PD, t), v._lifted(PD, t)
        rs = lift[0] + (1 - w) * (cut0[0] - lift0[0])
        self.assertAlmostEqual(rho, 1.0 / ((1 - w) / rs + w / ho.rho(p)), delta=1e-9 * rho)
        ds = lift[1] + (1 - w) * (cut0[1] - lift0[1])
        self.assertAlmostEqual(dtdp, (1 - w) * ds + w * ho.thermal(p, t)[0][0], delta=1e-12 * dtdp)
        cs = lift[2] + (1 - w) * (cut0[2] - lift0[2])
        self.assertAlmostEqual(cp, (1 - w) * cs + w * ho.thermal(p, t)[0][1], delta=1e-9 * cp)
        got = view()._solid(p, t)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("taper to the hand-over is not built yet", got.record.why)

    def test_continuous_at_both_ends_in_every_field(self):
        """C⁰ at p_dataset and at the zone's end, ρ, dT/dP and c_P, on every T row and between rows. Mutant: dT/dP by
        A4's V-blend α (0 for a T-independent ρ) falls away from the hand-over's at the end."""
        n = 0
        hole = btable()                         # (R1)'s P-first read, with an outer-row hole at the top's node (as the
        for c in hole["cells"]:                                                                  # real 136 GPa ones)
            if c["t"] == 1450.0 and c["dtdp_eq"] is not None:
                c["dtdp_eq"] *= 1.0 + 0.003 * PS.index(c["p"]) ** 2     # curved in P, so an end slope and a gap differ
        next(c for c in hole["cells"] if c["p"] == PD and c["t"] == 1450.0)["dtdp_eq"] = None
        for v, ts_ in ((view(handover()), [x + d for x in TS[4:-1] for d in (0.0, 17.0)]),
                       (view(handover(), hole), (1360.0, 1375.0, 1530.0))):
            for t in ts_:
                for pe in (PD, PE):
                    a, b = v._solid(pe * (1 - 1e-12), t), v._solid(pe * (1 + 1e-12), t)
                    if isinstance(a, st.Stop) or isinstance(b, st.Stop):
                        continue
                    n += 1
                    for i in range(3):
                        self.assertLess(abs(b[i] / a[i] - 1.0), 1e-9, (pe, t, i))
        self.assertGreater(n, 150)
        v = view(handover(), hole)          # there the read below and the lifted one differ at the top, which the
        a, b = v._table_read(PD, 1360.0), v._lifted(PD, 1360.0)            # 136 GPa match takes out (note 7 delta)
        self.assertGreater(max(abs(b[i] / a[i] - 1.0) for i in range(3)), 1e-8)

    def test_the_zone_reads_the_columns_above_the_top(self):
        """Note 7 §2: the SLB-extrapolated read lifts the cut, so it takes the columns above p_dataset (at a node, the
        node's own value). Mutant: no lift (the read extrapolates from below the top)."""
        tb = table()
        v = view(handover(), tb)
        for t in (1200.0, 2500.0):
            c = next(c for c in tb["cells"] if c["p"] == PS[-2] and c["t"] == t)
            self.assertEqual(v._lifted(PS[-2], t)[0], c["rho"])

    def test_above_the_end_the_hand_over_alone(self):
        ho = handover()
        v = view(ho)
        p, t = PE * 1.3, 2000.0
        rho, dtdp, cp, cells = solid(v, p, t)
        self.assertEqual(rho, ho.rho(p))
        (hd, hc, _b), _why = ho.thermal(p, t)
        self.assertEqual((dtdp, cp, cells), (hd, hc, []))

    def test_window_refusal_names_the_bound(self):
        v = view(handover(p_max_at={2000.0: 2}))
        got = v._solid(PD * 1.5 ** 4, 2000.0)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("past the hand-over's thermal window", got.record.why)
        self.assertIn("0 < alpha <= 2.0e-4 /K", got.record.why)
        got = view(handover(refused=(2000.0,)))._solid(PE * 1.2, 2000.0)
        self.assertIn("refuses: planted", got.record.why)

    def test_above_the_last_node_refuses(self):
        """r2 E1/R1 on delta 1: the hand-over never extrapolates past its last thermal node or its window."""
        ho = handover()
        v = view(ho)
        got = v._solid(ho.ps[-1] * 1.01, 2000.0)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("above the hand-over's last thermal node", got.record.why)
        self.assertNotIsInstance(v._solid(ho.ps[-1] * 0.99, 2000.0), st.Stop)

    def test_zone_refuses_where_the_top_cannot_be_matched(self):
        """r2 D2 on delta 1: where the read below refuses at p_dataset on the read's T, the zone refuses by name (an
        unshifted lifted read there stepped the zone ×3 in T). Mutant: the unshifted read answers."""
        v = view(handover())
        real = v._table_read

        def table_read(p, t):
            if p == PD and 1990.0 < t < 2010.0:
                return v._refuse(p, t, "input.material_out_of_data", "planted: no read at the top")
            return real(p, t)
        v._table_read = table_read
        got = v._solid(math.sqrt(PD * PE), 2000.0)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("cannot be matched", got.record.why)
        self.assertNotIsInstance(v._solid(math.sqrt(PD * PE), 2050.0), st.Stop)

    def test_match_size_in_the_band(self):
        """r2 D3 on delta 1: the 136 GPa match's (1 − w)·|ΔX|/|X| is added to that field's band."""
        hole = btable()
        for c in hole["cells"]:
            if c["t"] == 1450.0 and c["dtdp_eq"] is not None:
                c["dtdp_eq"] *= 1.0 + 0.003 * PS.index(c["p"]) ** 2
        next(c for c in hole["cells"] if c["p"] == PD and c["t"] == 1450.0)["dtdp_eq"] = None
        ho = handover()
        v = view(ho, hole)
        p, t = PD * 1.01, 1360.0
        v.notes.clear()
        solid(v, p, t)
        (n,) = [x for x in v.notes if isinstance(x, mv.BandNote) and x.edge == "taper to the hand-over"]
        w = ma._smoothstep((p - PD) / (PE - PD))
        cut0, lift0 = v._table_read(PD, t), v._lifted(PD, t)
        cells = v._lifted(p, t)[3]
        bc = max(c["dtdp_eq_band"] for c in cells if c.get("dtdp_eq_band") is not None)
        want = max((1 - w) * bc, w * ho.thermal(p, t)[0][2]) + (1 - w) * abs(cut0[1] - lift0[1]) / abs(cut0[1])
        self.assertAlmostEqual(n.dtdp_error, want, delta=1e-15)
        self.assertGreater((1 - w) * abs(cut0[1] - lift0[1]) / abs(cut0[1]), 1e-9)

    def test_zone_rho_must_rise(self):
        """Note 7 §5: a hand-over much lighter than the table makes the zone's ρ fall with P; that T row refuses by
        name, and rows where it rises answer. Mutant: the check off (the falling ρ answers)."""
        v = view(handover(rho0=2600.0))
        got = v._solid(math.sqrt(PD * PE), 2000.0)
        self.assertIsInstance(got, st.Stop)
        self.assertIn("ρ does not rise with P across the taper zone", got.record.why)
        self.assertIsNone(view(handover())._rise_ok(TS.index(2000.0)))

    def test_bands_one_per_field(self):
        """Note 7 §4: the ρ band is the local |ρ_SLB − ρ_HO|/ρ_SLB; the dT/dP band max((1 − w)·the cell's band,
        w·band_HO)."""
        ho = handover()
        v = view(ho)
        for p, t in ((math.sqrt(PD * PE), 2000.0), (PD * 1.01, 2000.0)):   # w·band_HO wins mid-zone, the cell's near the top
            v.notes.clear()
            solid(v, p, t)
            (n,) = [x for x in v.notes if isinstance(x, mv.BandNote) and x.edge == "taper to the hand-over"]
            w = ma._smoothstep((p - PD) / (PE - PD))
            cells = v._lifted(p, t)[3]
            bc = max(c["dtdp_eq_band"] for c in cells if c.get("dtdp_eq_band") is not None)
            self.assertAlmostEqual(n.dtdp_error, max((1 - w) * bc, w * ho.thermal(p, t)[0][2]), delta=1e-15)
            self.assertEqual(n.grade, ma.TAPER_GRADE)
        self.assertGreater((1 - w) * bc, w * ho.thermal(p, t)[0][2])

    def test_below_the_top_bit_identical(self):
        """Reads at P ≤ p_dataset do not change with the hand-over present (note 7 §2)."""
        a, b = view(), view(handover())
        for i in range(len(PS) - 3):
            p = math.sqrt(PS[i] * PS[i + 1])
            for t in (450.0, 1210.0, 2525.0, 4400.0):
                ga, gb = a._solid(p, t), b._solid(p, t)
                if isinstance(ga, st.Stop):
                    self.assertEqual(ga.record.why, gb.record.why)
                else:
                    self.assertEqual(ga[:3], gb[:3])
        self.assertEqual(a._solid(PD, 2000.0)[:3], b._solid(PD, 2000.0)[:3])

    def test_hand_over_rho_is_bm2_and_t_independent(self):
        """ρ_HO is BM2 on the PREM path, ρ0 at P = 0, and takes no T (note 2 item 2)."""
        ho = handover()
        self.assertAlmostEqual(ho.rho(0.0), 3300.0, delta=1e-9)
        for p in (1e9, PD, PE, 1e12):
            x = ho.rho(p) / 3300.0
            self.assertAlmostEqual(1.5 * 1.3e11 * (x ** (7 / 3) - x ** (5 / 3)), p, delta=1e-9 * p)
        self.assertEqual(ma.HandOver.rho.__code__.co_varnames[:2], ("self", "p"))
        self.assertEqual(ma.HandOver.rho.__code__.co_argcount, 2)


class HandOverRecord(unittest.TestCase):
    """The hand-over record's shape at load (note 7 §3): a single record of the handover form, its BM2 params, dT/dP
    from its pinned handover_table; the table's sha256, id and blocks checked."""

    def write(self, d, rec_edit=None, table_edit=None):
        import gzip
        import hashlib
        import json
        from pathlib import Path
        tb = {"id": "silicate_prem_test", "blocks": {"silicate_slb_x": {
            "p_nodes": [1.36e11, 2.04e11], "p_neighbour": 2.0e11,
            "rows": [{"t": 2000.0, "dtdp": [1e-8, 9e-9], "c_p": [1200.0, 1190.0], "p_max": 2.04e11}]}}}
        if table_edit:
            table_edit(tb)
        raw = gzip.compress(json.dumps(tb).encode(), mtime=0)
        (Path(d) / "tables").mkdir()
        (Path(d) / "tables" / "silicate_prem_test.json.gz").write_bytes(raw)
        src = {"cache": "2016ApJ...819..127Z.pdf", "page": "–3–", "where": "§2",
               "sha256": "80d1f3b0c360722f205a54ce24ec5b00dbc8966216dc3b7ade45eafc5b6b2422"}
        rec = {"id": "silicate_prem_test", "label": "t", "kind": "single", "system": "silicate", "fit_composition": "x",
               "requires_switch": "silicate_records",
               "primary_family": {"name": "Zeng", "sources": ["2016ApJ...819..127Z.pdf"], "reason": "test"},
               "handover_table": {"file": "tables/silicate_prem_test.json.gz",
                                  "sha256": hashlib.sha256(raw).hexdigest(), "blocks": ["silicate_slb_x"]},
               "phases": [{"id": "lm", "state": "solid",
                           "eos": {"form": "handover", "params": {
                               "rho0": {"value": 3980.0, "unit": "kg/m3", "grade": "read", "source": src},
                               "k0": {"value": 2.06e11, "unit": "Pa", "grade": "read", "source": src},
                               "k0p": {"value": 4.0, "unit": "1", "grade": "declared", "source": src}},
                               "reference": {"kind": "path", "path": "PREM path"}},
                           "thermal": {"source_state": "solid", "source_composition": "x",
                                       "from_assemblage": "handover_table"},
                           "field": {"kind": "declared", "box": {"p_min": 1.36e11, "p_max": 3.5e12}, "reason": "t"},
                           "window": {"p_min": 1.36e11, "p_max": 3.5e12}, "edges": {}}],
               "formula_checks": [{"quantity": "rho0", "state": {}, "expected": 3980.0, "unit": "kg/m3",
                                   "tolerance": 0.0, "tolerance_reason": "identity", "expression": "params.rho0",
                                   "source": src}]}
        if rec_edit:
            rec_edit(rec)
        import yaml
        (Path(d) / "silicate_prem_test.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
        import shutil
        from solver import material_registry as mr
        shutil.copy(mr.MATERIALS_DIR / "schema.yaml", Path(d) / "schema.yaml")
        shutil.copy(mr.MATERIALS_DIR / "sources.yaml", Path(d) / "sources.yaml")
        return mr.load(Path(d))

    def load(self, **kw):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            return self.write(d, **kw)

    def test_loads_with_its_table(self):
        from solver import material_registry as mr
        reg = self.load()
        self.assertIsInstance(reg, mr.Registry, getattr(reg, "evidence", None))
        self.assertEqual(sorted(reg.tables["silicate_prem_test"]["blocks"]), ["silicate_slb_x"])

    def test_shape_and_pins_refuse(self):
        from solver import material_registry as mr
        def no_table(r):
            del r["handover_table"]
        def bad_thermal(r):
            del r["phases"][0]["thermal"]["from_assemblage"]
        def bad_sha(r):
            r["handover_table"]["sha256"] = "0" * 64
        def other_blocks(r):
            r["handover_table"]["blocks"] = ["silicate_slb_y"]
        def stray(r):
            r["phases"][0]["eos"]["form"] = "bm2"
        for edit in (no_table, bad_thermal, bad_sha, other_blocks, stray):
            got = self.load(rec_edit=edit)
            self.assertIsInstance(got, mr.LoadStop, edit.__name__)
        got = self.load(table_edit=lambda tb: tb["blocks"]["silicate_slb_x"]["rows"][0]["c_p"].append(1.0))
        self.assertIsInstance(got, mr.LoadStop)


if __name__ == "__main__":
    unittest.main()
