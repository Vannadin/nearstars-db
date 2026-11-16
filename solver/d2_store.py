# D2 저장소(v2) 의 엔진 적재 검사 — 기록의 d2_read 상태·저장소 계약·여섯 고리 사슬·격자·edges 블록(행 동등·today·traced·kind·counts·coincident)·(2b) today 구간 칸 검사·(S1) sliver·인증 연장 행 H6; 아무 적재 경로도 부르지 않는 잠든 조각(D2 읽기 등록 rev 7 §2, §3, §5b; post-freeze note 2)
"""The view piece of the engine's D2 read (prereg-d2-engine-read rev 7, §2, §3 and §5b's load checks; post-freeze
note 2 (1)). Dormant: nothing on the load path imports this module (a test asserts that fall_sets.closure() does not
hold it and that material_assemblage.py is still the blob the tables' closure terms pin).

It imports material_assemblage's primitives and changes none of them. Its decisions are its own code, independent of
the writer's (rev 7 §5b (2b): «the loader's code is independent of the writer's»; note 2 (3)).

    load(record_doc, compact, materials_dir) → Loaded | None      (None: d2_read off; the store is never opened)
    check_edges(loaded, compact, view_on_store, view_on_compact)  (§5b's load checks; raises StoreRefusal)

Every refusal is a StoreRefusal whose `id` is the registration's name (material.d2_store_*)."""
import bisect
import gzip
import hashlib
import json
import math
from pathlib import Path
from types import MappingProxyType

from solver import material_assemblage as ma

CONTRACT_NAME = "nearstars d2 store"
TOP_KEYS = ("cells", "contract", "counts", "edges", "fields", "grid", "header")          # §2, contract v2
CLASSES = ("cut", "d2", "fallback", "limit", "subgrid")
STATES = ("off", "eligible", "ruled")
BASIS_KEYS = MappingProxyType({"eligible": ("line", "report_blob"), "ruled": ("date", "rows", "text_ref")})
#: §5b: the three keys the writer adds per edge, per node-resolved or swap row and per extension row
NEW_KEYS = ("match", "p_b_source", "p_b_today")
MATCH_KINDS = ("accepted", "unmatched", "none", "swap", "node", "no_p_b", "pair_split", "extension")
MATCH_POINT_KEYS = ("gap_cells", "n_candidates", "p", "phase_key", "record", "t")      # accepted and unmatched only
SOURCE_NEW_KEYS = ("compact_boundaries_sha256", "counts", "edges_json_sha256", "match_rule")
TOL_COINCIDENT = 1e-9           # AssemblageView init's own test, relative (l.1406 at ab5287970)
P_TOL = 1e5                     # Pa: boundary_pass.P_TOL (frozen §3.3), (S1)'s tolerance
S1_WS = (0.0, 0.25, 0.5, 0.75, 1.0)

# ── the read piece's interface (S0 stubs, D2-read note 2 (1); frozen here so ea's driver and harness can be written
#    against it; 68 checks the shape against the frozen text, not the logic) ─────────────────────────────────────────
#: §6 and d2_store_reader.NO_FIELD, verbatim: a d2 cell whose fields all miss the point reads the record's table
NO_FIELD = "d2: no field at the point → table read"
#: §6's run-time counts, per view (cleared and restored by `_quiet` like `s_counts`). NO_FIELD is §6's own name; the
#: other three name §5b's part-2 counts: (4) swap segments through a d2 or cut cell, (S1)'s per-read count, and
#: (5) forced reads on cut cells
COUNT_NAMES = (NO_FIELD, "d2: swap segment through a d2 or cut cell", "d2: (S1) read inside a subgrid sliver",
               "d2: forced side on a cut cell")
#: §6's proposed run-record line, one per record in material_notes: «<count name>: N of M reads»
RUN_RECORD_LINE = "{name}: {n} of {m} reads"
#: the reference reader's answer keys (d2_store_reader.read): «read» is table | d2 | cut | subgrid; a table answer
#: carries «why», a D2 answer «field» and «values» with these four quantities
READ_CLASSES = ("table", "d2", "cut", "subgrid")
VALUE_KEYS = ("c_p", "dtdp", "rho", "s")
#: a subgrid answer also carries alpha (dT/dP is T·α/(ρ·c_P) from it), as the reference reader's does
SUBGRID_VALUE_KEYS = ("alpha", "c_p", "dtdp", "rho", "s")


class StoreRefusal(Exception):
    """A named load refusal (§2, §3, §5b)."""

    def __init__(self, rid, why):
        super().__init__(f"{rid}: {why}")
        self.id, self.why = rid, why


class Loaded:
    """A D2 record's store, loaded and chained: the state, the document and the store's sha256."""

    def __init__(self, state, doc, sha256):
        self.state, self.doc, self.sha256 = state, doc, sha256


# ── the primitives' arithmetic, re-stated (note 2 (1), conditions 2 and 3) ─────────────────────────────────────────
def reach(ts):
    """(R1) §4's side reach past a cut curve's end, EXT_ROWS T rows: the value AssemblageView keeps as `_reach`."""
    return ma.EXT_ROWS * (ts[1] - ts[0]) if len(ts) > 1 else 0.0


def coincident(cut_runs):
    """The cut runs init merges into one step: runs over the same T rows whose P_b agree on every row within
    TOL_COINCIDENT × P_b, relative. → (count, ids): `count` is init's `coincident` (the merged runs that were edges),
    `ids` every merged run's id (each becomes kind «swap»). Reads only; `cut_runs` as _cut_runs(build_curves(…))."""
    by_ts = {}
    for c in cut_runs:
        by_ts.setdefault(tuple(r["t"] for r in c.rows), []).append(c)
    count, ids = 0, set()
    for group in by_ts.values():
        for a in group:
            if any(b is not a and all(abs(ra["p_b"] - rb["p_b"]) <= TOL_COINCIDENT * ra["p_b"]
                                      for ra, rb in zip(a.rows, b.rows)) for b in group):
                ids.add(a.id)
                count += a.kind == "edge"
    return count, ids


