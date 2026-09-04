# 인용을 열거·해석·판정한다 — 앵커 구절이 대상 문서에서 정확히 1회 매치되는지 (C33)
"""Resolve every citation in the engine against the document it names.

    python3 engine/check_refs.py            # report + verdict
    python3 engine/check_refs.py --list     # also list every citation it found
    python3 engine/check_refs.py --suspect  # classify the unmigrated ones by what their line lands on

A line number is not a citation, it is a bet that the document will not grow. It keeps losing:
`internal-heat-luminosity-methodology.md:119` was a contract block's Needs line when 30 edges were
drawn against it, then another block's Needs line, and then — inside the very commit that went to
*fix* citations (25980fdc) — a Returns line. Nothing failed at any step, because nothing resolved
the number. So the engine cites **phrases**, and this checker makes the citation carry its own test.

The anchor form, everywhere (chain.yaml, code comments and strings, notes):

    <doc>.md@«a phrase that occurs exactly once in that document»

and, inside a recipe module that declares `RECIPE = "<slug>"`, the same thing against its own doc:

    doc @«…»

Verdicts per anchor: exactly one match → ok. Zero → **rotten** (the phrase is gone or was never
there). Two or more → **ambiguous** (the anchor cannot say which place it means). Both fail.

The bare form is reserved for a module's own document, and the checker enforces it: in a file with no
`RECIPE` declaration a bare `doc` citation fails, and a phrase from some *other* document fails for
the ordinary reason (it is not in the RECIPE document). This closes the case `radiogenic.py` was in,
where a bare `doc :295–299` pointed at the tidal document's table while `doc` meant the heat one — a
citation naming the wrong document entirely, which no line number could have revealed.

Citations still written as `<doc>.md:123` or inline `doc :123` are counted as **unmigrated** and
listed, but do not fail: C33 is migrating them in batches. Tighten the last line of `main()` to
require zero once that is done.

Guillemets delimit the phrase because a phrase may contain quotes and apostrophes ("against
Earth's `T_eq ≈ 255 K`") and must survive being embedded in YAML, Python and Markdown without
escaping. The phrase is matched **verbatim**, including runs of spaces: the heat doc's
`⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴` is unique only with its double spaces.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DOCS = ROOT / "docs" / "reference"

# ① A citation can name any file in the repo, not just a lower-case .md: DANTE_HEAT_TRANSPORT_EVIDENCE.md
# carries the e_rms justification the board rests on, and boards and modules are cited too.
FILE = r"[A-Za-z0-9_./-]+\.(?:md|yaml|yml|py|json|tex|sh)"
ANCHOR = re.compile(rf"({FILE})@«([^»]*)»")
SELF_ANCHOR = re.compile(r"(?<![a-z0-9-])doc @«([^»]*)»")
# ② and a line-number citation into any of them counts as unmigrated, not only into a .md
LINE_REF = re.compile(rf"({FILE}):([0-9]+(?:[-–][0-9]+)?)")
SELF_LINE = re.compile(r"(?<![a-z0-9-])doc :([0-9]+(?:[-–][0-9]+)?)")
RECIPE_DECL = re.compile(r'^RECIPE = "([a-z0-9-]+)"', re.M)
# chain.yaml writes each edge as a one-line flow mapping, so the endpoints sit on the citing line itself
EDGE = re.compile(r"from: ([a-z_]+), to: ([a-z_]+)")
# A ref that is a bare file name cites the whole document. Two docs are cited that way on purpose:
# their payload is pinned by the edge's own `via:`, and their first line is a Korean header comment,
# so a line number there would cite the comment and an anchor would have to quote it.
# ⑤ A ref that is a bare file name cites a whole document. That is a legitimate form (the payload is
# pinned by the edge's own `via:`), but it aims at nothing inside the file, so it is counted and
# printed as its own class rather than passing invisibly.
WHOLE = re.compile(rf'"({FILE})"')

SCAN = (("engine/chain.yaml",), ("engine/bindings.yaml",), ("engine/bodies/*.yaml",),
        ("engine/*.py",), ("engine/tools/*.py",), ("engine/*.md",),
        ("scripts/**/*.py",))
CACHE: dict[Path, str] = {}


def text(path: Path) -> str:
    if path not in CACHE:
        CACHE[path] = path.read_text(encoding="utf-8")
    return CACHE[path]


# The self-test builds deliberately rotten anchors against a synthetic document; scanning them here
# would report the test's own fixtures as failures.
# This file and its test document the syntax in prose, so scanning them reports the documentation.
SKIP = {"check_refs.py", "test_check_refs.py"}


def files() -> list[Path]:
    out: list[Path] = []
    for (pattern,) in SCAN:
        out += sorted(ROOT.glob(pattern))
    return [p for p in out if p.is_file() and p.name not in SKIP]


def own_doc(path: Path) -> str | None:
    """The doc a module's bare `doc :N` / `doc @«…»` means: its own declared RECIPE."""
    if path.suffix != ".py":
        return None
    m = RECIPE_DECL.search(text(path))
    return f"{m.group(1)}.md" if m else None


