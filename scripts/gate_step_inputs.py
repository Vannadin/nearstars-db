# 게이트 단계의 선언 입력 표를 읽고, 차선의 also·표류 검사·전수 인쇄를 하는 도구 (C136)
"""Declared data inputs of gate steps (C136).

    python3 scripts/gate_step_inputs.py census <reads-log>     # print what each step read (pass-class)
    python3 scripts/gate_step_inputs.py check  <reads-log>     # drift guard: [FAIL] lines, rc 1 on any
    python3 scripts/gate_step_inputs.py draft  <reads-log>     # yaml entries for the measured steps

`gate_step_inputs.yaml` maps a step name, exactly as `step "<name>"` in `check.sh`, to
`{globs: [...], hand: bool}`. Globs are repo-relative paths with git-style wildcards: `*` and `?`
stay inside one path component, `**` crosses `/` (so `**.md` is every `.md`, `docs/*` is only
the files directly in `docs/`). A step with no data reads carries `globs: []`.

What a run observed, and what covers it:
- a file read (`open`, `git show <rev>:<path>`) — covered when a glob matches the path;
- a directory listed (`os.listdir` / `os.scandir`) — covered when a glob matches a new `.md` or
  `.py` placed directly in it;
- a `glob.glob` pattern or a `git ls-files` / `git grep` pathspec — covered when a glob matches
  the pass-class names the pattern could produce (probe names; a git pathspec's `*` crosses `/`,
  so it is probed one and three levels deep).

⚠ **Only pass-class paths matter** — the ones `lane_decide.classify` lets through (prose, and a
`.py` whose code object did not move). Everything else already forces the full lane, so a step's
reads of yaml, json or csv need no entry here.
"""
from __future__ import annotations

import fnmatch
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
YAML = HERE / "gate_step_inputs.yaml"
CHECK_SH = HERE / "check.sh"
STEP_RE = re.compile(r'^\s*(?:step|_step_serial) "([^"]+)"', re.M)


def pass_class(path: str) -> bool:
    import lane_decide
    return bool(lane_decide.PROSE.search(path)) or path.endswith(".py")


def load(path: pathlib.Path = YAML) -> dict[str, dict]:
    import yaml
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = {}
    for name, ent in raw.items():
        if not isinstance(ent, dict) or not isinstance(ent.get("globs"), list):
            raise SystemExit(f"거절: {path.name} 의 «{name}» 에 globs 목록이 없다")
        out[name] = {"globs": [str(g) for g in ent["globs"]], "hand": bool(ent.get("hand", False))}
    return out


def step_names(check_sh: pathlib.Path = CHECK_SH) -> list[str]:
    """`step "<이름>"` 줄의 이름. ⚠ 이름에 쉘 변수가 든 단계(바디 글롭 루프)는 변수를 `*` 로 바꾼
    **틀 이름**으로 센다 — 표의 키도 그 틀이고, 기록의 실제 이름은 `entry()` 가 틀에 맞춘다.
    이름 전체가 변수인 줄(`step()` 안의 `_step_serial "$name"`)은 단계가 아니다."""
    names = []
    for n in STEP_RE.findall(check_sh.read_text(encoding="utf-8")):
        if re.fullmatch(r"\$\{?\w+\}?", n):
            continue
        n = re.sub(r"\$\{?\w+\}?", "*", n)
        if n not in names:
            names.append(n)
    return names


def quick_steps(check_sh: pathlib.Path = CHECK_SH) -> list[str]:
    """`_QUICK_STEPS="…"` 의 여덟 — also 는 이 밖의 단계만 고른다 (C136 §1.3 «non-quick step»)."""
    m = re.search(r'^_QUICK_STEPS="([^"]*)"', check_sh.read_text(encoding="utf-8"), re.M)
    return [l.strip() for l in (m.group(1) if m else "").splitlines() if l.strip()]


def entry(table: dict[str, dict], step: str) -> dict | None:
    """기록에 찍힌 실제 단계 이름 → 표의 칸 (정확히 같은 키, 없으면 틀 키 하나)."""
    if step in table:
        return table[step]
    hits = [k for k in table if "*" in k and fnmatch.fnmatchcase(step, k)]
    return table[hits[0]] if len(hits) == 1 else None


