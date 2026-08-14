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
      'proxima_d': '프록시마 d'}
EN = {'venus': 'Venus', 'mars': 'Mars', 'earth': 'Earth', 'jupiter': 'Jupiter', 'saturn': 'Saturn', 'uranus': 'Uranus',
      'neptune': 'Neptune', 'mercury': 'Mercury', 'ganymede': 'Ganymede',
      'proxima_d': 'Proxima d'}
OFF_BELT = {'on': False, 'radiation': 0, 'dist': 1, 'rad': 0.5}


# Shue 기준선은 α 가 실제로 근거 있는 바디에서만 기본 표시한다.
# log2(pause_compression) 환산은 지구형 cfg 에서만 형상 충실이고(방법론 Part C),
# 자이언트에 쓰면 flank/nose 1.2 = 지구보다 덜 벌어진 주간면이라는 비물리 값이 된다.
# 자이언트도 Shue 형식 적합이 존재하는 경우엔 쓴다(목성=Rutala 2025 S97*). 없는 천체는
# 만들어 내지 않고 끈다(토성 적합은 있으나 계수가 유료 장벽, 얼음 자이언트는 적합 자체가 없음).
SHUE_GROUNDED = {
    # body: (α, nose r0, tail L, 출처)
    'earth': (0.58, 10, 200, 'Shue 1998'),
    'mercury': (0.5, 1.45, 0, 'Winslow 2013 (MESSENGER 통과 적합: R_ss 1.45 R_M, α 0.5)'),
    # 목성: Rutala 2025 의 S97* 적합. α = 0.28 + 1.08·p_SW, r_SS = 38.0·p_SW^-0.25 [R_J].
    # 우리 프리셋 노즈 63 R_J(Joy 2002 압축 상태)를 그 r_SS 관계에 넣으면 p_SW 0.132 nPa → α 0.423.
    # 금성·화성은 여기 두지 않는다 — 유도 경계라 Shue 가 아니라 원+원뿔 형식을 쓴다(imb_* 키).
    'jupiter': (0.423, 63, 0, 'Rutala 2025 S97* (α=0.28+1.08·p_SW, 노즈 63 R_J ⇒ p 0.132 nPa)'),
}


def conv(key, b):
    body, kind = key.rsplit('_', 1)
    # 그룹 라벨이 stock/phys 를 이미 말해주므로 버튼에는 천체명만 남긴다.
    p = {'label': KO[body], 'label_en': EN[body],
         'group': 'stock' if kind == 'stock' else 'phys',
         'view': {'R': b['R'], 'tilt': abs(b.get('tilt', 0)), 'z': 0,
                  'offset': b.get('offset', 0)}}
    for belt in ('inner', 'outer'):
        p[belt] = dict(b[belt]) if b.get(belt) else dict(OFF_BELT)
    p['pause'] = dict(b['pause']) if b.get('pause') else {'on': False, 'rad': 5}
    return p


SOL_KO, SOL_EN = '태양계', 'Solar System'
presets = {}
for key, b in BODIES.items():          # 소스 dict 순서 유지 (stock/phys 쌍)
    p = conv(key, b)
    p['sys'] = 'sol'
    p['sys_label'], p['sys_label_en'] = SOL_KO, SOL_EN
    p['body_key'] = key.rsplit('_', 1)[0]     # earth_stock / earth_phys → earth
    p['variant'] = p['group']                 # stock | phys — 같은 천체의 두 판본
    p['depth'] = 0
    g = SHUE_GROUNDED.get(p['body_key'])
    if p['variant'] == 'phys' and g:   # 근거 있는 α 가 있는 바디만 기본 표시
        a, r0, L, src = g
        p['view'].update({'shue': a, 'shue_r0': r0, 'shue_L': L})
        p['shue_src'] = src
    pz = b.get('pause') or {}
    if p['variant'] == 'phys' and pz.get('shue_alpha'):    # 바디 테이블이 직접 든 Shue 값
        p['view'].update({'shue': pz['shue_alpha'], 'shue_r0': pz.get('shue_nose', 0),
                          'shue_L': pz.get('shue_tail', 0),
                          'shue_an': pz.get('shue_alpha_night', 0)})
    if p['variant'] == 'phys' and pz.get('imb_term'):       # 유도 경계 오버레이(원 + 원뿔)
        p['view'].update({'imb_nose': pz['imb_nose'], 'imb_term': pz['imb_term'],
                          'imb_slope': pz['imb_slope'], 'imb_close': pz.get('imb_close', 40),
                          'imb_k': pz.get('imb_k', 2), 'imb_d0': pz.get('imb_d0', 20),
                          'imb_label': pz.get('imb_label', 'IMB'), 'shue': 0})
    presets[key] = p

