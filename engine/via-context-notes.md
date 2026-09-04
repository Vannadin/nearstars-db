<!-- Brief 43 — chain.yaml 의 via 91개 중 35개가 공급자가 내지 않는 양을 가리켰다: 분류, 수리, 게이트 -->
# `via` versus `outputs` — what Brief 43 found and fixed (context notes)

2026-09-03. Five commits, one per step, as the brief asked: `12eb701f` report only · `4654393a`
classes 1 + 5 · `257721a5` class 3 · `886ff1b5` class 4 · `5c1df658` the gate. Verifiers: (병)
parallel seat (parser and triage, `via_triage.py`), (직) directing seat (the four sharpest
misroutes verified), (여기) work seat.

## 1. The finding

`chain.yaml`'s header defines `via` as *"넘어가는 양"*, and the file is the canonical graph. Yet
nothing read the field except `build_graph_page.py`, for a tooltip. The parallel seat parsed all
**91** via-edges against their suppliers' `outputs`: **35 (38 %)** named a quantity the supplier
does not emit. Triage (병), reproduced mechanically (여기, `check_via.py`):

| class | n | what it was | fix |
|---|---|---|---|
| 0 already gap | 1 | `body_class → dynamo_rocky via sub_neptune` | none |
| 1 rename | 5 | the quantity exists under another name | via renamed |
| 2 derivable | 8 | computable from emitted quantities, four of them *assembled across edges* | allowlisted, each row naming **which inputs combine** |
| 3 selects-discriminant | 10 | a label the consumer forms, carried on a `selects` edge that the header says needs no via | see §2 |
| 4 real break | 8 → **6** | no node emits it | `status: gap` with the reason on the edge |
| 5 misrouted | 3 → **2** | the quantity is emitted — by another node, or by the destination | re-pointed / renamed; one reclassified (§2) |

