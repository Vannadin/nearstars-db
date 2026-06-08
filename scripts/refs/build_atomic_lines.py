# NIST ASD에서 원자 라인·준위·이온화 데이터를 받아 db/refs/atomic_lines.yaml 생성 (Saha/Boltzmann 엔진 입력)
"""Fetch atomic line + level data from the NIST Atomic Spectra Database and
build `db/refs/atomic_lines.yaml` — the input to the LTE Saha/Boltzmann plasma
color engine.

For each spectrum we pull, in tab-delimited (format=3) form:
  - LINES  (lines1.pl):  observed/Ritz air wavelength, Einstein A_ki, lower/upper
    energies (cm^-1), statistical weights g_i/g_k — visible band 360-830 nm.
  - LEVELS (energy1.pl): the low-lying energy levels {E(cm^-1), g} used to build
    the partition function U(T) = Σ g_j exp(-E_j / kT).

Provenance is the live NIST ASD. Network is required; if urllib is blocked the
script falls back to a local cache directory of the raw TSV dumps
(`--cache-dir`, default /tmp/nist) so a build can be reproduced offline.

Curation choices (documented, bounded):
  - Keep only lines with a numeric A_ki (needed for opacity).
  - Bound line count per species: keep lines whose 10000 K brightness proxy
    (A_ki · g_k · exp(-E_k/kT)) is within REL_KEEP of the species max, capped
    at MAX_LINES. Weak/very-high-excitation lines are dropped; documented.
  - Keep the lowest LEVELS_KEEP energy levels for the (truncated) partition
    function — ample at T ≤ 20000 K where high levels are unpopulated.

Usage:
    python3 scripts/refs/build_atomic_lines.py            # fetch + write
    python3 scripts/refs/build_atomic_lines.py --sanity   # print checks, no write
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "db" / "refs" / "atomic_lines.yaml"

# Spectrum table: key, NIST spectrum name, element, ion stage, ionization
# energy of THIS stage (eV, NIST recommended values, physics.nist.gov ionization
# energy tables). χ is the energy to reach the next stage.
SPECIES = [
    # key,    nist,    elem, stage, chi_eV
    ("H_I",   "H I",   "H",  0, 13.598434),
    ("He_I",  "He I",  "He", 0, 24.587389),
    ("C_I",   "C I",   "C",  0, 11.260288),
    ("C_II",  "C II",  "C",  1, 24.383154),
    ("N_I",   "N I",   "N",  0, 14.534130),
    ("N_II",  "N II",  "N",  1, 29.600210),
    ("O_I",   "O I",   "O",  0, 13.618055),
    ("O_II",  "O II",  "O",  1, 35.121120),
    ("S_I",   "S I",   "S",  0, 10.360010),
    ("S_II",  "S II",  "S",  1, 23.337880),
    # transition metals + Mg — for metal-oxide bands (TiO/VO/FeO/MgO) and their
    # high-T dissociation→atomic march. Complex spectra; the top-80 brightness
    # filter keeps the dominant visible lines.
    ("Mg_I",  "Mg I",  "Mg", 0, 7.646236),
    ("Mg_II", "Mg II", "Mg", 1, 15.035271),
    ("Ti_I",  "Ti I",  "Ti", 0, 6.828120),
    ("Ti_II", "Ti II", "Ti", 1, 13.575500),
    ("V_I",   "V I",   "V",  0, 6.746190),
    ("V_II",  "V II",  "V",  1, 14.634000),
    ("Fe_I",  "Fe I",  "Fe", 0, 7.902468),
    ("Fe_II", "Fe II", "Fe", 1, 16.199200),
]

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

# Curation bounds
T_REF = 10000.0          # K, brightness-proxy pivot for line selection
KT_REF_CM = 0.695034 * T_REF
REL_KEEP = 1e-4          # keep lines with proxy >= REL_KEEP * max_proxy
MAX_LINES = 80           # hard cap per species
LEVELS_KEEP = 25         # lowest N levels for the partition function


def fetch(url: str, cache_path: Path, refresh: bool) -> str:
    """Return a NIST TSV. Cache-first (the cache IS NIST data); --refresh forces
    a live re-fetch. Network failure falls back to the cache when present."""
    if cache_path.exists() and not refresh:
        return cache_path.read_text(encoding="utf-8")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NearStars/atomic-lines"})
        with urllib.request.urlopen(req, timeout=30) as r:
            text = r.read().decode("utf-8", "replace")
        if "Invalid" in text or "Input Error" in text:
            raise ValueError("NIST returned an input/column error")
        cache_path.write_text(text, encoding="utf-8")   # refresh cache
        return text
    except Exception as e:
        if cache_path.exists():
            print(f"  (network fetch failed: {e}; using cache {cache_path.name})")
            return cache_path.read_text(encoding="utf-8")
        raise


_NUM_RE = re.compile(r"[+-]?\d*\.?\d+(?:[eE][+-]?\d+)?")


def _num(s: str):
    """Parse a NIST numeric cell. Strips quotes + bracket/paren annotations
    (theoretical/interpolated values), then matches the leading numeric token
    (incl. scientific notation like 3.69e+07). NIST "+x" unknown-offset cells
    yield no digit → None."""
    s = s.strip().strip('"').strip().strip("[](){}")
    if not s:
        return None
    m = _NUM_RE.match(s)
    if not m:
        return None
    try:
        return float(m.group())
    except ValueError:
        return None


def _rows(text: str, header_key: str):
    """Yield dict rows from a NIST format=3 TSV blob, keyed by header names."""
    header = None
    for raw in text.splitlines():
        if "\t" not in raw:
            continue
        cells = raw.split("\t")
        if header is None:
            if cells[0].strip().startswith(header_key):
                header = [c.strip() for c in cells]
            continue
        if len(cells) < len(header):
            continue
        yield dict(zip(header, cells))


def parse_lines(text: str) -> list[dict]:
    out = []
    for r in _rows(text, "obs_wl_air"):
        wl = _num(r.get("obs_wl_air(nm)", "")) or _num(r.get("ritz_wl_air(nm)", ""))
        aki = _num(r.get("Aki(s^-1)", ""))
        ek = _num(r.get("Ek(cm-1)", ""))
        ei = _num(r.get("Ei(cm-1)", ""))
        gk = _num(r.get("g_k", ""))
        gi = _num(r.get("g_i", ""))
        if wl is None or aki is None or ek is None or gk is None or gi is None:
            continue
        if not (360.0 <= wl <= 830.0):
            continue
        term = (r.get("term_k", "").strip().strip('"') or "")
        out.append({"nm": round(wl, 3), "A_ki": aki, "E_upper_cm": ek,
                    "E_lower_cm": ei if ei is not None else 0.0,
                    "g_upper": int(gk), "g_lower": int(gi), "term": term})
    return out


def select_lines(lines: list[dict]) -> list[dict]:
    if not lines:
        return []
    def proxy(ln):
        return ln["A_ki"] * ln["g_upper"] * math.exp(-ln["E_upper_cm"] / KT_REF_CM)
    pmax = max(proxy(ln) for ln in lines)
    kept = [ln for ln in lines if proxy(ln) >= REL_KEEP * pmax]
    kept.sort(key=proxy, reverse=True)
    kept = kept[:MAX_LINES]
    kept.sort(key=lambda ln: ln["nm"])
    return kept


def parse_levels(text: str) -> list[dict]:
    seen = []
    for r in _rows(text, "Configuration"):
        e = _num(r.get("Level (cm-1)", ""))
        g = _num(r.get("g", ""))
        if e is None or g is None:
            continue
        term = (r.get("Term", "").strip().strip('"') or "")
        seen.append({"E_cm": round(e, 3), "g": int(g), "term": term})
    seen.sort(key=lambda x: x["E_cm"])
    return seen[:LEVELS_KEEP]


def build(cache_dir: Path, refresh: bool = False) -> dict:
    cache_dir.mkdir(parents=True, exist_ok=True)
    out: dict = {}
    for key, nist, elem, stage, chi in SPECIES:
        spec = urllib.parse.quote_plus(nist)
        lt = fetch(LINES_URL.format(spec=spec), cache_dir / f"lines_{key.lower()}.txt", refresh)
        vt = fetch(LEVELS_URL.format(spec=spec), cache_dir / f"levels_{key.lower()}.txt", refresh)
        lines = select_lines(parse_lines(lt))
        levels = parse_levels(vt)
        out[key] = {
            "species": nist,
            "element": elem,
            "ion_stage": stage,
            "ionization_energy_eV": chi,
            "source": "NIST ASD (lines1.pl + energy1.pl, format=3); ionization energy from NIST recommended tables",
            "partition_levels": levels,
            "lines": lines,
        }
        print(f"  {key:6} lines_kept={len(lines):3} (of {len(parse_lines(lt))} visible w/ A)  "
              f"levels={len(levels)}")
    return out


HEADER = """\
# Atomic line + level + ionization data from the NIST Atomic Spectra Database.
# Input to the LTE Saha/Boltzmann plasma-emission color engine
# (scripts/refs/saha_boltzmann.py). Built by scripts/refs/build_atomic_lines.py.
#
# Per species: ionization_energy_eV (to the next stage), partition_levels
# [{E_cm,g}] for U(T)=Σ g·exp(-E/kT) (lowest 25, truncated — ample at T≤20000K),
# and lines [{nm, A_ki, E_upper_cm, g_upper, g_lower}] kept by a 10000K
# brightness proxy (top 80, ≥1e-4 of species max). Air wavelengths, 360-830 nm.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", default="/tmp/nist",
                    help="raw NIST TSV cache (used first; the cache IS NIST data)")
    ap.add_argument("--refresh", action="store_true", help="force live re-fetch from NIST")
    ap.add_argument("--sanity", action="store_true", help="print checks, do not write")
    args = ap.parse_args()

    data = build(Path(args.cache_dir), refresh=args.refresh)

    if args.sanity:
        print("\n=== anchors ===")
        for key in ("H_I", "O_I", "He_I", "C_II"):
            d = data[key]
            strong = max(d["lines"], key=lambda l: l["A_ki"]) if d["lines"] else None
            print(f"  {key}: chi={d['ionization_energy_eV']}eV  "
                  f"n_lines={len(d['lines'])}  strongest A: "
                  f"{strong['nm'] if strong else '-'}nm A={strong['A_ki']:.2e}" if strong else f"  {key}: no lines")
        return 0

    body = yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False)
    OUT.write_text(HEADER + body, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(data)} species)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
