# chain.yaml 에서 인터랙티브 그래프 탐색 페이지를 생성 (노드 전체 + 마우스오버 연결 표시)
"""Generate `engine/chain-explorer.html` from `engine/chain.yaml`.

The explanatory page (`dependency-chain.html`) is prose about the graph; this
one *is* the graph — every node, every edge, hover to see what a value connects
to. It is generated rather than hand-drawn for the same reason the dynamo table
is: a hand-drawn copy drifts from the source the first time the source changes.

    python3 engine/build_graph_page.py

Node ids in chain.yaml are English because they are contract keys. The Korean
display labels live here, not there — chain.yaml carries the physics contract,
the builder carries presentation.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CHAIN = HERE / "chain.yaml"
OUT = HERE / "chain-explorer.html"

LABELS = {
    "star_physical": "별의 성질", "star_metallicity": "별 금속함량",
    "system_age": "계 나이", "body_age": "천체 나이",
    "orbit_elements": "궤도 요소", "mass_or_radius": "질량 또는 반지름",
    "composition_intent": "조성 의도", "ocean_fraction": "바다 비율",
    "ocean_depth": "바다 깊이", "resonance_architecture": "공명 구조",
    "ring_system": "고리",
    "body_class": "천체 분류", "mass_radius_relation": "질량–반지름 관계",
    "interior_structure": "내부 구조", "xuv_history": "XUV 이력",
    "internal_heat_nontidal": "내부 열",
    "nmoi_class_table": "관성모멘트 표", "k2q_class_table": "조석 소산 표",
    "omega0_class_table": "초기 자전 표", "t_exo_bracket": "외기권 온도 구간",
    "tidal_locking": "조석 고정", "body_figure": "편평도 J₂·C₂₂",
    "cassini_state": "자전축 기울기", "spin_axis_inclination": "자전축 방향",
    "dynamo_giant": "자기장 (거대행성)", "dynamo_rocky": "자기장 (암석)",
    "stellar_wind": "항성풍", "magnetosphere_geometry": "자기권 · 방사선대",
    "tidal_heating": "조석 가열", "heat_transport_mode": "열 수송 방식",
    "global_fluid_layer": "전 지구 유체층",
    "t_eq_stellar": "평형 온도", "moon_energy_budget": "위성 에너지수지",
    "t_eff_body": "유효 온도", "atmospheric_escape": "대기 탈출",
    "atmosphere_choice": "대기 조성·기압", "greenhouse": "온실 효과",
    "ice_stability": "얼음 안정성", "surface_albedo": "표면색 · 알베도",
    "crater_state": "크레이터", "surface_dose": "표면 방사선량",
    "surface_uv": "지표 UV", "atmosphere_reflected_color": "대기 반사색",
    "hapke_shader_values": "표면 광학값",
}

KIND_KO = {"requires": "값을 넘긴다", "selects": "방식을 고른다",
           "influences": "영향을 준다", "excludes": "아니라고 밝혀졌다"}
NODEKIND_KO = {"measured": "측정", "owner": "결정", "computed": "계산",
               "class_table": "분류표 조회"}


# 단은 손으로 정한다. 최장경로로 계산하면 선언된 순환 여섯 개가 경로 길이를
# 부풀려 대부분의 노드를 뒤쪽으로 밀어낸다 (실측: 12단까지 늘어졌다). 순환을
# SCC 로 접으면 이번엔 그래프 절반이 한 칸에 뭉친다. 단은 계산 결과가 아니라
# 문서가 이미 갖고 있는 의미적 구분이므로, 그대로 옮겨 적는 편이 정직하다.
LAYER = {
    0: ["star_physical", "star_metallicity", "system_age", "body_age",
        "orbit_elements", "mass_or_radius", "composition_intent",
        "ocean_fraction", "ocean_depth", "resonance_architecture", "ring_system"],
    1: ["body_class", "mass_radius_relation"],
    2: ["interior_structure", "nmoi_class_table", "k2q_class_table",
        "omega0_class_table", "t_exo_bracket", "xuv_history",
        "internal_heat_nontidal", "stellar_wind"],
    3: ["tidal_locking", "body_figure", "cassini_state", "spin_axis_inclination",
        "dynamo_giant", "dynamo_rocky", "magnetosphere_geometry",
        "tidal_heating", "heat_transport_mode", "global_fluid_layer"],
    4: ["t_eq_stellar", "moon_energy_budget", "t_eff_body",
        "atmospheric_escape", "atmosphere_choice", "greenhouse"],
    5: ["ice_stability", "surface_albedo", "crater_state", "surface_dose",
        "surface_uv", "atmosphere_reflected_color", "hapke_shader_values"],
}
LAYER_KO = {0: "먼저 정해지는 것", 1: "어떤 천체인가", 2: "속은 어떤가",
            3: "거기서 나오는 것", 4: "온도 · 대기", 5: "겉모습"}


def levels(nodes: dict, edges: list) -> dict[str, int]:
    lv = {n: l for l, members in LAYER.items() for n in members}
    missing = set(nodes) - set(lv)
    extra = set(lv) - set(nodes)
    if missing or extra:
        raise SystemExit(
            f"LAYER 가 chain.yaml 과 어긋난다 — 빠짐: {sorted(missing)} · 없는 노드: {sorted(extra)}")
    return lv


def build() -> None:
    g = yaml.safe_load(CHAIN.read_text(encoding="utf-8"))
    nodes, edges = g["nodes"], g["edges"]
    lv = levels(nodes, edges)

    cols: dict[int, list[str]] = {}
    for n in nodes:
        cols.setdefault(lv[n], []).append(n)
    for c in cols.values():
        c.sort(key=lambda n: LABELS.get(n, n))

    NW, NH, GX, GY = 154, 34, 210, 46
    PAD_X, PAD_Y = 26, 40
    width = PAD_X * 2 + (max(cols) + 1) * GX
    height = PAD_Y * 2 + max(len(c) for c in cols.values()) * GY

    pos = {}
    for level, members in cols.items():
        span = len(members) * GY
        y0 = PAD_Y + (height - PAD_Y * 2 - span) / 2
        for i, n in enumerate(members):
            pos[n] = (PAD_X + level * GX, y0 + i * GY)

    payload = {
        "nodes": {
            n: {
                "label": LABELS.get(n, n),
                "kind": nd.get("kind", "computed"),
                "kindKo": NODEKIND_KO.get(nd.get("kind", "computed"), ""),
                "status": nd.get("status", ""),
                "note": (nd.get("note") or "").strip(),
                "recipe": nd.get("recipe", ""),
                "outputs": nd.get("outputs", []),
                "x": pos[n][0], "y": pos[n][1],
            } for n, nd in nodes.items()
        },
        "edges": [
            {
                "f": e["from"], "t": e["to"], "k": e["kind"],
                "via": (", ".join(e["via"]) if isinstance(e.get("via"), list)
                        else (e.get("via") or "")),
                "scope": e.get("scope", "self"),
                "sign": e.get("sign", ""),
                "status": e.get("status", ""),
                "note": (e.get("note") or "").strip(),
            } for e in edges if e["from"] in nodes and e["to"] in nodes
        ],
        "kindKo": KIND_KO,
        "layers": [{"x": PAD_X + l * GX, "name": LAYER_KO[l]} for l in sorted(LAYER)],
        "w": width, "h": height,
    }

    counts = {k: sum(1 for e in edges if e["kind"] == k) for k in KIND_KO}
    OUT.write_text(TEMPLATE
                   .replace("__DATA__", json.dumps(payload, ensure_ascii=False))
                   .replace("__NN__", str(len(nodes)))
                   .replace("__NE__", str(len(payload["edges"])))
                   .replace("__CR__", str(counts["requires"]))
                   .replace("__CS__", str(counts["selects"]))
                   .replace("__CI__", str(counts["influences"]))
                   .replace("__CX__", str(counts["excludes"])),
                   encoding="utf-8")
    print(f"chain-explorer: {len(nodes)} nodes, {len(payload['edges'])} edges "
          f"→ {OUT.relative_to(HERE.parent)}  ({width}×{height})")


TEMPLATE = r"""<title>의존 사슬 탐색기</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&display=swap">
<style>
:root{
  --paper:#E7EBEF; --surface:#FBFCFD; --surface-2:#F1F4F7;
  --ink:#16202B; --ink-2:#48586A; --ink-3:#7B8B9B; --rule:#C7D0D9;
  --requires:#5A6B7D; --selects:#6A3FA0; --influences:#1F6E7C; --excludes:#A81F48;
  --missing:#A81F48; --missing-bg:#F7DFE6; --partial:#9A6605; --partial-bg:#F6ECD8;
  --font-sans:"IBM Plex Sans KR",-apple-system,BlinkMacSystemFont,sans-serif;
  --font-mono:"IBM Plex Mono","IBM Plex Sans KR",ui-monospace,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#10161D; --surface:#19212B; --surface-2:#1F2833;
  --ink:#DCE4EC; --ink-2:#A3B2C0; --ink-3:#6F7F8F; --rule:#2C3946;
  --requires:#93A3B4; --selects:#C4A0F0; --influences:#5FC0CF; --excludes:#FF7A9C;
  --missing:#FF7A9C; --missing-bg:#37202A; --partial:#E3AE4A; --partial-bg:#31281A;
}}
:root[data-theme="dark"]{
  --paper:#10161D; --surface:#19212B; --surface-2:#1F2833;
  --ink:#DCE4EC; --ink-2:#A3B2C0; --ink-3:#6F7F8F; --rule:#2C3946;
  --requires:#93A3B4; --selects:#C4A0F0; --influences:#5FC0CF; --excludes:#FF7A9C;
  --missing:#FF7A9C; --missing-bg:#37202A; --partial:#E3AE4A; --partial-bg:#31281A;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font-sans);line-height:1.7}
.top{max-width:1700px;margin:0 auto;padding:34px 24px 0}
h1{font-size:26px;font-weight:700;margin:0;letter-spacing:-.02em}
.sub{color:var(--ink-2);font-weight:300;margin:8px 0 0;font-size:15px}
.bar{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 14px;align-items:center}
.tg{font-family:var(--font-mono);font-size:11.5px;letter-spacing:.03em;border:1px solid var(--rule);
    background:var(--surface);color:var(--ink-2);border-radius:999px;padding:6px 14px;cursor:pointer;
    display:inline-flex;align-items:center;gap:7px;user-select:none}
.tg:hover{border-color:var(--ink-3)}
.tg .dot{width:16px;height:0;border-top:2px solid var(--c)}
.tg[data-on="0"]{opacity:.36}
.tg.requires{--c:var(--requires)} .tg.selects{--c:var(--selects)}
.tg.influences{--c:var(--influences)} .tg.excludes{--c:var(--excludes)}
.tg.selects .dot,.tg.excludes .dot{border-top-style:dashed}
.hint{font-size:12.5px;color:var(--ink-3);margin-left:auto}
.stage{max-width:1700px;margin:0 auto;padding:0 24px 60px;display:grid;
       grid-template-columns:minmax(0,1fr) 310px;gap:20px;align-items:start}
@media(max-width:1080px){.stage{grid-template-columns:1fr}}
.canvas{background:var(--surface);border:1px solid var(--rule);border-radius:12px;overflow-x:auto}
svg{display:block}
.panel{background:var(--surface);border:1px solid var(--rule);border-radius:12px;padding:20px;
       position:sticky;top:20px;min-height:340px;font-size:14px}
.panel .ph{color:var(--ink-3);font-weight:300;font-size:14px}
.panel h2{margin:0;font-size:19px;font-weight:600;letter-spacing:-.01em}
.panel .id{font-family:var(--font-mono);font-size:10.5px;color:var(--ink-3);margin-top:3px;word-break:break-all}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.tag{font-family:var(--font-mono);font-size:10.5px;border:1px solid var(--rule);border-radius:5px;
     padding:3px 8px;color:var(--ink-2)}
.tag.miss{border-color:var(--missing);color:var(--missing);background:var(--missing-bg)}
.tag.tbl{border-color:var(--partial);color:var(--partial);background:var(--partial-bg)}
.panel .note{font-size:13.5px;color:var(--ink-2);font-weight:300;margin:10px 0 0;
             border-left:2px solid var(--rule);padding-left:12px}
.grp{margin-top:18px}
.grp h3{margin:0 0 7px;font-family:var(--font-mono);font-size:10.5px;letter-spacing:.1em;
        text-transform:uppercase;color:var(--ink-3);font-weight:500}
.grp ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:5px}
.grp li{font-size:13px;display:flex;gap:8px;align-items:baseline;cursor:pointer;line-height:1.5}
.grp li:hover{color:var(--selects)}
.grp li i{width:9px;height:9px;border-radius:2px;background:var(--c);flex:0 0 auto;
          position:relative;top:1px}
