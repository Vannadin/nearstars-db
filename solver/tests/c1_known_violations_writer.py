# c1 부분 꺾임 조사의 알려진 위반 고정 목록을 쓰는 도구 — 시험 묶음 밖(파일 이름이 test_ 아님), TIP 의 출하 기록·s 켬·낙하 구간 세트로 훑고 귀속 파일의 꼬리표를 하나씩 붙임
"""Writes solver/tests/data/c1_known_violations.json (68 README §7–§12; directing 10-23).

Run from the worktree root, with the records' fall sets loaded (the pins' source; 68 §7 (4)):
  NS_FALL_SETS=<sets dir> <solver venv>/python -m solver.tests.c1_known_violations_writer ATTRIBUTION.json [OUT.json]
ATTRIBUTION.json: {record: [{line, P, T, field, class, tag, cite, trigger, note, …}]}, one entry per violation, made
outside the suite from the attribution runs (artifacts pc/ea-f13b/c1pin/fixture-tags.json). The writer re-runs the
subset scan exactly as test_kinks_named_and_bounded_subset does and STOPs unless every violation has an entry with the same
line, P, T, field and class (bit for bit, the same run; a kink found twice has two, tagged alike) and every entry is used, every tag is in
PIN_TAGS, every record reads s on, and a fall-set file is loaded for every record."""
import json
import os
import subprocess
import sys

from solver import material_assemblage as ma, material_registry as mr
from solver.tests import kinkscan as ks
from solver.tests.test_assemblage_c1 import PIN_FILE, PIN_TAGS, SUBSET, _scan_steps, _shipped, _view

KEYS = ("line", "P", "T", "field", "class")
#: stage A's push is held while any owner-pending pin remains (68 §12 condition 2; directing checks the count)
BLOCK = ("stage A does not push while any owner-pending pin remains; directing checks the count before the push, as "
         "with the expected-red list; owner-pending → s-read, or removing those pins, is its own audited commit citing "
         "the owner's ruling")


def main(argv):
    attr, out = argv[0], (argv[1] if len(argv) > 1 else PIN_FILE)
    if not _shipped():
        sys.exit("STOP: no shipped assemblage records with their tables")
    if not ma.FALL_SETS_DIR:
        sys.exit("STOP: NS_FALL_SETS is not set; the pins come from the run with the records' fall sets")
    reg, a = mr.load(), json.load(open(attr, encoding="utf-8"))
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    src = {"engine": head, "records_sha256": {}, "s_read": {}, "fall_sets": {}, "attribution_file": os.path.basename(attr),
           "attribution_blob": subprocess.run(["git", "hash-object", attr], capture_output=True, text=True,
                                              check=True).stdout.strip()}
    pins, steps = {}, {}
    for rid, (t_lines_at, p_gpa) in SUBSET.items():
        v = _view(reg, rid)
        if not getattr(v, "s_read", False):
            sys.exit(f"STOP: {rid} does not read s on")
        f = os.path.join(ma.FALL_SETS_DIR, f"{rid}.json")
        if not os.path.exists(f):
            sys.exit(f"STOP: no fall-set file for {rid} in NS_FALL_SETS")
        _ts, ps = ks.full_lines(v)
        p_lines = [min(ps, key=lambda q: abs(q / 1e9 - g)) for g in p_gpa]
        vi = ks.violations(ks.scan(v, p_lines=t_lines_at, t_lines=p_lines), rid)
        left, rows = list(a.get(rid, [])), []
        for k in vi:
            m = [e for e in left if all(e[x] == k.get(x) for x in KEYS)]
            if not m or len({(e["tag"], e["cite"], e["trigger"]) for e in m}) != 1:   # a kink the scan finds twice
                sys.exit(f"STOP: {rid}: {len(m)} attribution entries (or differing tags) for violation {k}")
            e = m[0]
            left.remove(e)
            if e["tag"] not in PIN_TAGS or not e.get("cite") or not e.get("trigger"):
                sys.exit(f"STOP: {rid}: entry {e} has an unknown tag or no cite / trigger")
            rows.append({**{x: k[x] for x in KEYS}, "jump_rel": k["jump_rel"], "width": k["width"],
                         **{x: e[x] for x in ("tag", "cite", "trigger", "note")}})
        if left:
            sys.exit(f"STOP: {rid}: {len(left)} attribution entries match no violation")
        pins[rid], steps[rid] = rows, _scan_steps(v)
        src["records_sha256"][rid] = v.record["assemblage"]["sha256"]
        src["s_read"][rid] = True
        src["fall_sets"][rid] = subprocess.run(["git", "hash-object", f], capture_output=True, text=True,
                                               check=True).stdout.strip()
    counts = {rid: {t: sum(p["tag"] == t for p in rows) for t in sorted(PIN_TAGS)} for rid, rows in pins.items()}
    doc = {"what": "c1 subset's known violations, one owner tag each (68 README §7–§12)",
           "landing_block": BLOCK,
           "tolerance": "the scan's own coarse step on the scanned coordinate (kinkscan.scan: ln P over n steps to "
                        "p_dataset on fixed-T lines, T over max(20·rows, 400) on fixed-P lines); the fixed coordinate "
                        "exact; not fitted to the list",
           "source": src, "steps": steps, "counts": counts, "pins": pins}
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    for rid, c in counts.items():
        print(rid, {t: n for t, n in c.items() if n})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
