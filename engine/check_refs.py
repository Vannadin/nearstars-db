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

Three kinds of citation are counted but never migrated: one that names a whole document (the payload
is pinned by the edge's own `via:`), one into a paper's own source in the gitignored cache, and one
inside a note that declares itself a verbatim record — that note's line numbers were true when it was
written, and rewriting them would edit the evidence.

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
# Everything that POINTS INTO a file: a file name immediately followed by `:` or `@`. Every one of
# these must fall into one of the known forms; one that does not is a citation form nobody taught the
# checker, and the checker must say so rather than skip it. Three arrived that way — `<doc>.md:Contract`
# — and sat in no bucket at all: not an anchor, not a line number, not a whole-document ref, absent
# from the report, gate green. That is the same failure as the unparseable YAML and the citation in a
# comment: the checker not saying that it did not look.
# "points into" means the colon is followed immediately by the target — `foo.md:123`, `foo.md:Contract`,
# `foo.md@«…»`. A colon followed by a space is prose introducing a file ("chain.yaml: outputs rewritten"),
# and `module.py::function` names a symbol, not a place; neither is a citation.
POINTER = re.compile(rf"({FILE})(?::(?![\s:])|@|#)")

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


# A paper's own source lives in the gitignored cache, so it cannot be anchored here; that is a
# classification, not a defect, and the listing must not offer it as work.
EXT = re.compile(r"\.tex$")
PRESERVED = re.compile(r"Preserved verbatim|원문 무편집|body unedited|from the parallel seat's scratch")


def is_preserved(path: Path) -> bool:
    """A note that declares itself a verbatim record of what someone measured at a moment.

    Its citations are part of the record: they were true when written, and rewriting them would edit
    the evidence. They are counted apart so that "unmigrated → 0" stays a reachable target."""
    if path.suffix != ".md":
        return False
    return bool(PRESERVED.search("\n".join(text(path).splitlines()[:6])))


def own_doc(path: Path) -> str | None:
    """The doc a module's bare `doc :N` / `doc @«…»` means: its own declared RECIPE."""
    if path.suffix != ".py":
        return None
    m = RECIPE_DECL.search(text(path))
    return f"{m.group(1)}.md" if m else None


BASENAMES: dict[str, list[Path]] = {}


def sharing_the_name(bare: str) -> list[Path]:
    """Every file in the repo with this base name."""
    if not BASENAMES:
        # `ko/` holds a translation of the same document, not a different file, so a mirror is not a
        # second meaning; caches and archives are not citable targets at all.
        skip = {".git", "ko", ".archive", "_papers", "node_modules", ".venv"}
        for q in ROOT.rglob("*"):
            if q.is_file() and not (skip & set(q.parts)):
                BASENAMES.setdefault(q.name, []).append(q)
    return BASENAMES.get(bare, [])


def ambiguous(doc: str) -> list[Path]:
    """The candidates a bare name could mean, when it could mean more than one.

    Resolution used to walk `docs/reference` → the citing file's directory → `engine/` → the repo
    root and stop at the first hit, so a citation to `checklist.md` quietly meant whichever one sat
    next to the citing file — and the repo has 68 of those, 68 `context-notes.md`, 22 `README.md`.
    Choosing by proximity is choosing without saying so, which is the thing this checker exists to
    stop. A bare name that could mean more than one file is now a failure, and the fix is to write
    the path."""
    if "/" in doc:
        return []
    found = sharing_the_name(doc)
    return found if len(found) > 1 else []


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
        return "a name no file in the repo has"
    lines = text(target).splitlines()
    n = int(re.split(r"[-–]", loc)[0])
    if not (1 <= n <= len(lines)):
        return "a line past the end of the document"
    raw = lines[n - 1]
    body = raw.strip()
    if not body:
        return "a blank line"
    if re.fullmatch(r"\|[\s\-:|]+\|", body):
        return "a table separator"
    if re.fullmatch(r"-{3,}|_{3,}|\*{3,}", body):
        return "a horizontal rule"
    if body.startswith("**Needs**") or body.startswith("**Returns**"):
        return "a contract Needs/Returns line"
    if body.startswith("#"):
        return "a heading"
    if body.startswith("|"):
        return "a table row"
    if re.match(r"^\d+\. \[", body):
        return "a table-of-contents row"
    # a `## Related` list item: a bullet inside that section
    before = "\n".join(lines[:n - 1])
    section = before.rfind("\n## ")
    if section != -1 and before[section:section + 20].startswith("\n## Related") and body.startswith("-"):
        return "a Related list item"
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


UNWRAP = re.compile(r"\n[ \t]*(?=\S)")


def unwrapped(t: str) -> str:
    """The document with its hard wrapping folded: a newline plus the following indent becomes one
    space, and nothing inside a line is touched. The methodology docs wrap prose at ~80 columns, so a
    sentence-long anchor cannot fit on one line otherwise; the alternative, normalising whitespace
    generally, would throw away the strictness that is doing work — `⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴`
    is unique only with its double spaces."""
    return UNWRAP.sub(" ", t)


def resolve(doc: str, phrase: str, citing: Path) -> tuple[str, int]:
    target = target_of(doc, citing)
    if target is None:
        return "a name no file in the repo has", 0
    body = unwrapped(text(target))
    n = body.count(phrase)
    # A phrase containing a double quote has to live in a single-quoted YAML scalar, where an
    # apostrophe is written twice. The raw-line scan reads YAML source rather than parsed values, so
    # it sees that doubling; the document does not have it.
    if n == 0 and "''" in phrase:
        n = body.count(phrase.replace("''", "'"))
    # A file may cite itself — radiogenic.py's heat-pipe refusal names the function it is decided in,
    # and that string ships as a result value. Writing the anchor puts the phrase in the file a second
    # time, so its own occurrences inside `@«…»` do not count as places the citation could mean.
    if target == citing:
        n -= body.count(f"@«{phrase}»")
    return "", n


class BrokenYAML(Exception):
    """A YAML file whose citations could not be read at all."""


def yaml_units(path: Path):
    """(label, endpoints, string) for every string in a YAML file, from the PARSED document.

    ④ The raw-line scan cannot see a citation that a folded `note: >` block splits across two lines:
    no match, no count, no failure. chain.yaml carries sixteen folded blocks, so the path is real.
    Reading the parsed values closes it, and for chain.yaml it also gives each citation its edge's
    endpoints exactly, instead of a regex over the citing line."""
    try:
        doc = yaml.safe_load(text(path))
    except Exception as exc:
        # Silence here is the disease this checker exists to end: with the parse failing, the citations
        # simply were not read, and a report of "0 failures" over 8 % of them is worse than no report.
        raise BrokenYAML(f"{path.relative_to(ROOT)} does not parse, so its citations were not read: {exc}")
    # only the key the citations actually live under: refs hang off edges, never off nodes
    expected = {"engine/chain.yaml": ("edges",)}.get(str(path.relative_to(ROOT)), ())
    missing = [k for k in expected if not isinstance(doc, dict) or k not in doc]
    if missing:
        raise BrokenYAML(f"{path.relative_to(ROOT)} parses but has no {', '.join(missing)} — "
                         f"its citations were not where they were looked for")
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
    ambiguous_a: list[str] = []
    mismatched: list[str] = []          # rule 2: landed inside another node's contract block
    whole = 0                           # refs that cite a whole document, which is a legitimate form
    external = 0                        # citations into a paper's own source, outside this repo
    unaimed: list[str] = []             # ⑤ whole-document refs: legitimate, but aimed at nothing inside
    preserved = 0                       # citations inside verbatim notes: the record, not a migration target
    quoted_n = 0                        # citations inside quoted material: the quote's, not the note's
    quoted: dict[tuple, bool] = {}
    ambig: list[str] = []               # a bare file name that could mean more than one file
    unknown: list[str] = []             # pointers into a file that match no known citation form
    shared: dict[tuple[str, str], list[tuple[str, list[str]]]] = {}   # anchor → the edges that share it
    dead: list[str] = []                # rule 3: a landing that cannot have been intended
    warned: list[str] = []              # rule 3: a landing that moves easily but may well be meant
    # L-3, narrowed 2026-09-05 after measurement: of 91 anchors without their payload's name, a hand
    # check of 20 found ZERO genuinely loose aims — all three failure sources were structural (unicode
    # symbols, capitalisation, and the heading anchors we chose on purpose). Narrowed to case-folded
    # token equality, a one-line window, and no headings, it catches **nothing in this repo today**,
    # and that is the rule being right rather than idle: it is the net under a future mis-aim, and it
    # costs nothing to keep. Do not delete it for being quiet.
    warned_aim: list[str] = []
    # A preserved note is exempt in EVERY citation form, not only the line-number one. The exemption
    # has to hold on the anchor path too, or the migration programme reaches such a note, rewrites a
    # citation into an anchor, and the only way back to green is editing the preserved record —
    # exactly what "preserved" forbids.
    note_name: list[str] = []           # an ambiguous bare name inside a preserved note
    note_rot: list[str] = []            # an anchor or form inside a preserved note that no longer resolves
    note_dead: list[str] = []           # rule 3 in a preserved note: dead, but a note records what was
    unmigrated: list[tuple] = []
    ok = 0

    live = {".py", ".yaml"}             # wiring and code must resolve; a note records what was true then
    for path in files():
        rel = path.relative_to(ROOT)
        mine = own_doc(path)
        ends: tuple[str, str] = ("", "")
        raw_lines = text(path).splitlines()
        # value → the endpoints of each edge that uses it, in document order: two edges can carry the
        # same ref, and collapsing them would evaluate the second against the first one's endpoints.
        by_value: dict[str, list[tuple]] = {}
        units = []
        if path.suffix in (".yaml", ".yml"):
            try:
                parsed = yaml_units(path)
            except BrokenYAML as exc:
                rotten.append(f"{rel}: {exc}")
                parsed = []
            # A citation the raw scan can see is counted there, with its line number. A citation the raw
            # scan CANNOT see — folded across lines by a `note: >` block — is counted from the parsed
            # value. The union covers both, and keeps YAML comments visible: parsing drops them, and
            # "write it in a comment and it goes quiet" is a path this checker must not reopen.
            for label, e, val, vias in parsed:
                if not any(val in line for line in raw_lines):
                    units.append((f"{rel} {label} (folded)", e, val, vias))
                # An edge written as a block mapping puts `from:`, `to:` and each ref on separate
                # lines, so a regex over the citing line sees no endpoints and would inherit the last
                # flow-style edge's — a false contract-owner mismatch. The parsed value knows them.
                by_value.setdefault(val, []).append((e, vias))
        ends_seen: tuple[str, str] = ("", "")
        for i, line in enumerate(raw_lines, 1):
            m = EDGE.search(line)
            if m:
                ends_seen = (m.group(1), m.group(2))
            vias_here = []
            for g in re.findall(r"via: (\[[^\]]*\]|[a-z_0-9]+)", line):
                vias_here += [v.strip(" []") for v in g.split(",") if v.strip(" []")]
            units.append((f"{rel}:{i}", ends_seen if path.suffix in (".yaml", ".yml") else ("", ""), line,
                          vias_here))
        for where0, ends, line, via_names in units:
            hits = [(m.group(1), m.group(2)) for m in ANCHOR.finditer(line)]
            for m in SELF_ANCHOR.finditer(line):
                # The bare form is only ever the module's OWN document. radiogenic.py used it for the
                # tidal document's section 6.2 table, so the citation named the wrong document while
                # looking right; a citation that crosses documents has to say which one.
                if mine:
                    hits.append((mine, m.group(1)))
                else:
                    (note_rot if is_preserved(path) else rotten).append(
                        f"{where0}: doc @«{m.group(1)[:50]}» — a bare `doc` citation in a file "
                        f"that declares no RECIPE; name the document")
            for doc, phrase in hits:
                if ambiguous(doc):
                    others = ", ".join(str(q.relative_to(ROOT)) for q in ambiguous(doc)[:4])
                    row = (f"{where0}: {doc}@«{phrase[:40]}» — {len(ambiguous(doc))} files share that "
                           f"name ({others}…); write the path")
                    (note_name if is_preserved(path) else ambig).append(row)
                    continue
                queue = by_value.get(f"{doc}@«{phrase}»")
                ends = queue.pop(0)[0] if queue else ends
                why, n = resolve(doc, phrase, path)
                where = f"{where0}: {doc}@«{phrase[:60]}»"
                bucket = note_rot if is_preserved(path) else None
                if why:
                    (bucket if bucket is not None else rotten).append(f"{where} — {why}")
                elif n == 0:
                    (bucket if bucket is not None else rotten).append(f"{where} — no such phrase in {doc}")
                elif n > 1:
                    (bucket if bucket is not None else ambiguous_a).append(
                        f"{where} — matches {n}x, the anchor cannot say which")
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
                for m in WHOLE.finditer(line):
                    if target_of(m.group(1), path) is None:
                        rotten.append(f"{where0}: {m.group(1)} — no file in the repo has that name")
                    else:
                        whole += 1
                        unaimed.append(f"{where0}: {m.group(1)} — cites the whole document")
            classified = {m.start() for m in ANCHOR.finditer(line)}
            classified |= {m.start() for m in LINE_REF.finditer(line)}
            for m in POINTER.finditer(line):
                if m.start() not in classified:
                    (note_rot if is_preserved(path) else unknown).append(
                        f"{where0}: {line[m.start():m.start() + 60].strip()} — a citation form "
                        f"this checker does not know; it was counted in no bucket")
            near = "\n".join(raw_lines[max(0, i - 3):i]) if where0.endswith(str(i)) else ""
            # A quotation is a record only if it says WHEN it was true. Without a date, `*"…"` and a
            # `>` blockquote are just quotation marks, and "wrap it and the checker goes quiet" is a
            # path this must not open. The date may sit in the marker or in the quoted block itself.
            DATE = r"\d{4}-\d{2}-\d{2}"
            marker = re.search(r'\*"|^\s*>|note \(' + DATE + r'\):', line) or re.search(r'\*"|^\s*>', near)
            in_quote = bool(marker and (re.search(DATE, line) or re.search(DATE, near)))
            for m in LINE_REF.finditer(line):
                if ambiguous(m.group(1)):
                    others = ", ".join(str(q.relative_to(ROOT)) for q in ambiguous(m.group(1))[:4])
                    row = (f"{where0}: {m.group(0)} — {len(ambiguous(m.group(1)))} files share that "
                           f"name ({others}…); write the path")
                    # In a preserved note the citation is a record of what someone wrote, so an
                    # ambiguous name there is reported, not failed.
                    (note_name if is_preserved(path) else ambig).append(row)
                    continue
                if in_quote:
                    quoted[(where0, m.group(1), m.group(2))] = True
                queue = by_value.get(f"{m.group(1)}:{m.group(2)}")
                unmigrated.append((where0, m.group(1), m.group(2), path,
                                   queue.pop(0)[0] if queue else ends))
            for m in SELF_LINE.finditer(line):
                if mine:
                    unmigrated.append((where0, mine, m.group(1), path, ends))
                else:
                    rotten.append(f"{where0}: doc :{m.group(1)} — a bare `doc` citation in a file that "
                                  f"declares no RECIPE; name the document")

    DEAD = {"a blank line", "a table separator", "a horizontal rule", "a table-of-contents row",
            "a line past the end of the document", "a name no file in the repo has"}
    # A paper's own source is cited the same way but lives in the gitignored paper cache, so it cannot
    # be resolved here. That is not rot: it is a citation into something outside the repo, like a
    # bibcode, and it is counted as such rather than failed.
    EXTERNAL = EXT
    MOVES = {"a table row", "a heading", "a Related list item", "a contract Needs/Returns line"}
    kinds: dict[str, int] = {}
    for where, doc, loc, citing, ends in unmigrated:
        if is_preserved(citing):
            preserved += 1
            continue
        record = quoted.get((where, doc, loc))
        if record:
            # This repo quotes past state verbatim on purpose — context-notes-log, provenance blocks,
            # a note reproducing the edge text of the day. Rewriting such a citation would edit the
            # quotation, so it is not migration work. It is still resolved: an exemption from being
            # rewritten is not an exemption from being checked, or wrapping a citation in quotes
            # would turn a failure green.
            quoted_n += 1
        kind = lands_on(doc, loc, citing)
        kinds[kind] = kinds.get(kind, 0) + 1
        owner = contract_owner(doc, citing, line_no=int(re.split(r"[-–]", loc)[0])
                               if kind not in ("a name no file in the repo has", "a line past the end of the document") else None)
        if owner and ends != ("", "") and owner not in ends:
            mismatched.append(f"{where}: {doc}:{loc} — lands in {owner}'s contract block, "
                              f"but this edge runs {ends[0]} → {ends[1]}")
        elif EXTERNAL.search(doc):
            external += 1
        elif kind in DEAD:
            row = f"{where}: {doc}:{loc} — lands on {kind}, which cannot have been the intent"
            if record:
                row += " (inside a dated quotation: report, do not rewrite — the quotation stands)"
            # Only a file that DECLARES itself a preserved record is exempt from failing. A quotation
            # inside a living document is not: the fact that its citation now points at nothing is
            # true whether or not the sentence around it is a quotation.
            (note_dead if is_preserved(citing) else dead).append(row)
        elif kind in MOVES:
            warned.append(f"{where}: {doc}:{loc} — lands on {kind}, which moves when the document grows")

    print(f"인용 점검 — 앵커 {ok + len(rotten) + len(ambiguous_a)}건 (해석 성공 {ok}) · "
          f"문서 전체 인용 {whole}건 · 레포 밖 인용 {external}건 · 보존 노트 인용 {preserved}건 · "
          f"인용문 안 인용 {quoted_n}건 · 미이행 줄번호 {len(unmigrated) - external - preserved - quoted_n}건 · "
          f"문서 {len(list(DOCS.glob('*.md')))}종")
    for label, rows in (("썩은 앵커", rotten), ("애매한 앵커", ambiguous_a),
                        ("계약 주인 불일치", mismatched), ("있을 수 없는 착지", dead),
                        ("알 수 없는 인용 형식", unknown), ("모호한 문서 이름", ambig)):
        for r in rows:
            print(f"  [FAIL] {label} — {r}")
    for (doc, phrase), users in sorted(shared.items()):
        # L-3: a value cited by two or more edges is where inheritance happened — heat:119 was cited
        # thirty times. If the anchored sentence does not literally name the payload an edge wants,
        # that edge is aiming loosely; measured 8/8 on the reused targets, and useless on single-use
        # ones (most of those cite prose that names nothing). A warning, not a failure: a sentence can
        # be the right place without spelling the field name.
        if len(users) < 2 or phrase.lstrip().startswith("#"):
            # A heading anchor is exempt: a section title is not supposed to spell a field name, and
            # heading anchors are what this project deliberately chose for the contract blocks.
            continue
        window = phrase
        target = target_of(doc, ROOT / "engine" / "chain.yaml")
        if target is not None:                     # ⑤ one line past the anchor counts as naming it
            body = unwrapped(text(target))
            at = body.find(phrase)
            if at >= 0:
                # to the end of the paragraph the anchor sits in: after folding, "one line further"
                # is the rest of that paragraph, and a document names its payload in the sentence
                # around the formula as often as in the formula itself
                end = body.find("\n\n", at)
                window = body[at:end if end > at else at + len(phrase) + 240]
        words = {w.lower() for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", window)}
        for where0, via_names in users:
            # token equality, case-folded: a substring test made "ref" match inside "reference", which
            # silenced eight anchors. Symbol-versus-name (`k2_over_q` against `k₂/Q`) is NOT bridged —
            # a symbol dictionary would cost more upkeep than the rule is worth.
            if not any(v.lower() in words for v in via_names):
                warned_aim.append(f"{where0}: {doc}@«{phrase[:50]}» — shared by {len(users)} edges and does "
                                  f"not name {'/'.join(via_names)}, the payload this one wants")
    for w in warned:
        print(f"  [WARN] 쉽게 밀리는 착지 — {w}")
    for w in warned_aim:
        print(f"  [WARN] 느슨한 조준 — {w}")
    for w in note_name:
        print(f"  [WARN] 보존 노트의 모호한 이름 — {w}")
    for w in note_rot:
        print(f"  [WARN] 보존 노트의 안 풀리는 인용 — {w}")
    for w in note_dead:
        print(f"  [WARN] 노트 안의 죽은 착지 — {w}")
    if listing:
        for u in unaimed:
            print(f"  [미조준] {u}")
    if unmigrated and (listing or suspect):
        for where, doc, loc, citing, _ends in unmigrated:
            if listing or lands_on(doc, loc, citing) != "body text":
                tag = ("보존" if is_preserved(citing)
                       else "외부" if EXT.search(doc)
                       else "인용문" if quoted.get((where, doc, loc)) else "미이행")
                print(f"  [{tag}] {where}: {doc}:{loc} — lands on {lands_on(doc, loc, citing)}")
        print("  미이행 착지 종류: " + " · ".join(f"{k} {v}" for k, v in sorted(kinds.items(), key=lambda x: -x[1])))
        print("  (본문 착지가 정답을 뜻하지는 않는다 — heat:119 부류가 정확히 그랬다. 종류는 의심의 순서일 뿐이다.)")
    bad = len(rotten) + len(ambiguous_a) + len(mismatched) + len(dead) + len(unknown) + len(ambig)
    if bad:
        print(f"[FAIL] 인용 {bad}건이 해석되지 않는다")
        return 1
    # C33 이 끝나면 여기서 미이행 0 을 요구하도록 조인다.
    print(f"  [PASS] 앵커 {ok}건 전부 대상 문서에서 정확히 1회 매치 · 문서 전체 인용 {whole}건 · "
          f"보존 노트 인용 {preserved}건 · 인용문 안 인용 {quoted_n}건은 기록이라 이행 대상이 아니다 · "
          f"미이행 {len(unmigrated) - external - preserved - quoted_n}건은 배치 이행 대기")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
