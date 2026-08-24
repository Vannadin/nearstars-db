# Backflow layer — context notes

Decisions taken while building, and why. Append as work continues.

## Bind by field name, not by row

969 field instances, but only 158 distinct field names across 7 boards — `mass`, `radius`,
`geopotential_j2` recur once per body. Binding the name carries to every body that has it,
and a new board inherits the bindings for free. Binding 969 instances would have to be
redone per system and would rot immediately.

The cost of this choice: a field name that means different things on different bodies gets
one binding. `composition` on a ring is not `composition` on a mantle. Watch for it — if it
shows up, the fix is to bind on `(axis, name)` rather than `name`, which is a mechanical
widening, not a redesign.

## Three edge kinds, not one

The first sketch had only `produced_by`. That misses both real failures:

- Proxima was `derived_from` — one shipped value is the parent of another shipped value,
  with no methodology in between.
- The J₂ case is `consumed_by` — the shipped value leaves the board entirely and enters a
  simulation, whose result comes back as another shipped value.

A layer with only `produced_by` would have caught neither, which is to say it would have
been decoration.

## `bundled` is a flag, not a fix

~116 of 969 values pack several things into one string. The split cannot be automated: a
sampling pass tried to separate "value + its evidence" from "outputs of several nodes" and
mis-classified visibly, because the parenthetical carries both kinds of content freely
(`~25× 지구 (Weir canon; 강한 이유=높은 코어 열플럭스…)` is value + rationale;
`temperate Saturn (H₂/He, 120 M⊕, Teq 225K, Class I/II clouds)` is four nodes).

So the flag records the debt rather than paying it. The point is that `impact` can then
report "of the N rows this re-opens, M are bundled and cannot be re-derived until split" —
which turns one undifferentiated 116-item chore into a per-node queue, ordered by what
recipes actually reach. Bundles nothing reaches never need splitting.

## Bindings live beside `chain.yaml`, not inside it

`chain.yaml` is about methodologies and stays readable at 44 nodes. Bindings are about
shipped instances and will grow with every body added. Different lifetimes, different
review cadence, so a separate file — but validated together, so a binding cannot name a
node that no longer exists.

## What this layer is *not* allowed to do

It records what the boards already say. It must not become a second place where physical
values live, or it recreates the exact disease it exists to detect. `produced_by` names a
node; it never restates the value.
