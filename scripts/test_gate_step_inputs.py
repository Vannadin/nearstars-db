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


def _hooked_main(tmp: pathlib.Path, script: str) -> list[dict]:
    log = tmp / "reads.jsonl"
    log.unlink(missing_ok=True)
    env = dict(os.environ, GATE_READS_LOG=str(log), GATE_READS_ROOT=str(tmp), GATE_READS_RAW="1",
               GATE_STEP="fixture", PYTHONPATH=str(HERE / "gate_reads"), PYTHONDONTWRITEBYTECODE="1",
               PYTHONWARNINGS="default")
    subprocess.run([sys.executable, script], cwd=tmp, env=env, check=True, capture_output=True)
    return [json.loads(l) for l in log.read_text().splitlines() if l.strip()]


def test_fix4_a_runtime_warnings_source_reload_dropped():
    # FIX4 (1): a repo module warning at run time — linecache reloads its source to print the line; not data
    tmp = _scratch()
    (tmp / "warn_mod.py").write_text("import warnings\ndef go():\n    warnings.warn('w', RuntimeWarning)\n")
    (tmp / "main_w.py").write_text("import warn_mod\nwarn_mod.go()\n")
    recs = _hooked_main(tmp, "main_w.py")
    assert not _kept(recs, "warn_mod.py"), "a warning's source-line reload must not read as data"
    assert any(r["path"] == "warn_mod.py" and r.get("by") == "linecache" and r.get("dropped") for r in recs)


def test_fix4_a_compile_warning_in_the_main_script_dropped():
    # FIX4: the landing's group 4 shape — `\|` in the main script's docstring, a 3.12 SyntaxWarning (3.9: hidden)
    tmp = _scratch()
    (tmp / "main_s.py").write_text('"""a `\\|` b"""\nX = 1\n')
    recs = _hooked_main(tmp, "main_s.py")
    assert not _kept(recs, "main_s.py")


def test_fix4_a_data_file_through_linecache_recorded():
    # FIX4 (2): linecache.getlines on a data file is a read, before and after FIX4
    tmp = _scratch()
    (tmp / "main_l.py").write_text("import linecache\nlinecache.getlines('table.md')\n")
    recs = _hooked_main(tmp, "main_l.py")
    assert len(_kept(recs, "table.md")) == 1


def test_fix4_a_repo_py_opened_as_text_recorded():
    # FIX4 (3): open() of another repo .py as text stays a read (11-03), loaded or not
    tmp = _scratch()
    (tmp / "main_o.py").write_text("import scratch_mod\nopen('scratch_mod.py').read()\nopen('loader_mod.py').read()\n")
    recs = _hooked_main(tmp, "main_o.py")
    assert len(_kept(recs, "scratch_mod.py")) == 1 and len(_kept(recs, "loader_mod.py")) == 1


def test_fix4_a_data_file_named_as_a_modules_file_recorded():
    # FIX4: only a .py source is a reload — a module whose __file__ names a data file does not hide that file's read
    tmp = _scratch()
    (tmp / "main_d.py").write_text("import sys, types, linecache\nm = types.ModuleType('fake')\n"
                                   "m.__file__ = 'table.md'\nsys.modules['fake'] = m\nlinecache.getlines('table.md')\n")
    recs = _hooked_main(tmp, "main_d.py")
    assert len(_kept(recs, "table.md")) == 1


def test_fix4_inspect_getsource_of_a_loaded_module_recorded():
    # FIX4 (r2 B1 on ef0167d4): inspect.getsource reads through linecache too — a source read as text, recorded
    tmp = _scratch()
    (tmp / "src_mod.py").write_text("def f():\n    return 1\n")
    (tmp / "main_i.py").write_text("import inspect, src_mod\ninspect.getsource(src_mod.f)\n")
    recs = _hooked_main(tmp, "main_i.py")
    assert len(_kept(recs, "src_mod.py")) == 1
    assert any(r["kind"] == "leak" and r["path"] == "src_mod.py" for r in recs)


def test_fix4_a_traceback_print_reload_dropped():
    # FIX4: traceback.print_stack shows source lines through linecache — display, not data
    tmp = _scratch()
    (tmp / "tb_mod.py").write_text("import traceback, io\ndef go():\n    traceback.print_stack(file=io.StringIO())\n")
    (tmp / "main_t.py").write_text("import tb_mod\ntb_mod.go()\n")
    recs = _hooked_main(tmp, "main_t.py")
    assert not _kept(recs, "tb_mod.py")


