<!-- ② 바디 클래스 기본값(authored 뒤) + 장치 셋 — 사전등록만. 구현 안 함(오너: 노드는 여기까지). -->
# Class defaults behind `authored` — item ② — pre-registration only

**Status: pre-registered 2026-09-04, NOT built.** The owner stopped node work the same afternoon ("노드는 여기까지만"); this file is the record for whenever ② is released. Nothing here exists in code.


**What it is.** A per-body-class default table so that a chain does not stop for want of a declared input:
when a body declares nothing for a quantity, the class table supplies a value **graded `authored`** with the two
policy markers. The predecessor's speed came from exactly this (class defaults for every quantity); ours keeps
the label on every such value.

**Three devices, built with it, not after (directing seat; the strict mode is the most important):**
- (가) **Strict mode** — a path that runs with no defaults at all, so "how far do we actually know" stays visible.
  Concretely: `run.py --strict` (or an env flag) makes the state supply no class default; a node that would have
  taken one refuses by name instead. The gate runs *both* modes on the roster and prints the difference.
- (나) **Per-body authored count in the gate** — `run.py` prints, per body, how many inputs came from the class
  table, and asserts that no `measured` input was replaced by a default (a declared value always wins).
- (다) **Class table only** — defaults live in one table keyed by body class; no per-body ad-hoc authoring.

**Boundary carried over from ① (⑨), quoted here so it lives in two places** — from `phase-tables-context-notes.md`
§2 ⑨ and `phase_tables.py`'s docstring: *"②'s class defaults attach to the body-class axis only. The phase side
tables' empty cells are not a target of ② — a phase is not a class — so ② can never silently swallow this
table's emptiness."* A default that would fill a phase cell is refused by the phase table's own contract.

**Registered outcomes, before a default is written:**
- ① Every default row carries `gap:` (why no source per class) and `consistent-with:` (the bound it sits in);
  the table itself carries a provenance line ("where this table came from") — a default without both is refused
  at construction (the same `payload` check).
- ② The strict-mode roster run shows *exactly* the refusals we see today (no default may change a strict result);
  the default-mode run differs from strict only where a class default was consumed — the diff is printed.
- ③ If a class default would contradict a held source for that class, the default is not written (the
  contradiction is a finding).
- ④ Anchors untouched, `--refresh` not run; gate FAIL 0 with both modes.
- ⑤ Which quantities get defaults first: only those a *waiting* consumer needs — `t_form` (C21), `locked`
  (C16) are candidates; the owner orders them. Nothing beyond the mechanism and the first row is built here.

**Grade propagation — the most dangerous gap, added before ② is built (directing seat's code read, reproduced):**
no recipe reads the grade of its inputs — `cmb_flux.py@«grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)»` and `core_energy.py@«grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)»` write `grade="analog"` as
literals, `core_state.py@«grade=grade, inputs=inputs, refs=REFS,»` sets its own — so once ② supplies an `authored` default to a recipe whose grade is
a literal `calibrated`, the output still says `calibrated`. Over a five-step chain each step can absorb one
authored input and the final value still carries the literal grade: **false provenance manufactured by the
system itself**, at volume. So ② ships with:
- **A propagation record, not a downgrade**: `payload.Result` gains `authored_inputs: tuple[str, ...]` — the
  names of this result's inputs that were class defaults (the runner fills it from the state's provenance);
  `run.py` prints per body the count of results carrying any; anything that reaches a cfg emit with an
  authored default somewhere in its chain is made visible there.
- **No grade downgrade now** (output ≤ worst input would mean re-grading eleven recipes and can be wrong — a
  calibrated recipe fed an analog input may still be calibrated). Visibility first; whether to downgrade is
  decided on the measured number, separately.
- **Pairing**: `--strict` answers "how far without defaults"; the propagation record answers "how far the
  defaults seeped". Both are needed to close the picture.
- **Threshold, written now, by this seat, before any run** — on the first full roster run after ② lands, the
  share of applicable results that carry at least one authored input is measured:
  **< 10 % → visibility suffices, no downgrade rule; ≥ 10 % → a downgrade rule is needed, decided separately.**
  Why 10 %: one value in ten is the density at which a reader skimming a board meets an authored-fed value on
  every screen; it is a declared line, not a derived one, and it is written here so it is not chosen after
  the number is seen.
