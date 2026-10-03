# 뚜껑 체제 규칙(C158)을 지키는가 — 한 파서 · 하한 플럭스 · 음성 대조 · 단조 · 열파이프 · Korenaga · 오너 메모
"""prereg-c158-lid-regime (frozen a4310e84): L-parse, L-bound, L-neg, L-mono, L-pipe, L-kor, L-note.

    python3 engine/test_lid_regime.py
"""
from __future__ import annotations

import ast
import math
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lid_regime as L          # noqa: E402
import tectonic_regime as tr    # noqa: E402
import tidal_heating as th      # noqa: E402

fails: list[str] = []


def ok(cond: bool, label: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        fails.append(label)


def body(name: str) -> dict:
    """선언값 — g, 맨틀 두께 h(선언된 핵 반지름 비, 없으면 지구의 0.547), T_p, T_s."""
    d = yaml.safe_load((HERE / "bodies" / f"{name}.yaml").read_text(encoding="utf-8"))["inputs"]
    crf = d.get("core_radius_fraction")
    crf = crf.get("value") if isinstance(crf, dict) else (crf or 0.547)
    r = d["radius_earth"] * th.R_EARTH_M
    ts = d.get("surface_temperature_k")
    return {"g": th.G * d["mass_earth"] * th.M_EARTH_KG / r ** 2, "h": r * (1.0 - crf),
            "tp": d.get("potential_temperature"), "ts": ts.get("value") if isinstance(ts, dict) else ts,
            "regime": d.get("tectonic_regime")}


def l_parse() -> None:
    contested = {"value": "contested", "grade": "declared", "source": "x", "contested": ["a", "b"]}
    ok(tr.declared(contested).value == "contested" and tr.derived_stagnant_lid(contested).value is True,
       "L-parse: a `contested` block reads «contested» through the one parser, and derives stagnant=True")
    # 블록을 읽는 모듈은 전부 `tectonic_regime` 모듈을 통한다 — 원시 값을 꺼내는 자리가 없다
    readers = []
    for f in sorted(HERE.glob("*.py")):
        if f.name.startswith("test_") or f.name == "tectonic_regime.py":
            continue
        src = f.read_text(encoding="utf-8")
        if '"tectonic_regime"' in src:
            mods = {a.name for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Import) for a in n.names}
            mods |= {n.module for n in ast.walk(ast.parse(src)) if isinstance(n, ast.ImportFrom) and n.module}
            readers.append((f.name, "tectonic_regime" in mods))
    # structure_grid 은 이 키를 표의 방아쇠 목록(THERMAL_KEYS)에 이름으로만 싣는다 — 값을 읽지 않는다
    bad = [n for n, uses in readers if not uses and n != "structure_grid.py"]
    ok(readers and not bad, f"L-parse: every module that reads the `tectonic_regime` key imports the parser — "
                            f"{len(readers)} reader(s){'; not: ' + ', '.join(bad) if bad else ''}")


def l_bound() -> None:
    cases = [(3.0, None, th.MODE_HEAT_PIPE), (0.0902, None, th.MODE_PLATE), (0.0426, "earth", th.MODE_NOT_STAGNANT),
             (0.025, "venus", th.MODE_NOT_STAGNANT), (0.025, "mars", th.MODE_UNDECIDED),
             (0.0121, "mars", th.MODE_UNDECIDED)]
    got = [th.flux_reading(f, b)[0] for f, b, _w in cases]
    ok(got == [w for *_x, w in cases], f"L-bound: the flux reading decides only upward, per-body ceiling — {got}")
    c = th.regime_candidates(0.0426, 1.0, flux_kind="lower")
    hot = th.regime_candidates(0.147, 0.9499, flux_kind="lower")
    ok(c["mobile lid"][0] == "cannot decide" and hot["mobile lid"][0] == "excluded",
       "L-bound: a lower bound below the 40 TW floor cannot decide; above the 50 TW ceiling it still excludes")


def l_neg() -> None:
    """flux 를 값(exact)으로 읽으면 오늘의 이름표가 돌아와야 한다 — 픽스처가 R2 를 본다."""
    ok(th.transport_mode(0.0426) == th.MODE_PLATE and th.regime_ladder_cell(0.0426)[0] == th.CEILING_EXCEEDED_CELL
       and th.transport_mode(0.0121) == th.MODE_STAGNANT
       and th.regime_candidates(0.0426, 1.0)["mobile lid"][0] == "excluded",
       "L-neg: read as exact, Earth's flux is «plate» and «squishy» at once, Mars «stagnant», mobile lid excluded")


def l_mono() -> None:
    for name in ("earth", "venus", "mars", "pandora"):
        b = body(name)
        p = L.heat_pipe_test(0.0, b["tp"], b["ts"] or 273.0, b["g"], b["h"])
        ok(p.get("mono") is True, f"L-mono: {name} q_SL rises strictly on [{b['tp']:.0f} K, {p['t_liq_k']:.0f} K] "
                                  f"(20 K steps) — max {p['q_sl_max']:.4g} W/m² at the liquidus")


