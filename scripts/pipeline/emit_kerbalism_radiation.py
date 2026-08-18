# 피팅된 방사선대 지오메트리(+물리 강도)를 Kerbalism RadiationModel/RadiationBody MM 패치로 방출하는 emitter
# 지오메트리 단일 소스 = scripts/viz/render_belts_bodies.py 의 *_phys 엔트리 (fit_belts.py 산출).
import os
import sys

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(D, '..', 'viz'))
from render_belts_bodies import BODIES  # noqa: E402

OUT = os.path.join(D, '..', '..', 'dist', 'NearStars-Configs', 'Patches', 'Kerbalism',
                   'NearStars-SolarSystemRadiation.cfg')
OUT_NS = os.path.join(D, '..', '..', 'dist', 'NearStars-Configs', 'Patches', 'Kerbalism',
                      'NearStars-Radiation.cfg')
PHASE4_DIR = os.path.join(D, '..', '..', 'phase4')
ADS = 'https://ui.adsabs.harvard.edu/abs/'

# RadiationModel geometry field names as they appear in phase4 board fields[]
MODEL_KEYS = [
    'inner_dist', 'inner_radius', 'inner_deform_xy', 'inner_compression',
    'inner_extension', 'inner_border_dist', 'inner_border_radius',
    'inner_border_deform_xy', 'inner_deform',
    'outer_dist', 'outer_radius', 'outer_deform_xy', 'outer_compression',
    'outer_extension', 'outer_border_dist', 'outer_border_radius',
    'outer_border_deform_xy', 'outer_deform',
    'pause_radius', 'pause_compression', 'pause_extension', 'pause_height_scale',
    'pause_deform',            # 다중극 경계의 비축대칭 로브 (스톡 mercury/irregular = 0.1)
]
# ⚗ 보드가 담지만 스톡 Kerbalism이 소비하지 않는 키 — 자기권계면 플러그인 대기.
# emit에서는 주석으로만 흘려보내고 실제 cfg 라인으로 쓰지 않는다.
PENDING_MODEL_KEYS = ['pause_deform_scale', 'pause_nose', 'pause_alpha', 'pause_tail',
                      # 야간면 α (2-α 후류 형상). 2026-08-18 까지 이 목록에 없어서 c·d 가
                      # 게이트한 0.52 가 emit 주석에도 뷰어 오버레이에도 닿지 않았다.
                      'pause_alpha_night',
                      # 스톡 계면 함수 일반화 (둘 다 0 이면 스톡과 동일) — 방법론 Part C ⚗ 절
                      # 일반화 스톡 pause 는 네 값이 한 세트다 — smooth 만 적용하면 형상이 깨진다.
                      'pause_waist', 'pause_smooth',
                      # 일반화 스톡 계획에서 compression 은 1.0 으로 은퇴하고 비대칭을
                      # waist 가 받는다 — 그 1.0 도 적어둘 자리가 있어야 계획이 완결된다.
                      'pause_radius_smoothed', 'pause_compression_smoothed',
                      'pause_extension_smoothed',
                      # pause_offset 은 pause_waist 로 흡수됐다(같은 연산, 부호 반대). 옛 보드 호환용.
                      'pause_offset', 'pause_offset_radius',
                      'pause_offset_compression', 'pause_offset_extension']
BODY_KEYS = ['radiation_inner', 'radiation_inner_gradient',
             'radiation_outer', 'radiation_outer_gradient', 'radiation_pause',
             'geomagnetic_pole_lat', 'geomagnetic_pole_lon', 'geomagnetic_offset']
# cfg 로 나가지 않는 것이 정상인 서술/물리량 필드. 위 세 목록 어디에도 없고 여기에도 없는
# 이름이 게이트된 magnetism 행에 나타나면 그것은 '조용히 버려지는 값'이므로 경고한다
# (2026-08-18: c 의 geomagnetic_* 와 c·d 의 pause_alpha_night 가 실제로 그렇게 사라져 있었다).
DESCRIPTIVE_KEYS = ['magnetic_field', 'magnetic_field_polar', 'field_geometry',
                    'belt_architecture', 'magnetosphere', 'radiation_model',
                    'magnetopause_standoff_rp']

