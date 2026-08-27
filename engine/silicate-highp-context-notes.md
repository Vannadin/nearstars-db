# Deep silicate — context notes

Decisions taken while carrying the silicate equation of state above 3.5 TPa, and the
reasoning behind them. Appended as the work went.

## The ceiling was never a missing paper; it was a missing row

The brief framed this as research into an unknown regime. It half was. What the search
actually found is that the fit needed had been sitting in a paper this file already reads,
in the section it already quotes for iron.

`fe_eps` stops at 2.09 × 10⁴ GPa because Seager+ 2007 §III.3 says "a Vinet fit up to
P = 2.09 × 10⁴ GPa … we switch to the TFD EOS". Two paragraphs later the same section says
the same thing about silicate: "a fourth order BME fit up to P = 1.35 × 10⁴ GPa. At this
pressure we switch to the TFD EOS." Iron came from Seager and silicate came from Zeng, and
that is the whole reason one ceiling was six times the other.

So the shape of the answer is not "we found a new equation of state". It is **the two
materials were sourced from different papers and only one of them had been read to the end.**

## What the literature says is up there, and why one phase is enough

Umemoto+ 2017 ([arXiv:1708.04767](https://arxiv.org/abs/1708.04767)) gives the sequence from
first principles, at Mg/Si = 1:

| transition | pressure |
|---|---|
| MgSiO₃ post-perovskite → Mg₂SiO₄ + MgSi₂O₅ | 0.75 TPa |
| → Mg₂SiO₄ + Fe₂P-type SiO₂ | 1.31 TPa |
| → CsCl-type MgO + Fe₂P-type SiO₂ | 3.10 TPa |

All three sit **below** 3.5 TPa, inside the range the PREM fit already covers, so none of
them can be spliced in without moving the anchors. And the paper closes the range above:
"The last solid-solid transition identified so far remains the dissociation of Mg₂SiO₄ into
the pure oxides Fe₂P-type SiO₂ and CsCl-type MgO at 3 TPa at low temperatures." That
sentence is why the ladder needed exactly one new rung and not four. It also says the
assemblage above 3 TPa "is the relevant one for the core of Jupiter like planets", which is
mechanism 3's regime named by the same paper.

The honest consequence: the phase is labelled `mgsio3_pv` and what is physically there is
MgO + SiO₂. The licence for using a perovskite fit anyway is compositional, not structural:
Zeng+ 2016 §II notes that the TFD curves of MgO, SiO₂, MgSiO₃ and Mg₂SiO₄ coincide above
~1 TPa because all four have A = 20 and Z = 10, so "Mg/Si ratio does not matter towards the
high-pressure end". That is an argument. It is why the grade drops.

## Candidates rejected, and why

**Zeng+ 2016's own prescription: TFD above 3.5 TPa.** Their §II literally writes
"> 3.5 TPa: TFD EOS of MgSiO₃ calculated using method in (Salpeter & Zapolsky 1967)". This
is the most directly sourced option available and it was rejected on purpose: TFD is not a
material fit, it is the asymptotic theory this recipe declines by name, and implementing it
would erase the boundary rather than move it.

**Seager Table 3's modified polytrope, ρ = ρ₀ + cPⁿ, "valid for P < 10¹⁶ Pa".** Tempting,
because 10 PPa would raise the ceiling by three orders of magnitude. Rejected: it is a refit
of the *merged* Vinet/BME **plus TFD** curve, so adopting it smuggles electron degeneracy in
under a material's name. It is used in the tests instead, as an independent check on the
transcription, which is the honest use of it.

**MgO + SiO₂ as a two-component `Mixture`.** Compositionally the right object, and the
machinery exists from the previous session. Rejected on the numbers: Seager's own MgO row
merges into TFD at log₁₀P = 12.8, i.e. 0.63 TPa, far below the splice, and the mixture takes
the *lowest* component ceiling, so this would have lowered the limit rather than raised it.
No cold ρ(P) fit for Fe₂P-type SiO₂ in one of this file's forms was found.

**Mazevet+ 2015 ([arXiv:1408.3806](https://arxiv.org/abs/1408.3806)) and Mazevet+ 2019
([arXiv:1909.07640](https://arxiv.org/abs/1909.07640)).** Both are DFT-MD at giant-planet
conditions and both are about melting and metallization, not a cold isotherm; 2019's
deliverable is a Simon-law melting fit. Not usable here, but 2019 independently confirms the
dissociation picture and adds that in Jupiter's core the products are liquid, which is a
caveat this recipe cannot represent and does not claim to.

**Wagner+ 2011 (2011Icar..214..366W), Keane and generalized Rydberg forms.** These are the
principled answer to "what functional form behaves correctly at infinite pressure", and they
would be two new forms with parameter sets fitted to their own composition. Rejected for
scope, but their result is the reason to be comfortable here: they report that terrestrial
planet radii to 10 M⊕ differ by **less than 2 %** between three high-pressure-consistent
equations of state. Unterborn+ 2019 ([arXiv:1905.06530](https://arxiv.org/abs/1905.06530))
says the same from the other side: "mass-radius models are more sensitive to bulk composition
than any uncertainty in the equation of state, even when extrapolated to terapascal
pressures."

## BME4 had to be a new form, and finding that out was a two-line check

The brief predicted no new functional form, and that prediction looked right for about ten
minutes. Seager quotes K₀″ = −0.016 /GPa, and the K₀″ that makes a fourth-order BM collapse
into a third-order one is

    K₀″ = −(1/K₀)[(3 − K₀′)(4 − K₀′) + 35/9] = −0.015627 /GPa

which is 2.3 % away. It would be easy to call that rounding and use `bme3`.

It is not rounding. That term enters multiplied by f², and f reaches 1.17 at the fit's
ceiling, so the two curves separate by **9.1 % in density at 13.5 TPa**. A constant printed
to two significant figures is load-bearing here, and `bme3` is not an approximation of it.
Hence `bme4`, with the test measuring the 9.1 % rather than asserting it.

## The seam is the part that makes this trustworthy

Nothing forced the PREM fit and the Seager fit to agree at 3.5 TPa. One is a Birch-Murnaghan
fit to seismic densities in the Earth, the other a fourth-order fit to a DFT calculation of a
crystal, and the papers do not reference each other on this point. They give 14292 and
14263 kg/m³, **0.21 % apart**. That is why the splice carries no density jump: there was
nothing to invent.

The reverse check matters too. Extending the PREM BM2 curve past its stated ceiling does not
merely lose support, it goes wrong in a knowable direction: against Seager's merged curve it
runs +2.5 % at 3.5 TPa, crosses at about 6.4 TPa and is −4.2 % at 13.5 TPa. Since TFD is a
*lower bound* on density (Zeng+ 2016 §II), a curve drifting below it is unphysical, which is
exactly the failure Zeng describes for the Rydberg iron EOS. Zeng's 3.5 TPa is conservative
and correct.

## 6.84 M⊕ was not the mass at which Earth-like rock reaches 3.5 TPa

Verification step 3 asked for the new ceiling. Measuring it turned up something about the old
one that has to be said.

At Earth composition the converged mantle base only reaches 3.5 TPa near **20.7 M⊕**. The
recipe was refusing at 6.84. The gap is the shooting bracket: `shoot` establishes its upper
bracket at four times a uniform-density estimate of the central pressure and integrates
there, and that trial profile drives the mantle base past the ceiling long before the
converged solution would. The refusal was real, the ceiling caused it, and raising the
ceiling is the fix — but "6.84 M⊕" was never a statement about rock.

The new numbers do not have that character. Earth composition stops at 22.78 M⊕ with the
converged central pressure equal to `fe_prem`'s 12 TPa exactly, and pure silicate at
53.38 M⊕ with the centre at 13.5 TPa exactly. Both are the hard bracket cap, i.e. the
material ceiling itself.

**The Earth-composition limit changed hands.** It is an iron limit now, not a silicate one,
which is the physically right owner for a body with a 32.5 % core. Fixing the bracket to back
off on a PhaseGap instead of dying would be a separate, safe change; it is not made here
because it is not this task, and because the ceiling that matters is now reached by the
converged solution rather than by a trial.

## Three mechanisms, three different amounts of opening

The brief's warning was right and worth recording concretely.

| mechanism | before | after |
|---|---|---|
| rocky mass ceiling | 6.84 M⊕ (earth_like), 19.32 M⊕ (pure silicate) | 22.78 and 53.38 M⊕; iron unchanged at 24.92 M⊕ |
| Jupiter's envelope Z | declined at all three Guillot notches | **fully open**: 11 / 26.5 / 42 M⊕ integrate at 4.29 / 4.98 / 5.80 TPa; branch ends at Z = 0.383 |
| compact rock core in a giant | declined outright | **half open**: up to 17.66 M⊕ in a Jupiter-mass giant; Guillot's 19 M⊕ still declines |

The third is the interesting one. What blocks it is no longer what the document said blocked
it. A 19 M⊕ silicate body on its own reaches 3.43 TPa, comfortably inside the new range; put
it under a Jupiter envelope and its base passes 13.5 TPa. The limit is the pair, not the core,
so there is no single core mass to quote.

And mechanism 2 opening did not make it right. Jupiter's radius gets **worse** with Z, from
+0.6 % at Z = 0 to −9.8 % at 42 M⊕, because Helled+ 2022 fitted K to the real Jupiter, which
already contains those heavy elements: adding Z counts them twice. Saturn improves under the
same operation precisely because K was not fitted to Saturn. Meanwhile C/MR² moves the other
way and enters the 0.2634–0.2644 anchor band at the top of the budget. Radius and moment of
inertia pointing at different Z is the diluted-core signature, and this recipe has one
homogeneous Z. Opening the branch turned a refusal into a diagnosis, which is the useful
outcome, not a better Jupiter.

## Related

- [`mixture-context-notes.md`](mixture-context-notes.md) — the previous session, which hit
  this same ceiling from the envelope side and recorded it as "two mechanisms, one ceiling".
  It was three.
- `engine/eos.py`, the `SILICATE` comment — the constants, their tables, and the argument in
  full.
