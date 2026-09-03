<!-- C19 — body_age → dynamo_giant via cooling_luminosity 간선. 코드가 실제로 무엇을 소비하는지 측정한다. 사전등록 → 실행 기록 -->
# Body age and the giant-planet dynamo (C19) — context notes

2026-09-04. **§1–§2 are the pre-registration, committed before any measurement ran. No expectation is written.**

## 1. What the edge says, and what the code says

`chain.yaml:644`: `body_age → dynamo_giant, kind: requires, via: cooling_luminosity, status: gap, ref:
planetary-dynamo-scaling.md:34`, note (2026-09-03): *"the graph was more optimistic than the module —
`dynamo.py` writes that it refuses to supply L(M, age) from an unverified cooling track and the brown-dwarf
branch returns out_of_domain. The code is right and this mark was missing."*

Read before measuring — `dynamo.py` has **two** age-bearing branches, and the `via` names only one of them:
- **giant, 0.3–13 M_J, age ≥ 0.2 Gyr** (`dynamo.py:122–135`): B_pol = 9 G · (age/4.5 Gyr)^−0.33 ·
  (M/M_J)^0.93 — an interpolation of Reiners & Christensen 2010's cooling-track results in (mass, age).
  **The luminosity never appears as a quantity**; the branch consumes `age_gyr` directly and the −0.33
  exponent *is* the cooling track, folded in. The method doc (`planetary-dynamo-scaling.md:78–88`) says so:
  *"rather than re-derive internal cooling luminosities L(M, age) from scratch … tabulate, and interpolate
  in (mass, age)."*
- **brown dwarf, 13–70 M_J** (`dynamo.py:94–102`): out_of_domain, *"needs the internal cooling luminosity
  L(M, age) … the document chose not to supply L rather than use an unverified cooling track."*
- **age < 0.2 Gyr**: out_of_domain (cooling luminosity changes too fast for the interpolation).

So the edge's `via: cooling_luminosity` is exact for the brown-dwarf branch and **mislabelled for the giant
branch, whose payload is `age_gyr`** — the same shape as C17 (payload named after the mechanism, not after
what the code takes). Whether the graph's gap is a gap therefore depends on **which class the roster body is**.

## 2. Measurement and registered outcomes

**Instrument.** `run.py` on the roster's giant (`engine/bodies/alpha_centauri_a_b.yaml`, Polyphemus) and
`dynamo.dipole_field` directly at the roster's brown dwarf mass (Luhman 16 A/B, 13–70 M_J band, host age as
declared on its board — read, not constructed), plus one age below 0.2 Gyr as the third branch. Read
`regime`, `grade`, `reason`, `values.b_pol`, and whether `body_age`'s output reached the recipe.
Positive control: changing `age_gyr` on the giant must move `b_pol`.

- **①** The giant branch runs from `body_age` alone, and moves with age → for the **giant class the edge is
  already delivered**; its `via` is relabelled to `age_gyr` (docs + one `chain.yaml` edge). The
  brown-dwarf `L(M, age)` refusal stays as its own gap, on its own edge or note, with the Tier request
  (Burrows / Baraffe cooling tracks) named.
- **②** The giant branch does not run from `body_age` (the state key does not reach the recipe, or the
  runner declares age differently) → the gap is a wiring gap in `run.py`/`_from_state`, reported, not
  patched in this item.
- **③** The brown-dwarf mass returns out_of_domain with the L(M, age) sentence → confirmed; **no track is
  grounded tonight** (a cooling-track paper is a request, not a read-in).
- **④** Age < 0.2 Gyr returns out_of_domain → confirmed; recorded as the third named refusal.
- **⑤** No numeric constant moves; anchors untouched; no `dynamo.py` change. Gate FAIL 0, time, `pmset`.