def curve_kinds(block, ts):
    """{(kind after the merge, phase, row T tuple, row p_lo tuple)} of a block's cut runs: what a view built on the
    block reads as steps and edges, for comparing two blocks' curve kinds."""
    runs = ma._cut_runs(ma.build_curves(block, ts))
    _n, ids = coincident(runs)
    return sorted(("swap" if c.id in ids else c.kind, c.phase or "", tuple(r["t"] for r in c.rows),
                   tuple(r["p_lo"] for r in c.rows)) for c in runs)


# ── §2: the record's fields and the store's contract ───────────────────────────────────────────────────────────────
def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def state_of(record_doc):
    """§2: the record's `d2_read` state; absent → off. A present key with no or an unknown value is a refusal."""
    rid = record_doc.get("id")
    if "d2_read" not in record_doc:
        return "off"
    v = record_doc["d2_read"]
    if v not in STATES:
        raise StoreRefusal("material.d2_read_unknown", f"record {rid}: d2_read {v!r}")
    return v


def check_keys(record_doc):
    """§2's record-key refusals, with nothing opened: the state (absent → off; unknown → refusal), a `d2_read_basis` or
    `d2_store` key on an off or absent record, the basis's exact keys, and the pin's shape and fields/ path. Returns
    (state, the pin's relative path) — (\"off\", None) when off. The registry runs it on every assemblage record at load,
    whatever the global switch (68 B1, B2 on 54dd5042: §4 forbids opening the store with the switch off, not checking
    the record's own keys); `load` runs it again before opening."""
    rid = record_doc.get("id")
    state = state_of(record_doc)
    if state == "off":
        for k in ("d2_read_basis", "d2_store"):
            if k in record_doc:
                raise StoreRefusal("material.d2_store_missing" if k == "d2_store" else "material.d2_read_basis",
                                   f"record {rid}: {k} on a record whose d2_read is off")
        return state, None
    basis = record_doc.get("d2_read_basis")
    if not isinstance(basis, dict):
        raise StoreRefusal("material.d2_read_basis", f"record {rid}: d2_read {state} without d2_read_basis")
    miss = [k for k in BASIS_KEYS[state] if basis.get(k) in (None, "")]
    if miss or sorted(basis) != sorted(BASIS_KEYS[state]):
        raise StoreRefusal("material.d2_read_basis", f"record {rid}: d2_read_basis for {state} must hold exactly "
                           f"{list(BASIS_KEYS[state])}; missing {miss}, has {sorted(basis)}")
    pin = record_doc.get("d2_store")
    if not isinstance(pin, dict) or not isinstance(pin.get("path"), str) or not isinstance(pin.get("sha256"), str):
        raise StoreRefusal("material.d2_store_missing", f"record {rid}: d2_store {{path, sha256}} missing")
    rel = Path(pin["path"])
    if rel.is_absolute() or ".." in rel.parts or rel.parts[:1] != ("fields",):
        raise StoreRefusal("material.d2_store_missing", f"record {rid}: d2_store path {pin['path']!r} is not under fields/")
    return state, rel


def load(record_doc, compact, materials_dir, compact_sha256=None):
    """§2 and §3. d2_read off (or absent) → None, and the store is never opened (a `d2_store` key is then a refusal:
    the writer never writes it there). Else the store is read, its contract and classes checked, its grid compared to
    the compact's nodes and the six links of the chain checked."""
    rid = record_doc.get("id")
    state, rel = check_keys(record_doc)
    if state == "off":
        return None
    path = Path(materials_dir) / rel
    if not path.is_file():
        raise StoreRefusal("material.d2_store_missing", f"record {rid}: no file {rel}")
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    doc = json.loads(gzip.decompress(raw))
    check_contract(doc, rid)
    check_grid(doc, compact, rid)
    chain(doc, sha, record_doc, compact, compact_sha256)
    return Loaded(state, doc, sha)


def check_contract(doc, rid="?"):
    """§2's rows: the contract (v1 refused once, by name), the closed top-level keys, one known class per cell."""
    c = doc.get("contract") if isinstance(doc.get("contract"), dict) else {}
    if c.get("name") == CONTRACT_NAME and c.get("version") == 1:
        raise StoreRefusal("material.d2_store_contract", f"record {rid}: contract version 1: v1 has no edges block")
    if sorted(doc) != list(TOP_KEYS):
        raise StoreRefusal("material.d2_store_keys", f"record {rid}: top-level keys {sorted(doc)}, not {list(TOP_KEYS)}")
    if c.get("name") != CONTRACT_NAME or c.get("version") != 2:
        raise StoreRefusal("material.d2_store_contract", f"record {rid}: contract {c!r}, not {CONTRACT_NAME!r} version 2")
    for key, cell in doc["cells"].items():
        if not isinstance(cell, dict) or cell.get("class") not in CLASSES:
            raise StoreRefusal("material.d2_store_class", f"record {rid}: cell {key} class "
                               f"{(cell or {}).get('class') if isinstance(cell, dict) else cell!r}")


def nodes(compact):
    return sorted({c["p"] for c in compact["cells"]}), sorted({c["t"] for c in compact["cells"]})


def check_grid(doc, compact, rid="?"):
    """§2: the store's grid equals the compact's P and T nodes over the population's range: its T rows are the
    compact's T rows (the view's `ts`), its P nodes a contiguous run of the compact's P nodes."""
    ps, ts = nodes(compact)
    g = doc.get("grid") or {}
    sp, st = list(g.get("ps") or ()), list(g.get("ts") or ())
    ok = st == ts and len(sp) >= 2 and sp[0] in ps and ps[ps.index(sp[0]):ps.index(sp[0]) + len(sp)] == sp
    if not ok:
        raise StoreRefusal("material.d2_store_grid", f"record {rid}: the store's grid ({len(sp)} P, {len(st)} T) is not "
                           f"the compact's nodes ({len(ps)} P, {len(ts)} T) over its range")


