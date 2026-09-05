<!-- 유도 자기권 갈래의 근거를 원문까지 되짚은 결과 — 새 규율(방법론 문서는 출발점) 첫 적용 -->
# The induced-magnetosphere branch, checked against the sources — 2026-09-05

First application of the rule the owner set on 2026-09-05: *our methodology documents are the
starting point, not the evidence.* Nothing here changes a document or a value. It records what the
sources say, what they do not say, and which links cannot be checked at all right now.

## What is held, and what is not

`planetary-magnetosphere-geometry-methodology` rests this branch on six papers. **One of them is in
the cache.**

| paper | role in the document | held |
|---|---|---|
| **Egan+ 2019** `2019MNRAS.488.2108E` | the crossover test — a weak dipole is worse than none | **yes** (as arXiv 1907.02978) |
| Bertucci+ 2011 `2011SSRv..162..113B` | the review that names the boundary | no |
| Luhmann 1991 `1991SSRv...55..201L` | the Venus ionospheric field | no |
| Brace+ 1980 `1980JGR....85.7663B` | **the 330 / 700 / 1000 km altitudes → the adopted `1.05–1.2 R_p`** | no |
| Zhang+ 2009 `2009GeoRL..3620203Z` | the boundary vanishes under a radial IMF | no |
| Martinecz+ 2009 `2009JGRA..114.0B30M` | the shape function (dayside circle, nightside line) | no |

Two of the missing links are reachable second-hand through **Edberg+ 2024** (`2410.21856`), which is
held; see below. The other three — including the one the adopted number comes from — are not.

## Egan 2019 says IMB, and never says ionopause

The document writes the test as `R_mp(B_eq) > r_ionopause` and attributes it to Egan. Egan's own
sentence is:

> increasing the strength of a planet's magnetic field enhances ion escape until the magnetic
> dipole's standoff distance reaches the **induced magnetosphere boundary**. After this point
> increasing the planetary magnetic field begins to inhibit ion escape.

and, on the same transition, *"the magnetic standoff reaches the **terminator IMB**"*. The word
**ionopause does not occur in the arXiv version at all** — 0 occurrences, against 13 for the two
spellings of the induced magnetosphere boundary counted together. ⚠ Corrected 2026-09-06: that 13 was
`IMB` (8) and `induced magnetosphere boundary` (6) summed in one grep and reported as if it were one
count, and the two figures below are from the **published PDF**, which reads 1 and 5. Neither number
was wrong about its own file; presenting a combined count as a single one, and then a second file's
count beside it without saying so, is what made the note contradict itself. The document elsewhere joins the two with a slash, *"the **ionopause /
induced magnetosphere boundary**"*, which is where the substitution happens; the authority for that
equation would be Bertucci 2011 or Luhmann 1991, and **neither is held**.

This matters for the branch rather than being a wording quibble, because the number the test is
compared against — `1.05–1.2 R_p` — is a Venus **ionopause** measurement (Brace 1980, absent). If the
two surfaces differ, the test is being run against the wrong one.

Egan also prints a threshold the document does not: for their simulation set the transition occurs at
**`B_P = 50 nT`**. Whether that is portable is a separate question — it is one planet, one wind — but
it is the paper's own number and it is not in our document.

## Edberg 2024 carries two of the missing links, verbatim

- The shape: *"the IMB shape was represented by a circle on the dayside and a straight line on the
  nightside (Martinecz et al. 2009)"* — the document's rendering is exact.
- The range: *"the model of Martinecz et al. (2009) still seems to be valid in the far downtail region
  down to at least 20 R_V, without the need for adjustment of the model parameters"*. The document
  says "found valid to at least 20 R_V unchanged", which is one notch firmer than "still seems to be
  valid"; Edberg notes "a considerable spread in the location of the crossings".
