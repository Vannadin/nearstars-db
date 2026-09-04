<!-- 내부구조 → 다이나모 인수인계 인벤토리: 자기장 노드가 요구하는 값을 내부구조 도메인이 지금 내는가, 소비자가 실제로 읽는가 -->
# Interior → dynamo handoff — inventory (2026-09-04, evening)

**The question (owner, relayed by the directing seat):** can the interior domain *today* supply what the magnetic
side (`dynamo_rocky`, `dynamo_giant`) asks for? Not "build the dynamo" — measure the supply, and name each place
where it fails. Method: the chain run over the five roster bodies (`run.py`, 35d6eead) with an instrument on
`BodyState.__getitem__` recording **which keys each recipe actually read and from where** (C6 discipline: a read is
counted only when the hook fires, not when a grep finds the name). Probe and raw output: the work seat's scratch
(`handoff_probe.py`, `handoff_probe.log`, `handoff_probe.json`), not the repository.

## §1 Pre-registration (written before the run)

Ⓟ all four `status: gap` edges are stale — every quantity is supplied and consumed · Ⓠ some are real gaps, each of
one of three kinds: **no value** / **value exists, consumer does not read it** / **value exists, no verdict can be
drawn from it** · Ⓡ supply exists but every grade is judgment or below, so the consumer cannot use it · Ⓢ (added
before the run, after the parallel seat read the methodology's printed **Needs**, `rocky-planet-dynamo-methodology.md:24–25`):
the interior domain owes the dynamo exactly one quantity, `conductor_phase`, and already supplies it; every other
interior output the chain draws into `dynamo_rocky` (C14 · C15 · C17 · C20) has **no consumer by the methodology's
design** (`:108–109` — RM22's structure/thermal solver is not re-run per body).

## §2 What the consumers actually read (instrument-fired, per body)

`dynamo_rocky._from_state` (dynamo_rocky.py:263) read, on every body: `mass_earth`, `radius`/`radius_earth`,
`conductor_phase`, `stagnant_lid`, `age_gyr`, `ice_mass_fraction`, `body_class`, `dynamo_regime`, `locked`,
`rotation_period`. **It never read `core_radius`, `q_cmb`, any thermal-history output, or `entropy_production`.**
`dynamo_giant._from_state` (dynamo.py:257) read `mass_earth`, `radius_rj`, `age_gyr`, `body_class`,
`luminosity_lsun`, `rotation_period_h`, `radius_rj_min/max`, `isolated`. **It never read `l_int`.**

| key the dynamo reads | Earth | Pandora | α Cen A b | Luhman 16 A / B |
|---|---|---|---|---|
| `conductor_phase` (core_state) | emit `liquid_outer_solid_inner` · analog · **consumed** | core_state refuses (no `potential_temperature` declared → isothermal, no geotherm) · — · dynamo_rocky reads None → `cannot-say (conductor_phase undecided)` | core_state not ready (raises Missing on a giant) · consumer out of the rocky ladder | same as A b |
| `stagnant_lid` (input, declared) | `false` · declared · consumed | absent · dynamo stops one step earlier | n/a | n/a |
| `ice_mass_fraction` (input; graph name `layer_fractions`) | absent → default 0.0 · consumed as 0 | absent → 0.0 | n/a | n/a |
| `dynamo_regime` (Phase 4 declaration) | absent · both branches emitted | absent | n/a | n/a |
| `locked`, `rotation_period` (tidal_locking) | absent — no recipe | absent | n/a | n/a |
| `radius` (interior_layers / mass_radius_relation) | 1.003 R⊕ · calibrated · consumed (declared `radius_earth` wins) | 0.885 R⊕ · calibrated · consumed | interior refuses (P_c > 12 000 GPa, fe_prem ceiling) | interior refuses (brown dwarf) |
| `radius_rj`, `age_gyr`, `luminosity_lsun` (dynamo_giant) | radius_rj absent → not ready | same | 1.0 R_J · 5.3 Gyr · declared · consumed → B_eq 172 µT calibrated | declared, L_bol measured · consumed → B_eq 44 / 42 mT calibrated |

**Supplied by the interior domain and *not* read by any dynamo (Earth, the only body where they exist):**
`core_radius` 0.547 R⊕ (calibrated) · `q_cmb` 2.75 TW, band 1.54–4.77 (analog) · `core_cmb_temperature_present`
4 028 K, `q_cmb_present` 5.07 TW (analog, C20) · `entropy_production` −69 MW/K, band −264…+238 (analog, C15) ·
`l_int` 21.3 TW (analog, radiogenic only).

## §3 Edge-by-edge verdict (chain.yaml, line numbers at 35d6eead)

Cells: **emit** (per body, grade) · **doc-Needs** (the printed line, or none) · **code-consumes** (hook fired?) · **chain-claims**
(kind/status) · **verdict** — (가) Need printed + code consumes → live · (나) no Need, no consumer → drawn by the chain, not
required (status left as is, the mark is a note; a new status word is the owner's call) · (다) Need printed, not flowing → gap.

| edge | emit | doc-Needs | code-consumes | chain-claims | verdict / ref fix |
|---|---|---|---|---|---|
| `:659` internal_heat_nontidal → dynamo_giant via l_int | Earth 21.3 TW (analog, radiogenic only); every roster giant/BD: supplier refuses by design | none — `scaling:18` lists nothing from the interior; `:78–81` declines to derive L(M, age) | **no** (dipole_field reads `luminosity_lsun` on the BD branch only; `l_int` never read) | requires | (나). ref kept; note added |
| `:677` interior_layers → dynamo_rocky via core_radius | Earth 0.547 R⊕ (calibrated), Pandora emitted | none — not in `rocky:24–25`; `:108–109` "does not re-run RM22's … solver"; the sole claim is Related `:258` | **no** (`ladder()` has no such argument; hook never fired) | requires | (나). ref :23 (Returns) → :258, old kept in note |
| `:678` core_state → dynamo_rocky via conductor_phase | Earth `liquid_outer_solid_inner` (analog); Pandora: core_state refuses (no `potential_temperature`) | `rocky:24`, `:28` | **yes** (hook fired, source core_state, Earth) | requires | (가) live. ref :25 → :24 |
| `:684` composition_intent → dynamo_rocky via layer_fractions | no node emits `layer_fractions`; input `ice_mass_fraction` undeclared on every body → default 0.0 | `rocky:25`, `:27` — the *declared* ice fraction | reads the input (hook fired, source absent → 0.0) | influences · gap | (다) gap, kind **no value** — a declaration, not a solver output. ref :109 → :27 |
| `:686` heat_transport_mode → dynamo_rocky via cmb_heat_flux | Earth q_cmb 2.75 TW, band 1.54–4.77 (analog) from the `cmb_heat_flux` node (Brief 60); from-node has no recipe | none (`:113–114` is prose: stagnant lid → low CMB flux) | **no** (hook never fired) | selects · gap ("내는 노드가 없다" — **stale** since Brief 60) | (나) drawn, not required; the gap note re-typed: value exists, consumer does not read it. ref :70 → :113 |
| `:687` internal_heat_nontidal → dynamo_rocky via geotherm | core_thermal_history (C20): Earth T_cmb,present 4 028 K, q_cmb,present 5.07 TW (analog); no value *named* geotherm | none in either dynamo doc | **no** | requires · gap ("열진화 모형이 필요" — **stale** since C20) | (나) drawn, not required; note re-typed: value exists, consumer does not read it. ref kept (ihl:202) |
| `:725` core_entropy_production → dynamo_rocky | Earth φ −69 MW/K, band −264…+238 (analog) | none (`rocky:183` reports the band, as a result, not a Need) | **no** | influences · gap | (나) drawn, not required; kind: value exists, no verdict can be drawn. ref :60 → :183 |
| `:668` `:669` `:685` `:658` `:660` (dynamo inbound, refs only) | — | Needs on `rocky:24`/`:25`/`:28`, `scaling:27`/`:18` | — | — | refs pointed at Returns lines or blank lines; corrected, old numbers in notes |

## §4 Outcome against the pre-registration

**Ⓢ.** The methodology's printed Needs (`rocky:24–25`) name ten inputs; the interior domain owes **one**,
`conductor_phase`, and supplies it (Earth: emitted, analog, consumed — the hook fired). The other nine are measured or
declared. Of the five interior → dynamo_rocky edges the chain draws beyond the Needs line, **none is a printed
requirement and none is read by the code**; the two whose gap notes said "no supplier" (`:686`, `:687`) were stale
in their reason — `cmb_heat_flux` (Brief 60) and `core_thermal_history` (C20) exist and emit on Earth — and are
re-typed as "value exists, consumer does not read it". `:684` is the one gap of kind "no value", and it is a
*declaration* the roster never makes, not a solver output. `:725` is "value exists, no verdict". Ⓡ does not hold:
every interior supply is calibrated or analog. `dynamo_giant` owes nothing to the interior (`scaling:18`).

**What this answers.** Yes — the interior domain supplies what the dynamo *as written* asks of it. The five drawn
edges are the chain's picture of RM22's *own* solver, which the methodology explicitly does not re-run (`:108–109`);
whether they should become requirements (wiring core_radius, q_cmb, T_cmb(t), φ into a gate the paper does not
give) is a design decision, not a supply failure. Nothing wired; `dynamo_rocky.py` untouched.

**Roster coverage.** Earth is the only body on which the full interior chain resolves. Pandora's stops at
`core_state` for want of a declared `potential_temperature` (and a core-side CMB temperature for C14/C15/C20) — a
declaration gap. Giants and brown dwarfs are outside the rocky chain by design and their dynamo runs on declared
inputs alone (A b: B_eq 172 µT calibrated; Luhman 16 A/B: 44 / 42 mT calibrated).

**Also found, not repaired.** Twelve `ref:` line numbers on dynamo-inbound edges pointed at Returns lines, blank
lines or unrelated gates (parallel seat's sweep, re-checked line by line here); the eleven in this inventory's scope
are corrected with the old number kept in each note. The stale sentences are kept beneath the dated correction.
