# The iron-alloy melting depression — what surveys ⑮/⑰ measured (context notes)

2026-09-02. **Documentation only** — preserving the parallel session's survey results
(H15-core-alloys.md, H17-fes-melting-depression.md, read in the original) in the repo
before the session teardown, so the next seat does not re-run the same investigation.
No code touched; `melt_scale` and `IRON_LIGHT_ELEMENT_FACTOR` are unchanged — **this
note is the grounding Brief 38 consumes, not an adoption.** Verifiers are named per
item: (직) = directing seat reproduced, (병) = parallel session measured, (여기) = this
session.

## 1. The printed eutectic curve — Mori+ 2017 eq. (1), our exact algebraic form

*Melting experiments on Fe–Fe₃S system to 254 GPa*, EPSL 464, 135
([`2017E&PSL.464..135M`](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.464..135M)),
cached, title checked. §3.3 prints a Simon equation for the Fe–Fe₃S eutectic:

    T_m = T_ref · ((P − P_ref)/a + 1)^(1/c),  T_ref = 1348 K @ P_ref = 21 GPa,
    a = 36.5(4) GPa, c = 2.07(1)

**Identical shape to `eos.py`'s `iron_t_melt`** (`t0·(1+(p−p0)/a)^c` — our exponent is
Mori's 1/c ≈ 0.48309). A second `melt` curve, not a scale factor; no interface change.

