<!-- Brief 47 — 암석 행성 다이나모 사다리(RM22/OC06)를 dynamo_rocky 레시피로: 선언 네 가지, 게이트 둘, Rm > 40 은 인용이지 평가가 아니다 -->
# The rocky dynamo ladder — Brief 47 (context notes)

2026-09-03. **§1–§3 are the pre-registration and were committed before any code ran.** Verifiers: (병)
parallel seat, (직) directing seat, (감) audit, (여기) work seat. Owner decision: build the ladder now; the
entropy-production alternative (Nimmo+ 2004) needs the coupled forward integration Brief 45 closed on and
is not foreclosed by this.

## 1. Sources, and what is actually held

- **RM22** — Rodríguez-Mozos & Moya 2022, *Internal structures and magnetic moments of rocky planets*,
  **A&A 661, A101** (`2022A&A...661A.101R`, arXiv 2203.01065). **Held**: `docs/phase3/_papers/2203.01065.md`
  + `.html` in the main checkout's cache, now reached from every worktree by the symlink (the engine
  worktree's own copy never had it — the "not cached" finding of this morning was a check against the wrong
  of two caches; `SESSION-HANDOFF.md`). ⚠ The methodology doc cites it as **"A&A 661, A176"** at lines 21 and
  151 — **wrong article number**, ADS-verified; fixed in this brief, EN and ko.
- **OC06** — Olson & Christensen 2006, *Dipole moment scaling for convection-driven planetary dynamos*,
  E&PSL 250, 561 (`2006E&PSL.250..561O`). **Not held in either cache** (checked both). On the request list.
- **Gaidos+ 2010** — *Thermodynamic Limits on Magnetodynamos in Rocky Exoplanets*, ApJ 718, 596
  (`2010ApJ...718..596G`). **Not held in either cache.** ⚠ Authors are **Gaidos, Conrad, Manga & Hernlund**
  (ADS); the doc's bibliography row (line 160) prints *"Gaidos, Conrad, Manoj & Blake"* — wrong author list,
  fixed. The body's "Gaidos 2010" is ordinary et-al shorthand. **Cited for the `Rm > 40` threshold we never
  evaluate** (§2).
- **Zhang & Rogers 2022** (`2208.06523`, ApJ 938, 131), *Thermal Evolution and magnetic history of rocky
  planets* — **held**, already cited by `core_state` (the 0.80 depression convention), **not cited by the
  rocky-dynamo methodology though it is on its subject**. It is a **computed alternative** (thermal evolution
  + Henyey solver, `Re_m` evaluated cell by cell): the same fork the owner just decided, so it is **flagged,
  not followed**. Two of its sentences bear on the ladder and are carried as conditions: §2.8 *"so long as
  the liquid iron core exists and is convective, it could support a dynamo with Re_m > Re_m,crit"* (which is
  what lets `conductor_phase` stand in for the alive gate); and §4.2.5's lifetimes — 1 M⊕ dynamos shutting
  off at **~2.5 Gyr (CMF 0.7) / ~5 Gyr (CMF 0.326)** at T_eq 255–1350 K, 3 M⊕ at ~10–12 Gyr, ~1–2 Gyr at
  T_eq 2500 K — which make the ladder's death-age declaration ("Mars-mass by ~7 Gyr") **contested**, not
  settled.

