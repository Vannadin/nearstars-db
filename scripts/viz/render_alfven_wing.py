# Proxima d 알펜 윙(sub-Alfvénic SPI) 개념도 — 시스템 뷰 + 행성 근접 뷰 2패널 PNG (numpy+PIL)
"""Proxima d Alfven-wing concept figure.

Physics: at 0.029 AU the M-dwarf wind is plausibly sub-Alfvenic (M_A ~ 0.3
assumed, extrapolated inward from Proxima-b wind models, Garraffo 2016 family)
-> no bow shock; instead the planet's 16 G field (Zapatero Osorio 2026 SPI)
connects directly to the star's field lines as a pair of Alfven wings, tilted
theta_A = arctan(M_A) from the background field. That magnetic connection is
the channel that phase-locks the star's flares to d's orbit.

Concept figure: scales exaggerated (planet/magnetosphere), wing tubes schematic.
No matplotlib in this environment: numpy + PIL only.
Usage: python3 scripts/viz/render_alfven_wing.py [out.png]
Default output: docs/img/proxima-d-alfven-wing.png
"""
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BG = (10, 12, 18)
FG = (236, 240, 248)
DIM = (140, 150, 168)
GRID = (44, 50, 64)
STAR = (255, 107, 87)
WING = (54, 215, 220)
CORE = (199, 146, 234)
PAUSE = (92, 207, 230)
ROCK = (60, 56, 51)
CAP = (42, 38, 34)

M_A = 0.3
TH = math.degrees(math.atan(M_A))   # ~17 deg

W, H = 1400, 680
PW = 660                            # panel width


def fonts():
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
        fs = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
        fb = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 17)
    except Exception:
        f = fs = fb = ImageFont.load_default()
    return f, fs, fb


def aline(dr, pts, color, width=1, alpha=255):
    c = color + (alpha,)
    dr.line(pts, fill=c, width=width)


def panel_system(img, ox, f, fs):
    """Panel A: star + near-radial field + planet + wing pair (system view)."""
    dr = ImageDraw.Draw(img, 'RGBA')
    cx, cy = ox + 90, H // 2        # star center
    px, py = ox + 520, H // 2       # planet
    scale = 34.0                    # px per unit

    # near-radial stellar field lines with slight spiral curvature
    for ang in np.linspace(-64, 64, 11):
        a = math.radians(ang)
        pts = []
        for r in np.linspace(1.2, 16.0, 70):
            curve = 0.010 * (r - 1.2) ** 2
            x = r * math.cos(a) - curve * math.sin(a)
            y = r * math.sin(a) + curve * math.cos(a)
            pts.append((cx + x * scale, cy + y * scale))
        aline(dr, pts, GRID, 1, 200)

    # Alfven wings: one branch along +B (toward the star), one along -B (away),
    # both tilted by theta_A into the wind-flow direction
    th = math.radians(TH)
    for sgn in (+1, -1):
        ux, uy = sgn * -math.cos(th), math.sin(th)   # +: toward star / -: away; both lean downstream
        L = (12.8 if sgn > 0 else 4.2) * scale
        for off in np.linspace(-10, 10, 7):
            aline(dr, [(px + off * 0.25, py + off),
                       (px + ux * L + off * 0.25, py + uy * L + off)],
                  WING, 2, 90)

    # star on top of wings
    r_star = 38
    dr.ellipse([cx - r_star, cy - r_star, cx + r_star, cy + r_star], fill=STAR)
    dr.text((cx, cy + r_star + 10), "Proxima Cen (M5.5)", fill=STAR, font=f, anchor="ma")

    # planet
    dr.ellipse([px - 7, py - 7, px + 7, py + 7], fill=CORE)
    dr.text((px, py + 14), "d  (0.029 AU)", fill=CORE, font=f, anchor="ma")

    dr.text((px - 175, py - 128), "Alfven wing", fill=WING, font=f, anchor="mm")
    dr.text((px - 175, py - 110), "(magnetic connection to the star)", fill=WING, font=fs, anchor="mm")
    dr.text((px - 150, py + 130), "flare particles channel down the wing", fill=FG, font=fs, anchor="mm")
    dr.text((px - 150, py + 146), "(SPI - flares phase-locked to the orbit)", fill=FG, font=fs, anchor="mm")

    dr.text((ox + 16, 66), f"sub-Alfvenic wind: M_A ~ {M_A} (assumed) -> no bow shock", fill=FG, font=f)
    dr.text((ox + 16, 86), f"wing tilt theta_A = arctan(M_A) = {TH:.0f} deg from the field", fill=FG, font=f)
    dr.text((ox + 16, 40), "A - system view (not to scale)", fill=FG, font=f)


