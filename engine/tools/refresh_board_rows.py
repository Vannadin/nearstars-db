# Phase 4 보드의 조석 행을 tidal_heating 레시피 emit 으로 갱신하는 도구 (C31) — 종속 행은 값 대신 날짜 붙은 stale 주석만
"""Refresh one body's tidal rows on a Phase 4 board from the `tidal_heating` recipe (C31).

    python3 engine/tools/refresh_board_rows.py --board <path/to/phase4/alpha_centauri.yaml> --body Dante [--apply]

Without `--apply` it is a dry run: it prints where every input came from, what the recipe returned, a unified diff,
and the 900-km-era text it deliberately did NOT touch. It writes nothing. `--apply` rewrites the board in place and
is the owner's separate order — the board of record is the MAIN checkout's copy, which carried uncommitted changes on
2026-09-04, so `--apply` never runs there without that order.

What it rewrites (three fields, all owned by the recipe):
- `bulk.tidal_heating` → `tidal_heating`, `tidal_surface_flux`: values from the recipe; the old value is preserved
  verbatim in a dated note ("was: …"), so nothing is deleted.
- `bulk` → `internal_heat`: an echo of the tidal_heating row, refreshed with it. The 2026-07-28 audit (C3) is the
  precedent: this echo sat at ~820× Io for two days after its owning row moved to ~1200×.

What it marks stale and does not compute (there is no recipe that partitions the heat, so a value here would be
authored): `geopotential_j2`, `surface_temperature`, `albedo`. Each gets a dated note naming what it was derived from.
Prose — narrative, evidence, divergence_note — is never edited: it is owner-approved text, and the board's numeric
fields are what the emit reads. Stale prose is listed in the dry-run report instead.

Inputs come from the board itself, each with the line it was read from, so a refresh is reproducible from the board
alone: radius and semi-major axis from the satellites (moons) table, e_rms and k₂/Q from the tidal_heating value
string, the parent mass from the parent body's own `mass` field. Edits are made on the raw lines rather than through a
YAML round-trip, so comments, ordering and quoting survive — a dumped YAML would rewrite all 3 500 lines.
"""
from __future__ import annotations

import argparse
import difflib
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))          # engine/
import tidal_heating as th  # noqa: E402

M_EARTH_KG = th.M_EARTH_KG
# Field names this tool owns, split by whether a recipe can produce the value.
REFRESHED = ("tidal_heating", "tidal_surface_flux", "internal_heat")
STALE = ("geopotential_j2", "surface_temperature", "albedo")
# Strings whose staleness the tool reports but never edits (prose, or rows another decision owns).
WATCH = (r"900\s*km", r"900,", r"8\.0e21", r"~?1200×", r"~?1200배", r"11,500", r"673 K", r"5\.7\s*%", r"2\.1 m", r"2\.4 m")


def sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=HERE, text=True).strip()
    except Exception:                     # pragma: no cover - a board can be refreshed outside a checkout
        return "unknown"


def body_ranges(lines: list[str], body: str) -> list[tuple[int, int]]:
    """(start, end) of every `- body: <body>` decision entry, in file order."""
    starts = [i for i, l in enumerate(lines) if re.match(rf"^\s*- body: {re.escape(body)}\s*(#.*)?$", l)]
    out = []
    for s in starts:
        e = s + 1
        while e < len(lines) and not re.match(r"^\s*- body: ", lines[e]):
            e += 1
        out.append((s, e))
    return out


def field_lines(lines: list[str], ranges: list[tuple[int, int]], name: str) -> list[int]:
    hits = []
    for s, e in ranges:
        for i in range(s, e):
            if re.search(rf"\{{\s*name: {re.escape(name)},", lines[i]):
                hits.append(i)
    return hits


def moons_row(lines: list[str], body: str) -> tuple[int, dict]:
    """The satellites-table row for one moon: `- { name: Dante, parent: "…", …, radius_km: 521, design: {…} }`."""
    for i, l in enumerate(lines):
        if re.search(rf"^\s*- \{{\s*name: {re.escape(body)},\s*parent:", l):
            got = {}
            for key in ("a_km", "radius_km", "mass_kg", "e"):
                m = re.search(rf"(?<![a-z_]){key}: ([\d.eE+-]+)", l)
                if m:
                    got[key] = float(m.group(1))
            m = re.search(r"design: \{([^}]*)\}", l)
            if m:
                for key in ("a_km", "e"):
                    d = re.search(rf"(?<![a-z_]){key}: ([\d.eE+-]+)", m.group(1))
                    if d:
                        got["design_" + key] = float(d.group(1))
            m = re.search(r'parent: "([^"]*)"', l)
            if m:
                got["parent"] = m.group(1)
            return i, got
    raise SystemExit(f"no satellites-table row for {body} (looked for '- {{ name: {body}, parent: …')")