def _glob_re(g: str) -> re.Pattern:
    out, i = [], 0
    while i < len(g):
        c = g[i]
        if g.startswith("**", i):
            out.append(".*")
            i += 2
            continue
        if c == "*":
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c == "[":
            j = g.find("]", i + 1)
            if j < 0:
                out.append(re.escape(c))
            else:
                cls = g[i + 1:j]
                out.append("[" + ("^" + cls[1:] if cls.startswith("!") else cls) + "]")
                i = j
        else:
            out.append(re.escape(c))
        i += 1
    return re.compile("".join(out) + r"\Z")


def matches(path: str, globs: list[str]) -> bool:
    return any(_glob_re(g).match(path) for g in globs)


def probes(pattern: str, git: bool = False) -> list[str]:
    """이 패턴이 낼 수 있는 산문·코드 이름의 표본 — 와일드카드를 `__new__` 로 채운다.
    git pathspec 의 `*` 는 `/` 를 넘으므로 한 층과 세 층 깊이 둘로 채운다."""
    fills = ["__new__", "a/b/__new__"] if git else ["__new__"]
    out = []
    for f in fills:
        s = re.sub(r"\*\*/?", "a/", pattern) if not git else pattern
        s = s.replace("*", f).replace("?", "x")
        s = re.sub(r"\[[^\]]*\]", "x", s)
        cands = [s] + ([s + ".md", s + ".py"] if s.endswith(f) else [])   # 끝이 와일드카드면 확장자를 붙여 본다
        for q in cands:
            if pass_class(q) and q not in out:
                out.append(q)
    return out


def also(passed: list[str], table: dict[str, dict], names: list[str],
         quick: list[str] = ()) -> tuple[list[str], list[str]]:
    """(non-quick steps whose globs meet a passed path, non-quick steps in check.sh with no entry).

    ⚠ A step with no entry could read anything — the caller must go full when `passed` is not
    empty and the second list is not empty (C136 §1.3)."""
    rest = [n for n in names if n not in quick]
    hit = [n for n in rest if n in table and any(matches(p, table[n]["globs"]) for p in passed)]
    missing = [n for n in rest if n not in table]
    return hit, missing


def read_log(log: pathlib.Path) -> list[dict]:
    recs = []
    for line in log.read_text(encoding="utf-8").splitlines():
        if line.strip():
            recs.append(json.loads(line))
    return recs


def observed(recs: list[dict]) -> dict[str, dict[str, set]]:
    """step → {"files": pass-class files opened or git-shown, "dirs": listed dirs, "leak": ...}."""
    out: dict[str, dict[str, set]] = {}
    for r in recs:
        if r.get("dropped"):
            continue
        d = out.setdefault(r["step"], {"files": set(), "dirs": set(), "leak": set(), "specs": set()})
        if r["kind"] in ("open", "git") and pass_class(r["path"]):
            d["files"].add(r["path"])
        elif r["kind"] == "list":
            d["dirs"].add(r["path"])
        elif r["kind"] == "leak":
            d["leak"].add(r["path"])
        elif r["kind"] == "gitlist":
            d["specs"].add(("git", r["path"]))
        elif r["kind"] == "glob":
            d["specs"].add(("glob", r["path"]))
    return out


def obs_for(obs: dict[str, dict[str, set]], name: str) -> dict[str, set] | None:
    """표의 이름(틀 포함)에 해당하는 기록을 합친다."""
    keys = [k for k in obs if k == name or ("*" in name and fnmatch.fnmatchcase(k, name))]
    if not keys:
        return None
    return {f: set().union(*(obs[k][f] for k in keys)) for f in ("files", "dirs", "leak", "specs")}


def dir_covered(d: str, globs: list[str]) -> bool:
    """A listed directory matters when a pass-class file could be added to it: covered if a
    declared glob would match a new `.md` or `.py` there."""
    base = "" if d == "." else d + "/"
    return matches(base + "__new__.md", globs) or matches(base + "__new__.py", globs)


def dir_relevant(d: str) -> bool:
    base = "" if d == "." else d + "/"
    return pass_class(base + "__new__.md")


