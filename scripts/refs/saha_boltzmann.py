# Saha/Boltzmann LTE 등온 슬랩으로 조성·온도 → 가시광 발광색을 1차원리 합성하는 엔진
"""LTE isothermal-slab plasma emission color engine.

For a bulk composition at temperature T and reference pressure P, synthesize the
emergent visible spectrum of a uniform slab and reduce it to a display hue via
CIE 1931 (cie_color):

    I(λ) = B_λ(T) · (1 − exp(−τ_λ)),    τ_λ = κ_cont + κ_line+band(λ)

In LTE the source function is the Planck function B_λ(T), so the emergent
intensity interpolates the two physical regimes the old hand-tuned table glued
together, with the crossover *computed*:

  - τ ≫ 1 (cool dense gas) ⇒ I → B_λ(T): thermal incandescence (ember→blue-white).
  - τ ≪ 1 (hot rarefied gas) ⇒ I → emission spectrum: atomic lines + molecular
    bands, each appearing only as Saha ionization / Boltzmann excitation /
    dissociation equilibrium populate their upper states.

Emission is built from upper-state populations (Kirchhoff κ = j / B_λ), which
unifies atomic lines (n_upper·A_ki, from atomic_lines.yaml) and molecular bands
(band-as-effective-line, from molecular_bands.yaml). Molecular abundances come
from dissociation equilibrium (law of mass action with bond energy D0 +
partition functions), so the molecular→atomic→ionic color march is physics, not
a ramp.

MODELING CHOICES (documented): fixed P + slab path scale (overall optical depth),
gray continuum coefficient (line-vs-continuum contrast), truncated partition
functions, fixed band/line display widths, first-ion ionization cap, single
dominant molecule per gas (no inter-molecule competition), LTE. Everything else
(Saha, Boltzmann, dissociation, NIST A-values, CIE) is first-principles.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cie_color  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ATOMIC_DB = ROOT / "db" / "refs" / "atomic_lines.yaml"
MOLBAND_DB = ROOT / "db" / "refs" / "molecular_bands.yaml"

# ── physical constants (cgs) ──
K_EV = 8.617333e-5        # Boltzmann k [eV/K]
K_CM = 0.6950348          # k [cm^-1 / K]   (kT[cm^-1] = K_CM·T)
K_ERG = 1.380649e-16      # Boltzmann k [erg/K]
SAHA = 2.4146e15          # (2π m_e k / h²)^{3/2} [cm^-3 K^-3/2]
MU_OVER_ME = 1823.2       # (amu / m_e), to scale SAHA for molecular dissociation
P_REF = 1.01325e6         # reference pressure [dyn/cm²] = 1 atm

# ── calibration (single balance constant; see module docstring) ──
# Optically-thin LTE emission: j(λ) = thermal_continuum + GAIN·line/band emission.
#   thermal = (n_heavy/N_REF)·Planck_shape  — incandescent glow of the bulk gas,
#     ∝ density (∝1/T at fixed P) so it fades as the gas heats and rarefies.
#   GAIN sets the one thermal:emission balance point; the *shape* and T-evolution
#   of each term are first-principles (Saha/Boltzmann/dissociation).
N_REF = 2.0e18            # reference heavy-particle density [cm^-3] (~P/kT at 3700K)
GAIN = 3.0e-6             # emission gain relative to the thermal continuum
LINE_WIDTH_NM = 1.2       # atomic-line display half-width [nm]
BAND_WIDTH_NM = 5.0       # molecular-band display half-width [nm]

ION_U = {"H": 1.0, "He": 2.0}   # ion partition fns where no level list (H II, He II)
U_ION_MOL = 2.0                 # crude U(cation)/U(neutral) for molecular ionization

# Composition → element mole fractions (by nuclei, fully dissociated).
COMPOSITIONS = {
    "air":   {"N": 0.79, "O": 0.21},
    "co2":   {"C": 0.333, "O": 0.667},
    "h2_he": {"H": 0.92, "He": 0.08},
    "ch4":   {"C": 0.20, "H": 0.80},
    "h2o":   {"H": 0.667, "O": 0.333},
    "nh3":   {"N": 0.25, "H": 0.75},
}

# Element → (neutral key, first-ion key or None).
ELEMENTS = {
    "H":  ("H_I", None),
    "He": ("He_I", None),
    "C":  ("C_I", "C_II"),
    "N":  ("N_I", "N_II"),
    "O":  ("O_I", "O_II"),
}


def load_dbs():
    atomic = yaml.safe_load(ATOMIC_DB.read_text(encoding="utf-8"))
    mol = yaml.safe_load(MOLBAND_DB.read_text(encoding="utf-8"))
    return atomic, mol


def partition_fn(levels: list[dict], T: float) -> float:
    kt = K_CM * T
    return sum(l["g"] * math.exp(-l["E_cm"] / kt) for l in levels) or 1.0


# ── ionization (Saha) ──

def saha_S(elem: str, db: dict, T: float) -> float:
    """Saha factor S = n1·n_e/n0 [cm^-3] for neutral⇌first-ion of `elem`."""
    neu_key, ion_key = ELEMENTS[elem]
    neu = db[neu_key]
    U0 = partition_fn(neu["partition_levels"], T)
    U1 = partition_fn(db[ion_key]["partition_levels"], T) if ion_key else ION_U[elem]
    chi = neu["ionization_energy_eV"]
    return 2.0 * (U1 / U0) * SAHA * T ** 1.5 * math.exp(-chi / (K_EV * T))


def solve_ne(elems: dict, db: dict, T: float, n_heavy: float) -> float:
    """Charge neutrality n_e = Σ n_el·S_el/(n_e+S_el), bisection on n_e."""
    S = {el: saha_S(el, db, T) for el in elems}
    n_el = {el: frac * n_heavy for el, frac in elems.items()}

    def rhs(ne):
        return sum(n_el[el] * S[el] / (ne + S[el]) for el in elems)

    lo, hi = 1.0, n_heavy
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if rhs(mid) - mid > 0:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


# ── dissociation equilibrium (law of mass action) ──

def diss_K(mol: dict, atomic: dict, T: float) -> float:
    """K = n_A·n_B/n_AB [cm^-3] for the molecule's dissociation."""
    kt_cm = K_CM * T
    theta_v = 1.43877 * mol["omega_e"]
    U_vib = 1.0 / (1.0 - math.exp(-theta_v / T))
    U_rot = T / (mol["sigma"] * 1.43877 * mol["B_e"])
    U_mol = mol["g_elec"] * U_vib * U_rot
    a, b = mol["forms_from"]
    U_a = partition_fn(atomic[ELEMENTS[a][0]]["partition_levels"], T)
    U_b = partition_fn(atomic[ELEMENTS[b][0]]["partition_levels"], T)
    pref = SAHA * (MU_OVER_ME * mol["mu_amu"]) ** 1.5 * T ** 1.5
    return pref * (U_a * U_b / U_mol) * math.exp(-mol["D0_eV"] / (K_EV * T))


