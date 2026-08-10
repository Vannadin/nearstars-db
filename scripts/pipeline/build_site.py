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

# file:// 로 열면 Chromium 이 fetch 를 CORS 로 막아 표가 통째로 비므로, 같은 데이터를
# 클래식 <script> 로도 실을 수 있게 사본을 낸다 (index.html 의 폴백 경로).
with open(os.path.join(base, 'docs', 'data.js'), 'w', encoding='utf-8') as fh:
    fh.write('window.NS_DATA=')
    json.dump(data, fh, ensure_ascii=False, separators=(',', ':'))
    fh.write(';')

print(f'docs/data.json 생성 완료: {len(data)}개 시스템 (+ data.js 폴백)')