def l_pipe() -> None:
    b = body("pandora")
    q = L.heat_pipe_test(0.0, b["tp"], 288.0, b["g"], b["h"])["q_sl_max"]
    above = L.heat_pipe_test(q * 1.001, b["tp"], 288.0, b["g"], b["h"])["verdict"]
    below = L.heat_pipe_test(q * 0.999, b["tp"], 288.0, b["g"], b["h"])["verdict"]
    pan = L.heat_pipe_test(45.36, b["tp"], 288.0, b["g"], b["h"])
    ok(above == "heat pipe" and below is None and pan["verdict"] == "heat pipe",
       f"L-pipe: heat pipe only above q_SL,max ({q:.4g} W/m²); Pandora {pan['ratio']:.0f}×")
    t_free = [L.heat_pipe_test(45.36, b["tp"], ts, b["g"], b["h"])["q_sl_max"] for ts in (0.0, 288.0, 700.0)]
    ok(max(t_free) - min(t_free) <= 1e-12 * max(t_free),
       "L-pipe: q_SL does not depend on T_s (θ and Ra both ∝ ΔT; ΔT^(1 − 4/3 + 1/3) = 1), so R3 needs no T_s")
    ok(L.heat_pipe_test(1.0, 2100.0, 288.0, b["g"], b["h"])["refusal"] == L.MAGMA_OCEAN_REFUSAL,
       "L-pipe: a declared T_p above the 1-bar liquidus refuses by name")


def l_kor() -> None:
    b = body("earth")
    mc = L.mu_crit(b["tp"], b["ts"], b["g"], b["h"])
    dl, crit = L.korenaga(mc, b["tp"], b["ts"], b["g"], b["h"])
    ok(abs(dl / crit - 1.0) < 1e-9, f"L-kor: μ_crit {mc:.4f} closes Δη_L = 0.25 Ra^½ to 1e-9 (a self-check)")
    def v(lo, hi, basis="water-weakened"):
        return L.korenaga_test({"low": lo, "high": hi, "basis": basis, "grade": "declared", "source": "t"},
                               b["tp"], b["ts"], b["g"], b["h"])
    below, strad, above = v(0.5 * mc, 0.9 * mc), v(0.5 * mc, 2.0 * mc), v(0.6, 0.7, "dry")
    ok(below["verdict"].startswith("plate") and strad["verdict"].startswith("undetermined")
       and above["verdict"].startswith("stagnant") and f"{mc:.3f}" in strad["verdict"],
       "L-kor: μ wholly below / straddling / wholly above μ_crit → plate favoured / undetermined (μ_crit) / "
       "stagnant favoured — dry Byerlee 0.6–0.7 gives stagnant on Earth")
    none = L.korenaga_test(None, b["tp"], b["ts"], b["g"], b["h"])
    nobasis = L.korenaga_test({"low": 0.03, "high": 0.13}, b["tp"], b["ts"], b["g"], b["h"])
    ok(none["refusal"] == L.UNDECLARED_REFUSAL and nobasis["refusal"] and "basis" in nobasis["refusal"],
       "L-kor: μ undeclared → named refusal; μ without a dry / water-weakened basis → named refusal (owner Q3)")
    und = L.resolve(None, 0.0426, b["tp"], b["ts"], b["g"], b["h"], None)
    ok(und["value"] is None and und["source"] == "undetermined" and und["why"] == L.UNDECLARED_REFUSAL,
       "L-kor: an undeclared body with no μ gets the regime-only named refusal (owner Q1)")


def l_note() -> None:
    b = body("pandora")
    reading = tr.declared(b["regime"])
    out = L.resolve(reading.value, 45.36, b["tp"], None, b["g"], b["h"], None, override=reading.override is not None)
    ratio = out["heat_pipe"]["ratio"]
    want = L.OVERRIDE_NOTE.format(h=45.36, ratio=ratio)
    ok(reading.override and out["source"] == "declared (owner setting override)" and want in out["notes"]
       and want == f"physics says heat pipe (tidal 45 W/m², {ratio:.0f}× the max stagnant-lid capacity); "
                   "owner setting override: mobile lid",
       f"L-note: Pandora carries the owner's template note, ratio computed ({ratio:.0f}×)")
    ok(abs(ratio / 526.0 - 1.0) <= 0.20,
       f"L-note: the ratio {ratio:.0f} is within 526 ± 20 % (outside would be an owner report, not a FAIL)")


if __name__ == "__main__":
    for fn in (l_parse, l_bound, l_neg, l_mono, l_pipe, l_kor, l_note):
        fn()
    print(f"{'모두 통과' if not fails else f'{len(fails)} 실패'}")
    sys.exit(1 if fails else 0)