def interp_term_blob(compact):
    """The compact's interp-term blob (§3 link 6): `interp_terms.source.file_blob`, the git blob of the interp sidecar
    file step 5 was handed. Today no compact writes it (ea 11-13: note 17 §3.3 presumes a key that is not written);
    ea's post-freeze note through r2 adds it to step 5. Until then a D2 record cannot pass link 6, which is the
    registered refusal, not a fallback."""
    return ((compact.get("interp_terms") or {}).get("source") or {}).get("file_blob")


def chain(doc, store_sha256, record_doc, compact, compact_sha256):
    """§3: note 17 §3.3's six links, in the reference reader's order; each miss names the link and both values."""
    h = doc["header"]
    pins = (record_doc.get("assemblage") or {}).get("pins") or {}
    strict = next((b.get("blob") for b in pins.get("builders") or () if b.get("role") == "strict"), None)
    links = (("pins.compact_sha256", pins.get("compact_sha256"), compact_sha256),
             ("d2_store.sha256", (record_doc.get("d2_store") or {}).get("sha256"), store_sha256),
             ("builder_manifest_blob", strict, h.get("builder_manifest_blob")),
             ("record_id", record_doc.get("id"), h.get("record_id")),
             ("table_blob", (compact.get("source") or {}).get("table_blob"), h.get("table_blob")),
             ("interp_term_blob", interp_term_blob(compact), (h.get("inputs") or {}).get("interp_term_blob")))
    for name, want, got in links:
        if want is None or want != got:
            raise StoreRefusal("material.d2_store_chain", f"record {record_doc.get('id')}: link {name}: {want!r} ≠ {got!r}")


# ── §5b: the edges block against the compact's boundaries ──────────────────────────────────────────────────────────
def _units(block):
    """[(where, unit dict, compact-side key path)]: every unit carrying §5b's three keys — an edge of an edge-class row
    that is not node-resolved; a node-resolved row (and each of its edges, kind node too); a swap row; an extension
    row."""
    out = []
    for i, r in enumerate(block.get("rows", ())):
        if r.get("node_resolved") or r.get("class") == "swap":
            out.append((f"row {i}", r))
        if r.get("node_resolved") or r.get("class") != "swap":
            for e_i, e in enumerate(r.get("edges") or ()):
                out.append((f"row {i} edge {e_i}", e))
    for i, r in enumerate((block.get("extension") or {}).get("rows", ())):
        out.append((f"extension row {i}", r))
    return out


def _strip(d):
    return {k: v for k, v in d.items() if k not in NEW_KEYS and k != "p_b"}


def check_edges_rows(edges, boundaries, rid="?"):
    """material.d2_store_edges_rows: the store's block equals the compact's, `==`, on every key except `p_b` and the
    three new keys; one row for one row, one edge for one edge, one extension row for one; the block's `source` is the
    compact's plus exactly SOURCE_NEW_KEYS."""
    def refuse(why):
        raise StoreRefusal("material.d2_store_edges_rows", f"record {rid}: {why}")
    if sorted(edges) != sorted(boundaries):
        refuse(f"block keys {sorted(edges)} ≠ the compact's {sorted(boundaries)}")
    if edges.get("status") != boundaries.get("status"):
        refuse(f"status {edges.get('status')!r} ≠ {boundaries.get('status')!r}")
    src, csrc = edges.get("source") or {}, boundaries.get("source") or {}
    if sorted(set(src) - set(csrc)) != sorted(SOURCE_NEW_KEYS) or any(src.get(k) != v for k, v in csrc.items()):
        refuse(f"source keys {sorted(src)} are not the compact's {sorted(csrc)} plus {list(SOURCE_NEW_KEYS)}")
    for part in ("rows", "extension"):
        a = edges.get("rows", []) if part == "rows" else (edges.get("extension") or {}).get("rows", [])
        b = boundaries.get("rows", []) if part == "rows" else (boundaries.get("extension") or {}).get("rows", [])
        if part == "extension" and _strip({k: v for k, v in (edges.get("extension") or {}).items() if k != "rows"}) != \
                _strip({k: v for k, v in (boundaries.get("extension") or {}).items() if k != "rows"}):
            refuse("the extension block's keys other than rows differ")
        if len(a) != len(b):
            refuse(f"{part}: {len(a)} rows ≠ the compact's {len(b)}")
        for i, (ra, rb) in enumerate(zip(a, b)):
            if {k: v for k, v in _strip(ra).items() if k != "edges"} != {k: v for k, v in _strip(rb).items() if k != "edges"}:
                refuse(f"{part} row {i} differs from the compact's on a copied key")
            ea_, eb_ = ra.get("edges"), rb.get("edges")
            if (ea_ is None) != (eb_ is None) or len(ea_ or ()) != len(eb_ or ()):
                refuse(f"{part} row {i}: edges {len(ea_ or ())} ≠ the compact's {len(eb_ or ())}")
            for e_i, (x, y) in enumerate(zip(ea_ or (), eb_ or ())):
                if _strip(x) != _strip(y):
                    refuse(f"{part} row {i} edge {e_i} differs from the compact's on a copied key")


def _compact_pb(boundaries):
    """The compact's own p_b per unit, in _units' order."""
    return [u.get("p_b") for _w, u in _units(boundaries)]


