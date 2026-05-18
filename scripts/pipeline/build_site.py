# db/systems/*.json 전체를 docs/data.json 하나로 합치는 빌드 스크립트
import json, glob, os

base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
systems_dir = os.path.join(base, 'db', 'systems')
output = os.path.join(base, 'docs', 'data.json')

files = sorted(glob.glob(os.path.join(systems_dir, '*.json')))
data = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        data.append(json.load(fh))

os.makedirs(os.path.dirname(output), exist_ok=True)
with open(output, 'w', encoding='utf-8') as fh:
    json.dump(data, fh, ensure_ascii=False, separators=(',', ':'))

print(f'docs/data.json 생성 완료: {len(data)}개 시스템')
