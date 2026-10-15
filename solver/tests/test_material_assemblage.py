# 광물 집합 기록 시험 — 조성 지문, 압축 표 sha·B3 적재 검사(Maxwell 의 FD 맹점 면제 포함), 개발 기록 거부, 종류 규칙 (규산염 기록 등록 §2, 사후 노트 3)
"""Tests of the assemblage-kind record (rewrite/phase2-silicate-record-registration.frozen.md §2.1–§2.3 as post-freeze
note 3 amends them). The table is synthetic: an analytic G with v = v0(1 − P/K) + c(T − 300) and
s = s0 + c_P ln(T/300) − cP, so every B3 identity holds exactly and each planted defect is the only one.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_assemblage
"""
import copy
import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path

import yaml

from solver import material_assemblage as ma
from solver import material_registry as mr

V0, K, C, CP = 1 / 3300.0, 5e10, 1e-8, 1200.0
P_TOP = 2e10 * 1.05 ** 8                                       # the synthetic grid's last P node, its p_dataset
B3 = {"gamma_tolerance": 1e-9, "frozen_alpha_tolerance": 2e-2, "maxwell_k": 3.0, "maxwell_floor": 1e-3,
      "reason": "test"}
BSE = {"SiO2": 45.0, "TiO2": 0.201, "Al2O3": 4.45, "Cr2O3": 0.384, "MnO": 0.135, "FeO": 8.05, "NiO": 0.25,
       "MgO": 37.8, "CaO": 3.55, "Na2O": 0.36, "K2O": 0.029, "P2O5": 0.021}


def table(steps=()):
    """9 × 9 nodes (P 20 GPa × 1.05^i, T 200–600 K); frozen below 350 K. `steps`: (P, ΔS) steps in s between nodes, a
    G with sharp features between nodes: the model's exact derivatives at the nodes are the smooth ones."""
    ps = [2e10 * 1.05 ** i for i in range(9)]
    ts = [200.0 + 50 * k for k in range(9)]
    cells = []
    for p in ps:
        for t in ts:
            v = V0 * (1 - p / K) + C * (t - 300)
            s = 3000 + CP * math.log(t / 300) - C * p - sum(a for q, a in steps if p > q)
            fr = t < 350
            c = {"p": p, "t": t, "kind": "frozen" if fr else "equilibrium", "grade": None, "assemblage": "ol+opx",
                 "rho": 1 / v, "s": s, "c_p": CP, "c_v": 1150.0, "alpha_k_t": (C / v) * (v * K / V0),
                 "dtdp_s": t * C / CP, "freeze_t": 350.0 if fr else None,
                 "freeze_class": "convergence edge" if fr else None}
            c["gamma"] = c["alpha_k_t"] / (c["rho"] * c["c_v"])
            c.update({f"{f}_model": c[f] for f in ma.MODEL_FIELDS})
            if fr:
                c.update(dtdp_eq=c["dtdp_s"], dtdp_eq_from="frozen: dtdp_s", dtdp_eq_band=None, dtdp_g=None,
                         dv_dt_model=None, ds_dp_model=None, envelope_gap_v=None, envelope_gap_s=None)
            else:
                c.update(dtdp_eq=c["dtdp_s"], dtdp_eq_from="model", dtdp_eq_band=2.5e-4, dtdp_g=c["dtdp_s"],
                         dv_dt_model=C, ds_dp_model=-C, envelope_gap_v=1e-6, envelope_gap_s=1e-7,
                         c_p_eq=-(-C) * t / c["dtdp_s"])          # dtdp_eq = −ds_dp·T/c_p_eq
            cells.append(c)
    cols = [{"p": p, "t_sol": 1000.0, "t_window_top": ts[-1], "window": {"cause": "grid_end"}} for p in ps]
    return {"cells": cells, "columns": cols, "p_dataset": ps[-1],
            "boundaries": {"status": "pending", "why": "test", "rows": []},
            "feature_regions": {"status": "pending", "why": "test", "rows": []},
            "dtdp_eq_refused": [], "dtdp_eq_source": {"table_blob": "x"}, "source": {}}


