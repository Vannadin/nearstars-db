# 몸 파일에서 층 적분기 Stack 을 짓는 body_stack 의 시험 — 화성 칸 대조 · 비트 · 이름 댄 거절 · 가상 정체 지구 끝까지 (ⓐ1)
"""Checks for ⓐ1 (pre-registration `prereg-a1-body-stack.md`, frozen ea6000e1, addenda 1–2).

    python3 engine/test_body_stack.py

A1-화성      — `body_stack(mars.yaml)` against `samuel_stack` (no-layer set, source-form switches, P_m at the upper
               end — addendum 1), slot by slot: every difference must be a body-file declaration or a structure
               derivation, and each is printed with its reason.
A1-화성-비트  — with those differences overwritten by the plate's values, one evaluation and one full 4.5 Gyr run are
               bit-identical to `samuel_stack` (the builder moves slots without changing values). ⚠ The frozen text
               also names a 4S point; Mars declares no basal layer (addendum 1), so no layered stack can be built
               from its body file — the check runs on the no-layer form only.
A1-거절      — each required field removed is refused by its name; Λ missing with no argument is refused; a bad grade
               and a non-number are refused; the shipped Earth (`mobile`) is refused by name.
A1-끝까지    — the test-only stagnant Earth runs to its age or is refused by name; no `samuel_model` default is used.
"""
from __future__ import annotations

import copy
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import body_stack as bs                # noqa: E402
import samuel_model as sm              # noqa: E402
import samuel_structure as sst         # noqa: E402
import thermal_stack as ts             # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


MARS = HERE / "bodies" / "mars.yaml"
EARTH = HERE / "bodies" / "earth.yaml"
FAKE_EARTH = HERE / "test_fixtures" / "earth_stagnant_test_only.yaml"
STATE = (2191.8284607057844, 1752.7913502870781, 80e3, 20e3, 1.0)

prof = sst.mars_profile(MARS)
b = bs.body_stack(MARS, profile=prof)
s = ts.samuel_stack(lam=b.lam, profile=prof, g=prof.gravity(prof.radius_m), model="no_bml", p_m_mode="top",
                    source_volume=True, source_lid_heat=True, r_c=prof.core_radius_m)

# ── A1-화성 — slot by slot
EXPECTED = {("core", "rho"): "derived from the structure (core mass ÷ volume, decision ③)",
            ("core", "t0"): "the body file's core_initial_temperature",
            ("mantle", "t0"): "the body file's mantle_initial_potential_temperature",
            ("lid", "r_top"): "the structure's radius",
            ("body", "age_gyr"): "the body file's age_gyr",
            ("body", "t_surface"): "the body file's surface_temperature_k"}
diffs = []
for L1, L2 in zip(b.layers, s.layers):
    for k in sorted(set(L1.params) | set(L2.params)):
        if L1.params.get(k, "<none>") != L2.params.get(k, "<none>"):
            diffs.append((L1.role, k, L1.params.get(k), L2.params.get(k)))
    for k, a, c in (("r_bot", L1.r_bot, L2.r_bot), ("r_top", L1.r_top, L2.r_top)):
        if a != c:
            diffs.append((L1.role, k, a, c))
for tag, x, y in (("opt", b.opt, s.opt), ("body", b.body, s.body)):
    for k in sorted(set(x) | set(y)):
        if x.get(k, "<none>") != y.get(k, "<none>"):
            diffs.append((tag, k, x.get(k), y.get(k)))
check("A1-화성 — same layers", [x.role for x in b.layers] == [x.role for x in s.layers],
      str([x.role for x in b.layers]))
unexplained = [d for d in diffs if (d[0], d[1]) not in EXPECTED]
for d in diffs:
    print(f"      differs: {d[0]}.{d[1]} — body_stack {d[2]!r} · samuel_stack {d[3]!r} — "
          f"{EXPECTED.get((d[0], d[1]), 'UNEXPLAINED')}")
check("A1-화성 — every difference is a body declaration or a structure derivation", not unexplained,
      f"{len(diffs)} differ, {len(unexplained)} unexplained")
check("A1-화성 — gravity from the same structure", b.g == s.g)

# ── A1-화성-비트 — overwrite the differences with the plate's values
for L1, L2 in zip(b.layers, s.layers):
    for k in ("rho", "t0"):
        if k in L2.params:
            L1.params[k] = L2.params[k]
    L1.r_bot, L1.r_top = L2.r_bot, L2.r_top
b.r_p = s.r_p
b.body.update(age_gyr=s.body["age_gyr"], t_surface=s.body["t_surface"])
check("A1-화성-비트 — one evaluation bit-identical to samuel_stack",
      ts.state_terms(b, *STATE, -0.02) == ts.state_terms(s, *STATE, -0.02))
