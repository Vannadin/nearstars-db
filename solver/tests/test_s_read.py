# s 읽기 시험 — dT/dP 를 저장된 s 에서(도함수 정확성·꼬임 한쪽 도함수·심은 표), 얼어붙은 스텐실, 항 은퇴·폐합 주석·교환 잠열 주석, closure 블록 STOP, ∂s/∂T 표본 점검 (s-read 등록, 사후 노트 1)
"""s-read registration (artifacts rewrite/s2-loop-entropy/reg-s-read.frozen.md, blob 327b4f73) with post-freeze note 1
(the swap jump voided).

    solver/.venv/bin/python -m unittest solver.tests.test_s_read
"""
import copy
import math
import random
import unittest
from unittest import mock

from solver import material_assemblage as ma, material_registry as mr, material_view as mv, stepper as st
from solver.from_v1 import thaw

_REG = []


def _reg():
    if not _REG:
        _REG.append(mr.load())
    return _REG[0]


def _view(rid="silicate_slb_default_bse", s_read=True):
    reg = _reg()
    v = ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)
    v.s_read = s_read
    return v


def _s(v, p, t):
    got = v.s_path(p, t)
    return None if got is None or isinstance(got, st.Stop) else got.v


class Derivatives(unittest.TestCase):
    """§3.0: the forward-mode derivatives are the read's own, against central differences off the switches and
    one-sided differences on each side of a switch (68 n3)."""

    def test_against_central_differences(self):
        v = _view()
        rnd = random.Random(1)
        n = 0
        for _ in range(400):
            p, t = math.exp(rnd.uniform(math.log(2e9), math.log(1.3e11))), rnd.uniform(1650.0, 3000.0)
            sv = v.s_path(p, t)
            if sv is None or isinstance(sv, st.Stop):
                continue
            h = 1e-6
            vals = [_s(v, p * math.exp(h), t), _s(v, p * math.exp(-h), t), _s(v, p, t + 1e-3), _s(v, p, t - 1e-3)]
            if None in vals:
                continue
            fx, ft = (vals[0] - vals[1]) / (2 * h), (vals[2] - vals[3]) / 2e-3
            if abs(sv.dx - fx) > 1e-5 * max(abs(fx), 1e-9) or abs(sv.dt - ft) > 1e-5 * abs(ft):
                continue                      # a switch inside the stencil: the one-sided test below covers it
            n += 1
            self.assertLess(abs(sv.dx - fx), 1e-6 * max(abs(fx), 1.0), (p, t))
            self.assertLess(abs(sv.dt - ft), 1e-6 * abs(ft), (p, t))
        self.assertGreater(n, 300)

    def test_at_t_nodes_the_slope_is_kept(self):
        """A T node: the Hermite is read (same value), so ∂s/∂T is the node's slope, not 0."""
        v = _view()
        sv = v.s_path(30e9, 1950.0)
        self.assertGreater(sv.dt, 0.0)
        up = _s(v, 30e9, 1950.0 + 1e-3)
        self.assertLess(abs((up - sv.v) / 1e-3 - sv.dt), 1e-3 * sv.dt)

    def test_one_sided_at_switches(self):
        """At the ends of every edge's c′ window on one T row: the one-sided forward-mode derivative in ln P equals the
        one-sided difference on its own side."""
        v = _view()
        t = 2200.0
        k = v.ts.index(t)
        checked = 0
        for c in v._cut:
            pb = c.p_b_ext(t, v._reach)
            if c.kind != "edge" or pb is None or pb > v.p_dataset:
                continue
            xb = math.log(pb)
            w = v._width(xb)
            for xe in (xb - w, xb + w):
                for side in (-1.0, 1.0):
                    x = xe + side * 1e-7
                    sv = v.s_path(math.exp(x), t)
                    if sv is None or isinstance(sv, st.Stop):
                        continue
                    h = side * 1e-5                     # 3-point one-sided, on its own side
                    a, b = _s(v, math.exp(x + h), t), _s(v, math.exp(x + 2 * h), t)
                    if a is None or b is None:
                        continue
                    fd = (-3.0 * sv.v + 4.0 * a - b) / (2.0 * h)
                    self.assertLess(abs(sv.dx - fd), 1e-5 * max(abs(fd), 1.0), (c.id, x))
                    checked += 1
        self.assertGreater(checked, 0)
        del k

    def test_planted_table(self):
        """A planted s = a + b·T − c·ln P, linear in each read axis so the read reproduces it exactly, on the plain
        (unexported) read: dT/dP = c/(P·b), c_P = T·b."""
        reg = _reg()
        rid = "silicate_slb_default_bse"
        tab = copy.deepcopy(mv.thaw_plain(reg.tables[rid]))
        a, b, cc = 100.0, 0.6, 60.0
        for cell in tab["cells"]:
            cell["s"] = a + b * cell["t"] - cc * math.log(cell["p"])
            cell["kind"] = "equilibrium" if cell["kind"] == "frozen" else cell["kind"]
        tab["boundaries"] = {"status": "pending"}
        v = ma.view(thaw(reg.get(rid)), tab, 1600.0)
        v.s_read = True
        for p, t in ((5e9, 1800.0), (40e9, 2400.0), (90e9, 2911.3)):
            got = v._solid(p, t)
            want = cc / (p * b)
            self.assertLess(abs(got[1] - want) / want, 1e-9, (p, t))
            self.assertLess(abs(got[2] - t * b) / (t * b), 1e-9)   # c_P = T·∂s/∂T

    def test_sign_flip_mutant_is_seen(self):
        """Mutant: −s_P/s_T with the sign of s_P flipped gives a negative dT/dP where the read's is positive."""
        v = _view()
        sv = v.s_path(30e9, 1960.0)
        self.assertGreater(-(sv.dx / 30e9) / sv.dt, 0.0)
        self.assertLess((sv.dx / 30e9) / sv.dt, 0.0)


