#!/usr/bin/env python3
# Phase 4 v2 결정 보드(phase4/<system>.yaml)를 바디별 HTML + 시스템 인덱스로 렌더 —
# (body×axis) 결정마다 산문 narrative(읽기 좋은 sans 문단) + typed fields(정확한 수치 spec 표) 병기.
# 천체별 1페이지로 분리(혼동 방지). NearStars Design System v2 토큰 사용. 슬러그=_naming.to_url_slug.
"""Render a schema_version:2 Phase 4 board into per-body pages + a system index.

Usage: python3 scripts/phase4/build_phase4_html.py alpha_centauri
Writes docs/phase4/<system-slug>/index.html + one <body-slug>.html per body.
"""
import html
import re
import datetime
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from pipeline._naming import to_url_slug  # noqa: E402
from pipeline._nav import global_bar  # noqa: E402

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}")


def body_slug(b):
    # 와일드카드 바디("*", 행성 공통 행)는 to_url_slug가 빈 문자열을 내므로 고정 슬러그 사용
    return "system-wide" if b.strip("* ") == "" else to_url_slug(b)

STATUS_LABEL = {
    "gated": ("확정", "Gated"), "passthrough": ("손대지 않음", "Passthrough"),
    "open": ("미결", "Open"), "art-directed": ("연출", "Art-directed"),
    "emitted": ("반영", "Emitted"), "superseded": ("대체됨", "Superseded"),
}
VERDICT_LABEL = {
    "pass-in-window": ("허용 범위 내", "In-window"),
    "documented-divergence": ("문서화 이탈", "Doc. divergence"),
    "owner-override": ("오너 확정", "Owner override"),
    "methodology-derived": ("방법론 도출", "Methodology-derived"),
}


def esc(s):
    return html.escape("" if s is None else str(s))


def _nullish(x):
    return (not x) or str(x).strip().lower() == "null"


def bi(en, ko):
    """Bilingual prose: default (data-i18n) = ko mirror, data-en = English source.
    English is source-of-truth; during migration one side may be missing, in which
    case render whichever exists untoggled so un-migrated bodies keep working."""
    e = esc(en).replace("\n", "<br>").strip() if not _nullish(en) else ""
    k = esc(ko).replace("\n", "<br>").strip() if not _nullish(ko) else ""
    if e and k:
        return f'<span data-i18n>{k}</span><span data-en hidden>{e}</span>'
    return e or k


def value_html(value):
    def repl(m):
        h = m.group(0)
        return f'<span class="chip" style="background:{h}"></span><span class="hx">{h}</span>'
    return HEX_RE.sub(repl, esc(value))


def fields_of(d):
    """fields가 없고 행 레벨 value만 있는 행(v1형)을 한 줄 표로 승격"""
    fields = d.get("fields")
    if fields:
        return fields
    if d.get("value") is not None:
        return [{"name": d.get("axis", "value"), "value": d["value"]}]
    return None


def fields_table(fields):
    if not fields:
        return ""
    body = []
    for f in fields:
        if not isinstance(f, dict):
            body.append(f'<tr><td colspan="3" class="v">{value_html(f)}</td></tr>')
            continue
        name = esc(f.get("name", ""))
        div = f.get("verdict") == "documented-divergence"
        ovr = f.get("verdict") == "owner-override"
        warn = ' <span class="mini" title="documented divergence">⚠</span>' if div else ""
        if ovr:
            warn = ' <span class="mini" title="owner override: 물리가 지지하지 않는 연출 선택 (근거 참조)">✳</span>'
        raw = f.get("value")
        if raw is None and f.get("na_reason"):
            val = '<span data-i18n>없음</span><span data-en hidden>N/A</span>'
        elif isinstance(raw, str) and not _nullish(f.get("value_ko")):
            # bilingual field value: `value` is the English source, `value_ko` its mirror
            val = bi(raw, f.get("value_ko"))
        else:
            val = value_html(raw)
        if f.get("unit"):
            val += f' <span class="u">{esc(f["unit"])}</span>'
        if f.get("reference_radius_km"):
            val += f' <span class="u">· R_ref {esc(f["reference_radius_km"])} km</span>'
        if f.get("window"):
            val += f' <span class="win">window {value_html(f["window"])}</span>'
        colors = f.get("colors")
        if isinstance(colors, dict):
            val += ('<div class="swatches">' + "".join(
                f'<span class="sw"><span class="chip" style="background:{esc(c)}"></span>'
                f'{esc(n)} <span class="hx">{esc(c)}</span></span>'
                for n, c in colors.items()) + "</div>")
        # note / na_reason / phase3_default follow the prose contract: the base key is
        # the English source, `<key>_ko` its mirror. Legacy single-language entries
        # (most of the board) render untoggled via bi()'s fallback.
        if f.get("na_reason"):
            val += f'<div class="fnote">{bi(f["na_reason"], f.get("na_reason_ko"))}</div>'
        if f.get("note"):
            val += f'<div class="fnote">{bi(f["note"], f.get("note_ko"))}</div>'
        if f.get("phase3_default"):
            val += (f'<div class="fnote p3">Phase 3: '
                    f'{bi(f["phase3_default"], f.get("phase3_default_ko"))}</div>')
        op = f.get("op")
        opcell = f'<span class="op {esc(op)}">{esc(op)}</span>' if op and op != "set" else ""
        body.append(
            f'<tr{" class=d" if div else ""}>'
            f'<td class="k">{name}{warn}</td>'
            f'<td class="v">{val}</td>'
            f'<td class="o">{opcell}</td></tr>')
    return ('<table class="spec"><thead><tr>'
            '<th><span data-i18n>필드</span><span data-en hidden>Field</span></th>'
            '<th><span data-i18n>값</span><span data-en hidden>Value</span></th>'
            '<th></th></tr></thead><tbody>' + "".join(body) + "</tbody></table>")


