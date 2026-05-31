#!/usr/bin/env bash
# 마크다운 파일을 GitHub 스타일 HTML로 임시 렌더링해서 브라우저에서 열어주는 미리보기 도구

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $(basename "$0") <markdown-file> [more-files...]" >&2
  echo "  Renders each .md to /tmp/preview-<basename>.html and opens in browser." >&2
  exit 1
fi

for src in "$@"; do
  if [ ! -f "$src" ]; then
    echo "Not found: $src" >&2
    continue
  fi
  abs=$(cd "$(dirname "$src")" && pwd)/$(basename "$src")
  base=$(basename "$src" .md)
  out="/tmp/preview-${base}.html"

  python3 - "$abs" "$out" <<'PYEOF'
import re, sys, pathlib

src_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])

raw = src_path.read_text()
md = re.sub(r'^---\n.*?\n---\n+', '', raw, count=1, flags=re.DOTALL)
md_safe = md.replace('</script>', '<\\/script>')
title = next((ln[2:].strip() for ln in md.splitlines() if ln.startswith('# ')), src_path.stem)

template = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>__TITLE__</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5.5.0/github-markdown-light.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<style>
  body { box-sizing: border-box; min-width: 200px; max-width: 980px; margin: 0 auto; padding: 45px; }
  @media (max-width: 767px) { body { padding: 15px; } }
  .markdown-body table { display: table; width: 100%; }
  .markdown-body blockquote { color: #1f6feb; border-left-color: #1f6feb; background: #f0f6ff; padding: 8px 16px; border-radius: 4px; }
  .markdown-body h1 { border-bottom: 2px solid #d0d7de; }
  .markdown-body h2 { border-bottom: 1px solid #d0d7de; margin-top: 28px; }
  footer { color: #57606a; font-size: 0.85em; margin-top: 48px; padding-top: 12px; border-top: 1px solid #d0d7de; }
</style>
</head>
<body class="markdown-body">
<div id="content"></div>
<footer>Source: <code>__SRC__</code></footer>
<script type="text/markdown" id="src">__MD__</script>
<script>
  const md = document.getElementById('src').textContent;
  document.getElementById('content').innerHTML = marked.parse(md, { gfm: true, breaks: false });
  // 색 카탈로그 등에서 첫 열이 "color"인 표의 색 이름 셀 앞에 참고용 색 칩을 주입 (en/ko 키워드)
  (function(){
    var MAP = [
      [['무지개','rainbow','iridescent','spectral','스펙트럼','full-spectrum','play-of-color','flash','섬광','opal','오팔','nacre','진주층','labradorite','라브라도'], 'linear-gradient(90deg,#ee3322,#eedd00,#22cc44,#2299dd,#8833ee)'],
      [['백열','광휘','glow','glowing','incandescent','빛나는','molten'], 'linear-gradient(90deg,#5a1500,#e8862e,#ffd9a0)'],
      [['황동','금색','gold','brass','electrum','자연금'], 'linear-gradient(135deg,#b8860b,#ffe085,#8a6a00)'],
      [['은회','강철','steely','silver','gunmetal','건메탈','steel','specular'], '#aab2bd'],
      [['회청','grey-blue','gray-blue'], '#6b7a90'],
      [['황록','yellow-green','yellowgreen'], '#a9c520'],
      [['청록','cyan','teal','aquamarine','turquoise','터키석','터쿼이즈'], '#2bb3c0'],
      [['마젠타','magenta'], '#c0398f'],
      [['분홍','장미','살구','salmon','pink','rose'], '#e58aa0'],
      [['보라','자주','purple','violet','lilac','royal'], '#7b3fa0'],
      [['적갈','황갈','갈색','황토','brown','tan','ochre','red-brown','rust'], '#8a6d3b'],
      [['청','남색','blue','cobalt','sapphire','azure','ultramarine','navy'], '#2f6fd0'],
      [['녹','에메랄드','올리브','green','emerald','olive','malachite'], '#2e9e4f'],
      [['주황','orange'], '#e8862e'],
      [['적','진홍','주홍','red','crimson','scarlet','vermilion','ruby'], '#c0392b'],
      [['황','yellow','golden','lemon'], '#e6c100'],
      [['백','흰','white','frost','서리'], '#eef0f2'],
      [['회','grey','gray','hazy','흐림'], '#9aa0a6'],
      [['흑','검','어두','dark','black','jet','sooty'], '#222222'],
    ];
    function swatch(text){
      var t = text.toLowerCase();
      for (var i=0;i<MAP.length;i++){
        var keys = MAP[i][0];
        for (var j=0;j<keys.length;j++){ if (t.indexOf(keys[j])>=0) return MAP[i][1]; }
      }
      return null;
    }
    document.querySelectorAll('#content table').forEach(function(tbl){
      var th = tbl.querySelector('thead th');
      if (!th || th.textContent.trim().toLowerCase() !== 'color') return;
      tbl.querySelectorAll('tbody tr').forEach(function(tr){
        var td = tr.querySelector('td');
        if (!td) return;
        var css = swatch(td.textContent);
        if (!css) return;
        var sp = document.createElement('span');
        sp.style.cssText = 'display:inline-block;width:0.85em;height:0.85em;margin-right:6px;border:1px solid rgba(0,0,0,0.3);border-radius:3px;vertical-align:-1px;background:'+css;
        td.insertBefore(sp, td.firstChild);
      });
    });
  })();
</script>
</body>
</html>
'''

html = (template
    .replace('__TITLE__', title)
    .replace('__SRC__', str(src_path))
    .replace('__MD__', md_safe))
out_path.write_text(html)
print(f'wrote {out_path}')
PYEOF

  open "$out"
done