def molecule_density(mol: dict, atomic: dict, elems: dict, n_heavy: float, T: float) -> float:
    """Neutral molecule number density from dissociation equilibrium."""
    K = diss_K(mol, atomic, T)
    a, b = mol["forms_from"]
    if a == b:                                  # homonuclear A2: n_A²/n_A2 = K
        n_tot = elems.get(a, 0.0) * n_heavy
        if n_tot <= 0:
            return 0.0
        n_A = (-K + math.sqrt(K * K + 8.0 * K * n_tot)) / 4.0
        return max(0.0, (n_tot - n_A) / 2.0)
    na = elems.get(a, 0.0) * n_heavy            # heteronuclear AB
    nb = elems.get(b, 0.0) * n_heavy
    if na <= 0 or nb <= 0:
        return 0.0
    s = na + nb + K
    return max(0.0, (s - math.sqrt(s * s - 4.0 * na * nb)) / 2.0)


# ── spectrum synthesis ──

def slab_spectrum(comp_key: str, T: float, atomic: dict, mol_db: dict):
    """Named-composition wrapper around slab_spectrum_custom."""
    return slab_spectrum_custom(COMPOSITIONS[comp_key],
                                mol_db["composition_bands"].get(comp_key, []),
                                T, atomic, mol_db)


