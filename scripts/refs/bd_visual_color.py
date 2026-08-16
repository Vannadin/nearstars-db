# 갈색왜성 가시광 지각색 도출기 — SVO BT-Settl 스펙트럼을 CIE 적분해 색조 헥스 산출 (광구색 방법론 §6 regime 4)
"""Brown-dwarf visual color from a BT-Settl model spectrum.

Downloads the BT-Settl (Allard & Homeier 2012) spectrum for (Teff, logg,
[M/H]=0) from the SVO theoretical spectra service, integrates 360-830 nm
against the CIE 1931 observer (scripts/refs/cie_color.py), and reports:

  - pre-clip linear sRGB (shows how far out of gamut the chromaticity is)
  - gamut-mapped hue hex (desaturated toward white just enough to fit sRGB)
  - CIE xy chromaticity
  - a 40%-value render tint (the phase-3 ember-dimming convention)

Grounding + validation anchors (see stellar-photospheric-color-methodology.md
regime 4): Burrows 2001 sec VI.2 (mechanism + the observed L5 soft magenta),
Cranmer 2021 RNAAS 5, 201 (published per-Teff RGB table, Zenodo
10.5281/zenodo.5293307). Saturation from any model is an upper bound - the
400-520 nm window has no T-type observational anchor.

Usage:  python3 scripts/refs/bd_visual_color.py [teff=900] [logg=5.0]
"""
import re
import sys
import bisect
import urllib.request

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cie_color import spectrum_to_xyz, rgb_to_hex

SVO = "http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=bt-settl"


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")


def find_fid(teff: int, logg: float, meta: float = 0.0) -> int:
    """SVO 인덱스 VOTable에서 (teff, logg, meta) 모델의 fid를 찾는다."""
    txt = _fetch(SVO + "&format=ascii")
    rows = re.findall(
        r"<TR>\s*<TD>(\d+)</TD><TD>([\d.]+)</TD><TD>([-\d.]+)</TD><TD>([-\d.]+)</TD>"
        r"<TD>\d+</TD><TD>[^<]*</TD>(?:<TD>[^<]*</TD>){4}<TD><!\[CDATA\[[^\]]*fid=(\d+)\]\]>",
        txt,
    )
    for t, g, m, _a, fid in rows:
        if int(t) == teff and float(g) == logg and float(m) == meta:
            return int(fid)
    raise SystemExit(f"no BT-Settl model for teff={teff} logg={logg} meta={meta}")


def load_spectrum(fid: int):
    """fid의 스펙트럼(Å, flux)을 받아 nm 기준 보간 함수로 돌려준다."""
    txt = _fetch(SVO + f"&fid={fid}")
    rows = re.findall(r"<TR>\s*<TD>([\d.eE+-]+)</TD>\s*<TD>([\d.eE+-]+)</TD>", txt)
    pts = sorted((float(a) / 10.0, float(b)) for a, b in rows)
    wl = [p[0] for p in pts]
    fx = [p[1] for p in pts]

    def intensity(w: float) -> float:
        i = bisect.bisect_left(wl, w)
        if i <= 0 or i >= len(wl):
            return 0.0
        w0, w1 = wl[i - 1], wl[i]
        return fx[i - 1] + (fx[i] - fx[i - 1]) * (w - w0) / (w1 - w0)

    return intensity


def _linrgb(X, Y, Z):
    return (
        3.2406 * X - 1.5372 * Y - 0.4986 * Z,
        -0.9689 * X + 1.8758 * Y + 0.0415 * Z,
        0.0557 * X - 0.2040 * Y + 1.0570 * Z,
    )


def _gamma(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def gamut_mapped_hue(X, Y, Z):
    """색역 밖 색을 흰색 방향으로 최소 감채도해 sRGB에 넣는다 (하드 클리핑 금지)."""
    r, g, b = _linrgb(X, Y, Z)
    m = max(r, g, b)
    r, g, b = r / m, g / m, b / m
    lo = min(r, g, b)
    if lo < 0:  # mix with white w=(1,1,1): (1-t)c + t, solve (1-t)lo + t = 0
        t = -lo / (1 - lo)
        r, g, b = ((1 - t) * c + t for c in (r, g, b))
        m = max(r, g, b)
        r, g, b = r / m, g / m, b / m
    return r, g, b


def main() -> None:
    teff = int(sys.argv[1]) if len(sys.argv) > 1 else 900
    logg = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    fid = find_fid(teff, logg)
    I = load_spectrum(fid)
    X, Y, Z = spectrum_to_xyz(I)
    r0, g0, b0 = _linrgb(X, Y, Z)
    m = max(r0, g0, b0)
    x, y = X / (X + Y + Z), Y / (X + Y + Z)
    r, g, b = gamut_mapped_hue(X, Y, Z)
    hue = rgb_to_hex((_gamma(r), _gamma(g), _gamma(b)))
    tint = rgb_to_hex(tuple(_gamma(c * 0.4) for c in (r, g, b)))
    print(f"BT-Settl teff={teff} logg={logg} (SVO fid {fid})")
    print(f"  pre-clip lin RGB : ({r0/m:+.3f}, {g0/m:+.3f}, {b0/m:+.3f})")
    print(f"  CIE xy           : ({x:.3f}, {y:.3f})")
    print(f"  gamut-mapped hue : {hue}")
    print(f"  40%-value tint   : {tint}")
    print("  NOTE: model saturation is an upper bound (no T-type blue-window")
    print("        observation exists); hue family is the grounded quantity.")


if __name__ == "__main__":
    main()
