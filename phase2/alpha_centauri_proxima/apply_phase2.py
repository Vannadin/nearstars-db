# Alpha Cen A/B + Proxima Cen Phase 2 측정값을 stellar_props_curated.json/planets_curated.json에 적용
"""Alpha Cen A, Alpha Cen B, Proxima Cen + Proxima 행성 2개의 Phase 2 측정값 array 적용.

각 별별로 mass / radius / teff / luminosity / age / metallicity / rotation /
activity 8개 카테고리를 paper-attributed array 로 확장.
Proxima 행성은 orbital + physical 을 dict 에서 array 로 확장.

실행:
    python3 phase2/alpha_centauri_proxima/apply_phase2.py
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STELLAR_CURATED = os.path.join(BASE, "db", "stellar_props_curated.json")
PLANETS_CURATED = os.path.join(BASE, "db", "planets_curated.json")


# ── Alpha Centauri A ────────────────────────────────────────────────────────

ALPHA_A = {
    "teff_k": 5790,
    "spectype": "G2 V",
    "mass_measurements": [
        {
            "value_msun": 1.1055,
            "uncertainty_msun": 0.0039,
            "method": "binary_orbit",
            "reference": "Pourbaix & Boffin 2016",
            "bibcode": "2016A&A...586A..90P",
            "doi": "10.1051/0004-6361/201527859",
            "recommended": True,
        },
        {
            "value_msun": 1.133,
            "uncertainty_msun": 0.005,
            "method": "binary_orbit",
            "reference": "Kervella et al. 2016",
            "bibcode": "2016A&A...594A.107K",
            "doi": "10.1051/0004-6361/201629201",
            "recommended": False,
        },
        {
            "value_msun": 1.105,
            "uncertainty_msun": 0.007,
            "method": "evolutionary_model",
            "reference": "Joyce & Chaboyer 2018",
            "bibcode": "2018ApJ...864...99J",
            "doi": "10.3847/1538-4357/aad464",
            "recommended": False,
        },
        {
            "value_msun": 1.105,
            "uncertainty_msun": 0.007,
            "method": "asteroseismology",
            "reference": "Bazot et al. 2007",
            "bibcode": "2007A&A...470..295B",
            "doi": "10.1051/0004-6361:20065694",
            "recommended": False,
        },
    ],
    "radius_measurements": [
        {
            "value_rsun": 1.2234,
            "uncertainty_rsun": 0.0053,
            "method": "interferometry",
            "reference": "Kervella et al. 2017",
            "bibcode": "2017A&A...597A.137K",
            "doi": "10.1051/0004-6361/201629505",
            "recommended": True,
        },
        {
            "value_rsun": 1.224,
            "uncertainty_rsun": 0.003,
            "method": "interferometry",
            "reference": "Kervella et al. 2003",
            "bibcode": "2003A&A...404.1087K",
            "doi": "10.1051/0004-6361:20030570",
            "recommended": False,
        },
        {
            "value_rsun": 1.224,
            "uncertainty_rsun": 0.003,
            "method": "evolutionary_model",
            "reference": "Bazot et al. 2007",
            "bibcode": "2007A&A...470..295B",
            "doi": "10.1051/0004-6361:20065694",
            "recommended": False,
        },
    ],
    "teff_measurements": [
        {
            "value_k": 5847,
            "uncertainty_k": 27,
            "method": "high_res_spectroscopy",
            "reference": "Porto de Mello et al. 2008",
            "bibcode": "2008A&A...488..653P",
            "doi": "10.1051/0004-6361:200810031",
            "recommended": True,
        },
        {
            "value_k": 5792,
            "uncertainty_k": 16,
            "method": "sed_fitting",
            "reference": "Heiter et al. 2015",
            "bibcode": "2015A&A...582A..49H",
            "doi": "10.1051/0004-6361/201526319",
            "recommended": False,
        },
        {
            "value_k": 5810,
            "uncertainty_k": 50,
            "method": "high_res_spectroscopy",
            "reference": "Bazot et al. 2007",
            "bibcode": "2007A&A...470..295B",
            "doi": "10.1051/0004-6361:20065694",
            "recommended": False,
        },
    ],
    "luminosity_measurements": [
        {
            "value_lsun": 1.521,
            "uncertainty_lsun": 0.013,
            "method": "bolometric_flux",
            "reference": "Kervella et al. 2017",
            "bibcode": "2017A&A...597A.137K",
            "doi": "10.1051/0004-6361/201629505",
            "recommended": True,
        },
    ],
    "age_measurements": [
        {
            "value_gyr": 4.81,
            "uncertainty_gyr": 0.50,
            "method": "isochrone",
            "reference": "Joyce & Chaboyer 2018",
            "bibcode": "2018ApJ...864...99J",
            "doi": "10.3847/1538-4357/aad464",
            "recommended": True,
        },
        {
            "value_gyr": 6.52,
            "uncertainty_gyr": 0.30,
            "method": "asteroseismology",
            "reference": "Bazot et al. 2007",
            "bibcode": "2007A&A...470..295B",
            "doi": "10.1051/0004-6361:20065694",
            "recommended": False,
        },
        {
            "value_gyr": 4.4,
            "uncertainty_gyr": 1.1,
            "method": "asteroseismology",
            "reference": "Bazot et al. 2016",
            "bibcode": "2016A&A...588A..77B",
            "doi": "10.1051/0004-6361/201527967",
            "recommended": False,
        },
        {
            "value_gyr": 6.41,
            "uncertainty_gyr": 0.30,
            "method": "asteroseismology",
            "reference": "Thévenin et al. 2002",
            "bibcode": "2002A&A...392L...9T",
            "doi": "10.1051/0004-6361:20021094",
            "recommended": False,
        },
    ],
    "metallicity_measurements": [
        {
            "value_dex": 0.24,
            "uncertainty_dex": 0.03,
            "method": "high_res_spectroscopy",
            "reference": "Porto de Mello et al. 2008",
            "bibcode": "2008A&A...488..653P",
            "doi": "10.1051/0004-6361:200810031",
            "recommended": True,
        },
        {
            "value_dex": 0.26,
            "uncertainty_dex": 0.08,
            "method": "high_res_spectroscopy",
            "reference": "Heiter et al. 2015",
            "bibcode": "2015A&A...582A..49H",
            "doi": "10.1051/0004-6361/201526319",
            "recommended": False,
        },
    ],
    "rotation_measurements": [
        {
            "value_days": 22.0,
            "uncertainty_days": 3.0,
            "method": "photometric_variability",
            "reference": "DeWarf et al. 2010",
            "bibcode": "2010ApJ...722..343D",
            "doi": "10.1088/0004-637X/722/1/343",
            "recommended": True,
        },
    ],
    "activity_measurements": [
        {
            "value_log_rhk": -4.95,
            "method": "log_rhk",
            "reference": "DeWarf et al. 2010",
            "bibcode": "2010ApJ...722..343D",
            "doi": "10.1088/0004-637X/722/1/343",
            "recommended": True,
        },
        {
            "value_log_rhk": -5.00,
            "method": "log_rhk",
            "reference": "Henry et al. 1996",
            "bibcode": "1996AJ....111..439H",
            "doi": "10.1086/117796",
            "recommended": False,
        },
    ],
}


# ── Alpha Centauri B ────────────────────────────────────────────────────────

ALPHA_B = {
    "teff_k": 5260,
    "spectype": "K1 V",
    "mass_measurements": [
        {
            "value_msun": 0.9373,
            "uncertainty_msun": 0.0033,
            "method": "binary_orbit",
            "reference": "Pourbaix & Boffin 2016",
            "bibcode": "2016A&A...586A..90P",
            "doi": "10.1051/0004-6361/201527859",
            "recommended": True,
        },
        {
            "value_msun": 0.972,
            "uncertainty_msun": 0.0045,
            "method": "binary_orbit",
            "reference": "Kervella et al. 2016",
            "bibcode": "2016A&A...594A.107K",
            "doi": "10.1051/0004-6361/201629201",
            "recommended": False,
        },
        {
            "value_msun": 0.934,
            "uncertainty_msun": 0.0061,
            "method": "evolutionary_model",
            "reference": "Joyce & Chaboyer 2018",
            "bibcode": "2018ApJ...864...99J",
            "doi": "10.3847/1538-4357/aad464",
            "recommended": False,
        },
    ],
    "radius_measurements": [
        {
            "value_rsun": 0.8632,
            "uncertainty_rsun": 0.0037,
            "method": "interferometry",
            "reference": "Kervella et al. 2017",
            "bibcode": "2017A&A...597A.137K",
            "doi": "10.1051/0004-6361/201629505",
            "recommended": True,
        },
        {
            "value_rsun": 0.863,
            "uncertainty_rsun": 0.005,
            "method": "interferometry",
            "reference": "Bigot et al. 2006",
            "bibcode": "2006A&A...446..635B",
            "doi": "10.1051/0004-6361:20053187",
            "recommended": False,
        },
        {
            "value_rsun": 0.863,
            "uncertainty_rsun": 0.005,
            "method": "interferometry",
            "reference": "Kervella et al. 2003",
            "bibcode": "2003A&A...404.1087K",
            "doi": "10.1051/0004-6361:20030570",
            "recommended": False,
        },
    ],
    "teff_measurements": [
        {
            "value_k": 5316,
            "uncertainty_k": 28,
            "method": "high_res_spectroscopy",
            "reference": "Porto de Mello et al. 2008",
            "bibcode": "2008A&A...488..653P",
            "doi": "10.1051/0004-6361:200810031",
            "recommended": True,
        },
        {
            "value_k": 5231,
            "uncertainty_k": 20,
            "method": "sed_fitting",
            "reference": "Heiter et al. 2015",
            "bibcode": "2015A&A...582A..49H",
            "doi": "10.1051/0004-6361/201526319",
            "recommended": False,
        },
    ],
    "luminosity_measurements": [
        {
            "value_lsun": 0.503,
            "uncertainty_lsun": 0.007,
            "method": "bolometric_flux",
            "reference": "Kervella et al. 2017",
            "bibcode": "2017A&A...597A.137K",
            "doi": "10.1051/0004-6361/201629505",
            "recommended": True,
        },
    ],
    "age_measurements": [
        {
            "value_gyr": 4.81,
            "uncertainty_gyr": 0.50,
            "method": "isochrone",
            "reference": "Joyce & Chaboyer 2018",
            "bibcode": "2018ApJ...864...99J",
            "doi": "10.3847/1538-4357/aad464",
            "recommended": True,
        },
        {
            "value_gyr": 6.41,
            "uncertainty_gyr": 0.30,
            "method": "asteroseismology",
            "reference": "Eggenberger et al. 2004",
            "bibcode": "2004A&A...417..235E",
            "doi": "10.1051/0004-6361:20034203",
            "recommended": False,
        },
        {
            "value_gyr": 6.41,
            "uncertainty_gyr": 0.30,
            "method": "asteroseismology",
            "reference": "Thévenin et al. 2002",
            "bibcode": "2002A&A...392L...9T",
            "doi": "10.1051/0004-6361:20021094",
            "recommended": False,
        },
    ],
    "metallicity_measurements": [
        {
            "value_dex": 0.25,
            "uncertainty_dex": 0.04,
            "method": "high_res_spectroscopy",
            "reference": "Porto de Mello et al. 2008",
            "bibcode": "2008A&A...488..653P",
            "doi": "10.1051/0004-6361:200810031",
            "recommended": True,
        },
        {
            "value_dex": 0.22,
            "uncertainty_dex": 0.10,
            "method": "high_res_spectroscopy",
            "reference": "Heiter et al. 2015",
            "bibcode": "2015A&A...582A..49H",
            "doi": "10.1051/0004-6361/201526319",
            "recommended": False,
        },
    ],
    "rotation_measurements": [
        {
            "value_days": 41.0,
            "uncertainty_days": 3.0,
            "method": "photometric_variability",
            "reference": "DeWarf et al. 2010",
            "bibcode": "2010ApJ...722..343D",
            "doi": "10.1088/0004-637X/722/1/343",
            "recommended": True,
        },
    ],
    "activity_measurements": [
        {
            "value_log_rhk": -4.85,
            "method": "log_rhk",
            "reference": "DeWarf et al. 2010",
            "bibcode": "2010ApJ...722..343D",
            "doi": "10.1088/0004-637X/722/1/343",
            "recommended": True,
        },
    ],
}


# ── Proxima Cen ─────────────────────────────────────────────────────────────

PROXIMA = {
    "teff_k": 2904,
    "spectype": "M5.5 Ve",
    "mass_measurements": [
        {
            "value_msun": 0.1221,
            "uncertainty_msun": 0.0022,
            "method": "evolutionary_model",
            "reference": "Suárez Mascareño et al. 2025",
            "bibcode": "2025A&A...700A..11M",
            "doi": "10.1051/0004-6361/202554723",
            "recommended": True,
        },
        {
            "value_msun": 0.1221,
            "uncertainty_msun": 0.0035,
            "method": "spectroscopic_calibration",
            "reference": "Mann et al. 2019",
            "bibcode": "2019ApJ...871...63M",
            "doi": "10.3847/1538-4357/aaf3bc",
            "recommended": False,
        },
        {
            "value_msun": 0.120,
            "uncertainty_msun": 0.015,
            "method": "spectroscopic_calibration",
            "reference": "Anglada-Escudé et al. 2016",
            "bibcode": "2016Natur.536..437A",
            "doi": "10.1038/nature19106",
            "recommended": False,
        },
    ],
    "radius_measurements": [
        {
            "value_rsun": 0.1410,
            "uncertainty_rsun": 0.0070,
            "method": "interferometry",
            "reference": "Boyajian et al. 2012",
            "bibcode": "2012ApJ...757..112B",
            "doi": "10.1088/0004-637X/757/2/112",
            "recommended": True,
        },
        {
            "value_rsun": 0.141,
            "uncertainty_rsun": 0.011,
            "method": "interferometry",
            "reference": "Demory et al. 2009",
            "bibcode": "2009A&A...505..205D",
            "doi": "10.1051/0004-6361/200911976",
            "recommended": False,
        },
        {
            "value_rsun": 0.141,
            "uncertainty_rsun": 0.021,
            "method": "evolutionary_model",
            "reference": "Suárez Mascareño et al. 2025",
            "bibcode": "2025A&A...700A..11M",
            "doi": "10.1051/0004-6361/202554723",
            "recommended": False,
        },
        {
            "value_rsun": 0.146,
            "uncertainty_rsun": 0.007,
            "method": "sed_fitting",
            "reference": "Schweitzer et al. 2019",
            "bibcode": "2019A&A...625A..68S",
            "doi": "10.1051/0004-6361/201834965",
            "recommended": False,
        },
    ],
    "teff_measurements": [
        {
            "value_k": 2904,
            "uncertainty_k": 51,
            "method": "high_res_spectroscopy",
            "reference": "Passegger et al. 2019",
            "bibcode": "2019A&A...627A.161P",
            "doi": "10.1051/0004-6361/201935679",
            "recommended": True,
        },
        {
            "value_k": 3000,
            "uncertainty_k": 70,
            "method": "sed_fitting",
            "reference": "Cifuentes et al. 2020",
            "bibcode": "2020A&A...642A.115C",
            "doi": "10.1051/0004-6361/202038295",
            "recommended": False,
        },
        {
            "value_k": 2900,
            "uncertainty_k": 100,
            "method": "high_res_spectroscopy",
            "reference": "Pineda et al. 2021",
            "bibcode": "2021ApJ...918...40P",
            "doi": "10.3847/1538-4357/ac0aea",
            "recommended": False,
        },
        {
            "value_k": 3050,
            "uncertainty_k": 100,
            "method": "sed_fitting",
            "reference": "Anglada-Escudé et al. 2016",
            "bibcode": "2016Natur.536..437A",
            "doi": "10.1038/nature19106",
            "recommended": False,
        },
    ],
    "luminosity_measurements": [
        {
            "value_lsun": 0.00155,
            "uncertainty_lsun": 0.00006,
            "method": "bolometric_flux",
            "reference": "Boyajian et al. 2012",
            "bibcode": "2012ApJ...757..112B",
            "doi": "10.1088/0004-637X/757/2/112",
            "recommended": True,
        },
        {
            "value_lsun": 0.00150,
            "uncertainty_lsun": 0.00012,
            "method": "bolometric_flux",
            "reference": "Demory et al. 2009",
            "bibcode": "2009A&A...505..205D",
            "doi": "10.1051/0004-6361/200911976",
            "recommended": False,
        },
    ],
    "age_measurements": [
        {
            "value_gyr": 4.85,
            "uncertainty_gyr": 0.50,
            "method": "kinematic",
            "reference": "Kervella et al. 2017",
            "bibcode": "2017A&A...598L...7K",
            "doi": "10.1051/0004-6361/201629930",
            "recommended": True,
        },
    ],
    "metallicity_measurements": [
        {
            "value_dex": 0.05,
            "uncertainty_dex": 0.16,
            "method": "high_res_spectroscopy",
            "reference": "Passegger et al. 2019",
            "bibcode": "2019A&A...627A.161P",
            "doi": "10.1051/0004-6361/201935679",
            "recommended": True,
        },
    ],
    "rotation_measurements": [
        {
            "value_days": 83.0,
            "uncertainty_days": 0.8,
            "method": "photometric_variability",
            "reference": "Suárez Mascareño et al. 2016",
            "bibcode": "2016MNRAS.459.3565S",
            "doi": "10.1093/mnras/stw1059",
            "recommended": True,
        },
        {
            "value_days": 89.8,
            "uncertainty_days": 4.0,
            "method": "zeeman_doppler",
            "reference": "Klein et al. 2021",
            "bibcode": "2021MNRAS.500.1844K",
            "doi": "10.1093/mnras/staa3396",
            "recommended": False,
        },
        {
            "value_days": 83.5,
            "uncertainty_days": 0.5,
            "method": "photometric_variability",
            "reference": "Benedict et al. 1998",
            "bibcode": "1998AJ....116..429B",
            "doi": "10.1086/300420",
            "recommended": False,
        },
    ],
    "activity_measurements": [
        {
            "value_log_rhk": -5.55,
            "method": "log_rhk",
            "reference": "Suárez Mascareño et al. 2016",
            "bibcode": "2016MNRAS.459.3565S",
            "doi": "10.1093/mnras/stw1059",
            "recommended": True,
        },
    ],
}


# ── Proxima Cen 행성들 (orbital + physical 모두 array) ────────────────────────

PROXIMA_B = [
    # (paper_key, orbital_dict, physical_dict)
    (
        "A16",
        {
            "period_days": 11.186,
            "uncertainty_period_days": 0.002,
            "semi_major_axis_au": 0.0485,
            "eccentricity": 0.35,
            "uncertainty_eccentricity": 0.25,
            "mean_anomaly_at_epoch_deg": 0.0,
        },
        {
            "mass_mearth": 1.27,
            "uncertainty_mearth": 0.18,
            "mass_type": "Msini",
        },
        {
            "source": "Anglada-Escudé et al. 2016",
            "bibcode": "2016Natur.536..437A",
            "doi": "10.1038/nature19106",
            "method": "rv",
        },
        False,
    ),
    (
        "F22",
        {
            "period_days": 11.18427,
            "uncertainty_period_days": 0.00041,
            "semi_major_axis_au": 0.04857,
            "uncertainty_semi_major_axis_au": 0.00029,
            "eccentricity": 0.02,
            "uncertainty_eccentricity": 0.10,
            "mean_anomaly_at_epoch_deg": 0.0,
        },
        {
            "mass_mearth": 1.07,
            "uncertainty_mearth": 0.06,
            "mass_type": "Msini",
        },
        {
            "source": "Faria et al. 2022",
            "bibcode": "2022A&A...658A.115F",
            "doi": "10.1051/0004-6361/202142337",
            "method": "rv",
        },
        False,
    ),
    (
        "SM25",
        {
            "period_days": 11.18465,
            "uncertainty_period_days": 0.00053,
            "semi_major_axis_au": 0.04848,
            "uncertainty_semi_major_axis_au": 0.00029,
            "eccentricity": 0.0,
            "longitude_of_ascending_node_deg": None,
            "epoch_jd": 2460548.59,
            "mean_anomaly_at_epoch_deg": 0.0,
        },
        {
            "mass_mearth": 1.055,
            "uncertainty_mearth": 0.055,
            "mass_type": "Msini",
        },
        {
            "source": "Suárez Mascareño et al. 2025",
            "bibcode": "2025A&A...700A..11M",
            "doi": "10.1051/0004-6361/202554723",
            "method": "rv",
        },
        True,
    ),
]

PROXIMA_D = [
    (
        "F22",
        {
            "period_days": 5.122,
            "uncertainty_period_days": 0.001,
            "semi_major_axis_au": 0.02885,
            "eccentricity": 0.04,
            "uncertainty_eccentricity": 0.11,
            "mean_anomaly_at_epoch_deg": 0.0,
        },
        {
            "mass_mearth": 0.26,
            "uncertainty_mearth": 0.05,
            "mass_type": "Msini",
        },
        {
            "source": "Faria et al. 2022",
            "bibcode": "2022A&A...658A.115F",
            "doi": "10.1051/0004-6361/202142337",
            "method": "rv",
        },
        False,
    ),
    (
        "SM25",
        {
            "period_days": 5.12338,
            "uncertainty_period_days": 0.00035,
            "semi_major_axis_au": 0.02881,
            "uncertainty_semi_major_axis_au": 0.00017,
            "eccentricity": 0.0,
            "longitude_of_ascending_node_deg": None,
            "epoch_jd": 2460557.55,
            "mean_anomaly_at_epoch_deg": 0.0,
        },
        {
            "mass_mearth": 0.26,
            "uncertainty_mearth": 0.038,
            "mass_type": "Msini",
        },
        {
            "source": "Suárez Mascareño et al. 2025",
            "bibcode": "2025A&A...700A..11M",
            "doi": "10.1051/0004-6361/202554723",
            "method": "rv",
        },
        True,
    ),
]


def _build_planet_array(entries):
    """(key, orb_extras, phy_extras, prov, recommended) → curated array"""
    out = []
    for _key, orb, phy, prov, rec in entries:
        orbital = dict(orb)
        orbital.update(prov)
        orbital["recommended"] = rec
        physical = dict(phy)
        physical.update(prov)
        physical["recommended"] = rec
        out.append({"orbital": orbital, "physical": physical})
    return out


def main():
    # stellar_props_curated.json
    with open(STELLAR_CURATED, "r", encoding="utf-8") as f:
        stellar = json.load(f)

    stellar["Alpha Centauri A"] = ALPHA_A
    stellar["Alpha Centauri B"] = ALPHA_B
    stellar["Proxima Cen"] = PROXIMA

    with open(STELLAR_CURATED, "w", encoding="utf-8") as f:
        json.dump(stellar, f, indent=2, ensure_ascii=False)
    print(f"updated stellar_props_curated.json: Alpha A/B + Proxima")

    # planets_curated.json
    with open(PLANETS_CURATED, "r", encoding="utf-8") as f:
        planets = json.load(f)

    # Proxima b, d 를 array 형식으로 재구성
    proxima_planets = []
    proxima_planets.append({
        "pl_name": "Proxima Cen b",
        "orbital": _extract_blocks(PROXIMA_B, "orbital"),
        "physical": _extract_blocks(PROXIMA_B, "physical"),
    })
    proxima_planets.append({
        "pl_name": "Proxima Cen d",
        "orbital": _extract_blocks(PROXIMA_D, "orbital"),
        "physical": _extract_blocks(PROXIMA_D, "physical"),
    })

    planets["Proxima Cen"] = proxima_planets

    with open(PLANETS_CURATED, "w", encoding="utf-8") as f:
        json.dump(planets, f, indent=2, ensure_ascii=False)
    print(f"updated planets_curated.json: Proxima b/d arrays")


def _extract_blocks(entries, block_name):
    """entries → list of block dicts (orbital or physical)"""
    out = []
    for _key, orb, phy, prov, rec in entries:
        block = dict(orb if block_name == "orbital" else phy)
        block.update(prov)
        block["recommended"] = rec
        out.append(block)
    return out


if __name__ == "__main__":
    main()
