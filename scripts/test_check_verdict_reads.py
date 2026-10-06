# 판정 읽기 검사의 자기 시험 — 초안 7f2d8d2e §2 의 실제 결함 꼴 다섯이 잡히고, 그 고친 꼴과 까닭 단 탈출은 통과하는가
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import check_verdict_reads as c


def reads(src):
    return c.scan_source(src)["reads"]


# 1. edge_census c1daac79 — `ok, reason = r.applicable, …` 뒤 `if ok: kind = "answer"`
EDGE = 'def f(r):\n    ok, reason = r.applicable, r.reason\n    if ok:\n        kind = "answer"\n'
# 2. tight_census pre-797b82b9 :54 — getattr 꼴
TIGHT54 = 'def f(r):\n    ok = getattr(r, "applicable", True)\n    return "A" if ok else "U"\n'
# 3. tight_census pre-797b82b9 :108 — 판정을 돌려주는 함수와 그 호출부(한 단계 함수 사이 흐름)
TIGHT108 = ('def answers(t):\n    r = solve(t)\n    return bool(getattr(r, "applicable", False))\n'
            'def g(hi, m_):\n    if not answers(hi):\n        return None\n    return m_ if answers(m_) else hi\n')
# 4. 부정 꼴 — `if not res.applicable: break` 뒤 `best = res` (황 맞춤의 꼴)
NEG = 'def f(xs):\n    best = None\n    for res in xs:\n        if not res.applicable:\n            break\n        best = res\n    return best\n'
# 5. 까닭 빈 탈출
EMPTY = 'def f(r):\n    print(r.applicable)  # verdict-ok:\n'


def test_edge_flagged():
    assert [(ln, q) for ln, q, _ in reads(EDGE)] == [(2, "f")]


def test_getattr_flagged():
    assert [(ln, w) for ln, _, w in reads(TIGHT54)] == [(2, "getattr")]


def test_return_source_and_callers_flagged():
    got = reads(TIGHT108)
    assert (3, "answers", "getattr") in got
    callers = [(ln, q) for ln, q, w in got if w.startswith("answers()")]
    assert callers == [(5, "g"), (7, "g")], callers


def test_negative_polarity_flagged():
    assert [(ln, q) for ln, q, _ in reads(NEG)] == [(4, "f")]


def test_empty_escape_is_a_fail():
    res = c.scan_source(EMPTY)
    assert res["empty_ok"] == [2] and res["reads"] == [(2, "f", ".applicable")] and res["escaped"] == []


def test_rewrites_pass():
    src = ('import interior\n'
           'def f(r):\n    kind = interior.verdict_of(r).kind\n    return interior.is_answer(r)\n'
           'def g(r):\n    print(r.applicable)  # verdict-ok: 기록만, 인쇄\n')
    res = c.scan_source(src)
    assert res["reads"] == [] and res["empty_ok"] == [] and res["escaped"] == [(6, "g", "기록만, 인쇄")]


def test_escaped_source_does_not_propagate():
    src = ('def answers(r):\n    return r.applicable  # verdict-ok: 이 함수는 기록 줄만 만든다\n'
           'def g(r):\n    return answers(r)\n')
    assert reads(src) == []


def test_exempt_bodies():
    src = ('def answer_verdict(r, tags=None):\n    if not r.applicable:\n        return "거절"\n'
           'def verdict_of(r):\n    return r.applicable\ndef is_answer(r):\n    return r.applicable\n')
    assert reads(src) == []


def test_loose_listed_not_flagged():
    res = c.scan_source('def f(d):\n    return d["applicable"] or d.get("applicable")\n')
    assert res["reads"] == [] and len(res["loose"]) == 2


def test_store_not_flagged():
    assert reads('def f(r):\n    r.applicable = True\n') == []


def test_compare_exact():
    base = {"a.py": {"f": 2}}
    assert c.compare({"a.py": {"f": 2}}, base) == []
    assert any("새 판정 읽기" in f for f in c.compare({"a.py": {"f": 3}}, base))
    assert any("기준표가 낡음" in f for f in c.compare({"a.py": {"f": 1}}, base))
    assert any("새 판정 읽기 b.py" in f for f in c.compare({"a.py": {"f": 2}, "b.py": {"<module>": 1}}, base))


if __name__ == "__main__":
    n = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            n += 1
    print(f"  [PASS] 판정 읽기 검사 자기 시험 {n}")