def check_units(edges, boundaries, rid="?"):
    """§5b's per-unit checks: the three keys present; `kind` closed and the keys present matching it; «today» →
    p_b == p_b_today == the compact's p_b (n2; material.d2_store_today_row); «traced» → p_lo < p_b < p_hi strictly
    (the row's pair); p_b_today always the compact's value; `source.counts` equal to the loader's own count."""
    rows = edges.get("rows", [])
    owner = {}
    for i, r in enumerate(rows):
        owner[f"row {i}"] = r
        for e_i in range(len(r.get("edges") or ())):
            owner[f"row {i} edge {e_i}"] = r
    for i, r in enumerate((edges.get("extension") or {}).get("rows", [])):
        owner[f"extension row {i}"] = r
    units, want = _units(edges), _compact_pb(boundaries)
    if len(units) != len(want):
        raise StoreRefusal("material.d2_store_edges_rows", f"record {rid}: {len(units)} units ≠ the compact's {len(want)}")
    counts = {k: 0 for k in MATCH_KINDS}
    over, multi = 0, 0
    for (where, u), pb_c in zip(units, want):
        miss = [k for k in NEW_KEYS if k not in u]
        if miss:
            raise StoreRefusal("material.d2_store_keys", f"record {rid}: {where} lacks {miss}")
        m = u["match"] if isinstance(u["match"], dict) else {}
        kind = m.get("kind")
        if kind not in MATCH_KINDS:
            raise StoreRefusal("material.d2_store_keys", f"record {rid}: {where} match.kind {kind!r}")
        point = kind in ("accepted", "unmatched")
        if sorted(k for k in m if k != "kind") != (list(MATCH_POINT_KEYS) if point else []):
            raise StoreRefusal("material.d2_store_keys", f"record {rid}: {where} match keys {sorted(m)} for kind {kind}")
        src = u["p_b_source"]
        if src not in ("today", "traced") or (src == "traced") != point:
            raise StoreRefusal("material.d2_store_keys", f"record {rid}: {where} p_b_source {src!r} with kind {kind}")
        if u["p_b_today"] != pb_c:
            raise StoreRefusal("material.d2_store_today_row", f"record {rid}: {where} p_b_today {u['p_b_today']!r} ≠ "
                               f"the compact's {pb_c!r}")
        if src == "today" and u.get("p_b") != pb_c:
            raise StoreRefusal("material.d2_store_today_row", f"record {rid}: {where} is «today» with p_b "
                               f"{u.get('p_b')!r} ≠ the compact's {pb_c!r}")
        if src == "traced":
            r = owner[where]
            pb = u.get("p_b")
            if not (ma._finite(r.get("p_lo")) and ma._finite(r.get("p_hi"))):   # an uncertified extension row has no
                raise StoreRefusal("material.d2_store_edges_rows",              # pair: «traced» there is refused by id
                                   f"record {rid}: {where} is «traced» on a row without p_lo/p_hi")
            if not (ma._finite(pb) and r["p_lo"] < pb < r["p_hi"]):
                raise StoreRefusal("material.d2_store_edges_rows", f"record {rid}: {where} is «traced» with p_b {pb!r} "
                                   f"not strictly inside ({r['p_lo']!r}, {r['p_hi']!r})")
            over += m["gap_cells"] > 0.1 and kind == "unmatched"
            multi += m["n_candidates"] > 1
        if not (where.startswith("row ") and " edge " not in where and owner[where].get("node_resolved")):
            counts[kind] += 1                    # the writer's count (d2_edges_v2 rule 2): a node-resolved row's
                                                 # edges are counted, the row itself is marked but not counted
    mine = {**counts, "unmatched_over_0p1_cell": over, "multi_candidate": multi}
    got = dict((edges.get("source") or {}).get("counts") or {})
    got.pop("coincident_created", None)          # the writer's own per-row flag (§5b: not an engine mismatch)
    if got != mine:
        raise StoreRefusal("material.d2_store_edges_rows", f"record {rid}: source.counts {got} ≠ the loader's {mine}")


def check_coincident(edges, boundaries, ts, rid="?"):
    """material.d2_store_coincident: the coincident set and the curve kinds built from the store's block equal those
    built from the compact's (a coincident group must not become two edges, rev 5)."""
    a, b = curve_kinds(edges, ts), curve_kinds(boundaries, ts)
    if a != b:
        diff = sorted(set(a) ^ set(b))[:3]
        raise StoreRefusal("material.d2_store_coincident", f"record {rid}: curve kinds differ from the compact's, e.g. {diff}")


def check_extension_h6(edges, compact, rid="?"):
    """H6 on the store block's certified extension rows (note 2 (1); the store side of §5b (2c)): the table loader's
    own per-row check, material_assemblage.check_extension_row, so H6 has one code (note 3 (5)); its TableStop
    becomes this registration's refusal."""
    ps, _ts = nodes(compact)
    nxt = dict(zip(ps, ps[1:]))
    by = {(c["p"], c["t"]): c for c in compact["cells"]}
    for i, r in enumerate((edges.get("extension") or {}).get("rows", ())):
        if not r.get("certified"):
            continue
        where = f"record {rid}: certified extension row {i} ({r.get('t')!r} K)"
        try:
            ma.check_extension_row(r, where, by, nxt)
        except ma.TableStop as e:
            raise StoreRefusal("material.d2_store_edges_rows", f"{e} (H6)") from None


# ── §5b (2b) and (S1): the «today» segments of the view built on the store's block ─────────────────────────────────
def _unit_sources(edges):
    """{(t, p_lo, p_hi, left label, right label, phase or None): p_b_source} for every unit."""
    out = {}
    for r in edges.get("rows", ()):
        key = (r["t"], r["p_lo"], r["p_hi"], r["left"], r["right"])
        if r.get("node_resolved") or r.get("class") == "swap":
            out[key + (None,)] = r.get("p_b_source")
        if not r.get("node_resolved") and r.get("class") != "swap":
            for e in r.get("edges") or ():
                out[key + (e["phase"],)] = e.get("p_b_source")
    for r in (edges.get("extension") or {}).get("rows", ()):
        if not r.get("certified"):               # only certified extension rows are curve rows (curve_groups; the
            continue                             # writer's d2_store_checks.sources): uncertified ones carry no p_lo/p_hi
        out[(r["t"], r["p_lo"], r["p_hi"], r["left"], r["right"], None)] = r.get("p_b_source")
    return out


def _is_today(src, curve, row):
    # curve_groups' key: an edge group carries its edge's phase (kept when init merges it into a swap); a swap or node
    # group carries None, read at row level
    got = src.get((row["t"], row["p_lo"], row["p_hi"], row["left_label"], row["right_label"], curve.phase))
    if got is None:
        raise StoreRefusal("material.d2_store_edges_rows", f"curve {curve.id} row at {row['t']!r} K has no unit in the block")
    return got == "today"


def _holder(view, row, hi):
    """The run of the initialised view's `_events` (init's merged cut runs and the runs read across) whose own end is
    `row` (a lower end if not `hi`): it carries that end's stop and kind after init. Runs share the curve's row dicts,
    so the match is by identity."""
    for r in view._events:
        if (r.rows[-1] if hi else r.rows[0]) is row:
            return r
    raise StoreRefusal("material.d2_store_edges_rows", f"no event run ends at the curve row of {row['t']!r} K")


