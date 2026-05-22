#!/usr/bin/env python3
# Firefly cfg eval grader — mechanical schema checks
import json
import re
import sys
from pathlib import Path

ITERATION = Path(__file__).parent

def grade_cfg(cfg_text: str, expected_name: str) -> list[dict]:
    results = []
    def add(test_id, text, passed, evidence=""):
        results.append({"id": test_id, "text": text, "passed": passed, "evidence": evidence})

    add("atmofx_body", "Contains ATMOFX_BODY node",
        "ATMOFX_BODY" in cfg_text,
        "found" if "ATMOFX_BODY" in cfg_text else "missing")

    name_match = re.search(rf"name\s*=\s*{re.escape(expected_name)}\b", cfg_text)
    add("name_match", f"name = {expected_name}",
        bool(name_match),
        name_match.group(0) if name_match else "no match")

    add("config_version_5", "config_version = 5",
        re.search(r"config_version\s*=\s*5\b", cfg_text) is not None,
        "v5" if "config_version = 5" in cfg_text or "config_version=5" in cfg_text else "")

    required_colors = ["glow", "glow_hot", "trail_primary", "trail_secondary",
                       "trail_tertiary", "trail_streak", "wrap_layer", "wrap_streak", "shockwave"]
    missing = [c for c in required_colors if not re.search(rf"\b{c}\s*=", cfg_text)]
    add("all_9_colors", "All 9 Color keys present",
        len(missing) == 0,
        "all present" if not missing else f"missing: {missing}")

    color_keys_pat = r"(glow|glow_hot|trail_primary|trail_secondary|trail_tertiary|trail_streak|wrap_layer|wrap_streak|shockwave)"
    color_lines = re.findall(rf"^\s*{color_keys_pat}\s*=\s*(.+?)$",
                              cfg_text, re.MULTILINE)
    bad = []
    for key, val in color_lines:
        tokens = val.strip().split()
        # Strip trailing comment if present
        if "//" in tokens:
            tokens = tokens[:tokens.index("//")]
        if len(tokens) != 4:
            bad.append(f"{key}={val!r} ({len(tokens)} tokens)")
            continue
        try:
            r, g, b, i = map(float, tokens)
        except ValueError:
            bad.append(f"{key}={val!r} (parse fail)")
    add("color_format_valid", "Every color is 4 space-separated floats",
        len(bad) == 0,
        "all valid" if not bad else f"bad: {bad[:2]}")

    trail_primary = re.search(r"trail_primary\s*=\s*(\d+)\s+(\d+)\s+(\d+)", cfg_text)
    if trail_primary:
        r, g, b = map(int, trail_primary.groups())
        add("trail_warm", "trail_primary R > B (warm tone)",
            r > b, f"R={r} B={b}")
    else:
        add("trail_warm", "trail_primary R > B (warm tone)", False, "trail_primary not parseable")

    shockwave = re.search(r"shockwave\s*=\s*(\d+)\s+(\d+)\s+(\d+)", cfg_text)
    if shockwave:
        r, g, b = map(int, shockwave.groups())
        add("shockwave_cool", "shockwave B > R (cool blue-violet)",
            b > r, f"R={r} B={b}")
    else:
        add("shockwave_cool", "shockwave B > R (cool blue-violet)", False, "shockwave not parseable")

    sm = re.search(r"strength_multiplier\s*=\s*([\d.]+)", cfg_text)
    if sm:
        v = float(sm.group(1))
        add("strength_earth_like", "strength_multiplier in [0.8, 1.2]",
            0.8 <= v <= 1.2, f"={v}")
    else:
        add("strength_earth_like", "strength_multiplier in [0.8, 1.2]", False, "not found")

    add("no_f_suffix", "No '1.0f'-style float literals",
        re.search(r"=\s*[\d.]+f\b", cfg_text) is None,
        "clean" if re.search(r"=\s*[\d.]+f\b", cfg_text) is None else "found f-suffix")

    # commas inside color values
    has_color_commas = any("," in val for _, val in color_lines)
    add("no_commas", "No commas in color values",
        not has_color_commas, "clean" if not has_color_commas else "found")

    add("name_no_special", "Body name has no spaces/dashes/special chars",
        re.search(rf"name\s*=\s*[A-Za-z0-9]+\b", cfg_text) is not None,
        "ok" if re.search(rf"name\s*=\s*[A-Za-z0-9]+\b", cfg_text) else "fail")

    return results

def grade_decision(decision_text: str) -> list[dict]:
    results = []
    def add(test_id, text, passed, evidence=""):
        results.append({"id": test_id, "text": text, "passed": passed, "evidence": evidence})

    lower = decision_text.lower()
    add("decision_correctly_airless", "Mentions airless / no atmosphere",
        "airless" in lower or "no atmosphere" in lower,
        "found 'airless'" if "airless" in lower else "found 'no atmosphere'" if "no atmosphere" in lower else "missing")

    add("decision_cites_phase3", "Cites Phase 3 / Ducrot / Greene / Ih",
        any(x in lower for x in ["phase 3", "ducrot", "greene", "atmosphere_present"]),
        "found citation" if any(x in lower for x in ["phase 3", "ducrot", "greene", "atmosphere_present"]) else "no")

    return results

def grade_run(run_dir: Path, expected_name: str, expected_decision: str):
    cfg_files = list(run_dir.glob("outputs/*.cfg"))
    decision_files = list(run_dir.glob("outputs/_decision.md"))

    grading = {"run_id": run_dir.parent.name + "-" + run_dir.name, "results": []}

    if expected_decision == "skip_airless":
        # accept either decision or cfg
        if decision_files:
            grading["results"].append({"id": "decision_or_cfg",
                "text": "Either _decision.md or .cfg present", "passed": True,
                "evidence": "_decision.md present"})
            grading["results"].extend(grade_decision(decision_files[0].read_text()))
        elif cfg_files:
            grading["results"].append({"id": "decision_or_cfg",
                "text": "Either _decision.md or .cfg present", "passed": True,
                "evidence": ".cfg present (thin-atmo route)"})
            grading["results"].extend(grade_cfg(cfg_files[0].read_text(), expected_name))
        else:
            grading["results"].append({"id": "decision_or_cfg",
                "text": "Either _decision.md or .cfg present", "passed": False,
                "evidence": "neither found"})
    else:
        if not cfg_files:
            grading["results"].append({"id": "file_exists",
                "text": f"Output {expected_name}.cfg exists", "passed": False,
                "evidence": "no cfg file"})
            return grading
        grading["results"].append({"id": "file_exists",
            "text": f"Output {expected_name}.cfg exists", "passed": True,
            "evidence": cfg_files[0].name})
        grading["results"].extend(grade_cfg(cfg_files[0].read_text(), expected_name))

    return grading

cases = [
    ("eval-trappist-1-e", "Trappist1e", "emit_cfg"),
    ("eval-trappist-1-b", "Trappist1b", "skip_airless"),
    ("eval-proxima-cen-b", "ProximaCenB", "emit_cfg"),
]

for eval_dir, expected_name, expected_decision in cases:
    for condition in ["with_skill", "without_skill"]:
        run_dir = ITERATION / eval_dir / condition
        if not run_dir.exists(): continue
        grading = grade_run(run_dir, expected_name, expected_decision)
        out = run_dir / "grading.json"
        out.write_text(json.dumps(grading, indent=2))
        passed = sum(1 for r in grading["results"] if r["passed"])
        total = len(grading["results"])
        print(f"{eval_dir}/{condition}: {passed}/{total}")
