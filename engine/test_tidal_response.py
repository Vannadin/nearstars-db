# 조석 응답 노드의 앵커 — 균질구 고전해 재현, 지구 탄성 Love 수, 층 사상의 덮음·거절, 밴드 (C62 (b))
"""Anchor the tidal-response node (C62 (b)).

    python3 engine/test_tidal_response.py

1. **J0 — the wiring check, and it is the strongest one here.** Shrink the core until the stack is one
   uniform density and the propagator must reproduce the closed form a held paper prints for a
   homogeneous body — Bagheri+ 2022 eqs (56)(57), `k̄_n = [3/(2(n−1))] / (1 + B_n/J̄)` with
   `B_n = (2n² + 4n + 3)/(n g ρ R)`, which at n = 2 and `J̄ = 1/μ` is `1.5 / (1 + 19μ/(2ρgR))`.
   ⚠ *The formula is cited, not remembered.* Saito's start vectors, Beuthe's six ODEs, the surface
   conditions and eq. (7) all have to be right for that to come out; it holds to **4e-5 relative** at
   three rigidities.
2. **J1 — Earth, elastic.** A two-layer Earth against Wahr 1981's `k₀ = 0.302`, `h₀ = 0.609` (PEM-C).
   ⚠ **Report only.** Two homogeneous layers are not PEM-C, and the printed pair is reproduced at a
   mantle rigidity this test prints rather than at one it tuned.
3. **The layer map.** The mantle's top is the **minimum** of the existing upper boundaries, so an ocean
   body does not get its ocean double-covered; the coverage check catches a planted overlap, which no
   name-based refusal can see.
4. **Refusals, each by name** — a solid core (start values in an unheld paper), an ocean under an ice
   shell (eq. 27 is for a fluid layer reaching the surface), a declared layer the solve does not have,
   a solved layer nothing declared, an ice fraction with no ice boundary, a missing viscosity.
5. **The band.** Three rheologies are emitted and none is elected; a member whose parameters are absent
   is named and the others still publish.
6. **J8/J9 and the identity.** `g_surface_identity` is an arithmetic identity and is pinned as one;
   `homogeneous_nmoi` is printed beside the structure recipe's value as the size of the approximation.
"""
from __future__ import annotations

import math
import sys

import tidal_response as tr

R_EARTH = 6.371e6
M_EARTH = 5.9722e24
R_CORE = 3.480e6
CMF_EARTH = 0.325

#: Wahr 1981, body text (M₂ tide, model PEM-C, rotation and ellipticity included).
WAHR_K2, WAHR_H2 = 0.302, 0.609

#: Earth's measured normalized moment of inertia — J9 compares the homogeneous stack against it.
EARTH_NMOI = 0.3307


