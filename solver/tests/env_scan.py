# 환경 스위치 스캐너 — 소스의 환경 변수 읽기·쓰기, in_gate() 호출, 환경으로 걸러지는 unittest 시험을 AST 로 찾음(test_env_tiers 와 착륙 판정이 씀)
"""HEAVY-onctl rev 2 P2. Pure functions over source text, so a planted source is a control.

- `env_names(src)`: every env name the module reads or writes: `<x>.environ.get/pop/setdefault(N)`, `<x>.environ[N]`,
  `os.getenv(N)`, `N in <x>.environ`, `dict(os.environ, N=…)` and `{… for k in os.environ.items() if k != N}`
  are not reads and are not counted. N is a string literal or a module-level name bound to one.
- `in_gate_sites(src)`: calls `<x>.in_gate()` or `in_gate()`.
- `gated_tests(src, module)`: {test id: env names} for TestCase methods whose run depends on an env read: a
  skip decorator on the method or its class, or an `if` in the method, setUp or setUpClass whose branch calls
  skipTest / raises SkipTest, where the decorator or the `if` test reads env directly or through a module-level
  name bound to an env read."""
import ast

_ENV_METHODS = ("get", "pop", "setdefault")


def _consts(tree):
    out = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
            out[node.targets[0].id] = node.value.value
    return out


def _is_environ(node):
    return isinstance(node, ast.Attribute) and node.attr == "environ"


def _name_of(arg, consts):
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        return arg.value
    if isinstance(arg, ast.Name) and arg.id in consts:
        return consts[arg.id]
    return None


def _reads(node, consts):
    """Env names read anywhere under `node`."""
    out = set()
    for n in ast.walk(node):
        name = None
        if isinstance(n, ast.Call) and n.args:
            f = n.func
            if isinstance(f, ast.Attribute) and f.attr in _ENV_METHODS and _is_environ(f.value):
                name = _name_of(n.args[0], consts)
            elif isinstance(f, ast.Attribute) and f.attr == "getenv":
                name = _name_of(n.args[0], consts)
        elif isinstance(n, ast.Subscript) and _is_environ(n.value):
            name = _name_of(n.slice, consts)
        elif isinstance(n, ast.Compare) and len(n.ops) == 1 and isinstance(n.ops[0], (ast.In, ast.NotIn)) \
                and _is_environ(n.comparators[0]):
            name = _name_of(n.left, consts)
        if name:
            out.add(name)
    return out


def env_names(src):
    tree = ast.parse(src)
    return _reads(tree, _consts(tree))


def in_gate_sites(src):
    tree = ast.parse(src)
    return sum(1 for n in ast.walk(tree) if isinstance(n, ast.Call)
               and ((isinstance(n.func, ast.Attribute) and n.func.attr == "in_gate")
                    or (isinstance(n.func, ast.Name) and n.func.id == "in_gate")))


def _aliases(tree, consts):
    """Module-level names bound to an expression that reads env: name → env names."""
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            r = _reads(node.value, consts)
            if r:
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        out[t.id] = r
    return out


def _cond_envs(node, consts, aliases):
    r = set(_reads(node, consts))
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and n.id in aliases:
            r |= aliases[n.id]
    return r


def _skips(stmts):
    for n in ast.walk(ast.Module(body=list(stmts), type_ignores=[])):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "skipTest":
            return True
        if isinstance(n, ast.Raise) and n.exc is not None and "SkipTest" in ast.unparse(n.exc):
            return True
    return False


def _body_gates(fn, consts, aliases):
    out = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.If) and (_skips(n.body) or _skips(n.orelse)):
            out |= _cond_envs(n.test, consts, aliases)
    return out


def _deco_gates(decos, consts, aliases):
    out = set()
    for d in decos:
        if isinstance(d, ast.Call) and ast.unparse(d.func).split(".")[-1] in ("skipUnless", "skipIf") and d.args:
            out |= _cond_envs(d.args[0], consts, aliases)
    return out


def gated_tests(src, module):
    tree = ast.parse(src)
    consts = _consts(tree)
    aliases = _aliases(tree, consts)
    out = {}
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        fns = {f.name: f for f in cls.body if isinstance(f, ast.FunctionDef)}
        common = _deco_gates(cls.decorator_list, consts, aliases)
        for setup in ("setUp", "setUpClass"):
            if setup in fns:
                common |= _body_gates(fns[setup], consts, aliases)
        for name, f in fns.items():
            if not name.startswith("test"):
                continue
            envs = common | _deco_gates(f.decorator_list, consts, aliases) | _body_gates(f, consts, aliases)
            if envs:
                out[f"{module}.{cls.name}.{name}"] = envs
    return out
