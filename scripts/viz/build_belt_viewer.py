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

# NearStars Phase 4 도출 프리셋 (아티팩트 2026-07-23에서 이월)
presets['pandora'] = {'label': 'Pandora (NearStars)',
    'view': {'R': 4, 'tilt': 10, 'z': 0, 'offset': 0},
    'inner': {'radiation': 4.0, 'grad': 3.3, 'dist': 1.4, 'rad': 0.5, 'comp': 1.1,
              'ext': 0.8, 'bdist': 0.0001, 'brad': 1.05},
    'outer': dict(OFF_BELT),
    'pause': {'on': True, 'rad': 2.6, 'radiation': -0.01, 'comp': 1.15, 'ext': 0.6,
              'hscale': 1.0}}
presets['polyphemus'] = {'label': 'Polyphemus (NearStars)',
    'view': {'R': 13, 'tilt': 5, 'z': 0, 'offset': 0},
    'inner': {'radiation': 300, 'grad': 3.3, 'dist': 1.8, 'rad': 1.0, 'comp': 1.05, 'ext': 0.9},
    'outer': {'radiation': 40, 'grad': 2.2, 'dist': 8.5, 'rad': 4.0, 'comp': 1.05, 'ext': 0.85},
    'pause': {'on': True, 'rad': 22, 'radiation': -0.01, 'comp': 1.1, 'ext': 0.1, 'hscale': 1.02}}
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
