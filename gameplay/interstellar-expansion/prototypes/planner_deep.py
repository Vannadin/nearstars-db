# 플래너 심화: 중력 게이팅 경계, 3-leg 프로파일, 쌍성 궤도항, 도착 감속 — 실수치 검증
import math
AU=1.495978707e11; ly=9.4607e15; yr=3.15576e7; c=2.99792458e8
G=6.674e-11; Msun=1.98892e30; g0=9.80665

print("="*64)
print("1) 중력 게이팅 경계  r_g where  GM/r^2 < a_thresh")
print("="*64)
for thr in [1e-9,1e-10,1e-12]:
    for name,M in [("Sol",1.0),("AlphaCenA",1.1055),("TRAPPIST-1",0.0898)]:
        rg=math.sqrt(G*M*Msun/thr)
        print(f"  a<{thr:.0e} m/s^2  {name:11s} M={M:.3f}  r_g={rg/AU:8.0f} AU = {rg/ly:.4f} ly")
    print()

print("="*64)
print("2) 3-leg 프로파일 — leg2(워프)가 거리를 지배하는가")
print("="*64)
rg=math.sqrt(G*1.0*Msun/1e-10)  # ~boundary, both ends ~ similar order
for tgt,dly in [("AlphaCen",4.40),("Barnard",5.99),("TRAPPIST-1",40.7)]:
    d=dly*ly
    sub=2*rg  # 양끝 각각 한 번
    print(f"  {tgt:11s} dist={dly:5.2f} ly  sublight legs≈{2*rg/AU:6.0f} AU = {sub/d*100:6.3f}% of trip  → warp leg = {100-sub/d*100:.3f}%")

print()
print("="*64)
print("3) 쌍성 궤도항 — Alpha Cen A 가 transit 동안 궤도상에서 얼마나 움직이나")
print("="*64)
# Alpha Cen AB: P=79.91yr e=0.5179 a_arcsec=17.57 @ 1.3475pc, M_A=1.1055 M_B=0.9092
P=79.91; e=0.5179; a_arcsec=17.57; dist_pc=1.34749
a_tot_AU=a_arcsec*dist_pc
MA,MB=1.1055,0.9092
a_A=a_tot_AU*MB/(MA+MB)   # A의 바리센터 기준 궤도 반장축
print(f"  a_total={a_tot_AU:.2f} AU, a_A(barycentric)={a_A:.2f} AU, P={P} yr, e={e}")
def kepler_pos(a,e,P,t,t0=0.0):
    n=2*math.pi/P; M=n*(t-t0)
    E=M
    for _ in range(50): E=M+e*math.sin(E)
    x=a*(math.cos(E)-e); y=a*math.sqrt(1-e*e)*math.sin(E)
    return x,y
for warp,T in [("1c",4.40),("10c",0.44),("100c",0.044)]:
    x0,y0=kepler_pos(a_A,e,P,0.0)
    x1,y1=kepler_pos(a_A,e,P,T)
    disp=math.hypot(x1-x0,y1-y0)
    print(f"  warp={warp:5s} transit={T:5.2f} yr  A moves {disp:6.3f} AU along its orbit  (vs lead-miss scale)")

print()
print("="*64)
print("4) 도착 감속 — frame(a)로 도착속도 |v_star| 죽이는 비용 (토치 Isp=1e6 s)")
print("="*64)
ve=1e6*g0  # 9.81e6 m/s
for star,vkm in [("AlphaCen A",28.0),("Barnard",142.0),("TRAPPIST-1",80.0)]:
    v=vkm*1000
    MR=math.exp(v/ve)
    prop_pct=(1-1/MR)*100
    # 1g 감속 가정
    t_brake=v/g0; dist_brake=v*v/(2*g0)
    print(f"  {star:11s} arrive {vkm:5.0f} km/s  propellant={prop_pct:5.2f}% of wet mass  | @1g: brake {t_brake/3600:4.1f} h over {dist_brake/AU:.4f} AU")
