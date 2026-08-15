# 1986년 보이저 2호 천왕성 조우의 pole-on 자기권 기하를 지구와 대비해 보여주는 docs/uranus-geometry.html 생성
"""Build the Uranus pole-on magnetotail geometry explainer (docs/uranus-geometry.html).

One template + this builder, the same shape as build_belt_viewer.py: every physical
number lives here (paper-cited, see REFS) and is injected into the template as JSON,
so the HTML carries no hard-coded physics.

Geometry conventions used by the template:
    +X = sunward (the solar wind blows toward -X), +Y = orbit normal, +Z = orbital motion.
    Length unit = one planetary radius. Obliquity tilts the spin axis in the X-Y plane,
    so Uranus' 97.8 deg puts the spin axis within 8 deg of the Sun direction — the
    "pole-on" configuration Voyager 2 met in January 1986.

Usage:
    python3 scripts/viz/build_uranus_geometry.py
"""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(D, 'uranus_geometry_template.html')
OUT = os.path.normpath(os.path.join(D, '..', '..', 'docs', 'uranus-geometry.html'))

import sys  # noqa: E402
sys.path.insert(0, os.path.join(D, '..', 'pipeline'))
from _nav import global_bar  # noqa: E402

# ── physical parameters ──────────────────────────────────────────────────────
# Shue r(theta) = r0 * (2 / (1 + cos theta))^alpha; flank = r0 * 2^alpha (theta = 90 deg).
# Earth r0/alpha: Shue 1998. Uranus r0 = 18 R_U with Earth's alpha adopted by analogy —
# both rows are already carried by docs/reference/planetary-magnetosphere-geometry-methodology.md.
EARTH = {
    'name': 'earth',
    'color': 0x6aa4ff,
    'obliquity': 23.4,        # deg, spin axis vs orbit normal
    'dipole_tilt': 11.0,      # deg, magnetic dipole vs spin axis
    'offset': 0.08,           # R_E, dipole centre offset along the magnetic axis
    'r0': 10.0,               # R_E, subsolar standoff (Shue 1998)
    'alpha': 0.58,            # Shue flaring exponent
    'flank': 14.948,          # R_E, r0 * 2^alpha at the terminator
    'period': 23.93,          # h
    'pitch': 0.0,             # deg, no helical twist: the tail stays put
    'tail_len': 60.0,         # R_E, how far downtail the surface is drawn
}
URANUS = {
    'name': 'uranus',
    'color': 0x68d8d0,
    'obliquity': 97.8,        # deg — near-sunward spin axis at the 1986 encounter
    'dipole_tilt': 59.0,      # deg from the rotation axis (Ness 1986)
    'offset': 0.3,            # R_U from the planet centre (Ness 1986)
    'r0': 18.0,               # R_U subsolar standoff
    'alpha': 0.58,            # adopted from Earth by analogy
    'flank': 26.907,          # R_U, 18 * 2^0.58
    'period': 17.24,          # h
    'pitch': 5.5,             # deg helical pitch of the tail field lines (Behannon 1987, +/- 3.0)
    'tail_len': 82.0,         # R_U drawn, past the ~54 R_U plasmoid
    'plasmoid': 54.0,         # R_U downtail, Voyager 2 plasmoid (DiBraccio 2019)
}

REFS = [
    {'bibcode': '1987JGR....9215354B',
     'en': 'Behannon et al. 1987 — the Uranian tail rotates 360 deg about its axis; '
           'helical pitch 5.5 +/- 3.0 deg',
     'ko': 'Behannon et al. 1987 — 천왕성 자기꼬리가 자기 축 둘레로 360° 회전, 나선 피치 5.5 ± 3.0°'},
    {'bibcode': '1986Sci...233...85N',
     'en': 'Ness et al. 1986 — Voyager 2 magnetic field results: dipole tilted ~59 deg, '
           'offset ~0.3 R_U',
     'ko': 'Ness et al. 1986 — 보이저 2호 자기장 관측: 쌍극자 약 59° 기울기, 중심에서 0.3 R_U 이탈'},
    {'bibcode': '2019AGUFMSM33E3247D',
     'en': 'DiBraccio et al. 2019 — plasmoid at ~54 R_U, the single-pass X-line constraint',
     'ko': 'DiBraccio et al. 2019 — 약 54 R_U 지점의 플라스모이드, 단 한 번 통과로 얻은 X-선 제약'},
    {'bibcode': '2024JGRA..12932723T',
     'en': 'Turner et al. 2024 — seasonal dependence of the Uranian magnetosphere over the '
           '84-year orbit',
     'ko': 'Turner et al. 2024 — 84년 공전 주기에 걸친 천왕성 자기권의 계절 의존성'},
    {'bibcode': '1998JGR...10317691S',
     'en': 'Shue et al. 1998 — the magnetopause shape model r(theta) = r0 (2/(1+cos theta))^alpha',
     'ko': 'Shue et al. 1998 — 자기권계면 형상 모형 r(θ) = r0 (2/(1+cos θ))^α'},
]

PARAMS = {
    'earth': EARTH,
    'uranus': URANUS,
    'refs': REFS,
    'anim_seconds_per_rotation': 15.0,   # 화면 시간 기준 자전 1회
}

# ── build ────────────────────────────────────────────────────────────────────
tpl = open(TEMPLATE).read()
assert '__PARAMS__' in tpl and '__NAVBAR__' in tpl
html = (tpl.replace('__PARAMS__', json.dumps(PARAMS, ensure_ascii=False))
           .replace('__NAVBAR__', global_bar('')))

# 본문에 반드시 남아 있어야 하는 수치 (템플릿 문구와 파라미터가 어긋나면 여기서 걸린다)
for token in ('97.8', '59', '0.3', '17.24', '5.5', '18', '0.58', '26.9',
              '23.4', '11', '10', '14.95', '54', '84', '360', '1986'):
    assert token in html, f'missing parameter in output: {token}'

with open(OUT, 'w') as f:
    f.write(html)
print('wrote', OUT, f'({len(html)} bytes)')
