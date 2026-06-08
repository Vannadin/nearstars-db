# 전 원소의 LTE 원자 발광색을 NIST 라인에서 계산해 db/refs/lte_plasma_colors.yaml 생성 (주기율표 계산 regime)
"""Compute a per-element atomic plasma-emission color from NIST ASD neutral
lines, and write db/refs/lte_plasma_colors.yaml — the periodic table's computed
`lte_plasma` regime, distinct from the curated flame/reentry/aurora regimes.

Per element, two methods (see emission_color):
  PRIMARY — LTE Boltzmann at T_REF: optically-thin emission
    j(λ) = Σ n_upper·A_ki·hν·φ(λ),  n_upper ∝ g_u·exp(-E_u/kT)/U(T),
  using NIST A-values + level populations → CIE 1931. Gives the familiar
  characteristic colors (Na yellow, Cu green, Li red) for the ~73 elements with
  measured A-values.
  FALLBACK — top-N NIST observed intensities, for complex spectra (Zr, Nb,
  lanthanides, actinides) that NIST lists without A-values. Flagged confidence=low.

HONEST CAVEATS (per element, flagged):
  - `confidence: low` for the intensity fallback, OR when the strongest line sits
    at the visibility edge (total CMF < CMF_MIN) so the perceived color is set by
    trace lines (alkali IR resonance K/Rb/Cs; deep-violet-dominant Fe/Sc).
  - This is the ATOMIC color. Where a classic flame color is MOLECULAR (CaOH
    brick-red, SrOH crimson) the atomic fingerprint differs (Ca→violet 422,
    Sr→blue 461) — same LTE-vs-observed split as air's non-LTE reentry blue.
    The curated flame regime keeps the familiar color; this is the physics layer.
  - `no_measured_spectra`: NIST has no usable visible lines for the neutral
    (At + the superheavies) — left null, not fabricated.

Fetch is via curl (cache-first under --cache-dir; the cache IS NIST data). The
bulk fetch must avoid high concurrency — NIST truncates responses under load.

Usage:
    python3 scripts/refs/build_lte_plasma_colors.py
    python3 scripts/refs/build_lte_plasma_colors.py --sanity
"""
from __future__ import annotations

import argparse
import math
import subprocess
import sys
import urllib.parse
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cie_color                       # noqa: E402
import build_atomic_lines as BA        # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ELEMENT_DB = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
OUT = ROOT / "db" / "refs" / "lte_plasma_colors.yaml"

K_CM = 0.6950348
T_REF = 3500.0           # reference plasma temperature [K] for the Boltzmann path
WIDTH_NM = 1.5           # line display half-width
INTENS_TOPN = 8          # fallback: mix this many strongest lines by NIST intensity
CMF_MIN = 0.05           # dominant line's total CMF response (x̄+ȳ+z̄); below = edge
                         # of vision (e.g. alkali IR resonance 766+ nm) → low confidence

LINES_URL = ("https://physics.nist.gov/cgi-bin/ASD/lines1.pl?spectra={spec}"
             "&limits_type=0&low_w=360&upp_w=830&unit=1&submit=Retrieve+Data"
             "&de=0&format=3&line_out=0&en_unit=0&output=0&bibrefs=1&page_size=15"
             "&show_obs_wl=1&show_calc_wl=1&unc_out=1&order_out=0&max_low_enrg="
             "&show_av=2&max_upp_enrg=&tsb_value=0&min_str=&A_out=0&intens_out=on"
             "&max_str=&allowed_out=1&forbid_out=1&min_accur=&min_intens="
             "&conf_out=on&term_out=on&enrg_out=on&J_out=on&g_out=on")
LEVELS_URL = ("https://physics.nist.gov/cgi-bin/ASD/energy1.pl?spectrum={spec}"
              "&units=0&format=3&output=0&page_size=15&multiplet_ordered=0"
              "&conf_out=on&term_out=on&level_out=on&j_out=on&g_out=on"
              "&temp=&submit=Retrieve+Data")


def fetch(url: str, cache_path: Path, refresh: bool) -> str:
    if cache_path.exists() and not refresh:
        return cache_path.read_text(encoding="utf-8")
    try:
        out = subprocess.run(["curl", "-s", "-m", "30", url],
                             capture_output=True, text=True, timeout=40).stdout
        if out and "Invalid" not in out and "Input Error" not in out:
            cache_path.write_text(out, encoding="utf-8")
            return out
    except Exception:
        pass
    return cache_path.read_text(encoding="utf-8") if cache_path.exists() else ""


def _partition(levels: list[dict], T: float) -> float:
    kt = K_CM * T
    return sum(l["g"] * math.exp(-l["E_cm"] / kt) for l in levels) or 1.0


def _intensity_lines(lines_text: str) -> list[tuple]:
    """Visible (nm, NIST observed intensity) — fallback for spectra without A."""
    rows = []
    for r in BA._rows(lines_text, "obs_wl_air"):
        wl = BA._num(r.get("obs_wl_air(nm)", "")) or BA._num(r.get("ritz_wl_air(nm)", ""))
        if wl is None or not (360.0 <= wl <= 830.0):
            continue
        w = BA._num(r.get("intens", ""))
        if w and w > 0:
            rows.append((wl, w))
    return rows