MOON_COLS = (("a_km", "a (km)"), ("e", "e"), ("inc_deg", "inc°"), ("lan_deg", "Ω°"),
             ("argp_deg", "ω°"), ("ma_deg", "M°"), ("epoch", "epoch"),
             ("mass_kg", "mass (kg)"), ("radius_km", "R (km)"))


def moons_table(moons):
    """Body-def ledger for invented satellite systems — the 1:1 Kopernicus/Principia
    orbit source, so it must be visible on the review page."""
    if not moons:
        return ""
    head = "<th>moon</th>" + "".join(f"<th>{esc(h)}</th>" for _, h in MOON_COLS)
    rows = []
    for m in moons:
        if not isinstance(m, dict):
            continue
        cells = f'<td class="k">{esc(m.get("name",""))}</td>' + "".join(
            f'<td class="v">{esc(m.get(k, "—"))}</td>' for k, _ in MOON_COLS)
        rows.append(f"<tr>{cells}</tr>")
        design = m.get("design")
        if isinstance(design, dict):  # design prototype paired under the live (snapshot) row
            dcells = ('<td class="k dsn">└ <span data-i18n>설계 t=0</span>'
                      '<span data-en hidden>design t=0</span></td>') + "".join(
                f'<td class="v dsn">{esc(design[k]) if k in design else "·"}</td>'
                for k, _ in MOON_COLS)
            rows.append(f'<tr class="mdesign">{dcells}</tr>')
        if m.get("note"):
            rows.append(f'<tr class="mnote"><td></td><td colspan="{len(MOON_COLS)}">'
                        f'<div class="fnote">{bi(m["note"], m.get("note_ko"))}</div></td></tr>')
    return ('<div class="moonwrap"><table class="spec moons"><thead><tr>' + head
            + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


REPO_BLOB = "https://github.com/Vannadin/nearstars-db/blob/main/"


def ref_url(r):
    """Map a ref to a live URL:
    - arXiv new/old-style -> arxiv.org
    - a repo doc path (docs/reference/*.md, plans/*.md) -> its built wiki page
    - any other repo .md path -> the GitHub blob (not rendered to the wiki)
    - otherwise an ADS bibcode -> ui.adsabs.harvard.edu."""
    s = str(r).strip()
    if re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", s):                 # 2508.03814
        return "https://arxiv.org/abs/" + s
    if re.fullmatch(r"[a-z-]+(\.[A-Z]{2})?/\d{7}(v\d+)?", s):     # astro-ph/0612671
        return "https://arxiv.org/abs/" + s
    if s.endswith(".md"):                                        # our own docs, not a bibcode
        m = re.fullmatch(r"docs/reference/(.+)\.md", s)
        if m:
            return "../../wiki/reference__" + m.group(1) + ".html"
        # plans/ 는 미발행(내부 문서, 오너 2026-08-13) → 저장소 파일 뷰로
        if re.fullmatch(r"plans/(.+)\.md", s):
            return REPO_BLOB + s
        return REPO_BLOB + s                                     # e.g. phase3/stability-sim/*.md
    return "https://ui.adsabs.harvard.edu/abs/" + quote(s, safe="")  # ADS bibcode


def ref_label(r):
    """Display text for a ref: doc paths show just the filename (full paths
    read badly next to bibcodes); everything else shows verbatim."""
    s = str(r).strip()
    return s.rsplit("/", 1)[-1] if s.endswith(".md") else s


def refs_html(refs):
    if not refs:
        return ""
    if isinstance(refs, str):  # defensive — the validator rejects this, but never render per-char
        refs = [refs]
    return '<div class="refs">' + "".join(
        f'<a class="ref" href="{esc(ref_url(r))}" target="_blank" rel="noopener">{esc(ref_label(r))}</a>'
        for r in refs) + "</div>"


def decision_html(d):
    status = d.get("status", "")
    gate = d.get("gate") or {}
    verdict = gate.get("verdict", "")
    div = verdict == "documented-divergence"
    vclass = {"documented-divergence": "vd-div",
              "owner-override": "vd-ovr",
              "methodology-derived": "vd-meth"}.get(verdict, "vd-ok")

    sk, se = STATUS_LABEL.get(status, (status, status))
    pills = (f'<span class="pill st-{esc(status)}">'
             f'<span data-i18n>{esc(sk)}</span><span data-en hidden>{esc(se)}</span></span>')
    if verdict:
        vk, ve = VERDICT_LABEL.get(verdict, (verdict, verdict))
        pills += (f'<span class="pill {vclass}">'
                  f'<span data-i18n>{esc(vk)}</span><span data-en hidden>{esc(ve)}</span></span>')

    narrative = bi(d.get("narrative"), d.get("narrative_ko"))
    nar = f'<p class="narrative">{narrative}</p>' if narrative else ""


    ev = bi(gate.get("evidence"), gate.get("evidence_ko"))
    ev_html = f'<div class="ev"><span class="tag">evidence</span> {ev}</div>' if ev else ""
    dn = bi(gate.get("divergence_note"), gate.get("divergence_note_ko"))
    dn_html = ""
    if dn:
        dn_html = (f'<div class="ev div"><span class="tag">divergence</span> '
                   f'{dn}</div>')
    dep = d.get("depends_on")
    dep_html = ""
    if dep:
        dep = [dep] if isinstance(dep, str) else dep
        dep_html = ('<div class="disc"><span class="tag">depends on</span> '
                    + " · ".join(f"<code>{esc(x)}</code>" for x in dep) + "</div>")

    return f"""<article class="dec{' is-div' if div else ''}{' is-sup' if status=='superseded' else ''}" id="{esc(d.get('axis',''))}">
  <div class="dec-head">
    <code class="axis">{esc(d.get('axis',''))}</code>
    <span class="pills">{pills}</span>
  </div>
  {nar}
  {fields_table(fields_of(d))}
  {figures_html(d)}
  {moons_table(d.get('moons'))}
  {dep_html}{ev_html}{dn_html}
  {refs_html(d.get('refs'))}
</article>"""


IMG_RE = re.compile(r"docs/img/[\w./-]+\.(?:png|jpg|jpeg|svg)")


def figures_of(d):
    """Figures this decision cites, in first-mention order.

    Boards already name their diagrams inline — "Shape diagram:
    docs/img/field-geometry-proxima-c.png" sits in the row's own note — so a figure
    belongs to the row that raised it and no second mapping has to be curated. A
    path that no longer resolves is dropped with a warning, not emitted broken.
    """
    out = []
    blob = yaml.safe_dump(d, allow_unicode=True, default_flow_style=False)
    for path in IMG_RE.findall(blob):
        if path in out:
            continue
        if not (REPO / path).exists():
            print(f"[warn] {d.get('body','?')} / {d.get('axis','?')}: "
                  f"cited figure not found — {path}", file=sys.stderr)
            continue
        out.append(path)
    return out


def figures_html(d):
    """The row's figures, attached inside it — thumbnail now, full size on click."""
    figs = figures_of(d)
    if not figs:
        return ""
    items = "".join(
        f'<a class="fig" href="../../{path[len("docs/"):]}" target="_blank" rel="noopener">'
        f'<img src="../../{path[len("docs/"):]}" alt="{esc(d.get("axis",""))} figure" '
        f'loading="lazy"></a>'
        for path in figs)
    return f'<div class="figs">{items}</div>'


def body_stats(rows):
    ng = sum(1 for d in rows if d.get("status") in ("gated", "emitted"))
    npt = sum(1 for d in rows if d.get("status") == "passthrough")
    nd = sum(1 for d in rows if (d.get("gate") or {}).get("verdict") == "documented-divergence")
    nopen = sum(1 for d in rows if d.get("status") in ("open", "art-directed"))
    return {"total": len(rows), "gated": ng, "passthrough": npt, "divergence": nd, "open": nopen}


LEGEND = """<details class="legend"><summary><span data-i18n>표시 읽는 법</span><span data-en hidden>How to read the badges</span></summary>
<dl>
  <dt><span class="pill st-gated"><span data-i18n>확정</span><span data-en hidden>Gated</span></span></dt>
  <dd><span data-i18n>이 축의 값을 Phase 4에서 정해 굳혔다.</span><span data-en hidden>The value for this axis was decided here and frozen.</span></dd>
  <dt><span class="pill st-passthrough"><span data-i18n>손대지 않음</span><span data-en hidden>Passthrough</span></span></dt>
  <dd><span data-i18n>정할 것이 없어 앞 단계 값이 그대로 나간다.</span><span data-en hidden>Nothing to decide; the earlier value goes out unchanged.</span></dd>
  <dt><span class="pill vd-ok"><span data-i18n>허용 범위 내</span><span data-en hidden>In-window</span></span></dt>
  <dd><span data-i18n>고른 값이 물리적으로 허용되는 구간 안에 있다.</span><span data-en hidden>The chosen value sits inside the physically allowed range.</span></dd>
  <dt><span class="pill vd-meth"><span data-i18n>방법론 도출</span><span data-en hidden>Methodology-derived</span></span></dt>
  <dd><span data-i18n>값을 근거 문서의 계산으로 얻었다.</span><span data-en hidden>The value was computed by a documented method.</span></dd>
  <dt><span class="pill vd-ovr"><span data-i18n>오너 확정</span><span data-en hidden>Owner override</span></span></dt>
  <dd><span data-i18n>물리가 지지하지 않는데도 연출을 위해 택했다. 이유는 근거 항목에 있다.</span><span data-en hidden>Chosen for the look even though the physics does not support it; the reason is in the evidence.</span></dd>
  <dt><span class="pill vd-div"><span data-i18n>문서화 이탈</span><span data-en hidden>Doc. divergence</span></span></dt>
  <dd><span data-i18n>원작·관측과 어긋나지만 그 사실을 기록해 두었다.</span><span data-en hidden>It departs from canon or observation, and that departure is recorded.</span></dd>
  <dt><span class="mini">⚠ ✳</span></dt>
  <dd><span data-i18n>행이 아니라 필드 하나에 붙는 같은 표시. ⚠는 문서화 이탈, ✳는 오너 확정.</span><span data-en hidden>The same marks at single-field level: ⚠ documented divergence, ✳ owner override.</span></dd>
</dl></details>"""


def render_body(system, body, rows, alias, prev_link, next_link):
    st = body_stats(rows)
    meta = (f'{st["total"]} <span data-i18n>결정</span><span data-en hidden>decisions</span> · '
            f'{st["gated"]} gated · {st["divergence"]} divergence'
            + (f' · {st["open"]} open' if st["open"] else ""))
    decs = "\n".join(decision_html(d) for d in rows)
    # 축 앵커 목차 — 보드가 길어 특정 축으로 바로 못 가던 문제(2026-08-10 UX 점검).
    axes = [d.get("axis", "") for d in rows if d.get("axis")]
    toc = ('<nav class="axis-toc" aria-label="Decisions on this page">'
           + "".join(f'<a href="#{esc(a)}">{esc(a)}</a>' for a in axes)
           + '</nav>') if len(axes) > 3 else ""
    nav = []
    if prev_link:
        nav.append(f'<a class="navlink" href="{prev_link[0]}">← {esc(prev_link[1])}</a>')
    if next_link:
        nav.append(f'<a class="navlink" href="{next_link[0]}">{esc(next_link[1])} →</a>')
    nav_html = f'<div class="bodynav">{"".join(nav)}</div>' if nav else ""
    alias_html = f' <span class="alias">{esc(alias)}</span>' if alias else ""

    # Back-link to the Phase 3 synthesis for this body, when one exists. Board
    # body-slugs equal Phase 3 slugs (art-name-only bodies have no synthesis),
    # so a source-file check is authoritative.
    p3_slug = body_slug(body)
    p3_link = (
        f' · <a href="../../phase3/{p3_slug}.html">'
        f'<span data-i18n>Phase 3 합성 ↗</span><span data-en hidden>Phase 3 synthesis ↗</span></a>'
        if (REPO / "docs" / "phase3" / f"{p3_slug}.md").exists() else ""
    )

    content = f"""<nav class="crumb">
  <a href="../../wiki/reference__methodology-index.html"><span data-i18n>방법론</span><span data-en hidden>Methodology</span></a> ·
  <a href="../index.html">Phase 4</a> ·
  <a href="index.html"><span class="sys">{esc(system)}</span></a> ·
  <span class="here">{esc(body)}</span>{p3_link}
</nav>
<header>
  <h1>{esc(body)}{alias_html}</h1>
  <div class="spacer"></div>
  {LANG_SEG}
  <div class="seg"><button id="collapse"><span data-i18n>설명 접기</span><span data-en hidden>Collapse</span></button></div>
</header>
<div class="summary"><span class="body-meta">{meta}</span></div>
{toc}
{LEGEND}
<div class="decisions">{decs}</div>
{nav_html}
{build_stamp()}"""
    return page(f"Phase 4 — {system} / {body}", content)


def render_index(system, order, bodies, aliases):
    total = sum(len(bodies[b]) for b in order)
    ndiv = sum(1 for b in order for d in bodies[b]
               if (d.get("gate") or {}).get("verdict") == "documented-divergence")
    cards = []
    for b in order:
        st = body_stats(bodies[b])
        slug = body_slug(b)
        alias = aliases.get(b)
        alias_html = f'<span class="alias">{esc(alias)}</span>' if alias else ""
        badges = [f'<span class="mini-pill g">{st["gated"]} gated</span>']
        if st["divergence"]:
            badges.append(f'<span class="mini-pill d">{st["divergence"]} div</span>')
        if st["passthrough"]:
            badges.append(f'<span class="mini-pill p">{st["passthrough"]} pass</span>')
        if st["open"]:
            badges.append(f'<span class="mini-pill o">{st["open"]} open</span>')
        cards.append(f"""<a class="body-card" href="{slug}.html">
  <div class="bc-head"><span class="bc-name">{esc(b)}</span>{alias_html}</div>
  <div class="bc-count">{st["total"]} <span data-i18n>결정</span><span data-en hidden>decisions</span></div>
  <div class="bc-badges">{"".join(badges)}</div>
</a>""")
    content = f"""<nav class="crumb">
  <a href="../../wiki/reference__methodology-index.html"><span data-i18n>방법론</span><span data-en hidden>Methodology</span></a> ·
  <a href="../index.html">Phase 4</a> · <span class="here"><span class="sys">{esc(system)}</span></span>
</nav>
<header>
  <h1><span data-i18n>Phase 4 결정 보드</span><span data-en hidden>Phase 4 decision board</span> · <span class="sys">{esc(system)}</span></h1>
  <div class="spacer"></div>
  {LANG_SEG}
</header>
<p class="intro"><span data-i18n>art-direction을 고증 게이트로 검증한 emit용 확정값. 천체를 골라 그 바디의 결정(산문 근거 + 정확한 수치)을 봅니다.</span><span data-en hidden>Art-direction validated against the 고증 gate. Pick a body to see its decisions — prose reasoning next to the exact emit numbers.</span></p>
<div class="summary">
  <span><b>{len(order)}</b> <span data-i18n>바디</span><span data-en hidden>bodies</span></span>
  <span><b>{total}</b> <span data-i18n>결정</span><span data-en hidden>decisions</span></span>
  <span><b>{ndiv}</b> documented-divergence</span>
</div>
<div class="body-grid">{"".join(cards)}</div>"""
    return page(f"Phase 4 — {system}", content)


LANG_SEG = ('<div class="seg"><button id="ko">한</button>'
            '<button id="en" class="on">EN</button></div>')

SCRIPT = """<script>
const b=document.body;
function setLang(en){
  document.querySelectorAll('[data-i18n]').forEach(e=>e.hidden=en);
  document.querySelectorAll('[data-en]').forEach(e=>e.hidden=!en);
  ko_.classList.toggle('on',!en); en_.classList.toggle('on',en);
}
const ko_=document.getElementById('ko'), en_=document.getElementById('en');
ko_.onclick=()=>{setLang(false);localStorage.setItem('nearstars-lang','ko');};
en_.onclick=()=>{setLang(true);localStorage.setItem('nearstars-lang','en');};
// English is the default view; a stored choice wins.
setLang(localStorage.getItem('nearstars-lang') !== 'ko');
const cb=document.getElementById('collapse');
if(cb) cb.onclick=e=>{b.classList.toggle('collapsed');
  e.currentTarget.classList.toggle('on',b.classList.contains('collapsed'));};
</script>"""


def build_stamp():
    """Build time + source revision, so a stale page in a browser tab is obvious."""
    import subprocess
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                             capture_output=True, text=True, timeout=5).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "phase4"], cwd=REPO,
                               capture_output=True, text=True, timeout=5).stdout.strip()
        rev = f"{sha}{'+미커밋' if dirty else ''}" if sha else ""
    except Exception:
        rev = ""
    return f'<div class="stamp">빌드 {ts}{" · " + rev if rev else ""}</div>'