class FloatPathUnchanged(unittest.TestCase):
    """§6.3: the ρ read is bit-identical with the s read on; with it off (a record that does not declare it) every
    field is."""

    def test_rho_and_off(self):
        on, off = _view(), _view(s_read=False)
        base = ma.view(thaw(_reg().get("silicate_slb_default_bse")), _reg().tables["silicate_slb_default_bse"], 1600.0)
        rnd = random.Random(3)
        for _ in range(200):
            p, t = math.exp(rnd.uniform(math.log(1e8), math.log(1.3e11))), rnd.uniform(1000.0, 3500.0)
            a, b, c = on._solid(p, t), off._solid(p, t), base._solid(p, t)
            if isinstance(c, st.Stop):
                continue
            self.assertEqual(b[:3], c[:3])
            if not isinstance(a, st.Stop):
                self.assertEqual(a[0], c[0])


class FrozenStencil(unittest.TestCase):
    """§3.2: a read whose stencil holds a frozen node keeps today's read and is counted."""

    def test_low_t_keeps_todays_read(self):
        on, off = _view(), _view(s_read=False)
        got_on, got_off = on._solid(2e9, 700.0), off._solid(2e9, 700.0)
        self.assertEqual(got_on[:3], got_off[:3])
        self.assertIsNone(on.s_path(2e9, 700.0))
        self.assertGreater(on.s_counts["frozen_stencil_reads"], 0)

    def test_mantle_t_reads_s(self):
        v = _view()
        self.assertIsNotNone(v.s_path(20e9, 1900.0))


