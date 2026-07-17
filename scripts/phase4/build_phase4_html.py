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
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from pipeline._naming import to_url_slug  # noqa: E402

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}")


def body_slug(b):
    # 와일드카드 바디("*", 행성 공통 행)는 to_url_slug가 빈 문자열을 내므로 고정 슬러그 사용
    return "system-wide" if b.strip("* ") == "" else to_url_slug(b)

STATUS_LABEL = {
    "gated": ("확정", "Gated"), "passthrough": ("통과", "Passthrough"),
    "open": ("미결", "Open"), "art-directed": ("연출", "Art-directed"),
    "emitted": ("반영", "Emitted"), "superseded": ("대체됨", "Superseded"),
}
VERDICT_LABEL = {
    "pass-in-window": ("범위 내", "In-window"),
    "documented-divergence": ("문서화 이탈", "Doc. divergence"),
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
        warn = ' <span class="mini" title="documented divergence">⚠</span>' if div else ""
        val = value_html(f.get("value"))
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
        if f.get("note"):
            val += f'<div class="fnote">{esc(f["note"])}</div>'
        if f.get("phase3_default"):
            val += f'<div class="fnote p3">Phase 3: {esc(f["phase3_default"])}</div>'
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
                        f'<div class="fnote">{esc(m["note"])}</div></td></tr>')
    return ('<div class="moonwrap"><table class="spec moons"><thead><tr>' + head
            + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")


def refs_html(refs):
    if not refs:
        return ""
    if isinstance(refs, str):  # defensive — the validator rejects this, but never render per-char
        refs = [refs]
    return '<div class="refs">' + "".join(
        f'<span class="ref">{esc(r)}</span>' for r in refs) + "</div>"


def decision_html(d):
    status = d.get("status", "")
    gate = d.get("gate") or {}
    verdict = gate.get("verdict", "")
    div = verdict == "documented-divergence"

    sk, se = STATUS_LABEL.get(status, (status, status))
    pills = (f'<span class="pill st-{esc(status)}">'
             f'<span data-i18n>{esc(sk)}</span><span data-en hidden>{esc(se)}</span></span>')
    if verdict:
        vk, ve = VERDICT_LABEL.get(verdict, (verdict, verdict))
        pills += (f'<span class="pill {"vd-div" if div else "vd-ok"}">'
                  f'<span data-i18n>{esc(vk)}</span><span data-en hidden>{esc(ve)}</span></span>')

    narrative = bi(d.get("narrative"), d.get("narrative_ko"))
    nar = f'<p class="narrative">{narrative}</p>' if narrative else ""

    disc = d.get("discoverability_cfg")
    disc_html = ""
    if disc:
        disc_html = (f'<div class="disc"><span class="tag">discoverability</span> '
                     f'<code>{esc(disc.get("category",""))}</code> · IGNORELEVELS '
                     f'<code>{esc(disc.get("ignorelevels",""))}</code></div>')

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
  {fields_table(d.get('fields'))}
  {moons_table(d.get('moons'))}
  {disc_html}{dep_html}{ev_html}{dn_html}
  {refs_html(d.get('refs'))}
</article>"""


def body_stats(rows):
    ng = sum(1 for d in rows if d.get("status") in ("gated", "emitted"))
    npt = sum(1 for d in rows if d.get("status") == "passthrough")
    nd = sum(1 for d in rows if (d.get("gate") or {}).get("verdict") == "documented-divergence")
    nopen = sum(1 for d in rows if d.get("status") in ("open", "art-directed"))
    return {"total": len(rows), "gated": ng, "passthrough": npt, "divergence": nd, "open": nopen}


def render_body(system, body, rows, alias, prev_link, next_link):
    st = body_stats(rows)
    meta = (f'{st["total"]} <span data-i18n>결정</span><span data-en hidden>decisions</span> · '
            f'{st["gated"]} gated · {st["divergence"]} divergence'
            + (f' · {st["open"]} open' if st["open"] else ""))
    decs = "\n".join(decision_html(d) for d in rows)
    nav = []
    if prev_link:
        nav.append(f'<a class="navlink" href="{prev_link[0]}">← {esc(prev_link[1])}</a>')
    if next_link:
        nav.append(f'<a class="navlink" href="{next_link[0]}">{esc(next_link[1])} →</a>')
    nav_html = f'<div class="bodynav">{"".join(nav)}</div>' if nav else ""
    alias_html = f' <span class="alias">{esc(alias)}</span>' if alias else ""

    content = f"""<nav class="crumb">
  <a href="index.html"><span data-i18n>Phase 4</span></a> ·
  <a href="index.html"><span class="sys">{esc(system)}</span></a> ·
  <span class="here">{esc(body)}</span>
</nav>
<header>
  <h1>{esc(body)}{alias_html}</h1>
  <div class="spacer"></div>
  {LANG_SEG}
  <div class="seg"><button id="collapse"><span data-i18n>설명 접기</span><span data-en hidden>Collapse</span></button></div>
</header>
<div class="summary"><span class="body-meta">{meta}</span></div>
<div class="decisions">{decs}</div>
{nav_html}"""
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
  <a href="../../index.html"><span data-i18n>NearStars</span></a> ·
  <span class="here"><span data-i18n>Phase 4</span> · <span class="sys">{esc(system)}</span></span>
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


LANG_SEG = ('<div class="seg"><button id="ko" class="on">한국어</button>'
            '<button id="en">EN</button></div>')

SCRIPT = """<script>
const b=document.body;
function setLang(en){
  document.querySelectorAll('[data-i18n]').forEach(e=>e.hidden=en);
  document.querySelectorAll('[data-en]').forEach(e=>e.hidden=!en);
  ko_.classList.toggle('on',!en); en_.classList.toggle('on',en);
}
const ko_=document.getElementById('ko'), en_=document.getElementById('en');
ko_.onclick=()=>setLang(false); en_.onclick=()=>setLang(true);
const cb=document.getElementById('collapse');
if(cb) cb.onclick=e=>{b.classList.toggle('collapsed');
  e.currentTarget.classList.toggle('on',b.classList.contains('collapsed'));};
</script>"""


def page(title, content):
    return f"""<!DOCTYPE html>
<!-- autogenerated by scripts/phase4/build_phase4_html.py from phase4/*.yaml (schema v2). Do not hand-edit. -->
<html lang="ko" data-ns="v2">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500&family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
<div class="wrap">
{content}
</div>
{SCRIPT}
</body>
</html>"""


STYLE = """
:root {
  --bg:#06070a; --fg1:rgba(255,255,255,.94); --fg2:rgba(255,255,255,.80); --fg3:rgba(255,255,255,.56);
  --fg4:rgba(255,255,255,.36); --s1:rgba(255,255,255,.022); --s2:rgba(255,255,255,.045);
  --s3:rgba(255,255,255,.07); --bd1:rgba(255,255,255,.05); --bd2:rgba(255,255,255,.09);
  --accent:#7aa8ff; --accent-bg:rgba(122,168,255,.10);
  --ok:#4ec9b0; --ok-bg:rgba(78,201,176,.12); --warn:#e0b070; --warn-bg:rgba(224,176,112,.12);
  --danger:#e090d0; --danger-bg:rgba(224,144,208,.14);
  --sans:'Geist','Inter',system-ui,-apple-system,'Noto Sans KR',sans-serif;
  --mono:'Geist Mono','SF Mono',Menlo,monospace;
}
* { box-sizing:border-box; margin:0; padding:0 }
html,body { max-width:100vw; overflow-x:hidden }
body {
  background:
    radial-gradient(60% 50% at 18% -10%, rgba(122,168,255,.07), transparent 70%),
    radial-gradient(50% 45% at 92% 110%, rgba(224,144,208,.05), transparent 70%),
    var(--bg);
  background-attachment:fixed; color:var(--fg2);
  font-family:var(--sans); font-size:14px; line-height:1.6;
  font-feature-settings:'ss01','cv11','tnum'; -webkit-font-smoothing:antialiased;
}
a { color:var(--accent); text-decoration:none }
a:hover { color:#aac8ff }
.wrap { max-width:940px; margin:0 auto; padding:26px 22px 90px }
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
.seg { display:inline-flex; padding:2px; gap:2px; background:var(--s1); border:1px solid var(--bd2); border-radius:8px }
.seg button { background:transparent; border:none; color:var(--fg3); font:500 12px/1 var(--sans);
  padding:6px 11px; border-radius:6px; cursor:pointer; transition:.14s }
.seg button:hover { color:var(--fg2) } .seg button.on { background:var(--s3); color:var(--fg1) }
/* index grid */
.body-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:12px }
.body-card { display:block; background:var(--s1); border:1px solid var(--bd2); border-radius:12px;
  padding:14px 16px; transition:.16s; box-shadow:inset 0 1px 0 rgba(255,255,255,.05) }
