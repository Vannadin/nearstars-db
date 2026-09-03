# 암석 행성의 쌍극자 자기장 — RM22/OC06 결정 사다리를 레시피로: 두 게이트는 라벨, 네 선언은 격자, Rm > 40 은 인용 (Brief 47)
"""Rocky-planet dipole moment and surface field by the RM22 decision ladder.

    from dynamo_rocky import ladder
    ladder(mass_earth=1.0, radius_earth=1.0, conductor_phase="liquid_outer_solid_inner",
           stagnant_lid=False, age_gyr=4.54)        -> dipolar 1.0 M_E, B_eq 30 uT (+ multipolar branch)

Grounding: docs/reference/rocky-planet-dynamo-methodology.md — the *practical procedure*, which the doc
itself says is the recipe: "the whole recipe reduces to estimating the normalized moment M/M_E from the
regime ladder, then reading off the surface field"; "NearStars does not re-run RM22's full internal-
structure + thermal-evolution solver per body." Closing relation, anchored on Earth:

    B_eq = 30 µT · (ℳ/ℳ⊕) · (R/R⊕)⁻³ ,   B_pol = 2 · B_eq

⚠ What is a label here, and what is quoted rather than evaluated (owner's condition, 2026-09-03):
* **`Rm > 40` is QUOTED, NEVER EVALUATED.** The doc lists it at step 2 as a disqualifier beside two class
  judgements, with no formula anywhere in the file. This recipe does not compute a magnetic Reynolds
  number; it carries the citation (Gaidos, Conrad, Manga & Hernlund 2010) and says so on every result.
  Zhang & Rogers 2022 §2.8 argue the threshold is generically met while the liquid core convects — which
  is why `conductor_phase` stands in for the alive gate — and that too is a citation, not a computation.
* **The alive gate is three labels**: `conductor_phase` (core_state's verdict: solid → ℳ = 0, undecided →
  cannot-say), the **declared** stagnant-lid judgement (per body; undeclared → cannot-say), and a
  **declared** dynamo-death age per class (regime 5 only; the doc's one worked point, "Mars-mass by
  ~7 Gyr"; Zhang & Rogers' lifetimes make it contested and are carried beside it).
* **ℳ_base is a declared family.** The doc's "(table below)" at step 3 points at the per-body validation
  table, not a per-class anchor. Regime 1 → 1.0 ("up to ~1 ℳ⊕"), regime 4 → 2×10⁻³ (Ganymede), regime 5 → 0;
  **regimes 2 and 3 have no value in the doc** and are carried as grids with **no elected number** (C11).
* **The regime gate is declared or emitted both ways.** `rossby` is a gap (a rotation period cannot give
  Ro_ℓ). Undeclared → dipolar and multipolar branches both emitted, the multipolar factor itself a grid
  {0.06 (OC06; RM22 "about 0.06"), 0.15 (Grießmeier 2009)} — a factor 2.5 that rides on every value.
* **RM22's own Solar-System numbers differ from the doc's zeros.** RM22 Table 8 computes Mercury 0.0003,
  Venus 0.0007, Mars 0.084 (marked extinct); the doc's validation table writes Venus and Mars as ℳ = 0.
  The zeros are this ladder's class judgements, not the model's output (rocky-dynamo-context-notes.md §1).
"""
from __future__ import annotations

from payload import Result, out_of_domain

RECIPE = "rocky-planet-dynamo-methodology"
VERSION = "1"
REFS = (
    "docs/reference/rocky-planet-dynamo-methodology.md",
    "2022A&A...661A.101R",      # RM22, Rodríguez-Mozos & Moya 2022, A&A 661, A101 (arXiv 2203.01065) — held
    "2006E&PSL.250..561O",      # OC06, Olson & Christensen 2006 — the 0.12 boundary and the ~0.06 factor; HELD
                               # (owner, 2026-09-03 13:40, PROVENANCE) — so the 0.06 in MULTIPOLAR_FACTORS is now
                               # checkable at source instead of via RM22; not re-read in Brief 64, value unchanged
    "2010ApJ...718..596G",      # Gaidos, Conrad, Manga & Hernlund 2010 — cited for the Rm > 40 threshold that this
                               # recipe QUOTES AND DOES NOT EVALUATE; HELD (arXiv preprint, parallel seat,
                               # 2026-09-03 13:37, PROVENANCE). Both "NOT HELD" were true at 12:00 when written.
    "2009Icar..199..526G",      # Grießmeier+ 2009 — the alternative 0.15 multipolar factor
    "2022ApJ...938..131Z",      # Zhang & Rogers 2022 — computed alternative (thermal evolution), flagged, not followed
)

