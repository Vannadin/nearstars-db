# 상 구간 행 착지 증명 — 이름 붙인 상태 집합을 풀어 zones·solve_id 를 뺀 결과 해시를 기록하고 base·tip 을 대조 (zones-prereg §4.1, 시험 묶음 밖)
"""Landing proof of `rewrite/layers/zones-prereg.frozen.md` §4.1 (artifacts, blob 244711f0): no physics change.

Outside the suite on purpose (§4.1): whole-answer hashes depend on the interpreter and the machine (§8.1: the same tree
gives different hashes on 3.11 and 3.12), so the proof is base against tip on one machine with one interpreter, and its
output goes into the landing note.

    <python> -m solver.landing.zones_identity record OUT.json [state …]   # from the engine tree root, at base and at tip
    <python> -m solver.landing.zones_identity compare BASE.json TIP.json
    <python> -m solver.landing.zones_identity control note|ulp OUT.json [state …]   # §4.1.2's two controls, at the tip

Per state (§4.1.1), `record` writes:
- (a) `digest`: sha256 of canonical plain((outcome, warm)) with every `solve_id` and every `zones` key removed;
- (b) `solve_ids`: the solve_id values the outcome carries, computed with `context.solver_code_bytes` replaced by
  b"" for the whole run (post-freeze note 1: solve_id also hashes the solver's own code, note 17 §5, so it moves with
  any solver edit by design; without the code bytes it hashes the body, material bytes, options and SOLVER_VERSION,
  which must not move), and `solver_code`: sha256 of the real code bytes, which does move;
- (d) `oracle_digest`: sha256 of run_oracle.one's record with `solve_id`, `zones` and the header's tree, dirty, venv
  and engine_identical_to_oracle_tree removed (those name the checkout, not the physics);
- `outcome`: the outcome kind and, for a refusal or no-answer, its id or reason;
- at a tree whose Answer has `zones`, `rows`: the rows' plain form, and `row_checks`: §4.3 (a), (b) and (d) on them
  (68's note on the frozen text: Earth 1600 K on's row checks run here, not in the suite). (d) compares the rows of the
  direct solve with the rows run_oracle's own solve wrote, so a second solve is not added.
`control note` records with the zoned Answer built with one extra Note; `control ulp` with one node's T moved by one
ulp in the profiles. Each is a mutant of the answer as built, so its compare against the base record must be RED
naming the state (§4.1.2's controls, 68 B1 on the code package).
`compare` prints one line per state and «zones identity: PASS» only when (a), (b) and (d) are equal on every state and
every tip row check holds; else «RED» with the states named. rc 0 / 1.
(c) derived --all is run beside it by the landing round (derived/check.py), not here.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys

#: §4.1.1: (name, body file, state, switch). «declared» is the body's own T_pot; a float is a T_pot state.
STATES = (
    ("earth_1700_off", "engine/bodies/earth.yaml", 1700.0, False),
    ("earth_1600_on", "engine/bodies/earth.yaml", 1600.0, True),
    ("earth_1700_on", "engine/bodies/earth.yaml", 1700.0, True),
    ("mars_off", "engine/bodies/mars.yaml", "declared", False),
    ("mars_on", "engine/bodies/mars.yaml", "declared", True),
    ("venus_off", "engine/bodies/venus.yaml", "declared", False),
    ("venus_on", "engine/bodies/venus.yaml", "declared", True),
    ("dante_off", "engine/bodies/dante_fixture.yaml", "declared", False),
    ("dante_on", "engine/bodies/dante_fixture.yaml", "declared", True),
    ("pandora_off", "engine/bodies/pandora.yaml", "declared", False),
    ("pandora_on", "engine/bodies/pandora.yaml", "declared", True),
)
HEADER_DROP = ("tree", "dirty", "venv", "engine_identical_to_oracle_tree", "solve_id")


def _drop(x, keys=("solve_id", "zones")):
    if isinstance(x, dict):
        return {k: _drop(v, keys) for k, v in x.items() if k not in keys}
    if isinstance(x, list):
        return [_drop(v, keys) for v in x]
    return x


def _sha(obj) -> str:
    text = json.dumps(obj, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def _solve_ids(x, out):
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "solve_id" and isinstance(v, str):
                out.add(v)
            else:
                _solve_ids(v, out)
    elif isinstance(x, list):
        for v in x:
            _solve_ids(v, out)
    return out


def _outcome(o) -> dict:
    from solver import result
    kind = result.outcome_kind(o)
    return {"kind": kind, "id": getattr(o, "id", None) if kind == "refusal" else getattr(o, "reason", None)}


def record_state(name, path, state, switch) -> dict:
    from solver import context, from_v1, result, run_oracle, solve as sv
    opt = dataclasses.replace(context.Options(), silicate_records=switch)
    got = from_v1.load_v1(path)
    body = got[0] if isinstance(got, tuple) else got
    if isinstance(body, result.Refusal):
        out, warm = body, None
    else:
        if state != "declared":
            body = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=float(state)))
        out, warm = sv.solve(body, opt)
    plain = result.plain((out, warm))
    rec = run_oracle.one(path, state, opt)
    hdr = {k: v for k, v in (rec.get("header") or {}).items() if k not in HEADER_DROP}
    orec = _drop({**rec, "header": hdr})
    got = {"state": [path, state, switch], "outcome": _outcome(out), "digest": _sha(_drop(plain)),
           "solve_ids": sorted(_solve_ids(plain, set())), "oracle_digest": _sha(orec)}
    if isinstance(out, result.Answer) and hasattr(out, "zones"):
        from solver import phase_zones
        rows = [result.plain(z) for z in out.zones]
        got["rows"] = rows
        got["row_checks"] = phase_zones.check_rows(out) + (
            [] if rows == rec.get("zones") else ["(d) the oracle solve's rows differ from the direct solve's"])
    return got


def _plant(kind):
    """Replace phase_zones.Answer (what solve.py builds) with a mutant builder for this process: «note» appends one
    Note, «ulp» moves the last node's T of the first profiled layer by one ulp."""
    import math
    from solver import phase_zones, result
    real = phase_zones.Answer

    def build(qs, lbs, profiles, missing, notes, zones=()):
        if kind == "note":
            notes = tuple(notes) + (result.Note("planted_control", "zones §4.1.2 control: one appended note", {}),)
        elif kind == "ulp":
            prof = {lid: dict(cols) for lid, cols in dict(profiles).items()}
            lid = next(iter(prof))
            t = list(prof[lid]["T"] if "T" in prof[lid] else prof[lid]["P"])
            col = "T" if "T" in prof[lid] else "P"
            t[-1] = math.nextafter(t[-1], math.inf)
            prof[lid][col] = tuple(t)
            profiles = prof
        else:
            raise ValueError(kind)
        return real(qs, lbs, profiles, missing, notes, zones)
    phase_zones.Answer = build