The header's own warning: *"근거 없는 엣지는 넣지 않는다. 그림을 위해 추측한 화살표가 이 프로젝트가
반복해 온 실수다."* Two arrows were pointing at nodes that do not emit what they promise
(`stellar_wind`'s **only** input was `star_physical via age`, and no node emits `age`;
`crater_state → hapke_shader_values via terrain` named the destination's own output), and one
promise was the supplier's list being short (below).

## 2. Three places the triage moved, said rather than absorbed

- **`star_physical → body_figure via p_rot` is not misrouted (class 5 → 2 rows).** It refs
  `body-figure-methodology.md@«| **α Cen A** | star (G2V) | P_rot 22 d | 4.6e-5 | **4.8e-7** | – | solar-anchored scaling (0.0105·q); ±~30 % from P_rot ±3 d, first star rows emitted under the always-emit policy |»`, the **α Cen A** row (P_rot 22 d, *measured*); the
  `spin_axis_inclination` edge refs `:244`, the **Fomalhaut A** row (P_rot *derived* from v sin i and
  i★). Two routes, both real, separated by their refs on purpose. The defect was `star_physical`'s
  output list lacking a measured stellar rotation period — and the DB does carry one
  (`rotation_measurements` ×212, `rotation_period_days` ×157 in `db/stellar_props_curated.json` and
  `db/systems/`), so adding `p_rot` is a kept promise, not a new unkeepable one (직, 여기).
- **Class 3 was handled two ways, not one (pre-registered ③'s shape).** Where the supplier
  *computes* the label it is declared as an output: `dynamo_rocky` gains `regime` (the RM22
  ladder's Ro_ℓ gate, computed and discarded); `tidal_heating` gains `radius_ceiling` and
  `plains_temperature` (the transport test's hard ceiling → Dante 521 km; the external-budget
  plains → 223 K, §6.3/6.5) — those two had been in class 4 and left it. For the other eight the
  supplier does **not** compute the label: five sit on `atmosphere_choice`, an *owner* node that
  declares numbers, and the rest are formed by the consumer from `t_eq`, `power`, or
  `retained`/`loss_rate`. Adding them to `outputs` would have declared a promise nobody keeps. The
  header says `selects` carries no via, so the via is dropped and the discriminant word moves into
  the edge note; the one `requires` edge (`plasma_source`, scope parent) now passes `power`.
  Deviation from the brief's step 3, argued here; the brief's own ③ registered it.
- **`circulation_regime`** was called the class table's own verdict; `omega0_class_table` outputs
  `p_init` (initial spin), and the advection-versus-radiation regime is `day_night_contrast`'s
  judgement (`tidally-locked-temperature-methodology.md@«### What sets the contrast: advection vs radiation»`). Treated as consumer-formed.

## 3. The six gaps, and what closes each

`fossil_bulge` (body_figure does not emit it; the upstream verdict exists as
`interior_layers.figure_relaxation` since Brief 39 — the gap closes when the figure solver reads
it) · `cooling_luminosity` (**the graph was more optimistic than the module**: `dynamo.py` already
refuses to supply L(M, age); the file now agrees with code that was right) · `rossby` (needs a
convective velocity and length scale) · `cmb_heat_flux` (wanted by two consumers, emitted by
none; one supplier, not two workarounds) · `spe_fluence` · `outgassing` (survey ㉓: the supplier
computes nothing yet).

## 4. Invariants checked at every step (여기)

`graph.components()`: one coupled core of **16** nodes, identical to `coupled_core`, before and
after every edit; `graph.undeclared()` empty throughout; `chain.py check` passes. **Branch ①**:
the misroutes fixed cleanly and the cycles did not move — `coupled_core` was never touched.

**How to read 35 → 15 → 0 open.** Not "twenty problems fixed". Only **6–7 were ever real**
(the six gaps plus the one already marked); the other ~20 were **a field doing four jobs** — a
passed number, a rename, a contribution assembled across edges, and a `selects` discriminant. What
was fixed is that `via` now means one thing, and the seven real breaks are named as breaks on the
edge. That distinction is the finding; a later reader who sees "35 mismatches, now 0" without it
will count wrong.

**Pre-registration ③ was under-specified, not unmet** (직, on reading the deviation). It said a
class-3 discriminant its supplier does not compute *"is a class-4 break in disguise"* — a binary
that treats a `selects` edge naming a discriminant as making the same claim a `requires` edge
makes. It does not: the header already says `selects` carries no via, so the third ending (drop the
via, keep the word in the note) was in the file's own rules and the branch list did not have it.
Registered as the pre-registration's gap, not as an unregistered outcome.

**The invariant is stronger than "unchanged" (감, 여기 reproduced).** Removing **all 19
`status: gap` edges** and recomputing the strongly-connected components still gives **exactly 16
nodes, exactly `coupled_core`**. The declared coupled core does not lean on a single edge nobody
can satisfy — the cycle is real physical coupling, not an artefact of gaps. `chain.py check` would
not have said this, because it orders with gap edges included.

**Instrument ledger — "a count without its rule is not a count."** The audit's first SCC pass gave
**20**, then **17**, then **16**, depending on whether `scope: parent` edges were followed and class
tables included, before it read `graph.py`'s rule (`t_eff_body` joins the cycle only through a
`scope: parent` edge to `moon_energy_budget`). Third instance tonight of a locator or count that
looks complete and is not — beside the pdftotext line numbers without their extraction mode and the
directing seat's unstated `T_s = 1600` on Brief 39.

Result: **83 via-edges, 15 mismatches = 8 allowlisted + 7 `status: gap` + 0 open.** The gate
(`check_via.py --gate` in `check.sh`) fails on any via outside those two lists. pyyaml is not a
new dependency (`chain.py`, `check_pipeline_flow.py`, `check_phase4_gate.py` already import it on
unconditional `check.sh` paths — verified, not relayed).

**What the gate cannot see — first instance (Brief 46 audit).** `check_via` asks *"does a `via` name
something its supplier does not emit?"* It cannot ask *"is an input read that no `via` names?"* — an edge
with `via: None` is invisible to it. Brief 46's recipe read `interior_layers`' derived radius with no
`interior_layers → internal_heat_nontidal` edge declared at all, and every in-edge to that node carried
`via: None`; the gate passed. So the gate catches **wrong arrows, not missing ones**. Extending it needs to
know what a recipe reads (its `Result.inputs` against the declared in-edges' `via`s) — a separate, harder
question; recorded, not built.

**Free fix recorded for the `dynamo_rocky` build**: `regime` is now a declared output, so the
node's recipe must emit it when built.
