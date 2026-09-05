# 조석 가열 앵커 — 이오 밴드 재현·판도라 보드 45 W/m² 재현·×Io 규약·라벨 표·입력 부재 거절 (C30)
"""Anchor the fixed-Q tidal-heating recipe on what the document prints.

    python3 engine/test_tidal_heating.py

1. Io (tidal-heating-methodology.md@«**Io (the calibration).** `M_p = M_Jupiter`, `R = 1822 km`, `a = 421,700 km`» inputs: a 421,700 km, e 0.0041, k₂/Q 0.015, R 1822 km, M_p = M_J 1.89813e27): Ė inside the printed
   observed band ~0.6–1.6e14 W (tidal-heating-methodology.md@«| **Io** | Jupiter | ~5.9 R_J | ~0.0041 | ~0.6–1.6 ×10¹⁴ W») and P_orb 1.769 d. A band, not a point — the doc itself says "~10¹⁴ W".
2. Pandora (board inputs a 252,393 km · e 0.005 · k₂/Q 0.0016 · M_p 120 M⊕ · R 5724 km): F 45.34 W/m², the board's 45
   within 0.75 %; ×Io 187 on the printed 1e14 W denominator; regime "vigorous …"; total-flux mode "heat pipe".
3. ×Io convention: the doc's Dante rows (:451/:453) scale as R⁵ in the ×Io column and R³ in W/m² — output ratio, not flux.
4. Labels: the four §6.1 rows + the unclassified decade; the three §6.2 modes + the gap between 0.14 and 2.5 W/m².
5. Refusals by name: no orbit, no k₂/Q, no radius; mode without any heat source.
"""
from __future__ import annotations

import math
import sys

import tidal_heating as th

