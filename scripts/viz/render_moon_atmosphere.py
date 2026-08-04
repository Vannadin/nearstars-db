# 대기 보유 가능한 대형 위성이 성립하는지를 3패널로 시각화 (Jeans 보유 한계 + 동기궤도 + 실측 선례 스케일)
"""Moon-atmosphere feasibility figure.

Three panels answering "can this moon hold an atmosphere?":
  A. system layout in parent radii -- rings, moon orbit, and the *synchronous
     orbit* line (inside it a moon spirals in, Phobos-style).
  B. moons drawn to a common scale, with atmosphere shells where they exist.
  C. retention diagram: moon radius vs surface temperature, with the Jeans
     lambda = 25 / 60 contours for N2 and the real bodies plotted.

Grounding: Jeans parameter lambda = G M mu / (k T R); bodies with lambda > ~60
keep N2 over Gyr (Pluto 62, Triton 94, Titan 125), below ~25 it blows off
(Charon 11 -- and Charon indeed has no atmosphere).

No matplotlib in this environment: numpy + PIL only.
Usage: python3 scripts/viz/render_moon_atmosphere.py [out.png]
"""
import math
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

K_B = 1.380649e-23
G = 6.674e-11
AMU = 1.66054e-27

BG = (12, 14, 20)
INK = (232, 237, 246)
DIM = (136, 147, 166)
LINE = (44, 56, 76)
ACC = (122, 162, 255)
WARM = (255, 154, 82)
GOOD = (127, 209, 160)
BAD = (255, 107, 90)


