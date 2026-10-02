# 범위는 자기가 묶는 방향으로만 판정하는가 — 도우미 · 음성 대조 · 세 자리(핵 · 암석 · 조석 고정)의 픽스처 (C154)
"""prereg-c154-bound-verdicts: B-helper, B-neg, B-sites (rows 4–6).

    python3 engine/test_bounds.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bounds              # noqa: E402
import core_state as cs    # noqa: E402
import interior            # noqa: E402
import tidal_locking as tl  # noqa: E402

fails: list[str] = []


def ok(cond: bool, label: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        fails.append(label)


def b_helper() -> None:
    v = lambda val, kind: bounds.verdict(val, kind, 10.0, "A", "B", "U")[0]   # noqa: E731
    ok(v(12, "lower") == "A" and v(8, "lower") == "U", "B-helper: a lower bound proves «above» only")
    ok(v(8, "upper") == "B" and v(12, "upper") == "U", "B-helper: an upper bound proves «below» only")
    ok(v(12, "exact") == "A" and v(8, "exact") == "B", "B-helper: an exact value decides both sides")
    why = bounds.verdict(8, "lower", 10.0, "A", "B", "U", name="x")[1]
    ok("lower bound" in why and "x" in why, "B-helper: the undetermined reason names the bound")
    iv = lambda lo, hi: bounds.interval_verdict(lo, hi, 10.0, "A", "B", "U")[0]  # noqa: E731
    ok(iv(11, 12) == "A" and iv(8, 9) == "B" and iv(9, 11) == "U", "B-helper: an interval decides only off the threshold")


def sites() -> dict:
    out = {}
    # row 4 — melt_bracket at 18–20 GPa, bracket 1023–1423 K; 900 K is below both ends
    und = cs.solve(20.0, 18.0, 1000.0, 900.0, core_material="fe_s_13wt_19gpa")
    dec = cs.solve(20.0, 18.0, 800.0, 700.0, core_material="fe_s_13wt_19gpa", core_cmb_temperature=700.0)
    # 900 K declared: the centre's own adiabat reaches ~1052 K, inside the bracket — undecided, where t_top said solid
    dec_mid = cs.solve(20.0, 18.0, 1000.0, 900.0, core_material="fe_s_13wt_19gpa", core_cmb_temperature=900.0)
    out["row4_declared_centre_in_bracket"] = dec_mid.values["conductor_phase"]
    out["row4_undeclared"] = und.values["conductor_phase"]
    out["row4_declared"] = dec.values["conductor_phase"]
    hot = cs.solve(20.0, 18.0, 2500.0, 2400.0, core_material="fe_s_13wt_19gpa")
    out["row4_liquid"] = hot.values["conductor_phase"]
    # row 5 — a rock sample at 150 GPa well below the MgSiO₃ curve; and one at 50 GPa
    from eos import silicate_solidus
    p_hi, p_lo = 150e9, 50e9
    st_hi = SimpleNamespace(rock_samples=[(p_hi, silicate_solidus(p_hi, "peridotitic") - 500.0)])
    st_lo = SimpleNamespace(rock_samples=[(p_lo, silicate_solidus(p_lo, "peridotitic") - 500.0)])
    out["row5_150"] = interior._silicate_melt_verdict(st_hi, 1600.0, "peridotitic")[0]
    out["row5_50"] = interior._silicate_melt_verdict(st_lo, 1600.0, "peridotitic")[0]
    out["row5_basal_150"] = interior._basal_silicate_state(st_hi, "peridotitic")[0]
    out["row5_basal_50"] = interior._basal_silicate_state(st_lo, "peridotitic")[0]
    # row 6 — test_tidal_locking's own straddling case (Venus-like at 50 h)
    strad = tl.solve(0.815, 0.9499, 1.082e8, 332946.0, 50.0, 0.007)
    out["row6_straddle"] = (strad.values["locked"], strad.values["rotation_state"])
    return out


def b_sites(o: dict) -> None:
    ok(o["row4_undeclared"] == cs.CONDUCTOR_UNDECIDED, f"B-sites row 4: undeclared t_top below the bracket → undecided (was solid); got {o['row4_undeclared']}")
    ok(o["row4_declared"] == cs.CONDUCTOR_SOLID, f"B-sites row 4: declared t_top, centre from its own adiabat, below the bracket → solid; got {o['row4_declared']}")
    ok(o["row4_declared_centre_in_bracket"] == cs.CONDUCTOR_UNDECIDED, f"B-sites row 4: declared 900 K, centre adiabat ~1052 K inside the bracket → undecided; got {o['row4_declared_centre_in_bracket']}")
    ok(o["row4_liquid"] == cs.CONDUCTOR_LIQUID, f"B-sites row 4: a lower bound above the bracket → liquid (supported); got {o['row4_liquid']}")
    ok(o["row5_150"] == interior.SILICATE_STATE_UNDECIDED, f"B-sites row 5: rock at 150 GPa below the MgSiO₃ curve → undecided; got {o['row5_150']}")
    ok(o["row5_50"] == interior.SILICATE_STATE_SOLID, f"B-sites row 5: rock at 50 GPa below the solidus → solid (unchanged); got {o['row5_50']}")
    ok(o["row5_basal_150"] == interior.BASAL_UNDECIDED, f"B-sites row 5: basal sample at 150 GPa → undecided; got {o['row5_basal_150']}")
    ok(o["row5_basal_50"] == interior.BASAL_SOLID, f"B-sites row 5: basal sample at 50 GPa → solid (unchanged); got {o['row5_basal_50']}")
    ok(o["row6_straddle"] == (None, tl.STATE_UNDETERMINED), f"B-sites row 6: straddling band → rotation_state undetermined; got {o['row6_straddle']}")


def b_neg() -> None:
    """Every bound treated as exact: today's verdicts must come back, or the fixtures could not see C154."""
    real = bounds.verdict
    bounds.verdict = lambda value, kind, *a, **k: real(value, "exact", *a, **k)
    try:
        o = sites()
    finally:
        bounds.verdict = real
    ok(o["row4_undeclared"] == cs.CONDUCTOR_SOLID, f"B-neg row 4: as exact, the undeclared case is solid again; got {o['row4_undeclared']}")
    ok(o["row5_150"] == interior.SILICATE_STATE_SOLID, f"B-neg row 5: as exact, 150 GPa is solid again; got {o['row5_150']}")
    ok(o["row5_basal_150"] == interior.BASAL_SOLID, f"B-neg row 5 basal: as exact, 150 GPa basal is solid again; got {o['row5_basal_150']}")


if __name__ == "__main__":
    b_helper()
    b_sites(sites())
    b_neg()
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    sys.exit(1 if fails else 0)
