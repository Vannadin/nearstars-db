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




# ---------------------------------------------------------------------------
# 실제 비율 도면: 프록시마 c + 고리 + c I (모행성 크기·거리·위성 크기 동일 축척)
# ---------------------------------------------------------------------------
def scale_figure(out="docs/img/proxima-c-system-to-scale.png"):
    RC_KM = 17202.0          # c 반지름
    RING_INNER, RING_OUTER = (1.40, 1.90), (2.40, 3.00)
    ROCHE, SYNC = 3.30, 5.31
    BELT = (3.90, 6.50)
    MOON_R_KM, FLAT = 326.0, 0.0478
    ORBITS = [(4.01, "현 보드값 4.0 R_c", BAD), (7.00, "제안 7.0 R_c", GOOD)]

    W, H = 1720, 1040
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f9, f10, f11, f13 = font(11), font(12), font(13), font(15)
    d.text((30, 20), "Proxima c 계 — 실제 비율", font=font(24, True), fill=INK)
    d.text((30, 56), "모행성 크기 · 고리 · 위성 크기 · 궤도 거리를 모두 같은 축척으로 "
                     "·  c 반지름 17,202 km", font=f11, fill=DIM)

    # ---------------- A. 측면(궤도면 안에서 본) 실제 비율 ----------------
    x0, ymid, XMAX = 250, 322, 7.9
    ppu = (W - x0 - 130) / XMAX
    d.text((30, 100), "A. 궤도면 측면에서 본 모습 (실제 비율)", font=f13, fill=INK)
    # 방사선 외대
    d.rectangle([x0 + BELT[0] * ppu, ymid - 66, x0 + BELT[1] * ppu, ymid + 66],
                fill=(32, 22, 32))
    d.text((x0 + BELT[0] * ppu + 8, ymid - 86), "방사선 외대 3.9–6.5 R_c",
           font=f9, fill=(160, 116, 148))
    # 고리 두 띠 (측면이라 선)
    for lo, hi in (RING_INNER, RING_OUTER):
        d.rectangle([x0 + lo * ppu, ymid - 2, x0 + hi * ppu, ymid + 2],
                    fill=(182, 186, 196))
    d.text((x0 + RING_INNER[0] * ppu - 4, ymid + 12),
           "고리 1.4–1.9 · 2.4–3.0 R_c", font=f9, fill=(182, 186, 196))
    # Roche / 동기궤도
    for val, lbl, col in ((ROCHE, "얼음 Roche 3.3", (206, 126, 116)),
                          (SYNC, "동기궤도 5.31", WARM)):
        xv = x0 + val * ppu
        for yy in range(ymid - 108, ymid + 109, 8):
            d.line([(xv, yy), (xv, yy + 4)], fill=col)
        d.text((xv - 30, ymid - 130), lbl, font=f9, fill=col)
    # 모행성
    pr = ppu
    d.ellipse([x0 - pr, ymid - pr, x0 + pr, ymid + pr], fill=(150, 164, 176))
    d.ellipse([x0 - pr, ymid - pr, x0 + pr, ymid + pr], outline=(196, 208, 220))
    d.text((x0 - 34, ymid + pr + 14), "Proxima c", font=f11, fill=INK)
    d.text((x0 - 34, ymid + pr + 30), "지름 34,404 km", font=f9, fill=DIM)
    # 위성 (실제 비율)
    for a_rc, lbl, col in ORBITS:
        xm = x0 + a_rc * ppu
        rm = MOON_R_KM / RC_KM * ppu
        d.ellipse([xm - rm, ymid - rm, xm + rm, ymid + rm], fill=col)
        d.line([(xm, ymid - 34), (xm, ymid - rm - 3)], fill=col)
        d.text((xm - 44, ymid - 52), lbl, font=f10, fill=col)
        d.text((xm - 44, ymid + 26), f"{a_rc * RC_KM:,.0f} km".replace(",", " "),
               font=f9, fill=col)
    # 축척 바
    barkm = 20000
    bl = barkm / RC_KM * ppu
    bx_, by_ = x0 + 3.9 * ppu, ymid + pr + 22
    d.line([(bx_, by_), (bx_ + bl, by_)], fill=INK, width=2)
    for xx in (bx_, bx_ + bl):
        d.line([(xx, by_ - 5), (xx, by_ + 5)], fill=INK)
    d.text((bx_ + bl / 2 - 30, by_ + 9), "20 000 km", font=f9, fill=INK)

    # ---------------- B. c I 확대 ----------------
    MAG = 25
    d.text((30, 622), f"B. c I 확대 (A 도면의 {MAG}배) — 조석으로 늘어난 계란형",
           font=f13, fill=INK)
    rm_b = MOON_R_KM / RC_KM * ppu * MAG
    bx, by2 = 170, 790
    d.ellipse([bx - rm_b, by2 - rm_b * (1 - FLAT), bx + rm_b, by2 + rm_b * (1 - FLAT)],
              fill=(178, 152, 142), outline=(214, 194, 184))
    d.text((bx - 50, by2 + rm_b + 18), "Proxima c I", font=f11, fill=INK)
    d.text((bx - 50, by2 + rm_b + 34), "지름 652 km · a/c 1.05", font=f9, fill=DIM)
    tx = bx + rm_b + 46
    for j, s in enumerate((
            f"같은 {MAG}배로 모행성을 그리면 지름이 {2*ppu*MAG:,.0f} px, 화면 밖이다.",
            "A 도면의 위성 점 크기가 실제 비율이다 — 반지름이 c의 1/53.",
            "행성 원반 안에 c I을 53개 늘어놓을 수 있다.",
            "편평도 4.8%는 실제로 이 정도로 미묘하다. 계란형이라 해도 눈에 겨우 걸린다.")):
        d.text((tx, by2 - 30 + j * 20), s.replace(",", " "), font=f10, fill=DIM)

    # ---------------- C. c I 하늘에서 본 c ----------------
    d.text((980, 622), "C. c I 하늘에서 본 c의 겉보기 크기", font=f13, fill=INK)
    cy = 790
    dpp = 6.4
    xx = 1120
    for a_rc, col in ((4.01, BAD), (7.00, GOOD)):
        ang = 2 * math.degrees(math.asin(1 / a_rc))
        r = ang / 2 * dpp
        d.line([(xx - r * 2.2, cy), (xx + r * 2.2, cy)], fill=(198, 202, 212))
        d.ellipse([xx - r, cy - r, xx + r, cy + r], fill=(150, 164, 176))
        d.ellipse([xx - r, cy - r, xx + r, cy + r], outline=col)
        d.text((xx - 52, cy + r + 16), f"{a_rc:.1f} R_c 에서 {ang:.1f}°",
               font=f10, fill=col)
        xx += 250
    mr = 0.52 / 2 * dpp
    d.ellipse([1600 - mr, cy - mr, 1600 + mr, cy + mr], fill=(216, 216, 216))
    d.text((1556, cy + 14), "지구에서 본 달 0.52°", font=f9, fill=DIM)
    d.text((980, 946), "고리는 c I이 적도면을 돌기 때문에 정확히 측면으로 보인다. "
                       "원반이 아니라 밝은 한 줄이다.", font=f10, fill=DIM)

    img.save(out)
    print("wrote", out)
    print(f"  c I / c 반지름비 = {MOON_R_KM / RC_KM:.4f} (1/{RC_KM / MOON_R_KM:.0f})")
    for a_rc, _, _ in ORBITS:
        print(f"  a={a_rc:.2f} R_c = {a_rc*RC_KM:,.0f} km, "
              f"c 겉보기 지름 {2*math.degrees(math.asin(1/a_rc)):.1f} deg")