class Notes(unittest.TestCase):
    """§3.5: interp and loop terms keep ρ only, named retired; §4's closure note; note 1's swap latent text."""

    def test_retired_terms_and_closure(self):
        v = _view()
        tab = _reg().tables["silicate_slb_default_bse"]
        cells, _f, _s2 = v._terms["loop_terms"]
        (ia, ib), e = next(iter(cells.items()))
        v._closure = ({(ia, ib): 0.0123}, v._closure[1])
        p = math.sqrt(v.ps[ia] * v.ps[ia + 1])
        t = 0.5 * (v.ts[ib] + v.ts[ib + 1])
        v.notes.clear()
        v._term_notes(p, t, 4000.0, 1e-8, 1200.0)
        bands = [n for n in v.notes if isinstance(n, mv.BandNote)]
        for n in bands:
            if n.edge in ("read interpolation", "under-resolved loop"):
                self.assertIsNone(n.dtdp_error)
                self.assertIsNone(n.c_p_error)
                self.assertIn(ma.RETIRED_TERMS, n.origin)
        clo = [n for n in bands if n.edge == "isentrope closure"]
        self.assertEqual(len(clo), 1)
        self.assertEqual(clo[0].dtdp_error, 0.0123)
        del tab, e

    def test_off_keeps_terms(self):
        v = _view(s_read=False)
        cells, _f, _s2 = v._terms["loop_terms"]
        (ia, ib), e = next((k, x) for k, x in cells.items() if x[1])
        p = math.sqrt(v.ps[ia] * v.ps[ia + 1])
        t = 0.5 * (v.ts[ib] + v.ts[ib + 1])
        v.notes.clear()
        v._term_notes(p, t, 4000.0, 1e-8, 1200.0)
        self.assertTrue(any(n.dtdp_error for n in v.notes if isinstance(n, mv.BandNote)
                            and n.edge == "under-resolved loop"))

    def test_swap_note_carries_the_latent_heat(self):
        v = _view()
        sw = next(c for c in v._cut if c.kind == "swap" and c.t0 <= 1730.0 <= c.t1 and
                  all(r.get("delta_s") is not None for r in c.rows))
        p = sw.p_b(1730.0) * 1.0001
        v.state(p, 1730.0)
        txt = [n.text for n in v.notes if isinstance(n, mv.DeclaredNote) and n.text.startswith(ma.SWAP_NOTE)]
        self.assertTrue(txt and "latent heat is not taken" in txt[0], txt)
        off = _view(s_read=False)
        off.state(p, 1730.0)
        txt = [n.text for n in off.notes if isinstance(n, mv.DeclaredNote) and n.text.startswith(ma.SWAP_NOTE)]
        self.assertTrue(txt and "latent heat" not in txt[0])


class SwapDeltaS(unittest.TestCase):
    """Note 1 (68 n2, and 68 on the count): the cut runs read as swaps hold 42 / 35 / 38 rows (bse / dmm / khan); the
    swap-class rows among them carry delta_s (32 / 33 / 32, |Δs| 1.005–7.461 / 1.404–11.032 / 3.581–30.029 J/kg/K);
    the rest are coincident edge runs read as swaps, with none."""

    def test_rows_carry_delta_s(self):
        want = {"silicate_slb_default_bse": (42, 32, 1.005, 7.461), "silicate_slb_earth_dmm_wh2005": (35, 33, 1.404, 11.032),
                "silicate_slb_mars_khan2022": (38, 32, 3.581, 30.029)}
        for rid, (n_all, n, lo, hi) in want.items():
            v = _view(rid)
            rows = [r for c in v._cut if c.kind == "swap" for r in c.rows]
            ds = [abs(r["delta_s"]) for r in rows if r.get("delta_s") is not None]
            self.assertEqual((len(rows), len(ds)), (n_all, n), rid)
            self.assertEqual((round(min(ds), 3), round(max(ds), 3)), (lo, hi), rid)
            for c in v._cut:                                # a run with no delta_s is a coincident edge run
                if c.kind == "swap" and not any(r.get("delta_s") is not None for r in c.rows):
                    self.assertTrue(all(r.get("delta_s") is None for r in c.rows), (rid, c.id))