def page(title, content, depth=2):
    return f"""<!DOCTYPE html>
<!-- autogenerated by scripts/phase4/build_phase4_html.py from phase4/*.yaml (schema v2). Do not hand-edit. -->
<html lang="en" data-ns="v2" class="ns-light-ok">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<link href="{'../' * depth}assets/fonts/geist.css" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
{global_bar('../' * depth, 'Phase 4' if depth == 1 else None)}
{_split_head(content)}
{SCRIPT}
</body>
</html>"""


def _split_head(content):
    """크럼+헤더를 전폭 스트립(.pagehead)으로 분리 — 다른 표면들과 좌측 정렬을 맞춤.
    본문(요약·결정 카드)은 기존 중앙 열(.wrap)에 남는다."""
    if "</header>" in content:
        head, rest = content.split("</header>", 1)
        return (f'<div class="pagehead">{head}</header></div>\n'
                f'<div class="wrap">{rest}</div>')
    return f'<div class="wrap">{content}</div>'


STYLE = """
:root {
  --bg:#06070a; --fg1:rgba(255,255,255,.94); --fg2:rgba(255,255,255,.80); --fg3:rgba(255,255,255,.56);
  --fg4:rgba(255,255,255,.46); --s1:rgba(255,255,255,.022); --s2:rgba(255,255,255,.045);
  --s3:rgba(255,255,255,.07); --bd1:rgba(255,255,255,.05); --bd2:rgba(255,255,255,.09);
  --accent:#7aa8ff; --accent-bg:rgba(122,168,255,.10);
  --ok:#4ec9b0; --ok-bg:rgba(78,201,176,.12); --warn:#e0b070; --warn-bg:rgba(224,176,112,.12);
  --danger:#e090d0; --danger-bg:rgba(224,144,208,.14);
  --ovr:#c9a227; --ovr-bg:rgba(201,162,39,.13);
  --meth:#3a9ec9; --meth-bg:rgba(58,158,201,.13);
  --sans:'Geist','Inter',system-ui,-apple-system,'Noto Sans KR',sans-serif;
  --mono:'Geist Mono','SF Mono',Menlo,monospace;
  --grad:
    radial-gradient(60% 50% at 18% -10%, rgba(122,168,255,.07), transparent 70%),
    radial-gradient(50% 45% at 92% 110%, rgba(224,144,208,.05), transparent 70%);
}
/* 라이트 테마 — 브라우저 설정(prefers-color-scheme)을 따른다. 값은 v2 라이트 팔레트. */
@media (prefers-color-scheme: light) {
  html.ns-light-ok {
    --bg:#f5f6fa;
    --grad:
      radial-gradient(58% 48% at 16% -12%, rgba(47,102,216,.07), transparent 70%),
      radial-gradient(48% 44% at 94% 108%, rgba(168,58,142,.05), transparent 70%);
    --fg1:rgba(9,12,22,.95); --fg2:rgba(9,12,22,.80); --fg3:rgba(9,12,22,.66);
    --fg4:rgba(9,12,22,.60);
    --s1:rgba(12,17,34,.030); --s2:rgba(12,17,34,.055); --s3:rgba(12,17,34,.085);
    --bd1:rgba(12,17,34,.08); --bd2:rgba(12,17,34,.13);
    --accent:#114edd; --accent-bg:rgba(17,78,221,.10);
    --ok:#1e6657; --ok-bg:rgba(30,102,87,.12);
    --warn:#765419; --warn-bg:rgba(118,84,25,.13);
    --danger:#992c83; --danger-bg:rgba(153,44,131,.12);
    --ovr:#6c5815; --ovr-bg:rgba(108,88,21,.13);
    --meth:#21607c; --meth-bg:rgba(33,96,124,.13);
    --accent-hover:#0a3fb0;
  }
}

* { box-sizing:border-box; margin:0; padding:0 }
html,body { max-width:100vw; overflow-x:clip }
body {
  background: var(--grad), var(--bg);
  background-attachment:fixed; color:var(--fg2);
  font-family:var(--sans); font-size:14px; line-height:1.6;
  font-feature-settings:'ss01','cv11','tnum'; -webkit-font-smoothing:antialiased;
}
a { color:var(--accent); text-decoration:none }
a:hover { color:var(--accent-hover,#aac8ff) }
.wrap { max-width:940px; margin:0 auto; padding:20px 22px 90px }
.pagehead { padding:16px 28px 2px; border-bottom:1px solid var(--bd1) }
@media (max-width:600px) { .pagehead { padding:12px 16px 2px } }
.crumb { font-family:var(--mono); font-size:11.5px; color:var(--fg4); margin-bottom:14px }
.crumb a { color:var(--fg3) } .crumb .here { color:var(--fg2) } .crumb .sys { color:var(--accent) }
header { display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:6px }
h1 { font-size:20px; font-weight:600; letter-spacing:-.01em; color:var(--fg1) }
h1 .alias, h1 .sys { color:var(--accent); font-weight:400; font-size:14px; font-family:var(--mono) }
.spacer { margin-left:auto }
.intro { color:var(--fg3); font-size:13px; max-width:720px; line-height:1.7; margin:6px 0 16px }
.summary { display:flex; gap:18px; flex-wrap:wrap; font-size:12px; color:var(--fg4);
  font-family:var(--mono); font-variant-numeric:tabular-nums; margin-bottom:22px;
  padding-bottom:14px; border-bottom:1px solid var(--bd1) }
.summary b { color:var(--fg2); font-weight:500 }
.body-meta { font-family:var(--mono); font-size:11.5px; color:var(--fg4) }
/* figures attached inside a decision row — no chrome, just the picture */
.figs { display:flex; flex-wrap:wrap; gap:10px; margin:10px 0 2px }
.figs .fig { display:block; max-width:min(420px, 100%); border:1px solid var(--bd2);
  border-radius:10px; overflow:hidden; background:var(--s2); line-height:0 }
.figs .fig:hover { border-color:rgba(122,168,255,.4) }
.figs .fig img { display:block; width:100%; height:auto }
.axis-toc { display:flex; flex-wrap:wrap; gap:5px; margin:2px 0 12px }
.axis-toc a { font-family:var(--mono); font-size:11px; color:var(--fg3); text-decoration:none;
  background:var(--s1); border:1px solid var(--bd2); border-radius:6px; padding:3px 8px }
.axis-toc a:hover { color:var(--fg1); background:var(--s2); border-color:var(--bd1) }
.dec { scroll-margin-top:14px }
@media (max-width:700px){
  .axis-toc a{min-height:36px;display:inline-flex;align-items:center;padding:0 11px;font-size:12px}
  .crumb a,.crumb .here{min-height:36px;display:inline-flex;align-items:center}
  .wrap{padding:14px 13px 70px} .pagehead{padding:12px 14px 2px}
  .dec{padding:12px 13px} .spec th,.spec td{font-size:12px}
  .narr{font-size:14px;line-height:1.72}
  .ref{min-height:36px;display:inline-flex;align-items:center}
  .navlink{min-height:40px;display:inline-flex;align-items:center;padding:0 13px}
}
/* decision cards */
.decisions { display:flex; flex-direction:column; gap:10px }
.dec { background:var(--s1); border:1px solid var(--bd2); border-radius:12px; padding:14px 16px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.05); scroll-margin-top:16px }
.dec.is-div { border-left:2px solid var(--danger) }
.dec.is-sup { opacity:.5 }
.dec-head { display:flex; align-items:center; gap:10px; flex-wrap:wrap }
.axis { font-family:var(--mono); font-size:12.5px; color:var(--accent); background:var(--accent-bg);
  padding:2px 8px; border-radius:6px }
.pills { display:flex; gap:5px; flex-wrap:wrap; margin-left:auto }
.pill { font:600 11px/1.4 var(--sans); letter-spacing:.03em; text-transform:uppercase;
  padding:2px 9px; border-radius:999px }
.pill.st-gated,.pill.st-emitted { color:var(--ok); background:var(--ok-bg) }
.pill.st-passthrough { color:var(--fg4); background:var(--s2) }
.pill.st-open,.pill.st-art-directed { color:var(--warn); background:var(--warn-bg) }
.pill.st-superseded { color:var(--fg4); background:var(--s2); text-decoration:line-through }
.pill.vd-ok { color:var(--ok); background:var(--ok-bg) }
.pill.vd-div { color:var(--danger); background:var(--danger-bg) }
.pill.vd-ovr { color:var(--ovr); background:var(--ovr-bg) }
.pill.vd-meth { color:var(--meth); background:var(--meth-bg) }
.stamp { margin:26px 0 0; padding-top:11px; border-top:1px solid var(--bd1);
  font:400 11px/1.4 var(--mono); color:var(--fg4); letter-spacing:.02em }
.legend { margin:0 0 18px; border:1px solid var(--bd1); border-radius:10px; background:var(--s1) }
.legend > summary { padding:9px 13px; cursor:pointer; font:500 12px/1.4 var(--sans);
  color:var(--fg3); list-style:none }
.legend > summary::-webkit-details-marker { display:none }
.legend > summary::before { content:"?"; display:inline-grid; place-items:center;
  width:15px; height:15px; margin-right:8px; border-radius:50%; background:var(--s3);
  color:var(--fg3); font:600 11px/1 var(--sans); vertical-align:-2px }
.legend > summary:hover { color:var(--fg1) }
.legend[open] > summary { border-bottom:1px solid var(--bd1) }
.legend dl { margin:0; padding:11px 13px 13px;
  display:grid; grid-template-columns:auto minmax(0,1fr); gap:7px 12px; align-items:baseline }
.legend dt { margin:0 }
.legend dd { margin:0; font:400 12.5px/1.5 var(--sans); color:var(--fg3) }
@media (max-width:560px){ .legend dl { grid-template-columns:minmax(0,1fr); gap:3px }
  .legend dd { margin-bottom:6px } }
.narrative { color:var(--fg2); font-size:13.5px; line-height:1.75; margin:9px 0 10px; max-width:70ch }
table.spec { width:100%; border-collapse:collapse; margin:6px 0 2px;
  font-family:var(--mono); font-variant-numeric:tabular-nums }
.spec th { text-align:left; font:500 9.5px/1 var(--sans); text-transform:uppercase; letter-spacing:.1em;
  color:var(--fg4); padding:0 10px 5px; border-bottom:1px solid var(--bd1) }
.spec td { padding:5px 10px; border-bottom:1px solid var(--bd1); font-size:12px; vertical-align:top }
.spec tr:last-child td { border-bottom:none }
.spec tr.d td.k { color:var(--danger) }
.spec td.k { color:var(--fg3); white-space:nowrap; width:1%; padding-right:22px }
.spec td.v { color:var(--fg1); word-break:break-word }
.spec td.o { text-align:right; width:1% }
.spec .u { color:var(--fg4); font-size:11px } .spec .hx { color:var(--fg2) }
.spec .win { color:var(--fg4); font-size:11.5px; border:1px solid var(--bd1); border-radius:4px;
  padding:1px 6px; margin-left:6px; white-space:nowrap }
.fnote { color:var(--fg4); font-size:11.5px; font-family:var(--sans); line-height:1.5; margin-top:3px; max-width:64ch }
.fnote.p3 { color:var(--fg4); font-style:italic }
.swatches { display:flex; gap:6px 12px; flex-wrap:wrap; margin-top:5px }
.swatches .sw { font-size:11.5px; color:var(--fg3); white-space:nowrap }
.swatches .hx { color:var(--fg4); font-size:9.5px }
.moonwrap { overflow-x:auto; margin:8px 0 2px }
.spec.moons td.v { white-space:nowrap }
.spec.moons tr.mnote td { border-bottom:1px solid var(--bd1); padding-top:0 }
.spec.moons tr.mnote + tr td { border-top:none }
.spec.moons tr td { border-bottom:none }
.spec.moons tr.mdesign td, .spec.moons td.dsn { color:var(--fg4); font-size:11.5px; padding-top:0 }
.spec.moons tr.mdesign td.k { font-family:var(--sans); font-size:11px }
.spec.moons tr:last-child td, .spec.moons tr.mnote td { border-bottom:1px solid var(--bd1) }
.op { font-family:var(--sans); font-size:9px; font-weight:600; text-transform:uppercase; color:var(--warn);
  background:var(--warn-bg); border-radius:4px; padding:1px 5px }
.mini { color:var(--danger) }
.chip { display:inline-block; width:11px; height:11px; border-radius:3px; vertical-align:-1px;
  margin-right:5px; border:1px solid rgba(255,255,255,.22) }
.ev { font-size:12px; line-height:1.65; color:var(--fg3); margin-top:9px; max-width:74ch }
.ev.div { color:var(--danger) }
.tag { font-family:var(--mono); font-size:9px; text-transform:uppercase; letter-spacing:.1em;
  color:var(--fg4); border:1px solid var(--bd2); border-radius:4px; padding:1px 5px; margin-right:6px }
.ev.div .tag { color:var(--danger); border-color:var(--danger) }
.refs { margin-top:9px; display:flex; gap:5px; flex-wrap:wrap }
.ref { font-family:var(--mono); font-size:11px; color:var(--fg4); background:var(--s1);
  border:1px solid var(--bd1); border-radius:5px; padding:2px 7px; text-decoration:none }
a.ref:hover { color:var(--fg2); border-color:#3b78d0 }
code { font-family:var(--mono); font-size:11.5px; color:var(--fg2) }
.bodynav { display:flex; justify-content:space-between; gap:12px; margin-top:26px;
  padding-top:16px; border-top:1px solid var(--bd1) }
.navlink { font-size:13px; color:var(--fg3) } .navlink:hover { color:var(--accent) }
body.collapsed .narrative, body.collapsed .ev, body.collapsed .disc, body.collapsed .refs { display:none }
@media (max-width:640px) {
  .wrap { padding:16px 13px 60px } .pills { margin-left:0 }
  /* The field ledger cannot stay a 3-column table here: a long snake_case key has no
     break opportunity, so at 390px it claimed 219px and left the value column 54px —
     one word per line, cells 1000px tall. Stack it instead: label on top, value full
     width underneath. */
  table.spec:not(.moons), .spec:not(.moons) tbody, .spec:not(.moons) tr,
  .spec:not(.moons) td { display:block; width:auto }
  .spec:not(.moons) thead { display:none }
  .spec:not(.moons) tr { padding:7px 0; border-bottom:1px solid var(--bd1) }
  .spec:not(.moons) tr:last-child { border-bottom:none }
  .spec:not(.moons) td { padding:0; border-bottom:none }
  .spec:not(.moons) td.k { white-space:normal; overflow-wrap:anywhere; padding:0 0 3px;
    font:500 11px/1.35 var(--sans); letter-spacing:.06em; text-transform:uppercase;
    color:var(--fg4) }
  .spec:not(.moons) tr.d td.k { color:var(--danger) }
  .spec:not(.moons) td.v { font-size:13px }
  .spec:not(.moons) td.o { text-align:left; margin-top:5px }
  .spec:not(.moons) td.o:empty { display:none }
  /* the moon ledger is a genuine matrix — let it exceed the viewport and scroll.
     Its per-moon prose must not scroll with it: pin those notes to the table's left
     edge and wrap them at viewport width, or they are unreadable without panning. */
  .spec.moons { width:auto; min-width:100% }
  .spec.moons tr.mnote td:first-child { display:none }
  .spec.moons tr.mnote .fnote { width:calc(100vw - 76px) }
}
"""