# ---------------------------------------------------------------------------
# 벨트 안쪽 경계 vs 바깥쪽 경계 배치 비교 (c 자전이 동기궤도를 어디로 옮기는지 포함)
# ---------------------------------------------------------------------------
def edge_compare(out="docs/img/proxima-c-i-orbit-edge-compare.png"):
    G_ = 6.674e-11
    RC_KM = 17202.0
    MC = 8 * 5.972e24
    MOON_R_KM = 326.0
    RHO = 1.6e3
    BELT = ((1.54 + 1.42) / math.sqrt(0.66), (2.8 + 2.5) / math.sqrt(0.66))
    RING = ((1.40, 1.90), (2.40, 3.00))
    ROCHE = 3.30

    def sync_rc(P_h):
        return (G_ * MC * (P_h * 3600 / (2 * math.pi)) ** 2) ** (1 / 3) / (RC_KM * 1e3)

    def figure(a_rc):
        a = a_rc * RC_KM * 1e3
        n = math.sqrt(G_ * MC / a ** 3)
        qs = n * n / (G_ * RHO * 4 * math.pi / 3)
        J2 = 0.88 * qs
        return (2 * math.pi / n / 3600, J2, 2.5 * J2,
                2 * math.degrees(math.asin(1 / a_rc)))

    CASES = [
        ("안쪽 경계  3.75 R_c", 3.75, 16.0, GOOD, "c 자전 16 h — 해왕성 16.1 · 천왕성 17.2"),
        ("바깥쪽 경계  6.4 R_c", 6.40, 27.0, ACC, "c 자전 27 h — 기존 보드값"),
    ]

    W, H = 1700, 1050
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f9, f10, f11, f13 = font(11), font(12), font(13), font(15)
    d.text((30, 20), "c I 궤도 — 벨트 안쪽 경계 vs 바깥쪽 경계", font=font(24, True), fill=INK)
    d.text((30, 56), "동기궤도(주황)는 c의 자전이 정한다. 위성이 그 안쪽이면 감겨 들어가고 "
                     "바깥이면 물러난다.  ·  모행성·위성·거리는 실제 비율", font=f11, fill=DIM)

    x0, XMAX = 250, 7.6
    ppu = 900 / XMAX
    for k, (title, a_rc, prot, col, sub) in enumerate(CASES):
        y = 300 + k * 350
        P_h, J2, flat, ang = figure(a_rc)
        rs = sync_rc(prot)
        inside = a_rc < rs
        d.text((30, y - 152), title, font=font(17, True), fill=col)
        d.text((30, y - 130), sub, font=f9, fill=DIM)
        d.rectangle([x0 + BELT[0] * ppu, y - 50, x0 + BELT[1] * ppu, y + 50],
                    fill=(34, 24, 34))
        d.text((x0 + BELT[0] * ppu + 6, y - 70),
               f"방사선 외대 {BELT[0]:.2f}–{BELT[1]:.2f} R_c", font=f9, fill=(162, 118, 150))
        for lo, hi in RING:
            d.rectangle([x0 + lo * ppu, y - 2, x0 + hi * ppu, y + 2], fill=(182, 186, 196))
        xv = x0 + ROCHE * ppu
        for yy in range(y - 76, y + 77, 8):
            d.line([(xv, yy), (xv, yy + 4)], fill=(206, 126, 116))
        d.text((xv - 96, y + 84), "얼음 Roche 3.3", font=f9, fill=(206, 126, 116))
        xs = x0 + rs * ppu
        for yy in range(y - 96, y + 97, 8):
            d.line([(xs, yy), (xs, yy + 4)], fill=WARM)
        d.text((xs - 36, y - 118), f"동기궤도 {rs:.2f}", font=f10, fill=WARM)
        pr = ppu
        d.ellipse([x0 - pr, y - pr, x0 + pr, y + pr], fill=(150, 164, 176))
        d.ellipse([x0 - pr, y - pr, x0 + pr, y + pr], outline=(196, 208, 220))
        xm = x0 + a_rc * ppu
        rm = MOON_R_KM / RC_KM * ppu
        d.ellipse([xm - rm, y - rm, xm + rm, y + rm], fill=col)
        d.text((xm - 30, y - 96), f"c I  {a_rc} R_c", font=f10, fill=col)
        d.line([(xm, y - 82), (xm, y - rm - 3)], fill=col)
        arrow = "◀ 안쪽으로 감김" if inside else "바깥으로 물러남 ▶"
        d.text((xm - (72 if inside else 16), y + 14), arrow, font=f10,
               fill=BAD if inside else GOOD)
        # 위성 확대 (편평도 차이가 이 결정의 시각적 핵심)
        MAG = 22
        rb = MOON_R_KM / RC_KM * ppu * MAG
        bx2, by3 = xm, y + 108
        d.ellipse([bx2 - rb, by3 - rb * (1 - flat), bx2 + rb, by3 + rb * (1 - flat)],
                  fill=(178, 152, 142), outline=col)
        d.text((bx2 - 52, by3 + rb + 8), f"c I ×{MAG}  편평도 {flat*100:.2f}%",
               font=f9, fill=col)
        # 오른쪽 요약표
        tx = x0 + XMAX * ppu + 46
        rows = [
            ("공전 · 자전", f"{P_h:.1f} h"),
            ("하늘의 c", f"{ang:.1f}°  (달 0.52°의 {ang/0.52:.0f}배)"),
            ("편평도", f"{flat*100:.2f}%  " +
                      ("가시 계란형 · 메쉬 emit" if flat > 0.02 else "비가시 · 중력만")),
            ("벨트", "안쪽 테두리를 안음" if a_rc < 4.5 else "바깥 테두리를 스침"),
            ("조석 운명", "수억 년 내 고리로 낙하" if inside else "안정 (바깥으로 이동)"),
        ]
        for jj, (kk, vv) in enumerate(rows):
            yy = y - 62 + jj * 27
            d.text((tx, yy), kk, font=f9, fill=DIM)
            d.text((tx + 86, yy), vv, font=f11,
                   fill=BAD if (kk == "조석 운명" and inside) else INK)

    vy = 858
    d.rectangle([30, vy, W - 30, vy + 136], outline=LINE)
    d.text((48, vy + 12), "차이 요약", font=f13, fill=INK)
    for jj, (s, c) in enumerate((
            ("안쪽 경계로 가려면 c의 자전을 27 h에서 16 h로 낮춰야 한다. 동기궤도가 5.31에서 3.77 R_c로 내려와 위성이 그 바깥에 놓인다.", GOOD),
            ("27 h는 보드에 미구속 자유자전·오너 art 선택으로 적힌 임의값이고, 실측 빙거성은 천왕성 17.2 h · 해왕성 16.1 h로 원래 빠르다.", GOOD),
            ("안쪽이 얻는 것: 편평도 5.84%로 계란형 부활, 하늘의 c가 30.9°, 공전 16 h가 c 자전과 같아 하늘 한자리에 붙박인 것처럼 보인다.", INK),
            ("안쪽이 치르는 것: 동기궤도 3.77과 궤도 3.75가 거의 붙어 조석 이동이 사실상 0이다. 마진을 원하면 c 자전 15 h + 위성 3.7 R_c.", WARM),
    )):
        d.text((48, vy + 40 + jj * 21), s, font=f11, fill=c)

    img.save(out)
    print("wrote", out)
    for title, a_rc, prot, _, _ in CASES:
        P_h, J2, flat, ang = figure(a_rc)
        rs = sync_rc(prot)
        print(f"  {title}: sync={rs:.2f}  P={P_h:.2f} h  flat={flat*100:.2f}%  "
              f"ang={ang:.1f} deg  {'INSIDE' if a_rc < rs else 'outside'}")


if __name__ == "__main__":
    if "--edge" in sys.argv:
        edge_compare()
    elif "--scale" in sys.argv:
        scale_figure()
    elif "--all" in sys.argv:
        main()
        scale_figure()
        edge_compare()
    else:
        main(sys.argv[1] if len(sys.argv) > 1 else
             "docs/img/moon-atmosphere-feasibility.png")
