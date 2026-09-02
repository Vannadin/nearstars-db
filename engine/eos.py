# 층 재료의 상태방정식 ρ(P) — 상수 하나하나가 어느 논문 어느 표에서 왔는지 붙여둔다
"""Cold equations of state for the materials a solid body is built from.

    from eos import MATERIALS
    MATERIALS["fe_prem"].density(136e9)      → 9.9e3 kg/m³ 근처 (지구 핵-맨틀 경계)

내부 구조를 적분하려면 압력에서 밀도를 돌려주는 함수가 있어야 한다. 층 밀도를
상수로 두면 자기압축이 통째로 빠지고, 그게 균질 2층 모형이 지구에서 C/MR² 를
4.8 % 크게 냈던 이유다.

**여기 있는 숫자는 전부 발표된 적합값이고, 상수마다 출처를 옆에 적었다.** 손으로
친 표에서 54배가 어긋났던 전례가 있어서, 출처 없는 상수는 이 파일에 못 들어온다.

다섯 가지 함수형을 쓴다. 어느 것을 쓸지는 그 재료를 적합한 논문이 정한 것이지 우리가
고른 게 아니다.

* **BM2** — 2차 Birch-Murnaghan. K₀′ 를 4 로 고정한 형태다.
  P = (3/2) K₀ [(ρ/ρ₀)^(7/3) − (ρ/ρ₀)^(5/3)]
  Zeng+ 2016 이 PREM 을 이 형태로 적합했다 (arXiv:1512.08827 eq. 1).
* **BME3** — 3차 Birch-Murnaghan. K₀′ 가 자유롭다. Seager+ 2007 Table 1 의 기본형.
* **BME4** — 4차 Birch-Murnaghan. K₀″ 가 하나 더 붙는다. Seager+ 2007 이 규산염
  **하나에만** 쓴 형태이고, 고른 이유가 "TFD 와 매끄럽게 이어지는 유일한 적합" 이다.
  그 한 자리가 3.5 TPa 위의 규산염이라 이 형태가 필요했다 — 자세한 사정은 SILICATE 주석에.
* **Vinet** — 고압 외삽에 BME 보다 낫다고 Seager+ 2007 §III.1 이 적는다. Fe(ε) 에 쓴다.
* **Polytrope** — P = K ρ^(1+1/n). 응축상이 아니라 수소-헬륨 외피에 쓰는 형태다.
  폴리트로프는 **별도의 가지가 아니라 상태방정식의 한 형태** 이고, 그래서 같은 적분기가
  거대행성을 그대로 푼다. n = 1 의 계수는 H_HE 주석에 있다.

다섯 형태가 전부 **순수한 물질 하나** 를 서술한다. 한 층 안에 두 물질이 섞여 있는 상태는
형태가 아니라 **재료를 합성하는 규칙** 이 필요하고, 그것이 `Mixture` 다. 부피 가법
혼합이며 상수와 유효 한계는 그 클래스 위 주석에 있다.

**등온이 아니다 — 온도를 주면 열압력이 붙는다.** `density(p)` 는 예전 그대로이고,
`density(p, t, t_pot)` 가 냉각 곡선에서 열압력을 뺀 자리를 뒤집는다. 상수와 기준, 그리고
기준을 틀리면 왜 지구를 두 번 데우는지는 아래 "열 항" 절에 있다. 열 상수가 없는 상
(얼음 VII, 수소-헬륨)은 등온으로 남고, `cold_phases()` 가 그 이름을 들고 있다.

각 재료는 **상(phase) 의 열** 이다. 상마다 유효 압력 구간이 있고, 구간 사이에 근거가
없는 틈이 있으면 그 틈을 이름 붙여 들고 있는다 — 얼음의 209.5 MPa ~ 2.216 GPa 가
그렇다. 솔버가 거기에 발을 디디면 조용히 외삽하는 게 아니라 그 사실을 돌려준다.
"""
from __future__ import annotations

import math

import hhe_table
import ice_melt_table
import water_hot
import water_table
import water2_table
import ammonia_table
from dataclasses import dataclass

R_GAS = 8.314462618          # J mol⁻¹ K⁻¹. CODATA 2018 기체상수


class PhaseGap(Exception):
    """근거 있는 상 사이의 빈 구간에 압력이 떨어졌다. 외삽 대신 이걸 던진다.

    온도 천장을 넘어도 같은 것을 던진다. 막힌 것이 압력인지 온도인지는 `temperature_k`
    가 채워져 있는지로 갈리고, 두 경우에 다른 예외를 만들면 잡는 쪽이 둘로 갈린다.

    **온도가 막았다면 어느 쪽으로 막았는지까지 말한다.** 시험 온도를 올려야 풀리는
    경우(`too_cold=True`) 와 내려야 풀리는 경우가 있고, 사격의 괄호는 그것으로 방향을
    정한다. 이 구분이 없던 동안 괄호는 늘 올리기만 했고, 수소-헬륨 표가 위아래로 다 벽을
    갖게 되면서 실제로 걸렸다 — 목성의 첫 시험값이 아래 벽에 막혀 열두 번 올라가다
    92,887 K 로 위 벽을 뚫었다."""

    def __init__(self, material: str, pressure_pa: float, reason: str,
                 temperature_k: float = 0.0, too_cold: bool = False):
        self.material = material
        self.pressure_pa = pressure_pa
        self.temperature_k = temperature_k
        self.too_cold = too_cold
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class Phase:
    """한 상의 냉각 등온 상태방정식."""
    name: str
    form: str                 # bm2 | bme3 | bme4 | vinet | polytrope
    rho0: float               # kg/m³. polytrope 는 0 이다 — 영압에서 밀도가 0 이다
    k0: float                 # Pa. polytrope 는 K [m⁵ kg⁻¹ s⁻²] 를 여기 넣는다
    k0p: float                # K₀′ (bm2 는 4 로 고정이므로 무시된다). polytrope 는 지수 n
    p_max: float              # Pa. 이 상이 유효한 상한
    ref: str                  # 어느 논문 어느 표에서 왔는가
    p_min: float = 0.0        # Pa. 앞 상에서 넘어오는 전이압
    k0pp: float = 0.0         # Pa⁻¹. K₀″. bme4 만 쓴다 — 다른 형태는 무시한다
    # ── 열 항 ──────────────────────────────────────────────────────────
    # alpha_k 가 0 이면 **이 상에는 발표된 열 상수가 없다** 는 뜻이고, 그러면 이 상은
    # 등온으로 남는다. 0 을 "열팽창이 없다" 로 읽으면 안 된다 — 있는 척하지 않는 것이다.
    alpha_k: float = 0.0      # Pa/K. αK_T. 부피에 무관하다고 두는 Anderson & Goto 근사
    alpha_k_dt: float = 0.0   # Pa/K². (∂αK/∂T)_V. 전자 여기 때문에 금속에만 붙는다
    t_ref: float = 0.0        # K. 이 적합이 놓인 기준의 온도
    t_ref_kind: str = "isotherm"   # "isotherm" | "adiabat" — 아래 delta_t 를 보라
    c_v_ref: float = 0.0      # J kg⁻¹ K⁻¹. 정적비열. 아래 상수 절에 출처가 있다
    # ── 녹는곡선 ───────────────────────────────────────────────────────
    # melt 가 빈 문자열이면 **이 상에는 발표된 녹는곡선이 없다** 는 뜻이고, 그러면
    # 이 상에서는 고체·액체를 판정하지 않는다. alpha_k = 0 과 같은 규율이다.
    melt: str = ""            # "" | "water" | "iron" | "silicate". 어느 곡선을 쓰는가
    melt_scale: float = 1.0   # 녹는점에 곱하는 인자. 합금 핵의 내림폭이 여기 들어온다
    melt_ref: str = ""        # 그 곡선이 어느 논문·표준 어느 절에서 왔는가
    # 규산염 곡선의 조성 가지 (peridotitic | chondritic). **우리 선언이다** — 논문은
    # 두 조성을 나란히 인쇄할 뿐 고르는 법을 말하지 않고, 분화 이력이 고른다는 연결은
    # interior.solve 가 differentiated 에서 시딩한다 (분화 잔류물 = 페리도타이트).
    # 20 GPa 아래는 Monteux 가 조성 하나만 인쇄하므로 이 선택은 **20 GPa 위에서만**
    # 곡선을 바꾼다. melt != "silicate" 인 상은 이 필드를 안 읽는다.
    melt_variant: str = "peridotitic"
    # ── 온도 천장 ──────────────────────────────────────────────────────
    # p_max 와 **같은 종류** 다. 적합이 어디까지 유효한가를 말하지, 물질이 어디서
    # 상을 바꾸는가를 말하지 않는다. 0 이면 선언된 천장이 없다는 뜻이다.
    #
    # melt 와 헷갈리기 쉬워서 적어둔다. melt 는 이 레시피가 **위치를 아는 물리적
    # 전이** 이고 압력에 따라 움직이는 곡선이며, 소비처가 밀도를 안 건드린 채 상태를
    # 이름 붙이는 데 쓴다. t_max 는 곡선이 아니라 적합의 울타리이고, 넘으면 판정이
    # 아니라 거절이 나온다. 초이온상 경계는 melt 와 같은 종류인데 이 레시피에 그
    # 곡선이 없어서, 대신 그 아래에 울타리를 세운 것이다 — 아래 t_over_reason 이
    # 무엇이 그 위에 있는지를 이름 댄다.
    t_max: float = 0.0        # K. 이 상의 적합이 유효한 상한 온도

    @property
    def has_melt(self) -> bool:
        """이 상에 발표된 녹는곡선이 있는가."""
        return bool(self.melt)

    def t_melt(self, p: float) -> float | None:
        """압력 p 에서 이 상이 녹는 온도 [K]. 곡선이 없거나 곡선 밖이면 None.

        **곡선이 자기 분기점을 들고 다닌다.** 물얼음의 녹는곡선 분기점(IAPWS 삼중점)은
        이 파일의 상 전이압(Choukroun & Grasset 2007)과 최대 2.3 % 어긋나고, 어느 쪽도
        상대에 맞춰 옮기지 않는다 — 옮기면 그 값이 속한 적합이 깨진다. 그래서 이 함수는
        상 이름이 아니라 **압력** 으로 분기를 고른다."""
        if not self.melt:
            return None
        if self.melt == "silicate":
            # 규산염은 다성분이라 융해가 점이 아니라 창이다 — 이 함수의 한 값은
            # **솔리더스**(첫 용융이 나타나는 온도)이고, 전체 상태(용융분율)는
            # silicate_melt_fraction 이 단일 진리원으로 낸다. 500 GPa 위는 None
            # (silicate_melt_refusal 이 이유를 말한다).
            base = silicate_solidus(p, self.melt_variant)
        else:
            base = water_t_melt(p) if self.melt == "water" else iron_t_melt(p)
        return None if base is None else base * self.melt_scale

    @property
    def has_thermal(self) -> bool:
        """이 상에 발표된 열 상수가 있는가. 없으면 등온으로 남는다."""
        return self.alpha_k > 0.0 and self.c_v_ref > 0.0

    def delta_t(self, t: float, t_pot: float = 0.0) -> float:
        """이 상의 **기준** 에서 얼마나 뜨거운가. 열압력이 먹는 것이 이 차분이다.

        기준이 두 종류다. 실험실 등온에 맞춘 상(`isotherm`)은 기준이 상수 한 개다.
        PREM 에 맞춘 상(`adiabat`)은 다르다 — PREM 은 **뜨거운 실제 지구** 를 관측한
        것이라 그 적합의 기준이 지구의 지오섬이고, 상수가 아니라 곡선이다. 거기에
        열팽창을 통째로 얹으면 지구를 두 번 데운다.

        단열선은 앵커에 선형이므로(dT/dP = γT/K_S 가 T 에 1차) 그 곡선을 따로 적분할
        필요가 없다. T_ref(P) = T(P)·(T_ref_pot / T_pot) 이고, 차분이 닫힌 형태로 나온다.
        T_pot 이 기준값과 같으면 차분이 **정확히 0** 이다 — 그것이 지구가 안 움직이는
        이유이고, 허용오차가 아니라 항등식이다."""
        if not self.has_thermal or t is None or t <= 0.0:
            return 0.0
        if self.t_ref_kind == "adiabat":
            if t_pot <= 0.0:
                return 0.0
            return t * (1.0 - self.t_ref / t_pot)
        return t - self.t_ref

    def thermal_pressure(self, t: float, t_pot: float = 0.0) -> float:
        """열압력 P_th. 기준 대비 ΔT 의 함수다.

        Anderson & Goto 1989 의 근사를 Seager+ 2007 §IV.2.2 가 쓰는 형태 그대로다 —
        Debye 온도 위에서 αK_T 가 부피에 무관하므로 P_th 가 T 에 선형이다. 금속에는
        전자 여기 때문에 2차 항이 하나 더 붙는다 (Isaak & Anderson 2003)."""
        dt = self.delta_t(t, t_pot)
        return self.alpha_k * dt + 0.5 * self.alpha_k_dt * dt * dt

    def dpdt_v(self, t: float, t_pot: float = 0.0) -> float:
        """(∂P/∂T)_V. 열압력의 기울기이고, 그뤼나이젠 계수가 이걸 먹는다."""
        return self.alpha_k + self.alpha_k_dt * self.delta_t(t, t_pot)

    def gruneisen(self, rho: float, t: float, t_pot: float = 0.0) -> float:
        """그뤼나이젠 계수 γ = (∂P/∂T)_V / (ρ c_V). 단열 기울기가 이걸 먹는다.

        **새 상수가 아니라 항등식이다.** 열압력에 이미 있는 (∂P/∂T)_V 와 Dulong-Petit
        c_V 로 닫힌다. 이 항등식이 맞는지는 얼음 III·V·VI 에서 확인된다 — SeaFreeze 가
        자기 γ 를 따로 들고 있고, 여기 식으로 계산한 값과 소수 넷째 자리까지 같다.
        test_interior.py 가 그 대조를 돌린다."""
        if not self.has_thermal or rho <= 0.0:
            return 0.0
        return self.dpdt_v(t, t_pot) / (rho * self.c_v_ref)

    def pressure(self, rho: float) -> float:
        """ρ 에서 P. 정방향은 닫힌 형태라 이쪽이 값싸다."""
        if self.form == "polytrope":
            # P = K ρ^(1+1/n). ρ₀ 로 나누지 않으므로 rho0 = 0 이어도 된다.
            return self.k0 * rho ** (1.0 + 1.0 / self.k0p)
        x = rho / self.rho0
        if self.form == "bm2":
            return 1.5 * self.k0 * (x ** (7.0 / 3.0) - x ** (5.0 / 3.0))
        if self.form == "bme3":
            return (1.5 * self.k0 * (x ** (7.0 / 3.0) - x ** (5.0 / 3.0))
                    * (1.0 + 0.75 * (self.k0p - 4.0) * (x ** (2.0 / 3.0) - 1.0)))
        if self.form == "bme4":
            # 오일러 유한변형 f = ½[(ρ/ρ₀)^(2/3) − 1] 로 쓴 4차 BME.
            #   P = 3K₀ f (1+2f)^(5/2) [1 + (3/2)(K₀′−4) f
            #                             + (3/2)(K₀K₀″ + (K₀′−4)(K₀′−3) + 35/9) f²]
            # f² 항을 떼면 3차와 같은 식이 된다 — 위의 bme3 가지가 같은 관계를 x 로
            # 쓴 것이고, test_interior.py 가 두 형태의 항등성을 실제로 재서 확인한다.
            f = 0.5 * (x ** (2.0 / 3.0) - 1.0)
            a = 1.5 * (self.k0p - 4.0)
            b = 1.5 * (self.k0 * self.k0pp
                       + (self.k0p - 4.0) * (self.k0p - 3.0) + 35.0 / 9.0)
            return 3.0 * self.k0 * f * (1.0 + 2.0 * f) ** 2.5 * (1.0 + a * f + b * f * f)
        if self.form == "vinet":
            e = x ** (-1.0 / 3.0)
            return (3.0 * self.k0 * x ** (2.0 / 3.0) * (1.0 - e)
                    * math.exp(1.5 * (self.k0p - 1.0) * (1.0 - e)))
        raise ValueError(f"모르는 EOS 형태 '{self.form}'")

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """P 에서 ρ. 온도를 주면 열압력을 뺀 **냉각 곡선의** 압력에서 뒤집는다.

        전체 압력이 냉각 압력과 열압력의 합이므로(P = P_cold + P_th), 같은 P 를
        지탱하는 밀도는 뜨거울수록 낮다. 열 상수가 없는 상은 P_th 가 0 이라 예전과
        같은 경로를 탄다 — 비트까지 같다.

        정방향은 닫힌 형태이므로 Newton 으로 뒤집는다.

        P(ρ) 는 단조증가라 뿌리가 하나뿐이다. 첫 추측은 선형 압축
        ρ ≈ ρ₀(1 + P/K₀) 이고, 이 자리가 적분 안쪽 고리라 반복 횟수가 그대로
        실행시간이다 — 이분법 200회로는 쓸 수 없이 느렸다.

        폴리트로프는 뒤집기가 닫힌 형태라 반복이 아예 없다."""
        p_th = self.thermal_pressure(t, t_pot)
        if p_th:
            # 열압력이 전체 압력을 넘으면 그 온도에서 이 상은 존재할 수 없다. 냉각
            # 압력을 음수로 넘기면 Newton 이 발산하므로, 영압 밀도로 바닥을 친다.
            p = p - p_th
        if self.form == "polytrope":
            if p <= 0.0:
                return 0.0
            return (p / self.k0) ** (self.k0p / (self.k0p + 1.0))
        if p <= 0.0:
            return self.rho0
        rho = self.rho0 * (1.0 + p / self.k0) ** 0.4
        for _ in range(60):
            f = self.pressure(rho) - p
            if abs(f) <= 1e-9 * max(p, 1.0):
                return rho
            h = rho * 1e-7
            dfd = (self.pressure(rho + h) - self.pressure(rho - h)) / (2.0 * h)
            if dfd <= 0.0:
                break
            step = f / dfd
            nxt = rho - step
            if nxt <= self.rho0 * 0.5:
                nxt = 0.5 * (rho + self.rho0 * 0.5)
            if abs(nxt - rho) <= 1e-12 * rho:
                return nxt
            rho = nxt
        raise ValueError(f"{self.name}: P={p:.3e} Pa 에서 밀도가 수렴하지 않는다")