def test_fix4_a_traceback_format_exc_reload_dropped():
    # FIX4 (c): traceback.format_exc after an exception in a repo module — the same display class as a warning
    tmp = _scratch()
    (tmp / "exc_mod.py").write_text("def go():\n    raise ValueError('x')\n")
    (tmp / "main_e.py").write_text("import traceback, exc_mod\ntry:\n    exc_mod.go()\n"
                                   "except ValueError:\n    traceback.format_exc()\n")
    recs = _hooked_main(tmp, "main_e.py")
    assert not _kept(recs, "exc_mod.py")


def test_fix4_a_repo_file_named_warnings_or_traceback_is_not_the_stdlib():
    # FIX4 (b): repo files named warnings.py / traceback.py calling linecache on a loaded module's source — recorded
    tmp = _scratch()
    (tmp / "fake").mkdir()
    for name in ("warnings", "traceback"):
        (tmp / "fake" / f"{name}.py").write_text("import linecache\ndef show(p):\n    linecache.getlines(p)\n")
    (tmp / "plain_mod.py").write_text("Y = 2\n")        # no warnings of its own (loader_mod's open is a ResourceWarning)
    (tmp / "main_n.py").write_text(
        "import importlib.util, scratch_mod, plain_mod\n"
        "def load(name, alias):\n"
        "    spec = importlib.util.spec_from_file_location(alias, f'fake/{name}.py')\n"
        "    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m\n"
        "load('warnings', 'repo_warnings').show('scratch_mod.py')\n"
        "load('traceback', 'repo_traceback').show('plain_mod.py')\n")
    recs = _hooked_main(tmp, "main_n.py")
    assert len(_kept(recs, "scratch_mod.py")) == 1 and len(_kept(recs, "plain_mod.py")) == 1


def test_fix4_a_repo_warnings_installed_as_sys_modules_warnings_is_not_the_stdlib():
    # FIX4: the stdlib frames are those under sysconfig's stdlib dir — a repo warnings.py put in sys.modules is not one
    tmp = _scratch()
    (tmp / "fake").mkdir()
    (tmp / "fake" / "warnings.py").write_text("import linecache\ndef show(p):\n    linecache.getlines(p)\n")
    (tmp / "main_m.py").write_text(
        "import sys, importlib.util, scratch_mod\n"
        "spec = importlib.util.spec_from_file_location('warnings', 'fake/warnings.py')\n"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
        "sys.modules['warnings'] = m\nm.show('scratch_mod.py')\n")
    recs = _hooked_main(tmp, "main_m.py")
    assert len(_kept(recs, "scratch_mod.py")) == 1


def test_fix4_a_warning_naming_an_unloaded_py_recorded():
    # FIX4: the dropped reload is of a loaded module's source — a warning pointing at another .py reads it
    tmp = _scratch()
    (tmp / "unl_mod.py").write_text("Z = 3\n")
    (tmp / "main_x2.py").write_text("import warnings\nwarnings.warn_explicit('w', UserWarning, 'unl_mod.py', 1)\n")
    recs = _hooked_main(tmp, "main_x2.py")
    assert len(_kept(recs, "unl_mod.py")) == 1


def test_fix4_a_warning_naming_a_data_file_as_a_modules_file_recorded():
    # FIX4: only a .py is a source reload — a warning shown against a data file a module names as __file__ is a read
    tmp = _scratch()
    (tmp / "main_x3.py").write_text("import sys, types, warnings\nm = types.ModuleType('fake')\n"
                                    "m.__file__ = 'table.md'\nsys.modules['fake'] = m\n"
                                    "warnings.warn_explicit('w', UserWarning, 'table.md', 1)\n")
    recs = _hooked_main(tmp, "main_x3.py")
    assert len(_kept(recs, "table.md")) == 1


def test_fix4_a_repo_showwarning_opening_a_source_recorded():
    # FIX4: under a warnings frame, only linecache's reload is dropped — a repo showwarning that open()s a source reads it
    tmp = _scratch()
    (tmp / "main_x4.py").write_text("import warnings, scratch_mod\n"
                                    "def show(*a, **k):\n    open('scratch_mod.py').read()\n"
                                    "warnings.showwarning = show\nwarnings.warn('w')\n")
    recs = _hooked_main(tmp, "main_x4.py")
    assert len(_kept(recs, "scratch_mod.py")) == 1