def parent_mass_kg(lines: list[str], parent: str) -> tuple[float, int]:
    for i in field_lines(lines, body_ranges(lines, parent), "mass"):
        m = re.search(r"value: ([\d.eE+-]+), unit: (\w+)", lines[i])
        if not m:
            continue
        v, unit = float(m.group(1)), m.group(2)
        if unit == "M_earth":
            return v * M_EARTH_KG, i + 1
        if unit == "kg":
            return v, i + 1
    raise SystemExit(f"no mass field with unit M_earth/kg on '- body: {parent}'")


def set_value(line: str, new: str) -> str:
    return re.sub(r"(name: \w+, value: )(\"[^\"]*\"|[^,}]+)", lambda m: m.group(1) + f'"{new}"', line, count=1)


def old_value(line: str) -> str:
    """The value as it stands, unquoted — it is quoted back inside a double-quoted note, so it must carry no `"`."""
    m = re.search(r"name: \w+, value: (\"[^\"]*\"|[^,}]+)", line)
    return m.group(1).strip().strip('"') if m else "?"


def set_value_ko(line: str, new: str) -> str:
    """Refresh `value_ko` if the field has one. These particular mirrors are numbers, not prose — leaving them at the
    old figure would print a stale value to every Korean reader of the board."""
    if "value_ko:" not in line:
        return line
    return re.sub(r'(value_ko: )"[^"]*"', lambda m: m.group(1) + f'"{new}"', line, count=1)


