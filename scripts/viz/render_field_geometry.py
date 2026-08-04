# 행성 자기장 기하(쌍극 vs 다중극) 도식 렌더러 — 자오면 자기력선 + 표면 B_r 지도 + 오로라 발자국
"""Render the *shape* of a planetary field, not its strength.

The rocky-dynamo recipe (docs/reference/rocky-planet-dynamo-methodology.md) gates on
the local Rossby number: `Ro_l < 0.12` gives a dipolar field, above it the dynamo goes
**multipolar** and the dipole moment collapses to ~0.06x. That gate is a statement about
geometry, and geometry is what the player actually sees: a dipolar field puts aurora in
two clean polar caps, a multipolar one scatters it into patches down to mid-latitudes.

This renders both cases side by side from a potential-field (Gauss coefficient) model so
an art-direction choice can be made against a picture instead of a sentence.

**Schematic, not a dynamo simulation.** The multipolar coefficient set is a seeded
realization with the spectrum weighted the way the literature describes (dipole no longer
dominant); it is not a solution of the induction equation. Field-line tracing is done in
the meridional plane, so the azimuthal component is not drawn.

Usage: python3 scripts/viz/render_field_geometry.py [out.png]
Default output: docs/img/field-geometry.png
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ---- palette (NearStars Design System v2 dark surface) ----
BG = (10, 12, 18)
FG = (236, 240, 248)
DIM = (140, 150, 168)
GRID = (44, 50, 64)
POS = (232, 120, 90)     # field out of the surface
NEG = (110, 160, 255)    # field into the surface
AUR = (150, 240, 200)    # auroral footprint
BODY = (30, 34, 44)

L_MAX = 4


def _legendre(lmax: int, ct: np.ndarray):
    """Schmidt semi-normalized P_lm(cos t) and dP_lm/dt, as dicts keyed (l, m)."""
    st = np.sqrt(np.maximum(0.0, 1.0 - ct * ct))
    P = {(0, 0): np.ones_like(ct)}
    dP = {(0, 0): np.zeros_like(ct)}
    for l in range(1, lmax + 1):
        for m in range(0, l + 1):
            if m == l:                                     # sectoral seed
                k = math.sqrt((2 * l - 1) / (2 * l)) if l > 1 else 1.0
                P[(l, m)] = k * st * P[(l - 1, l - 1)]
                dP[(l, m)] = k * (ct * P[(l - 1, l - 1)] + st * dP[(l - 1, l - 1)])
            else:
                a = (2 * l - 1) / math.sqrt((l - m) * (l + m))
                P[(l, m)] = a * ct * P[(l - 1, m)]
                dP[(l, m)] = a * (ct * dP[(l - 1, m)] - st * P[(l - 1, m)])
                if l - 2 >= m:
                    b = math.sqrt(((l - 1) ** 2 - m * m) / ((l - m) * (l + m)))
                    P[(l, m)] -= b * P[(l - 2, m)]
                    dP[(l, m)] -= b * dP[(l - 2, m)]
    return P, dP


def field(coeffs, r, theta, phi):
    """B_r, B_theta from Gauss coefficients {(l,m): (g,h)}; r in body radii."""
    ct = np.cos(theta)
    P, dP = _legendre(L_MAX, ct)
    Br = np.zeros_like(r, dtype=float)
    Bt = np.zeros_like(r, dtype=float)
    for (l, m), (g, h) in coeffs.items():
        if g == 0.0 and h == 0.0:
            continue
        rad = r ** (-(l + 2))
        ang = g * np.cos(m * phi) + h * np.sin(m * phi)
        Br += (l + 1) * rad * ang * P[(l, m)]
        Bt += -rad * ang * dP[(l, m)]
    return Br, Bt


DIPOLAR = {(1, 0): (-1.0, 0.0)}          # axial dipole, Earth-like reference

def multipolar(seed: int = 20260804):
    """Dipole present but not dominant; power spread to l = 2..4.

    Weighting follows the qualitative picture in the dipolar/multipolar literature
    (Olson & Christensen 2006): past the Rossby gate the axial dipole is no longer the
    leading term. Amplitudes here are a seeded realization, not a fitted model.
    """
    rng = np.random.default_rng(seed)
    c = {(1, 0): (-0.35, 0.0)}
    for l in range(2, L_MAX + 1):
        scale = 1.0 / l ** 0.5
        for m in range(0, l + 1):
            g = float(rng.normal(0, scale))
            h = 0.0 if m == 0 else float(rng.normal(0, scale))
            c[(l, m)] = (g, h)
    return c


def icegiant(tilt_deg=50.0, offset=0.4, seed=20260804):
    """Tilted + offset multipolar field, the Uranus/Neptune shape.

    A dipole tilted by `tilt_deg` puts power into g11 as well as g10. Displacing that
    dipole along its axis by `offset` body radii is, to leading order, a quadrupole of
    g20 ≈ 2·offset·g10, which is why an "offset dipole" is already a multipolar field.
    Thin-shell convection then adds the rest of the l = 2-3 power.
    """
    t = math.radians(tilt_deg)
    g10 = -math.cos(t)
    c = {(1, 0): (g10, 0.0), (1, 1): (-math.sin(t), 0.0),
         (2, 0): (2.0 * offset * g10, 0.0)}
    rng = np.random.default_rng(seed)
    for l in (2, 3):
        for m in range(0, l + 1):
            g, h = c.get((l, m), (0.0, 0.0))
            sc = 0.35 / l ** 0.5
            c[(l, m)] = (g + float(rng.normal(0, sc)),
                         h + (0.0 if m == 0 else float(rng.normal(0, sc))))
    return c


def trace_lines(coeffs, n_seed=13, r_max=6.0, steps=2600, ds=0.02):
    """Meridional (phi = 0 and pi) field lines, integrated both ways from the surface."""
    lines = []
    for sign, phi in ((1, 0.0), (-1, math.pi)):
        for k in range(n_seed):
            th0 = math.pi * (k + 0.5) / n_seed
            for direction in (1.0, -1.0):
                x = 1.001 * math.sin(th0) * sign
                z = 1.001 * math.cos(th0)
                pts = [(x, z)]
                for _ in range(steps):
                    r = math.hypot(x, z)
                    if r < 0.999 or r > r_max:
                        break
                    th = math.acos(max(-1.0, min(1.0, z / r)))
                    br, bt = field(coeffs, np.array([r]), np.array([th]), np.array([phi]))
                    br, bt = float(br[0]), float(bt[0])
                    # spherical -> plane (x is the phi=0 meridian direction)
                    ex, ez = math.sin(th), math.cos(th)
                    tx, tz = math.cos(th), -math.sin(th)
                    bx = (br * ex + bt * tx) * sign
                    bz = br * ez + bt * tz
                    n = math.hypot(bx, bz)
                    if n < 1e-12:
                        break
                    x += direction * ds * bx / n
                    z += direction * ds * bz / n
                    pts.append((x, z))
                if len(pts) > 12:
                    lines.append(pts)
    return lines


def field_cart(coeffs, xyz):
    """Vectorized B in Cartesian for an (N,3) array of positions (body radii)."""
    x, y, z = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    r = np.sqrt(x * x + y * y + z * z)
    r = np.maximum(r, 1e-9)
    th = np.arccos(np.clip(z / r, -1.0, 1.0))
    ph = np.arctan2(y, x)
    st = np.sin(th)
    ct = np.cos(th)
    P, dP = _legendre(L_MAX, ct)
    Br = np.zeros_like(r); Bt = np.zeros_like(r); Bp = np.zeros_like(r)
    for (l, m), (g, h) in coeffs.items():
        if g == 0.0 and h == 0.0:
            continue
        rad = r ** (-(l + 2))
        cs = g * np.cos(m * ph) + h * np.sin(m * ph)
        sn = g * np.sin(m * ph) - h * np.cos(m * ph)
        Br += (l + 1) * rad * cs * P[(l, m)]
        Bt += -rad * cs * dP[(l, m)]
        if m:
            Bp += rad * m * sn * P[(l, m)] / np.maximum(st, 1e-6)
    cp, sp = np.cos(ph), np.sin(ph)
    bx = Br * st * cp + Bt * ct * cp - Bp * sp
    by = Br * st * sp + Bt * ct * sp + Bp * cp
    bz = Br * ct - Bt * st
    return np.stack([bx, by, bz], axis=1)


def open_field_footprint(coeffs, nlon=96, nlat=48, r_open=4.0, steps=1400, ds=0.03):
    """Mark surface cells whose field line escapes to r_open (an auroral footprint).

    This is the physical criterion: aurora lights up where field lines are open to the
    outside, so precipitating particles reach the atmosphere. A dipole gives two polar
    caps; a multipolar field scatters the caps into patches.
    """
    lon = np.linspace(-math.pi, math.pi, nlon)
    lat = np.linspace(math.pi / 2, -math.pi / 2, nlat)
    PH, LA = np.meshgrid(lon, lat)
    th = math.pi / 2 - LA.ravel()
    ph = PH.ravel()
    seed = np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], axis=1) * 1.02
    opened = np.zeros(seed.shape[0], dtype=bool)
    for direction in (1.0, -1.0):          # a line is open if either end escapes
        pos = seed.copy()
        alive = np.ones(pos.shape[0], dtype=bool)
        for _ in range(steps):
            if not alive.any():
                break
            b = field_cart(coeffs, pos[alive])
            n = np.linalg.norm(b, axis=1, keepdims=True)
            n = np.maximum(n, 1e-12)
            pos[alive] += direction * ds * b / n
            r = np.linalg.norm(pos, axis=1)
            esc = alive & (r > r_open)
            opened |= esc
            back = alive & (r < 0.995)
            alive = alive & ~esc & ~back
    return opened.reshape(nlat, nlon)


def surface_br(coeffs, nlon=360, nlat=180):
    lon = np.linspace(-math.pi, math.pi, nlon)
    lat = np.linspace(math.pi / 2, -math.pi / 2, nlat)
    PH, TH = np.meshgrid(lon, math.pi / 2 - lat)
    R = np.ones_like(PH)
    br, _ = field(coeffs, R, TH, PH)
    return br


def _blend(dst, box, rgb, alpha):
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", dst.size, rgb + (0,))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=rgb + (int(alpha * 255),))
    return Image.alpha_composite(dst, layer)


def draw_panel(img, ox, oy, w, h, coeffs, title, subtitle, font, fsmall):
    d = ImageDraw.Draw(img)
    cx, cy = ox + w // 2, oy + h // 2 + 10
    scale = min(w, h) * 0.155
    d.text((ox + 14, oy + 8), title, font=font, fill=FG)
    d.text((ox + 14, oy + 30), subtitle, font=fsmall, fill=DIM)
    limit = min(cx - ox - 8, ox + w - cx - 8, cy - (oy + 52), oy + h - cy - 8)
    for rr in (2, 3, 4):
        r = rr * scale
        if r <= limit:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GRID)
    clip = (ox + 6, oy + 52, ox + w - 6, oy + h - 6)
    for pts in trace_lines(coeffs, r_max=5.0):
        xy = [(cx + x * scale, cy - z * scale) for x, z in pts]
        seg = []
        for X, Y in xy:
            if clip[0] <= X <= clip[2] and clip[1] <= Y <= clip[3]:
                seg.append((X, Y))
            else:
                if len(seg) > 1:
                    d.line(seg, fill=(92, 104, 128), width=1)
                seg = []
        if len(seg) > 1:
            d.line(seg, fill=(92, 104, 128), width=1)
    r = scale
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BODY, outline=(70, 78, 96))
    # surface radial field, drawn as coloured arcs around the limb
    th = np.linspace(0, math.pi, 181)
    br, _ = field(coeffs, np.ones_like(th), th, np.zeros_like(th))
    br2, _ = field(coeffs, np.ones_like(th), th, np.full_like(th, math.pi))
    m = max(np.abs(br).max(), np.abs(br2).max()) or 1.0
    for arr, sgn in ((br, 1), (br2, -1)):
        for i, t in enumerate(th):
            v = arr[i] / m
            col = POS if v > 0 else NEG
            a = min(1.0, abs(v))
            x = cx + sgn * math.sin(t) * scale
            y = cy - math.cos(t) * scale
            rr = 1.6 + 2.6 * a
            d.ellipse([x - rr, y - rr, x + rr, y + rr],
                      fill=tuple(int(c * (0.25 + 0.75 * a)) for c in col))
    return cx, cy, scale


def draw_map(img, ox, oy, w, h, coeffs, title, font, fsmall):
    d = ImageDraw.Draw(img)
    d.text((ox + 14, oy + 8), title, font=font, fill=FG)
    br = surface_br(coeffs)
    m = np.abs(br).max() or 1.0
    nlat, nlon = br.shape
    mw, mh = w - 40, h - 60
    x0, y0 = ox + 20, oy + 40
    cell = Image.new("RGB", (nlon, nlat))
    px = cell.load()
    for j in range(nlat):
        for i in range(nlon):
            v = br[j, i] / m
            base = POS if v > 0 else NEG
            a = min(1.0, abs(v)) ** 0.7
            px[i, j] = tuple(int(BG[k] + (base[k] - BG[k]) * a) for k in range(3))
    img.paste(cell.resize((mw, mh), Image.BILINEAR), (x0, y0))
    # auroral footprint: open field lines (traced), not a |B_r| threshold
    fp = open_field_footprint(coeffs)
    fj, fi = fp.shape
    d2 = ImageDraw.Draw(img)
    for j in range(fj):
        for i in range(fi):
            if fp[j, i]:
                X = x0 + (i + 0.5) * mw / fi
                Y = y0 + (j + 0.5) * mh / fj
                d2.ellipse([X - 2, Y - 2, X + 2, Y + 2], fill=AUR)
    d.rectangle([x0, y0, x0 + mw, y0 + mh], outline=GRID)
    d.text((x0, y0 + mh + 6), "경도 -180 ~ +180, 위도 +90 ~ -90 (등장방형)", font=fsmall, fill=DIM)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    case = "c" if "--case=c" in sys.argv or "--icegiant" in sys.argv else "b"
    default = ("docs/img/field-geometry-proxima-c.png" if case == "c"
               else "docs/img/field-geometry.png")
    out = args[0] if args else default
    W, H = 1500, 1180
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 19)
        fsmall = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 14)
        fbig = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 27)
    except OSError:
        font = fsmall = fbig = ImageFont.load_default()

    d.text((36, 26), "자기장 기하: 쌍극 vs 다중극" if case == "b" else "자기장 기하: 축대칭 다중극 vs 기울고 이탈한 다중극",
           font=fbig, fill=FG)
    d.text((36, 64), "Ro_l = 0.12 게이트가 강도만이 아니라 형태를 바꾼다. 붉은색 = 표면에서 나오는 자기장, "
                     "푸른색 = 들어가는 자기장, 연두색 = 오로라 발자국(r > 4까지 열린 자기력선을 추적해 표시).",
           font=fsmall, fill=DIM)

    if case == "c":
        left, right = multipolar(), icegiant()
        lt = ("다중극, 축대칭 — Proxima Cen b",
              "느린 자전이 형태를 정한다. 축은 그대로 두고 쌍극 지배력만 잃는다.")
        rt = ("기울고 이탈한 다중극 — Proxima Cen c 채택",
              "얇은 전도층 대류. 축이 50° 기울고 0.4 R 밀려나며 l = 2~3이 섞인다.")
        lm = "표면 B_r — b: 축을 따라 반점이 남는다"
        rm = "표면 B_r — c: 기울기·이탈로 발자국이 한쪽으로 몰린다"
    else:
        left, right = DIPOLAR, multipolar()
        lt = ("쌍극 (Ro_l < 0.12) — 지구 기준",
              "축대칭 쌍극자 하나. 자기력선이 두 극으로 모인다.")
        rt = ("다중극 (Ro_l > 0.12) — Proxima Cen b 채택",
              "쌍극 성분이 지배력을 잃고 l = 2~4가 섞인다. 모멘트는 0.06배로 붕괴.")
        lm = "표면 B_r — 쌍극: 두 극에 열린 극관 하나씩"
        rm = "표면 B_r — 다중극: 중위도까지 흩어진 발자국 반점"
    draw_panel(img, 30, 100, 720, 520, left, lt[0], lt[1], font, fsmall)
    draw_panel(img, 760, 100, 710, 520, right, rt[0], rt[1], font, fsmall)
    draw_map(img, 30, 630, 720, 500, left, lm, font, fsmall)
    draw_map(img, 760, 630, 710, 500, right, rm, font, fsmall)

    d.text((36, H - 26), "도식이며 dynamo 해가 아니다. 다중극 계수는 seed 20260804의 실현값 "
                         "(문헌이 기술하는 스펙트럼 가중을 따름). 근거: rocky-planet-dynamo-methodology.md",
           font=fsmall, fill=DIM)

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out)
    print(f"[ok] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