def test_fix4_inspect_getsource_under_a_warnings_frame_recorded():
    # FIX4: walking out from linecache, an inspect frame before the warnings frame makes it a source read
    tmp = _scratch()
    (tmp / "src_mod2.py").write_text("def f():\n    return 2\n")
    (tmp / "main_x5.py").write_text("import inspect, warnings, src_mod2\n"
                                    "def show(*a, **k):\n    inspect.getsource(src_mod2.f)\n"
                                    "warnings.showwarning = show\nwarnings.warn('w')\n")
    recs = _hooked_main(tmp, "main_x5.py")
    assert len(_kept(recs, "src_mod2.py")) == 1


def test_fix4_linecache_on_an_unloaded_py_recorded():
    # FIX4: linecache on a .py that is no loaded module's source is not a warning reload: recorded
    tmp = _scratch()
    (tmp / "main_u.py").write_text("import linecache\nlinecache.getlines('loader_mod.py')\n")
    recs = _hooked_main(tmp, "main_u.py")
    assert len(_kept(recs, "loader_mod.py")) == 1


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


def test_c147_pkg_resources_walk_dropped():
    # L-meta-pr (부록 1): 가짜 pkg_resources 패키지 — 설치와 무관하게 모듈 경로로 걸러지는지. SKIP 없음.
    tmp = _scratch()
    (tmp / "sub").mkdir()
    stub = tmp / "stubs" / "pkg_resources"
    stub.mkdir(parents=True)
    (stub / "__init__.py").write_text("import os, sys\nfor _p in list(sys.path):\n"
                                      "    try: os.listdir(_p)\n    except OSError: pass\n")
    recs = _hooked(tmp, "import sys; sys.path[:0] = ['stubs', 'sub']; import pkg_resources")
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
    assert _lists(recs, "d") and _lists(recs, "d")[0].get("by", "").partition(":")[0] == "pathlib.py"


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


def _repo_like(tmp):
    """scratch 나무: engine/test_k.py (게이트 전용) · engine/libmod.py (라이브러리) · engine/data.yaml."""
    eng = tmp / "engine"
    eng.mkdir()
    (eng / "data.yaml").write_text("a: 1\n")
    (eng / "libmod.py").write_text("import pathlib\n"
                                   "def read(): return pathlib.Path(__file__).with_name('data.yaml').read_text()\n"
                                   "def load(p):\n    with open(p) as f: return f.read()\n")
    (eng / "test_k.py").write_text("import pathlib, sys\nsys.path.insert(0, str(pathlib.Path(__file__).parent))\n"
                                   "import libmod\n"
                                   "MODE = sys.argv[1]\n"
                                   "if MODE == 'test': pathlib.Path(__file__).with_name('data.yaml').read_text()\n"
                                   "if MODE == 'lib': libmod.read()\n"
                                   "if MODE == 'helper': libmod.load(str(pathlib.Path(__file__).with_name('data.yaml')))\n")
    return eng


def _hooked_script(tmp, *args):
    log = tmp / "reads.jsonl"
    log.unlink(missing_ok=True)
    env = dict(os.environ, GATE_READS_LOG=str(log), GATE_READS_ROOT=str(tmp), GATE_STEP="fixture",
               PYTHONPATH=str(HERE / "gate_reads"), PYTHONDONTWRITEBYTECODE="1")
    subprocess.run([sys.executable, *args], cwd=tmp, env=env, check=True)
    return [json.loads(l) for l in log.read_text().splitlines() if l.strip()]


def _openers(recs, path):
    return {r.get("by") for r in recs if r["kind"] == "open" and r["path"] == path and not r.get("dropped")}


def test_c149_opener_is_innermost_repo_frame():
    # K-opener: (i) 시험이 read_text → 시험 모듈 · (ii) 라이브러리가 read_text → 그 모듈 · (iii) 시험→라이브러리 도우미 → 도우미
    tmp = _scratch()
    _repo_like(tmp)
    assert _openers(_hooked_script(tmp, "engine/test_k.py", "test"), "engine/data.yaml") == {"engine/test_k.py"}
    assert _openers(_hooked_script(tmp, "engine/test_k.py", "lib"), "engine/data.yaml") == {"engine/libmod.py"}
    assert _openers(_hooked_script(tmp, "engine/test_k.py", "helper"), "engine/data.yaml") == {"engine/libmod.py"}