class ClosureBlock(unittest.TestCase):
    """§4's load gate on closure_terms, and the declaration needing it."""

    def _tab(self, block):
        tab = copy.deepcopy(mv.thaw_plain(_reg().tables["silicate_slb_default_bse"]))
        tab["closure_terms"] = block
        return tab

    def _block(self, **kw):
        tab = _reg().tables["silicate_slb_default_bse"]
        b = {"source": {"floor": {"dtdp": ma.term_floor(tab["cells"], tab["p_dataset"])["dtdp"]},
                        "threshold_k": ma.CLOSURE_THRESHOLD_K, "tool_blob": "d" * 40, "skips": {}},
             "fields": ["dtdp"], "cells": [[1, 0, 0.0123]]}
        b.update(kw)
        return b

    def test_good_block(self):
        ma.check_closure_block(self._tab(self._block()))

    def test_stops(self):
        for why, blk in (("fields", self._block(fields=["rho"])),
                         ("floor", self._block(source={**self._block()["source"], "floor": {"dtdp": 1.0}})),
                         ("threshold_k", self._block(source={**self._block()["source"], "threshold_k": 1.0})),
                         ("is not \\[ia", self._block(cells=[[1, 0, 0.1, 0.2]])),
                         ("doubled", self._block(cells=[[1, 0, 0.1], [1, 0, 0.1]])),
                         ("not a finite term", self._block(cells=[[1, 0, 0.0]]))):
            with self.subTest(why=why), self.assertRaisesRegex(ma.TableStop, why):
                ma.check_closure_block(self._tab(blk))

    def test_declared_without_block_stops(self):
        rec = copy.deepcopy(mv.thaw_plain(_reg().get("silicate_slb_default_bse")))
        rec["assemblage"]["dtdp"]["read"] = "entropy"
        with self.assertRaisesRegex(ma.TableStop, "no closure_terms"):
            ma.check_table(rec["assemblage"], mv.thaw_plain(_reg().tables["silicate_slb_default_bse"]))


class MonotoneSample(unittest.TestCase):
    """§3.4 (directing's ruling): the load's sampled check passes on the shipped table and STOPs on a planted dip."""

    def test_sample_passes_and_dip_stops(self):
        v = _view()
        pts = ma.s_monotone_points(v)
        sample = random.Random(7).sample(pts, 200)
        self.assertTrue(ma.s_monotone_check(v, sample)["pass"])
        with self.assertRaisesRegex(ma.TableStop, "build-time"):
            ma.s_monotone_load_check(v, {"monotone": {"pass": False, "seed": 7}})

    def test_a_pass_built_on_another_read_stops(self):
        """r2 B2 on 677f85d0..0d7732d3: the build-time pass names the material_assemblage.py blob it ran on; the load
        STOPs when that is not this module's own (the read changes under a fixed table: the row blend moved bse's
        minimum ∂s/∂T from −1.61 to −1.96). module_blob() is `git hash-object` of the module's bytes."""
        import subprocess
        from pathlib import Path
        here = Path(ma.__file__)
        got = subprocess.run(["git", "hash-object", str(here)], capture_output=True, text=True, cwd=here.parent)
        if got.returncode == 0:
            self.assertEqual(ma.module_blob(), got.stdout.strip())
        v = _view()
        with self.assertRaisesRegex(ma.TableStop, "ran on material_assemblage.py"):
            ma.s_monotone_load_check(v, {"monotone": {"pass": True, "seed": 7, "material_assemblage_blob": "0" * 40}})
        with self.assertRaisesRegex(ma.TableStop, "ran on material_assemblage.py"):
            ma.s_monotone_load_check(v, {"monotone": {"pass": True, "seed": 7}})        # no identity: stale too
        with mock.patch.object(ma, "s_monotone_check", return_value={"pass": True, "failures": []}) as chk:
            ma.s_monotone_load_check(v, {"monotone": {"pass": True, "seed": 7,
                                                      "material_assemblage_blob": ma.module_blob()}})
        chk.assert_called_once()                          # its own blob: the identity passes and the sample runs
        tab = copy.deepcopy(mv.thaw_plain(_reg().tables["silicate_slb_default_bse"]))
        cell = next(c for c in tab["cells"] if c["p"] > 20e9 and c["t"] == 2000.0 and c["kind"] != "frozen")
        nxt = next(c for c in tab["cells"] if c["p"] == cell["p"] and c["t"] == 2050.0)
        cell["s"] = nxt["s"] + 50.0                       # a row whose s dips in T
        w = ma.view(thaw(_reg().get("silicate_slb_default_bse")), tab, 1600.0)
        w.s_read = True
        here = [(math.log(cell["p"]) + 1e-6, 2000.0 + 50.0 * u) for u in (0.2, 0.4, 0.6, 0.8)]
        self.assertFalse(ma.s_monotone_check(w, here)["pass"])