.body-card:hover { background:var(--s2); border-color:rgba(122,168,255,.4); transform:translateY(-1px) }
.bc-head { display:flex; align-items:baseline; gap:8px; flex-wrap:wrap; margin-bottom:6px }
.bc-name { font-size:15px; font-weight:600; color:var(--fg1) }
.alias { color:var(--accent); font-size:12px; font-family:var(--mono) }
.bc-count { font-family:var(--mono); font-size:11px; color:var(--fg4); margin-bottom:8px }
.bc-badges { display:flex; gap:5px; flex-wrap:wrap }
.mini-pill { font:600 9.5px/1.4 var(--sans); letter-spacing:.03em; text-transform:uppercase;
  padding:2px 8px; border-radius:999px }
.mini-pill.g { color:var(--ok); background:var(--ok-bg) }
.mini-pill.d { color:var(--danger); background:var(--danger-bg) }
.mini-pill.p { color:var(--fg4); background:var(--s2) }
.mini-pill.o { color:var(--warn); background:var(--warn-bg) }
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
.pill { font:600 10px/1.4 var(--sans); letter-spacing:.03em; text-transform:uppercase;
  padding:2px 9px; border-radius:999px }
.pill.st-gated,.pill.st-emitted { color:var(--ok); background:var(--ok-bg) }
.pill.st-passthrough { color:var(--fg4); background:var(--s2) }
.pill.st-open,.pill.st-art-directed { color:var(--warn); background:var(--warn-bg) }
.pill.st-superseded { color:var(--fg4); background:var(--s2); text-decoration:line-through }
.pill.vd-ok { color:var(--ok); background:var(--ok-bg) }
.pill.vd-div { color:var(--danger); background:var(--danger-bg) }
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
.spec .win { color:var(--fg4); font-size:10.5px; border:1px solid var(--bd1); border-radius:4px;
  padding:1px 6px; margin-left:6px; white-space:nowrap }
