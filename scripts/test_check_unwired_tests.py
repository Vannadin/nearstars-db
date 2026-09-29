# 안 엮인 시험 검사(C129)의 자기 시험 — 합성 목록으로 FAIL 조건 넷과 PASS 하나
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import check_unwired_tests as c

SH = "# 주석 test_c.py\nstep \"test_a.py\" bash -c 'cd engine && exec python3 test_a.py'\n"
A, B, C = "engine/test_a.py", "scripts/test_b.py", "engine/test_c.py"


def fails(tests, ex):
    return c.audit(tests, SH, ex)[0]


def test_pass():
    assert fails([A, B], {B: "까닭"}) == []


def test_unwired():
    assert fails([A, B], {}) == [f"[FAIL] 안 엮인 시험 {B}"]


def test_comment_line_not_wired():
    assert fails([A, C], {}) == [f"[FAIL] 안 엮인 시험 {C}"]


def test_stale_exclusion():
    assert fails([A], {B: "까닭"}) == [f"[FAIL] 낡은 제외 {B} — 추적 파일 없음"]


def test_wired_and_excluded():
    assert fails([A], {A: "까닭"}) == [f"[FAIL] 엮여 있는데 제외 목록에도 있음 {A}"]


def test_empty_reason():
    assert fails([A, B], {B: " "}) == [f"[FAIL] 제외 까닭 빈 칸 {B}"]


def test_basename_clash():
    assert any("basename 겹침" in f for f in fails([A, "scripts/test_a.py"], {}))


if __name__ == "__main__":   # pytest 없는 게이트 venv 에서도 돈다
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for n, f in tests:
        f()
        print(f"  [PASS] {n}")
    print(f"{len(tests)} 통과")
