# 게이트 직렬 단계 쓰기 규칙 시험 — 트리에 쓰는 직렬 단계는 «풀이 다 빈 뒤» 묶음에만 있고, 나머지 직렬 단계는 쓰지 않는다고 판정된 목록과 같은지
"""s4r 68 n5 → directing 11-08 ruling (b): no step that writes into the gate tree runs while a pool worker is alive.

Serial steps (check.sh `_pool_eligible`: everything but test_* and run.py*) do not wait for the pool, so a serial
step that writes runs only in the block that opens with its own `step_flush`, after every pool step. This test pins
that block's members to WRITERS, and every other serial step to NO_WRITE. A new serial step fails here until it is
classified. Each verdict is in the commit message of the commit that introduced this file; the reasons are kept short
beside each name."""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CHECK_SH = HERE / "check.sh"
STEP_RE = re.compile(r'^\s*(?:step|_step_serial) "([^"]+)"', re.M)
BLOCK_MARK = "# ── 풀이 다 빈 뒤에만 트리에 쓰는 직렬 단계"

WRITERS = [
    "tools/core_items.py",          # writes engine/core-items-<MMDD>.html (s4r gate.log l.4841)
    "derived *",                    # a moved stamp runs the entry's build census with --restore (rewrites, then puts back)
    "derived/test_derived.py",      # its restore fixtures rewrite engine/chain-explorer.html and leave a probe file
]
NO_WRITE = {
    # scripts/ guards and their tests: scratch dirs only (tempfile/mktemp), or read-only scans
    "scripts/test_gate_cleanup.sh", "scripts/test_gate_pool_reap.sh", "scripts/test_gate_serial_writes.py",
    "scripts/test_lane_decide.py",
    "scripts/test_gate_step_inputs.py", "scripts/test_interface_side_labels.py", "scripts/test_check_unwired_tests.py",
    "scripts/check_unwired_tests.py", "scripts/test_check_verdict_reads.py",
    "scripts/check_verdict_reads.py",               # writes its baseline only with --write-baseline (not the gate's argv)
    "scripts/test_check_py39.py", "scripts/check_py39.py", "scripts/test_check_compile_warnings.py",
    "scripts/test_gate_python_version.py",          # runs check.sh's head copy in a tempfile dir with a stub interpreter
    "scripts/check_compile_warnings.py", "scripts/pipeline/validate.py", "scripts/refs/validate_plasma_temp.py",
    "scripts/check_dead_links.py", "scripts/check_site_links.py", "scripts/check_citation_links.py", "경로 잔여물 grep",
    "scripts/check_language.py", "scripts/check_md_tables.py", "scripts/check_md_dupes.py",
    "scripts/check_build_freshness.py", "scripts/check_phase4_gate.py", "scripts/check_pipeline_flow.py",
    "build_sitemap",                                # --audit-only: the report is written only without it
    "scripts/check_methodology_coverage.py", "check_via", "check_contracts.py",
    "check_graph_page",                             # builds in a tempfile.mkdtemp mirror, not in the tree
    "engine/check_refs.py", "engine/chain.py", "engine/backflow.py",
    "structure_grid.py --check",                    # check_all/_recheck solve in memory; builds write only under --refresh
    "engine/tools/reference_adiabats.py --check",   # --check exits before the write
    "solver/tests/test_env_tiers.py", "tools/c51_regimes.py", "tools/c55_cells.py",
    "scripts/test_check_mass_formula.py",           # edits a copy under a temp tree
    "scripts/check_mass_formula.py", "tools/c47_step4.py",
    "dynamo_table",                                 # --check
}


def _names(src: str) -> list:
    out = []
    for n in STEP_RE.findall(src):
        if re.fullmatch(r"\$\{?\w+\}?", n):
            continue
        n = re.sub(r"\$\{?\w+\}?", "*", n)
        if n not in out:
            out.append(n)
    return out


def _serial(n: str) -> bool:
    return not re.match(r"(test_|run\.py)", n)


def _block(src: str) -> str:
    i = src.index(BLOCK_MARK)
    j = src.index("\nfi   # lane", i)
    return src[i:j]


def test_the_post_flush_block_holds_exactly_the_writers():
    src = CHECK_SH.read_text(encoding="utf-8")
    blk = _block(src)
    lines = [l for l in blk.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    assert lines[0].strip() == "step_flush", lines[:2]
    assert _names(blk) == WRITERS, _names(blk)
    assert not [n for n in _names(blk) if not _serial(n)], "a pool step inside the post-flush block"


def test_no_pool_step_after_the_block_flush():
    # nothing can start beside the writers: after the block's flush the only steps are the writers, and the next
    # barrier is the final one
    src = CHECK_SH.read_text(encoding="utf-8")
    tail = src[src.index(BLOCK_MARK):]
    assert not [n for n in _names(tail) if not _serial(n)], _names(tail)


def test_every_serial_step_outside_the_block_is_classified_no_write():
    src = CHECK_SH.read_text(encoding="utf-8")
    blk = _block(src)
    outside = [n for n in _names(src.replace(blk, "")) if _serial(n)]
    assert set(outside) == NO_WRITE, (sorted(set(outside) - NO_WRITE), sorted(NO_WRITE - set(outside)))
    assert not set(WRITERS) & set(outside), "a writer also runs outside the post-flush block"


def test_control_a_block_without_its_flush_is_red():
    src = CHECK_SH.read_text(encoding="utf-8")
    bad = src.replace(BLOCK_MARK, BLOCK_MARK, 1)
    i = bad.index(BLOCK_MARK)
    j = bad.index("\nstep_flush\n", i)
    bad = bad[:j] + "\n" + bad[j + len("\nstep_flush\n"):]
    lines = [l for l in _block(bad).splitlines() if l.strip() and not l.lstrip().startswith("#")]
    assert lines[0].strip() != "step_flush"


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for n, f in tests:
        f()
        print(f"  [PASS] {n}")
    print(f"{len(tests)} 통과")
    sys.exit(0)
