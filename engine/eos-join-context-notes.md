<!-- Brief 41 — 한 Phase 의 밀도 적합과 녹는곡선이 같은 조성·같은 물질상을 말하는지 게이트가 묻게 한다 -->
# Melting curve versus density fit — the join/phase assertion (Brief 41, context notes)

2026-09-03. **§1–§2 are the pre-registration and were committed before the check ran.** §3 is
filled after. Verifiers: (병) parallel seat, (직) directing seat, (여기) work seat.

## 1. The trap, and the two clauses

`eos.Phase` couples a **melting curve** (`melt = "water" | "iron" | "silicate"`, dispatched in
`Phase.t_melt`) and a **density fit** (`form`, `rho0`, `k0`, …) in one frozen object, and
**nothing asserts that the two describe the same thing.** Two clauses, same shape:

1. **Same composition (join).** Brief 38 grounded the eutectic on **Fe–Fe₃S** (Mori+ 2017's
   title, read at source: *"Melting experiments on Fe–Fe₃S system to 254 GPa"*). The queued next
   step was "add an FeS density". Stoichiometric FeS is 36.5 wt % S, Fe₃S 16.1 wt % — different
   joins — and nothing in the code would have objected. Our own identifiers invite it:
   `MORI_FES_EUTECTIC` and `iron_fes_eutectic_t_melt` say "FeS" for the Fe–Fe₃S eutectic.
2. **Same phase of matter.** `fe_prem` is a **liquid** fit — Zeng+ 2016 §II's PREM *outer*-core
   density, and Earth's outer core is liquid (`eos.py` block comment, 여기 read). `fe_eps` is
   the **solid** (pure ε-Fe, hcp, Anderson+ 2001). The engine already carries a solid/liquid pair
   for iron and `core_state` correctly answers liquid verdicts with the liquid member — but the
   distinction lives only in a Korean prose comment; no field records which side a fit was
   measured on.

**Forward condition, recorded now for the Fe₃S paper when it arrives** (직): Thompson+ 2020 is
compression on *solid* Fe₃S, so its K₀ is a solid's — which (Brief 42's K₀ table) biases the core
verdict toward *solid* for an S-rich core. One-sided: it cannot manufacture a liquid core that
is not there, but it must be stated on arrival.

## 2. Design, argued, and the pre-registered outcomes

**Shape chosen: two declared string fields on `Phase` plus one note field, and one gate test.**
`join` — what composition the *density fit* describes, in the fit's own words (from each phase's
`ref`); `fit_state` — `"solid"` or `"liquid"`, which side of the melting curve the fit was
measured on; `join_note` — required whenever `join` differs from the composition the melting
curve is measured on (a module table `MELT_CURVE_JOIN`: water → H₂O, iron → pure Fe,
silicate → mantle rock, peridotitic / A-chondrite solidus). **No taxonomy is invented**: `join`
is free text copied from the fit's provenance, and the check is only *"if they differ, say so
beside the phase"*. That is the same discipline as `melt_scale` on `fe_prem`, made mandatory
and visible. The minimum alternative — a comment at the dispatch — is rejected on this file's
own rule: a comment is not a check, and Brief 39's ⑤ is the precedent (a rule enforced only by
a mode nobody ran).

**Cost**: two defaulted fields on a frozen dataclass (existing positional constructors in
`test_interior.py` are unaffected), fifteen phase declarations copied from their `ref` strings,
one test. `Phase` is not one of `test_ice_giant.py`'s `PATH_FUNCTIONS`; the anchors should be
bit-identical **and the fingerprint unchanged** — verified after, not assumed.

**Pre-registered outcomes**
- ① **No existing material violates it** → the check is a tripwire for future materials
  (Fe₃S first); kept because it costs almost nothing, and said so.
- ② **Some existing material already violates it** → the check earns its place now and the
  violation is the finding.
- ③ **The join cannot be declared without inventing a taxonomy** → the comment is the right
  answer; say so and stop.

**Expectation, registered so it can be wrong (여기)**: ② fires in a *soft* form on two
materials, neither of which is an error but both of which are undeclared bridges today —
`fe_prem` (alloy density, pure-Fe curve, bridged by the declared `melt_scale = 0.80` — already
labelled, so the note will merely name it), and **`silicate`**, whose three density fits are
MgSiO₃ end-member / PREM lower-mantle aggregate / DFT MgSiO₃-perovskite while its melting curve
is a peridotitic or A-chondrite **mantle-rock solidus** (Brief 36) — a join mismatch Brief 36
accepted as "the mantle-rock proxy" without a field saying so. Clause 2 is expected to pass
everywhere once declared: every fit is solid except `fe_prem`, which is the liquid member
`core_state` needs.

## 3. Result — filled after the check ran

*(pending)*