.grp li em{font-style:normal;font-family:var(--font-mono);font-size:10.5px;color:var(--ink-3)}
.node{cursor:pointer}
.node rect{fill:var(--surface-2);stroke:var(--ink-3);stroke-width:1.2}
.node.miss rect{fill:var(--missing-bg);stroke:var(--missing);stroke-width:2}
.node.tbl rect{fill:var(--partial-bg);stroke:var(--partial);stroke-width:1.8}
.node text{font-size:11.5px;font-weight:500;fill:var(--ink);pointer-events:none}
.node.dim{opacity:.16}
.node.hot rect{stroke-width:2.6;stroke:var(--selects)}
.ed{fill:none;stroke-width:1.1;opacity:.13}
.ed.requires{stroke:var(--requires)} .ed.selects{stroke:var(--selects);stroke-dasharray:5 3}
.ed.influences{stroke:var(--influences)} .ed.excludes{stroke:var(--excludes);stroke-dasharray:3 3}
.ed.hot{opacity:1;stroke-width:2}
.ed.off{display:none}
.lvl{font-family:var(--font-mono);font-size:10px;fill:var(--ink-3);letter-spacing:.08em}
</style>

<div class="top">
  <h1>의존 사슬 탐색기</h1>
  <p class="sub">노드 __NN__개, 연결 __NE__개 전부. 값 하나에 올려두면 그 값이 무엇에 기대고 무엇을 흔드는지 보인다. 눌러서 고정.</p>
  <div class="bar">
    <span class="tg requires" data-k="requires" data-on="1"><span class="dot"></span>값을 넘긴다 __CR__</span>
    <span class="tg selects" data-k="selects" data-on="1"><span class="dot"></span>방식을 고른다 __CS__</span>
    <span class="tg influences" data-k="influences" data-on="1"><span class="dot"></span>영향을 준다 __CI__</span>
    <span class="tg excludes" data-k="excludes" data-on="0"><span class="dot"></span>아니라고 밝혀졌다 __CX__</span>
    <span class="hint">왼쪽이 먼저 정해지는 값이다</span>
  </div>
