# Alpha Centauri A b (JWST/MIRI 2025 직접촬영 후보 "S1")를 사용자 결정에 따라 candidate 로 planets_curated 에 추가하는 일회성 스크립트
"""Add Alpha Centauri A b (candidate "S1") per user decision.

alpha Cen A had no planet entry. In Aug 2024 JWST/MIRI (F1550C, 15.5um) imaged a
point source "S1" in the habitable zone:

  Beichman et al. 2025  (arXiv:2508.03814 = 2025ApJ...989L..22B, "Worlds Next Door I")
  Sanghi & Beichman et al. 2025 (arXiv:2508.03812 = 2025ApJ...989L..23S, "II")

  S1: sep 1.5" (~2 AU) E of alpha Cen A, F(15.5um)=3.5+/-1.0 mJy, contrast 5.5e-5,
  S/N 4-6; detected Aug 2024, NOT recovered Feb/Apr 2025 (52% chance of being
  missed due to orbital motion if S1 == VLT/NEAR candidate C1, Wagner 2021).
  Dynamically stable orbit families: P = 2-3 yr, e ~ 0.4, mutual inclination
  ~50deg (prograde) / ~130deg (retrograde) wrt the alpha Cen AB plane.
  Inferred: T ~ 225 K, radius ~1-1.1 R_Jup, mass 90-150 M_earth (Saturn-class),
  consistent with RV upper limits (Zhao et al. 2018).

CANDIDATE — a single-roll detection; the authors explicitly call it a planet
candidate that "would be alpha Cen Ab" only if confirmed. Recorded with that
status in the reference note (same documented-candidate pattern as Proxima c).

Representative orbital values used: P = 2.5 yr (912 d), a ~ 1.9 AU (Kepler-
consistent with P and M_A = 1.0788 M_sun), e = 0.4. Line-of-sight inclination is
NOT the quoted mutual inclination, so inclination_deg is omitted (mutual value
kept in prose only). Both papers are cached at docs/phase3/_papers/2508.03814.md
and 2508.03812.md.
"""

import json
import sys

sys.path.insert(0, "scripts/pipeline")
import schema  # noqa: E402

pc = json.load(open("db/planets_curated.json"))

ORB_REF = (
    "Beichman et al. 2025 (arXiv:2508.03814, 'Worlds Next Door I') + Sanghi & "
    "Beichman et al. 2025 (arXiv:2508.03812, 'II') — JWST/MIRI 15.5um direct-"
    "imaging candidate 'S1', sep 1.5\" (~2 AU), detected Aug 2024, not recovered "
    "Feb/Apr 2025. Dynamically stable orbit families P=2-3 yr, e~0.4, mutual "
    "inclination ~50deg (prograde) or ~130deg (retrograde) wrt alpha Cen AB "
    "plane; representative P=2.5 yr / a~1.9 AU used here. CANDIDATE — would be "
    "'alpha Cen Ab' if confirmed; possibly the counterpart of VLT/NEAR C1 "
    "(Wagner et al. 2021)."
)
PHY_REF = (
    "Beichman et al. 2025 / Sanghi & Beichman et al. 2025 — photometric + orbit-"
    "constrained mass 90-150 M_earth (Saturn-class), radius ~1-1.1 R_Jup "
    "(~11.2-12.3 R_earth), T ~ 225 K, consistent with RV upper limits "
    "(Zhao et al. 2018). Single-roll detection; planet candidate, unconfirmed."
)

entry = {
    "pl_name": "Alpha Centauri A b",
    "orbital": [{
        "period_days": 912.0,
        "semi_major_axis_au": 1.9,
        "eccentricity": 0.4,
        "method": "direct_imaging",
        "reference": ORB_REF,
        "bibcode": "2025ApJ...989L..22B",
        "doi": "10.3847/2041-8213/adf53f",
        "recommended": True,
    }],
    "physical": [{
        "mass_mearth": 120.0,
        "mass_type": "imaging_photometric_estimate",
        "radius_rearth": 11.8,
        "method": "direct_imaging",
        "reference": PHY_REF,
        "bibcode": "2025ApJ...989L..22B",
        "doi": "10.3847/2041-8213/adf53f",
        "recommended": True,
    }],
}

pc["Alpha Centauri A"] = [
    p for p in pc.get("Alpha Centauri A", [])
    if p.get("pl_name") != "Alpha Centauri A b"
] + [entry]  # idempotent

schema.write_canonical("db/planets_curated.json", pc)
print("added planets_curated['Alpha Centauri A'] = [Alpha Centauri A b]  (Beichman/Sanghi 2025 candidate)")
print("  ->", [p["pl_name"] for p in pc["Alpha Centauri A"]])
