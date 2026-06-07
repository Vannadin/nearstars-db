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

Two orbital entries:
  [0] OBSERVED (Beichman, recommended:false) — a~1.6 AU, e~0.4, mutual incl
      ~50deg. This favored family is dynamically UNSTABLE (eccentric Kozai-Lidov
      pumps e->~1 within a few kyr; REBOUND/TRACE), so it is not recommended.
  [1] NEARSTARS stability-selected (recommended:true) — a=1.6 AU (=observed),
      e=0.1, mutual incl ~16deg = the MEDIAN of the HZ-stable range (e 0-0.22,
      i 0-33deg) from a TRACE scan. HZ-stable over 1e5 yr and hosts a Hill-stable
      Pandora-class moon. This is Avatar's 'Polyphemus' — the Saturn-class gas
      giant in alpha Cen A's habitable zone whose moon Pandora is the Na'vi
      homeworld (Beichman 2025 / NPR 2025 / 'Seeking the Worlds of Avatar'
      Astrobiology 2025). The canon 1.2 AU is unusable (secular resonance pumps
      e->0.64), so 1.6 AU is the nearest robust HZ orbit.
inclination_deg is left unset on both (the constrained quantity is mutual
inclination to the AB plane, a different frame; kept in prose). a/P are
Kepler-consistent with M_A ~ 1.10 M_sun. Papers cached at
docs/phase3/_papers/2508.03814.md and 2508.03812.md.
"""

import json
import sys

sys.path.insert(0, "scripts/pipeline")
import schema  # noqa: E402

pc = json.load(open("db/planets_curated.json"))

ORB_REF_OBS = (
    "OBSERVED (Beichman et al. 2025, arXiv:2508.03814 'Worlds Next Door I' + "
    "Sanghi & Beichman, arXiv:2508.03812 'II') — JWST/MIRI 15.5um direct-imaging "
    "candidate 'S1', sep 1.5\" (~2 AU), Aug 2024, not recovered Feb/Apr 2025. "
    "Stable orbit families P=2-3 yr, e~0.4, mutual inclination ~50deg (prograde) "
    "/ ~130deg (retrograde) wrt alpha Cen AB plane; authors favor a<2 AU "
    "(a~1.6 AU). recommended:false — this favored orbit is DYNAMICALLY UNSTABLE: "
    "eccentric Kozai-Lidov at i_mut~50deg pumps e->~1 within a few kyr "
    "(REBOUND/TRACE; see Phase 3 Canonical alternatives + "
    "phase3/stability-sim/STABILITY_REPORT.md). Possibly the counterpart of "
    "VLT/NEAR C1 (Wagner et al. 2021)."
)
ORB_REF_NS = (
    "NEARSTARS stability-selected orbit (recommended). The observed favored "
    "family is Kozai-unstable, so NearStars adopts the median of the HZ-stable "
    "range from a TRACE eccentricity/inclination scan: a=1.6 AU (= observed), "
    "e=0.1 (HZ-stable range 0-0.22), mutual inclination ~16deg (range 0-33deg). "
    "Verified HZ-stable over 1e5 yr (e_max 0.15, orbit stays 1.37-1.84 AU within "
    "alpha Cen A's HZ) and hosts a Hill-stable Pandora-class moon. This is the "
    "real-life 'Polyphemus' of Avatar (Saturn-class gas giant in alpha Cen A's "
    "habitable zone; cf. Beichman 2025 / NPR 2025 / 'Seeking the Worlds of "
    "Avatar', Astrobiology 2025). a/e set here; the mutual inclination is "
    "documented in prose (cfg-frame inclination is an open item)."
)
PHY_REF = (
    "Beichman et al. 2025 / Sanghi & Beichman et al. 2025 — photometric + orbit-"
    "constrained mass 90-150 M_earth (Saturn-class), radius ~1-1.1 R_Jup "
    "(~11.2-12.3 R_earth), T ~ 225 K, consistent with RV upper limits "
    "(Zhao et al. 2018). Single-roll detection; planet candidate, unconfirmed. "
    "Matches Avatar's Polyphemus ('slightly smaller and denser than Jupiter')."
)

entry = {
    "pl_name": "Alpha Centauri A b",
    "orbital": [
        {
            "period_days": 705.0,
            "semi_major_axis_au": 1.6,
            "eccentricity": 0.4,
            "method": "direct_imaging",
            "reference": ORB_REF_OBS,
            "bibcode": "2025ApJ...989L..22B",
            "doi": "10.3847/2041-8213/adf53f",
            "recommended": False,
        },
        {
            "period_days": 705.0,
            "semi_major_axis_au": 1.6,
            "eccentricity": 0.1,
            "method": "predicted",
            "reference": ORB_REF_NS,
            "bibcode": "2025ApJ...989L..22B",
            "doi": "10.3847/2041-8213/adf53f",
            "recommended": True,
        },
    ],
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