# 벨트 dict 키 → cfg 필드 (렌더 전용 키 radiation/grad 제외)
BELT_FIELDS = [('dist', 'dist'), ('radius', 'rad'), ('deform_xy', 'dxy'),
               ('compression', 'comp'), ('extension', 'ext'),
               ('border_dist', 'bdist'), ('border_radius', 'brad'),
               ('border_deform_xy', 'bdxy')]

# geomagnetic 축·offset은 자오면 렌더가 극성/경도를 담지 못하므로 여기서 명시 (전부 인용 부착).
# refs: (label, bibcode) — 주석에 클릭 가능한 ADS URL로 방출.
SOLAR = [
    {'body': 'Earth', 'phys': 'earth_phys',
     'pole_lat': 80.37, 'pole_lon': -72.62, 'offset': 0.07,
     'pole_note': 'IGRF dipole, tilt ~9.6 deg (stock value kept -- already accurate)',
     'summary': ['Validation anchor -- near-stock. Inner belt L 1.1-2 with the real ~1000 km',
                 'loss-cone floor, slot, outer belt L 3-7; magnetopause nose 10 R_E (= 15/1.5).',
                 'Fit IoU 0.99 (inner) / 0.98 (outer).'],
     'refs': [('Shue 1997 (magnetopause)', '1997JGR...102.9497S'),
              ('Reeves 2013 (outer belt L 3-7)', '2013Sci...341..991R'),
              ('Ripoll 2016 (slot L 2-3)', '2016GeoRL..43.5616R'),
              ('Liu 2024 (outer-horn loss-cone precipitation)', '2024JGRA..12932171L')]},
    {'body': 'Jupiter', 'phys': 'jupiter_phys',
     'pole_lat': -80.0, 'pole_lon': 0.0, 'offset': 0.1,
     'pole_note': 'JRM33: tilt 10.3 deg, reversed polarity, eccentric dipole ~0.1 R_J',
     'summary': ['Intense dipolar inner belt moved in to L 1.2-3 (peak ~1.5-2 R_J; stock had a',
                 'round shell at 5-7 R_J) with loss-cone D-cut; outer = flat magnetodisc lens',
                 '3-24 R_J x +-3. The physical disc runs past 50 R_J, so the shell edge is where',
                 'the dose ramps out rather than where the disc ends; 24 keeps Ganymede at full',
                 'intensity and Callisto outside. Pause nose 63 R_J.',
                 'Fit IoU 0.98 (inner) / 0.87 (disc -- torus-model ceiling).',
                 'radiation_inner 1500 rad/h is a conf-low regime call (order 10^3-10^4 rad/day).'],
     'refs': [('Divine & Garrett 1983 (belt model)', '1983JGR....88.6889D'),
              ('Santos-Costa 2001 (dipolar inner)', '2001P&SS...49..303S'),
              ('Khurana 1989 (magnetodisc half-width ~3-3.5)', '1989JGR....9411791K'),
              ('Joy 2002 (pause nose 63 compressed)', '2002JGRA..107.1309J'),
              ('Connerney 2022 JRM33 (pole/offset)', '2022JGRE..12707055C')]},
    {'body': 'Saturn', 'phys': 'saturn_phys',
     'pole_lat': 90.0, 'pole_lon': 0.0, 'offset': 0.047,
     'pole_note': 'Cao 2020: tilt < 0.007 deg (aligned), offset 0.047 R_S north',
     'summary': ['No inner belt (rings absorb it -- stock had this right). Outer belt confined to',
                 'the real CRAND shell L 2.3-6 (A-ring edge to Dione filter) instead of a 7/7 blob',
                 'flooding the swept ring zone; intensity nerfed to ~10 rad/h (CRAND-weak, orders',
                 'below Jupiter). Pause nose 24 R_S. Fit IoU 0.98.'],
     'refs': [('Cooper 1983 (rings absorb inner belt)', '1983JGR....88.3945C'),
              ('Kollmann 2013 (belt L-range, moon corridors)', '2013Icar..222..323K'),
              ('Kollmann 2017 (CRAND-weak intensity)', '2017NatAs...1..872K'),
              ('Achilleos 2008 (pause 22-27 bimodal)', '2008JGRA..11311209A'),
              ('Cao 2020 (tilt/offset)', '2020Icar..34413541C')]},
    {'body': 'Uranus', 'phys': 'uranus_phys',
     'pole_lat': 31.4, 'pole_lon': 0.0, 'offset': 0.3,
     'pole_note': 'Ness 1986: tilt 58.6 deg, offset 0.3 R_U (stock axis kept; OTD longitude not modeled)',
     'summary': ['Replaces the shared generic `saturn` blob (whose radiation_inner was dead cfg)',
                 'with a real two-shell structure bounded by moon sweeping: inner L 1.5-5 (inside',
                 'Miranda L 5.1), outer L 5-10 (Miranda to Umbriel; electron maxima live between',
                 'the moon minima). Trapping is detectable to Titania ~L 17. Pause nose 18 R_U.',
                 'Fit IoU 0.98 (inner) / 0.97 (outer).'],
     'refs': [('Ness 1986 (tilt/offset/standoff)', '1986Sci...233...85N'),
              ('Krimigis 1986 (Miranda exception region)', '1986Sci...233...97K'),
              ('Cheng 1987 (electron minima at moon L-shells)', '1987JGR....9215315C'),
              ('Stone 1986 (moon sweeping)', '1986Sci...233...93S')]},
    {'body': 'Neptune', 'phys': 'neptune_phys',
     'pole_lat': 43.0, 'pole_lon': 0.0, 'offset': 0.55,
     'pole_note': 'Ness 1989: tilt 47 deg, offset 0.55 R_N (largest planetary offset; stock axis kept)',
     'summary': ['Replaces the shared generic blob with the real structure: inner L 1.5-5 (moon/ring',
                 'absorption zone, Proteus divider at L 4.75), outer L 5-14 peaking at L~7, hard',
                 'Triton cut at ~14 R_N. Pause nose 26.5 R_N (stock had 20 via the shared model).',
                 'Fit IoU 0.98 (inner) / 0.97 (outer).'],
     'refs': [('Ness 1989 (tilt/offset/standoff)', '1989Sci...246.1473N'),
              ('Stone 1989 (peak L~7)', '1989Sci...246.1489S'),
              ('Krimigis 1989 (Triton cut, Proteus signature)', '1989Sci...246.1483K')]},
    {'body': 'Mercury', 'phys': 'mercury_phys',
     'pole_lat': 90.0, 'pole_lon': 0.0, 'offset': 0.198,
     'pole_note': 'Anderson 2011/2012: tilt < 0.8-3 deg -- aligned within uncertainty; the offset carries the north-south asymmetry',
     'summary': ['No stable belt (correct in stock) -- the magnetosphere is too small/dynamic to trap.',
                 'Pause nose corrected to 1.45 R_M (stock 1.6/1.4 put it at a tight 1.14); the',
                 '0.198 R_M northward dipole offset concentrates surface dose in the south.'],
     'refs': [('Winslow 2013 (nose 1.45, range 1.35-1.55)', '2013JGRA..118.2213W'),
              ('Anderson 2011 (offset 484 km, tilt < 3 deg)', '2011Sci...333.1859A'),
              ('Schriver 2015 (no stable belt)', '2015AGUFM.P53A2089S')]},
    {'body': 'Ganymede', 'phys': 'ganymede_phys',
     'pole_lat': -86.0, 'pole_lon': 0.0, 'offset': 0.0,
     'pole_note': 'Kivelson 2002: 719 nT dipole, tilt ~176 deg (near anti-aligned with Jupiter)',
     'summary': ['Gains its missing magnetopause (stock omits it entirely): nose 2 R_G upstream,',
                 'width 5.5 R_G across. The single weak closed-line belt (L 1.1-1.9) is absorbed at',
                 'the airless surface -- no altitude cut. Fit IoU 0.97. The pause shields ~50-60% of',
                 'the ambient Jovian dose for a low orbiter.'],
     'refs': [('Kivelson 1998 (standoff ~2 R_G)', '1998JGR...10319963K'),
              ('Kivelson 2002 (719 nT, tilt 176 deg)', '2002Icar..157..507K'),
              ('Allioux 2013 (belt + shield -50-60%)', '2013AdSpR..51.1204A')]},
]

