# 안정성 런 결과를 3D 궤도 세차 애니메이션(self-contained HTML)으로 생성 — plot_moons.py의 3D 짝.
"""Generate a self-contained 3D orbit-evolution animation from a stability run.

Snapshots are far coarser than the moons' orbital periods, so the FAST orbital
motion cannot be reconstructed. What IS real and worth animating is the SECULAR
evolution of each orbit ellipse (a, e, inc, node, peri) over the run — the plane
tips/precesses, e pumps. The animation plays that back; each moon also carries a
decorative marker on an illustrative (non-physical) fast phase so the scene reads
as a live system.

De-jitter (approach B — oversample then bin-average):
  The instantaneous elements oscillate on short periods; a coarse snapshot stride
  aliases them (adjacent frames land on osc. max then min → the ring visibly
  jitters). Fix in two steps:
    (1) run.py with a DENSE --snapshots so the short-period oscillation is
        resolved rather than aliased, e.g. for the 2000 yr Polyphemus run:
          .venv/bin/python phase3/stability-sim/scripts/run.py \
            --system alpha_centauri --integrator leapfrog --dt-minutes 10 \
            --years 2000 --snapshots 8000 \
            --hypotheticals phase3/stability-sim/hypotheticals/alpha_centauri.json \
            --acen-a-au 1.6 --acen-e 0.1 --acen-incl-deg 16 \
            --j2 0.023 --j2-obliquity-deg 5 \
            --out-dir phase3/stability-sim/results/_principia2000_dense
    (2) this script bin-averages those dense snapshots down to --frames keyframes
        (below), collapsing each bin to its secular mean. Angles (node, peri) use
        a circular mean so the 359->1 deg wrap never flips the ring.
  Point this script at the dense run: --dir results/_principia2000_dense.

Reads  <dir>/<label>_summary.json  +  <dir>/<label>_timeseries.csv
Writes <dir>/<label>_orbit3d.html   (open in a browser; uses the three@0.160 CDN
                                      importmap stack, same as polyphemus-moon-viewer.html)

Usage: python3 scripts/animate_orbits.py --dir results/_principia2000_dense [--label alpha_centauri] [--frames 240]
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

RJUP_KM = 71492.0
AU_KM = 1.495978707e8

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True, type=Path)
ap.add_argument("--label", default="alpha_centauri")
ap.add_argument("--frames", type=int, default=240, help="keyframes to embed (decimated)")
ap.add_argument("--flattening", type=float, default=0.13,
                help="central-body oblateness for the render (planet-center mode only)")
ap.add_argument("--center", default=None,
                help="central body name. Default: the moon parent if the run has moons, "
                     "else the star. Pass the star name to view planets around the star.")
args = ap.parse_args()

root = Path(__file__).resolve().parent.parent
d = args.dir if args.dir.is_absolute() else (root / args.dir)
summary = json.loads((d / f"{args.label}_summary.json").read_text())

# ── resolve the central body and the set of bodies orbiting it ───────────────
# Two hierarchy levels share one code path: planet-center (moons, unit = R_p,
# oblate central + spin axis) and star-center (planets, unit = AU, star sphere).
# Both take display a = a_au · AU_KM / unit_km, so the rest is level-agnostic.
star_name = summary["star"]["name"]
moons_all = [h for h in summary.get("hypotheticals", []) if h.get("type") == "moon"]
if args.center:
    center = args.center
elif moons_all:
    center = moons_all[0]["parent"]
else:
    center = star_name

if center != star_name:
    mode, unit, central_kind = "planet", "R_p", "planet"
    bodies_meta = [m for m in moons_all if m["parent"] == center]
    j2 = summary.get("j2", {})
    unit_km = j2.get("r_eq_au", RJUP_KM / AU_KM) * AU_KM
    spin_axis, J2v, flattening = j2.get("axis"), j2.get("J2"), args.flattening
else:
    mode, unit, central_kind = "star", "AU", "star"
    bodies_meta = list(summary.get("planets", []))
    unit_km = AU_KM
    spin_axis, J2v, flattening = None, None, 0.0

names = [b["name"] for b in bodies_meta]
if not names:
    raise SystemExit(f"no bodies orbit '{center}' in {args.label} — nothing to animate")

# collect per-body snapshots: t -> elements (a in display units, e, inc/node/peri deg)
raw = defaultdict(list)  # name -> [(t, a_disp, e, inc, node, peri)]
center_first = None      # center body's own orbit (inc,node), for the reference-plane frame
with (d / f"{args.label}_timeseries.csv").open() as f:
    for r in csv.DictReader(f):
        if r["body"] in names:
            a_disp = (float(r["a_au"]) * AU_KM) / unit_km
            raw[r["body"]].append((float(r["t_yr"]), a_disp, float(r["e"]),
                                   float(r["inc_deg"]), float(r["Omega_deg"]),
                                   float(r["omega_deg"])))
        elif r["body"] == center and center_first is None:
            center_first = (float(r["inc_deg"]), float(r["Omega_deg"]))

for n in names:
    raw[n].sort()
times = [row[0] for row in raw[names[0]]]

# --- de-jitter step (2): bin-average the snapshots down to `frames` keyframes.
# With a dense run each bin holds many snapshots spanning several oscillation
# periods, so the mean is the secular value and the frame-to-frame jitter dies.
# node/peri are angles -> circular mean (sin/cos) to survive the 360 deg wrap.
nbins = min(args.frames, len(times))
groups = defaultdict(list)
for i in range(len(times)):
    groups[i * nbins // len(times)].append(i)
bins = [groups[b] for b in range(nbins)]

def _mean(vals):
    return sum(vals) / len(vals)

def _circmean_deg(vals):
    s = sum(math.sin(math.radians(v)) for v in vals)
    c = sum(math.cos(math.radians(v)) for v in vals)
    return math.degrees(math.atan2(s, c))

frame_times = [_mean([times[i] for i in b]) for b in bins]

# per body: list of [a, e, inc, node, peri], each a bin mean
body_series = {}
for n in names:
    rows = raw[n]
    series = []
    for b in bins:
        series.append([
            round(_mean([rows[i][1] for i in b]), 6),          # a  (display units)
            round(_mean([rows[i][2] for i in b]), 5),          # e
            round(_mean([rows[i][3] for i in b]), 4),          # inc  (deg, no wrap)
            round(_circmean_deg([rows[i][4] for i in b]), 4),  # node (circular)
            round(_circmean_deg([rows[i][5] for i in b]), 4),  # peri (circular)
        ])
    body_series[n] = series

# outermost orbit (display units) — the JS scales all scene furniture to this so
# one renderer fits any span (0.01 AU TRAPPIST moons → 24 AU α Cen companion).
maxa = max(s[0] * (1 + s[1]) for n in names for s in body_series[n])

# --- reference-frame up-vectors (sim frame). The viewer rotates the scene so a
# chosen up-vector points to +Y, i.e. the grid = that reference plane.
def _orbit_normal(inc_deg, node_deg):
    i, o = math.radians(inc_deg), math.radians(node_deg)
    return [math.sin(i) * math.sin(o), -math.sin(i) * math.cos(o), math.cos(i)]

def _vnorm(v):
    m = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / m for x in v]

# invariable plane: angular-momentum-weighted (m·sqrt(a(1-e²))) sum of orbit normals
mass_of = {b["name"]: b.get("mass_msun", 0.0) for b in bodies_meta}
inv = [0.0, 0.0, 0.0]
for n in names:
    _, a, e, inc, node, _ = raw[n][0]
    w = mass_of.get(n, 0.0) * math.sqrt(max(a * (1 - e * e), 1e-9))
    nrm = _orbit_normal(inc, node)
    inv = [inv[k] + nrm[k] * w for k in range(3)]
inv = _vnorm(inv) if any(inv) else [0.0, 0.0, 1.0]

# middle frame: the center's own orbital plane if it orbits something (moon mode:
# the parent planet's orbit); else the most-massive orbiting body's plane (star mode).
if center_first:
    ref_up, ref_label = _orbit_normal(*center_first), "중심체 공전면"
else:
    mb = max(names, key=lambda n: mass_of.get(n, 0.0))
    _, _, _, inc0, node0, _ = raw[mb][0]
    ref_up, ref_label = _orbit_normal(inc0, node0), f"{mb.split()[-1]} 궤도면"

frames = [
    {"name": "invariable", "label": "불변면", "up": [round(x, 5) for x in inv]},
    {"name": "reference", "label": ref_label, "up": [round(x, 5) for x in ref_up]},
    {"name": "sky", "label": "하늘면(관측)", "up": [0.0, 0.0, 1.0]},
]

# plasma-ish palette matching plot_moons.py order
PALETTE = ["#7e03a8", "#b12a90", "#e16462", "#fca636", "#f0f921", "#0d0887", "#46039f"]
colors = {n: PALETTE[i % len(PALETTE)] for i, n in enumerate(names)}

j = summary["judgment"]
integ = summary["integration"]
hill = summary.get("hill_track", {})
data = {
    "system": summary["system"],
    "center": center,
    "mode": mode,
    "unit": unit,
    "central_kind": central_kind,
    "maxa": round(maxa, 6),
    "verdict": j["overall"],
    "integrator": integ["integrator"],
    "dt_min": round(integ["dt_yr"] * 365.25 * 24 * 60, 2),
    "dE": f"{integ['energy_relative_error']:.1e}",
    "J2": J2v,
    "spin_axis": spin_axis,         # sim-frame unit vector of the J2/spin axis (planet mode)
    "frames": frames,              # reference-frame toggles (sim-frame up-vectors)
    "flattening": flattening,
    "frame_times": [round(t, 1) for t in frame_times],
    "bodies": [{"name": n, "color": colors[n],
                "hill_max": round(hill.get(n, {}).get("frac_max", 0.0), 3) if hill.get(n) else None,
                "series": body_series[n]} for n in names],
}

HTML = r"""<!-- __TITLE__ : 안정성 런 3D 궤도 세차 애니메이션 (자동 생성, animate_orbits.py). three@0.160 importmap. -->
<meta charset="utf-8"><title>__TITLE__</title>
<style>
  html,body{margin:0;height:100%;background:#06070d;color:#cdd6e6;font:13px/1.5 system-ui,sans-serif;overflow:hidden}
  #hud{position:fixed;top:10px;left:12px;z-index:10;background:rgba(10,13,22,.72);padding:10px 13px;border-radius:9px;backdrop-filter:blur(4px);max-width:290px}
  #hud h1{font-size:14px;margin:0 0 4px}
  #hud .v{color:#8fe3a0;font-weight:600}
  #hud .sub{color:#8a94a8;font-size:11px}
  #leg{margin-top:8px;border-top:1px solid #263049;padding-top:7px}
  #leg .row{display:flex;justify-content:space-between;gap:10px;font-variant-numeric:tabular-nums}
  #leg .nm{display:flex;align-items:center;gap:6px}
  #leg .sw{width:10px;height:10px;border-radius:50%}
  #ctl{position:fixed;bottom:12px;left:12px;right:12px;z-index:10;display:flex;align-items:center;gap:12px;background:rgba(10,13,22,.72);padding:9px 13px;border-radius:9px;backdrop-filter:blur(4px)}
  #ctl button{background:#1c2740;color:#cdd6e6;border:1px solid #2c3a5a;border-radius:6px;padding:5px 12px;cursor:pointer;font-size:13px}
  #ctl button:hover{background:#26355a}
  #ctl input[type=range]{flex:1}
  #yr{font-variant-numeric:tabular-nums;color:#8fe3a0;font-weight:600;min-width:90px}
  .note{color:#8a94a8;font-size:11px;max-width:200px}
  #frames{margin-top:7px;display:flex;gap:5px;flex-wrap:wrap;align-items:center}
  #frames .lab{color:#8a94a8;font-size:11px;margin-right:2px}
  #frames button{background:#141c30;color:#aeb8cc;border:1px solid #2c3a5a;border-radius:6px;padding:3px 8px;cursor:pointer;font-size:11px}
  #frames button.on{background:#2b60b0;color:#fff;border-color:#3b78d0}
</style>
<div id="hud">
  <h1>__SYSTEM__ — <span class="v">__VERDICT__</span></h1>
  <div class="sub">center __CENTER__ · 단위 __UNIT__ · __INTEG__ dt=__DT__min · |ΔE/E|=__DE__</div>
  <div id="frames"><span class="lab">기준면</span></div>
  <div id="leg"></div>
</div>
<div id="ctl">
  <button id="play">⏸ 일시정지</button>
  <span id="yr"></span>
  <input id="scrub" type="range" min="0" max="1000" value="0">
  <span class="note">궤도면·이심률 진화 = 실측. 천체 마커의 공전 위상 = 예시(빠른 궤도는 스냅샷으로 복원 불가).</span>
</div>
<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const DATA = __DATA__;
const DEG = Math.PI/180;

// perifocal → inertial (3-1-3: Ω, i, ω), Three.Y = reference-plane normal
function orbitVec(a,e,inc,node,peri,f){
  const p=a*(1-e*e), r=p/(1+e*Math.cos(f));
  const xo=r*Math.cos(f), yo=r*Math.sin(f);
  const cO=Math.cos(node),sO=Math.sin(node),ci=Math.cos(inc),si=Math.sin(inc),cw=Math.cos(peri),sw=Math.sin(peri);
  const x = xo*(cO*cw - sO*sw*ci) - yo*(cO*sw + sO*cw*ci);
  const y = xo*(sO*cw + cO*sw*ci) - yo*(sO*sw - cO*cw*ci);
  const z = xo*(sw*si) + yo*(cw*si);
  return new THREE.Vector3(x, z, y);
}

// Render at a FIXED scene size regardless of the physical span: scale every
// orbit radius by SC so the outermost orbit sits at ~VIEW units. This keeps one
// comfortable camera/furniture scale for both R_p moon systems (maxa ~21) and
// tiny AU planet systems (maxa ~0.06) — drawing at native units would put a
// 0.06-unit scene at the edge of float/near-plane precision and render blank.
const VIEW=20, SC=VIEW/DATA.maxa;

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(devicePixelRatio); renderer.setSize(innerWidth,innerHeight);
document.body.appendChild(renderer.domElement);
const scene=new THREE.Scene(); scene.background=new THREE.Color('#06070d');
const camera=new THREE.PerspectiveCamera(52, innerWidth/innerHeight, 0.05, 1e5);
camera.position.set(26, 19, 32);
const controls=new OrbitControls(camera, renderer.domElement); controls.enableDamping=true;
scene.add(new THREE.AmbientLight(0xffffff,0.5));
const dir=new THREE.DirectionalLight(0xfff4e0,1.4); dir.position.set(5,3,4); scene.add(dir);

// content group holds everything drawn in the sim frame (central body, orbits,
// markers). Switching reference frame = one quaternion on this group so the
// chosen plane normal points to +Y; the grid stays at +Y and thus always
// depicts the selected reference plane.
const content=new THREE.Group(); scene.add(content);
// sim (x,y,z) -> Three (x,z,y), same mapping as orbitVec
function upThree(u){ return new THREE.Vector3(u[0], u[2], u[1]).normalize(); }

if(DATA.central_kind==='planet'){
  // oblate planet at 1 R_p equatorial (scaled to scene); bulge ⟂ TRUE spin axis
  const SPIN = DATA.spin_axis ? upThree(DATA.spin_axis) : new THREE.Vector3(0,1,0);
  const planet=new THREE.Mesh(new THREE.SphereGeometry(1,48,32),
    new THREE.MeshStandardMaterial({color:0xc9a06a,roughness:.85}));
  planet.scale.set(SC, SC*(1-DATA.flattening), SC);
  planet.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), SPIN);
  content.add(planet);
  const axL=7;   // spin-axis indicator (blue line through the poles)
  content.add(new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([SPIN.clone().multiplyScalar(-axL), SPIN.clone().multiplyScalar(axL)]),
    new THREE.LineBasicMaterial({color:0x66ccff, transparent:true, opacity:.75})));
}else{
  // star: a small emissive dot + glow sprite at the focus (fixed scene size)
  const star=new THREE.Mesh(new THREE.SphereGeometry(0.5,24,16),
    new THREE.MeshBasicMaterial({color:0xfff2c0}));
  content.add(star);
  const glowTex=(()=>{const c=document.createElement('canvas');c.width=c.height=64;
    const g=c.getContext('2d'),grd=g.createRadialGradient(32,32,0,32,32,32);
    grd.addColorStop(0,'rgba(255,244,200,.9)');grd.addColorStop(1,'rgba(255,244,200,0)');
    g.fillStyle=grd;g.fillRect(0,0,64,64);return new THREE.CanvasTexture(c);})();
  const glow=new THREE.Sprite(new THREE.SpriteMaterial({map:glowTex,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));
  glow.scale.set(3,3,1); content.add(glow);
}
// reference-plane grid (fixed at +Y = the currently selected reference plane)
scene.add(new THREE.PolarGridHelper(23, 8, 6, 64, 0x2a3650, 0x18202e));

// reference-frame toggle: rotate `content` so frames[i].up -> +Y
const framesUI=document.getElementById('frames');
function applyFrame(i){
  const q=new THREE.Quaternion().setFromUnitVectors(upThree(DATA.frames[i].up), new THREE.Vector3(0,1,0));
  content.quaternion.copy(q);
  framesUI.querySelectorAll('button').forEach((b,bi)=>b.classList.toggle('on', bi===i));
}
DATA.frames.forEach((fr,i)=>{
  const b=document.createElement('button'); b.textContent=fr.label; b.onclick=()=>applyFrame(i);
  framesUI.appendChild(b);
});
applyFrame(0);  // default = invariable plane

// per-body: evolving orbit ring + decorative body marker
const N=160; const bodies=[];
for(const m of DATA.bodies){
  const col=new THREE.Color(m.color);
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.BufferAttribute(new Float32Array((N+1)*3),3));
  const ring=new THREE.LineLoop(g, new THREE.LineBasicMaterial({color:col,transparent:true,opacity:.9}));
  content.add(ring);
  const mk=new THREE.Mesh(new THREE.SphereGeometry(0.28,16,12), new THREE.MeshStandardMaterial({color:col,emissive:col,emissiveIntensity:.5}));
  content.add(mk);
  bodies.push({...m, ring, mk, phase:Math.random()*6.283});
}

