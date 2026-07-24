# Mauk & Fox (2010/2021) 상대론적 Kennel-Petschek 안정포획 전자플럭스 한계를 재현하는 이식 모듈
"""Relativistic Kennel-Petschek (KP) trapped-electron flux limit.

Python port of the Mauk & Fox (2010) Mathematica notebook
(Zenodo 2021zndo...4782323M, files mauk_fox_KP.nb / _run.txt), which itself
implements the relativistic whistler formulation of Summers, Tang & Thorne
(2009, 2009JGRA..11410210S), Appendix A.

Given an equatorial-dipole magnetosphere and a differential electron spectrum
j(E), this computes the marginal-stability parameter CmCk(E) over a sweep of
whistler resonant frequencies, and the KP-limited intensity (j rescaled so the
peak of CmCk touches 1). CmCk >= 1 means the spectrum sits at/above the KP limit.

NOTE on norm1/norm2: the notebook lost the analytic definitions of its 'norm1'
(eta normalisation) and 'norm2' (anisotropy normalisation) from kernel state --
they appear only via ReplaceAll, never with '='. Both are now taken directly from
the published Summers, Tang & Thorne 2009 Appendix A (the paper PDF is cached at
docs/phase3/_papers/summers_tang_thorne_2009_kp_limit.pdf):
  * norm1 = pi * me * (wr - We) / (n_cold * kr)   -- the A2 prefactor
        (pi me / N0) * ((wr - |We|)/k). Matches the notebook's printed
        norm1(0.1 We) anchor (Out[232]) to 7e-7 -- 35x better than the earlier
        single-anchor reconstruction, and it makes wi(0.03 We) and the CmCk
        peak land on the printed values to ~1e-5.
  * norm2 = -kr / (me * (We - wr))                -- the A3 prefactor
        k / (me * (wr - |We|)); identical to the earlier reconstruction.
(History: before the paper was obtained, both were reverse-engineered from the
notebook's printed numbers; the A2/A3 forms confirmed that reconstruction --
the fitted coefficient 3.1582 was pi to 0.5%, the drift being the relativistic
gamma_R in the reconstructed pR0 that the exact form does not carry.)

Per-planet validation: the __main__ self-test reproduces the notebook's Earth
L=5 run exactly, then checks the Mauk & Fox 2010 published per-planet analyses
(their Table 1 spectra + the per-figure B/N/D choices; the paper PDF is cached)
at the factor level their figures support: Earth L=4/6, Uranus L=4.73,
Jupiter L=8.3 (D=3), Neptune L=7.4.
"""
import warnings
import numpy as np
from dataclasses import dataclass
from scipy.integrate import quad, IntegrationWarning

# --- CGS constants (verbatim from the notebook) ---
QE = 4.80e-10      # electron charge [esu]
ME = 9.1e-28       # electron mass [g]
C  = 3e10          # speed of light [cm/s]
KEV_ERG = 1.61e-9  # 1 keV in erg (notebook's conversion constant)

@dataclass
class KPParams:
    """Inputs for one body/L-shell. Field/plasma in the notebook's units."""
    MB: float       # dipole moment [Gauss * Rp^3] (ignored if B_nT given)
    L: float        # L-shell
    Rp: float       # body radius [cm]
    bsub: float     # storm depression subtracted from B [nT]
    n_cold: float   # cold electron density [cm^-3]
    # differential-intensity shape j(E)=Const*E*(kT(gam1+1)+E)^(-gam1-1)/(1+(E/Eo)^gam2)
    Const: float
    kT: float
    gam1: float
    Eo: float       # keV
    gam2: float
    ss: float       # pitch-angle index: angular term (pperp/p)^(2*ss)
    B_nT: float = None   # direct equatorial field [nT]; overrides MB/L^3 - bsub
    D: float = None      # convective growth length in Rp for CmCk; default = L
                         # (Mauk & Fox use D=3 for Jupiter, plasma scale height)


