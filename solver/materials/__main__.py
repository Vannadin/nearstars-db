# 물질 추가 명령 — new(빈 기록 뼈대) · check(적재 검사를 평이한 말로) · add-source(PDF 해시를 출처 목록에) (phase-2 impl note 3 C1–C3)
"""Adding a material by hand, with no AI and no seat protocol (rewrite/phase2-impl.frozen.md note 3 Part C).

    python -m solver.materials new <kind> <id>        write solver/materials/<id>.yaml, every field present, commented
    python -m solver.materials check [<id> ...|--all] run every load check; report field / what is wrong / how to fix
    python -m solver.materials add-source <pdf> --citation "<author year, title, journal>" [--label <name>]
                                                      register a PDF: sha256 → provenance stub → sources.yaml row

Kinds for `new`: single, branched, hand_over, table. `assemblage` records are not built in phase 2.
Exit code: 0 when everything checked loads, 1 otherwise.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

from solver import material_registry as mr
from solver.yamlio import LoadError, parse

SCHEMA_TEXT = (mr.MATERIALS_DIR / "schema.yaml").read_text(encoding="utf-8")
_SECTION = re.compile(r"^([a-z_]+):\s*(?:#.*)?$")
_KEY = re.compile(r"^  ([a-z_0-9]+):\s*\{.*?\}?\s*(?:#\s*(.*))?$")


def schema_comments() -> dict:
    """(section, key) → the schema line's own comment, so the scaffold cannot drift from the schema."""
    out, sec = {}, None
    for line in SCHEMA_TEXT.splitlines():
        m = _SECTION.match(line)
        if m:
            sec = m.group(1)
            continue
        m = _KEY.match(line)
        if m and sec:
            out[(sec, m.group(1))] = (m.group(2) or "").strip()
    return out


# ── new: the scaffold ───────────────────────────────────────────────────────────────────────────────────────
def _placeholder(spec, sec, key, comments) -> str:
    what = comments.get((sec, key), "")
    shape = spec["shape"]
    if shape == "number":
        unit = spec.get("unit")
        return f"FILL: a number in SI{f' ({unit})' if unit else ''}{f' — {what}' if what else ''}"
    if shape == "enum":
        return f"FILL: one of {list(spec['values'])}{f' — {what}' if what else ''}"
    return f"FILL: {what or key}"


def _emit(sec: str, ind: str, lines: list, comments: dict, only=None, overrides=None):
    """Emit section `sec` at indent `ind`: required keys filled with placeholders, optional ones commented."""
    spec = mr.SCHEMA[sec]
    overrides = overrides or {}
    for key, ks in spec.items():
        if only is not None and key not in only:
            continue
        note = comments.get((sec, key), "")
        tail = f"  # {note}" if note else ""
        if key in overrides:
            lines.append(f"{ind}{key}: {overrides[key]}{tail}")
            continue
        if not ks.get("required"):
            lines.append(f"{ind}# {key}: (optional){tail}")
            continue
        shape, sub = ks["shape"], ks.get("of")
        if shape == "source":
            lines.append(f"{ind}{key}:{tail}   # exactly one of cache / library / doi / formula / user_declared")
            lines.append(f'{ind}  cache: "FILL: the registered PDF file name (python -m solver.materials add-source)"')
            lines.append(f'{ind}  page: "FILL: the printed page"')
            lines.append(f'{ind}  where: "FILL: the table, equation or figure"')
            lines.append(f'{ind}  sha256: "FILL: printed by add-source"')
            lines.append(f"{ind}  # library: name@version · doi: doi:10.… · formula: <formula and inputs> · "
                         "user_declared: <reason>")
            continue
        if shape in ("record", "constant"):
            lines.append(f"{ind}{key}:{tail}")
            _emit(sub or shape, ind + "  ", lines, comments)
        elif shape == "list" and sub:
            lines.append(f"{ind}{key}:{tail}")
            lines.append(f"{ind}  -")
            _emit(sub, ind + "    ", lines, comments)
        elif shape == "mapping":
            lines.append(f"{ind}{key}: {{}}{tail}   # FILL as name: value pairs")
        else:
            lines.append(f"{ind}{key}: \"{_placeholder(ks, sec, key, comments)}\"")


