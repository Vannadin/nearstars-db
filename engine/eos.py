# 층 재료의 상태방정식 ρ(P) — 상수 하나하나가 어느 논문 어느 표에서 왔는지 붙여둔다
"""Cold equations of state for the materials a solid body is built from.

    from eos import MATERIALS
    MATERIALS["fe_prem"].density(136e9)      → 9.9e3 kg/m³ 근처 (지구 핵-맨틀 경계)

내부 구조를 적분하려면 압력에서 밀도를 돌려주는 함수가 있어야 한다. 층 밀도를
상수로 두면 자기압축이 통째로 빠지고, 그게 균질 2층 모형이 지구에서 C/MR² 를
4.8 % 크게 냈던 이유다.

**여기 있는 숫자는 전부 발표된 적합값이고, 상수마다 출처를 옆에 적었다.** 손으로
친 표에서 54배가 어긋났던 전례가 있어서, 출처 없는 상수는 이 파일에 못 들어온다.

세 가지 함수형을 쓴다. 어느 것을 쓸지는 그 재료를 적합한 논문이 정한 것이지 우리가
고른 게 아니다.

* **BM2** — 2차 Birch-Murnaghan. K₀′ 를 4 로 고정한 형태다.
  P = (3/2) K₀ [(ρ/ρ₀)^(7/3) − (ρ/ρ₀)^(5/3)]
  Zeng+ 2016 이 PREM 을 이 형태로 적합했다 (arXiv:1512.08827 eq. 1).
* **BME3** — 3차 Birch-Murnaghan. K₀′ 가 자유롭다. Seager+ 2007 Table 1 의 기본형.
* **Vinet** — 고압 외삽에 BME 보다 낫다고 Seager+ 2007 §III.1 이 적는다. Fe(ε) 에 쓴다.

각 재료는 **상(phase) 의 열** 이다. 상마다 유효 압력 구간이 있고, 구간 사이에 근거가
없는 틈이 있으면 그 틈을 이름 붙여 들고 있는다 — 얼음의 209.5 MPa ~ 2.216 GPa 가
그렇다. 솔버가 거기에 발을 디디면 조용히 외삽하는 게 아니라 그 사실을 돌려준다.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


class PhaseGap(Exception):
    """근거 있는 상 사이의 빈 구간에 압력이 떨어졌다. 외삽 대신 이걸 던진다."""

    def __init__(self, material: str, pressure_pa: float, reason: str):
        self.material = material
        self.pressure_pa = pressure_pa
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class Phase:
    """한 상의 냉각 등온 상태방정식."""
    name: str
    form: str                 # bm2 | bme3 | vinet
    rho0: float               # kg/m³
    k0: float                 # Pa
    k0p: float                # K₀′ (bm2 는 4 로 고정이므로 무시된다)
    p_max: float              # Pa. 이 상이 유효한 상한
    ref: str                  # 어느 논문 어느 표에서 왔는가
    p_min: float = 0.0        # Pa. 앞 상에서 넘어오는 전이압

    def pressure(self, rho: float) -> float:
        """ρ 에서 P. 정방향은 닫힌 형태라 이쪽이 값싸다."""
        x = rho / self.rho0
        if self.form == "bm2":
            return 1.5 * self.k0 * (x ** (7.0 / 3.0) - x ** (5.0 / 3.0))
        if self.form == "bme3":
            return (1.5 * self.k0 * (x ** (7.0 / 3.0) - x ** (5.0 / 3.0))
                    * (1.0 + 0.75 * (self.k0p - 4.0) * (x ** (2.0 / 3.0) - 1.0)))
        if self.form == "vinet":
            e = x ** (-1.0 / 3.0)
            return (3.0 * self.k0 * x ** (2.0 / 3.0) * (1.0 - e)
                    * math.exp(1.5 * (self.k0p - 1.0) * (1.0 - e)))
        raise ValueError(f"모르는 EOS 형태 '{self.form}'")

    def density(self, p: float) -> float:
        """P 에서 ρ. 정방향은 닫힌 형태이므로 Newton 으로 뒤집는다.

        P(ρ) 는 단조증가라 뿌리가 하나뿐이다. 첫 추측은 선형 압축
        ρ ≈ ρ₀(1 + P/K₀) 이고, 이 자리가 적분 안쪽 고리라 반복 횟수가 그대로
        실행시간이다 — 이분법 200회로는 쓸 수 없이 느렸다."""
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

    @property
    def rho0(self) -> float:
        """영압 밀도. 어떤 조성이 어떤 평균밀도를 낼 수 있는지의 하한이다."""
        return self.phases[0].rho0

    @property
    def p_max(self) -> float:
        return self.phases[-1].p_max

    def phase_at(self, p: float) -> Phase:
        """이 압력에서 유효한 상. 없으면 왜 없는지를 들고 던진다."""
        for ph in self.phases:
            if p < ph.p_min:
                raise PhaseGap(self.name, p, self.gap_reason.format(p_gpa=p / 1e9))
            if p <= ph.p_max:
                return ph
        raise PhaseGap(self.name, p, self.over_reason.format(
            p_gpa=p / 1e9, max_gpa=self.p_max / 1e9))

    def density(self, p: float) -> float:
        return self.phase_at(p).density(p)


GPA = 1e9
MPA = 1e6

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
           "Zeng+ 2016 §II (arXiv:1512.08827) — PREM 외핵 BM2 적합"),),
)
FE_EPS = Material(
    "fe_eps", "순수 ε-철",
    (Phase("fe_eps", "vinet", 8300.0, 156.2 * GPA, 6.08, 2.09e4 * GPA,
           "Seager+ 2007 Table 1 (arXiv:0707.2895) — Fe(ε) Vinet, Anderson+ 2001"),),
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
SILICATE = Material(
    "silicate", "규산염 맨틀",
    (Phase("mgsio3_en", "bme3", 3220.0, 125.0 * GPA, 5.0, 23.83 * GPA,
           "Seager+ 2007 Table 1 (arXiv:0707.2895) — MgSiO₃ enstatite BME"),
     Phase("mgsio3_prem", "bm2", 3980.0, 206.0 * GPA, 4.0, 3.5e3 * GPA,
           "Zeng+ 2016 §II (arXiv:1512.08827) — PREM 하부맨틀 BM2 적합",
           p_min=23.83 * GPA)),
)

# ── 물 ──────────────────────────────────────────────────────────────────
#
# 얼음은 상이 갈린다. 저압에서는 육방정 얼음 Ih 이고, 209.5 MPa 에서 얼음 III 으로
# 넘어간다 (Choukroun & Grasset 2007 의 삼중점 209.5 MPa / 251.15 K; Zeng &
# Sasselov 2013 §III.3.1, arXiv:1301.0818 이 행성 모형에 그대로 채택). 이어서 III →
# V (355.0 MPa) → VI (618.4 MPa) → VII (2.216 GPa) 로 간다.
#
# **III · V · VI 은 여기 없다.** 그 세 상의 상태방정식 계수는 Choukroun & Grasset
# 2007/2010 과 Bezacier+ 2014 에 있는데 전문을 못 구했다. 없는 것을 있는 척하지
# 않는다 — 209.5 MPa 와 2.216 GPa 사이는 틈으로 남겨두고, 솔버가 거기에 닿으면
# 그 사실을 이름과 함께 돌려준다.
#
# Ih 의 두 상수는 IAPWS-06 (Feistel & Wagner 2006) 의 검증표에서 직접 읽었다.
# T = 273.152519 K, p = 101 325 Pa 에서 ρ = 916.721463419 kg/m³ 이고
# κ_T = 1.17785291765e-10 Pa⁻¹ 이므로 K_T = 1/κ_T = 8.490 GPa 다.
# K₀′ 는 그 표에 없어서 BM2 (K₀′ = 4 고정) 를 쓴다. Ih 이 존재하는 구간 전체에서
# 압축이 2.4 % 뿐이라 K₀′ 를 4 로 두든 6 으로 두든 밀도가 0.2 % 안에서 같다 —
# test_interior.py 가 그 감도를 실제로 재서 보여준다.
ICE_IH_RHO0 = 916.721463419        # IAPWS-06 Table 6, T=273.152519 K, p=101325 Pa
ICE_IH_KT = 1.0 / 1.17785291765e-10  # 같은 표의 κ_T 를 뒤집은 것. 8.490 GPa
ICE_IH_TO_III = 209.5 * MPA        # Choukroun & Grasset 2007 삼중점
ICE_VI_TO_VII = 2.216 * GPA        # Daucik & Dooley 2011 (Zeng & Sasselov 2013 §III.3.1 경유)

H2O = Material(
    "h2o", "물얼음",
    (Phase("ice_ih", "bm2", ICE_IH_RHO0, ICE_IH_KT, 4.0, ICE_IH_TO_III,
           "IAPWS-06 / Feistel & Wagner 2006 Table 6 검증값"),
     Phase("ice_vii", "bme3", 1460.0, 23.7 * GPA, 4.15, 37.4 * GPA,
           "Seager+ 2007 Table 1 (arXiv:0707.2895) — H₂O ice VII BME, Hemley+ 1987",
           p_min=ICE_VI_TO_VII)),
    over_reason=("얼음 기둥 바닥이 {p_gpa:.1f} GPa 로 근거 구간의 상한"
                 "({max_gpa:.1f} GPa) 위다. 그 위는 얼음 X 와 초이온상이고 "
                 "(Goncharov+ 2005 의 47 GPa 전이, French+ 2009), 이 레시피에는 그 "
                 "상태방정식이 없다. 물이 많은 큰 천체는 여기서 멈춘다."),
    gap_reason=("얼음 기둥 바닥이 {p_gpa:.3f} GPa 다. 209.5 MPa 에서 얼음 Ih 이 "
                "얼음 III 으로 넘어가고 2.216 GPa 까지 III·V·VI 이 이어지는데, 이 셋의 "
                "상태방정식 계수는 이 리포지토리에 근거된 게 없다 (Choukroun & Grasset "
                "2007/2010, Bezacier+ 2014 의 전문을 못 구했다). 없는 계수를 지어내는 "
                "대신 여기서 멈춘다 — 그 세 상이 들어오면 이 천체는 풀린다."),
)
MATERIALS: dict[str, Material] = {
    m.name: m for m in (FE_PREM, FE_EPS, SILICATE, H2O)
}
