# 검증된 벨트 데이터(render_belts_bodies.BODIES)를 인터랙티브 뷰어 템플릿에 주입해 docs/belt-viewer.html 생성
import json
import math
import os
import re
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from render_belts_bodies import BODIES  # noqa: E402

TEMPLATE = os.path.join(D, 'belt_viewer_template.html')
OUT = os.path.join(D, '..', '..', 'docs', 'belt-viewer.html')

KO = {'venus': '금성', 'mars': '화성', 'earth': '지구', 'jupiter': '목성', 'saturn': '토성', 'uranus': '천왕성',
      'neptune': '해왕성', 'mercury': '수성', 'ganymede': '가니메데',
      'proxima_d': '프록시마 d',
      # NearStars 재게이트 짝 — 그룹 토글이 '재게이트 전 / 후'로 읽힌다
      'polyphemus': '폴리페무스', 'pandora': '판도라',
      'proxima_b': '프록시마 b', 'proxima_c': '프록시마 c'}
EN = {'venus': 'Venus', 'mars': 'Mars', 'earth': 'Earth', 'jupiter': 'Jupiter', 'saturn': 'Saturn', 'uranus': 'Uranus',
      'neptune': 'Neptune', 'mercury': 'Mercury', 'ganymede': 'Ganymede',
      'proxima_d': 'Proxima d',
      'polyphemus': 'Polyphemus', 'pandora': 'Pandora',
      'proxima_b': 'Proxima b', 'proxima_c': 'Proxima c'}
OFF_BELT = {'on': False, 'radiation': 0, 'dist': 1, 'rad': 0.5}

# ---- 궤도 고리 오버레이 ----
# 자기꼬리 길이를 위성계·모천체 궤도와 견주기 위한 오버레이이고, 물리 계산에는 쓰이지 않는다.
# 둘 다 body_key 로 붙는다. NearStars 쪽은 손으로 키를 적어 두면 body_key 가 바뀔 때 조용히
# 빠지므로(2026-08-18 에 kopernicus_name 소급 적용이 전부 떨어뜨렸다) 보드에서 계산한다.
AU_KM, R_EARTH_KM, R_JUP_KM = 1.495978707e8, 6371.0, 71492.0
# 폴리페무스 반경 = 1.0 R_Jup — Phase 3 리포트의 채택값(고리 모델 반경, Beichman §5.3).
R_POLY_KM = 1.0 * R_JUP_KM

# 위성 궤도 반장축(모행성 반경 단위). 태양계는 실측, A b 계는 보드/설정 앵커.
MOON_ORBITS = {
    'earth': [('Moon', 60.34)],
    'mars': [('Phobos', 2.77), ('Deimos', 6.92)],
    'jupiter': [('Io', 5.90), ('Europa', 9.39), ('Ganymede', 14.97), ('Callisto', 26.33)],
    'saturn': [('Enceladus', 3.95), ('Rhea', 8.75), ('Titan', 20.27), ('Iapetus', 59.08)],
    'uranus': [('Miranda', 5.12), ('Ariel', 7.53), ('Umbriel', 10.49),
               ('Titania', 17.20), ('Oberon', 23.01)],
    'neptune': [('Triton', 14.41), ('Nereid', 223.94)],
    'alpha_centauri_a_b': [('Dante', 1.54), ('Hades', 2.07), ('Pandora', 3.53),
                           ('Cassandra', 8.40), ('Chaos', 21.0)],
}

# 바디 자신의 모천체 궤도 반경(그 바디의 반경 단위) + 모천체 이름. 기본 줌에서는 늘 화면 밖이고,
# 사용자가 축소해 자기꼬리와 한 프레임에 담는 것이 이 오버레이의 목적이다.
BODY_ORBITS = {
    'mercury':  (23733, '태양', 'Sun'),
    'venus':    (17880, '태양', 'Sun'),
    'earth':    (23481, '태양', 'Sun'),
    'mars':     (67239, '태양', 'Sun'),
    'jupiter':  (10890, '태양', 'Sun'),
    'saturn':   (23786, '태양', 'Sun'),
    'uranus':   (113360, '태양', 'Sun'),
    'neptune':  (182699, '태양', 'Sun'),
    'ganymede': (406, '목성', 'Jupiter'),
    'alpha_centauri_a_b': (3348, '알파 센타우리 A', 'Alpha Cen A'),   # 1.6 AU
}