QUALITY = {'inner': 50.0, 'outer': 60.0, 'pause': 30.0}   # 스톡 earth 모델의 메시 품질 값


def fmt(v):
    s = f"{v:.6f}".rstrip('0').rstrip('.')
    return s if s else '0'


def belt_block(kind, d, out):
    out.append(f"  has_{kind} = true")
    for cfg, key in BELT_FIELDS:
        if key in d:
            out.append(f"  {kind}_{cfg} = {fmt(d[key])}")
    out.append(f"  {kind}_quality = {fmt(QUALITY[kind])}")


def pause_block(d, out):
    out.append("  has_pause = true")
    out.append(f"  pause_radius = {fmt(d['rad'])}")
    out.append(f"  pause_compression = {fmt(d['comp'])}")
    out.append(f"  pause_extension = {fmt(d['ext'])}")
    out.append(f"  pause_height_scale = {fmt(d.get('hscale', 1.0))}")
    out.append(f"  pause_quality = {fmt(QUALITY['pause'])}")


def emit():
    L = []
    L.append("// Generated by scripts/pipeline/emit_kerbalism_radiation.py -- do not hand-edit.")
    L.append("// Physics-grounded solar-system radiation belts for Kerbalism / ROKerbalism (RSS).")
    L.append("// Geometry: the in-game SDF numerically fitted (Nelder-Mead, IoU-scored) to the real")
    L.append("// dipole drift shells between ADS-anchored field lines; magnetopauses use the correct")
    L.append("// nose semantics (nose = pause_radius / pause_compression).")
    L.append("// Intensities: physical values -- conf-low regime calls, not field readouts.")
    L.append("// Full audit + renders: docs/reference/solar-system-radiation-belts.md")
    L.append("// https://vannadin.github.io/nearstars-db/wiki/reference__solar-system-radiation-belts.html")
    for s in SOLAR:
        b = BODIES[s['phys']]
        model = 'nearstars_' + s['body'].lower()
        L.append("")
        L.append(f"// ==== {s['body']} " + "=" * max(4, 60 - len(s['body'])))
        for line in s['summary']:
            L.append(f"// {line}")
        for label, bib in s['refs']:
            L.append(f"//   {label}: {ADS}{bib}")
        L.append(f"RadiationModel:NEEDS[RealSolarSystem]")
        L.append("{")
        L.append(f"  name = {model}")
        for kind in ('inner', 'outer'):
            if b.get(kind):
                L.append("")
                belt_block(kind, b[kind], L)
        if b.get('pause'):
            L.append("")
            pause_block(b['pause'], L)
        L.append("}")
        L.append(f"@RadiationBody[{s['body']}]:NEEDS[RealSolarSystem]:AFTER[KerbalismConfig]")
        L.append("{")
        L.append(f"  %radiation_model = {model}")
        if b.get('inner'):
            L.append(f"  %radiation_inner = {fmt(b['inner']['radiation'])}")
        if b.get('outer'):
            L.append(f"  %radiation_outer = {fmt(b['outer']['radiation'])}")
        if b.get('pause'):
            L.append(f"  %radiation_pause = {fmt(b['pause']['radiation'])}")
        L.append(f"  %geomagnetic_pole_lat = {fmt(s['pole_lat'])}   // {s['pole_note']}")
        L.append(f"  %geomagnetic_pole_lon = {fmt(s['pole_lon'])}")
        L.append(f"  %geomagnetic_offset = {fmt(s['offset'])}")
        L.append("}")
    return "\n".join(L) + "\n"