.fnote { color:var(--fg4); font-size:10.5px; font-family:var(--sans); line-height:1.5; margin-top:3px; max-width:64ch }
.fnote.p3 { color:var(--fg4); font-style:italic }
.swatches { display:flex; gap:6px 12px; flex-wrap:wrap; margin-top:5px }
.swatches .sw { font-size:10.5px; color:var(--fg3); white-space:nowrap }
.swatches .hx { color:var(--fg4); font-size:9.5px }
.moonwrap { overflow-x:auto; margin:8px 0 2px }
.spec.moons td.v { white-space:nowrap }
.spec.moons tr.mnote td { border-bottom:1px solid var(--bd1); padding-top:0 }
.spec.moons tr.mnote + tr td { border-top:none }
.spec.moons tr td { border-bottom:none }
.spec.moons tr.mdesign td, .spec.moons td.dsn { color:var(--fg4); font-size:10.5px; padding-top:0 }
.spec.moons tr.mdesign td.k { font-family:var(--sans); font-size:10px }
.spec.moons tr:last-child td, .spec.moons tr.mnote td { border-bottom:1px solid var(--bd1) }
.op { font-family:var(--sans); font-size:9px; font-weight:600; text-transform:uppercase; color:var(--warn);
  background:var(--warn-bg); border-radius:4px; padding:1px 5px }
.mini { color:var(--danger) }
.chip { display:inline-block; width:11px; height:11px; border-radius:3px; vertical-align:-1px;
  margin-right:5px; border:1px solid rgba(255,255,255,.22) }
.ev,.disc { font-size:12px; line-height:1.65; color:var(--fg3); margin-top:9px; max-width:74ch }
.ev.div { color:var(--danger) }
.tag { font-family:var(--mono); font-size:9px; text-transform:uppercase; letter-spacing:.1em;
  color:var(--fg4); border:1px solid var(--bd2); border-radius:4px; padding:1px 5px; margin-right:6px }
.ev.div .tag { color:var(--danger); border-color:var(--danger) }
.refs { margin-top:9px; display:flex; gap:5px; flex-wrap:wrap }
.ref { font-family:var(--mono); font-size:10px; color:var(--fg4); background:var(--s1);
  border:1px solid var(--bd1); border-radius:5px; padding:2px 7px }
code { font-family:var(--mono); font-size:11.5px; color:var(--fg2) }
.bodynav { display:flex; justify-content:space-between; gap:12px; margin-top:26px;
  padding-top:16px; border-top:1px solid var(--bd1) }
.navlink { font-size:13px; color:var(--fg3) } .navlink:hover { color:var(--accent) }
body.collapsed .narrative, body.collapsed .ev, body.collapsed .disc, body.collapsed .refs { display:none }
@media (max-width:640px) {
  .wrap { padding:16px 13px 60px } .pills { margin-left:0 } .spec td.k { white-space:normal }
}
"""


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

    rel = out_dir.relative_to(REPO)
    print(f"[ok] wrote {rel}/index.html + {len(order)} body pages ({len(decisions)} decisions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