def _tree() -> dict:
    import subprocess
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    git = lambda *a: subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True).stdout.strip()
    return {"head": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain", "--", "solver", "engine"))}


def record(path_out, names=None) -> int:
    from solver import context
    code = hashlib.sha256(context.solver_code_bytes()).hexdigest()
    context.solver_code_bytes = lambda: b""                 # (b): solve_id without the code digest, this process only
    names = set(names or [s[0] for s in STATES])
    unknown = names - {s[0] for s in STATES}
    if unknown:
        print(f"STOP: unknown states {sorted(unknown)}")
        return 2
    out = {"python": sys.version.split()[0], "options_default": dataclasses.asdict(context.Options()),
           "solver_code": code, "tree": _tree(), "states": {}}
    for name, path, state, switch in STATES:
        if name not in names:
            continue
        out["states"][name] = got = record_state(name, path, state, switch)
        print(f"{name}: {got['outcome']['kind']} {got['outcome']['id'] or ''} · digest {got['digest'][:12]} · "
              f"oracle {got['oracle_digest'][:12]}" + (f" · rows {len(got['rows'])} · checks "
                                                      f"{'ok' if not got['row_checks'] else got['row_checks']}"
                                                      if "rows" in got else ""), flush=True)
    with open(path_out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, sort_keys=True, indent=1, default=str)
        fh.write("\n")
    return 0


def compare(base_path, tip_path) -> int:
    base, tip = (json.load(open(p, encoding="utf-8")) for p in (base_path, tip_path))
    bad = []
    if base["python"] != tip["python"]:
        bad.append(f"interpreter {base['python']} vs {tip['python']}")
    for name in sorted(set(base["states"]) | set(tip["states"])):
        b, t = base["states"].get(name), tip["states"].get(name)
        if b is None or t is None:
            bad.append(f"{name} missing on {'base' if b is None else 'tip'}")
            print(f"{name}: missing on {'base' if b is None else 'tip'}")
            continue
        diff = [k for k in ("outcome", "digest", "solve_ids", "oracle_digest") if b[k] != t[k]]
        checks = t.get("row_checks") or []
        print(f"{name}: {t['outcome']['kind']} · " + ("equal" if not diff else f"DIFFER {diff}")
              + (f" · tip rows {len(t['rows'])} · checks {'ok' if not checks else checks}" if "rows" in t else ""))
        if diff or checks:
            bad.append(name)
    print(f"solver code digest {base['solver_code'][:12]} → {tip['solver_code'][:12]} "
          f"({'moved, as any solver edit moves it' if base['solver_code'] != tip['solver_code'] else 'equal'})")
    print("zones identity: " + ("PASS" if not bad else "RED — " + "; ".join(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["record"] and len(a) >= 2:
        sys.exit(record(a[1], a[2:]))
    if a[:1] == ["control"] and len(a) >= 3 and a[1] in ("note", "ulp"):
        _plant(a[1])
        sys.exit(record(a[2], a[3:]))
    if a[:1] == ["compare"] and len(a) == 3:
        sys.exit(compare(a[1], a[2]))
    print(__doc__)
    sys.exit(2)
