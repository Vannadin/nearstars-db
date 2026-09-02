# The Militzer 2024 carbon/water deposit — what survey ⑯ established (context notes)

2026-09-02. **Documentation only** — preserving the parallel session's survey ⑯
(H16-carbon-deposit.md, read in the original) in the repo before the session teardown.
No code touched. Verifiers: (병) = parallel session measured, (직) = directing seat.
Paper: Militzer 2024 (PNAS 121, e2403981121; `2024PNAS..12103981M.xml` cached; deposit
= Zenodo record 13937364, seven files, in the worktree cache).

## 1. The deposit is 2 of 7 — a real gap, and the hypothesis that it was enough is refuted

The paper's Results, at its own location, says the intermediates were **simulated**:
*"we **performed** ab initio simulations of O₈₄H₂₂₆, O₈₄H₂₈₂, and O₈₄H₃₉₆ … we
**conducted** simulations of C₄₈N₁₂, C₄₈N₁₂H₅₈, C₄₈N₁₂H₁₁₄, and C₄₈N₁₂H₂₂₈ … The
density is then derived via interpolation as a function of pressure, temperature, and
hydrogen fraction."* Two interpolations exist and must not be conflated (the earlier
brief conflated them — corrected by ⑯): (i) hydrogen fraction along the radius
(structural), (ii) **density between simulated compositions** — the second is the one
that needs the intermediates, and they are simulations, not derivations.

**Deposited: `O₈₄H₂₂₆` and `C₄₈N₁₂` only — one point per axis** (the carbon one at the
H = 0 end), so **there is nothing to interpolate along**; Fig. 5's layer model cannot
be rebuilt from the deposit. The third file (`EOS_H2O-NH3-CH4.txt`, 84O+12N+48C+396H)
is the homogeneous pre-separation mixture — not one of the seven. Every row of every
file was parsed (병): no file mixes compositions; the `logU2/logN2_layers` files carry
**no composition and no temperature** (8 columns of radial structure, 513 spheroids
each) — a confirmed negative, though their ρ(P) columns are a usable published profile
pair for U/N under the standing condition that they are the *fit-target* model
(the neighbouring harmonics reproduce measured J₂/J₄ to all printed digits), i.e.
"consistent with", never "constrained by".

## 2. Grid completeness, cell-counted (병)

| file | T × ρ grid | filled | P coverage |
|---|---|---|---|
| `84O+226H` | 4 × 6 | **24/24 = 100 %** | **197.8–571.1 GPa** |
| `12N+48C` | 6 × 9 | 38/54 = 70 % (ragged) | 32.2–1126.0 GPa |
| `H2O-NH3-CH4` | 12 × 11 | 57/132 = 43 % (5 of 12 T-rows have ≤2 points) | 57.8–688.0 GPa |

The only clean rectangular grid (`84O+226H`) has **exactly 4 temperature nodes — the
width of a 4×4 stencil, zero margin** (no extrapolation guard, no interior/edge
distinction — a hard constraint on any bake), and covers under half of the ice-giant
mantle span (~34.5–1000 GPa); below 198 GPa the water side of the deposit has nothing.
The other two files need scattered-data fitting, a different tool from our stencil.

## 3. The factor-of-2 defect (paper-defects.md #9)

Eq. [3] defines H₁ = N_H/(2N_O) (read from raw MathML — unambiguous), and the prose +
Table 1 agree with it; **the three water-side simulation labels are exactly 2× that
scale** (O₈₄H₂₂₆: eq-[3] value 1.345, printed 2.69; likewise H₂₈₂, H₃₉₆). Control: the
C-N-H fraction eq. [2] reproduces its labels exactly, so the defect is isolated. It is
load-bearing because the interpolation axis IS the hydrogen fraction — anyone placing
the deposited file on that axis meets both values in the same paper.

## 4. C₈N₂H₈ (Uranus' C-N-H layer bottom, Table 1) is not obtainable from the deposit

Scaled to the cell it is C₄₈N₁₂H₄₈ (H₂,₃ = 0.2105) — **not among the simulated set**
(0, 0.254, 0.5, 1), so even the paper interpolated it, between H = 0 and H = 58. The
deposit holds only H = 0, which gives a **density floor** for the layer, not the
composition the model sits at.

## 5. The ask — five files by name, author contact (not a re-download)

`unzip -l` of the local record (no network) lists exactly seven files, 130,650 bytes —
**the five compositions were never deposited** (and the embedded indices `OH_02` /
`CNH_03` imply an author-side numbering with other members):

    O₈₄H₂₈₂ · O₈₄H₃₉₆ · **C₄₈N₁₂H₅₈ (priority — the one file that turns the carbon
    layer from a point into an interpolable segment, and the one C₈N₂H₈ needs)** ·
    C₄₈N₁₂H₁₁₄ · C₄₈N₁₂H₂₂₈

Initiating contact is the owner's call — recorded, not begun.

## 6. Where survey ⑰ changes this note's conclusion

⑰ (Fe–S melting) landed with a printed curve replacing a convention — the analogous
question here is whether **linear mixing** across the hydrogen-fraction axis is
grounded enough to substitute for the missing files. If a grounded mixing rule stands,
the gap above is *replaced*; if not, the author ask stands. That determination was not
made by ⑯ and stays open.

Gate delta 0 (prose only; nothing new executes); anchors untouched by construction.
