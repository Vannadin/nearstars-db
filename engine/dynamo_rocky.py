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
  {0.05, 0.10} — OC06's own two printed statements of the SAME quantity (multipolar moment / the same dynamo's
  maximum dipolar moment): "falls by nearly a factor of 20" (text) and "reduced by a factor of 10 or more"
  (abstract) — a 2× width; RM22's Solar-System validation point 0.06 sits inside it (RM22's adopted value is
  0.05, its reading of OC06). ⚠ Applies to base-heated dynamos only (MULTIPOLAR_CONDITION).
  ⚠ This value was corrected three times on 2026-09-03/04 — {0.06, 0.15} "2.5×" → {0.05, 0.06} "1.2×" →
  {0.05, 0.10} "2×, base-heated" — each time closer to the source, each time caught by a different seat:
  the case that checking a secondary citation against its source is not done in one pass.
  ⚠ Until 2026-09-04 the second grid point was 0.15 "(Grießmeier 2009)" and the spread read 2.5× — that was a
  different quantity: Grießmeier §2.2 gives 0.02–0.15 M_E for ONE configuration (Earth-like, 0.2 AU,
  0.5 M☉), the denominator is Earth's present moment, and 0.15 is the range's maximum "adopted to obtain a
  lower limit for the cosmic ray flux"; their Table 1 prints 0.37, 0.65, 0.96 for other locked cases. It
  reached us through RM22's one-line aside ("Some other authors work with a dipole moment reduction
  coefficient of 0.15") — a secondary citation that broke on reading the source. RM22 itself prints three
  numbers in one paragraph (OC06 "of the order of 0.05", its own "about 0.06", and that 0.15) — kept as printed.
* **RM22's own Solar-System numbers differ from the doc's zeros.** RM22 Table 8 computes Mercury 0.0003,
  Venus 0.0007, Mars 0.084 (marked extinct); the doc's validation table writes Venus and Mars as ℳ = 0.
  The zeros are this ladder's class judgements, not the model's output (rocky-dynamo-context-notes.md §1).
