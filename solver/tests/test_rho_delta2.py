# 계단 가진 스왑의 λ 시험 — rev3d 수정안 2 delta 2 의 P12 와 그 변이 (khan 1100 K 한 줄 스왑)
"""rev3d amendment 2 delta 2 (68, artifacts a56d8326): a cut swap owning a holding-row step lands with its own λ
(_row_step_lambdas), as its step does. P12 (§4): khan's one-row swaps 117 / 118 at 1100 K, the repaired ρ C⁰ in T at
x_s ± 1e-4 within 1e-9·ρ (S_17..S_19 as F13-A built them on the F13 records, a literal fixture installed as the view's
_fall_sets); mutant SWAP_STEP_LAMBDA False (every cut swap always lands) red. P10 stays in test_rho_rev3d."""
import math
import unittest
from unittest import mock

from solver import material_assemblage as ma

KHAN = "silicate_slb_mars_khan2022"
H_SETS = {17: [[23.935511244634238, 23.938354614172734], [23.96528401110338, 24.014119487816476]],
          18: [[23.935511244634238, 23.938354614172734]],
          19: [[23.935521502708813, 23.93832383994901]]}
H_T, H_XS = 1100.0, 23.936222


def _view(rid, s_read=True):
    from solver import material_registry as mr
    from solver.from_v1 import thaw
    reg = mr.load()
    v = ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)
    v.s_read = s_read
    return v


class StepOwningSwap(unittest.TestCase):
    def _jump(self):
        v = _view(KHAN, s_read=False)
        v._fall_sets = {k: [tuple(iv) for iv in ivs] for k, ivs in H_SETS.items()}
        out = 0.0
        for dx in (-1e-4, 1e-4):
            x = math.exp(H_XS + dx)
            at = v._solid(x, H_T)[0]
            for d in (-1e-7, -1e-12, 1e-12, 1e-7):
                out = max(out, abs(v._solid(x, H_T + d)[0] - at) / at)
        return out

    def test_p12_c0_in_t(self):
        with mock.patch.object(ma, "RHO_BRIDGE", True):
            self.assertLessEqual(self._jump(), 1e-9)

    def test_mutant_swap_always_lands(self):
        with mock.patch.object(ma, "RHO_BRIDGE", True), mock.patch.object(ma, "SWAP_STEP_LAMBDA", False):
            self.assertGreater(self._jump(), 1e-6)


if __name__ == "__main__":
    unittest.main()