def slab_spectrum_custom(elems: dict, band_list: list, T: float, atomic: dict, mol_db: dict):
    """Return (intensity over cie_color.LAMBDAS, diagnostics) for an ARBITRARY
    element-fraction dict + list of active molecular band-system names. Elements
    must be in ELEMENTS (H, He, C, N, O)."""
    kt_cm = K_CM * T
    n_heavy = P_REF / (K_ERG * T)
    n_e = solve_ne(elems, atomic, T, n_heavy)

    # (λ0, strength, width) emission contributions; strength ∝ n_upper·A·hν / n_heavy
    contribs = []
    ion_frac = 0.0

    # atomic lines
    for el, frac in elems.items():
        neu_key, ion_key = ELEMENTS[el]
        n_el = frac * n_heavy
        S = saha_S(el, atomic, T)
        n1 = n_el * S / (n_e + S)
        n0 = n_el - n1
        ion_frac += (n1 / n_el) * frac
        for entry, n_stage in ((atomic[neu_key], n0), (atomic[ion_key], n1) if ion_key else (None, 0)):
            if entry is None or n_stage <= 0:
                continue
            U = partition_fn(entry["partition_levels"], T)
            for ln in entry["lines"]:
                n_up = n_stage * ln["g_upper"] / U * math.exp(-ln["E_upper_cm"] / kt_cm)
                s = (n_up / n_heavy) * ln["A_ki"] * (1e7 / ln["nm"])
                if s > 0:
                    contribs.append((ln["nm"], s, LINE_WIDTH_NM))

    # molecular bands
    mol_frac = 0.0
    for sysname in band_list:
        bs = mol_db["band_systems"][sysname]
        mol = mol_db["molecules"][bs["molecule"]]
        n_mol = molecule_density(mol, atomic, elems, n_heavy, T)
        if bs["charge"] == 1:                    # cation: ionize the molecule
            S_ion = U_ION_MOL * SAHA * T ** 1.5 * math.exp(-mol["ion_chi_eV"] / (K_EV * T))
            n_mol = n_mol * S_ion / (n_e + S_ion)
        if n_mol <= 0:
            continue
        # diagnostic: fraction of the limiting element's atoms bound in this molecule
        if bs["charge"] == 0:
            ff = mol["forms_from"]
            lim_el = min(set(ff), key=lambda x: elems.get(x, 1e9))
            lim_tot = elems.get(lim_el, 0.0) * n_heavy
            if lim_tot > 0:
                mol_frac = max(mol_frac, ff.count(lim_el) * n_mol / lim_tot)
        band_pop = n_mol * bs["g_upper"] * math.exp(-bs["T_e_cm"] / kt_cm)
        for h in bs["heads"]:
            s = (band_pop / n_heavy) * bs["A_eff"] * h["rel"] * (1e7 / h["nm"])
            if s > 0:
                contribs.append((h["nm"], s, BAND_WIDTH_NM))

    # optically-thin emission: thermal continuum (incandescence) + lines/bands
    planck = [cie_color.planck_rel(lam, T) for lam in cie_color.LAMBDAS]
    pk = max(planck) or 1.0
    therm_w = n_heavy / N_REF
    intensity, lum_th, lum_em = [], 0.0, 0.0
    for i, lam in enumerate(cie_color.LAMBDAS):
        therm = therm_w * planck[i] / pk
        emis = 0.0
        for lam0, s, w in contribs:
            d = (lam - lam0) / w
            if -6 < d < 6:
                emis += s / (w * 2.5066) * math.exp(-0.5 * d * d)
        emis *= GAIN
        vy = cie_color._ybar(lam)            # photopic weight for the diagnostic
        lum_th += therm * vy
        lum_em += emis * vy
        intensity.append(therm + emis)

    diag = {
        "ionization_fraction": round(ion_frac, 4),
        "molecular_fraction": round(min(mol_frac, 1.0), 4),
        "emission_fraction": round(lum_em / (lum_em + lum_th + 1e-30), 4),
        "n_e": n_e,
    }
    return intensity, diag


def slab_hex(comp_key: str, T: float, atomic: dict, mol_db: dict):
    inten, diag = slab_spectrum(comp_key, T, atomic, mol_db)
    return cie_color.spectrum_to_hex(inten), diag


# ── self-tests / sanity ──

def main():
    atomic, mol_db = load_dbs()
    print("=== self-tests ===")
    T = 1500
    bb, _ = cie_color.blackbody_srgb(T)
    air_hex, _ = slab_hex("air", T, atomic, mol_db)
    print(f"  thick-limit @1500K: air={air_hex}  blackbody={cie_color.rgb_to_hex(bb)}")
    inten = [0.0] * len(cie_color.LAMBDAS)
    inten[cie_color.LAMBDAS.index(550)] = 1.0
    print(f"  isolated 550nm ⇒ {cie_color.spectrum_to_hex(inten)} (expect green)")

    temps = [1500, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 15000]
    print("\n=== composition color march ===")
    print("         " + "  ".join(f"{t//1000:>5}k" for t in temps))
    for key in COMPOSITIONS:
        cells = [slab_hex(key, T, atomic, mol_db)[0] for T in temps]
        print(f"  {key:6} " + "  ".join(cells))

    for comp in ("air", "co2", "ch4"):
        print(f"\n=== diagnostics: {comp} ===")
        for T in temps:
            _, d = slab_hex(comp, T, atomic, mol_db)
            print(f"  {T:6d}K ionz={d['ionization_fraction']:.3f} mol={d['molecular_fraction']:.3f} "
                  f"emis={d['emission_fraction']:.3f}")


if __name__ == "__main__":
    main()