**What RM22 itself prints for the Solar System (Table 8, HTML render, 여기)** — calculated / observed
ℳ/ℳ⊕: Mercury **0.0003 / 0.0004**, Venus **0.0007 / 0**, Earth 1 / 1, Mars **0.084 / 0.10** (marked *"extinct
dynamo"*), Ganymede **0.003 / 0.002**. ⚠ **The methodology's "validation table" uses the observed column and
writes Mars and Venus as ℳ = 0 ("frozen", "stagnant lid").** RM22's model does **not** compute zero for either
— its 0.084 and 0.0007 are what the model gives; the zeros are the ladder's own class judgements (step 2)
laid over the model. That is a real difference between the doc's rendering and the paper, registered here
before the build; the transcription check below therefore closes the doc's closing relation against the
doc's *observed* column and says so.

## 2. Design — five steps, four declarations, two gates that are labels

**Placement**: `engine/dynamo_rocky.py`, `@recipe("dynamo_rocky")` (the node has 11 edges and no module).
`dynamo.py` keeps refusing `body_class == "rocky"` by name and pointing here.

**Step 1 — classify** from mass, radius, declared `ice_mass_fraction`: regime 1 dry M < 2 M⊕; 2 dry
2–2.5 M⊕; 3 dry > 2.5 M⊕; 4 water-rich (imf ≥ 0.05, a declared threshold); 5 low-density dry
(ρ < 0.8 ρ⊕). > 10 M⊕ or non-rocky classes → out of domain (giant recipe).

**Step 2 — alive gate, made of labels, not a formula.** (a) `conductor_phase` from `core_state`: `solid` →
ℳ = 0; `undecided` → **cannot-say (④)**; liquid / mixed → alive. (b) **stagnant-lid judgement — declared
per body** (`stagnant_lid: true|false` input); undeclared → cannot-say. (c) **dynamo-death age — declared
per class** (`DYNAMO_DEATH_AGE_GYR`, regime 5 only, 7 Gyr from the doc's one worked point; Zhang & Rogers'
contested range carried beside it). (d) **`Rm > 40` — QUOTED, NEVER EVALUATED.** The doc lists it as a
disqualifier beside two class judgements with no formula anywhere in the file (zero hits for μ₀, "Rm =",
conductivity/velocity outside prose); it reads as a computation and is a citation. Marked at the step, in
the emitted note, and in the contract, so building the ladder does not freeze that state into code.

**Step 3 — ℳ_base, the declared family.** The doc's *"(table below)"* points at the per-body validation
table, not a per-class anchor — **a pointer to the wrong table, said where the anchor is declared.** Values:
regime 1 → **1.0** ("up to ~1 ℳ⊕"); regime 4 → **2×10⁻³** (Ganymede analog); regime 5 → 0. **Regimes 2 and 3
have no value in the doc** ("can exceed Earth's while young"; "weaker and shorter-lived") — the ladder
cannot execute for a super-Earth without one. Declared as a **grid, never one elected tuple**: regime 2
{1.0, 2.0}, regime 3 {0.3, 1.0}; the recipe emits the endpoints and **no elected `dipole_moment`** there
(C11's ending: downstream declares its own and carries the label).

**Step 4 — regime gate, declared and gridded.** The `rossby` edge is a gap (`tidal_locking` cannot supply
Ro_ℓ). A body may declare `dynamo_regime: dipolar|multipolar`; undeclared → **both branches emitted**:
dipolar ℳ_base and multipolar ℳ_base × {0.06 (OC06/RM22 — RM22: *"about 0.06 … ratif[ies] OC06"*), 0.15
(Grießmeier 2009)} — a **factor 2.5 in the answer** that rides on every emitted value. `regime` output =
the declared branch or `undeclared (both emitted)`; the edge to `magnetosphere_geometry via regime` gets
this.

**Step 5 — field.** `B_eq = 30 µT · ℳ/ℳ⊕ · (R/R⊕)⁻³`, `B_pol = 2 B_eq`, per branch.

**Transcription check** = the doc's own Solar-System table through step 5 (Mercury 4×10⁻⁴, 0.38 → 0.22 µT;
Ganymede 2×10⁻³, 0.41 → 0.87 µT; Earth 30; Mars, Venus 0), **and** the finding above pinned: RM22's
computed Mercury 0.0003 → 0.16 µT and Venus 0.0007 → 0.024 µT are not the zeros the doc writes.

**REFS**: the methodology; RM22 as **A101**; OC06 (not held); Gaidos, Conrad, Manga & Hernlund 2010 — *"cited
for a threshold this recipe quotes and does not evaluate"* in the comment; Zhang & Rogers 2022 flagged as the
computed alternative not followed.

## 3. Pre-registered outcomes, and the work seat's expectation

① the validation table reproduces and the roster's rocky bodies get moments; ② it does not → the finding,
do not tune the anchor; ③ a roster body falls in regime 2 or 3 and the declaration is load-bearing → name it
and the spread across the grid; ④ `conductor_phase` undecided for a body → cannot-say, not a default; ⑤ the
×0.06-vs-×0.15 spread swamps the answer for some body → the recipe cannot grade there and refuses by name.

**Expectation (여기; the directing seat declined to register one)**: ① the table reproduces trivially —
`B = 30 ℳ R⁻³` is the doc's own arithmetic on the doc's own observed column — so the check certifies the
transcription and nothing about RM22; the substantive finding is the Mars/Venus zeros (§1), which is a
doc-versus-paper difference rather than ②. Earth → regime 1, alive (`liquid_outer_solid_inner`, and
`stagnant_lid: false` declared in `bodies/earth.yaml` as a fact — plate tectonics), regime gate undeclared
→ both branches emitted: dipolar 1.0 ℳ⊕ → **30 µT** (the anchor, reproduced not predicted), multipolar
0.06–0.15 ℳ⊕ → **1.8–4.5 µT**. Pandora → **④ cannot-say** (`core_state` is undecided for it — no
temperature). The giant → out of domain. ③ does not fire (no roster body above 2 M⊕ reaches the recipe);
⑤ does not fire as a refusal because the regime is emitted as a family rather than graded — the spread is
carried, not adjudicated. **Load-bearing declarations for Earth**: the regime branch (2.5× in the answer)
and `stagnant_lid`; not ℳ_base (regime 1 has a value) and not the death age (regime 5 only).

## 4. Result — filled after the run

*(pending)*
