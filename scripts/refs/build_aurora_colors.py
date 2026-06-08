# 오로라 색을 밀도(고도)·조성의 함수로 산출해 db/refs/aurora_colors.yaml 로 생성 (비-LTE 금지선 + quenching)
"""Build a density(altitude)-resolved aurora color table per atmosphere.

Aurora is NON-LTE: no gas temperature sets the populations. The color is set by
which emission lines SURVIVE collisional quenching at a given density — that is
what makes auroral color altitude-stratified (red high → green mid → N2 pink
low on Earth). So the axis is DENSITY (≈ altitude), not temperature.

Model (per emitter line):
    intensity = x_source · n · yield · φ
    φ_forbidden = A_line / (A_total + Σ_q k_q · x_q · n)   (metastable quenching)
    φ_allowed   = A_line                                   (fast, excitation-limited)
The ·n factor = collisional excitation grows with density, so allowed N2 bands
dominate the dense low-altitude border while quenched forbidden O lines plateau
and fade *relatively* → the stratification emerges. Mixed → CIE 1931 → color.

Earth uses a density-dependent composition profile (atomic-O-rich thermosphere
top → N2/O2 air at the bottom) so the full red→green→pink layering appears.

MODELING CHOICES (documented): relative yields (calibrated), fixed quenching
coefficients, electron-impact excitation ∝ density, representative composition
profiles. First-principles: the quenching branching φ(n) with measured A + k.

Usage:
    python3 scripts/refs/build_aurora_colors.py
    python3 scripts/refs/build_aurora_colors.py --sanity
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cie_color  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AURORA_DB = ROOT / "db" / "refs" / "aurora_lines.yaml"
OUT = ROOT / "db" / "refs" / "aurora_colors.yaml"

# density grid [cm^-3], high altitude (low n) → low altitude (high n)
LOG_N = [7, 8, 9, 10, 11, 12, 13, 14]
ALT_HINT = {7: "~350km", 8: "~300km", 9: "~250km", 10: "~180km",
            11: "~140km", 12: "~115km", 13: "~100km", 14: "~90km"}
WIDTH_NM = 2.5

# Per-atmosphere composition. Earth: density-dependent anchors (log10 n, comp),
# interpolated. Others: single fixed comp (one anchor).
ATMOSPHERES = {
    # Earth: high alt O-rich thermosphere → low alt N2-rich; the densest rows reach
    # the ~80-105 km airglow / meteoric-metal layer (Na yellow + OH red + metals).
    "earth": {"label": "Earth (N2/O2)", "anchors": [
        (7,  {"O": 0.92, "N2": 0.07, "O2": 0.01}),
        (10, {"O": 0.55, "N2": 0.36, "O2": 0.09}),
        (13, {"O": 0.05, "N2": 0.76, "O2": 0.18, "Na": 0.006}),
        (14, {"O": 0.02, "N2": 0.66, "O2": 0.28, "Na": 0.02,
              "Li": 0.003, "K": 0.008, "Ca": 0.004})]},
    "venus_mars": {"label": "Venus/Mars (CO2)", "anchors": [
        (7, {"O": 0.5, "CO2": 0.45, "N2": 0.05}),
        (13, {"O": 0.05, "CO2": 0.92, "N2": 0.03})]},
    # (Mars hosts a meteoric metal layer too — MAVEN — but its visible emission is
    #  faint/UV-dominant, so the metal airglow is modeled only for Earth below.)
    "gas_giant": {"label": "Gas giant (H2/He)", "anchors": [
        (7, {"H": 0.9, "He": 0.1})]},
}


def comp_at(anchors, ln):
    """Interpolate composition at log10(n) between anchors."""
    if len(anchors) == 1 or ln <= anchors[0][0]:
        return anchors[0][1]
    if ln >= anchors[-1][0]:
        return anchors[-1][1]
    for (l0, c0), (l1, c1) in zip(anchors, anchors[1:]):
        if l0 <= ln <= l1:
            f = (ln - l0) / (l1 - l0)
            keys = set(c0) | set(c1)
            return {k: c0.get(k, 0) * (1 - f) + c1.get(k, 0) * f for k in keys}
    return anchors[-1][1]


def aurora_spectrum(emitters, comp, n):
    contribs = []                       # (nm, strength)
    diag = {}                           # per-emitter production (for the dominant label)
    for name, e in emitters.items():
        x = comp.get(e["source"], 0.0)
        if x <= 0:
            continue
        base = x * n * e["yield"]
        if e.get("forbidden"):
            Q = sum(k * comp.get(q, 0.0) * n for q, k in e["quench"].items())
            denom = e["A_total"] + Q
            for ln in e["lines"]:
                s = base * ln["A"] / denom          # production·branching·survival
                if s > 0:
                    contribs.append((ln["nm"], s))
            diag[name] = base * e["A_total"] / denom
        else:
            for ln in e["lines"]:
                contribs.append((ln["nm"], base * ln["A"]))
            diag[name] = base
    if not contribs:
        return None, {}
    mx = max(s for _, s in contribs)
    inten = []
    for lam in cie_color.LAMBDAS:
        j = 0.0
        for lam0, s in contribs:
            d = (lam - lam0) / WIDTH_NM
            if -6 < d < 6:
                j += s * 2.718 ** (-0.5 * d * d)
        inten.append(j)
    dom = max(diag, key=diag.get)
    return cie_color.spectrum_to_hex(inten), {"dominant": dom}


def build():
    emitters = yaml.safe_load(AURORA_DB.read_text(encoding="utf-8"))["emitters"]
    out = {}
    for key, atm in ATMOSPHERES.items():
        rows = {}
        for ln in LOG_N:
            comp = comp_at(atm["anchors"], ln)
            n = 10.0 ** ln
            hexv, d = aurora_spectrum(emitters, comp, n)
            if hexv is None:
                continue
            rgb = cie_color.hex_to_rgb(hexv)
            rows[ln] = {"log_n": ln, "altitude_hint": ALT_HINT[ln], "hex": hexv,
                        "rgb": [round(c * 255) for c in rgb], "dominant": d["dominant"]}
        out[key] = {"label": atm["label"], "colors": rows}
    return out


HEADER = """\
# Aurora color vs density (altitude proxy), per atmosphere — NON-LTE.
# Built by scripts/refs/build_aurora_colors.py from aurora_lines.yaml.
# Color is set by quenching of metastable forbidden lines (O 1D red, 1S green)
# + N2 bands, NOT by temperature. Axis = number density [cm^-3] (high altitude =
# low n → low altitude = high n). Earth shows the red(high)→green(mid)→pink(low)
# stratification. See plasma-color-methodology-review.md for the (separate) LTE
# reentry engine; aurora is the non-LTE counterpart and feeds aurora/EVE, not Firefly.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sanity", action="store_true")
    args = ap.parse_args()
    data = build()
    if args.sanity:
        for key, blk in data.items():
            print(f"\n{blk['label']} (high alt → low alt):")
            for ln, c in blk["colors"].items():
                print(f"  n=1e{ln} {c['altitude_hint']:>7}  {c['hex']}  ({c['dominant']})")
        return 0
    OUT.write_text(HEADER + yaml.dump(data, sort_keys=False, allow_unicode=True,
                                      default_flow_style=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(data)} atmospheres x {len(LOG_N)} densities)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