def _earth(mu_pa: float, **extra) -> list[tr.Layer]:
    mantle = {"name": "mantle", "state": "solid", "mu_pa": mu_pa}
    mantle.update(extra)
    return tr.build_layers(radius_m=R_EARTH, core_radius_m=R_CORE, mass_kg=M_EARTH,
                           cmf=CMF_EARTH, imf=0.0,
                           declared=[{"name": "core", "state": "liquid"}, mantle])


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    def refuses(fn, needle: str, msg: str) -> None:
        try:
            fn()
        except tr.Refusal as exc:
            ok(needle in str(exc), f"{msg} — 거절은 났는데 이유가 다르다: {exc}")
        else:
            fails.append(f"{msg} — 거절하지 않았다")

    print("조석 응답 (C62 (b)) — J0: 거의 균질한 몸에서 균질 비압축 구의 고전해를 재현하는가")
    rho_bar = M_EARTH / (4 / 3 * math.pi * R_EARTH ** 3)
    g_bar = tr.G * M_EARTH / R_EARTH ** 2

    def bagheri_k(n: int, mu: float) -> float:
        """Bagheri+ 2022 식 (56)(57) — 균질 몸의 **k̄ₙ**, 탄성이면 J̄ = 1/μ."""
        b_n = (2 * n * n + 4 * n + 3) / (n * g_bar * rho_bar * R_EARTH)
        return 3.0 / (2.0 * (n - 1)) / (1.0 + b_n * mu)

    def kelvin_love_h(mu: float) -> float:
        """Beuthe 2015 의 Kelvin-Love 식 — 균질 몸의 **h₂**, μ̂ = μ/(ρgR)."""
        mu_hat = mu / (rho_bar * g_bar * R_EARTH)
        return 2.5 / (1.0 + 9.5 * mu_hat)
    worst = worst_h = 0.0
    for mu in (1e10, 5e10, 1.45e11):
        rc = 0.02 * R_EARTH
        layers = tr.build_layers(radius_m=R_EARTH, core_radius_m=rc, mass_kg=M_EARTH,
                                 cmf=(rc / R_EARTH) ** 3, imf=0.0,
                                 declared=[{"name": "core", "state": "liquid"},
                                           {"name": "mantle", "state": "solid", "mu_pa": mu}])
        e = tr.elastic_love(layers)
        want, want_h = bagheri_k(2, mu), kelvin_love_h(mu)
        rel = abs(e["k2"] / want - 1.0)
        rel_h = abs(e["h2"] / want_h - 1.0)
        worst, worst_h = max(worst, rel), max(worst_h, rel_h)
        print(f"  μ {mu:.1e} Pa → k₂ {e['k2']:.5f} · Bagheri (56)(57) {want:.5f} ({rel:.1e}) · "
              f"h₂ {e['h2']:.5f} · Kelvin-Love {want_h:.5f} ({rel_h:.1e})")
    ok(abs(bagheri_k(2, 1.45e11) * (1.0 + 19.0 * 1.45e11 / (2.0 * rho_bar * g_bar * R_EARTH))
           - 1.5) < 1e-12,
       "식 (57) 의 B_n 이 n = 2 에서 19/(2ρgR) 로 떨어져야 한다 — 인쇄된 일반형을 "
       "손으로 특수화한 자리라 되짚어 둔다")
    ok(worst_h < 1e-4,
       f"J0-h: 균질 극한에서 Beuthe 의 Kelvin-Love h₂ 를 1e-4 안에서 재현해야 한다 — "
       f"최악 {worst_h:.2e}")
    # ⚠ **love_ratio_identity — 물리 검사가 아니라 산술 항등식이다.** 두 인쇄 형식이
    #   분모 (1 + 19μ̂/2) 를 공유하므로 비는 구조상 3/5 다. 이 줄이 잡는 것은 «우리 구현이
    #   두 양을 같은 분모에서 냈는가» 뿐이고, 1e-12 는 그래서 여기에만 쓴다 — 인쇄값 대
    #   우리 값의 물리 검사는 위의 1e-4 쪽이다.
    ratio_elastic = tr.elastic_love(_earth(2.0e11))
    ok(abs(bagheri_k(2, 1.45e11) / kelvin_love_h(1.45e11) - 0.6) < 1e-12,
       "love_ratio_identity: 인쇄된 두 형식의 비가 3/5 여야 한다 (분모 공유, 산술 항등식)")
    ok(abs(ratio_elastic["k2"] / ratio_elastic["h2"] - 0.6) < 5e-2,
       f"love_ratio_identity: 두 층 지구에서는 3/5 에서 벗어나는 것이 정상이다 — "
       f"균질 극한의 항등식이지 모든 구조의 성질이 아니다 "
       f"(측정 {ratio_elastic['k2'] / ratio_elastic['h2']:.4f})")
    ok(worst < 1e-4,
       f"J0: 균질 극한에서 인쇄된 닫힌 형식(Bagheri 식 56·57)을 1e-4 안에서 재현해야 한다 — "
       f"최악 {worst:.2e}. "
       f"이 하나가 Saito 출발 벡터·Beuthe 여섯 ODE·표면 조건·식 (7) 을 한꺼번에 문다")

    print("\nJ1 — 지구 두 층의 탄성 Love 수 (보고만, 맞추지 않는다)")
    for mu in (1.45e11, 2.0e11, 2.1e11):
        e = tr.elastic_love(_earth(mu))
        print(f"  μ {mu:.2e} Pa → k₂ {e['k2']:.4f} (Wahr {WAHR_K2}, {e['k2']/WAHR_K2-1:+.1%}) · "
              f"h₂ {e['h2']:.4f} (Wahr {WAHR_H2}, {e['h2']/WAHR_H2-1:+.1%})")
    base = tr.elastic_love(_earth(2.0e11))
    ok(0.2 < base["k2"] < 0.45,
       f"J1: 지구 두 층의 k₂ 는 Wahr 근처 자리에 있어야 한다 — {base['k2']:.4f}")
    ok(base["h2"] > base["k2"],
       "J1: h₂ 는 k₂ 보다 커야 한다 — 인쇄된 두 값의 순서다")
    # ⚠ **맞춘 것이 아니라 인쇄한 것이다.** 두 층 균질 모형은 PEM-C 가 아니므로 μ 를 움직여
    #   0.302 에 대는 것은 조정이다. 위 세 줄은 그 셋을 나란히 인쇄만 한다.

    print("\n층 사상 — 맨틀 위쪽은 «존재하는 상위 경계 중 최소»")
    ocean = tr.build_layers(
        radius_m=R_EARTH, core_radius_m=R_CORE, mass_kg=M_EARTH, cmf=0.2, imf=0.1,
        declared=[{"name": "core", "state": "liquid"},
                  # ⚠ 점성을 넣어 둔다. 없으면 맨틀이 먼저 «점성 미선언» 으로 거절해서
                  #   바다 거절이 발화하기 전에 멈춘다 — 시험이 엉뚱한 문장을 물게 된다.
                  {"name": "mantle", "state": "solid", "mu_pa": 1e11, "eta_pa_s": 1e21},
                  {"name": "ocean", "state": "liquid"},
                  {"name": "ice_shell", "state": "solid", "mu_pa": 3.5e9, "eta_pa_s": 1e14}],
        ocean_m=100e3, ice_shell_m=30e3)
    names = [lay.name for lay in ocean]
    ok(names == ["core", "mantle", "ocean", "ice_shell"],
       f"층이 안쪽부터 정렬돼야 한다 — {names}")
    mantle_top = [lay for lay in ocean if lay.name == "mantle"][0].r_outer
    ocean_base = [lay for lay in ocean if lay.name == "ocean"][0].r_inner
    ok(abs(mantle_top - ocean_base) < 1.0,
       f"맨틀 꼭대기가 바다 바닥이어야 한다 — 맨틀 {mantle_top:.0f} m, 바다 {ocean_base:.0f} m. "
       f"«지각 바닥 아니면 표면» 규칙이면 맨틀이 표면까지 올라가 바다와 껍질을 두 번 덮는다")
    ok(abs(sum(lay.mass for lay in ocean) / M_EARTH - 1.0) < 1e-12,
       "층 질량의 합이 천체 질량이어야 한다")

    print("  덮음 검사 — 겹침을 심으면 잡히는가")
    refuses(lambda: tr._check_coverage(
        {"core": (0.0, R_CORE), "mantle": (R_CORE, R_EARTH), "crust": (R_CORE * 0.9, R_EARTH)},
        R_EARTH), "overlap",
        "겹친 구간은 잡혀야 한다 — 전파자가 두 번 적분하고 이름 거절로는 안 보인다")
    refuses(lambda: tr._check_coverage(
        {"core": (0.0, R_CORE), "mantle": (R_CORE * 1.1, R_EARTH)}, R_EARTH), "gap",
        "빈틈도 잡혀야 한다")

    print("\n이름 붙은 거절 여섯")
    refuses(lambda: tr.elastic_love(tr.build_layers(
        radius_m=R_EARTH, core_radius_m=R_CORE, mass_kg=M_EARTH, cmf=CMF_EARTH, imf=0.0,
        declared=[{"name": "core", "state": "solid", "mu_pa": 1.6e11},
                  {"name": "mantle", "state": "solid", "mu_pa": 1e11}])),
        "Takeuchi & Saito 1972",
        "고체 핵은 출발해가 미보유 논문에 있다고 말해야 한다")
    refuses(lambda: tr.solve_response(ocean, forcing_period_s=3600.0), "reaches the",
        "껍질 아래 바다는 식 (27) 의 적용 조건을 말하며 거절해야 한다")
    refuses(lambda: tr.build_layers(
        radius_m=R_EARTH, core_radius_m=R_CORE, mass_kg=M_EARTH, cmf=CMF_EARTH, imf=0.0,
        declared=[{"name": "core", "state": "liquid"},
                  {"name": "mantle", "state": "solid", "mu_pa": 1e11},
                  {"name": "ocean", "state": "liquid"}]),
        "declared but absent",
        "선언에만 있는 층은 이름으로 거절해야 한다")
    refuses(lambda: tr.build_layers(
        radius_m=R_EARTH, core_radius_m=R_CORE, mass_kg=M_EARTH, cmf=CMF_EARTH, imf=0.0,
        declared=[{"name": "core", "state": "liquid"}]),
        "no tidal declaration",
        "풀이에만 있는 층도 이름으로 거절해야 한다")
    refuses(lambda: tr.build_layers(
        radius_m=R_EARTH, core_radius_m=R_CORE, mass_kg=M_EARTH, cmf=0.3, imf=0.1,
        declared=[{"name": "core", "state": "liquid"},
                  {"name": "mantle", "state": "solid", "mu_pa": 1e11}]),
        "no radius boundary",
        "얼음 분율이 있는데 경계 반지름이 없으면 거절해야 한다 — 전부 언 기둥은 "
        "맨틀 사상이 조용히 삼킨다")
    refuses(lambda: tr.complex_mu(_earth(1e11)[1], 1e-4, "maxwell"),
        "viscosity is not declared",
        "점성이 없으면 세 레올로지가 다 못 선다고 말해야 한다")

    print("\n밴드 — 셋을 다 내고 고르지 않는다")
    full = _earth(1.45e11, eta_pa_s=1e21, andrade_alpha=0.3, andrade_zeta=1.0,
                  sc_delta_j=1.0, sc_tau=1e4)
    band = tr.solve_response(full, forcing_period_s=12.42 * 3600)
    ok(sorted(band["members"]) == sorted(tr.RHEOLOGIES),
       f"셋이 다 나와야 한다 — {sorted(band['members'])}")
    ok(not band["refused"], f"거절이 없어야 한다 — {band['refused']}")
    for rh in tr.RHEOLOGIES:
        m = band["members"][rh]
        print(f"  {rh:16s} k₂ {abs(m['k2']):.4f} · Q {m['q']:.4g}")
    lo, hi = band["k2_band"]
    ok(lo <= hi and lo > 0.0, f"밴드는 정렬돼 있어야 한다 — {band['k2_band']}")
    ok(band["k2_over_q_band"] is not None and band["k2_over_q_band"][0] > 0.0,
       "k₂/Q 밴드가 나와야 한다")

    partial = _earth(1.45e11, eta_pa_s=1e21)      # Andrade·S–C 의 매개변수가 없다
    pb = tr.solve_response(partial, forcing_period_s=12.42 * 3600)
    ok(pb["rheology_members_emitted"] == ["maxwell"],
       f"매개변수가 없는 멤버는 빠지고 나머지는 나와야 한다 — {pb['rheology_members_emitted']}")
    ok(set(pb["refused"]) == {"andrade", "sundberg_cooper"},
       f"빠진 둘은 이름이 적혀야 한다 — {sorted(pb['refused'])}")

    print("\n몸 전체 정적 한계의 등록 귀결 — 주기는 μ̃(ω) 로만 들어온다")
    stiff = _earth(1.45e11, eta_pa_s=1e30, andrade_alpha=0.3, andrade_zeta=1.0,
                   sc_delta_j=1.0, sc_tau=1e4)
    k_short = tr.solve_response(stiff, forcing_period_s=3600.0)["members"]["maxwell"]["k2"]
    k_long = tr.solve_response(stiff, forcing_period_s=86400.0)["members"]["maxwell"]["k2"]
    k_elastic = tr.elastic_love(stiff)["k2"]
    print(f"  η 1e30 Pa·s → k₂ (1 h) {abs(k_short):.6f} · k₂ (24 h) {abs(k_long):.6f} · "
          f"탄성 {k_elastic:.6f}")
    ok(abs(abs(k_short) / abs(k_long) - 1.0) < 1e-9 and abs(abs(k_short) / k_elastic - 1.0) < 1e-6,
       f"정적 한계를 몸 전체에 쓰므로 점성이 아주 크면 주기가 k₂ 를 못 움직여야 한다 — "
       f"{abs(k_short):.8f} 대 {abs(k_long):.8f} 대 {k_elastic:.8f}. "
       f"⚠ 이것이 «ω 는 유동학으로만 들어온다» 의 시험이다; 움직이면 ω² 관성항이 살아 있는 것이다")

    print("\n항등식과 J9")
    ident = tr.g_surface_identity(full, M_EARTH, R_EARTH)
    ok(ident < 1e-12,
       f"g_surface_identity 는 1e-12 안이어야 한다 — {ident:.2e}")
    # ⚠ 이 줄이 «구조가 맞다» 는 뜻이 아니다. 층 밀도를 선언 분율에서 지었으므로 Σm = M 은
    #   구성상 참이고, 잡는 것은 덮음의 빈틈·겹침과 분율 합뿐이다. 이름에 identity 가 있는 이유다.
    nmoi = tr.homogeneous_nmoi(full, M_EARTH, R_EARTH)
    print(f"  J9 — 균질 더미 nmoi {nmoi:.4f} 대 지구 실측 {EARTH_NMOI} "
          f"({nmoi / EARTH_NMOI - 1:+.1%}) — 이 근사의 크기다, 일치 판정이 아니다")
    ok(0.25 < nmoi < 0.45, f"J9 의 nmoi 가 물리적 범위 안이어야 한다 — {nmoi:.4f}")

    print("\nJ5 — 이 빌드 범위 밖")
    print("  Beuthe 의 h₂ 1.27 / 1.35 는 §3 막 근사의 값이고, 이 빌드는 그 공식을 짓지 않는다. "
          "식 (27) 은 유체층이 **표면에 닿을 때**의 관계라 껍질 아래 바다에 쓸 수 없다 — C62 (c).")

    if fails:
        print("\n[FAIL] " + f"{len(fails)}건")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("\n  [PASS] 조석 응답 — J0 고전해 재현 · J1 지구 두 층 인쇄 · 층 사상 최소 규칙 · "
          "덮음(겹침·빈틈) · 이름 붙은 거절 여섯 · 밴드 셋과 부분 거절 · g 항등식 · J9 근사 크기")
    return 0


if __name__ == "__main__":
    sys.exit(main())
