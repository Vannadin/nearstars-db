# TRAPPIST-1 Phase 2 측정값을 planets_curated.json에 array form으로 덮어쓰기
"""TRAPPIST-1 7개 행성의 physical을 dict → array로 확장.

NASA Archive ps 테이블에서 가져온 paper별 mass/radius (Gillon 2017,
Grimm 2018, Agol 2021, Luger 2017 for h) 를 누적. recommended=Agol 2021.
orbital은 dict 유지 (paper별 변동이 작아 Phase 2로 분리 불필요).

실행:
    python3 phase2/trappist_1/apply_phase2.py
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURATED = os.path.join(BASE, "db", "planets_curated.json")

REFS = {
    "G17": {
        "source": "Gillon et al. 2017",
        "bibcode": "2017Natur.542..456G",
        "doi": "10.1038/nature21360",
        "method": "ttv",
    },
    "Gr18": {
        "source": "Grimm et al. 2018",
        "bibcode": "2018A&A...613A..68G",
        "doi": "10.1051/0004-6361/201732233",
        "method": "ttv",
    },
    "A21": {
        "source": "Agol et al. 2021",
        "bibcode": "2021PSJ.....2....1A",
        "doi": "10.3847/PSJ/abd022",
        "method": "ttv",
    },
    "L17": {
        "source": "Luger et al. 2017",
        "bibcode": "2017NatAs...1E.129L",
        "doi": "10.1038/s41550-017-0129",
        "method": "discovery",
    },
}

# (paper_key, mass, mass_err, rad, rad_err)  — None = no measurement in this paper
DATA = {
    "TRAPPIST-1 b": [
        ("G17", 0.85,  0.72,  1.086, 0.035),
        ("Gr18", 1.017, 0.154, 1.121, 0.031),
        ("A21", 1.374, 0.069, 1.116, 0.014),
    ],
    "TRAPPIST-1 c": [
        ("G17", 1.38, 0.61, 1.056, 0.035),
        ("Gr18", 1.156, 0.142, 1.095, 0.030),
        ("A21", 1.308, 0.056, 1.097, 0.014),
    ],
    "TRAPPIST-1 d": [
        ("G17", 0.41, 0.27, 0.772, 0.030),
        ("Gr18", 0.297, 0.039, 0.784, 0.023),
        ("A21", 0.388, 0.012, 0.788, 0.011),
    ],
    "TRAPPIST-1 e": [
        ("G17", 0.62, 0.58, 0.918, 0.039),
        ("Gr18", 0.772, 0.079, 0.910, 0.026),
        ("A21", 0.692, 0.022, 0.920, 0.013),
    ],
    "TRAPPIST-1 f": [
        ("G17", 0.68, 0.18, 1.045, 0.038),
        ("Gr18", 0.934, 0.080, 1.046, 0.029),
        ("A21", 1.039, 0.031, 1.045, 0.013),
    ],
    "TRAPPIST-1 g": [
        ("G17", 1.34, 0.88, 1.127, 0.041),
        ("Gr18", 1.148, 0.098, 1.148, 0.032),
        ("A21", 1.321, 0.038, 1.129, 0.015),
    ],
    "TRAPPIST-1 h": [
        ("G17", None, None, 0.755, 0.034),
        ("L17", None, None, 0.752, 0.032),
        ("Gr18", 0.331, 0.056, 0.773, 0.026),
        ("A21", 0.326, 0.020, 0.755, 0.014),
    ],
}

# 어느 paper가 recommended인지 (모두 Agol 2021)
RECOMMENDED_KEY = "A21"


def physical_array(measurements):
    """list of (key, m, m_e, r, r_e) → array of measurement dicts."""
    out = []
    for key, m, m_e, r, r_e in measurements:
        ref = REFS[key]
        entry = {
            "source":   ref["source"],
            "bibcode":  ref["bibcode"],
            "doi":      ref["doi"],
            "method":   ref["method"],
            "recommended": (key == RECOMMENDED_KEY),
        }
        # Mass: 있는 경우만
        if m is not None:
            entry["true_mass_mearth"] = m
            entry["uncertainty_mearth"] = m_e
            entry["mass_type"] = "true mass"
        # Radius
        if r is not None:
            entry["radius_rearth"] = r
            entry["uncertainty_rearth"] = r_e
        out.append(entry)
    return out


def main():
    with open(CURATED) as f:
        curated = json.load(f)

    t = curated["TRAPPIST-1"]
    for pl in t:
        name = pl["pl_name"]
        if name not in DATA:
            print(f"WARN: {name} not in DATA")
            continue
        pl["physical"] = physical_array(DATA[name])
        # orbital은 dict 유지

    with open(CURATED, "w") as f:
        json.dump(curated, f, indent=2, ensure_ascii=False)
    print(f"updated {CURATED}: 7 TRAPPIST-1 planets → physical array form")


if __name__ == "__main__":
    main()
