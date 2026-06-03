# beyond-50ly 두 타깃(V1400 Cen, PSR J0108-1431)을 target_list/stellar_props/planets curated 에 surgical 병합하는 일회성 큐레이션 스크립트
"""Curated-layer insertion for the two beyond-50ly targets, via
schema.write_canonical (sanctioned by the curation data contract; surgical —
only the new keys/entries are added, existing entries untouched).

Values trace to the Phase 2 dossiers under phase3/_survey/.
"""

import json
import sys

sys.path.insert(0, "scripts/pipeline")
import schema  # noqa: E402

MAMAJEK = "2012AJ....143...72M"
KM2015 = "2015ApJ...800..126K"
DELLER = "2009ApJ...701.1243D"
PAVLOV = "2009ApJ...691..458P"

# ── target_list.json ──
tl = json.load(open("db/target_list.json"))
existing = {e["system"] for e in tl}
for sysname, comp, gaia in [
    ("V1400 Centauri", "V1400 Centauri", ["6117085769513415168"]),
    ("PSR J0108-1431", "PSR J0108-1431", []),
]:
    if sysname not in existing:
        tl.append({
            "system": sysname,
            "components": [comp],
            "gaia_source_ids": gaia,
            "hip_ids": [],
            "binary": False,
        })
schema.write_canonical("db/target_list.json", tl)

# ── stellar_props_curated.json ──
sp = json.load(open("db/stellar_props_curated.json"))

sp["V1400 Centauri"] = {
    "spectype": "K5 IV(e) Li",
    "spectype_reference": "Mamajek et al. 2012",
    "teff_k": 4500,
    "mass_measurements": [{
        "value_msun": 0.9, "method": "evolutionary_model",
        "reference": "Mamajek et al. 2012", "bibcode": MAMAJEK, "recommended": True,
    }],
    "radius_measurements": [{
        "value_rsun": 0.99, "uncertainty_rsun": 0.11, "method": "evolutionary_model",
        "reference": "Kenworthy & Mamajek 2015", "bibcode": KM2015, "recommended": True,
    }],
    "teff_measurements": [{
        "value_k": 4500, "uncertainty_k": 200, "method": "low_res_spectroscopy",
        "reference": "Mamajek et al. 2012", "bibcode": MAMAJEK, "recommended": True,
    }],
    "age_measurements": [{
        "value_gyr": 0.016, "method": "isochrone",
        "reference": "Mamajek et al. 2012 (Sco-Cen UCL membership)", "bibcode": MAMAJEK,
        "recommended": True,
    }],
    "rotation_measurements": [{
        "value_days": 3.20, "method": "photometric_variability",
        "reference": "Mamajek et al. 2012", "bibcode": MAMAJEK, "recommended": True,
    }],
    "activity_measurements": [{
        "value_x_ray_log_lx_lbol": -3.4, "method": "x_ray",
        "reference": "Mamajek et al. 2012 (near-saturation, fast rotator)", "bibcode": MAMAJEK,
        "recommended": True,
    }],
    "meta_notes": (
        "Young (~16 Myr) pre-main-sequence K5 member of Upper Centaurus-Lupus "
        "(Sco-Cen). Gaia DR3 distance 138.2 pc (~451 ly) — far beyond the 50 ly "
        "Kopernicus cap; added as a beyond-implementation-range data / Phase-3 "
        "entry (intentional exception), NOT a KSP target body. Host of J1407b, "
        "the largest known (candidate) ring system. Teff uncertainty asymmetric "
        "(+100/-200 K); post-Gaia isochrone analyses favor a slightly older "
        "~20 Myr age and Teff ~4343 K."
    ),
}

