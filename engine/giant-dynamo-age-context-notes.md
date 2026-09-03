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

## 3. Run record — 2026-09-04

**Branch fired: ① for the roster giant; ③ and ④ confirmed as named refusals. Nothing in `dynamo.py` moved.**

    body / trial                         M (M_J)   age (Gyr)   regime          grade        b_pol (µT)   reason (head)
    Polyphemus, run.py from body_age     0.378     5.3         giant           calibrated   344.7        "inside the calibrated giant range; dipole set by internal cooling luminosity"
    Polyphemus, age halved (control)     0.378     2.65        giant           calibrated   433.3        same
    Luhman 16 A-class mass (board 76)    33.5      0.5         out-of-domain   judgment     —            "brown-dwarf band 13–70 M_J: needs L(M, age); the document chose not to supply an unverified track"
    below the calibration                0.378     0.15        out-of-domain   judgment     —            "0.15 Gyr is below the 0.2 Gyr floor; cooling luminosity changes too fast to interpolate"

- **Positive control held**: halving the age raises b_pol 344.7 → 433.3 µT (the −0.33 exponent, as written).
- **① for the giant class**: `run.py` delivers `dynamo_giant` from `body_age` alone — `body_age.age_gyr` reaches
  the recipe and it produces a calibrated value. **The edge's `via: cooling_luminosity` was the mechanism's
  name, not the payload's** (C17's shape again); for giants the payload is `age_gyr` and it is already wired.
  Relabelled in `chain.yaml`: `body_age → dynamo_giant via t_body` (the graph's name for the code's `age_gyr`), no longer a gap.
- **③ confirmed, and it is not academic**: Luhman 16 A and B (33.5 and 28.5 M_J on the board, 0.5 Gyr) are on
  the v1 roster, and both sit in the band that returns out-of-domain. **The brown-dwarf L(M, age) gap is a
  roster gap, not a corner case.** It stays a gap, on its own line: `body_age → dynamo_giant via
  cooling_luminosity, status: gap`, now scoped to the brown-dwarf branch, with the request named (a
  Burrows / Baraffe-class cooling track, grounded before it is read in — a Tier request, not tonight's read).
- **④ confirmed**: age < 0.2 Gyr refuses by name. No roster body is that young on its board (Luhman 16 is
  0.5 Gyr), so it is recorded, not prioritised.
- **Observed beside it, not judged**: the same `run.py` shows `internal_heat_nontidal` refusing the giant for
  the *same* reason (*"a giant's internal heat is the cooling luminosity L(M, age), and this recipe does not
  supply an unverified cooling track"*). So the cooling-luminosity gap has **two consumers** — the brown-dwarf
  dynamo branch and the giant's internal heat — and one supplier missing. Whichever item grounds a cooling
  track closes both; that is a note for the owner's C list, not a wiring done here.

**Closure state**: C19 **closes for the giant class (already wired, mislabelled) and narrows to the
brown-dwarf branch**, where it stays open with its supplier named and two consumers listed. No code path
touched; anchors untouched.
