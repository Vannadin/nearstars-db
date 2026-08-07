# Proxima d 벨트 선량 도출 — 자기권 기하 방법론 Part B(dose-anchor 보간 + K-P 검증) 재현 스크립트
import numpy as np
from kp_limit import KPParams, kp_cmck

# --- 1) 경험적 dose-anchor 보간 (Earth 31 uT -> 10.4 rad/h, Jupiter 428 uT -> ~1500) ---
B_eq_uT = 800.0      # 16 G polar / 2 = 8 G equatorial = 800 uT
inner = 10.4 * (B_eq_uT/31.0)**1.9
outer = 0.2 * inner  # wind-fed (Earth) outer/inner ratio; d has no volcanic-moon torus
print(f"anchor interpolation: inner {inner:.0f} rad/h, outer {outer:.0f} rad/h")
print(f"  (extrapolation: B_eq {B_eq_uT/428:.1f}x Jupiter anchor)")
# field-range sensitivity 3-280 G polar
for Bp in (3.0, 280.0):
    Beq = Bp/2*100  # G -> uT
    print(f"  B_p {Bp:>5.0f} G -> inner {10.4*(Beq/31.0)**1.9:,.0f} rad/h")

# --- 2) K-P ceiling check (outer belt L=4, Earth spectral shape, no plasmasphere) ---
Rp_cm = 4.587e8  # 4587 km
for n_cold in (1.0, 10.0, 100.0):
    p = KPParams(MB=None, L=4, Rp=Rp_cm, bsub=0, n_cold=n_cold,
                 Const=2.38e6, kT=0.001, gam1=0.978364, Eo=1748.566,
                 gam2=7.036234, ss=0.3, B_nT=8e5/64)  # B_eq/L^3
    E, cm = kp_cmck(p)
    print(f"n_cold {n_cold:>5.0f} cm^-3: CmCk peak {np.max(cm):.3g} "
          f"(Earth-shape spectrum at Earth normalization; <1 = below KP ceiling)")