def test_c149_library_read_of_listed_path_fails():
    # K-lib: 목록에 오른 파일을 라이브러리가 열면 FAIL, 게이트 전용이 열면 통과
    listed = {"engine/data.yaml"}
    ok = [{"step": "s", "kind": "open", "path": "engine/data.yaml", "by": "engine/test_k.py"}]
    bad = [{"step": "s", "kind": "open", "path": "engine/data.yaml", "by": "engine/libmod.py"}]
    none = [{"step": "s", "kind": "open", "path": "engine/data.yaml", "by": "<none>"}]
    assert gsi.via_also_drift(ok, listed) == []
    assert "read by engine/libmod.py, not gate-only" in gsi.via_also_drift(bad, listed)[0]
    assert gsi.via_also_drift(none, listed)          # 레포 프레임 없음 = 라이브러리


def test_c149_unlisted_data_stays_full(monkeypatch=None):
    # K-unread: 목록 밖 데이터 경로는 오늘처럼 full
    import lane_decide as ld
    real = ld._via_also
    ld._via_also = lambda: {"engine/tools/core_items_kind.yaml"}
    try:
        assert not ld.ALWAYS_FULL.search("docs/x.md")
        assert "engine/bodies/mars.yaml" not in ld._via_also() and ld.ALWAYS_FULL.search("engine/bodies/mars.yaml")
    finally:
        ld._via_also = real


def test_c149_import_grep():
    # K-census grep: 라이브러리가 게이트 전용 모듈을 import 하면 FAIL
    tmp = _scratch()
    eng = tmp / "engine"
    (eng / "tools").mkdir(parents=True)
    (eng / "tools" / "core_items.py").write_text("X = 1\n")
    (eng / "test_a.py").write_text("import libok\n")
    (eng / "libok.py").write_text("import math\n")
    assert gsi.library_imports_gate_only(tmp) == []
    (eng / "libbad.py").write_text("from tools import core_items\nimport test_a\n")
    fails = gsi.library_imports_gate_only(tmp)
    assert len(fails) == 2 and all("engine/libbad.py imports" in f for f in fails)


def test_derived_is_gate_only_and_never_imported_by_shipped_code():
    # derived/ 는 게이트 전용: 출하 모듈(engine/·solver/·solver/materials/)이 derived 를 import 하면 FAIL
    assert gsi.gate_only("derived/check.py") and gsi.gate_only("derived/census_site/sitecustomize.py")
    assert not gsi.gate_only("solver/solve.py") and not gsi.gate_only("engine/payload.py")
    tmp = _scratch()
    for d in ("engine", "solver/materials", "derived"):
        (tmp / d).mkdir(parents=True, exist_ok=True)
    (tmp / "derived" / "check.py").write_text("X = 1\n")
    (tmp / "solver" / "ok.py").write_text("from solver import result\n")
    (tmp / "engine" / "test_x.py").write_text("import derived.check\n")      # 시험은 출하 아님
    assert gsi.library_imports_gate_only(tmp) == []
    (tmp / "solver" / "materials" / "bad.py").write_text("from derived import check\n")
    (tmp / "engine" / "bad.py").write_text("import derived.check\n")
    fails = gsi.library_imports_gate_only(tmp)
    assert sorted(f.split(" — ")[1] for f in fails) == [
        "engine/bad.py imports derived.check (a gate-only module)",
        "solver/materials/bad.py imports derived (a gate-only module)"], fails


def test_real_tree_has_no_shipped_import_of_gate_only_code():
    # 실제 트리: 출하 모듈 111개 어디도 derived/·tools/·게이트 전용 모듈을 import 하지 않음
    assert gsi.library_imports_gate_only() == []


def test_c149_listed_path_is_pass_class():
    real = gsi.via_also
    gsi.via_also = lambda path=None: {"engine/tools/core_items_kind.yaml"}
    try:
        assert gsi.pass_class("engine/tools/core_items_kind.yaml") and not gsi.pass_class("engine/bodies/mars.yaml")
    finally:
        gsi.via_also = real


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