def _add_board_orbits():
    """보드에서 NearStars 천체의 궤도 고리를 채운다.

    행성은 orbit 축의 semi_major_axis_au 와 bulk 축의 radius 로, A b 의 위성은 위의
    MOON_ORBITS(모행성 반경 단위)와 각자의 bulk radius 로 환산한다. 손 표를 두지 않는 이유는
    body_key 가 보드 body 키에서 나오기 때문이다 — 이름이 한 번 바뀌면 손 표는 말없이 빠진다.
    """
    import yaml as _yaml
    for fn, star_ko, star_en in (('proxima_cen.yaml', '프록시마 센타우리', 'Proxima Cen'),
                                 ('alpha_centauri.yaml', '알파 센타우리 A', 'Alpha Cen A')):
        doc = _yaml.safe_load(open(os.path.join(D, '..', '..', 'phase4', fn)))
        a_au, rad = {}, {}
        for row in doc.get('decisions', []):
            for fl in row.get('fields', []):
                if fl.get('name') == 'semi_major_axis_au' and row.get('axis') == 'orbit':
                    a_au[row['body']] = fl.get('value')
                if fl.get('name') == 'radius' and row.get('axis') == 'bulk':
                    rad[row['body']] = (fl.get('value'), fl.get('unit'))
        desig = designations(fn)
        for body, a in a_au.items():
            r, unit = rad.get(body, (None, None))
            if not (a and r) or unit not in ('R_earth', 'km'):
                continue                      # 별(R_sun)과 단위 없는 행은 대상이 아니다
            if ROMAN.search(desig.get(body, body)):
                continue                      # 위성 — 모천체가 별이 아니라 제 행성이다
            r_km = r * R_EARTH_KM if unit == 'R_earth' else r
            key = body.lower().replace(' ', '_')
            BODY_ORBITS.setdefault(key, (round(a * AU_KM / r_km), star_ko, star_en))
    # A b 의 위성: 모행성 반경 단위 궤도 → 위성 자신의 반경 단위
    doc = _yaml.safe_load(open(os.path.join(D, '..', '..', 'phase4', 'alpha_centauri.yaml')))
    moon_rad = {row['body']: fl.get('value')
                for row in doc.get('decisions', []) if row.get('axis') == 'bulk'
                for fl in row.get('fields', [])
                if fl.get('name') == 'radius' and fl.get('unit') == 'km'}
    for name, a_parent in MOON_ORBITS['alpha_centauri_a_b']:
        if name in moon_rad:
            BODY_ORBITS.setdefault(name.lower(), (round(a_parent * R_POLY_KM / moon_rad[name]),
                                                  '폴리페무스', 'Polyphemus'))


# 호출은 ROMAN / designations() 가 정의된 뒤로 미룬다(아래 _desig_cache 앞).

# Shue 기준선은 α 가 실제로 근거 있는 바디에서만 기본 표시한다.
# log2(pause_compression) 환산은 지구형 cfg 에서만 형상 충실이고(방법론 Part C),
# 자이언트에 쓰면 flank/nose 1.2 = 지구보다 덜 벌어진 주간면이라는 비물리 값이 된다.
# 2026-08-14: 여섯 자기화 천체 모두 α 가 확보됐다(수성·지구·목성·토성 = 전문 검증 적합,
# 천왕성·해왕성 = 지구 유추). α 는 BODIES 의 pause 딕트에 shue_alpha 로 직접 들어 있고 아래에서
# 읽는다. 이 표는 남겨두지만 목성 외에는 딕트 값이 우선한다(방법론 Part A 표 참조).
SHUE_GROUNDED = {
    # body: (α, nose r0, tail L, 출처)
    'earth': (0.58, 10, 200, 'Shue 1998'),
    'mercury': (0.5, 1.45, 0, 'Winslow 2013 (MESSENGER 통과 적합: R_ss 1.45 R_M, α 0.5)'),
    # 목성: Rutala 2025 의 S97* 적합. α = 0.28 + 1.08·p_SW, r_SS = 38.0·p_SW^-0.25 [R_J].
    # 우리 프리셋 노즈 63 R_J(Joy 2002 압축 상태)를 그 r_SS 관계에 넣으면 p_SW 0.132 nPa → α 0.423.
    # 금성·화성은 여기 두지 않는다 — α 가 BODIES 의 pause 딕트에 직접 들어 있고 아래에서 읽는다.
    'jupiter': (0.423, 63, 0, 'Rutala 2025 S97* (α=0.28+1.08·p_SW, 노즈 63 R_J ⇒ p 0.132 nPa)'),
}