class _KP:
    """Builds all resonance / growth-rate closures for a given KPParams."""

    def __init__(self, p: KPParams):
        self.p = p
        # --- field & plasma (recipe "Field / plasma inputs") ---
        self.B = p.B_nT if p.B_nT is not None else 1e5 * p.MB / p.L**3 - p.bsub  # [nT]
        self.We = QE * self.B * 1e-5 / (ME * C)               # gyrofreq [rad/s]
        self.wpe = np.sqrt(4 * np.pi * p.n_cold * QE**2 / ME) # plasma freq [rad/s]
        self.a = (self.We / self.wpe)**2                      # key cold-plasma ratio
        # spectrum helpers
        self.mec = ME * C
        self.mec2 = ME * C**2
        self.A0 = self.mec2 / KEV_ERG        # 508.696 keV: E[keV] scale
        self.b = 1.0 / self.mec**2           # 1/(me c)^2
        self.K = p.Const / KEV_ERG           # 'Int' front factor (per-erg units)
        self.D0 = p.kT * (p.gam1 + 1)

    # ---- spectrum as a function of momentum p (notebook In[189]-In[198]) ----
    def E_of_p(self, p):
        # invert (p/mec)^2 = (E/mec2)(E/mec2 + 2): positive root, in keV
        return self.A0 * (-1.0 + np.sqrt(1.0 + self.b * p * p))

    def dE_dp(self, p):
        return self.A0 * (self.b * p) / np.sqrt(1.0 + self.b * p * p)

    def Int_E(self, E):
        pp = self.p
        return self.K * E * (self.D0 + E)**(-pp.gam1 - 1) / (1 + (E / pp.Eo)**pp.gam2)

    def dInt_E(self, E):
        pp = self.p
        pw = (self.D0 + E)**(-pp.gam1 - 1)
        br = 1 + (E / pp.Eo)**pp.gam2
        return self.K * (pw / br
                         + E * (-pp.gam1 - 1) * (self.D0 + E)**(-pp.gam1 - 2) / br
                         - E * pw / br**2 * (pp.gam2 / pp.Eo) * (E / pp.Eo)**(pp.gam2 - 1))

    def F(self, p):     # fp = Int/p^2  (In[193]) -- momentum distribution vs |p|
        return self.Int_E(self.E_of_p(p)) / p**2

    def dF(self, p):    # dF/d|p|
        return (self.dInt_E(self.E_of_p(p)) * self.dE_dp(p)) / p**2 \
            - 2 * self.Int_E(self.E_of_p(p)) / p**3

    # ---- fpa2 and its analytic derivatives (In[195]-In[198]) ----
    # fpa2 = F(p) * (pperp/p)^(2 ss),  p = sqrt(ppar^2 + pperp^2)
    def fpa2(self, pperp, ppar):
        p = np.sqrt(ppar * ppar + pperp * pperp)
        return self.F(p) * (pperp / p)**(2 * self.p.ss)

    def dfdpperp(self, pperp, ppar):
        ss = self.p.ss
        p = np.sqrt(ppar * ppar + pperp * pperp)
        ang = (pperp / p)**(2 * ss)
        return ang * (self.dF(p) * (pperp / p)
                      + self.F(p) * 2 * ss * ppar * ppar / (pperp * p * p))

    def dfdppar(self, pperp, ppar):
        ss = self.p.ss
        p = np.sqrt(ppar * ppar + pperp * pperp)
        ang = (pperp / p)**(2 * ss)
        return ang * (ppar / p) * (self.dF(p) - self.F(p) * 2 * ss / p)

    # ---- relativistic whistler resonance (Summers 2009 A4-A8) ----
    def kr(self, wr):                                    # A8: dispersion k(wr)
        return (wr / C) * np.sqrt(1 + self.wpe**2 / (wr * (self.We - wr)))

    def gamR(self, wr, pperp):                           # A4: resonant Lorentz gamma (+ root)
        ck = C * self.kr(wr) / wr
        return (-1 + ck * np.sqrt((ck * ck - 1) * (1 + pperp * pperp / self.mec**2)
                                  * (wr / self.We)**2 + 1)) \
            / ((ck * ck - 1) * (wr / self.We))

    def pR(self, wr, pperp):                             # A5: resonant momentum (can be <0)
        return (ME / self.kr(wr)) * (self.gamR(wr, pperp) * wr - self.We)

    def delR(self, wr, pperp):                           # A6
        return 1 - wr * self.pR(wr, pperp) / (self.mec2 * self.kr(wr) * self.gamR(wr, pperp))

    # ---- Summers A1/A2 integrands, evaluated at ppar = pR(pperp) (In[229], In[248]) ----
    def Integrand1(self, pperp, wr):     # -> the 'eta' resonant integral
        pr = self.pR(wr, pperp)
        return (pperp**2 / self.delR(wr, pperp)) * self.dfdpperp(pperp, pr)

    def Integrand2(self, pperp, wr):     # -> the anisotropy integral
        pr = self.pR(wr, pperp)
        g = self.gamR(wr, pperp)
        d = self.delR(wr, pperp)
        return (pperp**2 / (g * d)) * (pperp * self.dfdppar(pperp, pr) - pr * self.dfdpperp(pperp, pr))

    def _integ(self, func, wr, imult=1000):
        # notebook: NIntegrate over {pperp, 0, imult*|pR(pperp=0)|}; imult=1000 in
        # the CmCk table (integrals are converged well before this limit, so the
        # wide upper bound only triggers a benign slow-convergence warning).
        hi = imult * abs(self.pR(wr, 0.0))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", IntegrationWarning)
            val, _ = quad(lambda x: func(x, wr), 0.0, hi, limit=800)
        return val

    # ---- growth-rate normalisations ----
    def normg(self, wr):   # growth normalisation (In[266]); denom = d(k^2 c^2)/dwr
        return np.pi * self.wpe**2 / (2 * wr + self.wpe**2 * self.We / (wr - self.We)**2)

    def Ac(self, wr):      # critical anisotropy wr/(We-wr) (In[263])
        return wr / (self.We - wr)

    def norm1(self, wr):   # eta normalisation = Summers 2009 A2 prefactor (pi me/N0)(wr-We)/k
        return np.pi * ME * (wr - self.We) / (self.p.n_cold * self.kr(wr))

    def norm2(self, wr):   # anisotropy normalisation = Summers 2009 A3 prefactor k/(me(wr-We))
        return -self.kr(wr) / (ME * (self.We - wr))

    def vg(self, wr):      # group speed (full dispersion form, In[277]; used by CmCk table)
        r = self.We**2 / self.wpe**2
        ck = C * self.kr(wr)
        return C * 2 * r * (ck / self.We) * ((1 - wr / self.We)**2) \
            / (1 + 2 * r * (wr / self.We) * (1 - wr / self.We)**2)

    def wi(self, wr):      # whistler linear growth rate (Summers A1; In[269] assembly)
        t1 = self._integ(self.Integrand1, wr)
        t2 = self._integ(self.Integrand2, wr)
        return self.normg(wr) * self.norm1(wr) * t1 \
            * (self.norm2(wr) * t2 / t1 - self.Ac(wr))

    def cmck(self, wr):    # KP marginal-stability parameter (Summers Eq 21; In[283])
        D = self.p.D if self.p.D is not None else self.p.L
        return self.wi(wr) * D * self.p.Rp / (3 * self.vg(wr))


