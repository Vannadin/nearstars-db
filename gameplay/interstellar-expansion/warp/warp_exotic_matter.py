# 이종물질(음에너지) 실존 가정 하의 워프 연료·에너지 소요량 프로토타입.
# 동일한 Alcubierre 음에너지 적분에서 (벽두께 Δ·유효 버블반경 R)만 바꿔 모델 비교:
#   1) 정통 Alcubierre/Pfenning-Ford  — 플랑크 박벽 → 우주질량급 (왜 불가능한가)
#   2) illustrative toy               — 미시 R_eff + 두꺼운 벽 → g~kg (※ 공개 논문값 아님, 스케일 감각용)
#   3) 게임튜닝 KSPIE식                — 메트릭 무시, ExoticMatter ∝ 선체질량 + MJ ∝ 거리
# NearStars 거리는 db/systems astrometry(parallax)에서 직접 읽음. FTL이므로 광속하한 무시.
# 이론·인용 전체는 docs/reference/warp-drive-energetics.md 참조.
#
# 음에너지 적분 근거(교과서/고전 워프 문헌, 차원해석 수준):
#   E ≈ -(c⁴/12G)·β_s²·(R²/Δ)              (Alcubierre 1994; Lobo&Visser 2004 적분형)
#   - Pfenning&Ford 1997(gr-qc/9702026): 양자부등식 → 벽 Δ ~ 플랑크길이 수백배 → "physically unattainable"
#     (우주질량 수치는 본문에만 있어 본 표의 10^65 kg은 위 스케일링식의 자체 추정값임)
#   주의: 'optimized' 컬럼의 g~kg은 R_eff를 공격적으로 줄인 illustrative toy일 뿐이며,
#         실제 공개된 감축값은 Van Den Broeck 1999(gr-qc/9905084) "수 태양질량",
#         Fell&Heisenberg 2021(2104.06488) "태양질량의 ~10^-4" — 아래 PUBLISHED 표 참조.
import json, math

# --- 물리상수 (SI) ---
G   = 6.674e-11        # m^3 kg^-1 s^-2
C   = 2.998e8          # m/s
C2  = C*C
C4_G = C**4 / G        # ≈ 1.21e44 N
M_SUN = 1.989e30       # kg
M_UNIVERSE = 1.5e53    # kg (관측가능 우주 바리온+암흑 ~규모, order-of-magnitude)
PC_AU = 206264.806; LY_PER_PC = 3.261564

def dist_ly(path):
    d = json.load(open(path)); r = d['stars'][0]['raw']
    return d.get('system_name', path), (1000.0/r['parallax_mas']) * LY_PER_PC

# --- 음에너지 적분: 모델은 (R_eff, Δ)로만 구분 ---
def neg_energy_J(beta_s, R_eff, delta):
    """|E| in Joules = (c^4/12G)·β_s²·R²/Δ."""
    return (C4_G / 12.0) * beta_s*beta_s * (R_eff*R_eff) / delta

# 모델 파라미터: 같은 물리식, (유효반경 R_eff, 벽두께 Δ)만 다름
PLANCK_L = 1.616e-35   # m
MODELS = {
    'classic':   dict(R_eff=100.0,  delta=10*PLANCK_L,  # 100m 버블, 플랑크 수백배 박벽(Pfenning-Ford)
                      note="정통 Alcubierre/Pfenning-Ford — 플랑크 박벽"),
    'toy':       dict(R_eff=1e-15,  delta=1.0,          # 공격적 R_eff(~fm) + 두꺼운 벽(~m)
                      note="illustrative toy (공개 논문값 아님)"),
}

# 실제 논문이 발표한 감축값(스케일링 toy와 별개의 권위 수치). docs/reference/warp-drive-energetics.md §4–5.
PUBLISHED = [
    ("Van Den Broeck 1999 (gr-qc/9905084)", "음에너지 ~수 태양질량 (양에너지 동급, WEC-QI 충족)"),
    ("Bobrick & Martire 2021 (2102.06824)", "Alcubierre 대비 음에너지 ~2자릿수 감소; 초광속은 여전히 에너지조건 위배"),
    ("Fell & Heisenberg 2021 (2104.06488)", "양에너지 솔리톤, 총에너지 ~태양질량의 10^-4"),
    ("Santiago/Schuster/Visser 2022 (2105.03079)", "반박: 일반 워프는 NEC/WEC/SEC/DEC 모두 위배 (초광속=음에너지 필수)"),
]

