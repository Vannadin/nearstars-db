# D2 «추가된 곡선» 재계수(D2-read §5b (6), 지도 행 c8-16) — 저장 파일 edges 블록의 edge 행과 PC-D edges.json 의 P 방향 추적점을 대어, 어떤 행에도 쓰이지 않은 점(accepted·unmatched 따로)을 zone_added.py 의 규칙대로 세고 예측 상한과 나란히 적음
"""python3 -B -m solver.landing.d2_added_recount --out OUT.json RECORD=STORE.json.gz,EDGES.json [RECORD=… …]

D2-read rev 7 §5b (6), «“Added” curves, disclosed (n5)»: traced P-direction points in D2's region that no row uses. «It
is recounted at L on PC-D's file.» Part 2's row c8-16; the definition is c8's, and its counting rule is the forecast
tool's, rewrite/family/s3/migration/d2-engine-read/q7-forecast/zone_added.py (blob 3a879084), kept here:
- points: accepted = P-direction edges with `accepted` and a p, with phases {x, x_base} on `line.t`; unmatched =
  P-direction unmatched points, with phases the base names (trailing digits dropped) of a_parts △ b_parts, on `t`;
- a point is used when an edge row at the same T, whose P_b lies in a column [ps[j], ps[j+1]] at or below p_dataset,
  carries a phase of the point inside that column;
- added = points at or below p_dataset used by no row, accepted and unmatched counted apart.
What differs from the forecast, by part 2's inputs (c8 11-16):
- the rows are the part-2 store's `edges` block, not the stand-in curves.json: the edge rows are classes edge_in and
  edge_out (swap and swap_two_edges are swaps, as the forecast's kind «edge» excluded them); each of a row's edges is
  taken with its own phase and P_b (the forecast's curves had one phase per curve); an edge that carries no P_b of its
  own (a node-resolved row whose edge did not converge) takes the row's;
- p_dataset is the store header's and the columns are the store grid's.
A second count is printed beside it, not judged: the points named by a row edge's own `match.record` (the writer's
record of which point it took). Points the rule counts as used but no match names, and the reverse, are listed.
OUT holds per record the counts, the forecast's upper bound, both inputs' sha256 and git blob, and the cross-check. rc 2 on a bad
input; the counts are a disclosure, so no count STOPs."""
import argparse
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path
from types import MappingProxyType

EDGE_ROWS = ("edge_in", "edge_out")
FORECAST = MappingProxyType({                                       # D2-read §5b (6), stand-ins (khan / bse / dmm);
    r: MappingProxyType(v) for r, v in (                                # read-only all the way down (A6 guard 1)
        ("mars_khan2022", {"accepted": 22, "unmatched": 560}), ("default_bse", {"accepted": 20, "unmatched": 501}),
        ("earth_dmm_wh2005", {"accepted": 12, "unmatched": 504}))})


def base(x):
    return re.sub(r"\d+$", "", x)


def points(edges):
    acc = [("accepted", i, e["line"]["t"], e["p"], frozenset({e["x"], e.get("x_base")}))
           for i, e in enumerate(edges["edges"]) if e["direction"] == "P" and e["accepted"] and e.get("p") is not None]
    um = [("unmatched", i, u["t"], u["p"], frozenset(base(x) for x in set(u["a_parts"]) ^ set(u["b_parts"])))
          for i, u in enumerate(edges["unmatched"]) if u["direction"] == "P"]
    return acc + um


def row_edges(doc):
    """(t, p_b, phase, match) for every edge of every edge row of the store's block"""
    for r in doc["edges"]["rows"]:
        if r["class"] in EDGE_ROWS:
            for e in r.get("edges") or []:
                yield r["t"], e.get("p_b", r.get("p_b")), e["phase"], e.get("match") or {}


def recount(doc, edges):
    ps, pd = doc["grid"]["ps"], doc["header"]["p_dataset"]
    pts = points(edges)
    by_t = {}
    for x in pts:
        by_t.setdefault(x[2], []).append(x)
    used = set()
    for t, pb, phase, _ in row_edges(doc):
        if pb is None or pb > pd:
            continue
        j = next((q for q in range(len(ps) - 1) if ps[q] <= pb <= ps[q + 1]), None)
        if j is None:
            continue
        used |= {(x[0], x[1]) for x in by_t.get(t, ()) if ps[j] <= x[3] <= ps[j + 1] and phase in x[4]}
    region = [x for x in pts if x[3] <= pd]
    left = {"accepted": 0, "unmatched": 0}
    for x in region:
        if (x[0], x[1]) not in used:
            left[x[0]] += 1
    named = {(m["record"]["list"].replace("edges", "accepted"), m["record"]["index"]) for _, _, _, m in row_edges(doc)
             if m.get("kind") in ("accepted", "unmatched") and m.get("record")}
    in_region = {(x[0], x[1]) for x in region}
    return {"points_in_region": {k: sum(1 for x in region if x[0] == k) for k in ("accepted", "unmatched")},
            "added": left,
            "cross_check_by_match_record": {
                "named_by_a_row": len(named & in_region),
                "used_by_the_rule_but_named_by_no_row": len((used & in_region) - named),
                "named_by_a_row_but_not_used_by_the_rule": sorted(map(list, (named & in_region) - used))[:20]}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("records", nargs="+", help="RECORD=STORE.json.gz,EDGES.json")
    a = ap.parse_args(argv)
    res = {"tool": "d2_added_recount", "rule": "zone_added.py 3a879084, on the store's edge rows", "records": {}}
    for arg in a.records:
        try:
            rid, paths = arg.split("=", 1)
            sp, ep = paths.split(",")
            raw, eraw = Path(sp).read_bytes(), Path(ep).read_bytes()
            doc, edges = json.loads(gzip.decompress(raw)), json.loads(eraw)
            r = recount(doc, edges)
        except Exception as e:
            print(f"STOP: {arg}: {type(e).__name__}: {e}")
            return 2
        blob = lambda b: hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()      # noqa: E731 (rows cite git blobs)
        r.update(store_sha256=hashlib.sha256(raw).hexdigest(), edges_sha256=hashlib.sha256(eraw).hexdigest(),
                 store_git_blob=blob(raw), edges_git_blob=blob(eraw),
                 forecast_upper_bound=dict(FORECAST[rid]) if rid in FORECAST else None)
        res["records"][rid] = r
        f = FORECAST.get(rid) or {}
        print(f"{rid}: added accepted {r['added']['accepted']} (forecast ≤ {f.get('accepted')}), unmatched "
              f"{r['added']['unmatched']} (forecast ≤ {f.get('unmatched')}); in region {r['points_in_region']}")
    Path(a.out).write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