def render_hub():
    """Top-level docs/phase4/ landing page across every v2 board.

    The wiki's Viewers Gallery links `…/phase4/`, which 404s without an index
    here (found 2026-08-03). check_site_links.py only walks links inside docs/,
    so an inbound wiki link cannot be gated — this page is what keeps it alive.
    """
    boards = []
    for src in sorted((REPO / "phase4").glob("*.yaml")):
        try:
            b = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if str(b.get("schema_version", "")).strip() not in {"2", "2.0"}:
            continue
        system = b.get("system") or src.stem
        rows = b.get("decisions") or []
        if not rows:
            continue
        slug = to_url_slug(src.stem)
        if not (REPO / "docs" / "phase4" / slug / "index.html").exists():
            continue
        bodies = []
        for d in rows:
            if d.get("body") not in bodies:
                bodies.append(d.get("body"))
        ndiv = sum(1 for d in rows
                   if (d.get("gate") or {}).get("verdict") == "documented-divergence")
        boards.append((system, slug, len(bodies), len(rows), ndiv))

    cards = []
    for system, slug, nb, nr, ndiv in boards:
        badges = [f'<span class="mini-pill g">{nb} bodies</span>']
        if ndiv:
            badges.append(f'<span class="mini-pill d">{ndiv} div</span>')
        cards.append(f"""<a class="body-card" href="{slug}/index.html">
  <div class="bc-head"><span class="bc-name">{esc(system)}</span></div>
  <div class="bc-count">{nr} <span data-i18n>결정</span><span data-en hidden>decisions</span></div>
  <div class="bc-badges">{"".join(badges)}</div>
</a>""")
    content = f"""<nav class="crumb">
  <a href="../wiki/reference__methodology-index.html"><span data-i18n>방법론</span><span data-en hidden>Methodology</span></a>
</nav>
<header>
  <h1><span data-i18n>Phase 4 결정 보드</span><span data-en hidden>Phase 4 decision boards</span></h1>
  <div class="spacer"></div>
  {LANG_SEG}
</header>
<p class="intro"><span data-i18n>각 항성계의 art-direction을 고증 게이트로 검증해 emit용으로 확정한 값입니다. 계를 골라 천체별 결정을 봅니다.</span><span data-en hidden>Per-system art-direction validated against the 고증 gate and frozen for emit. Pick a system to see its bodies' decisions.</span></p>
<div class="summary">
  <span><b>{len(boards)}</b> <span data-i18n>항성계</span><span data-en hidden>systems</span></span>
  <span><b>{sum(x[3] for x in boards)}</b> <span data-i18n>결정</span><span data-en hidden>decisions</span></span>
  <span><b>{sum(x[4] for x in boards)}</b> documented-divergence</span>
</div>
<div class="body-grid">{"".join(cards)}</div>
<p class="intro"><a href="orbit-viewers/index.html"><span data-i18n>궤도 뷰어 갤러리 →</span><span data-en hidden>Orbit viewer gallery →</span></a></p>"""
    return page("Phase 4 — NearStars decision boards", content, depth=1)