def check(text):
    """라운드트립: 방출된 cfg를 파싱해 BODIES phys 값과 대조."""
    import re
    blocks = re.findall(r'RadiationModel:NEEDS\[RealSolarSystem\]\s*\{(.*?)\n\}', text, re.S)
    assert len(blocks) == len(SOLAR), f"model count {len(blocks)} != {len(SOLAR)}"
    for s, blk in zip(SOLAR, blocks):
        b = BODIES[s['phys']]
        kv = dict(re.findall(r'(\w+) = ([^\s/]+)', blk))
        for kind in ('inner', 'outer'):
            if not b.get(kind):
                assert f'has_{kind}' not in kv, f"{s['body']}: unexpected {kind}"
                continue
            for cfg, key in BELT_FIELDS:
                if key in b[kind]:
                    got, want = float(kv[f'{kind}_{cfg}']), b[kind][key]
                    assert abs(got - want) < 1e-6, f"{s['body']} {kind}_{cfg}: {got} != {want}"
        if b.get('pause'):
            assert abs(float(kv['pause_radius']) - b['pause']['rad']) < 1e-6, s['body']
            assert abs(float(kv['pause_compression']) - b['pause']['comp']) < 1e-6, s['body']
    print(f"round-trip check OK ({len(SOLAR)} bodies)")


