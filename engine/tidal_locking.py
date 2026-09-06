# 조석 잠김 판정 — 문서가 인쇄한 despin 식과 §4 상태 분류. 원문 여섯은 하나도 보유하지 않았다 (C36)
"""Has this body despun, and if so into what rotation state?

    from tidal_locking import solve

The chain has had a `tidal_locking` node since it was drawn, with a recipe document and nothing behind
it, so `locked` never reached any of its **eight** consumers and every body took `cannot-say`. This is
the supplier.

⚠ **Nothing here is attributed to a paper.** The despin formula, Hut 1981's equilibrium spin and the
`Q/k₂` classes all come from `tidal-locking-timescale-methodology.md`, and **none of the six sources
that document cites is held** — Goldreich & Soter 1966, Murray & Dermott 1999, Hut 1981, Goldreich &
Peale 1966, Barnes 2017, Leconte 2015 are all absent from the cache. So the grade is what the document
supports and the citations say *"the document prints this"*, not *"the paper says this"*.

**What the document prints** (§1):

    τ_lock  ≈  (ω₀ − n) · (Q/k₂) · (I a⁶) / (3 G M_p² R⁵),      I = α m R²

with `n = √(G M_p / a³)`. The verdict is one comparison: `τ_lock ≪ t_sys` → despun.

⚠ **The document's own calibration table does not reproduce under this formula, and no choice of
constants fixes it.** With `Q/k₂` and `ω₀` shared across bodies their ratio is fixed —
`τ(Venus)/τ(Moon) ≈ 6.1×10³` — so if the Moon lands where §2 prints it (10⁷–10⁸ yr) Venus lands at
6×10¹⁰–6×10¹¹ yr, **13 to 135 times the system age**. Any order-unity factor missing from the printed
formula multiplies both rows and cancels out of the ratio, so obtaining the missing sources cannot
change this. `test_tidal_locking.py` pins it.

**Where the defect is, corrected 2026-09-06 after reading the primary sources.** The first reading
here was that §5's thermal-tide exception rescues a prediction the formula never makes. **That is
wrong, and Leconte 2015 (`2015Sci...347..632L`, now held) says so**: *"although tidal friction inside
the planet is continuously trying to spin it down to a state of synchronous rotation, thermal tides
are strong enough to drive the planet out of synchronicity."* The literature holds that the solid tide
**would** synchronise Venus. So the exception is well-founded and the failure is ours.

The ratio argument then locates it exactly. Since no shared constant can move `τ(Venus)/τ(Moon)`, the
repair cannot be a global coefficient — **it has to be per-body**, and the direction is fixed: Venus
needs `Q/k₂ ≲ 28` to despin within the age, below the floor of the rocky class this document prints
as 10²–10³. §2's own Venus cell says *"rocky + atmosphere"* where every other row names a class range,
and that missing number is the defect. **A single class band cannot carry Venus**, which is a
statement about the table rather than about the formula.

⚠ Goldreich & Peale 1966 (`1966AJ.....71..425G`, held) devotes §V to Venus and **agrees with Leconte
on the premise**: it calls the synchronous state *"the otherwise stable synchronous state of
rotation"*, i.e. where the solid tide drives Venus. Two sources fifty years apart, one conclusion, and
it is the one our §2 row cannot reproduce.

They part on the *cause* of the escape. G&P report atmospheric-torque proposals (Gold; MacDonald 1964)
and call them *"quite reasonable"* on mass grounds — and then object: *"However, if the atmosphere is
capable of pushing Venus through the otherwise stable synchronous state of rotation, present control
of the rotation of Venus by the earth would be hard to understand."* Their Venus–Earth synodic
resonance is not a separate topic from the atmospheric explanation; it is their reason for doubting
it. This recipe takes no position on the cause, only on the premise both accept.

⚠ **A correction about how this was read.** The first version of this note said the paper never
mentions thermal or atmospheric tides. The count behind that was real — the phrases *"atmospheric
tide"* and *"thermal tide"* occur zero times — but the sentence written over it was not: the stem
`atmospher` occurs three times and every one is about torques on Venus's spin. A phrase count was
reported as a claim about the concept. (In the same scan, `therm` matches four times and all four are
*"Furthermore"*, so the errors run in both directions.)

**Three rotation states, not two** (§4). Despinning is not synchronisation:

- `e ≈ 0` → **1:1 synchronous**, a fixed substellar point;
- `e` significant, no permanent quadrupole → **pseudo-synchronous**, `ω_eq/n` above 1, so the
  substellar point drifts;
- `e` significant **with** a permanent quadrupole → capture into a **p:q resonance**, Mercury's 3:2.

⚠ Capture into p:q is *probabilistic* in the document's own words, so this recipe never asserts one:
it reports that the body is in the p:q class and leaves which resonance unanswered.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bands import Band  # noqa: E402
from payload import Result, out_of_domain  # noqa: E402
from registry import recipe  # noqa: E402

RECIPE = "tidal-locking-timescale-methodology"
VERSION = "1"
REFS = ("docs/reference/tidal-locking-timescale-methodology.md@«τ_lock  ≈  (ω₀ − n) · (Q / k₂) · (I a⁶) / (3 G M_p² R⁵)»",
        "docs/reference/tidal-locking-timescale-methodology.md@«ω_eq / n  =  (1 + (15/2)e² + (45/8)e⁴ + (5/16)e⁶) / [(1 + 3e² + (3/8)e⁴)(1 − e²)^{3/2}]»")

G = 6.674e-11
YEAR_S = 3.155815e7
M_EARTH_KG = 5.9722e24
R_EARTH_M = 6.371e6

#: §2 가 인쇄한 암석체 class 값. 점이 아니라 밴드다 — 문서가 밴드로 인쇄한다.
#: doc @«| **Moon** | Earth | 3.84×10⁵ km | rocky ~10²–10³ |»
Q_OVER_K2_ROCKY = Band(None, 1e2, 1e3,
                       "tidal-locking-timescale-methodology §2 prints the rocky class as ~10²–10³",
                       "analog", estimates="Q/k2")

#: 원시 자전. §6 이 미상이라고 명시한다. 5 h 는 이 코드가 고른 작업값이고 문서의 수가 아니다.
#: 판정을 흔드는지는 test 가 잰다 — 흔들지 않는 것이 이 값을 쓸 수 있는 유일한 이유다.
OMEGA0_PERIOD_H = 5.0

#: §4 상태 이름. bool 이 아니다 — 'despun' 과 '1:1' 은 같은 말이 아니라고 문서가 절 하나를 들여 말한다.
STATE_SYNCHRONOUS = "1:1 synchronous"
STATE_PSEUDO = "pseudo-synchronous (ω_eq > n; the substellar point drifts)"
STATE_RESONANCE = "p:q spin-orbit resonance class (which resonance is not decided here)"
STATE_UNDESPUN = "not despun within the system age"

#: §4 는 'e ≈ 0' 과 '유의미한 e' 로만 가르고 **경계를 인쇄하지 않는다.** 그래서 경계는 문서가 아니라
#: 문서의 앵커 두 천체가 정한다 — 달은 e = 0.0549 인데 관측 1:1 이고, 수성은 e = 0.206 인데 3:2 다.
#: 그 사이에는 아무 근거도 없으므로 여기서는 **분류하지 않는다.** (처음 짠 0.01 문턱은 문서 자신의
#: 1:1 앵커인 달을 pseudo-synchronous 로 잘못 분류했다. 그래서 그 수를 버렸다.)
E_MOON_ONE_TO_ONE = 0.055        # the Moon's e, quoted to the digits §2 uses; observed 1:1 there
E_MERCURY_RESONANT = 0.206       # observed 3:2 at this eccentricity
STATE_UNCLASSIFIED = ("unclassified — §4 prints no eccentricity boundary; the Moon is 1:1 at e = 0.055 "
                      "and Mercury is 3:2 at e = 0.206, and this body falls between them")


def mean_motion(a_m: float, perturber_mass_kg: float) -> float:
    """n = √(G M_p / a³) [rad/s]."""
    return math.sqrt(G * perturber_mass_kg / a_m ** 3)


def despin_timescale_yr(mass_kg: float, radius_m: float, alpha: float, a_m: float,
                        perturber_mass_kg: float, q_over_k2: float,
                        omega0_period_h: float = OMEGA0_PERIOD_H) -> float:
    """문서 §1 이 인쇄한 식 그대로. 반환은 년."""
    n = mean_motion(a_m, perturber_mass_kg)
    omega0 = 2.0 * math.pi / (omega0_period_h * 3600.0)
    inertia = alpha * mass_kg * radius_m ** 2
    tau_s = (omega0 - n) * q_over_k2 * inertia * a_m ** 6 / (3.0 * G * perturber_mass_kg ** 2 * radius_m ** 5)
    return tau_s / YEAR_S


def equilibrium_spin_ratio(e: float) -> float:
    """Hut 1981 의 ω_eq/n, 문서 §4(b) 가 인쇄한 형태 그대로."""
    num = 1.0 + 7.5 * e ** 2 + (45.0 / 8.0) * e ** 4 + (5.0 / 16.0) * e ** 6
    den = (1.0 + 3.0 * e ** 2 + (3.0 / 8.0) * e ** 4) * (1.0 - e ** 2) ** 1.5
    return num / den


def rotation_state(e: float, permanent_quadrupole: bool) -> str:
    """§4. 감속했다는 전제 아래 최종 상태를 고른다 — 고를 수 있는 구간에서만."""
    if e <= E_MOON_ONE_TO_ONE:
        return STATE_SYNCHRONOUS
    if e < E_MERCURY_RESONANT:
        return STATE_UNCLASSIFIED
    return STATE_RESONANCE if permanent_quadrupole else STATE_PSEUDO


def solve(mass_earth: float | None, radius_earth: float | None, semi_major_axis_km: float | None,
          perturber_mass_earth: float | None, age_gyr: float | None,
          eccentricity: float | None = 0.0, permanent_quadrupole: bool = False,
          nmoi: float | None = None) -> Result:
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth,
              "semi_major_axis_km": semi_major_axis_km, "perturber_mass_earth": perturber_mass_earth,
              "age_gyr": age_gyr, "eccentricity": eccentricity,
              "permanent_quadrupole": permanent_quadrupole, "nmoi": nmoi}
    missing = [k for k in ("mass_earth", "radius_earth", "semi_major_axis_km", "perturber_mass_earth",
                           "age_gyr") if inputs[k] in (None, 0)]
    if missing:
        return out_of_domain(RECIPE, VERSION,
                             f"no {', '.join(missing)} — the despin formula needs all of them "
                             f"(§1: ω₀, n, I, a, M_p)", inputs=inputs, refs=REFS)

    alpha = nmoi if nmoi else 0.33
    m = mass_earth * M_EARTH_KG
    r = radius_earth * R_EARTH_M
    a = semi_major_axis_km * 1e3
    mp = perturber_mass_earth * M_EARTH_KG
    age_yr = age_gyr * 1e9

    lo = despin_timescale_yr(m, r, alpha, a, mp, Q_OVER_K2_ROCKY.low)
    hi = despin_timescale_yr(m, r, alpha, a, mp, Q_OVER_K2_ROCKY.high)
    tau = Band(None, lo, hi,
               f"the Q/k₂ class band 10²–10³ carried through §1's formula "
               f"(ω₀ from a {OMEGA0_PERIOD_H:g} h primordial period, this code's working value)",
               "analog", estimates="tau_lock")

    if hi < age_yr:
        locked, state = True, rotation_state(eccentricity or 0.0, permanent_quadrupole)
        verdict = f"despun: even the slow end of the band, {hi:.3g} yr, is under the {age_yr:.3g} yr age"
    elif lo > age_yr:
        locked, state = False, STATE_UNDESPUN
        verdict = f"not despun: even the fast end, {lo:.3g} yr, exceeds the {age_yr:.3g} yr age"
    else:
        locked, state = None, STATE_UNDESPUN
        verdict = (f"cannot say: the band {lo:.3g}–{hi:.3g} yr straddles the {age_yr:.3g} yr age, so "
                   f"the Q/k₂ class alone decides the verdict and the document prints it as a band")

    n = mean_motion(a, mp)
    period_h = 2.0 * math.pi / n / 3600.0
    if locked and state == STATE_PSEUDO:
        period_h /= equilibrium_spin_ratio(eccentricity or 0.0)

    values = {"locked": locked, "rotation_state": state,
              "orbital_period_h": 2.0 * math.pi / n / 3600.0,
              "t_lock_yr_min": lo, "t_lock_yr_max": hi,
              "t_lock_width_source": tau.width_source}
    if locked:
        values["rotation_period_h"] = period_h
    return Result(recipe=RECIPE, version=VERSION,
                  regime=state, reason=verdict, grade="analog", inputs=inputs,
                  values=values,
                  units={"t_lock_yr_min": "yr", "t_lock_yr_max": "yr", "rotation_period_h": "h",
                         "orbital_period_h": "h", "locked": "", "rotation_state": "",
                         "t_lock_width_source": ""},
                  refs=REFS,
                  notes=("⚠ none of the six sources this recipe's document cites is held; every "
                         "formula here is carried as what that document prints.",))


@recipe("tidal_locking")
def _(state) -> Result:
    return solve(mass_earth=state.get("mass_earth"), radius_earth=state.get("radius_earth"),
                 semi_major_axis_km=state.get("semi_major_axis_km"),
                 perturber_mass_earth=state.get("perturber_mass_earth"),
                 age_gyr=state.get("age_gyr"),
                 eccentricity=state.get("eccentricity", 0.0),
                 permanent_quadrupole=bool(state.get("permanent_quadrupole", False)),
                 nmoi=state.get("nmoi"))
