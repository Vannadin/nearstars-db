# 광물 집합 읽기 C¹ 항목(5d998d40) 시험 — 실제 기록에서 변 P_b 의 C⁰, 곁 읽기가 남기는 표시·노트 없음, 꺾임 조사 부분집합의 이름 붙은 부류·한도
"""The C¹ read's acceptance in the suite, on the shipped records (a TIP; skipped on the engine branch alone).
- C⁰ at every cut edge (68 ruling 1 (1)): across x_b in ln P by the J₄ test (stage 5c's form, r2 4a60fad7), to 1e-9 of
  the field's size there, in all three fields, every third row, wherever neither side refuses; unresolved at the
  floor is a FINDING; planted jumps of 1e-6 and 1e-8 go red. The blend's C⁰ there rests on the own read equalling the
  same-side side read.
- Side reads leave nothing on the read (ruling 1 (3)): inside the windows a read's notes and counts are its own read's
  (the blend switched off), and a point read cold (fresh view) and warm (after the other points) is the same.
- Slope jumps (68 ruling 4): kinkscan's subset of lines finds no kink outside the named classes or above their bounds
  but the pinned known ones (data/c1_known_violations.json, each with its owner tag; red on a new or grown one);
  the full scan does the same once per landing, outside the suite (landing_kink_scan.py, a PC round task).

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_assemblage_c1
"""
import dataclasses
import json
import math
import os
import unittest

from solver import material_assemblage as ma, material_registry as mr, material_view as mv
from solver.from_v1 import thaw
from solver.tests import kinkscan as ks

#: the in-suite kink subset (68 ruling 4, Q4): per record two fixed-T lines that hold T-clip kinks and one fixed-P line
#: (the full scan's line nearest the given GPa) that holds a T-row-line kink, at v4
SUBSET = {"silicate_slb_default_bse": ((1068.5, 1568.5), (0.9606,)),
          "silicate_slb_earth_dmm_wh2005": ((1668.5, 2268.5), (1.4193,)),
          "silicate_slb_mars_khan2022": ((1668.5, 1768.5), (120.3063,))}

RECORDS = ("silicate_slb_default_bse", "silicate_slb_earth_dmm_wh2005", "silicate_slb_mars_khan2022")

#: the subset's known violations, pinned with an owner tag each (68 README §7–§12, directing 10-23): written by
#: c1_known_violations_writer.py from TIP's shipped records at s on with their fall sets; the test is red on any
#: violation not pinned or grown past 2× its pinned jump_rel, and prints the pins no longer seen («resolved»)
PIN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "c1_known_violations.json")
#: the closed owner tags (68 §7 (a), §8 Q1, §9; directing 10-23 «owner-pending»: s-read entries awaiting the owner's
#: ruling, which block stage A's push while any remain)
PIN_TAGS = frozenset({"kinkscan-b′", "E24", "E26", "records", "pre-existing-AF", "unattributed", "s-read", "owner-pending"})


def _load_pins(path=PIN_FILE):
    """The fixture, checked on load: every pin's tag in PIN_TAGS and a cite and a trigger on each, else ValueError."""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for rid, pins in d["pins"].items():
        for p in pins:
            if p.get("tag") not in PIN_TAGS:
                raise ValueError(f"{rid}: unknown owner tag {p.get('tag')!r}")
            if not p.get("cite") or not p.get("trigger"):
                raise ValueError(f"{rid}: a pin without its cite or trigger ({p.get('tag')}, {p.get('field')})")
    return d


def _scan_steps(v):
    """kinkscan.scan's own coarse steps, the pins' matching tolerance: fixed-T lines in ln P (n steps to p_dataset),
    fixed-P lines in T (max(20·rows, 400) steps)."""
    n = ks.scan.__defaults__[-1]
    return {"P": (math.log(v.p_dataset) - math.log(v.ps[0])) / n, "T": (v.ts[-1] - v.ts[0]) / max(len(v.ts) * 20, 400)}


def _pin_match(k, p, steps):
    """A violation k is pin p: same line, field and class, the line's fixed coordinate equal (T exactly; P, an exp of
    the grid, to 1e-12), the scanned one within one scan step (ln P on a fixed-T line, T on a fixed-P line)."""
    if "line" not in k or (k["line"], k["field"], k["class"]) != (p["line"], p["field"], p["class"]):
        return False
    if k["line"] == "P":                             # fixed T: a SUBSET constant
        return k["T"] == p["T"] and abs(math.log(k["P"]) - math.log(p["P"])) <= steps["P"]
    # fixed P: full_lines' exp of the grid's ln P, so equal to 1e-12 (another libm may differ by an ulp)
    return abs(k["P"] / p["P"] - 1.0) <= 1e-12 and abs(k["T"] - p["T"]) <= steps["T"]


def _against_pins(kinks_violations, pins, steps):
    """(new, grown, resolved, matched): violations matched one to one to their nearest pin; new = unpinned, grown =
    (violation, pin) past 2× the pin's jump_rel, resolved = pins nothing matched."""
    left, new, grown, matched = list(pins), [], [], []
    for k in kinks_violations:
        m = [p for p in left if _pin_match(k, p, steps)]
        if not m:
            new.append(k)
            continue
        p = min(m, key=lambda q: abs(math.log(k["P"] / q["P"])) + abs(k["T"] - q["T"]))
        left.remove(p)
        matched.append(p)
        if k["jump_rel"] > 2.0 * p["jump_rel"]:
            grown.append((k, p))
    return new, grown, left, matched