def load_nearstars_specs():
    """phase4 보드에서 gated 자기권 행을 읽어 emit 스펙으로 변환.

    두 축을 함께 읽는다. 대부분의 천체는 pause 필드를 magnetism.radiation_belts 에
    싣지만, 벨트가 없거나 아직 벨트 행이 없는 천체(Proxima b·d)는 같은 값을
    magnetism.magnetic_field 에 단다. 한 축만 읽으면 그런 천체의 계면이 조용히
    누락되므로(2026-08-16 발견), body 단위로 두 축을 병합한다. 충돌 시에는
    보드 문서 순서상 뒤에 오는 radiation_belts 가 이긴다.

    반환: {kopernicus_name: {'model': {...}, 'body': {...}, 'row': row}} (보드 순서)."""
    import yaml
    unclassified = {}                 # 이름 → [보드/바디] (아래에서 경고로 흘린다)
    CFG_AXES = ('magnetism.magnetic_field', 'magnetism.radiation_belts')
    specs = {}
    for fn in sorted(os.listdir(PHASE4_DIR)):
        if not fn.endswith('.yaml'):
            continue
        board = yaml.safe_load(open(os.path.join(PHASE4_DIR, fn)))
        # cfg 바디명의 단일 진실원 = bulk 축의 kopernicus_name (2026-08-18 소급 적용).
        # 그전에는 magnetism 행의 row-level 키였고, 없으면 보드의 body 키를 그대로 썼다.
        # 여섯 중 다섯이 후자여서 보드 표기와 인게임 이름이 갈리면 조용히 어긋났다.
        # 옛 row-level 키도 계속 읽어 주되 bulk 가 우선한다.
        kop_names = {}
        for row in board.get('decisions', []):
            if row.get('axis') != 'bulk':
                continue
            for fl in row.get('fields', []):
                if fl.get('name') == 'kopernicus_name':
                    kop_names[row['body']] = fl.get('value')
        merged = {}                       # body → 병합 결과 (보드 순서 유지)
        for row in board.get('decisions', []):
            if row.get('axis') not in CFG_AXES or row.get('status') != 'gated':
                continue
            fields = {f['name']: f['value'] for f in row.get('fields', [])}
            for k in fields:
                if not (k in MODEL_KEYS or k in BODY_KEYS or k in PENDING_MODEL_KEYS
                        or k in DESCRIPTIVE_KEYS):
                    unclassified.setdefault(k, []).append(f"{fn}/{row['body']}")
            if row['axis'] == 'magnetism.radiation_belts' and 'radiation_model' not in fields:
                raise SystemExit(f"{fn} {row['body']}: radiation_belts row has no "
                                 "individual cfg fields (legacy packed format?)")
            # 서술만 있는 자기장 행은 건너뛴다. 단 '서술만'의 기준이 pause_ 접두사였던 탓에
            # geomagnetic_* 를 이 행에 단 바디는 값이 조용히 사라졌다(2026-08-18 발견:
            # Proxima Cen c 의 기울기 40·offset 0.4 가 보드에는 게이트돼 있는데 cfg 에는
            # geomagnetic 줄이 아예 없었다). BODY_KEYS 기여도 함께 본다.
            if row['axis'] == 'magnetism.magnetic_field' and not any(
                    k.startswith('pause_') or k in BODY_KEYS for k in fields):
                continue                  # 서술만 있는 자기장 행 — cfg 기여 없음
            e = merged.setdefault(row['body'], {'fields': {}, 'refs': [], 'row': row,
                                                'kop': None})
            e['fields'].update(fields)
            e['refs'] += [r for r in row.get('refs', []) if r not in e['refs']]
            if row.get('kopernicus_name'):
                e['kop'] = row['kopernicus_name']
            if row['axis'] == 'magnetism.radiation_belts':
                e['row'] = row            # 벨트 행이 대표 행
        for body, e in merged.items():
            fields = e['fields']
            if 'radiation_model' not in fields:
                continue                  # 계면도 벨트도 없는 천체
            name = kop_names.get(body) or e['kop'] or body
            specs[name] = {'model_name': fields['radiation_model'],
                           # 보드의 body 키. emit 이름(kopernicus_name)과 다를 수 있고,
                           # 사람이 읽는 이름은 이쪽이다(Pandora vs Alpha Centauri A b III).
                           # 소비자가 emit 이름으로 라벨을 잡으면 kopernicus_name 을 고칠 때마다
                           # UI 가 따라 깨진다(2026-08-18 뷰어 피커가 실제로 그렇게 갈라졌다).
                           'board_body': body,
                           'model': {k: fields[k] for k in MODEL_KEYS if k in fields},
                           'body': {k: fields[k] for k in BODY_KEYS if k in fields},
                           'pending': {k: fields[k] for k in PENDING_MODEL_KEYS if k in fields},
                           'refs': e['refs'], 'system': fn}
    if unclassified:
        print("WARNING: gated magnetism field(s) reach no consumer -- add them to "
              "MODEL_KEYS / BODY_KEYS / PENDING_MODEL_KEYS, or to DESCRIPTIVE_KEYS if "
              "they are narrative only:", file=sys.stderr)
        for k, where in sorted(unclassified.items()):
            print(f"  {k}: {', '.join(sorted(set(where)))}", file=sys.stderr)
    return specs