def conv(key, b):
    body, kind = key.rsplit('_', 1)
    # NearStars 재게이트 프리셋은 stock/phys 대신 pre/regate 로 짝짓는다. 뜻은 같은 축이라
    # (저작·상속값 대 물리 도출값) 기존 두 그룹 토글에 그대로 태운다.
    kind = {'pre': 'stock', 'regate': 'phys'}.get(kind, kind)
    # 그룹 라벨이 stock/phys 를 이미 말해주므로 버튼에는 천체명만 남긴다.
    p = {'label': KO[body], 'label_en': EN[body],
         'group': 'stock' if kind == 'stock' else 'phys',
         'view': {'R': b['R'], 'tilt': abs(b.get('tilt', 0)), 'z': 0,
                  'offset': b.get('offset', 0)}}
    for belt in ('inner', 'outer'):
        p[belt] = dict(b[belt]) if b.get(belt) else dict(OFF_BELT)
    p['pause'] = dict(b['pause']) if b.get('pause') else {'on': False, 'rad': 5}
    return p


SYS_LABEL = {'alpha_centauri': ('알파 센타우리', 'Alpha Centauri'),
             'proxima_cen': ('프록시마 센타우리', 'Proxima Centauri')}

SOL_KO, SOL_EN = '태양계', 'Solar System'

# 재게이트 전 스냅샷. 현재값은 phase4 보드에서 자동으로 실리므로(아래 load_nearstars_specs 블록)
# 여기 손으로 두는 것은 '무엇이 어떻게 바뀌었나'를 나란히 보기 위한 비교판뿐이다. 이 표가 그 스냅샷을
# 태양계 탭이 아니라 제 계 탭으로 보내고, 보드판과 같은 body_key 로 묶어 stock/phys 토글에 태운다.
# key = BODIES 의 body_key, 값 = (계, 표시명, depth, 보드 프리셋과 묶일 body_key)
# 네 번째 항목이 필요한 이유: 보드 프리셋은 kopernicus 이름을 소문자화해 키를 잡으므로
# 같은 천체라도 이름이 다를 수 있다(Proxima Cen c → proxima_cen_c).
NEARSTARS_PRE = {
    # 넷째 항목은 보드의 body 키에서 나온 body_key 다(문화명이 아니라 보드가 그 천체를 부르는 이름).
    # 폴리페무스는 보드가 'Alpha Centauri A b' 로 키를 잡는다.
    'polyphemus': ('alpha_centauri', 'Alpha Centauri A b', 0, 'alpha_centauri_a_b'),
    'pandora':    ('alpha_centauri', 'Pandora', 1, 'pandora'),
    # b·d 는 2026-08-18 까지 보드 키(proxima_cen_b/d)가 아니라 제 BODIES 키로 묶여 있어서
    # 피커에 같은 이름 버튼이 두 개씩 떴다(c 만 제대로 묶여 있었다). 넷째 항목은 반드시
    # 보드 프리셋의 body_key 여야 stock/phys 토글 한 쌍으로 합쳐진다.
    'proxima_b':  ('proxima_cen', 'Proxima Cen b', 0, 'proxima_cen_b'),
    'proxima_c':  ('proxima_cen', 'Proxima Cen c', 0, 'proxima_cen_c'),
    'proxima_d':  ('proxima_cen', 'Proxima Cen d', 0, 'proxima_cen_d'),
}
# 합치고 나면 *_regate 두 개는 피커에서 밀려난다(보드 프리셋이 같은 phys 자리를 나중에 덮는다).
# 잃는 것이 없는지 확인한 결과를 남긴다.
#   proxima_b_regate : pause 가 보드 행과 완전히 같다(1.3728 / 1.144 / 0.0076267 / deform 0.1).
#                      보드 쪽은 여기에 ⚗ 대기 세트까지 들고 있으므로 순수한 상위집합이다.
#   proxima_d_regate : pause 도 Shue 값도 보드와 같지만, 보드에 없는 벨트(5000 / 1000 rad/h)를
#                      들고 있다. 그 벨트는 게이트된 적이 없다 — 보드의 d 는 magnetism.magnetic_field
#                      행뿐이고 출하 cfg 에도 has_inner/has_outer 가 없다. 그래서 피커의 phys 는
#                      출하되는 것(벨트 없음)을 보여주는 게 맞고, 이 엔트리는 아직 게이트되지 않은
#                      판단의 기록으로만 남는다. 다만 이건 보드 안의 모순이다 — d 의 environment /
#                      gameplay 행은 "trapped belts", "radiation belts of Jupiter's kind" 라고
#                      서술하는데 magnetism 축에 벨트 행이 없어서 cfg 에는 계면만 나간다.
#                      벨트 게이팅은 Phase 4 오너 결정이라 여기서 만들어 넣지 않는다(2026-08-18 보고).