def _shipped():
    reg = mr.load()
    return all(reg.get(r) is not None and r in reg.tables for r in RECORDS)


def _view(reg, rid):
    return ma.view(thaw(reg.get(rid)), reg.tables[rid], 1600.0)


#: r2 4a60fad7: the edges where the s read crosses the narrow bg→ppv loops, checked by name
NAMED_EDGES = {"silicate_slb_default_bse": (34, 36, 42, 43)}
#: the J₄ ladder in ln P (start, floor: reads down to ±floor/8; under the s read the loop edges 43 resolve at 7.8e-9) and the round-off floor's multiplier on ε|v| (stage 5c,
#: r2 32cf0efe: J₄'s weights (|8| + |6| + |1|)/3 = 5 over two-read differences, 1.6 ε|v| each: 16)
C0_H0, C0_H_FLOOR, C0_FLOOR_K = 1e-6, 1e-10, 16.0


def _j3(s, h):
    return (8.0 * s(h / 4.0) - 6.0 * s(h / 2.0) + s(h)) / 3.0


def _c0_j4(s, v_abs, tol):
    """The stage 5c C⁰ test (r2 32cf0efe, B1 on ac9af31a, addendum db668a80): J = J₃(h/2) + (J₃(h/2) − J₃(h))/7,
    allowance |J₃(h) − J₃(h/2)|/7 + C0_FLOOR_K·ε·|v|; resolved when allowance ≤ tol/2, then ok when |J| ≤ tol + allowance;
    else h halves from C0_H0 down to C0_H_FLOOR, and still unresolved there is «C⁰ unresolved» (not ok)."""
    h = C0_H0
    while True:
        a, b = _j3(s, h), _j3(s, h / 2.0)
        est, allow = b + (b - a) / 7.0, abs(a - b) / 7.0 + C0_FLOOR_K * 2.220446049250313e-16 * v_abs
        q = {"J": est, "allowance": allow, "tol": tol, "h": h}
        if allow <= tol / 2.0:
            return {**q, "resolved": True, "ok": abs(est) <= tol + allow}
        if h / 2.0 < C0_H_FLOOR * (1.0 - 1e-12):
            return {**q, "resolved": False, "ok": False}
        h /= 2.0


def _edge_c0(v, xb, t, plant=None):
    """Per field, _c0_j4 of s(h) = v(x_b + h) − v(x_b − h) in ln P at T; tol 1e-9 of the field's size there (max of
    |v| at x_b and half a window either side, not a 0 crossing). None when a read refuses (a refusal boundary).
    `plant` (field, rel): a jump of rel × the field's size added above x_b (the plants)."""
    cache = {}

    def read(x):
        if x not in cache:
            g = v._solid(math.exp(x), t)
            if not isinstance(g, tuple):
                raise LookupError
            cache[x] = g
        return cache[x]
    try:
        w = v._width(xb)
        mid, far = read(xb), [read(xb + e * w) for e in (-0.5, 0.5)]
        out = []
        for f in range(3):
            scale = max(abs(mid[f]), abs(far[0][f]), abs(far[1][f]))
            add = (lambda x, f=f, sc=scale: plant[1] * sc if (plant and plant[0] == f and x > xb) else 0.0)
            s = (lambda h, f=f: (read(xb + h)[f] + add(xb + h)) - (read(xb - h)[f] + add(xb - h)))
            out.append(_c0_j4(s, scale, 1e-9 * scale))
        return out
    except LookupError:
        return None


def _noscale(n):
    return dataclasses.replace(n, scale=None) if isinstance(n, mv.BandNote) else n