def kp_cmck(params: KPParams):
    """Sweep whistler resonant frequency and return (E_keV, CmCk) arrays.

    Mirrors the notebook table (In[291]): wr = 0.5*We * 0.93**ii, ii=0..120.
    E is the resonant energy at pperp=0; CmCk is L*Rp*wi/(3*vg)."""
    kp = _KP(params)
    E, cm = [], []
    for ii in range(121):
        wr = 0.5 * kp.We * 0.93**ii
        E.append(kp.E_of_p(kp.pR(wr, 0.0)))
        cm.append(kp.cmck(wr))
    order = np.argsort(E)
    return np.array(E)[order], np.array(cm)[order]


def j_shape(params: KPParams, E_keV):
    """Raw differential intensity j(E) [1/(cm^2 s sr keV)] (recipe 'Spectral shape')."""
    p = params
    E = np.asarray(E_keV, dtype=float)
    return p.Const * E * (p.kT * (p.gam1 + 1) + E)**(-p.gam1 - 1) / (1 + (E / p.Eo)**p.gam2)


def kp_limited_intensity(params: KPParams, E_keV):
    """KP-limited differential intensity at E_keV, plus the raw j(E).

    The KP-limited spectrum is j(E) rescaled so max(CmCk)=1 (Mauk & Fox differential
    limit). Since CmCk scales linearly with the spectrum normalisation Const, the
    rescale factor is simply 1/max(CmCk). Returns (j_limited, j_raw)."""
    _, cm = kp_cmck(params)
    cmck_max = np.max(cm)
    j = j_shape(params, E_keV)
    return j / cmck_max, j