</div>

<div class="stage">
  <div class="canvas"><svg id="g" role="img" aria-label="의존 그래프 전체. 노드에 올리면 연결이 강조된다."></svg></div>
  <aside class="panel" id="p"><p class="ph">노드에 마우스를 올리면 여기에 설명과 연결이 표시된다.</p></aside>
</div>

<script>
const D = __DATA__;
const NW = 154, NH = 34;
const svg = document.getElementById('g'), panel = document.getElementById('p');
svg.setAttribute('viewBox', `0 0 ${D.w} ${D.h}`);
svg.setAttribute('width', D.w); svg.setAttribute('height', D.h);

const ns = 'http://www.w3.org/2000/svg';
const mk = (t, a) => { const e = document.createElementNS(ns, t);
  for (const k in a) e.setAttribute(k, a[k]); return e; };

const gE = mk('g', {}), gN = mk('g', {});
svg.appendChild(gE); svg.appendChild(gN);

const path = (a, b) => {
  const x1 = a.x + NW, y1 = a.y + NH / 2, x2 = b.x, y2 = b.y + NH / 2;
  if (x2 >= x1) { const m = (x1 + x2) / 2;
    return `M${x1} ${y1} C${m} ${y1} ${m} ${y2} ${x2} ${y2}`; }
  const lift = Math.max(46, Math.abs(y2 - y1) * .6 + 30);
  return `M${x1} ${y1} C${x1 + lift} ${y1 - lift} ${x2 - lift} ${y2 - lift} ${x2} ${y2}`;
};

