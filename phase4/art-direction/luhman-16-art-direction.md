<!-- Luhman 16 A/B 비주얼 art-direction Phase 4 스크래치 — 사용자 창작 영역, 미게이팅 -->
# Phase 4 Draft — Luhman 16 A & B Visual Art Direction

**Status:** DRAFT · **Phase 4a creative input** · NOT gated. Gated conclusions
will live in the decision board `../luhman_16.yaml` (being authored); this is
the 4a scratch that feeds it.

## Color direction (owner call, 2026-08-16)

The physical hue family for both bodies is **magenta/violet**, not the
Planck-ember red their Phase 3 reports carried — grounded in the brown-dwarf
regime of
[`stellar-photospheric-color-methodology.md`](../../docs/reference/stellar-photospheric-color-methodology.md)
(Burrows 2001 observed L5; Cranmer 2021 "Brown Dwarfs are Violet"; our
BT-Settl integration, `scripts/refs/bd_visual_color.py`).

- **Owner pick: the soft, R-dominant magenta** — the observed-L5 anchor end of
  the family (`#ff4c6b`–`#ff95ad` hue direction, dimmed for render), i.e. the
  reading closest to blackbody incandescence. Explicitly NOT the saturated
  model violets (`#a300ff` / `#4f20a6`), which stay as the far edge of the
  defensible window (model saturation = upper bound, no T-type blue
  observation).
- **Layered concept (owner, refined 2026-08-17)**: three visual layers —
  (1) below the deck, the hot interior glows **red** at the local gas
  temperature (clearing centers show it directly); (2) the thick cloud body
  reads **dark**, near-non-emitting relative to the interior (cool cloud
  tops; at 1310 K they still glow faintly, so "dark" is relative, not zero);
  (3) **cloud edges/rims glow soft magenta** — the physically right place for
  it, since a thinning cloud column is where light escapes through the
  alkali-carving absorber, and the carved (magenta) spectrum is exactly the
  transmitted light. On B the patchy deck gives many red clearings with
  magenta rims; on A the smoother deck keeps rare seams, mostly dark deck
  with faint magenta edging.
- The two bodies stay color-siblings (1310 vs 1280 K is imperceptible);
  the visual contrast between them remains **texture and weather**, not hue:
  A = quiet, near-featureless dusty ball; B = banded, fast-evolving weather
  world on its 4.87 h spin.
- Magenta at *full* saturation is reserved for the genuinely cold roster BD:
  eps Ind Bb (T6, 910 K), hue anchor `#a300ff`, when its pass comes.

## Open art items

- Concrete cfg hexes (base + accent per body) to be fixed in the board's
  `appearance` rows, superseding the Phase 3 ember `#662400`/`#662200`.
- B's cloud-map treatment: dynamic banded character per Phase 3 (Crossfield
  2014 map as reference, not as a frozen texture).
- Illumination color: keep the 1310/1280 K thermal light for lighting the
  companion (hue of *illumination* is continuum-dominated; the magenta is the
  disk's own perceived color, not the light it casts).