def main():
    if len(sys.argv) < 2:
        print("usage: build_phase4_html.py <system>", file=sys.stderr)
        return 2
    system = sys.argv[1]
    src = REPO / "phase4" / f"{system}.yaml"
    board = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
    # same normalization as check_phase4_gate.is_v2 — a quoted "2" must not skip the board
    if str(board.get("schema_version", "")).strip() not in {"2", "2.0"}:
        print(f"[skip] {src.name} is not schema_version:2 — normalize it first.", file=sys.stderr)
        return 1

    decisions = board.get("decisions") or []
    bodies, order, aliases = {}, [], {}
    for d in decisions:
        b = d.get("body", "?")
        if b not in bodies:
            bodies[b] = []
            order.append(b)
        bodies[b].append(d)
        if d.get("kopernicus_name"):
            aliases.setdefault(b, d["kopernicus_name"])

    out_dir = REPO / "docs" / "phase4" / to_url_slug(system)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "index.html").write_text(
        render_index(system, order, bodies, aliases), encoding="utf-8")

    for i, b in enumerate(order):
        prev_link = (body_slug(order[i - 1]) + ".html", order[i - 1]) if i > 0 else None
        next_link = (body_slug(order[i + 1]) + ".html", order[i + 1]) if i < len(order) - 1 else None
        (out_dir / f"{body_slug(b)}.html").write_text(
            render_body(system, b, bodies[b], aliases.get(b), prev_link, next_link),
            encoding="utf-8")

    hub = REPO / "docs" / "phase4" / "index.html"
    hub.write_text(render_hub(), encoding="utf-8")

    rel = out_dir.relative_to(REPO)
    print(f"[ok] wrote {rel}/index.html + {len(order)} body pages ({len(decisions)} decisions)")
    print(f"[ok] wrote {hub.relative_to(REPO)} (hub across all v2 boards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
