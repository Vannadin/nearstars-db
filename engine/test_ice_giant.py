# 얼음거대행성 앵커 — 굳혀 둔 수렴점을 적분 한 번으로 대조한다 (전체 재계산은 --refresh)
"""Anchor the ice-giant branch without paying for the full solve on every gate run.

    python3 engine/test_ice_giant.py              빠른 대조 (수 초). check.sh 가 부른다
    python3 engine/test_ice_giant.py --refresh    전체 재계산 → ice_giant_anchor.json 갱신
    python3 engine/test_ice_giant.py --table      문서의 얼음거대행성 표를 다시 낸다

**왜 굳히는가.** 천왕성 하나가 2026-08-28 기준 729 초다 (이 작업 전 1038 초) (`speed-context-notes.md` §3·§6 —
압력 사격이 층 경계의 계단에서 수렴하지 못하고 SHOOT_ITERS 를 다 쓰는 것이 원인이고, 그
수렴 결함을 고치는 것은 답을 바꾸는 일이라 이 파일의 몫이 아니다). check.sh 예산에 안
들어가므로 예전에는 앵커가 `--icegiant` 뒤에 숨어 있었고, 그 플래그마저 낡은 2500 K
선언으로 거절을 찍고 있었다. 그래서 얼음 III·V·VI 상수와 같은 규율로 간다 — 비싼 계산은
한 번 해서 파일에 굳히고, 게이트는 **그 파일이 코드와 아직 맞는지** 만 싸게 확인한다.

**굳힌 값이 낡는 것을 무엇이 잡는가.** 둘이다.

1. **적분 한 번.** 수렴점의 (중심압, 중심온도) 에서 `integrate()` 를 한 번 돌리면 그것이
   곧 풀이의 마지막 적분이고, 그 출력(반지름·질량·관성모멘트·표면온도)이 굳힌 값과
   **비트까지** 같아야 한다. 상태방정식·페르미 적분·적분기·층 쌓기 어느 것이 바뀌어도
   여기서 걸린다. 0.5 초.
2. **경로 지문.** 사격과 온도 고리(`shoot`, `_shoot_pressure`, `_narrow_bracket`, `solve` 와
   그 상수들)의 바이트코드 해시. 적분 한 번은 바깥 고리가 **다른 수렴점** 으로 가게 된
   변화를 못 본다 — 괄호잡기 순서 하나가 바뀌면 마지막 비트가 움직인 전례가 있다
   (ice-giant-context-notes). 그 코드가 바뀌면 이 게이트는 실패하고 --refresh 를 요구한다.
   주석·docstring 만 바뀐 것은 지문에 안 잡힌다.

둘 다 통과하면 굳힌 값은 **현재 코드가 낼 값** 이다. 어느 하나라도 어긋나면 게이트가
실패하고, 그 실패를 지우는 방법은 --refresh 하나뿐이다 — 값을 손으로 고치면 굳힌 것이
아니라 적은 것이 된다.

**해왕성도 앵커다.** hhe-eos-context-notes 는 해왕성이 클래스 기반 얼음 디스패치에서
3 K 차이로 거절된다고 적었지만, 지금 코드로 72 K 에서 돌리면 적분된다 (345 초, +8.99 %,
speed-context-notes §8). 디스패치는 손대지 않았다. 어느 천체든 거절로 끝나면 거절문을
굳혀 두고 게이트는 [FROZEN] 으로 그 사실만 말한다 — 거절도 전체 온도 고리를 돈 뒤에
나오므로 빠르지 않다.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import interior
from interior import EARTH_MASS_KG, EARTH_RADIUS_M, integrate, solve

ANCHOR_FILE = Path(__file__).with_name("ice_giant_anchor.json")

# 얼음거대행성의 앵커. Scheibe+ 2019 Table 1 의 **Mazevet 물 EOS 행** 에서 왔다 —
# 우리가 쓰는 것과 같은 상태방정식으로 지은 모형이라야 조성을 빌려올 수 있다.
# 온도는 **1 bar 온도** 다 (Voyager 전파엄폐, hhe-eos-context-notes). 수소-헬륨 표가 들어온
# 뒤로 포텐셜 온도의 선언은 표면(1 bar)에 걸리고, 발표 반지름도 그 준위의 값이다.
# 2500 K (얼음 맨틀 꼭대기로 읽던 폴리트로프 시절의 값) 를 그대로 두면 두 행성 다 거절된다.
# (이름, M⊕, 발표 평균반지름 R⊕, 암석 핵 M⊕, H/He 총량 M⊕, 1 bar K)
ICE_GIANTS = (
    ("Uranus", 14.536, 3.9808, 0.79, 2.0, 76.0),
    ("Neptune", 17.147, 3.8646, 1.04, 2.2, 72.0),
)


def _fractions(m: float, m_core: float, m_hhe: float) -> tuple[float, float]:
    gmf = m_hhe / m
    return 1.0 - gmf - m_core / m, gmf


def _solve(name: str):
    for n, m, _r, m_core, m_hhe, t1bar in ICE_GIANTS:
        if n == name:
            imf, gmf = _fractions(m, m_core, m_hhe)
            return solve(m, body_class="ice_giant", core_mass_fraction=0.0,
                         ice_mass_fraction=imf, gas_mass_fraction=gmf,
                         potential_temperature=t1bar)
    raise KeyError(name)


# ── 경로 지문 ────────────────────────────────────────────────────────────

# 굳힌 수렴점으로 가는 길을 정하는 것들. 적분기 자체는 지문에 없어도 된다 — 적분 한 번이
# 그것을 직접 대조한다. 여기 있는 것은 **어느 수렴점에 닿는가** 를 정하는 바깥 고리다.
PATH_FUNCTIONS = ("solve", "shoot", "_shoot_pressure", "_narrow_bracket",
                  "_surface_temperature_met", "_stack")
PATH_CONSTANTS = ("STEPS", "MAX_STEPS", "SHOOT_ITERS", "SHOOT_TOL", "T_PASSES", "T_TOL",
                  "T_SURFACE_TOL", "T_BRACKET_TRIES", "NARROW_ITERS", "NARROW_RATIO",
                  "FLUID_CLASSES", "ICE_GIANT_CLASSES")


def _feed_code(h, code) -> None:
    """코드 객체를 재귀로 해시한다. docstring(첫 상수가 문자열이면) 은 뺀다."""
    h.update(code.co_code)
    h.update(repr(code.co_names).encode())
    consts = list(code.co_consts)
    if consts and isinstance(consts[0], str):
        consts = consts[1:]
    for c in consts:
        if hasattr(c, "co_code"):
            _feed_code(h, c)
        else:
            h.update(repr(c).encode())


def path_fingerprint() -> str:
    h = hashlib.sha256()
    for name in PATH_FUNCTIONS:
        _feed_code(h, getattr(interior, name).__code__)
    for name in PATH_CONSTANTS:
        h.update(f"{name}={getattr(interior, name)!r}".encode())
    # 바이트코드는 인터프리터 버전에 묶인다. 버전이 바뀌면 지문이 바뀌고, 그건 --refresh 로
    # 답할 일이지 지문을 넓힐 일이 아니다.
    h.update(platform.python_version().encode())
    return h.hexdigest()[:16]


# ── 굳히기 ──────────────────────────────────────────────────────────────

def _standalone(name: str, p_center_pa: float, t_center: float):
    """수렴점에서 적분 한 번. 풀이의 마지막 적분과 같은 인자다."""
    for n, m, _r, m_core, m_hhe, t1bar in ICE_GIANTS:
        if n == name:
            imf, gmf = _fractions(m, m_core, m_hhe)
            return integrate(p_center_pa, m * EARTH_MASS_KG, 0.0, imf, "fe_prem", gmf=gmf,
                             t_center=t_center, t_pot=t1bar, ice_material="h2o_hot")
    raise KeyError(name)


def _structure_record(st) -> dict:
    return {"radius_earth": repr(st.radius_m / EARTH_RADIUS_M),
            "mass_kg": repr(st.mass_kg), "moi": repr(st.moi), "nmoi": repr(st.nmoi),
            "t_surface": repr(st.t_surface), "p_ice_base": repr(st.p_ice_base),
            "core_radius_m": repr(st.core_radius_m)}


def refresh() -> int:
    out = {"python": platform.python_version(), "path_fingerprint": path_fingerprint(),
           "frozen_at": time.strftime("%Y-%m-%d"), "bodies": {}}
    for name, m, r_pub, _mc, _mh, t1bar in ICE_GIANTS:
        print(f"{name} — 전체 풀이 (느리다) …", flush=True)
        t0 = time.perf_counter()
        res = _solve(name)
        seconds = time.perf_counter() - t0
        rec = {"seconds": round(seconds, 1), "regime": res.regime, "applicable": res.applicable,
               "converged": res.converged, "grade": res.grade, "t_1bar_k": t1bar,
               "r_published_earth": r_pub}
        if res.applicable:
            v = res.values
            rec["values"] = {k: (repr(x) if isinstance(x, float) else x) for k, x in v.items()}
            p_pa = v["core_pressure"] * 1e9
            st = _standalone(name, p_pa, v["core_temperature"])
            rec["standalone"] = {"p_center_pa": repr(p_pa),
                                 "t_center": repr(v["core_temperature"]),
                                 **_structure_record(st)}
            same = rec["standalone"]["radius_earth"] == repr(v["radius"])
            rec["standalone_reproduces_solve"] = same
            print(f"  {seconds:.0f} s · R {v['radius']:.4f} R⊕ ({(v['radius'] / r_pub - 1) * 100:+.2f} %) "
                  f"· T_c {v['core_temperature']:.0f} K · converged={res.converged} · "
                  f"적분 한 번이 풀이를 재현{'한다' if same else '하지 못한다'}")
        else:
            rec["reason"] = res.reason
            print(f"  {seconds:.0f} s · 거절 — {res.reason[:90]}")
        out["bodies"][name] = rec
    ANCHOR_FILE.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"굳혔다 → {ANCHOR_FILE.name}")
    return 0


def table() -> None:
    """문서의 얼음거대행성 표. 굳힌 파일에서 낸다 — 전체 풀이를 다시 돌리지 않는다."""
    frozen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    print("| planet | T at 1 bar | R derived | R published | Δ | C/MR² | T_c | P_c | "
          "converged | grade |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, rec in frozen["bodies"].items():
        r_pub = rec["r_published_earth"]
        if not rec["applicable"]:
            print(f"| {name} | {rec['t_1bar_k']:.0f} K | declined | {r_pub:.3f} R⊕ | – | – | – | – "
                  f"| – | – |")
            continue
        v = {k: float(rec["values"][k]) for k in ("radius", "nmoi", "core_temperature", "core_pressure")}
        print(f"| {name} | {rec['t_1bar_k']:.0f} K | {v['radius']:.3f} R⊕ | {r_pub:.3f} R⊕ | "
              f"{(v['radius'] / r_pub - 1) * 100:+.2f} % | {v['nmoi']:.4f} | "
              f"{v['core_temperature']:.0f} K | {v['core_pressure']:.0f} GPa | "
              f"{rec['converged']} | {rec['grade']} |")


# ── 빠른 대조 ────────────────────────────────────────────────────────────

def main() -> int:
    if "--refresh" in sys.argv:
        return refresh()
    if "--table" in sys.argv:
        table()
        return 0

    fails: list[str] = []
    if not ANCHOR_FILE.exists():
        print(f"  [FAIL] {ANCHOR_FILE.name} 이 없다 — `--refresh` 로 굳혀라 (천왕성 ~13 분)")
        return 1
    frozen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))

    print("얼음거대행성 앵커 — 굳힌 수렴점이 아직 이 코드의 것인가")
    print(f"  굳힌 날 {frozen['frozen_at']} · python {frozen['python']}")
    fp_now, fp_then = path_fingerprint(), frozen["path_fingerprint"]
    ok = fp_now == fp_then
    if not ok:
        fails.append("사격·온도 고리의 경로 지문이 굳힐 때와 다르다 — 수렴점이 옮겨갔을 수 "
                     "있다. `test_ice_giant.py --refresh` 로 다시 굳혀라")
    print(f"  [{'PASS' if ok else 'FAIL'}] 경로 지문 {fp_then} "
          f"{'그대로' if ok else '→ ' + fp_now + ' (바뀜)'} — "
          f"{', '.join(PATH_FUNCTIONS)} + 상수 {len(PATH_CONSTANTS)}개")

    for name, rec in frozen["bodies"].items():
        if not rec["applicable"]:
            print(f"  [FROZEN] {name} — 거절이 앵커다 ({rec['seconds']:.0f} s 라 다시 안 돈다). "
                  f"굳힌 이유: {rec['reason'][:70]}…")
            continue
        sa = rec["standalone"]
        t0 = time.perf_counter()
        st = _standalone(name, float(sa["p_center_pa"]), float(sa["t_center"]))
        dt = time.perf_counter() - t0
        now = _structure_record(st)
        moved = [k for k in ("radius_earth", "mass_kg", "moi", "t_surface", "p_ice_base")
                 if now[k] != sa[k]]
        if moved:
            fails.append(f"{name}: 굳힌 수렴점에서 적분이 다른 값을 낸다 — "
                         + ", ".join(f"{k} {sa[k]} → {now[k]}" for k in moved)
                         + ". 상태방정식이나 적분기가 바뀌었다. `--refresh` 로 다시 굳혀라")
        v = rec["values"]
        r = float(v["radius"])
        print(f"  [{'FAIL' if moved else 'PASS'}] {name} — 수렴점 (P_c {float(sa['p_center_pa']) / 1e9:.1f} GPa, "
              f"T_c {float(sa['t_center']):.0f} K) 에서 적분 한 번 {dt:.1f} s: "
              f"{'움직였다: ' + ', '.join(moved) if moved else '반지름·질량·관성모멘트·표면온도 비트까지 같다'}")
        print(f"         R {r:.4f} R⊕ vs 발표 {rec['r_published_earth']:.4f} "
              f"({(r / rec['r_published_earth'] - 1) * 100:+.2f} %) · T_c {float(v['core_temperature']):.0f} K "
              f"· 전체 풀이 {rec['seconds']:.0f} s · converged={rec['converged']}"
              + ("" if rec["converged"] else " — **수렴하지 못한 해다** (speed-context-notes §6)"))
        if not rec.get("standalone_reproduces_solve", True):
            print("         (굳힐 때 적분 한 번이 풀이의 반지름을 재현하지 못했다 — 이 대조는 "
                  "적분의 자기 일관성만 본다)")

    print("  [SKIP] 전체 풀이(온도 고리 + 압력 사격)는 여기서 안 돈다 — `--refresh` 가 돈다. "
          "위 지문이 그 고리의 변화를 대신 잡는다")

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
