# 검증된 벨트 데이터(render_belts_bodies.BODIES)를 인터랙티브 뷰어 템플릿에 주입해 docs/belt-viewer.html 생성
import json
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from render_belts_bodies import BODIES  # noqa: E402

TEMPLATE = os.path.join(D, 'belt_viewer_template.html')
OUT = os.path.join(D, '..', '..', 'docs', 'belt-viewer.html')

KO = {'earth': '지구', 'jupiter': '목성', 'saturn': '토성', 'uranus': '천왕성',
      'neptune': '해왕성', 'mercury': '수성', 'ganymede': '가니메데',
      'proxima_d': '프록시마 d'}
EN = {'earth': 'Earth', 'jupiter': 'Jupiter', 'saturn': 'Saturn', 'uranus': 'Uranus',
      'neptune': 'Neptune', 'mercury': 'Mercury', 'ganymede': 'Ganymede',
      'proxima_d': 'Proxima d'}
OFF_BELT = {'on': False, 'radiation': 0, 'dist': 1, 'rad': 0.5}


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


presets = {}
for key, b in BODIES.items():          # 소스 dict 순서 유지 (stock/phys 쌍)
    presets[key] = conv(key, b)

# 지구 쌍: Shue 기준을 실측 물리값에 고정 (Shue 1998 α=0.58, nose 10 R_E, 꼬리 관측 ~200 R_E)
for key in ('earth_stock', 'earth_phys'):
    if key in presets:
        presets[key]['view'].update({'shue': 0.58, 'shue_r0': 10, 'shue_L': 200})

# NearStars 프리셋: 게이트된 phase4 보드에서 (emitter와 동일 소스)
sys.path.insert(0, os.path.join(D, '..', 'pipeline'))
from emit_kerbalism_radiation import load_nearstars_specs  # noqa: E402

CFG2VIEW = {'dist': 'dist', 'radius': 'rad', 'deform_xy': 'dxy', 'compression': 'comp',
            'extension': 'ext', 'border_dist': 'bdist', 'border_radius': 'brad',
            'border_deform_xy': 'bdxy', 'deform': 'deform'}

for name, spec in load_nearstars_specs().items():
    m, bd = spec['model'], spec['body']
    p = {'label': name, 'label_en': name, 'group': 'nearstars',
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
    presets[name.lower()] = p
# Shue 데모: 지구 물리 파라미터 + 넓은 뷰 + α 오버레이
shue = conv('earth_shue', dict(BODIES['earth_phys'], tilt=0))
shue['label'] = 'Shue 데모'
shue['label_en'] = 'Shue demo'
shue['group'] = 'demo'          # 지구 물리와 같은 줄에 서면 중복처럼 보인다
shue['view'].update({'R': 210, 'shue': 0.58})
shue['pause']['alpha'] = 0.35
presets['shueDemo'] = shue

tpl = open(TEMPLATE).read()
assert '__PRESETS__' in tpl
html = tpl.replace('__PRESETS__', json.dumps(presets, ensure_ascii=False))
with open(OUT, 'w') as f:
    f.write(html)
print('wrote', os.path.normpath(OUT), f'({len(presets)} presets)')
