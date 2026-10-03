# C159 시험 — 구조 표 방아쇠가 러너가 읽는 것만 보고(설명 편집엔 안 낡음), 실제 변경엔 서고, 표 없는 열진화 몸은 게이트에서 FAIL
"""python3 engine/test_table_triggers.py — prereg-c159-table-trigger-reads (e0ab5682) acceptance 1, 2, 4 and 4b (light; no solve)."""
from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import structure_grid as sg  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


chain_text = (HERE / "chain.yaml").read_text(encoding="utf-8")
base = sg.chain_reads_digest()


def _digest_of(text: str) -> str:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "chain.yaml"
        p.write_text(text, encoding="utf-8")
        return sg.chain_reads_digest(p)


check("수락 1 — 원본 사본의 투영 해시가 원본과 같음(사본 경로가 바뀌어도)", _digest_of(chain_text) == base)
note_edit = chain_text.replace("    note: >\n", "    note: >\n      C159 시험 — 설명 한 줄.\n", 1)
check("수락 1 — 노드 note 만 고치면 투영 해시가 안 움직임", note_edit != chain_text and _digest_of(note_edit) == base)
layer_edit = re.sub(r'(\n    layer: )"([^"]*)"', r'\1"\2 (C159 시험)"', chain_text, count=1)
check("수락 1 — 노드 layer 만 고치면 투영 해시가 안 움직임", layer_edit != chain_text and _digest_of(layer_edit) == base)
recipe_edit = chain_text.replace("    recipe: interior-structure-methodology\n", "    recipe: interior-structure-methodology-c159\n", 1)
check("수락 2a — 노드 recipe 를 고치면 투영 해시가 움직임", recipe_edit != chain_text and _digest_of(recipe_edit) != base)
edge_edit = re.sub(r"(kind: )requires", r"\1selects", chain_text, count=1)
check("수락 2a — 간선 kind 를 고치면 투영 해시가 움직임", edge_edit != chain_text and _digest_of(edge_edit) != base)

# 수락 2b · 2c — eos.py 는 바이트 칸에서 빠지고 AST 해시(코드 칸)만 남는다
check("규칙 2 — eos.py 는 바이트 칸에 없고 코드 칸에 있다", "eos.py" not in sg.BYTE_FILES and "eos.py" in sg.CODE_FILES)
eos_text = (HERE / "eos.py").read_text(encoding="utf-8")
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "eos.py"
    p.write_text(eos_text, encoding="utf-8")
    d0 = sg._code_digest(p)
    p.write_text(eos_text + "\n# C159 시험 — 주석 한 줄\n", encoding="utf-8")
    d_comment = sg._code_digest(p)
    p.write_text(eos_text.replace("GPA = 1e9", "GPA = 1.0000001e9", 1), encoding="utf-8")
    d_const = sg._code_digest(p)
check("수락 2c — eos.py 주석만 고치면 코드 해시가 안 움직임", d_comment == d0)
check("수락 2b — eos.py 상수를 고치면 코드 해시가 움직임(게이트 다시 풀기)", "GPA = 1e9" in eos_text and d_const != d0)

# 수락 4b — reference_adiabats.json 은 데이터 방아쇠: 바이트가 바뀌면 데이터 움직임
check("규칙 1b — reference_adiabats.json 이 바이트(데이터) 칸에 있다", "reference_adiabats.json" in sg.BYTE_FILES)
then = {"declared": {}, "code": {}, "bytes": {"reference_adiabats.json": "aaaa"}, "chain_reads": base,
        "sulphur_fixings": None, "mantle_table": None}
now = {**then, "bytes": {"reference_adiabats.json": "bbbb"}}
data, code = sg._moved(then, now)
check("수락 4b — reference_adiabats.json 바이트가 바뀌면 데이터 움직임(즉시 낡음)", data == ["bytes.reference_adiabats.json"] and not code,
      f"{data} / {code}")
