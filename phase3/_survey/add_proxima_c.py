# Proxima Cen c (Damasso 2020 RV 후보)를 사용자 결정에 따라 candidate 로 planets_curated 에 추가하는 일회성 스크립트
"""Add Proxima Cen c as a documented RV candidate per user decision.

Proxima c was never ingested into raw (the pipeline only pulled b & d, so the
"second planet" the user read about on Namu Wiki was simply missing). It is a
candidate super-Earth / mini-Neptune:

  Damasso et al. 2020 (Sci. Adv. 6, eaax7467) — RV minimum mass
  m sin i = 5.8 +/- 1.9 M_earth, P = 5.21(+0.26/-0.22) yr (~1900 d),
  a = 1.48 +/- 0.08 AU, circular orbit assumed, T_eq ~ 39 K.

Astrometric follow-up (Kervella et al. 2020; Benedict & McArthur 2020) suggests
a true mass ~7 M_earth. Existence remains UNCONFIRMED — later analyses cast
doubt (the Namu Wiki article itself notes a 2022 study questioning it). Treated
as a documented candidate, the same pattern as tau Cet e / 40 Eri A b.

NO RINGS: the popular "Proxima c may have rings" claim rests on Gratton et al.
2020's SPHERE imaging counterpart, which was itself disputed/unconfirmed. Per the
ring-fabrication guardrail we do NOT add a rings block; the speculation is left
out of the structured DB.

Damasso 2020 has no arXiv preprint; its full text is cached manually at
docs/phase3/_papers/2020SciA_6_7467D.md (open-access via PMC6962037) so the
recommended values stay value-checkable against frozen text.
"""

import json
import sys

sys.path.insert(0, "scripts/pipeline")
import schema  # noqa: E402

pc = json.load(open("db/planets_curated.json"))

ORB_REF = (
    "Damasso et al. 2020 (Sci. Adv. 6, eaax7467) — RV candidate; "
    "P=5.21(+0.26/-0.22) yr (~1900 d), a=1.48+/-0.08 AU, circular orbit assumed. "
    "Astrometric follow-up (Kervella et al. 2020; Benedict & McArthur 2020) "
    "suggests true mass ~7 M_earth. CANDIDATE — existence unconfirmed; later "
    "analyses (e.g. 2022) cast doubt. Re-included as a documented candidate "
    "(never ingested into raw)."
)
PHY_REF = (
    "Damasso et al. 2020 — m sin i = 5.8 +/- 1.9 M_earth (RV minimum mass), "
    "T_eq ~ 39 K. Astrometric true mass ~7 M_earth (Benedict & McArthur 2020; "
    "Kervella et al. 2020)."
)

entry = {
    "pl_name": "Proxima Cen c",
    "orbital": [{
        "period_days": 1900.0,
        "uncertainty_period_days": 96.0,
        "semi_major_axis_au": 1.48,
        "uncertainty_semi_major_axis_au": 0.08,
        "eccentricity": 0.0,
        "method": "rv",
        "reference": ORB_REF,
        "bibcode": "2020SciA....6.7467D",
        "doi": "10.1126/sciadv.aax7467",
        "recommended": True,
    }],
    "physical": [{
        "mass_mearth": 5.8,
        "uncertainty_mearth": 1.9,
        "mass_type": "msini",
        "method": "rv",
        "reference": PHY_REF,
        "bibcode": "2020SciA....6.7467D",
        "doi": "10.1126/sciadv.aax7467",
        "recommended": True,
    }],
}

host = pc.setdefault("Proxima Cen", [])
host[:] = [p for p in host if p.get("pl_name") != "Proxima Cen c"]  # idempotent
host.append(entry)

schema.write_canonical("db/planets_curated.json", pc)
print("added planets_curated['Proxima Cen'] += Proxima Cen c  (Damasso 2020 candidate)")
print("  ->", [p["pl_name"] for p in pc["Proxima Cen"]])
