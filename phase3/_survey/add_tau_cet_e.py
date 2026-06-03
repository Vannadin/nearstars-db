# tau Cet e(Adrian, PHM)를 사용자 결정에 따라 Feng 2017 값으로 planets_curated 에 재등재하는 일회성 스크립트
"""Re-include tau Cet e per user decision (parallel to 40 Eri A b). Feng 2017
RV values; signal reclassified False Positive (NEA 2026-04-09, Figueira 2025).
Disposition documented in Phase 3 (docs/phase3/tau-cet-e.md). PHM cultural
weight: tau Cet e = "Adrian".
"""

import json
import sys

sys.path.insert(0, "scripts/pipeline")
import schema  # noqa: E402

pc = json.load(open("db/planets_curated.json"))

REF = ("Feng et al. 2017 RV; signal reclassified False Positive (NEA 2026-04-09, "
       "Figueira 2025 ESPRESSO non-detection — stellar activity). Re-included per "
       "project decision (PHM Adrian cultural weight); disposition documented in Phase 3.")

e = {
    "pl_name": "tau Cet e",
    "orbital": [{
        "period_days": 162.87,
        "semi_major_axis_au": 0.538,
        "eccentricity": 0.18,
        "method": "rv",
        "reference": REF,
        "recommended": True,
    }],
    "physical": [{
        "mass_mearth": 3.93,
        "mass_type": "msini",
        "method": "rv",
        "reference": "Feng et al. 2017 — m sin i; signal refuted (Figueira 2025)",
        "recommended": True,
    }],
}

lst = pc.get("tau Cet", [])
if not any(p["pl_name"] == "tau Cet e" for p in lst):
    lst.insert(0, e)            # letter order: e before f/g/h
pc["tau Cet"] = lst

schema.write_canonical("db/planets_curated.json", pc)
print("planets_curated['tau Cet'] =", [p["pl_name"] for p in pc["tau Cet"]])