def append_note(line: str, text: str, text_ko: str | None = None) -> str:
    """Append to the English note (adding one if absent) and, when the field already has a `note_ko`, to that too."""
    if re.search(r'note: "', line):
        line = re.sub(r'(?<!_ko)(note: ")([^"]*)(")',
                      lambda m: m.group(1) + m.group(2) + " · " + text + m.group(3), line, count=1)
    else:
        line = re.sub(r"\s*\}\s*$", f', note: "{text}" }}\n', line, count=1)
    if text_ko and "note_ko:" in line:
        line = re.sub(r'(note_ko: ")([^"]*)(")',
                      lambda m: m.group(1) + m.group(2) + " · " + text_ko + m.group(3), line, count=1)
    return line


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", required=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = Path(a.board)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    ranges = body_ranges(lines, a.body)
    if not ranges:
        raise SystemExit(f"no '- body: {a.body}' entry in {path}")

    # ── inputs, all read from the board ───────────────────────────────────────────────
    mrow, moon = moons_row(lines, a.body)
    th_rows = field_lines(lines, ranges, "tidal_heating")
    if not th_rows:
        raise SystemExit(f"{a.body} has no bulk.tidal_heating row to refresh")
    m = re.search(r"e_rms ([\d.]+), k₂/Q ~?([\d.]+)", lines[th_rows[0]])
    if not m:
        raise SystemExit("cannot read e_rms / k₂/Q from the tidal_heating value string")
    e, k2q = float(m.group(1)), float(m.group(2))
    if "radius_km" not in moon or "parent" not in moon:
        raise SystemExit(f"the satellites row for {a.body} carries no radius_km/parent")
    r_km = moon["radius_km"]
    a_km = moon.get("design_a_km", moon.get("a_km"))
    mp_kg, mp_line = parent_mass_kg(lines, moon["parent"])

    power, flux, n = th.tidal_power(k2q, mp_kg, r_km * 1e3, a_km * 1e3, e)
    ratio = power / th.IO_POWER_W
    today = date.today().isoformat()
    stamp = (f"refreshed {today} from the tidal_heating recipe @{sha()} at R {r_km:.0f} km "
             f"(a {a_km:,.0f} km · e_rms {e} · k₂/Q {k2q} · M_p {mp_kg / M_EARTH_KG:.0f} M⊕)")
    stamp_ko = (f"{today} tidal_heating 레시피 @{sha()}에서 갱신, R {r_km:.0f} km "
                f"(a {a_km:,.0f} km · e_rms {e} · k₂/Q {k2q} · M_p {mp_kg / M_EARTH_KG:.0f} M⊕)")
    partition = (f"stale {today}: this figure was partitioned from the 900 km flux, before the 2026-08-21 resize to "
                 f"{r_km:.0f} km; no recipe partitions the heat, so no value is computed here")
    partition_ko = (f"stale {today}: 이 값은 900 km 플럭스를 분배해 얻은 것으로, 2026-08-21 {r_km:.0f} km "
                    f"리사이즈 이전이다. 열을 분배하는 레시피가 없으므로 여기서 값을 새로 내지 않는다")
    figure = (f"stale {today}: reference_radius_km is still 900 km, which the body_figure decision owns; "
              f"the satellites table has carried {r_km:.0f} km since 2026-08-21")
    figure_ko = (f"stale {today}: reference_radius_km이 아직 900 km이고 이 값은 body_figure 결정 소유다. "
                 f"satellites 표는 2026-08-21부터 {r_km:.0f} km를 싣고 있다")
    rests = (f"stale {today}: this value rests on the 360 K plains, which were partitioned from the 900 km flux "
             f"before the 2026-08-21 resize to {r_km:.0f} km; the plains have no recipe, so nothing is recomputed here")
    rests_ko = (f"stale {today}: 이 값은 360 K 평원에 기대고 있고, 그 평원은 2026-08-21 {r_km:.0f} km 리사이즈 이전의 "
                f"900 km 플럭스를 분배해 얻은 것이다. 평원에는 레시피가 없으므로 여기서 다시 계산하지 않는다")
    stale_reason = {"geopotential_j2": (figure, figure_ko),
                    "surface_temperature": (partition, partition_ko),
                    "albedo": (rests, rests_ko)}

    new = list(lines)
    for i in th_rows:
        value = f"~{ratio:.0f}× Io (simulated e_rms {e}, k₂/Q ~{k2q})"
        new[i] = append_note(set_value_ko(set_value(new[i], value), f"~{ratio:.0f}× Io (시뮬 e_rms {e}, k₂/Q≈{k2q})"),
                             f"{stamp}; was: {old_value(lines[i])}",
                             f"{stamp_ko}; 구값: {old_value(lines[i])}")
    for i in field_lines(lines, ranges, "tidal_surface_flux"):
        new[i] = append_note(set_value_ko(set_value(new[i], f"~{flux:,.0f} W/m²"), f"~{flux:,.0f} W/m²"),
                             f"{stamp}; was: {old_value(lines[i])} — the partition text in that value is stale too",
                             f"{stamp_ko}; 구값: {old_value(lines[i])} — 그 값에 붙어 있던 분배 서술도 stale")
    for i in field_lines(lines, ranges, "internal_heat"):
        new[i] = append_note(set_value(new[i], f"tidal (see bulk.tidal_heating row, ~{ratio:.0f}× Io)"),
                             f"{stamp} — echo of the owning row; was: {old_value(lines[i])}",
                             f"{stamp_ko} — 소유 행의 에코; 구값: {old_value(lines[i])}")
    for name in STALE:
        for i in field_lines(lines, ranges, name):
            new[i] = append_note(new[i], *stale_reason[name])

    # ── report ────────────────────────────────────────────────────────────────────────
    print(f"# board {path}  ·  body {a.body}  ·  {'APPLY' if a.apply else 'dry run'}")
    print(f"# inputs: R {r_km:.0f} km · a {a_km:,.0f} km (satellites row, line {mrow + 1}) · "
          f"e_rms {e} · k₂/Q {k2q} (tidal_heating value, line {th_rows[0] + 1}) · "
          f"M_p {mp_kg / M_EARTH_KG:.0f} M⊕ (line {mp_line})")
    print(f"# recipe: Ė {power:.4e} W · F {flux:,.1f} W/m² · {ratio:.2f}× Io (Io = {th.IO_POWER_W:.0e} W) · "
          f"n {n:.4e} rad/s · regime \"{th.outcome_regime(flux)}\"")
    diff = "".join(difflib.unified_diff(lines, new, fromfile=str(path), tofile=f"{path} (refreshed)", n=1))
    print(diff or "# no change")
    print("# not touched — 900-km-era text this tool does not own (report only):")
    for s, e_ in ranges:
        for i in range(s, e_):
            if any(re.search(p, lines[i]) for p in WATCH) and new[i] == lines[i]:
                print(f"#   {i + 1}: {lines[i].strip()[:150]}")
    if a.apply:
        path.write_text("".join(new), encoding="utf-8")
        print("# applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