def asm(refused=0):
    return {"b3": dict(B3), "dtdp": {"refused_count": refused, "band_floor": 2.5e-4}}


def cell(tb, i, k):
    ps = sorted({c["p"] for c in tb["cells"]})
    ts = sorted({c["t"] for c in tb["cells"]})
    return next(c for c in tb["cells"] if c["p"] == ps[i] and c["t"] == ts[k])


def record(sha, status="development", **over):
    rid = "silicate_slb_test"
    rec = {
        "id": rid, "label": "test", "kind": "assemblage", "system": "silicate", "fit_composition": "default_bse",
        "role_hint": "mantle", "composition_key": ma.composition_key(BSE),
        "primary_family": {"name": "SLB", "sources": ["BurnMan@2.1.0"], "reason": "test"},
        "assemblage": {
            "file": f"tables/{rid}.json", "sha256": sha, "p_dataset": P_TOP, "interpolation": "c1_lnp_t",
            "melt_variant": "peridotitic", "frozen_classes": ["convergence edge"], "dataset": "test",
            "disclosures": ["test"], "floor_band": {"origin": "test"}, "handover": "silicate_prem_zeng2016",
            "b3": dict(B3),
            "dtdp": {"field": "equilibrium_isentrope", "band_floor": 2.5e-4, "band_origin": "test", "refused_count": 0,
                     "sidecar": {"table_blob": "x"}},
            "pins": {"status": status, "table_blob": "b" * 40,
                     "builders": [{"role": "strict", "blob": "b" * 40, "sha256": "s" * 64}],
                     "compact_sha256": sha, "rebuilt": []}},
        "phases": [{
            "id": "slb_assemblage", "state": "solid",
            "eos": {"form": "assemblage", "reference": {"kind": "path", "path": "SLB assemblage table"}},
            "thermal": {"source_state": "solid", "source_composition": "default_bse"},
            "field": {"kind": "declared", "box": {"p_min": 2e10, "p_max": P_TOP, "t_min": 200.0, "t_max": 600.0},
                      "reason": "test"},
            "window": {"p_min": 2e10, "p_max": P_TOP, "t_min": 200.0, "t_max": 600.0},
            "edges": {"p_max": {"refusal": "input.material_out_of_data"},
                      "t_min": {"refusal": "input.material_out_of_data"},
                      "t_max": {"refusal": "input.material_above_solid_window"}}}],
        "formula_checks": [{"quantity": "gamma", "state": {"p": 2e10, "t": 300.0}, "expected": 1.0, "unit": "1",
                            "tolerance": 1e-9, "tolerance_reason": "test", "expression": "alpha_k_t / (rho * c_v)",
                            "source": {"formula": "test"}}],
    }
    rec.update(over)
    return rec


def write(d, tb, status="development", rec_over=None, sha=None):
    body = (json.dumps(tb, sort_keys=True, separators=(",", ":")) + "\n").encode()
    (Path(d) / "tables").mkdir(exist_ok=True)
    (Path(d) / "tables/silicate_slb_test.json").write_bytes(body)
    rec = record(sha or hashlib.sha256(body).hexdigest(), status)
    for k, v in (rec_over or {}).items():
        if v is None:
            rec.pop(k)
        else:
            rec[k] = v
    (Path(d) / "silicate_slb_test.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")


class CompositionKey(unittest.TestCase):
    def test_key_and_one_oxide_misses(self):
        """§2.1, §7 item 10: the key is the generator's (it imports this function); BSE's is pinned; one changed
        oxide misses; a non-CFMASNa oxide does not move it (they are dropped before the reduction)."""
        self.assertEqual(ma.composition_key(BSE), "14f8758a7681f418")
        self.assertNotEqual(ma.composition_key({**BSE, "MgO": 37.81}), ma.composition_key(BSE))
        self.assertEqual(ma.composition_key({**BSE, "TiO2": 0.3}), ma.composition_key(BSE))