// legend — keep a direct element reference per body (body names contain spaces,
// e.g. "TRAPPIST-1 b", so a name-based #id selector would be invalid → null).
const leg=document.getElementById('leg');
const legRows={};
for(const m of DATA.bodies){
  const row=document.createElement('div'); row.className='row';
  const nm=document.createElement('span'); nm.className='nm';
  nm.innerHTML=`<span class="sw" style="background:${m.color}"></span>`;
  nm.appendChild(document.createTextNode(m.name));
  const val=document.createElement('span');
  row.appendChild(nm); row.appendChild(val); leg.appendChild(row);
  legRows[m.name]=val;
}

const nF=DATA.frame_times.length;
function lerp(a,b,t){return a+(b-a)*t;}
function elemsAt(m, fpos){
  const i=Math.min(nF-1, Math.floor(fpos)), i2=Math.min(nF-1,i+1), t=fpos-i;
  const A=m.series[i], B=m.series[i2];
  return [lerp(A[0],B[0],t), lerp(A[1],B[1],t), lerp(A[2],B[2],t), lerp(A[3],B[3],t), lerp(A[4],B[4],t)];
}
function updateRing(m, el){
  const [a,e,inc,node,peri]=el;
  const as=a*SC;   // orbit radius scaled to the fixed scene size
  const pos=m.ring.geometry.attributes.position.array;
  for(let k=0;k<=N;k++){ const f=k/N*6.283185;
    const v=orbitVec(as,e,inc*DEG,node*DEG,peri*DEG,f); pos[k*3]=v.x;pos[k*3+1]=v.y;pos[k*3+2]=v.z; }
  m.ring.geometry.attributes.position.needsUpdate=true;
  // decorative marker on illustrative phase, rate ∝ a^-1.5 (Kepler-ish, sped up)
  m.phase += 0.06 * Math.pow(Math.max(as,1.0), -1.5) * 60;
  const v=orbitVec(as,e,inc*DEG,node*DEG,peri*DEG,m.phase); m.mk.position.copy(v);
  legRows[m.name].textContent=`i=${inc.toFixed(1)}°  e=${e.toFixed(3)}`;
}