def _pieces(view, curve, ts, rch):
    """(a, b, end indices, where): the straight pieces of one full curve of the view (`_curves`: rev 7 §5b (2b) «every
    curve … on every T interval of its domain»; 68 B1 on 039c875b) — between its consecutive rows, whether a row pair
    is cut or read across, and past each of its two true ends that does not stop, to `rch`, broken at the table's T
    rows. Each end's stop and extension are those of the event run holding it (`_holder`): there init's coincident
    merge and reach-0 stops live, and at a true end no run has the interior-end flat stub (note 8 (b′)). a, b are
    (T, P_b)."""
    rows = curve.rows
    for i in range(len(rows) - 1):
        yield (rows[i]["t"], rows[i]["p_b"]), (rows[i + 1]["t"], rows[i + 1]["p_b"]), (i, i + 1), "rows"
    if not rch:
        return
    for hi in (False, True):
        h = _holder(view, rows[-1] if hi else rows[0], hi)
        if h.stop_hi if hi else h.stop_lo:
            continue
        t_end = rows[-1]["t"] if hi else rows[0]["t"]
        far = t_end + rch if hi else t_end - rch
        mid = [t for t in ts if (t_end < t < far if hi else far < t < t_end)]
        knots = [t_end] + (mid if hi else mid[::-1]) + [far]
        knots = [t for t in knots if ts[0] <= t <= ts[-1]]
        end_i = len(rows) - 1 if hi else 0
        prev = None
        for t in knots:
            p = h.p_b_ext(t, rch)
            if p is None:
                break
            if prev is not None:
                yield prev, (t, p), (end_i,), "extension " + ("hi" if hi else "lo")
            prev = (t, p)


def _cells_through(ps, ts, a, b):
    """Every cell (j, k) the straight piece a–b passes through: one T cell (the piece lies between adjacent T rows),
    every P cell from the lower P_b's to the higher's; a P_b exactly on a column line belongs to both cells."""
    (ta, pa), (tb, pb) = (a, b) if a[0] <= b[0] else (b, a)
    k = max(0, min(bisect.bisect_right(ts, ta) - 1, len(ts) - 2))
    if tb > ts[k + 1]:
        raise ValueError(f"a piece spans more than one T cell: {ta}–{tb}")
    lo, hi = min(pa, pb), max(pa, pb)
    j0 = bisect.bisect_right(ps, lo) - 1
    if j0 >= 0 and ps[j0] == lo:
        j0 -= 1                                      # on a column line: the cell below too
    j1 = bisect.bisect_left(ps, hi)                 # the first node ≥ hi; cells up to j1 − 1, and j1 if hi is on it
    if j1 < len(ps) and ps[j1] == hi:
        j1 += 1
    return [(j, k) for j in range(max(j0, 0), min(j1, len(ps) - 1))]


def _sliver(cell, ps, ts, j, k, w):
    """(lower, upper) of [L_A(w), L_B(w)] as fractions of the cell along its direction: the two sides sorted by their
    lowest node, side 1 reversed when its A is not side 0's (rev 7 §5, note 19)."""
    s0, s1 = sorted(cell["sides"], key=lambda s: min(tuple(n) for n in s["nodes"]))
    axis = 0 if cell["direction"] == "P" else 1
    lo, hi = (ps[j], ps[j + 1]) if axis == 0 else (ts[k], ts[k + 1])
    frac = lambda pt: (pt[axis] - lo) / (hi - lo)      # noqa: E731
    a1, b1 = (s1["lines"][1], s1["lines"][0]) if s1["A"] != s0["A"] else (s1["lines"][0], s1["lines"][1])
    la = (1.0 - w) * frac(s0["lines"][0]) + w * frac(a1)
    lb = (1.0 - w) * frac(s0["lines"][1]) + w * frac(b1)
    return min(la, lb), max(la, lb)


def _sliver_miss(cell, ps, ts, j, k, a, b):
    """→ (worst miss beyond the tolerance or None, [(w, signed offset inside)])."""
    (ta, pa), (tb, pb) = (a, b) if a[0] <= b[0] else (b, a)
    offs, worst = [], None
    for w in S1_WS:
        if cell["direction"] == "P":
            t = ts[k] + w * (ts[k + 1] - ts[k])
            if tb == ta or not ta <= t <= tb:
                continue
            x = pa + (pb - pa) * (t - ta) / (tb - ta)
            u, span, tol = (x - ps[j]) / (ps[j + 1] - ps[j]), ps[j + 1] - ps[j], P_TOL
        else:
            p = ps[j] + w * (ps[j + 1] - ps[j])
            if pb == pa or not min(pa, pb) <= p <= max(pa, pb):
                continue
            t = ta + (tb - ta) * (p - pa) / (pb - pa)
            u, span = (t - ts[k]) / (ts[k + 1] - ts[k]), ts[k + 1] - ts[k]
            tol = P_TOL * (tb - ta) / abs(pb - pa)          # P_TOL taken through the segment's slope, in K
        lo, hi = _sliver(cell, ps, ts, j, k, w)
        inside = min(u - lo, hi - u) * span
        offs.append((w, inside))
        if -inside > tol and (worst is None or -inside > worst[1]):
            worst = (w, -inside, tol)
    return worst, offs