class C1(unittest.TestCase):
    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_continuous_at_every_cut_edge(self):
        """C⁰ in ln P across every cut edge's P_b_ext (every third row, T and T + 17 K), each field, by the J₄ test (r2
        4a60fad7: the stage 5c form): a field whose steps don't resolve its jump to the floor is «C⁰ unresolved», a
        FINDING, never a pass. The four edges where the s read crosses the narrow bg→ppv loops (bse 34/36 at 118 GPa,
        42/43 at 23.5–24 GPa: two-phase slivers ~1/230 of the blend width, the read C¹ with a steep slope across them)
        must be among those checked; their resolved h and allowance are printed. Both reads, s on and off, explicitly
        (r2 n1 on 19178a16: the records' default doesn't leave the other unchecked)."""
        reg = mr.load()
        for rid, s_on in ((r, m) for r in RECORDS for m in (False, True)):
            v = _view(reg, rid)
            v.s_read = s_on
            rid_m = f"{rid} (s read {'on' if s_on else 'off'})"
            n, bad, unres, named = 0, [], [], {}
            for c in v._cut:
                if c.kind != "edge":
                    continue
                for r in c.rows[::3]:
                    for t in (r["t"], r["t"] + 17.0):
                        pb = c.p_b_ext(t, v._reach)
                        if pb is None or not v.ps[0] < pb < v.p_dataset:
                            continue
                        xb = math.log(pb)
                        got = _edge_c0(v, xb, t)
                        if got is None:
                            continue                         # a refusal boundary
                        n += 1
                        for f, q in enumerate(got):
                            if not q["resolved"]:
                                unres.append((c.id, pb / 1e9, t, f, q["h"], q["allowance"]))
                            elif not q["ok"]:
                                bad.append((c.id, pb / 1e9, t, f, q["J"], q["tol"] + q["allowance"]))
                        if c.id in NAMED_EDGES.get(rid, ()):
                            named.setdefault(c.id, []).append((t, [(q["h"], q["allowance"]) for q in got]))
            for cid in sorted(named):
                print(f"{rid_m} edge {cid}: (T, [(resolved h, allowance) per field]) {named[cid][:2]}")
            self.assertGreater(n, 100, rid_m)
            self.assertEqual(sorted(named), sorted(NAMED_EDGES.get(rid, ())), rid_m)
            self.assertEqual(unres[:5], [], f"{rid_m}: C⁰ unresolved at the floor (a FINDING for review)")
            self.assertEqual(bad[:5], [], rid_m)

    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_c0_plants_go_red(self):
        """r2 4a60fad7 (a): a jump planted at bse edge 34's P_b_ext (1650 K) in dT/dP, 1e-6 and 1e-8 of the field's size,
        goes red (resolved, not ok); the same point unplanted passes. The 1e-8 plant shows the floor sits below the band
        the test claims (1e-9 of the field's size). On the s read, explicitly (r2 n1 on 19178a16): the read F13 ships,
        where the loop edges need the deepest resolution."""
        reg = mr.load()
        v = _view(reg, "silicate_slb_default_bse")
        v.s_read = True
        c = next(c for c in v._cut if c.id == 34)
        t = 1650.0
        xb = math.log(c.p_b_ext(t, v._reach))
        clean = _edge_c0(v, xb, t)
        self.assertTrue(all(q["ok"] for q in clean), clean)
        for jump in (1e-6, 1e-8):
            with self.subTest(jump=jump):
                got = _edge_c0(v, xb, t, plant=(1, jump))
                self.assertTrue(got[1]["resolved"] and not got[1]["ok"], got[1])

    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_side_reads_leave_no_note(self):
        """Inside the windows, a read's notes and counts are its own read's: the same as with the blend switched off
        (side reads on scratch marks, 68 ruling 1 (3)); and a point read cold (fresh view) and warm (after the others)
        is the same, values and notes."""
        reg = mr.load()
        for rid in RECORDS:
            v = _view(reg, rid)
            pts = []
            for c in v._cut:
                if c.kind != "edge":
                    continue
                for r in c.rows[::3]:
                    xb = math.log(r["p_b"])
                    w = v._width(xb)
                    for f in (-0.6, -0.2, 0.2, 0.6):
                        p = math.exp(xb + f * w)
                        if v.ps[0] < p < v.p_dataset:
                            pts.append((p, r["t"] + 11.0))
            self.assertGreater(len(pts), 300, rid)
            on, off = _view(reg, rid), _view(reg, rid)
            off._blend_sides = lambda f, x, t, ib, sides, near, own: own
            keys = [k for k in on.cut_counts if k not in ("corrections", "blend_drops")]
            for p, t in pts:
                a, b = on.state(p, t), off.state(p, t)
                if isinstance(a, tuple) and isinstance(b, tuple):
                    # a term note's scale is its read's own value's denominators, so it follows the blend; the
                    # notes are otherwise the read's own (registration reg-interp-term §4)
                    self.assertEqual([repr(_noscale(n)) for n in a[2]], [repr(_noscale(n)) for n in b[2]], (rid, p, t))
                else:
                    self.assertEqual(type(a), type(b), (rid, p, t))
            self.assertEqual({k: on.cut_counts[k] for k in keys}, {k: off.cut_counts[k] for k in keys}, rid)
            for p, t in pts[:40]:                            # cold against warm
                self.assertEqual(repr(_view(reg, rid).state(p, t)), repr(on.state(p, t)), (rid, p, t))

    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_kinks_named_and_bounded_subset(self):
        """kinkscan's subset finds no violation outside the pinned known ones (PIN_FILE), and none grown past 2× its pin;
        each run prints per table the pins resolved, the unattributed count and the owner-pending count («landing
        blocked until the owner rules»), and whether fall sets were loaded (the E24 pin is sets-only)."""
        reg = mr.load()
        d = _load_pins()
        named = 0
        for rid, (t_lines_at, p_gpa) in SUBSET.items():
            v = _view(reg, rid)
            _ts, ps = ks.full_lines(v)
            p_lines = [min(ps, key=lambda q: abs(q / 1e9 - g)) for g in p_gpa]
            kinks = ks.scan(v, p_lines=t_lines_at, t_lines=p_lines)
            steps = _scan_steps(v)
            for ax in ("P", "T"):                            # the tolerance the pins were written with (to 1e-12: libm)
                self.assertLessEqual(abs(steps[ax] / d["steps"][rid][ax] - 1.0), 1e-12, (rid, ax))
            new, grown, resolved, matched = _against_pins(ks.violations_with_hold(v, kinks, rid)[0], d["pins"][rid], steps)
            tags = {t: sum(p["tag"] == t for p in d["pins"][rid]) for t in sorted(PIN_TAGS)}
            sha = v.record["assemblage"]["sha256"]
            print(f"\n{rid}: {len(matched)} pinned violations seen, {len(resolved)} pins resolved (remove them), "
                  f"unattributed {tags['unattributed']}; fall sets {'loaded' if ma.FALL_SETS_DIR else 'none'}; "
                  f"records {'as pinned' if sha == d['source']['records_sha256'][rid] else 'CHANGED since the pins'}")
            print(f"{rid}: owner-pending {tags['owner-pending']}: landing blocked until the owner rules")
            for p in resolved:
                print(f"   resolved: {p['tag']} {p['line']} P {p['P']:.6g} T {p['T']:.6g} {p['field']} {p['class']}")
            self.assertEqual(new, [], f"{rid}: violations not pinned")
            self.assertEqual([(k, p) for k, p in grown], [], f"{rid}: pinned violations grown past 2× their jump_rel")
            named += len(kinks)
        self.assertGreater(named, 0)                         # the scan sees the named classes it bounds

    def test_pins_load_and_match(self):
        """The fixture's checks, on stand-ins: an unknown tag and a pin without a cite fail the load; a violation one
        step off its pin matches, two steps off is new; one at 2× + ε its pin's jump_rel is grown; a pin unmatched is
        resolved; two equal violations need two pins."""
        import tempfile
        steps = {"P": 0.01, "T": 2.0}
        pin = {"line": "P", "P": 1e9, "T": 1500.0, "field": "dtdp", "class": "unnamed", "jump_rel": 10.0, "width": None,
               "tag": "owner-pending", "cite": "c", "trigger": "t"}
        for bad in ({**pin, "tag": "s read"}, {**pin, "cite": ""}):
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                json.dump({"pins": {"r": [bad]}}, f)
            with self.assertRaises(ValueError):
                _load_pins(f.name)
            os.remove(f.name)
        near = {**pin, "P": 1e9 * math.exp(0.0099)}
        far = {**pin, "P": 1e9 * math.exp(0.0201)}
        self.assertEqual(_against_pins([near], [pin], steps)[0], [])
        self.assertEqual(_against_pins([far], [pin], steps)[0], [far])
        self.assertEqual(len(_against_pins([{**pin, "jump_rel": 20.0001}], [pin], steps)[1]), 1)
        self.assertEqual(_against_pins([{**pin, "jump_rel": 20.0}], [pin], steps)[1], [])
        self.assertEqual(_against_pins([], [pin], steps)[2], [pin])
        self.assertEqual(len(_against_pins([pin, pin], [pin], steps)[0]), 1)
        self.assertEqual(_against_pins([{**pin, "T": 1500.5}], [pin], steps)[0], [{**pin, "T": 1500.5}])   # fixed T exact
        tp = {**pin, "line": "T"}                        # fixed P: to 1e-12, an ulp of libm is not a new kink
        self.assertEqual(_against_pins([{**tp, "P": 1e9 * (1 + 1e-13)}], [tp], steps)[0], [])
        self.assertEqual(len(_against_pins([{**tp, "P": 1e9 * (1 + 1e-11)}], [tp], steps)[0]), 1)
        self.assertTrue(_load_pins()["pins"])            # the shipped fixture loads

    def test_landing_scan_is_the_full_scan(self):
        """The full scan runs once per landing outside the suite (solver/tests/landing_kink_scan.py, a phase-1 task of
        the PC round; directing 10-18). Its scan is every full line in both directions with the full bounds, on the
        same view as the subset; the module is not collected by discover."""
        import inspect
        from solver.tests import landing_kink_scan as lk
        src = inspect.getsource(lk.full)
        for part in ("ks.full_lines(v)", "ks.scan(v, p_lines=ts, t_lines=ps)", "full=True", "_view(reg, rid)"):
            self.assertIn(part, src)
        self.assertFalse(lk.__name__.rsplit(".", 1)[1].startswith("test"))

    def test_landing_scan_exit_code(self):
        """The landing task fails only by main()'s exit code (68 B1 on bb274848): with full() stubbed, one violation
        exits 1 and none exits 0, and the JSON is written both times."""
        import json
        import os
        import tempfile
        from unittest import mock
        from solver.tests import landing_kink_scan as lk
        rid = RECORDS[0]
        with tempfile.TemporaryDirectory() as d, mock.patch.object(lk.mr, "load", return_value=None), \
                mock.patch.object(lk, "_shipped", return_value=True):
            for viol, rc in ((["planted"], 1), ([], 0)):
                out = os.path.join(d, f"scan-{rc}.json")
                with mock.patch.object(lk, "full", return_value=([object()], viol)):
                    self.assertEqual(lk.main([out, rid]), rc)
                self.assertEqual(json.load(open(out)), {rid: {"kinks": 1, "violations": [repr(x) for x in viol]}})


