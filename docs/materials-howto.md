# Adding a material by hand

This guide shows how to add a material to the interior solver without an AI and without the engine seats. A material is one YAML file in `solver/materials/`, read by the registry the solver uses. Three commands do the mechanical work. This page covers the judgment calls they leave to you.

You need a terminal in the repository root and the solver's Python (`solver/.venv/bin/python`, written `python` below).

## What a material record is

One record is one data sheet:
- **phases**: each with an equation of state (`eos`), a thermal model, a stability field and a validity window;
- **edges**: what happens just past each window bound;
- **sources**: every number cites where it was read;
- **formula checks**: printed values the checker recomputes from your record.

The record holds what the source prints, in SI, with the printed text beside each number. The solver never guesses: outside what you declare, it refuses by name.

## The three commands

| Command | What it does |
|---|---|
| `python -m solver.materials new <kind> <id>` | Writes `solver/materials/<id>.yaml` with every required field present and commented from the schema. Kinds: `single`, `branched`, `hand_over`, `table`. Every value starts as `FILL`, and the checker refuses a record that still holds one. |
| `python -m solver.materials add-source <pdf> --citation "<author year, title, journal>"` | Hashes the PDF, adds a row to `solver/materials/sources.yaml`, and prints the exact cite block to paste. A cite whose `sha256` is not in that file refuses at load. |
| `python -m solver.materials check <id>` (or `--all`) | Runs every load rule, then the record's generated checks and formula checks. It reports each problem as *field / what is wrong / how to fix*. Exit code 0 means the record loads and its checks pass. |

`check` also prints warnings, such as a source outside the record's primary family. A warning never fails the check, but read it.

## Worked example: solid ε-iron from two cached papers

The goal is a single-phase record for hcp iron from 0 to 100 GPa and 300 to 3000 K. Two cached papers give everything:
- **Seager et al. 2007**, Table 1, row «Fe (ε)»: a Vinet fit with K0 = 156.2 GPa, K0′ = 6.08, ρ0 = 8.30 Mg m⁻³. The table is on page 15 of the cached preprint `2007ApJ...669.1279S.pdf`.
- **Isaak & Anderson 2003**, p.347, text below eq. (4): (αK_T) at 300 K = 12.1 × 10⁻³ GPa K⁻¹, with anharmonic slope 7.8 × 10⁻⁷ GPa K⁻². The file is `2003PhyB..328..345I.pdf`.

For the heat capacity we take the Dulong–Petit limit, 3R/M, as a stated formula.

**1. Scaffold.**
```
python -m solver.materials new single fe_eps_example
```

**2. Register the sources.** The cached PDFs live in the main checkout's `docs/phase3/_papers/`. Run `add-source` once per paper you cite:
```
python -m solver.materials add-source <main checkout>/docs/phase3/_papers/2007ApJ...669.1279S.pdf \
    --citation "Seager, S. et al. 2007, Mass-Radius Relationships for Solid Exoplanets, ApJ 669, 1279"
python -m solver.materials add-source <main checkout>/docs/phase3/_papers/2003PhyB..328..345I.pdf \
    --citation "Isaak, D.G. & Anderson, O.L. 2003, Thermal expansivity of HCP iron at very high pressure and temperature, Physica B 328, 345"
```
What the output means:
- `registered, sha256 …`: a new row was added to `solver/materials/sources.yaml`. That file is now modified; commit it together with your record.
- `already registered (sha256 …)`: the paper was in the manifest already. Nothing changes, and the citation you gave is ignored. It prints no cite block; build the cite yourself as `{cache: <file name>, page: <printed page>, where: <table, eq. or §>, sha256: <the printed hash>}`.
- `provenance stub: <path>`: the provenance note beside the PDF. A cached paper keeps its own note, so nothing is written into the main checkout; for a new PDF outside the cache, a stub is written next to it.

Copy each paper's printed `sha256` into every cite of that file.

