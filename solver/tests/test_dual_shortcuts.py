# s 읽기의 Dual 지름길 시험 — delta 4 §5: 무게의 값과 도함수가 모두 지름길 값일 때만 건너뜀(_at), 값만 보는 변이는 빨강
import math
import unittest
from unittest import mock

from solver import material_assemblage as ma

BSE = "silicate_slb_default_bse"


def _view():
    from solver import material_registry as mr
    from solver.from_v1 import thaw
    reg = mr.load()
    v = ma.view(thaw(reg.get(BSE)), reg.tables[BSE], 1600.0)
    v.s_read = True
    return v


@mock.patch.object(ma, "RHO_BRIDGE", False)
class DualAwareShortcuts(unittest.TestCase):
    """Delta 4 §5 (68, artifacts 0cf53783): a shortcut on a possibly-Dual weight is taken only when its derivatives are 0
    too. At bse x = 22.0342623, T = 2235.6306204 K (exactly on edge 179's window boundary) the value-only zero test dropped
    (1 − H)′·(side value) from ∂s/∂T in a ~1e-8 band of u just inside the window. On this tree (no taper), at
    h = 1e-6 / 1e-8: Dual-aware s 3.89e-8 / 3.89e-10, s8/s6 0.00999 (smooth, ∝ h); the value-only mutant
    (DUAL_AWARE_SHORTCUTS False) s 3.89e-8 / 2.77e-7, s8/s6 7.12 (a step). The form is 91a8e53d's (delta 4 §2). Moved here from test_sread_taper (df6e1ae0, 91a8e53d), whose
    taper does not land."""
    X, T = 22.034261836127737, 2235.630620432312       # exactly on the window boundary at T (the band is ~3e-10 in ln P)

    def _s(self, h):
        v = _view()
        a, b = v._solid(math.exp(self.X), self.T - h), v._solid(math.exp(self.X), self.T + h)
        return abs(b[1] - a[1]) / abs(a[1])

    def test_smooth(self):
        s6, s8 = self._s(1e-6), self._s(1e-8)
        self.assertLess(s8 / s6, 0.1, (s6, s8))           # delta 4 §2's test: not a step (this tree: 0.00999)

    def test_mutant_value_only(self):
        with mock.patch.object(ma, "DUAL_AWARE_SHORTCUTS", False):
            s6, s8 = self._s(1e-6), self._s(1e-8)
            self.assertTrue(0.1 <= s8 / s6 <= 10.0, (s6, s8))   # §2: a step (this tree: 7.12)


if __name__ == "__main__":
    unittest.main()