#: the permanent (b′) plant (artifacts pc/ea-f13b/kink-plant.md, blob ade4f642; 68's two conditions): per record one
#: fixed-P line where rev3d's s-off scan had accepted members, read with s off; and the accepted count there at TIP
PLANT = {"silicate_slb_default_bse": 931943836.1517304, "silicate_slb_earth_dmm_wh2005": 693577755.6642308,
         "silicate_slb_mars_khan2022": 666239746.8287351}
PLANT_PIN = {"silicate_slb_default_bse": 3, "silicate_slb_earth_dmm_wh2005": 3, "silicate_slb_mars_khan2022": 3}   # ρ, dT/dP, c_P at each end (kmeas)


class HoldClass(unittest.TestCase):
    """The «interior-end hold (b′)» class (kinkscan.hold; note 8 delta 1 addendum 1, r2 c8a2fab3, 68 README §14–§15):
    at s on on the subset lines every accepted member within its bound and every failing violation an E26 pin; the s-off plant
    accepts its pinned count and the x_r mutant accepts none while still locating members; the shipped AF data and
    census are checked on load."""

    def test_shipped_data_checked_on_load(self):
        import tempfile
        from unittest import mock
        for name in ("kinkscan_af_kinks.json", "kinkscan_af_lines.json", "e26_census.json"):
            ks._SHIPPED.pop(name, None)
            self.assertTrue(ks.shipped(name))
        with tempfile.TemporaryDirectory() as d, mock.patch.object(ks, "DATA", d), mock.patch.dict(ks._SHIPPED, clear=True):
            with self.assertRaises(FileNotFoundError):
                ks.shipped("kinkscan_af_kinks.json")
            for bad in ({"data": {}}, {"provenance": {"af": "x"}, "sha256": "0" * 64, "data": {"r": []}}):
                with open(os.path.join(d, "kinkscan_af_lines.json"), "w") as f:
                    json.dump(bad, f)
                ks._SHIPPED.clear()
                with self.assertRaises(ValueError):
                    ks.shipped("kinkscan_af_lines.json")

    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_s_on_members_bounded(self):
        """At s on on the subset's fixed-P lines: no candidate left for want of an AF lookup, every accepted member within
        HOLD_BOUND, and every C⁰-failing member above the generic T-row bound one of the c1 fixture's E26 or owner-pending pins
        (counted once, 68 §14 (iii))."""
        reg = mr.load()
        pins = _load_pins()
        for rid, (_t_lines, p_gpa) in SUBSET.items():
            v = _view(reg, rid)
            self.assertTrue(v.s_read, rid)
            _ts, ps = ks.full_lines(v)
            p_lines = [min(ps, key=lambda q: abs(q / 1e9 - g)) for g in p_gpa]
            members, no_af = ks.holds(v, ks.scan(v, t_lines=p_lines))
            self.assertEqual(no_af, 0, rid)
            acc = [k for k, h in members if h["accepted"]]
            self.assertEqual([k for k in acc if k["jump_rel"] > ks.HOLD_BOUND[rid][k["field"]]], [], rid)
            # E26's pins, and the owner-pending s-read pins that 68's census amendment 1 (README §18) moves to E26 once the
            # fixture is re-tagged in its own commit
            e26 = [p for p in pins["pins"][rid] if p["tag"] in ("E26", "owner-pending")]
            steps = _scan_steps(v)
            fails = [k for k, h in members if not h["c0"]["ok"]]
            # a failing member that is itself a violation must be one of those pins (counted once, 68 §14 (iii)); one
            # inside the generic bound is no violation and has no pin
            viol = [k for k in fails if k["jump_rel"] > ks.BOUNDS["T row line"][k["field"]]]
            self.assertEqual([k for k in viol if not any(_pin_match(k, p, steps) for p in e26)], [], rid)
            only_op = [k for k in viol if not any(_pin_match(k, p, steps) for p in e26 if p["tag"] == "E26")]
            print(f"\n{rid}: (b′) members {len(members)} at s on, accepted {len(acc)} (within HOLD_BOUND), C⁰-failing "
                  f"{len(fails)} ({len(viol)} above the T-row bound, each a c1 pin; {len(only_op)} only an owner-pending one)")

    @unittest.skipUnless(_shipped(), "no shipped assemblage records with their tables")
    def test_plant_and_xr_mutant(self):
        """The s-off plant (68 §17): unmutated accepted = PLANT_PIN per table; under x_r (1) members located over the
        plant as a whole, (2) each pinned member absent or not accepted, (3) none accepted; no AF lookup missing."""
        reg = mr.load()
        located = 0
        for rid, p in PLANT.items():
            v = _view(reg, rid)
            v.s_read = False
            members, no_af = ks.holds(v, ks.scan(v, t_lines=[p]))
            self.assertEqual(no_af, 0, rid)
            self.assertEqual(sum(h["accepted"] for _k, h in members), PLANT_PIN[rid], rid)
            with ks.xr_mutant():
                w = _view(reg, rid)
                w.s_read = False
                mm, no_af_m = ks.holds(w, ks.scan(w, t_lines=[p]))
            self.assertEqual(no_af_m, 0, rid)
            self.assertEqual([k for k, h in mm if h["accepted"]], [], rid)     # (3) none accepted under x_r
            located += len(mm)
            pinned = [k for k, h in members if h["accepted"]]
            for k in pinned:                       # (2) each pinned member absent under x_r, or a member not accepted
                self.assertFalse(any(m["field"] == k["field"] and abs(m["T"] - k["T"]) <= _scan_steps(v)["T"] and hm["accepted"]
                                     for m, hm in mm), (rid, k))
        self.assertGreater(located, 0)                # (1) the mutant locates members over the plant as a whole (68 §17)


