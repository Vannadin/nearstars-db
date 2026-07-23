# 태양계 자기권 천체 6종 스톡 vs 물리 단면 렌더 드라이버 (위키 업로드용 PNG 생성)
import os
from render_belts import render
D=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(D,'wiki-img'); os.makedirs(OUT,exist_ok=True)

BODIES={
 # ---- JUPITER: 스톡=원거리 통짜 동심, 물리=근접 D형 내대+납작 자기원반 ----
 'jupiter_stock':{'title':'Jupiter — stock (ROKerbalism)','sub':'inner 6/1, outer 6.5/6.5 concentric','R':16,'tilt':10.3,
   'inner':{'radiation':300,'grad':3.3,'dist':6.0,'rad':1.0,'comp':1.05,'ext':0.9},
   'outer':{'radiation':50,'grad':2.2,'dist':6.5,'rad':6.5,'comp':1.05,'ext':0.85},
   'pause':{'radiation':-0.01,'rad':60,'comp':1.05,'ext':0.01,'hscale':1.02}},
 # phys 지오메트리 = fit_belts.py 수치 피팅(쌍극자 L-셸 타깃, IoU 명기). pause는 nose=rad/comp 의미론으로 계산.
 'jupiter_phys':{'title':'Jupiter — physical (SDF fit)','sub':'dipolar inner L 1.2-3 (IoU .98) + magnetodisc slab 3-16 (IoU .87)','R':18,'tilt':10.3,'offset':0.1,
   'inner':{'radiation':1500,'grad':3.3,'dist':1.3435,'rad':1.159,'dxy':0.693,'comp':1.05,'ext':0.9,'bdist':3e-4,'brad':0.8889,'bdxy':0.5866},
   'outer':{'radiation':150,'grad':2.2,'dist':2.7525,'rad':2.6703,'dxy':0.1046,'comp':1.05,'ext':0.9,'bdist':1e-4,'brad':3.6874,'bdxy':1.4559},  # 자기원반=적도 전류시트(렌즈형)
   'pause':{'radiation':-0.01,'rad':75.6,'comp':1.2,'ext':0.05,'hscale':1.15}},  # nose 63 R_J (Joy 2002)

 # ---- SATURN: 스톡=외대만, 물리=고리가 내대 소거→외대만(축대칭), CRAND 약함 ----
 # 스톡 값 검증: KSP-RO/ROKerbalism Support/RSS.cfg `saturn` 모델 (2026-07-24 재검증)
 'saturn_stock':{'title':'Saturn — stock (ROKerbalism RSS.cfg)','sub':'saturn model: outer 7/7 only, pause 20/1.02','R':16,'tilt':0,
   'outer':{'radiation':150,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.011,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 'saturn_phys':{'title':'Saturn — physical (SDF fit)','sub':'rings absorb inner belt; CRAND shell L 2.3-6 (IoU .98); ~0° tilt','R':16,'tilt':0.01,
   'outer':{'radiation':10,'grad':2.2,'dist':2.6173,'rad':2.3184,'dxy':0.6735,'comp':1.05,'ext':0.85,'bdist':0.9889,'brad':0.8883,'bdxy':0.6616},  # 고리 바깥 단일 초승달
   'pause':{'radiation':-0.011,'rad':28.8,'comp':1.2,'ext':0.05,'hscale':1.1}},  # nose 24 R_S (Achilleos 2008)

 # ---- URANUS: 극단 tilt 59° + offset 0.3 ----
 # 스톡=generic `saturn` 모델 재사용(외대 7/7만; radiation_inner 75는 has_inner=false라 미사용 죽은 값)
 'uranus_stock':{'title':'Uranus — stock (ROKerbalism RSS.cfg)','sub':'generic saturn model: outer 7/7, pause 20; pole_lat 31.4, offset 0.3','R':16,'tilt':58.6,'offset':0.3,
   'outer':{'radiation':4,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.010,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 'uranus_phys':{'title':'Uranus — physical (SDF fit)','sub':'tilt 59°, offset 0.3 R_U; shells L 1.5-3 / L 3-7 (IoU .97/.98)','R':16,'tilt':59,'offset':0.3,
   'inner':{'radiation':40,'grad':3.3,'dist':1.3456,'rad':1.1589,'dxy':0.6952,'comp':1.02,'ext':1.0,'bdist':0.371,'brad':0.6916,'bdxy':0.5021},
   'outer':{'radiation':8,'grad':2.2,'dist':3.0123,'rad':2.7018,'dxy':0.662,'comp':1.02,'ext':0.95,'bdist':1.3175,'brad':1.1596,'bdxy':0.6748},
   'pause':{'radiation':-0.010,'rad':21.6,'comp':1.2,'ext':0.1,'hscale':1.1}},  # nose 18 R_U (Ness 1986)

 # ---- NEPTUNE: tilt 47° + offset 0.55, 외곽 Triton 컷 ----
 # 스톡=generic `saturn` 모델 재사용(pause 20 — 26.5 아님; radiation_inner 39 미사용 죽은 값)
 'neptune_stock':{'title':'Neptune — stock (ROKerbalism RSS.cfg)','sub':'generic saturn model: outer 7/7, pause 20; pole_lat 43, offset 0.55','R':16,'tilt':47,'offset':0.55,
   'outer':{'radiation':2.5,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.007,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 'neptune_phys':{'title':'Neptune — physical (SDF fit)','sub':'tilt 47°, offset 0.55 R_N; shells L 1.5-5 / L 5-14 Triton cut (IoU .98/.97)','R':16,'tilt':47,'offset':0.55,
   'inner':{'radiation':30,'grad':3.3,'dist':2.1836,'rad':1.93,'dxy':0.6732,'comp':1.02,'ext':1.0,'bdist':0.0563,'brad':0.8488,'bdxy':0.3727},
   'outer':{'radiation':6,'grad':2.2,'dist':5.9998,'rad':5.4076,'dxy':0.6573,'comp':1.02,'ext':0.95,'bdist':2.5862,'brad':1.9982,'bdxy':0.8656},  # peak ~L7, 외곽 ~14(Triton)
   'pause':{'radiation':-0.007,'rad':31.8,'comp':1.2,'ext':0.08,'hscale':1.1}},  # nose 26.5 R_N (Ness 1989)

 # ---- MERCURY: 벨트 없음, 초소형 offset 자기권 (표면 직격) ----
 'mercury_stock':{'title':'Mercury — stock (ROKerbalism)','sub':'no belt; pause 1.6/1.4 (nose 1.14), pole_lat 96, offset 0.208','R':3,'tilt':6,'offset':0.208,
   'pause':{'radiation':-0.001,'rad':1.6,'comp':1.4,'ext':0.05,'hscale':1.0}},
 'mercury_phys':{'title':'Mercury — physical','sub':'no stable belt; mp nose 1.45 R_M, offset 0.20 north, tilt <3°','R':3,'tilt':2,'offset':0.20,
   'pause':{'radiation':-0.001,'rad':2.03,'comp':1.4,'ext':0.05,'hscale':1.0}},  # nose 1.45 R_M (Winslow 2013)

 # ---- EARTH: 앵커 (스톡=튜닝 모델) vs 물리 (standoff 10, 외대 heart L~4.5) ----
 'earth_stock':{'title':'Earth — stock (ROKerbalism)','sub':'inner 0.81/0.70 (D), outer 2.63/2.48 (O), pause 15','R':8,'tilt':11,
   'inner':{'radiation':10.376,'grad':3.3,'dist':0.813,'rad':0.70,'dxy':0.572,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':0.915,'bdxy':0.5},
   'outer':{'radiation':2.214,'grad':2.2,'dist':2.6338,'rad':2.48,'dxy':0.7225,'comp':1.01,'ext':1.0,'bdist':1.4412,'brad':1.4875,'bdxy':0.7225},
   'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1}},
 'earth_phys':{'title':'Earth — physical (SDF fit)','sub':'shells L 1.1-2 / L 3-7, slot between (IoU .98/.98); mp nose 10','R':8,'tilt':11,
   'inner':{'radiation':10.376,'grad':3.3,'dist':0.9104,'rad':0.7714,'dxy':0.7041,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':0.9596,'bdxy':0.8327},
   'outer':{'radiation':2.214,'grad':2.2,'dist':3.0123,'rad':2.7018,'dxy':0.662,'comp':1.01,'ext':1.0,'bdist':1.3175,'brad':1.1596,'bdxy':0.6748},  # L3-7, 보더 카브=슬롯
   'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1}},  # nose 15/1.5=10 R_E — 스톡과 동일(스톡이 이미 정확)

 # ---- GANYMEDE: 약장 임베디드 미니자기권 (Kivelson 2002: 719nT, standoff ~2 R_G, open caps) ----
 'ganymede_stock':{'title':'Ganymede — stock (ROKerbalism)','sub':'inner 0.8/0.6, no pause defined','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':0.8,'rad':0.6}},
 'ganymede_phys':{'title':'Ganymede — physical (SDF fit)','sub':'719 nT dipole; closed-line belt L 1.1-1.9 (IoU .96); mp nose 2, width 5.5','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':0.9573,'rad':0.7293,'dxy':0.7903,'comp':1.05,'ext':0.9,'bdist':0.086,'brad':0.8615,'bdxy':0.7791},
   'pause':{'radiation':-0.01,'rad':2.75,'comp':1.375,'ext':0.7,'hscale':1.0}},  # nose 2.0 / 폭 5.5 R_G (Kivelson 1998)
}

if __name__=='__main__':
    import sys
    only=sys.argv[1:] if len(sys.argv)>1 else None
    for k,b in BODIES.items():
        if only and k not in only: continue
        render(b, os.path.join(OUT,k+'.png'))