presets = {}
for key, b in BODIES.items():          # 소스 dict 순서 유지 (stock/phys 쌍)
    p = conv(key, b)
    p['body_key'] = key.rsplit('_', 1)[0]     # earth_stock / earth_phys → earth
    p['variant'] = p['group']                 # stock | phys — 같은 천체의 두 판본
    pre = NEARSTARS_PRE.get(p['body_key'])
    if pre:
        syskey, board_name, depth, board_key = pre
        ko_sys, en_sys = SYS_LABEL[syskey]
        p['sys'], p['sys_label'], p['sys_label_en'] = syskey, ko_sys, en_sys
        p['depth'] = depth
        p['label'] = p['label_en'] = board_name
        p['body_key'] = board_key
    else:
        p['sys'] = 'sol'
        p['sys_label'], p['sys_label_en'] = SOL_KO, SOL_EN
        p['depth'] = 0
    g = SHUE_GROUNDED.get(p['body_key'])
    if p['variant'] == 'phys' and g:   # 근거 있는 α 가 있는 바디만 기본 표시
        a, r0, L, src = g
        p['view'].update({'shue': a, 'shue_r0': r0, 'shue_L': L})
        p['shue_src'] = src
    pz = b.get('pause') or {}
    # ⚗ 플러그인 Deliverable 1 대기 세트 — 다섯 값이 한 벌이라 통째로 실어 보낸다
    pend = {k[8:]: v for k, v in pz.items() if k.startswith('pending_')}
    if pend:
        p['pending'] = pend
    if p['variant'] == 'phys' and pz.get('shue_alpha'):    # 바디 테이블이 직접 든 Shue 값
        p['view'].update({'shue': pz['shue_alpha'], 'shue_r0': pz.get('shue_nose', 0),
                          'shue_L': pz.get('shue_tail', 0),
                          'shue_an': pz.get('shue_alpha_night', 0)})
    presets[key] = p

# NearStars 프리셋: 게이트된 phase4 보드에서 (emitter와 동일 소스)
sys.path.insert(0, os.path.join(D, '..', 'pipeline'))
from emit_kerbalism_radiation import load_nearstars_specs  # noqa: E402

CFG2VIEW = {'dist': 'dist', 'radius': 'rad', 'deform_xy': 'dxy', 'compression': 'comp',
            'extension': 'ext', 'border_dist': 'bdist', 'border_radius': 'brad',
            'border_deform_xy': 'bdxy', 'deform': 'deform'}

import yaml  # noqa: E402

ROMAN = re.compile(r'\s+(I{1,3}|IV|V|VI{0,3}|IX|X)$')


def designations(board_file):
    """보드의 identity 행에서 body → designation 을 모은다 (계층 판정용)."""
    doc = yaml.safe_load(open(os.path.join(D, '..', '..', 'phase4', board_file)))
    out = {}
    for row in doc.get('decisions', []):
        if row.get('axis') == 'identity':
            for fl in row.get('fields', []):
                if fl.get('name') == 'designation':
                    out[row['body']] = str(fl.get('value', '')).split(' (')[0]
    return out