def today_segments(store_doc, view):
    """§5b (2b) and (S1) on the view built on the store's block: every full curve (`_curves`) row to row, and past its
    true ends with the stops and extensions of the event runs holding them (`_events`, after init's merge). → {"stops": [(id, text)], "s1": [...]}; the stops are d2_store_today_row (a «today» segment through
    a d2 or cut cell) and d2_store_sliver (outside a kept subgrid cell's sliver by more than P_TOL)."""
    ps, ts = store_doc["grid"]["ps"], store_doc["grid"]["ts"]
    if list(view.ts) != list(ts):
        return {"stops": [("material.d2_store_grid", "the view's T rows are not the store's")], "s1": []}
    src, cells = _unit_sources(store_doc["edges"]), store_doc["cells"]
    rch = view._reach
    stops, s1, seen = [], [], set()
    for c in view._curves:
        today = [_is_today(src, c, r) for r in c.rows]
        for a, b, ends, where in _pieces(view, c, ts, rch):
            if not any(today[i] for i in ends):
                continue
            for j, k in _cells_through(ps, ts, a, b):
                cell = cells.get(f"{j},{k}")
                if cell is None:
                    continue
                name = f"curve {c.id} ({c.kind}{'' if c.phase is None else ' ' + c.phase}) {where} {a[0]:g}–{b[0]:g} K, cell ({j}, {k})"
                if cell["class"] in ("d2", "cut"):
                    if (c.id, a, b, j, k) not in seen:
                        seen.add((c.id, a, b, j, k))
                        stops.append(("material.d2_store_today_row", f"«today» segment through a {cell['class']} cell: {name}"))
                elif cell["class"] == "subgrid":
                    worst, offs = _sliver_miss(cell, ps, ts, j, k, a, b)
                    s1.append({"curve": c.id, "cell": [j, k], "where": where, "offsets": offs})
                    if worst:
                        stops.append(("material.d2_store_sliver", f"outside the sliver by {worst[1]:.6g} "
                                      f"{'Pa' if cell['direction'] == 'P' else 'K'} > {worst[2]:.6g} at w {worst[0]}: {name}"))
    return {"stops": stops, "s1": s1}


def check_edges(loaded, compact, record_doc):
    """All of §5b's load checks on a loaded store, in order; raises the first StoreRefusal."""
    rid, doc = record_doc.get("id"), loaded.doc
    b = ma.boundary_block(None, compact, None, "read") or {}      # the compact's block (§5b load checks)
    ps, ts = nodes(compact)
    check_edges_rows(doc["edges"], b, rid)
    check_units(doc["edges"], b, rid)
    check_extension_h6(doc["edges"], compact, rid)
    check_coincident(doc["edges"], b, ts, rid)
    v = ma.view(record_doc, {**compact, "boundaries": doc["edges"]}, 1600.0)
    got = today_segments(doc, v)
    if got["stops"]:
        rid0, text = got["stops"][0]
        raise StoreRefusal(rid0, f"record {rid}: {text} ({len(got['stops'])} in all)")
    return got


def read_point(doc, p, t, view=None):
    """The engine's read at one point of a D2-routed record (D2-read §5): a port of the reference reader's `read`
    (d2_store_reader, note 17 §4.1), floating-point order kept expression for expression so §9 item 1's `==` holds.

        read_point(doc, p, t, view=None) → {"read": "table", "why": str, "notes": ()}
                                          | {"read": "d2" | "cut", "field": str, "values": {rho, s, c_p, dtdp}, "notes": …}
                                          | {"read": "subgrid", "field": str, "values": {rho, c_p, alpha, s, dtdp}, "notes": …}

    `doc` is the store document, `p` in Pa, `t` in K. Value keys per class: d2 and cut give VALUE_KEYS; subgrid gives
    SUBGRID_VALUE_KEYS (alpha too, as the reference does). A «table» answer names why; the view then reads its table
    as with d2_read off. Cells by the lower-cell rule on both axes (§5's registered tie). `notes` are the engine's own
    (code, text) pairs (Q9); the comparison leaves them out. `view`, when given, takes the «no field» count (§6)."""
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    j, k = _lower_cell(ps, p), _lower_cell(ts, t)
    if j is None or k is None:
        return {"read": "table", "why": "outside the store's grid", "notes": ()}
    cell = doc["cells"].get(f"{j},{k}")
    if cell is None:
        return {"read": "table", "why": "no entry (frozen corner or above p_dataset)", "notes": ()}
    box = (ps[j], ps[j + 1], ts[k], ts[k + 1])
    u, v = (p - box[0]) / (box[1] - box[0]), (t - box[2]) / (box[3] - box[2])
    cls = cell["class"]
    if cls in ("fallback", "limit"):
        return {"read": "table", "why": cls, "notes": ()}
    if cls in ("d2", "cut"):
        got = _surface(doc, cell, j, k, u, v, box, p, t)
        if got is None:
            if view is not None and hasattr(view, "d2_counts"):
                view.d2_counts[NO_FIELD] = view.d2_counts.get(NO_FIELD, 0) + 1
            return {"read": "table", "why": NO_FIELD, "notes": ()}
        f, cs = got
        return {"read": cls, "field": f, "values": _g_values(cs, box, p, t),
                "notes": ((cls, D2_NOTE if cls == "d2" else CUT_NOTE),)}
    # subgrid (note 17 §2.5 as note 19 amends it): u along the sides, w across; lines linear in w; inside the sliver
    # the w-blend of the two sides' Lagrange quadratics; outside it the table
    s0, s1 = sorted(cell["sides"], key=lambda sd: min(map(tuple, sd["nodes"])))
    uu, w = (u, v) if cell["direction"] == "P" else (v, u)
    lo, hi = (box[0], box[1]) if cell["direction"] == "P" else (box[2], box[3])
    pos = lambda pt: ((pt[0] if cell["direction"] == "P" else pt[1]) - lo) / (hi - lo)  # noqa: E731
    rev = s1["A"] != s0["A"]
    ua = [pos(s0["lines"][0]), pos(s1["lines"][1] if rev else s1["lines"][0])]
    ub = [pos(s0["lines"][1]), pos(s1["lines"][0] if rev else s1["lines"][1])]
    k0 = s0["knots"]
    k1 = {"A": s1["knots"]["B"], "C": s1["knots"]["C"], "B": s1["knots"]["A"]} if rev else s1["knots"]
    la, lb = (1 - w) * ua[0] + w * ua[1], (1 - w) * ub[0] + w * ub[1]
    if not (min(la, lb) <= uu <= max(la, lb)):
        return {"read": "table", "why": "subgrid cell outside the sliver", "notes": ()}
    sfr = (uu - la) / (lb - la)
    if view is not None and hasattr(view, "d2_counts"):               # §6: (S1)'s per-read count
        view.d2_counts["d2: (S1) read inside a subgrid sliver"] = view.d2_counts.get("d2: (S1) read inside a subgrid sliver", 0) + 1
    vals = {n: (1 - w) * _lagrange(k0, sfr, n) + w * _lagrange(k1, sfr, n) for n in ("rho", "c_p", "alpha", "s")}
    vals["dtdp"] = t * vals["alpha"] / (vals["rho"] * vals["c_p"])        # T·α/(ρ·c_P), never differentiated
    return {"read": "subgrid", "field": s0["C"], "values": vals, "notes": (("subgrid", SUBGRID_NOTE),)}


