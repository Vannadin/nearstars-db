<!-- 어느 재료 쌍의 혼화 경계에 근거가 있고 어디가 비어 있는지 — 빈칸을 보이게 두는 표 -->
# Miscibility pairs — which boundaries have grounding, and which are blank

Written 2026-09-01 by the directing seat, because the owner asked the right question when the
composition-gradient work opened: *"so we would have to research every material property?"*

**No — and this table is why.** Ten materials make 45 pairs in principle. Only the pairs that
**actually meet** in a solved body matter, and only a few of those are reachable by the
roster. The rest stay blank **visibly**, because a blank nobody can see is the failure this
list keeps meeting: C6's ice ladder ran 650 GPa past its source's data because the ceiling in
the table was the spline's knot box, not the evidence. An unmarked gap gets crossed silently.

**What "grounded" means here.** Not "the two dissolve" — that alone changes nothing. It means
a published statement of **where** they become miscible in (P, T), in a form this recipe can
either evaluate or refuse by name. The width of a resulting gradient is a separate question
and no pair's miscibility paper answers it (see the C13 / gradient work: Ledoux gives an
inequality, not a width).

## Where layers actually touch

From `_stack` (`engine/interior.py`): core → rock → ice ladder → crust → envelope, plus the
envelope's own internal mixture. So the contacts a solved body can present are these, and
nothing else:

| contact | materials | which bodies present it |
|---|---|---|
| envelope ↔ ice | `h_he` ↔ `h2o` (and the envelope's dissolved water) | ice giants, sub-Neptunes |
| envelope ↔ rock | `h_he` ↔ `silicate` (dissolved Z is silicate today) | sub-Neptunes with no ice layer, magma worlds |
| ice ↔ rock | `h2o` ↔ `silicate` | every layered icy body; mixed already above 2.3 GPa via `mantle_rock_fraction` |
| rock ↔ core | `silicate` ↔ `fe_prem` / `fe_eps` | every differentiated body |

## The table

| pair | grounded? | source / what is missing | who needs it |
|---|---|---|---|
| **`h_he` ↔ `h2o`** | **candidate named, unread** | Gupta+ 2025, ApJL 982, L35 (arXiv 2407.04685) — *The Miscibility of Hydrogen and Water in Planetary Atmospheres and Interiors*. **Year care: 2024 is the preprint, the journal version is 2025.** Howard+ 2025 (A&A 703, A154, arXiv 2507.06288) applies it to Uranus, Neptune, K2-18 b and TOI-270 d. Neither has been read; the first is the gradient work's position axis. | **C13 / the gradient.** The one pair that is needed now. |
| **`h_he` ↔ `silicate`** | **blank** | Nothing read. The pair is physically real at interior conditions — hydrogen there is a fluid denser than water (1994 kg/m³ at 800 GPa, measured from our own table), and the silicate is above its solidus — so this is dense fluid dissolving into magma, not gas into rock. Published work exists (a third-party tool lists H₂–silicate immiscibility among its features); we have read none of it. | Hot sub-Neptunes and magma worlds. **No body in the confirmed roster presents it**, so it is not queued. |
| **`h2o` ↔ `silicate`** | **partial, and it is a mixture rule rather than a boundary** | The recipe already mixes silicate into the water phases above 2.3 GPa (`mantle_rock_fraction`, C5's second declaration) with **no published mass fraction** — a declared grid, not a miscibility boundary. What is missing is *where* the two become miscible, as opposed to *what happens if we declare that they are*. Vazan & Helled 2020's conclusion pushes on exactly this: *"an interior with a mixture of ice and rock, rather than separated ice and rock shells, is consistent with measurements, suggesting that Uranus might not be 'differentiated'."* | Ice giants, icy moons. **Second in priority** — the paper above asks for it. |
| **`silicate` ↔ `fe_prem` / `fe_eps`** | **not a miscibility question** | Core formation, not dissolution; the recipe handles it as differentiation (`differentiation_front`, C7 / C11), and C7 closed on the grounds that the intermediate state is a reaction and a transport history rather than a mixture. Recorded here so nobody opens it as a miscibility item. | — |
| `h2o` ↔ `nh3` · `antigorite` ↔ anything · the water phases with each other | **not contacts** | These never meet as adjacent layers in `_stack`. `antigorite` is a serpentinisation product inside the rock layer; `nh3` is a separate material; the water phases are one layer whose local representation the integrator swaps by (P, T). | — |

## What this table is not

It does not say the blanks are safe to cross. It says **which crossings we have not grounded**,
so a future session that finds itself needing one meets a named gap instead of an implicit
assumption. That is the whole function.

And one line the gradient work must carry: **a grounded miscibility boundary gives the
transition's position, never its width.** Position is physics we can fetch. Width is a
declaration in every option on the table — cite Howard+ 2023's 0.075, declare a slope and test
it against Ledoux, or fit to the observables. The first two are what this project does; the
third would cost us the moment-of-inertia comparison we use to check ourselves.

## Related

- `interior-core.md` — C5 (the dilute core and its declarations), C6 (material ceilings, and
  the ladder's knot-box ceiling), C13 (the moment-of-inertia deficit and the gradient axis)
- `engine/surveys-2026-08-31-context-notes.md` — where the Gupta and Howard names entered