class LandingCensus(unittest.TestCase):
    def test_census_match_moves_the_verdict(self):
        """68 §20 B1: on the landing scan a C⁰-failing (b′) member above the generic T-row bound is no violation when
        every failing field is in E26's census, and is one when it is not (stand-ins for the view, scan and census)."""
        from unittest import mock
        from solver.tests import landing_kink_scan as lk
        rid = RECORDS[0]
        k = {"line": "T", "P": 1e9, "T": 2000.0, "field": "dtdp", "class": "T row line",
             "jump_rel": 10 * ks.BOUNDS["T row line"]["dtdp"], "width": None}
        h = {"member": True, "accepted": False, "curve": 7, "side": "hi", "t_e": 2000.0,
             "c0": {"ok": False, "fields": [{"field": "rho", "ok": True}, {"field": "dtdp", "ok": False},
                                            {"field": "c_p", "ok": False}]}}
        with mock.patch.object(lk, "_view", return_value=object()), \
                mock.patch.object(ks, "full_lines", return_value=([], [])), \
                mock.patch.object(ks, "scan", return_value=[k]), \
                mock.patch.object(ks, "holds", return_value=([(k, h)], 0)):
            with mock.patch.object(ks, "e26_census_match", return_value={"curve": 7}):
                self.assertEqual(lk.full(None, rid)[1], [])                       # matched: counted as E26, not red
            with mock.patch.object(ks, "e26_census_match", return_value=None):
                viol = lk.full(None, rid)[1]
            self.assertEqual([x.get("c0_fails_outside_e26") for x in viol if x.get("class") == ks.HOLD], [["dtdp", "c_p"]])
            self.assertEqual(len([x for x in viol if x["class"] == "T row line"]), 0)   # not also a generic violation