sp["PSR J0108-1431"] = {
    "spectype": "neutron star (radio pulsar)",
    "spectype_reference": "Tauris et al. 1994",
    "mass_measurements": [{
        "value_msun": 1.4, "method": "assumed_canonical",
        "reference": "canonical neutron-star mass (not measured)", "recommended": True,
    }],
    "radius_measurements": [{
        "value_rsun": 1.724e-5, "method": "assumed_canonical",
        "reference": "canonical neutron-star radius ~12 km (not measured)", "recommended": True,
    }],
    "compact_object": {
        "object_type": "neutron_star",
        "subclass": "rotation_powered_radio_pulsar",
        "spin_period_s": 0.8075646822,
        "spin_period_derivative": 7.7e-17,
        "characteristic_age_myr": 168,
        "surface_b_field_gauss": 2.5e11,
        "spin_down_luminosity_erg_s": 5.8e30,
        "xray_kt_kev": 0.11,
        "xray_luminosity_erg_s": 2.0e28,
        "reference": "Pavlov et al. 2009; Posselt et al. 2012",
        "bibcode": PAVLOV,
        "notes": (
            "Distance disputed: raw VLBI parallax 4.17 mas -> 240 pc (Deller 2009), "
            "Lutz-Kelker-corrected best ~210 pc (Verbiest 2012); legacy DM ~130 pc "
            "superseded. Pdot/tau/B from Pavlov 2009 (ATNF timing differs ~2x). X-ray "
            "kT: XMM 0.11 keV (Posselt 2012) vs Chandra 0.28 keV (Pavlov 2009). M/R "
            "canonical, not measured."
        ),
    },
    "meta_notes": (
        "Nearest known radio pulsar (Cetus), ~210-240 pc (~685 ly) — far beyond the "
        "50 ly Kopernicus cap; beyond-implementation-range data / Phase-3 entry "
        "(intentional exception), NOT a KSP target. Ordinary (non-recycled), old "
        "(~168 Myr characteristic age), faint, near the radio death line. Astrometry "
        "from VLBI (Deller et al. 2009), not Gaia — optically far below Gaia's limit. "
        "Solitary: no planets (IR companion search to ~5000 AU, Posselt 2008/09)."
    ),
}
schema.write_canonical("db/stellar_props_curated.json", sp)

# ── planets_curated.json (J1407b + circumplanetary rings) ──
pc = json.load(open("db/planets_curated.json"))
pc["V1400 Centauri"] = [{
    "pl_name": "J1407b",
    "orbital": [{
        "semi_major_axis_au": 5.0, "eccentricity": 0.7,
        "method": "theoretical",
        "reference": "Kenworthy & Mamajek 2015 (ring-eclipse model; period ~13-17 yr unconfirmed)",
        "bibcode": KM2015, "recommended": True,
    }],
    "physical": [{
        "mass_mearth": 7627, "mass_type": "ring_model_estimate",
        "method": "theoretical",
        "reference": "Kenworthy & Mamajek 2015 (~24 M_Jup photometric; range 8->100 M_Jup)",
        "bibcode": KM2015, "recommended": True,
    }],
    "rings": {
        "outer_radius_au": 0.6,
        "ring_count": 37,
        "total_mass_mearth": 1.0,
        "gap_radius_au": 0.4,
        "inclination_deg": 70.0,
        "orientation_deg": 166.1,
        "prograde": False,
        "eclipse_duration_days": 56,
        "exomoon_mass_mearth_upper": 0.8,
        "method": "eclipse_modeling",
        "reference": "Kenworthy & Mamajek 2015",
        "bibcode": KM2015,
        "notes": (
            "TENTATIVE / DISPUTED. The 2007 eclipse light curve is real data; the "
            "ring system is the best-fit MODEL of that single, never-repeated event. "
            "Companion's bound orbit unconfirmed (Mentel 2018: no second eclipse in "
            "plates 1890-2018). Mass spans 8-100 M_Jup (photometric ~24 vs ring-"
            "stability dynamics 60-100, Rieder & Kenworthy 2016). Retrograde favored. "
            "Outer radius ~90 million km, ~200x Saturn's rings; gap at ~0.4 AU "
            "attributed to an exomoon (<0.8 M_earth)."
        ),
    },
}]
schema.write_canonical("db/planets_curated.json", pc)

print("curated: target_list (+2), stellar_props (+V1400 Cen, +PSR J0108), planets (+J1407b w/ rings)")