def _surface(doc, cell, j, k, u, v, box, p, t):
    """(field, corners) of a d2 or cut cell at (u, v), or None for a d2 cell with no field left (§5, the reference's
    order): d2 — among `surfaces` with every bilinear mode ≥ 0, the lowest solved G; cut — the cross product's side,
    A's nodes with A's virtual nodes at B's corners on A's side, B's own nodes on B's."""
    if cell["class"] == "d2":
        ok = {}
        for f in cell["surfaces"]:
            cs = _corners(doc, f, j, k)
            if _lowest_mode(cs, u, v) >= 0.0:
                ok[f] = cs
        if not ok:
            return None
        f = min(ok, key=lambda x: _hermite_g(ok[x], *box, p, t, 0, 0, "solved"))
        return f, ok[f]
    c = cell["cut"]
    (x1, y1), (x2, y2) = c["points"]
    cross = lambda uu, vv: (x2 - x1) * (vv - y1) - (y2 - y1) * (uu - x1)  # noqa: E731
    a0 = c["a_corners"][0]
    if cross(u, v) * math.copysign(1.0, cross(*a0)) > 0:
        f = c["a"]
        nodes = doc["fields"][f]["nodes"]
        return f, [_corner(c["a_virtual"].get(f"{j + i},{k + l}") or nodes[f"{j + i},{k + l}"]) for i, l in CORNERS]
    return c["b"], _corners(doc, c["b"], j, k)


def s_parts(doc, p, t, forced=None):
    """The s read's parts at (p, t) through the same dispatch (Q6, Q8), or None where the table's s_path applies:
    ("surface", s, G_PT, G_TT) on d2 and cut (consistent-G form (ii)); ("sliver", s, rho, alpha, c_p) inside a subgrid
    sliver (the read's own blend, Q8). The view builds Dual(s, −P·G_PT, −G_TT) or Dual(s, −P·α/ρ, c_P/T) from them.
    `forced` (§5b (5), note 7): a cut cell reads the forced side's surface; (iii)'s cases give None (today's forced
    table s path). Nothing is counted here (the view counts, s_path)."""
    r = read_forced(doc, p, t, forced) if forced else read_point(doc, p, t)
    if r["read"] == "table":
        return None
    if r["read"] == "subgrid":
        v = r["values"]
        return ("sliver", v["s"], v["rho"], v["alpha"], v["c_p"])
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    j, k = _lower_cell(ps, p), _lower_cell(ts, t)
    box = (ps[j], ps[j + 1], ts[k], ts[k + 1])
    u, v = (p - box[0]) / (box[1] - box[0]), (t - box[2]) / (box[3] - box[2])
    fs = forced_side(doc, p, t, forced) if forced else None
    if fs is not None:
        _f, cs = _cut_corners(doc, doc["cells"][f"{j},{k}"], j, k, fs[0])
    else:
        _f, cs = _surface(doc, doc["cells"][f"{j},{k}"], j, k, u, v, box, p, t)
    return ("surface", -_hermite_g(cs, *box, p, t, 0, 1, "cons"), _hermite_g(cs, *box, p, t, 1, 1, "cons"),
            _hermite_g(cs, *box, p, t, 0, 2, "cons"))




FORCED = "d2: forced side on a cut cell"
#: note 7 (§5b (5) (iii)): a forced read on a cut cell with no forced curve in the cell, two or more, or a cut line
#: with no P side, reads today's forced table read, counted here (and in FORCED), never refused
FORCED_TABLE = "d2: forced side on a cut cell → table read"


def forced_side(doc, p, t, forced):
    """§5b (5) with D2-read note 7 (ii)/(iii): the side a force picks on the cut cell at (p, t). `forced` is
    [(P_b(t), side)] of the force's curves on the position set, side −1 (P below P_b) or +1. None when (p, t) is not
    on a cut cell (the force does not change a d2, subgrid or table answer); else ("A" | "B", None), or
    (None, why) for (iii)'s cases. The forced curve is the one whose P_b lies in the cell's P span by the lower-cell
    tie (a P_b on the cell's upper P node is in the cell, on its lower node in the cell below); −1 / +1 name the
    field on the low / high P side of the cut line, by the sign of ∂cross/∂u = −(y2 − y1) against A's first corner."""
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    j, k = _lower_cell(ps, p), _lower_cell(ts, t)
    if j is None or k is None:
        return None
    cell = doc["cells"].get(f"{j},{k}")
    if cell is None or cell["class"] != "cut":
        return None
    mine = [sd for pb, sd in forced if pb is not None and sd in (-1, 1) and _lower_cell(ps, pb) == j]
    if len(mine) != 1:
        return None, ("no forced curve in the cell" if not mine else "two or more forced curves in the cell")
    c = cell["cut"]
    (x1, y1), (x2, y2) = c["points"]
    if y1 == y2:
        return None, "the cut line has no P side"
    a0 = c["a_corners"][0]
    a_sign = math.copysign(1.0, (x2 - x1) * (a0[1] - y1) - (y2 - y1) * (a0[0] - x1))
    low = "A" if math.copysign(1.0, y2 - y1) == a_sign else "B"       # u → −∞: cross → sign(y2 − y1)·∞
    return (low if mine[0] == -1 else ("B" if low == "A" else "A")), None


