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

## 5. Pre-registration for the brown-dwarf branch (directing seat's brief, copied verbatim before any code — 2026-09-04)

##### C19 brown-dwarf branch — pre-registration

**Owner released this 2026-09-04 knowing it sits OUTSIDE the interior-structure stem.** The
owner asked *"지금 혹시 내부구조 그룹 밖 작업 하려는거야?"*, the directing seat confirmed it does
(this branch consumes mass, luminosity and radius and touches nothing the interior solver
produces), and the owner answered *"뭐 이미 시작했으니까 걍 2,3 하는데까지 해보자."*
**Record that in the commit.** C19 stays on the interior C-list because that is where it was
opened; the *work* is a `dynamo.py` job, and the next seat must not read this as the stem moving.

#### 1. Why the old refusal no longer holds

`dynamo.py`'s docstring refuses the brown-dwarf branch like this:

    "The document sends it to B_dyn = 4.8 (M L^2 / R^7)^(1/6), which needs the body's
     internal cooling luminosity, and the same document explicitly refuses to supply
     L(M, age) rather than ground a cooling track it has not verified."

**The refusal was about deriving L, not about the scaling.** The scaling is published and held:
Reiners & Christensen 2010 (`2010A&A...522A..13R`, cached as arXiv `1007.1514`), relayed in
`docs/reference/planetary-dynamo-scaling.md` §"Brown dwarfs, 13–70 M_J: use B_dyn directly".

For **an isolated brown dwarf there is no cooling track to derive** — the body has no host star
and no fusion, so its observed bolometric luminosity *is* the internal cooling luminosity, and
the DB already holds it as a **measurement**. Christensen, Holzwarth & Reiners 2009
(`2009Natur.457..167C`, obtained by the owner 2026-09-04) makes the same move explicitly: its
`q_o` is *"the bolometric flux at the outer boundary"*, and for stars it is taken from the
effective temperature, not from a track.

⚠ **The one thing that must be stated, not assumed**: that identification (observed L_bol =
internal cooling L) is *sound for an isolated brown dwarf* and *false for an irradiated
planet*. Write the condition into the code beside the branch, or a later seat will apply this
to a hot Jupiter.

#### 2. Inputs — and their honest status

Read from `db/systems/luhman_16_{a,b}.json` on 2026-09-04:

| input | A | B | status |
|---|---|---|---|
| M [M☉] | 0.032 ± 0.0003 | 0.0273 ± 0.0003 | **measured** — binary orbit, Lazorenko & Sahlmann 2018 (`2018A&A...618A.111L`), `recommended: true` |
| L [L☉] | 2.14e-05 | 1.95e-05 | **measured** — bolometric, Faherty+ 2014 |
| R [R☉] | 0.09 ± 0.01 | 0.09 ± 0.01 | ⚠ **DECLARED, not measured** |

⚠⚠ **The radius is an assumption and it is the most sensitive input.** The DB says so itself:
*"No measured radius exists for either component. Faherty 2014 adopts R = 0.9 R_Jup via the
Vrba et al. 2004 prescription … this is the standard field-brown-dwarf radius assumption, not a
measurement. ~0.08–0.10 R☉ over the 0.1–3 Gyr age range."* Both components carry the same value
**because it is the same assumption**, not because anyone measured them equal — this was raised
as suspect (owner list O2) and is hereby **closed as correctly labelled**.

In `B_dyn ∝ (M L² / R⁷)^(1/6)` the radius enters as **R^(−7/6)** — the steepest exponent in the
formula, applied to the only input that is a declaration. **This is the branch's dominant
uncertainty and it must be reported as a band, never as a single number.**

#### 3. Branches — named before any number is computed

##### ① Magnitude against the published expectation
Two independent published statements exist *before* we compute, and they are the pre-registered
target:
- Christensen+ 2009: a typical **1-Gyr-old BD of 0.05 M☉ at T_eff 1500 K** → surface field
  **of order 0.1 T = 1 kG**.
