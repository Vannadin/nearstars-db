<!-- 도출값을 사람 기억이 아니라 기계가 지키게 만드는 규율 — 왜 이렇게 정했는지의 근거 기록 -->
# Derivation discipline: why the recipes are built the way they are

NearStars derives a lot of numbers. A body's dipole field, its tidal heating, its
magnetopause standoff, the colour of its rings — each comes from a methodology document
that says how to get it from measured inputs and published physics.

That worked, and it also kept going wrong. Not spectacularly; quietly, in the way that a
number written in three places drifts in one of them and nobody notices for months. This
document records the disciplines adopted in response, and the specific failure behind each
one, so that a later reader can tell which rules are load-bearing and which are taste.

Every failure quoted below is one this project actually had.

---

## What kept going wrong

**A value moved and its dependants did not.** Proxima's magnetopause nose was updated from
23.5 to 35.33. `outer_compression` and `outer_extension` are functions of it and stayed at
their old values. Nothing caught it, because the relationship between the three numbers
existed only in the head of whoever last worked on that row.

**A worked example drifted from the formula it illustrated.** The dynamo scaling table
listed ε Ind A b's dipole moment as ~3 700 × Earth. Recomputing from the document's own
power law gives ~201 000 — a factor of 54. The table had been typed by hand and had not
been re-derived since an input changed.

**Two documents contradicted each other in the open.** The tidal-heating methodology and
the moon energy-budget methodology disagreed about whether the solid-body tidal term is
global or local. Both were published, both were being used, and the disagreement had no
owner because nothing compared them.

**Prose hid whether a recipe even applied.** A survey of which methodology documents state
their domain of validity returned "eight have none". Reading them showed the real number
was two: the other six state it perfectly well under headings nobody thought to search
for. The content was fine; the form made it unfindable, including to us.

**A vocabulary that rejected nothing.** The Phase 4 gate appeared to validate field names
against a menu. It did not — it only checked the axis key's suffix, and the field names
that actually ship went unchecked. Injecting `ZZZ_totally_bogus_name` into a board passed
with zero errors. Under that gate, 158 distinct field names accumulated, 36 of them used
exactly once, and `base_color` and `base_colour` shipped side by side. The duplicate was
recorded in three separate audit files; the fourth file simply added both spellings to the
menu, which made the drift legal.

The pattern is the same every time. **The knowledge was real but it lived in a person, and
people forget.** None of these were physics mistakes.

---

## The disciplines

### 1. A recipe returns a state, not a number

Every derivation returns the value *plus* the exact inputs it used, the regime it decided
it was in, a machine-written sentence saying why, a confidence grade, its citations, and
whether it converged. A bare number cannot be audited later; a state can.

Lives in `engine/payload.py`.

### 2. Out of domain is a return value, not an exception

When a recipe is handed a body it cannot handle, it returns that fact with a reason,
rather than raising or — worse — extrapolating. The giant-dynamo recipe declines brown
dwarfs explicitly, because the source refuses to supply the luminosity track that branch
would need. Declining is an answer. Guessing is not.

This is what the heat-transport contradiction cost us: neither document declined, so both
applied.

### 3. Anchor on published values, never on our own output

A recipe's tests reproduce numbers other people published for known bodies — Jupiter at
9.0 G, ε Eri b at 19 G — within a stated tolerance. Testing our output against our output
verifies nothing at all. This discipline is what surfaced the 54× table error.

### 4. Tables are generated, never hand-keyed

Any worked example in a methodology document is regenerated from the same code that
implements it, and the check fails on drift. A hand-typed table is a copy of a value, and
copies drift.

Lives in `engine/dynamo_table.py`, wired into `scripts/check.sh`.

### 5. Dependencies are declared in a file, not remembered

`engine/chain.yaml` records which derivation needs which, in four kinds: `requires` (a
numeric input), `selects` (chooses which model applies), `influences` (forces a recheck
without necessarily changing the value), and `excludes` (considered and rejected — worth
recording so it is not reconsidered from scratch). Cycles are allowed but must be declared
with a citation; an undeclared one fails the check.

`engine/chain.py affects <node>` then answers "what do I have to look at again", which is
the question that used to be answered from memory.

### 6. Shipped values flow back, so model that too

A dependency graph over methodologies is not enough, because this is a curation
repository: values are decided, written down, and then *reused*. `geopotential_j2 = 0.023`
is not a conclusion — it is an argument to a 21-hour moon integration whose result becomes
another recorded decision, and the stability report notes that the oblateness reverses
which moon orbit is chosen. Change the interior and that run re-opens.

So the layer records three more relations: which node should produce each shipped field,
which shipped fields are computed from other shipped fields, and what consumes them.
The Proxima failure is exactly the second kind, and a methodology-only graph cannot see it.

Lives in `engine/bindings.yaml` and `engine/backflow.py`.

### 7. A vocabulary is only real if something rejects what is not in it

Field names are checked against a single enumeration, and a name outside it fails. There
is exactly one such list, because two lists drift against each other. Widening the list is
itself checked: a spelling variant cannot be admitted to the menu, since that was how the
last duplicate survived four audits.

### 8. Prose explains; typed fields carry

Where a decision was recorded as prose, several quantities ended up bundled into one
string — one field packs a body's composition, mass, equilibrium temperature and cloud
class together, and no machine can take it apart. Values belong in typed fields, one
quantity each with its unit. Narrative stays as the settings-book text that explains them.

Existing approved narrative is not rewritten. The work is to lift the values out of it.

### 9. Derive physical state; let an adapter encode it

What the recipes produce is a body's physics, not a config file for whatever renders it.
An adapter turns the physical state into the target's fields.

```
recipes  →  physical state (target-agnostic)  →  adapter  →  KSP cfg
```

This is not tidiness. Sixteen `pause_*` parameters were being maintained by hand on the
boards, and they are not physics — they parametrise a shape function in the game engine.
The physics is one number, the magnetopause standoff. Sixteen hand-kept encodings of one
value is what produced the Proxima failure; the same shape repeats in the radiation-belt
shell fields. Recorded as physical state, the encodings are regenerated on every build and
cannot disagree with their source.

It also answers a question that otherwise has no floor: what stops the vocabulary growing
forever? Each layer is bounded for its own reason. The engine is bounded by physics — a
body's state is a finite list of quantities, and the admission test is *"is this a quantity
with a unit, or a declared dimensionless or categorical state?"* A description is not a
quantity. The adapter is bounded by a schema we do not own and that does not grow with our
ambition. Neither bound pushes on the other.

---

## What this does not fix

These rules make errors *detectable*. They do not make the derivations right, and they add
real cost: every new value needs a binding, a citation, and usually a test.

One of the two structural gaps closed on 2026-08-25: interior structure is now derived
rather than assumed. The layer densities that four recipes each used to assume privately
are outputs of an integration, and the two lookup tables that stood in for them are gone.
What the solver cannot do it now **declines by naming the mechanism**, which is the part
that makes the remaining gaps actionable: three of the Alpha Centauri moons come back
"needs the equation of state for ices III, V and VI", not "too low density".

The other gap is still open. Nineteen shipped fields have no node that produces them at
all, mostly stellar appearance and activity, plus two (`color`, `ring_color`) that have
methodology documents but no entry in the graph.

## Related

- `engine/chain.yaml`, `engine/bindings.yaml` — the two declarations
- [Methodology index](methodology-index.md) — the recipes themselves
- [Tools](tools.md) — what to run
