# The ice giants' C/MR² against publication — checklist

Task from the directing session, 2026-08-31: `nmoi` is bit-compared against the frozen
anchor but never against a published value; find published C/MR² with sources and
assumptions, put the comparison in the gate, and write the Δ down however large it is.
**A check, not a change** — if the anchor moves, something is miswired.

- [x] Find published C/MR² with sources → verify: values read from cached full texts, not
      made; identifiers checked by title (Nettelmann+ 2013 `2013P&SS...77..143N`
      arXiv:1207.2309; Neuenschwander & Helled 2022 `2022MNRAS.512.3124N` arXiv:2203.02233)
- [x] Settle the normalization from the text → verify: N13 footnote 2 prints
      λ = I/(M_p R_mean²); NH22 §3.6 prints MoI = I/(M a²) — different radii, conversion
      required before any comparison
- [x] State the load-bearing assumption → verify: the rotation period (P_Voy vs P_HAS)
      moves the published value −3.3 % (Uranus) / +6.0 % (Neptune); both hypotheses recorded
- [x] Put the comparison in the gate → verify: `--table` gains `C/MR² published` and `Δ`
      columns; the live/fast paths print the Δ block; the only FAIL-able assertion is the
      two-source consistency after conversion (transcription check), Δ itself has no
      tolerance
- [x] Anchor untouched → verify: full gate run passes with zero diff on
      `ice_giant_anchor.json`
- [x] Methodology doc (en + ko) gains the published C/MR² block and the two citations
- [x] Report to the directing session with the measured Δ
