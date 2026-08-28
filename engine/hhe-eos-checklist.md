<!-- 수소-헬륨 외피 상태방정식 — 할 일 목록 -->
# H/He envelope EOS — plan and checklist

## The plan

Replace the one-constant n = 1 polytrope with the published Chabrier, Mazevet & Soubiran
2019 mixture table, baked at native resolution over the planetary rectangle, wrapped the way
`water_hot.py` wraps Mazevet's water. The table carries ∇_ad, so the same change closes the
temperature hole. Then re-measure the four giants, re-decide the validation-range grade on
the new anchor count, and measure what the interpolation costs in wall-clock.

1. **judgment** → verify: written in `hhe-eos-context-notes.md` before any code — **done, (A)**
2. `hhe_table.py`, generated from the archive in the dev venv → verify: a test regenerates it
   from the distributed file and fails on drift, SKIP when the file is absent
3. `HydrogenHelium` in `eos.py`, duck-typing `Material` → verify: `density`, `phase_at`,
   `cold_phases`, `check_temperature` all answer; `p_max` no longer a polytrope fence
4. the adiabatic gradient reads ∇_ad instead of rebuilding it → verify: `_adiabatic_dtdp`
   prefers a material's own gradient when it has one, and is byte-unchanged when it does not
5. re-measure Jupiter, Saturn (Z = 0 and Z > 0), Uranus, Neptune → verify: numbers in the test
6. re-decide `giant_unvalidated` → verify: the rule states its anchor count and its reason
7. re-measure the two central temperatures → verify: against 5700 / 5500 K (Scheibe+ 2019)
8. cost → verify: seconds per ice-giant solve, before and after
9. docs, ko mirror, `build_docs.py`, `check.sh`

## Checklist

### Before code
- [x] **(A)/(B)/(C)** — (A). The archive is reachable and carries the mixture in (log T, log P)
- [x] Y = 0.275 not Y = 0.292, because `envelope_z` already carries the metals
- [x] the flawed cells located and measured, and the reachable region measured against them
- [x] coarsening measured and rejected — native 0.05 dex or nothing

### The table
- [x] `hhe_table.py` — log ρ and ∇_ad over the planetary rectangle, generated not typed
- [x] the unreachable region left out and named, rather than repaired
- [x] Catmull-Rom bicubic in pure Python interpolation in pure Python, no runtime dependency
- [x] interpolation error measured — ρ 2.0e-3, ∇_ad 9.1e-3 and stated, as `fermi.py` states its own

### The material
- [x] `HydrogenHelium` in `eos.py`; the polytrope's constants stay, with what they are now for
- [x] `cold_phases()` no longer names `hhe_n1`
- [x] out-of-table declines name the mechanism

### The integrator
- [x] `_adiabatic_dtdp` prefers a published ∇_ad when the material has one
- [x] the mass-based demotion removed; the remaining reason is the declared potential temperature, with three anchors named on the new anchor count, with the reason recorded

### Verification
- [x] condensed-phase anchors bit-identical — Earth, Mars, Mercury, Moon, six moons, five icy moons
- [x] Jupiter −0.83 %
- [x] Saturn Z = 0 +7.06 %; the fitting Z fell from 0.200 (19.0 M⊕) to 0.0825 (7.85 M⊕), below the Guillot budget; where the fitting Z moves inside the Guillot budget
- [x] Uranus +5.46 % (was +23.8 %). Neptune declines on the class-based ice dispatch, not on the envelope — were +23.8 % / +29.2 %. **This is the gate**
- [x] Uranus 6158 K against 5700 K. Neptune cannot be re-measured until the dispatch is fixed, so its gap is neither closed nor confirmed re-measured against 5700 / 5500 K; if Neptune's gap
      survives, say so and hand it on as its own task
- [x] temperature flows through the envelope
- [x] cost measured — Jupiter 0.2 → 5.4 s, Uranus 148 → 1038 s
- [x] `bash scripts/check.sh` green

### Docs
- [x] `interior-structure-methodology.md` §Giants replaced (1564 → 1587, +23) — a replacement, not an addition
- [x] ko mirror
- [x] `python3 scripts/build_docs.py`
