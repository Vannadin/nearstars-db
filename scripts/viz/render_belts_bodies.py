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
 'jupiter_phys':{'title':'Jupiter — physical','sub':'D-cut dipolar inner + flat magnetodisc outer','R':18,'tilt':10.3,'offset':0.1,
   'inner':{'radiation':1500,'grad':3.3,'dist':2.0,'rad':2.0,'bdist':1e-4,'brad':1.3},
   'outer':{'radiation':150,'grad':2.2,'dist':4.17,'rad':2.5,'dxy':0.174,'comp':1.05,'ext':0.9},
   'pause':{'radiation':-0.01,'rad':63,'comp':1.2,'ext':0.05,'hscale':1.15}},

 # ---- SATURN: 스톡=외대만, 물리=고리가 내대 소거→외대만(축대칭), CRAND 약함 ----
 'saturn_stock':{'title':'Saturn — stock (RSS anchor)','sub':'outer 7/7 only, no inner (rings sweep)','R':12,'tilt':0,
   'outer':{'radiation':150,'grad':2.2,'dist':4.5,'rad':3.0,'comp':1.02,'ext':0.9},
   'pause':{'radiation':-0.011,'rad':20,'comp':1.1,'ext':0.05,'hscale':1.05}},
 'saturn_phys':{'title':'Saturn — physical','sub':'rings absorb inner belt; weak CRAND outer; ~0° tilt','R':12,'tilt':0.01,
   'outer':{'radiation':10,'grad':2.2,'dist':4.0,'rad':1.8,'dxy':0.5,'comp':1.05,'ext':0.85},
   'pause':{'radiation':-0.011,'rad':24,'comp':1.2,'ext':0.05,'hscale':1.1}},

 # ---- URANUS: 극단 tilt 59° + offset 0.3 ----
 'uranus_stock':{'title':'Uranus — stock (RSS anchor)','sub':'offset dipole, pole_lat 31 (=59 tilt), offset 0.3','R':10,'tilt':59,'offset':0.3,
   'inner':{'radiation':75,'grad':3.3,'dist':0.81,'rad':0.7,'bdist':1e-4,'brad':0.9},
   'outer':{'radiation':4,'grad':2.2,'dist':2.6,'rad':2.4,'comp':1.01,'ext':1.0},
   'pause':{'radiation':-0.010,'rad':18,'comp':1.3,'ext':0.1,'hscale':1.1}},
 'uranus_phys':{'title':'Uranus — physical','sub':'tilt 59°, offset 0.3 R_U, mp 18, belt peak ~4.2 R_U','R':10,'tilt':59,'offset':0.3,
   'inner':{'radiation':40,'grad':3.3,'dist':2.0,'rad':1.2,'bdist':1e-4,'brad':1.3},
   'outer':{'radiation':8,'grad':2.2,'dist':4.2,'rad':2.5,'comp':1.05,'ext':0.9},
   'pause':{'radiation':-0.010,'rad':18,'comp':1.2,'ext':0.1,'hscale':1.1}},

 # ---- NEPTUNE: tilt 47° + offset 0.55, 외곽 Triton 컷 ----
 'neptune_stock':{'title':'Neptune — stock (RSS anchor)','sub':'offset dipole, pole_lat 43 (=47 tilt), offset 0.55','R':16,'tilt':47,'offset':0.55,
   'inner':{'radiation':39,'grad':3.3,'dist':0.81,'rad':0.7,'bdist':1e-4,'brad':0.9},
   'outer':{'radiation':2.5,'grad':2.2,'dist':2.6,'rad':2.4,'comp':1.01,'ext':1.0},
   'pause':{'radiation':-0.007,'rad':26.5,'comp':1.3,'ext':0.1,'hscale':1.1}},
 'neptune_phys':{'title':'Neptune — physical','sub':'tilt 47°, offset 0.55 R_N, peak L~7, Triton cut ~14','R':16,'tilt':47,'offset':0.55,
   'inner':{'radiation':30,'grad':3.3,'dist':3.0,'rad':1.5,'bdist':1e-4,'brad':1.3},
   'outer':{'radiation':6,'grad':2.2,'dist':7.0,'rad':4.0,'comp':1.05,'ext':0.9},
   'pause':{'radiation':-0.007,'rad':26.5,'comp':1.2,'ext':0.08,'hscale':1.1}},

 # ---- MERCURY: 벨트 없음, 초소형 offset 자기권 (표면 직격) ----
 'mercury_stock':{'title':'Mercury — stock (ROKerbalism)','sub':'no belt; pause 1.6, offset 0.208','R':3,'tilt':0,'offset':0.208,
   'pause':{'radiation':-0.001,'rad':1.6,'comp':1.4,'ext':0.05,'hscale':1.0}},
 'mercury_phys':{'title':'Mercury — physical','sub':'no stable belt; mp 1.45 R_M, offset 0.20 north, tilt <3°','R':3,'tilt':2,'offset':0.20,
   'pause':{'radiation':-0.001,'rad':1.45,'comp':1.4,'ext':0.05,'hscale':1.0}},

 # ---- EARTH: 기준 (완료) ----
 'earth':{'title':'Earth — reference','sub':'ROKerbalism earth model','R':7,'tilt':11,
   'inner':{'radiation':10.376,'grad':3.3,'dist':0.813,'rad':0.70,'dxy':0.572,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':0.915,'bdxy':0.5},
   'outer':{'radiation':2.214,'grad':2.2,'dist':2.6338,'rad':2.48,'dxy':0.7225,'comp':1.01,'ext':1.0,'bdist':1.4412,'brad':1.4875,'bdxy':0.7225},
   'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1}},

 # ---- GANYMEDE: 약장 임베디드 미니자기권 (Kivelson 2002: 719nT, standoff ~2 R_G, open caps) ----
 'ganymede_stock':{'title':'Ganymede — stock (ROKerbalism)','sub':'inner 0.8/0.6, no pause defined','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':0.8,'rad':0.6}},
 'ganymede_phys':{'title':'Ganymede — physical','sub':'719 nT dipole, standoff ~2 R_G, single weak belt, open caps','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':1.3,'rad':0.4,'bdist':1e-4,'brad':1.05},
   'pause':{'radiation':-0.01,'rad':2.0,'comp':1.15,'ext':0.7,'hscale':1.0}},
}

if __name__=='__main__':
    import sys
    only=sys.argv[1:] if len(sys.argv)>1 else None
    for k,b in BODIES.items():
        if only and k not in only: continue
        render(b, os.path.join(OUT,k+'.png'))