- ⚠ And a piece of context the document does not carry: the Martinecz, Whittaker and Signoles models
  *"were all confined to within 5 R_V, i.e., the orbital limit of Venus Express."* ⚠ The balance to
  that: Edberg prints the agreement as numbers, not only as a verdict — slope −0.097 against −0.101,
  intercept 1.10 against 1.13 R_V, and the IMB position moving only 0.1 R_V out at 20 R_V. Few
  crossings, but the conclusion is quantitative. So the shape
  function is used four times beyond the data it was fitted to. Edberg is what supports it out there —
  which makes Edberg load-bearing, not merely corroborating.

## Second pass, 2026-09-06: the paper itself, and the verdict

The PDF arrived (green OA), and five things in it change the picture. All quotations below were read
out of the cached PDF here, not taken from a summary.

- **The threshold has a number, and it is outside our band.** *"This transition occurs where the
  magnetic stand-off crosses the unmagnetized induced magnetosphere boundary (**847 km**) (Trotignon
  et al. 2006)."* At Mars that is `(3389.5 + 847) / 3389.5` = **1.250 R_p**. Our adopted `1.05–1.2 R_p`
  does not contain it.
- **The single word "ionopause" in the paper is a reference title** — *"Ionopause-like density
  gradients in the Martian ionosphere"* — and even that title says *ionopause-**like***. The body text
  uses IMB throughout.
- **Moving to another star is a rule the paper prints and our document drops.** *"Because Bmax occurs
  when the intrinsic magnetosphere reaches the induced magnetosphere, it will also scale with stellar
  wind pressure as `Bmax ∝ Psw^(1/2)`."* And the other side of it: *"The induced magnetosphere
  boundary has also been shown to depend weakly on dynamic pressure and extreme ultra-violet input,
  but much less so than the intrinsic magnetosphere (Ramstad et al. **2017a**)."* ⚠ This note first
  wrote 2017b inside those quotation marks. Both papers exist and Egan cites both, so it is not a
  typo but the wrong one of two — and 2017a is the one we now hold, so the error would have sent a
  reader looking for a paper we lack instead of opening the one on the shelf.
- **The tested field range is far below our roster.** *"The range of planetary magnetic fields runs
  from unmagnetized to an equatorial surface dipole field of Bp = 150 nT, which corresponds to
  approximately 1/400th of the Earths equatorial surface magnetic field."* Pandora's 75 µT is **500×**
  the top of that range.
- **The transition's location is resolved to 25 nT.** The runs are *"0, 10, 25, 50, 75, 100, 150 nT"*,
  so `B_P = 50 nT` is a grid point as much as a result.

⚠ **`B_P = 50 nT` and Tang's `Rm > 50` have nothing to do with each other.** One is a field strength
in nanotesla, the other a dimensionless Reynolds number. The digits coincide; nothing else does. Both
appear in this engine's notes, so it is written down here once.

### The boundary is a published function of the wind, and it reproduces

Ramstad+ 2017a arrived and was worked through end to end rather than taken on report. Its IMB is a
double conic whose only wind-dependent parameter is `L_n = a·n^b·(v/100)^c + d` (Table 2: 0.59,
−0.30, −0.81, 0.49) with `ε_n 0.95 · x_Fn 1.64 · ε_d 0.57` fixed; `L_d` and `x_Fd` are *not* printed
and come through eqs (7), (8), (5), (6), and the subsolar point is eq (9) `r_SD = x_Fd + L_d/(1+ε_d)`.

Carried through, `(2 cm⁻³, 400 km/s)` gives **`r_SD = 1.2417 R_M`**, reproducing the relayed figure
exactly. ⚠ Eq (6) admits two readings from the text, and only `x_Fd = (ε_d L_d + ξ)/(1 − ε_d²)` works
— the other gives 0.887 R_M, inside the planet's own atmosphere. Worth writing down, because the next
reader will meet the same ambiguity.