def panel_closeup(img, ox, f, fs):
    """Panel B: closed dipole core + Shue magnetopause + wing pair + weathered caps."""
    dr = ImageDraw.Draw(img, 'RGBA')
    cx, cy = ox + PW // 2 + 30, H // 2
    s = 19.0                        # px per R_d
    to_star = -1                    # star is to the left (-x)

    # wings first (background): along +/- field (field ~ radial -> horizontal here),
    # tilted theta_A vertically
    th = math.radians(TH)
    for sgn in (+1, -1):
        ux, uy = sgn * to_star * math.cos(th), math.sin(th)  # one branch starward, one anti-starward
        L = 17 * s
        for off in np.linspace(-30, 30, 9):
            aline(dr, [(cx + off * 0.2, cy + off),
                       (cx + ux * L + off * 0.2, cy + uy * L + off)],
                  WING, 2, 70)

    # closed dipole field lines r = L cos^2(lambda)
    for Lsh in (2.0, 3.5, 5.0, 6.5):
        for mirror in (1, -1):
            pts = []
            for lam in np.linspace(-math.pi / 2, math.pi / 2, 160):
                r = Lsh * math.cos(lam) ** 2
                if r < 1.0:
                    continue
                x = mirror * r * math.cos(lam)
                y = r * math.sin(lam)
                pts.append((cx + x * s, cy + y * s))
            if len(pts) > 1:
                aline(dr, pts, CORE, 1, 190)

    # magnetopause: Shue-like r = R0*(2/(1+cos t))^0.5, nose 7 R_d toward star
    pts = []
    for t in np.linspace(-2.2, 2.2, 200):
        r = 7.0 * (2.0 / (1.0 + math.cos(t))) ** 0.5
        pts.append((cx + to_star * r * math.cos(t) * s, cy + r * math.sin(t) * s))
    aline(dr, pts, PAUSE, 2, 230)
    dr.text((cx + to_star * 7 * s - 8, cy - 78), "magnetopause", fill=PAUSE, font=f, anchor="rm")
    dr.text((cx + to_star * 7 * s - 8, cy - 60), "nose 7 R_d", fill=PAUSE, font=f, anchor="rm")

    # planet + weathered magnetic-pole caps
    r_p = s
    dr.ellipse([cx - r_p, cy - r_p, cx + r_p, cy + r_p], fill=ROCK)
    for sgn in (+1, -1):
        yy = cy + sgn * 0.62 * s
        dr.ellipse([cx - 0.45 * s, yy - 0.42 * s, cx + 0.45 * s, yy + 0.42 * s], fill=CAP)
    dr.text((cx + 60, cy - 150), "flare ions precipitate at the", fill=FG, font=fs)
    dr.text((cx + 60, cy - 134), "magnetic poles -> dark caps", fill=FG, font=fs)
    aline(dr, [(cx + 56, cy - 128), (cx + 6, cy - 0.95 * s - 4)], FG, 1, 180)

    dr.text((ox + 16, 40), "B - planet close-up (closed core + wing pair)", fill=FG, font=f)
    dr.text((ox + 16, 66), "<- to the star", fill=WING, font=f)


def main(out=None):
    out = out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '..', '..', 'docs', 'img', 'proxima-d-alfven-wing.png')
    img = Image.new('RGB', (W, H), BG)
    f, fs, fb = fonts()
    dr = ImageDraw.Draw(img)
    dr.text((W // 2, 14), "Proxima Cen d - sub-Alfvenic magnetosphere: Alfven wings, no bow shock",
            fill=FG, font=fb, anchor="ma")
    panel_system(img, 0, f, fs)
    panel_closeup(img, 700, f, fs)
    dr.text((W // 2, H - 22),
            "Concept figure. B_p 16 G (Zapatero Osorio 2026 SPI); M_A ~ 0.3 assumed; "
            "the wing pair carries the star-planet magnetic connection that phase-locks the flares.",
            fill=DIM, font=fs, anchor="ma")
    img.save(out)
    print('wrote', os.path.abspath(out))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