def emit_nearstars(specs):
    L = []
    L.append("// Generated by scripts/pipeline/emit_kerbalism_radiation.py -- do not hand-edit.")
    L.append("// NearStars body radiation belts, read from the gated phase4 boards")
    L.append("// (axis magnetism.radiation_belts; geometry = fit_belts.py dipole-shell fits,")
    L.append("// intensities = methodology Part B regime calls). Provenance refs per body below.")
    for name, s in specs.items():
        L.append("")
        L.append(f"// ==== {name} ({s['system']}) " + "=" * max(4, 46 - len(name) - len(s['system'])))
        for r in s['refs']:
            L.append(f"//   {r}")
        L.append("RadiationModel:NEEDS[NearStarsSystem]")
        L.append("{")
        L.append(f"  name = {s['model_name']}")
        m = s['model']
        for kind in ('inner', 'outer'):
            keys = [k for k in MODEL_KEYS if k.startswith(kind) and k in m]
            if not keys:
                continue
            L.append("")
            L.append(f"  has_{kind} = true")
            for k in keys:
                L.append(f"  {k} = {fmt(m[k])}")
            L.append(f"  {kind}_quality = {fmt(QUALITY[kind])}")
        if 'pause_radius' in m:
            L.append("")
            L.append("  has_pause = true")
            # pause_deform 은 MODEL_KEYS 에 있으면서도 이 목록에서 빠져 있었다 —
            # 다중극 경계를 가진 천체(Proxima b)의 로브가 조용히 cfg 에서 사라졌다. 2026-08-16 수정.
            for k in ('pause_radius', 'pause_compression', 'pause_extension',
                      'pause_height_scale', 'pause_deform'):
                if k in m:
                    L.append(f"  {k} = {fmt(m[k])}")
            L.append(f"  pause_quality = {fmt(QUALITY['pause'])}")
        L.append("}")
        L.append("RadiationBody:NEEDS[NearStarsSystem]")
        L.append("{")
        L.append(f"  name = {name}")
        L.append(f"  radiation_model = {s['model_name']}")
        for k in BODY_KEYS:
            if k in s['body']:
                L.append(f"  {k} = {fmt(s['body'][k])}")
        L.append("}")
    return "\n".join(L) + "\n"


if __name__ == '__main__':
    text = emit()
    check(text)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        f.write(text)
    print("wrote", os.path.normpath(OUT))
    specs = load_nearstars_specs()
    if specs:
        with open(OUT_NS, 'w') as f:
            f.write(emit_nearstars(specs))
        print("wrote", os.path.normpath(OUT_NS), f"({len(specs)} bodies)")