def target_of(doc: str, citing: Path) -> Path | None:
    """Where a cited file name resolves. Methodology docs live in docs/reference; the engine's notes
    cite each other by bare name; boards, evidence files and modules are cited by repo path or by
    bare name from anywhere, so the search widens outward from the citing file."""
    for cand in (DOCS / doc, citing.parent / doc, ROOT / "engine" / doc, ROOT / doc):
        if cand.exists() and cand.is_file():
            return cand
    bare = Path(doc).name
    if bare == doc:                       # a bare name: look for exactly one file with it
        found = [q for q in ROOT.rglob(bare) if ".git" not in q.parts and q.is_file()]
        if len(found) == 1:
            return found[0]
    return None


def lands_on(doc: str, loc: str, citing: Path) -> str:
    """What a line-number citation currently points at. The kind is the first thing to look at when
    deciding whether a citation is worth trusting: a contract Needs/Returns line is the shape that
    rotted 30 edges at once (five blocks, near-identical lines), a `## Related` item moves whenever
    a sibling doc is added, and a blank line means the target is already gone."""
    target = target_of(doc, citing)
    if target is None:
        return "no such document"
    lines = text(target).splitlines()
    n = int(re.split(r"[-–]", loc)[0])
    if not (1 <= n <= len(lines)):
        return "past the end of the document"
    raw = lines[n - 1]
    body = raw.strip()
    if not body:
        return "blank line"
    if re.fullmatch(r"\|[\s\-:|]+\|", body):
        return "table separator"
    if re.fullmatch(r"-{3,}|_{3,}|\*{3,}", body):
        return "horizontal rule"
    if body.startswith("**Needs**") or body.startswith("**Returns**"):
        return "contract Needs/Returns line"
    if body.startswith("#"):
        return "heading"
    if body.startswith("|"):
        return "table row"
    if re.match(r"^\d+\. \[", body):
        return "table of contents"
    # a `## Related` list item: a bullet inside that section
    before = "\n".join(lines[:n - 1])
    section = before.rfind("\n## ")
    if section != -1 and before[section:section + 20].startswith("\n## Related") and body.startswith("-"):
        return "Related list item"
    return "body text"


CONTRACT = re.compile(r"^## Contract — `([a-z0-9_]+)`")


def contract_owner(doc: str, citing: Path, line_no: int | None = None, phrase: str | None = None) -> str | None:
    """The node whose `## Contract — \u0060X\u0060` block a landing falls inside, or None.

    This is the one deterministic test for the failure that rotted 30 edges: they did not land on a
    contract block by accident, they landed on **another node's** contract block. Five blocks in one
    document carry near-identical Needs lines, so nothing about the line's text gave it away."""
    target = target_of(doc, citing)
    if target is None:
        return None
    lines = text(target).splitlines()
    if phrase is not None:
        offset = text(target).find(phrase)
        if offset < 0:
            return None
        line_no = text(target)[:offset].count("\n") + 1
    if line_no is None or not (1 <= line_no <= len(lines)):
        return None
    for l in reversed(lines[:line_no]):
        if l.startswith("## "):
            m = CONTRACT.match(l)
            return m.group(1) if m else None
    return None


def resolve(doc: str, phrase: str, citing: Path) -> tuple[str, int]:
    target = target_of(doc, citing)
    if target is None:
        return "no such document", 0
    return "", text(target).count(phrase)


