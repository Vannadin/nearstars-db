# Δv 기반 lead-intercept 플래너 프로토타입: Δv→소요시간 T→T시점 별 위치를 타겟으로
# 입력 Δv(단위 c), 출력 T·미래타겟 오프셋(lead)·도착상대속도. 실제 DB astrometry 사용.
import json, math

PC_AU=206264.806; KMS_TO_AUYR=0.21094952; C_AUYR=63241.077; K_PM=4.740470446
def vec_sub(a,b): return [a[i]-b[i] for i in range(3)]
def dot(a,b): return sum(a[i]*b[i] for i in range(3))
def norm(a): return math.sqrt(dot(a,a))

def star_state(path):
    """returns (name, P0[AU], v_star[AU/yr], dist_ly)"""
    d=json.load(open(path)); r=d['stars'][0]['raw']
    ra=math.radians(r['ra_deg']); dec=math.radians(r['dec_deg'])
    dist_pc=1000.0/r['parallax_mas']; dist_au=dist_pc*PC_AU
    ca,sa,cd,sd=math.cos(ra),math.sin(ra),math.cos(dec),math.sin(dec)
    r_hat=[cd*ca, cd*sa, sd]; a_hat=[-sa, ca, 0.0]; d_hat=[-sd*ca,-sd*sa,cd]
    P0=[dist_au*x for x in r_hat]
    v_ra =K_PM*(r['pmra_mas_yr']/1000.0)*dist_pc      # km/s
    v_dec=K_PM*(r['pmdec_mas_yr']/1000.0)*dist_pc
    v_rad=r.get('radial_velocity_km_s',0.0) or 0.0
    v_kms=[v_rad*r_hat[i]+v_ra*a_hat[i]+v_dec*d_hat[i] for i in range(3)]
    v_star=[v*KMS_TO_AUYR for v in v_kms]
    return d.get('system_name',path), P0, v_star, dist_au/PC_AU/0.30660139  # ly

def solve_T(P0, v_star, dv_c, r0=(0,0,0), v0=(0,0,0)):
    """v_avg = c*tanh(Δv/4c) (광속 하한 자동 준수). returns T_yr, target, lead_miss_AU, arrival_relv_kms"""
    v_avg=C_AUYR*math.tanh(dv_c*C_AUYR/(4*C_AUYR)/ (C_AUYR/C_AUYR))  # = c*tanh(dv_c/4) since dv in units c
    v_avg=C_AUYR*math.tanh(dv_c/4.0)
    R0=vec_sub(P0,list(r0))
    A=v_avg*v_avg-dot(v_star,v_star)
    B=-2*dot(R0,v_star); Cc=-dot(R0,R0)
    disc=B*B-4*A*Cc
    T=(-B+math.sqrt(disc))/(2*A)
    target=[P0[i]+v_star[i]*T for i in range(3)]
    lead_miss=norm([v_star[i]*T for i in range(3)])          # |P(T)-P0|
    relv_auyr=norm(vec_sub(list(v0),v_star))                 # mode(a): v0 - v_star
    return T, target, lead_miss, relv_auyr/KMS_TO_AUYR, v_avg/C_AUYR

stars=['alpha_centauri_a','barnards_star','tau_cet','luhman_16_a','40_eridani_a','fomalhaut','trappist_1']
states={s:star_state(f'db/systems/{s}.json') for s in stars}

print("별 운동 요약 (DB astrometry → 바리센터 공간속도)")
print(f"{'star':14s}{'dist ly':>9s}{'|v_star| km/s':>15s}")
for s in stars:
    n,P0,v,ly=states[s]; print(f"{n[:14]:14s}{ly:9.2f}{norm(v)/KMS_TO_AUYR:15.1f}")

for dv in [0.2, 1.0, 4.0, 12.0]:
    print("\n"+"="*78)
    print(f"Δv = {dv:.1f} c   →   v_avg = {math.tanh(dv/4)*100:.2f}% c   (광속 하한 자동 준수)")
    print("="*78)
    print(f"{'target':14s}{'T (yr)':>9s}{'light floor':>12s}{'lead (future':>14s}{'arrive rel':>12s}")
    print(f"{'':14s}{'':>9s}{'d/c yr':>12s}{' offset AU)':>14s}{'v km/s':>12s}")
    for s in stars:
        n,P0,v,ly=states[s]
        T,tgt,miss,relv,beta=solve_T(P0,v,dv)
        print(f"{n[:14]:14s}{T:9.2f}{ly:12.2f}{miss:14.1f}{relv:12.1f}")