_add_board_orbits()      # ROMAN·designations() 가 필요하므로 여기서 호출한다

_desig_cache = {}
for name, spec in load_nearstars_specs().items():
    m, bd = spec['model'], spec['body']
    # name 은 emit 이름(kopernicus_name)이다. 라벨과 body_key 는 보드의 body 키로 잡는다 —
    # 사람이 읽는 이름이 그쪽이고(Pandora vs Alpha Centauri A b III), emit 이름으로 잡으면
    # kopernicus_name 을 고칠 때마다 pre 스냅샷과의 짝이 깨진다(2026-08-18 실제로 깨졌다).
    board_body = spec['board_body']
    sysfile = spec['system']
    syskey = sysfile.replace('.yaml', '')
    _desig_cache.setdefault(sysfile, designations(sysfile))
    desig = _desig_cache[sysfile].get(board_body, board_body)
    ko_sys, en_sys = SYS_LABEL.get(syskey, (syskey, syskey))
    is_moon = bool(ROMAN.search(desig))
    p = {'label': board_body, 'label_en': board_body, 'group': 'nearstars',
         'sys': syskey, 'sys_label': ko_sys, 'sys_label_en': en_sys,
         'depth': 1 if is_moon else 0, 'desig': desig,
         'body_key': board_body.lower().replace(' ', '_'), 'variant': 'phys',
         'parent': ROMAN.sub('', desig) if is_moon else None,
         'inner': dict(OFF_BELT), 'outer': dict(OFF_BELT)}
    extent = 5.0
    for kind, grad in (('inner', 3.3), ('outer', 2.2)):
        belt = {CFG2VIEW[k[len(kind) + 1:]]: v for k, v in m.items() if k.startswith(kind)}
        if belt:
            belt['radiation'] = bd.get(f'radiation_{kind}', 0)
            belt['grad'] = bd.get(f'radiation_{kind}_gradient', grad)
            p[kind] = belt
            extent = max(extent, (belt['dist'] + belt['rad'])
                         / (belt.get('dxy', 1) ** 0.5) * 1.15)
    p['pause'] = {'on': True, 'rad': m.get('pause_radius', 5),
                  'comp': m.get('pause_compression', 1), 'ext': m.get('pause_extension', 1),
                  'hscale': m.get('pause_height_scale', 1),
                  'deform': m.get('pause_deform', 0),
                  # ⚗ 비-cfg: 스톡은 파수 5/7/6 하드코딩. 보드가 값을 담아도 엔진은 아직 안 읽는다.
                  'dscale': m.get('pause_deform_scale', 1),
                  'radiation': bd.get('radiation_pause', -0.01)}
    p['view'] = {'R': round(extent), 'tilt': 90 - bd.get('geomagnetic_pole_lat', 90),
                 'z': 0, 'offset': bd.get('geomagnetic_offset', 0)}
    # ⚗ Shue-native 보드값이 있으면 오버레이를 pause 슬라이더가 아니라 그 물리값에 고정
    pend = spec.get('pending', {})
    ps = {}
    for src, dst in (('pause_radius_smoothed', 'rad'), ('pause_compression_smoothed', 'comp'),
                     ('pause_extension_smoothed', 'ext'), ('pause_waist', 'waist'),
                     ('pause_smooth', 'smooth')):
        if src in pend:
            ps[dst] = pend[src]
    if ps:
        ps.setdefault('comp', 1.0)
        p['pending'] = ps
    if 'pause_alpha' in pend:
        p['view']['shue'] = pend['pause_alpha']
        p['view']['shue_r0'] = pend.get('pause_nose', 0)
        p['view']['shue_L'] = pend.get('pause_tail', 0)
        # 야간면 α(2-α 후류). 2026-08-18 까지 여기서 안 읽어서 보드가 게이트한 값이
        # 오버레이에 닿지 않았다 — 태양계 프리셋만 BODIES 딕트 경로로 받고 있었다.
        p['view']['shue_an'] = pend.get('pause_alpha_night', 0)
    # 보드가 α 를 게이트하지 않았으면 켜지 않는다(만들어 낸 값이 되므로)
    presets[board_body.lower()] = p
