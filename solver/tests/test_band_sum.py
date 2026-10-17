# 띠 노트 합 시험 — BandNote 의 c_P 항·분모(scale)와 material_notes 의 필드별 절대 띠 합(등록 reg-interp-term §4·§7.4, 지휘석 10-17 «더한다»)
import types
import unittest

from solver import material_notes as mn, material_view as mv


class _View(mv.RecordView):
    """A record view whose state is planted per (P, T): (ρ, dT/dP, notes)."""
    def __init__(self, states):
        self.material_id = "planted"
        self.record = {"id": "planted", "phases": []}
        self.states = states

    def state(self, p, t, guess_rho=None):
        return self.states[(p, t)]

    def phase_read(self, p, t):
        return "x"


def _note(edge, error=None, dtdp=None, cp=None, scale=None, form="relative"):
    return mv.BandNote("planted", edge, form, error, None, "g", "o", dtdp_error=dtdp, dtdp_origin=None if dtdp is None
                       else "do", c_p_error=cp, c_p_origin=None if cp is None else "co", scale=scale)


def _collect(states):
    nodes = [(0.0, (0.0, p, t, t), 0) for p, t in states]
    body = types.SimpleNamespace(layers=[types.SimpleNamespace(id="L")])
    return mn.collect(body, {"L": _View(states)}, types.SimpleNamespace(profiles={"L": nodes}))


def _sum(notes):
    got = [n for n in notes if n.kind == "material_band_sum"]
    return got[0].fields if got else None


class BandSum(unittest.TestCase):
    def test_terms_add_per_field_in_absolute(self):
        """A relative term without a scale is taken against the read's |value|; one with a scale against the scale."""
        mc = _note("dT/dP model consistency", dtdp=1e-3)
        ri = _note("read interpolation", error=2e-3, dtdp=0.05, cp=0.01, scale=(3000.0, 2e-9, 900.0))
        s = _sum(_collect({(1e9, 1000.0): (3300.0, 1e-8, (mc, ri))}))
        self.assertAlmostEqual(s["dtdp"]["band"], 1e-3 * 1e-8 + 0.05 * 2e-9, delta=1e-24)
        self.assertEqual(list(s["dtdp"]["edges"]), ["dT/dP model consistency", "read interpolation"])
        self.assertNotIn("rho", s)                        # one ρ term only: nothing to add
        self.assertNotIn("c_p", s)

    def test_one_term_per_field_no_sum(self):
        """Control: one band note per field, as every answer before the term, gives no sum note."""
        mc = _note("dT/dP model consistency", dtdp=1e-3)
        fl = _note("p_min floor", error=1e-4)
        self.assertIsNone(_sum(_collect({(1e9, 1000.0): (3300.0, 1e-8, (mc, fl))})))

    def test_absolute_rho_band_is_its_own(self):
        a = _note("γ set past", error=5.0, form="absolute")
        r = _note("read interpolation", error=1e-3, scale=(3000.0, 1e-9, 900.0))
        s = _sum(_collect({(1e9, 1000.0): (3300.0, 1e-8, (a, r))}))
        self.assertAlmostEqual(s["rho"]["band"], 5.0 + 3.0, delta=1e-12)

    def test_c_p_needs_a_scale(self):
        """state carries no c_P: a c_P term without a scale is not summed (it has no absolute value here)."""
        a = _note("e1", cp=0.1)
        b = _note("e2", cp=0.2, scale=(1.0, 1.0, 900.0))
        c = _note("e3", cp=0.3, scale=(1.0, 1.0, 1000.0))
        self.assertIsNone(_sum(_collect({(1e9, 1000.0): (3300.0, 1e-8, (a, b))})))
        s = _sum(_collect({(1e9, 1000.0): (3300.0, 1e-8, (a, b, c))}))
        self.assertAlmostEqual(s["c_p"]["band"], 0.2 * 900.0 + 0.3 * 1000.0, delta=1e-9)

    def test_largest_node_and_where(self):
        lo = (_note("a", dtdp=1e-3), _note("b", dtdp=0.1, scale=(1.0, 1e-9, 1.0)))
        hi = (_note("a", dtdp=1e-3), _note("b", dtdp=0.9, scale=(1.0, 1e-9, 1.0)))
        s = _sum(_collect({(1e9, 1000.0): (3300.0, 1e-8, lo), (2e9, 1100.0): (3300.0, 1e-8, hi),
                           (3e9, 1200.0): (3300.0, 1e-8, lo)}))
        self.assertEqual((s["dtdp"]["p_at_max"], s["dtdp"]["t_at_max"]), (2e9, 1100.0))
        self.assertAlmostEqual(s["dtdp"]["band"], 1e-11 + 0.9e-9, delta=1e-24)

    def test_c_p_error_on_the_band_note(self):
        """material_band carries c_p_error and its origin when a note holds one, and no such key otherwise."""
        got = _collect({(1e9, 1000.0): (3300.0, 1e-8, (_note("ri", error=1e-3, cp=0.02, scale=(1.0, 1.0, 1.0)),
                                                         _note("mc", dtdp=1e-3)))})
        band = {n.fields["edge"]: n.fields for n in got if n.kind == "material_band"}
        self.assertEqual((band["ri"]["c_p_error"], band["ri"]["c_p_origin"]), (0.02, "co"))
        self.assertNotIn("c_p_error", band["mc"])

    def test_defaults_keep_old_notes(self):
        n = mv.BandNote("m", "e", "relative", 1e-3, None, "g", "o")
        self.assertEqual((n.c_p_error, n.c_p_origin, n.scale), (None, None, None))


if __name__ == "__main__":
    unittest.main()