const eEls = [];
D.edges.forEach((e, i) => {
  const a = D.nodes[e.f], b = D.nodes[e.t];
  const p = mk('path', { d: path(a, b), class: `ed ${e.k}` });
  p.dataset.f = e.f; p.dataset.t = e.t; p.dataset.k = e.k; p.dataset.i = i;
  gE.appendChild(p); eEls.push(p);
});

const nEls = {};
for (const id in D.nodes) {
  const n = D.nodes[id];
  const cls = n.status === 'missing' || n.status === 'gap' ? 'miss'
            : n.kind === 'class_table' ? 'tbl' : '';
  const g = mk('g', { class: `node ${cls}`, tabindex: '0', role: 'button' });
  g.appendChild(mk('rect', { x: n.x, y: n.y, width: NW, height: NH, rx: 6 }));
  const t = mk('text', { x: n.x + NW / 2, y: n.y + NH / 2 + 4.5, 'text-anchor': 'middle' });
  t.textContent = n.label; g.appendChild(t);
  g.addEventListener('mouseenter', () => show(id));
  g.addEventListener('focus', () => show(id));
  g.addEventListener('click', () => { pinned = pinned === id ? null : id; show(id); });
  gN.appendChild(g); nEls[id] = g;
}

const off = new Set(['excludes']);
let pinned = null;

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function list(items, dir) {
  if (!items.length) return '';
  const li = items.map(e => {
    const other = dir === 'in' ? e.f : e.t;
    const bits = [D.kindKo[e.k]];
    if (e.via) bits.push(e.via);
    if (e.scope !== 'self') bits.push('부모');
    if (e.sign === 'non-monotonic') bits.push('비단조');
    if (e.status) bits.push('공백');
    return `<li data-go="${esc(other)}"><i style="--c:var(--${e.k})"></i>
      <span>${esc(D.nodes[other].label)}<br><em>${esc(bits.join(' · '))}</em></span></li>`;
  }).join('');
  return `<div class="grp"><h3>${dir === 'in' ? '이것이 기대는 값' : '이 값이 흔드는 것'} ${items.length}</h3><ul>${li}</ul></div>`;
}