- `planetary-dynamo-scaling.md` §domain: *"massive BDs reach a few kG when young, weakening
  ~10× by 10 Gyr."*

Luhman 16 A/B are **less massive** (0.032 / 0.027 vs 0.05 M☉) and **less luminous**, so a value
*at or somewhat below 1 kG* is the expectation.
- **①a within a factor of ~3 of 1 kG** → consistent; report with the band from ②.
- **①b an order of magnitude or more away** → **do not report the number as a result.** Find
  the disagreement first: unit slip (the formula is in **solar units** and returns **kG**), or
  the L identification of §1, or the radius.
- **①c the formula returns something unphysical** (non-finite, negative) → a coding fault, stop.

##### ② The band is mandatory, and its width is pre-declared
Propagate **R over the DB's own 0.08–0.10 R☉**, not over ±1σ of a fictional measurement. That
is ~±11 % in R, hence **~±13 % in B** through R^(−7/6). Also carry the mass uncertainty
(±0.9 %, negligible by comparison) so the report shows which input dominates.
- **Emit `b_dyn_min` / `b_dyn_max`, and state in the result that the width is radius-driven.**
- ⚠ **A single-valued `b_dyn` is forbidden on this branch.** The radius is declared; a bare
  number would be the most confident-looking output in the engine and the least earned.

##### ③ What the consumer actually wants — check before wiring
`dynamo.py` today returns `B_pol`, `B_eq` and a moment normalised to Earth. The giant branch
gets there via `B_dip^eq = B_dyn / (2√2)` **plus a mass-dependent depth attenuation**, because
in a giant the dynamo sits below the visible surface (~0.83 R in Jupiter).
- ⚠ **The methodology says brown dwarfs are different**: *"use B_dyn directly (dynamo near the
  surface)"*. So for a BD, **do not apply the giant's depth attenuation.**
- **③a the consumer wants a surface dipole** → the 2√2 conversion applies but the depth
  correction does not; say so in the code.
- **③b the consumer wants B_dyn itself** → emit it and label it as the dynamo-surface rms field,
  not a surface dipole.
- **③c the consumer wants a magnetic moment** → the moment normalisation uses `(R/R_J)³`;
  confirm it is meaningful for a BD before reusing the giant's constant.
**Resolve ③ by reading the consumer, not by choosing.**

##### ④ The saturation condition must be checked, not assumed
The scaling is rotation-independent **only above a critical rotation rate**. The methodology
says this *"holds for isolated brown dwarfs"*, and Luhman 16 rotates in **6.94 h (A)** and
**4.87 h (B)** (`rotation_period_days` 0.2892 / 0.2029) — fast. **Assert the condition in the
code with those numbers**, so a slow rotator later cannot silently take this path.

##### ⑤ Domain guard
Branch applies to **13–70 M_J**. Luhman 16 A/B are ~33.5 / ~28.5 M_J — inside. Bodies outside
must keep returning out-of-domain, and the existing giant / ice-giant / rocky refusals must not
be disturbed.

##### ⑥ Anchors and gate
Confirm no anchor path traverses this branch; if so **anchors untouched, no `--refresh`** —
state it in the commit. Gate **FAIL 0**, and say what it adds to gate time.

#### 4. What must NOT be claimed

- Not *"Luhman 16's magnetic field is X"* — it is **the field an energy-flux dynamo scaling
  predicts, on a declared radius**. Christensen+ 2009 itself notes *"Magnetic fields have not
  been detected at brown dwarfs so far."* There is no measurement to agree with.
- Not that C19 is closed for anything but this branch. The **giant** half was already wired
  (mislabelled, fixed 2026-09-04); the **`internal_heat_nontidal` for giants** consumer named in
  the C19 row is a separate waiting consumer and this does not serve it.
- ⚠ Do not equate Christensen+ 2009's `c = 0.63` with Driscoll & Olson's `c_d = 0.2`; different
  quantities (energy density vs dipole intensity). Recorded in `2009Natur.457..167C.PROVENANCE.txt`.

#### 5. Order