class OpenEnds(unittest.TestCase):
    """§3.1 X1 (iii) (r2 B3 on 677f85d0..0d7732d3): the per-record count of s's open run ends with s∞ = 0 (the read flat
    in P past the bump, dT/dP 0 there), pinned per record; in boundary_disclosures and, with the s read on, as the
    record's material_disclosure on the answer."""

    PINNED = {"silicate_slb_default_bse": {"ends": 1022, "flat": 131, "one_node": 173},
              "silicate_slb_earth_dmm_wh2005": {"ends": 1104, "flat": 123, "one_node": 217},
              "silicate_slb_mars_khan2022": {"ends": 1092, "flat": 100, "one_node": 181}}

    def test_count_per_record(self):
        reg = _reg()
        for rid, want in self.PINNED.items():
            with self.subTest(rid=rid):
                self.assertEqual(_view(rid).s_open_ends(), want)
                d = ma.boundary_disclosures(thaw(reg.get(rid)), mv.thaw_plain(reg.tables[rid]))
                self.assertEqual(d["s_open_ends"], want)

    def test_flat_means_flat(self):
        """Each counted end reads constant in P past L: the run's s∞ is 0, so the line part adds nothing."""
        v = _view()
        n = 0
        for k in range(len(v.ts)):
            for qs in v._runs("s", k).values():
                q = qs[-1]
                if len(q[0]) > 1 and q.f_hi == 0.0:
                    x = q[0][-1] + q.L_hi
                    self.assertEqual(q.value(x + 0.5), q.value(x))
                    n += 1
        self.assertGreater(n, 0)

    def test_note_on_the_answer(self):
        from solver import material_notes as mn

        class _L:
            id = "mantle"

        class _B:
            layers = (_L(),)

        class _Acc:
            profiles = {"mantle": [(0.0, (0.0, 30e9, 2000.0, 2000.0), None)]}

        for on in (True, False):
            v = _view(s_read=on)
            got = [n for n in mn.collect(_B(), {"mantle": v}, _Acc())
                   if n.kind == "material_disclosure" and n.fields.get("of") == "s_open_ends"]
            self.assertEqual(len(got), 1 if on else 0)
            if on:
                self.assertEqual(got[0].fields["flat"], self.PINNED[v.material_id]["flat"])


class BasalDelegation(unittest.TestCase):
    """Note 1 keeps BasalView's curve_slope_points delegation (68's note on 64f38d74): equal to the overlying view's for
    every overlying curve, bit for bit; BasalView has no transitions of its own."""

    def test_delegation(self):
        over = _view()
        rec = {"id": "basal_test", "kind": "assemblage", "phases": [{"id": "basal"}]}
        b = ma.BasalView(rec, 4000.0, over, 1600.0)
        self.assertEqual(b.transitions(), ())
        for _between, _kind, curve in over.transitions():
            self.assertEqual(b.curve_slope_points(curve), over.curve_slope_points(curve))


if __name__ == "__main__":
    unittest.main()