def _cut_corners(doc, cell, j, k, which):
    """§5b (5): A — A's virtual-corner surface over the whole cell; B — B's four-corner surface."""
    c = cell["cut"]
    if which == "A":
        nodes = doc["fields"][c["a"]]["nodes"]
        return c["a"], [_corner(c["a_virtual"].get(f"{j + i},{k + l}") or nodes[f"{j + i},{k + l}"]) for i, l in CORNERS]
    return c["b"], _corners(doc, c["b"], j, k)


def read_forced(doc, p, t, forced, view=None):
    """read_point under a force (§5b (5), note 7): off a cut cell the unforced read; on a cut cell the forced side's
    surface, or a «table» answer for (iii)'s cases (the view then reads today's forced table read). `view` takes the
    counts: FORCED per forced read on a cut cell, FORCED_TABLE for (iii)."""
    fs = forced_side(doc, p, t, forced)
    if fs is None:
        return read_point(doc, p, t, view)
    which, why = fs
    if view is not None and hasattr(view, "d2_counts"):
        view.d2_counts[FORCED] = view.d2_counts.get(FORCED, 0) + 1
        if which is None:
            view.d2_counts[FORCED_TABLE] = view.d2_counts.get(FORCED_TABLE, 0) + 1
    if which is None:
        return {"read": "table", "why": f"forced side: {why}", "notes": ()}
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    j, k = _lower_cell(ps, p), _lower_cell(ts, t)
    box = (ps[j], ps[j + 1], ts[k], ts[k + 1])
    f, cs = _cut_corners(doc, doc["cells"][f"{j},{k}"], j, k, which)
    return {"read": "cut", "field": f, "values": _g_values(cs, box, p, t), "notes": (("cut", CUT_NOTE),)}


def class_at(doc, p, t):
    """The store's class at (p, t) by the dispatch's lower-cell tie, or None (outside the grid, no entry)."""
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    j, k = _lower_cell(ps, p), _lower_cell(ts, t)
    if j is None or k is None:
        return None
    return (doc["cells"].get(f"{j},{k}") or {}).get("class")

def s_slopes(doc, p, t, forced=None):
    """(s, ∂s/∂lnP, ∂s/∂T) at (p, t) through the dispatch, load-free, or None where the table's s path applies: the
    numbers the view's s_path puts in its Dual (Q6: −P·G_PT, −G_TT; Q8: −P·α/ρ, c_P/T)."""
    sp = s_parts(doc, p, t, forced)
    if sp is None:
        return None
    if sp[0] == "surface":
        return sp[1], -p * sp[2], -sp[3]
    _k, s_, rho, alpha, cp = sp
    return s_, -p * alpha / rho, cp / t

# ── the port's arithmetic (the reference reader's, in its order) ─────────────────────────────────────────────────────
CORNERS = ((0, 0), (1, 0), (0, 1), (1, 1))
D2_NOTE = "D2 read (s3-d2 §4): the field's own surface, gated by s3-d2 §7, not the table's band"
CUT_NOTE = "D2 cut read (note 17 §2.4): the side's own field, gated by s3-d2 §7, not the table's band"
SUBGRID_NOTE = "D2 subgrid read (note 17 §2.5): the sliver blend, checkpoints against band/10, not the table's band"


def _lower_cell(xs, x):
    """The lower cell at a node (§5's registered tie): the first i with xs[i] ≤ x ≤ xs[i + 1], else None."""
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            return i
    return None


def _hermite_basis(u, d):
    if d == 0:
        return (2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2, u**3 - u**2)
    if d == 1:
        return (6 * u**2 - 6 * u, 3 * u**2 - 4 * u + 1, -6 * u**2 + 6 * u, 3 * u**2 - 2 * u)
    return (12 * u - 6, 6 * u - 4, -12 * u + 6, 6 * u - 2)


def _hermite_g(cs, p0, p1, t0, t1, p, t, dp, dt, which):
    """Form (ii) (s3-d2 §2.4): bicubic Hermite on G with V, −S and ∂V/∂T at the four corners, CORNERS order."""
    hp, ht = p1 - p0, t1 - t0
    bu, bv = _hermite_basis((p - p0) / hp, dp), _hermite_basis((t - t0) / ht, dt)
    tot = 0.0
    for (i, l), c in zip(CORNERS, cs):
        f = c["g_cons"] if which == "cons" else c["g"]
        a0, a1, b0, b1 = bu[2 * i], bu[2 * i + 1], bv[2 * l], bv[2 * l + 1]
        tot += f * a0 * b0 + c["v"] * hp * a1 * b0 + (-c["s"]) * ht * a0 * b1 + c["w"] * hp * ht * a1 * b1
    return tot / (hp ** dp * ht ** dt)


def _lowest_mode(cs, u, v):
    w = ((1 - u) * (1 - v), u * (1 - v), (1 - u) * v, u * v)
    return min(sum(wi * c["amounts"][q] for wi, c in zip(w, cs)) for q in range(len(cs[0]["amounts"])))


def _g_values(cs, box, p, t):
    gp, gt = _hermite_g(cs, *box, p, t, 1, 0, "cons"), _hermite_g(cs, *box, p, t, 0, 1, "cons")
    gpp, gtt, gpt = (_hermite_g(cs, *box, p, t, 2, 0, "cons"), _hermite_g(cs, *box, p, t, 0, 2, "cons"),
                     _hermite_g(cs, *box, p, t, 1, 1, "cons"))
    return {"rho": 1.0 / gp, "s": -gt, "c_p": -t * gtt, "dtdp": -gpt / gtt if gtt else math.nan}


def _corner(n):
    return {"g": n["g_solved"], "g_cons": n["g_consistent"], "v": n["v"], "s": n["s"], "w": n["dv_dt_eq"],
            "amounts": n["amounts"]}


def _corners(doc, field, j, k):
    nodes = doc["fields"][field]["nodes"]
    return [_corner(nodes[f"{j + i},{k + l}"]) for i, l in CORNERS]


def _lagrange(kn, x, name):
    a, m, b = kn["A"][name], kn["C"][name], kn["B"][name]
    return 2 * (x - 0.5) * (x - 1) * a - 4 * x * (x - 1) * m + 2 * x * (x - 0.5) * b   # Lagrange, as note 15 §2
