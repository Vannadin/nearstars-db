# 정의역·한계 레코드 자기검증 — 거절이 양쪽으로 발화하는가, 전개점 아래는 note 인가, 앵커 구절이 원문에 있는가 (Brief 155)
"""Hold `domain.py` and its first two consumers to what they claim.

    python3 engine/test_domain.py

1. Domain — inside passes, outside is a NAMED refusal, an edge of None is open, no anchor is refused.
   Below the expansion point is a note, not a refusal, and only when an expansion point is declared.
2. eqs 34–36 (`mantle_flux.implied_flux`) — the callee refuses at 4900 K; passes at 1600 K with no note;
   passes at 1400 K WITH the extrapolation note (Brief 57's band machinery lives there); the inversion
   bracket still refuses by name below 1000 K and above 2500 K — the five Brief 57 anchors are untouched.
3. eqs 37–39 (`cmb_flux.bottom_layer`) — refuses when T_a > 4800 K; Earth's present state (4161, 2694)
   passes with no note; a Mars-shaped deep mantle (T_c 2500, T̃_m 1910) passes WITH the note.
4. `core_history` — an initial mantle temperature of 5000 K ends as `out-of-domain` naming the law;
   the shipped Earth start (4800 / 3040) is inside and integrates.
5. Anchors — every `file@«phrase»` in the two Domain records resolves in the cache text layer when the
   gitignored cache is present; absent, the check is reported as skipped, not passed.
6. Limit — the operator is generated from the word: a floor holds above, a ceiling below; a bad word,
   a one-ended width and a missing anchor are refused at construction.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import cmb_flux as cf
import core_history as ch
import mantle_flux as mf
from domain import DOMAIN_REFUSED, Domain, Limit

CACHE = Path(__file__).resolve().parents[1] / "docs" / "phase3" / "_papers"


def main() -> int:
    fails: list[str] = []
    skipped: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    def refused(fn, *a, **k) -> bool:
        try:
            fn(*a, **k)
            return False
        except ValueError:
            return True

    # ── 1. Domain record ─────────────────────────────────────────────────────
    d = Domain("x [K]", lo=None, hi=10.0, anchor="a.txt@«p»", expansion=5.0)
    ok(d.in_domain(-1e9) and d.in_domain(10.0) and not d.in_domain(10.0001), "1: open below, closed at hi")
    ok(d.refusal(10.5) is not None and d.refusal(10.5).startswith(DOMAIN_REFUSED) and "above" in d.refusal(10.5),
       "1: outside → a named refusal saying which side")
    ok(d.refusal(3.0) is None and d.extrapolation_note(3.0) is not None and "2 K below" in d.extrapolation_note(3.0),
       f"1: below the expansion point → note, not refusal; got {d.extrapolation_note(3.0)}")
    ok(d.extrapolation_note(7.0) is None, "1: above the expansion point → no note")
    ok(Domain("y", lo=1.0, hi=2.0, anchor="a@«p»").extrapolation_note(1.5) is None, "1: no expansion point → never a note")
    ok(refused(Domain, "z", None, None, "a@«p»"), "1: a domain with no edge declares nothing → refused")
    ok(refused(Domain, "z", 2.0, 1.0, "a@«p»"), "1: lo above hi → refused")
    ok(refused(Domain, "z", 1.0, 2.0, "no anchor"), "1: an anchor that is not file@«phrase» → refused")

    # ── 2. eqs 34–36 ────────────────────────────────────────────────────────
    hot = mf.implied_flux(4900.0, 9.8, 6.4e6)
    ok(hot["q_m_w"] is None and hot["domain_refusal"] and DOMAIN_REFUSED in hot["domain_refusal"]
       and "4800" in hot["domain_refusal"],
       f"2: 4900 K must be refused by the callee naming the 4800 K edge, got {hot['domain_refusal']}")
    edge = mf.implied_flux(4800.0, 9.8, 6.4e6)
    ok(edge["domain_refusal"] is None and edge["q_m_w"] is not None, "2: the printed edge itself is inside")
    earth = mf.implied_flux(1600.0, 9.8, 6.4e6)
    ok(earth["domain_refusal"] is None and earth["extrapolation_note"] is None,
       f"2: Earth's declared 1600 K passes with no note (above T_0 = 1573), got {earth['extrapolation_note']}")
    cold = mf.implied_flux(1400.0, 9.8, 6.4e6)
    ok(cold["domain_refusal"] is None and cold["q_m_w"] is not None and cold["extrapolation_note"]
       and "173 K below" in cold["extrapolation_note"],
       f"2: 1400 K passes WITH the extrapolation note (173 K under T_0), got {cold['extrapolation_note']}")
    ok(mf.INVERSION_BRACKET_K == (1000.0, 2500.0) and not hasattr(mf, "BRACKET_K"),
       "2: the bisection bracket is named as what it is, and the old name is gone")
    ok(mf.EQ35_DOMAIN.lo is None and mf.EQ35_DOMAIN.hi == 4800.0 and mf.EQ35_DOMAIN.expansion == mf.T_0,
       "2: eqs 34–36's domain: open below, 4800 K above, expansion point T_0")
    ok(mf.invert_for_flow(0.10e12, 1.8, 1.82e6) is None and mf.invert_for_flow(1e20, 9.8, 6.4e6) is None,
       "2: the inversion still refuses by name outside its own bracket")
    ok(abs(mf.invert_for_flow(14.81e12, 9.8, 6.4e6) - 1379.3) < 1.0, "2: Brief 57's 1379 K inversion is untouched")
    c = mf.consistency(4900.0, 21.3e12, 9.8, 6.4e6)
    ok(c["verdict"] == mf.NO_DOMAIN and c["q_m_w"] is None, f"2: consistency at 4900 K → {mf.NO_DOMAIN!r}, got {c['verdict']}")
    ok(mf.consistency(1400.0, 21.3e12, 9.8, 6.4e6)["verdict"] == mf.TOO_COLD, "2: 1400 K still flags TOO_COLD (a note, not a refusal)")

    # ── 3. eqs 37–39 ────────────────────────────────────────────────────────
    hot_b = cf.bottom_layer(4900.0, 4800.0, 3.48e6)          # T_a = 4850
    ok(hot_b["q_c_w"] is None and hot_b["domain_refusal"] and "4800" in hot_b["domain_refusal"],
       f"3: T_a 4850 K must be refused naming 4800, got {hot_b['domain_refusal']}")
    ok(cf.bottom_layer(4800.0, 4800.0 - 1e-6, 3.48e6)["domain_refusal"] is None, "3: T_a at the printed edge is inside")
    present = cf.bottom_layer(4161.0, 2694.0, 3.48e6)       # T_a 3427.5
    ok(present["domain_refusal"] is None and present["extrapolation_note"] is None,
       f"3: Earth's present T_a 3428 K passes with no note (above T_1 = 3400), got {present['extrapolation_note']}")
    mars = cf.bottom_layer(2500.0, 1910.0, 1.83e6)          # T_a 2205
    ok(mars["domain_refusal"] is None and mars["q_c_w"] is not None and mars["extrapolation_note"]
       and "1195 K below" in mars["extrapolation_note"],
       f"3: a Mars-shaped deep mantle passes WITH the note (1195 K under T_1), got {mars['extrapolation_note']}")
    ok(cf.EQ39_DOMAIN.lo is None and cf.EQ39_DOMAIN.hi == 4800.0 and cf.EQ39_DOMAIN.expansion == cf.T_1,
       "3: eqs 37–39's domain: open below, 4800 K above, expansion point T_1 — its first declaration")

    # ── 4. core_history refuses by name from an out-of-domain start ────────
    from interior import solve as interior_solve
    v = interior_solve(1.0, core_mass_fraction=0.325, potential_temperature=1600.0).values
    args = (1.0, 0.325, v["core_radius"], v["cmb_pressure"], v["cmb_temperature"], 1600.0, 1.0, 4.54)
    r_hot = ch.solve(*args, 4800.0, 5000.0)
    ok(r_hot.regime == "out-of-domain" and DOMAIN_REFUSED in r_hot.reason and "eqs 34–36" in r_hot.reason,
       f"4: T_m0 5000 K → out-of-domain naming eqs 34–36, got {r_hot.regime}: {r_hot.reason[:120]}")
    r_hot_c = ch.solve(*args, 5200.0, 3040.0)
    ok(r_hot_c.regime == "out-of-domain" and "eqs 37–39" in r_hot_c.reason,
       f"4: T_c0 5200 K (T_a > 4800 at the start) → out-of-domain naming eqs 37–39, got {r_hot_c.reason[:120]}")
    # the shipped Earth start is inside both domains — asserted through solve(), which test_core_history already anchors
    r_earth = ch.solve(*args, 4800.0, 3040.0)
    ok(r_earth.regime != "out-of-domain", f"4: Earth's shipped start (4800 / 3040) integrates, got {r_earth.regime}")
    ok(any("extrapolat" in n for n in r_earth.notes),
       "4: Earth's history carries the extrapolation count note (its early T_m is below T_0 on no step, its late T_a is below T_1)")

    # ── 5. anchors resolve in the cache text layer ──────────────────────────
    txt = CACHE / mf.NIMMO_TXT
    if txt.exists():
        body = txt.read_text()
        for rec in (mf.EQ35_DOMAIN, cf.EQ39_DOMAIN):
            for phrase in re.findall(rf"{re.escape(mf.NIMMO_TXT)}@«([^»]+)»", rec.anchor + " " + rec.caveat):
                ok(body.count(phrase) >= 1, f"5: anchor phrase not in {mf.NIMMO_TXT}: «{phrase}»")
    else:
        skipped.append(f"5: {mf.NIMMO_TXT} not in the gitignored cache — anchor phrases not checked here")

    # ── 6. Limit ─────────────────────────────────────────────────────────────
    fl = Limit(0.09, "floor", "doc@«0.09»")
    ce = Limit(0.030, "ceiling", "doc@«10–30»", low=0.010, high=0.030)
    ok(fl.holds(0.1) and not fl.holds(0.08) and fl.holds(0.09), "6: a floor holds at and above its value")
    ok(ce.holds(0.02) and ce.holds(0.030) and not ce.holds(0.031), "6: a ceiling holds at and below its value")
    ok(Limit(4.0, "upper", "d@«x»").kind == "domain-edge" and fl.kind == "label", "6: floor/ceiling are labels, lower/upper are domain edges")
    ok(refused(Limit, 1.0, "top", "d@«x»"), "6: an unknown direction word is refused")
    ok(refused(Limit, 1.0, "floor", "d@«x»", low=0.5), "6: a one-ended width is refused")
    ok(refused(Limit, 1.0, "floor", ""), "6: a limit without an anchor is refused")
    ok(refused(Limit, 5.0, "floor", "d@«x»", low=1.0, high=2.0), "6: a value outside its own width is refused")

    for f in fails:
        print(f"  [FAIL] {f}")
    for s in skipped:
        print(f"  [SKIP] {s}")
    if not fails:
        print("  [PASS] 정의역·한계 — eqs 34–36 · 37–39 위끝 4800 K 거절 발화 · 전개점 아래는 note · 브리프 57 앵커 5 유지 · "
              f"core_history 5000 K 시작 거절 · Limit 부호는 단어에서 · 앵커 {'확인' if not skipped else '캐시 없음(건너뜀)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