read the consumer (③) → domain + saturation guards (⑤ ④) → the band (②) → compute → ① check.
**① is read last.** It is the number everyone wants and the one most easily produced by a unit slip.

**Resolved before code, by reading (③)**: `chain.yaml:718` is the only edge out of `dynamo_giant` — `magnetosphere_geometry` requires `b_eq` [µT]. So ③a: emit `b_eq = B_dyn/(2√2)` (RC10 eq. 2) with **no depth attenuation**, `b_pol = 2 b_eq`, and reuse the moment normalisation (a dipole moment is B_eq·R³ by definition; 4.5 G · 20000 only sets the ×Earth scale). **And a lowered expectation, stated up front**: `magnetosphere_geometry` has no recipe, so the giant branch's `b_eq` already has no consumer — building this branch removes one refusal inside the module and closes the `cooling_luminosity` gap edge; it does **not** wire the dynamo downstream and creates no new orphan output. Beside it: `tidal_locking → dynamo_giant` (`:648`, selects) — the tidal-locking recipe candidate has two consumers, not one. Recorded, not acted on.


## 6. Run record — brown-dwarf branch built (2026-09-04, daytime)

**Order kept**: consumer read (③, `b_eq`) → guards (⑤ 13–70 M_J kept, ④ saturation: rotation period required and ≤ 4 d
— RC10 §2.1's own evidence bound, the critical rate itself "somewhat uncertain") → band (② radius band required;
single value forbidden) → compute → ① magnitude read last.

    body          M (M_J)   L (L☉, measured)   R (R_J, declared; band)   P_rot (h)   B_dyn (kG)   band (kG)     b_eq (kG)   moment (×Earth)
    Luhman 16 A   33.5      2.14e-5            0.876 (0.778–0.973)       6.94        1.246        1.10–1.43     0.440       1.32e6
    Luhman 16 B   28.6      1.95e-5            0.876 (0.778–0.973)       4.87        1.176        1.04–1.35     0.416       1.24e6

- **Guards, seven rows, all refuse by name** (no luminosity / no rotation / no band / `isolated` undeclared /
  `isolated=False` (the hot-Jupiter route) / P_rot 5 d / 80 M_J). The old "no inputs" brown-dwarf refusal
  row still refuses, now naming the missing inputs instead of an L(M, age) track.
- **By-hand check**: 4.8 (0.032 · (2.14e-5)² / 0.09⁷)^(1/6) = 1.246 kG, code 1.246 (0.04 %).
- **② band**: width 26 % of B_dyn from R 0.08–0.10 R☉ alone (pre-registered ~±13 %) — **the width is
  radius-driven**, written into the result's notes; the mass ±0.9 % is negligible beside it.
