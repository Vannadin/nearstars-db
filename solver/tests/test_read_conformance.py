# 읽기 적합성 시험 — 동결된 read-view 등록서 §4 와 note 1–4 가 «읽기»에 요구하는 메서드·속성·키·거절 종류를 한 읽기 객체에 행마다 확인; 장난감 읽기와 c8 의 커밋된 읽기에서 돎 (directing 11-18)
"""Every row is one sentence of the frozen read-view registration (§4) or its notes 1–4 that requires something of «the
read». `check(read)` returns [(row, ok, detail)]. Run on:
- ConformingToy: a minimal read written to the rows here, so every row can pass (and each row's mutant fails);
- c8's committed read (NEARSTARS_C8_PROTO = a checkout of pc/c8-part2/proto, NEARSTARS_BMCPP for its loader), red
  until it carries every row; skipped by name where NEARSTARS_C8_PROTO is unset.
Rows not exercisable on an arbitrary read («cut», «invalid_state»: they need the read's own excluded region or a
continuation that fails) are listed in ROWS_NOT_EXERCISED, by name."""
import math
import os
import pickle
import sys
import unittest

from solver import read_view as rv
from solver import stepper as st

STATE_KEYS = ("rho", "s", "c_p", "dtdp", "alpha", "K_T", "field")
FOLD_KEYS = ("zone", "curve", "dPb_dT_max_Pa_per_K", "walk_reach_pa_up", "walk_reach_pa_down", "to_field_up",
             "to_field_down", "walk_t_served_up", "walk_t_served_down")
TJUMP_KEYS = ("T_new", "ds", "dT", "from", "to")
ROWS_NOT_EXERCISED = ("§4.4 kind «cut» (needs the read's own declared exclusion)",
                      "§4.4 kind «invalid_state» (needs a continuation that gives c_P, K_T or V ≤ 0)",
                      "§4.7 determinism (same inputs, same bytes): covered by solve_id tests on the read's stamp")


def _refusal(fn):
    try:
        fn()
    except Exception as e:                                         # noqa: BLE001 — classified by the row
        return e
    return None


def _is_refusal(e, kind):
    return (e is not None and type(e).__name__ == "ReadRefusal" and isinstance(e, ValueError)
            and getattr(e, "kind", None) == kind and getattr(e, "why", None) == str(e))


