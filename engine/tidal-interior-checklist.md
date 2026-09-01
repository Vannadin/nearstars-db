# Wire tidal heating into interior structure — checklist (Brief 35)

Registered 2026-09-01, before work. Read-first done: methodology §6 whole + citation
block (~563–610), brief-35.md. **The transport mode is DECLARED, not derived** — Ė(T)
is not required because we evaluate the conversion at a given heating rate, exactly as
Kankanamge & Moore 2019 §6 does for Io (*"the internal heating rate is chosen to
satisfy the observed thermal emission"*); our Ė is likewise a computed input. **Hard
line: no roster body's answer changes in this brief — Hades/Dante are NOT re-solved**
(parked owner decision; measure only, adopt nothing).

**Order and items**
- [x] **A (extract the relation)**: read Kankanamge & Moore 2019
  (`docs/phase3/_papers/2019JGRE..124..114K.pdf`) and transcribe the heat-pipe
  parameterization: surface heat flux → internal (mantle) temperature + lithosphere
  thickness, every equation labelled `Kankanamge & Moore eq. N` checked at its place
  in the text, every constant with its condition. Known traps (do not re-derive, do
  not step in): ⚠ never transcribe §6's "totaling ∼1 TW" (2.5 W/m² × Io's area =
  104 TW, two orders off; the flux itself is sound); "<15 %" is parameterization vs
  their own simulation (§5), not accuracy vs Io; Rovira-Navarro Fig. 2 is a topology
  diagram (no numeric x labels at 1200 dpi) — no digitizing, recorded as an absence.
- [x] **B (pre-register the Io tolerance)**: from the paper's own printed precision,
  BEFORE the first run — never back-derived from what the run produces. Written in
  the context notes with its derivation.
- [x] **C (wire the axis)**: Ė → (internal temperature, lithosphere thickness) under a
  declared transport mode (§6.2 three-mode ladder is the menu; declaration carries
  its label). Output is a **labelled result**: each number says whether it is derived
  from Ė or declared, plus a **stability label** (Rovira-Navarro+ 2021: one stable
  equilibrium; unstable point exists only in Maxwell+convection pairing, and a body
  there *"enters a runaway cooling phase"* — labelled result, not a bare temperature).
  Where this axis can derive `potential_temperature`, the output states derived-vs-
  declared explicitly. No new runtime dependency.
- [x] **D (Io validation)**: feed Io's observed heat flux (2.5 W/m², Kankanamge §6)
  through our wiring; accept iff it lands on **1471 K and 12.6 km** within the item-B
  tolerance. Io is not in the anchor set — record the choice: gate check-table vs
  one-off reproduction.
- [x] **E (measure, don't adopt)**: what the axis *would* do to affected roster bodies
  (Hades, Dante, any tidally heated roster body) — measured and reported, zero
  adoption, anchors bit-identical.
- [ ] **F (landing)**: context notes closed; report SHAs, Io reproduction + which
  pre-registered branch fired, what the labelled result returns, roster measurement,
  anchor bit-state, gate delta. (interior-core.md / SESSION-HANDOFF.md rows are the
  directing seat's edit — not mine.)

**Pre-registered outcomes, five**
1. Io reproduces within tolerance → axis wired and validated; report roster measurement.
2. Io reproduces on one half only (T xor lithosphere) → adopt only the cleared half,
   name the other as unvalidated.
3. Io misses both → the test failed; the product is the NAME of the wrong assumption
   (transport mode? flux? unit?). Do not tune the declaration until Io comes out right.
4. §6 does not print enough to reproduce → legitimate "not found": what was searched,
   how, what would unblock.
5. Outside the register → name it; record the kind afterwards.

**Hard constraints**: anchors bit-identical expected (movement stops the brief, traced);
`test_ice_giant.py --refresh` only if a fingerprinted function/constant moves, same
commit, cause stated; gate FAIL 0, backgrounded under `caffeinate -i`, log-tail watch,
in-log timestamps, measured delta reported (Brief 34 added +22 s); numbers enter only
with label (quantity, source location, condition, paper name where a file carries two
papers); filled-in numbers say so; no WebSearch (ADS token + `_papers/` cache,
identifiers read not made, checked by title); commits English, one logical change,
`VaNnadin <vannadin00@gmail.com>`; `git diff --stat <file>` before `git add <file>`.

**Verdict (2026-09-01, landed)**: Branches ③+④. Transcription verbatim-verified (PDF
text layer); solver exact to 1e-14 with F_m+F_c=HD closure; natural readings put Io at
T_i 1447–1594 K, δ 97–534 km (δ misses 12.6 km by 8–42× everywhere); exact-root
recovery shows (1471, 12.6) requires α=8.71e-7·ΔT_rh=354 K (unphysical); the paper's
own Tables 2–4 fail deterministic inversion (per-row L drifts 0.3→10.8). Axis shipped
wired + labelled + `validation: failed-io-reproduction`; Io = gate check table
(test_tidal_transport.py); Dante = no root at 11,500 W/m², Hades = (1844 K, 224 km)
measured-not-adopted. *Corrected same day (notes §6): the Dante input was a mismatched
pair (11,500 is the rejected 900-km draft's flux); at the canonical §6.5 pair
(2,231 W/m²) Dante has a unique root (2122 K, 147 km). Roster inputs are now read
from canonical files with a pairing gate (roster_inputs), hand-typing removed.* Declaration untouched. Details: tidal-interior-context-notes.md §4–5.