B_EQ_EARTH_UT = 30.0           # equatorial surface field anchor
EARTH_DENSITY = 5514.0         # kg/m³ (M_E / (4/3 π R_E³) with the constants below)
M_EARTH_KG, R_EARTH_M = 5.972e24, 6.371e6

# ── declarations, every one a family or a labelled judgement ─────────────────────────
WATER_RICH_IMF = 0.05          # declared threshold: ice_mass_fraction at/above this → regime 4
LOW_DENSITY_RATIO = 0.8        # doc: "ρ < 0.8 ρ⊕, Mars-analog" → regime 5
M_BASE = {                     # ℳ/ℳ⊕ — the declared family. None = the doc prints no value.
    1: (1.0, 1.0),             # dry, M < 2 M⊕: "up to ~1 ℳ⊕"
    2: (1.0, 2.0),             # dry, 2–2.5 M⊕: "can exceed Earth's moment while young" — NO VALUE IN THE DOC
    3: (0.3, 1.0),             # dry, > 2.5 M⊕: "weaker and shorter-lived" — NO VALUE IN THE DOC
    4: (2.0e-3, 2.0e-3),       # water-rich: Ganymede analog
    5: (0.0, 0.0),             # low-density dry, Mars analog: dynamo-dead by a few Gyr
}
ELECTED = {1, 4, 5}            # regimes where the doc prints one value; 2 and 3 emit endpoints only
MULTIPOLAR_FACTORS = (0.06, 0.15)   # OC06 / RM22 ("about 0.06") vs Grießmeier 2009 — factor 2.5 spread
DYNAMO_DEATH_AGE_GYR = {5: 7.0}     # the doc's one worked point ("Mars-mass by ~7 Gyr"); Zhang & Rogers 2022
                                    # §4.2.5 give 1 M⊕ shut-off at ~2.5–5 Gyr and 3 M⊕ at ~10–12 Gyr from a
                                    # different model — contested, carried, not adopted
ROCKY_CLASSES = ("rocky", "super_earth", "moon", "icy")
MAX_ROCKY_MASS = 10.0

ALIVE = "alive"
DEAD_SOLID = "dead (core solid)"
DEAD_LID = "dead (stagnant lid, declared)"
DEAD_AGE = "dead (past declared death age for its class)"
UNDECIDED_CORE = "cannot-say (conductor_phase undecided)"
UNDECIDED_LID = "cannot-say (stagnant-lid judgement undeclared)"
RM_NOTE = ("Rm > 40 (Gaidos, Conrad, Manga & Hernlund 2010) is QUOTED, not evaluated: no magnetic Reynolds "
           "number is computed here; the liquid-core label stands in for it (Zhang & Rogers 2022 §2.8, also a citation)")


def regime_class(mass_earth: float, radius_earth: float, ice_mass_fraction: float) -> int:
    if ice_mass_fraction >= WATER_RICH_IMF:
        return 4
    rho = mass_earth * M_EARTH_KG / (4.0 / 3.0 * 3.141592653589793 * (radius_earth * R_EARTH_M) ** 3)
    if rho < LOW_DENSITY_RATIO * EARTH_DENSITY:
        return 5
    if mass_earth < 2.0:
        return 1
    if mass_earth <= 2.5:
        return 2
    return 3


def b_eq_ut(moment_earth: float, radius_earth: float) -> float:
    return B_EQ_EARTH_UT * moment_earth * radius_earth ** -3


