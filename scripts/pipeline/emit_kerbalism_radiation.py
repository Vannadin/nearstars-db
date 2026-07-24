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
    'inner_border_deform_xy',
    'outer_dist', 'outer_radius', 'outer_deform_xy', 'outer_compression',
    'outer_extension', 'outer_border_dist', 'outer_border_radius',
    'outer_border_deform_xy',
    'pause_radius', 'pause_compression', 'pause_extension', 'pause_height_scale',
]
BODY_KEYS = ['radiation_inner', 'radiation_outer', 'radiation_pause',
             'geomagnetic_pole_lat', 'geomagnetic_pole_lon', 'geomagnetic_offset']

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
                 '3-16 R_J x +-3 (frame truncation -- the disc runs past 50 R_J). Pause nose 63 R_J.',
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
    L.append("// https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts")
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
    """phase4 보드에서 gated magnetism.radiation_belts 행을 읽어 emit 스펙으로 변환.
    반환: {kopernicus_name: {'model': {...}, 'body': {...}, 'row': row}} (보드 순서)."""
    import yaml
    specs = {}
    for fn in sorted(os.listdir(PHASE4_DIR)):
        if not fn.endswith('.yaml'):
            continue
        board = yaml.safe_load(open(os.path.join(PHASE4_DIR, fn)))
        for row in board.get('decisions', []):
            if row.get('axis') != 'magnetism.radiation_belts' or row.get('status') != 'gated':
                continue
            fields = {f['name']: f['value'] for f in row.get('fields', [])}
            if 'radiation_model' not in fields:
                raise SystemExit(f"{fn} {row['body']}: radiation_belts row has no "
                                 "individual cfg fields (legacy packed format?)")
            name = row.get('kopernicus_name', row['body'])
            model = {k: fields[k] for k in MODEL_KEYS if k in fields}
            body = {k: fields[k] for k in BODY_KEYS if k in fields}
            specs[name] = {'model_name': fields['radiation_model'], 'model': model,
                           'body': body, 'refs': row.get('refs', []), 'system': fn}
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
            for k in ('pause_radius', 'pause_compression', 'pause_extension', 'pause_height_scale'):
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
