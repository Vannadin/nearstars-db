# 태양계 자기권 천체 6종 스톡 vs 물리 단면 렌더 드라이버 (위키 업로드용 PNG 생성)
import os
from render_belts import render
D=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(D,'wiki-img'); os.makedirs(OUT,exist_ok=True)

# ---- 자기권계면 α 정합 (2026-08-14) ----
# 정책상 적합된 α 가 있는 천체는 Shue 를 쓴다. 그래서 phys 프리셋의 pause_radius/compression 을
# α 와 정합하게 맞췄다: compression = 2^α (= 플랭크/노즈), pause_radius = 노즈 × 2^α.
# α 근거(전부 전문 검증, docs/phase3/_papers/ 캐시):
#   수성 0.5     Winslow 2013 (_winslow2013) — R_ss 1.45 R_M, α 0.5 @ P_Ram 14.3 nPa
#   지구 0.58    Shue 1998 (_shue1998) 식 (11): α = (0.58 − 0.007 Bz)[1 + 0.024 ln Dp]
#   목성 0.423   Rutala 2025 (2502.09186) S97* Table 2: α = 0.28 + 1.08 p_SW, r_SS = 38.0 p_SW^-0.25
#   토성 0.7358  Kanani 2010 (_kanani2010) 식 (12): α = 0.73 ± 0.07 + (0.4 ± 0.5) Dp → Dp 무의존.
#                노즈 24 R_S ⇒ Dp 0.0146 nPa. 교차검증: Arridge 2006 (_arridge2006) α = 0.77 − 1.5 Dp
#                는 같은 노즈에서 0.7356 — 계수도 자료도 다른 두 적합이 0.0002 안에서 일치한다.
#   천왕성·해왕성 0.58  적합이 존재하지 않아 지구 값을 유추로 채택(오너 결정). 근거는 내부 플라스마
#                부하가 지구급이라는 점 — Bridge 1986 "The Uranian moons do not appear to be a
#                significant plasma source"(피크 2 cm^-3), Belcher 1989 해왕성 최대밀도 1.4 cm^-3
#                "the smallest observed by Voyager in any magnetosphere". 유추이며 적합이 아니다.
# ---- 꼬리 길이 L = 150 · 노즈 (2026-08-15 확정) ----
# L(= pause_radius/pause_extension)은 엔진이 부피를 닫는 지점이고 물리량이 아니다. Shue 는
# 파라미터가 r₀ 와 α 둘뿐이라 길이를 주지 않고(α<0.5 는 0 으로 점근, =0.5 는 원통, >0.5 는 발산),
# 물리적 꼬리 끝은 어느 행성에서도 측정된 적이 없다. 도출 시도 여섯 개는 방법론 Part A 에 기각 표로.
# 그래서 관례로 정하되 조건 하나를 만족시킨다 — 어떤 실측과도 모순되지 않을 것.
# 발표된 꼬리 도달 범위는 전부 탐사 범위가 만든 하한이고, 가장 먼 것이 목성 ≥9000 R_J
# (Lepping 1983) = 노즈 63 R_J 의 142.9 배다. 그래서 L = 150 × 노즈 로 둔다.
#   실측 하한 검사: 목성 143× ✓  지구 22.5× ✓  금성 19× ✓  수성 2.1× ✓
# 결과(꼬리를 AU 로): 목성 4.516 AU 로 토성 궤도(9.58 AU)를 넘는다 — Voyager 2 가 4.5 AU 하류에서
# 검출하고(Kurth 1982) 토성이 그 안에 잠기는 것까지 관측된(Desch 1983) 그 현상과 맞는다.
# 주의: 가니메데(알프벤 날개 영역, 태양풍이 아니라 목성 플라스마가 흐름)와 NearStars 바디는
# 적용하지 않았다. 후자는 phase4 보드가 소스이므로 거기서 바꿔야 한다.
# ---- 스톡 값의 근거: 상류 cfg 주석을 직접 확인한 결과 (2026-08-15) ----
# 스톡 숫자가 무엇을 근거로 그 형상이 됐는지 알아보려고 Kerbalism 원본
# GameData/KerbalismConfig/System/Radiation.cfg 의 저작자 주석을 전부 읽었다. 결론은
# **숫자의 근거를 적은 주석이 하나도 없다** 는 것이다. 남아 있는 주석은 근거가 아니라 설정 서술이다.
#   earth      "Use this when you tweak radiation belts, it helps. Promise." + Desmos 계산기 링크,
#              NASA/위키 밴앨런 자료 — 즉 값을 눈으로 맞추는 도구를 안내한 것이지 도출이 아니다.
#   giant      "the magnetopause lies at a distance of between 60 and 70 RJ" — 유일하게 실측에 가깝고,
#              우리 노즈 63 R_J 와 부합한다. Pioneer 10 이 25만 rad 를 받았다는 서술이 함께 있다.
#   irregular  "some unknown mechanism is producing a very weak, irregular field"
#   ionosphere "lacking internal dynamo, the upper strate of atmosphere is ionized ... by the solar wind"
#   metallic   "the body is deep in the star gravity well, and rich in heavy elements"
#   solidiron  "radiation model for a giant's moon"        anomaly "...small but intense field at the poles"
#   Sun(body)  "we want ~0.01 rad/h at Kerbin (d = 1 AU)"  ← 목표치를 정하고 역산했음을 저작자가 직접 밝힌다.
#   Jool(body) 목성 자기장이 자전축에서 10.8° 기울고 극성이 반대라는 서술.
#   그 외 바디는 주석이 전혀 없다.
# 그러니 스톡 값은 "출처를 못 찾은" 것이 아니라 **저작자가 근거를 두지 않은** 값이다. 게다가
# metallic·solidiron·anomaly 처럼 이름부터 KSP 가상 천체용 범용 모델이고, ROKerbalism 은 그걸 실제
# 행성에 재바인딩만 한다 — 토성·천왕성·해왕성이 같은 `saturn` 모델을 공유하는 이유다.
# 이것이 우리가 phys 프리셋을 전부 다시 도출한 이유이고, 아래 각 stock 항목의 주석은 그 대조다.
# pause_height_scale 은 물리 프리셋에서 전부 1.0 이다. Shue 는 축대칭이고, 스톡이 쓰는 1.1 은
# 자오면 폭을 1/1.1 로 눌러 인코딩하려던 곡선 자체에서 벗어난다(방법론 Part C). 2026-08-16 에
# 태양계 물리 프리셋 다섯 개(지구·목성·토성·천왕성·해왕성)를 1.0 으로 맞춰 NearStars 쪽과 통일했다.
# *_stock 과 *_pre 는 당시 값을 기록하는 프리셋이라 손대지 않는다.
BODIES={
 # ---- JUPITER: 스톡=원거리 통짜 동심, 물리=근접 D형 내대+납작 자기원반 ----
 # 스톡은 Kerbalism/ROKerbalism 저작값이고 물리 도출이 아니다(전용 `jupiter` 모델).
 # pause 60 / comp 1.05 → 노즈 57. 실측 노즈는 63 R_J 압축 · 92 팽창
 #   (Joy 2002, https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J) — 스톡이 10% 작다.
 # 내대 6.0/1.0 = 적도 5-7 R_J / 실측 피크는 1.5-2 R_J (Divine & Garrett 1983,
 #   https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D) — 강한 벨트를 3배 밖에 둔다.
 # 외대 6.5/6.5 동심 구 / 실측은 납작한 적도 전류시트 (Khurana 1989,
 #   https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K).
 'jupiter_stock':{'title':'Jupiter — stock (ROKerbalism)','sub':'inner 6/1, outer 6.5/6.5 concentric','R':16,'tilt':10.3,
   'inner':{'radiation':300,'grad':3.3,'dist':6.0,'rad':1.0,'comp':1.05,'ext':0.9},
   'outer':{'radiation':50,'grad':2.2,'dist':6.5,'rad':6.5,'comp':1.05,'ext':0.85},
   'pause':{'radiation':-0.01,'rad':60,'comp':1.05,'ext':0.01,'hscale':1.02}},
 # phys 지오메트리 = fit_belts.py 수치 피팅(쌍극자 L-셸 타깃, IoU 명기). pause는 nose=rad/comp 의미론으로 계산.
 # 도출 사슬(pause): 노즈 63 R_J (Joy 2002) + α 0.423 (Rutala 2025 S97*) →
 #   pause_radius = 노즈·2^α = 84.4649, compression = 2^α = 1.3407,
 #   extension = pause_radius/(150·노즈) = 0.0089380  ← L = 150×노즈 관례(도출 아님, 파일 머리말).
 # 벨트: fit_belts.py 로 쌍극 L-셸에 수치 피팅(IoU 아래 캡션), 셸 경계는 위 논문들.
 'jupiter_phys':{'title':'Jupiter — physical (SDF fit)','sub':'dipolar inner L 1.2-3 (IoU .98) + magnetodisc slab 3-16 × ±3 (IoU .87)','R':18,'tilt':10.3,'offset':0.1,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). 63 R_J standoff 안의 벨트라 eps~0.002 → 대칭이 물리값
   # (배포 1.05/0.9는 연출이었음). grad 내대: 피크 1.5-2 R_J (Divine & Garrett 1983).
   'inner':{'radiation':1500,'grad':2.24,'dist':1.3435,'rad':1.159,'dxy':0.693,'comp':1.0,'ext':1.0,'bdist':3e-4,'brad':0.8889,'bdxy':0.5866},
   # 자기원반 = 적도 전류시트(렌즈형, 반두께 3 = Khurana). 반경 절단 3-24 는 인코딩 선택이다 —
   # 실제 원반은 50 R_J 를 넘어 뻗지만 엔진은 껍질당 세기가 하나뿐이라, 껍질 끝이 선량이 빠지는
   # 자리를 대신한다. 2026-08-18 에 16 → 24 로 옮겼다. 16 에서는 렌즈가 가니메데(14.97) 바로
   # 위에서 반두께 1.40 으로 뾰족해져 그 자리 선량이 물리가 아니라 기하 때문에 71.8 로 떨어졌다.
   'outer':{'radiation':150,'grad':2.15,'dist':2.7016,'rad':3.1729,'dxy':0.054,'comp':1.0021,'ext':0.9938,'bdist':0.0,'brad':4.3547,'bdxy':1.9894},
   # Rutala 2025 S97* 적합: α = 0.28 + 1.08·p_SW, r_SS = 38.0·p_SW^-0.25 [R_J].
   # 노즈 63 R_J(Joy 2002 압축 상태) ⇒ p_SW 0.132 nPa ⇒ α 0.423.
   'pause':{'radiation':-0.01,'rad':84.4649,'comp':1.3407,'ext':0.0089380,'hscale':1.0,
            'shue_alpha':0.423,'shue_nose':63,'shue_tail':9450,
            # α_day ≤ 0.5 라 야간 α 미적용. 일반화 스톡 근사안은 2026-08-16 기각
            #   (이 α 대역에서 꼬리가 +70% 어긋난다).
            'shue_alpha_night':0}},  # nose 63 R_J (Joy 2002)

 # ---- SATURN: 스톡=외대만, 물리=고리가 내대 소거→외대만(축대칭), CRAND 약함 ----
 # 스톡 값 검증: KSP-RO/ROKerbalism Support/RSS.cfg `saturn` 모델 (2026-07-24 재검증)
 # 스톡은 저작값이고 물리 도출이 아니다. 게다가 이 `saturn` 모델 하나를 토성·천왕성·해왕성이
 # 공유한다(세 바디 모두 outer 7/7, pause 20/comp 1.02 → 노즈 19.6).
 # 실측 노즈는 24 R_S, 22-27 이중모드 (Achilleos 2008,
 #   https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A) — 스톡이 18% 작다.
 # 외대 7/7 = 적도 0-14 R_S 로 고리가 쓸어 간 구역까지 채운다 / 실측 셸은 L 2.3-6
 #   (Kollmann 2013, https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K).
 # has_inner=false 는 맞다 — 고리가 내대 자리를 흡수한다 (Cooper 1983,
 #   https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C).
 'saturn_stock':{'title':'Saturn — stock (ROKerbalism RSS.cfg)','sub':'saturn model: outer 7/7 only, pause 20/1.02','R':16,'tilt':0,
   'outer':{'radiation':150,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.011,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 # 도출 사슬(pause): 노즈 24 R_S (Achilleos 2008) + α 0.7358 (Kanani 2010 식 12) →
 #   pause_radius = 노즈·2^α = 39.9677, compression = 2^α = 1.6653,
 #   extension = pause_radius/(150·노즈) = 0.0111020  ← L = 150×노즈 관례(도출 아님).
 # 벨트: fit_belts.py 수치 피팅, 셸 L 2.3-6 = Kollmann 2013.
 'saturn_phys':{'title':'Saturn — physical (SDF fit)','sub':'rings absorb inner belt; CRAND shell L 2.3-6 (IoU .98); ~0° tilt','R':16,'tilt':0.01,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). eps 0.002 → 대칭. grad: 자기 프로파일 근거 없어 CRAND 아날로그(지구 외대)
   'outer':{'radiation':10,'grad':2.15,'dist':2.6173,'rad':2.3184,'dxy':0.6735,'comp':1.0,'ext':0.998,'bdist':0.9889,'brad':0.8883,'bdxy':0.6616},  # 고리 바깥 단일 초승달
   'pause':{'radiation':-0.011,'rad':39.9677,'comp':1.6653,'ext':0.0111020,'hscale':1.0,
            'shue_alpha':0.7358,'shue_nose':24,'shue_tail':3600,
            # 야간 α = α_day × 0.8966 (지구 −0.06 앵커의 비례 확장, 아트 정책). α_day ≤ 0.5 인
            #   바디는 이미 뒤가 좁아지므로 적용하지 않는다 — 수성·목성·폴리페무스가 자동 제외된다.
            # 이 형상을 일반화 스톡(waist/smooth)으로 근사하는 안은 2026-08-16 에 기각했다.
            #   α≈0.5 에서만 맞고 꼬리가 목성급 +70%, 토성급 −42% 로 어긋난다. 두 슬라이더는
            #   원래 용도인 유도 가지(금성·화성)에 남는다.
            'shue_alpha_night':0.6599}},  # nose 24 R_S (Achilleos 2008)

 # ---- URANUS: 극단 tilt 59° + offset 0.3 ----
 # 스톡=generic `saturn` 모델 재사용(외대 7/7만; radiation_inner 75는 has_inner=false라 미사용 죽은 값)
 # 즉 형상은 토성에서 복사된 저작값이고 천왕성용 도출이 아니다. pause 20/comp 1.02 → 노즈 19.6.
 # 실측 노즈는 18.0 R_U (Ness 1986, https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N) —
 #   여기서는 스톡이 9% 크다. 배향(pole_lat 31.4 = 틸트 58.6°, offset 0.3)은 Ness 1986 과 일치한다.
 # 외대 7/7 통짜 blob / 실측은 위성 소거로 갈린 두 셸 L 1.5-5 · 5-10 (Krimigis 1986,
 #   https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K; Cheng 1987,
 #   https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C).
 'uranus_stock':{'title':'Uranus — stock (ROKerbalism RSS.cfg)','sub':'generic saturn model: outer 7/7, pause 20; pole_lat 31.4, offset 0.3','R':22,'tilt':58.6,'offset':0.3,
   'outer':{'radiation':4,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.010,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 # 벨트 구조 경계=위성 L-셸 (Krimigis 1986 Miranda 안쪽 예외역 + Cheng 1987 전자 극소: Miranda 5.1/Ariel 7.5/Umbriel 10.4)
 # 도출 사슬(pause): 노즈 18 R_U (Ness 1986) + α 0.58 (적합 없음 → 지구값 유추, 파일 머리말) →
 #   pause_radius = 노즈·2^α = 26.9073, compression = 2^α = 1.4948,
 #   extension = pause_radius/(150·노즈) = 0.0099653  ← L = 150×노즈 관례(도출 아님).
 'uranus_phys':{'title':'Uranus — physical (SDF fit)','sub':'tilt 59°, offset 0.3; L 1.5-5 / 5-10 Miranda·Umbriel cut (IoU .98/.97)','R':22,'tilt':59,'offset':0.3,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). grad: 프로파일이 위성-소거 극소 사이 넓은 최대(Cheng 1987)라
   # 피크가 껍질 핵심 → 컷 이후 최심점으로 클램프한 하한값. 1.0을 그대로 넣으면 포화 지점이 없어 실효 강도가 0.64배로 깎임.
   'inner':{'radiation':40,'grad':1.57,'dist':2.1836,'rad':1.93,'dxy':0.6732,'comp':1.001,'ext':0.997,'bdist':0.0563,'brad':0.8488,'bdxy':0.3727},
   'outer':{'radiation':8,'grad':1.85,'dist':4.3078,'rad':3.8644,'dxy':0.6644,'comp':1.005,'ext':0.977,'bdist':2.3256,'brad':1.9463,'bdxy':0.7307},
   'pause':{'radiation':-0.010,'rad':26.9073,'comp':1.4948,'ext':0.0099653,'hscale':1.0,
            'shue_alpha':0.58,'shue_nose':18,'shue_tail':2700,
            # 야간 α = α_day × 0.8966 (지구 −0.06 앵커의 비례 확장, 아트 정책). α_day ≤ 0.5 인
            #   바디는 이미 뒤가 좁아지므로 적용하지 않는다 — 수성·목성·폴리페무스가 자동 제외된다.
            # 이 형상을 일반화 스톡(waist/smooth)으로 근사하는 안은 2026-08-16 에 기각했다.
            #   α≈0.5 에서만 맞고 꼬리가 목성급 +70%, 토성급 −42% 로 어긋난다. 두 슬라이더는
            #   원래 용도인 유도 가지(금성·화성)에 남는다.
            'shue_alpha_night':0.52}},  # nose 18 R_U (Ness 1986)

 # ---- NEPTUNE: tilt 47° + offset 0.55, 외곽 Triton 컷 ----
 # 스톡=generic `saturn` 모델 재사용(pause 20 — 26.5 아님; radiation_inner 39 미사용 죽은 값)
 # 형상은 토성에서 복사된 저작값이고 해왕성용 도출이 아니다. pause 20/comp 1.02 → 노즈 19.6.
 # 실측 노즈는 26.5 R_N (Ness 1989, https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N) —
 #   스톡이 26% 작다. 배향(pole_lat 43 = 틸트 47°, offset 0.55)은 Ness 1989 와 일치한다.
 # 외대 7/7 통짜 blob / 실측은 셸 L 1.5-5 · 5-14, 피크 L≈7 (Stone 1989,
 #   https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S), 외곽 컷은 Triton 궤도 ~14 R_N
 #   (Krimigis 1989, https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K).
 'neptune_stock':{'title':'Neptune — stock (ROKerbalism RSS.cfg)','sub':'generic saturn model: outer 7/7, pause 20; pole_lat 43, offset 0.55','R':28,'tilt':47,'offset':0.55,
   'outer':{'radiation':2.5,'grad':2.2,'dist':7.0,'rad':7.0,'comp':1.05,'ext':0.95},
   'pause':{'radiation':-0.007,'rad':20,'comp':1.02,'ext':0.1,'hscale':1.0}},
 # 도출 사슬(pause): 노즈 26.5 R_N (Ness 1989) + α 0.58 (적합 없음 → 지구값 유추) →
 #   pause_radius = 노즈·2^α = 39.6135, compression = 2^α = 1.4948,
 #   extension = pause_radius/(150·노즈) = 0.0099653  ← L = 150×노즈 관례(도출 아님).
 'neptune_phys':{'title':'Neptune — physical (SDF fit)','sub':'tilt 47°, offset 0.55 R_N; shells L 1.5-5 / L 5-14 Triton cut (IoU .98/.97)','R':28,'tilt':47,'offset':0.55,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). grad 외대: 피크 L7 (Stone 1989), 내대: 프로파일 없어 지구 내대 아날로그
   'inner':{'radiation':30,'grad':2.09,'dist':2.1836,'rad':1.93,'dxy':0.6732,'comp':1.0,'ext':0.999,'bdist':0.0563,'brad':0.8488,'bdxy':0.3727},
   'outer':{'radiation':6,'grad':2.63,'dist':5.9998,'rad':5.4076,'dxy':0.6573,'comp':1.004,'ext':0.98,'bdist':2.5862,'brad':1.9982,'bdxy':0.8656},  # peak ~L7, 외곽 ~14(Triton)
   'pause':{'radiation':-0.007,'rad':39.6135,'comp':1.4948,'ext':0.0099653,'hscale':1.0,
            'shue_alpha':0.58,'shue_nose':26.5,'shue_tail':3975,
            # 야간 α = α_day × 0.8966 (지구 −0.06 앵커의 비례 확장, 아트 정책). α_day ≤ 0.5 인
            #   바디는 이미 뒤가 좁아지므로 적용하지 않는다 — 수성·목성·폴리페무스가 자동 제외된다.
            # 이 형상을 일반화 스톡(waist/smooth)으로 근사하는 안은 2026-08-16 에 기각했다.
            #   α≈0.5 에서만 맞고 꼬리가 목성급 +70%, 토성급 −42% 로 어긋난다. 두 슬라이더는
            #   원래 용도인 유도 가지(금성·화성)에 남는다.
            'shue_alpha_night':0.52}},  # nose 26.5 R_N (Ness 1989)

 # ---- MERCURY: 벨트 없음, 초소형 offset 자기권 (표면 직격) ----
 # 스톡은 저작값이고 물리 도출이 아니다(전용 `mercury` 모델). pause 1.6/comp 1.4 → 노즈 1.14.
 # 실측 노즈는 1.45 R_M, 1.35-1.55 (Winslow 2013,
 #   https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) — 스톡이 21% 작다(빡빡한 쪽).
 # 벨트 없음은 맞다 — 자기권이 너무 작고 요동쳐 안정 포획이 안 된다 (Schriver 2015,
 #   https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S). offset 0.208 도 실측 0.198 에 근접.
 'mercury_stock':{'title':'Mercury — stock (ROKerbalism)','sub':'no belt; pause 1.6/1.4 (nose 1.14), pole_lat 96, offset 0.208, deform 0.1','R':3,'tilt':6,'offset':0.208,
   'pause':{'radiation':-0.001,'rad':1.6,'comp':1.4,'ext':0.05,'hscale':1.0,'deform':0.1}},  # pause_deform=0.1 그대로 반영 (2026-08-04 누락 수정): 다중극 경계의 비축대칭 로브
 'mercury_phys':{'title':'Mercury — physical','sub':'no stable belt; mp nose 1.45 R_M, offset 0.20 north, tilt <3°, deform 0.1','R':3,'tilt':2,'offset':0.20,
   # Winslow 2013 은 MESSENGER 통과를 Shue 형식으로 적합했다: R_ss 1.45 R_M, flaring α 0.5
   # 도출 사슬(pause): pause_radius = 노즈·2^α = 2.0506, compression = 2^α = 1.4142,
   #   extension = pause_radius/(150·노즈) = 0.0094280  ← L = 150×노즈 관례(도출 아님).
   # deform 0.1 은 스톡에서 상속(다중극 비축대칭은 실재하나 진폭은 도출하지 않았다).
   'pause':{'radiation':-0.001,'rad':2.0506,'comp':1.4142,'ext':0.0094280,'hscale':1.0,'deform':0.1,
            'shue_alpha':0.5,'shue_nose':1.45,'shue_tail':217.5,
            # α_day ≤ 0.5 라 야간 α 미적용.
            # 2026-08-17 주석 정정: "일반화 스톡은 이 α 대역에서 꼬리가 +70% 어긋난다"고
            #   적혀 있었는데, +70% 는 목성(α 0.423)의 값이고 수성이 아니다. α 0.5 는
            #   일반화 스톡이 Shue 를 표현할 수 있는 바로 그 지점이다.
            #   그래서 Shue-native 와 일반화 스톡 계획을 둘 다 들고 간다.
            # 2026-08-18: 수기 적합(waist 0.0777 / smooth 4.2533, rms 3.4e-3)을 닫힌 해로 교체.
            #   α 0.5 에서 두 곡면은 근사가 아니라 같은 곡면이고 waist 가 0 이다
            #   (scripts/refs/fit_generalized_pause.py). 노즈 1.45·꼬리 217.5 는 그대로.
            'pending_rad':2.8808,'pending_comp':1.0,'pending_ext':0.013333,
            'pending_waist':0.0,'pending_smooth':4.1015,
            'shue_alpha_night':0}},  # nose 1.45 R_M (Winslow 2013); deform 유지 — 실제 자기장이 offset dipole + 고차 다중극

 # ---- VENUS: 다이나모 없음 → 유도 자기권(전리층 pause만, 벨트 없음) ----
 # ROKerbalism: RadiationBody[Eve]→Venus, radiation_model = ionosphere, radiation_pause = -0.005.
 # ionosphere 모델 = pause_radius 1.1 / extension 0.2 (System/Radiation.cfg). 벨트 필드 자체가 없다.
 # 이 `ionosphere` 모델도 저작값이고 금성 실측에서 도출된 값이 아니다(Titan 과 공유).
 # 실측 이오노포즈는 직하 1.055 · 명암경계선 1.140 R_V (Brace 1980,
 #   https://ui.adsabs.harvard.edu/abs/1980JGR....85.7663B) — 스톡의 균일 1.1 은 앞쪽이 헐겁다.
 # 꼬리는 스톡이 1.1/0.2 = 5.5 R_V 에서 닫히는데, 확정 IMB 횡단은 20 R_V 까지 있다
 #   (Edberg 2024, https://ui.adsabs.harvard.edu/abs/2024JGRA..12932603E).
 'venus_stock':{'title':'Venus — stock (ROKerbalism)','sub':'ionosphere model: pause 1.1/ext 0.2, no belts (induced magnetosphere)','R':22,'tilt':0,
   'pause':{'radiation':-0.005,'rad':1.1,'ext':0.2,'hscale':1.0}},

 # phys = 방법론 Part A '유도 자기권' 절로 계산. 이오노포즈는 실측 스케일을 쓴다(압력균형이 열압 대
 # 항성풍이라 ^(1/6) 법칙 부적용). Brace 1980(PVO): 평균 이오노포즈 직하 330 km, 황혼 700 km,
 # 새벽 1000 km → R_V 6051.8 km 기준 nose 1.0545, 명암경계선 평균 1.1405 R_V.
 # Kerbalism 의미론: pause_radius=플랭크=1.140, compression=플랭크/노즈=1.081 (→ 노즈 1.0545 복원),
 # extension=플랭크/꼬리=0.057 (꼬리 20 R_V = Edberg 2024 의 최원거리 확정 IMB 횡단).
 # 벨트 없음(고유 다이나모 부재), radiation_pause 는 유도 경계라 쌍극보다 약한 스톡 스케일 -0.005 유지.
 # 정책(오너 결정 2026-08-14): 인게임 형상은 가능한 한 Shue 로 통일하고, Shue 가 기하적으로
 # 불가능한 경우에만 스톡 함수를 두 필드로 일반화해 쓴다. 금성·화성이 그 예외다 — 유도 경계는
 # 허리가 좁고 꼬리가 벌어지는데 Shue 는 α 하나가 둘을 겸해 어떤 값에서도 못 만든다(주간면을
 # 맞추면 후류가 −83~−100% 로 소멸). 적합된 α 가 있는 지구·수성·목성은 Shue 를 그대로 쓴다. smooth=waist=0 이면 스톡과 바이트 동일.
 #   waist  : 두 반구를 가르는(=최대 단면) 평면의 x 위치. + 는 항성 방향. 스톡은 0 고정.
 #   smooth : x=0 의 기울기 점프(C0 이고 C1 아님)를 쌍곡선으로 뭉개 C∞ 로 만든다.
 # 요구사항: 뒤쪽이 불룩해지지 않을 것. 폭은 √(rad²−g²) 이므로 rad 를 넘을 수 없다 →
 # rad = 명암경계선 폭으로 두면 최대폭이 정확히 그 값이고 뒤로는 단조 감소한다(불룩함 0.000%).
 # comp/ext 는 노즈와 꼬리끝에 맞춰 풀었다: 노즈 1.0545 정확, 폭 상한 = 실측 명암경계선.
 # smooth 는 적합으로 결정되지 않는다(RMS 가 거의 평평). 관례로 smooth = 0.5×rad 를 쓴다 —
 # 금성·화성·수성에서 독립적으로 구한 얕은 최적점이 0.50·0.54·0.57×rad 로 일치한다. 도출이 아니라
 # 관례이고, comp 는 그 smooth 에서 노즈가 정확해지도록 다시 풀었다. 폭 상한이 rad 라 대가는 없다.
 # 최대폭 평면은 스톡(waist=0)에서는 x=0 이지만 smooth 를 켜면 −½(comp−ext)·smooth/√(comp·ext)
 # 로 하류에 놓인다(여기서 −3.35 R_V). 그래서 x=0 단면은 상한 1.140 이 아니라 1.1034 —
 # Brace 의 명암경계선 1.1405 보다 3.3% 좁다. 불룩함 금지(폭 ≤ 실측 명암경계선)를 지키는 대가이고,
 # waist 로 최대폭 평면을 x=0 까지 끌어오는 것은 이 꼬리 길이에서는 불가능하다(노즈가 무너진다).
 # 후류 폭은 실측 원뿔(Martinecz 2009 / Edberg 2024, arXiv:2410.21856)보다 좁다(d2 −15%,
 # d5 −33%, d10 −54%). 불룩함 금지가 우선이라 받아들인 값이다. 방법론 Part A 참조.
 # 도출 사슬(pause): rad = 명암경계선 1.14 R_V (Brace 1980), comp 1.0123576 = 그 smooth 에서 노즈
 #   1.0545 가 정확해지도록 |px| = rad 를 닫힌형으로 푼 값, ext = rad/(150·노즈) = 0.0072072
 #   → 꼬리 158 R_V. (2026-08-17: 옛 comp 1.0151 은 노즈를 1.0513 으로 놓아 0.31% 어긋나 있었다.
 #    스톡 항등식 rad/comp 는 smooth 가 켜지면 성립하지 않는다 — belt-viewer 의 pauseNoseTail 참조.)
 #   (위 문단의 "꼬리 20 R_V" 는 L 관례 확정 전 표현이다. 20 R_V 는 확정 IMB 횡단의 최원거리
 #    하한이고, 158 은 그 하한을 넘기는 L = 150×노즈 관례값이다.)
 'venus_phys':{'title':'Venus — physical (induced)','sub':'generalized stock pause: nose 1.0545 exact, cap 1.1405 = terminator, tail 158 R_V','R':22,'tilt':0,
   'pause':{'radiation':-0.005,'rad':1.14,'comp':1.0123576,'ext':0.0072072,'hscale':1.0,
            'smooth':0.57,'waist':0.0}},

 # ---- MARS: 지각 잔류 자기(다극·약장) → irregular 모델 (pause_deform 0.1 로 울퉁불퉁) ----
 # 업스트림 Kerbalism: RadiationBody[Duna] = irregular, radiation_pause = -0.003.
 # ROKerbalism 의 RSS.cfg 는 +RadiationBody[Duna]{@name = Mars} 로 복사하지만, 그들 자신의
 # System/Radiation.cfg 에는 Duna 정의가 없다 → 그 조합에서는 화성에 RadiationBody 가 안 생긴다(배포 갭).
 # 이 `irregular` 모델도 저작값이고 화성 실측 도출이 아니다. pause 1.25/comp 1.1 → 노즈 1.14.
 # 실측 MPB 는 직하 1.29 ± 0.04 · 명암경계선 1.47 ± 0.08 R_M (Vignes 2000,
 #   https://ui.adsabs.harvard.edu/abs/2000GeoRL..27...49V) — 스톡이 앞도 옆도 작다.
 # 꼬리는 스톡이 1.25/0.75 = 1.7 R_M 에서 닫힌다(유도 자기꼬리 실측 대비 훨씬 짧다).
 'mars_stock':{'title':'Mars — stock (Kerbalism irregular)','sub':'irregular model: pause 1.25/comp 1.1/ext 0.75/deform 0.1 — crustal-anomaly look; no belts','R':22,'tilt':0,
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
 # 도출 사슬(pause): rad = 명암경계선 1.47 R_M (Vignes 2000), comp 1.0601082 = smooth 0.735 에서
 #   노즈 1.29 가 정확해지도록 |px| = rad 를 닫힌형으로 푼 값, ext = rad/(150·노즈) = 0.0075969
 #   → 꼬리 194 R_M (L 관례). 금성과 같은 이유로 x=0 단면은 상한 1.47 이 아니라 1.4182 (−3.5%).
 #   (2026-08-17: 옛 comp 1.0684 는 노즈를 1.2785 로 놓아 Vignes 의 1.29 에서 0.89% 어긋나 있었다.
 #    문서에 남아 있던 "노즈 1.285" 는 목표가 아니라 그 어긋난 값이었다.)
 'mars_phys':{'title':'Mars — physical (MPB fit)','sub':'generalized stock pause: nose 1.29 exact, cap 1.47 = terminator, tail 194 R_M','R':22,'tilt':0,
   'pause':{'radiation':-0.003,'rad':1.47,'comp':1.0601082,'ext':0.0075969,'hscale':1.0,'deform':0.1,
            'smooth':0.735,'waist':0.0}},

 # ---- EARTH: 앵커 (스톡=튜닝 모델) vs 물리 (standoff 10, 외대 heart L~4.5) ----
 # 스톡은 저작값이지만 이 바디에서는 저작자가 제대로 맞췄다(전용 `earth` 모델).
 # pause 15/comp 1.5 → 노즈 10 R_E = 실측 standoff 와 일치 (Shue 1998,
 #   https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S; Fairfield 1971).
 # 내대 적도 1.29-2.0 R_E ↔ 실측 피크 L≈1.5 (Ripoll 2016,
 #   https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R), 외대 3.45-6.0 ↔ heart L 4-5, L 3-7
 #   (Reeves 2013, https://ui.adsabs.harvard.edu/abs/2013Sci...341..991R) — 슬롯까지 성격이 맞다.
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
   # 도출 사슬(pause): 노즈 10 R_E (Shue 1997/1998) + α 0.58 (Shue 1998 식 11) →
   #   pause_radius = 노즈·2^α = 14.9485, compression = 2^α = 1.4948,
   #   extension = pause_radius/(150·노즈) = 0.0099653  ← L = 150×노즈 관례(도출 아님).
   'pause':{'radiation':-0.01,'rad':14.9485,'comp':1.4948,'ext':0.0099653,'hscale':1.0,
            'shue_alpha':0.58,'shue_nose':10,'shue_tail':1500,
            # 야간 α = α_day × 0.8966 (지구 −0.06 앵커의 비례 확장, 아트 정책). α_day ≤ 0.5 인
            #   바디는 이미 뒤가 좁아지므로 적용하지 않는다 — 수성·목성·폴리페무스가 자동 제외된다.
            # 이 형상을 일반화 스톡(waist/smooth)으로 근사하는 안은 2026-08-16 에 기각했다.
            #   α≈0.5 에서만 맞고 꼬리가 목성급 +70%, 토성급 −42% 로 어긋난다. 두 슬라이더는
            #   원래 용도인 유도 가지(금성·화성)에 남는다.
            'shue_alpha_night':0.52}},  # nose 15/1.5=10 R_E — 스톡과 동일(스톡이 이미 정확)

 # ---- GANYMEDE: 약장 임베디드 미니자기권 (Kivelson 2002: 719nT, standoff ~2 R_G, open caps) ----
 # 스톡은 저작값이고 물리 도출이 아니다(전용 `ganymede` 모델). 계면 자체가 없다(has_pause 미정의).
 # 실측은 상류 standoff ~2 R_G, 폭 5.5 R_G 의 자기권이 실재한다 (Kivelson 1998,
 #   https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K) — 스톡의 가장 큰 누락.
 # 내대 0.8/0.6 / 실측은 폐자력선 벨트 L 1.1-1.9, 표면에서 흡수 (Allioux 2013,
 #   https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A).
 'ganymede_stock':{'title':'Ganymede — stock (ROKerbalism)','sub':'inner 0.8/0.6, no pause defined','R':4,'tilt':4,
   'inner':{'radiation':0.33,'grad':3.3,'dist':0.8,'rad':0.6}},
 'ganymede_phys':{'title':'Ganymede — physical (SDF fit)','sub':'719 nT dipole; closed-line belt L 1.1-1.9, surface-absorbed (IoU .97); mp sphere r=2.0 R_G, no tail (Alfven wings)','R':4,'tilt':4,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). eps 0.139(작은 standoff의 큰 몫을 벨트가 채움)이라
   # 도출 comp 1.052가 배포값 1.05를 되찾음 — 이 바디가 비대칭 레시피의 검증 앵커다.
   'inner':{'radiation':0.33,'grad':2.09,'dist':0.8758,'rad':0.7327,'dxy':0.715,'comp':1.052,'ext':0.958,'bdist':0.0222,'brad':0.9408,'bdxy':0.8693},  # 무대기 → 컷=표면(r=1.0)
   # 도출 사슬(pause): 실측 직하 standoff 2.0 R_G (Kivelson 1998) 를 그대로 반지름으로 삼은 구다 →
   # rad 2.0, comp = ext = hscale = 1.0. 다른 바디의 노즈·2^α 사슬을 쓰지 않는다(아래 이유).
   # 정직하게 적자면 실제 경계는 구가 아니다 — Kivelson 1998 은 노즈 2 R_G, 폭 5.5 R_G 를 주므로
   # 플랭크는 2.75 R_G 이고, standoff 반지름의 구는 옆구리를 약 27% 작게 그린다. 그럼에도 구를
   # 택한 이유는 둘이다. (1) 실제 형상을 지배하는 것은 흐름에 거의 수직으로 뻗은 알프벤 날개인데
   # (Kivelson 2013, https://ui.adsabs.harvard.edu/abs/2013AGUFMSM12B..01K — "Alfvén wings
   # stretched almost transverse to the upstream flow replacing tail lobes folded back in the
   # flow direction"), 엔진의 형상족(압축/신장 두 계수로 눌린 구)은 날개를 아예 표현하지 못한다.
   # 어떤 값을 넣어도 옳아지지 않는 축이라 플랭크를 맞추는 편평 구가 더 정확하지도 않다.
   # (2) 그 편평 구는 3D 뷰에서 흐름축으로 눌린 원반처럼 읽혔고, 얻는 것 없이 오해만 만들었다.
   # 꼬리는 여전히 없다 — 가니메데는 태양계에서 유일하게 아음속이 아니라 sub-Alfvénic 흐름 안에
   # 자기권이 서고, 그런 흐름은 뒤로 접힌 꼬리 로브를 만들지 않는다. 그래서 ext = comp 로 야간면을
   # 주간면과 대칭으로 닫고(닫힘 2.0 R_G = 노즈와 같음), 이 바디에는 L = 150×노즈 관례도 적용하지
   # 않는다(파일 머리말의 제외 항목).
   # 계획값(⚗): α 0.5 라 일반화 스톡이 이 경계를 표현할 수 있다. 2026-08-18 에 수기 적합
   #   (waist 0.0558 / smooth 6.2441, rms 4.7e-3)을 닫힌 해로 교체했다 — α 0.5 에서 두 곡면은
   #   근사가 아니라 같은 곡면이고 waist 가 0 이라, compression 이 1.0 으로 은퇴하는 것도
   #   관례가 아니라 정확한 값이다(scripts/refs/fit_generalized_pause.py).
   'pause':{'radiation':-0.01,'rad':2.9834,'comp':1.4142,'ext':0.12826,'hscale':1.0,
            'pending_rad':3.8683,'pending_comp':1.0,'pending_ext':0.179943,
            'pending_waist':0.0,'pending_smooth':6.0411}},  # 2026-08-17: 구 → M_A 로 줄인 Shue 꼬리 (L = 150^M_A x nose, M_A 0.479 → 11.03x)

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
 # 도출 사슬(pause): 노즈 7 R_d = Chapman-Ferraro (위 계산). comp 1.5 · ext 0.07474 는 지구 스톡
 #   pause 형상(15/1.5)을 그대로 스케일한 값이고 이 바디의 α 는 적합되지 않았다 — 근거 미확인.
 'proxima_d_pre':{'title':'Proxima Cen d — pre-regate board','sub':'B_p 16 G → mp nose ~7 R_d (4-18 over 3-280 G); shells L 1.2-2 / 3-5.5; dose anchor-interp (low conf); tilt unknown (10° drawn)','R':12,'tilt':10,
   # grad/comp/ext = 방법론 Part C 도출값 (2026-08-13). 지구 프리셋서 복사돼 있던 comp/ext를 교체:
   # 외대 핵심이 nose의 47%(eps 0.107)라 이 바디는 실제로 비대칭이어야 한다 → 1.053/0.901. grad는 지구 아날로그.
   'inner':{'radiation':5000,'grad':2.09,'dist':0.9413,'rad':0.7698,'dxy':0.7314,'comp':1.002,'ext':0.996,'bdist':1e-4,'brad':1.0,'bdxy':1.0},  # 무대기 → 하부 컷=표면 r=1.0 (지구 1000km loss-cone 경계는 대기 흡수 산물이라 부적용)
   'outer':{'radiation':1000,'grad':2.15,'dist':2.7,'rad':2.3,'dxy':0.662,'comp':1.053,'ext':0.901,'bdist':1.2,'brad':1.0,'bdxy':0.6748},  # L 3-5.5 (nose 7 안쪽)
   'pause':{'radiation':-0.01,'rad':10.5,'comp':1.5,'ext':0.07474,'hscale':1.1}},  # nose 10.5/1.5 = 7 R_d

 # 재게이트: 노즈 7.517 = Chapman-Ferraro (B_eq 800 uT vs 5648 nPa, Garraffo 하한을 b 에서 r^-2 내삽).
 #   기록값 7 이 이제 재현된다 — 구 도출은 어느 압력으로도 7 을 주지 못했다(보드 스케일링은 11.33).
 # alpha 0.58 = 지구 유추. b 는 standoff 가 수성 범위라 수성을, d 는 지구 범위라 지구를 받는다.
 # 오너 결정으로 알펜 날개 가지는 적용하지 않는다. 다만 d 의 자기장 근거인 SPI 위상고정 플레어는
 #   sub-Alfvenic 결합을 요구하므로, 채택 형상과 채택 근거가 어긋난다는 점은 보드에 기록돼 있다.
 # ================= NEARSTARS — 2026-08-16 자기권계면 재게이트 (전/후 비교) =================
 # 짝지어 읽는다: *_pre = 재게이트 전 보드값, *_regate = 방법론대로 다시 구한 값.
 # 도출·근거는 phase4/magnetopause-regate/context-notes.md, 재현은
 #   scripts/refs/magnetopause_geometry.py.

 # ---- POLYPHEMUS (Alpha Centauri A b): 노즈가 magnetodisc 팽창으로 23.5 → 35.33 ----
 # 진공 쌍극자 Chapman-Ferraro 는 22.14 를 준다. 목성에서 Rutala 2025 실측피팅이 그 식을
 #   1.6-2.0배 넘어서므로(디스크가 경계를 밀어낸다) 같은 압력에서의 인자 1.596 을 곱했다.
 # alpha 0.42 = 목성 피팅 상한 클램프. 선형 외삽하면 0.702 지만 보정범위 3배 밖이다.
 'polyphemus_pre':{'title':'Polyphemus — pre-regate board','sub':'nose 23.5 (unreproducible), comp 1.2 (no fitted alpha), hs 1.1','R':50,'tilt':10,
   'inner':{'radiation':300,'grad':1.65,'dist':1.3793,'rad':1.159,'dxy':0.7142,'comp':1.0,'ext':1.0,'bdist':0.2656,'brad':0.7491,'bdxy':0.6384},
   'outer':{'radiation':30,'grad':2.15,'dist':4.2824,'rad':3.8588,'dxy':0.659,'comp':1.002,'ext':0.989,'bdist':2.0738,'brad':1.6687,'bdxy':0.8079},
   'pause':{'radiation':-0.01,'rad':28.2,'comp':1.2,'ext':0.05,'hscale':1.1}},
 # ---- PANDORA (A b III): Shue 꼬리 → 알펜 날개 정구 ----
 # 3.53 R_p 궤도는 sub-Alfvenic 이다(M_A=1 이려면 Io 토러스 피크의 216배가 필요).
 #   sub-Alfvenic 흐름은 활머리충격파도 끌린 꼬리도 만들지 않는다 — 가니메데와 같은 판정.
 # standoff 도 다시 구했다: 모체 자기압 5.943 uPa 가 램압 0.001 uPa 를 6000배 압도하는데
 #   구값 2.6 은 램압만으로 균형을 잡고 있었다 → 3.386.
 'pandora_pre':{'title':'Pandora — pre-regate board','sub':'standoff 2.6 from ram alone; ext 0.6 draws a tail the flow cannot make','R':6,'tilt':10,
   'inner':{'radiation':4.0,'grad':2.09,'dist':1.0193,'rad':0.8489,'dxy':0.7196,'comp':1.015,'ext':0.961,'bdist':0.0971,'brad':0.9349,'bdxy':0.8829},
   'pause':{'radiation':-0.01,'rad':2.99,'comp':1.15,'ext':0.6,'hscale':1.0}},
 # ---- PROXIMA CEN b: 스톡 irregular 템플릿 → 수성 아날로그 Shue ----
 # 구값은 dynamo 가 '없는' 화성 잔류 지각자기용 템플릿이라 b 자신의 활성 dynamo 행과 모순이었다.
 #   게다가 템플릿 1.25/1.1 은 노즈 1.14 를 주는데 보드 기록 standoff 는 1.54 였다.
 # standoff 1.54 가 수성 1.45 와 거의 같고, 수성은 Shue alpha 가 피팅된 유일한 소형 자기권이다
 #   (0.5, Winslow 2013, https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W).
 # PANDORA 재게이트 프리셋은 여기 두지 않는다 — 판도라는 phase4 보드에서
 # load_nearstars_specs() 로 자동 유입된다(build_belt_viewer.py). 손 프리셋을 나란히 두면
 # 출처가 둘이 되어 보드를 고칠 때 갈라진다. 태양계는 이 표, NearStars 는 보드가 단일 출처.
 'proxima_b_pre':{'title':'Proxima Cen b — pre-regate board','sub':'stock irregular template (Mars crustal, no dynamo); template nose 1.14 vs recorded standoff 1.54','R':3,'tilt':30,'offset':0.25,
   'pause':{'radiation':-0.005,'rad':1.25,'comp':1.1,'ext':0.75,'hscale':1.0,'deform':0.1}},
 # ---- PROXIMA CEN c: alpha 0.5 → 0.58, 꼬리 125 → 1791 ----
 # 노즈는 그대로 재현된다(11.942 대 기록 11.905). 움직인 것은 alpha 뿐이다.
 # 빙거성 대체값을 지구 피팅값으로 확정: 보이저 2호가 천왕성·해왕성을 측정된 자기권 중 가장
 #   비어 있는 것으로 확인했고(Bridge 1986 / Belcher 1989), Io·엔켈라두스급 공급원이 없으니
 #   적재량이 가스자이언트보다 지구 쪽에 가깝다. 피팅이 아니라 유추다.

 # b·d 재게이트판은 2026-08-18 에 삭제했다. 이 자리에 손으로 둔 이유가 "보드에 기록은 됐지만 emitter
 # 가 안 읽어서 눈으로 볼 길이 여기뿐"이었는데, 두 축 병합(2026-08-16)과 kopernicus_name 소급 적용으로
 # 그 값들이 보드에서 그대로 cfg 로 나가고 뷰어도 보드 프리셋으로 그린다. 사본을 남기면 갈라진다.
 'proxima_c_pre':{'title':'Proxima Cen c — pre-regate board','sub':'alpha 0.5 borrowed from Earth; tail 125 by judgement','R':22,'tilt':50,'offset':0.4,
   'inner':{'radiation':8.0,'grad':2.09,'dist':1.5,'rad':0.86,'dxy':0.66,'comp':1.002,'ext':0.997,'bdist':0.0001,'brad':1.0,'bdxy':0.5},
   'outer':{'radiation':1.2,'grad':2.15,'dist':2.8,'rad':2.5,'dxy':0.66,'comp':1.01,'ext':0.979,'bdist':1.54,'brad':1.42,'bdxy':0.66},
   'pause':{'radiation':-0.01,'rad':16.84,'comp':1.414,'ext':0.135,'hscale':1.0}},
}

if __name__=='__main__':
    import sys
    only=sys.argv[1:] if len(sys.argv)>1 else None
    for k,b in BODIES.items():
        if only and k not in only: continue
        render(b, os.path.join(OUT,k+'.png'))
