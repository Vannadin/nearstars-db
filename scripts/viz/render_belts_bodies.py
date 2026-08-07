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
 'jupiter_phys':{'title':'Jupiter — physical (SDF fit)','sub':'dipolar inner L 1.2-3 (IoU .98) + magnetodisc slab 3-16 × ±3 (IoU .87)','R':18,'tilt':10.3,'offset':0.1,
   'inner':{'radiation':1500,'grad':3.3,'dist':1.3435,'rad':1.159,'dxy':0.693,'comp':1.05,'ext':0.9,'bdist':3e-4,'brad':0.8889,'bdxy':0.5866},
   'outer':{'radiation':150,'grad':2.2,'dist':3.2565,'rad':3.2269,'dxy':0.1483,'comp':1.05,'ext':0.9,'bdist':1e-4,'brad':4.238,'bdxy':1.85},  # 자기원반=적도 전류시트(렌즈형, 반두께 3=Khurana; 3-16은 프레임 절단)
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
 # 벨트 구조 경계=위성 L-셸 (Krimigis 1986 Miranda 안쪽 예외역 + Cheng 1987 전자 극소: Miranda 5.1/Ariel 7.5/Umbriel 10.4)
 'uranus_phys':{'title':'Uranus — physical (SDF fit)','sub':'tilt 59°, offset 0.3; L 1.5-5 / 5-10 Miranda·Umbriel cut (IoU .98/.97)','R':16,'tilt':59,'offset':0.3,
   'inner':{'radiation':40,'grad':3.3,'dist':2.1836,'rad':1.93,'dxy':0.6732,'comp':1.02,'ext':1.0,'bdist':0.0563,'brad':0.8488,'bdxy':0.3727},
   'outer':{'radiation':8,'grad':2.2,'dist':4.3078,'rad':3.8644,'dxy':0.6644,'comp':1.02,'ext':0.95,'bdist':2.3256,'brad':1.9463,'bdxy':0.7307},
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
 'mercury_stock':{'title':'Mercury — stock (ROKerbalism)','sub':'no belt; pause 1.6/1.4 (nose 1.14), pole_lat 96, offset 0.208, deform 0.1','R':3,'tilt':6,'offset':0.208,
   'pause':{'radiation':-0.001,'rad':1.6,'comp':1.4,'ext':0.05,'hscale':1.0,'deform':0.1}},  # pause_deform=0.1 그대로 반영 (2026-08-04 누락 수정): 다중극 경계의 비축대칭 로브
 'mercury_phys':{'title':'Mercury — physical','sub':'no stable belt; mp nose 1.45 R_M, offset 0.20 north, tilt <3°, deform 0.1','R':3,'tilt':2,'offset':0.20,
   'pause':{'radiation':-0.001,'rad':2.03,'comp':1.4,'ext':0.05,'hscale':1.0,'deform':0.1}},  # nose 1.45 R_M (Winslow 2013); deform 유지 — 실제 자기장이 offset dipole + 고차 다중극

 # ---- EARTH: 앵커 (스톡=튜닝 모델) vs 물리 (standoff 10, 외대 heart L~4.5) ----
 'earth_stock':{'title':'Earth — stock (ROKerbalism)','sub':'inner 0.81/0.70 (D), outer 2.63/2.48 (O), pause 15','R':8,'tilt':11,
   'inner':{'radiation':10.376,'grad':3.3,'dist':0.813,'rad':0.70,'dxy':0.572,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':0.915,'bdxy':0.5},
   'outer':{'radiation':2.214,'grad':2.2,'dist':2.6338,'rad':2.48,'dxy':0.7225,'comp':1.01,'ext':1.0,'bdist':1.4412,'brad':1.4875,'bdxy':0.7225},
   'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1}},
 'earth_phys':{'title':'Earth — physical (SDF fit)','sub':'shells L 1.1-2 (>1000 km) / L 3-7, slot between (IoU .99/.98); mp nose 10','R':8,'tilt':11,
   'inner':{'radiation':10.376,'grad':3.3,'dist':0.9413,'rad':0.7698,'dxy':0.7314,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':1.1836,'bdxy':1.0505},  # 내대 하한=1000km(loss-cone 고갈 경계)
   'outer':{'radiation':2.214,'grad':2.2,'dist':3.0123,'rad':2.7018,'dxy':0.662,'comp':1.01,'ext':1.0,'bdist':1.3175,'brad':1.1596,'bdxy':0.6748},  # L3-7, 보더 카브=슬롯
   'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1}},  # nose 15/1.5=10 R_E — 스톡과 동일(스톡이 이미 정확)

 # ---- GANYMEDE: 약장 임베디드 미니자기권 (Kivelson 2002: 719nT, standoff ~2 R_G, open caps) ----
 'ganymede_stock':{'title':'Ganymede — stock (ROKerbalism)','sub':'inner 0.8/0.6, no pause defined','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':0.8,'rad':0.6}},
 'ganymede_phys':{'title':'Ganymede — physical (SDF fit)','sub':'719 nT dipole; closed-line belt L 1.1-1.9, surface-absorbed (IoU .97); mp nose 2, width 5.5','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':0.8758,'rad':0.7327,'dxy':0.715,'comp':1.05,'ext':0.9,'bdist':0.0222,'brad':0.9408,'bdxy':0.8693},  # 무대기 → 컷=표면(r=1.0)
   'pause':{'radiation':-0.01,'rad':2.75,'comp':1.375,'ext':0.7,'hscale':1.0}},  # nose 2.0 / 폭 5.5 R_G (Kivelson 1998)

 # ---- PROXIMA d: 16 G SPI 관측장 (Zapatero Osorio 2026) → 지구급 자기권 + 강한 포획 벨트 ----
 # 기하 도출(자기권 기하 방법론 Chapman-Ferraro): B_eq = 극장 16 G / 2 = 8 G;
 #   P_ram(0.029 AU) = 태양풍 1 AU (n 5 cm^-3, v 450 km/s) r^-2 스케일 ~ 2.0e-6 Pa
 #   → nose = (B_eq²/2μ0 P_ram)^(1/6) ≈ 7 R_d. 장 범위 3-280 G → nose 4-18 (B^(1/3)).
 # 벨트 셸은 지구형 SDF 재사용(L 1.2-2 내대 / L 3-5.5 외대, standoff 7 안쪽으로 압축).
 # 강도(자기권 기하 방법론 Part B): dose-anchor 보간 10.4×(B_eq/31µT)^1.9, B_eq 800 µT
 #   → 내대 ~5×10³ rad/h, 외대 = 0.2×내대(wind-fed 비, 토러스 없음) ~1×10³ rad/h.
 #   kp_limit.py 검증: L=4, n_cold 1-100 cm⁻³서 CmCk ≪ 1 → K-P 상한 비구속(source-set).
 #   주의: 앵커쌍(지구·목성) 밖 외삽(B_eq 1.9× 목성)이라 신뢰 낮음; 장 범위 3-280 G면
 #   2×10²-10⁶ rad/h. dipole tilt 미지 → 지구형 10° 가정 명기.
 'proxima_d_phys':{'title':'Proxima Cen d — physical (16 G SPI)','sub':'B_p 16 G → mp nose ~7 R_d (4-18 over 3-280 G); shells L 1.2-2 / 3-5.5; dose anchor-interp (low conf); tilt unknown (10° drawn)','R':12,'tilt':10,
   'inner':{'radiation':5000,'grad':3.3,'dist':0.9413,'rad':0.7698,'dxy':0.7314,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':1.0,'bdxy':1.0},  # 무대기 → 하부 컷=표면 r=1.0 (지구 1000km loss-cone 경계는 대기 흡수 산물이라 부적용)
   'outer':{'radiation':1000,'grad':2.2,'dist':2.7,'rad':2.3,'dxy':0.662,'comp':1.01,'ext':1.0,'bdist':1.2,'brad':1.0,'bdxy':0.6748},  # L 3-5.5 (nose 7 안쪽)
   'pause':{'radiation':-0.01,'rad':10.5,'comp':1.5,'ext':0.075,'hscale':1.1}},  # nose 10.5/1.5 = 7 R_d
}

if __name__=='__main__':
    import sys
    only=sys.argv[1:] if len(sys.argv)>1 else None
    for k,b in BODIES.items():
        if only and k not in only: continue
        render(b, os.path.join(OUT,k+'.png'))