def check(read, probe):
    """`probe`: {"p", "t"} a served state; {"p_deep"} past the deepest piece; {"t_cold"} below the T box."""
    rows = []

    def row(name, ok, detail=""):
        rows.append((name, bool(ok), detail))
    p, t = probe["p"], probe["t"]
    d = _refusal(lambda: read.state(p, t))
    got = read.state(p, t) if d is None else None
    row("§4.1 state(p, t) → {rho, s, c_p, dtdp, alpha, K_T, field}", got is not None and all(k in got for k in STATE_KEYS),
        repr(d) if d is not None else f"missing {[k for k in STATE_KEYS if k not in (got or {})]}")
    row("§4.1 state values finite (§4.4 last bullet)", got is not None and all(
        isinstance(got[k], (int, float)) and math.isfinite(got[k]) for k in STATE_KEYS if k != "field"))
    e = _refusal(lambda: read.state(-1.0, t))
    row("§4.4 ReadRefusal(ValueError) with .kind, .why == str(e); «p_negative» at P < 0", _is_refusal(e, "p_negative"),
        repr(e))
    e = _refusal(lambda: read.state(p, probe["t_cold"]))
    row("§4.4 «extent» outside the T box", _is_refusal(e, "extent"), repr(e))
    e = _refusal(lambda: read.state(probe["p_deep"], t))
    row("§4.4 «past_deepest» past the last piece", _is_refusal(e, "past_deepest"), repr(e))
    folds = getattr(read, "folds", None)
    row("§4.5 / note 3 §1 rd.folds: a list of dicts with the directional keys", isinstance(folds, list) and folds and all(
        all(k in f for k in FOLD_KEYS) for f in folds), "" if folds else "no folds attribute or empty")
    row("note 4 §1 rd.continuations: a list", isinstance(getattr(read, "continuations", None), list))
    evs = _refusal(lambda: read.events(t_index=2))
    evs = read.events(t_index=2) if evs is None else evs
    ok_ev = isinstance(evs, (list, tuple)) and all(isinstance(ev, st.Event) for ev in evs)
    row("§4.3 events(t_index=2) → stepper.Event list", ok_ev, repr(evs)[:200] if not ok_ev else "")
    if ok_ev:
        bad = [ev.name for ev in evs if not (ev.seam and not ev.terminal and ev.scale and math.isfinite(ev.scale)
                                             and isinstance(ev.tag, dict))]
        row("§4.3 every Event seam, not terminal, finite scale, a tag dict", not bad, f"{bad[:5]}")
        curves = [ev for ev in evs if ev.component == 1]
        row("§4.3 curve and P-seam Events on component 1", bool(curves))
        tagged = [ev for ev in evs if ev.tag.get("tagged")]
        keys = {(ev.tag.get("zone"), ev.tag.get("curve")) for ev in tagged}
        fk = {(f["zone"], f["curve"]) for f in (folds or [])}
        row("§4.5 the tagged Events are exactly the folds (zone, curve)", keys == fk and len(tagged) == len(fk),
            f"tagged {sorted(map(str, keys))} folds {sorted(map(str, fk))}")
        if tagged and folds:
            f = folds[0]
            ev = next(e_ for e_ in tagged if (e_.tag["zone"], e_.tag["curve"]) == (f["zone"], f["curve"]))
            ev3 = next((e_ for e_ in read.events(t_index=3) if e_.name == ev.name), None)
            tz = probe["t_fold"]
            y2 = (1.0, probe["p_fold"], tz, tz + 50.0, 0.0, 0.0)
            y3 = (1.0, probe["p_fold"], tz + 50.0, tz, 0.0, 0.0)
            row("§4.3 t_index=3 reads y[3], t_index=2 reads y[2]", ev3 is not None and ev.g(0.0, y2) is not None
                and ev.g(0.0, y2) == ev3.g(0.0, y3), "")
            j = _refusal(lambda: read.t_jump(probe["p_fold"], tz, f["zone"], f["curve"], True))
            j = read.t_jump(probe["p_fold"], tz, f["zone"], f["curve"], True) if j is None else j
            row("§4.5 t_jump(P, T, zone, curve, upward) → {T_new, ds, dT, from, to}", isinstance(j, dict) and all(
                k in j for k in TJUMP_KEYS), repr(j)[:200])
            row("note 3 §1 t_jump «to» upward == fold to_field_up", isinstance(j, dict) and j.get("to") == f["to_field_up"],
                f"{j.get('to') if isinstance(j, dict) else j} vs {f['to_field_up']}")
            un = probe.get("untagged")
            if un is not None:
                e = _refusal(lambda: read.t_jump(probe["p_fold"], tz, un[0], un[1], True))
                row("§4.4 «tjump_untagged» at an untagged curve", _is_refusal(e, "tjump_untagged"), repr(e))
            lo, hi = (float(x) for x in f["walk_t_served_up"])
            pin = (f["zone"], f["curve"], "up")
            ins = read.state(probe["p_fold"], tz, field=f["to_field_up"], pin=pin)
            row("note 3 §2 pinned state → the to-field, with t_continuation (note 4)", ins.get("field") == f["to_field_up"]
                and isinstance(ins.get("t_continuation"), bool), repr({k: ins.get(k) for k in ("field", "t_continuation")}))
            out_t = hi + 10.0 if math.isfinite(hi) else lo - 10.0
            e = _refusal(lambda: read.state(probe["p_fold"], out_t, field=f["to_field_up"], pin=pin))
            row("note 3 §2 «pin_unserved» outside walk_t_served", _is_refusal(e, "pin_unserved"), repr(e))
            e = _refusal(lambda: read.state(probe["p_fold"], tz, field="__no_such_field__", pin=pin))
            row("§4.4 «field_unknown» for a field the fold does not have", _is_refusal(e, "field_unknown"), repr(e))
            e = _refusal(lambda: read.state(probe["p_fold"], tz, field=f["to_field_up"], pin=(10 ** 6, 0, "up")))
            row("note 3 §3 a pin naming no fold refuses «pin_unserved»", _is_refusal(e, "pin_unserved"), repr(e))
    return rows


class ReadRefusal(ValueError):
    def __init__(self, kind, why):
        super().__init__(why)
        self.kind, self.why = kind, why


