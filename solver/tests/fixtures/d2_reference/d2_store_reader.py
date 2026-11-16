# D2 저장 파일의 기준 읽기기(노트 17 §4.1) — 계약(§2)만 보고 쓴 읽기: 불러오기·닫힌 칸·판 번호·여섯 고리 사슬·(P, T) 의 칸 부류와 값; 엔진도 bmcpp 도 import 하지 않음(엔진 읽기 등록이 이것과 견줌)
"""Reference reader of the D2 store, written from prereg-bmcpp note 17 §2 (with note 19) only. It imports nothing
from the engine or from bmcpp, so the engine read (its own registration) can be checked against it.

    doc = load(raw_gz_bytes)              # closed keys, contract version, one known class per cell → or ReaderRefusal
    chain(doc, store_sha256, yaml_doc, compact, compact_sha256)   # note 17 §3.3's six links → or ReaderRefusal
    read(doc, p, t) → {"read": "table", "why": …} | {"read": "d2"|"cut"|"subgrid", "field": …, "values": {…}}

Classes (§2.3): d2, cut, subgrid, fallback, limit; no class refuses (note 17 as amended): fallback, limit, a cell with
no entry, and a d2 point with no field left read the record's table. Counts of «d2: no field at the point → table
read» are kept in COUNTS."""
import gzip
import json
import math

TOP_KEYS = ("cells", "contract", "counts", "edges", "fields", "grid", "header")       # contract v2 (note 37 §1)
CLASSES = ("cut", "d2", "fallback", "limit", "subgrid")
CORNERS = ((0, 0), (1, 0), (0, 1), (1, 1))
NO_FIELD = "d2: no field at the point → table read"
COUNTS = {NO_FIELD: 0}


class ReaderRefusal(Exception):
    pass


def load(raw):
    doc = json.loads(gzip.decompress(raw))
    c = doc.get("contract") or {}
    if c.get("name") == "nearstars d2 store" and c.get("version") == 1:
        raise ReaderRefusal("contract version 1: positions need the v2 `edges` block (note 37)")
    if sorted(doc) != list(TOP_KEYS):
        raise ReaderRefusal(f"material.d2_store_keys: top-level keys {sorted(doc)}")
    c = doc["contract"]
    if c.get("name") != "nearstars d2 store" or c.get("version") != 2:
        raise ReaderRefusal(f"material.d2_store_contract: {c}")
    for key, cell in doc["cells"].items():
        if cell.get("class") not in CLASSES:
            raise ReaderRefusal(f"material.d2_store_class: cell {key} class {cell.get('class')!r}")
    return doc


def compact_keys(compact):
    """the compact's two chain keys, at the paths step 5 writes them: `source.table_blob`, and the interp term file's
    git blob at `interp_terms.source.file_blob` (note 44; absent → None, which the chain refuses)"""
    return {"table_blob": (compact.get("source") or {}).get("table_blob"),
            "interp_term_blob": ((compact.get("interp_terms") or {}).get("source") or {}).get("file_blob")}


def chain(doc, store_sha256, yaml_doc, compact, compact_sha256):
    """note 17 §3.3's six links: yaml pins.compact_sha256 = the compact's sha256; yaml d2_store.sha256 = the store's;
    store record_id = the yaml's id; store table_blob = the compact's source table_blob; store interp term blob = the
    compact's interp_terms' blob; store builder_manifest_blob = the yaml pins' builder blob (the «strict» builder)
    (r2 n4 on 69115f42f: the first and the last were missing)."""
    h = doc["header"]
    compact_header = compact_keys(compact)
    pins = (yaml_doc.get("assemblage") or {}).get("pins") or {}
    strict = next((b.get("blob") for b in pins.get("builders") or [] if b.get("role") == "strict"), None)
    links = [("pins.compact_sha256", pins.get("compact_sha256"), compact_sha256),
             ("d2_store.sha256", yaml_doc.get("d2_store", {}).get("sha256"), store_sha256),
             ("builder_manifest_blob", strict, h.get("builder_manifest_blob")),
             ("record_id", yaml_doc.get("id"), h.get("record_id")),
             ("table_blob", compact_header.get("table_blob"), h.get("table_blob")),
             ("interp_term_blob", compact_header.get("interp_term_blob"), (h.get("inputs") or {}).get("interp_term_blob"))]
    for name, want, got in links:
        if want is None or want != got:
            raise ReaderRefusal(f"material.d2_store_chain: {name}: {want!r} ≠ {got!r}")


def _h(u, d):
    if d == 0:
        return (2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2, u**3 - u**2)
    if d == 1:
        return (6 * u**2 - 6 * u, 3 * u**2 - 4 * u + 1, -6 * u**2 + 6 * u, 3 * u**2 - 2 * u)
    return (12 * u - 6, 6 * u - 4, -12 * u + 6, 6 * u - 2)


def _g(cs, p0, p1, t0, t1, p, t, dp, dt, which):
    """Form (ii) (s3-d2 §2.4): bicubic Hermite on G with V, −S and ∂V/∂T at the four corners."""
    hp, ht = p1 - p0, t1 - t0
    bu, bv = _h((p - p0) / hp, dp), _h((t - t0) / ht, dt)
    tot = 0.0
    for (i, l), c in zip(CORNERS, cs):
        f = c["g_cons"] if which == "cons" else c["g"]
        a0, a1, b0, b1 = bu[2 * i], bu[2 * i + 1], bv[2 * l], bv[2 * l + 1]
        tot += f * a0 * b0 + c["v"] * hp * a1 * b0 + (-c["s"]) * ht * a0 * b1 + c["w"] * hp * ht * a1 * b1
    return tot / (hp ** dp * ht ** dt)


