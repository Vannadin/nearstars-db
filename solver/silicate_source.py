# 규산염 표 출처 뼈대 — 조성 지문으로 출하 레코드를 찾고, 없으면 오늘의 거절에 건축 요청서를 붙인다 (layers S2; 빌더는 S3)
"""The silicate table interface (layers S2 registration 106041ab; design 7a5c34ab §5), stubbed until the migration.

- `key(oxides_wt)` delegates to `material_assemblage.composition_key`, byte-unchanged (§2.2: material_assemblage.py's
  blob is pinned by the shipped tables' monotone sidecars, the 8d-silicate-slb entry and the fall-set stamps).
- `lookup(key, registry)`: the assemblage records whose composition_key equals `key` (moved from solve._silicate_route).
- `request(...)`: a BuildRequest, pure. It carries the **declared** CFMASNa oxides (rev 1, 68 B1: composition_key
  re-normalises before it rounds, so only the declared oxides recompute the key; the generator keys a record the same
  way, gen_silicate_records.py:566/:1124/:1221).
- `request_json(req)`: its deterministic bytes. The caller writes them (run_oracle, §3); nothing here does I/O.
- `resolve(...)`: (rid, None) or (None, (kind, detail)) with today's kinds: unknown_material, composition_key_ambiguous,
  no_table_for_composition (detail (key, built, request)).
No module state (A6); the registry is passed in.
"""
from __future__ import annotations

import json

from solver import material_assemblage as ma
from solver.result import freeze, plain

SCHEMA = 1
GRID = "default"                                    # the shipped 176-column grid and window (design §5)
BUILDER = "burnman_cpp (pinned at S3)"              # a name only; the pin is S3's, after the migration lands


def key(oxides_wt) -> str:
    """The composition fingerprint: material_assemblage.composition_key, unchanged."""
    return ma.composition_key(oxides_wt)


def lookup(k: str, registry) -> tuple:
    """The assemblage records whose composition_key is `k`, in the registry's order (today's `hits`)."""
    return tuple(rid for rid, r in registry.records.items() if r["kind"] == "assemblage" and r["composition_key"] == k)


def request(oxides_wt, *, source_kind, grade, requested_by):
    """A BuildRequest for a composition no shipped record holds (pure; frozen)."""
    return freeze({"schema": SCHEMA, "composition_key": key(oxides_wt),
                   "oxides_wt": {c: oxides_wt[c] for c in ma.CFMASNA},
                   "dropped_wt": {c: v for c, v in oxides_wt.items() if c not in ma.CFMASNA},
                   "source_kind": source_kind, "grade": grade, "grid": GRID, "builder": BUILDER,
                   "requested_by": requested_by})


def request_json(req) -> str:
    """The request's bytes: sorted keys, no NaN, one trailing newline (two equal requests give equal bytes)."""
    return json.dumps(plain(req), sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def resolve(oxides_wt, registry, *, source_kind, grade, requested_by):
    """(rid, None), or (None, (kind, detail)) with today's kinds and texts (solve._silicate_route before S2)."""
    try:
        k = key(oxides_wt)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as e:
        return None, ("unknown_material", f"silicate_decl composition has no CFMASNa reduction: {e!r}")
    hits = lookup(k, registry)
    if len(hits) > 1:                                # load refuses this; a hand-built registry must not pick one
        return None, ("composition_key_ambiguous", f"records {sorted(hits)} share composition key {k}")
    if not hits:
        built = sorted(r["composition_key"] for r in registry.records.values() if r["kind"] == "assemblage")
        return None, ("no_table_for_composition",
                      (k, built, request(oxides_wt, source_kind=source_kind, grade=grade, requested_by=requested_by)))
    return hits[0], None