class TableChecks(unittest.TestCase):
    def test_clean_table_passes(self):
        r = ma.check_table(asm(), table())
        self.assertGreater(r["maxwell_gated"], 0)
        self.assertEqual(r["maxwell_fd_blind"], [])
        self.assertLess(r["frozen_alpha_max"], 1e-3)

    def stops(self, tb, a=None, why=""):
        with self.assertRaisesRegex(ma.TableStop, why):
            ma.check_table(a or asm(), tb)

    def test_planted_controls(self):
        """A single-field 1 % bump of any stored field the engine reads, at a frozen or a non-frozen cell, fails the
        stored-value gate (r2's ruling on the 1 % bump finding: the adaptive Maxwell tolerance cannot see a one-node
        spike). The other checks are tested with the model value moved too, so each is the only one that can fail:
        γ identity, a hole, the frozen in-column identity, a missing dT/dP not listed, a band not its recomputation."""
        for f in ma.MODEL_FIELDS:
            for k in (1, 5):
                with self.subTest(field=f, kind="frozen" if k == 1 else "equilibrium"):
                    tb = table(); cell(tb, 4, k)[f] *= 1.01
                    self.stops(tb, why="differ from the model")

        def both(tb, i, k, f, factor):
            c = cell(tb, i, k); c[f] *= factor; c[f"{f}_model"] = c[f]
        tb = table(); both(tb, 4, 5, "gamma", 1 + 1e-6)
        self.stops(tb, why="γ")
        tb = table(); tb["cells"].remove(cell(tb, 4, 5))
        self.stops(tb, why="hole")
        tb = table(); both(tb, 4, 1, "dtdp_s", 1.05); cell(tb, 4, 1)["dtdp_eq"] = cell(tb, 4, 1)["dtdp_s"]
        self.stops(tb, why="frozen cell")
        tb = table(); cell(tb, 4, 5)["dtdp_eq"] = None
        self.stops(tb, why="not listed as refused")
        for f in ("dtdp_g", "dtdp_eq_band"):
            with self.subTest(field=f):
                tb = table(); cell(tb, 4, 5)[f] *= 1.01
                self.stops(tb, why="recomputation")
        for f in ("dtdp_eq", "c_p_eq", "ds_dp_model"):                     # r2 B1 on note 3: c_p_eq's guard
            with self.subTest(field=f):
                tb = table(); cell(tb, 4, 5)[f] *= 1.01
                self.stops(tb, why="−ds_dp·T/c_p_eq")

    def test_planted_coverage_synthetic(self):
        """r2 condition 3: every field the engine reads × cell kind is caught by a named check."""
        cov = ma.planted_coverage(asm(), table(), per=3)
        self.assertTrue(cov)
        for key, row in cov.items():
            with self.subTest(pair=key):
                self.assertEqual((row["caught"], row["missed"]), (row["tried"], []))
                self.assertGreater(row["tried"], 0)

    @unittest.skipUnless(sorted((mr.MATERIALS_DIR / "tables").glob("silicate_slb_*.json")),
                         "no shipped silicate assemblage tables yet")
    def test_planted_coverage_real(self):
        """r2 conditions 2–3 on the shipped records: seeded single-field 1 % bumps per field × kind are all caught."""
        reg = mr.load()
        for rid, tb in reg.tables.items():
            cov = ma.planted_coverage(reg[rid]["assemblage"], tb, per=5, seed=1)
            for key, row in cov.items():
                with self.subTest(record=rid, pair=key):
                    self.assertEqual(row["missed"], [])

    def test_gate_near_zero(self):
        """r2 NB 3: a field at 0 with a model value of 0 passes, and one at 0 against a nonzero model fails, without a
        division by zero (each field's declared scale floor)."""
        for f in ma.MODEL_FIELDS:
            c = {**cell(table(), 4, 5)}
            c[f] = c[f"{f}_model"] = 0.0
            self.assertEqual(ma._model_miss(c)[0], 0.0)
            c[f"{f}_model"] = 10.0 * ma.FIELD_SCALE[f]
            self.assertGreater(ma._model_miss(c)[0], ma.STORED_MODEL_REL)

    def test_c_p_eq_guards(self):
        """68 on 9582a67b: a negative c_p_eq with dtdp_eq flipped along (the recompute and band still hold) STOPs as
        positivity; a refused cell's NaN c_p_eq (read as an outer stencil node) STOPs as finite fields."""
        tb = table(); c = cell(tb, 4, 5)
        c["c_p_eq"], c["dtdp_eq"] = -c["c_p_eq"], -c["dtdp_eq"]
        c["dtdp_eq_band"] = ma.band(c["dtdp_eq"], c["dtdp_g"], c["dtdp_s"], 2.5e-4)
        with self.assertRaises(ma.TableStop) as cm:
            ma.check_table(asm(), tb)
        self.assertEqual(cm.exception.check, "positivity")
        tb = table(); c = cell(tb, 4, 5)
        c.update(dtdp_eq=None, dtdp_eq_band=None, c_p_eq=float("nan"))
        tb["dtdp_eq_refused"] = [{"p": c["p"], "t": c["t"]}]
        with self.assertRaises(ma.TableStop) as cm:
            ma.check_table(asm(refused=1), tb)
        self.assertEqual(cm.exception.check, "finite fields")

    def test_cell_without_model_values(self):
        """r2 condition 2: a cell the stored-value gate cannot cover (no model values) is a STOP for a ruling."""
        tb = table(); cell(tb, 4, 5).update({f"{f}_model": None for f in ma.MODEL_FIELDS})
        self.stops(tb, why="no model values")

    def test_non_finite_model_values(self):
        """68 B1: a NaN or partial model group, or a NaN exact derivative, STOPs; it never switches a gate off."""
        for f in ma.MODEL_FIELDS:
            with self.subTest(field=f):
                tb = table(); c = cell(tb, 4, 5); c[f] *= 1.01; c[f"{f}_model"] = float("nan")
                self.stops(tb, why="neither all absent nor all finite")
        tb = table(); cell(tb, 4, 5)["c_p_model"] = None
        self.stops(tb, why="neither all absent nor all finite")
        ps = [2e10 * 1.05 ** i for i in range(9)]
        steps = ((0.5 * (ps[4] + ps[5]), 1.0), (0.5 * (ps[5] + ps[6]), 1.0))
        tb = table(steps)
        for c in tb["cells"]:
            if c["kind"] != "frozen":
                c["dv_dt_model"] = float("nan")
        self.stops(tb, why="exact derivatives are neither")
        tb = table(); cell(tb, 4, 5)["ds_dp_model"] = None          # caught first by the field rule's presence check
        self.stops(tb, why="exact derivatives are neither|envelope gap is missing")

    def test_guards(self):
        """68 B2: one planted control per check_table guard (each the only defect)."""
        def both(c, f, x):
            c[f] = x
            if f"{f}_model" in c and c[f"{f}_model"] is not None:
                c[f"{f}_model"] = x
        cases = []
        tb = table()                                        # M9: ρ falls with P inside one state
        for k in range(9):
            a, b = cell(tb, 3, k), cell(tb, 4, k)
            if a["kind"] != "frozen":
                both(b, "rho", a["rho"] * 0.999)
                b["gamma"] = b["gamma_model"] = b["alpha_k_t"] / (b["rho"] * b["c_v"])
                break
        cases.append((tb, "ρ does not rise"))
        for f in ("c_p", "c_v", "alpha_k_t", "dtdp_s"):        # M10: positivity, each field
            tb = table(); c = cell(tb, 4, 5); both(c, f, -abs(c[f]))
            c["gamma"] = c["gamma_model"] = c["alpha_k_t"] / (c["rho"] * c["c_v"])
            cases.append((tb, "must be > 0"))
        tb = table(); cell(tb, 4, 5)["dtdp_eq_from"] = "frozen: dtdp_s"   # M14
        cases.append((tb, "dT/dP field"))
        tb = table(); tb["columns"] = tb["columns"][:-1]     # M15
        cases.append((tb, "column list"))
        tb = table(); tb["columns"][2]["window"] = {"cause": "made_up"}   # M16
        cases.append((tb, "window cause"))
        tb = table(); tb["cells"].append(dict(tb["cells"][10]))           # M17
        cases.append((tb, "share a node"))
        tb = table(); cell(tb, 4, 5)["s"] = float("inf")                   # M18
        cases.append((tb, "not a finite number"))
        tb = table(); cell(tb, 4, 5)["dtdp_eq"] = "1e-8"                   # 68 N2: a string, not a crash
        cases.append((tb, "not a finite number"))
        tb = table(); cell(tb, 4, 5)["p"] = "2e10"
        cases.append((tb, "finite numbers"))
        tb = table(); tb["columns"].append(dict(tb["columns"][0]))         # 68 N3: duplicate columns
        cases.append((tb, "two columns share"))
        tb = table(); fr = cell(tb, 4, 0)                                  # M27: a refused entry naming a frozen node
        tb["dtdp_eq_refused"] = [{"p": fr["p"], "t": fr["t"]}]
        cases.append((tb, "refused dT/dP list names"))
        tb = table(); tb["dtdp_eq_refused"] = [{"p": 1.0, "t": 1.0}]       # … or an absent one
        cases.append((tb, "refused dT/dP list names"))
        tb = table(); top = cell(tb, 4, 8); extra = dict(top); extra["t"] = top["t"] + 50.0   # M28
        tb["cells"].append(extra)
        cases.append((tb, "last cell is not its window top|hole"))
        for tb, why in cases:
            with self.subTest(why=why):
                self.stops(tb, why=why)

    def test_grid_assumptions(self):
        """68 B1 on 2390a7e2: the T grid starts at the view's floor, and p_dataset is a P node of the table."""
        tb = table(); tb["cells"] = [c for c in tb["cells"] if c["t"] > 200.0]
        self.stops(tb, why="first T node")
        for pd in (2e10 * 1.05 ** 9, 0.5 * (2e10 + 2e10 * 1.05)):        # above the last node; between two nodes
            tb = table(); tb["p_dataset"] = pd
            with self.subTest(p_dataset=pd):
                self.stops(tb, why="not a P node")

    def test_boundaries_status(self):
        """68 R16: a missing or unknown boundaries.status STOPs with check «structure» (the resolver reads it)."""
        for bad in (None, {"status": "made_up"}, {}):
            tb = table()
            if bad is None:
                tb.pop("boundaries")
            else:
                tb["boundaries"] = bad
            with self.subTest(boundaries=bad):
                with self.assertRaises(ma.TableStop) as cm:
                    ma.check_table(asm(), tb)
                self.assertEqual(cm.exception.check, "structure")
                self.assertIn("boundaries.status", str(cm.exception))

    def test_freeze_t_breaks_one_state(self):
        """68 M22: frozen neighbours with different freeze_t are not one state, so the in-column identity is not
        formed across them: a dtdp_s that fails it with equal freeze_t passes with a different one."""
        def bad(tb):
            c = cell(tb, 4, 1)
            c["dtdp_s"] *= 1.05; c["dtdp_s_model"] = c["dtdp_s"]; c["dtdp_eq"] = c["dtdp_s"]
            return tb
        self.stops(bad(table()), why="frozen cell")
        tb = bad(table())
        for k in (0, 2):
            cell(tb, 4, k)["freeze_t"] = 999.0
        ma.check_table(asm(), tb)

    def test_refused_dtdp_cell(self):
        """Note 3 §2 condition 4: a listed not-converged cell has no value, the record counts it."""
        tb = table(); c = cell(tb, 4, 5)
        c.update(dtdp_eq=None, dtdp_eq_band=None)
        tb["dtdp_eq_refused"] = [{"p": c["p"], "t": c["t"]}]
        self.assertEqual(ma.check_table(asm(refused=1), tb)["dtdp_eq_refused"], 1)
        self.stops(tb, asm(refused=0), why="refused dT/dP cells")

    def test_maxwell_fd_blind_excuse(self):
        """r2's Maxwell rulings: two steps in s half a node apart defeat Richardson (D_h ≈ D_2h). The model's exact
        derivatives there are the smooth ones, so the cells are excused as FD-blind; without exact derivatives they
        fail; a 1 % ρ bump at an excused cell, or at a P neighbour in its stencil, fails through the stored-value
        condition, not excused. (A bump that makes the FD check pass is not excused either: it is not a failure.)"""
        ps = [2e10 * 1.05 ** i for i in range(9)]
        steps = ((0.5 * (ps[4] + ps[5]), 1.0), (0.5 * (ps[5] + ps[6]), 1.0))
        r = ma.check_table(asm(), table(steps))
        self.assertTrue(r["maxwell_fd_blind"])
        p_ex, t_ex = r["maxwell_fd_blind"][0][:2]
        tb = table(steps)
        for c in tb["cells"]:
            c["dv_dt_model"] = c["ds_dp_model"] = None
        self.stops(tb, why="no exact derivatives")
        for di, dk in ((0, 0), (1, 0)):
            tb = table(steps)
            i, k = ps.index(p_ex) + di, int((t_ex - 200) / 50) + dk
            cell(tb, i, k)["rho"] *= 1.01
            with self.subTest(node=(di, dk)):
                self.stops(tb, why="differ from the model")

    def test_exact_maxwell_not_small_enough(self):
        """An FD failure is excused only if the model's exact Maxwell is ≤ the gate's tol at the cell (note 5, r2 (iii))."""
        ps = [2e10 * 1.05 ** i for i in range(9)]
        steps = ((0.5 * (ps[4] + ps[5]), 1.0), (0.5 * (ps[5] + ps[6]), 1.0))
        tb = table(steps)
        for c in tb["cells"]:
            if c["kind"] != "frozen":
                c["ds_dp_model"] = -C * 1.5
        self.stops(tb, why="over the gate's tol")

    def test_exact_within_tol_boundary(self):
        """68's pair (r2 (iii) condition (b)): at an FD-failing cell, exact Maxwell just under the cell's tol is excused
        (FD, exact and tol listed), just over it STOPs. The exact residual is set through dv_dt_model alone, so the
        dT/dP recompute (ds_dp_model, c_p_eq) is untouched: exact = x/(1+x) for dv = −ds·(1+x)."""
        ps = [2e10 * 1.05 ** i for i in range(9)]
        steps = ((0.5 * (ps[4] + ps[5]), 1.0), (0.5 * (ps[5] + ps[6]), 1.0))
        r = ma.check_table(asm(), table(steps))
        p_ex, t_ex, fd, _e, tol = r["maxwell_fd_blind"][0]
        self.assertGreater(fd, tol)
        for factor, excused in ((0.99, True), (1.01, False)):
            tb = table(steps)
            c = next(x for x in tb["cells"] if (x["p"], x["t"]) == (p_ex, t_ex))
            e = factor * tol
            c["dv_dt_model"] = -c["ds_dp_model"] * (1.0 + e / (1.0 - e))
            with self.subTest(factor=factor):
                if excused:
                    got = ma.check_table(asm(), tb)["maxwell_fd_blind"]
                    row = next(x for x in got if x[:2] == (p_ex, t_ex))
                    self.assertAlmostEqual(row[3], e, delta=1e-12)
                    self.assertEqual(row[4], tol)
                else:
                    self.stops(tb, why="over the gate's tol")

    def test_sha_pin(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, table(), sha="0" * 64)
            got = mr.load(Path(d), allow_development=True)
        self.assertIsInstance(got, mr.LoadStop)
        self.assertEqual(got.id, "material.assemblage_table")       # 68 M3: the sha pin itself, nothing else
        self.assertIn("sha256", got.evidence["why"])


