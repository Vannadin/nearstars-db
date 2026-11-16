# 엔진 D2 읽기와 기준 읽기기 대조 — 저장 파일마다 모집단 칸의 네 꼭짓점·가운데(c8-14)와 §9 항목 1 의 점들(부류별 씨앗 점·마디 ±1 ulp·136 GPa)에서 두 답을 키별로, 값은 비트로 견줌; 하나라도 다르면 STOP
"""python3 -B -m solver.landing.d2_read_compare --reference READER.py --out OUT.json [--item1] [--seed N] [--per-cell K]
                                                 STORE.json.gz [STORE.json.gz ...]

D2-read rev 7 §9: «Engine read = reference reader, `==` bit for bit», class by class and value by value.
- Points. Always every population cell's four corners and its centre (§9's deferred item, map row c8-14). With --item1,
  also §9 item 1's: K seeded interior points per population cell, every grid node of a population cell and the points
  1 ulp either side of it on each axis (§5's ties), and P = 136e9 where the grid spans it (Q3).
- Both readers get the store as the reference reader's `load` returns it; the engine gets its own deep copy.
- An answer pair agrees when (c8 11-16, the S0 interface):
  - «read» is equal;
  - a table answer's «why» is equal; a D2 answer's «field» is equal, and «values» has the same keys, each value equal
    bit for bit (IEEE-754 binary64 packing, so a NaN equals only a NaN with the same bits, and 0.0 is not -0.0);
  - no other key, except the engine's «notes», which the reference does not carry and which is not compared.
- An engine exception at a point is a difference, by its type and message (NotImplementedError until S2).
- With --item1 the stores together must reach every case in ITEM1_CASES (each class, each table «why», the 136e9 node,
  a non-integer T grid), or the run STOPs naming the missing ones: a case that never runs is not a pass.
OUT holds per store: the store's sha256, the counts of points and of answers by «read», the number of differences and
the first 50. rc 0 when every store agrees, rc 2 otherwise or on a bad input."""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
import math
import random
import struct
import sys
from pathlib import Path

#: §9 item 1's registered cases (68 B1 on 270edf72): with --item1 the run STOPs, naming them, unless the stores together
#: give the reference answer of every class (the table answers by their «why»), read the 136e9 node, and include a grid
#: whose T steps are not whole numbers
ITEM1_CASES = ("read d2", "read cut", "cut both sides", "read subgrid", "why fallback", "why limit",
               "why no entry (frozen corner or above p_dataset)", "why d2: no field at the point → table read",
               "why subgrid cell outside the sliver", "point p136", "grid non-integer T step")
#: cases a case list cannot see in the answers, so the fixtures' manifest must name them (68 n1): A's virtual corners on a
#: cut cell, and a subgrid cell whose side 1 is reversed
ITEM1_STORES = ("cut_a_virtual", "subgrid_reversed")
NOT_COMPARED = ("notes",)                     # the engine's own (code, text) pairs; the reference has none
P_TIE = 136e9                                 # Q3: the taper's match at p_dataset is a column node