@dataclass(frozen=True)
class Material:
    """압력 구간별로 갈리는 상들의 열. 구간 밖은 이름 붙여 거절한다."""
    name: str
    label_ko: str
    phases: tuple[Phase, ...]
    gap_reason: str = ""      # 상 사이 빈 구간에 붙일 설명
    over_reason: str = ("{p_gpa:.1f} GPa 는 근거 있는 상의 상한({max_gpa:.1f} GPa) 위다")
    t_over_reason: str = ("{t_k:.0f} K 는 '{phase}' 적합의 상한({t_max:.0f} K) 위다")

    @property
    def rho0(self) -> float:
        """영압 밀도. 어떤 조성이 어떤 평균밀도를 낼 수 있는지의 하한이다."""
        return self.phases[0].rho0

    @property
    def p_max(self) -> float:
        return self.phases[-1].p_max

    def rho_seed(self, mass_kg: float) -> float:
        """사격의 괄호를 잡을 때만 쓰는 밀도 척도. 계산 결과에는 들어가지 않는다.

        응축상은 영압 밀도가 그 척도다. 폴리트로프는 영압에서 밀도가 0 이라 그걸 쓸 수
        없고, 대신 **n = 1 해의 평균밀도** 를 쓴다. n = 1 은 반지름이 질량과 무관하게
        R = √(πK/2G) 로 고정되므로 (Helled+ 2022 §2), 그 반지름에서의 평균밀도
        3M/(4πR³) 이 K 와 질량만으로 정해진다 — 새로 가정한 상수가 아니다."""
        ph = self.phases[0]
        if ph.rho0 > 0.0:
            return ph.rho0
        if ph.form == "polytrope" and abs(ph.k0p - 1.0) < 1e-9:
            r = polytrope_radius_n1(ph.k0)
            return 3.0 * mass_kg / (4.0 * math.pi * r ** 3)
        raise ValueError(f"{self.name}: 괄호잡기용 밀도 척도를 정할 수 없다")

    def phase_at(self, p: float) -> Phase:
        """이 압력에서 유효한 상. 없으면 왜 없는지를 들고 던진다."""
        for ph in self.phases:
            if p < ph.p_min:
                raise PhaseGap(self.name, p, self.gap_reason.format(p_gpa=p / 1e9))
            if p <= ph.p_max:
                return ph
        raise PhaseGap(self.name, p, self.over_reason.format(
            p_gpa=p / 1e9, max_gpa=self.p_max / 1e9))

    @property
    def has_thermal(self) -> bool:
        """모든 상에 열 상수가 있는가. 하나라도 없으면 이 재료는 부분적으로 등온이다."""
        return all(ph.has_thermal for ph in self.phases)

    def cold_phases(self) -> tuple[str, ...]:
        """열 상수가 없어 등온으로 남는 상들. 없는 척하지 않고 이름을 들고 있는다."""
        return tuple(ph.name for ph in self.phases if not ph.has_thermal)

    def melt_free_phases(self) -> tuple[str, ...]:
        """발표된 녹는곡선이 없는 상들. cold_phases() 와 같은 규율이다."""
        return tuple(ph.name for ph in self.phases if not ph.has_melt)

    def t_melt(self, p: float) -> float | None:
        """압력 p 에서 이 재료가 녹는 온도 [K]. 곡선이 없으면 None."""
        return self.phase_at(p).t_melt(p)

    def liquid_at(self, p: float, t: float) -> bool | None:
        """이 (P, T) 에서 이 재료가 액체인가. 곡선이 없거나 닿지 않으면 None.

        `t > t_melt(p)` 와 같은 답을 뒤집기 없이 낸다. 물만 이 길을 갖는다 — 철의 곡선은
        core_state 가 층 경계에서 몇 번 묻는 것이라 t_melt 로 충분하다."""
        ph = self.phase_at(p)
        if ph.melt != "water":
            return None
        if ph.melt_scale != 1.0:
            t_m = ph.t_melt(p)
            return None if t_m is None else t > t_m
        return water_liquid_at(p, t)

    def check_temperature(self, p: float, t: float) -> None:
        """이 압력의 상이 이 온도에서도 유효한가. 아니면 이름 대며 던진다."""
        if t <= 0.0:
            return              # 온도가 선언되지 않았다. 등온 경로다
        ph = self.phase_at(p)
        if ph.t_max and t > ph.t_max:
            raise PhaseGap(self.name, p, self.t_over_reason.format(
                t_k=t, t_max=ph.t_max, phase=ph.name, p_gpa=p / 1e9), t)

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        self.check_temperature(p, t)
        return self.phase_at(p).density(p, t, t_pot)

    def gruneisen(self, p: float, rho: float, t: float, t_pot: float = 0.0) -> float:
        return self.phase_at(p).gruneisen(rho, t, t_pot)

    def k_t(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """등온 체적탄성률 K_T [Pa]. 냉각 곡선의 수치 미분이다.

        위쪽 반 걸음이 이 재료의 상한을 넘으면 그 걸음을 상한에서 자른다 — 사격의 괄호가 상한 바로
        위에 시험점을 놓을 때(antigorite 10 GPa 에서 실제로 걸렸다, 2026-08-30 F2) 미분이 상한 밖을
        찔러 거절을 만들면 안 된다. 상한에 닿지 않는 자리에서는 예전과 같은 중앙차분이다."""
        h = p * 1e-4
        rho = self.density(p, t, t_pot)
        p_hi = min(p + h, self.p_max)
        p_lo = max(p - h, 1.0)
        if p_hi <= p_lo:
            return 0.0
        d_hi = self.density(p_hi, t, t_pot)
        d_lo = self.density(p_lo, t, t_pot)
        return 0.0 if d_hi <= d_lo else rho * (p_hi - p_lo) / (d_hi - d_lo)

    def c_p(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """정압비열 c_P = c_V (1 + αγT) [J/kg/K]. 새 상수가 아니라 항등식이다.

        α = (∂P/∂T)_V / K_T 이고 γ = (∂P/∂T)_V / (ρ c_V) 이므로, 이 파일이 이미 들고
        있는 것들로 닫힌다. 열 상수가 없는 상은 0 을 낸다 — 없는 척하지 않는다."""
        ph = self.phase_at(p)
        if not ph.has_thermal or t <= 0.0:
            return 0.0
        rho = self.density(p, t, t_pot)
        k_t = self.k_t(p, t, t_pot)
        if k_t <= 0.0 or rho <= 0.0:
            return ph.c_v_ref + self._latent_cp(ph, p, t)
        dpdt = ph.dpdt_v(t, t_pot)
        gamma = dpdt / (rho * ph.c_v_ref)
        alpha = dpdt / k_t
        return ph.c_v_ref * (1.0 + alpha * gamma * t) + self._latent_cp(ph, p, t)

    @staticmethod
    def _latent_cp(ph, p: float, t: float) -> float:
        """부분용융 창 안의 잠열을 겉보기 비열로 — Monteux+ 2016 식 (17), Solomatov 2007.

            C′_p = C_p + ΔH / (T_liq − T_sol)

        창 밖(완전 고체·완전 액체·곡선 밖·온도 미선언)은 0 을 더한다. 상 경계에서
        온도를 계단으로 밟는 대신 창에서 단열선을 평평하게 만드는 적분기-안정
        패턴이고, 폭(T_liq − T_sol)은 솔리더스·리퀴더스가 따로 인쇄된 측정에서 온다
        (140 GPa 위 단일점 구간만 선언된 명목 폭 — SILICATE_MELT_POINT_WIDTH)."""
        if ph.melt != "silicate" or t <= 0.0:
            return 0.0
        sol = silicate_solidus(p, ph.melt_variant)
        if sol is None or not sol < t:
            return 0.0
        liq = silicate_liquidus(p, ph.melt_variant)
        if t >= liq:
            return 0.0
        return SILICATE_MELT_DH / (liq - sol)

    def grad_ad(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """(∂lnT/∂lnP)_S = γ P / K_S. 혼합이 이걸 c_P 로 가중해 합친다.

        부분용융 창 안에서는 기울기에 C_p/C′_p 를 곱한다 — ∇_ad ∝ 1/c_p 이고 잠열이
        겉보기 비열을 키우므로(식 (17), _latent_cp) 단열선이 창에서 평평해진다.
        인쇄된 식 (16)의 α′ 은 비채택이다: 식 (15)의 용융 밀도를 채택하지 않는 채로
        α′ 만 넣으면 고체 밀도 기둥에 용융 팽창 기울기를 섞는 비일관이 된다
        (SILICATE_MELT_DH 블록 주석)."""
        if t <= 0.0 or p <= 0.0:
            return 0.0
        rho = self.density(p, t, t_pot)
        gamma = self.gruneisen(p, rho, t, t_pot)
        if gamma <= 0.0:
            return 0.0
        k_s = self.k_t(p, t, t_pot) + self.phase_at(p).dpdt_v(t, t_pot) * gamma * t
        if k_s <= 0.0:
            return 0.0
        grad = gamma * p / k_s
        ph = self.phase_at(p)
        lat = self._latent_cp(ph, p, t)
        if lat > 0.0:
            base = self.c_p(p, t, t_pot) - lat
            if base > 0.0:
                grad *= base / (base + lat)
        return grad


# ── 섞인 층 ─────────────────────────────────────────────────────────────
#
# 위의 재료는 전부 순수하다. 금속이 가라앉지 않아 규산염에 섞여 있는 천체나, 중원소가
# 수소-헬륨 외피에 녹아 있는 거대행성은 **한 층 안에 두 물질** 이고, 그걸 표현하려면
# 새 상태방정식이 아니라 있는 것 둘을 합치는 규칙이 필요하다.
#
# 쓰는 규칙은 **부피 가법 혼합(additive volume law, AVL)** 이다. 같은 압력에서 각
# 성분이 자기 부피를 차지하고, 그 부피를 질량분율로 더한다.
#
#     1/ρ_mix(P) = Σ_i  w_i / ρ_i(P)          w_i 는 질량분율, Σw_i = 1
#
# Baraffe+ 2008 §3.3 (arXiv:0802.1810) 이 이 형태를 그대로 적는다 — "the EOS of the
# mixture is simply the mass-weighted interpolation of each species contribution at
# constant intensive variables, P and T". 같은 문단이 이 규칙을 "exact in the ideal gas
# limit, without restriction on the species mass fractions and densities" 라고 부르고,
# 대신 "the interactions between the three different fluids ... are not taken into
# account" 라고 못박는다. 그 두 문장이 이 규칙의 내용과 값이다.
#
# 이 규칙은 거대행성 상태방정식의 표준이고 새로 고른 것이 아니다. Saumon+ 1995
# (1995ApJS...99..713S) 가 H/He 표를 "the additive volume rule and an additional ideal
# entropy-of-mixing term" 으로 만들었고, Chabrier+ 2019 (arXiv:1902.01852) 가 24년 뒤에
# 같은 말을 다시 한다 — "based on the so-called additive volume law and thus does not
# take into account the interactions between the two species".
#
# **유효 한계는 그 셋이 말해 주지 않는다. 규칙을 쓰는 논문이지 시험하는 논문이 아니라서다.**
# 시험한 것은 Vorberger+ 2007 (arXiv:cond-mat/0609476) 이고, 거대행성 내부 조건의 H-He
# 혼합을 제일원리 DFT-MD 로 돌려 "investigate the validity of the widely used linear
# mixing approximation" 했다. 결과가 이렇다.
#
#   * 정압에서 **부피 편차가 최대 8 %** ("deviations of up to 8% in energy and volume
#     from linear mixing at constant pressure in the region of molecular dissociation").
#   * 가장 나쁜 자리가 **분자 해리 구간** 이다. 순수 분자상에서는 "LM is a good
#     approximation" 이라고 같은 논문이 적고, 목성형 혼합비 x≈0.14 에서 압력 편차가
#     500 K 의 ~0 에서 5000 K 의 10 % 까지 간다. 부피 편차는 "slightly smaller than the
#     one in the pressure" 다.
#
# 그래서 이 규칙이 이 파일에 들고 오는 오차는 **8 % 수준으로 유계** 이고, 그 크기가
# 어디서 나는지도 이름이 있다. 그게 유효 한계다.
#
# **암석-금속 혼합에는 그런 수가 없다.** 같은 규칙을 쓰는 것이 관행이지만, ADS 로 찾은
# 범위에서 철-규산염 혼합의 AVL 편차를 정량한 논문은 없었다. 문헌이 침묵하므로 여기서도
# 침묵한다 — H-He 의 8 % 를 암석에 옮겨 적지 않는다. 그쪽 유효성의 근거는 두 성분이
# 화학적으로 섞이지 않고 각자 자기 상으로 남는다는 것뿐이고, 그 이상은 주장하지 않는다.
#
# **행성 얼음(물·암모니아·메탄)에는 있다.** 2026-08-27 에는 이 자리도 침묵이었는데,
# 얼음거대행성 외피를 조사하면서 나왔다. Bethkenhagen+ 2017 (arXiv:1709.04133) 이
# 1000 GPa · 20 000 K 까지의 DFT-MD 자료로 세 1:1 이성분 혼합과 2:1:4 삼성분 혼합을
# 실제 혼합과 대조했다.
#
#   * 이성분 — "deviations of the linear mixing approximation from the results of the real
#     mixture are generally small; for the thermal EOS they amount to 4% or less". 같은
#     논문이 그 4 % 를 전형값이 아니라 **상한** 이라고 부른다.
#   * 삼성분(천왕성 프로파일 셋) — "maximum deviations in density amount to up to 2.1%"
#     이고 10 000 K 위에서는 0.5 % 아래로 떨어진다.
#   * **부호가 있다** — "the LMA overestimates the density, while the internal energy is
#     underestimated". 편차가 큰 자리도 이름이 있다: 성분 하나만 초이온이 되거나 탄소가
#     화학반응을 시작하는 구간이다.
#
# 즉 행성 얼음은 부피 가법 아래에서 H-He 보다 **얌전하다** (4 % 대 8 %).
#
# **이 수가 무엇을 덮고 무엇을 안 덮는지 적어둔다.** 이건 세 성분의 순수 상태방정식을 다
# 갖춘 뒤 그것들을 부피 가법으로 섞는 **그 단계** 의 한계다. 물 하나로 얼음 전체를
# 대신하는 흔한 근사의 대가가 아니다 — 그 길은 이 단계를 아예 밟지 않는다. 물 EOS 와
# 혼합물 EOS 의 차이는 다른 수이고, 인용한 문헌 범위에서 정량되지 않았다. 같은 논문
# 결론부가 세 순수 성분의 열역학 퍼텐셜 구축을 후속 과제로 꼽는 것 자체가 물 하나로는
# 안 된다는 전제이고, 그 §V 가 water-only 모형과 icy 모형을 대조하는 절이다. H-He 의
# 8 % 를 암석에 옮겨 적지 않았던 규율 그대로, 이 수도 그쪽으로 옮겨 적지 않는다.
#
# 소비처는 아직 없다 — 메탄의 상태방정식이 이 파일에 없어서다(암모니아는 2026-08-30 C4 재개로
# 들어왔다: 아래 Ammonia). 그래도 여기 둔다. 침묵이 아니게 된 자리를 침묵으로 남겨두면 다음
# 조사가 같은 길을 다시 걷는다.
AVL_VOLUME_DEVIATION = 0.08   # Vorberger+ 2007 초록. 정압 부피, H-He, 분자 해리 구간
AVL_DEVIATION_REGIME = "분자 해리 구간 (순수 분자상에서는 ~0)"
AVL_ICES_DEVIATION = 0.04     # Bethkenhagen+ 2017 초록. 1:1 이성분, 밀도, **상한**
AVL_ICES_TERNARY_DEVIATION = 0.021   # 같은 논문. 2:1:4 삼성분, 천왕성 프로파일 위
AVL_ICES_SIGN = "밀도는 과대평가, 내부에너지는 과소평가"

# 얼음거대행성 외피의 조성비. **관측이 묶지 않는다** — 항성 조성과 형성 이력이 정하고
# 이 레시피에 그 둘이 없으므로, 들어온다면 envelope_z 와 같은 **선언** 이 된다.
# 기본값으로 쓸 만한 발표값은 태양 H:C:N:O 조성에서 나온다 (Bethkenhagen+ 2017 §V):
# Z_CH4 : Z_NH3 : Z_H2O = 0.31 : 0.08 : 0.61 (질량분율). 같은 절이 자기들이 시뮬레이션한
# 2:1:4 분자비를 고른 이유를 "resemblance to the solar abundances of about 4:1:7 of
# C:N:O (Asplund+ 2009)" 로 적는다.
SOLAR_ICE_MASS_FRACTIONS = {"ch4": 0.31, "nh3": 0.08, "h2o": 0.61}


@dataclass(frozen=True)
class Mixture:
    """한 층 안에 섞인 두 재료 이상. 부피 가법으로 합친다.

    `Material` 과 같은 자리에 꽂히도록 같은 이름의 것들을 낸다 — `density(p)`,
    `rho0`, `p_max`, `rho_seed(mass)`. 적분기는 층에 들어온 것이 순수 재료인지
    혼합인지 묻지 않는다."""
    name: str
    label_ko: str
    parts: tuple[tuple[Material, float], ...]   # (재료, 질량분율)

    def __post_init__(self) -> None:
        if not self.parts:
            raise ValueError(f"{self.name}: 성분이 없다")
        total = sum(w for _m, w in self.parts)
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"{self.name}: 질량분율 합이 {total} 다, 1 이어야 한다")
        if any(w < 0.0 for _m, w in self.parts):
            raise ValueError(f"{self.name}: 음수 질량분율")

    @property
    def rho0(self) -> float:
        """영압 밀도. 성분 중 하나라도 영압에서 0 이면(폴리트로프) 혼합도 0 이다."""
        if any(m.rho0 <= 0.0 for m, w in self.parts if w > 0.0):
            return 0.0
        return 1.0 / sum(w / m.rho0 for m, w in self.parts if w > 0.0)

    @property
    def p_max(self) -> float:
        """**가장 낮은 성분 상한** 이 혼합의 상한이다.

        하나가 근거 구간을 벗어나면 그 압력의 혼합 밀도는 근거가 없다. 가장 높은
        상한을 쓰면 근거 없는 외삽을 근거 있는 성분 뒤에 숨기게 된다."""
        return min(m.p_max for m, w in self.parts if w > 0.0)

    def rho_seed(self, mass_kg: float) -> float:
        """사격 괄호잡기용 밀도 척도. 성분들의 척도를 같은 규칙으로 합친다."""
        return 1.0 / sum(w / m.rho_seed(mass_kg)
                         for m, w in self.parts if w > 0.0)

    @property
    def has_thermal(self) -> bool:
        return all(m.has_thermal for m, w in self.parts if w > 0.0)

    def cold_phases(self) -> tuple[str, ...]:
        out: list[str] = []
        for m, w in self.parts:
            if w > 0.0:
                out.extend(m.cold_phases())
        return tuple(out)

    def melt_free_phases(self) -> tuple[str, ...]:
        out: list[str] = []
        for m, w in self.parts:
            if w > 0.0:
                out.extend(m.melt_free_phases())
        return tuple(out)

    def t_melt(self, p: float) -> float | None:
        """섞인 층에는 녹는점이 하나가 아니다. **판정하지 않는다.**

        두 성분이 각자의 녹는점을 가지고, 그 사이는 부분용융이라 고상선과 액상선 두
        곡선이 필요하다 — 순물질의 녹는점 하나가 아니다. 이 파일에 그 두 곡선이 없으므로
        여기서는 답하지 않는다. 미분화 천체와 중원소 섞인 외피가 이 자리에 온다."""
        return None

    def check_temperature(self, p: float, t: float) -> None:
        for m, w in self.parts:
            if w > 0.0:
                m.check_temperature(p, t)

    @property
    def p_floor(self) -> float:
        """성분 중 하나라도 압력 바닥을 말하면 혼합도 거기서 멈춘다. 중원소가 녹아
        있어도 외피는 여전히 기체이고, P = 0 인 표면이 없는 것은 그대로다."""
        return max((getattr(m, "p_floor", 0.0)
                    for m, w in self.parts if w > 0.0), default=0.0)

    def in_domain(self, p: float, t: float) -> bool:
        return all(m.in_domain(p, t) for m, w in self.parts
                   if w > 0.0 and hasattr(m, "in_domain"))

    def c_p(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """정압비열도 질량분율로 더한다. 엔트로피가 가법이면 그 온도 도함수도 가법이다."""
        return sum(w * m.c_p(p, t, t_pot) for m, w in self.parts if w > 0.0)

    def grad_ad(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """혼합의 단열 기울기. **c_P 로 가중한 평균이지 부피 가법이 아니다.**

            ∇_ad,mix = Σ wᵢ c_P,ᵢ ∇_ad,ᵢ / Σ wᵢ c_P,ᵢ

        밀도는 부피가 가법이라 조화평균으로 합쳐지지만 ∇_ad 는 엔트로피의 도함수이고,
        엔트로피는 **가법 그 자체** 다. Chabrier+ 2019 §V 가 자기 혼합 규칙을 그렇게
        적는다 — "the so-called 'additive volume law' ... is based on the additivity of
        the extensive variables (volume, energy, **entropy**, ...) at constant intensive
        variables (P,T)", 결론부에서 다시 "simply taking into account the ideal mixing
        entropy contribution between the two species". 같은 문장이 이 파일이 밀도 규칙에
        이미 인용해 둔 그 문장이다.

        그 전제에서 닫힌 형태가 나온다. (∂S/∂P)_T 와 (∂S/∂T)_P 가 각각 가법이고
        (∂S/∂P)_T,ᵢ = −c_P,ᵢ ∇_ad,ᵢ / P, (∂S/∂T)_P,ᵢ = c_P,ᵢ / T 이므로,
        ∇_ad = −(P/T)(∂S/∂P)_T/(∂S/∂T)_P 에 넣으면 위 식이 된다. 이상 혼합
        엔트로피 항은 조성만의 함수라 두 도함수에서 사라진다.

        **2026-08-28 까지 이 자리가 비어 있었고, 그게 조용한 결함이었다.** 혼합에
        ∇_ad 가 없으면 적분기가 γ 와 K_S 로 **재조립한** 기울기로 되돌아갔고, 표를
        들여온 이유가 바로 그 조립을 그만두는 것이었다. 중원소를 한 톨(Z = 0.02) 넣는
        순간 토성의 표면 온도가 135 K 대신 19 K 로 나왔고, 온도 고리가 매 통과 7배씩
        중심 온도를 올리다 가짜 가지로 걸어갔다."""
        num = den = 0.0
        for m, w in self.parts:
            if w <= 0.0:
                continue
            if not m.has_thermal:
                # **열 상수가 없는 성분은 온도를 그대로 통과시킨다** — 순수 재료에서 cold_phases 가
                # 받는 것과 같은 규칙(그 상에서 dT/dP = 0). 열 상수가 있는 성분들만 c_P 로 가중한다.
                # 2026-08-30 에 antigorite 가 들어오며 생긴 자리다: Hilairet+ 2006 은 상온뿐이라
                # 열항이 없고, 그 결핍은 지어내지 않고 등급과 note 가 말한다.
                #
                # **중첩 모서리.** 성분이 자기도 Mixture 면 Mixture.has_thermal 이 all() 이라 cold 성분
                # 하나 때문에 그 안의 **열 성분까지 통째로** 통과된다. 2026-08-30 F2 에서 antigorite 가
                # 열항(Holland & Powell 1998)을 얻어 이 저장소의 어느 재료도 더는 cold 가 아니므로, 이 분기
                # 자체가 지금은 **어느 혼합에서도 안 걸린다** — 사문석화 암석도 전 성분이 열 성분이다. 분기는
                # 열 상수 없는 재료가 다시 들어올 때를 위해 남겨 두고, 그때 성분이 Mixture 면 flatten 해서
                # 열 부분과 cold 부분을 따로 이 고리에 넣을 것.
                continue
            c = m.c_p(p, t, t_pot)
            if c <= 0.0:
                # 발표된 열용량이 없는 성분이 있으면 가중치를 지어낼 수 없다.
                raise PhaseGap(
                    self.name, p,
                    f"'{m.name}' 의 정압비열이 없어 혼합의 단열 기울기를 c_P 로 가중할 "
                    "수 없다. 엔트로피 가법에서 나오는 가중치가 c_P 인데 그 값이 이 "
                    "재료에 없으므로, 지어내는 대신 여기서 멈춘다.", t)
            g = m.grad_ad(p, t, t_pot)
            num += w * c * g
            den += w * c
        return 0.0 if den <= 0.0 else num / den

    def dtdp_adiabat(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """dT/dP = ∇_ad · T / P. 적분기가 이걸 우선해서 조립 경로를 안 탄다."""
        if t <= 0.0 or p <= 0.0:
            return 0.0
        return self.grad_ad(p, t, t_pot) * t / p

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """압력 p 에서 혼합 밀도. 성분마다 **같은 압력과 같은 온도** 에서 평가한다.

        성분이 자기 근거 구간 밖이면 그 성분이 PhaseGap 을 던지고, 그게 그대로
        올라간다 — 혼합이 그 사실을 삼키지 않는다."""
        return 1.0 / sum(w / m.density(p, t, t_pot) for m, w in self.parts if w > 0.0)

    def gruneisen(self, p: float, rho: float, t: float, t_pot: float = 0.0) -> float:
        """혼합의 γ. 성분의 γ 를 질량분율로 더한다 — 부피 가법과 같은 결이다."""
        return sum(w * m.gruneisen(p, m.density(p, t, t_pot), t, t_pot)
                   for m, w in self.parts if w > 0.0)


# ── 뜨거운 물 — 사다리가 아니라 이웃 ────────────────────────────────────
#
# 위의 물 사다리는 20 ~ 1800 K 의 응축상이다. 얼음거대행성의 '얼음' 맨틀은 그 위에서
# 시작해 위로 가므로 (100 GPa 에서 5000~7000 K, 중심 5500~5700 K — Scheibe+ 2019),
# 사다리를 늘리는 것이 아니라 **다른 상** 을 나란히 세운다.
#
# 상태방정식은 water_hot.py 에 있다. 여기 있는 것은 그것을 적분기가 먹을 수 있는 모양으로
# 감싸는 껍질이다 — Material 과 같은 것들을 내지만 상(Phase) 의 열이 아니다. 냉각 곡선과
# 열압력으로 갈리지 않고 P(ρ,T) 가 통째로 하나이기 때문이고, 그래서 Phase 를 억지로
# 씌우는 대신 같은 자리에 꽂히는 별개의 것으로 둔다.
@dataclass(frozen=True)
class HotWater:
    """유체·초이온 물. `Material` 과 같은 자리에 꽂히지만 상의 열이 아니다."""
    name: str = "h2o_hot"
    label_ko: str = "뜨거운 물 (유체·초이온)"

    @property
    def rho0(self) -> float:
        """괄호잡기용 영압 밀도. 이 적합은 영압에서 뜻이 없으므로 유효 하한을 쓴다."""
        return water_hot.RHO_MIN

    @property
    def p_max(self) -> float:
        """압력 상한. 이 적합은 밀도로 잘리므로, 상한 밀도의 압력을 상한으로 쓴다.

        온도에 따라 움직이지만, 괄호잡기와 거절 판정에만 쓰이므로 이 갈래에서 실제로
        도달하는 가장 낮은 온도(T_MIN)에서 잡는다 — 가장 보수적인 자리다."""
        return water_hot.pressure(water_hot.RHO_MAX, water_hot.T_MIN)

    def rho_seed(self, mass_kg: float) -> float:
        return water_hot.RHO_MIN

    @property
    def has_thermal(self) -> bool:
        return True

    def cold_phases(self) -> tuple[str, ...]:
        return ()

    def melt_free_phases(self) -> tuple[str, ...]:
        """녹는곡선이 없다 — **있을 자리가 아니다.** 이 재료는 이미 유체다."""
        return (self.name,)

    def t_melt(self, p: float) -> float | None:
        return None

    def check_temperature(self, p: float, t: float) -> None:
        """이 적합이 유효한 온도 구간 밖인가. 양쪽 다 이름을 대며 거절한다."""
        if t <= 0.0:
            raise PhaseGap(
                self.name, p,
                "뜨거운 물은 등온 경로로 풀 수 없다. 이 적합은 P(ρ,T) 가 통째로 하나라 "
                "온도가 인자이고, 얼음 사다리처럼 냉각 곡선을 따로 갖고 있지 않다. "
                "포텐셜 온도를 선언하면 이 층이 풀린다.")
        if t < water_hot.T_MIN:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 이 적합이 유체에 대해 적은 하한({water_hot.T_MIN:.0f} K) 아래다 — "
                "Mazevet+ 2019 §3.1 이 ρ ≳ 1 g/cc 의 적합 구간을 '10³ K ≲ T' 로 적는다. 녹는곡선은 "
                "여기를 액체라 한다. 그 온도의 조밀한 액체는 h2o_liquid_dense (SeaFreeze water2 / Brown 2018, "
                "굳힌 창 360–1100 K · 등온선별 천장 2.3–36 GPa)가 받고, 그 천장 위·1000 K 아래는 어느 표현도 "
                "없다. 고체는 얼음 사다리가 받는다.",
                t, too_cold=True)
        if t > water_hot.T_MAX:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 이 적합의 상한({water_hot.T_MAX:.0f} K) 위다. "
                "Mazevet+ 2019 초록이 'for temperatures below 50,000K' 로 적는다.", t)

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        self.check_temperature(p, t)
        return water_hot.density(p, t)

    def gruneisen(self, p: float, rho: float, t: float, t_pot: float = 0.0) -> float:
        if t <= 0.0:
            return 0.0
        return water_hot.gruneisen(rho, t)

    def c_p(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """정압비열 c_P = c_V (1 + αγT) [J/kg/K]. Material 과 같은 항등식이고, c_V 와 (∂P/∂T)_ρ 는
        water_hot 의 P(ρ,T)·U(ρ,T) 유한차분이다. **혼합(Mixture)이 ∇_ad 를 c_P 로 가중할 때만 쓴다**
        — 적분기의 단열 기울기는 예전 그대로 gruneisen 과 수치 K_S 로 조립하므로(dtdp_adiabat 을
        일부러 두지 않는다), 이 함수가 생겨도 순수 물 경로는 비트까지 같다."""
        c_v, dpdt, k_t = self._thermal(p, t)
        if c_v <= 0.0:
            return 0.0
        if k_t <= 0.0:
            return c_v
        rho = water_hot.density(p, t)
        gamma = dpdt / (rho * c_v)
        alpha = dpdt / k_t
        return c_v * (1.0 + alpha * gamma * t)

    def grad_ad(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """(∂lnT/∂lnP)_S = γ P / K_S, K_S = K_T (1 + αγT). c_p 와 같은 유한차분에서 닫힌다."""
        if t <= 0.0 or p <= 0.0:
            return 0.0
        c_v, dpdt, k_t = self._thermal(p, t)
        if c_v <= 0.0 or k_t <= 0.0:
            return 0.0
        rho = water_hot.density(p, t)
        gamma = dpdt / (rho * c_v)
        k_s = k_t + dpdt * gamma * t
        return 0.0 if k_s <= 0.0 else gamma * p / k_s

    def _thermal(self, p: float, t: float) -> tuple[float, float, float]:
        """(c_V, (∂P/∂T)_ρ, K_T) 를 water_hot 의 P·U 중앙차분으로. h = 1 % (gruneisen 과 같은 걸음)."""
        if t <= 0.0:
            return 0.0, 0.0, 0.0
        rho = water_hot.density(p, t)
        h = 0.01 * t
        dpdt = (water_hot.pressure(rho, t + h) - water_hot.pressure(rho, t - h)) / (2.0 * h)
        c_v = (water_hot.internal_energy(rho, t + h)
               - water_hot.internal_energy(rho, t - h)) / (2.0 * h)
        dr = 0.01 * rho
        k_t = rho * (water_hot.pressure(rho + dr, t) - water_hot.pressure(rho - dr, t)) / (2.0 * dr)
        return c_v, dpdt, k_t

    def phase_at(self, p: float):
        """단열 기울기가 (∂P/∂T)_V 를 묻는다. 상이 아니라 닫힘 하나로 답한다."""
        return _HotWaterSlope(p)


@dataclass(frozen=True)
class _HotWaterSlope:
    """`_adiabatic_dtdp` 가 K_S 를 만들 때 쓰는 (∂P/∂T)_V. 유한차분이다."""
    p: float

    def dpdt_v(self, t: float, t_pot: float = 0.0) -> float:
        if t <= 0.0:
            return 0.0
        rho = water_hot.density(self.p, t)
        h = 0.01 * t
        return (water_hot.pressure(rho, t + h) - water_hot.pressure(rho, t - h)) / (2.0 * h)


H2O_HOT = HotWater()


# ── 암모니아 — 표 하나, 아직 소비처 없음 ──────────────────────────────────
#
# 2026-08-30 C4 가 "표에 닿을 수 없다" 로 닫혔고, 오너가 논문을 받아오면서 그 조건이 뒤집혔다:
# Bethkenhagen, French & Redmer 2013 (2013JChPh.138w4504B) 의 Appendix B Table I 이 암모니아의
# p(ρ,T)·u(ρ,T) 를 93 점 인쇄한다 — 저장소도 적합식도 없고 인쇄가 배포다. ammonia_table.py 가
# 그 표를 굳힌 것이고(tools/make_ammonia_table.py, PDF 텍스트층 파싱 + 인쇄본 대조), 여기는
# 적분기가 먹을 수 있는 껍질이다 — HotWater 와 같은 모양, P(ρ,T) 가 통째로 하나라 Phase 가 아니다.
#
# **어느 천체에도 아직 배선되지 않았다.** 암모니아 혼자는 얼음거대행성 맨틀이 아니고, 메탄 표는
# 여전히 없다. 이것이 당장 여는 것은 **검사** 다 — 물(Mazevet+ 2019)과 암모니아(이 표)를 같은
# (P, T) 에서 읽어 부피 가법으로 섞으면 물 하나로 두 성분을 대신할 때의 값이 처음으로 표에서
# 나온다. test_ammonia.py 가 그것을 재고 interior-core.md C4 가 결과를 든다.
#
# **규약 — 내부에너지에 진동(핵 양자) 보정이 들어 있다.** 이 표의 u 는 u = u* + u_vc (2013 식 (1),
# Appendix B, Fig. 7 캡션). Bethkenhagen+ 2017 §II.4 는 같은 데이터에서 그 보정을 **뺐다**. 이
# 저장소는 인쇄된(보정된) 값을 굳힌다 — 인쇄된 것이 그것뿐이고, 물리적으로 맞는 쪽이다. 노출은
# c_P 와 ∇_ad 뿐이다(u 의 온도 도함수). 밀도 혼합은 p 만 읽으므로 규약과 무관하고, 논문이 p_vc 를
# 이 데이터에서 무시할 만하다고 적되 "this should not be understood as a general result" 라 한다.
# ammonia_table.U_INCLUDES_VIBRATIONAL_CORRECTION 이 그 사실을 들고, test_ammonia.py 가 확인한다.
NH3_REF = ("Bethkenhagen, French & Redmer 2013 (2013JChPh.138w4504B) Appendix B Table I — "
           "FT-DFT-MD 암모니아 p(ρ,T)·u(ρ,T), 0.5–3.0 g/cm³ · 500–10 000 K · 0.309–333.2 GPa, "
           "압력 2 % (표시점 5 %)")


@dataclass(frozen=True)
class Ammonia:
    """암모니아 유체·초이온·해리상, 굳힌 표 위에서. `Material` 과 같은 자리에 꽂힌다."""
    name: str = "nh3"
    label_ko: str = "암모니아 (표, Bethkenhagen+ 2013)"

    @property
    def rho0(self) -> float:
        """괄호잡기용. 표의 최저 밀도 — 영압은 표 밖이다."""
        return 0.5e3

    @property
    def p_max(self) -> float:
        """표의 가장 큰 압력(3.0 g/cm³ · 10 000 K). 온도마다의 실제 천장은 density 가 표 이름을
        대며 거절한다 — 격자가 들쭉날쭉해서 하나의 수로 말할 수 없다."""
        return ammonia_table.P_MAX_PA

    def rho_seed(self, mass_kg: float) -> float:
        return 1.5e3

    @property
    def has_thermal(self) -> bool:
        return True

    def cold_phases(self) -> tuple[str, ...]:
        return ()

    def melt_free_phases(self) -> tuple[str, ...]:
        """녹는곡선이 없다 — 표는 유체·초이온·해리상을 한 격자로 잇고, 1차 전이(Fig. 6·7 의
        점선)를 가로질러 보간한다. 어디가 전이인지는 이 재료가 판정하지 않는다."""
        return (self.name,)

    def t_melt(self, p: float) -> float | None:
        return None

    def in_domain(self, p: float, t: float) -> bool:
        return ammonia_table.in_domain(p, t)

    def check_temperature(self, p: float, t: float) -> None:
        if t <= 0.0:
            raise PhaseGap(
                self.name, p,
                "암모니아는 등온 경로로 풀 수 없다. 표가 (ρ, T) 격자라 온도가 인자다. "
                "포텐셜 온도를 선언하면 이 층이 풀린다.")
        if t < ammonia_table.T_MIN_K or t > ammonia_table.T_MAX_K:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 {ammonia_table.SOURCE} 의 등온선 범위"
                f"({ammonia_table.T_MIN_K:.0f}–{ammonia_table.T_MAX_K:.0f} K) 밖이다. "
                "표 밖은 외삽하지 않는다.", t, too_cold=t < ammonia_table.T_MIN_K)

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        self.check_temperature(p, t)
        try:
            return ammonia_table.density(p, t)
        except ValueError as e:
            # 표의 들쭉날쭉한 가장자리. 500 K 는 1.5 g/cm³, 700 K 는 2.0 까지만 있고, 압력 천장은
            # 등온선마다 다르다(1000 K 237 GPa … 10 000 K 333.2 GPa). 여섯 칸은 계산되지 않은 것이지
            # 떨어진 것이 아니라, 그 사이를 채우지 않고 표 이름을 대며 거절한다.
            raise PhaseGap(self.name, p, f"{e} — 표 밖은 외삽하지 않는다.", t) from None

    def uncertainty(self, p: float, t: float) -> float:
        """논문이 적은 압력 불확도: 보간이 밟는 격자점에 별표가 있으면 5 %, 아니면 2 %."""
        return ammonia_table.uncertainty(self.density(p, t), t)

    def gruneisen(self, p: float, rho: float, t: float, t_pot: float = 0.0) -> float:
        if t <= 0.0:
            return 0.0
        c_v, dpdt, _k_t = self._thermal(p, t)
        return 0.0 if c_v <= 0.0 else dpdt / (rho * c_v)

    def c_p(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """c_P = c_V (1 + αγT). HotWater 와 같은 항등식, 표의 p·u 유한차분에서."""
        c_v, dpdt, k_t = self._thermal(p, t)
        if c_v <= 0.0:
            return 0.0
        if k_t <= 0.0:
            return c_v
        rho = ammonia_table.density(p, t)
        gamma = dpdt / (rho * c_v)
        alpha = dpdt / k_t
        return c_v * (1.0 + alpha * gamma * t)

    def grad_ad(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """(∂lnT/∂lnP)_S = γ P / K_S, K_S = K_T (1 + αγT)."""
        if t <= 0.0 or p <= 0.0:
            return 0.0
        c_v, dpdt, k_t = self._thermal(p, t)
        if c_v <= 0.0 or k_t <= 0.0:
            return 0.0
        rho = ammonia_table.density(p, t)
        gamma = dpdt / (rho * c_v)
        k_s = k_t + dpdt * gamma * t
        return 0.0 if k_s <= 0.0 else gamma * p / k_s

    def _thermal(self, p: float, t: float) -> tuple[float, float, float]:
        """(c_V, (∂P/∂T)_ρ, K_T) 를 표의 p·u 중앙차분으로. h = 1 % (HotWater 와 같은 걸음).
        온도 걸음이 표의 끝을 넘으면 안쪽으로 한쪽 차분을 쓴다."""
        if t <= 0.0:
            return 0.0, 0.0, 0.0
        rho = ammonia_table.density(p, t)
        h = 0.01 * t
        t_lo = max(t - h, ammonia_table.T_MIN_K)
        t_hi = min(t + h, ammonia_table.T_MAX_K)
        dpdt = (ammonia_table.pressure(rho, t_hi) - ammonia_table.pressure(rho, t_lo)) / (t_hi - t_lo)
        c_v = (ammonia_table.internal_energy(rho, t_hi)
               - ammonia_table.internal_energy(rho, t_lo)) / (t_hi - t_lo)
        dr = 0.01 * rho
        lo, hi = ammonia_table.rho_bounds(t)
        r_lo, r_hi = max(rho - dr, lo), min(rho + dr, hi)
        k_t = rho * (ammonia_table.pressure(r_hi, t) - ammonia_table.pressure(r_lo, t)) / (r_hi - r_lo)
        return c_v, dpdt, k_t

    def phase_at(self, p: float):
        return _AmmoniaSlope(p)


@dataclass(frozen=True)
class _AmmoniaSlope:
    """`_adiabatic_dtdp` 가 K_S 를 만들 때 쓰는 (∂P/∂T)_V. 표의 유한차분이다."""
    p: float

    def dpdt_v(self, t: float, t_pot: float = 0.0) -> float:
        if t <= 0.0:
            return 0.0
        return NH3._thermal(self.p, t)[1]


NH3 = Ammonia()


# ── 액체 물 ─────────────────────────────────────────────────────────────
#
# 2026-08-27 의 녹는곡선은 얼음 기둥의 어느 자리가 녹았는지를 **판정** 만 했고, 밀도는 고체상의
# 것이었다. 그때 "액체 상태방정식이 하나 더 있어야 한다" 고 적었는데, 그 상태방정식은 이 파일이
# 얼음 III·V·VI 을 읽어 온 같은 라이브러리 안에 이미 있었다 — SeaFreeze v1.1.0 의 `water1`,
# Bollengier, Brown & Shaw 2019 (2019JChPh.151e4501B). 700 MPa 까지 어는점까지 잰 음속에
# 앵커한 Gibbs 표현이고, 2300 MPa · 240–500 K 까지 적합했다. 그 창이 얼음 껍질 아래의 바다다:
# 위쪽 끝 2.3 GPa 는 얼음 VI→VII 전이(2.216 GPa) 바로 위이고, IAPWS 녹는곡선의 저압 갈래
# 넷(식 1–4)이 끝나는 자리다.
#
# **세 상수로는 안 된다. 재봤다.** 얼음 III·V·VI 처럼 기준 상태의 (ρ₀, K₀, K₀′, αK_T, c_V) 를
# 읽어 BME3 + Anderson–Goto 로 두면 273 K 등온선의 2.2 GPa 에서 5.3 %, 400 K 에서 10.6 % 어긋난다.
# 액체 물의 αK_T 가 밀도 최대(277 K)에서 부호를 바꾸고 창 안에서 40 배 커지기 때문이고, 이 파일의
# 열 항 전체가 기대는 "αK_T 는 부피에 무관" 이 액체에서는 성립하지 않는다. 그래서 수소-헬륨
# 외피와 같은 길을 간다 — 표를 굳혀 온다 (water_table.py, tools/make_water_table.py). 격자 사이
# 보간 오차는 생성기가 재서 적는다: 얼음 껍질 아래 바다가 놓이는 252–360 K 에서 밀도 2e-4 안.
#
# **어디서 액체가 되는가는 이 재료가 정하지 않는다.** 얼음 사다리(H2O)의 녹는곡선이 정하고,
# 적분기가 걸음마다 그 판정으로 사다리와 이 재료 사이를 갈아 끼운다 — interior.py 를 보라.
# 이 재료는 액체라고 결정된 자리의 밀도와 단열 기울기만 낸다. 2.3 GPa 위(또는 500 K 위)의 액체는
# 같은 라이브러리의 `water2` (Brown 2018, 2018FlPEq.463...18B) 를 굳힌 h2o_liquid_dense 가 받는다 —
# 2026-08-30 까지 "굳히지 않았다" 로 선반에만 있었고, 그 사이 500–1000 K 의 조밀한 액체가 거절돼
# 온도 괄호가 중심 온도를 밀어 올렸다 (F2 의 칼리스토·타이탄 f = 0.75, 70 CPU-분). 아래 클래스.
LIQUID_WATER_REF = ("SeaFreeze v1.1.0 water1 / Bollengier, Brown & Shaw 2019 "
                    "(2019JChPh.151e4501B) — 액체 물 Gibbs 표현, 0–2300 MPa · 240–500 K")
LIQUID_WATER_DENSE_REF = (
    "SeaFreeze v1.1.0 water2 / Brown 2018 (2018FlPEq.463...18B) — 조밀한 액체·초임계 물의 Gibbs "
    "표현. AQUA(Haldemann+ 2020) §2.3.5 가 '1–100 GPa, 10⁴ K 까지' 로 적는 그 표현이고, 굳힌 창은 "
    "스플라인이 실제로 유효한 부분 — 0.1 GPa 부터 등온선별 천장(360 K 2.3 GPa · 600 K 10 GPa · "
    "1000 K 30 GPa)까지, 360–1100 K")


class LiquidWater:
    """액체 물. `Material` 과 같은 자리에 꽂히지만 상의 열이 아니라 표 하나다.

    HotWater · HydrogenHelium 과 같은 모양이다. 응축상 사다리처럼 P = 0 인 표면이 있으므로
    `p_floor` 는 없다 — 바다가 표면까지 올라오면 적분은 P = 0 에서 멈춘다."""
    name: str = "h2o_liquid"
    label_ko: str = "액체 물 (바다)"

    @property
    def rho0(self) -> float:
        """영압 밀도. 어는점의 물이다. 괄호잡기와 표면 바깥 반 걸음에만 쓰인다."""
        return water_table.density(0.0, 273.15)

    @property
    def p_max(self) -> float:
        return water_table.P_MAX_PA

    def rho_seed(self, mass_kg: float) -> float:
        return self.rho0

    @property
    def has_thermal(self) -> bool:
        return True

    def cold_phases(self) -> tuple[str, ...]:
        return ()

    def melt_free_phases(self) -> tuple[str, ...]:
        """녹는곡선이 없다 — 이 재료는 이미 액체다. 어디서 어는지는 얼음 사다리가 말한다."""
        return (self.name,)

    def t_melt(self, p: float) -> float | None:
        return None

    def in_domain(self, p: float, t: float) -> bool:
        return water_table.in_domain(p, t)

    def check_temperature(self, p: float, t: float) -> None:
        """이 표가 유효한 (P, T) 밖인가. 세 방향을 각각 이름 대며 거절한다."""
        if t <= 0.0:
            raise PhaseGap(
                self.name, p,
                "액체 물은 등온 경로로 풀 수 없다. 이 표는 (P, T) 의 함수이고, 애초에 온도가 "
                "선언되지 않으면 녹는곡선이 어느 자리를 액체라고 말할 일도 없다.")
        if p > water_table.P_MAX_PA:
            # **온도가 막은 것으로 던진다.** 여기 오는 것은 압력이 아니라 그 압력에서 얼음 VII 을
            # 녹일 만큼 뜨거운 온도이고, 사격의 온도 괄호가 중심 온도를 내리면 풀린다 — 첫 시험
            # 온도(포텐셜 온도의 두 배)가 실제로 여기 걸린다. 수렴점에서도 걸리는 천체(따뜻한
            # 물 세계)는 온도 고리가 표면 온도를 못 맞춰 converged=False 로 나간다.
            raise PhaseGap(
                self.name, p,
                f"{p / 1e9:.3f} GPa 의 액체 물은 바다 표의 상한({water_table.P_MAX_PA / 1e9:.1f} "
                "GPa) 위다. 얼음 VII 이 녹을 만큼 따뜻한 기둥인데, 그 압력의 액체는 "
                f"{LIQUID_WATER_REF} 의 창 밖이다 — 적분기는 그 자리를 h2o_liquid_dense (water2) 로 "
                "보내므로 여기 온 것은 편집 오류다.",
                t)
        if t > water_table.T_MAX_K:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 액체 물 표의 상한({water_table.T_MAX_K:.0f} K) 위다. "
                f"{LIQUID_WATER_REF}. 그 위는 뜨거운 물(h2o_hot)의 영역이고 별건이다.", t)
        if t < water_table.T_LO_K:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 액체 물 표의 하한({water_table.T_LO_K:.0f} K) 아래다 — 녹는곡선의 "
                "최저점(251 K)보다 낮으므로 여기 오는 것은 판정이 아니라 편집 오류다.",
                t, too_cold=True)

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        self.check_temperature(p, t)
        return water_table.density(max(p, 0.0), t)

    def c_p(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """c_P [J/kg/K] — 원본(Bollengier+ 2019 깁스 표현)이 처음부터 싣던 양을 2026-08-31
        (얼음 축, 브리프 23) 에 표로 구웠다. 혼합(Mixture)의 ∇_ad 가중이 소비처다 — 그 전까지
        이 표는 dT/dP|_S 만 실어서 물 섞인 혼합이 바다 창에서 c_P 없음으로 거절됐다."""
        self.check_temperature(p, t)
        return water_table.c_p(max(p, 0.0), t)

    def grad_ad(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """(∂lnT/∂lnP)_S = (dT/dP|_S)·P/T — 표의 기울기에서 그대로."""
        self.check_temperature(p, t)
        if t <= 0.0:
            return 0.0
        return water_table.dtdp_adiabat(max(p, 0.0), t) * max(p, 0.0) / t

    def gruneisen(self, p: float, rho: float, t: float, t_pot: float = 0.0) -> float:
        """쓰이지 않는다 — 단열 기울기는 표가 직접 든다 (dtdp_adiabat). 0 은 '없다' 가 아니라
        이 길이 아니라는 뜻이다."""
        return 0.0

    def dtdp_adiabat(self, p: float, t: float, t_pot: float = 0.0) -> float:
        """단열 기울기 dT/dP|_S = α T / (ρ c_P) [K/Pa]. 표에서 읽는다, 조립하지 않는다."""
        if t <= 0.0:
            return 0.0
        return water_table.dtdp_adiabat(max(p, 0.0), t)

    def phase_at(self, p: float, t: float = 0.0):
        return _LiquidWaterSlope(p)


@dataclass(frozen=True)
class _LiquidWaterSlope:
    """`_adiabatic_dtdp` 가 own 기울기를 쓰므로 여기까지 오지 않지만, 상 자리를 묻는 호출자에게
    이름을 돌려준다."""
    p: float
    name: str = "h2o_liquid"
    t_max: float = 0.0

    def dpdt_v(self, t: float, t_pot: float = 0.0) -> float:
        return 0.0


H2O_LIQUID = LiquidWater()


# ── 조밀한 액체 물 — 바다 표 위, 뜨거운 물 아래 ────────────────────────────
#
# 2026-08-30 까지 이 자리는 빈 띠였다: 2.3 GPa 위(또는 500 K 위)의 액체를 녹는곡선이 인정해도 이
# 저장소에 그 상태방정식이 없어 too_cold 로 던졌고, 온도 괄호가 중심 온도를 1000 K 위로 밀어
# Mazevet 의 적합으로 넘겼다. C3 가 그 띠를 "열린 결함" 으로 적었고 F2 가 값을 치렀다.
# 표는 water_table.py 와 같은 길로 굳혔다 (water2_table.py, tools/make_water2_table.py).
#
# **천장은 매듭이 아니라 스플라인의 것이다.** SeaFreeze 의 water2 는 매듭 상자가 0–100 GPa 인데
# 그 안쪽에서 밀도가 음수로 가고 c_P 가 10⁶ 이 된다 — 700 K 에서 ~13 GPa 위, 1000 K 에서
# ~30 GPa 위 (2026-08-30 측정, water2-context-notes.md). 유효 천장은 녹는곡선을 바짝 따라간다:
# 10 GPa 까지는 녹는점 바로 위부터 유효하고, 12–20.6 GPa 에서는 녹는점(663–705 K)과 천장이 서는
# 온도(~780–870 K) 사이에 좁은 띠가 남는다. 그 띠는 이름 대며 거절한다 — 더 뜨거우면 이 표나
# Mazevet 이 받으므로 too_cold 다. 1000 K 위는 예전 그대로 Mazevet 이 받는다 (h2o_hot 경로는
# 한 줄도 안 바뀌었다 — 얼음거대행성 앵커가 그 위에 서 있다).
class DenseLiquidWater:
    """조밀한 액체·초임계 물, SeaFreeze water2 (Brown 2018) 의 굳힌 표. LiquidWater 와 같은 모양에
    c_P 를 더 들고 있어 암석 혼합(Mixture.grad_ad 의 c_P 가중)이 이 띠에서도 닫힌다."""
    name: str = "h2o_liquid_dense"
    label_ko: str = "조밀한 액체 물 (water2)"

    @property
    def rho0(self) -> float:
        return water2_table.density(water2_table.P_MIN_PA, water2_table.T_LO_K)

    @property
    def p_max(self) -> float:
        """가장 뜨거운 등온선의 천장. 온도마다의 실제 천장은 density 가 이름 대며 거절한다."""
        return water2_table.P_MAX_PA

    def rho_seed(self, mass_kg: float) -> float:
        return self.rho0

    @property
    def has_thermal(self) -> bool:
        return True

    def cold_phases(self) -> tuple[str, ...]:
        return ()

    def melt_free_phases(self) -> tuple[str, ...]:
        return (self.name,)

    def t_melt(self, p: float) -> float | None:
        return None

    def in_domain(self, p: float, t: float) -> bool:
        return water2_table.in_domain(p, t)

    def check_temperature(self, p: float, t: float) -> None:
        if t <= 0.0:
            raise PhaseGap(self.name, p,
                           "조밀한 액체 물은 등온 경로로 풀 수 없다. 이 표는 (P, T) 의 함수다.")
        if t < water2_table.T_LO_K:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 조밀한 액체 물 표의 하한({water2_table.T_LO_K:.0f} K) 아래다 — 2.3 GPa 의 "
                "녹는점(362 K)보다 낮으므로 여기 오는 것은 판정이 아니라 편집 오류다.", t, too_cold=True)
        if t > water2_table.T_MAX_K:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 조밀한 액체 물 표의 상한({water2_table.T_MAX_K:.0f} K) 위다 — 1000 K 위는 "
                "뜨거운 물(Mazevet+ 2019)의 자리라 적분기가 여기로 보내지 않는다.", t)
        if p < water2_table.P_MIN_PA:
            # **온도가 막은 것으로 던진다** — 2026-08-30 전에 이 자리(500–1000 K 의 저압 액체)가 던지던 방향
            # 그대로. 더 뜨거우면 1000 K 부터 Mazevet 이 받고, 시험 경로가 실제로 여기를 지난다(해왕성의
            # 온도 괄호가 0.098 GPa · 817 K 를 밟았다). 압력 벽으로 던지면 괄호가 이것을 진짜 거절로 읽는다.
            raise PhaseGap(
                self.name, p,
                f"{p / 1e9:.3f} GPa · {t:.0f} K 의 물은 조밀한 액체 물 표(SeaFreeze water2 / Brown 2018)의 굳힌 "
                f"창의 압력 바닥({water2_table.P_MIN_PA / 1e9:.1f} GPa) 아래다 — 500 K 위의 저압 물은 증기에 가깝고 "
                f"쌍선형 격자가 정직하지 않아 굳히지 않았다. 더 뜨거우면 {water_hot.T_MIN:.0f} K 부터 Mazevet+ 2019 가 받는다.",
                t, too_cold=True)
        ceiling = water2_table.p_ceiling(t)
        if p > ceiling * (1.0 + 1e-12):
            raise PhaseGap(
                self.name, p,
                f"{p / 1e9:.2f} GPa · {t:.0f} K 의 액체 물은 {LIQUID_WATER_DENSE_REF} 의 이 온도 천장"
                f"({ceiling / 1e9:.1f} GPa) 위다 — 스플라인이 그 위에서 비물리적이라 굳히지 않았다. "
                f"더 뜨거우면 천장이 오르고 {water_hot.T_MIN:.0f} K 부터는 Mazevet+ 2019 가 받는다.",
                t, too_cold=True)

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        self.check_temperature(p, t)
        return water2_table.density(p, t)

    def gruneisen(self, p: float, rho: float, t: float, t_pot: float = 0.0) -> float:
        return 0.0

    def dtdp_adiabat(self, p: float, t: float, t_pot: float = 0.0) -> float:
        if t <= 0.0:
            return 0.0
        return water2_table.dtdp_adiabat(p, t)

    def c_p(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        return water2_table.c_p(p, t)

    def grad_ad(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        if t <= 0.0 or p <= 0.0:
            return 0.0
        return water2_table.dtdp_adiabat(p, t) * p / t

    def phase_at(self, p: float, t: float = 0.0):
        return _LiquidWaterSlope(p, name=self.name)


H2O_LIQUID_DENSE = DenseLiquidWater()


def mix(name: str, label_ko: str, *parts: tuple[Material, float]) -> Material | Mixture:
    """혼합을 만든다. 성분이 실질적으로 하나면 그 재료를 그대로 돌려준다.

    분율 0 인 성분을 남겨두면 `p_max` 가 쓰지도 않는 재료의 상한에 묶인다."""
    live = [(m, w) for m, w in parts if w > 0.0]
    if len(live) == 1:
        return live[0][0]
    return Mixture(name, label_ko, tuple(live))


GPA = 1e9
MPA = 1e6

# ── 열 항 ───────────────────────────────────────────────────────────────
#
# 여기까지의 상태방정식은 전부 **등온** 이다. 온도를 넣는 표준 처리는 냉각 곡선에
# 열압력을 더하는 것이고, 형태는 Seager+ 2007 §IV.2.2 (arXiv:0707.2895) 가 쓰는
# Anderson & Goto 1989 근사 그대로다.
#
#     P(ρ, T) = P_cold(ρ) + P_th(T),      P_th = αK_T · ΔT
#
# **왜 선형인가.** Debye 온도 위에서 αK_T 가 부피에 거의 무관하다는 것이 Anderson &
# Goto 1989 의 결과이고, Seager 가 그것을 근거로 이 형태를 쓴다. θ_D 는 규산염과
# 철 함유 광물에서 ~700 K, 물얼음에서 ~300 K, 탄소에서 ~2000 K 라고 같은 절이 적는다.
# 금속은 전자 여기 때문에 2차 항이 하나 더 붙는다 (Isaak & Anderson 2003).
#
#     P_th(금속) = αK₀ · ΔT + ½ (∂αK₀/∂T)_V · ΔT²
#
# **유효 한계도 같은 절이 준다.** 그 논문이 이 처리로 재보고 적은 밀도 변화폭이다.
#   * MgSiO₃ — 10 GPa 위에서 300 K ~ 6000 K 구간에 걸쳐 4 % 미만
#   * Fe — 100 GPa 위에서 4 % 미만
#   * H₂O 얼음 VII — Frank+ 2004 의 자료가 있는 50 GPa · 800 K 까지 "a few percent"
#
# **기준이 재료마다 다르다. 이게 이 절에서 제일 조심할 자리다.**
#
# `fe_prem` 과 `mgsio3_prem` 은 PREM 적합이고 PREM 은 **뜨거운 실제 지구를 관측한
# 결과** 다. 지구의 지오섬이 그 유효 ρ₀ 안에 이미 들어 있다. 거기에 300 K 기준의
# 열팽창을 얹으면 지구를 두 번 데운다 — 직전 세션이 목성에 중원소를 두 번 넣어
# 반지름을 +0.6 % 에서 −9.8 % 로 만든 것과 똑같은 함정이다.
#
# 그래서 암석-금속 기둥의 기준은 **등온이 아니라 지구의 단열선** 이다. 앵커는
# Unterborn+ 2019 §2 (arXiv:1905.06530) 의 지구형 맨틀 포텐셜 온도 1600 K 이고,
# 그 논문이 T(R) = T_Pot 을 경계조건으로 쓰면서 같은 값을 기준으로 삼는다.
# 포텐셜 온도를 1600 K 로 선언하면 ΔT 가 **정확히 0** 이라 지구가 비트까지 그대로다.
# 허용오차가 아니라 항등식이고, 그 사정은 Phase.delta_t 주석에 있다.
#
# 얼음은 다르다. 상마다 기준이 실제 등온이고 그 온도가 이미 이 파일에 있다.
#
# **규산염 세 상이 전부 같은 기준을 쓴다.** mgsio3_en 은 실험실 상온 적합이고 mgsio3_pv 는
# 3.5 TPa 위라 지구가 닿지도 않는데, 셋 다 지구 단열선을 기준으로 둔다. 이유는 이 스택에서
# 그 셋이 하나의 암석 기둥이고, 지구를 0.3 % 로 재현한 것이 그 기둥 전체이기 때문이다 —
# 상마다 기준을 갈라 두면 그 0.3 % 안에 이미 흡수돼 있는 몫을 다시 꺼내게 되고, 이음매마다
# 열압력이 튄다. 대가는 차가운 천체의 규산염이 지구 맨틀 기준으로 계산된다는 것이고,
# 그 방향은 맞다 (차가우면 밀하다). 균일한 규칙 하나를 쓰고 그렇다고 적는다.
SILICATE_ALPHA_K = 0.00692 * GPA     # Pa/K. Anderson & Masuda 1994, Seager+ 2007 §IV.2.2
IRON_ALPHA_K = 0.00121 * GPA         # Pa/K. Isaak & Anderson 2003, 같은 절
IRON_ALPHA_K_DT = 7.8e-7 * GPA       # Pa/K². 전자 여기 항, 같은 절
EARTH_POTENTIAL_T = 1600.0           # K. Unterborn+ 2019 §2 의 지구형 맨틀 포텐셜 온도
LAB_ISOTHERM_T = 300.0               # K. 실험실 압축 자료의 관례적 기준 온도

# 정적비열. **두 가지 다른 출처에서 왔고 섞으면 안 된다.**
#
# 규산염과 철은 Debye 온도(~700 K) 위에서 쓰이므로 **Dulong-Petit 극한** 3R/M_atom
# 이다. 적합한 상수가 아니라 교과서 결과이고, M_atom 은 조성에서 나오는 몰질량이다.
#   MgSiO₃ : M = 100.3875 g/mol, 원자 5개 → M_atom = 20.0775 g/mol
#   Fe     : M = 55.845 g/mol,  원자 1개 → M_atom = 55.845 g/mol
#
# **얼음에는 그 극한을 쓰면 안 된다.** θ_D 가 ~300 K 인데 얼음이 존재하는 온도가
# 그 아래라, Dulong-Petit 이 c_V 를 두 배 넘게 과대평가한다 (물 3원자 기준 4154
# 대 실제 ~1700~2050). 그래서 얼음의 c_V 는 ρ₀·K₀·K₀′ 와 **같은 자리에서 같은
# 방식으로** 읽었다 — SeaFreeze v1.1.0 을 각 상의 기준 상태에서 평가한 값이다.
def dulong_petit(m_atom_kg_per_mol: float) -> float:
    """3R/M_atom. Debye 온도 위의 격자 비열 극한 [J kg⁻¹ K⁻¹]."""
    return 3.0 * R_GAS / m_atom_kg_per_mol


CV_SILICATE = dulong_petit(0.0200775)   # 1242.4 J/kg/K
CV_IRON = dulong_petit(0.0558450)       # 446.6 J/kg/K

# ── 녹는곡선 ─────────────────────────────────────────────────────────────
#
# 여기까지가 "이 압력에서 이 상이 유효한가" 였다. 녹는곡선은 그 **옆에 서는 같은 종류**
# 다 — 압력의 함수인 온도 문턱이고, 적분이 지나가는 자리마다 물으면 "지금 여기가 고체인가
# 액체인가" 가 답해진다. 상태방정식의 새 층이 아니라 이웃이다.
#
# 상마다 `melt` 이름이 붙는다. 빈 문자열은 **이 상에는 발표된 녹는곡선이 없다** 는 뜻이고,
# `alpha_k = 0` 이 열 상수가 없다는 뜻인 것과 같은 규율이다. 없는 척하지 않는다.
#
# ── 물 ──
#
# IAPWS R14-08(2011), *Revised Release on the Pressure along the Melting and Sublimation
# Curves of Ordinary Water Substance* 가 얼음 Ih·III·V·VI·VII 의 p_melt(T) 를 닫힌 형태로
# 준다. 이 파일이 얼음 Ih 의 ρ₀·K_T 를 읽어온 IAPWS-06 과 같은 기관의 같은 종류의 문서이고,
# 릴리스 번호로 핀한다 (ADS 밖의 표준 문서라 그렇게 인용한다).
#
#   Ih   π = 1 + Σ aᵢ(1 − θ^bᵢ)              T* = 273.16 K,   p* = 611.657 Pa,  273.16→251.165 K
#   III  π = 1 − 0.299948(1 − θ⁶⁰)           T* = 251.165 K,  p* = 208.566 MPa, 251.165→256.164 K
#   V    π = 1 − 1.18721(1 − θ⁸)             T* = 256.164 K,  p* = 350.1 MPa,   256.164→273.31 K
#   VI   π = 1 − 1.07476(1 − θ⁴·⁶)           T* = 273.31 K,   p* = 632.4 MPa,   273.31→355 K
#   VII  ln π = 1.73683(1 − θ⁻¹) − 0.0544606(1 − θ⁵) + 8.06106e−8(1 − θ²²)
#                                             T* = 355 K,      p* = 2216 MPa,   355→715 K
#
# **불확도도 그 문서가 준다** — 2 % (Ih) · 3 % (III·V·VI) · 7 % (VII). 그리고 §7 이
# 프로그램 검증용 계산값을 하나씩 싣는다. test_interior.py 가 그 다섯 점을 다시 낸다.
#
# **삼중점이 이 파일의 전이압과 비트까지 같지 않다. 그 사실이 내용이다.** 상 사다리의
# 전이압은 Choukroun & Grasset 2007 (Zeng & Sasselov 2013 경유) 에서 왔고, IAPWS 는 자기
# 녹는곡선을 자기 삼중점 표에 맞춰 구속했다. 압력으로 0.45 % (Ih–III) · 1.4 % (III–V) ·
# 2.3 % (V–VI) 차이다. 어느 쪽도 상대에 맞춰 옮기지 않는다 — 옮기면 그 값이 속한 적합이
# 깨진다. 대신 **녹는곡선은 자기 분기점을 들고 다닌다** (아래 WATER_MELT_BREAKS). 그래서
# 삼중점 근처 2 % 폭에서 두 표가 "어느 상이 녹는가" 를 다르게 말할 수 있고, 그 폭은 IAPWS
# 자신의 3 % 불확도보다 좁다.
#
# ── 철 ──
#
# 두 조각이 이 엔진이 닿는 압력대를 덮는다. 둘 다 논문이 초록에 적합식을 그대로 실었다.
#
#   Zhang+ 2015 (2015PEPI..244...69Z) — 2상 분자동역학 자료에 Simon 식을 적합.
#       T_m = 1825 K (1 + P/57.723 GPa)^0.654           365 GPa 까지 적합
#     영압에서 1825 K 로 실측 1811 K 와 0.8 % 차이이고, 330 GPa 에서 6345 K 를 준다.
#
#   González-Cataldo & Militzer 2023 (2023PhRvR...5c3194G) — 고체·액체 Gibbs 자유에너지를
#   같게 두어 녹는선을 얻고, 역시 Simon 형태로 적었다.
#       T_m = 6469 K (1 + (P − 300 GPa)/434.82 GPa)^0.54369      300 – 5000 GPa
#     같은 논문이 이 곡선을 Kraus+ 2022 (2022Sci...375..202K) 의 1 TPa 실측과 대조해
#     "in very good agreement" 라고 적는다.
#
# **겹치는 구간에서 둘이 6.8 ~ 7.5 % 어긋난다.** 그 폭은 같은 압력의 두 정적압축 실험이
# 어긋나는 폭보다 좁다 — Anzellini+ 2013 이 내핵 경계에서 6230 ± 500 K, Sinmyo+ 2019 가
# 5500 ± 220 K 로 13 % 차이다. 그래서 평균내지 않고 Zhang 의 적합 상한(365 GPa)에서
# 갈아탄다. 이음매의 6.8 % 는 지어낸 것이 아니라 **잰** 것이고 test_interior.py 가 다시 잰다.
#
# 5 TPa 위는 두 적합 다 밖이다. IRON_MELT_MAX 가 그 자리를 들고 있고, 그 위를 물으면
# 값이 아니라 None 이 온다.
#
# **가벼운 원소가 섞인 핵은 녹는점이 내려간다.** 그 몫은 재료마다 다르고, 이 파일은 이미
# 그 구분을 들고 있다 — `fe_eps` 는 실험실 순철이고 `fe_prem` 은 PREM 외핵 적합이라
# 가벼운 원소가 유효 ρ₀ 안에 이미 있다. 그래서 녹는곡선도 같은 자리에서 갈린다.
# 내림폭 20 % 는 발표된 열진화 모형들의 관례다 (Stevenson+ 1983 → Tachinami+ 2011,
# Stixrude 2014, Zhang & Rogers 2022 arXiv:2208.06523 이 "the melting temperature of iron
# is reduced by 20 % to account for the influence of light elements in the iron core" 라고
# 적는다). 독립 검산이 같은 자리에 떨어진다 — Sinmyo+ 2019 의 지구 내핵 경계 온도
# 5120 ± 390 K 를 위 순철 곡선의 329 GPa 값 6331 K 에 대면 19.1 % 다. 두 수는 같은 주장이
# 아니라서(Sinmyo 는 자기 5500 K 곡선에 380 K 를 뺀 것이다) 이 일치는 도출이 아니라 검산이고,
# 그렇게 적는다. **이 값은 선언이다** — 이 레시피는 핵의 조성을 도출하지 않는다.

# IAPWS R14-08(2011) §3. (계수, 지수) 와 (T*, p*), 그리고 그 식이 유효한 온도 구간.
IAPWS_IH_A = (0.119539337e7, 0.808183159e5, 0.333826860e4)
IAPWS_IH_B = (3.0, 25.75, 103.75)
IAPWS_MELT: dict[str, tuple[float, float, float, float, float, float]] = {
    # name: (T*, p* [Pa], 계수, 지수, T_lo, T_hi)
    "ice_iii": (251.165, 208.566e6, 0.299948, 60.0, 251.165, 256.164),
    "ice_v":   (256.164, 350.1e6, 1.18721, 8.0, 256.164, 273.31),
    "ice_vi":  (273.31, 632.4e6, 1.07476, 4.6, 273.31, 355.0),
}
IAPWS_IH_RANGE = (251.165, 273.16)     # K. 식 (1) 의 유효 구간
IAPWS_VII_RANGE = (355.0, 715.0)       # K. 식 (5) — 상한은 측정이 끝나는 온도다
IAPWS_VII_TP = (355.0, 2216.0e6)       # T*, p*
IAPWS_VII_C = (1.73683, -0.0544606, 8.06106e-8)
IAPWS_VII_E = (-1.0, 5.0, 22.0)
# 녹는곡선 자신의 분기점 [Pa]. 위 삼중점 표에서 오고, 상 사다리의 전이압과 다르다.
WATER_MELT_BREAKS = (208.566e6, 350.1e6, 632.4e6, 2216.0e6)
IAPWS_MELT_UNCERTAINTY = {"ice_ih": 0.02, "ice_iii": 0.03, "ice_v": 0.03,
                          "ice_vi": 0.03, "ice_vii": 0.07}
IAPWS_MELT_REF = ("IAPWS R14-08(2011) §3 — Revised Release on the Pressure along the "
                  "Melting and Sublimation Curves of Ordinary Water Substance")

# **20.6 GPa 위의 녹는곡선.** IAPWS 식 (5) 가 715 K 에서 끝나는 자리부터 Reinhardt+ 2022
# (2022NatCo..13.4707R) 의 액체–고체 공존선을 쓴다 — 열역학 적분으로 계산한 11 점, 10–52.4 GPa,
# 공개 데이터에서 생성한 표(ice_melt_table.py)를 점 사이 선형 보간한다. **실험이 아니라
# 기계학습 퍼텐셜(PBE) 시뮬레이션** 이라 이 곡선으로 낸 판정은 analog 다. 같은 논문의
# 얼음 VII′–VII″ 공존선(20–70 GPa, 1차 전이)도 같이 든다 — 밀도에는 안 쓰고 상의 이름에만 쓴다.
#
# **이음매는 20.6 GPa 이고 그 폭은 잰 것이다.** IAPWS 가 거기서 715 K, Reinhardt 보간이 902 K —
# 녹는점으로 +26 % 다. 두 곡선이 15–16 GPa 에서 교차하므로 교차점에서 갈아탈 수도 있었지만,
# 그러면 측정 곡선의 마지막 5 GPa 를 시뮬레이션으로 바꾸고 이음매 압력이 우리 것이 된다.
# 규산염 이음매(3.5 TPa, 0.21 %)와 같은 규칙 — 출처가 끝나는 자리에서 갈아타고 폭을 적는다.
# test_interior.py 가 이 폭을 다시 잰다. 이 폭 안의 띠(20.6 GPa 근처 715–902 K)에 앉은 자리는
# 판정문이 "두 출처가 다투는 띠" 라고 이름 댄다.
REINHARDT_LIQUID = tuple((p_gpa * GPA, t_k) for p_gpa, t_k, _s in ice_melt_table.LIQUID_LINE)
REINHARDT_VII1_VII2 = tuple((p_gpa * GPA, t_k) for p_gpa, t_k in ice_melt_table.VII1_VII2_LINE)
REINHARDT_P_MAX = REINHARDT_LIQUID[-1][0]        # 52.4 GPa. 이 위의 액체선은 이 레시피에 없다
REINHARDT_VII1_VII2_P_MAX = REINHARDT_VII1_VII2[-1][0]   # 70 GPa. VII′–VII″ 선이 끝나는 자리
REINHARDT_MELT_REF = ("Reinhardt+ 2022 (2022NatCo..13.4707R) Fig. 1a — 열역학 적분 액체–고체 "
                      "공존선 10–52.4 GPa, 공개 데이터(BingqingCheng/highP-ice)에서 생성. "
                      "기계학습 퍼텐셜 시뮬레이션, 등급 analog")
# 52.4 GPa 위에서 이 레시피가 드는 유일한 융해 측정. **점이지 곡선이 아니다** — Millot+ 2018
# (2018NatPh..14..297M) 초록의 "ice melts near 5,000 K at 190 GPa". 판정문이 거리를 재는 데만 쓴다.
MILLOT_2018_MELT = (190.0 * GPA, 5000.0)

# Simon 적합 두 조각. (T₀ [K], P₀ [Pa], a [Pa], c) 로 T = T₀(1 + (P−P₀)/a)^c 다.
IRON_MELT_LOW = (1825.0, 0.0, 57.723 * GPA, 0.654)        # Zhang+ 2015 초록
IRON_MELT_HIGH = (6469.0, 300.0 * GPA, 434.82 * GPA, 0.54369)   # González-Cataldo+ 2023 초록
IRON_MELT_SPLICE = 365.0 * GPA     # Zhang+ 2015 가 자기 적합의 상한으로 적은 압력
IRON_MELT_MAX = 5000.0 * GPA       # González-Cataldo+ 2023 의 계산 상한
# 가벼운 원소의 융해 내림 20 %. **혈통 수리(브리프 38 D) — 값은 안 움직였다**: 기원은
# Stevenson 1981 의 이상혼합 추정이고, Boehler 1996 p. 29 가 그 방법을 "making crude
# assumptions on the entropy of melting and assuming ideal mixing" 이라 적으며, 우리에게는
# Zhang & Rogers 2022 를 거쳐 오는데 그 논문 스스로 "artificial" · "fine tune[d] … to
# match Tachinami et al. (2011)" 이라 부른다. **지금 이 값 밑에 서 있는 것은 그 관례가
# 아니라 독립 검산이다** — Sinmyo+ 2019 의 지구 ICB 5120 ± 390 K 에 순철 곡선 ×0.80 을
# 대면 −0.12 σ (core_state.py 가 계산해서 낸다). 1981 년 추정치에 2019 년 측정이 독립적으로
# 착지한 모양이고, 아래 공정(eutectic) 바운드가 그 반대편 울타리다. Boehler 의 "고압 수렴"
# 기대는 지지되지 않는다(두 번 헤지된 자기 인용 외삽이고, 같은 문단의 Anderson & Ahrens
# 1995 FeS ICB 4310 ± 750 K 가 Mori 공정 3993 K 를 품는다) — 절대 내림은 자라고(1 bar
# 546 K → 254 GPa 1958 K) 분율은 평평하므로, **상수 인자는 형태로서 정당하다**.
IRON_LIGHT_ELEMENT_FACTOR = 0.80
IRON_MELT_REF_LOW = ("Zhang+ 2015 (2015PEPI..244...69Z) — 2상 MD 자료의 Simon 적합, "
                     "365 GPa 까지")
IRON_MELT_REF_HIGH = ("González-Cataldo & Militzer 2023 (2023PhRvR...5c3194G) — ab initio "
                      "Gibbs 자유에너지, 300–5000 GPa, Kraus+ 2022 의 1 TPa 실측과 일치")

# ── Fe–Fe₃S 공정(eutectic) 융해곡선 — **바운드이지 우리 melt 곡선이 아니다** (브리프 38) ──
#
# Mori+ 2017 (2017E&PSL.464..135M) §3.3 식 (1), 캐시 1차에서 전사. 융해면의 **바닥** —
# S-부화 공정 조성에서의 최저 융해온도라, 어떤 철 합금 핵의 선언 융해곡선도 이 아래로
# 내려갈 수 없다. **0.63(공정) < 0.81(우리 0.80 = 지구 실제 조성, Sinmyo 검산 −0.12 σ)
# < 1.0(순철) 은 물리적으로 맞는 순서다** — 이 곡선으로 0.80 을 "정정" 하는 것은 브리프
# 38 §0 이 잡은 짝-오류다(맞는 수, 틀린 짝). 조건 셋, 상수 옆이 제자리다:
#   ① **황이 최대 내림** — Fig. 6 캡션이 순서를 인쇄한다(Fe–Fe₃S 가 Fe·Fe–FeSi·Fe–FeO·
#     Fe–Fe₃C 보다 낮고 FeH 만 비슷). Si/O/C 핵은 0.65 와 1.0 사이다.
#   ② **니켈 미포함** — Mori 조성은 Fe–S 뿐(Table 2).
#   ③ **곡선 전체가 미확보 앵커 한 점에 걸린다** — 기준점 1348 K @ 21 GPa 는 Fei+ 2000
#     이고 우리에게 없다. 네 검산은 적합을 확인하지 앵커를 확인하지 않는다.
# 전사 검산 넷(test_core_state.py 가 게이트에 든다): 60 GPa → 1915.0 (인쇄 1910, run #6) ·
# 254 GPa → 3541.1 (3550, run #11) · 136 GPa → 2681.0 ("~2700 K at the CMB") · ~350 GPa →
# 4102.7 ("~4100 K at the ICB"). ⚠ 넷째는 **라벨 세부이지 결함이 아니다** — 교과서 ICB
# 330 GPa 에서 식 (1)은 3993 K 이고, 논문의 "~4100 ICB" 는 자기 곡선 위 ~350 GPa 에 있다.
# 판정 완료(브리프 35 후속), paper-defects 에 넣지 말 것.
# 범위: 측정 21→254 GPa, 논문 자신의 외삽 사용처가 ~350 GPa. **10–21 GPa 는 Mori 도
# Buono & Walker 2011 도 못 덮는다**(Buono 는 1 bar–10 GPa 를 조성 다항식으로만) — 그
# 구간이 필요하면 값을 맞추지 말고 IRON_FES_GAP_REASON 으로 이름 대고 거절하라. Buono
# 식 (5) 를 쓸 일이 있으면 **+2140.2 로 교정해 읽되 결함 인용 필수** (paper-defects #10).
# 소비처 현황(브리프 38 F, 갈래 ④): 로스터 전원이 0.80 상수라 공정/순철 괄호를 위반할
# 수 있는 천체가 없고(21–350 GPa 최소 여유 +407.5 K @ 48 GPa — test_core_state 가 잰다),
# C5 에 따라 런타임 배선은 짓지 않았다. S-부화 핵을 선언하는 날 이 상수가 기다린다.
MORI_FES_EUTECTIC = (1348.0, 21.0 * GPA, 36.5 * GPA, 1.0 / 2.07)  # (T_ref, P_ref, a, 1/c)
MORI_FES_P_MEASURED_MAX = 254.0 * GPA   # 측정 상한 (run #11)
MORI_FES_P_MAX = 350.0 * GPA            # 논문 자신의 외삽 사용처 ("~4100 at the ICB")
IRON_FES_GAP_REASON = ("10–21 GPa 의 Fe–S 융해는 Mori+ 2017(21 GPa 아래는 기준점 밖)도 "
                       "Buono & Walker 2011(1 bar–10 GPa, 조성 다항식)도 덮지 않는다 — "
                       "이 구간의 공정 온도는 적합이 아니라 부재다.")


def iron_fes_eutectic_t_melt(p: float) -> float | None:
    """Fe–Fe₃S 공정 융해온도 [K] — 융해 바운드(바닥). 21–350 GPa 밖은 None.

    Mori+ 2017 식 (1). 우리 iron_t_melt 와 같은 Simon 형이고 지수가 그들의 1/c 다.
    바운드로만 쓴다 — 위 블록 주석의 조건 셋과 짝-오류 경고를 보라."""
    t_ref, p_ref, a, cinv = MORI_FES_EUTECTIC
    if p < p_ref or p > MORI_FES_P_MAX:
        return None
    return t_ref * ((p - p_ref) / a + 1.0) ** cinv


def iapws_p_melt(name: str, t: float) -> float:
    """IAPWS R14-08(2011) 의 p_melt(T) [Pa]. 상 이름이 어느 식인지를 고른다."""
    if name == "ice_ih":
        th = t / 273.16
        return 611.657 * (1.0 + sum(a * (1.0 - th ** b)
                                    for a, b in zip(IAPWS_IH_A, IAPWS_IH_B)))
    if name == "ice_vii":
        t_star, p_star = IAPWS_VII_TP
        th = t / t_star
        ln_pi = sum(c * (1.0 - th ** e)
                    for c, e in zip(IAPWS_VII_C, IAPWS_VII_E))
        return p_star * math.exp(ln_pi)
    t_star, p_star, c, e, _lo, _hi = IAPWS_MELT[name]
    return p_star * (1.0 - c * (1.0 - (t / t_star) ** e))


IAPWS_VII_END = iapws_p_melt("ice_vii", IAPWS_VII_RANGE[1])   # Pa. 식 (5) 의 옛 끝, 20.6 GPa —
# 이제 분쟁 대역의 위 모서리이자 Reinhardt 이음매의 자리로 남는다 (브리프 33).

# ── 얼음 VII 녹는곡선, 킨크 아래 (브리프 33 해결) ──────────────────────────────
# **킨크(14.6 GPa) 아래는 2020 년 이후 두 측정의 비가중 평균이다** — Queyroux+ 2020 (PRL 125,
# 195501; 2020PhRvL.125s5501Q, Table I 하부) 와 Prakapenka+ 2021 (Nat. Phys. 17, 1233;
# 2021NatPh..17.1233P, Supp. Table 3 "Ice VII melt"). 연속-대-불연속 계보 논쟁(Rescigno+ 2025,
# Nature 640, 662 가 연속 쪽을 옹호)은 킨크와 그 위의 일이고, 킨크 아래는 두 계보가 일치한다 —
# 논쟁이 없는 구간의 채택이다. 우리 곡선(IAPWS 식 (5))은 평균에서 제외한다: 자기 시험에 자기가
# 투표하는 3자 평균은 실측 둘보다 111–120 K 아래로 끌려갔다.
# **라벨 조건 셋 (전부 의무)**: ① 두 논문은 앵커를 공유한다 (둘 다 Datchi 의 VI–VII–유체 삼중점
# 2.17 GPa · 354.8 K 를 인쇄) — 8.2 GPa 의 1.0 K 일치는 같은 못에 가까운 두 선이지 독립 확인이
# 아니며, 독립 일치는 앵커에서 먼 20.0 GPa 의 8.7 K 다. ② 평균의 불확도는 σ/√2 가 아니라 **두
# 곡선의 간격(채택 구간 2.17–14.6 GPa 에서 최대 16.1 K, 킨크 14.6 GPa 에서)** 을 각자의 σ 와
# 나란히 진다. [정정 2026-09-01: 처음 여기 적힌 "최대 54 K" 는 구간 밖 15.4 GPa 의 서베이 격자
# 값을 지휘석이 잘못 인용한 것 — 발신자(지휘석) 기록. 보수 방향(54 > 16)이라 판정 무관. 아래
# 두 채택식 자체의 15.4 GPa 간격은 18.0 K 이므로 54.1 은 이 식들이 아니라 서베이 격자의 곡선셋
# (분쟁 대역 형태 포함)에서 온 수다 — 이 식들에서 재도출하려 하지 말 것.]
# ③ 8.4 GPa 아래는 측정 지지가 아니라
# 앵커드 보간이다 (두 논문의 측정 최저점이 8.2–8.4 GPa).
QUEYROUX_LOWER = (1.555, 2.557, 2.17e9, 354.8)     # T = T_t·[(P−P_t)/a+1]^(1/b), P ≤ 14.6 GPa
PRAKAPENKA_VII = (1.25, 2.85, 2.17e9, 354.8)       # P = P₀+a[(T/T₀)ⁿ−1] 의 역산, 같은 형
MELT_KINK_PA = 14.6e9                              # Queyroux 삼중점 압력 — 채택 상한
# 분쟁 대역 14.6–20.6 GPa: 두 출처가 수치로는 일치하나 **상 배정이 다르다** (Queyroux 는 14.6 부터
# VII′ 상부 가지, Prakapenka 는 자기 17.5 GPa 분절까지 VII) — 디스패치는 온도만이 아니라 상을
# 소비하므로 평균하지 않고 이름을 대고 거절한다. 로스터 천체는 이 대역에 닿지 않는다 (실측:
# 두 얼음거대행성 기둥 꼭대기 34.5/39.2 GPa, 위성 전 호출 8.4 GPa 아래). 대역의 위·아래 봉투
# 밖은 후보 전원이 일치하므로 판정한다. 금지 수 유지: 782/2188 K 는 Queyroux 불확도가 아니다.


def _melt_sg(p: float, coef) -> float:
    a, b, p_t, t_t = coef
    return t_t * ((p - p_t) / (a * 1e9) + 1.0) ** (1.0 / b)


def water_vii_melt_mean(p: float) -> float:
    """킨크 아래 채택 곡선: Queyroux+ 2020 하부와 Prakapenka+ 2021 VII 분절의 비가중 평균 [K].
    이름은 "Queyroux 채택" 이 아니라 **킨크 아래 두 post-2020 측정의 평균, 둘 다 Datchi 앵커** 다."""
    return 0.5 * (_melt_sg(p, QUEYROUX_LOWER) + _melt_sg(p, PRAKAPENKA_VII))


def _vii_disputed_bounds(p: float) -> tuple[float, float]:
    """분쟁 대역의 온도 봉투: 아래 = IAPWS 식 (5) (후보 중 최저), 위 = Queyroux 상부 적합 (최고).
    봉투 밖은 후보 전원이 같은 답을 내므로 판정하고, 안은 거절한다."""
    lo_t, hi_t = IAPWS_VII_RANGE
    lo, hi = lo_t, hi_t
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if iapws_p_melt("ice_vii", mid) < p:
            lo = mid
        else:
            hi = mid
    t_lo = 0.5 * (lo + hi)
    t_hi = _melt_sg(p, (3.44, 4.33, 14.6e9, 850.0))   # Queyroux Table I 상부 (채택 아님 — 봉투 전용)
    return t_lo, t_hi


def _water_branch(p: float) -> str | None:
    """이 압력에서 녹는 것이 어느 얼음인가. **녹는곡선 자신의 분기점** 으로 고른다."""
    b3, b5, b6, b7 = WATER_MELT_BREAKS
    if p <= 0.0:
        return None
    if p < b3:
        return "ice_ih"
    if p < b5:
        return "ice_iii"
    if p < b6:
        return "ice_v"
    if p < b7:
        return "ice_vi"
    if p <= MELT_KINK_PA:
        return "ice_vii"
    if p <= IAPWS_VII_END:
        return "ice_vii_disputed"   # 브리프 33: 두 출처의 상 배정이 갈리는 대역 — 곡선이 답을 거절
    if p <= REINHARDT_P_MAX:
        return "ice_vii_reinhardt"
    return None


def _interp_line(line: tuple[tuple[float, float], ...], p: float) -> float | None:
    """(P, T) 점 사이를 선형 보간한 T [K]. 표 밖이면 None. 점이 열한 개라 선형 탐색이 싸다."""
    if p < line[0][0] or p > line[-1][0]:
        return None
    for (p0, t0), (p1, t1) in zip(line, line[1:]):
        if p <= p1:
            return t0 + (t1 - t0) * (p - p0) / (p1 - p0)
    return line[-1][1]


def water_vii1_vii2_boundary(p: float) -> float | None:
    """압력 p 에서 얼음 VII′ 이 VII″ 로 넘어가는 온도 [K] (Reinhardt+ 2022). 20–70 GPa 밖은 None."""
    return _interp_line(REINHARDT_VII1_VII2, p)


def water_t_melt(p: float) -> float | None:
    """압력 p 에서 물얼음이 녹는 온도 [K]. 곡선 밖이면 None.

    IAPWS 는 p(T) 를 준다. 각 분기 안에서 단조라 이분법으로 뒤집는다 — 층 경계에서만
    묻는 질문이라 적분 안쪽 고리가 아니고, 그래서 값싼 형태보다 확실한 형태를 쓴다."""
    name = _water_branch(p)
    if name is None:
        return None
    if name == "ice_vii_reinhardt":
        return _interp_line(REINHARDT_LIQUID, p)
    if name == "ice_vii":
        return water_vii_melt_mean(p)   # 브리프 33 — 킨크 아래 두 측정의 평균 (위 라벨 조건 셋)
    if name == "ice_vii_disputed":
        return None                     # 대역의 녹는점은 출처들이 상 배정으로 갈린다 — 지어내지 않는다
    lo, hi = (IAPWS_IH_RANGE if name == "ice_ih" else
              IAPWS_VII_RANGE if name == "ice_vii" else
              IAPWS_MELT[name][4:6])
    # Ih 은 압력이 오르면 녹는점이 **내려간다**. 두 방향을 한 코드로 다루려고 부호를 뽑는다.
    rising = iapws_p_melt(name, hi) > iapws_p_melt(name, lo)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if (iapws_p_melt(name, mid) < p) == rising:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def water_liquid_at(p: float, t: float) -> bool | None:
    """이 (P, T) 의 물이 액체인가. 곡선이 닿지 않는 압력이면 None.

    `water_t_melt` 를 뒤집지 않고 답한다 — 적분기가 **걸음마다** 묻는 질문이라 80 회 이분법이
    한 걸음마다 붙으면 바다 있는 천체의 풀이에서 3 분의 1 이 그 자리에 갔다 (2026-08-29 프로파일).
    분기 안에서 p_melt(T) 가 단조이므로 압력을 곡선의 압력과 대면 같은 답이다: 올라가는
    분기(III·V·VI·VII)는 P < p_melt(T) 면 액체, 거꾸로 가는 얼음 Ih 은 P > p_melt(T) 면 액체.
    분기의 온도 구간 밖은 곡선을 부를 것도 없이 정해진다 — 구간 위면 액체, 아래면 고체."""
    name = _water_branch(p)
    if name is None:
        return None
    if name == "ice_vii_reinhardt":
        t_m = _interp_line(REINHARDT_LIQUID, p)
        return None if t_m is None else t > t_m
    if name == "ice_vii":
        return t > water_vii_melt_mean(p)     # 브리프 33 — 직접 비교라 역산보다 싸다
    if name == "ice_vii_disputed":
        t_lo, t_hi = _vii_disputed_bounds(p)
        if t >= t_hi:
            return True                        # 후보 전원이 액체라는 온도
        if t <= t_lo:
            return False                       # 후보 전원이 고체라는 온도
        raise PhaseGap(
            "h2o", p,
            f"{p / 1e9:.1f} GPa · {t:.0f} K 는 녹는곡선의 분쟁 대역(14.6–20.6 GPa) 안이다 — "
            f"Queyroux+ 2020 과 Prakapenka+ 2021 은 이 대역에서 수치로는 겹치지만 상 배정이 "
            f"다르고(VII′ 대 VII), IAPWS 식 (5) 는 두 측정보다 210–300 K 차다. 후보 봉투 "
            f"{t_lo:.0f}–{t_hi:.0f} K 밖이면 판정하고 안은 고르지 않는다 (브리프 33). 더 "
            "뜨거우면 전원이 액체로 일치한다.",
            t, too_cold=True)
    lo, hi = (IAPWS_IH_RANGE if name == "ice_ih" else
              IAPWS_MELT[name][4:6])
    if t >= hi:
        return True
    if t <= lo:
        return False
    if name == "ice_ih":
        return p > iapws_p_melt(name, t)
    return p < iapws_p_melt(name, t)


WATER_PHASE_LABELS = {"ice_ih": "얼음 Ih", "ice_iii": "얼음 III", "ice_v": "얼음 V",
                      "ice_vi": "얼음 VI", "ice_vii": "얼음 VII"}


def water_phase_name(p: float, t: float) -> tuple[str, str, str]:
    """이 (P, T) 의 물이 어느 상인가 — (판정, 상 이름, 왜) 를 돌려준다.

    판정은 "liquid" · "solid" · "undecided" 셋이다. 밀도에는 안 쓰인다: 적분기는 `water_liquid_at`
    로 재료를 고르고, 이 함수는 그 선택을 **말로 옮기는** 자리다 — 어느 곡선에 댔고 얼마나 떨어져
    있는지를 수로 적어서, 상이 조용히 갈리는 일이 없게 한다. 곡선이 닿지 않는 자리는 이름을
    지어내지 않고 undecided 로 두며 무엇이 닿지 않는지를 적는다."""
    if t <= 0.0:
        return "undecided", "", "온도가 없다"
    name = _water_branch(p)
    t_m = water_t_melt(p)
    if name == "ice_vii_disputed":
        t_lo, t_hi = _vii_disputed_bounds(p)
        if t >= t_hi:
            return "liquid", "액체", f"분쟁 대역(14.6–20.6 GPa)이지만 후보 봉투 위({t_hi:.0f} K)라 전원이 액체"
        if t <= t_lo:
            return "solid", "얼음 VII/VII′ (출처 분쟁)", f"후보 봉투 아래({t_lo:.0f} K)라 전원이 고체 — 상 이름은 출처가 갈린다"
        return "undecided", "", (f"녹는곡선의 분쟁 대역(14.6–20.6 GPa) — Queyroux 와 Prakapenka 가 상 배정으로 "
                                 f"갈리고 봉투({t_lo:.0f}–{t_hi:.0f} K) 안이라 고르지 않는다 (브리프 33)")
    if name is not None and t_m is not None:
        margin = t - t_m
        if name == "ice_vii_reinhardt":
            src = f"Reinhardt+ 2022 의 액체선 (analog), 녹는점 {t_m:.0f} K"
            if margin > 0.0:
                return "liquid", "액체", f"{src} 보다 {margin:+.0f} K 위"
            t_b = water_vii1_vii2_boundary(p)
            if t_b is not None and t > t_b:
                band = (" — IAPWS 식 (5) 의 끝(715 K)은 여기를 액체라 하고 Reinhardt 는 고체라 "
                        "한다, 두 출처가 다투는 띠" if t > IAPWS_VII_RANGE[1] and p < 26.0 * GPA
                        else "")
                return ("solid", "얼음 VII″",
                        f"{src} 보다 {margin:+.0f} K 아래, VII′–VII″ 선({t_b:.0f} K) 위 — "
                        f"초이온 bcc 얼음, VII′ 과 1차 전이로 갈리며 밀도는 초이온을 덮는 Mazevet+ 2019 "
                        f"의 적합이 받는다{band}")
            return ("solid", "얼음 VII′/X",
                    f"{src} 보다 {margin:+.0f} K 아래" + (f", VII′–VII″ 선({t_b:.0f} K) 아래 — "
                    "VII·VII′·X 는 한 열역학 상이다" if t_b is not None else ""))
        if name == "ice_vii":
            src = f"Queyroux+ 2020·Prakapenka+ 2021 평균(킨크 아래, 브리프 33), 녹는점 {t_m:.0f} K"
        else:
            src = f"{IAPWS_MELT_REF.split(' — ')[0]}, 녹는점 {t_m:.0f} K"
        if margin > 0.0:
            return "liquid", "액체", f"{src} 보다 {margin:+.0f} K 위"
        return "solid", WATER_PHASE_LABELS[name], f"{src} 보다 {margin:+.0f} K 아래"
    if p > REINHARDT_P_MAX:
        t_b = water_vii1_vii2_boundary(p)
        if t_b is not None and t < t_b:
            return ("solid", "얼음 VII′/X",
                    f"액체선은 {REINHARDT_P_MAX / GPA:.1f} GPa 에서 끝나지만 VII′–VII″ 선({t_b:.0f} K) "
                    f"아래라 고체다")
        p_m, t_mm = MILLOT_2018_MELT
        return ("undecided", "유체 또는 초이온",
                f"이 레시피의 액체선이 {REINHARDT_P_MAX / GPA:.1f} GPa 에서 끝나 여기({p / GPA:.0f} GPa "
                f"· {t:.0f} K)에는 닿지 않는다. 드는 측정은 Millot+ 2018 의 점 하나 — {p_m / GPA:.0f} GPa "
                f"에서 {t_mm:.0f} K 근처에서 녹는다 — 뿐이라 어느 쪽인지 말하지 않는다")
    return "undecided", "", "녹는곡선이 닿지 않는 압력이다"


def iron_t_melt(p: float) -> float | None:
    """압력 p 에서 **순철** 이 녹는 온도 [K]. 5 TPa 위는 None (두 적합 다 밖이다)."""
    if p < 0.0 or p > IRON_MELT_MAX:
        return None
    t0, p0, a, c = IRON_MELT_LOW if p <= IRON_MELT_SPLICE else IRON_MELT_HIGH
    return t0 * (1.0 + (p - p0) / a) ** c


# ── 철 ──────────────────────────────────────────────────────────────────
#
# 두 갈래가 있고 둘 다 필요하다.
#
# `fe_prem` 은 지구 외핵의 PREM 밀도를 BM2 로 적합한 것이다 (Zeng+ 2016 §II,
# arXiv:1512.08827 — "Outer Core: ρ₀ = 7.05 g/cc, K₀ = 201 GPa, error ~1 % in ρ").
# ρ₀ 가 순철(8300)보다 낮은 것은 **결함이 아니라 내용** 이다 — 지구 핵에는 가벼운
# 원소가 약 10 % 섞여 있고 온도도 높다. 그 둘이 이 유효 ρ₀ 안에 이미 들어 있으므로,
# 이 EOS 로 풀면 지구가 재현된다. 행성 핵을 풀 때 이쪽을 쓴다.
#
# `fe_eps` 는 실험실의 순수한 ε-철이다 (Seager+ 2007 Table 1, Anderson+ 2001 데이터의
# Vinet 적합). 가벼운 원소도 열도 없다. 순철 곡선 — 즉 "이보다 밀할 수 없다" 는
# 한계를 그을 때 쓴다.
FE_PREM = Material(
    "fe_prem", "철 핵 (PREM 외핵 외삽)",
    (Phase("fe_prem", "bm2", 7050.0, 201.0 * GPA, 4.0, 12e3 * GPA,
           "Zeng+ 2016 §II (arXiv:1512.08827) — PREM 외핵 BM2 적합",
           alpha_k=IRON_ALPHA_K, alpha_k_dt=IRON_ALPHA_K_DT, c_v_ref=CV_IRON,
           t_ref=EARTH_POTENTIAL_T, t_ref_kind="adiabat",
           # PREM 외핵 적합이라 가벼운 원소가 이미 들어 있는 재료다. 녹는점도 같은
           # 자리에서 갈린다 — 순철 곡선에 관례적 20 % 내림을 곱한다.
           melt="iron", melt_scale=IRON_LIGHT_ELEMENT_FACTOR,
           melt_ref=IRON_MELT_REF_LOW + " · 합금 내림 "
                    f"{(1 - IRON_LIGHT_ELEMENT_FACTOR) * 100:.0f} % (Stevenson+ 1983 관례)"),),
)
FE_EPS = Material(
    "fe_eps", "순수 ε-철",
    (Phase("fe_eps", "vinet", 8300.0, 156.2 * GPA, 6.08, 2.09e4 * GPA,
           "Seager+ 2007 Table 1 (arXiv:0707.2895) — Fe(ε) Vinet, Anderson+ 2001",
           alpha_k=IRON_ALPHA_K, alpha_k_dt=IRON_ALPHA_K_DT, c_v_ref=CV_IRON,
           t_ref=LAB_ISOTHERM_T,
           # 실험실 순철이므로 내림이 없다. 순철 곡선 그대로다.
           melt="iron", melt_ref=IRON_MELT_REF_LOW),),
)

# ── 규산염 ──────────────────────────────────────────────────────────────
#
# 맨틀은 한 재료가 아니다. 지구에서 상부맨틀→하부맨틀 전이는 23.83 GPa 에서 일어나고
# 밀도가 4.0 → 4.4 g/cc 로 10 % 튄다 (Zeng+ 2016 §II.1). 그 위아래에 각각의 적합이
# 있고, 둘을 이어 붙인 것이 이 재료다.
#
# * 23.83 GPa 아래 — enstatite (MgSiO₃ 저압상). Seager+ 2007 Table 1 의 BME 적합.
#   Seager 자신이 §IV.2.1 에서 10 GPa 아래를 enstatite 로 두고, 그 선택이 반지름을
#   1 % 미만 움직인다고 적는다.
# * 23.83 GPa 위 — PREM 하부맨틀 BM2 적합 (Zeng+ 2016 §II: "Lower Mantle:
#   ρ₀ = 3.98 g/cc, K₀ = 206 GPa").
# * 3.5 TPa 위 — Seager+ 2007 의 MgSiO₃ 페로브스카이트 BME4. 아래에 사정을 적는다.
#
# ── 3.5 TPa 위: 왜 상이 하나 더 필요했고, 왜 **하나** 면 됐나 ──────────────
#
# PREM 하부맨틀 적합의 3.5 TPa 는 우리가 고른 수가 아니라 Zeng+ 2016 §II 가 자기 적합의
# 상한으로 적은 수다 — "mantle (good up to 3.5 TPa where it asymptotically approaches
# TFD)". 같은 절이 그 위에 무엇을 쓰라고까지 적는다: "> 3.5 TPa: TFD EOS of MgSiO₃
# calculated using method in (Salpeter & Zapolsky 1967)".
#
# **그 처방을 따르지 않았다.** TFD 는 재료의 적합이 아니라 전자축퇴의 점근이고, 이
# 레시피는 그 영역을 이름 대며 거절하는 쪽을 택했다. 대신 그 사이를 메우는 적합이
# 문헌에 있는지를 물었고, 있었다 — **이 파일이 이미 쓰고 있는 논문 안에** 있었다.
#
# Seager+ 2007 §III.3 (arXiv:0707.2895) 이 규산염을 이렇게 만든다. "For a silicate EOS
# we use the perovskite phase of MgSiO₃. We use a fourth order BME fit up to
# P = 1.35×10⁴ GPa. At this pressure we switch to the TFD EOS. The fourth order BME fit
# is from a density functional calculation up to P = 150 GPa by Karki et al. 2000. …
# the fourth order BME is the only fit we found that smoothly matches the TFD EOS at
# high pressures." 상수는 그 논문 Table 1 의 MgSiO₃(pv) 행이다.
#
#     ρ₀ = 4.10 Mg/m³ · K₀ = 247 ± 4 GPa · K₀′ = 3.97 · 적합 BME4 · K₀″ = −0.016 /GPa
#     log₁₀ P_V/T = 13.13  (= 1.35×10⁴ GPa. Vinet/BME 가 TFD 로 넘어가는 압력)
#
# **이 구성은 이 파일에 이미 선례가 있다.** fe_eps 의 상한 2.09×10⁴ GPa 가 정확히 같은
# 절의 같은 문장에서 왔다 ("a Vinet fit up to P = 2.09×10⁴ GPa … we switch to the TFD
# EOS"). 철은 Seager 에서, 규산염은 Zeng 에서 가져왔기 때문에 상한이 20.9 TPa 대 3.5 TPa
# 로 갈렸던 것이고, 빠져 있던 것은 새 물리가 아니라 **Seager 의 규산염 행** 이었다.
#
# **왜 하나면 되나 — 상전이는 실재하지만 전부 3.5 TPa 아래다.** Umemoto+ 2017 §3.1
# (arXiv:1708.04767) 이 MgSiO₃ 의 사다리를 제일원리로 준다. PPv → Mg₂SiO₄ + MgSi₂O₅ 가
# 0.75 TPa, → Mg₂SiO₄ + Fe₂P-형 SiO₂ 가 1.31 TPa, → CsCl-형 MgO + Fe₂P-형 SiO₂ 가
# 3.10 TPa 다. 그리고 같은 논문의 결론이 그 위를 닫는다 — "The last solid-solid
# transition identified so far remains the dissociation of Mg₂SiO₄ into the pure oxides
# Fe₂P-type SiO₂ and CsCl-type MgO at 3 TPa at low temperatures." 즉 3.5 TPa 위에서는
# **알려진 상전이가 없다.** 이어 붙일 상이 하나인 것은 그래서다. 셋은 이미 PREM 적합이
# 덮는 구간 안에 있고, 그 구간을 건드리면 앵커가 움직인다.
#
# **그러면 이 상은 무엇의 적합인가 — 이름과 실물이 다르다는 것을 적어둔다.** 3.5 TPa
# 위의 실물은 페로브스카이트가 아니라 MgO + SiO₂ 다. Seager 의 적합에 붙은 이름은
# 'perovskite' 이고, 그 이름을 믿는 근거가 아니라 **조성이 그 압력에서 밀도를 거의
# 정하지 않는다** 는 것이 근거다. Zeng+ 2016 §II 가 그것을 수로 적는다 — "the TFD beyond
# 1 TPa for MgO, SiO₂, MgSiO₃, and Mg₂SiO₄ are almost identical as they all have average
# atomic weight A=20 and average atomic charge Z=10 … it indicates that Mg/Si ratio does
# not matter towards the high-pressure end." Seager 자신도 §IV.2.1 에서 고압 상전이의
# EOS 효과를 "small" 이라고 적는다. 이 근거는 조성 무관성이지 결정구조의 동일성이
# 아니고, 그래서 이 구간은 등급이 내려간다 (interior.py 의 SILICATE_EXTRAPOLATED_MIN).
#
# **이음매는 지어낸 것이 아니라 재본 것이다.** 3.5 TPa 에서 PREM BM2 가 14293 kg/m³,
# 이 BME4 가 14263 kg/m³ 로 **0.21 % 차이** 다. 지진학 적합과 DFT 적합이 서로를 모른 채
# 그 압력에서 겹친 것이고, 그래서 이 자리에 밀도 도약을 넣지 않았다. test_interior.py 가
# 그 0.21 % 를 다시 잰다.
#
# **K₀″ 를 3차로 반올림하면 안 된다.** BME3 의 암묵적 K₀″ 는
# −(1/K₀)[(3−K₀′)(4−K₀′) + 35/9] = −0.01563 /GPa 로, Seager 가 적은 −0.016 /GPa 와
# 2.3 % 차이다. 그런데 그 차이가 f² 항을 타고 커져서 13.5 TPa 에서 밀도가 9.1 % 벌어진다.
# 즉 이 재료는 BME3 으로 근사할 수 없고, 그래서 BME4 형태가 필요했다. 그 감도를
# test_interior.py 가 실제로 재서 보여준다.
#
# **상한 위는 여전히 전자축퇴다.** 1.35×10⁴ GPa 는 Seager 가 TFD 로 갈아타는 압력이므로,
# 이 재료의 상한은 "적합이 떨어졌다" 가 아니라 "여기부터는 축퇴가 지배한다" 는 뜻이다.
# 물얼음의 37.4 GPa 와 같은 종류의 울타리이고, 아래 over_reason 이 그렇게 말한다.
SILICATE_EN_TO_PREM = 23.83 * GPA    # Zeng+ 2016 §II.1 상부→하부 맨틀 전이
SILICATE_PREM_TO_PV = 3.5e3 * GPA    # Zeng+ 2016 §II — PREM 하부맨틀 적합의 상한
SILICATE_PV_TO_TFD = 1.35e4 * GPA    # Seager+ 2007 §III.3 — BME4 가 TFD 로 넘어가는 압력


# ── 규산염 녹는곡선 — 압력대별 갈아타기, 분화-시딩 (브리프 36) ──────────────────
#
# 철(Zhang & Rogers 2022)과 물(IAPWS·Reinhardt)에는 녹는곡선이 있는데 규산염에는
# 없었다 — 그래서 솔버가 "암석 맨틀이 녹았는가" 를 말하지 못했다. 여기의 사슬이
# 그 구멍을 닫는다. **형태는 오너 결정(2026-09-02, 브리프 36 + 정정)**: 암석 자료가
# 있는 데까지 암석을 쓰고(0–140 GPa, Monteux), 그 위는 순수 MgSiO₃(Deng·Fei)로
# 갈아타되 이음매의 계단을 **물질 종류 차이의 선언**으로 라벨하고 절대 뭉개지 않는다.
#
#   0 – 20 GPa      Monteux+ 2016 식 (10)/(11) — Herzberg & Zhang 1996 의 실험 적합.
#                   조성 하나만 인쇄되어 있어(본문 "chondritic mantle", 그 논문 제목은
#                   "anhydrous peridotite KLB-1" — Monteux 내부 긴장, 우리가 안 푼다)
#                   **조성 선택은 이 구간에서 곡선을 못 바꾼다.**
#   20 – 140 GPa    솔리더스 = 식 (12) (A-콘드라이트, Andrault+ 2011 — Monteux 자신이
#                   "F 와 A 의 솔리더스 차이가 크지 않다" 며 양쪽에 이걸 쓴다).
#                   리퀴더스 = 식 (13), **조성이 여기서 갈린다**: F-페리도타이트
#                   (Fiquet+ 2010) 대 A-콘드라이트 (Andrault+ 2011). 20 GPa 에서 0 K,
#                   140 GPa 에서 +879 K (F 가 더 내화성 — 잔류물이라 그래야 한다).
#   ~140 GPa 이음매  암석 → 순수 MgSiO₃. **조성 차이가 아니라 물질 종류 차이**이고
#                   계단은 선언 그 자체다. 140 GPa 채택 근거: Andrault+ 2011 의 적합
#                   범위는 논문 미확보로 **범위 미확인**이며, Monteux 는 "지구 최하부
#                   맨틀 조건까지" 라고만 적는다 — 다만 Monteux 자신의 모델이 곡선을
#                   140 GPa 에서 구사하므로("melt fraction ≈ 40% at P = 140 GPa")
#                   인쇄 출처가 스스로 밟은 압력을 경계로 택했다. 대안은 지구 CMB
#                   136 GPa 였다.
#   140 – 180 GPa   Deng+ 2023 bridgmanite (Table I 자료 20–160 GPa; 160–180 은
#                   그 위 20 GPa 외삽 — 라벨). 180 GPa = 논문이 인쇄한 bdg/ppv/액체
#                   삼중점. 논문 내부 불일치 병기: 두 적합의 교차는 173.6 GPa/6413 K,
#                   인쇄된 삼중점은 180 GPa/6420 K — 삼중점은 원자료에서 왔다.
#   180 – 200 GPa   Deng+ 2023 post-perovskite. 200 GPa = 논문 자신의 경고 경계
#                   ("extrapolating beyond ~200 GPa is subject to uncertainty").
#   200 – 500 GPa   Fei+ 2021 상계 (Z-머신 충격압축; 멜팅 구속은 ~500 GPa 까지).
#   500 GPa 위      **이름 대고 거절** — 여섯 논문 어디에도 자료가 있는 전사 가능한
#                   MgSiO₃ 곡선이 없다 (규산염 사다리는 13.5 TPa 까지 가는데도).
#
# **140 GPa 위의 순수 광물 곡선은 암석 솔리더스의 상계로 읽는다**: 순수 내화 광물은
# 저융점 성분이 있는 암석보다 높은 온도에서 녹으므로, T 가 곡선 위면 암석은 확실히
# (적어도 부분) 용융이고, 곡선 아래면 **미정**이다 — "안 녹았다" 는 말은 못 한다.
# 단일점 융해에는 명목 폭(아래 SILICATE_MELT_POINT_WIDTH)을 선언해 적분기가 칼날
# 계단을 밟지 않게 한다.
#
# 라벨 규율: Monteux 는 **인쇄 출처이지 적합자가 아니다** — "연속성 재적합" 이라는
# 말은 1차 본문에 없다(서베이 ⑬이 자기 앞선 보고를 철회). 실험 출처는 Herzberg &
# Zhang 1996 / Andrault+ 2011 / Fiquet+ 2010. 그리고 기록해 둘 조건 하나: Monteux 의
# 리퀴더스 세 가지가 20 GPa 에서 0.040 K 안에서 만난다 — 따로 인용된 실험 적합
# 셋이 다섯 자리로 우연히 만나지 않으므로 누군가 그 일치를 만들었고 논문은 말하지
# 않는다(당사자 미지목; Andrault+ 2011 확보가 이 열린 질문을 닫는다).
SILICATE_MELT_REF = "Monteux+ 2016 (2016E&PSL.448..140M) §2.2.1 식 (10)–(13)"
# 식 (10)/(11): P < 20 GPa, Herzberg & Zhang 1996 의 콘드라이트질 맨틀 (T [K], P [Pa]).
# ⚠ 솔리더스 스케일은 **1.336×10⁹ Pa** — 1차 275행에서 확정. 널리 인용되는 2차 표기
# (Walterová & Behounková 2020)의 1336×10⁹ 은 오식이고, 그대로 쓰면 위성·소형행성
# 전 범위에서 750 K 차갑다. test_silicate_melt.py 가 이 함정을 조인 잔차로 고정한다.
MONTEUX_SOL_LOW = (1661.2, 1.336e9, 7.437)    # 식 (10)
MONTEUX_LIQ_LOW = (1982.1, 6.594e9, 5.374)    # 식 (11)
MONTEUX_SOL_HIGH = (2081.8, 101.69e9, 1.226)  # 식 (12), A-콘드라이트 (Andrault+ 2011)
# 식 (13): T_liq = c₁(P/c₂ + 1)^(1/c₃). 두 조성이 여기서 갈린다.
MONTEUX_LIQ_F = (78.74, 4.054e6, 2.44)        # F-페리도타이트 (Fiquet+ 2010)
MONTEUX_LIQ_A = (2006.8, 34.65e9, 1.844)      # A-콘드라이트 (Andrault+ 2011)
MONTEUX_JOIN_PA = 20e9                        # 논문 자신의 저압/고압 가지 전환
SILICATE_ROCK_MAX_PA = 140e9                  # 암석→순수 MgSiO₃ 이음매 (위 주석의 근거)
# Deng+ 2023 (2023PhRvB.107f4103D) 본문의 두 Simon 적합 (T [K], P [GPa]).
# 전사 확정: 인쇄된 외삽점 "9376 ± 656 K at 500 GPa" 를 전사식이 9376.6 K 로 낸다.
DENG_BDG = (2875.0, 20.0, 8.11, 3.73)         # Tm = 2875·((P−20)/8.11 + 1)^(1/3.73)
DENG_PPV = (5600.0, 120.0, 113.60, 2.85)      # Tm = 5600·((P−120)/113.60 + 1)^(1/2.85)
# bdg 적합은 (P−20)/8.11+1 = 0 이 되는 **11.89 GPa 아래에서 산술적으로 정의되지
# 않는다** — 산문이 아니라 계수 안에 사는 범위 한계(서베이 ⑬ 신규 종류 (f)). 체제상
# 140 GPa 아래로는 안 내려가지만, 잘못 호출되면 조용한 복소수 대신 이름을 대게 한다.
DENG_BDG_FLOOR_GPA = 20.0 - 8.11              # = 11.89, 계수의 성질이지 논문의 진술이 아니다
DENG_TRIPLE_PA = 180e9                        # 인쇄된 bdg/ppv/액체 삼중점 (교차는 173.6)
DENG_CEILING_PA = 200e9                       # 논문 자신의 외삽 경고 경계
FEI_UPPER = (6295.0, 140.0, 0.317)            # Fei+ 2021: Tm = 6295·(P/140)^0.317 [K, GPa]
SILICATE_MELT_MAX_PA = 500e9                  # 이 위는 자료 있는 전사 가능 곡선이 없다
# 잠열과 부분용융 열역학 — Monteux+ 2016 §2.2.2, Solomatov 2007 을 따른 인쇄식.
#   식 (6):  φ = (T − T_sol)/(T_liq − T_sol)            ← 용융분율, 인쇄된 정의
#   식 (17): C′_p = C_p + ΔH/(T_liq − T_sol)            ← 겉보기 비열 (채택)
#   식 (16): α′ = α + Δρ/(ρ(T_liq−T_sol)) 는 **인쇄돼 있으나 비채택** — 식 (15)의
#   용융 밀도를 채택하지 않으므로(밀도는 고체 EOS 그대로), 16만 넣으면 고체 밀도
#   기둥에 용융 팽창 기울기를 섞는 비일관이 된다. 기록만 남긴다: Δρ/ρ = 1.5 %
#   (Monteux Table 1, Tosi et al.).
SILICATE_MELT_DH = 4.0e5      # J/kg. Monteux+ 2016 Table 1, ΔH (Ghosh & McSween 1998)
# 단일점 융해(140 GPa 위 순수 MgSiO₃)의 명목 부분용융 폭. **선언이고 채워 넣은
# 값이다** — 실제 다성분 암석은 솔리더스와 리퀴더스가 따로 인쇄되어 폭이 측정에서
# 오지만(20 GPa 에서 158 K, 140 GPa 에서 606 K), 순수 광물 단일점에는 인쇄된 폭이
# 없어 적분기 안정용 명목값을 선언한다. 브리프 36 의 100–200 K 대의 중앙.
SILICATE_MELT_POINT_WIDTH = 150.0   # K. 선언 (명목), 논문값 아님


def _simon_pa(p: float, t0: float, p_scale: float, c: float) -> float:
    """Simon–Glatzel 형 T = t0·(P/p_scale + 1)^(1/c). P [Pa]."""
    return t0 * (p / p_scale + 1.0) ** (1.0 / c)


def _silicate_melt_point(p: float) -> float | None:
    """140–500 GPa 순수 MgSiO₃ 단일 녹는점 [K]. 사슬: Deng bdg → ppv → Fei 상계."""
    if p > SILICATE_MELT_MAX_PA:
        return None
    gpa = p / GPA
    if p >= DENG_CEILING_PA:                       # 200–500 GPa: Fei+ 2021 상계
        t0, p_ref, ex = FEI_UPPER
        return t0 * (gpa / p_ref) ** ex
    if p >= DENG_TRIPLE_PA:                        # 180–200 GPa: Deng ppv
        t0, p0, a, c = DENG_PPV
        return t0 * ((gpa - p0) / a + 1.0) ** (1.0 / c)
    if gpa < DENG_BDG_FLOOR_GPA:
        raise ValueError(
            f"Deng+ 2023 bridgmanite 적합은 {DENG_BDG_FLOOR_GPA:.2f} GPa 아래에서 "
            f"산술적으로 정의되지 않는다 ((P−20)/8.11+1 ≤ 0, {gpa:.2f} GPa 요청) — "
            "계수 안에 사는 범위 한계다. 이 압력의 곡선은 Monteux 암석 가지가 맡는다.")
    t0, p0, a, c = DENG_BDG                        # 140–180 GPa: Deng bdg
    return t0 * ((gpa - p0) / a + 1.0) ** (1.0 / c)


def _silicate_variant_check(variant: str) -> None:
    if variant not in ("peridotitic", "chondritic"):
        raise ValueError(
            f"미등록 규산염 조성: {variant!r} — peridotitic | chondritic. "
            "조성은 differentiated 선언에서 온다 (interior.solve).")


def silicate_solidus(p: float, variant: str = "peridotitic") -> float | None:
    """압력 p [Pa] 에서 규산염 솔리더스 [K]. 500 GPa 위는 None (곡선 없음).

    조성(variant)은 리퀴더스에서만 곡선을 바꾼다 — 솔리더스는 20 GPa 아래 HZ96,
    20–140 GPa 는 Monteux 가 양쪽 조성에 같이 쓰는 A-콘드라이트 식 (12)다.
    140 GPa 위는 순수 MgSiO₃ 단일점 − 명목 폭/2 이고 **암석 솔리더스의 상계**로
    읽는다 (위 블록 주석)."""
    _silicate_variant_check(variant)
    if p < 0.0 or p > SILICATE_MELT_MAX_PA:
        return None
    if p < MONTEUX_JOIN_PA:
        return _simon_pa(p, *MONTEUX_SOL_LOW)
    if p < SILICATE_ROCK_MAX_PA:
        return _simon_pa(p, *MONTEUX_SOL_HIGH)
    tm = _silicate_melt_point(p)
    return None if tm is None else tm - 0.5 * SILICATE_MELT_POINT_WIDTH


def silicate_liquidus(p: float, variant: str = "peridotitic") -> float | None:
    """압력 p [Pa] 에서 규산염 리퀴더스 [K]. 조성이 20–140 GPa 에서 곡선을 바꾼다."""
    _silicate_variant_check(variant)
    if p < 0.0 or p > SILICATE_MELT_MAX_PA:
        return None
    if p < MONTEUX_JOIN_PA:
        return _simon_pa(p, *MONTEUX_LIQ_LOW)
    if p < SILICATE_ROCK_MAX_PA:
        coef = MONTEUX_LIQ_F if variant == "peridotitic" else MONTEUX_LIQ_A
        return _simon_pa(p, *coef)
    tm = _silicate_melt_point(p)
    return None if tm is None else tm + 0.5 * SILICATE_MELT_POINT_WIDTH


def silicate_melt_fraction(p: float, t: float, variant: str = "peridotitic") -> float | None:
    """용융분율 φ = (T − T_sol)/(T_liq − T_sol), 0..1 로 잘라서 (Monteux+ 2016 식 (6)).

    **단일 진리원이다** — 상 이름·겉보기 비열·하류 가중치가 전부 이 수 하나를 읽어야
    한 천체가 묻는 사람에 따라 다른 결정:용융 비를 보이지 않는다 (C7·C11 이 분화
    상태에 쓰는 원리와 같다). 곡선 밖(500 GPa 위)이나 온도 미선언(t ≤ 0)은 None —
    0 인 척하지 않는다. 140 GPa 위에서 0.0 은 "확실히 고체" 가 아니라 "상계 아래" 다."""
    if t <= 0.0:
        return None
    sol = silicate_solidus(p, variant)
    if sol is None:
        return None
    liq = silicate_liquidus(p, variant)
    if t <= sol:
        return 0.0
    if t >= liq:
        return 1.0
    return (t - sol) / (liq - sol)


def silicate_melt_refusal(p: float) -> str:
    """500 GPa 위에서 곡선이 없는 이유 — 이름 대는 거절문."""
    return (f"{p / GPA:.0f} GPa 는 규산염 녹는곡선의 상한(500 GPa) 위다. 자료가 있는 "
            "전사 가능한 MgSiO₃ 곡선이 그 위에 없다 — Fei+ 2021 의 융해 구속이 "
            "~500 GPa 에서 끝나고, 1400 GPa 를 표방하는 후보(Nguyen Quang Hoc+ 2024)는 "
            "그 수가 그림에만 산다(인쇄 표는 100 GPa 까지). 규산염 EOS 사다리는 "
            "13.5 TPa 까지 가므로 그 구간의 고체·액체는 판정하지 않는다. TPa 대의 "
            "답이 곡선이 아니라 선언된 '고체' 일 가능성(González-Cataldo+ 2016 이 "
            "실리카에 대해 그렇게 결론)은 기록만 하고 채택하지 않았다 — 유추이지 "
            "결과가 아니다.")


SILICATE = Material(
    "silicate", "규산염 맨틀",
    (Phase("mgsio3_en", "bme3", 3220.0, 125.0 * GPA, 5.0, SILICATE_EN_TO_PREM,
           "Seager+ 2007 Table 1 (arXiv:0707.2895) — MgSiO₃ enstatite BME",
           alpha_k=SILICATE_ALPHA_K, c_v_ref=CV_SILICATE,
           t_ref=EARTH_POTENTIAL_T, t_ref_kind="adiabat",
           melt="silicate", melt_ref=SILICATE_MELT_REF + " + Deng+ 2023 + Fei+ 2021 — "
           "압력대별 사슬, 조성은 differentiated 시딩 (블록 주석)"),
     Phase("mgsio3_prem", "bm2", 3980.0, 206.0 * GPA, 4.0, SILICATE_PREM_TO_PV,
           "Zeng+ 2016 §II (arXiv:1512.08827) — PREM 하부맨틀 BM2 적합",
           p_min=SILICATE_EN_TO_PREM, alpha_k=SILICATE_ALPHA_K, c_v_ref=CV_SILICATE,
           t_ref=EARTH_POTENTIAL_T, t_ref_kind="adiabat",
           melt="silicate", melt_ref=SILICATE_MELT_REF + " + Deng+ 2023 + Fei+ 2021 — "
           "500 GPa 위는 곡선 밖 (silicate_melt_refusal)"),
     Phase("mgsio3_pv", "bme4", 4100.0, 247.0 * GPA, 3.97, SILICATE_PV_TO_TFD,
           "Seager+ 2007 Table 1 · §III.3 (arXiv:0707.2895) — MgSiO₃ perovskite BME4, "
           "Karki+ 2000 의 DFT 계산. 실물은 MgO + SiO₂ 다 (Umemoto+ 2017, "
           "arXiv:1708.04767) — 조성이 이 압력대에서 밀도를 거의 안 정한다는 것이 근거",
           p_min=SILICATE_PREM_TO_PV, k0pp=-0.016 / GPA,
           alpha_k=SILICATE_ALPHA_K, c_v_ref=CV_SILICATE,
           t_ref=EARTH_POTENTIAL_T, t_ref_kind="adiabat",
           melt="silicate", melt_ref="이 상의 압력대(3.5–13.5 TPa)는 전부 곡선 상한 "
           "(500 GPa) 위라 t_melt 가 항상 None 이다 — 판정하지 않는다는 사실의 기록")),
    over_reason=("규산염 기둥 바닥이 {p_gpa:.0f} GPa 로 근거 구간의 상한"
                 "({max_gpa:.0f} GPa) 위다. 그 상한은 Seager+ 2007 §III.3 이 규산염의 "
                 "BME4 를 놓고 TFD 로 갈아타는 압력이므로, 그 위는 전자축퇴가 지배하는 "
                 "영역이고 (Salpeter & Zapolsky 1967), 이 레시피에는 그 상태방정식이 "
                 "없다. 암석이 많은 아주 큰 천체는 여기서 멈춘다."),
    # 2026-08-27 에 mgsio3_pv 가 들어와 enstatite 부터 13.5 TPa 까지 사다리가 이어졌다.
    # 그래서 이 설명은 도달하지 않는다 — 도달하면 전이압 상수 하나가 이웃과 어긋나게
    # 편집된 것이다. test_interior.py 가 사다리의 연속성을 따로 확인한다.
    gap_reason=("{p_gpa:.4f} GPa 가 규산염 상 사다리의 두 상 **사이** 에 떨어졌다. "
                "enstatite(~23.83 GPa) · PREM 하부맨틀(~3.5 TPa) · MgSiO₃(pv) 는 "
                "이어져 있어야 하므로, 이건 물리가 아니라 전이압 상수가 이웃과 어긋나게 "
                "편집됐다는 뜻이다."),
)

# 미분화(한 번도 녹지 않은) 암석의 규산염 — 같은 상태방정식, 녹는곡선 조성만
# A-콘드라이트 가지다. **조성은 differentiated 선언에서 온다** (분화 잔류물 =
# 페리도타이트 = 위의 SILICATE 기본값; 원시 미분화 = 콘드라이트질 = 이 변형).
# 이 연결은 논문이 시킨 게 아니라 우리 선언이다 — 물리 검산: 잔류물은 저융점 성분이
# 빠져 더 내화성이어야 하고, 인쇄된 F 리퀴더스가 실제로 A 보다 뜨겁다(140 GPa 에서
# +879 K). 20 GPa 아래는 인쇄된 조성이 하나라 두 변형이 같은 곡선을 쓴다.
from dataclasses import replace as _dc_replace

SILICATE_CHONDRITIC = Material(
    "silicate_chondritic", "규산염 맨틀 (미분화, A-콘드라이트 녹는곡선)",
    tuple(_dc_replace(ph, melt_variant="chondritic") for ph in SILICATE.phases),
    over_reason=SILICATE.over_reason, gap_reason=SILICATE.gap_reason,
)

# ── 물 ──────────────────────────────────────────────────────────────────
#
# 얼음은 상이 갈린다. 녹는곡선을 따라가면 Ih → III → V → VI → VII 이고, 전이압은
# 네 삼중점이 정한다. 넷 다 Choukroun & Grasset 2007 (VI→VII 만 Daucik & Dooley
# 2011) 의 값이고, Zeng & Sasselov 2013 §III.3.1 (arXiv:1301.0818) 이 행성 모형에
# 채택한 것을 그대로 읽었다.
#
#     Ih  → III    209.5 MPa / 251.15 K
#     III → V      355.0 MPa / 256.43 K
#     V   → VI     618.4 MPa / 272.73 K
#     VI  → VII    2.216 GPa / 355 K
#
# **III·V·VI 의 세 상수는 적합한 게 아니라 읽은 것이다.** SeaFreeze v1.1.0 이 얼음
# III·V·VI 의 Gibbs 표현을 들고 있고 (Journaux+ 2020, JGR Planets 125, e2019JE006176),
# 각 상의 기준 등온에서 P = 0 의 ρ · K_T · K′ 를 그 자리에서 평가해 BME3 의 ρ₀ · K₀ ·
# K₀′ 로 쓴다. 얼음 Ih 이 IAPWS-06 검증표에서 ρ 와 κ_T 를 읽어 BM2 로 들어온 것과
# **같은 구성** 이다 — 곡선을 맞춘 상수가 아니라 기준 상태의 상태량이다.
#
# 기준 등온은 그 상이 시작하는 삼중점의 온도로 잡았다. 세 상에 규칙 하나이고, 얼음 Ih 이
# 녹는점에서 읽힌 것과 결이 같다. 그렇게 세운 BME3 가 각 상의 유효 구간 전체에서
# SeaFreeze 의 ρ(P) 와 0.006 % · 0.014 % · 0.118 % 안에서 같아서, 적합할 이유가 없었다.
#
# **온도는 값이다.** 녹는곡선이 구간 안에서 올라가므로 구간 상단에서 기준 등온과의 밀도
# 차가 III 0.11 % · V 0.27 % · VI 1.3 % 다. 얼음 VI 의 구간이 82 K 에 걸쳐 넓어서 그쪽이
# 크고, 그 1.3 % 가 이 재료의 정직한 오차폭이다.
#
# **SeaFreeze 는 런타임 의존성이 아니다.** 이 파일의 다른 재료가 전부 발표된 상수를 박아둔
# 형태이고 scripts/check.sh 가 무거운 의존성 없이 돌아야 한다. 대신 test_interior.py 가
# SeaFreeze 가 있을 때만 도는 대조 절을 들고 있어서, 박아둔 상수가 원 표현과 어긋나면 그
# 자리에서 잡히고, 없으면 그 절만 건너뛴다.
#
# 얼음 Ih 의 두 상수는 IAPWS-06 (Feistel & Wagner 2006) 의 검증표에서 직접 읽었다.
# T = 273.152519 K, p = 101 325 Pa 에서 ρ = 916.721463419 kg/m³ 이고
# κ_T = 1.17785291765e-10 Pa⁻¹ 이므로 K_T = 1/κ_T = 8.490 GPa 다.
# K₀′ 는 그 표에 없어서 BM2 (K₀′ = 4 고정) 를 쓴다. Ih 이 존재하는 구간 전체에서
# 압축이 2.4 % 뿐이라 K₀′ 를 4 로 두든 6 으로 두든 밀도가 0.2 % 안에서 같다 —
# test_interior.py 가 그 감도를 실제로 재서 보여준다. SeaFreeze 의 얼음 Ih 도 같은
# IAPWS-06 이라, 그 표현을 같은 상태에서 평가하면 ρ 가 아홉 자리까지 겹친다. 그 일치가
# III·V·VI 을 같은 표현에서 읽어올 근거다.
ICE_IH_RHO0 = 916.721463419        # IAPWS-06 Table 6, T=273.152519 K, p=101325 Pa
ICE_IH_KT = 1.0 / 1.17785291765e-10  # 같은 표의 κ_T 를 뒤집은 것. 8.490 GPa
ICE_IH_TO_III = 209.5 * MPA        # Choukroun & Grasset 2007 삼중점
ICE_III_TO_V = 355.0 * MPA         # Choukroun & Grasset 2007 삼중점 (256.43 K)
ICE_V_TO_VI = 618.4 * MPA          # Choukroun & Grasset 2007 삼중점 (272.73 K)
ICE_VI_TO_VII = 2.216 * GPA        # Daucik & Dooley 2011 (Zeng & Sasselov 2013 §III.3.1 경유)

# 기준 등온에서 P = 0 의 (ρ₀, K₀, K₀′). SeaFreeze v1.1.0 을 그 자리에서 평가한 값이고,
# 세 상 모두 상이 시작하는 삼중점의 온도를 기준으로 삼았다.
# 열 상수도 **같은 자리에서 같은 방식으로** 읽었다 — SeaFreeze v1.1.0 을 각 상의 기준
# 상태에서 평가한 αK_T 와 c_V 다. 얼음의 Debye 온도가 ~300 K 이고 이 상들이 존재하는
# 온도가 그 아래라, Dulong-Petit 극한을 쓰면 c_V 가 두 배 넘게 틀린다. 그래서 규산염·철과
# 달리 읽어 왔다.
#
# **그리고 그 대가로 얻는 것이 이 파일이 이미 적어둔 수의 검증이다.** 아래 주석은 기준
# 등온과 구간 상단의 밀도 차를 III 0.11 % · V 0.27 % · VI 1.3 % 로 적어두고 그것을 "이
# 재료의 정직한 오차폭" 이라고 불렀다. 그 수는 SeaFreeze 와 대조해서 **잰** 것이다. 이제
# 열 항이 들어왔으므로 같은 수가 **계산돼서** 나와야 하고, test_interior.py 가 그 둘을
# 맞춰 본다. 맞으면 열 항의 크기가 독립적으로 확인된 것이다.
#
# **얼음 VII 에는 열 상수가 없다.** SeaFreeze 의 얼음 VII 는 별개 표현(VII_X_French)이라
# 이 파일의 VII (Seager+ 2007 / Hemley+ 1987) 와 기준이 다르고, Seager 자신은 얼음 VII 의
# 열압력을 Fei+ 1993 의 관계식에 Frank+ 2004 의 매개변수를 넣어 만들었을 뿐 옮겨 적을
# 상수를 싣지 않았다. 그래서 얼음 VII 은 **등온으로 남는다.** 있는 척하지 않는다.
ICE_IH_ALPHA_K = 1.357059e6        # Pa/K. SeaFreeze Ih 를 273.152519 K, 101325 Pa 에서
ICE_IH_CV = 2032.079310            # J/kg/K. 같은 상태
ICE_III_ALPHA_K = 2.048279e6       # Pa/K. SeaFreeze III 를 P=0, T=251.15 K 에서
ICE_III_CV = 1769.447868           # J/kg/K. 같은 상태
ICE_V_ALPHA_K = 2.369011e6         # Pa/K. SeaFreeze V 를 P=0, T=256.43 K 에서
ICE_V_CV = 1742.729067             # J/kg/K. 같은 상태
ICE_VI_ALPHA_K = 3.739766e6        # Pa/K. SeaFreeze VI 를 P=0, T=272.73 K 에서
ICE_VI_CV = 2053.963382            # J/kg/K. 같은 상태

ICE_III_REF_T = 251.15             # K. Ih→III 삼중점
ICE_V_REF_T = 256.43               # K. III→V 삼중점
ICE_VI_REF_T = 272.73              # K. V→VI 삼중점

# ── 얼음 VII 과 얼음 X — 하나의 퍼텐셜, 두 칸 ────────────────────────────
#
# 2026-08-27 에 "얼음 VII 에는 열 상수가 없다" 고 적었고, 그건 **논문** 을 찾은
# 결과였다. 그때 놓친 것은 이 파일이 이미 기대고 있는 SeaFreeze 가 여섯 번째 표현을
# 싣고 있다는 사실이다 — `VII_X_French` 이고, 패키지 README 가 출처를 French & Redmer
# 2015 (2015PhRvB..91a4308F, "Construction of a thermodynamic potential for the water ices
# VII and X") 로 적는다. 셔플된 스플라인에서 매듭 구간을 직접 읽으면
#
#     P 1.7 GPa ~ 1000 GPa · T 20 K ~ 1800 K        (SeaFreeze v1.1.0)
#
# 이다. 얼음 III·V·VI 이 들어온 것과 **같은 출처의 같은 구성** 이라, 같은 방식으로
# 읽는다. (README 머리말은 "up to 100 GPa and 10,000 K" 라고 적는데 실제 매듭 구간은
# 위쪽이다. 우리가 쓰는 것은 스플라인이므로 매듭 구간을 따른다.)
#
# **VII 과 X 를 가르지 않는다.** French & Redmer 는 둘을 하나의 자유에너지로 다룬다 —
# VII→X 는 수소결합이 연속적으로 대칭화되는 것이라 밀도 도약이 없고, 옛 거절 문구가
# 이름 대던 Goncharov+ 2005 의 47 GPa 는 그 대칭화가 끝나는 자리이지 새 상태방정식이
# 시작하는 자리가 아니다. 그래서 사다리에 붙는 칸은 **하나** 다.
#
# ── 왜 읽지 않고 적합했나 ────────────────────────────────────────────────
#
# 얼음 III·V·VI 은 P = 0 의 (ρ, K_T, K′) 를 읽어서 BME3 에 그대로 꽂았고, 그 셋이 BME3
# 이 받는 전부라 적합할 이유가 없었다. 여기서는 그 길이 막힌다. 매듭 구간이 1.7 GPa 에서
# 시작해 P = 0 을 평가할 수 없고, 37.4 GPa 에서 (ρ, K_T, K′) 를 읽어 BME3 을 거꾸로 풀면
# 1 TPa 에서 **15.5 %** 어긋난다 — 국소적으로 읽은 세 값은 27배의 압력 구간을 못 건넌다.
#
# 그래서 이 상은 **적합** 이다. 쓰는 구간(37.4 GPa ~ 1 TPa)의 300 K 등온선에 최소제곱으로
# 맞췄고, 형태 셋을 같은 자료에 대봤다.
#
#     Vinet  ρ₀ 1644.29 · K₀ 22.29 GPa · K₀′ 6.75   최악 1.475 %   ← 이걸 쓴다
#     BME3   ρ₀ 1855.97 · K₀ 58.37 GPa · K₀′ 4.67   최악 1.621 %
#     BME4                                          발산
#
# Vinet 이 이긴 것이 우연이 아니고 이 파일 자신의 규칙이 가리키던 쪽이다 — Seager+ 2007
# §III.1 이 고압 외삽에서 Vinet 이 BME 보다 낫다고 적고, Fe(ε) 가 그래서 Vinet 이다.
# 잔차는 양 끝이 제일 크고(37.4 GPa 에서 +1.48 %, 1 TPa 에서 −1.02 %) 가운데가 0.5 % 쯤이다.
# 두 조각으로 쪼개면 0.26 % 까지 내려가지만 아래 조각의 상수가 ρ₀ = 382 kg/m³ · K₀ =
# 0.4 MPa 로 나온다 — 무엇의 상수도 아닌 적합 부산물이고, 이 파일은 뜻 없는 상수를 안 싣는다.
#
# **1.475 % 가 이 상의 정직한 오차폭이고, 사다리에서 제일 넓다.** 등급이 내려가는 이유다.
#
# ── 이음매 ──────────────────────────────────────────────────────────────
#
# 37.4 GPa 에서 기존 얼음 VII (Hemley+ 1987 자료의 BME3) 이 2467.7 kg/m³, 이 Vinet 이
# 2524.0 kg/m³ 로 **−2.26 %** 다. 3분의 2는 이 적합이 자기 구간 아래 끝에서 +1.48 % 넘치는
# 몫이고, 나머지는 1987년 실험 적합을 37.4 GPa 까지 끌고 간 값이 2015년 퍼텐셜보다 0.82 %
# 낮은 몫이다. 어느 쪽도 상대에 맞춰 당기지 않았다 — 당기면 우리 출력에 적합하는 것이고
# 규율 3 이 금지한다. 규산염 이음매의 0.21 % 보다 열 배 넓으므로, 지어낸 수가 아니라 **잰**
# 수로 두고 test_interior.py 가 다시 잰다. 37.4 GPa 자체도 우리 수가 아니다 — Zeng &
# Sasselov 2013 §III.3.2 가 "the intersection between FFH2004's EOS and FMNR2009's EOS" 로
# 정한 값이고, 같은 두 출처의 앞 세대에 같은 구성을 쓴 것이다.
#
# ── 열 항, 그리고 그 한계 ────────────────────────────────────────────────
#
# 두 상의 αK_T 와 c_V 를 같은 표현에서, 각 상의 기준 상태에서 읽었다. 기준 등온은 둘 다
# 300 K 다 — 얼음 VII 의 BME 가 Hemley+ 1987 의 상온 자료이고 이 Vinet 도 300 K 등온선에
# 맞췄으므로, 두 칸에 규칙 하나다.
#
# **이 재료에서 Anderson-Goto 근사가 다른 재료보다 거칠다. 재서 적어둔다.** 이 파일의 열
# 항 전체가 αK_T 가 부피에 무관하다는 것에 기대는데, 이 표현을 훑으면 αK_T 가 300 K 에서
# 1800 K 사이에 어느 압력에서든 **두 배쯤 오른다** (37.4 GPa 에서 4.34 → 9.39 MPa/K).
# 그래서 열 항을 표현과 대보면 100 GPa 위에서는 300~1800 K 전 구간에 0.7 % 안이고,
# 37.4 GPa 에서 600 K 에 2.0 %, 1800 K 에 7.7 % 까지 벌어진다. 그 모서리는 애초에 얼음이
# 아니지만(37.4 GPa 에서 얼음 VII 은 870 K 근처에서 녹는다) 이 레시피가 그걸 스스로
# 증명하지 못하므로 수를 지우지 않고 적는다.
#
# **그리고 매듭 구간이 사각형인데 상 영역은 사각형이 아니다.** 2.216 GPa · 1500 K 에서
# 이 표현은 c_V = 1.5×10⁸ J/kg/K 를, 10 GPa · 1800 K 에서 −7.3×10⁵ 를 돌려준다. 둘 다
# 녹는곡선 한참 위라 얼음 VII 이 존재하지 않는 자리이고, 스플라인이 외삽해서 헛것을 내는
# 것이다. 아래 온도 천장은 그걸 막아주지 않는다 — 낮은 압력에서 실제로 막는 것은
# ice_column_state 가 그 구간에서 이미 undecided 를 내는 것이다.
ICE_VII_X_REF_T = 300.0            # K. 두 칸이 공유하는 기준 등온
ICE_VII_ALPHA_K = 5.921738e6       # Pa/K. SeaFreeze VII_X_French 를 2.216 GPa, 300 K 에서
ICE_VII_CV = 2476.728978           # J/kg/K. 같은 상태
ICE_X_ALPHA_K = 4.337479e6         # Pa/K. 같은 표현을 37.4 GPa, 300 K 에서
ICE_X_CV = 1226.296689             # J/kg/K. 같은 상태
# Vinet 적합 상수. 37.4 GPa ~ 1 TPa 의 300 K 등온선에 상대압력 잔차 최소제곱.
ICE_X_RHO0 = 1644.294888           # kg/m³
ICE_X_K0 = 22.286772 * GPA         # Pa
ICE_X_K0P = 6.750653
ICE_VII_TO_X = 37.4 * GPA          # Zeng & Sasselov 2013 §III.3.2 — 두 EOS 의 교점
# ── ice_x 의 천장은 셋이고 전부 다른 수다 (브리프 34 표기; 수와 출처는 interior-core.md C6
# 행과 superionic-ceiling-context-notes.md 가 정본, 여기서는 가리키기만 한다) ──
#   데이터   ≈355 GPa — French & Redmer 2015 자신의 최고 시뮬레이션 밀도(4.25 g/cc, 300 K); 위는 외삽
#   안정성   ≈520 GPa — French+ 2016 Fig. 4 에서 얼음 영역이 닫히는 곳. 그 경계의 얼음 쪽
#            퍼텐셜이 ref.[30] = French & Redmer 2015 = VII_X_French = **ice_x 가 적합된 그것** —
#            경쟁 출처가 아니라 우리 퍼텐셜의 저자들이 자기 얼음이 서는 곳을 계산한 것
#   인쇄     1000 GPa — SeaFreeze v1.1.0 매듭 상한. **코드가 드는 값은 셋 중 제일 큰 이것이다.**
# 좁히는 것은 브리프 34 범위 밖의 별도 결정이다 (C5: 소비자 시험이 먼저).
ICE_X_P_MAX = 1000.0 * GPA         # SeaFreeze v1.1.0 의 VII_X_French 매듭 상한 (인쇄 천장)
# 온도 천장. **매듭 구간의 상한이지 상 경계가 아니다.** 1800 K 위에 초이온상이 놓인다는
# 옛 근거 문장은 귀속이 틀려 있었다(브리프 34): "exceeding 100 GPa … above 2,000 K" 는
# Millot+ 2019 (2019Natur.569..251M) 초록이 **자기 refs 6–12 의 예측을 소개**한 문장이지
# 그 논문의 결과가 아니고, 그 논문의 100–400 GPa × 2000–3000 K 는 실험창이지 경계가 아니다.
# 실제 발표 경계(French+ 2016 Fig. 4, 전사 불가 — 그림 선으로만 존재)는 평평하지 않다:
# ~200 GPa 에서 ~2130 K 로 정점을 찍고 내려와 **305–375 GPa 어디에서 1800 K 아래를 지난다**
# (두 판독의 29 GPa 차는 비판정, superionic-ceiling-context-notes.md). 그리고 실측(브리프 34
# 항목 A): **천왕성의 시험 회랑은 그 구역을 실제로 관통한다** — ice_x 평가 1,854회,
# 355→535 GPa · 1643→1800 K 를 단열선 모양으로 연속 보행. 그래도 답은 서는데, 그 근거는
# 주장이 아니라 측정이다(항목 A2): 구역 값 ±5 % 교란 1,754회도, 첫-접촉 거절도 앵커를
# **비트까지** 재현했다 — 수렴한 해는 그 구역의 값에도 통과에도 무관하다. 게이트가 이제
# 검사하는 것이 바로 그 무관함이다 (test_ice_giant 의 교란-불변 회귀, 브리프 34).
# **범위 제한**: 이 무관함은 현 로스터의 천왕성에 대한 실측이지 일반 보증이 아니다 — 어떤
# 천체의 **수렴한** 기둥이 이 구역에 들어가면 다시 열린다 (C6 이 상시 감시로 남는 이유).
# ICE_X_P_MAX 좁힘은 여전히 별도 결정이고, A2 는 그 이유를 오히려 약화시켰다 — 유일한
# 소비자가 시험 회랑이고 그 회랑은 답에 기여하지 않는다.
ICE_VII_X_T_MAX = 1800.0           # K

# ── antigorite — 사문석화된 암석의 가벼운 끝 ───────────────────────────────
#
# Hilairet, Daniel & Reynard 2006 (2006GeoRL..33.2302H, 오픈 액세스, PDF 가 캐시에 있다) 가 천연
# antigorite (Cu12, 쿠바 Escambray) 를 다이아몬드 앤빌 셀에서 10 GPa 까지 방사광 XRD 로 압축했다 —
# "No amorphization, phase transition or hysteresis were detected during compression or
# decompression". 그들이 채택한 적합은 **2차 Birch-Murnaghan** 이고 F–f 도표로 확인했다 (§3 [13]):
#
#     V₀ = 2926.23(50) Å³,  K₀ = 67.27(123) GPa,  K₀′ = 4 (고정)
#
# 3차 적합(V₀ 2926.65, K₀ 62.03, K₀′ 6.39)은 비교용으로만 싣는다. **논문은 ρ₀ 를 인쇄하지 않는다.**
# 대신 그것을 내는 둘을 인쇄한다 — 구조식 (Mg₂.₆₂Fe₀.₁₆Al₀.₁₅)(Si₁.₉₆Al₀.₀₄)O₅(OH)₃.₅₇ (§2 [6]) 과
# "The V₀ value corresponding to m = 1 for antigorite is 172 Å³" (§4 [15]). 구조식 한 단위의 질량은
# 273.50 u (Mg 63.68 + Fe 8.93 + Al 5.13 + Si 55.05 + O 80.00 + OH 60.71), 그것을 172 Å³ 에 놓으면
#
#     ρ₀ = 273.50 u / 172 Å³ = 2640.5 kg/m³            (도출값 — 아래 test_interior 가 다시 낸다)
#
# 검산 둘. 2926.23 / 172 = 17.013 로 정수이고, 논문이 회절선 지수화에 쓴 구조가 Capitani & Mellini
# 2004 의 **m = 17 폴리솜** 이다 (2004AmMin..89..147C). 그리고 논문의 유일한 인쇄 밀도 — "at 5.7 GPa
# and 470°C, antigorite density calculated with our new bulk modulus is 2765 kg·m⁻³" — 를 이 곡선은
# 상온에서 2839 로 낸다: 2.7 % 차이는 450 K 열팽창의 크기와 부호다.
#
# **열항은 빌린 것이다 — Hilairet 이 빌린 그 출처에서.** Hilairet+ 2006 은 상온만 재고, 필요한 자리에서
# "thermal expansivity of Holland and Powell [1998]" 을 쓴다고 §4 에 적는다. Holland & Powell 1998
# (1998JMetG..16..309H, PDF 가 캐시에 있다) Table 5 의 antigorite (atg, Mg₄₈Si₃₄O₈₅(OH)₆₂) 행:
#
#     a° = 4.70 × 10⁻⁵ K⁻¹ (열팽창 인자),  κ₂₉₈ = 525 kbar,  C_p = a + bT + cT⁻² + dT⁻½ 에
#     a 9.6210 kJ/K · b −9.1183×10⁻⁵ kJ/K² · c −35941.6 kJ·K · d −83.0342 kJ·K^½,  V 175.480 J/bar
#
# 그들의 열팽창은 온도에 의존한다 — V(1,T) = V°[1 + a°(T−298) − 20a°(√T − √298)], 곧
# α(T) = a°(1 − 10/√T): 298 K 에서 1.98×10⁻⁵, 600 K 에서 2.78×10⁻⁵, 1000 K 에서 3.21×10⁻⁵ K⁻¹.
# 이 파일의 열항은 αK_T 상수(Anderson & Goto)라 **298 K 에서 평탄화** 한다 — α(298) 에 Hilairet 의
# K₀ 를 곱해 αK_T = 1.33 MPa/K. 600 K 에서는 그 40 % 를 놓치는 평탄화이고, 그것이 이 열항의 폭이다
# (그들의 κ(T) = κ₂₉₈(1 − 1.5×10⁻⁴(T−298)) 도 이 형태에는 자리가 없어 들지 않는다).
# c_V 는 Table 5 의 C_p 를 298 K 에서 평가해(4381 J/K/mol) 몰질량 4535.9 g/mol 로 나눈 966 J/kg/K
# 이고, 고체라 c_P ≈ c_V 로 둔다. **조성이 다르다** — Holland & Powell 은 순수 Mg 단성분(ρ 2585),
# Hilairet 의 시료는 Fe·Al 을 든 천연 antigorite(ρ₀ 2640). 열항을 순수 단성분에서 빌려 천연 시료의
# 압축 곡선에 얹은 것이고, 그래서 등급은 여전히 analog 다: 결핍이 아니라 **빌린 항의 평탄화와 조성
# 차이** 가 정한다 (2026-08-30, F2).
#
# **C7 이 막은 혼합이 아니다.** C7 은 물을 규산염에 섞는 것(반응)을 막았다. 이것은 antigorite 와
# enstatite/PREM 이라는 **두 고체가 알갱이로 공존** 하는 것 — 부분 사문석화된 암석의 실제 모습 — 이고,
# 그 사이의 부피 가법은 이 파일의 암석–금속 규칙과 같은 모양이다. 축은 하나, "얼마나 사문석화됐는가".
ANTIGORITE_RHO0 = 2640.5           # kg/m³. 위 도출
ANTIGORITE_K0 = 67.27 * GPA        # Pa. Hilairet+ 2006 BM2
ANTIGORITE_P_MAX = 10.0 * GPA      # Pa. 실험 상한 — 가역, 무이력, 같은 공간군
ANTIGORITE_REF = ("Hilairet, Daniel & Reynard 2006 (2006GeoRL..33.2302H) §3 [13] — 2차 BM 적합, "
                  "V₀ 2926.23 Å³ · K₀ 67.27 GPa · K₀′ 4; ρ₀ 는 §2 [6] 구조식과 §4 [15] 의 m = 1 부피 "
                  "172 Å³ 에서 도출. 열항은 Holland & Powell 1998 (1998JMetG..16..309H) Table 5 의 "
                  "atg 행에서 — a° 4.70×10⁻⁵ K⁻¹ 을 298 K 에서 평탄화, C_p(298)")
HP98_ATG_A0 = 4.70e-5              # K⁻¹. Holland & Powell 1998 Table 5, atg, a° (열 ×10⁻⁵ 이 표의 규약)
HP98_ATG_ALPHA_298 = HP98_ATG_A0 * (1.0 - 10.0 / 298.15 ** 0.5)   # 1.978e-5 K⁻¹, α(T) = a°(1 − 10/√T)
HP98_ATG_CP_298 = 4380.7 / 4.5359  # J/kg/K. Table 5 C_p 다항식을 298.15 K 에서, Mg₄₈Si₃₄O₈₅(OH)₆₂ 4535.9 g/mol
ANTIGORITE_ALPHA_K = HP98_ATG_ALPHA_298 * ANTIGORITE_K0   # 1.331 MPa/K
ANTIGORITE = Material(
    "antigorite", "antigorite (사문석)",
    (Phase("antigorite", "bm2", ANTIGORITE_RHO0, ANTIGORITE_K0, 4.0, ANTIGORITE_P_MAX,
           ANTIGORITE_REF,
           # melt 가 비어 있는 것은 **판정이지 미채움 구멍이 아니다** (브리프 36):
           # 사문석의 고온 운명은 일치 융해가 아니라 탈수·분해라서, 규산염 녹는곡선
           # 여섯 후보 어느 것도 이 상에 적용되지 않는다. 탈수 경계 곡선은 별도
           # 근거가 필요한 다른 물건이고 여기서 찾지 않았다.
           alpha_k=ANTIGORITE_ALPHA_K, c_v_ref=HP98_ATG_CP_298, t_ref=298.15),),
    over_reason=("사문석화된 암석층의 바닥이 {p_gpa:.1f} GPa 로 antigorite 실험 상한({max_gpa:.0f} GPa) "
                 "위다. Hilairet+ 2006 이 압축한 것이 거기까지이고, 그 위의 사문석은 탈수 반응의 "
                 "영역이라 같은 상이 아니다."))

H2O = Material(
    "h2o", "물얼음",
    (Phase("ice_ih", "bm2", ICE_IH_RHO0, ICE_IH_KT, 4.0, ICE_IH_TO_III,
           "IAPWS-06 / Feistel & Wagner 2006 Table 6 검증값",
           alpha_k=ICE_IH_ALPHA_K, c_v_ref=ICE_IH_CV, t_ref=273.152519,
           melt="water", melt_ref=IAPWS_MELT_REF + " 식 (1)"),
     Phase("ice_iii", "bme3", 1126.384048, 7.834907 * GPA, 6.709734, ICE_III_TO_V,
           "SeaFreeze v1.1.0 / Journaux+ 2020 (2020JGRE..12506176J) — "
           "얼음 III 을 P=0, T=251.15 K 에서 평가한 ρ·K_T·K′",
           p_min=ICE_IH_TO_III,
           alpha_k=ICE_III_ALPHA_K, c_v_ref=ICE_III_CV, t_ref=ICE_III_REF_T,
           melt="water", melt_ref=IAPWS_MELT_REF + " 식 (2)"),
     Phase("ice_v", "bme3", 1207.841865, 10.636814 * GPA, 6.745951, ICE_V_TO_VI,
           "SeaFreeze v1.1.0 / Journaux+ 2020 (2020JGRE..12506176J) — "
           "얼음 V 를 P=0, T=256.43 K 에서 평가한 ρ·K_T·K′",
           p_min=ICE_III_TO_V,
           alpha_k=ICE_V_ALPHA_K, c_v_ref=ICE_V_CV, t_ref=ICE_V_REF_T,
           melt="water", melt_ref=IAPWS_MELT_REF + " 식 (3)"),
     Phase("ice_vi", "bme3", 1263.385752, 10.368592 * GPA, 7.821860, ICE_VI_TO_VII,
           "SeaFreeze v1.1.0 / Journaux+ 2020 (2020JGRE..12506176J) — "
           "얼음 VI 를 P=0, T=272.73 K 에서 평가한 ρ·K_T·K′",
           p_min=ICE_V_TO_VI,
           alpha_k=ICE_VI_ALPHA_K, c_v_ref=ICE_VI_CV, t_ref=ICE_VI_REF_T,
           melt="water", melt_ref=IAPWS_MELT_REF + " 식 (4)"),
     Phase("ice_vii", "bme3", 1460.0, 23.7 * GPA, 4.15, ICE_VII_TO_X,
           "Seager+ 2007 Table 1 (arXiv:0707.2895) — H₂O ice VII BME, Hemley+ 1987. "
           "열 상수는 SeaFreeze v1.1.0 의 VII_X_French (French & Redmer 2015, "
           "2015PhRvB..91a4308F) 를 2.216 GPa · 300 K 에서 평가한 값이다",
           p_min=ICE_VI_TO_VII, melt="water",
           melt_ref=IAPWS_MELT_REF + " 식 (5) — 355–715 K (2.216–20.6 GPa); 그 위는 "
                    + REINHARDT_MELT_REF,
           alpha_k=ICE_VII_ALPHA_K, c_v_ref=ICE_VII_CV, t_ref=ICE_VII_X_REF_T,
           t_max=ICE_VII_X_T_MAX),
     Phase("ice_x", "vinet", ICE_X_RHO0, ICE_X_K0, ICE_X_K0P, ICE_X_P_MAX,
           "SeaFreeze v1.1.0 의 VII_X_French (French & Redmer 2015, "
           "2015PhRvB..91a4308F) 300 K 등온선에 맞춘 Vinet 적합. 37.4 GPa–1 TPa 에서 "
           "최악 1.475 % — 이 사다리에서 제일 넓은 오차폭이고, 읽은 게 아니라 적합한 "
           "유일한 얼음 상이다",
           p_min=ICE_VII_TO_X,
           alpha_k=ICE_X_ALPHA_K, c_v_ref=ICE_X_CV, t_ref=ICE_VII_X_REF_T,
           t_max=ICE_VII_X_T_MAX,
           # 녹는곡선이 52.4 GPa 까지 온다 (Reinhardt+ 2022). 그 위는 water_t_melt 가 None 을
           # 돌려주고 소비처가 undecided 로 적는다 — 곡선이 어디서 끝나는지를 판정문이 수로 말한다.
           melt="water", melt_ref=REINHARDT_MELT_REF),),
    over_reason=("얼음 기둥 바닥이 {p_gpa:.0f} GPa 로 근거 구간의 상한"
                 "({max_gpa:.0f} GPa) 위다. 그 상한은 SeaFreeze v1.1.0 이 싣는 "
                 "French & Redmer 2015 표현의 매듭 구간이 끝나는 자리다. 그 위에 "
                 "물리가 없는 것이 아니라 **읽을 형태가 없다** — Zeng & Sasselov 2013 이 "
                 "French+ 2009 의 표를 8.893 TPa 까지 끌고 간 뒤에야 전자축퇴로 넘어가므로 "
                 "(Salpeter & Zapolsky 1967), 여기와 축퇴 사이에 아홉 배쯤의 여백이 "
                 "발표돼 있다. 물이 아주 많은 큰 천체는 여기서 멈춘다."),
    t_over_reason=("얼음 기둥의 온도 {t_k:.0f} K 가 '{phase}' 적합의 상한"
                   "({t_max:.0f} K) 위다. 그 위는 초이온상이다 — 산소는 격자에 남고 "
                   "수소만 액체처럼 돌아다니는 상태이고, Millot+ 2019 "
                   "(2019Natur.569..251M) 이 100 GPa 위 · 2000 K 위로 적는다. 이 천장은 "
                   "그 아래에 서 있어서 초이온상을 얼음 X 라고 부르지 않는다. "
                   "그 상의 상태방정식은 French & Redmer 2016 (2016PhRvE..93b2140F) 이 "
                   "두 초이온상의 열역학 퍼텐셜로 구성해 두었고, 이 레시피에 그것이 없다."),
    # 2026-08-25 에 III·V·VI 이 들어와 Ih 부터 VII 까지 사다리가 이어졌다. 그래서 이
    # 설명은 더 이상 도달하지 않는다 — 도달하면 전이압 상수 하나가 이웃과 어긋나게
    # 편집된 것이다. 침묵하는 대신 그렇게 말한다. test_interior.py 가 사다리의 연속성을
    # 따로 확인한다.
    gap_reason=("{p_gpa:.4f} GPa 가 물얼음 상 사다리의 두 상 **사이** 에 떨어졌다. "
                "Ih(~209.5 MPa) · III(~355.0) · V(~618.4) · VI(~2.216 GPa) · VII 은 "
                "이어져 있어야 하므로, 이건 물리가 아니라 전이압 상수가 이웃과 어긋나게 "
                "편집됐다는 뜻이다."),
)
# ── 수소-헬륨 ───────────────────────────────────────────────────────────
#
# 거대행성 외피는 응축상이 아니다. 그래서 여기 있는 다른 재료의 Birch-Murnaghan 이나
# Vinet 은 쓸 수 없고, 대신 **폴리트로프** 를 쓴다. P = K ρ^(1+1/n) 이고 n = 1 이다.
#
# n = 1 이 "인위적이지만 놀랄 만큼 쓸 만한" 근사라는 것과 그 계수를 Helled, Movshovitz &
# Nettelmann 2022 §2 (arXiv:2202.10046) 가 적는다 — "a surprisingly reasonable
# approximation of the compressibility of a hydrogen-helium mixture at conditions typical
# of giant planet envelopes". 같은 절이 비회전 구형 해를 닫힌 형태로 준다.
#
#     ρ(r) = ρ_c · sin(kr)/(kr),   k = √(2πG/K),   R = √(πK/2G)
#
# **K 를 옮겨 적을 때 함정이 하나 있었고, 논문 자신의 숫자로 걸러냈다.** 그 논문은
# K = 2.1×10¹² 라고 쓰면서 단위를 m⁵ kg⁻¹ s⁻² 로 달아 놓았다. 그런데 같은 문단이 그
# K 에서 R = 70,300 km 가 나온다고 적는다. SI 로 2.1e12 를 넣으면 R 이 1.5 AU 가 되고,
# 2.1e5 를 넣으면 70,302 km 가 된다. 즉 적힌 수는 cgs (cm⁵ g⁻¹ s⁻²) 이고 SI 로는
# 2.1×10⁵ 다. 손으로 친 표에서 54배가 어긋났던 전례가 있는 리포지토리라, 이 검산을
# test_giant.py 가 다시 돌린다.
POLYTROPE_K_HHE = 2.1e5      # m⁵ kg⁻¹ s⁻². Helled+ 2022 §2 의 2.1×10¹² cgs
POLYTROPE_N_HHE = 1.0        # 지수. 같은 절
#
# **압력 상한은 문헌이 말해 주지 않는다.** 그 논문은 압력 한계를 적지 않고, 근사가
# 깨지는 방식이 압력 절단이 아니라 조성과 열이기 때문이다 (같은 절이 그 근사가 목성보다
# 토성에 덜 맞는 이유로 P∝ρ² 가 토성 외피에 덜 맞는 것과 토성이 중원소가 더 많은 것
# 둘을 든다). 그래서 여기 두는 상한은 **선언된 범위의 두 번째 울타리** 다 — 이 관계식이
# 13 M_J 에서 도달하는 중심압으로 잡았고, 13 M_J 는 중수소 연소로 갈리는 관례적
# 행성/갈색왜성 경계다 (Spiegel, Burrows & Milsom 2011, arXiv:1008.5150 이 "13 M_J is
# generally a reasonable rule of thumb" 라고 적으면서 그 값이 헬륨량·중수소량·금속량에
# 달렸다고 덧붙인다). 그 위는 body_class 가 이미 이름 대며 거절하므로, 이 상한이
# 하중을 받는 자리는 아니다.
JUPITER_MASS_EARTH = 317.828     # M⊕. 목성 질량, IAU/IAG 보고 (Archinal+ 2011)
DEUTERIUM_LIMIT_MJ = 13.0        # M_J. Spiegel+ 2011 의 rule of thumb
G_NEWTON = 6.67430e-11           # m³ kg⁻¹ s⁻². interior.py 의 G 와 같은 값
EARTH_MASS_KG_EOS = 5.972e24     # kg. 위 상한을 계산하는 데만 쓴다


def polytrope_radius_n1(k: float) -> float:
    """n = 1 폴리트로프의 반지름 R = √(πK/2G). 질량과 무관하다 (Helled+ 2022 §2)."""
    return math.sqrt(math.pi * k / (2.0 * G_NEWTON))


def polytrope_central_pressure_n1(k: float, mass_kg: float) -> float:
    """n = 1 해의 중심압. ρ_c = πM/(4R³) 이고 P_c = K ρ_c² 다."""
    r = polytrope_radius_n1(k)
    rho_c = math.pi * mass_kg / (4.0 * r ** 3)
    return k * rho_c ** 2


# 폴리트로프는 2026-08-28 에 **밀도를 내는 자리에서 물러났다.** 상수 하나가 목성에
# 맞춰져 있어서 목성에서만 맞고(+0.6 %) 외피가 일부뿐인 천체에서 세 배 부풀었다 —
# 토성 +20.7 %, 천왕성 +23.8 %, 해왕성 +29.2 %. 남은 쓰임은 하나다: 사격의 괄호를
# 잡을 때 쓰는 **밀도 척도**. 질량과 무관한 닫힌 해가 있어서 그 자리에 값싸고, 계산
# 결과에는 들어가지 않는다 (Material.rho_seed 의 주석과 같은 규율).


class HydrogenHelium:
    """수소-헬륨 외피. `Material` 과 같은 자리에 꽂히지만 상의 열이 아니다.

    상태방정식은 hhe_table.py 에 있다 — Chabrier, Mazevet & Soubiran 2019 (ApJ 872, 51,
    arXiv:1902.01852) 가 배포한 표를 행성 창에서 굳힌 것이고, 출처·유효 영역·보간 오차가
    그 파일 머리에 있다. 여기 있는 것은 그것을 적분기가 먹을 수 있는 모양으로 감싸는
    껍질이다. water_hot.py 를 감싼 HotWater 와 같은 이유·같은 모양이다.

    **이 재료에는 P = 0 인 표면이 없다.** 기체라서 밀도가 압력과 함께 0 으로 가고,
    발표된 거대행성 반지름은 전부 특정 압력 준위(1 bar)의 값이다. 그래서 `p_floor` 를
    들고 있고, 적분기가 거기서 멈춘다."""
    name: str = "h_he"
    label_ko: str = "수소-헬륨 외피"

    @property
    def rho0(self) -> float:
        """영압 밀도. 기체이므로 0 이다 — 폴리트로프도 같은 값을 냈다."""
        return 0.0

    @property
    def p_max(self) -> float:
        """굳힌 창의 위쪽 끝. 표 자체는 10¹³ GPa 까지 가지만 행성 창만 굳혔다."""
        return 10.0 ** (hhe_table.LOGP_LO + (hhe_table.NP - 1) * hhe_table.STEP) * 1e9

    @property
    def p_floor(self) -> float:
        """굳힌 창의 아래쪽 끝 = 1 bar. 기체 외피의 적분이 여기서 멈춘다."""
        return hhe_table.P_FLOOR_PA

    def rho_seed(self, mass_kg: float) -> float:
        """괄호잡기용 밀도 척도. **n = 1 폴리트로프가 남아서 하는 일이 이것뿐이다.**
        질량과 무관한 닫힌 해라 값싸고, 계산 결과에는 들어가지 않는다."""
        r = polytrope_radius_n1(POLYTROPE_K_HHE)
        return 3.0 * mass_kg / (4.0 * math.pi * r ** 3)

    @property
    def has_thermal(self) -> bool:
        return True

    def cold_phases(self) -> tuple[str, ...]:
        """**비었다.** 2026-08-28 까지 여기에 hhe_n1 이 있었고, 그 한 줄 때문에 온도가
        외피를 안 흘러 포텐셜 온도가 표면이 아니라 얼음 맨틀 꼭대기에 떨어졌다."""
        return ()

    def melt_free_phases(self) -> tuple[str, ...]:
        """녹는곡선이 없다 — 있을 자리가 아니다. 이 재료는 유체다."""
        return (self.name,)

    def t_melt(self, p: float) -> float | None:
        return None

    def in_domain(self, p: float, t: float) -> bool:
        return hhe_table.in_domain(p, t)

    def check_temperature(self, p: float, t: float) -> None:
        if t <= 0.0:
            raise PhaseGap(
                self.name, p,
                "수소-헬륨 외피는 등온 경로로 풀 수 없다. 이 상태방정식은 표가 통째로 "
                "(P, T) 의 함수라 온도가 인자이고, 폴리트로프처럼 압력 하나로 닫히지 "
                "않는다. 포텐셜 온도를 선언하면 이 층이 풀린다.")
        # **압력으로 막힌 것을 온도로 막혔다고 말하면 안 된다.** 사격의 괄호는 둘을
        # 다르게 다룬다 — 압력이면 시험압을 좁히고, 온도면 시험 온도를 옮긴다. 굳힌 창의
        # 압력 밖은 온도와 무관하므로 temperature_k 를 채우지 않는다.
        if p < self.p_floor or p > self.p_max:
            raise PhaseGap(
                self.name, p,
                f"{p / 1e9:.4g} GPa 는 굳힌 창의 압력 구간"
                f"({self.p_floor / 1e9:.4g}–{self.p_max / 1e9:.4g} GPa) 밖이다. "
                "아래쪽 끝은 1 bar 이고 발표된 거대행성 반지름이 재어진 준위다 — "
                "기체에는 P = 0 인 표면이 없다.")
        if hhe_table.in_domain(p, t):
            return
        lt_max = 10.0 ** (hhe_table.LOGT_LO + (hhe_table.NT - 1) * hhe_table.STEP)
        if t > lt_max:
            raise PhaseGap(
                self.name, p,
                f"{t:.0f} K 는 굳힌 창의 상한({lt_max:.0f} K) 위다. Chabrier+ 2019 의 "
                "표는 10⁸ K 까지 가지만 이 리포지토리는 행성 구간만 굳혔다 — 그 위는 "
                "갈색왜성과 별이고, body_class 가 이미 이름 대며 거절한다.", t)
        raise PhaseGap(
            self.name, p,
            f"{p / 1e9:.4g} GPa 에서 {t:.0f} K 는 대류하는 외피가 닿는 것보다 차다. "
            "이 창의 아래 경계는 1 bar · 50 K 에서 출발한 단열선 아래에 그은 선이고 "
            "(천왕성의 1 bar 온도가 76 K 다), 그 아래에는 배포 표 자신이 예고한 결함이 "
            "몰려 있다 — 밀도 자리의 sentinel 과 0.1/0.5 로 눌린 grad_ad. 발표된 수를 "
            "손보는 대신 영역을 말한다.", t, too_cold=True)

    def density(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        self.check_temperature(p, t)
        return hhe_table.density(p, t)

    def gruneisen(self, p: float, rho: float, t: float, t_pot: float = 0.0) -> float:
        if t <= 0.0:
            return 0.0
        return hhe_table.gruneisen(p, t)

    def c_p(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        """정압비열 [J/kg/K]. 표의 엔트로피 열에서 온다 — 조립한 값이 아니다."""
        return 0.0 if t <= 0.0 else hhe_table.heat_capacity_p(p, t)

    def grad_ad(self, p: float, t: float = 0.0, t_pot: float = 0.0) -> float:
        return 0.0 if t <= 0.0 else hhe_table.grad_ad(p, t)

    def dtdp_adiabat(self, p: float, t: float, t_pot: float = 0.0) -> float:
        """단열 기울기 dT/dP = ∇_ad · T / P [K/Pa].

        **표가 ∇_ad 를 들고 있으므로 다시 만들지 않는다.** 다른 재료에서는 이 기울기를
        γ 와 K_S 로 조립하는데, 그건 Birch-Murnaghan 상이 내줄 수 있는 것이 그것뿐이라
        그렇다. 여기서는 저자들이 자기 엔트로피에서 계산한 값이 그대로 있다."""
        if t <= 0.0 or p <= 0.0:
            return 0.0
        return hhe_table.grad_ad(p, t) * t / p

    def phase_at(self, p: float, t: float = 0.0):
        return _HydrogenHeliumSlope(p)


@dataclass(frozen=True)
class _HydrogenHeliumSlope:
    """혼합 안에 들어갔을 때 `_adiabatic_dtdp` 가 묻는 (∂P/∂T)_V."""
    p: float
    name: str = "h_he"
    t_max: float = 0.0

    def dpdt_v(self, t: float, t_pot: float = 0.0) -> float:
        return 0.0 if t <= 0.0 else hhe_table.dpdt_v(self.p, t)


H_HE = HydrogenHelium()

MATERIALS: dict[str, Material | HotWater | HydrogenHelium | LiquidWater | DenseLiquidWater | Ammonia] = {
    m.name: m for m in (FE_PREM, FE_EPS, SILICATE, SILICATE_CHONDRITIC, ANTIGORITE, H2O, H_HE, H2O_HOT, H2O_LIQUID,
                        H2O_LIQUID_DENSE, NH3)
}