**3. Fill in.** Replace the scaffold's body with the record below; it is the scaffold with every `FILL` answered, plus what this material needs beyond the scaffold:
- a `p_max` edge, because the window's upper P bound is finite (the scaffold lists only `t_min` and `t_max`);
- the thermal keys the scaffold leaves commented (`pressure`, `gamma_window`, `phase_constants`).

Write each cite out in full every time it is used, with its own `page` and `where` for that number. `… same cite …` below stands for the full block written again; YAML anchors are not used.

```yaml
id: fe_eps_example
label: solid ε-iron (worked example)
kind: single
system: Fe
fit_composition: pure Fe, hcp
primary_family:
  name: Seager et al. 2007 Vinet fit
  sources: [2007ApJ...669.1279S.pdf]
  reason: the cold curve answers; the I&A constants and the Dulong–Petit c_V are thermal constants, not answering sources
phases:
  - id: fe_eps
    state: solid
    eos:
      form: vinet
      params:
        rho0: {value: 8300.0, unit: kg/m3, grade: read, printed: "8.30 Mg m^-3", source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1, Fe (ε) row", sha256: <printed by add-source>}}
        k0: {value: 1.562e11, unit: Pa, grade: read, printed: "156.2 GPa", source: {… same cite …}}
        k0p: {value: 6.08, unit: "1", grade: read, printed: "6.08", source: {… same cite …}}
      reference:
        kind: state
        p: {value: 0.0, unit: Pa, grade: read, note: "zero-pressure fit", source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1: ρ0 is the zero-pressure density", sha256: <Seager's>}}
        t: {value: 300.0, unit: K, grade: read, note: "room-temperature fits", source: {cache: 2007ApJ...669.1279S.pdf, page: "2", where: "§2: «use experimental data obtained at room temperature»", sha256: <Seager's>}}
        t_ref_kind: isotherm
    thermal:
      source_state: solid
      source_composition: pure-Fe-hcp
      pressure:
        alpha_k: {value: 1.21e7, unit: Pa/K, grade: read, printed: "(αK_T)300 K = 12.1 × 10^-3 GPa K^-1", conversion: "×1e9",
                  source: {cache: 2003PhyB..328..345I.pdf, page: "347", where: "text below eq. (4)", sha256: <from sources.yaml>}}
        alpha_k_dt: {value: 780.0, unit: Pa/K2, grade: read, printed: "7.8 × 10^-7 GPa K^-2", conversion: "×1e9", source: {… I&A cite …}}
        c_v: {value: 446.6539144775719, unit: J/kg/K, grade: declared, note: "Dulong–Petit limit",
              source: {formula: "3R/M, R = 8.314462618 J/mol/K, M = 0.055845 kg/mol"}}
      gamma_window: {p_min: 0.0, p_max: 1.0e11}
      phase_constants: {p_min: 0.0, p_max: 1.0e11, reason: "no thermal set: γ from the phase's own constants over the whole window"}
    field:
      kind: sourced
      box: {p_min: 0.0, p_max: 1.0e11}
      source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1, Fe (ε) row", sha256: <Seager's>}
    window: {p_min: 0.0, p_max: 1.0e11, t_min: 300.0, t_max: 3000.0}
    edges:
      p_max: {refusal: input.material_out_of_data}
      t_min: {refusal: input.material_out_of_data}
      t_max: {refusal: input.material_out_of_data}
formula_checks:
  - quantity: K0 as printed
    state: {}
    expected: 1.562e11
    unit: Pa
    tolerance: 0.0
    tolerance_reason: a transcription check of the printed value
    expression: params.k0
    source: {cache: 2007ApJ...669.1279S.pdf, page: "15", where: "Table 1, Fe (ε) row", sha256: <Seager's>}
```

**4. Check.**
```
python -m solver.materials check fe_eps_example
```
Expected:
```
fe_eps_example.yaml: loads
fe_eps_example.yaml: generated checks and formula checks pass
```

**5. Use it.** The registry now serves the record by its id. Bodies read phase-2 records once the switch-over from the legacy materials is registered; until then, `check` and the tests are where it runs.

