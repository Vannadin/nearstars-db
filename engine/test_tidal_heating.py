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

    # ── 4c. C34: 먹이는 양의 후보 넷은 판정 중립이 아니다 (오너 결정 2026-09-07, 저단 채택) ──
    # ⚠ 이것이 결정의 근거다. 지구 기준 후보 넷이 2.203× 폭인데, 수성·화성은 정체뚜껑 경계까지
    # 1.9× 여유뿐이다. 그래서 먹이는 양을 위로 재는 선택은 그 둘을 판구조로 넘기고, 문서는 둘 다
    # 정체뚜껑으로 적는다. **고른 것이 아니라 문서 앵커가 판별했다** — 이 시험이 그 판별을 고정한다.
    C34_LOW, C34_HIGH = 0.0418, 0.0921
    docs = {"Mercury": (0.01575, th.MODE_STAGNANT), "Venus": (0.03775, th.MODE_STAGNANT),
            "Earth": (0.04180, th.MODE_PLATE), "Mars": (0.01587, th.MODE_STAGNANT)}
    span = C34_HIGH / C34_LOW
    agree_low = sum(th.transport_mode(f) == want for f, want in docs.values())
    agree_high = sum(th.transport_mode(f * span) == want for f, want in docs.values())
    ok((agree_low, agree_high) == (3, 1),
       f"4c/C34: the low end must reproduce 3 of the document's 4 anchor labels and the high end 1; "
       f"got {agree_low} and {agree_high}. If this moves, the grounds for feeding the total flux moved")
    ok(abs(span - 2.203) < 0.002, f"4c/C34: the candidate spread is 2.203×, got {span:.4f}")
    for name, margin in (("Mercury", 0.030 / 0.01575), ("Mars", 0.030 / 0.01587)):
        ok(margin < span,
           f"4c/C34: {name} sits {margin:.2f}× below the boundary, inside the {span:.2f}× spread — "
           f"that is why the band was not neutral")
    # ⚠ 안 고쳐진 것: 금성은 양쪽 끝에서 다 어긋난다. 3/4 이지 4/4 가 아니다.
    ok(th.transport_mode(0.03775) != th.MODE_STAGNANT and
       th.transport_mode(0.03775 * span) != th.MODE_STAGNANT,
       "4c/C34: Venus disagrees with the document at both ends — the decision does not repair it")

    # 5. refusals
    ok(not th.solve(1.0, 1.0, None, None, None, 0.01).applicable and "no orbit" in th.solve(1.0, 1.0, None, None, None, 0.01).reason, "5: no orbit refuses by name")
    ok("no k2_over_q" in th.solve(1.0, 1.0, 3.8e5, 1.0, 0.05, None).reason, "5: no k₂/Q refuses by name")
    ok("no radius" in th.solve(1.0, None, 3.8e5, 1.0, 0.05, 0.01).reason, "5: no radius refuses by name")
    ok("no heat source" in th.solve_mode(None, None, 1.0).reason, "5: mode with no heat source refuses by name")

    # ── 4d. C46 (b): 열류는 체이고 분류기가 아니다 (오너 결정 2026-09-07, 밴드) ──────────────
    # ⚠ 이 시험이 지키는 것은 수가 아니라 **밴드가 좁혀지지 않는다**는 사실이다. 문헌은 이 체제들을
    # mobility 와 plateness 로 가르고(Lourenço+ 2020 §3.1·§3.3) 둘 다 4.5 Gyr 시뮬레이션 출력이라
    # 관측 못 하는 천체에는 잴 수 없다. 그래서 우리가 열류로 할 수 있는 일은 **인쇄된 구간 밖을
    # 배제하는 것**뿐이고, 대개 그것도 못 한다.
    E_AREA = th.EARTH_AREA_M2
    earth = th.solve_mode(surface_flux=46.0e12 / E_AREA, radiogenic_power=None, radius_earth=1.0)
    ok(len(earth.values["regime_candidates"]) == 4 and not earth.values["regime_excluded"],
       f"4d/C46: Earth at its measured 46 TW excludes NOTHING — the textbook mobile-lid planet is "
       f"compatible with stagnant lid on this axis. Got {earth.values['regime_candidates']} / "
       f"excluded {earth.values['regime_excluded']}")
    # ⚠ 엔진의 금성 값은 mobile lid 를 배제한다. 그런데 **측정값은 배제하지 않는다.**
    v_engine = th.solve_mode(surface_flux=0.03775, radiogenic_power=None, radius_earth=0.9499)
    v_measured = th.solve_mode(surface_flux=0.078, radiogenic_power=None, radius_earth=0.9499)
    ok(v_engine.values["regime_excluded"] == ["mobile lid"],
       f"4d/C46: the engine's own Venus flux (17.4 TW) is the one case that excludes anything; "
       f"got {v_engine.values['regime_excluded']}")
    # ⚠ 정정 2026-09-07: 이 자리에 "측정값을 먹이면 배제가 사라진다" 가 있었고 **틀렸다.**
    # mobile lid 의 총합 40–50 TW 를 그때 못 봤고, 바닥이 35 가 아니라 40 이다. 금성 측정 35.9 TW 는
    # 그 밑이라 **여전히 배제된다** — 그리고 그게 문헌과 맞는다(금성에 판구조 없음).
    ok(v_measured.values["regime_excluded"] == ["mobile lid"],
       f"4d/C46: Smrekar's measured Venus is 35.9 TW, under the printed mobile-lid floor of 40 TW, so "
       f"mobile lid stays excluded; got {v_measured.values['regime_excluded']}")
    earth_only = th.solve_mode(surface_flux=0.0902, radiogenic_power=None, radius_earth=1.0)
    ok(not earth_only.values["regime_excluded"],
       "4d/C46: and Earth at 46 TW is the ONE body compatible with mobile lid — the axis separates the "
       "two after all, once the total range is read instead of the conductive component")
    ok("heat pipe (a stagnant-lid sub-case)" in earth.values["regime_flux_cannot_decide"],
       "4d/C46: heat pipe is not a peer regime — it is stagnant lid at 100 % eruption efficiency, and "
       "no flux is printed for it, so flux cannot speak to it at all")
    ok(all(len(th.solve_mode(surface_flux=f, radiogenic_power=None,
                             radius_earth=1.0).values["regime_candidates"]) >= 3
           for f in (0.01, 0.05, 0.09, 0.2)),
       "4d/C46: across four decades of flux the candidate set never narrows below three — that is the "
       "result, not a failure to classify")

    # ── 4e. C46 사다리 (오너 결정 2026-09-07): 넘긴 눈금 중 가장 높은 칸으로 확정 ─────────────
    # ⚠ 이 시험이 지키는 것은 "지구가 plate 로 나온다" 가 **아니다** — 그 눈금이 지구이므로 그건
    # 증거가 아니다. 지키는 것은 (1) 눈금이 §6.2 가 인쇄한 천체 값 그대로일 것, (2) 금성 오차가
    # 칸 둘을 가로지른다는 사실, (3) 최저 눈금 밑에 별도 상태가 있을 것, (4) 사다리가 밴드를
    # 지우지 않을 것.
    ok([f for _n, f, _w in th.REGIME_LADDER] == [0.010, 0.09, 2.5],
       f"4e/C46: the rungs must be §6.2's printed body values, unchanged; got {th.REGIME_LADDER}")
    ok(th.regime_ladder_cell(0.0902)[0] == "plate tectonics" and
       abs(0.0902 / 0.09 - 1) < 0.005,
       "4e/C46: Earth's measured flux sits on the Earth rung with 0.2 % to spare — a tautology, "
       "recorded so nobody reads it as a verdict")
    v_lo, v_mid, v_hi = (th.regime_ladder_cell(f)[0] for f in (0.009, 0.078, 0.147))
    ok(v_lo == th.BELOW_LADDER and v_mid == "stagnant lid" and v_hi == "plate tectonics",
       f"4e/C46: ⚠ Venus's 78±69 mW/m² spans THREE states — {v_lo!r} / {v_mid!r} / {v_hi!r}. One "
       f"error bar crosses the ladder, which is the honest reading of a one-cell answer")
    ok(th.regime_ladder_cell(0.005)[1] is None,
       "4e/C46: below the lowest rung there is a named state, not a silent stagnant lid")
    both = th.solve_mode(surface_flux=0.0902, radiogenic_power=None, radius_earth=1.0).values
    ok(both["regime_ladder_cell"] == "plate tectonics" and len(both["regime_candidates"]) == 4,
       "4e/C46: the one-cell answer travels BESIDE the band, so a reader sees how thin it is")
    # ⚠ 4f. 어제 놓친 줄 — mobile lid 는 총합 양쪽이 인쇄돼 있다. 그래서 위로도 배제된다.
    hot = th.solve_mode(surface_flux=0.147, radiogenic_power=None, radius_earth=0.9499).values
    ok("mobile lid" in hot["regime_excluded"],
       f"4f/C46: Lourenço prints the mobile-lid TOTAL as 40–50 TW, so 67.7 TW is excluded from above. "
       f"An earlier version recorded that regime as having no printed ceiling; got "
       f"{hot['regime_excluded']}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 조석 가열 — 이오 Ė {p_io:.3e} W (밴드 0.6–1.6e14 안, P {2 * math.pi / n_io / 86400:.3f} d) · 판도라 F {pan.values['surface_flux']:.2f} W/m² "
              f"(보드 45, {(pan.values['surface_flux'] / 45 - 1) * 100:+.2f} %) {pan.values['io_power_ratio']:.0f}× Io → {th.REGIME_VIGOROUS[:9]}… / {th.MODE_HEAT_PIPE} · "
              f"×Io 규약 R⁵ · 라벨 표 둘 · 정체뚜껑 선택지 3/4 대 1/4 · 거절 4 · ⚠ C46 열류=체(지구 배제 0 · 측정 금성 배제 0 · 후보 3 미만 없음) · C46 사다리(눈금=§6.2 천체값 · 금성 오차가 칸 셋 가로지름 · 최저 밑 별도 상태 · 밴드 동반)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
