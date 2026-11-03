# check_mass_formula(M1 엔진 쪽)의 시험 — 실제 트리는 PASS, 대조 일곱(목록 r 변경 · 목록에서 빠진 불일치 · 고침 표지+비지 않은 목록 · 별칭 생성자 · getattr 생성자 · 데이터셋 둘 · 경로 위 목록 밖 클래스)은 각각 빨강
"""python3 scripts/test_check_mass_formula.py     (the gate venv: BurnMan 2.1.0)

Each control is a temp copy of engine/*.py, engine/bodies/ and scripts/ with one plant, checked in its own process
(`check_mass_formula.py --root TMP`), so the plant's import of mantle_composition is fresh."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_mass_formula.py"
fails = []


def ok(cond, label):
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if not cond:
        fails.append(label)


def run(root):
    p = subprocess.run([sys.executable, str(CHECK), "--root", str(root)], capture_output=True, text=True)
    return p.returncode, p.stdout


def tree(plant):
    tmp = Path(tempfile.mkdtemp(prefix="m1-"))
    (tmp / "engine").mkdir()
    for f in (ROOT / "engine").glob("*.py"):
        shutil.copy2(f, tmp / "engine" / f.name)
    shutil.copytree(ROOT / "engine" / "bodies", tmp / "engine" / "bodies")
    (tmp / "scripts").mkdir()
    shutil.copy2(ROOT / "scripts" / "mass_allowlist.json", tmp / "scripts" / "mass_allowlist.json")
    (tmp / "solver").mkdir()
    plant(tmp)
    return tmp


def appended(text):
    def plant(t):
        f = t / "engine" / "mantle_composition.py"
        f.write_text(f.read_text(encoding="utf-8") + text, encoding="utf-8")
    return plant


def new_file(name, text):
    def plant(t):
        (t / "engine" / name).write_text(text, encoding="utf-8")
    return plant


def edit_list(fn):
    def plant(t):
        f = t / "scripts" / "mass_allowlist.json"
        al = json.loads(f.read_text(encoding="utf-8"))
        fn(al)
        f.write_text(json.dumps(al, indent=1) + "\n", encoding="utf-8")
    return plant


CONTROLS = [
    ("C5b a listed r changed", edit_list(lambda al: al["entries"][0].update(r=al["entries"][0]["r"] * 1.001)), "listed ("),
    ("C5c a listed entry removed", edit_list(lambda al: al["entries"].pop(0)), "unlisted mismatch"),
    ("C5d marker True with a non-empty list", appended("\nMASS_FROM_FORMULA = True\n"), "MASS_FROM_FORMULA is True"),
    ("B2 an alias-form constructor", new_file("zz_plant.py", "from burnman.minerals import SLB_2022 as Q\n\n\ndef f():\n"
                                                              "    return Q.almandine()\n"), "unlisted mismatch"),
    ("B2 a getattr constructor", new_file("zz_plant.py", "from burnman import minerals as m\n\n\ndef f(n):\n"
                                                        "    return getattr(m.SLB_2022, n)()\n"), "dynamic BurnMan constructor"),
    ("n1 two datasets in mantle_composition", appended("\nfrom burnman import minerals as _m2\n_X = _m2.SLB_2011\n"),
     "minerals datasets"),
    ("n4 a class off the list on the engine's route", appended(
        "\n_orig_phase = _phase\n\n\ndef _phase(key, x=None):\n    from burnman import minerals\n"
        "    getattr(minerals.SLB_2022, \"periclase\")()\n    return _orig_phase(key, x)\n"), "runtime: class"),
]


def main():
    rc, out = run(ROOT)
    ok(rc == 0 and out.strip().splitlines()[-1].startswith("M1: PASS"), f"the tree: {out.strip().splitlines()[-1]}")
    for label, plant, want in CONTROLS:
        t = tree(plant)
        try:
            rc, out = run(t)
        finally:
            shutil.rmtree(t)
        hit = [ln for ln in out.splitlines() if "[FAIL] M1" in ln and want in ln]
        ok(rc == 1 and bool(hit), f"{label} → red ({hit[0].strip()[:110] if hit else out.strip()[-120:]})")
    print("모두 통과" if not fails else f"{len(fails)} 실패")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