- **③ consumer contract**: b_eq = B_dyn/(2√2), b_pol = 2 b_eq, no depth attenuation; moment reused.
- **① magnitude, read last**: B_dyn 1.25 kG sits inside RC10 §4.1's printed brown-dwarf range ("a few kG
  and a hundred G") → PASS. Against Christensen+ 2009's "~0.1 T for 1 Gyr · 0.05 M☉ · 1500 K" it is 1.25× —
  **inside ①a's factor of 3, but on the *high* side, where the pre-registration expected "at or somewhat
  below 1 kG" for a lighter, dimmer body.** Stated, not explained away: the 1 kG is an order-of-magnitude
  sentence for a different object, and at that precision the direction "lighter → weaker" is not decidable;
  what would decide it is Christensen's own L and R for that object, which the Letter does not tabulate.
  **Reconstructed after the gate (directing seat's route, independently recomputed here)**: the Letter does
  not tabulate L and R but it prints ⟨ρ⟩ = 90 000 kg m⁻³ and T_eff = 1 500 K for that 0.05 M☉ example
  (pdftotext lines 326–331), and those recover both: R = (3M/4πρ)^⅓ = 0.0922 R☉, L = 4πR²σT⁴ = 3.88e-5 L☉.
  Put through the same RC10 eq. 1: **B_dyn = 1.59 kG** against the Letter's "of the order of 0.1 T" —
  1.6×, inside "of order", so **the two formulations are one family, checked in our own hands**. And on the
  same formula Luhman 16 A (1.25) < the example (1.59), ratio 0.78: **the direction "lighter and dimmer →
  weaker" holds.** The pre-registered expectation was not overturned; its comparison value was 1.59 kG,
  not 1 kG. Radius is not the confounder: ours 0.0900 R☉ vs the example's 0.0922 R☉ (written in R☉, not
  R_J — the Jupiter-radius convention, equatorial 7.1492e7 m vs mean 6.9911e7 m, moves the R_J number by
  2 % and Faherty's "0.9 R_Jup" was not checked for which one it used), i.e. the example is 2.4 % larger,
  which through R^(−7/6) is −2.8 % in B and cannot carry the 22 % gap between 1.25 and 1.59. Band wording
  corrected: the pre-registration's "~±13 %" was one-sided; the full width is 26 %.
  Not a result about Luhman 16's field: **the field an energy-flux scaling predicts on a declared radius;
  no brown-dwarf field has been detected** (Christensen+ 2009).
- **Contract checker generalised** (`check_contracts.py`): a recipe with branches is now checked against the
  union of inputs/outputs over all sample bodies that return a value (Polyphemus + Luhman 16 A/B), instead of
  the first one — otherwise the brown-dwarf-only outputs could not be declared in Returns.
- **Graph supplier, found by the via check**: `cooling_luminosity` has no supplier node, so the edge could not simply drop its gap mark — `check_via` refused the commit's first form (masked by `tail` in the launch chain; that gate was killed and stamped void). The supplier of a brown dwarf's measured bolometric luminosity is `star_physical.luminosity` (Luhman 16 A/B sit in the DB's `stars[]`), so the edge is now `star_physical → dynamo_giant via luminosity` (code name `luminosity_lsun`), the `body_age … cooling_luminosity` edge removed.
- **What this closes and what it does not** (directing seat's framing): Luhman 16 A/B receive a value instead
  of out-of-domain and the `cooling_luminosity` gap edge closes. **Not** "the dynamo is wired downstream":
  `magnetosphere_geometry` has no recipe, so the giant branch's `b_eq` already has no consumer and this
  branch adds none — one refusal inside the module is gone, no new orphan output was made. `tidal_locking →
  dynamo_giant` (`chain.yaml:648`) means the tidal-locking recipe candidate has two consumers — recorded.
- **Anchors**: no anchor path traverses `dynamo.py`; `test_ice_giant.py --fast` 모두 통과 on this tree, no `--refresh`.

**Gate lines** (kept out of the powermode-2 table where marked):
- gate79 on `0554889c` ('&' fix, docs): `GATE END sha=0554889c rc=0`, 485 PASS, FAIL 0, 10:05:15 → 10:47:41 =
  **2546 s**, powermode 2 both ends, no throttle record (`pmset -g therm`). ⚠ **2.07× gate78 under the same
  power condition — excluded from the table.** Directing seat's *estimate, not a measurement*: host contention
  (it ran pdftotext on 9 MB PDFs, five repo-wide recursive greps, a 739-file cache loop and ADS round-trips in
  that window). The control is the next gate with the directing seat idle.
- gate80b on `76677df8` (brown-dwarf branch): `GATE END sha=76677df8 rc=0`, **498 PASS** (+13 rows from
  `test_dynamo.py`), FAIL 0, 10:52:36 → 11:18:37 = **1561 s**, powermode 2, directing seat idle throughout.
  ⚠ The control did *not* return to the 1224–1362 s band: 1561 is +15 % over its top with the peer quiet,
  so the host-contention estimate for gate79 is **partly supported at best** (2546 → 1561 with the peer
  idle) and the residual +200–300 s is **unexplained** — the added work (13 trivial rows, two brown-dwarf
  bodies whose interior recipes refuse at once) does not account for it. Kept out of the table, labelled.
- gate80 on `a87124f8`: killed at launch (via failure masked by `| tail -1` in the launch chain), void.