What the example teaches:
- **Every record names its primary family** (`primary_family`, required). Here the family is Seager's fit; the thermal constants do not answer ρ, so they are not family sources.
- **Every number has a cite** (`cache`, `page`, `where`, `sha256`) or a stated formula. `printed` holds the text as printed, and `conversion` how you made it SI.
- **The thermal model is required.** A cold curve alone loads, but answers nowhere: γ = αK_T/(ρc_V) is asked at every point, and `check` reports «answers nowhere». With no thermal sets, `phase_constants` must cover the whole γ window with the phase's own `alpha_k` and `c_v`.
- **Every finite window bound has an edge.** Here each bound refuses. A band is allowed only with a stated origin (below).

## Judgment points and the allowed choices

The checker enforces the shapes. These choices are yours, and each has a fixed list of allowed answers.

**The primary family** (design note 4). Choose one self-consistent source family for the material: the one that reaches furthest with ρ, thermal terms and phase fields from one model. Declare it as `primary_family: {name, sources, reason}`; every record must. `sources` lists family keys: a cached file name, or a library pin as cited (`SeaFreeze@1.1.0`). What counts as «answering» is everything the equation of state cites (its params, its reference state, an evaluator's params, a table); thermal constants do not count. A user-declared record has no cached key; name it and list what you used. Every other source is one of:
- **beyond the family's reach**, joined by the taper rules below;
- **a cross-check**, never answering.
A phase the family cannot cover takes **one** source for the whole phase. Say so in `multi_source_reason: {reach: beyond_primary | whole_phase, text}`. A split inside a phase across a T line is not available. The only exception is a source seam between two phases of one family with a nil step (design note 5, below). The checker warns (`material.multi_source`) until the reason is written.

**Two sources in one phase** (impl note 3 Part A). Each source declares `basis` (measured or computed), `data_range` (with page), `sigma` and `sigma_kind`. The overlap is the intersection of their *data* ranges, not their windows. Then pick one of:
- **cross_check**: the preferred source answers. The other is compared on a declared grid, its |Δρ|/ρ goes into the band, and nodes with r > 2 are disclosed by name. It is never gated.
- **blend**: both answer inside the overlap, weighted by a C¹ smoothstep in P only (a T weight is refused). It is **gated**: any node with r = |Δρ|/σ_allow > 2 stops the load as `material.source_conflict`, and so does any node where a side cannot answer. The overlap must lie inside both data ranges, and the sampling box must be the overlap.
- **taper**: outside the measured source's range, a P-only V-blend over P_e → 1.5·P_e (or a declared width with its reason) toward the other source. Use it instead of a density step.
- **seam**: a point join where windows only touch. It is listed by `seams()`, never by `transitions()`.

**When the gate stops** (A6), the allowed answers are:
1. measured beats computed inside the measured range, with seams at its edges;
2. a different source;
3. a narrower window, so the conflicting region becomes a named refusal.

Picking a source's alternative column after seeing the comparison is never allowed.

**σ and sigma_kind.**
- An unprinted σ is `{kind: not_printed, where}` with `sigma_kind: not_applicable`, and contributes 0. There is never a stand-in value.
- A printed CI is converted: ci90 ÷ 1.645, ci95 ÷ 1.960.
- Shared data, where one fit includes the other's points, combines by max; otherwise by quadrature.
- σ may vary by region: `{kind: by_region, regions: […], else: …}`. Where boxes overlap, the smallest value wins.

**Refusal or band at an edge.** Past a window bound the record either refuses (`{refusal: input.material_out_of_data}`) or answers with a band. A band needs `{form, error | method, grade, origin}`, and its origin must be a stated source or method. Without an origin it is a refusal.

**The γ window** (G4). Thermal sets stay inside the source's printed scope (`printed_scope`). Past it, only a declared `edge_above` band up to a stated limit is allowed. Inside the γ window, the sets plus `phase_constants` must cover every pressure, and wherever γ comes from constants both `alpha_k` and `c_v > 0` are required.

**A sourced or a user-declared table** (Part B). A direct table is `eos.form: table` over (P, T), bilinear in (ln P, T).
- Shape: `first` lists the P nodes [Pa] and `t` the T nodes [K], both increasing. Each column (`rho`, `alpha`, `c_p`, optionally `k_t`) is a list of rows, one row per P node, each row one value per T node.
- It must carry **α and c_P columns**, so that dT/dP = αT/(ρc_P) is read and never differentiated (impl note 9). K_T is optional.
- Its thermal block is only `{source_state, source_composition}`: γ and dT/dP come from the columns, so a table phase takes no `gamma_window`, `sets` or `phase_constants` (the checker refuses them).
- Its grid is its window, and each finite window bound needs its edge.
- Maxwell consistency is checked within your declared `maxwell_tolerance`, the relative misfit allowed between α and −∂lnρ/∂T along each isobar (and between ∂c_P/∂P and −T∂²v/∂T²). Set it before running the check, from how finely your table is spaced. `alpha_range: [lo, hi]` declares the sane α range.
- A formula check still applies. For a user-declared table, a transcription check of one node (for example `rho(<phase> @ P=…, T=…)` against the value you entered) with `source: {user_declared: <reason>}` is enough.
- A table from a paper cites it. A table for a fictional or exotic material uses `source: {user_declared: <reason>}`, which grades every output that uses it «declared» and is counted on the boards. It is allowed, never hidden.

**Formula checks and disclosed fails** (C4).
- A check recomputes a printed value from your record. The expression grammar is: constants by path (`params.k0`, `sets[0].c_v`), state values, `curve(boundaries[i] @ T=…)`, `melt_p(a, b @ T=…)`, `rho(<phase> @ P=…, T=…)` and arithmetic.
- The tolerance and its reason are written before you run the check. Never widen them after a miss.
- A check that fails may be carried as a **disclosed fail** only when a cached source *prints* the disagreement, cited with page, and the miss stays within that printed size. A disclosed fail that starts passing is stale and fails.

**Source seams in T** (design note 5). Two phases of one physical substance may meet at a temperature t only when both sides are one family (one formulation, or a cited refit) and their measured step is nil: |Δρ|/ρ ≤ 1e-9, |Δα|/α and |Δc_P|/c_P ≤ 1e-6, global constants you cannot raise. List the lower-T phase first. The upper side owns t.

**The composition source kind** (a body's layer, not a material). A silicate layer declaring oxide wt% gives `source_kind`: `measured` (a paper's value for this body, with grade, source and counter_evidence_searched), `owner_override`, `preset` or `default_bse`. Values are stored as printed, with a printed sum within 100 ± 2 wt%.

## What `check` messages mean

| Message | Meaning and fix |
|---|---|
| `placeholder` | A `FILL` is left. Replace it. |
| `unregistered source` | A cite's sha256 is not in `sources.yaml`. Run `add-source` and copy the printed hash. |
| `edge undeclared` | The field reaches a finite window bound with no edge entry. Declare a refusal or a band with origin. |
| `answers nowhere` | The record loads but refuses at its window's middle. Read the reason: «γ asked …» means there is no thermal model. |
| `formula check «…»: got …, expected …` | Re-read the printed value and its unit. Never widen the tolerance after the miss. |
| `table check` | A table fails a physical check (ρ falls with P, K_T ≤ 0, a hole, α out of its declared range, Maxwell). Fix the data or its declaration, never the check. |
| `source conflict` | A blend's sources disagree beyond 2σ, or a side cannot answer, at a named node. Use one of the A6 answers above. |
| `gamma window` | A thermal set lies past its window or printed scope, the γ window is not covered, or constants lack alpha_k or c_v. |
| warning `multi source` | A source outside the primary family answers in a phase. Write `multi_source_reason`, or use a family source. |

## Never

- Normalise, round or re-fit a printed value. Store it as printed, with `printed` and `conversion`.
- Use a stand-in for an unprinted σ, γ, c_V or range.
- Choose a tolerance, a window, a k or a column after seeing a comparison.
- Edit `db/systems/*.json` or any derived file by hand.
