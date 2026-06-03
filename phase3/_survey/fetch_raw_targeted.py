# beyond-50ly 신규 2개(V1400 Cen, PSR J0108-1431)의 raw astrometry/photometry 를 surgical 병합하는 일회성 스크립트
"""Surgically add raw astrometry/photometry for the two beyond-50ly targets
WITHOUT re-fetching the whole target_list (which fetch_astrometry.py does and
would risk churning the other 150 systems' raw values / clashing with parallel
sessions).

- V1400 Cen: one targeted Gaia DR3 TAP query by source_id (real fetched data).
- PSR J0108-1431: hand-set from VLBI literature (Deller et al. 2009) — the
  pulsar is optically far below Gaia's limit, so it has no Gaia row; VLBI is
  the authoritative (and more precise) astrometry.

Merges into db/astrometry_raw.json + db/photometry_raw.json via
schema.write_canonical, touching only the two new keys.
"""

import json
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, "scripts/pipeline")
import schema  # noqa: E402

JD_GAIA = 2457389.0     # J2016.0 (Gaia DR3 reference epoch)
JD_J2000 = 2451545.0    # J2000.0

V1400_SID = "6117085769513415168"


def fetch_gaia_one(source_id):
    cols = ("ra,dec,ra_error,dec_error,parallax,parallax_error,"
            "pmra,pmra_error,pmdec,pmdec_error,"
            "radial_velocity,radial_velocity_error,phot_g_mean_mag,bp_rp")
    adql = (f"SELECT {cols} FROM gaiadr3.gaia_source "
            f"WHERE source_id={source_id}")
    params = {
        "REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json",
        "QUERY": adql,
    }
    url = ("https://gea.esac.esa.int/tap-server/tap/sync?"
           + urllib.parse.urlencode(params))
    with urllib.request.urlopen(url, timeout=60) as r:
        data = json.load(r)
    names = [c["name"] for c in data["metadata"]]
    row = dict(zip(names, data["data"][0]))
    return row


def main():
    astro = schema.load_json("db/astrometry_raw.json") if hasattr(schema, "load_json") \
        else json.load(open("db/astrometry_raw.json"))
    phot = json.load(open("db/photometry_raw.json"))

    # ── V1400 Cen — real Gaia DR3 row ──
    g = fetch_gaia_one(V1400_SID)
    astro["V1400 Centauri"] = {
        "source": "gaia_dr3",
        "source_id": V1400_SID,
        "epoch_jd": JD_GAIA,
        "epoch_label": "J2016.0",
        "ra_deg": g["ra"],
        "ra_error_mas": g["ra_error"],
        "dec_deg": g["dec"],
        "dec_error_mas": g["dec_error"],
        "parallax_mas": g["parallax"],
        "parallax_error_mas": g["parallax_error"],
        "pmra_mas_yr": g["pmra"],
        "pmra_error_mas_yr": g["pmra_error"],
        "pmdec_mas_yr": g["pmdec"],
        "pmdec_error_mas_yr": g["pmdec_error"],
        "radial_velocity_km_s": g.get("radial_velocity"),
        "rv_error_km_s": g.get("radial_velocity_error"),
    }
    if g.get("phot_g_mean_mag") is not None:
        phot["V1400 Centauri"] = {
            "g_mag": g["phot_g_mean_mag"],
            "bp_rp": g.get("bp_rp"),
            "vmag_v": 12.31,                       # Mamajek et al. 2012
            "vmag_source": "Mamajek et al. 2012",
        }

    # ── PSR J0108-1431 — VLBI literature (Deller et al. 2009, ApJ 701, 1243) ──
    # position = catalog J2000 (ATNF); parallax + proper motion = VLBI.
    # No spectroscopic RV (a neutron star has no spectral lines) → null.
    astro["PSR J0108-1431"] = {
        "source": "vlbi",
        "source_id": None,
        "epoch_jd": JD_J2000,
        "epoch_label": "J2000.0",
        "ra_deg": 17.034583,                       # 01h08m08.3s
        "ra_error_mas": None,
        "dec_deg": -14.530556,                     # -14d31m50s
        "dec_error_mas": None,
        "parallax_mas": 4.17,                      # Deller et al. 2009 (raw VLBI)
        "parallax_error_mas": 1.42,
        "pmra_mas_yr": 75.05,
        "pmra_error_mas_yr": 2.26,
        "pmdec_mas_yr": -152.54,
        "pmdec_error_mas_yr": 1.65,
        "radial_velocity_km_s": None,
        "rv_error_km_s": None,
    }

    schema.write_canonical("db/astrometry_raw.json", astro)
    schema.write_canonical("db/photometry_raw.json", phot)
    print("merged: V1400 Centauri (Gaia DR3), PSR J0108-1431 (VLBI)")
    print(f"  V1400 Cen parallax = {astro['V1400 Centauri']['parallax_mas']:.4f} mas "
          f"({1000/astro['V1400 Centauri']['parallax_mas']:.1f} pc)")
    print(f"  PSR J0108 parallax = {astro['PSR J0108-1431']['parallax_mas']} mas "
          f"({1000/astro['PSR J0108-1431']['parallax_mas']:.0f} pc)")


if __name__ == "__main__":
    main()
