# 입력 선언 차선(C136)의 픽스처 — 후크의 import 거르기 셋 · 표류 · 빠진 단계 · also 고르기
import json
import os
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate_step_inputs as gsi


def _hooked(tmp: pathlib.Path, code: str) -> list[dict]:
    """scratch 디렉터리에서 후크를 켠 파이썬 하나를 돌리고 그 기록을 돌려준다 (raw 포함)."""
    log = tmp / "reads.jsonl"
    log.unlink(missing_ok=True)
    env = dict(os.environ, GATE_READS_LOG=str(log), GATE_READS_ROOT=str(tmp), GATE_READS_RAW="1",
               GATE_STEP="fixture", PYTHONPATH=str(HERE / "gate_reads"), PYTHONDONTWRITEBYTECODE="1")
    subprocess.run([sys.executable, "-c", code], cwd=tmp, env=env, check=True)
    return [json.loads(l) for l in log.read_text().splitlines() if l.strip()]


def _scratch() -> pathlib.Path:
    tmp = pathlib.Path(tempfile.mkdtemp()).resolve()
    (tmp / "scratch_mod.py").write_text("X = 1\n")
    (tmp / "table.md").write_text("| a |\n")
    (tmp / "loader_mod.py").write_text("DATA = open('table.md').read()\n")
    return tmp


def _kept(recs, path):
    return [r for r in recs if r["path"] == path and r["kind"] == "open" and not r.get("dropped")]


def _raw(recs, path):
    return [r for r in recs if r["path"] == path and r["kind"] == "open" and r.get("dropped")]


def test_import_only_absent():
    tmp = _scratch()
    recs = _hooked(tmp, "import scratch_mod")
    assert _raw(recs, "scratch_mod.py"), "open_code event for the import must fire (raw)"
    assert not _kept(recs, "scratch_mod.py")


def test_import_and_open_once():
    tmp = _scratch()
    recs = _hooked(tmp, "import scratch_mod; open('scratch_mod.py').read()")
    assert _raw(recs, "scratch_mod.py")
    assert len(_kept(recs, "scratch_mod.py")) == 1
    assert any(r["kind"] == "leak" and r["path"] == "scratch_mod.py" for r in recs)   # 출구 그물이 이름을 댄다


def test_import_time_data_read_recorded():
    tmp = _scratch()
    recs = _hooked(tmp, "import loader_mod")
    assert len(_kept(recs, "table.md")) == 1, "import frames below must not hide a data read"
    assert not _kept(recs, "loader_mod.py")


def test_main_script_not_recorded():
    tmp = _scratch()
    (tmp / "main_x.py").write_text("import scratch_mod\n")
    log = tmp / "reads.jsonl"
    env = dict(os.environ, GATE_READS_LOG=str(log), GATE_READS_ROOT=str(tmp), GATE_READS_RAW="1",
               GATE_STEP="fixture", PYTHONPATH=str(HERE / "gate_reads"), PYTHONDONTWRITEBYTECODE="1")
    subprocess.run([sys.executable, "main_x.py"], cwd=tmp, env=env, check=True)
    recs = [json.loads(l) for l in log.read_text().splitlines() if l.strip()]
    assert _raw(recs, "main_x.py"), "the main script's open must fire (raw)"
    assert not _kept(recs, "main_x.py") and not _kept(recs, "scratch_mod.py")


def test_glob_pattern_recorded_not_its_walk():
    tmp = _scratch()
    (tmp / "sub").mkdir()
    recs = _hooked(tmp, "import glob; glob.glob('sub/*.md')")
    assert any(r["kind"] == "glob" and r["path"] == "sub/*.md" for r in recs)
    assert not any(r["kind"] == "list" for r in recs)


def _lists(recs, path):
    return [r for r in recs if r["kind"] == "list" and r["path"] == path and not r.get("dropped")]


def test_c147_metadata_walk_dropped():
    # L-meta: importlib.metadata 가 sys.path 를 훑는 나열은 import 기계 — 기록 안 됨, raw 에는 dropped
    tmp = _scratch()
    (tmp / "sub").mkdir()
    recs = _hooked(tmp, "import sys, importlib.metadata as m; sys.path.insert(0, 'sub')\n"
                        "try: m.version('no-such-dist-c147')\nexcept Exception: pass")
    assert not _lists(recs, "sub")
    assert any(r["kind"] == "list" and r["path"] == "sub" and r.get("dropped") for r in recs)


def test_c147_pathlib_glob_is_a_pattern():
    # L-pathlib: glob/rglob 아래의 나열은 그 패턴 하나 — `list d` 없음. glob 프레임 없는 iterdir 는 `list d`
    tmp = _scratch()
    (tmp / "d").mkdir()
    (tmp / "d" / "x.py").write_text("")
    recs = _hooked(tmp, "import pathlib; list(pathlib.Path('d').glob('*.py')); list(pathlib.Path('d').rglob('*.md'))")
    assert any(r["kind"] == "glob" and r["path"] == "d/*.py" for r in recs)
    assert any(r["kind"] == "glob" and r["path"] == "d/**/*.md" for r in recs)
    assert not _lists(recs, "d")
    recs = _hooked(tmp, "import pathlib; list(pathlib.Path('d').iterdir())")
    assert _lists(recs, "d") and _lists(recs, "d")[0].get("by", "").startswith("pathlib.py:")


