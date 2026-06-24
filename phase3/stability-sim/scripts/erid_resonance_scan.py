# 40 Eri A b(Erid)/c/d(Threeworld) 공명 스캔: c 질량·c:d 공명으로 d의 e 펌핑, b는 저-e 안정 유지 탐색
import rebound, itertools, math

MSUN_PER_ME = 3.0035e-6
M_STAR = 0.78
A_B, E_B, M_B = 0.224, 0.04, 4.97*MSUN_PER_ME     # Erid (고정)
M_D = 0.015*MSUN_PER_ME                             # Threeworld (달 크기, 고정)
YEARS = 20000.0

def run(a_c, m_c_me, ratio):
    p, q = ratio
    a_d = a_c*(p/q)**(2/3)                          # 외측 d : 내측 c = p:q (p>q)
    sim = rebound.Simulation()
    sim.units = ('yr','AU','Msun')
    sim.integrator = 'whfast'
    sim.add(m=M_STAR)
    # 위상 분산 (resonance capture 가능성 + 비특이)
    sim.add(m=M_B,            a=A_B, e=E_B,  l=0.0,  pomega=0.0)
    sim.add(m=m_c_me*MSUN_PER_ME, a=a_c, e=0.01, l=1.7,  pomega=0.9)
    sim.add(m=M_D,            a=a_d, e=0.01, l=3.3,  pomega=2.1)
    sim.move_to_com()
    P_b = 2*math.pi*math.sqrt(A_B**3/(M_STAR))      # ~ yr (G=4pi^2 in these units)
    sim.dt = P_b/30.0
    sim.init_megno()
    names=['b','c','d']
    emax={n:0.0 for n in names}
    nsteps=int(YEARS/sim.dt)
    sample=max(1,nsteps//4000)
    try:
        for i in range(nsteps):
            sim.integrate(sim.t + sim.dt, exact_finish_time=0)
            if i % sample == 0:
                for j,n in enumerate(names):
                    o=sim.particles[j+1].orbit(primary=sim.particles[0])
                    if o.e>emax[n]: emax[n]=o.e
                    if o.e>0.95 or o.a<0 or o.a>50: raise RuntimeError('unstable')
        megno=sim.megno()
    except (RuntimeError, Exception) as ex:
        return dict(a_c=a_c,m_c=m_c_me,ratio=f"{p}:{q}",a_d=a_d,unstable=True,emax=emax,megno=float('nan'))
    return dict(a_c=a_c,m_c=m_c_me,ratio=f"{p}:{q}",a_d=a_d,unstable=False,emax=emax,megno=megno)

print(f"{'res':4} {'a_c':5} {'m_c':4} {'a_d':6} | {'b_emax':7} {'c_emax':7} {'d_emax':7} {'MEGNO':6} verdict")
rows=[]
for ratio in [(2,1),(3,2)]:
    for a_c in [0.32,0.40]:
        for m_c in [3,10,20]:
            r=run(a_c,m_c,ratio); rows.append(r)
            v = 'UNSTABLE' if r['unstable'] else ('chaos' if (r['megno']>3 or math.isnan(r['megno'])) else 'stable')
            print(f"{r['ratio']:4} {a_c:5.2f} {m_c:4d} {r['a_d']:6.3f} | "
                  f"{r['emax']['b']:7.4f} {r['emax']['c']:7.4f} {r['emax']['d']:7.4f} {r['megno']:6.2f} {v}")
# 최적: 안정 + b 저-e + d 고-e
ok=[r for r in rows if not r['unstable'] and r['megno']<3 and r['emax']['b']<0.12]
ok.sort(key=lambda r:-r['emax']['d'])
print("\n안정+b<0.12 중 d_emax 상위:")
for r in ok[:4]:
    print(f"  {r['ratio']} a_c={r['a_c']} m_c={r['m_c']}M⊕ a_d={r['a_d']:.3f} → d_emax={r['emax']['d']:.3f} b_emax={r['emax']['b']:.4f} MEGNO={r['megno']:.2f}")
