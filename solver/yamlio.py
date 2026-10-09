# 프로젝트 YAML 로더 — YAML 1.2 core 의 수 · 참거짓만 풀고, 겹친 키와 이상한 키는 이름 대며 멈춘다 (D-A7-2).
"""The project YAML loader (`rewrite/phase1-design.frozen.md` D-A7-2), shared by body files and the solver's own
data files (schema, roles, presets).

PyYAML is YAML 1.1. Its implicit resolvers read `6.0e21` as a string, `no`/`on` as booleans, `017` as octal 15,
`1_000` and `1:30` as integers, and `2024-01-01` as a date. Here only the YAML 1.2 core schema resolves:
null (`~`, `null`), bool (`true`/`false`), int (`[-+]?[0-9]+`, `0o…`, `0x…`) and float. Everything else is a string.
A duplicate key, an unhashable key, or a value no constructor can build raises `LoadError` with a line number.
"""
from __future__ import annotations

import re

import yaml

from solver.result import freeze


class LoadError(Exception):
    """A document the loader refuses: `kind` ∈ {duplicate_key, bad_key, unreadable}; `key`/`line` where known."""

    def __init__(self, kind: str, detail: str, key=None, line=None):
        super().__init__(detail)
        self.kind, self.detail, self.key, self.line = kind, detail, key, line


class Loader(yaml.SafeLoader):
    pass


_KEEP = ("tag:yaml.org,2002:null", "tag:yaml.org,2002:str")
Loader.yaml_implicit_resolvers = {
    ch: [(tag, rx) for tag, rx in rs if tag in _KEEP]
    for ch, rs in yaml.SafeLoader.yaml_implicit_resolvers.items()}
_INT_RE = re.compile(r"^(?:[-+]?[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+)$")
_FLOAT_RE = re.compile(r"^(?:[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?|[-+]?\.(?:inf|Inf|INF)"
                       r"|\.(?:nan|NaN|NAN))$")
Loader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
                             list("tTfF"))
Loader.add_implicit_resolver("tag:yaml.org,2002:int", _INT_RE, list("-+0123456789"))
Loader.add_implicit_resolver("tag:yaml.org,2002:float", _FLOAT_RE, list("-+0123456789."))


def _int(loader, node):
    s = loader.construct_scalar(node)
    if s.startswith("0o"):
        return int(s[2:], 8)
    if s.startswith("0x"):
        return int(s[2:], 16)
    return int(s, 10)                       # «017» is 17 (YAML 1.2), not octal 15


def _map(loader, node):
    if not isinstance(node, yaml.MappingNode):
        raise LoadError("unreadable", "expected a mapping", line=node.start_mark.line + 1)
    out, seen = {}, set()
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        line = key_node.start_mark.line + 1
        try:
            hash(key)
        except TypeError:
            raise LoadError("bad_key", f"unhashable key {key!r}", key=repr(key), line=line) from None
        if key in seen:
            raise LoadError("duplicate_key", f"key {key!r} repeated", key=key, line=line)
        seen.add(key)
        out[key] = loader.construct_object(value_node, deep=True)
    return out


Loader.add_constructor("tag:yaml.org,2002:int", _int)
Loader.add_constructor("tag:yaml.org,2002:map", _map)


def parse(text: str):
    """Parse YAML text with the project loader. Raises `LoadError` only."""
    try:
        return yaml.load(text, Loader=Loader)
    except LoadError:
        raise
    except yaml.YAMLError as e:
        raise LoadError("unreadable", str(e).splitlines()[0][:160]) from None
    except (RecursionError, ValueError, TypeError, OverflowError) as e:
        raise LoadError("unreadable", f"{type(e).__name__}: {str(e)[:120]}") from None


def load_data(path):
    """A solver data file (schema, roles, presets), parsed with the project loader and deep-frozen."""
    from pathlib import Path
    return freeze(parse(Path(path).read_text(encoding="utf-8")))
