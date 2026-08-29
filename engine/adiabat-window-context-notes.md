# The adiabat's validated window — context notes

## The source, and what was read from it

Noack & Lasbleis 2020, A&A 638, A129 (2020A&A...638A.129N, doi 10.1051/0004-6361/202037723),
open access, fetched by the owner into `docs/phase3/_papers/2020A&A...638A.129N.pdf`. Text
extracted with `pdftotext -layout` into the scratchpad and every equation located by its
number in the layout. What was transcribed (their numbering):

| eq. | statement | constants |
|---|---|---|
| (8) | R_p [km] = (7030 − 1840 X_Fe)(M/M⊕)^0.282 | exponent "within the literature range (0.26−0.3)" |
| (9) | R_c,hot [km] = 4850 X_CMF^0.328 (M/M⊕)^0.266 | |
| (13), (14) | g_0 = G M/(R_p·1000)², g_CMB = G X_CMF M/(R_c·1000)² | G = 6.67384e−11, M⊕ = 5.972e24 as printed |
| (15) | g_m,av = (g_0 + g_CMB)/2 | |
| (18) | α_m,av = (13 + 0.738 X_CMF − 11 (M/M⊕)^0.04) × 10⁻⁵ K⁻¹ | |
| (19) | C_p,m,av = 1275 − 585 #FeM^1.06 J/kg/K | |
| (22) | T_CMB,cold = T_um exp(dT g_m,av α_m,av / C_p,m,av (R_p − R_c,hot − D_l)·1000) | T_um = 2000 K "for simplicity", D_l = 250 km, dT ≈ 0.5 |

Validity: "We limited our mass range to two Earth masses, to be in the confidence interval
of the EoS selected" (§2.2) and "planets with masses between 0.8 and 2 Earth masses"; the
paper says its laws "can be extrapolated up to approximately five Earth masses" but that is
their extrapolation, not their validation, and it is not used. Earth-like reference: iron
content 0.35, mantle iron number #FeM = 0.1 ("best resembles Earth's interior structure").
Eq. (17), the mantle Grüneisen law, is not needed by (22) and was not transcribed.

**Eqs. (20) and (21) were excluded on purpose.** T_CMB,hot and T_CMB,warm are the initial
temperatures just after the magma ocean, on the Stixrude 2014 melting curve, and the paper's
own argument is that they exceed literature values by thousands of kelvin. They are a claim
about early planets; putting them beside eq. 7 would be a category error.

## Two comparisons, because the anchors differ

Eq. (22) starts from 2000 K at 250 km depth; this recipe and Unterborn's eq. 7 start from a
1600 K potential temperature at the surface. So two things were measured:

- **(A)** eq. (22) as printed against the engine's CMB temperature — in the engine's own
  geometry (its R_p and R_c, so only the adiabat is being compared) and in the paper's
  (eqs. 8 and 9 with X_Fe = 0.35, X_CMF = 0.325);
- **(B)** the exponential factor of eq. (22) against the engine's own rise T_CMB / T(250 km),
  the engine's mantle temperature at that depth read off the silicate density calls of one
  re-integration at the solved centre, at the hydrostatic pressure ρ_um g h.

| M (M⊕) | R (R⊕) | engine T_CMB | (22) engine geom. | Δ | (22) paper geom. | Δ | eq. 7 | Δ | T(250 km) | rise engine | rise (22) | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.8 | 0.942 | 2430 K | 2485 K | −2.2 % | 2536 K | −4.2 % | 2503 K | −2.9 % | 1725 K | 1.409 | 1.243 | +13.4 % |
| 1.0 | 1.003 | 2526 K | 2563 K | −1.4 % | 2622 K | −3.7 % | 2642 K | −4.4 % | 1736 K | 1.455 | 1.282 | +13.5 % |
| 1.2 | 1.056 | 2611 K | 2637 K | −1.0 % | 2702 K | −3.4 % | 2767 K | −5.6 % | 1747 K | 1.495 | 1.319 | +13.4 % |
| 1.5 | 1.123 | 2724 K | 2742 K | −0.7 % | 2814 K | −3.2 % | 2936 K | −7.2 % | 1760 K | 1.548 | 1.371 | +12.9 % |
| 2.0 | 1.216 | 2884 K | 2906 K | −0.8 % | 2984 K | −3.3 % | 3186 K | −9.5 % | 1779 K | 1.621 | 1.453 | +11.6 % |

Readings:

- The Earth point in the engine's geometry is **2563 K**, against the 2562 K the parallel
  survey reported from its own arithmetic — an independent transcription check.
- (A): the engine sits 0.7–2.2 % under eq. (22) and 2.9–9.5 % under eq. 7, and the two
  published estimates disagree with each other by 0.7 % at 0.8 M⊕ rising to 9.7 % at 2 M⊕.
  The engine is between them everywhere from 1 M⊕ up. The paper's own geometry moves
  eq. (22) up by ~2 % (their R_p is 1–2 % larger than the engine's for the same mass).
- (B): the engine's rise from 250 km to the CMB is 12–14 % steeper than the paper's damped
  exponent, and its temperature at 250 km is 13 % below the paper's 2000 K. The absolute
  agreement in (A) is therefore partly a cancellation. That is stated, not absorbed: the
  paper's `dT = 0.5` is an empirical correction for using mantle-averaged g, α and C_p in a
  profile whose slope is steeper in the upper mantle, and 2000 K is their simplification —
  neither is a measurement of Earth's adiabat. Both numbers are pinned by the test.

## What the grade rests on now

Above 1.05 R⊕ the note no longer says "unchecked". It says: two anchors, disagreeing with
each other by up to 9.7 %, engine between them, within 2.2 % of one; still analog, because
`core_state` consumes the number and the spread is the honest width. At 2 M⊕ (1.22 R⊕) the
second anchor ends by the paper's own limit, and above it the recipe has Unterborn's cubic
alone to 1.5 R⊕ — a stated boundary.

## What moved

No solved number. The check is test-side (`test_interior.py`: constants `NL2020_*`, the
functions, `--adiabat`, and three banded assertions). The grade note in `solve` changed its
text, so the ice-giant anchor was re-frozen — fingerprint only, values bit-identical. Gate
cost: five more rocky solves with a declared temperature plus five short re-integrations,
about a minute.
