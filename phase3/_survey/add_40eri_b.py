# 40 Eridani A b(HD 26965 b, "Vulcan")를 사용자 결정에 따라 철회 이전 실측값으로 planets_curated 에 재등재하는 일회성 스크립트
"""Re-include 40 Eridani A b per user decision (override of the default
"exclude full retractions" policy). Uses the REAL pre-retraction Ma 2018 RV
candidate values (NOT the fictional movie blue-atmosphere/rings). The
refutation (Lubin/Burrows 2024 — signal is stellar activity) is documented
in the reference note and the Phase 3 report.
"""

import json
import sys

sys.path.insert(0, "scripts/pipeline")
import schema  # noqa: E402

pc = json.load(open("db/planets_curated.json"))

REF = ("Ma et al. 2018 (Dharma Planet Survey RV); 42.2-d signal later refuted as "
       "stellar rotation/activity (Lubin & Burrows 2024). Re-included per project "
       "decision (gameplay/cultural variety: Star Trek Vulcan + PHM Erid); "
       "refutation documented in Phase 3.")

pc["40 Eridani A"] = [{
    "pl_name": "40 Eridani A b",
    "orbital": [{
        "period_days": 42.245,
        "semi_major_axis_au": 0.224,
        "eccentricity": 0.04,
        "method": "rv",
        "reference": REF,
        "recommended": True,
    }],
    "physical": [{
        "mass_mearth": 8.47,
        "mass_type": "msini",
        "method": "rv",
        "reference": "Ma et al. 2018 (Dharma Planet Survey) — m sin i; signal refuted Lubin/Burrows 2024",
        "recommended": True,
    }],
}]

schema.write_canonical("db/planets_curated.json", pc)
print("added planets_curated['40 Eridani A'] = [40 Eridani A b]  (Ma 2018 values, refuted-flagged)")
