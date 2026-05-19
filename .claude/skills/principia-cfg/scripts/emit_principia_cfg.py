#!/usr/bin/env python3
# db/systems/*.json 을 읽어 Principia용 GravityModel·InitialState cfg 를 생성하는 스크립트
"""Emit Principia cfg patches for NearStars (Sol real scale MVP).

Reads every db/systems/*.json, validates the Principia-specific fields, and
writes a single combined GravityModel patch + InitialState patch under
`dist/Principia/`.

See `.claude/skills/principia-cfg/SKILL.md` for scope and decisions.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SOLAR_SYSTEM_EPOCH_JD = 2433282.5  # Sol real scale, B1950-Jan-01

REPO_ROOT = Path(__file__).resolve().parents[4]
DB_SYSTEMS_DIR = REPO_ROOT / "db" / "systems"
DIST_DIR = REPO_ROOT / "dist" / "NearStars-Configs" / "Patches" / "Principia"
OUT_GRAVITY = DIST_DIR / "Real_NearStars-GravityModel.cfg"
OUT_INITIAL = DIST_DIR / "Real_NearStars-InitialState.cfg"

GRAVITY_HEADER = "@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem]"
INITIAL_HEADER = "@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]"


@dataclass(frozen=True)
class BodyEntry:
    body_name: str
    source_system: str
    gm_km3_s2: float
    x_km: float
    y_km: float
    z_km: float
    vx_km_s: float
    vy_km_s: float
    vz_km_s: float


def normalize_body_name(raw: str) -> str:
    parts: list[str] = []
    for word in raw.split():
        token = re.sub(r"[^A-Za-z0-9]", "", word)
        if not token:
            continue
        if any(c.isupper() for c in token):
            parts.append(token)
        else:
            parts.append(token[0].upper() + token[1:])
    return "".join(parts)


def fmt_value(value: float) -> str:
    return f"{value:+.15e}"


def is_finite_number(value) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


class EmitError(RuntimeError):
    """Raised when something is structurally wrong before validation begins."""


def load_systems(only: list[str] | None) -> list[tuple[Path, dict]]:
    if not DB_SYSTEMS_DIR.is_dir():
        raise EmitError(f"DB systems dir not found: {DB_SYSTEMS_DIR}")
    files = sorted(DB_SYSTEMS_DIR.glob("*.json"))
    if only:
        wanted = set(only)
        files = [p for p in files if p.stem in wanted]
        missing = wanted - {p.stem for p in files}
        if missing:
            raise EmitError(f"--system: no DB file for {sorted(missing)}")
    out = []
    for p in files:
        with p.open(encoding="utf-8") as fh:
            out.append((p, json.load(fh)))
    return out


def validate_system(path: Path, data: dict, errors: list[str], warnings: list[str]) -> None:
    """Append validation problems (per-star) to `errors` / `warnings`. Never raises."""
    meta = data.get("meta") or {}
    ss_epoch = meta.get("solar_system_epoch_jd")
    if ss_epoch != SOLAR_SYSTEM_EPOCH_JD:
        errors.append(
            f"{path.name}: meta.solar_system_epoch_jd = {ss_epoch!r}, expected {SOLAR_SYSTEM_EPOCH_JD}"
        )

    stars = data.get("stars") or []
    if not stars:
        errors.append(f"{path.name}: 'stars' is empty or missing")

    for star in stars:
        name = star.get("name") or "<unnamed>"
        derived = star.get("derived") or {}
        principia = star.get("principia") or {}
        if derived.get("epoch_jd") != SOLAR_SYSTEM_EPOCH_JD:
            errors.append(
                f"{path.name} / {name}: derived.epoch_jd = {derived.get('epoch_jd')!r}, expected {SOLAR_SYSTEM_EPOCH_JD}"
            )
        for field in ("icrs_x_km", "icrs_y_km", "icrs_z_km",
                      "icrs_vx_km_s", "icrs_vy_km_s", "icrs_vz_km_s"):
            v = derived.get(field)
            if not is_finite_number(v):
                errors.append(
                    f"{path.name} / {name}: derived.{field} is not a finite number ({v!r})"
                )
        gm = principia.get("gravitational_parameter_km3_s2")
        if not is_finite_number(gm):
            errors.append(
                f"{path.name} / {name}: principia.gravitational_parameter_km3_s2 is not finite ({gm!r})"
            )

    planets = data.get("planets") or []
    if planets:
        warnings.append(
            f"{path.name}: has {len(planets)} planet(s) — skipped in MVP "
            f"(see references/planet-contract.md)"
        )


def collect_bodies(systems: Iterable[tuple[Path, dict]]) -> list[BodyEntry]:
    bodies: list[BodyEntry] = []
    seen_names: dict[str, str] = {}
    for path, data in systems:
        for star in data.get("stars") or []:
            override = star.get("kopernicus_body_name")
            body_name = override if override else normalize_body_name(star["name"])
            if not body_name:
                raise EmitError(f"{path.name}: star '{star.get('name')}' resolved to empty body name")
            if body_name in seen_names:
                raise EmitError(
                    f"body name collision: '{body_name}' from both {seen_names[body_name]} and {path.name}"
                )
            seen_names[body_name] = path.name
            d = star["derived"]
            p = star["principia"]
            bodies.append(BodyEntry(
                body_name=body_name,
                source_system=path.stem,
                gm_km3_s2=float(p["gravitational_parameter_km3_s2"]),
                x_km=float(d["icrs_x_km"]),
                y_km=float(d["icrs_y_km"]),
                z_km=float(d["icrs_z_km"]),
                vx_km_s=float(d["icrs_vx_km_s"]),
                vy_km_s=float(d["icrs_vy_km_s"]),
                vz_km_s=float(d["icrs_vz_km_s"]),
            ))
    bodies.sort(key=lambda b: b.body_name)
    return bodies


def render_gravity_model(bodies: list[BodyEntry]) -> str:
    lines = [
        "// NearStars — Principia gravity model patch (Sol real scale)",
        "// Generated by .claude/skills/principia-cfg/scripts/emit_principia_cfg.py",
        "// Do not hand-edit; regenerate from db/systems/*.json.",
        "",
        GRAVITY_HEADER,
        "{",
    ]
    for b in bodies:
        lines += [
            "    body",
            "    {",
            f"        name                    = {b.body_name}",
            f"        gravitational_parameter = {fmt_value(b.gm_km3_s2)} km^3/s^2",
            "    }",
        ]
    lines += ["}", ""]
    return "\n".join(lines)


def render_initial_state(bodies: list[BodyEntry]) -> str:
    lines = [
        "// NearStars — Principia initial state patch (Sol real scale, JD 2433282.5)",
        "// Generated by .claude/skills/principia-cfg/scripts/emit_principia_cfg.py",
        "// Do not hand-edit; regenerate from db/systems/*.json.",
        "",
        INITIAL_HEADER,
        "{",
    ]
    for b in bodies:
        lines += [
            "    body",
            "    {",
            f"        name = {b.body_name}",
            f"        x    = {fmt_value(b.x_km)} km",
            f"        y    = {fmt_value(b.y_km)} km",
            f"        z    = {fmt_value(b.z_km)} km",
            f"        vx   = {fmt_value(b.vx_km_s)} km/s",
            f"        vy   = {fmt_value(b.vy_km_s)} km/s",
            f"        vz   = {fmt_value(b.vz_km_s)} km/s",
            "    }",
        ]
    lines += ["}", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit Principia cfg patches for NearStars.")
    ap.add_argument("--dry-run", action="store_true", help="Print to stdout, do not write files.")
    ap.add_argument("--system", action="append", default=[],
                    help="Only emit this system file stem. Repeatable, e.g. "
                         "--system alpha_centauri_a --system alpha_centauri_b. "
                         "If unset, all db/systems/*.json are emitted.")
    args = ap.parse_args()

    try:
        systems = load_systems(args.system or None)
    except EmitError as e:
        print(f"ABORT: {e}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []
    for path, data in systems:
        validate_system(path, data, errors, warnings)

    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)

    if errors:
        print(f"ABORT: {len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 2

    try:
        bodies = collect_bodies(systems)
    except EmitError as e:
        print(f"ABORT: {e}", file=sys.stderr)
        return 2

    if not bodies:
        print("ABORT: no bodies collected — nothing to emit.", file=sys.stderr)
        return 2

    gravity_text = render_gravity_model(bodies)
    initial_text = render_initial_state(bodies)

    if args.dry_run:
        sys.stdout.write("===== " + str(OUT_GRAVITY.relative_to(REPO_ROOT)) + " =====\n")
        sys.stdout.write(gravity_text)
        sys.stdout.write("\n===== " + str(OUT_INITIAL.relative_to(REPO_ROOT)) + " =====\n")
        sys.stdout.write(initial_text)
    else:
        DIST_DIR.mkdir(parents=True, exist_ok=True)
        OUT_GRAVITY.write_text(gravity_text, encoding="utf-8")
        OUT_INITIAL.write_text(initial_text, encoding="utf-8")
        print(f"wrote {OUT_GRAVITY.relative_to(REPO_ROOT)} ({len(bodies)} bodies)")
        print(f"wrote {OUT_INITIAL.relative_to(REPO_ROOT)} ({len(bodies)} bodies)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