def scaffold(kind: str, material_id: str) -> str:
    if kind == "assemblage":
        raise SystemExit("assemblage records are not built in phase 2 (design D-P2 is a later step)")
    if kind not in ("single", "branched", "hand_over", "table"):
        raise SystemExit(f"kind is one of single, branched, hand_over, table; got {kind!r}")
    lines = [f"# {material_id} — material record written by `python -m solver.materials new {kind}`.",
             "# Replace every FILL with the value read from your source; uncomment optional keys you need.",
             "# Then run: python -m solver.materials check " + material_id, ""]
    comments = schema_comments()
    rec_kind = "single" if kind == "table" else kind
    _emit("record", "", lines, comments, only=("id", "label", "kind", "system", "fit_composition"),
          overrides={"id": material_id, "kind": rec_kind})
    lines.append("phases:")
    for n in range(2 if kind in ("branched", "hand_over") else 1):
        lines.append(f"  -   # phase {n + 1}")
        over = {"form": "table"} if kind == "table" else {}
        _emit("phase", "    ", lines, comments, only=("id", "label", "state"))
        lines.append("    eos:")
        _emit("eos", "      ", lines, comments, only=("form", "params", "reference") + (("table",) if kind == "table" else ()),
              overrides=over)
        if kind == "table":
            lines.append("      table:")
            _emit("table", "        ", lines, comments)
        for part in ("thermal", "field", "window"):
            lines.append(f"    {part}:")
            _emit(mr.SCHEMA["phase"][part]["of"], "      ", lines, comments)
        lines.append("    edges:   # one entry per finite window edge the field passes: {refusal: input.material_out_of_data}")
        lines.append("             # or {band: {form, error, grade, origin}}")
        lines.append("      t_min: {refusal: input.material_out_of_data}")
        lines.append("      t_max: {refusal: input.material_out_of_data}")
    if kind == "branched":
        lines.append("boundaries:")
        lines.append("  -")
        _emit("boundary", "    ", lines, comments)
    if kind == "hand_over":
        lines.append("joins:")
        lines.append("  -")
        _emit("join", "    ", lines, comments)
    lines.append("formula_checks:")
    lines.append("  -")
    _emit("formula_check", "    ", lines, comments)
    return "\n".join(lines) + "\n"


# ── check: plain-words report ───────────────────────────────────────────────────────────────────────────────
def _what(stop: mr.LoadStop) -> str:
    ev = dict(stop.evidence)
    ev.pop("file", None)
    where = ev.pop("path", None) or (f"phase {ev.pop('phase')}" if "phase" in ev else "")
    rest = "; ".join(f"{k} = {v}" for k, v in ev.items())
    return f"{where or '(record)'}: {stop.id.split('.', 1)[1].replace('_', ' ')}{f' — {rest}' if rest else ''}"


def check(paths: list, directory: Path = mr.MATERIALS_DIR) -> int:
    registered = mr.read_manifest(directory / "sources.yaml")
    if isinstance(registered, mr.LoadStop):
        print(f"sources.yaml: {_what(registered)}\n  how to fix: {registered.fix}")
        return 1
    bad = 0
    for f in paths:
        try:
            raw = parse(Path(f).read_text(encoding="utf-8"))
        except (LoadError, OSError) as e:
            print(f"{Path(f).name}: unreadable — {e}\n  how to fix: {mr.STOPS['material.unreadable'][1]}")
            bad += 1
            continue
        out = mr.check_record(raw, Path(f).name, registered)
        if isinstance(out, mr.LoadStop):
            print(f"{Path(f).name}: {_what(out)}\n  how to fix: {out.fix}")
            bad += 1
        else:
            print(f"{Path(f).name}: loads")
    whole = mr.load(directory)
    if isinstance(whole, mr.LoadStop) and not bad:
        print(f"registry: {_what(whole)}\n  how to fix: {whole.fix}")
        bad += 1
    return 1 if bad else 0