"""
from __future__ import annotations

import dataclasses

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
    "2009Icar..199..526G",      # Grießmeier+ 2009 — HELD (parallel seat, 2026-09-04). Cited for the tidal-locking
                               # coupling only; its 0.15 M_E is NOT a multipolar factor (see the docstring) and is no
                               # longer in MULTIPOLAR_FACTORS. Rossby / 0.12 appear nowhere in that paper.
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
MULTIPOLAR_FACTORS = (0.05, 0.10)   # OC06's own two printed statements of ONE quantity (multipolar / the same dynamo's
                                    # maximum dipolar moment): text "falls by nearly a factor of 20" (≳ 0.05) and abstract
                                    # "reduced by a factor of 10 or more" (≤ 0.1) — a 2× width, base-heated dynamos only.
                                    # (0.15 removed 2026-09-04 — a different quantity; {0.05, 0.06} stood for one hour and
                                    # was not two independent sources: 0.05 is RM22's reading of OC06 — the docstring.)
MULTIPOLAR_SOLAR_SYSTEM = 0.06      # RM22's Solar-System validation point inside that width ("about 0.06 … ratifies OC06");
                                    # RM22's own adopted value is 0.05 (its eq. 22 / "of the order of 0.05").
MULTIPOLAR_CONDITION = ("OC06's collapse is for base-heated dynamos ('as is the case on Earth', RM22); internally heated "
                        "ones are 'more gradual, show more scatter, and begin at smaller Ro_l' (OC06) — a different value "
                        "and a different threshold. This recipe cannot say which heating mode a roster body's core has.")
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


ROSSBY_REFUSAL = ("cannot-say (Ro_ℓ: ν has no value in RM22 — Appendix A.2's η_c is a mineral's viscosity in a different "
                  "equation; q_conv has one phrase and no definition — total vs super-adiabatic excess undecided; and the "
                  "printed Ro_ℓ equation misses RM22's own Table 8 by 4–5× on the slow rotators, a table that is itself a "
                  "fit of k = 60)")
NO_LOCK = "cannot-say (no tidal_locking — the branch key `locked` is that node's output and it has no recipe yet)"
FREE_ROTATION = ("dipolar by rule — RM22 §5.2: 'If the planet is not tidally coupled, we assume free rotation leading to a "
                 "dipolar magnetic moment … we use equation 20'; the dipolar zone 'does not present an explicit dependence "
                 "on the angular velocity'. Ro_ℓ is not evaluated on this path.")


def ladder(mass_earth: float, radius_earth: float | None, conductor_phase: str | None,
           stagnant_lid: bool | None, age_gyr: float | None, ice_mass_fraction: float = 0.0,
           body_class: str | None = "rocky", dynamo_regime: str | None = None,
           locked: bool | None = None, rotation_period_h: float | None = None) -> Result:
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth, "conductor_phase": conductor_phase,
              "stagnant_lid": stagnant_lid, "age_gyr": age_gyr, "ice_mass_fraction": ice_mass_fraction,
              "body_class": body_class, "dynamo_regime": dynamo_regime,
              "locked": locked, "rotation_period": rotation_period_h}
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

    # step 3 — ℳ_base (declared family) · step 4 — regime gate · step 5 — field
    # Step 4 (C16, 2026-09-04): RM22's branch structure. A declared dynamo_regime (Phase 4) still wins. Otherwise
    # the key is `locked` — tidal_locking's output, which the engine does not yet compute (no recipe) and which
    # this node does NOT declare for itself (tidal lock is a Phase 4 fact, as C22 kept its dial at 0):
    #   locked False → dipolar by the paper's rule (free rotation, eq. 20 = the ladder's base; no Ro_ℓ)
    #   locked True  → the locked branch, whose Ro_ℓ is refused by three names → both branches emitted
    #   locked None  → cannot-say (no tidal_locking) → both branches emitted, as before
    if dynamo_regime in ("dipolar", "multipolar"):
        branch, rossby = dynamo_regime, f"declared regime '{dynamo_regime}' (Phase 4) — Ro_ℓ not consulted"
    elif locked is False:
        branch, rossby = "dipolar", FREE_ROTATION
    elif locked is True:
        branch, rossby = "undeclared (both emitted)", ROSSBY_REFUSAL
    else:
        branch, rossby = "undeclared (both emitted)", NO_LOCK
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
        "regime": branch, "ladder_regime": reg, "dynamo_alive": alive, "rossby_verdict": rossby,
    }
    notes.append(
        f"단계 3 ℳ_base: regime {reg} → "
        + (f"{lo} ℳ⊕ (문서 인쇄값; 선언)" if elected else
           f"**문서에 값이 없다** — 격자 {lo}–{hi} ℳ⊕ 를 싣고 하나를 뽑지 않는다 (C11); 소비처가 자기 값을 선언하고 라벨을 단다")
        + ". 문서의 '(table below)' 는 클래스 앵커가 아니라 천체별 검증 표를 가리킨다 — 잘못된 표를 가리키는 포인터. "
        f"단계 4 영역 게이트 (C16): 열쇠는 tidal_locking 의 `locked` — 자유 자전이면 논문 규칙으로 쌍극자(식 20, Ro_ℓ 안 거침), "
        f"잠김이면 Ro_ℓ 경로인데 세 이유로 거절(ν 값 없음 · q_conv 정의 없음 · 인쇄 식이 Table 8 과 4–5배 불일치), 열쇠가 없으면 "
        f"cannot-say → **{branch}** [{rossby}]"
        + ("" if branch != "undeclared (both emitted)" else
           f"; 쌍극자 {dip_lo}–{dip_hi} ℳ⊕ 와 다극자 ×{MULTIPOLAR_FACTORS[0]}–{MULTIPOLAR_FACTORS[1]} "
           f"({mp_lo:.3g}–{mp_hi:.3g} ℳ⊕) 를 둘 다 싣는다 — 다극자 계수는 OC06 자신의 두 진술 '거의 20배'(≥0.05)와 "
           f"'10배 이상'(≤0.1) 사이 2배 폭이고 RM22 태양계 검증점 {MULTIPOLAR_SOLAR_SYSTEM} 은 그 안(RM22 채택값은 0.05). "
           "⚠ base-heated 다이나모 한정(지구가 그렇다, RM22) — 내부가열형은 더 완만하고 더 작은 Ro_ℓ 에서 시작(OC06); "
           "이 천체의 핵이 어느 쪽인지 이 레시피는 판정하지 못한다. (Grießmeier 의 0.15 는 다른 양이라 2026-09-04 에 뺐다)")
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
                         "regime": "", "ladder_regime": "", "dynamo_alive": "", "rossby_verdict": ""},
                  refs=REFS, notes=tuple(notes))


from registry import recipe  # noqa: E402


def ice_fraction_from_state(state) -> tuple[float | None, str]:
    """(ice_mass_fraction, where it came from) — C28 (2026-09-04).

    A declared `ice_mass_fraction` wins. Otherwise the value is READ from `interior.COMPOSITIONS`
    (the composition preset the body already chose with `composition_intent`; tuple slot 1 is the
    ice fraction) — referenced, not copied, so the interior and the dynamo know one number for the
    same body. No preset → (None, reason): the caller refuses by name instead of assuming 0."""
    if state.get("ice_mass_fraction") is not None:
        return float(state["ice_mass_fraction"]), "declared ice_mass_fraction"
    intent = state.get("composition_intent")
    from interior import COMPOSITIONS  # 조회만. dynamo 가 interior 의 표를 복제하지 않는다.
    if intent in COMPOSITIONS:
        return COMPOSITIONS[intent][1], f"composition preset: {intent} (interior.COMPOSITIONS, grade class)"
    return None, f"cannot-say (no composition preset): composition_intent '{intent}' 는 interior.COMPOSITIONS 에 없고 ice_mass_fraction 선언도 없다"


@recipe("dynamo_rocky")
def _from_state(state):
    imf, imf_source = ice_fraction_from_state(state)
    if imf is None:
        return out_of_domain(RECIPE, VERSION, imf_source,
                             inputs={"mass_earth": state["mass_earth"], "composition_intent": state.get("composition_intent"),
                                     "ice_mass_fraction": None}, refs=REFS)
    res = ladder(mass_earth=state["mass_earth"],
                  radius_earth=state.get("radius_earth", state.get("radius")),
                  conductor_phase=state.get("conductor_phase"),
                  stagnant_lid=state.get("stagnant_lid"),
                  age_gyr=state.get("age_gyr"),
                  ice_mass_fraction=imf,                            # C28: declared, else the composition preset (see above)
                  body_class=state.get("body_class"),
                  dynamo_regime=state.get("dynamo_regime"),
                  locked=state.get("locked"),                      # tidal_locking's output — absent until that node has a recipe
                  rotation_period_h=state.get("rotation_period"))
    # 어디서 온 분율인지 결과에 인쇄한다 (C28). Result 는 frozen 이라 notes 만 덧붙인다.
    return dataclasses.replace(res, notes=res.notes + (f"ice_mass_fraction {imf:.2f} ({imf_source})",))
