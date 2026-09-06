# 조석 잠김 판정 — 문서가 인쇄한 despin 식과 §4 상태 분류. 원문 여섯은 하나도 보유하지 않았다 (C36)
"""Has this body despun, and if so into what rotation state?

    from tidal_locking import solve

The chain has had a `tidal_locking` node since it was drawn, with a recipe document and nothing behind
it, so `locked` never reached any of its **eight** consumers and every body took `cannot-say`. This is
the supplier.

⚠ **What rests on the document and what rests on a paper — they are different here, and the split
moved on 2026-09-06.** Of the six sources the document cites:

- **Not held, and the formula's own sources**: Goldreich & Soter 1966 (Elsevier, paywalled) and Murray
  & Dermott 1999 (a textbook). So `τ_lock` itself is carried as *"the document prints this"*.
- **Held and read**: Leconte 2015 and Goldreich & Peale 1966. The Venus reasoning below stands on
  those two directly, quoted from the PDFs.
- **Held, not yet read**: Barnes 2017. And **Hut 1981 is held as a scan**, so its `ω_eq/n` is still
  carried from the document rather than from the paper — an image cannot be searched, and a clean-
  looking OCR is still OCR.

An earlier version of this header said all six were absent. Four arrived the same afternoon; **not
obtainable and not yet read are different grades**, and only the first is permanent.

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

#: 원시 자전의 **기본값**. §6 이 미상이라고 명시하고, 5 h 는 이 코드가 고른 출발점이지 문서의 수도
#: 진리도 아니다.
#: ⚠ 여기 처음 적혀 있던 정당화 — "판정을 흔들지 않는 것이 이 값을 쓸 수 있는 유일한 이유" — 는
#: **거짓이었다.** 금성에서 흔든다: P₀ 를 5 h 에서 19 h 로 옮기면 τ 가 1.62e10 → 4.26e9 yr 로 내려와
#: 나이 안에 든다. 하필 시험이 고정한 그 천체에서 깨진다. 정당화를 쓰면서 그 정당화를 시험하지 않은
#: 것이고, 그래서 이 값은 이제 **기본값이라고만** 불린다.
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


class NoExcessSpin(ValueError):
    """`|ω₀| ≤ n` — 걷어낼 초과가 없다. 이 공식이 서술하는 과정이 아니다."""


def despin_coefficient_yr_per_rad_s(mass_kg: float, radius_m: float, alpha: float, a_m: float,
                                    perturber_mass_kg: float, q_over_k2: float) -> float:
    """τ = C · |ω₀ − n| 의 C [yr per rad/s]. 역산이 이 값 하나로 닫힌다."""
    inertia = alpha * mass_kg * radius_m ** 2
    return q_over_k2 * inertia * a_m ** 6 / (3.0 * G * perturber_mass_kg ** 2 * radius_m ** 5) / YEAR_S


def despin_timescale_yr(mass_kg: float, radius_m: float, alpha: float, a_m: float,
                        perturber_mass_kg: float, q_over_k2: float,
                        omega0_period_h: float = OMEGA0_PERIOD_H) -> float:
    """문서 §1 이 인쇄한 식 그대로. 반환은 년."""
    n = mean_motion(a_m, perturber_mass_kg)
    omega0 = 2.0 * math.pi / (omega0_period_h * 3600.0)
    # 걷어낼 것은 **초과** 각운동량이라 크기다 — 문서 §1: "the time for that torque to remove the
    # **excess** spin angular momentum", 그리고 토크는 "drives the spin toward n". 부호 있는 차를 그대로
    # 쓰면 역행 출발에서 τ 가 음수로 나오고, `solve` 의 `hi < age` 가 그걸 **조용히 '잠김'으로** 읽는다.
    # 역행 출발은 도메인 밖이 아니다 — Goldreich & Peale 이 그 경우의 포획 확률을 그림 둘로 계산한다.
    # ⚠ 크기가 n 이하면 걷어낼 **초과**가 없다 — 오히려 가속해야 한다. `abs()` 만으로는 그 경우도
    # 양수 τ 를 내고 `solve` 가 그걸 '잠김'으로 읽는다. 부호 버그를 고치면서 열린 문이라 여기서 닫는다.
    # 문서 §1 이 "remove the **excess** spin angular momentum" 이라 적고, G&P 의 역행 논의도 |ω₀| > n
    # 이다. 초과가 없는 경우는 원문에도 우리 문서에도 없는 과정이다.
    if abs(omega0) <= n:
        raise NoExcessSpin(
            f"|ω₀| = {abs(omega0):.4g} rad/s is not above n = {n:.4g}: no excess spin to remove, so "
            f"this formula does not describe what would happen. The initial period must be shorter "
            f"than the orbital period, {2.0 * math.pi / n / 3600.0:.4g} h.")
    return abs(omega0 - n) * despin_coefficient_yr_per_rad_s(
        mass_kg, radius_m, alpha, a_m, perturber_mass_kg, q_over_k2)


def initial_period_h(target_tau_yr: float, mass_kg: float, radius_m: float, alpha: float,
                     a_m: float, perturber_mass_kg: float, q_over_k2: float) -> float:
    """역방향. 이 τ 를 내려면 원시 자전주기가 얼마여야 했는가 [h].

    유효 구간(`ω₀ > n`)에서 τ 는 `ω₀` 에 **선형**이라 대수 한 줄로 뒤집힌다 — `ω₀ = n + τ/C`.
    ⚠ **수치 탐색을 쓰지 않는 것이 요점이다.** `abs()` 때문에 τ 는 `ω₀ = n` 에서 최소인 V자라 같은 τ 를
    주는 `ω₀` 가 위아래로 둘 있고, 탐색기는 초기 추정값에 따라 **아래 가지로 수렴할 수 있다.** 그 가지는
    `τ/C` 를 빼는 해이고 물리적으로는 가속해야 하는 천체다. 대수로 풀면 그 가지가 아예 생기지 않는다.
    """
    n = mean_motion(a_m, perturber_mass_kg)
    c = despin_coefficient_yr_per_rad_s(mass_kg, radius_m, alpha, a_m, perturber_mass_kg, q_over_k2)
    omega0 = n + target_tau_yr / c
    if omega0 <= n:                      # 도중에 물리적으로 불가능해지는 양을 여기서 잡는다
        raise NoExcessSpin(f"the inversion returned ω₀ = {omega0:.4g} rad/s, not above n = {n:.4g}")
    return 2.0 * math.pi / omega0 / 3600.0


def initial_period_band_h(target_tau_yr: float, mass_earth: float, radius_earth: float, a_km: float,
                          perturber_mass_earth: float, nmoi: float | None = None) -> Band:
    """역산 밴드. 폭은 전적으로 `Q/k₂` 클래스 폭에서 온다 — 다른 불확실성은 안 들어간다.

    ⚠ 낙관 끝(`Q/k₂` 작음)이 **짧은** 주기다: 덜 흩는 천체는 같은 시간을 쓰려면 더 적은 초과에서
    출발해야 한다. 라벨이 어느 끝이 어느 가정인지 말한다."""
    args = (mass_earth * M_EARTH_KG, radius_earth * R_EARTH_M, nmoi if nmoi else 0.33,
            a_km * 1e3, perturber_mass_earth * M_EARTH_KG)
    fast = initial_period_h(target_tau_yr, *args, Q_OVER_K2_ROCKY.low)
    slow = initial_period_h(target_tau_yr, *args, Q_OVER_K2_ROCKY.high)
    lo, hi = sorted((fast, slow))
    return Band(None, lo, hi,
                f"the whole width is the Q/k₂ class band 10²–10³: {fast:.4g} h at the low end "
                f"(less dissipative) and {slow:.4g} h at the high end, for τ = {target_tau_yr:.3g} yr",
                "analog", estimates="omega_0")


def breakup_period_h(mass_earth: float, radius_earth: float) -> float:
    """자전 분열 한계 [h] — 적도 원심가속도 = 표면중력.

    `P_min = 2π√(R³/GM)` 인데 `M = (4/3)πR³ρ` 를 넣으면 **R 이 소거되어 `√(3π/Gρ)`** 가 된다. 즉 질량도
    반지름도 아니고 **밀도만**의 함수다. ⚠ 그래서 이 한계는 천체를 거의 안 가른다 — 밀도 3000–5500 이
    전부 1.9–1.4 h 안에 든다. 물리 한계라 지어낼 여지가 없다는 게 장점이고, **변별력이 없다는 게 한계**다.
    ⚠ 느린 쪽에는 이런 한계가 **없다**: 문헌이 초기 자전을 채택값으로만 인쇄한다 (Barnes: Kasting 13.5 h,
    지구 3 일). 그래서 허용 구간은 **한쪽만 닫혀 있다.**"""
    return 2.0 * math.pi * math.sqrt((radius_earth * R_EARTH_M) ** 3 /
                                     (G * mass_earth * M_EARTH_KG)) / 3600.0


def consistency_window_h(bodies, target_tau_yr: float, q_over_k2: float):
    """현재 자전이 측정된 천체들이 **하나의** ω₀ 로 동시에 설명되는가.

    각 천체는 관측 상태에 따라 **반대 방향의 경계**를 준다 — 감속한 천체는 `τ ≤ age` 라 `P₀ >` 어떤 값,
    감속 안 한 천체는 `τ > age` 라 `P₀ <` 어떤 값. ⚠ 그래서 이건 밴드끼리 겹치는지를 보는 게 아니다.
    한쪽은 바닥이고 한쪽은 천장이며, **창이 비면 그 `Q/k₂` 로는 네 천체를 함께 설명할 수 없다.**

    `bodies`: (label, m_earth, r_earth, a_km, perturber_m_earth, despun: bool) 의 순회 가능한 것.
    반환: (floor, ceiling, floor 를 정한 이름, ceiling 을 정한 이름)."""
    floor, ceiling = 0.0, math.inf
    who_lo, who_hi = "—", "—"
    for label, m, r, a_km, mp, despun in bodies:
        p_break = breakup_period_h(m, r)
        if p_break > floor:
            floor, who_lo = p_break, f"{label} breakup"
        p = initial_period_h(target_tau_yr, m * M_EARTH_KG, r * R_EARTH_M, 0.33,
                             a_km * 1e3, mp * M_EARTH_KG, q_over_k2)
        if despun and p > floor:
            floor, who_lo = p, label
        if not despun and p < ceiling:
            ceiling, who_hi = p, label
    return floor, ceiling, who_lo, who_hi


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
                  notes=("⚠ the despin formula is carried as what the methodology document prints: "
                         "its own sources (Goldreich & Soter 1966, Murray & Dermott 1999) are not "
                         "held. Four of the document's six sources are held, two of them read.",))


@recipe("tidal_locking")
def _(state) -> Result:
    return solve(mass_earth=state.get("mass_earth"), radius_earth=state.get("radius_earth"),
                 semi_major_axis_km=state.get("semi_major_axis_km"),
                 perturber_mass_earth=state.get("perturber_mass_earth"),
                 age_gyr=state.get("age_gyr"),
                 eccentricity=state.get("eccentricity", 0.0),
                 permanent_quadrupole=bool(state.get("permanent_quadrupole", False)),
                 nmoi=state.get("nmoi"))
