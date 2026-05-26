# Firefly emitter — context notes

## Why an element-level DB

The Helmenstine 2017 "Plasma Colors of the Periodic Table" chart
(sciencenotes.org, used by the Firefly community as the trace-species
color reference) renders each cell as a gradient-textured tile. The
gradient is decorative — the *intended* color per element is a single
value but the gradient blurs it. Sampling the image pixel-by-pixel
gives noisy results.

The DB at `db/refs/element_plasma_colors.yaml` replaces image-sampling
with explicit per-element hex codes grounded in:

1. **Wikipedia Flame test article** — canonical descriptor + wavelength
   for ~25 elements with classical observation.
2. **NIST Atomic Spectra Database** — dominant visible emission line(s).
3. **Helmenstine chart** — visual sanity check + secondary source for
   elements where chemistry textbooks are silent but flame-test
   experiments have been done (most main-group and some transition).
4. **Legend categories** — explicit no-data state for synthetic
   short-lived isotopes, radioactives whose flame test is unsafe to
   perform, or elements with no visible emission.

Each entry carries a `basis:` line citing the dominant emission line(s)
and a `source:` tag for the canonical reference. Future Phase 3
syntheses and other cfg emitters (Kopernicus AtmosphereFromGround,
Scatterer when authorized) can read from the same DB.

## Sourcing decisions

### When chemistry refs and image diverge

The image's gradient may render a green flame as "checkerboard with
green tint" while the chemistry literature unambiguously says
"emerald green at 510 nm". When that happens, chemistry literature
wins; image is at best a visual sanity check on hue family.

### Wavelength → RGB conversion

Where the only data is "dominant emission at λ nm", I convert via the
piecewise CIE color-matching approximation (Bruton, 1996), then map
the resulting tristimulus to sRGB. This gives a single hex that
*approximately* matches what a clean line at that wavelength looks
like to a normal observer. The result is not perceptually identical
to viewing a flame (which is broadband + thermal continuum), but it's
honest about the spectroscopic basis.

For multi-line emitters (e.g. H has both Hα 656 nm red and Hβ 486 nm
cyan), I pick a perceptually-mixed hex weighted by published line
intensities, NOT a naïve RGB average.

### Status enum

Mirrors the Helmenstine chart's legend, with the addition of explicit
`visible` for the affirmative case:

| status | Meaning | hex |
|---|---|---|
| `visible` | Has a documented flame/plasma emission color | required |
| `no_flame_color` | Element exists, no visible flame color (most transition metals without volatile salts) | null |
| `not_visible_to_humans` | Emission falls outside the 380–780 nm visible band | null |
| `too_radioactive` | Flame test unsafe; spectra not documented under normal lab conditions | null |
| `too_short` | Half-life too short for observation (most superheavies) | null |
| `no_data` | Catch-all for "literature is silent" | null |

## Open questions / deferred

- The Helmenstine chart marks N (Nitrogen) and O (Oxygen) as having
  specific tile colors (pale yellow and blue respectively), but in real
  reentry plasma they band-emit as N2+/N2 (blue-violet) and OI/OII
  (auroral green-red). Phase 3 uses the bulk-gas reentry table for
  these, NOT the atomic flame color. The DB documents both: per-element
  `hex` is flame/atomic emission, and a separate `reentry_note:`
  field flags when bulk-gas reentry diverges.
- For lanthanides where Eu, Tb, Dy etc. have documented flame colors:
  status=`visible` with appropriate basis. The vast majority are
  no_data.
- Should Wood's law (Ritz combination + line-strength priors) drive a
  generated DB rather than hand-curated? Probably not at this scale —
  the chemistry literature is the better source for visible-band
  perceptual color than first-principles RGB synthesis.

## Related

- [checklist](checklist.md)
- [composition-color reference](../../../../.claude/skills/firefly-cfg/references/composition-color.md) — current state of bulk-gas + chart-trustworthy-where tables