# --------------------------------------------------------------------------
if __name__ == "__main__":
    # Exact Earth L=5 case from the notebook.
    earth = KPParams(MB=0.311, L=5, Rp=6.37e8, bsub=100, n_cold=16.0,
                     Const=2.38e6, kT=0.001, gam1=0.978364, Eo=1748.566,
                     gam2=7.036234, ss=0.3)
    kp = _KP(earth)

    def check(name, got, exp, rtol):
        ok = abs(got - exp) <= rtol * abs(exp)
        print(f"[{'PASS' if ok else 'FAIL'}] {name:28s} computed={got:.6g}  expected={exp:.6g}"
              f"  (rel {abs(got-exp)/abs(exp):.2e})")
        return ok

    allok = True
    # 1. field & plasma
    allok &= check("B [nT]", kp.B, 148.8, 1e-4)
    allok &= check("We [rad/s]", kp.We, 26162.6, 1e-5)
    allok &= check("wpe [rad/s]", kp.wpe, 225624., 1e-5)
    allok &= check("a=(We/wpe)^2", kp.a, 0.013446, 1e-4)

    # 2. spectrum spot-check: (pperp^2+ppar^2)*fpa2*KEV_ERG at E=100 keV, ppar=0 (Out[200])
    Eerg = 100 * KEV_ERG
    pperptest = kp.mec * np.sqrt((Eerg / kp.mec2) * ((Eerg / kp.mec2) + 2))
    jtest = (pperptest**2) * kp.fpa2(pperptest, 0.0) * KEV_ERG
    allok &= check("j spot-check (E=100keV)", jtest, 26292.5, 1e-5)

    # 3. norm1 anchor (Out[232]): the exact Summers A2 prefactor matches to ~7e-7
    allok &= check("norm1(0.1 We)", kp.norm1(0.1 * kp.We), -1.6772188670355305e-18, 1e-5)
    # norm2 anchors (Out[256] norm2*temp2, Out[262] norm2*temp2/temp1)
    n2t2 = kp.norm2(0.1 * kp.We) * kp._integ(kp.Integrand2, 0.1 * kp.We, imult=10000)
    allok &= check("norm2*temp2 (0.1 We)", n2t2, -1.36463e13, 1e-4)
    aniso = kp.norm2(0.9 * kp.We) * kp._integ(kp.Integrand2, 0.9 * kp.We, imult=3000) \
        / kp._integ(kp.Integrand1, 0.9 * kp.We, imult=3000)
    allok &= check("anisotropy A (0.9 We)", aniso, 0.29943, 1e-3)

    # 4. growth rate wi at wr = 0.03 We (notebook In[269] block prints wi = 0.658455)
    allok &= check("wi (wr=0.03 We)", kp.wi(0.03 * kp.We), 0.658455, 1e-3)

    # 5. CmCk peak (~0.608 near E~100 keV; notebook table row 40: 0.607879 @ 102.923 keV)
    E, cm = kp_cmck(earth)
    ipk = int(np.argmax(cm))
    allok &= check("CmCk peak", cm[ipk], 0.607879, 1e-3)
    allok &= check("E at CmCk peak [keV]", E[ipk], 102.923, 1e-2)

    # 6. Mauk & Fox 2010 per-planet analyses (Table 1 spectra; B/N/D from the
    #    per-planet figures; PDF cached). Their published results are figures,
    #    so the targets are factor-level bands read from them:
    #      Earth L=4  (Fig 7): well below the limit          -> peak in [0.1, 0.8]
    #      Earth L=6  (Fig 7): near the limit                -> peak in [0.3, 2]
    #      Uranus L=4.73 (Fig 8, N=5): matched/exceeded      -> peak in [0.5, 5]
    #      Jupiter L=8.3 (Fig 9, N=200, D=3): near the limit -> peak in [0.3, 3]
    #      Neptune L=7.4 (Fig 11, N=0.3): peak ~1 at low E,
    #        but ~30x below near 1 MeV                       -> peak in [0.3, 3]
    #                                                           and peak/cm(1MeV) in [10, 90]
    def band(name, val, lo, hi):
        ok = lo <= val <= hi
        print(f"[{'PASS' if ok else 'FAIL'}] {name:28s} computed={val:.4g}  expected in [{lo}, {hi}]")
        return ok

    def peak(pp):
        Ex, cmx = kp_cmck(pp)
        return Ex, cmx, float(np.max(cmx))

    _, _, pk = peak(KPParams(MB=0, L=4, Rp=6.37e8, bsub=0, n_cold=40, B_nT=376,
                             Const=2.34e7, kT=0.001, gam1=1.290, Eo=1324, gam2=6.714, ss=0.3))
    allok &= band("Earth L=4 CmCk peak", pk, 0.1, 0.8)
    _, _, pk = peak(KPParams(MB=0, L=6, Rp=6.37e8, bsub=0, n_cold=8, B_nT=69,
                             Const=7.96e6, kT=0.001, gam1=1.324, Eo=1715, gam2=5.676, ss=0.3))
    allok &= band("Earth L=6 CmCk peak", pk, 0.3, 2.0)
    _, _, pk = peak(KPParams(MB=0, L=4.73, Rp=2.5559e9, bsub=0, n_cold=5, B_nT=217,
                             Const=6.5e6, kT=0.001, gam1=1.101, Eo=1189, gam2=5.604, ss=0.3))
    allok &= band("Uranus L=4.73 CmCk peak", pk, 0.5, 5.0)
    _, _, pk = peak(KPParams(MB=0, L=8.3, Rp=7.1492e9, bsub=0, n_cold=200, B_nT=747, D=3,
                             Const=1.0e6, kT=0.001, gam1=0.8367, Eo=2546, gam2=1.741, ss=0.3))
    allok &= band("Jupiter L=8.3 D=3 CmCk peak", pk, 0.3, 3.0)
    En, cmn, pk = peak(KPParams(MB=0, L=7.4, Rp=2.4764e9, bsub=0, n_cold=0.3, B_nT=35,
                                Const=5.49e6, kT=5.2, gam1=1.560, Eo=625, gam2=2.745, ss=0.3))
    allok &= band("Neptune L=7.4 CmCk peak", pk, 0.3, 3.0)
    cm1mev = float(np.interp(1000.0, En, cmn))
    allok &= band("Neptune peak/CmCk(1MeV)", pk / cm1mev, 10.0, 90.0)

    print("\n" + ("ALL CHECKS PASSED" if allok else "SOME CHECKS FAILED"))
