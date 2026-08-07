# Proxima d 알펜 윙(sub-Alfvénic SPI) 물리 기하 도식 — 궤도면 뷰 + 자오면 근접 뷰 (numpy+PIL)
"""Proxima d Alfven-wing figure, physical geometry (Neubauer 1980; Saur+ 2013).

The wing axes are the Alfven characteristics c+- = u +- v_A*bhat: with a
near-radial stellar field at 0.029 AU and a sub-Alfvenic wind (v_A > u_wind),
one wing runs starward, the other anti-starward, and BOTH lean toward the
trailing side of the orbit (the aberration flow u_orb), each by its own angle:

    theta_starward  = arctan( u_orb / (v_A - u_wind) )   (leans more)
    theta_antistar  = arctan( u_orb / (v_A + u_wind) )   (leans less)

Numbers used (assumptions stated on the figure): u_orb = 61 km/s (computed,
sqrt(GM/a) for 0.122 M_sun at 0.029 AU), u_wind = 100 km/s (assumed slow wind
inside the Alfven surface), M_A = 0.3 -> v_A = |u|/M_A = 390 km/s
-> theta_starward ~ 12 deg, theta_antistar ~ 7 deg.

The wings are flux tubes of the obstacle's cross-section (the magnetosphere,
diameter ~ 2 x 7 R_d), attached to it - not lines through the planet. In this
regime there is no bow shock, and the "magnetotail" is really the
anti-starward wing. The starward wing's footpoint on the star is the SPI
flare site, phase-locked to the orbit.

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

# --- physics inputs (figure states which are assumed) ---
U_ORB = 61.0     # km/s, computed sqrt(GM/a)
U_WIND = 100.0   # km/s, ASSUMED slow wind inside the Alfven surface
M_A = 0.3        # ASSUMED
U_TOT = math.hypot(U_WIND, U_ORB)
V_A = U_TOT / M_A
TH_STAR = math.degrees(math.atan(U_ORB / (V_A - U_WIND)))   # ~12 deg
TH_ANTI = math.degrees(math.atan(U_ORB / (V_A + U_WIND)))   # ~7 deg

W, H = 1400, 700


def fonts():
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
        fs = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
        fb = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 17)
    except Exception:
        f = fs = fb = ImageFont.load_default()
    return f, fs, fb


def aline(dr, pts, color, width=1, alpha=255):
    dr.line(pts, fill=color + (alpha,), width=width)


def arrow(dr, x0, y0, x1, y1, color, width=2, alpha=255, head=7):
    aline(dr, [(x0, y0), (x1, y1)], color, width, alpha)
    ang = math.atan2(y1 - y0, x1 - x0)
    for da in (math.radians(150), -math.radians(150)):
        dr.line([(x1, y1), (x1 + head * math.cos(ang + da), y1 + head * math.sin(ang + da))],
                fill=color + (alpha,), width=width)


def panel_orbital(img, ox, f, fs):
    """Panel A: orbital-plane (top-down) view. Star left, planet right,
    orbital motion up-screen, aberration -> wings lean down-screen (trailing)."""
    dr = ImageDraw.Draw(img, 'RGBA')
    sx, sy = ox + 130, H // 2
    px, py = ox + 540, H // 2

    # orbit arc around the star through the planet
    R_orb = px - sx
    pts = [(sx + R_orb * math.cos(a), sy + R_orb * math.sin(a))
           for a in np.linspace(-0.55, 0.55, 60)]
    aline(dr, pts, GRID, 1, 220)

    # radial field lines
    for ang in np.linspace(-58, 58, 9):
        a = math.radians(ang)
        aline(dr, [(sx + 48 * math.cos(a), sy + 48 * math.sin(a)),
                   (sx + 560 * math.cos(a), sy + 560 * math.sin(a))], GRID, 1, 150)

    # --- wings: flux tubes of half-width ~ magnetosphere radius (exaggerated) ---
    hw = 9  # px half-width (obstacle cross-section, exaggerated for visibility)

    def tube(theta_deg, starward, L, taper=1.0):
        th = math.radians(theta_deg)
        sgn = -1 if starward else +1
        ux, uy = sgn * math.cos(th), math.sin(th)     # lean = screen +y (trailing)
        nx, ny = -uy, ux                              # unit normal
        p0 = np.array([px, py]); u = np.array([ux, uy]); n = np.array([nx, ny])
        if starward:
            # bend the last stretch onto the star (field converges radially)
            ts = np.linspace(0, 1, 60)
            path = []
            for t in ts:
                p = p0 + u * L * t
                blend = max(0.0, (t - 0.72) / 0.28) ** 2
                tostar = np.array([sx, sy]) - p
                tostar = tostar / np.linalg.norm(tostar)
                d = (1 - blend) * u + blend * tostar
                if len(path) == 0:
                    path.append(p)
                else:
                    step = L / len(ts)
                    path.append(path[-1] + d * step)
            path = np.array(path)
        else:
            path = np.array([p0 + u * L * t for t in np.linspace(0, 1, 30)])
        for s_off in (-hw, hw):
            edge = path + n * s_off * taper
            aline(dr, [tuple(p) for p in edge], WING, 2, 150)
        # translucent fill via many faint center lines
        for s_off in np.linspace(-hw + 2, hw - 2, 5):
            edge = path + n * s_off
            aline(dr, [tuple(p) for p in edge], WING, 1, 45)
        return path

    path_s = tube(TH_STAR, True, 395)
    tube(TH_ANTI, False, 210)

    # star drawn over the wing, footpoint marker where the wing lands
    r_star = 40
    dr.ellipse([sx - r_star, sy - r_star, sx + r_star, sy + r_star], fill=STAR)
    fp = path_s[-1]
    dr.ellipse([fp[0] - 5, fp[1] - 5, fp[0] + 5, fp[1] + 5], fill=(255, 230, 160))
    dr.text((sx, sy - r_star - 24), "Proxima Cen (M5.5)", fill=STAR, font=f, anchor="ma")
    dr.text((fp[0] + 4, fp[1] + 26), "wing footpoint = flare site", fill=(255, 230, 160), font=fs)
    dr.text((fp[0] + 4, fp[1] + 41), "(sweeps with the orbit -> phase-lock)", fill=(255, 230, 160), font=fs)

    # planet + orbital motion arrow (up-screen)
    dr.ellipse([px - 7, py - 7, px + 7, py + 7], fill=CORE)
    arrow(dr, px, py - 16, px, py - 58, FG, 2, 230)
    dr.text((px + 10, py - 56), "orbital motion", fill=FG, font=fs)
    dr.text((px + 12, py + 2), "d", fill=CORE, font=f)

    # angle labels
    dr.text((px - 190, py + 6), f"starward wing  theta ~ {TH_STAR:.0f} deg", fill=WING, font=f)
    dr.text((px + 40, py + 46), f"anti-starward wing  theta ~ {TH_ANTI:.0f} deg", fill=WING, font=fs)
    dr.text((px - 120, py + 96), "both lean toward the trailing side", fill=DIM, font=fs)
    dr.text((px - 120, py + 112), "(aberration u_orb = 61 km/s)", fill=DIM, font=fs)

    dr.text((ox + 16, 40), "A - orbital plane, top-down (not to scale; tube width exaggerated)",
            fill=FG, font=f)
    dr.text((ox + 16, 64),
            f"wing axes = u +- v_A: M_A ~ {M_A} (assumed), wind {U_WIND:.0f} km/s (assumed)",
            fill=FG, font=fs)
    dr.text((ox + 16, 80), "sub-Alfvenic -> no bow shock", fill=FG, font=fs)


def panel_meridional(img, ox, f, fs):
    """Panel B: meridional close-up. Star left; wing tubes attach to the
    magnetosphere cross-section; wing lean is azimuthal (out of this plane)."""
    dr = ImageDraw.Draw(img, 'RGBA')
    cx, cy = ox + 330, H // 2
    s = 15.0

    flank = 7.0 * math.sqrt(2.0)   # Shue r at t=90deg ~ 9.9 R_d

    # wing tubes: attached at the obstacle, spanning its cross-section
    for x0, x1, label, lx in ((0, -21.5, "starward wing", -20.0),
                              (0, 21.5, "anti-starward wing (replaces the magnetotail)", 3.0)):
        top = cy - flank * s
        bot = cy + flank * s
        # edges
        aline(dr, [(cx + x0 * s, top), (cx + x1 * s, top)], WING, 2, 150)
        aline(dr, [(cx + x0 * s, bot), (cx + x1 * s, bot)], WING, 2, 150)
        for yy in np.linspace(top + 8, bot - 8, 7):
            aline(dr, [(cx + x0 * s, yy), (cx + x1 * s, yy)], WING, 1, 35)
        dr.text((cx + lx * s, top - 18), label, fill=WING, font=fs)

    # background field lines through the region (radial ~ horizontal)
    for yy in np.linspace(cy - flank * s - 40, cy + flank * s + 40, 6):
        aline(dr, [(ox + 20, yy), (ox + 660, yy)], GRID, 1, 90)

    # magnetopause (Shue, nose 7 R_d toward the star = left)
    pts = []
    for t in np.linspace(-2.2, 2.2, 200):
        r = 7.0 * (2.0 / (1.0 + math.cos(t))) ** 0.5
        pts.append((cx - r * math.cos(t) * s, cy + r * math.sin(t) * s))
    aline(dr, pts, PAUSE, 2, 235)
    dr.text((cx - 7.4 * s, cy - 30), "nose 7 R_d", fill=PAUSE, font=f, anchor="rm")

    # closed dipole core
    for Lsh in (2.0, 3.5, 5.0):
        for mirror in (1, -1):
            pp = []
            for lam in np.linspace(-math.pi / 2, math.pi / 2, 160):
                r = Lsh * math.cos(lam) ** 2
                if r < 1.0:
                    continue
                pp.append((cx + mirror * r * math.cos(lam) * s, cy + r * math.sin(lam) * s))
            if len(pp) > 1:
                aline(dr, pp, CORE, 1, 200)

    # planet + weathered caps + precipitation arrows along polar field
    r_p = s
    dr.ellipse([cx - r_p, cy - r_p, cx + r_p, cy + r_p], fill=ROCK)
    for sgn in (+1, -1):
        yy = cy + sgn * 0.62 * s
        dr.ellipse([cx - 0.45 * s, yy - 0.4 * s, cx + 0.45 * s, yy + 0.4 * s], fill=CAP)
        arrow(dr, cx, cy + sgn * (flank * s - 6), cx, cy + sgn * 1.5 * s, (255, 230, 160), 2, 200)
    dr.text((cx + 14, cy - 3.6 * s), "wing ions precipitate", fill=(255, 230, 160), font=fs)
    dr.text((cx + 14, cy - 3.6 * s + 15), "onto the poles -> dark caps", fill=(255, 230, 160), font=fs)

    dr.text((ox + 16, 40), "B - meridional close-up (wing tubes attach to the magnetosphere)",
            fill=FG, font=f)
    dr.text((ox + 16, 64), f"wing lean ({TH_ANTI:.0f}-{TH_STAR:.0f} deg) is azimuthal - out of this plane",
            fill=FG, font=fs)
    dr.text((ox + 16, 80), "<- to the star", fill=WING, font=fs)


def main(out=None):
    out = out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '..', '..', 'docs', 'img', 'proxima-d-alfven-wing.png')
    img = Image.new('RGB', (W, H), BG)
    f, fs, fb = fonts()
    dr = ImageDraw.Draw(img)
    dr.text((W // 2, 12), "Proxima Cen d - Alfven wings (sub-Alfvenic star-planet interaction)",
            fill=FG, font=fb, anchor="ma")
    panel_orbital(img, 0, f, fs)
    panel_meridional(img, 700, f, fs)
    dr.text((W // 2, H - 22),
            "Wing axes c+- = u +- v_A (Neubauer 1980; Saur+ 2013). B_p 16 G = Zapatero Osorio 2026 SPI; "
            "u_orb 61 km/s computed; wind 100 km/s and M_A 0.3 assumed.",
            fill=DIM, font=fs, anchor="ma")
    img.save(out)
    print('wrote', os.path.abspath(out))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