def load_reference(path):
    spec = importlib.util.spec_from_file_location("d2_store_reader_ref", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bits(x):
    return struct.pack("<d", x)


def same_value(a, b):
    if isinstance(a, float) and isinstance(b, float):
        return bits(a) == bits(b)
    return type(a) is type(b) and a == b


def diff(ref, eng):
    """the reasons the two answers disagree, empty when they agree"""
    out = []
    rk = set(ref)
    ek = set(eng) - set(NOT_COMPARED)
    if rk != ek:
        out.append(f"keys: reference {sorted(rk)}, engine {sorted(ek)}")
    if ref.get("read") != eng.get("read"):
        out.append(f"read: reference {ref.get('read')!r}, engine {eng.get('read')!r}")
        return out
    if ref.get("read") == "table":
        if ref.get("why") != eng.get("why"):
            out.append(f"why: reference {ref.get('why')!r}, engine {eng.get('why')!r}")
        return out
    if ref.get("field") != eng.get("field"):
        out.append(f"field: reference {ref.get('field')!r}, engine {eng.get('field')!r}")
    rv, ev = ref.get("values") or {}, eng.get("values") or {}
    if set(rv) != set(ev):
        out.append(f"value keys: reference {sorted(rv)}, engine {sorted(ev)}")
    for q in sorted(set(rv) & set(ev)):
        if not same_value(rv[q], ev[q]):
            out.append(f"values.{q}: reference {rv[q]!r}, engine {ev[q]!r}")
    return out


def cell_points(doc):
    """every population cell's corners and centre, in cell order: (cell, label, p, t)"""
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    for key in sorted(doc["cells"], key=lambda s: tuple(map(int, s.split(",")))):
        j, k = map(int, key.split(","))
        for lab, (i, l) in (("c00", (0, 0)), ("c10", (1, 0)), ("c01", (0, 1)), ("c11", (1, 1))):
            yield key, lab, ps[j + i], ts[k + l]
        yield key, "centre", 0.5 * (ps[j] + ps[j + 1]), 0.5 * (ts[k] + ts[k + 1])


def item1_points(doc, seed, per_cell):
    """§9 item 1: seeded interior points per population cell; every node of a population cell, and ±1 ulp on each
    axis; P = 136e9 at each population cell's T centre where the grid spans it"""
    ps, ts = doc["grid"]["ps"], doc["grid"]["ts"]
    rng = random.Random(seed)
    keys = sorted(doc["cells"], key=lambda s: tuple(map(int, s.split(","))))
    nodes = set()
    for key in keys:
        j, k = map(int, key.split(","))
        for _ in range(per_cell):
            yield key, "seeded", ps[j] + rng.random() * (ps[j + 1] - ps[j]), ts[k] + rng.random() * (ts[k + 1] - ts[k])
        nodes.update((j + i, k + l) for i in (0, 1) for l in (0, 1))
    for (a, b) in sorted(nodes):
        p, t = ps[a], ts[b]
        yield f"node {a},{b}", "node", p, t
        for lab, pp, tt in (("p-ulp", math.nextafter(p, -math.inf), t), ("p+ulp", math.nextafter(p, math.inf), t),
                            ("t-ulp", p, math.nextafter(t, -math.inf)), ("t+ulp", p, math.nextafter(t, math.inf))):
            yield f"node {a},{b}", lab, pp, tt
    if ps[0] <= P_TIE <= ps[-1]:
        for key in keys:
            k = int(key.split(",")[1])
            yield key, "p136", P_TIE, 0.5 * (ts[k] + ts[k + 1])


def compare_store(raw, ref_mod, engine_read, item1=False, seed=0, per_cell=4):
    doc = ref_mod.load(raw)
    edoc = copy.deepcopy(doc)
    pts = list(cell_points(doc))
    if item1:
        pts += list(item1_points(doc, seed, per_cell))
    by_read, diffs, cover, cut_fields = {}, [], set(), {}
    ts = doc["grid"]["ts"]
    if any(b - a != int(b - a) for a, b in zip(ts, ts[1:])):
        cover.add("grid non-integer T step")
    for where, lab, p, t in pts:
        ref = ref_mod.read(doc, p, t)
        try:
            eng = engine_read(edoc, p, t)
        except Exception as e:                          # a raise is a difference, named
            eng = {"raised": f"{type(e).__name__}: {e}"}
        by_read[ref["read"]] = by_read.get(ref["read"], 0) + 1
        cover.add(f"read {ref['read']}" if ref["read"] != "table" else f"why {ref['why']}")
        if ref["read"] == "cut":
            cut_fields.setdefault(where, set()).add(ref["field"])
        if lab == "p136":
            cover.add("point p136")
        if not isinstance(eng, dict):
            d = [f"engine answer is a {type(eng).__name__}, not a dict"]
        else:
            d = [f"engine raised {eng['raised']}"] if "raised" in eng else diff(ref, eng)
        if d:
            diffs.append({"where": where, "point": lab, "p": p, "t": t, "why": d})
    for key, seen in cut_fields.items():                 # both of a cut cell's fields answered: A's side and B's
        c = doc["cells"].get(key, {}).get("cut") or {}
        if c.get("a") != c.get("b") and {c.get("a"), c.get("b")} <= seen:
            cover.add("cut both sides")
    return {"store_sha256": hashlib.sha256(raw).hexdigest(), "cells": len(doc["cells"]), "points": len(pts),
            "by_read": dict(sorted(by_read.items())), "covered": sorted(cover), "n_differences": len(diffs),
            "differences": diffs[:50]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reference", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--item1", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--per-cell", type=int, default=4)
    ap.add_argument("stores", nargs="+")
    a = ap.parse_args(argv)
    try:
        ref_mod = load_reference(a.reference)
        from solver import d2_store
        raws = {s: Path(s).read_bytes() for s in a.stores}
        gzip.decompress(next(iter(raws.values())))
    except Exception as e:
        print(f"STOP: {type(e).__name__}: {e}")
        return 2
    rblob = hashlib.sha1(b"blob %d\0" % len(Path(a.reference).read_bytes()) + Path(a.reference).read_bytes()).hexdigest()
    res = {"tool": "d2_read_compare", "reference_reader": a.reference, "reference_reader_blob": rblob,
           "item1": a.item1, "seed": a.seed, "per_cell": a.per_cell, "stores": {}}
    bad = 0
    for s, raw in raws.items():
        try:
            r = compare_store(raw, ref_mod, d2_store.read_point, a.item1, a.seed, a.per_cell)
        except Exception as e:
            print(f"STOP: {s}: {type(e).__name__}: {e}")
            return 2
        res["stores"][s] = r
        bad += r["n_differences"]
        print(f"{s}: {r['cells']} cells, {r['points']} points {r['by_read']}, differences {r['n_differences']}")
    covered = set().union(*(set(r["covered"]) for r in res["stores"].values()))
    res["item1_missing"] = [c for c in ITEM1_CASES if c not in covered] if a.item1 else []
    Path(a.out).write_text(json.dumps(res, indent=1, sort_keys=True, default=repr) + "\n")
    if res["item1_missing"]:
        print(f"STOP: §9 item 1's cases with no reference answer in these stores: {res['item1_missing']}")
        return 2
    if bad:
        print(f"STOP: {bad} points where the engine read differs from the reference reader")
        return 2
    print("d2_read_compare: the engine read equals the reference reader at every point, bit for bit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
