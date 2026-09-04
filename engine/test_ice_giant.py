# 얼음거대행성 앵커 — 천왕성·해왕성을 실제로 풀어 굳힌 값과 비트까지 대조한다
"""Anchor the ice-giant branch: Uranus and Neptune, solved live on every gate run.

    python3 engine/test_ice_giant.py              전체 풀이 둘 (~1.5 분) + 굳힌 값과 비트 대조
    python3 engine/test_ice_giant.py --fast       적분 한 번 + 경로 지문만 (1 초). 반복 작업용
    python3 engine/test_ice_giant.py --refresh    전체 재계산 → ice_giant_anchor.json 갱신
    python3 engine/test_ice_giant.py --table      문서의 얼음거대행성 표를 다시 낸다

**왜 이 파일이 있나.** 2026-08-28 아침까지 이 두 앵커는 `test_interior.py --icegiant` 뒤에
있었고 check.sh 는 그것을 돌리지 않았다 — 천왕성 하나가 1038 초였기 때문이다. 그 플래그마저
낡은 2500 K 선언으로 거절만 찍고 있었으니 지키는 것이 없었다. 같은 날 그 1038 초의 정체가
잡혔다: 상태방정식이 아니라 **층 경계가 걸음 단위로 양자화돼 겉질량이 계단이 되고, 압력
사격이 그 수직면에서 수렴하지 못해 200 회를 같은 중심압에 다시 적분** 하는 것이었다
(`speed-context-notes.md` §6). 경계를 걸음 안에서 보간하자 (§11) 천왕성이 40 초대로
내려왔고, 그래서 앵커가 게이트로 **실제 계산으로** 돌아왔다. 굳힌 파일은 그 계산의
회귀선이다 — 얼음 III·V·VI 상수와 같은 규율로, 값이 마지막 비트까지 같아야 통과하고,
물리를 바꾸는 작업은 `--refresh` 로 다시 굳혀 그 사실을 diff 에 남긴다.

**해왕성 앵커는 커버리지 공백에 기대고 있다 (측정 2026-09-04, 문턱 |Δx/x| ≤ 1e-9 를 실행 전에 기록).**
외피 아래에서도 IF97 창(0.1 GPa 아래 · 500–1000 K 의 물)을 열면 — 목성·토성 둘·천왕성은 비트 동일(그 창이
안 물린다), 해왕성은 **풀이가 사라진다**: ice_x 적합의 1800 K 천장(초이온상)에 걸린다. 읽기: 0.098 GPa · 817 K
의 거절이 해왕성 온도 괄호를 기록된 해로 이끌고, 그 거절을 물리(IF97)로 대체하면 해가 사라지고 다른 벽이
드러난다 — 그 벽은 커버리지 공백이 아니라 진짜 표 한계다. 따라서 해왕성의 기록된 해는 **우리 표의 공백에
의존해 도달된다**: 회귀 앵커로서는 유효하고(재현되고, 바뀌면 잡는다), 물리적 주장으로서는 흔들린다(경로가
우리 무지에 의존한다). 그 해의 반지름 4.210 R⊕ 는 관측 3.86–3.89 보다 +8–9 % 이며 이번 측정으로 안 바뀐 기존
상태다. **창을 닫아 두는 이유는 "닫는 것이 물리적으로 옳아서" 가 아니라 "열면 우리가 평가할 수 없는 영역이
드러나서" 다** — 닫힌 상태를 옳은 상태로 읽지 말 것. 앞선 앵커 이동(2026-09-04 낮)의 원인은 둘 다였다:
`_Steam` 에 붙인 메서드가 getattr 로 외피 경로를 바꾼 것, 그리고 열린 창 자체. 초이온 표현은 C26 으로 등재.

**경로 함수는 주석·docstring 으로 자유롭게 문서화할 수 있다** (2026-09-04, 스스로 만든 제약을 걷어냄). 지문
(`_feed_code`)은 바이트코드·이름·docstring 을 뺀 상수만 본다 — 바뀌는 것은 코드 자체·이름·리터럴 상수·파이썬
버전이지 주석·docstring·행 번호가 아니다. 위 해왕성 기록을 `interior.attempt` 의 docstring 에도 두었고, 그
커밋에서 `--fast` 가 지문 불변을 확인했다.

**게이트가 보는 것 넷.**

1. **전체 풀이가 굳힌 값과 비트까지 같다** — 반지름·C/MR²·중심온도·중심압. 상태방정식,
   페르미 적분, 적분기, 층 쌓기, 사격, 온도 고리 어느 것이 바뀌어도 여기서 걸린다.
2. **격자 위상에 둔감하다** — 수렴점에서 1499 와 1501 걸음으로 적분한 반지름이 1e-5 안.
   계단 결함은 바로 이 검사에 걸린다 (보간 전에는 2e-3 이 흔들렸다). `test_interior.py`
   의 격자 수렴 검사가 지구에서 묻는 것을, 밀도 대비가 큰 얼음/가스 경계에서 묻는다.
3. **격자 수렴** — 1500 → 6000 걸음에서 반지름이 1e-3 안에서 움직인다 (측정: 4.6e-4, 1차 수렴).
4. **발표 C/MR² 과의 거리** (2026-08-31) — 반지름만 `R published` 열이 있었고 C/MR² 은
   자기 자신과만 대조되고 있었다. 발표값(도출값이다 — `PUBLISHED_NMOI` 의 주석이 출처와
   가정을 적는다) 대비 Δ 를 재서 적는다. Δ 에 허용치는 없다; FAIL 을 걸 수 있는 것은
   두 출처가 정규화 환산 뒤 서로 만나는가 하는 전사 검사뿐이다.

`--fast` 는 굳힌 수렴점에서 적분 한 번과 사격 경로의 바이트코드 지문만 본다. 1 초.
전체 풀이 없이 적분기·상태방정식의 변화를 잡는 용도이고, 게이트는 이것을 쓰지 않는다.
**경로 지문은 전체 모드도 대조한다** (2026-09-03) — 값이 그대로여도 경로 함수가 바뀌면 FAIL 이고,
그 커밋에서 `--refresh` 하라고 말한다.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import interior
from eos import PhaseGap
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
PHASE_TOL = 1e-5        # 1499 ↔ 1501 걸음의 반지름 상대차. 계단이면 2e-3 이 나온다
GRID_TOL = 1e-3         # 1500 → 6000 걸음의 반지름 상대차. 측정 4.6e-4
BIT_KEYS = ("radius", "nmoi", "core_temperature", "core_pressure")

# ── 발표 C/MR² — 목성과 같은 규율로 **고르지 않고 조사했다** (2026-08-31) ──────────
#
# 얼음거대행성의 관성모멘트는 측정이 아니다. 발표되는 모든 C/MR² 는 중력장(J₂·J₄,
# Voyager 2 + 위성·고리 천체측량, Jacobson 2007/2009)에 **가정된 자전주기** 아래 맞춘
# 내부구조 모형의 도출값이라, 무엇을 발표값으로 삼느냐가 그 자체로 판단이다. 좌우하는
# 가정은 자전주기다.
#   P_Voy  Voyager 2 전파 주기 — 천왕성 17.24 h (Desch+ 1986), 해왕성 16.11 h
#          (Warwick+ 1989). IAU 자전상수의 기준선.
#   P_HAS  Helled+ 2010 이 동역학 높이·바람을 최소화해 제안한 수정 주기 (16.57 h/17.46 h).
# 이 하나가 발표값을 천왕성 −3.3 %, 해왕성 +6.0 % 움직인다 — 그 폭도 답의 일부다.
#
# 출처 둘, 그리고 정규화 함정 하나.
#   Nettelmann+ 2013 (2013P&SS...77..143N, https://ui.adsabs.harvard.edu/abs/2013P%26SS...77..143N
#     · arXiv:1207.2309) — LM-R EOS 3층 물리 모형. **각주 2 가 λ = I/(M_p R_mean²) 를
#     직접 적는다 — 평균반지름 정규화, 이 파일의 nmoi 와 같은 규약.**
#     P_Voy: 천왕성 0.230(1) · 해왕성 0.2410(8). P_HAS: 0.2224(1) · 0.2555(2).
#   Neuenschwander & Helled 2022 (2022MNRAS.512.3124N,
#     https://ui.adsabs.harvard.edu/abs/2022MNRAS.512.3124N · arXiv:2203.02233) Table 2 —
#     경험적 조각별-폴리트로프(ToF 4차) 해 공간. **§3.6: MoI = I/(M a²), 적도반지름 정규화.**
# 두 정규화는 (a/R_mean)² ≈ 1.6 %(천왕성)/1.2 %(해왕성) 차이 — 두 논문의 자체 밴드보다
# 크므로, 환산 없이 나란히 적으면 가짜 불일치를 만든다 (목성 팩트시트 0.254 와 같은 함정).
# 환산 뒤 두 출처는 0.15 % 안에서 만나고 (최악: 해왕성 P_HAS), 게이트가 그 환산을 매번
# 다시 계산해 전사 오류를 잡는다.
#
# **대조 열은 Nettelmann+ 2013 의 P_Voy 값이다** — 정규화가 우리 구와 같고(비회전 구에는
# 적도반지름이 없다), 불확도가 인쇄된 값이며, IAU 와 같은 자전 가정이다. Δ 자체에는
# 허용치가 없다 — 크면 큰 대로 적는 것이 이 대조의 산출물이다.
PUBLISHED_NMOI = {
    # n13_*: (값, 마지막 자리 불확도) — λ = I/(M R_mean²). nh22_*: Table 2 밴드 — I/(M a²).
    # r_eq_km: NH22 Table 1 의 적도반지름 (P_Voy 행, P_HAS 행 — 해왕성+ 는 24 787 km).
    "Uranus": {"n13_voy": (0.230, 0.001), "n13_has": (0.2224, 0.0001),
               "nh22_voy": (0.22594, 0.22670), "nh22_has": (0.21919, 0.21964),
               "r_eq_km": (25559.0, 25559.0)},
    "Neptune": {"n13_voy": (0.2410, 0.0008), "n13_has": (0.2555, 0.0002),
                "nh22_voy": (0.23727, 0.23900), "nh22_has": (0.25248, 0.25431),
                "r_eq_km": (24766.0, 24787.0)},
}
NMOI_SOURCE_TOL = 5e-3   # 환산 뒤 두 출처가 만나야 하는 거리. 측정 최악 1.5e-3 (해왕성 P_HAS)
R_EARTH_KM = EARTH_RADIUS_M / 1e3


def _fractions(m: float, m_core: float, m_hhe: float) -> tuple[float, float]:
    gmf = m_hhe / m
    return 1.0 - gmf - m_core / m, gmf


def _body(name: str):
    for row in ICE_GIANTS:
        if row[0] == name:
            return row
    raise KeyError(name)


def _solve(name: str):
    _n, m, _r, m_core, m_hhe, t1bar = _body(name)
    imf, gmf = _fractions(m, m_core, m_hhe)
    return solve(m, body_class="ice_giant", core_mass_fraction=0.0,
                 ice_mass_fraction=imf, gas_mass_fraction=gmf,
                 potential_temperature=t1bar)


def _standalone(name: str, p_center_pa: float, t_center: float):
    """수렴점에서 적분 한 번. 풀이의 마지막 적분과 같은 인자다."""
    _n, m, _r, m_core, m_hhe, t1bar = _body(name)
    imf, gmf = _fractions(m, m_core, m_hhe)
    return integrate(p_center_pa, m * EARTH_MASS_KG, 0.0, imf, "fe_prem", gmf=gmf,
                     t_center=t_center, t_pot=t1bar)


def _radius_at_steps(name: str, p_center_pa: float, t_center: float, steps: int) -> float:
    base = interior.STEPS
    try:
        interior.STEPS = steps
        return _standalone(name, p_center_pa, t_center).radius_m / EARTH_RADIUS_M
    finally:
        interior.STEPS = base


# ── 경로 지문 (--fast) ──────────────────────────────────────────────────

# 굳힌 수렴점으로 가는 길을 정하는 것들. `--fast` 가 적분 한 번으로 못 보는 바깥 고리다.
PATH_FUNCTIONS = ("solve", "shoot", "_shoot_pressure", "_narrow_bracket",
                  "_surface_temperature_met", "_stack", "integrate")
PATH_CONSTANTS = ("STEPS", "INTERPOLATE_LAYERS", "MAX_STEPS", "SHOOT_ITERS", "SHOOT_TOL",
                  "T_PASSES", "T_TOL", "T_SURFACE_TOL", "T_BRACKET_TRIES", "NARROW_ITERS",
                  "NARROW_RATIO", "FLUID_CLASSES", "ICE_GIANT_CLASSES")


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

def _structure_record(st) -> dict:
    return {"radius_earth": repr(st.radius_m / EARTH_RADIUS_M),
            "mass_kg": repr(st.mass_kg), "moi": repr(st.moi), "nmoi": repr(st.nmoi),
            "t_surface": repr(st.t_surface), "core_radius_m": repr(st.core_radius_m)}


def _record(name: str, res, seconds: float) -> dict:
    _n, _m, r_pub, _mc, _mh, t1bar = _body(name)
    rec = {"seconds": round(seconds, 1), "regime": res.regime, "applicable": res.applicable,
           "converged": res.converged, "grade": res.grade, "t_1bar_k": t1bar,
           "r_published_earth": r_pub}
    if not res.applicable:
        rec["reason"] = res.reason
        return rec
    v = res.values
    rec["values"] = {k: (repr(x) if isinstance(x, float) else x) for k, x in v.items()}
    p_pa = v["core_pressure"] * 1e9
    st = _standalone(name, p_pa, v["core_temperature"])
    rec["standalone"] = {"p_center_pa": repr(p_pa), "t_center": repr(v["core_temperature"]),
                         **_structure_record(st)}
    rec["standalone_reproduces_solve"] = rec["standalone"]["radius_earth"] == repr(v["radius"])
    return rec


def refresh() -> int:
    out = {"python": platform.python_version(), "path_fingerprint": path_fingerprint(),
           "frozen_at": time.strftime("%Y-%m-%d"), "steps": interior.STEPS, "bodies": {}}
    for name, _m, r_pub, _mc, _mh, _t in ICE_GIANTS:
        print(f"{name} — 전체 풀이 …", flush=True)
        t0 = time.perf_counter()
        res = _solve(name)
        rec = _record(name, res, time.perf_counter() - t0)
        if res.applicable:
            v = res.values
            print(f"  {rec['seconds']:.0f} s · R {v['radius']:.4f} R⊕ "
                  f"({(v['radius'] / r_pub - 1) * 100:+.2f} %) · T_c {v['core_temperature']:.0f} K "
                  f"· converged={res.converged}")
        else:
            print(f"  {rec['seconds']:.0f} s · 거절 — {res.reason[:90]}")
        out["bodies"][name] = rec
    ANCHOR_FILE.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"굳혔다 → {ANCHOR_FILE.name}")
    return 0


def table() -> None:
    """문서의 얼음거대행성 표. 굳힌 파일에서 낸다 — 전체 풀이를 다시 돌리지 않는다."""
    frozen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    print("| planet | T at 1 bar | R derived | R published | Δ | C/MR² | C/MR² published | Δ | "
          "T_c | P_c | converged | grade |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name, rec in frozen["bodies"].items():
        r_pub = rec["r_published_earth"]
        if not rec["applicable"]:
            print(f"| {name} | {rec['t_1bar_k']:.0f} K | declined | {r_pub:.3f} R⊕ | – | – | – | – "
                  f"| – | – | – | – |")
            continue
        v = {k: float(rec["values"][k]) for k in BIT_KEYS}
        n_pub, n_unc = PUBLISHED_NMOI[name]["n13_voy"]
        print(f"| {name} | {rec['t_1bar_k']:.0f} K | {v['radius']:.3f} R⊕ | {r_pub:.3f} R⊕ | "
              f"{(v['radius'] / r_pub - 1) * 100:+.2f} % | {v['nmoi']:.4f} | "
              f"{n_pub:.4f}±{n_unc:g} | {(v['nmoi'] / n_pub - 1) * 100:+.1f} % | "
              f"{v['core_temperature']:.0f} K | {v['core_pressure']:.0f} GPa | "
              f"{rec['converged']} | {rec['grade']} |")
    print("\nC/MR² published: Nettelmann+ 2013 (2013P&SS...77..143N), Voyager 자전주기, "
          "λ = I/(M R_mean²) — 상수 블록 PUBLISHED_NMOI 의 주석이 근거다.")


# ── 게이트 ──────────────────────────────────────────────────────────────

def _published_nmoi(frozen: dict, fails: list[str]) -> None:
    """발표 C/MR² 대조 — 굳힌 값에서 Δ 를 재고, 두 출처의 정합을 환산으로 다시 계산한다.

    FAIL 을 걸 수 있는 것은 출처 정합(두 논문이 적도→평균 환산 뒤 서로 만나는가 — 전사
    검사)뿐이다. Δ 자체에는 허용치가 없다: 재고 적는 것까지가 이 대조다."""
    print("\n발표 C/MR² — J₂+자전주기에 맞춘 모형의 도출값 vs 우리 구 (비회전, R_mean 정규화)")
    for name, rec in frozen["bodies"].items():
        if not rec["applicable"]:
            continue
        pub = PUBLISHED_NMOI[name]
        nmoi, r_der = float(rec["values"]["nmoi"]), float(rec["values"]["radius"])
        r_pub = rec["r_published_earth"]
        voy, has = pub["n13_voy"][0], pub["n13_has"][0]
        renorm = nmoi * (r_der / r_pub) ** 2      # I/(M·R_발표²) — 반지름 몫을 걷어낸 값
        print(f"  {name}: 도출 {nmoi:.4f} vs 발표 {voy:.4f}±{pub['n13_voy'][1]:g} "
              f"(Nettelmann+ 2013, P_Voy, R_mean) → **{(nmoi / voy - 1) * 100:+.1f} %** "
              f"· P_HAS {has:.4f} 대비 {(nmoi / has - 1) * 100:+.1f} %")
        print(f"         반지름 몫(도출 R {(r_der / r_pub - 1) * 100:+.2f} %)을 걷어내면 "
              f"I/(M·R_발표²) = {renorm:.4f} → {(renorm / voy - 1) * 100:+.1f} % — "
              f"반지름이 설명 못 하는 나머지다. 기록, 판정 없음")
        # 출처 정합 — NH22 의 적도 정규화 밴드를 (a/R_mean)² 로 평균 정규화로 환산하면
        # N13 의 값과 만나야 한다. 전사(자릿수·반지름) 오류는 여기서 0.5 % 를 훌쩍 넘긴다.
        r_mean_km = r_pub * R_EARTH_KM
        worst = 0.0
        for (lam, _unc), band, a_km in ((pub["n13_voy"], pub["nh22_voy"], pub["r_eq_km"][0]),
                                        (pub["n13_has"], pub["nh22_has"], pub["r_eq_km"][1])):
            f_conv = (a_km / r_mean_km) ** 2
            lo, hi = band[0] * f_conv, band[1] * f_conv
            dist = 0.0 if lo <= lam <= hi else min(abs(lam - lo), abs(lam - hi)) / lam
            worst = max(worst, dist)
        ok = worst < NMOI_SOURCE_TOL
        if not ok:
            fails.append(f"{name}: 발표 C/MR² 의 두 출처가 정규화 환산 뒤에도 {worst * 100:.2f} % "
                         "떨어져 있다 — 전사나 환산 반지름을 의심하라")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — Neuenschwander & Helled 2022 밴드를 "
              f"(a/R_mean)² 환산하면 Nettelmann+ 2013 과 {worst * 100:.2f} % 거리 "
              f"(< {NMOI_SOURCE_TOL * 100:.1f} %; 두 자전 가정 모두)")


def _fingerprint(frozen: dict, fails: list[str], full: bool) -> None:
    """경로 지문 대조. 두 모드 다 본다 (2026-09-03, Brief 39 감사 ⑤).

    2026-09-02 까지 이 대조는 `--fast` 에만 있었고 게이트는 전체 모드를 돌린다 — 그래서
    "경로 함수를 고치면 같은 커밋에서 --refresh" 라는 규칙은 아무도 돌리지 않는 모드가
    지키고 있었다. Brief 36 (9ff07deb) 이 `_stack`·`integrate`·`solve` 를 고치고 값은 비트까지
    확인했지만 지문은 갱신하지 않았고, 하루 동안 규칙과 게이트가 어긋난 채 아무도 못 봤다.
    전체 모드에서는 값이 맞아도 지문이 다르면 FAIL 이고, 메시지가 할 일을 말한다: 이 커밋에서
    `--refresh`. 값이 움직였다면 그것은 아래 전체 풀이 대조가 따로 잡는다."""
    fp_now, fp_then = path_fingerprint(), frozen["path_fingerprint"]
    ok = fp_now == fp_then
    if not ok:
        fails.append("사격·온도 고리·적분기의 경로 지문이 굳힐 때와 다르다 — "
                     + ("값이 그대로여도 경로 함수가 바뀐 것이니 **이 커밋에서 `--refresh`** 로 "
                        "다시 굳혀 diff 에 남겨라" if full else
                        "수렴점이 옮겨갔을 수 있다. 전체 풀이(기본 실행)나 `--refresh` 로 확인하라"))
    print(f"  [{'PASS' if ok else 'FAIL'}] 경로 지문 {fp_then} "
          f"{'그대로' if ok else '→ ' + fp_now + ' (바뀜)'} — "
          f"{', '.join(PATH_FUNCTIONS)} + 상수 {len(PATH_CONSTANTS)}개")


def _fast(frozen: dict, fails: list[str]) -> None:
    """적분 한 번 + 경로 지문. 전체 풀이 없이 적분기·상태방정식의 변화를 잡는다."""
    _fingerprint(frozen, fails, full=False)
    for name, rec in frozen["bodies"].items():
        if not rec["applicable"]:
            print(f"  [FROZEN] {name} — 거절이 앵커다. 굳힌 이유: {rec['reason'][:70]}…")
            continue
        sa = rec["standalone"]
        t0 = time.perf_counter()
        st = _standalone(name, float(sa["p_center_pa"]), float(sa["t_center"]))
        dt = time.perf_counter() - t0
        now = _structure_record(st)
        moved = [k for k in ("radius_earth", "mass_kg", "moi", "t_surface") if now[k] != sa[k]]
        if moved:
            fails.append(f"{name}: 굳힌 수렴점에서 적분이 다른 값을 낸다 — "
                         + ", ".join(f"{k} {sa[k]} → {now[k]}" for k in moved))
        print(f"  [{'FAIL' if moved else 'PASS'}] {name} — 수렴점에서 적분 한 번 {dt:.1f} s: "
              f"{'움직였다: ' + ', '.join(moved) if moved else '반지름·질량·관성모멘트·표면온도 비트까지 같다'}")
    print("  [SKIP] --fast 는 전체 풀이를 돌리지 않는다. 게이트(기본 실행)가 돌린다")
    _declarations(frozen, fails)


def _declarations(frozen: dict, fails: list[str]) -> None:
    """C5 의 두 선언이 수렴점 적분을 예상한 방향으로 움직이는가 — 그리고 0 이면 안 움직이는가.

    열경계층 점프는 외피 바닥을 그만큼 식히므로 이 시험 중심 온도로는 표의 온도 바닥 아래로
    떨어져 **온도가 막은 것으로** 던져야 하고(사격이 중심 온도를 올린다), 맨틀 암석은 맨틀을
    조밀하게 해 같은 중심압에서 겉질량이 모자라야 한다. 풀이는 여기서 안 돌린다 — 그 표는
    interior-core.md C5 행에 있다."""
    print("\n선언 둘 (C5) — 수렴점 적분이 예상한 방향으로 움직이는가")
    rec = frozen["bodies"]["Neptune"]
    if not rec["applicable"]:
        return
    sa = rec["standalone"]
    _n, m, _r, m_core, m_hhe, t1bar = _body("Neptune")
    imf, gmf = _fractions(m, m_core, m_hhe)
    base = _standalone("Neptune", float(sa["p_center_pa"]), float(sa["t_center"]))
    got = None
    try:
        integrate(float(sa["p_center_pa"]), m * EARTH_MASS_KG, 0.0, imf, "fe_prem", gmf=gmf,
                  t_center=float(sa["t_center"]), t_pot=t1bar, boundary_temperature_jump=2500.0)
    except PhaseGap as gap:
        got = gap
    ok = got is not None and got.too_cold
    if not ok:
        fails.append("열경계층 2500 K 가 수렴점에서 온도가 막은 것으로 던지지 않는다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 열경계층 2500 K → 외피가 표 바닥 아래로 떨어져 too_cold 로 던진다"
          + (f" ({got.temperature_k:.0f} K)" if got is not None and got.temperature_k else ""))
    st = integrate(float(sa["p_center_pa"]), m * EARTH_MASS_KG, 0.0, imf, "fe_prem", gmf=gmf,
                   t_center=float(sa["t_center"]), t_pot=t1bar, mantle_rock_fraction=0.2)
    ok = st.mass_kg < base.mass_kg and st.radius_m < base.radius_m
    if not ok:
        fails.append(f"맨틀 암석 0.2 가 같은 중심압에서 맨틀을 조밀하게 하지 않는다 — "
                     f"질량 {st.mass_kg / base.mass_kg:.4f}, 반지름 {st.radius_m / base.radius_m:.4f}")
    print(f"  [{'PASS' if ok else 'FAIL'}] 맨틀 암석 0.2 → 같은 중심압에서 겉질량 "
          f"{st.mass_kg / base.mass_kg:.3f} 배, 반지름 {st.radius_m / base.radius_m:.3f} 배")


def _live(frozen: dict, fails: list[str]) -> None:
    for name, rec in frozen["bodies"].items():
        t0 = time.perf_counter()
        res = _solve(name)
        dt = time.perf_counter() - t0
        if not rec["applicable"]:
            same = (not res.applicable) and res.reason == rec["reason"]
            if not same:
                fails.append(f"{name}: 굳힌 것은 거절인데 지금은 "
                             f"{'다른 이유로 거절한다' if not res.applicable else '풀린다'} — "
                             "의도한 변화면 --refresh")
            print(f"  [{'PASS' if same else 'FAIL'}] {name} — 거절이 앵커다 ({dt:.0f} s): "
                  f"{rec['reason'][:70]}…")
            continue
        if not res.applicable:
            fails.append(f"{name}: 풀려야 하는데 거절했다 — {res.reason[:80]}")
            print(f"  [FAIL] {name} 거절됨 ({dt:.0f} s)")
            continue
        v = res.values
        moved = [k for k in BIT_KEYS if repr(v[k]) != rec["values"][k]]
        if moved:
            fails.append(f"{name}: 전체 풀이가 굳힌 값과 다르다 — "
                         + ", ".join(f"{k} {rec['values'][k]} → {v[k]!r}" for k in moved)
                         + ". 의도한 변화면 `--refresh` 로 다시 굳혀 diff 에 남겨라")
        if not res.converged:
            fails.append(f"{name}: converged=False")
        r_pub = rec["r_published_earth"]
        print(f"  [{'FAIL' if moved or not res.converged else 'PASS'}] {name} — 전체 풀이 {dt:.0f} s"
              f" (굳힐 때 {rec['seconds']:.0f} s): "
              f"{'움직였다: ' + ', '.join(moved) if moved else '반지름·C/MR²·중심온도·중심압 비트까지 같다'}")
        print(f"         R {v['radius']:.4f} R⊕ vs 발표 {r_pub:.4f} ({(v['radius'] / r_pub - 1) * 100:+.2f} %) "
              f"· C/MR² {v['nmoi']:.4f} · T_c {v['core_temperature']:.0f} K "
              f"· P_c {v['core_pressure']:.0f} GPa · converged={res.converged}")

        # 격자 위상과 격자 수렴 — 수렴점에서 적분만 다시 한다 (사격은 안 돈다).
        p_pa, t_c = v["core_pressure"] * 1e9, v["core_temperature"]
        base = interior.STEPS
        r_lo = _radius_at_steps(name, p_pa, t_c, base - 1)
        r_hi = _radius_at_steps(name, p_pa, t_c, base + 1)
        r_4x = _radius_at_steps(name, p_pa, t_c, base * 4)
        phase = abs(r_hi - r_lo) / v["radius"]
        drift = abs(r_4x - v["radius"]) / r_4x
        ok = phase < PHASE_TOL
        if not ok:
            fails.append(f"{name}: 격자 위상 {base - 1} ↔ {base + 1} 에서 반지름이 {phase:.1e} "
                         "움직인다 — 걸음 안의 경계가 다시 양자화됐다 (계단)")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — 격자 위상 {base - 1} ↔ {base + 1}: "
              f"반지름 상대차 {phase:.1e} (< {PHASE_TOL:.0e}; 계단이면 ~2e-3)")
        ok = drift < GRID_TOL
        if not ok:
            fails.append(f"{name}: 격자 {base} → {base * 4} 에서 반지름이 {drift:.1e} 움직인다")
        print(f"  [{'PASS' if ok else 'FAIL'}] {name} — 격자 {base} → {base * 4}: "
              f"반지름 상대차 {drift:.1e} (< {GRID_TOL:.0e}; 발표값과의 차 "
              f"{abs(v['radius'] / r_pub - 1):.1e} 의 {abs(v['radius'] / r_pub - 1) / max(drift, 1e-12):.0f} 분의 1)")


def _clamp_invariance(frozen: dict, fails: list[str]) -> None:
    """교란-불변 회귀 (브리프 34 항목 B, A2 의 V1+ 를 게이트로 승격 — 게이트 +22 s, 1205 s 의
    2 % 라 승격이 쌈). 주장은 세상이 아니라 우리 코드에 대한 것이다: **천왕성의 수렴한 해는
    초이온 예측 구역(P > 355 GPa · 0 < T < 1800 K — French+ 2016 Fig. 4 의 경계가 우리 1800 K
    천장 아래로 지나간 곳)의 ice_x 값에 무관하다.** 구역 밀도를 +5 % 밀고 전체를 다시 풀어
    굳힌 앵커와 비트 대조한다 — A2(2026-09-01)에서 ±5 %(발화 1,754회)와 첫-접촉 거절이 전부
    비트 동일이었다. 이 검사가 깨지는 날은 솔버 변경이 그 무관함을 깨뜨린 날이고, 그때 C6 의
    상시 감시가 다시 열린다. 범위 제한: 현 로스터의 천왕성에 대한 실측이지 일반 보증이 아니다."""
    import eos as _eos
    h2o = _eos.MATERIALS["h2o"]
    cls = type(h2o)
    orig = cls.density

    def bumped(self, p, t=0.0, t_pot=0.0):
        if (self is h2o and p > 355e9 and 0.0 < t < 1800.0
                and getattr(self.phase_at(p), "name", "") == "ice_x"):
            return orig(self, p, t, t_pot) * 1.05
        return orig(self, p, t, t_pot)

    name = "Uranus"
    rec = frozen["bodies"][name]
    cls.density = bumped
    try:
        t0 = time.perf_counter()
        res = _solve(name)
        dt = time.perf_counter() - t0
    finally:
        cls.density = orig
    if not res.applicable:
        fails.append(f"교란-불변: {name} 이 구역 교란에서 거절됐다 — {res.reason[:80]}")
        print(f"  [FAIL] 교란-불변 — 거절 ({dt:.0f} s)")
        return
    moved = [k for k in BIT_KEYS if repr(res.values[k]) != rec["values"][k]]
    ok = not moved and res.converged
    if not ok:
        fails.append("교란-불변이 깨졌다 — 수렴한 해가 초이온 예측 구역의 ice_x 값에 의존하기 "
                     "시작했다: " + (", ".join(moved) if moved else "converged=False")
                     + ". 무엇이 시험 회랑의 결과를 답에 연결했는지 추적하라 (브리프 34 A2)")
    print(f"  [{'PASS' if ok else 'FAIL'}] 교란-불변 ({dt:.0f} s): 구역(>355 GPa · <1800 K) 밀도 +5 % "
          f"에서도 천왕성 해가 앵커와 비트 동일 — 수렴한 해는 그 구역에 무관 (A2, 브리프 34)")


def main() -> int:
    if "--refresh" in sys.argv:
        return refresh()
    if "--table" in sys.argv:
        table()
        return 0

    fails: list[str] = []
    if not ANCHOR_FILE.exists():
        print(f"  [FAIL] {ANCHOR_FILE.name} 이 없다 — `--refresh` 로 굳혀라")
        return 1
    frozen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    print("얼음거대행성 앵커 — 천왕성·해왕성이 굳힌 값을 비트까지 다시 내는가")
    print(f"  굳힌 날 {frozen['frozen_at']} · python {frozen['python']} · {frozen.get('steps')} 걸음")
    if "--fast" in sys.argv:
        _fast(frozen, fails)
    else:
        _fingerprint(frozen, fails, full=True)
        _live(frozen, fails)
        _clamp_invariance(frozen, fails)
    _published_nmoi(frozen, fails)

    if fails:
        print(f"\n실패 {len(fails)}건")
        for f in fails:
            print(f"  · {f}")
        return 1
    print("\n모두 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