def ladder(mass_earth: float, radius_earth: float | None, conductor_phase: str | None,
           stagnant_lid: bool | None, age_gyr: float | None, ice_mass_fraction: float = 0.0,
           body_class: str | None = "rocky", dynamo_regime: str | None = None) -> Result:
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth, "conductor_phase": conductor_phase,
              "stagnant_lid": stagnant_lid, "age_gyr": age_gyr, "ice_mass_fraction": ice_mass_fraction,
              "body_class": body_class, "dynamo_regime": dynamo_regime}
    if body_class not in ROCKY_CLASSES or mass_earth > MAX_ROCKY_MASS:
        return out_of_domain(RECIPE, VERSION,
                             f"'{body_class}' {mass_earth} M⊕ 는 암석 사다리 밖이다 (암석 클래스, ≤ {MAX_ROCKY_MASS} M⊕) "
                             "— 거대행성·서브넵튠은 dynamo_giant / planetary-dynamo-scaling 의 몫이다.",
                             inputs=inputs, refs=REFS)
    if not radius_earth or radius_earth <= 0.0:
        return out_of_domain(RECIPE, VERSION, "반지름이 없다 — 밀도 분류도 표면장(R⁻³)도 낼 수 없다.",
                             inputs=inputs, refs=REFS)

    # step 1 — classify
    reg = regime_class(mass_earth, radius_earth, ice_mass_fraction or 0.0)
    # step 2 — alive gate: three labels, no formula
    if conductor_phase in (None, "undecided"):
        alive = UNDECIDED_CORE
    elif conductor_phase == "solid":
        alive = DEAD_SOLID
    elif stagnant_lid is None:
        alive = UNDECIDED_LID
    elif stagnant_lid:
        alive = DEAD_LID
    elif reg in DYNAMO_DEATH_AGE_GYR and age_gyr is not None and age_gyr > DYNAMO_DEATH_AGE_GYR[reg]:
        alive = DEAD_AGE
    else:
        alive = ALIVE

    lo, hi = M_BASE[reg]
    elected = reg in ELECTED
    notes = [
        f"RM22 사다리 (rocky-planet-dynamo-methodology, 실무 절차). 단계 1 regime {reg} "
        f"({'물 풍부' if reg == 4 else '저밀도 건조' if reg == 5 else f'건조 {mass_earth:.2f} M⊕'}; "
        f"얼음질량분율 {ice_mass_fraction or 0.0:.2f}, 문턱 {WATER_RICH_IMF} 는 선언). 단계 2 생존 게이트 = "
        f"라벨 셋: conductor_phase '{conductor_phase}' (core_state), 정체 암석권 선언 {stagnant_lid}, "
        f"클래스별 사멸 연령 선언 {DYNAMO_DEATH_AGE_GYR} → **{alive}**. {RM_NOTE}.",
    ]
    if alive != ALIVE:
        values = {"dipole_moment": 0.0 if alive.startswith("dead") else None, "b_eq": 0.0 if alive.startswith("dead") else None,
                  "b_pol": 0.0 if alive.startswith("dead") else None, "regime": alive, "ladder_regime": reg,
                  "dynamo_alive": alive, "dipole_moment_min": None, "dipole_moment_max": None,
                  "b_eq_multipolar_min": None, "b_eq_multipolar_max": None}
        notes.append("죽었거나 판정 불가이므로 ℳ_base 와 영역 게이트를 평가하지 않는다. "
                     + ("판정 불가는 기본값이 아니다 — 소비처는 값을 받지 않는다." if alive.startswith("cannot") else
                        "ℳ = 0, 표면장 0 — 사다리의 단계 2 ('ℳ = 0, done')."))
        return Result(recipe=RECIPE, version=VERSION, regime=f"ladder_regime_{reg}_{'dead' if alive.startswith('dead') else 'undecided'}",
                      reason=f"단계 2 에서 끝난다: {alive}.",
                      grade="judgment", inputs=inputs, values=values,
                      units={"dipole_moment": "M_earth", "dipole_moment_min": "M_earth", "dipole_moment_max": "M_earth",
                             "b_eq": "uT", "b_pol": "uT", "b_eq_multipolar_min": "uT", "b_eq_multipolar_max": "uT",
                             "regime": "", "ladder_regime": "", "dynamo_alive": ""},
                      refs=REFS, notes=tuple(notes))

    # step 3 — ℳ_base (declared family) · step 4 — regime gate (declared or both) · step 5 — field
    branch = dynamo_regime if dynamo_regime in ("dipolar", "multipolar") else "undeclared (both emitted)"
    dip_lo, dip_hi = lo, hi
    mp_lo, mp_hi = lo * MULTIPOLAR_FACTORS[0], hi * MULTIPOLAR_FACTORS[1]
    if branch == "dipolar":
        m_lo, m_hi = dip_lo, dip_hi
    elif branch == "multipolar":
        m_lo, m_hi = mp_lo, mp_hi
    else:
        m_lo, m_hi = dip_lo, dip_hi          # the dipolar branch is the primary reading; multipolar rides beside it
    # an elected regime has one number on the primary branch (dipolar unless multipolar was declared); the
    # multipolar pair is always emitted beside it. Regimes 2 and 3 elect nothing.
    moment = m_lo if elected else None
    values = {
        "dipole_moment": moment if elected else None,
        "dipole_moment_min": m_lo, "dipole_moment_max": m_hi,
        "b_eq": b_eq_ut(moment, radius_earth) if (elected and moment is not None) else None,
        "b_pol": 2.0 * b_eq_ut(moment, radius_earth) if (elected and moment is not None) else None,
        "b_eq_multipolar_min": b_eq_ut(mp_lo, radius_earth), "b_eq_multipolar_max": b_eq_ut(mp_hi, radius_earth),
        "regime": branch, "ladder_regime": reg, "dynamo_alive": alive,
    }
    notes.append(
        f"단계 3 ℳ_base: regime {reg} → "
        + (f"{lo} ℳ⊕ (문서 인쇄값; 선언)" if elected else
           f"**문서에 값이 없다** — 격자 {lo}–{hi} ℳ⊕ 를 싣고 하나를 뽑지 않는다 (C11); 소비처가 자기 값을 선언하고 라벨을 단다")
        + ". 문서의 '(table below)' 는 클래스 앵커가 아니라 천체별 검증 표를 가리킨다 — 잘못된 표를 가리키는 포인터. "
        f"단계 4 영역 게이트: rossby 엣지는 gap 이라 선언으로 받는다 → **{branch}**"
        + ("" if branch != "undeclared (both emitted)" else
           f"; 쌍극자 {dip_lo}–{dip_hi} ℳ⊕ 와 다극자 ×{MULTIPOLAR_FACTORS[0]}–{MULTIPOLAR_FACTORS[1]} "
           f"({mp_lo:.3g}–{mp_hi:.3g} ℳ⊕) 를 둘 다 싣는다 — 다극자 계수 자체가 OC06/RM22 0.06 대 Grießmeier 0.15, "
           "답에서 2.5배")
        + f". 단계 5 B_eq = 30 µT · ℳ · (R/R⊕)⁻³ (R = {radius_earth:.4f} R⊕), B_pol = 2 B_eq. "
        "지구 30 µT 는 앵커의 재현이지 예측이 아니다. RM22 자신의 Table 8 은 수성 0.0003 · 금성 0.0007 · 화성 0.084 를 "
        "계산하고, 문서의 검증 표는 관측열을 쓰며 금성·화성을 0 으로 적는다 — 그 0 은 이 사다리의 클래스 판단이다.")
    return Result(recipe=RECIPE, version=VERSION, regime=f"ladder_regime_{reg}_{branch.split()[0]}",
                  reason=(f"regime {reg}, {alive}; ℳ_base " + (f"{lo} ℳ⊕" if elected else f"{lo}–{hi} ℳ⊕ (미선출)")
                          + f", 영역 {branch}; "
                          + (f"B_eq {values['b_eq']:.3g} µT" if values["b_eq"] is not None else "B_eq 미선출")
                          + f" (다극자면 {values['b_eq_multipolar_min']:.3g}–{values['b_eq_multipolar_max']:.3g} µT)."),
                  # 등급: 두 게이트가 라벨이고 ℳ_base·영역·다극자 계수가 선언이므로 judgment 를 넘지 않는다.
                  grade="judgment", inputs=inputs, values=values,
                  units={"dipole_moment": "M_earth", "dipole_moment_min": "M_earth", "dipole_moment_max": "M_earth",
                         "b_eq": "uT", "b_pol": "uT", "b_eq_multipolar_min": "uT", "b_eq_multipolar_max": "uT",
                         "regime": "", "ladder_regime": "", "dynamo_alive": ""},
                  refs=REFS, notes=tuple(notes))


from registry import recipe  # noqa: E402


@recipe("dynamo_rocky")
def _from_state(state):
    return ladder(mass_earth=state["mass_earth"],
                  radius_earth=state.get("radius_earth", state.get("radius")),
                  conductor_phase=state.get("conductor_phase"),
                  stagnant_lid=state.get("stagnant_lid"),
                  age_gyr=state.get("age_gyr"),
                  ice_mass_fraction=state.get("ice_mass_fraction", 0.0),
                  body_class=state.get("body_class"),
                  dynamo_regime=state.get("dynamo_regime"))
