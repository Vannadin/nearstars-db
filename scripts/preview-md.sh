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