b2 = bs.body_stack(MARS, profile=prof)
s2 = ts.samuel_stack(lam=b2.lam, profile=prof, g=prof.gravity(prof.radius_m), model="no_bml", p_m_mode="top",
                     source_volume=True, source_lid_heat=True, r_c=prof.core_radius_m)
for L1, L2 in zip(b2.layers, s2.layers):
    for k in ("rho", "t0"):
        if k in L2.params:
            L1.params[k] = L2.params[k]
    L1.r_bot, L1.r_top = L2.r_bot, L2.r_top
b2.r_p = s2.r_p
b2.body.update(age_gyr=s2.body["age_gyr"], t_surface=s2.body["t_surface"])
ra, rb = ts.run(b2, 10.0), ts.run(s2, 10.0)
key = lambda out: (out.get("refused"), [(r["t"], r["t_c"], r["t_m"], r["d_l"], r["d_cr"]) for r in out["rows"]])
check("A1-화성-비트 — full run bit-identical to samuel_stack", key(ra) == key(rb),
      f"{len(ra['rows'])} rows · refused {ra.get('refused')}")

# ── A1-거절
doc = yaml.safe_load(MARS.read_text(encoding="utf-8"))


def refused_with(mutate, needle: str, lam=None) -> tuple[bool, str]:
    d = copy.deepcopy(doc)
    mutate(d["inputs"])
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        yaml.safe_dump(d, f, allow_unicode=True)
        path = Path(f.name)
    try:
        bs.body_stack(path, profile=prof, crust_lambda=lam)
        return False, "built"
    except bs.Refused as e:
        return needle in str(e), str(e)
    finally:
        path.unlink()


n_ok = 0
for group, keys in bs.FIELDS.items():
    for k in keys:
        ok, msg = refused_with(lambda i, g=group, k=k: i["thermal_evolution"][g].pop(k), f"thermal_evolution.{group}.{k}")
        n_ok += ok
        if not ok:
            print(f"      not refused by name: {group}.{k} — {msg}")
total = sum(len(v) for v in bs.FIELDS.values())
check(f"A1-거절 — each required field removed is refused by its name", n_ok == total, f"{n_ok}/{total}")
ok, msg = refused_with(lambda i: i["thermal_evolution"]["crust"].pop("enrichment"), "crust.enrichment")
check("A1-거절 — Λ missing and no crust_lambda: refused by name", ok, msg)
ok, _ = refused_with(lambda i: i["thermal_evolution"]["crust"].pop("enrichment"), "", lam=10.0)
check("A1-거절 — Λ missing but crust_lambda given: builds", not ok)
ok, msg = refused_with(lambda i: i["thermal_evolution"]["mantle"]["k"].update(grade="calibrated"), "mantle.k.grade")
check("A1-거절 — a result-only grade in an input field is refused", ok, msg)
ok, msg = refused_with(lambda i: i["thermal_evolution"]["mantle"]["k"].pop("counter_evidence_searched"),
                       "counter_evidence_searched")
check("A1-거절 — a missing counter_evidence_searched is refused", ok, msg)
ok, msg = refused_with(lambda i: i["thermal_evolution"]["mantle"]["eta0"].update(value="6.0e21"), "not a number")
check("A1-거절 — a value YAML read as text is refused", ok, msg)
try:
    bs.read(EARTH)
    check("A1-거절 — the shipped Earth (mobile) is refused by name", False, "built")
except bs.Refused as e:
    check("A1-거절 — the shipped Earth (mobile) is refused by name", bs.MOBILE_REFUSAL in str(e), str(e))
lam_override = bs.body_stack(MARS, profile=prof, crust_lambda=5.0).lam
check("A1-거절 — crust_lambda overrides the body file's Λ", lam_override == 5.0 and b.lam == 11.7,
      f"file {b.lam} · override {lam_override}")

# ── A1-끝까지 — the test-only stagnant Earth
sm.DEFAULT_USES.clear()
try:
    e = bs.body_stack(FAKE_EARTH)
    out = ts.run(e, 10.0)
    end = out["rows"][-1]["t"] if out["rows"] else None
    ran = out.get("refused") is None and end is not None and abs(end - e.body["age_gyr"]) < 1e-9
    named = out.get("refused") is not None
    check("A1-끝까지 — test-only stagnant Earth runs to its age or is refused by name", ran or named,
          f"end {end} Gyr of {e.body['age_gyr']} · refused {out.get('refused')}")
except bs.Refused as err:
    check("A1-끝까지 — test-only stagnant Earth runs to its age or is refused by name", True, f"refused: {err}")
check("A1-끝까지 — no samuel_model default used", sm.DEFAULT_USES == {}, str(sm.DEFAULT_USES))

print(f"\n  test_body_stack — {'모두 통과' if fails == 0 else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