def _mix(contribs: list[tuple]):
    if not contribs:
        return None, None
    dom = max(contribs, key=lambda c: c[1])[0]
    inten = []
    for lam in cie_color.LAMBDAS:
        j = 0.0
        for lam0, w in contribs:
            d = (lam - lam0) / WIDTH_NM
            if -6 < d < 6:
                j += w * math.exp(-0.5 * d * d)
        inten.append(j)
    if max(inten) <= 0:
        return None, None
    return cie_color.spectrum_to_hex(inten), dom


def emission_color(lines_text: str, levels_text: str):
    """Return (hex, dominant_nm, method, n_lines).

    PRIMARY: LTE Boltzmann at T_REF using NIST A-values + level populations
    (rigorous; gives familiar colors — Na yellow, Cu green, Li red). FALLBACK
    for complex spectra without A-values (Zr, Nb, lanthanides, actinides): mix
    the top-INTENS_TOPN visible lines by NIST observed intensity (less rigorous,
    flagged). Bare summing of all NIST intensities washes out the hue, hence
    top-N only."""
    a_lines = BA.parse_lines(lines_text) if lines_text else []
    if a_lines:
        U = _partition(BA.parse_levels(levels_text) if levels_text else [], T_REF)
        kt = K_CM * T_REF
        contribs = []
        for ln in a_lines:
            s = (ln["g_upper"] * math.exp(-ln["E_upper_cm"] / kt) / U
                 * ln["A_ki"] * (1e7 / ln["nm"]))
            if s > 0:
                contribs.append((ln["nm"], s))
        hexv, dom = _mix(contribs)
        return hexv, dom, "boltzmann", len(contribs)
    rows = sorted(_intensity_lines(lines_text), key=lambda r: r[1], reverse=True)[:INTENS_TOPN]
    hexv, dom = _mix(rows)
    return hexv, dom, "intensity", len(rows)


def build(cache_dir: Path, refresh: bool, sanity: bool) -> dict:
    cache_dir.mkdir(parents=True, exist_ok=True)
    edb = yaml.safe_load(ELEMENT_DB.read_text(encoding="utf-8"))
    # YAML parses the symbol "No" (Nobelium) as the boolean False — coerce back.
    bool_sym = {False: "No", True: "Yes"}
    elements = sorted(((v["atomic_number"], bool_sym.get(sym, sym), v["name"])
                       for sym, v in edb.items() if isinstance(v, dict)),
                      key=lambda t: t[0])
    out: dict = {}
    for z, sym, name in elements:
        spec = urllib.parse.quote_plus(f"{sym} I")
        key = sym.lower()
        lt = fetch(LINES_URL.format(spec=spec), cache_dir / f"lines_{key}.txt", refresh)
        vt = fetch(LEVELS_URL.format(spec=spec), cache_dir / f"levels_{key}.txt", refresh)
        hexv, dom, method, nlines = emission_color(lt, vt) if lt else (None, None, None, 0)
        if hexv is None:
            out[sym] = {"z": z, "status": "no_measured_spectra", "hex": None,
                        "basis": "no NIST neutral visible lines with A-values or intensity"}
        else:
            cmf = cie_color._xbar(dom) + cie_color._ybar(dom) + cie_color._zbar(dom)
            edge = cmf < CMF_MIN
            low = edge or method == "intensity"
            if method == "boltzmann":
                note = f"LTE Boltzmann from {nlines} NIST lines (A-values) at {int(T_REF)}K"
            else:
                note = f"top-{nlines} NIST observed intensities (no A-values for this spectrum)"
            note += f"; dominant {dom:.1f}nm"
            if edge:
                note += " (dominant line near the visibility edge)"
            out[sym] = {"z": z, "status": "visible", "hex": hexv, "method": method,
                        "confidence": "low" if low else "high",
                        "dominant_nm": round(dom, 1), "n_lines": nlines,
                        "basis": note}
        if sanity:
            print(f"  {sym:3} Z={z:3} {out[sym]['status']:18} {out[sym].get('hex') or '-':8} "
                  f"{out[sym].get('confidence','')}")
    return out


HEADER = f"""\
# Computed atomic plasma-emission color per element — the periodic table's
# `lte_plasma` regime. Built by scripts/refs/build_lte_plasma_colors.py from NIST
# ASD neutral lines via the cie_color machinery.
#   method=boltzmann: LTE optically-thin emission at {int(T_REF)}K from A-values
#     + level populations (the spectral fingerprint; ~73 elements).
#   method=intensity: top-N NIST observed intensities for spectra without
#     A-values (Zr, Nb, lanthanides, actinides) — flagged confidence=low.
#
# status: visible (hex + method + confidence + dominant_nm) | no_measured_spectra.
# confidence=low: intensity method, OR the dominant line is at the visibility
#   edge (alkali IR resonance; deep-violet-dominant Fe/Sc) so it is edge-sensitive.
# This is the ATOMIC color; where the classic flame color is molecular (CaOH,
# SrOH) it differs from the curated flame regime — that is expected.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", default="/tmp/nist_clean")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--sanity", action="store_true")
    args = ap.parse_args()

    data = build(Path(args.cache_dir), args.refresh, args.sanity)
    visible = sum(1 for v in data.values() if v["status"] == "visible")
    low = sum(1 for v in data.values() if v.get("confidence") == "low")
    if args.sanity:
        print(f"\nvisible={visible}  low_confidence={low}  "
              f"no_data={len(data) - visible}  total={len(data)}")
        return 0
    OUT.write_text(HEADER + yaml.dump(data, sort_keys=False, allow_unicode=True,
                                      default_flow_style=False), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  (visible={visible}, low_conf={low}, "
          f"no_data={len(data) - visible}, total={len(data)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