M_JUP_KG = 1.89813e27   # IAU 2015 B3 nominal


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # 1. Io band
    p_io, f_io, n_io = th.tidal_power(0.015, M_JUP_KG, 1822e3, 421_700e3, 0.0041)
    ok(0.6e14 <= p_io <= 1.6e14, f"1: Io Ė {p_io:.3e} W outside the doc's observed band 0.6–1.6e14")
    ok(abs(2 * math.pi / n_io / 86400 - 1.769) < 0.002, f"1: Io P_orb {2 * math.pi / n_io / 86400:.4f} d, expected 1.769")
    ok(abs(p_io - 9.343e13) / 9.343e13 < 1e-3, f"1: Io Ė {p_io:.4e} W should reproduce the parallel seat's 9.343e13")
    # 2. Pandora
    pan = th.solve(0.6447, 5724e3 / th.R_EARTH_M, 252_393, 120.0, 0.005, 0.0016)   # a in km, the declared key
    ok(pan.applicable and abs(pan.values["surface_flux"] / 45.0 - 1.0) < 0.0075,
       f"2: Pandora F {pan.values.get('surface_flux')} W/m² vs board 45 (tol 0.75 %)")
    ok(pan.applicable and abs(pan.values["surface_flux"] - 45.337) < 0.01, f"2: Pandora F should be 45.337 W/m² (tidal_check), got {pan.values.get('surface_flux')}")
    ok(pan.applicable and abs(pan.values["io_power_ratio"] - 186.7) < 0.2, f"2: Pandora ×Io(output) {pan.values.get('io_power_ratio')}, expected 186.7")
    ok(pan.applicable and abs(pan.values["orbital_period"] - 31.9987) < 0.001, f"2: Pandora P_orb {pan.values.get('orbital_period')} h, expected 31.9987")
    ok(pan.applicable and pan.values["heat_transport_regime"] == th.REGIME_VIGOROUS, "2: Pandora regime must be the §6.1 top row")
    mode = th.solve_mode(pan.values["surface_flux"], 13.744e12, 5724e3 / th.R_EARTH_M)
    ok(mode.applicable and mode.values["mode"] == th.MODE_HEAT_PIPE, f"2: Pandora total flux → heat pipe, got {mode.values.get('mode')}")
    ok(mode.applicable and abs(mode.values["total_surface_flux"] - (45.337 + 13.744e12 / (4 * math.pi * 5724e3 ** 2))) < 0.01,
       "2: total flux must add the radiogenic W/4πR²")
    # 3. ×Io convention (doc rows)
    e9 = th.tidal_power(0.0155, 120.0 * th.M_EARTH_KG, 900e3, 110_000e3, 0.0186)
    e5 = th.tidal_power(0.0155, 120.0 * th.M_EARTH_KG, 521e3, 110_000e3, 0.0186)
    ok(abs(e9[0] / e5[0] - 1200 / 78) / (1200 / 78) < 0.001, "3: the doc's ×Io column must scale as R⁵ (1200/78)")
    ok(abs(e9[1] / e5[1] - 11500 / 2231) / (11500 / 2231) < 0.001, "3: the doc's W/m² column must scale as R³ (11500/2231)")
    ok(abs(e5[0] / th.IO_POWER_W - 79.3) < 0.2, f"3: Dante 521 km is {e5[0] / th.IO_POWER_W:.1f}× on the 1e14 denominator (doc 78× on 1.016e14)")
    # 4. labels
    ok([th.outcome_regime(f) for f in (2.0, 0.5, 0.05, 0.005, 1e-4)] ==
       [th.REGIME_VIGOROUS, th.REGIME_ACTIVE, th.REGIME_OCEAN, th.REGIME_UNCLASSIFIED, th.REGIME_DEAD], "4: §6.1 rows and the unclassified decade")
    ok([th.transport_mode(f) for f in (3.0, 0.0921, 0.02, 0.5)] ==
       [th.MODE_HEAT_PIPE, th.MODE_PLATE, th.MODE_STAGNANT, th.MODE_UNCLASSIFIED], "4: §6.2 modes (Earth 92.1 mW/m² → plate tectonics) and the gap")
    # 4b. 정체뚜껑 상한 선택지 (C32 ②) — `consequences` 에 적힌 3/4 대 1/4 을 문장이 아니라 기계로 확인한다.
    # 엔진이 방사성만으로 낸 네 대조군 플럭스 [W/m²] 와 문서 §6.2 가 그 바디에 붙인 라벨
    # (c32-f-g-transport-thresholds-notes.ko.md 의 실행표; Mercury 는 측정 플럭스가 없고 라벨만 있다).
    controls = ((0.01575, th.MODE_STAGNANT), (0.03775, th.MODE_STAGNANT),   # Mercury, Venus
                (0.04180, th.MODE_PLATE),    (0.01587, th.MODE_STAGNANT))   # Earth, Mars
    agree = {c["value"]: sum(th.transport_mode(f, c["value"]) == want for f, want in controls)
             for c in th.STAGNANT_LID_CEILING_CHOICE.candidates}
    ok(agree == {0.030: 3, 0.010: 1},
       f"4b: the choice's stated consequence is 3 of 4 at the high end and 1 of 4 at the low end, got {agree}")
    ok(th.STAGNANT_LID_CEILING_CHOICE.default == th.STAGNANT_LID_CEILING.high and
       th.transport_mode(0.02) == th.MODE_STAGNANT,
       "4b: until someone chooses, the high end stands and today's behaviour is unchanged")
    ok(th.transport_mode(0.01587, 0.010) == th.MODE_PLATE,
       "4b: below the ceiling the table has no 'neither' — the low end calls Mars plate tectonics")

    # 5. refusals
    ok(not th.solve(1.0, 1.0, None, None, None, 0.01).applicable and "no orbit" in th.solve(1.0, 1.0, None, None, None, 0.01).reason, "5: no orbit refuses by name")
    ok("no k2_over_q" in th.solve(1.0, 1.0, 3.8e5, 1.0, 0.05, None).reason, "5: no k₂/Q refuses by name")
    ok("no radius" in th.solve(1.0, None, 3.8e5, 1.0, 0.05, 0.01).reason, "5: no radius refuses by name")
    ok("no heat source" in th.solve_mode(None, None, 1.0).reason, "5: mode with no heat source refuses by name")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 조석 가열 — 이오 Ė {p_io:.3e} W (밴드 0.6–1.6e14 안, P {2 * math.pi / n_io / 86400:.3f} d) · 판도라 F {pan.values['surface_flux']:.2f} W/m² "
              f"(보드 45, {(pan.values['surface_flux'] / 45 - 1) * 100:+.2f} %) {pan.values['io_power_ratio']:.0f}× Io → {th.REGIME_VIGOROUS[:9]}… / {th.MODE_HEAT_PIPE} · "
              f"×Io 규약 R⁵ · 라벨 표 둘 · 정체뚜껑 선택지 3/4 대 1/4 · 거절 4")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