class RegistryLoad(unittest.TestCase):
    def test_development_record_only_in_tests(self):
        """68: a development record is refused unless the test asks; a pinned one loads; the table is kept."""
        with tempfile.TemporaryDirectory() as d:
            write(d, table())
            no = mr.load(Path(d))
            yes = mr.load(Path(d), allow_development=True)
        self.assertIsInstance(no, mr.LoadStop)
        self.assertEqual(no.id, "material.assemblage_table")
        self.assertIn("development", no.evidence["why"])
        self.assertIsInstance(yes, mr.Registry)
        self.assertIn("silicate_slb_test", yes.tables)
        with tempfile.TemporaryDirectory() as d:
            write(d, table(), status="pinned")
            self.assertIsInstance(mr.load(Path(d)), mr.Registry)

    def test_sha_mismatch_stops(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, table(), status="pinned")
            p = Path(d) / "tables/silicate_slb_test.json"
            p.write_bytes(p.read_bytes().replace(b"ol+opx", b"ol+opy", 1))
            got = mr.load(Path(d))
        self.assertEqual(got.id, "material.assemblage_table")
        self.assertIn("sha256", got.evidence["why"])

    def test_kind_rules(self):
        """§2.1: an assemblage record without its key or table STOPs; it has none of the seven forbidden keys (68 M5b);
        one phase only (M6)."""
        cases = [({"composition_key": None}, "composition_key"), ({"assemblage": None}, "assemblage")]
        cases += [({k: v}, "has no") for k, v in (("boundaries", []), ("joins", []), ("triple_points", []),
                                                 ("choice", "chain"), ("source_seams", []),
                                                 ("field_probe", {"box": {"p_min": 1.0, "p_max": 2.0}, "dp": 1.0,
                                                                  "dt": 1.0}),
                                                 ("field_probes", []))]
        two = record("0" * 64)["phases"] * 2
        cases.append(({"phases": [two[0], {**two[1], "id": "b"}]}, "one phase"))
        for over, why in cases:
            with self.subTest(why=why), tempfile.TemporaryDirectory() as d:
                write(d, table(), status="pinned", rec_over=over)
                got = mr.load(Path(d))
                self.assertEqual(got.id, "material.kind_rule")
                self.assertIn(why, got.evidence["why"])

    def test_registry_guards(self):
        """68 B2: the sha ≠ compact_sha256 (M3), assemblage keys on another kind (M4), an absolute or «..» path (M7),
        a p_dataset mismatch (M8)."""
        with tempfile.TemporaryDirectory() as d:
            write(d, table(), status="pinned")
            rec = yaml.safe_load((Path(d) / "silicate_slb_test.yaml").read_text())
            rec["assemblage"]["pins"]["compact_sha256"] = "0" * 64
            (Path(d) / "silicate_slb_test.yaml").write_text(yaml.safe_dump(rec, sort_keys=False))
            got = mr.load(Path(d))
        self.assertEqual((got.id, "compact_sha256" in got.evidence["why"]), ("material.kind_rule", True))
        for over in ({"kind": "single"},):
            with tempfile.TemporaryDirectory() as d:
                write(d, table(), status="pinned", rec_over=over)
                got = mr.load(Path(d))
            self.assertEqual(got.id, "material.kind_rule")
            self.assertIn("belong to an assemblage record", got.evidence["why"])
        for path in ("/tmp/x.json", "../x.json"):
            with tempfile.TemporaryDirectory() as d:
                write(d, table(), status="pinned")
                rec = yaml.safe_load((Path(d) / "silicate_slb_test.yaml").read_text())
                rec["assemblage"]["file"] = path
                (Path(d) / "silicate_slb_test.yaml").write_text(yaml.safe_dump(rec, sort_keys=False))
                got = mr.load(Path(d))
            with self.subTest(path=path):
                self.assertEqual(got.id, "material.assemblage_table")
                self.assertIn("a path under solver/materials", got.evidence["why"])
        with tempfile.TemporaryDirectory() as d:
            tb = table(); tb["p_dataset"] = 2e10 * 1.05 ** 7                     # a node, but not the record's
            write(d, tb, status="pinned")
            got = mr.load(Path(d))
        self.assertEqual(got.id, "material.assemblage_table")
        self.assertIn("p_dataset", got.evidence["why"])

    def test_gzip_table(self):
        """The shipped form: a gzip-packed compact table, the sha pinned on the packed bytes, loads as the plain one."""
        import gzip
        tb = table()
        raw = (json.dumps(tb, sort_keys=True, separators=(",", ":")) + "\n").encode()
        packed = gzip.compress(raw, compresslevel=9, mtime=0)
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "tables").mkdir()
            (Path(d) / "tables/silicate_slb_test.json.gz").write_bytes(packed)
            rec = record(hashlib.sha256(packed).hexdigest(), "pinned")
            rec["assemblage"]["file"] = "tables/silicate_slb_test.json.gz"
            (Path(d) / "silicate_slb_test.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
            reg = mr.load(Path(d))
            self.assertIsInstance(reg, mr.Registry)
            self.assertEqual(len(reg.tables["silicate_slb_test"]["cells"]), len(tb["cells"]))
            rec["assemblage"]["sha256"] = rec["assemblage"]["pins"]["compact_sha256"] = hashlib.sha256(raw).hexdigest()
            (Path(d) / "silicate_slb_test.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
            got = mr.load(Path(d))                     # a pin on the unpacked bytes does not match: a STOP
            self.assertEqual(got.id, "material.assemblage_table")
            (Path(d) / "tables/silicate_slb_test.json.gz").write_bytes(raw)
            rec["assemblage"]["sha256"] = rec["assemblage"]["pins"]["compact_sha256"] = hashlib.sha256(raw).hexdigest()
            (Path(d) / "silicate_slb_test.yaml").write_text(yaml.safe_dump(rec, sort_keys=False), encoding="utf-8")
            got = mr.load(Path(d))                     # not gzip under a .gz name: a named STOP, not a crash
            self.assertEqual(got.id, "material.assemblage_table")
            self.assertIn("gzip", got.evidence["why"])

    def test_tables_read_only(self):
        """68 N3: the registry hands the table out read-only."""
        with tempfile.TemporaryDirectory() as d:
            write(d, table(), status="pinned")
            reg = mr.load(Path(d))
        with self.assertRaises(TypeError):
            reg.tables["silicate_slb_test"]["cells"][0]["rho"] = 1.0

    def test_gate_reruns_on_a_loaded_table(self):
        """68 on 2922f022: check_table and planted_coverage take the table as the registry hands it out (frozen)."""
        with tempfile.TemporaryDirectory() as d:
            write(d, table(), status="pinned")
            reg = mr.load(Path(d))
        rid = "silicate_slb_test"
        ma.check_table(reg[rid]["assemblage"], reg.tables[rid])
        cov = ma.planted_coverage(reg[rid]["assemblage"], reg.tables[rid], per=1)
        self.assertTrue(all(row["missed"] == [] for row in cov.values()))

    def test_b3_stop_reaches_the_registry(self):
        tb = table(); cell(tb, 4, 5)["gamma"] *= 1.1
        with tempfile.TemporaryDirectory() as d:
            write(d, tb, status="pinned")
            got = mr.load(Path(d))
        self.assertEqual(got.id, "material.assemblage_table")
        self.assertIn("differ from the model", got.evidence["why"])


if __name__ == "__main__":
    unittest.main()