class ConformingToy:
    """One zone (T 1000–3000 K, P 0–1e11 Pa), two fields A (P < P_b) and B, one tagged curve P_b = 1e10 + 1e6·(T − 2000)
    and one untagged curve (zone 0, curve 1) at P_b' = 5e10; written to the rows above."""
    K, P0, T0 = 1.0e6, 1.0e10, 2000.0

    def __init__(self):
        self.folds = [{"zone": 0, "curve": 0, "dPb_dT_max_Pa_per_K": self.K, "walk_reach_pa_up": 1e9,
                       "walk_reach_pa_down": 1e9, "to_field_up": "B", "to_field_down": "A",
                       "walk_t_served_up": [1000.0, 3000.0], "walk_t_served_down": [1000.0, 3000.0]}]
        self.continuations = []

    def _check(self, p, t):
        if p < 0:
            raise ReadRefusal("p_negative", f"refused: P {p} < 0")
        if p > 1e11:
            raise ReadRefusal("past_deepest", "refused: P past the deepest piece")
        if not 1000.0 <= t <= 3000.0:
            raise ReadRefusal("extent", f"refused: T {t} outside the T box")

    def _d(self, f):
        return {"rho": 3500.0, "s": 0.0, "c_p": 1200.0, "dtdp": 1e-8 if f == "A" else 5e-7, "alpha": 1e-5,
                "K_T": 1e11, "field": f}

    def state(self, p, t, field=None, pin=None):
        if pin is not None:
            if (pin[0], pin[1]) != (0, 0) or pin[2] not in ("up", "down"):
                raise ReadRefusal("pin_unserved", f"refused: pin {pin} names no tagged fold")
            if field not in ("A", "B"):
                raise ReadRefusal("field_unknown", f"refused: field {field}")
            if not 1000.0 <= t <= 3000.0:
                raise ReadRefusal("pin_unserved", f"refused: T {t} outside the served T")
            return dict(self._d(field), t_continuation=False)
        self._check(p, t)
        return self._d("A" if p < self.P0 + self.K * (t - self.T0) else "B")

    def events(self, t_index=2):
        def g0(m, y, ti=t_index):
            return y[1] - (self.P0 + self.K * (y[ti] - self.T0)) if 1000.0 <= y[ti] <= 3000.0 else None

        def g1(m, y):
            return y[1] - 5e10
        return [st.Event("z0:c0", g0, scale=self.P0 + self.K * 1000.0, terminal=False, seam=True, component=1,
                         tag={"curve": 0, "zone": 0, "tagged": True}),
                st.Event("z0:c1", g1, scale=5e10, terminal=False, seam=True, component=1,
                         tag={"curve": 1, "zone": 0, "tagged": False})]

    def t_jump(self, p, t, zone, curve, upward=True):
        if (zone, curve) != (0, 0):
            raise ReadRefusal("tjump_untagged", f"refused: T jump at an untagged crossing ({zone}, {curve})")
        a, b = ("A", "B") if upward else ("B", "A")
        return {"T_new": t + 0.01, "ds": 0.0, "dT": 0.01, "from": a, "to": b}


TOY_PROBE = {"p": 5e9, "t": 2000.0, "p_deep": 2e11, "t_cold": 500.0, "p_fold": 1e10, "t_fold": 2000.0,
             "untagged": (0, 1)}


class Conformance(unittest.TestCase):
    def assert_rows(self, rows):
        bad = [(n, d) for n, ok, d in rows if not ok]
        self.assertEqual(bad, [], "\n".join(f"{n}: {d}" for n, d in bad))

    def test_conforming_toy(self):
        self.assert_rows(check(ConformingToy(), TOY_PROBE))

    def test_each_toy_mutant_fails_a_row(self):
        """Removing one thing the rows require fails at least one row (the rows can fail)."""
        for name, mutate in (("no folds", lambda r: delattr(r, "folds")),
                             ("no continuations", lambda r: delattr(r, "continuations")),
                             ("wrong to_field_up", lambda r: r.folds[0].update(to_field_up="A")),
                             ("no t_continuation", lambda r: setattr(r, "state", lambda p, t, field=None, pin=None:
                                                                      ConformingToy._d(r, field or "A"))),
                             ("events not Event", lambda r: setattr(r, "events", lambda t_index=2: [object()]))):
            with self.subTest(mutant=name):
                r = ConformingToy()
                mutate(r)
                self.assertTrue(any(not ok for _, ok, _ in check(r, TOY_PROBE)), name)

    def test_c8_committed_read(self):
        d = os.environ.get("NEARSTARS_C8_PROTO")
        if not d:
            raise unittest.SkipTest("NEARSTARS_C8_PROTO not set: c8's committed Pandora read is not on this machine")
        if d not in sys.path:
            sys.path.insert(0, d)
        with open(os.path.join(d, "read_pandora_1600.pkl"), "rb") as f:
            rd = pickle.load(f)
        f0 = rd.folds[0]
        z0, z1 = (float(x) for x in rd.zones[f0["zone"]][:2])
        tz = 0.5 * (z0 + z1)
        ev = next(e for e in rd.events(t_index=2) if (e.tag or {}).get("tagged")
                  and (e.tag["zone"], e.tag["curve"]) == (f0["zone"], f0["curve"]))
        lo_p, hi_p = 1e9, 1e11
        for _ in range(200):                                  # P_b(tz) by bisection on the event's own g
            mid = 0.5 * (lo_p + hi_p)
            g = ev.g(0.0, (1.0, mid, tz, tz, 0.0, 0.0))
            if g is None:
                lo_p = mid if mid < 1.3e10 else lo_p
                hi_p = mid if mid >= 1.3e10 else hi_p
                continue
            lo_p, hi_p = (mid, hi_p) if g < 0 else (lo_p, mid)
        untagged = next(((e.tag["zone"], e.tag["curve"]) for e in rd.events(t_index=2)
                         if e.tag.get("zone") == f0["zone"] and e.tag.get("curve") is not None
                         and not e.tag.get("tagged")), None)
        probe = {"p": 13.0e9, "t": 1755.0, "p_deep": 1e13, "t_cold": 500.0, "p_fold": 0.5 * (lo_p + hi_p),
                 "t_fold": tz, "untagged": untagged}
        self.assert_rows(check(rv.PinGuard(rd), probe))
