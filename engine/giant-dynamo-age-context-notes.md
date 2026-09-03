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

## 4. After the measurement — what the cache already holds, and what the records disagree on (2026-09-04, directing seat's review)

**② The brown-dwarf branch has nothing to request.** Burrows, Hubbard, Lunine & Liebert 2001
(`2001RvMP...73..719B`, cached as `astro-ph_0103383` — the cache-lookup tool reported it ABSENT until its
old-style-id regex was fixed the same night) prints L(M, t) as an analytic power law with its conditions:

    L ≈ 4×10⁻⁵ L☉ (10⁹ yr/t)^1.3 (M/0.05 M☉)^2.64 (κ_R/10⁻²)^0.35       (their eq. 1)
    M ≈ 35 M_J (g/10⁵)^0.64 (T_eff/1000 K)^0.23                           (3)
    t ≈ 1.0 Gyr (g/10⁵)^1.7 (1000 K/T_eff)^2.8                             (4)
    R ≈ 6.7×10⁴ km (10⁵/g)^0.18 (T_eff/1000 K)^0.11                        (5)

Solar metallicity; zero-metallicity exponents printed beside (1.25, 2.4); stated range *"two orders of
magnitude in mass, three in age, T_eff 80–3000 K"* — Luhman 16 is inside. **κ_R is a free parameter that
absorbs the atmosphere model and the review gives it no value: reading eq. 1 in makes κ_R a declaration.**
The alternative is Baraffe+ 2003's tabulated tracks. **Neither is read in tonight** — owner's choice.
**④'s floor gains a printed basis, its value unmoved**: Burrows write that deuterium burning *"roughly
stabilizes T_eff, L, and R … from a few ×10⁶ years to 10⁸ years"* — so the 0.2 Gyr refusal's reason can
become *"the deuterium-burning plateau (≲10⁸ yr, mass-dependent) breaks the power law"* instead of
*"interpolation does not hold"*. The floor stays 0.2 Gyr; only the reason sentence is grounded. Not applied
to `dynamo.py` tonight (a reason-string change is a code change; it goes with the branch's next commit).

**③ Two of our own records disagree on Luhman 16's age** (directing seat's check, verified here):

    db/systems/luhman_16_{a,b}.json   stars[].derived.age_gyr = 1.5   ← age_measurements: 1.5 ± 1.5 Gyr, method "unverified", attributed Faherty+ 2014 (2014ApJ...790...90F)
    phase4/luhman_16.yaml:80, :640    age = 0.5 Gyr, op: passthrough   ← "Oceanus moving group (Gagné 2023), 12C/13C corroboration (de Regt 2026)"

The DB's 1.5 ± 1.5 reads as the midpoint of a 0.1–3 Gyr range, not a measurement. Three pieces of evidence
point at 0.5: the board's Gagné 2023 membership; eq. 4 with g from the DB's own mass and radius gives
0.54 / 0.44 Gyr (parallel seat); and at that age eq. 1 reproduces the DB luminosity within 20–30 %, while at
1.5 Gyr it misses by 3–4×. **Not fixed tonight**: `db/systems/*.json` is build output (never edited
directly), the fix belongs in the source layer, and that is the main repository, outside this worktree.
**Owner decision.** Beside it: the DB gives A and B the **same radius 62 613 km**, in the `principia` block
(not a measurement block) — a declared value whose source needs checking, and eqs 3–4 are sensitive to it
through g.

**④ The wiring may be shorter than a track.** The L(M, age) that `dynamo.py`'s refusal asks for already
exists in the DB as `derived.luminosity_lsun` (A 2.14e-05, B 1.95e-05) — and it is a **measurement**
(bolometric flux, Faherty+ 2014, `2014ApJ...790...90F`), not a model. Two routes, written side by side,
**not judged**:
- (a) ground a cooling track (Burrows eq. 1 with a declared κ_R, or Baraffe+ 2003 tables) and compute L;
- (b) consume the DB's measured luminosity directly — shorter, but it hangs on ③: the same L at 0.5 vs
  1.5 Gyr sits on different tracks, so the age must be settled before the value is trusted as an *input to
  a dynamo scaling* (Reiners & Christensen's B_dyn wants the internal flux, which the measurement gives
  only if nothing else contributes).
Both go to the owner's list with ③.