def yaml_units(path: Path):
    """(label, endpoints, string) for every string in a YAML file, from the PARSED document.

    ④ The raw-line scan cannot see a citation that a folded `note: >` block splits across two lines:
    no match, no count, no failure. chain.yaml carries sixteen folded blocks, so the path is real.
    Reading the parsed values closes it, and for chain.yaml it also gives each citation its edge's
    endpoints exactly, instead of a regex over the citing line."""
    try:
        doc = yaml.safe_load(text(path))
    except Exception as exc:                       # a malformed board is a different check's problem
        return [(f"{path.name}", ("", ""), f"__yaml_error__ {exc}", [])]
    out = []

    def walk(node, label, ends, vias):
        if isinstance(node, str):
            out.append((label, ends, node, vias))
        elif isinstance(node, dict):
            local = (str(node.get("from", "")), str(node.get("to", ""))) if "from" in node and "to" in node else ends
            v_here = node.get("via", vias)
            v_here = [v_here] if isinstance(v_here, str) else (v_here if isinstance(v_here, list) else vias)
            for k, v in node.items():
                walk(v, f"{label}.{k}" if label else str(k), local, v_here)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{label}[{i}]", ends, vias)

    walk(doc, "", ("", ""), [])
    return out


def main() -> int:
    listing = "--list" in sys.argv
    suspect = "--suspect" in sys.argv          # classify every unmigrated citation by what it lands on
    rotten: list[str] = []
    ambiguous: list[str] = []
    mismatched: list[str] = []          # rule 2: landed inside another node's contract block
    whole = 0                           # refs that cite a whole document, which is a legitimate form
    external = 0                        # citations into a paper's own source, outside this repo
    unaimed: list[str] = []             # ⑤ whole-document refs: legitimate, but aimed at nothing inside
    shared: dict[tuple[str, str], list[tuple[str, list[str]]]] = {}   # anchor → the edges that share it
    dead: list[str] = []                # rule 3: a landing that cannot have been intended
    warned: list[str] = []              # rule 3: a landing that moves easily but may well be meant
    unmigrated: list[tuple] = []
    ok = 0

    live = {".py", ".yaml"}             # wiring and code must resolve; a note records what was true then
    for path in files():
        rel = path.relative_to(ROOT)
        mine = own_doc(path)
        ends: tuple[str, str] = ("", "")
        if path.suffix in (".yaml", ".yml"):
            units = [(f"{rel} {label}", e, val, vias) for label, e, val, vias in yaml_units(path)]
        else:
            units = [(f"{rel}:{i}", ("", ""), line, []) for i, line in enumerate(text(path).splitlines(), 1)]
        for where0, ends, line, via_names in units:
            hits = [(m.group(1), m.group(2)) for m in ANCHOR.finditer(line)]
            for m in SELF_ANCHOR.finditer(line):
                # The bare form is only ever the module's OWN document. radiogenic.py used it for the
                # tidal document's section 6.2 table, so the citation named the wrong document while
                # looking right; a citation that crosses documents has to say which one.
                if mine:
                    hits.append((mine, m.group(1)))
                else:
                    rotten.append(f"{where0}: doc @«{m.group(1)[:50]}» — a bare `doc` citation in a file "
                                  f"that declares no RECIPE; name the document")
            for doc, phrase in hits:
                why, n = resolve(doc, phrase, path)
                where = f"{where0}: {doc}@«{phrase[:60]}»"
                if why:
                    rotten.append(f"{where} — {why}")
                elif n == 0:
                    rotten.append(f"{where} — no such phrase in {doc}")
                elif n > 1:
                    ambiguous.append(f"{where} — matches {n}x, the anchor cannot say which")
                else:
                    owner = contract_owner(doc, path, phrase=phrase)
                    if owner and ends != ("", "") and owner not in ends:
                        mismatched.append(f"{where} — lands in {owner}'s contract block, "
                                          f"but this edge runs {ends[0]} → {ends[1]}")
                    else:
                        ok += 1
                        if via_names:
                            shared.setdefault((doc, phrase), []).append((where0, via_names))
                        if listing:
                            print(f"  [ok] {where}")
            if path.suffix in (".yaml", ".yml"):
                # a whole-document ref is the entire value, not a substring of prose
                if re.fullmatch(FILE, line.strip()):
                    if target_of(line.strip(), path) is None:
                        rotten.append(f"{where0}: {line.strip()} — no such document")
                    else:
                        whole += 1
                        unaimed.append(f"{where0}: {line.strip()} — cites the whole document")
            for m in LINE_REF.finditer(line):
                unmigrated.append((where0, m.group(1), m.group(2), path, ends))
            for m in SELF_LINE.finditer(line):
                if mine:
                    unmigrated.append((where0, mine, m.group(1), path, ends))
                else:
                    rotten.append(f"{where0}: doc :{m.group(1)} — a bare `doc` citation in a file that "
                                  f"declares no RECIPE; name the document")

    DEAD = {"blank line", "table separator", "horizontal rule", "table of contents",
            "past the end of the document", "no such document"}
    # A paper's own source is cited the same way but lives in the gitignored paper cache, so it cannot
    # be resolved here. That is not rot: it is a citation into something outside the repo, like a
    # bibcode, and it is counted as such rather than failed.
    EXTERNAL = re.compile(r"(^|/)main\.tex$|\.tex$")
    MOVES = {"table row", "heading", "Related list item", "contract Needs/Returns line"}
    kinds: dict[str, int] = {}
    for where, doc, loc, citing, ends in unmigrated:
        kind = lands_on(doc, loc, citing)
        kinds[kind] = kinds.get(kind, 0) + 1
        owner = contract_owner(doc, citing, line_no=int(re.split(r"[-–]", loc)[0])
                               if kind not in ("no such document", "past the end of the document") else None)
        if owner and ends != ("", "") and owner not in ends:
            mismatched.append(f"{where}: {doc}:{loc} — lands in {owner}'s contract block, "
                              f"but this edge runs {ends[0]} → {ends[1]}")
        elif EXTERNAL.search(doc):
            external += 1
        elif kind in DEAD:
            row = f"{where}: {doc}:{loc} — lands on a {kind}, which cannot have been the intent"
            (dead if citing.suffix in live else warned).append(row)
        elif kind in MOVES:
            warned.append(f"{where}: {doc}:{loc} — lands on a {kind}, which moves when the document grows")

    print(f"인용 점검 — 앵커 {ok + len(rotten) + len(ambiguous)}건 (해석 성공 {ok}) · "
          f"문서 전체 인용 {whole}건 · 레포 밖 인용 {external}건 · 미이행 줄번호 {len(unmigrated) - external}건 · "
          f"문서 {len(list(DOCS.glob('*.md')))}종")
    for label, rows in (("썩은 앵커", rotten), ("애매한 앵커", ambiguous),
                        ("계약 주인 불일치", mismatched), ("있을 수 없는 착지", dead)):
        for r in rows:
            print(f"  [FAIL] {label} — {r}")
    for (doc, phrase), users in sorted(shared.items()):
        # L-3: a value cited by two or more edges is where inheritance happened — heat:119 was cited
        # thirty times. If the anchored sentence does not literally name the payload an edge wants,
        # that edge is aiming loosely; measured 8/8 on the reused targets, and useless on single-use
        # ones (most of those cite prose that names nothing). A warning, not a failure: a sentence can
        # be the right place without spelling the field name.
        if len(users) < 2:
            continue
        for where0, via_names in users:
            if not any(v in phrase for v in via_names):
                warned.append(f"{where0}: {doc}@«{phrase[:50]}» — shared by {len(users)} edges and does not "
                              f"name {'/'.join(via_names)}, the payload this one wants")
    for w in warned:
        print(f"  [WARN] 쉽게 밀리는 착지 — {w}")
    if listing:
        for u in unaimed:
            print(f"  [미조준] {u}")
    if unmigrated and (listing or suspect):
        for where, doc, loc, citing, _ends in unmigrated:
            if listing or lands_on(doc, loc, citing) != "body text":
                print(f"  [미이행] {where}: {doc}:{loc} — lands on a {lands_on(doc, loc, citing)}")
        print("  미이행 착지 종류: " + " · ".join(f"{k} {v}" for k, v in sorted(kinds.items(), key=lambda x: -x[1])))
        print("  (본문 착지가 정답을 뜻하지는 않는다 — heat:119 부류가 정확히 그랬다. 종류는 의심의 순서일 뿐이다.)")
    bad = len(rotten) + len(ambiguous) + len(mismatched) + len(dead)
    if bad:
        print(f"[FAIL] 인용 {bad}건이 해석되지 않는다")
        return 1
    # C33 이 끝나면 여기서 미이행 0 을 요구하도록 조인다.
    print(f"  [PASS] 앵커 {ok}건 전부 대상 문서에서 정확히 1회 매치 · 문서 전체 인용 {whole}건 · "
          f"미이행 {len(unmigrated) - external}건은 배치 이행 대기")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
