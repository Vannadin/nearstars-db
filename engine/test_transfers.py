# 전이 기록(transfers.py) 규칙 자기검증 — 3040 K 모양이 거절되는지, 그리고 맞는 기록은 통과하는지 양쪽 다
"""Fire transfers.py's three rules in both directions.

    python3 engine/test_transfers.py

Each rule is shown to refuse the case it exists for **and** to pass the case it must not touch — a
check that always fires is a constant (derivation-discipline §10). The case this module was built for
is spelled out as a body file: Mars declaring Earth's 3040 K.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transfers  # noqa: E402
from transfers import Transfer, TransferError, check_body  # noqa: E402

EARTH = {"name": "Earth", "inputs": {"age_gyr": 4.54, "potential_temperature": 1600.0,
                                     "core_initial_temperature": 4800.0,
                                     "mantle_initial_potential_temperature": 3040.0}}
GOOD = dict(from_body="Earth", form="printed", kind="state", grade="analog")


def rec(field, anchor="earth.yaml@«age_gyr: 4.54»", **kw):
    d = {"field": field, "anchor": anchor, **GOOD}
    d.update(kw)
    return d


def main() -> int:
    fails: list[str] = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)

    def refused(doc, why):
        try:
            check_body(doc, {"Earth": EARTH})
        except TransferError as e:
            return str(e)
        fails.append(f"{why}: was accepted, must be refused")
        return ""

    def accepted(doc, why):
        try:
            check_body(doc, {"Earth": EARTH})
            return True
        except TransferError as e:
            fails.append(f"{why}: refused — {e}")
            return False

    # ① the 3040 case, both shapes it can take
    mars = {"name": "Mars", "inputs": {"mantle_initial_potential_temperature": 3040.0}}
    msg = refused(mars, "1a: Earth's 3040 K in Mars with no record")
    ok("neither side records" in msg, f"1a: wrong reason — {msg}")
    mars["transfers"] = [rec("mantle_initial_potential_temperature", form="derived")]
    msg = refused(mars, "1b: Earth's 3040 K in Mars recorded as derived state")
    ok("does not travel" in msg, f"1b: wrong reason — {msg}")

    # ② the same rule passes what it must: a printed state with an analog record, either side recording
    mars2 = {"name": "Mars", "inputs": {"core_initial_temperature": 4800.0},
             "transfers": [rec("core_initial_temperature")]}
    accepted(mars2, "2a: printed state, analog, recorded on the receiving side")
    earth_rec = dict(EARTH, transfers=[{"field": "core_initial_temperature", "from_body": "Mars",
                                        **{k: v for k, v in GOOD.items() if k != "from_body"},
                                        "anchor": "mars.yaml@«name: Mars»"}])
    try:
        check_body({"name": "Mars", "inputs": {"core_initial_temperature": 4800.0}}, {"Earth": earth_rec})
    except TransferError as e:
        fails.append(f"2b: record on the giving side must satisfy rule (i) — {e}")
    # and a value nobody else declares needs no record at all
    accepted({"name": "Mars", "inputs": {"mantle_initial_potential_temperature": 4021.0}},
             "2c: Mars's own 4021 K equals no other body's value")
    # equality is per key: the same number under another key is not a transfer
    accepted({"name": "X", "inputs": {"something_else": 4.54}}, "2d: same number, different key")

    # ③ the vocabulary refuses what is not in it, and grade follows kind
    for kw, why in [({"form": "printed-ish"}, "3a: unknown form"),
                    ({"kind": "constant"}, "3b: unknown kind"),
                    ({"grade": "measured"}, "3c: a state carries analog, not measured"),
                    ({"kind": "parameter", "grade": "analog"}, "3d: a parameter carries calibrated"),
                    ({"anchor": "earth.yaml line 17"}, "3e: anchor must be file@«phrase»")]:
        try:
            Transfer(**rec("age_gyr", **kw))
            fails.append(f"{why}: accepted")
        except TransferError:
            pass
    # a derived parameter is allowed — K_T is the case
    try:
        Transfer("K_T", "Earth", "derived", "parameter", "calibrated", "mantle_flux.py@«K_T = KAPPA_T * RHO_M * C_PM»")
    except TransferError as e:
        fails.append(f"3f: a derived parameter must pass — {e}")
    # an unknown key in a yaml entry is refused, not ignored
    try:
        transfers.parse({"name": "X", "transfers": [dict(rec("age_gyr"), demonstrated="Earth")]})
        fails.append("3g: unknown yaml key accepted")
    except TransferError:
        pass

    # ④ the code-default registry names real attributes, and the two known derived ones are marked so
    problems = transfers.check_code_defaults()
    ok(not problems, f"4a: {problems}")
    derived = {t.field for t in transfers.CODE_DEFAULTS if t.form == "derived"}
    ok(derived == {"K_T", "K_B"}, f"4b: derived code defaults should be K_T and K_B, got {derived}")
    ok(all(t.kind == "parameter" for t in transfers.CODE_DEFAULTS), "4c: code defaults are parameters")

    # ⑤ the real body files load under the rules — wiring, not answers
    others = transfers.load_others()
    for name, doc in others.items():
        try:
            check_body(doc, others)
        except TransferError as e:
            fails.append(f"5: {name} — {e}")
    ok({t.field for t in transfers.parse(others["Mars"])} >= {"potential_temperature", "core_initial_temperature"},
       "5: mars.yaml must record its two Earth temperatures")

    for f in fails:
        print(f"  [FAIL] {f}")
    print(f"test_transfers: {'PASS' if not fails else 'FAIL'} ({len(fails)} failures)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
