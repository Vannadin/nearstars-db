# chain.yaml 의 via 가 공급자의 outputs 에 실재하는지 — 그래프의 화살표가 약속을 지키는지 검사한다 (브리프 43)
"""Check every `via` in chain.yaml against its supplier's declared `outputs`.

    python3 engine/check_via.py            # report: every mismatch, classified; never fails
    python3 engine/check_via.py --gate     # fail on any mismatch not in the allowlist

Why this exists. `via` reads as a contract ("넘어가는 양") but until 2026-09-03 nothing read it
except `build_graph_page.py`, for a tooltip. The parallel seat parsed all 91 via-edges: 35 named a
quantity the supplier does not emit — five renames, eight derivables, ten selects-discriminants,
eight real breaks, three misroutings (one of which was the supplier's output list being short,
not the arrow). The header's own warning is *"근거 없는 엣지는 넣지 않는다. 그림을 위해 추측한
화살표가 이 프로젝트가 반복해 온 실수다"*, and four of those arrows were pointing at nodes that
do not emit what they promise.

What the gate accepts. After Brief 43's edits, every remaining mismatch must be in ALLOWLIST:
edges whose `via` names a quantity **derivable** from the supplier's outputs, each row recording
**which inputs combine** — not merely "derivable", which would license anything. A mismatch that
is not allowlisted is either a new wrong arrow or a new promise nobody keeps; the gate names it
and fails. Adding a row here is a declaration and belongs in the same commit as the edge.

The mechanical parts (mismatch, misroute) are the parallel seat's `via_triage.py` (2026-09-03),
ported; the class table lived there and is summarised in the allowlist reasons and in
engine/via-context-notes.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

CHAIN = Path(__file__).resolve().parent / "chain.yaml"

# (from, to, via) -> which supplier outputs (and which other edges) combine into it.
ALLOWLIST = {
    ("orbit_elements", "dynamo_rocky", "period"):
        "from `n`: P = 2π/n",
    ("mass_or_radius", "surface_dose", "gravity"):
        "from `mass`,`radius`: g = GM/R²",
    ("mass_or_radius", "atmospheric_escape", "v_esc"):
        "from `mass`,`radius`: v_esc = √(2GM/R)",
    ("mass_radius_relation", "body_class", "radius_valley"):
        "from `radius`,`density`: a classification boundary, not a new quantity",
    # The four below name the quantity the edge CONTRIBUTES TO, assembled across several edges.
    ("star_physical", "mass_radius_relation", "insolation"):
        "COMBINES `luminosity` (here) + `a` (orbit_elements): S = L/(4πa²)",
    ("atmosphere_choice", "surface_dose", "column"):
        "COMBINES `pressure`,`composition` (here) + gravity (mass_or_radius): column = P/g per species",
    ("t_eq_stellar", "atmosphere_choice", "scale_height"):
        "COMBINES `t_eq` (here) + gravity (mass_or_radius) + mean molecular mass (atmosphere_choice): H = kT/(μ m_u g)",
    ("t_eq_stellar", "crater_state", "homologous_temperature"):
        "COMBINES `t_eq` (here) + a melting temperature (the surface material's): T_h = T/T_melt",
}


def load(path: Path = CHAIN) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def mismatches(d: dict) -> tuple[list[tuple], int]:
    """Every via-edge whose via is not in its supplier's outputs. Mechanical."""
    nodes = d["nodes"]
    out, total = [], 0
    for e in d.get("edges") or []:
        via = e.get("via")
        if via is None:
            continue
        total += 1
        src, dst = e.get("from"), e.get("to")
        outs = (nodes.get(src) or {}).get("outputs") or []
        for v in (via if isinstance(via, list) else [via]):
            if v not in outs:
                out.append((src, dst, v, e))
    return out, total


def emitters(d: dict) -> dict[str, list[str]]:
    own: dict[str, list[str]] = {}
    for n, spec in d["nodes"].items():
        for o in (spec or {}).get("outputs") or []:
            own.setdefault(o, []).append(n)
    return own


def main(argv: list[str]) -> int:
    gate = "--gate" in argv
    d = load()
    miss, total = mismatches(d)
    own = emitters(d)
    allowed, gapped, open_ = [], [], []
    for src, dst, v, e in miss:
        key = (src, dst, v)
        if key in ALLOWLIST:
            allowed.append((key, ALLOWLIST[key]))
        elif e.get("status") == "gap":
            gapped.append(key)
        else:
            open_.append((key, own.get(v, [])))

    print(f"via 엣지 {total}개 · outputs 에 없는 via {len(miss)}개 — 허용목록 {len(allowed)} · "
          f"status:gap {len(gapped)} · 미분류 {len(open_)}")
    for key, why in allowed:
        print(f"  [ALLOW] {key[0]} → {key[1]} via {key[2]}: {why}")
    for key in gapped:
        print(f"  [GAP]   {key[0]} → {key[1]} via {key[2]} (status: gap — 결합은 실재, 공급자가 아직 내지 않는다)")
    for key, who in open_:
        hint = (f" — 이 양은 {', '.join(who)} 가 낸다" + (" (목적지!)" if key[1] in who else "")) if who else ""
        print(f"  [{'FAIL' if gate else 'OPEN'}] {key[0]} → {key[1]} via {key[2]}: 공급자 outputs 에 없다{hint}")
    if gate and open_:
        print(f"  {len(open_)}개의 via 가 지켜지지 않는 약속이다 — outputs 에 넣거나, 이름을 고치거나, "
              "status: gap 으로 적거나, 도출이면 ALLOWLIST 에 어느 입력이 합쳐지는지와 함께 적어라")
        return 1
    if gate:
        print(f"  [PASS] 모든 via 가 공급자 outputs 에 있거나 허용목록/gap 에 적혀 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
