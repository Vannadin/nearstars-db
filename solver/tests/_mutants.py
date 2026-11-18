# 변형 시험 도우미 — 함수의 소스를 고쳐 원래 모듈의 전역 위에서 다시 만들어, 모듈에 건 패치가 변형에도 닿게 함; 고치지 않은 사본(identity)도 같은 길로 만들어 통과를 보임 (68 B1 on C2, directing 11-18)
"""`variant(fn, old, new)`: fn rebuilt from its source with `old` replaced by `new` (exactly one occurrence), compiled
with fn's own module globals, so a mock.patch on that module reaches it, as it reaches the real fn. `variant(fn)` with
no replacement is the identity copy: a mutant test shows the identity copy passes and the mutant fails."""
import inspect
import textwrap


def variant(fn, old=None, new=None, more=()):
    """`more`: further (old, new) pairs applied after the first, each found exactly once."""
    src = textwrap.dedent(inspect.getsource(fn))
    pairs = ([(old, new)] if old is not None else []) + list(more)
    for o, n in pairs:
        if src.count(o) != 1:
            raise AssertionError(f"mutant anchor found {src.count(o)} times in {fn.__name__}")
        src = src.replace(o, n)
    loc = {}
    exec(compile(src, inspect.getsourcefile(fn), "exec"), fn.__globals__, loc)
    return loc[fn.__name__]