function show(id) {
  const n = D.nodes[id];
  const inc = D.edges.filter(e => e.t === id && !off.has(e.k));
  const out = D.edges.filter(e => e.f === id && !off.has(e.k));
  const near = new Set([id, ...inc.map(e => e.f), ...out.map(e => e.t)]);

  for (const k in nEls) nEls[k].classList.toggle('dim', !near.has(k));
  nEls[id].classList.add('hot');
  for (const k in nEls) if (k !== id) nEls[k].classList.remove('hot');
  eEls.forEach(p => p.classList.toggle('hot',
    !off.has(p.dataset.k) && (p.dataset.f === id || p.dataset.t === id)));

  const tags = [`<span class="tag">${esc(n.kindKo)}</span>`];
  if (n.status) tags.push(`<span class="tag miss">${n.status === 'missing' ? '없음' : '공백'}</span>`);
  if (n.kind === 'class_table') tags.push('<span class="tag tbl">계산값 아님</span>');
  if (n.recipe) tags.push(`<span class="tag">${esc(n.recipe)}</span>`);

  panel.innerHTML = `<h2>${esc(n.label)}</h2><div class="id">${esc(id)}</div>
    <div class="tags">${tags.join('')}</div>
    ${n.note ? `<p class="note">${esc(n.note)}</p>` : ''}
    ${n.outputs.length ? `<div class="grp"><h3>내놓는 값</h3><ul><li><span><em>${esc(n.outputs.join(' · '))}</em></span></li></ul></div>` : ''}
    ${list(inc, 'in')}${list(out, 'out')}`;

  panel.querySelectorAll('[data-go]').forEach(li =>
    li.addEventListener('click', ev => { ev.stopPropagation(); pinned = li.dataset.go; show(pinned); }));
}

function clear() {
  if (pinned) return;
  for (const k in nEls) { nEls[k].classList.remove('dim'); nEls[k].classList.remove('hot'); }
  eEls.forEach(p => p.classList.remove('hot'));
  panel.innerHTML = '<p class="ph">노드에 마우스를 올리면 여기에 설명과 연결이 표시된다.</p>';
}
svg.addEventListener('mouseleave', clear);

function apply() {
  eEls.forEach(p => p.classList.toggle('off', off.has(p.dataset.k)));
  if (pinned) show(pinned);
}
document.querySelectorAll('.tg').forEach(t => {
  if (t.dataset.on === '0') off.add(t.dataset.k);
  t.addEventListener('click', () => {
    const k = t.dataset.k, on = t.dataset.on === '1';
    t.dataset.on = on ? '0' : '1';
    if (on) off.add(k); else off.delete(k);
    apply();
  });
});
apply();

// 단 라벨
D.layers.forEach(l => {
  const t = mk('text', { x: l.x, y: 18, class: 'lvl' });
  t.textContent = l.name;
  svg.appendChild(t);
});
</script>
"""

if __name__ == "__main__":
    build()