def fmt_mass(kg):
    if kg >= 1e6*M_SUN: return f"{kg/M_UNIVERSE:.1e} 우주질량"
    if kg >= 1e-3*M_SUN: return f"{kg/M_SUN:.2e} M_sun"
    if kg >= 1.0:        return f"{kg:.2e} kg"
    return f"{kg*1000:.2e} g"

STARS = ['alpha_centauri_a','barnards_star','tau_cet','luhman_16_a',
         '40_eridani_a','fomalhaut','trappist_1']
dists = {s: dist_ly(f'db/systems/{s}.json') for s in STARS}

# 워프 속도(빛의 배수) — FTL. 같은 메트릭 에너지는 거리 무관(버블 standing load),
# 거리는 '체류 시간'에만 들어감(게임 모델의 MJ 적분용).
WARP_BETAS = [10.0, 100.0, 1000.0]

print("="*86)
print("이종물질 실존 가정 — 워프 음에너지 적재량 (메트릭 모델, 거리 무관 standing load)")
print("="*86)
print(f"버블 음에너지 |E| = (c⁴/12G)·β_s²·R²/Δ  →  적재 이종물질 = |E|/c²\n")
print(f"{'β_s (warp)':>11s} | {'정통 Alcubierre/PF':>22s} | {'illustrative toy':>22s}")
print("-"*86)
for b in WARP_BETAS:
    row = [f"{b:>9.0f}c "]
    for key in ('classic','toy'):
        m = MODELS[key]
        E = neg_energy_J(b, m['R_eff'], m['delta'])
        row.append(f"{fmt_mass(E/C2):>22s}")
    print(" | ".join(row))
print()
print("해석: 정통 모델은 β_s=10c·100m 버블에서도 |E|/c²가 우주질량을 수십자릿수 초과 →")
print("      '이종물질이 있어도' 우주 전체를 음에너지로 환산해야 함 = 사실상 불가.")
print("      'toy' 컬럼(g~kg)은 R_eff를 공격적으로 줄였을 때의 스케일 감각용일 뿐, 공개 논문값이 아님.")
print()
print("실제 논문 발표 감축값 (PUBLISHED — 위 toy와 별개의 권위 수치):")
for src, claim in PUBLISHED:
    print(f"  · {src}: {claim}")

# --- 게임튜닝(KSPIE식): 메트릭 무시, ExoticMatter ∝ 선체질량, MJ ∝ 거리·β_s² ---
print("\n" + "="*86)
print("게임튜닝 모델 (KSPIE식) — 거리별 1회 워프 소요량")
print("="*86)
SHIP_T = 100.0                 # 선체 질량 (톤) — 예시 vessel
EM_PER_TONNE = 0.5             # ExoticMatter(units) per tonne — 버블 유지 standing load (튜너)
MJ_PER_TONNE_LY = 2.0          # MegaJoule per (tonne · ly) — 구동/스티어 적분 (튜너)
em_load = SHIP_T * EM_PER_TONNE
print(f"선체 {SHIP_T:.0f} t · ExoticMatter {EM_PER_TONNE}/t · MJ {MJ_PER_TONNE_LY}/(t·ly)  (모두 튜너)")
print(f"버블 유지 ExoticMatter 적재 = {em_load:.1f} units (거리 무관)\n")
print(f"{'target':16s}{'dist ly':>9s}" + "".join(f"{f'T@{int(b)}c (yr)':>14s}" for b in WARP_BETAS) + f"{'구동 MJ/회':>14s}")
for s in STARS:
    name, ly = dists[s]
    times = "".join(f"{ly/b:>14.3f}" for b in WARP_BETAS)   # FTL: T = d/v_s, 광속하한 무시
    mj = SHIP_T * ly * MJ_PER_TONNE_LY
    print(f"{name[:16]:16s}{ly:>9.2f}{times}{mj:>14.0f}")
print("\n해석: 게임 모델은 메트릭 60자릿수 폭주를 버리고 ExoticMatter를 '선체질량 비례 적재물'로,")
print("      에너지를 '거리×질량 MJ'로 재정의 → RP-1 cfg/밸런싱에 바로 얹을 수 있는 실용값.")
print("      (정통/최적화 표는 '왜 게임은 메트릭을 포기하는가'의 근거로 동반.)")