def font(sz, bold=False):
    """AppleSDGothicNeo carries both Latin and Hangul (index 1 = Bold)."""
    try:
        return ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc",
                                  sz, index=2 if bold else 0)
    except OSError:
        pass
    for p in ("/System/Library/Fonts/Supplemental/AppleGothic.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def lam(M, R, T, mu=28):
    """Jeans escape parameter for molecular weight mu."""
    return G * M * mu * AMU / (K_B * T * R)


def mass(R_km, rho):
    return rho * 1000 * 4 / 3 * math.pi * (R_km * 1e3) ** 3


# ---- bodies: (label, R_km, rho, T_surf_K, atmosphere)  atmosphere: None or (label, kind)
MOONS = [
    ("Titan",   2575, 1.88,  94, ("1.5 bar N2", "thick")),
    ("Ganymede", 2634, 1.94, 110, None),
    ("Triton",  1353, 2.06,  38, ("1.4 Pa N2", "thin")),
    ("Pluto",   1188, 1.85,  40, ("~1 Pa N2", "thin")),
    ("Charon",   606, 1.70,  53, None),
    ("Enceladus", 252, 1.61,  75, None),
    ("Mimas",    198, 1.15,  64, None),
]
# our candidates
CAND = [
    ("Proxima c I\n(652 km)", 326, 1.60, 45, None, BAD),
    ("Pluto-class\nc I (2500 km)", 1250, 1.60, 45, ("~1 Pa N2", "thin"), WARM),
    ("Titan-class moon\nat eps Eri b", 2575, 1.88, 100, ("thick N2", "thick"), GOOD),
]

# ---- systems: (label, R_parent_km, P_rot_parent_h, M_parent_kg, rings(Rp lo,hi) or None,
#                [(moon, a_Rp, R_km, has_atm)])
M_E = 5.972e24
SYSTEMS = [
    ("Saturn / Titan", 60268, 10.56, 5.683e26, (1.24, 2.27),
     [("Titan", 20.3, 2575, True)]),
    ("Neptune / Triton", 24622, 16.11, 1.024e26, None,
     [("Triton", 14.4, 1353, True)]),
    ("Proxima c / c I  (proposed)", 17202, 27.0, 8 * M_E, (1.40, 3.00),
     [("c I", 7.0, 326, False)]),
    ("eps Eri b / Titan-class  (idea)", 89832, 10.0, 317.8 * M_E, None,
     [("moon", 20.0, 2575, True)]),
]


def sync_radius(M, P_h, R_km):
    a = (G * M * (P_h * 3600 / (2 * math.pi)) ** 2) ** (1 / 3)
    return a / (R_km * 1e3)


def main(out="docs/img/moon-atmosphere-feasibility.png"):
    W, H = 1700, 990
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f9, f10, f11, f13 = font(11), font(12), font(13), font(15)

    d.text((30, 20), "대기 있는 대형 위성이 성립하는가", font=font(24, True), fill=INK)
    d.text((30, 56), "Jeans 보유 한계 + 동기궤도 + 실측 선례 스케일  ·  NearStars Phase 4",
           font=f11, fill=DIM)

    # ================= PANEL A: system layouts =================
    ax0, ay0, axw = 210, 128, 700
    d.text((30, ay0 - 26), "A. 계 배치 (모행성 반지름 단위)", font=f13, fill=INK)
    d.text((30, ay0 - 8), "회색 띠 = 고리 · 주황 점선 = 동기궤도(이 안쪽이면 조석으로 감겨 들어감)",
           font=f9, fill=DIM)
    XMAX, rowh = 23.0, 96
    ppu = axw / XMAX
    for i, (lbl, Rp, Prot, Mp, rings, moons) in enumerate(SYSTEMS):
        y = ay0 + 44 + i * rowh
        rs = sync_radius(Mp, Prot, Rp)
        d.text((30, y - 30), lbl, font=f11, fill=INK)
        d.text((30, y - 13), f"R_p {Rp:,} km · 자전 {Prot:g} h", font=f9, fill=DIM)
        d.line([(ax0, y), (ax0 + axw, y)], fill=LINE)
        # parent: quarter disk clipped at the axis start
        pr = 26
        d.ellipse([ax0 - pr, y - pr, ax0 + pr, y + pr], fill=(58, 72, 96))
        d.ellipse([ax0 - pr, y - pr, ax0 + pr, y + pr], outline=(86, 104, 134))
        if rings:
            lo, hi = rings
            d.rectangle([ax0 + lo * ppu, y - 4, ax0 + hi * ppu, y + 4],
                        fill=(158, 164, 176))
            d.text((ax0 + lo * ppu, y + 9), "고리", font=f9, fill=(158, 164, 176))
        if rs < XMAX:
            xs = ax0 + rs * ppu
            for yy in range(int(y - 26), int(y + 27), 7):
                d.line([(xs, yy), (xs, yy + 4)], fill=WARM)
            d.text((xs - 12, y - 44), f"동기 {rs:.1f}", font=f9, fill=WARM)
        for mn, a_rp, mr_km, atm in moons:
            x = ax0 + a_rp * ppu
            rr = max(4.0, mr_km / Rp * 26)
            col = GOOD if atm else BAD
            if atm:
                d.ellipse([x - rr - 4, y - rr - 4, x + rr + 4, y + rr + 4],
                          outline=(120, 200, 160))
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col)
            d.text((x + rr + 8, y - 14), f"{mn}  {a_rp:.1f} R_p", font=f10, fill=INK)
            d.text((x + rr + 8, y + 2), "대기 유지" if atm else "대기 불가",
                   font=f9, fill=col)
            if a_rp < rs:
                d.text((x - 20, y + 16), "조석 감김", font=f9, fill=BAD)

    # ================= PANEL B: moons to scale =================
    by = ay0 + 44 + len(SYSTEMS) * rowh + 118
    d.text((30, by - 178), "B. 위성 실제 크기 (같은 축척) — 초록 테두리 = 대기 보유",
           font=f13, fill=INK)
    scale = 0.0265
    x = 108
    strip = [(m[0], m[1], m[4] is not None, (150, 160, 178)) for m in MOONS] + \
            [(c[0].replace("\n", " "), c[1], c[4] is not None, c[5]) for c in CAND[:2]]
    for name, R_km, has_atm, col in strip:
        r = R_km * scale
        d.ellipse([x - r, by - 2 * r, x + r, by], fill=col)
        if has_atm:
            d.ellipse([x - r - 5, by - 2 * r - 5, x + r + 5, by + 5],
                      outline=(120, 200, 160))
        short = name.replace("Pluto-class c I (2500 km)", "c I 2500 km 안") \
                    .replace("Proxima c I (652 km)", "c I 652 km 안")
        d.text((x - 30, by + 12), short[:16], font=f9, fill=INK)
        d.text((x - 30, by + 27), f"{R_km} km", font=f9, fill=DIM)
        x += 2 * r + 56

    # ================= PANEL C: retention diagram =================
    cx0, cy0, cw, ch = 1130, 172, 500, 400
    d.text((cx0, cy0 - 44), "C. N₂ 보유 가능 영역", font=f13, fill=INK)
    d.text((cx0, cy0 - 26), "Jeans λ = GMμ/kTR  ·  λ>60 보유 · λ<25 날림 (밀도 1.9 기준선)",
           font=f9, fill=DIM)
    Tlo, Thi, Rlo, Rhi = 25, 125, 120, 3400
    C = G * (1.9 * 1000 * 4 / 3 * math.pi) * 28 * AMU / K_B * 1e6   # lambda = C R_km^2 /T *1e-6

    def px(T, R):
        return (cx0 + (T - Tlo) / (Thi - Tlo) * cw,
                cy0 + ch - (math.log10(R) - math.log10(Rlo)) /
                (math.log10(Rhi) - math.log10(Rlo)) * ch)

    def R_of(lv, T):
        # C absorbs the km^2 conversion, so this is already in km
        return math.sqrt(lv * T / C)

    # shaded bands, clipped to the frame
    for i in range(0, cw):
        T = Tlo + i / cw * (Thi - Tlo)
        xx = cx0 + i
        _, y60 = px(T, min(max(R_of(60, T), Rlo), Rhi))
        _, y25 = px(T, min(max(R_of(25, T), Rlo), Rhi))
        d.line([(xx, cy0 + 1), (xx, y60)], fill=(20, 40, 32))
        d.line([(xx, y25), (xx, cy0 + ch - 1)], fill=(38, 22, 24))
    # contours
    for lv, col in ((60, GOOD), (25, BAD)):
        pts = []
        for i in range(0, cw + 1, 3):
            T = Tlo + i / cw * (Thi - Tlo)
            R = R_of(lv, T)
            if Rlo <= R <= Rhi:
                pts.append(px(T, R))
        if len(pts) > 1:
            d.line(pts, fill=col, width=2)
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], outline=LINE)
    for T in (40, 60, 80, 100, 120):
        x1, _ = px(T, Rlo)
        d.line([(x1, cy0 + ch), (x1, cy0 + ch + 5)], fill=DIM)
        d.text((x1 - 9, cy0 + ch + 9), f"{T}", font=f9, fill=DIM)
    d.text((cx0 + cw / 2 - 44, cy0 + ch + 30), "표면 온도 [K]", font=f10, fill=DIM)
    for R in (200, 500, 1000, 2000, 3000):
        _, y1 = px(Tlo, R)
        d.line([(cx0 - 5, y1), (cx0, y1)], fill=DIM)
        d.text((cx0 - 48, y1 - 7), f"{R}", font=f9, fill=DIM)
    d.text((cx0 - 52, cy0 - 8), "반지름 [km]", font=f9, fill=DIM)
    d.text((cx0 + 14, cy0 + 14), "보유 영역 (λ>60)", font=f10, fill=GOOD)
    d.text((cx0 + 14, cy0 + ch - 26), "날림 영역 (λ<25)", font=f10, fill=BAD)
    # 정직성 주석: 보유는 필요조건일 뿐 충분조건이 아니다 (가니메데가 반례)
    for j, s in enumerate((
            "가니메데는 보유 영역인데도 대기가 없다.",
            "110 K에서는 N₂가 얼음으로 남지 못해 공급원이 없다.",
            "이 그림은 필요조건이고, 휘발성 공급은 따로 물어야 한다.")):
        d.text((cx0 + 214, cy0 + 214 + j * 15), s, font=f9, fill=(176, 184, 200))

    for name, R_km, rho, T, atm in MOONS:
        L = lam(mass(R_km, rho), R_km * 1e3, T)
        x1, y1 = px(T, R_km)
        col = GOOD if atm else (176, 184, 200)
        d.ellipse([x1 - 4, y1 - 4, x1 + 4, y1 + 4], fill=col)
        dx, dy = {"Ganymede": (-34, 16), "Charon": (-96, -6),
                  "Titan": (-88, -18), "Pluto": (-84, 6),
                  "Triton": (-88, -8)}.get(name, (8, -7))
        d.text((x1 + dx, y1 + dy), f"{name} λ{L:.0f}", font=f9, fill=col)
    for name, R_km, rho, T, atm, col in CAND:
        L = lam(mass(R_km, rho), R_km * 1e3, T)
        x1, y1 = px(T, R_km)
        d.rectangle([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=col)
        a, b = name.split("\n")
        ox, oy = (10, 6) if a.startswith("Pluto-class") else (10, -13)
        d.text((x1 + ox, y1 + oy), f"{a} λ{L:.0f}", font=f10, fill=col)
        d.text((x1 + ox, y1 + oy + 14), b, font=f9, fill=col)

    # ---- verdict box
    vy = by + 62
    d.rectangle([30, vy, 1080, vy + 132], outline=LINE)
    d.text((48, vy + 12), "판정", font=f13, fill=INK)
    lines = [
        ("Proxima c I 652 km / 45 K → λ 3.6. 대기 없는 카론(λ 11)보다도 한참 아래라 대기가 성립하지 않는다.", BAD),
        ("같은 45 K에서 N₂를 붙잡으려면 반지름 1,160 km 이상, 즉 명왕성 크기(지름 2,500 km)가 필요하다.", WARM),
        ("그런데 4 R_c 궤도는 동기궤도 5.3 R_c 안쪽이라, 크기와 무관하게 조석이 위성을 감아들인다.", WARM),
        ("eps Eri b는 세 조건이 한꺼번에 맞는다. 목성급 모행성, 3.53 AU에서 위성 온도 약 100 K(타이탄 94 K),", GOOD),
        ("동기궤도는 1.8 R_p라 한참 안쪽. 타이탄을 그대로 옮겨 놓은 구도이므로 여기가 제자리다.", GOOD),
    ]
    for i, (s, c) in enumerate(lines):
        d.text((48, vy + 38 + i * 18), s, font=f11, fill=c)

    img.save(out)
    print("wrote", out)
    print("\n-- lambda(N2) --")
    for name, R_km, rho, T, atm in MOONS:
        print(f"  {name:10s} R={R_km:5d} T={T:3d}  lambda={lam(mass(R_km,rho),R_km*1e3,T):6.1f}"
              f"  atm={'yes' if atm else 'no'}")
    for name, R_km, rho, T, atm, _ in CAND:
        print(f"  {name.replace(chr(10),' '):30s} R={R_km:5d} T={T:3d}  "
              f"lambda={lam(mass(R_km,rho),R_km*1e3,T):6.1f}")
    print("\n-- synchronous orbit --")
    for lbl, Rp, Prot, Mp, _, moons in SYSTEMS:
        rs = sync_radius(Mp, Prot, Rp)
        for mn, a_rp, _, _ in moons:
            print(f"  {lbl:34s} sync={rs:5.2f} R_p, moon at {a_rp:5.2f} "
                  f"-> {'INWARD DECAY' if a_rp < rs else 'outward, stable'}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "docs/img/moon-atmosphere-feasibility.png")