⚠ **Two printed-unit defects in that equation block**, both registered in `paper-defects.md` (#20,
#21). The velocity is declared in km/s and the fit needs 100 km/s (130 km if taken as printed), and
the check equation declares its pressure *"in units of nT"* where it must be nPa.

⚠ **State the agreement in the same quantity both times.** Egan's 847 km and Ramstad's 819 km are
**altitudes**, 3.3 % apart; as planetocentric radii the same two numbers are 1.2499 and 1.2417,
**0.66 %** apart. Nothing changed but the quantity, and the apparent agreement moved by a factor of
five. Quote the altitude pair, since that is the form both papers print.

Across the wind range the paper studies, the subsolar IMB runs **1.42 R_p** at 0.031 nPa to **1.16
R_p** at 9.8 nPa — a 110× pressure swing moving the boundary by about ±10 %.

### Verdict: ㉮ — the surface is the IMB, and `1.05–1.2 R_p` is not it

㉯ cannot be supported. The equation `ionopause = IMB` has **no held source** (Bertucci 2011 and
Luhmann 1991 are both absent), and it is not merely unevidenced: Egan's own IMB sits at 1.250 R_p
while the band derived from Venus ionopause altitudes stops at 1.2. The one number we can check falls
outside the band, which is evidence against the equation rather than absence of evidence for it.

㉰ is heavier than the case needs, because **the pressure dependence sits almost entirely on the side
we compute**. `R_mp` carries `P_sw^(1/2)`; the IMB depends on pressure *"weakly … much less so than
the intrinsic magnetosphere"*. So carrying the IMB altitude as roughly fixed while the standoff moves
with the wind is the paper's own division, not our invention.

What the branch should therefore do:

1. **Compare against the IMB**, and stop attributing an `r_ionopause` to Egan — that word is not in
   the paper's body at all.
2. **Anchor the IMB altitude on Egan's 847 km (1.250 R_p at Mars)** as a *declared* value, and say in
   the same breath that it is one body under one wind. ⚠ **Superseded 2026-09-06**: this said the
   altitude was second-hand because Trotignon+ 2006 is not held. Ramstad+ 2017a, which we do hold,
   puts the nominal subsolar IMB at **1.2417 R_p (819 km)** — within **3.3 %** of Egan's 847 km. It is
   not a re-quotation any more; one held paper independently reproduces it, and gives it as a function
   of the wind rather than a constant.
3. **Keep `1.05–1.2 R_p` in the document as what it is** — Venus ionopause altitudes, from an absent
   Brace 1980 — and stop using it as this test's threshold. ⚠ It is also authored at the top: the
   three Venus measurements convert to 1.0545 · 1.1157 · 1.1652, and **1.2 is in none of them**.
4. **Carry `Bmax ∝ Psw^(1/2)` into the branch**, or the criterion is valid only at Mars under one wind.

⚠ **One thing here is the owner's, not the engine's**: whether a single body's boundary altitude may
stand in for every atmosphered body, or whether the branch should refuse until a second measured IMB
exists. That is a `Choice` in C32's sense — two candidates, consequences measured — and it is left
open rather than settled here.

**And the crossover barely touches our roster.** Egan's regime tops out at 150 nT; every magnetised
body on our boards is hundreds of times above it. The "a weak field is worse than none" finding
therefore bears on the **induced candidates** — the bodies we would classify as unmagnetised anyway —
and not on the strong-field ones, where the standoff clears any of these boundaries by orders of
magnitude.

## What follows for the branch

Three things, none of them decided here:

1. **Name the surface the test compares against.** Either the sources support `ionopause = IMB` and
   the document should say so with the paper that supports it, or they do not and the crossover test
   needs the IMB while `1.05–1.2 R_p` describes something else.
2. **The adopted `1.05–1.2 R_p` rests on an absent paper.** It can be carried as *what the document
   prints*, but it cannot be attributed to Brace 1980 by anyone who has not read Brace 1980.
3. **Egan's `B_P = 50 nT` should be in the document** or explicitly declined, with the reason.
