<!-- Saha/Boltzmann LTE 플라스마 발광색 엔진 — 손맛 가중치 w(T)를 1차원리 계산으로 대체하는 작업 계획 -->
# Plan — Saha/Boltzmann LTE plasma-emission color vs temperature

Replace the hand-tuned blend in `build_plasma_temperature_colors.py`

```
combined(T) = (1-w)·continuum(T) + w·emission      # w(T): hand-set 3000→9000K ramp
```

with a **first-principles LTE isothermal-slab spectral synthesis**, so the
color-vs-temperature emerges from physics and the synthetic `emission_weight`
disappears.

## The model (isothermal LTE slab)

```
I_λ(T) = B_λ(T) · (1 − exp(−τ_λ))
τ_λ    = L · [ Σ_lines κ_line(λ;T) + κ_cont(λ;T) ]
```

Why this shape — it is the standard emergent intensity of a uniform slab and it
**physically interpolates** the two regimes the old model glued together:

- **τ ≫ 1** (dense / thick column) → `I_λ → B_λ(T)` = exact blackbody. Recovers
  the low-T incandescence glow (ember red, lava orange) with no fudge.
- **τ ≪ 1** (thin plasma) → `I_λ → B_λ(T)·τ_λ` = optically-thin emission; line
  peaks stand out over a weak thermal continuum. Recovers reentry/discharge
  emission color.
- The crossover is **computed**: line opacity `κ_line` rises with T as Saha
  ionization + Boltzmann excitation populate the transition's lower level, so
  the molecular→atomic→ionic color march is per-composition, not a global ramp.

The single free parameter is the column `L·n` (optical-depth scale). It is a
real physical knob (density × path), fixed + documented, optionally rendered at
2–3 tiers (thin / medium / thick).

### Physics pieces

1. **Dissociation equilibrium** (law of mass action) — `K_diss(T)` from bond
   dissociation energy + molecular/atomic partition functions → molecular vs
   atomic number fractions. Computed, not assumed.
2. **Saha equation** — ionization balance per stage; solve for `n_e`
   self-consistently (charge neutrality) at fixed total pressure `P`.
3. **Boltzmann** — level populations within each stage; partition function
   `U(T) = Σ_j g_j exp(−E_j/kT)` from a curated low-lying level list
   (truncated; documented).
4. **Line opacity** — `κ_line ∝ f_lu · n_lower · φ(λ) · [1 − exp(−hν/kT)]`,
   with `f_lu` from NIST `A_ki` via `f_lu = (g_u/g_l)(m_e c / 8π²e²) λ² A_ul`.
   Profile `φ`: Doppler Gaussian at T (visual width floor a few nm; color is
   CMF-integrated so exact profile is unimportant).
5. **Continuum opacity** — free-free (Kramers) + neutral bound-free (hydrogenic
   approx). Minimal but real; document.
6. **Molecular bands** — kept (so the iconic reentry green / violet survive) via
   a **band-as-effective-line** approximation: each band system = one or a few
   effective transitions at the band heads, upper energy `T_e + vibrational`,
   an effective band strength, populated by Boltzmann × the molecular fraction
   from step 1. Documented approximation.
7. **Color** — integrate `I_λ` over 360–830 nm against CIE 1931 (Wyman 2013
   analytic CMF, already in repo) → XYZ → sRGB, hue-normalized (max-channel) →
   hex. Same as the existing pipeline.

## Key decisions (defaults chosen; flagged for the user)

- **D1 Pressure / column.** Saha needs a density. Default reference `P = 1 atm`;
  render emission at 2–3 column tiers (thin/medium/thick) + document sensitivity.
- **D2 Molecular bands kept** via band-as-effective-line (vs atoms-only, which
  would lose the reentry C₂-Swan green / CN-violet). Weight = computed
  dissociation fraction.
- **D3 Atom set = H, He, C, N, O** (+ first ions) — covers all 6 current
  compositions. S / SO₂ deferred to the breadth-expansion track.
- **D4 LTE only.** Valid for dense reentry/flame plasma. Auroral non-LTE
  (electron-impact) is explicitly out of scope — aurora stays curated.

## Honesty after the change

The `# MODEL — not ab-initio` header is replaced by an **explicit assumption
list**: LTE, isothermal uniform slab, fixed column, truncated partition
functions, Doppler-only line profile, band-as-effective-line for molecules,
free-free+hydrogenic-bound-free continuum. Everything else (Saha, Boltzmann,
line f-values, CIE) is first-principles.

## Stages

1. **Engine + CIE refactor** — extract `cie_color.py` (Planck + CMF + XYZ→sRGB,
   shared with old builder); write `saha_boltzmann.py` (partition fns, Saha
   solver, Boltzmann pops, line+continuum opacity, slab `I_λ`, → spectrum).
   Unit limits: τ→∞ ⇒ blackbody; single strong line ⇒ that line's hue.
2. **Atomic data** (delegate, verify) — `db/refs/atomic_lines.yaml`: per species
   H I, He I, C I/II, N I/II, O I/II — ionization energies, partition-level list
   `{E_cm,g}`, strong visible lines `{nm, A_ki, E_upper_cm, g_upper, g_lower}`.
   Source NIST ASD. Verify anchors (Hα A=4.41e7; O I 777.4; He D3 587.6; χ_H=13.6,
   χ_He=24.6, χ_C=11.26, χ_N=14.53, χ_O=13.62 eV).
3. **Molecular band data** (delegate, verify) — `db/refs/molecular_bands.yaml`:
   N₂ 1P/2P, N₂⁺ 1NG, CN violet, C₂ Swan, CH, NH, OH, H₂ — band heads, `T_e`,
   effective strength, dissociation energy. Source Pearse&Gaydon / NIST molec.
4. **Wire compositions** — map the 6 compositions → species mix → engine; emit
   YAML with the existing color fields + new diagnostics (ionization_fraction,
   molecular_fraction, tau_peak, dominant_species); drop `emission_weight`.
5. **Render + validate + verify** — update tooltip/caption + assumption note in
   `render_color_visualizer.py`; add `validate_plasma_temp.py`; wire `check.sh`;
   regenerate `docs/firefly-colors.html`; verify colors vs anchors + existing
   curated reentry hexes (sanity, not bit-equality); `./scripts/check.sh` clean.
6. **Docs + commit** — refresh YAML/script headers, `docs/reference/tools.md`
   (+ ko), this workspace; semantic commit per stage.

## Delegation (token discipline)

Stages 2 & 3 (NIST / literature pulls) → subagents; main writes the engine,
wires it, and **verifies** against anchors + existing curated hexes. Spawn the
two curation agents in parallel.

## Related
- [checklist](checklist.md)
- [context-notes](context-notes.md)
- [composition-color reference](../../../../.claude/skills/firefly-cfg/references/composition-color.md)
- old builder: `scripts/refs/build_plasma_temperature_colors.py`