# Shue 데모: 지구 물리 파라미터 + 넓은 뷰 + α 오버레이
shue = conv('earth_shue', dict(BODIES['earth_phys'], tilt=0))
shue['label'] = 'Shue 데모'
shue['label_en'] = 'Shue demo'
shue['group'] = 'demo'          # 지구 물리와 같은 줄에 서면 중복처럼 보인다
shue.update({'sys': 'demo', 'sys_label': '데모', 'sys_label_en': 'Demo', 'depth': 0,
             'body_key': 'shue_demo', 'variant': None})
shue['view'].update({'R': 210, 'shue': 0.58})
shue['pause']['alpha'] = 0.35
presets['shueDemo'] = shue

# 위성 궤도는 프리셋마다 body_key 로 붙인다(없으면 빈 목록).
for p in presets.values():
    bk = p.get('body_key') or ''
    p['moons'] = [[n, a] for n, a in MOON_ORBITS.get(bk, [])]
    orb = BODY_ORBITS.get(bk)
    p['orbit'] = {'r': orb[0], 'ko': orb[1], 'en': orb[2]} if orb else None

# ---- 손 표 결속 점검 ----
# body_key 는 보드의 body 키에서 나오므로 이름이 바뀌면 같이 움직인다. 그 키로 붙는 손 표가
# 따라오지 못하면 아무것도 실패하지 않고 오버레이·라벨만 조용히 빠진다 — 2026-08-18 하루에
# 세 번(자기축, 피커, 궤도 고리) 그렇게 됐다. 그래서 빌드마다 결속을 확인하고 경고한다.
def _audit_tables(presets):
    preset_bk = {p['body_key'] for p in presets.values()}
    bodies_bk = {k.rsplit('_', 1)[0] for k in BODIES}
    warn = []
    for name, keys, universe, what in (
            ('SHUE_GROUNDED', set(SHUE_GROUNDED), preset_bk, 'preset body_key'),
            ('MOON_ORBITS', set(MOON_ORBITS), preset_bk, 'preset body_key'),
            ('KO', set(KO), bodies_bk, 'BODIES body key'),
            ('EN', set(EN), bodies_bk, 'BODIES body key'),
            ('NEARSTARS_PRE', set(NEARSTARS_PRE), bodies_bk, 'BODIES body key')):
        dead = sorted(keys - universe)
        if dead:
            warn.append(f"  {name}: key(s) bind to no {what}: {dead}")
    dead = sorted(v[3] for v in NEARSTARS_PRE.values() if v[3] not in preset_bk)
    if dead:
        warn.append(f"  NEARSTARS_PRE board keys bind to no preset body_key: {dead}")
    # BODY_ORBITS 는 아직 프리셋이 없는 위성까지 미리 담으므로 미결속을 경고하지 않는다.
    # 대신 반대 방향 — 고리도 라벨도 없는 천체가 생기면 그것이 결손이다.
    for bk in sorted(preset_bk):
        p = next(p for p in presets.values() if p['body_key'] == bk)
        if p.get('sys') != 'demo' and bk not in BODY_ORBITS:
            warn.append(f"  BODY_ORBITS: no parent-orbit ring for '{bk}' ({p['label']})")
    # 피커 무결성: 한 계 안에서 같은 라벨이 두 버튼으로 갈리면 그것이 중복 증상이다
    # (프록시마 b·d 가 2026-08-18 에 두 번 그렇게 갈렸다).
    seen = {}
    for p in presets.values():
        seen.setdefault((p.get('sys'), p['label']), set()).add(p['body_key'])
    for (sysk, label), bks in sorted(seen.items()):
        if len(bks) > 1:
            warn.append(f"  picker: '{label}' in {sysk} splits into {sorted(bks)}")
    if warn:
        print("WARNING: hand-keyed table(s) no longer bind to the data:", file=sys.stderr)
        for w in warn:
            print(w, file=sys.stderr)


_audit_tables(presets)

tpl = open(TEMPLATE).read()
assert '__PRESETS__' in tpl
html = tpl.replace('__PRESETS__', json.dumps(presets, ensure_ascii=False))
with open(OUT, 'w') as f:
    f.write(html)
print('wrote', os.path.normpath(OUT), f'({len(presets)} presets)')