**Transcription checks, four, all printed by the paper itself** (병, 직 재현): 60 GPa →
1915.0 vs printed 1910 (run #6); 254 GPa → 3541.1 vs 3550 (run #11); 136 GPa → 2681.0
vs "~2700 K at the core–mantle boundary"; **~350 GPa → 4103 vs "~4100 K at the ICB"**.
⚠ Label caution on the last: at the textbook ICB pressure 330 GPa eq. (1) gives
3993 K; the paper's own "~4100 ICB" sits at **~350 GPa on its own curve** — a
labelling detail in the paper, checked before being called a defect.

**Unaudited dependency** (병): the anchor `1348 K @ 21 GPa` is **Fei et al. 2000**,
unobtained — the entire eutectic curve hangs on that single point.

## 2. The measured factor — 0.61–0.70, flat over five decades of pressure

> **Correction (Brief 38 §0, 2026-09-02 — the original text below stands as the record;
> the directing seat wrote both the original headline and this correction).** What this
> section measures is the **Fe–Fe₃S eutectic** — the *floor* of the melting surface, at
> the S-rich eutectic composition, which no roster body runs. It is **not a correction
> to `IRON_LIGHT_ELEMENT_FACTOR = 0.80`**: our 0.80 rides `fe_prem`, the PREM
> outer-core fit — Earth's *actual*, non-eutectic composition, whose liquidus sits
> above the eutectic and below pure Fe. `0.63 (eutectic) < 0.81 (ours) < 1.0 (pure
> Fe)` is a physically correct ordering, not a discrepancy. The check that decides it
> is already in the repo — `core_state.py`'s Sinmyo+ 2019 Earth ICB 5120 ± 390 K: at
> 330 GPa ours ×0.80 gives 5073.7 K (**−0.12 σ**) while Mori's eutectic gives
> 3992.7 K (**−2.56 σ, ~950 K cold**). Swapping 0.80 → 0.65 would break the one
> independent check the recipe has. Same failure class as the day's others: **right
> number, wrong pairing.** The eutectic is stored as a labelled *bound*, and the
> 0.80's *provenance* — not its value — is what Brief 38 repairs.


High pressure, Mori eq. (1) against our own pure-Fe curve (Zhang+ 2015 `IRON_MELT_LOW`;
the pairing is ours, not Mori's) (병): 60 GPa **0.658** · 136 GPa **0.666** · 254 GPa
**0.644** · 330 GPa **0.630**. Independently from Mori's own statement against *its*
reference (Anzellini+ 2013): 0.643 (CMB) / 0.672 (ICB) — the two routes agree.

Low pressure, entirely inside Buono & Walker 2011 (one paper, like-for-like; their
measured eutectic 1263 ± 25 K vs their own polynomial intercepts) (병): 1 bar
**0.698** · 3 GPa **0.675** · 6 GPa **0.614**.

**⚠ The denominator trap — this bit the directing seat on 2026-09-02** (직, 자기
기록): when measuring the factor, the pure-Fe reference is **`FE_EPS` (melt_scale
1.0)**. `FE_PREM`'s melt already carries the 0.80, so using it yields 0.79–0.83 —
a wrong number that looks plausible. Write the denominator into any future
measurement.

## 3. Our 0.80, its provenance, and why it is high everywhere

`IRON_LIGHT_ELEMENT_FACTOR = 0.80` reaches us through Zhang & Rogers 2022, whose own
text calls the 20 % reduction *"artificial"* and part of choices *"fine tune[d] …to
match … Tachinami et al. (2011)"* (survey ⑮, quotes at their place). The origin one
step earlier (직, ADS 페이지 이미지로 판독): Boehler 1996 p. 29 — *"For 8 wt% sulfur,
Stevenson (1981) calculated a melting depression … of ~1100 degrees, by making crude
assumptions on the entropy of melting and assuming ideal mixing."* 1100 K at 330 GPa
against our pure-Fe 6342 K is 17.3 % — our 20 %, rounded. **A 1981 ideal-mixing
estimate; the 2017 measurement at the same pressures is 1500–2000 K, 1.4–1.8× larger.**

**Boehler's "convergence at high pressure" is not supported** (병): the claim is twice
hedged (*"are expected to converge"*), rests on Boehler's own 1993/1995, and the same
paragraph prints Anderson & Ahrens 1995's FeS ICB shock value **4310 ± 750 K** — which
*brackets* Mori's eutectic 3993 K at the same pressure, 22 years and two methods
apart. The depression does not vanish: absolute it grows (546 K @ 1 bar → 1958 K @
254 GPa), fractional it is flat. **So a constant factor is a defensible shape.** *(The original clause here ended "at ~0.65, not 0.80" — superseded by the section-2 correction: 0.65 is the eutectic floor at a composition we do not run, and 0.80, Earth's actual, passes the Sinmyo check at −0.12 σ.)*

## 4. Conditions on the 0.65

① **Sulfur is the largest depressor** — Mori Fig. 6 caption prints the order (Fe–Fe₃S
lower than Fe, Fe–FeSi, Fe–FeO, Fe–Fe₃C; only FeH comparable). 0.65 is the **S-rich
bound**, not a generic alloy value; Si/O/C cores sit between 0.65 and 1.0.
② **No nickel** — Mori's compositions are Fe–S only.
③ **Coverage**: Mori measured 21→254 GPa (self-extrapolated to ~350); Buono covers
1 bar–10 GPa as liquidus polynomials in composition (converting to T(P) needs the
eutectic composition per pressure — a separate read); **10–21 GPa is covered by
neither**. Dante-class pressures (0.26 GPa) are served only by Buono's 1-bar fit.

## 5. Buono & Walker 2011 — the low-pressure polynomials, and eq. (5)'s sign defect

Five printed liquidus polynomials T(x_FeS) at 1 bar/3/6/10/14 GPa (transcribed by 병;
x=0 intercepts rise monotonically 1808.9 → 2093.0 K, and the 6 GPa intercept matches
the paper's own prose "2050 K at 6 GPa" to 6 K). **Eq. (5) (14 GPa) as printed has a
negative constant, −2140.2 — T(x=0) = −2140.2 K, a negative melting point.** Read
+2140.2 it continues the monotone rise past 2093.0. Recorded as a source defect
(paper-defects.md **#10**), not silently fixed; the paper itself says eqs. (2)/(5)
were not used to calibrate its model.

## 6. The density side (survey ⑮) — one scale parameter, and a premise correction

- **Hakim+ 2018** (cached, arXiv:1805.10530) Table 3 + §5.2: M–R curves with **0.8 ρ_Fe**
  are *"almost overlapping"* with FeS, FeSi and Fe₀.₉₅O cores — the composition axis
  collapses to **one density-scale number** on pure Fe (structural twin of melt_scale).
  Underlying alloy EOS = Sata+ 2010, paywalled — held second-hand only.
- **Wicks+ 2018** (Sci Adv, PMC full text): Vinet fits for Fe-7Si/Fe-15Si with printed
  V₀·K₀·K₀′; transcription-checked against its own "compression 2.5" and "17–18 g/cm³
  at 1300 GPa" (병; ρ₀ from stoichiometry is derived, marked as such). Ambient ratios
  0.896/0.864 ρ_Fe land inside Hakim's 0.8–0.9 bracket — genuine cross-check (mutual
  citations checked: 0). Scale factor drifts: good to ~1 % below 330 GPa, ~7 points
  off by 1.3 TPa.
- **Premise correction the survey found (⑮ §0)**: `earth_like` already runs on
  `fe_prem` (= 0.849 ρ_Fe at ambient — lighter than Fe-7Si below 1 TPa), so **the
  Dante −12.5 % measurement was already alloy-equivalent in the core; core alloying
  cannot be what that deficit was.** (Consistent with our own Brief-35-followup
  finding that the family's 2,620 constant is the culprit.)

## 7. Blocked list (owner-request candidates, from ⑮ §5)

Mori+ 2017 · Buono & Walker 2011 (both since obtained and read — the two rows above);
still blocked: **Sata+ 2010** (load-bearing under Hakim's table), Fischer+ 2014,
Komabayashi 2014, Noack+ 2020, Chen+ 2008, **Fei+ 2000** (Mori's single anchor point —
**unobtained, load-bearing, and contradicted at the pressure where it is load-bearing by a paper we
hold**; §8 below. Not on the request list: the list closed 2026-09-03 and stays the owner's).
Three of these answer 403 to plain fetches while marked OA — bot checks, not paywalls;
not worked around.

Gate delta 0 (nothing new executes — prose only); anchors untouched by construction.

## 8. Two Pommier papers, owner-fetched — what they change and what they do not (Brief 58)

Quotes verbatim from the cached PDFs (c4 read, 직 re-read, 여기 re-grepped `pdftotext` before writing).

**① `IRON_FES_GAP_REASON` (10–21 GPa) now has two measured points inside it — and does not
close.** Pommier, Laurenz, Davies & Frost 2018 (`2018Icar..306..150P`,
[ADS](https://ui.adsabs.harvard.edu/abs/2018Icar..306..150P)): *"Experiments were performed at high
temperatures (1400–1850 °C) and high pressures (14 and 20 GPa) using a multi-anvil apparatus."* Both
pressures are inside the refused interval. It does not close it: the eutectic values it prints
(*"about 15 wt.% S at 20 GPa and 18 wt.% S at 14 GPa"*) are a **citation** to Fei+ 2000,
Chudinovskikh & Boehler 2007, Chen+ 2008a and Buono & Walker 2015, not its measurement — its own
samples are *"containing mostly 1 and 5 wt.% S (and a few on FeS)"*, deliberately below the eutectic
(it studies the snow regime); and two pressures are points, the hole is an interval. The gap reason
in `eos.py` now says so.

**② Fei+ 2000 is contradicted where it is load-bearing.** Verbatim: *"The determination of the
liquidus curve from our data at 20 GPa and about 5 wt.% S does not agree with the predicted liquidus
curve from Fei et al. (2000) at 21 GPa: for this composition, Fei et al. predicted a liquidus
temperature of 1900 °C, while an additional data point from our experiments suggests a temperature of
1700 °C (±50) that would be consistent with a sigmoidal shape of the liquidus curve."* A shape
dispute, not an offset — the field *"suggested either a parabolic (Fei et al., 2000) or a sigmoidal
shape (Chen et al., 2008a)"* and this paper concludes *"our results show the liquidus curve is not
parabolic"*, with a steep slope between 2000 and ~1600 °C. Mori's 1348 K @ 21 GPa anchor is Fei's;
obtaining Fei would yield two disagreeing sources, not a settlement. Provenance fact, not
corroboration: the paper cites **our** melting-curve source — *"The eutectic composition is expected
to have more than ≈13 wt.% S over the entire depth of the Martian core (Mori et al., 2017)."*

**③ Electrical conductivity stays refused, now with a measured reason.** Pommier 2018
(`2018E&PSL.496...37P`, [ADS](https://ui.adsabs.harvard.edu/abs/2018E%26PSL.496...37P)) is point
measurements, not a law — no Arrhenius form, no fitted σ(P,T); its own words: *"It is presently
unknown which scaling law applies to what terrestrial body, and new parameterized modeling studies …
are required."* Range *"up to 8 GPa and 1850 °C"* — an order of magnitude below Mars' centre
(~40 GPa) and two below our bodies. Values with their conditions, not to be used without them: at
**4.5 GPa**, Fe-5 wt.% S under equilibrium crystallisation *"from about 300 to 190 microhm-cm,
depending on temperature"*; liquid FeS *">10 times more resistive than Fe-5 wt.% S"*; compositions
Fe, Fe-5 wt.% S, Fe-20 wt.% S, FeS, FeSi₂. Same shape as the thermal refusal — points where a front
was wanted, in a domain that does not reach the consumer.

**④ Shared-author dependency.** The Icarus paper's third author is Christopher J. Davies, first
author of the iron-snow paper `2018E&PSL.481..189D` (Davies & Pommier 2018, *Iron snow in the
Martian core?*). Agreement between these melting relations and that snow model is **internal
consistency, not corroboration**. ⚠ The snow branch has **no engine documentation** today — the
paper is in the cache with provenance only; this paragraph is where the fact lives until a snow row
exists, so nobody counts the pair as two sources.