# NearStars 프리셋: 게이트된 phase4 보드에서 (emitter와 동일 소스)
sys.path.insert(0, os.path.join(D, '..', 'pipeline'))
from emit_kerbalism_radiation import load_nearstars_specs  # noqa: E402

CFG2VIEW = {'dist': 'dist', 'radius': 'rad', 'deform_xy': 'dxy', 'compression': 'comp',
            'extension': 'ext', 'border_dist': 'bdist', 'border_radius': 'brad',
            'border_deform_xy': 'bdxy', 'deform': 'deform'}

import yaml  # noqa: E402

ROMAN = re.compile(r'\s+(I{1,3}|IV|V|VI{0,3}|IX|X)$')
SYS_LABEL = {'alpha_centauri': ('알파 센타우리', 'Alpha Centauri'),
             'proxima_cen': ('프록시마 센타우리', 'Proxima Centauri')}


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


_desig_cache = {}
for name, spec in load_nearstars_specs().items():
    m, bd = spec['model'], spec['body']
    sysfile = spec['system']
    syskey = sysfile.replace('.yaml', '')
    _desig_cache.setdefault(sysfile, designations(sysfile))
    desig = _desig_cache[sysfile].get(name, name)
    ko_sys, en_sys = SYS_LABEL.get(syskey, (syskey, syskey))
    is_moon = bool(ROMAN.search(desig))
    p = {'label': name, 'label_en': name, 'group': 'nearstars',
         'sys': syskey, 'sys_label': ko_sys, 'sys_label_en': en_sys,
         'depth': 1 if is_moon else 0, 'desig': desig,
         'body_key': name.lower().replace(' ', '_'), 'variant': None,
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
    if 'pause_alpha' in pend:
        p['view']['shue'] = pend['pause_alpha']
        p['view']['shue_r0'] = pend.get('pause_nose', 0)
        p['view']['shue_L'] = pend.get('pause_tail', 0)
    # 보드가 α 를 게이트하지 않았으면 켜지 않는다(만들어 낸 값이 되므로)
    presets[name.lower()] = p
# Proxima d 는 보드 행이 없어 render_belts_bodies 에 값이 있지만, 계 소속은 프록시마다.
if 'proxima_d_phys' in presets:
    pd = presets['proxima_d_phys']
    pd.update({'group': 'nearstars', 'sys': 'proxima_cen', 'body_key': 'proxima_cen_d', 'variant': None,
               'sys_label': SYS_LABEL['proxima_cen'][0], 'sys_label_en': SYS_LABEL['proxima_cen'][1],
               'depth': 0, 'desig': 'Proxima Centauri d',
               'label': 'Proxima Cen d', 'label_en': 'Proxima Cen d'})
    presets['proxima_cen_d'] = presets.pop('proxima_d_phys')

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

tpl = open(TEMPLATE).read()
assert '__PRESETS__' in tpl
html = tpl.replace('__PRESETS__', json.dumps(presets, ensure_ascii=False))
with open(OUT, 'w') as f:
    f.write(html)
print('wrote', os.path.normpath(OUT), f'({len(presets)} presets)')
