# Belt `*_compression` / `*_extension` — derivation instead of a copied constant

Goal: replace "copy the class anchor" with a recipe, because Proxima d's belt fills 70 %
of its standoff and inherits Earth's near-symmetric numbers.

- [x] ADS: find the grounding for inner-magnetosphere distortion (Mead 1964 anchor,
      Mead & Fairfield 1975 for the tail currents, Pfitzer 1969 / Öztürk 2007 for the
      outer limit)
- [x] Currency check: is Mead superseded? — still cited 2024–2026 for the *description*;
      its coefficients are superseded by the Tsyganenko family (T02). Recorded in the
      citation entry so a later reader does not have to redo the check.
- [x] Recipe: `ε = (r_core/R_mp)³`, `comp = 1 + ε(comp_pause − 1)`,
      `ext = 1 − ε(1 − ext_pause)`, evaluated at the shell core
- [x] Validation: recovers ROKerbalism Ganymede 1.05 unprompted; reproduces Earth's
      symmetric inner belt; geosynchronous ε 0.29 → 1.36× nightside stretch
- [x] Doc section + ko mirror + citations (`check.sh` green)
- [x] Per-body recompute + comparison cross-section PNG
- [ ] Owner decision: write the derived values into the boards (with the gradient values
      from the same pass), and whether Proxima c's owner-tuned 1.9 gradient stays
- [ ] If adopted: `scripts/viz/render_belts_bodies.py` `*_phys` entries updated (they are
      the single source of truth for fitted geometry) + emitter round-trip check

## Known limits (do not lose these)

- One x-scale per shell, so the recipe can only carry the shell average; the edge value
  (Earth outer ε 0.35 vs core 0.05) is the size of that approximation.
- The interpolation toward the pause shape is a proxy for the asymmetric tail-current
  term, not a derivation of it → medium-low confidence, stated in the doc.
- The giants' shipped 1.05 / 0.9 is unreachable (ε ~0.002). Leaving them as-is means
  keeping a stylistic value; changing them is a visual change to shipped anchors.
