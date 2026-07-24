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
      'neptune': '해왕성', 'mercury': '수성', 'ganymede': '가니메데'}
OFF_BELT = {'on': False, 'radiation': 0, 'dist': 1, 'rad': 0.5}


def conv(key, b):
    body, kind = key.rsplit('_', 1)
    label = KO[body] + (' 스톡' if kind == 'stock' else ' 물리')
    p = {'label': label,
         'view': {'R': b['R'], 'tilt': abs(b.get('tilt', 0)), 'z': 0,
                  'offset': b.get('offset', 0)}}
    for belt in ('inner', 'outer'):
        p[belt] = dict(b[belt]) if b.get(belt) else dict(OFF_BELT)
    p['pause'] = dict(b['pause']) if b.get('pause') else {'on': False, 'rad': 5}
    return p


presets = {}
for key, b in BODIES.items():          # 소스 dict 순서 유지 (stock/phys 쌍)
    presets[key] = conv(key, b)

# NearStars 프리셋: 게이트된 phase4 보드에서 (emitter와 동일 소스)
sys.path.insert(0, os.path.join(D, '..', 'pipeline'))
from emit_kerbalism_radiation import load_nearstars_specs  # noqa: E402

CFG2VIEW = {'dist': 'dist', 'radius': 'rad', 'deform_xy': 'dxy', 'compression': 'comp',
            'extension': 'ext', 'border_dist': 'bdist', 'border_radius': 'brad',
            'border_deform_xy': 'bdxy'}

for name, spec in load_nearstars_specs().items():
    m, bd = spec['model'], spec['body']
    p = {'label': f'{name} (NearStars)', 'inner': dict(OFF_BELT), 'outer': dict(OFF_BELT)}
    extent = 5.0
    for kind, grad in (('inner', 3.3), ('outer', 2.2)):
        belt = {CFG2VIEW[k[len(kind) + 1:]]: v for k, v in m.items() if k.startswith(kind)}
        if belt:
            belt['radiation'] = bd.get(f'radiation_{kind}', 0)
            belt['grad'] = grad
            p[kind] = belt
            extent = max(extent, (belt['dist'] + belt['rad'])
                         / (belt.get('dxy', 1) ** 0.5) * 1.15)
    p['pause'] = {'on': True, 'rad': m.get('pause_radius', 5),
                  'comp': m.get('pause_compression', 1), 'ext': m.get('pause_extension', 1),
                  'hscale': m.get('pause_height_scale', 1),
                  'radiation': bd.get('radiation_pause', -0.01)}
    p['view'] = {'R': round(extent), 'tilt': 90 - bd.get('geomagnetic_pole_lat', 90),
                 'z': 0, 'offset': bd.get('geomagnetic_offset', 0)}
    presets[name.lower()] = p
# Shue 데모: 지구 물리 파라미터 + 넓은 뷰 + α 오버레이
shue = conv('earth_shue', dict(BODIES['earth_phys'], tilt=0))
shue['label'] = 'Shue 데모'
shue['view'].update({'R': 210, 'shue': 0.58})
shue['pause']['alpha'] = 0.35
presets['shueDemo'] = shue

tpl = open(TEMPLATE).read()
assert '__PRESETS__' in tpl
html = tpl.replace('__PRESETS__', json.dumps(presets, ensure_ascii=False))
with open(OUT, 'w') as f:
    f.write(html)
print('wrote', os.path.normpath(OUT), f'({len(presets)} presets)')
