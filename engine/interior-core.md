<!-- 내부구조 솔버를 "끝났다" 고 말하려면 남은 것 — 코어 작업 목록 -->
# Interior solver — the core list

What remains before the interior solver can be called finished. Not a wish list: every
entry here is something **this recipe can close by itself**, and closing all of them is the
definition of done for this tool.

The information was scattered across the methodology document's domain table, six sets of
context notes, and a review file that is now half stale. Asking "what is left" meant
re-reading all three and getting a slightly different answer each time. This is the one
place.

**Order, set by the owner 2026-08-29: C1 first, then down the list in number.** No entry
depends on another, so the numbers are a queue rather than a chain; an entry that closes as
*"recorded, not found"* still closes.

**Keeping this file alive.** C2 was stale within a day of being written. So each brief's
Landing section carries one checkbox — *update the matching row in `interior-core.md`* — and
a row is not closed by the work being done but by that line being written here.

**Prose that carries a number carries the duty to update it.** Notes, domain rows, tables —
wherever a number sits, when the code moves that number the same commit either fixes it or
dates it *interim, superseded <date>*. Three times a note fell behind the code (C2 within a
day; the domain row that stated Neptune's "1797 K, three kelvin under the floor" as fact; the
H/He note's Saturn +2.09 % after the gas-layer temperature carry moved it to +7.06 %), and
the rule above only covered core rows.

**Labels are re-checked at their place in the text, not only the constants.** When a
transcription is verified against a source, the equation number itself is confirmed to sit
where the text puts it. Constants that are right hide a wrong label, and the next reader who
follows the label opens the wrong equation — the same failure as a fabricated DOI that
resolves to a real, unrelated paper: the form is plausible, so it passes. (C8 wrote Noack &
Lasbleis's R_p scaling as their eq. (8); it is their eq. (5), and (8) is X_CMF. The constants
were right, eight labels were not.) **And when one file carries two papers, the same number
can exist twice, so a label is written with the paper's name** — `Noack & Lasbleis eq. 5`,
never a bare `eq. 8` — which is how `test_interior.py` came to hold Unterborn's real eq. 8
beside a mislabelled Noack & Lasbleis eq. 8 without either looking wrong. That is the fourth
kind of plausible-because-well-formed failure this list has met, after the fabricated
identifier, the stale number and the label slip: the same number from a different paper.

**When a source is baked, its claimed range is swept against physical criteria registered
in advance, and the effective ceiling is measured and recorded with the table.** A label can
be verified faithfully at its place in the source and the source's own claim can still
break in execution — the fifth kind of plausible-because-well-formed failure. SeaFreeze's
`water2` (water2 item, 2026-08-30) carries knots to 100 GPa and AQUA quotes that as its
range, and the spline returns negative densities inside it; the effective ceiling (2.3 GPa
at 360 K rising to 30 GPa at 1000 K) was found by a sweep whose criteria — ρ finite and
rising with P, 1000 < c_P < 15 000 J/kg/K, dT/dP|_S > 0, no runaway in successive density
increments, two cells of margin — were fixed *before* the sweep, so the ceiling could not
drift to wherever the results looked odd. **Pre-registration is the point**: without it,
"as far as it looks fine" is an impression, not a verdict. `fermi.py`, `hhe_table.py` and
`ammonia_table.py` already meet this in their own ways; it is stated here so the next baked
table does too.

**Relays without verification, in both directions.** *Downward*: a number without its label
does not enter a brief. *Upward*: **a number that changes a verdict is reproduced by the
directing session before it goes to the audit.** Verdict-changing, specified in advance so
it is not judged by impression: (a) a number that opens, closes or reopens a row; (b) **a
first claim that a published value is contained or reproduced**; (c) a number that moves an
anchor; (d) a number that changes a grade. The directing session's reproduction does **not**
replace the audit's: a verdict-changing number is computed by the working session,
reproduced by the directing session, and reproduced again by the audit. The five failures
that produced these two sentences are one disease in two directions — four unlabelled
numbers travelling down into briefs, and one headline (C11's "Titan is inside a declared
band", 2026-08-30) travelling up without reproduction; the rule above stops the first and
this one the second.

**The disease is independent of role.** On 2026-08-30 it fired once in each of the three
sessions: the directing session put unlabelled numbers into briefs (four times); the working
session wrote a gate time it had not measured; the audit session joined the triple point's
pressure (14.6 GPa) to an isotherm's temperature (905 K) into one pair and took it for a
melting point (Queyroux+ 2020 — the pressure belongs to 14.6(5) GPa · 850(20) K, the
temperature to an isotherm whose melting pressure the Letter does not print). What stops it
is not the role but the label and the prior reading — and the procedure held: the audit had
fenced its own suggestion with "read first · do not quote · direction only", so the mistaken
pair was read before it was used and never reached a verdict. An error occurred and the
procedure caught it; "it passed the audit" is not a reason to skip the reading.

**False provenance — the label is present and false.** Registered as sub-kind 7 by the
audit, and worse than a missing label, because **a label stops verification**: a reader who sees "the
value you gave me" checks nothing. (2026-08-31: a relay message attributed Neptune's J₂ as
3538.0×10⁻⁶ "from your message" — the message had carried only (2/3)J₂ and the source name;
the digits were filled from memory and labeled as received. NH22 Table 1 prints 3535.94.)
This is **the only sub-kind whose check lives in someone else's hands**: a fabricated
identifier is caught by holding the title against the original, but a false attribution is
caught only when **the attributed party compares it with what they actually sent**. The
prescription is therefore a pair — *sender*: quote only what sits inside quotation marks;
never fill in a number the other party did not say and label it "yours"; a filled value is
marked "filled by me". *Receiver*: a number someone attributes to you is compared against
what you actually sent before it is accepted. And the verification is **exhaustive, not
sampled**: in the case that named this, the same message's Uranus J₂ (3510.7) happened to
be right, so a spot-check would have passed both. Scope, stated precisely: the error lived
only in the relay message; the notes' printed values (3510.68 / 3535.94) were correct.

**A third party checks a solver by closure, not by A/B against a harness whose brackets it
does not own.** Registered 2026-09-01 by the audit, against its own instrument. Verifying the
region-3 Newton inversion, its first two bisection harnesses reported a worst disagreement of
**0.4** — and both were the harness's fault: the first bisected globally across a
non-monotonic stretch below T_c, the second used a lower bracket of 50 kg/m³ while the hot
low-pressure root sat at 34.3. At the worst point the audit evaluated **p(ρ_Newton) = 17.0 MPa
against p(ρ_bisection) = 24.3** and judged, on the spot, that **Newton was right and the
instrument was wrong**. It then changed the final check from A/B to **root reproduction** —
does the returned density close the equation it was inverting — and got worst **8.6e-13**.
The general form: an A/B against the previous implementation is the *implementer's* check,
because they know the old brackets; **an outside leg's check should be one that cannot inherit
the old method's assumptions**, and a closure test is that. A verification harness is code, and
code that disagrees with the thing it verifies is a suspect, not a verdict.

**An unreachable boundary condition should close as a named refusal, not as a failure to
converge.** Proposed by the audit 2026-09-01 and recorded here as the ice axis's settling path.
The four ends of Brief 23/25 are currently `conv=False`, which reads as *"the solver could not
do it"* — but the measurement says something stronger and more specific: **no central
temperature reaches a 76 K surface, because the `h_he` table has no state below ~1830 K at
130 GPa.** That is the same kind of statement every material ceiling in C6 makes, and this
list's standard is that a refusal names its mechanism and its citation. Once the controller can
*conclude* rather than cycle (the second defect above), these ends stop being an unfinished
measurement and become a **recorded refusal with coordinates** — which is a closeable state,
where "did not converge" is not.

**A sentinel carried in a variable something else re-arms is not a contract.** Registered
2026-09-01 from the temperature loop's non-termination. The loop meant to extend its pass
budget **once**: on running out it set `bracketed = "extended"` and checked for that sentinel
before extending again. But the deviation test re-armed `bracketed = True` on every pass that
failed to contract, overwriting the sentinel, so *"one more set, only once"* re-fired every
time the budget hit zero. A converged attempt was measured at **51 attempts against an
intended ceiling of 29** (1 + 14 + 14). The repair is five lines: a dedicated `extended` flag
that nothing else writes. **State that encodes a promise gets its own variable** — a value
doing double duty is a promise anyone downstream can silently revoke.

**And it is the cold flank again, in a new form: the climb hid the wall from the controller.**
The four members registered on 2026-08-31 were trial refusals *killing* a solve. This one is
the opposite failure with the same cause — the temperature loop lowers by ratio, meets a
too-cold refusal at 130–152 GPa (the H/He envelope's base), and the attempt's internal climb
(×1.6) carries it back up to the same ~360 K surface, so **the controller never learns that
its target is unreachable from below** and cycles forever instead of refusing by name. A wall
that a trial path climbs away from is a wall the answer never gets told about. Brief 22 taught
trial refusals to steer the bracket; this says the steering must also be able to **conclude**.
It was invisible before region 3 was baked, because every trial died in the steam wedge first —
which is why the earlier four-end measurement finished in 195–246 s.

**A process listing is an instant, not a state — and a serial chain is invisible between its
steps.** Registered 2026-08-31 by the directing seat, against itself. After the work session
was compacted, this seat ran `ps` for `python|check.sh`, saw nothing, and reported *"the run
never started"* as measured fact. The chain was alive — started 22:27 — and the work session,
trusting that report, launched an identical chain at 22:53; **two copies of the same solve ran
at once on a machine whose owner had spent the day fighting thermal throttling.** The `ps` was
not wrong about its instant: a chain that runs its steps sequentially shows **no matching
process in the gap between two steps**, and a single sample lands in that gap often enough to
be useless. The same seat had, an hour earlier, used `ps` correctly to find two 31-hour ghost
processes — which is exactly why the second reading felt authoritative.

The prescription is a pair, and it mirrors sub-kind 7's. *Reporting*: process state is
reported with its sampling — "no match in one `ps` at 22:5x", never "it never started" — and
liveness is established from something durable (the task's own output file growing, a
timestamped log, the launching session's own record), not from absence in one listing.
*Receiving*: **a session about to re-launch work checks for itself before starting**, however
the report reads; the cost of a duplicate heavy run is paid in someone's battery and fan, and
the check costs a second. The work session drew that conclusion unprompted and it is the right
one.

**A runtime estimate belongs to the code state it was measured on.** Same event, second
lesson. The "~15 minutes" this seat put in a brief was measured on the four ice-axis ends
before region 3 existed, when every path stopped early at the wall. With the wall filled the
paths integrate all the way, and the first solve passed **two hours of CPU** without printing.
The number was honest when taken and false when quoted, because the thing it measured had been
replaced in between — so a timing carried into a brief carries the commit it was taken on, or
it is not carried.

**A number whose source was not stated is quoted without one — you do not supply the
provenance.** The receiving half of the rule above, registered 2026-08-31 by the work session
against itself. The brief said only *"about 15 minutes"*; the checklist and the commit message
that quoted it wrote *"measured on the runs that died in 1 s at the wall"* — a provenance
inferred from the diagnostic story around it and then written as fact. The figure was in fact
measured on the directing seat's four full integrations (195 / 246 / 213 / 212 s, all
`conv=False`, on paths that stopped early at the wall). Nothing downstream moved, and the
sub-kind is still worth its line, because **an invented source is harder to catch than a
missing one**: a reader who sees a provenance stops looking for it — the same mechanism as
sub-kind 7, arriving from the other direction. The correction was made in place with a
correction commit rather than by rewriting an already-quoted hash.

**A new number is carried back to the old ones before it is used to clear them.** Registered
2026-08-31 by the parallel session, against itself, and it is its own kind because nothing was
misread: having established that the ice ladder's data ceiling is ~355 GPa, it wrote that
"every anchor sits far below 355 GPa" — while the ice giants' mantles reach 820 and 1016 GPa,
a table it had read that same morning. The anchors *are* safe, for a different reason
(`ICE_VII_X_T_MAX` = 1800 K, above which Mazevet carries the column), so the conclusion held
and **the condition was inverted**: not "safe below 355 GPa" but "safe above 1800 K", which
sends the next reader looking for danger in exactly the wrong place. The others in this list
are failures of reading; this one is a failure of *re-reading* — a new measurement obsoletes
the safety statements standing around it, and clearing them requires opening them again, not
recalling them. The check is cheap and its absence is invisible, which is why it is written
down.

**A correction request is itself a labelled claim, and it is opened before it is sent.**
Registered 2026-08-31 by the audit, against itself. Reviewing the directing seat's handoff,
it asked that C13's 26 % / 41 % be marked as standing on two of three legs, with the work
session's reproduction and two caveats outstanding — and wrote *"`19360f72` already records
the row as revisited"* while never opening `19360f72`, whose checklist closes all three and
whose §6 table reproduces the audit's own float-residual point to the digit. The correction
was withdrawn the same hour. Two known sub-kinds combined: a number left stale (2), resting
on an identifier cited but not read (the shadow of 1). What makes it worth its own line is
the direction — **the list was ahead of the ledger, not behind it**, so "the row closed
before verification did" was the exact inverse of what happened, and a correction accepted
on its face would have re-opened a settled row. Hence the pair: *sender* — the moment you
write "X already says so", X is a document you have opened, exhaustively, not by title;
*receiver* — **a correction is reproduced before it is applied**, the same duty as a number
attributed to you. The incoming seat reproduced it and it did not survive, which is the
only reason this is a recorded lesson rather than a re-opened row.

**A retrial's outcomes are registered before it runs, and the register now has five kinds:**
sits with A · sits with B · between · the source does not reach the deciding region (added
after F1) · **the source disagrees with both candidates** (added after F4, where Queyroux sat
above IAPWS and Reinhardt alike) — in which no reopening condition fires, the band's question
is rewritten from "which one" to "how wrong are both", and the grade keeps its word while its
reason changes. Two unregistered results in a row meant the list was young; every retrial
brief now carries all five.

**A discriminating test states, beside each prediction, the assumption that prediction
stands on, and its register includes the default ending "every prediction misses = the test
itself failed; the product is the name of the wrong assumption."** Born in C12 (2026-08-31):
the test's (나) prediction — "our water lands on the printed density" — carried the unspoken
assumption that the water-only profile's material is pure water, forgetting the H/He of a
three-layer model's inner envelope; when every prediction missed by 18–32 %, the result was
not a reading chosen but an assumption exposed. This is a rule about the tool, not about the
evidence: the outcome register classifies what the evidence did; this classifies what the
test could not do.

**A trial-path refusal steers the bracket; it does not kill the solve.** The refusal
machinery exists to keep the **answer** honest — every material stops where its evidence
stops (C6) — but the shoot and temperature loops route their *trials* through the same
refusals, so a solve could die in a state no converged answer would occupy. Repeated
sightings in two days (C11's over-broad refusal · the Queyroux–Neptune route death ·
C13 end B's stack-build death, sharpened by the 1 ULP that separated a 1 s refusal from a
112 s convergence) made it structure, and Brief 22 (2026-08-31) repaired the corridor's
three static spots: the centre seed dispatches fluid/solid like a step; the pressure
bracket's ceiling respects the dispatch (a hot centre is the fluid's, whose fit states no
pressure cap — a **cold** watery centre still stops at the ladder's 1 TPa by name); and
the fluid↔solid **availability seam** at exactly that cap — which the in-step boundary
finder can land a trial on — throws too_cold with the local temperature instead of a
temperatureless cap refusal the shoot would mis-read as geometry. Acceptance was
pre-registered and measured: end B solves with no stub under either `imf` expression, and
the Queyroux-window Neptune converges to the anchor's own solution. The distinction to
keep: **evidence caps are real for answers** (the cold refusal survives, tested), **and
representational for trials**. `engine/cold-flank-context-notes.md`.

**A table is regenerated on the code that ships, in the commit that ships it — and when the
regeneration differs, which side is right is settled by a separate trace.** The sub-kind's
name ("the table ran ahead of the code inside one commit") invites doubting the table first;
in the case that named it (C11, 2026-08-30) the table was right and the code had regressed —
an over-broad refusal written after the table removed a converged member. Regenerate, diff,
then trace; do not correct the table to the code, or the code to the table, on the name alone.

## Where the line is

Not by body class — by **what is missing**.

**In:** the missing thing is a material, a structure, a declaration, or a wire. The recipe
can reach it.

**Out:** the missing thing is physics the hydrostatic integration does not contain, or a
node that already exists elsewhere.

| out of scope | why |
|---|---|
| brown dwarf | deuterium burning above ~13 M_J puts an energy source inside the body. Not an input this recipe lacks — a term the equations do not have |
| star | the stellar C/MR² is the n = 3/2 polytrope value 0.205 (Chandrasekhar 1939), already on a separate `body_figure` branch |
| evolution and cooling tracks | age-dependent envelope thickness and luminosity belong to `internal_heat_nontidal` and to nodes not yet written |
| gate economics | the gate ran 14:12 → 14:22 → 17:44 and the cost was twice *recorded, not repaid*. Not solver physics — but it belongs on **a maintenance list of its own**, written down here only so it cannot fall between the two. Two small fixes ride with it: the conditional `_LAST_INVERSE` line, and a double-cut test for a thin layer |

**Sub-Neptunes are in.** What they lack is a gas mass fraction, which age and irradiation
set — an *input*, not physics. This recipe already takes six such inputs by declaration and
drops its grade for each: `ice_allowed`, `tidal_heating`, `initial_porosity`, `envelope_z`,
`potential_temperature`, `core_cmb_temperature`. A seventh is the same move, not a new
standard.

## The list

### C1 — Sub-Neptunes, and the defect hiding behind them — **closed 2026-08-30**

The sweep (5 M⊕ · CMF 0.20 · 500 K at 1 bar) now solves at 2, 5, 10, 20 and 30 % gas and
declines at 50, 80 and 100 % citing the hottest bound solution and the wall above it —
neither sentence mentions a ceiling. `sub_neptune` is off `FLUID_CLASSES`; `gas_mass_fraction`
is the seventh declaration. GJ 1214 b (8.41 M⊕, 2.733 R⊕) is reproduced by 1.5–2.4 % H/He for
1-bar temperatures of 350–250 K, inside Valencia+ 2013's < 7 % and beside their ~3 % for a
solar-metallicity envelope.

Both measurements were wrong: the 17.7 M⊕ row was the polytrope era's, the "0 M⊕ since the
table" of 2026-08-28 was the same defect as the sweep's refusal (the envelope base cut off as a
surface), and the cap re-measured with the defect fixed was 11.46 M⊕ (interim, superseded
2026-08-30 F2: 16.69 M⊕ once the bulk-modulus finite difference stopped poking past the
silicate ceiling on the shooting's ceiling trial). Under it were three defects, none a ceiling: the
integrator took the envelope base leaving the H/He table's reach line for the 1-bar surface,
so the envelope had no mass; the temperature loop's proportional update diverges when the
1-bar temperature scales faster than the central one (thin envelopes on heavy cores); and a
ladder seed already over the target fell onto the inflated branch of the U-shaped surface-mass
curve. Each fix is gated so that no anchor path enters it, and the bit lines say so.
`engine/sub-neptune-context-notes.md` has the measurements.

Left open, named: a sub-Neptune now integrates but has **no dynamo path** — `core_state`
declines by class, `dynamo_giant` excludes it by mass, `dynamo_rocky` does not take the class.
Recorded as a gap edge in `chain.yaml` (`body_class → dynamo_rocky, via: sub_neptune`); not a
solver item, so it is not on this list.

### C2 — The ocean layer, and multi-axis inversion — **closed 2026-08-29**

Liquid water came from SeaFreeze's `water1`, the phase switch is pinned inside the
integration step the same way layer boundaries are, and `infer_three_layer` returns a band
over the core axis, narrowing only when a measured C/MR² is supplied. Grid phase 2e-3 → 8e-7,
asserted at the gate. Condensed anchors bit-identical; `chain.yaml` cycle 7 declares the
phase → density → temperature loop.

Two of the five icy anchors came inside — Ganymede 2.1 % → 0.4 %, Europa narrowed to a 7 %
core under a 104 km ocean. **The other three moved the question rather than answering it,
which is C10.**

Reasoning: `engine/ocean-layer-context-notes.md`.

### C3 — The melting-curve gap, and dispatch by class — **closed 2026-08-30**

The ice material is now chosen by the local (P, T) against two published lines, never by
`body_class`: IAPWS's melting curve to 20.6 GPa, then Reinhardt+ 2022's liquid–solid line
(to 52.4 GPa) and its ice VII′–VII″ line (to 70 GPa), baked from the paper's public data by
`tools/make_ice_melt_table.py`. Below the VII′–VII″ line the column is the condensed ladder;
above it, VII″ and the liquid alike go to Mazevet's fit, whose floor is now the paper's own
1000 K rather than the ladder's 1800 K ceiling. Every result names the phase at both ends of
the column and the line it was measured against. Neptune's envelope base at convergence is
39 GPa · 2 555 K, 999 K above the liquid line — fluid for a stated reason. The seam at
20.6 GPa is +26 % in melting temperature, measured and stated; the grade is analog because
the lines are simulation.

Two things came out from under it. The "1797 K, three kelvin under the floor" was a trial
path, not the converged point; and Neptune's old convergence was luck — the 1-bar
temperature was jagged in the central temperature by ±0.4 K because the closing
extrapolation read its adiabatic gradient at a grid-bound step start. The gradient is now read
at the exit point and the temperature loop keeps its best pass; Uranus moved +3.8 × 10⁻⁵ in
radius, Neptune −2.8 × 10⁻⁴ (6 308 → 6 296 K at the centre), both reported in
`engine/melting-curve-context-notes.md`. Above 70 GPa no line reaches and none is invented:
the verdict says "fluid or superionic" with Millot+ 2018's one point.

**The seam is itself under review.** Kimura 2023
([`2023JChPh.158m4504K`](https://ui.adsabs.harvard.edu/abs/2023JChPh.158m4504K), *Revisiting
the melting curve of H₂O by Brillouin spectroscopy to 54 GPa* — a measurement across the whole
Reinhardt range, on the owner's paper-request list; bibcode checked by title, this session and
the audit session) becomes the arbiter of the disputed band when it arrives: its product is
not only a possible grade upgrade but a **re-verdict of the band (16.5–20.6 GPa / 715–902 K)
and a possible narrowing of the seam's width.**

**Revisited 2026-08-30 (F1), with the criterion fixed before the comparison.** Kimura &
Murakami measure melting only from 25.9 to 53.6 GPa (their lower rows are liquid runs at a
temperature *estimated from Queyroux's curve*). Against Reinhardt's line, six of their seven
melting points sit inside their own stated ±130–150 K, and the one outside (25.9 GPa) is the
measurement *hotter* than the simulation by 171 K — away from IAPWS, not toward it. At the
seam their Simon–Glatzel fit (eq. (2), anchored on Queyroux's 14.6 GPa · 850 K triple point)
gives 1028 K (968–1155 at 1σ): +14 % above Reinhardt and +44 % above IAPWS's 715 K.
**Kimura sits with Reinhardt; the step is not an artefact of the simulation.** C3 stays
closed, the seam number stands, the dispatch is unchanged, and the grade stays analog
because the check's own error is 8–11 % and it does not reach the seam. The band is not
narrowed: the measurement gives no support to IAPWS's end. Table I enters the gate as a check
table. What would still move this is a measured point between 15 and 26 GPa — Queyroux+ 2020,
now in the cache. `engine/seam-retrial-context-notes.md` has the tables.

**Revisited 2026-08-30 (water2): the open defect this row named is filled, not overturned.**
The band with no equation of state — liquid water above the ocean table's 2.3 GPa (or above
its 500 K) and below the hot-water fit's 1000 K floor, the one F2's Callisto and Titan at
f = 0.75 walked into — is now carried by SeaFreeze `water2` (Brown 2018,
2018FlPEq.463...18B; range as AQUA §2.3.5 states it, *"liquid and supercritical H₂O from
1 GPa to 100 GPa and up to 10⁴ K"*), baked ragged to the spline's **real** ceiling, which is
not its knot box: SeaFreeze's `water2` returns negative densities inside 100 GPa — valid to
2.3 GPa at 360 K, 10 GPa at 600 K, 13 GPa at 700 K, 30 GPa at 1000 K, hugging the liquid
side of this row's melting curve. Two seams measured: water1 ↔ water2 in their overlap ρ
0.13 % / dT/dP|_S 9 %; water2 ↔ Mazevet at 1000 K, Mazevet 2.5–3.3 % less dense over
2.3–26 GPa. Still uncovered by name: 12–20.6 GPa between the melting curve and the ceiling
(≲ 170 K wide), and hot water below 0.1 GPa. `engine/water2-context-notes.md`. C3 stays
closed; the dispatch by (P, T) is unchanged, one more material answers it.

**Parked at the gate 2026-08-30 (F4, Queyroux at the seam).** The band 16.5–20.6 GPa has
one measurement, Queyroux+ 2020 (2020PhRvL.125s5501Q, the arbiter's seat, independent of
Kimura 2023), and this repository holds its six-page Letter but not the Supplemental Material
that carries the individual melting points (Table S1). The values printed in the band —
15.6(2) GPa at 905 K and **18.4(9) GPa at 944 K** — are the ice VII″ → VII′ **isostructural
solid transition** on two isotherms (§*Isostructural transition*; Fig. 1 keeps "melting line"
and "isostructural solid transition" as separate symbols), not melting points; the triple
point is 14.6(5) GPa · 850(20) K. F1's criterion, reused, has nothing to put a residual inside
of, and a fit cannot reopen a row, so the fourth branch fires and nothing moves. What the
Letter does give is a **bound**: liquid at 15.4 GPa · 944 K (Fig. 2a) and solid at 18.4(9) GPa
· 944 K put T_m(18.4 GPa) above 944 K — above IAPWS's 690 K by 254 K and Reinhardt's 801 K by
143 K, the direction and size of Kimura's out-of-band point. Recorded as orientation, not a
verdict. Table S1 (free from APS, requested from the owner) is what would run the item.
`engine/queyroux-seam-context-notes.md`.

**Revisited 2026-08-31 (F4 resumed): Table S1 arrived, and the measurement sits with
neither curve — it is hotter than both.** Twelve measured melting points (Queyroux+ 2020
Supplemental Material Table S1, read from the PDF), three inside the band: 16.6 ± 0.5 GPa ·
930 ± 10 K, 16.6 ± 0.2 · 944 ± 10, 17.3 ± 1.1 · 978 ± 10. Against them IAPWS eq. (5) is
255–297 K cold (25–30 σ) and Reinhardt's line 213–228 K cold (21–23 σ); at every point from
8.4 to 17.3 GPa both curves are on the cold side, IAPWS already 69–79 K (14–16 σ) cold at
8.4–8.8 GPa. So of the three registered outcomes none fires as written: not "with Reinhardt",
not "with IAPWS" — **C3 does not reopen** — and not "between" but *above both*. The band is
redrawn to what the data support: **both curves too cold by 210–300 K at 16.6–17.3 GPa**,
Reinhardt the less wrong by 40–70 K; the +26 % step is in the measured direction and not
large enough; the dispatch is unchanged because the recipe has no third curve, and adopting
Queyroux's points as a melting-curve source is an owner decision with this table as its
grounds. Above 27 GPa (σ_T = 100 K) Reinhardt is inside at 27 GPa and hotter than Queyroux by
160 and 239 K at 36.7 and 44.7 GPa — while F1 found it inside Kimura & Murakami's ±130–150 K
at six of seven points; the two experiments differ by the 100–150 K Queyroux themselves
report against the laser-heated family, and this recipe does not adjudicate between them.
Grade: the measurement clears the 5 % bar (σ_T/T_m 0.7–1.3 % to 17.3 GPa) and the curves do
not clear the measurement, so analog stands with a new reason — the one measurement in the
band sits 210–300 K above both lines. Table S1 is a check table in `test_interior.py`.
Two ways a check can fail to raise a grade, now both on record: F1's — the check's own error
(8–11 %) is larger than the scale, so it cannot see; F4's — the check is precise enough
(0.7–1.3 %) and **the thing checked is wrong**. The grade word is the same; the reasons are
opposites, and the second is the one that names what would have to change.

### C4 — Ammonia and methane — **closed 2026-08-30, unbuilt; reopened 2026-08-30 for ammonia and closed again for that half, built**

The ice-giant envelope is water alone, standing in for a water–ammonia–methane mixture. That
is the field's own convention, but it is a stated substitution and **its price is not
quantified** — not bounded, not estimated. Bethkenhagen+ 2017's 2.1 % is the deviation from
*mixing three components you already have*, not the cost of replacing two of them with the
third; `eos.py` states the distinction correctly. The number only comes into existence when
the tables do, and the tables cannot be reached from here. Three routes, checked on
2026-08-27 and again on 2026-08-30:

| route | why it fails |
|---|---|
| Bethkenhagen+ 2017 (2017ApJ...848...67B, full text in the cache) | describes the grid exactly — 1000 GPa · 20 000 K, thirteen isotherms — and publishes no data-availability statement and no URL |
| Bethkenhagen+ 2013 (2013JChPh.138w4504B, doi 10.1063/1.4810883), the ammonia source | AIP paywall; 330 GPa · 500–10 000 K, the set 2017 extended |
| FPEOS, Militzer+ 2021 (2021PhRvE.103a3203M) | distributes tables and code, and carries CH₄ — but **no NH₃**, and its range 10⁴–10⁹ K begins above the ice-giant adiabat (5500–6300 K) |

**An author request is the only remaining route.** Bethkenhagen+ 2013 goes on the owner's
paper-request list; the 2017 tables would come from the same authors.

What can be said about the sign, in three tiers, only the first carrying a number:

- **composition** — direction **+**, it *widens* the residual. The solar-ratio mixture
  (0.31 : 0.08 : 0.61 CH₄ : NH₃ : H₂O by mass, Bethkenhagen+ 2017 §V) has a mean molecular
  weight of 17.28 against water's 18.02, so water overestimates the ice density by 4.27 % at
  equal number density (*derived*); electrons per unit mass agree in direction (H₂O 0.555,
  NH₃ 0.587, CH₄ 0.623 e/amu, *derived*). Correcting it lowers the density and enlarges a
  planet the model already makes too large, on a ~1.5 % radius scale (*derived*).
- **thermal** — mechanism named, **sign ungrounded**. Atoms per unit mass run H₂O 3/18 <
  NH₃ 4/17 < CH₄ 5/16, so the ideal-gas intuition is a higher heat capacity, a shallower
  adiabat, a colder and denser interior (Bethkenhagen+ 2017's icy Uranus is cold, T_core ~
  4000 K), pulling the radius back. Dissociation at high pressure shrinks that difference
  and with it the sign; no direction is defended.
- **net** — needs the tables.

Writing "1.5 % worse" would quote the first tier as the third.

C5 was attributed on 2026-08-30: the ice giants' residual belongs to a thermal boundary
layer at the transition between the ice/rock interior and the H/He envelope and to the
inner mantle's ice:rock ratio (Nettelmann+ 2016), with non-adiabatic interiors the review's
own open question (Helled+ 2020). **C4 is not a candidate for that residual in either
direction**, so closing it unbuilt costs the recipe nothing it was counting on.
`engine/ammonia-methane-context-notes.md` has the search.

**Reopened 2026-08-30 for the ammonia half** — the registered overturn condition fired: the
owner obtained Bethkenhagen, French & Redmer 2013 and **the table is printed inside it**
(Appendix B, Table I; no repository, no fit — the printed table is the distribution). The
closure above assumed it was out of reach; it was not. The methane half stays closed as
written — nothing new bears on it.

**Closed again for ammonia, built.** `engine/ammonia_table.py`, baked by
`tools/make_ammonia_table.py` from the cached PDF's text layer and checked against the
printed page: 93 points on a **ragged** grid (500 K to 1.5 g/cm³, 700 K to 2.0, 1000 K and
above to 3.0; 0.309–333.2 GPa), the five asterisked points carried as a 5 % flag against the
paper's 2 %, nothing interpolated across the six absent cells. The material `nh3`
(`eos.Ammonia`) refuses outside the table by name. **The convention is stated and tested**:
the caloric column includes the vibrational correction (2013 Appendix B) — the correction
Bethkenhagen+ 2017 §II.4 removed from this set — and the exposure is c_P / ∇_ad only, never
the density mixing. The ice-giant adiabat (5500–6300 K) lies between the 5000 and 7000 K
isotherms: **interpolation, not extrapolation.** Interpolation error, leave-one-out at
doubled spacing: 8.7 % in the mantle region (ρ ≥ 1 g/cm³, T ≥ 2000 K), 17.3 % in the low-density dissociation corner.

**What the table settles, and only that.** Water (Mazevet+ 2019) and ammonia (this table)
read at the same (P, T) at eight points — four on the engine's own solved Uranus profile
(50–250 GPa, 2830–3950 K) and four bracketing the central temperatures — mixed by additive
volume at the solar-ratio pair fraction w_NH₃ = 0.1159: ammonia is 21–24 % less dense than water at
equal (P, T) — the equal-number-density μ argument (5.5 %) was a floor — and **water
standing in for the water–ammonia pair overestimates its density by 2.9–3.5 %**, direction
+, above the propagated noise (0.6 %). That is the composition tier's number for the
**ammonia share**; the tier's direction stands. The thermal tier gets a first table-derived
indication that is **not uniform**: ammonia's ∇_ad is 19–45 % below water's at seven points
(the pair's adiabat 3–10 % shallower) and above it at the mantle top (50 GPa, 2830 K: 2.6 %
steeper), under the convention caveat — so it **keeps "sign ungrounded"**. The net tier still needs the tables,
**because methane — the largest share, 0.31 — is still missing.** Ammonia is not wired
into any body; whether it enters the mantle as a declared fraction is the owner's decision,
with the grounds (for, against, and the ceiling below the ice giants' centres) in
`engine/ammonia-table-context-notes.md`. Anchors bit-identical — no path function moved.

**The methane half, re-stated from the full text (2026-08-30, not built).** Sherman, Wilson,
Weeraratne & Militzer 2012, *Ab initio simulations of hot, dense methane during shock
experiments*, Phys. Rev. B 86, 224113 (2012PhRvB..86v4113S, arXiv 1207.2948) is in the
cache as the published PDF and the arXiv LaTeX source. **A table exists and is distributed**:
the source's appendix carries 79 DFT-MD (T, P, E) points with 1σ error bars, marked *"to be
published as online supplementary information"* — the published PDF refers to the
supplement and does not print it. The row's old reason, *not obtained because paywalled*, is
replaced by two that hold with the table in hand:

- **Methane does not persist as a species in the region.** Sherman: *"At a temperature of
  approximately 4000–5000 K, a plateau is reached … the system entering into a polymeric
  regime where the methane molecules spontaneously dissociate to form long hydrocarbon
  chains"*, a regime they show to be metallic; at 6000 K a plasma. Bethkenhagen+ 2017 §III on
  their own runs: *"Pure methane does not become superionic but instead decomposes into
  long-chained molecules in our simulations."* Additive volume assumes each component keeps
  its identity at (P, T); **no mixing error for a dissociating component has been measured
  or published**, so a methane table would not make a linear-mixing mantle grounded.
- **The grid does not cover the region.** Counted from the source (13 densities × 13
  temperatures, 79 cells filled): the low densities stop at 4000 K, only two density lines
  (1.201 and 1.498 g/cm³) run the full 300–75 000 K, and single points sit at 0.600, 1.353,
  2.129 and 2.376 g/cm³. Bethkenhagen+ 2017 §II.3, naming Sherman: *"none of them covers the
  entire pressure-temperature region required for Uranus and Neptune interior models."*

| ρ (g/cm³) | 0.600 | 0.800 | 1.000 | 1.201 | 1.353 | 1.498 | 1.600 | 1.775 | 2.010 | 2.129 | 2.257 | 2.376 | 2.502 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| points | 1 | 5 | 5 | 13 | 1 | 13 | 9 | 9 | 9 | 1 | 6 | 1 | 6 |
| T (K) | 300 | 300–4000 | 300–4000 | 300–75 000 | 2000 | 300–75 000 | 2000–75 000 | 2000–75 000 | 2000–75 000 | 10 000 | 5000–75 000 | 10 000 | 5000–75 000 |

**Measured: the solved mantles do pass the published dissociation thresholds.**
`tools/methane_thresholds.py` reads the frozen convergence point and samples the ice layer:

| | Uranus | Neptune |
|---|---|---|
| ice mantle span | 34.5–820 GPa, 2663–5948 K | 39.2–1016 GPa, 2553–6066 K |
| C–C bonds (> 1100 K and > 10 GPa, Hirai+ via Sherman) | the whole mantle, from its top | the whole mantle, from its top |
| diamond, **C–H system** (> 3000 K) | from 80 GPa (3037 K) to the base — 71 of 78 samples | from 114 GPa (3049 K) — 67 of 76 |
| diamond, **C–O–H system** (> 1600 K) — *the mantle's own chemistry* | **the whole mantle, from its top** (34.5 GPa, 2663 K) — 78 of 78 | **the whole mantle, from its top** (39.2 GPa, 2553 K) — 76 of 76 |
| polymeric 4000 K / 5000 K | 262 GPa / 525 GPa | 334 GPa / 626 GPa |

**The threshold this row first used was the wrong chemical system, and it understated the
crossing** (survey ④, 2026-08-31). 3000 K is C–H, from Hirai+ via Sherman; our mantles are
C–O–H — methane *and water* — and Kadobayashi+ 2021 measure that system directly:
*"…to ultimately form diamond proceeds at **milder temperatures (~1600 K) and pressures
(13–45 GPa) in the C–O–H system than in the C–H system due to the influence of water**"*,
with *"below ~1600 K, diamond formation did not occur, even under prolonged [heating]"*.
Re-run at 1600 K (`tools/methane_thresholds.py`, one constant changed, reproduced by the
directing seat), the count is **78/78 and 76/76 — crossed at the mantle's top**, the
coldest point of either mantle (Neptune's 2553 K) sitting 953 K above the threshold. The
C–H row is kept above it rather than deleted, because it is what the earlier text was
measured against.

So in this recipe's own profiles the entire ice mantle sits above the carbon–carbon bond
threshold, **all of it above the diamond threshold of its own chemistry** (nine tenths, by
the C–H threshold this row first used), and its deeper half inside or beyond the polymeric
regime. That is a measurement, recorded here as grounds
either way; whether carbon separation becomes an item (carbon as its own phase rather than
methane in a mixture) is the owner's decision. **The three-tier sign statement does not
move**: methane's absence is now more precisely stated, and the net still needs tables that
would have to carry a dissociating component — which none published does.

**Opened by the owner 2026-08-31, and surveyed (④).** Four questions were put to the
literature; the answers move the blocker rather than removing it.

*Separation happens, and it has a destination.* Kadobayashi+ 2021 on the C–O–H system:
diamond formation *"can occur throughout the icy mantles of Uranus and Neptune (even in
their upper regions)"*, and the diamond *"settles deep into the icy mantle and accumulates
at the boundary between the icy mantle and rocky core."* The overlap is one-sided, and this
must be carried with the claim: **in temperature our whole mantle is above threshold, but
the experiments reach 45 GPa (C–O–H) and 80 GPa (C–H) against our 34.5–1016 GPa** — they
cover the mantle's top few per cent, and below that the authors are extrapolating.

*An equation of state exists and it reaches us — the survey's first answer was wrong and
was retracted.* Correa+ 2008's multiphase carbon EOS is neither a static-DAC table (≤900 K)
nor a warm-dense-matter one (≥10⁴ K), the two categories the survey had generalised into a
gap. §III: the solid-phase treatment holds *"in the range of our interest (below a pressure
of ~2500 GPa)"*, against our mantle base of 1016 GPa; BC8 becomes *"stable above a pressure
of roughly 1100"* GPa with the cold curves crossing at **1075 GPa**, so Neptune's base sits
inside the diamond field by ~60 GPa; and Correa+ 2006 puts the diamond–BC8–liquid triple
point at **7445 K · 850 GPa**, above our hottest 6066 K, so separated carbon is solid here.
Table I prints the coefficients.

*The cost is a form mismatch, not an absence.* The cold curve is a Vinet fit, which
`eos.Phase` already takes (V₀ = 5.785 Å³/atom → **ρ₀ = 3.4477 g/cc**, recomputed). The
thermal term is not ours: they carry a volume-dependent Debye θ(V) with a Grüneisen
parameter varying with volume plus an anharmonic term, and **our Anderson–Goto form is the
special case where γ₀/V is constant**. So this is an implementation extension with a
measurable error, of the kind the ladder has taken before — not a missing table. The
authors also flag their own bias: V₀ is *"3% larger than that of experiment **once
zero-point motion and thermal expansion have been accounted for** … it may be necessary to
shift V₀ 'by hand'"*, a *"well-known error resulting from the use of GGA-DFT"*. **Only that
3 % is theirs**: dividing their V₀ by a 298 K measurement gives −2.00 % in density and is
not like-for-like — their V₀ is a static-lattice cold-curve parameter with neither
zero-point motion nor thermal expansion in it, and both corrections shrink the experimental
static volume, which is why their number is the larger one.

*And the experimental branch is a table too, not just a range check.* Dewaele+ 2008's
Table III prints a complete Mie–Grüneisen–Debye equation of state for diamond —
V₀ = 5.6693 Å³/atom, K₀ = 444.5 GPa (fixed), K₀′ = 4.18(15), θ₀ = 1860 K fixed *"based on
heat capacity measurements"*, γ₀ = 0.85 fixed *"based on ambient pressure thermal expansion
data"*, with q = 3.6(1.5) the single adjusted parameter; Occelli's 298 K V₀ = 5.6724(19)
sits beside it. It reaches only 80 GPa · 900 K, so it cannot carry our mantle — **but it is
the same function family as Correa's**, which is what makes either of them consumable: one
`Phase` extension takes both, and **the experimental set becomes a low-pressure check on
the first-principles one**. That is a better position than either paper alone.

**And there are two carbon stories, not one** (survey ⑤, 2026-08-31 — the owner asked
whether theory exists where measurement does not). Everything above is **diamond**: a solid
that nucleates, sinks and piles up. The other is **fluid**: Militzer 2024
([`2024PNAS..12103981M`](https://ui.adsabs.harvard.edu/abs/2024PNAS..12103981M), single
author, CC BY; Europe PMC full text cached as `.xml`/`.txt` — the PDF is script-blocked,
not paywalled, and the figures and SI are not in the cache) finds a solar-type
7 H₂O : 4 CH₄ : 1 NH₃ mixture at **343 GPa · 4750 K** — inside our solved mantles, not an
extrapolation — where *"the homogeneous fluid **spontaneously phase separates** into a
water-rich fluid and a C-N-H fluid"*, self-checked as *"not sensitive to the hydrogen
concentration"*, with compositions printed (C₈N₂H₁₁…H₃₄ / C₈N₂H₁₃…H₃₈). **No solid**: the
word `precipitat` appears **0 times** in the distributed full text (counted twice, by the
surveyor and by the directing seat), and `diamond` 5 times — all in the literature review,
where *"the formation of diamond from CH₄ in ice giant interiors has been explored with
theoretical and experimental techniques (17–19)"*. **It cites the diamond work and models
something else.**

That splits both blockers by axis:

| | a theory for *how much* | a target model that has it |
|---|---|---|
| **fluid C-N-H separation** | **yes** — Militzer 2024, first-principles | **yes** — Militzer 2024 builds Concentric MacLaurin Spheroid ensembles that *"match the observed gravity field"*, printing J₂ = 3510.99 and J₄ = −33.61 / −35.8 (×10⁻⁶) as the fit targets |
| **diamond precipitation** | partial — Cheng+ 2023, still C/H with no water | **none found** (three ADS sweeps; Ross 1981 is the idea's origin, Bailey & Stevenson 2021 separates H₂–H₂O, not carbon) |

**So C13's trap is lifted on the fluid axis and stands on the diamond axis** — and choosing
between them is a physics choice, not a gap: Militzer knew the diamond literature and
modelled the other thing. One cost rides along with the fluid axis: their mixture
**contains ammonia** and our column does not, so adopting the theory adopts a composition.

*What blocks the diamond axis is the other two questions.* **How much** carbon separates has no
published rule that includes water (Cheng+ 2023 give coexisting compositions for C/H, with
no water, and the quantity still needs a declared bulk carbon fraction — `composition_intent`,
currently a gap). And **the target does not have this component**: the three-layer practice,
Nettelmann+ 2013 included, represents HCNO molecules by a water equation of state. That is
C13's registered trap — adding what the target lacks and then matching its number means no
longer computing the same thing. Both are owner questions, not literature ones.

*A timescale, not an uncertainty.* Frost+ 2024 measure diamond forming at 2500 K over
19–27 GPa and find it *"took at least 30 µs to form"*, and name why the field splits:
*"the disagreement between static and shock compression studies is the timescale of the
physical processes, which can differ by more than 10 orders of magnitude."* The static and
shock thresholds are one process seen at timescales ten orders apart — so the spread
between them is **a rate, and must not be carried as an error bar**. On planetary
timescales the static side is the relevant one.

### C5 — Where the giants' leftovers belong — **closed 2026-08-30**

Two residuals; both now have an owner, and one has two declarations it can be read against.

**Jupiter, and the diluted core — reached, no consumer.** The mixture rule carries one
homogeneous Z through the envelope. Post-Juno structure is not "graded inward": Debras &
Chabrier 2019 §4.1 (2019ApJ...872..100D, text in the cache) is titled *Inward decreasing
abundance of heavy elements in some part of the outer envelope* — locally ∇Z > 0 — and the
structure needs four regions: an outer convective envelope, a composition-and-entropy
gradient, an inner convective envelope and an extended dilute core. Not implemented: Alpha
Centauri A b's radius is a declaration, so nothing in the roster would read a graded-Z
envelope today. The earlier compact-core attempt and its silicate ceiling stay in the domain
row.

**Corrected 2026-08-31 (survey ⑥) — this row claimed "two transcribable forms exist" and one
of them is not one.** *Helled & Stevenson 2017's* Z(m) is a Gaussian the paper prints and
then disowns twice: the sentence introducing it says *"In such a case (**which is merely
chosen to aid the explanation**)"*, and §I says the validity of their suggestion
*"**doesn't automatically lead to a prediction for the final Z-profile** which depends on the
specific conditions under which the giant planet has formed."* What the paper gives is a
**formation-history relation** plus an illustrative profile computed from a specific Jupiter
formation model — not a form to transcribe. The accurate label is *"a formation-history
relation, and an example Gaussian chosen to aid an argument."* **`Howard, Guillot & Bazot
2023` is a real closed form** and stands: an erf profile whose width parameter δm_dil the
paper *"set[s] to 0.075"*, with no derivation or sensitivity test in the text.

*The consequence for C13*: its registered fourth branch — Helled & Stevenson's ice-envelope
applicability — **closes here, and not for the registered reason.** Not "Jupiter-only, cannot
be transferred" but **there is no function to transfer**; the mechanism's own conditions are
composition-independent, and the profile only ever arrives through a formation model our
bodies do not have.

*And the row was missing the paper that matters most for the ice giants.* **Vazan & Helled
2020** ([`2020A&A...633A..50V`](https://ui.adsabs.harvard.edu/abs/2020A%26A...633A..50V),
arXiv 1908.10682, cached) is about **Uranus**, fits **the moment of inertia directly**
(*"we fit MoI instead of the gravitational moments"*, target **0.222–0.230 MR²**), tests
whether a gradient survives on Gyr timescales with the Ledoux criterion, and tabulates four
adopted models. Its conclusion lands on this list's own open question: *"an interior with a
**mixture of ice and rock, rather than separated ice and rock shells**, is consistent with
measurements, suggesting that **Uranus might not be 'differentiated'**."* It has no closed
Z(r) either — it sweeps *"composition gradients of various slopes"* and selects on R, L and
MoI.

**The ice giants — the residual has an owner, and the question was wrong.** Helled,
Nettelmann & Guillot 2020 (2020SSRv..216...38H, text in the cache): "even a very small (in
mass) H-He atmosphere can imply high interior temperatures, if an adiabatic temperature
profile is assumed" — the +8 % / +14.7 % central-temperature excess is the signature of an
adiabatic H/He envelope, not a missing material, and whether layer transitions are sharp or
gradual is open (their Fig. 4). Nettelmann, Wang & Fortney 2016 (2016Icar..275..107N, text
in the cache) put the mechanism at the **boundary**: a stably stratified thermal boundary
layer at the H/He–ice/rock transition near 0.1 Mbar (their Table 1), whose class II and III
models "yield by a factor of up to about 2 to 3 warmer core temperatures than the class I
models. As a result, the presence of rocks is required in the inner mantle in order to
match the gravity data" (§7); their U15-II has ΔT = 2500 K and U15-III 4700 K (Fig. 9),
≈ 5000 K (≈ 9000 K) higher central temperatures (§6), and their favoured models carry 1× solar
I:R with "the mixing behavior of rocks with … ices … not well-understood". Their negative
result is narrower than it was quoted: the I:R ratio "does not provide a solution to the
**low luminosity**" (§3) — a cooling-time statement, not a gravity-fit one. C4 is not a
candidate for this residual either way.

**Two declarations, integrated without tuning.** `boundary_temperature_jump` (the TBL step at
this recipe's mantle/envelope boundary, 30–40 GPa for the anchors) and
`mantle_rock_fraction` (silicate mixed into the water phases above 2.3 GPa). Published values
for the first (2500 K, 4700 K); no published mass fraction for the second, so a declared grid:

| declaration | Uranus ΔR (T_c) | Neptune ΔR (T_c) |
|---|---|---|
| none (anchor) | +5.48 % (6 160 K) | +8.94 % (6 296 K) |
| ΔT 2500 K | +7.99 % (11 493 K) | +11.50 % (11 886 K) |
| ΔT 4700 K | +10.04 % (15 661 K) | +13.58 % (16 241 K) |
| rock 0.10 | +3.64 % (6 275 K) | +7.02 % (6 401 K) |
| rock 0.20 | +1.83 % (6 369 K) | +5.13 % (6 486 K) |
| ΔT 2500 K + rock 0.10 | +5.61 % (11 630 K) | +9.00 % (11 994 K) |
| ΔT 2500 K + rock 0.20 | +3.26 % (11 718 K) | +6.56 % (12 053 K) |

Read, not fitted: the boundary layer **widens** the radius residual (+2.5 %p per 2500 K) and
raises the centre by ≈ 5 300 K per 2500 K — the same ≈ 5 000 K Nettelmann report for class II;
rock **narrows** it by ≈ 1.8 %p per 0.10. Neither published value closes either planet on its
own; the two together are the chain the paper describes (warmer → less dense → rock), and the
rock fraction that would close it is not a number this recipe has a source for, so it is not
declared. Anchors keep both at 0 and are bit-identical. `engine/giant-residual-context-notes.md`
has the runs and the provenance of every number.

*Revisited 2026-08-31 (C13)* — (a)'s *"reached, no consumer"* was true when written and is
**superseded on the consumer half**: the ice giants' measured C/MR² deficit (−15.8 % /
−11.4 % after the radius is stripped, the gate's 2026-08-31 comparison) is a consumer. The
blocker moved, it did not vanish — not "nothing would read a graded-Z envelope" but "the
recipe cannot yet hold the arrangement it would grade toward": see C13, where the rock-free
extreme refuses at stack build. (b) is untouched.

### C6 — Material ceilings

Each material stops where its evidence stops, and each ceiling is a row that declines by
name. They are listed together because they are one kind of work.

| material | ceiling | what is above it |
|---|---|---|
| `h2o` | 1 TPa · 1800 K **(printed; the data ceiling is ~355 GPa — see below)** | ice X above the knot domain; superionic above the temperature |
| `silicate` | 13.5 TPa | Thomas–Fermi–Dirac (electron degeneracy) |
| `fe_prem` · `fe_eps` | 12 · 20.9 TPa | the same |
| `h_he` | 10⁴ GPa in the giant branch | the table's own edge |

Needs: nothing, unless a body the roster wants is refused by one of them. **Each is a
correctly stated limit, not a defect** — the work here is to keep them honest, not to remove
them. Listed so that a future refusal can be traced to its row rather than re-diagnosed.

**Except one, found 2026-08-31 — `h2o`'s 1 TPa is the spline's knot box, not the source's
data ceiling.** French & Redmer 2015 §III, read in the cached PDF: *"A total number of 92 MD
simulations of these ices were [performed] … The densities were varied between 1.6 and
4.25 g/cm³, and the temperatures were chosen from 295 up to 2000 K… Densities of 4.5 g/cm³
and higher lead to a distortion of the bcc oxygen lattice."* On our own 300 K isotherm
(point evaluations, not a sweep) ρ = 4.201 g/cc at 340 GPa and 4.267 at 360 GPa, so their
highest simulated density sits at **≈355 GPa**; at the printed 1 TPa ceiling our ladder
returns **5.755 g/cc** — 1.35× their highest simulation and well past the 4.5 g/cc where
they say the lattice distorts. **The ladder's upper two thirds in pressure is extrapolation**,
resting on the paper's own §I assurance that the potential "is well behaved in
extrapolation" — a statement about the function's smoothness, not about those values being
verified. This is the fifth failure kind (printed validity range ≠ executed range, the rule
`water2` produced) landing on **our** side rather than a third party's, and the rule's
prescription — record the effective ceiling with the table — is what this paragraph is.

**Where it bites, stated precisely, because the obvious reading is wrong.** It is *not* true
that the anchors stay under 355 GPa: the ice giants' mantles span 34.5–820 GPa (Uranus) and
39.2–1016 GPa (Neptune). They are unaffected for a different reason — their mantles run
2553–6066 K, above `ICE_VII_X_T_MAX` = 1800 K (`eos.py:1840`), so the ladder branch never
fires there and Mazevet carries the column. **The extrapolation therefore bites only on a
cold, dense water column: T < 1800 K above ~355 GPa** — the same cold flank this list has
been tracking all day, and a second reason (beyond "no table at all") that AQUA's high-
pressure 300–1000 K corner is the gain worth having. No answer moves today; what moves is
what this row is allowed to claim.

Depends on: a body that actually hits one.

### C7 — Partial differentiation — **closed 2026-08-30: the intermediate state is not a mixture**

`differentiated: false` integrates rock and metal mixed in one layer and declines when ice
or gas is present. The refusal stays; its reason is raised. It used to say the mixture rule
handles rock and metal only — true of the code, and an invitation to go looking for the
missing rule. Searched 2026-08-30 (additive-volume / ideal / linear mixing for rock + ice,
interior models of undifferentiated icy bodies): **no mixing rule for an ice-bearing layer
exists, and no published bound on the error of using one.** Two reasons, and they are the
content of this closure.

**It is a reaction, not a mixture.** Water and silicate combine into hydrated minerals with
their own density, volume change and heat; that is why hydrated-rock density in the
literature comes from Gibbs-energy minimisation over a mineral database rather than from
mixing two end-member densities. C10 hit the same wall from the other side — no closed-form
hydrated-rock EOS and no ice–rock mixing rule are two faces of one fact.

**It is a process, not a state.** What makes a body neither fully mixed nor fully layered is
how far the water got. Malamud & Prialnik 2015 (2015Icar..246...21M) start from a
homogeneous ice–rock body and follow the multiphase flow of water through porous rock, the
differentiation that results and the aqueous alteration of the rock, with the density profile
from hydrostatic equilibrium maintained through changing composition, pressure and
temperature; Malamud & Prialnik 2013 (2013Icar..225..763M) treat serpentinisation
explicitly, exothermy included; Prialnik & Merk 2008 (2008Icar..197..211P) is the porous
icy-body evolution code both stand on. **Provenance, plainly: all three are Elsevier, no
preprint, and only the abstracts were read.** This closure can say a treatment exists and
what kind it is; it cannot say whether it is transcribable. Malamud & Prialnik 2015 goes on
the owner's paper-request list serving **C7 and C9 at once** — its heat sources include
compaction's gravitational potential energy and serpentinisation, two of the five
exclusions C9 is about.

**This does not touch C10.** C7 forbids mixing water *into* silicate — a reaction. C10 mixes
antigorite with enstatite/PREM: two solids coexisting as grains, each with its own measured
equation of state, which is what a partially serpentinised rock physically is. Volume
additivity between them is standard and is the same shape as the rock–metal rule this
recipe already carries, so C10's interpolation is one declared axis — how serpentinised —
and not the forbidden mixture.

**Revisited 2026-08-30 (F3), from the full text now in the cache.** The stated limit is
removed in the transcribable direction: the paper's EOS (§3.3, eqs. (1)–(7)) is an
**equilibrium closed form in (P, T, X_d) with every coefficient printed** — porosity of ice
ψ_w = 0.45 exp(−β_w(T/T_m)√P) and of rock ψ_d = 0.4 exp(−β_d P) Γ(T_max), volumes added by
the two-layer model — and its only history variable is T_max, one number per shell. It fits
laboratory compaction to 764 MPa, ice I only, no rock melt; at Callisto's and Titan's core
pressures it is out of range and gives ~1 % void, so **it does not reach the deciding region
of C10's three moons; it reaches their crusts.** Both reasons above are confirmed from the
text: serpentinisation is a reaction *"only so long as there is available liquid water"*, and
the front is an output of a 4.6 Gyr multiphase-flow run with no input parameter for how far
melting reached. **One sentence above was too broad and is corrected here in words:** a
mixing rule for an ice-bearing layer *does* exist for the never-wet state — cold ice and rock
grains, each compacted on its own curve, volumes additive (Yasui & Arakawa 2009's two-layer
model, adopted as eq. (1) and reported to reproduce the mixture's compaction curve) — which is
C10's shape; what still has no rule is the reacted, partially differentiated body, and the
refusal stays on that. "No consumer" is therefore a **choice** about the missing front, not an
absence of a treatment. The full text names the declared-front shortcut (*"assuming that
differentiation somehow occurred, without actually computing how"*) and does not take it;
grounds for a middle rung — a declared front plus a cold mixed crust, Callisto and Titan as
consumers — are written as a proposal, not an item, in
`engine/malamud-readthrough-context-notes.md`. C7 stays closed.

### C8 — The temperature branch's validated window — **closed 2026-08-30**

The adiabat had one published check, Unterborn+ 2019 eq. 7 — 4.4 % at 1 R⊕, −17 % at
1.46 R⊕ — and one anchor is a coincidence with an error bar. The second is Noack & Lasbleis
2020 (2020A&A...638A.129N, PDF in the cache): their eq. (22) carries the mantle adiabat to the
CMB with every term printed, valid 0.8–2 M⊕ for Earth-like composition, and all constants
were re-read from the PDF. Their eqs. (20)–(21) are initial post-magma-ocean temperatures and
were not used. Engine against both, Earth-like CMF 0.325 at 1600 K
(`test_interior.py --adiabat`, and the section *Temperature, checked against a published
core-mantle boundary* carries the full table):

| M (M⊕) | R (R⊕) | engine | vs eq. (22) | vs eq. 7 | anchors vs each other |
|---|---|---|---|---|---|
| 0.8 | 0.942 | 2430 K | −2.2 % | −2.9 % | +0.7 % |
| 1.0 | 1.003 | 2526 K | −1.4 % | −4.4 % | +3.1 % |
| 1.5 | 1.123 | 2724 K | −0.7 % | −7.2 % | +7.1 % |
| 2.0 | 1.216 | 2884 K | −0.8 % | −9.5 % | +9.6 % |

The Earth point reproduces the 2562 K an independent reading reported (2563 K) — the
transcription check. So the grade above 1.05 R⊕ rests on a measured spread: the engine is
within 2.2 % of one published estimate and within 9.5 % of the other, and **the two published
estimates disagree with each other by up to 9.7 %**, with the engine between them. The
agreement in absolute temperature is partly two differences cancelling (the paper's 2000 K at
250 km against the engine's 1736 K there; the engine's rise to the CMB 12–14 % steeper than
the paper's damped exponent), and the test pins both. **2 M⊕ (1.22 R⊕) is the paper's own
ceiling**; above it the recipe is back to one anchor, to Unterborn's 1.5 R⊕. Anchors
bit-identical: this added a comparison, not a change to the adiabat.
`engine/adiabat-window-context-notes.md` has the transcription and the runs.

### C9 — Porosity on a heated body — **closed 2026-08-30: a relation exists, and it depends on rheology**

**This row's own prediction was wrong, and is corrected here rather than quietly.** It said
*"this one may close as 'the bound is the answer', which is a legitimate ending."* The
2026-08-30 survey found otherwise, and a row that carries a guess carries the duty to correct
it — left standing, it tells the next reader to skip the search.

The compaction relation (Bierson+ 2019) returns an upper bound on void space, never an
estimate, because melt, differentiation, convection, impacts and tidal heating all remove
porosity and its §2.2 excludes all five. **Three of the five are carried, with
coefficients, by Neumann & Kruse 2019** (2019ApJ...882...47N, open access, full text fetched
through the ADS gateway into the cache and read): Enceladus heated by radionuclides and tidal
dissipation, differentiating through a melting front, its core compacted by creep — their
§2.5, "compaction is a change of the density and volume of a porous material that is being
heated and applied pressure to … facilitated by creep processes on a geologic timescale" —
with the olivine creep laws of Mei & Kohlstedt 2000 and the antigorite law of Amiguet+ 2012,
coefficients for dry olivine (A1–A4), wet olivine (B1–B4) and antigorite (C1–C2) in their
Table 3. Results: core radius 185–205 km, **porous core layer 4–70 km**, ocean ≈10–27 km, ice
shell ≈30–40 km. Convection and impacts: ✗ — still carried by nobody, and said so.

**How it closes.** Not "the bound is the answer" and not "the bound is replaced":

- Bierson's bound stays the **general case**, validated over 123–2326 km diameter; Neumann is
  one body at one size (252 km) and cannot replace a general bound.
- Neumann & Kruse enter as the **branch** for a tidally heated, differentiating body, grade
  analog — **reached and specified, not wired.** The relation is a creep law integrated over
  a thermal history (porosity as a function of time, stress, grain size, water and
  temperature), and this recipe integrates hydrostatics, not time. Wiring it means a thermal
  evolution the recipe does not have; the specification (which creep laws, which table) is
  written so that whoever brings the history finds the branch ready. Consumers, when it is
  wired: the icy anchors that are heated and differentiating — Enceladus first (the paper's
  own body; on the icy roster, solved today with no porosity declared), Europa, and the roster's
  tidally heated moons that declare `tidal_heating`.
- **The path on the day it is wired:** parse Table 3 from the cached publisher HTML
  (`docs/phase3/_papers/2019ApJ...882...47N.html`, whose `<table>` keeps the columns the text
  extraction flattened) or from the publisher PDF (`PUB_PDF` on ADS), bake the creep
  coefficients the way the other tables are baked, and integrate the creep law over a declared
  thermal history — the history being the thing the recipe does not yet have.
- Malamud & Prialnik 2015 (2015Icar..246...21M, on the request list from C7) serves this item
  too: its abstract carries compaction's gravitational potential energy and serpentinisation
  heat as heat sources — two more of the five.

**The discriminator it hands C10, kept on its own layer.** "No porosity is retained for an
antigorite rheology, implying that the core of Enceladus is not dominated by this mineral."
Vance+ 2018 gave two routes to Enceladus's ~2700 kg/m³ — hydrous rock, or anhydrous rock plus
pores — and density alone cannot tell them apart; retained porosity can, because antigorite
is weak and creep closes its pores. **That is a rheology statement, not a density
statement**: Hilairet's antigorite ρ₀ still stands and still lands on Vance's target. What
Neumann adds is that a body *made* of it would not keep its pores. The two live on different
layers; a later session must not read this as a density refutation.

*Revisited 2026-08-31* — **a time axis was considered and rejected** (owner's decision; the
planned C13 was not opened). Not because the recipe lacks an axis, but because **the axis is
a different one**. The Neumann & Kruse relation does not take an age in Gyr. What it takes is
**t₀ — the accretion time after CAI formation, in Ma** (their §2.3), and the outcome turns
on that value at the megayear level: for the wet olivine rheology successful models live in
t₀ ≈ 1.3–1.9 Ma (§3.3), and for the antigorite rheology **no differentiation occurs at all
for t₀ ≥ 5.5 Ma (at ϕ₀ = 0.6)** (§3.4) — because the short-lived isotopes (²⁶Al, ⁵³Mn, ⁶⁰Fe) release their
heat "within the first few millions of years after CAIs" (§2.3; all read from the cached
text this session). The structure is decided within ~5 Ma; the remaining 4.5 Gyr is
bookkeeping. **Feeding `body_age` (Gyr) into this node would give it the number it is least
sensitive to while the number it is most sensitive to stays undefined.** The six consumers
in sight (Uranus, Neptune, Callisto, Titan, Europa, Enceladus) are all solar-system anchors
whose ages are CAI-anchored directly, so inheriting an age from a star does not even arise
for them. For invented bodies neither t₀ nor the initial ²⁶Al abundance derives from the
star's age (Lichtenberg+ 2019 — reported by the directing session as 0–10× solar ²⁶Al₀
across systems, not re-read here): both are **declarations**, not derived values, and
whether to introduce them is a Phase 4 owner decision. Since ²⁶Al matters only for bodies
small enough to be shaped by it, the node never applies to the ice giants. **Do not draw a
`body_age → porosity` edge in the chain**: the edge is real but the payload would be wrong —
it must carry `t_form` (Ma after CAI), not `t_body` (Gyr); a Gyr endpoint is at most an
`influences`. Two papers considered for the request list are dropped with the time axis —
**Kruijer+ 2017** (Jupiter's Hf-W age) and **Castillo-Rogez+ 2009** (Iapetus): both served
only the Gyr-age inheritance question, which no longer exists.

**Revisited 2026-08-30 (F3), from the full text.** The abstract-derived sentence holds and
gets its weights: serpentinisation heat is the second source after radioactivity (an order of
magnitude below it over the run, twice it in the first 200–235 Myr); compaction's
gravitational energy is *"marginal"*, two orders below serpentinisation. Tidal heating,
impacts and convection are still carried by nobody — satellites are excluded from the
paper's sample for the first two. What the text adds is a **third relation of its own kind**:
rock porosity as a closed form in (P, T_max), eq. (5) with a step Γ centred at 675 K that the
authors call *"hypothetical"*, valid to ~0.8 GPa, ice I, no rock melt. It does not replace
Bierson (general) or Neumann (rheology over a history); but its history is one declared
number per shell, T_max ≥ T, and the present T gives the maximum porosity — a bound. For
this relation "reached, no consumer" is a choice about a declaration, not about a thermal
evolution. Transcription note when it is ever wired: the printed eq. (7) exponent
15(T_max/675) − 1 contradicts the text's stated behaviour; 15(T_max/675 − 1) is the form the
text describes. `engine/malamud-readthrough-context-notes.md`. C9 stays closed.

### C10 — Lighter rock — **closed 2026-08-30: the axis exists, and it does not reach**

Callisto, Titan and Enceladus sit **above** every three-layer band: every member of a band
lowers C/MR² as the core grows, so a published value above the zero-core end cannot be reached
by any layering, and the reason was read as the material — rock lighter than the
enstatite-plus-PREM silicate, hydrated or porous. Set aside on 2026-08-26 for want of a
grounded lighter rock; the evidence arrived and was used.

**The material.** Hilairet, Daniel & Reynard 2006 (2006GeoRL..33.2302H, open access, PDF in
the cache): antigorite compressed to 10 GPa with no amorphisation, transition or hysteresis;
their adopted second-order Birch–Murnaghan **V₀ = 2926.23(50) Å³, K₀ = 67.27(123) GPa,
K₀′ = 4**, confirmed by an F–f plot (§3 [13]). The paper prints no ρ₀; it prints the structural
formula (Mg₂.₆₂Fe₀.₁₆Al₀.₁₅)(Si₁.₉₆Al₀.₀₄)O₅(OH)₃.₅₇ (§2 [6]) and "the V₀ value corresponding to
m = 1 … is 172 Å³" (§4 [15]), and from those **ρ₀ = 273.50 u / 172 Å³ = 2640.5 kg/m³** — derived
here from the PDF, matching two earlier independent readings (2638–2640), and checked twice:
2926.23 / 172 = 17.01 is the m = 17 polysome the paper indexes with (Capitani & Mellini 2004),
and the paper's one printed density, 2765 kg/m³ at 5.7 GPa and 470 °C, comes back as 2841 at
room temperature on this curve — +2.7 %, the size and sign of 450 K of expansion.
**Room temperature only**: the paper measures no thermal term and borrows Holland & Powell
1998 where it needs one; that paper is on the request list, and the grade is set by this
deficiency, not by the fit. `test_interior.py` re-derives ρ₀ and re-runs both checks.

**The axis.** `serpentinisation`, a declared fraction of antigorite in the rock layer, mixed
by additive volume with the silicate — **two solids coexisting as grains**, the rock–metal
rule's own shape and not the reaction C7 declined (water *into* silicate). Where the water
went is history, so it is a declaration and drops the grade. Temperature passes through the
antigorite component the way it passes through any phase without thermal constants.

**Bracketing, and the result.** Antigorite sits under the Vance+ 2018 targets (2641 kg/m³ at
Enceladus's 0.023 GPa, 2742 at Callisto's 2.73, 2761 at Titan's 3.28, against ~2700 and
~3100) and the existing silicate sits over them, so the three-layer band was re-run at
fractions 0, 0.25, 0.5, 0.75, 1 — declared, not fitted:

| moon | published | band top f = 0 → 1 | fraction in [0, 1] that closes it |
|---|---|---|---|
| Callisto | 0.3549 | 0.3119 → 0.3321 | **none** — 0.023 short at pure antigorite |
| Titan | 0.3414 | 0.3126 → 0.3334 | **none** — 0.008 short |
| Enceladus | 0.3350 | 0.3008 → 0.3216 | **none** — 0.013 short |

Lightening the rock to pure antigorite closes 40–75 % of each gap and no more. That is the
strong result the brief allowed for: **the answer on these three is not serpentinisation but
void space** — C9's branch, porosity retained on a heated body — or the partial
differentiation C7 declined to model. Two items now answer one question from two sides, and
C9's discriminator keeps its own layer: a body whose core is antigorite-dominated would not
keep its pores (rheology), while Hilairet's density stands (density) — on Enceladus the two
statements together say the pores are in rock that is *not* mostly antigorite, which is
consistent with this table.

**Dante / Hades.** One of the two readings of that open radius question is that the rock is
lighter than this silicate; C10 gives it a tool and does not run it. The judgment is the
owner's.

**Revisited 2026-08-30 (F2), with the overturn condition registered first.** Holland & Powell
1998 is in the cache and antigorite **is** in its Table 5 (atg, a° = 4.70×10⁻⁵ K⁻¹ in
α(T) = a°(1 − 10/√T), κ₂₉₈ = 525 kbar, the C_p polynomial), and Hilairet's §4 borrows from
exactly that paper — the chain holds. The term is carried flattened at 298 K
(αK_T = 1.33 MPa/K with Hilairet's K₀; c_V 966 J/kg/K), from a pure-Mg end-member onto a
natural Fe/Al sample. Re-run on the same grid, the bands are unchanged to four decimals at
every finished point (Enceladus −0.0001 at f ≥ 0.75; Callisto and Titan at f = 0.75 ran past
the sweep's budget, a C3 band defect traced in the notes, not a change in the answer): the
moons' rock sits within ~100 K of the reference and the thermal pressure is ≲ 0.1 GPa
against 2–3 GPa. **No moon reaches its
published C/MR² at any fraction in [0, 1]; C10 stays closed.** The grade stays analog, and
its reason is now the borrowing and flattening, not the term's absence — the sentence that
said otherwise is rewritten here and in the docs. Two ceiling-poking finite differences were
fixed on the way (`eos.Material.k_t`, `interior._adiabatic_dtdp`); no anchor touched.
`engine/antigorite-thermal-context-notes.md` has the transcription and the runs.

### C11 — The middle rung: a declared differentiation front and a never-melted crust — **opened 2026-08-30 on F3's grounds; closed 2026-08-30**

**What it is, and what it is not.** C7 refuses a body that is neither fully mixed nor fully
layered, because ice mixed through rock *where liquid water reached it* is a reaction and a
transport history. **C7 stays closed, and C11 is not its repair.** C11 is the other case F3
found in Malamud & Prialnik 2015's full text: the depth the melting reached is taken as a
**declaration**, and the body is static — metal core, rock, water/ice mantle, and above the
front a crust that never melted, cold ice and rock grains never in contact with liquid water.
Hydration is a story about places liquid water reached, so C7's argument does not apply
there; and for that state a mixing rule exists — Yasui & Arakawa 2009's two-layer model,
adopted as Malamud & Prialnik's eq. (1) and reported to do *"a very good job of reproducing
the compaction curve of the mixture"* (§3.1.3) — the shape C10 already uses for antigorite
plus enstatite. The first row added after the list closed.

**Two declarations, not one.** `differentiation_front` (cumulative mass fraction from the
centre that melted; 1.0 is today's body) and `crust_rock_fraction` — the second because the
source's outer mantle is *not* primordial: it is ice-enriched by water that rose and refroze
(§5.1), so the front alone does not fix the crust's composition; the primordial fraction is
an upper bound. Optional `crust_porosity`: the same paper's eqs. (4)–(6) with Γ = 1 (never
melted), laboratory compaction curves, an **upper bound** on void. Directions registered
before the sweep: crust rock **raises** C/MR², porosity **lowers** it. `_stack` gains the
crust as a fourth layer (ice ladder + silicate as grains, additive volume, no
serpentinisation — water never reached it); a crust step above the melting curve is refused
as a self-contradictory declaration. Grade analog whenever a crust is declared; the
Malamud porosity functions landed first (8786d857) so no intermediate commit is broken.

**The sweep, on a declared grid, not tuned.** Potential temperature 200 K — at the roster's
270 K the crust is refused, because ice Ih/III/V melt at 251–273 K between 0.02 and 0.6 GPa
and a never-melted crust cannot sit there; the reference (front 1.0) is re-run at the same
200 K. `infer_three_layer` over core fractions 0/0.15/0.30/0.45; `test_interior.py
--middle-rung` regenerates it. Band = C/MR² over the core-fraction members that reproduce
the radius:

| moon (published) | front | X_d 0.3 | X_d 0.6 |
|---|---|---|---|
| Callisto (0.3549) | 1.0 | 0.2881–0.3127 (no crust) | — |
| | 0.9 | 0.3010–0.3077 | 0.3155–0.3203 |
| | 0.8 | 0.3107–0.3158 | 0.3393 |
| | 0.7 | 0.3220–0.3348 | **0.3561–0.3643** |
| | 0.6 | 0.3275–0.3390 | 0.3714–0.3768 |
| Titan (0.3414) | 1.0 | 0.2883–0.3138 (no crust) | — |
| | 0.9 | 0.3011–0.3081 | 0.3158–0.3207 |
| | 0.8 | 0.3103–0.3300 | **0.3384–0.3498** |
| | 0.7 | 0.3218–0.3350 | 0.3547–0.3633 |
| | 0.6 | 0.3270–0.3390 | 0.3695–0.3757 |

**Where they land.** C10's grid lay entirely below both published values; C11's grid
**brackets them**. Titan's 0.3414 falls **inside** the band of one declared pair — front
0.8, X_d 0.6 (0.3384 at core 0.15 to 0.3498 at core 0) — closed along the core axis the way
Europa's is, with the declarations untouched. Callisto's 0.3549 falls **between** two
declared pairs: above the front 0.8 · X_d 0.6 band (0.3393) and just below the front 0.7 ·
X_d 0.6 band (0.3561–0.3643), 0.0012 under its low end; no grid point's band contains it,
and the grid is not refined to make one — that would be the fitting C5 and C10 declined.
Porosity on the front 0.7 · X_d 0.6 pair moves the band down as registered: Callisto
0.3561–0.3643 → 0.3390–0.3494, Titan 0.3547–0.3633 → 0.3386–0.3496 (about −0.015, the
laboratory upper bound on crust void). One member did not converge (Callisto, front 0.9 ·
X_d 0.3, core 0.30). The table is the regeneration on the code that
ships (2026-08-30, after the crust-refusal fix was narrowed — see the notes' post-mortem),
identical at all twenty points to the first pass; run times 2–7 min per point; the 270 K
refusal through the inversion route did not finish in 17–24 CPU-minutes and was stopped — the temperature bracket is
exhausted on every solve of the regula falsi — where the direct `solve` refuses in about 12 s.
Recorded as a cost, not fixed here.

**What moves and what does not.** Anchors bit-identical: Uranus and Neptune (the stack's
bounds for a body with a gas envelope reproduce the old expressions to the bit — checked
after a negative-crust bug in the first pass had frozen both as refusals, which is exactly
the failure the anchor exists to catch), Europa's inversion, the rock and giant anchors;
`--refresh` for the fingerprint (`_stack`, `integrate`, `shoot` changed). The Callisto and
Titan question C10 left — *void space or partial differentiation* — now has its second half
measured: a declared front with a rock-bearing crust reaches the published values, a
serpentinisation fraction does not. Which pair, if any, a body should declare is the owner's
call; this row supplies the grid. `engine/middle-rung-context-notes.md`.

### C12 — A ternary anchor from a diffusion table? — **opened 2026-08-31 on the owner's grounds; closed 2026-08-31, recorded**

**A check, not a material — and not a reopening of C4.** Opened when the owner doubted the
report that Bethkenhagen+ 2017's typeset version (`2017ApJ...848...67B.pdf`, in the cache)
carried no usable data — a report made from the text layer twice — and read it as images:
the EOS grid is indeed absent (Figures 1–3 only, no table, no supplement; **C4's methane half
stays on its author-request route**), but **Table 1** prints R · ρ · T · p at thirty state
points along three Uranus profiles beside the real 2:1:4 mixture's self-diffusion
coefficients. If ρ were the mixture's, water-alone could be measured against the real ternary
— the number C4 said needed the tables.

**Settled from the text first**: §4 introduces the table as *"the diffusion coefficients of
each species in the real ternary mixture, as well as radius, density, temperature, and
pressure along the three profiles"* — profile quantities; §2.7 matches the profile's
*pressure* within 2 % and says nothing of tabulating the box's density; the mixture's own
density appears as Figure 4. The text's reading is (나), the profile's density. **The
registered discriminating check then failed on its own premise**: this recipe's water
(Mazevet+ 2019 at all thirty rows) is 18–32 % denser than *every* printed ρ, including the
water-only profile's (29 % at 6.9 GPa · 1775 K → 18 % at 510 GPa · 5750 K), so the column is
not pure water's density anywhere — and both readings can explain that size (an H/He-bearing
inner envelope under (나); a mixture 15–25 % lighter than water under (가), which C4's own
ammonia result makes plausible). **Closed on the conservative branch**: no ternary anchor can
be read from the column with the evidence held; C4's composition tier keeps its water +
ammonia number. What would settle it: Redmer+ 2011's own ρ(R) for the water-only model, or the
authors. **The failed test was the audit session's proposal, fixed into the brief by the
directing session — the responsibility is joint**, recorded the way this project keeps every
error named. *Observation, derived, not a verdict*: the residual shrinks with depth
(+29 % → +16–19 %), which is qualitatively what reading (나) with a small H/He admixture in
the inner envelope would do; Redmer+ 2011's ρ(R) would most likely settle it that way.
**Redmer+ 2011** (Icarus 211, 798, the water-only Uranus model) goes on the owner's
paper-request list; if it prints 1.00 g cm⁻³ at 0.839 R_U, (나) is settled and C12 reopens as
*revisited*. No code, no anchor, no gate change. `engine/ternary-anchor-context-notes.md`.

*Revisited 2026-08-31* — the owner obtained **Redmer+ 2011**
([2011Icar..211..798R](https://ui.adsabs.harvard.edu/abs/2011Icar..211..798R), cached as
`docs/phase3/_papers/2011Icar..211..798R.pdf`), and the expected settle path does not exist
in it: **no ρ(R) table** (Figures 1–3 only, no supplement; the structure models are taken
from Fortney & Nettelmann 2010). **(나) is settled anyway, by a shorter path** — one
sentence of shell geometry instead of a number. Bethkenhagen+ 2017's Figure 3 caption names
the model (*"water-only (Redmer et al. 2011)"*), their §2(i) states what the name means
(*"ices are represented solely by a water EOS"* — the ice component's representation, not
the planet's composition; the model is three-layer with an H/He-rich outer envelope), and
Redmer+ 2011 prints the shell boundaries: *"the ionic water shell extending from 0.6 to
0.8 R_p"*. Table 1's shallowest row sits at **0.839 R_U — above the water shell, inside the
H/He-bearing outer envelope**, where ρ = 1.00 g cm⁻³ is the profile's density and could not
be pure water's; our water being +29 % against it is thereby explained. The verdict does not
move (closed, conservative branch; no ternary anchor; C4's tier keeps water + ammonia — that
Table 1 gives no mixture density is now confirmed, not assumed). What moves is the closure's
quality, from *"could not confirm — the anchor cannot be read under either reading"* to
*"confirmed — reading (나)"*, and the failed test's wrong assumption gets its final name: **a
misreading of the profile's name** — "water-only" states the ice component's composition,
not the body's. Redmer+ 2011 comes **off the request list**: not because it yielded the
number, but because the shell-boundary sentence replaced the need for it. All three quotes
verified against the cached PDFs in this session.

### C13 — Does the fuzzy core account for the moment-of-inertia deficit? — **opened 2026-08-31; the rock axis measured same day — it cannot close the deficit; the ice axis stays open**

**Not C5's repair.** C5(a) recorded a graded-Z envelope as *reached, no consumer* — true
when written. What opened this row is a **measurement**: the ice giants' C/MR² sits
−24.3 % / −25.3 % under Nettelmann+ 2013 (P_Voy, R_mean), and **−15.8 % / −11.4 % remains
after the radius is stripped**. A fuzzy core is the candidate whose sign matches — and sign
is not size (C5(b) taught that: the boundary layer had the plausible direction and widened
the residual).

**The target is a derived value, said plainly**: λ is J₂, J₄ and an assumed rotation period
passed through an interior model — matching 0.230 is agreeing with what the gravity field
permits, not matching nature. And N13's own models are three-layer with **rocks confined to
the core**, so the number this row would chase was produced by a model that does not contain
the thing this row would add; λ being gravity-constrained softens that, but any future
"matched by adding what they did not have" needs its own justification, written here in
advance.

**The non-core terms, bounded first** (each ruled out as the owner of the remainder): the
rotation term — our λ is a non-rotating sphere's — is order 1 % by the axial-vs-mean
identity (2/3)J₂ = 0.00234 / 0.00236, with m_rot = ω²R_eq³/GM = 2.95 % / 2.61 % as the
restructuring scale; the rotation-period spread is a **target-side** spread of −3.3 % /
+6.0 % (attribution measured against P_Voy: IAU baseline, normalization-matched, both
papers' default). Together ≲ 7 % against 11.4–15.8 %: a remainder survives.

**The bracket, and why it could not be held.** As briefed: end A = the anchor's compact
central silicate; end B = the same rock mass (5.43 % / 6.07 % of the planet) spread
uniformly through the envelope (`envelope_z` = 0.283 / 0.321, no silicate layer). **End B
refuses at stack build, at any temperature**: with no silicate at the centre the water
column reaches P_c (1220 / 1533 GPa) and the cold-phase pre-check demands the solid
ladder's coverage, whose French & Redmer 2015 evidence span ends at **1000 GPa** — even
though the answer's deep column is fluid (Mazevet) and never touches the ladder there.
Branch 2's registered assumption ("nothing in the recipe caps the outer extreme") is
**false, with the cap named**. Third member of one family in two days (C11's over-broad
refusal, the Queyroux–Neptune route death): **the trial corridor's cold flank demands
evidence the answer never uses.** The analytic ceiling, computed since the engine could not
(all rock at the surface, structure held fixed — assumptions written): Δλ/λ ≤ f_rock/λ =
+31.2 % / +33.7 %, above the required +18.7 % / +12.9 % — so the fuzzy core **cannot be
excluded**, and is not confirmed: the solvable span was never measured.

**Open, with the settling path named**: the cold-flank representability work (route the
over-depth ladder refusal so the temperature loop stays on the fluid side, or teach the
pre-check that a column can be fluid-only where the answer is), after which end B is two
solves. It is the same prerequisite the Queyroux adoption would need — the two owner
decisions share it. **The registered fourth branch — Helled & Stevenson 2017's
ice-envelope applicability — is closed as of survey ⑥ (see C5's correction): there is no
closed form to apply, because that paper disowns its own Gaussian as illustrative and
delivers a formation-history relation instead.**
Both refusals reproduce in ≤ 1 s. No code, no anchor, no gate change.
`engine/fuzzy-core-context-notes.md`.

*Revisited 2026-08-31, same day — the audit overturned "could not be held": end B was
**1 ULP away**, and the bracket is now measured.* The audit's independent construction
(`imf = 1 − (rock+hhe)/m`) leaves a floating-point residual of +5.6e-17 for Neptune — a
ghost silicate stub that occupies the centre, keeps the water column off the 1000 GPa
ladder cap, and lets the cold flank survive: **1 s refusal vs 112 s convergence on one
ULP.** The directing session pre-registered the reading (λ stable across ε → the ε→0
limit; λ moving with ε → artifact) and ran ε = 1e-7 / 1e-9; this session's runner
reproduced every digit (triple complete), added the float-residual point, and retired the
caveats: **λ is stable across nine orders of ε** (Neptune 0.219683 at 1e-9 vs 0.219617 at
5.6e-17, a 3e-4 relative move; Uranus 0.209756 / 0.209749 at 1e-9 / 1e-7 — its
float-residual point does not exist, because 1 − (0.79+2.0)/14.536 leaves a residual of
exactly 0.0 and dies: **the same expression revives Neptune and leaves Uranus dead**,
which is the cold-flank family's strongest exhibit); the ladder wall does **not** press
Neptune's P_c 984 GPa (a probe at 1010 GPa integrates; mass closure 1.000000); grid
1500 → 6000 moves the radius 3.7–3.9e-4, the anchors' own order. **The measured bracket:**

| | I/(M·R_pub²), end A | end B | target (N13, P_Voy) | gap covered |
|---|---|---|---|---|
| Uranus | 0.1937 | 0.2032 (λ 0.2098, R −1.57 %) | 0.2300 | **26 %** |
| Neptune | 0.2135 | 0.2248 (λ 0.2197, R +1.15 %) | 0.2410 | **41 %** |

**The answer this axis gives: rearranging the declared rock mass — any grading between
compact core and uniform envelope Z — buys at most 26 % / 41 % of the gap. This axis
cannot close the deficit.** What this is *not*: a ceiling on the fuzzy core as the
literature means it, which spreads **ice** as well as rock; the recipe's end B moves only
the declared rock. The remaining owners on the table are that difference (graded ice) and
the ice mantle's own density profile — the ice axis stays open, unmeasured. The stub is an
apparatus, not a repair: that the corridor's boundary sits one floating-point digit from
the answer's path strengthens the structural diagnosis (`f3f3a3fd`), and the general fix
remains the shared prerequisite of both pending owner decisions. Bonus, measured on the
way: end B also **shrinks the radius residual** (Uranus +5.48 % → −1.57 %, Neptune
+8.94 % → +1.15 %) and cools the centre (T_c 4953 / 4901 K) — recorded, not attributed.

*Revisited 2026-08-31, later the same day (Brief 22)* — **the stub is retired: end B
solves with no stub at all.** The cold-flank corridor repair (the rules paragraph;
`engine/cold-flank-context-notes.md`) removed the three static spots, and the
pre-registered acceptance passed: both planets solve under **both** `imf` expressions —
Uranus (residual exactly 0.0, the configuration that died) λ 0.209729 · renorm 0.2032;
Neptune (±5.6e-17) λ 0.219577 / 0.219617 · renorm 0.2248 both ways. 1 ULP no longer gates
solvability, only nudging λ by 1.8e-4 relative, inside the ε-ladder envelope. **The
measured bracket stands stub-free: 26 % / 41 % were not stub-dependent** (branch 4 did
not fire). The ice axis (③) is now measurable without any phantom device — which was the
reason ① was ordered before it.

*Revisited 2026-08-31, Brief 23 — **the ice axis, attempted: representable except one
named wall, and no bracket end converges through it.*** The mixing question was answered
from sources first (Soubiran & Militzer 2015: additive volume for H₂O–H₂ measured good to
a few %, ≤10 % locally, over 2–70 GPa × 1000–6000 K; and N13's own envelopes are LM-REOS
*linear-mixed* water — matching like with like), so branch 4 did not fire. The
representation was built (`envelope_z_rock_fraction`, a dispatching `_EnvelopeWater`
part, and **water1's c_P baked** — the source's own Gibbs quantity, closing the hole that
confined C5(b)'s rock mixing to ≥ 2.3 GPa). All four end-B states (ice / ice+rock × two
planets) close mass exactly and **none converges**: a refusal spy shows 1102 of 1202
trial deaths on one wall — **liquid envelope water at p ≲ 0.1 GPa × 500–1000 K**, the
tri-corner of water1's 500 K top, water2's 0.1 GPa floor and Mazevet's 1000 K floor,
which every path cold enough to reach the 76 / 72 K boundary must cross carrying 85 %
dissolved water. Branch 3, refined: blocker named, with a published filler (IAPWS-95 /
IF97 steam covers it) whose baking is an owner decision. **No gap-covered percentage is
reported** — a bracket end that misses the boundary condition by ~1200 K is not a
measured end. Recorded, not judged: all four states sit *above* the targets (renorm
0.2531–0.3061 vs 0.2300 / 0.2410), and the wedge-crossing is partly the uniform-Z
bracket's own artifact — a graded profile tapers the water toward 1 bar and is not
blocked to the same degree. `engine/ice-axis-context-notes.md`.

**The ice axis, attempted twice and measured as a wall both times — 2026-09-01 (Briefs 23, 25).**
Brief 23 put the declared ice into the envelope as a uniform Z; every bracket end refused, and
**1102 of 1202 refusals sat at one water wall** (p ≲ 0.1 GPa × 500–1000 K — the junction of
water1's 500 K ceiling, water2's 0.1 GPa floor and Mazevet's 1000 K floor). Brief 25 baked
IAPWS-IF97 regions 1–3 to fill exactly that window.

**The steam bake did what it was for: the water wall is retired.** In the same solve the spy
now counts **100 refusals, 100 % of them `h_he`, water 0.** But no end converges, so **no
gap-covered percentage exists** and the registered product is the next wall's coordinates.

**Where it moved, and why the target is unreachable.** The surface pins at **355–363 K
regardless of central temperature, against a declared 76 K.** Every trial adiabat cold enough
to head for 76 K dies on the **H/He table's low-temperature floor**, measured here directly
rather than inferred from the refusals:

| pressure | lowest temperature the `h_he` table will evaluate |
|---|---|
| 130 GPa | **1830 K** |
| 150 GPa | 1900 K |
| 164 GPa | 1945 K |
| 1050 GPa | 3130 K |

The refusal samples sit at 131–1121 K in the first band (130–164 GPa) and 1929–3096 K in the
second (~1046–1062 GPa) — **below the floor in both.** So a cold envelope at those depths has
no representation at all, and the 76 K surface is not reachable from below by any central
temperature. This is a **material ceiling of the kind C6 lists**, met from underneath rather
than above.

*The four ends, recorded and not judged* (λ, then the radius residual, then
`I/(M·R_pub²)`): Uranus B_ice 0.294150 / −10.51 % / 0.2356; Uranus B_both 0.313228 /
−12.81 % / 0.2381; Neptune B_ice 0.299345 / −7.81 % / 0.2544; Neptune B_both 0.305116 /
−5.30 % / 0.2736. All four sit **above** the targets (0.2300 / 0.2410), the same direction as
the earlier attempt with values moved by the surface coming down from ~1275 K to ~360 K.
**None of this is a measurement** — an end that misses its boundary condition is not an end,
and these numbers must not be quoted as the ice axis's coverage.

**The label steam does not buy still rides**: trial paths now *cross* the old wedge on IF97,
and that crossing happens over an unverified additive mixture, outside Soubiran & Militzer's
validated band on both axes (`7769be6e`).

Two defects were found on the way and are registered in the rules above — the re-armed
sentinel that let the temperature loop run 51 attempts against a ceiling of 29, and the
climb that hid the wall from the controller. Both were invisible while every trial died in
the steam wedge first.

**The composition gradient, measured — and the widths that work are the ones that are not
allowed (2026-09-01, Brief 26).** Z(x) as Howard+ 2023's erf, discretised by shell mass. The
implementation's own check came first and passed twice: **width → 0 reproduces the layer stack
bit-identically**, both against the anchor and against a rock-free toy, so the gradient is
continuous with what it replaces rather than a second recipe. It also **clears the wall that
stopped the ice axis** — the uniform-Z end carried heavy material to the surface and dragged
the adiabat under `h_he`'s floor, while a gradient's upper envelope converges to clean H/He
and stays inside the window. That was predicted in Brief 23's landing note and tested here.

**Then the cap excluded the result — and the cap is weaker than "stability".** What route A
actually transcribes is **a description of Vazan & Helled 2020's successful models, not a
stability calculation.** Their sentence, read at its place in the cached text: models matching
radius, luminosity and moment of inertia *"have some **common properties**: in these models the
outer 20% of the planetary radius develop a large-scale convection on top of a stratified inner
region. This convective layer is metal rich for all models except for the two-layer model
(U-1) … heavy-element enrichment of 0.6-0.7."* So the criterion is **"does this look like the
profiles that worked for them"**, not **"is this convectively stable"** — Ledoux is what
*they* used to test survival; the 0.8 R figure is an outcome they observed. The row says so
because the two readings license very different next moves.

Under that criterion, the gradient's span sits below 0.8 R **only at δm_dil = 0.01 and 0.025 —
the two widths that sit on the layer limit and move nothing.** w ≥ 0.05 crosses
0.8 R and w ≥ 0.075 reaches the surface. **Taking route A as transcribed, the reachable
coverage is ~0 %, and the span below is a set of unreachable points.** Route B (deriving our
own ∇X) refuses by name: no radiative gradient exists in this recipe, and the check does not
invent one.

| δm_dil | Uranus renorm | ΔR | Neptune renorm | ΔR |
|---|---|---|---|---|
| 0.01 · 0.025 *(within the cap)* | 0.1937 · 0.1937 | +5.44 % · +5.32 % | 0.2135 · 0.2136 | +8.90 % · +8.78 % |
| 0.05 | 0.1938 | +4.97 % | 0.2137 | +8.37 % |
| 0.075 *(Howard's value)* | 0.1941 | +4.27 % | 0.2140 | +7.58 % |
| 0.125 | 0.1951 | +2.19 % | 0.2153 | +5.50 % |
| 0.20 | 0.1991 | +0.33 % | 0.2200 | **+3.98 %** |
| 0.30 | 0.2081 | **+0.12 %** | 0.2300 | +4.14 % |
| target (N13, P_Voy) | 0.2300 | | 0.2410 | |

All fourteen converged; **no width was adopted** and the observables are reported beside the
grid, never fitted to. The span, if the cap were not there: **39.7 % (Uranus) / 60.0 %
(Neptune)** of the deficit, monotonic in width with no plateau inside the registered grid.
(Neptune's 0.2300 at w = 0.30 equals *Uranus's* target — a coincidence of digits, not a
result.) Shell count is not a knob: 32 → 64 leaves renorm at 0.1941.

**The exclusion's own scope, stated because it bounds the verdict.** The declared family here
is a two-end erf with `z_shallow = 0`; Vazan's stable models put a **metal-rich homogeneous
convective top (Z ≈ 0.6–0.7) above the gradient** — a shape this family cannot express. So the
finding is *"widths that move the answer are outside the cap **for this family**"*, not
*"gradients are unstable."*

**A second product, unasked for: the radius residual collapses.** Uranus **+5.44 % → +0.12 %**,
monotonic. Neptune **+8.90 % → 3.98 % at w = 0.20, then back to 4.14 %** — **non-monotonic,
with its optimum inside the grid**, while renorm rises monotonically for both. So the radius
axis behaves differently from the moment-of-inertia axis, and the two planets behave
differently from each other. Recorded, not judged.

**What this leaves the owner.** A gradient that reaches the numbers exists; a gradient that
reaches them *and* resembles the profiles Vazan found workable does not. Two ways forward,
both declarations of their own: **(a)** find or derive an actual stability cap — this recipe
has never had one, and route A turned out to be a family resemblance rather than a criterion —
or **(b)** widen the declared family to `z_shallow > 0`, which **is Vazan's own successful
shape**, and measure again. (b) is the cheaper honesty: it tests our recipe against the
literature's geometry instead of re-drawing a line around our own answer. Fitting the width
to the observables would have produced 39.7 % / 60.0 % and no way to know this — which is
what the method was chosen to prevent.

## What closing all of these does not do

It does not make the solver answer every body. Brown dwarfs and stars stay out by the line
above, and each material ceiling stays where its evidence stops. What it does is make every
remaining refusal **one this recipe chose**, with a named mechanism and a citation, rather
than one it fell into.

That is the standard the rest of the engine is held to, and it is what "finished" means
here.

## Related

- [`interior-structure-methodology.md`](../docs/reference/interior-structure-methodology.md)
  — the domain table these entries index
- `engine/*-context-notes.md` — the reasoning behind each closed item
- `engine/coverage-review.md` — a 2026-08-27 snapshot, superseded by this file