def drift(recs: list[dict], table: dict[str, dict], names: list[str]) -> list[str]:
    fails = [f"[FAIL] gate_step_inputs — step «{n}» is in check.sh but not in {YAML.name}"
             for n in names if n not in table]
    for step, d in sorted(observed(recs).items()):
        if step == "?":                       # step() 밖의 읽기 — 단계가 아니라 also 로 돌릴 수 없다 (인쇄만)
            continue
        ent = entry(table, step)
        globs = ent["globs"] if ent else []
        if ent is None:
            if d["files"]:
                fails.append(f"[FAIL] gate_step_inputs — «{step}» read {sorted(d['files'])[0]} "
                             f"(+{len(d['files']) - 1}) and has no entry")
            continue
        for p in sorted(d["files"]):
            if not matches(p, globs):
                fails.append(f"[FAIL] gate_step_inputs — {step} read {p}, not declared")
        for dd in sorted(d["dirs"]):
            if dir_relevant(dd) and not dir_covered(dd, globs):
                fails.append(f"[FAIL] gate_step_inputs — {step} listed {dd}/, not declared")
        for kind, s in sorted(d["specs"]):   # 패턴 나열: 그 패턴이 낼 산문·코드 이름이 선언에 덮여야 한다
            miss = [q for q in probes(s, git=kind == "git") if not matches(q, globs)]
            if miss:
                fails.append(f"[FAIL] gate_step_inputs — {step} enumerated {kind} pattern {s}, not declared"
                             f" (e.g. {miss[0]})")
    return fails


def _main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] not in ("census", "check", "draft"):
        print(__doc__)
        return 2
    recs = read_log(pathlib.Path(argv[1]))
    obs = observed(recs)
    if argv[0] == "census":
        n = 0
        for step, d in sorted(obs.items()):
            dirs = sorted(x for x in d["dirs"] if dir_relevant(x))
            if not d["files"] and not dirs and not d["specs"]:
                continue
            n += 1
            print(f"  {step}: files {len(d['files'])} · dirs {len(dirs)} · git pathspecs {len(d['specs'])}")
            for kind, s in sorted(d["specs"]):
                print(f"      {kind}: {s}{'' if probes(s, git=kind == 'git') else '  (no pass-class name)'}")
            for p in sorted(d["files"]):
                print(f"      {p}")
            for x in dirs:
                print(f"      {x}/ (listed)")
            for p in sorted(d["leak"]):
                print(f"      ⚠ also imported by this process: {p}")
        print(f"[census] steps with a non-empty pass-class input set: {n} · steps seen {len(obs)}")
        return 0
    if argv[0] == "draft":
        for step in step_names():
            d = obs_for(obs, step)
            if d is None:
                print(f'"{step}":\n  globs: []   # not seen by the hook — hand entry needed?\n  hand: true')
                continue
            pats = [("**" + s[1:] if s.startswith("*") and not s.startswith("**") else s) if k == "git" else s
                    for k, s in sorted(d["specs"]) if probes(s, git=k == "git")]
            globs = pats + sorted(d["files"]) + sorted(f"{x}/*" for x in d["dirs"] if dir_relevant(x))
            print(f'"{step}":\n  globs: {json.dumps(globs, ensure_ascii=False)}')
        return 0
    table = load()
    fails = drift(recs, table, step_names())
    for f in fails:
        print(f"  {f}")
    unread = [(n, g) for n, e in table.items() if not e["hand"] for g in e["globs"]
              if not any(matches(p, [g]) for p in (obs_for(obs, n) or {}).get("files", ()))
              and not any(dir_covered(x, [g]) for x in (obs_for(obs, n) or {}).get("dirs", ()))]
    for n, g in unread:
        print(f"  [선언만] {n}: {g} — this run never read it (printed only)")
    hand = [n for n, e in table.items() if e["hand"]]
    print(f"  [손 선언] {len(hand)} — {' · '.join(hand) if hand else '-'}")
    if not fails:
        print(f"  [PASS] gate_step_inputs — every pass-class read is declared · steps {len(table)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    raise SystemExit(_main(sys.argv[1:]))