def test_c147_plain_listdir_keeps_dir_star():
    # L-plain: 단계 자신의 os.listdir 는 그대로 `list d` 이고 `d/*` 를 요구한다 (동결 그대로)
    tmp = _scratch()
    (tmp / "d").mkdir()
    recs = _hooked(tmp, "import os; os.listdir('d')")
    got = _lists(recs, "d")
    assert got and got[0]["by"] == "<string>:<module>"
    table = {"s": {"globs": [], "hand": False}}
    assert gsi.drift([dict(got[0], step="s")], table, ["s"])
    assert gsi.drift([dict(got[0], step="s")], {"s": {"globs": ["d/*"], "hand": False}}, ["s"]) == []


def test_git_show_recorded():
    tmp = _scratch()
    recs = _hooked(tmp, "import subprocess; subprocess.run(['git', 'show', 'HEAD:table.md'], capture_output=True)")
    assert any(r["kind"] == "git" and r["path"] == "table.md" for r in recs)


def test_git_ls_files_pathspec_recorded():
    tmp = _scratch()
    recs = _hooked(tmp, "import subprocess; subprocess.run(['git', 'ls-files', '*.md'], capture_output=True)")
    assert any(r["kind"] == "gitlist" and r["path"] == "*.md" for r in recs)


def test_drift_git_pathspec_crosses_directories():
    # git 의 `*.md` 는 모든 깊이의 .md — 한 층 글롭 `*.md` 로는 못 덮고 `**.md` 로 덮는다
    assert gsi.drift([_rec("s", "*.md", kind="gitlist")], {"s": {"globs": ["**.md"], "hand": False}}, ["s"]) == []
    assert gsi.drift([_rec("s", "*.md", kind="gitlist")], {"s": {"globs": ["*.md"], "hand": False}}, ["s"])
    assert gsi.drift([_rec("s", "*", kind="gitlist")], {"s": {"globs": ["**.md"], "hand": False}}, ["s"])


def test_glob_pattern_without_pass_class_names_needs_nothing():
    table = {"s": {"globs": [], "hand": False}}
    assert gsi.drift([_rec("s", "engine/bodies/*.yaml", kind="glob")], table, ["s"]) == []
    assert gsi.drift([_rec("s", "docs/reference/*.md", kind="glob")], table, ["s"])


def test_glob_star_stays_in_one_directory():
    assert gsi.matches("docs/x.md", ["docs/*"]) and not gsi.matches("docs/a/x.md", ["docs/*"])
    assert gsi.matches("docs/a/x.md", ["**.md"]) and gsi.matches("x.md", ["**.md"])


def _rec(step, path, kind="open"):
    return {"step": step, "kind": kind, "path": path}


def test_drift_undeclared_fails_declared_passes():
    table = {"s": {"globs": ["engine/interior-core.md"], "hand": False}}
    assert gsi.drift([_rec("s", "engine/interior-core.md")], table, ["s"]) == []
    fails = gsi.drift([_rec("s", "docs/x.md")], table, ["s"])
    assert fails and "s read docs/x.md, not declared" in fails[0]


def test_drift_ignores_non_pass_class():
    table = {"s": {"globs": [], "hand": False}}
    assert gsi.drift([_rec("s", "engine/bodies/mars.yaml")], table, ["s"]) == []


def test_drift_listing_needs_glob():
    table = {"s": {"globs": [], "hand": False}}
    assert gsi.drift([_rec("s", "docs", kind="list")], table, ["s"])
    table = {"s": {"globs": ["docs/*"], "hand": False}}
    assert gsi.drift([_rec("s", "docs", kind="list")], table, ["s"]) == []


def test_missing_step_fails():
    table = {"s": {"globs": [], "hand": False}}
    fails = gsi.drift([], table, ["s", "t"])
    assert fails and "«t» is in check.sh but not in" in fails[0]


def test_also_picks_reader_and_names_missing():
    table = {"core_items": {"globs": ["engine/interior-core.md"], "hand": False},
             "other": {"globs": ["docs/*.md"], "hand": False}}
    hit, missing = gsi.also(["engine/interior-core.md"], table, ["core_items", "other"])
    assert hit == ["core_items"] and missing == []
    hit, missing = gsi.also(["engine/interior-core.md"], table, ["core_items", "other", "new"])
    assert missing == ["new"]
    assert gsi.also(["plans/p.md"], table, ["core_items", "other"]) == ([], [])
    # quick 여덟은 어차피 돈다 — also 에 안 든다
    assert gsi.also(["engine/interior-core.md"], table, ["core_items"], quick=["core_items"]) == ([], [])


def test_quick_steps_parsed():
    q = gsi.quick_steps()
    assert len(q) == 8 and "engine/check_refs.py" in q


def test_every_check_sh_step_declared():
    table = gsi.load()
    missing = [n for n in gsi.step_names() if n not in table]
    extra = [n for n in table if n not in gsi.step_names()]
    assert not missing, f"steps without an entry: {missing}"
    assert not extra, f"entries for no step: {extra}"


if __name__ == "__main__":   # pytest 없는 게이트 venv 에서도 돈다
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for n, f in tests:
        f()
        print(f"  [PASS] {n}")
    print(f"{len(tests)} 통과")
