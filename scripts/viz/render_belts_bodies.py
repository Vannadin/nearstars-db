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
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). 63 R_J standoff 안의 벨트라 eps~0.002 → 대칭이 물리값
   # (배포 1.05/0.9는 연출이었음). grad 내대: 피크 1.5-2 R_J (Divine & Garrett 1983).
   'inner':{'radiation':1500,'grad':2.24,'dist':1.3435,'rad':1.159,'dxy':0.693,'comp':1.0,'ext':1.0,'bdist':3e-4,'brad':0.8889,'bdxy':0.5866},
   'outer':{'radiation':150,'grad':2.15,'dist':3.2565,'rad':3.2269,'dxy':0.1483,'comp':1.0,'ext':0.998,'bdist':1e-4,'brad':4.238,'bdxy':1.85},  # 자기원반=적도 전류시트(렌즈형, 반두께 3=Khurana; 3-16은 프레임 절단)
   # Rutala 2025 S97* 적합: α = 0.28 + 1.08·p_SW, r_SS = 38.0·p_SW^-0.25 [R_J].
   # 노즈 63 R_J(Joy 2002 압축 상태) ⇒ p_SW 0.132 nPa ⇒ α 0.423.
   'pause':{'radiation':-0.01,'rad':75.6,'comp':1.2,'ext':0.05,'hscale':1.15,
            'shue_alpha':0.423,'shue_nose':63}},  # nose 63 R_J (Joy 2002)

 # ---- SATURN: 스톡=외대만, 물리=고리가 내대 소거→외대만(축대칭), CRAND 약함 ----
 # 스톡 값 검증: KSP-RO/ROKerbalism Support/RSS.cfg `saturn` 모델 (2026-07-24 재검증)
 'saturn_stock':{'title':'Saturn — stock (ROKerbalism RSS.cfg)','sub':'saturn model: outer 7/7 only, pause 20/1.02','R':16,'tilt':0,
   'outer':{'radiation':150,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.011,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 'saturn_phys':{'title':'Saturn — physical (SDF fit)','sub':'rings absorb inner belt; CRAND shell L 2.3-6 (IoU .98); ~0° tilt','R':16,'tilt':0.01,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). eps 0.002 → 대칭. grad: 자기 프로파일 근거 없어 CRAND 아날로그(지구 외대)
   'outer':{'radiation':10,'grad':2.15,'dist':2.6173,'rad':2.3184,'dxy':0.6735,'comp':1.0,'ext':0.998,'bdist':0.9889,'brad':0.8883,'bdxy':0.6616},  # 고리 바깥 단일 초승달
   'pause':{'radiation':-0.011,'rad':28.8,'comp':1.2,'ext':0.05,'hscale':1.1}},  # nose 24 R_S (Achilleos 2008)

 # ---- URANUS: 극단 tilt 59° + offset 0.3 ----
 # 스톡=generic `saturn` 모델 재사용(외대 7/7만; radiation_inner 75는 has_inner=false라 미사용 죽은 값)
 'uranus_stock':{'title':'Uranus — stock (ROKerbalism RSS.cfg)','sub':'generic saturn model: outer 7/7, pause 20; pole_lat 31.4, offset 0.3','R':22,'tilt':58.6,'offset':0.3,
   'outer':{'radiation':4,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.010,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 # 벨트 구조 경계=위성 L-셸 (Krimigis 1986 Miranda 안쪽 예외역 + Cheng 1987 전자 극소: Miranda 5.1/Ariel 7.5/Umbriel 10.4)
 'uranus_phys':{'title':'Uranus — physical (SDF fit)','sub':'tilt 59°, offset 0.3; L 1.5-5 / 5-10 Miranda·Umbriel cut (IoU .98/.97)','R':22,'tilt':59,'offset':0.3,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). grad: 프로파일이 위성-소거 극소 사이 넓은 최대(Cheng 1987)라
   # 피크가 껍질 핵심 → 컷 이후 최심점으로 클램프한 하한값. 1.0을 그대로 넣으면 포화 지점이 없어 실효 강도가 0.64배로 깎임.
   'inner':{'radiation':40,'grad':1.57,'dist':2.1836,'rad':1.93,'dxy':0.6732,'comp':1.001,'ext':0.997,'bdist':0.0563,'brad':0.8488,'bdxy':0.3727},
   'outer':{'radiation':8,'grad':1.85,'dist':4.3078,'rad':3.8644,'dxy':0.6644,'comp':1.005,'ext':0.977,'bdist':2.3256,'brad':1.9463,'bdxy':0.7307},
   'pause':{'radiation':-0.010,'rad':21.6,'comp':1.2,'ext':0.1,'hscale':1.1}},  # nose 18 R_U (Ness 1986)

 # ---- NEPTUNE: tilt 47° + offset 0.55, 외곽 Triton 컷 ----
 # 스톡=generic `saturn` 모델 재사용(pause 20 — 26.5 아님; radiation_inner 39 미사용 죽은 값)
 'neptune_stock':{'title':'Neptune — stock (ROKerbalism RSS.cfg)','sub':'generic saturn model: outer 7/7, pause 20; pole_lat 43, offset 0.55','R':28,'tilt':47,'offset':0.55,
   'outer':{'radiation':2.5,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.007,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 'neptune_phys':{'title':'Neptune — physical (SDF fit)','sub':'tilt 47°, offset 0.55 R_N; shells L 1.5-5 / L 5-14 Triton cut (IoU .98/.97)','R':28,'tilt':47,'offset':0.55,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). grad 외대: 피크 L7 (Stone 1989), 내대: 프로파일 없어 지구 내대 아날로그
   'inner':{'radiation':30,'grad':2.09,'dist':2.1836,'rad':1.93,'dxy':0.6732,'comp':1.0,'ext':0.999,'bdist':0.0563,'brad':0.8488,'bdxy':0.3727},
   'outer':{'radiation':6,'grad':2.63,'dist':5.9998,'rad':5.4076,'dxy':0.6573,'comp':1.004,'ext':0.98,'bdist':2.5862,'brad':1.9982,'bdxy':0.8656},  # peak ~L7, 외곽 ~14(Triton)
   'pause':{'radiation':-0.007,'rad':31.8,'comp':1.2,'ext':0.08,'hscale':1.1}},  # nose 26.5 R_N (Ness 1989)

 # ---- MERCURY: 벨트 없음, 초소형 offset 자기권 (표면 직격) ----
 'mercury_stock':{'title':'Mercury — stock (ROKerbalism)','sub':'no belt; pause 1.6/1.4 (nose 1.14), pole_lat 96, offset 0.208, deform 0.1','R':3,'tilt':6,'offset':0.208,
   'pause':{'radiation':-0.001,'rad':1.6,'comp':1.4,'ext':0.05,'hscale':1.0,'deform':0.1}},  # pause_deform=0.1 그대로 반영 (2026-08-04 누락 수정): 다중극 경계의 비축대칭 로브
 'mercury_phys':{'title':'Mercury — physical','sub':'no stable belt; mp nose 1.45 R_M, offset 0.20 north, tilt <3°, deform 0.1','R':3,'tilt':2,'offset':0.20,
   # Winslow 2013 은 MESSENGER 통과를 Shue 형식으로 적합했다: R_ss 1.45 R_M, flaring α 0.5
   'pause':{'radiation':-0.001,'rad':2.03,'comp':1.4,'ext':0.05,'hscale':1.0,'deform':0.1,
            'shue_alpha':0.5,'shue_nose':1.45}},  # nose 1.45 R_M (Winslow 2013); deform 유지 — 실제 자기장이 offset dipole + 고차 다중극

 # ---- VENUS: 다이나모 없음 → 유도 자기권(전리층 pause만, 벨트 없음) ----
 # ROKerbalism: RadiationBody[Eve]→Venus, radiation_model = ionosphere, radiation_pause = -0.005.
 # ionosphere 모델 = pause_radius 1.1 / extension 0.2 (System/Radiation.cfg). 벨트 필드 자체가 없다.
 'venus_stock':{'title':'Venus — stock (ROKerbalism)','sub':'ionosphere model: pause 1.1/ext 0.2, no belts (induced magnetosphere)','R':28,'tilt':0,
   'pause':{'radiation':-0.005,'rad':1.1,'ext':0.2,'hscale':1.0}},

 # phys = 방법론 Part A '유도 자기권' 절로 계산. 이오노포즈는 실측 스케일을 쓴다(압력균형이 열압 대
 # 항성풍이라 ^(1/6) 법칙 부적용). Brace 1980(PVO): 평균 이오노포즈 직하 330 km, 황혼 700 km,
 # 새벽 1000 km → R_V 6051.8 km 기준 nose 1.0545, 명암경계선 평균 1.1405 R_V.
 # Kerbalism 의미론: pause_radius=플랭크=1.140, compression=플랭크/노즈=1.081 (→ 노즈 1.0545 복원),
 # extension=플랭크/꼬리=0.0456 (폐곡선 X=25 R_V — 확정 횡단 20 R_V 바로 밖, 엔진 요구 파라미터).
 # 벨트 없음(고유 다이나모 부재), radiation_pause 는 유도 경계라 쌍극보다 약한 스톡 스케일 -0.005 유지.
 # 오버레이 = Martinecz et al. 2009 의 IMB 모델 형식 그대로: 주간면 원 + 야간면 직선.
 # 야간면 직선 ρ = 1.13 − 0.101·X' (Edberg 2024 arXiv:2410.21856 §4.2 가 20 R_V 까지 유효 확인,
 # 재적합 0.097/1.10 과의 차이는 20 R_V 에서 0.1 R_V). 벌어짐 각 arctan(0.101) = 5.77°.
 # 원뿔 단면은 쓰지 않는다 — 그건 활머리충격파용 형식이고, 노즈·명암경계선을 지나는 원뿔은
 # 꼬리가 실측의 1.6배로 벌어진다(−20 R_V 에서 5.05 대 3.15). 자세한 기각 근거는 방법론 Part C.
 # 엔진은 닫힌 부피를 요구한다(cfg 로 번역돼야 하므로 페이드아웃은 쓸 수 없다). 측정된 원뿔에
# 폐곡선 항 (1-(d/X)^m) 을 곱해 닫는다 — X=25, m=20 이면 15 R_V 안쪽 오차 0.00%,
# 최외곽 측정점(20 R_V)에서 1.15% 로 Edberg 의 통과 불확실성(~1시간 구간)보다 훨씬 작다.
# X 를 40 까지 늘리면 그 점이 더 좋아지지만 확정 범위의 2배까지 외삽하게 된다 → 25 를 택한다.
# 닫힌 면이 벌어지면 최대폭이 반드시 생긴다. 여기서는 d≈21(측정 범위 바로 밖)이고,
# 기각한 타원은 d=5(측정 범위 안)였다 — 그게 둘의 차이다.
 'venus_phys':{'title':'Venus — physical (induced)','sub':'nose 1.05 R_V (330 km), terminator 1.13, flare 5.8° (measured to 20), closed at 25 R_V; no belts','R':28,'tilt':0,
   'pause':{'radiation':-0.005,'rad':1.14,'comp':1.081,'ext':0.0456,'hscale':1.0,
            'imb_nose':1.055,'imb_term':1.13,'imb_slope':0.101,'imb_close':25,'imb_m':20,
            'imb_label':'Martinecz 2009 / Edberg 2024'}},

 # ---- MARS: 지각 잔류 자기(다극·약장) → irregular 모델 (pause_deform 0.1 로 울퉁불퉁) ----
 # 업스트림 Kerbalism: RadiationBody[Duna] = irregular, radiation_pause = -0.003.
 # ROKerbalism 의 RSS.cfg 는 +RadiationBody[Duna]{@name = Mars} 로 복사하지만, 그들 자신의
 # System/Radiation.cfg 에는 Duna 정의가 없다 → 그 조합에서는 화성에 RadiationBody 가 안 생긴다(배포 갭).
 'mars_stock':{'title':'Mars — stock (Kerbalism irregular)','sub':'irregular model: pause 1.25/comp 1.1/ext 0.75/deform 0.1 — crustal-anomaly look; no belts','R':28,'tilt':0,
   'pause':{'radiation':-0.003,'rad':1.25,'comp':1.1,'ext':0.75,'hscale':1.0,'deform':0.1}},

 # phys = Vignes et al. 2000 (GRL 27, 49) Table 2 의 MPB 원뿔 적합, 직접 적합 N=488:
 #   X0 0.78 ± 0.01,  e 0.90 ± 0.01,  L 0.96 ± 0.01,  R_SD(직하) 1.29 ± 0.04,  R_TD(명암경계선) 1.47 ± 0.08 [R_M]
 # Kerbalism 의미론으로: pause_radius = 플랭크 = 1.47, compression = 1.47/1.29 = 1.1395 (→ 노즈 1.29 복원).
 # 야간면은 Vignes 의 원뿔을 쓰지 않는다: 초록 자신이 "nightside MPB position is highly variable" 이라
 # 적었고, Němec 2020 (2020JGRA..12528509N) 은 MAVEN 기반 모델조차 "unreliable beyond the terminator"
 # 라고 명시한다. 그 타원을 연장하면 x −3.77 에서 폭이 명암경계선의 1.5배로 불룩해지고 −8.8 에서 닫히는데,
 # 둘 다 통과 자료가 없는 구간의 외삽이다. 대신 금성의 실측 벌어짐(5.77°)을 명암경계선 반지름 비로
 # 스케일해 7.49° 로 쓴다 — Phobos-2 대 PVO 비교가 두 유도 자기꼬리 구조에 유의미한 차이가 없다고
 # 보고한 데 근거한 유추다(2001AGUSM..SM32D06K). 화성 실측이 아니라 유추임을 명시한다.
 # 검증: 그 각도면 주간면 원의 명암경계선 기울기 0.135 와 야간면 원뿔 0.131 이 3% 안에서 접합된다(설계 아님).
 # pause_deform 0.1 은 스톡 irregular 에서 물려받은 값이다 — 지각 잔류자기의 비축대칭성을 뜻하지만
 # 크기는 도출하지 않았다(Vignes 는 남북 비대칭을 정량화하지 않는다).
 'mars_phys':{'title':'Mars — physical (MPB fit)','sub':'dayside nose 1.29 R_M, terminator 1.47; nightside flare 7.5° (Venus analogue), closed at 25 R_M; no belts','R':28,'tilt':0,
   'pause':{'radiation':-0.003,'rad':1.47,'comp':1.1395,'ext':0.0588,'hscale':1.0,'deform':0.1,
            'imb_nose':1.285,'imb_term':1.47,'imb_slope':0.1314,'imb_close':25,'imb_m':20,
            'imb_label':'Vignes 2000 dayside + Venus-analogue flare'}},

 # ---- EARTH: 앵커 (스톡=튜닝 모델) vs 물리 (standoff 10, 외대 heart L~4.5) ----
 'earth_stock':{'title':'Earth — stock (ROKerbalism)','sub':'inner 0.81/0.70 (D), outer 2.63/2.48 (O), pause 15','R':12,'tilt':11,
   'inner':{'radiation':10.376,'grad':3.3,'dist':0.813,'rad':0.70,'dxy':0.572,'comp':1.01,'ext':1.0,'bdist':1e-4,'brad':0.915,'bdxy':0.5},
   'outer':{'radiation':2.214,'grad':2.2,'dist':2.6338,'rad':2.48,'dxy':0.7225,'comp':1.01,'ext':1.0,'bdist':1.4412,'brad':1.4875,'bdxy':0.7225},
   'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1}},
 'earth_phys':{'title':'Earth — physical (SDF fit)','sub':'shells L 1.1-2 (>1000 km) / L 3-7, slot between (IoU .99/.98); mp nose 10','R':12,'tilt':11,
   # grad/comp/ext = 자기권 기하 방법론 Part C 도출값 (2026-08-13). grad=rad/d*(피크 깊이, d_max 클램프),
   # comp/ext = pause 비대칭 × eps=(r_core/nose)³. 아래 IoU 수치는 L-셸 피팅(dist/rad/dxy/border) 기준이라 무영향.
   'inner':{'radiation':10.376,'grad':2.09,'dist':0.9413,'rad':0.7698,'dxy':0.7314,'comp':1.001,'ext':0.999,'bdist':1e-4,'brad':1.1836,'bdxy':1.0505},  # 내대 하한=1000km(loss-cone 고갈 경계). grad: 피크 L1.5(Ginet 2013)
   'outer':{'radiation':2.214,'grad':2.15,'dist':3.0123,'rad':2.7018,'dxy':0.662,'comp':1.025,'ext':0.953,'bdist':1.3175,'brad':1.1596,'bdxy':0.6748},  # L3-7, 보더 카브=슬롯. grad: heart L4.5 → 배포 2.2 복원
   # Shue 기준선: 적합값이 있는 바디에만 넣는다(Shue 1998 지구 α 0.58, 노즈 10 R_E, 꼬리 관측 ~200)
   'pause':{'radiation':-0.01,'rad':15,'comp':1.5,'ext':0.075,'hscale':1.1,
            'shue_alpha':0.58,'shue_nose':10,'shue_tail':200}},  # nose 15/1.5=10 R_E — 스톡과 동일(스톡이 이미 정확)

 # ---- GANYMEDE: 약장 임베디드 미니자기권 (Kivelson 2002: 719nT, standoff ~2 R_G, open caps) ----
 'ganymede_stock':{'title':'Ganymede — stock (ROKerbalism)','sub':'inner 0.8/0.6, no pause defined','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':0.8,'rad':0.6}},
 'ganymede_phys':{'title':'Ganymede — physical (SDF fit)','sub':'719 nT dipole; closed-line belt L 1.1-1.9, surface-absorbed (IoU .97); mp nose 2, width 5.5','R':4,'tilt':4,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). eps 0.139(작은 standoff의 큰 몫을 벨트가 채움)이라
   # 도출 comp 1.052가 배포값 1.05를 되찾음 — 이 바디가 비대칭 레시피의 검증 앵커다.
   'inner':{'radiation':0.33,'grad':2.09,'dist':0.8758,'rad':0.7327,'dxy':0.715,'comp':1.052,'ext':0.958,'bdist':0.0222,'brad':0.9408,'bdxy':0.8693},  # 무대기 → 컷=표면(r=1.0)
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
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). 지구 프리셋서 복사돼 있던 comp/ext를 교체:
   # 외대 핵심이 nose의 47%(eps 0.107)라 이 바디는 실제로 비대칭이어야 한다 → 1.053/0.901. grad는 지구 아날로그.
   'inner':{'radiation':5000,'grad':2.09,'dist':0.9413,'rad':0.7698,'dxy':0.7314,'comp':1.002,'ext':0.996,'bdist':1e-4,'brad':1.0,'bdxy':1.0},  # 무대기 → 하부 컷=표면 r=1.0 (지구 1000km loss-cone 경계는 대기 흡수 산물이라 부적용)
   'outer':{'radiation':1000,'grad':2.15,'dist':2.7,'rad':2.3,'dxy':0.662,'comp':1.053,'ext':0.901,'bdist':1.2,'brad':1.0,'bdxy':0.6748},  # L 3-5.5 (nose 7 안쪽)
   'pause':{'radiation':-0.01,'rad':10.5,'comp':1.5,'ext':0.075,'hscale':1.1}},  # nose 10.5/1.5 = 7 R_d
}

if __name__=='__main__':
    import sys
    only=sys.argv[1:] if len(sys.argv)>1 else None
    for k,b in BODIES.items():
        if only and k not in only: continue
        render(b, os.path.join(OUT,k+'.png'))