def _min_mode(cs, u, v):
    w = ((1 - u) * (1 - v), u * (1 - v), (1 - u) * v, u * v)
    return min(sum(wi * c["amounts"][q] for wi, c in zip(w, cs)) for q in range(len(cs[0]["amounts"])))


def _values(cs, box, p, t):
    gp, gt = _g(cs, *box, p, t, 1, 0, "cons"), _g(cs, *box, p, t, 0, 1, "cons")
    gpp, gtt, gpt = _g(cs, *box, p, t, 2, 0, "cons"), _g(cs, *box, p, t, 0, 2, "cons"), _g(cs, *box, p, t, 1, 1, "cons")
    return {"rho": 1.0 / gp, "s": -gt, "c_p": -t * gtt, "dtdp": -gpt / gtt if gtt else math.nan}


def _corner_doc(n):
    return {"g": n["g_solved"], "g_cons": n["g_consistent"], "v": n["v"], "s": n["s"], "w": n["dv_dt_eq"],
            "amounts": n["amounts"]}


def _corners_of(doc, field, j, k):
    nodes = doc["fields"][field]["nodes"]
    return [_corner_doc(nodes[f"{j + i},{k + l}"]) for i, l in CORNERS]


def _cell_of(ps, x):
    for i in range(len(ps) - 1):
        if ps[i] <= x <= ps[i + 1]:
            return i
    return None


def read(doc, p, t):
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    j, k = _cell_of(ps, p), _cell_of(ts, t)
    if j is None or k is None:
        return {"read": "table", "why": "outside the store's grid"}
    cell = doc["cells"].get(f"{j},{k}")
    if cell is None:
        return {"read": "table", "why": "no entry (frozen corner or above p_dataset)"}
    box = (ps[j], ps[j + 1], ts[k], ts[k + 1])
    u, v = (p - box[0]) / (box[1] - box[0]), (t - box[2]) / (box[3] - box[2])
    cls = cell["class"]
    if cls in ("fallback", "limit"):
        return {"read": "table", "why": cls}
    if cls == "d2":
        ok = {}
        for f in cell["surfaces"]:
            cs = _corners_of(doc, f, j, k)
            if _min_mode(cs, u, v) >= 0.0:
                ok[f] = cs
        if not ok:
            COUNTS[NO_FIELD] += 1
            return {"read": "table", "why": NO_FIELD}
        f = min(ok, key=lambda x: _g(ok[x], *box, p, t, 0, 0, "solved"))
        return {"read": "d2", "field": f, "values": _values(ok[f], box, p, t)}
    if cls == "cut":
        c = cell["cut"]
        (x1, y1), (x2, y2) = c["points"]
        cross = lambda uu, vv: (x2 - x1) * (vv - y1) - (y2 - y1) * (uu - x1)  # noqa: E731
        a0 = c["a_corners"][0]
        side_a = cross(u, v) * math.copysign(1.0, cross(*a0)) > 0
        if side_a:                               # A's own corners from fields, B's corners from A's virtual nodes
            f = c["a"]
            nodes = doc["fields"][f]["nodes"]
            cs = [_corner_doc(c["a_virtual"].get(f"{j + i},{k + l}") or nodes[f"{j + i},{k + l}"]) for i, l in CORNERS]
        else:
            f = c["b"]
            cs = _corners_of(doc, f, j, k)
        return {"read": "cut", "field": f, "values": _values(cs, box, p, t)}
    # subgrid (note 17 §2.5): u along the sides, w across; lines linear in w; inside the sliver the blend of the two
    # sides' quadratics at s; outside it the table
    s0, s1 = sorted(cell["sides"], key=lambda s: min(map(tuple, s["nodes"])))
    along = (u, v) if cell["direction"] == "P" else (v, u)
    uu, w = along
    lo, hi = (box[0], box[1]) if cell["direction"] == "P" else (box[2], box[3])
    pos = lambda pt: ((pt[0] if cell["direction"] == "P" else pt[1]) - lo) / (hi - lo)  # noqa: E731
    rev = s1["A"] != s0["A"]
    ua = [pos(s0["lines"][0]), pos(s1["lines"][1] if rev else s1["lines"][0])]
    ub = [pos(s0["lines"][1]), pos(s1["lines"][0] if rev else s1["lines"][1])]
    k0 = s0["knots"]
    k1 = {"A": s1["knots"]["B"], "C": s1["knots"]["C"], "B": s1["knots"]["A"]} if rev else s1["knots"]
    la, lb = (1 - w) * ua[0] + w * ua[1], (1 - w) * ub[0] + w * ub[1]
    if not (min(la, lb) <= uu <= max(la, lb)):
        return {"read": "table", "why": "subgrid cell outside the sliver"}
    sfr = (uu - la) / (lb - la)

    def q(kn, x, name):
        a, m, b = kn["A"][name], kn["C"][name], kn["B"][name]
        return 2 * (x - 0.5) * (x - 1) * a - 4 * x * (x - 1) * m + 2 * x * (x - 0.5) * b   # Lagrange, as note 15 §2
    vals = {n: (1 - w) * q(k0, sfr, n) + w * q(k1, sfr, n) for n in ("rho", "c_p", "alpha", "s")}
    vals["dtdp"] = t * vals["alpha"] / (vals["rho"] * vals["c_p"])   # §2.5: T·α/(ρ·c_P) from the read's own values,
    return {"read": "subgrid", "field": s0["C"], "values": vals}    # never differentiated (r2 n5 on 69115f42f)