old_form = {"declared": {}, "code": {}, "bytes": {"eos.py": "x", "chain.yaml": "y"}, "sulphur_fixings": None, "mantle_table": None}
data, code = sg._moved(old_form, {**then})
check("규칙 4 — 옛 꼴 방아쇠(chain.yaml 바이트 · chain_reads 없음)는 데이터 움직임으로 이름 댄다",
      "bytes.chain.yaml" in data and "chain_reads" in data, f"{data} / {code}")

# 수락 4 — 열진화 입력을 선언한 몸은 표가 있어야 한다: 빈 표 폴더에서 셋 다 FAIL
check("규칙 3 — 열진화 입력을 선언한 출하 몸 = earth · mars · venus", sg.history_bodies() == ["earth", "mars", "venus"],
      str(sg.history_bodies()))
import contextlib  # noqa: E402
import io  # noqa: E402

saved = sg.GRID_DIR
with tempfile.TemporaryDirectory() as d:
    sg.GRID_DIR = Path(d)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            bad = sg.check_all()
    finally:
        sg.GRID_DIR = saved
out = buf.getvalue()
check("수락 4 — 표 폴더가 비면 --check 가 세 몸을 이름 대며 FAIL", bad == 3 and all(f"[FAIL] {b} —" in out for b in ("earth", "mars", "venus")),
      f"bad {bad}")
present = {p.stem for p in saved.glob("*.json")}
missing = [b for b in sg.history_bodies() if b not in present]
print(f"  [기록] 지금 트리에서 표 없는 열진화 몸: {missing} (C159 수락 4 의 «전» 상태 — 금성은 이식의 PC 재굳힘에서 짓는다)")

# C159 메모 1 — 읽기 가드는 check_all 안에서 **코드가 움직인 표에서만** 돈다(데이터만 움직이면 안 돈다)
import json  # noqa: E402
import run  # noqa: E402

_body, _ = run.load_body(sg.BODIES_DIR / "earth.yaml")
_now = sg.triggers(_body.inputs)


def _check_with(trig, reads):
    saved_dir, saved_rc = sg.GRID_DIR, sg._recheck
    with tempfile.TemporaryDirectory() as d:
        sg.GRID_DIR = Path(d)
        (Path(d) / "earth.json").write_text(json.dumps({"body": "Earth", "t_pot": [1.0], "points": [{}], "triggers": trig}),
                                            encoding="utf-8")
        sg._recheck = lambda doc, body: (0.0, "stub")
        sg._READS.clear(); sg._READS.update(reads)
        n0 = sg.GUARD_RUNS[0]
        buf2 = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf2):
                sg.check_all()
        finally:
            sg.GRID_DIR, sg._recheck = saved_dir, saved_rc
            sg._READS.clear()
    return sg.GUARD_RUNS[0] - n0, buf2.getvalue()


_code_moved = {**_now, "code": {**_now["code"], "eos.py": "0000000000000000"}}
runs, out = _check_with(_code_moved, {"reference_adiabats.json", "chain.yaml", "bodies/earth.yaml"})
check("메모 1 — 코드가 움직인 표에서 읽기 가드가 돈다(목록 안 읽기면 통과)", runs == 1 and "읽기 가드" not in out, f"runs {runs}")
runs, out = _check_with(_code_moved, {"reference_adiabats.json", "fake_new_table.csv"})
check("메모 1 — 코드 움직임 + 방아쇠 밖 데이터 읽기 → 읽기 가드 FAIL", runs == 1 and "읽기 가드" in out and "fake_new_table.csv" in out,
      f"runs {runs}")
_data_moved = {**_now, "bytes": {**_now["bytes"], "reference_adiabats.json": "0000000000000000"}}
runs, out = _check_with(_data_moved, {"fake_new_table.csv"})
check("메모 1 음성 — 데이터만 움직인 표에선 읽기 가드가 안 돈다(이미 낡음 FAIL)", runs == 0 and "데이터 방아쇠" in out, f"runs {runs}")

print(f"  test_table_triggers — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