class RunEnd(unittest.TestCase):
    """The truth check's run-end rule (item 5d998d40; 68 ruling on the bump): an open run end's node slope s_n is PCHIP's
    end slope capped at 4|s∞|, s∞ = minmod(PCHIP end, the run's gentlest secant); past the end, s∞'s line plus the bump
    (s_n − s∞)·d(1 − d/L)² within L = END_BUMP·h_end. Mutants: L = 0 (a kink at the node), no cap (the bump turns),
    the linear ramp with its offset (bse 2125 K falls past 21.42 GPa)."""

    XS, YS = [0.0, 1.0, 2.0, 3.0], [10.0, 20.0, 21.0, 22.0]       # a steep first segment: s_e 14.5, s∞ 1, s_n 4

    def _d(self, run, x, h):
        return (run.value(x + h) - run.value(x - h)) / (2.0 * h)

    def test_bump_shape(self):
        run = ma._Run(list(self.XS), list(self.YS), [0, 1, 2, 3], 0)
        self.assertEqual((run.se_lo, run.f_lo, run.m_lo), (14.5, 1.0, 4.0))
        x0, L, h = self.XS[0], run.L_lo, 1e-6
        self.assertEqual(L, ma.END_BUMP * 1.0)
        # the node: the same slope s_n from the run's end segment and from the bump
        inner = (run.value(x0 + h) - run.value(x0)) / h
        outer = (run.value(x0) - run.value(x0 - h)) / h
        self.assertAlmostEqual(inner, 4.0, delta=1e-3)
        self.assertAlmostEqual(outer, 4.0, delta=1e-3)
        # at L: C¹, slope s∞ on both sides
        self.assertAlmostEqual((run.value(x0 - L + h) - run.value(x0 - L)) / h, 1.0, delta=1e-3)
        self.assertAlmostEqual((run.value(x0 - L) - run.value(x0 - L - h)) / h, 1.0, delta=1e-3)
        # beyond L: exactly the line of s∞ (no offset)
        for d in (L, 2 * L, 1.0, 7.0):
            self.assertEqual(run.value(x0 - d), self.YS[0] - 1.0 * d)
        # monotone throughout, the cap at its bound included
        xs = [x0 - 2 * L + i * 2 * L / 400 for i in range(401)]
        self.assertTrue(all(run.value(a) <= run.value(b) for a, b in zip(xs, xs[1:])))
        cap = ma._Run([0.0, 1.0, 2.0], [0.0, 4.0, 5.0], [0, 1, 2], 0)       # s_e 5.5 > 4·s∞ = 4: s_n = 4 exactly
        self.assertEqual(cap.m_lo, 4.0)
        xs = [-0.5 + i * 0.5 / 400 for i in range(401)]
        self.assertTrue(all(cap.value(a) <= cap.value(b) for a, b in zip(xs, xs[1:])))

    def test_gap_end_shared_with_the_bridge(self):
        """An end facing a gap takes PCHIP's end slope clipped against the gap's secant, in its end segment and in the
        bridge alike: C¹ at both run ends. The bridge is the linear join plus each end's bump over L = min(¼ h_end, h/2).
        Mutant: the cubic Hermite bridge (its value at the gap's middle is 4.19375, not 4)."""
        a = ma._Run([0.0, 1.0, 2.0, 3.0], [0.0, 0.1, 1.0, 3.0], [0, 1, 2, 3], 0)   # gentlest secant 0.1: Z's s_n 0.4
        b = ma._Run([4.0, 5.0, 6.0], [5.0, 6.0, 7.0], [4, 5, 6], 0)
        s = (b[1][0] - a[1][-1]) / (b[0][0] - a[0][-1])
        a.set_end(True, s)
        b.set_end(False, s)
        self.assertEqual((a.se_hi, s, a.m_hi), (2.55, 2.0, 2.55))      # PCHIP's end slope, inside the clip's 3|s|
        # planted values: the join's middle (both bumps 0 past L = 0.25), and 0.1 into each end's bump
        self.assertAlmostEqual(ma._bridge(3.5, a, b), 4.0, places=12)
        self.assertAlmostEqual(ma._bridge(3.1, a, b), 3.2 + 0.55 * 0.1 * 0.6 ** 2, places=12)
        self.assertAlmostEqual(ma._bridge(3.9, a, b), 4.8 + 1.0 * 0.1 * 0.6 ** 2, places=12)
        h = 1e-6
        for x, left_f, right_f in ((3.0, a.value, lambda x: ma._bridge(x, a, b)),
                                   (4.0, lambda x: ma._bridge(x, a, b), b.value)):
            self.assertAlmostEqual((left_f(x) - left_f(x - h)) / h, (right_f(x + h) - right_f(x)) / h, delta=1e-4)

    def test_bridge_shape(self):
        """_bridge (68 on the gap-bridge fix, condition 3): the linear join plus each end's bump over L = min(¼ h_end,
        h/2). C¹ at both ends (the end's slope), exactly the join between the bumps, monotone at m = 3s and at m = 0;
        a short gap whose two bumps meet in the middle (L = h/2 from both ends) is C¹ there; a one-node partner's end
        has slope 0."""
        h = 1e-7
        def slope(f, x, side):
            return (f(x + h) - f(x)) / h if side > 0 else (f(x) - f(x - h)) / h
        def monotone(f, lo, hi):
            xs = [lo + (hi - lo) * i / 2000 for i in range(2001)]
            return all(f(p) <= f(q) for p, q in zip(xs, xs[1:]))
        for ma_hi, mb_lo in ((3.0, 3.0), (0.0, 0.0), (3.0, 0.0)):         # in units of the gap secant s = 1
            a = ma._Run([0.0, 1.0, 2.0], [0.0, 1.0, 2.0], [0, 1, 2], 0)
            b = ma._Run([4.0, 5.0, 6.0], [4.0, 5.0, 6.0], [4, 5, 6], 0)
            a.m_hi, b.m_lo = ma_hi, mb_lo
            br = lambda x: ma._bridge(x, a, b)
            self.assertAlmostEqual(slope(br, 2.0, 1), ma_hi, delta=1e-5)
            self.assertAlmostEqual(slope(br, 4.0, -1), mb_lo, delta=1e-5)
            for x in (2.25, 2.6, 3.0, 3.4, 3.75):                         # between the bumps (L = 0.25): the join
                self.assertEqual(br(x), 2.0 + 1.0 * (x - 2.0))
            self.assertTrue(monotone(br, 2.0, 4.0), (ma_hi, mb_lo))
        a = ma._Run([0.0, 4.0], [0.0, 2.0], [0, 1], 0)                     # h_end 4: ¼ h_end = 1 > h/2 = 0.25
        b = ma._Run([4.5, 8.5], [2.5, 4.5], [2, 3], 0)
        a.m_hi, b.m_lo = 3.0, 0.0
        br = lambda x: ma._bridge(x, a, b)
        self.assertAlmostEqual(slope(br, 4.25, -1), slope(br, 4.25, 1), delta=1e-5)
        self.assertAlmostEqual(slope(br, 4.25, 1), 1.0, delta=1e-5)       # both bumps end at the middle with slope s
        self.assertTrue(monotone(br, 4.0, 4.5))
        one = ma._Run([0.0], [1.0], [0], 0)                                # a one-node partner: slope 0 at its end
        b = ma._Run([1.0, 2.0, 3.0], [2.0, 3.0, 4.0], [1, 2, 3], 0)
        b.m_lo = 1.0
        br = lambda x: ma._bridge(x, one, b)
        self.assertAlmostEqual(slope(br, 0.0, 1), 0.0, delta=1e-5)
        self.assertEqual(br(0.5), 1.5)                                     # L = h/2 from the one-node end: the join
        self.assertTrue(monotone(br, 0.0, 1.0))

    def test_cap_by_field(self):
        """END_CAPPED: an open end's node slope is capped at 4|s∞| for ρ only; dT/dP and c_P keep PCHIP's end slope (the
        hold-out truth). Unit: a run whose s_e 5.5 exceeds 4·s∞ = 4. Mutant: the cap on every field."""
        xs, ys = [0.0, 1.0, 2.0], [0.0, 4.0, 5.0]
        self.assertEqual(ma._Run(xs, ys, [0, 1, 2], 0).m_lo, 4.0)
        free = ma._Run(xs, ys, [0, 1, 2], 0, capped=False)
        self.assertEqual(free.m_lo, free.se_lo)
        self.assertGreater(free.m_lo, 4.0)
        self.assertEqual(ma.END_CAPPED, frozenset({"rho"}))

    @unittest.skipUnless(_shipped(), "no shipped assemblage record with its table (the engine branch without records)")
    def test_cap_by_field_wired(self):
        """_runs builds each field's runs with its cap: on the shipped bse record some ρ open end and some dT/dP or c_P
        open end have |s_e| > 4|s∞| > 0, and only ρ's node slope is capped there."""
        v = _view(mr.load(), "silicate_slb_default_bse")
        seen = set()
        for f in ("rho", "dtdp_eq", "c_p"):
            for k in range(len(v.ts)):
                for runs in v._runs(f, k).values():
                    q = runs[0]
                    if len(q[0]) > 1 and q.f_lo != 0.0 and abs(q.se_lo) > 4.0 * abs(q.f_lo) and len(runs) == 1:
                        self.assertEqual(q.m_lo, 4.0 * q.f_lo if f == "rho" else q.se_lo, (f, k))
                        seen.add(f)
        self.assertIn("rho", seen)
        self.assertTrue(seen & {"dtdp_eq", "c_p"})

    def test_one_node_gap_partner(self):
        """An end whose gap's far side is a one-node run (slope 0 in the bridge) keeps its own slope, clipped against
        the gap's secant, so the bridge's clip is a no-op and the read is C¹ there (68 z3)."""
        a = ma._Run([0.0, 1.0, 2.0], [0.0, 1.0, 2.0], [0, 1, 2], 0)     # s_n 1
        b = ma._Run([3.0], [2.1], [3], 0)
        s = (b[1][0] - a[1][-1]) / (b[0][0] - a[0][-1])
        a.set_end(True, s, keep=True)
        self.assertAlmostEqual(a.m_hi, 3 * s, places=12)                # 1 clipped to 3·0.1
        h, x = 1e-6, 2.0
        self.assertAlmostEqual((a.value(x) - a.value(x - h)) / h, (ma._bridge(x + h, a, b) - ma._bridge(x, a, b)) / h,
                               delta=1e-4)

    #: the ρ-monotone cases each run-end variant failed (rhomono on the three records): (record, T row, P range GPa)
    #: - bse 2100 K, 19–25 GPa: dd3e58a7's steep first segment (22.49 → 23.62 GPa), and the linear ramp's offset
    #:   carried past 21.42 GPa at 2125 K (−0.2 % to −1.4 %);
    #: - bse 900 K, 10–14 GPa: a loop cell's end segment at 11.93 GPa, 925 K, under L = 0 and an end-two s∞ (−1e-4), and
    #:   under a sharper ρ blend (BLEND_SHARP ρ 2: −5e-3);
    #: - dmm 1000 K, 11–14 GPa: 12.52 GPa, 1025 K, under BLEND_SHARP ρ 2 (−1.1e-3; 68 on BLEND_SHARP, condition 1)
    CASES = (("silicate_slb_default_bse", 2100.0, 19.0, 25.0), ("silicate_slb_default_bse", 900.0, 10.0, 14.0),
             ("silicate_slb_earth_dmm_wh2005", 1000.0, 11.0, 14.0))

    @unittest.skipUnless(_shipped(), "no shipped assemblage record with its table (the engine branch without records)")
    def test_named_rho_cases(self):
        """On each case's line (the cell centres' T above the row), ρ at consecutive cell centres rises wherever the
        table rises (Envelope's test, on these lines). Mutants: L = 0, no cap, the linear ramp, s∞ end-two, κ_ρ = 2."""
        reg = mr.load()
        for rid, row, lo, hi in self.CASES:
            v = _view(reg, rid)
            ib = max(i for i, t in enumerate(v.ts) if t <= row)
            t, last, bad = 0.5 * (v.ts[ib] + v.ts[ib + 1]), None, []
            for ia in range(len(v.ps) - 1):
                if not lo * 1e9 <= v.ps[ia] <= hi * 1e9:
                    continue
                got = v._solid(math.sqrt(v.ps[ia] * v.ps[ia + 1]), t)
                if not isinstance(got, tuple):
                    last = None
                    continue
                if last is not None:
                    cols = [[(v._cell(j, k) or {}).get("rho") for k in (ib, ib + 1)] for j in (ia - 1, ia, ia + 1)]
                    if all(p and q and r and p < q < r for p, q, r in zip(*cols)) and got[0] < last * (1.0 - 1e-5):
                        bad.append((v.ps[ia], got[0] / last - 1.0))
                last = got[0]
            self.assertEqual(bad, [], (rid, row))


if __name__ == "__main__":
    unittest.main()