# ── add-source: register a PDF ──────────────────────────────────────────────────────────────────────────────
def add_source(pdf: Path, citation: str, label: str | None, manifest: Path = mr.MATERIALS_DIR / "sources.yaml") -> int:
    if not pdf.is_file():
        print(f"{pdf}: no such file")
        return 1
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    have = mr.read_manifest(manifest)
    if isinstance(have, mr.LoadStop):
        print(f"sources.yaml: {_what(have)}\n  how to fix: {have.fix}")
        return 1
    if sha in have:
        print(f"{pdf.name}: already registered (sha256 {sha})")
        return 0
    name = label or pdf.name
    today = datetime.date.today().isoformat()
    stub = pdf.with_name(pdf.name + ".PROVENANCE.txt")
    existing = pdf.with_name(pdf.stem + ".PROVENANCE.txt")      # the paper cache's own naming
    route = "user-supplied"
    if existing.exists():                                     # 68 N2: a cached paper keeps its own provenance and route
        stub, route = existing, f"paper cache ({existing.name})"
    body = manifest.read_text(encoding="utf-8") if manifest.exists() else "sources:\n"
    body = body.replace("sources: []", "sources:")
    if body[-1:] != "\n":
        body += "\n"
    q = lambda x: '"' + x.replace("\\", "\\\\").replace('"', '\\"') + '"'          # noqa: E731
    body += (f"  - {{name: {q(name)}, sha256: {sha}, citation: {q(citation)}, route: {q(route)}, "
             f"date: {q(today)}}}\n")
    again = mr.manifest_shas(body)                    # checked in memory first; the file is written only if it reads back
    if isinstance(again, mr.LoadStop) or sha not in again or not have <= again:
        print("sources.yaml: the new row would not read back (is there content after the sources list?); "
              "nothing was written — add the row by hand under `sources:`")
        return 1
    if stub is not existing and not stub.exists():           # 68 N1: nothing is written before the check passes
        stub.write_text(f"file: {pdf.name}\nsha256: {sha}\nsize: {pdf.stat().st_size} B\nlabel: {name}\n"
                        f"citation: {citation}\nroute: user-supplied\nregistered: {today} by "
                        "`python -m solver.materials add-source`\n", encoding="utf-8")
    manifest.write_text(body, encoding="utf-8")
    print(f"{pdf.name}: registered, sha256 {sha}\n  cite it as: {{cache: {pdf.name}, page: <printed page>, "
          f"where: <table or eq.>, sha256: {sha}}}\n  provenance stub: {stub}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m solver.materials", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="write a new record scaffold")
    n.add_argument("kind")
    n.add_argument("id")
    c = sub.add_parser("check", help="check records and report problems in plain words")
    c.add_argument("ids", nargs="*")
    c.add_argument("--all", action="store_true")
    a = sub.add_parser("add-source", help="register a PDF in sources.yaml")
    a.add_argument("pdf", type=Path)
    a.add_argument("--citation", required=True)
    a.add_argument("--label")
    args = ap.parse_args(argv)
    if args.cmd == "new":
        dest = mr.MATERIALS_DIR / f"{args.id}.yaml"
        if dest.exists():
            print(f"{dest} exists; not overwritten")
            return 1
        dest.write_text(scaffold(args.kind, args.id), encoding="utf-8")
        print(f"wrote {dest}\nnext: replace every FILL, then python -m solver.materials check {args.id}")
        return 0
    if args.cmd == "check":
        files = sorted(f for f in mr.MATERIALS_DIR.glob("*.yaml") if f.name not in mr.NOT_RECORDS) if args.all \
            else [mr.MATERIALS_DIR / f"{i}.yaml" for i in args.ids]
        if not files:
            print("nothing to check: give record ids or --all")
            return 1
        return check(files)
    return add_source(args.pdf, args.citation, args.label)


if __name__ == "__main__":
    sys.exit(main())
