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
* **Polytrope** — P = K ρ^(1+1/n). 응축상이 아니라 수소-헬륨 외피에 쓰는 형태다.
  폴리트로프는 **별도의 가지가 아니라 상태방정식의 한 형태** 이고, 그래서 같은 적분기가
  거대행성을 그대로 푼다. n = 1 의 계수는 H_HE 주석에 있다.

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
    form: str                 # bm2 | bme3 | vinet | polytrope
    rho0: float               # kg/m³. polytrope 는 0 이다 — 영압에서 밀도가 0 이다
    k0: float                 # Pa. polytrope 는 K [m⁵ kg⁻¹ s⁻²] 를 여기 넣는다
    k0p: float                # K₀′ (bm2 는 4 로 고정이므로 무시된다). polytrope 는 지수 n
    p_max: float              # Pa. 이 상이 유효한 상한
    ref: str                  # 어느 논문 어느 표에서 왔는가
    p_min: float = 0.0        # Pa. 앞 상에서 넘어오는 전이압

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
        if self.form == "vinet":
            e = x ** (-1.0 / 3.0)
            return (3.0 * self.k0 * x ** (2.0 / 3.0) * (1.0 - e)
                    * math.exp(1.5 * (self.k0p - 1.0) * (1.0 - e)))
        raise ValueError(f"모르는 EOS 형태 '{self.form}'")

    def density(self, p: float) -> float:
        """P 에서 ρ. 정방향은 닫힌 형태이므로 Newton 으로 뒤집는다.

        P(ρ) 는 단조증가라 뿌리가 하나뿐이다. 첫 추측은 선형 압축
        ρ ≈ ρ₀(1 + P/K₀) 이고, 이 자리가 적분 안쪽 고리라 반복 횟수가 그대로
        실행시간이다 — 이분법 200회로는 쓸 수 없이 느렸다.

        폴리트로프는 뒤집기가 닫힌 형태라 반복이 아예 없다."""
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
ICE_III_REF_T = 251.15             # K. Ih→III 삼중점
ICE_V_REF_T = 256.43               # K. III→V 삼중점
ICE_VI_REF_T = 272.73              # K. V→VI 삼중점

H2O = Material(
    "h2o", "물얼음",
    (Phase("ice_ih", "bm2", ICE_IH_RHO0, ICE_IH_KT, 4.0, ICE_IH_TO_III,
           "IAPWS-06 / Feistel & Wagner 2006 Table 6 검증값"),
     Phase("ice_iii", "bme3", 1126.384048, 7.834907 * GPA, 6.709734, ICE_III_TO_V,
           "SeaFreeze v1.1.0 / Journaux+ 2020 (2020JGRE..12506176J) — "
           "얼음 III 을 P=0, T=251.15 K 에서 평가한 ρ·K_T·K′",
           p_min=ICE_IH_TO_III),
     Phase("ice_v", "bme3", 1207.841865, 10.636814 * GPA, 6.745951, ICE_V_TO_VI,
           "SeaFreeze v1.1.0 / Journaux+ 2020 (2020JGRE..12506176J) — "
           "얼음 V 를 P=0, T=256.43 K 에서 평가한 ρ·K_T·K′",
           p_min=ICE_III_TO_V),
     Phase("ice_vi", "bme3", 1263.385752, 10.368592 * GPA, 7.821860, ICE_VI_TO_VII,
           "SeaFreeze v1.1.0 / Journaux+ 2020 (2020JGRE..12506176J) — "
           "얼음 VI 를 P=0, T=272.73 K 에서 평가한 ρ·K_T·K′",
           p_min=ICE_V_TO_VI),
     Phase("ice_vii", "bme3", 1460.0, 23.7 * GPA, 4.15, 37.4 * GPA,
           "Seager+ 2007 Table 1 (arXiv:0707.2895) — H₂O ice VII BME, Hemley+ 1987",
           p_min=ICE_VI_TO_VII)),
    over_reason=("얼음 기둥 바닥이 {p_gpa:.1f} GPa 로 근거 구간의 상한"
                 "({max_gpa:.1f} GPa) 위다. 그 위는 얼음 X 와 초이온상이고 "
                 "(Goncharov+ 2005 의 47 GPa 전이, French+ 2009), 이 레시피에는 그 "
                 "상태방정식이 없다. 물이 많은 큰 천체는 여기서 멈춘다."),
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


H_HE = Material(
    "h_he", "수소-헬륨 외피",
    (Phase("hhe_n1", "polytrope", 0.0, POLYTROPE_K_HHE, POLYTROPE_N_HHE,
           polytrope_central_pressure_n1(
               POLYTROPE_K_HHE,
               DEUTERIUM_LIMIT_MJ * JUPITER_MASS_EARTH * EARTH_MASS_KG_EOS),
           "Helled+ 2022 §2 (arXiv:2202.10046) — n=1 폴리트로프, K=2.1e5 SI"),),
    over_reason=("수소-헬륨 외피가 {p_gpa:.0f} GPa 까지 내려간다. n=1 폴리트로프를 "
                 "이 리포지토리가 선언한 범위의 상한({max_gpa:.0f} GPa, 13 M_J 의 "
                 "중심압) 위로 끌고 가는 것이고, 그 위는 갈색왜성이다 — 중수소가 타고 "
                 "(Spiegel+ 2011), 이 레시피에는 그 광도 이력이 없다."),
)

MATERIALS: dict[str, Material] = {
    m.name: m for m in (FE_PREM, FE_EPS, SILICATE, H2O, H_HE)
}