// playback
let fpos=0, playing=true, speed=nF/600; // ~10 s to sweep the run at 60fps
const yr=document.getElementById('yr'), scrub=document.getElementById('scrub'), playBtn=document.getElementById('play');
playBtn.onclick=()=>{playing=!playing; playBtn.textContent=playing?'⏸ 일시정지':'▶ 재생';};
scrub.oninput=()=>{fpos=(+scrub.value/1000)*(nF-1); playing=false; playBtn.textContent='▶ 재생';};

function tick(){
  requestAnimationFrame(tick);
  if(playing){ fpos+=speed; if(fpos>=nF-1){fpos=0;} scrub.value=(fpos/(nF-1))*1000; }
  for(const m of bodies) updateRing(m, elemsAt(m, fpos));
  yr.textContent=`${DATA.frame_times[Math.round(fpos)]|0} yr`;
  controls.update(); renderer.render(scene,camera);
}
tick();
addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);});
</script>
"""

title = f"{summary['system']} — 3D orbit evolution"
html = (HTML
        .replace("__DATA__", json.dumps(data))
        .replace("__TITLE__", title)
        .replace("__SYSTEM__", summary["system"])
        .replace("__CENTER__", center)
        .replace("__UNIT__", unit)
        .replace("__VERDICT__", j["overall"].upper())
        .replace("__INTEG__", integ["integrator"])
        .replace("__DT__", str(data["dt_min"]))
        .replace("__DE__", data["dE"]))

out = d / f"{args.label}_orbit3d.html"
out.write_text(html)
print(f"wrote {out}  ({mode}-center '{center}', {len(frame_times)} frames, {len(names)} bodies, unit {unit})")
